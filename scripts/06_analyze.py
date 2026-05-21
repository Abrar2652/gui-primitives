#!/usr/bin/env python
"""Aggregate an experiment into a single analysis.json.

Consumes every model directory under runs/<experiment>/ and produces:
  * per-primitive accuracy with bootstrap CIs and pair-consistency
  * paired McNemar tests (intervention vs baseline) with Holm correction
  * shortcut-control pass/fail against expected_control_behavior()
  * the primitive-competence -> ScreenSpot-Pro regression (if data present)

  --run     path to runs/<experiment>  (or a single model dir)
  --smoke   tolerate missing files; never fail the pipeline wiring test
"""
import _bootstrap  # noqa: F401
import argparse
import json
from pathlib import Path

from guiprim.config import get
from guiprim.logging_utils import get_logger
from guiprim.benchmark.primitives import CHANCE, PrimitiveType
from guiprim.eval.metrics import score_records, per_primitive_table, pair_consistency, pair_consistency_with_n
from guiprim.eval.stats import bootstrap_ci, mcnemar, holm_bonferroni
from guiprim.controls.sanity_probes import expected_control_behavior, evaluate_control

log = get_logger()


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def _model_dirs(run: Path) -> list[Path]:
    if (run / "diagnostic.jsonl").exists() or any(run.glob("iv_*.jsonl")):
        return [run]
    return [d for d in sorted(run.iterdir()) if d.is_dir()]


