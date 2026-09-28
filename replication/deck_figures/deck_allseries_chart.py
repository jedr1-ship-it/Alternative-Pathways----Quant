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
NAVY, CORAL, CORAL_M, CORAL_L, INK, MUT = "#1F3864", "#7B2530", "#A2606A", "#C79AA0", "#1A2430", "#55606B"

P = pd.read_csv("outputs/p_series.csv")
E = pd.read_csv("outputs/evolution_by_year_gender.csv")
R3 = pd.read_csv("outputs/panel_person_r3.csv"); R3 = R3[R3.base_year <= 2024]
FN = pd.read_csv("outputs/panel_person_final.csv")
# NCES waves inside the sample window (1997-2024) only
NCES_Y = [2000, 2004, 2008, 2012, 2021]
NCES_V = [7.4, 8.4, 8.0, 7.7, 8.0]

fig, ax = plt.subplots(figsize=(12.2, 6.0))
ax.plot(R3.base_year, R3.leaver_r3, color=CORAL_L, lw=1.6)
ax.plot(E.base_year, E.attr12_all, color=CORAL_M, lw=1.6, ls=(0, (4, 2)))
ax.plot(FN.base_year, FN.leaver_final, color=CORAL, lw=2.6)
ax.plot(P.cal_year, P.leaver_ba, color=NAVY, lw=2.8)
ax.plot(NCES_Y, NCES_V, color=INK, ls="none", marker="o",
        ms=6.5, mfc=INK, mec="white", mew=1.2)
for txt, yv, c in [("Any sighting   18.2", R3.leaver_r3.iloc[-1], CORAL_L),
                   ("Month pairs   15.4", E.attr12_all.iloc[-1], CORAL_M),
                   ("Panel measure   13.0", FN.leaver_final.iloc[-1], CORAL),
                   ("Annual recall   8.6", P.leaver_ba.iloc[-1] + 0.4, NAVY),
                   ("NCES follow-up   8.0", NCES_V[-1] - 0.9, INK)]:
    ax.annotate(txt, (2024.4, yv), fontsize=12, color=c, va="center", fontweight="bold")
ax.set_xlim(1996.3, 2031.5); ax.set_ylim(0, 23)
ax.set_xticks(range(1997, 2025, 4))
ax.set_ylabel("teachers leaving per year, percent", fontsize=12, color=INK)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1); ax.set_axisbelow(True)
ax.tick_params(labelsize=11)
fig.tight_layout()
fig.savefig(f"{SC}/v_allseries.png", dpi=170)
print("saved v_allseries")
