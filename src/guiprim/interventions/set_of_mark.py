"""Intervention 2 — GUI Set-of-Mark (SoM).

Overlays numbered marks on the candidate UI elements of an item and asks the
model to name the mark to click. This follows Yang et al. (Set-of-Mark Prompting,
arXiv 2310.11441): turning regions into "speakable" symbols decouples the
language decision from sub-pixel coordinate regression.

This repo's variant marks the candidate set the minimal pair is built from
(target + distractor, plus any extra `candidate_boxes` carried on the item). It
supports two output modes:
  * "id"     — model returns a mark number; resolved to that mark's box center.
  * "coord"  — marks are visual scaffolding only; model still returns click(x,y).
The paper reports "id" as the headline SoM and "coord" as an ablation.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Any

_MARK_COLOR = (255, 64, 0)


def _candidate_boxes(item: dict) -> list[list[int]]:
    boxes = [item["target_bbox"], item["distractor_bbox"]]
    boxes += item.get("candidate_boxes", [])
    # De-duplicate while preserving order.
    seen, uniq = set(), []
    for b in boxes:
        key = tuple(b)
        if key not in seen:
            seen.add(key)
            uniq.append(list(b))
    return uniq


def render_marked_image(item: dict, out_dir: str | Path,
                        rng_seed: int = 0) -> tuple[str, dict[int, list[int]]]:
    """Draw numbered marks on candidate elements. Returns (path, {mark_id: bbox}).

    Mark order is shuffled deterministically by item_id so the correct answer is
    not always mark 1 — a necessary control against a positional answer prior.
    """
    import random
    from PIL import Image, ImageDraw

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(item["image_path"]).convert("RGB")
    draw = ImageDraw.Draw(img)

    boxes = _candidate_boxes(item)
    order = list(range(len(boxes)))
    random.Random(hash(item["item_id"]) ^ rng_seed).shuffle(order)

    mark_map: dict[int, list[int]] = {}
    for mark_id, idx in enumerate(order, start=1):
        b = boxes[idx]
        draw.rectangle(b, outline=_MARK_COLOR, width=4)
        tag = (b[0], max(0, b[1] - 18))
        draw.rectangle((tag[0], tag[1], tag[0] + 22, tag[1] + 18), fill=_MARK_COLOR)
        draw.text((tag[0] + 5, tag[1] + 3), str(mark_id), fill=(255, 255, 255))
        mark_map[mark_id] = b

    path = out_dir / f"som_{item['item_id']}.png"
    img.save(path)
    return str(path), mark_map


def som_instruction(item: dict, mode: str = "id") -> str:
    if mode == "id":
        n = len(_candidate_boxes(item))
        return (f"{item['instruction']}\n"
                f"The candidate elements are marked 1-{n}. "
                f"Respond with ONLY the mark number to click, e.g. 'mark 2'.")
    return (f"{item['instruction']}\n"
            "Numbered marks highlight the candidates. Output ONLY click(x, y).")


def apply_set_of_mark(items: list[dict[str, Any]], out_dir: str | Path,
                      mode: str = "id") -> list[dict[str, Any]]:
    """Return new item dicts prepared for a SoM run (marked image + rewritten
    instruction + `_mark_map`/`_som_mode` for the runner's resolver)."""
    prepared = []
    for it in items:
        path, mark_map = render_marked_image(it, out_dir)
        nit = dict(it)
        nit["_render_path"] = path
        nit["instruction"] = som_instruction(it, mode)
        nit["_mark_map"] = {str(k): v for k, v in mark_map.items()}
        nit["_som_mode"] = mode
        prepared.append(nit)
    return prepared


def resolve_mark(raw_text: str, mark_map: dict[str, list[int]]) -> tuple[float, float] | None:
    """Map an 'id'-mode model response to a click coordinate (center of the mark)."""
    m = re.search(r"\b(\d+)\b", raw_text or "")
    if not m:
        return None
    box = mark_map.get(m.group(1))
    if not box:
        return None
    return ((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)
