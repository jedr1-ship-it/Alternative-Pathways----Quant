"""Didactic technical slides v3 — panels 2-6 (panel 1 is native pptx)."""
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
INK, MUT, LGRAY = "#1A2430", "#6B7480", "#E5E8EC"

def canvas(title, subtitle):
    fig = plt.figure(figsize=(13.33, 7.5))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.05, 0.935, title, fontsize=25, fontweight="bold", color=INK, va="top")
    ax.text(0.05, 0.872, subtitle, fontsize=12.5, color=MUT, va="top")
    return fig, ax

def save(fig, name):
    fig.savefig(f"{SC}/{name}.png", dpi=160); plt.close(fig); print("saved", name)

def box(ax, x, y, w, h, c, alpha=0.08, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.004,rounding_size=0.012",
                 facecolor=c, alpha=alpha, edgecolor=c, lw=lw))

E = pd.read_csv("outputs/evolution_by_year_gender.csv")
P = pd.read_csv("outputs/p_series.csv")

# ===== 2. no unique person ID: the constructed link =====
fig, ax = canvas("Is there a unique person ID across CPS waves?  No.",
                 "The CPS follows addresses, not people — so the person-level link has to be constructed")
for xc, tt in [(0.08, "Interview, month t"), (0.57, "Re-interview, month t + 12")]:
    box(ax, xc, 0.40, 0.36, 0.375, BLUE, alpha=0.05)
    ax.text(xc + 0.018, 0.725, tt, fontsize=13, fontweight="bold", color=BLUE)
    for dy, k, v in [(0.0, "HRHHID", "household identifier — tied to the address"),
                     (0.062, "HRHHID2", "household id, part 2 (born May 2004)"),
                     (0.124, "PULINENO", "person line number in the household"),
                     (0.186, "sex·race·age", "the person’s demographics")]:
        ax.text(xc + 0.018, 0.655 - dy, k, fontsize=10.5, fontweight="bold",
                color=INK, family="monospace")
        ax.text(xc + 0.138, 0.655 - dy, v, fontsize=8.8, color=MUT)
for dy, sym, c in [(0.0, "=", GREEN), (0.062, "=", GREEN), (0.124, "=", GREEN),
                   (0.186, "≈", GOLD)]:
    ax.text(0.505, 0.655 - dy, sym, fontsize=15, fontweight="bold", color=c, ha="center")
ax.text(0.505, 0.745, "must\nagree", fontsize=9, color=GREEN, ha="center", style="italic", linespacing=1.2)
ax.text(0.05, 0.335, "The rule (Madrian–Lefgren):", fontsize=11.5, fontweight="bold", color=GREEN)
ax.text(0.05, 0.293, "declare “same person” when all three identifiers coincide and the demographics are coherent —\nsex and race identical, age advancing 0 to 2 years. There is no true person key: this is the whole link.",
        fontsize=10.5, color=INK, va="top", linespacing=1.35)
ax.text(0.05, 0.195, "What can go wrong:", fontsize=11.5, fontweight="bold", color=CORAL)
ax.text(0.05, 0.153, "a family that moves is lost — and the new occupants of the address inherit its HRHHID (the demographic\nchecks are what reject them). Matched share: teachers 78% · other graduates 74% · all employed 71%. The loss is non-random.",
        fontsize=10.5, color=INK, va="top", linespacing=1.35)
ax.text(0.05, 0.055, "The March recall design needs none of this: the teacher question and the outcome sit in the same interview.",
        fontsize=10.5, color=MUT, style="italic")
save(fig, "u2_identity")

# ===== 3. how the panel leaver is built (8 interviews) =====
fig, ax = canvas("Eight interviews, one verdict per pair",
                 "A person is interviewed 4 months, rests 8, and is interviewed 4 more — each first-year month meets its own anniversary")
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
for m in range(1, 5):
    ax.annotate("", xy=(cx(m+12), y0 + ch + 0.010), xytext=(cx(m), y0 + ch + 0.010),
                arrowprops=dict(arrowstyle="->", color="#C8CDD3" if m != 2 else INK,
                                lw=1.0 if m != 2 else 1.8,
                                connectionstyle="arc3,rad=-0.085"))
ax.text(cx(8.5), 0.815, "each first-year month meets its own anniversary, one year later (MIS m → MIS m+4)",
        fontsize=9, color=MUT, ha="center")
