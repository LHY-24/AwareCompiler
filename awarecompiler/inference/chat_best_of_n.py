#!/usr/bin/env python3
"""
Script to process a Parquet dataset, run inference with Best-of-N sampling,
extract optimization passes, and calculate the Best OverOz score.
For each record, the model generates N different optimization sequences,
and the best one (with highest OverOz score) is selected as the final result.
"""

# # 使用 16 次采样（默认）
# python -m awarecompiler.inference.chat_best_of_n \
#     --input-file dataset/rl/validation_data.parquet \
#     --num-samples 16

# # 自定义采样次数
# python -m awarecompiler.inference.chat_best_of_n \
#     --input-file dataset/rl/validation_data.parquet \
#     -n 32

# # 保存所有样本的详细结果
# python -m awarecompiler.inference.chat_best_of_n \
#     --input-file dataset/rl/validation_data.parquet \
#     --num-samples 16 \
#     --output-file results/best_of_n_results.csv \
#     --save-all-samples

import argparse
import json
import importlib
import os
import sys
import re
import pandas as pd
import ast
import time
from openai import OpenAI, APIError, APITimeoutError, APIConnectionError, RateLimitError
from typing import List, Optional, Dict, Tuple

# Assuming these imports are correct
from awarecompiler.tool import ToolEnv
from awarecompiler.tool.tools import _default_tools
from awarecompiler.tool.tools.compiler_autotuning.raw_tool.get_instrcount import get_instrcount
import awarecompiler.inference.config as default_config

# Best-of-N Configuration
DEFAULT_NUM_SAMPLES = 16  # Default number of samples for Best-of-N

# Retry Configuration Constants
MAX_ROW_RETRIES = 3  # Reduced since we have multiple samples
ROW_RETRY_DELAY = 30  # Seconds to wait between row processing retries
MAX_API_RETRIES_INTERNAL = 10  # Retries within get_model_response
API_RETRY_DELAY_INTERNAL = 60  # Delay within get_model_response
MAX_INTERACTION_ATTEMPTS = 10  # Max turns for model interaction within one attempt

# ANSI color codes
COLORS = {
    "info": "\033[1;34m", "success": "\033[1;32m", "warning": "\033[1;33m",
    "error": "\033[1;31m", "retry": "\033[1;36m", "reset": "\033[0m",
    "user": "\033[1;34m", "assistant": "\033[1;32m", "tool": "\033[1;33m",
    "tool_call": "\033[1;35m", "bg_user": "\033[44m", "bg_assistant": "\033[42m",
    "bg_tool": "\033[43m", "bg_tool_call": "\033[45m",
    "best": "\033[1;35m",  # Magenta for best result
}

# --- Helper Functions ---
def get_overOz(ll_code: Optional[str], opt_flags: List[str], llvm_tools_path: Optional[str] = None) -> Optional[float]:
    """Calculates OverOz score."""
    if ll_code is None: return None
    if not isinstance(opt_flags, list): return None
    if not all(isinstance(f, str) for f in opt_flags): return None

    try:
        valid_opt_flags = [flag for flag in opt_flags if flag]
        ic_value_result = get_instrcount(ll_code, valid_opt_flags, llvm_tools_path=llvm_tools_path)
        oz_value_result = get_instrcount(ll_code, [" "], llvm_tools_path=llvm_tools_path)

        if oz_value_result is None or ic_value_result is None: return None
        ic_value = ic_value_result.get('ic') if isinstance(ic_value_result, dict) else ic_value_result
        oz_value = oz_value_result.get('ic') if isinstance(oz_value_result, dict) else oz_value_result
        if oz_value is None or ic_value is None: return None

        try:
            oz_value = float(oz_value)
            ic_value = float(ic_value)
        except (ValueError, TypeError): return None
        if oz_value == 0: return None

        overoz = (oz_value - ic_value) / oz_value
        return overoz
    except Exception: return None

