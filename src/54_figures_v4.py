"""
Figure set v4: implements every figure fix in the referee report.
g1 raw+smoothed workforce panels with labels outside the data area;
g2 three-series evolution with CI ribbon, visible gaps, harmonized
   old-style overlap and the H&A band tied to the comparable series;
g3 flow-of-100 with ONE education-and-care definition in both panels and
   an explicit Unclassified bar; g4 route bands labeled in the margin;
g5 three earnings distributions plus the zero-earnings block; g6 grouped
coefficient plot with background bands (no rotated-text collisions,
significance by fill vs outline); g7 professions dumbbell with H&A
anchors and half-up labels; g8 eight-profession new-baby panel.
"""
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "src")
from paperstyle import BLUE, CORAL, GOLD, GREEN, GRAY, INK, SUBTLE  # noqa

FIG = "report/figures"
LIGHT = "#AEC3DE"
DARK = "#3D4754"


def h1(v):
    """half-up to one decimal, as a string"""
    return f"{math.floor(v * 10 + 0.5) / 10:.1f}"


def despine(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# ================ G1 workforce ================
WF = pd.read_csv("outputs/p_workforce.csv").sort_values("cal_year")
panels = [("age", "Mean age (years)", 2005), ("female", "Female", 2005),
          ("ma_plus", "Master's or higher", 2005),
          ("black", "Black", 2005),
          ("child_u6", "Child under 6", 2005),
          ("public", "Public school", 2005),
          ("parttime", "Part-time", 2005),
          ("pension", "Pension plan", 2005)]
fig, axes = plt.subplots(2, 4, figsize=(11.8, 5.6))
for axp, (v, lab, start) in zip(axes.flat, panels):
    d = WF[(WF["cal_year"] >= start) & WF[v].notna()]
    y = d[v].astype(float).reset_index(drop=True)
    xs = d["cal_year"].reset_index(drop=True)
    sm3 = y.rolling(3, center=True, min_periods=2).mean()
    axp.plot(xs, y, color="#BBBBBB", lw=1.0)
    axp.plot(xs, sm3, color=BLUE, lw=2.2)
    i13 = xs == 2013
    axp.plot(xs[i13], y[i13], "o", mfc="white", mec=GRAY, ms=4)
    axp.set_title(lab, fontsize=10, color=INK, pad=6)
    lo, hi = y.min(), y.max()
    pad = max((hi - lo) * 0.35, 0.8)
    axp.set_ylim(lo - pad, hi + pad * 1.7)
    dec = 1 if v == "age" else 0
    suf = "" if v == "age" else "%"
    x0, y0 = xs.iloc[0], sm3.iloc[0]
    x1, y1 = xs.iloc[-1], sm3.iloc[-1]
    axp.plot([x0, x1], [y0, y1], "o", color=BLUE, ms=5.5, zorder=5)
    rising0 = sm3.iloc[min(2, len(sm3) - 1)] > sm3.iloc[0]
    off0 = (2, -16) if rising0 else (2, 10)
    axp.annotate(f"{y0:.{dec}f}{suf}", (x0, y0), xytext=off0,
                 textcoords="offset points", ha="left", fontsize=8.8,
                 color=BLUE, fontweight="bold")
    axp.annotate(f"{y1:.{dec}f}{suf}", (x1, y1), xytext=(-2, 10),
                 textcoords="offset points", ha="right", fontsize=8.8,
                 color=BLUE, fontweight="bold")
    axp.set_xlim(2003.6, 2025.4)
    axp.set_xticks(range(2006, 2025, 2))
    axp.set_xticklabels([str(t) for t in range(2006, 2025, 2)],
                        fontsize=6.6, rotation=45)
    axp.tick_params(axis="y", labelsize=8)
    axp.grid(axis="y", color="#EFEFEF", lw=0.6)
    axp.set_axisbelow(True)
    despine(axp)
fig.tight_layout(h_pad=2.4)
fig.savefig(f"{FIG}/g1_workforce.pdf")
plt.close(fig)

# ================ G2 evolution (approved: minimal layout) ================
S = pd.read_csv("outputs/p_series.csv").sort_values("cal_year")
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
ax.text(2019.5, 12.3, "Covid", ha="center", fontsize=8.5, color=SUBTLE)
ax.axhspan(7.4, 8.0, color="#FBE9E7", zorder=0)
ax.text(1996.9, 6.75, "Harris\u2013Adams,\n1992\u20132001: 7.7",
        fontsize=8.4, color=CORAL, va="top")
# historical harmonized segment (pre-2005 only), gaps break the line
hist = S[S["weighted"] == 0]
ax.plot(hist["cal_year"], hist["leaver_oldstyle"], color=GRAY, lw=1.4,
        ls="--", marker="s", ms=3.2)
ax.annotate("1997\u20132004: unweighted\noccupation pairs", (2000.6, 11.2),
            fontsize=8, color=GRAY, ha="center")
# main series: clean line, faint CI, long-run mean reference
ok = S["leaver_ba"].notna()
main = S[ok]
mean_ba = np.average(main["leaver_ba"])
ax.fill_between(main["cal_year"], main["leaver_ba"] - 1.96 * main["se_ba"],
                main["leaver_ba"] + 1.96 * main["se_ba"], color=BLUE,
                alpha=0.07, lw=0)
ax.axhline(mean_ba, color=INK, lw=0.9, ls=":", zorder=1)
ax.text(2014.0, 6.55, f"2005\u20132024 average: {mean_ba:.1f}",
        fontsize=8, color=INK, ha="center", va="top")
ax.plot(main["cal_year"], main["leaver_ba"], color=BLUE, lw=2.4)
last = main.iloc[-1]
pk = main.loc[main["leaver_ba"].idxmax()]
for r in (last, pk):
    ax.plot(r["cal_year"], r["leaver_ba"], "o", color=BLUE, ms=5)
    ax.annotate(f"{r['leaver_ba']:.1f}", (r["cal_year"], r["leaver_ba"]),
                xytext=(0, 9), textcoords="offset points", ha="center",
                fontsize=9, color=BLUE, fontweight="bold")
ax.set_ylim(0, 13)
ax.set_xlim(1996, 2025.5)
ax.set_xticks(range(1998, 2025, 2))
ax.set_xticklabels([str(t) for t in range(1998, 2025, 2)], fontsize=8,
                   rotation=45)
ax.set_ylabel("Percent leaving teaching")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g2_evolution.pdf")
plt.close(fig)

# appendix version with the definitional layers (all-teacher, harmonized)
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
ax.plot(S["cal_year"], S["leaver_oldstyle"], color=GRAY, lw=1.4, ls="--",
        marker="s", ms=3.2)
ax.plot(S["cal_year"], S["leaver_all"], color=GRAY, lw=1.4, marker="s",
        ms=3.2)
ax.plot(S["cal_year"], S["leaver_ba"], color=BLUE, lw=2.0, marker="o",
        ms=4.0)
ax.annotate("all teachers, full definition (weighted)", (2014.5, 12.8),
            fontsize=8.4, color=GRAY, ha="center")
ax.annotate("harmonized: occupation pairs only, unweighted\n"
            "(identical construction in every year)", (2003.4, 6.1),
            fontsize=8.2, color=GRAY, ha="center")
ax.annotate("college graduates, full definition", (2018.6, 5.4),
            fontsize=8.6, color=BLUE, fontweight="bold", ha="center")
ax.set_ylim(0, 14)
ax.set_xlim(1996, 2025.5)
ax.set_ylabel("Percent leaving teaching")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/gapp_evolution_layers.pdf")
plt.close(fig)

# ================ G3 flow of 100, two-tier ================
F = pd.read_csv("outputs/p_flow100_leavers.csv", index_col=0).iloc[:, 0]
DG = pd.read_csv("outputs/q_dest_groups.csv").set_index("group")[
    "per100_leavers"]
emp = F["education and care job"] + F["other occupation"]
edu_job = (DG["Postsecondary teaching"]
           + DG["School support (tutor, assistant, library)"]
           + DG["Education administration"])
care = DG["Counseling, social work, childcare"]
otherprof = DG["Management and business"] + DG["Other professional"]
salesetc = (DG["Office and administrative support"]
            + DG["Sales and personal service"]
            + DG["Production, transport, other"] + DG["Unclassified"])
fig, ax = plt.subplots(figsize=(9.6, 4.6))
Y1, Y0, H = 1.72, 0.55, 0.34
top = [("Employed", emp, BLUE),
       ("Out of the labor force, 55+", F["out of LF, 55plus"], LIGHT),
       ("Out of the labor force, <55", F["out of LF, under 55"], GOLD),
       ("Unemployed", F["unemployed"], "#6E6E6E")]
x = 0
for lab, v, c in top:
    ax.barh([Y1], [v], left=x, color=c, height=H)
    txtc = "white" if c in (BLUE, "#6E6E6E") else INK
    ax.text(x + v / 2, Y1, f"{v:.0f}", ha="center", va="center",
            color=txtc, fontsize=11, fontweight="bold")
    yl = Y1 + H / 2 + (0.10 if lab != "Unemployed" else 0.24)
    ax.text(x + v / 2, yl, lab, ha="center", va="bottom", fontsize=8.8,
            color=INK)
    x += v
bot = [("Education job", edu_job, BLUE),
       ("Care and\nchildren", care, CORAL),
       ("Other\nprofessional", otherprof, GREEN),
       ("Sales, office\nand manual", salesetc, GRAY)]
sc = 100.0 / emp                       # expand the employed bar to full width
x = 0
for lab, v, c in bot:
    w = v * sc
    ax.barh([Y0], [w], left=x, color=c, height=H)
    ax.text(x + w / 2, Y0, f"{v:.0f}", ha="center", va="center",
            color="white", fontsize=10.5, fontweight="bold")
    ax.text(x + w / 2, Y0 - H / 2 - 0.10, lab, ha="center", va="top",
            fontsize=8.8, color=INK)
    x += w
# diverging dotted connectors: employed segment opens into the full bar
ax.plot([0, 0], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=1.0)
ax.plot([emp, 100], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE,
        lw=1.0)
ax.text(-1.2, Y1, "Of every 100\nleavers", ha="right", va="center",
        fontsize=9.6, color=INK)
ax.text(-1.2, Y0, "What the employed\nare doing", ha="right", va="center",
        fontsize=9.6, color=INK)
# bracket: education and care total, on the expanded scale
ec = edu_job + care
xb = ec * sc
yb = Y0 - H / 2 - 0.52
ax.plot([0, 0, xb, xb], [yb + 0.05, yb, yb, yb + 0.05], color=INK, lw=1.1)
ax.text(xb / 2, yb - 0.07,
        f"{ec:.0f} of every 100 leavers keep working in education or care",
        ha="center", va="top", fontsize=9.6, color=INK,
        fontweight="bold")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.35, 2.35)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{FIG}/g3_flow100.pdf")
