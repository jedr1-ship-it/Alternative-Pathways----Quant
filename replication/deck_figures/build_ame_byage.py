"""Do the drivers differ for early-career teachers? The full
specification (analyze_ext.py Block 3, calendar 2018-2024), estimated
separately for teachers under 35 and 35-70, as probit average marginal
effects. Age enters each model as a quadratic and is not displayed.
Writes outputs/ame_byage.csv and report/figures_deck/ame_byage.{pdf,png}.
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

XV = ["fullyear", "parttime", "pension", "public_ly",
      "baby", "nkids", "kid_u6", "married", "sepdiv",
      "age", "age2", "female", "black", "ma_plus",
      "badhealth", "disab", "lowinc"]

def fit(mask):
    R = T[mask].dropna(subset=XV + ["leaver"])
    X = pd.concat([R[XV], pd.get_dummies(R.cal_year.astype(int), prefix="y",
                   drop_first=True).astype(float)], axis=1)
    X = sm.add_constant(X)
    m = sm.Probit(R.leaver.astype(float), X).fit(disp=0, maxiter=300)
    mg = m.get_margeff(at="overall")
    me = pd.Series(mg.margeff, index=X.columns[1:])[XV] * 100
    se = pd.Series(mg.margeff_se, index=X.columns[1:])[XV] * 100
    return me, se, len(R), 100 * R.leaver.mean()

me_y, se_y, n_y, base_y = fit(T.A_AGE < 35)
me_o, se_o, n_o, base_o = fit(T.A_AGE >= 35)
print(f"under 35: N={n_y:,} base={base_y:.1f} | 35-70: N={n_o:,} "
      f"base={base_o:.1f}")
pd.DataFrame({"ame_u35": me_y, "se_u35": se_y,
              "ame_35p": me_o, "se_35p": se_o}).to_csv(
    "outputs/ame_byage.csv")

NAVY, GRAY, INK = "#1F3864", "#8A9096", "#1A2430"
GROUPS = [
 ("Job attachment", [("fullyear", "Full-year contract"),
                     ("parttime", "Part-time contract")]),
 ("Compensation", [("pension", "Employer pension plan"),
                   ("public_ly", "Public sector")]),
 ("Family", [("baby", "New baby during the year"),
             ("kid_u6", "Child under 6"),
             ("nkids", "Number of children"),
             ("married", "Married")]),
 ("Health and income", [("badhealth", "Fair or poor health"),
                        ("disab", "With a disability"),
                        ("lowinc", "Bottom-quartile household income")]),
 ("Demographics", [("female", "Female"),
                   ("black", "Black"),
                   ("ma_plus", "Master's degree or higher")]),
]
fig, ax = plt.subplots(figsize=(11.6, 7.0))
yy = 0
yticks, ylabels, heads = [], [], []
for gname, items in GROUPS:
    heads.append((yy, gname))
    yy -= 1
    for v, lab in items:
        for me, se_, dy, col, filled in [(me_o, se_o, -0.20, GRAY, False),
                                         (me_y, se_y, 0.20, NAVY, True)]:
            a, s = me[v], se_[v]
            ax.plot([a - 1.96 * s, a + 1.96 * s], [yy + dy, yy + dy],
                    color=col, lw=1.1, solid_capstyle="butt")
            ax.plot(a, yy + dy, "o", ms=6,
                    mfc=col if filled else "white", mec=col, mew=1.2)
        yticks.append(yy); ylabels.append(lab)
        yy -= 1
    yy -= 0.4
ax.axvline(0, color="#000000", lw=0.8)
for hy, lab in heads:
    ax.text(-13.4, hy, lab, fontsize=12, fontweight="bold", color=INK,
            va="center")
ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=11)
ax.set_xlim(-13.5, 10)
ax.set_ylim(yy + 0.2, 1.2)
ax.set_xticks(range(-12, 10, 3))
ax.set_xlabel("average marginal effect on the probability of leaving "
              "(percentage points)", fontsize=11, color=INK)
from matplotlib.lines import Line2D
ax.legend(handles=[
    Line2D([], [], marker="o", color=NAVY, mfc=NAVY, lw=1.1,
           label=f"Under 35 (N = {n_y:,}, {base_y:.0f}% leave per year)"),
    Line2D([], [], marker="o", color=GRAY, mfc="white", lw=1.1,
           label=f"35–70 (N = {n_o:,}, {base_o:.0f}% leave per year)")],
    frameon=False, fontsize=10.5, loc="lower right")
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("report/figures_deck/ame_byage.pdf")
fig.savefig("report/figures_deck/ame_byage.png", dpi=200)
print("saved ame_byage")
