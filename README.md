

## 🔧 Environment Setup

```bash
# Create and activate conda environment
conda create -n Aware-Compiler python==3.10
conda activate Aware-Compiler

# Initialize and update submodules
git submodule update --init --recursive

# Install verl and other dependencies
cd verl
pip3 install -e .
cd .. 
pip3 install vllm
pip3 install flash-attn --no-build-isolation
pip3 install FlagEmbedding
pip3 install faiss-cpu
```

---

## 🧪 Training

To run **Experiment 1 and 2**, follow these steps:

### 1. Generate Dataset and Train

```bash
cd examples/data_preprocess
PYTHONPTYH="../../" python3 compiler_autotuning_sft.py
PYTHONPTYH="../../" python3 compiler_autotuning_rl.py
```

```bash
bash train_sft.sh
bash train_rl.sh
```

---

## 🚀 Inference

After training your models, follow these steps for inference:

1.  **Merge model weights and VLLM server:**
```bash
bash infer_model_merge.sh
bash infer_vllm_serve.sh
```
2.  **Run inference:**
```bash
bash infer_run.sh
```
            