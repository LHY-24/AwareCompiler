### train/poj104-v1/poj104-v1_50_62.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_50_62.ll`

**Performance Improvement (OverOz):** 0.0345

**Optimal Pass Sequence:**
```json
[
  "--functionattrs",
  "--mergefunc",
  "--flattencfg",
  "--inline",
  "--jump-threading",
  "--mldst-motion",
  "--gvn",
  "-loop-reduce",
  "--sroa",
  "--prune-eh",
  "--newgvn",
  "--elim-avail-extern",
  "--mergefunc",
  "--loop-reroll",
  "--newgvn",
  "--simplifycfg",
  "--instsimplify",
  "--aggressive-instcombine",
  "--load-store-vectorizer",
  "--inline",
  "--elim-avail-extern",
  "--loop-simplifycfg",
  "--memcpyopt",
  "--inline",
  "--loop-rotate",
  "--elim-avail-extern",
  "--instcombine",
  "--loop-instsimplify",
  "--mergefunc",
  "--inline"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 4 |
| onePredOneSuc | 1 |
| onePredTwoSuc | 2 |
| oneSuccessor | 4 |
| twoPred | 3 |
| twoPredOneSuc | 2 |
| twoEach | 1 |
| twoSuccessor | 3 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 10 |
| BeginPhi | 0 |
| BranchCount | 7 |
| returnInt | 3 |
| CriticalCount | 3 |
| NumEdges | 10 |
| const32Bit | 17 |
| const64Bit | 10 |
| numConstZeroes | 4 |
| numConstOnes | 9 |
| UncondBranches | 4 |
| binaryConstArg | 4 |
| NumAShrInst | 0 |
| NumAddInst | 5 |
| NumAllocaInst | 7 |
| NumAndInst | 0 |
| BlockMid | 1 |
| BlockLow | 9 |
| NumBitCastInst | 9 |
| NumBrInst | 7 |
| NumCallInst | 14 |
| NumGetElementPtrInst | 1 |
| NumICmpInst | 3 |
| NumLShrInst | 0 |
| NumLoadInst | 11 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 1 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 7 |
| NumSubInst | 0 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 10 |
| TotalInsts | 70 |
| TotalMemInst | 40 |
| TotalFuncs | 11 |
| ArgsPhi | 0 |
| testUnary | 28 |

---

### train/poj104-v1/poj104-v1_84_2702.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_84_2702.ll`

**Performance Improvement (OverOz):** 0.0690

**Optimal Pass Sequence:**
```json
[
  "--dse",
  "--correlated-propagation",
  "--early-cse",
  "--early-cse-memssa",
  "--loop-simplifycfg",
  "--early-cse",
  "--loop-simplifycfg",
  "--loop-deletion",
  "--jump-threading",
  "--simplifycfg",
  "--aggressive-instcombine",
  "--loop-instsimplify",
  "--loop-simplifycfg",
  "--die",
  "--dse",
  "--lower-constant-intrinsics",
  "--gvn-hoist",
  "--inline",
  "--slp-vectorizer",
  "--early-cse",
  "--ipsccp",
  "--jump-threading",
  "--newgvn",
  "--flattencfg",
  "--inline",
  "--loop-instsimplify",
  "--mem2reg",
  "--mergefunc",
  "--bdce",
  "--dse"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 7 |
| onePredOneSuc | 4 |
| onePredTwoSuc | 2 |
| oneSuccessor | 7 |
| twoPred | 4 |
| twoPredOneSuc | 3 |
| twoEach | 1 |
| twoSuccessor | 4 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 14 |
| BeginPhi | 0 |
| BranchCount | 11 |
| returnInt | 5 |
| CriticalCount | 2 |
| NumEdges | 15 |
| const32Bit | 10 |
| const64Bit | 10 |
| numConstZeroes | 1 |
| numConstOnes | 8 |
| UncondBranches | 7 |
| binaryConstArg | 2 |
| NumAShrInst | 0 |
| NumAddInst | 1 |
| NumAllocaInst | 6 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 12 |
| NumBitCastInst | 10 |
| NumBrInst | 11 |
| NumCallInst | 17 |
| NumGetElementPtrInst | 0 |
| NumICmpInst | 4 |
| NumLShrInst | 0 |
| NumLoadInst | 18 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 0 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 9 |
| NumSubInst | 1 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 14 |
| TotalInsts | 80 |
| TotalMemInst | 50 |
| TotalFuncs | 10 |
| ArgsPhi | 0 |
| testUnary | 34 |

---

### train/poj104-v1/poj104-v1_82_590.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_82_590.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 8 |
| onePredOneSuc | 3 |
| onePredTwoSuc | 4 |
| oneSuccessor | 6 |
| twoPred | 3 |
| twoPredOneSuc | 1 |
| twoEach | 2 |
| twoSuccessor | 6 |
| morePreds | 1 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 15 |
| BeginPhi | 0 |
| BranchCount | 12 |
| returnInt | 4 |
| CriticalCount | 5 |
| NumEdges | 18 |
| const32Bit | 21 |
| const64Bit | 12 |
| numConstZeroes | 5 |
| numConstOnes | 12 |
| UncondBranches | 6 |
| binaryConstArg | 2 |
| NumAShrInst | 0 |
| NumAddInst | 2 |
| NumAllocaInst | 9 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 13 |
| NumBitCastInst | 12 |
| NumBrInst | 12 |
| NumCallInst | 18 |
| NumGetElementPtrInst | 0 |
| NumICmpInst | 6 |
| NumLShrInst | 0 |
| NumLoadInst | 12 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 0 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 10 |
| NumSubInst | 0 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 15 |
| TotalInsts | 84 |
| TotalMemInst | 49 |
| TotalFuncs | 10 |
| ArgsPhi | 0 |
| testUnary | 33 |

---

### train/poj104-v1/poj104-v1_33_1674.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_33_1674.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 13 |
| onePredOneSuc | 8 |
| onePredTwoSuc | 4 |
| oneSuccessor | 13 |
| twoPred | 6 |
| twoPredOneSuc | 4 |
| twoEach | 2 |
| twoSuccessor | 6 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 22 |
| BeginPhi | 0 |
| BranchCount | 19 |
| returnInt | 9 |
| CriticalCount | 1 |
| NumEdges | 25 |
| const32Bit | 11 |
| const64Bit | 14 |
| numConstZeroes | 18 |
| numConstOnes | 3 |
| UncondBranches | 13 |
| binaryConstArg | 2 |
| NumAShrInst | 0 |
| NumAddInst | 2 |
| NumAllocaInst | 1 |
| NumAndInst | 0 |
| BlockMid | 0 |
| BlockLow | 22 |
| NumBitCastInst | 0 |
| NumBrInst | 19 |
| NumCallInst | 11 |
| NumGetElementPtrInst | 12 |
| NumICmpInst | 6 |
| NumLShrInst | 0 |
| NumLoadInst | 20 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 14 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 6 |
| NumSubInst | 0 |
| NumTruncInst | 1 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 22 |
| TotalInsts | 95 |
| TotalMemInst | 50 |
| TotalFuncs | 9 |
| ArgsPhi | 0 |
| testUnary | 36 |

---

### train/poj104-v1/poj104-v1_99_2295.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_99_2295.ll`

