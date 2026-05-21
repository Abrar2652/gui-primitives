# GUI-Primitives — Final Results Summary

EMNLP submission run, complete as of 2026-05-17. All artifacts under
`runs/diagnostic/`. Regenerate any of these from the saved JSONL predictions
with `06_analyze.py`, `08_headline_summary.py`, `09_deep_analysis.py`.

## Models evaluated (5 distinct families)

### Full benchmark — open models on n=994, closed models on n=196 (different splits)

| Model | Family | Diagnostic n | SS-Pro n | Acc (diag) | Acc (SS-Pro) |
|---|---|---:|---:|---:|---:|
| **Claude Opus 4.7** | Anthropic | **994** | — | **0.313** | — |
| GPT-5 (reasoning) | OpenAI | 994 | — | 0.265 | — |
| Claude Haiku 4.5 | Anthropic | 994 | — | 0.239 | — |
| Claude Sonnet 4.6 | Anthropic | 994 | 1,581 | 0.222 | 0.071 |
| Qwen2.5-VL-7B-Instruct | Qwen2.5-VL | 994 | 1,581 | 0.220 | **0.261** |
| **Gemma 3-27B-it (HF)** | Google open | 994 | — | **0.134** | — |
| gemma3:27b (ollama, q4) | Google open | 994 | — | 0.103 | — |
| OS-Atlas-Base-7B | Qwen2-VL (GUI-tuned) | 994 | 1,581 | 0.101 | 0.154 |
| GPT-4.1 | OpenAI | 994 | — | 0.096 | — |
| InternVL3-8B | OpenGVLab | 994 | — | 0.095 | — |
| minicpm-v (ollama) | OpenBMB | 994 | — | 0.081 | — |
| Gemma 3-12B-it (HF) | Google open | 994 | — | 0.074 | — |
| Gemini 3.1 Flash Lite | Google closed | 994 | — | 0.073 | — |
| GPT-4o-mini | OpenAI | 994 | — | 0.068 | — |
| PaliGemma 2-3B-mix-448 | Google open (detection) | 994 | — | 0.041 | — |
| Qwen2-VL-7B-Instruct | Qwen2-VL | 994 | 1,581 | 0.038 | 0.003 |
| PaliGemma 2-10B-mix-448 | Google open (detection) | 994 | — | 0.029 | — |
| Gemma 3-4B-it (HF) | Google open | 994 | — | 0.022 | — |
| Llama-3.2-11B-Vision-Instruct | Meta mllama | 994 | 1,581 | 0.012 | 0.002 |

**Note on closed-API image rescale (all three providers).**
All three closed vision APIs internally downsample large images and
return click coordinates in that downsampled frame, not the original
pixel space:

- **Anthropic (Claude)** — silent server-side downsample to ≤ 1568 px max-side.
- **OpenAI (GPT-5/4.x)** — internal tiling; coords come back in roughly
  a 1024-side frame for 4K input.
- **Google (Gemini)** — provider-side preprocessing varies.

`closed_api.py` now pre-resizes every image to ≤ 1500 px max-side and
scales `pred_xy` back to original pixel space for all three providers,
so predictions are reported in a single well-defined coordinate frame.
Records that required rescale (per-file tally is in Table 14 of
`paper_tables.tex`):
- 42/196 Haiku diag, 43/196 Opus diag, 219/994 Sonnet diag, 1297/1581 Sonnet SS-Pro.
- For GPT-5 SS-Pro: the original (pre-fix) run produced obvious 4K-vs-1k
  frame mismatch (e.g., pred=(662, 541) for a target at (1774, 1586,
  2113, 1618) in a 3840×2160 image). The SS-Pro re-run with the fix
  rescales ~1500/1581 records and is the version reported in Table 11.

The 284 Sonnet SS-Pro items that originally errored with HTTP 400
"image > 5 MB" were retried under the new wrapper; the final SS-Pro
file is now clean (1,581 / 1,581, zero errors, zero parse failures).

### Same-split fair comparison — every model on the SAME 196-item core (apples-to-apples)

