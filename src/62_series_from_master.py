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