**Performance Improvement (OverOz):** 0.0000

**Optimal Pass Sequence:**
```json
[
  "--sroa",
  "--instcombine",
  "--flattencfg",
  "--early-cse-memssa",
  "--lower-expect",
  "--instcombine",
  "--loop-simplifycfg",
  "--mem2reg",
  "--load-store-vectorizer",
  "--loop-instsimplify",
  "--lower-expect",
  "--jump-threading",
  "--mldst-motion",
  "--instsimplify",
  "--globalopt",
  "--gvn-hoist",
  "--bdce",
  "--early-cse-memssa",
  "--inline",
  "--sroa",
  "--instcombine",
  "--reassociate",
  "--early-cse-memssa",
  "--die",
  "--mergefunc",
  "--jump-threading",
  "--loop-instsimplify",
  "--early-cse",
  "--prune-eh",
  "--gvn"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 9 |
| onePredOneSuc | 5 |
| onePredTwoSuc | 3 |
| oneSuccessor | 9 |
| twoPred | 4 |
| twoPredOneSuc | 3 |
| twoEach | 1 |
| twoSuccessor | 4 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 16 |
| BeginPhi | 0 |
| BranchCount | 13 |
| returnInt | 4 |
| CriticalCount | 0 |
| NumEdges | 17 |
| const32Bit | 23 |
| const64Bit | 14 |
| numConstZeroes | 7 |
| numConstOnes | 13 |
| UncondBranches | 9 |
| binaryConstArg | 9 |
| NumAShrInst | 0 |
| NumAddInst | 5 |
| NumAllocaInst | 8 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 14 |
| NumBitCastInst | 14 |
| NumBrInst | 13 |
| NumCallInst | 20 |
| NumGetElementPtrInst | 0 |
| NumICmpInst | 4 |
| NumLShrInst | 0 |
| NumLoadInst | 18 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 0 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 11 |
| NumSubInst | 0 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 16 |
| TotalInsts | 112 |
| TotalMemInst | 57 |
| TotalFuncs | 10 |
| ArgsPhi | 0 |
| testUnary | 48 |

---

### train/poj104-v1/poj104-v1_40_1569.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_40_1569.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 5 |
| onePredOneSuc | 5 |
| onePredTwoSuc | 0 |
| oneSuccessor | 5 |
| twoPred | 2 |
| twoPredOneSuc | 0 |
| twoEach | 0 |
| twoSuccessor | 2 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 11 |
| BeginPhi | 0 |
| BranchCount | 7 |
| returnInt | 4 |
| CriticalCount | 0 |
| NumEdges | 9 |
| const32Bit | 21 |
| const64Bit | 20 |
| numConstZeroes | 1 |
| numConstOnes | 20 |
| UncondBranches | 5 |
| binaryConstArg | 3 |
| NumAShrInst | 0 |
| NumAddInst | 0 |
| NumAllocaInst | 18 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 9 |
| NumBitCastInst | 20 |
| NumBrInst | 7 |
| NumCallInst | 30 |
| NumGetElementPtrInst | 0 |
| NumICmpInst | 0 |
| NumLShrInst | 0 |
| NumLoadInst | 32 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 4 |
| NumSExtInst | 0 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 15 |
| NumSubInst | 0 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 11 |
| TotalInsts | 149 |
| TotalMemInst | 95 |
| TotalFuncs | 13 |
| ArgsPhi | 0 |
| testUnary | 70 |

---

### train/poj104-v1/poj104-v1_26_674.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_26_674.ll`

