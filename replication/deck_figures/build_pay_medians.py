"""Real median earnings by profession, calendar 1997-2024, for the
relative-pay figure. College graduates aged 25-64 whose longest job
last year was in the profession, working 50+ weeks and 35+ hours;
weighted median of annual wage and salary income, deflated to 2024
dollars with the CPI series in outputs/n_cpi.csv.
Writes outputs/pay_prof_medians.csv. Run from the repo root."""
import numpy as np
import pandas as pd

def codes(ay):
    if ay <= 2002:
        return {"Teachers": {155, 156, 157, 158, 159},
                "Registered nurses": {95}, "Social workers": {174},
                "Accountants": {23}, "Lawyers": {178},
                "Counselors": {163}}
    rn = {3130} if ay <= 2010 else {3255, 3256, 3257, 3258}
    sw = {2010} if ay <= 2019 else {2011, 2012, 2013, 2014}
    co = {2000} if ay <= 2019 else {2001, 2002, 2003, 2004, 2005, 2006}
    t = {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360})
    return {"Teachers": t, "Registered nurses": rn, "Social workers": sw,
            "Accountants": {800}, "Lawyers": {2100}, "Counselors": co}

M = pd.read_parquet("data/processed/asec_master.parquet",
    columns=["asec_year", "cal_year", "OCCUP", "WGT", "ba_plus",
             "A_AGE", "WSAL_VAL", "WKSWORK", "HRSWK"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
M = M[(M.ba_plus == 1) & M.A_AGE.between(25, 64) & (M.WKSWORK >= 50)
      & (M.HRSWK >= 35) & (M.WSAL_VAL > 0) & M.WGT.notna()]

cpi = pd.read_csv("outputs/n_cpi.csv").set_index("year")["CPIAUCSL"]
defl = cpi.loc[2024] / cpi

def wmed(g):
    g = g.sort_values("WSAL_VAL")
    cw = g.WGT.cumsum() / g.WGT.sum()
    return g.loc[cw >= 0.5, "WSAL_VAL"].iloc[0]

rows = []
for ay, g in M.groupby("asec_year"):
    cy = int(ay) - 1
    if cy < 1997 or cy > 2024:
        continue
    cs = codes(int(ay))
    allprof = set().union(*cs.values())
    r = {"cal_year": cy}
    for name, cc in cs.items():
        b = g[g.OCCUP.isin(cc)]
        r[name] = wmed(b) * defl.loc[cy] if len(b) >= 50 else np.nan
    oth = g[~g.OCCUP.isin(allprof)]
    r["All other graduates"] = wmed(oth) * defl.loc[cy]
    rows.append(r)
P = pd.DataFrame(rows).sort_values("cal_year")
P = P[["cal_year", "Teachers", "Registered nurses", "Social workers",
       "Accountants", "Lawyers", "Counselors", "All other graduates"]]
P.to_csv("outputs/pay_prof_medians.csv", index=False)
print(P.round(0).to_string(index=False))
print("missing cells:", int(P.isna().sum().sum()))
