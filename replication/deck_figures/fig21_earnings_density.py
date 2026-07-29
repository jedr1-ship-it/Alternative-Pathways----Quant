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


# Figure 10. The Distribution of Earnings Changes: Stayers and Leavers
DM = pd.read_csv("outputs/p_dlog_micro.csv")
STd = DM.loc[DM["group"] == "stayer", "dlog"]
LVd = DM.loc[DM["group"] == "leaver_employed", "dlog"]
NAVY6, RED6 = "#33526E", "#B04A42"
fig, ax = plt.subplots(figsize=(8.8, 4.6))
xg = np.linspace(-160, 210, 500)
ys_ = gaussian_kde(STd, bw_method=0.25)(xg)
yl_ = gaussian_kde(LVd, bw_method=0.25)(xg)
ax.fill_between(xg, 0, ys_, color="#E2E7EC", alpha=0.9, zorder=2)
ax.fill_between(xg, 0, yl_, color="#F3DCD8", alpha=0.75, zorder=3)
ax.plot(xg, ys_, color=NAVY6, lw=2.4, solid_capstyle="round", zorder=4)
ax.plot(xg, yl_, color=RED6, lw=2.4, solid_capstyle="round", zorder=5)
for d, c, yy in [(STd, NAVY6, ys_), (LVd, RED6, yl_)]:
    med = np.median(d)
    ax.plot([med, med], [0, np.interp(med, xg, yy)], color=c, lw=1.1,
            ls=(0, (3, 2)), zorder=6)
ax.annotate("Stayers", (12, 0.0146), fontsize=11, color=NAVY6,
            fontweight="bold")
ax.annotate("median +3", (12, 0.0134), fontsize=8.8, color=NAVY6)
ax.annotate("Leavers, employed", (68, 0.0054), fontsize=11,
            color=RED6, fontweight="bold")
ax.annotate("median +15", (68, 0.0042), fontsize=8.8, color=RED6)
ax.annotate("24% lose big", (-92, 0.0035), fontsize=9, color=RED6,
            ha="center", fontweight="bold")
ax.annotate("45% win big", (146, 0.0035), fontsize=9, color=RED6,
            ha="center", fontweight="bold")
ax.set_xlim(-160, 210)
ax.set_ylim(0, 0.0175)
ax.set_yticks([])
ax.set_xticks([-150, -100, -50, 0, 50, 100, 150, 200])
ax.set_xlabel("Change in annual earnings, log points ×100",
              fontsize=10, color=TXT6)
ax.tick_params(labelsize=9, length=0, colors=MUT6)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8DBDE")
fig.tight_layout()
fig.savefig(f"{FIG}/g5b_earnings_density.png", dpi=200)
fig.savefig(f"{FIG}/g5b_earnings_density.pdf")
plt.close(fig)


