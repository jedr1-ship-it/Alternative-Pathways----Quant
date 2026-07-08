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
B = df[df["sampleB"]].copy()
pubB = B["PEIO1COW_0"].isin([1, 2, 3])
B["out_edu"] = ((B["leaver_p"] == 1)
                & ~B["PTIO1OCD_1"].isin(EDU_ADJ)).astype(int)

L1 = B[pubB]
rows = [
    ("Conventional 12-month leaver, analytic universe",
     wrate(df, "leaver"), f"{len(df):,}"),
    ("Non-returning leaver (main definition)",
     wrate(B, "leaver_p"), f"{len(B):,}"),
    ("\\quad public school teachers only",
     wrate(L1, "leaver_p"), f"{len(L1):,}"),
    ("\\quad and in no education occupation at $t{+}12$",
     wrate(L1, "out_edu"), f"{len(L1):,}"),
]
asec = pd.read_csv("outputs/asec_retrospective.csv")
asec_rate = np.average(asec["leaver_rate"], weights=asec["teachers_n"])
asec_n = int(asec["teachers_n"].sum())
MEMO = [
    ("Teacher Follow-up Survey, public school leavers", "8.0",
     "$\\sim$10,300$^{\\dagger}$"),
    ("Teacher Follow-up Survey, private school leavers", "12.0",
     "$\\sim$10,300$^{\\dagger}$"),
    ("My retrospective replication, 2022--2024 March CPS",
     f"{asec_rate:.1f}", f"{asec_n:,}"),
    ("\\quad without the degree restriction", "6.7", "7,909"),
    ("Harris and Adams (2007); Aldeman and Yi (2025)", "7.7; 7.6",
     "not reported"),
]
with open("report/table_reconcile.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n"
             " & Annual rate & Observations \\\\\n\\midrule\n")
    for lab, r, n in rows:
        fh.write(f"{lab} & {r:.1f}\\% & {n} \\\\\n")
    fh.write("\\midrule\n\\multicolumn{3}{l}{\\textit{Benchmarks and"
             " retrospective measures}} \\\\[2pt]\n")
    for lab, r, n in MEMO:
        fh.write(f"{lab} & {r}\\% & {n} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# ---------- linked panel vs teacher universe (representativeness) ----------
import glob
cols = ["PEMLR", "PTIO1OCD", "PEEDUCA", "PRTAGE", "PESEX", "PEIO1COW",
        "PEHRUSL1", "PTDTRACE", "PWSSWGT", "HRHHID", "HRHHID2", "PULINENO"]
acc = []
for f in sorted(glob.glob("data/interim/cps_??????.parquet")):
    d2 = pd.read_parquet(f, columns=cols)
    t = d2[d2["PEMLR"].isin([1, 2])
           & d2["PTIO1OCD"].isin([2310, 2320, 2330])
           & (d2["PEEDUCA"] >= 43)
           & ~d2["PEHRUSL1"].between(1, 34)]
    acc.append(t)
U = pd.concat(acc)
REP = [
    ("Age, years", U["PRTAGE"], df["PRTAGE_0"], "num"),
    ("Female", U["PESEX"] == 2, df["PESEX_0"] == 2, "pct"),
    ("White", U["PTDTRACE"] == 1, df["PTDTRACE_0"] == 1, "pct"),
    ("Master's degree or higher", U["PEEDUCA"] >= 44,
     df["PEEDUCA_0"] >= 44, "pct"),
    ("Public-sector employer", U["PEIO1COW"].isin([1, 2, 3]),
     df["PEIO1COW_0"].isin([1, 2, 3]), "pct"),
]
with open("report/table_linkrep.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n"
             " & All teacher interviews & Linked panel \\\\\n\\midrule\n")
    for lab, u, l, kind in REP:
        a = np.average(u, weights=U["PWSSWGT"])
        b = np.average(l, weights=df[W])
        if kind == "pct":
            fh.write(f"{lab} & {a*100:.1f}\\% & {b*100:.1f}\\% \\\\\n")
        else:
            fh.write(f"{lab} & {a:.1f} & {b:.1f} \\\\\n")
    nU = len(U.drop_duplicates(["HRHHID", "HRHHID2", "PULINENO"]))
    nL = df.drop_duplicates(["HRHHID", "HRHHID2", "PULINENO"]).shape[0]
    fh.write("\\midrule\nUnique persons & "
             f"{nU:,} & {nL:,} \\\\\n"
             "\\bottomrule\n\\end{tabular}\n")
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
