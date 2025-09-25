#!/usr/bin/env python

import re
import os
import json
import ast
import datetime # Added for the dummy save function
from typing import List, Union, Optional, Dict, Any, Tuple

# This function is used by the scoring logic, so it's kept.
from agent_r1.tool.tools.comiler_autotuning.raw_tool.get_instrcount import get_overOz, get_instrcount

import logging

logging.basicConfig(
    level=logging.INFO,  # 设置最低日志级别为 INFO
    format='%(asctime)s %(levelname)s %(message)s',  # 日志格式
    filename='rl_3B.log',  # 输出到文件（如需输出到控制台可去掉 filename 参数）
    filemode='w'  # 覆盖模式，每次运行会清空旧内容
)

# --- Helper Functions (Existing and New) ---

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
        # Suppress print for scoring function
        print(f"Error reading file {file_path}: {e}")
        return None


def extract_conversation_blocks(text: str) -> List[Dict[str, str]]:
    """
    Extracts all <think>, <tool_call>, <tool_response>, <answer> blocks in order,
    with their role (assistant/user) and tag type.
    """
    blocks = []
    # 先按 <|im_start|>role ... <|im_end|> 分块
    main_pattern = re.compile(
        r"<\|im_start\|>\s*(assistant|user)\s*\n?(.*?)(?=<\|im_end\|>)<\|im_end\|>",
        re.DOTALL | re.IGNORECASE
    )
    # 再在每个块内按标签拆分
    tag_pattern = re.compile(r"<(think|tool_call|tool_response|answer)>(.*?)</\1>", re.DOTALL)
    for match in main_pattern.finditer(text):
        role = match.group(1).strip().lower()
        content = match.group(2).strip()
        for tag_match in tag_pattern.finditer(content):
            tag = tag_match.group(1)
            tag_content = tag_match.group(2).strip()
            blocks.append({"role": role, "tag": tag, "content": tag_content})
    return blocks


def extract_content_between_tags(text: str, tag: str) -> List[str]:
    """Extract all content between specified tags"""
    pattern = f'<{tag}>(.*?)</{tag}>'
    matches = re.findall(pattern, text, re.DOTALL)
    return ast.literal_eval([match.strip() for match in matches][-1])


def validate_pass_sequence(pass_seq: Any) -> bool:
    if not isinstance(pass_seq, list): return False
    for pass_item in pass_seq:
        if not isinstance(pass_item, str) or not (pass_item.startswith('--') or pass_item == '-Oz'):
            return False
    return True


def check_filename_exists(filename: str) -> bool:
    """Check if the provided filename exists in the dataset directory."""
    # Per the prompt, the path is fixed. Be careful with execution context.
    # We assume the script runs in a context where this relative path is valid.
    base_path = os.path.join(os.path.dirname(__file__), "../../../examples/data_preprocess/llvmir_datasets/")
    # The prompt mentions a `test` subdir, let's check there first, then the base.
    test_path = os.path.join(base_path, "test", filename)
    base_path_full = os.path.join(base_path, filename)
    
    return os.path.exists(test_path) or os.path.exists(base_path_full)


def extract_passes_from_rag_response(rag_response_text: str) -> List[str] | None:
    pattern = re.compile(r"\*\*Optimal Pass Sequence for this Program:\*\*\s*```json\s*(.*?)\s*```", re.DOTALL)
    match = pattern.search(rag_response_text)
    if not match: return None
    try:
        passes = json.loads(match.group(1).strip())
        return passes if validate_pass_sequence(passes) else None
    except json.JSONDecodeError:
        return None


