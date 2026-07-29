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


# Figure 1. Composition of the Teaching Workforce, 2005-2024
WF = pd.read_csv("outputs/p_workforce.csv").sort_values("cal_year")
panels = [("age", "Mean age (years)", 2005), ("female", "Female", 2005),
          ("ma_plus", "Master's or higher", 2005),
          ("black", "Black", 2005),
          ("child_u6", "Child under 6", 2005),
          ("public", "Public school", 2005),
          ("parttime", "Part-time", 2005),
          ("pension", "Pension plan", 2005)]
fig, axes = plt.subplots(2, 4, figsize=(11.8, 5.6))
for axp, (v, lab, start) in zip(axes.flat, panels):
    d = WF[(WF["cal_year"] >= start) & WF[v].notna()]
    y = d[v].astype(float).reset_index(drop=True)
    xs = d["cal_year"].reset_index(drop=True)
    sm3 = y.rolling(3, center=True, min_periods=2).mean()
    axp.plot(xs, y, color="#BBBBBB", lw=1.0)
    axp.plot(xs, sm3, color=BLUE, lw=2.2)
    i13 = xs == 2013
    axp.plot(xs[i13], y[i13], "o", mfc="white", mec=GRAY, ms=4)
    axp.set_title(lab, fontsize=10, color=INK, pad=6)
    lo, hi = y.min(), y.max()
    pad = max((hi - lo) * 0.35, 0.8)
    axp.set_ylim(lo - pad, hi + pad * 1.7)
    dec = 1 if v == "age" else 0
    suf = "" if v == "age" else "%"
    x0, y0 = xs.iloc[0], sm3.iloc[0]
    x1, y1 = xs.iloc[-1], sm3.iloc[-1]
    axp.plot([x0, x1], [y0, y1], "o", color=BLUE, ms=5.5, zorder=5)
    rising0 = sm3.iloc[min(2, len(sm3) - 1)] > sm3.iloc[0]
    off0 = (2, -16) if rising0 else (2, 10)
    axp.annotate(f"{y0:.{dec}f}{suf}", (x0, y0), xytext=off0,
                 textcoords="offset points", ha="left", fontsize=8.8,
                 color=BLUE, fontweight="bold")
    axp.annotate(f"{y1:.{dec}f}{suf}", (x1, y1), xytext=(-2, 10),
                 textcoords="offset points", ha="right", fontsize=8.8,
                 color=BLUE, fontweight="bold")
    axp.set_xlim(2003.6, 2025.4)
    axp.set_xticks(range(2006, 2025, 2))
    axp.set_xticklabels([str(t) for t in range(2006, 2025, 2)],
                        fontsize=6.6, rotation=45)
    axp.tick_params(axis="y", labelsize=8)
    axp.grid(axis="y", color="#EFEFEF", lw=0.6)
    axp.set_axisbelow(True)
    despine(axp)
fig.tight_layout(h_pad=2.4)
fig.savefig(f"{FIG}/g1_workforce.png", dpi=200)
fig.savefig(f"{FIG}/g1_workforce.pdf")
plt.close(fig)


