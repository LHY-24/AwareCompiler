#!/usr/bin/env python
import os
import pandas as pd
import datasets
import argparse
import json
import random
import ast
from tqdm import tqdm
import numpy as np
from verl.utils.hdfs_io import copy, makedirs
from typing import List, Dict, Optional, Any
import glob
import sys

# Add path to import RAG tool
sys.path.append('../../')
from agent_r1.tool.tools.comiler_autotuning.lightrag_knowledge_tool import LightRAGCompilerTool

# Initialize RAG tool
rag_tool = LightRAGCompilerTool()

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

def format_autophase_features(features):
    """
    Format autophase features as JSON string
    
    Args:
        features: Dictionary of autophase features
        
    Returns:
        Formatted JSON string
    """
    return json.dumps(features, indent=2)

def simulate_instrcount_tool(program_id, pass_sequence, improvement_over_oz):
    """
    Simulate the instrcount_tool output

    Args:
        program_id: Program identifier
        pass_sequence: List of optimization passes
        improvement_over_oz: Improvement over -Oz baseline

    Returns:
        Simulated tool response
    """
    # Convert percentage string to float
    if isinstance(improvement_over_oz, str):
        improvement_value = float(improvement_over_oz.replace('%', ''))
    else:
        improvement_value = improvement_over_oz
    
    return {
        "status": "success",
        "improvement_over_oz": improvement_value
    }

def simulate_find_best_pass_sequence_tool(program_id, best_pass_sequence, improvement_percentage):
    """
    Simulate the find_best_pass_sequence_tool output

    Args:
        program_id: Program identifier
        best_pass_sequence: Best pass sequence found
        improvement_percentage: Improvement percentage

    Returns:
        Simulated tool response
    """
    # Convert percentage string to float
    if isinstance(improvement_percentage, str):
        improvement_value = float(improvement_percentage.replace('%', ''))
    else:
        improvement_value = improvement_percentage
    
    return {
        "status": "success",
        "best_pass_sequence": best_pass_sequence,
        "improvement_percentage": improvement_value
    }

def generate_fast_thinking_success_data(json_data):
    """
    Generate SFT data for fast thinking success scenario (Turn1 BetterThanOz)

    Args:
        json_data: JSON data from meta_dataset

    Returns:
        Dictionary with question and answer
    """
    program_id = json_data['program_id']
    autophase_features = json_data['autophase_features']
    trajectory = json_data['trajectory']

    # Format features
    formatted_features = format_autophase_features(autophase_features)
    
    # Build question
    question = f"""Act as a compiler optimization expert finding an optimal pass sequence for LLVM IR, aiming to reduce the total instruction count.
The LLVM IR code is represented by autophase features, the initial autophase features are:
```json
{formatted_features}
```
Initial instruction count: {autophase_features.get('TotalInsts', 'N/A')}

Your task is to analyze the program characteristics and provide an optimal pass sequence to minimize instruction count compared to the default -Oz optimization.

Please follow this workflow:
1. First, analyze the autophase features based on your experience and intuition to derive an initial pass sequence
2. Call the instrcount tool to check the performance of this sequence
3. If the performance is good (better than -Oz), output the answer directly
4. If the performance is not good, reflect and derive a new pass sequence
5. Call the instrcount tool again to check the performance of the refined sequence
6. If the performance is good, output the answer directly
7. If the performance is still not good, call the lightrag_compiler_optimization tool and use its result as the final answer

Requirements:
- Use <Intuition> tags to wrap your initial analysis of the autophase features
- Use <Reflection> tags if you need to reflect after getting poor results
- Use <tool_call> and <tool_response> tags for tool interactions
- Always end with <answer> tags containing the final pass sequence in list format (e.g., ["--mem2reg", "--instcombine", "--simplifycfg"])

When you invoke the instrcount tool, you must provide the {program_id} as the filename and the optimization flags as the optimization_flags.
"""
    
    # Extract turn1 data
    turn1 = trajectory[0]
    turn1_pass_sequence = turn1['action_input']['pass_sequence']
    turn1_performance = turn1['observation']['performance_vs_Oz']

    tool_call_dict = {
        "name": "instrcount",
        "arguments": {
            "filename": program_id,
            "optimization_flags": turn1_pass_sequence
        }
    }
    tool_call_json = json.dumps(tool_call_dict, indent=2)
    
    
    # Simulate tool call and response
    tool_response = simulate_instrcount_tool(program_id, turn1_pass_sequence, turn1_performance)
    
    # Generate answer for fast thinking success
    answer = f"""
<|im_start|>assistant
<Intuition>
Looking at the autophase features, I can see:
- Total instructions: {autophase_features.get('TotalInsts', 'N/A')}
- Total blocks: {autophase_features.get('TotalBlocks', 'N/A')}
- Memory instructions: {autophase_features.get('TotalMemInst', 'N/A')}
- Branch count: {autophase_features.get('BranchCount', 'N/A')}

Based on these characteristics, I'll formulate a strong initial optimization sequence. Let me call the instrcount tool to check the performance.
</Intuition>

<tool_call>
{tool_call_json}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
{json.dumps(tool_response, indent=2)}
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
Great! The instrcount tool reports an improvement_over_oz of {tool_response['improvement_over_oz']}%. It means the pass sequence provides better optimization than -Oz.
</think>


<answer>{json.dumps(turn1_pass_sequence)}</answer>

<|im_end|>
"""
    print(answer)
    return {
        'question': question,
        'answer': answer,
        'program_id': program_id,
        'scenario': 'fast_thinking_success',
        'performance': turn1_performance,
        'pass_sequence': turn1_pass_sequence
    }

