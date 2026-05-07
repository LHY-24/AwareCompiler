# LLVM Pass Synergy Relationships

This document contains information about synergistic relationships between LLVM optimization passes.

## Overview

Pass synergy occurs when one pass enables or enhances the effectiveness of another pass. The synergy data is based on analysis of 19,603 programs, showing how often pass combinations provide beneficial effects.

## Synergy Calculation

The synergy score is calculated as: `synergy_count / total_programs`

Where:
- `synergy_count`: Number of programs where the pass combination showed synergy
- `total_programs`: 19,603 (total programs analyzed)

## Pass Synergy Data

### --adce

**Synergistic relationships for --adce:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn | 90 | 0.0046 |
| --sroa | 80 | 0.0041 |
| --jump-threading | 77 | 0.0039 |
| --mem2reg | 76 | 0.0039 |
| --simplifycfg | 71 | 0.0036 |
| --gvn-hoist | 64 | 0.0033 |
| --loop-simplifycfg | 61 | 0.0031 |
| --inline | 50 | 0.0026 |
| --early-cse | 33 | 0.0017 |
| --early-cse-memssa | 31 | 0.0016 |
| --die | 26 | 0.0013 |
| --newgvn | 21 | 0.0011 |
| --instcombine | 19 | 0.0010 |
| --elim-avail-extern | 18 | 0.0009 |
| --reassociate | 17 | 0.0009 |
| --licm | 10 | 0.0005 |
| --ipsccp | 9 | 0.0005 |
| --dse | 8 | 0.0004 |
| --lower-expect | 7 | 0.0004 |
| --loop-instsimplify | 5 | 0.0003 |
| --instsimplify | 4 | 0.0002 |
| --aggressive-instcombine | 4 | 0.0002 |
| --lower-constant-intrinsics | 4 | 0.0002 |
| --sccp | 3 | 0.0002 |
| --slp-vectorizer | 2 | 0.0001 |
| --bdce | 2 | 0.0001 |
| --dce | 2 | 0.0001 |
| --load-store-vectorizer | 1 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |

---

### --aggressive-instcombine

**Synergistic relationships for --aggressive-instcombine:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --ipsccp | 293 | 0.0149 |
| --mem2reg | 288 | 0.0147 |
| --sroa | 288 | 0.0147 |
| --gvn | 287 | 0.0146 |
| --simplifycfg | 286 | 0.0146 |
| --early-cse-memssa | 285 | 0.0145 |
| --early-cse | 285 | 0.0145 |
| --newgvn | 285 | 0.0145 |
| --jump-threading | 278 | 0.0142 |
| --loop-simplifycfg | 257 | 0.0131 |
| --gvn-hoist | 240 | 0.0122 |
| --licm | 177 | 0.0090 |
| --inline | 168 | 0.0086 |
| --globalopt | 151 | 0.0077 |
| --elim-avail-extern | 116 | 0.0059 |
| --mergefunc | 101 | 0.0052 |
| --instsimplify | 53 | 0.0027 |
| --reassociate | 50 | 0.0026 |
| --lower-constant-intrinsics | 43 | 0.0022 |
| --lower-expect | 43 | 0.0022 |
| --dse | 27 | 0.0014 |
| --globaldce | 6 | 0.0003 |
| --flattencfg | 5 | 0.0003 |
| --adce | 4 | 0.0002 |
| --loop-instsimplify | 3 | 0.0002 |
| --bdce | 2 | 0.0001 |
| --dce | 2 | 0.0001 |
| --die | 2 | 0.0001 |
| --prune-eh | 1 | 0.0001 |
| --loweratomic | 1 | 0.0001 |
| --instcombine | 1 | 0.0001 |
| --loop-rotate | 1 | 0.0001 |
| --load-store-vectorizer | 1 | 0.0001 |

---

### --bdce

**Synergistic relationships for --bdce:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn | 75 | 0.0038 |
| --simplifycfg | 64 | 0.0033 |
| --sroa | 63 | 0.0032 |
| --jump-threading | 62 | 0.0032 |
| --mem2reg | 59 | 0.0030 |
| --gvn-hoist | 50 | 0.0026 |
| --loop-simplifycfg | 50 | 0.0026 |
| --inline | 37 | 0.0019 |
| --die | 26 | 0.0013 |
| --early-cse | 17 | 0.0009 |
| --reassociate | 16 | 0.0008 |
| --early-cse-memssa | 15 | 0.0008 |
| --newgvn | 15 | 0.0008 |
| --elim-avail-extern | 14 | 0.0007 |
| --ipsccp | 9 | 0.0005 |
| --dse | 8 | 0.0004 |
| --lower-expect | 6 | 0.0003 |
| --licm | 4 | 0.0002 |
| --sccp | 3 | 0.0002 |
| --lower-constant-intrinsics | 3 | 0.0002 |
| --loop-instsimplify | 3 | 0.0002 |
| --load-store-vectorizer | 2 | 0.0001 |
| --slp-vectorizer | 2 | 0.0001 |
| --aggressive-instcombine | 2 | 0.0001 |
| --instcombine | 1 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |

---

### --break-crit-edges

**Synergistic relationships for --break-crit-edges:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 45 | 0.0023 |
| --simplifycfg | 16 | 0.0008 |
| --jump-threading | 3 | 0.0002 |
| --gvn | 1 | 0.0001 |

---

### --correlated-propagation

**Synergistic relationships for --correlated-propagation:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 34 | 0.0017 |
| --simplifycfg | 34 | 0.0017 |
| --early-cse-memssa | 25 | 0.0013 |
| --early-cse | 25 | 0.0013 |
| --newgvn | 25 | 0.0013 |
| --jump-threading | 20 | 0.0010 |
| --gvn | 18 | 0.0009 |
| --gvn-hoist | 11 | 0.0006 |
| --lower-constant-intrinsics | 4 | 0.0002 |
| --load-store-vectorizer | 4 | 0.0002 |
| --loop-reroll | 4 | 0.0002 |
| --mergefunc | 3 | 0.0002 |
| --nary-reassociate | 2 | 0.0001 |
| --slp-vectorizer | 2 | 0.0001 |
| --adce | 1 | 0.0001 |
| --bdce | 1 | 0.0001 |
| --dce | 1 | 0.0001 |
| --die | 1 | 0.0001 |
| --dse | 1 | 0.0001 |
| --lower-expect | 1 | 0.0001 |
| --reassociate | 1 | 0.0001 |
| --sroa | 1 | 0.0001 |
| --globalopt | 1 | 0.0001 |
| --ipsccp | 1 | 0.0001 |

---

### --dce

**Synergistic relationships for --dce:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn | 75 | 0.0038 |
| --simplifycfg | 63 | 0.0032 |
| --sroa | 63 | 0.0032 |
| --jump-threading | 61 | 0.0031 |
| --mem2reg | 59 | 0.0030 |
| --gvn-hoist | 50 | 0.0026 |
| --loop-simplifycfg | 50 | 0.0026 |
| --inline | 37 | 0.0019 |
| --die | 26 | 0.0013 |
| --early-cse | 16 | 0.0008 |
| --reassociate | 16 | 0.0008 |
| --early-cse-memssa | 14 | 0.0007 |
| --newgvn | 14 | 0.0007 |
| --elim-avail-extern | 14 | 0.0007 |
| --ipsccp | 9 | 0.0005 |
| --dse | 8 | 0.0004 |
| --lower-expect | 6 | 0.0003 |
| --licm | 4 | 0.0002 |
| --sccp | 3 | 0.0002 |
| --lower-constant-intrinsics | 3 | 0.0002 |
| --loop-instsimplify | 3 | 0.0002 |
| --slp-vectorizer | 2 | 0.0001 |
| --aggressive-instcombine | 2 | 0.0001 |
| --load-store-vectorizer | 1 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |

---

### --deadargelim

**Synergistic relationships for --deadargelim:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --mergefunc | 1 | 0.0001 |

---

### --die

**Synergistic relationships for --die:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn | 75 | 0.0038 |
| --simplifycfg | 63 | 0.0032 |
| --sroa | 63 | 0.0032 |
| --jump-threading | 61 | 0.0031 |
| --mem2reg | 59 | 0.0030 |
| --gvn-hoist | 50 | 0.0026 |
| --loop-simplifycfg | 50 | 0.0026 |
| --inline | 37 | 0.0019 |
| --die | 26 | 0.0013 |
| --early-cse | 16 | 0.0008 |
| --reassociate | 16 | 0.0008 |
| --elim-avail-extern | 14 | 0.0007 |
| --early-cse-memssa | 13 | 0.0007 |
| --newgvn | 13 | 0.0007 |
| --ipsccp | 9 | 0.0005 |
| --dse | 8 | 0.0004 |
| --lower-expect | 6 | 0.0003 |
| --licm | 4 | 0.0002 |
| --sccp | 3 | 0.0002 |
| --lower-constant-intrinsics | 3 | 0.0002 |
| --loop-instsimplify | 3 | 0.0002 |
| --slp-vectorizer | 2 | 0.0001 |
| --aggressive-instcombine | 2 | 0.0001 |
| --load-store-vectorizer | 1 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |

---

### --dse

