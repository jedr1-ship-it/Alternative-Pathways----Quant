"""
Probit models of teacher attrition on the linked CPS panel (2005 -> 2025).

Main outcome (definition B): PERSISTENT leaver — taught in month t, not an
employed school teacher at t+12, and not observed teaching in any of the
up-to-3 monthly re-interviews after t+12. Defined on the subsample with a
potential follow-up interview (baseline MIS 1-3).

Robustness (definition A): standard 12-month leaver on the full sample,
comparable with the NCES TFS convention.

Sample: school teachers with a bachelor's degree or higher. Covariates at t;
base-year fixed effects; cluster-robust SE by household.
Requires: 02_build_cps_panel.py then 05_evolution.py (exports return flags).
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from covariates import load_panel, COVS

df = load_panel()
B = df[df["sampleB"]].copy()

report = []
def log(*a):
    line = " ".join(str(x) for x in a); print(line); report.append(line)

wB, wA = B["PWSSWGT_0"], df["PWSSWGT_0"]
log("=" * 70)
log("TEACHER ATTRITION, LINKED CPS PANEL 2005->2025 (teachers with BA+)")
log("=" * 70)
log(f"Full sample (A)             : {len(df):,}")
log(f"Follow-up sample (B)        : {len(B):,}  (baseline MIS 1-3)")
log(f"12-month attrition (A, wtd) : {np.average(df['leaver12'], weights=wA):6.2%}")
log(f"12-month attrition (B smpl) : {np.average(B['leaver12'], weights=wB):6.2%}")
log(f"PERSISTENT attrition (B)    : {np.average(B['leaver_p'], weights=wB):6.2%}")

log("\nDestination at t+12, persistent leavers only (weighted % of teachers):")
for d in ["other occupation", "out of labor force", "unemployed"]:
    v = np.average((B["dest"].eq(d) & (B["leaver_p"] == 1)).astype(float),
                   weights=wB) * 100
    log(f"  {d:20s}: {v:5.2f}")

prof = B.groupby("leaver_p")[COVS].mean().T
prof.columns = ["stayer", "leaver"]
prof["diff"] = prof["leaver"] - prof["stayer"]
log("\n--- Mean characteristics at t: stayer vs persistent leaver ---")
log(prof.round(3).to_string())

# ---------- main probit: persistent leaver ----------
rhs = " + ".join(COVS) + " + C(base_year)"
mB = smf.probit("leaver_p ~ " + rhs, data=B).fit(
    cov_type="cluster", cov_kwds={"groups": B["HRHHID"]}, disp=False)
log("\n--- MAIN probit: persistent leaver (B), cluster SE, year FE ---")
log(mB.summary2().tables[1].round(4).to_string())

me = mB.get_margeff(at="overall")
mtab = pd.DataFrame({"AME": me.margeff, "se": me.margeff_se,
                     "z": me.tvalues, "p": me.pvalues},
                    index=me.summary_frame().index)
mtab = mtab.reindex(mtab["z"].abs().sort_values(ascending=False).index)
log("\n--- AMEs, persistent leaver (pp), ranked ---")
log((mtab.assign(AME_pp=mtab["AME"] * 100)
         [["AME_pp", "se", "z", "p"]].round(4)).to_string())

# ---------- robustness: 12-month leaver, full sample ----------
mA = smf.probit("leaver12 ~ " + rhs, data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["HRHHID"]}, disp=False)
meA = mA.get_margeff(at="overall")
ameA = pd.Series(meA.margeff * 100, index=meA.summary_frame().index)
comp = pd.DataFrame({
    "AME_B_persistent": mtab["AME"] * 100,
    "AME_A_12month": ameA}).loc[[c for c in COVS]]
log("\n--- AME comparison: B (main) vs A (robustness) ---")
log(comp.round(2).to_string())

top = mtab.drop(index=[i for i in mtab.index if "base_year" in i]).index[0]
log(f"\nStrongest predictor (B): {top} "
    f"(AME = {mtab.loc[top,'AME']*100:+.2f} pp, p = {mtab.loc[top,'p']:.4f})")

B["phat"] = mB.predict(B)
hi = B.nlargest(len(B) // 10, "phat")
log("\n--- Highest-risk decile profile (persistent leaver) ---")
log(hi[COVS].mean().round(3).to_string())
log(f"mean predicted P in decile: {hi['phat'].mean():.2%} "
    f"vs sample {B['phat'].mean():.2%}")

with open("outputs/cps_attrition_report.txt", "w") as f:
    f.write("\n".join(report))
prof.round(4).to_csv("outputs/cps_profile_stayer_vs_leaver.csv")
mtab.round(5).to_csv("outputs/cps_marginal_effects.csv")
comp.round(4).to_csv("outputs/cps_ame_A_vs_B.csv")
log("\nsaved outputs/*")
