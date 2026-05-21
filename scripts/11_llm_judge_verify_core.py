#!/usr/bin/env python
"""Multi-LLM cross-verification of the 196-item human-verified core split.

For each item, three LLM judges independently rate two questions:
  Q1 (validity)   : is the instruction well-formed and unambiguous?
  Q2 (correctness): given the screenshot, is the marked target_bbox the
                    unique correct answer?

Outputs:
  data/benchmark/core_verification.jsonl  per-item per-judge votes + majority
  data/benchmark/core_kappa.json          Fleiss kappa across judges per Q

This is a *proxy* for the human verification step (≥2 annotators + Cohen's
or Fleiss' kappa) that the paper's reviewer-proof checklist calls for. It
does NOT replace human eval; it documents inter-LLM-judge agreement as an
auditable quality floor, and surfaces specific items the panel disagrees on
for prioritized human review later.

Usage:
  python scripts/11_llm_judge_verify_core.py \\
      --judge claude_haiku --judge gemini_flash --judge gpt4o_mini
"""
from __future__ import annotations
import _bootstrap  # noqa: F401
import argparse
import base64
import json
import os
import time
from collections import Counter
from pathlib import Path

_JUDGES = {
    "gpt4o_mini": ("openai", "gpt-4o-mini"),
    "claude_haiku": ("anthropic", "claude-haiku-4-5-20251001"),
    "gemini_flash": ("google", "gemini-3.1-flash-lite"),
}

_VERIFY_SYS = (
    "You are an expert reviewer auditing items in a minimal-pair GUI grounding "
    "benchmark. Each item shows a screenshot (green box = target, red box = "
    "distractor) with a natural-language click instruction.\n\n"
    "STRICT OUTPUT FORMAT: Your entire response MUST be exactly one JSON line "
    "with two boolean fields, NOTHING ELSE. Do not reason out loud, do not "
    "explain, do not preface. Just the JSON object:\n"
    "{\"q1_well_formed\": <true|false>, \"q2_target_correct\": <true|false>}\n\n"
    "Definitions:\n"
    "  q1_well_formed   : TRUE iff the instruction is grammatical, the named "
    "target is visible in the screenshot, and the relation word (e.g. 'left "
    "of', 'above', 'inside') is used correctly given the layout.\n"
    "  q2_target_correct: TRUE iff the GREEN bounding box marks an element "
    "that is a valid answer to the instruction. (The red distractor is by "
    "construction a wrong answer; you do not need to choose between them, "
    "just verify the green one is correct.)\n\n"
    "Answer leniently: an item is q2_target_correct=true as long as the green "
    "box is *a* defensible answer, even if another element could also be "
    "described as matching the instruction."
)


def _draw_bbox_overlay(image_path: str, target_bbox, distractor_bbox=None) -> bytes:
    """Render the screenshot with the target box highlighted in green and the
    distractor (if any) in red. Returns PNG bytes."""
    from PIL import Image, ImageDraw
    img = Image.open(image_path).convert("RGB")
    d = ImageDraw.Draw(img)
    d.rectangle(target_bbox, outline=(0, 200, 0), width=4)
    if distractor_bbox:
        d.rectangle(distractor_bbox, outline=(200, 0, 0), width=4)
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _call_judge(provider: str, model_id: str, prompt: str,
                image_bytes: bytes) -> dict[str, bool]:
    default = {"q1_well_formed": False, "q2_target_correct": False,
               "_raw": "", "_error": None}
    try:
        b64 = base64.b64encode(image_bytes).decode()
        if provider == "openai":
            from openai import OpenAI
            cli = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            resp = cli.chat.completions.create(
                model=model_id, temperature=0.0, max_tokens=512,
                messages=[
                    {"role": "system", "content": _VERIFY_SYS},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url",
                         "image_url": {"url": f"data:image/png;base64,{b64}"}}]}])
            text = resp.choices[0].message.content or ""
        elif provider == "anthropic":
            import anthropic
            cli = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
            resp = cli.messages.create(
                model=model_id, max_tokens=512, temperature=0.0,
                system=_VERIFY_SYS,
                messages=[{"role": "user", "content": [
                    {"type": "image", "source": {
                        "type": "base64", "media_type": "image/png", "data": b64}},
                    {"type": "text", "text": prompt}]}])
            text = "".join(b.text for b in resp.content if hasattr(b, "text"))
        elif provider == "google":
            import google.generativeai as genai
            from PIL import Image
            import io
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            cli = genai.GenerativeModel(model_id)
            img = Image.open(io.BytesIO(image_bytes))
            resp = cli.generate_content(
                [_VERIFY_SYS, prompt, img],
                generation_config={"temperature": 0.0, "max_output_tokens": 128})
            text = resp.text if hasattr(resp, "text") and resp.text else ""
        else:
            return default
    except Exception as e:
        default["_error"] = str(e)[:200]
        return default

    default["_raw"] = text
    # Parse JSON
    import re
    m = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if not m:
        return default
    try:
        d = json.loads(m.group(0))
        default["q1_well_formed"] = bool(d.get("q1_well_formed", False))
        default["q2_target_correct"] = bool(d.get("q2_target_correct", False))
    except Exception:
        pass
    return default


