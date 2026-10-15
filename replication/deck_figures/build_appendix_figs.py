"""Visual appendix figures: US mover rate 1948-2023 (Census A-1), linkage
rates teachers vs other graduates, the NCES TFS wave timeline with its
gaps, and the narrow-vs-full teacher-code series. Also rebuilds the
unified flow in the cascade style and the defs6 chart with a visible
benchmark. Run from the repo root."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["EB Garamond", "STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})

OUT = "report/figures_deck"
NAVY, BURG, INK, MUT = "#1F3864", "#7B2530", "#1A1A1A", "#6B7480"
BLUE, GOLD, LIGHT, GRAYD = "#2A5DB0", "#D9A441", "#AEC3DE", "#6E6E6E"
CORAL, SUBTLE = "#C4534B", "#C9CFD6"

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.pdf")
    fig.savefig(f"{OUT}/{name}.png", dpi=190)
    plt.close(fig)
    print("saved", name)

# ================= 1. US mover rate, 1948-2023 =================
import openpyxl
wb = openpyxl.load_workbook("data/raw/census_mobility_a1.xlsx", data_only=True)
ws = wb[wb.sheetnames[0]]
rows = []
for r in ws.iter_rows(min_row=9, max_col=4):
    y, tot, same, mov = [c.value for c in r][:4]
    if y is None or not isinstance(tot, (int, float)):
        continue
    ys = str(y)
    if "2010 controls" in ys:
        continue
    try:
        yr = int(ys[:4])
    except ValueError:
        continue
    rows.append((yr, 100 * mov / tot))
mig = pd.DataFrame(rows, columns=["year", "rate"]).drop_duplicates("year")
mig = mig.sort_values("year").reset_index(drop=True)
mig = mig[mig.year >= 1981].reset_index(drop=True)
fig, ax = plt.subplots(figsize=(11.4, 5.2))
ax.bar(mig.year, mig.rate, width=0.82, color=NAVY)
ax.bar(mig.year.iloc[-1], mig.rate.iloc[-1], width=0.82, color=BURG)
ax.annotate(f"2023\n{mig.rate.iloc[-1]:.1f}%", (2023, mig.rate.iloc[-1] + 0.4),
            ha="center", va="bottom", fontsize=12, fontweight="bold",
            color=BURG)
hi = mig.loc[mig.rate.idxmax()]
ax.annotate(f"{hi.rate:.0f}% in {int(hi.year)}", (hi.year + 1.5, hi.rate + 0.4),
            ha="left", fontsize=11, color=MUT)
ax.set_ylim(0, 24)
ax.set_xlim(1979.8, 2025.2)
ax.set_ylabel("share who changed residence in the year, percent",
              fontsize=11.5, color=INK)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(labelsize=11)
fig.tight_layout()
save(fig, "migration_rate")

# ================= 2. linkage rates, teachers vs other graduates ======
lk = pd.read_csv("outputs/linkage_rates_by_group.csv")
t = lk[lk.group.str.contains("teachers")].set_index("year").linked_w * 100
g = lk[lk.group.str.contains("other college")].set_index("year").linked_w * 100
fig, ax = plt.subplots(figsize=(11.4, 5.2))
ax.plot(t.index, t.values, color=NAVY, lw=2.4)
ax.plot(g.index, g.values, color=MUT, lw=1.8, ls=(0, (4, 2)))
ax.annotate(f"Teachers   {t.iloc[-1]:.0f}%", (t.index[-1] + 0.3, t.iloc[-1]),
            fontsize=12.5, color=NAVY, va="center", fontweight="bold")
ax.annotate(f"Other graduates   {g.iloc[-1]:.0f}%",
            (g.index[-1] + 0.3, g.iloc[-1] - 1.5), fontsize=12.5, color=MUT,
            va="center", fontweight="bold")
ax.set_xlim(2004.5, 2029)
ax.set_ylim(55, 90)
ax.set_ylabel("share linked to the next year's interviews, percent",
              fontsize=11.5, color=INK)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(labelsize=11)
fig.tight_layout()
save(fig, "linkage_series")

# ================= 3. the NCES TFS waves and their gaps ===============
WAVES = [(1989, 5.6), (1992, 5.1), (1995, 6.6), (2001, 7.4),
         (2005, 8.4), (2009, 8.0), (2013, 7.7), (2022, 8.0)]
wy = [w[0] for w in WAVES]
wv = [w[1] for w in WAVES]
fig, ax = plt.subplots(figsize=(11.6, 5.0))
ax.plot(wy, wv, color=SUBTLE, lw=1.2, ls=(0, (3, 3)), zorder=1)
ax.plot(wy, wv, "o", ms=10, mfc=NAVY, mec="white", mew=1.4, zorder=3)
for x, v in WAVES:
    ax.annotate(f"{v}", (x, v), xytext=(0, 12), textcoords="offset points",
                ha="center", fontsize=11.5, fontweight="bold", color=NAVY)
for (x0, _), (x1, _) in zip(WAVES[:-1], WAVES[1:]):
    gap = x1 - x0
    col = BURG if gap >= 6 else MUT
    ax.annotate(f"{gap} yrs", ((x0 + x1) / 2, 3.1), ha="center",
                fontsize=10.5 if gap >= 6 else 9.5, color=col,
                fontweight="bold" if gap >= 6 else "normal")
    ax.annotate("", xy=(x1 - 0.35, 2.6), xytext=(x0 + 0.35, 2.6),
                arrowprops=dict(arrowstyle="<->", color=col, lw=1.0))
ax.set_xlim(1986.5, 2025.5)
ax.set_ylim(1.5, 10.5)
ax.set_xticks(wy)
ax.set_xticklabels([f"{y-1}–{str(y)[2:]}" for y in wy], fontsize=10)
ax.set_ylabel("public school teachers leaving, percent", fontsize=11.5,
              color=INK)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "tfs_waves")

# ================= 4. narrow vs full teacher codes ====================
M = pd.read_parquet("data/processed/asec_master.parquet",
                    columns=["asec_year", "cal_year", "OCCUP", "PEIOOCC",
                             "A_LFSR", "WGT", "ba_plus", "A_AGE"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
M = M[(M.ba_plus == 1) & (M.A_AGE >= 18) & M.WGT.notna()]
def sets(ay, narrow):
    if ay <= 2002:
        return {155, 156, 157} if narrow else {155, 156, 157, 158, 159}
    core = {2300, 2310, 2320}
    if narrow:
        return core
    return core | {2330} | ({2340} if ay <= 2019 else {2360})
emp = M.A_LFSR.isin([1, 2])
out = {}
for narrow in (False, True):
    M["t"] = False
    M["now"] = False
    for ay, gg in M.groupby("asec_year"):
        s = sets(int(ay), narrow)
        M.loc[gg.index, "t"] = gg.OCCUP.isin(s)
        M.loc[gg.index, "now"] = gg.PEIOOCC.isin(s)
    M["lv"] = ((emp & ~M.now) | ~emp).astype(float)
    ser = (M[M.t].groupby("cal_year")
           .apply(lambda g: 100 * np.average(g.lv, weights=g.WGT)))
    out["narrow" if narrow else "full"] = ser
    pool = M[M.t]
    out[("pool_narrow" if narrow else "pool_full")] = \
        100 * np.average(pool.lv, weights=pool.WGT)
fig, ax = plt.subplots(figsize=(11.4, 5.2))
f = out["full"]; nrw = out["narrow"]
ax.plot(f.index, f.values, color=NAVY, lw=2.4)
ax.plot(nrw.index, nrw.values, color=BURG, lw=1.6, ls=(0, (4, 2)))
ax.annotate(f"All five codes    pooled {out['pool_full']:.2f}",
            (f.index[-1] + 0.4, f.iloc[-1] + 0.3), fontsize=12, color=NAVY,
            fontweight="bold", va="center")
ax.annotate(f"Core three codes    pooled {out['pool_narrow']:.2f}",
            (nrw.index[-1] + 0.4, nrw.iloc[-1] - 0.5), fontsize=12,
            color=BURG, fontweight="bold", va="center")
for yr in (2002.5, 2019.5):
    ax.axvline(yr, color=SUBTLE, lw=1.0)
ax.annotate("2003 reclassification", (2002.5, 11.9), fontsize=9.5,
            color=MUT, ha="center")
ax.annotate("2020 reclassification", (2019.5, 11.9), fontsize=9.5,
            color=MUT, ha="center")
ax.set_xlim(1996.5, 2033)
ax.set_ylim(0, 12.8)
ax.set_xticks(range(1997, 2025, 3))
ax.set_ylabel("teachers leaving per year, percent", fontsize=11.5, color=INK)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(labelsize=10.5)
fig.tight_layout()
save(fig, "codes_narrow")

# ================= 5. unified flow, cascade style =====================
F = pd.read_csv("outputs/flow_unified.csv", index_col=0).iloc[:, 0]
fig, ax = plt.subplots(figsize=(9.6, 4.9))
Y1, Y0, H = 1.72, 0.55, 0.34
top = [("Employed", F.another_job, BLUE, "white"),
       ("Out of the labor force, 55+", F.olf_55plus, LIGHT, INK),
       ("Out of the labor force, <55", F.olf_u55, GOLD, INK),
       ("Unemployed", F.unemployed, GRAYD, "white")]
x = 0
x_yl0 = x_yl1 = None
for lab, v, c, tc in top:
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
bot = [("Baby born\nthat year", F.u55_mother_baby, C1, "white"),
       ("Youngest\nunder 6", F.u55_mother_u6, C2, "white"),
       ("Youngest\n6–17", F.u55_mother_617, C3, INK),
       ("Women, no own\nchild at home", F.u55_woman_nokid, LIGHT, INK),
       ("Fathers", F.u55_father, "#5B7BA6", "white"),
       ("Men, no own\nchild at home", F.u55_man_nokid, GRAYD, "white")]
sc = 100.0 / F.olf_u55
x = 0
for lab, v, c, tc in bot:
    w = v * sc
    ax.barh([Y0], [w], left=x, color=c, height=H)
    ax.text(x + w / 2, Y0, f"{v:.0f}", ha="center", va="center", color=tc,
            fontsize=10.5, fontweight="bold")
    ax.text(x + w / 2, Y0 - H / 2 - 0.10, lab, ha="center", va="top",
            fontsize=8.6, color=INK)
    x += w
ax.plot([x_yl0, 0], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=1.0)
ax.plot([x_yl1, 100], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=1.0)
ax.text(-1.2, Y1, "Of every 100\nleavers", ha="right", va="center",
        fontsize=9.6, color=INK)
ax.text(-1.2, Y0, "Who leaves the labor\nforce before 55", ha="right",
        va="center", fontsize=9.6, color=INK)
mb = F.u55_mother_baby + F.u55_mother_u6 + F.u55_mother_617
xb = mb * sc
ax.text(xb / 2, Y0 + H / 2 + 0.10, "Mothers, child at home", ha="center",
        va="bottom", fontsize=8.8, color=CORAL, fontweight="bold")
yb = Y0 - H / 2 - 0.62
ax.plot([0, 0, xb, xb], [yb + 0.05, yb, yb, yb + 0.05], color=INK, lw=1.1)
ax.text(xb / 2, yb - 0.07,
        f"More than half are mothers with a child at home "
        f"({mb:.0f} of the {F.olf_u55:.0f})", ha="center", va="top",
        fontsize=9.4, color=INK, fontweight="bold")
ax.text(100, yb - 0.07,
        f"about {F.u55_inschool_share:.0f}% of the group\nis enrolled in school",
        ha="right", va="top", fontsize=9.0, color=INK, style="italic")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.75, 2.35)
ax.axis("off")
fig.tight_layout()
save(fig, "flow_unified")

# ================= 6. defs6 with a visible benchmark ==================
L = pd.read_csv("outputs/definitions_ladder.csv")
L = L[L.base_year <= 2024]
REDS = ["#C79AA0", "#A2606A", "#8A4450", "#7B2530"]
fig, ax = plt.subplots(figsize=(12.4, 6.4))
series = [("single", REDS[0], "-", 1.7, "Single   17.5"),
          ("month_pairs", MUT, (0, (4, 2)), 1.7, "Month pairs   15.4"),
          ("pair", REDS[1], "-", 1.7, "Pair   13.4"),
          ("triple", REDS[2], "-", 1.7, "Triple   11.7"),
          ("strict", REDS[3], "-", 2.5, "Strict   10.5")]
for col, c, ls, lw, lab in series:
    ax.plot(L.base_year, L[col], color=c, ls=ls, lw=lw)
    ax.annotate(lab, (2024.3, L[col].iloc[-1]), fontsize=12.5, color=c,
                va="center", fontweight="bold")
# annual recall runs from 1997 (the March supplement needs no panel) with
# its 95 percent confidence band
P = pd.read_csv("outputs/p_series.csv").sort_values("cal_year")
P = P[P.cal_year <= 2024]
ax.fill_between(P.cal_year, P.leaver_ba - 1.96 * P.se_ba,
                P.leaver_ba + 1.96 * P.se_ba, color=NAVY, alpha=0.10, lw=0)
ax.plot(P.cal_year, P.leaver_ba, color=NAVY, lw=2.7)
ax.annotate("Annual recall   8.6", (2024.3, P.leaver_ba.iloc[-1]),
            fontsize=12.5, color=NAVY, va="center", fontweight="bold")
ax.axvline(2004.9, ls=(0, (2, 2)), color=MUT, lw=1.1, zorder=1)
ax.annotate("linkable household\nidentifiers begin (2005)",
            (2004.5, 22.8), fontsize=13.5, color=NAVY, ha="right",
            va="top", fontweight="bold")
# waves at the survey year, except 2000-01, placed at its exit year
# (2000) because the 2001 point of the recall series carries the
# recession spike the wave predates
NC_Y, NC_V = [2000, 2005, 2009, 2013, 2022], [7.4, 8.4, 8.0, 7.7, 8.0]
ax.plot(NC_Y, NC_V, ls="none", marker="D", ms=10, mfc="black",
        mec="white", mew=1.6, zorder=6)
ax.annotate("NCES follow-up survey\n(official benchmark)   8.0",
            (2024.3, 6.4), fontsize=12.5, color="black", va="center",
            fontweight="bold")
for x, v in zip(NC_Y, NC_V):
    ax.annotate(f"{v}", (x, v), xytext=(0, -16), textcoords="offset points",
                ha="center", fontsize=10.5, color="black", fontweight="bold")
ax.set_xlim(1996.5, 2031.5)
ax.set_ylim(0, 24)
ax.set_xticks(range(1997, 2025, 3))
ax.set_ylabel("teachers leaving per year, percent", fontsize=12.5, color=INK)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(labelsize=11.5)
fig.tight_layout()
save(fig, "defs6")
print("done")