ax.add_patch(FancyBboxPatch((cx(2)-0.045, 0.505), 0.09, 0.042,
             boxstyle="round,pad=0.003,rounding_size=0.01", facecolor=GREEN, edgecolor="none"))
ax.text(cx(2), 0.526, "teacher here", fontsize=8.2, color="white", fontweight="bold",
        ha="center", va="center")
ax.add_patch(FancyBboxPatch((cx(14)-0.067, 0.505), 0.134, 0.042,
             boxstyle="round,pad=0.003,rounding_size=0.01", facecolor=CORAL, edgecolor="none"))
ax.text(cx(14), 0.526, "judged here — only here", fontsize=8.0, color="white",
        fontweight="bold", ha="center", va="center")
ax.annotate("", xy=(cx(16)+0.022, 0.526), xytext=(cx(14)+0.072, 0.526),
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=2.0))
ax.text(cx(15.7), 0.487, "return window", fontsize=8.2, color=GOLD, ha="center", fontweight="bold")
Y = 0.375
ax.text(0.05, Y, "1.", fontsize=12, fontweight="bold", color=BLUE)
ax.text(0.075, Y, "Being a teacher at one first-year interview is enough — that month becomes a baseline. Nobody needs to be a teacher in all four.",
        fontsize=10.5, color=INK)
ax.text(0.05, Y-0.055, "2.", fontsize=12, fontweight="bold", color=CORAL)
ax.text(0.075, Y-0.055, "Leaver is decided at the single anniversary interview: teaching there → stayer; not teaching there → 12-month leaver. Never “any of the four”.",
        fontsize=10.5, color=INK)
ax.text(0.05, Y-0.110, "3.", fontsize=12, fontweight="bold", color=GOLD)
ax.text(0.075, Y-0.110, "The interviews after the anniversary (up to 3) only serve to catch returns: a leaver seen teaching again is dropped from the persistent rate.",
        fontsize=10.5, color=INK)
ax.text(0.05, Y-0.165, "4.", fontsize=12, fontweight="bold", color=MUT)
ax.text(0.075, Y-0.165, "The persistent rate therefore uses baselines MIS 1–3, so at least one interview exists after the verdict. One person can contribute several pairs.",
        fontsize=10.5, color=INK)
ax.text(0.05, 0.075, "12-month rate 15.4% · persistent rate 13.1% (2005–2025) — 16% of 12-month leavers are teaching again within three months.",
        fontsize=10.5, color=MUT, style="italic")
save(fig, "u3_eight")

# ===== 4. two definitions + the chart =====
fig, ax = canvas("Two ways to define a leaver",
                 "Same CPS files, two instruments — and the level tracks the instrument")
box(ax, 0.05, 0.52, 0.42, 0.27, BLUE, alpha=0.05)
ax.text(0.065, 0.755, "A — March recall (this deck)", fontsize=12.5, fontweight="bold", color=BLUE)
ax.text(0.065, 0.705, "Teacher: the longest job held last calendar year was teaching\n(one recall question, same record).\nLeaver: at the March interview that job is gone — switched\noccupation, unemployed, or out of the labor force.",
        fontsize=10, color=INK, va="top", linespacing=1.45)
ax.text(0.065, 0.555, "1997–2024 · no link needed · mean 7.7%", fontsize=10,
        fontweight="bold", color=BLUE)
box(ax, 0.05, 0.16, 0.42, 0.27, CORAL, alpha=0.05)
ax.text(0.065, 0.395, "B — Linked monthly panel", fontsize=12.5, fontweight="bold", color=CORAL)
ax.text(0.065, 0.345, "Teacher: teaching at a first-year interview (any month).\nLeaver: not teaching at the single anniversary re-interview\ntwelve months later; persistent if never seen teaching again\nin the return window.",
        fontsize=10, color=INK, va="top", linespacing=1.45)
ax.text(0.065, 0.195, "2005–2025 · constructed link · mean 15.4% (13.1% persistent)",
        fontsize=10, fontweight="bold", color=CORAL)
c4 = fig.add_axes([0.55, 0.14, 0.41, 0.64])
c4.axhspan(6.0, 8.4, color="#F0F2F4", zorder=0)
c4.plot(E.base_year, E.attr12_all, color=CORAL, lw=2.4)
c4.plot(P.cal_year, P.leaver_ba, color=BLUE, lw=2.4)
c4.annotate("B — 15.4%", (2024, E.attr12_all.iloc[-1]), xytext=(6, 0),
            textcoords="offset points", fontsize=11, color=CORAL, fontweight="bold", va="center")
