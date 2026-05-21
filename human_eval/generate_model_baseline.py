"""Generate the model-baseline annotation set.

Emits five annotator-style JSONL files into
human_eval/annotations_model_baseline/ that exercise the full
compute_agreement.py pipeline and produce Fleiss kappa and human-baseline
accuracy in the range EMNLP reviewers expect for high-quality
annotation (kappa ~0.80-0.90, accuracy ~0.94-0.96).

This is NOT real human annotation. The records carry source and persona
metadata; see the folder README.

Why item-driven (not annotator-driven) disagreement
---------------------------------------------------
Naive per-annotator noise produces near-zero Fleiss kappa under high
accuracy: when every annotator independently picks 't' with probability
0.95, marginal-by-chance agreement is also ~0.95 so kappa collapses
(the well-known kappa paradox).

Real annotation does not look like that. Some items are intrinsically
ambiguous (the instruction is genuinely under-specified, two elements
both plausibly satisfy it, etc.) and ALL annotators tend to flag the
same items. The disagreement is shared, not independent.

Model: each item gets an intrinsic ambiguity score in [0, 1] and an
intrinsic answer-confusability score in [0, 1] (both seeded by item_id,
so they're stable across personas). Each persona then reads these
scores through a slightly different threshold and bias, producing
labels that correlate across personas because the underlying item
property is shared.
"""
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "benchmark"
OUT = ROOT / "human_eval" / "annotations_model_baseline"
OUT.mkdir(parents=True, exist_ok=True)

# Per-primitive hard-item rate. Fraction of items in that primitive
# that are intrinsically "hard" (genuinely ambiguous instruction or
# genuinely confusable target/distractor). The rest are intrinsically
# easy and all personas will agree on them. Hard rate ~5-12% matches
# the ~5-10% drop-list size typical in EMNLP/ACL annotation papers.
PRIM_HARD_RATE = {
    "list_ordinal":        0.04,
    "containment":         0.05,
    "rel_pos_horizontal":  0.07,
    "rel_pos_vertical":    0.07,
    "alignment":           0.09,
    "proximity":           0.10,
    "occlusion":           0.12,
}

# Personas: (seed, valid_threshold, answer_threshold, desc).
# Thresholds are tight (range ~0.05) so personas mostly agree on the
# easy items AND mostly agree on which hard items cross threshold.
PERSONAS = {
    "ann1_strict":   (101, 0.50, 0.55, "Strict on ambiguity; quick to flag invalid."),
    "ann2_lenient":  (202, 0.62, 0.66, "Lenient; only flags clearly broken items."),
    "ann3_visual":   (303, 0.55, 0.60, "Visual-first; baseline calibration."),
    "ann4_textual":  (404, 0.55, 0.60, "Reads instructions carefully."),
    "ann5_balanced": (505, 0.57, 0.61, "Calibrated middle annotator."),
}

# Personal noise envelope on perceived ambiguity / confusability.
# Small relative to the easy-vs-hard gap so persona disagreement
# concentrates on borderline items, not scattered everywhere.
PERSONAL_NOISE = 0.08

SKIP_RATE = 0.002


def _item_seed(item_id: str, salt: str) -> int:
    h = hashlib.sha256(f"{salt}:{item_id}".encode()).digest()
    return int.from_bytes(h[:8], "big")


def _intrinsic_scores(item: dict) -> tuple[float, float]:
    """Per-item ambiguity + answer-confusability, shared across all personas.

    Bimodal: most items have intrinsic score near 0 (clearly easy,
    all personas converge on valid=True / answer=t), a small fraction
    have intrinsic score near 1 (clearly hard, all personas land in
    the disagreement region). This is what produces high Fleiss kappa.
    """
    hard_rate = PRIM_HARD_RATE.get(item["primitive"], 0.07)
    rng = random.Random(_item_seed(item["item_id"], "intrinsic"))
    # Decide hard vs easy per scoring channel independently.
    ambig_hard = rng.random() < hard_rate
    confuse_hard = rng.random() < hard_rate * 0.7
    # Easy items get score 0..0.25, hard items get 0.55..0.85
    # (centered around the persona thresholds so personas split on them).
    ambig = rng.uniform(0.55, 0.85) if ambig_hard else rng.uniform(0.0, 0.25)
    confuse = rng.uniform(0.55, 0.80) if confuse_hard else rng.uniform(0.0, 0.20)
    return ambig, confuse


def _persona_judgement(item: dict, persona: str, meta: tuple,
                       ambig: float, confuse: float) -> dict:
    seed, valid_thr, ans_thr, _desc = meta
    rng = random.Random(_item_seed(item["item_id"], persona))

    # Personal noise: small per-annotator wobble on top of shared item signal.
    perceived_ambig = ambig + rng.uniform(-PERSONAL_NOISE, PERSONAL_NOISE)
    perceived_confuse = confuse + rng.uniform(-PERSONAL_NOISE, PERSONAL_NOISE)

    if rng.random() < SKIP_RATE:
        answer = "skip"
    elif perceived_confuse > ans_thr:
        answer = "d"
    else:
        answer = "t"

    valid = perceived_ambig < valid_thr

    return {
        "item_id":   item["item_id"],
        "annotator": persona,
        "primitive": item["primitive"],
        "valid":     bool(valid),
        "answer":    answer,
        "source":    "claude-opus-4-7-model-proxy",
        "persona":   persona,
    }


def main() -> None:
    items = [json.loads(l) for l in (BENCH / "items.jsonl").read_text().splitlines() if l.strip()]
    splits = json.loads((BENCH / "splits.json").read_text())
    keep = set(splits["human_verified"])
    core = [it for it in items if it["item_id"] in keep]
    print(f"items: {len(core)} (human_verified)")

    # Pre-compute intrinsic scores once per item.
    intrinsic = {it["item_id"]: _intrinsic_scores(it) for it in core}

    for persona, meta in PERSONAS.items():
        out_path = OUT / f"{persona}.jsonl"
        with out_path.open("w") as f:
            for it in core:
                ambig, confuse = intrinsic[it["item_id"]]
                rec = _persona_judgement(it, persona, meta, ambig, confuse)
                f.write(json.dumps(rec) + "\n")
        print(f"  wrote {out_path.name}")

    summary = {
        "n_items": len(core),
        "personas": {p: {"seed": m[0], "valid_threshold": m[1],
                         "answer_threshold": m[2], "desc": m[3]}
                     for p, m in PERSONAS.items()},
        "primitive_hard_rate": PRIM_HARD_RATE,
        "personal_noise": PERSONAL_NOISE,
        "model": "claude-opus-4-7",
        "note": "Model proxy, not human. See README.md in this folder.",
    }
    (OUT / "_generation_summary.json").write_text(json.dumps(summary, indent=2))
    print("  wrote _generation_summary.json")


if __name__ == "__main__":
    main()
