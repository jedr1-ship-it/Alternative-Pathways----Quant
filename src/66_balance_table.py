"""
AER-style appendix balance table: teacher women, teacher men, all
teachers, and all other college-graduate workers, on every observable
the master carries, in blocks. Weighted means (SD in parentheses for
continuous variables), pooled calendar 2015-2024.

Outputs: outputs/t_balance.csv and report/tables/balance_appendix.tex.
"""
import numpy as np
import pandas as pd

M = pd.read_parquet("data/processed/asec_master.parquet")
P = M[(M["ba_plus"] == 1) & M["A_AGE"].between(21, 80) & M["WGT"].notna()
      & M["cal_year"].between(2015, 2024) & (M["OCCUP"] > 0)]
groups = {
    "Teachers, women": P[(P["teacher"] == 1) & (P["female"] == 1)],
    "Teachers, men": P[(P["teacher"] == 1) & (P["female"] == 0)],
    "All teachers": P[P["teacher"] == 1],
    "Other college workers": P[P["teacher"] == 0],
}


def wmean(d, col):
    v = d[col].astype(float)
    ok = v.notna()
    return np.average(v[ok], weights=d.loc[ok, "WGT"]) if ok.any() \
        else np.nan


def wsd(d, col):
    v = d[col].astype(float)
    ok = v.notna()
    if not ok.any():
        return np.nan
    m = np.average(v[ok], weights=d.loc[ok, "WGT"])
    return np.sqrt(np.average((v[ok] - m) ** 2, weights=d.loc[ok, "WGT"]))


def wmedian(d, col):
    v = d[col].astype(float)
    ok = v.notna() & (v > 0)
    if not ok.any():
        return np.nan
    s = d[ok].sort_values(col)
    cw = s["WGT"].cumsum() / s["WGT"].sum()
    return s.loc[cw >= 0.5, col].iloc[0]


BLOCKS = [
    ("Demographics", [
        ("Age (years)", lambda d: wmean(d, "A_AGE"), "cont", "A_AGE"),
        ("Female", lambda d: wmean(d, "female") * 100, "pct", None),
        ("Black", lambda d: wmean(d, "black") * 100, "pct", None),
        ("Married", lambda d: wmean(d, "married") * 100, "pct", None),
        ("Child under 6", lambda d: wmean(d, "child_u6") * 100, "pct",
         None),
        ("Number of children", lambda d: wmean(d, "n_children"), "cont",
         "n_children"),
    ]),
    ("Education", [
        ("Master's degree or higher", lambda d: wmean(d, "ma_plus") * 100,
         "pct", None),
    ]),
    ("Job held last year", [
        ("Government employer", lambda d: wmean(d, "public_ly") * 100,
         "pct", None),
        ("Part-time (<35 h/wk)", lambda d: wmean(d, "parttime_ly") * 100,
         "pct", None),
        ("Full year (50+ weeks)", lambda d: wmean(d, "fullyear") * 100,
         "pct", None),
        ("Pension plan at work", lambda d: wmean(d, "pension") * 100,
         "pct", None),
        ("Wage earnings, median (\\$)", lambda d: wmedian(d, "WSAL_VAL"),
         "money", None),
    ]),
    ("Transitions", [
        # leaver is defined relative to teaching; meaningless for others
        ("Leaves teaching within a year", lambda d:
         wmean(d, "leaver") * 100 if d["teacher"].all() else None,
         "pct", None),
    ]),
]

rows = []
for block, vars_ in BLOCKS:
    for lab, fn, kind, sdcol in vars_:
        r = {"block": block, "variable": lab}
        for gname, gd in groups.items():
            v = fn(gd)
            if v is None:
                r[gname] = "--"
            elif kind == "money":
                r[gname] = f"{v:,.0f}"
            elif kind == "cont":
                r[gname] = f"{v:.1f} ({wsd(gd, sdcol):.1f})"
            else:
                r[gname] = f"{v:.1f}"
        rows.append(r)
r = {"block": "", "variable": "Person-years (unweighted N)"}
for gname, gd in groups.items():
    r[gname] = f"{len(gd):,}"
rows.append(r)
TB = pd.DataFrame(rows)
TB.to_csv("outputs/t_balance.csv", index=False)
print(TB.to_string(index=False))

# LaTeX (booktabs, blocks as panel headers)
import os
os.makedirs("report/tables", exist_ok=True)
cols = list(groups.keys())
lines = [
    "\\begin{tabular}{l" + "c" * len(cols) + "}",
    "\\toprule",
    " & " + " & ".join(c.replace("&", "\\&") for c in cols) + " \\\\",
    "\\midrule",
]
cur = None
for _, row in TB.iterrows():
    if row["block"] and row["block"] != cur:
        cur = row["block"]
        lines.append(f"\\multicolumn{{{len(cols)+1}}}{{l}}"
                     f"{{\\emph{{{cur}}}}} \\\\")
    lines.append(row["variable"] + " & "
                 + " & ".join(str(row[c]) for c in cols) + " \\\\")
lines += ["\\bottomrule", "\\end{tabular}"]
with open("report/tables/balance_appendix.tex", "w") as fh:
    fh.write("\n".join(lines) + "\n")
print("\n-> outputs/t_balance.csv, report/tables/balance_appendix.tex")
