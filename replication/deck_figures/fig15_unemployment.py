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


# Figure 8. Leaving Teaching and the Unemployment Rate, 1997-2024
S5 = pd.read_csv("outputs/p_series.csv").sort_values("cal_year")
U = pd.read_csv("outputs/n_urate_official.csv")
M = S5.merge(U[["cal_year", "urate"]], on="cal_year")
M = M[M["leaver_ba"].notna()].sort_values("cal_year").reset_index(
    drop=True)
M = M.rename(columns={"leaver_ba": "leave", "rate_switch": "switch",
                      "rate_unemp": "unemp", "rate_leftlf": "leftlf"})


UM = pd.read_csv("outputs/n_urate_march.csv")
M["survey_year"] = M["cal_year"] + 1
M = M.merge(UM, on="survey_year", how="left")
M["urate_obs"] = M["u_march"]
M.to_csv("outputs/n_cyclicality.csv", index=False)
MS = M.dropna(subset=["urate_obs"])
for a in ("leave", "switch", "leftlf", "unemp"):
    r = np.corrcoef(MS[a], MS["urate_obs"])[0, 1]
    print(f"corr({a}, u March of survey) = {r:+.2f}")

TXT5, MUT5 = "#3B4046", "#8A9096"
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.6, 4.3),
                             gridspec_kw={"width_ratios": [1.35, 1]})
a1.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
M1 = M[M["cal_year"] >= 2000]


a1.plot(M1["cal_year"], M1["leave"], color=BLUE, lw=2.0, marker="o",
        ms=4.2, mec="white", mew=0.9, solid_capstyle="round")
a1.plot(M1["cal_year"], M1["urate"], color=TXT5, lw=1.6,
        ls=(0, (5, 3)), marker="o", ms=4.2, mec="white", mew=0.9,
        solid_capstyle="round")
for col, c in [("leave", BLUE), ("urate", TXT5)]:
    a1.annotate(f"{M1[col].iloc[-1]:.1f}", (M1["cal_year"].iloc[-1],
                M1[col].iloc[-1]), xytext=(6, 6),
                textcoords="offset points", fontsize=9, color=c,
                fontweight="bold")
a1.annotate("Teachers leaving the profession", (2010.5, 11.3),
            fontsize=9.5, color=BLUE, fontweight="bold", ha="center")
a1.annotate("Unemployment rate (BLS)", (2006.2, 2.2), fontsize=9,
            color=TXT5, ha="center")
a1.text(2019.5, 12.15, "Covid", ha="center", fontsize=8.5, color=SUBTLE)
a1.set_ylim(0, 12.8)
a1.set_yticks([0, 2, 4, 6, 8, 10, 12])
a1.set_xticks(range(2000, 2025, 4))
a1.tick_params(labelsize=9, length=0, colors=MUT5)
a1.set_ylabel("Percent", fontsize=10, color=TXT5)
a1.grid(axis="y", color="#F1F2F3", lw=1.0)
a1.set_axisbelow(True)
for s in ("top", "right", "left"):
    a1.spines[s].set_visible(False)
a1.spines["bottom"].set_color("#D8DBDE")


MS = MS.copy()
MS["bin"] = pd.qcut(MS["urate_obs"], 10, labels=False,
                    duplicates="drop")
NAVY, GRPH = "#2F5D8C", "#6B7280"
bx = MS.groupby("bin")["urate_obs"].mean()
for dep, c, lab in [("leftlf", NAVY, "Out of the labor force"),
                    ("switch", GRPH, "To another job")]:
    by = MS.groupby("bin")[dep].mean()
    a2.scatter(bx, by, color=c, s=42, zorder=4)
    b1, b0 = np.polyfit(MS["urate_obs"], MS[dep], 1)
    xs = np.linspace(MS["urate_obs"].min(), MS["urate_obs"].max(), 10)
    a2.plot(xs, b0 + b1 * xs, color=c, lw=1.4, zorder=3)

    a2.annotate(lab, (xs[-1], b0 + b1 * xs[-1]), fontsize=9,
                color=TXT5, va="bottom", ha="right",
                xytext=(0, 9), textcoords="offset points")
a2.set_ylim(1.55, 6.55)
a2.set_xlabel("Unemployment rate in the survey month (%)",
              fontsize=10, color=TXT5)
a2.set_ylabel("Exit rate by route (%)", fontsize=10, color=TXT5)
a2.tick_params(labelsize=9, length=0, colors=MUT5)
a2.grid(color="#F1F2F3", lw=1.0)
a2.set_axisbelow(True)
for s in ("top", "right", "left"):
    a2.spines[s].set_visible(False)
a2.spines["bottom"].set_color("#D8DBDE")
fig.tight_layout(w_pad=3)
fig.savefig(f"{FIG}/n5_cyclicality.png", dpi=200)
fig.savefig(f"{FIG}/n5_cyclicality.pdf")
plt.close(fig)


