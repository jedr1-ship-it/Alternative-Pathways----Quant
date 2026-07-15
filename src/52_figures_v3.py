"""
Publication figure set, v3. Coherent visual system: one accent color for
teachers/main series, muted comparisons, direct labeling over legends
where possible, thematic grouping in the coefficient plot, and the
two-panel destination figure that decomposes where the employed leavers
go. Writes report/figures/g*.pdf and the paper's LaTeX tables.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "src")
from paperstyle import BLUE, CORAL, GOLD, GREEN, GRAY, INK, SUBTLE  # noqa

FIG = "report/figures"
LIGHT = "#C9D6E8"


def despine(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# ================ G1: the changing workforce ================
WF = pd.read_csv("outputs/p_workforce.csv")
panels = [("female", "Female", "%"), ("age", "Mean age", "yrs"),
          ("ma_plus", "Master's or higher", "%"),
          ("public", "Public school", "%"),
          ("parttime", "Part-time", "%"),
          ("pension", "Pension plan", "%"),
          ("black", "Black", "%"), ("child_u6", "Child under 6", "%")]
fig, axes = plt.subplots(2, 4, figsize=(11.8, 5.4))
for axp, (v, lab, unit) in zip(axes.flat, panels):
    y = WF[v]
    axp.plot(WF["cal_year"], y, color=BLUE, lw=2.0)
    axp.fill_between(WF["cal_year"], y, y.min() - 2, color=BLUE, alpha=0.06)
    axp.plot(WF["cal_year"].iloc[[0, -1]], y.iloc[[0, -1]], "o", color=BLUE,
             ms=4.5)
    axp.annotate(f"{y.iloc[0]:.0f}", (WF["cal_year"].iloc[0], y.iloc[0]),
                 textcoords="offset points", xytext=(-2, 7), fontsize=8.2,
                 color=SUBTLE, ha="left")
    axp.annotate(f"{y.iloc[-1]:.0f}", (WF["cal_year"].iloc[-1], y.iloc[-1]),
                 textcoords="offset points", xytext=(2, 7), fontsize=8.2,
                 color=INK, ha="right", fontweight="bold")
    axp.set_title(f"{lab} ({unit})", fontsize=10, color=INK, pad=8)
    axp.set_xticks([2010, 2017, 2024])
    axp.tick_params(labelsize=8)
    axp.grid(axis="y", color="#EEEEEE", lw=0.7)
    axp.set_axisbelow(True)
    despine(axp)
fig.tight_layout(h_pad=2.2)
fig.savefig(f"{FIG}/g1_workforce.pdf")
plt.close(fig)

# ================ G2: attrition 1999-2024 ================
S = pd.read_csv("outputs/p_series.csv")
old = S[S["weighted"] == 0]
new = S[S["weighted"] == 1]
fig, ax = plt.subplots(figsize=(8.2, 4.1))
ax.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
ax.text(2019.5, 12.9, "Covid", ha="center", fontsize=9, color=SUBTLE)
ax.axhspan(7.4, 8.0, xmin=0, xmax=1, color="#F9E9E7", zorder=0)
ax.text(1999.2, 7.7, "Harris–Adams 1992–2001: 7.7", fontsize=8.2,
        color=CORAL, va="center")
ax.plot(old["cal_year"], old["leaver_all"], color=GRAY, lw=1.5, ls="--",
        marker="s", ms=3.4)
ax.plot(new["cal_year"], new["leaver_all"], color=GRAY, lw=1.5,
        marker="s", ms=3.4)
ax.plot(new["cal_year"], new["leaver_ba"], color=BLUE, lw=2.2, marker="o",
        ms=4.6)
ax.annotate("all teachers\n(dashed: unweighted early files)",
            (2004.4, old["leaver_all"].iloc[-1] + 2.6), fontsize=8.4,
            color=GRAY, ha="center")
ax.annotate("college graduates (main)", (2015.6, 6.35), fontsize=8.8,
            color=BLUE, fontweight="bold", ha="center")
ax.set_ylim(0, 14)
ax.set_ylabel("Percent leaving teaching")
ax.grid(axis="y", color="#EEEEEE", lw=0.7)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g2_evolution.pdf")
plt.close(fig)

# ================ G3: of every 100 leavers, two panels ================
F = pd.read_csv("outputs/p_flow100_leavers.csv", index_col=0).iloc[:, 0]
DG = pd.read_csv("outputs/q_dest_groups.csv")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.6, 4.3),
                             gridspec_kw={"width_ratios": [1, 1.25]})
# left: the five routes
routes = [("Out of labor force, 55+", F["out of LF, 55plus"], BLUE),
          ("Out of labor force, <55", F["out of LF, under 55"], LIGHT),
          ("Unemployed", F["unemployed"], GRAY),
          ("Education-adjacent job", F["education-adjacent job"], GREEN),
          ("Other occupation", F["other occupation"], GOLD)]
bottom = 0
for lab, v, c in routes:
    a1.bar([0], [v], bottom=bottom, color=c, width=0.55)
    a1.text(0.33, bottom + v / 2, f"{lab}  ({v:.0f})", fontsize=9.2,
            va="center", color=INK)
    bottom += v
a1.set_xlim(-0.45, 1.7)
a1.set_ylim(0, 100)
a1.set_xticks([])
a1.set_ylabel("Of every 100 leavers")
a1.set_title("Where the 100 go", fontsize=10.5, loc="left")
despine(a1)
# right: employed leavers by destination group
DG = DG.sort_values("per100_leavers")
cols = [GREEN if ("teach" in g.lower() or "school" in g.lower()
                  or "education" in g.lower() or "counsel" in g.lower())
        else GOLD for g in DG["group"]]
a2.barh(DG["group"], DG["per100_leavers"], color=cols, height=0.62)
for i, (_, r) in enumerate(DG.iterrows()):
    a2.text(r["per100_leavers"] + 0.07, i, f"{r['per100_leavers']:.1f}",
            fontsize=8.6, va="center", color=INK)
a2.set_xlabel("Per 100 leavers")
a2.set_title("The 26 with another job, by destination", fontsize=10.5,
             loc="left")
a2.tick_params(axis="y", labelsize=8.6)
a2.grid(axis="x", color="#EEEEEE", lw=0.7)
a2.set_axisbelow(True)
despine(a2)
fig.tight_layout(w_pad=3.0)
fig.savefig(f"{FIG}/g3_flow100.pdf")
plt.close(fig)

# ================ G4: exit routes over the lifecycle ================
R5 = pd.read_csv("outputs/p_routes_age.csv")
x = np.arange(len(R5))
fig, ax = plt.subplots(figsize=(8.0, 4.1))
ax.stackplot(x, R5["switch"], R5["unemp"], R5["leftlf"],
             colors=[GOLD, GRAY, BLUE], alpha=0.92)
ax.plot(x, R5["total"], color=INK, lw=1.5)
for i, t in enumerate(R5["total"]):
    ax.annotate(f"{t:.0f}", (i, t), textcoords="offset points",
                xytext=(0, 5), ha="center", fontsize=8.2, color=INK)
ax.text(0.6, 5.6, "to another job", fontsize=9, color="#7A5B00")
ax.text(7.15, 9.0, "out of the\nlabor force", fontsize=9, color="white",
        fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(R5["age"], fontsize=8.5)
ax.set_ylabel("Percent leaving, by route")
ax.set_xlabel("Age group")
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g4_routes_age.pdf")
plt.close(fig)

# ================ G5: the earnings gamble ================
E = pd.read_csv("outputs/p_earnings_gamble.csv")
E = E[E["group"].isin(["stayer", "leaver, employed"])]
names = {"stayer": "Stayers", "leaver, employed": "Leavers with a job"}
fig, ax = plt.subplots(figsize=(7.2, 4.2))
for i, (_, r) in enumerate(E.iterrows()):
    c = BLUE if r["group"] == "stayer" else CORAL
    ax.fill_betweenx([r["p10"], r["p90"]], i - 0.045, i + 0.045, color=c,
                     alpha=0.30)
    ax.fill_betweenx([r["p25"], r["p75"]], i - 0.10, i + 0.10, color=c,
                     alpha=0.75)
    ax.plot([i - 0.16, i + 0.16], [r["p50"]] * 2, color=INK, lw=2.2)
    for p, val in [("p10", r["p10"]), ("p90", r["p90"])]:
        ax.annotate(f"{val:+.0f}", (i + 0.13, val), fontsize=8.2,
                    color=SUBTLE, va="center")
    ax.annotate(f"median {r['p50']:+.0f}", (i + 0.19, r["p50"]),
                fontsize=9, color=INK, va="center", fontweight="bold")
ax.axhline(0, color=INK, lw=0.8)
ax.set_xlim(-0.5, 1.75)
ax.set_xticks(range(len(E)))
ax.set_xticklabels([names[g] for g in E["group"]], fontsize=10)
ax.set_ylabel("Earnings change, log points ×100")
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g5_earnings.pdf")
plt.close(fig)

# ================ G6: what predicts leaving, grouped ================
M = pd.read_csv("outputs/p_ame.csv")
M = M[~M["var"].isin(["age2"])]
BLOCKS = [("Job attachment", ["fullyear", "parttime"], BLUE),
          ("Compensation", ["pension", "public"], GREEN),
          ("Family", ["new_baby", "child_u6", "n_children", "married",
                      "sepdiv"], CORAL),
          ("Demographics", ["A_AGE", "female", "black", "ma_plus"], GRAY)]
NAMES = {"fullyear": "Worked full year (50+ wks)",
         "parttime": "Part-time (<35 h/wk)",
         "pension": "Pension plan", "public": "Public school",
         "new_baby": "New baby this year", "child_u6": "Child under 6",
         "n_children": "Number of children", "married": "Married",
         "sepdiv": "Separated/divorced", "A_AGE": "Age (per year)",
         "female": "Female", "black": "Black", "ma_plus": "Master's+"}
order, colors, labels = [], [], []
for bl, vs, c in BLOCKS:
    for v in vs:
        order.append(v)
        colors.append(c)
        labels.append(NAMES[v])
M = M.set_index("var").loc[order].reset_index()
ypos = np.arange(len(M))[::-1]
fig, ax = plt.subplots(figsize=(7.6, 5.2))
sig = (M["AME_pp"].abs() > 1.96 * M["se_pp"])
ax.barh(ypos, M["AME_pp"],
        color=[c if s else "#D5D5D5" for c, s in zip(colors, sig)],
        height=0.62)
ax.errorbar(M["AME_pp"], ypos, xerr=1.96 * M["se_pp"], fmt="none",
            ecolor=INK, elinewidth=0.9, capsize=2.0)
ax.set_yticks(ypos)
ax.set_yticklabels(labels, fontsize=9.2)
ax.axvline(0, color=INK, lw=0.9)
prev = 0
for bl, vs, c in BLOCKS:
    mid = ypos[prev:prev + len(vs)].mean()
    ax.text(-13.4, mid, bl, fontsize=9, color=c, fontweight="bold",
            rotation=90, va="center")
    prev += len(vs)
ax.set_xlim(-12, 7)
ax.set_xlabel("Average marginal effect on P(leave teaching), pp")
ax.grid(axis="x", color="#EEEEEE", lw=0.7)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g6_ame.pdf")
plt.close(fig)

# ================ G7: professions, two periods ================
P = pd.read_csv("outputs/p_professions.csv")
piv = P.pivot(index="prof", columns="period", values="leaver_%")
piv = piv.sort_values("2015-2024")
fig, ax = plt.subplots(figsize=(7.6, 4.3))
y = np.arange(len(piv))
for i, (prof, r) in enumerate(piv.iterrows()):
    c = BLUE if prof == "Teachers" else GRAY
    ax.plot([r["2010-2014"], r["2015-2024"]], [i, i], color=c, lw=1.8,
            alpha=0.75, zorder=2)
    ax.plot(r["2010-2014"], i, "o", color=c, ms=6.5, mfc="white", zorder=3)
    ax.plot(r["2015-2024"], i, "o", color=c, ms=7.5, zorder=3)
    ax.annotate(f"{r['2015-2024']:.1f}", (r["2015-2024"], i),
                textcoords="offset points", xytext=(8, -3), fontsize=8.6,
                color=c, fontweight="bold" if prof == "Teachers" else
                "normal")
ax.set_yticks(y)
ax.set_yticklabels(piv.index, fontsize=9.6)
for tick, prof in zip(ax.get_yticklabels(), piv.index):
    if prof == "Teachers":
        tick.set_fontweight("bold")
        tick.set_color(BLUE)
ax.set_xlabel("Percent leaving the profession per year "
              "(open 2010–14 → filled 2015–24)")
ax.grid(axis="x", color="#EEEEEE", lw=0.7)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g7_professions.pdf")
plt.close(fig)

# ================ G8: the new-baby effect ================
NB = pd.read_csv("outputs/p_newbaby.csv").sort_values("AME_newbaby_pp")
fig, ax = plt.subplots(figsize=(7.0, 3.9))
cols9 = [BLUE if p == "Teachers" else GRAY for p in NB["prof"]]
ax.barh(NB["prof"], NB["AME_newbaby_pp"], color=cols9, height=0.6)
ax.errorbar(NB["AME_newbaby_pp"], NB["prof"], xerr=1.96 * NB["se_pp"],
            fmt="none", ecolor=INK, elinewidth=0.9, capsize=2.5)
for i, (_, r) in enumerate(NB.iterrows()):
    ax.text(r["AME_newbaby_pp"] + 1.96 * r["se_pp"] + 0.18, i,
            f"+{r['AME_newbaby_pp']:.1f}", fontsize=9, va="center",
            color=BLUE if r["prof"] == "Teachers" else SUBTLE,
            fontweight="bold" if r["prof"] == "Teachers" else "normal")
for tick, prof in zip(ax.get_yticklabels(), NB["prof"]):
    if prof == "Teachers":
        tick.set_fontweight("bold")
        tick.set_color(BLUE)
ax.axvline(0, color=INK, lw=0.9)
ax.set_xlabel("Effect of a new baby on P(a woman leaves her profession), pp")
ax.grid(axis="x", color="#EEEEEE", lw=0.7)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g8_newbaby.pdf")
plt.close(fig)
print("figures g1-g8 written")

# ================ LaTeX tables ================
ROB = pd.read_csv("outputs/q_robustness.csv")
with open("report/table_q_robustness.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccccc}\n\\toprule\n"
             " & Full year & Part-time & Pension & New baby & Public & $n$"
             " \\\\\n\\midrule\n")
    for _, r in ROB.iterrows():
        cells = []
        for v in ["fullyear", "parttime", "pension", "new_baby", "public"]:
            star = "$^{*}$" if abs(r[v]) > 1.96 * r[v + "_se"] else ""
            cells.append(f"{r[v]:.2f}{star}")
        fh.write(f"{r['specification']} & " + " & ".join(cells)
                 + f" & {int(r['n']):,} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

RT = pd.read_csv("outputs/q_routes_model.csv")
NAMES2 = dict(NAMES)
with open("report/table_q_routes.tex", "w") as fh:
    fh.write("\\begin{tabular}{lccc}\n\\toprule\n & To another job & "
             "Unemployed & Out of labor force \\\\\n\\midrule\n")
    for v in ["fullyear", "parttime", "pension", "new_baby", "child_u6",
              "female", "A_AGE", "public", "ma_plus"]:
        cells = []
        for dep in ["switch", "unemp", "leftlf"]:
            r = RT[(RT["var"] == v) & (RT["route"] == dep)].iloc[0]
            star = "$^{*}$" if abs(r["AME_pp"]) > 1.96 * r["se_pp"] else ""
            cells.append(f"{r['AME_pp']:.2f}{star} ({r['se_pp']:.2f})")
        fh.write(f"{NAMES2.get(v, v)} & " + " & ".join(cells) + " \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

DEC = pd.read_csv("outputs/q_decades.csv")
with open("report/table_q_decades.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccccc}\n\\toprule\n & Leave & To job & "
             "Unemp. & Out LF & Public & Private \\\\\n\\midrule\n")
    for _, r in DEC.iterrows():
        fh.write(f"{r['period']} & {r['leaver_%']:.1f} & "
                 f"{r['switch_pp']:.1f} & {r['unemp_pp']:.1f} & "
                 f"{r['leftlf_pp']:.1f} & {r['public_%']:.1f} & "
                 f"{r['private_%']:.1f} \\\\\n")
    fh.write("\\midrule\nHarris--Adams 1992--2001 & 7.7 & 2.6 & 0.6 & 4.5"
             " & 6.6 & -- \\\\\n\\bottomrule\n\\end{tabular}\n")
print("tables written")
