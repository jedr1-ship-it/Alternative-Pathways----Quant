"""
Probit model of teacher attrition on the linked CPS panel (2021 -> 2025).

Outcome: leaver = taught in month t and is NOT an employed school teacher
12 months later. Sample: school teachers with a bachelor's degree or higher.
Covariates measured at t; base-year fixed effects; cluster-robust SE by
household. Survey-weighted rates reported descriptively.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from covariates import add_covariates, COVS

df = pd.read_csv("data/processed/cps_teacher_panel.csv",
                 dtype={"HRHHID": str, "HRHHID2": str})
df = add_covariates(df)

report = []
def log(*a):
    line = " ".join(str(x) for x in a); print(line); report.append(line)

w = df["PWSSWGT_0"]
log("=" * 70)
log("TEACHER ATTRITION, LINKED CPS PANEL 2021->2025 (teachers with BA+)")
log("=" * 70)
log(f"Teachers followed 12 months : {len(df):,}")
log("By base year                :",
    df.groupby("base_year").size().to_dict())
log(f"Attrition rate  (weighted)  : {np.average(df['leaver'], weights=w):6.2%}")
log(f"Attrition rate  (unweighted): {df['leaver'].mean():6.2%}")
log("\nDestination at t+12 (weighted %):")
log((df.groupby("dest")["PWSSWGT_0"].sum() / w.sum() * 100).round(2).to_string())
log("\nAttrition by base year (weighted %):")
log(df.groupby("base_year").apply(
    lambda g: np.average(g["leaver"], weights=g["PWSSWGT_0"]) * 100,
    include_groups=False).round(1).to_string())

prof = df.groupby("leaver")[COVS].mean().T
prof.columns = ["stayer", "leaver"]
prof["diff"] = prof["leaver"] - prof["stayer"]
log("\n--- Mean characteristics at t: stayer vs leaver ---")
log(prof.round(3).to_string())

formula = "leaver ~ " + " + ".join(COVS) + " + C(base_year)"
m = smf.probit(formula, data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["HRHHID"]}, disp=False)
log("\n--- Probit (cluster-robust SE by household, year FE) ---")
log(m.summary2().tables[1].round(4).to_string())

me = m.get_margeff(at="overall")
mtab = pd.DataFrame({"AME": me.margeff, "se": me.margeff_se,
                     "z": me.tvalues, "p": me.pvalues},
                    index=me.summary_frame().index)
mtab = mtab.reindex(mtab["z"].abs().sort_values(ascending=False).index)
log("\n--- Average marginal effects (pp change in P(leave)), ranked ---")
log((mtab.assign(AME_pp=mtab["AME"] * 100)
         [["AME_pp", "se", "z", "p"]].round(4)).to_string())

top = mtab.drop(index=[i for i in mtab.index if "base_year" in i]).index[0]
log(f"\nStrongest predictor: {top} (AME = {mtab.loc[top,'AME']*100:+.2f} pp, "
    f"p = {mtab.loc[top,'p']:.4f})")

df["phat"] = m.predict(df)
hi = df.nlargest(len(df) // 10, "phat")
log("\n--- Profile of the highest-risk decile ('typical leaver') ---")
log(hi[COVS].mean().round(3).to_string())
log(f"mean predicted P(leave) in decile: {hi['phat'].mean():.2%} "
    f"vs sample {df['phat'].mean():.2%}")

with open("outputs/cps_attrition_report.txt", "w") as f:
    f.write("\n".join(report))
prof.round(4).to_csv("outputs/cps_profile_stayer_vs_leaver.csv")
mtab.round(5).to_csv("outputs/cps_marginal_effects.csv")
log("\nsaved outputs/*")
