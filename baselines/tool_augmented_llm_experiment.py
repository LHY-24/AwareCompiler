#!/usr/bin/env python3
"""
Tool-Augmented LLM Experiment for ICML Rebuttal (Q3)
=====================================================
Tests a pretrained LLM using the SAME tool-calling pipeline as AwareCompiler
(knowledge retrieval + instrcount) WITHOUT SFT/RL training.

This directly addresses: "include a comparison against a strong baseline where
a pretrained LLM uses the same tool-calling pipeline without additional SFT/RL training."
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

# ============================================================
# Configuration
# ============================================================
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

REPO_ROOT = Path(__file__).resolve().parents[1]
LLVM_IR_DIR = str(REPO_ROOT / "examples/data_preprocess/llvmir_datasets")
LLVM_TOOLS_PATH = str(REPO_ROOT / "agent_r1/tool/tools/comiler_autotuning/raw_tool")
DATASET_DIR = str(REPO_ROOT / "dataset/rl")
KNOWLEDGE_BASE_PATH = str(REPO_ROOT / "knowledge_base")

MODELS = [
    ("deepseek/deepseek-chat-v3-0324", "DeepSeek-V3"),
    ("qwen/qwen3-235b-a22b", "Qwen3-235B"),
    ("anthropic/claude-sonnet-4", "Claude-Sonnet-4"),
]

DATASETS = [
    "rl_validation_cbench-v1.parquet",
]

MAX_TOOL_ROUNDS = 4  # Max tool-calling rounds per program
RETRY_DELAY = 1

# ============================================================
# LLVM Tools (same as iterative_feedback_experiment.py)
# ============================================================
# Reuse the project's proven instrcount implementation
sys.path.insert(0, str(REPO_ROOT))
from agent_r1.tool.tools.comiler_autotuning.raw_tool.get_instrcount import (
    get_instrcount as _raw_get_instrcount, get_overOz as _raw_get_overOz,
    GenerateOptimizedLLCode
)


def apply_passes_and_count(ll_code, opt_flags):
    """Apply optimization passes and return (instrcount, success, error_msg)."""
    try:
        ic = _raw_get_instrcount(ll_code, opt_flags, llvm_tools_path=LLVM_TOOLS_PATH)
        if ic is None:
            return None, False, "Failed to get instrcount"
        return ic, True, ""
    except subprocess.CalledProcessError as e:
        return None, False, str(e.stderr)[:300] if e.stderr else str(e)[:300]
    except Exception as e:
        return None, False, str(e)[:300]


def execute_instrcount_tool(ll_code, opt_flags):
    """Simulate the instrcount tool call, returning a JSON response string."""
    try:
        ic = _raw_get_instrcount(ll_code, opt_flags, llvm_tools_path=LLVM_TOOLS_PATH)
        oz_ic = _raw_get_instrcount(ll_code, [""], llvm_tools_path=LLVM_TOOLS_PATH)

        if ic is None:
            return json.dumps({"status": "error", "message": "Compilation failed or invalid passes"})

        overoz = (oz_ic - ic) / oz_ic if oz_ic and oz_ic > 0 else 0.0

        return json.dumps({
            "status": "success",
            "instruction_count": ic,
            "oz_instruction_count": oz_ic,
            "improvement_over_oz": round(overoz, 6),
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)[:300]})


# ============================================================
# Knowledge Base (simplified, reusing existing logic)
# ============================================================
import math

_knowledge_entries = None

def load_knowledge_base():
    global _knowledge_entries
    if _knowledge_entries is not None:
        return _knowledge_entries

    kb_path = Path(KNOWLEDGE_BASE_PATH) / "docs" / "autophase_features.md"
    if not kb_path.exists():
        print(f"Knowledge base not found: {kb_path}")
        _knowledge_entries = []
        return _knowledge_entries

    with open(kb_path, 'r') as f:
        content = f.read()

    entries = re.split(r'\n### [^\n]+\n', content)
    knowledge_entries = []

    for entry in entries:
        if not entry.strip():
            continue
        entry_data = {}
        fp = re.search(r'\*\*File Path:\*\* `([^`]+)`', entry)
        if fp:
            entry_data['file_path'] = fp.group(1)
        perf = re.search(r'\*\*Performance Improvement \(OverOz\):\*\* ([-\d.]+)', entry)
        if perf:
            entry_data['performance_improvement'] = float(perf.group(1))
        ps = re.search(r'\*\*Optimal Pass Sequence:\*\*\n```json\n(\[.*?\])\n```', entry, re.DOTALL)
        if ps:
            try:
                entry_data['optimal_pass_sequence'] = json.loads(ps.group(1))
            except:
                continue
        feat_section = re.search(r'\*\*Autophase Features:\*\*\n\n\| Feature \| Value \|\n\|[^\n]+\|\n((?:\| [^\n]+ \|\n)+)', entry)
        if feat_section:
            features = {}
            for line in feat_section.group(1).strip().split('\n'):
                if '|' in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 2:
                        try:
                            features[parts[0]] = int(parts[1])
                        except:
                            continue
            entry_data['autophase_features'] = features

        if all(k in entry_data for k in ['file_path', 'performance_improvement', 'optimal_pass_sequence', 'autophase_features']):
            knowledge_entries.append(entry_data)

    print(f"Loaded {len(knowledge_entries)} knowledge base entries")
    _knowledge_entries = knowledge_entries
    return _knowledge_entries


FEATURE_WEIGHTS = {
    'TotalInsts': 1.0, 'TotalBlocks': 0.8, 'TotalMemInst': 0.9,
    'BranchCount': 0.7, 'TotalFuncs': 0.6, 'NumLoadInst': 0.8,
    'NumStoreInst': 0.8, 'NumCallInst': 0.7, 'NumAddInst': 0.6,
    'NumMulInst': 0.6, 'NumICmpInst': 0.5, 'NumAllocaInst': 0.7,
    'NumPHIInst': 0.6, 'CriticalCount': 0.5, 'NumEdges': 0.4,
}


def calc_similarity(f1, f2):
    common = set(f1.keys()) & set(f2.keys())
    if not common:
        return 0.0
    tw, wd = 0.0, 0.0
    for feat in common:
        w = FEATURE_WEIGHTS.get(feat, 0.1)
        tw += w
        v1, v2 = f1[feat], f2[feat]
        if v1 == 0 and v2 == 0:
            continue
        elif v1 == 0 or v2 == 0:
            wd += w
        else:
            wd += w * abs(v1 - v2) / max(v1, v2)
    return 1 / (1 + wd / tw) if tw > 0 else 0.0


def execute_knowledge_tool(query_features):
    """Simulate the knowledge retrieval tool call."""
    entries = load_knowledge_base()
    if not entries:
        return json.dumps({"status": "error", "message": "Knowledge base empty"})

    scored = []
    for e in entries:
        sim = calc_similarity(query_features, e.get('autophase_features', {}))
        if sim > 0.05:
            scored.append((sim, e))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:3] if scored else []

    results = []
    for sim, e in top:
        results.append({
            "similarity": round(sim, 4),
            "performance_improvement": e['performance_improvement'],
            "recommended_pass_sequence": e['optimal_pass_sequence'],
        })

    return json.dumps({
        "status": "success",
        "matches": results,
        "message": f"Found {len(results)} similar programs in knowledge base."
    }, indent=2)


# ============================================================
# Tool-Augmented LLM Interaction
# ============================================================

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "lightrag_compiler_optimization",
            "description": "Query the compiler knowledge base for recommended pass sequences based on program features.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Program autophase features as text or JSON, e.g. 'TotalInsts: 180, NumCallInst: 45'"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "instrcount",
            "description": "Apply LLVM optimization passes and measure instruction count. Returns instruction count and improvement over -Oz.",
            "parameters": {
                "type": "object",
                "properties": {
                    "optimization_flags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of LLVM optimization flags, e.g. ['--mem2reg', '--gvn', '--dce']"
                    }
                },
                "required": ["optimization_flags"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are a compiler optimization expert. Your goal is to find an optimal LLVM pass sequence that minimizes total instruction count.

Workflow:
1. Analyze the program's autophase features
2. Use the lightrag_compiler_optimization tool to query the knowledge base for recommended sequences
3. Based on the recommendation, generate a pass sequence
4. Use the instrcount tool to verify the sequence's effectiveness
5. If the result is not satisfactory, refine and try again
6. Output your final pass sequence as a JSON list in <answer> tags

Example final output:
<answer>["--mem2reg", "--gvn", "--dce", "--simplifycfg"]</answer>
"""


