import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import sys
sys.path.insert(0, "replication")
from paperstyle import BLUE, CORAL, GOLD, GREEN, GRAY, INK, SUBTLE

FIG = "report/figures"
LIGHT = "#AEC3DE"
DARK = "#3D4754"
TXT5 = TXT5b = TXT6 = "#3B4046"
MUT5 = MUT5b = MUT6 = "#8A9096"


def h1(v):
    return f"{math.floor(v * 10 + 0.5) / 10:.1f}"


def despine(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# Figure 1. Composition of the Teaching Workforce, 2005-2024
WF = pd.read_csv("outputs/p_workforce.csv").sort_values("cal_year")
panels = [("age", "Mean age (years)", 2005), ("female", "Female", 2005),
          ("ma_plus", "Master's or higher", 2005),
          ("black", "Black", 2005),
          ("child_u6", "Child under 6", 2005),
          ("public", "Public school", 2005),
          ("parttime", "Part-time", 2005),
          ("pension", "Pension plan", 2005)]
fig, axes = plt.subplots(2, 4, figsize=(11.8, 5.6))
for axp, (v, lab, start) in zip(axes.flat, panels):
    d = WF[(WF["cal_year"] >= start) & WF[v].notna()]
    y = d[v].astype(float).reset_index(drop=True)
    xs = d["cal_year"].reset_index(drop=True)
    sm3 = y.rolling(3, center=True, min_periods=2).mean()
    axp.plot(xs, y, color="#BBBBBB", lw=1.0)
    axp.plot(xs, sm3, color=BLUE, lw=2.2)
    i13 = xs == 2013
    axp.plot(xs[i13], y[i13], "o", mfc="white", mec=GRAY, ms=4)
    axp.set_title(lab, fontsize=10, color=INK, pad=6)
    lo, hi = y.min(), y.max()
    pad = max((hi - lo) * 0.35, 0.8)
    axp.set_ylim(lo - pad, hi + pad * 1.7)
    dec = 1 if v == "age" else 0
    suf = "" if v == "age" else "%"
    x0, y0 = xs.iloc[0], sm3.iloc[0]
    x1, y1 = xs.iloc[-1], sm3.iloc[-1]
    axp.plot([x0, x1], [y0, y1], "o", color=BLUE, ms=5.5, zorder=5)
    rising0 = sm3.iloc[min(2, len(sm3) - 1)] > sm3.iloc[0]
    off0 = (2, -16) if rising0 else (2, 10)
    axp.annotate(f"{y0:.{dec}f}{suf}", (x0, y0), xytext=off0,
                 textcoords="offset points", ha="left", fontsize=8.8,
                 color=BLUE, fontweight="bold")
    axp.annotate(f"{y1:.{dec}f}{suf}", (x1, y1), xytext=(-2, 10),
                 textcoords="offset points", ha="right", fontsize=8.8,
                 color=BLUE, fontweight="bold")
    axp.set_xlim(2003.6, 2025.4)
    axp.set_xticks(range(2006, 2025, 2))
    axp.set_xticklabels([str(t) for t in range(2006, 2025, 2)],
                        fontsize=6.6, rotation=45)
    axp.tick_params(axis="y", labelsize=8)
    axp.grid(axis="y", color="#EFEFEF", lw=0.6)
    axp.set_axisbelow(True)
    despine(axp)
fig.tight_layout(h_pad=2.4)
fig.savefig(f"{FIG}/g1_workforce.pdf")
plt.close(fig)


# Figure 2. Leaving Teaching, 1997-2024
S = pd.read_csv("outputs/p_series.csv").sort_values("cal_year")
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
ax.text(2019.5, 12.3, "Covid", ha="center", fontsize=8.5, color=SUBTLE)

ok = S["leaver_ba"].notna()
main = S[ok]
mean_ba = np.average(main["leaver_ba"])
ax.fill_between(main["cal_year"], main["leaver_ba"] - 1.96 * main["se_ba"],
                main["leaver_ba"] + 1.96 * main["se_ba"], color=BLUE,
                alpha=0.07, lw=0)
ax.axhline(mean_ba, color=INK, lw=0.9, ls=":", zorder=1)
ax.text(2014.0, 6.55, f"1997\u20132024 average: {mean_ba:.1f}",
        fontsize=8, color=INK, ha="center", va="top")
ax.plot(main["cal_year"], main["leaver_ba"], color=BLUE, lw=2.4)
last = main.iloc[-1]
pk = main.loc[main["leaver_ba"].idxmax()]
cov = main.loc[main["cal_year"] == 2019].iloc[0]
for r in (last, pk, cov):
    ax.plot(r["cal_year"], r["leaver_ba"], "o", color=BLUE, ms=5)
    ax.annotate(f"{r['leaver_ba']:.1f}", (r["cal_year"], r["leaver_ba"]),
                xytext=(0, 9), textcoords="offset points", ha="center",
                fontsize=9, color=BLUE, fontweight="bold")
ax.set_ylim(0, 13)
ax.set_xlim(1996, 2025.5)
ax.set_xticks(range(1998, 2025, 2))
ax.set_xticklabels([str(t) for t in range(1998, 2025, 2)], fontsize=8,
                   rotation=45)
ax.set_ylabel("Percent leaving teaching")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g2_evolution.pdf")
plt.close(fig)


# Figure 3. Destinations of Teachers Who Leave the Profession
F = pd.read_csv("outputs/p_flow100_leavers.csv", index_col=0).iloc[:, 0]
DG = pd.read_csv("outputs/q_dest_groups.csv").set_index("group")[
    "per100_leavers"]
emp = F["education and care job"] + F["other occupation"]
edu_job = (DG["Postsecondary teaching"]
           + DG["School support (tutor, assistant, library)"]
           + DG["Education administration"])
care = DG["Counseling, social work, childcare"]
otherprof = DG["Management and business"] + DG["Other professional"]
salesetc = (DG["Office and administrative support"]
            + DG["Sales and personal service"]
            + DG["Production, transport, other"] + DG["Unclassified"])
fig, ax = plt.subplots(figsize=(9.6, 4.6))
Y1, Y0, H = 1.72, 0.55, 0.34
top = [("Employed", emp, BLUE),
       ("Out of the labor force, 55+", F["out of LF, 55plus"], LIGHT),
       ("Out of the labor force, <55", F["out of LF, under 55"], GOLD),
       ("Unemployed", F["unemployed"], "#6E6E6E")]
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
    ax.text(x + w / 2, Y0, f"{v:.0f}", ha="center", va="center",
            color="white", fontsize=10.5, fontweight="bold")
    ax.text(x + w / 2, Y0 - H / 2 - 0.10, lab, ha="center", va="top",
            fontsize=8.8, color=INK)
    x += w

ax.plot([0, 0], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE, lw=1.0)
ax.plot([emp, 100], [Y1 - H / 2, Y0 + H / 2], ls=":", color=SUBTLE,
        lw=1.0)
ax.text(-1.2, Y1, "Of every 100\nleavers", ha="right", va="center",
        fontsize=9.6, color=INK)
ax.text(-1.2, Y0, "What the employed\nare doing", ha="right", va="center",
        fontsize=9.6, color=INK)

ec = edu_job + care
xb = ec * sc
yb = Y0 - H / 2 - 0.52
ax.plot([0, 0, xb, xb], [yb + 0.05, yb, yb, yb + 0.05], color=INK, lw=1.1)
ax.text(xb / 2, yb - 0.07,
        f"{ec:.0f} of every 100 leavers keep working in education or care",
        ha="center", va="top", fontsize=9.6, color=INK,
        fontweight="bold")
ax.set_xlim(-14, 101)
ax.set_ylim(-0.35, 2.35)
ax.axis("off")
fig.tight_layout()
fig.savefig(f"{FIG}/g3_flow100.pdf")
plt.close(fig)


# Figure 4. Leaving Teaching by Age and Route
R5 = pd.read_csv("outputs/p_routes_age.csv")
x = np.arange(len(R5))
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.stackplot(x, R5["switch"], R5["unemp"], R5["leftlf"],
             colors=[GOLD, GRAY, BLUE], alpha=0.92)
ax.plot(x, R5["total"], color=INK, lw=1.5)
for i in (0, 5, len(R5) - 1):
    ax.annotate(f"{R5['total'].iloc[i]:.0f}%", (i, R5["total"].iloc[i]),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=8.6, color=INK, fontweight="bold")
last = len(R5) - 1
y0 = R5["switch"].iloc[last]
y1 = y0 + R5["unemp"].iloc[last]
y2 = y1 + R5["leftlf"].iloc[last]
for lab, ym, c in [("to another job", y0 / 2, "#7A5B00"),
                   ("unemployed", (y0 + y1) / 2, "#555555"),
                   ("out of the labor force", (y1 + y2) / 2, BLUE)]:
    ax.annotate(lab, (last + 0.15, ym), fontsize=9, color=c, va="center",
                annotation_clip=False)
ax.set_xticks(x)
ax.set_xticklabels(R5["age"], fontsize=8.6)
ax.set_xlim(-0.3, last + 2.3)
ax.set_ylabel("Percent leaving, by route")
ax.set_xlabel("Age group")
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g4_routes_age.pdf")
plt.close(fig)


# Figure 5. Exit Routes by School Sector
SEC = pd.read_csv("outputs/p_sector_routes.csv").set_index("sector")
labels = ["To another job", "Unemployed", "Out of the\nlabor force"]
xs3 = np.arange(3)
fig, ax = plt.subplots(figsize=(6.6, 3.9))
for tag, c, off in [("public", BLUE, -0.17), ("private", CORAL, 0.17)]:
    vals = [SEC.loc[tag, k] for k in ("job", "unemp", "outlf")]
    ax.bar(xs3 + off, vals, width=0.34, color=c, label=tag.capitalize())
    for xi, v in zip(xs3 + off, vals):
        ax.annotate(f"{v:.1f}", (xi, v), xytext=(0, 3),
                    textcoords="offset points", ha="center", fontsize=9,
                    color=c, fontweight="bold")
ax.set_xticks(xs3)
ax.set_xticklabels(labels, fontsize=9.2)
ax.legend(frameon=False, fontsize=9)
ax.set_ylim(0, 6.4)
ax.set_ylabel("Percent of teachers, 2015–2024", fontsize=10)
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g10_sector_routes.pdf")
plt.close(fig)


# Figure 6. The Effect of a New Baby on Leaving, by Profession
NB = pd.read_csv("outputs/p_newbaby.csv").sort_values("AME_newbaby_pp")
NB["sig"] = NB["AME_newbaby_pp"].abs() > 1.96 * NB["se_pp"]
fig, ax = plt.subplots(figsize=(7.6, 4.4))
cols9 = [BLUE if p == "Teachers" else
         ("#5B6570" if s else "#D5D9DD")
         for p, s in zip(NB["prof"], NB["sig"])]
ax.barh(NB["prof"], NB["AME_newbaby_pp"], color=cols9, height=0.6)
ax.errorbar(NB["AME_newbaby_pp"], NB["prof"], xerr=1.96 * NB["se_pp"],
            fmt="none", ecolor=INK, elinewidth=0.9, capsize=2.5)
for i, (_, r) in enumerate(NB.iterrows()):
    ax.text(r["AME_newbaby_pp"] + 1.96 * r["se_pp"] + 0.45, i,
            f"+{r['AME_newbaby_pp']:.1f}", fontsize=9, va="center",
            color=BLUE if r["prof"] == "Teachers" else
            ("#3B4046" if r["sig"] else SUBTLE),
            fontweight="bold" if r["sig"] else "normal")
for tick, prof in zip(ax.get_yticklabels(), NB["prof"]):
    if prof == "Teachers":
        tick.set_fontweight("bold"); tick.set_color(BLUE)
ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-6, 14.5)
ax.set_xlabel("Effect of a new baby on P(a woman leaves her profession), pp")
ax.grid(axis="x", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g8_newbaby.pdf")
plt.close(fig)


# Figure 7. Labor Force Exit of Women Teachers, With and Without Young Children
MO = pd.read_csv("outputs/p_mothers.csv").pivot(
    index="cal_year", columns="grp", values="rate").reset_index()
for c in ("mom", "nomom"):
    MO[c + "_s"] = MO[c].rolling(3, center=True, min_periods=2).mean()
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.plot(MO["cal_year"], MO["mom"], color="#F2C9C4", lw=1.0)
ax.plot(MO["cal_year"], MO["nomom"], color="#CCCCCC", lw=1.0)
ax.plot(MO["cal_year"], MO["mom_s"], color=CORAL, lw=2.4)
ax.plot(MO["cal_year"], MO["nomom_s"], color=GRAY, lw=2.2)
ax.annotate("with a child under 6", (2003.3, 10.6), fontsize=9.5,
            color=CORAL, fontweight="bold", ha="center")
ax.annotate("without a child under 6", (2012.6, 0.7), fontsize=9.5,
            color=GRAY, fontweight="bold", ha="center")
for c, col in [("mom_s", CORAL), ("nomom_s", GRAY)]:
    for i in (0, len(MO) - 1):
        ax.plot(MO["cal_year"].iloc[i], MO[c].iloc[i], "o", color=col,
                ms=5)
        ax.annotate(f"{MO[c].iloc[i]:.1f}%",
                    (MO["cal_year"].iloc[i], MO[c].iloc[i]),
                    xytext=(0, 9), textcoords="offset points",
                    ha="center", fontsize=8.8, color=col,
                    fontweight="bold")
ax.set_ylim(0, 13.5)
ax.set_xlim(1996.2, 2024.9)
ax.set_xticks(range(1998, 2025, 2))
ax.set_xticklabels([str(t) for t in range(1998, 2025, 2)], fontsize=8,
                   rotation=45)
ax.set_ylabel("Percent leaving the labor force")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g9_mothers.pdf")
plt.close(fig)


# Figure 8. Leaving Teaching and the Unemployment Rate, 1997-2024
S5 = pd.read_csv("outputs/p_series.csv").sort_values("cal_year")
U = pd.read_csv("outputs/n_urate_official.csv")
M = S5.merge(U[["cal_year", "urate"]], on="cal_year")
M = M[M["leaver_ba"].notna()].sort_values("cal_year").reset_index(
    drop=True)
M = M.rename(columns={"leaver_ba": "leave", "rate_switch": "switch",
                      "rate_unemp": "unemp", "rate_leftlf": "leftlf"})


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


# Figure 9. Leaving and State Unemployment: Two Examples
FIPS_NAME = {37: "North Carolina", 34: "New Jersey"}
SS = pd.read_csv("outputs/p_state_series.csv")
SU = pd.read_csv("outputs/n_urate_states.csv")
SC = pd.read_csv("outputs/p_state_cycl.csv").set_index("GESTFIPS")
TXT5b, MUT5b = "#3B4046", "#8A9096"
fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9), sharey=True)