**Synergistic relationships for --dse:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn | 882 | 0.0450 |
| --simplifycfg | 865 | 0.0441 |
| --newgvn | 861 | 0.0439 |
| --early-cse | 852 | 0.0435 |
| --early-cse-memssa | 845 | 0.0431 |
| --jump-threading | 822 | 0.0419 |
| --loop-simplifycfg | 787 | 0.0401 |
| --gvn-hoist | 734 | 0.0374 |
| --elim-avail-extern | 468 | 0.0239 |
| --inline | 371 | 0.0189 |
| --instcombine | 324 | 0.0165 |
| --licm | 222 | 0.0113 |
| --instsimplify | 139 | 0.0071 |
| --lower-expect | 56 | 0.0029 |
| --lower-constant-intrinsics | 54 | 0.0028 |
| --sroa | 48 | 0.0024 |
| --mem2reg | 47 | 0.0024 |
| --reassociate | 43 | 0.0022 |
| --loop-instsimplify | 36 | 0.0018 |
| --aggressive-instcombine | 27 | 0.0014 |
| --load-store-vectorizer | 19 | 0.0010 |
| --adce | 15 | 0.0008 |
| --bdce | 15 | 0.0008 |
| --dce | 15 | 0.0008 |
| --die | 15 | 0.0008 |
| --ipsccp | 13 | 0.0007 |
| --globalopt | 11 | 0.0006 |
| --slp-vectorizer | 9 | 0.0005 |
| --mergefunc | 9 | 0.0005 |
| --sccp | 7 | 0.0004 |
| --nary-reassociate | 3 | 0.0002 |
| --dse | 3 | 0.0002 |
| --mldst-motion | 1 | 0.0001 |
| --loop-rotate | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |

---

### --early-cse

**Synergistic relationships for --early-cse:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 7061 | 0.3602 |
| --simplifycfg | 7022 | 0.3582 |
| --mem2reg | 6911 | 0.3525 |
| --sroa | 6909 | 0.3524 |
| --jump-threading | 6718 | 0.3427 |
| --loop-simplifycfg | 6264 | 0.3195 |
| --gvn-hoist | 5673 | 0.2894 |
| --inline | 4262 | 0.2174 |
| --gvn | 2421 | 0.1235 |
| --elim-avail-extern | 2286 | 0.1166 |
| --licm | 1702 | 0.0868 |
| --newgvn | 1628 | 0.0830 |
| --early-cse-memssa | 1355 | 0.0691 |
| --dse | 913 | 0.0466 |
| --instsimplify | 741 | 0.0378 |
| --lower-constant-intrinsics | 316 | 0.0161 |
| --lower-expect | 309 | 0.0158 |
| --aggressive-instcombine | 288 | 0.0147 |
| --reassociate | 257 | 0.0131 |
| --loop-instsimplify | 213 | 0.0109 |
| --load-store-vectorizer | 161 | 0.0082 |
| --early-cse | 159 | 0.0081 |
| --adce | 94 | 0.0048 |
| --bdce | 78 | 0.0040 |
| --dce | 77 | 0.0039 |
| --die | 77 | 0.0039 |
| --mergefunc | 61 | 0.0031 |
| --globalopt | 56 | 0.0029 |
| --slp-vectorizer | 50 | 0.0026 |
| --ipsccp | 49 | 0.0025 |
| --sccp | 40 | 0.0020 |
| --nary-reassociate | 27 | 0.0014 |
| --correlated-propagation | 23 | 0.0012 |
| --slsr | 13 | 0.0007 |
| --loop-reroll | 10 | 0.0005 |
| --mldst-motion | 9 | 0.0005 |
| --prune-eh | 6 | 0.0003 |
| --flattencfg | 6 | 0.0003 |
| --loop-rotate | 6 | 0.0003 |
| --memcpyopt | 4 | 0.0002 |
| --indvars | 2 | 0.0001 |
| --loop-fusion | 1 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --early-cse-memssa

**Synergistic relationships for --early-cse-memssa:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 7062 | 0.3603 |
| --simplifycfg | 7023 | 0.3583 |
| --early-cse | 6994 | 0.3568 |
| --sroa | 6976 | 0.3559 |
| --mem2reg | 6968 | 0.3555 |
| --jump-threading | 6718 | 0.3427 |
| --loop-simplifycfg | 6264 | 0.3195 |
| --gvn-hoist | 5673 | 0.2894 |
| --inline | 4233 | 0.2159 |
| --gvn | 3145 | 0.1604 |
| --elim-avail-extern | 2286 | 0.1166 |
| --licm | 1702 | 0.0868 |
| --dse | 913 | 0.0466 |
| --instsimplify | 741 | 0.0378 |
| --newgvn | 604 | 0.0308 |
| --lower-constant-intrinsics | 316 | 0.0161 |
| --lower-expect | 309 | 0.0158 |
| --aggressive-instcombine | 288 | 0.0147 |
| --reassociate | 257 | 0.0131 |
| --loop-instsimplify | 213 | 0.0109 |
| --load-store-vectorizer | 162 | 0.0083 |
| --early-cse-memssa | 144 | 0.0073 |
| --adce | 94 | 0.0048 |
| --bdce | 78 | 0.0040 |
| --dce | 77 | 0.0039 |
| --die | 77 | 0.0039 |
| --mergefunc | 61 | 0.0031 |
| --globalopt | 56 | 0.0029 |
| --slp-vectorizer | 50 | 0.0026 |
| --ipsccp | 49 | 0.0025 |
| --sccp | 40 | 0.0020 |
| --nary-reassociate | 27 | 0.0014 |
| --correlated-propagation | 23 | 0.0012 |
| --slsr | 13 | 0.0007 |
| --loop-reroll | 11 | 0.0006 |
| --mldst-motion | 9 | 0.0005 |
| --prune-eh | 6 | 0.0003 |
| --flattencfg | 6 | 0.0003 |
| --loop-rotate | 6 | 0.0003 |
| --memcpyopt | 4 | 0.0002 |
| --indvars | 2 | 0.0001 |
| --loop-fusion | 1 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --elim-avail-extern

**Synergistic relationships for --elim-avail-extern:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 2286 | 0.1166 |
| --early-cse | 2286 | 0.1166 |
| --newgvn | 2286 | 0.1166 |
| --mem2reg | 2286 | 0.1166 |
| --sroa | 2286 | 0.1166 |
| --instcombine | 2285 | 0.1166 |
| --simplifycfg | 2260 | 0.1153 |
| --gvn | 2228 | 0.1137 |
| --jump-threading | 2179 | 0.1112 |
| --loop-simplifycfg | 2064 | 0.1053 |
| --gvn-hoist | 1979 | 0.1010 |
| --licm | 626 | 0.0319 |
| --dse | 468 | 0.0239 |
| --instsimplify | 393 | 0.0200 |
| --lower-constant-intrinsics | 306 | 0.0156 |
| --lower-expect | 306 | 0.0156 |
| --inline | 201 | 0.0103 |
| --aggressive-instcombine | 116 | 0.0059 |
| --reassociate | 69 | 0.0035 |
| --load-store-vectorizer | 61 | 0.0031 |
| --loop-instsimplify | 49 | 0.0025 |
| --mergefunc | 46 | 0.0023 |
| --globalopt | 31 | 0.0016 |
| --slp-vectorizer | 22 | 0.0011 |
| --adce | 18 | 0.0009 |
| --bdce | 14 | 0.0007 |
| --dce | 14 | 0.0007 |
| --die | 14 | 0.0007 |
| --ipsccp | 11 | 0.0006 |
| --sccp | 11 | 0.0006 |
| --nary-reassociate | 7 | 0.0004 |
| --loop-rotate | 5 | 0.0003 |
| --memcpyopt | 2 | 0.0001 |
| --flattencfg | 2 | 0.0001 |
| --mldst-motion | 2 | 0.0001 |
| --prune-eh | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --flattencfg

**Synergistic relationships for --flattencfg:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 335 | 0.0171 |
| --gvn | 161 | 0.0082 |
| --gvn-hoist | 111 | 0.0057 |
| --early-cse-memssa | 69 | 0.0035 |
| --newgvn | 60 | 0.0031 |
| --early-cse | 46 | 0.0023 |
| --jump-threading | 27 | 0.0014 |
| --loop-simplifycfg | 7 | 0.0004 |
| --mem2reg | 7 | 0.0004 |
| --sroa | 7 | 0.0004 |
| --simplifycfg | 6 | 0.0003 |
| --licm | 6 | 0.0003 |
| --aggressive-instcombine | 5 | 0.0003 |
| --adce | 4 | 0.0002 |
| --inline | 3 | 0.0002 |
| --ipsccp | 3 | 0.0002 |
| --load-store-vectorizer | 2 | 0.0001 |
| --elim-avail-extern | 2 | 0.0001 |
| --globalopt | 1 | 0.0001 |
| --mergefunc | 1 | 0.0001 |

---

### --float2int

**Synergistic relationships for --float2int:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 1 | 0.0001 |
| --early-cse | 1 | 0.0001 |
| --newgvn | 1 | 0.0001 |

---

### --functionattrs

**Synergistic relationships for --functionattrs:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse | 305 | 0.0156 |
| --early-cse-memssa | 172 | 0.0088 |
| --newgvn | 170 | 0.0087 |
| --gvn | 144 | 0.0073 |
| --gvn-hoist | 87 | 0.0044 |
| --instcombine | 30 | 0.0015 |
| --mergefunc | 4 | 0.0002 |
| --simplifycfg | 3 | 0.0002 |
| --instsimplify | 2 | 0.0001 |
| --reassociate | 2 | 0.0001 |
| --ipsccp | 1 | 0.0001 |
| --adce | 1 | 0.0001 |
| --bdce | 1 | 0.0001 |
| --dce | 1 | 0.0001 |
| --die | 1 | 0.0001 |

