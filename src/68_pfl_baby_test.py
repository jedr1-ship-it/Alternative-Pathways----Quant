"""
Does the new-baby exit effect vary with state maternity policy?
Weighted LPM of leaving on new_baby interacted with an indicator for
the state having an active paid-family-leave program (first full
calendar year benefits were payable: CA 2005, NJ 2010, RI 2014,
NY 2018, WA 2020, DC/MA 2021, CT 2022, OR 2024), with state and year
fixed effects, SEs clustered by state. Run from repo root.
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

M = pd.read_parquet("data/processed/asec_master.parquet")
T = M[(M["teacher"] == 1) & (M["ba_plus"] == 1)
      & M["A_AGE"].between(21, 60) & M["WGT"].notna()
      & M["leaver"].notna()].copy()
S = pd.concat([pd.read_parquet(f) for f in
               sorted(glob.glob("data/raw/asec/asec_state_*.parquet"))],
              ignore_index=True)
T = T.merge(S, on=["asec_year", "PH_SEQ"], how="inner")
PFL = {6: 2005, 34: 2010, 44: 2014, 36: 2018, 53: 2020, 11: 2021,
       25: 2021, 9: 2022, 41: 2024}
T["pfl"] = 0
for st, y0 in PFL.items():
    T.loc[(T["GESTFIPS"] == st) & (T["cal_year"] >= y0), "pfl"] = 1
T["baby"] = T["new_baby"].fillna(0)
T["age2"] = T["A_AGE"] ** 2
print(f"n={len(T)}  babies={int(T['baby'].sum())}  "
      f"babies under PFL={int(T.loc[T['pfl'] == 1, 'baby'].sum())}")
m = smf.wls("leaver ~ baby*pfl + A_AGE + age2 + female + married"
            " + C(GESTFIPS) + C(cal_year)", data=T,
            weights=T["WGT"]).fit(cov_type="cluster",
                                  cov_kwds={"groups": T["GESTFIPS"]})
rows = []
for k in ["baby", "pfl", "baby:pfl"]:
    rows.append({"term": k, "b_pp": round(m.params[k] * 100, 2),
                 "se_pp": round(m.bse[k] * 100, 2),
                 "p": round(m.pvalues[k], 3)})
R = pd.DataFrame(rows)
R.to_csv("outputs/p_pfl_baby.csv", index=False)
print(R.to_string(index=False))
