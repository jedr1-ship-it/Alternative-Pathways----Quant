"""Unified flow chart (two bars, same numbers), the probit AME coefficient
plot for the extended specification, and the LPM boundedness check.
Run from the repo root after replication/analyze_ext.py."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["EB Garamond", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})

OUT = "report/figures_deck"
NAVY, BURG, INK, MUT = "#1F3864", "#7B2530", "#23373B", "#6B7480"
PALE, GOLD, GRAY = "#AFC3DC", "#D9A441", "#6B7480"

F = pd.read_csv("outputs/flow_unified.csv", index_col=0).iloc[:, 0]

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.pdf")
    fig.savefig(f"{OUT}/{name}.png", dpi=180)
    plt.close(fig)
    print("saved", name)

# ================= unified two-bar flow =================
fig, ax = plt.subplots(figsize=(12.6, 6.0))
ax.set_xlim(0, 100); ax.set_ylim(0, 10); ax.axis("off")
top = [("Another job", F.another_job, NAVY, "white"),
       ("Out of the labor force, 55+", F.olf_55plus, PALE, INK),
       ("Out of the labor force, under 55", F.olf_u55, GOLD, INK),
       ("Unemployed", F.unemployed, GRAY, "white")]
x = 0
ytop, h = 6.9, 1.7
for lab, v, c, tc in top:
    ax.add_patch(plt.Rectangle((x, ytop), v, h, color=c))
    ax.text(x + v / 2, ytop + h / 2, f"{v:.0f}", ha="center", va="center",
            fontsize=15, fontweight="bold", color=tc)
    ax.text(x + v / 2, ytop + h + 0.35, lab, ha="center", va="bottom",
            fontsize=10.5, color=INK)
    x += v
ax.text(-1.2, ytop + h / 2, "Of every 100\nleavers", ha="right", va="center",
        fontsize=11.5, color=INK)
# bottom bar: the under-55 OLF group, same units (per 100 leavers)
u0 = F.another_job + F.olf_55plus
bot = [("Baby born\nthat year", F.u55_mother_baby, "#B03A2E", "white"),
       ("Mother,\nyoungest under 6", F.u55_mother_u6, "#CD6155", "white"),
       ("Mother,\nyoungest 6–17", F.u55_mother_617, "#E6B0AA", INK),
       ("Women,\nno own child", F.u55_woman_nokid, PALE, INK),
       ("Fathers", F.u55_father, "#7C93B8", "white"),
       ("Men,\nno own child", F.u55_man_nokid, GRAY, "white")]
ybot, hb = 3.0, 1.7
x = u0
lvl = 0
for lab, v, c, tc in bot:
    ax.add_patch(plt.Rectangle((x, ybot), v, hb, color=c))
    ax.text(x + v / 2, ybot + hb / 2, f"{v:.0f}" if v >= 1.5 else "",
            ha="center", va="center", fontsize=13, fontweight="bold", color=tc)
    yl = ybot - 0.35 - (0 if lvl % 2 == 0 else 1.05)
    ax.plot([x + v / 2, x + v / 2], [ybot - 0.12, yl + 0.18],
            color=MUT, lw=0.6)
    ax.text(x + v / 2, yl, lab, ha="center", va="top",
            fontsize=9.0, color=INK)
    lvl += 1
    x += v
for xx in (u0, u0 + F.olf_u55):
    ax.plot([xx, xx], [ybot + hb, ytop],
            color=MUT, lw=0.8, ls=(0, (3, 3)))
ax.text(u0 + F.olf_u55 / 2, ybot + hb + 0.55,
        f"about {F.u55_inschool_share:.0f} percent of this group is enrolled in school",
        ha="center", va="bottom", fontsize=10, color=INK, style="italic")
fig.tight_layout()
save(fig, "flow_unified")

# ================= probit AME coefplot (extended spec) =================
import statsmodels.api as sm
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
emp = d.A_LFSR.isin([1, 2])
d["leaver"] = ((emp & ~d.teach_now) | ~emp).astype(float)
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
d["ma_plus"] = d.A_HGA >= 44
kids = d[(d.PEPAR1 > 0) | (d.PEPAR2 > 0)][
    ["asec_year", "PH_SEQ", "PEPAR1", "PEPAR2", "A_AGE"]].copy()
k1 = kids.rename(columns={"PEPAR1": "pline"})[["asec_year", "PH_SEQ", "pline", "A_AGE"]]
k2 = kids[kids.PEPAR2 > 0].rename(columns={"PEPAR2": "pline"})[["asec_year", "PH_SEQ", "pline", "A_AGE"]]
kk = pd.concat([k1, k2]); kk = kk[kk.pline > 0]
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
R = d[d.teach_ly & d.ba_plus & d.A_AGE.between(18, 70)
      & d.cal_year.between(2018, 2024)].copy()
R["age"] = R.A_AGE
R["age2"] = R.A_AGE ** 2
XV = ["fullyear", "parttime", "pension", "public_ly",
      "baby", "nkids", "kid_u6", "married", "sepdiv",
      "age", "age2", "female", "black", "ma_plus",
      "badhealth", "disab", "lowinc"]
R = R.dropna(subset=XV + ["leaver"])
X = pd.concat([R[XV], pd.get_dummies(R.cal_year.astype(int), prefix="y",
                                     drop_first=True).astype(float)], axis=1)
X = sm.add_constant(X)
m = sm.Probit(R.leaver, X).fit(disp=0)
mg = m.get_margeff(at="overall")
me = pd.Series(mg.margeff, index=X.columns[1:])
se = pd.Series(mg.margeff_se, index=X.columns[1:])
res = pd.DataFrame({"ame": me[XV] * 100, "se": se[XV] * 100}).drop(index="age2")
res.to_csv("outputs/ame_ext_probit.csv")
print(res.round(2).to_string())

GROUPS = [
 ("Job attachment", [("fullyear", "Full-year contract"),
                     ("parttime", "Part-time contract")]),
 ("Compensation", [("pension", "Employer pension plan"),
                   ("public_ly", "Public sector"),
                   ("lowinc", "Bottom-quartile household income")]),
 ("Family", [("baby", "New baby during the year"),
             ("kid_u6", "Child under 6"),
             ("nkids", "Number of children"),
             ("married", "Married"),
             ("sepdiv", "Separated or divorced")]),
 ("Health", [("badhealth", "Fair or poor health"),
             ("disab", "With a disability")]),
 ("Demographics", [("age", "Age (per year)"),
                   ("female", "Female"),
                   ("black", "Black"),
                   ("ma_plus", "Master's degree or higher")]),
]
BLACK = "#000000"
fig, ax = plt.subplots(figsize=(11.6, 7.2))
y = 0
yticks, ylabels, heads = [], [], []
for gname, items in GROUPS:
    heads.append((y, gname))
    y -= 1
    for v, lab in items:
        a, s = res.loc[v, "ame"], res.loc[v, "se"]
        lo, hi = a - 1.96 * s, a + 1.96 * s
        sig = (lo > 0) or (hi < 0)
        ax.plot([lo, hi], [y, y], color=BLACK, lw=1.0,
                solid_capstyle="butt")
        ax.plot([lo, lo], [y - .10, y + .10], color=BLACK, lw=1.0)
        ax.plot([hi, hi], [y - .10, y + .10], color=BLACK, lw=1.0)
        ax.plot(a, y, "o", ms=6.5, mfc=BLACK if sig else "white",
                mec=BLACK, mew=1.1)
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
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "ame_ext")

# ================= LPM boundedness check =================
fit = np.load("outputs/lpm_fitted_main.npy")
below = 100 * (fit < 0).mean()
fig, ax = plt.subplots(figsize=(10.5, 5.2))
ax.hist(fit, bins=80, color=NAVY, alpha=0.85)
ax.axvline(0, color=BURG, lw=2)
ax.axvline(1, color=BURG, lw=2)
ax.annotate(f"{below:.0f}% of fitted values\nbelow zero", (0.015, 0.84),
            xycoords="axes fraction", fontsize=12.5, color=BURG)
ax.set_xlabel("fitted probability, linear probability model", fontsize=11.5,
              color=INK)
ax.set_ylabel("teachers", fontsize=11.5, color=INK)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1); ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "lpm_check")
print("done")
