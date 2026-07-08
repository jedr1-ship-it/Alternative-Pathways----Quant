"""
Of every 100 non-returning leavers: labor force status twelve months
later, and the occupation composition of the employed, in one two-bar
zoom. Also the detailed destination bars for the appendix. Writes
report/figures/fig23_flow100.pdf and fig24_dest_detail.pdf.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from paperstyle import *
from covariates import load_panel

EDU = {230, 2200, 2205, 2340, 2350, 2360, 2430, 2435, 2440, 2540, 2545,
       2550, 2555}
CARE = {1820, 2000, 2001, 2002, 2010, 2011, 2012, 2013, 2014, 2015, 2016,
        2025, 2040, 2050, 2060, 2720, 2721, 2722, 3130, 3230, 3255, 3256,
        3257, 3258, 4600, 4610}

df = load_panel()
B = df[df["sampleB"]].copy()
L = B[B["leaver_p"] == 1].copy()
W = "PWSSWGT_0"
tot = L[W].sum()
emp_m = L["PEMLR_1"].isin([1, 2])
emp = L[emp_m]
e_edu = emp["PTIO1OCD_1"].isin(EDU)
e_care = emp["PTIO1OCD_1"].isin(CARE)
e_prof = ~e_edu & ~e_care & (emp["PTIO1OCD_1"] <= 3655)
e_rest = ~e_edu & ~e_care & ~e_prof
v1 = [np.average(emp_m, weights=L[W]) * 100,
      np.average((L["PEMLR_1"] == 5), weights=L[W]) * 100,
      np.average(L["PEMLR_1"].isin([6, 7]), weights=L[W]) * 100,
      np.average(L["PEMLR_1"].isin([3, 4]), weights=L[W]) * 100]
v2 = [emp.loc[m, W].sum() / tot * 100 for m in (e_edu, e_care, e_prof,
                                                e_rest)]
L1 = ["Employed", "Retired", "Out of the labor force", "Unemployed"]
C1 = [BLUE, "#9aa3ad", GOLD, "#5A6572"]
LV1 = [0, 0, 0, 1]
L2 = ["Education job", "Care and\nchildren", "Other\nprofessional",
      "Sales, office\nand manual"]
C2 = [BLUE, CORAL, GREEN, GRAY]

fig, ax = plt.subplots(figsize=(8.4, 3.9))
y1, y2, h = 1.72, 0.42, 0.4
x = 0
for lab, c, v, lv in zip(L1, C1, v1, LV1):
    ax.barh(y1, v, left=x, height=h, color=c,
            alpha=1.0 if lab == "Employed" else 0.75)
    ax.text(x + v / 2, y1, f"{v:.0f}", ha="center", va="center",
            fontsize=11, color="white", fontweight="bold")
    yl = y1 + h / 2 + 0.10 + lv * 0.30
    ax.text(x + v / 2, yl, lab, ha="center", va="bottom", fontsize=9)
    if lv:
        ax.plot([x + v / 2, x + v / 2], [y1 + h / 2 + 0.02, yl - 0.02],
                color=GRAY, lw=0.7)
    x += v
x = 0
for lab, c, v in zip(L2, C2, v2):
    ax.barh(y2, v, left=x, height=h, color=c)
    ax.text(x + v / 2, y2, f"{v:.0f}", ha="center", va="center",
            fontsize=11, color="white", fontweight="bold")
    ax.text(x + v / 2, y2 - h / 2 - 0.10, lab, ha="center", va="top",
            fontsize=9)
    x += v
ax.plot([0, 0], [y1 - h / 2 - 0.02, y2 + h / 2 + 0.02], color=GRAY,
        lw=0.9, ls=":")
ax.plot([v1[0], sum(v2)], [y1 - h / 2 - 0.02, y2 + h / 2 + 0.02],
        color=GRAY, lw=0.9, ls=":")
ax.text(-2, y1, "Of every 100\nnon-returning leavers", ha="right",
        va="center", fontsize=10)
ax.text(-2, y2, "What the employed\nare doing", ha="right", va="center",
        fontsize=10)
tot_ec = v2[0] + v2[1]
ax.annotate("", xy=(0, y2 - h / 2 - 0.62), xytext=(tot_ec, y2 - h / 2 - 0.62),
            arrowprops=dict(arrowstyle="-", color=INK, lw=1.1),
            annotation_clip=False)
for xx in (0, tot_ec):
    ax.plot([xx, xx], [y2 - h / 2 - 0.62, y2 - h / 2 - 0.54], color=INK,
            lw=1.1, clip_on=False)
ax.text(tot_ec / 2, y2 - h / 2 - 0.78,
        f"{tot_ec:.0f} of every 100 leavers keep working in education"
        " or care",
        ha="center", fontsize=10, fontweight="bold", color=INK)
ax.set_xlim(0, 100.5)
ax.set_ylim(-0.72, 2.72)
ax.axis("off")
fig.tight_layout()
fig.savefig("report/figures/fig23_flow100.pdf", bbox_inches="tight")
plt.close(fig)
print("fig23 saved", [round(v, 1) for v in v1], [round(v, 1) for v in v2])

# ---- appendix: detailed destination bars, complete to 100 ----------------
EDU_D = [("Education administrators", {230}),
         ("Other teachers, instructors and tutors", {2340, 2350, 2360}),
         ("Teaching assistants", {2540, 2545}),
         ("Postsecondary teachers", {2200, 2205}),
         ("Other education workers", {2550, 2555}),
         ("Librarians", {2430, 2435})]
CARE_D = [("Counselors", {2000, 2001, 2002}),
          ("Childcare workers", {4600}),
          ("Coaches and scouts", {2720, 2721, 2722}),
          ("Registered nurses", {3130, 3255, 3256, 3257, 3258}),
          ("Speech-language pathologists", {3230}),
          ("Social workers", {2010, 2011, 2012, 2013, 2014}),
          ("Clergy and religious workers", {2040, 2050, 2060})]
shown = set()
for _, cc in EDU_D + CARE_D:
    shown |= cc


def fam(o):
    if o <= 950:
        return "Management, business and finance"
    if o <= 1965:
        return "Computer, engineering and science"
    if o <= 2960:
        return "Arts, media and other professional"
    if o <= 3655:
        return "Other health occupations"
    if o <= 4650:
        return "Food, cleaning and personal services"
    if o <= 4965:
        return "Sales occupations"
    if o <= 5940:
        return "Office and administrative support"
    return "Blue-collar occupations"


tote = emp[W].sum()
rows = []
for lab, cc in EDU_D:
    rows.append((lab, emp.loc[emp["PTIO1OCD_1"].isin(cc), W].sum()
                 / tote * 100, "edu"))
for lab, cc in CARE_D:
    rows.append((lab, emp.loc[emp["PTIO1OCD_1"].isin(cc), W].sum()
                 / tote * 100, "care"))
r = emp[~emp["PTIO1OCD_1"].isin(shown)]
fams = r.groupby(r["PTIO1OCD_1"].map(fam))[W].sum() / tote * 100
for lab, v in fams.items():
    rows.append((lab, v, "oth"))
rows.sort(key=lambda x: x[1])
CMAP = {"edu": BLUE, "care": CORAL, "oth": GRAY}
fig, ax = plt.subplots(figsize=(7.4, 5.4))
yy = np.arange(len(rows))
ax.barh(yy, [x[1] for x in rows], color=[CMAP[x[2]] for x in rows],
        height=0.62)
for y, x in zip(yy, rows):
    ax.text(x[1] + 0.15, y, f"{x[1]:.1f}", va="center", fontsize=8.5)
ax.set_yticks(yy, [x[0] for x in rows], fontsize=9)
ax.set_xlabel("Share of employed non-returning leavers, %"
              " (bars sum to 100)")
ax.legend(handles=[Patch(color=BLUE, label="Education (detailed)"),
                   Patch(color=CORAL, label="Care and children (detailed)"),
                   Patch(color=GRAY, label="Broad occupation families")],
          loc="lower right", frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("report/figures/fig24_dest_detail.pdf", bbox_inches="tight")
print("fig24 saved; leavers n =", len(L), "employed n =", len(emp))
