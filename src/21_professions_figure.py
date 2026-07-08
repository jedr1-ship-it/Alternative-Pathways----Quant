"""
Body figure: leaving the occupation within twelve months for four
degree-holding professions under the identical linked design. Reads the
rates refreshed by 18_professions_fertility.py. Writes
report/figures/fig19_professions.pdf.
"""
import pandas as pd
import matplotlib.pyplot as plt

from paperstyle import *

r = pd.read_csv("outputs/professions_attrition.csv")
piv = r.pivot(index="base_year", columns="group", values="rate")

fig, ax = plt.subplots(figsize=(6.9, 3.8))
SERIES = [("Social workers", GREEN, 1.6, "Social workers"),
          ("Accountants and auditors", GOLD, 1.6, "Accountants"),
          ("Registered nurses", CORAL, 1.6, "Registered nurses"),
          ("Teachers", BLUE, 2.6, "Teachers")]
ends = {}
for g, c, lw, lab in SERIES:
    s = piv[g].rolling(3, center=True, min_periods=2).mean()
    ax.plot(s.index, s.values, color=c, lw=lw, solid_capstyle="round")
    ends[lab] = (s.index[-1], s.values[-1], c, g == "Teachers")
# spread end labels that sit within 2.5 points of each other
labs = sorted(ends.items(), key=lambda kv: kv[1][1])
ys = [v[1] for _, v in labs]
for i in range(1, len(ys)):
    if ys[i] - ys[i - 1] < 2.6:
        ys[i] = ys[i - 1] + 2.6
for (lab, (x, y0, c, bold)), y in zip(labs, ys):
    ax.text(x + 0.4, y, lab, fontsize=9.5, color=c, va="center",
            fontweight="bold" if bold else "normal")
ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
ax.set_xticks([2005, 2010, 2015, 2020, 2024])
ax.set_xlim(2004.5, 2030)
ax.set_ylim(0, 50)
ax.set_ylabel("Left the occupation within 12 months, %")
fig.tight_layout()
fig.savefig("report/figures/fig19_professions.pdf", bbox_inches="tight")
print("fig19 saved; latest rates:")
print(piv.tail(3).round(1).to_string())