plt.close(fig)

# ================ G4 routes over the lifecycle ================
R5 = pd.read_csv("outputs/p_routes_age.csv")
x = np.arange(len(R5))
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.stackplot(x, R5["switch"], R5["unemp"], R5["leftlf"],
             colors=[GOLD, GRAY, BLUE], alpha=0.92)
ax.plot(x, R5["total"], color=INK, lw=1.5)
for i in (0, 5, len(R5) - 1):
    ax.annotate(f"{R5['total'].iloc[i]:.0f}", (i, R5["total"].iloc[i]),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=8.6, color=INK, fontweight="bold")
last = len(R5) - 1
y0 = R5["switch"].iloc[last]
y1 = y0 + R5["unemp"].iloc[last]
y2 = y1 + R5["leftlf"].iloc[last]
for lab, ym, c in [("to another job", y0 / 2, "#7A5B00"),
                   ("unemployed", (y0 + y1) / 2, "#555555"),
                   ("out of the labor force", (y1 + y2) / 2, BLUE)]:
    ax.annotate(lab, (last + 0.15, ym), fontsize=9, color=c, va="center",
                annotation_clip=False)
ax.set_xticks(x)
ax.set_xticklabels(R5["age"], fontsize=8.6)
ax.set_xlim(-0.3, last + 2.3)
ax.set_ylabel("Percent leaving, by route")
ax.set_xlabel("Age group")
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g4_routes_age.pdf")
plt.close(fig)