---

### --globaldce

**Synergistic relationships for --globaldce:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --ipsccp | 15 | 0.0008 |
| --aggressive-instcombine | 6 | 0.0003 |
| --mergefunc | 1 | 0.0001 |

---

### --globalopt

**Synergistic relationships for --globalopt:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --aggressive-instcombine | 181 | 0.0092 |
| --gvn | 89 | 0.0045 |
| --mergefunc | 79 | 0.0040 |
| --ipsccp | 62 | 0.0032 |
| --mem2reg | 62 | 0.0032 |
| --sroa | 62 | 0.0032 |
| --early-cse-memssa | 60 | 0.0031 |
| --newgvn | 60 | 0.0031 |
| --loop-simplifycfg | 60 | 0.0031 |
| --early-cse | 58 | 0.0030 |
| --instcombine | 56 | 0.0029 |
| --gvn-hoist | 50 | 0.0026 |
| --elim-avail-extern | 31 | 0.0016 |
| --jump-threading | 26 | 0.0013 |
| --inline | 21 | 0.0011 |
| --licm | 17 | 0.0009 |
| --sccp | 14 | 0.0007 |
| --flattencfg | 14 | 0.0007 |
| --dse | 11 | 0.0006 |
| --instsimplify | 10 | 0.0005 |
| --lower-constant-intrinsics | 9 | 0.0005 |
| --lower-expect | 8 | 0.0004 |
| --globaldce | 1 | 0.0001 |
| --loop-instsimplify | 1 | 0.0001 |
| --loweratomic | 1 | 0.0001 |
| --reassociate | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |

---

### --gvn

**Synergistic relationships for --gvn:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 7014 | 0.3578 |
| --simplifycfg | 6953 | 0.3547 |
| --jump-threading | 6637 | 0.3386 |
| --early-cse | 6397 | 0.3263 |
| --mem2reg | 6394 | 0.3262 |
| --sroa | 6394 | 0.3262 |
| --loop-simplifycfg | 6080 | 0.3102 |
| --gvn-hoist | 5576 | 0.2844 |
| --newgvn | 4882 | 0.2490 |
| --inline | 4180 | 0.2132 |
| --early-cse-memssa | 3826 | 0.1952 |
| --elim-avail-extern | 2206 | 0.1125 |
| --licm | 1570 | 0.0801 |
| --dse | 908 | 0.0463 |
| --gvn | 745 | 0.0380 |
| --instsimplify | 740 | 0.0377 |
| --lower-constant-intrinsics | 321 | 0.0164 |
| --lower-expect | 309 | 0.0158 |
| --aggressive-instcombine | 288 | 0.0147 |
| --reassociate | 257 | 0.0131 |
| --loop-instsimplify | 209 | 0.0107 |
| --load-store-vectorizer | 153 | 0.0078 |
| --adce | 94 | 0.0048 |
| --bdce | 78 | 0.0040 |
| --dce | 78 | 0.0040 |
| --die | 78 | 0.0040 |
| --mergefunc | 60 | 0.0031 |
| --globalopt | 57 | 0.0029 |
| --ipsccp | 47 | 0.0024 |
| --slp-vectorizer | 46 | 0.0023 |
| --sccp | 41 | 0.0021 |
| --correlated-propagation | 24 | 0.0012 |
| --nary-reassociate | 23 | 0.0012 |
| --slsr | 13 | 0.0007 |
| --loop-reroll | 11 | 0.0006 |
| --mldst-motion | 9 | 0.0005 |
| --prune-eh | 6 | 0.0003 |
| --flattencfg | 6 | 0.0003 |
| --loop-rotate | 6 | 0.0003 |
| --memcpyopt | 5 | 0.0003 |
| --indvars | 2 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --gvn-hoist

**Synergistic relationships for --gvn-hoist:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 5443 | 0.2777 |
| --jump-threading | 5261 | 0.2684 |
| --early-cse | 4934 | 0.2517 |
| --simplifycfg | 4281 | 0.2184 |
| --loop-simplifycfg | 3955 | 0.2018 |
| --inline | 3307 | 0.1687 |
| --early-cse-memssa | 2406 | 0.1227 |
| --mem2reg | 2402 | 0.1225 |
| --sroa | 2402 | 0.1225 |
| --newgvn | 2397 | 0.1223 |
| --gvn | 1927 | 0.0983 |
| --elim-avail-extern | 1727 | 0.0881 |
| --dse | 735 | 0.0375 |
| --licm | 726 | 0.0370 |
| --instsimplify | 603 | 0.0308 |
| --lower-constant-intrinsics | 300 | 0.0153 |
| --lower-expect | 286 | 0.0146 |
| --aggressive-instcombine | 240 | 0.0122 |
| --reassociate | 205 | 0.0105 |
| --loop-instsimplify | 137 | 0.0070 |
| --load-store-vectorizer | 104 | 0.0053 |
| --adce | 62 | 0.0032 |
| --mergefunc | 52 | 0.0027 |
| --bdce | 50 | 0.0026 |
| --dce | 50 | 0.0026 |
| --die | 50 | 0.0026 |
| --globalopt | 49 | 0.0025 |
| --slp-vectorizer | 41 | 0.0021 |
| --ipsccp | 38 | 0.0019 |
| --sccp | 36 | 0.0018 |
| --nary-reassociate | 21 | 0.0011 |
| --correlated-propagation | 11 | 0.0006 |
| --mldst-motion | 9 | 0.0005 |
| --slsr | 7 | 0.0004 |
| --gvn-hoist | 6 | 0.0003 |
| --memcpyopt | 6 | 0.0003 |
| --loop-rotate | 4 | 0.0002 |
| --prune-eh | 2 | 0.0001 |
| --flattencfg | 2 | 0.0001 |
| --loop-reroll | 2 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --hotcoldsplit

**Synergistic relationships for --hotcoldsplit:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --mergefunc | 4 | 0.0002 |

---

### --indvars

**Synergistic relationships for --indvars:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 32 | 0.0016 |
| --simplifycfg | 20 | 0.0010 |
| --early-cse | 17 | 0.0009 |
| --newgvn | 17 | 0.0009 |
| --early-cse-memssa | 16 | 0.0008 |
| --instcombine | 14 | 0.0007 |
| --jump-threading | 9 | 0.0005 |
| --nary-reassociate | 6 | 0.0003 |
| --loop-reroll | 4 | 0.0002 |
| --load-store-vectorizer | 3 | 0.0002 |
| --slsr | 2 | 0.0001 |
| --correlated-propagation | 2 | 0.0001 |
| --loop-fusion | 2 | 0.0001 |
| --sroa | 2 | 0.0001 |
| --slp-vectorizer | 1 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |

---

### --inferattrs

**Synergistic relationships for --inferattrs:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 32 | 0.0016 |
| --newgvn | 32 | 0.0016 |
| --instcombine | 11 | 0.0006 |
| --gvn | 4 | 0.0002 |
| --dse | 1 | 0.0001 |

---

### --inline

**Synergistic relationships for --inline:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --sroa | 5763 | 0.2940 |
| --mem2reg | 5758 | 0.2937 |
| --instcombine | 5675 | 0.2895 |
| --early-cse | 4489 | 0.2290 |
| --early-cse-memssa | 4437 | 0.2263 |
| --newgvn | 4437 | 0.2263 |
| --gvn | 4383 | 0.2236 |
| --simplifycfg | 4165 | 0.2125 |
| --jump-threading | 4067 | 0.2075 |
| --loop-simplifycfg | 3818 | 0.1948 |
| --gvn-hoist | 3307 | 0.1687 |
| --licm | 980 | 0.0500 |
| --elim-avail-extern | 664 | 0.0339 |
| --dse | 371 | 0.0189 |
| --instsimplify | 303 | 0.0155 |
| --aggressive-instcombine | 168 | 0.0086 |
| --reassociate | 156 | 0.0080 |
| --loop-instsimplify | 151 | 0.0077 |
| --load-store-vectorizer | 77 | 0.0039 |
| --adce | 50 | 0.0026 |
| --ipsccp | 44 | 0.0022 |
| --bdce | 37 | 0.0019 |
| --dce | 37 | 0.0019 |
| --die | 37 | 0.0019 |
| --sccp | 26 | 0.0013 |
| --slp-vectorizer | 21 | 0.0011 |
| --globalopt | 20 | 0.0010 |
| --mldst-motion | 5 | 0.0003 |
| --flattencfg | 3 | 0.0002 |
| --mergefunc | 3 | 0.0002 |
| --memcpyopt | 2 | 0.0001 |
| --prune-eh | 2 | 0.0001 |
| --loop-rotate | 2 | 0.0001 |
| --nary-reassociate | 1 | 0.0001 |

---

### --instcombine

