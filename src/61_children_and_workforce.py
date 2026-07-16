"""
From the master base only. (1) Is the 24 (out of the labor force, under
55, per 100 leavers) about children? Composition of that group, pooled
2015-2024, plus its evolution 2010-2024 for the one fundamental change.
(2) Rebuild the workforce-composition series from the master so Figure 1
starts in calendar 2005 (tier B carries demographics via the March
monthly link; last-year job detail exists only from 2010).
"""
import numpy as np
import pandas as pd

M = pd.read_parquet("data/processed/asec_master.parquet")


def wavg(d, col, w="WGT"):
    v = d[col].astype(float)
    ok = v.notna() & d[w].notna()
    return np.average(v[ok], weights=d.loc[ok, w]) if ok.any() else np.nan


# ---------- (1) the 24: out of LF, under 55 ----------
TA = M[(M["tier"] == "A") & (M["teacher"] == 1) & (M["ba_plus"] == 1)
       & (M["A_AGE"] >= 18)]
win = TA[TA["cal_year"].between(2015, 2024)]
grp = win[(win["leftlf"] == 1) & (win["A_AGE"] < 55)]
print(f"out-of-LF-under-55 leavers, 2015-2024: n={len(grp)}")
stats = {
    "share_female_%": wavg(grp, "female") * 100,
    "mean_age": wavg(grp, "A_AGE"),
    "share_child_u6_%": wavg(grp, "child_u6") * 100,
    "share_new_baby_%": wavg(grp, "new_baby") * 100,
    "share_any_children_%": wavg(grp, "n_children"
                                 ).__class__ and np.average(
        (grp["n_children"] > 0), weights=grp["WGT"]) * 100,
    "share_married_%": wavg(grp, "married") * 100,
}
for k, v in stats.items():
    print(f"  {k}: {v:.1f}")
# same shares among STAYERS of the same ages, for contrast
st = win[(win["leaver"] == 0) & (win["A_AGE"] < 55)]
print(f"  [stayers <55: child_u6 {wavg(st,'child_u6')*100:.1f}%, "
      f"new_baby {wavg(st,'new_baby')*100:.1f}%]")
pd.Series(stats).round(1).to_csv("outputs/w_outlf_young.csv")

# evolution: what has changed inside this group, 2010-2024
rows = []
for cy, g in TA.groupby("cal_year"):
    gg = g[(g["leftlf"] == 1) & (g["A_AGE"] < 55)]
    if len(gg) < 30:
        continue
    rows.append({"cal_year": int(cy),
                 "child_u6": round(wavg(gg, "child_u6") * 100, 1),
                 "new_baby": round(wavg(gg, "new_baby") * 100, 1),
                 "any_children": round(np.average(gg["n_children"] > 0,
                                                  weights=gg["WGT"]) * 100,
                                       1),
                 "mean_age": round(wavg(gg, "A_AGE"), 1),
                 "n": len(gg)})
EV = pd.DataFrame(rows)
EV.to_csv("outputs/w_outlf_young_evolution.csv", index=False)
print("\nevolution of the young out-of-LF leavers:")
print(EV.to_string(index=False))

# ---------- (2) workforce composition from the master, 2005-2024 ----------
T = M[(M["teacher"] == 1) & (M["ba_plus"] == 1) & (M["A_AGE"] >= 18)
      & M["tier"].isin(["A", "B"])].copy()
# tier B pension from the calibrated old-layout files (asec_jobs_{yy})
jobs = pd.concat([pd.read_parquet(f"data/raw/asec/asec_jobs_{y}.parquet")
                  for y in ("06", "07", "08", "09", "10")])
jobs = jobs[jobs["PENPLAN"].isin([1, 2])]
pen_of = dict(zip(jobs["asec_year"].astype(str) + jobs["PERIDNUM"],
                  (jobs["PENPLAN"] == 1).astype(float)))
isB = T["tier"] == "B"
T.loc[isB, "pension"] = (T.loc[isB, "asec_year"].astype(int).astype(str)
                         + T.loc[isB, "PERIDNUM"]).map(pen_of)
comp = []
for cy, g in T.groupby("cal_year"):
    comp.append({
        "cal_year": int(cy),
        "female": round(wavg(g, "female") * 100, 1),
        "age": round(wavg(g, "A_AGE"), 1),
        "ma_plus": round(wavg(g, "ma_plus") * 100, 1),
        "black": round(wavg(g, "black") * 100, 1),
        "child_u6": round(wavg(g, "child_u6") * 100, 1),
        "married": round(wavg(g, "married") * 100, 1),
        "public": round(wavg(g, "public_ly") * 100, 1)
        if g["public_ly"].notna().any() else
        round(wavg(g[g["leaver"] == 0], "cur_public") * 100, 1),
        "parttime": round(wavg(g, "parttime_ly") * 100, 1)
        if g["parttime_ly"].notna().any() else
        round(wavg(g[g["leaver"] == 0], "cur_parttime") * 100, 1),
        "pension": round(wavg(g, "pension") * 100, 1),
        "n": len(g)})
WF = pd.DataFrame(comp).sort_values("cal_year")
WF.to_csv("outputs/p_workforce.csv", index=False)
print("\nworkforce series 2005-2024 (from the master):")
print(WF.to_string(index=False))
