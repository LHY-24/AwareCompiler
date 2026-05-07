# Reproducibility Checklist

This anonymous artifact is organized for NeurIPS-style review.

- Anonymity: no git history, no original remote, no author names, no API keys, and no local account paths are included.
- Scope: training, inference, analysis, compact datasets, knowledge documents, and result CSVs are included.
- Excluded artifacts: raw LLVM IR dump, model checkpoints, wandb logs, generated cache files, and local build products.
- Baseline fairness: external LLM calls use explicit decoding and retry budgets in the scripts; API credentials are provided only through environment variables. The current representative model-family set is `GPT-5.5`, `Gemini-3.1-Pro`, `Claude-Opus-4.7`, `DeepSeek-V3.2`, `GLM-4.5`, `Kimi-Dev-72B`, and `Qwen3-Coder-480B`.
- Statistical testing: paper tables should be interpreted with paired benchmark-level tests and bootstrap confidence intervals over the seven benchmark suites. Curated representative CSVs under `results/model_bench_*_curated_representative.csv` reproduce the anonymous draft figures/tables and should be refreshed after full API reruns.

Before public release after acceptance, replace this anonymous README with a full non-anonymous artifact description, add permanent model/data links, and restore normal citation metadata.
