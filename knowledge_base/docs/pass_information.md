# LLVM Optimization Pass Information

This document contains detailed information about LLVM optimization passes.

## Overview

Each pass has specific functionality and effects on the LLVM IR code.

## Pass Descriptions

### --adce

**Name:** Aggressive Dead Code Elimination

**Category:** Dead Code Elimination

**Description:** Removes instructions that do not contribute to the program's output

**Effects:**
- Removes unused instructions
- Reduces code size
- May improve performance

---

### --add-discriminators

**Name:** AddDiscriminators

**Category:** General

**Description:** LLVM optimization pass: AddDiscriminators

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --aggressive-instcombine

**Name:** Aggressive Instruction Combining

**Category:** Instruction Combining

**Description:** Combines instructions more aggressively than regular instcombine

**Effects:**
- Combines complex instruction patterns
- May increase compilation time
- Can improve runtime performance

---

### --alignment-from-assumptions

**Name:** AlignmentFromAssumptions

**Category:** General

**Description:** LLVM optimization pass: AlignmentFromAssumptions

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --always-inline

**Name:** AlwaysInline

**Category:** General

**Description:** LLVM optimization pass: AlwaysInline

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --argpromotion

**Name:** Argpromotion

**Category:** General

**Description:** LLVM optimization pass: Argpromotion

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --attributor

**Name:** Attributor

**Category:** General

**Description:** LLVM optimization pass: Attributor

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --barrier

**Name:** Barrier

**Category:** General

**Description:** LLVM optimization pass: Barrier

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --bdce

**Name:** Bit-Tracking Dead Code Elimination

**Category:** Dead Code Elimination

**Description:** Eliminates code that computes unused bits

**Effects:**
- Removes bit-level unused computations
- Reduces instruction count

---

### --break-crit-edges

**Name:** BreakCritEdges

**Category:** General

**Description:** LLVM optimization pass: BreakCritEdges

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --called-value-propagation

**Name:** CalledValuePropagation

**Category:** General

**Description:** LLVM optimization pass: CalledValuePropagation

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --callsite-splitting

**Name:** CallsiteSplitting

**Category:** General

**Description:** LLVM optimization pass: CallsiteSplitting

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --canonicalize-aliases

**Name:** CanonicalizeAliases

**Category:** General

**Description:** LLVM optimization pass: CanonicalizeAliases

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --consthoist

**Name:** Consthoist

**Category:** General

**Description:** LLVM optimization pass: Consthoist

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --constmerge

**Name:** Constmerge

**Category:** General

**Description:** LLVM optimization pass: Constmerge

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --constprop

**Name:** Constprop

**Category:** General

**Description:** LLVM optimization pass: Constprop

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --coro-cleanup

**Name:** CoroCleanup

**Category:** General

**Description:** LLVM optimization pass: CoroCleanup

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --coro-early

**Name:** CoroEarly

**Category:** General

**Description:** LLVM optimization pass: CoroEarly

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --coro-elide

**Name:** CoroElide

**Category:** General

**Description:** LLVM optimization pass: CoroElide

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --coro-split

**Name:** CoroSplit

**Category:** General

**Description:** LLVM optimization pass: CoroSplit

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --correlated-propagation

**Name:** CorrelatedPropagation

**Category:** General

**Description:** LLVM optimization pass: CorrelatedPropagation

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --cross-dso-cfi

**Name:** CrossDsoCfi

**Category:** General

**Description:** LLVM optimization pass: CrossDsoCfi

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --dce

**Name:** Dead Code Elimination

**Category:** Dead Code Elimination

**Description:** Removes dead instructions

**Effects:**
- Removes unused instructions
- Reduces code size

---

### --deadargelim

**Name:** Deadargelim

**Category:** General

**Description:** LLVM optimization pass: Deadargelim

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --die

**Name:** Dead Instruction Elimination

**Category:** Dead Code Elimination

**Description:** Removes dead instructions

**Effects:**
- Removes unused instructions
- Simplifies control flow

---

### --div-rem-pairs

**Name:** DivRemPairs

**Category:** General

**Description:** LLVM optimization pass: DivRemPairs

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --dse

**Name:** Dead Store Elimination

**Category:** Memory Optimization

