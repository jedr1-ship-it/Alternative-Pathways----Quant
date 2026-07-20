"""
The annual attrition series, computed exclusively from the master base.

  leaver_ba   full route-based definition, college graduates, weighted:
              tier A (cal 2010-2024) and upgraded tier B (cal 2005-2009,
              routes and weights from the March-monthly link).
  leaver_all  same definition, all education levels.
  leaver_oldstyle  occupation pairs only, unweighted, all education --
              the harmonized construction available in every year
              (cal 1997-2024, continuous).
Writes outputs/p_series.csv.
"""
import numpy as np
import pandas as pd

M = pd.read_parquet("data/processed/asec_master.parquet")
T = M[M["teacher"] == 1]

rows = []
for cy, g in T.groupby("cal_year"):
    tier = g["tier"].iloc[0]
    # harmonized old-style: occupation pair, unweighted (every tier)
    ay = int(g["asec_year"].iloc[0])
    from_codes = {155, 156, 157, 158, 159} if ay <= 2002 else \
        ({2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360}))
    olds = (~g["PEIOOCC"].isin(from_codes)).mean() * 100
    row = {"cal_year": int(cy), "tier": tier,
           "leaver_oldstyle": round(olds, 2), "n": len(g),
           "leaver_all": np.nan, "leaver_ba": np.nan, "se_ba": np.nan,
           "weighted": 0}
    full = g[g["leaver"].notna() & g["WGT"].notna()]
    if tier in ("A", "B") and len(full) > 500:
        row["leaver_all"] = round(np.average(full["leaver"],
                                             weights=full["WGT"]) * 100, 2)
        ba = full[(full["ba_plus"] == 1) & (full["A_AGE"] >= 18)]
        p = np.average(ba["leaver"], weights=ba["WGT"])
        row["leaver_ba"] = round(p * 100, 2)
        row["se_ba"] = round(np.sqrt(1.5 * p * (1 - p) / len(ba)) * 100, 2)
        row["weighted"] = 1
        for k, col in [("rate_switch", "switch"), ("rate_unemp", "unemp"),
                       ("rate_leftlf", "leftlf")]:
            row[k] = round(np.average(ba[col] == 1,
                                      weights=ba["WGT"]) * 100, 2)
    rows.append(row)
S = pd.DataFrame(rows).sort_values("cal_year")
S.to_csv("outputs/p_series.csv", index=False)
print(S.to_string(index=False))

# ---- route composition among BA+ leavers, per calendar year ----
L = M[(M["teacher"] == 1) & (M["ba_plus"] == 1) & (M["A_AGE"] >= 18)
      & (M["leaver"] == 1) & M["WGT"].notna()].copy()
L["route"] = np.select(
    [L["switch"] == 1, L["unemp"] == 1,
     (L["leftlf"] == 1) & (L["A_AGE"] >= 55),
     (L["leftlf"] == 1) & (L["A_AGE"] < 55)],
    ["employed", "unemployed", "outlf_55", "outlf_u55"], "other")
rr = []
for cy, g in L.groupby("cal_year"):
    tot = g["WGT"].sum()
    rr.append({"cal_year": int(cy), "n": len(g),
               **{rt: round(g.loc[g["route"] == rt, "WGT"].sum()
                            / tot * 100, 2)
                  for rt in ("employed", "outlf_55", "outlf_u55",
                             "unemployed")}})
R = pd.DataFrame(rr).sort_values("cal_year")
R.to_csv("outputs/p_routes.csv", index=False)
print("\nroute shares among leavers -> outputs/p_routes.csv")

# ---- public vs private: route rates, pooled 2015-2024 ----
P = M[(M["teacher"] == 1) & (M["ba_plus"] == 1) & (M["A_AGE"] >= 18)
      & M["cal_year"].between(2015, 2024) & M["WGT"].notna()
      & M["public_ly"].notna()]
sec_rows = []
for tag, g in [("public", P[P["public_ly"] == 1]),
               ("private", P[P["public_ly"] == 0])]:
    w = g["WGT"]
    sec_rows.append({
        "sector": tag, "n": len(g),
        "leaver": round(np.average(g["leaver"], weights=w) * 100, 2),
        "job": round(np.average(g["switch"] == 1, weights=w) * 100, 2),
        "unemp": round(np.average(g["unemp"] == 1, weights=w) * 100, 2),
        "outlf": round(np.average(g["leftlf"] == 1, weights=w) * 100, 2)})
pd.DataFrame(sec_rows).to_csv("outputs/p_sector_routes.csv", index=False)
print("sector route rates -> outputs/p_sector_routes.csv")

