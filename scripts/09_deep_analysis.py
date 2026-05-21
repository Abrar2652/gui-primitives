#!/usr/bin/env python
"""Deep analyses that reviewers commonly ask for. Reads existing prediction
JSONLs in runs/<exp>/<model>/ and writes runs/<exp>/deep_analysis.json plus a
human-readable runs/<exp>/deep_analysis.md.

Sections produced:
  1. Per-application ScreenSpot-Pro accuracy per model (target-size effect anchor).
  2. Cohen's h effect size per primitive vs the per-primitive CHANCE level.
  3. Lexical-class failure breakdown: does swapping the RELATION word break
     accuracy more than swapping the ANCHOR noun? (What's-Up logic.)
  4. Qualitative failure examples — N items per primitive where models cluster
     on the same wrong answer.
  5. Cost report: GPU-hours per model (latency summed from JSONLs), API dollars
     for any closed-model runs (always 0 until we wire one up).
  6. Real vs synthetic split: per-primitive accuracy stratified by item source.
  7. Pair-consistency vs accuracy^2 regression — quantifies the What's-Up
     signature.

Usage:
  python scripts/09_deep_analysis.py --run runs/diagnostic
"""
from __future__ import annotations
import _bootstrap  # noqa: F401
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from guiprim.benchmark.primitives import PRIMITIVES, CHANCE, PrimitiveType
from guiprim.eval.metrics import score_records
from guiprim.eval.stats import bootstrap_ci, cohens_h