**Performance Improvement (OverOz):** 0.0000

**Optimal Pass Sequence:**
```json
[
  "--reg2mem",
  "--gvn",
  "--jump-threading",
  "--instsimplify",
  "--lower-expect",
  "--bdce",
  "--reassociate",
  "--early-cse-memssa",
  "--adce",
  "--loop-simplifycfg",
  "--mergefunc",
  "--instcombine",
  "--correlated-propagation",
  "--reassociate",
  "--sroa",
  "--slp-vectorizer",
  "--mem2reg",
  "--loop-instsimplify",
  "--globalopt",
  "--globaldce",
  "--aggressive-instcombine",
  "--elim-avail-extern",
  "--sroa",
  "--early-cse-memssa",
  "--inline",
  "--flattencfg",
  "--simplifycfg",
  "--gvn",
  "--reassociate",
  "--newgvn"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 11 |
| onePredOneSuc | 6 |
| onePredTwoSuc | 4 |
| oneSuccessor | 11 |
| twoPred | 7 |
| twoPredOneSuc | 4 |
| twoEach | 3 |
| twoSuccessor | 7 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 21 |
| BeginPhi | 0 |
| BranchCount | 18 |
| returnInt | 3 |
| CriticalCount | 4 |
| NumEdges | 25 |
| const32Bit | 23 |
| const64Bit | 24 |
| numConstZeroes | 20 |
| numConstOnes | 12 |
| UncondBranches | 11 |
| binaryConstArg | 4 |
| NumAShrInst | 0 |
| NumAddInst | 4 |
| NumAllocaInst | 7 |
| NumAndInst | 0 |
| BlockMid | 1 |
| BlockLow | 20 |
| NumBitCastInst | 12 |
| NumBrInst | 18 |
| NumCallInst | 18 |
| NumGetElementPtrInst | 10 |
| NumICmpInst | 7 |
| NumLShrInst | 0 |
| NumLoadInst | 23 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 12 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 14 |
| NumSubInst | 0 |
| NumTruncInst | 1 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 21 |
| TotalInsts | 129 |
| TotalMemInst | 72 |
| TotalFuncs | 11 |
| ArgsPhi | 0 |
| testUnary | 55 |

---

### train/poj104-v1/poj104-v1_38_623.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_38_623.ll`

**Performance Improvement (OverOz):** 0.0000

**Optimal Pass Sequence:**
```json
[
  "--loop-guard-widening",
  "--newgvn",
  "--licm",
  "--loop-instsimplify",
  "--reassociate",
  "--dse",
  "--ipsccp",
  "--early-cse",
  "--simplifycfg",
  "--early-cse-memssa",
  "--dce",
  "--reassociate",
  "--jump-threading",
  "--reassociate",
  "--sroa",
  "--mergefunc",
  "--loop-instsimplify",
  "--jump-threading",
  "--simplifycfg",
  "--gvn",
  "--inline",
  "--load-store-vectorizer",
  "--indvars",
  "--sroa",
  "--gvn",
  "--jump-threading",
  "--newgvn",
  "--globalopt",
  "--elim-avail-extern",
  "--instcombine"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 9 |
| onePredOneSuc | 8 |
| onePredTwoSuc | 0 |
| oneSuccessor | 9 |
| twoPred | 3 |
| twoPredOneSuc | 0 |
| twoEach | 3 |
| twoSuccessor | 3 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 15 |
| BeginPhi | 0 |
| BranchCount | 12 |
| returnInt | 5 |
| CriticalCount | 0 |
| NumEdges | 15 |
| const32Bit | 16 |
| const64Bit | 22 |
| numConstZeroes | 13 |
| numConstOnes | 11 |
| UncondBranches | 9 |
| binaryConstArg | 3 |
| NumAShrInst | 0 |
| NumAddInst | 3 |
| NumAllocaInst | 8 |
| NumAndInst | 0 |
| BlockMid | 4 |
| BlockLow | 11 |
| NumBitCastInst | 14 |
| NumBrInst | 12 |
| NumCallInst | 22 |
| NumGetElementPtrInst | 8 |
| NumICmpInst | 3 |
| NumLShrInst | 0 |
| NumLoadInst | 29 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 8 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 14 |
| NumSubInst | 0 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 15 |
| TotalInsts | 133 |
| TotalMemInst | 81 |
| TotalFuncs | 11 |
| ArgsPhi | 0 |
| testUnary | 61 |

---

### train/poj104-v1/poj104-v1_1_2216.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_1_2216.ll`

**Performance Improvement (OverOz):** 0.0222

