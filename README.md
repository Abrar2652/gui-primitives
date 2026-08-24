# GUI-Primitives: Reproducibility Package

This release contains everything needed to reproduce the headline results of our paper **"GUI-Primitives: Diagnosing Spatial Reasoning Failures in Vision-Language GUI Grounding."**

## What this package contains

```
gui-primitives/
├── src/guiprim/          # Library code (pure Python core; torch only for
│                         #   open-weight inference)
├── scripts/              # 0X_*.py — the staged pipeline (build → run →
│                         #   intervene → analyze → figures)
├── configs/              # YAML configs; one model file per model evaluated
├── tests/                # pytest unit tests for parsing/metrics/stats
├── slurm/                # Optional cluster submission scripts
├── data/
│   ├── benchmark/
│   │   ├── items.jsonl       # 994-item GUI-Primitives benchmark
│   │   ├── splits.json       # human_verified (196) + human_verified_clean (185)
│   │   ├── validation.json   # benchmark quality-gate output
│   │   └── core_kappa.json   # LLM-judge panel agreement (proxy)
│   └── schema/               # JSON schemas for items / corpora
├── human_eval/
│   ├── annotate.py / compute_agreement.py / render_for_annotation.py
│   ├── agreement.json        # Fleiss κ + n=185 clean accuracy
│   └── annotations/ann{1-5}.jsonl   # 5 anonymized annotator label files
├── runs/diagnostic/
│   ├── analysis.json         # main statistical output
│   ├── deep_analysis.{json,md}      # per-app + Cohen's h + stratified ρ
│   ├── extras_analysis.{json,md}    # bootstrap CIs + loose-acc sweep
│   ├── headline.md / FINAL_SUMMARY.md   # human-readable summaries
│   └── figs/                 # PDF + 300dpi PNG paper figures
├── Makefile / pyproject.toml / requirements.txt / environment.yml
└── README.md (this file)     # README_dev.md is the original dev-facing brief
```

## What is NOT in this package

- **Screenshot images.** UI-Vision and ScreenSpot-Pro images are downloaded
  from their respective HuggingFace mirrors at run time
  (see *Downloading data* below).
- **Per-model prediction JSONLs** (`diagnostic.jsonl`, `iv_*.jsonl`,
  `screenspot.jsonl` per model). Those are several hundred MB total and
  regenerate deterministically — see `scripts/02_run_diagnostic.py`,
  `scripts/04_run_interventions.py`, `scripts/05_run_screenspot.py`.
- **API keys.** Set them in your shell or in a local `.env` file.

## Quick-start: smoke test

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make smoke    # synthetic UIs + dummy model; verifies the pipeline wiring
```

`make smoke` is offline and GPU-free. If this passes, the harness is sound.

## Full reproduction

```bash
# 1. Download the source corpora (UI-Vision + ScreenSpot-Pro)
python scripts/00_setup_check.py                       # env + GPU check
python scripts/convert_ui_vision.py                    # → ui_corpus.jsonl
# (set SCREENSPOT_PRO_PATH or symlink into data/screenspot_pro/)

# 2. Build the benchmark (994 minimal-pair items across 7 primitives)
python scripts/01_build_benchmark.py \
    --config configs/experiments/diagnostic.yaml

# 3. Run the diagnostic + ScreenSpot-Pro for each model
#    (open models = ~12 GPU-hours on A6000; closed models = ~$30 API budget)
python scripts/02_run_diagnostic.py  --config configs/experiments/diagnostic.yaml \
    --model configs/models/qwen2_5_vl_7b.yaml          # … repeat per model
python scripts/05_run_screenspot.py  --config configs/experiments/diagnostic.yaml \
    --model configs/models/qwen2_5_vl_7b.yaml

# 4. Interventions (SoM, CoT, activation steering)
python scripts/04_run_interventions.py \
    --config configs/experiments/interventions.yaml \
    --model configs/models/qwen2_5_vl_7b.yaml

# 5. Shortcut controls
python scripts/02b_run_controls.py \
    --config configs/experiments/diagnostic.yaml \
    --model configs/models/qwen2_5_vl_7b.yaml

# 6. Aggregate analyses + camera-ready figures
python scripts/06_analyze.py        --run runs/diagnostic
python scripts/09_deep_analysis.py  --run runs/diagnostic
python scripts/12_extras_analysis.py --run runs/diagnostic
python scripts/08_headline_summary.py --run runs/diagnostic --md
python scripts/07_make_figures.py   --run runs/diagnostic
```

## Headline numbers (verified outputs in this package)

| Quantity | Value |
|---|---|
| n models with both GUI-Primitives + SS-Pro | 10 |
| Spearman ρ (model-level, all items) | +0.736 (p=0.015) |
| Spearman ρ (real-screenshot UI-Vision only) | +0.705 (p=0.023) |
| Item-level pseudo-R² (n=15,810) | 0.404 |
| Fleiss κ inter-annotator (5 annotators) | 0.942 (validity), 0.787 (target) |
| Human accuracy on n=185 clean core | 0.969 |
| Best-model accuracy on n=185 clean core | 0.324 (Opus 4.7) |
| Set-of-Mark Δaccuracy (Qwen2.5-VL, n=994) | +0.351 (p<10⁻⁵⁰, Holm) |
| Set-of-Mark Δaccuracy (OS-Atlas, n=994) | +0.421 (p<10⁻⁵⁰, Holm) |
| Set-of-Mark Δaccuracy (GPT-5, n=196 core) | +0.571 (p<10⁻⁵⁰, Holm) |
| Set-of-Mark Δaccuracy (Opus 4.7, n=196 core) | +0.092 (p=0.080) |

All numbers reproducible from `runs/diagnostic/analysis.json` and
`runs/diagnostic/extras_analysis.json` via the scripts above.

## Reproducibility guarantees

- **Determinism.** Every script calls `set_global_seed(13)`. Generation is
  greedy (`temperature: 0.0`). Stochastic resampling (bootstrap CIs) uses
  fixed seeds (see `src/guiprim/eval/stats.py`).
- **Provenance.** Each run directory carries a `manifest.json` with the
  effective config + Git commit at run time.
- **Resumable runs.** `run_model_on_items` appends one JSONL record per item
  and skips items already present, so SLURM pre-emption is safe.

## Models we evaluated (19 total)

Open-weight (HuggingFace): Qwen2.5-VL-7B, Qwen2-VL-7B, OS-Atlas-Base-7B,
InternVL3-8B, Llama-3.2-11B-Vision, Gemma 3-{4B,12B,27B}-it, PaliGemma 2-{3B,10B}.
Local Ollama: gemma3:27b-q4, MiniCPM-V 2.6. Closed APIs: Claude
{Opus 4.7, Sonnet 4.6, Haiku 4.5}, GPT-{5, 4.1, 4o-mini}, Gemini 3.1 Flash Lite.
Coordinate-space and prompt-format conventions per model are in
`configs/models/*.yaml`.


## License

MIT (see `LICENSE`). Benchmark items derived from UI-Vision and ScreenSpot-Pro
inherit those projects' licenses; please consult their respective repos.




