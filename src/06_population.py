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

from paperstyle import *

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
rows.append(("Linked 12 months later (unique persons, 20 waves)",
             f"{n_linked:,}", "the same 4.6M"))
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
ax.legend(handles, order, loc="upper center",
          bbox_to_anchor=(0.5, 1.16), ncols=2, frameon=False, fontsize=9)
ax.set_ylim(0, None)
ax.set_xticks([2005, 2010, 2015, 2020, 2025])
ax.set_xlim(2004.5, 2028)
ax.set_ylabel("Teachers, millions")
fig.tight_layout()
fig.savefig("report/figures/fig8_by_level.pdf", bbox_inches="tight")
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
ax.legend(handles, ["Entering teaching", "Leaving teaching"],
          loc="upper center", bbox_to_anchor=(0.5, 1.14), ncols=2,
          frameon=False, fontsize=9)
ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
ax.set_ylim(0, None)
ax.set_xticks([2005, 2010, 2015, 2020, 2024])
ax.set_xlim(2004.5, 2027)
ax.set_ylabel("% per year")
fig.tight_layout()
fig.savefig("report/figures/fig9_flows.pdf", bbox_inches="tight")
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
P["female"] = (P["PESEX"] == 2).astype(int)
P["ma_only"] = (P["PEEDUCA"] == 44).astype(int)
P["ma_plus"] = (P["PEEDUCA"] >= 44).astype(int)
P["prof_phd"] = (P["PEEDUCA"] >= 45).astype(int)
P["public"] = P["PEIO1COW"].isin([1, 2, 3]).astype(int)
P["parttime"] = P["PEHRUSL1"].between(1, 34).astype(int)
P["hours"] = P["PEHRUSL1"].where(P["PEHRUSL1"] > 0)
P["multjob"] = (P["PEMJOT"] == 1).astype(int)
P["married"] = P["PEMARITL"].isin([1, 2]).astype(int)
P["n_children"] = P["PRNMCHLD"].clip(lower=0)
P["child_u6"] = P["PRCHLD"].isin(CHLD_U6).astype(int)
P["white"] = (P["PTDTRACE"] == 1).astype(int)
P["black"] = (P["PTDTRACE"] == 2).astype(int)
P["asian"] = (P["PTDTRACE"] == 4).astype(int)
P["hispanic"] = (P["PEHSPNON"] == 1).astype(int)
P["noncitizen"] = (P["PRCITSHP"] == 5).astype(int)
P["faminc75k"] = (P["HEFAMINC"] >= 13).astype(int)
# outgoing rotations only (months in sample 4 and 8)
P["union"] = (P["PEERNLAB"] == 1).astype(float).where(P["PEERNLAB"] > 0)
P["wkearn"] = (P["PTERNWA"] / 100.0).where(P["PTERNWA"] > 0)
P["region"] = np.select(
    [P["GESTFIPS"].isin(NEs), P["GESTFIPS"].isin(MWs), P["GESTFIPS"].isin(SOs)],
    ["Northeast", "Midwest", "South"], default="West")
P["tch_i"] = P["tch"].astype(int)


def wsh(g, col):
    return np.average(g[col], weights=g["PWSSWGT"]) * 100


def wmean(g, col):
    m = g[col].notna()
    return np.average(g.loc[m, col], weights=g.loc[m, "PWSSWGT"])


def wmedian(g, col):
    m = g[col].notna()
    s = g.loc[m].sort_values(col)
    cw = s["PWSSWGT"].cumsum() / s["PWSSWGT"].sum()
    return s.loc[cw >= 0.5, col].iloc[0]


T, O = P[P["tch"]], P[~P["tch"]]

# ---------- portrait table with tests ----------
import statsmodels.formula.api as smf


def pstars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


PANELS = [
    ("Panel A. Demographics", [
        ("Age, years", "PRTAGE", "num"),
        ("Female", "female", "pct"),
        ("White", "white", "pct"),
        ("Black", "black", "pct"),
        ("Asian", "asian", "pct"),
        ("Hispanic", "hispanic", "pct"),
        ("Non-citizen", "noncitizen", "pct"),
    ]),
    ("Panel B. Family", [
        ("Married", "married", "pct"),
        ("Number of own children ($<$18) at home", "n_children", "num"),
        ("Child under 6 at home", "child_u6", "pct"),
    ]),
    ("Panel C. Education", [
        ("Master's degree", "ma_only", "pct"),
        ("Professional degree or doctorate", "prof_phd", "pct"),
    ]),
    ("Panel D. The job", [
        ("Public-sector employer", "public", "pct"),
        ("Union member$^{a}$", "union", "pct"),
        ("Usual weekly hours", "hours", "num"),
        ("Part-time ($<$35 h/week)", "parttime", "pct"),
        ("Holds more than one job", "multjob", "pct"),
    ]),
    ("Panel E. Pay and income", [
        ("Weekly earnings, median$^{a}$", "wkearn", "usd"),
        ("Family income \\$75k+", "faminc75k", "pct"),
    ]),
]

