#!/usr/bin/env python
"""Post-hoc fix: rescale Anthropic predictions for images whose largest side
exceeded ~1568 px.

Anthropic's vision API silently downsamples images to a max-side of ~1568 px
(and ≤ ~1.15 megapixels). The model outputs click coordinates in the resized
image's pixel space, NOT in the original screenshot's pixel space. Our
existing wrapper passed the original image_wh to the parser, so for images
larger than 1568 px the recorded `pred_xy` is in the wrong coordinate frame
and scores 0 % even when the prediction is in the right place.

This script reads each Anthropic model's prediction JSONL, finds records
whose `meta.image_wh` has max-side > 1568, multiplies `pred_xy` by
(max_orig / 1568), and writes the corrected file with a `.rescaled.jsonl`
suffix. It also writes a rescale report.

Usage:
  python scripts/13_rescale_anthropic.py --run runs/diagnostic
  # then re-run 06_analyze.py / 12_extras_analysis.py
"""
from __future__ import annotations
import _bootstrap  # noqa: F401
import argparse
import json
from pathlib import Path


ANTHROPIC_KEYS = {"closed_claude_haiku", "closed_claude_sonnet", "closed_claude_opus"}
MAX_DIM = 1568  # Anthropic's effective max-side after server-side resize


def rescale_records(in_path: Path, out_path: Path) -> dict:
    # Read all rows FIRST (in case in_path == out_path).
    lines = [l for l in in_path.read_text().splitlines() if l.strip()]
    n_total = n_rescaled = 0
    with open(out_path, "w") as fo:
        for line in lines:
            r = json.loads(line)
            n_total += 1
            pred = r.get("pred_xy")
            iw = (r.get("meta") or {}).get("image_wh")
            if pred and iw:
                W, H = iw
                mx = max(W, H)
                if mx > MAX_DIM:
                    scale = mx / MAX_DIM
                    r["pred_xy"] = [pred[0] * scale, pred[1] * scale]
                    r.setdefault("meta", {})["rescaled_anthropic"] = scale
                    n_rescaled += 1
            fo.write(json.dumps(r) + "\n")
    return {"n_total": n_total, "n_rescaled": n_rescaled}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--in-place", action="store_true",
                    help="overwrite the original JSONL instead of writing a "
                         ".rescaled.jsonl alongside it")
    args = ap.parse_args()

    run = Path(args.run)
    report = {}
    for mdir in sorted(run.iterdir()):
        if not mdir.is_dir() or mdir.name not in ANTHROPIC_KEYS:
            continue
        for jp in sorted(mdir.glob("*.jsonl")):
            target = jp if args.in_place else jp.with_suffix(".rescaled.jsonl")
            r = rescale_records(jp, target)
            report[f"{mdir.name}/{jp.name}"] = {**r, "out": str(target)}
            print(f"  {mdir.name}/{jp.name}: "
                  f"{r['n_rescaled']}/{r['n_total']} records rescaled "
                  f"-> {target.name}")
    out_report = run / "anthropic_rescale_report.json"
    out_report.write_text(json.dumps(report, indent=2))
    print(f"\nReport: {out_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
