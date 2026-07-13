"""
Evolution of teacher attrition 2005-2024 and short-run return to teaching,
overall and by gender. Produces fig6 (two panels) + CSV.

Return measure: a leaver observed out of teaching at t+12 (MIS 5-7) is
re-observed in up to three following monthly interviews (until MIS 8);
'returns' = teaching again in any of them. The CPS rotation design caps the
observable return window at ~3 months, so this is short-run churn, not
lifetime re-entry. Leavers with MIS 8 at t+12 have no follow-up and are
excluded from the return denominator.
"""
import glob
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from paperstyle import *

INTDIR = "data/interim"
TEACHER_OCC = {2300, 2310, 2320, 2330}
KEY = ["HRHHID", "HRHHID2", "PULINENO"]

df = pd.read_csv("data/processed/cps_teacher_panel.csv",
                 dtype={"HRHHID": str, "HRHHID2": str})
# analytic universe: full-time elementary-through-secondary teachers, the
# same restriction load_panel() applies for every other figure
df = df[df["PTIO1OCD_0"].isin([2310, 2320, 2330])
        & ~df["PEHRUSL1_0"].between(1, 34)]
df["female"] = (df["PESEX_0"] == 2).astype(int)
w = "PWSSWGT_0"

# ---------- follow-up teacher status for leavers ----------
lv = df[(df["leaver"] == 1) & (df["HRMIS_1"] < 8)].copy()
lv["fid"] = np.arange(len(lv))

# expected follow-up (year, month, mis) rows for each leaver
rows = []
for k in range(1, 4):
    e = lv[lv["HRMIS_1"] + k <= 8][
        ["fid"] + KEY + ["HRMONTH", "base_year", "HRMIS_1"]].copy()
    if e.empty:
        continue
    mo = e["HRMONTH"] + k
    e["HRYEAR4"] = e["base_year"] + 1 + (mo > 12).astype(int)
    e["HRMONTH"] = np.where(mo > 12, mo - 12, mo)
    e["HRMIS"] = e["HRMIS_1"] + k
    rows.append(e.drop(columns=["base_year", "HRMIS_1"]))
exp = pd.concat(rows, ignore_index=True)

# teacher status lookup for the needed months (MIS 6-8 only)
need = exp[["HRYEAR4", "HRMONTH"]].drop_duplicates()
frames = []
for _, (yr, mo) in need.iterrows():
    fs = glob.glob(f"{INTDIR}/cps_{yr}{mo:02d}.parquet")
    if not fs:
        continue
    d = pd.read_parquet(
        fs[0], columns=KEY + ["HRYEAR4", "HRMONTH", "HRMIS", "PEMLR",
                              "PTIO1OCD", "PESEX"])
    d = d[d["HRMIS"].between(6, 8)]
    d["tch"] = (d["PEMLR"].isin([1, 2])
                & d["PTIO1OCD"].isin(TEACHER_OCC)).astype(int)
    frames.append(d[KEY + ["HRYEAR4", "HRMONTH", "HRMIS", "tch", "PESEX"]])
look = pd.concat(frames, ignore_index=True)

m = exp.merge(look, on=KEY + ["HRYEAR4", "HRMONTH", "HRMIS"], how="inner")
# guard against household churn: same sex as at baseline
m = m.merge(lv[["fid", "PESEX_0"]], on="fid")
m = m[m["PESEX"] == m["PESEX_0"]]
obs = m.groupby("fid").agg(n_obs=("tch", "size"), returned=("tch", "max"))
lv = lv.merge(obs, on="fid", how="left")
lv_obs = lv[lv["n_obs"].notna()].copy()   # at least one observed follow-up

# ---------- export return flags for the model scripts ----------
ret = lv[KEY + ["HRMONTH", "base_year", "n_obs", "returned"]].copy()
ret.to_csv("data/processed/cps_returns.csv", index=False)

print(f"leavers total                    : {(df['leaver']==1).sum():,}")
print(f"leavers with observed follow-up  : {len(lv_obs):,}")
ret_w = np.average(lv_obs["returned"], weights=lv_obs[w])
print(f"return to teaching (<=3 months)  : {ret_w:6.2%}")
for g, name in [(1, "women"), (0, "men")]:
    s = lv_obs[lv_obs["female"] == g]
    print(f"  {name:6s}: {np.average(s['returned'], weights=s[w]):6.2%}")