# ================ G5 earnings gamble ================
E = pd.read_csv("outputs/p_earnings_gamble.csv")
Z = E[E["group"] == "leaver, share zero earnings next year"]["p50"].iloc[0]
E = E[E["group"].isin(["stayer", "leaver, employed", "leaver, all"])]
names = {"stayer": "Stayers", "leaver, employed": "Leavers,\nemployed",
         "leaver, all": "Leavers, all\n(with any earnings)"}
fig, ax = plt.subplots(figsize=(8.0, 4.4))
for i, (_, r) in enumerate(E.iterrows()):
    c = BLUE if r["group"] == "stayer" else CORAL
    ax.fill_betweenx([r["p10"], r["p90"]], i - 0.05, i + 0.05, color=c,
                     alpha=0.30)
    ax.fill_betweenx([r["p25"], r["p75"]], i - 0.11, i + 0.11, color=c,
                     alpha=0.75)
    ax.plot([i - 0.17, i + 0.17], [r["p50"]] * 2, color=INK, lw=2.2)
    ax.annotate(f"median {r['p50']:+.0f}", (i + 0.20, r["p50"]),
                fontsize=8.8, color=INK, va="center", fontweight="bold")
    for val in (r["p10"], r["p90"]):
        ax.annotate(f"{val:+.0f}", (i - 0.135, val), fontsize=8.0,
                    color=SUBTLE, va="center", ha="right")
