"""
Full figure set for the paper, old visual architecture on the new
instrument. Reads outputs/p_*.csv. Writes report/figures/f*.pdf and the
LaTeX tables report/table_p_*.tex.
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

# ---------- F1: instrument design ----------
fig, ax = plt.subplots(figsize=(7.6, 2.6))
ax.axis("off")
ax.annotate("", xy=(0.97, 0.42), xytext=(0.03, 0.42),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
ax.text(0.5, 0.30, "calendar year $t$", ha="center", fontsize=10,
        color=SUBTLE)
ax.add_patch(plt.Rectangle((0.06, 0.46), 0.62, 0.30, fc="#EAF0F8",
                           ec=BLUE, lw=1.2))
ax.text(0.37, 0.61, "longest job of year $t$:\nK--12 teacher (OCCUP)",
        ha="center", va="center", fontsize=10, color=INK)
ax.add_patch(plt.Rectangle((0.76, 0.46), 0.20, 0.30, fc="#FBEFEA",
                           ec=CORAL, lw=1.2))
ax.text(0.86, 0.61, "March $t{+}1$:\nteaching now?", ha="center",
        va="center", fontsize=10, color=INK)
ax.annotate("", xy=(0.755, 0.61), xytext=(0.685, 0.61),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
ax.text(0.86, 0.30, "leaver if not:\nother job / unemployed / out of LF",
        ha="center", va="top", fontsize=8.7, color=SUBTLE)
fig.tight_layout()
fig.savefig(f"{FIG}/f1_design.pdf")
plt.close(fig)

# ---------- F2: the changing profile of the teaching workforce ----------
WF = pd.read_csv("outputs/p_workforce.csv")
panels = [("female", "Female (%)"), ("age", "Mean age (years)"),
          ("ma_plus", "Master's or higher (%)"), ("public", "Public school (%)"),
          ("parttime", "Part-time (%)"), ("pension", "Pension plan (%)"),
          ("black", "Black (%)"), ("child_u6", "Child under 6 at home (%)")]
fig, axes = plt.subplots(2, 4, figsize=(11.5, 5.2))
for axp, (v, lab) in zip(axes.flat, panels):
    axp.plot(WF["cal_year"], WF[v], color=BLUE, lw=1.6)
    axp.set_title(lab, fontsize=9.5, color=INK)
    axp.tick_params(labelsize=8)
    axp.set_xticks([2010, 2017, 2024])
fig.tight_layout()
fig.savefig(f"{FIG}/f2_workforce.pdf")
plt.close(fig)

# ---------- F3: attrition by year, two definitions ----------
S = pd.read_csv("outputs/p_series.csv")
old = S[S["weighted"] == 0]
new = S[S["weighted"] == 1]
fig, ax = plt.subplots(figsize=(7.6, 3.9))
ax.plot(new["cal_year"], new["leaver_ba"], color=BLUE, lw=1.9, marker="o",
        ms=4, label="College-graduate teachers (main)")
ax.plot(new["cal_year"], new["leaver_all"], color=GRAY, lw=1.2, marker="s",
        ms=3, label="All teachers")
ax.plot(old["cal_year"], old["leaver_all"], color=GRAY, lw=1.2, ls="--",
        marker="s", ms=3, label="All teachers, 2005--09 (unweighted)")
ax.axvspan(2018.5, 2020.5, color="#F2F2F2", zorder=0)
ax.text(2019.5, 13.0, "Covid", ha="center", fontsize=9, color=SUBTLE)
ax.axhline(7.73, color=CORAL, lw=0.9, ls=":")
ax.text(2005.2, 7.73 + 0.25, "Harris–Adams 1992–2001 (7.7)", fontsize=8.3,
        color=CORAL)
ax.set_ylim(0, 14)
ax.set_ylabel("Percent leaving teaching")
ax.legend(frameon=False, fontsize=8.5, loc="lower left")
fig.tight_layout()
fig.savefig(f"{FIG}/f3_evolution.pdf")
plt.close(fig)

# ---------- F4: of every 100 leavers ----------
F = pd.read_csv("outputs/p_flow100_leavers.csv", index_col=0).iloc[:, 0]
labels = ["Education-adjacent job", "Other occupation", "Unemployed",
          "Out of labor force, <55", "Out of labor force, 55+"]
keys = ["education-adjacent job", "other occupation", "unemployed",
        "out of LF, under 55", "out of LF, 55plus"]
cols = [GREEN, GOLD, GRAY, CORAL, BLUE]
fig, ax = plt.subplots(figsize=(7.8, 3.1))
left = 0
for lab, k, c in zip(labels, keys, cols):
    v = F[k]
    ax.barh([0], [v], left=left, color=c, height=0.5)
    tx = left + v / 2
    if v >= 9:
        ax.text(tx, 0, f"{v:.0f}", ha="center", va="center", color="white",
                fontsize=11, fontweight="bold")
    else:
        ax.text(tx, 0.38, f"{v:.0f}", ha="center", va="bottom", color=c,
                fontsize=9.5, fontweight="bold")
    left += v
ax.set_xlim(0, 100)
ax.set_ylim(-0.55, 0.85)
ax.set_yticks([])
ax.set_xlabel("Of every 100 teachers who leave the profession...")
hnd = [plt.Rectangle((0, 0), 1, 1, color=c) for c in cols]
ax.legend(hnd, labels, frameon=False, fontsize=8.3, ncol=3,
          loc="upper center", bbox_to_anchor=(0.5, 1.38))
fig.tight_layout()
fig.savefig(f"{FIG}/f4_flow100.pdf")
plt.close(fig)

# ---------- F5: exit routes over the lifecycle ----------
R5 = pd.read_csv("outputs/p_routes_age.csv")
x = range(len(R5))
fig, ax = plt.subplots(figsize=(7.4, 3.9))
ax.stackplot(x, R5["switch"], R5["unemp"], R5["leftlf"],
             colors=[GOLD, GRAY, BLUE], alpha=0.92,
             labels=["To another occupation", "Unemployed",
                     "Out of the labor force"])
ax.plot(x, R5["total"], color=INK, lw=1.4)
ax.set_xticks(list(x))
ax.set_xticklabels(R5["age"], fontsize=8.4)
ax.set_ylabel("Percent of teachers leaving, by route")
ax.set_xlabel("Age group")
ax.legend(frameon=False, fontsize=8.7, loc="upper left")
fig.tight_layout()
fig.savefig(f"{FIG}/f5_routes_age.pdf")
plt.close(fig)

# ---------- F6: the earnings gamble ----------
E = pd.read_csv("outputs/p_earnings_gamble.csv")
E = E[E["group"].isin(["stayer", "leaver, employed", "leaver, all"])]
names = {"stayer": "Stayers", "leaver, employed": "Leavers,\nemployed",
         "leaver, all": "Leavers, all"}
fig, ax = plt.subplots(figsize=(7.0, 3.9))
for i, (_, r) in enumerate(E.iterrows()):
    c = BLUE if r["group"] == "stayer" else CORAL
    ax.plot([i, i], [r["p10"], r["p90"]], color=c, lw=2.2, alpha=0.45)
    ax.plot([i, i], [r["p25"], r["p75"]], color=c, lw=6, alpha=0.8)
    ax.plot(i, r["p50"], "o", color=INK, ms=6, zorder=5)
    ax.text(i + 0.09, r["p50"], f"median {r['p50']:+.0f}", fontsize=8.5,
            va="center", color=INK)
ax.axhline(0, color=INK, lw=0.8)
ax.set_xticks(range(len(E)))
ax.set_xticklabels([names[g] for g in E["group"]], fontsize=9.5)
ax.set_ylabel("Change in annual earnings, log points ×100")
fig.tight_layout()
fig.savefig(f"{FIG}/f6_earnings.pdf")
plt.close(fig)

# ---------- F7: AME ----------
M = pd.read_csv("outputs/p_ame.csv")
M = M[~M["var"].isin(["age2"])]
NAMES = {"fullyear": "Worked full year (50+ weeks)",
         "new_baby": "New baby during the year",
         "parttime": "Part-time (<35 h/week)",
         "pension": "Enrolled in a pension plan",
         "black": "Black", "public": "Public school", "female": "Female",
         "sepdiv": "Separated or divorced", "A_AGE": "Age (per year)",
         "ma_plus": "Master's degree or higher", "married": "Married",
         "n_children": "Number of children", "child_u6": "Child under 6"}
M["lab"] = M["var"].map(NAMES)
M["a"] = M["AME_pp"].abs()
M = M.sort_values("a").drop(columns="a")
fig, ax = plt.subplots(figsize=(7.2, 4.6))
sig = (M["AME_pp"].abs() > 1.96 * M["se_pp"])
ax.barh(M["lab"], M["AME_pp"],
        color=[BLUE if s else GRAY for s in sig], height=0.62)
ax.errorbar(M["AME_pp"], M["lab"], xerr=1.96 * M["se_pp"], fmt="none",
            ecolor=INK, elinewidth=0.9, capsize=2.2)
ax.axvline(0, color=INK, lw=0.8)
ax.set_xlabel("Average marginal effect on P(leave teaching), pp")
fig.tight_layout()
fig.savefig(f"{FIG}/f7_ame.pdf")
plt.close(fig)

# ---------- F8: professions, two periods ----------
P = pd.read_csv("outputs/p_professions.csv")
piv = P.pivot(index="prof", columns="period", values="leaver_%")
piv = piv.sort_values("2015-2024")
fig, ax = plt.subplots(figsize=(7.2, 4.2))
y = np.arange(len(piv))
for i, (prof, r) in enumerate(piv.iterrows()):
    c = BLUE if prof == "Teachers" else GRAY
    ax.plot([r["2010-2014"], r["2015-2024"]], [i, i], color=c, lw=1.6,
            alpha=0.7)
    ax.plot(r["2010-2014"], i, "o", color=c, ms=6, mfc="white")
    ax.plot(r["2015-2024"], i, "o", color=c, ms=7)
ax.set_yticks(y)
ax.set_yticklabels([p if p != "Teachers" else "Teachers"
                    for p in piv.index],
                   fontsize=9.5)
for tick, prof in zip(ax.get_yticklabels(), piv.index):
    if prof == "Teachers":
        tick.set_fontweight("bold")
ax.set_xlabel("Percent leaving the profession per year "
              "(open: 2010–14; filled: 2015–24)")
fig.tight_layout()
fig.savefig(f"{FIG}/f8_professions.pdf")
plt.close(fig)

# ---------- F9: new baby by profession ----------
NB = pd.read_csv("outputs/p_newbaby.csv")
fig, ax = plt.subplots(figsize=(6.8, 3.6))
cols9 = [BLUE if p == "Teachers" else GRAY for p in NB["prof"]]
ax.bar(NB["prof"], NB["AME_newbaby_pp"], color=cols9, width=0.6)
ax.errorbar(NB["prof"], NB["AME_newbaby_pp"], yerr=1.96 * NB["se_pp"],
            fmt="none", ecolor=INK, elinewidth=0.9, capsize=3)
ax.axhline(0, color=INK, lw=0.8)
ax.set_ylabel("New-baby effect on P(leave), pp (women)")
plt.setp(ax.get_xticklabels(), fontsize=9)
fig.tight_layout()
fig.savefig(f"{FIG}/f9_newbaby.pdf")
plt.close(fig)
print("figures f1-f9 written")

# ---------- LaTeX tables ----------
S.rename(columns={"leaver_all": "all", "leaver_ba": "ba"}, inplace=True)
with open("report/table_p_series.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccc}\n\\toprule\nCalendar year & "
             "College graduates & All teachers & Observations & Weighted "
             "\\\\\n\\midrule\n")
    for _, r in S.iterrows():
        ba = f"{r['ba']:.1f}\\%" if pd.notna(r["ba"]) else "--"
        fh.write(f"{int(r['cal_year'])} & {ba} & {r['all']:.1f}\\% & "
                 f"{int(r['n']):,} & {'yes' if r['weighted'] else 'no'} "
                 f"\\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

D = pd.read_csv("outputs/p_topdecile.csv")
with open("report/table_p_topdecile.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n & Top-risk decile & "
             "All teachers \\\\\n\\midrule\n")
    for _, r in D.iterrows():
        lab = str(r["trait"]).replace("%", "\\%")
        fh.write(f"{lab} & {r['top decile']} & {r['all teachers']} "
                 f"\\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

A = pd.read_csv("outputs/p_ame.csv")
with open("report/table_p_probit.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n & AME (pp) & SE \\\\\n"
             "\\midrule\n")
    for _, r in A.iterrows():
        fh.write(f"{NAMES.get(r['var'], r['var'])} & {r['AME_pp']:.2f} & "
                 f"({r['se_pp']:.2f}) \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")
print("tables written")