def compute_score_format(text: str) -> float:
    """
    Computes format score for the reasoning workflow.
    """
    if not text or not isinstance(text, str):
        logging.info(f"[FORMAT ERROR] the format score: 0.0")
        return 0.0

    score = 0.0

    # 鼓励输出<think>、<tool_call>、<answer>
    blocks = extract_conversation_blocks(text)
    assistant_blocks = [b for b in blocks if b['role'] == 'assistant']
    if not assistant_blocks:
        return 0.0
    tags = [b['tag'] for b in assistant_blocks]
    if "think" in tags:
        score += 1
    if "tool_call" in tags:
        score += 1
    if tags[-1] != 'answer':
        logging.info(f"[FORMAT SCORE] no <answer> in tags={tags}, format score=0.0")
        return 0.0

    # 是否调用lightrag_compiler_optimization
    lightrag_called = any(
        b['tag'] == 'tool_call' and (
            (isinstance(b['content'], str) and 'lightrag_compiler_optimization' in b['content'])
            or (isinstance(b['content'], dict) and b['content'].get('name') == 'lightrag_compiler_optimization')
        )
        for b in assistant_blocks
    )
    if lightrag_called:
        score += 1
        logging.info(f"[FORMAT SCORE] call lightrag_compiler_optimization, score={score}")
    else:
        logging.info(f"[FORMAT SCORE] not call lightrag_compiler_optimization, score={score}")

    # 判断<answer>结果和lightrag_compiler_optimization给出的方案是否一致
    rag_passes = None
    for b in blocks:
        if b['tag'] == 'tool_response' and "OverOz" in b['content']:
            # 提取json方案
            rag_passes = extract_passes_from_rag_response(b['content'])
            break

    # 提取<answer>内容
    answer_passes = None
    for b in assistant_blocks:
        if b['tag'] == 'answer':
            try:
                answer_passes = json.loads(b['content'])
            except Exception:
                pass
            break

    if validate_pass_sequence(answer_passes):
        score += 1
        logging.info(f"[FORMAT SCORE] 'optimization_flags' is a valid pass sequence, score={score}")

    # 比较两者是否一致
    logging.info(f"[FORMAT SCORE] rag_passes={rag_passes}, answer_passes={answer_passes}")
    if rag_passes is not None and answer_passes is not None:
        overlap = len(set(rag_passes) & set(answer_passes)) / max(len(set(rag_passes) | set(answer_passes)), 1)
        innovation_score = 1 - overlap  # 创新度越高分越高
        score += innovation_score  # 可调权重
        logging.info(f"[FORMAT SCORE] innovation_score={innovation_score}, score={score}")
    else:
        logging.info(f"[FORMAT SCORE] <answer> is not consistent with RAG solution or missing, score={score}")

    # 分数归一化到[0,1]
    norm_score = score / 5.0
    logging.info(f"[FORMAT SCORE] the final normalized score: {norm_score}")
    return min(norm_score, 1.0)


def compute_score_answer(solution_str: Optional[str], ground_truth: Optional[Union[str, List[str]]]) -> float:
    """
    Compute the answer reward score:
    - 绝对分数：最终指令数 vs 初始指令数
    - 相对分数：最终指令数 vs -Oz指令数
    - 两者加权作为最终分数
    """
    if solution_str is None or ground_truth is None:
        return 0.0
    # print(f"[DEBUG] solution_str: {solution_str}")

    # Get the filename from ground_truth
    filename = ground_truth if isinstance(ground_truth, str) else ground_truth[0]
    ll_file_path = os.path.join(os.path.dirname(__file__) + "/../../../examples/data_preprocess/llvmir_datasets/", filename)
    ll_code = read_llvm_ir_file(ll_file_path)
    if not ll_code:
        print(f"[DEBUG] Could not read LLVM IR file for ground truth: {filename}")
        return 0.0
    # print(f"[DEBUG] ll_code: read successful!")
        
    try:    
        # Extract pass sequence from the final answer tag
        pass_list = extract_content_between_tags(solution_str, 'answer')
        if not pass_list:
            print("[DEBUG] No valid pass list found in the answer.")
            return 0.0     # Penalize heavily for no valid answer
        # print(f"[DEBUG] pass_list: {pass_list}")

        # Calculate over initial instruction count using the extracted passes
        initial_inst_count = None
        match = re.search(r"Initial instruction count:\s*(\d+)", solution_str)
        if match:
            initial_inst_count = int(match.group(1))
        else:
            logging.warning("Initial instruction count not found in solution_str.")
        print(f"[DEBUG] initial_inst_count: {initial_inst_count}")
        
        # 获取最终指令数
        llvm_tools_path = os.path.join(os.path.dirname(__file__), '../../../agent_r1/tool/tools/comiler_autotuning/raw_tool/')
        final_inst_count = get_instrcount(ll_code, pass_list, llvm_tools_path=llvm_tools_path)
        oz_inst_count = get_instrcount(ll_code, ['-Oz'], llvm_tools_path=llvm_tools_path)

        # 绝对优化分数（初始 vs 最终）
        absolute_score = (initial_inst_count - final_inst_count) / max(initial_inst_count, 1)
        print(f"[DEBUG] pass_list: {pass_list}, absolute_score: {absolute_score}")
        # 相对优化分数（-Oz vs 最终）
        relative_score = (oz_inst_count - final_inst_count) / max(oz_inst_count, 1)
        # overoz = get_overOz(ll_code, pass_list, llvm_tools_path=llvm_tools_path)
        print(f"[DEBUG] pass_list: {pass_list}, overOz: {relative_score}")

        # Scale the reward
        reward = 0.4 * absolute_score + 0.6 * relative_score
        reward = min(max(reward * 10, -1.0), 1.0)
        print(f"[ANSWER SCORE] initial: {initial_inst_count}, oz: {oz_inst_count}, final: {final_inst_count}, overInit: {absolute_score:.3f}, overOz: {relative_score:.3f}, reward: {reward:.3f}")
        return reward
        
    except Exception as e:
        print(f"[DEBUG] Error in compute_score_answer: {e}")
        return 0.0


