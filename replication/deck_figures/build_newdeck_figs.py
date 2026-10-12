"""Figures and the comparability table for the restructured deck that do
not need the extended ASEC file: the six-definitions chart, the single
cyclicality chart, the profession-comparability table, and the extended
professions chart with an all-other-professionals average line.
Run from the repo root."""
import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})

OUT = "report/figures_deck"
NAVY, BURG, INK, MUT = "#1F3864", "#7B2530", "#23373B", "#6B7480"
REDS = ["#C79AA0", "#A2606A", "#8A4450", "#7B2530"]

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.pdf")
    fig.savefig(f"{OUT}/{name}.png", dpi=180)
    plt.close(fig)
    print("saved", name)

# ================= 1. six definitions, one chart =================
L = pd.read_csv("outputs/definitions_ladder.csv")
L = L[L.base_year <= 2024]
fig, ax = plt.subplots(figsize=(12.0, 6.0))
series = [("single", REDS[0], "-", 1.6, "Single   17.5"),
          ("month_pairs", MUT, (0, (4, 2)), 1.6, "Month pairs   15.4"),
          ("pair", REDS[1], "-", 1.6, "Pair   13.4"),
          ("triple", REDS[2], "-", 1.6, "Triple   11.7"),
          ("strict", REDS[3], "-", 2.4, "Strict   10.5"),
          ("annual_recall", NAVY, "-", 2.6, "Annual recall   8.6")]
for col, c, ls, lw, lab in series:
    ax.plot(L.base_year, L[col], color=c, ls=ls, lw=lw)
    ax.annotate(lab, (2024.3, L[col].iloc[-1]), fontsize=12, color=c,
                va="center", fontweight="bold")
NC_Y, NC_V = [2008, 2012, 2021], [8.0, 7.7, 8.0]
ax.plot(NC_Y, NC_V, color=INK, ls="none", marker="o", ms=6, mfc=INK,
        mec="white", mew=1.1)
ax.annotate("NCES follow-up", (2021.4, 6.9), fontsize=10.5, color=INK)
ax.set_xlim(2004.5, 2030.5)
ax.set_ylim(0, 24)
ax.set_xticks(range(2005, 2025, 3))
ax.set_ylabel("teachers leaving per year, percent", fontsize=12, color=INK)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(labelsize=11)
fig.tight_layout()
save(fig, "defs6")

# ================= 2. one cyclicality chart =================
P = pd.read_csv("outputs/p_series.csv")
U = pd.read_csv("outputs/n_urate_official.csv")
D = P.merge(U, on="cal_year")
r = np.corrcoef(D.leaver_ba, D.urate)[0, 1]
fig, ax = plt.subplots(figsize=(12.0, 5.6))
ax.plot(D.cal_year, D.leaver_ba, color=NAVY, lw=2.6)
ax.plot(D.cal_year, D.urate, color=MUT, lw=1.8, ls=(0, (4, 2)))
ax.annotate(f"Teachers leaving   {D.leaver_ba.iloc[-1]:.1f}",
            (2024.3, D.leaver_ba.iloc[-1]), fontsize=12.5, color=NAVY,
            va="center", fontweight="bold")
ax.annotate(f"Unemployment rate   {D.urate.iloc[-1]:.1f}",
            (2024.3, D.urate.iloc[-1]), fontsize=12.5, color=MUT,
            va="center", fontweight="bold")
ax.annotate(f"correlation {r:+.2f}", (0.02, 0.93), xycoords="axes fraction",
            fontsize=11.5, color=INK)
ax.set_xlim(1996.5, 2031)
ax.set_ylim(0, 12.5)
ax.set_xticks(range(1997, 2025, 3))
ax.set_ylabel("percent", fontsize=12, color=INK)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(labelsize=11)
fig.tight_layout()
save(fig, "cycle1")

