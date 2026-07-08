"""
One figure, two definitions. Annual non-returning attrition for all
teachers (the headline) and for the official universe, full-time public
school teachers, so the reader sees that the level difference is
composition while the trend is the same. Writes
report/figures/fig22_evolution_defs.pdf.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from paperstyle import *
from covariates import load_panel

df = load_panel()
B = df[df["sampleB"]].copy()
W = "PWSSWGT_0"
official = B["PEIO1COW_0"].isin([1, 2, 3]) & \
    ~B["PEHRUSL1_0"].between(1, 34) & (B["PTIO1OCD_0"] != 2300)

rows = []
for y, g in B.groupby("base_year"):
    rows.append({"year": y,
                 "all": np.average(g["leaver_p"], weights=g[W]) * 100,
                 "off": np.average(g.loc[official.reindex(g.index),
                                         "leaver_p"],
                                   weights=g.loc[official.reindex(g.index),
                                                 W]) * 100})
r = pd.DataFrame(rows).set_index("year")
print(r.round(1).to_string())
print("mean gap", (r["all"] - r["off"]).mean().round(2),
      "sd of gap", (r["all"] - r["off"]).std().round(2))

fig, ax = plt.subplots(figsize=(6.9, 3.4))
ax.plot(r.index, r["all"], color=BLUE, lw=2.6, solid_capstyle="round")
ax.plot(r.index, r["off"], color=GRAY, lw=1.8, ls="--",
        solid_capstyle="round")
ax.text(r.index[-1] + 0.4, r["all"].iloc[-1], "All teachers",
        color=BLUE, fontsize=10, fontweight="bold", va="center")
ax.text(r.index[-1] + 0.4, r["off"].iloc[-1],
        "Official universe\n(full-time public)", color=GRAY, fontsize=9.5,
        va="center")
ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
ax.set_xticks([2005, 2010, 2015, 2020, 2024])
ax.set_xlim(2004.5, 2031)
ax.set_ylim(0, 22)
ax.set_ylabel("Non-returning leavers, % per year")
fig.tight_layout()
fig.savefig("report/figures/fig22_evolution_defs.pdf", bbox_inches="tight")
print("fig22 saved")
