"""Figures 1-3 of the Former Teachers working paper, in the layout of OECD
Education at a Glance 2025 (Figures D3.1 and D8.6): light grey plot area
with white gridlines, legend in a grey box above the plot, countries ranked
in descending order, OECD average highlighted, Arial Narrow type (Nimbus Sans
Narrow, its metric clone, when Arial Narrow is not installed).

Data: Figure 1, EAG 2025 Table D8.4 columns 9-11 (pre-primary to upper
secondary, 2022/23); Figure 2, EAG 2025 Table D3.2 column 7 (primary
teachers' actual salaries relative to earnings of full-time, full-year
tertiary-educated workers, 2024); Figure 3, probit profiles estimated on the
CPS ASEC (college-graduate teachers, 2015-2024), as in fig13_age_route_profiles.py.

Run from the repository root: python3 replication/deck_figures/fig_oecd_former_teachers.py
"""
import glob
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle

OUT = "report/former_teachers/figures"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- style
for f in fm.findSystemFonts():
    if "NimbusSansNarrow" in f or "ArialNarrow" in f.replace(" ", "") or "arialn" in f.lower():
        fm.fontManager.addfont(f)
NARROW = next((n for n in ("Arial Narrow", "Nimbus Sans Narrow")
               if any(n == x.name for x in fm.fontManager.ttflist)), "DejaVu Sans")
plt.rcParams.update({
    "font.family": NARROW, "font.size": 7.5, "axes.unicode_minus": False,
    "axes.facecolor": "#F1F1F1", "figure.facecolor": "white",
    "axes.edgecolor": "#000000", "axes.linewidth": 0.6,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": "white",
    "grid.linewidth": 0.8, "axes.axisbelow": True,
    "xtick.major.size": 0, "ytick.major.size": 0,
    "xtick.color": "#000000", "ytick.color": "#000000",
    "savefig.dpi": 300,
})
NAVY, BLUE, LBLUE, CYAN, LCYAN = "#002F6C", "#006BB6", "#7FA8D9", "#00AACC", "#83D2E3"
SAL = "#113C75"
AVG_DARK, AVG_LIGHT, AVG_PALE = "#E2401C", "#F0A08A", "#F6C9BC"
W_IN = 16.4 / 2.54


def frame(ax, unit):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.text(-0.005, 1.02, unit, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7.5)


def legend_box(fig, ax, handles, labels, ncol=1):
    leg = ax.legend(handles, labels, loc="lower left", bbox_to_anchor=(0, 1.06, 1, 0.2),
                    mode="expand", ncol=ncol, frameon=True, fontsize=7,
                    handlelength=0.9, handleheight=0.9, borderpad=0.6,
                    labelspacing=0.35, columnspacing=1.5)
    leg.get_frame().set_facecolor("#F1F1F1")
    leg.get_frame().set_edgecolor("#F1F1F1")
    leg.get_frame().set_boxstyle("Square", pad=0.0)
    return leg


def xlabels(ax, names):
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right", rotation_mode="anchor",
                       fontsize=7.2)
    ax.set_xlim(-0.6, len(names) - 0.4)


# ---------------------------------------------------------------- Figure 1
# (name, total %, resigned share %, retired share %); None = no breakdown
D84 = [
    ("Lithuania", 12.5, None, None), ("Denmark", 11.8, 85, 15),
    ("Estonia", 11.6, 81, 19), ("England (UK)", 9.5, 91, 9),
    ("Netherlands", 8.6, None, None), ("New Zealand", 8.5, None, None),
    ("Bulgaria", 8.3, None, None), ("Flemish Comm. (Belgium)", 8.3, 76, 24),
    ("United States", 7.9, None, None), ("OECD average", 6.5, 51, 49),
    ("Slovak Republic", 6.4, 58, 42), ("Austria", 6.2, 51, 49),
    ("Sweden", 5.9, 77, 23), ("French Comm. (Belgium)", 4.8, 33, 67),
    ("Poland", 4.4, 61, 39), ("Portugal", 3.9, None, None),
    ("Greece", 2.7, 5, 95), ("France", 2.7, 15, 85),
    ("Ireland", 2.3, 39, 61), ("Israel", 2.1, 28, 72),
]
fig, ax = plt.subplots(figsize=(W_IN, 3.55))
names = [r[0] for r in D84]
for i, (n, tot, rs, rt) in enumerate(D84):
    avg = n == "OECD average"
    if rs is None:
        ax.bar(i, tot, 0.6, color=LCYAN, lw=0)
    else:
        res = tot * rs / 100
        ax.bar(i, res, 0.6, color=AVG_DARK if avg else BLUE, lw=0)
        ax.bar(i, tot - res, 0.6, bottom=res, color=AVG_LIGHT if avg else CYAN, lw=0)
