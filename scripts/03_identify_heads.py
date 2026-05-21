#!/usr/bin/env python
"""Identify localization heads for one open model (Kang et al., 2503.06287).

Runs attention capture over the probe split and saves a ranked head list to
runs/<exp>/<model>/localization_heads.json for the steering experiments.
"""
import _bootstrap  # noqa: F401
import argparse
import json
from pathlib import Path

from guiprim.config import load_config, get
from guiprim.logging_utils import get_logger, init_run
from guiprim.seeds import set_global_seed
from guiprim.models import build_model
from guiprim.interventions.localization_heads import score_heads, save_heads

log = get_logger()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--bench", default="data/benchmark")
    ap.add_argument("--max-probe", type=int, default=120)
    args = ap.parse_args()

    cfg = load_config(args.config)
    mcfg = load_config(args.model)
    set_global_seed(get(cfg, "seed", 13))

    if not mcfg.get("supports_attention_capture"):
        log.error("%s has supports_attention_capture=false", mcfg["key"])
        return 1

    items = [json.loads(l) for l in
             (Path(args.bench) / "items.jsonl").read_text().splitlines() if l.strip()]
    splits = json.loads((Path(args.bench) / "splits.json").read_text())
    probe_split = get(cfg, "heads.probe_split", "human_verified")
    keep = set(splits.get(probe_split, []))
    probe = [it for it in items if it["item_id"] in keep][:args.max_probe]
    log.info("identifying heads on %d probe items", len(probe))

    run_dir = init_run(Path(get(cfg, "paths.runs_dir", "runs")) / cfg["name"] / mcfg["key"],
                       {"experiment": cfg, "model": mcfg, "stage": "heads"})
    model = build_model(mcfg)
    result = score_heads(model, probe)
    top_k = get(cfg, "heads.top_k", 16)
    out = save_heads(result, run_dir / "localization_heads.json", top_k=top_k)
    model.cleanup()
    log.info("top-%d localization heads -> %s", top_k, out)
    for h in result["ranking"][:5]:
        log.info("  L%02d H%02d  score=%.4f  img_mass=%.3f  focus=%.3f",
                 h["layer"], h["head"], h["score"], h["image_mass"], h["spatial_focus"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
