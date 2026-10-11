"""The attachment gradient, shown: share never seen teaching in year 2,
by how many year-1 interviews showed the person teaching.
Writes report/figures_deck/sighting_gradient.{pdf,png} and the copy the
Beamer deck uses. Run from the repo root."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})

NAVY, BURG, INK, MUT = "#1F3864", "#7B2530", "#1A2430", "#6B7480"

d = pd.read_csv("outputs/panel_person_r3_decomp.csv")
d = d[d.leaver.notna() & (d.n_y2_obs >= 2)]
g = d.groupby("n_y1_teach").apply(
    lambda x: pd.Series({"rate": 100 * np.average(x.leaver, weights=x.PWSSWGT),
                         "n": len(x)})).reindex([1, 2, 3, 4])

fig, ax = plt.subplots(figsize=(10.8, 5.4))
colors = [BURG, "#A2606A", "#7C93B8", NAVY]
bars = ax.bar(g.index, g.rate, color=colors, width=0.62)
for xi, (r, n) in zip(g.index, zip(g.rate, g.n)):
    ax.annotate(f"{r:.0f}%", (xi, r + 1.2), ha="center", fontsize=16,
                fontweight="bold", color=INK)
    ax.annotate(f"n = {int(n):,}", (xi, -4.6), ha="center", fontsize=10.5,
                color=MUT, annotation_clip=False)
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(["once", "twice", "three times", "all four"], fontsize=13)
ax.set_xlabel("interviews of year 1 in which the person is seen teaching",
              fontsize=12.5, color=INK, labelpad=26)
ax.set_ylabel("share never seen teaching in year 2, percent",
              fontsize=12, color=INK)
ax.set_ylim(0, 62)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(labelsize=11)
fig.tight_layout()
fig.savefig("report/figures_deck/sighting_gradient.pdf")
fig.savefig("report/figures_deck/sighting_gradient.png", dpi=180)
fig.savefig("report/data_cluster/figures/sighting_gradient.pdf")
print("saved sighting_gradient")
