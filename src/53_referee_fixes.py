"""
Implement the referee report's substantive fixes.

(A3)  One definition of "education and care" used everywhere: the four
      green groups (postsecondary, school support, education admin,
      counseling/social work/childcare). Flow-of-100 recomputed with it,
      plus an explicit Unclassified remainder.
(B1)  Timing audit of the new-baby effect: among linked teachers, the
      share of new-mother leavers who are teaching again the following
      March, versus other prime-age leavers.
(B4)  Sampling errors for the headline aggregates and the annual series.
(B5)  Harmonized old-style series (unweighted, occupation-pair only) for
      2010-2024, to validate the pre-2010 segment against the same
      construction; missing years written as explicit gaps.
(F)   Extended new-baby profession panel (all eight professions).
(T)   Tables regenerated: profile with significance stars and dollar
      formatting, destinations with scheme-duplicates merged, series with
      gap rows and SEs, top-decile reordered, probit relabeled.
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
            "Accountants": {800}, "Lawyers": {2100},
            "Physicians": {3060} if old else {3090, 3100},
            "Pharmacists": {3050}, "Physical therapists": {3160}}


def wavg(d, col, w=W):
    v = d[col].astype(float)
    ok = v.notna() & d[w].notna()
    return np.average(v[ok], weights=d.loc[ok, w]) if ok.any() else np.nan


# ---------- rebuild person universe (as in 47/50) ----------
R = pd.concat([pd.read_parquet(f) for f in
               sorted(glob.glob(f"{RAW}/asec_rich_*.parquet"))],
              ignore_index=True)
for c in R.columns:
    if c != "PERIDNUM":
        R[c] = pd.to_numeric(R[c], errors="coerce")
R["cal_year"] = R["asec_year"] - 1
ptr = []
for c in ["A_PARENT", "PEPAR1", "PEPAR2"]:
    k = R[(pd.to_numeric(R[c], errors="coerce") > 0) & (R["A_AGE"] < 18)][
        ["asec_year", "PH_SEQ", c, "A_AGE", "A_LINENO"]].rename(
        columns={c: "parent_line", "A_LINENO": "kid_line"})
    ptr.append(k)
kids = pd.concat(ptr, ignore_index=True).drop_duplicates(
    ["asec_year", "PH_SEQ", "parent_line", "kid_line"])
agg = kids.groupby(["asec_year", "PH_SEQ", "parent_line"])["A_AGE"].agg(
    n_children="size", child_u6=lambda s: int((s < 6).any()),
    new_baby=lambda s: int((s < 1).any())).reset_index().rename(
    columns={"parent_line": "A_LINENO"})
R = R.merge(agg, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
sp = R[R["A_SPOUSE"] > 0][["asec_year", "PH_SEQ", "A_SPOUSE", "n_children",
                           "child_u6", "new_baby"]].rename(
    columns={"A_SPOUSE": "A_LINENO", "n_children": "n2", "child_u6": "c2",
             "new_baby": "b2"})
sp = sp.groupby(["asec_year", "PH_SEQ", "A_LINENO"]).max().reset_index()
R = R.merge(sp, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
for a, b in [("n_children", "n2"), ("child_u6", "c2"), ("new_baby", "b2")]:
    R[a] = R[[a, b]].max(axis=1).fillna(0)
R["female"] = (R["A_SEX"] == 2).astype(int)
R["ba_plus"] = (R["A_HGA"] >= 43).astype(int)
R["ma_plus"] = (R["A_HGA"] >= 44).astype(int)
R["married"] = R["A_MARITL"].isin([1, 2, 3]).astype(int)
R["age2"] = R["A_AGE"] ** 2

teach = []
for ay, g in R.groupby("asec_year"):
    cs = tset(int(ay))
    b = g[g["OCCUP"].isin(cs)].copy()
    emp = b["A_LFSR"].isin([1, 2])
    b["switch"] = (emp & ~b["PEIOOCC"].isin(cs)).astype(int)
    b["unemp"] = b["A_LFSR"].isin([3, 4]).astype(int)
    b["leftlf"] = (~b["A_LFSR"].isin([1, 2, 3, 4])).astype(int)
    b["leaver"] = (b["switch"] | b["unemp"] | b["leftlf"]).astype(int)
    teach.append(b)
T = pd.concat(teach, ignore_index=True)
TB = T[(T["ba_plus"] == 1) & (T["A_AGE"] >= 18)]
win = TB[TB["cal_year"].between(2015, 2024)].copy()

# ---------- (A3) unified education-and-care definition ----------
EDU_CARE = ({2200, 2205} | {2340, 2350, 2360, 2540, 2545, 2430, 2435, 2440,
                            2550, 2555} | {230}
            | {2001, 2002, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2025,
               4600})
L = win[win["leaver"] == 1]
wl = L[W].sum()
sw = L[L["switch"] == 1]
educare = sw[sw["PEIOOCC"].isin(EDU_CARE)][W].sum() / wl * 100
other = sw[~sw["PEIOOCC"].isin(EDU_CARE)][W].sum() / wl * 100
un = L[L["unemp"] == 1][W].sum() / wl * 100
lf_y = L[(L["leftlf"] == 1) & (L["A_AGE"] < 55)][W].sum() / wl * 100
lf_o = L[(L["leftlf"] == 1) & (L["A_AGE"] >= 55)][W].sum() / wl * 100
F4 = pd.Series({"education and care job": educare,
                "other occupation": other, "unemployed": un,
                "out of LF, under 55": lf_y, "out of LF, 55plus": lf_o})
F4.round(1).to_csv("outputs/p_flow100_leavers.csv")
print("flow of 100 leavers (unified):")
print(F4.round(1).to_string(), f"  sum={F4.sum():.1f}")

# destination groups with explicit unclassified remainder
DG = pd.read_csv("outputs/q_dest_groups.csv")
uncl = round(sw[W].sum() / wl * 100 - DG["per100_leavers"].sum(), 1)
DG = pd.concat([DG, pd.DataFrame([{"group": "Unclassified",
                                   "per100_leavers": uncl,
                                   "per100_switchers": round(
                                       uncl * wl / sw[W].sum(), 1)}])],
               ignore_index=True)
DG.to_csv("outputs/q_dest_groups.csv", index=False)
print(f"unclassified remainder: {uncl}")

# ---------- (B1) new-baby timing audit ----------
rows = []
for ay in range(2011, 2025):
    t0 = T[(T["asec_year"] == ay) & (T["ba_plus"] == 1)
           & (T["female"] == 1) & T["PERIDNUM"].notna()]
    nxt = R[R["asec_year"] == ay + 1][["PERIDNUM", "PEIOOCC", "A_SEX",
                                       "A_AGE"]]
    m = t0.merge(nxt, on="PERIDNUM", suffixes=("", "_1"))
    m = m[(m["A_SEX"] == m["A_SEX_1"])
          & (m["A_AGE_1"] - m["A_AGE"]).between(0, 2)]
    m["teach_next"] = m["PEIOOCC_1"].isin(tset(ay + 1)).astype(int)
    rows.append(m)
LKB = pd.concat(rows, ignore_index=True)
lv = LKB[LKB["leaver"] == 1]
nb = lv[(lv["new_baby"] == 1)]
ot = lv[(lv["new_baby"] == 0) & lv["A_AGE"].between(23, 45)]
r_nb = wavg(nb, "teach_next") * 100
r_ot = wavg(ot, "teach_next") * 100
print(f"\nB1 return audit: new-mother leavers teaching again next March: "
      f"{r_nb:.0f}% (n={len(nb)}) vs other leavers 23-45: {r_ot:.0f}% "
      f"(n={len(ot)})")
pd.DataFrame([{"group": "new-mother leavers", "back_next_year_%":
               round(r_nb, 1), "n": len(nb)},
              {"group": "other leavers 23-45", "back_next_year_%":
               round(r_ot, 1), "n": len(ot)}]).to_csv(
    "outputs/p_baby_return.csv", index=False)

# ---------- (B4/B5) series with SEs, old-style overlap, explicit gaps ----
T90 = {155, 156, 157, 158, 159}
rows = []
for f in sorted(glob.glob(f"{RAW}/asec_90s_*.parquet")):
    d = pd.read_parquet(f)
    ay = int(d["asec_year"].iloc[0])
    cs = T90 if ay <= 2002 else (CORE | {2340})
    b = d[d["OCCUP"].isin(cs)]
    p = (~b["PEIOOCC"].isin(cs)).mean()
    rows.append({"cal_year": ay - 1, "leaver_all": np.nan,
                 "leaver_ba": np.nan,
                 "leaver_oldstyle": round(p * 100, 2),
                 "se_ba": np.nan, "n": len(b), "weighted": 0})
for yy in ("06", "07", "08", "09", "10"):
    d = pd.read_parquet(f"{RAW}/asec_id_{yy}.parquet")
    for c in ("OCCUP", "PEIOOCC"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    cs = CORE | {2340}
    b = d[d["OCCUP"].isin(cs)]
    p = (~b["PEIOOCC"].isin(cs)).mean()
    rows.append({"cal_year": 2000 + int(yy) - 1, "leaver_all": np.nan,
                 "leaver_ba": np.nan,
                 "leaver_oldstyle": round(p * 100, 2),
                 "se_ba": np.nan, "n": len(b), "weighted": 0})
for ay, g in T.groupby("asec_year"):
    cs = tset(int(ay))
    gb = g[(g["ba_plus"] == 1) & (g["A_AGE"] >= 18)]
    pba = wavg(gb, "leaver")
    se = np.sqrt(1.5 * pba * (1 - pba) / len(gb)) * 100
    oldstyle = (~g["PEIOOCC"].isin(cs)).mean() * 100  # unweighted, occ-pair
    rows.append({"cal_year": int(ay) - 1,
                 "leaver_all": round(wavg(g, "leaver") * 100, 2),
                 "leaver_ba": round(pba * 100, 2),
                 "leaver_oldstyle": round(oldstyle, 2),
                 "se_ba": round(se, 2), "n": len(g), "weighted": 1})
S = pd.DataFrame(rows)
for gap in (1998, 2002, 2003, 2004):
    S = pd.concat([S, pd.DataFrame([{"cal_year": gap, "leaver_all": np.nan,
                                     "leaver_ba": np.nan,
                                     "leaver_oldstyle": np.nan,
                                     "se_ba": np.nan, "n": 0,
                                     "weighted": 0}])], ignore_index=True)
S = S.sort_values("cal_year").reset_index(drop=True)
S.to_csv("outputs/p_series.csv", index=False)
print("\nseries with old-style overlap (2010+ shown):")
print(S[S["weighted"] == 1][["cal_year", "leaver_ba", "se_ba",
                             "leaver_all", "leaver_oldstyle"]]
      .head(4).to_string(index=False))

# pooled headline SE
p = wavg(win, "leaver")
se = np.sqrt(1.5 * p * (1 - p) / len(win)) * 100
print(f"\nheadline 2015-2024: {p*100:.2f}%  SE~{se:.2f}pp")

# ---------- (F) new-baby AMEs for all eight professions ----------
rows8, rows9 = [], []
for ay, g in R[(R["ba_plus"] == 1) & (R["A_AGE"] >= 18)].groupby("asec_year"):
    for prof, cs in profs(int(ay)).items():
        b = g[g["OCCUP"].isin(cs)].copy()
        emp = b["A_LFSR"].isin([1, 2])
        b["leaver"] = (~(emp & b["PEIOOCC"].isin(cs))).astype(int)
        b["prof"] = prof
        rows8.append(b)
P8 = pd.concat(rows8, ignore_index=True)
for prof in ["Teachers", "Nurses", "Social workers", "Accountants",
             "Lawyers", "Physicians", "Pharmacists", "Physical therapists"]:
    d = P8[(P8["prof"] == prof) & (P8["female"] == 1)
           & P8["cal_year"].between(2010, 2024)]
    d = d.dropna(subset=["leaver", "new_baby", "A_AGE", W])
    Xv = ["A_AGE", "age2", "married", "ma_plus", "new_baby", "child_u6",
          "n_children"]
    X9 = sm.add_constant(d[Xv].astype(float))
    try:
        m9 = sm.Probit(d["leaver"].astype(float), X9).fit(disp=0,
                                                          maxiter=200)
        if not m9.mle_retvals["converged"]:
            raise RuntimeError("no convergence")
        a9 = m9.get_margeff(at="overall")
        i = Xv.index("new_baby")
        rows9.append({"prof": prof,
                      "AME_newbaby_pp": round(a9.margeff[i] * 100, 2),
                      "se_pp": round(a9.margeff_se[i] * 100, 2),
                      "n": int(m9.nobs)})
    except Exception:
        print(f"  {prof}: women probit failed (n={len(d)}), omitted")
NB = pd.DataFrame(rows9)
NB.to_csv("outputs/p_newbaby.csv", index=False)
print("\nnew-baby panel (8 professions attempted):")
print(NB.to_string(index=False))

# ---------- (T) regenerate tables ----------
# profile with stars and $ formatting
S_, L_ = win[win["leaver"] == 0], win[win["leaver"] == 1]
VARS_ = [("Age, years", "A_AGE", "num"),
         ("Female", "female", "pct"),
         ("Black", None, "pct"), ("Married", "married", "pct"),
         ("Separated or divorced", None, "pct"),
         ("Master's degree or higher", "ma_plus", "pct"),
         ("Public school", None, "pct"),
         ("Enrolled in a pension plan", None, "pct"),
         ("Part-time ($<$35 h/week)", None, "pct"),
         ("Worked full year (50+ weeks)", None, "pct"),
         ("Weekly earnings", None, "usd")]
win["black"] = (win["PRDTRACE"] == 2).astype(int)
win["sepdiv"] = win["A_MARITL"].isin([5, 6]).astype(int)
win["public"] = win["LJCW"].isin([2, 3, 4]).astype(int)
win["pension"] = (win["PENPLAN"] == 1).astype(int)
win["parttime"] = win["HRSWK"].between(1, 34).astype(int)
win["fullyear"] = (win["WKSWORK"] >= 50).astype(int)
win["earn_wk"] = np.where((win["WSAL_VAL"] > 0) & (win["WKSWORK"] > 0),
                          win["WSAL_VAL"] / win["WKSWORK"], np.nan)
COLMAP = {"Age, years": "A_AGE", "Female": "female", "Black": "black",
          "Married": "married", "Separated or divorced": "sepdiv",
          "Master's degree or higher": "ma_plus", "Public school": "public",
          "Enrolled in a pension plan": "pension",
          "Part-time ($<$35 h/week)": "parttime",
          "Worked full year (50+ weeks)": "fullyear",
          "Weekly earnings": "earn_wk"}
S_, L_ = win[win["leaver"] == 0], win[win["leaver"] == 1]


def wse(d, col):
    v = d[col].astype(float).dropna()
    return v.std(ddof=1) / np.sqrt(len(v))


with open("report/table_m_profile.tex", "w") as fh:
    fh.write("\\begin{tabular}{lccc}\n\\toprule\n"
             " & Stayers & Leavers & Difference \\\\\n\\midrule\n")
    for lab, _, kind in VARS_:
        col = COLMAP[lab]
        a, b = wavg(S_, col), wavg(L_, col)
        t = abs(b - a) / np.sqrt(wse(S_, col) ** 2 + wse(L_, col) ** 2)
        star = "$^{***}$" if t > 2.58 else "$^{**}$" if t > 1.96 else \
            "$^{*}$" if t > 1.64 else ""
        if kind == "pct":
            fh.write(f"{lab} & {a*100:.1f}\\% & {b*100:.1f}\\% & "
                     f"{(b-a)*100:+.1f}{star} \\\\\n")
        elif kind == "usd":
            fh.write(f"{lab} & \\${a:,.0f} & \\${b:,.0f} & "
                     f"\\${b-a:+,.0f}{star} \\\\\n")
        else:
            fh.write(f"{lab} & {a:.1f} & {b:.1f} & {b-a:+.1f}{star} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# destinations with duplicates merged
D = pd.read_csv("outputs/main_destinations.csv")
D["label"] = D["occupation"].replace({"?": np.nan})
MANUAL = {2200: "Postsecondary teachers", 2540: "Teaching assistants"}
D["label"] = D.apply(lambda r: MANUAL.get(int(r["PEIOOCC"]),
                                          r["label"]), axis=1)
DM = D.groupby("label", as_index=False)["share_%"].sum() \
    .sort_values("share_%", ascending=False)
with open("report/table_m_destinations.tex", "w") as fh:
    fh.write("\\begin{tabular}{lc}\n\\toprule\nDestination occupation & "
             "Share of switchers \\\\\n\\midrule\n")
    for _, r in DM.iterrows():
        fh.write(f"{r['label']} & {r['share_%']:.1f}\\% \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# series table with explicit gap rows
with open("report/table_p_series.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccc}\n\\toprule\nCalendar year & College "
             "graduates & All teachers & Old-style (unwtd.) & Obs. "
             "\\\\\n\\midrule\n")
    for _, r in S.iterrows():
        if r["n"] == 0:
            fh.write(f"{int(r['cal_year'])} & -- & -- & -- & -- \\\\\n")
            continue
        ba = (f"{r['leaver_ba']:.1f}\\% ({r['se_ba']:.1f})"
              if pd.notna(r["leaver_ba"]) else "--")
        al = f"{r['leaver_all']:.1f}\\%" if pd.notna(r["leaver_all"]) else \
            "--"
        os_ = f"{r['leaver_oldstyle']:.1f}\\%" \
            if pd.notna(r["leaver_oldstyle"]) else "--"
        fh.write(f"{int(r['cal_year'])} & {ba} & {al} & {os_} & "
                 f"{int(r['n']):,} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# top-decile reordered, leaver rate first and bold
D5 = pd.read_csv("outputs/p_topdecile.csv")
D5 = pd.concat([D5[D5["trait"] == "Actual leaver rate %"],
                D5[D5["trait"] != "Actual leaver rate %"]])
with open("report/table_p_topdecile.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n & Top-risk decile & "
             "All teachers \\\\\n\\midrule\n")
    for _, r in D5.iterrows():
        lab = str(r["trait"]).replace("%", "\\%")
        if "leaver rate" in lab:
            fh.write(f"\\textbf{{{lab}}} & \\textbf{{{r['top decile']}}} & "
                     f"\\textbf{{{r['all teachers']}}} \\\\\n\\midrule\n")
        else:
            fh.write(f"{lab} & {r['top decile']} & {r['all teachers']} "
                     f"\\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# probit table relabeled
A = pd.read_csv("outputs/p_ame.csv")
NAMES = {"fullyear": "Worked full year (50+ weeks)",
         "new_baby": "New baby during the year",
         "parttime": "Part-time ($<$35 h/week)",
         "pension": "Enrolled in a pension plan", "black": "Black",
         "public": "Public school", "female": "Female",
         "sepdiv": "Separated or divorced", "A_AGE": "Age (per year)",
         "age2": "Age squared", "ma_plus": "Master's degree or higher",
         "married": "Married", "n_children": "Number of children",
         "child_u6": "Child under 6"}
with open("report/table_p_probit.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n & AME (pp) & SE \\\\\n"
             "\\midrule\n")
    for _, r in A.iterrows():
        dec = 3 if r["var"] == "age2" else 2
        fh.write(f"{NAMES.get(r['var'], r['var'])} & "
                 f"{r['AME_pp']:.{dec}f} & ({r['se_pp']:.{dec}f}) \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# robustness with (se) in cells
ROB = pd.read_csv("outputs/q_robustness.csv")
with open("report/table_q_robustness.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccccc}\n\\toprule\n & Full year & "
             "Part-time & Pension & New baby & Public & $n$ \\\\\n"
             "\\midrule\n")
    for _, r in ROB.iterrows():
        cells = []
        for v in ["fullyear", "parttime", "pension", "new_baby", "public"]:
            if pd.isna(r[v]):
                cells.append("--")
                continue
            star = "$^{*}$" if abs(r[v]) > 1.96 * r[v + "_se"] else ""
            cells.append(f"{r[v]:.2f}{star} ({r[v+'_se']:.2f})")
        fh.write(f"{r['specification']} & " + " & ".join(cells)
                 + f" & {int(r['n']):,} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")
print("\ntables regenerated")
