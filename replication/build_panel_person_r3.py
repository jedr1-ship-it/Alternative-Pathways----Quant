"""Rule R3 — one teacher, one verdict, from the CPS monthly panel.

The unit is the person-rotation: the up-to-8 interviews (4-8-4 design) of
one person at one address, grouped by (HRHHID, HRHHID2, PULINENO) and the
rotation's starting month implied by (year, month, MIS). Demographic
validation within the group follows Madrian-Lefgren: constant sex and race,
age advancing at most 2 years.

  Teacher : seen teaching (employed, occ 2300/2310/2320/2330, BA+) in at
            least one first-year interview (MIS 1-4).
  Stayer  : seen teaching in at least one second-year interview (MIS 5-8).
  Leaver  : observed in the second year and never seen teaching there.
  Persons with no second-year interview are unclassifiable and dropped.

Each person counts exactly once, weighted by PWSSWGT at their first
first-year teaching interview; base_year is that interview's year.
Writes outputs/panel_person_r3.csv (annual series) and prints the rates.
"""
import glob
import numpy as np
import pandas as pd

INTDIR = "data/interim"
TEACHER_OCC = {2300, 2310, 2320, 2330}
USE = ["HRHHID", "HRHHID2", "PULINENO", "HRMIS", "HRYEAR4", "HRMONTH",
       "PESEX", "PTDTRACE", "PRTAGE", "PEEDUCA", "PEMLR", "PTIO1OCD", "PWSSWGT"]

files = sorted(glob.glob(f"{INTDIR}/cps_??????.parquet"))
assert files, "run replication/build_cps_monthly.py first"

# ---- pass 1: rotation keys of everyone ever seen teaching (BA+) ----
def add_keys(d):
    d = d[d["HRMIS"].between(1, 8) & d["PULINENO"].notna()].copy()
    idx = d["HRYEAR4"] * 12 + d["HRMONTH"]
    d["start"] = (idx - (d["HRMIS"] - 1) - 8 * (d["HRMIS"] >= 5)).astype("Int32")
    d["pkey"] = (d["HRHHID"].astype(str) + "|" + d["HRHHID2"].astype(str) + "|"
                 + d["PULINENO"].astype(str) + "|" + d["start"].astype(str))
    return d

teach_keys = set()
for f in files:
    d = add_keys(pd.read_parquet(f, columns=USE))
    t = d[d["PEMLR"].isin([1, 2]) & d["PTIO1OCD"].isin(TEACHER_OCC)
          & (d["PEEDUCA"] >= 43) & (d["HRMIS"] <= 4)]
    teach_keys.update(t["pkey"])
print(f"pass 1: {len(teach_keys):,} person-rotations seen teaching (BA+, MIS 1-4)", flush=True)

# ---- pass 2: gather every interview of those persons ----
parts = []
for f in files:
    d = add_keys(pd.read_parquet(f, columns=USE))
    parts.append(d[d["pkey"].isin(teach_keys)])
R = pd.concat(parts, ignore_index=True)
R["teaching"] = (R["PEMLR"].isin([1, 2]) & R["PTIO1OCD"].isin(TEACHER_OCC)).astype(int)
print(f"pass 2: {len(R):,} interviews of those persons", flush=True)

# ---- demographic validation within the rotation (Madrian-Lefgren) ----
g = R.groupby("pkey")
ok = (g["PESEX"].nunique() == 1) & (g["PTDTRACE"].nunique() == 1) \
     & ((g["PRTAGE"].max() - g["PRTAGE"].min()) <= 2)
R = R[R["pkey"].map(ok)]
print(f"validated: {R['pkey'].nunique():,} person-rotations", flush=True)

# ---- classify: one person, one verdict ----
y1 = R[R["HRMIS"] <= 4]
y2 = R[R["HRMIS"] >= 5]
first_teach = (y1[y1["teaching"] == 1].sort_values(["HRYEAR4", "HRMONTH"])
               .drop_duplicates("pkey"))
has_y2 = y2.groupby("pkey").size()
stay = y2.groupby("pkey")["teaching"].max()

P = first_teach.set_index("pkey")[["HRYEAR4", "PWSSWGT"]].copy()
P["observed_y2"] = P.index.isin(has_y2.index)
P = P[P["observed_y2"]]
P["stayer"] = stay.reindex(P.index).fillna(0).astype(int)
P["leaver"] = 1 - P["stayer"]

w = P["PWSSWGT"].astype(float)
rate = np.average(P["leaver"], weights=w) * 100
print(f"\nR3 person-level sample      : {len(P):,} teachers")
print(f"R3 leaving rate (weighted)  : {rate:.2f}%")

ann = (P.groupby("HRYEAR4")
        .apply(lambda d: pd.Series({
            "n": len(d),
            "leaver_r3": np.average(d["leaver"], weights=d["PWSSWGT"]) * 100}),
            include_groups=False)
        .reset_index().rename(columns={"HRYEAR4": "base_year"}))
ann.to_csv("outputs/panel_person_r3.csv", index=False)
print(ann.round(2).to_string(index=False))
