import pandas as pd
import requests
import json
import subprocess
import re
import io
import os
from pathlib import Path
import ctypes

LLVM_IR_DIR = './examples/data_preprocess/llvmir_datasets'
DATASET_DIR = './dataset/rl/'
DATASETS = [
    "rl_validation_cbench-v1.parquet",
    "rl_validation_mibench-v1.parquet",
    "rl_validation_blas-v0.parquet",
    "rl_validation_opencv-v0.parquet",
    "rl_validation_chstone-v0.parquet",
    "rl_validation_tensorflow-v0.parquet",
    "rl_validation_npb-v0.parquet"
]
# DATASETS = ["rl_validation_cbench-v1.parquet"]

# 支持本地或远程API，模型名和URL可灵活配置
API_URL = 'xxx'  # 或远程API
API_KEY = 'xxx'
API_VLLM_URL = 'http://localhost:18888/v1' # VLLM Qwen
API_VLLM_KEY = 'EMPTY'
API_VLLM_MODEL = 'Qwen/Qwen2.5-1.5B-Instruct'
# MODEL_NAME = 'gpt-5'
# 'DeepSeek-V3'
# 'tencent/Hunyuan-A13B-Instruct'
# 'Qwen/Qwen3-235B-A22B-Instruct-2507',
# 'Qwen/Qwen3-Coder-480B-A35B-Instruct',
# 'Tongyi-Zhiwen/QwenLong-L1-32B',
# 'gemini-2.5-pro'
# 'zai-org/GLM-4.5'
# 'claude-opus-4-20250514'
# 'moonshotai/Kimi-Dev-72B'
MODEL_LIST = [
    'gpt-5'
]
# 'baidu/ERNIE-4.5-300B-A47B'
# MiniMaxAI/MiniMax-M1-80k
# gpt-5-mini


class InstCountDataStruct(ctypes.Structure):
    _fields_ = [("name", ctypes.c_char * 64), ("value", ctypes.c_int)]

def get_inst_count_obs(ir_file_path, llvm_version="llvm-10.0.0"):
    project_directory = os.path.dirname(os.path.abspath(__file__))
    library_path = None
    library_path = "./agent_r1/tool/tools/comiler_autotuning/raw_tool/libInstCount_10_0_0.so"
    
    result_array = (InstCountDataStruct * 70)()
    my_cpp_lib = ctypes.CDLL(library_path)
    my_cpp_lib.GetInstCount(ir_file_path.encode(), result_array)

    result_dict = {item.name.decode(): item.value for item in result_array}
    ic_value = result_dict.get('TotalInsts', None)

    return ic_value


