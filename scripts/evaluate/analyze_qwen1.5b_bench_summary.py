import os
import pandas as pd
import glob
import ast
import math

RESULTS_DIR = './qwen7b-result/'
OUTPUT_CSV = 'qwen7b_bench_summary_include_nonzero_pass.csv'

# 数据集名关键词
BENCH_KEYS = ['cbench', 'mibench', 'blas', 'opencv', 'chstone', 'tensorflow', 'npb']

def get_bench_name(filename):
    for k in BENCH_KEYS:
        if k in filename:
            return k
    return 'unknown'

# 收集所有结果csv
csv_files = glob.glob(os.path.join(RESULTS_DIR, '*.csv'))

bench_stats = {}
bench_total = {}
bench_valid = {}

for csv_file in csv_files:
    bench = get_bench_name(csv_file)
    if bench not in bench_stats:
        bench_stats[bench] = []
        bench_total[bench] = 0
        bench_valid[bench] = 0
    df = pd.read_csv(csv_file)
    if 'pass_sequence' in df.columns and 'improvement_over_oz' in df.columns:
        for _, row in df.iterrows():
            try:
                seq = row['pass_sequence']
                # 兼容字符串和直接list
                if isinstance(seq, str):
                    seq_list = ast.literal_eval(seq)
                else:
                    seq_list = seq
                if isinstance(seq_list, list) and len(seq_list) > 0:
                    try:
                        val = float(row['improvement_over_oz'])
                        bench_stats[bench].append(val)
                        if val > 0:
                            bench_valid[bench] += 1
                    except Exception:
                        pass
            except Exception:
                pass
            bench_total[bench] += 1
print("Bench stats collected:", bench_stats)
print("Bench total counts:", bench_total)
print("Bench valid counts:", bench_valid)

# 输出表格
rows = []
for bench in BENCH_KEYS:
    if bench in bench_stats and bench_valid[bench] > 0:
        valid_vals = [v for v in bench_stats[bench] if v is not None and not (isinstance(v, float) and math.isnan(v))]
        avg = round(sum(valid_vals) / len(valid_vals), 4) if valid_vals else 0.0
        success_rate = round(bench_valid[bench] / bench_total[bench], 4) if bench_total[bench] > 0 else 0.0
        print(f"Bench {bench}: avg_improvement={avg}, success_rate={success_rate}")
        rows.append({'dataset': bench, 'avg_improvement': avg, 'success_rate': success_rate})

out_df = pd.DataFrame(rows)
out_df.to_csv(OUTPUT_CSV, index=False)
print(f'Summary saved to {OUTPUT_CSV}')
print(out_df)