for ax, fips in zip(axes, FIPS_NAME):
    L = SS[SS["GESTFIPS"] == fips].copy()
    u = SU[SU["GESTFIPS"] == fips].copy()
    u["cal_year"] = u["survey_year"] - 1
    L = L.merge(u[["cal_year", "u_march"]], on="cal_year")

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


# Figure 10. The Distribution of Earnings Changes: Stayers and Leavers
DM = pd.read_csv("outputs/p_dlog_micro.csv")
STd = DM.loc[DM["group"] == "stayer", "dlog"]
LVd = DM.loc[DM["group"] == "leaver_employed", "dlog"]
NAVY6, RED6 = "#33526E", "#B04A42"
fig, ax = plt.subplots(figsize=(8.8, 4.6))
xg = np.linspace(-160, 210, 500)
ys_ = gaussian_kde(STd, bw_method=0.25)(xg)
yl_ = gaussian_kde(LVd, bw_method=0.25)(xg)
ax.fill_between(xg, 0, ys_, color="#E2E7EC", alpha=0.9, zorder=2)
ax.fill_between(xg, 0, yl_, color="#F3DCD8", alpha=0.75, zorder=3)
ax.plot(xg, ys_, color=NAVY6, lw=2.4, solid_capstyle="round", zorder=4)
ax.plot(xg, yl_, color=RED6, lw=2.4, solid_capstyle="round", zorder=5)
for d, c, yy in [(STd, NAVY6, ys_), (LVd, RED6, yl_)]:
    med = np.median(d)
    ax.plot([med, med], [0, np.interp(med, xg, yy)], color=c, lw=1.1,
            ls=(0, (3, 2)), zorder=6)
