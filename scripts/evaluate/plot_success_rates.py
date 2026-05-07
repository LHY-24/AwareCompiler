#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams.update(
    {
        "font.family": "DejaVu Serif",
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.titleweight": "bold",
        "xtick.color": "#222222",
        "ytick.color": "#222222",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    }
)

BENCHMARK_ORDER = [
    "blas",
    "cbench",
    "chstone",
    "mibench",
    "npb",
    "opencv",
    "tensorflow",
    "average",
]

DISPLAY_NAMES = {
    "blas": "BLAS",
    "cbench": "CBench",
    "chstone": "CHStone",
    "mibench": "MiBench",
    "npb": "NPB",
    "opencv": "OpenCV",
    "tensorflow": "TensorFlow",
    "average": "Average",
}

DEFAULT_MODEL_ORDER = [
    "GPT-5.5",
    "Gemini-3.1-Pro",
    "Claude-Opus-4.7",
    "DeepSeek-V3.2",
    "GLM-4.5",
    "Kimi-Dev-72B",
    "Qwen3-Coder-480B",
    "Hunyuan-A13B",
    "AwareCompiler",
]

MODEL_COLORS = {
    "GPT-5.5": "#4F7FB3",
    "Gemini-3.1-Pro": "#63B7B0",
    "Claude-Opus-4.7": "#9A7BA0",
    "DeepSeek-V3.2": "#D98A3D",
    "GLM-4.5": "#68A95B",
    "Kimi-Dev-72B": "#A7A7A7",
    "Qwen3-Coder-480B": "#6F96B8",
    "AwareCompiler": "#B51E34",
}


def normalize_benchmark(name: str) -> str:
    name = name.lower()
    for suffix in ("-v0", "-v1"):
        name = name.replace(suffix, "")
    return name


def model_from_filename(path: Path) -> str:
    return path.name.split("_results_rl_validation_")[0]


def benchmark_from_filename(path: Path) -> str:
    tail = path.name.split("_results_rl_validation_")[-1]
    return normalize_benchmark(tail.replace(".csv", ""))


def read_summary_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "model" not in df.columns:
        raise ValueError(f"{path} must contain a 'model' column")
    df = df.set_index("model")
    df.columns = [normalize_benchmark(c) for c in df.columns]
    return df


def read_raw_results(results_dir: Path) -> pd.DataFrame:
    records = []
    for csv_path in sorted(results_dir.glob("*_results_rl_validation_*.csv")):
        df = pd.read_csv(csv_path)
        if "improvement_over_oz" not in df.columns:
            continue
        vals = pd.to_numeric(df["improvement_over_oz"], errors="coerce").fillna(0.0)
        records.append(
            {
                "model": model_from_filename(csv_path),
                "benchmark": benchmark_from_filename(csv_path),
                "success_rate": float((vals > 0).mean()),
            }
        )

    if not records:
        raise FileNotFoundError(f"No compatible result CSVs found in {results_dir}")

    table = (
        pd.DataFrame(records)
        .pivot_table(index="model", columns="benchmark", values="success_rate", aggfunc="mean")
        .fillna(0.0)
    )
    available = [b for b in BENCHMARK_ORDER if b != "average" and b in table.columns]
    table["average"] = table[available].mean(axis=1)
    return table


def order_models(df: pd.DataFrame, explicit_order: str | None) -> pd.DataFrame:
    if explicit_order:
        order = [m.strip() for m in explicit_order.split(",") if m.strip()]
    else:
        order = DEFAULT_MODEL_ORDER

    ordered = [m for m in order if m in df.index]
    remaining = [m for m in df.index if m not in ordered]
    remaining = sorted(remaining, key=lambda m: float(df.loc[m].get("average", 0.0)), reverse=True)
    return df.loc[ordered + remaining]


def trim_models(df: pd.DataFrame, max_models: int | None) -> pd.DataFrame:
    if not max_models or len(df) <= max_models:
        return df
    if "AwareCompiler" not in df.index:
        return df.head(max_models)
    keep = [m for m in df.index if m != "AwareCompiler"][: max_models - 1]
    return df.loc[keep + ["AwareCompiler"]]


def color_for_model(model: str, cmap, idx: int, total: int):
    if model in MODEL_COLORS:
        return MODEL_COLORS[model]
    return cmap(idx / max(total - 1, 1))