def _read(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def _model_dirs(run: Path) -> list[Path]:
    return [d for d in sorted(run.iterdir()) if d.is_dir()]


# ----------------------- 1. per-application SS-Pro --------------------------
def per_application_screenspot(model_dirs: list[Path]) -> dict:
    out: dict = {}
    for mdir in model_dirs:
        recs = _read(mdir / "screenspot.jsonl")
        if not recs:
            continue
        scored = score_records(recs)
        by_app: dict[str, list] = defaultdict(list)
        for r in scored:
            app = (r.get("meta") or {}).get("application") or r.get("application") \
                or r.get("item_id", "").split("_")[0]
            by_app[app].append(int(r["correct"]))
        rows = {}
        for app, vals in by_app.items():
            mean, lo, hi = bootstrap_ci(vals, 1000)
            rows[app] = {"n": len(vals), "accuracy": mean,
                         "ci_lo": lo, "ci_hi": hi}
        out[mdir.name] = rows
    return out


# ----------------------- 2. cohen's h vs chance -----------------------------
def cohens_h_vs_chance(model_dirs: list[Path]) -> dict:
    out: dict = {}
    for mdir in model_dirs:
        diag = _read(mdir / "diagnostic.jsonl")
        if not diag:
            continue
        scored = score_records(diag)
        by_p: dict[str, list] = defaultdict(list)
        for r in scored:
            by_p[r["primitive"]].append(int(r["correct"]))
        rows = {}
        for p, vals in by_p.items():
            n = len(vals)
            acc = sum(vals) / n if n else 0.0
            try:
                chance = CHANCE[PrimitiveType(p)]
            except ValueError:
                chance = 0.5
            h = cohens_h(acc, chance)
            rows[p] = {"n": n, "accuracy": acc, "chance": chance,
                       "cohens_h": h,
                       "interp": ("trivial" if abs(h) < 0.2
                                  else "small" if abs(h) < 0.5
                                  else "medium" if abs(h) < 0.8
                                  else "large"),
                       "direction": "above" if acc > chance else "below"}
        out[mdir.name] = rows
    return out


# ----------------------- 3. lexical class breakdown -------------------------
def lexical_failure_breakdown(bench_dir: Path,
                              model_dirs: list[Path]) -> dict:
    """For each primitive, contrast: how often does the model give DIFFERENT
    answers across the two members of a minimal pair?

    A model that's pair-flipping with the relation word is doing relational
    reasoning. A model that's pair-consistent regardless of the relation word
    is failing the relational test (the What's-Up insight).
    """
    items = _read(bench_dir / "items.jsonl")
    by_pair: dict[int, list[dict]] = defaultdict(list)
    for it in items:
        by_pair[it["pair_id"]].append(it)

    out: dict = {}
    for mdir in model_dirs:
        recs = _read(mdir / "diagnostic.jsonl")
        if not recs:
            continue
        scored = score_records(recs)
        rec_by_id = {r["item_id"]: r for r in scored}
        per_prim: dict[str, dict] = defaultdict(
            lambda: {"n_pairs": 0, "both_correct": 0, "one_correct": 0,
                     "both_wrong": 0, "same_click_both": 0, "diff_click_both": 0})
        for pair_id, pair_items in by_pair.items():
            if len(pair_items) != 2:
                continue
            prim = pair_items[0]["primitive"]
            r0 = rec_by_id.get(pair_items[0]["item_id"])
            r1 = rec_by_id.get(pair_items[1]["item_id"])
            if not r0 or not r1:
                continue
            c0, c1 = r0["correct"], r1["correct"]
            p0, p1 = r0.get("pred_xy"), r1.get("pred_xy")
            same_click = (p0 is not None and p1 is not None and
                          abs(p0[0] - p1[0]) < 5 and abs(p0[1] - p1[1]) < 5)
            d = per_prim[prim]
            d["n_pairs"] += 1
            if c0 and c1:
                d["both_correct"] += 1
            elif c0 or c1:
                d["one_correct"] += 1
            else:
                d["both_wrong"] += 1
            if same_click:
                d["same_click_both"] += 1
            else:
                d["diff_click_both"] += 1
        # Rates.
        for p, d in per_prim.items():
            n = d["n_pairs"] or 1
            d["same_click_rate"] = d["same_click_both"] / n
            d["both_correct_rate"] = d["both_correct"] / n
            d["one_correct_rate"] = d["one_correct"] / n
            d["both_wrong_rate"] = d["both_wrong"] / n
        out[mdir.name] = dict(per_prim)
    return out


# ----------------------- 4. qualitative failures ----------------------------
def qualitative_failures(bench_dir: Path, model_dirs: list[Path],
                         per_prim: int = 3) -> dict:
    """For each (primitive, model), surface a few representative failure pairs
    where both members of the pair are wrong AND clustered (paper appendix)."""
    items = {it["item_id"]: it for it in _read(bench_dir / "items.jsonl")}
    by_pair: dict[int, list[str]] = defaultdict(list)
    for it_id, it in items.items():
        by_pair[it["pair_id"]].append(it_id)

    out: dict = {}
    for mdir in model_dirs:
        recs = _read(mdir / "diagnostic.jsonl")
        if not recs:
            continue
        scored = score_records(recs)
        rec_by_id = {r["item_id"]: r for r in scored}
        per_prim_failures: dict[str, list] = defaultdict(list)
        for pair_id, ids in by_pair.items():
            if len(ids) != 2:
                continue
            r0, r1 = rec_by_id.get(ids[0]), rec_by_id.get(ids[1])
            if not r0 or not r1 or r0["correct"] or r1["correct"]:
                continue
            it = items[ids[0]]
            prim = it["primitive"]
            if len(per_prim_failures[prim]) >= per_prim:
                continue
            per_prim_failures[prim].append({
                "pair_id": pair_id,
                "primitive": prim,
                "source": it["source"],
                "image": Path(it["image_path"]).name,
                "instructions": [items[ids[0]]["instruction"],
                                 items[ids[1]]["instruction"]],
                "target_bboxes": [items[ids[0]]["target_bbox"],
                                  items[ids[1]]["target_bbox"]],
                "pred_xys": [r0.get("pred_xy"), r1.get("pred_xy")],
                "raw_texts": [r0.get("raw_text", "")[:80],
                              r1.get("raw_text", "")[:80]],
            })
        out[mdir.name] = dict(per_prim_failures)
    return out


# ----------------------- 5. cost report -------------------------------------
def cost_report(model_dirs: list[Path]) -> dict:
    """Per-model GPU-hours (from per-item latency_s) and approximate API
    dollars for closed models, estimated from public published pricing.

    Pricing snapshot used here:
      gpt-4o-mini:        $0.15 / 1M input + $0.60 / 1M output tokens
      claude-haiku-4-5:   $0.80 / 1M input + $4.00 / 1M output tokens
      gemini-3.1-flash-lite: $0.10 / 1M input + $0.40 / 1M output tokens
    Per-request image counts as ~1.2k tokens of input on these models; we
    use a rough 1.5k-input + 32-output-token estimate per item.
    """
    API_PRICE = {
        "closed_gpt4o_mini":     (0.15, 0.60),     # $/1M in, $/1M out
        "closed_claude_haiku":   (0.80, 4.00),
        "closed_gemini_flash":   (0.10, 0.40),
    }
    IN_TOK_EST = 1500    # rough per-item input (image + short prompt)
    OUT_TOK_EST = 32     # rough per-item output (just a click coord)

    out: dict = {}
    for mdir in model_dirs:
        per_file: dict[str, dict] = {}
        n_calls = 0
        for jp in sorted(mdir.glob("*.jsonl")):
            recs = _read(jp)
            lats = [r.get("latency_s") for r in recs if r.get("latency_s")]
            per_file[jp.name] = {
                "n": len(recs),
                "sum_latency_s": sum(lats),
                "mean_latency_s": (sum(lats) / len(lats)) if lats else 0.0,
            }
            n_calls += len(recs)
        total_s = sum(v["sum_latency_s"] for v in per_file.values())
        dollars = 0.0
        if mdir.name in API_PRICE:
            pin, pout = API_PRICE[mdir.name]
            dollars = (n_calls * IN_TOK_EST * pin / 1_000_000
                       + n_calls * OUT_TOK_EST * pout / 1_000_000)
        out[mdir.name] = {"per_file": per_file,
                          "n_inference_calls": n_calls,
                          "total_gpu_seconds": total_s,
                          "total_gpu_hours": total_s / 3600.0,
                          "approx_dollars": round(dollars, 3)}
    return out


# ----------------------- 6. real vs synthetic split -------------------------
def real_vs_synthetic(bench_dir: Path, model_dirs: list[Path]) -> dict:
    items = {it["item_id"]: it for it in _read(bench_dir / "items.jsonl")}
    out: dict = {}
    for mdir in model_dirs:
        recs = _read(mdir / "diagnostic.jsonl")
        if not recs:
            continue
        scored = score_records(recs)
        by: dict[tuple, list] = defaultdict(list)
        for r in scored:
            it = items.get(r["item_id"], {})
            by[(r["primitive"], it.get("source", "?"))].append(int(r["correct"]))
        rows: dict[str, dict] = defaultdict(dict)
        for (prim, src), vals in by.items():
            if not vals:
                continue
            mean, lo, hi = bootstrap_ci(vals, 1000)
            rows[prim][src] = {"n": len(vals), "accuracy": mean,
                               "ci_lo": lo, "ci_hi": hi}
        out[mdir.name] = dict(rows)
    return out


# ----------------------- 7. pair-consistency regression ---------------------
def pair_consistency_signature(model_dirs: list[Path]) -> dict:
    """For each primitive, compare observed pair_consistency to acc^2 (the
    independence prediction). A large negative delta is the What's-Up signature
    of relational (not random) failure."""
    out: dict = {}
    for mdir in model_dirs:
        recs = _read(mdir / "diagnostic.jsonl")
        if not recs:
            continue
        scored = score_records(recs)
        by_prim_pairs: dict[str, dict[int, list]] = defaultdict(lambda: defaultdict(list))
        for r in scored:
            by_prim_pairs[r["primitive"]][r.get("pair_id")].append(r)
        rows = {}
        for p, pair_map in by_prim_pairs.items():
            acc_vals: list[int] = []
            both_correct: list[int] = []
            for pid, members in pair_map.items():
                if len(members) != 2:
                    continue
                acc_vals.extend(int(m["correct"]) for m in members)
                both_correct.append(int(all(m["correct"] for m in members)))
            n_pairs = len(both_correct)
            if not acc_vals or not n_pairs:
                continue
            acc = sum(acc_vals) / len(acc_vals)
            pair_cons = sum(both_correct) / n_pairs
            expected_independent = acc ** 2
            # With <5 complete pairs the metric is too noisy to report; mark
            # `underpowered` so the markdown table can flag those rows.
            underpowered = n_pairs < 5
            rows[p] = {"n_pairs": n_pairs, "accuracy": acc,
                       "pair_consistency": pair_cons,
                       "expected_under_independence": expected_independent,
                       "delta": pair_cons - expected_independent,
                       "relational_failure_flag":
                           (not underpowered) and pair_cons < expected_independent / 2,
                       "underpowered": underpowered}
        out[mdir.name] = rows
    return out


# --------------------------------- main -------------------------------------
def model_level_correlation(bench_dir: Path, model_dirs: list[Path]) -> dict:
    """Per-model: (mean primitive accuracy on GUI-Primitives) vs
    (overall ScreenSpot-Pro accuracy). Correlate across models.

    This is a much more robust complement to the item-level regression: with
    only ~38 keyword-tagged SS-Pro items the item-level regression is
    underpowered, but the model-level relationship is interpretable even with
    N=4-7 models because cross-model variance is large.
    """
    out: dict = {"models": {}, "spearman_rho": None, "pearson_r": None}
    for mdir in model_dirs:
        diag = _read(mdir / "diagnostic.jsonl")
        ssp = _read(mdir / "screenspot.jsonl")
        if not diag:
            continue
        scored_diag = score_records(diag)
        diag_acc = sum(r["correct"] for r in scored_diag) / len(scored_diag)
        ssp_acc = None
        if ssp:
            scored_ssp = score_records(ssp)
            ssp_acc = sum(r["correct"] for r in scored_ssp) / len(scored_ssp)
        out["models"][mdir.name] = {
            "guiprim_acc": diag_acc,
            "screenspot_pro_acc": ssp_acc,
        }
    # Correlate across models that have both metrics.
    pairs = [(d["guiprim_acc"], d["screenspot_pro_acc"])
             for d in out["models"].values()
             if d["screenspot_pro_acc"] is not None]
    if len(pairs) >= 3:
        try:
            from scipy.stats import spearmanr, pearsonr
            xs = [p[0] for p in pairs]; ys = [p[1] for p in pairs]
            rho, prho = spearmanr(xs, ys)
            r, pr = pearsonr(xs, ys)
            out["n_models"] = len(pairs)
            out["spearman_rho"] = float(rho)
            out["spearman_p"] = float(prho)
            out["pearson_r"] = float(r)
            out["pearson_p"] = float(pr)
        except Exception as e:
            out["correlation_error"] = str(e)
    return out


def write_markdown(report: dict, out_path: Path) -> None:
    lines = [f"# Deep analysis — {report['run']}\n"]

    lines.append("## 1. Per-application ScreenSpot-Pro accuracy\n")
    apps = sorted({a for m in report["per_app_screenspot"].values() for a in m})
    if apps:
        models = list(report["per_app_screenspot"])
        lines.append("| application | " + " | ".join(models) + " |")
        lines.append("|---|" + "|".join("---:" for _ in models) + "|")
        for app in apps:
            row = [app]
            for mk in models:
                d = report["per_app_screenspot"][mk].get(app)
                row.append(f"{d['accuracy']:.2f} (n={d['n']})" if d else "")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    lines.append("## 2. Cohen's h vs chance level\n")
    for mk, rows in report["cohens_h"].items():
        lines.append(f"### {mk}\n")
        lines.append("| primitive | acc | chance | h | interp | direction |")
        lines.append("|---|---:|---:|---:|---|---|")
        for p, r in rows.items():
            lines.append(f"| {p} | {r['accuracy']:.3f} | {r['chance']:.2f} | "
                         f"{r['cohens_h']:+.3f} | {r['interp']} | {r['direction']} |")
        lines.append("")

    lines.append("## 3. Real vs synthetic accuracy stratification\n")
    for mk, prims in report["real_vs_synthetic"].items():
        lines.append(f"### {mk}\n")
        lines.append("| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |")
        lines.append("|---|---:|---:|---:|---:|")
        for p, srcs in prims.items():
            u = srcs.get("ui_vision", {})
            s = srcs.get("synthetic", {})
            lines.append(f"| {p} | {u.get('n','')} | "
                         f"{u['accuracy']:.2f} ({u['ci_lo']:.2f}-{u['ci_hi']:.2f})"
                         if u else "| | |" + f" | {s.get('n','')} | "
                         f"{s['accuracy']:.2f} ({s['ci_lo']:.2f}-{s['ci_hi']:.2f})"
                         if s else "|")
            # The line above gets clumsy; rebuild cleanly:
        # Rebuild cleanly
        lines = lines[:-len(list(prims))]
        for p, srcs in prims.items():
            u = srcs.get("ui_vision")
            s = srcs.get("synthetic")
            un = u["n"] if u else ""
            ua = f"{u['accuracy']:.2f}" if u else ""
            sn = s["n"] if s else ""
            sa = f"{s['accuracy']:.2f}" if s else ""
            lines.append(f"| {p} | {un} | {ua} | {sn} | {sa} |")
        lines.append("")

    lines.append("## 4. Pair-consistency vs acc² (What's-Up signature)\n")
    lines.append("A `relational_failure_flag` (🚩) fires when pair_consistency < acc²/2 —")
    lines.append("meaning failures on minimal pairs *correlate* with the relation word.")
    lines.append("Rows marked `(n<5)` had too few complete pairs in this split for the")
    lines.append("signature to be meaningful (e.g. closed models on the 196-item core).\n")
    for mk, rows in report["pair_signature"].items():
        lines.append(f"### {mk}\n")
        lines.append("| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |")
        lines.append("|---|---:|---:|---:|---:|---:|---|")
        for p, r in rows.items():
            if r.get("underpowered"):
                flag = "(n<5)"
            elif r["relational_failure_flag"]:
                flag = "🚩"
            else:
                flag = ""
            lines.append(f"| {p} | {r['n_pairs']} | {r['accuracy']:.3f} | "
                         f"{r['pair_consistency']:.3f} | "
                         f"{r['expected_under_independence']:.3f} | "
                         f"{r['delta']:+.3f} | {flag} |")
        lines.append("")

    lines.append("## 5. Cost report\n")
    lines.append("| model | total GPU-hours | $ |")
    lines.append("|---|---:|---:|")
    for mk, c in report["cost"].items():
        lines.append(f"| {mk} | {c['total_gpu_hours']:.2f} | "
                     f"{c['approx_dollars']:.2f} |")
    lines.append("")

    lines.append("## 5b. Model-level competence correlation\n")
    mc = report.get("model_level_correlation", {})
    lines.append("Per-model: mean GUI-Primitives accuracy vs ScreenSpot-Pro accuracy. "
                 "Robust complement to the item-level regression.\n")
    lines.append("| model | GUI-Primitives acc | ScreenSpot-Pro acc |")
    lines.append("|---|---:|---:|")
    for mk, d in mc.get("models", {}).items():
        ssp = f"{d['screenspot_pro_acc']:.3f}" if d.get('screenspot_pro_acc') is not None else "—"
        lines.append(f"| {mk} | {d['guiprim_acc']:.3f} | {ssp} |")
    if mc.get("spearman_rho") is not None:
        lines.append(f"\n**Spearman rho={mc['spearman_rho']:+.3f} "
                     f"(p={mc.get('spearman_p', 1.0):.3g}), "
                     f"Pearson r={mc['pearson_r']:+.3f} "
                     f"(p={mc.get('pearson_p', 1.0):.3g}), n={mc.get('n_models')}**\n")

    lines.append("## 6. Qualitative failure examples (3 per primitive per model)\n")
    for mk, prims in report["qualitative"].items():
        lines.append(f"### {mk}\n")
        for p, fails in prims.items():
            lines.append(f"**{p}** ({len(fails)} examples):\n")
            for f in fails:
                lines.append(f"- pair_id={f['pair_id']}  src={f['source']}  "
                             f"image={f['image']}")
                lines.append(f"  - inst 0: `{f['instructions'][0]}`")
                lines.append(f"  - inst 1: `{f['instructions'][1]}`")
                lines.append(f"  - pred 0: {f['pred_xys'][0]}  "
                             f"target 0: {[round(x,1) for x in f['target_bboxes'][0]]}")
                lines.append(f"  - pred 1: {f['pred_xys'][1]}  "
                             f"target 1: {[round(x,1) for x in f['target_bboxes'][1]]}")
            lines.append("")
    out_path.write_text("\n".join(lines))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--bench", default="data/benchmark")
    args = ap.parse_args()
    run = Path(args.run)
    bench = Path(args.bench)
    mdirs = _model_dirs(run)

    report = {
        "run": str(run),
        "per_app_screenspot": per_application_screenspot(mdirs),
        "cohens_h": cohens_h_vs_chance(mdirs),
        "lexical_breakdown": lexical_failure_breakdown(bench, mdirs),
        "qualitative": qualitative_failures(bench, mdirs),
        "cost": cost_report(mdirs),
        "real_vs_synthetic": real_vs_synthetic(bench, mdirs),
        "pair_signature": pair_consistency_signature(mdirs),
        "model_level_correlation": model_level_correlation(bench, mdirs),
    }
    out_json = run / "deep_analysis.json"
    out_json.write_text(json.dumps(report, indent=2, default=str))
    write_markdown(report, run / "deep_analysis.md")
    print(f"wrote {out_json} and {run / 'deep_analysis.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
