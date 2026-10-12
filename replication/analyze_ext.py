"""Block 2 and Block 3 computations on the extended ASEC file.
Writes:
  outputs/flow_unified.csv        - of every 100 leavers, 5-year average,
                                    master segments + the under-55 OLF
                                    opening (demography and activity)
  outputs/lpm_results.csv         - LPM (year FE main; no FE; state FE),
                                    logit and probit AMEs
  outputs/lpm_fitted_check.csv    - share of fitted values outside [0,1]
Run from the repo root after replication/build_asec_ext.py."""
import numpy as np
import pandas as pd
import statsmodels.api as sm

d = pd.read_parquet("data/processed/asec_ext.parquet")
d["cal_year"] = d.asec_year - 1

# ---------- derivations (master conventions) ----------
def tset(ay):
    return {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360})

d["teach_ly"] = False
d["teach_now"] = False
for ay, g in d.groupby("asec_year"):
    s = tset(int(ay))
    d.loc[g.index, "teach_ly"] = g.OCCUP.isin(s)
    d.loc[g.index, "teach_now"] = g.PEIOOCC.isin(s)
d["ba_plus"] = d.A_HGA >= 43
d["ma_plus"] = d.A_HGA >= 44
emp = d.A_LFSR.isin([1, 2])
d["switch"] = emp & ~d.teach_now
d["unemp"] = d.A_LFSR.isin([3, 4])
d["leftlf"] = d.A_LFSR.isin([5, 6, 7])
d["leaver"] = (d.switch | d.unemp | d.leftlf).astype(float)
d["female"] = (d.A_SEX == 2).astype(float)
d["black"] = (d.PRDTRACE == 2).astype(float)
d["married"] = d.A_MARITL.isin([1, 2, 3]).astype(float)
d["sepdiv"] = d.A_MARITL.isin([4, 5]).astype(float)
d["pension"] = (d.PENPLAN == 1).astype(float)          # employer plan exists
d["public_ly"] = d.LJCW.isin([2, 3, 4]).astype(float)
d["fullyear"] = (d.WKSWORK >= 50).astype(float)
d["parttime"] = ((d.HRSWK > 0) & (d.HRSWK < 35)).astype(float)
d["badhealth"] = d.HEA.isin([4, 5]).astype(float)        # fair or poor
d["disab"] = (d.DIS_HP == 1).astype(float)

# own children in the household via the parent line-number pointers
kids = d[(d.PEPAR1 > 0) | (d.PEPAR2 > 0)][
    ["asec_year", "PH_SEQ", "PEPAR1", "PEPAR2", "A_AGE"]].copy()
k1 = kids.rename(columns={"PEPAR1": "pline"})[
    ["asec_year", "PH_SEQ", "pline", "A_AGE"]]
k2 = kids[kids.PEPAR2 > 0].rename(columns={"PEPAR2": "pline"})[
    ["asec_year", "PH_SEQ", "pline", "A_AGE"]]
kk = pd.concat([k1, k2])
kk = kk[kk.pline > 0]
agg = kk.groupby(["asec_year", "PH_SEQ", "pline"]).A_AGE.agg(
    youngest="min", nkids="size").reset_index()
d = d.merge(agg, left_on=["asec_year", "PH_SEQ", "A_LINENO"],
            right_on=["asec_year", "PH_SEQ", "pline"], how="left")
d["nkids"] = d.nkids.fillna(0)
d["haskid"] = (d.nkids > 0).astype(float)
d["baby"] = (d.youngest < 1).astype(float).fillna(0)
d["kid_u6"] = (d.youngest < 6).astype(float).fillna(0)