def plot_success_rates(df: pd.DataFrame, output: Path, title: str | None):
    benchmarks = [b for b in BENCHMARK_ORDER if b in df.columns]
    nrows, ncols = 2, 4
    fig, axes = plt.subplots(nrows, ncols, figsize=(18.2, 8.8), sharey=True)
    axes_flat = axes.flatten()

    cmap = plt.get_cmap("Set2")
    models = list(df.index)
    x = np.arange(len(models))

    for i, benchmark in enumerate(benchmarks):
        ax = axes_flat[i]
        values = df[benchmark].astype(float).to_numpy()
        colors = [color_for_model(m, cmap, j, len(models)) for j, m in enumerate(models)]
        bars = ax.bar(x, values, color=colors, width=0.70, edgecolor="white", linewidth=0.8)

        ax.set_title(DISPLAY_NAMES.get(benchmark, benchmark.title()), fontsize=17, fontweight="bold")
        ax.set_ylim(0, 1.08)
        ax.grid(axis="y", alpha=0.20, linewidth=0.7, color="#7f7f7f")
        ax.set_axisbelow(True)
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=36, ha="right", fontsize=11)
        ax.tick_params(axis="y", labelsize=12, length=3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        if i % ncols == 0:
            ax.set_ylabel("Success rate", fontsize=14)

        for tick in ax.get_xticklabels():
            if tick.get_text() == "AwareCompiler":
                tick.set_fontweight("bold")
                tick.set_color(MODEL_COLORS["AwareCompiler"])

        for bar, model, value in zip(bars, models, values):
            if value >= 0.995:
                label = "1.00"
            else:
                label = f"{value:.2f}"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                min(value + 0.018, 1.035),
                label,
                ha="center",
                va="bottom",
                fontsize=10.5,
                fontweight="bold" if model == "AwareCompiler" else "normal",
                color="#333333",
            )

        if "AwareCompiler" in models:
            aware_value = float(df.loc["AwareCompiler", benchmark])
            baseline_values = [float(df.loc[m, benchmark]) for m in models if m != "AwareCompiler"]
            if baseline_values:
                gain = aware_value - max(baseline_values)
                if gain > 1e-9:
                    aware_idx = models.index("AwareCompiler")
                    ax.annotate(
                        f"+{gain:.2f}",
                        xy=(aware_idx, min(aware_value + 0.015, 1.0)),
                        xytext=(0, -16),
                        textcoords="offset points",
                        ha="center",
                        va="top",
                        fontsize=10.5,
                        fontweight="bold",
                        color="white",
                        bbox=dict(boxstyle="round,pad=0.22", fc=MODEL_COLORS["AwareCompiler"], ec="none", alpha=0.95),
                    )

    for ax in axes_flat[len(benchmarks) :]:
        ax.axis("off")

    if title:
        fig.suptitle(title, fontsize=15, fontweight="bold", y=0.995)

    plt.tight_layout(rect=(0, 0, 1, 0.975 if title else 1))
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300, bbox_inches="tight")
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved {output}")
    print(f"Saved {output.with_suffix('.pdf')}")


def main():
    parser = argparse.ArgumentParser(description="Plot per-benchmark valid-sequence success rates.")
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=Path("results/model_bench_success_rate_curated_representative.csv"),
        help="Pre-aggregated success-rate CSV with a 'model' column.",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=None,
        help="Optional directory of raw '*_results_rl_validation_*.csv' files. Overrides --summary-csv.",
    )
    parser.add_argument("--output", type=Path, default=Path("figures/success_curated_representative.png"))
    parser.add_argument("--model-order", type=str, default=None)
    parser.add_argument("--max-models", type=int, default=None)
    parser.add_argument("--title", type=str, default=None)
    args = parser.parse_args()

    if args.results_dir:
        df = read_raw_results(args.results_dir)
    else:
        df = read_summary_csv(args.summary_csv)

    columns = [b for b in BENCHMARK_ORDER if b in df.columns]
    df = df[columns]
    df = order_models(df, args.model_order)
    df = trim_models(df, args.max_models)
    plot_success_rates(df, args.output, args.title)


if __name__ == "__main__":
    main()
