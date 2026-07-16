"""
Data for the re-founded narrative: (1) an unemployment-rate series computed
from our own CPS monthly files (internally consistent with the leaving
series) plus a college-graduate rate from the ASEC, for the cyclicality
block; (2) relative teacher pay: median weekly earnings of full-time
full-year teachers against all college graduates and each comparison
profession, by year; (3) the five-year balance blocks, teachers versus
other college graduates, for the appendix table and bar chart; (4) the
N-per-source comparison table.  Writes outputs/n_*.csv.
"""
import glob
import numpy as np
import pandas as pd

RAW = "data/raw/asec"
MON = "data/raw/cps"
W = "MARSUPWT"
CORE = {2300, 2310, 2320, 2330}


def tset(ay):
    return CORE | ({2340} if ay <= 2019 else {2360})


def profs(ay):
    old = ay <= 2019
    return {"Nurses": {3255, 3256, 3257, 3258, 3500},
            "Social workers": {2010} if old else {2011, 2012, 2013, 2014},
            "Accountants": {800}}


# ---------- (1) unemployment series from the monthly files ----------
rows = []
for y in range(2005, 2026):
    fs = sorted(glob.glob(f"{MON}/slim_{y}_??.parquet"))
    if not fs:
        continue
    urates = []
    for f in fs:
        d = pd.read_parquet(f, columns=["PEMLR"])
        lf = d["PEMLR"].isin([1, 2, 3, 4]).sum()
        un = d["PEMLR"].isin([3, 4]).sum()
        if lf:
            urates.append(un / lf * 100)
    rows.append({"cal_year": y, "urate": round(np.mean(urates), 2),
                 "months": len(urates)})
U = pd.DataFrame(rows)
U.to_csv("outputs/n_urate.csv", index=False)
print("unemployment (own monthly files):")
print(U.head(3).to_string(index=False), "...")
print(U.tail(3).to_string(index=False))

# college-graduate unemployment from the ASEC survey week
R = pd.concat([pd.read_parquet(f) for f in
               sorted(glob.glob(f"{RAW}/asec_rich_*.parquet"))],
              ignore_index=True)
for c in R.columns:
    if c != "PERIDNUM":
        R[c] = pd.to_numeric(R[c], errors="coerce")
cg = []
for ay, g in R.groupby("asec_year"):
    d = g[(g["A_HGA"] >= 43) & (g["A_AGE"].between(25, 64))]
    lf = d[d["A_LFSR"].isin([1, 2, 3, 4])]
    u = np.average(lf["A_LFSR"].isin([3, 4]), weights=lf[W]) * 100
    cg.append({"cal_year": int(ay), "urate_cg": round(u, 2)})
pd.DataFrame(cg).to_csv("outputs/n_urate_cg.csv", index=False)

# ---------- (2) relative pay: FTFY median weekly earnings ----------
R["cal_year"] = R["asec_year"] - 1
R["ba_plus"] = (R["A_HGA"] >= 43).astype(int)
R["earn_wk"] = np.where((R["WSAL_VAL"] > 0) & (R["WKSWORK"] >= 50)
                        & (R["HRSWK"] >= 35),
                        R["WSAL_VAL"] / R["WKSWORK"], np.nan)


def wmedian(d, col):
    d = d.dropna(subset=[col, W]).sort_values(col)
    if d.empty:
        return np.nan
    cw = d[W].cumsum() / d[W].sum()
    return d.loc[cw >= 0.5, col].iloc[0]


pay = []
for ay, g in R[(R["ba_plus"] == 1) & R["A_AGE"].between(25, 64)].groupby(
        "asec_year"):
    cs = tset(int(ay))
    row = {"cal_year": int(ay) - 1,
           "teachers": wmedian(g[g["OCCUP"].isin(cs)], "earn_wk"),
           "all_college": wmedian(g, "earn_wk")}
    for p, cc in profs(int(ay)).items():
        row[p] = wmedian(g[g["OCCUP"].isin(cc)], "earn_wk")
    pay.append(row)
PAY = pd.DataFrame(pay).sort_values("cal_year")
PAY["rel_college"] = (PAY["teachers"] / PAY["all_college"] * 100).round(1)
PAY["rel_nurses"] = (PAY["teachers"] / PAY["Nurses"] * 100).round(1)
PAY.round(0).to_csv("outputs/n_relative_pay.csv", index=False)
print("\nrelative pay (teacher median FTFY weekly / all college grads, %):")
print(PAY[["cal_year", "rel_college", "rel_nurses"]].to_string(index=False))