**Synergistic relationships for --instcombine:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse | 7011 | 0.3576 |
| --simplifycfg | 6960 | 0.3550 |
| --newgvn | 6947 | 0.3544 |
| --early-cse-memssa | 6940 | 0.3540 |
| --gvn | 6754 | 0.3445 |
| --jump-threading | 6678 | 0.3407 |
| --loop-simplifycfg | 6242 | 0.3184 |
| --gvn-hoist | 5605 | 0.2859 |
| --sroa | 5365 | 0.2737 |
| --mem2reg | 4567 | 0.2330 |
| --inline | 4216 | 0.2151 |
| --elim-avail-extern | 2284 | 0.1165 |
| --licm | 1694 | 0.0864 |
| --dse | 906 | 0.0462 |
| --instsimplify | 754 | 0.0385 |
| --lower-constant-intrinsics | 318 | 0.0162 |
| --lower-expect | 309 | 0.0158 |
| --aggressive-instcombine | 288 | 0.0147 |
| --reassociate | 258 | 0.0132 |
| --loop-instsimplify | 212 | 0.0108 |
| --load-store-vectorizer | 154 | 0.0079 |
| --adce | 95 | 0.0048 |
| --bdce | 79 | 0.0040 |
| --dce | 78 | 0.0040 |
| --die | 78 | 0.0040 |
| --mergefunc | 62 | 0.0032 |
| --globalopt | 56 | 0.0029 |
| --slp-vectorizer | 50 | 0.0026 |
| --ipsccp | 48 | 0.0024 |
| --sccp | 40 | 0.0020 |
| --correlated-propagation | 24 | 0.0012 |
| --nary-reassociate | 20 | 0.0010 |
| --mldst-motion | 10 | 0.0005 |
| --loop-reroll | 9 | 0.0005 |
| --prune-eh | 6 | 0.0003 |
| --memcpyopt | 6 | 0.0003 |
| --flattencfg | 6 | 0.0003 |
| --loop-rotate | 6 | 0.0003 |
| --slsr | 5 | 0.0003 |
| -loop-reduce | 3 | 0.0002 |
| --loop-deletion | 1 | 0.0001 |

---

### --instsimplify

**Synergistic relationships for --instsimplify:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --sroa | 738 | 0.0376 |
| --mem2reg | 734 | 0.0374 |
| --simplifycfg | 724 | 0.0369 |
| --jump-threading | 708 | 0.0361 |
| --loop-simplifycfg | 657 | 0.0335 |
| --gvn-hoist | 601 | 0.0307 |
| --elim-avail-extern | 393 | 0.0200 |
| --lower-expect | 309 | 0.0158 |
| --lower-constant-intrinsics | 306 | 0.0156 |
| --inline | 297 | 0.0152 |
| --licm | 195 | 0.0099 |
| --dse | 145 | 0.0074 |
| --gvn | 88 | 0.0045 |
| --reassociate | 86 | 0.0044 |
| --early-cse | 53 | 0.0027 |
| --aggressive-instcombine | 53 | 0.0027 |
| --early-cse-memssa | 48 | 0.0024 |
| --die | 47 | 0.0024 |
| --newgvn | 46 | 0.0023 |
| --ipsccp | 35 | 0.0018 |
| --loop-instsimplify | 34 | 0.0017 |
| --adce | 32 | 0.0016 |
| --bdce | 30 | 0.0015 |
| --dce | 30 | 0.0015 |
| --sccp | 29 | 0.0015 |
| --load-store-vectorizer | 26 | 0.0013 |
| --instcombine | 18 | 0.0009 |
| --globalopt | 10 | 0.0005 |
| --mergefunc | 9 | 0.0005 |
| --slp-vectorizer | 5 | 0.0003 |
| --prune-eh | 2 | 0.0001 |
| --nary-reassociate | 2 | 0.0001 |
| --mldst-motion | 1 | 0.0001 |
| --loop-rotate | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |
| --loop-reroll | 1 | 0.0001 |

---

### --ipconstprop

**Synergistic relationships for --ipconstprop:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --globalopt | 36 | 0.0018 |
| --early-cse-memssa | 8 | 0.0004 |
| --early-cse | 8 | 0.0004 |
| --newgvn | 8 | 0.0004 |
| --instcombine | 7 | 0.0004 |
| --instsimplify | 6 | 0.0003 |
| --gvn | 3 | 0.0002 |
| --aggressive-instcombine | 1 | 0.0001 |
| --licm | 1 | 0.0001 |

---

### --ipsccp

**Synergistic relationships for --ipsccp:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --aggressive-instcombine | 296 | 0.0151 |
| --mergefunc | 141 | 0.0072 |
| --globalopt | 131 | 0.0067 |
| --gvn-hoist | 42 | 0.0021 |
| --sroa | 41 | 0.0021 |
| --mem2reg | 40 | 0.0020 |
| --early-cse-memssa | 38 | 0.0019 |
| --early-cse | 38 | 0.0019 |
| --loop-simplifycfg | 38 | 0.0019 |
| --jump-threading | 37 | 0.0019 |
| --simplifycfg | 35 | 0.0018 |
| --inline | 30 | 0.0015 |
| --newgvn | 30 | 0.0015 |
| --instcombine | 22 | 0.0011 |
| --ipsccp | 20 | 0.0010 |
| --gvn | 19 | 0.0010 |
| --flattencfg | 15 | 0.0008 |
| --sccp | 14 | 0.0007 |
| --dse | 13 | 0.0007 |
| --elim-avail-extern | 11 | 0.0006 |
| --instsimplify | 8 | 0.0004 |
| --adce | 8 | 0.0004 |
| --bdce | 8 | 0.0004 |
| --dce | 8 | 0.0004 |
| --die | 8 | 0.0004 |
| --licm | 7 | 0.0004 |
| --reassociate | 7 | 0.0004 |
| --nary-reassociate | 4 | 0.0002 |
| --lower-constant-intrinsics | 2 | 0.0001 |
| --globaldce | 1 | 0.0001 |
| --lower-expect | 1 | 0.0001 |
| --loweratomic | 1 | 0.0001 |
| --loop-instsimplify | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |

---

### --irce

**Synergistic relationships for --irce:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --jump-threading

**Synergistic relationships for --jump-threading:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse | 6589 | 0.3361 |
| --instcombine | 6511 | 0.3321 |
| --sroa | 6435 | 0.3283 |
| --newgvn | 6433 | 0.3282 |
| --mem2reg | 6430 | 0.3280 |
| --early-cse-memssa | 6416 | 0.3273 |
| --gvn-hoist | 5395 | 0.2752 |
| --inline | 4062 | 0.2072 |
| --gvn | 3611 | 0.1842 |
| --loop-simplifycfg | 3508 | 0.1790 |
| --elim-avail-extern | 2179 | 0.1112 |
| --licm | 1496 | 0.0763 |
| --dse | 823 | 0.0420 |
| --instsimplify | 714 | 0.0364 |
| --lower-constant-intrinsics | 345 | 0.0176 |
| --simplifycfg | 339 | 0.0173 |
| --lower-expect | 309 | 0.0158 |
| --aggressive-instcombine | 278 | 0.0142 |
| --reassociate | 231 | 0.0118 |
| --loop-instsimplify | 206 | 0.0105 |
| --load-store-vectorizer | 171 | 0.0087 |
| --mergefunc | 84 | 0.0043 |
| --adce | 78 | 0.0040 |
| --bdce | 63 | 0.0032 |
| --dce | 62 | 0.0032 |
| --die | 62 | 0.0032 |
| --globalopt | 56 | 0.0029 |
| --slp-vectorizer | 52 | 0.0027 |
| --ipsccp | 45 | 0.0023 |
| --sccp | 41 | 0.0021 |
| --correlated-propagation | 23 | 0.0012 |
| --loop-reroll | 16 | 0.0008 |
| --nary-reassociate | 15 | 0.0008 |
| --mldst-motion | 9 | 0.0005 |
| --memcpyopt | 8 | 0.0004 |
| --loop-rotate | 5 | 0.0003 |
| --prune-eh | 4 | 0.0002 |
| --slsr | 3 | 0.0002 |
| --flattencfg | 1 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --licm

**Synergistic relationships for --licm:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 5417 | 0.2763 |
| --early-cse | 4449 | 0.2270 |
| --gvn | 3273 | 0.1670 |
| --simplifycfg | 2043 | 0.1042 |
| --jump-threading | 2023 | 0.1032 |
| --loop-simplifycfg | 1715 | 0.0875 |
| --early-cse-memssa | 1376 | 0.0702 |
| --newgvn | 1238 | 0.0632 |
| --inline | 980 | 0.0500 |
| --gvn-hoist | 904 | 0.0461 |
| --elim-avail-extern | 626 | 0.0319 |
| --dse | 565 | 0.0288 |
| --instsimplify | 461 | 0.0235 |
| --licm | 189 | 0.0096 |
| --aggressive-instcombine | 177 | 0.0090 |
| --lower-constant-intrinsics | 90 | 0.0046 |
| --lower-expect | 90 | 0.0046 |
| --reassociate | 87 | 0.0044 |
| --loop-instsimplify | 62 | 0.0032 |
| --load-store-vectorizer | 41 | 0.0021 |
| --die | 17 | 0.0009 |
| --adce | 15 | 0.0008 |
| --globalopt | 14 | 0.0007 |
| --bdce | 12 | 0.0006 |
| --dce | 12 | 0.0006 |
| --mergefunc | 9 | 0.0005 |
| --slp-vectorizer | 8 | 0.0004 |
| --ipsccp | 8 | 0.0004 |
| --sccp | 6 | 0.0003 |
| --nary-reassociate | 5 | 0.0003 |
| --prune-eh | 3 | 0.0002 |
| --mem2reg | 3 | 0.0002 |
| --sroa | 3 | 0.0002 |
| --mldst-motion | 2 | 0.0001 |
| --flattencfg | 1 | 0.0001 |
| --loop-rotate | 1 | 0.0001 |
| --memcpyopt | 1 | 0.0001 |

---

### --load-store-vectorizer

