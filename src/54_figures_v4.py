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
panels = [("female", "Female (%)"), ("age", "Mean age (years)"),
          ("ma_plus", "Master's or higher (%)"),
          ("public", "Public school (%)"), ("parttime", "Part-time (%)"),
          ("pension", "Pension plan (%)"), ("black", "Black (%)"),
          ("child_u6", "Child under 6 (%)")]
fig, axes = plt.subplots(2, 4, figsize=(11.8, 5.6))
for axp, (v, lab) in zip(axes.flat, panels):
    y = WF[v].astype(float)
    sm3 = y.rolling(3, center=True, min_periods=2).mean()
    axp.plot(WF["cal_year"], y, color="#BBBBBB", lw=1.0)
    axp.plot(WF["cal_year"], sm3, color=BLUE, lw=2.2)
    i13 = WF["cal_year"] == 2013
    axp.plot(WF.loc[i13, "cal_year"], y[i13], "o", mfc="white", mec=GRAY,
             ms=4)
    axp.set_title(lab, fontsize=10, color=INK, pad=6)
    lo, hi = y.min(), y.max()
    pad = max((hi - lo) * 0.35, 0.8)
    axp.set_ylim(lo - pad, hi + pad)
    axp.annotate(f"{sm3.iloc[0]:.0f}", (0.02, 1.02), xycoords="axes fraction",
                 fontsize=8.4, color=SUBTLE)
    axp.annotate(f"{sm3.iloc[-1]:.0f}", (0.98, 1.02),
                 xycoords="axes fraction", fontsize=8.6, color=BLUE,
                 fontweight="bold", ha="right")
    axp.set_xticks([2010, 2017, 2024])
    axp.tick_params(labelsize=8)
    axp.grid(axis="y", color="#EFEFEF", lw=0.6)
    axp.set_axisbelow(True)
    despine(axp)
fig.tight_layout(h_pad=2.4)
fig.savefig(f"{FIG}/g1_workforce.pdf")
plt.close(fig)

# ================ G2 evolution ================
S = pd.read_csv("outputs/p_series.csv").sort_values("cal_year")
fig, ax = plt.subplots(figsize=(8.4, 4.3))
ax.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
ax.text(2019.5, 13.0, "Covid", ha="center", fontsize=9, color=SUBTLE)
ax.axhspan(7.4, 8.0, color="#E9F0FA", zorder=0)
ax.text(1996.8, 7.7, "Harris–Adams 1992–2001: 7.7\n(college graduates)",
        fontsize=8.0, color=BLUE, va="center")
# harmonized old-style, full span, gaps break naturally on NaN
ax.plot(S["cal_year"], S["leaver_oldstyle"], color=GRAY, lw=1.4, ls="--",
        marker="s", ms=3.2)
# weighted, full definition, all teachers
ax.plot(S["cal_year"], S["leaver_all"], color=GRAY, lw=1.4, marker="s",
        ms=3.2)
# main series with CI ribbon
ok = S["leaver_ba"].notna()
ax.fill_between(S.loc[ok, "cal_year"],
                S.loc[ok, "leaver_ba"] - 1.96 * S.loc[ok, "se_ba"],
                S.loc[ok, "leaver_ba"] + 1.96 * S.loc[ok, "se_ba"],
                color=BLUE, alpha=0.15, lw=0)
ax.plot(S["cal_year"], S["leaver_ba"], color=BLUE, lw=2.2, marker="o",
        ms=4.4)
ax.annotate("all teachers, full definition (weighted)", (2013.5, 12.9),
            fontsize=8.4, color=GRAY, ha="center")
ax.annotate("harmonized series: occupation pairs only,\nunweighted "
            "(comparable across all years)", (2003.4, 6.35), fontsize=8.2,
            color=GRAY, ha="center")
ax.annotate("college graduates, full definition (main)", (2018.5, 5.6),
            fontsize=8.8, color=BLUE, fontweight="bold", ha="center")
ax.set_ylim(0, 14)
ax.set_xlim(1996, 2025.5)
ax.set_ylabel("Percent leaving teaching")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g2_evolution.pdf")
plt.close(fig)

# ================ G3 flow of 100, unified ================
F = pd.read_csv("outputs/p_flow100_leavers.csv", index_col=0).iloc[:, 0]
DG = pd.read_csv("outputs/q_dest_groups.csv")
GREENS = {"Postsecondary teaching",
          "School support (tutor, assistant, library)",
          "Education administration",
          "Counseling, social work, childcare"}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.8, 4.5),
                             gridspec_kw={"width_ratios": [0.85, 1.35]})
routes = [("Out of labor force, 55+", F["out of LF, 55plus"], BLUE),
          ("Out of labor force, <55", F["out of LF, under 55"], LIGHT),
          ("Unemployed", F["unemployed"], GRAY),
          ("Education and care job", F["education and care job"], GREEN),
          ("Other occupation", F["other occupation"], GOLD)]
bottom = 0
for lab, v, c in routes:
    a1.bar([0], [v], bottom=bottom, color=c, width=0.5)
    a1.text(0.32, bottom + v / 2, f"{lab}  ({v:.1f})", fontsize=9.4,
            va="center", color=INK)
    bottom += v
a1.set_xlim(-0.35, 1.85)
a1.set_ylim(0, 100)
a1.set_xticks([])
a1.set_ylabel("Of every 100 leavers")
a1.set_title("The five routes out", fontsize=10.5, loc="left")
despine(a1)
DGs = DG.sort_values("per100_leavers")
DGs = pd.concat([DGs[DGs["group"] == "Unclassified"],
                 DGs[DGs["group"] != "Unclassified"]])
cols = ["#C9C9C9" if g == "Unclassified" else
        (GREEN if g in GREENS else GOLD) for g in DGs["group"]]
a2.barh(DGs["group"], DGs["per100_leavers"], color=cols, height=0.62)
for i, (_, r) in enumerate(DGs.iterrows()):
    a2.text(r["per100_leavers"] + 0.06, i, f"{r['per100_leavers']:.1f}",
            fontsize=8.7, va="center", color=INK)
a2.set_xlabel("Per 100 leavers")
a2.set_title("The 26 with another job: education and care (green) "
             "versus the rest", fontsize=10.5, loc="left")
a2.tick_params(axis="y", labelsize=8.7)
a2.grid(axis="x", color="#EFEFEF", lw=0.6)
a2.set_axisbelow(True)
despine(a2)
fig.tight_layout(w_pad=3.0)
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
