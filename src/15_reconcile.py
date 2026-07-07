"""
Reconciling this paper's attrition rates with the published benchmarks:
a ladder of definitions, from the broadest 12-month leaver to the
strictest non-returning leaver with no education destination, next to the
TFS and retrospective-CPS reference numbers. Also quantifies mobility
without attrition (sector switches among continuing teachers).
Writes report/table_reconcile.tex.
"""
import numpy as np
import pandas as pd
from covariates import load_panel

EDU_ADJ = {230, 2200, 2205, 2340, 2350, 2360, 2430, 2435, 2440,
           2540, 2545, 2550, 2555}

df = load_panel()
W = "PWSSWGT_0"


def wrate(d, col):
    return np.average(d[col], weights=d[W]) * 100


pub = df["PEIO1COW_0"].isin([1, 2, 3])
k12 = df["PTIO1OCD_0"] != 2300
B = df[df["sampleB"]]
Bpub, Bk12 = B[B["PEIO1COW_0"].isin([1, 2, 3])], B[B["PTIO1OCD_0"] != 2300]

# non-returning leaver who is in no education occupation at t+12
out_edu = ((B["leaver_p"] == 1)
           & ~B["PTIO1OCD_1"].isin(EDU_ADJ)).astype(int)

rows = [
    ("Conventional 12-month leaver, all teachers",
     wrate(df, "leaver"), f"{len(df):,}"),
    ("\\quad public-sector teachers only",
     wrate(df[pub], "leaver"), f"{int(pub.sum()):,}"),
    ("\\quad excluding preschool and kindergarten",
     wrate(df[k12], "leaver"), f"{int(k12.sum()):,}"),
    ("\\quad public sector and K--12 only",
     wrate(df[pub & k12], "leaver"), f"{int((pub & k12).sum()):,}"),
    ("Non-returning leaver (main definition)",
     wrate(B, "leaver_p"), f"{len(B):,}"),
    ("\\quad and in no education occupation at $t{+}12$",
     np.average(out_edu, weights=B[W]) * 100, f"{len(B):,}"),
]
MEMO = [
    ("Teacher Follow-up Survey, public school leavers 2021--22", "8.0"),
    ("Retrospective CPS estimates, 1992--2001 and 2015--2024",
     "7.7 and 7.6"),
]
with open("report/table_reconcile.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n"
             " & Annual rate & Persons \\\\\n\\midrule\n")
    for lab, r, n in rows:
        fh.write(f"{lab} & {r:.1f}\\% & {n} \\\\\n")
    fh.write("\\midrule\n\\multicolumn{3}{l}{\\textit{Published"
             " benchmarks}} \\\\[2pt]\n")
    for lab, r in MEMO:
        fh.write(f"{lab} & {r}\\% & \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")
print("wrote report/table_reconcile.tex")
for lab, r, n in rows:
    print(f"{lab:55s} {r:5.1f}  {n}")

# ---------- mobility without attrition ----------
S = B[B["leaver_p"] == 0]
S = S[S["teacher_1"] == 1]          # still teaching at t+12
sw_pub_priv = ((S["PEIO1COW_0"].isin([1, 2, 3]))
               & ~S["PEIO1COW_1"].isin([1, 2, 3])).astype(int)
sw_priv_pub = ((~S["PEIO1COW_0"].isin([1, 2, 3]))
               & S["PEIO1COW_1"].isin([1, 2, 3])).astype(int)
lvl_switch = (S["PTIO1OCD_0"] != S["PTIO1OCD_1"]).astype(int)
state_move = (S["GESTFIPS_0"] != S["GESTFIPS_1"]).astype(int)
print("\ncontinuing teachers, n =", len(S))
print(f"public -> private: {np.average(sw_pub_priv, weights=S[W])*100:.2f}%")
print(f"private -> public: {np.average(sw_priv_pub, weights=S[W])*100:.2f}%")
print(f"teaching-level switch: {np.average(lvl_switch, weights=S[W])*100:.2f}%")
print(f"state change (should be ~0): "
      f"{np.average(state_move, weights=S[W])*100:.3f}%")
pd.DataFrame({"metric": ["pub_to_priv", "priv_to_pub", "level_switch",
                         "state_move"],
              "pct": [np.average(x, weights=S[W]) * 100 for x in
                      (sw_pub_priv, sw_priv_pub, lvl_switch, state_move)]}
             ).round(3).to_csv("outputs/mobility_without_attrition.csv",
                               index=False)
