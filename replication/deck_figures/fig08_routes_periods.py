import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import BLUE, GOLD, INK

OUT = "report/figures_deck"
LIGHT, INKGRAY = "#AEC3DE", "#6E6E6E"
CORE = {2300, 2310, 2320, 2330}

def tset(ay):
    return CORE | ({2340} if ay <= 2019 else {2360})

M = pd.read_parquet("data/processed/asec_master.parquet",
                    columns=["asec_year", "OCCUP", "PEIOOCC", "A_LFSR",
                             "WGT", "ba_plus", "A_AGE"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
M = M[(M["ba_plus"] == 1) & (M["A_AGE"] >= 18) & M["WGT"].notna()
      & (M["asec_year"] >= 2003)]

recs = []
for ay, g in M.groupby("asec_year"):
    cs = tset(int(ay))
    t = g[g["OCCUP"].isin(cs)].copy()
    emp = t["A_LFSR"].isin([1, 2])
    t["switch"] = (emp & ~t["PEIOOCC"].isin(cs)).astype(int)
    t["unemp"] = t["A_LFSR"].isin([3, 4]).astype(int)
    t["leftlf"] = (~t["A_LFSR"].isin([1, 2, 3, 4])).astype(int)
    t["leaver"] = (t["switch"] | t["unemp"] | t["leftlf"]).astype(int)
    L = t[t["leaver"] == 1].copy()
    L["olf55"] = ((L["leftlf"] == 1) & (L["A_AGE"] >= 55)).astype(int)
    L["olfu55"] = ((L["leftlf"] == 1) & (L["A_AGE"] < 55)).astype(int)
    recs.append(L[["asec_year", "WGT", "switch", "olf55", "olfu55", "unemp"]])
S = pd.concat(recs, ignore_index=True)
S["cal_year"] = S["asec_year"] - 1

WINDOWS = [("2002-2009", 2002, 2009), ("2010-2016", 2010, 2016),
           ("2017-2024", 2017, 2024)]
CATS = [("switch", "Employed", BLUE, "white"),
        ("olf55", "Out of the labor\nforce, 55+", LIGHT, INK),
        ("olfu55", "Out of the labor\nforce, <55", GOLD, INK),
        ("unemp", "Unemployed", INKGRAY, "white")]

fig, ax = plt.subplots(figsize=(9.6, 4.3))
H = 0.42
ys = [2.0, 1.0, 0.0]
for (lab, a, b), y in zip(WINDOWS, ys):
    win = S[S["cal_year"].between(a, b)]
    w = win["WGT"].sum()
    x = 0
    for k, klab, c, tc in CATS:
        v = (win["WGT"] * win[k]).sum() / w * 100
        ax.barh([y], [v], left=x, color=c, height=H)
        ax.text(x + v / 2, y, f"{v:.0f}", ha="center", va="center",
                color=tc, fontsize=11, fontweight="bold")
        if y == ys[0]:
            ax.text(x + v / 2, y + H / 2 + 0.09, klab, ha="center",
                    va="bottom", fontsize=8.8, color=INK)
        x += v
    ax.text(-1.5, y, lab, ha="right", va="center", fontsize=11,
            color=INK, fontweight="bold")
ax.set_xlim(-13, 101)
ax.set_ylim(-0.45, 2.85)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/routes_bars3.pdf")
fig.savefig(f"{OUT}/routes_bars3.png", dpi=200)
print("saved")
