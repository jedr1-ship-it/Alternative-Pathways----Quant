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
M = M[M["leaver_ba"].notna()].sort_values("cal_year").reset_index(
    drop=True)
M = M.rename(columns={"leaver_ba": "leave", "rate_switch": "switch",
                      "rate_unemp": "unemp", "rate_leftlf": "leftlf"})
# the exit assigned to calendar t is observed in March t+1: the
# cleanest market measure is the unemployment rate OF that March
UM = pd.read_csv("outputs/n_urate_march.csv")
M["survey_year"] = M["cal_year"] + 1
M = M.merge(UM, on="survey_year", how="left")
M["urate_obs"] = M["u_march"]
M.to_csv("outputs/n_cyclicality.csv", index=False)
MS = M.dropna(subset=["urate_obs"])
for a in ("leave", "switch", "leftlf", "unemp"):
    r = np.corrcoef(MS[a], MS["urate_obs"])[0, 1]
    print(f"corr({a}, u March of survey) = {r:+.2f}")

TXT5, MUT5 = "#3B4046", "#8A9096"
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.6, 4.3),
                             gridspec_kw={"width_ratios": [1.35, 1]})
a1.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
lv_s = M["leave"].rolling(3, center=True, min_periods=2).mean()
ur_s = M["urate"].rolling(3, center=True, min_periods=2).mean()
a1.plot(M["cal_year"], M["leave"], color="#C3D3E4", lw=1.0)
a1.plot(M["cal_year"], M["urate"], color="#D4D7DA", lw=1.0)
a1.plot(M["cal_year"], lv_s, color=BLUE, lw=2.4,
        solid_capstyle="round")
a1.plot(M["cal_year"], ur_s, color=TXT5, lw=2.0, ls=(0, (5, 3)),
        solid_capstyle="round")
for ser, c in [(lv_s, BLUE), (ur_s, TXT5)]:
    a1.plot(M["cal_year"].iloc[-1], ser.iloc[-1], "o", color=c, ms=6,
            mec="white", mew=1.6, zorder=6)
    a1.annotate(f"{ser.iloc[-1]:.1f}", (M["cal_year"].iloc[-1],
                ser.iloc[-1]), xytext=(4, 8),
                textcoords="offset points", fontsize=9, color=c,
                fontweight="bold")
a1.annotate("Teachers leaving the profession", (2010.5, 10.6),
            fontsize=9.5, color=BLUE, fontweight="bold", ha="center")
a1.annotate("Unemployment rate (BLS)", (2005.6, 2.4), fontsize=9,
            color=TXT5, ha="center")
a1.text(2019.5, 11.9, "Covid", ha="center", fontsize=8.5, color=SUBTLE)
a1.set_ylim(0, 12.8)
a1.set_yticks([0, 2, 4, 6, 8, 10, 12])
a1.set_xticks(range(1998, 2025, 4))
a1.tick_params(labelsize=9, length=0, colors=MUT5)
a1.set_ylabel("Percent (3-yr averages; annual in light)", fontsize=10,
              color=TXT5)
a1.grid(axis="y", color="#F1F2F3", lw=1.0)
a1.set_axisbelow(True)
for s in ("top", "right", "left"):
    a1.spines[s].set_visible(False)
a1.spines["bottom"].set_color("#D8DBDE")
# binscatter: 8 quantile bins of the March unemployment rate; each
# point is the mean exit rate within the bin (Stata binscatter style)
MS = MS.copy()
MS["bin"] = pd.qcut(MS["urate_obs"], 8, labels=False, duplicates="drop")
NAVY, GRPH = "#2F5D8C", "#6B7280"
for dep, c, lab, dy in [("leftlf", NAVY, "Out of the labor force", 7),
                        ("switch", GRPH, "To another job", -13)]:
    bx = MS.groupby("bin")["urate_obs"].mean()
    by = MS.groupby("bin")[dep].mean()
    a2.scatter(bx, by, color=c, s=42, zorder=4)
    b1, b0 = np.polyfit(MS["urate_obs"], MS[dep], 1)
    xs = np.linspace(MS["urate_obs"].min(), MS["urate_obs"].max(), 10)
    a2.plot(xs, b0 + b1 * xs, color=c, lw=1.4, zorder=3)
    a2.annotate(lab, (xs[-1], b0 + b1 * xs[-1]), fontsize=9,
                color=TXT5, va="center", ha="right",
                xytext=(0, dy), textcoords="offset points")
a2.set_xlabel("Unemployment rate in the survey month (%)",
              fontsize=10, color=TXT5)
a2.set_ylabel("Exit rate by route (%)", fontsize=10, color=TXT5)
a2.tick_params(labelsize=9, length=0, colors=MUT5)
a2.grid(color="#F1F2F3", lw=1.0)
a2.set_axisbelow(True)
for s in ("top", "right", "left"):
    a2.spines[s].set_visible(False)
a2.spines["bottom"].set_color("#D8DBDE")
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