ax.set_ylim(0, 14)
ax.set_yticks(range(0, 15, 2))
frame(ax, "%")
xlabels(ax, names)
h = [Rectangle((0, 0), 1, 1, color=c) for c in (BLUE, CYAN, LCYAN)]
legend_box(fig, ax, h, ["Teachers who resigned from the profession",
                        "Teachers who retired from the profession",
                        "Teachers who resigned or retired (no breakdown available)"])
fig.subplots_adjust(left=0.06, right=0.995, top=0.80, bottom=0.27)
fig.savefig(f"{OUT}/figure1_leaving_rate.png")
plt.close(fig)

# ---------------------------------------------------------------- Figure 2
D32 = [
    ("Peru", 1.51), ("Costa Rica", 1.31), ("Portugal", 1.28), ("Romania", 1.14),
    ("Australia", 0.97), ("Scotland (UK)", 0.94), ("Lithuania", 0.89),
    ("Germany", 0.88), ("Estonia", 0.87), ("Israel", 0.86), ("Poland", 0.85),
    ("New Zealand", 0.84), ("OECD average", 0.83), ("Slovenia", 0.83),
    ("Denmark", 0.82), ("England (UK)", 0.82), ("Flemish Comm. (Belgium)", 0.82),
    ("Finland", 0.81), ("Netherlands", 0.80), ("French Comm. (Belgium)", 0.78),
    ("Latvia", 0.77), ("Austria", 0.75), ("Chile", 0.75), ("France", 0.74),
    ("Slovak Republic", 0.74), ("Norway", 0.73), ("Sweden", 0.73),
    ("Czechia", 0.72), ("Greece", 0.69), ("Italy", 0.67), ("Hungary", 0.66),
    ("United States", 0.63),
]
fig, ax = plt.subplots(figsize=(W_IN, 3.4))
for i, (n, v) in enumerate(D32):
    ax.bar(i, v, 0.6, color=AVG_DARK if n == "OECD average" else SAL, lw=0)
ax.axhline(1.0, color="#000000", lw=0.9, zorder=3)
ax.set_ylim(0, 1.6)
ax.set_yticks(np.arange(0, 1.61, 0.2))
ax.set_yticklabels([f"{t:.1f}" for t in np.arange(0, 1.61, 0.2)])
frame(ax, "Ratio")
xlabels(ax, [r[0] for r in D32])
h = [Rectangle((0, 0), 1, 1, color=SAL),
     plt.Line2D([0], [0], color="#000000", lw=0.9)]
legend_box(fig, ax, h, ["Primary teachers' actual salaries relative to earnings of "
                        "full-time, full-year tertiary-educated workers",
                        "Parity with tertiary-educated workers"])
fig.subplots_adjust(left=0.06, right=0.995, top=0.83, bottom=0.27)
fig.savefig(f"{OUT}/figure2_relative_salaries.png")
plt.close(fig)

# ---------------------------------------------------------------- Figure 3
import statsmodels.api as sm
from scipy.stats import norm

RAW = "data/raw/asec"
WGT = "MARSUPWT"
CORE = {2300, 2310, 2320, 2330}


def tset(ay):
    return CORE | ({2340} if ay <= 2019 else {2360})


cache = f"{OUT}/figure3_profiles.csv"
if os.path.exists(cache):
    PR = pd.read_csv(cache)
