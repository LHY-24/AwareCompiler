#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$REPO_ROOT"
# export CHECKPOINT_DIR="$REPO_ROOT/checkpoints/compiler_autotuning_qwen/grpo-after-sft-Qwen2.5-1.5B-Instruct/global_step_145/actor"
# export CHECKPOINT_DIR="$REPO_ROOT/model_save/cold_start_model/1.5B/global_step_248"
export CHECKPOINT_DIR="$REPO_ROOT/checkpoints/compiler_autotuning_qwen/grpo-after-sft-Qwen2.5-3B-Instruct/global_step_45/actor"

python3 verl/scripts/model_merger.py --local_dir $CHECKPOINT_DIR