**Synergistic relationships for --load-store-vectorizer:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 259 | 0.0132 |
| --simplifycfg | 187 | 0.0095 |
| --early-cse | 175 | 0.0089 |
| --jump-threading | 171 | 0.0087 |
| --early-cse-memssa | 158 | 0.0081 |
| --newgvn | 153 | 0.0078 |
| --gvn | 149 | 0.0076 |
| --mem2reg | 140 | 0.0071 |
| --loop-simplifycfg | 135 | 0.0069 |
| --sroa | 129 | 0.0066 |
| --gvn-hoist | 104 | 0.0053 |
| --inline | 77 | 0.0039 |
| --elim-avail-extern | 61 | 0.0031 |
| --licm | 56 | 0.0029 |
| --slp-vectorizer | 41 | 0.0021 |
| --instsimplify | 26 | 0.0013 |
| --dse | 19 | 0.0010 |
| --loop-instsimplify | 16 | 0.0008 |
| --lower-constant-intrinsics | 10 | 0.0005 |
| --mergefunc | 7 | 0.0004 |
| --indvars | 5 | 0.0003 |
| --correlated-propagation | 4 | 0.0002 |
| --nary-reassociate | 4 | 0.0002 |
| --memcpyopt | 3 | 0.0002 |
| --reassociate | 3 | 0.0002 |
| --bdce | 2 | 0.0001 |
| --mldst-motion | 2 | 0.0001 |
| -loop-reduce | 2 | 0.0001 |
| --loop-reroll | 2 | 0.0001 |
| --loop-fusion | 2 | 0.0001 |
| --adce | 1 | 0.0001 |
| --dce | 1 | 0.0001 |
| --die | 1 | 0.0001 |
| --lower-expect | 1 | 0.0001 |
| --slsr | 1 | 0.0001 |
| --aggressive-instcombine | 1 | 0.0001 |

---

### --loop-deletion

**Synergistic relationships for --loop-deletion:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 36 | 0.0018 |
| --gvn | 19 | 0.0010 |
| --jump-threading | 8 | 0.0004 |
| --instcombine | 7 | 0.0004 |
| --early-cse | 5 | 0.0003 |
| --early-cse-memssa | 3 | 0.0002 |
| --newgvn | 3 | 0.0002 |
| --elim-avail-extern | 1 | 0.0001 |
| --loop-simplifycfg | 1 | 0.0001 |
| --mem2reg | 1 | 0.0001 |
| --sccp | 1 | 0.0001 |
| --sroa | 1 | 0.0001 |

---

### --loop-fusion

**Synergistic relationships for --loop-fusion:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --gvn | 6 | 0.0003 |
| --early-cse | 5 | 0.0003 |
| --early-cse-memssa | 3 | 0.0002 |
| --newgvn | 3 | 0.0002 |
| --simplifycfg | 3 | 0.0002 |
| --indvars | 2 | 0.0001 |
| --load-store-vectorizer | 2 | 0.0001 |
| --loop-reroll | 1 | 0.0001 |
| --nary-reassociate | 1 | 0.0001 |

---

### --loop-guard-widening

**Synergistic relationships for --loop-guard-widening:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-idiom

**Synergistic relationships for --loop-idiom:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-instsimplify

**Synergistic relationships for --loop-instsimplify:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --jump-threading | 222 | 0.0113 |
| --simplifycfg | 221 | 0.0113 |
| --gvn-hoist | 217 | 0.0111 |
| --loop-simplifycfg | 217 | 0.0111 |
| --mem2reg | 212 | 0.0108 |
| --sroa | 212 | 0.0108 |
| --inline | 151 | 0.0077 |
| --licm | 123 | 0.0063 |
| --gvn | 49 | 0.0025 |
| --elim-avail-extern | 49 | 0.0025 |
| --dse | 36 | 0.0018 |
| --early-cse | 25 | 0.0013 |
| --reassociate | 25 | 0.0013 |
| --ipsccp | 25 | 0.0013 |
| --sccp | 25 | 0.0013 |
| --early-cse-memssa | 20 | 0.0010 |
| --die | 16 | 0.0008 |
| --load-store-vectorizer | 16 | 0.0008 |
| --newgvn | 15 | 0.0008 |
| --instcombine | 6 | 0.0003 |
| --lower-constant-intrinsics | 4 | 0.0002 |
| --lower-expect | 4 | 0.0002 |
| --adce | 3 | 0.0002 |
| --aggressive-instcombine | 3 | 0.0002 |
| --bdce | 2 | 0.0001 |
| --dce | 2 | 0.0001 |
| --globalopt | 1 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --nary-reassociate | 1 | 0.0001 |

---

### --loop-interchange

**Synergistic relationships for --loop-interchange:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-load-elim

**Synergistic relationships for --loop-load-elim:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --gvn | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-predication

**Synergistic relationships for --loop-predication:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-reroll

**Synergistic relationships for --loop-reroll:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 37 | 0.0019 |
| --simplifycfg | 32 | 0.0016 |
| --gvn | 32 | 0.0016 |
| --jump-threading | 25 | 0.0013 |
| --early-cse | 17 | 0.0009 |
| --newgvn | 17 | 0.0009 |
| --early-cse-memssa | 16 | 0.0008 |
| --instcombine | 16 | 0.0008 |
| --indvars | 9 | 0.0005 |
| --nary-reassociate | 8 | 0.0004 |
| -loop-reduce | 7 | 0.0004 |
| --load-store-vectorizer | 7 | 0.0004 |
| --correlated-propagation | 5 | 0.0003 |
| --mergefunc | 3 | 0.0002 |
| --lower-constant-intrinsics | 2 | 0.0001 |
| --slsr | 2 | 0.0001 |
| --loop-fusion | 2 | 0.0001 |
| --loop-simplifycfg | 1 | 0.0001 |
| --memcpyopt | 1 | 0.0001 |
| --slp-vectorizer | 1 | 0.0001 |
| --sroa | 1 | 0.0001 |
| --instsimplify | 1 | 0.0001 |

---

### --loop-rotate

**Synergistic relationships for --loop-rotate:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --jump-threading | 306 | 0.0156 |
| --gvn | 186 | 0.0095 |
| --licm | 26 | 0.0013 |
| --instcombine | 20 | 0.0010 |
| --early-cse-memssa | 10 | 0.0005 |
| --newgvn | 10 | 0.0005 |
| --early-cse | 9 | 0.0005 |
| --mem2reg | 6 | 0.0003 |
| --sroa | 6 | 0.0003 |
| --elim-avail-extern | 5 | 0.0003 |
| --gvn-hoist | 5 | 0.0003 |
| --loop-simplifycfg | 3 | 0.0002 |
| --inline | 2 | 0.0001 |
| --dse | 1 | 0.0001 |
| --aggressive-instcombine | 1 | 0.0001 |
| --instsimplify | 1 | 0.0001 |
| --lower-constant-intrinsics | 1 | 0.0001 |
| --lower-expect | 1 | 0.0001 |

---

### --loop-simplify

**Synergistic relationships for --loop-simplify:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --gvn | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-simplifycfg

**Synergistic relationships for --loop-simplifycfg:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 6269 | 0.3198 |
| --early-cse | 6269 | 0.3198 |
| --newgvn | 6265 | 0.3196 |
| --instcombine | 6254 | 0.3190 |
| --sroa | 6251 | 0.3189 |
| --mem2reg | 6250 | 0.3188 |
| --gvn-hoist | 5024 | 0.2563 |
| --inline | 3818 | 0.1948 |
| --elim-avail-extern | 2064 | 0.1053 |
| --licm | 1590 | 0.0811 |
| --dse | 787 | 0.0401 |
| --instsimplify | 657 | 0.0335 |
| --lower-constant-intrinsics | 287 | 0.0146 |
| --lower-expect | 285 | 0.0145 |
| --aggressive-instcombine | 257 | 0.0131 |
| --loop-instsimplify | 206 | 0.0105 |
| --reassociate | 205 | 0.0105 |
| --load-store-vectorizer | 135 | 0.0069 |
| --adce | 61 | 0.0031 |
| --bdce | 50 | 0.0026 |
| --dce | 50 | 0.0026 |
| --die | 50 | 0.0026 |
| --globalopt | 47 | 0.0024 |
| --mergefunc | 44 | 0.0022 |
| --slp-vectorizer | 43 | 0.0022 |
| --ipsccp | 38 | 0.0019 |
| --sccp | 36 | 0.0018 |
| --gvn | 25 | 0.0013 |
| --jump-threading | 10 | 0.0005 |
| --nary-reassociate | 8 | 0.0004 |
| --mldst-motion | 8 | 0.0004 |
| --flattencfg | 5 | 0.0003 |
| --prune-eh | 4 | 0.0002 |
| --memcpyopt | 4 | 0.0002 |
| --loop-rotate | 3 | 0.0002 |
| --correlated-propagation | 2 | 0.0001 |
| --loop-reroll | 1 | 0.0001 |
| --slsr | 1 | 0.0001 |
| --simplifycfg | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --loop-sink

**Synergistic relationships for --loop-sink:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-unroll

**Synergistic relationships for --loop-unroll:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-unroll-and-jam

**Synergistic relationships for --loop-unroll-and-jam:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --gvn | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-unswitch

**Synergistic relationships for --loop-unswitch:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-vectorize

**Synergistic relationships for --loop-vectorize:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --loop-versioning-licm

**Synergistic relationships for --loop-versioning-licm:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --lower-constant-intrinsics

