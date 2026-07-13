"""
Replication of Aldeman & Yi (2025, Education Next), "Are Teachers
Abandoning Their Profession in Large Numbers?" -- the retrospective CPS
turnover measure (following Harris & Adams 2007).

Instrument (CPS ASEC, one survey): a person TAUGHT last year if the
occupation of the longest job held last year (OCCUP) is a teaching code;
she LEFT the profession if her current survey-week occupation (PEIOOCC) is
no longer a teaching code -- including PEIOOCC = -1 (not employed). This is
a leaver, not a mover (school/district switchers keep the same occupation).

The rate for calendar year Y is measured in the ASEC of year Y+1 (OCCUP
refers to the prior year). ASEC surveys 2016-2025 cover calendar 2015-2024.

Occupation coding changes from the 2010 Census scheme (surveys <=2019) to
the 2018 scheme (surveys >=2020). Codes 2300/2310/2320/2330 (preschool-K,
elementary-middle, secondary, special ed) are identical across both. "Other
teachers and instructors" is 2340 in the 2010 scheme and splits into
2350/2360 in the 2018 scheme; the era-consistent set handles this.

Targets (Aldeman & Yi): pooled 2015-2024 = 7.6%; nurses comparable (~7.6%).
"""
import glob
import numpy as np
import pandas as pd

CORE = {2300, 2310, 2320, 2330}


def teacher_codes(asec_year, broad):
    """K-12 teaching codes, optionally adding 'other teachers', per era."""
    if not broad:
        return CORE
    return CORE | ({2340} if asec_year <= 2019 else {2350, 2360})


df = pd.concat([pd.read_parquet(f) for f in
                sorted(glob.glob("data/raw/asec/asec_slim_*.parquet"))],
               ignore_index=True)
df["cal_year"] = df["asec_year"] - 1
print(f"loaded {len(df):,} person-rows, surveys "
      f"{df['asec_year'].min()}-{df['asec_year'].max()}")


def flag(d, broad=False):
    """Return (taught_last_year, left) boolean masks under era-correct codes."""
    taught = pd.Series(False, index=d.index)
    left = pd.Series(False, index=d.index)
    for ay, g in d.groupby("asec_year"):
        codes = teacher_codes(ay, broad)
        t = g["OCCUP"].isin(codes)
        taught.loc[g.index] = t
        left.loc[g.index] = t & ~g["PEIOOCC"].isin(codes)
    return taught, left


def rate(d, broad=False):
    taught, left = flag(d, broad)
    base = d[taught]
    if base.empty:
        return np.nan, 0
    lv = left[taught]
    return np.average(lv.astype(int), weights=base["MARSUPWT"]) * 100, len(base)


win = df[df["cal_year"].between(2015, 2024)]

print("\n=== pooled 2015-2024 ===")
for lab, broad in [("K-12 core (2300-2330)", False),
                   ("K-12 + other teachers", True)]:
    for aname, m in [("all ages", win["A_AGE"] >= 0),
                     ("age 21+", win["A_AGE"] >= 21)]:
        r, n = rate(win[m], broad)
        print(f"  {lab:24s} {aname:9s}: {r:5.2f}%   n={n:,}")

print("\n=== annual series (K-12 + other teachers, all ages) ===")
rows = []
for y in range(2015, 2025):
    r, n = rate(df[df["cal_year"] == y], broad=True)
    rows.append({"cal_year": y, "rate": round(r, 2), "n": n})
    print(f"  {y}: {r:5.2f}%   n={n:,}")
pd.DataFrame(rows).to_csv("outputs/aldeman_annual.csv", index=False)

# decompose the pooled leaver into occupation-switch vs not-employed
taught, left = flag(win, broad=True)
base = win[taught]
sw = base["PEIOOCC"] > 0
r_all = np.average(left[taught].astype(int), weights=base["MARSUPWT"]) * 100
r_sw = np.average((left[taught] & sw).astype(int),
                  weights=base["MARSUPWT"]) * 100
r_ne = np.average((left[taught] & ~sw).astype(int),
                  weights=base["MARSUPWT"]) * 100
print(f"\ndecomposition of {r_all:.2f}% pooled leaver rate:")
print(f"  switched to another occupation : {r_sw:.2f}%")
print(f"  not employed at survey week    : {r_ne:.2f}%")

