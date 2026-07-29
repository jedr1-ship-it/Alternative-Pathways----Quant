import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

OUT = "report/figures_deck"
BLUE, CORAL, GREEN, GRAY, DARK, MUT = "#2A5DB0", "#C4534B", "#3E7C59", "#9AA1A8", "#3B4046", "#8A9096"
piv = pd.read_csv("outputs/pay_prof_medians.csv").set_index("cal_year")
sm = piv.rolling(3, center=True, min_periods=2).mean()
LVL = (sm.iloc[-1]/1000).to_dict()
idx = sm/sm.iloc[0]*100

fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.7), sharey=True)

def base(ax):
    ax.axhline(100, color="#B9BEC4", lw=1.0)
    ticks = list(range(1997, 2026, 4))
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticks, fontsize=8.8, rotation=45, ha="right")
    ax.tick_params(length=0, labelsize=9)
    ax.grid(axis="y", color="#F1F2F3", lw=1.0)
    ax.set_axisbelow(True)
    for s in ("top","right","left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8DBDE")

# panel 1: teachers vs all other graduates, gap in red
ax = axes[0]
ax.fill_between(idx.index, idx["Teachers"], idx["All other graduates"],
                color=CORAL, alpha=0.20, lw=0)
ax.plot(idx.index, idx["All other graduates"], color="#4A4F55", lw=2.1, solid_capstyle="round")
ax.plot(idx.index, idx["Teachers"], color=BLUE, lw=3.0, solid_capstyle="round")
ax.text(2013.5, 110.5,
        f"All other graduates  {idx['All other graduates'].iloc[-1]-100:+.0f}%",
        ha="center", fontsize=9.6, color=DARK)
ax.text(2013.5, 108.9, f"(${LVL['All other graduates']:.0f}k in 2024)",
        ha="center", fontsize=8.4, color=MUT)
ax.annotate(f"Teachers  {idx['Teachers'].iloc[-1]-100:+.0f}%",
            (2018, idx["Teachers"].loc[2018]), xytext=(0, -22),
            textcoords="offset points", ha="center", fontsize=9.8, color=BLUE,
            fontweight="bold")
ax.annotate(f"(${LVL['Teachers']:.0f}k in 2024)",
            (2018, idx["Teachers"].loc[2018]), xytext=(0, -34),
            textcoords="offset points", ha="center", fontsize=8.4, color=MUT)
ax.set_title("Teachers vs. the college labor market", fontsize=11,
             color=DARK, pad=10)
ax.set_ylabel("Real median earnings, 1997 = 100",
              fontsize=9.8, color=DARK)
base(ax)
ax.set_xlim(1996.5, 2025.4)

# panel 2: the kindred professions
ax = axes[1]
STYLE = {"Teachers": (BLUE, 3.0), "Registered nurses": (GREEN, 1.9),
         "Social workers": (CORAL, 1.9), "Accountants": ("#6E7680", 1.9)}
ends = {p: idx[p].iloc[-1] for p in STYLE}
for p_, (c, lw) in STYLE.items():
    ax.plot(idx.index, idx[p_], color=c, lw=lw, solid_capstyle="round")
order = sorted(ends, key=ends.get); ys = sorted(ends.values())
for i in range(1, len(ys)):
    if ys[i]-ys[i-1] < 4.6: ys[i] = ys[i-1]+4.6
for p_, y in zip(order, ys):
    ax.text(2025.0, y, f"{p_}  {ends[p_]-100:+.0f}%", fontsize=9.4,
            color=STYLE[p_][0], va="center",
            fontweight="bold" if p_=="Teachers" else "normal")
    ax.text(2025.0, y-1.7, f"(${LVL[p_]:.0f}k in 2024)", fontsize=8.2,
            color=MUT, va="center")
ax.set_title("Teachers vs. the comparable professions", fontsize=11,
             color=DARK, pad=10)
base(ax)
ax.set_xlim(1996.5, 2036)
axes[0].set_ylim(90, 128)
fig.tight_layout(w_pad=2.2)
fig.savefig(f"{OUT}/msgA3.png", dpi=200)
fig.savefig(f"{OUT}/msgA3.pdf")
print("saved")
