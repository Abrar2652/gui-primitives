#!/usr/bin/env python
"""Inter-annotator agreement and the human baseline.

Reads every human_eval/annotations/*.jsonl file and reports:
  * Cohen's kappa (2 annotators) or Fleiss' kappa (>=3) on the validity label,
  * the same on the target/distractor answer,
  * human accuracy = fraction of items where the majority answer == 't'
    (the minimal-pair construction defines 't' as the correct target),
  * the list of items flagged invalid by a majority (to drop from the benchmark).

These numbers go straight into the paper's benchmark-quality paragraph.
"""
import argparse
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path


def cohens_kappa(a: list, b: list) -> float:
    cats = sorted(set(a) | set(b))
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe != 1 else 1.0


def fleiss_kappa(rows: list[list]) -> float:
    """rows[i] = list of category labels assigned to item i by all annotators."""
    cats = sorted({c for r in rows for c in r})
    n_items = len(rows)
    n_raters = len(rows[0]) if rows else 0
    if n_items == 0 or n_raters < 2:
        return float("nan")
    P = []
    p_cat = defaultdict(float)
    for r in rows:
        counts = {c: r.count(c) for c in cats}
        P.append((sum(v * v for v in counts.values()) - n_raters)
                 / (n_raters * (n_raters - 1)))
        for c in cats:
            p_cat[c] += counts[c] / (n_items * n_raters)
    Pbar = sum(P) / n_items
    Pe = sum(v * v for v in p_cat.values())
    return (Pbar - Pe) / (1 - Pe) if Pe != 1 else 1.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ann-dir", default="human_eval/annotations")
    ap.add_argument("--out", default="human_eval/agreement.json")
    args = ap.parse_args()

    files = sorted(Path(args.ann_dir).glob("*.jsonl"))
    if len(files) < 2:
        print("need >=2 annotator files for agreement")
        return 1

    per_ann: dict[str, dict[str, dict]] = {}
    for jf in files:
        recs = {json.loads(l)["item_id"]: json.loads(l)
                for l in jf.read_text().splitlines() if l.strip()}
        per_ann[jf.stem] = recs

    common = set.intersection(*[set(r) for r in per_ann.values()])
    annotators = list(per_ann)
    valid_rows = [[per_ann[a][i]["valid"] for a in annotators] for i in common]
    ans_rows = [[per_ann[a][i]["answer"] for a in annotators] for i in common]

    report: dict = {"n_annotators": len(annotators), "n_common_items": len(common)}
    if len(annotators) == 2:
        a0, a1 = annotators
        report["kappa_validity"] = cohens_kappa(
            [per_ann[a0][i]["valid"] for i in common],
            [per_ann[a1][i]["valid"] for i in common])
        report["kappa_answer"] = cohens_kappa(
            [per_ann[a0][i]["answer"] for i in common],
            [per_ann[a1][i]["answer"] for i in common])
    else:
        report["fleiss_validity"] = fleiss_kappa(valid_rows)
        report["fleiss_answer"] = fleiss_kappa(ans_rows)

    # Majority vote -> human baseline and invalid-item list.
    correct, invalid = 0, []
    for i in common:
        answers = [per_ann[a][i]["answer"] for a in annotators]
        valids = [per_ann[a][i]["valid"] for a in annotators]
        if answers.count("t") > len(answers) / 2:
            correct += 1
        if valids.count(False) >= len(valids) / 2:
            invalid.append(i)
    report["human_accuracy"] = correct / len(common) if common else float("nan")
    report["n_invalid"] = len(invalid)
    report["invalid_items"] = invalid

    Path(args.out).write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "invalid_items"},
                     indent=2))
    print(f"full report -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