**Synergistic relationships for --lower-constant-intrinsics:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 347 | 0.0177 |
| --jump-threading | 345 | 0.0176 |
| --instcombine | 318 | 0.0162 |
| --newgvn | 318 | 0.0162 |
| --early-cse-memssa | 316 | 0.0161 |
| --early-cse | 316 | 0.0161 |
| --elim-avail-extern | 306 | 0.0156 |
| --instsimplify | 306 | 0.0156 |
| --lower-expect | 306 | 0.0156 |
| --mem2reg | 306 | 0.0156 |
| --sroa | 306 | 0.0156 |
| --gvn-hoist | 300 | 0.0153 |
| --loop-simplifycfg | 287 | 0.0146 |
| --licm | 90 | 0.0046 |
| --dse | 54 | 0.0028 |
| --aggressive-instcombine | 43 | 0.0022 |
| --reassociate | 31 | 0.0016 |
| --gvn | 15 | 0.0008 |
| --load-store-vectorizer | 10 | 0.0005 |
| --mergefunc | 10 | 0.0005 |
| --globalopt | 9 | 0.0005 |
| --correlated-propagation | 4 | 0.0002 |
| --loop-instsimplify | 4 | 0.0002 |
| --adce | 4 | 0.0002 |
| --bdce | 3 | 0.0002 |
| --dce | 3 | 0.0002 |
| --die | 3 | 0.0002 |
| --nary-reassociate | 3 | 0.0002 |
| --loop-reroll | 2 | 0.0001 |
| --ipsccp | 2 | 0.0001 |
| --sccp | 2 | 0.0001 |
| --memcpyopt | 1 | 0.0001 |
| --loop-rotate | 1 | 0.0001 |
| --mldst-motion | 1 | 0.0001 |
| --prune-eh | 1 | 0.0001 |
| --slp-vectorizer | 1 | 0.0001 |

---

### --lower-expect

**Synergistic relationships for --lower-expect:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 309 | 0.0158 |
| --early-cse-memssa | 309 | 0.0158 |
| --early-cse | 309 | 0.0158 |
| --gvn | 309 | 0.0158 |
| --instsimplify | 309 | 0.0158 |
| --instcombine | 309 | 0.0158 |
| --jump-threading | 309 | 0.0158 |
| --newgvn | 309 | 0.0158 |
| --sroa | 309 | 0.0158 |
| --mem2reg | 307 | 0.0157 |
| --elim-avail-extern | 306 | 0.0156 |
| --lower-constant-intrinsics | 306 | 0.0156 |
| --gvn-hoist | 286 | 0.0146 |
| --loop-simplifycfg | 285 | 0.0145 |
| --licm | 90 | 0.0046 |
| --dse | 56 | 0.0029 |
| --aggressive-instcombine | 43 | 0.0022 |
| --reassociate | 34 | 0.0017 |
| --globalopt | 8 | 0.0004 |
| --adce | 7 | 0.0004 |
| --mergefunc | 7 | 0.0004 |
| --bdce | 6 | 0.0003 |
| --dce | 6 | 0.0003 |
| --die | 6 | 0.0003 |
| --loop-instsimplify | 4 | 0.0002 |
| --ipsccp | 1 | 0.0001 |
| --sccp | 1 | 0.0001 |
| --load-store-vectorizer | 1 | 0.0001 |
| --loop-rotate | 1 | 0.0001 |
| --prune-eh | 1 | 0.0001 |
| --nary-reassociate | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |
| --slp-vectorizer | 1 | 0.0001 |

---

### --loweratomic

**Synergistic relationships for --loweratomic:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 1 | 0.0001 |
| --aggressive-instcombine | 1 | 0.0001 |
| --globalopt | 1 | 0.0001 |
| --ipsccp | 1 | 0.0001 |
| --early-cse-memssa | 1 | 0.0001 |
| --early-cse | 1 | 0.0001 |

---

### --lowerinvoke

**Synergistic relationships for --lowerinvoke:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 57 | 0.0029 |
| --newgvn | 14 | 0.0007 |
| --instcombine | 11 | 0.0006 |

---

### --lowerswitch

**Synergistic relationships for --lowerswitch:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 42 | 0.0021 |
| --early-cse | 42 | 0.0021 |
| --gvn | 42 | 0.0021 |
| --instcombine | 42 | 0.0021 |
| --jump-threading | 24 | 0.0012 |
| --simplifycfg | 10 | 0.0005 |
| --instsimplify | 8 | 0.0004 |
| --ipsccp | 1 | 0.0001 |
| --loop-simplifycfg | 1 | 0.0001 |
| --gvn-hoist | 1 | 0.0001 |

---

### --mem2reg

**Synergistic relationships for --mem2reg:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 7010 | 0.3576 |
| --early-cse | 7010 | 0.3576 |
| --newgvn | 7003 | 0.3572 |
| --gvn | 6916 | 0.3528 |
| --instcombine | 6873 | 0.3506 |
| --simplifycfg | 6835 | 0.3487 |
| --jump-threading | 6635 | 0.3385 |
| --loop-simplifycfg | 6261 | 0.3194 |
| --gvn-hoist | 5601 | 0.2857 |
| --inline | 4251 | 0.2169 |
| --elim-avail-extern | 2286 | 0.1166 |
| --licm | 1703 | 0.0869 |
| --dse | 898 | 0.0458 |
| --instsimplify | 734 | 0.0374 |
| --lower-expect | 307 | 0.0157 |
| --lower-constant-intrinsics | 306 | 0.0156 |
| --aggressive-instcombine | 288 | 0.0147 |
| --reassociate | 239 | 0.0122 |
| --loop-instsimplify | 213 | 0.0109 |
| --load-store-vectorizer | 140 | 0.0071 |
| --adce | 77 | 0.0039 |
| --bdce | 60 | 0.0031 |
| --dce | 60 | 0.0031 |
| --die | 60 | 0.0031 |
| --globalopt | 55 | 0.0028 |
| --mergefunc | 46 | 0.0023 |
| --slp-vectorizer | 44 | 0.0022 |
| --ipsccp | 40 | 0.0020 |
| --sccp | 38 | 0.0019 |
| --mldst-motion | 9 | 0.0005 |
| --nary-reassociate | 8 | 0.0004 |
| --prune-eh | 6 | 0.0003 |
| --flattencfg | 6 | 0.0003 |
| --loop-rotate | 6 | 0.0003 |
| --memcpyopt | 4 | 0.0002 |
| --loop-deletion | 1 | 0.0001 |

---

### --memcpyopt

**Synergistic relationships for --memcpyopt:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn | 11 | 0.0006 |
| --instcombine | 10 | 0.0005 |
| --simplifycfg | 8 | 0.0004 |
| --jump-threading | 8 | 0.0004 |
| --early-cse-memssa | 7 | 0.0004 |
| --early-cse | 7 | 0.0004 |
| --gvn-hoist | 7 | 0.0004 |
| --newgvn | 7 | 0.0004 |
| --mem2reg | 6 | 0.0003 |
| --loop-simplifycfg | 4 | 0.0002 |
| --sroa | 3 | 0.0002 |
| --elim-avail-extern | 2 | 0.0001 |
| --slp-vectorizer | 2 | 0.0001 |
| --load-store-vectorizer | 2 | 0.0001 |
| --inline | 2 | 0.0001 |
| --licm | 2 | 0.0001 |
| --lower-constant-intrinsics | 1 | 0.0001 |
| --loop-reroll | 1 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --instsimplify | 1 | 0.0001 |

---

### --mergefunc

**Synergistic relationships for --mergefunc:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --ipsccp | 157 | 0.0080 |
| --aggressive-instcombine | 101 | 0.0052 |
| --simplifycfg | 94 | 0.0048 |
| --jump-threading | 84 | 0.0043 |
| --globalopt | 76 | 0.0039 |
| --newgvn | 63 | 0.0032 |
| --instcombine | 62 | 0.0032 |
| --early-cse-memssa | 61 | 0.0031 |
| --early-cse | 61 | 0.0031 |
| --gvn | 60 | 0.0031 |
| --gvn-hoist | 52 | 0.0027 |
| --sroa | 47 | 0.0024 |
| --elim-avail-extern | 46 | 0.0023 |
| --mem2reg | 46 | 0.0023 |
| --loop-simplifycfg | 44 | 0.0022 |
| --lower-constant-intrinsics | 10 | 0.0005 |
| --dse | 9 | 0.0005 |
| --licm | 9 | 0.0005 |
| --instsimplify | 9 | 0.0005 |
| --load-store-vectorizer | 8 | 0.0004 |
| --lower-expect | 7 | 0.0004 |
| --mergefunc | 6 | 0.0003 |
| --correlated-propagation | 3 | 0.0002 |
| --loop-reroll | 3 | 0.0002 |
| --inline | 2 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --slp-vectorizer | 1 | 0.0001 |
| --loop-instsimplify | 1 | 0.0001 |
| --adce | 1 | 0.0001 |
| --bdce | 1 | 0.0001 |
| --dce | 1 | 0.0001 |
| --die | 1 | 0.0001 |
| --reassociate | 1 | 0.0001 |
| --memcpyopt | 1 | 0.0001 |
| --flattencfg | 1 | 0.0001 |
| --globaldce | 1 | 0.0001 |

---

### --mergereturn

**Synergistic relationships for --mergereturn:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 5 | 0.0003 |
| --jump-threading | 3 | 0.0002 |

---

### --mldst-motion