# ================= 3+4. professions: comparability + extended chart ====
M = pd.read_parquet("data/processed/asec_master.parquet",
                    columns=["asec_year", "cal_year", "OCCUP", "PEIOOCC",
                             "A_LFSR", "WGT", "ba_plus", "ma_plus",
                             "A_AGE", "female", "public_ly", "WKSWORK",
                             "WSAL_VAL"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
M = M[(M.ba_plus == 1) & (M.A_AGE >= 18) & M.WGT.notna()]

def prof_codes(ay):
    if ay <= 2002:
        return None
    rn = {3130} if ay <= 2010 else {3255, 3256, 3257, 3258}
    sw = {2010} if ay <= 2019 else {2011, 2012, 2013, 2014}
    md = {3060} if ay <= 2019 else {3090, 3100}
    return {
        "Teachers": {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360}),
        "Registered nurses": rn,
        "Social workers": sw,
        "Accountants": {800},
        "Lawyers": {2100},
        "Pharmacists": {3050},
        "Physicians": md,
        "Physical therapists": {3160},
        "Postsecondary teachers": {2200} if ay <= 2019 else {2205},
    }

M = M[M.asec_year >= 2003].copy()
M["in_prof"] = ""
for ay, g in M.groupby("asec_year"):
    sets = prof_codes(int(ay))
    for name, codes in sets.items():
        M.loc[g.index[g.OCCUP.isin(codes)], "in_prof"] = name
    M.loc[g.index, "_cur"] = g.PEIOOCC.where(g.PEIOOCC.notna(), -9)
    M.loc[g.index, "_cur_in"] = ""
    for name, codes in sets.items():
        M.loc[g.index[g.PEIOOCC.isin(codes)], "_cur_in"] = name

emp = M.A_LFSR.isin([1, 2])
M["left_prof"] = np.where(M.in_prof != "",
                          ((emp & (M._cur_in != M.in_prof)) | ~emp), np.nan)
# generic own-occupation exit, professional occupations only (codes < 3600)
pro = (M.in_prof == "") & (M.OCCUP < 3600) & M.OCCUP.notna()
M["left_own"] = np.where(pro, ((emp & (M.PEIOOCC != M.OCCUP)) | ~emp), np.nan)

# --- comparability table (pooled cal 2015-2024; wages cal 2020-2024)
rows = []
for name in ["Teachers", "Registered nurses", "Social workers", "Accountants"]:
    g = M[(M.in_prof == name) & M.cal_year.between(2015, 2024)]
    w = g.WGT
    def wm(s, cond=None):
        v = g if cond is None else g[cond]
        x = v[s].astype(float)
        k = x.notna()
        return np.average(x[k], weights=v.WGT[k])
    gw = g[g.cal_year.between(2020, 2024) & (g.WSAL_VAL > 0)].sort_values("WSAL_VAL")
    cw = gw.WGT.cumsum() / gw.WGT.sum()
    med = gw.loc[cw >= 0.5, "WSAL_VAL"].iloc[0]
    rows.append({"prof": name, "female": 100 * wm("female"),
                 "age": wm("A_AGE"), "ma_plus": 100 * wm("ma_plus"),
                 "public": 100 * wm("public_ly"), "weeks": wm("WKSWORK"),
                 "medwage": med, "n": len(g)})
C = pd.DataFrame(rows).set_index("prof")
C.to_csv("outputs/comparable_professions.csv")
print(C.round(1).to_string())

# --- extended chart: 9 professions + professional average, 3-yr MA
fig, ax = plt.subplots(figsize=(12.4, 6.4))
hl = {"Teachers": (NAVY, 2.8), "Registered nurses": ("#3E7C59", 1.5),
      "Social workers": ("#C4534B", 1.5), "Accountants": ("#9AA1A8", 1.5)}
ends = []
for name in prof_codes(2024):
    s = (M[M.in_prof == name].groupby("cal_year")
         .apply(lambda g: 100 * np.average(g.left_prof.astype(float),
                                           weights=g.WGT)))
    s = s[(s.index >= 2002) & (s.index <= 2024)].rolling(3, center=True).mean()
    c, lw = hl.get(name, ("#C3C9CF", 1.1))
    ax.plot(s.index, s.values, color=c, lw=lw)
    ends.append((name, s.dropna().iloc[-1], c, lw > 2 or name in hl))
oth = M[(M.in_prof != "") & (M.in_prof != "Teachers")]
s = (oth.groupby("cal_year")
     .apply(lambda g: 100 * np.average(g.left_prof.astype(float), weights=g.WGT)))
s = s[(s.index >= 2002) & (s.index <= 2024)].rolling(3, center=True).mean()
ax.plot(s.index, s.values, color=INK, lw=2.0, ls=(0, (4, 2)))
ends.append(("Average of the eight professions",
             s.dropna().iloc[-1], INK, True))
ends.sort(key=lambda t: -t[1])
yprev = None
for name, yv, c, strong in ends:
    y = yv if yprev is None else min(yv, yprev - 1.05)
    ax.annotate(f"{name}  {yv:.1f}", (2024.3, y), fontsize=10.5, color=c,
                va="center", fontweight="bold" if strong else "normal")
    yprev = y
ax.set_xlim(2002.5, 2033)
ax.set_ylim(0, 19)
ax.set_xticks(range(2003, 2025, 3))
ax.set_ylabel("leaving the occupation per year, percent (3-yr MA)",
              fontsize=11.5, color=INK)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(labelsize=11)
fig.tight_layout()
save(fig, "profs_ext")
print("done")
