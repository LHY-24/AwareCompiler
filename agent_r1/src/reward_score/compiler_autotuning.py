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
    """Validate if pass sequence is correctly formatted"""
    if not isinstance(pass_seq, list):
        return False
    
    for pass_item in pass_seq:
        if not isinstance(pass_item, str):
            return False
        # Pass must start with "--" or be "-Oz"
        if not (pass_item.startswith('--') or pass_item == '-Oz'):
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
    
def extract_passes_from_rag_response(rag_response_text: str) -> Optional[List[str]]:
    """Extracts the pass sequence from the RAG tool's markdown/JSON response."""
    # Regex to find the JSON block for the optimal pass sequence
    pattern = re.compile(r"\*\*Optimal Pass Sequence for this Program:\*\*\s*```json\s*(.*?)\s*```", re.DOTALL)
    match = pattern.search(rag_response_text)
    if not match:
        return None
    
    json_str = match.group(1).strip()
    try:
        passes = json.loads(json_str)
        if validate_pass_sequence(passes):
            return passes
        return None
    except json.JSONDecodeError:
        return None

# --- Core Scoring Logic (Rewritten) ---

def compute_score_format(text: str) -> float:
    """
    Compute format score based on the strict SFT workflow requirements.

    Args:
        text: The solution text to evaluate

    Returns:
        Format score (0.0 to 1.0, where 1.0 is perfect)
    """
    if not text or not isinstance(text, str):
        return 0.0

    score = 0.0
    max_score = 0.0
    log = []

    try:
        blocks = extract_conversation_blocks(text)
        if not blocks:
            return 0.0

        # --- Turn 1: Assistant's Initial Move ---
        max_score += 30 # Points for the first assistant turn
        log.append("\n--- Validating Turn 1 (Assistant) ---")
        if len(blocks) > 0 and blocks[0]['role'] == 'assistant':
            content = blocks[0]['content']
            
            # 1.1: Check <Intuition> tag and its specific content
            intuition_content = extract_content_between_tags(content, 'Intuition')
            intuition_pattern = r"Looking at the autophase features, I can see:.*?Total instructions:.*?Total blocks:.*?Memory instructions:.*?Branch count:.*?Based on these characteristics, I'll formulate a strong initial optimization sequence\. Let me call the instrcount tool to check the performance\."
            if intuition_content and re.search(intuition_pattern, intuition_content[0], re.DOTALL):
                score += 10
                log.append("[+10] Intuition tag found with correct boilerplate text.")
            else:
                log.append("[+0] FAILED: Intuition tag missing or content incorrect.")

            # 1.2: Check first <tool_call> for instrcount
            tool_calls = extract_content_between_tags(content, 'tool_call')
            if tool_calls:
                try:
                    call_data = json.loads(tool_calls[0])
                    if call_data.get('name') == 'instrcount':
                        score += 5
                        log.append("[+5] First tool call is 'instrcount'.")
                        args = call_data.get('arguments', {})
                        filename = args.get('filename')
                        passes = args.get('optimization_flags')
                        
                        if filename and isinstance(filename, str): # and check_filename_exists(filename):
                            # Filename check is commented out as it relies on a specific file structure
                            # that might not be available in all evaluation environments.
                            # We will trust the format for now.
                            score += 5
                            log.append(f"[+5] Filename '{filename}' is present.")
                        else:
                             log.append(f"[+0] FAILED: Filename is missing or invalid.")
                        
                        if validate_pass_sequence(passes):
                            score += 10
                            log.append("[+10] 'optimization_flags' is a valid pass sequence.")
                            first_instrcount_passes = passes
                        else:
                            log.append("[+0] FAILED: 'optimization_flags' is not a valid pass sequence.")
                            return score / max_score
                    else:
                        log.append("[+0] FAILED: First tool call is not 'instrcount'.")
                        return score / max_score
                except json.JSONDecodeError:
                    log.append("[+0] FAILED: First tool_call content is not valid JSON.")
                    return score / max_score
            else:
                log.append("[+0] FAILED: First tool_call tag is missing.")
                return score / max_score
        else:
            log.append("[+0] FAILED: First conversation block is not from assistant.")
            return score / max_score

        # --- Turn 2: User's Response (First Tool) ---
        max_score += 10
        log.append("\n--- Validating Turn 2 (User) ---")
        if len(blocks) > 1 and blocks[1]['role'] == 'user':
            content = blocks[1]['content']
            responses = extract_content_between_tags(content, 'tool_response')
            if responses:
                try:
                    response_data = json.loads(responses[0])
                    improvement = response_data.get('improvement_over_oz')
                    if isinstance(improvement, (int, float)):
                        score += 10
                        log.append(f"[+10] First tool_response is valid JSON with 'improvement_over_oz': {improvement}.")
                        first_improvement = improvement
                    else:
                        log.append("[+0] FAILED: 'improvement_over_oz' missing or not a number.")
                        return score / max_score
                except json.JSONDecodeError:
                    log.append("[+0] FAILED: First tool_response content is not valid JSON.")
                    return score / max_score
            else:
                log.append("[+0] FAILED: First tool_response tag missing.")
                return score / max_score
        else:
            log.append("[+0] FAILED: Second conversation block is not from user.")
            return score / max_score

        # --- Turn 3: Assistant's Reaction & Next Step ---
        max_score += 25
        log.append("\n--- Validating Turn 3 (Assistant) ---")
        if len(blocks) > 2 and blocks[2]['role'] == 'assistant':
            content = blocks[2]['content']
            think_content = extract_content_between_tags(content, 'think')
            
            # SCENARIO 1: Fast Thinking Success
            if first_improvement > 0:
                log.append(">>> DETECTED SCENARIO: Fast Thinking Success")
                expected_think = "Great! The instrcount tool reports an improvement_over_oz"
                if think_content and expected_think in think_content[0]:
                    score += 10
                    log.append("[+10] 'think' content matches success pattern.")
                else:
                    log.append("[+0] FAILED: 'think' content does not match success pattern.")
                
                answer_content = extract_content_between_tags(content, 'answer')
                if answer_content:
                    try:
                        answer_passes = json.loads(answer_content[0])
                        if validate_pass_sequence(answer_passes):
                            score += 5
                            log.append("[+5] 'answer' tag found with valid pass sequence.")
                            if answer_passes == first_instrcount_passes:
                                score += 10
                                log.append("[+10] 'answer' passes match the first successful tool call.")
                            else:
                                log.append("[+0] FAILED: 'answer' passes do not match tool call.")
                        else:
                            log.append("[+0] FAILED: 'answer' content is not a valid pass sequence.")
                    except json.JSONDecodeError:
                        log.append("[+0] FAILED: 'answer' content is not valid JSON.")
                else:
                    log.append("[+0] FAILED: 'answer' tag missing.")
                return score / max_score

            # SCENARIO 2/3: Reflection Path
            else: # first_improvement <= 0
                log.append(">>> DETECTED SCENARIO: Reflection or RAG Fallback")
                expected_think = "The instrcount tool reports an improvement_over_oz"
                if think_content and expected_think in think_content[0]:
                    score += 5
                    log.append("[+5] 'think' content matches failure pattern.")
                else:
                    log.append("[+0] FAILED: 'think' content does not match failure pattern.")

                if extract_content_between_tags(content, 'Reflection'):
                    score += 5
                    log.append("[+5] 'Reflection' tag found after first failure.")
                else:
                    log.append("[+0] FAILED: 'Reflection' tag missing.")

                # Check for second instrcount tool call
                tool_calls = extract_content_between_tags(content, 'tool_call')
                if len(tool_calls) > 0:
                    try:
                        call_data = json.loads(tool_calls[-1]) # Check the last tool call in this block
                        if call_data.get('name') == 'instrcount' and validate_pass_sequence(call_data.get('arguments', {}).get('optimization_flags')):
                            score += 15
                            log.append("[+15] Second 'instrcount' tool call is valid.")
                            second_instrcount_passes = call_data['arguments']['optimization_flags']
                        else:
                            log.append("[+0] FAILED: Second 'instrcount' tool call is invalid.")
                            return score / max_score
                    except (json.JSONDecodeError, IndexError):
                        log.append("[+0] FAILED: Second tool_call is malformed.")
                        return score / max_score
                else:
                    log.append("[+0] FAILED: Second tool_call missing.")
                    return score / max_score
        else:
            log.append("[+0] FAILED: Third conversation block is not from assistant.")
            return score / max_score
            
        # --- Turn 4: User's Response (Second Tool) ---
        max_score += 10
        log.append("\n--- Validating Turn 4 (User) ---")
        if len(blocks) > 3 and blocks[3]['role'] == 'user':
            content = blocks[3]['content']
            responses = extract_content_between_tags(content, 'tool_response')
            if responses:
                try:
                    response_data = json.loads(responses[0])
                    improvement = response_data.get('improvement_over_oz')
                    if isinstance(improvement, (int, float)):
                        score += 10
                        log.append(f"[+10] Second tool_response is valid with 'improvement_over_oz': {improvement}.")
                        second_improvement = improvement
                    else:
                        log.append("[+0] FAILED: Second 'improvement_over_oz' missing or not a number.")
                        return score / max_score
                except json.JSONDecodeError:
                    log.append("[+0] FAILED: Second tool_response content is not valid JSON.")
                    return score / max_score
            else:
                log.append("[+0] FAILED: Second tool_response tag missing.")
                return score / max_score
        else:
            log.append("[+0] FAILED: Fourth conversation block is not from user.")
            return score / max_score

        # --- Turn 5: Assistant's Final Decision ---
        max_score += 25
        log.append("\n--- Validating Turn 5 (Assistant) ---")
        if len(blocks) > 4 and blocks[4]['role'] == 'assistant':
            content = blocks[4]['content']
            think_content = extract_content_between_tags(content, 'think')
            
            # SCENARIO 2: Reflection Success
            if second_improvement > 0:
                log.append(">>> CONFIRMED SCENARIO: Reflection Success")
                expected_think = "Excellent! After reflection, the refined sequence achieves"
                if think_content and expected_think in think_content[0]:
                    score += 10
                    log.append("[+10] 'think' content matches reflection success pattern.")
                else:
                    log.append("[+0] FAILED: 'think' content for reflection success is incorrect.")
                
                answer_content = extract_content_between_tags(content, 'answer')
                if answer_content:
                    try:
                        answer_passes = json.loads(answer_content[0])
                        if validate_pass_sequence(answer_passes):
                            score += 5
                            log.append("[+5] 'answer' tag found with valid pass sequence.")
                            if answer_passes == second_instrcount_passes:
                                score += 10
                                log.append("[+10] 'answer' passes match the second successful tool call.")
                            else:
                                log.append("[+0] FAILED: 'answer' passes do not match second tool call.")
                        else:
                            log.append("[+0] FAILED: 'answer' content is not a valid pass sequence.")
                    except json.JSONDecodeError:
                        log.append("[+0] FAILED: 'answer' content is not valid JSON.")
                else:
                    log.append("[+0] FAILED: 'answer' tag missing.")
                return score / max_score

            # SCENARIO 3: RAG Fallback Path
            else: # second_improvement <= 0
                log.append(">>> CONFIRMED SCENARIO: RAG Fallback")
                expected_think = "The refined sequence still achieves an improvement_over_oz"
                if think_content and expected_think in think_content[0]:
                    score += 5
                    log.append("[+5] 'think' content matches second failure pattern for RAG fallback.")
                else:
                    log.append("[+0] FAILED: 'think' content for RAG fallback is incorrect.")
                
                tool_calls = extract_content_between_tags(content, 'tool_call')
                if tool_calls:
                    try:
                        call_data = json.loads(tool_calls[0])
                        if call_data.get('name') == 'lightrag_compiler_optimization' and isinstance(call_data.get('arguments', {}).get('query'), str):
                            score += 10
                            log.append("[+10] 'lightrag_compiler_optimization' tool call is valid.")
                        else:
                            log.append("[+0] FAILED: RAG tool call is invalid.")
                            return score / max_score
                    except json.JSONDecodeError:
                         log.append("[+0] FAILED: RAG tool_call is malformed.")
                         return score / max_score
                else:
                    log.append("[+0] FAILED: RAG tool_call is missing.")
                    return score / max_score
                
                # We need to look for a RAG response and final answer in the next turns.
                # --- Turn 6: User's RAG Response ---
                max_score += 15
                log.append("\n--- Validating Turn 6 (User - RAG Response) ---")
                if len(blocks) > 5 and blocks[5]['role'] == 'user':
                    content_rag_resp = blocks[5]['content']
                    rag_responses = extract_content_between_tags(content_rag_resp, 'tool_response')
                    if rag_responses:
                        rag_passes = extract_passes_from_rag_response(rag_responses[0])
                        if rag_passes:
                            score += 15
                            log.append("[+15] RAG tool_response found with an extractable pass sequence.")
                        else:
                            log.append("[+0] FAILED: RAG tool_response format incorrect or no passes found.")
                            return score / max_score
                    else:
                        log.append("[+0] FAILED: RAG tool_response tag missing.")
                        return score / max_score
                else:
                    log.append("[+0] FAILED: Sixth conversation block (RAG response) missing or not from user.")
                    return score / max_score

                # --- Turn 7: Assistant's Final Answer from RAG ---
                max_score += 15
                log.append("\n--- Validating Turn 7 (Assistant - RAG Answer) ---")
                if len(blocks) > 6 and blocks[6]['role'] == 'assistant':
                    content_rag_ans = blocks[6]['content']
                    think_content_rag = extract_content_between_tags(content_rag_ans, 'think')
                    expected_think = "Based on the RAG knowledge base retrieval"
                    if think_content_rag and expected_think in think_content_rag[0]:
                        score += 5
                        log.append("[+5] Post-RAG 'think' content is correct.")
                    else:
                        log.append("[+0] FAILED: Post-RAG 'think' content is incorrect.")
                    
                    answer_content = extract_content_between_tags(content_rag_ans, 'answer')
                    if answer_content:
                        try:
                            answer_passes = json.loads(answer_content[0])
                            if answer_passes == rag_passes:
                                score += 10
                                log.append("[+10] Final 'answer' matches the passes from the RAG response.")
                            else:
                                log.append("[+0] FAILED: Final 'answer' does not match RAG passes.")
                        except json.JSONDecodeError:
                            log.append("[+0] FAILED: Final 'answer' is not valid JSON.")
                    else:
                        log.append("[+0] FAILED: Final 'answer' tag missing.")
                    return score / max_score
                else:
                    log.append("[+0] FAILED: Seventh conversation block (RAG answer) missing or not from assistant.")
                    return score / max_score
        else:
            log.append("[+0] FAILED: Fifth conversation block missing or not from assistant.")
            return score / max_score

    except Exception as e:
        log.append(f"An unexpected error occurred during scoring: {e}")
    finally:
        print("\n".join(log)) # Uncomment for detailed debugging
        final_score = score / max_score if max_score > 0 else 0.0
        # print(f"[DEBUG] Final Format Score: {score}/{max_score} = {final_score:.3f}")
        return final_score


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
        total_reward = 0.5 * format_reward + 0.5 * answer_reward
        
        return total_reward
        
    except Exception as e:
        # print(f"[DEBUG] Error in compute_score_format_answer: {e}")
        return 0.0

# Legacy functions for potential backward compatibility, but their logic has been
# superseded by the more robust methods above.
def extract_answer(solution_str: str) -> str:
    """Extract the answer from the solution string."""
    answer_content = extract_answer_content(solution_str)
    return json.dumps(answer_content) if answer_content else ""