ax.annotate("Stayers", (12, 0.0146), fontsize=11, color=NAVY6,
            fontweight="bold")
ax.annotate("median +3", (12, 0.0134), fontsize=8.8, color=NAVY6)
ax.annotate("Leavers, employed", (68, 0.0054), fontsize=11,
            color=RED6, fontweight="bold")
ax.annotate("median +15", (68, 0.0042), fontsize=8.8, color=RED6)
ax.annotate("24% lose big", (-92, 0.0035), fontsize=9, color=RED6,
            ha="center", fontweight="bold")
ax.annotate("45% win big", (146, 0.0035), fontsize=9, color=RED6,
            ha="center", fontweight="bold")
ax.set_xlim(-160, 210)
ax.set_ylim(0, 0.0175)
ax.set_yticks([])
ax.set_xticks([-150, -100, -50, 0, 50, 100, 150, 200])
ax.set_xlabel("Change in annual earnings, log points ×100",
              fontsize=10, color=TXT6)
ax.tick_params(labelsize=9, length=0, colors=MUT6)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8DBDE")
fig.tight_layout()
fig.savefig(f"{FIG}/g5b_earnings_density.pdf")
plt.close(fig)


# Figure 11. Real Median Earnings by Profession, 2004-2014 and 2015-2025
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


