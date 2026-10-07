"""Seminar-style coefficient plot of the probit AMEs.
Writes report/figures_deck/ame_seminar.pdf. Run from the repo root.
Estimates and standard errors as in report/table_p_probit.tex
(probit, college-graduate teachers, 2015-2024, year effects, n=28,900)."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})

NAVY, INK, MUT = "#1F3864", "#1A2430", "#6B7480"

GROUPS = [
    ("Job attachment", [
        ("Worked full year (50+ weeks)", -9.31, 0.32),
        ("Part-time (<35 h/week)",        4.47, 0.37)]),
    ("Compensation", [
        ("Enrolled in a pension plan",   -2.44, 0.32),
        ("Public school",                -1.72, 0.32)]),
    ("Family", [
        ("New baby during the year",      4.67, 0.78),
        ("Child under 6",                 0.53, 0.51),
        ("Number of children",           -0.53, 0.17),
        ("Married",                      -0.40, 0.43),
        ("Separated or divorced",         0.83, 0.58)]),
    ("Demographics", [
        ("Female",                       -1.41, 0.34),
        ("Black",                         1.87, 0.49),
        ("Master's degree or higher",    -0.86, 0.30)]),
]

rows = []
for gname, items in GROUPS:
    rows.append(("HEAD", gname, None, None))
    for lab, ame, se in items:
        rows.append(("EST", lab, ame, se))
    rows.append(("GAP", "", None, None))
rows = rows[:-1]

fig, ax = plt.subplots(figsize=(11.6, 6.4))
y = 0
yticks, ylabels, head_ys = [], [], []
for kind, lab, ame, se in rows:
    if kind == "HEAD":
        head_ys.append((y, lab))
    elif kind == "EST":
        lo, hi = ame - 1.96 * se, ame + 1.96 * se
        sig = (lo > 0) or (hi < 0)
        ax.plot([lo, hi], [y, y], color=NAVY, lw=1.4,
                solid_capstyle="butt", zorder=3)
        ax.plot([lo, lo], [y - 0.14, y + 0.14], color=NAVY, lw=1.2, zorder=3)
        ax.plot([hi, hi], [y - 0.14, y + 0.14], color=NAVY, lw=1.2, zorder=3)
        ax.plot(ame, y, marker="o", ms=7.5, mfc=NAVY if sig else "white",
                mec=NAVY, mew=1.4, zorder=4)
        ax.annotate(f"{ame:+.1f}", (ame, y), xytext=(0, 9),
                    textcoords="offset points", ha="center",
                    fontsize=10, color=INK)
        yticks.append(y)
        ylabels.append(lab)
    y -= 1

ax.axvline(0, color=MUT, lw=0.9, ls=(0, (4, 3)), zorder=1)
for hy, lab in head_ys:
    ax.text(-11.6, hy, lab, fontsize=12.5, fontweight="bold", color=INK,
            va="center", ha="left")
ax.set_yticks(yticks)
ax.set_yticklabels(ylabels, fontsize=11.5, color=INK)
ax.set_xlim(-11.7, 7.2)
ax.set_ylim(y + 0.4, 0.8)
ax.set_xticks(range(-9, 7, 3))
ax.set_xlabel("average marginal effect on the probability of leaving, "
              "percentage points", fontsize=11.5, color=INK)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0, labelsize=11.5)
ax.tick_params(axis="x", labelsize=10.5)
ax.grid(axis="x", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.annotate("filled: significant at 5 percent; whiskers: 95 percent "
            "confidence intervals", (0.0, -0.115),
            xycoords="axes fraction", fontsize=9.5, color=MUT)
fig.tight_layout()
fig.savefig("report/figures_deck/ame_seminar.pdf")
print("saved ame_seminar.pdf")
