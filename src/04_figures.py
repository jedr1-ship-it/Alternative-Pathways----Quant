"""
EsadeEcPol-style figures for the teacher-attrition brief.

Palette validated with the dataviz six-checks script:
  blue #2a78d6 (protective / baseline series), coral #e34948 (exit risk),
  gold #eda100 (highlight series; contrast WARN covered by direct labels),
  neutral gray #8a8f98 for non-significant marks.
"""
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from covariates import load_panel, COVS, LABELS

from paperstyle import *
os.makedirs("report/figures", exist_ok=True)

# main analysis sample: definition B (persistent leaver), baseline MIS 1-3
df = load_panel()
df = df[df["sampleB"]].copy()
W = "PWSSWGT_0"


def wrate(d):
    return np.average(d["leaver_p"], weights=d[W]) * 100


def style_barh(ax):
    ax.xaxis.grid(True); ax.yaxis.grid(False)


# ---------- Figure 1: where leavers go (single coral series) ----------
dest = {
    lab: np.average((df["dest"].eq(code)
                     & (df["leaver_p"] == 1)).astype(float),
                    weights=df[W]) * 100
    for lab, code in [("Moved to another occupation", "other occupation"),
                      ("Left the labor force", "out of labor force"),
                      ("Unemployed", "unemployed")]
}
fig, ax = plt.subplots(figsize=(6.4, 2.1))
names = list(dest)[::-1]
vals = [dest[n] for n in names]
bars = ax.barh(names, vals, height=0.52, color=CORAL, zorder=3)
for b, v in zip(bars, vals):
    ax.text(v + 0.35, b.get_y() + b.get_height() / 2, f"{v:.1f}%",
            va="center", ha="left", fontsize=10.5, color=INK,
            fontweight="bold")
ax.set_xlim(0, 19)
ax.set_xlabel("Share of baseline teachers, 12 months later (weighted %)")
style_barh(ax)
fig.tight_layout()
fig.savefig("report/figures/fig1_destinations.pdf")
plt.close(fig)

# ---------- Figure 2: attrition rate by characteristics (small multiples) --
groups = [
    ("Weekly hours", [("Full-time", df[df.parttime == 0]),
                      ("Part-time", df[df.parttime == 1])]),
    ("Highest degree", [("Bachelor's", df[df.ma_plus == 0]),
                        ("Master's+", df[df.ma_plus == 1])]),
    ("Teaching level", [("Preschool/K", df[df.preschool_kg == 1]),
                        ("Elem./middle", df[(df.preschool_kg == 0) & (df.secondary == 0) & (df.special_ed == 0)]),
                        ("Secondary", df[df.secondary == 1]),
                        ("Special ed.", df[df.special_ed == 1])]),
]
xmax = max(wrate(d) for _, rows in groups for _, d in rows) * 1.3
fig, axes = plt.subplots(1, 3, figsize=(9.2, 2.5),
                         gridspec_kw={"width_ratios": [2, 2, 4]})
for ax, (title, rows) in zip(axes, groups):
    names = [n for n, _ in rows][::-1]
    vals = [wrate(d) for _, d in rows][::-1]
    bars = ax.barh(names, vals, height=0.55, color=BLUE, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(v + xmax * 0.02, b.get_y() + b.get_height() / 2, f"{v:.0f}%",
                va="center", fontsize=10, color=INK, fontweight="bold")
    ax.set_title(title, loc="left", fontsize=10.5, color=NAVY,
                 fontweight="bold", pad=8)
    ax.set_xlim(0, xmax)
    style_barh(ax)
sample_line = np.average(df["leaver_p"], weights=df[W]) * 100
for ax in axes:
    ax.axvline(sample_line, color=SUBTLE, lw=1, ls=(0, (4, 3)), zorder=2)
axes[0].text(sample_line + 1.5, -0.68, f"all teachers: {sample_line:.0f}%",
             fontsize=8.5, color=SUBTLE)
fig.tight_layout(w_pad=2.2)
fig.savefig("report/figures/fig2_rates_by_group.pdf")
plt.close(fig)

# ---------- probit (shared by figures 3-5 and the table) ----------
formula = "leaver_p ~ " + " + ".join(COVS) + " + C(base_year)"
m = smf.probit(formula, data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["HRHHID"]}, disp=False)
me = m.get_margeff(at="overall")
ame = pd.DataFrame({"AME": me.margeff * 100, "se": me.margeff_se * 100,
                    "p": me.pvalues}, index=me.summary_frame().index)

# ---------- Figure 3: AME dot plot grouped by block ----------
BLOCKS = [
    ("THE JOB", ["parttime", "public", "hours_missing", "multjob"]),
    ("EDUCATION", ["ma_plus", "prof_phd"]),
    ("FAMILY", ["married", "n_children", "child_u6", "fem_child_u6",
                "new_baby", "fem_newbaby"]),
    ("DEMOGRAPHICS", ["female", "black", "hispanic", "noncitizen"]),
    ("TEACHING LEVEL", ["preschool_kg", "secondary", "special_ed"]),
    ("FAMILY INCOME", ["faminc75k"]),
]
# region indicators stay in the model but are not displayed
rows, ypos, ylabels, headers = [], [], [], []
y = 0.0
for title, vs in BLOCKS:
    headers.append((y + 0.85, title))
    for v in sorted(vs, key=lambda v: -abs(ame.loc[v, "AME"])):
        rows.append(v); ypos.append(y); ylabels.append(LABELS[v]); y -= 1.0
    y -= 1.4   # gap between blocks
