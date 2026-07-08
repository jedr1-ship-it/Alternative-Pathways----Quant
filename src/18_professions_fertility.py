"""
Linked 12-month pairs for four professions carrying the family covariates,
so the new-baby event can be interacted with occupation exit profession by
profession. Supersedes the exploratory 17_professions_link.py rates (nurse
codes now include advanced practice, 3255-3258, matching the single 3130
code used before 2011). Writes data/processed/professions_pairs.csv and
refreshes outputs/professions_attrition.csv.
"""
import glob
import os
import numpy as np
import pandas as pd

KEY = ["HRHHID", "HRHHID2", "PULINENO"]
C0 = KEY + ["HRMIS", "HRYEAR4", "PEMLR", "PTIO1OCD", "PEEDUCA", "PESEX",
            "PTDTRACE", "PRTAGE", "PEMARITL", "PRNMCHLD", "PRCHLD",
            "PEHRUSL1", "PEIO1COW", "PWSSWGT"]
C1 = KEY + ["PEMLR", "PTIO1OCD", "PESEX", "PTDTRACE", "PRTAGE", "PRCHLD"]
U3 = {1, 5, 6, 7, 11, 12, 13, 15}   # own child under 3 present


def codes(group, year):
    if group == "Teachers":
        return {2300, 2310, 2320, 2330}
    if group == "Registered nurses":
        return {3130} if year <= 2010 else {3255, 3256, 3257, 3258}
    if group == "Accountants and auditors":
        return {800}
    if group == "Social workers":
        return {2010} if year <= 2019 else {2011, 2012, 2013, 2014}
    raise ValueError(group)


GROUPS = ["Teachers", "Registered nurses", "Accountants and auditors",
          "Social workers"]
files = {os.path.basename(f)[4:10]: f
         for f in glob.glob("data/interim/cps_??????.parquet")}

parts = []
for ym, f in sorted(files.items()):
    y, m = int(ym[:4]), int(ym[4:])
    ym1 = f"{y+1}{m:02d}"
    if y > 2024 or ym1 not in files:
        continue
    d0 = pd.read_parquet(f, columns=C0)
    d0 = d0[d0["HRMIS"] <= 4]
    e0 = d0[d0["PEMLR"].isin([1, 2]) & (d0["PEEDUCA"] >= 43)]
    d1 = pd.read_parquet(files[ym1], columns=C1)
    for g in GROUPS:
        base = e0[e0["PTIO1OCD"].isin(codes(g, y))]
        if base.empty:
            continue
        mrg = base.merge(d1, on=KEY, suffixes=("_0", "_1"), how="inner")
        ok = ((mrg["PESEX_0"] == mrg["PESEX_1"])
              & (mrg["PTDTRACE_0"] == mrg["PTDTRACE_1"])
              & mrg["PRTAGE_1"].sub(mrg["PRTAGE_0"]).between(0, 2))
        mrg = mrg[ok].copy()
        if mrg.empty:
            continue
        mrg["group"] = g
        mrg["base_year"] = y
        mrg["stay"] = (mrg["PEMLR_1"].isin([1, 2])
                       & mrg["PTIO1OCD_1"].isin(codes(g, y + 1))).astype(int)
        parts.append(mrg)

P = pd.concat(parts, ignore_index=True)
P["leave"] = 1 - P["stay"]
P["dest_occ"] = ((P["leave"] == 1) & P["PEMLR_1"].isin([1, 2])).astype(int)
P["dest_unemp"] = ((P["leave"] == 1)
                   & P["PEMLR_1"].isin([3, 4])).astype(int)
P["dest_olf"] = ((P["leave"] == 1)
                 & ~P["PEMLR_1"].isin([1, 2, 3, 4])).astype(int)
P["female"] = (P["PESEX_0"] == 2).astype(int)
P["married"] = P["PEMARITL"].isin([1, 2]).astype(int)
P["new_baby"] = (P["PRCHLD_1"].isin(U3)
                 & ~P["PRCHLD_0"].isin(U3)).astype(int)
P["age"] = P["PRTAGE_0"]
P["ma_plus"] = (P["PEEDUCA"] >= 44).astype(int)
P["parttime"] = P["PEHRUSL1"].between(1, 34).astype(int)
P["public"] = P["PEIO1COW"].isin([1, 2, 3]).astype(int)

keep = (KEY + ["group", "base_year", "leave", "dest_occ", "dest_olf",
               "dest_unemp", "female", "married", "new_baby", "age",
               "ma_plus", "parttime", "public", "PWSSWGT"])
P[keep].to_csv("data/processed/professions_pairs.csv", index=False)
print("pairs saved:", len(P))
print(P.groupby("group").agg(n=("leave", "size"), leave=("leave", "mean"),
                             fem=("female", "mean"),
                             baby=("new_baby", "sum")).round(3))

# refreshed annual rates with the corrected nurse codes
out = []
for (y, g), gg in P.groupby(["base_year", "group"]):
    out.append({"base_year": y, "group": g, "n": len(gg),
                "rate": np.average(gg["leave"], weights=gg["PWSSWGT"]) * 100})
pd.DataFrame(out).to_csv("outputs/professions_attrition.csv", index=False)
print("rates refreshed")
