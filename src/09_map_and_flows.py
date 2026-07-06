"""
Geography and destination dynamics:
  - fig13_dest_time.pdf : leavers to another occupation vs out of the labor
    force, evolving by base year
  - fig14_map.pdf       : US state map, teachers as a share of employment
"""
import glob
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from covariates import load_panel

BLUE, CORAL, GOLD, GRAY = "#2a78d6", "#e34948", "#eda100", "#8a8f98"
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
TEACHER_OCC = {2300, 2310, 2320, 2330}

# ---------- fig13: where leavers go, over time ----------
df = load_panel()
B = df[df["sampleB"]].copy()
W = "PWSSWGT_0"
rows = []
for y, g in B.groupby("base_year"):
    w = g[W].sum()
    rows.append({
        "year": y,
        "occ": g.loc[(g.leaver_p == 1) & (g.dest == "other occupation"), W].sum() / w * 100,
        "olf": g.loc[(g.leaver_p == 1) & (g.dest == "out of labor force"), W].sum() / w * 100,
        "unemp": g.loc[(g.leaver_p == 1) & (g.dest == "unemployed"), W].sum() / w * 100,
    })
d = pd.DataFrame(rows)
d.round(2).to_csv("outputs/destinations_by_year.csv", index=False)

fig, ax = plt.subplots(figsize=(6.9, 3.3))
series = [("occ", CORAL, "Move to another occupation"),
          ("olf", GOLD, "Leave the labor force"),
          ("unemp", GRAY, "Become unemployed")]
for col, c, lab in series:
    ax.plot(d.year, d[col], color=c, lw=2, solid_capstyle="round")
    ax.scatter([d.year.iloc[-1]], [d[col].iloc[-1]], s=40, color=c,
               zorder=4, edgecolor=SURFACE, linewidth=2)
    ax.text(d.year.iloc[-1] + 0.4, d[col].iloc[-1], f"{d[col].iloc[-1]:.0f}%",
            va="center", fontsize=9.5, color=INK, fontweight="bold")
handles = [plt.Line2D([], [], color=c, lw=2) for _, c, _ in series]
ax.legend(handles, [lab for *_, lab in series], loc="upper center",
          bbox_to_anchor=(0.5, 1.16), ncols=3, frameon=False, fontsize=8.5)
ax.axvspan(2019.5, 2020.5, color="#e9ebee", zorder=0)
ax.set_ylim(0, None)
ax.set_xticks([2005, 2010, 2015, 2020, 2024])
ax.set_xlim(2004.5, 2026.5)
ax.set_ylabel("% of teachers per year")
ax.tick_params(length=0)
fig.tight_layout()
fig.savefig("report/figures/fig13_dest_time.pdf")
plt.close(fig)
print("fig13 saved; 2024:", d.iloc[-1].round(1).to_dict())

# ---------- fig14: US map, teachers as % of employment by state ----------
FIPS = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT",
        10: "DE", 11: "DC", 12: "FL", 13: "GA", 15: "HI", 16: "ID",
        17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
        23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS",
        29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ",
        35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
        41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN",
        48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV",
        55: "WI", 56: "WY"}
acc = {}
for f in sorted(glob.glob("data/interim/cps_202[1-5]??.parquet")):
    d = pd.read_parquet(f, columns=["PEMLR", "PTIO1OCD", "PEEDUCA",
                                    "GESTFIPS", "PWSSWGT"])
    e = d[d["PEMLR"].isin([1, 2])]
    t = e[e["PTIO1OCD"].isin(TEACHER_OCC) & (e["PEEDUCA"] >= 43)]
    for fips, g in e.groupby("GESTFIPS"):
        a = acc.setdefault(fips, [0.0, 0.0])
        a[0] += g["PWSSWGT"].sum()
    for fips, g in t.groupby("GESTFIPS"):
        acc[fips][1] += g["PWSSWGT"].sum()
st = pd.DataFrame([{"state": FIPS[k], "share": v[1] / v[0] * 100}
                   for k, v in acc.items() if k in FIPS])
st.round(3).to_csv("outputs/teacher_share_by_state.csv", index=False)
print("state share range:", st.share.min().round(2), "-",
      st.share.max().round(2))

import json
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable

ABBR2NAME = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona",
             "AR": "Arkansas", "CA": "California", "CO": "Colorado",
             "CT": "Connecticut", "DE": "Delaware",
             "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
             "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
             "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
             "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
             "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan",
             "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
             "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
             "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
             "NY": "New York", "NC": "North Carolina", "ND": "North Dakota",
             "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
             "PA": "Pennsylvania", "RI": "Rhode Island",
             "SC": "South Carolina", "SD": "South Dakota",
             "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
             "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
             "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}
NAME2SHARE = dict(zip(st["state"].map(ABBR2NAME), st["share"]))
gj = json.load(open("data/raw/us_states.geojson"))

cmap = LinearSegmentedColormap.from_list(
    "ec_blues", ["#eef4fc", "#8db6e6", "#3873bd", "#0d2a4a"])
# clip the tails so mid-range differences get more color intensity
norm = Normalize(vmin=np.percentile(st["share"], 5),
                 vmax=np.percentile(st["share"], 95), clip=True)


def draw(ax, names):
    patches, vals = [], []
    for ft in gj["features"]:
        nm = ft["properties"]["name"]
        if nm not in names or nm not in NAME2SHARE:
            continue
        geom = ft["geometry"]
        polys = ([geom["coordinates"]] if geom["type"] == "Polygon"
                 else geom["coordinates"])
        for poly in polys:
            patches.append(MplPolygon(np.asarray(poly[0]), closed=True))
            vals.append(NAME2SHARE[nm])
    pc = PatchCollection(patches, edgecolor=SURFACE, linewidth=0.6)
    pc.set_array(np.asarray(vals))
    pc.set_cmap(cmap); pc.set_norm(norm)
    ax.add_collection(pc)
    ax.autoscale()
    ax.set_aspect(1.25)
    ax.axis("off")


lower48 = [n for n in NAME2SHARE if n not in ("Alaska", "Hawaii")]
fig = plt.figure(figsize=(7.6, 4.4))
ax = fig.add_axes([0.02, 0.06, 0.82, 0.92]); draw(ax, lower48)
axk = fig.add_axes([0.03, 0.05, 0.20, 0.24]); draw(axk, ["Alaska"])
axk.set_xlim(-180, -128)
axh = fig.add_axes([0.26, 0.04, 0.12, 0.14]); draw(axh, ["Hawaii"])
axh.set_xlim(-161, -154)
cax = fig.add_axes([0.88, 0.22, 0.022, 0.56])
cb = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cax)
cb.set_label("Teachers, % of employed", fontsize=9, color=SUBTLE)
cb.ax.tick_params(labelsize=9, length=0)
cb.outline.set_visible(False)
fig.savefig("report/figures/fig14_map.pdf")
plt.close(fig)
print("fig14 saved; top:", st.nlargest(3, 'share')[['state', 'share']].round(2).to_dict('records'))