else:
    R = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{RAW}/asec_rich_*.parquet"))],
                  ignore_index=True)
    for c in R.columns:
        if c != "PERIDNUM":
            R[c] = pd.to_numeric(R[c], errors="coerce")
    R["cal_year"] = R["asec_year"] - 1
    ptr = []
    for c in ["A_PARENT", "PEPAR1", "PEPAR2"]:
        if c in R.columns:
            k = R[(pd.to_numeric(R[c], errors="coerce") > 0) & (R["A_AGE"] < 18)][
                ["asec_year", "PH_SEQ", c, "A_AGE", "A_LINENO"]].rename(
                columns={c: "parent_line", "A_LINENO": "kid_line"})
            ptr.append(k)
    kids = pd.concat(ptr, ignore_index=True).drop_duplicates(
        ["asec_year", "PH_SEQ", "parent_line", "kid_line"])
    agg = kids.groupby(["asec_year", "PH_SEQ", "parent_line"])["A_AGE"].agg(
        n_children="size", child_u6=lambda s: int((s < 6).any()),
        new_baby=lambda s: int((s < 1).any())).reset_index().rename(
        columns={"parent_line": "A_LINENO"})
    R = R.merge(agg, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
    sp = R[R["A_SPOUSE"] > 0][["asec_year", "PH_SEQ", "A_SPOUSE", "n_children",
                               "child_u6", "new_baby"]].rename(
        columns={"A_SPOUSE": "A_LINENO", "n_children": "n2", "child_u6": "c2",
                 "new_baby": "b2"})
    sp = sp.groupby(["asec_year", "PH_SEQ", "A_LINENO"]).max().reset_index()
    R = R.merge(sp, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
    for a, b in [("n_children", "n2"), ("child_u6", "c2"), ("new_baby", "b2")]:
        R[a] = R[[a, b]].max(axis=1).fillna(0)
    R["female"] = (R["A_SEX"] == 2).astype(int)
    R["black"] = (R["PRDTRACE"] == 2).astype(int)
    R["married"] = R["A_MARITL"].isin([1, 2, 3]).astype(int)
    R["sepdiv"] = R["A_MARITL"].isin([5, 6]).astype(int)
    R["ba_plus"] = (R["A_HGA"] >= 43).astype(int)
    R["ma_plus"] = (R["A_HGA"] >= 44).astype(int)
    R["public"] = R["LJCW"].isin([2, 3, 4]).astype(int)
    R["pension"] = (R["PENPLAN"] == 1).astype(int)
    R["parttime"] = R["HRSWK"].between(1, 34).astype(int)
    R["fullyear"] = (R["WKSWORK"] >= 50).astype(int)
    R["age2"] = R["A_AGE"] ** 2
    teach = []
    for ay, g in R.groupby("asec_year"):
        cs = tset(int(ay))
        b = g[g["OCCUP"].isin(cs)].copy()
        emp = b["A_LFSR"].isin([1, 2])
        b["switch"] = (emp & ~b["PEIOOCC"].isin(cs)).astype(int)
        b["unemp"] = b["A_LFSR"].isin([3, 4]).astype(int)
        b["leftlf"] = (~b["A_LFSR"].isin([1, 2, 3, 4])).astype(int)
        b["leaver"] = (b["switch"] | b["unemp"] | b["leftlf"]).astype(int)
        teach.append(b)
    T = pd.concat(teach, ignore_index=True)
    win = T[(T["ba_plus"] == 1) & (T["A_AGE"] >= 18) & T["cal_year"].between(2015, 2024)]
    XV = ["A_AGE", "age2", "female", "black", "married", "sepdiv", "ma_plus", "public",
          "pension", "parttime", "fullyear", "n_children", "child_u6", "new_baby"]
    rows = []
    for dep in ("leaver", "switch", "leftlf"):
        sub = win.dropna(subset=XV + [dep, WGT]).copy()
        yd = pd.get_dummies(sub["asec_year"], prefix="y", drop_first=True, dtype=float)
        X = sm.add_constant(pd.concat([sub[XV].astype(float), yd], axis=1))
        pm = sm.Probit(sub[dep].astype(float), X).fit(disp=0)
        beta, V = pm.params.values, pm.cov_params().values
        cols = list(X.columns)
        xbar = X.mean(axis=0).values.copy()
        ia, ia2 = cols.index("A_AGE"), cols.index("age2")
        for a in range(23, 67):
            xx = xbar.copy()
            xx[ia], xx[ia2] = a, a * a
            z = xx @ beta
            se = np.sqrt(xx @ V @ xx)
            rows.append((dep, a, norm.cdf(z) * 100, norm.cdf(z - 1.96 * se) * 100,
                         norm.cdf(z + 1.96 * se) * 100))
    PR = pd.DataFrame(rows, columns=["outcome", "age", "p", "lo", "hi"])
    PR.to_csv(cache, index=False)

panels = [("leaver", "Leaving teaching by any route", NAVY),
          ("switch", "Moving to another occupation", BLUE),
          ("leftlf", "Leaving the labour force", CYAN)]
fig, axes = plt.subplots(1, 3, figsize=(W_IN, 2.55))
for ax, (dep, title, col) in zip(axes, panels):
    s = PR[PR["outcome"] == dep]
    ax.fill_between(s["age"], s["lo"], s["hi"], color=col, alpha=0.22, lw=0)
    ax.plot(s["age"], s["p"], color=col, lw=1.6)
    ax.set_title(title, fontsize=8, fontweight="bold", pad=14)
    ax.set_xticks([25, 35, 45, 55, 65])
    ax.set_xlim(22, 67)
    ax.set_ylim(0, None)
    frame(ax, "%")
    ax.set_xlabel("Age", fontsize=7.5, labelpad=2)
fig.subplots_adjust(left=0.05, right=0.99, top=0.82, bottom=0.17, wspace=0.28)
fig.savefig(f"{OUT}/figure3_age_profiles.png")
plt.close(fig)
print("saved figures with font", NARROW)
