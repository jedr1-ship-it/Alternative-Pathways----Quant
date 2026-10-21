"""The employed-leavers flow chart pooled over the whole period, calendar
1997-2024. Destination groups are mapped across the 1990 and
2002/2010/2018 occupation classifications. Writes flow_employed_pooled."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import BLUE, CORAL, GOLD, GREEN, GRAY, INK, SUBTLE

OUT = "report/figures_deck"
LIGHT, GRAYD = "#C3D4E9", "#9AA3AE"

M = pd.read_parquet("data/processed/asec_master.parquet",
    columns=["asec_year", "OCCUP", "PEIOOCC", "A_LFSR", "WGT", "ba_plus",
             "A_AGE"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
M = M[M.asec_year.between(1998, 2025)]
def tset(ay):
    if ay <= 2002:
        return {155, 156, 157, 158, 159}
    return {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360})
M["teach_ly"] = False
M["teach_now"] = False
M["old_codes"] = M.asec_year <= 2002
for ay, g in M.groupby("asec_year"):
    s = tset(int(ay))
    M.loc[g.index, "teach_ly"] = g.OCCUP.isin(s)
    M.loc[g.index, "teach_now"] = g.PEIOOCC.isin(s)
T = M[M.teach_ly & (M.ba_plus == 1) & (M.A_AGE >= 18) & M.WGT.notna()]
emp_now = T.A_LFSR.isin([1, 2])
T = T.assign(switch=emp_now & ~T.teach_now, unemp=T.A_LFSR.isin([3, 4]),
             leftlf=T.A_LFSR.isin([5, 6, 7]))
L = T[T.switch | T.unemp | T.leftlf]
wl = L.WGT.sum()
def share(m):
    return L.WGT[m].sum() / wl * 100
emp = share(L.switch)
olf55 = share(L.leftlf & (L.A_AGE >= 55))
olfu = share(L.leftlf & (L.A_AGE < 55))
un = share(L.unemp)
cs = {2300, 2310, 2320, 2330, 2340, 2360}
o = L.PEIOOCC
sw = L.switch
oldc = L.old_codes
# 2002/2010/2018 classifications
edu_new = (o.between(2200, 2555) & ~o.isin(cs)) | (o == 230)
care_new = o.between(2000, 2025) | (o == 4600)
prof_new = ((o.between(10, 960) & (o != 230)) | o.between(1000, 1965)
            | o.between(2600, 2960) | o.between(3000, 3550))
# 1990 classification (surveys 1998-2002): the same groups
edu_old = (o == 14) | o.between(113, 154) | o.isin({164, 165, 387})
care_old = o.isin({163, 174, 406, 468})
prof_old = ((o.between(3, 37) & (o != 14)) | o.between(43, 112)
            | o.between(166, 173) | o.between(178, 199)
            | o.between(203, 235))
edu_m = np.where(oldc, edu_old, edu_new)
care_m = np.where(oldc, care_old, care_new)
prof_m = np.where(oldc, prof_old, prof_new)
edu_job = share(sw & edu_m); care = share(sw & care_m)
otherprof = share(sw & prof_m); salesetc = emp - edu_job - care - otherprof
print(f"pooled 1997-2024: n_leavers={len(L)} | top {emp:.1f}/{olf55:.1f}/"
      f"{olfu:.1f}/{un:.1f} | split {edu_job:.1f}/{care:.1f}/{otherprof:.1f}/"
      f"{salesetc:.1f}")

fig, ax = plt.subplots(figsize=(9.6, 4.6))
TAGS = {"Employed": ("Switchers", "#3A6BA8"),
        "Out of the labor force, <55": ("Early exits", "#B8922F"),
        "Out of the labor force, 55+": ("Retirees", "#7E99BD")}
Y1, Y0, H = 1.72, 0.55, 0.34
# softened palette for the flow charts, easier on the eye
SBLUE, SGOLD, SCORAL, SGREEN, SGRAY = ("#5E8DC9", "#E8BE55", "#CC6F63",
                                       "#63A388", "#AEB4BB")
top = [("Employed", emp, SBLUE),
       ("Out of the labor force, <55", olfu, SGOLD),
       ("Out of the labor force, 55+", olf55, LIGHT),
       ("Unemployed", un, GRAYD)]
x = 0
for lab, v, c in top:
    ax.barh([Y1], [v], left=x, color=c, height=H)
    txtc = "white" if c in (SBLUE, GRAYD) else INK
    ax.text(x + v / 2, Y1, f"{v:.0f}", ha="center", va="center", color=txtc,
            fontsize=11, fontweight="bold")
    yl = Y1 + H / 2 + (0.10 if lab != "Unemployed" else 0.24)
    ax.text(x + v / 2, yl, lab, ha="center", va="bottom", fontsize=9.3,
            color=INK, fontweight="bold")
    if lab in TAGS:
        tg, tc = TAGS[lab]
        ax.text(x + v / 2, Y1 + H / 2 + 0.42, tg, ha="center",
                va="bottom", fontsize=10, color=tc, fontweight="bold",
                style="italic")
    x += v
bot = [("Education job", edu_job, SBLUE),
       ("Care and\nchildren", care, SCORAL),
       ("Other professional\n(usually degree jobs)", otherprof,
        SGREEN),
       ("Sales, office and manual\n(usually non-degree jobs)", salesetc,
        SGRAY)]
sc = 100.0 / emp
x = 0
for lab, v, c in bot:
    w = v * sc
    ax.barh([Y0], [w], left=x, color=c, height=H)
    ax.text(x + w / 2, Y0, f"{v * sc:.0f}%", ha="center", va="center",
            color="white" if c != SGRAY else INK, fontsize=10.5,
            fontweight="bold")
    ax.text(x + w / 2, Y0 - H / 2 - 0.10, lab, ha="center", va="top",
            fontsize=9.3, color=INK, fontweight="bold")
    x += w
ax.plot([0, 0], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=1.0)
ax.plot([emp, 100], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=1.0)
ax.text(-1.2, Y1, "Of every 100\nleavers", ha="right", va="center",
        fontsize=9.6, color=INK)
ax.text(-1.2, Y0, "What the employed\nare doing", ha="right", va="center",
        fontsize=9.6, color=INK)
ec = edu_job + care
xb = ec * sc
yb = Y0 - H / 2 - 0.52
ax.plot([0, 0, xb, xb], [yb + 0.05, yb, yb, yb + 0.05], color=INK, lw=1.1)
ax.text(xb / 2, yb - 0.07,
        f"{ec * sc:.0f}% of the employed stay in education or care "
        f"({ec:.0f} of every 100 leavers)",
        ha="center", va="top", fontsize=9.6, color=INK, fontweight="bold")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.35, 2.75)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/flow_employed_pooled.pdf")
fig.savefig(f"{OUT}/flow_employed_pooled.png", dpi=200)
print("saved flow_employed_pooled")