# ---- routes by age group, pooled 2015-2024 (weighted midpoints) ----
A = M[(M["teacher"] == 1) & (M["ba_plus"] == 1) & M["WGT"].notna()
      & M["cal_year"].between(2015, 2024) & M["A_AGE"].between(21, 80)]
age_rows = []
for a, b in [(21, 25), (26, 30), (31, 35), (36, 40), (41, 45), (46, 50),
             (51, 55), (56, 60), (61, 64), (65, 80)]:
    g = A[A["A_AGE"].between(a, b)]
    w = g["WGT"]
    age_rows.append({
        "age": f"{a}-{b}", "mid": round(np.average(g["A_AGE"],
                                                   weights=w), 2),
        "n": len(g),
        "switch": round(np.average(g["switch"] == 1, weights=w) * 100, 2),
        "unemp": round(np.average(g["unemp"] == 1, weights=w) * 100, 2),
        "leftlf": round(np.average(g["leftlf"] == 1, weights=w) * 100, 2),
        "total": round(np.average(g["leaver"], weights=w) * 100, 2)})
pd.DataFrame(age_rows).to_csv("outputs/p_routes_age.csv", index=False)
print("routes by age -> outputs/p_routes_age.csv")

# ---- annual occupational-leaving series for comparison professions ----
# (2000-census occupation codes: surveys 2003+, calendar 2002-2024)
def prof_codes(ay):
    """2002-census codes (surveys 2003-2010), 2010 codes (2011-2019),
    2018 codes (2020+). Teachers/accountants/lawyers/pharmacists are
    stable except the teacher n.e.c. bucket; the rest move."""
    rn = {3130} if ay <= 2010 else {3255, 3256, 3257, 3258}
    sw = {2010} if ay <= 2019 else {2011, 2012, 2013, 2014}
    md = {3060} if ay <= 2019 else {3090, 3100}
    pt = {3160} if ay <= 2019 else {3140}
    return {
        "Teachers": {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019
                                                else {2360}),
        "Registered nurses": rn,
        "Social workers": sw,
        "Accountants": {800},
        "Lawyers": {2100},
        "Physicians": md,
        "Pharmacists": {3050},
        "Physical therapists": pt,
    }


PLOT_PROFS = ["Teachers", "Registered nurses", "Social workers",
              "Accountants", "Lawyers"]


W2 = M[(M["ba_plus"] == 1) & (M["A_AGE"] >= 18) & M["WGT"].notna()
       & (M["asec_year"] >= 2003)]
prows = []
for ay, g in W2.groupby("asec_year"):
    emp = g["A_LFSR"].isin([1, 2])
    for prof, codes in prof_codes(int(ay)).items():
        b = g[g["OCCUP"].isin(codes)]
        if len(b) < 150:
            continue
        st = emp.loc[b.index] & b["PEIOOCC"].isin(codes)
        prows.append({"cal_year": int(ay) - 1, "prof": prof,
                      "n": len(b),
                      "leave": round(np.average(~st, weights=b["WGT"])
                                     * 100, 2)})
PS = pd.DataFrame(prows).sort_values(["prof", "cal_year"])
PS = PS[PS["prof"].isin(PLOT_PROFS)]
PS.to_csv("outputs/p_prof_series.csv", index=False)
print("profession series -> outputs/p_prof_series.csv")

# ---- two symmetric windows for the professions dumbbell (G7):
# surveys 2004-2014 and 2015-2025, eleven surveys each ----
wrows = []
for a, b, tag in [(2004, 2014, "2004-2014"), (2015, 2025, "2015-2025")]:
    Ww = W2[W2["asec_year"].between(a, b)]
    for ay, g in Ww.groupby("asec_year"):
        emp = g["A_LFSR"].isin([1, 2])
        for prof, codes in prof_codes(int(ay)).items():
            bb = g[g["OCCUP"].isin(codes)]
            if not len(bb):
                continue
            st = emp.loc[bb.index] & bb["PEIOOCC"].isin(codes)
            wrows.append({"window": tag, "prof": prof,
                          "w": bb["WGT"].sum(),
                          "wl": (bb["WGT"] * ~st).sum(), "n": len(bb)})
WD = pd.DataFrame(wrows).groupby(["window", "prof"]).sum().reset_index()
WD["leave"] = (WD["wl"] / WD["w"] * 100).round(2)
WD[["window", "prof", "leave", "n"]].to_csv(
    "outputs/p_prof_windows.csv", index=False)
print(WD[["window", "prof", "leave", "n"]].to_string(index=False))

