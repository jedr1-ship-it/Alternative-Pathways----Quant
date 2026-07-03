"""
Population story for the brief:
  - table_population.tex : funnel from CPS adults to the analytic sample
  - fig0_design.pdf      : CPS 4-8-4 design — who we can follow, for how long
  - fig7_stock.pdf       : estimated number of school teachers per year
  - fig8_by_level.pdf    : teachers by teaching level per year
  - fig9_flows.pdf       : teachers entering vs leaving per year (linked pairs)
All population estimates use CPS final person weights (PWSSWGT).
"""
import glob
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

BLUE, GREEN, GOLD, CORAL = "#2a78d6", "#1baf7a", "#eda100", "#e34948"
GRAY = "#8a8f98"
INK, SUBTLE, SURFACE = "#1a2430", "#5a6572", "#fcfcfb"
NAVY = "#12355b"
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK, "axes.edgecolor": "#d8dbe0", "axes.labelcolor": SUBTLE,
    "xtick.color": SUBTLE, "ytick.color": SUBTLE,
    "axes.grid": True, "grid.color": "#e9ebee", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.size": 10,
})

TEACHER_OCC = {2300, 2310, 2320, 2330}
LEVELS = {2300: "Preschool / kindergarten", 2310: "Elementary / middle",
          2320: "Secondary", 2330: "Special education"}
LEVEL_COLOR = {"Elementary / middle": BLUE, "Secondary": GREEN,
               "Preschool / kindergarten": GOLD, "Special education": CORAL}

# ---------- sweep the monthly cache: funnel + stocks ----------
# counts are per-month averages: persons in the sample and, via weights,
# the population they represent
funnel = {k: [0, 0.0] for k in
          ["adults", "employed", "teachers", "teachers_ba"]}
n_months = 0
wstock = []          # per (year, month): weighted teachers by level
for f in sorted(glob.glob("data/interim/cps_??????.parquet")):
    d = pd.read_parquet(f, columns=["PEMLR", "PTIO1OCD", "PEEDUCA", "HRMIS",
                                    "HRYEAR4", "HRMONTH", "PWSSWGT"])
    n_months += 1
    e = d[d["PEMLR"].isin([1, 2])]
    t = e[e["PTIO1OCD"].isin(TEACHER_OCC)]
    tb = t[t["PEEDUCA"] >= 43]
    for k, dd in [("adults", d), ("employed", e), ("teachers", t),
                  ("teachers_ba", tb)]:
        funnel[k][0] += len(dd)
        funnel[k][1] += dd["PWSSWGT"].sum()
    g = tb.groupby("PTIO1OCD")["PWSSWGT"].sum()
    wstock.append({"year": int(d["HRYEAR4"].iat[0]),
                   "month": int(d["HRMONTH"].iat[0]),
                   **{LEVELS[k]: g.get(k, 0.0) for k in LEVELS},
                   "total": tb["PWSSWGT"].sum()})
stock = pd.DataFrame(wstock)
yr = stock.groupby("year").mean(numeric_only=True).drop(columns="month") / 1e6
yr.round(3).to_csv("outputs/teacher_stock_by_year.csv")

panel = pd.read_csv("data/processed/cps_teacher_panel.csv",
                    usecols=["HRMIS_0", "PWSSWGT_0"])
n_linked = len(panel)
n_followup = int((panel["HRMIS_0"] <= 3).sum())

# ---------- funnel table: persons + population represented ----------
def month_avg(k):
    n, w = funnel[k]
    return n / n_months, w / n_months / 1e6

rows = []
for lab, k in [("Adults interviewed in an average month", "adults"),
               ("\\quad employed", "employed"),
               ("\\quad\\quad school teachers (occ. 2300--2330)", "teachers"),
               ("\\quad\\quad\\quad with bachelor's degree or higher",
                "teachers_ba")]:
    n, w = month_avg(k)
    rows.append((lab, f"{n:,.0f}", f"{w:.1f}M"))
