"""Six visual technical-appendix slides, full-bleed 13.33x7.5in panels."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
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

def chart(title, subtitle, rect=(0.07, 0.14, 0.86, 0.60)):
    fig, ax = canvas(title, subtitle)
    return fig, ax, fig.add_axes(rect)

def save(fig, name):
    fig.savefig(f"{SC}/{name}.png", dpi=160); plt.close(fig); print("saved", name)

E = pd.read_csv("outputs/evolution_by_year_gender.csv")
P = pd.read_csv("outputs/p_series.csv")

# ============ 1. codes crosswalk ============
fig, ax = canvas("Who counts as a teacher",
                 "Occupation of the longest job held last year, CPS ASEC — three Census classifications, 28 surveys")
ERAS = [("SURVEYS 1998–2002", "1990 classification", 0.175, 0.425),
        ("SURVEYS 2003–2019", "2002/2010 classification (SOC)", 0.455, 0.705),
        ("SURVEYS 2020–2025", "2018 classification (SOC 2018)", 0.735, 0.985)]
LANES = [
    ("Pre-K &\nkindergarten", GOLD,
     [("155", "Teachers, prekindergarten\nand kindergarten"),
      ("2300", "Preschool and\nkindergarten teachers"),
      ("2300", "Preschool and\nkindergarten teachers")]),
    ("Elementary\n& middle †", BLUE,
     [("156", "Teachers,\nelementary school †"),
      ("2310", "Elementary and middle\nschool teachers"),
      ("2310", "Elementary and middle\nschool teachers")]),
    ("Secondary", GREEN,
     [("157", "Teachers,\nsecondary school †"),
      ("2320", "Secondary school\nteachers"),
      ("2320", "Secondary school\nteachers")]),
    ("Special\neducation", CORAL,
     [("158", "Teachers,\nspecial education"),
      ("2330", "Special education\nteachers"),
      ("2330", "Special education\nteachers")]),
    ("Other\nteachers", "#5E6672",
     [("159", "Teachers, n.e.c."),
      ("2340", "Other teachers\nand instructors"),
      ("2360", "Other teachers\nand instructors")]),
]
ys = [0.685, 0.575, 0.465, 0.355, 0.245]; H = 0.092
for name, sub, x0, x1 in ERAS:
    xm = (x0 + x1) / 2
    ax.text(xm, 0.812, name, fontsize=12, fontweight="bold", color=INK, ha="center")
    ax.text(xm, 0.782, sub, fontsize=9.5, style="italic", color=MUT, ha="center")
for xs in (0.44, 0.72):
    ax.plot([xs, xs], [0.19, 0.80], ls=(0, (2, 3)), color="#B9C0C8", lw=1.1)
ax.text(0.44, 0.168, "2003 reclassification", fontsize=8.5, color=MUT, ha="center")
ax.text(0.72, 0.168, "2020 reclassification", fontsize=8.5, color=MUT, ha="center")
for (lab, c, cells), y in zip(LANES, ys):
    ax.text(0.148, y + H/2, lab, fontsize=10.5, fontweight="bold", color=c,
            ha="right", va="center", linespacing=1.1)
    for (code, txt), (_, _, x0, x1) in zip(cells, ERAS):
        ax.add_patch(FancyBboxPatch((x0, y), x1-x0, H,
                     boxstyle="round,pad=0.004,rounding_size=0.012",
                     facecolor=c, alpha=0.10, edgecolor=c, lw=1.1))
        ax.text(x0 + 0.014, y + H/2, code, fontsize=13, fontweight="bold",
                color=c, va="center")
        ax.text(x0 + 0.07, y + H/2, txt, fontsize=8.4, color=INK, va="center",
                linespacing=1.15)
    for i in range(2):
        xa = ERAS[i][3] + 0.004; xb = ERAS[i+1][2] - 0.004
        ax.annotate("", xy=(xb, y + H/2), xytext=(xa, y + H/2),
                    arrowprops=dict(arrowstyle="-", color=c, lw=1.2, alpha=0.55))
ax.text(0.05, 0.105, "Traceable as a block: the K–12 teaching group maps one-to-one across the three classifications — every figure uses the union, never a sub-code across regimes.",
        fontsize=10, color=INK)
ax.text(0.05, 0.066, "† middle-school teachers sit under elementary or secondary before 2003, with elementary (2310) after.",
        fontsize=9, color=MUT)
ax.text(0.05, 0.034, "Never included: postsecondary (2200s) · tutors (2350) · teaching assistants (2540/2545) · childcare workers (4600) · administrators (0230).",
        fontsize=9, color=MUT)
save(fig, "t1_codes")

# ============ 2. the synthetic link ============
fig, ax = canvas("The synthetic link",
                 "CPS 4-8-4 rotation: the same address is interviewed 4 months, rests 8, and returns — one year later exactly")
x0, cw, gap = 0.065, 0.0525, 0.004
y0, ch = 0.47, 0.115
for m in range(1, 17):
    x = x0 + (m-1) * (cw + gap)
    inn = m <= 4 or m >= 13
    c = BLUE if inn else LGRAY
    ax.add_patch(FancyBboxPatch((x, y0), cw, ch,
                 boxstyle="round,pad=0.002,rounding_size=0.008",
                 facecolor=c, edgecolor="none"))
    ax.text(x + cw/2, y0 + ch/2, str(m), fontsize=11.5, fontweight="bold",
            ha="center", va="center", color="white" if inn else MUT)
cx = lambda m: x0 + (m-1) * (cw + gap) + cw/2
ax.text(cx(2.5), y0 - 0.045, "interviewed (MIS 1–4)", fontsize=9.5, color=MUT, ha="center")
ax.text(cx(8.5), y0 - 0.045, "not interviewed (8 months)", fontsize=9.5, color=MUT, ha="center")
ax.text(cx(14.5), y0 - 0.045, "interviewed again (MIS 5–8)", fontsize=9.5, color=MUT, ha="center")
# leaver badges
ax.add_patch(FancyBboxPatch((cx(1.5)-0.062, 0.665), 0.124, 0.05,
             boxstyle="round,pad=0.003,rounding_size=0.01", facecolor=GREEN, edgecolor="none"))
ax.text(cx(1.5), 0.69, "teacher in month t", fontsize=8.6, color="white",
        fontweight="bold", ha="center", va="center")
ax.add_patch(FancyBboxPatch((cx(13.5)-0.098, 0.665), 0.196, 0.05,
             boxstyle="round,pad=0.003,rounding_size=0.01", facecolor=CORAL, edgecolor="none"))
ax.text(cx(13.5), 0.69, "not teaching at t+12  →  leaver", fontsize=8.6, color="white",
        fontweight="bold", ha="center", va="center")
ax.annotate("", xy=(cx(13.5)-0.101, 0.69), xytext=(cx(1.5)+0.065, 0.69),
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
ax.text((cx(1.5)+cx(13.5))/2, 0.723, "the 12-month link", fontsize=10.5,
        fontweight="bold", color=INK, ha="center")
ax.annotate("", xy=(cx(16)+0.02, 0.625), xytext=(cx(13.6), 0.625),
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=2.2))
ax.text(cx(14.9), 0.645, "return window (≤3 months)", fontsize=9, color=INK, ha="center")
ax.text(0.05, 0.352, "Who is matched:", fontsize=11, fontweight="bold", color=BLUE)
ax.text(0.05, 0.310, "same household and person identifiers (HRHHID · HRHHID2 · PULINENO) in both interviews,\nkept only if sex and race agree and age advances 0–2 years (Madrian–Lefgren).",
        fontsize=10.5, color=INK, va="top", linespacing=1.35)
ax.text(0.05, 0.226, "Who is a leaver:", fontsize=11, fontweight="bold", color=CORAL)
ax.text(0.05, 0.184, "a teacher at month t who is not teaching at the re-interview twelve months later. If the return window\nshows them teaching again — 16% of leavers do within three months — they drop from the persistent rate.",
        fontsize=10.5, color=INK, va="top", linespacing=1.35)
ax.text(0.05, 0.100, "The price:", fontsize=11, fontweight="bold", color=INK)
ax.text(0.05, 0.058, "matched share averages 78% for teachers (74% other graduates, 71% all employed) — the loss is non-random.\nAnd HRHHID2 exists only from May 2004: no linked panel before 2005, none reaching 1997. The March recall design needs no link at all.",
        fontsize=10.5, color=MUT, va="top", linespacing=1.35)
save(fig, "t2_link")

# ============ 3. the rate under the richer design ============
fig, ax, cx3 = chart("What the richer design measured",
                     "Linked monthly panel, every month 2005–2025 — share of teachers not teaching at the re-interview a year later")
cx3.plot(E.base_year, E.attr12_all, color=CORAL, lw=2.6, solid_capstyle="round")
cx3.plot(E.base_year, E.attrp_all, color=GREEN, lw=2.2, solid_capstyle="round")
cx3.annotate(f"12-month leaver — mean 15.4%", (2024, E.attr12_all.iloc[-1]),
             xytext=(8, 8), textcoords="offset points", fontsize=11, color=CORAL, fontweight="bold")
cx3.annotate(f"persistent (never returns\nin the window) — mean 13.1%", (2024, E.attrp_all.iloc[-1]),
             xytext=(8, -26), textcoords="offset points", fontsize=11, color=GREEN, fontweight="bold")
cx3.set_xlim(2004.5, 2029); cx3.set_ylim(0, 21)
cx3.set_xticks(range(2005, 2025, 2))
cx3.set_ylabel("percent of teachers, base year t", fontsize=10, color=INK)
for s in ("top", "right"): cx3.spines[s].set_visible(False)
cx3.grid(axis="y", color="#F1F2F3", lw=1); cx3.set_axisbelow(True)
cx3.tick_params(labelsize=9.5)
ax.text(0.05, 0.055, "Twelve measurements per year instead of one — and a rate around fifteen, double the published numbers. That gap is the next slide.",
        fontsize=10.5, color=MUT)
save(fig, "t3_richrate")

# ============ 4. side by side ============
fig, ax, cx4 = chart("Two instruments, two levels",
                     "The linked panel and the March recall question, on the same axis")
cx4.axhspan(6.0, 8.4, color="#F0F2F4", zorder=0)
cx4.text(1997.2, 5.2, "shaded band: published benchmarks — WA payroll 6–8 · Aldeman–Yi 7.6 · TFS 8.4",
         fontsize=9, color=MUT)
cx4.plot(E.base_year, E.attr12_all, color=CORAL, lw=2.4)
cx4.plot(P.cal_year, P.leaver_ba, color=BLUE, lw=2.6)
cx4.plot([1997, 2024.5], [7.7, 7.7], color=BLUE, lw=0.9, ls=(0, (4, 4)), alpha=0.55)
cx4.annotate("linked panel, 12-month — 15.4%", (2024, E.attr12_all.iloc[-1]),
             xytext=(8, 0), textcoords="offset points", fontsize=11, color=CORAL,
             fontweight="bold", va="center")
cx4.annotate("March recall (this deck) — 7.7%", (2024, P.leaver_ba.iloc[-1]),
             xytext=(8, 0), textcoords="offset points", fontsize=11, color=BLUE,
             fontweight="bold", va="center")
cx4.set_xlim(1996.5, 2032); cx4.set_ylim(0, 21)
cx4.set_xticks(range(1997, 2025, 3))
cx4.set_ylabel("percent of teachers leaving per year", fontsize=10, color=INK)
for s in ("top", "right"): cx4.spines[s].set_visible(False)
cx4.grid(axis="y", color="#F1F2F3", lw=1); cx4.set_axisbelow(True)
cx4.tick_params(labelsize=9.5)
ax.text(0.05, 0.055, "Same files, same teachers, same country — the level tracks the instrument. The published literature sits on the recall side.",
        fontsize=10.5, color=MUT)
save(fig, "t4_compare")

# ============ 5. why the difference: bridge ============
fig, ax, cx5 = chart("Why the difference",
                     "From the point-in-time re-interview to the recall question, step by step",
                     rect=(0.07, 0.20, 0.86, 0.56))
steps = [("Linked panel\n12-month rate", 0, 15.4, CORAL),
         ("short-run returners:\n16% of leavers teach\nagain within 3 months", 15.4, 13.1, GOLD),
         ("Persistent rate", 0, 13.1, CORAL),
         ("different question:\nstatus this week vs the main\njob of last year — summer\ntiming, temporary absences,\nshort teaching spells", 13.1, 7.7, "#9AA1A8"),
         ("March recall\n(this deck)", 0, 7.7, BLUE)]
xs5 = np.arange(5)
for x, (lab, a, b, c) in zip(xs5, steps):
    lo, hi = min(a, b), max(a, b)
    full = a == 0
    cx5.bar(x, hi - lo, bottom=lo, width=0.58, color=c,
            alpha=1.0 if full else 0.45, zorder=3,
            edgecolor="none" if full else c, lw=0 if full else 1.2)
    val = b if full else a - b
    cx5.text(x, hi + 0.5, f"{b:.1f}" if full else f"–{val:.1f}",
             ha="center", fontsize=13, fontweight="bold", color=c)
    if full:
        cx5.text(x, -0.9, lab, ha="center", fontsize=9.6, color=INK, va="top",
                 fontweight="bold", linespacing=1.15)
    else:
        cx5.text(x, lo - 1.0, lab, ha="center", fontsize=8.6, color=MUT,
                 va="top", linespacing=1.2)
for x, lev in [(0.5, 13.1), (2.5, 7.7)]:
    pass
cx5.plot([0.29, 1.29], [15.4, 15.4], ls=(0, (2, 2)), color="#C6CBD1", lw=1)
cx5.plot([1.29, 2.29], [13.1, 13.1], ls=(0, (2, 2)), color="#C6CBD1", lw=1)
cx5.plot([2.29, 3.29], [13.1, 13.1], ls=(0, (2, 2)), color="#C6CBD1", lw=1)
cx5.plot([3.29, 4.29], [7.7, 7.7], ls=(0, (2, 2)), color="#C6CBD1", lw=1)
cx5.set_xlim(-0.6, 4.6); cx5.set_ylim(0, 18)
cx5.axis("off")
ax.text(0.05, 0.045, "The first step is measured in our own panel; the second is the change of object — both instruments are right about the thing they measure.",
        fontsize=10.5, color=MUT)
save(fig, "t5_bridge")

# ============ 6. why march ============
fig, ax, cx6 = chart("Why we keep the March question",
                     "One reason: it is the literature’s measure — every published benchmark is directly comparable",
                     rect=(0.10, 0.18, 0.80, 0.52))
rows6 = [("Washington payroll (Goldhaber–Theobald)", (6.0, 8.0), None, "#5E6672"),
         ("TFS roster follow-up, 2021–22", None, 8.4, "#5E6672"),
         ("Retrospective CPS (Aldeman–Yi 2025)", None, 7.6, "#5E6672"),
         ("This deck — March recall, 1997–2024", None, 7.7, BLUE),
         ("Linked monthly panel (different object)", None, 15.4, CORAL)]
yy = np.arange(len(rows6))[::-1]
for y, (lab, iv, pt, c) in zip(yy, rows6):
    if iv:
        cx6.plot(iv, [y, y], color=c, lw=5, alpha=0.45, solid_capstyle="round")
        cx6.text(iv[1] + 0.25, y, "6–8", fontsize=10.5, color=c, va="center", fontweight="bold")
    if pt:
        big = c in (BLUE, CORAL)
        cx6.plot([pt], [y], "o", ms=13 if big else 9, color=c,
                 mec="white", mew=1.6, zorder=5)
        cx6.text(pt + 0.32, y, f"{pt}", fontsize=11.5 if big else 10.5,
                 color=c, va="center", fontweight="bold")
    cx6.text(3.6, y, lab, fontsize=11, color=c, ha="right", va="center",
             fontweight="bold" if c == BLUE else "normal")
cx6.axvspan(6.0, 8.4, color="#F0F2F4", zorder=0)
cx6.set_xlim(-8, 18); cx6.set_ylim(-0.7, 4.7)
cx6.set_xticks(range(4, 18, 2))
cx6.tick_params(labelsize=9.5, left=False, labelleft=False)
for s in ("top", "right", "left"): cx6.spines[s].set_visible(False)
cx6.set_xlabel("teachers leaving per year, percent", fontsize=10, color=INK)
ax.text(0.05, 0.065, "Our March number sits inside the published band; the linked panel sits far outside it because it answers a different question. Comparability decides.",
        fontsize=10.5, color=MUT)
save(fig, "t6_whymarch")
print("all done")