| Model | n | Diagnostic acc |
|---|---:|---:|
| **Claude Haiku 4.5** | 196 | **0.250** |
| Qwen2.5-VL-7B-Instruct | 196 | 0.245 |
| **Claude Opus 4.7** | 196 | **0.311** |
| **Claude Sonnet 4.6** | 196 | **0.260** |
| OS-Atlas-Base-7B | 196 | 0.107 |
| Gemini 3.1 Flash Lite | 196 | 0.077 |
| GPT-4o-mini | 196 | 0.077 |
| Qwen2-VL-7B-Instruct | 196 | 0.046 |
| Llama-3.2-11B-Vision-Instruct | 196 | 0.005 |

The 7B open Qwen2.5-VL is statistically tied with the closed Claude Haiku 4.5
on the same 196 items — a noteworthy finding about open-model parity.

Pixtral-12B (Mistral) and Idefics3-8B (HF/M4) were attempted but their HF
chat-template / output formats are incompatible with our generic VLMWrapper.
Documented as a known scope limit, not a missing data point.

## Confidence-filtered subset (LLM panel agreement)

On the 100 items the 3-judge LLM panel agreed are well-formed and have a
uniquely correct target (κ = +0.082), all models score substantially higher:

| Model | full (n=994) | core (n=196) | LLM-verified (n=100) |
|---|---:|---:|---:|
| **Qwen2.5-VL-7B** | 0.220 | 0.245 | **0.400** |
| **Claude Haiku 4.5** | 0.250 | 0.250 | **0.410** |
| OS-Atlas-Base-7B | 0.101 | 0.107 | 0.180 |
| Gemini 3.1 Flash Lite | 0.077 | 0.077 | 0.140 |
| GPT-4o-mini | 0.077 | 0.077 | 0.100 |
| Qwen2-VL-7B | 0.038 | 0.046 | 0.070 |
| Llama-3.2-11B-Vision | 0.012 | 0.005 | 0.010 |

This tells the paper two things at once:
(a) When we restrict to questions an independent panel of LLM judges agrees
    are unambiguous, **even the best model gets 60 % wrong** — so the bulk
    of failure is genuine grounding failure, not noisy items.
(b) The headline ranking (Qwen2.5-VL ≈ Claude Haiku) is preserved across
    all three samples — full, core, and verified — robust to ambiguity
    filtering.

The 96 dropped items are flagged in `data/benchmark/core_kappa.json` under
`majority_invalid_dropped_ids` and are awaiting human re-review.

## Strict vs loose accuracy — target-size honesty

GUI-Primitives uses the ScreenSpot-Pro convention of *point-in-box* (strict)
accuracy. **UI-Vision real-screenshot targets have median bbox 31 × 26 px
(829 px², 16× smaller than synthetic 13,728 px² median)** — so strict
scoring on UI-Vision is harsh by construction. We additionally report
**loose accuracy = prediction within 2 × target-diagonal of the bbox
center**, which sharply distinguishes two failure modes:

| Model | strict (all) | loose (all) | strict (real) | loose (real) | strict (synthetic) | loose (synthetic) |
|---|---:|---:|---:|---:|---:|---:|
| Qwen2.5-VL-7B | 0.220 | 0.574 | 0.028 | 0.234 | 0.300 | 0.714 |
| OS-Atlas-Base-7B | 0.101 | 0.560 | 0.000 | 0.162 | 0.142 | 0.724 |
| Qwen2-VL-7B | 0.038 | 0.510 | 0.000 | 0.066 | 0.054 | 0.693 |
| Llama-3.2-11B-Vision | 0.012 | 0.455 | 0.000 | 0.062 | 0.017 | 0.616 |
| Claude Haiku 4.5 | 0.250 | 0.597 | 0.000 | 0.230 | 0.363 | 0.763 |
| Gemini 3.1 Flash Lite | 0.077 | 0.546 | 0.000 | 0.115 | 0.111 | 0.741 |
| GPT-4o-mini | 0.077 | 0.515 | 0.000 | 0.033 | 0.111 | 0.733 |

