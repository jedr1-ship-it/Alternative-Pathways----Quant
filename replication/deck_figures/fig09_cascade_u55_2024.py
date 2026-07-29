import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from paperstyle import BLUE, CORAL, GOLD, INK, SUBTLE

OUT = "report/figures_deck"
LIGHT, GRAYD = "#AEC3DE", "#6E6E6E"

M = pd.read_parquet("data/processed/asec_master.parquet",
                    columns=["asec_year","teacher","ba_plus","A_AGE","WGT","leaver",
                             "leftlf","unemp","switch","female","new_baby","child_u6",
                             "n_children"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
M["cal_year"] = M["asec_year"] - 1
T = M[(M.teacher==1)&(M.ba_plus==1)&(M.A_AGE>=18)&M.WGT.notna()&M.leaver.notna()
      &(M.asec_year==2025)]
L = T[T.leaver==1]
wl = L["WGT"].sum()
def share(m): return L.loc[m,"WGT"].sum()/wl*100
emp = share(L.switch==1)
olf55 = share((L.leftlf==1)&(L.A_AGE>=55))
un = share(L.unemp==1)
Y = L[(L.leftlf==1)&(L.A_AGE<55)]
olfu = Y["WGT"].sum()/wl*100
f = (L.leftlf==1)&(L.A_AGE<55)&(L.female==1)
baby = share(f&(L.new_baby==1))
u6 = share(f&(L.new_baby==0)&(L.child_u6==1))
k617 = share(f&(L.new_baby==0)&(L.child_u6==0)&(L.n_children>0))
nok = share(f&(L.new_baby==0)&(L.child_u6==0)&(L.n_children==0))
men = olfu - baby - u6 - k617 - nok
print("top:", round(emp), round(olf55), round(olfu), round(un))
print("split:", round(baby,1), round(u6,1), round(k617,1), round(nok,1), round(men,1))

fig, ax = plt.subplots(figsize=(9.6, 4.6))
Y1, Y0, H = 1.72, 0.55, 0.34
top = [("Employed", emp, BLUE, "white"),
       ("Out of the labor force, 55+", olf55, LIGHT, INK),
       ("Out of the labor force, <55", olfu, GOLD, INK),
       ("Unemployed", un, GRAYD, "white")]
x = 0
x_yl0 = x_yl1 = None
for lab, v, c, tc in top:
    ax.barh([Y1],[v], left=x, color=c, height=H)
    ax.text(x+v/2, Y1, f"{v:.0f}", ha="center", va="center", color=tc,
            fontsize=11, fontweight="bold")
    yl = Y1 + H/2 + (0.10 if lab != "Unemployed" else 0.24)
    ax.text(x+v/2, yl, lab, ha="center", va="bottom", fontsize=8.8, color=INK)
    if "<55" in lab:
        x_yl0, x_yl1 = x, x+v
    x += v
C1, C2, C3 = CORAL, "#D3766F", "#E2A19B"
bot = [("Baby born\nthat year", baby, C1, "white"),
       ("Youngest\nunder 6", u6, C2, "white"),
       ("Youngest\n6–17", k617, C3, INK),
       ("Women, no own\nchild at home", nok, LIGHT, INK),
       ("Men", men, GRAYD, "white")]
sc = 100.0/olfu
x = 0
for lab, v, c, tc in bot:
    w = v*sc
    ax.barh([Y0],[w], left=x, color=c, height=H)
    ax.text(x+w/2, Y0, f"{v:.0f}", ha="center", va="center", color=tc,
            fontsize=10.5, fontweight="bold")
    ax.text(x+w/2, Y0-H/2-0.10, lab, ha="center", va="top", fontsize=8.8,
            color=INK)
    x += w
ax.plot([x_yl0, 0], [Y1-H/2, Y0+H/2], ls=":", color=SUBTLE, lw=1.0)
ax.plot([x_yl1, 100], [Y1-H/2, Y0+H/2], ls=":", color=SUBTLE, lw=1.0)
ax.text(-1.2, Y1, "Of every 100\nleavers", ha="right", va="center",
        fontsize=9.6, color=INK)
ax.text(-1.2, Y0, "Who leaves the labor\nforce before 55", ha="right",
        va="center", fontsize=9.6, color=INK)
mb = baby+u6+k617
xb = mb*sc
mid = xb/2
ax.text(mid+7, Y0+H/2+0.10, "Mothers, child at home", ha="center", va="bottom",
        fontsize=8.8, color=CORAL, fontweight="bold")
yb = Y0 - H/2 - 0.62
ax.plot([0,0,xb,xb],[yb+0.05,yb,yb,yb+0.05], color=INK, lw=1.1)
ax.text(xb/2, yb-0.07,
        f"Nearly half of them are mothers with a child at home "
        f"({mb:.0f} of the {olfu:.0f})", ha="center", va="top", fontsize=9.4,
        color=INK, fontweight="bold")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.55, 2.35)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/yellow_flow2024.pdf")
fig.savefig(f"{OUT}/yellow_flow2024.png", dpi=200)
print("saved")
