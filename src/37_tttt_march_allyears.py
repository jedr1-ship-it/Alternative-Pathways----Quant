"""
Replicate the TTTT vs March-retrospective confusion table for every cohort
year with ASEC PERIDNUM coverage (entry cohorts 2018-2024, ASEC 2019-2025).

Per cohort year Y: follow persons whose MIS 1-4 fall in Y (entry Jan-Aug)
and MIS 5-8 in Y+1, from the slim basic monthly files. Keep TTTT teachers
(K-12 core codes 2300/2310/2320/2330, employed). Columns per person:

  MARZO         1 if March(Y) is among the four pre months
  leaver        1 if NT in all four post months (NA if post incomplete)
  leaver_MARCH  from ASEC Y+1 retrospective: 1 left / 0 stayed /
                -1 not counted as a teacher last year (NA if no March/link)

Outputs the per-year table and the pooled one.
"""
import glob
import os
import numpy as np
import pandas as pd

CORE = {2300, 2310, 2320, 2330}
RAW = "data/raw/cps"


def load_months(year):
    fs = sorted(glob.glob(f"{RAW}/slim_{year}_??.parquet"))
    return pd.concat([pd.read_parquet(f) for f in fs], ignore_index=True)


def build_cohort(y):
    d = pd.concat([load_months(y), load_months(y + 1)], ignore_index=True)
    emp = d["PEMLR"].isin([1, 2])
    d["is_t"] = (emp & d["PTIO1OCD"].isin(CORE))
    # keep persons whose MIS1 happens in year y (entry cohort of y)
    first = d[(d["HRMIS"] == 1) & (d["HRYEAR4"] == y)][["PERIDNUM"]]
    d = d.merge(first.drop_duplicates(), on="PERIDNUM")
    st = d.pivot_table(index="PERIDNUM", columns="HRMIS", values="is_t",
                       aggfunc="first")
    mm = d.pivot_table(index="PERIDNUM", columns="HRMIS", values="HRMONTH",
                       aggfunc="first")
    st = st.reindex(columns=range(1, 9))
    mm = mm.reindex(columns=range(1, 9))
    pre, post = st[[1, 2, 3, 4]], st[[5, 6, 7, 8]]
    tttt = pre.notna().all(axis=1) & (pre == True).all(axis=1)  # noqa: E712
    db = pd.DataFrame(index=st.index[tttt])
    db["cohort"] = y
    db["MARZO"] = (mm.loc[db.index, [1, 2, 3, 4]] == 3).any(axis=1).astype(int)
    p = post.loc[db.index]
    obs = p.notna().sum(axis=1)
    db["leaver"] = np.where(obs == 4, (p != True).all(axis=1).astype(float),  # noqa: E712
                            np.nan)
    # link to ASEC of Y+1
    yy = str(y + 1)[2:]
    asec = pd.read_parquet(f"data/raw/asec/asec_id_{yy}.parquet")[
        ["PERIDNUM", "OCCUP", "PEIOOCC"]]
    db = db.reset_index().merge(asec, on="PERIDNUM", how="left")
    occ_t = db["OCCUP"].isin(CORE)
    now_t = db["PEIOOCC"].isin(CORE)
    db["leaver_MARCH"] = np.where(~occ_t, -1, np.where(now_t, 0, 1)).astype(float)
    db.loc[db["OCCUP"].isna() | (db["MARZO"] == 0), "leaver_MARCH"] = np.nan
    return db


all_db = []
print(f"{'cohorte':>7s} {'TTTT':>6s} {'MARZO':>6s} {'comparables':>11s} "
      f"{'-1':>4s} {'acuerdo(excl -1)':>16s} {'lv_our':>7s} {'lv_MAR':>7s}")
for y in range(2018, 2025):
    if not glob.glob(f"{RAW}/slim_{y}_01.parquet"):
        print(f"{y:7d}  (sin ficheros mensuales, salto)")
        continue
    db = build_cohort(y)
    all_db.append(db)
    c = db[(db["MARZO"] == 1) & db["leaver"].notna()
           & db["leaver_MARCH"].notna()]
    cc = c[c["leaver_MARCH"] >= 0]
    agree = (cc["leaver"] == cc["leaver_MARCH"]).mean() * 100 if len(cc) else np.nan
    n1 = int((c["leaver_MARCH"] == -1).sum())
    print(f"{y:7d} {len(db):6,d} {int(db['MARZO'].sum()):6,d} {len(c):11,d} "
          f"{n1:4d} {agree:15.0f}% {c['leaver'].mean()*100:6.1f}% "
          f"{cc['leaver_MARCH'].mean()*100 if len(cc) else np.nan:6.1f}%")

DB = pd.concat(all_db, ignore_index=True)
DB.to_csv("outputs/tttt_march_allyears.csv", index=False)
C = DB[(DB["MARZO"] == 1) & DB["leaver"].notna() & DB["leaver_MARCH"].notna()]
print(f"\n=== POOLED cohortes 2018-2024: comparables n={len(C)} ===")
print(pd.crosstab(C["leaver"], C["leaver_MARCH"], margins=True).to_string())
CC = C[C["leaver_MARCH"] >= 0]
print(f"\nacuerdo (excl -1): {(CC['leaver']==CC['leaver_MARCH']).mean()*100:.1f}%"
      f"   -1: {int((C['leaver_MARCH']==-1).sum())} "
      f"({(C['leaver_MARCH']==-1).mean()*100:.0f}%)")
print(f"tasa leaver nuestra: {C['leaver'].mean()*100:.1f}%  |  "
      f"tasa leaver MARZO (excl -1): {CC['leaver_MARCH'].mean()*100:.1f}%")
# de los -1, cuantos son leavers nuestros y su OCCUP
m1 = C[C["leaver_MARCH"] == -1]
print(f"\nde los -1: leavers nuestros {int(m1['leaver'].sum())} / {len(m1)}; "
      f"top OCCUP:")
print(m1[m1["OCCUP"] > 0]["OCCUP"].astype(int).value_counts().head(8).to_string())