rows.append(("Teachers linked to their interview 12 months later "
             "(unique persons, 20 waves)", f"{n_linked:,}",
             "the same 4.6M"))
rows.append(("\\quad with re-interviews after $t{+}12$: \\textbf{main sample}",
             f"{n_followup:,}", "the same 4.6M"))
with open("report/table_population.tex", "w") as fh:
    fh.write("\\begin{tabular}{lrr}\n\\toprule\n"
             " & Persons & Population represented \\\\\n\\midrule\n")
    for lab, n, w in rows:
        fh.write(f"{lab} & {n} & {w} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# ---------- fig0: the 4-8-4 design ----------
fig, ax = plt.subplots(figsize=(9.2, 2.6))
months = np.arange(1, 17)
status = ["in"] * 4 + ["out"] * 8 + ["in"] * 4
for mth, st in zip(months, status):
    c = BLUE if st == "in" else "#e3e6ea"
    ax.add_patch(plt.Rectangle((mth - 0.44, 0), 0.88, 0.8, color=c, zorder=3))
    ax.text(mth, 0.4, str(mth), ha="center", va="center", fontsize=9,
            color="white" if st == "in" else SUBTLE, fontweight="bold",
            zorder=4)
ax.annotate("", xy=(13, 1.28), xytext=(1, 1.28),
            arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.8))
ax.text(7, 1.42, "12-month link: teacher at t $\\rightarrow$ still teaching?",
        ha="center", fontsize=9.5, color=INK, fontweight="bold")
ax.annotate("", xy=(16.4, 0.98), xytext=(13.6, 0.98),
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.8))
ax.text(15.1, 1.10, "return window", ha="center", fontsize=9, color=INK)
ax.text(2.5, -0.32, "interviewed\n(4 months)", ha="center", fontsize=8.5,
        color=SUBTLE)
ax.text(8.5, -0.32, "not interviewed (8 months)", ha="center", fontsize=8.5,
        color=SUBTLE)
ax.text(14.5, -0.32, "interviewed again\n(4 months)", ha="center",
        fontsize=8.5, color=SUBTLE)
ax.set_xlim(0.3, 17.6)
ax.set_ylim(-0.75, 1.65)
ax.axis("off")
fig.tight_layout()
fig.savefig("report/figures/fig0_design.pdf")
plt.close(fig)

# ---------- fig7: teacher stock ----------
fig, ax = plt.subplots(figsize=(6.6, 3.0))
ax.plot(yr.index, yr["total"], color=BLUE, lw=2, solid_capstyle="round")
ax.scatter([yr.index[-1]], [yr["total"].iloc[-1]], s=42, color=BLUE,
           zorder=4, edgecolor=SURFACE, linewidth=2)
ax.text(yr.index[-1] + 0.4, yr["total"].iloc[-1],
        f"{yr['total'].iloc[-1]:.1f}M", va="center", fontsize=10,
        fontweight="bold", color=INK)
ax.set_ylim(0, None)
ax.set_xticks([2005, 2010, 2015, 2020, 2025])
ax.set_xlim(2004.5, 2027)
ax.set_ylabel("Teachers, millions")
ax.tick_params(length=0)
fig.tight_layout()
fig.savefig("report/figures/fig7_stock.pdf")
plt.close(fig)

# ---------- fig8: by teaching level ----------
fig, ax = plt.subplots(figsize=(6.9, 3.4))
order = ["Elementary / middle", "Secondary", "Preschool / kindergarten",
         "Special education"]
for lev in order:
    ax.plot(yr.index, yr[lev], color=LEVEL_COLOR[lev], lw=2,
            solid_capstyle="round")
    ax.text(yr.index[-1] + 0.4, yr[lev].iloc[-1], f"{yr[lev].iloc[-1]:.2f}M",
            va="center", fontsize=9, color=INK, fontweight="bold")
handles = [plt.Line2D([], [], color=LEVEL_COLOR[l], lw=2) for l in order]
ax.legend(handles, order, loc="upper left", frameon=False, fontsize=9,
          ncol=2)
