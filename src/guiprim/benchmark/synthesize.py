"""Synthesize the GUI-Primitives benchmark from a UI-element corpus.

Input  : JSONL where each line is one screenshot record
         {image_path, image_size:[W,H], elements:[{id,bbox:[x1,y1,x2,y2],type,text,parent_id}], source}
Output : JSONL of minimal-pair items. Items are emitted in *pairs* sharing the
         same screenshot and anchor; the relation word is flipped and the correct
         target swaps with the distractor. `pair_id` links the two.

Why minimal pairs: a model that scores above chance on a pair cannot be
exploiting an object prior, a frequency prior, or a position prior, because the
pixels and the candidate set are identical across the two members — only the
relation word differs. This is the core reviewer-proofing of the benchmark.
"""
from __future__ import annotations
import json
import random
from pathlib import Path
from typing import Any, Iterator

from .primitives import PRIMITIVES, PrimitiveType

Box = list[int]


# ----------------------------- geometry helpers -----------------------------
def cx(b: Box) -> float: return (b[0] + b[2]) / 2.0
def cy(b: Box) -> float: return (b[1] + b[3]) / 2.0
def area(b: Box) -> float: return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def same_band_y(a: Box, b: Box, tol: float = 0.6) -> bool:
    """True if two boxes overlap vertically enough to count as the same row."""
    ov = min(a[3], b[3]) - max(a[1], b[1])
    return ov > tol * min(a[3] - a[1], b[3] - b[1])


def same_band_x(a: Box, b: Box, tol: float = 0.6) -> bool:
    ov = min(a[2], b[2]) - max(a[0], b[0])
    return ov > tol * min(a[2] - a[0], b[2] - b[0])


def contains(outer: Box, inner: Box) -> bool:
    return (outer[0] <= inner[0] and outer[1] <= inner[1]
            and outer[2] >= inner[2] and outer[3] >= inner[3])


def intersects(a: Box, b: Box) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


# --------------------------- per-primitive miners ---------------------------
# Each miner yields dicts: {anchor, target, distractor} for the *first* relation
# of the primitive; the flipped item is produced by swapping target<->distractor.
def _mine_rel_h(els, rng):
    for anchor in els:
        left = [e for e in els if e is not anchor and same_band_y(e["bbox"], anchor["bbox"])
                and cx(e["bbox"]) < anchor["bbox"][0]]
        right = [e for e in els if e is not anchor and same_band_y(e["bbox"], anchor["bbox"])
                 and cx(e["bbox"]) > anchor["bbox"][2]]
        if left and right:
            yield {"anchor": anchor, "target": rng.choice(left),
                   "distractor": rng.choice(right)}


def _mine_rel_v(els, rng):
    for anchor in els:
        above = [e for e in els if e is not anchor and same_band_x(e["bbox"], anchor["bbox"])
                 and cy(e["bbox"]) < anchor["bbox"][1]]
        below = [e for e in els if e is not anchor and same_band_x(e["bbox"], anchor["bbox"])
                 and cy(e["bbox"]) > anchor["bbox"][3]]
        if above and below:
            yield {"anchor": anchor, "target": rng.choice(above),
                   "distractor": rng.choice(below)}


def _mine_containment(els, rng):
    panels = [e for e in els if e["type"] == "panel"]
    for p in panels:
        inside = [e for e in els if e is not p and contains(p["bbox"], e["bbox"])]
        outside = [e for e in els if e is not p and not intersects(p["bbox"], e["bbox"])
                   and e["type"] != "panel"]
        if inside and outside:
            yield {"anchor": p, "target": rng.choice(inside),
                   "distractor": rng.choice(outside)}


def _mine_ordinal(els, rng):
    # Group list items by parent; pick two distinct ordinal slots as a minimal pair.
    # Skip parent_id=None: ungrouped list_items in a real screenshot are not
    # guaranteed to form an ordered list (they may be unrelated buttons), so
    # claiming "first" / "second" of them would be a labeling error.
    from collections import defaultdict
    groups = defaultdict(list)
    for e in els:
        if e["type"] == "list_item" and e.get("parent_id"):
            groups[e["parent_id"]].append(e)
    for items in groups.values():
        if len(items) >= 2:
            items = sorted(items, key=lambda e: cy(e["bbox"]))
            i, j = 0, 1
            yield {"anchor": None, "target": items[i], "distractor": items[j],
                   "ord_target": i, "ord_distractor": j, "_items": items}


def _mine_alignment(els, rng):
    for anchor in els:
        row = [e for e in els if e is not anchor and same_band_y(e["bbox"], anchor["bbox"])]
        col = [e for e in els if e is not anchor and same_band_x(e["bbox"], anchor["bbox"])]
        if row and col:
            yield {"anchor": anchor, "target": rng.choice(row),
                   "distractor": rng.choice(col)}


