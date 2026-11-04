"""Figure on teachers' aides for the Former Teachers working paper, in the
layout of OECD Education at a Glance (same style as fig_oecd_former_teachers.py).

Indicator: share of teachers' aides among contact staff (teachers' aides plus
classroom teachers), full-time equivalents, all educational institutions,
primary education, 2014 and 2024.

Data: INES-UOE data collection on educational personnel, OECD Data Explorer,
dataflows OECD.EDU.IMEP DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_RAW_INST2
("Number of teacher aides") and @DF_UOE_NF_PERS_RAW_INST ("Number of
classroom teachers and academic staffs by type of institution"). The same
calculation for pre-primary education in 2023 reproduces EAG 2025 Table D2.1,
column 7, for every country with data (checked in check_against_d21()).

Run from the repository root:
    python3 replication/deck_figures/fig_oecd_teacher_aides.py
The extract is cached in report/former_teachers/figures/figure_aides_data.csv.
"""
import io
import os
import urllib.request
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle

OUT = "report/former_teachers/figures"
CACHE = f"{OUT}/figure_aides_data.csv"
API = "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@{}/{}"
LEVELS = ["ISCED11_02", "ISCED11_1", "ISCED11_2", "ISCED11_3"]


# ---------------------------------------------------------------- data
def fetch(flow, measure):
    # key: REF_AREA.EDUCATION_LEV.MEASURE.EDUCATION_TYPE.INTENSITY....; filter after download
    req = urllib.request.Request(API.format(flow, "all"), headers={
        "Accept": "application/vnd.sdmx.data+csv;version=2.0.0",
        "User-Agent": "curl/8.5.0"})
    d = pd.read_csv(io.BytesIO(urllib.request.urlopen(req, timeout=600).read()), dtype=str)
    d = d[(d.MEASURE == measure) & (d.EDUCATION_TYPE == "FE") & (d.INTENSITY == "_T")
          & (d.SEX == "_T") & (d.INST_TYPE_EDU == "INST_EDU") & (d.UNIT_MEASURE == "PS_FTE")
          & d.EDUCATION_LEV.isin(LEVELS)]
    d["v"] = pd.to_numeric(d.OBS_VALUE, errors="coerce")
    return d[["REF_AREA", "EDUCATION_LEV", "TIME_PERIOD", "v"]].dropna()


if os.path.exists(CACHE):
    D = pd.read_csv(CACHE, dtype={"TIME_PERIOD": int})
else:
    a = fetch("DF_UOE_NF_PERS_RAW_INST2", "AIDE").rename(columns={"v": "aides_fte"})
    t = fetch("DF_UOE_NF_PERS_RAW_INST", "TEACH").rename(columns={"v": "teachers_fte"})
    D = a.merge(t, on=["REF_AREA", "EDUCATION_LEV", "TIME_PERIOD"])
    D["TIME_PERIOD"] = D["TIME_PERIOD"].astype(int)
    D["share_aides"] = 100 * D.aides_fte / (D.aides_fte + D.teachers_fte)
    D = D.sort_values(["EDUCATION_LEV", "REF_AREA", "TIME_PERIOD"])
    D.to_csv(CACHE, index=False, float_format="%.3f")


def check_against_d21():
    """EAG 2025 Table D2.1 col. 7 (pre-primary, 2023), rounded as published."""
    d21 = {"AUT": 38, "CHL": 59, "CZE": 10, "DNK": 42, "DEU": 14, "HUN": 47,
           "JPN": 10, "LTU": 36, "NLD": 22, "NOR": 59, "SVK": 5, "SVN": 45,
           "SWE": 55, "GBR": 86, "USA": 25, "BRA": 15, "ROU": 5}
    s = D[(D.EDUCATION_LEV == "ISCED11_02") & (D.TIME_PERIOD == 2023)].set_index("REF_AREA")
    bad = {k: round(s.share_aides[k], 1) for k, v in d21.items()
           if round(s.share_aides[k]) != v}
    assert not bad, bad


check_against_d21()

NAMES = {"BGR": "Bulgaria", "BRA": "Brazil", "CAN": "Canada", "CHL": "Chile",
         "COL": "Colombia", "CZE": "Czechia", "DNK": "Denmark", "FIN": "Finland",
         "GBR": "United Kingdom", "HUN": "Hungary", "IRL": "Ireland", "ISL": "Iceland",
         "LTU": "Lithuania", "NLD": "Netherlands", "NOR": "Norway", "PER": "Peru",
         "ROU": "Romania", "SVK": "Slovak Republic", "SWE": "Sweden",
         "USA": "United States"}
P = D[D.EDUCATION_LEV == "ISCED11_1"].pivot_table(index="REF_AREA", columns="TIME_PERIOD",
                                                   values="share_aides")
rows = []
for c, r in P.iterrows():
    if pd.isna(r.get(2024)):
        continue
    base, flag = (r.get(2014), "") if pd.notna(r.get(2014)) else \
                 ((r.get(2015), "1") if pd.notna(r.get(2015)) else (None, ""))
    rows.append((NAMES[c] + flag, r[2024], base))
rows.sort(key=lambda x: -x[1])
pd.DataFrame(rows, columns=["country", "share_2024", "share_2014"]).to_csv(
    f"{OUT}/figure_aides_primary.csv", index=False, float_format="%.1f")

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
NAVY, BLUE = "#002F6C", "#006BB6"
W_IN = 16.4 / 2.54

fig, ax = plt.subplots(figsize=(W_IN, 3.4))
for i, (n, v, b) in enumerate(rows):
    ax.bar(i, v, 0.6, color=BLUE, lw=0)
    if b is not None:
        ax.scatter(i, b, marker="D", s=16, color="white", edgecolor=NAVY, lw=0.9, zorder=4)
ax.set_ylim(0, 50)
ax.set_yticks(range(0, 51, 5))
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)
ax.text(-0.005, 1.02, "%", transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5)
ax.set_xticks(range(len(rows)))
ax.set_xticklabels([r[0] for r in rows], rotation=45, ha="right", rotation_mode="anchor",
                   fontsize=7.2)
ax.set_xlim(-0.6, len(rows) - 0.4)
h = [Rectangle((0, 0), 1, 1, color=BLUE),
     plt.Line2D([0], [0], marker="D", ls="", markersize=4, markerfacecolor="white",
                markeredgecolor=NAVY, markeredgewidth=0.9)]
ax.add_patch(Rectangle((0, 1.06), 1, 0.11, transform=ax.transAxes, clip_on=False,
                       facecolor="#F1F1F1", edgecolor="none"))
ax.legend(h, ["2024", "2014"], loc="center", bbox_to_anchor=(0.5, 1.115), ncol=2,
          frameon=False, fontsize=7, handlelength=0.9, handleheight=0.9,
          columnspacing=3.0)
fig.subplots_adjust(left=0.06, right=0.995, top=0.85, bottom=0.23)
fig.savefig(f"{OUT}/figure_teacher_aides.png")
plt.close(fig)
for r in rows:
    print(f"{r[0]:<20} {r[1]:5.1f}  {'' if r[2] is None else round(r[2], 1)}")
print("font", NARROW)