ax.set_ylim(0, None)
ax.set_xticks([2005, 2010, 2015, 2020, 2025])
ax.set_xlim(2004.5, 2028)
ax.set_ylabel("Teachers, millions")
ax.tick_params(length=0)
fig.tight_layout()
fig.savefig("report/figures/fig8_by_level.pdf")
plt.close(fig)

# ---------- fig9: entering vs leaving ----------
fl = pd.read_csv("data/processed/cps_flows.csv")
fl["entry_rate"] = fl["entrants_w"] / fl["teachers_t1_w"] * 100
fl["exit_rate"] = fl["leavers_w"] / fl["teachers_t_w"] * 100
fl.round(3).to_csv("outputs/flows_by_year.csv", index=False)
fig, ax = plt.subplots(figsize=(6.9, 3.2))
ax.plot(fl.base_year, fl.entry_rate, color=GREEN, lw=2,
        solid_capstyle="round")
ax.plot(fl.base_year, fl.exit_rate, color=CORAL, lw=2,
        solid_capstyle="round")
for col, c in [("entry_rate", GREEN), ("exit_rate", CORAL)]:
    ax.scatter([fl.base_year.iloc[-1]], [fl[col].iloc[-1]], s=42, color=c,
               zorder=4, edgecolor=SURFACE, linewidth=2)
    ax.text(fl.base_year.iloc[-1] + 0.4, fl[col].iloc[-1],
            f"{fl[col].iloc[-1]:.0f}%", va="center", fontsize=9.5,
            color=INK, fontweight="bold")
handles = [plt.Line2D([], [], color=c, lw=2) for c in (GREEN, CORAL)]
ax.legend(handles, ["Entering teaching (share of year-$t{+}1$ teachers)",
                    "Leaving teaching (share of year-$t$ teachers)"],
          loc="lower left", frameon=False, fontsize=8.5)
ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
ax.set_ylim(0, None)
ax.set_xticks([2005, 2010, 2015, 2020, 2024])
ax.set_xlim(2004.5, 2027)
ax.set_ylabel("% per year")
ax.tick_params(length=0)
fig.tight_layout()
fig.savefig("report/figures/fig9_flows.pdf")
plt.close(fig)

# ---------- fig12: portrait of the teaching workforce, 2021-2025 ----------
# teachers vs other college-educated employed
CHLD_U6 = {1, 2, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15}
NEs = {9, 23, 25, 33, 44, 50, 34, 36, 42}
MWs = {17, 18, 26, 39, 55, 19, 20, 27, 29, 31, 38, 46}
SOs = {10, 11, 12, 13, 24, 37, 45, 51, 54, 1, 21, 28, 47, 5, 22, 40, 48}
parts = []
for f in sorted(glob.glob("data/interim/cps_202[1-5]??.parquet")):
    d = pd.read_parquet(f)
    e = d[d["PEMLR"].isin([1, 2]) & (d["PEEDUCA"] >= 43)].copy()
    e["tch"] = e["PTIO1OCD"].isin(TEACHER_OCC)
    parts.append(e)
P = pd.concat(parts, ignore_index=True)
P["female"] = (P["PESEX"] == 2)
P["ma_plus"] = P["PEEDUCA"] >= 44
P["public"] = P["PEIO1COW"].isin([1, 2, 3])
P["parttime"] = P["PEHRUSL1"].between(1, 34)
P["married"] = P["PEMARITL"].isin([1, 2])
P["child_u6"] = P["PRCHLD"].isin(CHLD_U6)
P["region"] = np.select(
    [P["GESTFIPS"].isin(NEs), P["GESTFIPS"].isin(MWs), P["GESTFIPS"].isin(SOs)],
    ["Northeast", "Midwest", "South"], default="West")


def wsh(g, col):
    return np.average(g[col], weights=g["PWSSWGT"]) * 100


T, O = P[P["tch"]], P[~P["tch"]]
fig, axes = plt.subplots(1, 3, figsize=(9.8, 3.3),
                         gridspec_kw={"width_ratios": [3, 3.4, 2.6]})

