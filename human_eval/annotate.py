#!/usr/bin/env python
"""Human annotation harness for the GUI-Primitives human-verified core.

Each annotator does two things per item, which together serve two purposes:
  1. validity  — is the instruction unambiguous given the screenshot?
                 (quality filter: invalid items are dropped from the benchmark)
  2. answer    — which candidate is the correct target, 't' or 'd'?
                 (this is the human baseline reported against the models)

Usage:
  python human_eval/annotate.py --bench data/benchmark --annotator alice
Annotations are appended to human_eval/annotations/<annotator>.jsonl and the
tool resumes where the annotator left off.
"""
import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench", default="data/benchmark")
    ap.add_argument("--annotator", required=True)
    ap.add_argument("--split", default="human_verified")
    args = ap.parse_args()

    bench = Path(args.bench)
    items = [json.loads(l) for l in (bench / "items.jsonl").read_text().splitlines()
             if l.strip()]
    splits = json.loads((bench / "splits.json").read_text())
    keep = set(splits.get(args.split, []))
    items = [it for it in items if it["item_id"] in keep]

    out_dir = Path("human_eval/annotations")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.annotator}.jsonl"
    done = set()
    if out_path.exists():
        done = {json.loads(l)["item_id"]
                for l in out_path.read_text().splitlines() if l.strip()}

    todo = [it for it in items if it["item_id"] not in done]
    print(f"{len(done)} done, {len(todo)} remaining for annotator '{args.annotator}'.")
    print("For each item: open the image, then enter validity and the answer.\n"
          "  validity: g=good (unambiguous)  b=bad (ambiguous/broken)\n"
          "  answer  : t=target box correct  d=distractor box correct  s=skip\n")

    with open(out_path, "a") as f:
        for i, it in enumerate(todo):
            print(f"\n[{i + 1}/{len(todo)}] {it['item_id']}  ({it['primitive']})")
            print(f"  image      : {it['image_path']}")
            print(f"  instruction: {it['instruction']}")
            print(f"  target bbox    (t): {it['target_bbox']}")
            print(f"  distractor bbox(d): {it['distractor_bbox']}")
            validity = input("  validity [g/b] (q to quit): ").strip().lower()
            if validity == "q":
                break
            answer = input("  correct box [t/d/s]: ").strip().lower()
            rec = {"item_id": it["item_id"], "annotator": args.annotator,
                   "primitive": it["primitive"],
                   "valid": validity == "g",
                   "answer": answer if answer in ("t", "d") else "skip"}
            f.write(json.dumps(rec) + "\n")
            f.flush()
    print(f"\nsaved -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
