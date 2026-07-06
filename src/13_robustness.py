"""
Robustness of the main estimates to the choice of estimator and sample:
probit AMEs (baseline) vs logit AMEs vs the linear probability model, plus
the probit excluding the pandemic years. Writes report/table_robustness.tex.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from covariates import load_panel, COVS, LABELS

df = load_panel()
B = df[df["sampleB"]].copy()
rhs = " + ".join(COVS) + " + C(base_year)"

SHOW = ["parttime", "public", "prof_phd", "ma_plus", "black", "noncitizen",
        "new_baby", "fem_newbaby", "n_children", "faminc75k", "female"]


def stars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


def ame_frame(model):
    me = model.get_margeff(at="overall")
    idx = list(me.summary_frame().index)
    return {v: (me.margeff[idx.index(v)] * 100,
                me.margeff_se[idx.index(v)] * 100,
                me.pvalues[idx.index(v)]) for v in SHOW}


print("probit ...", flush=True)
mP = smf.probit("leaver_p ~ " + rhs, data=B).fit(
    cov_type="cluster", cov_kwds={"groups": B["HRHHID"]}, disp=False)
aP = ame_frame(mP)
print("logit ...", flush=True)
mL = smf.logit("leaver_p ~ " + rhs, data=B).fit(
    cov_type="cluster", cov_kwds={"groups": B["HRHHID"]}, disp=False)
aL = ame_frame(mL)
print("lpm ...", flush=True)
mO = smf.ols("leaver_p ~ " + rhs, data=B).fit(
    cov_type="cluster", cov_kwds={"groups": B["HRHHID"]})
aO = {v: (mO.params[v] * 100, mO.bse[v] * 100, mO.pvalues[v]) for v in SHOW}
print("probit excl. 2019-2021 ...", flush=True)
Bx = B[~B["base_year"].isin([2019, 2020, 2021])]
mX = smf.probit("leaver_p ~ " + rhs, data=Bx).fit(
    cov_type="cluster", cov_kwds={"groups": Bx["HRHHID"]}, disp=False)
aX = ame_frame(mX)

LABELS_TEX = {**LABELS,
              "faminc75k": "Family income \\$75k+",
              "parttime": "Part-time ($<$35 h/week)"}
with open("report/table_robustness.tex", "w") as fh:
    fh.write("""\\begin{tabular}{lcccc}
\\toprule
 & (1) & (2) & (3) & (4) \\\\
 & Probit & Logit & Linear probability & Probit, excl. \\\\
 & (baseline) & & model & 2019--2021 \\\\
\\midrule
""")
    for v in SHOW:
        row, serow = [LABELS_TEX[v]], [""]
        for a in (aP, aL, aO, aX):
            est, se, p = a[v]
            row.append(f"{est:.2f}{stars(p)}")
            serow.append(f"({se:.2f})")
        fh.write(" & ".join(row) + " \\\\\n")
        fh.write(" & ".join(serow) + " \\\\[2pt]\n")
    fh.write(f"""\\midrule
Base-year fixed effects & Yes & Yes & Yes & Yes \\\\
Full covariate set & Yes & Yes & Yes & Yes \\\\
Observations & {int(mP.nobs):,} & {int(mL.nobs):,} & {int(mO.nobs):,} & {int(mX.nobs):,} \\\\
\\bottomrule
\\end{{tabular}}
""")
print("wrote report/table_robustness.tex")
comp = pd.DataFrame({"probit": {v: aP[v][0] for v in SHOW},
                     "logit": {v: aL[v][0] for v in SHOW},
                     "lpm": {v: aO[v][0] for v in SHOW},
                     "noCovid": {v: aX[v][0] for v in SHOW}})
print(comp.round(2).to_string())
comp.round(3).to_csv("outputs/robustness_estimators.csv")
