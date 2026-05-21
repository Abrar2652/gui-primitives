#!/usr/bin/env python
"""Run GUI grounding on ScreenSpot-Pro for one model.

ScreenSpot-Pro (Li et al., arXiv 2504.07981) ships expert-annotated
instruction/screenshot/bbox triples for 23 professional applications. This
script normalizes its annotations into the repo's record schema, evaluates the
model, and writes runs/<exp>/<model>/screenspot.jsonl. Each record is tagged
with the spatial primitives its instruction requires, which feeds the
primitive -> grounding regression in 06_analyze.py.

Expected layout (see data/README.md):
  <screenspot_pro>/annotations/*.json   per-app annotation files, OR
  <screenspot_pro>/screenspot_pro.jsonl a single normalized JSONL
  <screenspot_pro>/images/...           screenshots referenced by the annotations
"""
import _bootstrap  # noqa: F401
import argparse
import json
from pathlib import Path

from guiprim.config import load_config, get
from guiprim.logging_utils import get_logger, init_run
from guiprim.seeds import set_global_seed
from guiprim.models import build_model
from guiprim.inference.runner import run_model_on_items
from guiprim.benchmark.primitives import tag_instruction

log = get_logger()


def load_screenspot_pro(root: Path) -> list[dict]:
    """Normalize ScreenSpot-Pro annotations into repo records."""
    records: list[dict] = []
    jsonl = root / "screenspot_pro.jsonl"
    if jsonl.exists():
        raw = [json.loads(l) for l in jsonl.read_text().splitlines() if l.strip()]
    else:
        ann_dir = root / "annotations"
        if not ann_dir.exists():
            raise FileNotFoundError(
                f"no annotations under {root} — see data/README.md")
        raw = []
        for jf in sorted(ann_dir.glob("*.json")):
            data = json.loads(jf.read_text())
            raw.extend(data if isinstance(data, list) else [data])

    img_root = root / "images"
    for i, r in enumerate(raw):
        bbox = r.get("bbox") or r.get("gt_bbox")
        if bbox and len(bbox) == 4 and bbox[2] < bbox[0]:  # [x,y,w,h] -> [x1,y1,x2,y2]
            bbox = [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]]
        img = r.get("img_filename") or r.get("image")
        instr = r.get("instruction") or r.get("prompt") or ""
        records.append({
            "item_id": r.get("id", f"ssp-{i}"),
            "instruction": instr,
            "image_path": str(img_root / img) if img else r.get("image_path"),
            "target_bbox": bbox,
            "distractor_bbox": None,
            "application": r.get("application"),
            "required_primitives": tag_instruction(instr),
        })
    return records


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--limit", type=int, default=None,
                    help="cap items (use for the closed-model budget)")
    args = ap.parse_args()

    cfg = load_config(args.config)
    mcfg = load_config(args.model)
    set_global_seed(get(cfg, "seed", 13))

    root = Path(get(cfg, "paths.screenspot_pro", "data/screenspot_pro"))
    try:
        items = load_screenspot_pro(root)
    except FileNotFoundError as e:
        log.error("%s", e)
        return 1
    if args.limit:
        items = items[:args.limit]
    log.info("ScreenSpot-Pro: %d items on model '%s'", len(items), mcfg["key"])

    run_dir = init_run(Path(get(cfg, "paths.runs_dir", "runs")) / cfg["name"] / mcfg["key"],
                       {"experiment": cfg, "model": mcfg, "stage": "screenspot"})
    model = build_model(mcfg)
    run_model_on_items(model, items, run_dir / "screenspot.jsonl")
    model.cleanup()
    log.info("ScreenSpot-Pro complete -> %s", run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