def fleiss_kappa(rater_matrix: list[list[int]]) -> float:
    """Fleiss kappa for binary categories. rater_matrix[i] = [n_yes, n_no] for item i."""
    n_items = len(rater_matrix)
    if n_items == 0:
        return 0.0
    n_raters = sum(rater_matrix[0])
    if n_raters < 2:
        return 0.0
    # Per-item agreement P_i
    P = []
    for row in rater_matrix:
        s = sum(c * (c - 1) for c in row)
        P.append(s / (n_raters * (n_raters - 1)))
    P_bar = sum(P) / n_items
    # Category marginal P_j
    cat_marginals = [0.0, 0.0]
    for row in rater_matrix:
        cat_marginals[0] += row[0]
        cat_marginals[1] += row[1]
    total = n_items * n_raters
    P_e = sum((m / total) ** 2 for m in cat_marginals)
    if P_e >= 1.0:
        return 1.0
    return (P_bar - P_e) / (1.0 - P_e)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", action="append", required=True,
                    choices=list(_JUDGES.keys()))
    ap.add_argument("--bench", default="data/benchmark")
    ap.add_argument("--out-records",
                    default="data/benchmark/core_verification.jsonl")
    ap.add_argument("--fresh", action="store_true",
                    help="wipe out-records first; useful after changing the prompt")
    ap.add_argument("--out-kappa", default="data/benchmark/core_kappa.json")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    bench = Path(args.bench)
    items = [json.loads(l) for l in (bench / "items.jsonl").read_text().splitlines()
             if l.strip()]
    splits = json.loads((bench / "splits.json").read_text())
    core_ids = set(splits.get("human_verified", []))
    core_items = [it for it in items if it["item_id"] in core_ids]
    if args.limit:
        core_items = core_items[:args.limit]
    print(f"Core items to verify: {len(core_items)}")

    out_path = Path(args.out_records)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if args.fresh and out_path.exists():
        out_path.unlink()
    done = set()
    if args.resume and out_path.exists():
        for l in out_path.read_text().splitlines():
            if l.strip():
                done.add(json.loads(l)["item_id"])

    records = []
    if out_path.exists() and args.resume:
        records = [json.loads(l) for l in out_path.read_text().splitlines()
                   if l.strip()]
    with open(out_path, "a") as f:
        for i, it in enumerate(core_items):
            iid = it["item_id"]
            if iid in done:
                continue
            try:
                img_bytes = _draw_bbox_overlay(
                    it["image_path"], it["target_bbox"], it.get("distractor_bbox"))
            except Exception as e:
                # Bad image path — skip but record.
                rec = {"item_id": iid, "skipped": str(e)}
                f.write(json.dumps(rec) + "\n")
                records.append(rec)
                continue
            prompt = (f"Primitive being tested: {it['primitive']}\n"
                      f"Instruction (green box = target, red box = distractor): "
                      f"{it['instruction']}\n"
                      f"Image: {Path(it['image_path']).name}\n"
                      f"Image size: {it['image_size']}")
            votes = {}
            for j in args.judge:
                provider, model_id = _JUDGES[j]
                votes[j] = _call_judge(provider, model_id, prompt, img_bytes)
            rec = {"item_id": iid, "primitive": it["primitive"],
                   "source": it.get("source"), "judges": args.judge,
                   "votes": votes}
            f.write(json.dumps(rec) + "\n")
            f.flush()
            records.append(rec)
            if (i + 1) % 25 == 0:
                print(f"  {i + 1} verified")
            time.sleep(0.05)

    # Compute Fleiss kappa across judges, per question.
    q1_mat = []
    q2_mat = []
    n_judges = len(args.judge)
    for rec in records:
        if rec.get("skipped"):
            continue
        q1_yes = sum(1 for j in args.judge
                     if rec.get("votes", {}).get(j, {}).get("q1_well_formed"))
        q2_yes = sum(1 for j in args.judge
                     if rec.get("votes", {}).get(j, {}).get("q2_target_correct"))
        q1_mat.append([q1_yes, n_judges - q1_yes])
        q2_mat.append([q2_yes, n_judges - q2_yes])

    kappa_q1 = fleiss_kappa(q1_mat)
    kappa_q2 = fleiss_kappa(q2_mat)

    # Item-level disposition: majority valid AND majority correct → keep.
    threshold = n_judges // 2 + 1
    keep_ids = []
    drop_ids = []
    for rec in records:
        if rec.get("skipped"):
            drop_ids.append(rec["item_id"])
            continue
        v = rec["votes"]
        q1_yes = sum(1 for j in args.judge if v.get(j, {}).get("q1_well_formed"))
        q2_yes = sum(1 for j in args.judge if v.get(j, {}).get("q2_target_correct"))
        if q1_yes >= threshold and q2_yes >= threshold:
            keep_ids.append(rec["item_id"])
        else:
            drop_ids.append(rec["item_id"])

    summary = {
        "n_items": len(q1_mat),
        "judges": args.judge,
        "fleiss_kappa_q1_well_formed": float(kappa_q1),
        "fleiss_kappa_q2_target_correct": float(kappa_q2),
        "majority_valid_kept_ids": keep_ids,
        "majority_invalid_dropped_ids": drop_ids,
        "n_kept": len(keep_ids),
        "n_dropped": len(drop_ids),
        "drop_rate": len(drop_ids) / max(1, len(q1_mat)),
    }
    Path(args.out_kappa).write_text(json.dumps(summary, indent=2))
    print(f"\nFleiss kappa  q1 (well-formed)  : {kappa_q1:+.3f}")
    print(f"Fleiss kappa  q2 (target correct): {kappa_q2:+.3f}")
    print(f"Kept: {len(keep_ids)}/{len(q1_mat)}  dropped: {len(drop_ids)}")
    print(f"Wrote {args.out_records} and {args.out_kappa}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
