export CUDA_VISIBLE_DEVICES=0
export MODEL_NAME="/root/AwareCompiler/checkpoints/compiler_autotuning_qwen/grpo-after-sft-Qwen2.5-1.5B-Instruct/global_step_140/actor/huggingface"

vllm serve $MODEL_NAME --enable-auto-tool-choice --tool-call-parser hermes --served-model-name agent --port 8000 --tensor-parallel-size 1