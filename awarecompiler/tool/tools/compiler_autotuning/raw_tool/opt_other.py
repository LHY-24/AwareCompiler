from get_instrcount import get_overOz
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_file(ll_path, opt_flags, llvm_tools_path):
    """处理单个 ll 文件，返回 overOz"""
    try:
        with open(ll_path, "r", encoding="utf-8") as f:
            ll_code = f.read()
        overoz = get_overOz(ll_code, opt_flags, llvm_tools_path=llvm_tools_path)
        return overoz
    except Exception as e:
        print(f"[Warning] Failed on {ll_path}: {e}")
        return None


def compute_avg_overoz(base_dir, opt_flags, llvm_tools_path=None, max_workers=8):
    results = {}

    # 遍历每个子文件夹（数据集）
    for dataset_name in os.listdir(base_dir):
        dataset_path = os.path.join(base_dir, dataset_name)
        if not os.path.isdir(dataset_path):
            continue

        ll_files = [
            os.path.join(dataset_path, fname)
            for fname in os.listdir(dataset_path)
            if fname.endswith(".ll")
        ]

        overoz_values = []

        # 多线程处理每个 ll 文件
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(process_file, ll_path, opt_flags, llvm_tools_path): ll_path
                for ll_path in ll_files
            }

            for future in as_completed(future_to_file):
                result = future.result()
                if result is not None:
                    overoz_values.append(result)

        avg_overoz = sum(overoz_values) / len(overoz_values) if overoz_values else None
        results[dataset_name] = avg_overoz

    return results


if __name__ == "__main__":
    base_dir = "<repo_root>/examples/data_preprocess/llvmir_datasets/test"
    opt_flags = ["-Oz"]  # 举例
    llvm_tools_path = "./"
    max_workers = 16  # 线程数，可以根据机器 CPU 核心数调整

    results = compute_avg_overoz(base_dir, opt_flags, llvm_tools_path, max_workers)

    for dataset, avg_val in results.items():
        print(f"{dataset}: {avg_val}")