def generate_reflection_success_data(json_data):
    """
    Generate SFT data for reflection success scenario (Turn1 WorseThanOz, Turn2 BetterThanOz)
    
    Args:
        json_data: JSON data from meta_dataset
        
    Returns:
        Dictionary with question and answer
    """
    program_id = json_data['program_id']
    autophase_features = json_data['autophase_features']
    trajectory = json_data['trajectory']
    
    # Format features
    formatted_features = format_autophase_features(autophase_features)
    
    # Build question
    question = f"""Act as a compiler optimization expert finding an optimal pass sequence for LLVM IR, aiming to reduce the total instruction count.
The LLVM IR code is represented by autophase features, the initial autophase features are:
```json
{formatted_features}
```
Initial instruction count: {autophase_features.get('TotalInsts', 'N/A')}

Your task is to analyze the program characteristics and provide an optimal pass sequence to minimize instruction count compared to the default -Oz optimization.

Please follow this workflow:
1. First, analyze the autophase features based on your experience and intuition to derive an initial pass sequence
2. Call the instrcount tool to check the performance of this sequence
3. If the performance is good (better than -Oz), output the answer directly
4. If the performance is not good, reflect and derive a new pass sequence
5. Call the instrcount tool again to check the performance of the refined sequence
6. If the performance is good, output the answer directly
7. If the performance is still not good, call the lightrag_compiler_optimization tool and use its result as the final answer

Requirements:
- Use <Intuition> tags to wrap your initial analysis of the autophase features
- Use <Reflection> tags if you need to reflect after getting poor results
- Use <tool_call> and <tool_response> tags for tool interactions
- Always end with <answer> tags containing the final pass sequence in list format (e.g., ["--mem2reg", "--instcombine", "--simplifycfg"])

When you invoke the instrcount tool, you must provide the {program_id} as the filename and the optimization flags as the optimization_flags.
"""
    
    # Extract turn1 and turn2 data
    turn1 = trajectory[0]
    turn1_pass_sequence = turn1['action_input']['pass_sequence']
    turn1_performance = turn1['observation']['performance_vs_Oz']
    
    turn2 = trajectory[1]
    turn2_thought = turn2['thought']
    turn2_pass_sequence = turn2['action_input']['pass_sequence']
    turn2_performance = turn2['observation']['performance_vs_Oz']
    
    tool_call_dict = {
        "name": "instrcount",
        "arguments": {
            "filename": program_id,
            "optimization_flags": turn1_pass_sequence
        }
    }
    tool_call_json1 = json.dumps(tool_call_dict, indent=2)

    tool_call_dict2 = {
        "name": "instrcount",
        "arguments": {
            "filename": program_id,
            "optimization_flags": turn2_pass_sequence
        }
    }
    tool_call_json2 = json.dumps(tool_call_dict2, indent=2)
    # Simulate tool calls and responses
    tool_response1 = simulate_instrcount_tool(program_id, turn1_pass_sequence, turn1_performance)
    tool_response2 = simulate_instrcount_tool(program_id, turn2_pass_sequence, turn2_performance)
    
    # Generate answer with reflection
    answer = f"""
<|im_start|>assistant
<Intuition>
Looking at the autophase features, I can see:
- Total instructions: {autophase_features.get('TotalInsts', 'N/A')}
- Total blocks: {autophase_features.get('TotalBlocks', 'N/A')}
- Memory instructions: {autophase_features.get('TotalMemInst', 'N/A')}
- Branch count: {autophase_features.get('BranchCount', 'N/A')}

Based on these characteristics, I'll formulate a strong initial optimization sequence. Let me call the instrcount tool to check the performance.
</Intuition>

<tool_call>
{tool_call_json1}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
{json.dumps(tool_response1, indent=2)}
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
The instrcount tool reports an improvement_over_oz of {tool_response1['improvement_over_oz']}%. It means the pass sequence performs worse than -Oz optimization. Let me reflect on this result.
</think>

<Reflection>
{turn2_thought} Let me try a refined approach with a different pass sequence.
</Reflection>

<tool_call>
{tool_call_json2}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
{json.dumps(tool_response2, indent=2)}
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
Excellent! After reflection, the refined sequence achieves an improvement_over_oz of {tool_response2['improvement_over_oz']}%, which is better than -Oz optimization.
</think>

<answer>{json.dumps(turn2_pass_sequence)}</answer>

<|im_end|>
"""
    print(answer)
    return {
        'question': question,
        'answer': answer,
        'program_id': program_id,
        'scenario': 'reflection_success',
        'performance': turn2_performance,
        'pass_sequence': turn2_pass_sequence
    }

