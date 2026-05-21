"""Inference loop.

Runs one model over a list of benchmark items and writes one JSONL prediction
record per item. Records carry everything eval needs (predicted coordinate,
ground-truth box, primitive, pair id) so evaluation never has to re-join data.

Resumability: if an output file exists, already-finished item_ids are skipped.
This matters on a cluster where a 4-day job may be pre-empted.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Any, Callable, Iterable

from ..logging_utils import get_logger
from ..models.base import VLMWrapper

log = get_logger()


def _done_ids(out_path: Path) -> set[str]:
    if not out_path.exists():
        return set()
    ids = set()
    for line in out_path.read_text().splitlines():
        if line.strip():
            ids.add(json.loads(line)["item_id"])
    return ids


def run_model_on_items(
    model: VLMWrapper,
    items: list[dict[str, Any]],
    out_path: str | Path,
    instruction_fn: Callable[[dict], str] | None = None,
    system: str | None = None,
    image_root: str | Path = "",
) -> Path:
    """Evaluate `model` on `items`, appending prediction records to `out_path`.

    instruction_fn lets interventions (CoT, Set-of-Mark) rewrite the instruction
    or the image path per item without changing this loop.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = _done_ids(out_path)
    if done:
        log.info("resuming %s: %d items already done", out_path.name, len(done))

    with open(out_path, "a") as f:
        for i, it in enumerate(items):
            if it["item_id"] in done:
                continue
            instr = instruction_fn(it) if instruction_fn else it["instruction"]
            img = it.get("_render_path") or str(Path(image_root) / it["image_path"]) \
                if image_root else it.get("_render_path", it["image_path"])
            t0 = time.time()
            try:
                res = model.ground(img, instr, system=system)
                rec = {
                    "item_id": it["item_id"],
                    "pair_id": it.get("pair_id"),
                    "primitive": it.get("primitive"),
                    "relation": it.get("relation"),
                    "instruction": instr,
                    "image_path": it["image_path"],
                    "target_bbox": it.get("target_bbox"),
                    "distractor_bbox": it.get("distractor_bbox"),
                    "pred_xy": list(res.pred_xy) if res.pred_xy else None,
                    "raw_text": res.raw_text,
                    "latency_s": round(time.time() - t0, 3),
                    "meta": res.meta,
                }
            except Exception as e:  # never let one bad item kill a 4-day run
                log.warning("item %s failed: %s", it["item_id"], e)
                rec = {"item_id": it["item_id"], "primitive": it.get("primitive"),
                       "pred_xy": None, "error": str(e),
                       "target_bbox": it.get("target_bbox")}
            f.write(json.dumps(rec) + "\n")
            f.flush()
            if (i + 1) % 50 == 0:
                log.info("  %d / %d done", i + 1, len(items))
    return out_path
