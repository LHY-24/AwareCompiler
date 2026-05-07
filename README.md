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
pip install FlagEmbedding faiss-cpu pandas pyarrow requests
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
export OPENROUTER_API_KEY=<your-key>
python baselines/iterative_feedback_experiment.py
python baselines/tool_augmented_llm_experiment.py
```

No private API keys, author identifiers, local account paths, or original git history are included in this artifact.
