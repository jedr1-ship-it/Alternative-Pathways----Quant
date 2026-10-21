"""Cascade-style chart: the under-55 OLF group (the 24 of every 100
leavers, calendar 2020-2024) split into the six family groups, and below
it the share of each group enrolled in school. Same derivation as
build_flow5yr_figs.py; pinks for the women's groups, blues for the
men's. Writes study_bygroup.{pdf,png}."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import CORAL, INK, SUBTLE

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
emp_now = d.A_LFSR.isin([1, 2])
d["switch"] = emp_now & ~d.teach_now
d["unemp"] = d.A_LFSR.isin([3, 4])
d["leftlf"] = d.A_LFSR.isin([5, 6, 7])
d["leaver"] = (d.switch | d.unemp | d.leftlf).astype(float)
d["female"] = (d.A_SEX == 2).astype(float)
kids = d[(d.PEPAR1 > 0) | (d.PEPAR2 > 0)][
    ["asec_year", "PH_SEQ", "PEPAR1", "PEPAR2", "A_AGE"]].copy()
k1 = kids.rename(columns={"PEPAR1": "pline"})[
    ["asec_year", "PH_SEQ", "pline", "A_AGE"]]
k2 = kids[kids.PEPAR2 > 0].rename(columns={"PEPAR2": "pline"})[
    ["asec_year", "PH_SEQ", "pline", "A_AGE"]]
kk = pd.concat([k1, k2])
kk = kk[kk.pline > 0]
agg = kk.groupby(["asec_year", "PH_SEQ", "pline"]).A_AGE.agg(
    youngest="min", nkids="size").reset_index()
d = d.merge(agg, left_on=["asec_year", "PH_SEQ", "A_LINENO"],
            right_on=["asec_year", "PH_SEQ", "pline"], how="left")
d["nkids"] = d.nkids.fillna(0)
d["haskid"] = d.nkids > 0
d["baby"] = (d.youngest < 1).fillna(False)
d["kid_u6"] = (d.youngest < 6).fillna(False)

T = d[d.teach_ly & d.ba_plus & (d.A_AGE >= 18) & d.MARSUPWT.notna()
      & d.cal_year.between(2020, 2024)].copy()
L = T[T.leaver == 1]
wl = L.MARSUPWT.sum()

def share(m):
    return L.loc[m, "MARSUPWT"].sum() / wl * 100

f = L.leftlf & (L.A_AGE < 55)
olfu = share(f)
baby = share(f & (L.female == 1) & L.baby)
u6 = share(f & (L.female == 1) & ~L.baby & L.kid_u6)
k617 = share(f & (L.female == 1) & ~L.kid_u6 & L.haskid)
nok = share(f & (L.female == 1) & ~L.haskid)
father = share(f & (L.female == 0) & L.haskid)
mennok = share(f & (L.female == 0) & ~L.haskid)

U = L[f].copy()
U["insch"] = np.where(U.PRNLFSCH == 1, 1.0,
                      np.where(U.PRNLFSCH == 2, 0.0, np.nan))
def insch(m):
    g = U[m & U.insch.notna()]
    return 100 * np.average(g.insch, weights=g.MARSUPWT)
s_moth = insch((U.female == 1) & U.haskid)
s_wnok = insch((U.female == 1) & ~U.haskid)
s_fath = insch((U.female == 0) & U.haskid)
s_mnok = insch((U.female == 0) & ~U.haskid)
s_all = insch(pd.Series(True, index=U.index))
s_u30 = insch(U.A_AGE < 30)
print("widths:", [round(v, 1) for v in (baby, u6, k617, nok, father, mennok)])
print("study:", [round(v, 1) for v in (s_moth, s_wnok, s_fath, s_mnok,
                                       s_all, s_u30)])

# pinks for the women's groups, blues for the men's
C1, C2, C3, C4 = "#CC6F63", "#DC948A", "#EBB9B0", "#F7DAD4"
M1, M2 = "#7095C2", "#B9CDE8"
fig, ax = plt.subplots(figsize=(9.6, 4.6))
Y1, Y0, H = 1.72, 0.55, 0.34
segs = [("Baby born\nthat year", baby, C1, "white"),
        ("Youngest\nunder 6", u6, C2, INK),
        ("Youngest\n6–17", k617, C3, INK),
        ("Women, no own\nchild at home", nok, C4, INK),
        ("Fathers", father, M1, "white"),
        ("Men, no own\nchild at home", mennok, M2, INK)]
sc = 100.0 / olfu
x = 0
lvl = 0
edges = [0]
for lab, v, c, tc in segs:
    w = v * sc
    ax.barh([Y1], [w], left=x, color=c, height=H)
    yl = Y1 + H / 2 + 0.12
    ax.text(x + w / 2, yl, lab, ha="center", va="bottom", fontsize=9.0,
            color=INK, fontweight="bold")
    lvl += 1
    x += w
    edges.append(x)
# bottom bar: within each family group, the share enrolled in school
xm = (baby + u6 + k617) * sc          # mothers as one block
regions = [(0, xm, s_moth, C1),
           (xm, edges[4], s_wnok, C4),
           (edges[4], edges[5], s_fath, M1),
           (edges[5], 100, s_mnok, M2)]
ax.barh([Y0], [100], left=0, color="white", height=H, edgecolor="#C9CFD6",
        lw=0.8, zorder=2)
lvl = 0
for x0, x1, sh, c in regions:
    ax.barh([Y0], [(x1 - x0) * sh / 100], left=x0, color=c, height=H,
            zorder=3)
    yl = Y0 - H / 2 - 0.16
    ax.text((x0 + x1) / 2, yl, f"{sh:.0f}% study", ha="center", va="top",
            fontsize=9.2, color=INK, fontweight="bold")
    ax.plot([x1, x1], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE,
            lw=0.9, zorder=1)
    lvl += 1
ax.plot([0, 0], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=0.9,
        zorder=1)
ax.text(-1.2, Y1, "Who leaves the labor\nforce before 55",
        ha="right", va="center", fontsize=9.2, color=INK)
ax.text(-1.2, Y0, "Of each group,\nthe share enrolled\nin school",
        ha="right", va="center", fontsize=9.2, color=INK)
ax.text(50, Y0 - H / 2 - 0.80,
        f"Overall, {s_all:.0f}% of the group is studying; among those "
        f"under 30, {s_u30:.0f}%.", ha="center", va="top", fontsize=9.4,
        color=INK, style="italic")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.85, 2.60)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/study_bygroup.pdf")
fig.savefig(f"{OUT}/study_bygroup.png", dpi=200)
print("saved study_bygroup")
