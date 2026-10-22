"""Does the panel's linkage loss introduce selection? For every BA+
teacher observed in ASEC surveys 2019-2024, the outcome is NOT being
found in the next year's ASEC (PERIDNUM match validated by sex, race,
and an age advancing at most two years). That outcome is regressed on
the covariates of the main leaving regression (analyze_ext.py Block 3).
About half of the non-observations are mechanical: the 4-8-4 rotation
retires half of each March sample before the next March, independently
of characteristics. The regression therefore tests whether the
remaining loss is correlated with observables.
Writes outputs/attrition_selection.csv and prints the table rows.
Run from the repo root."""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

d = pd.read_parquet("data/processed/asec_ext.parquet")
d["cal_year"] = d.asec_year - 1

def tset(ay):
    return {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360})

d["teach_ly"] = False
for ay, g in d.groupby("asec_year"):
    d.loc[g.index, "teach_ly"] = g.OCCUP.isin(tset(int(ay)))
d["ba_plus"] = d.A_HGA >= 43
d["ma_plus"] = (d.A_HGA >= 44).astype(float)
d["female"] = (d.A_SEX == 2).astype(float)
d["black"] = (d.PRDTRACE == 2).astype(float)
d["married"] = d.A_MARITL.isin([1, 2, 3]).astype(float)
d["sepdiv"] = d.A_MARITL.isin([4, 5]).astype(float)
d["pension"] = (d.PENPLAN == 1).astype(float)
d["public_ly"] = d.LJCW.isin([2, 3, 4]).astype(float)
d["fullyear"] = (d.WKSWORK >= 50).astype(float)
d["parttime"] = ((d.HRSWK > 0) & (d.HRSWK < 35)).astype(float)
d["badhealth"] = d.HEA.isin([4, 5]).astype(float)
d["disab"] = (d.DIS_HP == 1).astype(float)

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
d["baby"] = (d.youngest < 1).astype(float).fillna(0)
d["kid_u6"] = (d.youngest < 6).astype(float).fillna(0)
d["hinc_q"] = d.groupby("asec_year").HTOTVAL.transform(
    lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
d["lowinc"] = (d.hinc_q == 0).astype(float)

# ---- link each teacher to the next survey year's file ----
d["pid"] = d.PERIDNUM.astype(str).str.strip()
nxt = {ay: g.set_index("pid")[["A_SEX", "PRDTRACE", "A_AGE"]]
       for ay, g in d[d.pid != ""].groupby("asec_year")}

T = d[d.teach_ly & d.ba_plus & (d.A_AGE >= 18) & (d.A_AGE <= 70)
      & d.MARSUPWT.notna() & d.asec_year.between(2019, 2024)].copy()

def linked(row):
    N = nxt.get(row.asec_year + 1)
    if N is None or row.pid not in N.index:
        return 0.0
    cand = N.loc[[row.pid]]
    ok = ((cand.A_SEX == row.A_SEX) & (cand.PRDTRACE == row.PRDTRACE)
          & (cand.A_AGE - row.A_AGE).between(0, 2))
    return float(ok.any())

T["obs_next"] = T.apply(linked, axis=1)
T["notobs"] = 1.0 - T.obs_next
T["age"] = T.A_AGE
T["age2"] = T.A_AGE ** 2
T["W"] = T.MARSUPWT

XV = ["fullyear", "parttime", "pension", "public_ly",
      "baby", "nkids", "kid_u6", "married", "sepdiv",
      "age", "age2", "female", "black", "ma_plus",
      "badhealth", "disab", "lowinc"]
R = T.dropna(subset=XV + ["notobs", "W"]).copy()
W = R.W / R.W.mean()
Y = R.notobs
base = np.average(Y, weights=R.W) * 100
print(f"n={len(R)}  weighted share not observed next March: {base:.1f}%")

X = pd.concat([R[XV], pd.get_dummies(R.cal_year.astype(int), prefix="cal_year",
                                     drop_first=True).astype(float)], axis=1)
X = sm.add_constant(X)
lpm = sm.WLS(Y, X, weights=W).fit(cov_type="HC1")

Rg = R.copy()
Rg["y"] = Y
form = "y ~ " + " + ".join(XV) + " + C(cal_year)"
probit = smf.glm(form, data=Rg,
                 family=sm.families.Binomial(sm.families.links.Probit()),
                 freq_weights=W).fit()

BIN = {v: set(R[v].dropna().unique()) <= {0.0, 1.0} for v in XV}

def ame(model, data, var):
    if BIN[var]:
        d1 = data.copy(); d1[var] = 1.0
        d0 = data.copy(); d0[var] = 0.0
        return float(np.average(model.predict(d1) - model.predict(d0),
                                weights=W))
    eps = data[var].std() / 100
    d1 = data.copy(); d1[var] = d1[var] + eps
    return float(np.average((model.predict(d1) - model.predict(data)) / eps,
                            weights=W))

rows = []
for v in XV:
    rows.append({"var": v, "lpm": lpm.params[v] * 100,
                 "lpm_se": lpm.bse[v] * 100, "lpm_p": lpm.pvalues[v],
                 "probit_ame": ame(probit, Rg, v) * 100})
out = pd.DataFrame(rows)
out["n"] = len(R)
out["base"] = base
out.to_csv("outputs/attrition_selection.csv", index=False)
print(out.round(2).to_string(index=False))