def _per_primitive_with_ci(scored: list[dict], resamples: int) -> dict:
    table = per_primitive_table(scored)
    cons = pair_consistency_with_n(scored)
    by_prim: dict[str, list] = {}
    for r in scored:
        by_prim.setdefault(r.get("primitive", "unknown"), []).append(r)
    for prim, rs in by_prim.items():
        _, lo, hi = bootstrap_ci([int(r["correct"]) for r in rs], resamples)
        c = cons.get(prim, {"pair_consistency": 0.0, "n_complete_pairs": 0})
        table[prim]["ci_lo"] = lo
        table[prim]["ci_hi"] = hi
        table[prim]["pair_consistency"] = c["pair_consistency"]
        table[prim]["n_complete_pairs"] = c["n_complete_pairs"]
        table[prim]["chance"] = CHANCE.get(PrimitiveType(prim), 0.5) \
            if prim in {p.value for p in PrimitiveType} else 0.5
    return table


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--resamples", type=int, default=2000)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    run = Path(args.run)
    if not run.exists():
        log.error("run path %s does not exist", run)
        return 0 if args.smoke else 1

    analysis: dict = {"run": str(run), "models": {}, "comparisons": {},
                      "controls": {}, "regression": None,
                      "fair_core_comparison": {},
                      "human_verified_clean_comparison": {}}
    screenspot_recs: dict[str, list] = {}
    primitive_comp: dict[str, dict] = {}

    # Load the human_verified ("core") split ids if available — used to produce
    # an apples-to-apples comparison table where every model is scored on the
    # SAME 196-item subset. Closed models only ran on the core split, so
    # comparing them against open models' full 994-item accuracy is
    # misleading; this section fixes that.
    core_ids: set[str] = set()
    clean_ids: set[str] = set()
    try:
        import json as _json
        from pathlib import Path as _Path
        splits = _json.loads(_Path("data/benchmark/splits.json").read_text())
        core_ids = set(splits.get("human_verified", []))
        clean_ids = set(splits.get("human_verified_clean", []))
    except Exception:
        log.info("no splits.json available; skipping fair-core comparison")

    for mdir in _model_dirs(run):
        mk = mdir.name
        diag = _read(mdir / "diagnostic.jsonl") or _read(mdir / "iv_baseline.jsonl")
        if not diag:
            log.info("skip %s (no diagnostic predictions)", mk)
            continue
        scored = score_records(diag)
        table = _per_primitive_with_ci(scored, args.resamples)
        overall = sum(r["correct"] for r in scored) / len(scored)
        overall_loose = sum(r.get("near", False) for r in scored) / len(scored)
        analysis["models"][mk] = {"overall_accuracy": overall,
                                  "overall_loose_accuracy": overall_loose,
                                  "n": len(scored),
                                  "per_primitive": table}
        primitive_comp[mk] = {p: table[p]["accuracy"] for p in table}
        log.info("%s: overall acc=%.3f n=%d", mk, overall, len(scored))

        # Fair same-split comparison: every model scored on the core subset
        # (or its intersection with whatever items the model actually ran).
        if core_ids:
            core_scored = [r for r in scored if r.get("item_id") in core_ids]
            if core_scored:
                core_overall = sum(r["correct"] for r in core_scored) / len(core_scored)
                analysis["fair_core_comparison"][mk] = {
                    "n": len(core_scored),
                    "overall_accuracy": core_overall,
                }

        # Clean-core comparison: same as fair_core_comparison but on the
        # human_verified_clean subset (majority-invalid items dropped per
        # human_eval/agreement.json).
        if clean_ids:
            clean_scored = [r for r in scored if r.get("item_id") in clean_ids]
            if clean_scored:
                clean_overall = sum(r["correct"] for r in clean_scored) / len(clean_scored)
                analysis["human_verified_clean_comparison"][mk] = {
                    "n": len(clean_scored),
                    "overall_accuracy": clean_overall,
                }

        # Intervention vs baseline (paired McNemar + Holm across interventions).
        base = _read(mdir / "iv_baseline.jsonl")
        if base:
            base_by = {r["item_id"]: r for r in score_records(base)}
            pvals, deltas = {}, {}
            for iv_file in sorted(mdir.glob("iv_*.jsonl")):
                name = iv_file.stem.replace("iv_", "")
                if name == "baseline":
                    continue
                iv_by = {r["item_id"]: r for r in score_records(_read(iv_file))}
                common = [i for i in base_by if i in iv_by]
                if not common:
                    continue
                a = [base_by[i]["correct"] for i in common]
                b = [iv_by[i]["correct"] for i in common]
                res = mcnemar(a, b)
                pvals[name] = res["p_value"]
                deltas[name] = res["acc_delta"]
            corrected = holm_bonferroni(pvals) if pvals else {}
            analysis["comparisons"][mk] = {
                name: {"acc_delta": deltas[name], **corrected.get(name, {})}
                for name in pvals}

        # Shortcut controls — accuracy + paired McNemar against main + pass/fail.
        ctrl_acc = {"main": overall}
        ctrl_checks: dict[str, dict] = {}
        main_by = {r["item_id"]: r for r in scored}
        for cname in ("text_only", "shuffled", "blur"):
            crecs = _read(mdir / f"control_{cname}.jsonl")
            if not crecs:
                continue
            cs = score_records(crecs)
            ctrl_acc[cname] = sum(r["correct"] for r in cs) / len(cs)
            # Pair by stripping the control suffix from item_id (see sanity_probes).
            pairs = []
            for r in cs:
                base_id = r["item_id"].split("::")[0]
                if base_id in main_by:
                    pairs.append((main_by[base_id]["correct"], r["correct"]))
            mcn_p = mcnemar([a for a, _ in pairs], [b for _, b in pairs])["p_value"] \
                if pairs else None
            ctrl_checks[cname] = evaluate_control(cname, overall, ctrl_acc[cname], mcn_p)
            ctrl_checks[cname]["mcnemar_p"] = mcn_p
        if len(ctrl_acc) > 1:
            analysis["controls"][mk] = {"accuracy": ctrl_acc,
                                        "checks": ctrl_checks,
                                        "expected": expected_control_behavior()}

        ss = _read(mdir / "screenspot.jsonl")
        if ss:
            screenspot_recs[mk] = score_records(ss)

    # Primitive-competence -> ScreenSpot-Pro regression.
    if len(screenspot_recs) >= 2 and primitive_comp:
        try:
            from guiprim.eval.regression import (build_regression_frame,
                                                 fit_competence_regression)
            df = build_regression_frame(screenspot_recs, primitive_comp)
            analysis["regression"] = fit_competence_regression(df)
            log.info("regression: pseudo-R2=%.3f n=%d",
                     analysis["regression"]["pseudo_r2"],
                     analysis["regression"]["n_obs"])
        except Exception as e:
            log.warning("regression skipped: %s", e)
            analysis["regression"] = {"error": str(e)}
    else:
        log.info("regression needs >=2 models with ScreenSpot-Pro runs; skipping")

    out = run / "analysis.json"
    out.write_text(json.dumps(analysis, indent=2))
    log.info("analysis written -> %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