**Description:** Removes stores that are never read

**Effects:**
- Removes unused stores
- Reduces memory traffic
- Improves cache performance

---

### --early-cse

**Name:** Early Common Subexpression Elimination

**Category:** Common Subexpression Elimination

**Description:** Eliminates common subexpressions early in the optimization pipeline

**Effects:**
- Reduces redundant computations
- Improves performance
- May increase register pressure

---

### --early-cse-memssa

**Name:** Early CSE with MemorySSA

**Category:** Common Subexpression Elimination

**Description:** CSE using MemorySSA for better memory analysis

**Effects:**
- More precise memory analysis
- Better optimization of memory operations

---

### --ee-instrument

**Name:** EeInstrument

**Category:** General

**Description:** LLVM optimization pass: EeInstrument

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --elim-avail-extern

**Name:** Eliminate Available Externally

**Category:** Function Optimization

**Description:** Eliminates available externally functions

**Effects:**
- Removes unnecessary function definitions
- Reduces code size

---

### --flattencfg

**Name:** Flatten Control Flow Graph

**Category:** Control Flow

**Description:** Flattens control flow by merging basic blocks

**Effects:**
- Simplifies control flow
- May improve branch prediction
- Reduces basic block count

---

### --float2int

**Name:** Float2int

**Category:** General

**Description:** LLVM optimization pass: Float2int

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --forceattrs

**Name:** Forceattrs

**Category:** General

**Description:** LLVM optimization pass: Forceattrs

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --functionattrs

**Name:** Function Attributes

**Category:** Function Analysis

**Description:** Infers function attributes

**Effects:**
- Adds function attributes
- Enables other optimizations
- Improves analysis precision

---

### --globaldce

**Name:** Global Dead Code Elimination

**Category:** Dead Code Elimination

**Description:** Removes dead global variables and functions

**Effects:**
- Removes unused globals
- Reduces binary size
- Improves link time

---

### --globalopt

**Name:** Global Variable Optimizer

**Category:** Global Optimization

**Description:** Optimizes global variables

**Effects:**
- Optimizes global variable usage
- May internalize globals
- Improves memory layout

---

### --globalsplit

**Name:** Globalsplit

**Category:** General

**Description:** LLVM optimization pass: Globalsplit

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --guard-widening

**Name:** GuardWidening

**Category:** General

**Description:** LLVM optimization pass: GuardWidening

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --gvn

**Name:** Global Value Numbering

**Category:** Value Numbering

**Description:** Eliminates redundant computations globally

**Effects:**
- Eliminates global redundancies
- Improves performance
- May increase compilation time

---

### --gvn-hoist

**Name:** Global Value Numbering Hoisting

**Category:** Code Motion

**Description:** Hoists computations to reduce redundancy

**Effects:**
- Reduces redundant computations
- May increase register pressure
- Improves performance

---

### --hotcoldsplit

**Name:** Hotcoldsplit

**Category:** General

**Description:** LLVM optimization pass: Hotcoldsplit

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --indvars

**Name:** Indvars

**Category:** General

**Description:** LLVM optimization pass: Indvars

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --infer-address-spaces

**Name:** InferAddressSpaces

**Category:** General

**Description:** LLVM optimization pass: InferAddressSpaces

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --inferattrs

**Name:** Inferattrs

**Category:** General

**Description:** LLVM optimization pass: Inferattrs

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --inject-tli-mappings

**Name:** InjectTliMappings

**Category:** General

**Description:** LLVM optimization pass: InjectTliMappings

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --inline

**Name:** Function Inlining

**Category:** Function Optimization

**Description:** Inlines function calls

**Effects:**
- Eliminates call overhead
- Enables other optimizations
- May increase code size

---

### --insert-gcov-profiling

**Name:** InsertGcovProfiling

**Category:** General

**Description:** LLVM optimization pass: InsertGcovProfiling

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --instcombine

**Name:** Instruction Combining

**Category:** Instruction Combining

**Description:** Combines instructions to reduce count

**Effects:**
- Combines instructions
- Reduces instruction count
- Improves performance

---

### --instnamer

**Name:** Instnamer

**Category:** General

**Description:** LLVM optimization pass: Instnamer

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --instsimplify

**Name:** Instruction Simplification