**Optimal Pass Sequence:**
```json
[
  "--sroa",
  "--load-store-vectorizer",
  "--loop-reroll",
  "--nary-reassociate",
  "--simplifycfg",
  "--mergefunc",
  "--loop-instsimplify",
  "--simplifycfg",
  "--loop-simplifycfg",
  "--ipsccp",
  "--lower-constant-intrinsics",
  "--loop-simplifycfg",
  "--mergefunc",
  "--memcpyopt",
  "--inline",
  "--dse",
  "--reassociate",
  "--reassociate",
  "--slsr",
  "--indvars",
  "--early-cse-memssa",
  "--indvars",
  "--instcombine",
  "--load-store-vectorizer",
  "--inline",
  "--loop-simplifycfg",
  "--mldst-motion",
  "--load-store-vectorizer",
  "--simplifycfg",
  "--early-cse-memssa"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 10 |
| onePredOneSuc | 7 |
| onePredTwoSuc | 2 |
| oneSuccessor | 9 |
| twoPred | 3 |
| twoPredOneSuc | 0 |
| twoEach | 2 |
| twoSuccessor | 5 |
| morePreds | 1 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 18 |
| BeginPhi | 0 |
| BranchCount | 14 |
| returnInt | 6 |
| CriticalCount | 2 |
| NumEdges | 19 |
| const32Bit | 24 |
| const64Bit | 16 |
| numConstZeroes | 3 |
| numConstOnes | 19 |
| UncondBranches | 9 |
| binaryConstArg | 2 |
| NumAShrInst | 0 |
| NumAddInst | 3 |
| NumAllocaInst | 13 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 16 |
| NumBitCastInst | 16 |
| NumBrInst | 14 |
| NumCallInst | 24 |
| NumGetElementPtrInst | 0 |
| NumICmpInst | 5 |
| NumLShrInst | 0 |
| NumLoadInst | 21 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 4 |
| NumSExtInst | 0 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 13 |
| NumSubInst | 0 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 18 |
| TotalInsts | 116 |
| TotalMemInst | 71 |
| TotalFuncs | 11 |
| ArgsPhi | 0 |
| testUnary | 50 |

---

### train/poj104-v1/poj104-v1_90_1692.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_90_1692.ll`

**Performance Improvement (OverOz):** 0.0192

**Optimal Pass Sequence:**
```json
[
  "--sroa",
  "--simplifycfg",
  "--mldst-motion",
  "--mem2reg",
  "--sccp",
  "--inline",
  "--gvn",
  "--inline",
  "--load-store-vectorizer",
  "--adce",
  "--loop-simplifycfg",
  "--loop-reroll",
  "--mergefunc",
  "--gvn",
  "--dce",
  "--gvn-hoist",
  "--flattencfg",
  "--early-cse-memssa",
  "--ipsccp",
  "--sroa",
  "--simplifycfg",
  "--prune-eh",
  "--elim-avail-extern",
  "--gvn-hoist",
  "--slsr",
  "--gvn-hoist",
  "--instcombine",
  "--globalopt",
  "--loweratomic",
  "--ipsccp"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 11 |
| onePredOneSuc | 8 |
| onePredTwoSuc | 2 |
| oneSuccessor | 10 |
| twoPred | 4 |
| twoPredOneSuc | 1 |
| twoEach | 3 |
| twoSuccessor | 6 |
| morePreds | 1 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 20 |
| BeginPhi | 0 |
| BranchCount | 16 |
| returnInt | 6 |
| CriticalCount | 3 |
| NumEdges | 22 |
| const32Bit | 29 |
| const64Bit | 14 |
| numConstZeroes | 7 |
| numConstOnes | 21 |
| UncondBranches | 10 |
| binaryConstArg | 3 |
| NumAShrInst | 0 |
| NumAddInst | 3 |
| NumAllocaInst | 13 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 18 |
| NumBitCastInst | 14 |
| NumBrInst | 16 |
| NumCallInst | 22 |
| NumGetElementPtrInst | 0 |
| NumICmpInst | 6 |
| NumLShrInst | 0 |
| NumLoadInst | 22 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 4 |
| NumSExtInst | 0 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 17 |
| NumSubInst | 2 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 20 |
| TotalInsts | 119 |
| TotalMemInst | 74 |
| TotalFuncs | 11 |
| ArgsPhi | 0 |
| testUnary | 49 |

---

### train/poj104-v1/poj104-v1_22_157.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_22_157.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 15 |
| onePredOneSuc | 8 |
| onePredTwoSuc | 7 |
| oneSuccessor | 13 |
| twoPred | 6 |
| twoPredOneSuc | 2 |
| twoEach | 3 |
| twoSuccessor | 10 |
| morePreds | 2 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 26 |
| BeginPhi | 0 |
| BranchCount | 23 |
| returnInt | 4 |
| CriticalCount | 6 |
| NumEdges | 33 |
| const32Bit | 22 |
| const64Bit | 20 |
| numConstZeroes | 15 |
| numConstOnes | 10 |
| UncondBranches | 13 |
| binaryConstArg | 4 |
| NumAShrInst | 0 |
| NumAddInst | 3 |
| NumAllocaInst | 8 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 24 |
| NumBitCastInst | 14 |
| NumBrInst | 23 |
| NumCallInst | 20 |
| NumGetElementPtrInst | 5 |
| NumICmpInst | 10 |
| NumLShrInst | 0 |
| NumLoadInst | 32 |
| NumMulInst | 1 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 7 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 16 |
| NumSubInst | 1 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 26 |
| TotalInsts | 143 |
| TotalMemInst | 81 |
| TotalFuncs | 10 |
| ArgsPhi | 0 |
| testUnary | 61 |

---

### train/poj104-v1/poj104-v1_45_137.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_45_137.ll`

**Performance Improvement (OverOz):** 0.0000