with open("report/table_portrait.tex", "w") as fh:
    fh.write("\\begin{tabular}{lccc}\n\\toprule\n"
             " & School teachers & Other college- & Difference \\\\\n"
             " & & educated workers & \\\\\n\\midrule\n")
    for ipanel, (panel, items) in enumerate(PANELS):
        rows_out = []
        for lab, v, kind in items:
            sub = P[P[v].notna()]
            t = smf.wls(f"{v} ~ tch_i", data=sub,
                        weights=sub["PWSSWGT"]).fit(
                cov_type="cluster", cov_kwds={"groups": sub["HRHHID"]})
            d, p = t.params["tch_i"], t.pvalues["tch_i"]
            tstat = abs(t.tvalues["tch_i"])
            if kind == "usd":
                a, b = wmedian(T, v), wmedian(O, v)
                cells = [f"\\${a:,.0f}", f"\\${b:,.0f}",
                         f"$-$\\${b-a:,.0f}" + pstars(p)]
            else:
                a, b = (wmean(T, v) * 100, wmean(O, v) * 100) \
                    if kind == "pct" else (wmean(T, v), wmean(O, v))
                fmt = (lambda x: f"{x:.1f}\\%") if kind == "pct" else \
                      (lambda x: f"{x:.1f}")
                dtxt = f"{d*100:+.1f}\\,pp" if kind == "pct" else f"{d:+.2f}"
                cells = [fmt(a), fmt(b), dtxt + pstars(p)]
            rows_out.append((tstat, f"{lab} & " + " & ".join(cells) + " \\\\\n"))
        if ipanel > 0:
            fh.write("\\midrule\n")
        fh.write(f"\\multicolumn{{4}}{{l}}{{\\textit{{{panel}}}}} \\\\[2pt]\n")
        for _, line in sorted(rows_out, key=lambda r: -r[0]):
            fh.write(line)
        fh.write("\\addlinespace[3pt]\n")
    fh.write("\\midrule\nPersons (monthly interviews pooled) & "
             f"{len(T):,} & {len(O):,} & \\\\\n\\bottomrule\n\\end{{tabular}}\n")
print("wrote report/table_portrait.tex")
print(f"union: T {wmean(T,'union')*100:.1f}% vs O {wmean(O,'union')*100:.1f}%")
print(f"median weekly earnings: T ${wmedian(T,'wkearn'):,.0f} "
      f"vs O ${wmedian(O,'wkearn'):,.0f}")
# ---------- fig12a: age distribution, standalone ----------
fig, ax = plt.subplots(figsize=(6.6, 3.2))
bins = np.arange(20, 75, 2)
for g, c in [(O, GRAY), (T, BLUE)]:
    h, _ = np.histogram(g["PRTAGE"], bins=bins, weights=g["PWSSWGT"])
    ax.plot(bins[:-1] + 1, h / h.sum() * 100, color=c, lw=2,
            solid_capstyle="round")
handles = [plt.Line2D([], [], color=c, lw=2) for c in (BLUE, GRAY)]
ax.legend(handles, ["School teachers", "Other college-educated workers"],
          loc="upper center", bbox_to_anchor=(0.5, 1.16), ncols=2,
          frameon=False, fontsize=9)
ax.set_ylim(0, None)
ax.set_xlabel("Age")
ax.set_ylabel("% of the group")
fig.tight_layout()
fig.savefig("report/figures/fig12a_age.pdf", bbox_inches="tight")
plt.close(fig)

# ---------- fig12b: composition dumbbells (geography lives in the map) ----
fig, ax = plt.subplots(figsize=(6.9, 3.6))
traits = [("Female", "female"), ("Master's degree+", "ma_plus"),
          ("Public sector", "public"), ("Union member", "union"),
          ("Married", "married"), ("Child under 6", "child_u6"),
          ("Part-time", "parttime")]
yy = np.arange(len(traits))[::-1]
for yi, (lab, v) in zip(yy, traits):
    a, b = wmean(O, v) * 100, wmean(T, v) * 100
    ax.plot([a, b], [yi, yi], color="#d8dbe0", lw=2, zorder=2)
    ax.scatter([a], [yi], s=54, color=GRAY, zorder=3, edgecolor=SURFACE,
               linewidth=2)
    ax.scatter([b], [yi], s=54, color=BLUE, zorder=4, edgecolor=SURFACE,
               linewidth=2)
    off = 3.2 if b >= a else -3.2
    ax.text(b + off, yi, f"{b:.0f}%", va="center",
            ha="left" if b >= a else "right", fontsize=9, color=INK,
            fontweight="bold")
    ax.text(a - off, yi, f"{a:.0f}%", va="center",
            ha="right" if b >= a else "left", fontsize=9, color=SUBTLE)
ax.set_yticks(yy, [t for t, _ in traits], fontsize=9.5)
ax.set_xlim(-6, 112)
ax.yaxis.grid(False)
handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=c)
           for c in (BLUE, GRAY)]
ax.legend(handles, ["School teachers", "Other college-educated workers"],
          loc="upper center", bbox_to_anchor=(0.5, -0.08), ncols=2,
          frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("report/figures/fig12b_traits.pdf", bbox_inches="tight")
plt.close(fig)
print("portrait: teachers female", round(wsh(T, 'female')),
      "% vs others", round(wsh(O, 'female')), "%")

print("funnel:", funnel, "| linked:", n_linked, "| follow-up:", n_followup)
print(yr[["total"]].round(2).tail(3).to_string())
print(fl[["base_year", "entry_rate", "exit_rate"]].round(1).tail(3).to_string(index=False))
print("saved table_population.tex, fig0, fig7, fig8, fig9")
