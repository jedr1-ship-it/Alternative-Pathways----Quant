"""
Analysis engine for the full paper. Consumes asec_rich_{11..25}.parquet
(surveys 2011-2025 = calendar 2010-2024) plus the minimal asec_id_{06..10}
files (calendar 2005-2009, rate only), and writes every table the paper
needs to outputs/p_*.csv.

Temporal comparisons run through everything: annual series, half-decade
panels, and the Harris & Adams 1992-2001 benchmarks as the long anchor.
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.api as sm

RAW = "data/raw/asec"
W = "MARSUPWT"
CORE = {2300, 2310, 2320, 2330}


def tset(ay):
    return CORE | ({2340} if ay <= 2019 else {2360})


def profs(ay):
    old = ay <= 2019
    return {"Teachers": tset(ay),
            "Nurses": {3255, 3256, 3257, 3258, 3500},
            "Social workers": {2010} if old else {2011, 2012, 2013, 2014},
            "Accountants": {800},
            "Lawyers": {2100},
            "Physicians": {3060} if old else {3090, 3100},
            "Pharmacists": {3050},
            "Physical therapists": {3160}}


def wavg(d, col, w=W):
    v = d[col].astype(float)
    ok = v.notna() & d[w].notna()
    return np.average(v[ok], weights=d.loc[ok, w]) if ok.any() else np.nan


# ---------------- load rich years and derive person variables -------------
rich = []
for f in sorted(glob.glob(f"{RAW}/asec_rich_*.parquet")):
    d = pd.read_parquet(f)
    rich.append(d)
R = pd.concat(rich, ignore_index=True)
for c in R.columns:
    if c != "PERIDNUM":
        R[c] = pd.to_numeric(R[c], errors="coerce")
R["cal_year"] = R["asec_year"] - 1

# own children from the parent pointers: A_PARENT in the fixed-width years,
# PEPAR1/PEPAR2 (both parents) in the CSV years; spouse crediting below
# covers the second parent where only one pointer exists.
ptr = []
for c in ["A_PARENT", "PEPAR1", "PEPAR2"]:
    if c in R.columns:
        k = R[(pd.to_numeric(R[c], errors="coerce") > 0)
              & (R["A_AGE"] < 18)][["asec_year", "PH_SEQ", c, "A_AGE",
                                    "A_LINENO"]].rename(
            columns={c: "parent_line", "A_LINENO": "kid_line"})
        ptr.append(k)
kids = pd.concat(ptr, ignore_index=True).drop_duplicates(
    ["asec_year", "PH_SEQ", "parent_line", "kid_line"])
agg = kids.groupby(["asec_year", "PH_SEQ", "parent_line"])["A_AGE"].agg(
    n_children="size", child_u6=lambda s: int((s < 6).any()),
    new_baby=lambda s: int((s < 1).any())).reset_index().rename(
    columns={"parent_line": "A_LINENO"})
R = R.merge(agg, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
sp = R[R["A_SPOUSE"] > 0][["asec_year", "PH_SEQ", "A_SPOUSE",
                           "n_children", "child_u6", "new_baby"]].rename(
    columns={"A_SPOUSE": "A_LINENO", "n_children": "n2", "child_u6": "c2",
             "new_baby": "b2"})
sp = sp.groupby(["asec_year", "PH_SEQ", "A_LINENO"]).max().reset_index()
R = R.merge(sp, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
for a, b in [("n_children", "n2"), ("child_u6", "c2"), ("new_baby", "b2")]:
    R[a] = R[[a, b]].max(axis=1).fillna(0)
R = R.drop(columns=["n2", "c2", "b2"])

R["female"] = (R["A_SEX"] == 2).astype(int)
R["black"] = (R["PRDTRACE"] == 2).astype(int)
R["married"] = R["A_MARITL"].isin([1, 2, 3]).astype(int)
R["sepdiv"] = R["A_MARITL"].isin([5, 6]).astype(int)
R["ba_plus"] = (R["A_HGA"] >= 43).astype(int)
R["ma_plus"] = (R["A_HGA"] >= 44).astype(int)
R["public"] = R["LJCW"].isin([2, 3, 4]).astype(int)
R["pension"] = (R["PENPLAN"] == 1).astype(int)
R["parttime"] = R["HRSWK"].between(1, 34).astype(int)
R["fullyear"] = (R["WKSWORK"] >= 50).astype(int)
R["age2"] = R["A_AGE"] ** 2


def outcomes(b, cset):
    emp = b["A_LFSR"].isin([1, 2])
    b["switch"] = (emp & ~b["PEIOOCC"].isin(cset)).astype(int)
    b["unemp"] = b["A_LFSR"].isin([3, 4]).astype(int)
    b["leftlf"] = (~b["A_LFSR"].isin([1, 2, 3, 4])).astype(int)
    b["leaver"] = (b["switch"] | b["unemp"] | b["leftlf"]).astype(int)
    return b


# teacher universe, BA+ (main) and all-educ (series robustness)
teach = []
for ay, g in R.groupby("asec_year"):
    cs = tset(int(ay))
    b = outcomes(g[g["OCCUP"].isin(cs)].copy(), cs)
    teach.append(b)
T = pd.concat(teach, ignore_index=True)
TB = T[(T["ba_plus"] == 1) & (T["A_AGE"] >= 18)]
print(f"teachers: {len(T):,} all-educ, {len(TB):,} BA+ "
      f"(cal {int(T['cal_year'].min())}-{int(T['cal_year'].max())})")

# ---------------- 1. long annual series (cal 2005-2024) -------------------
rows = []
for yy in ("06", "07", "08", "09", "10"):
    d = pd.read_parquet(f"{RAW}/asec_id_{yy}.parquet")
    for c in ("OCCUP", "PEIOOCC"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    cs = CORE | {2340}
    b = d[d["OCCUP"].isin(cs)]
    rows.append({"cal_year": 2000 + int(yy) - 1,
                 "leaver_all": round((~b["PEIOOCC"].isin(cs)).mean() * 100, 2),
                 "leaver_ba": np.nan, "n": len(b), "weighted": 0})
for cy, g in T.groupby("cal_year"):
    gb = g[(g["ba_plus"] == 1) & (g["A_AGE"] >= 18)]
    rows.append({"cal_year": int(cy),
                 "leaver_all": round(wavg(g, "leaver") * 100, 2),
                 "leaver_ba": round(wavg(gb, "leaver") * 100, 2),
                 "n": len(g), "weighted": 1})
S = pd.DataFrame(rows).sort_values("cal_year")
S.to_csv("outputs/p_series.csv", index=False)
print("\n=== annual leaver series ===")
print(S.to_string(index=False))

# ---------------- 2. workforce composition by year (F2) -------------------
comp = []
for cy, g in TB.groupby("cal_year"):
    comp.append({"cal_year": int(cy),
                 "female": round(wavg(g, "female") * 100, 1),
                 "age": round(wavg(g, "A_AGE"), 1),
                 "ma_plus": round(wavg(g, "ma_plus") * 100, 1),
                 "public": round(wavg(g, "public") * 100, 1),
                 "parttime": round(wavg(g, "parttime") * 100, 1),
                 "pension": round(wavg(g, "pension") * 100, 1),
                 "black": round(wavg(g, "black") * 100, 1),
                 "child_u6": round(wavg(g, "child_u6") * 100, 1)})
pd.DataFrame(comp).to_csv("outputs/p_workforce.csv", index=False)

# ---------------- 3. of every 100 leavers (F4) ----------------------------
win = TB[TB["cal_year"].between(2015, 2024)]
L = win[win["leaver"] == 1].copy()
edu_adj = L["PEIOOCC"].between(2200, 2555) & (L["switch"] == 1)
oth_sw = (L["switch"] == 1) & ~edu_adj
un = L["unemp"] == 1
lf_old = (L["leftlf"] == 1) & (L["A_AGE"] >= 55)
lf_yng = (L["leftlf"] == 1) & (L["A_AGE"] < 55)
wl = L[W]
f4 = {"education-adjacent job": np.average(edu_adj, weights=wl) * 100,
      "other occupation": np.average(oth_sw, weights=wl) * 100,
      "unemployed": np.average(un, weights=wl) * 100,
      "out of LF, under 55": np.average(lf_yng, weights=wl) * 100,
      "out of LF, 55plus": np.average(lf_old, weights=wl) * 100}
pd.Series(f4).round(1).to_csv("outputs/p_flow100_leavers.csv")
print("\n=== of every 100 leavers ===")
print(pd.Series(f4).round(1).to_string())

# earlier decade for the temporal comparison
win2 = TB[TB["cal_year"].between(2010, 2014)]
L2 = win2[win2["leaver"] == 1]
f4b = {"switch": wavg(L2, "switch") * 100, "unemp": wavg(L2, "unemp") * 100,
       "leftlf": wavg(L2, "leftlf") * 100}
pd.Series(f4b).round(1).to_csv("outputs/p_flow_2010s.csv")

# ---------------- 4. exit routes over the lifecycle (F5) ------------------
r5 = []
for lo, hi in [(21, 25), (26, 30), (31, 35), (36, 40), (41, 45), (46, 50),
               (51, 55), (56, 60), (61, 64), (65, 80)]:
    d = win[win["A_AGE"].between(lo, hi)]
    r5.append({"age": f"{lo}-{hi}",
               "switch": round(wavg(d, "switch") * 100, 2),
               "unemp": round(wavg(d, "unemp") * 100, 2),
               "leftlf": round(wavg(d, "leftlf") * 100, 2),
               "total": round(wavg(d, "leaver") * 100, 2)})
pd.DataFrame(r5).to_csv("outputs/p_routes_age.csv", index=False)

# ---------------- 5. earnings at destination (F6) -------------------------
link = []
for ay in range(2011, 2025):
    t0 = T[(T["asec_year"] == ay) & (T["ba_plus"] == 1)
           & T["PERIDNUM"].notna()].copy()
    b = R[R["asec_year"] == ay + 1][["PERIDNUM", "WSAL_VAL", "WKSWORK",
                                     "A_SEX", "A_AGE"]]
    m = t0.merge(b, on="PERIDNUM", suffixes=("", "_1"))
    m = m[(m["A_SEX"] == m["A_SEX_1"])
          & (m["A_AGE_1"] - m["A_AGE"]).between(0, 2)]
    link.append(m)
LK = pd.concat(link, ignore_index=True)
LK = LK[(LK["WSAL_VAL"] > 0)]
LK["earn0"] = LK["WSAL_VAL"]
LK["earn1"] = LK["WSAL_VAL_1"]
LK["dlog"] = np.where(LK["earn1"] > 0,
                      np.log(LK["earn1"]) - np.log(LK["earn0"]), np.nan)
res6 = []
for lab, m in [("stayer", LK["leaver"] == 0),
               ("leaver, employed", (LK["switch"] == 1)),
               ("leaver, all", LK["leaver"] == 1)]:
    d = LK[m & LK["dlog"].notna()]
    qs = np.percentile(d["dlog"], [10, 25, 50, 75, 90]) * 100
    res6.append({"group": lab, "n": len(d),
                 **{f"p{p}": round(q, 1) for p, q in
                    zip([10, 25, 50, 75, 90], qs)}})
    # share with any earnings in the transition year
zero = LK[LK["leaver"] == 1]
res6.append({"group": "leaver, share zero earnings next year",
             "n": int((zero["earn1"] <= 0).sum()),
             "p50": round(np.average((zero["earn1"] <= 0),
                                     weights=zero[W]) * 100, 1)})
pd.DataFrame(res6).to_csv("outputs/p_earnings_gamble.csv", index=False)
print("\n=== earnings gamble (linked March-to-March, dlog x100) ===")
print(pd.DataFrame(res6).to_string(index=False))

# ---------------- 6. enriched probit (F7) + top decile --------------------
XV = ["A_AGE", "age2", "female", "black", "married", "sepdiv", "ma_plus",
      "public", "pension", "parttime", "fullyear", "n_children", "child_u6",
      "new_baby"]
sub = win.dropna(subset=XV + ["leaver", W]).copy()
yd = pd.get_dummies(sub["asec_year"], prefix="y", drop_first=True,
                    dtype=float)
X = sm.add_constant(pd.concat([sub[XV].astype(float), yd], axis=1))
pm = sm.Probit(sub["leaver"].astype(float), X).fit(disp=0)
ame = pm.get_margeff(at="overall")
AME = pd.DataFrame({"var": XV,
                    "AME_pp": (ame.margeff[:len(XV)] * 100).round(2),
                    "se_pp": (ame.margeff_se[:len(XV)] * 100).round(2)})
AME.to_csv("outputs/p_ame.csv", index=False)
print("\n=== probit AME (BA+ teachers, 2015-2024) ===")
print(AME.sort_values("AME_pp", key=abs, ascending=False).to_string(index=False))
sub["phat"] = pm.predict(X)
top = sub[sub["phat"] >= sub["phat"].quantile(0.9)]
dec = []
for lab, v in [("Age", "A_AGE"), ("Female %", "female"),
               ("Part-time %", "parttime"), ("Full-year %", "fullyear"),
               ("Pension %", "pension"), ("Public %", "public"),
               ("Actual leaver rate %", "leaver")]:
    scale = 1 if lab == "Age" else 100
    dec.append({"trait": lab, "top decile": round(wavg(top, v) * scale, 1),
                "all teachers": round(wavg(sub, v) * scale, 1)})
pd.DataFrame(dec).to_csv("outputs/p_topdecile.csv", index=False)

# ---------------- 7. professions: level + new-baby effect (F8, F9) --------
rows8, rows9 = [], []
for ay, g in R[(R["ba_plus"] == 1) & (R["A_AGE"] >= 18)].groupby("asec_year"):
    for prof, cs in profs(int(ay)).items():
        b = outcomes(g[g["OCCUP"].isin(cs)].copy(), cs)
        b["prof"] = prof
        rows8.append(b)
P8 = pd.concat(rows8, ignore_index=True)
lev = []
for prof, d in P8.groupby("prof"):
    for per, m in [("2010-2014", d["cal_year"].between(2010, 2014)),
                   ("2015-2024", d["cal_year"].between(2015, 2024))]:
        lev.append({"prof": prof, "period": per,
                    "leaver_%": round(wavg(d[m], "leaver") * 100, 2),
                    "n": int(m.sum())})
pd.DataFrame(lev).to_csv("outputs/p_professions.csv", index=False)
print("\n=== professions ===")
print(pd.DataFrame(lev).pivot(index="prof", columns="period",
                              values="leaver_%").to_string())

# new-baby AME for women, per profession (the fig18 replication)
for prof in ["Teachers", "Nurses", "Social workers", "Accountants",
             "Lawyers"]:
    d = P8[(P8["prof"] == prof) & (P8["female"] == 1)
           & P8["cal_year"].between(2010, 2024)]
    d = d.dropna(subset=["leaver", "new_baby", "A_AGE", W])
    Xv = ["A_AGE", "age2", "married", "ma_plus", "new_baby", "child_u6",
          "n_children"]
    X9 = sm.add_constant(d[Xv].astype(float))
    try:
        m9 = sm.Probit(d["leaver"].astype(float), X9).fit(disp=0)
        a9 = m9.get_margeff(at="overall")
        i = Xv.index("new_baby")
        rows9.append({"prof": prof, "AME_newbaby_pp":
                      round(a9.margeff[i] * 100, 2),
                      "se_pp": round(a9.margeff_se[i] * 100, 2),
                      "n": int(m9.nobs)})
    except Exception as e:
        rows9.append({"prof": prof, "AME_newbaby_pp": np.nan,
                      "se_pp": np.nan, "n": len(d)})
pd.DataFrame(rows9).to_csv("outputs/p_newbaby.csv", index=False)
print("\n=== new-baby AME, women, by profession ===")
print(pd.DataFrame(rows9).to_string(index=False))
print("\nall outputs written to outputs/p_*.csv")
