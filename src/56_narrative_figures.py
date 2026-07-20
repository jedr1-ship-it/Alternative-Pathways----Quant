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
M1 = M[M["cal_year"] >= 2000]
# one marker per year on BOTH series: every point above has its pair
# below, same year
a1.plot(M1["cal_year"], M1["leave"], color=BLUE, lw=2.0, marker="o",
        ms=4.2, mec="white", mew=0.9, solid_capstyle="round")
a1.plot(M1["cal_year"], M1["urate"], color=TXT5, lw=1.6,
        ls=(0, (5, 3)), marker="o", ms=4.2, mec="white", mew=0.9,
        solid_capstyle="round")
for col, c in [("leave", BLUE), ("urate", TXT5)]:
    a1.annotate(f"{M1[col].iloc[-1]:.1f}", (M1["cal_year"].iloc[-1],
                M1[col].iloc[-1]), xytext=(6, 6),
                textcoords="offset points", fontsize=9, color=c,
                fontweight="bold")
a1.annotate("Teachers leaving the profession", (2010.5, 11.3),
            fontsize=9.5, color=BLUE, fontweight="bold", ha="center")
a1.annotate("Unemployment rate (BLS)", (2006.2, 2.2), fontsize=9,
            color=TXT5, ha="center")
a1.text(2019.5, 12.15, "Covid", ha="center", fontsize=8.5, color=SUBTLE)
a1.set_ylim(0, 12.8)
a1.set_yticks([0, 2, 4, 6, 8, 10, 12])
a1.set_xticks(range(2000, 2025, 4))
a1.tick_params(labelsize=9, length=0, colors=MUT5)
a1.set_ylabel("Percent", fontsize=10, color=TXT5)
a1.grid(axis="y", color="#F1F2F3", lw=1.0)
a1.set_axisbelow(True)
for s in ("top", "right", "left"):
    a1.spines[s].set_visible(False)
a1.spines["bottom"].set_color("#D8DBDE")
# binscatter: 8 quantile bins of the March unemployment rate; each
# point is the mean exit rate within the bin (Stata binscatter style)
MS = MS.copy()
MS["bin"] = pd.qcut(MS["urate_obs"], 10, labels=False,
                    duplicates="drop")
NAVY, GRPH = "#2F5D8C", "#6B7280"
bx = MS.groupby("bin")["urate_obs"].mean()
for dep, c, lab in [("leftlf", NAVY, "Out of the labor force"),
                    ("switch", GRPH, "To another job")]:
    by = MS.groupby("bin")[dep].mean()
    a2.scatter(bx, by, color=c, s=42, zorder=4)
    b1, b0 = np.polyfit(MS["urate_obs"], MS[dep], 1)
    xs = np.linspace(MS["urate_obs"].min(), MS["urate_obs"].max(), 10)
    a2.plot(xs, b0 + b1 * xs, color=c, lw=1.4, zorder=3)
    # both labels sit clearly ABOVE the right end of their fitted line
    a2.annotate(lab, (xs[-1], b0 + b1 * xs[-1]), fontsize=9,
                color=TXT5, va="bottom", ha="right",
                xytext=(0, 9), textcoords="offset points")
a2.set_ylim(1.55, 6.55)
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

# ------ N5b: three cyclicality regimes, one exemplar state each ------
FIPS_NAME = {37: "North Carolina", 34: "New Jersey"}
SS = pd.read_csv("outputs/p_state_series.csv")
SU = pd.read_csv("outputs/n_urate_states.csv")
SC = pd.read_csv("outputs/p_state_cycl.csv").set_index("GESTFIPS")
TXT5b, MUT5b = "#3B4046", "#8A9096"
fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9), sharey=True)
# scatter form: with 60-80 teachers per state-year the annual PATH is
# noise; a state's cyclicality lives in the SLOPE, so use the same
# language as the national binscatter -- one dot per year, OLS line
for ax, fips in zip(axes, FIPS_NAME):
    L = SS[SS["GESTFIPS"] == fips].copy()
    u = SU[SU["GESTFIPS"] == fips].copy()
    u["cal_year"] = u["survey_year"] - 1
    L = L.merge(u[["cal_year", "u_march"]], on="cal_year")
    # all 28 years as dots, OLS line on the same annual data
    ax.scatter(L["u_march"], L["leave"], color=BLUE, s=34, alpha=0.85,
               edgecolors="white", linewidths=1.1, zorder=4)
    b1, b0 = np.polyfit(L["u_march"], L["leave"], 1)
    xs = np.linspace(L["u_march"].min(), L["u_march"].max(), 10)
    ax.plot(xs, b0 + b1 * xs, color=TXT5b, lw=1.6, zorder=3)
    ax.set_title(FIPS_NAME[fips], fontsize=11, color=TXT5b, loc="left")
    ax.set_xlabel("State unemployment in the survey month (%)",
                  fontsize=9.3, color=TXT5b)
    ax.tick_params(labelsize=8.8, length=0, colors=MUT5b)
    ax.grid(color="#F1F2F3", lw=1.0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8DBDE")
axes[0].set_ylabel("Percent of teachers leaving", fontsize=10,
                   color=TXT5b)
axes[0].annotate("each dot: one year, 1997–2024", (0.97, 0.04),
                 xycoords="axes fraction", fontsize=8.6, color=MUT5b,
                 ha="right")
fig.tight_layout()
fig.savefig(f"{FIG}/n5b_states_trio.pdf")
plt.close(fig)

# ---- APPENDIX: per-state cyclicality forest, full state names ----
NAMES_FULL = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut",
    "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida",
    "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
    "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
    "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"}
