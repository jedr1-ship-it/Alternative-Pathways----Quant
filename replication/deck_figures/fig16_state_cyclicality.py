import sys
sys.path.insert(0, "replication")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import paperstyle  # noqa: F401

BLUE, CORAL, TXT = "#2A5DB0", "#C4534B", "#3B4046"
OUT = "report/figures_deck"

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
xpos = np.arange(len(RC))

fig, ax = plt.subplots(figsize=(12.4, 5.6))
ax.axhline(0, color="#999999", lw=1.0)
for xv, (_, r) in zip(xpos, RC.iterrows()):
    c = (BLUE if r["beta_pp"] > 0 else CORAL) if r["sig"] else "#C4C9CE"
    ax.errorbar(xv, r["beta_pp"], yerr=1.96 * r["se_pp"], fmt="o",
                color=c, ms=5.2, elinewidth=1.2, capsize=0, zorder=4)
ax.set_xticks(xpos)
ax.set_xticklabels([NAMES_FULL[a] for a in RC["abbr"]], fontsize=7.6, color=TXT, rotation=90)
for tick, (_, r) in zip(ax.get_xticklabels(), RC.iterrows()):
    if r["sig"]:
        tick.set_fontweight("bold")
ax.set_xlim(-1, len(RC))
ax.set_ylim(-6, 6)
ax.set_ylabel("Change in the leaving rate (pp) per 1-pt\nhigher state unemployment",
              fontsize=10, color=TXT)
ax.tick_params(length=0)
ax.grid(axis="y", color="#F1F2F3", lw=1.0)
ax.set_axisbelow(True)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#D8DBDE")
fig.tight_layout()
fig.savefig(f"{OUT}/states_landscape.pdf")
fig.savefig(f"{OUT}/states_landscape.png", dpi=220)
print("saved", len(RC))
