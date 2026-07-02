"""
Evolution of teacher attrition 2005-2024 and short-run return to teaching,
overall and by gender. Produces fig6 (two panels) + CSV.

Return measure: a leaver observed out of teaching at t+12 (MIS 5-7) is
re-observed in up to three following monthly interviews (until MIS 8);
'returns' = teaching again in any of them. The CPS rotation design caps the
observable return window at ~3 months, so this is short-run churn, not
lifetime re-entry. Leavers with MIS 8 at t+12 have no follow-up and are
excluded from the return denominator.
"""
import glob
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

BLUE, CORAL, GRAY = "#2a78d6", "#e34948", "#8a8f98"
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

INTDIR = "data/interim"
TEACHER_OCC = {2300, 2310, 2320, 2330}
KEY = ["HRHHID", "HRHHID2", "PULINENO"]

df = pd.read_csv("data/processed/cps_teacher_panel.csv",
                 dtype={"HRHHID": str, "HRHHID2": str})
df["female"] = (df["PESEX_0"] == 2).astype(int)
w = "PWSSWGT_0"

# ---------- follow-up teacher status for leavers ----------
lv = df[(df["leaver"] == 1) & (df["HRMIS_1"] < 8)].copy()
lv["fid"] = np.arange(len(lv))

# expected follow-up (year, month, mis) rows for each leaver
rows = []
for k in range(1, 4):
    e = lv[lv["HRMIS_1"] + k <= 8][
        ["fid"] + KEY + ["HRMONTH", "base_year", "HRMIS_1"]].copy()
    if e.empty:
        continue
    mo = e["HRMONTH"] + k
    e["HRYEAR4"] = e["base_year"] + 1 + (mo > 12).astype(int)
    e["HRMONTH"] = np.where(mo > 12, mo - 12, mo)
    e["HRMIS"] = e["HRMIS_1"] + k
    rows.append(e.drop(columns=["base_year", "HRMIS_1"]))
exp = pd.concat(rows, ignore_index=True)

# teacher status lookup for the needed months (MIS 6-8 only)
need = exp[["HRYEAR4", "HRMONTH"]].drop_duplicates()
frames = []
for _, (yr, mo) in need.iterrows():
    fs = glob.glob(f"{INTDIR}/cps_{yr}{mo:02d}.parquet")
    if not fs:
        continue
    d = pd.read_parquet(
        fs[0], columns=KEY + ["HRYEAR4", "HRMONTH", "HRMIS", "PEMLR",
                              "PTIO1OCD", "PESEX"])
    d = d[d["HRMIS"].between(6, 8)]
    d["tch"] = (d["PEMLR"].isin([1, 2])
                & d["PTIO1OCD"].isin(TEACHER_OCC)).astype(int)
    frames.append(d[KEY + ["HRYEAR4", "HRMONTH", "HRMIS", "tch", "PESEX"]])
look = pd.concat(frames, ignore_index=True)

m = exp.merge(look, on=KEY + ["HRYEAR4", "HRMONTH", "HRMIS"], how="inner")
# guard against household churn: same sex as at baseline
m = m.merge(lv[["fid", "PESEX_0"]], on="fid")
m = m[m["PESEX"] == m["PESEX_0"]]
obs = m.groupby("fid").agg(n_obs=("tch", "size"), returned=("tch", "max"))
lv = lv.merge(obs, on="fid", how="left")
lv_obs = lv[lv["n_obs"].notna()].copy()   # at least one observed follow-up

print(f"leavers total                    : {(df['leaver']==1).sum():,}")
print(f"leavers with observed follow-up  : {len(lv_obs):,}")
ret_w = np.average(lv_obs["returned"], weights=lv_obs[w])
print(f"return to teaching (<=3 months)  : {ret_w:6.2%}")
for g, name in [(1, "women"), (0, "men")]:
    s = lv_obs[lv_obs["female"] == g]
    print(f"  {name:6s}: {np.average(s['returned'], weights=s[w]):6.2%}")

# ---------- yearly series ----------
def wavg(d, col):
    return np.average(d[col], weights=d[w]) * 100

years = sorted(df["base_year"].unique())
ev = []
for y in years:
    dy = df[df["base_year"] == y]
    ly = lv_obs[lv_obs["base_year"] == y]
    ev.append({
        "base_year": y,
        "attr_all": wavg(dy, "leaver"),
        "attr_f": wavg(dy[dy.female == 1], "leaver"),
        "attr_m": wavg(dy[dy.female == 0], "leaver"),
        "ret_all": wavg(ly, "returned"),
        "ret_f": wavg(ly[ly.female == 1], "returned"),
        "ret_m": wavg(ly[ly.female == 0], "returned"),
        "n": len(dy), "n_lv_obs": len(ly),
    })
ev = pd.DataFrame(ev)
ev.round(2).to_csv("outputs/evolution_by_year_gender.csv", index=False)
print("\n", ev.round(1).to_string(index=False))

# ---------- figure: two panels ----------
fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.4))
for ax, (a_f, a_m, title) in zip(axes, [
        ("attr_f", "attr_m", "Leaving teaching within 12 months, %"),
        ("ret_f", "ret_m", "Leavers back in teaching within 3 months, %")]):
    ax.plot(ev.base_year, ev[a_f], color=CORAL, lw=2, solid_capstyle="round")
    ax.plot(ev.base_year, ev[a_m], color=BLUE, lw=2, solid_capstyle="round")
    for col, c in [(a_f, CORAL), (a_m, BLUE)]:
        ax.scatter([ev.base_year.iloc[-1]], [ev[col].iloc[-1]], s=42,
                   color=c, zorder=4, edgecolor=SURFACE, linewidth=2)
        ax.text(ev.base_year.iloc[-1] + 0.4, ev[col].iloc[-1],
                f"{ev[col].iloc[-1]:.0f}%", va="center", fontsize=9.5,
                color=INK, fontweight="bold")
    ax.set_title(title, loc="left", fontsize=10.5, color=NAVY,
                 fontweight="bold", pad=8)
    ax.set_xlim(2004.5, 2027)
    ax.set_ylim(0, None)
    ax.set_xticks([2005, 2010, 2015, 2020, 2024])
    ax.tick_params(length=0)
    ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
handles = [plt.Line2D([], [], color=c, lw=2) for c in (CORAL, BLUE)]
axes[0].legend(handles, ["Women", "Men"], loc="lower left", frameon=False,
               fontsize=9)
axes[0].text(2020, axes[0].get_ylim()[1] * 0.95, "COVID", ha="center",
             fontsize=8, color=SUBTLE)
fig.tight_layout(w_pad=2.5)
fig.savefig("report/figures/fig6_evolution.pdf")
print("\nsaved report/figures/fig6_evolution.pdf, outputs/evolution_by_year_gender.csv")
