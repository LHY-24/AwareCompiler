import os
import argparse
import pandas as pd
import glob
from pathlib import Path

DEFAULT_RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"
DEFAULT_OUTPUT_CSV_AVG = Path(__file__).resolve().parents[2] / "results" / "model_bench_summary_include_nonzero_pass.csv"
DEFAULT_OUTPUT_CSV_SUCCESS = Path(__file__).resolve().parents[2] / "results" / "model_bench_success_rate_include_nonzero_pass.csv"

# bench名映射（文件名到列名）
BENCH_MAP = {
    'cbench': 'cbench',
    'mibench': 'mibench',
    'blas': 'blas',
    'opencv': 'opencv',
    'chstone': 'chstone',
    'tensorflow': 'tensorflow',
    'npb': 'npb'
}

def get_bench_name(filename):
    for k in BENCH_MAP:
        if k in filename:
            return BENCH_MAP[k]
    return filename

def get_model_name(filename):
    # 取文件名第一个下划线前的部分
    base = os.path.basename(filename)
    return base.split('_')[0]

parser = argparse.ArgumentParser(description='Aggregate LLM baseline result CSVs')
parser.add_argument('--results-dir', type=Path, default=DEFAULT_RESULTS_DIR)
parser.add_argument('--output-csv-avg', type=Path, default=DEFAULT_OUTPUT_CSV_AVG)
parser.add_argument('--output-csv-success', type=Path, default=DEFAULT_OUTPUT_CSV_SUCCESS)
args = parser.parse_args()

# 收集所有结果csv
csv_files = glob.glob(os.path.join(str(args.results_dir), '*.csv'))

# {model: {bench: {'avg': avg, 'success_rate': rate}}}
summary = {}
bench_names = set()

for csv_file in csv_files:
    bench = get_bench_name(csv_file)
    bench_names.add(bench)
    df = pd.read_csv(csv_file)
    # 计算success rate: improvement > 0的程序在所有程序中的比例
    vals = pd.to_numeric(df['improvement_over_oz'], errors='coerce')
    vals = vals.dropna()
    positive_vals = vals[vals > 0]
    total_programs = len(vals)
    success_rate = round(len(positive_vals) / total_programs, 4) if total_programs > 0 else 0.0
    
    # 只统计 pass sequence 不为空的行来计算平均优化效果
    if 'pass_sequence' in df.columns:
        mask = df['pass_sequence'].apply(lambda x: isinstance(x, str) and len(eval(x)) > 0)
        vals_for_avg = df.loc[mask, 'improvement_over_oz']
        vals_for_avg = pd.to_numeric(vals_for_avg, errors='coerce')
        vals_for_avg = vals_for_avg.dropna()
    else:
        # 如果没有pass_sequence列，全部参与
        vals_for_avg = vals
    avg = round(vals_for_avg.mean(), 4) if not vals_for_avg.empty else 0.0
    model = get_model_name(csv_file)
    if model not in summary:
        summary[model] = {}
    summary[model][bench] = {'avg': avg, 'success_rate': success_rate}

# 构造输出表 - 平均优化效果
bench_names = sorted(list(bench_names))
avg_rows = []
success_rows = []
for model in sorted(summary.keys()):
    avg_row = {'model': model}
    success_row = {'model': model}
    bench_scores = []
    bench_success_rates = []
    for bench in bench_names:
        bench_data = summary[model].get(bench, {'avg': 0.0, 'success_rate': 0.0})
        score = bench_data['avg']
        success_rate = bench_data['success_rate']
        avg_row[bench] = score
        success_row[bench] = success_rate
        bench_scores.append(score)
        bench_success_rates.append(success_rate)
    # 计算该模型所有 bench 的平均分和平均成功率
    avg_row['average'] = round(sum(bench_scores) / len(bench_scores), 4) if bench_scores else 0.0
    success_row['average'] = round(sum(bench_success_rates) / len(bench_success_rates), 4) if bench_success_rates else 0.0
    avg_rows.append(avg_row)
    success_rows.append(success_row)

# 输出平均优化效果表
avg_df = pd.DataFrame(avg_rows)
avg_df.set_index('model', inplace=True)
avg_df.to_csv(args.output_csv_avg)
print(f'Average improvement summary saved to {args.output_csv_avg}')
print("Average Improvement:")
print(avg_df)

# 输出成功率表
success_df = pd.DataFrame(success_rows)
success_df.set_index('model', inplace=True)
success_df.to_csv(args.output_csv_success)
print(f'\nSuccess rate summary saved to {args.output_csv_success}')
print("Success Rate:")
print(success_df)