def read_llvm_ir_file(file_path: str) -> Optional[str]:
    """Reads LLVM IR code."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file: return file.read()
    except Exception: return None

# --- Argument Parsing and Config Loading ---
def parse_args():
    parser = argparse.ArgumentParser(description='Run Best-of-N batch inference on Parquet data and calculate OverOz.')
    parser.add_argument('--input-file', type=str, required=True, help='Path to the input Parquet file')
    parser.add_argument('--llvm-ir-dir', type=str, default='/PATH_PLACEHOLDER/NIPS_Material/examples/data_preprocess/llvmir_datasets/', help='Base directory containing the LLVM IR files')
    parser.add_argument('--llvm-tools-path', type=str, default="/PATH_PLACEHOLDER/NIPS_Material/awarecompiler/tool/tools/compiler_autotuning/raw_tool/", help='Path to LLVM tools directory')
    parser.add_argument('--env', type=str, default=default_config.ENV, help='Environment for tool selection')
    parser.add_argument('--api-key', type=str, default=default_config.OPENAI_API_KEY, help='OpenAI API key')
    parser.add_argument('--api-base', type=str, default=default_config.OPENAI_API_BASE, help='OpenAI API base URL')
    parser.add_argument('--model', type=str, default=default_config.MODEL_NAME, help='Model name for inference')
    parser.add_argument('--temperature', type=float, default=default_config.TEMPERATURE, help='Temperature for sampling')
    parser.add_argument('--top-p', type=float, default=default_config.TOP_P, help='Top-p for nucleus sampling')
    parser.add_argument('--max-tokens', type=int, default=default_config.MAX_TOKENS, help='Maximum number of tokens to generate')
    parser.add_argument('--repetition-penalty', type=float, default=default_config.REPETITION_PENALTY, help='Repetition penalty')
    parser.add_argument('--config', type=str, default=None, help='Path to custom config file')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    # Best-of-N specific arguments
    parser.add_argument('--num-samples', '-n', type=int, default=DEFAULT_NUM_SAMPLES, 
                        help=f'Number of samples for Best-of-N (default: {DEFAULT_NUM_SAMPLES})')
    parser.add_argument('--output-file', type=str, default=None,
                        help='Path to save detailed results CSV (optional)')
    parser.add_argument('--save-all-samples', action='store_true',
                        help='Save all N samples for each record, not just the best one')
    return parser.parse_args()

def load_custom_config(config_path):
    if not os.path.exists(config_path): raise FileNotFoundError(f"Config file not found: {config_path}")
    spec = importlib.util.spec_from_file_location("custom_config", config_path)
    custom_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(custom_config); return custom_config

# --- Model Response with Internal Retry Logic ---
def get_model_response(client, model_name, messages, env, temperature, top_p, max_tokens, repetition_penalty):
    """Send messages to the model and get the response, with internal retries."""
    last_exception = None
    for attempt in range(MAX_API_RETRIES_INTERNAL + 1):
        try:
            response = client.chat.completions.create(
                model=model_name, messages=messages, tools=env.tool_desc,
                tool_choice="auto", temperature=temperature, top_p=top_p,
                max_tokens=max_tokens, extra_body={"repetition_penalty": repetition_penalty,},
                stop=["</tool_call>"]
            )
            return response
        except (APIError, APITimeoutError, APIConnectionError, RateLimitError) as e:
            last_exception = e
            if attempt < MAX_API_RETRIES_INTERNAL: time.sleep(API_RETRY_DELAY_INTERNAL)
        except Exception as e:
            last_exception = e
            break
    return None

# --- Extract Answer Passes ---
def extract_answer_passes(response_content: Optional[str]) -> Optional[List[str]]:
    """
    Extracts the list of passes from the <answer> tag in the response.
    """
    if response_content is None:
        return None

    answer_match = re.search(r"<answer>(.*?)</answer>", response_content, re.DOTALL | re.IGNORECASE)
    if not answer_match:
        return None

    content_within_answer_tags = answer_match.group(1).strip()
    if not content_within_answer_tags:
        return None

    list_matches = list(re.finditer(r"(\[.*?\])", content_within_answer_tags, re.DOTALL))
    if not list_matches:
        return None

    for list_match in reversed(list_matches):
        list_str_candidate = list_match.group(1)
        try:
            if not (list_str_candidate.count("'") >= 2 or list_str_candidate.count('"') >= 2):
                if list_str_candidate.strip() != "[]":
                    continue

            pass_list = ast.literal_eval(list_str_candidate)
            if isinstance(pass_list, list):
                processed_list = []
                valid_list = True
                for item in pass_list:
                    if isinstance(item, str):
                        stripped_item = item.strip()
                        if stripped_item:
                            processed_list.append(stripped_item)
                    else:
                        valid_list = False
                        break
                
                if valid_list:
                    return processed_list
        except (ValueError, SyntaxError):
            pass

    return None

# --- Process Tool Calls ---
def process_tool_calls(response_message, messages, env, use_colors=True, verbose=False):
    """Process any tool calls in the response"""
    assistant_message = {
        "role": "assistant",
        "content": response_message.content
    }
    
    if response_message.tool_calls:
        assistant_message["tool_calls"] = [
            {
                "id": tool_call.id,
                "type": tool_call.type,
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            }
            for tool_call in response_message.tool_calls
        ]
    
    messages.append(assistant_message)
    
    if verbose:
        if use_colors:
            print(f"\n{COLORS['bg_assistant']} Assistant {COLORS['reset']} {COLORS['assistant']}{response_message.content}{COLORS['reset']}")
        else:
            print(f"\nAssistant: {response_message.content}")
    
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            try:
                args_dict = json.loads(tool_call.function.arguments)
                formatted_args = json.dumps(args_dict, indent=2)
            except json.JSONDecodeError:
                formatted_args = tool_call.function.arguments
            
            if verbose:
                if use_colors:
                    print(f"\n{COLORS['bg_tool_call']} Tool Call {COLORS['reset']} {COLORS['tool_call']}Function: {tool_call.function.name}{COLORS['reset']}")
                else:
                    print(f"\n[Tool Call] Function: {tool_call.function.name}")
            
            result = env.tool_map[tool_call.function.name].execute(json.loads(tool_call.function.arguments))
            
            if verbose:
                if use_colors:
                    print(f"\n{COLORS['bg_tool']} Tool {COLORS['reset']} {COLORS['tool']}{result}{COLORS['reset']}")
                else:
                    print(f"\nTool: {result}")
            
            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })
        
        return True
    else:
        return False


def run_single_inference(client, model_name, final_prompt, env, temperature, top_p, 
                         max_tokens, repetition_penalty, ll_code, llvm_tools_path,
                         use_colors=True, verbose=False) -> Tuple[Optional[float], Optional[List[str]], Optional[str]]:
    """
    Run a single inference and return (overoz_score, flags, response_content).
    Returns (None, None, None) if inference fails.
    """
    messages = [{"role": "user", "content": final_prompt}]
    final_response_content = None
    
    # Model Interaction Loop
    for interaction_attempt in range(MAX_INTERACTION_ATTEMPTS):
        response = get_model_response(client, model_name, messages, env, temperature, top_p, max_tokens, repetition_penalty)
        
        if response is None or not response.choices:
            return None, None, None
        
        response_message = response.choices[0].message
        had_tool_calls = process_tool_calls(response_message, messages, env, use_colors, verbose)

        if not had_tool_calls:
            final_response_content = response_message.content
            break
    
    if final_response_content is None:
        return None, None, None
    
    # Extract flags
    extracted_flags = extract_answer_passes(final_response_content)
    if extracted_flags is None:
        return None, None, final_response_content
    
    # Calculate OverOz
    overoz_value = get_overOz(ll_code, extracted_flags, llvm_tools_path=llvm_tools_path)
    
    return overoz_value, extracted_flags, final_response_content


def run_best_of_n_inference(client, model_name, final_prompt, env, temperature, top_p,
                            max_tokens, repetition_penalty, ll_code, llvm_tools_path,
                            num_samples, use_colors=True, verbose=False) -> Dict:
    """
    Run N independent inferences and return the best result.
    
    Returns a dictionary with:
    - best_overoz: The best OverOz score among all samples
    - best_flags: The flags that achieved the best score
    - best_response: The response content for the best result
    - all_samples: List of all (overoz, flags, response) tuples
    - valid_count: Number of valid samples (non-None OverOz)
    - sample_scores: List of all valid scores
    """
    all_samples = []
    valid_scores = []
    
    for sample_idx in range(num_samples):
        if verbose:
            print(f"  Running sample {sample_idx + 1}/{num_samples}...")
        
        overoz, flags, response = run_single_inference(
            client, model_name, final_prompt, env, temperature, top_p,
            max_tokens, repetition_penalty, ll_code, llvm_tools_path,
            use_colors, verbose
        )
        
        sample_result = {
            'sample_idx': sample_idx,
            'overoz': overoz,
            'flags': flags,
            'response': response
        }
        all_samples.append(sample_result)
        
        if overoz is not None:
            valid_scores.append(overoz)
            if verbose or sample_idx == 0 or (sample_idx + 1) % 4 == 0:
                print(f"    Sample {sample_idx + 1}: OverOz = {overoz:.6f}")
        else:
            if verbose:
                print(f"    Sample {sample_idx + 1}: Failed (None)")
    
    # Find the best result
    best_result = None
    best_overoz = None
    
    for sample in all_samples:
        if sample['overoz'] is not None:
            if best_overoz is None or sample['overoz'] > best_overoz:
                best_overoz = sample['overoz']
                best_result = sample
    
    return {
        'best_overoz': best_overoz,
        'best_flags': best_result['flags'] if best_result else None,
        'best_response': best_result['response'] if best_result else None,
        'best_sample_idx': best_result['sample_idx'] if best_result else None,
        'all_samples': all_samples,
        'valid_count': len(valid_scores),
        'sample_scores': valid_scores,
        'mean_score': sum(valid_scores) / len(valid_scores) if valid_scores else None,
        'min_score': min(valid_scores) if valid_scores else None,
        'max_score': max(valid_scores) if valid_scores else None,
    }


def main():
    args = parse_args()
    use_colors = not args.no_color
    if args.no_color:
        for key in COLORS: COLORS[key] = ""

    config = default_config
    if args.config:
        try: 
            config = load_custom_config(args.config)
            print(f"{COLORS['info']}Info: Loaded custom config.{COLORS['reset']}")
        except Exception as e: 
            print(f"{COLORS['error']}Error loading config: {e}. Using defaults.{COLORS['reset']}")

    ENV = args.env
    OPENAI_API_KEY = args.api_key
    OPENAI_API_BASE = args.api_base
    MODEL_NAME = args.model
    TEMPERATURE = args.temperature
    TOP_P = args.top_p
    MAX_TOKENS = args.max_tokens
    REPETITION_PENALTY = args.repetition_penalty
    INSTRUCTION_FOLLOWING = config.INSTRUCTION_FOLLOWING
    LLVM_IR_DIR = args.llvm_ir_dir
    LLVM_TOOLS_PATH = args.llvm_tools_path
    NUM_SAMPLES = args.num_samples

    print(f"{COLORS['info']}=" * 60)
    print(f"Best-of-{NUM_SAMPLES} Inference Mode")
    print(f"=" * 60 + f"{COLORS['reset']}")

    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    try:
        tools = _default_tools(ENV)
        env = ToolEnv(tools=tools)
        if not isinstance(env.tool_desc, list) or not all(isinstance(t, dict) and t.get("type") == "function" and "function" in t for t in env.tool_desc):
            print(f"{COLORS['error']}Error: ToolEnv format check failed.{COLORS['reset']}")
            sys.exit(1)
    except Exception as e:
        print(f"{COLORS['error']}Error initializing ToolEnv: {e}.{COLORS['reset']}")
        sys.exit(1)

    print(f"{COLORS['info']}Info: Processing file: {args.input_file}{COLORS['reset']}")
    try:
        df = pd.read_parquet(args.input_file)
        print(f"{COLORS['info']}Info: Loaded {len(df)} records.{COLORS['reset']}")
    except Exception as e:
        print(f"{COLORS['error']}Error loading Parquet: {e}{COLORS['reset']}")
        sys.exit(1)

    # Results storage
    results = []
    best_overoz_scores = []
    mean_overoz_scores = []
    processed_count = 0
    error_count = 0

    for index, row in df.iterrows():
        processed_count += 1
        print(f"\n{COLORS['info']}{'='*60}")
        print(f"Record {index+1}/{len(df)} - Best-of-{NUM_SAMPLES}")
        print(f"{'='*60}{COLORS['reset']}")

        # --- Initial Extraction ---
        try:
            user_prompt = next((msg['content'] for msg in row['prompt'] if msg['role'] == 'user'), None)
            filename = row['reward_model']['ground_truth']
            if not user_prompt or not filename:
                raise ValueError("Missing prompt or filename")
            final_prompt = INSTRUCTION_FOLLOWING + "Question: " + user_prompt
            file_path = os.path.join(LLVM_IR_DIR, filename)
            ll_code = read_llvm_ir_file(file_path)
            if ll_code is None:
                raise ValueError(f"Failed to read LLVM IR: {filename}")
        except Exception as e:
            print(f"{COLORS['warning']}Warning: Initial data extraction/read failed for row {index}: {e}. Skipping.{COLORS['reset']}")
            error_count += 1
            continue

        print(f"{COLORS['info']}Filename: {filename}{COLORS['reset']}")

        # --- Run Best-of-N Inference ---
        bon_result = run_best_of_n_inference(
            client, MODEL_NAME, final_prompt, env, TEMPERATURE, TOP_P,
            MAX_TOKENS, REPETITION_PENALTY, ll_code, LLVM_TOOLS_PATH,
            NUM_SAMPLES, use_colors, verbose=False
        )

        # Store result
        record_result = {
            'index': index,
            'filename': filename,
            'num_samples': NUM_SAMPLES,
            'valid_samples': bon_result['valid_count'],
            'best_overoz': bon_result['best_overoz'],
            'mean_overoz': bon_result['mean_score'],
            'min_overoz': bon_result['min_score'],
            'max_overoz': bon_result['max_score'],
            'best_sample_idx': bon_result['best_sample_idx'],
            'best_flags': json.dumps(bon_result['best_flags']) if bon_result['best_flags'] else None,
            'all_scores': json.dumps(bon_result['sample_scores']),
        }
        
        if args.save_all_samples:
            for i, sample in enumerate(bon_result['all_samples']):
                record_result[f'sample_{i}_overoz'] = sample['overoz']
                record_result[f'sample_{i}_flags'] = json.dumps(sample['flags']) if sample['flags'] else None
        
        results.append(record_result)

        if bon_result['best_overoz'] is not None:
            best_overoz_scores.append(bon_result['best_overoz'])
            if bon_result['mean_score'] is not None:
                mean_overoz_scores.append(bon_result['mean_score'])
            
            print(f"\n{COLORS['best']}★ Best-of-{NUM_SAMPLES} Result:{COLORS['reset']}")
            print(f"  {COLORS['success']}Best OverOz: {bon_result['best_overoz']:.6f} (Sample #{bon_result['best_sample_idx'] + 1}){COLORS['reset']}")
            print(f"  Valid Samples: {bon_result['valid_count']}/{NUM_SAMPLES}")
            if bon_result['mean_score'] is not None:
                print(f"  Mean OverOz: {bon_result['mean_score']:.6f}")
                print(f"  Score Range: [{bon_result['min_score']:.6f}, {bon_result['max_score']:.6f}]")
                improvement = bon_result['best_overoz'] - bon_result['mean_score']
                print(f"  {COLORS['best']}Best vs Mean Improvement: +{improvement:.6f}{COLORS['reset']}")
        else:
            print(f"{COLORS['error']}Error: All {NUM_SAMPLES} samples failed for record {index+1}.{COLORS['reset']}")
            error_count += 1

    # --- Final Summary ---
    print(f"\n{COLORS['info']}{'='*60}")
    print("Best-of-N Batch Processing Summary")
    print(f"{'='*60}{COLORS['reset']}")
    print(f"Number of samples per record (N): {NUM_SAMPLES}")
    print(f"Total records attempted: {processed_count}")
    print(f"Records with valid results: {len(best_overoz_scores)}")
    print(f"Records completely failed: {error_count}")

    if best_overoz_scores:
        avg_best_overoz = sum(best_overoz_scores) / len(best_overoz_scores)
        print(f"\n{COLORS['success']}Average Best-of-{NUM_SAMPLES} OverOz: {avg_best_overoz:.6f}{COLORS['reset']}")
        
        if mean_overoz_scores:
            avg_mean_overoz = sum(mean_overoz_scores) / len(mean_overoz_scores)
            print(f"Average Mean OverOz (single sample equivalent): {avg_mean_overoz:.6f}")
            improvement = avg_best_overoz - avg_mean_overoz
            improvement_pct = (improvement / abs(avg_mean_overoz) * 100) if avg_mean_overoz != 0 else 0
            print(f"{COLORS['best']}Best-of-{NUM_SAMPLES} Improvement over Mean: +{improvement:.6f} ({improvement_pct:.2f}%){COLORS['reset']}")
    else:
        print(f"{COLORS['warning']}Warning: No valid OverOz scores were calculated.{COLORS['reset']}")

    # --- Save Results to CSV ---
    if args.output_file or True:  # Always save results
        output_file = args.output_file
        if output_file is None:
            # Generate default output filename
            input_basename = os.path.splitext(os.path.basename(args.input_file))[0]
            output_file = f"{MODEL_NAME}_best_of_{NUM_SAMPLES}_{input_basename}.csv"
        
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_file, index=False)
        print(f"\n{COLORS['info']}Results saved to: {output_file}{COLORS['reset']}")

    # --- Summary Statistics ---
    if best_overoz_scores:
        print(f"\n{COLORS['info']}Detailed Statistics:{COLORS['reset']}")
        print(f"  Best OverOz scores - Min: {min(best_overoz_scores):.6f}, Max: {max(best_overoz_scores):.6f}")
        
        # Calculate percentiles if we have enough data
        if len(best_overoz_scores) >= 4:
            sorted_scores = sorted(best_overoz_scores)
            n = len(sorted_scores)
            p25 = sorted_scores[int(n * 0.25)]
            p50 = sorted_scores[int(n * 0.50)]
            p75 = sorted_scores[int(n * 0.75)]
            print(f"  Percentiles - 25th: {p25:.6f}, 50th (Median): {p50:.6f}, 75th: {p75:.6f}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcessing interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{COLORS['error']}An unexpected critical error occurred: {e}{COLORS['reset']}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