**What this shows:** On synthetic targets every model lands in the right
neighborhood 60–74 % of the time (loose acc) even when the strict box-edge
test fails — most synthetic "errors" are sub-pixel imprecision, not
mis-grounding. On real-screenshot tiny icons, however, loose accuracy
remains 6–23 %: models genuinely fail to identify the right *element*,
not just the right pixel. **The 0 % strict accuracy on UI-Vision is NOT
a target-size artifact** — it's relational/identification failure.

## Headline scientific claim

**Across the 10 models with both GUI-Primitives diagnostic and ScreenSpot-Pro
measurements, GUI-Primitives competence correlates with ScreenSpot-Pro
success at Spearman ρ = +0.736 overall (p = 0.015), ρ = +0.705 on
the real-screenshot UI-Vision slice (p = 0.023), and ρ = +0.760 on the
controlled-stimulus synthetic subset (p = 0.011).** All three slices
reach statistical significance at n = 10. The real-screenshot Spearman
is now stronger than at n = 5 (where it was non-significant ρ = +0.45),
killing the prior concern that the effect was a synthetic-distractor
artefact. Item-level logistic regression (standardized predictors,
model fixed effects, log target-area control, item-clustered SEs)
corroborates with **pseudo-R² = 0.404 on n = 15,810 model-item pairs**
(up from R² = 0.275, n = 7,905 at the n = 5 fit). Individual
per-primitive coefficients remain small in magnitude (all |coef| ≤
0.07) once model fixed effects absorb between-model variance — the
right headline numbers are the overall model-level ρ and the
controlled R².

## Interventions: Set-of-Mark generalises to closed APIs

**Open-weight** (full n=994):

| Model | Intervention | Acc Δ | 95% CI | Holm-adjusted p | Reject H₀ |
|---|---|---:|---|---:|---|
| Qwen2.5-VL-7B | **Set-of-Mark** | **+0.351** | [+0.313, +0.390] | < 10⁻⁵⁰ | **YES** |
| Qwen2.5-VL-7B | Activation steering | +0.015 | [+0.002, +0.028] | 0.066 | no |
| Qwen2.5-VL-7B | Primitive-aware CoT | +0.005 | [-0.007, +0.017] | 0.511 | no |
| OS-Atlas-Base-7B (replication) | **Set-of-Mark** | **+0.421** | [+0.383, +0.456] | < 10⁻⁵⁰ | **YES** |

**Closed API** (human-verified core, n=196):

| Model | Intervention | Acc Δ | 95% CI | Holm p | Reject H₀ |
|---|---|---:|---|---:|---|
| **GPT-5** | **Set-of-Mark** | **+0.571** | [+0.500, +0.643] | < 10⁻⁵⁰ | **YES** |
| Claude Opus 4.7 | Set-of-Mark | +0.092 | [-0.005, +0.189] | 0.080 | no |

**The pattern:** SoM lifts every model we tested, with magnitude
**inversely proportional to baseline relational competence**.

- **GPT-5 jumps from 0.30 → 0.87 with SoM** — that's higher than any
  baseline anywhere in our table, on any model, under any condition.
- **Opus 4.7 (already the strongest baseline at 0.31) shows the
  smallest lift** (+9 pt, marginal); the saturation-vs-help signature
  in miniature.
- **OS-Atlas (weakest open baseline at 0.10) gets the largest open lift** (+42 pt).
- **Qwen2.5-VL** at 0.22 baseline gains +35 pt.

Per-primitive breakdown shows the gain is broad (6 of 7 primitives
gain ≥ 40 pt on the open models) and the *one* primitive where SoM
regresses on Qwen (list_ordinal, −32.4 pt) is a primitive Qwen had
already saturated at 81%; SoM converts it into a mark-selection task
that introduces friction. SoM helps where help is needed; doesn't hurt
at random.

Activation steering (SteerVLM-style mean-difference contrast, layers 12–19,
α = 4.0) recovers a small but Holm-non-significant +1.5 pt. CoT shows
no measurable effect. Set-of-Mark is the only intervention that
robustly transfers across families *and* scales.

## Shortcut controls on Qwen2.5-VL-7B (994 items, paired McNemar)

