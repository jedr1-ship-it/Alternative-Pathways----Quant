"""Every combination of the two stringency axes of the panel
definition, pooled 2005-2024: how much teaching is required in year 1
to count as a teacher (at least 1/2/3, all 4 interviews) crossed with
how much year-2 evidence is required before calling the absence a
leave (observed in at least 1/2/3, all 4 second-year interviews).
A leaver is always a person never seen teaching in year 2. Uses the
same person-rotation machinery as build_panel_person_r3.py (monthly
CPS, Madrian-Lefgren validation). Writes outputs/definition_grid.csv
and report/figures_deck/definition_grid.{pdf,png}.
Run from the repo root after replication/build_cps_monthly.py."""
import glob
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import INK

INTDIR = "data/interim"
TEACHER_OCC = {2300, 2310, 2320, 2330}
USE = ["HRHHID", "HRHHID2", "PULINENO", "HRMIS", "HRYEAR4", "HRMONTH",
       "PESEX", "PTDTRACE", "PRTAGE", "PEEDUCA", "PEMLR", "PTIO1OCD",
       "PWSSWGT"]

files = sorted(glob.glob(f"{INTDIR}/cps_??????.parquet"))
assert files, "run replication/build_cps_monthly.py first"

def add_keys(d):
    d = d[d["HRMIS"].between(1, 8) & d["PULINENO"].notna()].copy()
    idx = d["HRYEAR4"] * 12 + d["HRMONTH"]
    d["start"] = (idx - (d["HRMIS"] - 1) - 8 * (d["HRMIS"] >= 5)).astype("Int32")
    d["pkey"] = (d["HRHHID"].astype(str) + "|" + d["HRHHID2"].astype(str)
                 + "|" + d["PULINENO"].astype(str) + "|"
                 + d["start"].astype(str))
    return d

teach_keys = set()
for f in files:
    d = add_keys(pd.read_parquet(f, columns=USE))
    t = d[d["PEMLR"].isin([1, 2]) & d["PTIO1OCD"].isin(TEACHER_OCC)
          & (d["PEEDUCA"] >= 43) & (d["HRMIS"] <= 4)]
    teach_keys.update(t["pkey"])
print(f"pass 1: {len(teach_keys):,} person-rotations", flush=True)

parts = []
for f in files:
    d = add_keys(pd.read_parquet(f, columns=USE))
    parts.append(d[d["pkey"].isin(teach_keys)])
R = pd.concat(parts, ignore_index=True)
R["teaching"] = (R["PEMLR"].isin([1, 2])
                 & R["PTIO1OCD"].isin(TEACHER_OCC)).astype(int)

g = R.groupby("pkey")
ok = (g["PESEX"].nunique() == 1) & (g["PTDTRACE"].nunique() == 1) \
     & ((g["PRTAGE"].max() - g["PRTAGE"].min()) <= 2)
R = R[R["pkey"].map(ok)]
print(f"validated: {R['pkey'].nunique():,} person-rotations", flush=True)

y1 = R[R["HRMIS"] <= 4]
y2 = R[R["HRMIS"] >= 5]
first_teach = (y1[y1["teaching"] == 1].sort_values(["HRYEAR4", "HRMONTH"])
               .drop_duplicates("pkey"))
P = first_teach.set_index("pkey")[["HRYEAR4", "PWSSWGT"]].copy()
P["n_y1_teach"] = y1.groupby("pkey")["teaching"].sum().reindex(P.index).fillna(0)
P["n_y2_obs"] = y2.groupby("pkey").size().reindex(P.index).fillna(0)
P["stay"] = y2.groupby("pkey")["teaching"].max().reindex(P.index).fillna(0)
P = P[P["HRYEAR4"] <= 2024]

rows = []
grid = np.full((4, 4), np.nan)
ns = np.zeros((4, 4), dtype=int)
for j in (1, 2, 3, 4):           # teaching in >= j year-1 interviews
    for k in (1, 2, 3, 4):       # observed in >= k year-2 interviews
        S = P[(P.n_y1_teach >= j) & (P.n_y2_obs >= k)]
        r = 100 * np.average(1 - S.stay, weights=S.PWSSWGT.astype(float))
        grid[j - 1, k - 1] = r
        ns[j - 1, k - 1] = len(S)
        rows.append({"teach_min": j, "obs_min": k, "rate": r, "n": len(S)})
pd.DataFrame(rows).to_csv("outputs/definition_grid.csv", index=False)
print(pd.DataFrame(grid.round(1),
                   index=[f"teach>={j}" for j in (1, 2, 3, 4)],
                   columns=[f"obs>={k}" for k in (1, 2, 3, 4)]).to_string())

NAVY = "#1F3864"
fig, ax = plt.subplots(figsize=(10.6, 5.6))
lo, hi = np.nanmin(grid), np.nanmax(grid)
for j in range(4):
    for k in range(4):
        v = grid[j, k]
        t = (v - lo) / (hi - lo)
        base = np.array([0.93, 0.95, 0.98])
        navy = np.array([0x1F, 0x38, 0x64]) / 255
        c = base + (navy - base) * (0.15 + 0.85 * t)
        ax.add_patch(plt.Rectangle((k, -j), 0.97, 0.97, facecolor=c,
                                   edgecolor="white", lw=2))
        dark = t > 0.45
        ax.text(k + 0.485, -j + 0.60, f"{v:.1f}", ha="center", va="center",
                fontsize=15, fontweight="bold",
                color="white" if dark else INK)
        ax.text(k + 0.485, -j + 0.24, f"n = {ns[j, k]:,}", ha="center",
                va="center", fontsize=8.2,
                color="#D6DEEA" if dark else "#6B7480")
for j, lab in enumerate(["teaching in at least 1\nof 4 interviews",
                         "teaching in at least 2",
                         "teaching in at least 3",
                         "teaching in all 4"]):
    ax.text(-0.12, -j + 0.485, lab, ha="right", va="center", fontsize=10.5,
            color=INK)
for k, lab in enumerate(["observed in at\nleast 1 interview",
                         "observed in\nat least 2",
                         "observed in\nat least 3",
                         "observed in\nall 4"]):
    ax.text(k + 0.485, 1.12, lab, ha="center", va="bottom", fontsize=9.8,
            color=INK)
ax.text(-2.55, 0.485, "Who is a teacher\n(year-1 requirement)",
        ha="left", va="center", fontsize=11, color=INK, fontweight="bold")
ax.text(1.97, 1.78, "Who is a leaver: never seen teaching in year 2, "
        "given how much of year 2 we require to see",
        ha="center", va="bottom", fontsize=11, color=INK, fontweight="bold")
ax.set_xlim(-2.6, 4.05)
ax.set_ylim(-3.1, 2.3)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig("report/figures_deck/definition_grid.pdf")
fig.savefig("report/figures_deck/definition_grid.png", dpi=200)
print("saved definition_grid")
