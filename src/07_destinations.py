"""
Where do persistent leavers go, 12 months after teaching?

Classifies each persistent leaver's situation at t+12 using labor force
status (PEMLR: unemployed, retired, disabled, other out of the labor force)
and, for the employed, the destination occupation code. Education-adjacent
occupations (postsecondary teaching, tutoring and instruction, teaching
assistance, librarians, education administration) are singled out; the rest
are grouped into four broad occupation classes whose code ranges are stable
across the 2002, 2010 and 2020 classifications.
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from covariates import load_panel

BLUE, CORAL, GOLD = "#2a78d6", "#e34948", "#eda100"
INK, SUBTLE, SURFACE = "#1a2430", "#5a6572", "#fcfcfb"
NAVY = "#12355b"
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK, "axes.edgecolor": "#d8dbe0", "axes.labelcolor": SUBTLE,
    "xtick.color": SUBTLE, "ytick.color": SUBTLE,
    "axes.grid": True, "grid.color": "#e9ebee", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.size": 10,
})

# education-adjacent occupations across code vintages
EDU_ADJ = {230,                       # education administrators
           2200, 2205,                # postsecondary teachers
           2340, 2350, 2360,          # tutors, other teachers and instructors
           2430, 2435, 2440,          # librarians and library technicians
           2540, 2545, 2550, 2555}    # teaching assistants, other instruction


def classify(row):
    mlr, occ = row["PEMLR_1"], row["PTIO1OCD_1"]
    if mlr in (3, 4):
        return "Unemployed"
    if mlr == 5:
        return "Retired"
    if mlr == 6:
        return "Disabled"
    if mlr == 7:
        return "Out of the labor force, other"
    if occ in EDU_ADJ:
        return "Other education job"
    if occ <= 3655:
        return "Management and professional"
    if occ <= 4965:
        return "Services and sales"
    if occ <= 5940:
        return "Office and administrative"
    return "Manual and transportation"


df = load_panel()
B = df[df["sampleB"]].copy()
lv = B[B["leaver_p"] == 1].copy()
lv["where"] = lv.apply(classify, axis=1)
w = lv["PWSSWGT_0"]

shares = (lv.groupby("where")["PWSSWGT_0"].sum() / w.sum() * 100)
order = shares.sort_values(ascending=True)
print("destination shares of persistent leavers (weighted %):")
print(order.sort_values(ascending=False).round(1).to_string())

print("\nby gender (weighted %):")
tab = (lv.groupby(["where", "female"])["PWSSWGT_0"].sum()
         .unstack() / lv.groupby("female")["PWSSWGT_0"].sum() * 100)
tab.columns = ["men", "women"]
print(tab.round(1).sort_values("women", ascending=False).to_string())
tab.round(2).to_csv("outputs/destinations_by_gender.csv")

print("\nmean age by destination:")
print(lv.groupby("where").apply(
    lambda g: np.average(g["age"], weights=g["PWSSWGT_0"]),
    include_groups=False).round(1).sort_values(ascending=False).to_string())

# ---------- figure ----------
fig, ax = plt.subplots(figsize=(6.9, 3.6))
bars = ax.barh(order.index, order.values, height=0.6, color=BLUE, zorder=3)
for b, v in zip(bars, order.values):
    ax.text(v + 0.6, b.get_y() + b.get_height() / 2, f"{v:.0f}%",
            va="center", fontsize=10, color=INK, fontweight="bold")
ax.set_xlim(0, order.max() * 1.18)
ax.set_xlabel("Share of persistent leavers, 12 months after teaching (%)")
ax.xaxis.grid(True); ax.yaxis.grid(False)
ax.tick_params(length=0)
fig.tight_layout()
fig.savefig("report/figures/fig10_where.pdf")
print("\nsaved report/figures/fig10_where.pdf")
