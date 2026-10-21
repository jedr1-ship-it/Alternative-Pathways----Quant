"""The under-55 OLF cascade pooled over the whole period, calendar
1997-2024, from the master file (same conventions as the old fig09).
Percent labels within the group. Writes flow_olf55_pooled."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import BLUE, CORAL, GOLD, INK, SUBTLE

OUT = "report/figures_deck"
LIGHT, GRAYD = "#C3D4E9", "#9AA3AE"
# softened palette for the flow charts, easier on the eye
SBLUE, SGOLD = "#5E8DC9", "#E8BE55"

M = pd.read_parquet("data/processed/asec_master.parquet",
    columns=["asec_year", "teacher", "ba_plus", "A_AGE", "WGT", "leaver",
             "leftlf", "unemp", "switch", "female", "new_baby", "child_u6",
             "n_children"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
T = M[(M.teacher == 1) & (M.ba_plus == 1) & (M.A_AGE >= 18) & M.WGT.notna()
      & M.leaver.notna() & M.asec_year.between(1998, 2025)]
L = T[T.leaver == 1]
wl = L.WGT.sum()
def share(m):
    return L.WGT[m].sum() / wl * 100
emp = share(L.switch == 1)
olf55 = share((L.leftlf == 1) & (L.A_AGE >= 55))
un = share(L.unemp == 1)
olfu = share((L.leftlf == 1) & (L.A_AGE < 55))
f = (L.leftlf == 1) & (L.A_AGE < 55)
fem = L.female == 1
baby = share(f & fem & (L.new_baby == 1))
u6 = share(f & fem & (L.new_baby == 0) & (L.child_u6 == 1))
k617 = share(f & fem & (L.new_baby == 0) & (L.child_u6 == 0) & (L.n_children > 0))
nok = share(f & fem & (L.n_children == 0) & (L.new_baby == 0) & (L.child_u6 == 0))
father = share(f & ~fem & (L.n_children > 0))
mennok = olfu - baby - u6 - k617 - nok - father
print(f"pooled 1997-2024: n_leavers={len(L)} | top {emp:.1f}/{olf55:.1f}/"
      f"{olfu:.1f}/{un:.1f} | split {baby:.1f}/{u6:.1f}/{k617:.1f}/{nok:.1f}/"
      f"{father:.1f}/{mennok:.1f}")

fig, ax = plt.subplots(figsize=(9.6, 4.6))
TAGS = {"Employed": ("Switchers", "#3A6BA8"),
        "Out of the labor force, <55": ("Early exits", "#B8922F"),
        "Out of the labor force, 55+": ("Retirees", "#7E99BD")}
Y1, Y0, H = 1.72, 0.80, 0.34
top2 = [("Employed", emp, SBLUE, "white"),
        ("Out of the labor force, <55", olfu, SGOLD, INK),
        ("Out of the labor force, 55+", olf55, LIGHT, INK),
        ("Unemployed", un, GRAYD, "white")]
x = 0
x_yl0 = x_yl1 = None
for lab, v, c, tc in top2:
    ax.barh([Y1], [v], left=x, color=c, height=H)
    ax.text(x + v / 2, Y1, f"{v:.0f}", ha="center", va="center", color=tc,
            fontsize=11, fontweight="bold")
    yl = Y1 + H / 2 + (0.10 if lab != "Unemployed" else 0.24)
    ax.text(x + v / 2, yl, lab, ha="center", va="bottom", fontsize=9.3,
            color=INK, fontweight="bold")
    if lab in TAGS:
        tg, tc = TAGS[lab]
        ax.text(x + v / 2, Y1 + H / 2 + 0.42, tg, ha="center",
                va="bottom", fontsize=10, color=tc, fontweight="bold",
                style="italic")
    if "<55" in lab:
        x_yl0, x_yl1 = x, x + v
    x += v
# pinks for the women's groups, blues for the men's
C1, C2, C3, C4 = "#CC6F63", "#DC948A", "#EBB9B0", "#F7DAD4"
M1, M2 = "#7095C2", "#B9CDE8"
bot2 = [("Baby born\nthat year", baby, C1, "white"),
        ("Youngest\nunder 6", u6, C2, INK),
        ("Youngest\n6\u201317", k617, C3, INK),
        ("Women, no own\nchild at home", nok, C4, INK),
        ("Fathers", father, M1, "white"),
        ("Men, no own\nchild at home", mennok, M2, INK)]
sc = 100.0 / olfu
x = 0
lvl = 0
for lab, v, c, tc in bot2:
    w = v * sc
    ax.barh([Y0], [w], left=x, color=c, height=H)
    ax.text(x + w / 2, Y0, f"{v * sc:.0f}%", ha="center", va="center",
            color=tc, fontsize=10, fontweight="bold")
    yl = Y0 - H / 2 - 0.14
    ax.text(x + w / 2, yl, lab, ha="center", va="top", fontsize=9.0,
            color=INK, fontweight="bold")
    lvl += 1
    x += w
ax.plot([x_yl0, 0], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=0.8)
ax.plot([x_yl1, 100], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=0.8)
ax.text(-1.2, Y1, "Of every 100\nleavers", ha="right", va="center",
        fontsize=9.6, color=INK)
ax.text(-1.2, Y0, "Who leaves the labor\nforce before 55", ha="right",
        va="center", fontsize=9.6, color=INK)
mb = baby + u6 + k617
xb = mb * sc
ax.text(xb / 2, Y0 + H / 2 + 0.10, "Mothers, child at home", ha="center",
        va="bottom", fontsize=9.3, color=C1, fontweight="bold")
yb = Y0 - H / 2 - 0.80
ax.plot([0, 0, xb, xb], [yb + 0.05, yb, yb, yb + 0.05], color=INK, lw=1.1)
ax.text(xb / 2, yb - 0.07,
        f"{mb * sc:.0f}% of them are mothers with a child at home "
        f"({mb:.0f} of the {olfu:.0f} of every 100 leavers)",
        ha="center", va="top", fontsize=9.4, color=INK, fontweight="bold")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.75, 2.95)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/flow_olf55_pooled.pdf")
fig.savefig(f"{OUT}/flow_olf55_pooled.png", dpi=200)
print("saved flow_olf55_pooled")