ax.axhline(0, color=INK, lw=0.8)
ax.annotate(f"and {Z:.0f}% of all leavers\nreport zero earnings\n"
            "the following year", (2.42, -150), fontsize=9.2, color=CORAL,
            ha="left", va="center", annotation_clip=False)
ax.set_xlim(-0.5, 3.15)
ax.set_ylim(-215, 215)
ax.set_xticks(range(len(E)))
ax.set_xticklabels([names[g] for g in E["group"]], fontsize=9.6)
ax.set_ylabel("Earnings change, log points ×100")
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g5_earnings.pdf")
plt.close(fig)

# ================ G6 coefficient plot, grouped ================
M = pd.read_csv("outputs/p_ame.csv")
M = M[~M["var"].isin(["age2"])]
BLOCKS = [("Job attachment", ["fullyear", "parttime"], BLUE),
          ("Compensation", ["pension", "public"], GREEN),
          ("Family", ["new_baby", "child_u6", "n_children", "married",
                      "sepdiv"], CORAL),
          ("Demographics", ["A_AGE", "female", "black", "ma_plus"], DARK)]
NAMES = {"fullyear": "Worked full year (50+ wks)",
         "parttime": "Part-time (<35 h/wk)", "pension": "Pension plan",
         "public": "Public school", "new_baby": "New baby this year",
         "child_u6": "Child under 6", "n_children": "Number of children",
         "married": "Married", "sepdiv": "Separated/divorced",
         "A_AGE": "Age (per year)", "female": "Female", "black": "Black",
         "ma_plus": "Master's+"}
order, colors, labels, blocks = [], [], [], []
for bl, vs, c in BLOCKS:
    for v in vs:
        order.append(v); colors.append(c); labels.append(NAMES[v])
        blocks.append(bl)
M = M.set_index("var").loc[order].reset_index()
n = len(M)
ypos = np.arange(n)[::-1]
fig, ax = plt.subplots(figsize=(8.2, 5.4))
# background bands per block
prev = 0
for bl, vs, c in BLOCKS:
    top = ypos[prev] + 0.5
    bot = ypos[prev + len(vs) - 1] - 0.5
    ax.axhspan(bot, top, color=c, alpha=0.055, zorder=0)
    ax.annotate(bl, (7.15, (top + bot) / 2), fontsize=9.2, color=c,
                fontweight="bold", va="center", ha="left",
                annotation_clip=False)
    prev += len(vs)
sig = (M["AME_pp"].abs() > 1.96 * M["se_pp"])
for i, (yv, (_, r), c, s) in enumerate(zip(ypos, M.iterrows(), colors,
                                           sig)):
    if s:
        ax.barh(yv, r["AME_pp"], color=c, height=0.6, zorder=3)
    else:
        ax.barh(yv, r["AME_pp"], color="white", edgecolor=c, lw=1.2,
                height=0.6, zorder=3)
