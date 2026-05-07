import os
import pandas as pd
import glob

RESULTS_DIR = './results/'
OUTPUT_CSV = 'model_bench_summary.csv'

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

# 收集所有结果csv
csv_files = glob.glob(os.path.join(RESULTS_DIR, '*.csv'))

# {model: {bench: avg}}
summary = {}
bench_names = set()

for csv_file in csv_files:
    bench = get_bench_name(csv_file)
    bench_names.add(bench)
    df = pd.read_csv(csv_file)
    # 只统计非0且非空的improvement_over_oz
    vals = df['improvement_over_oz']
    vals = pd.to_numeric(vals, errors='coerce')
    vals = vals[vals != 0]
    vals = vals.dropna()
    avg = round(vals.mean(), 4) if not vals.empty else 0.0
    model = get_model_name(csv_file)
    if model not in summary:
        summary[model] = {}
    summary[model][bench] = avg

# 构造输出表
bench_names = sorted(list(bench_names))
rows = []
for model in sorted(summary.keys()):
    row = {'model': model}
    bench_scores = []
    for bench in bench_names:
        score = summary[model].get(bench, 0.0)
        row[bench] = score
        bench_scores.append(score)
    # 计算该模型所有 bench 的平均分
    row['average'] = round(sum(bench_scores) / len(bench_scores), 4) if bench_scores else 0.0
    rows.append(row)

out_df = pd.DataFrame(rows)
out_df.set_index('model', inplace=True)
out_df.to_csv(OUTPUT_CSV)
print(f'Summary saved to {OUTPUT_CSV}')
print(out_df)
