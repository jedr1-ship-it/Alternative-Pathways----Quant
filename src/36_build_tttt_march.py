"""
Build the requested person-level database.

One row per person who is a teacher in ALL FOUR of their first interviews
(TTTT over MIS 1-4). Columns:

  MARZO         1 if March is among their four MIS 1-4 months, else 0
  leaver        1 if in the last four interviews (MIS 5-8) they are teacher
                in NONE of them (NT-NT-NT-NT); 0 if they teach in some;
                NA if the post spell is not fully observed
  leaver_MARCH  from the ASEC of the last observed year (2024), using the
                retrospective question:
                   1  OCCUP(last year)=teacher AND now not teaching  (left)
                   0  OCCUP=teacher AND still teaching                (stayed)
                  -1  OCCUP is not even a teaching occupation
                (NA if MARZO=0 -- no March questionnaire for that person)

Then compares leaver vs leaver_MARCH: how many -1, and how much they agree,
to say whether the March retrospective under- or over-estimates leaving.
"""
import glob
import numpy as np
import pandas as pd

CORE = {2300, 2310, 2320, 2330}
RAW = "data/raw/cps"

d = pd.concat([pd.read_parquet(f) for f in
               sorted(glob.glob(f"{RAW}/slim_20??_??.parquet"))],
              ignore_index=True)
emp = d["PEMLR"].isin([1, 2])
d["st"] = np.where(emp & d["PTIO1OCD"].isin(CORE), "T",
          np.where(emp, "E", np.where(d["PEMLR"].isin([3, 4]), "U", "N")))

# pivot status and month by month-in-sample
st = d.pivot_table(index="PERIDNUM", columns="HRMIS", values="st",
                   aggfunc="first")
mo = d.pivot_table(index="PERIDNUM", columns="HRMONTH", values="HRMIS",
                   aggfunc="count")  # placeholder, not used
# month of each MIS interview
mm = d.pivot_table(index="PERIDNUM", columns="HRMIS", values="HRMONTH",
                   aggfunc="first")

st = st.reindex(columns=range(1, 9))
pre = st[[1, 2, 3, 4]]
post = st[[5, 6, 7, 8]]

# TTTT: teacher in all four first interviews (all observed and == 'T')
tttt = (pre == "T").all(axis=1) & pre.notna().all(axis=1)
db = pd.DataFrame(index=st.index)
db["MARZO"] = ((mm[[1, 2, 3, 4]] == 3).any(axis=1)).astype(int)
post_obs = post.notna().sum(axis=1)
never_teach = (post != "T").all(axis=1)          # NT in every observed post
db["leaver"] = np.where(post_obs == 4, never_teach.astype(int), np.nan)
db = db[tttt].copy()
print(f"personas TTTT (profe en los 4 primeros meses): {len(db):,}")
print(f"  con MARZO en su ventana: {int(db['MARZO'].sum()):,} "
      f"({db['MARZO'].mean()*100:.1f}%)")
print(f"  con post completo (4 meses) para definir leaver: "
      f"{int((db['leaver'].notna()).sum()):,}")

# link the MARCH people to the ASEC 2024 retrospective
asec = pd.read_parquet("data/raw/asec/asec_id_24.parquet")[
    ["PERIDNUM", "OCCUP", "PEIOOCC"]]
db = db.reset_index().merge(asec, on="PERIDNUM", how="left")
has_asec = db["OCCUP"].notna()
occ_t = db["OCCUP"].isin(CORE)
now_t = db["PEIOOCC"].isin(CORE)
db["leaver_MARCH"] = np.where(~occ_t, -1, np.where(now_t, 0, 1))
db.loc[~has_asec, "leaver_MARCH"] = np.nan   # not linked to ASEC
db.loc[db["MARZO"] == 0, "leaver_MARCH"] = np.nan

db.to_csv("outputs/tttt_march_database.csv", index=False)
print(f"\nescrito outputs/tttt_march_database.csv  ({len(db):,} filas)")

# --- the comparison the user wants, on TTTT people with March + ASEC + post ---
c = db[(db["MARZO"] == 1) & has_asec & db["leaver"].notna()].copy()
print(f"\n=== comparacion (TTTT, MARZO=1, enlazados a ASEC, post completo): "
      f"n={len(c)} ===")
print("leaver_MARCH values:")
print(c["leaver_MARCH"].value_counts().sort_index().to_string())
n_m1 = int((c["leaver_MARCH"] == -1).sum())
print(f"\n-1 (la retrospectiva ni los ve como docentes): {n_m1} "
      f"({n_m1/len(c)*100:.0f}%)")
print("\ncruce leaver (nuestro) x leaver_MARCH:")
print(pd.crosstab(c["leaver"], c["leaver_MARCH"], margins=True).to_string())
# agreement excluding -1
cc = c[c["leaver_MARCH"] >= 0]
agree = (cc["leaver"] == cc["leaver_MARCH"]).mean() * 100
print(f"\nacuerdo leaver==leaver_MARCH (excluyendo -1): {agree:.0f}%  "
      f"(n={len(cc)})")
print(f"tasa leaver NUESTRA: {c['leaver'].mean()*100:.1f}%  |  "
      f"tasa leaver MARZO (excl -1): {cc['leaver_MARCH'].mean()*100:.1f}%")
