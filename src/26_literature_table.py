"""
Literature-comparison table: teacher attrition estimates across data
sources and measurement instruments. My own rates are computed from the
linked panel and the March-supplement replication; every other number is
quoted from its published source (no invented figures). The point of the
table is that the level tracks the instrument, not the truth: a single
recall question and a one-shot roster follow-up both read low, my linked
two-interview panel reads high, and applying the recall instrument to my
own data reproduces the recall literature.

Writes report/table_literature.tex.
"""
import numpy as np
import pandas as pd
from covariates import load_panel

df = load_panel()
B = df[df["sampleB"]].copy()
W = "PWSSWGT_0"


def wr(d, c):
    return np.average(d[c], weights=d[W]) * 100


pub = B[B["PEIO1COW_0"].isin([1, 2, 3])]
priv = B[~B["PEIO1COW_0"].isin([1, 2, 3])]
mine_all = wr(B, "leaver_p")
mine_pub = wr(pub, "leaver_p")
mine_priv = wr(priv, "leaver_p")
mine_conv = wr(df, "leaver")
asec = pd.read_csv("outputs/asec_retrospective.csv")
mine_recall = np.average(asec["leaver_rate"], weights=asec["teachers_n"])

# every literature figure below is quoted verbatim from its source
rows = [
    ("\\multicolumn{5}{l}{\\textit{A. This paper: linked CPS panel,"
     " two interviews twelve months apart}} \\\\", None),
    ("\\quad Non-returning leaver, all teachers",
     "Linked panel", "Full-time K--12, public and private",
     "2005--2025", f"{mine_all:.1f}"),
    ("\\quad\\quad public schools only",
     "Linked panel", "Full-time public K--12", "2005--2025",
     f"{mine_pub:.1f}"),
    ("\\quad\\quad private schools only",
     "Linked panel", "Full-time private K--12", "2005--2025",
     f"{mine_priv:.1f}"),
    ("\\quad Conventional 12-month leaver",
     "Linked panel", "Full-time K--12, public and private",
     "2005--2025", f"{mine_conv:.1f}"),
    ("\\multicolumn{5}{l}{\\textit{B. Retrospective March CPS: one recall"
     " question about the job held a year ago}} \\\\", None),
    ("\\quad This paper's replication",
     "March CPS", "Teachers, bachelor's or higher", "2022--2024",
     f"{mine_recall:.1f}"),
    ("\\quad Aldeman and Yi (2025)",
     "March CPS", "All teachers", "2015--2024", "7.6"),
    ("\\quad Harris and Adams (2007)",
     "March CPS", "All teachers", "1972--2004", "n.r."),
    ("\\multicolumn{5}{l}{\\textit{C. Roster follow-up survey: one"
     " re-interview of a sample drawn from school staff lists}} \\\\", None),
    ("\\quad Teacher Follow-up Survey, public",
     "NCES roster", "Public K--12", "2021--2022", "8.0"),
    ("\\quad\\quad private",
     "NCES roster", "Private K--12", "2021--2022", "12.0"),
    ("\\quad\\quad public and private",
     "NCES roster", "All K--12", "2021--2022", "8.4"),
    ("\\quad Tan et al. (2026), public",
     "NCES roster", "Public K--12", "2021--2022", "7.1"),
    ("\\multicolumn{5}{l}{\\textit{D. State administrative payroll"
     " records}} \\\\", None),
    ("\\quad Goldhaber and Theobald (2023)",
     "WA payroll", "Public, one state", "1984--2021", "6--8"),
]

with open("report/table_literature.tex", "w") as fh:
    fh.write("\\begin{tabular}{p{5.4cm}llcc}\n\\toprule\n"
             " & Instrument & Population & Years & Rate (\\%) \\\\\n"
             "\\midrule\n")
    for r in rows:
        if r[1] is None:
            fh.write("\\addlinespace[2pt]" + r[0] + "\n")
        else:
            lab, inst, pop, yr, rate = r
            fh.write(f"{lab} & {inst} & {pop} & {yr} & {rate} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

print("wrote report/table_literature.tex")
print(f"mine: all {mine_all:.1f}  public {mine_pub:.1f}  "
      f"private {mine_priv:.1f}  conv {mine_conv:.1f}  "
      f"recall {mine_recall:.1f}")