# ---------- (3) five-year balance blocks ----------
R["female"] = (R["A_SEX"] == 2).astype(int)
R["married"] = R["A_MARITL"].isin([1, 2, 3]).astype(int)
R["ma_plus"] = (R["A_HGA"] >= 44).astype(int)
R["black"] = (R["PRDTRACE"] == 2).astype(int)
R["parttime"] = R["HRSWK"].between(1, 34).astype(int)
ptr = []
for c in ["A_PARENT", "PEPAR1", "PEPAR2"]:
    k = R[(pd.to_numeric(R[c], errors="coerce") > 0) & (R["A_AGE"] < 18)][
        ["asec_year", "PH_SEQ", c, "A_LINENO"]].rename(
        columns={c: "pl", "A_LINENO": "kl"})
    ptr.append(k)
kk = pd.concat(ptr).drop_duplicates(["asec_year", "PH_SEQ", "pl", "kl"])
kk = kk.groupby(["asec_year", "PH_SEQ", "pl"]).size().rename("nk") \
    .reset_index().rename(columns={"pl": "A_LINENO"})
R = R.merge(kk, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
R["haskids"] = (R["nk"].fillna(0) > 0).astype(int)


def wavg(d, col):
    v = d[col].astype(float)
    ok = v.notna() & d[W].notna()
    return np.average(v[ok], weights=d.loc[ok, W]) if ok.any() else np.nan


BLOCKS = [("2010-2014", 2010, 2014), ("2015-2019", 2015, 2019),
          ("2020-2024", 2020, 2024)]
VARS = [("Age", "A_AGE", 1), ("Female %", "female", 100),
        ("Black %", "black", 100), ("Married %", "married", 100),
        ("Has own children %", "haskids", 100),
        ("Master's+ %", "ma_plus", 100), ("Part-time %", "parttime", 100),
        ("Median FTFY weekly earnings $", "earn_wk", None)]
bal = []
for bl, lo, hi in BLOCKS:
    g = R[(R["ba_plus"] == 1) & R["A_AGE"].between(25, 64)
          & R["cal_year"].between(lo, hi)]
    ist = pd.Series(False, index=g.index)
    for ay, gg in g.groupby("asec_year"):
        ist.loc[gg.index] = gg["OCCUP"].isin(tset(int(ay)))
    tch, oth = g[ist], g[~ist]
    for lab, v, sc in VARS:
        if sc is None:
            a, b = wmedian(tch, v), wmedian(oth, v)
        else:
            a, b = wavg(tch, v) * sc, wavg(oth, v) * sc
        bal.append({"block": bl, "variable": lab,
                    "teachers": round(a, 1), "other_college": round(b, 1)})
    bal.append({"block": bl, "variable": "N (unweighted)",
                "teachers": len(tch), "other_college": len(oth)})
BAL = pd.DataFrame(bal)
BAL.to_csv("outputs/n_balance_blocks.csv", index=False)
print("\nbalance blocks written")

# ---------- (4) N per source ----------
NS = pd.DataFrame([
    {"source": "This paper, characterized sample",
     "survey": "CPS ASEC 2011-2025", "window": "2010-2024",
     "teacher_obs": 45296, "notes": "college-graduate teacher-years"},
    {"source": "This paper, main window",
     "survey": "CPS ASEC 2016-2025", "window": "2015-2024",
     "teacher_obs": 28932, "notes": "college-graduate teacher-years"},
    {"source": "This paper, rate series",
     "survey": "CPS ASEC 1998-2025", "window": "1997-2024 (4 gaps)",
     "teacher_obs": 76000, "notes": "approx.; all-education for the "
     "harmonized series"},
    {"source": "Harris & Adams (2007)", "survey": "March CPS 1992-2001",
     "window": "1992-2001", "teacher_obs": 18786,
     "notes": "their Table 1"},
    {"source": "Aldeman & Yi (2025)", "survey": "CPS (pooled decades)",
     "window": "~1984-2024", "teacher_obs": np.nan,
     "notes": "N not reported"},
    {"source": "Tan et al. (2026), LPI", "survey": "NTPS 2020-21 + TFS "
     "2021-22", "window": "2020-22", "teacher_obs": np.nan,
     "notes": "NTPS samples ~40-50k public school teachers per wave; "
     "follow-up subsample smaller (verify against report)"},
])
NS.to_csv("outputs/n_sources.csv", index=False)
print("\nN-per-source table written (two cells flagged for verification)")
