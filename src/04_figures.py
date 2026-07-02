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

BLUE, CORAL, GOLD, GRAY = "#2a78d6", "#e34948", "#eda100", "#8a8f98"
INK, SUBTLE, SURFACE = "#1a2430", "#5a6572", "#fcfcfb"
NAVY = "#12355b"

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK, "axes.edgecolor": "#d8dbe0", "axes.labelcolor": SUBTLE,
    "xtick.color": SUBTLE, "ytick.color": SUBTLE,
    "axes.grid": True, "grid.color": "#e9ebee", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.size": 10,
})
os.makedirs("report/figures", exist_ok=True)

# main analysis sample: definition B (persistent leaver), baseline MIS 1-3
df = load_panel()
df = df[df["sampleB"]].copy()
W = "PWSSWGT_0"


def wrate(d):
    return np.average(d["leaver_p"], weights=d[W]) * 100


def style_barh(ax):
    ax.xaxis.grid(True); ax.yaxis.grid(False)
    ax.tick_params(length=0)


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

# ---------- Figure 3: AME dot plot (dummies only; age shown in fig 4) -----
plot_vars = [v for v in COVS if v not in ("age", "age2", "hours_missing")]
d3 = ame.loc[plot_vars].sort_values("AME")
d3["lo"] = d3["AME"] - 1.96 * d3["se"]
d3["hi"] = d3["AME"] + 1.96 * d3["se"]
colors = [GRAY if p >= 0.05 else (CORAL if a > 0 else BLUE)
          for a, p in zip(d3["AME"], d3["p"])]
fig, ax = plt.subplots(figsize=(6.8, 4.4))
y = np.arange(len(d3))
ax.axvline(0, color=SUBTLE, lw=1, zorder=2)
for yi, (lo, hi, c) in enumerate(zip(d3["lo"], d3["hi"], colors)):
    ax.plot([lo, hi], [yi, yi], color=c, lw=2, zorder=3,
            solid_capstyle="round")
ax.scatter(d3["AME"], y, s=64, color=colors, zorder=4,
           edgecolor=SURFACE, linewidth=2)
for yi, (v, c, p) in enumerate(zip(d3["AME"], colors, d3["p"])):
    if p < 0.05:
        ax.text(v, yi + 0.32, f"{v:+.1f}", ha="center", fontsize=9,
                color=INK, fontweight="bold")
ax.set_yticks(y, [LABELS[v] for v in d3.index], fontsize=10)
ax.set_xlabel("Change in P(persistently leaving teaching), percentage points")
ax.tick_params(length=0)
ax.yaxis.grid(False)
handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=c) for c in
           (CORAL, BLUE, GRAY)]
ax.legend(handles, ["Raises exit risk", "Lowers exit risk",
                    "Not significant (p≥0.05)"],
          loc="lower right", frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("report/figures/fig3_ame.pdf")
plt.close(fig)

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
ax.tick_params(length=0)
fig.tight_layout()
fig.savefig("report/figures/fig4_age_profile.pdf")
plt.close(fig)

# ---------- Figure 5: high-risk decile vs all teachers (dumbbell) ----------
df["phat"] = m.predict(df)
hi10 = df.nlargest(len(df) // 10, "phat")
traits = ["parttime", "ma_plus", "preschool_kg", "female", "married",
          "hispanic", "black"]
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
ax.tick_params(length=0)
ax.yaxis.grid(False)
handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=c)
           for c in (BLUE, GOLD)]
ax.legend(handles, ["All teachers", "Highest-risk decile"],
          loc="lower right", frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("report/figures/fig5_profile.pdf")
plt.close(fig)

# ---------- LaTeX regression table ----------
coefs = m.params
ses = m.bse
pvals = m.pvalues


def stars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


LABELS_TEX = {**LABELS,
              "faminc75k": "Family income \\$75k+",
              "parttime": "Part-time ($<$35 h/week)"}
rows = []
for v in COVS:
    rows.append(
        f"{LABELS_TEX[v]} & {coefs[v]:.3f}{stars(pvals[v])} & ({ses[v]:.3f}) & "
        f"{ame.loc[v,'AME']:+.2f}{stars(ame.loc[v,'p'])} \\\\")
table = "\n".join(rows)
with open("report/table_probit.tex", "w") as f:
    f.write(f"""\\begin{{tabular}}{{lccc}}
\\toprule
 & Probit coef. & (SE) & AME (pp) \\\\
\\midrule
{table}
\\midrule
Constant & {coefs['Intercept']:.3f}{stars(pvals['Intercept'])} & ({ses['Intercept']:.3f}) & \\\\
Base-year fixed effects & \\multicolumn{{3}}{{c}}{{Yes}} \\\\
Observations & \\multicolumn{{3}}{{c}}{{{int(m.nobs):,}}} \\\\
Pseudo $R^2$ & \\multicolumn{{3}}{{c}}{{{m.prsquared:.3f}}} \\\\
\\bottomrule
\\end{{tabular}}
""")

print("figures + table written to report/")
print(f"attrition {sample_line:.1f}% | decile mean phat {hi10['phat'].mean():.1%}")
