"""State-level attrition levels (teachers under 55), landscape bar chart.
Writes report/figures_deck/states_level.pdf. Run from the repo root."""
import sys
sys.path.insert(0, "replication")
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})

NAVY, BURG, INK, MUT = "#1F3864", "#7B2530", "#1A2430", "#6B7480"
FIPS = {1:"AL",2:"AK",4:"AZ",5:"AR",6:"CA",8:"CO",9:"CT",10:"DE",11:"DC",
        12:"FL",13:"GA",15:"HI",16:"ID",17:"IL",18:"IN",19:"IA",20:"KS",
        21:"KY",22:"LA",23:"ME",24:"MD",25:"MA",26:"MI",27:"MN",28:"MS",
        29:"MO",30:"MT",31:"NE",32:"NV",33:"NH",34:"NJ",35:"NM",36:"NY",
        37:"NC",38:"ND",39:"OH",40:"OK",41:"OR",42:"PA",44:"RI",45:"SC",
        46:"SD",47:"TN",48:"TX",49:"UT",50:"VT",51:"VA",53:"WA",54:"WV",
        55:"WI",56:"WY"}

d = pd.read_csv("outputs/state_correlates.csv")
d["st"] = d.fips.map(FIPS)
d = d.sort_values("att_u55").reset_index(drop=True)
mean = (d.att_u55 * d.n_t).sum() / d.n_t.sum()

fig, ax = plt.subplots(figsize=(13.0, 5.6))
colors = [BURG if v >= d.att_u55.iloc[-6] else
          (NAVY if v <= d.att_u55.iloc[5] else "#C9CFD6") for v in d.att_u55]
ax.bar(range(len(d)), d.att_u55, color=colors, width=0.78)
ax.axhline(mean, color=INK, lw=1.0, ls=(0, (4, 3)))
ax.annotate(f"national mean  {mean:.1f}", (1.0, mean + 0.25),
            fontsize=11, color=INK)
ax.set_xticks(range(len(d)))
ax.set_xticklabels(d.st, fontsize=8.5, rotation=90, color=INK)
ax.set_ylabel("teachers under 55 leaving per year, percent", fontsize=11.5,
              color=INK)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#F1F2F3", lw=1)
ax.set_axisbelow(True)
ax.tick_params(axis="y", labelsize=10)
ax.set_xlim(-0.8, len(d) - 0.2)
fig.tight_layout()
fig.savefig("report/figures_deck/states_level.pdf")
print("saved states_level.pdf")