def GenerateOptimizedLLCode(input_code, optimization_options, llvm_tools_path=None):
    try:
        opt_path = os.path.join(llvm_tools_path, "opt") if llvm_tools_path else "opt"
        
        # Flatten the optimization options list
        flat_opt_options = [str(item) for sublist in optimization_options for item in (sublist if isinstance(sublist, list) else [sublist])]

        # Use io.StringIO to simulate a file-like object
        input_code_io = io.StringIO()
        input_code_io.write(input_code)
        input_code_io.seek(0)  # Reset the file position to the beginning

        # Prepare the command for subprocess
        cmd_opt = [opt_path] + flat_opt_options + ["-S"]

        # Run the opt command with the given input code
        result = subprocess.run(cmd_opt, input=input_code_io.getvalue(), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # Return the optimized LLVM code
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If there's an error, output the original input code
        # print(f"Error occurred during optimization: {e}")
        # print(f"Standard output: {e.stdout}")
        # print(f"Standard error: {e.stderr}")
        return input_code


def get_instrcount(ll_code, *opt_flags, llvm_tools_path=None):
    if llvm_tools_path is None:
        raise ValueError("llvm_tools_path must be provided")
    after_ll_code = GenerateOptimizedLLCode(ll_code, opt_flags, llvm_tools_path)
    return get_inst_count_obs(after_ll_code, "llvm-10.0.0")


def get_overOz(ll_code, opt_flags, llvm_tools_path=None):
    ic_value = get_instrcount(ll_code, *opt_flags, llvm_tools_path=llvm_tools_path)
    oz_value = get_instrcount(ll_code, [""], llvm_tools_path=llvm_tools_path)
    overoz = (oz_value - ic_value) / oz_value
    return overoz


# TODO:修改输出格式
def call_large_model(formatted_features, model_name, use_vllm = False):
    prompt = (
        "You are a compiler optimization expert. Given the following LLVM IR autophase features:\n"
        f"{json.dumps(formatted_features, indent=2)}\n"
        "Your task: Recommend an LLVM pass sequence to minimize instruction count.\n"
        "Output ONLY a JSON list of optimization passes, each starting with '--', e.g.:\n"
        "[\n  \"--mem2reg\", \"--sroa\", \"--instcombine\", \"--simplifycfg\"\n]\n"
        "Do not include any explanation, comments, or text outside the JSON list."
    )
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    if not use_vllm:
        response = requests.post(API_URL, headers=headers, json=payload)
        try:
            result = response.json()
        except Exception:
            print('API返回非JSON格式:', response.text)
            return []
        print('API返回:', result)
        # 兼容不同API返回格式
        if 'choices' in result and result['choices'] and 'message' in result['choices'][0]:
            answer = result['choices'][0]['message']['content']
        elif 'choices' in result and result['choices'] and 'content' in result['choices'][0]:
            answer = result['choices'][0]['content']
        else:
            print('API响应无choices字段:', result)
            return []
    else:
        from openai import OpenAI
        client = OpenAI(base_url=API_VLLM_URL, api_key=API_VLLM_KEY)
        conversation = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        response = client.chat.completions.create(messages=conversation, model=API_VLLM_MODEL)
        answer = response.choices[0].message.content
    # 提取pass sequence
    try:
        raw_seq = json.loads(answer)
    except Exception:
        raw_seq = []
    # 格式化：补全为['--pass']格式，并去重
    formatted_seq = []
    seen = set()
    for p in raw_seq:
        # 只保留字符串类型
        if isinstance(p, str):
            p = p.strip()
            if not p.startswith('--'):
                p = '--' + p
            if p not in seen:
                formatted_seq.append(p)
                seen.add(p)
    return formatted_seq


def process_parquet_file(parquet_path, output_csv, model_name):
    try:
        df = pd.read_parquet(parquet_path)
    except Exception as e:
        print(f"Failed to read {parquet_path}: {e}")
        return
    print(f"Read {parquet_path} with {len(df)} rows.")
    results = []
    for idx, row in df.iterrows():
        match = re.search(r'```json\n(.*?)\n```', row['question'], re.DOTALL)
        if match:
            formatted_features = json.loads(match.group(1))
        else:
            formatted_features = {}
        print("Processing row", idx)
        program_id = row['ground_truth']
        if not program_id:
            print(f"No program_id found in row {idx}, skip.")
            continue
        pass_sequence = call_large_model(formatted_features, model_name)
        try:
            ll_path = Path(LLVM_IR_DIR) / program_id
            ll_code = ll_path.read_text()
            improvement = get_overOz(ll_code, pass_sequence, llvm_tools_path="./agent_r1/tool/tools/comiler_autotuning/raw_tool/")
        except Exception as e:
            print(f"Error processing {program_id}: {e}")
            improvement = None
        print("Improvement for program", program_id, "with passes", pass_sequence, ":", improvement)
        results.append({
            'program_id': program_id,
            'pass_sequence': pass_sequence,
            'improvement_over_oz': improvement
        })
    pd.DataFrame(results).to_csv(output_csv, index=False)
    print(f'Done! Results saved to {output_csv}')


def main():
    for MODEL_NAME in MODEL_LIST:
        print(f"\n=== Testing model: {MODEL_NAME} ===")
        for dataset_file in DATASETS:
            parquet_path = os.path.join(DATASET_DIR, dataset_file)
            model_short_name = MODEL_NAME.split('/')[-1] if '/' in MODEL_NAME else MODEL_NAME
            output_csv = f'{model_short_name}_results_{dataset_file.replace(".parquet", ".csv")}'
            print(f"\n=== Processing {parquet_path} ===")
            process_parquet_file(parquet_path, output_csv, MODEL_NAME)


if __name__ == '__main__':
    main()