**Optimal Pass Sequence:**
```json
[
  "--simple-loop-unswitch",
  "--instcombine",
  "--memcpyopt",
  "--inline",
  "--adce",
  "--lower-constant-intrinsics",
  "--newgvn",
  "--nary-reassociate",
  "--ipsccp",
  "--sroa",
  "--loop-deletion",
  "--early-cse-memssa",
  "--ipsccp",
  "--instsimplify",
  "--correlated-propagation",
  "--loop-reroll",
  "--instsimplify",
  "--newgvn",
  "--load-store-vectorizer",
  "--bdce",
  "--loop-simplifycfg",
  "--simplifycfg",
  "--instsimplify",
  "--load-store-vectorizer",
  "--mldst-motion",
  "--mem2reg",
  "--instsimplify",
  "--simplifycfg",
  "--prune-eh",
  "--elim-avail-extern"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 3 |
| onePred | 14 |
| onePredOneSuc | 10 |
| onePredTwoSuc | 4 |
| oneSuccessor | 13 |
| twoPred | 6 |
| twoPredOneSuc | 2 |
| twoEach | 3 |
| twoSuccessor | 8 |
| morePreds | 1 |
| BB03Phi | 3 |
| BBHiPhi | 0 |
| BBNoPhi | 21 |
| BeginPhi | 3 |
| BranchCount | 21 |
| returnInt | 3 |
| CriticalCount | 5 |
| NumEdges | 29 |
| const32Bit | 28 |
| const64Bit | 26 |
| numConstZeroes | 24 |
| numConstOnes | 18 |
| UncondBranches | 13 |
| binaryConstArg | 3 |
| NumAShrInst | 0 |
| NumAddInst | 3 |
| NumAllocaInst | 11 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 22 |
| NumBitCastInst | 16 |
| NumBrInst | 21 |
| NumCallInst | 21 |
| NumGetElementPtrInst | 9 |
| NumICmpInst | 10 |
| NumLShrInst | 0 |
| NumLoadInst | 22 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 3 |
| NumRetInst | 3 |
| NumSExtInst | 6 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 16 |
| NumSubInst | 0 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 24 |
| TotalInsts | 141 |
| TotalMemInst | 79 |
| TotalFuncs | 10 |
| ArgsPhi | 7 |
| testUnary | 55 |

---

### train/poj104-v1/poj104-v1_86_984.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_86_984.ll`

**Performance Improvement (OverOz):** 0.0656

**Optimal Pass Sequence:**
```json
[
  "--gvn",
  "--slp-vectorizer",
  "--loop-simplifycfg",
  "--instcombine",
  "--simplifycfg",
  "--dse",
  "--adce",
  "--instcombine",
  "--lower-constant-intrinsics",
  "--elim-avail-extern",
  "--ipsccp",
  "--instsimplify",
  "--loop-simplifycfg",
  "--adce",
  "--loop-instsimplify",
  "--sccp",
  "--instsimplify",
  "--gvn-hoist",
  "--lower-constant-intrinsics",
  "--ipsccp",
  "--die",
  "--correlated-propagation",
  "--instcombine",
  "--early-cse",
  "--bdce",
  "--lower-constant-intrinsics",
  "--early-cse-memssa",
  "--prune-eh",
  "--jump-threading",
  "--dse"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 14 |
| onePredOneSuc | 10 |
| onePredTwoSuc | 3 |
| oneSuccessor | 13 |
| twoPred | 4 |
| twoPredOneSuc | 1 |
| twoEach | 3 |
| twoSuccessor | 6 |
| morePreds | 1 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 22 |
| BeginPhi | 0 |
| BranchCount | 19 |
| returnInt | 5 |
| CriticalCount | 2 |
| NumEdges | 25 |
| const32Bit | 26 |
| const64Bit | 16 |
| numConstZeroes | 9 |
| numConstOnes | 13 |
| UncondBranches | 13 |
| binaryConstArg | 10 |
| NumAShrInst | 0 |
| NumAddInst | 7 |
| NumAllocaInst | 7 |
| NumAndInst | 0 |
| BlockMid | 1 |
| BlockLow | 21 |
| NumBitCastInst | 12 |
| NumBrInst | 19 |
| NumCallInst | 19 |
| NumGetElementPtrInst | 4 |
| NumICmpInst | 6 |
| NumLShrInst | 0 |
| NumLoadInst | 21 |
| NumMulInst | 3 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 4 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 10 |
| NumSubInst | 2 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 22 |
| TotalInsts | 117 |
| TotalMemInst | 61 |
| TotalFuncs | 10 |
| ArgsPhi | 0 |
| testUnary | 44 |

---

### train/poj104-v1/poj104-v1_8_1344.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_8_1344.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 12 |
| onePredOneSuc | 11 |
| onePredTwoSuc | 0 |
| oneSuccessor | 12 |
| twoPred | 4 |
| twoPredOneSuc | 0 |
| twoEach | 4 |
| twoSuccessor | 4 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 20 |
| BeginPhi | 0 |
| BranchCount | 16 |
| returnInt | 8 |
| CriticalCount | 0 |
| NumEdges | 20 |
| const32Bit | 21 |
| const64Bit | 8 |
| numConstZeroes | 6 |
| numConstOnes | 15 |
| UncondBranches | 12 |
| binaryConstArg | 6 |
| NumAShrInst | 0 |
| NumAddInst | 4 |
| NumAllocaInst | 11 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 18 |
| NumBitCastInst | 10 |
| NumBrInst | 16 |
| NumCallInst | 20 |
| NumGetElementPtrInst | 6 |
| NumICmpInst | 4 |
| NumLShrInst | 0 |
| NumLoadInst | 32 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 4 |
| NumSExtInst | 8 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 15 |
| NumSubInst | 3 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 2 |
| TotalBlocks | 20 |
| TotalInsts | 135 |
| TotalMemInst | 84 |
| TotalFuncs | 14 |
| ArgsPhi | 0 |
| testUnary | 63 |

---

### train/poj104-v1/poj104-v1_61_202.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_61_202.ll`

