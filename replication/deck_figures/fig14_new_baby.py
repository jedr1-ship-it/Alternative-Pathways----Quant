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


# Figure 6. The Effect of a New Baby on Leaving, by Profession
NB = pd.read_csv("outputs/p_newbaby.csv").sort_values("AME_newbaby_pp")
NB["sig"] = NB["AME_newbaby_pp"].abs() > 1.96 * NB["se_pp"]
fig, ax = plt.subplots(figsize=(7.6, 4.4))
cols9 = [BLUE if p == "Teachers" else
         ("#5B6570" if s else "#D5D9DD")
         for p, s in zip(NB["prof"], NB["sig"])]
ax.barh(NB["prof"], NB["AME_newbaby_pp"], color=cols9, height=0.6)
ax.errorbar(NB["AME_newbaby_pp"], NB["prof"], xerr=1.96 * NB["se_pp"],
            fmt="none", ecolor=INK, elinewidth=0.9, capsize=2.5)
for i, (_, r) in enumerate(NB.iterrows()):
    ax.text(r["AME_newbaby_pp"] + 1.96 * r["se_pp"] + 0.45, i,
            f"+{r['AME_newbaby_pp']:.1f}", fontsize=9, va="center",
            color=BLUE if r["prof"] == "Teachers" else
            ("#3B4046" if r["sig"] else SUBTLE),
            fontweight="bold" if r["sig"] else "normal")
for tick, prof in zip(ax.get_yticklabels(), NB["prof"]):
    if prof == "Teachers":
        tick.set_fontweight("bold"); tick.set_color(BLUE)
ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-6, 14.5)
ax.set_xlabel("Effect of a new baby on P(a woman leaves her profession), pp")
ax.grid(axis="x", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g8_newbaby.png", dpi=200)
fig.savefig(f"{FIG}/g8_newbaby.pdf")
plt.close(fig)


