#!/bin/bash
set -euo pipefail
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$REPO_ROOT"
export CUDA_VISIBLE_DEVICES=0,1

# --- Best-of-N Configuration ---
NUM_SAMPLES=16  # Number of samples for Best-of-N (can be changed: 4, 8, 16, 32, etc.)

# --- Configuration ---
PYTHON_SCRIPT="agent_r1.vllm_infer.chat_best_of_n"
DATA_DIR="./dataset/rl/"
OUTPUT_FILE="overoz_summary_best_of_${NUM_SAMPLES}.txt"
RESULTS_DIR="./results/best_of_n/"
LLVM_IR_DIR="$REPO_ROOT/examples/data_preprocess/llvmir_datasets"
LLVM_TOOLS_PATH="$REPO_ROOT/agent_r1/tool/tools/comiler_autotuning/raw_tool/"

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

declare -a DATASETS=(
    "rl_validation_cbench-v1.parquet"
    "rl_validation_mibench-v1.parquet"
    "rl_validation_blas-v0.parquet"
    "rl_validation_opencv-v0.parquet"
    "rl_validation_chstone-v0.parquet"
    "rl_validation_tensorflow-v0.parquet"
    "rl_validation_npb-v0.parquet"
)

# Uncomment to test with a single dataset
# declare -a DATASETS=(
#     "rl_validation_cbench-v1.parquet"
# )

COMMON_ARGS=(
    --env optimizer
    --api-key EMPTY
    --api-base http://localhost:8000/v1
    --model agent
    --temperature 0.7
    --top-p 0.8
    --max-tokens 10240
    --repetition-penalty 1.1
    --llvm-ir-dir "$LLVM_IR_DIR"
    --llvm-tools-path "$LLVM_TOOLS_PATH"
    --num-samples "$NUM_SAMPLES"
    # --save-all-samples  # Uncomment to save all N samples per record
)

# --- Script Logic ---

# Prepare the output file with header (simplified: only Best-of-N result)
printf "%-40s | %-18s\n" "Dataset" "Best-of-${NUM_SAMPLES} OverOz" > "$OUTPUT_FILE"
printf "%-40s-|-%-18s\n" "----------------------------------------" "------------------" >> "$OUTPUT_FILE"

echo "============================================================"
echo "Starting Best-of-${NUM_SAMPLES} batch processing..."
echo "============================================================"

# Loop through each dataset filename
for dataset_file in "${DATASETS[@]}"; do
    full_input_path="${DATA_DIR}${dataset_file}"
    
    # Generate output CSV filename for detailed results
    dataset_basename="${dataset_file%.parquet}"
    csv_output="${RESULTS_DIR}best_of_${NUM_SAMPLES}_${dataset_basename}.csv"

    echo "-----------------------------------------------------"
    echo "Processing: ${dataset_file} with Best-of-${NUM_SAMPLES}"
    echo "-----------------------------------------------------"

    # Initialize variables for each dataset
    best_overoz="N/A"

    # Check if the input file exists
    if [[ ! -f "$full_input_path" ]]; then
        echo "Error: Input file not found: ${full_input_path}"
        best_overoz="File_Not_Found"
    else
        # Run the Python script and capture the output
        echo "Running Best-of-${NUM_SAMPLES} inference for ${dataset_file}..."
        script_output=$(python3 -m "$PYTHON_SCRIPT" "${COMMON_ARGS[@]}" \
            --input-file "$full_input_path" \
            --output-file "$csv_output" \
            --no-color 2>&1)
        echo "${script_output}"

        # --- Extract Data from Output ---

        # 1. Extract Average Best-of-N OverOz Score
        best_overoz=$(echo "$script_output" | grep -oP 'Average Best-of-[0-9]+ OverOz: \K[0-9.-]+')
        if [[ -z "$best_overoz" ]]; then
            if echo "$script_output" | grep -q "No valid OverOz scores were calculated"; then
                best_overoz="No_Scores"
            elif echo "$script_output" | grep -q "Error"; then
                best_overoz="Error"
            else
                best_overoz="N/A"
            fi
            echo "Warning: Could not extract Best-of-N OverOz for ${dataset_file}. Set to ${best_overoz}."
        else
            echo "Extracted Best-of-${NUM_SAMPLES} OverOz: ${best_overoz}"
        fi

    fi

    # Append the result to the output file (only Best-of-N OverOz)
    printf "%-40s | %-18s\n" "$dataset_file" "$best_overoz" >> "$OUTPUT_FILE"

done

echo "============================================================"
echo "Best-of-${NUM_SAMPLES} batch processing finished."
echo "Summary saved to: ${OUTPUT_FILE}"
echo "Detailed CSV results saved to: ${RESULTS_DIR}"
echo "============================================================"

# Display the final table
echo ""
echo "=== Summary Table ==="
cat "$OUTPUT_FILE"
