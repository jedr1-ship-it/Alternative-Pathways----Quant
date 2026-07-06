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

# ---------- weighted descriptive table for the brief ----------
B["elem"] = ((B["preschool_kg"] + B["secondary"] + B["special_ed"]) == 0).astype(int)
DESC = [
    ("Age, years", "age", "num"),
    ("Female", "female", "pct"),
    ("Female aged 25--44", "fem_fertile", "pct"),
    ("Married", "married", "pct"),
    ("Number of own children ($<$18) at home", "n_children", "num"),
    ("Child under 6 at home", "child_u6", "pct"),
    ("New baby during the year", "new_baby", "pct"),
    ("Black", "black", "pct"),
    ("Hispanic", "hispanic", "pct"),
    ("Non-citizen", "noncitizen", "pct"),
    ("Master's degree or higher", "ma_plus", "pct"),
    ("Professional degree or doctorate", "prof_phd", "pct"),
    ("Part-time ($<$35 h/week)", "parttime", "pct"),
    ("Holds more than one job", "multjob", "pct"),
    ("Public-sector employer", "public", "pct"),
    ("Family income \\$75k+", "faminc75k", "pct"),
    ("Elementary / middle school", "elem", "pct"),
    ("Preschool / kindergarten", "preschool_kg", "pct"),
    ("Secondary school", "secondary", "pct"),
    ("Special education", "special_ed", "pct"),
]
groups = [("All teachers", B), ("Stayers", B[B["leaver_p"] == 0]),
          ("Persistent leavers", B[B["leaver_p"] == 1])]


def dstars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


# economic relevance thresholds for highlighting: at least 2 pp for shares,
# one year of age, or 0.15 children
ECON_MIN = {"pct": 0.02, "num": 1.0}
ECON_MIN_VAR = {"n_children": 0.15}

with open("report/table_descriptives.tex", "w") as fh:
    fh.write("\\begin{tabular}{lcccc}\n\\toprule\n & "
             + " & ".join(g for g, _ in groups)
             + " & Difference \\\\\n\\midrule\n")
    for lab, v, kind in DESC:
        cells = []
        for _, g in groups:
            m = np.average(g[v], weights=g["PWSSWGT_0"])
            cells.append(f"{m*100:.1f}\\%" if kind == "pct" else f"{m:.1f}")
        # test of the stayer-leaver difference, household-clustered SE
        t = smf.wls(f"{v} ~ leaver_p", data=B, weights=B["PWSSWGT_0"]).fit(
            cov_type="cluster", cov_kwds={"groups": B["HRHHID"]})
        d, p = t.params["leaver_p"], t.pvalues["leaver_p"]
        dtxt = (f"{d*100:+.1f}\\,pp" if kind == "pct" else f"{d:+.2f}")
        dtxt += dstars(p)
        thr = ECON_MIN_VAR.get(v, ECON_MIN[kind])
        if p < 0.05 and abs(d) >= thr:
            dtxt = "\\cellcolor{sigok}" + dtxt
        cells.append(dtxt)
        fh.write(f"{lab} & " + " & ".join(cells) + " \\\\\n")
    fh.write("\\midrule\nPersons & "
             + " & ".join(f"{len(g):,}" for _, g in groups)
             + " & \\\\\n\\bottomrule\n\\end{tabular}\n")
log("wrote report/table_descriptives.tex")

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

# ---------- destination of leavers with a new baby ----------
nb = B[(B["leaver_p"] == 1) & (B["new_baby"] == 1) & (B["female"] == 1)]
if len(nb) > 50:
    sh = (nb.groupby("dest")["PWSSWGT_0"].sum()
            / nb["PWSSWGT_0"].sum() * 100).round(1)
    log(f"\n--- Women leavers with a new baby (n={len(nb)}), destination ---")
    log(sh.to_string())

# ---------- wage sub-analysis (earnings only asked at MIS 4/8) ----------
# baseline earnings exist only for teachers whose first linked interview is
# their 4th month in sample, so this runs on the 12-month definition
Wg = df[(df["HRMIS_0"] == 4) & df["wkearn"].notna()].copy()
Wg["log_wkearn"] = np.log(Wg["wkearn"].clip(lower=50))
mW = smf.probit("leaver12 ~ log_wkearn + " + rhs, data=Wg).fit(
    cov_type="cluster", cov_kwds={"groups": Wg["HRHHID"]}, disp=False)
meW = mW.get_margeff(at="overall")
iW = list(meW.summary_frame().index).index("log_wkearn")
log(f"\n--- Wage sub-model (MIS-4 subsample, n={len(Wg):,}) ---")
log(f"AME of log weekly earnings: {meW.margeff[iW]*100:+.2f} pp "
    f"(p={meW.pvalues[iW]:.4f})")
log("(a 10% higher weekly wage changes P(leave) by "
    f"{meW.margeff[iW]*100*0.10:+.2f} pp)")

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
