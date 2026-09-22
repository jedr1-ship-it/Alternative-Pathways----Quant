"""Tech slides under rule R3 (person-level): regenerates u3, u3b, u3c, u4, u5, u6."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import paperstyle  # noqa: F401

SC = "report/figures_deck"
BLUE, CORAL, GREEN, GOLD = "#00549F", "#B5443C", "#3A8A62", "#D9A21B"
INK, MUT, LGRAY, GHOST = "#1A2430", "#6B7480", "#D9DDE2", "#F2F3F5"

def canvas(title, subtitle):
    fig = plt.figure(figsize=(13.33, 7.5))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.05, 0.94, title, fontsize=25, fontweight="bold", color=INK, va="top")
    ax.text(0.05, 0.877, subtitle, fontsize=12.5, color=MUT, va="top")
    return fig, ax

def save(fig, name):
    fig.savefig(f"{SC}/{name}.png", dpi=160); plt.close(fig); print("saved", name)

def rbox(ax, x, y, w, h, c, alpha=0.08, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.004,rounding_size=0.012",
                 facecolor=c, alpha=alpha, edgecolor=c, lw=lw))

R3 = pd.read_csv("outputs/panel_person_r3.csv")
R3 = R3[R3.base_year <= 2024]
P = pd.read_csv("outputs/p_series.csv")

# ================= u3: the design, verdict under R3 =================
fig, ax = canvas("Eight interviews, one verdict per teacher",
                 "Interviewed 4 months, at rest 8, interviewed 4 more — the verdict lives in the second-year block")
x0, cw, gap = 0.065, 0.0525, 0.004
y0, ch = 0.585, 0.105
cx = lambda m: x0 + (m-1) * (cw + gap) + cw/2
for m in range(1, 17):
    x = x0 + (m-1) * (cw + gap)
    mis = m if m <= 4 else (m - 8 if m >= 13 else None)
    inn = mis is not None
    c = BLUE if inn else LGRAY
    ax.add_patch(FancyBboxPatch((x, y0), cw, ch,
                 boxstyle="round,pad=0.002,rounding_size=0.008",
                 facecolor=c, edgecolor="none", alpha=1 if inn else 0.8))
    ax.text(x + cw/2, y0 + ch*0.62, str(m), fontsize=10.5, fontweight="bold",
            ha="center", va="center", color="white" if inn else MUT)
    if inn:
        ax.text(x + cw/2, y0 + ch*0.24, f"MIS {mis}", fontsize=6.8,
                ha="center", va="center", color="white", alpha=0.85)
# year-1 bracket
ax.plot([cx(1)-0.024, cx(4)+0.024], [0.73, 0.73], color=GREEN, lw=2)
ax.text((cx(1)+cx(4))/2, 0.748, "teacher: seen teaching in at least one of these",
        fontsize=9.5, color=GREEN, ha="center", fontweight="bold")
# year-2 bracket
ax.plot([cx(13)-0.024, cx(16)+0.024], [0.73, 0.73], color=CORAL, lw=2)
ax.text((cx(13)+cx(16))/2, 0.748, "the verdict block",
        fontsize=9.5, color=CORAL, ha="center", fontweight="bold")
ax.text(cx(8.5), 0.528, "the second-year interviews fall exactly one year after the first-year ones",
        fontsize=9, color=MUT, ha="center")
Y = 0.42
RULES = [
    ("Teacher", GREEN, "seen teaching (occupation code, employed, BA+) in at least one first-year interview — one sighting is enough."),
    ("Stayer", BLUE, "seen teaching in at least one second-year interview. One sighting anywhere in the block settles it."),
    ("Leaver", CORAL, "observed in the second year and never seen teaching there. Not one month, in any of the interviews."),
    ("Dropped", MUT, "no second-year interview at all (the household moved or never answered again) — unclassifiable, out of the sample."),
]
for lab, c, txt in RULES:
    ax.text(0.05, Y, lab, fontsize=12, fontweight="bold", color=c, va="top")
    ax.text(0.155, Y, txt, fontsize=10.8, color=INK, va="top")
    Y -= 0.062
ax.text(0.05, 0.115, "One person, one verdict, counted once — weighted by their first teaching interview. "
        "Rate under this rule: 18.2% per year (2005–2024).",
        fontsize=11, color=INK, fontweight="bold", va="top")
ax.text(0.05, 0.068, "Sample: 54,847 classified teachers; 20% of teaching rotations have no second-year interview and are dropped — that loss is the price of the constructed link.",
        fontsize=9.5, color=MUT, va="top")
save(fig, "u3_eight")

# ================= u3b: worked examples under R3 =================
fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.05, 0.945, "Five teachers, five verdicts", fontsize=24,
        fontweight="bold", color=INK, va="top")
ax.text(0.05, 0.885, "Rule R3, cell by cell: one sighting in the second year makes you a stayer; "
        "silence across the whole block makes you a leaver.",
        fontsize=12.5, color=MUT, va="top")
LEG = [(BLUE, "seen teaching, first year"), (GREEN, "seen teaching, second year"),
       (CORAL, "second year, never teaching"), (LGRAY, "interviewed, not teaching"),
       ("#EAE4D4", "not interviewed")]
lx = 0.05
for c, lab in LEG:
    ax.add_patch(FancyBboxPatch((lx, 0.822), 0.016, 0.026,
                 boxstyle="round,pad=0.001,rounding_size=0.004", facecolor=c, edgecolor="none"))
    ax.text(lx + 0.022, 0.835, lab, fontsize=8.6, color=INK, va="center")
    lx += 0.03 + len(lab) * 0.0052
X0, CW, GAP = 0.05, 0.0385, 0.0033
def cxm(m): return X0 + (m-1) * (CW + GAP)
def strip(y, cells, verdict, vc, caption):
    for m in range(1, 17):
        fill, letter, lc = cells.get(m, (GHOST, "", MUT))
        ax.add_patch(FancyBboxPatch((cxm(m), y), CW, 0.052,
                     boxstyle="round,pad=0.0015,rounding_size=0.006",
                     facecolor=fill, edgecolor="none"))
        ax.text(cxm(m) + CW/2, y + 0.026, letter or str(m),
                fontsize=8.3 if letter else 6.8,
                fontweight="bold" if letter else "normal",
                ha="center", va="center", color=lc if letter else "#B9BFC7")
    ax.add_patch(FancyBboxPatch((0.755, y + 0.002), 0.088, 0.048,
                 boxstyle="round,pad=0.002,rounding_size=0.008", facecolor=vc, edgecolor="none"))
    ax.text(0.799, y + 0.026, verdict, fontsize=9.5, color="white",
            fontweight="bold", ha="center", va="center")
    ax.text(0.05, y - 0.019, caption, fontsize=9.2, color=INK, va="top", linespacing=1.3)
T  = (BLUE, "T", "white")
NG = (LGRAY, "–", MUT)
SY = (GREEN, "T", "white")
LV = (CORAL, "–", "white")
NO = ("#EAE4D4", "×", "#A89F8A")
rows = [
 ({1:T,2:T,3:T,4:T, 13:SY,14:SY,15:SY,16:SY}, "STAYER", GREEN,
  "1 · Teaching at every interview → stayer, counted once."),
 ({1:T,2:NG,3:NG,4:NG, 13:LV,14:LV,15:LV,16:SY}, "STAYER", GREEN,
  "2 · YOUR CASE — teacher only in month 1, silent at 13–15, teaching again at 16: one second-year sighting settles it → stayer."),
 ({1:T,2:T,3:NG,4:NG, 13:LV,14:LV,15:LV,16:LV}, "LEAVER", CORAL,
  "3 · Taught in months 1–2, observed all through the second year and never teaching there → leaver."),
 ({1:T,2:T,3:T,4:T, 13:LV,14:LV,15:LV,16:LV}, "LEAVER", CORAL,
  "4 · The fully attached teacher who is gone: taught all four, silent across the whole second-year block → leaver."),
 ({1:T,2:T,3:T,4:T, 13:NO,14:NO,15:NO,16:NO}, "DROPPED", "#8A9096",
  "5 · Moved away — no second-year interview exists: unclassifiable, dropped (20% of teaching rotations)."),
]
y = 0.735
for cells, verdict, vc, cap in rows:
    strip(y, cells, verdict, vc, cap)
    y -= 0.125
ax.text(0.05, 0.095, "No cell-by-cell pairing anymore:", fontsize=12, fontweight="bold", color=BLUE, va="top")
ax.text(0.32, 0.095, "the first-year block answers “was this person a teacher?”;\nthe second-year block answers “are they still?”. One person, one verdict.",
        fontsize=11, color=INK, va="top", linespacing=1.4)
fig.savefig(f"{SC}/u3b_examples.png", dpi=160); plt.close(fig); print("saved u3b")

# ================= u3c: the R3 number =================
fig, ax = canvas("One teacher, one verdict — the rate under rule R3",
                 "Person-level leaving in the linked monthly panel, 2005–2024")
c3 = fig.add_axes([0.07, 0.14, 0.55, 0.60])
c3.plot(R3.base_year, R3.leaver_r3, color=CORAL, lw=2.6, solid_capstyle="round")
c3.plot(P.cal_year, P.leaver_ba, color=BLUE, lw=2.4)
c3.annotate("R3 — person level\nmean 18.2%", (2024, R3.leaver_r3.iloc[-1]),
            xytext=(8, -2), textcoords="offset points", fontsize=10.5,
            color=CORAL, fontweight="bold", va="center", linespacing=1.2)
c3.annotate("March recall\n7.7%", (2024, P.leaver_ba.iloc[-1]),
            xytext=(8, 0), textcoords="offset points", fontsize=10.5,
            color=BLUE, fontweight="bold", va="center", linespacing=1.2)
c3.set_xlim(1996.5, 2031); c3.set_ylim(0, 23)
c3.set_xticks(range(1997, 2025, 4))
c3.set_ylabel("percent of teachers leaving per year", fontsize=9.5, color=INK)
for s in ("top", "right"): c3.spines[s].set_visible(False)
c3.grid(axis="y", color="#F1F2F3", lw=1); c3.set_axisbelow(True)
c3.tick_params(labelsize=9)
ax.text(0.68, 0.71, "Why 18 — above the old pair-\ncounting 15.4:", fontsize=11.5,
        fontweight="bold", color=INK, va="top", linespacing=1.3)
ax.text(0.68, 0.625, "every person counts once, so the teacher\nseen only one month weighs as much as\n"
        "the teacher seen all four — and the loosely\nattached leave more.",
        fontsize=10.5, color=INK, va="top", linespacing=1.4)
ax.text(0.68, 0.46, "Why still far above 7.7:", fontsize=11.5,
        fontweight="bold", color=INK, va="top")
ax.text(0.68, 0.415, "R3 asks “did anyone who ever taught this\nyear teach at all next year?”; March asks\n"
        "“is the year’s main job still the job?”.\nDifferent question, different level.",
        fontsize=10.5, color=INK, va="top", linespacing=1.4)
ax.text(0.05, 0.062, "54,847 teachers classified · weighted by the first teaching interview · base year 2025 dropped (second-year windows censored).",
        fontsize=9.5, color=MUT, va="top")
save(fig, "u3c_pairs")

# ================= u4: two definitions =================
fig, ax = canvas("Two ways to define a leaver",
                 "Same CPS files, two instruments — and the level tracks the instrument")
rbox(ax, 0.05, 0.52, 0.42, 0.27, BLUE, alpha=0.05)
ax.text(0.065, 0.755, "A — March recall (this deck)", fontsize=12.5, fontweight="bold", color=BLUE)
ax.text(0.065, 0.705, "Teacher: the longest job held last calendar year was teaching\n(one recall question, same record).\nLeaver: at the March interview that job is gone — switched\noccupation, unemployed, or out of the labor force.",
        fontsize=10, color=INK, va="top", linespacing=1.45)
ax.text(0.065, 0.555, "1997–2024 · no link needed · one person, one record · 7.7%",
        fontsize=10, fontweight="bold", color=BLUE)
rbox(ax, 0.05, 0.16, 0.42, 0.27, CORAL, alpha=0.05)
ax.text(0.065, 0.395, "B — Linked monthly panel, rule R3", fontsize=12.5, fontweight="bold", color=CORAL)
ax.text(0.065, 0.345, "Teacher: seen teaching in at least one first-year interview.\nStayer: seen teaching in at least one second-year interview.\nLeaver: observed in year two, never seen teaching there.\nOne person, one verdict.",
        fontsize=10, color=INK, va="top", linespacing=1.45)
ax.text(0.065, 0.195, "2005–2024 · constructed link · person level · 18.2%",
        fontsize=10, fontweight="bold", color=CORAL)
c4 = fig.add_axes([0.55, 0.14, 0.41, 0.64])
c4.axhspan(6.0, 8.4, color="#F0F2F4", zorder=0)
c4.plot(R3.base_year, R3.leaver_r3, color=CORAL, lw=2.4)
c4.plot(P.cal_year, P.leaver_ba, color=BLUE, lw=2.4)
c4.annotate("B — 18.2%", (2024, R3.leaver_r3.iloc[-1]), xytext=(6, 0),
            textcoords="offset points", fontsize=11, color=CORAL, fontweight="bold", va="center")
c4.annotate("A — 7.7%", (2024, P.leaver_ba.iloc[-1]), xytext=(6, 0),
            textcoords="offset points", fontsize=11, color=BLUE, fontweight="bold", va="center")
c4.text(1997.5, 5.2, "band: published benchmarks 6–8.4", fontsize=8.5, color=MUT)
c4.set_xlim(1996.5, 2029.5); c4.set_ylim(0, 23)
c4.set_xticks(range(1997, 2025, 4))
c4.set_ylabel("percent leaving per year", fontsize=9.5, color=INK)
for s in ("top", "right"): c4.spines[s].set_visible(False)
c4.grid(axis="y", color="#F1F2F3", lw=1); c4.set_axisbelow(True)
c4.tick_params(labelsize=9)
ax.text(0.05, 0.075, "Both are correct about the thing they measure: B counts people who ever taught and vanish from teaching; A counts durable exits from the year’s main job.",
        fontsize=10.5, color=MUT)
save(fig, "u4_twodefs")

# ================= u5: why 18 and 8 are both true =================
fig, ax = canvas("Why 18 and 8 are both true",
                 "The gap between the two instruments is composition and question, not error")
c5 = fig.add_axes([0.07, 0.18, 0.30, 0.58])
for x, v, c, lab in [(0, 18.2, CORAL, "Linked panel\nrule R3"),
                     (1, 7.7, BLUE, "March recall\n(this deck)")]:
    c5.bar(x, v, width=0.55, color=c, zorder=3)
    c5.text(x, v + 0.5, f"{v}", ha="center", fontsize=14, fontweight="bold", color=c)
    c5.text(x, -1.2, lab, ha="center", fontsize=10, color=INK, va="top",
            fontweight="bold", linespacing=1.2)
c5.set_xlim(-0.6, 1.6); c5.set_ylim(0, 21); c5.axis("off")
YR = 0.72
REASONS = [
    ("Who counts as a teacher", "R3: anyone seen teaching even one month — substitutes, half-years, marginal spells all count once.\nMarch: only those whose main job of the year was teaching."),
    ("What counts as leaving", "R3: never observed teaching across the second-year interviews — a point-in-time absence repeated.\nMarch: the main teaching job of last year is gone by the interview."),
    ("Who survives the link", "R3 loses the 20% who move or stop answering — and movers leave more, so the loss cuts both ways.\nMarch: no link, nobody lost."),
]
for hd, txt in REASONS:
    ax.text(0.44, YR, hd, fontsize=11.5, fontweight="bold", color=INK, va="top")
    ax.text(0.44, YR - 0.042, txt, fontsize=10, color=INK, va="top", linespacing=1.4)
    YR -= 0.185
ax.text(0.05, 0.062, "Neither number is wrong; they answer different questions. The deck reports the March measure because it is the one the literature reports.",
        fontsize=10.5, color=MUT, va="top")
save(fig, "u5_bridge")

# ================= u6: why march =================
fig, ax = canvas("Why we keep the March question",
                 "One reason: it is the literature’s measure — every published benchmark is directly comparable")
c6 = fig.add_axes([0.10, 0.18, 0.80, 0.52])
rows6 = [("Washington payroll (Goldhaber–Theobald)", (6.0, 8.0), None, "#5E6672"),
         ("TFS roster follow-up, 2021–22", None, 8.4, "#5E6672"),
         ("Retrospective CPS (Aldeman–Yi 2025)", None, 7.6, "#5E6672"),
         ("This deck — March recall, 1997–2024", None, 7.7, BLUE),
         ("Linked monthly panel, rule R3 (different object)", None, 18.2, CORAL)]
yy = np.arange(len(rows6))[::-1]
for y, (lab, iv, pt, c) in zip(yy, rows6):
    if iv:
        c6.plot(iv, [y, y], color=c, lw=5, alpha=0.45, solid_capstyle="round")
        c6.text(iv[1] + 0.25, y, "6–8", fontsize=10.5, color=c, va="center", fontweight="bold")
    if pt:
        big = c in (BLUE, CORAL)
        c6.plot([pt], [y], "o", ms=13 if big else 9, color=c, mec="white", mew=1.6, zorder=5)
        c6.text(pt + 0.32, y, f"{pt}", fontsize=11.5 if big else 10.5,
                color=c, va="center", fontweight="bold")
    c6.text(3.6, y, lab, fontsize=11, color=c, ha="right", va="center",
            fontweight="bold" if c == BLUE else "normal")
c6.axvspan(6.0, 8.4, color="#F0F2F4", zorder=0)
c6.set_xlim(-9, 21); c6.set_ylim(-0.7, 4.7)
c6.set_xticks(range(4, 21, 2))
c6.tick_params(labelsize=9.5, left=False, labelleft=False)
for s in ("top", "right", "left"): c6.spines[s].set_visible(False)
c6.set_xlabel("teachers leaving per year, percent", fontsize=10, color=INK)
ax.text(0.05, 0.065, "Our March number sits inside the published band; the person-level panel number sits far outside it because it answers a different question. Comparability decides.",
        fontsize=10.5, color=MUT)
save(fig, "u6_whymarch")
print("all R3 panels done")
