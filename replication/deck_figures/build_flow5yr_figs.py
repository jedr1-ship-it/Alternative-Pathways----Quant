"""The two old flow figures (fig07 destinations, fig09 under-55 cascade)
exactly as they were, recomputed on the five-year window (calendar
2020-2024, ASEC 2021-2025) from the extended file, so every number
matches outputs/flow_unified.csv. Same geometry, palette and typography
as the originals; the only content change in the cascade is the Men
segment split into Fathers and Men with no own child.
Also writes the in-school shares by subgroup of the under-55 OLF group.
Run from the repo root after replication/build_asec_ext.py."""
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
LIGHT, GRAYD = "#AEC3DE", "#6E6E6E"

# ---------- derivations, identical to replication/analyze_ext.py ----------
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
print("teachers 2020-24:", len(T), "| leavers:", len(L))

def share(m):
    return L.loc[m, "MARSUPWT"].sum() / wl * 100

emp = share(L.switch)
olf55 = share(L.leftlf & (L.A_AGE >= 55))
olfu = share(L.leftlf & (L.A_AGE < 55))
un = share(L.unemp)
print("top:", round(emp, 1), round(olf55, 1), round(olfu, 1), round(un, 1))

# ================= fig07 as before: what the employed are doing ========
CORE = {2300, 2310, 2320, 2330}
cs = CORE | {2360}
o = L["PEIOOCC"]
sw = L["switch"]
edu_m = (o.between(2200, 2555) & ~o.isin(cs)) | (o == 230)
care_m = o.between(2000, 2025) | (o == 4600)
prof_m = ((o.between(10, 960) & (o != 230)) | o.between(1000, 1965)
          | o.between(2600, 2960) | o.between(3000, 3550))
edu_job = share(sw & edu_m)
care = share(sw & care_m)
otherprof = share(sw & prof_m)
salesetc = emp - edu_job - care - otherprof
print("bot07:", round(edu_job, 1), round(care, 1), round(otherprof, 1),
      round(salesetc, 1))

fig, ax = plt.subplots(figsize=(9.6, 4.6))
Y1, Y0, H = 1.72, 0.55, 0.34
top = [("Employed", emp, BLUE),
       ("Out of the labor force, 55+", olf55, LIGHT),
       ("Out of the labor force, <55", olfu, GOLD),
       ("Unemployed", un, "#6E6E6E")]
x = 0
for lab, v, c in top:
    ax.barh([Y1], [v], left=x, color=c, height=H)
    txtc = "white" if c in (BLUE, "#6E6E6E") else INK
    ax.text(x + v / 2, Y1, f"{v:.0f}", ha="center", va="center",
            color=txtc, fontsize=11, fontweight="bold")
    yl = Y1 + H / 2 + (0.10 if lab != "Unemployed" else 0.24)
    ax.text(x + v / 2, yl, lab, ha="center", va="bottom", fontsize=8.8,
            color=INK)
    x += v
bot = [("Education job", edu_job, BLUE),
       ("Care and\nchildren", care, CORAL),
       ("Other\nprofessional", otherprof, GREEN),
       ("Sales, office\nand manual", salesetc, GRAY)]
sc = 100.0 / emp
x = 0
for lab, v, c in bot:
    w = v * sc
    ax.barh([Y0], [w], left=x, color=c, height=H)
    ax.text(x + w / 2, Y0, f"{v * sc:.0f}%", ha="center", va="center",
            color="white", fontsize=10.5, fontweight="bold")
    ax.text(x + w / 2, Y0 - H / 2 - 0.10, lab, ha="center", va="top",
            fontsize=8.8, color=INK)
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
ax.set_ylim(-0.35, 2.35)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/flow_employed_5yr.pdf")
fig.savefig(f"{OUT}/flow_employed_5yr.png", dpi=200)
plt.close(fig)
print("saved flow_employed_5yr")

# ================= fig09 as before: the under-55 cascade ===============
f = L.leftlf & (L.A_AGE < 55)
baby = share(f & (L.female == 1) & L.baby)
u6 = share(f & (L.female == 1) & ~L.baby & L.kid_u6)
k617 = share(f & (L.female == 1) & ~L.kid_u6 & L.haskid)
nok = share(f & (L.female == 1) & ~L.haskid)
father = share(f & (L.female == 0) & L.haskid)
mennok = share(f & (L.female == 0) & ~L.haskid)
print("split09:", round(baby, 1), round(u6, 1), round(k617, 1),
      round(nok, 1), round(father, 1), round(mennok, 1))