c4.annotate("A — 7.7%", (2024, P.leaver_ba.iloc[-1]), xytext=(6, 0),
            textcoords="offset points", fontsize=11, color=BLUE, fontweight="bold", va="center")
c4.text(1997.5, 5.2, "band: published benchmarks 6–8.4", fontsize=8.5, color=MUT)
c4.set_xlim(1996.5, 2029.5); c4.set_ylim(0, 20)
c4.set_xticks(range(1997, 2025, 4))
c4.set_ylabel("percent leaving per year", fontsize=9.5, color=INK)
for s in ("top", "right"): c4.spines[s].set_visible(False)
c4.grid(axis="y", color="#F1F2F3", lw=1); c4.set_axisbelow(True)
c4.tick_params(labelsize=9)
ax.text(0.05, 0.075, "Both are correct about the thing they measure: B counts any month spent away from teaching; A counts durable exits from the year’s main job.",
        fontsize=10.5, color=MUT)
save(fig, "u4_twodefs")

# ===== 5. bridge =====
fig, ax = canvas("Why the difference",
                 "From the point-in-time re-interview to the recall question, step by step")
cx5 = fig.add_axes([0.07, 0.20, 0.86, 0.56])
steps = [("Linked panel\n12-month rate", 0, 15.4, CORAL),
         ("short-run returners:\n16% of leavers teach\nagain within 3 months", 15.4, 13.1, GOLD),
         ("Persistent rate", 0, 13.1, CORAL),
         ("different question:\nstatus this week vs the main\njob of last year — summer\ntiming, temporary absences,\nshort teaching spells", 13.1, 7.7, "#9AA1A8"),
         ("March recall\n(this deck)", 0, 7.7, BLUE)]
for x, (lab, a, b, c) in zip(np.arange(5), steps):
    lo, hi = min(a, b), max(a, b)
    full = a == 0
    cx5.bar(x, hi - lo, bottom=lo, width=0.58, color=c,
            alpha=1.0 if full else 0.45, zorder=3,
            edgecolor="none" if full else c, lw=0 if full else 1.2)
    cx5.text(x, hi + 0.5, f"{b:.1f}" if full else f"–{a-b:.1f}",
             ha="center", fontsize=13, fontweight="bold", color=c)
    if full:
        cx5.text(x, -0.9, lab, ha="center", fontsize=9.6, color=INK, va="top",
                 fontweight="bold", linespacing=1.15)
    else:
        cx5.text(x, lo - 1.0, lab, ha="center", fontsize=8.6, color=MUT,
                 va="top", linespacing=1.2)
for xa, lev in [(0.29, 15.4), (1.29, 13.1), (2.29, 13.1), (3.29, 7.7)]:
    cx5.plot([xa, xa+1], [lev, lev], ls=(0, (2, 2)), color="#C6CBD1", lw=1)
cx5.set_xlim(-0.6, 4.6); cx5.set_ylim(0, 18); cx5.axis("off")
ax.text(0.05, 0.045, "The first step is measured in our own panel; the second is the change of object — both instruments are right about the thing they measure.",
        fontsize=10.5, color=MUT)
save(fig, "u5_bridge")

# ===== 6. why march =====
fig, ax = canvas("Why we keep the March question",
                 "One reason: it is the literature’s measure — every published benchmark is directly comparable")
c6 = fig.add_axes([0.10, 0.18, 0.80, 0.52])
rows6 = [("Washington payroll (Goldhaber–Theobald)", (6.0, 8.0), None, "#5E6672"),
         ("TFS roster follow-up, 2021–22", None, 8.4, "#5E6672"),
         ("Retrospective CPS (Aldeman–Yi 2025)", None, 7.6, "#5E6672"),
         ("This deck — March recall, 1997–2024", None, 7.7, BLUE),
         ("Linked monthly panel (different object)", None, 15.4, CORAL)]
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
c6.set_xlim(-8, 18); c6.set_ylim(-0.7, 4.7)
c6.set_xticks(range(4, 18, 2))
c6.tick_params(labelsize=9.5, left=False, labelleft=False)
for s in ("top", "right", "left"): c6.spines[s].set_visible(False)
c6.set_xlabel("teachers leaving per year, percent", fontsize=10, color=INK)
ax.text(0.05, 0.065, "Our March number sits inside the published band; the linked panel sits far outside it because it answers a different question. Comparability decides.",
        fontsize=10.5, color=MUT)
save(fig, "u6_whymarch")
print("panels done")