**Performance Improvement (OverOz):** 0.0147

**Optimal Pass Sequence:**
```json
[
  "--mergefunc",
  "--load-store-vectorizer",
  "--slsr",
  "--loop-reroll",
  "--early-cse-memssa",
  "--newgvn",
  "--flattencfg",
  "--sroa",
  "--mergefunc",
  "-loop-reduce",
  "--newgvn",
  "--lower-expect",
  "--loop-simplifycfg",
  "--lower-constant-intrinsics",
  "--correlated-propagation",
  "--load-store-vectorizer",
  "--lower-expect",
  "--dse",
  "--sccp",
  "--loop-deletion",
  "--instcombine",
  "--dse",
  "--simplifycfg",
  "--prune-eh",
  "--simplifycfg",
  "--early-cse-memssa",
  "--jump-threading",
  "--inline",
  "--loop-instsimplify",
  "--loop-simplifycfg"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 11 |
| onePredOneSuc | 9 |
| onePredTwoSuc | 1 |
| oneSuccessor | 11 |
| twoPred | 4 |
| twoPredOneSuc | 1 |
| twoEach | 3 |
| twoSuccessor | 4 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 18 |
| BeginPhi | 0 |
| BranchCount | 15 |
| returnInt | 5 |
| CriticalCount | 0 |
| NumEdges | 19 |
| const32Bit | 23 |
| const64Bit | 28 |
| numConstZeroes | 14 |
| numConstOnes | 17 |
| UncondBranches | 11 |
| binaryConstArg | 6 |
| NumAShrInst | 0 |
| NumAddInst | 4 |
| NumAllocaInst | 9 |
| NumAndInst | 0 |
| BlockMid | 3 |
| BlockLow | 15 |
| NumBitCastInst | 16 |
| NumBrInst | 15 |
| NumCallInst | 23 |
| NumGetElementPtrInst | 10 |
| NumICmpInst | 4 |
| NumLShrInst | 0 |
| NumLoadInst | 25 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 8 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 14 |
| NumSubInst | 3 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 18 |
| TotalInsts | 134 |
| TotalMemInst | 81 |
| TotalFuncs | 10 |
| ArgsPhi | 0 |
| testUnary | 58 |

---

### train/poj104-v1/poj104-v1_19_515.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_19_515.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 10 |
| onePredOneSuc | 7 |
| onePredTwoSuc | 2 |
| oneSuccessor | 10 |
| twoPred | 5 |
| twoPredOneSuc | 2 |
| twoEach | 3 |
| twoSuccessor | 5 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 18 |
| BeginPhi | 0 |
| BranchCount | 15 |
| returnInt | 7 |
| CriticalCount | 2 |
| NumEdges | 20 |
| const32Bit | 19 |
| const64Bit | 45 |
| numConstZeroes | 36 |
| numConstOnes | 13 |
| UncondBranches | 10 |
| binaryConstArg | 3 |
| NumAShrInst | 0 |
| NumAddInst | 3 |
| NumAllocaInst | 8 |
| NumAndInst | 0 |
| BlockMid | 3 |
| BlockLow | 15 |
| NumBitCastInst | 14 |
| NumBrInst | 15 |
| NumCallInst | 25 |
| NumGetElementPtrInst | 20 |
| NumICmpInst | 5 |
| NumLShrInst | 0 |
| NumLoadInst | 20 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 7 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 10 |
| NumSubInst | 0 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 18 |
| TotalInsts | 130 |
| TotalMemInst | 83 |
| TotalFuncs | 15 |
| ArgsPhi | 0 |
| testUnary | 49 |

---

### train/poj104-v1/poj104-v1_86_1339.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_86_1339.ll`

**Performance Improvement (OverOz):** 0.0000

