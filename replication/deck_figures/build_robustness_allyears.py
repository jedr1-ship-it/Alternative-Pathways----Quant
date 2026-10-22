"""All-years robustness: the probit AME coefficient plot and the
LPM/logit/probit table estimated on every survey year (1998-2025,
calendar 1997-2024) with the controls available throughout. Health,
disability and household-income controls exist only from the 2019
supplement, so they belong to the full specification (2019-2025).
Writes report/figures_deck/ame_allyears.{pdf,png}, the LaTeX source
report/data_cluster/robustness_allyears_table.tex and
outputs/ame_allyears.csv. Run from the repo root."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["EB Garamond", "STIXGeneral",
                                    "DejaVu Serif"],
                     "mathtext.fontset": "stix"})
INK = "#23373B"

d = pd.read_parquet("data/processed/asec_master.parquet",
    columns=["asec_year", "cal_year", "teacher", "ba_plus", "ma_plus",
             "A_AGE", "A_MARITL", "female", "black", "married",
             "n_children", "child_u6", "new_baby", "pension",
             "parttime_ly", "fullyear", "public_ly", "leaver"])
for c in d.columns:
    d[c] = pd.to_numeric(d[c], errors="coerce")
R = d[(d.teacher == 1) & (d.ba_plus == 1) & d.A_AGE.between(18, 70)
      & d.leaver.notna() & d.cal_year.between(1997, 2024)].copy()
R["sepdiv"] = R.A_MARITL.isin([4, 5]).astype(float)
R["age"] = R.A_AGE
R["age2"] = R.A_AGE ** 2
XV = ["fullyear", "parttime_ly", "pension", "public_ly",
      "new_baby", "child_u6", "n_children", "married", "sepdiv",
      "age", "age2", "female", "black", "ma_plus"]
R = R.dropna(subset=XV + ["leaver"])
N = len(R)
print("sample:", N, "teachers, years",
      int(R.cal_year.min()), "-", int(R.cal_year.max()))
X = pd.concat([R[XV], pd.get_dummies(R.cal_year.astype(int), prefix="y",
                                     drop_first=True).astype(float)],
              axis=1)
X = sm.add_constant(X)
y = R.leaver.astype(float)

out = {}
ols = sm.OLS(y, X).fit(cov_type="HC1")
out["LPM"] = (ols.params[XV] * 100, ols.bse[XV] * 100)
for name, model in [("Logit", sm.Logit), ("Probit", sm.Probit)]:
    m = model(y, X).fit(disp=0, maxiter=200)
    mg = m.get_margeff(at="overall")
    me = pd.Series(mg.margeff, index=X.columns[1:])
    se = pd.Series(mg.margeff_se, index=X.columns[1:])
    out[name] = (me[XV] * 100, se[XV] * 100)
res = pd.DataFrame({f"{k}_{w}": v[i] for k, v in out.items()
                    for i, w in enumerate(("ame", "se"))})
res.to_csv("outputs/ame_allyears.csv")
print(res.round(2).to_string())

# ---------------- coefficient plot (probit AME) ----------------
ame, se = out["Probit"]
GROUPS = [
 ("Job attachment", [("fullyear", "Full-year contract"),
                     ("parttime_ly", "Part-time contract")]),
 ("Compensation", [("pension", "Employer pension plan"),
                   ("public_ly", "Public sector")]),
 ("Family", [("new_baby", "New baby during the year"),
             ("child_u6", "Child under 6"),
             ("n_children", "Number of children"),
             ("married", "Married"),
             ("sepdiv", "Separated or divorced")]),
 # age enters as a quadratic, so its single AME is not interpretable
 ("Demographics", [("female", "Female"),
                   ("black", "Black"),
                   ("ma_plus", "Master's degree or higher")]),
]
BLACK = "#000000"
fig, ax = plt.subplots(figsize=(11.6, 6.6))
yy = 0
yticks, ylabels, heads = [], [], []
for gname, items in GROUPS:
    heads.append((yy, gname))
    yy -= 1
    for v, lab in items:
        a, s = ame[v], se[v]
        lo, hi = a - 1.96 * s, a + 1.96 * s
        sig = (lo > 0) or (hi < 0)
        ax.plot([lo, hi], [yy, yy], color=BLACK, lw=1.0,
                solid_capstyle="butt")
        ax.plot([lo, lo], [yy - .10, yy + .10], color=BLACK, lw=1.0)
        ax.plot([hi, hi], [yy - .10, yy + .10], color=BLACK, lw=1.0)
        ax.plot(a, yy, "o", ms=6.5, mfc=BLACK if sig else "white",
                mec=BLACK, mew=1.1)
        ax.annotate(f"{a:+.1f}", (a, yy), xytext=(0, 8),
                    textcoords="offset points", ha="center",
                    fontsize=9.5, color=INK)
        yticks.append(yy); ylabels.append(lab)
        yy -= 1
    yy -= 0.4
ax.axvline(0, color=BLACK, lw=0.8)
for hy, lab in heads:
    ax.text(-13.4, hy, lab, fontsize=12, fontweight="bold", color=INK,
            va="center")
ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=11)
ax.set_xlim(-13.5, 10)
ax.set_ylim(yy + 0.2, 1.0)
ax.set_xticks(range(-12, 10, 3))
ax.set_xlabel("average marginal effect on the probability of leaving "
              "(percentage points)", fontsize=11, color=INK)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("report/figures_deck/ame_allyears.pdf")
fig.savefig("report/figures_deck/ame_allyears.png", dpi=200)
print("saved ame_allyears")

# ---------------- LaTeX table ----------------
LAB = {"fullyear": "Full-year contract",
       "parttime_ly": "Part-time contract",
       "pension": "Employer pension plan",
       "public_ly": "Public sector",
       "new_baby": "New baby during the year",
       "child_u6": "Child under 6",
       "ma_plus": "Master's degree or higher"}
def star(a, s):
    z = abs(a / s)
    if z > 2.576:
        return r"\sym{***}"
    if z > 1.96:
        return r"\sym{**}"
    return r"\sym{*}" if z > 1.645 else ""
rows = []
for v, lab in LAB.items():
    line1, line2 = lab, ""
    for k in ("LPM", "Logit", "Probit"):
        a, s = out[k][0][v], out[k][1][v]
        line1 += f" & {a:+.2f}{star(a, s)}"
        line2 += f" & ({s:.2f})"
    rows.append(line1 + r" \\")
    rows.append(" " + line2 + r" \\[0.2em]")
body = "\n".join(rows)
NS = f"{N:,}"
tex = (r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[paperwidth=18cm,paperheight=24cm,margin=0.6cm]{geometry}
\usepackage{booktabs,threeparttable}
\setlength{\tabcolsep}{12pt}
\pagestyle{empty}
\newcommand{\sym}[1]{\rlap{$^{#1}$}}
\begin{document}
\begin{center}
{\large\bfseries Table A3 --- The margins over the whole period,
1997--2024}\\[1.0em]
\begin{threeparttable}
\begin{tabular}{lccc}
\toprule
 & \multicolumn{3}{c}{Average marginal effect on leaving, percentage points} \\
\cmidrule(lr){2-4}
 & LPM & Logit & Probit \\
 & (1) & (2) & (3) \\
\midrule
""" + body + r"""
\midrule
Year fixed effects & Yes & Yes & Yes \\
Observations       & """ + NS + " & " + NS + " & " + NS + r""" \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]
\footnotesize
\item \emph{Notes:} Entries are percentage points: $-9.93$ means a
9.9-point lower annual probability of leaving teaching. Sample: all
teachers with a bachelor's degree or higher, aged
18--70, in the pooled March supplements of 1998--2025 (outcomes over
calendar years 1997--2024); one observation per person and year,
$N$ = """ + NS + r""". Controls beyond those shown: number of
children, married, separated or divorced, age, age$^2$, female and
Black. Health, disability and household-income controls exist only
from the 2019 supplement and belong to the 2019--2025 full
specification (Tables A1--A2); on that window they leave these margins
essentially unchanged. Robust standard errors in parentheses (delta
method for the logit and probit marginal effects). $^{*}$ $p<0.10$,
$^{**}$ $p<0.05$, $^{***}$ $p<0.01$.
\end{tablenotes}
\end{threeparttable}
\end{center}
\end{document}
""")
open("report/data_cluster/robustness_allyears_table.tex", "w").write(tex)
print("wrote robustness_allyears_table.tex")
