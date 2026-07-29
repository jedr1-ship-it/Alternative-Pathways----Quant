import sys
sys.path.insert(0, "replication")
import glob
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401  (applies the paper's rcParams)
from scipy.stats import norm

RAW = "data/raw/asec"
W = "MARSUPWT"
CORE = {2300, 2310, 2320, 2330}
BLUE, CORAL, DARK = "#2A5DB0", "#C4534B", "#3B4046"
OUT = "report/figures_deck"

def tset(ay):
    return CORE | ({2340} if ay <= 2019 else {2360})

rich = [pd.read_parquet(f) for f in sorted(glob.glob(f"{RAW}/asec_rich_*.parquet"))]
R = pd.concat(rich, ignore_index=True)
for c in R.columns:
    if c != "PERIDNUM":
        R[c] = pd.to_numeric(R[c], errors="coerce")
R["cal_year"] = R["asec_year"] - 1

ptr = []
for c in ["A_PARENT", "PEPAR1", "PEPAR2"]:
    if c in R.columns:
        k = R[(pd.to_numeric(R[c], errors="coerce") > 0)
              & (R["A_AGE"] < 18)][["asec_year", "PH_SEQ", c, "A_AGE",
                                    "A_LINENO"]].rename(
            columns={c: "parent_line", "A_LINENO": "kid_line"})
        ptr.append(k)
kids = pd.concat(ptr, ignore_index=True).drop_duplicates(
    ["asec_year", "PH_SEQ", "parent_line", "kid_line"])
agg = kids.groupby(["asec_year", "PH_SEQ", "parent_line"])["A_AGE"].agg(
    n_children="size", child_u6=lambda s: int((s < 6).any()),
    new_baby=lambda s: int((s < 1).any())).reset_index().rename(
    columns={"parent_line": "A_LINENO"})
R = R.merge(agg, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
sp = R[R["A_SPOUSE"] > 0][["asec_year", "PH_SEQ", "A_SPOUSE",
                           "n_children", "child_u6", "new_baby"]].rename(
    columns={"A_SPOUSE": "A_LINENO", "n_children": "n2", "child_u6": "c2",
             "new_baby": "b2"})
sp = sp.groupby(["asec_year", "PH_SEQ", "A_LINENO"]).max().reset_index()
R = R.merge(sp, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
for a, b in [("n_children", "n2"), ("child_u6", "c2"), ("new_baby", "b2")]:
    R[a] = R[[a, b]].max(axis=1).fillna(0)
R = R.drop(columns=["n2", "c2", "b2"])

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

def outcomes(b, cset):
    emp = b["A_LFSR"].isin([1, 2])
    b["switch"] = (emp & ~b["PEIOOCC"].isin(cset)).astype(int)
    b["unemp"] = b["A_LFSR"].isin([3, 4]).astype(int)
    b["leftlf"] = (~b["A_LFSR"].isin([1, 2, 3, 4])).astype(int)
    b["leaver"] = (b["switch"] | b["unemp"] | b["leftlf"]).astype(int)
    return b

teach = []
for ay, g in R.groupby("asec_year"):
    cs = tset(int(ay))
    teach.append(outcomes(g[g["OCCUP"].isin(cs)].copy(), cs))
T = pd.concat(teach, ignore_index=True)
TB = T[(T["ba_plus"] == 1) & (T["A_AGE"] >= 18)]
win = TB[TB["cal_year"].between(2015, 2024)]

XV = ["A_AGE", "age2", "female", "black", "married", "sepdiv", "ma_plus",
      "public", "pension", "parttime", "fullyear", "n_children", "child_u6",
      "new_baby"]

def profile(dep):
    sub = win.dropna(subset=XV + [dep, W]).copy()
    yd = pd.get_dummies(sub["asec_year"], prefix="y", drop_first=True, dtype=float)
    X = sm.add_constant(pd.concat([sub[XV].astype(float), yd], axis=1))
    pm = sm.Probit(sub[dep].astype(float), X).fit(disp=0)
    beta, V = pm.params, pm.cov_params()
    cols = list(X.columns)
    xbar = X.mean(axis=0).values.copy()
    i_age, i_age2 = cols.index("A_AGE"), cols.index("age2")
    ages = np.arange(23, 67)
    P, Plo, Phi = [], [], []
    for a in ages:
        xx = xbar.copy()
        xx[i_age], xx[i_age2] = a, a * a
        z = xx @ beta.values
        se_z = np.sqrt(xx @ V.values @ xx)
        P.append(norm.cdf(z) * 100)
        Plo.append(norm.cdf(z - 1.96 * se_z) * 100)
        Phi.append(norm.cdf(z + 1.96 * se_z) * 100)
    return ages, np.array(P), np.array(Plo), np.array(Phi)

GREEN = "#3E7C59"
panels = [("leaver", "Leaving at all", BLUE),
          ("switch", "Switching to another job", GREEN),
          ("leftlf", "Leaving the labor force", CORAL)]
fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.2))
for ax, (dep, title, col) in zip(axes, panels):
    ages, P, Plo, Phi = profile(dep)
    ax.fill_between(ages, Plo, Phi, color=col, alpha=0.14, lw=0)
    ax.plot(ages, P, color=col, lw=2.2)
    for a0, dx, ha in [(25, 10, "left"), (60, -10, "right")]:
        p0 = P[list(ages).index(a0)]
        ax.annotate(f"{p0:.1f}%", (a0, p0), xytext=(dx, 5),
                    textcoords="offset points", ha=ha, fontsize=9,
                    color=DARK)
    ax.set_title(title, fontsize=11, color=DARK, pad=10)
    ax.set_xlabel("Age", fontsize=9.5)
    ax.set_ylim(0, None)
axes[0].set_ylabel("Predicted probability, %", fontsize=9.5)
fig.tight_layout()
fig.savefig(f"{OUT}/u_routes_deck.pdf")
fig.savefig(f"{OUT}/u_routes_deck.png", dpi=200)
print("saved")