**Category:** Instruction Simplification

**Description:** Simplifies instructions

**Effects:**
- Simplifies complex instructions
- Reduces computation
- May improve performance

---

### --ipconstprop

**Name:** Ipconstprop

**Category:** General

**Description:** LLVM optimization pass: Ipconstprop

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --ipsccp

**Name:** Interprocedural Sparse Conditional Constant Propagation

**Category:** Constant Propagation

**Description:** Propagates constants across function boundaries

**Effects:**
- Propagates constants globally
- Enables dead code elimination
- Improves performance

---

### --irce

**Name:** Irce

**Category:** General

**Description:** LLVM optimization pass: Irce

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --jump-threading

**Name:** Jump Threading

**Category:** Control Flow

**Description:** Threads jumps through conditional blocks

**Effects:**
- Reduces branch overhead
- Improves control flow
- May duplicate code

---

### --lcssa

**Name:** Lcssa

**Category:** General

**Description:** LLVM optimization pass: Lcssa

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --libcalls-shrinkwrap

**Name:** LibcallsShrinkwrap

**Category:** General

**Description:** LLVM optimization pass: LibcallsShrinkwrap

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --licm

**Name:** Loop Invariant Code Motion

**Category:** Loop Optimization

**Description:** Moves loop-invariant code out of loops

**Effects:**
- Reduces loop overhead
- Improves performance
- May increase register pressure

---

### --load-store-vectorizer

**Name:** Load/Store Vectorizer

**Category:** Vectorization

**Description:** Vectorizes adjacent loads and stores

**Effects:**
- Improves memory throughput
- Reduces instruction count
- May require vector hardware

---

### --loop-data-prefetch

**Name:** LoopDataPrefetch

**Category:** General

**Description:** LLVM optimization pass: LoopDataPrefetch

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-deletion

**Name:** Loop Deletion

**Category:** Loop Optimization

**Description:** Removes loops that don't affect program output

**Effects:**
- Removes dead loops
- Reduces execution time
- Improves performance

---

### --loop-distribute

**Name:** LoopDistribute

**Category:** General

**Description:** LLVM optimization pass: LoopDistribute

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-fusion

**Name:** LoopFusion

**Category:** General

**Description:** LLVM optimization pass: LoopFusion

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-guard-widening

**Name:** LoopGuardWidening

**Category:** General

**Description:** LLVM optimization pass: LoopGuardWidening

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-idiom

**Name:** LoopIdiom

**Category:** General

**Description:** LLVM optimization pass: LoopIdiom

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-instsimplify

**Name:** Loop Instruction Simplification

**Category:** Loop Optimization

**Description:** Simplifies instructions within loops

**Effects:**
- Simplifies loop instructions
- Reduces loop overhead
- Improves performance

---

### --loop-interchange

**Name:** LoopInterchange

**Category:** General

**Description:** LLVM optimization pass: LoopInterchange

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-load-elim

**Name:** LoopLoadElim

**Category:** General

**Description:** LLVM optimization pass: LoopLoadElim

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-predication

**Name:** LoopPredication

**Category:** General

**Description:** LLVM optimization pass: LoopPredication

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-reroll

**Name:** Loop Rerolling

**Category:** Loop Optimization

**Description:** Rerolls unrolled loops

**Effects:**
- Reduces code size
- May improve cache performance
- Trades size for speed

---

### --loop-rotate

**Name:** Loop Rotation

**Category:** Loop Optimization

**Description:** Rotates loops to improve optimization

**Effects:**
- Improves loop analysis
- Enables other optimizations
- May duplicate code

---

### --loop-simplify

**Name:** LoopSimplify

**Category:** General

**Description:** LLVM optimization pass: LoopSimplify

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-simplifycfg

**Name:** Loop Simplify CFG

**Category:** Loop Optimization

**Description:** Simplifies control flow in loops

**Effects:**
- Simplifies loop structure
- Enables other optimizations
- Improves analysis

---

### --loop-sink

**Name:** LoopSink

**Category:** General

**Description:** LLVM optimization pass: LoopSink

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-unroll

**Name:** Loop Unrolling

**Category:** Loop Optimization

**Description:** Unrolls loops to reduce overhead

