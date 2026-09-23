"""Final panel definition slides: three conditions, no more. Regenerates
u3 (the definition), u3b (examples), u3c (the rate), u4, u5, u6."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import paperstyle  # noqa: F401
import matplotlib as mpl
mpl.rcParams.update({"font.serif": ["STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})

SC = "report/figures_deck"
BLUE, CORAL, GREEN, GOLD = "#00549F", "#B5443C", "#3A8A62", "#D9A21B"
INK, MUT, LGRAY, GHOST = "#1A2430", "#6B7480", "#D9DDE2", "#F2F3F5"

def canvas(title, subtitle):
    fig = plt.figure(figsize=(13.33, 7.5))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.05, 0.94, title, fontsize=25, fontweight="bold", color=INK, va="top")
    ax.text(0.05, 0.877, subtitle, fontsize=12.5, color=MUT, va="top", style="italic")
    return fig, ax

def save(fig, name):
    fig.savefig(f"{SC}/{name}.png", dpi=160); plt.close(fig); print("saved", name)

def rbox(ax, x, y, w, h, c, alpha=0.08, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.004,rounding_size=0.012",
                 facecolor=c, alpha=alpha, edgecolor=c, lw=lw))

F = pd.read_csv("outputs/panel_person_final.csv")
P = pd.read_csv("outputs/p_series.csv")

# ================= u3: THE DEFINITION =================
fig, ax = canvas("The panel definition",
                 "Each person is interviewed up to 8 times: 4 months, 8 at rest, 4 more one year later. Three conditions, one verdict.")
# strip
x0, cw, gap = 0.065, 0.0525, 0.004
y0, ch = 0.63, 0.10
cx = lambda m: x0 + (m-1) * (cw + gap) + cw/2
for m in range(1, 17):
    x = x0 + (m-1) * (cw + gap)
    inn = m <= 4 or m >= 13
    c = BLUE if inn else LGRAY
    ax.add_patch(FancyBboxPatch((x, y0), cw, ch,
                 boxstyle="round,pad=0.002,rounding_size=0.008",
                 facecolor=c, edgecolor="none", alpha=1 if inn else 0.8))
    ax.text(x + cw/2, y0 + ch/2, str(m), fontsize=10.5, fontweight="bold",
            ha="center", va="center", color="white" if inn else MUT)
ax.plot([cx(1)-0.024, cx(4)+0.024], [0.755, 0.755], color=GREEN, lw=2)
ax.text((cx(1)+cx(4))/2, 0.772, "Year 1", fontsize=10, color=GREEN, ha="center", fontweight="bold")
ax.plot([cx(13)-0.024, cx(16)+0.024], [0.755, 0.755], color=CORAL, lw=2)
ax.text((cx(13)+cx(16))/2, 0.772, "Year 2", fontsize=10, color=CORAL, ha="center", fontweight="bold")
COND = [
    ("1", GREEN, "Teacher",
     "seen teaching in at least two YEAR-1 interviews, holding a bachelor’s degree or higher.\nTeaching was the occupation, not an episode."),
    ("2", BLUE, "Stayer",
     "seen teaching in at least one YEAR-2 interview."),
    ("3", CORAL, "Leaver",
     "never seen teaching in YEAR 2 — having at least two YEAR-2 interviews, at least one outside June–August."),
]
Y = 0.555
for num, c, lab, txt in COND:
    ax.add_patch(plt.Circle((0.063, Y - 0.012), 0.016, color=c))
    ax.text(0.063, Y - 0.012, num, fontsize=12, color="white", fontweight="bold",
            ha="center", va="center")
    ax.text(0.095, Y, lab, fontsize=13.5, fontweight="bold", color=c, va="top")
    ax.text(0.23, Y, txt, fontsize=11.5, color=INK, va="top")
    Y -= 0.092
ax.text(0.05, 0.275, "Anyone else is out of the sample: one teaching sighting only, or too few second-year interviews to convict.",
        fontsize=10.5, color=MUT, va="top")
ax.text(0.05, 0.238, "The degree requirement (BA+) keeps this universe identical to the rest of the deck — the March sample is college-graduate teachers too.",
        fontsize=10.5, color=MUT, va="top")
ax.text(0.05, 0.172, "Leaving rate under this definition:", fontsize=13,
        fontweight="bold", color=INK, va="top")
ax.text(0.375, 0.181, "13.0% per year", fontsize=19, fontweight="bold", color=BLUE, va="top")
ax.text(0.585, 0.172, "(2005–2024, 48,842 teachers, one verdict each)", fontsize=10.5, color=MUT, va="top")
ax.text(0.05, 0.09, "Identity across interviews: household and dwelling identifiers plus the person’s roster line, kept only if sex and race match and age advances 0–2 years.",
        fontsize=9.5, color=MUT, va="top")
save(fig, "u3_eight")

# ================= u3b: examples under the definition =================
fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.05, 0.945, "The definition, applied", fontsize=24,
        fontweight="bold", color=INK, va="top")
ax.text(0.05, 0.885, "Five cases, cell by cell — the three conditions decide everything.",
        fontsize=12.5, color=MUT, va="top")
LEG = [(BLUE, "seen teaching"), (CORAL, "year 2, not teaching"),
       (LGRAY, "interviewed, not teaching"), ("#EEF0F2", "not interviewed")]
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
    ax.add_patch(FancyBboxPatch((0.755, y + 0.002), 0.115, 0.048,
                 boxstyle="round,pad=0.002,rounding_size=0.008", facecolor=vc, edgecolor="none"))
    ax.text(0.8125, y + 0.026, verdict, fontsize=8.8, color="white",
            fontweight="bold", ha="center", va="center")
    ax.text(0.05, y - 0.019, caption, fontsize=9.2, color=INK, va="top", linespacing=1.3)
T  = (BLUE, "T", "white")
NG = (LGRAY, "–", MUT)
SY = (BLUE, "T", "white")
LV = (CORAL, "–", "white")
NO = ("#EEF0F2", "×", "#9AA1A8")
rows = [
 ({1:T,2:T,3:T,4:T, 13:SY,14:SY,15:SY,16:SY}, "STAYER", BLUE,
  "1 · Teaching at every interview: condition 1 met, condition 2 met → stayer."),
 ({1:T,2:T,3:T,4:T, 13:LV,14:LV,15:LV,16:SY}, "STAYER", BLUE,
  "2 · Silent at 13–15, teaching again at 16: one YEAR-2 sighting is enough (condition 2) → stayer."),
 ({1:T,2:T,3:NG,4:NG, 13:LV,14:LV,15:LV,16:LV}, "LEAVER", CORAL,
  "3 · Two YEAR-1 sightings (condition 1 met), four YEAR-2 interviews and never teaching (condition 3 met) → leaver."),
 ({1:T,2:NG,3:NG,4:NG, 13:LV,14:LV,15:LV,16:LV}, "NOT A TEACHER", "#7A828C",
  "4 · Seen teaching only once: condition 1 fails — teaching was an episode, not the occupation. Out of the denominator."),
 ({1:T,2:T,3:T,4:T, 13:NO,14:NO,15:NO,16:LV}, "NOT ENOUGH", "#7A828C",
  "5 · Only one YEAR-2 interview: condition 3 needs at least two to convict — out of the sample, not a leaver."),
]
y = 0.735
for cells, verdict, vc, cap in rows:
    strip(y, cells, verdict, vc, cap)
    y -= 0.125
ax.text(0.05, 0.095, "Nobody is convicted on one look, nobody is a teacher on one sighting — and each person appears exactly once.",
        fontsize=11.5, fontweight="bold", color=INK, va="top")
fig.savefig(f"{SC}/u3b_examples.png", dpi=160); plt.close(fig); print("saved u3b")

# ================= u3c: the rate + why the conditions matter =================
fig, ax = canvas("The rate, and why the conditions matter",
                 "Person-level leaving under the panel definition, 2005–2024")
c3 = fig.add_axes([0.07, 0.14, 0.50, 0.60])
c3.plot(F.base_year, F.leaver_final, color=CORAL, lw=2.6, solid_capstyle="round")
c3.plot(P.cal_year, P.leaver_ba, color=BLUE, lw=2.4)
c3.annotate("panel definition\nmean 13.0%", (2024, F.leaver_final.iloc[-1]),
            xytext=(8, 4), textcoords="offset points", fontsize=10.5,
            color=CORAL, fontweight="bold", va="center", linespacing=1.2)
c3.annotate("March recall\n7.7%", (2024, P.leaver_ba.iloc[-1]),
            xytext=(8, -6), textcoords="offset points", fontsize=10.5,
            color=BLUE, fontweight="bold", va="center", linespacing=1.2)
c3.set_xlim(1996.5, 2031); c3.set_ylim(0, 18)
c3.set_xticks(range(1997, 2025, 4))
c3.set_ylabel("percent of teachers leaving per year", fontsize=9.5, color=INK)
for s in ("top", "right"): c3.spines[s].set_visible(False)
c3.grid(axis="y", color="#F1F2F3", lw=1); c3.set_axisbelow(True)
c3.tick_params(labelsize=9)
c4 = fig.add_axes([0.66, 0.14, 0.30, 0.60])
grads = [("1 of 4", 55.0), ("2 of 4", 30.4), ("3 of 4", 17.3), ("4 of 4", 10.8)]
ys4 = np.arange(len(grads))[::-1]
for y, (lab, v) in zip(ys4, grads):
    c4.barh(y, v, height=0.55, color=CORAL, alpha=0.28 + 0.24 * y, zorder=3)
    c4.text(v + 1.2, y, f"{v:.0f}%", fontsize=11, color=INK, va="center", fontweight="bold")
    c4.text(-2, y, lab, fontsize=10, color=INK, va="center", ha="right")
c4.set_xlim(-14, 68); c4.set_ylim(-0.6, 3.6); c4.axis("off")
c4.set_title("leaving by year-1 interviews\nseen teaching (before condition 1)",
             fontsize=10, color=INK, loc="left")
ax.text(0.05, 0.08, "Condition 1 is what disciplines the rate: the one-sighting group leaves at 55% and would drag the mean from 13 to 18. "
        "Requiring two sightings is the whole fix — the summer and evidence conditions trim the rest.",
        fontsize=10.5, color=MUT, va="top")
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
ax.text(0.065, 0.395, "B — Linked monthly panel", fontsize=12.5, fontweight="bold", color=CORAL)
ax.text(0.065, 0.345, "Teacher: seen teaching in two or more first-year interviews.\nStayer: seen teaching in any second-year interview.\nLeaver: never seen teaching in year 2, on two or more\ninterviews with one outside the summer.",
        fontsize=10, color=INK, va="top", linespacing=1.45)
ax.text(0.065, 0.195, "2005–2024 · constructed link · one person, one verdict · 13.0%",
        fontsize=10, fontweight="bold", color=CORAL)
c5 = fig.add_axes([0.55, 0.14, 0.41, 0.64])
c5.axhspan(6.0, 8.4, color="#F0F2F4", zorder=0)
c5.plot(F.base_year, F.leaver_final, color=CORAL, lw=2.4)
c5.plot(P.cal_year, P.leaver_ba, color=BLUE, lw=2.4)
c5.annotate("B — 13.0%", (2024, F.leaver_final.iloc[-1]), xytext=(6, 0),
            textcoords="offset points", fontsize=11, color=CORAL, fontweight="bold", va="center")
c5.annotate("A — 7.7%", (2024, P.leaver_ba.iloc[-1]), xytext=(6, 0),
            textcoords="offset points", fontsize=11, color=BLUE, fontweight="bold", va="center")
c5.text(1997.5, 5.2, "band: published benchmarks 6–8.4", fontsize=8.5, color=MUT)
c5.set_xlim(1996.5, 2029.5); c5.set_ylim(0, 18)
c5.set_xticks(range(1997, 2025, 4))
c5.set_ylabel("percent leaving per year", fontsize=9.5, color=INK)
for s in ("top", "right"): c5.spines[s].set_visible(False)
c5.grid(axis="y", color="#F1F2F3", lw=1); c5.set_axisbelow(True)
c5.tick_params(labelsize=9)
ax.text(0.05, 0.075, "Both are correct about the thing they measure. The deck reports A — the March measure — because it is the one the published literature reports (benchmarks 6–8.4).",
        fontsize=10.5, color=MUT)
save(fig, "u4_twodefs")

# ================= u5: why 13 and 8 are both true =================
fig, ax = canvas("Why 13 and 8 are both true",
                 "The remaining gap between the two instruments is question and linkage, not error")
c6 = fig.add_axes([0.07, 0.18, 0.30, 0.58])
for x, v, c, lab in [(0, 13.0, CORAL, "Linked panel\ndefinition"),
                     (1, 7.7, BLUE, "March recall\n(this deck)")]:
    c6.bar(x, v, width=0.55, color=c, zorder=3)
    c6.text(x, v + 0.4, f"{v}", ha="center", fontsize=14, fontweight="bold", color=c)
    c6.text(x, -0.9, lab, ha="center", fontsize=10, color=INK, va="top",
            fontweight="bold", linespacing=1.2)
c6.set_xlim(-0.6, 1.6); c6.set_ylim(0, 15); c6.axis("off")
YR = 0.72
REASONS = [
    ("What counts as leaving", "Panel: never observed teaching across the second-year interviews — a point-in-time status, four times.\nMarch: the main teaching job of last year is gone by the interview. Part-year moves count in one, not the other."),
    ("Who is a teacher", "Panel: seen teaching at two monthly interviews. March: teaching was the longest job of the calendar year.\nThe March bar is still higher — closer to “a working teacher with a contract”."),
    ("Who survives the link", "The panel loses the 20% who move or stop answering, and movers leave more.\nMarch loses nobody: question and outcome sit in one record."),
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
c7 = fig.add_axes([0.10, 0.18, 0.80, 0.52])
rows6 = [("Washington payroll (Goldhaber–Theobald)", (6.0, 8.0), None, "#5E6672"),
         ("TFS roster follow-up, 2021–22", None, 8.4, "#5E6672"),
         ("Retrospective CPS (Aldeman–Yi 2025)", None, 7.6, "#5E6672"),
         ("This deck — March recall, 1997–2024", None, 7.7, BLUE),
         ("Linked monthly panel (different object)", None, 13.0, CORAL)]
yy = np.arange(len(rows6))[::-1]
for y, (lab, iv, pt, c) in zip(yy, rows6):
    if iv:
        c7.plot(iv, [y, y], color=c, lw=5, alpha=0.45, solid_capstyle="round")
        c7.text(iv[1] + 0.25, y, "6–8", fontsize=10.5, color=c, va="center", fontweight="bold")
    if pt:
        big = c in (BLUE, CORAL)
        c7.plot([pt], [y], "o", ms=13 if big else 9, color=c, mec="white", mew=1.6, zorder=5)
        c7.text(pt + 0.28, y, f"{pt}", fontsize=11.5 if big else 10.5,
                color=c, va="center", fontweight="bold")
    c7.text(3.6, y, lab, fontsize=11, color=c, ha="right", va="center",
            fontweight="bold" if c == BLUE else "normal")
c7.axvspan(6.0, 8.4, color="#F0F2F4", zorder=0)
c7.set_xlim(-8.5, 16); c7.set_ylim(-0.7, 4.7)
c7.set_xticks(range(4, 16, 2))
c7.tick_params(labelsize=9.5, left=False, labelleft=False)
for s in ("top", "right", "left"): c7.spines[s].set_visible(False)
c7.set_xlabel("teachers leaving per year, percent", fontsize=10, color=INK)
ax.text(0.05, 0.065, "Our March number sits inside the published band; the panel number sits outside it because it answers a different question. Comparability decides.",
        fontsize=10.5, color=MUT)
save(fig, "u6_whymarch")
print("final-rule panels done")


# ================= u2: identity (sober) =================
fig, ax = canvas("Is there a unique person ID across CPS waves?  No.",
                 "The CPS follows addresses, not people — so the person-level link has to be constructed")
for xc, tt in [(0.08, "Interview, month t"), (0.57, "Re-interview, month t + 12")]:
    rbox(ax, xc, 0.40, 0.36, 0.375, BLUE, alpha=0.045)
    ax.text(xc + 0.018, 0.725, tt, fontsize=13, fontweight="bold", color=INK)
    for dy, k, v in [(0.0, "Household identifier", "tied to the address, not the person"),
                     (0.062, "Dwelling identifier", "distinguishes households at one address"),
                     (0.124, "Person’s line number", "their slot on the household roster"),
                     (0.186, "Sex · race · age", "the person’s demographics")]:
        ax.text(xc + 0.018, 0.655 - dy, k, fontsize=10.5, fontweight="bold", color=BLUE)
        ax.text(xc + 0.175, 0.655 - dy, v, fontsize=8.8, color=MUT)
for dy, sym in [(0.0, "="), (0.062, "="), (0.124, "="), (0.186, "≈")]:
    ax.text(0.505, 0.655 - dy, sym, fontsize=15, fontweight="bold", color=INK, ha="center")
ax.text(0.505, 0.745, "must\nagree", fontsize=9, color=MUT, ha="center",
        style="italic", linespacing=1.2)
ax.text(0.05, 0.335, "The rule (Madrian–Lefgren):", fontsize=11.5, fontweight="bold", color=INK)
ax.text(0.05, 0.293, "declare “same person” when household, dwelling and roster line all coincide and the demographics are coherent —\nsex and race identical, age advancing 0 to 2 years. There is no true person identifier: this is the whole link.",
        fontsize=10.5, color=INK, va="top", linespacing=1.35)
ax.text(0.05, 0.195, "What can go wrong:", fontsize=11.5, fontweight="bold", color=INK)
ax.text(0.05, 0.153, "a family that moves is lost — and the new occupants of the address inherit its household identifier (the\ndemographic checks are what reject them). Matched share: teachers 78% · other graduates 74% · all employed 71%. The loss is non-random.",
        fontsize=10.5, color=INK, va="top", linespacing=1.35)
ax.text(0.05, 0.055, "The March recall design needs none of this: the teacher question and the outcome sit in the same interview.",
        fontsize=10.5, color=MUT, style="italic")
save(fig, "u2_identity")
