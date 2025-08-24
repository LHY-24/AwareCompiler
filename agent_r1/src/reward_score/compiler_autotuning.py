#!/usr/bin/env python

import re
import os
import json
import ast
import datetime # Added for the dummy save function
from typing import List, Union, Optional, Dict, Any, Tuple

# This function is used by the scoring logic, so it's kept.
from agent_r1.tool.tools.comiler_autotuning.raw_tool.get_instrcount import get_overOz

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
        # print(f"Error reading file {file_path}: {e}")
        return None

def extract_content_between_tags(text: str, tag: str) -> List[str]:
    """Extract all content between specified tags"""
    pattern = f'<{tag}>(.*?)</{tag}>'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]

def extract_conversation_blocks(text: str) -> List[Dict[str, str]]:
    """Extract conversation blocks delimited by <|im_start|> and <|im_end|>."""
    blocks = []
    pattern = re.compile(r"<\|im_start\|>\s*(\w+)\s*\n?(.*?)<\|im_end\|>", re.DOTALL)
    matches = pattern.finditer(text)
    for match in matches:
        role = match.group(1).strip().lower()
        content = match.group(2).strip()
        if role in ["assistant", "user"]:
             blocks.append({"role": role, "content": content})
    return blocks

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
    Computes format score with strict path validation and dynamic max_score.
    """
    if not text or not isinstance(text, str):
        return 0.0

    score = 0.0
    log = []
    
    # Define max scores for each path based on a base unit (e.g., 60)
    # to reflect the 1 : 1.5 : 2 weight ratio.
    BASE_SCORE_UNIT = 60
    MAX_SCORE_INTUITION = 1.0 * BASE_SCORE_UNIT   # Path A
    MAX_SCORE_REFLECTION = 1.5 * BASE_SCORE_UNIT  # Path B
    MAX_SCORE_RAG = 2.0 * BASE_SCORE_UNIT         # Path C
    
    max_score = 0.0 # Will be set dynamically based on the detected path

    try:
        blocks = extract_conversation_blocks(text)
        if not blocks:
            log.append("FAILED: No conversation blocks found.")
            # print("\n".join(log)) # Uncomment for debugging

        start_index = 0
        if blocks[0]['role'] == 'user':
            # If the text starts with a user prompt, the actual solution starts from the next block.
            start_index = 1
            log.append("NOTE: Initial user prompt detected and skipped for evaluation.")

        # The 'blocks' to be evaluated are from the first assistant move onwards.
        blocks = blocks[start_index:]
        if not blocks:
            log.append("FAILED: No assistant blocks found to evaluate.")
            return 0.0

        # --- Variables to hold state across turns ---
        first_instrcount_passes = None
        second_instrcount_passes = None
        rag_passes = None
        first_improvement = None
        second_improvement = None

        # --- Turn 1: Assistant's Initial Move (Common to all paths) ---
        log.append("\n--- Validating Turn 1 (Assistant) ---")
        if len(blocks) < 1 or blocks[0]['role'] != 'assistant':
            log.append("FAILED: First block is not from assistant.")
            return 0.0
        
        content = blocks[0]['content']
        # 1.1: Check Intuition
        intuition_content = extract_content_between_tags(content, 'Intuition')
        if intuition_content: 
            score += 5; 
            log.append("[+5] Intuition tag found.")
        else: 
            log.append("[+0] FAILED: Intuition tag missing.")
        
        # 1.2: Check first tool_call for instrcount
        tool_calls = extract_content_between_tags(content, 'tool_call')
        if tool_calls and len(tool_calls) == 1:
            try:
                call_data = json.loads(tool_calls[0])
                if call_data.get('name') == 'instrcount':
                    score += 5; 
                    log.append("[+5] First tool call is 'instrcount'.")
                    args = call_data.get('arguments', {})
                    if args.get('filename'): 
                        score += 5; 
                        log.append("[+5] Filename is present.")
                    else: 
                        log.append("[+0] FAILED: Filename missing.")
                    
                    passes = args.get('optimization_flags')
                    if validate_pass_sequence(passes):
                        score += 15; 
                        log.append("[+15] 'optimization_flags' is a valid pass sequence.")
                        first_instrcount_passes = passes
                    else: 
                        log.append("[+0] FAILED: 'optimization_flags' invalid.")
                else: 
                    log.append("[+0] FAILED: First tool call is not 'instrcount'.")
            except json.JSONDecodeError:
                log.append("[+0] FAILED: First tool_call content is not valid JSON.")
        else: 
            log.append("[+0] FAILED: Incorrect number of tool_calls in Turn 1.")

        # --- Turn 2: User's Response (Common to all paths) ---
        log.append("\n--- Validating Turn 2 (User) ---")
        if len(blocks) < 2 or blocks[1]['role'] != 'user':
            log.append("FAILED: Second block is not from user or missing.")
            return 0.0
        
        content = blocks[1]['content']
        responses = extract_content_between_tags(content, 'tool_response')
        if responses and len(responses) == 1:
            try:
                response_data = json.loads(responses[0])
                improvement = response_data.get('improvement_over_oz')
                if isinstance(improvement, (int, float)):
                    score += 10; 
                    log.append(f"[+10] First tool_response is valid with 'improvement_over_oz'.")
                    first_improvement = improvement
                else: 
                    log.append("[+0] FAILED: 'improvement_over_oz' missing or not a number.")
            except json.JSONDecodeError:
                log.append("[+0] FAILED: First tool_response is not valid JSON.")
        else: 
            log.append("[+0] FAILED: Incorrect number of tool_responses in Turn 2.")

        # --- PATH DETERMINATION AND VALIDATION ---
        if first_improvement is None:
            log.append("CRITICAL FAILURE: Cannot determine path due to invalid first tool response.")
            # print("\n".join(log)); return score / (MAX_SCORE_INTUITION) # Punish against lowest bar
            return 0.0

        # --- PATH A: Intuition Success ---
        if first_improvement > 0:
            max_score = MAX_SCORE_INTUITION
            log.append(f"\n>>> DETECTED PATH: Intuition Success (Max Score: {max_score})")

            if len(blocks) < 3 or blocks[2]['role'] != 'assistant':
                log.append("PATH FAILED: Assistant's Turn 3 is missing.")
                return score / max_score if max_score > 0 else 0.0
            
            # Path Structure Validation
            content = blocks[2]['content']
            has_think = len(extract_content_between_tags(content, 'think')) == 1
            has_answer = len(extract_content_between_tags(content, 'answer')) == 1
            has_no_reflection = len(extract_content_between_tags(content, 'Reflection')) == 0
            has_no_tool_call = len(extract_content_between_tags(content, 'tool_call')) == 0
            if not (has_think and has_answer and has_no_reflection and has_no_tool_call):
                log.append("PATH FAILED: Incorrect block structure for Intuition Success path.")
                return score / max_score if max_score > 0 else 0.0
            log.append("PATH VALIDATED: Correct block structure found.")
            score += 10     # Points for correct path structure
            
            # Content Validation
            answer_content = extract_content_between_tags(content, 'answer')[0]
            try:
                answer_passes = json.loads(answer_content)
                if answer_passes == first_instrcount_passes:
                    score += 10; 
                    log.append("[+10] 'answer' passes match the successful tool call.")
                else: 
                    log.append("[+0] FAILED: 'answer' passes do not match.")
            except json.JSONDecodeError:
                log.append("[+0] FAILED: 'answer' content is not valid JSON.")
            return score / max_score if max_score > 0 else 0.0

        # --- PATH B or C: Reflection or RAG Fallback ---
        else: # first_improvement <= 0
            log.append("\n>>> DETECTED PATH: Reflection or RAG (To be determined)")
            
            # --- Turn 3: Assistant's Reflection ---
            if len(blocks) < 3 or blocks[2]['role'] != 'assistant':
                log.append("PATH FAILED: Assistant's Turn 3 is missing.")
                return score / MAX_SCORE_REFLECTION if MAX_SCORE_REFLECTION > 0 else 0.0

            # Path Structure Validation
            content = blocks[2]['content']
            has_think = len(extract_content_between_tags(content, 'think')) == 1
            has_reflection = len(extract_content_between_tags(content, 'Reflection')) == 1
            has_tool_call = len(extract_content_between_tags(content, 'tool_call')) == 1
            has_no_answer = len(extract_content_between_tags(content, 'answer')) == 0
            if not (has_think and has_reflection and has_tool_call and has_no_answer):
                log.append("PATH FAILED: Incorrect block structure for Reflection step.")
                return score / MAX_SCORE_REFLECTION if MAX_SCORE_REFLECTION > 0 else 0.0
            log.append("PATH VALIDATED: Correct block structure for Reflection step.")
            score += 15     # Points for correct reflection structure
            
            # Content Validation
            tool_calls = extract_content_between_tags(content, 'tool_call')
            try:
                call_data = json.loads(tool_calls[0])
                if call_data.get('name') == 'instrcount':
                    passes = call_data.get('arguments', {}).get('optimization_flags')
                    if validate_pass_sequence(passes):
                        second_instrcount_passes = passes
                        score += 10; 
                        log.append("[+10] Second 'instrcount' tool call is valid.")
                    else: 
                        log.append("[+0] FAILED: Second tool call has invalid passes.")
                else: 
                    log.append("[+0] FAILED: Expected 'instrcount' tool call, found another.")
            except json.JSONDecodeError:
                log.append("[+0] FAILED: Second tool_call is malformed.")

            # --- Turn 4: User's Response to Second Tool ---
            if len(blocks) < 4 or blocks[3]['role'] != 'user':
                log.append("PATH FAILED: User's Turn 4 is missing.")
                return score / MAX_SCORE_REFLECTION if MAX_SCORE_REFLECTION > 0 else 0.0
            
            content = blocks[3]['content']
            responses = extract_content_between_tags(content, 'tool_response')
            if responses and len(responses) == 1:
                try:
                    response_data = json.loads(responses[0])
                    improvement = response_data.get('improvement_over_oz')
                    if isinstance(improvement, (int, float)):
                        second_improvement = improvement
                        score += 5; 
                        log.append("[+5] Second tool_response is valid.")
                    else: 
                        log.append("[+0] FAILED: Second 'improvement_over_oz' missing.")
                except json.JSONDecodeError:
                    log.append("[+0] FAILED: Second tool_response is malformed.")
            else: log.append("[+0] FAILED: Incorrect number of tool_responses in Turn 4.")
            
            if second_improvement is None:
                log.append("CRITICAL FAILURE: Cannot determine sub-path due to invalid second tool response.")
                return score / MAX_SCORE_REFLECTION if MAX_SCORE_REFLECTION > 0 else 0.0

            # --- PATH B: Reflection Success ---
            if second_improvement > 0:
                max_score = MAX_SCORE_REFLECTION
                log.append(f"\n>>> CONFIRMED PATH: Reflection Success (Max Score: {max_score})")

                if len(blocks) < 5 or blocks[4]['role'] != 'assistant':
                    log.append("PATH FAILED: Assistant's Turn 5 is missing.")
                    return score / max_score if max_score > 0 else 0.0
                
                # Path Structure Validation
                content = blocks[4]['content']
                has_think = len(extract_content_between_tags(content, 'think')) == 1
                has_answer = len(extract_content_between_tags(content, 'answer')) == 1
                has_no_other_tags = len(extract_content_between_tags(content, 'Reflection')) + len(extract_content_between_tags(content, 'tool_call')) == 0
                if not (has_think and has_answer and has_no_other_tags):
                    log.append("PATH FAILED: Incorrect block structure for Reflection Success.")
                    return score / max_score if max_score > 0 else 0.0
                log.append("PATH VALIDATED: Correct block structure found.")
                score += 10     # Points for correct path structure
                
                # Content Validation
                answer_content = extract_content_between_tags(content, 'answer')[0]
                try:
                    answer_passes = json.loads(answer_content)
                    if answer_passes == second_instrcount_passes:
                        score += 10; 
                        log.append("[+10] 'answer' passes match second successful call.")
                    else: 
                        log.append("[+0] FAILED: 'answer' passes do not match.")
                except json.JSONDecodeError:
                    log.append("[+0] FAILED: 'answer' content is not valid JSON.")
                return score / max_score if max_score > 0 else 0.0
            
            # --- PATH C: RAG Fallback ---
            else: # second_improvement <= 0
                max_score = MAX_SCORE_RAG
                log.append(f"\n>>> CONFIRMED PATH: RAG Fallback (Max Score: {max_score})")
                
                # --- Turn 5: Assistant's RAG Tool Call ---
                if len(blocks) < 5 or blocks[4]['role'] != 'assistant':
                    log.append("PATH FAILED: Assistant's Turn 5 is missing.")
                    return score / max_score if max_score > 0 else 0.0
                
                # Path Structure Validation
                content = blocks[4]['content']
                has_think = len(extract_content_between_tags(content, 'think')) == 1
                has_tool_call = len(extract_content_between_tags(content, 'tool_call')) == 1
                has_no_other_tags = len(extract_content_between_tags(content, 'Reflection')) + len(extract_content_between_tags(content, 'answer')) == 0
                if not (has_think and has_tool_call and has_no_other_tags):
                    log.append("PATH FAILED: Incorrect block structure for RAG tool call.")
                    return score / max_score if max_score > 0 else 0.0
                log.append("PATH VALIDATED: Correct block structure for RAG call.")
                score += 10 # Points for correct path structure
                
                # Content Validation
                tool_calls = extract_content_between_tags(content, 'tool_call')
                try:
                    call_data = json.loads(tool_calls[0])
                    if call_data.get('name') == 'lightrag_compiler_optimization':   # TODO: 修改名称
                        score += 10; 
                        log.append("[+10] RAG tool call is valid.")
                    else: 
                        log.append("[+0] FAILED: Expected RAG tool call.")
                except json.JSONDecodeError:
                    log.append("[+0] FAILED: RAG tool_call is malformed.")
                
                # --- Turn 6: User's RAG Response ---
                if len(blocks) < 6 or blocks[5]['role'] != 'user':
                    log.append("PATH FAILED: User's RAG response (Turn 6) is missing.")
                    return score / max_score if max_score > 0 else 0.0

                content = blocks[5]['content']
                responses = extract_content_between_tags(content, 'tool_response')
                if responses and len(responses) == 1:
                    rag_passes = extract_passes_from_rag_response(responses[0])
                    if rag_passes:
                        score += 15; 
                        log.append("[+15] Valid RAG tool response found.")
                    else: 
                        log.append("[+0] FAILED: RAG response format incorrect.")
                else: 
                    log.append("[+0] FAILED: RAG tool response missing.")

                # --- Turn 7: Assistant's Final Answer from RAG ---
                if len(blocks) < 7 or blocks[6]['role'] != 'assistant':
                    log.append("PATH FAILED: Assistant's final answer (Turn 7) is missing.")
                    return score / max_score if max_score > 0 else 0.0
                
                content = blocks[6]['content']
                has_think = len(extract_content_between_tags(content, 'think')) == 1
                has_answer = len(extract_content_between_tags(content, 'answer')) == 1
                has_no_other_tags = len(extract_content_between_tags(content, 'Reflection')) + len(extract_content_between_tags(content, 'tool_call')) == 0
                if not (has_think and has_answer and has_no_other_tags):
                    log.append("PATH FAILED: Incorrect block structure for final answer.")
                    return score / max_score if max_score > 0 else 0.0
                
                log.append("PATH VALIDATED: Correct block structure for final answer.")
                score += 5 # Points for correct structure

                answer_content = extract_content_between_tags(content, 'answer')[0]
                try:
                    answer_passes = json.loads(answer_content)
                    if rag_passes and answer_passes == rag_passes:
                        score += 10; log.append("[+10] Final answer matches RAG passes.")
                    else: log.append("[+0] FAILED: Final answer does not match RAG passes.")
                except json.JSONDecodeError:
                    log.append("[+0] FAILED: Final answer is malformed.")
                return score / max_score if max_score > 0 else 0.0

    except Exception as e:
        log.append(f"An unexpected error occurred during scoring: {e}")
        return score / max_score if max_score > 0 else 0.0
    finally:
        print("\n".join(log))
    
    # Default return value if no path is matched
    return score / max_score if max_score > 0 else 0.0


def extract_answer_content(text: str) -> Optional[List[str]]:
    """Extract and parse answer content"""
    # Find all assistant blocks to ensure we get the final answer
    assistant_blocks = re.findall(r"<\|im_start\|>\s*assistant\s*\n?(.*?)<\|im_end\|>", text, re.DOTALL)
    if not assistant_blocks:
        return None

    # The final answer should be in the last assistant block
    last_block = assistant_blocks[-1]
    answer_matches = extract_content_between_tags(last_block, 'answer')
    if not answer_matches:
        return None
        
    answer_content = answer_matches[-1]
    
    try:
        # Try to parse as JSON
        parsed_answer = json.loads(answer_content)
        if validate_pass_sequence(parsed_answer):
            return parsed_answer
    except (json.JSONDecodeError, TypeError):
         pass # Fall through to other methods
            
    # Try to parse as a Python literal list string (e.g., "['--pass1', '--pass2']")
    try:
        parsed_answer = ast.literal_eval(answer_content)
        if validate_pass_sequence(parsed_answer):
            return parsed_answer
    except (ValueError, SyntaxError, TypeError):
        pass

    return None

# --- Remaining Functions (Unchanged, but necessary) ---

def compute_score_answer(solution_str: Optional[str], ground_truth: Optional[Union[str, List[str]]]) -> float:
    """Compute the answer reward score based on the overOz value."""
    if solution_str is None or ground_truth is None:
        return 0.0
    
    try:
        # Get the filename from ground_truth
        filename = ground_truth if isinstance(ground_truth, str) else ground_truth[0]
        ll_file_path = os.path.join(os.path.dirname(__file__) + "/../../../examples/data_preprocess/llvmir_datasets/", filename)
        ll_code = read_llvm_ir_file(ll_file_path)
        
        if not ll_code:
            # print(f"[DEBUG] Could not read LLVM IR file for ground truth: {filename}")
            return 0.0
        
        # Extract pass sequence from the final answer tag
        pass_list = extract_answer_content(solution_str)
        
        if not pass_list:
            # print("[DEBUG] No valid pass list found in the answer.")
            return -30.0 # Penalize heavily for no valid answer
        
        # Calculate overOz using the extracted passes
        llvm_tools_path = os.path.join(os.path.dirname(__file__), 
                                     '../../../agent_r1/tool/tools/comiler_autotuning/raw_tool/')
        
        overoz = get_overOz(ll_code, pass_list, llvm_tools_path=llvm_tools_path)
        print(f"[DEBUG] pass_list: {pass_list}, overOz: {overoz}")
        
        # Scale the reward
        reward = overoz * 10
        return reward
        
    except Exception as e:
        # print(f"[DEBUG] Error in compute_score_answer: {e}")
        return 0.0


def compute_score_format_answer(solution_str: str, ground_truth: Union[str, List[str]]) -> float:
    """Compute the total reward score combining format and answer scores."""
    if solution_str is None or ground_truth is None:
        return 0.0
    
    try:
        # Calculate individual scores
        format_reward = compute_score_format(solution_str)
        answer_reward = compute_score_answer(solution_str, ground_truth)
        print(f"[DEBUG] Format reward: {format_reward:.3f}, Answer reward: {answer_reward:.3f}")
        
        # Combine scores. The prompt implies format is critical, so we give it some weight.
        # If format is perfect (1.0), full answer reward is possible. If format is bad (e.g., < 0.5), we penalize.
        # This implementation uses a simple weighting scheme as before.
        if format_reward != None and answer_reward != None:
            total_reward = 0.5 * format_reward + 0.5 * answer_reward
        else:
            total_reward = -30.0
        
        return total_reward
        
    except Exception as e:
        print(f"[DEBUG] Error in compute_score_format_answer: {e}")
        return 0.0

# Legacy functions for potential backward compatibility, but their logic has been
# superseded by the more robust methods above.
def extract_answer(solution_str: str) -> str:
    """Extract the answer from the solution string."""
    answer_content = extract_answer_content(solution_str)
    return json.dumps(answer_content) if answer_content else ""


question = '''

<|im_start|>assistant
<Intuition>
Looking at the autophase features, I can see:
- Total instructions: 809
- Total blocks: 138
- Memory instructions: 485
- Branch count: 127

Based on the high memory instruction count, I'll prioritize -mem2reg and -licm optimizations. Reduce call instructions with -simplifycfg. After memory optimizations, store/reg reuse reduces future overhead. Dispatch simple unary ops to -inline. Point to BB03Phi for possible constant propagation if non-zero.
</Intuition>

<tool_call>
{"name": "instrcount", "arguments": {"filename": "tensorflow-v0_1606.ll", "optimization_flags": ["--indvars", "--loop-simplifycfg", "--aggressive-instcombine", "--loop-load-elim", "--sroa", "--lower-guard-intrinsic", "--loop-vectorize", "--post-inline-ee-instrument", "--simple-loop-unswitch", "--loop-interchange", "--elim-avail-extern", "--lower-guard-intrinsic", "--coro-cleanup", "--lower-expect", "--lower-matrix-intrinsics", "--loop-load-elim", "--mem2reg", "--gvn-gcse", "--dce", "--mldst-motion", "--flattencfg", "--dse", "--prune-eh", "--reassociate", "--redundant-dbg-inst-elim"]}}
</tool_call><|im_end|>
<|im_start|>user
<tool_response>
{"filename": "/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/tensorflow-v0_1606.ll", "status": "success", "improvement_over_oz": -0.12376237623762376}
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
{"filename": "/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/tensorflow-v0_1606.ll", "status": "success", "improvement_over_oz": -4.207920792079208}
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

print(compute_score_format(question))
# print(compute_score_format_answer(question))