"""Why teachers leave the labor force before 55, by age at exit:
share enrolled in school, with an own child at home, and with a
disability or fair/poor health (not mutually exclusive). Calendar
2020-2024. Writes study_reasons.{pdf,png}."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import INK, SUBTLE

OUT = "report/figures_deck"
NAVY, CORAL, GRAYD = "#102D5E", "#B5443C", "#8C8C8C"

d = pd.read_parquet("data/processed/asec_ext.parquet")
d["cal_year"] = d.asec_year - 1
def tset(ay):
    return {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360})
d["teach_ly"] = False
for ay, g in d.groupby("asec_year"):
    d.loc[g.index, "teach_ly"] = g.OCCUP.isin(tset(int(ay)))
d["ba"] = d.A_HGA >= 43
d["leftlf"] = d.A_LFSR.isin([5, 6, 7])
kids = d[(d.PEPAR1 > 0) | (d.PEPAR2 > 0)][
    ["asec_year", "PH_SEQ", "PEPAR1", "PEPAR2"]].copy()
k1 = kids.rename(columns={"PEPAR1": "pline"})[["asec_year", "PH_SEQ", "pline"]]
k2 = kids[kids.PEPAR2 > 0].rename(columns={"PEPAR2": "pline"})[
    ["asec_year", "PH_SEQ", "pline"]]
kk = pd.concat([k1, k2])
kk = kk[kk.pline > 0]
agg = kk.groupby(["asec_year", "PH_SEQ", "pline"]).size().rename(
    "nk").reset_index()
d = d.merge(agg, left_on=["asec_year", "PH_SEQ", "A_LINENO"],
            right_on=["asec_year", "PH_SEQ", "pline"], how="left")
d["haskid"] = d.nk.fillna(0) > 0
U = d[d.teach_ly & d.ba & d.cal_year.between(2020, 2024) & d.leftlf
      & d.A_AGE.between(18, 54) & d.MARSUPWT.notna()].copy()
U["insch"] = np.where(U.PRNLFSCH == 1, 1.0,
                      np.where(U.PRNLFSCH == 2, 0.0, np.nan))
U["dh"] = ((U.DIS_HP == 1) | (U.HEA.isin([4, 5]))).astype(float)

BANDS = [("Under 30", U.A_AGE < 30), ("30\u201339", U.A_AGE.between(30, 39)),
         ("40\u201354", U.A_AGE.between(40, 54))]
S, K, H, N = [], [], [], []
for lab, m in BANDS:
    g = U[m]; w = g.MARSUPWT
    ins = g[g.insch.notna()]
    S.append(100 * np.average(ins.insch, weights=ins.MARSUPWT))
    K.append(100 * np.average(g.haskid, weights=w))
    H.append(100 * np.average(g.dh, weights=w))
    N.append(len(g))
print([round(v, 1) for v in S], [round(v, 1) for v in K],
      [round(v, 1) for v in H], N)

fig, ax = plt.subplots(figsize=(10.8, 4.9))
xs = np.arange(3)
w = 0.26
ax.bar(xs - w, S, width=w, color=NAVY, label="Enrolled in school")
ax.bar(xs, K, width=w, color=CORAL, label="Own child at home")
ax.bar(xs + w, H, width=w, color=GRAYD,
       label="Disability or fair/poor health")
for off, vals, c in [(-w, S, NAVY), (0, K, CORAL), (w, H, GRAYD)]:
    for x, v in zip(xs + off, vals):
        ax.text(x, v + 1.6, f"{v:.0f}%", ha="center", va="bottom",
                fontsize=11.5, fontweight="bold", color=c)
for x, n in zip(xs, N):
    ax.text(x, -6.2, f"n = {n}", ha="center", va="top", fontsize=8.5,
            color=SUBTLE)
ax.set_xticks(xs)
ax.set_xticklabels([b[0] for b in BANDS], fontsize=13)
ax.set_ylim(0, 85)
ax.set_ylabel("share of the group, percent", fontsize=11)
ax.tick_params(axis="x", length=0)
ax.legend(frameon=False, fontsize=11, loc="upper left", ncol=1)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.annotate("Teachers who left the labor force before 55, 2020\u20132024. "
            "The markers are not mutually exclusive.",
            (0.0, -0.16), xycoords="axes fraction", fontsize=9.5,
            color=SUBTLE)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(f"{OUT}/study_reasons.pdf")
fig.savefig(f"{OUT}/study_reasons.png", dpi=200)
print("saved study_reasons")
