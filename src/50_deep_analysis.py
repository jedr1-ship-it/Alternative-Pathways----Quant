"""
Deep analysis layer for the paper: (i) detailed destination groups for the
leavers who hold another job, (ii) a robustness battery for the attrition
probit, (iii) route-specific models (which characteristics push toward
each exit route), (iv) the decades comparison table. Consumes the rich
files via the same construction as 47; writes outputs/q_*.csv.
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.api as sm

RAW = "data/raw/asec"
W = "MARSUPWT"
CORE = {2300, 2310, 2320, 2330}


def tset(ay):
    return CORE | ({2340} if ay <= 2019 else {2360})


def wavg(d, col, w=W):
    v = d[col].astype(float)
    ok = v.notna() & d[w].notna()
    return np.average(v[ok], weights=d.loc[ok, w]) if ok.any() else np.nan


R = pd.concat([pd.read_parquet(f) for f in
               sorted(glob.glob(f"{RAW}/asec_rich_*.parquet"))],
              ignore_index=True)
for c in R.columns:
    if c != "PERIDNUM":
        R[c] = pd.to_numeric(R[c], errors="coerce")
R["cal_year"] = R["asec_year"] - 1

ptr = []
for c in ["A_PARENT", "PEPAR1", "PEPAR2"]:
    k = R[(pd.to_numeric(R[c], errors="coerce") > 0) & (R["A_AGE"] < 18)][
        ["asec_year", "PH_SEQ", c, "A_AGE", "A_LINENO"]].rename(
        columns={c: "parent_line", "A_LINENO": "kid_line"})
    ptr.append(k)
kids = pd.concat(ptr, ignore_index=True).drop_duplicates(
    ["asec_year", "PH_SEQ", "parent_line", "kid_line"])
agg = kids.groupby(["asec_year", "PH_SEQ", "parent_line"])["A_AGE"].agg(
    n_children="size", child_u6=lambda s: int((s < 6).any()),
    new_baby=lambda s: int((s < 1).any())).reset_index().rename(
    columns={"parent_line": "A_LINENO"})
R = R.merge(agg, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
sp = R[R["A_SPOUSE"] > 0][["asec_year", "PH_SEQ", "A_SPOUSE", "n_children",
                           "child_u6", "new_baby"]].rename(
    columns={"A_SPOUSE": "A_LINENO", "n_children": "n2", "child_u6": "c2",
             "new_baby": "b2"})
sp = sp.groupby(["asec_year", "PH_SEQ", "A_LINENO"]).max().reset_index()
R = R.merge(sp, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
for a, b in [("n_children", "n2"), ("child_u6", "c2"), ("new_baby", "b2")]:
    R[a] = R[[a, b]].max(axis=1).fillna(0)

R["female"] = (R["A_SEX"] == 2).astype(int)
R["black"] = (R["PRDTRACE"] == 2).astype(int)
R["married"] = R["A_MARITL"].isin([1, 2, 3]).astype(int)
R["sepdiv"] = R["A_MARITL"].isin([5, 6]).astype(int)
R["ba_plus"] = (R["A_HGA"] >= 43).astype(int)
R["ma_plus"] = (R["A_HGA"] >= 44).astype(int)
R["public"] = R["LJCW"].isin([2, 3, 4]).astype(int)
R["pension"] = (R["PENPLAN"] == 1).astype(int)
R["parttime"] = R["HRSWK"].between(1, 34).astype(int)
R["fullyear"] = (R["WKSWORK"] >= 50).astype(int)
R["age2"] = R["A_AGE"] ** 2

teach = []
for ay, g in R.groupby("asec_year"):
    cs = tset(int(ay))
    b = g[g["OCCUP"].isin(cs)].copy()
    emp = b["A_LFSR"].isin([1, 2])
    b["switch"] = (emp & ~b["PEIOOCC"].isin(cs)).astype(int)
    b["unemp"] = b["A_LFSR"].isin([3, 4]).astype(int)
    b["leftlf"] = (~b["A_LFSR"].isin([1, 2, 3, 4])).astype(int)
    b["leaver"] = (b["switch"] | b["unemp"] | b["leftlf"]).astype(int)
    teach.append(b)
T = pd.concat(teach, ignore_index=True)
TB = T[(T["ba_plus"] == 1) & (T["A_AGE"] >= 18)]
win = TB[TB["cal_year"].between(2015, 2024)].copy()

# ------- (i) destination groups of switchers, share of 100 LEAVERS -------
GRP = [
    ("Postsecondary teaching", lambda o: o.isin({2200, 2205})),
    ("School support (tutor, assistant, library)",
     lambda o: o.isin({2340, 2350, 2360, 2540, 2545, 2430, 2435, 2440,
                       2550, 2555})),
    ("Education administration", lambda o: o.isin({230})),
    ("Counseling, social work, childcare",
     lambda o: o.isin({2001, 2002, 2010, 2011, 2012, 2013, 2014, 2015,
                       2016, 2025, 4600})),
    ("Management and business", lambda o: (o >= 10) & (o <= 960)
     & ~o.isin({230})),
    ("Other professional", lambda o: (o >= 1000) & (o <= 3550)
     & ~o.between(2000, 2555)),
    ("Office and administrative support", lambda o: (o >= 5000)
     & (o <= 5940)),
    ("Sales and personal service", lambda o: ((o >= 4000) & (o <= 4965)
                                              & (o != 4600))
     | ((o >= 3600) & (o <= 3955))),
    ("Production, transport, other", lambda o: o >= 6000),
]
L = win[win["leaver"] == 1]
sw = L[L["switch"] == 1].copy()
wl = L[W].sum()
rows = []
for name, fn in GRP:
    m = fn(sw["PEIOOCC"])
    rows.append({"group": name,
                 "per100_leavers": round(sw.loc[m, W].sum() / wl * 100, 1),
                 "per100_switchers": round(sw.loc[m, W].sum()
                                           / sw[W].sum() * 100, 1)})
D = pd.DataFrame(rows)
D.to_csv("outputs/q_dest_groups.csv", index=False)
print("=== destination groups (per 100 leavers | per 100 switchers) ===")
print(D.to_string(index=False))

# ------- (ii) robustness battery -------
XV = ["A_AGE", "age2", "female", "black", "married", "sepdiv", "ma_plus",
      "public", "pension", "parttime", "fullyear", "n_children",
      "child_u6", "new_baby"]
KEY = ["fullyear", "parttime", "pension", "new_baby", "public"]


def fit(d, label, kind="probit"):
    d = d.dropna(subset=XV + ["leaver", W])
    yd = pd.get_dummies(d["asec_year"], prefix="y", drop_first=True,
                        dtype=float)
    X = sm.add_constant(pd.concat([d[XV].astype(float), yd], axis=1))
    if kind == "probit":
        m = sm.Probit(d["leaver"].astype(float), X).fit(disp=0)
        eff = m.get_margeff(at="overall")
        coefs = dict(zip(XV, eff.margeff[:len(XV)] * 100))
        ses = dict(zip(XV, eff.margeff_se[:len(XV)] * 100))
    else:
        m = sm.WLS(d["leaver"].astype(float), X, weights=d[W]).fit(
            cov_type="HC1")
        coefs = {v: m.params[v] * 100 for v in XV}
        ses = {v: m.bse[v] * 100 for v in XV}
    row = {"specification": label, "n": int(m.nobs)}
    for v in KEY:
        row[v] = round(coefs[v], 2)
        row[v + "_se"] = round(ses[v], 2)
    return row


rob = [fit(win, "Baseline probit"),
       fit(win, "Weighted LPM", kind="lpm"),
       fit(win[win["A_AGE"] < 55], "Age under 55", kind="lpm"),
       fit(win[win["public"] == 1], "Public school only", kind="lpm"),
       fit(win[win["female"] == 1], "Women only", kind="lpm"),
       fit(win[~win["asec_year"].isin([2020, 2021])], "Excluding Covid surveys"),
       fit(TB[TB["cal_year"].between(2010, 2014)], "2010-2014 window")]
# strict K-12 core codes (drop n.e.c.)
strict = []
for ay, g in R.groupby("asec_year"):
    b = g[g["OCCUP"].isin(CORE)].copy()
    emp = b["A_LFSR"].isin([1, 2])
    b["leaver"] = (~(emp & b["PEIOOCC"].isin(CORE))).astype(int)
    strict.append(b)
ST = pd.concat(strict, ignore_index=True)
ST = ST[(ST["ba_plus"] == 1) & (ST["A_AGE"] >= 18)
        & ST["cal_year"].between(2015, 2024)]
rob.append(fit(ST, "Core codes only (2300-2330)"))
ROB = pd.DataFrame(rob)
ROB.to_csv("outputs/q_robustness.csv", index=False)
print("\n=== robustness battery (key AMEs, pp) ===")
print(ROB[["specification", "n"] + KEY].to_string(index=False))

# ------- (iii) route-specific models -------
routes = []
for dep in ["switch", "unemp", "leftlf"]:
    d = win.dropna(subset=XV + [dep, W])
    yd = pd.get_dummies(d["asec_year"], prefix="y", drop_first=True,
                        dtype=float)
    X = sm.add_constant(pd.concat([d[XV].astype(float), yd], axis=1))
    m = sm.Probit(d[dep].astype(float), X).fit(disp=0, maxiter=200)
    eff = m.get_margeff(at="overall")
    for v, c, s in zip(XV, eff.margeff[:len(XV)] * 100,
                       eff.margeff_se[:len(XV)] * 100):
        routes.append({"route": dep, "var": v, "AME_pp": round(c, 2),
                       "se_pp": round(s, 2)})
RT = pd.DataFrame(routes)
RT.to_csv("outputs/q_routes_model.csv", index=False)
print("\n=== route-specific AMEs (selected) ===")
sel = RT[RT["var"].isin(["fullyear", "parttime", "pension", "new_baby",
                         "A_AGE", "female"])]
print(sel.pivot(index="var", columns="route", values="AME_pp").to_string())

# ------- (iv) decades table -------
dec = []
for per, m in [("2010-2014", TB["cal_year"].between(2010, 2014)),
               ("2015-2019", TB["cal_year"].between(2015, 2019)),
               ("2020-2024", TB["cal_year"].between(2020, 2024))]:
    d = TB[m]
    lv = d[d["leaver"] == 1]
    dec.append({
        "period": per,
        "leaver_%": round(wavg(d, "leaver") * 100, 2),
        "switch_pp": round(wavg(d, "switch") * 100, 2),
        "unemp_pp": round(wavg(d, "unemp") * 100, 2),
        "leftlf_pp": round(wavg(d, "leftlf") * 100, 2),
        "public_%": round(wavg(d[d['public'] == 1], "leaver") * 100, 2),
        "private_%": round(wavg(d[d['public'] == 0], "leaver") * 100, 2),
        "n": len(d)})
DEC = pd.DataFrame(dec)
DEC.to_csv("outputs/q_decades.csv", index=False)
print("\n=== periods ===")
print(DEC.to_string(index=False))
print("\nwrote outputs/q_*.csv")
