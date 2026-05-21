#!/usr/bin/env python
"""Run the per-primitive diagnostic for one model.

Evaluates the model on the diagnostic split and, unless disabled, on the
shortcut controls (text-only, shuffled, blurred). Writes prediction JSONL into
runs/<exp>/<model>/.

  --model   path to a model config YAML
  --split   which benchmark split to run (default: human_verified)
  --smoke   tiny subset; pairs well with configs/models/dummy.yaml
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
from guiprim.controls.sanity_probes import make_text_only, make_shuffled, make_blurred

log = get_logger()


def _load_split(bench_dir: Path, split: str) -> list[dict]:
    items = [json.loads(l) for l in (bench_dir / "items.jsonl").read_text().splitlines()
             if l.strip()]
    splits = json.loads((bench_dir / "splits.json").read_text())
    keep = set(splits.get(split, []))
    return [it for it in items if it["item_id"] in keep] if keep else items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--split", default="human_verified")
    ap.add_argument("--bench", default="data/benchmark")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    cfg = load_config(args.config)
    mcfg = load_config(args.model)
    set_global_seed(get(cfg, "seed", 13))

    items = _load_split(Path(args.bench), args.split)
    if args.smoke:
        items = items[:24]
    if not items:
        log.error("no items found — run 01_build_benchmark.py first")
        return 1
    log.info("diagnostic: %d items on model '%s'", len(items), mcfg["key"])

    run_dir = init_run(Path(get(cfg, "paths.runs_dir", "runs")) / cfg["name"] / mcfg["key"],
                       {"experiment": cfg, "model": mcfg, "split": args.split})
    model = build_model(mcfg)

    run_model_on_items(model, items, run_dir / "diagnostic.jsonl")

    ctrl_dir = run_dir / "controls"
    if get(cfg, "controls.run_text_only", False) and not args.smoke:
        run_model_on_items(model, make_text_only(items, ctrl_dir / "imgs"),
                           run_dir / "control_text_only.jsonl")
    if get(cfg, "controls.run_shuffled", False) and not args.smoke:
        run_model_on_items(model, make_shuffled(items, get(cfg, "seed", 13)),
                           run_dir / "control_shuffled.jsonl")
    if get(cfg, "controls.run_blur", False) and not args.smoke:
        run_model_on_items(model, make_blurred(items, ctrl_dir / "imgs"),
                           run_dir / "control_blur.jsonl")

    model.cleanup()
    log.info("diagnostic complete -> %s", run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
