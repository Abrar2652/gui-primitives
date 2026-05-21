#!/usr/bin/env python
"""Extra analyses produced from existing JSONLs, with no new model inference:

  (B) Per-primitive intervention deltas table:
      for every (model, intervention, primitive) cell, report
      acc_baseline -> acc_intervention with paired bootstrap CI on delta.

  (C) Source-stratified model-level competence correlation:
      re-fit Spearman/Pearson between GUI-Primitives accuracy and
      ScreenSpot-Pro accuracy separately on
          - all items
          - real (UI-Vision) screenshots only
          - synthetic items only
      to verify the headline rho=1.0 isn't driven by one source.

  (D) Bootstrap 95% CI on intervention accuracy deltas
      via item-paired resampling (1000 resamples).

Writes runs/<run>/extras_analysis.json plus runs/<run>/extras_analysis.md.
"""
from __future__ import annotations
import _bootstrap  # noqa: F401
import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from guiprim.eval.metrics import score_records


def _read(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def _model_dirs(run: Path) -> list[Path]:
    return [d for d in sorted(run.iterdir()) if d.is_dir()]


# -------------------- (S1) loose-accuracy sensitivity curve ----------------
def loose_accuracy_sensitivity(model_dirs: list[Path],
                               items_path: Path) -> dict:
    """Reviewer S1: justify the 2x-diagonal loose-tolerance. Show how
    accuracy varies as the tolerance multiplier sweeps over {0 (strict),
    1, 2, 3, 5}-times the target bbox diagonal. If our 2x choice is
    arbitrary, the curve will look strange; if it's natural, the
    sensitivity is monotone and well-behaved."""
    import math
    items = {it["item_id"]: it for it in _read(items_path)}
    multipliers = [0.0, 1.0, 2.0, 3.0, 5.0]
    out: dict = {"multipliers": multipliers, "models": {}}
    for mdir in model_dirs:
        recs = _read(mdir / "diagnostic.jsonl")
        if not recs:
            continue
        # For each item we already have correct (point-in-box). For loose at
        # multiplier k, need predicted dist <= k * bbox_diagonal.
        scored = score_records(recs)
        by_mult: dict[float, dict[str, float]] = {}
        for k in multipliers:
            hits_all = hits_real = hits_synth = 0
            n_all = n_real = n_synth = 0
            for r in scored:
                if r.get("pred_xy") is None or r.get("dist") is None:
                    n_all += 1
                    if items.get(r["item_id"], {}).get("source") == "ui_vision":
                        n_real += 1
                    else:
                        n_synth += 1
                    continue
                bb = r["target_bbox"]
                diag = math.hypot(bb[2] - bb[0], bb[3] - bb[1])
                tol = k * diag
                # k=0 means strict point-in-box (use existing `correct`).
                hit = r["correct"] if k == 0.0 else (r["dist"] <= tol)
                n_all += 1
                hits_all += int(hit)
                if items.get(r["item_id"], {}).get("source") == "ui_vision":
                    n_real += 1
                    hits_real += int(hit)
                else:
                    n_synth += 1
                    hits_synth += int(hit)
            by_mult[k] = {"all_acc": hits_all / n_all if n_all else 0.0,
                          "real_acc": hits_real / n_real if n_real else 0.0,
                          "synth_acc": hits_synth / n_synth if n_synth else 0.0}
        out["models"][mdir.name] = by_mult
    return out


# -------------------- (S2) per-app primitive predictive analysis -----------
def per_app_primitive_predictive(model_dirs: list[Path]) -> dict:
    """Reviewer S2: do specific primitives predict failure in specific apps?

    For each application, compute the average SS-Pro accuracy across models,
    cross-classified by whether the item required each primitive (via the
    LLM-judge tags). An app with much-lower accuracy on items needing a
    primitive than on items NOT needing it identifies where that primitive
    is the bottleneck."""
    # Load LLM tags
    from guiprim.eval.regression import _load_llm_tags
    tags = _load_llm_tags("data/screenspot_pro/ssp_primitive_tags.jsonl")
    if not tags:
        return {"note": "no LLM tags available; skipping per-app primitive analysis"}

    # Gather per-(app, primitive) accuracy across all models that ran SS-Pro
    from collections import defaultdict
    per_app: dict = defaultdict(lambda: defaultdict(list))
    for mdir in model_dirs:
        recs = _read(mdir / "screenspot.jsonl")
        if not recs:
            continue
        scored = score_records(recs)
        for r in scored:
            iid = r["item_id"]
            app = r.get("application") or iid.split("_")[0]
            required = set(tags.get(iid, []))
            for p in ["rel_pos_horizontal", "rel_pos_vertical", "containment",
                      "list_ordinal", "alignment", "proximity", "occlusion"]:
                key = (app, p, "required" if p in required else "not_required")
                per_app[key[0]][f"{key[1]}_{key[2]}"].append(int(r["correct"]))

    # Compute mean acc per (app, primitive, required/not).
    out: dict = {}
    for app, m in per_app.items():
        row = {}
        for k, vals in m.items():
            if vals:
                row[k] = {"n": len(vals), "acc": sum(vals) / len(vals)}
        # For each primitive, compute the *delta* (req - not_req)
        for p in ["rel_pos_horizontal", "rel_pos_vertical", "containment",
                  "list_ordinal", "alignment", "proximity", "occlusion"]:
            req = row.get(f"{p}_required")
            nor = row.get(f"{p}_not_required")
            if req and nor and req["n"] >= 3 and nor["n"] >= 3:
                row[f"{p}_delta_required_minus_not"] = req["acc"] - nor["acc"]
        out[app] = row
    return out


# -------------------- (B) per-primitive intervention deltas ----------------
def per_primitive_interventions(model_dirs: list[Path],
                                items_path: Path,
                                n_resamples: int = 1000) -> dict:
    """For each (model, intervention), compute per-primitive accuracy delta
    vs baseline, with item-paired bootstrap 95% CI on the delta."""
    rng = random.Random(13)
    out: dict = {}
    for mdir in model_dirs:
        base = _read(mdir / "iv_baseline.jsonl")
        if not base:
            continue
        base_scored = {r["item_id"]: r["correct"]
                       for r in score_records(base)}
        ivs: dict[str, dict] = {}
        for iv_file in sorted(mdir.glob("iv_*.jsonl")):
            name = iv_file.stem.replace("iv_", "")
            if name == "baseline":
                continue
            iv_scored = {r["item_id"]: r for r in score_records(_read(iv_file))}
            common = [iid for iid in base_scored if iid in iv_scored]
            if not common:
                continue
            # Group by primitive
            by_prim: dict[str, list[tuple[int, int]]] = defaultdict(list)
            for iid in common:
                prim = iv_scored[iid].get("primitive", "?")
                by_prim[prim].append((int(base_scored[iid]),
                                      int(iv_scored[iid]["correct"])))
            rows = {}
            for prim, pairs in by_prim.items():
                if not pairs:
                    continue
                base_acc = sum(a for a, _ in pairs) / len(pairs)
                iv_acc = sum(b for _, b in pairs) / len(pairs)
                delta = iv_acc - base_acc
                # Item-paired bootstrap on the delta
                deltas = []
                n = len(pairs)
                for _ in range(n_resamples):
                    sample = [pairs[rng.randrange(n)] for _ in range(n)]
                    da = sum(a for a, _ in sample) / n
                    db = sum(b for _, b in sample) / n
                    deltas.append(db - da)
                deltas.sort()
                lo, hi = deltas[int(0.025 * n_resamples)], deltas[int(0.975 * n_resamples) - 1]
                rows[prim] = {"n": n,
                              "baseline_acc": base_acc,
                              "intervention_acc": iv_acc,
                              "delta": delta,
                              "delta_ci_lo": lo, "delta_ci_hi": hi,
                              "sig": (lo > 0 or hi < 0)}
            ivs[name] = rows
        if ivs:
            out[mdir.name] = ivs
    return out


# -------------------- (C) source-stratified correlation --------------------
def stratified_correlation(model_dirs: list[Path], items_path: Path) -> dict:
    """Spearman/Pearson between GUI-Primitives accuracy and ScreenSpot-Pro
    accuracy across models, broken down by item source."""
    items = {it["item_id"]: it for it in _read(items_path)}
    # Compute per-model GUI-Prim accuracy on each source
    per_model: dict[str, dict] = {}
    for mdir in model_dirs:
        diag = _read(mdir / "diagnostic.jsonl")
        ssp = _read(mdir / "screenspot.jsonl")
        if not diag or not ssp:
            continue
        diag_scored = score_records(diag)
        ssp_scored = score_records(ssp)
        ssp_acc = sum(r["correct"] for r in ssp_scored) / len(ssp_scored)
        slices: dict[str, float] = {}
        for src in ("all", "ui_vision", "synthetic"):
            subset = diag_scored if src == "all" else [
                r for r in diag_scored if items.get(r["item_id"], {}).get("source") == src]
            if subset:
                slices[src] = sum(r["correct"] for r in subset) / len(subset)
        per_model[mdir.name] = {"ssp": ssp_acc, **slices}

    # Now compute correlations per slice
    out: dict = {"per_model": per_model, "correlations": {}}
    try:
        from scipy.stats import spearmanr, pearsonr
        for slice_name in ("all", "ui_vision", "synthetic"):
            xs = [d[slice_name] for d in per_model.values() if slice_name in d]
            ys = [d["ssp"] for d in per_model.values() if slice_name in d]
            if len(xs) < 3:
                continue
            rho, prho = spearmanr(xs, ys)
            r, pr = pearsonr(xs, ys)
            out["correlations"][slice_name] = {
                "n_models": len(xs),
                "spearman_rho": float(rho),
                "spearman_p": float(prho),
                "pearson_r": float(r),
                "pearson_p": float(pr),
            }
    except Exception as e:
        out["error"] = str(e)
    return out


# -------------------- (D) bootstrap CIs on intervention deltas -------------
def intervention_deltas_with_ci(model_dirs: list[Path],
                                n_resamples: int = 2000) -> dict:
    """Top-line: each intervention vs baseline, item-paired bootstrap CI on
    the overall accuracy delta."""
    rng = random.Random(13)
    out: dict = {}
    for mdir in model_dirs:
        base = _read(mdir / "iv_baseline.jsonl")
        if not base:
            continue
        base_scored = {r["item_id"]: int(r["correct"])
                       for r in score_records(base)}
        rows: dict[str, dict] = {}
        for iv_file in sorted(mdir.glob("iv_*.jsonl")):
            name = iv_file.stem.replace("iv_", "")
            if name == "baseline":
                continue
            iv_scored = {r["item_id"]: int(r["correct"])
                         for r in score_records(_read(iv_file))}
            common = [iid for iid in base_scored if iid in iv_scored]
            if not common:
                continue
            pairs = [(base_scored[iid], iv_scored[iid]) for iid in common]
            base_acc = sum(a for a, _ in pairs) / len(pairs)
            iv_acc = sum(b for _, b in pairs) / len(pairs)
            delta = iv_acc - base_acc
            deltas = []
            n = len(pairs)
            for _ in range(n_resamples):
                sample = [pairs[rng.randrange(n)] for _ in range(n)]
                da = sum(a for a, _ in sample) / n
                db = sum(b for _, b in sample) / n
                deltas.append(db - da)
            deltas.sort()
            lo = deltas[int(0.025 * n_resamples)]
            hi = deltas[int(0.975 * n_resamples) - 1]
            rows[name] = {"n_items": n, "baseline_acc": base_acc,
                          "intervention_acc": iv_acc, "delta": delta,
                          "delta_ci_lo": lo, "delta_ci_hi": hi,
                          "ci_excludes_zero": lo > 0 or hi < 0}
        if rows:
            out[mdir.name] = rows
    return out


def write_markdown(report: dict, out_path: Path) -> None:
    L = [f"# Extras analysis — {report['run']}\n"]

    L.append("## (D) Intervention deltas with paired bootstrap 95% CI\n")
    L.append("Per-model, per-intervention accuracy improvement over baseline,")
    L.append("with item-paired bootstrap CI on the delta (2000 resamples).\n")
    L.append("| model | intervention | n | baseline | with intervention | Δ (95% CI) | CI excludes 0 |")
    L.append("|---|---|---:|---:|---:|---:|:---:|")
    for mk, ivs in report["intervention_deltas"].items():
        for name, d in ivs.items():
            ci = f"{d['delta']:+.3f}  [{d['delta_ci_lo']:+.3f}, {d['delta_ci_hi']:+.3f}]"
            flag = "✓" if d["ci_excludes_zero"] else "—"
            L.append(f"| {mk} | {name} | {d['n_items']} | "
                     f"{d['baseline_acc']:.3f} | {d['intervention_acc']:.3f} | "
                     f"{ci} | {flag} |")
    L.append("")

    L.append("## (B) Per-primitive intervention deltas\n")
    L.append("Where each intervention helps and where it hurts, per primitive.\n")
    for mk, ivs in report["per_primitive"].items():
        for name, rows in ivs.items():
            L.append(f"### {mk} — {name}\n")
            L.append("| primitive | n | baseline | with intervention | Δ (95% CI) |")
            L.append("|---|---:|---:|---:|---:|")
            for prim, d in sorted(rows.items()):
                marker = " ✓" if d["sig"] else ""
                L.append(f"| {prim} | {d['n']} | {d['baseline_acc']:.3f} | "
                         f"{d['intervention_acc']:.3f} | "
                         f"{d['delta']:+.3f}  "
                         f"[{d['delta_ci_lo']:+.3f}, {d['delta_ci_hi']:+.3f}]{marker} |")
            L.append("")

    L.append("## (C) Source-stratified model-level competence correlation\n")
    L.append("Per-model GUI-Primitives accuracy (overall, real-only, synthetic-only)")
    L.append("vs ScreenSpot-Pro accuracy, then Spearman ρ across models for each slice.")
    L.append("This tests whether the headline rho=1.0 is driven by one source.\n")
    pm = report["stratified_corr"]["per_model"]
    L.append("| model | GUI-Prim (all) | GUI-Prim (real) | GUI-Prim (synth) | SS-Pro |")
    L.append("|---|---:|---:|---:|---:|")
    for mk, d in pm.items():
        L.append(f"| {mk} | {d.get('all', float('nan')):.3f} | "
                 f"{d.get('ui_vision', float('nan')):.3f} | "
                 f"{d.get('synthetic', float('nan')):.3f} | "
                 f"{d.get('ssp', float('nan')):.3f} |")
    L.append("")
    L.append("Spearman ρ between each slice's accuracy and SS-Pro accuracy:\n")
    L.append("| slice | n models | Spearman ρ (p) | Pearson r (p) |")
    L.append("|---|---:|---:|---:|")
    for slc, c in report["stratified_corr"].get("correlations", {}).items():
        L.append(f"| {slc} | {c['n_models']} | "
                 f"{c['spearman_rho']:+.3f} ({c['spearman_p']:.3g}) | "
                 f"{c['pearson_r']:+.3f} ({c['pearson_p']:.3g}) |")
    L.append("")

    L.append("## (S1) Loose-accuracy sensitivity to the tolerance multiplier\n")
    L.append("Reviewer-asked: justify the 2× target-diagonal tolerance. We sweep the")
    L.append("multiplier k ∈ {0, 1, 2, 3, 5} and report accuracy at each. A natural")
    L.append("choice will produce a smooth, monotone curve; an arbitrary choice")
    L.append("would not.\n")
    sens = report.get("loose_sensitivity", {})
    if sens.get("models"):
        muls = sens["multipliers"]
        L.append("| model | " + " | ".join(f"k={m}" for m in muls) + " |")
        L.append("|---|" + "|".join("---:" for _ in muls) + "|")
        for mk, by_mult in sens["models"].items():
            row = [mk] + [f"{by_mult[m]['all_acc']:.3f}" for m in muls]
            L.append("| " + " | ".join(row) + " |")
        L.append("")
        L.append("(k=0 is strict point-in-box; k=2 is the paper's loose metric.")
        L.append(" k=5 effectively converges to in-the-screenshot.)")
        L.append("")

    L.append("## (S2) Per-application × per-primitive predictive analysis\n")
    L.append("Reviewer-asked: do specific primitives predict failure in specific")
    L.append("apps? For each application, we report SS-Pro accuracy delta =")
    L.append("(items needing primitive p) − (items NOT needing p), averaged")
    L.append("across models. A large negative delta says items in that app needing")
    L.append("primitive p are systematically harder.\n")
    per_app = report.get("per_app_primitive", {})
    if per_app and not per_app.get("note"):
        primitives = ["rel_pos_horizontal", "rel_pos_vertical", "containment",
                      "list_ordinal", "alignment", "proximity", "occlusion"]
        L.append("| app | " + " | ".join(p.replace("rel_pos_", "rp_")[:8] for p in primitives) + " |")
        L.append("|---|" + "|".join("---:" for _ in primitives) + "|")
        for app, row in sorted(per_app.items()):
            cells = [app]
            for p in primitives:
                k = f"{p}_delta_required_minus_not"
                v = row.get(k)
                cells.append(f"{v:+.2f}" if v is not None else "—")
            L.append("| " + " | ".join(cells) + " |")
        L.append("")
        L.append("(blank cells = too few items in that app needed/didn't-need the")
        L.append(" primitive to compute a stable delta; minimum 3 items per side.)")
    elif per_app.get("note"):
        L.append(f"_{per_app['note']}_")
    L.append("")

    out_path.write_text("\n".join(L))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--bench", default="data/benchmark")
    args = ap.parse_args()
    run = Path(args.run)
    mdirs = _model_dirs(run)
    items_path = Path(args.bench) / "items.jsonl"

    report = {
        "run": str(run),
        "intervention_deltas": intervention_deltas_with_ci(mdirs),
        "per_primitive": per_primitive_interventions(mdirs, items_path),
        "stratified_corr": stratified_correlation(mdirs, items_path),
        "loose_sensitivity": loose_accuracy_sensitivity(mdirs, items_path),
        "per_app_primitive": per_app_primitive_predictive(mdirs),
    }
    out_json = run / "extras_analysis.json"
    out_json.write_text(json.dumps(report, indent=2, default=str))
    write_markdown(report, run / "extras_analysis.md")
    print(f"wrote {out_json} and {run / 'extras_analysis.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