# Figure 12. Average Marginal Effects on the Probability of Leaving Teaching
M = pd.read_csv("outputs/p_ame.csv")
M = M[~M["var"].isin(["age2"])]
BLOCKS = [("Job attachment", ["fullyear", "parttime"], BLUE),
          ("Compensation", ["pension", "public"], GREEN),
          ("Family", ["new_baby", "child_u6", "n_children", "married",
                      "sepdiv"], CORAL),
          ("Demographics", ["A_AGE", "female", "black", "ma_plus"], DARK)]
NAMES = {"fullyear": "Worked full year (50+ wks)",
         "parttime": "Part-time (<35 h/wk)", "pension": "Pension plan",
         "public": "Public school", "new_baby": "New baby this year",
         "child_u6": "Child under 6", "n_children": "Number of children",
         "married": "Married", "sepdiv": "Separated/divorced",
         "A_AGE": "Age (per year)", "female": "Female", "black": "Black",
         "ma_plus": "Master's+"}


Mi = M.set_index("var")
rows = []
for bl, vs, c in BLOCKS:
    rows.append(("head", bl, c))
    for v in vs:
        rows.append(("var", v, c))
    rows.append(("gap", None, None))
rows = rows[:-1]
ypos = np.arange(len(rows))[::-1]
fig, ax = plt.subplots(figsize=(8.0, 6.0))
ax.axvline(0, color="#999999", lw=1.0)
ylabels = []
for yv, (kind, payload, c) in zip(ypos, rows):
    if kind == "head":
        ylabels.append(payload)
        continue
    if kind == "gap":
        ylabels.append("")
        continue
    r = Mi.loc[payload]
    s = abs(r["AME_pp"]) > 1.96 * r["se_pp"]
    ax.errorbar(r["AME_pp"], yv, xerr=1.96 * r["se_pp"], fmt="o",
                color=c, ms=6.5, elinewidth=1.4, capsize=3,
                mfc=c if s else "white", mew=1.6)
    ax.annotate(f"{r['AME_pp']:+.1f}", (r["AME_pp"], yv), xytext=(0, 7),
                textcoords="offset points", ha="center", fontsize=8,
                color="#3B4046")
    ylabels.append(NAMES[payload])