**Optimal Pass Sequence:**
```json
[
  "--deadargelim",
  "--mergefunc",
  "--gvn-hoist",
  "--bdce",
  "--inline",
  "--early-cse-memssa",
  "--slp-vectorizer",
  "--loop-simplifycfg",
  "--reassociate",
  "--early-cse",
  "--gvn-hoist",
  "--loop-deletion",
  "--early-cse-memssa",
  "--globalopt",
  "--globaldce",
  "--mergefunc",
  "--gvn-hoist",
  "--mldst-motion",
  "--mem2reg",
  "--load-store-vectorizer",
  "--lower-expect",
  "--aggressive-instcombine",
  "--simplifycfg",
  "--reassociate",
  "--prune-eh",
  "--sroa",
  "--load-store-vectorizer",
  "--correlated-propagation",
  "--newgvn",
  "--jump-threading"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 14 |
| onePredOneSuc | 10 |
| onePredTwoSuc | 3 |
| oneSuccessor | 13 |
| twoPred | 5 |
| twoPredOneSuc | 2 |
| twoEach | 3 |
| twoSuccessor | 7 |
| morePreds | 1 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 23 |
| BeginPhi | 0 |
| BranchCount | 20 |
| returnInt | 8 |
| CriticalCount | 2 |
| NumEdges | 27 |
| const32Bit | 32 |
| const64Bit | 19 |
| numConstZeroes | 12 |
| numConstOnes | 14 |
| UncondBranches | 13 |
| binaryConstArg | 11 |
| NumAShrInst | 0 |
| NumAddInst | 7 |
| NumAllocaInst | 9 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 21 |
| NumBitCastInst | 16 |
| NumBrInst | 20 |
| NumCallInst | 26 |
| NumGetElementPtrInst | 3 |
| NumICmpInst | 7 |
| NumLShrInst | 0 |
| NumLoadInst | 25 |
| NumMulInst | 3 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 3 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 15 |
| NumSubInst | 2 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 23 |
| TotalInsts | 139 |
| TotalMemInst | 78 |
| TotalFuncs | 10 |
| ArgsPhi | 0 |
| testUnary | 53 |

---

### train/poj104-v1/poj104-v1_55_17.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_55_17.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 11 |
| onePredOneSuc | 5 |
| onePredTwoSuc | 4 |
| oneSuccessor | 10 |
| twoPred | 4 |
| twoPredOneSuc | 2 |
| twoEach | 2 |
| twoSuccessor | 6 |
| morePreds | 1 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 20 |
| BeginPhi | 0 |
| BranchCount | 16 |
| returnInt | 3 |
| CriticalCount | 3 |
| NumEdges | 22 |
| const32Bit | 22 |
| const64Bit | 35 |
| numConstZeroes | 22 |
| numConstOnes | 12 |
| UncondBranches | 10 |
| binaryConstArg | 5 |
| NumAShrInst | 0 |
| NumAddInst | 4 |
| NumAllocaInst | 10 |
| NumAndInst | 0 |
| BlockMid | 3 |
| BlockLow | 17 |
| NumBitCastInst | 17 |
| NumBrInst | 16 |
| NumCallInst | 23 |
| NumGetElementPtrInst | 11 |
| NumICmpInst | 6 |
| NumLShrInst | 0 |
| NumLoadInst | 31 |
| NumMulInst | 2 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 4 |
| NumSExtInst | 14 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 16 |
| NumSubInst | 3 |
| NumTruncInst | 1 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 20 |
| TotalInsts | 160 |
| TotalMemInst | 91 |
| TotalFuncs | 12 |
| ArgsPhi | 0 |
| testUnary | 73 |

---

### train/poj104-v1/poj104-v1_55_430.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_55_430.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 15 |
| onePredOneSuc | 10 |
| onePredTwoSuc | 4 |
| oneSuccessor | 15 |
| twoPred | 9 |
| twoPredOneSuc | 5 |
| twoEach | 4 |
| twoSuccessor | 9 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 27 |
| BeginPhi | 0 |
| BranchCount | 24 |
| returnInt | 5 |
| CriticalCount | 5 |
| NumEdges | 33 |
| const32Bit | 35 |
| const64Bit | 40 |
| numConstZeroes | 27 |
| numConstOnes | 15 |
| UncondBranches | 15 |
| binaryConstArg | 12 |
| NumAShrInst | 0 |
| NumAddInst | 8 |
| NumAllocaInst | 11 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 25 |
| NumBitCastInst | 20 |
| NumBrInst | 24 |
| NumCallInst | 27 |
| NumGetElementPtrInst | 16 |
| NumICmpInst | 9 |
| NumLShrInst | 0 |
| NumLoadInst | 41 |
| NumMulInst | 1 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 20 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 19 |
| NumSubInst | 6 |
| NumTruncInst | 3 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 27 |
| TotalInsts | 210 |
| TotalMemInst | 114 |
| TotalFuncs | 11 |
| ArgsPhi | 0 |
| testUnary | 95 |

---

### train/poj104-v1/poj104-v1_9_722.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_9_722.ll`

**Performance Improvement (OverOz):** 0.0303

**Optimal Pass Sequence:**
```json
[
  "--speculative-execution",
  "--early-cse-memssa",
  "--globalopt",
  "--loweratomic",
  "--early-cse",
  "--instcombine",
  "--simplifycfg",
  "--jump-threading",
  "--inline",
  "--reassociate",
  "--dce",
  "--slp-vectorizer",
  "--bdce",
  "--mergefunc",
  "--mergefunc",
  "--dce",
  "--sccp",
  "--instcombine",
  "--bdce",
  "--mem2reg",
  "--gvn",
  "--sroa",
  "--flattencfg",
  "--early-cse-memssa",
  "--ipsccp",
  "--aggressive-instcombine",
  "--sroa",
  "--ipsccp",
  "--gvn",
  "--correlated-propagation"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 18 |
| onePredOneSuc | 15 |
| onePredTwoSuc | 2 |
| oneSuccessor | 18 |
| twoPred | 7 |
| twoPredOneSuc | 2 |
| twoEach | 5 |
| twoSuccessor | 7 |
| morePreds | 0 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 28 |
| BeginPhi | 0 |
| BranchCount | 25 |
| returnInt | 5 |
| CriticalCount | 1 |
| NumEdges | 32 |
| const32Bit | 46 |
| const64Bit | 21 |
| numConstZeroes | 27 |
| numConstOnes | 27 |
| UncondBranches | 18 |
| binaryConstArg | 12 |
| NumAShrInst | 0 |
| NumAddInst | 10 |
| NumAllocaInst | 14 |
| NumAndInst | 0 |
| BlockMid | 4 |
| BlockLow | 24 |
| NumBitCastInst | 22 |
| NumBrInst | 25 |
| NumCallInst | 26 |
| NumGetElementPtrInst | 24 |
| NumICmpInst | 7 |
| NumLShrInst | 0 |
| NumLoadInst | 41 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 15 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 19 |
| NumSubInst | 3 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 3 |
| TotalBlocks | 28 |
| TotalInsts | 212 |
| TotalMemInst | 124 |
| TotalFuncs | 13 |
| ArgsPhi | 0 |
| testUnary | 95 |

---

### train/poj104-v1/poj104-v1_23_1128.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_23_1128.ll`

