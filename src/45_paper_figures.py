"""
Figures and LaTeX tables for the rewritten paper (retrospective instrument,
calendar 2015-2024). Reads outputs/main_*.csv and outputs/ha_*.csv written
by 44_main_analysis.py and 43_harris_update.py.

Figures (report/figures/): fig_m1_evolution, fig_m2_flow100, fig_m3_ame,
fig_m4_age, fig_m5_professions.
Tables  (report/): table_m_profile, table_m_annual, table_m_destinations,
table_app_ha, table_app_confusion.
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

# ---------- fig 1: annual evolution with decomposition ----------
A = pd.read_csv("outputs/main_annual.csv")
fig, ax = plt.subplots(figsize=(7.4, 3.9))
ax.plot(A["cal_year"], A["leaver_%"], color=INK, lw=1.8, marker="o",
        ms=4, label="Leave teaching (total)")
ax.plot(A["cal_year"], A["out_of_LF"], color=BLUE, lw=1.3, marker="s",
        ms=3.5, label="Out of the labor force")
ax.plot(A["cal_year"], A["to_other_job"], color=CORAL, lw=1.3, marker="^",
        ms=3.5, label="Employed in another occupation")
ax.plot(A["cal_year"], A["unemployed"], color=GRAY, lw=1.1, marker="d",
        ms=3, label="Unemployed")
ax.axvspan(2018.5, 2020.5, color="#F2F2F2", zorder=0)
ax.text(2019.5, 11.2, "Covid", ha="center", fontsize=9, color=SUBTLE)
ax.set_ylim(0, 12)
ax.set_ylabel("Percent of teachers")
ax.set_xticks(A["cal_year"])
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
fig.tight_layout()
fig.savefig(f"{FIG}/fig_m1_evolution.pdf")
plt.close(fig)

# ---------- fig 2: of each 100 teachers ----------
F = pd.read_csv("outputs/main_flow100.csv", index_col=0).iloc[:, 0]
labels = ["Still teaching", "Employed in\nanother occupation",
          "Unemployed", "Out of the\nlabor force"]
vals = [F["siguen ensenando"], F["otro empleo"], F["parados"],
        F["fuera de la fuerza laboral"]]
cols = [GREEN, CORAL, GRAY, BLUE]
fig, ax = plt.subplots(figsize=(7.4, 2.9))
left = 0
for lab, v, c in zip(labels, vals, cols):
    ax.barh([0], [v], left=left, color=c, height=0.55)
    if v > 6:
        ax.text(left + v / 2, 0, f"{v:.1f}", ha="center", va="center",
                color="white", fontsize=11, fontweight="bold")
    else:
        ax.text(left + v / 2, 0.42, f"{v:.1f}", ha="center", va="bottom",
                color=c, fontsize=9.5, fontweight="bold")
    left += v
ax.set_xlim(0, 100)
ax.set_ylim(-0.6, 0.9)
ax.set_yticks([])
ax.set_xlabel("Of every 100 teachers in a school year, one year later...")
hnd = [plt.Rectangle((0, 0), 1, 1, color=c) for c in cols]
ax.legend(hnd, [x.replace("\n", " ") for x in labels], frameon=False,
          fontsize=8.5, ncol=4, loc="upper center",
          bbox_to_anchor=(0.5, 1.32))
fig.tight_layout()
fig.savefig(f"{FIG}/fig_m2_flow100.pdf")
plt.close(fig)

# ---------- fig 3: AME ranked ----------
M = pd.read_csv("outputs/main_ame.csv")
M = M[~M["var"].isin(["age2"])]
NAMES = {"fullyear": "Worked full year (50+ weeks)",
         "parttime": "Part-time (<35 h/week)",
         "pension": "Enrolled in a pension plan",
         "black": "Black", "public": "Public school",
         "female": "Female", "sepdiv": "Separated or divorced",
         "A_AGE": "Age (per year)", "ma_plus": "Master's degree or higher",
         "married": "Married"}
M["lab"] = M["var"].map(NAMES)
M = M.iloc[::-1]
fig, ax = plt.subplots(figsize=(7.0, 4.2))
sig = (M["AME_pp"].abs() > 1.96 * M["se_pp"])
ax.barh(M["lab"], M["AME_pp"],
        color=[BLUE if s else GRAY for s in sig], height=0.62)
ax.errorbar(M["AME_pp"], M["lab"], xerr=1.96 * M["se_pp"], fmt="none",
            ecolor=INK, elinewidth=0.9, capsize=2.2)
ax.axvline(0, color=INK, lw=0.8)
ax.set_xlabel("Average marginal effect on P(leave teaching), percentage points")
fig.tight_layout()
fig.savefig(f"{FIG}/fig_m3_ame.pdf")
plt.close(fig)

# ---------- fig 4: age profile ----------
H5 = pd.read_csv("outputs/ha_table5.csv")
fig, ax = plt.subplots(figsize=(7.0, 3.8))
x = range(len(H5))
ax.plot(x, H5["Teachers"], color=BLUE, lw=1.9, marker="o", ms=4.5,
        label="Teachers")
ax.plot(x, H5["Nurses"], color=GREEN, lw=1.2, marker="s", ms=3.4,
        label="Nurses")
ax.plot(x, H5["Social workers"], color=CORAL, lw=1.2, marker="^", ms=3.4,
        label="Social workers")
ax.plot(x, H5["Accountants"], color=GOLD, lw=1.2, marker="d", ms=3.4,
        label="Accountants")
ax.set_xticks(list(x))
ax.set_xticklabels(H5["age"], fontsize=8.5)
ax.set_ylabel("Percent leaving the profession")
ax.set_xlabel("Age group")
ax.legend(frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(f"{FIG}/fig_m4_age.pdf")
plt.close(fig)

# ---------- fig 5: professions, then and now ----------
T1 = pd.read_csv("outputs/ha_table1.csv").set_index("profession")
HA = {"Teachers": 7.73, "Nurses": 6.09, "Social workers": 14.94,
      "Accountants": 8.01}
order = ["Teachers", "Nurses", "Social workers", "Accountants"]
fig, ax = plt.subplots(figsize=(7.0, 3.6))
xx = np.arange(len(order))
ax.bar(xx - 0.19, [HA[p] for p in order], width=0.38, color=GRAY,
       label="1992–2001 (Harris & Adams)")
ax.bar(xx + 0.19, [T1.loc[p, "turnover_%"] for p in order], width=0.38,
       color=BLUE, label="2015–2024 (this paper)")
for i, p in enumerate(order):
    ax.text(i - 0.19, HA[p] + 0.25, f"{HA[p]:.1f}", ha="center", fontsize=9,
            color=SUBTLE)
    ax.text(i + 0.19, T1.loc[p, "turnover_%"] + 0.25,
            f"{T1.loc[p, 'turnover_%']:.1f}", ha="center", fontsize=9,
            color=BLUE, fontweight="bold")
ax.set_xticks(xx)
ax.set_xticklabels(order)
ax.set_ylabel("Percent leaving the profession per year")
ax.set_ylim(0, 17)
ax.legend(frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(f"{FIG}/fig_m5_professions.pdf")
plt.close(fig)
print("figures written")

# ================= LaTeX tables =================
def esc(s):
    return str(s).replace("%", "\\%").replace("$", "\\$")


# table: profile stayer vs leaver
PR = pd.read_csv("outputs/main_profile.csv")
with open("report/table_m_profile.tex", "w") as fh:
    fh.write("\\begin{tabular}{lccc}\n\\toprule\n"
             " & Stayers & Leavers & Difference \\\\\n\\midrule\n")
    EN = {"Edad": "Age, years", "Mujer": "Female", "Negra/o": "Black",
          "Casada/o": "Married",
          "Separada/divorciada": "Separated or divorced",
          "Master o mas": "Master's degree or higher",
          "Escuela publica": "Public school",
          "Con plan de pension": "Enrolled in a pension plan",
          "Tiempo parcial (<35h)": "Part-time ($<$35 h/week)",
          "Ano completo (50+ sem)": "Worked full year (50+ weeks)",
          "Salario semanal ($)": "Weekly earnings (\\$)"}
    pctset = {"Female", "Black", "Married", "Separated or divorced",
              "Master's degree or higher", "Public school",
              "Enrolled in a pension plan", "Part-time ($<$35 h/week)",
              "Worked full year (50+ weeks)"}
    for _, r in PR.iterrows():
        lab = EN[r["variable"]]
        suf = "\\%" if lab in pctset else ""
        fh.write(f"{lab} & {r['stayer']}{suf} & {r['leaver']}{suf} & "
                 f"{r['diff']}{suf} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# table: annual
with open("report/table_m_annual.tex", "w") as fh:
    fh.write("\\begin{tabular}{lccccc}\n\\toprule\n"
             "Year & Leave teaching & Other occupation & Unemployed & "
             "Out of LF & Teachers \\\\\n\\midrule\n")
    for _, r in A.iterrows():
        fh.write(f"{int(r['cal_year'])} & {r['leaver_%']:.1f}\\% & "
                 f"{r['to_other_job']:.1f}\\% & {r['unemployed']:.1f}\\% & "
                 f"{r['out_of_LF']:.1f}\\% & {int(r['n']):,} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# table: destinations
D = pd.read_csv("outputs/main_destinations.csv")
with open("report/table_m_destinations.tex", "w") as fh:
    fh.write("\\begin{tabular}{lc}\n\\toprule\n"
             "Destination occupation & Share of switchers \\\\\n\\midrule\n")
    FIXLAB = {"?": None, "nan": None}
    MANUAL = {2200: "Postsecondary teachers", 2540: "Teaching assistants"}
    for _, r in D.iterrows():
        lab = r["occupation"]
        if lab in ("?", "nan") or pd.isna(lab):
            lab = MANUAL.get(int(r["PEIOOCC"]), f"occ {int(r['PEIOOCC'])}")
        fh.write(f"{esc(lab)} & {r['share_%']:.1f}\\% \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# appendix: H&A comparison
T2 = pd.read_csv("outputs/ha_table2.csv")
T2a = T2[T2["sample"] == "All"].set_index("profession")
HA_FULL = {"Teachers": (7.73, 2.59, 0.61, 4.53),
           "Nurses": (6.09, 1.68, 0.86, 3.54),
           "Social workers": (14.94, 10.87, 1.34, 2.73),
           "Accountants": (8.01, 4.10, 1.55, 2.36)}
with open("report/table_app_ha.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccccccc}\n\\toprule\n"
             " & \\multicolumn{4}{c}{Harris \\& Adams, 1992--2001}"
             " & \\multicolumn{4}{c}{This paper, 2015--2024} \\\\\n"
             "\\cmidrule(lr){2-5}\\cmidrule(lr){6-9}\n"
             " & All & Switch & Unemp. & Out LF & All & Switch & Unemp."
             " & Out LF \\\\\n\\midrule\n")
    for p in order:
        h = HA_FULL[p]
        m = T2a.loc[p]
        fh.write(f"{p} & {h[0]:.2f} & {h[1]:.2f} & {h[2]:.2f} & {h[3]:.2f}"
                 f" & {m['left_all']:.2f} & {m['switch']:.2f} & "
                 f"{m['unemployed']:.2f} & {m['left_LF']:.2f} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# appendix: validation confusion matrix (20 cohorts)
DB = pd.read_csv("outputs/tttt_march_allyears.csv", dtype={"PERIDNUM": str})
C = DB[(DB["MARZO"] == 1) & DB["leaver"].notna() & DB["leaver_MARCH"].notna()]
ct = pd.crosstab(C["leaver"], C["leaver_MARCH"])
with open("report/table_app_confusion.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccc}\n\\toprule\n"
             " & \\multicolumn{3}{c}{March retrospective classification}"
             " & \\\\\n\\cmidrule(lr){2-4}\n"
             "Linked-panel classification & Not a teacher & Stayed & Left &"
             " Total \\\\\n\\midrule\n")
    fh.write(f"Stayer (teaches all 4 post months) & {int(ct.loc[0,-1]):,} & "
             f"{int(ct.loc[0,0]):,} & {int(ct.loc[0,1]):,} & "
             f"{int(ct.loc[0].sum()):,} \\\\\n")
    fh.write(f"Leaver (teaches in none) & {int(ct.loc[1,-1]):,} & "
             f"{int(ct.loc[1,0]):,} & {int(ct.loc[1,1]):,} & "
             f"{int(ct.loc[1].sum()):,} \\\\\n\\midrule\n")
    fh.write(f"Total & {int(ct[-1].sum()):,} & {int(ct[0].sum()):,} & "
             f"{int(ct[1].sum()):,} & {int(ct.values.sum()):,} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")
print("tables written")