d3 = ame.loc[rows]
d3["lo"] = d3["AME"] - 1.96 * d3["se"]
d3["hi"] = d3["AME"] + 1.96 * d3["se"]
colors = [GRAY if p >= 0.05 else (CORAL if a > 0 else BLUE)
          for a, p in zip(d3["AME"], d3["p"])]
fig, ax = plt.subplots(figsize=(6.9, 7.2))
ax.axvline(0, color=SUBTLE, lw=1, zorder=2)
for yi, (lo, hi, c) in zip(ypos, zip(d3["lo"], d3["hi"], colors)):
    ax.plot([lo, hi], [yi, yi], color=c, lw=2, zorder=3,
            solid_capstyle="round")
ax.scatter(d3["AME"], ypos, s=64, color=colors, zorder=4,
           edgecolor=SURFACE, linewidth=2)
for yi, (v, c, p) in zip(ypos, zip(d3["AME"], colors, d3["p"])):
    if p < 0.05:
        ax.text(v, yi + 0.34, f"{v:+.1f}", ha="center", fontsize=8.8,
                color=INK, fontweight="bold")
xmin = min(d3["lo"].min(), -3) - 1
for hy, title in headers:
    ax.text(xmin + 1.8, hy, title, fontsize=8.2, color=NAVY,
            fontweight="bold", ha="left", va="center")
ax.set_yticks(ypos, ylabels, fontsize=9.5)
ax.set_ylim(min(ypos) - 1, 1.7)
ax.set_xlabel("Change in P(leaving teaching), percentage points")
ax.yaxis.grid(False)
handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=c) for c in
           (CORAL, BLUE, GRAY)]
