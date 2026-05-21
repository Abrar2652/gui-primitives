#!/usr/bin/env python
"""Render all EMNLP camera-ready figures from a finished analysis run.

Reads `analysis.json` and `extras_analysis.json`; emits PDF + PNG per figure.
Missing inputs are skipped with a logged note so the driver is safe to
re-run after partial completion.
"""
import _bootstrap  # noqa: F401
import argparse
import json
import logging
from pathlib import Path

from guiprim.logging_utils import get_logger
from guiprim.viz.plots import (
    fig_teaser_minimal_pair,
    fig_per_primitive,
    fig_intervention_deltas,
    fig_controls,
    fig_regression_forest,
    fig_supp_heatmap,
    fig_supp_attention,
    fig_headline_scatter,
    fig_human_gap,
    fig_pair_consistency,
    fig_som_per_primitive,
)

log = get_logger()
logging.getLogger("guiprim.viz").setLevel(logging.INFO)


def _load(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--items", default="data/benchmark/items.jsonl",
                    help="path to items.jsonl (for the teaser figure)")
    ap.add_argument("--heads", default=None,
                    help="optional path to a top-localization-head JSON for the attention supp figure")
    args = ap.parse_args()

    run = Path(args.run)
    figs = run / "figs"
    figs.mkdir(parents=True, exist_ok=True)

    analysis = _load(run / "analysis.json")
    extras = _load(run / "extras_analysis.json")
    if not analysis:
        log.error("no analysis.json under %s -- run scripts/06_analyze.py first", run)
        return 1

    # ----- Fig 1: minimal-pair teaser -------------------------------------
    items_path = Path(args.items)
    if items_path.exists():
        out = fig_teaser_minimal_pair(items_path, figs)
        if out:
            log.info("fig1 (teaser) -> %s", out)
    else:
        log.warning("fig1 (teaser) skipped: %s missing", items_path)

    # ----- Fig 2: per-primitive accuracy ----------------------------------
    table, chance = {}, {}
    for mk, m in analysis.get("models", {}).items():
        per = m.get("per_primitive", {})
        if not per:
            continue
        table[mk] = {p: {"accuracy": v["accuracy"],
                         "ci_lo": v.get("ci_lo", v["accuracy"]),
                         "ci_hi": v.get("ci_hi", v["accuracy"])}
                     for p, v in per.items()}
        for p, v in per.items():
            chance[p] = v.get("chance", 0.5)
    if table:
        out = fig_per_primitive(table, chance, figs)
        log.info("fig2 (per-primitive) -> %s", out)
    else:
        log.warning("fig2 (per-primitive) skipped: no per-primitive data")

    # ----- Fig 3: intervention deltas -------------------------------------
    iv_with_ci = extras.get("intervention_deltas", {})
    comp_holm = analysis.get("comparisons", {})
    if iv_with_ci:
        out = fig_intervention_deltas(iv_with_ci, comp_holm, figs)
        log.info("fig3 (interventions) -> %s", out)
    else:
        log.warning("fig3 (interventions) skipped: no intervention deltas")

    # ----- Fig 4: shortcut controls ---------------------------------------
    ctrl = analysis.get("controls", {})
    if ctrl:
        out = fig_controls(ctrl, figs)
        log.info("fig4 (controls) -> %s", out)
    else:
        log.warning("fig4 (controls) skipped: no controls data")

    # ----- Fig 5: regression forest plot ----------------------------------
    reg = analysis.get("regression", {})
    if reg and "primitives" in reg:
        out = fig_regression_forest(reg, figs)
        log.info("fig5 (forest) -> %s", out)
    else:
        log.warning("fig5 (forest) skipped: no regression block")

    # ----- Supp S1: heatmap ----------------------------------------------
    if table:
        out = fig_supp_heatmap(table, figs)
        log.info("supp-S1 (heatmap) -> %s", out)

    # ----- Supp S2: top localization head attention ----------------------
    heads_json = Path(args.heads) if args.heads else (run / "qwen2_5_vl_7b" / "top_head_attention.json")
    out = fig_supp_attention(heads_json, items_path, figs)
    if out:
        log.info("supp-S2 (attention) -> %s", out)

    # ----- Fig 6: headline GUI-Primitives vs SS-Pro scatter ---------------
    strat = extras.get("stratified_corr", {})
    if strat.get("per_model"):
        out = fig_headline_scatter(strat, figs)
        if out:
            log.info("fig6 (headline scatter) -> %s", out)
    else:
        log.warning("fig6 (headline scatter) skipped: no stratified_corr.per_model")

    # ----- Fig 7: human-vs-model gap on the 185-clean core ----------------
    clean = analysis.get("human_verified_clean_comparison", {})
    human_acc = None
    try:
        agreement = json.loads(Path("human_eval/agreement.json").read_text())
        human_acc = agreement.get("human_accuracy")
    except Exception:
        log.warning("fig7 (human gap): human_eval/agreement.json not loadable")
    if clean and human_acc is not None:
        out = fig_human_gap(clean, human_acc, figs)
        if out:
            log.info("fig7 (human gap) -> %s", out)
    else:
        log.warning("fig7 (human gap) skipped: missing clean accuracies or human_accuracy")

    # ----- Fig 8: pair-consistency vs accuracy (What's-Up signature) ------
    # Add pair_consistency + n_complete_pairs to the table dict we built earlier
    pc_table = {}
    for mk, m in analysis.get("models", {}).items():
        per = m.get("per_primitive", {})
        if not per:
            continue
        pc_table[mk] = {p: {
            "accuracy": v["accuracy"],
            "pair_consistency": v.get("pair_consistency"),
            "n_complete_pairs": v.get("n_complete_pairs", 0),
        } for p, v in per.items()}
    if pc_table:
        out = fig_pair_consistency(pc_table, figs)
        log.info("fig8 (pair-consistency) -> %s", out)
    else:
        log.warning("fig8 (pair-consistency) skipped: no per-primitive data")

    # ----- Fig 9: per-primitive Set-of-Mark lift --------------------------
    per_prim = extras.get("per_primitive", {})
    if per_prim:
        out = fig_som_per_primitive(per_prim, figs)
        if out:
            log.info("fig9 (SoM per-primitive) -> %s", out)
    else:
        log.warning("fig9 (SoM per-primitive) skipped: no extras.per_primitive")

    log.info("figures complete -> %s", figs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
