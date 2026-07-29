import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

OUT = "report/figures_deck"
BLUE, CORAL, GREEN, GRAY, DARK, MUT = ("#2A5DB0", "#C4534B", "#3E7C59",
                                       "#9AA1A8", "#3B4046", "#8A9096")

M = pd.read_parquet("data/processed/asec_master.parquet",
                    columns=["asec_year", "teacher", "ba_plus", "A_AGE", "WGT",
                             "public_ly", "WSAL_VAL", "fullyear", "parttime_ly",
                             "OCCUP"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
cpi = pd.read_csv("outputs/n_cpi.csv").set_index("year")["CPIAUCSL"]
M["cal_year"] = M["asec_year"] - 1
M["earn24"] = M["WSAL_VAL"] * M["cal_year"].map(lambda y: cpi.loc[2024]/cpi.loc[y])
B = M[(M.ba_plus == 1) & M.WGT.notna()]

def wpct(d, col, q):
    d = d.sort_values(col)
    cw = d["WGT"].cumsum()/d["WGT"].sum()
    return d.loc[cw >= q, col].iloc[0]

FT = B[(B.fullyear == 1) & (B.parttime_ly == 0) & (B.WSAL_VAL > 0)
       & B.cal_year.between(2015, 2024)]

groups = []
groups.append(("Teachers", FT[FT.teacher == 1], BLUE))
o5 = FT[(FT.teacher == 0) & (FT.OCCUP > 0)]
groups.append(("Registered nurses",
               o5[o5.OCCUP.isin({3255, 3256, 3257, 3258, 3130})], GREEN))
groups.append(("Social workers",
               o5[o5.OCCUP.isin({2010, 2011, 2012, 2013, 2014})], CORAL))
groups.append(("Accountants", o5[o5.OCCUP == 800], GRAY))
groups.append(("All other graduates", o5, DARK))
fig, ax = plt.subplots(figsize=(8.8, 4.9))
ys = np.arange(len(groups))[::-1]
for y, (lab, d, c) in zip(ys, groups):
    p10, p50, p90 = [wpct(d, "earn24", q)/1000 for q in (0.1, 0.5, 0.9)]
    ax.plot([p10, p90], [y, y], color=c, lw=3, alpha=0.35,
            solid_capstyle="round")
    ax.plot([p50], [y], "o", color=c, ms=9, mec="white", mew=1.4, zorder=5)
    for v, va in [(p10, "P10"), (p50, "P50"), (p90, "P90")]:
        ax.annotate(f"{v:.0f}", (v, y), xytext=(0, 9),
                    textcoords="offset points", ha="center", fontsize=8.6,
                    color=DARK)
    ax.text(-4, y, lab, ha="right", va="center", fontsize=10.5, color=c,
            fontweight="bold" if lab == "Teachers" else "normal")
    ax.annotate(f"P90/P10 = {p90/p10:.1f}", (252, y), fontsize=9, color=MUT,
                va="center")
ax.set_xlim(-60, 285)
ax.set_ylim(-0.6, len(groups)-0.3)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/pay5_compression_deck.png", dpi=200)
fig.savefig(f"{OUT}/pay5_compression_deck.pdf")
plt.close(fig)
print("fig19 compression done")
