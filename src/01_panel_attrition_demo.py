"""
Panel occupational-exit analysis — methodological pipeline.

Goal of the wider project: predict who LEAVES a profession using longitudinal
micro-data that follows the SAME individuals over time, then profile the typical
leaver with a probit.

Because the teacher-specific longitudinal sources (NCES SASS/TFS, CPS, PSID full)
are blocked by this environment's egress policy, this script builds and validates
the ENTIRE machinery on a genuine, openly downloadable panel: the PSID Earnings
Panel 1976-1982 (AER::PSID7682), 595 individuals x 7 years.

Here "leaving the profession" is operationalised as an occupational EXIT:
being a white-collar worker in year t and NOT a white-collar worker in t+1.
Swap PSID7682 for a teacher-coded panel and the same code answers the real
research question.
"""
import os
import urllib.request
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

URL = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
       "master/csv/AER/PSID7682.csv")
RAW = "data/raw/PSID7682.csv"
OUT = "outputs"

# self-download the panel if not present (only GitHub is reachable here)
os.makedirs("data/raw", exist_ok=True)
os.makedirs(OUT, exist_ok=True)
if not os.path.exists(RAW):
    print(f"downloading {URL}")
    urllib.request.urlretrieve(URL, RAW)

df = pd.read_csv(RAW)
df = df.rename(columns={c: c.strip() for c in df.columns})

# --- tidy factors -> clean 0/1 ---
def yn(s):  # "yes"/"no" -> 1/0
    return (s.astype(str).str.lower().str.strip() == "yes").astype(int)

df["white_collar"] = (df["occupation"].astype(str).str.lower() == "white").astype(int)
df["manufacturing"] = yn(df["industry"])
df["south"] = yn(df["south"])
df["smsa"] = yn(df["smsa"])
df["married"] = yn(df["married"])
df["union"] = yn(df["union"])
df["afam"] = (df["ethnicity"].astype(str).str.lower() == "afam").astype(int)
df["female"] = (df["gender"].astype(str).str.lower() == "female").astype(int)
df["lwage"] = np.log(df["wage"].clip(lower=1))

df = df.sort_values(["id", "year"]).reset_index(drop=True)

# --- build t -> t+1 transitions (only consecutive years) ---
df["year_next"] = df.groupby("id")["year"].shift(-1)
df["wc_next"] = df.groupby("id")["white_collar"].shift(-1)
trans = df[(df["year_next"] == df["year"] + 1)].copy()   # valid one-year link

# occupational mobility overview
n_pairs = len(trans)
switch = (trans["white_collar"] != trans["wc_next"]).mean()
report = []
def log(*a):
    line = " ".join(str(x) for x in a); print(line); report.append(line)

log("=" * 68)
log("PANEL OCCUPATIONAL-EXIT ANALYSIS  (PSID 1976-1982, real panel)")
log("=" * 68)
log(f"Individuals            : {df['id'].nunique()}")
log(f"Person-years           : {len(df)}")
log(f"Linked t->t+1 pairs    : {n_pairs}")
log(f"Any occupation switch  : {switch:6.2%} of pairs")

# --- sample at risk: white-collar in t, observed in t+1 ---
risk = trans[trans["white_collar"] == 1].copy()
risk["leave"] = (risk["wc_next"] == 0).astype(int)
log(f"\nAt-risk (white-collar in t): {len(risk)} person-years")
log(f"EXIT rate (white->non-white): {risk['leave'].mean():6.2%}")

# --- descriptive profile: leavers vs stayers ---
covs = ["experience", "weeks", "education", "lwage",
        "union", "married", "south", "smsa", "manufacturing", "afam", "female"]
prof = risk.groupby("leave")[covs].mean().T
prof.columns = ["stayer", "leaver"]
prof["diff"] = prof["leaver"] - prof["stayer"]
log("\n--- Mean characteristics: stayer vs leaver ---")
log(prof.round(3).to_string())

# --- probit: P(leave | characteristics at t), cluster SE by individual ---
formula = ("leave ~ experience + weeks + education + lwage + union + married "
           "+ south + smsa + manufacturing + afam + female")
m = smf.probit(formula, data=risk).fit(
    cov_type="cluster", cov_kwds={"groups": risk["id"]}, disp=False)
log("\n--- Probit (cluster-robust SE by individual) ---")
log(m.summary2().tables[1].round(4).to_string())

# --- average marginal effects + ranking ---
me = m.get_margeff(at="overall")
mtab = pd.DataFrame({"AME": me.margeff, "se": me.margeff_se,
                     "z": me.tvalues, "p": me.pvalues},
                    index=me.summary_frame().index)
mtab["abs_z"] = mtab["z"].abs()
mtab = mtab.sort_values("abs_z", ascending=False)
log("\n--- Average marginal effects, ranked by |z| ---")
log(mtab.round(4).to_string())
top = mtab.index[0]
log(f"\nStrongest predictor of exit : {top} "
    f"(AME={mtab.loc[top,'AME']:+.4f}, p={mtab.loc[top,'p']:.3f})")

# --- "typical leaver" via predicted probability ---
risk = risk.copy()
risk["phat"] = m.predict(risk)
hi = risk.nlargest(int(len(risk) * 0.10), "phat")
log("\n--- Profile of highest-risk decile (typical leaver) ---")
log(hi[covs].mean().round(3).to_string())

with open(f"{OUT}/panel_attrition_report.txt", "w") as f:
    f.write("\n".join(report))
prof.round(4).to_csv(f"{OUT}/profile_stayer_vs_leaver.csv")
mtab.round(5).to_csv(f"{OUT}/marginal_effects.csv")
log(f"\nSaved: {OUT}/panel_attrition_report.txt, profile_stayer_vs_leaver.csv, marginal_effects.csv")
