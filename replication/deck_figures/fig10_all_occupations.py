import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import BLUE, CORAL, GREEN, INK

OUT = "report/figures_deck"
CORE = {2300,2310,2320,2330}; cs = CORE|{2360}
GRAYB = "#5E6672"

M = pd.read_parquet("data/processed/asec_master.parquet",
    columns=["asec_year","teacher","ba_plus","A_AGE","WGT","leaver","switch","PEIOOCC"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
t = M[(M.asec_year>=2020)&(M.teacher==1)&(M.ba_plus==1)&(M.A_AGE>=18)
      &M.WGT.notna()&(M.leaver==1)&(M.switch==1)].copy()
lab = pd.read_csv("outputs/occ2018_labels.csv").set_index("code")["label"]
def bucket(c):
    c = int(c)
    if (2200 <= c <= 2555 and c not in cs) or c == 230: return "edu"
    if 2000 <= c <= 2025 or c == 4600: return "care"
    if (10 <= c <= 960 and c != 230) or 1000 <= c <= 1965 \
       or 2600 <= c <= 2960 or 3000 <= c <= 3550: return "prof"
    return "rest"
agg = t.groupby("PEIOOCC").agg(w=("WGT","sum"), n=("WGT","size"))
agg["share"] = agg.w/agg.w.sum()*100
agg["bucket"] = [bucket(c) for c in agg.index]
agg["label"] = [lab.get(int(c), f"code {int(c)}") for c in agg.index]

FIX = {"Secretaries and administrative assistants, except legal, medical, and executive":
       "Secretaries and admin. assistants",
       "Executive secretaries and executive administrative assistants":
       "Executive secretaries",
       "Education and childcare administrators": "Education administrators",
       "Educational, guidance, and career counselors and advisors":
       "Educational and career counselors",
       "Architects, except landscape and naval": "Architects",
       "Exercise trainers and group fitness instructors": "Exercise trainers",
       "Librarians and media collections specialists": "Librarians",
       "Other educational instruction and library workers":
       "Other instruction and library workers"}
def short(s, n=33):
    s = FIX.get(s, s)
    return s if len(s) <= n else s[:n-1].rstrip(" ,") + "…"

META = {"edu":  ("EDUCATION, NON-TEACHING", BLUE),
        "care": ("CARE", CORAL),
        "prof": ("PROFESSIONAL & MANAGERIAL", GREEN),
        "rest": ("SALES, OFFICE & MANUAL", GRAYB)}
items = []
for b in ["edu","care","prof","rest"]:
    d = agg[agg.bucket==b].sort_values("share", ascending=False)
    nm, col = META[b]
    items.append(("hdr", f"{nm} — {d.share.sum():.0f}%", col))
    for _, r in d.iterrows():
        items.append(("row", f"{r.share:.1f}", short(r.label), col))

NCOL, NROW = 6, 25
fig, ax = plt.subplots(figsize=(12.4, 5.45))
ax.set_xlim(0, NCOL); ax.set_ylim(0, NROW+1); ax.axis("off")
col = row = 0
for it in items:
    if it[0] == "hdr":
        if row > NROW - 5 and row > 0:
            col, row = col+1, 0
        if row > 0:
            row += 1          # blank slot above a mid-column header
        x, y = col+0.02, NROW - row
        ax.text(x, y, it[1], fontsize=6.1, color=it[2], fontweight="bold",
                ha="left", va="top", family="sans-serif")
        row += 2
    else:
        _, sh, nmm, c = it
        x, y = col+0.02, NROW - row
        ax.text(x, y, sh, fontsize=6.2, color=c, ha="left", va="top",
                fontweight="bold", family="sans-serif")
        ax.text(x+0.145, y, nmm, fontsize=6.2, color=INK, ha="left", va="top",
                family="sans-serif")
        row += 1
        if row >= NROW:
            col, row = col+1, 0
fig.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
fig.savefig(f"{OUT}/occ_all_slide.pdf")
fig.savefig(f"{OUT}/occ_all_slide.png", dpi=220)
print("cols used:", col, "row:", row, "items:", len(items))
