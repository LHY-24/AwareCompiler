#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$REPO_ROOT"
export CUDA_VISIBLE_DEVICES=0
# export MODEL_NAME="$REPO_ROOT/checkpoints/compiler_autotuning_qwen/grpo-after-sft-Qwen2.5-1.5B-Instruct/global_step_145/actor/huggingface"
# export MODEL_NAME="$REPO_ROOT/model_save/cold_start_model/3B/global_step_248"
export MODEL_NAME="$REPO_ROOT/checkpoints/compiler_autotuning_qwen/grpo-after-sft-Qwen2.5-3B-Instruct/global_step_45/actor/huggingface"

vllm serve $MODEL_NAME --enable-auto-tool-choice --tool-call-parser hermes --served-model-name agent --port 8000 --tensor-parallel-size 1