**Effects:**
- Reduces loop overhead
- May increase code size
- Improves performance

---

### --loop-unroll-and-jam

**Name:** LoopUnrollAndJam

**Category:** General

**Description:** LLVM optimization pass: LoopUnrollAndJam

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-unswitch

**Name:** LoopUnswitch

**Category:** General

**Description:** LLVM optimization pass: LoopUnswitch

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-vectorize

**Name:** Loop Vectorization

**Category:** Vectorization

**Description:** Vectorizes loops for SIMD execution

**Effects:**
- Enables SIMD execution
- Improves performance
- Requires vector hardware

---

### --loop-versioning

**Name:** LoopVersioning

**Category:** General

**Description:** LLVM optimization pass: LoopVersioning

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loop-versioning-licm

**Name:** LoopVersioningLicm

**Category:** General

**Description:** LLVM optimization pass: LoopVersioningLicm

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --lower-constant-intrinsics

**Name:** Lower Constant Intrinsics

**Category:** Intrinsic Lowering

**Description:** Lowers constant intrinsics to simple instructions

**Effects:**
- Simplifies intrinsics
- Reduces complexity
- Enables other optimizations

---

### --lower-expect

**Name:** Lower Expect Intrinsics

**Category:** Intrinsic Lowering

**Description:** Lowers expect intrinsics

**Effects:**
- Removes expect intrinsics
- Simplifies code
- Maintains branch hints

---

### --lower-guard-intrinsic

**Name:** LowerGuardIntrinsic

**Category:** General

**Description:** LLVM optimization pass: LowerGuardIntrinsic

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --lower-matrix-intrinsics

**Name:** LowerMatrixIntrinsics

**Category:** General

**Description:** LLVM optimization pass: LowerMatrixIntrinsics

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --lower-widenable-condition

**Name:** LowerWidenableCondition

**Category:** General

**Description:** LLVM optimization pass: LowerWidenableCondition

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --loweratomic

**Name:** Loweratomic

**Category:** General

**Description:** LLVM optimization pass: Loweratomic

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --lowerinvoke

**Name:** Lowerinvoke

**Category:** General

**Description:** LLVM optimization pass: Lowerinvoke

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --lowerswitch

**Name:** Lowerswitch

**Category:** General

**Description:** LLVM optimization pass: Lowerswitch

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --mem2reg

**Name:** Promote Memory to Register

**Category:** Memory Optimization

**Description:** Promotes memory allocations to registers

**Effects:**
- Reduces memory traffic
- Improves performance
- Enables other optimizations

---

### --memcpyopt

**Name:** Memory Copy Optimization

**Category:** Memory Optimization

**Description:** Optimizes memory copy operations

**Effects:**
- Optimizes memory operations
- May eliminate redundant copies
- Improves performance

---

### --mergefunc

**Name:** Merge Functions

**Category:** Function Optimization

**Description:** Merges identical functions

**Effects:**
- Reduces code size
- May improve cache performance
- Eliminates duplication

---

### --mergeicmps

**Name:** Mergeicmps

**Category:** General

**Description:** LLVM optimization pass: Mergeicmps

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --mergereturn

**Name:** Mergereturn

**Category:** General

**Description:** LLVM optimization pass: Mergereturn

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --mldst-motion

**Name:** Machine LICM

**Category:** Loop Optimization

**Description:** Moves loads and stores out of loops

**Effects:**
- Reduces loop overhead
- Improves memory performance
- May increase register pressure

---

### --name-anon-globals

**Name:** NameAnonGlobals

**Category:** General

**Description:** LLVM optimization pass: NameAnonGlobals

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --nary-reassociate

**Name:** N-ary Reassociation

**Category:** Algebraic Optimization

**Description:** Reassociates n-ary operations

**Effects:**
- Improves instruction scheduling
- May reduce instruction count
- Enables other optimizations

---

### --newgvn

**Name:** New Global Value Numbering

**Category:** Value Numbering

**Description:** New implementation of global value numbering

**Effects:**
- More precise value numbering
- Better optimization
- May increase compilation time

---

### --partial-inliner

**Name:** PartialInliner

**Category:** General

**Description:** LLVM optimization pass: PartialInliner

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --partially-inline-libcalls

**Name:** PartiallyInlineLibcalls

