import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

OUT = "report/figures_deck"
BLUE, GREEN, CORAL, DARK = "#2A5DB0", "#3E7C59", "#C4534B", "#3B4046"
M = pd.read_csv("outputs/p_ame.csv")
BLOCKS = [("Job attachment", ["fullyear", "parttime"], BLUE),
          ("Compensation", ["pension", "public"], GREEN),
          ("Family", ["new_baby", "child_u6", "n_children", "married",
                      "sepdiv"], CORAL),
          ("Demographics", ["female", "black", "ma_plus"], DARK)]
NAMES = {"fullyear": "Worked full year (50+ wks)",
         "parttime": "Part-time (<35 h/wk)", "pension": "Pension plan",
         "public": "Public school", "new_baby": "New baby this year",
         "child_u6": "Child under 6", "n_children": "Number of children",
         "married": "Married", "sepdiv": "Separated/divorced",
         "female": "Female", "black": "Black", "ma_plus": "Master's+"}
Mi = M.set_index("var")
rows = []
for bl, vs, c in BLOCKS:
    rows.append(("head", bl, c))
    for v in vs:
        rows.append(("var", v, c))
    rows.append(("gap", None, None))
rows = rows[:-1]
ypos = np.arange(len(rows))[::-1]
fig, ax = plt.subplots(figsize=(8.0, 5.7))
ax.axvline(0, color="#999999", lw=1.0)
ylabels = []
for yv, (kind, payload, c) in zip(ypos, rows):
    if kind == "head":
        ylabels.append(payload); continue
    if kind == "gap":
        ylabels.append(""); continue
    r = Mi.loc[payload]
    s = abs(r["AME_pp"]) > 1.96 * r["se_pp"]
    ax.errorbar(r["AME_pp"], yv, xerr=1.96 * r["se_pp"], fmt="o",
                color=c, ms=6.5, elinewidth=1.4, capsize=3,
                mfc=c if s else "white", mew=1.6)
    ax.annotate(f"{r['AME_pp']:+.1f}", (r["AME_pp"], yv), xytext=(0, 7),
                textcoords="offset points", ha="center", fontsize=8,
                color="#3B4046")
    ylabels.append(NAMES[payload])
ax.set_yticks(ypos)
ax.set_yticklabels(ylabels, fontsize=9.4)
for tick, (kind, payload, c) in zip(ax.get_yticklabels(), rows):
    if kind == "head":
        tick.set_fontweight("bold"); tick.set_color(c)
        tick.set_fontsize(9.8)
ax.tick_params(axis="y", length=0)
ax.set_xlim(-10.6, 7)
ax.set_ylim(ypos[-1] - 0.7, ypos[0] + 0.9)
ax.set_xticks([-9, -6, -3, 0, 3, 6])
ax.set_xlabel("Average marginal effect on P(leave teaching), pp   "
              "(filled: significant at 5%)", fontsize=9.5)
ax.grid(axis="x", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/g6_ame_v2.pdf")
fig.savefig(f"{OUT}/g6_ame_v2.png", dpi=220)
print("saved")
