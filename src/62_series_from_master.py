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
