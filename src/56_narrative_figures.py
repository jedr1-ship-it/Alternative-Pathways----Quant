"""
New figures for the re-founded narrative, matching the approved visual
system: n5 cyclicality (leaving and its routes against the unemployment
rate, with the route-level scatter that answers whether teacher exits are
countercyclical), n6 relative pay (teacher median full-time full-year
weekly earnings against all college graduates and nurses), and the
appendix balance bar chart by five-year block.
"""
import glob
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "src")
from paperstyle import BLUE, CORAL, GOLD, GREEN, GRAY, INK, SUBTLE  # noqa

FIG = "report/figures"
RAW = "data/raw/asec"
W = "MARSUPWT"
CORE = {2300, 2310, 2320, 2330}


def tset(ay):
    return CORE | ({2340} if ay <= 2019 else {2360})


def despine(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# ---------- N5 cyclicality: THE series (p_series, same as Figure 2)
# against the OFFICIAL unemployment rate (BLS via FRED), 1997-2024 ----
S5 = pd.read_csv("outputs/p_series.csv").sort_values("cal_year")
U = pd.read_csv("outputs/n_urate_official.csv")
M = S5.merge(U[["cal_year", "urate"]], on="cal_year")
M = M[M["leaver_ba"].notna()]
M = M.rename(columns={"leaver_ba": "leave", "rate_switch": "switch",
                      "rate_unemp": "unemp", "rate_leftlf": "leftlf"})
M.to_csv("outputs/n_cyclicality.csv", index=False)

for a in ("leave", "switch", "leftlf", "unemp"):
    r = np.corrcoef(M[a], M["urate"])[0, 1]
    print(f"corr({a}, official unemployment) = {r:+.2f}")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.8, 4.3),
                             gridspec_kw={"width_ratios": [1.35, 1]})
a1.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
a1.plot(M["cal_year"], M["leave"], color=BLUE, lw=2.2, marker="o", ms=4.0)
a1.plot(M["cal_year"], M["urate"], color=INK, lw=1.6, ls="--", marker="s",
        ms=3.0)
a1.annotate("teachers leaving the profession", (2011.5, 11.0), fontsize=9,
            color=BLUE, fontweight="bold", ha="center")
a1.annotate("unemployment rate (BLS)", (2002.5, 2.6), fontsize=8.6,
            color=INK, ha="center")
a1.text(2019.5, 11.9, "Covid", ha="center", fontsize=9, color=SUBTLE)
a1.set_ylim(0, 12.8)
a1.set_xticks(range(1998, 2025, 4))
a1.set_ylabel("Percent")
a1.set_title("Leaving is flat while unemployment swings", fontsize=10.5,
             loc="left")
a1.grid(axis="y", color="#EFEFEF", lw=0.6)
a1.set_axisbelow(True)
despine(a1)
for dep, c, lab in [("switch", GOLD, "to another job"),
                    ("leftlf", BLUE, "out of the labor force")]:
    a2.scatter(M["urate"], M[dep], color=c, s=30, zorder=3)
    b1, b0 = np.polyfit(M["urate"], M[dep], 1)
    xs = np.linspace(M["urate"].min(), M["urate"].max(), 10)
    a2.plot(xs, b0 + b1 * xs, color=c, lw=1.6)
    r = np.corrcoef(M["urate"], M[dep])[0, 1]
    ypos = (b0 + b1 * xs[-1])
    a2.annotate(f"{lab}  (r = {r:+.2f})", (xs[-1], ypos), fontsize=8.8,
                color=c, va="bottom", ha="right",
                xytext=(0, 5), textcoords="offset points")
a2.set_xlabel("Unemployment rate (%), BLS annual average")
a2.set_ylabel("Exit rate by route (%)")
a2.set_title("Routes respond differently to the cycle", fontsize=10.5,
             loc="left")
a2.grid(color="#EFEFEF", lw=0.6)
a2.set_axisbelow(True)
despine(a2)
fig.tight_layout(w_pad=3)
fig.savefig(f"{FIG}/n5_cyclicality.pdf")
plt.close(fig)

# ------ N6a: occupational leaving, teachers vs other professions ------
PSER = pd.read_csv("outputs/p_prof_series.csv")
PROF_STYLE = [("Teachers", BLUE, 2.6, 1.0),
              ("Registered nurses", "#3E7C59", 1.8, 0.9),
              ("Social workers", GOLD, 1.8, 0.9),
              ("Accountants", "#8D87A8", 1.8, 0.9),
              ("Lawyers", "#B0B6BC", 1.8, 0.9)]