# ---- real FTFY median earnings by profession: series and windows ----
import io as _io
import os as _os
import urllib.request as _ur
if not _os.path.exists("outputs/n_cpi.csv"):
    _raw = _ur.urlopen("https://fred.stlouisfed.org/graph/"
                       "fredgraph.csv?id=CPIAUCSL", timeout=60
                       ).read().decode()
    _c = pd.read_csv(_io.StringIO(_raw))
    _c["year"] = pd.to_datetime(_c["observation_date"]).dt.year
    _c = _c.groupby("year")["CPIAUCSL"].mean().reset_index()
    _c["source"] = "BLS CPI-U via FRED CPIAUCSL, annual average"
    _c.to_csv("outputs/n_cpi.csv", index=False)
CPI = pd.read_csv("outputs/n_cpi.csv").set_index("year")["CPIAUCSL"]
DEFL = (CPI.loc[2024] / CPI).to_dict()

PAY = M[(M["ba_plus"] == 1) & M["A_AGE"].between(25, 60)
        & M["WGT"].notna() & (M["WSAL_VAL"] > 0)
        & (M["fullyear"] == 1) & (M["parttime_ly"] == 0)
        & (M["asec_year"] >= 2003)]


def _wmed(d):
    s = d.sort_values("WSAL_VAL")
    cw = s["WGT"].cumsum() / s["WGT"].sum()
    return s.loc[cw >= 0.5, "WSAL_VAL"].iloc[0]


prow, wrow = [], []
for ay, g in PAY.groupby("asec_year"):
    cy = int(ay) - 1
    groups = {"All college graduates": g}
    for prof, codes in prof_codes(int(ay)).items():
        groups[prof] = g[g["OCCUP"].isin(codes)]
    for prof, b in groups.items():
        if len(b) < 100:
            continue
        prow.append({"cal_year": cy, "prof": prof, "n": len(b),
                     "real_med": round(_wmed(b) * DEFL[cy])})
pd.DataFrame(prow).to_csv("outputs/p_pay_profs.csv", index=False)
PAY = PAY.copy()
PAY["real"] = PAY["WSAL_VAL"] * (PAY["asec_year"] - 1).map(DEFL)
for a, b, tag in [(2004, 2014, "2004-2014"), (2015, 2025, "2015-2025")]:
    Ww = PAY[PAY["asec_year"].between(a, b)]
    groups = {"All college graduates": Ww}
    parts = {p: [] for p in prof_codes(2015)}
    for ay, g in Ww.groupby("asec_year"):
        for prof, codes in prof_codes(int(ay)).items():
            parts[prof].append(g[g["OCCUP"].isin(codes)])
    groups.update({p: pd.concat(v) for p, v in parts.items()})
    for prof, d in groups.items():
        s = d.sort_values("real")
        cw = s["WGT"].cumsum() / s["WGT"].sum()
        wrow.append({"window": tag, "prof": prof, "n": len(d),
                     "real_med_k": round(
                         s.loc[cw >= 0.5, "real"].iloc[0] / 1000, 1)})
pd.DataFrame(wrow).to_csv("outputs/p_pay_windows.csv", index=False)
print("pay series/windows -> p_pay_profs.csv, p_pay_windows.csv")

# ---- linked March-to-March earnings changes (micro, for the density
# figure): teachers BA+ linked to their next-March record ----
TL = M[(M["teacher"] == 1) & (M["ba_plus"] == 1)
       & M["PERIDNUM"].notna() & (M["PERIDNUM"] != "")]
mlink = []
for ay in range(2011, 2025):
    t0 = TL[TL["asec_year"] == ay]
    b = M[M["asec_year"] == ay + 1][["PERIDNUM", "WSAL_VAL", "female",
                                     "A_AGE"]]
    mm = t0.merge(b, on="PERIDNUM", suffixes=("", "_1"))
    mm = mm[(mm["female"] == mm["female_1"])
            & (mm["A_AGE_1"] - mm["A_AGE"]).between(0, 2)]
    mlink.append(mm)
LKm = pd.concat(mlink, ignore_index=True)
LKm = LKm[LKm["WSAL_VAL"] > 0]
LKm["dlog"] = np.where(
    LKm["WSAL_VAL_1"] > 0,
    (np.log(LKm["WSAL_VAL_1"]) - np.log(LKm["WSAL_VAL"])) * 100, np.nan)
out_m = pd.concat([
    pd.DataFrame({"group": "stayer",
                  "dlog": LKm.loc[(LKm["leaver"] == 0)
                                  & LKm["dlog"].notna(), "dlog"]}),
    pd.DataFrame({"group": "leaver_employed",
                  "dlog": LKm.loc[(LKm["switch"] == 1)
                                  & LKm["dlog"].notna(), "dlog"]})])
out_m.round(2).to_csv("outputs/p_dlog_micro.csv", index=False)
print(f"dlog micro -> p_dlog_micro.csv "
      f"({(out_m['group'] == 'stayer').sum()} stayers, "
      f"{(out_m['group'] == 'leaver_employed').sum()} leavers)")