print("\n=== comparison professions, pooled 2015-2024 (all ages) ===")
PROF = {"Teachers (K-12+other)": None,   # handled specially
        "Registered nurses": {3255},
        "Social workers": {2016, 2015, 2010, 2025},
        "Accountants and auditors": {800, 810},
        "Lawyers": {2100}}
prof_rows = []
for name, codes in PROF.items():
    if codes is None:
        r, n = rate(win, broad=True)
    else:
        base = win[win["OCCUP"].isin(codes)]
        lv = (~base["PEIOOCC"].isin(codes)).astype(int)
        r = np.average(lv, weights=base["MARSUPWT"]) * 100
        n = len(base)
    prof_rows.append({"profession": name, "rate": round(r, 2), "n": n})
    print(f"  {name:26s}: {r:5.2f}%   n={n:,}")
pd.DataFrame(prof_rows).to_csv("outputs/aldeman_professions.csv", index=False)

print("\n=== age gradient, pooled 2015-2024 (K-12+other) ===")
age_rows = []
for lo, hi, lab in [(21, 24, "21-24"), (25, 29, "25-29"), (30, 39, "30s"),
                    (40, 49, "40s"), (50, 59, "50s"), (60, 64, "60-64"),
                    (65, 120, "65+")]:
    r, n = rate(win[win["A_AGE"].between(lo, hi)], broad=True)
    age_rows.append({"age": lab, "rate": round(r, 2), "n": n})
    print(f"  {lab:6s}: {r:5.2f}%   n={n:,}")
pd.DataFrame(age_rows).to_csv("outputs/aldeman_age.csv", index=False)

# ----- headline: K-12 core rate with sampling CI, and public/private -----
print("\n=== HEADLINE: K-12 core teachers, pooled 2015-2024 ===")
taught, left = flag(win, broad=False)
base = win[taught]
w = base["MARSUPWT"].values
lv = left[taught].astype(int).values
p = np.average(lv, weights=w)
deff = 1.5                       # modest design effect for the ASEC
se = np.sqrt(deff * p * (1 - p) / len(base)) * 100
print(f"  turnover = {p*100:.2f}%   n={len(base):,}   "
      f"SE~{se:.2f}pp   95% CI [{p*100-1.96*se:.2f}, {p*100+1.96*se:.2f}]")
print(f"  Aldeman & Yi target: 7.6%  -> within CI: "
      f"{p*100-1.96*se <= 7.6 <= p*100+1.96*se}")

# public vs private, by class of worker on last year's longest job (LJCW):
#   1 private | 2 federal | 3 state | 4 local | 5 self-inc | 6 self-notinc
gov = base["LJCW"].isin([2, 3, 4])
priv = base["LJCW"] == 1
rp = np.average(lv[gov.values], weights=w[gov.values]) * 100
rv = np.average(lv[priv.values], weights=w[priv.values]) * 100
print(f"  public-school teachers : {rp:.2f}%   n={int(gov.sum()):,}")
print(f"  private-school teachers: {rv:.2f}%   n={int(priv.sum()):,}")

nb = win[win["OCCUP"].isin({3255})]
nurse = round(np.average((~nb["PEIOOCC"].isin({3255})).astype(int),
                         weights=nb["MARSUPWT"]) * 100, 2)
p_broad = rate(win, broad=True)[0]
# aldeman_yi source: CPS = their own CPS estimate; TFS = NCES figure they
# cite for context (administrative, not from the CPS -- not a CPS target).
summary = pd.DataFrame([
    {"quantity": "Teacher turnover, K-12 core codes, pooled 2015-2024",
     "replication": round(p*100, 2), "aldeman_yi": 7.6, "ay_source": "CPS"},
    {"quantity": "Teacher turnover, K-12 + other-teacher codes",
     "replication": round(p_broad, 2), "aldeman_yi": 7.6, "ay_source": "CPS"},
    {"quantity": "Registered nurses (comparable profession)",
     "replication": nurse, "aldeman_yi": 7.6, "ay_source": "CPS"},
    {"quantity": "public-school teachers (CPS class-of-worker)",
     "replication": round(rp, 2), "aldeman_yi": 7.9, "ay_source": "NCES TFS"},
    {"quantity": "private-school teachers (CPS class-of-worker)",
     "replication": round(rv, 2), "aldeman_yi": 11.7, "ay_source": "NCES TFS"},
])
summary.to_csv("outputs/aldeman_summary.csv", index=False)
print("\nwrote outputs/aldeman_summary.csv")
print(summary.to_string(index=False))