fig, ax = plt.subplots(figsize=(8.8, 4.5))
lab_y = {}
for prof, c, lw, al in PROF_STYLE:
    d = PSER[PSER["prof"] == prof].sort_values("cal_year")
    sm = d["leave"].rolling(3, center=True, min_periods=2).mean()
    ax.plot(d["cal_year"], sm, color=c, lw=lw, alpha=al)
    lab_y[prof] = sm.iloc[-1]
# de-collide right-margin labels
order = sorted(lab_y, key=lab_y.get)
ys = sorted(lab_y.values())
for i in range(1, len(ys)):
    if ys[i] - ys[i - 1] < 1.0:
        ys[i] = ys[i - 1] + 1.0
for prof, y in zip(order, ys):
    c = dict((p, cc) for p, cc, *_ in PROF_STYLE)[prof]
    ax.text(2024.6, y, prof, fontsize=9, color=c, va="center",
            fontweight="bold" if prof == "Teachers" else "normal")
ax.set_xticks(range(2002, 2025, 2))
ax.set_xticklabels(range(2002, 2025, 2), fontsize=8.4, rotation=45)
ax.set_xlim(2002, 2032)
ax.set_ylim(0, 16)
ax.set_ylabel("Percent leaving the occupation (3-yr avg)")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/n6a_professions_series.pdf")
plt.close(fig)

# ---------- N6 relative pay ----------
P = pd.read_csv("outputs/n_relative_pay.csv")
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.axhline(100, color=INK, lw=0.9)
ax.text(2010.1, 100.8, "parity with the median college graduate",
        fontsize=8.4, color=SUBTLE)
ax.plot(P["cal_year"], P["rel_college"], color=BLUE, lw=2.2, marker="o",
        ms=4.4)
ax.plot(P["cal_year"], P["rel_nurses"], color=GREEN, lw=1.5, marker="s",
        ms=3.4, alpha=0.85)
ax.annotate(f"{P['rel_college'].iloc[0]:.0f}",
            (P["cal_year"].iloc[0], P["rel_college"].iloc[0]),
            xytext=(-2, 8), textcoords="offset points", fontsize=9,
            color=BLUE, fontweight="bold")
ax.annotate(f"{P['rel_college'].iloc[-1]:.0f}",
            (P["cal_year"].iloc[-1], P["rel_college"].iloc[-1]),
            xytext=(4, 8), textcoords="offset points", fontsize=9,
            color=BLUE, fontweight="bold", ha="right")
ax.annotate("teachers / all college graduates", (2017.4, 78.3), fontsize=9,
            color=BLUE, fontweight="bold", ha="center")
ax.annotate("teachers / registered nurses", (2014.5, 69.6), fontsize=8.6,
            color=GREEN, ha="center")
ax.set_ylim(60, 105)
ax.set_ylabel("Teacher median weekly earnings, % of comparison group")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/n6_relative_pay.pdf")
plt.close(fig)

# ---------- appendix: balance bar chart by block ----------
B = pd.read_csv("outputs/n_balance_blocks.csv")
VARS = ["Age", "Female %", "Master's+ %", "Has own children %",
        "Part-time %", "Black %"]
blocks = ["2010-2014", "2015-2019", "2020-2024"]
fig, axes = plt.subplots(2, 3, figsize=(11.6, 5.6))
for axp, v in zip(axes.flat, VARS):
    d = B[B["variable"] == v].set_index("block").loc[
        blocks, ["teachers", "other_college"]].astype(float)
    x = np.arange(3)
    axp.bar(x - 0.19, d["teachers"], width=0.38, color=BLUE,
            label="Teachers")
    axp.bar(x + 0.19, d["other_college"], width=0.38, color=GRAY,
            label="Other college graduates")
    for xi, (t, o) in zip(x, zip(d["teachers"], d["other_college"])):
        axp.text(xi - 0.19, t, f"{t:.0f}", ha="center", va="bottom",
                 fontsize=8, color=BLUE)
        axp.text(xi + 0.19, o, f"{o:.0f}", ha="center", va="bottom",
                 fontsize=8, color=SUBTLE)
    axp.set_title(v, fontsize=10, pad=6)
    axp.set_xticks(x)
    axp.set_xticklabels(blocks, fontsize=8)
    axp.set_ylim(0, float(d.values.max()) * 1.22)
    despine(axp)
axes.flat[0].legend(frameon=False, fontsize=8, loc="lower right")
fig.tight_layout(h_pad=2.2)
fig.savefig(f"{FIG}/napp_balance.pdf")
plt.close(fig)
print("figures n5, n6, napp written")
