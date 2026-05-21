"""Identify 'localization heads' in an open VLM.

Method follows Kang et al., "Your Large Vision-Language Model Only Needs A Few
Attention Heads For Visual Grounding" (arXiv 2503.06287): a small subset of
attention heads concentrate their attention on the image region relevant to the
instruction. We score every (layer, head) on a probe set by two quantities:

  image_mass    — mean fraction of the head's last-token attention that lands on
                  image tokens (a head must look at the image to localize).
  spatial_focus — 1 - normalized spatial entropy of that attention over the
                  patch grid (a localizing head is spatially peaked, not diffuse).

A head's score is image_mass * spatial_focus, averaged over the probe set. The
top-K heads are saved and consumed by steering.py.

This is also a standalone interpretability result for the paper: it shows
*where* grounding lives inside the model, and whether better-grounding models
have cleaner localization heads.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
from typing import Any

from ..logging_utils import get_logger
from ..models.base import VLMWrapper

log = get_logger()


def _spatial_entropy(head_attn, rows: int, cols: int) -> float:
    """Normalized entropy of an attention vector reshaped to the patch grid."""
    import numpy as np
    v = np.asarray(head_attn, dtype=float)
    n = rows * cols
    if v.size < n or n <= 1:
        return 1.0
    v = v[:n]
    s = v.sum()
    if s <= 0:
        return 1.0
    p = v / s
    ent = -np.sum(np.where(p > 0, p * np.log(p + 1e-12), 0.0))
    return float(ent / math.log(n))  # in [0,1]


def score_heads(model: VLMWrapper, probe_items: list[dict[str, Any]],
                ) -> dict[str, Any]:
    """Score all heads on the probe set. Returns per-head scores + a ranking."""
    if not model.supports_attention_capture:
        raise RuntimeError(f"{model.key} cannot capture attention")
    import numpy as np

    accum_mass = None
    accum_focus = None
    used = 0
    for it in probe_items:
        try:
            cap = model.capture_attention(it["image_path"], it["instruction"])
        except Exception as e:
            log.warning("attention capture failed for %s: %s", it["item_id"], e)
            continue
        attn = cap["attn"].numpy()             # [L, H, Timg]
        rows, cols = cap["grid"]
        L, H, _ = attn.shape
        if accum_mass is None:
            accum_mass = np.zeros((L, H))
            accum_focus = np.zeros((L, H))
        # image_mass: attn rows are already restricted to image tokens, and the
        # full-sequence rows sum to 1, so the per-head sum here IS the image mass.
        accum_mass += attn.sum(axis=-1)
        for li in range(L):
            for hi in range(H):
                accum_focus[li, hi] += 1.0 - _spatial_entropy(attn[li, hi], rows, cols)
        used += 1

    if used == 0:
        raise RuntimeError("no probe items produced attention; check capture path")
    mass = accum_mass / used
    focus = accum_focus / used
    score = mass * focus
    L, H = score.shape
    ranking = sorted(((float(score[l, h]), l, h) for l in range(L) for h in range(H)),
                     reverse=True)
    return {
        "model": model.key, "n_probe": used, "n_layers": L, "n_heads": H,
        "ranking": [{"layer": l, "head": h, "score": s,
                     "image_mass": float(mass[l, h]), "spatial_focus": float(focus[l, h])}
                    for s, l, h in ranking],
    }


def save_heads(result: dict[str, Any], out_path: str | Path, top_k: int = 16) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result = dict(result)
    result["top_k"] = top_k
    result["selected"] = result["ranking"][:top_k]
    out_path.write_text(json.dumps(result, indent=2))
    return out_path