def compute_score_format_answer(solution_str: str, ground_truth: Union[str, List[str]]) -> float:
    """Compute the total reward score combining format and answer scores."""
    if solution_str is None or ground_truth is None:
        return 0.0
    
    try:
        # Calculate individual scores
        format_reward = compute_score_format(solution_str)
        answer_reward = compute_score_answer(solution_str, ground_truth)
        total_reward = format_reward * 0 + answer_reward * 0.5
        print(f"[DEBUG] Format reward: {format_reward:.3f}, Answer reward: {answer_reward:.3f}, Total reward: {total_reward:.3f}")
        return total_reward
        
    except Exception as e:
        print(f"[DEBUG] Error in compute_score_format_answer: {e}")
        return 0.0



question = '''
<|im_start|>assistant
<think>
Looking at the autophase features, I can see:
- Total instructions: 809
- Total blocks: 138
- Memory instructions: 485
- Branch count: 127

Based on the high memory instruction count, I'll prioritize -mem2reg and -licm optimizations. Reduce call instructions with -simplifycfg. After memory optimizations, store/reg reuse reduces future overhead. Dispatch simple unary ops to -inline. Point to BB03Phi for possible constant propagation if non-zero.
</think>

<tool_call>
{"name": "instrcount", "arguments": {"filename": "tensorflow-v0_1606.ll", "optimization_flags": ["--indvars", "--loop-simplifycfg", "--aggressive-instcombine", "--loop-load-elim", "--sroa", "--lower-guard-intrinsic", "--loop-vectorize", "--post-inline-ee-instrument", "--simple-loop-unswitch", "--loop-interchange", "--elim-avail-extern", "--lower-guard-intrinsic", "--coro-cleanup", "--lower-expect", "--lower-matrix-intrinsics", "--loop-load-elim", "--mem2reg", "--gvn-gcse", "--dce", "--mldst-motion", "--flattencfg", "--dse", "--prune-eh", "--reassociate", "--redundant-dbg-inst-elim"]}}
</tool_call><|im_end|>
<|im_start|>user
<tool_response>
{"filename": "/root/Compiler-R1_1/examples/data_preprocess/llvmir_datasets/tensorflow-v0_1606.ll", "status": "success", "improvement_over_oz": -0.12376237623762376}
</tool_response><|im_end|>
<|im_start|>assistant
<think>
The instrcount tool reports a performance improvement_over_oz of -0.1237%. Since this is not better than -Oz, let me reflect on this result.
</think>

<Reflection>
My initial attempt yielded a performance_over_oz of -0.12%. After reflecting, I believe I can achieve better results. My refined approach captures the program's memory-heavy workload better while preserving flow features. Let me try a different pass sequence.
</Reflection>

<tool_call>
{"name": "instrcount", "arguments": {"filename": "tensorflow-v0_1606.ll", "optimization_flags": ["--early-cse-memssa", "--loop-unroll-and-jam", "--partially-inline-libcalls", "--aggressive-instcombine", "--loop-simplifycfg", "--loop-load-elim", "--loop-load-elim", "--loop-simplifycfg", "--aggressive-instcombine", "--correlated-propagation", "--loop-instsimplify", "--elim-avail-extern", "--inline", "--loop-simplifycfg", "--correlated-propagation", "--die", "--lower-guard-intrinsic", "--partial-inliner", "--rpo-functionattrs", "--instnamer", "--sroa", "--loop-load-elim", "--insert-gcov-profiling", "--coro-cleanup", "--globalopt", "--instsimplify", "--instcombine", "--loop-data-prefetch", "--adce", "--loop-simplifycfg", "--prune-eh", "--newgvn", "--elim-avail-extern", "--post-inline-ee-instrument", "--lower-constant-intrinsics", "--loop-fusion", "--instcombine"]}}
</tool_call><|im_end|>
<|im_start|>user
<tool_response>
{"filename": "/root/Compiler-R1_1/examples/data_preprocess/llvmir_datasets/tensorflow-v0_1606.ll", "status": "success", "improvement_over_oz": -4.207920792079208}
</tool_response><|im_end|>
<|im_start|>assistant
<think>
The refined sequence still achieves an improvement_over_oz of -4.20%, which is still not better than -Oz. My heuristics are exhausted. I must now seek guidance from human experts.
</think>

<tool_call>
{"name": "lightrag_compiler_optimization", "arguments": {"query": "For the program with features:\n\nTotal instructions: 809\nTotal blocks: 138\nMemory instructions: 485\nBranch count: 127\n\nThe pass sequence returned by instrcount yielded:\n\n--indvars\n--loop-simplifycfg\n--aggressive-instcombine\n--loop-load-elim\n--sroa\n--lower-guard-intrinsic\n--loop-vectorize\n--post-inline-ee-instrument\n--simple-loop-unswitch\n--loop-interchange\n--elim-avail-extern\n--lower-guard-intrinsic\n--coro-cleanup\n--lower-expect\n--loop-load-elim\n--mem2reg\n--gvn-gcse\n--dce\n--mldst-motion\n--flattencfg\n--dse\n--prune-eh\n--reassociate\n--redundant-dbg-inst-elim\n\nYour task is to advise on a new pass sequence that strikes a better balance between optimization strength and preservation of program flow, shedding new light on program characteristics and minimizing the difference from -Oz."}}
</tool_call><|im_end|>
<|im_start|>user
<tool_response>
Based on knowledge base retrieval, the best program case was found (similarity: 0.957, composite score: 0.961):

**Optimal Pass Sequence for this Program:**
```json
[
  "--inferattrs",
  "--dse",
  "--mldst-motion",
  "--dse",
  "--mergefunc",
  "--instsimplify",
  "--correlated-propagation",
  "--slp-vectorizer",
  "--dse",
  "--slp-vectorizer",
  "--early-cse-memssa",
  "--gvn",
  "--instsimplify",
  "--load-store-vectorizer",
  "--adce",
  "--gvn-hoist",
  "--correlated-propagation",
  "--die",
  "--loop-simplifycfg",
  "--adce",
  "--sroa",
  "--reassociate",
  "--instsimplify",
  "--lower-constant-intrinsics",
  "--gvn",
  "--slsr",
  "--newgvn",
  "--slsr",
  "--simplifycfg",
  "--newgvn"
]
```

**Performance Improvement (OverOz):** 0.3405

**Selection Rationale:**
This program was selected using a composite scoring algorithm that balances feature similarity (95.7%) and performance improvement (34.1%).

</tool_response><|im_end|>
<|im_start|>assistant
<think>
Based on the human expert's advice, I will follow the optimal pass sequence provided for the program characteristics.
</think>

<answer>["--inferattrs", "--dse", "--mldst-motion", "--dse", "--mergefunc", "--instsimplify", "--correlated-propagation", "--slp-vectorizer", "--dse", "--slp-vectorizer", "--early-cse-memssa", "--gvn", "--instsimplify", "--load-store-vectorizer", "--adce", "--gvn-hoist", "--correlated-propagation", "--die", "--loop-simplifycfg", "--adce", "--sroa", "--reassociate", "--instsimplify", "--lower-constant-intrinsics", "--gvn", "--slsr", "--newgvn", "--slsr", "--simplifycfg", "--newgvn"]</answer>

<|im_end|>
'''