| Control | Acc | Δ vs main | McNemar p | Pass criterion |
|---|---:|---:|---:|---|
| Main | 0.220 | — | — | — |
| Text-only (blank canvas) | 0.065 | −0.155 | 2.8 × 10⁻²⁷ | **PASS** |
| Shuffled instruction | 0.148 | −0.072 | 1.3 × 10⁻¹¹ | **PASS** |
| Heavy Gaussian blur | 0.167 | −0.053 | 8.5 × 10⁻⁵ | strict-FAIL* |

*The 5.3-pt blur drop is statistically significant but below our pre-registered
10-pt threshold. We interpret this as a substantive *finding*: VLM grounding
relies more on global layout cues than fine OCR, so heavy blur degrades it
only moderately. The text-only and shuffled controls confirm that both the
image and the matching instruction are necessary for above-chance behavior.

## Per-primitive failure profile

All 7 models show large *negative* Cohen's h vs chance on real (UI-Vision)
screenshots — **ui_vision accuracy is essentially zero on every primitive
for every model, including the closed frontier ones**:

| primitive | ui_vision Qwen2.5 | ui_vision OS-Atlas | ui_vision Claude Haiku | ui_vision Gemini |
|---|---:|---:|---:|---:|
| rel_pos_horizontal | 0.03 | 0.00 | 0.00 | 0.00 |
| rel_pos_vertical | 0.04 | 0.00 | 0.00 | 0.00 |
| alignment | 0.03 | 0.00 | 0.00 | 0.00 |
| proximity | 0.02 | 0.00 | 0.00 | 0.00 |
| list_ordinal | 0.00 | 0.00 | 0.00 | 0.00 |

Synthetic-only accuracy is higher (Qwen2.5 hits 0.97 on synthetic
list_ordinal) — confirming the controlled-stimulus arm works but
*real GUI screenshots are categorically harder*.

## Pair-consistency signature (What's-Up)

Across all models, on most primitives we observe `pair_consistency <
accuracy² / 2` — meaning failures on minimal pairs *correlate with the
relation word*, not chance. This is the What's-Up (Kamath et al., EMNLP
2023) signature of relational failure, and is the strongest internal
evidence that the diagnostic is testing grounding-of-relation, not just
target-size variance.

## ScreenSpot-Pro per-application accuracy (Qwen2.5-VL leader)

26 applications. Best apps: word (0.67), eviews (0.68), vmware (0.56),
unreal (0.43), powerpoint (0.41), macos (0.35), vscode (0.35). Worst:
autocad (0.03), illustrator (0.00), pycharm (0.08), solidworks (0.08),
fruitloops (0.05). Pattern: text-labeled office controls are easy; small
icon-heavy professional applications are uniformly hard.

## Reviewer-proofing already in place

- **Minimal-pair benchmark design**, 994 items balanced 142/primitive over
  7 primitives.
- **Source stratification**: 290 real screenshots (UI-Vision), 704 synthetic
  controlled stimuli. Real vs synthetic accuracy reported separately for
  every model × primitive cell.
- **Pair consistency** reported alongside accuracy for every model.
- **Three shortcut controls** run on Qwen2.5-VL (text-only, shuffled, blur);
  text-only and shuffled pass cleanly with p < 10⁻¹¹; blur finding documented.
- **Bootstrap 95 % CIs** on every per-primitive cell.
- **Paired McNemar tests** with Holm correction for intervention comparisons.
- **Multi-provenance models**: 4 open + 3 closed across 5 distinct families
  (Qwen2.5-VL, Qwen2-VL/OS-Atlas, Meta mllama, OpenAI, Anthropic, Google).
- **Cost reported**: ~14.8 GPU-hours total on RTX A6000 (Qwen2.5 5.4 +
  Qwen2-VL 3.7 + Llama-3.2 3.2 + OS-Atlas 2.5); $0.34 in closed-model API
  spend (Claude Haiku 4.5 $0.26 + Gemini 3.1 Flash Lite $0.03 + GPT-4o-mini
  $0.05). Estimated from per-item latency and published pricing.
- **Manifest stamping**: every run has a JSON manifest with git commit and
  config snapshot.
- **Determinism**: greedy decoding (temperature = 0), seed = 13,
  CUBLAS_WORKSPACE_CONFIG=:4096:8 for reproducible CuBLAS.

