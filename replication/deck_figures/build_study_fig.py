"""Share enrolled in school among teachers who left the labor force
before 55, by age at exit, against the benchmark of all college
graduates out of the labor force at the same ages (same ASEC files,
same question, calendar 2020-2024). Writes study_olf55.{pdf,png}."""
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
NAVY, BENCH = "#102D5E", "#C9CFD6"

d = pd.read_parquet("data/processed/asec_ext.parquet",
    columns=["asec_year", "OCCUP", "PEIOOCC", "A_HGA", "A_AGE", "A_LFSR",
             "MARSUPWT", "PRNLFSCH", "A_SEX"])
d = d[d.asec_year.between(2021, 2025) & d.MARSUPWT.notna()]
d["ba"] = d.A_HGA >= 43
d["olf"] = d.A_LFSR.isin([5, 6, 7])
d["insch"] = np.where(d.PRNLFSCH == 1, 1.0,
                      np.where(d.PRNLFSCH == 2, 0.0, np.nan))
TEACH = {2300, 2310, 2320, 2330, 2340, 2360}

# teachers who left the labor force before 55 (longest job last year taught)
T = d[d.ba & d.OCCUP.isin(TEACH) & d.olf & (d.A_AGE >= 18) & (d.A_AGE < 55)
      & d.insch.notna()]
# benchmark: all other college graduates out of the labor force, under 55
B = d[d.ba & ~d.OCCUP.isin(TEACH) & d.olf & (d.A_AGE >= 18) & (d.A_AGE < 55)
      & d.insch.notna()]

def sh(g, m):
    g = g[m]
    return 100 * np.average(g.insch, weights=g.MARSUPWT), len(g)

BANDS = [("Under 30", lambda g: g.A_AGE < 30),
         ("30\u201339", lambda g: g.A_AGE.between(30, 39)),
         ("40\u201354", lambda g: g.A_AGE.between(40, 54))]
tv, tn, bv = [], [], []
for lab, f in BANDS:
    v, n = sh(T, f(T)); tv.append(v); tn.append(n)
    v2, _ = sh(B, f(B)); bv.append(v2)
print("teachers:", [round(v, 1) for v in tv], "bench:", [round(v, 1) for v in bv])

fig, ax = plt.subplots(figsize=(10.6, 4.9))
xs = np.arange(3)
w = 0.36
b1 = ax.bar(xs - w / 2, tv, width=w, color=NAVY,
            label="Teachers who left the labor force")
b2 = ax.bar(xs + w / 2, bv, width=w, color=BENCH,
            label="All college graduates out of the labor force")
for x, v in zip(xs - w / 2, tv):
    ax.text(x, v + 1.5, f"{v:.0f}%", ha="center", va="bottom", fontsize=13,
            fontweight="bold", color=NAVY)
for x, v in zip(xs + w / 2, bv):
    ax.text(x, v + 1.5, f"{v:.0f}%", ha="center", va="bottom", fontsize=12,
            color="#6B7480")
for x, n in zip(xs - w / 2, tn):
    ax.text(x, -4.6, f"n = {n}", ha="center", va="top", fontsize=8.5,
            color=SUBTLE)
ax.set_xticks(xs)
ax.set_xticklabels([b[0] for b in BANDS], fontsize=13)
ax.set_ylim(0, 70)
ax.set_ylabel("share enrolled in school, percent", fontsize=11)
ax.tick_params(axis="x", length=0)
ax.legend(frameon=False, fontsize=11, loc="upper right")
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(f"{OUT}/study_olf55.pdf")
fig.savefig(f"{OUT}/study_olf55.png", dpi=200)
print("saved study_olf55")
