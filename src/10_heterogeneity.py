"""
Heterogeneity: the persistent-leaver probit estimated on subsamples
(women/men, public/private, under 40 / 40 plus). Produces
fig15_heterogeneity.pdf with AMEs and 95% CIs for key predictors.
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from covariates import load_panel, COVS, LABELS

from paperstyle import *

df = load_panel()
B = df[df["sampleB"]].copy()

SPLITS = [
    ("By sex", [("Women", B[B.female == 1], CORAL),
                ("Men", B[B.female == 0], BLUE)],
     {"female", "fem_child_u6", "fem_newbaby"}),
    ("By sector", [("Public", B[B.public == 1], BLUE),
                   ("Private", B[B.public == 0], GOLD)],
     {"public"}),
    ("By age", [("Under 40", B[B.age < 40], GREEN),
                ("40 and older", B[B.age >= 40], NAVY)],
     set()),
]
SHOW = ["public", "new_baby", "child_u6", "black", "ma_plus"]
# the birth and young-child effects are sex-specific (the pooled models keep
# the female interactions), so they are only displayed in the sex panel
SHOW_BY_SPLIT = {
    "By sex": SHOW,
    "By sector": ["black", "ma_plus"],
    "By age": ["public", "black", "ma_plus"],
}

results = []
for split, groups, drop in SPLITS:
    rhs = " + ".join([v for v in COVS if v not in drop]) + " + C(base_year)"
    for gname, g, color in groups:
        m = smf.probit("leaver_p ~ " + rhs, data=g).fit(
            cov_type="cluster", cov_kwds={"groups": g["HRHHID"]}, disp=False)
        me = m.get_margeff(at="overall")
        idx = list(me.summary_frame().index)
        for v in SHOW:
            if v in drop or v not in idx:
                continue
            i = idx.index(v)
            results.append({"split": split, "group": gname, "color": color,
                            "var": v, "ame": me.margeff[i] * 100,
                            "se": me.margeff_se[i] * 100,
                            "p": me.pvalues[i], "n": len(g)})
        print(f"{split} / {gname}: n={len(g):,} done", flush=True)
res = pd.DataFrame(results)
res.round(4).to_csv("outputs/heterogeneity_ames.csv", index=False)

# ---------- figure: one panel per split ----------
# short row labels so the panels keep as much x-axis room as possible
SHORT = {"parttime": "Part-time", "public": "Public sector",
         "new_baby": "New baby", "child_u6": "Child under 6",
         "black": "Black", "ma_plus": "Master's degree+"}
fig, axes = plt.subplots(1, 3, figsize=(10.0, 4.6), sharey=False)
for ax, (split, groups, drop) in zip(axes, SPLITS):
    sub = res[res["split"] == split]
    vars_here = [v for v in SHOW_BY_SPLIT[split] if v not in drop]
    y = 0.0
    ypos, ylab = [], []
    for v in vars_here:
        for gname, _, color in groups:
            r = sub[(sub["var"] == v) & (sub["group"] == gname)]
            if r.empty:
                continue
            r = r.iloc[0]
            lo, hi = r.ame - 1.96 * r.se, r.ame + 1.96 * r.se
            a = 1.0 if r.p < 0.05 else 0.45
            ax.plot([lo, hi], [y, y], color=r.color, lw=2, alpha=a,
                    solid_capstyle="round")
            ax.scatter([r.ame], [y], s=46, color=r.color, alpha=a, zorder=4,
                       edgecolor=SURFACE, linewidth=1.5)
            y -= 0.62
        ypos.append(y + 0.62 * len(groups) / 2 + 0.31)
        ylab.append(SHORT[v])
        y -= 0.55
    ax.axvline(0, color=SUBTLE, lw=1, zorder=2)
    ax.set_xlim(-12, 16)
    ax.set_xticks([-10, -5, 0, 5, 10, 15])
    ax.tick_params(axis="x", labelsize=8.5)
    ax.set_yticks(ypos, ylab, fontsize=9)
    ax.set_title(split, loc="left", fontsize=10.5, color=NAVY,
                 fontweight="bold", pad=8)
    ax.yaxis.grid(False)
    handles = [plt.Line2D([], [], marker="o", ls="", ms=7, color=c)
               for _, _, c in groups]
    ax.legend(handles, [g for g, *_ in groups], loc="upper center",
              bbox_to_anchor=(0.5, -0.10), ncols=2, frameon=False,
              fontsize=8.5)
axes[1].set_xlabel("Change in P(leaving teaching), "
                   "percentage points")
fig.tight_layout(w_pad=1.6)
fig.savefig("report/figures/fig15_heterogeneity.pdf", bbox_inches="tight")
print("\nsaved fig15; key contrasts:")
for v in ["new_baby", "public"]:
    s = res[res["var"] == v][["split", "group", "ame", "p"]]
    print(v); print(s.round(2).to_string(index=False))
