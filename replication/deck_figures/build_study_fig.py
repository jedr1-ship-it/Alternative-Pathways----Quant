"""Who, among the under-55 OLF leavers, is enrolled in school: by age at
exit and by family situation. Calendar 2020-2024, from the extended
file (PRNLFSCH among those with a yes/no answer). Writes
report/figures_deck/study_olf55.{pdf,png}. Run from the repo root."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import BLUE, CORAL, GRAY, INK, SUBTLE

OUT = "report/figures_deck"

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
d["leftlf"] = d.A_LFSR.isin([5, 6, 7])
d["leaver"] = (emp & ~d.teach_now) | d.A_LFSR.isin([3, 4]) | d.leftlf
kids = d[(d.PEPAR1 > 0) | (d.PEPAR2 > 0)][
    ["asec_year", "PH_SEQ", "PEPAR1", "PEPAR2"]].copy()
k1 = kids.rename(columns={"PEPAR1": "pline"})[["asec_year", "PH_SEQ", "pline"]]
k2 = kids[kids.PEPAR2 > 0].rename(columns={"PEPAR2": "pline"})[
    ["asec_year", "PH_SEQ", "pline"]]
kk = pd.concat([k1, k2])
kk = kk[kk.pline > 0]
agg = kk.groupby(["asec_year", "PH_SEQ", "pline"]).size().rename(
    "nkids").reset_index()
d = d.merge(agg, left_on=["asec_year", "PH_SEQ", "A_LINENO"],
            right_on=["asec_year", "PH_SEQ", "pline"], how="left")
d["haskid"] = d.nkids.fillna(0) > 0
U = d[d.teach_ly & d.ba_plus & (d.A_AGE >= 18) & d.MARSUPWT.notna()
      & d.cal_year.between(2020, 2024) & d.leaver & d.leftlf
      & (d.A_AGE < 55)].copy()
U["insch"] = np.where(U.PRNLFSCH == 1, 1.0,
                      np.where(U.PRNLFSCH == 2, 0.0, np.nan))

def stat(m):
    g = U[m & U.insch.notna()]
    return 100 * np.average(g.insch, weights=g.MARSUPWT), len(g)

age_groups = [("Under 30", U.A_AGE < 30),
              ("30–39", U.A_AGE.between(30, 39)),
              ("40–54", U.A_AGE.between(40, 54))]
U["female"] = U.A_SEX == 2
fam_groups = [("Mothers,\nchild at home", U.female & U.haskid),
              ("Women, no\nown child", U.female & ~U.haskid),
              ("Fathers", ~U.female & U.haskid),
              ("Men, no\nown child", ~U.female & ~U.haskid)]

fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.6),
                         gridspec_kw={"width_ratios": [3, 4]})
for ax, groups, title, colors in [
        (axes[0], age_groups, "by age at exit",
         [BLUE, "#7C98C0", "#B9C8DC"]),
        (axes[1], fam_groups, "by group of the previous chart",
         [CORAL, "#AEC3DE", "#5B7BA6", "#6E6E6E"])]:
    vals, ns, labs = [], [], []
    for lab, m in groups:
        v, n = stat(m)
        vals.append(v); ns.append(n); labs.append(lab)
    xs = np.arange(len(vals))
    ax.bar(xs, vals, width=0.62, color=colors[:len(vals)])
    for x, v, n in zip(xs, vals, ns):
        ax.text(x, v + 1.2, f"{v:.0f}%", ha="center", va="bottom",
                fontsize=12, fontweight="bold", color=INK)
        ax.text(x, -5.4, f"n = {n}", ha="center", va="top",
                fontsize=8, color=SUBTLE)
    ax.set_xticks(xs)
    ax.set_xticklabels(labs, fontsize=10)
    ax.set_ylim(0, 55)
    ax.set_title(title, fontsize=11, color=INK)
    ax.tick_params(axis="x", length=0)
axes[0].set_ylabel("of each group, the share enrolled\nin school, percent",
                   fontsize=10)
axes[1].set_yticklabels([])
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(f"{OUT}/study_olf55.pdf")
fig.savefig(f"{OUT}/study_olf55.png", dpi=200)
print("saved study_olf55")
