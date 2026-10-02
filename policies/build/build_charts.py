"""Charts from policies.js: share of policies using each instrument, and policies by scale.
Run from policies/build:  python3 build_charts.py   (writes ../charts/*.png)"""
import json, subprocess, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "charts")
os.makedirs(OUT, exist_ok=True)

L = json.loads(subprocess.check_output(["node", "-e",
    "const P=require('./policies.js');const L=Array.isArray(P)?P:(P.POLICIES||P.policies||Object.values(P)[0]);"
    "console.log(JSON.stringify(L.map(p=>({used:[...new Set([p.cat,...(p.secondary||[])])],scale:p.scale}))))"],
    cwd=HERE))
N = len(L)

INSTR = ["Financial incentives", "Information & nudges", "Support & training",
         "Flexible positions", "Flexible re-certification"]
counts = {i: sum(i in p["used"] for p in L) for i in INSTR}
scales = {s: sum(p["scale"] == s for p in L) for s in ["Small", "Medium", "Large"]}

GREEN, MID, LIGHT = "#1F4E46", "#4E8C7F", "#A9CFC6"
INK, MUTED, GRID = "#1A1A1A", "#5F6368", "#E3E3E0"
FONT = "EB Garamond" if any("Garamond" in f.name for f in font_manager.fontManager.ttflist) else "serif"
plt.rcParams.update({"font.family": FONT, "font.size": 13, "text.color": INK,
                     "axes.labelcolor": MUTED, "xtick.color": INK, "ytick.color": MUTED})

# ---------- 1. instruments: bar chart, sorted from most to least used ----------
order = sorted(INSTR, key=lambda i: -counts[i])
pct = [100 * counts[i] / N for i in order]
fig, ax = plt.subplots(figsize=(10, 5.8), dpi=200)
fig.patch.set_facecolor("white")
bars = ax.bar(range(len(order)), pct, width=0.62, color=GREEN, zorder=3)
for b, i, v in zip(bars, order, pct):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.6, f"{v:.0f}%", ha="center", va="bottom",
            fontsize=16, fontweight="bold", color=INK)
    ax.text(b.get_x() + b.get_width() / 2, v + 7.2, f"{counts[i]} of {N}", ha="center", va="bottom",
            fontsize=11.5, color=MUTED)
ax.set_xticks(range(len(order)))
ax.set_xticklabels([i.replace(" & ", " &\n").replace("Flexible ", "Flexible\n") for i in order], fontsize=13.5)
ax.set_ylim(0, 100)
ax.set_yticks(range(0, 101, 25))
ax.set_yticklabels([f"{t}%" for t in range(0, 101, 25)], fontsize=11.5)
ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#9A9A96")
ax.tick_params(axis="both", length=0, pad=8)
fig.text(0.07, 0.95, "Share of policies that use each instrument", fontsize=21, fontweight="bold", color=INK)
fig.text(0.07, 0.905, f"{N} policies. A policy can use more than one instrument, so the shares add up to more than 100%.",
         fontsize=12.5, color=MUTED)
fig.subplots_adjust(left=0.07, right=0.98, top=0.84, bottom=0.15)
fig.savefig(os.path.join(OUT, "instruments_share.png"), facecolor="white")
plt.close(fig)

# ---------- 2. scale: pie chart, Small -> Medium -> Large clockwise from the top ----------
labels = ["Small", "Medium", "Large"]
vals = [scales[s] for s in labels]
cols = [LIGHT, MID, GREEN]
fig, ax = plt.subplots(figsize=(7, 6.2), dpi=200)
fig.patch.set_facecolor("white")
wedges, _ = ax.pie(vals, colors=cols, startangle=90, counterclock=False,
                   wedgeprops=dict(edgecolor="white", linewidth=2.5))
import math
for w, s, v in zip(wedges, labels, vals):
    ang = math.radians((w.theta1 + w.theta2) / 2)
    p = 100 * v / N
    if v / N < 0.12:   # thin slice: label outside with a short leader
        x, y = 1.25 * math.cos(ang), 1.2 * math.sin(ang)
        ax.annotate(f"{s}  {p:.0f}%\n{v} policies", xy=(1.0 * math.cos(ang), 1.0 * math.sin(ang)), xytext=(x, y),
                    ha="center", va="center", fontsize=14, color=INK,
                    arrowprops=dict(arrowstyle="-", color="#9A9A96", lw=1))
    else:
        x, y = 0.6 * math.cos(ang), 0.6 * math.sin(ang)
        ax.text(x, y, f"{s}\n{p:.0f}%", ha="center", va="center", fontsize=17, fontweight="bold", color="white")
        ax.text(x, y - 0.2, f"{v} policies", ha="center", va="top", fontsize=12, color="white")
ax.set_aspect("equal")
fig.text(0.06, 0.94, "Policies by scale", fontsize=21, fontweight="bold", color=INK)
fig.text(0.06, 0.895, f"{N} policies", fontsize=12.5, color=MUTED)
fig.subplots_adjust(left=0.04, right=0.96, top=0.86, bottom=0.03)
fig.savefig(os.path.join(OUT, "policies_by_scale.png"), facecolor="white")
plt.close(fig)

print(N, counts, scales)