ax.legend(handles, ["Raises exit risk", "Lowers exit risk",
                    "Not significant (p≥0.05)"],
          loc="upper center", bbox_to_anchor=(0.5, 1.05), ncols=3,
          frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("report/figures/fig3_ame.pdf", bbox_inches="tight")
plt.close(fig)

# ---------- Figure 11: attrition by birth cohort and sex ----------
df["birth_year"] = df["base_year"] - df["age"]
df["cohort"] = (df["birth_year"] // 5) * 5
df["haskids"] = (df["n_children"] > 0).astype(int)
coh = []
for (c, f), g in df.groupby(["cohort", "female"]):
    if len(g) < 400:
        continue
    coh.append({"cohort": c, "group": "Women" if f else "Men",
                "rate": np.average(g["leaver_p"], weights=g[W]) * 100,
                "n": len(g)})
for c, g in df[(df.female == 1) & (df.haskids == 1)].groupby("cohort"):
    if len(g) < 400:
        continue
    coh.append({"cohort": c, "group": "Women with children",
                "rate": np.average(g["leaver_p"], weights=g[W]) * 100,
                "n": len(g)})
coh = pd.DataFrame(coh)
fig, ax = plt.subplots(figsize=(6.9, 3.5))
SERIES = [("Men", BLUE, "-"), ("Women", CORAL, "-"),
          ("Women with children", GOLD, "-")]
for lab, c, ls in SERIES:
    s = coh[coh.group == lab].sort_values("cohort")
    ax.plot(s.cohort, s.rate, color=c, lw=2, ls=ls,
            solid_capstyle="round")
    ax.scatter([s.cohort.iloc[-1]], [s.rate.iloc[-1]], s=42, color=c,
               zorder=4, edgecolor=SURFACE, linewidth=2)
handles = [plt.Line2D([], [], color=c, lw=2) for _, c, _ in SERIES]
ax.legend(handles, [l for l, *_ in SERIES], loc="upper center",
          bbox_to_anchor=(0.5, 1.14), ncols=3, frameon=False, fontsize=9)
ax.set_xlabel("Birth cohort (five-year bins)")
ax.set_ylabel("% leaving per year")
ax.set_ylim(0, None)
fig.tight_layout()
fig.savefig("report/figures/fig11_cohort.pdf")
plt.close(fig)
coh.round(2).to_csv("outputs/attrition_by_cohort_sex.csv", index=False)

# ---------- Figure 4: predicted exit probability by age ----------
ages = np.arange(23, 71)
base = df[COVS].mean()
Xa = pd.DataFrame([base] * len(ages))
Xa["age"] = ages
Xa["age2"] = ages ** 2 / 100.0
Xa["base_year"] = int(df["base_year"].mode().iat[0])
pr = m.predict(Xa) * 100
# simulation-based CI via parameter draws on the model's design matrix
rng = np.random.default_rng(7)
draws = rng.multivariate_normal(m.params, m.cov_params(), size=400)
from patsy import dmatrix
Xmat = np.asarray(dmatrix(m.model.data.design_info, Xa))
from scipy.stats import norm
sims = norm.cdf(Xmat @ draws.T) * 100
lo, hi = np.percentile(sims, [2.5, 97.5], axis=1)
fig, ax = plt.subplots(figsize=(6.4, 3.2))
ax.fill_between(ages, lo, hi, color=BLUE, alpha=0.10, linewidth=0)
ax.plot(ages, pr, color=BLUE, lw=2, solid_capstyle="round", zorder=3)
imin = int(np.argmin(pr.values))
ax.scatter([ages[imin]], [pr.iloc[imin]], s=64, color=BLUE, zorder=4,
           edgecolor=SURFACE, linewidth=2)
ax.annotate(f"lowest risk at age {ages[imin]}: {pr.iloc[imin]:.0f}%",
            (ages[imin], pr.iloc[imin]), textcoords="offset points",
            xytext=(0, -18), ha="center", fontsize=9, color=INK)
ax.text(ages[-1], pr.iloc[-1] + 1.2, f"{pr.iloc[-1]:.0f}%", ha="right",
        fontsize=10, fontweight="bold", color=INK)
ax.set_xlabel("Age")
ax.set_ylabel("Predicted P(leave), %")
ax.set_ylim(0, float(hi.max()) * 1.06)
fig.tight_layout()
fig.savefig("report/figures/fig4_age_profile.pdf")
plt.close(fig)

# ---------- Figure 5: high-risk decile vs all teachers (dumbbell) ----------
df["phat"] = m.predict(df)
hi10 = df.nlargest(len(df) // 10, "phat")
traits = ["parttime", "public", "ma_plus", "preschool_kg", "female",
          "married", "hispanic", "black"]
fig, ax = plt.subplots(figsize=(6.8, 3.6))
yy = np.arange(len(traits))[::-1]
for yi, t in zip(yy, traits):
    a, b = df[t].mean() * 100, hi10[t].mean() * 100
    ax.plot([a, b], [yi, yi], color="#d8dbe0", lw=2, zorder=2)
    ax.scatter([a], [yi], s=72, color=BLUE, zorder=3, edgecolor=SURFACE,
               linewidth=2)
    ax.scatter([b], [yi], s=72, color=GOLD, zorder=3, edgecolor=SURFACE,
               linewidth=2)
    off = 2.2 if b >= a else -2.2
    ax.text(b + off, yi, f"{b:.0f}%", va="center",
            ha="left" if b >= a else "right",
            fontsize=9.5, fontweight="bold", color=INK)
    ax.text(a - off, yi, f"{a:.0f}%", va="center",
            ha="right" if b >= a else "left", fontsize=9.5, color=SUBTLE)
ax.set_yticks(yy, [LABELS[t] for t in traits], fontsize=10)
ax.set_xlim(-4, 104)
ax.set_xlabel("Share with the trait, %")
ax.yaxis.grid(False)
handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=c)
           for c in (BLUE, GOLD)]
ax.legend(handles, ["All teachers", "Highest-risk decile"],
          loc="upper center", bbox_to_anchor=(0.5, 1.12), ncols=2,
          frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("report/figures/fig5_profile.pdf", bbox_inches="tight")
plt.close(fig)

# ---------- LaTeX regression table ----------
coefs = m.params
ses = m.bse
pvals = m.pvalues


def stars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


# American-Economic-Review-style layout: one column per estimate, standard
# error in parentheses on the line below, stars on the estimate
LABELS_TEX = {**LABELS,
              "faminc75k": "Family income \\$75k+",
              "parttime": "Part-time ($<$35 h/week)"}
rows = []
for v in COVS:
    a_se = ame.loc[v, "se"]
    rows.append(
        f"{LABELS_TEX[v]} & {coefs[v]:.3f}{stars(pvals[v])} & "
        f"{ame.loc[v,'AME']:.2f}{stars(ame.loc[v,'p'])} \\\\")
    rows.append(f" & ({ses[v]:.3f}) & ({a_se:.2f}) \\\\[2pt]")
table = "\n".join(rows)
wmean_dep = float(np.average(df['leaver_p'], weights=df[W]))
with open("report/table_probit.tex", "w") as f:
    f.write(f"""\\begin{{tabular}}{{lcc}}
\\toprule
 & \\multicolumn{{2}}{{c}}{{Leaves teaching with no observed return}} \\\\
\\cmidrule(lr){{2-3}}
 & (1) & (2) \\\\
 & Probit & Marginal effect \\\\
 & coefficients & (percentage points) \\\\
\\midrule
{table}
\\midrule
Base-year fixed effects & Yes & Yes \\\\
Mean of dependent variable & {df['leaver_p'].mean():.3f} & {df['leaver_p'].mean():.3f} \\\\
Persons & {int(m.nobs):,} & {int(m.nobs):,} \\\\
Pseudo $R^2$ & {m.prsquared:.3f} & \\\\
\\bottomrule
\\end{{tabular}}
""")

print("figures + table written to report/")
print(f"attrition {sample_line:.1f}% | decile mean phat {hi10['phat'].mean():.1%}")
