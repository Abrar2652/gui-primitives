#!/usr/bin/env python
"""Build the GUI-Primitives benchmark.

Reads a UI-element corpus, synthesizes minimal-pair items, validates them, and
splits into a human-verified core and an auto pool.

  --synthetic   render a synthetic UI corpus first (no downloads; for smoke/CI)
  --n           override benchmark.n_items
Outputs under data/benchmark/: items.jsonl, splits.json, validation.json.
"""
import _bootstrap  # noqa: F401
import argparse
import json
import random
from pathlib import Path

from guiprim.config import load_config, get
from guiprim.logging_utils import get_logger
from guiprim.seeds import set_global_seed
from guiprim.benchmark.synthesize import synthesize, write_items
from guiprim.benchmark.synthetic_ui import build_synthetic_corpus
from guiprim.benchmark.validate import validate_items

log = get_logger()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--synthetic", action="store_true",
                    help="Render a synthetic-only corpus (no real screenshots).")
    ap.add_argument("--mix-synthetic", action="store_true",
                    help="Also render synthetic UIs and concatenate with the real "
                         "corpus, so primitives the real corpus cannot supply "
                         "(containment / list_ordinal / occlusion in UI-Vision) "
                         "fall back to controlled stimuli. Items keep their "
                         "`source` tag so analyses can split real vs synthetic.")
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--out", default="data/benchmark")
    args = ap.parse_args()

    cfg = load_config(args.config)
    set_global_seed(get(cfg, "seed", 13))
    n_items = args.n or get(cfg, "benchmark.n_items", 1000)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    primitives = get(cfg, "benchmark.primitives")
    min_elems = get(cfg, "benchmark.min_elements_per_image", 4)
    seed = get(cfg, "seed", 13)

    if args.synthetic:
        log.info("rendering synthetic UI corpus")
        n_images = max(40, n_items // 4)
        corpus = build_synthetic_corpus(out / "synthetic", n_images, seed)
        log.info("synthesizing %d items (synthetic-only)", n_items)
        items = synthesize(corpus_path=corpus, primitives=primitives,
                           n_items=n_items, seed=seed, min_elements=min_elems)
    elif args.mix_synthetic:
        real_corpus = Path(get(cfg, "paths.ui_corpus"))
        if not real_corpus.exists():
            log.error("UI corpus not found at %s — see data/README.md", real_corpus)
            return 1
        log.info("rendering synthetic UI corpus to fill primitives the real "
                 "corpus cannot supply")
        n_images = max(40, n_items // 4)
        synth_corpus = build_synthetic_corpus(out / "synthetic", n_images, seed)
        # Concatenate both corpora into one file so synthesize() round-robins
        # screenshots across both sources.
        mix_path = out / "mixed_corpus.jsonl"
        with open(mix_path, "w") as f:
            for src in (real_corpus, synth_corpus):
                with open(src) as g:
                    for line in g:
                        if line.strip():
                            f.write(line)
        log.info("synthesizing %d items (real %s + synthetic %s)",
                 n_items, real_corpus, synth_corpus)
        items = synthesize(corpus_path=mix_path, primitives=primitives,
                           n_items=n_items, seed=seed, min_elements=min_elems)
    else:
        corpus = Path(get(cfg, "paths.ui_corpus"))
        if not corpus.exists():
            log.error("UI corpus not found at %s — see data/README.md", corpus)
            return 1
        log.info("synthesizing %d items from %s", n_items, corpus)
        items = synthesize(corpus_path=corpus, primitives=primitives,
                           n_items=n_items, seed=seed, min_elements=min_elems)

    report = validate_items(items)
    (out / "validation.json").write_text(json.dumps(report, indent=2))
    log.info("validation: %d items, per-primitive=%s",
             report["n_items"], report["per_primitive"])
    for issue in report["issues"]:
        log.warning("validation note: %s", issue)

    # Split: a human-verified core (stratified by primitive) + the rest as pool.
    core_n = min(get(cfg, "benchmark.human_verified_n", 200), len(items))
    rng = random.Random(get(cfg, "seed", 13))
    by_prim: dict[str, list] = {}
    for it in items:
        by_prim.setdefault(it["primitive"], []).append(it)
    core_ids, per = [], max(1, core_n // max(1, len(by_prim)))
    for prim, group in by_prim.items():
        rng.shuffle(group)
        for it in group[:per]:
            it["split"] = "human_verified"
            core_ids.append(it["item_id"])
    splits = {"human_verified": core_ids,
              "pool": [it["item_id"] for it in items if it["split"] != "human_verified"]}

    write_items(items, out / "items.jsonl")
    (out / "splits.json").write_text(json.dumps(splits, indent=2))
    log.info("wrote %s (core=%d, pool=%d)", out / "items.jsonl",
             len(splits["human_verified"]), len(splits["pool"]))
    log.info("NEXT: human-verify the core with human_eval/annotate.py before "
             "trusting headline numbers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
