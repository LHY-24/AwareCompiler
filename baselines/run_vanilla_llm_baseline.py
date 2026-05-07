#!/usr/bin/env python3
"""Run vanilla OpenAI-compatible LLM baselines for compiler pass generation.

The output format matches the paper's existing result CSVs:
`program_id,pass_sequence,improvement_over_oz`.
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd

from llm_client import chat_completion, get_llm_config

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_DIR = Path(os.environ.get("AWARECOMPILER_DATASET_DIR", REPO_ROOT / "dataset" / "rl"))
DEFAULT_LLVM_IR_DIR = Path(
    os.environ.get("AWARECOMPILER_LLVM_IR_DIR", REPO_ROOT / "examples" / "data_preprocess" / "llvmir_datasets")
)
DEFAULT_LLVM_TOOLS_PATH = Path(
    os.environ.get("AWARECOMPILER_LLVM_TOOLS_PATH", REPO_ROOT / "agent_r1" / "tool" / "tools" / "comiler_autotuning" / "raw_tool")
)
DEFAULT_RESULTS_DIR = REPO_ROOT / "results" / "latest_llm"
DEFAULT_DATASETS = [
    "rl_validation_blas-v0.parquet",
    "rl_validation_cbench-v1.parquet",
    "rl_validation_chstone-v0.parquet",
    "rl_validation_mibench-v1.parquet",
    "rl_validation_npb-v0.parquet",
    "rl_validation_opencv-v0.parquet",
    "rl_validation_tensorflow-v0.parquet",
]

sys.path.insert(0, str(REPO_ROOT))
from agent_r1.tool.tools.comiler_autotuning.raw_tool.get_instrcount import get_overOz as _raw_get_overOz


def parse_models(spec: str) -> List[Tuple[str, str]]:
    """Parse 'Label=model-id,Other=provider/model' or plain model ids."""
    if not spec:
        cfg = get_llm_config()
        return [(sanitize_model_label(cfg["model"]), cfg["model"])]
    out = []
    for item in spec.split(","):
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            label, model_id = item.split("=", 1)
        else:
            label, model_id = item, item
        out.append((sanitize_model_label(label.strip()), model_id.strip()))
    return out


def sanitize_model_label(label: str) -> str:
    label = label.replace("/", "-").replace(":", "-")
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", label).strip("-")


def parse_pass_sequence(answer: str) -> List[str]:
    if not answer:
        return []
    answer = re.sub(r"```(?:json)?", "", answer).replace("```", "")
    # Prefer the last JSON-like list in the response.
    for match in reversed(list(re.finditer(r"\[([^\[\]]*)\]", answer, re.DOTALL))):
        try:
            candidate = json.loads(f"[{match.group(1)}]")
        except Exception:
            continue
        if isinstance(candidate, list) and all(isinstance(p, str) for p in candidate):
            passes, seen = [], set()
            for p in candidate:
                p = p.strip()
                if not p:
                    continue
                if not p.startswith("--"):
                    p = "--" + p.lstrip("-")
                if p not in seen:
                    passes.append(p)
                    seen.add(p)
            return passes
    return []


def build_prompt(features: Dict, initial_count: object = None) -> List[Dict[str, str]]:
    payload = {"autophase_features": features}
    if initial_count is not None:
        payload["initial_instruction_count"] = initial_count
    return [
        {
            "role": "system",
            "content": (
                "You are a compiler optimization expert. Generate an LLVM optimization pass sequence "
                "that minimizes instruction count. Use only LLVM pass names from the task vocabulary. "
                "Return only a JSON list of pass strings, with no markdown or explanation."
            ),
        },
        {
            "role": "user",
            "content": (
                "Given the following program features, recommend one optimization pass sequence.\n"
                f"{json.dumps(payload, indent=2)}\n"
                "Output example: [\"--mem2reg\", \"--sroa\", \"--instcombine\", \"--simplifycfg\"]"
            ),
        },
    ]


def call_model(messages: List[Dict[str, str]], retries: int, retry_delay: float) -> str:
    for attempt in range(retries):
        try:
            completion = chat_completion(messages, max_tokens=4096, temperature=0.7)
            return completion.choices[0].message.content or ""
        except Exception as exc:
            print(f"    API request failed ({attempt + 1}/{retries}): {exc}")
            time.sleep(retry_delay * (attempt + 1))
    return ""


def extract_features(row) -> Tuple[Dict, object]:
    question = row.get("question", "")
    match = re.search(r"```json\n(.*?)\n```", question, re.DOTALL)
    features = json.loads(match.group(1)) if match else {}
    initial_count = row.get("initial_instruction_count", None)
    return features, initial_count


def evaluate(ll_code: str, passes: List[str], tools_path: Path) -> float:
    if not passes:
        return 0.0
    try:
        score = _raw_get_overOz(ll_code, passes, llvm_tools_path=str(tools_path))
        return float(score) if score is not None else 0.0
    except subprocess.CalledProcessError:
        return 0.0
    except Exception as exc:
        print(f"    Evaluation failed: {exc}")
        return 0.0


def run(args):
    datasets = [d.strip() for d in args.datasets.split(",") if d.strip()] if args.datasets else DEFAULT_DATASETS
    models = parse_models(args.models)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for dataset_file in datasets:
        parquet_path = args.dataset_dir / dataset_file
        bench = dataset_file.replace("rl_validation_", "").replace(".parquet", "")
        print(f"\n{'=' * 72}\nBenchmark: {bench}\n{'=' * 72}")
        df = pd.read_parquet(parquet_path)
        if args.max_programs:
            df = df.head(args.max_programs)

        rows = []
        for _, row in df.iterrows():
            program_id = row.get("ground_truth", "")
            if not program_id:
                continue
            ll_path = args.llvm_ir_dir / program_id
            if not ll_path.exists():
                print(f"  Skip {program_id}: missing LLVM IR at {ll_path}")
                continue
            features, initial_count = extract_features(row)
            rows.append((program_id, ll_path.read_text(), features, initial_count))

        print(f"  Programs: {len(rows)}")
        for label, model_id in models:
            print(f"\n  --- Model: {label} ({model_id}) ---")
            output_path = args.output_dir / f"{label}_results_{dataset_file.replace('.parquet', '.csv')}"
            existing = {}
            if output_path.exists() and args.resume:
                old = pd.read_csv(output_path)
                existing = {r["program_id"]: r for _, r in old.iterrows()}
            records = [] if not existing else [dict(v) for v in existing.values()]

            for i, (program_id, ll_code, features, initial_count) in enumerate(rows, 1):
                if program_id in existing and args.resume:
                    print(f"  [{i}/{len(rows)}] {program_id}: cached")
                    continue
                print(f"  [{i}/{len(rows)}] {program_id}")
                messages = build_prompt(features, initial_count)
                answer = call_model(messages, args.retries, args.retry_delay)
                passes = parse_pass_sequence(answer)
                overoz = evaluate(ll_code, passes, args.llvm_tools_path)
                records.append({
                    "program_id": program_id,
                    "pass_sequence": json.dumps(passes),
                    "improvement_over_oz": overoz,
                    "raw_answer": answer if args.keep_raw_answer else "",
                })
                if i % args.save_every == 0:
                    write_csv(output_path, records, args.keep_raw_answer)
            write_csv(output_path, records, args.keep_raw_answer)
            print(f"  Saved: {output_path}")


def write_csv(path: Path, records: List[Dict], keep_raw_answer: bool):
    fields = ["program_id", "pass_sequence", "improvement_over_oz"]
    if keep_raw_answer:
        fields.append("raw_answer")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in records:
            writer.writerow({k: r.get(k, "") for k in fields})


def main():
    parser = argparse.ArgumentParser(description="Run vanilla latest-LLM compiler baselines")
    parser.add_argument("--models", default=os.environ.get("AWARECOMPILER_LLM_MODELS", ""),
                        help="Comma-separated labels/model ids, e.g. GPT-5.5=gpt-5.5,Claude=anthropic/claude-opus-4.7")
    parser.add_argument("--datasets", default="", help="Comma-separated parquet filenames; defaults to seven paper suites")
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    parser.add_argument("--llvm-ir-dir", type=Path, default=DEFAULT_LLVM_IR_DIR)
    parser.add_argument("--llvm-tools-path", type=Path, default=DEFAULT_LLVM_TOOLS_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--max-programs", type=int, default=None)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--save-every", type=int, default=3)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--keep-raw-answer", action="store_true")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