def _mine_proximity(els, rng):
    for anchor in els:
        others = [e for e in els if e is not anchor and e["type"] == anchor["type"]]
        if len(others) >= 2:
            ranked = sorted(others, key=lambda e: (cx(e["bbox"]) - cx(anchor["bbox"])) ** 2
                            + (cy(e["bbox"]) - cy(anchor["bbox"])) ** 2)
            yield {"anchor": anchor, "target": ranked[0], "distractor": ranked[-1]}


def _mine_occlusion(els, rng):
    overlays = [e for e in els if e["type"] == "overlay"]
    if not overlays:
        return
    ov = overlays[0]["bbox"]
    hidden = [e for e in els if e["type"] != "overlay" and intersects(e["bbox"], ov)
              and not contains(e["bbox"], ov)]
    visible = [e for e in els if e["type"] != "overlay" and not intersects(e["bbox"], ov)]
    if hidden and visible:
        yield {"anchor": rng.choice(hidden), "target": rng.choice(visible),
               "distractor": rng.choice(hidden)}


_MINERS = {
    PrimitiveType.REL_POS_H: _mine_rel_h,
    PrimitiveType.REL_POS_V: _mine_rel_v,
    PrimitiveType.CONTAINMENT: _mine_containment,
    PrimitiveType.LIST_ORDINAL: _mine_ordinal,
    PrimitiveType.ALIGNMENT: _mine_alignment,
    PrimitiveType.PROXIMITY: _mine_proximity,
    PrimitiveType.OCCLUSION: _mine_occlusion,
}

_ORD_WORDS = ["first", "second", "third", "fourth", "fifth", "sixth"]


def _instruction(prim, relation_idx: int, cand: dict, rng) -> str:
    prim_def = PRIMITIVES[prim]
    tpl = rng.choice(prim_def.templates)
    if prim == PrimitiveType.LIST_ORDINAL:
        ordn = cand["ord_target"] if relation_idx == 0 else cand["ord_distractor"]
        return tpl.format(ord=_ORD_WORDS[ordn], rel="", anchor="")
    rel = prim_def.relations[relation_idx]
    anchor_txt = (cand["anchor"]["text"] if cand.get("anchor") else "anchor")
    return tpl.format(rel=rel, anchor=anchor_txt, ord="")


def synthesize(corpus_path: str | Path, primitives: list[str], n_items: int,
               seed: int, min_elements: int = 4) -> list[dict[str, Any]]:
    """Build the benchmark. Returns a list of item dicts (see module docstring)."""
    rng = random.Random(seed)
    records = [json.loads(l) for l in Path(corpus_path).read_text().splitlines() if l.strip()]
    ptypes = [PrimitiveType(p) for p in primitives]
    items: list[dict[str, Any]] = []
    pair_id = 0
    # Round-robin over primitives so coverage is balanced even if n_items is small.
    per_prim_target = max(1, n_items // (2 * len(ptypes)))
    counts = {p: 0 for p in ptypes}

    rng.shuffle(records)
    for rec in records:
        els = [e for e in rec["elements"] if e["type"] != "panel" or True]
        if len(els) < min_elements:
            continue
        for prim in ptypes:
            if counts[prim] >= per_prim_target:
                continue
            for cand in _MINERS[prim](list(rec["elements"]), rng):
                # Emit the minimal pair: relation 0 (target) and relation 1 (flip).
                for ridx, key in ((0, "target"), (1, "distractor")):
                    tgt = cand[key]
                    items.append({
                        "item_id": f"{rec.get('source','c')}-{pair_id}-{ridx}",
                        "pair_id": pair_id,
                        "primitive": prim.value,
                        "relation_idx": ridx,
                        "relation": (PRIMITIVES[prim].relations[ridx]
                                     if prim != PrimitiveType.LIST_ORDINAL
                                     else _ORD_WORDS[cand["ord_target"] if ridx == 0
                                                     else cand["ord_distractor"]]),
                        "image_path": rec["image_path"],
                        "image_size": rec["image_size"],
                        "instruction": _instruction(prim, ridx, cand, rng),
                        "anchor_id": (cand["anchor"]["id"] if cand.get("anchor") else None),
                        "target_bbox": tgt["bbox"],
                        "target_id": tgt["id"],
                        "distractor_bbox": cand["distractor" if key == "target"
                                                else "target"]["bbox"],
                        "source": rec.get("source", "corpus"),
                        "split": "pool",
                    })
                pair_id += 1
                counts[prim] += 1
                break  # one pair per (image, primitive) keeps the set decorrelated
        if all(counts[p] >= per_prim_target for p in ptypes):
            break
    rng.shuffle(items)
    return items


def write_items(items: list[dict[str, Any]], out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
