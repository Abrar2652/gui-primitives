# GUI-Primitives

**Diagnosing spatial-primitive failures in VLM computer-use agents — and fixing
them without training.**

This repository accompanies an EMNLP submission. It contains (1) a controlled
minimal-pair diagnostic benchmark for elementary GUI spatial primitives, (2) a
multi-model failure analysis whose headline result links per-primitive
competence to GUI-grounding success on ScreenSpot-Pro, and (3) three
training-free interventions that recover measurable accuracy.

## The idea in one paragraph

VLM-based computer-use agents fail on OSWorld largely because of *grounding* —
mapping a language instruction to a click coordinate. Existing spatial-reasoning
benchmarks (What's-Up, BLINK, CV-Bench, VSR) use natural photos, not screenshots,
and no published work isolates *which* elementary spatial primitives drive GUI
click errors. We build **GUI-Primitives**: ~1,000 minimal-pair items over seven
primitives (horizontal/vertical relative position, containment, list ordinal,
alignment, proximity, occlusion). Each pair shares a screenshot and an anchor and
flips only the relation word, so above-chance accuracy cannot come from a prior.
We profile six-plus open-weight VLMs, show that per-primitive competence
**predicts** per-item ScreenSpot-Pro success in a logistic regression with model
fixed effects and item-clustered errors, and test Set-of-Mark prompting,
primitive-aware chain-of-thought, and activation steering as weight-free fixes.

## Install

```bash
conda env create -f environment.yml && conda activate guiprim   # or: pip install -r requirements.txt
pip install -e .
```

The pure-Python parts (benchmark synthesis, evaluation, statistics, plotting)
need only the scientific stack. `torch`/`transformers` are needed only to run
models on the cluster.

## Quickstart: prove the pipeline works (no GPU, no downloads)

```bash
make smoke
```

This renders a synthetic UI corpus, builds a 60-item benchmark, runs the
deterministic dummy model end to end, and writes an analysis — verifying every
stage is wired before any cluster time is spent.

## Real run (cluster)

```bash
# 1. obtain data — see data/README.md, then:
make benchmark                                       # build GUI-Primitives
sbatch slurm/diagnostic.sbatch                       # per-model diagnostic + ScreenSpot-Pro
sbatch slurm/interventions.sbatch                    # localization heads + interventions
python scripts/06_analyze.py --run runs/diagnostic   # stats + regression
python scripts/07_make_figures.py --run runs/diagnostic
```

## Repository layout

```
configs/        experiment + per-model YAML (inheritance via `inherit:`)
src/guiprim/
  benchmark/    primitive defs, minimal-pair synthesis, synthetic renderer, validation
  models/       VLM wrappers (HF open models, closed API, dummy) behind one interface
  inference/    coordinate parsing, resumable run loop
  eval/         point-in-box metrics, bootstrap/McNemar/Holm stats, the regression
  interventions/ Set-of-Mark, primitive-aware CoT, localization heads, steering
  controls/     shortcut probes (text-only, shuffled, blur, position-shift)
  viz/          paper figures
scripts/        00-07, the staged pipeline
human_eval/     annotation harness + inter-annotator agreement
tests/          unit tests for parsing, metrics, stats, synthesis
slurm/          CKG cluster job scripts
```

## Reviewer-proofing built into the code

Minimal-pair benchmark design; a `pair_consistency` metric that exposes
answer-priors; four shortcut controls; bootstrap CIs, paired McNemar tests and
Holm correction across the seven primitives; item-clustered SEs in the
regression; a human baseline with inter-annotator kappa; full run provenance
(git commit + config snapshot) in every `runs/<...>/manifest.json`.

## Handoff

`CLAUDE.md` is the working context for continuing this project with Claude Code
on the cluster — read it first.
