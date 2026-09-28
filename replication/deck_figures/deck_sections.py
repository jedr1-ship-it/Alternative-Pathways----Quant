"""Sober LaTeX-style panels: CPS definition, sensitivity chart, section dividers."""
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

SC = "report/figures_deck"
NAVY, CORAL, INK, MUT = "#1F4E79", "#B5443C", "#1A2430", "#55606B"

def save(fig, name):
    fig.savefig(f"{SC}/{name}.png", dpi=160); plt.close(fig); print("saved", name)

# ================= The Current Population Survey =================
fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.07, 0.90, "The Current Population Survey", fontsize=24,
        fontweight="bold", color=INK, va="top")
ax.plot([0.07, 0.93], [0.845, 0.845], color=INK, lw=0.8)
paras = [
    "The CPS is the monthly household survey of the United States, conducted by the Census Bureau for the Bureau of"
    "\nLabor Statistics. The country’s official employment and unemployment figures are computed from it.",
    "Each March, the Annual Social and Economic Supplement (ASEC) expands the sample to roughly 90,000 households"
    "\nand asks every adult about the previous calendar year: the longest job held, weeks worked, earnings, and benefits.",
    "The same recall question is the measurement device of this paper: whoever reports teaching as last year’s longest"
    "\njob, and no longer teaches at the March interview, has left the profession within the year.",
    "Households enter the survey on a fixed rotation (four months in, eight out, four in), so the same person can also"
    "\nbe found one year later — the basis of the alternative, panel-based measures discussed next.",
]
y = 0.76
for p in paras:
    ax.text(0.07, y, p, fontsize=12.5, color=INK, va="top", linespacing=1.5)
    y -= 0.135
ax.text(0.07, 0.15, "Pooled here: 28 consecutive supplements (1998–2025), 5,009,129 person-year records, 104,545 of them teachers.",
        fontsize=12.5, color=NAVY, va="top", fontweight="bold")
save(fig, "v_cps")

# ================= One file, many rates =================
P = pd.read_csv("outputs/p_series.csv")
E = pd.read_csv("outputs/evolution_by_year_gender.csv")
R3 = pd.read_csv("outputs/panel_person_r3.csv"); R3 = R3[R3.base_year <= 2024]
FN = pd.read_csv("outputs/panel_person_final.csv")
AR = pd.read_csv("outputs/asec_retrospective.csv")

fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.07, 0.93, "One file, many rates", fontsize=24, fontweight="bold",
        color=INK, va="top")
ax.text(0.07, 0.872, "Every series below is computed from the same CPS records; only the definition changes",
        fontsize=12.5, color=MUT, va="top", style="italic")
c = fig.add_axes([0.07, 0.30, 0.86, 0.52])
c.plot(R3.base_year, R3.leaver_r3, color=CORAL, lw=1.2, alpha=0.45)
c.plot(E.base_year, E.attr12_all, color=CORAL, lw=1.2, alpha=0.7, ls=(0, (4, 2)))
c.plot(FN.base_year, FN.leaver_final, color=CORAL, lw=2.4)
c.plot(P.cal_year, P.leaver_ba, color=NAVY, lw=2.4)
c.plot(AR.asec_year - 1, AR.leaver_rate, color=NAVY, lw=1.2, ls=(0, (2, 2)),
       marker="o", ms=4, mfc="white")
c.plot([2021], [8.0], marker="*", ms=13, color=INK, zorder=6)
c.annotate("NCES follow-up survey, 8.0", (2021, 8.0), xytext=(-40, -30),
           textcoords="offset points", fontsize=10, color=INK,
           arrowprops=dict(arrowstyle="-", color="#B9C0C8", lw=0.8))
LBL = [("panel, any teaching sighting — 18.2", R3.leaver_r3.iloc[-1], CORAL, 0.45),
       ("panel, month-pair counting — 15.4", E.attr12_all.iloc[-1], CORAL, 0.7),
       ("panel, one verdict per teacher — 13.0", FN.leaver_final.iloc[-1], CORAL, 1.0),
       ("March recall (this paper) — 8.6", P.leaver_ba.iloc[-1], NAVY, 1.0),
       ("pure occupation pair — 5.8", AR.leaver_rate.iloc[-1], NAVY, 0.8)]
for txt, yv, col, al in LBL:
    c.annotate(txt, (2024, yv), xytext=(8, 0), textcoords="offset points",
               fontsize=10.5, color=col, alpha=max(al, 0.75), va="center")
c.set_xlim(1996.5, 2033); c.set_ylim(0, 23)
c.set_xticks(range(1997, 2025, 3))
c.set_ylabel("teachers leaving per year, percent", fontsize=11, color=INK)
for s in ("top", "right"): c.spines[s].set_visible(False)
c.grid(axis="y", color="#F1F2F3", lw=1); c.set_axisbelow(True)
c.tick_params(labelsize=10)
ax.text(0.07, 0.205, "Three choices drive the spread. Who counts as a teacher: one monthly sighting admits substitutes and one-month spells, whose exit"
        "\nrate is five times that of year-round teachers. What counts as leaving: absence at a single later interview, or a durable exit of the year’s"
        "\nmain job. And how returns are treated: one in six panel leavers is teaching again within three months.",
        fontsize=11.5, color=INK, va="top", linespacing=1.55)
ax.text(0.07, 0.055, "The pure occupation pair understates exits to non-employment: the current-occupation field keeps the last job’s code for many respondents who no longer work.",
        fontsize=9.5, color=MUT, va="top")
save(fig, "v_sens")

# ================= section dividers =================
SECTIONS = [("d1", "1", "Data and measurement"),
            ("d2", "2", "The leaving rate"),
            ("d3", "3", "Where they go"),
            ("d4", "4", "Who leaves, and why"),
            ("d5", "5", "The business cycle"),
            ("d6", "6", "Pay and pensions")]
for tag, num, title in SECTIONS:
    fig = plt.figure(figsize=(13.33, 7.5))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.plot([0.38, 0.62], [0.585, 0.585], color=INK, lw=0.8)
    ax.text(0.5, 0.545, num, fontsize=16, color=MUT, ha="center", va="top")
    ax.text(0.5, 0.485, title, fontsize=27, color=INK, ha="center", va="top")
    ax.plot([0.38, 0.62], [0.40, 0.40], color=INK, lw=0.8)
    save(fig, f"v_{tag}")
print("panels done")