**Synergistic relationships for --mldst-motion:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 10 | 0.0005 |
| --instcombine | 10 | 0.0005 |
| --early-cse | 9 | 0.0005 |
| --gvn-hoist | 9 | 0.0005 |
| --gvn | 9 | 0.0005 |
| --jump-threading | 9 | 0.0005 |
| --mem2reg | 9 | 0.0005 |
| --loop-simplifycfg | 8 | 0.0004 |
| --early-cse-memssa | 8 | 0.0004 |
| --newgvn | 8 | 0.0004 |
| --sroa | 7 | 0.0004 |
| --inline | 5 | 0.0003 |
| --elim-avail-extern | 2 | 0.0001 |
| --load-store-vectorizer | 2 | 0.0001 |
| --slp-vectorizer | 2 | 0.0001 |
| --licm | 2 | 0.0001 |
| --dse | 1 | 0.0001 |
| --instsimplify | 1 | 0.0001 |
| --lower-constant-intrinsics | 1 | 0.0001 |

---

### --nary-reassociate

**Synergistic relationships for --nary-reassociate:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 55 | 0.0028 |
| --early-cse-memssa | 27 | 0.0014 |
| --early-cse | 27 | 0.0014 |
| --newgvn | 27 | 0.0014 |
| --gvn | 23 | 0.0012 |
| --instcombine | 18 | 0.0009 |
| --gvn-hoist | 17 | 0.0009 |
| --jump-threading | 15 | 0.0008 |
| --slsr | 11 | 0.0006 |
| --sroa | 9 | 0.0005 |
| --loop-simplifycfg | 8 | 0.0004 |
| --mem2reg | 8 | 0.0004 |
| --elim-avail-extern | 7 | 0.0004 |
| --indvars | 6 | 0.0003 |
| --licm | 5 | 0.0003 |
| --slp-vectorizer | 5 | 0.0003 |
| --load-store-vectorizer | 5 | 0.0003 |
| --ipsccp | 4 | 0.0002 |
| --dse | 3 | 0.0002 |
| --lower-constant-intrinsics | 3 | 0.0002 |
| -loop-reduce | 2 | 0.0001 |
| --correlated-propagation | 2 | 0.0001 |
| --instsimplify | 2 | 0.0001 |
| --loop-reroll | 1 | 0.0001 |
| --loop-fusion | 1 | 0.0001 |
| --lower-expect | 1 | 0.0001 |
| --loop-instsimplify | 1 | 0.0001 |
| --inline | 1 | 0.0001 |

---

### --newgvn

**Synergistic relationships for --newgvn:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 7056 | 0.3599 |
| --simplifycfg | 7031 | 0.3587 |
| --early-cse | 7000 | 0.3571 |
| --sroa | 6975 | 0.3558 |
| --mem2reg | 6968 | 0.3555 |
| --jump-threading | 6725 | 0.3431 |
| --loop-simplifycfg | 6264 | 0.3195 |
| --gvn-hoist | 5673 | 0.2894 |
| --inline | 4233 | 0.2159 |
| --gvn | 3107 | 0.1585 |
| --elim-avail-extern | 2286 | 0.1166 |
| --early-cse-memssa | 2106 | 0.1074 |
| --newgvn | 2097 | 0.1070 |
| --licm | 1702 | 0.0868 |
| --dse | 907 | 0.0463 |
| --instsimplify | 743 | 0.0379 |
| --lower-constant-intrinsics | 318 | 0.0162 |
| --lower-expect | 309 | 0.0158 |
| --aggressive-instcombine | 288 | 0.0147 |
| --reassociate | 246 | 0.0125 |
| --loop-instsimplify | 213 | 0.0109 |
| --load-store-vectorizer | 163 | 0.0083 |
| --adce | 82 | 0.0042 |
| --bdce | 67 | 0.0034 |
| --dce | 66 | 0.0034 |
| --die | 66 | 0.0034 |
| --mergefunc | 63 | 0.0032 |
| --globalopt | 57 | 0.0029 |
| --slp-vectorizer | 50 | 0.0026 |
| --ipsccp | 49 | 0.0025 |
| --sccp | 40 | 0.0020 |
| --nary-reassociate | 27 | 0.0014 |
| --correlated-propagation | 23 | 0.0012 |
| --slsr | 14 | 0.0007 |
| --loop-reroll | 12 | 0.0006 |
| --mldst-motion | 9 | 0.0005 |
| --prune-eh | 6 | 0.0003 |
| --flattencfg | 6 | 0.0003 |
| --loop-rotate | 6 | 0.0003 |
| --memcpyopt | 4 | 0.0002 |
| --indvars | 2 | 0.0001 |
| -loop-reduce | 2 | 0.0001 |
| --loop-fusion | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --partially-inline-libcalls

**Synergistic relationships for --partially-inline-libcalls:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn | 3 | 0.0002 |

---

### --prune-eh

**Synergistic relationships for --prune-eh:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 8 | 0.0004 |
| --newgvn | 8 | 0.0004 |
| --simplifycfg | 7 | 0.0004 |
| --early-cse-memssa | 4 | 0.0002 |
| --early-cse | 4 | 0.0002 |
| --gvn | 4 | 0.0002 |
| --mem2reg | 4 | 0.0002 |
| --sroa | 4 | 0.0002 |
| --inline | 2 | 0.0001 |
| --licm | 2 | 0.0001 |
| --instsimplify | 2 | 0.0001 |
| --jump-threading | 2 | 0.0001 |
| --loop-simplifycfg | 2 | 0.0001 |
| --aggressive-instcombine | 1 | 0.0001 |
| --reassociate | 1 | 0.0001 |
| --elim-avail-extern | 1 | 0.0001 |
| --gvn-hoist | 1 | 0.0001 |
| --lower-constant-intrinsics | 1 | 0.0001 |
| --lower-expect | 1 | 0.0001 |

---

### --reassociate

**Synergistic relationships for --reassociate:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 249 | 0.0127 |
| --sroa | 241 | 0.0123 |
| --mem2reg | 237 | 0.0121 |
| --jump-threading | 230 | 0.0117 |
| --gvn | 213 | 0.0109 |
| --gvn-hoist | 205 | 0.0105 |
| --loop-simplifycfg | 205 | 0.0105 |
| --early-cse-memssa | 160 | 0.0082 |
| --newgvn | 157 | 0.0080 |
| --inline | 156 | 0.0080 |
| --early-cse | 152 | 0.0078 |
| --instcombine | 91 | 0.0046 |
| --licm | 78 | 0.0040 |
| --elim-avail-extern | 69 | 0.0035 |
| --aggressive-instcombine | 50 | 0.0026 |
| --dse | 37 | 0.0019 |
| --lower-expect | 34 | 0.0017 |
| --instsimplify | 32 | 0.0016 |
| --lower-constant-intrinsics | 31 | 0.0016 |
| --die | 26 | 0.0013 |
| --ipsccp | 22 | 0.0011 |
| --reassociate | 16 | 0.0008 |
| --sccp | 16 | 0.0008 |
| --loop-instsimplify | 7 | 0.0004 |
| --slp-vectorizer | 4 | 0.0002 |
| --load-store-vectorizer | 3 | 0.0002 |
| --adce | 2 | 0.0001 |
| --bdce | 2 | 0.0001 |
| --dce | 2 | 0.0001 |
| --prune-eh | 1 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --globalopt | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |
| --slsr | 1 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |

---

### --reg2mem

**Synergistic relationships for --reg2mem:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 8 | 0.0004 |
| --simplifycfg | 2 | 0.0001 |
| --sroa | 1 | 0.0001 |
| --gvn | 1 | 0.0001 |

---

### --scalarizer

**Synergistic relationships for --scalarizer:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 4 | 0.0002 |
| --early-cse-memssa | 1 | 0.0001 |
| --early-cse | 1 | 0.0001 |

---

### --sccp

**Synergistic relationships for --sccp:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --sroa | 38 | 0.0019 |
| --mem2reg | 37 | 0.0019 |
| --gvn-hoist | 36 | 0.0018 |
| --loop-simplifycfg | 36 | 0.0018 |
| --jump-threading | 34 | 0.0017 |
| --simplifycfg | 28 | 0.0014 |
| --inline | 26 | 0.0013 |
| --early-cse-memssa | 23 | 0.0012 |
| --early-cse | 23 | 0.0012 |
| --gvn | 12 | 0.0006 |
| --elim-avail-extern | 11 | 0.0006 |
| --dse | 7 | 0.0004 |
| --newgvn | 7 | 0.0004 |
| --licm | 6 | 0.0003 |
| --instsimplify | 2 | 0.0001 |
| --lower-constant-intrinsics | 2 | 0.0001 |
| --adce | 2 | 0.0001 |
| --bdce | 2 | 0.0001 |
| --dce | 2 | 0.0001 |
| --die | 2 | 0.0001 |
| --lower-expect | 1 | 0.0001 |
| --globalopt | 1 | 0.0001 |
| --instcombine | 1 | 0.0001 |
| --loop-instsimplify | 1 | 0.0001 |
| --reassociate | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --separate-const-offset-from-gep

**Synergistic relationships for --separate-const-offset-from-gep:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --newgvn | 1400 | 0.0714 |
| --early-cse-memssa | 1399 | 0.0714 |
| --gvn | 1321 | 0.0674 |
| --early-cse | 1294 | 0.0660 |
| --gvn-hoist | 208 | 0.0106 |
| --simplifycfg | 50 | 0.0026 |
| --instcombine | 24 | 0.0012 |
| --reassociate | 5 | 0.0003 |

---

### --simple-loop-unswitch

