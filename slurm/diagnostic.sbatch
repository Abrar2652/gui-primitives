#!/bin/bash
#SBATCH --job-name=guiprim-diag
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --array=0-3
#SBATCH --output=runs/slurm/diag_%A_%a.out
# ---------------------------------------------------------------------------
# Per-model diagnostic as a job array. One array index = one open model.
# 72B models need a multi-GPU node: see slurm/interventions.sbatch for the
# --gres pattern, or launch the 72B config separately with gpu:a100:4.
# ---------------------------------------------------------------------------
set -euo pipefail
module load cuda || true
source activate guiprim

MODELS=(configs/models/qwen2_5_vl_7b.yaml \
        configs/models/internvl3_8b.yaml \
        configs/models/llama32_11b_vision.yaml \
        configs/models/qwen2_5_vl_72b.yaml)
MODEL=${MODELS[$SLURM_ARRAY_TASK_ID]}

echo "diagnostic for $MODEL"
python scripts/02_run_diagnostic.py \
    --config configs/experiments/diagnostic.yaml --model "$MODEL"
python scripts/05_run_screenspot.py \
    --config configs/experiments/diagnostic.yaml --model "$MODEL"