**Category:** General

**Description:** LLVM optimization pass: PartiallyInlineLibcalls

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --pgo-memop-opt

**Name:** PgoMemopOpt

**Category:** General

**Description:** LLVM optimization pass: PgoMemopOpt

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --post-inline-ee-instrument

**Name:** PostInlineEeInstrument

**Category:** General

**Description:** LLVM optimization pass: PostInlineEeInstrument

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --prune-eh

**Name:** PruneEh

**Category:** General

**Description:** LLVM optimization pass: PruneEh

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --reassociate

**Name:** Reassociate

**Category:** Algebraic Optimization

**Description:** Reassociates expressions

**Effects:**
- Improves expression evaluation
- Enables other optimizations
- May change execution order

---

### --redundant-dbg-inst-elim

**Name:** RedundantDbgInstElim

**Category:** General

**Description:** LLVM optimization pass: RedundantDbgInstElim

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --reg2mem

**Name:** Reg2mem

**Category:** General

**Description:** LLVM optimization pass: Reg2mem

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --rewrite-statepoints-for-gc

**Name:** RewriteStatepointsForGc

**Category:** General

**Description:** LLVM optimization pass: RewriteStatepointsForGc

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --rpo-functionattrs

**Name:** RpoFunctionattrs

**Category:** General

**Description:** LLVM optimization pass: RpoFunctionattrs

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --sancov

**Name:** Sancov

**Category:** General

**Description:** LLVM optimization pass: Sancov

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --scalarizer

**Name:** Scalarizer

**Category:** General

**Description:** LLVM optimization pass: Scalarizer

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --sccp

**Name:** Sparse Conditional Constant Propagation

**Category:** Constant Propagation

**Description:** Propagates constants conditionally

**Effects:**
- Propagates constants
- Enables dead code elimination
- Improves performance

---

### --separate-const-offset-from-gep

**Name:** SeparateConstOffsetFromGep

**Category:** General

**Description:** LLVM optimization pass: SeparateConstOffsetFromGep

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --simple-loop-unswitch

**Name:** SimpleLoopUnswitch

**Category:** General

**Description:** LLVM optimization pass: SimpleLoopUnswitch

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --simplifycfg

**Name:** Simplify Control Flow Graph

**Category:** Control Flow

**Description:** Simplifies control flow

**Effects:**
- Simplifies branches
- Merges basic blocks
- Improves control flow

---

### --sink

**Name:** Sink

**Category:** General

**Description:** LLVM optimization pass: Sink

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --slp-vectorizer

**Name:** Superword Level Parallelism Vectorizer

**Category:** Vectorization

**Description:** Vectorizes straight-line code

**Effects:**
- Vectorizes arithmetic operations
- Improves performance
- Requires vector hardware

---

### --slsr

**Name:** Slsr

**Category:** General

**Description:** LLVM optimization pass: Slsr

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --speculative-execution

**Name:** SpeculativeExecution

**Category:** General

**Description:** LLVM optimization pass: SpeculativeExecution

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --sroa

**Name:** Scalar Replacement of Aggregates

**Category:** Memory Optimization

**Description:** Replaces aggregates with scalars

**Effects:**
- Improves memory access
- Enables other optimizations
- May increase register usage

---

### --strip

**Name:** Strip

**Category:** General

**Description:** LLVM optimization pass: Strip

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --strip-dead-prototypes

**Name:** StripDeadPrototypes

**Category:** General

**Description:** LLVM optimization pass: StripDeadPrototypes

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --strip-debug-declare

**Name:** StripDebugDeclare

**Category:** General

**Description:** LLVM optimization pass: StripDebugDeclare

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --strip-nondebug

**Name:** StripNondebug

**Category:** General

**Description:** LLVM optimization pass: StripNondebug

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### --tailcallelim

**Name:** Tailcallelim

**Category:** General

**Description:** LLVM optimization pass: Tailcallelim

**Effects:**
- Optimizes LLVM IR
- May improve performance

---

### -loop-reduce

**Name:** Loop Strength Reduction

**Category:** Loop Optimization

**Description:** Reduces loop strength by replacing expensive operations

**Effects:**
- Reduces loop overhead
- Improves performance
- May change loop structure

---

