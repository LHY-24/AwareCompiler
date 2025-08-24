export CHECKPOINT_DIR="/root/AwareCompiler/checkpoints/compiler_autotuning_qwen/grpo-after-sft-Qwen2.5-1.5B-Instruct/global_step_140/actor"

python3 verl/scripts/model_merger.py --local_dir $CHECKPOINT_DIR