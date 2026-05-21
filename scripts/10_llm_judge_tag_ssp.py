#!/usr/bin/env python
"""LLM-as-judge: tag every ScreenSpot-Pro instruction with the spatial
primitives it semantically requires.

The keyword-based `tag_instruction` is high-precision but matches only ~38 of
1,581 SS-Pro items. Many instructions implicitly require spatial primitives
without using the explicit keyword set (e.g., "select the layer at the top of
the panel" requires `containment` + `list_ordinal`). An LLM-as-judge lifts
recall while keeping precision via majority voting across 2-3 judge models.

Usage:
  python scripts/10_llm_judge_tag_ssp.py --judge claude_haiku        # single judge
  python scripts/10_llm_judge_tag_ssp.py --judge claude_haiku --judge gemini_flash --judge gpt4o_mini   # majority

Outputs: data/screenspot_pro/ssp_primitive_tags.jsonl  — one record per item:
  {"item_id": ..., "primitives": {prim: int_count_of_judges_agreeing}, ...}
"""
from __future__ import annotations
import _bootstrap  # noqa: F401
import argparse
import json
import os
import time
from pathlib import Path

from guiprim.config import load_config
from guiprim.benchmark.primitives import PRIMITIVES

_JUDGE_SYS = (
    "You are an expert at classifying GUI grounding instructions by the "
    "spatial primitive(s) they require to solve. Read the instruction and "
    "answer with a JSON object whose keys are exactly the seven primitives "
    "below. For each primitive, output 1 if completing the instruction "
    "requires understanding that spatial relation, else 0. Output ONLY the "
    "JSON object, no other text.\n\n"
    "Primitives:\n"
    "  rel_pos_horizontal — relative left/right of an anchor element\n"
    "  rel_pos_vertical   — relative above/below of an anchor element\n"
    "  containment        — target inside/outside a panel/dialog/region\n"
    "  list_ordinal       — n-th item of a list/menu (first/second/last...)\n"
    "  alignment          — same row/column as an anchor (grid alignment)\n"
    "  proximity          — nearest/closest/farthest/adjacent to an anchor\n"
    "  occlusion          — target is hidden/covered/partly visible\n"
    "If the instruction is a bare 'click X' label-reference with no spatial "
    "anchor (e.g., 'Click the Save icon'), output all zeros."
)

_JUDGES = {
    "gpt4o_mini": ("openai", "gpt-4o-mini"),
    "claude_haiku": ("anthropic", "claude-haiku-4-5-20251001"),
    "gemini_flash": ("google", "gemini-3.1-flash-lite"),
}


def _call_judge(provider: str, model_id: str, instruction: str) -> dict[str, int]:
    """Return {primitive: 0/1} for one instruction from one LLM judge."""
    user = f"Instruction: {instruction}"
    prim_keys = [p.value for p in PRIMITIVES]
    default = {k: 0 for k in prim_keys}
    try:
        if provider == "openai":
            from openai import OpenAI
            cli = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            resp = cli.chat.completions.create(
                model=model_id, temperature=0.0, max_tokens=256,
                messages=[{"role": "system", "content": _JUDGE_SYS},
                          {"role": "user", "content": user}])
            text = resp.choices[0].message.content or ""
        elif provider == "anthropic":
            import anthropic
            cli = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
            resp = cli.messages.create(
                model=model_id, max_tokens=256, temperature=0.0,
                system=_JUDGE_SYS,
                messages=[{"role": "user", "content": user}])
            text = "".join(b.text for b in resp.content if hasattr(b, "text"))
        elif provider == "google":
            import google.generativeai as genai
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            cli = genai.GenerativeModel(model_id)
            resp = cli.generate_content(
                [_JUDGE_SYS, user],
                generation_config={"temperature": 0.0, "max_output_tokens": 256})
            text = resp.text if hasattr(resp, "text") and resp.text else ""
        else:
            return default
    except Exception as e:
        # Rate limits / refusals — leave all zeros for this judge on this item.
        return default

    # Parse JSON out of the response.
    text = text.strip()
    if "```" in text:
        text = text.split("```")[1] if "```" in text else text
        if text.startswith("json"):
            text = text[4:]
    text = text.strip().strip("`").strip()
    try:
        d = json.loads(text)
        return {k: int(bool(d.get(k, 0))) for k in prim_keys}
    except Exception:
        # Try to find the first {...} JSON object
        import re
        m = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if m:
            try:
                d = json.loads(m.group(0))
                return {k: int(bool(d.get(k, 0))) for k in prim_keys}
            except Exception:
                pass
        return default


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", action="append", required=True,
                    choices=list(_JUDGES.keys()),
                    help="LLM judge(s) to use. Pass --judge X --judge Y for a panel.")
    ap.add_argument("--ssp-dir", default="data/screenspot_pro")
    ap.add_argument("--out", default="data/screenspot_pro/ssp_primitive_tags.jsonl")
    ap.add_argument("--limit", type=int, default=None, help="cap items for budget")
    ap.add_argument("--resume", action="store_true",
                    help="skip items already in --out")
    args = ap.parse_args()

    # Load SS-Pro instructions.
    ssp_dir = Path(args.ssp_dir)
    raw = []
    ann_dir = ssp_dir / "annotations"
    for jf in sorted(ann_dir.glob("*.json")):
        raw.extend(json.loads(jf.read_text()))
    if args.limit:
        raw = raw[:args.limit]
    print(f"SS-Pro items to tag: {len(raw)}")

    # Resume from prior file if requested.
    done = set()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if args.resume and out_path.exists():
        for l in out_path.read_text().splitlines():
            if l.strip():
                done.add(json.loads(l)["item_id"])

    prim_keys = [p.value for p in PRIMITIVES]
    n_done_now = 0
    with open(out_path, "a") as f:
        for i, rec in enumerate(raw):
            iid = rec.get("id", f"ssp-{i}")
            if iid in done:
                continue
            instr = rec.get("instruction", "")
            votes: dict[str, list[int]] = {k: [] for k in prim_keys}
            for j in args.judge:
                provider, model_id = _JUDGES[j]
                d = _call_judge(provider, model_id, instr)
                for k in prim_keys:
                    votes[k].append(d.get(k, 0))
            # Aggregate: count of judges saying 1.
            counts = {k: sum(votes[k]) for k in prim_keys}
            # Majority decision over the requested judges.
            n_judges = len(args.judge)
            majority = {k: counts[k] > n_judges / 2 for k in prim_keys}
            out_rec = {
                "item_id": iid,
                "instruction": instr,
                "judges": args.judge,
                "vote_counts": counts,
                "majority_primitives": [k for k, v in majority.items() if v],
            }
            f.write(json.dumps(out_rec) + "\n")
            f.flush()
            n_done_now += 1
            if n_done_now % 50 == 0:
                print(f"  {n_done_now} tagged")
            # Be polite to APIs
            time.sleep(0.05)
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
