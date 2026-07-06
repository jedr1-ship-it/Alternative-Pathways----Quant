"""
The changing profile of the teaching workforce: key characteristics of
teachers in three sub-periods (2005-2011, 2012-2018, 2019-2025), with a
test of the change between the first and the last. Writes
report/table_profile_periods.tex.
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

TEACHER_OCC = {2300, 2310, 2320, 2330}
CHLD_U6 = {1, 2, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15}

parts = []
for f in sorted(glob.glob("data/interim/cps_??????.parquet")):
    d = pd.read_parquet(f)
    e = d[d["PEMLR"].isin([1, 2]) & (d["PEEDUCA"] >= 43)
          & d["PTIO1OCD"].isin(TEACHER_OCC)].copy()
    parts.append(e)
T = pd.concat(parts, ignore_index=True)
T["period"] = pd.cut(T["HRYEAR4"], [2004, 2011, 2018, 2025],
                     labels=["2005--2011", "2012--2018", "2019--2025"])
T["female"] = (T["PESEX"] == 2).astype(int)
T["age"] = T["PRTAGE"]
T["under35"] = (T["PRTAGE"] < 35).astype(int)
T["white"] = (T["PTDTRACE"] == 1).astype(int)
T["hispanic"] = (T["PEHSPNON"] == 1).astype(int)
T["married"] = T["PEMARITL"].isin([1, 2]).astype(int)
T["child_u6"] = T["PRCHLD"].isin(CHLD_U6).astype(int)
T["ma_plus"] = (T["PEEDUCA"] >= 44).astype(int)
T["public"] = T["PEIO1COW"].isin([1, 2, 3]).astype(int)
T["union"] = (T["PEERNLAB"] == 1).astype(float).where(T["PEERNLAB"] > 0)
T["parttime"] = T["PEHRUSL1"].between(1, 34).astype(int)
T["late"] = (T["period"] == "2019--2025").astype(int)

ROWS = [("Age, years", "age", "num"),
        ("Under 35", "under35", "pct"),
        ("Female", "female", "pct"),
        ("White", "white", "pct"),
        ("Hispanic", "hispanic", "pct"),
        ("Married", "married", "pct"),
        ("Child under 6 at home", "child_u6", "pct"),
        ("Master's degree or higher", "ma_plus", "pct"),
        ("Public-sector employer", "public", "pct"),
        ("Union member", "union", "pct"),
        ("Part-time", "parttime", "pct")]


def pstars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


def wmean(g, col):
    m = g[col].notna()
    return np.average(g.loc[m, col], weights=g.loc[m, "PWSSWGT"])


P1, P2, P3 = [T[T["period"] == p] for p in
              ["2005--2011", "2012--2018", "2019--2025"]]
sub13 = T[T["period"].isin(["2005--2011", "2019--2025"])]
with open("report/table_profile_periods.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccc}\n\\toprule\n"
             " & 2005--2011 & 2012--2018 & 2019--2025 & Change \\\\\n"
             "\\midrule\n")
    for lab, v, kind in ROWS:
        cells = []
        for g in (P1, P2, P3):
            m = wmean(g, v)
            cells.append(f"{m*100:.1f}\\%" if kind == "pct" else f"{m:.1f}")
        sub = sub13[sub13[v].notna()]
        t = smf.wls(f"{v} ~ late", data=sub, weights=sub["PWSSWGT"]).fit(
            cov_type="cluster", cov_kwds={"groups": sub["HRHHID"]})
        d, p = t.params["late"], t.pvalues["late"]
        dtxt = f"{d*100:+.1f}\\,pp" if kind == "pct" else f"{d:+.2f}"
        cells.append(dtxt + pstars(p))
        fh.write(f"{lab} & " + " & ".join(cells) + " \\\\\n")
    fh.write("\\midrule\nMonthly interviews & "
             + " & ".join(f"{len(g):,}" for g in (P1, P2, P3))
             + " & \\\\\n\\bottomrule\n\\end{tabular}\n")
print("wrote report/table_profile_periods.tex")
for lab, v, kind in ROWS:
    print(f"{lab:32s}", " ".join(f"{wmean(g, v)*100:5.1f}" for g in (P1, P2, P3)))
