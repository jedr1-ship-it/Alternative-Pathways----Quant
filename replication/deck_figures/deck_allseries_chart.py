"""All-series chart as a clean image, full NCES series included."""
import sys
sys.path.insert(0, "replication")
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})
SC = "/tmp/claude-0/-home-user-Alternative-Pathways----Quant/37b5ad96-b2b0-50d1-9e4b-6301ff28b789/scratchpad"
NAVY, CORAL, CORAL_M, CORAL_L, INK, MUT = "#1F4E79", "#B5443C", "#C9726A", "#D99A94", "#1A2430", "#55606B"

P = pd.read_csv("outputs/p_series.csv")
E = pd.read_csv("outputs/evolution_by_year_gender.csv")
R3 = pd.read_csv("outputs/panel_person_r3.csv"); R3 = R3[R3.base_year <= 2024]
FN = pd.read_csv("outputs/panel_person_final.csv")
NCES_Y = [1988, 1991, 1994, 2000, 2004, 2008, 2012, 2021]
NCES_V = [5.6, 5.1, 6.6, 7.4, 8.4, 8.0, 7.7, 8.0]

fig, ax = plt.subplots(figsize=(12.2, 6.0))
ax.plot(R3.base_year, R3.leaver_r3, color=CORAL_L, lw=1.6)
ax.plot(E.base_year, E.attr12_all, color=CORAL_M, lw=1.6, ls=(0, (4, 2)))
ax.plot(FN.base_year, FN.leaver_final, color=CORAL, lw=2.6)
ax.plot(P.cal_year, P.leaver_ba, color=NAVY, lw=2.8)
ax.plot(NCES_Y, NCES_V, color=INK, lw=1.6, ls=(0, (3, 2)), marker="o",
        ms=5.5, mfc="white", mew=1.4)
for txt, yv, c in [("panel, any sighting   18.2", R3.leaver_r3.iloc[-1], CORAL_L),
                   ("panel, month pairs   15.4", E.attr12_all.iloc[-1], CORAL_M),
                   ("panel, one verdict   13.0", FN.leaver_final.iloc[-1], CORAL),
                   ("March recall   8.6", P.leaver_ba.iloc[-1] + 0.4, NAVY),
                   ("NCES follow-up   8.0", NCES_V[-1] - 0.9, INK)]:
    ax.annotate(txt, (2024.4, yv), fontsize=12, color=c, va="center", fontweight="bold")
ax.set_xlim(1987, 2033.5); ax.set_ylim(0, 23)
ax.set_xticks(range(1988, 2025, 4))
ax.set_ylabel("teachers leaving per year, percent", fontsize=12, color=INK)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1); ax.set_axisbelow(True)
ax.tick_params(labelsize=11)
fig.tight_layout()
fig.savefig(f"{SC}/v_allseries.png", dpi=170)
print("saved v_allseries")