ax.set_yticks(ypos)
ax.set_yticklabels(ylabels, fontsize=9.2)
for tick, (kind, payload, c) in zip(ax.get_yticklabels(), rows):
    if kind == "head":
        tick.set_fontweight("bold")
        tick.set_color(c)
        tick.set_fontsize(9.6)
ax.tick_params(axis="y", length=0)
ax.set_xlim(-10.6, 7)
ax.set_ylim(ypos[-1] - 0.7, ypos[0] + 0.9)
ax.set_xticks([-9, -6, -3, 0, 3, 6])
ax.set_xlabel("Average marginal effect on P(leave teaching), pp   "
              "(filled: significant at 5%)", fontsize=9.5)
ax.grid(axis="x", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{FIG}/g6_ame.pdf")
plt.close(fig)


# Figure 13. Rates of Leaving by Profession, 2004-2014 and 2015-2025
P = pd.read_csv("outputs/p_prof_windows.csv")
piv = P.pivot(index="prof", columns="window", values="leave")
piv = piv.sort_values("2015-2025")
W1, W2L = "2004-2014", "2015-2025"
fig, ax = plt.subplots(figsize=(8.0, 4.6))
y = np.arange(len(piv))
for i, (prof, r) in enumerate(piv.iterrows()):
    c = BLUE if prof == "Teachers" else GRAY
    ax.plot([r[W1], r[W2L]], [i, i], color=c, lw=1.8, alpha=0.75,
            zorder=2)
    ax.plot(r[W1], i, "o", color=c, ms=6.5, mfc="white", zorder=3)
    ax.plot(r[W2L], i, "o", color=c, ms=7.5, zorder=3)
    lower = r[W2L] < r[W1]
    ax.annotate(h1(r[W2L]), (r[W2L], i), textcoords="offset points",
                xytext=(-9, -3) if lower else (9, -3),
                ha="right" if lower else "left", fontsize=8.7, color=c,
                fontweight="bold" if prof == "Teachers" else "normal")
ax.set_yticks(y)
ax.set_yticklabels(piv.index, fontsize=9.6)
for tick, prof in zip(ax.get_yticklabels(), piv.index):
    if prof == "Teachers":
        tick.set_fontweight("bold")
        tick.set_color(BLUE)
hnd = [plt.Line2D([], [], marker="o", color=GRAY, mfc="white", ls=""),
       plt.Line2D([], [], marker="o", color=GRAY, ls="")]
ax.legend(hnd, ["Surveys 2004–2014", "Surveys 2015–2025"],
          frameon=False, fontsize=8.8, loc="lower right")
ax.set_xlabel("Percent leaving the profession per year")
ax.grid(axis="x", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/g7_professions.pdf")
plt.close(fig)


# Appendix Figure 14. Route Composition of Leavers, 1997-2024
RT = pd.read_csv("outputs/p_routes.csv").sort_values("cal_year")
ROUTES = ["employed", "outlf_55", "outlf_u55", "unemployed"]
RLAB = {"employed": "Employed elsewhere",
        "outlf_55": "Out of the labor force, 55+",
        "outlf_u55": "Out of the labor force, <55",
        "unemployed": "Unemployed"}
RCOL = {"employed": BLUE, "outlf_55": LIGHT, "outlf_u55": GOLD,
        "unemployed": "#5B6570"}
RTs = RT.copy()
for rt in ROUTES:
    RTs[rt] = RT[rt].rolling(3, center=True, min_periods=2).mean()
tot_s = RTs[ROUTES].sum(axis=1)
for rt in ROUTES:
    RTs[rt] = RTs[rt] / tot_s * 100
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.stackplot(RTs["cal_year"], [RTs[rt] for rt in ROUTES],
             colors=[RCOL[rt] for rt in ROUTES], alpha=0.92)
rylab = {"employed": 15, "outlf_55": 48, "outlf_u55": 77,
         "unemployed": 95}
for rt in ROUTES:
    ax.text(2025.2, rylab[rt], RLAB[rt], fontsize=8.6,
            color=RCOL[rt] if rt != "outlf_55" else "#7A96B8",
            va="center", fontweight="bold")
ax.set_xlim(1997, 2024)
ax.set_ylim(0, 100)
ax.set_xticks(range(1998, 2025, 2))
ax.set_xticklabels([str(t) for t in range(1998, 2025, 2)], fontsize=8,
                   rotation=45)
ax.set_ylabel("Share of leavers")
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/gapp_routes_evolution.pdf", bbox_inches="tight")
plt.close(fig)


# Appendix Figure 15. State-Level Cyclicality of Leaving, All 51 Jurisdictions
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


# Appendix Figure 16. Leaving Rates in Five Professions, Annual Series
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


# Appendix Figure 17. Real Median Earnings by Profession, Indexed to 2002
PP = pd.read_csv("outputs/p_pay_profs.csv")
IDX_STYLE = {"Teachers": (BLUE, 2.6, "-"),
             "All college graduates": (INK, 1.8, (0, (5, 3))),
             "Registered nurses": ("#3E7C59", 1.6, "-"),
             "Social workers": ("#C9A227", 1.6, "-"),
             "Accountants": ("#8D87A8", 1.6, "-"),
             "Lawyers": ("#B0B6BC", 1.6, "-")}
fig, ax = plt.subplots(figsize=(8.4, 4.4))
endy = {}
for prof, (c, lw, ls) in IDX_STYLE.items():
    d = PP[PP["prof"] == prof].sort_values("cal_year")
    sm = d["real_med"].rolling(3, center=True, min_periods=2).mean()
    idx = sm / sm.iloc[0] * 100
    ax.plot(d["cal_year"], idx, color=c, lw=lw, ls=ls)
    endy[prof] = idx.iloc[-1]
order6 = sorted(endy, key=endy.get)
ys6 = sorted(endy.values())
for i in range(1, len(ys6)):
    if ys6[i] - ys6[i - 1] < 1.6:
        ys6[i] = ys6[i - 1] + 1.6
for prof, y in zip(order6, ys6):
    ax.text(2024.6, y, f"{prof}  {endy[prof]:.0f}", fontsize=8.8,
            color=IDX_STYLE[prof][0], va="center",
            fontweight="bold" if prof == "Teachers" else "normal")
ax.axhline(100, color="#CCCCCC", lw=0.8)
ax.set_xticks(range(2002, 2025, 4))
ax.set_xlim(2002, 2034.5)
ax.set_ylabel("Real median earnings, 2002 = 100\n(full-time full-year, "
              "3-yr avg)", fontsize=9.6, color=TXT6)
ax.tick_params(labelsize=9, length=0, colors=MUT6)
ax.grid(axis="y", color="#F1F2F3", lw=1.0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8DBDE")
fig.tight_layout()
fig.savefig(f"{FIG}/napp_pay_index.pdf")
plt.close(fig)


# Appendix Figure 18. The Leaving Series under Alternative Definitions
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.axvspan(2018.6, 2020.4, color="#F4F4F4", zorder=0)
ax.plot(S["cal_year"], S["leaver_oldstyle"], color=GRAY, lw=1.4, ls="--",
        marker="s", ms=3.2)
ax.plot(S["cal_year"], S["leaver_all"], color=GRAY, lw=1.4, marker="s",
        ms=3.2)
ax.plot(S["cal_year"], S["leaver_ba"], color=BLUE, lw=2.0, marker="o",
        ms=4.0)
ax.annotate("all teachers, full definition (weighted)", (2014.5, 12.8),
            fontsize=8.4, color=GRAY, ha="center")
ax.annotate("harmonized: occupation pairs only, unweighted\n"
            "(identical construction in every year)", (2003.4, 6.1),
            fontsize=8.2, color=GRAY, ha="center")
ax.annotate("college graduates, full definition", (2018.6, 5.4),
            fontsize=8.6, color=BLUE, fontweight="bold", ha="center")
ax.set_ylim(0, 14)
ax.set_xlim(1996, 2025.5)
ax.set_ylabel("Percent leaving teaching")
ax.grid(axis="y", color="#EFEFEF", lw=0.6)
ax.set_axisbelow(True)
despine(ax)
fig.tight_layout()
fig.savefig(f"{FIG}/gapp_evolution_layers.pdf")
plt.close(fig)