**Performance Improvement (OverOz):** 0.0187

**Optimal Pass Sequence:**
```json
[
  "--loop-unswitch",
  "--gvn",
  "--load-store-vectorizer",
  "--sroa",
  "--gvn",
  "--licm",
  "--bdce",
  "--inline",
  "--instcombine",
  "--mem2reg",
  "--adce",
  "--newgvn",
  "--correlated-propagation",
  "--newgvn",
  "--mergefunc",
  "--mem2reg",
  "--gvn-hoist",
  "--adce",
  "--slp-vectorizer",
  "--jump-threading",
  "--instsimplify",
  "--loop-instsimplify",
  "--load-store-vectorizer",
  "--early-cse-memssa",
  "--ipsccp",
  "--ipsccp",
  "--ipsccp",
  "--sccp",
  "--globalopt",
  "--globaldce"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 18 |
| onePredOneSuc | 13 |
| onePredTwoSuc | 4 |
| oneSuccessor | 17 |
| twoPred | 8 |
| twoPredOneSuc | 2 |
| twoEach | 6 |
| twoSuccessor | 10 |
| morePreds | 1 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 30 |
| BeginPhi | 0 |
| BranchCount | 27 |
| returnInt | 4 |
| CriticalCount | 7 |
| NumEdges | 37 |
| const32Bit | 34 |
| const64Bit | 37 |
| numConstZeroes | 29 |
| numConstOnes | 21 |
| UncondBranches | 17 |
| binaryConstArg | 11 |
| NumAShrInst | 0 |
| NumAddInst | 9 |
| NumAllocaInst | 9 |
| NumAndInst | 0 |
| BlockMid | 2 |
| BlockLow | 28 |
| NumBitCastInst | 16 |
| NumBrInst | 27 |
| NumCallInst | 23 |
| NumGetElementPtrInst | 17 |
| NumICmpInst | 10 |
| NumLShrInst | 0 |
| NumLoadInst | 40 |
| NumMulInst | 0 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 22 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 18 |
| NumSubInst | 2 |
| NumTruncInst | 0 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 30 |
| TotalInsts | 196 |
| TotalMemInst | 107 |
| TotalFuncs | 10 |
| ArgsPhi | 0 |
| testUnary | 87 |

---

### train/poj104-v1/poj104-v1_55_1585.ll

**File Path:** `/root/AwareCompiler/examples/data_preprocess/llvmir_datasets/train/poj104-v1/poj104-v1_55_1585.ll`

**Performance Improvement (OverOz):** 0.0

**Optimal Pass Sequence:**
```json
[
  "-Oz"
]
```

**Autophase Features:**

| Feature | Value |
|---------|-------|
| BBNumArgsHi | 0 |
| BBNumArgsLo | 0 |
| onePred | 19 |
| onePredOneSuc | 12 |
| onePredTwoSuc | 7 |
| oneSuccessor | 18 |
| twoPred | 11 |
| twoPredOneSuc | 4 |
| twoEach | 6 |
| twoSuccessor | 13 |
| morePreds | 1 |
| BB03Phi | 0 |
| BBHiPhi | 0 |
| BBNoPhi | 34 |
| BeginPhi | 0 |
| BranchCount | 31 |
| returnInt | 4 |
| CriticalCount | 10 |
| NumEdges | 44 |
| const32Bit | 40 |
| const64Bit | 53 |
| numConstZeroes | 41 |
| numConstOnes | 17 |
| UncondBranches | 18 |
| binaryConstArg | 13 |
| NumAShrInst | 0 |
| NumAddInst | 8 |
| NumAllocaInst | 11 |
| NumAndInst | 0 |
| BlockMid | 4 |
| BlockLow | 30 |
| NumBitCastInst | 20 |
| NumBrInst | 31 |
| NumCallInst | 26 |
| NumGetElementPtrInst | 25 |
| NumICmpInst | 13 |
| NumLShrInst | 0 |
| NumLoadInst | 53 |
| NumMulInst | 2 |
| NumOrInst | 0 |
| NumPHIInst | 0 |
| NumRetInst | 3 |
| NumSExtInst | 37 |
| NumSelectInst | 0 |
| NumShlInst | 0 |
| NumStoreInst | 23 |
| NumSubInst | 7 |
| NumTruncInst | 4 |
| NumXorInst | 0 |
| NumZExtInst | 0 |
| TotalBlocks | 34 |
| TotalInsts | 265 |
| TotalMemInst | 138 |
| TotalFuncs | 11 |
| ArgsPhi | 0 |
| testUnary | 125 |

---