#!/usr/bin/env python
"""Convert ServiceNow/ui-vision element_grounding annotations into the unified
GUI-Primitives UI corpus schema (data/schema/ui_corpus.schema.json).

UI-Vision element_grounding ships three annotation files (basic / functional /
spatial). Each row is one (image, element_bbox, instruction) tuple — no
per-screenshot element pool and no parent/container structure. To feed the
minimal-pair synthesizer, this converter:

  1) Groups all annotations by `image_path` to build a per-screenshot element pool.
  2) De-duplicates near-identical bboxes (centers within 4 px AND > 80% IoU).
  3) Maps (category, element_type) -> the synthesizer's element `type`.
  4) Heuristically infers `parent_id` by full bbox-containment between annotated
     elements (a button drawn fully inside a larger annotated region becomes its
     child). This is what unlocks the `containment` and `list_ordinal` primitives
     on real screenshots.
  5) Heuristically groups vertically-stacked Menu elements with overlapping x
     ranges under a synthetic `menu-group-<n>` parent, so `list_ordinal` can fire
     on real menu lists.

Occlusion is not present in UI-Vision element_grounding; it stays a
synthetic-only primitive (transparently disclosed in the paper).

Usage:
    python scripts/convert_ui_vision.py \\
        --annotations <ui-vision-dir>/annotations \\
        --images <ui-vision-dir>/images \\
        --out data/ui_corpus/corpus.jsonl
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from pathlib import Path

# (category, element_type) -> unified element type
_TYPE_MAP = {
    ("Button", "icon"):           "button",
    ("Button", "text"):           "button",
    ("Input Elements", "icon"):   "input",
    ("Input Elements", "text"):   "input",
    ("Menu", "icon"):             "list_item",
    ("Menu", "text"):             "list_item",
}


def _bbox_area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def _iou(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    union = _bbox_area(a) + _bbox_area(b) - inter
    return inter / union if union > 0 else 0.0


def _contains(outer, inner, slack: float = 1.0) -> bool:
    """outer fully contains inner (with `slack` pixels of tolerance)."""
    return (outer[0] - slack <= inner[0] and outer[1] - slack <= inner[1]
            and outer[2] + slack >= inner[2] and outer[3] + slack >= inner[3]
            and _bbox_area(outer) > _bbox_area(inner))


def _load_annotations(ann_dir: Path) -> dict[str, dict]:
    """Return {image_path: {"elements": [...], "size": [W,H], "platform": ...}}."""
    by_img: dict[str, dict] = defaultdict(
        lambda: {"elements": [], "size": None, "platform": None})
    seen_per_img: dict[str, list[tuple[tuple, str]]] = defaultdict(list)
    files = [
        ("basic", ann_dir / "element_grounding" / "element_grounding_basic.json"),
        ("functional", ann_dir / "element_grounding" / "element_grounding_functional.json"),
        ("spatial", ann_dir / "element_grounding" / "element_grounding_spatial.json"),
    ]
    for split, path in files:
        if not path.exists():
            continue
        for rec in json.load(open(path)):
            img = rec["image_path"]
            by_img[img]["size"] = rec["image_size"]
            by_img[img]["platform"] = rec.get("platform")
            bb = tuple(round(x, 1) for x in rec["bbox"])
            # Dedup: if a near-identical bbox is already present, keep the BASIC
            # prompt (likely a label) and otherwise skip.
            duplicate = False
            for prev_bb, prev_split in seen_per_img[img]:
                if _iou(bb, prev_bb) > 0.8 and split != "basic":
                    duplicate = True
                    break
            if duplicate:
                continue
            seen_per_img[img].append((bb, split))
            by_img[img]["elements"].append({
                "bbox": list(rec["bbox"]),
                "category": rec.get("category"),
                "element_type": rec.get("element_type"),
                "prompt": rec.get("prompt_to_evaluate") or "",
                "split": split,
            })
    return by_img


def _infer_parents(elements: list[dict]) -> None:
    """Set elements[i]['parent_id'] by full bbox containment.

    If element A fully contains element B and A is larger, A is B's parent. We
    pick the *smallest containing* element as the parent (tightest panel).
    """
    n = len(elements)
    for i, child in enumerate(elements):
        best_parent = None
        best_area = float("inf")
        for j, cand in enumerate(elements):
            if i == j:
                continue
            if _contains(cand["bbox"], child["bbox"]):
                a = _bbox_area(cand["bbox"])
                if a < best_area:
                    best_area = a
                    best_parent = elements[j]["_id"]
        child["parent_id"] = best_parent


def _group_menus(elements: list[dict], img_w: int) -> None:
    """Cluster vertically-stacked Menu elements with overlapping x-ranges.

    Each cluster gets a synthetic parent_id `menu-group-<k>`. Members are
    retyped to `list_item` so `_mine_ordinal` will pick them up.
    """
    menus = [e for e in elements if (e.get("category") == "Menu") and not e.get("parent_id")]
    if len(menus) < 2:
        return
    menus = sorted(menus, key=lambda e: e["bbox"][1])  # by top-y
    clusters: list[list[dict]] = []
    for e in menus:
        placed = False
        for c in clusters:
            ref = c[-1]
            # x-overlap >= 50% of the narrower box AND y-gap <= 1.5x the box height
            ax1, ax2 = ref["bbox"][0], ref["bbox"][2]
            bx1, bx2 = e["bbox"][0], e["bbox"][2]
            xov = max(0.0, min(ax2, bx2) - max(ax1, bx1))
            narrower = min(ax2 - ax1, bx2 - bx1) or 1.0
            yh = max(ref["bbox"][3] - ref["bbox"][1], e["bbox"][3] - e["bbox"][1]) or 1.0
            ygap = e["bbox"][1] - ref["bbox"][3]
            if xov / narrower >= 0.5 and -0.2 * yh <= ygap <= 1.5 * yh:
                c.append(e)
                placed = True
                break
        if not placed:
            clusters.append([e])
    for k, c in enumerate(clusters):
        if len(c) < 2:
            continue
        gid = f"menu-group-{k}"
        for member in c:
            member["parent_id"] = gid
            member["element_type"] = "text"
            # Ensure the unified type becomes "list_item" downstream.
            member["category"] = "Menu"


def _short_text(prompt: str, max_len: int = 40) -> str:
    """Trim a prompt down to a label-like string for instruction templating."""
    if not prompt:
        return ""
    p = prompt.strip().rstrip(".").strip('"\'')
    if len(p) <= max_len:
        return p
    return p[:max_len].rsplit(" ", 1)[0]


def convert(ann_dir: Path, images_dir: Path, out_path: Path,
            min_elements: int = 4) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    by_img = _load_annotations(ann_dir)

    n_written = 0
    n_skipped_no_image = 0
    n_skipped_few_elements = 0
    with open(out_path, "w") as f:
        for img_rel, payload in sorted(by_img.items()):
            if len(payload["elements"]) < min_elements:
                n_skipped_few_elements += 1
                continue
            img_abs = images_dir / img_rel
            if not img_abs.exists():
                n_skipped_no_image += 1
                continue
            # Build elements with ids first so parent_id resolution can reference them.
            elements: list[dict] = []
            stem = Path(img_rel).stem
            for i, e in enumerate(payload["elements"]):
                etype = _TYPE_MAP.get((e["category"], e["element_type"]), "button")
                elements.append({
                    "_id": f"{stem}-{i}",
                    "bbox": e["bbox"],
                    "category": e["category"],
                    "element_type": e["element_type"],
                    "prompt": e["prompt"],
                    "type": etype,
                })
            _group_menus(elements, payload["size"][0])
            _infer_parents(elements)

            out_elements = []
            for e in elements:
                etype = e["type"]
                pid = e.get("parent_id") or ""
                # Menu-cluster members get retyped to list_item explicitly.
                if pid.startswith("menu-group-"):
                    etype = "list_item"
                out_elements.append({
                    "id": e["_id"],
                    "bbox": e["bbox"],
                    "type": etype,
                    "text": _short_text(e["prompt"]),
                    "parent_id": e.get("parent_id"),
                })
            # If we synthesized any menu-group parents, materialize them as
            # `panel` elements so containment/list_ordinal miners can use them.
            menu_groups: dict[str, list[list[float]]] = defaultdict(list)
            for e in out_elements:
                pid = e.get("parent_id") or ""
                if pid.startswith("menu-group-"):
                    menu_groups[pid].append(e["bbox"])
            for gid, bbs in menu_groups.items():
                xs1 = min(b[0] for b in bbs)
                ys1 = min(b[1] for b in bbs)
                xs2 = max(b[2] for b in bbs)
                ys2 = max(b[3] for b in bbs)
                pad = 4.0
                out_elements.append({
                    "id": gid,
                    "bbox": [xs1 - pad, ys1 - pad, xs2 + pad, ys2 + pad],
                    "type": "panel",
                    "text": "menu",
                    "parent_id": None,
                })

            record = {
                "image_path": str(img_abs),
                "image_size": payload["size"],
                "source": "ui_vision",
                "platform": payload["platform"],
                "elements": out_elements,
            }
            f.write(json.dumps(record) + "\n")
            n_written += 1

    print(f"wrote {n_written} screenshots -> {out_path}")
    print(f"  skipped (no image file):   {n_skipped_no_image}")
    print(f"  skipped (<{min_elements} elements): {n_skipped_few_elements}")
    return n_written


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--annotations", required=True,
                    help="UI-Vision annotations dir (with element_grounding/ and layout_grounding/)")
    ap.add_argument("--images", required=True,
                    help="UI-Vision images dir (parent of element_grounding/ and layout_grounding/)")
    ap.add_argument("--out", required=True, help="Output corpus.jsonl path")
    ap.add_argument("--min-elements", type=int, default=4,
                    help="Skip screenshots with fewer annotated elements")
    args = ap.parse_args()
    n = convert(Path(args.annotations), Path(args.images),
                Path(args.out), args.min_elements)
    return 0 if n > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
