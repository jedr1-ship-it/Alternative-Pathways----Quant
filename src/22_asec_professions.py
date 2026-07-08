"""
The Aldeman and Yi (2025) retrospective measure computed for the same four
professions as the linked benchmark, on the ASEC 2022-2024 supplements. A
person belongs to a profession if the occupation of the longest job held
LAST year (OCCUP) matches the profession's codes; she left it if the
current-week occupation (PEIOOCC) no longer matches, including not being
employed. No degree restriction, matching their sample. Also the exit from
the whole occupational field, for comparison with the linked field-exit
series. Writes outputs/asec_professions.csv.
"""
import numpy as np
import pandas as pd

CODES = {"Teachers": [2300, 2310, 2320, 2330],
         "Registered nurses": [3255, 3256, 3257, 3258],
         "Pharmacists": [3050],
         "Physical therapists": [3160],
         "Physicians": [3065, 3070, 3090, 3100],
         "Lawyers": [2100],
         "Accountants and auditors": [800],
         "Social workers": [2011, 2012, 2013, 2014]}
FIELD = {"Teachers": (2200, 2555),
         "Registered nurses": (3000, 3550),
         "Pharmacists": (3000, 3550),
         "Physical therapists": (3000, 3550),
         "Physicians": (3000, 3550),
         "Lawyers": (2100, 2180),
         "Accountants and auditors": (500, 960),
         "Social workers": (2000, 2060)}
COLS = ["PEIOOCC", "OCCUP", "MARSUPWT", "A_AGE"]

rows = []
for y in (22, 23, 24):
    d = pd.read_csv(f"data/raw/asec/pppub{y}.csv", usecols=COLS)
    d = d[d["A_AGE"] >= 18]
    for g, cc in CODES.items():
        t = d[d["OCCUP"].isin(cc)].copy()
        left = (~t["PEIOOCC"].isin(cc)).astype(int)
        lo, hi = FIELD[g]
        left_f = (~t["PEIOOCC"].between(lo, hi)).astype(int)
        rows.append({"asec_year": 2000 + y, "group": g, "n": len(t),
                     "left_occ": np.average(left, weights=t["MARSUPWT"]) * 100,
                     "left_field": np.average(left_f,
                                              weights=t["MARSUPWT"]) * 100})

res = pd.DataFrame(rows)
res.round(2).to_csv("outputs/asec_professions.csv", index=False)
pool = (res.assign(wocc=res["left_occ"] * res["n"],
                   wfld=res["left_field"] * res["n"])
        .groupby("group").agg(n=("n", "sum"), wocc=("wocc", "sum"),
                              wfld=("wfld", "sum")))
pool["left_occ"] = pool["wocc"] / pool["n"]
pool["left_field"] = pool["wfld"] / pool["n"]
print(pool[["n", "left_occ", "left_field"]].round(1).to_string())

# appendix table: the same four professions under the linked and the
# retrospective instruments
lk = pd.read_csv("outputs/professions_attrition.csv")
ln = lk.groupby("group")["n"].sum()
locc = lk.assign(w=lk["rate"] * lk["n"]).groupby("group")["w"].sum() / ln
lfld = (lk.assign(w=lk["rate_field"] * lk["n"]).groupby("group")["w"].sum()
        / ln)
ORDER = ["Teachers", "Registered nurses", "Pharmacists",
         "Physical therapists", "Physicians", "Lawyers", "Social workers",
         "Accountants and auditors"]
with open("report/table_professions_instruments.tex", "w") as fh:
    fh.write("""\\begin{tabular}{lccccc}
\\toprule
 & \\multicolumn{3}{c}{Linked design, 2005--2024}
 & \\multicolumn{2}{c}{Retrospective, 2022--2024} \\\\
\\cmidrule(lr){2-4}\\cmidrule(lr){5-6}
 & Left detailed & Left occupational & Obser- & Left detailed & Sample \\\\
 & occupation & field & vations & occupation & \\\\
\\midrule
""")
    for g in ORDER:
        fh.write(f"{g} & {locc[g]:.1f} & {lfld[g]:.1f} & {ln[g]:,} & "
                 f"{pool.loc[g, 'left_occ']:.1f} & "
                 f"{int(pool.loc[g, 'n']):,} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")
print("wrote report/table_professions_instruments.tex")