# (a) age distribution
ax = axes[0]
bins = np.arange(20, 75, 5)
for g, c in [(O, GRAY), (T, BLUE)]:
    h, _ = np.histogram(g["PRTAGE"], bins=bins, weights=g["PWSSWGT"])
    ax.plot(bins[:-1] + 2.5, h / h.sum() * 100, color=c, lw=2,
            solid_capstyle="round")
ax.set_title("Age distribution, %", loc="left", fontsize=10, color=NAVY,
             fontweight="bold", pad=8)
ax.set_ylim(0, None)
ax.set_xlabel("Age")
ax.tick_params(length=0)

# (b) composition dumbbells
ax = axes[1]
traits = [("Female", "female"), ("Master's degree+", "ma_plus"),
          ("Public sector", "public"), ("Married", "married"),
          ("Child under 6", "child_u6"), ("Part-time", "parttime")]
yy = np.arange(len(traits))[::-1]
for yi, (lab, v) in zip(yy, traits):
    a, b = wsh(O, v), wsh(T, v)
    ax.plot([a, b], [yi, yi], color="#d8dbe0", lw=2, zorder=2)
    ax.scatter([a], [yi], s=54, color=GRAY, zorder=3, edgecolor=SURFACE,
               linewidth=2)
    ax.scatter([b], [yi], s=54, color=BLUE, zorder=3, edgecolor=SURFACE,
               linewidth=2)
    off = 3 if b >= a else -3
    ax.text(b + off, yi, f"{b:.0f}%", va="center",
            ha="left" if b >= a else "right", fontsize=9, color=INK,
            fontweight="bold")
ax.set_yticks(yy, [t for t, _ in traits], fontsize=9.5)
ax.set_xlim(-2, 108)
ax.set_title("Share with the trait, %", loc="left", fontsize=10,
             color=NAVY, fontweight="bold", pad=8)
ax.tick_params(length=0)
ax.yaxis.grid(False)

# (c) regional distribution
ax = axes[2]
regs = ["Northeast", "Midwest", "South", "West"]
yy = np.arange(len(regs))[::-1]
for yi, r in zip(yy, regs):
    a = np.average(O["region"] == r, weights=O["PWSSWGT"]) * 100
    b = np.average(T["region"] == r, weights=T["PWSSWGT"]) * 100
    ax.plot([a, b], [yi, yi], color="#d8dbe0", lw=2, zorder=2)
    ax.scatter([a], [yi], s=54, color=GRAY, zorder=3, edgecolor=SURFACE,
               linewidth=2)
    ax.scatter([b], [yi], s=54, color=BLUE, zorder=3, edgecolor=SURFACE,
               linewidth=2)
    ax.text(max(a, b) + 1.6, yi, f"{b:.0f}%", va="center", fontsize=9,
            color=INK, fontweight="bold")
ax.set_yticks(yy, regs, fontsize=9.5)
ax.set_xlim(0, 48)
ax.set_title("Region of residence, %", loc="left", fontsize=10,
             color=NAVY, fontweight="bold", pad=8)
ax.tick_params(length=0)
ax.yaxis.grid(False)

handles = [plt.Line2D([], [], color=c, lw=2) for c in (BLUE, GRAY)]
axes[0].legend(handles, ["School teachers", "Other college-educated"],
               loc="lower center", frameon=False, fontsize=8)
fig.tight_layout(w_pad=2.0)
fig.savefig("report/figures/fig12_portrait.pdf")
plt.close(fig)
print("portrait: teachers female", round(wsh(T, 'female')),
      "% vs others", round(wsh(O, 'female')), "%")

print("funnel:", funnel, "| linked:", n_linked, "| follow-up:", n_followup)
print(yr[["total"]].round(2).tail(3).to_string())
print(fl[["base_year", "entry_rate", "exit_rate"]].round(1).tail(3).to_string(index=False))
print("saved table_population.tex, fig0, fig7, fig8, fig9")