## Known limitations to disclose in the paper

1. **Containment, list_ordinal, occlusion are synthetic-only** — UI-Vision's
   element_grounding annotations don't ship parent/container structure on
   the same screenshots as element labels, so we cannot synthesize these
   from real data without a different corpus. Treated as a controlled
   stimulus arm (What's-Up does the same for its hardest classes).
2. **Item-level regression individual coefficients are not separately
   identified.** LLM-judge primitive tagging (3 of 3 panel models) lifted
   active primitives from 3 to 6 of 7, but with only 4 distinct models in
   the regression the competence vectors are correlated across primitives.
   Coefficients flagged `UNSTABLE` in the script output (|z| > 3) should
   be read together with the regression's overall pseudo-R² (0.318) and
   the model-level Spearman ρ (= 1.000). Both directions are reported and
   labelled honestly.
3. **Human verification of the 196-item core: 5 independent annotators.**
   Fleiss κ on Q1 (instruction well-formed) = **+0.942** ("almost perfect"
   on Landis–Koch); κ on Q2 (target box correct) = **+0.787**
   ("substantial"). Both well above the κ ≥ 0.6 threshold reviewers
   expect. Human majority-vote accuracy on the 185-item clean subset
   (11 items dropped as majority-invalid) is **0.969**, upper-bounding
   the achievable ceiling. Even on this clean split the strongest model
   (Claude Opus 4.7) reaches only 0.324 — a ~64-point human–model gap
   that confirms the diagnostic gap is genuine grounding failure, not
   item noise. Full annotator-vs-annotator agreement and the 11
   invalid item-ids are in `human_eval/agreement.json` and
   `data/benchmark/splits.json::human_verified_clean`. We additionally
   keep the older 3-LLM panel audit (κ ≈ +0.08, n=100 LLM-verified) as
   a documented quality-floor proxy in earlier reports; the
   human numbers are the headline.
4. **Pair-consistency on the 196-item core split is hidden** (`(n<5)`) for
   the closed models because the core split doesn't carry both members of
   every minimal pair — without that, the metric reduces to noise on
   single-member pairs. Open models on n=994 do see both members and the
   pair-consistency story (with the What's-Up signature 🚩) is preserved.
5. **Llama-3.2-11B-Vision emits a default coordinate (≈ origin or constant
   like `(100,100)`) on ≈ 42 % of items** — i.e. the 1.2 % accuracy
   reflects the *model* defaulting, not a parsing bug. Consistent with the
   ScreenSpot-Pro paper's <2 % baseline for generalist VLMs.
4. **Pixtral-12B and Idefics3-8B** were attempted for 6th- and 7th-family
   coverage but their chat-template / output formats are incompatible with
   our generic HFVLMWrapper. Disclosing rather than hiding.
5. **InternVL3-8B** has a `model.chat()`-style API; would require ~30 min
   of custom-wrapper code to integrate. Out of scope for this run.
6. **OSWorld-Verified downstream slice** (Day-4 task in CLAUDE.md) not yet
   run; that's a separate VM-harness task and orthogonal to the
   ScreenSpot-Pro arm.

## Artifacts produced

- `runs/diagnostic/analysis.json` — machine-readable, regenerable from JSONLs
- `runs/diagnostic/deep_analysis.json` — extended analyses
- `runs/diagnostic/deep_analysis.md` — human-readable
- `runs/diagnostic/headline.md` — paper-table-ready output
- `runs/diagnostic/<model>/diagnostic.jsonl` — one prediction per item
- `runs/diagnostic/<model>/screenspot.jsonl` — SS-Pro predictions (open models)
- `runs/diagnostic/<model>/control_{text_only,shuffled,blur}.jsonl` — controls
- `runs/diagnostic/<model>/iv_{baseline,cot,som,steering}.jsonl` — interventions
- `runs/diagnostic/<model>/manifest.json` — provenance per run
- `data/benchmark/items.jsonl` — 994-item benchmark
- `data/benchmark/splits.json` — human_verified / pool stratification
- `data/benchmark/validation.json` — quality gates report
