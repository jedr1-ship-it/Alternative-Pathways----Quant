"""
Is teaching family friendly? The effect of a new baby on leaving one's
profession, estimated with the same linked design profession by
profession, for women (and men as the placebo). Probits with age, age
squared, marital status, an advanced-degree indicator and base-year fixed
effects, standard errors clustered by household. Writes
report/figures/fig18_family_professions.pdf and outputs/family_professions.csv.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

from paperstyle import *

P = pd.read_csv("data/processed/professions_pairs.csv")
P["age2"] = P["age"] ** 2

GROUPS = ["Teachers", "Registered nurses", "Social workers",
          "Accountants and auditors"]
RHS = "new_baby + age + age2 + married + ma_plus + C(base_year)"

rows = []
for g in GROUPS:
    for sex, lab in [(1, "Women"), (0, "Men")]:
        d = P[(P["group"] == g) & (P["female"] == sex)]
        if d["new_baby"].sum() < 100:
            continue
        for y in ["leave", "dest_occ", "dest_olf"]:
            m = smf.probit(f"{y} ~ " + RHS, data=d).fit(
                cov_type="cluster", cov_kwds={"groups": d["HRHHID"]},
                disp=False)
            me = m.get_margeff(at="overall")
            idx = list(me.summary_frame().index)
            i = idx.index("new_baby")
            rows.append({"group": g, "sex": lab, "outcome": y,
                         "ame": me.margeff[i] * 100,
                         "se": me.margeff_se[i] * 100,
                         "p": me.pvalues[i], "n": len(d),
                         "babies": int(d["new_baby"].sum())})
            print(f"{g:26s} {lab:6s} {y:9s} "
                  f"AME {me.margeff[i]*100:+6.2f} "
                  f"(se {me.margeff_se[i]*100:.2f}) n={len(d):,} "
                  f"babies={int(d['new_baby'].sum())}", flush=True)

res = pd.DataFrame(rows)
res.round(3).to_csv("outputs/family_professions.csv", index=False)

# ---------- figure: women, effect of a new baby on leaving, by profession --
W = res[(res.sex == "Women") & (res.outcome == "leave")]
O = res[(res.sex == "Women") & (res.outcome == "dest_olf")]
order = ["Teachers", "Registered nurses", "Social workers",
         "Accountants and auditors"]
SHORT = {"Teachers": "Teachers", "Registered nurses": "Registered nurses",
         "Social workers": "Social workers",
         "Accountants and auditors": "Accountants"}
fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.0), sharey=True)
for ax, dd, title in [(axes[0], W, "Leave the profession"),
                      (axes[1], O, "Leave the labor force")]:
    yy = np.arange(len(order))[::-1]
    for yi, g in zip(yy, order):
        r = dd[dd.group == g]
        if r.empty:
            continue
        r = r.iloc[0]
        lo, hi = r.ame - 1.96 * r.se, r.ame + 1.96 * r.se
        c = BLUE if g == "Teachers" else GRAY
        ax.plot([lo, hi], [yi, yi], color=c, lw=2, solid_capstyle="round")
        ax.scatter([r.ame], [yi], s=52, color=c, zorder=4,
                   edgecolor=SURFACE, linewidth=1.5)
        ax.text(r.ame, yi + 0.28, f"{r.ame:.1f}", ha="center", fontsize=9,
                fontweight="bold", color=INK)
    ax.axvline(0, color=SUBTLE, lw=1)
    ax.set_yticks(yy, [SHORT[g] for g in order], fontsize=9.5)
    ax.set_title(title, fontsize=10.5, fontweight="bold", loc="left")
    ax.set_xlabel("Effect of a new baby, pp")
fig.tight_layout(w_pad=2)
fig.savefig("report/figures/fig18_family_professions.pdf",
            bbox_inches="tight")
plt.close(fig)
print("fig18 saved")
