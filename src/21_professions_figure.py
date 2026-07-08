"""
Body figure: leaving the occupational field within twelve months, teachers
versus registered nurses, the two comparison professions whose distinctive
occupational titles keep census coding error small. Field exit counts a
move to any occupation outside education (respectively outside health
practice), so promotions and switches inside the field do not count.
Reads the rates refreshed by 18_professions_fertility.py. Writes
report/figures/fig19_professions.pdf.
"""
import pandas as pd
import matplotlib.pyplot as plt

from paperstyle import *

r = pd.read_csv("outputs/professions_attrition.csv")
piv = r.pivot(index="base_year", columns="group", values="rate_field")

fig, ax = plt.subplots(figsize=(6.9, 3.4))
SERIES = [("Registered nurses", CORAL, 1.8, "Registered nurses"),
          ("Teachers", BLUE, 2.6, "Teachers")]
for g, c, lw, lab in SERIES:
    s = piv[g].rolling(3, center=True, min_periods=2).mean()
    ax.plot(s.index, s.values, color=c, lw=lw, solid_capstyle="round")
    ax.text(s.index[-1] + 0.4, s.values[-1], lab, fontsize=10, color=c,
            va="center", fontweight="bold" if g == "Teachers" else "normal")
ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
ax.set_xticks([2005, 2010, 2015, 2020, 2024])
ax.set_xlim(2004.5, 2030)
ax.set_ylim(0, 25)
ax.set_ylabel("Left the occupational field within 12 months, %")
fig.tight_layout()
fig.savefig("report/figures/fig19_professions.pdf", bbox_inches="tight")
print("fig19 saved; pooled field-exit rates:")
n = r.groupby("group")["n"].sum()
pool = (r.assign(w=r["rate_field"] * r["n"]).groupby("group")["w"].sum() / n)
pool_occ = (r.assign(w=r["rate"] * r["n"]).groupby("group")["w"].sum() / n)
print(pd.DataFrame({"occ": pool_occ, "field": pool, "n": n}).round(1))
