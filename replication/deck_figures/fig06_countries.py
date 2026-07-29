import sys
sys.path.insert(0, "replication")
import matplotlib.pyplot as plt
import numpy as np
import paperstyle  # noqa: F401

BLUE, GRAY, DARK, MUT = "#2A5DB0", "#D4DAE0", "#3B4046", "#8A9096"
OUT = "report/figures_deck"

data = [("Hong Kong", "2022/23", 9.2, "public schools, system exit"),
        ("England", "2024/25", 8.5, "state-funded schools"),
        ("Flanders (BE)", "2022/23", 8.3, "education sector"),
        ("United States", "2024", 7.7, "the teaching profession"),
        ("New Zealand", "2024", 7.3, "the teaching profession"),
        ("Netherlands", "2023/24", 7.0, "primary education"),
        ("Wales", "2023/24", 5.7, "the teaching profession"),
        ("Israel", "2021/22", 5.6, "the education system"),
        ("Australia", "2021", 5.1, "the profession, tax records"),
        ("Germany", "2024/25", 5.0, "school service, permanent"),
        ("Japan", "2021", 3.9, "public schools"),
        ("France", "2021/22", 2.7, "the profession, civil servants"),
        ("Ireland", "2022/23", 2.3, "the profession")]

fig, ax = plt.subplots(figsize=(9.6, 7.0))
ys = np.arange(len(data))[::-1]
for y, (c, yr, v, defn) in zip(ys, data):
    us = c == "United States"
    ax.barh(y, v, height=0.6, color=BLUE if us else GRAY, zorder=3)
    ax.text(-0.18, y + 0.17, c, ha="right", va="center", fontsize=11,
            color=BLUE if us else DARK,
            fontweight="bold" if us else "normal")
    ax.text(-0.18, y - 0.22, f"{defn}, {yr}", ha="right", va="center",
            fontsize=7.6, color=MUT)
    ax.text(v + 0.14, y, f"{v:.1f}", va="center", fontsize=11.5,
            color=BLUE if us else DARK, fontweight="bold")
ax.set_xlim(0, 10.4)
ax.set_ylim(-0.6, len(data) - 0.4)
ax.axis("off")

fig.subplots_adjust(left=0.28, right=0.95, top=0.985, bottom=0.015)
fig.savefig(f"{OUT}/intl_bars_deck.pdf")
fig.savefig(f"{OUT}/intl_bars_deck.png", dpi=200)
print("saved", len(data), "bars")
