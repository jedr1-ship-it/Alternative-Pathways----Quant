"""
Probit model of teacher attrition on the linked CPS panel (2024 -> 2025).

Outcome: leaver = taught in month t (2024) and is NOT an employed school
teacher 12 months later. Covariates measured at t. Cluster-robust SE by
household (CPS samples households). Survey-weighted rates are reported
descriptively; the probit is unweighted (standard practice: weights matter
for population rates, little for conditional coefficients).
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv("data/processed/cps_teacher_panel.csv",
                 dtype={"HRHHID": str, "HRHHID2": str})

# --- covariates at t ---
df["age"] = df["PRTAGE_0"]
df["age2"] = df["age"] ** 2 / 100.0
df["female"] = (df["PESEX_0"] == 2).astype(int)
df["married"] = df["PEMARITL_0"].isin([1, 2]).astype(int)
df["black"] = (df["PTDTRACE_0"] == 2).astype(int)
df["hispanic"] = (df["PEHSPNON_0"] == 1).astype(int)
df["noncitizen"] = (df["PRCITSHP_0"] == 5).astype(int)
# PEEDUCA: 43 = bachelor's, 44 = master's, 45 = professional, 46 = doctorate
df["ba"] = (df["PEEDUCA_0"] == 43).astype(int)
df["ma_plus"] = (df["PEEDUCA_0"] >= 44).astype(int)
# usual weekly hours; -4 = "hours vary", negatives = missing
df["hours"] = df["PEHRUSL1_0"].where(df["PEHRUSL1_0"] > 0)
df["parttime"] = (df["hours"] < 35).astype(int)
df["hours_missing"] = df["hours"].isna().astype(int)
df["parttime"] = df["parttime"].fillna(0)
# family income bands: HEFAMINC 13+ = $75,000 or more
df["faminc75k"] = (df["HEFAMINC_0"] >= 13).astype(int)
# teaching level at t (ref: elementary/middle 2310)
df["preschool_kg"] = (df["PTIO1OCD_0"] == 2300).astype(int)
df["secondary"] = (df["PTIO1OCD_0"] == 2320).astype(int)
df["special_ed"] = (df["PTIO1OCD_0"] == 2330).astype(int)

covs = ["age", "age2", "female", "married", "black", "hispanic", "noncitizen",
        "ba", "ma_plus", "parttime", "hours_missing", "faminc75k",
        "preschool_kg", "secondary", "special_ed"]

report = []
def log(*a):
    line = " ".join(str(x) for x in a); print(line); report.append(line)

w = df["PWSSWGT_0"]
log("=" * 70)
log("TEACHER ATTRITION, LINKED CPS PANEL 2024->2025 (official microdata)")
log("=" * 70)
log(f"Teachers followed 12 months : {len(df):,}")
log(f"Attrition rate  (weighted)  : {np.average(df['leaver'], weights=w):6.2%}")
log(f"Attrition rate  (unweighted): {df['leaver'].mean():6.2%}")
log("\nDestination at t+12 (weighted %):")
dest = (df.groupby("dest")["PWSSWGT_0"].sum() / w.sum() * 100).round(2)
log(dest.to_string())
log("\nNOTE: 'other occupation' in the CPS is inflated by independent")
log("re-coding of occupation at the second rotation; treat levels with")
log("caution, comparisons across characteristics remain informative.")

# --- descriptive profile ---
prof = df.groupby("leaver")[covs].mean().T
prof.columns = ["stayer", "leaver"]
prof["diff"] = prof["leaver"] - prof["stayer"]
log("\n--- Mean characteristics at t: stayer vs leaver ---")
log(prof.round(3).to_string())

# --- probit, cluster-robust by household ---
formula = "leaver ~ " + " + ".join(covs)
m = smf.probit(formula, data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["HRHHID"]}, disp=False)
log("\n--- Probit (cluster-robust SE by household) ---")
log(m.summary2().tables[1].round(4).to_string())

me = m.get_margeff(at="overall")
mtab = pd.DataFrame({"AME": me.margeff, "se": me.margeff_se,
                     "z": me.tvalues, "p": me.pvalues},
                    index=me.summary_frame().index)
mtab = mtab.reindex(mtab["z"].abs().sort_values(ascending=False).index)
log("\n--- Average marginal effects (pp change in P(leave)), ranked ---")
log((mtab.assign(AME_pp=mtab["AME"] * 100)
         .drop(columns="AME")[["AME_pp", "se", "z", "p"]]
         .round(4)).to_string())

top = mtab.index[0]
log(f"\nStrongest predictor: {top} (AME = {mtab.loc[top,'AME']*100:+.2f} pp, "
    f"p = {mtab.loc[top,'p']:.4f})")

# --- typical leaver: highest predicted-risk decile ---
df["phat"] = m.predict(df)
hi = df.nlargest(max(len(df) // 10, 1), "phat")
log("\n--- Profile of the highest-risk decile ('typical leaver') ---")
log(hi[["age"] + covs[2:]].mean().round(3).to_string())
log(f"mean predicted P(leave) in decile: {hi['phat'].mean():.2%} "
    f"vs sample {df['phat'].mean():.2%}")

with open("outputs/cps_attrition_report.txt", "w") as f:
    f.write("\n".join(report))
prof.round(4).to_csv("outputs/cps_profile_stayer_vs_leaver.csv")
mtab.round(5).to_csv("outputs/cps_marginal_effects.csv")
log("\nsaved outputs/cps_attrition_report.txt, cps_profile_stayer_vs_leaver.csv, cps_marginal_effects.csv")
