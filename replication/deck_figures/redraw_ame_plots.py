"""Redraw the two AME coefficient plots from the saved estimates
(outputs/ame_allyears.csv, outputs/ame_twoperiods.csv) without the age
row: age enters the specifications as a quadratic, so its single AME is
not interpretable. Sample sizes are those of the estimation runs.
Run from the repo root."""
import sys
sys.path.insert(0, "replication")
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

NAVY, GRAY, INK = "#1F3864", "#8A9096", "#1A2430"
BLACK = "#000000"
GROUPS = [
 ("Job attachment", [("fullyear", "Full-year contract"),
                     ("parttime_ly", "Part-time contract")]),
 ("Compensation", [("pension", "Employer pension plan"),
                   ("public_ly", "Public sector")]),
 ("Family", [("new_baby", "New baby during the year"),
             ("child_u6", "Child under 6"),
             ("n_children", "Number of children"),
             ("married", "Married"),
             ("sepdiv", "Separated or divorced")]),
 ("Demographics", [("female", "Female"),
                   ("black", "Black"),
                   ("ma_plus", "Master's degree or higher")]),
]

# ---------------- all-years probit AMEs ----------------
A = pd.read_csv("outputs/ame_allyears.csv", index_col=0)
ame, se = A["Probit_ame"], A["Probit_se"]
fig, ax = plt.subplots(figsize=(11.6, 6.6))
yy = 0
yticks, ylabels, heads = [], [], []
for gname, items in GROUPS:
    heads.append((yy, gname))
    yy -= 1
    for v, lab in items:
        a, s = ame[v], se[v]
        lo, hi = a - 1.96 * s, a + 1.96 * s
        sig = (lo > 0) or (hi < 0)
        ax.plot([lo, hi], [yy, yy], color=BLACK, lw=1.0,
                solid_capstyle="butt")
        ax.plot([lo, lo], [yy - .10, yy + .10], color=BLACK, lw=1.0)
        ax.plot([hi, hi], [yy - .10, yy + .10], color=BLACK, lw=1.0)
        ax.plot(a, yy, "o", ms=6.5, mfc=BLACK if sig else "white",
                mec=BLACK, mew=1.1)
        ax.annotate(f"{a:+.1f}", (a, yy), xytext=(0, 8),
                    textcoords="offset points", ha="center",
                    fontsize=9.5, color=INK)
        yticks.append(yy); ylabels.append(lab)
        yy -= 1
    yy -= 0.4
ax.axvline(0, color=BLACK, lw=0.8)
for hy, lab in heads:
    ax.text(-13.4, hy, lab, fontsize=12, fontweight="bold", color=INK,
            va="center")
ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=11)
ax.set_xlim(-13.5, 10)
ax.set_ylim(yy + 0.2, 1.0)
ax.set_xticks(range(-12, 10, 3))
ax.set_xlabel("average marginal effect on the probability of leaving "
              "(percentage points)", fontsize=11, color=INK)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("report/figures_deck/ame_allyears.pdf")
fig.savefig("report/figures_deck/ame_allyears.png", dpi=200)
print("saved ame_allyears")

# ---------------- the two-period comparison ----------------
B = pd.read_csv("outputs/ame_twoperiods.csv", index_col=0)
me1, se1 = B["ame_9717"], B["se_9717"]
me2, se2 = B["ame_1824"], B["se_1824"]
n1, n2 = 65575, 18571   # estimation Ns (build_ame_twoperiods.py)
fig, ax = plt.subplots(figsize=(11.6, 6.8))
yy = 0
yticks, ylabels, heads = [], [], []
for gname, items in GROUPS:
    heads.append((yy, gname))
    yy -= 1
    for v, lab in items:
        for me, se_, dy, col, filled in [(me1, se1, -0.20, GRAY, False),
                                         (me2, se2, 0.20, NAVY, True)]:
            a, s = me[v], se_[v]
            ax.plot([a - 1.96 * s, a + 1.96 * s], [yy + dy, yy + dy],
                    color=col, lw=1.1, solid_capstyle="butt")
            ax.plot(a, yy + dy, "o", ms=6,
                    mfc=col if filled else "white", mec=col, mew=1.2)
        yticks.append(yy); ylabels.append(lab)
        yy -= 1
    yy -= 0.4
ax.axvline(0, color=BLACK, lw=0.8)
for hy, lab in heads:
    ax.text(-13.4, hy, lab, fontsize=12, fontweight="bold", color=INK,
            va="center")
ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=11)
ax.set_xlim(-13.5, 10)
ax.set_ylim(yy + 0.2, 1.2)
ax.set_xticks(range(-12, 10, 3))
ax.set_xlabel("average marginal effect on the probability of leaving "
              "(percentage points)", fontsize=11, color=INK)
from matplotlib.lines import Line2D
ax.legend(handles=[
    Line2D([], [], marker="o", color=NAVY, mfc=NAVY, lw=1.1,
           label=f"2018–2024 (the deck's window, N = {n2:,})"),
    Line2D([], [], marker="o", color=GRAY, mfc="white", lw=1.1,
           label=f"1997–2017 (N = {n1:,})")],
    frameon=False, fontsize=10.5, loc="lower right")
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("report/figures_deck/ame_twoperiods.pdf")
fig.savefig("report/figures_deck/ame_twoperiods.png", dpi=200)
print("saved ame_twoperiods")
