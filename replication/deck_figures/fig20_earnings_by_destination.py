import sys, glob
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

OUT = "report/figures_deck"
BLUE, CORAL, GREEN, GRAY, DARK, MUT = "#2A5DB0", "#C4534B", "#3E7C59", "#9AA1A8", "#3B4046", "#8A9096"
CORE = {2300, 2310, 2320, 2330}
def tset(ay): return CORE | ({2340} if ay <= 2019 else {2360})

R = pd.concat([pd.read_parquet(f, columns=["asec_year","PERIDNUM","OCCUP","PEIOOCC",
              "A_LFSR","A_AGE","A_SEX","A_HGA","MARSUPWT","WSAL_VAL"])
               for f in sorted(glob.glob("data/raw/asec/asec_rich_*.parquet"))],
              ignore_index=True)
for c in R.columns:
    if c != "PERIDNUM":
        R[c] = pd.to_numeric(R[c], errors="coerce")
link = []
for ay in range(2011, 2025):
    cs = tset(ay)
    t0 = R[(R.asec_year==ay) & R.OCCUP.isin(cs) & (R.A_HGA>=43) & (R.A_AGE>=18)
           & R.PERIDNUM.notna() & (R.WSAL_VAL>0)]
    nxt = R[R.asec_year==ay+1][["PERIDNUM","PEIOOCC","A_LFSR","A_SEX","A_AGE","WSAL_VAL"]]
    m = t0.merge(nxt, on="PERIDNUM", suffixes=("","_1"))
    m = m[(m.A_SEX==m.A_SEX_1) & (m.A_AGE_1-m.A_AGE).between(0,2)]
    emp0 = m["A_LFSR"].isin([1,2])
    m["stay"] = (emp0 & m.PEIOOCC.isin(cs))
    emp1 = m["A_LFSR_1"].isin([1,2])
    m["sw"] = (emp1 & ~m["PEIOOCC_1"].isin(cs))
    link.append(m)
L = pd.concat(link, ignore_index=True)
L = L[L.WSAL_VAL_1>0]
L["dlog"] = np.log(L.WSAL_VAL_1) - np.log(L.WSAL_VAL)
o = L["PEIOOCC_1"]
edu = (o.between(2200,2555)) | (o==230)
care = o.between(2000,2025) | (o==4600)
prof = ((o.between(10,960)&(o!=230)) | o.between(1000,1965)
        | o.between(2600,2960) | o.between(3000,3550))
def wmed(d):
    d = d.sort_values("dlog"); cw = d["MARSUPWT"].cumsum()
    return d.loc[cw>=cw.iloc[-1]/2, "dlog"].iloc[0]*100
S = L[L.stay & L.PEIOOCC.isin ] if False else None
groups = [("Stayers (kept teaching)", L[L["stay"]], GRAY),
          ("To an education job", L[L.sw & edu], BLUE),
          ("To care and children", L[L.sw & care], CORAL),
          ("To other professional", L[L.sw & prof & ~edu & ~care], GREEN),
          ("To sales, office, manual", L[L.sw & ~edu & ~care & ~prof], "#6E6E6E")]
fig, ax = plt.subplots(figsize=(8.8,4.4))
ys = np.arange(len(groups))[::-1]
for y, (lab, d, c) in zip(ys, groups):
    v = wmed(d)
    ax.barh([y],[v], height=0.55, color=c, zorder=3)
    ax.text(v + (1.2 if v>=0 else -1.2), y, f"{v:+.0f}", va="center",
            ha="left" if v>=0 else "right", fontsize=11, color=DARK, fontweight="bold")
    ax.text(-38, y, f"{lab}  (n={len(d):,})", va="center", ha="left",
            fontsize=9.6, color=c if lab!="Stayers (kept teaching)" else DARK)
ax.axvline(0, color="#999999", lw=1.0)
ax.set_xlim(-38, 22); ax.set_ylim(-0.6, len(groups)-0.35)
ax.set_yticks([]) 
ax.set_xlabel("Median change in annual earnings, log points x 100", fontsize=10, color=DARK)
ax.tick_params(length=0, labelsize=9)
ax.grid(axis="x", color="#F1F2F3", lw=1.0)
ax.set_axisbelow(True)
for s in ("top","right","left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8DBDE")
fig.tight_layout(); fig.savefig(f"{OUT}/pay7_destinations_deck.png", dpi=200)
fig.savefig(f"{OUT}/pay7_destinations_deck.pdf"); plt.close(fig)
for lab, d, c in groups:
    print(lab, len(d), round(wmed(d),1))
