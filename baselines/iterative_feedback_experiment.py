#!/usr/bin/env python3
"""
Iterative Feedback Experiment for ICML Rebuttal (Q4)
=====================================================
Tests how LLM baseline performance changes with iterative compiler feedback.

Each round:
  1. LLM generates pass sequence
  2. Compile with LLVM opt and measure instrcount
  3. Feed back the result (success/failure + improvement) to LLM
  4. LLM refines the sequence

Records per-round OverOz and success rate across programs.
"""

import os
import sys
import json
import csv
import time
import re
import subprocess
import ctypes
import io
import argparse
import pandas as pd
from pathlib import Path
import requests
from llm_client import chat_completion, get_llm_config

# ============================================================
# Configuration
# ============================================================
# OpenAI-compatible endpoint. Configure with:
# AWARECOMPILER_LLM_API_KEY / OPENAI_API_KEY
# AWARECOMPILER_LLM_BASE_URL / OPENAI_BASE_URL
# AWARECOMPILER_LLM_MODEL (default: gpt-5.5)

REPO_ROOT = Path(__file__).resolve().parents[1]
LLVM_IR_DIR = str(REPO_ROOT / "examples/data_preprocess/llvmir_datasets")
LLVM_TOOLS_PATH = str(REPO_ROOT / "awarecompiler/tool/tools/compiler_autotuning/raw_tool")
DATASET_DIR = str(REPO_ROOT / "dataset/rl")

# By default, evaluate the configured OpenAI-compatible model.
# Override with AWARECOMPILER_LLM_MODEL, e.g. gpt-5.5.
_llm_cfg = get_llm_config()
MODELS = [(_llm_cfg["model"], _llm_cfg["model"])]

# Benchmarks to test (use CBENCH for efficiency, expand if needed)
DATASETS = [
    "rl_validation_cbench-v1.parquet",
]

MAX_ROUNDS = 5  # Number of feedback rounds
RETRY_DELAY = 2  # Seconds between API calls

# ============================================================
# LLVM Tools
# ============================================================
# Reuse the project's proven instrcount implementation
sys.path.insert(0, str(REPO_ROOT))
from awarecompiler.tool.tools.compiler_autotuning.raw_tool.get_instrcount import (
    get_instrcount as _raw_get_instrcount, get_overOz as _raw_get_overOz
)


def get_overoz(ll_code, opt_flags):
    """Calculate OverOz using the project's original implementation."""
    try:
        overoz = _raw_get_overOz(ll_code, opt_flags, llvm_tools_path=LLVM_TOOLS_PATH)
        if overoz is None:
            return None, False, "Failed to compute OverOz"
        return overoz, True, ""
    except subprocess.CalledProcessError as e:
        return None, False, str(e.stderr)[:500] if e.stderr else str(e)[:500]
    except Exception as e:
        return None, False, str(e)[:500]


# ============================================================
# LLM API
# ============================================================
def call_llm(messages, model_id):
    """Call an OpenAI-compatible Chat Completions endpoint."""
    for attempt in range(3):
        try:
            completion = chat_completion(messages, max_tokens=2048, temperature=0.7)
            return completion.choices[0].message.content
        except Exception as e:
            print(f"    Request failed (attempt {attempt+1}) for {model_id}: {e}")
            time.sleep(RETRY_DELAY * (attempt + 1))
    return None


def parse_pass_sequence(answer):
    """Extract pass sequence from LLM response."""
    if answer is None:
        return []

    # Try to find JSON list in the response
    patterns = [
        r'\[([^\[\]]*)\]',  # [...] pattern
    ]
    for pattern in patterns:
        matches = re.findall(pattern, answer, re.DOTALL)
        for match in reversed(matches):  # try last match first
            try:
                candidate = json.loads(f"[{match}]")
                if isinstance(candidate, list) and all(isinstance(p, str) for p in candidate):
                    # Format passes
                    formatted = []
                    seen = set()
                    for p in candidate:
                        p = p.strip()
                        if not p.startswith("--"):
                            p = "--" + p
                        if p not in seen:
                            formatted.append(p)
                            seen.add(p)
                    if formatted:
                        return formatted
            except:
                continue
    return []


# ============================================================
# Experiment Logic
# ============================================================
def build_initial_prompt(features):
    """Build the initial prompt (Round 0, no feedback)."""
    return (
        "You are a compiler optimization expert. Given the following LLVM IR autophase features:\n"
        f"{json.dumps(features, indent=2)}\n"
        "Your task: Recommend an LLVM pass sequence to minimize instruction count.\n"
        "Output ONLY a JSON list of optimization passes, each starting with '--', e.g.:\n"
        '[  "--mem2reg", "--sroa", "--instcombine", "--simplifycfg"]\n'
        "Do not include any explanation, comments, or text outside the JSON list."
    )


def build_feedback_prompt(features, prev_passes, success, overoz, error_msg, round_num):
    """Build feedback prompt for subsequent rounds."""
    if success:
        if overoz > 0:
            feedback = (
                f"Your previous pass sequence {json.dumps(prev_passes)} compiled successfully "
                f"and achieved an improvement of {overoz:.4f} over the -Oz baseline. "
                f"Can you find a better sequence that achieves even higher improvement? "
                f"Try different or additional passes."
            )
        else:
            feedback = (
                f"Your previous pass sequence {json.dumps(prev_passes)} compiled successfully "
                f"but did NOT improve over the -Oz baseline (OverOz = {overoz:.4f}). "
                f"Please try a different strategy with different passes to beat -Oz."
            )
    else:
        feedback = (
            f"Your previous pass sequence {json.dumps(prev_passes)} FAILED to compile. "
            f"Error: {error_msg[:300]}\n"
            f"Please fix the sequence by removing problematic passes or trying a different approach."
        )

    return (
        "You are a compiler optimization expert. Given the following LLVM IR autophase features:\n"
        f"{json.dumps(features, indent=2)}\n\n"
        f"[Feedback from Round {round_num}] {feedback}\n\n"
        "Output ONLY an improved JSON list of optimization passes, each starting with '--'.\n"
        "Do not include any explanation, comments, or text outside the JSON list."
    )


