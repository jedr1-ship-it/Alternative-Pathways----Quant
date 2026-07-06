"""
Link state-year education quality (NAEP grade-8 mathematics, official state
scores from the Nation's Report Card data service) with teacher attrition
by state. Produces fig16_naep.pdf and outputs/naep_state_scores.csv.
"""
import json
import time
import urllib.request
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from covariates import load_panel

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

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA",
          "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
          "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX",
          "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
YEARS = [2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2022, 2024]

rows = []
for yr in YEARS:
    url = ("https://www.nationsreportcard.gov/Dataservice/GetAdhocData.aspx"
           "?type=data&subject=mathematics&grade=8&subscale=MRPCM"
           f"&variable=TOTAL&jurisdiction={','.join(STATES)}"
           f"&stattype=MN:MN&Year={yr}")
    with urllib.request.urlopen(url, timeout=120) as r:
        d = json.load(r)
    for row in d.get("result", []):
        if row.get("isStatDisplayable"):
            rows.append({"state": row["jurisdiction"], "year": row["year"],
                         "naep_m8": row["value"]})
    print(f"NAEP {yr}: {len(d.get('result', []))} states", flush=True)
    time.sleep(1)
naep = pd.DataFrame(rows)
naep.round(2).to_csv("outputs/naep_state_scores.csv", index=False)

FIPS = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT",
        10: "DE", 11: "DC", 12: "FL", 13: "GA", 15: "HI", 16: "ID",
        17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
        23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS",
        29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ",
        35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
        41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN",
        48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV",
        55: "WI", 56: "WY"}

df = load_panel()
B = df[df["sampleB"]].copy()
B["state"] = B["GESTFIPS_0"].map(FIPS)
att = (B.groupby("state")
        .apply(lambda g: pd.Series(
            {"attr": np.average(g["leaver_p"], weights=g["PWSSWGT_0"]) * 100,
             "n": len(g)}), include_groups=False)
        .reset_index())
sc = att.merge(naep.groupby("state")["naep_m8"].mean().reset_index(),
               on="state")
r = np.corrcoef(sc["naep_m8"], sc["attr"])[0, 1]
print(f"\nstates: {len(sc)}, corr(NAEP, attrition) = {r:.2f}")
sc.round(2).to_csv("outputs/naep_vs_attrition.csv", index=False)

fig, ax = plt.subplots(figsize=(6.8, 3.8))
ax.scatter(sc["naep_m8"], sc["attr"], s=sc["n"] / 60, color=BLUE,
           alpha=0.75, edgecolor=SURFACE, linewidth=1.2, zorder=3)
b1, b0 = np.polyfit(sc["naep_m8"], sc["attr"], 1, w=sc["n"])
xs = np.linspace(sc["naep_m8"].min() - 1, sc["naep_m8"].max() + 1, 20)
ax.plot(xs, b0 + b1 * xs, color=CORAL, lw=2, zorder=2)
for s in ["CT", "MS", "NV", "MA", "TX", "FL", "WY"]:
    row = sc[sc["state"] == s]
    if not row.empty:
        ax.annotate(s, (row["naep_m8"].iat[0], row["attr"].iat[0]),
                    textcoords="offset points", xytext=(6, 4), fontsize=8.5,
                    color=SUBTLE)
ax.set_xlabel("NAEP grade-8 mathematics, average scale score (2005--2024)")
ax.set_ylabel("Persistent attrition, %")
ax.tick_params(length=0)
fig.tight_layout()
fig.savefig("report/figures/fig16_naep.pdf")
print("fig16 saved; slope per 10 NAEP points:", round(b1 * 10, 2), "pp")
