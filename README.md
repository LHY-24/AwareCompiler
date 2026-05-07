# AwareCompiler

Anonymous NeurIPS artifact for AwareCompiler, a knowledge-grounded agentic framework for LLM-based compiler optimization.

## Repository Layout

- `agent_r1/`: core implementation for agent training, rollout, compiler-tool interaction, reward computation, and vLLM inference.
- `scripts/train/`: SFT and RL training entry points.
- `scripts/infer/`: model merge, vLLM serving, standard inference, and best-of-N inference.
- `scripts/evaluate/`: result aggregation scripts for paper tables and baseline audits.
- `baselines/`: optional external-LLM baseline experiments; API keys are read only from environment variables.
- `dataset/`: compact parquet training and validation splits.
- `knowledge_base/`: compiler-pass knowledge, pass-synergy documentation, and compact processed artifacts.
- `results/`: measured CSV outputs for LLM baselines and AwareCompiler variants.
- `examples/data_preprocess/`: active data-construction scripts.
- `docs/`: artifact structure, reproducibility notes, and anonymization report.
- `archive/`: legacy scripts retained for transparency but not used by the main workflow.

Generated plots, exploratory chart scripts, logs, checkpoints, wandb runs, raw LLVM IR dumps, and local compiler build products are excluded from this review artifact.

## Environment

```bash
conda create -n awarecompiler python=3.10 -y
conda activate awarecompiler
pip install vllm flash-attn --no-build-isolation
pip install FlagEmbedding faiss-cpu pandas pyarrow requests matplotlib
pip install git+https://github.com/volcengine/verl.git
```

The conda environment files `environment.yml` and `aware_compiler_environment.yml` are also included as references.

## Data Construction

```bash
cd examples/data_preprocess
PYTHONPATH=../../ python3 compiler_autotuning_sft.py
PYTHONPATH=../../ python3 compiler_autotuning_rl.py
```

The full raw LLVM IR dump is excluded for size and anonymity reasons. The compact parquet splits under `dataset/` are included for inspecting and reproducing the training/evaluation pipeline.

## Training

Run from the repository root:

```bash
bash scripts/train/train_sft.sh
bash scripts/train/train_rl.sh
```

Model-size-specific variants are available under `scripts/train/`.

## Inference

```bash
bash scripts/infer/infer_model_merge.sh
bash scripts/infer/infer_vllm_serve.sh
bash scripts/infer/infer_run.sh
```

Best-of-N inference:

```bash
bash scripts/infer/infer_run_best_of_n.sh
```

## Evaluation

```bash
python scripts/evaluate/analyze_results_summary.py
python scripts/evaluate/analyze_results_summary_include_nonzero_pass.py
```

## External LLM Baselines

```bash
export AWARECOMPILER_LLM_API_KEY=<your-key>
export AWARECOMPILER_LLM_BASE_URL=https://api.openai.com/v1
export AWARECOMPILER_LLM_MODEL=gpt-5.5
python baselines/iterative_feedback_experiment.py
python baselines/tool_augmented_llm_experiment.py
```


Run the latest vanilla LLM baselines over the seven paper suites:

```bash
export AWARECOMPILER_LLM_API_KEY=<your-key>
export AWARECOMPILER_LLM_BASE_URL=https://api.openai.com/v1
export AWARECOMPILER_LLM_MODELS=GPT-5.5=gpt-5.5,Gemini-3.1-Pro=gemini-3.1-pro,Claude-Opus-4.7=claude-opus-4.7,DeepSeek-V3.2=deepseek-v3.2,GLM-4.5=glm-4.5,Kimi-Dev-72B=kimi-dev-72b,Qwen3-Coder-480B=qwen3-coder-480b
python baselines/run_vanilla_llm_baseline.py --resume
python scripts/evaluate/analyze_results_summary_include_nonzero_pass.py --results-dir results/latest_llm
python scripts/evaluate/plot_success_rates.py --results-dir results/latest_llm --output figures/success_latest_llm.png
```

If the anonymous artifact is used without raw LLVM IR files, set `AWARECOMPILER_LLVM_IR_DIR` to the raw LLVM IR directory before running.

For the representative model-family figure used by the current anonymous paper draft, the repository also includes curated summary files:

```bash
python scripts/evaluate/plot_success_rates.py \
  --summary-csv results/model_bench_success_rate_curated_representative.csv \
  --output figures/success_curated_representative.png
```

The representative model list is recorded in `config/baseline_models.representative.json`. The curated CSVs are for paper-figure reproduction and should be replaced by full API reruns before final release.

No private API keys, author identifiers, local account paths, or original git history are included in this artifact.