def generate_rag_fallback_data(json_data):
    """
    Generate SFT data for RAG fallback scenario (Turn1 WorseThanOz, Turn2 WorseThanOz, Use RAG)
    
    Args:
        json_data: JSON data from meta_dataset
        
    Returns:
        Dictionary with question and answer
    """
    program_id = json_data['program_id']
    autophase_features = json_data['autophase_features']
    trajectory = json_data['trajectory']
    
    # Format features
    formatted_features = format_autophase_features(autophase_features)
    
    # Build question
    question = f"""Act as a compiler optimization expert finding an optimal pass sequence for LLVM IR, aiming to reduce the total instruction count.
The LLVM IR code is represented by autophase features, the initial autophase features are:
```json
{formatted_features}
```
Initial instruction count: {autophase_features.get('TotalInsts', 'N/A')}

Your task is to analyze the program characteristics and provide an optimal pass sequence to minimize instruction count compared to the default -Oz optimization.

Please follow this workflow:
1. First, analyze the autophase features based on your experience and intuition to derive an initial pass sequence
2. Call the instrcount tool to check the performance of this sequence
3. If the performance is good (better than -Oz), output the answer directly
4. If the performance is not good, reflect and derive a new pass sequence
5. Call the instrcount tool again to check the performance of the refined sequence
6. If the performance is good, output the answer directly
7. If the performance is still not good, call the lightrag_compiler_optimization tool and use its result as the final answer

Requirements:
- Use <Intuition> tags to wrap your initial analysis of the autophase features
- Use <Reflection> tags if you need to reflect after getting poor results
- Use <tool_call> and <tool_response> tags for tool interactions
- Always end with <answer> tags containing the final pass sequence in list format (e.g., ["--mem2reg", "--instcombine", "--simplifycfg"])

When you invoke the instrcount tool, you must provide the {program_id} as the filename and the optimization flags as the optimization_flags.
"""
    
    # Extract trajectory data
    turn1 = trajectory[0]
    turn1_pass_sequence = turn1['action_input']['pass_sequence']
    turn1_performance = turn1['observation']['performance_vs_Oz']
    
    turn2 = trajectory[1]
    turn2_thought = turn2['thought']
    turn2_pass_sequence = turn2['action_input']['pass_sequence']
    turn2_performance = turn2['observation']['performance_vs_Oz']

    tool_call_dict = {
        "name": "instrcount",
        "arguments": {
            "filename": program_id,
            "optimization_flags": turn1_pass_sequence
        }
    }
    tool_call_json1 = json.dumps(tool_call_dict, indent=2)

    tool_call_dict2 = {
        "name": "instrcount",
        "arguments": {
            "filename": program_id,
            "optimization_flags": turn2_pass_sequence
        }
    }
    tool_call_json2 = json.dumps(tool_call_dict2, indent=2)

    rag_tool_call_dict = {
        "name": "lightrag_compiler_optimization",
        "arguments": {"query": question} # 直接传入原始 question 字符串
    }
    rag_tool_call_json = json.dumps(rag_tool_call_dict, indent=2)

    # Simulate tool calls and responses
    tool_response1 = simulate_instrcount_tool(program_id, turn1_pass_sequence, turn1_performance)
    tool_response2 = simulate_instrcount_tool(program_id, turn2_pass_sequence, turn2_performance)
    
    # Actually call RAG tool to get enhanced prompt
    try:
        rag_enhanced_prompt = rag_tool.execute({"query": question})
        
        # Get most similar pass sequence from RAG tool as final answer
        final_pass_sequence = rag_tool.get_most_similar_pass_sequence(question)
        
        # If RAG tool doesn't return valid pass sequence, use final_answer from original data
        if not final_pass_sequence:
            final_answer = json_data.get('final_answer', {})
            final_pass_sequence = final_answer.get('pass_sequence', ["--mem2reg", "--instcombine", "--simplifycfg"])
            
        # Get performance information
        final_performance = json_data.get('final_answer', {}).get('performance_vs_Oz', 'N/A')
        
    except Exception as e:
        print(f"RAG tool call failed: {e}")
        # Use fallback
        rag_enhanced_prompt = "RAG tool is temporarily unavailable. Please use general compiler optimization strategies."
        final_answer = json_data.get('final_answer', {})
        final_pass_sequence = final_answer.get('pass_sequence', ["--mem2reg", "--instcombine", "--simplifycfg"])
        final_performance = final_answer.get('performance_vs_Oz', 'N/A')
    
    # Generate answer with RAG fallback
    answer = f"""
<|im_start|>assistant
<Intuition>
Looking at the autophase features, I can see:
- Total instructions: {autophase_features.get('TotalInsts', 'N/A')}
- Total blocks: {autophase_features.get('TotalBlocks', 'N/A')}
- Memory instructions: {autophase_features.get('TotalMemInst', 'N/A')}
- Branch count: {autophase_features.get('BranchCount', 'N/A')}

Based on these characteristics, I'll formulate a strong initial optimization sequence. Let me call the instrcount tool to check the performance.
</Intuition>

<tool_call>
{tool_call_json1}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
{json.dumps(tool_response1, indent=2)}
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
The instrcount tool reports an improvement_over_oz of {tool_response1['improvement_over_oz']}%. Since this is not better than -Oz, let me reflect on this result.
</think>

<Reflection>
{turn2_thought} Let me try a refined approach with a different pass sequence.
</Reflection>

<tool_call>
{tool_call_json2}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
{json.dumps(tool_response2, indent=2)}
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
The refined sequence still achieves an improvement_over_oz of {tool_response2['improvement_over_oz']}%, which is still not better than -Oz. My heuristics are exhausted. I must now resort to my knowledge base (RAG) to find a known-good sequence.
</think>

<tool_call>
{rag_tool_call_json}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
{rag_enhanced_prompt}
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
Based on the RAG knowledge base retrieval, I can now provide a well-informed optimization sequence.
</think>

<answer>{json.dumps(final_pass_sequence)}</answer>

<|im_end|>
"""
    print(answer)
    return {
        'question': question,
        'answer': answer,
        'program_id': program_id,
        'scenario': 'rag_fallback',
        'performance': final_performance,
        'pass_sequence': final_pass_sequence
    }