# ---------- persistent-leaver (definition B) on the MIS 1-3 subsample ----------
ret_all = df.merge(lv[KEY + ["HRMONTH", "base_year", "returned"]],
                   on=KEY + ["HRMONTH", "base_year"], how="left")
B = ret_all[ret_all["HRMIS_0"] <= 3].copy()
B["leaver_p"] = ((B["leaver"] == 1)
                 & (B["returned"].fillna(0) == 0)).astype(int)
print(f"\nsample B (baseline MIS 1-3)      : {len(B):,}")
print(f"persistent attrition (weighted)  : "
      f"{np.average(B['leaver_p'], weights=B[w]):6.2%}")
print(f"12-month attrition, same sample  : "
      f"{np.average(B['leaver'], weights=B[w]):6.2%}")

# ---------- yearly series ----------
def wavg(d, col):
    return np.average(d[col], weights=d[w]) * 100

years = sorted(df["base_year"].unique())
ev = []
for y in years:
    dy, by = df[df["base_year"] == y], B[B["base_year"] == y]
    ly = lv_obs[lv_obs["base_year"] == y]
    ev.append({
        "base_year": y,
        "attr12_all": wavg(dy, "leaver"),
        "attrp_all": wavg(by, "leaver_p"),
        "attrp_f": wavg(by[by.female == 1], "leaver_p"),
        "attrp_m": wavg(by[by.female == 0], "leaver_p"),
        "ret_all": wavg(ly, "returned"),
        "ret_f": wavg(ly[ly.female == 1], "returned"),
        "ret_m": wavg(ly[ly.female == 0], "returned"),
        "n": len(dy), "nB": len(by), "n_lv_obs": len(ly),
    })
ev = pd.DataFrame(ev)
ev.round(2).to_csv("outputs/evolution_by_year_gender.csv", index=False)
print("\n", ev.round(1).to_string(index=False))

# ---------- figure: the headline series, all teachers -----------------------
# one hero line, the overall non-returning rate, so the reader sees exactly
# where the 13 percent headline comes from: the average of a rising line
pooled = np.average(B["leaver_p"], weights=B[w]) * 100
fig, ax = plt.subplots(figsize=(6.9, 3.4))
ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
ax.axhline(pooled, color=GRAY, lw=1.3, ls=(0, (5, 4)), zorder=1)
ax.text(2004.7, pooled + 0.5,
        f"2005--2025 average, {pooled:.0f}\\%".replace("\\%", "%"),
        fontsize=9, color=GRAY)
ax.plot(ev.base_year, ev.attrp_all, color=BLUE, lw=2.6,
        solid_capstyle="round", zorder=3)
for yy, lab, dy in [(0, "", 0), (len(ev) - 1, "", 0)]:
    ax.scatter([ev.base_year.iloc[yy]], [ev.attrp_all.iloc[yy]], s=44,
               color=BLUE, zorder=4, edgecolor=SURFACE, linewidth=2)
ax.text(ev.base_year.iloc[0] + 0.3, ev.attrp_all.iloc[0] - 1.1,
        f"{ev.attrp_all.iloc[0]:.0f}%", fontsize=9.5, color=INK,
        fontweight="bold", ha="center")
ax.text(ev.base_year.iloc[-1] + 0.4, ev.attrp_all.iloc[-1],
        f"{ev.attrp_all.iloc[-1]:.0f}%", va="center", fontsize=9.5,
        color=INK, fontweight="bold")
ax.set_xlim(2004.5, 2026.5)
ax.set_ylim(0, 18)
ax.set_xticks([2005, 2010, 2015, 2020, 2024])
ax.set_ylabel("Left teaching, no return, % per year")
ax.text(2020, 16.6, "COVID", ha="center", fontsize=8, color=SUBTLE)
fig.tight_layout()
fig.savefig("report/figures/fig6_evolution.pdf", bbox_inches="tight")
print(f"\npooled non-returning (headline): {pooled:.1f}")
print(f"2005 {ev.attrp_all.iloc[0]:.1f}  2024 {ev.attrp_all.iloc[-1]:.1f}")
print("saved report/figures/fig6_evolution.pdf, outputs/evolution_by_year_gender.csv")
