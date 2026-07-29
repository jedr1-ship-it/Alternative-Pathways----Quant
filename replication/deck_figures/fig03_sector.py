import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

OUT = "report/figures_deck"
BLUE, CORAL, DARK, MUT = "#2A5DB0", "#C4534B", "#3B4046", "#8A9096"

M = pd.read_parquet("data/processed/asec_master.parquet",
                    columns=["teacher","ba_plus","A_AGE","WGT","leaver",
                             "public_ly","asec_year"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
T = M[(M.teacher==1)&(M.ba_plus==1)&(M.A_AGE>=18)&M.WGT.notna()&M.leaver.notna()]
T["cal_year"] = T["asec_year"] - 1

rows = []
for (cy, pub), g in T.groupby(["cal_year", "public_ly"]):
    w = g["WGT"].values
    p = np.average(g["leaver"], weights=w)
    neff = w.sum()**2/(w**2).sum()
    rows.append({"cal_year": cy, "pub": pub, "rate": p*100,
                 "se": np.sqrt(p*(1-p)/neff)*1.5*100})
D = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(10.6, 5.4))
ax.axvspan(2018.5, 2020.5, color="#EFF0F2", zorder=0)
ax.text(2019.5, 16.55, "Covid", ha="center", fontsize=10, color=MUT)

for pub, c, lab in [(0, CORAL, "Private school"), (1, BLUE, "Public school")]:
    d = D[D.pub==pub].sort_values("cal_year").reset_index(drop=True)
    ax.fill_between(d.cal_year, d.rate-1.96*d.se, d.rate+1.96*d.se,
                    color=c, alpha=0.10, lw=0)
    m = d.rate.mean()
    ax.axhline(m, color=c, lw=0.9, ls=(0, (1, 3)), alpha=0.85)
    ax.plot(d.cal_year, d.rate, color=c, lw=2.5, solid_capstyle="round")
    ipk = int(d.rate[1:].idxmax())
    for i, dy in [(ipk, 10), (len(d)-1, 10)]:
        ax.plot(d.cal_year[i], d.rate[i], "o", color=c, ms=6.5,
                mec="white", mew=1.2, zorder=5)
        ax.annotate(f"{d.rate[i]:.1f}", (d.cal_year[i], d.rate[i]),
                    xytext=(0, dy), textcoords="offset points",
                    ha="center", fontsize=11, color=c, fontweight="bold")
    ax.annotate(lab, (2024.55, d.rate.iloc[-1]), va="center",
                fontsize=11.5, color=c, fontweight="bold",
                xytext=(14, 0), textcoords="offset points")
ax.text(2003.4, 3.1, "1997-2024 averages:  private 11.8,  public 7.4",
        fontsize=10, color=DARK)
ax.set_ylim(0, 17.2)
ax.set_yticks(range(0, 17, 2))
ax.set_xlim(1996.4, 2030.5)
ax.set_xticks(range(1998, 2025, 2))
ax.set_xticklabels(range(1998, 2025, 2), fontsize=9, rotation=45)
ax.set_ylabel("Percent leaving teaching", fontsize=11, color=DARK)
ax.tick_params(length=0, labelsize=9.5, colors=MUT)
ax.grid(axis="y", color="#F1F2F3", lw=1.0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8DBDE")
fig.tight_layout()
fig.savefig(f"{OUT}/pubpriv_series.pdf")
fig.savefig(f"{OUT}/pubpriv_series.png", dpi=200)
print("ok")