def run_experiment_for_program(features, ll_code, model_id, model_name, program_id):
    """Run multi-round feedback experiment for a single program."""
    results = []

    messages = []
    prev_passes = []

    for round_num in range(MAX_ROUNDS):
        # Build prompt
        if round_num == 0:
            prompt = build_initial_prompt(features)
        else:
            prompt = build_feedback_prompt(
                features, prev_passes, prev_success, prev_overoz, prev_error, round_num
            )

        messages = [{"role": "user", "content": prompt}]

        # Call LLM
        answer = call_llm(messages, model_id)
        passes = parse_pass_sequence(answer)

        # Evaluate
        if passes:
            overoz, success, error_msg = get_overoz(ll_code, passes)
            if overoz is None:
                overoz = 0.0
                success = False
        else:
            overoz = 0.0
            success = False
            error_msg = "Empty pass sequence generated"

        results.append({
            "round": round_num,
            "program_id": program_id,
            "model": model_name,
            "pass_sequence": json.dumps(passes),
            "success": success,
            "overoz": overoz if overoz is not None else 0.0,
            "num_passes": len(passes),
        })

        print(f"    Round {round_num}: success={success}, overoz={overoz:.4f}, passes={len(passes)}")

        # Store for next round's feedback
        prev_passes = passes
        prev_success = success
        prev_overoz = overoz if overoz is not None else 0.0
        prev_error = error_msg if not success else ""

        time.sleep(RETRY_DELAY)

    return results


def main():
    parser = argparse.ArgumentParser(description="Iterative Feedback Experiment")
    parser.add_argument("--max-programs", type=int, default=None,
                        help="Max programs per benchmark (for quick testing)")
    parser.add_argument("--max-rounds", type=int, default=5,
                        help="Number of feedback rounds")
    parser.add_argument("--output", type=str, default="iterative_feedback_results.csv",
                        help="Output CSV file")
    args = parser.parse_args()

    global MAX_ROUNDS
    MAX_ROUNDS = args.max_rounds

    all_results = []

    for dataset_file in DATASETS:
        parquet_path = os.path.join(DATASET_DIR, dataset_file)
        bench_name = dataset_file.replace("rl_validation_", "").replace(".parquet", "")
        print(f"\n{'='*60}")
        print(f"Benchmark: {bench_name}")
        print(f"{'='*60}")

        try:
            df = pd.read_parquet(parquet_path)
        except Exception as e:
            print(f"Failed to read {parquet_path}: {e}")
            continue

        programs = []
        for idx, row in df.iterrows():
            # Extract features
            match = re.search(r'```json\n(.*?)\n```', row.get('question', ''), re.DOTALL)
            if match:
                features = json.loads(match.group(1))
            else:
                features = {}

            program_id = row.get('ground_truth', '')
            if not program_id:
                continue

            ll_path = Path(LLVM_IR_DIR) / program_id
            if not ll_path.exists():
                print(f"  Skipping {program_id}: file not found")
                continue

            ll_code = ll_path.read_text()
            programs.append((features, ll_code, program_id))

        if args.max_programs:
            programs = programs[:args.max_programs]

        print(f"  Total programs: {len(programs)}")

        for model_id, model_name in MODELS:
            print(f"\n  --- Model: {model_name} ---")
            for i, (features, ll_code, program_id) in enumerate(programs):
                print(f"  [{i+1}/{len(programs)}] {program_id}")
                results = run_experiment_for_program(
                    features, ll_code, model_id, model_name, program_id
                )
                for r in results:
                    r["benchmark"] = bench_name
                all_results.extend(results)

                # Save intermediate results
                if (i + 1) % 3 == 0:
                    save_results(all_results, args.output)

    save_results(all_results, args.output)
    print_summary(all_results)


def save_results(results, output_path):
    """Save results to CSV."""
    if not results:
        return
    keys = results[0].keys()
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"  Results saved to {output_path}")


def print_summary(results):
    """Print per-round summary statistics."""
    print(f"\n{'='*70}")
    print("SUMMARY: Per-Round Performance")
    print(f"{'='*70}")

    models = sorted(set(r["model"] for r in results))
    rounds = sorted(set(r["round"] for r in results))

    print(f"\n{'Model':<20} {'Round':>6} {'AvgOverOz':>10} {'SuccessRate':>12} {'AvgPasses':>10}")
    print("-" * 62)

    for model in models:
        for rd in rounds:
            rd_results = [r for r in results if r["model"] == model and r["round"] == rd]
            if not rd_results:
                continue
            avg_overoz = sum(r["overoz"] for r in rd_results) / len(rd_results)
            success_rate = sum(1 for r in rd_results if r["success"]) / len(rd_results)
            avg_passes = sum(r["num_passes"] for r in rd_results) / len(rd_results)
            print(f"{model:<20} {rd:>6} {avg_overoz:>10.4f} {success_rate*100:>11.1f}% {avg_passes:>10.1f}")
        print()


if __name__ == "__main__":
    main()
