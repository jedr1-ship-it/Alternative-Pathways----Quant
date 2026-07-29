import sys
sys.path.insert(0, "replication")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401
from scipy import stats
from adjustText import adjust_text

OUT = "report/figures_deck"
PT, LN, DARK, MUT = "#4A4F55", "#9C8033", "#2B2F33", "#8A9096"
FIPS = {1:"AL",2:"AK",4:"AZ",5:"AR",6:"CA",8:"CO",9:"CT",10:"DE",11:"DC",
        12:"FL",13:"GA",15:"HI",16:"ID",17:"IL",18:"IN",19:"IA",20:"KS",
        21:"KY",22:"LA",23:"ME",24:"MD",25:"MA",26:"MI",27:"MN",28:"MS",
        29:"MO",30:"MT",31:"NE",32:"NV",33:"NH",34:"NJ",35:"NM",36:"NY",
        37:"NC",38:"ND",39:"OH",40:"OK",41:"OR",42:"PA",44:"RI",45:"SC",
        46:"SD",47:"TN",48:"TX",49:"UT",50:"VT",51:"VA",53:"WA",54:"WV",
        55:"WI",56:"WY"}
ABBR2NAME = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas",
    "CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware",
    "DC":"District of Columbia","FL":"Florida","GA":"Georgia","HI":"Hawaii",
    "ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas",
    "KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland",
    "MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi",
    "MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada",
    "NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York",
    "NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma",
    "OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island",
    "SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas",
    "UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington",
    "WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
D = pd.read_csv("outputs/state_correlates.csv")
D["abbr"] = D["fips"].map(FIPS)
x, y = D["pension"], D["att_u55"]
r, p = stats.pearsonr(x, y)
b1, b0 = np.polyfit(x, y, 1)

LABEL = {"DC","MT","OR","HI","NE","WV","DE","KY","MO","MN","FL","AZ","MA",
         "CA","NY","WY","MS","CO","WA","AK"}

fig, ax = plt.subplots(figsize=(10.6, 6.2))
xs = np.linspace(x.min()-0.6, x.max()+0.6, 60)
yhat = b0 + b1*xs
n = len(x)
se_fit = np.sqrt(np.sum((y-b0-b1*x)**2)/(n-2)) * np.sqrt(
    1/n + (xs-x.mean())**2/np.sum((x-x.mean())**2))
ax.plot(xs, yhat, color=LN, lw=1.8, zorder=3)
ax.scatter(x, y, s=42, color=PT, alpha=0.92, edgecolors="white",
           linewidths=1.2, zorder=4)
texts = []
for _, rr in D.iterrows():
    if rr["abbr"] in LABEL:
        texts.append(ax.text(rr["pension"], rr["att_u55"],
                             ABBR2NAME[rr["abbr"]], fontsize=8.8,
                             color="#2B2F33"))
line_x = np.linspace(x.min()-0.5, x.max()+0.5, 80)
adjust_text(texts, ax=ax,
            x=np.concatenate([x.values, line_x]),
            y=np.concatenate([y.values, b0+b1*line_x]),
            expand=(1.35, 1.8),
            arrowprops=dict(arrowstyle="-", color="#C4C9CE", lw=0.6,
                            shrinkA=2, shrinkB=3))
tx = D[D["abbr"]=="TX"].iloc[0]
ax.annotate("Texas", (tx["pension"], tx["att_u55"]), xytext=(71.35, 6.05),
            fontsize=8.8, color="#111111",
            arrowprops=dict(arrowstyle="-", color="#C4C9CE", lw=0.6,
                            shrinkA=2, shrinkB=3))
ax.annotate("slope = $-$0.21 pp per point of coverage\n"
            "r = $-$0.47   (p < 0.001)   51 jurisdictions",
            (0.02, 0.045), xycoords="axes fraction", fontsize=10,
            color=DARK,
)
ax.set_xlabel("Teachers with a pension plan at the job, % (state mean, 1997-2024)",
              fontsize=10.5, color=DARK)
ax.set_ylabel("Teachers under 55 leaving per year, %", fontsize=10.5,
              color=DARK)
ax.tick_params(length=0, labelsize=9.5, colors=MUT)
ax.grid(color="#F3F4F5", lw=0.9)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#D8DBDE")
fig.tight_layout()
fig.savefig(f"{OUT}/pension_scatter_deck.pdf")
fig.savefig(f"{OUT}/pension_scatter_deck.png", dpi=200)
print("saved")