RC = pd.read_csv("outputs/p_state_cycl.csv").sort_values("beta_pp")
RC["lo"] = RC["beta_pp"] - 1.96 * RC["se_pp"]
RC["hi"] = RC["beta_pp"] + 1.96 * RC["se_pp"]
RC["sig"] = (RC["lo"] > 0) | (RC["hi"] < 0)
ypos = np.arange(len(RC))
fig, ax = plt.subplots(figsize=(7.4, 10.2))
ax.axvline(0, color="#999999", lw=1.0)
for yv, (_, r) in zip(ypos, RC.iterrows()):
    c = (BLUE if r["beta_pp"] > 0 else CORAL) if r["sig"] else "#C4C9CE"
    ax.errorbar(r["beta_pp"], yv, xerr=1.96 * r["se_pp"], fmt="o",
                color=c, ms=4.6, elinewidth=1.1, capsize=0, zorder=4)
ax.set_yticks(ypos)
ax.set_yticklabels([NAMES_FULL[a] for a in RC["abbr"]], fontsize=7.8,
                   color=TXT5b)
for tick, (_, r) in zip(ax.get_yticklabels(), RC.iterrows()):
    if r["sig"]:
        tick.set_fontweight("bold")
ax.set_ylim(-1, len(RC))
ax.set_xlim(-6, 6)
ax.set_xlabel("Change in the leaving rate (pp) per 1-pt higher state\n"
              "unemployment at observation  (95% CI; bold = "
              "significant)", fontsize=9.5, color=TXT5b)
ax.annotate("exits rise in downturns →", (5.8, len(RC) - 2.2),
            fontsize=8.6, color=TXT5b, ha="right")
ax.annotate("← exits fall in downturns", (-5.8, 1.2),
            fontsize=8.6, color=TXT5b, ha="left")
ax.tick_params(length=0)
ax.grid(axis="x", color="#F1F2F3", lw=1.0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{FIG}/napp_state_cyclicality.pdf")
plt.close(fig)

# ==== N6b (approved): real FTFY median pay, same windows as G7 ====
PW = pd.read_csv("outputs/p_pay_windows.csv").pivot(
    index="prof", columns="window",
    values="real_med_k").sort_values("2015-2025")
TXT6, MUT6 = "#3B4046", "#8A9096"
fig, ax = plt.subplots(figsize=(8.0, 4.2))
for i, (prof, r) in enumerate(PW.iterrows()):
    c = BLUE if prof == "Teachers" else GRAY
    ax.plot([r["2004-2014"], r["2015-2025"]], [i, i], color=c, lw=1.8,
            alpha=0.75, zorder=2)
    ax.plot(r["2004-2014"], i, "o", color=c, ms=6.5, mfc="white",
            zorder=3)
    ax.plot(r["2015-2025"], i, "o", color=c, ms=7.5, zorder=3)
    ax.annotate(f"{r['2015-2025']:.0f}k", (r["2015-2025"], i),
                xytext=(9, -3), textcoords="offset points",
                fontsize=8.7, color=c,
                fontweight="bold" if prof == "Teachers" else "normal")
ax.set_yticks(range(len(PW)))
ax.set_yticklabels(PW.index, fontsize=9.6)
for tick, prof in zip(ax.get_yticklabels(), PW.index):
    if prof == "Teachers":
        tick.set_fontweight("bold")
        tick.set_color(BLUE)
hnd = [plt.Line2D([], [], marker="o", color=GRAY, mfc="white", ls=""),
       plt.Line2D([], [], marker="o", color=GRAY, ls="")]
ax.legend(hnd, ["Surveys 2004–2014", "Surveys 2015–2025"],
          frameon=False, fontsize=8.8, loc="lower right")
ax.set_xlabel("Real median annual earnings, full-time full-year, "
              "$1,000 of 2024", fontsize=9.8, color=TXT6)
ax.grid(axis="x", color="#F1F2F3", lw=1.0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{FIG}/n6b_pay_windows.pdf")
plt.close(fig)

# ==== N6c (candidate): real pay indexed, pruned to three lines ====
PP = pd.read_csv("outputs/p_pay_profs.csv")
fig, ax = plt.subplots(figsize=(8.4, 4.4))
for prof, c, lw, ls in [("Registered nurses", "#3E7C59", 1.7, "-"),
                        ("All college graduates", INK, 1.8, (0, (5, 3))),
                        ("Teachers", BLUE, 2.6, "-")]:
    d = PP[PP["prof"] == prof].sort_values("cal_year")
    sm = d["real_med"].rolling(3, center=True, min_periods=2).mean()
    idx = sm / sm.iloc[0] * 100
    ax.plot(d["cal_year"], idx, color=c, lw=lw, ls=ls)
    ax.text(2024.6, idx.iloc[-1], prof, fontsize=9, color=c,
            va="center",
            fontweight="bold" if prof == "Teachers" else "normal")
    ax.annotate(f"{idx.iloc[-1]:.0f}", (2024, idx.iloc[-1]),
                xytext=(-4, -11 if prof == "Teachers" else 8),
                textcoords="offset points", fontsize=8.8, color=c,
                fontweight="bold", ha="center")
ax.axhline(100, color="#CCCCCC", lw=0.8)
ax.set_xticks(range(2002, 2025, 4))
ax.set_xlim(2002, 2033)
ax.set_ylabel("Real median earnings, 2002 = 100\n(full-time full-year, "
              "3-yr avg)", fontsize=9.6, color=TXT6)
ax.tick_params(labelsize=9, length=0, colors=MUT6)
ax.grid(axis="y", color="#F1F2F3", lw=1.0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8DBDE")
fig.tight_layout()
fig.savefig(f"{FIG}/n6c_pay_index.pdf")
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