# household income quartile within year (total household income)
d["hinc_q"] = d.groupby("asec_year").HTOTVAL.transform(
    lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
d["lowinc"] = (d.hinc_q == 0).astype(float)

T = d[d.teach_ly & d.ba_plus & (d.A_AGE >= 18) & d.MARSUPWT.notna()].copy()
T["W"] = T.MARSUPWT

# ---------- Block 2: unified flow, calendar 2020-2024 ----------
F = T[T.cal_year.between(2020, 2024)]
L = F[F.leaver == 1]
tot = L.W.sum()
def sh(mask):
    return 100 * L.W[mask].sum() / tot
flow = {
    "another_job": sh(L.switch),
    "unemployed": sh(L.unemp),
    "olf_55plus": sh(L.leftlf & (L.A_AGE >= 55)),
    "olf_u55": sh(L.leftlf & (L.A_AGE < 55)),
}
U = L[L.leftlf & (L.A_AGE < 55)]
# demography of the under-55 OLF group, per 100 leavers
flow.update({
    "u55_mother_baby": sh(L.leftlf & (L.A_AGE < 55) & (L.female == 1) & (L.baby == 1)),
    "u55_mother_u6": sh(L.leftlf & (L.A_AGE < 55) & (L.female == 1) & (L.baby == 0) & (L.kid_u6 == 1)),
    "u55_mother_617": sh(L.leftlf & (L.A_AGE < 55) & (L.female == 1) & (L.kid_u6 == 0) & (L.haskid == 1)),
    "u55_woman_nokid": sh(L.leftlf & (L.A_AGE < 55) & (L.female == 1) & (L.haskid == 0)),
    "u55_father": sh(L.leftlf & (L.A_AGE < 55) & (L.female == 0) & (L.haskid == 1)),
    "u55_man_nokid": sh(L.leftlf & (L.A_AGE < 55) & (L.female == 0) & (L.haskid == 0)),
})
# activity of the under-55 OLF group (reason for not working last year)
sch = U[U.PRNLFSCH.isin([1, 2])]
flow["u55_inschool_share"] = 100 * sch.W[sch.PRNLFSCH == 1].sum() / sch.W.sum() \
    if len(sch) else np.nan
flow["u55_inschool_per100"] = flow["olf_u55"] * flow["u55_inschool_share"] / 100
flow["n_leavers"] = int(len(L))
flow["n_teachers"] = int(len(F))
pd.Series(flow).to_csv("outputs/flow_unified.csv")
print(pd.Series(flow).round(1).to_string())

# ---------- Block 3: LPM / logit / probit ----------
R = T[T.cal_year.between(2018, 2024) & (T.A_AGE <= 70)].copy()
R["age"] = R.A_AGE
R["age2"] = R.A_AGE ** 2
XV = ["fullyear", "parttime", "pension", "public_ly",
      "baby", "nkids", "kid_u6", "married", "sepdiv",
      "age", "age2", "female", "black", "ma_plus",
      "badhealth", "disab", "lowinc"]
R = R.dropna(subset=XV + ["leaver", "W"])
Y = R.leaver.astype(float)
W = R.W / R.W.mean()

def fes(col):
    return pd.get_dummies(R[col].astype(int), prefix=col, drop_first=True).astype(float)

def lpm(X):
    X = sm.add_constant(X)
    m = sm.WLS(Y, X, weights=W).fit(cov_type="HC1")
    return m

X_main = pd.concat([R[XV], fes("cal_year")], axis=1)
m_main = lpm(X_main)
m_nofe = lpm(R[XV].copy())
X_st = pd.concat([R[XV], fes("cal_year"), fes("GESTFIPS")], axis=1)
m_st = lpm(X_st)

fit = m_main.fittedvalues
check = {"share_below0": float((fit < 0).mean()),
         "share_above1": float((fit > 1).mean()),
         "min": float(fit.min()), "max": float(fit.max()), "n": int(len(fit))}
pd.Series(check).to_csv("outputs/lpm_fitted_check.csv")
print("LPM fitted check:", {k: round(v, 4) for k, v in check.items()})
np.save("outputs/lpm_fitted_main.npy", fit.values)

# logit / probit AMEs (weighted via GLM var-ish: use frequency-normalized)
import statsmodels.formula.api as smf
Rg = R.copy()
Rg["y"] = Y
form = "y ~ " + " + ".join(XV) + " + C(cal_year)"
logit = smf.glm(form, data=Rg, family=sm.families.Binomial(sm.families.links.Logit()),
                freq_weights=W).fit()
probit = smf.glm(form, data=Rg, family=sm.families.Binomial(sm.families.links.Probit()),
                 freq_weights=W).fit()

def ame(model, data, var, binary):
    if binary:
        d1 = data.copy(); d1[var] = 1
        d0 = data.copy(); d0[var] = 0
        return float(np.average(model.predict(d1) - model.predict(d0), weights=W))
    eps = data[var].std() / 100
    d1 = data.copy(); d1[var] = d1[var] + eps
    return float(np.average((model.predict(d1) - model.predict(data)) / eps, weights=W))

rows = []
BIN = {v: set(R[v].dropna().unique()) <= {0.0, 1.0} for v in XV}
for v in XV:
    if v == "age2":
        continue
    rows.append({
        "var": v,
        "lpm_main": m_main.params[v] * 100, "lpm_main_se": m_main.bse[v] * 100,
        "lpm_nofe": m_nofe.params[v] * 100, "lpm_nofe_se": m_nofe.bse[v] * 100,
        "lpm_statefe": m_st.params[v] * 100, "lpm_statefe_se": m_st.bse[v] * 100,
        "logit_ame": 100 * ame(logit, Rg, v, BIN[v]),
        "probit_ame": 100 * ame(probit, Rg, v, BIN[v]),
    })
res = pd.DataFrame(rows)
res.to_csv("outputs/lpm_results.csv", index=False)
print(res.round(2).to_string(index=False))
print("n =", len(R))
