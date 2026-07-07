"""
PROTOTYPE, not yet in the paper. Links four professions with the same
12-month design used for teachers and computes conventional annual
occupation-leaving rates: teachers, registered nurses, accountants and
auditors, and social workers. College-educated, employed at baseline.
Writes outputs/professions_attrition.csv.
"""
import glob
import os
import numpy as np
import pandas as pd

KEY = ["HRHHID", "HRHHID2", "PULINENO"]
COLS = KEY + ["HRMIS", "PEMLR", "PTIO1OCD", "PEEDUCA", "PESEX",
              "PTDTRACE", "PRTAGE", "PWSSWGT"]


def codes(group, year):
    if group == "Teachers":
        return {2300, 2310, 2320, 2330}
    if group == "Registered nurses":
        return {3130} if year <= 2010 else {3255}
    if group == "Accountants and auditors":
        return {800}
    if group == "Social workers":
        if year <= 2019:
            return {2010}
        return {2011, 2012, 2013, 2014}
    raise ValueError(group)


GROUPS = ["Teachers", "Registered nurses", "Accountants and auditors",
          "Social workers"]
files = {os.path.basename(f)[4:10]: f
         for f in glob.glob("data/interim/cps_??????.parquet")}

rows = []
for ym, f in sorted(files.items()):
    y, m = int(ym[:4]), int(ym[4:])
    ym1 = f"{y+1}{m:02d}"
    if y > 2024 or ym1 not in files:
        continue
    d0 = pd.read_parquet(f, columns=COLS)
    d0 = d0[d0["HRMIS"] <= 4]
    e0 = d0[d0["PEMLR"].isin([1, 2]) & (d0["PEEDUCA"] >= 43)]
    d1 = pd.read_parquet(files[ym1],
                         columns=KEY + ["PEMLR", "PTIO1OCD", "PESEX",
                                        "PTDTRACE", "PRTAGE"])
    for g in GROUPS:
        base = e0[e0["PTIO1OCD"].isin(codes(g, y))]
        if base.empty:
            continue
        mrg = base.merge(d1, on=KEY, suffixes=("_0", "_1"), how="inner")
        ok = ((mrg["PESEX_0"] == mrg["PESEX_1"])
              & (mrg["PTDTRACE_0"] == mrg["PTDTRACE_1"])
              & mrg["PRTAGE_1"].sub(mrg["PRTAGE_0"]).between(0, 2))
        mrg = mrg[ok]
        if mrg.empty:
            continue
        stay = (mrg["PEMLR_1"].isin([1, 2])
                & mrg["PTIO1OCD_1"].isin(codes(g, y + 1)))
        rows.append({"base_year": y, "month": m, "group": g,
                     "n": len(mrg),
                     "wleave": np.average(~stay, weights=mrg["PWSSWGT"]),
                     "w": mrg["PWSSWGT"].sum()})

r = pd.DataFrame(rows)
out = []
for (y, g), gg in r.groupby(["base_year", "group"]):
    out.append({"base_year": y, "group": g, "n": int(gg["n"].sum()),
                "rate": np.average(gg["wleave"], weights=gg["w"]) * 100})
res = pd.DataFrame(out)
res.to_csv("outputs/professions_attrition.csv", index=False)
print(res.pivot(index="base_year", columns="group", values="rate").round(1))
print(res.groupby("group")["n"].sum())
