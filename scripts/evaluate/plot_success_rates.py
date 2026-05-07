#!/usr/bin/env python3
"""Plot LLM baseline success rates from result CSVs."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BENCHES = ["blas", "cbench", "chstone", "mibench", "npb", "opencv", "tensorflow"]


def model_name(path: Path) -> str:
    return path.name.split("_results_rl_validation_")[0]


def bench_name(path: Path) -> str:
    return path.name.split("_results_rl_validation_")[-1].replace(".csv", "").replace("-v0", "").replace("-v1", "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results/latest_llm"))
    parser.add_argument("--output", type=Path, default=Path("figures/success_latest_llm.png"))
    args = parser.parse_args()

    records = []
    for csv_path in sorted(args.results_dir.glob("*_results_rl_validation_*.csv")):
        df = pd.read_csv(csv_path)
        vals = pd.to_numeric(df["improvement_over_oz"], errors="coerce").fillna(0.0)
        records.append({
            "model": model_name(csv_path),
            "bench": bench_name(csv_path),
            "success_rate": (vals > 0).mean(),
        })
    if not records:
        raise SystemExit(f"No result CSVs found in {args.results_dir}")

    table = pd.DataFrame(records).pivot(index="model", columns="bench", values="success_rate").fillna(0.0)
    table = table[[b for b in BENCHES if b in table.columns]]

    ax = table.T.plot(kind="bar", figsize=(12, 4.8), width=0.82)
    ax.set_ylabel("Success rate")
    ax.set_xlabel("Benchmark suite")
    ax.set_ylim(0, 1.02)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(title="Model", ncol=2, fontsize=8)
    plt.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=300)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
