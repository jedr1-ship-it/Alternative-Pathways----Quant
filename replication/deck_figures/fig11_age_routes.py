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


# Figure 4. Leaving Teaching by Age and Route
R5 = pd.read_csv("outputs/p_routes_age.csv")
x = np.arange(len(R5))
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.stackplot(x, R5["switch"], R5["unemp"], R5["leftlf"],
             colors=[GOLD, GRAY, BLUE], alpha=0.92)
ax.plot(x, R5["total"], color=INK, lw=1.5)
for i in (0, 5, len(R5) - 1):
    ax.annotate(f"{R5['total'].iloc[i]:.0f}%", (i, R5["total"].iloc[i]),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=8.6, color=INK, fontweight="bold")
last = len(R5) - 1
y0 = R5["switch"].iloc[last]
y1 = y0 + R5["unemp"].iloc[last]
y2 = y1 + R5["leftlf"].iloc[last]
for lab, ym, c in [("to another job", y0 / 2, "#7A5B00"),
                   ("unemployed", (y0 + y1) / 2, "#555555"),
                   ("out of the labor force", (y1 + y2) / 2, BLUE)]:
    ax.annotate(lab, (last + 0.15, ym), fontsize=9, color=c, va="center",
                annotation_clip=False)
ax.set_xticks(x)
ax.set_xticklabels(R5["age"], fontsize=8.6)
ax.set_xlim(-0.3, last + 2.3)
ax.set_ylabel("Percent leaving, by route")
ax.set_xlabel("Age group")
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g4_routes_age.png", dpi=200)
fig.savefig(f"{FIG}/g4_routes_age.pdf")
plt.close(fig)


