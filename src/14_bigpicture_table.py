"""
The flagship descriptive table of the paper: a portrait of the American
teaching workforce over 2005-2025 built on EVERY employed person observed
in a school-teaching occupation (no degree restriction), split by sex and
compared with other college-educated workers. Sample sizes are unique
persons, never person-months. Writes report/table_bigpicture.tex.
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

TEACHER_OCC = {2300, 2310, 2320, 2330}
CHLD_U6 = {1, 2, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15}

COLS = ["HRHHID", "HRHHID2", "PULINENO", "HRYEAR4", "PRTAGE", "PESEX",
        "PEEDUCA", "PTDTRACE", "PEHSPNON", "PRCITSHP", "PEMARITL",
        "PRNMCHLD", "PRCHLD", "PEIO1COW", "PEERNLAB", "PEHRUSL1", "PEMJOT",
        "PTERNWA", "HEFAMINC", "PWSSWGT", "PTIO1OCD", "PEMLR"]

parts, n_months = [], 0
for f in sorted(glob.glob("data/interim/cps_??????.parquet")):
    d = pd.read_parquet(f, columns=COLS)
    n_months += 1
    e = d[d["PEMLR"].isin([1, 2])]
    keep = e[e["PTIO1OCD"].isin(TEACHER_OCC) | (e["PEEDUCA"] >= 43)].copy()
    parts.append(keep)
P = pd.concat(parts, ignore_index=True)
del parts
P["tch"] = P["PTIO1OCD"].isin(TEACHER_OCC)
P["tch_i"] = P["tch"].astype(np.int8)
# non-teachers enter the comparison group only with a bachelor's degree
P = P[P["tch"] | (P["PEEDUCA"] >= 43)]

P["age"] = P["PRTAGE"].astype(np.float32)
P["female"] = (P["PESEX"] == 2).astype(np.int8)
P["white"] = (P["PTDTRACE"] == 1).astype(np.int8)
P["black"] = (P["PTDTRACE"] == 2).astype(np.int8)
P["asian"] = (P["PTDTRACE"] == 4).astype(np.int8)
P["hispanic"] = (P["PEHSPNON"] == 1).astype(np.int8)
P["noncitizen"] = (P["PRCITSHP"] == 5).astype(np.int8)
P["married"] = P["PEMARITL"].isin([1, 2]).astype(np.int8)
P["n_children"] = P["PRNMCHLD"].clip(lower=0).astype(np.float32)
P["child_u6"] = P["PRCHLD"].isin(CHLD_U6).astype(np.int8)
P["ba_plus"] = (P["PEEDUCA"] >= 43).astype(np.int8)
P["ma_plus"] = (P["PEEDUCA"] >= 44).astype(np.int8)
P["prof_phd"] = (P["PEEDUCA"] >= 45).astype(np.int8)
P["public"] = P["PEIO1COW"].isin([1, 2, 3]).astype(np.int8)
P["parttime"] = P["PEHRUSL1"].between(1, 34).astype(np.int8)
P["hours"] = P["PEHRUSL1"].where(P["PEHRUSL1"] > 0).astype(np.float32)
P["multjob"] = (P["PEMJOT"] == 1).astype(np.int8)
# outgoing rotations only
P["union"] = (P["PEERNLAB"] == 1).astype(np.float32).where(P["PEERNLAB"] > 0)
# nominal-dollar variables: measured over 2021-2025 only, to avoid mixing
# twenty years of price levels
recent = P["HRYEAR4"] >= 2021
P["wkearn"] = (P["PTERNWA"] / 100.0).where((P["PTERNWA"] > 0) & recent)
P["faminc75k"] = (P["HEFAMINC"] >= 13).astype(np.float32).where(recent)

T = P[P["tch"]]
O = P[~P["tch"]]
GROUPS = [T[T["female"] == 1], T[T["female"] == 0], T, O]


def wmean(g, col):
    m = g[col].notna()
    return np.average(g.loc[m, col], weights=g.loc[m, "PWSSWGT"])


def wmedian(g, col):
    m = g[col].notna()
    s = g.loc[m].sort_values(col)
    cw = s["PWSSWGT"].cumsum() / s["PWSSWGT"].sum()
    return s.loc[cw >= 0.5, col].iloc[0]


def pstars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


def n_persons(g):
    return len(g.drop_duplicates(["HRHHID", "HRHHID2", "PULINENO"]))


PANELS = [
    ("Panel A. Demographics", [
        ("Age, years", "age", "num"),
        ("Female", "female", "pct"),
        ("White", "white", "pct"),
        ("Black", "black", "pct"),
        ("Asian", "asian", "pct"),
        ("Hispanic", "hispanic", "pct"),
        ("Non-citizen", "noncitizen", "pct"),
    ]),
    ("Panel B. Family", [
        ("Married", "married", "pct"),
        ("Number of own children ($<$18) at home", "n_children", "num"),
        ("Child under 6 at home", "child_u6", "pct"),
    ]),
    ("Panel C. Education", [
        ("Bachelor's degree or higher", "ba_plus", "pct"),
        ("Master's degree or higher", "ma_plus", "pct"),
        ("Professional degree or doctorate", "prof_phd", "pct"),
    ]),
    ("Panel D. The job", [
        ("Public-sector employer", "public", "pct"),
        ("Union member$^{a}$", "union", "pct"),
        ("Usual weekly hours", "hours", "num"),
        ("Part-time ($<$35 h/week)", "parttime", "pct"),
        ("Holds more than one job", "multjob", "pct"),
    ]),
    ("Panel E. Pay and income", [
        ("Weekly earnings, median$^{b}$", "wkearn", "usd"),
        ("Family income \\$75k+$^{b}$", "faminc75k", "pct"),
    ]),
]

with open("report/table_bigpicture.tex", "w") as fh:
    fh.write("\\begin{tabular}{lccccc}\n\\toprule\n"
             " & \\multicolumn{3}{c}{School teachers} & Other college- &"
             " Difference \\\\\n\\cmidrule(lr){2-4}\n"
             " & Women & Men & All & educated workers & \\\\\n\\midrule\n")
    for panel, items in PANELS:
        fh.write(f"\\multicolumn{{6}}{{l}}{{\\textbf{{{panel}}}}} \\\\[2pt]\n")
        for lab, v, kind in items:
            sub = P[P[v].notna()]
            t = smf.wls(f"{v} ~ tch_i", data=sub,
                        weights=sub["PWSSWGT"]).fit(
                cov_type="cluster", cov_kwds={"groups": sub["HRHHID"]})
            p = t.pvalues["tch_i"]
            if kind == "usd":
                vals = [wmedian(g, v) for g in GROUPS]
                cells = [f"\\${x:,.0f}" for x in vals]
                dd = vals[2] - vals[3]
                cells.append(("$-$\\$" + f"{-dd:,.0f}" if dd < 0
                              else f"\\${dd:,.0f}") + pstars(p))
            else:
                vals = [wmean(g, v) for g in GROUPS]
                if kind == "pct":
                    cells = [f"{x*100:.1f}\\%" for x in vals]
                    cells.append(f"{(vals[2]-vals[3])*100:.1f}" + pstars(p))
                else:
                    cells = [f"{x:.1f}" for x in vals]
                    cells.append(f"{vals[2]-vals[3]:.2f}" + pstars(p))
            if v == "female":
                cells[0], cells[1] = "", ""
            fh.write(f"{lab} & " + " & ".join(cells) + " \\\\\n")
        fh.write("\\addlinespace[6pt]\n")
    fh.write("\\midrule\n")
    fh.write("Persons & " + " & ".join(f"{n_persons(g):,}" for g in GROUPS)
             + " & \\\\\n")
    fh.write("Population represented, millions$^{c}$ & "
             + " & ".join(f"{g['PWSSWGT'].sum()/n_months/1e6:.1f}"
                          for g in GROUPS)
             + " & \\\\\n\\bottomrule\n\\end{tabular}\n")
print("wrote report/table_bigpicture.tex")
print("persons:", [n_persons(g) for g in GROUPS], "| months:", n_months)
for lab in ["female", "ma_plus", "ba_plus", "public", "union", "parttime",
            "white", "hispanic", "married", "child_u6", "age", "hours",
            "multjob", "faminc75k"]:
    print(f"{lab:12s}", " ".join(f"{wmean(g, lab)*100:7.1f}" for g in GROUPS))
print("wkearn medians:", [round(wmedian(g, "wkearn")) for g in GROUPS])