def determine_scenario(json_data):
    """
    Determine which scenario this JSON data represents
    
    Args:
        json_data: JSON data from meta_dataset
        
    Returns:
        Scenario type: 'fast_thinking_success', 'reflection_success', or 'rag_fallback'
    """
    trajectory = json_data['trajectory']
    
    # Check if turn1 is BetterThanOz (negative improvement_over_oz)
    if len(trajectory) >= 1:
        turn1_status = trajectory[0]['observation']['status']
        if turn1_status == 'BetterThanOz':
            return 'fast_thinking_success'
    
    # Check if turn2 is BetterThanOz
    if len(trajectory) >= 2:
        turn2_status = trajectory[1]['observation']['status']
        if turn2_status == 'BetterThanOz':
            return 'reflection_success'
    
    # If both turns are WorseThanOz, use RAG fallback
    return 'rag_fallback'

def process_json_file(file_path):
    """
    Process a single JSON file and generate SFT data
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary with SFT data or None if error
    """
    json_data = read_json_file(file_path)
    if json_data is None:
        return None
    
    # Determine scenario
    scenario = determine_scenario(json_data)
    
    # Generate data based on scenario
    if scenario == 'fast_thinking_success':
        return generate_fast_thinking_success_data(json_data)
    elif scenario == 'reflection_success':
        return generate_reflection_success_data(json_data)
    else:
        return generate_rag_fallback_data(json_data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--meta_dataset_dir', default='./meta_dataset',
                        help='Directory containing JSON files from meta_dataset')
    parser.add_argument('--output_dir', default='../../dataset/cold_start',
                        help='Directory to save the processed data')
    # Data split ratios removed - all data will be used for training
    parser.add_argument('--max_samples', type=int, default=None,
                        help='Maximum number of samples to process')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for data splitting')
    parser.add_argument('--show_examples', action='store_true',
                        help='Show examples of different scenarios')
    parser.add_argument('--max_per_scenario', type=int, default=360,
                        help='Maximum number of samples per scenario to balance the dataset')

    args = parser.parse_args()

    # Set random seed
    random.seed(args.seed)
    np.random.seed(args.seed)

    # Create output directory
    output_dir = os.path.expanduser(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Get all JSON files from meta_dataset directory
    meta_dataset_path = os.path.join(os.path.dirname(__file__), args.meta_dataset_dir)
    json_files = glob.glob(os.path.join(meta_dataset_path, '*.json'))
    
    if not json_files:
        print(f"No JSON files found in {meta_dataset_path}")
        return
    
    print(f"Found {len(json_files)} JSON files in {meta_dataset_path}")
    
    # Shuffle files to ensure random distribution across scenarios
    random.shuffle(json_files)
    
    # Limit samples if needed
    if args.max_samples is not None and args.max_samples < len(json_files):
        json_files = json_files[:args.max_samples]
    
    # Process JSON files with balanced sampling
    data_records = []
    scenario_counts = {'fast_thinking_success': 0, 'reflection_success': 0, 'rag_fallback': 0}
    scenario_limits = {'fast_thinking_success': args.max_per_scenario, 'reflection_success': args.max_per_scenario, 'rag_fallback': args.max_per_scenario}
    
    for file_path in tqdm(json_files, desc="Processing JSON files"):
        try:
            # First, determine the scenario type without full processing
            json_data = read_json_file(file_path)
            if json_data is None:
                continue
                
            scenario = determine_scenario(json_data)
            
            # Check if this scenario has reached its limit
            if scenario_counts[scenario] >= scenario_limits[scenario]:
                continue  # Skip this file, scenario limit reached
            
            # Process the file if scenario limit not reached
            sft_data = process_json_file(file_path)
            if sft_data is not None:
                data_records.append(sft_data)
                scenario_counts[sft_data['scenario']] += 1
                
                # Check if all scenarios have reached their limits
                if all(scenario_counts[s] >= scenario_limits[s] for s in scenario_counts):
                    print(f"\nAll scenarios reached their limits ({args.max_per_scenario} each). Stopping processing.")
                    break
                
        except Exception as e:
            print(f"\nError processing {file_path}: {e}")
            continue
    
    print(f"Successfully processed {len(data_records)} records")
    print(f"Scenario distribution (limit: {args.max_per_scenario} each): {scenario_counts}")
    
    # Show which scenarios reached their limits
    for scenario, count in scenario_counts.items():
        if count >= args.max_per_scenario:
            print(f"  {scenario}: {count}/{args.max_per_scenario} (LIMIT REACHED)")
        else:
            print(f"  {scenario}: {count}/{args.max_per_scenario}")
    
    if args.show_examples:
        print("\n=== EXAMPLES ===")
        for scenario in ['fast_thinking_success', 'reflection_success', 'rag_fallback']:
            examples = [r for r in data_records if r['scenario'] == scenario]
            if examples:
                print(f"\n--- {scenario.upper()} EXAMPLE ---")
                example = examples[0]
                print(f"Program ID: {example['program_id']}")
                print(f"Performance: {example['performance']}")
                print(f"Question: {example['question']}")
                print(f"Answer: {example['answer']}")
                print("-" * 50)
    
    # Create dataset (all as training data)
    train_dataset = datasets.Dataset.from_pandas(pd.DataFrame(data_records))
    
    print(f"Dataset: {len(train_dataset)} training samples")
    
    # Format for SFT
    def process_for_sft(example):
        return {
            "extra_info": {
                "question": example["question"],
                "answer": example["answer"]
            },
            "data_source": "compiler_autotuning",
            "ability": "compiler_autotuning",
            "program_id": example["program_id"],
            "scenario": example["scenario"],
            "performance": example["performance"]
        }
    
    train_dataset = train_dataset.map(process_for_sft)
    
    # Save dataset
    train_dataset.to_parquet(os.path.join(output_dir, 'train.parquet'))
    
    print(f"Saved processed dataset to {output_dir}")

if __name__ == '__main__':
    main() 