fig, ax = plt.subplots(figsize=(9.6, 4.6))
top2 = [("Employed", emp, BLUE, "white"),
        ("Out of the labor force, 55+", olf55, LIGHT, INK),
        ("Out of the labor force, <55", olfu, GOLD, INK),
        ("Unemployed", un, GRAYD, "white")]
x = 0
x_yl0 = x_yl1 = None
for lab, v, c, tc in top2:
    ax.barh([Y1], [v], left=x, color=c, height=H)
    ax.text(x + v / 2, Y1, f"{v:.0f}", ha="center", va="center", color=tc,
            fontsize=11, fontweight="bold")
    yl = Y1 + H / 2 + (0.10 if lab != "Unemployed" else 0.24)
    ax.text(x + v / 2, yl, lab, ha="center", va="bottom", fontsize=8.8,
            color=INK)
    if "<55" in lab:
        x_yl0, x_yl1 = x, x + v
    x += v
C1, C2, C3 = CORAL, "#D3766F", "#E2A19B"
bot2 = [("Baby born\nthat year", baby, C1, "white"),
        ("Youngest\nunder 6", u6, C2, "white"),
        ("Youngest\n6–17", k617, C3, INK),
        ("Fathers", father, "#5B7BA6", "white"),
        ("Women, no own\nchild at home", nok, LIGHT, INK),
        ("Men, no own\nchild at home", mennok, GRAYD, "white")]
sc = 100.0 / olfu
x = 0
lvl = 0
for lab, v, c, tc in bot2:
    w = v * sc
    ax.barh([Y0], [w], left=x, color=c, height=H)
    ax.text(x + w / 2, Y0, f"{v * sc:.0f}%", ha="center", va="center",
            color=tc, fontsize=10, fontweight="bold")
    if lab != "Fathers":
        yl = Y0 - H / 2 - (0.10 if lvl % 2 == 0 else 0.42)
        ax.text(x + w / 2, yl, lab, ha="center", va="top", fontsize=8.4,
                color=INK)
    lvl += 1
    x += w
ax.plot([x_yl0, 0], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=1.0)
ax.plot([x_yl1, 100], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=1.0)
ax.text(-1.2, Y1, "Of every 100\nleavers", ha="right", va="center",
        fontsize=9.6, color=INK)
ax.text(-1.2, Y0, "Who leaves the labor\nforce before 55", ha="right",
        va="center", fontsize=9.6, color=INK)
mb = baby + u6 + k617
pb = mb + father
xm = mb * sc
xp = pb * sc
ax.text(xm / 2, Y0 + H / 2 + 0.10, "Mothers, child at home", ha="center",
        va="bottom", fontsize=8.8, color=CORAL, fontweight="bold")
ax.text(xm + (xp - xm) / 2, Y0 + H / 2 + 0.10, "Fathers", ha="center",
        va="bottom", fontsize=8.8, color="#5B7BA6", fontweight="bold")
yb = Y0 - H / 2 - 0.80
ax.plot([0, 0, xp, xp], [yb + 0.05, yb, yb, yb + 0.05], color=INK, lw=1.1)
ax.text(xp / 2, yb - 0.07,
        f"{pb * sc:.0f}% of them are parents with a child at home "
        f"({mb:.0f} mothers and {father:.0f} fathers, of the {olfu:.0f} "
        f"of every 100 leavers)",
        ha="center", va="top", fontsize=9.4, color=INK, fontweight="bold")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.80, 2.35)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{OUT}/flow_olf55_5yr.pdf")
fig.savefig(f"{OUT}/flow_olf55_5yr.png", dpi=200)
plt.close(fig)
print("saved flow_olf55_5yr")

# ================= who in the under-55 OLF group is studying ===========
U = L[f].copy()
U["insch"] = np.where(U.PRNLFSCH == 1, 1.0,
                      np.where(U.PRNLFSCH == 2, 0.0, np.nan))
rows = {}
for name, m in [("all under-55 OLF", pd.Series(True, index=U.index)),
                ("mothers (own child at home)", (U.female == 1) & U.haskid),
                ("women, no own child", (U.female == 1) & ~U.haskid),
                ("fathers", (U.female == 0) & U.haskid),
                ("men, no own child", (U.female == 0) & ~U.haskid)]:
    g = U[m & U.insch.notna()]
    rows[name] = {
        "in_school_pct": 100 * np.average(g.insch, weights=g.MARSUPWT)
        if len(g) else np.nan,
        "n": int(len(g))}
S = pd.DataFrame(rows).T
S.to_csv("outputs/olf55_inschool_by_group.csv")
print(S.round(1).to_string())
print("done")
