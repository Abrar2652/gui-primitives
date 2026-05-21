"""Intervention 3 — training-free representation steering.

Two modes, both inference-time and weight-free:

ACTIVATION steering (primary; precedent: SteerVLM, EMNLP 2025 Findings).
  We derive a steering vector per decoder layer as the mean-difference between
  hidden states on items the model grounded CORRECTLY vs INCORRECTLY in the
  diagnostic (a CAA-style contrast). At inference we add `alpha * unit(vector)`
  to the residual stream at the chosen layers via forward hooks. No training,
  no extra parameters; fully reversible.

ATTENTION steering (experimental; precedent: localization heads, 2503.06287).
  Boost the attention of the identified localization heads onto image tokens.
  This requires the model to run with eager attention and a per-family patch
  point; it is provided as a scaffold and is OFF by default. Verify per model
  before reporting (see CLAUDE.md, "Gotchas").

The two are complementary evidence: activation steering shows the *residual
stream* carries a recoverable grounding signal; attention steering shows the
*localization heads* are the lever.
"""
from __future__ import annotations
import contextlib
from typing import Any

from ..logging_utils import get_logger

log = get_logger()


def _decoder_layers(hf_model):
    """Best-effort handle on the language decoder layer list across VLM families."""
    for path in ("model.language_model.layers", "language_model.model.layers",
                 "model.layers", "model.model.layers"):
        obj = hf_model
        try:
            for attr in path.split("."):
                obj = getattr(obj, attr)
            if hasattr(obj, "__len__"):
                return obj
        except AttributeError:
            continue
    raise RuntimeError("could not locate decoder layers; add this family's path")


# ----------------------------- activation mode -----------------------------
def derive_activation_vectors(model, scored_records: list[dict[str, Any]],
                              layers: list[int]) -> dict[int, "Any"]:
    """Build per-layer steering vectors from correct-vs-incorrect contrast.

    `scored_records` must contain `correct` and the item's image/instruction so
    we can re-run a forward pass and read hidden states.
    """
    import torch
    hf = model.model
    decoder = _decoder_layers(hf)
    captured: dict[int, list] = {l: [] for l in layers}

    def make_hook(layer_idx):
        def hook(_m, _inp, out):
            h = out[0] if isinstance(out, tuple) else out
            captured[layer_idx].append(h[:, -1, :].detach().float().cpu())
        return hook

    handles = [decoder[l].register_forward_hook(make_hook(l)) for l in layers]
    labels: list[bool] = []
    try:
        for r in scored_records:
            inputs, _ = model._build_inputs(r["image_path"], r["instruction"],
                                            "You are a GUI grounding assistant.")
            with torch.no_grad():
                hf(**inputs, use_cache=False)
            labels.append(bool(r["correct"]))
    finally:
        for h in handles:
            h.remove()

    vectors: dict[int, Any] = {}
    for l in layers:
        stack = torch.cat(captured[l], dim=0)               # [N, D]
        pos = stack[[i for i, c in enumerate(labels) if c]]
        neg = stack[[i for i, c in enumerate(labels) if not c]]
        if len(pos) == 0 or len(neg) == 0:
            log.warning("layer %d: missing a class, skipping vector", l)
            continue
        diff = pos.mean(0) - neg.mean(0)
        vectors[l] = diff / (diff.norm() + 1e-8)            # unit vector
    return vectors


@contextlib.contextmanager
def activation_steering(model, vectors: dict[int, Any], alpha: float = 4.0):
    """Context manager: while active, add alpha*vector to the residual stream."""
    decoder = _decoder_layers(model.model)
    handles = []

    def make_hook(vec):
        def hook(_m, _inp, out):
            v = vec.to(out[0].device if isinstance(out, tuple) else out.device)
            if isinstance(out, tuple):
                return (out[0] + alpha * v,) + out[1:]
            return out + alpha * v
        return hook

    for l, vec in vectors.items():
        handles.append(decoder[l].register_forward_hook(make_hook(vec.to(
            next(model.model.parameters()).dtype))))
    try:
        yield
    finally:
        for h in handles:
            h.remove()


# ----------------------------- attention mode ------------------------------
@contextlib.contextmanager
def attention_steering(model, heads: list[dict], image_span, boost: float = 2.0):
    """EXPERIMENTAL scaffold. Boost selected heads' attention onto image tokens.

    Requires the HF model to be loaded with attn_implementation='eager' and a
    per-family hook into the attention probabilities. Left as a NotImplemented
    stub on purpose so a run cannot silently report un-verified numbers — fill
    in the family-specific patch and remove the guard once validated.
    """
    raise NotImplementedError(
        "attention_steering requires a verified per-family patch point; "
        "use activation_steering for the headline results (see steering.py docs)")
    yield  # pragma: no cover