**Synergistic relationships for --simple-loop-unswitch:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 35 | 0.0018 |
| --gvn | 18 | 0.0009 |
| --jump-threading | 7 | 0.0004 |
| --instcombine | 6 | 0.0003 |
| --early-cse | 4 | 0.0002 |
| --early-cse-memssa | 2 | 0.0001 |
| --newgvn | 2 | 0.0001 |

---

### --simplifycfg

**Synergistic relationships for --simplifycfg:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse | 7005 | 0.3573 |
| --newgvn | 6987 | 0.3564 |
| --early-cse-memssa | 6980 | 0.3561 |
| --instcombine | 6925 | 0.3533 |
| --sroa | 6801 | 0.3469 |
| --mem2reg | 6793 | 0.3465 |
| --gvn-hoist | 5569 | 0.2841 |
| --gvn | 4433 | 0.2261 |
| --loop-simplifycfg | 4269 | 0.2178 |
| --inline | 4164 | 0.2124 |
| --jump-threading | 3876 | 0.1977 |
| --elim-avail-extern | 2240 | 0.1143 |
| --licm | 1636 | 0.0835 |
| --dse | 866 | 0.0442 |
| --instsimplify | 725 | 0.0370 |
| --lower-constant-intrinsics | 347 | 0.0177 |
| --lower-expect | 309 | 0.0158 |
| --aggressive-instcombine | 286 | 0.0146 |
| --reassociate | 239 | 0.0122 |
| --loop-instsimplify | 208 | 0.0106 |
| --load-store-vectorizer | 184 | 0.0094 |
| --mergefunc | 94 | 0.0048 |
| --adce | 81 | 0.0041 |
| --bdce | 65 | 0.0033 |
| --dce | 64 | 0.0033 |
| --die | 64 | 0.0033 |
| --nary-reassociate | 59 | 0.0030 |
| --globalopt | 58 | 0.0030 |
| --slp-vectorizer | 55 | 0.0028 |
| --ipsccp | 50 | 0.0026 |
| --sccp | 41 | 0.0021 |
| --correlated-propagation | 36 | 0.0018 |
| --slsr | 22 | 0.0011 |
| --loop-reroll | 14 | 0.0007 |
| --mldst-motion | 10 | 0.0005 |
| --memcpyopt | 8 | 0.0004 |
| --prune-eh | 5 | 0.0003 |
| --flattencfg | 5 | 0.0003 |
| --loop-rotate | 5 | 0.0003 |
| -loop-reduce | 2 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |

---

### --sink

**Synergistic relationships for --sink:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 9 | 0.0005 |
| --gvn | 7 | 0.0004 |
| --newgvn | 5 | 0.0003 |
| --gvn-hoist | 4 | 0.0002 |
| --early-cse-memssa | 4 | 0.0002 |
| --early-cse | 4 | 0.0002 |
| --jump-threading | 3 | 0.0002 |
| --ipsccp | 2 | 0.0001 |
| --correlated-propagation | 2 | 0.0001 |
| --load-store-vectorizer | 1 | 0.0001 |

---

### --slp-vectorizer

**Synergistic relationships for --slp-vectorizer:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --instcombine | 67 | 0.0034 |
| --early-cse | 66 | 0.0034 |
| --early-cse-memssa | 62 | 0.0032 |
| --newgvn | 62 | 0.0032 |
| --gvn | 59 | 0.0030 |
| --simplifycfg | 55 | 0.0028 |
| --jump-threading | 52 | 0.0027 |
| --mem2reg | 44 | 0.0022 |
| --loop-simplifycfg | 43 | 0.0022 |
| --gvn-hoist | 41 | 0.0021 |
| --sroa | 41 | 0.0021 |
| --elim-avail-extern | 22 | 0.0011 |
| --inline | 21 | 0.0011 |
| --licm | 9 | 0.0005 |
| --dse | 9 | 0.0005 |
| --instsimplify | 6 | 0.0003 |
| --nary-reassociate | 5 | 0.0003 |
| --slsr | 4 | 0.0002 |
| --adce | 3 | 0.0002 |
| --bdce | 3 | 0.0002 |
| --dce | 3 | 0.0002 |
| --die | 3 | 0.0002 |
| --load-store-vectorizer | 3 | 0.0002 |
| --reassociate | 3 | 0.0002 |
| --mldst-motion | 2 | 0.0001 |
| --correlated-propagation | 2 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --indvars | 1 | 0.0001 |
| --loop-reroll | 1 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --lower-expect | 1 | 0.0001 |
| --lower-constant-intrinsics | 1 | 0.0001 |

---

### --slsr

**Synergistic relationships for --slsr:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --simplifycfg | 22 | 0.0011 |
| --nary-reassociate | 12 | 0.0006 |
| --early-cse-memssa | 11 | 0.0006 |
| --early-cse | 11 | 0.0006 |
| --gvn | 11 | 0.0006 |
| --newgvn | 11 | 0.0006 |
| --gvn-hoist | 8 | 0.0004 |
| --instcombine | 7 | 0.0004 |
| --slp-vectorizer | 4 | 0.0002 |
| --jump-threading | 3 | 0.0002 |
| --indvars | 2 | 0.0001 |
| --loop-reroll | 2 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --loop-simplifycfg | 1 | 0.0001 |
| --load-store-vectorizer | 1 | 0.0001 |

---

### --speculative-execution

**Synergistic relationships for --speculative-execution:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 28 | 0.0014 |
| --early-cse | 28 | 0.0014 |
| --gvn | 28 | 0.0014 |
| --newgvn | 28 | 0.0014 |
| --simplifycfg | 12 | 0.0006 |
| --gvn-hoist | 2 | 0.0001 |

---

### --sroa

**Synergistic relationships for --sroa:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 7019 | 0.3581 |
| --early-cse | 7019 | 0.3581 |
| --newgvn | 7012 | 0.3577 |
| --gvn | 6925 | 0.3533 |
| --instcombine | 6880 | 0.3510 |
| --simplifycfg | 6843 | 0.3491 |
| --jump-threading | 6640 | 0.3387 |
| --loop-simplifycfg | 6261 | 0.3194 |
| --gvn-hoist | 5601 | 0.2857 |
| --inline | 4252 | 0.2169 |
| --elim-avail-extern | 2286 | 0.1166 |
| --licm | 1703 | 0.0869 |
| --dse | 901 | 0.0460 |
| --instsimplify | 738 | 0.0376 |
| --lower-expect | 309 | 0.0158 |
| --lower-constant-intrinsics | 306 | 0.0156 |
| --aggressive-instcombine | 288 | 0.0147 |
| --reassociate | 243 | 0.0124 |
| --loop-instsimplify | 213 | 0.0109 |
| --load-store-vectorizer | 143 | 0.0073 |
| --mem2reg | 127 | 0.0065 |
| --adce | 81 | 0.0041 |
| --bdce | 64 | 0.0033 |
| --dce | 64 | 0.0033 |
| --die | 64 | 0.0033 |
| --globalopt | 55 | 0.0028 |
| --mergefunc | 47 | 0.0024 |
| --slp-vectorizer | 46 | 0.0023 |
| --ipsccp | 41 | 0.0021 |
| --sccp | 39 | 0.0020 |
| --nary-reassociate | 9 | 0.0005 |
| --mldst-motion | 9 | 0.0005 |
| --prune-eh | 6 | 0.0003 |
| --flattencfg | 6 | 0.0003 |
| --loop-rotate | 6 | 0.0003 |
| --memcpyopt | 4 | 0.0002 |
| --indvars | 2 | 0.0001 |
| --loop-reroll | 1 | 0.0001 |
| -loop-reduce | 1 | 0.0001 |
| --loop-deletion | 1 | 0.0001 |
| --correlated-propagation | 1 | 0.0001 |

---

### --strip

**Synergistic relationships for --strip:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --mergefunc | 3 | 0.0002 |

---

### --strip-nondebug

**Synergistic relationships for --strip-nondebug:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --mergefunc | 3 | 0.0002 |

---

### --tailcallelim

**Synergistic relationships for --tailcallelim:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --early-cse-memssa | 75 | 0.0038 |
| --newgvn | 75 | 0.0038 |
| --gvn | 28 | 0.0014 |
| --licm | 3 | 0.0002 |
| --instcombine | 3 | 0.0002 |
| --gvn-hoist | 2 | 0.0001 |
| --jump-threading | 1 | 0.0001 |
| --simplifycfg | 1 | 0.0001 |

---

### -loop-reduce

**Synergistic relationships for -loop-reduce:**

| Second Pass | Synergy Count | Synergy Rate |
|-------------|---------------|---------------|
| --gvn-hoist | 36 | 0.0018 |
| --simplifycfg | 26 | 0.0013 |
| --gvn | 25 | 0.0013 |
| --newgvn | 23 | 0.0012 |
| --early-cse | 22 | 0.0011 |
| --early-cse-memssa | 21 | 0.0011 |
| --jump-threading | 13 | 0.0007 |
| --instcombine | 10 | 0.0005 |
| --indvars | 7 | 0.0004 |
| --slsr | 4 | 0.0002 |
| --nary-reassociate | 3 | 0.0002 |
| --load-store-vectorizer | 2 | 0.0001 |
| --mergefunc | 1 | 0.0001 |
| --slp-vectorizer | 1 | 0.0001 |
| --sroa | 1 | 0.0001 |
| --reassociate | 1 | 0.0001 |

---

## Summary Statistics

- Total synergy pairs: 1548
- Most synergistic pair: ('--early-cse-memssa', '--instcombine') (count: 7062)
- Average synergy count: 575.93
- Total programs analyzed: 19,603
