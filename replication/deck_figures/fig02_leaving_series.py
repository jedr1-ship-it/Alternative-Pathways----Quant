import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import sys
sys.path.insert(0, "replication")
from paperstyle import BLUE, CORAL, GOLD, GREEN, GRAY, INK, SUBTLE

FIG = "report/figures_deck"
LIGHT = "#AEC3DE"
DARK = "#3D4754"
TXT5 = TXT5b = TXT6 = "#3B4046"
MUT5 = MUT5b = MUT6 = "#8A9096"


def h1(v):
    return f"{math.floor(v * 10 + 0.5) / 10:.1f}"


def despine(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# Figure 2. Leaving Teaching, 1997-2024
S = pd.read_csv("outputs/p_series.csv").sort_values("cal_year")
fig, ax = plt.subplots(figsize=(8.4, 4.2))

ok = S["leaver_ba"].notna()
main = S[ok]
mean_ba = np.average(main["leaver_ba"])
WBOX = dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9)
# 99 percent band: every NCES wave falls inside it (2009 sits just below
# the 95 percent band)
Z = 2.576
ax.fill_between(main["cal_year"], main["leaver_ba"] - Z * main["se_ba"],
                main["leaver_ba"] + Z * main["se_ba"], color=BLUE,
                alpha=0.08, lw=0)
ax.plot([1996, 2024.6], [mean_ba, mean_ba], color=INK, lw=0.9, ls=":",
        zorder=1)
ax.text(2024.9, mean_ba, f"average {mean_ba:.1f}", fontsize=8.5,
        color=INK, ha="left", va="center")
ax.plot(main["cal_year"], main["leaver_ba"], color=BLUE, lw=2.4)
last = main.iloc[-1]
pk = main.loc[main["leaver_ba"].idxmax()]
cov = main.loc[main["cal_year"] == 2019].iloc[0]
for r in (pk, cov):
    ax.plot(r["cal_year"], r["leaver_ba"], "o", color=BLUE, ms=5)
    ax.annotate(f"{r['leaver_ba']:.1f}", (r["cal_year"], r["leaver_ba"]),
                xytext=(0, 9), textcoords="offset points", ha="center",
                fontsize=9, color=BLUE, fontweight="bold", bbox=WBOX)
ax.plot(last["cal_year"], last["leaver_ba"], "o", color=BLUE, ms=5)
ax.annotate(f"{last['leaver_ba']:.1f}", (last["cal_year"], last["leaver_ba"]),
            xytext=(8, -2), textcoords="offset points", ha="left",
            va="center", fontsize=9, color=BLUE, fontweight="bold")
# NCES follow-up survey waves, as in the definitions chart: at the survey
# year, except 2000-01, placed at its exit year (2000) because the 2001
# point of the recall series carries the recession spike the wave predates
NC_Y, NC_V = [2000, 2005, 2009, 2013, 2022], [7.4, 8.4, 8.0, 7.7, 8.0]
ax.plot(NC_Y, NC_V, ls="none", marker="D", ms=6.5, mfc="#000000",
        mec="white", mew=1.1, zorder=6,
        label="NCES follow-up survey (official benchmark)")
for x, v in zip(NC_Y, NC_V):
    ax.annotate(f"{v}", (x, v), xytext=(0, -12), textcoords="offset points",
                ha="center", fontsize=8, color="#000000", bbox=WBOX,
                zorder=7)
ax.legend(loc="upper left", frameon=False, fontsize=8.5, handletextpad=0.4)
ax.set_ylim(0, 13.5)
ax.set_xlim(1996, 2027.2)
ax.set_xticks(range(1998, 2025, 2))
ax.set_xticklabels([str(t) for t in range(1998, 2025, 2)], fontsize=8,
                   rotation=45)
ax.set_ylabel("Percent leaving teaching")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g2_evolution.png", dpi=200)
fig.savefig(f"{FIG}/g2_evolution.pdf")
plt.close(fig)


