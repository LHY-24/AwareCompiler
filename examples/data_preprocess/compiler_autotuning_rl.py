#!/usr/bin/env python
# Copyright 2024 XXX and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Preprocess the compiler autotuning meta dataset to create RL training data
"""

import os
import pandas as pd
import datasets
import argparse
import json
import random
from tqdm import tqdm
import numpy as np
from verl.utils.hdfs_io import copy, makedirs
import glob
from agent_r1.tool.tools.comiler_autotuning.raw_tool.get_autophase import get_autophase_obs

import sys
# export PYTHONPATH=<repo_root>/verl/:$PYTHONPATH
sys.path.append('../../')
sys.path.append('../../verl/verl/utils')


def read_json_file(file_path):
    """
    Read JSON file from meta_dataset directory
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        JSON data as dictionary
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def read_llvm_ir_file(file_path):
    """
    Read LLVM IR code from a file
    
    Args:
        file_path: Path to the LLVM IR file
        
    Returns:
        LLVM IR code as string
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def get_autophase_features(ll_code):
    """
    Get autophase features from LLVM IR code
    
    Args:
        ll_code: LLVM IR code
        
    Returns:
        autophase features dictionary, or None if error
    """
    try:
        features = get_autophase_obs(ll_code)
        return features
    except Exception as e:
        print(f"Error getting autophase features: {e}")
        return None


def format_autophase_features(features):
    """
    Format autophase features as JSON string
    
    Args:
        features: Dictionary of autophase features
        
    Returns:
        Formatted JSON string
    """
    return json.dumps(features, indent=2)


def generate_rl_question(autophase_features, filename):
    """
    Generate question for RL training based on SFT question format
    
    Args:
        autophase_features: Dictionary of autophase features
        
    Returns:
        Formatted question string
    """
    # Format features
    formatted_features = format_autophase_features(autophase_features)
    
    # Build question
    question = (
    "You are a compiler optimization expert. Your goal is to find an optimal LLVM pass sequence that minimizes the total instruction count for the given program.\n"
    "The program's LLVM IR is summarized by autophase features:\n"
    "```json\n"
    + formatted_features +
    "\n```\n"
    "Initial instruction count: " + str(autophase_features.get('TotalInsts', 'N/A')) + "\n"
    "Your workflow:\n"
    "1. In <think> tags, analyze the autophase features and explain your reasoning about which passes may be effective.\n"
    "2. Use the lightrag_compiler_optimization tool to retrieve a recommended pass sequence from the knowledge base. Show the tool response in <tool_response> tags.\n"
    "3. Use the instrcount tool to verify the recommended pass sequence from lightrag_compiler_optimization. Show the tool call and response.\n"
    "4. Carefully interpret the instrcount tool's result: a positive value for improvement_over_oz means the optimization is effective, while a negative value indicates the pass sequence is less effective than -Oz (negative optimization). You should be able to distinguish and respond accordingly.\n"
    "5. Do NOT simply copy the pass sequence returned by lightrag_compiler_optimization. Instead, use it as a reference, and further reason, refine, or combine with your own analysis to propose an even better pass sequence. Your final answer should reflect your own optimization expertise and improvements over the baseline.\n"
    "6. Always end with <answer> tags containing your final recommended pass sequence.\n"
    "\nRequirements:\n"
    "- Always use <think> tags for your initial analysis.\n"
    "- Always use <tool_call> and <tool_response> tags for tool interactions.\n"
    f"- When invoking the instrcount tool, use {filename} as the filename and your chosen optimization_flags as the tool's parameters.\n"
    "- You MUST output the final pass sequence in <answer> tags, formatted as a JSON list.\n"
    "- The <answer> tag should only contain the pass sequence, nothing else.\n"
    "- If you do not output <answer> with a valid JSON list, you will receive zero reward.\n"
    "- If your first attempt does not improve over -Oz, reflect in <think> and try a new sequence, or consult the knowledge base again.\n"
    "- Do not include any explanation, text, or comments in <answer>. Only output the pass sequence as a JSON list.\n"
    "- Your reward is based on both format correctness and optimization effectiveness. Missing <answer> or incorrect format will result in zero reward.\n"
    "\nAdditional notes:\n"
    "- When interpreting instrcount results, remember: positive improvement_over_oz means the optimization is successful, negative means it is not. Adjust your strategy accordingly.\n"
    "- Your final answer should be the result of your own reasoning and refinement, not a direct copy of the tool's output.\n"
    "\nExample output format:\n"
    "<|im_start|>assistant\n"
    "<think>\n"
    "Analyzing the autophase features:\n"
    "- Total instructions: 1200\n"
    "- Total blocks: 200\n"
    "- Memory instructions: 800\n"
    "- Branch count: 150\n"
    "Given the high number of memory instructions and blocks, I will prioritize memory and control-flow optimizations. Let me try an initial pass sequence and use the instrcount tool to check its effectiveness.\n"
    "</think>\n\n"
    "<tool_call>\n"
    "{\n"
    "  \"name\": \"instrcount\",\n"
    "  \"arguments\": {\n"
    "    \"filename\": \"example_program.ll\",\n"
    "    \"optimization_flags\": [\"--mem2reg\", \"--instcombine\", \"--simplifycfg\", \"--gvn\", \"--dce\"]\n"
    "  }\n"
    "}\n"
    "</tool_call>\n"
    "<|im_end|>\n\n"
    "<|im_start|>user\n"
    "<tool_response>\n"
    "{\n"
    "  \"filename\": \"<repo_root>/examples/data_preprocess/llvmir_datasets/example_program.ll\",\n"
    "  \"status\": \"success\",\n"
    "  \"improvement_over_oz\": -0.05\n"
    "}\n"
    "</tool_response>\n"
    "<|im_end|>\n\n"
    "<|im_start|>assistant\n"
    "<think>\n"
    "The instrcount tool reports an improvement_over_oz of -0.05, which is not better than -Oz. I will consult the knowledge base using the lightrag_compiler_optimization tool.\n"
    "</think>\n\n"
    "<tool_call>\n"
    "{\n"
    "  \"name\": \"lightrag_compiler_optimization\",\n"
    "  \"arguments\": {\n"
    "    \"query\": \"Autophase features: TotalInsts=1200, TotalBlocks=200, TotalMemInst=800, BranchCount=150\"\n"
    "  }\n"
    "}\n"
    "</tool_call>\n"
    "<|im_end|>\n\n"
    "<|im_start|>user\n"
    "<tool_response>\n"
    "Based on the knowledge base, the recommended pass sequence is:\n"
    "**Optimal Pass Sequence for this Program:**\n"
    "```json\n"
    "[\"--inferattrs\", \"--dse\", \"--mldst-motion\", \"--mergefunc\", \"--instsimplify\", \"--correlated-propagation\", \"--slp-vectorizer\", \"--early-cse-memssa\", \"--gvn\", \"--load-store-vectorizer\", \"--adce\", \"--gvn-hoist\", \"--die\", \"--loop-simplifycfg\", \"--sroa\", \"--reassociate\", \"--lower-constant-intrinsics\", \"--newgvn\", \"--simplifycfg\"]\n"
    "```\n"
    "Performance Improvement (OverOz): 0.42\n"
    "</tool_response>\n"
    "<|im_end|>\n\n"
    "<|im_start|>assistant\n"
    "<think>\n"
    "I will verify the recommended pass sequence from the knowledge base using the instrcount tool.\n"
    "</think>\n\n"
    "<tool_call>\n"
    "{\n"
    "  \"name\": \"instrcount\",\n"
    "  \"arguments\": {\n"
    "    \"filename\": \"example_program.ll\",\n"
    "    \"optimization_flags\": [\"--inferattrs\", \"--dse\", \"--mldst-motion\", \"--mergefunc\", \"--instsimplify\", \"--correlated-propagation\", \"--slp-vectorizer\", \"--early-cse-memssa\", \"--gvn\", \"--load-store-vectorizer\", \"--adce\", \"--gvn-hoist\", \"--die\", \"--loop-simplifycfg\", \"--sroa\", \"--reassociate\", \"--lower-constant-intrinsics\", \"--newgvn\", \"--simplifycfg\"]\n"
    "  }\n"
    "}\n"
    "</tool_call>\n"
    "<|im_end|>\n\n"
    "<|im_start|>user\n"
    "<tool_response>\n"
    "{\n"
    "  \"filename\": \"<repo_root>/examples/data_preprocess/llvmir_datasets/example_program.ll\",\n"
    "  \"status\": \"success\",\n"
    "  \"improvement_over_oz\": 0.42\n"
    "}\n"
    "</tool_response>\n"
    "<|im_end|>\n\n"
    "<|im_start|>assistant\n"
    "<think>\n"
    "The recommended sequence from the knowledge base shows improvement over -Oz. I will use it as the final answer.\n"
    "</think>\n\n"
    "<answer>[\"--inferattrs\", \"--dse\", \"--mldst-motion\", \"--mergefunc\", \"--instsimplify\", \"--correlated-propagation\", \"--slp-vectorizer\", \"--early-cse-memssa\", \"--gvn\", \"--load-store-vectorizer\", \"--adce\", \"--gvn-hoist\", \"--die\", \"--loop-simplifycfg\", \"--sroa\", \"--reassociate\", \"--lower-constant-intrinsics\", \"--newgvn\", \"--simplifycfg\"]</answer>\n"
    "<|im_end|>\n"
)
    
    return question


def process_json_file(file_path):
    """
    Process a single JSON file for RL training (meta_dataset)
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary with question and ground_truth (program_id)
    """
    json_data = read_json_file(file_path)
    if json_data is None:
        return None
    
    try:
        program_id = json_data['program_id']
        autophase_features = json_data['autophase_features']
        question = generate_rl_question(autophase_features, program_id)
        
        return {
            'question': question,
            'ground_truth': program_id
        }
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def process_ll_file(file_path):
    """
    Process a single .ll file for RL validation training
    
    Args:
        file_path: Path to the .ll file
        
    Returns:
        Dictionary with question and ground_truth (filename)
    """
    ll_code = read_llvm_ir_file(file_path)
    if ll_code is None:
        return None
    
    try:
        # Extract autophase features
        autophase_features = get_autophase_features(ll_code)
        if autophase_features is None:
            return None
        
        # Use filename as program_id/ground_truth
        filename = os.path.basename(file_path)
        question = generate_rl_question(autophase_features, filename)
        
        return {
            'question': question,
            'ground_truth': filename
        }
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def process_validation_datasets(llvm_ir_dir, max_samples_per_val=None):
    """
    Process validation datasets from llvmir_datasets/test directory
    
    Args:
        llvm_ir_dir: Directory containing validation .ll files
        max_samples_per_val: Maximum samples per validation dataset
        
    Returns:
        Dictionary of validation datasets {dataset_name: records_list}
    """
    validation_datasets = {}
    
    if not os.path.exists(llvm_ir_dir):
        print(f"Validation directory {llvm_ir_dir} does not exist")
        return validation_datasets
    
    # Get all subdirectories
    subdirs = [d for d in os.listdir(llvm_ir_dir) 
               if os.path.isdir(os.path.join(llvm_ir_dir, d))]
    
    print(f"Found {len(subdirs)} validation subdirectories: {subdirs}")
    
    for subdir in subdirs:
        subdir_path = os.path.join(llvm_ir_dir, subdir)
        ll_files = glob.glob(os.path.join(subdir_path, '*.ll'))
        
        if not ll_files:
            print(f"No .ll files found in {subdir_path}")
            continue
            
        print(f"Processing {len(ll_files)} .ll files in {subdir}")
        
        # Limit samples if needed
        if max_samples_per_val is not None and max_samples_per_val < len(ll_files):
            ll_files = random.sample(ll_files, max_samples_per_val)
            print(f"Limited to {len(ll_files)} samples for {subdir}")
        
        val_records = []
        for ll_file in tqdm(ll_files, desc=f"Processing {subdir}"):
            rl_data = process_ll_file(ll_file)
            if rl_data is not None:
                val_records.append(rl_data)
        
        if val_records:
            validation_datasets[subdir] = val_records
            print(f"Generated {len(val_records)} records for validation dataset {subdir}")
    
    return validation_datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--meta_dataset_dir', default='./meta_dataset',
                        help='Directory containing JSON files from meta_dataset')
    parser.add_argument('--llvm_ir_dir', default='./llvmir_datasets/test',
                        help='Directory containing validation LLVM IR files')
    parser.add_argument('--output_dir', default='../../dataset/rl',
                        help='Directory to save the processed RL data')
    parser.add_argument('--max_samples', type=int, default=None,
                        help='Maximum number of samples to process from meta_dataset')
    parser.add_argument('--max_samples_per_val', type=int, default=None,
                        help='Maximum number of samples per validation dataset')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for data splitting')
    parser.add_argument('--skip_validation', action='store_true',
                        help='Skip processing validation datasets')

    args = parser.parse_args()

    # Set random seed
    random.seed(args.seed)
    np.random.seed(args.seed)

    # Create output directory
    output_dir = os.path.expanduser(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Process main training data from meta_dataset
    meta_dataset_path = os.path.join(os.path.dirname(__file__), args.meta_dataset_dir)
    json_files = glob.glob(os.path.join(meta_dataset_path, '*.json'))
    
    if json_files:
        print(f"Found {len(json_files)} JSON files in {meta_dataset_path}")
        
        # Shuffle files to ensure random distribution
        random.shuffle(json_files)
        
        # Limit samples if needed
        if args.max_samples is not None and args.max_samples < len(json_files):
            json_files = json_files[:args.max_samples]
        
        # Process JSON files
        data_records = []
        
        for file_path in tqdm(json_files, desc="Processing meta_dataset JSON files for RL"):
            try:
                rl_data = process_json_file(file_path)
                if rl_data is not None:
                    data_records.append(rl_data)
            except Exception as e:
                print(f"\nError processing {file_path}: {e}")
                continue
        
        print(f"Successfully processed {len(data_records)} records from meta_dataset for RL training")
        
        if data_records:
            # Create training dataset
            train_dataset = datasets.Dataset.from_pandas(pd.DataFrame(data_records))
            
            # Format for RL training
            def process_for_rl(example):
                return {
                    "data_source": "meta_dataset",
                    "prompt": [{"role": "user", "content": example["question"]}],
                    "ability": "compiler_autotuning",
                    "reward_model": {
                        "style": "rule",
                        "ground_truth": example["ground_truth"]
                    }
                }
            
            train_dataset = train_dataset.map(process_for_rl)
            
            # Save training dataset
            train_dataset.to_parquet(os.path.join(output_dir, 'rl_train.parquet'))
            print(f"Saved RL training dataset to {output_dir}/rl_train.parquet")
            
            # Show a sample
            sample = train_dataset[0]
            print(f"\nSample RL training record:")
            print(f"- Ground truth (program_id): {sample['ground_truth']}")
            print(f"- Question length: {len(sample['question'])} characters")
    else:
        print(f"No JSON files found in {meta_dataset_path}")
    
    # Process validation datasets
    if not args.skip_validation:
        llvm_ir_path = os.path.join(os.path.dirname(__file__), args.llvm_ir_dir)
        validation_datasets = process_validation_datasets(llvm_ir_path, args.max_samples_per_val)
        
        # Save each validation dataset
        for val_name, val_records in validation_datasets.items():
            if val_records:
                val_dataset = datasets.Dataset.from_pandas(pd.DataFrame(val_records))
                
                # Format for RL validation
                val_dataset = val_dataset.map(lambda example: {
                    "data_source": val_name,
                    "prompt": [{"role": "user", "content": example["question"]}],
                    "ability": "compiler_autotuning",
                    "reward_model": 
                        {
                            "style": "rule",
                            "ground_truth": example["ground_truth"]
                        }
                })
                
                # Save validation dataset
                val_filename = f'rl_validation_{val_name}.parquet'
                val_dataset.to_parquet(os.path.join(output_dir, val_filename))
                print(f"Saved RL validation dataset to {output_dir}/{val_filename}")
        
        print(f"\nProcessed {len(validation_datasets)} validation datasets")
    else:
        print("Skipped validation dataset processing")


if __name__ == '__main__':
    main() 