"""Worked examples: how each pair is judged in the linked monthly panel."""
import sys
sys.path.insert(0, "replication")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import paperstyle  # noqa: F401

SC = "report/figures_deck"
BLUE, CORAL, GREEN, GOLD = "#00549F", "#B5443C", "#3A8A62", "#D9A21B"
INK, MUT, LGRAY, GHOST = "#1A2430", "#6B7480", "#D9DDE2", "#F2F3F5"

fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.05, 0.945, "How each pair is judged — five worked examples",
        fontsize=24, fontweight="bold", color=INK, va="top")
ax.text(0.05, 0.885, "Month m is compared with month m+12 — and with nothing else. "
        "Every month you are seen teaching starts its own pair.",
        fontsize=12.5, color=MUT, va="top")

# legend
LEG = [(BLUE, "seen teaching (starts a pair)"), (GREEN, "anniversary: teaching → stayer"),
       (CORAL, "anniversary: not teaching → leaver"), (GOLD, "return caught after the verdict"),
       (LGRAY, "interviewed, no role in any verdict")]
lx = 0.05
for c, lab in LEG:
    ax.add_patch(FancyBboxPatch((lx, 0.822), 0.016, 0.026,
                 boxstyle="round,pad=0.001,rounding_size=0.004", facecolor=c, edgecolor="none"))
    ax.text(lx + 0.022, 0.835, lab, fontsize=8.6, color=INK, va="center")
    lx += 0.028 + len(lab) * 0.0052

X0, CW, GAP = 0.05, 0.0405, 0.0035
def cxm(m): return X0 + (m-1) * (CW + GAP)

# each cell: (fill, letter, letter_color, edge)
def strip(y, cells, caption, cap_color=INK):
    for m in range(1, 17):
        fill, letter, lc, edge = cells.get(m, (GHOST, "", MUT, "none"))
        ax.add_patch(FancyBboxPatch((cxm(m), y), CW, 0.055,
                     boxstyle="round,pad=0.0015,rounding_size=0.006",
                     facecolor=fill, edgecolor=edge, lw=1.4))
        ax.text(cxm(m) + CW/2, y + 0.0275, letter or str(m), fontsize=8.5 if letter else 7,
                fontweight="bold" if letter else "normal",
                ha="center", va="center", color=lc if letter else "#B9BfC7")
    ax.text(0.05, y - 0.021, caption, fontsize=9.3, color=cap_color, va="top", linespacing=1.35)

T  = (BLUE, "T", "white", "none")          # teaching, first year (baseline)
NG = (LGRAY, "–", MUT, "none")             # interviewed, not teaching, irrelevant
TG = (LGRAY, "T", MUT, "none")             # teaching but irrelevant to any verdict
SY = (GREEN, "T", "white", "none")         # anniversary, teaching -> stayer
LV = (CORAL, "–", "white", "none")         # anniversary, not teaching -> leaver
RC = (GOLD, "T", "white", "none")          # return caught

rows = [
 ({1:T,2:T,3:T,4:T, 13:SY,14:SY,15:SY,16:SY},
  "1 · Teacher at all four first-year interviews, teaching at all four anniversaries → four pairs, four stayers."),
 ({1:T,2:NG,3:NG,4:NG, 13:LV,14:NG,15:NG,16:RC},
  "2 · YOUR CASE — teacher only in month 1; saying “not a teacher” in months 2–4 creates no pairs. The only verdict is at month 13:\n"
  "     not teaching there → 12-month leaver. Teaching again at month 16 → a return, so dropped from the persistent rate."),
 ({1:T,2:T,3:NG,4:NG, 13:SY,14:LV,15:NG,16:NG},
  "3 · Teacher in months 1 and 2 → two pairs. Pair 1→13: stayer. Pair 2→14: leaver (not teaching at 15–16 either → persistent). One person, one of each."),
 ({1:NG,2:T,3:NG,4:NG, 13:TG,14:SY,15:NG,16:NG},
  "4 · Teacher only in month 2 → judged at month 14 only: teaching → stayer. Month 13 shows teaching and months 15–16 show nothing — none of that enters any verdict."),
 ({1:T,2:T,3:T,4:T, 13:LV,14:LV,15:LV,16:LV},
  "5 · Teacher at all four, never teaching in year two → four leaver pairs, and no return in sight → persistent leaver."),
]
y = 0.735
for cells, cap in rows:
    strip(y, cells, cap)
    y -= 0.128

ax.text(0.05, 0.085, "So, no:", fontsize=12, fontweight="bold", color=CORAL)
ax.text(0.115, 0.085, "“teacher in any of the first four, not teaching in any of the last four” is NOT the rule. "
        "The verdict lives in one cell: month m against month m+12.",
        fontsize=11, color=INK)
ax.text(0.05, 0.042, "The annual rate is a weighted rate over pairs, not over people — a person can contribute up to four pairs, and be a stayer in one and a leaver in another.",
        fontsize=10, color=MUT, style="italic")
fig.savefig(f"{SC}/u3b_examples.png", dpi=160)
print("saved u3b")
