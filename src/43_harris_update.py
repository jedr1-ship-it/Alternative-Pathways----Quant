"""
THE paper pipeline: Harris & Adams (2007) applied verbatim to the modern
decade. Their design, their definitions, their tables -- on the pooled
ASEC 2016-2025 (calendar years 2015-2024).

Design (H&A Sections 3.1-3.2):
  - March CPS retrospective: profession = occupation of the longest job
    held LAST year (OCCUP); leaver = current occupation (PEIOOCC) no longer
    in the profession, split into switched / unemployed / left labor force
    (A_LFSR).
  - Teachers: preK/K, elementary, secondary, special ed, teachers n.e.c.
    (2340 old scheme / 2360 new); postsecondary and aides excluded.
  - Comparison professions: registered+licensed practical nurses, social
    workers, accountants & auditors.
  - Sample: college graduates (A_HGA >= 43), pooled 10 years, MARSUPWT.

Outputs (CSV in outputs/, printed): Table 1 characteristics+turnover,
Table 2 turnover by type and gender, Table 3 teacher-dummy LPMs with
cumulative controls, Table 4-lite determinants per profession (incl. the
pension coefficient), Table 5-lite turnover by age group, plus the annual
teacher series and the public/private split (their footnote 18).
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.api as sm

RAW = "data/raw/asec"


def prof_codes(asec_year):
    old = asec_year <= 2019
    return {
        "Teachers": {2300, 2310, 2320, 2330} | ({2340} if old else {2360}),
        "Nurses": {3255, 3256, 3257, 3258, 3500},
        "Social workers": {2010} if old else {2011, 2012, 2013, 2014},
        "Accountants": {800},
    }


df = pd.concat([pd.read_parquet(f) for f in
                sorted(glob.glob(f"{RAW}/asec_ha_*.parquet"))],
               ignore_index=True)
for c in df.columns:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df[(df["A_HGA"] >= 43) & (df["A_AGE"] >= 18)]        # college graduates
print(f"universe: {len(df):,} college-graduate person-years, "
      f"surveys {int(df['asec_year'].min())}-{int(df['asec_year'].max())}\n")

# assign profession (longest job last year) and outcomes, era-consistent
parts = []
for ay, g in df.groupby("asec_year"):
    codes = prof_codes(int(ay))
    for prof, cset in codes.items():
        b = g[g["OCCUP"].isin(cset)].copy()
        b["prof"] = prof
        # A_LFSR: 1-2 employed, 3-4 unemployed, 0/7 not in labor force.
        # The unemployed carry their LAST job's occupation in PEIOOCC, so
        # employment status must come from A_LFSR, not from PEIOOCC.
        emp_now = b["A_LFSR"].isin([1, 2])
        b["switch"] = (emp_now & ~b["PEIOOCC"].isin(cset)).astype(int)
        b["unemp"] = b["A_LFSR"].isin([3, 4]).astype(int)
        b["leftlf"] = (~b["A_LFSR"].isin([1, 2, 3, 4])).astype(int)
        b["left"] = (b["switch"] | b["unemp"] | b["leftlf"]).astype(int)
        parts.append(b)
P = pd.concat(parts, ignore_index=True)
W = "MARSUPWT"


def wm(d, col):
    v = d[col].astype(float)
    ok = v.notna() & d[W].notna()
    return np.average(v[ok], weights=d.loc[ok, W])


# ---------------- Table 1: characteristics and turnover ----------------
rows = []
for prof, d in P.groupby("prof"):
    wk = d[(d["WSAL_VAL"] > 0) & (d["WKSWORK"] > 0)]
    weekly = (wk["WSAL_VAL"] / wk["WKSWORK"])
    pen = d[d["PENPLAN"].isin([1, 2])]
    rows.append({
        "profession": prof,
        "turnover_%": round(wm(d, "left") * 100, 2),
        "age": round(wm(d, "A_AGE"), 1),
        "female_%": round(np.average((d["A_SEX"] == 2), weights=d[W]) * 100, 1),
        "black_%": round(np.average((d["PRDTRACE"] == 2), weights=d[W]) * 100, 1),
        "married_%": round(np.average(d["A_MARITL"].isin([1, 2, 3]),
                                      weights=d[W]) * 100, 1),
        "sepdiv_%": round(np.average(d["A_MARITL"].isin([5, 6]),
                                     weights=d[W]) * 100, 1),
        "advdeg_%": round(np.average((d["A_HGA"] >= 44), weights=d[W]) * 100, 1),
        "wkly_earn_$": round(np.average(weekly, weights=wk[W]), 0),
        "pension_%": round(np.average((pen["PENPLAN"] == 1),
                                      weights=pen[W]) * 100, 1),
        "n": len(d),
    })
T1 = pd.DataFrame(rows).set_index("profession").reindex(
    ["Teachers", "Nurses", "Social workers", "Accountants"])
print("=== TABLE 1 (updated): characteristics and turnover, 2015-2024 ===")
print(T1.to_string())
T1.to_csv("outputs/ha_table1.csv")

# ---------------- Table 2: turnover by type and gender ----------------
rows = []
for sexlab, mask in [("All", P["A_SEX"].notna()), ("Women", P["A_SEX"] == 2),
                     ("Men", P["A_SEX"] == 1)]:
    for prof, d in P[mask].groupby("prof"):
        rows.append({"sample": sexlab, "profession": prof,
                     "left_all": round(wm(d, "left") * 100, 2),
                     "switch": round(wm(d, "switch") * 100, 2),
                     "unemployed": round(wm(d, "unemp") * 100, 2),
                     "left_LF": round(wm(d, "leftlf") * 100, 2)})
T2 = pd.DataFrame(rows)
print("\n=== TABLE 2 (updated): turnover by type, profession, gender ===")
print(T2.pivot(index="profession", columns="sample",
               values="left_all").round(2).to_string())
print("\n(All sample, by type)")
print(T2[T2["sample"] == "All"].set_index("profession")
      [["left_all", "switch", "unemployed", "left_LF"]].to_string())
T2.to_csv("outputs/ha_table2.csv", index=False)

# ---------------- Table 3: teacher dummy with cumulative controls -------
P["teacher"] = (P["prof"] == "Teachers").astype(int)
P["female"] = (P["A_SEX"] == 2).astype(int)
P["black"] = (P["PRDTRACE"] == 2).astype(int)
P["married"] = P["A_MARITL"].isin([1, 2, 3]).astype(int)
P["sepdiv"] = P["A_MARITL"].isin([5, 6]).astype(int)
P["advdeg"] = (P["A_HGA"] >= 44).astype(int)
P["age2"] = P["A_AGE"] ** 2
P["lweek"] = np.where((P["WSAL_VAL"] > 0) & (P["WKSWORK"] > 0),
                      np.log((P["WSAL_VAL"] / P["WKSWORK"]).clip(lower=1)),
                      np.nan)
P["pension"] = (P["PENPLAN"] == 1).astype(int)
DEMOG = ["A_AGE", "age2", "female", "black", "married", "sepdiv", "advdeg"]
JOB = ["lweek", "pension"]

print("\n=== TABLE 3 (updated): teacher coefficient (pp), LPM, "
      "cumulative controls ===")
t3 = []
for comp in ["Nurses", "Social workers", "Accountants"]:
    sub0 = P[P["prof"].isin(["Teachers", comp])].copy()
    yd = pd.get_dummies(sub0["asec_year"], prefix="y", drop_first=True,
                        dtype=float)
    for lab, ctr in [("no controls", []), ("+ demographics", DEMOG),
                     ("+ job chars", DEMOG + JOB)]:
        sub = sub0.dropna(subset=ctr + ["left", W]) if ctr else sub0
        X = pd.concat([sub[["teacher"] + ctr],
                       yd.loc[sub.index] if lab != "no controls" else
                       pd.DataFrame(index=sub.index)], axis=1)
        X = sm.add_constant(X.astype(float))
        m = sm.WLS(sub["left"].astype(float), X, weights=sub[W]).fit(
            cov_type="HC1")
        t3.append({"comparison": comp, "controls": lab,
                   "teacher_coef_pp": round(m.params["teacher"] * 100, 2),
                   "se_pp": round(m.bse["teacher"] * 100, 2),
                   "n": int(m.nobs)})
T3 = pd.DataFrame(t3)
print(T3.to_string(index=False))
T3.to_csv("outputs/ha_table3.csv", index=False)

# ---------------- Table 4-lite: determinants per profession -------------
print("\n=== TABLE 4-lite: LPM determinants per profession "
      "(coef pp, HC1 SE) ===")
t4 = []
for prof, d in P.groupby("prof"):
    sub = d.dropna(subset=DEMOG + JOB + ["left", W])
    X = sm.add_constant(sub[DEMOG + JOB].astype(float))
    m = sm.WLS(sub["left"].astype(float), X, weights=sub[W]).fit(
        cov_type="HC1")
    for v in ["A_AGE", "age2", "female", "lweek", "pension"]:
        t4.append({"profession": prof, "var": v,
                   "coef_pp": round(m.params[v] * 100, 3),
                   "se_pp": round(m.bse[v] * 100, 3)})
T4 = pd.DataFrame(t4)
print(T4.pivot(index="var", columns="profession",
               values="coef_pp").to_string())
T4.to_csv("outputs/ha_table4.csv", index=False)

# ---------------- Table 5-lite: turnover by age group -------------------
print("\n=== TABLE 5-lite: turnover by age group ===")
bins = [(21, 25), (26, 30), (31, 35), (36, 40), (41, 45), (46, 50),
        (51, 55), (56, 60), (61, 64), (65, 99)]
t5 = []
for lo, hi in bins:
    row = {"age": f"{lo}-{hi}"}
    for prof, d in P[P["A_AGE"].between(lo, hi)].groupby("prof"):
        row[prof] = round(wm(d, "left") * 100, 1)
    t5.append(row)
T5 = pd.DataFrame(t5).set_index("age")
print(T5.to_string())
T5.to_csv("outputs/ha_table5.csv")
# teachers by type at older ages (their retirement finding)
old = P[(P["prof"] == "Teachers") & P["A_AGE"].between(56, 64)]
print(f"\nteachers 56-64: left {wm(old,'left')*100:.1f}%  of which left-LF "
      f"{wm(old,'leftlf')*100:.1f}pp (retirement channel)")

# ---------------- annual teacher series + public/private ----------------
print("\n=== teachers: annual series (calendar year = survey - 1) ===")
ann = []
for ay, d in P[P["prof"] == "Teachers"].groupby("asec_year"):
    ann.append({"cal_year": int(ay) - 1,
                "turnover_%": round(wm(d, "left") * 100, 2), "n": len(d)})
A = pd.DataFrame(ann)
print(A.to_string(index=False))
A.to_csv("outputs/ha_annual.csv", index=False)
tch = P[P["prof"] == "Teachers"]
pub = tch[tch["LJCW"].isin([2, 3, 4])]
prv = tch[tch["LJCW"] == 1]
print(f"\npublic-school teachers : {wm(pub,'left')*100:.2f}%  (n={len(pub):,})")
print(f"private-school teachers: {wm(prv,'left')*100:.2f}%  (n={len(prv):,})")
print("\nH&A 1992-2001 benchmarks: teachers 7.73 (sw 2.59/un 0.61/lf 4.53); "
      "nurses 6.09; social workers 14.94; accountants 8.01; public 6.59")
