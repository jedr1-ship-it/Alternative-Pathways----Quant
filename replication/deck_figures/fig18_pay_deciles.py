import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

OUT = "report/figures_deck"
CORAL, DARK = "#C4534B", "#3B4046"

M = pd.read_parquet("data/processed/asec_master.parquet",
                    columns=["asec_year","teacher","ba_plus","A_AGE","WGT",
                             "leaver","WSAL_VAL"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
cpi = pd.read_csv("outputs/n_cpi.csv").set_index("year")["CPIAUCSL"]
M["cal_year"] = M["asec_year"] - 1
T = M[(M.teacher==1)&(M.ba_plus==1)&(M.A_AGE>=18)&M.WGT.notna()
      &M.leaver.notna()&(M.WSAL_VAL>0)&M.cal_year.between(2015,2024)].copy()
T["dec"] = T.groupby("cal_year")["WSAL_VAL"].transform(
    lambda s: pd.qcut(s.rank(method="first"), 10, labels=False)+1)

# decile boundaries in 2024 dollars: per-year cutoffs deflated, averaged
cuts = []
for y, g in T.groupby("cal_year"):
    q = np.percentile(g["WSAL_VAL"], np.arange(0, 101, 10))
    cuts.append(q * cpi.loc[2024]/cpi.loc[y])
cut = np.mean(cuts, axis=0)/1000

def fmt(v):
    return f"{v:.0f}"
labels = [f"<{fmt(cut[1])}k"]
for i in range(1, 9):
    labels.append(f"{fmt(cut[i])}-{fmt(cut[i+1])}k")
labels.append(f">{fmt(cut[9])}k")

rows = []
for d, g in T.groupby("dec"):
    rows.append({"d":int(d), "rate": np.average(g.leaver, weights=g.WGT)*100})
D3 = pd.DataFrame(rows)
fig, ax = plt.subplots(figsize=(8.8,4.4))
ax.bar(D3.d, D3.rate, width=0.62,
       color=[CORAL if d<=2 else "#D4DAE0" for d in D3.d], zorder=3)
for _, r in D3.iterrows():
    ax.annotate(f"{r['rate']:.0f}", (r["d"], r["rate"]), xytext=(0,5),
                textcoords="offset points", ha="center", fontsize=9.5,
                color=DARK, fontweight="bold")
ax.set_xticks(range(1,11))
ax.set_xticklabels(labels, fontsize=8.6, rotation=45, ha="right")
ax.set_xlabel("Within-year earnings decile among teachers ($1,000 of 2024)",
              fontsize=10, color=DARK)
ax.set_ylabel("Percent leaving teaching", fontsize=10, color=DARK)
ax.tick_params(length=0, labelsize=9)
ax.grid(axis="y", color="#F1F2F3", lw=1.0)
ax.set_axisbelow(True)
for s in ("top","right","left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8DBDE")
fig.tight_layout()
fig.savefig(f"{OUT}/pay3_deciles_deck.png", dpi=200)
fig.savefig(f"{OUT}/pay3_deciles_deck.pdf")
print("labels:", labels)
