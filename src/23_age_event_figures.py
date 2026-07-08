"""
Two age-at-baseline figures on the main analytic sample (non-returning
definition, baseline MIS 1-3). First, the U-shaped age profile of exit,
one line per decade, showing that the rise is within age groups rather
than composition. Second, the age profile of each exit route (another
occupation, retirement, other labor-force exit, unemployment), markers
drawn only where the rate reaches one percent. Writes
report/figures/fig20_age_periods.pdf and
report/figures/fig21_routes_age.pdf.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from paperstyle import *
from covariates import load_panel

df = load_panel()
B = df[df["sampleB"] & df["PRTAGE_0"].between(22, 64)].copy()

BINS = [(22, 24), (25, 29), (30, 34), (35, 39), (40, 44),
        (45, 49), (50, 54), (55, 59), (60, 64)]
B["bin"] = pd.cut(B["PRTAGE_0"], [a for a, _ in BINS] + [65],
                  labels=[f"{a}-{b}" for a, b in BINS], right=False)
labs = [f"{a}-{b}" for a, b in BINS]
x = np.arange(len(labs))
W = "PWSSWGT_0"


def wrate(d, col):
    return np.average(d[col], weights=d[W]) * 100


# ---- figure 20: the U by period -------------------------------------
fig, ax = plt.subplots(figsize=(6.9, 3.4))
for per, (y0, y1), color, ls in [("2005-2014", (2005, 2014), GRAY, "--"),
                                 ("2015-2024", (2015, 2024), BLUE, "-")]:
    d = B[B["base_year"].between(*(y0, y1))]
    r = [wrate(d[d["bin"] == l], "leaver_p") for l in labs]
    ax.plot(x, r, color=color, ls=ls, lw=2.2, marker="o", ms=5,
            solid_capstyle="round")
    ax.text(x[-1] + 0.15, r[-1], per, fontsize=10, color=color,
            va="center", fontweight="bold")
    print(per, [round(v, 1) for v in r])
ax.set_xticks(x)
ax.set_xticklabels(labs)
ax.set_xlim(-0.4, len(labs) + 0.9)
ax.set_ylim(0, 36)
ax.set_xlabel("Age at baseline")
ax.set_ylabel("Non-returning leavers, % per year")
fig.tight_layout()
fig.savefig("report/figures/fig20_age_periods.pdf", bbox_inches="tight")

# ---- figure 21: exit routes by age ----------------------------------
B["r_occ"] = ((B["leaver_p"] == 1) & B["PEMLR_1"].isin([1, 2])).astype(int)
B["r_unemp"] = ((B["leaver_p"] == 1) & B["PEMLR_1"].isin([3, 4])).astype(int)
B["r_ret"] = ((B["leaver_p"] == 1) & (B["PEMLR_1"] == 5)).astype(int)
B["r_olf"] = ((B["leaver_p"] == 1) & B["PEMLR_1"].isin([6, 7])).astype(int)

# unemployment never exceeds 1.2 percent of teachers at any age, so the
# figure shows the three routes that carry the story
ROUTES = [("r_occ", "Move to another occupation", CORAL),
          ("r_olf", "Leave the labor force, other", GOLD),
          ("r_ret", "Retire", GREEN)]
fig, ax = plt.subplots(figsize=(6.9, 3.6))
for col, lab, c in ROUTES:
    r = np.array([wrate(B[B["bin"] == l], col) for l in labs])
    ax.plot(x, r, color=c, lw=2.0, solid_capstyle="round", label=lab)
    m = r >= 1.0          # markers only where the route reaches 1 percent
    ax.plot(x[m], r[m], "o", color=c, ms=5)
    print(lab, [round(v, 1) for v in r])
print("Become unemployed",
      [round(v, 1) for v in
       [wrate(B[B["bin"] == l], "r_unemp") for l in labs]])
ax.set_xticks(x)
ax.set_xticklabels(labs)
ax.set_ylim(0, 18.5)
ax.set_xlabel("Age at baseline")
ax.set_ylabel("Share of teachers per year, %")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=3,
          frameon=False, fontsize=9.5)
fig.tight_layout()
fig.savefig("report/figures/fig21_routes_age.pdf", bbox_inches="tight")
print("figures 20 and 21 saved")
