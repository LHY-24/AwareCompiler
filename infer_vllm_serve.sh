export CUDA_VISIBLE_DEVICES=0
export MODEL_NAME="/root/project/Compiler-R1/checkpoints/compiler_autotuning_qwen/grpo-after-sft-Qwen2.5-1.5B-Instruct/global_step_50/actor/huggingface"

vllm serve $MODEL_NAME --enable-auto-tool-choice --tool-call-parser hermes --served-model-name agent --port 8001 --tensor-parallel-size 1