ax.errorbar(M["AME_pp"], ypos, xerr=1.96 * M["se_pp"], fmt="none",
            ecolor=INK, elinewidth=0.9, capsize=2.0, zorder=4)
ax.set_yticks(ypos)
ax.set_yticklabels(labels, fontsize=9.4)
ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-11.5, 7)
ax.set_xlabel("Average marginal effect on P(leave teaching), pp   "
              "(filled: significant at 5%)")
ax.grid(axis="x", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g6_ame.pdf")
plt.close(fig)

# ================ G7 professions with H&A anchors ================
P = pd.read_csv("outputs/p_professions.csv")
piv = P.pivot(index="prof", columns="period", values="leaver_%")
piv = piv.sort_values("2015-2024")
HA = {"Teachers": 7.73, "Nurses": 6.09, "Social workers": 14.94,
      "Accountants": 8.01}
fig, ax = plt.subplots(figsize=(8.0, 4.4))
y = np.arange(len(piv))
for i, (prof, r) in enumerate(piv.iterrows()):
    c = BLUE if prof == "Teachers" else GRAY
    ax.plot([r["2010-2014"], r["2015-2024"]], [i, i], color=c, lw=1.8,
            alpha=0.75, zorder=2)
    ax.plot(r["2010-2014"], i, "o", color=c, ms=6.5, mfc="white", zorder=3)
    ax.plot(r["2015-2024"], i, "o", color=c, ms=7.5, zorder=3)
    if prof in HA:
        ax.plot(HA[prof], i, marker="s", color=CORAL, ms=6, mfc="none",
                mew=1.4, zorder=3)
    ax.annotate(h1(r["2015-2024"]), (r["2015-2024"], i),
                textcoords="offset points", xytext=(9, -3), fontsize=8.7,
                color=c,
                fontweight="bold" if prof == "Teachers" else "normal")
ax.set_yticks(y)
ax.set_yticklabels(piv.index, fontsize=9.6)
for tick, prof in zip(ax.get_yticklabels(), piv.index):
    if prof == "Teachers":
        tick.set_fontweight("bold"); tick.set_color(BLUE)
hnd = [plt.Line2D([], [], marker="o", color=GRAY, mfc="white", ls=""),
       plt.Line2D([], [], marker="o", color=GRAY, ls=""),
       plt.Line2D([], [], marker="s", color=CORAL, mfc="none", ls="")]
ax.legend(hnd, ["2010–2014", "2015–2024", "Harris–Adams 1992–2001"],
          frameon=False, fontsize=8.6, loc="lower right")
ax.set_xlabel("Percent leaving the profession per year")
ax.grid(axis="x", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g7_professions.pdf")
plt.close(fig)

# ================ G8 new baby, eight professions ================
NB = pd.read_csv("outputs/p_newbaby.csv").sort_values("AME_newbaby_pp")
fig, ax = plt.subplots(figsize=(7.6, 4.4))
cols9 = [BLUE if p == "Teachers" else GRAY for p in NB["prof"]]
ax.barh(NB["prof"], NB["AME_newbaby_pp"], color=cols9, height=0.6)
ax.errorbar(NB["AME_newbaby_pp"], NB["prof"], xerr=1.96 * NB["se_pp"],
            fmt="none", ecolor=INK, elinewidth=0.9, capsize=2.5)
for i, (_, r) in enumerate(NB.iterrows()):
    ax.text(r["AME_newbaby_pp"] + 1.96 * r["se_pp"] + 0.45, i,
            f"+{r['AME_newbaby_pp']:.1f}", fontsize=9, va="center",
            color=BLUE if r["prof"] == "Teachers" else SUBTLE,
            fontweight="bold" if r["prof"] == "Teachers" else "normal")
for tick, prof in zip(ax.get_yticklabels(), NB["prof"]):
    if prof == "Teachers":
        tick.set_fontweight("bold"); tick.set_color(BLUE)
ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-6, 14.5)
ax.set_xlabel("Effect of a new baby on P(a woman leaves her profession), pp")
ax.grid(axis="x", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g8_newbaby.pdf")
plt.close(fig)
print("figures v4 written")
