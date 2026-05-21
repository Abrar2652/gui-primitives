#!/bin/bash
#SBATCH --job-name=guiprim-iv
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:2
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --time=10:00:00
#SBATCH --array=0-1
#SBATCH --output=runs/slurm/iv_%A_%a.out
# ---------------------------------------------------------------------------
# Localization-head identification + interventions for the open models that
# support attention capture. Steering reuses the baseline run automatically.
# ---------------------------------------------------------------------------
set -euo pipefail
module load cuda || true
source activate guiprim

MODELS=(configs/models/qwen2_5_vl_7b.yaml configs/models/internvl3_8b.yaml)
MODEL=${MODELS[$SLURM_ARRAY_TASK_ID]}

echo "heads + interventions for $MODEL"
python scripts/03_identify_heads.py \
    --config configs/experiments/interventions.yaml --model "$MODEL"
python scripts/04_run_interventions.py \
    --config configs/experiments/interventions.yaml --model "$MODEL"
