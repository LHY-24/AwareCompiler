# Artifact Structure

- `agent_r1/`: core training, rollout, reward, tool, and vLLM inference modules.
- `scripts/train/`: SFT and RL training entry points for 1.5B, 3B, and 7B models.
- `scripts/infer/`: model merge, vLLM serving, standard inference, and best-of-N inference scripts.
- `scripts/evaluate/`: CSV aggregation scripts for paper tables and baseline checks.
- `baselines/`: optional external-LLM baseline experiments using environment-provided credentials.
- `dataset/`: compact parquet splits used by the training and validation scripts.
- `knowledge_base/`: compiler pass knowledge and compact processed artifacts.
- `results/`: measured CSV outputs used for auditing reported results.
- `examples/data_preprocess/`: active SFT/RL data-construction scripts.
- `archive/`: legacy scripts retained for auditability only.
- `figures/`: paper-level framework figure.
