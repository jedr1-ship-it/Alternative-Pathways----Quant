"""Third level of the cascade: take the under-55 OLF bar exactly as it
appears in the previous chart (same segments, colors and values) and
shade, inside each group, the part that is enrolled in school.
Calendar 2020-2024, PRNLFSCH among those with a yes/no answer. Writes
report/figures_deck/study_olf55.{pdf,png}. Run from the repo root."""
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
LIGHT, GRAYD, FATH = "#AEC3DE", "#6E6E6E", "#5B7BA6"
C1, C2, C3 = CORAL, "#D3766F", "#E2A19B"

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
d["haskid"] = d.nkids.fillna(0) > 0
d["baby"] = (d.youngest < 1).fillna(False)
d["kid_u6"] = (d.youngest < 6).fillna(False)

T = d[d.teach_ly & d.ba_plus & (d.A_AGE >= 18) & d.MARSUPWT.notna()
      & d.cal_year.between(2020, 2024)].copy()
L = T[T.leaver]
wl = L.MARSUPWT.sum()
def share(m):
    return L.loc[m, "MARSUPWT"].sum() / wl * 100

f = L.leftlf & (L.A_AGE < 55)
fem = L.A_SEX == 2
olfu = share(f)
segs = [("Baby born\nthat year", share(f & fem & L.baby), C1),
        ("Youngest\nunder 6", share(f & fem & ~L.baby & L.kid_u6), C2),
        ("Youngest\n6–17", share(f & fem & ~L.kid_u6 & L.haskid), C3),
        ("Women, no own\nchild at home", share(f & fem & ~L.haskid), LIGHT),
        ("Fathers", share(f & ~fem & L.haskid), FATH),
        ("Men, no own\nchild at home", share(f & ~fem & ~L.haskid), GRAYD)]

U = L[f].copy()
U["insch"] = np.where(U.PRNLFSCH == 1, 1.0,
                      np.where(U.PRNLFSCH == 2, 0.0, np.nan))
U["female"] = U.A_SEX == 2
def st(m):
    g = U[m & U.insch.notna()]
    return 100 * np.average(g.insch, weights=g.MARSUPWT), len(g)

# study shares, one per visual group (the three mother segments share one)
sh_mom, n_mom = st(U.female & U.haskid)
sh_wnk, n_wnk = st(U.female & ~U.haskid)
sh_fat, n_fat = st(~U.female & U.haskid)
sh_mnk, n_mnk = st(~U.female & ~U.haskid)
sh_u30, n_u30 = st(U.A_AGE < 30)
sh_all, n_all = st(pd.Series(True, index=U.index))
print("study shares:", round(sh_mom, 1), round(sh_wnk, 1), round(sh_fat, 1),
      round(sh_mnk, 1), "| under30", round(sh_u30, 1), "| all",
      round(sh_all, 1))

fig, ax = plt.subplots(figsize=(9.6, 4.6))
Y1, Y0, H = 1.72, 0.80, 0.34
sc = 100.0 / olfu
# ---- the bar of the previous chart, unchanged ----
x = 0
spans = {}
lvl = 0
for lab, v, c in segs:
    w = v * sc
    ax.barh([Y1], [w], left=x, color=c, height=H)
    ax.text(x + w / 2, Y1, f"{v:.0f}", ha="center", va="center",
            color="white" if c in (C1, C2, FATH, GRAYD) else INK,
            fontsize=10.5, fontweight="bold")
    yl = Y1 + H / 2 + (0.08 if lvl % 2 == 0 else 0.45)
    ax.text(x + w / 2, yl, lab, ha="center", va="bottom", fontsize=8.4,
            color=INK)
    spans[lab] = (x, w)
    lvl += 1
    x += w
ax.text(-1.2, Y1, "Who leaves the labor\nforce before 55\n(the 24 of the"
        " previous chart)", ha="right", va="center", fontsize=9.2,
        color=INK)
# ---- inside each group, the part enrolled in school ----
groups = [("mothers", 0, 3, sh_mom, C1),
          ("women_nokid", 3, 4, sh_wnk, LIGHT),
          ("fathers", 4, 5, sh_fat, FATH),
          ("men_nokid", 5, 6, sh_mnk, GRAYD)]
for gi, (name, i0, i1, sh, c) in enumerate(groups):
    gx = spans[segs[i0][0]][0]
    gw = sum(spans[segs[i][0]][1] for i in range(i0, i1))
    ax.barh([Y0], [gw], left=gx, color="white", height=H,
            edgecolor="#B9BEC4", lw=0.8)
    wstudy = gw * sh / 100
    ax.barh([Y0], [wstudy], left=gx, color=c, height=H)
    yl = Y0 - H / 2 - (0.12 if gi % 2 == 0 else 0.46)
    ax.text(gx + gw / 2, yl, f"{sh:.0f}% study",
            ha="center", va="top", fontsize=9.4, color=INK,
            fontweight="bold")
    for xx in (gx, gx + gw):
        ax.plot([xx, xx], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE,
                lw=0.8)
ax.text(-1.2, Y0, "Of each group,\nthe share enrolled\nin school",
        ha="right", va="center", fontsize=9.2, color=INK)
ax.text(50, Y0 - H / 2 - 0.80,
        f"Overall, {sh_all:.0f}% of the group is studying; among those "
        f"under 30, {sh_u30:.0f}%.",
        ha="center", va="top", fontsize=9.6, color=INK, style="italic")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.55, 2.75)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/study_olf55.pdf")
fig.savefig(f"{OUT}/study_olf55.png", dpi=200)
print("saved study_olf55")
