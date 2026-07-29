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
ax.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
ax.text(2019.5, 12.3, "Covid", ha="center", fontsize=8.5, color=SUBTLE)

ok = S["leaver_ba"].notna()
main = S[ok]
mean_ba = np.average(main["leaver_ba"])
ax.fill_between(main["cal_year"], main["leaver_ba"] - 1.96 * main["se_ba"],
                main["leaver_ba"] + 1.96 * main["se_ba"], color=BLUE,
                alpha=0.07, lw=0)
ax.axhline(mean_ba, color=INK, lw=0.9, ls=":", zorder=1)
ax.text(2014.0, 6.55, f"1997\u20132024 average: {mean_ba:.1f}",
        fontsize=8, color=INK, ha="center", va="top")
ax.plot(main["cal_year"], main["leaver_ba"], color=BLUE, lw=2.4)
last = main.iloc[-1]
pk = main.loc[main["leaver_ba"].idxmax()]
cov = main.loc[main["cal_year"] == 2019].iloc[0]
for r in (last, pk, cov):
    ax.plot(r["cal_year"], r["leaver_ba"], "o", color=BLUE, ms=5)
    ax.annotate(f"{r['leaver_ba']:.1f}", (r["cal_year"], r["leaver_ba"]),
                xytext=(0, 9), textcoords="offset points", ha="center",
                fontsize=9, color=BLUE, fontweight="bold")
ax.set_ylim(0, 13)
ax.set_xlim(1996, 2025.5)
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


