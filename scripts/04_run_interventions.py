#!/usr/bin/env python
"""Run the training-free interventions on the diagnostic split.

Conditions (each enabled via configs/experiments/interventions.yaml):
  baseline     plain grounding prompt
  cot          primitive-aware chain-of-thought
  set_of_mark  numbered marks on candidates (id-output)
  steering     activation steering from the correct-vs-incorrect contrast

Writes one prediction JSONL per condition into runs/<exp>/<model>/.
Steering reuses the baseline predictions to derive its contrast vectors, so run
order is: baseline -> (cot, som) -> steering.
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
from guiprim.eval.metrics import score_records
from guiprim.interventions.cot import cot_instruction
from guiprim.interventions.set_of_mark import apply_set_of_mark, resolve_mark
from guiprim.interventions.steering import derive_activation_vectors, activation_steering

log = get_logger()


def _read(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--bench", default="data/benchmark")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--split", default=None,
                    help="optional split name in splits.json to restrict to (e.g. human_verified)")
    args = ap.parse_args()

    cfg = load_config(args.config)
    mcfg = load_config(args.model)
    set_global_seed(get(cfg, "seed", 13))

    items = _read(Path(args.bench) / "items.jsonl")
    if args.split:
        splits = json.loads((Path(args.bench) / "splits.json").read_text())
        keep = set(splits.get(args.split, []))
        items = [it for it in items if it["item_id"] in keep]
        log.info("restricted to split %s: %d items", args.split, len(items))
    if args.smoke:
        items = items[:24]
    iv = get(cfg, "interventions", {})
    run_dir = init_run(Path(get(cfg, "paths.runs_dir", "runs")) / cfg["name"] / mcfg["key"],
                       {"experiment": cfg, "model": mcfg, "stage": "interventions"})
    model = build_model(mcfg)

    # 1) baseline
    base_path = run_dir / "iv_baseline.jsonl"
    if get(iv, "baseline.enabled", True):
        run_model_on_items(model, items, base_path)

    # 2) primitive-aware CoT
    if get(iv, "cot.enabled", False):
        run_model_on_items(model, items, run_dir / "iv_cot.jsonl",
                           instruction_fn=cot_instruction)

    # 3) Set-of-Mark (id mode). Resolve mark ids back to coordinates post-hoc.
    if get(iv, "set_of_mark.enabled", False):
        som_items = apply_set_of_mark(items, run_dir / "som_imgs", mode="id")
        som_path = run_dir / "iv_som.jsonl"
        run_model_on_items(model, som_items, som_path)
        recs = _read(som_path)
        mark_maps = {it["item_id"]: it["_mark_map"] for it in som_items}
        for r in recs:
            mm = mark_maps.get(r["item_id"])
            if mm:
                xy = resolve_mark(r.get("raw_text", ""), mm)
                r["pred_xy"] = list(xy) if xy else None
        som_path.write_text("\n".join(json.dumps(r) for r in recs) + "\n")

    # 4) activation steering
    if get(iv, "steering.enabled", False) and mcfg["family"] != "dummy":
        try:
            scored = score_records(_read(base_path))
            layers = get(iv, "steering.layers", list(range(8, 16)))
            n_contrast = get(iv, "steering.n_contrast", 200)
            vecs = derive_activation_vectors(model, scored[:n_contrast], layers)
            alpha = get(iv, "steering.alpha", 4.0)
            steer_path = run_dir / "iv_steering.jsonl"
            with activation_steering(model, vecs, alpha=alpha):
                run_model_on_items(model, items, steer_path)
            (run_dir / "steering_meta.json").write_text(json.dumps(
                {"layers": layers, "alpha": alpha, "n_vectors": len(vecs)}, indent=2))
        except Exception as e:
            log.warning("steering skipped: %s", e)
    elif get(iv, "steering.enabled", False):
        log.info("steering skipped for dummy model (smoke mode)")

    model.cleanup()
    log.info("interventions complete -> %s", run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
