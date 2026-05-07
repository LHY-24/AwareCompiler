# Anonymous Release Report

This artifact branch was prepared for double-anonymous NeurIPS review.

## Included

- Core implementation under `agent_r1/`
- Data construction scripts under `examples/data_preprocess/`
- Compact SFT/RL parquet splits under `dataset/`
- Knowledge-base documentation and compact processed artifacts under `knowledge_base/`
- Evaluation CSVs and plotting scripts under `results/`
- Training, inference, and aggregation entry scripts

## Removed or Excluded

- Original git history and remotes
- Author/account-specific metadata
- Hard-coded API credentials
- wandb runs and logs
- Model checkpoints and merged weights
- Raw LLVM IR dump and local compiler build outputs
- Generated KG cache file `knowledge_base/compiler_kg/autophase_features_kg.json`

## Sanitization Checks

The release was scanned for API-key patterns, original GitHub owner strings, SSH host configuration, and local absolute paths. External LLM scripts now read credentials from `OPENROUTER_API_KEY` instead of embedding a key.

## Known Notes

The raw LLVM IR corpus and trained checkpoints are intentionally not stored in this anonymous Git branch because of size and double-anonymous metadata risks. The compact parquet splits and measured CSV outputs needed to inspect the paper experiments are included.
