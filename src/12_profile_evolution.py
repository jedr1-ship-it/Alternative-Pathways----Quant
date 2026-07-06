"""
The changing profile of the teaching workforce, built on every employed
person observed in a school-teaching occupation (no degree restriction):
  - fig17_profile_evolution.pdf : small-multiples annual series of six
    defining traits, the graphical version for the main text
  - table_profile_periods.tex   : the same traits in three sub-periods
    (2005-2011, 2012-2018, 2019-2025) with a test of the change between
    the first and the last, for the appendix. Sample sizes are unique
    persons.
"""
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.ticker import MaxNLocator
import statsmodels.formula.api as smf

from paperstyle import *

TEACHER_OCC = {2300, 2310, 2320, 2330}
CHLD_U6 = {1, 2, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15}

parts = []
for f in sorted(glob.glob("data/interim/cps_??????.parquet")):
    d = pd.read_parquet(f)
    e = d[d["PEMLR"].isin([1, 2]) & d["PTIO1OCD"].isin(TEACHER_OCC)].copy()
    parts.append(e)
T = pd.concat(parts, ignore_index=True)
T["period"] = pd.cut(T["HRYEAR4"], [2004, 2011, 2018, 2025],
                     labels=["2005--2011", "2012--2018", "2019--2025"])
T["female"] = (T["PESEX"] == 2).astype(int)
T["age"] = T["PRTAGE"]
T["under35"] = (T["PRTAGE"] < 35).astype(int)
T["white"] = (T["PTDTRACE"] == 1).astype(int)
T["hispanic"] = (T["PEHSPNON"] == 1).astype(int)
T["married"] = T["PEMARITL"].isin([1, 2]).astype(int)
T["child_u6"] = T["PRCHLD"].isin(CHLD_U6).astype(int)
T["ba_plus"] = (T["PEEDUCA"] >= 43).astype(int)
T["ma_plus"] = (T["PEEDUCA"] >= 44).astype(int)
T["public"] = T["PEIO1COW"].isin([1, 2, 3]).astype(int)
T["union"] = (T["PEERNLAB"] == 1).astype(float).where(T["PEERNLAB"] > 0)
T["parttime"] = T["PEHRUSL1"].between(1, 34).astype(int)
T["late"] = (T["period"] == "2019--2025").astype(int)

ROWS = [("Age, years", "age", "num"),
        ("Under 35", "under35", "pct"),
        ("Female", "female", "pct"),
        ("White", "white", "pct"),
        ("Hispanic", "hispanic", "pct"),
        ("Married", "married", "pct"),
        ("Child under 6 at home", "child_u6", "pct"),
        ("Bachelor's degree or higher", "ba_plus", "pct"),
        ("Master's degree or higher", "ma_plus", "pct"),
        ("Public-sector employer", "public", "pct"),
        ("Union member", "union", "pct"),
        ("Part-time", "parttime", "pct")]


def pstars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


def wmean(g, col):
    m = g[col].notna()
    return np.average(g.loc[m, col], weights=g.loc[m, "PWSSWGT"])


def n_persons(g):
    return len(g.drop_duplicates(["HRHHID", "HRHHID2", "PULINENO"]))


P1, P2, P3 = [T[T["period"] == p] for p in
              ["2005--2011", "2012--2018", "2019--2025"]]
sub13 = T[T["period"].isin(["2005--2011", "2019--2025"])]
with open("report/table_profile_periods.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccc}\n\\toprule\n"
             " & 2005--2011 & 2012--2018 & 2019--2025 & Change \\\\\n"
             "\\midrule\n")
    for lab, v, kind in ROWS:
        cells = []
        for g in (P1, P2, P3):
            m = wmean(g, v)
            cells.append(f"{m*100:.1f}\\%" if kind == "pct" else f"{m:.1f}")
        sub = sub13[sub13[v].notna()]
        t = smf.wls(f"{v} ~ late", data=sub, weights=sub["PWSSWGT"]).fit(
            cov_type="cluster", cov_kwds={"groups": sub["HRHHID"]})
        d, p = t.params["late"], t.pvalues["late"]
        dtxt = f"{d*100:+.1f}\\,pp" if kind == "pct" else f"{d:+.2f}"
        cells.append(dtxt + pstars(p))
        fh.write(f"{lab} & " + " & ".join(cells) + " \\\\\n")
    fh.write("\\midrule\nPersons & "
             + " & ".join(f"{n_persons(g):,}" for g in (P1, P2, P3))
             + " & \\\\\n\\bottomrule\n\\end{tabular}\n")
print("wrote report/table_profile_periods.tex")
for lab, v, kind in ROWS:
    scale = 1 if kind == "num" else 100
    print(f"{lab:32s}",
          " ".join(f"{wmean(g, v)*scale:5.1f}" for g in (P1, P2, P3)))
print("persons:", [n_persons(g) for g in (P1, P2, P3)])

# ---------- fig17: the evolution, graphically ----------
PANELS = [("Under 35", "under35"),
          ("Hispanic", "hispanic"),
          ("Bachelor's degree or higher", "ba_plus"),
          ("Master's degree or higher", "ma_plus"),
          ("Public-sector employer", "public"),
          ("Union member", "union")]
yearly = {v: T.groupby("HRYEAR4").apply(
    lambda g: wmean(g, v) * 100, include_groups=False)
    for _, v in PANELS}
pd.DataFrame(yearly).round(2).to_csv("outputs/profile_by_year.csv")

fig, axes = plt.subplots(2, 3, figsize=(9.6, 5.4))
for ax, (lab, v) in zip(axes.ravel(), PANELS):
    s = yearly[v]
    ax.plot(s.index, s.values, color=BLUE, lw=1.8, solid_capstyle="round")
    ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
    for x, ha, dx in [(s.index[0], "left", 0), (s.index[-1], "right", 0)]:
        ax.scatter([x], [s[x]], s=26, color=BLUE, zorder=4,
                   edgecolor=SURFACE, linewidth=1.5)
    lo, hi = s.min(), s.max()
    pad = max(1.5, (hi - lo) * 0.45)
    ax.set_ylim(lo - pad, hi + pad)
    halo = [pe.withStroke(linewidth=2.5, foreground=SURFACE)]
    ax.text(s.index[0], s.iloc[0] + pad * 0.28, f"{s.iloc[0]:.0f}%",
            ha="left", fontsize=9, fontweight="bold", color=INK,
            path_effects=halo)
    ax.text(s.index[-1], s.iloc[-1] + pad * 0.28, f"{s.iloc[-1]:.0f}%",
            ha="right", fontsize=9, fontweight="bold", color=INK,
            path_effects=halo)
    ax.set_title(lab, fontsize=10, fontweight="bold", color=INK, pad=6)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5, integer=True))
    ax.set_xticks([2005, 2015, 2025])
    ax.set_xlim(2004, 2026)
    ax.tick_params(labelsize=8.5)
fig.tight_layout(h_pad=2.2, w_pad=1.6)
fig.savefig("report/figures/fig17_profile_evolution.pdf",
            bbox_inches="tight")
plt.close(fig)
print("fig17 saved")
