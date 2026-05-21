# GUI-Primitives — common workflows. Run `make help` for the list.
PY ?= python
RUN ?= runs/diagnostic

.PHONY: help install smoke benchmark diagnostic heads interventions screenspot analyze figures test clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-14s %s\n",$$1,$$2}'

install: ## Install the package and dependencies
	$(PY) -m pip install -r requirements.txt && $(PY) -m pip install -e .

smoke: ## End-to-end dry run on synthetic UIs (no downloads, no GPU)
	$(PY) scripts/00_setup_check.py
	$(PY) scripts/01_build_benchmark.py --config configs/experiments/diagnostic.yaml --synthetic --n 60
	$(PY) scripts/02_run_diagnostic.py --config configs/experiments/diagnostic.yaml --model configs/models/dummy.yaml --smoke
	$(PY) scripts/06_analyze.py --run runs/diagnostic --smoke
	@echo "SMOKE OK — pipeline wiring verified."

benchmark: ## Build the GUI-Primitives benchmark from a real UI corpus
	$(PY) scripts/01_build_benchmark.py --config configs/experiments/diagnostic.yaml

diagnostic: ## Run per-primitive diagnostic for one model (set MODEL=...)
	$(PY) scripts/02_run_diagnostic.py --config configs/experiments/diagnostic.yaml --model $(MODEL)

heads: ## Identify localization heads for one model (set MODEL=...)
	$(PY) scripts/03_identify_heads.py --config configs/experiments/interventions.yaml --model $(MODEL)

interventions: ## Run SoM / CoT / steering interventions (set MODEL=...)
	$(PY) scripts/04_run_interventions.py --config configs/experiments/interventions.yaml --model $(MODEL)

screenspot: ## Run grounding eval on ScreenSpot-Pro (set MODEL=...)
	$(PY) scripts/05_run_screenspot.py --config configs/experiments/interventions.yaml --model $(MODEL)

analyze: ## Aggregate stats, run the primitive->grounding regression
	$(PY) scripts/06_analyze.py --run $(RUN)

figures: ## Render all camera-ready paper figures (PDF+PNG) from an analyzed run (set RUN=...)
	$(PY) scripts/07_make_figures.py --run $(RUN)

test: ## Run the unit test suite
	$(PY) -m pytest

clean: ## Remove caches and dev runs
	find . -name __pycache__ -type d -exec rm -rf {} + ; rm -rf runs data/benchmark/synthetic
