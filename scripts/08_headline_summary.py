#!/usr/bin/env python
"""Print the paper's headline results from a completed run.

Reads runs/<exp>/analysis.json (produced by 06_analyze.py) and emits:
  * per-primitive table with bootstrap CIs, pair-consistency, distractor rate
  * paired McNemar p-values between control conditions and the main run
  * primitive -> ScreenSpot-Pro regression coefficients with odds ratios
  * a compact text summary suitable for the paper's Section 4 (Results).

  --run     path to a completed run directory
  --md      also write a Markdown table block to runs/<exp>/headline.md
"""
import _bootstrap  # noqa: F401
import argparse
import json
from pathlib import Path
from collections import defaultdict


def _fmt(x, n=3):
    return "n/a" if x is None or isinstance(x, str) else f"{x:.{n}f}"


def emit(run_dir: Path, md: bool) -> None:
    analysis = json.loads((run_dir / "analysis.json").read_text())
    models = analysis["models"]
    if not models:
        print("no models in analysis.json")
        return

    # Per-primitive table per model.
    print("=" * 88)
    print(f"PER-PRIMITIVE ACCURACY  (run: {run_dir})")
    print("=" * 88)
    primitives = sorted({p for m in models.values() for p in m["per_primitive"]})
    header = f"{'primitive':<22} " + " ".join(f"{k[:14]:>14}" for k in models)
    print(header)
    print("-" * len(header))
    for p in primitives:
        row = f"  {p:<20}"
        for mk, m in models.items():
            t = m["per_primitive"].get(p)
            if t:
                row += f" {t['accuracy']:.2f} [{t['ci_lo']:.2f},{t['ci_hi']:.2f}]"
            else:
                row += f" {'':>14}"
        print(row)
    print()
    for mk, m in models.items():
        n_total = m.get("n", "?")
        loose = m.get("overall_loose_accuracy")
        loose_str = f"  loose={loose:.3f}" if loose is not None else ""
        print(f"  overall  {mk:<28} acc={m['overall_accuracy']:.3f}{loose_str}  n={n_total}")
    print(f"  (loose = prediction within 2x target-diagonal of center; "
          f"complements strict point-in-box on tiny UI-Vision targets)")

    # Fair same-split (human-verified core) comparison.
    fair = analysis.get("fair_core_comparison", {})
    if fair:
        print()
        print("FAIR-CORE COMPARISON  (every model on the SAME 196-item core split)")
        print(f"  {'model':<28} {'n':>4} {'acc':>7}")
        for mk in sorted(fair, key=lambda k: -fair[k]["overall_accuracy"]):
            d = fair[mk]
            print(f"  {mk:<28} {d['n']:>4d} {d['overall_accuracy']:>7.3f}")

    # Pair consistency per primitive (sanity check on minimal-pair behaviour).
    print()
    print("PAIR CONSISTENCY  (fraction of pairs where BOTH members correct)")
    print(f"  chance for a 2-option primitive = 0.25 under independence (=acc^2 at acc=0.5)")
    for p in primitives:
        row = f"  {p:<20}"
        for mk, m in models.items():
            t = m["per_primitive"].get(p)
            if t:
                pc = t.get("pair_consistency", 0.0)
                acc2 = t["accuracy"] ** 2
                npairs = t.get("n_complete_pairs", 0)
                # Hide pair_consistency when too few complete pairs to be meaningful.
                if npairs < 5:
                    row += f" {'(n<5)':>14}"
                else:
                    marker = "*" if pc < 0.5 * acc2 else " "
                    row += f" {pc:.2f}{marker}(n={npairs})"
            else:
                row += f" {'':>14}"
        print(row)
    print("  '*' marks primitives where pair_consistency < accuracy^2/2 — the")
    print("    What's-Up signature of relational (not random) failure.")
    print("  '(n<5)' hides pair_consistency when fewer than 5 complete pairs ran "
          "(e.g. closed models on the 196-item core).")

    # Controls.
    if analysis.get("controls"):
        print()
        print("SHORTCUT CONTROLS")
        for mk, c in analysis["controls"].items():
            print(f"  [{mk}]")
            for name, acc in c["accuracy"].items():
                check = c.get("checks", {}).get(name, {})
                tag = ""
                if check:
                    tag = " PASS" if check.get("passed") else " FAIL"
                    if check.get("mcnemar_p") is not None:
                        tag += f" (mcn p={check['mcnemar_p']:.3g})"
                    if "reason" in check:
                        tag += f"  — {check['reason']}"
                print(f"    {name:<14} acc={acc:.3f}{tag}")

    # Intervention comparisons.
    if analysis.get("comparisons"):
        print()
        print("INTERVENTION vs BASELINE (paired McNemar, Holm-corrected)")
        for mk, comps in analysis["comparisons"].items():
            print(f"  [{mk}]")
            for name, c in comps.items():
                print(f"    {name:<14} acc_delta={c.get('acc_delta',0):+.3f}  "
                      f"p_raw={_fmt(c.get('p_raw'))}  "
                      f"p_adj={_fmt(c.get('p_adj'))}  "
                      f"reject={c.get('reject', False)}")

    # Regression — THE headline scientific result.
    reg = analysis.get("regression")
    if reg and "primitives" in reg:
        print()
        print("PRIMITIVE -> SCREENSPOT-PRO REGRESSION")
        print(f"  pseudo R^2 = {reg['pseudo_r2']:.3f},  n_obs = {reg['n_obs']},  "
              f"model fixed effects + log_area control,  item-clustered SEs,")
        print(f"  standardized predictors,  active primitives: "
              f"{', '.join(reg.get('active_primitives', []))}")
        print(f"  {'primitive':<22} {'coef':>8} {'odds':>8} {'p':>10}  note")
        for p, c in reg["primitives"].items():
            sig = "***" if c["p_value"] < 0.001 else "**" if c["p_value"] < 0.01 else \
                  "*" if c["p_value"] < 0.05 else " "
            note = "UNSTABLE" if c.get("unstable") else ""
            print(f"  {p:<22} {c['coef']:>+8.2f} {c['odds_ratio']:>8.2f} "
                  f"{c['p_value']:>10.3g} {sig}  {note}")
        if reg.get("coefficient_stability_warning"):
            print()
            for line in [reg["coefficient_stability_warning"][i:i+78]
                         for i in range(0, len(reg["coefficient_stability_warning"]), 78)]:
                print(f"  ! {line}")
    elif reg:
        print()
        print(f"REGRESSION SKIPPED: {reg.get('error', 'insufficient data')}")
    else:
        print()
        print("REGRESSION SKIPPED: needs >=2 models with both diagnostic and "
              "ScreenSpot-Pro data")

    if md:
        out = run_dir / "headline.md"
        with open(out, "w") as f:
            f.write(f"# Headline results — {run_dir.name}\n\n")
            f.write("## Per-primitive accuracy (with bootstrap 95% CI)\n\n")
            f.write("| primitive | " + " | ".join(models) + " |\n")
            f.write("|---|" + "|".join("---:" for _ in models) + "|\n")
            for p in primitives:
                row = [p]
                for mk, m in models.items():
                    t = m["per_primitive"].get(p)
                    row.append(f"{t['accuracy']:.2f} [{t['ci_lo']:.2f},{t['ci_hi']:.2f}]"
                               if t else "")
                f.write("| " + " | ".join(row) + " |\n")
            if reg and "primitives" in reg:
                f.write(f"\n## Primitive → ScreenSpot-Pro regression"
                        f" (pseudo R²={reg['pseudo_r2']:.3f}, n={reg['n_obs']})\n\n")
                f.write("| primitive | coef | odds ratio | p-value |\n|---|---:|---:|---:|\n")
                for p, c in reg["primitives"].items():
                    f.write(f"| {p} | {c['coef']:+.2f} | {c['odds_ratio']:.2f} "
                            f"| {c['p_value']:.3g} |\n")
        print(f"\n[wrote markdown summary -> {out}]")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--md", action="store_true")
    args = ap.parse_args()
    emit(Path(args.run), args.md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