def call_llm_with_tools(messages, model_id):
    """Call LLM via OpenRouter with tool definitions."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://awarecompiler.org",
    }
    payload = {
        "model": model_id,
        "messages": messages,
        "tools": TOOL_DEFINITIONS,
        "max_tokens": 4096,
        "temperature": 0.7,
    }

    for attempt in range(3):
        try:
            response = requests.post(OPENROUTER_API_URL, headers=headers,
                                     json=payload, timeout=90)
            result = response.json()
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]
            elif "error" in result:
                print(f"    API error: {result['error']}")
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                print(f"    Unexpected: {str(result)[:200]}")
                time.sleep(RETRY_DELAY * (attempt + 1))
        except Exception as e:
            print(f"    Request failed (attempt {attempt+1}): {e}")
            time.sleep(RETRY_DELAY * (attempt + 1))
    return None


def extract_answer(text):
    """Extract pass list from <answer> tags or JSON list in text."""
    if not text:
        return []
    # Try <answer> tags
    m = re.search(r'<answer>(.*?)</answer>', text, re.DOTALL)
    if m:
        text = m.group(1)
    # Find JSON list
    for match in reversed(list(re.finditer(r'\[([^\[\]]*)\]', text, re.DOTALL))):
        try:
            candidate = json.loads(f"[{match.group(1)}]")
            if isinstance(candidate, list) and all(isinstance(p, str) for p in candidate):
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


def run_tool_augmented(features, ll_code, model_id, model_name, program_id):
    """Run tool-augmented LLM for one program."""
    features_str = json.dumps(features, indent=2)
    user_msg = (
        f"Optimize the following LLVM IR program. Here are its autophase features:\n"
        f"```json\n{features_str}\n```\n"
        f"Find the best pass sequence to minimize instruction count."
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    tool_calls_made = 0
    best_overoz = 0.0
    best_passes = []
    final_passes = []

    for turn in range(MAX_TOOL_ROUNDS * 2):  # *2 for tool call + response pairs
        response_msg = call_llm_with_tools(messages, model_id)
        if response_msg is None:
            break

        content = response_msg.get("content", "") or ""
        tool_calls = response_msg.get("tool_calls", [])

        # Add assistant message
        messages.append(response_msg)

        if tool_calls:
            for tc in tool_calls:
                func_name = tc["function"]["name"]
                try:
                    args = json.loads(tc["function"]["arguments"])
                except:
                    args = {}

                tool_calls_made += 1
                print(f"    Tool call #{tool_calls_made}: {func_name}")

                # Execute tool
                if func_name == "lightrag_compiler_optimization":
                    query = args.get("query", features_str)
                    # Parse features from query
                    query_features = {}
                    for k, v in features.items():
                        query_features[k] = v
                    tool_result = execute_knowledge_tool(query_features)
                elif func_name == "instrcount":
                    flags = args.get("optimization_flags", [])
                    tool_result = execute_instrcount_tool(ll_code, flags)
                    # Track best result
                    try:
                        tr = json.loads(tool_result)
                        if tr.get("status") == "success":
                            ov = tr.get("improvement_over_oz", 0)
                            if ov > best_overoz:
                                best_overoz = ov
                                best_passes = flags
                    except:
                        pass
                else:
                    tool_result = json.dumps({"error": f"Unknown tool: {func_name}"})

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": tool_result,
                })

            time.sleep(RETRY_DELAY)
        else:
            # No tool calls - check for final answer
            final_passes = extract_answer(content)
            if final_passes:
                break
            # If no answer and no tools, break
            if not content.strip():
                break

    # If we got final passes, evaluate them
    if final_passes:
        try:
            final_overoz = _raw_get_overOz(ll_code, final_passes, llvm_tools_path=LLVM_TOOLS_PATH)
            if final_overoz is None:
                final_overoz = 0.0
        except:
            final_overoz = 0.0
    else:
        final_passes = best_passes
        final_overoz = best_overoz

    return {
        "program_id": program_id,
        "model": model_name,
        "tool_calls": tool_calls_made,
        "final_passes": json.dumps(final_passes),
        "overoz": round(final_overoz, 6),
        "success": len(final_passes) > 0 and final_overoz is not None,
        "num_passes": len(final_passes),
    }


# ============================================================
# Main
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Tool-Augmented LLM Experiment")
    parser.add_argument("--max-programs", type=int, default=None)
    parser.add_argument("--output", type=str, default="tool_augmented_results.csv")
    args = parser.parse_args()

    all_results = []

    for dataset_file in DATASETS:
        parquet_path = os.path.join(DATASET_DIR, dataset_file)
        bench_name = dataset_file.replace("rl_validation_", "").replace(".parquet", "")
        print(f"\n{'='*60}")
        print(f"Benchmark: {bench_name}")
        print(f"{'='*60}")

        df = pd.read_parquet(parquet_path)
        programs = []
        for idx, row in df.iterrows():
            match = re.search(r'```json\n(.*?)\n```', row.get('question', ''), re.DOTALL)
            features = json.loads(match.group(1)) if match else {}
            program_id = row.get('ground_truth', '')
            if not program_id:
                continue
            ll_path = Path(LLVM_IR_DIR) / program_id
            if not ll_path.exists():
                continue
            ll_code = ll_path.read_text()
            programs.append((features, ll_code, program_id))

        if args.max_programs:
            programs = programs[:args.max_programs]

        print(f"  Programs: {len(programs)}")

        for model_id, model_name in MODELS:
            print(f"\n  --- Model: {model_name} (with tools) ---")
            for i, (features, ll_code, pid) in enumerate(programs):
                print(f"  [{i+1}/{len(programs)}] {pid}")
                result = run_tool_augmented(features, ll_code, model_id, model_name, pid)
                result["benchmark"] = bench_name
                all_results.append(result)
                print(f"    Result: overoz={result['overoz']:.4f}, tools={result['tool_calls']}, passes={result['num_passes']}")

                if (i + 1) % 3 == 0:
                    save_results(all_results, args.output)

    save_results(all_results, args.output)
    print_summary(all_results)


def save_results(results, path):
    if not results:
        return
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"  Saved to {path}")


def print_summary(results):
    print(f"\n{'='*70}")
    print("SUMMARY: Tool-Augmented LLM vs AwareCompiler")
    print(f"{'='*70}")

    models = sorted(set(r["model"] for r in results))
    print(f"\n{'Model':<25} {'AvgOverOz':>10} {'SuccessRate':>12} {'AvgToolCalls':>13} {'AvgPasses':>10}")
    print("-" * 74)

    for model in models:
        mr = [r for r in results if r["model"] == model]
        avg_ov = sum(r["overoz"] for r in mr) / len(mr)
        sr = sum(1 for r in mr if r["success"]) / len(mr)
        avg_tc = sum(r["tool_calls"] for r in mr) / len(mr)
        avg_p = sum(r["num_passes"] for r in mr) / len(mr)
        print(f"{model + ' (w/ tools)':<25} {avg_ov:>10.4f} {sr*100:>11.1f}% {avg_tc:>13.1f} {avg_p:>10.1f}")

    print(f"\n  Compare with AwareCompiler-7B (CBENCH): OverOz=0.5055, SuccessRate=95%")
    print(f"  Compare with baselines without tools (Table 1 in paper)")


if __name__ == "__main__":
    main()
