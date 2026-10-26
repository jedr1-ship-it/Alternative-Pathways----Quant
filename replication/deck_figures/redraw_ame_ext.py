"""Redraw the main-body coefficient plot (full specification, probit
AMEs, calendar 2018-2024) from outputs/ame_ext_probit.csv without the
age row: age enters as a quadratic, so its single AME is not
interpretable. Writes report/figures_deck/ame_ext_noage.{pdf,png}.
Run from the repo root after build_flow_lpm_figs.py."""
import sys
sys.path.insert(0, "replication")
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

INK, BLACK = "#1A2430", "#000000"
res = pd.read_csv("outputs/ame_ext_probit.csv", index_col=0)
GROUPS = [
 ("Job attachment", [("fullyear", "Full-year contract"),
                     ("parttime", "Part-time contract")]),
 ("Compensation", [("pension", "Employer pension plan"),
                   ("public_ly", "Public sector"),
                   ("lowinc", "Bottom-quartile household income")]),
 ("Family", [("baby", "New baby during the year"),
             ("kid_u6", "Child under 6"),
             ("nkids", "Number of children"),
             ("married", "Married"),
             ("sepdiv", "Separated or divorced")]),
 ("Health", [("badhealth", "Fair or poor health"),
             ("disab", "With a disability")]),
 ("Demographics", [("female", "Female"),
                   ("black", "Black"),
                   ("ma_plus", "Master's degree or higher")]),
]
fig, ax = plt.subplots(figsize=(11.6, 7.0))
y = 0
yticks, ylabels, heads = [], [], []
for gname, items in GROUPS:
    heads.append((y, gname))
    y -= 1
    for v, lab in items:
        a, s = res.loc[v, "ame"], res.loc[v, "se"]
        lo, hi = a - 1.96 * s, a + 1.96 * s
        sig = (lo > 0) or (hi < 0)
        ax.plot([lo, hi], [y, y], color=BLACK, lw=1.0, solid_capstyle="butt")
        ax.plot([lo, lo], [y - .10, y + .10], color=BLACK, lw=1.0)
        ax.plot([hi, hi], [y - .10, y + .10], color=BLACK, lw=1.0)
        ax.plot(a, y, "o", ms=6.5, mfc=BLACK if sig else "white",
                mec=BLACK, mew=1.1)
        ax.annotate(f"{a:+.1f}", (a, y), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=9.5,
                    color=INK)
        yticks.append(y); ylabels.append(lab)
        y -= 1
    y -= 0.4
ax.axvline(0, color=BLACK, lw=0.8)
for hy, lab in heads:
    ax.text(-14.4, hy, lab, fontsize=12, fontweight="bold", color=INK,
            va="center")
ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=11)
ax.set_xlim(-14.5, 12)
ax.set_ylim(y + 0.2, 1.0)
ax.set_xticks(range(-12, 11, 3))
ax.set_xlabel("average marginal effect on the probability of leaving "
              "(percentage points)", fontsize=11, color=INK)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("report/figures_deck/ame_ext_noage.pdf")
fig.savefig("report/figures_deck/ame_ext_noage.png", dpi=200)
print("saved ame_ext_noage")
