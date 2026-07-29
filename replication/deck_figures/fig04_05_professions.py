import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

OUT = "report/figures_deck"
BLUE, CORAL, GREEN, GRAY, DARK = "#2A5DB0", "#C4534B", "#3E7C59", "#9AA1A8", "#3B4046"

def prof_codes(ay):
    if ay <= 2002:
        return {"Teachers": {155, 156, 157, 158, 159},
                "Registered nurses": {95},
                "Social workers": {174},
                "Accountants": {23}}
    rn = {3130} if ay <= 2010 else {3255, 3256, 3257, 3258}
    sw = {2010} if ay <= 2019 else {2011, 2012, 2013, 2014}
    return {"Teachers": {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360}),
            "Registered nurses": rn,
            "Social workers": sw,
            "Accountants": {800}}

M = pd.read_parquet("data/processed/asec_master.parquet",
                    columns=["asec_year", "OCCUP", "PEIOOCC", "A_LFSR",
                             "WGT", "ba_plus", "A_AGE", "female"])
for c in M.columns:
    M[c] = pd.to_numeric(M[c], errors="coerce")
M = M[(M["ba_plus"] == 1) & (M["A_AGE"] >= 18) & M["WGT"].notna()]

# person-level rows tagged by profession-year, then 3-yr pooled rates + CI
recs = []
for ay, g in M.groupby("asec_year"):
    emp = g["A_LFSR"].isin([1, 2])
    outlf = ~g["A_LFSR"].isin([1, 2, 3, 4])
    for prof, codes in prof_codes(int(ay)).items():
        b = g[g["OCCUP"].isin(codes)]
        if not len(b):
            continue
        stay = emp.loc[b.index] & b["PEIOOCC"].isin(codes)
        d = pd.DataFrame({"cal_year": int(ay) - 1, "prof": prof,
                          "w": b["WGT"].values,
                          "leave": (~stay).values.astype(float),
                          "female": b["female"].values,
                          "outlf": outlf.loc[b.index].values.astype(float)})
        recs.append(d)
L = pd.concat(recs, ignore_index=True)

def pooled(d, col):
    w, v = d["w"].values, d[col].values
    p = np.average(v, weights=w)
    neff = w.sum() ** 2 / (w ** 2).sum()
    se = np.sqrt(p * (1 - p) / neff)
    return p * 100, se * 100

rows = []
years = range(1997, 2025)
for prof in ["Teachers", "Registered nurses", "Social workers", "Accountants"]:
    dp = L[L["prof"] == prof]
    dpw = dp[dp["female"] == 1]
    for y in years:
        win = dp[dp["cal_year"].between(y - 1, y + 1)]
        winw = dpw[dpw["cal_year"].between(y - 1, y + 1)]
        if len(win) < 200:
            continue
        p, se = pooled(win, "leave")
        pw, sew = pooled(winw, "outlf")
        rows.append({"prof": prof, "cal_year": y, "leave": p, "se": se,
                     "lf": pw, "se_lf": sew})
P = pd.DataFrame(rows)

STYLE = {"Teachers": (BLUE, 2.6), "Registered nurses": (GREEN, 1.8),
         "Social workers": (CORAL, 1.8), "Accountants": (GRAY, 1.8)}

def draw(col, secol, ylab, title, fname, ymax, smooth=False, deck=False):
    fig, ax = plt.subplots(figsize=(9.4, 4.7))
    ends = {}
    for prof, (c, lw) in STYLE.items():
        d = P[P["prof"] == prof].sort_values("cal_year").copy()
        if smooth:
            for cc in (col, secol):
                d[cc] = d[cc].rolling(3, center=True, min_periods=2).mean()
        ax.fill_between(d["cal_year"], d[col] - 1.96 * d[secol],
                        d[col] + 1.96 * d[secol], color=c, alpha=0.11,
                        lw=0)
        ax.plot(d["cal_year"], d[col], color=c, lw=lw,
                solid_capstyle="round")
        ends[prof] = d[col].iloc[-1]
    order = sorted(ends, key=ends.get)
    ys = sorted(ends.values())
    gap = ymax * 0.055
    for i in range(1, len(ys)):
        if ys[i] - ys[i - 1] < gap:
            ys[i] = ys[i - 1] + gap
    for prof, y in zip(order, ys):
        ax.text(2025.3, y, f"{prof}  {ends[prof]:.1f}%", fontsize=9.4,
                color=STYLE[prof][0], va="center",
                fontweight="bold" if prof == "Teachers" else "normal")
    ax.set_xlim(1996.4, 2033.5)
    ax.set_ylim(0, ymax)
    ax.set_xticks(range(1998, 2025, 2))
    ax.set_xticklabels(range(1998, 2025, 2), fontsize=8.4, rotation=45)
    ax.set_ylabel(ylab, fontsize=10, color=DARK)
    ax.tick_params(length=0, labelsize=9)
    ax.grid(axis="y", color="#F1F2F3", lw=1.0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8DBDE")
    if not deck:
        ax.set_title(title, fontsize=12.5, color=DARK, pad=12)
    fig.tight_layout()
    fig.savefig(f"{OUT}/{fname}.pdf")
    fig.savefig(f"{OUT}/{fname}.png", dpi=200)

T1 = "Rates of Leaving the Occupation, Teachers vs. Comparable Professions, 1997-2024"
T2 = "Labor Force Exit of Women, Teachers vs. Comparable Professions, 1997-2024"
draw("leave", "se", "Percent leaving the occupation", T1, "leave_professions_full", 18)
draw("lf", "se_lf", "Percent of women leaving the labor force", T2, "lf_professions_full", 9, smooth=True)
draw("leave", "se", "Percent leaving the occupation", T1, "leave_professions_deck", 18, deck=True)
draw("lf", "se_lf", "Percent of women leaving the labor force", T2, "lf_professions_deck", 9, smooth=True, deck=True)
print(P[P.prof == "Teachers"][["cal_year", "leave", "se"]].tail(3).round(2).to_string(index=False))
