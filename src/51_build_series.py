"""
Rebuild the long annual leaver series, calendar 1999-2024, from every
extraction tier: calibrated 1990s-layout files (surveys 2000-2005),
calibrated 2006-2010 files, and the rich 2011-2025 files. Pre-2010
segments are all-education and unweighted (the old layouts do not yield
validated weights); 2010 onward is weighted with the college-graduate
main definition alongside. Writes outputs/p_series.csv.
"""
import glob
import numpy as np
import pandas as pd

RAW = "data/raw/asec"
CORE = {2300, 2310, 2320, 2330}
T90 = {155, 156, 157, 158, 159}


def codes(ay):
    if ay <= 2002:
        return T90
    return CORE | ({2340} if ay <= 2019 else {2360})


rows = []
for f in sorted(glob.glob(f"{RAW}/asec_90s_*.parquet")):
    d = pd.read_parquet(f)
    ay = int(d["asec_year"].iloc[0])
    cs = codes(ay)
    b = d[d["OCCUP"].isin(cs)]
    rows.append({"cal_year": ay - 1,
                 "leaver_all": round((~b["PEIOOCC"].isin(cs)).mean() * 100, 2),
                 "leaver_ba": np.nan, "n": len(b), "weighted": 0})
for yy in ("06", "07", "08", "09", "10"):
    d = pd.read_parquet(f"{RAW}/asec_id_{yy}.parquet")
    for c in ("OCCUP", "PEIOOCC"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    cs = CORE | {2340}
    b = d[d["OCCUP"].isin(cs)]
    rows.append({"cal_year": 2000 + int(yy) - 1,
                 "leaver_all": round((~b["PEIOOCC"].isin(cs)).mean() * 100, 2),
                 "leaver_ba": np.nan, "n": len(b), "weighted": 0})
R = pd.concat([pd.read_parquet(f) for f in
               sorted(glob.glob(f"{RAW}/asec_rich_*.parquet"))],
              ignore_index=True)
for c in ("OCCUP", "PEIOOCC", "A_LFSR", "A_HGA", "A_AGE", "MARSUPWT"):
    R[c] = pd.to_numeric(R[c], errors="coerce")
for ay, g in R.groupby("asec_year"):
    cs = codes(int(ay))
    b = g[g["OCCUP"].isin(cs)].copy()
    emp = b["A_LFSR"].isin([1, 2])
    b["leaver"] = (~(emp & b["PEIOOCC"].isin(cs))).astype(int)
    ba = b[(b["A_HGA"] >= 43) & (b["A_AGE"] >= 18)]
    rows.append({"cal_year": int(ay) - 1,
                 "leaver_all": round(np.average(b["leaver"],
                                                weights=b["MARSUPWT"]) * 100, 2),
                 "leaver_ba": round(np.average(ba["leaver"],
                                               weights=ba["MARSUPWT"]) * 100, 2),
                 "n": len(b), "weighted": 1})
S = pd.DataFrame(rows).sort_values("cal_year")
S.to_csv("outputs/p_series.csv", index=False)
print(S.to_string(index=False))