example = '''
<|im_start|>assistant
<think>
Analyzing the autophase features:
- Total instructions: 1200
- Total blocks: 200
- Memory instructions: 800
- Branch count: 150
Given the high number of memory instructions and blocks, I will prioritize memory and control-flow optimizations. Let me try an initial pass sequence and use the instrcount tool to check its effectiveness.
</think>

<tool_call>
{
  "name": "instrcount",
  "arguments": {
    "filename": "example_program.ll",
    "optimization_flags": ["--mem2reg", "--instcombine", "--simplifycfg", "--gvn", "--dce"]
  }
}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
{
  "filename": "/root/Compiler-R1_1/examples/data_preprocess/llvmir_datasets/example_program.ll",
  "status": "success",
  "improvement_over_oz": -0.05
}
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
The instrcount tool reports an improvement_over_oz of -0.05, which is not better than -Oz. I will consult the knowledge base using the lightrag_compiler_optimization tool.
</think>

<tool_call>
{
  "name": "lightrag_compiler_optimization",
  "arguments": {
    "query": "Autophase features: TotalInsts=1200, TotalBlocks=200, TotalMemInst=800, BranchCount=150"
  }
}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
Based on the knowledge base, the recommended pass sequence is:
**Optimal Pass Sequence for this Program:**
```json
["--inferattrs", "--dse", "--mldst-motion", "--mergefunc", "--instsimplify", "--correlated-propagation", "--slp-vectorizer", "--early-cse-memssa", "--gvn", "--load-store-vectorizer", "--adce", "--gvn-hoist", "--die", "--loop-simplifycfg", "--sroa", "--reassociate", "--lower-constant-intrinsics", "--newgvn", "--simplifycfg"]
```
Performance Improvement (OverOz): 0.42
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
I will verify the recommended pass sequence from the knowledge base using the instrcount tool.
</think>

<tool_call>
{
  "name": "instrcount",
  "arguments": {
    "filename": "example_program.ll",
    "optimization_flags": ["--inferattrs", "--dse", "--mldst-motion", "--mergefunc", "--instsimplify", "--correlated-propagation", "--slp-vectorizer", "--early-cse-memssa", "--gvn", "--load-store-vectorizer", "--adce", "--gvn-hoist", "--die", "--loop-simplifycfg", "--sroa", "--reassociate", "--lower-constant-intrinsics", "--newgvn", "--simplifycfg"]
  }
}
</tool_call>
<|im_end|>

<|im_start|>user
<tool_response>
{
  "filename": "/root/Compiler-R1_1/examples/data_preprocess/llvmir_datasets/example_program.ll",
  "status": "success",
  "improvement_over_oz": 0.42
}
</tool_response>
<|im_end|>

<|im_start|>assistant
<think>
The recommended sequence from the knowledge base shows improvement over -Oz. I will use it as the final answer.
</think>

<answer>["--inferattrs", "--dse", "--mldst-motion", "--mergefunc", "--instsimplify", "--correlated-propagation", "--slp-vectorizer", "--early-cse-memssa", "--gvn", "--load-store-vectorizer", "--adce", "--gvn-hoist", "--die", "--loop-simplifycfg", "--sroa", "--reassociate", "--lower-constant-intrinsics", "--newgvn", "--simplifycfg"]</answer>
<|im_end|>
'''

print(compute_score_format(example))
# print(compute_score_format_answer(question))