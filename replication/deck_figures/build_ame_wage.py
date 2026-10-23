"""Coefficient plot of the full specification with pay added:
probit average marginal effects, calendar 2018-2024, college-graduate
teachers aged 18-70. Pay enters as the log of hourly pay (annual wage
and salary over weeks times usual weekly hours, trimmed at the 1st and
99th percentiles within year), since weeks and hours are already in
the model; its effect is shown per 10 percent higher hourly pay
(AME x ln 1.1). Age enters as a quadratic and is not displayed.
Writes outputs/ame_wage.csv and report/figures_deck/ame_wage.{pdf,png}.
Run from the repo root."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

d = pd.read_parquet("data/processed/asec_ext.parquet")
d["cal_year"] = d.asec_year - 1

def tset(ay):
    return {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360})

d["teach_ly"] = False
d["teach_now"] = False
for ay, g in d.groupby("asec_year"):
    s = tset(int(ay))
    d.loc[g.index, "teach_ly"] = g.OCCUP.isin(s)
    d.loc[g.index, "teach_now"] = g.PEIOOCC.isin(s)
d["ba_plus"] = d.A_HGA >= 43
d["ma_plus"] = (d.A_HGA >= 44).astype(float)
emp = d.A_LFSR.isin([1, 2])
d["leaver"] = ((emp & ~d.teach_now) | d.A_LFSR.isin([3, 4, 5, 6, 7])
               ).astype(float)
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
d["age"] = d.A_AGE
d["age2"] = d.A_AGE ** 2


T = d[d.teach_ly & d.ba_plus & (d.A_AGE >= 18) & (d.A_AGE <= 70)
      & d.MARSUPWT.notna() & d.cal_year.between(2018, 2024)].copy()
n_all = len(T)
ok = (T.WSAL_VAL > 0) & (T.WKSWORK > 0) & (T.HRSWK > 0)
T = T[ok].copy()
T["hw"] = T.WSAL_VAL / (T.WKSWORK * T.HRSWK)
lo = T.groupby("cal_year").hw.transform(lambda s: s.quantile(0.01))
hi = T.groupby("cal_year").hw.transform(lambda s: s.quantile(0.99))
T = T[(T.hw >= lo) & (T.hw <= hi)].copy()
T["lnw"] = np.log(T.hw)
print(f"teachers 2018-2024: {n_all:,}; with positive pay, weeks, hours "
      f"and inside the 1-99 percentile band: {len(T):,}")

XV = ["lnw", "fullyear", "parttime", "pension", "public_ly",
      "baby", "nkids", "kid_u6", "married", "sepdiv",
      "age", "age2", "female", "black", "ma_plus",
      "badhealth", "disab", "lowinc"]
R = T.dropna(subset=XV + ["leaver"])
X = pd.concat([R[XV], pd.get_dummies(R.cal_year.astype(int), prefix="y",
               drop_first=True).astype(float)], axis=1)
X = sm.add_constant(X)
m = sm.Probit(R.leaver.astype(float), X).fit(disp=0, maxiter=300)
mg = m.get_margeff(at="overall")
me = pd.Series(mg.margeff, index=X.columns[1:])[XV] * 100
se = pd.Series(mg.margeff_se, index=X.columns[1:])[XV] * 100
pv = pd.Series(mg.pvalues, index=X.columns[1:])[XV]
# pay per 10 percent higher hourly pay: dP/dln(w) x ln(1.1)
K = np.log(1.1)
res = pd.DataFrame({"ame": me, "se": se, "p": pv}).drop(index="age2")
res.loc["lnw10"] = [me["lnw"] * K, se["lnw"] * K, pv["lnw"]]
res["n"] = len(R)
res["base"] = 100 * R.leaver.mean()
res["median_hw"] = R.hw.median()
res.to_csv("outputs/ame_wage.csv")
print(f"N={len(R):,} base={100*R.leaver.mean():.1f}% median hourly pay "
      f"${R.hw.median():.2f}")
print(res[["ame", "se", "p"]].round(3).to_string())

NAVY, INK = "#1F3864", "#1A2430"
BLACK = "#000000"
GROUPS = [
 ("Job attachment", [("fullyear", "Full-year contract"),
                     ("parttime", "Part-time contract")]),
 ("Pay and security", [("lnw10", "Hourly pay, 10 percent higher"),
                       ("pension", "Employer pension plan"),
                       ("public_ly", "Public sector"),
                       ("lowinc", "Bottom-quartile household income")]),
 ("Life events and health", [("baby", "New baby during the year"),
                             ("disab", "With a disability"),
                             ("badhealth", "Fair or poor health")]),
 ("Family", [("kid_u6", "Child under 6"),
             ("nkids", "Number of children"),
             ("married", "Married"),
             ("sepdiv", "Separated or divorced")]),
 ("Demographics", [("female", "Female"),
                   ("black", "Black"),
                   ("ma_plus", "Master's degree or higher")]),
]
fig, ax = plt.subplots(figsize=(11.6, 7.4))
y = 0
yticks, ylabels, heads = [], [], []
for gname, items in GROUPS:
    heads.append((y, gname))
    y -= 1
    for v, lab in items:
        a, s_ = res.loc[v, "ame"], res.loc[v, "se"]
        lo_, hi_ = a - 1.96 * s_, a + 1.96 * s_
        sig = (lo_ > 0) or (hi_ < 0)
        col = NAVY if v == "lnw10" else BLACK
        ax.plot([lo_, hi_], [y, y], color=col, lw=1.0, solid_capstyle="butt")
        ax.plot([lo_, lo_], [y - .10, y + .10], color=col, lw=1.0)
        ax.plot([hi_, hi_], [y - .10, y + .10], color=col, lw=1.0)
        ax.plot(a, y, "o", ms=6.5, mfc=col if sig else "white", mec=col,
                mew=1.1)
        ax.annotate(f"{a:+.1f}", (a, y), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=9.5,
                    color=INK)
        yticks.append(y); ylabels.append(lab)
        y -= 1
    y -= 0.4
ax.axvline(0, color=BLACK, lw=0.8)
for hy, lab in heads:
    ax.text(-14.4, hy, lab, fontsize=12, fontweight="bold", color=INK,
            va="center")
ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=11)
ax.set_xlim(-14.5, 12)
ax.set_ylim(y + 0.2, 1.0)
ax.set_xticks(range(-12, 11, 3))
ax.set_xlabel("average marginal effect on the probability of leaving "
              "(percentage points)", fontsize=11, color=INK)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("report/figures_deck/ame_wage.pdf")
fig.savefig("report/figures_deck/ame_wage.png", dpi=200)
print("saved ame_wage")
