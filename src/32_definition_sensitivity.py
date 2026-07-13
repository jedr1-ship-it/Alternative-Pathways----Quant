"""
How much does the retrospective ASEC turnover rate move as we CLEAN the
definition? Two levers:

  (1) which occupation codes count as "teacher"
  (2) which years -- restricted to a single, comparable Census occupation
      coding scheme, to avoid mixing 2010-scheme and 2018-scheme years

Census occupation scheme in the CPS/ASEC:
  surveys 2016-2019  (calendar 2015-2018) -> 2010 scheme
  surveys 2020-2025  (calendar 2019-2024) -> 2018 scheme

K-12 classroom teacher = 2300/2310/2320/2330 (identical in both schemes).
The adjacent codes are NOT K-12 teachers; teaching assistant is the only
genuine coder-confusion boundary. We show what including each does.
"""
import glob
import numpy as np
import pandas as pd

CORE = {2300, 2310, 2320, 2330}
OTHER = {2010: {2340}, 2018: {2350, 2360}}      # "other teachers / tutors"
ASSIST = {2010: {2540}, 2018: {2545}}           # teaching assistants


def scheme(asec_year):
    return 2010 if asec_year <= 2019 else 2018


df = pd.concat([pd.read_parquet(f) for f in
                sorted(glob.glob("data/raw/asec/asec_slim_*.parquet"))],
               ignore_index=True)
df["cal_year"] = df["asec_year"] - 1
df["scheme"] = df["asec_year"].map(scheme)


def codes_for(asec_year, defn):
    s = scheme(asec_year)
    c = set(CORE)
    if "other" in defn:
        c |= OTHER[s]
    if "assist" in defn:
        c |= ASSIST[s]
    return c


def rate(d, defn):
    num = den = n = 0.0
    for ay, g in d.groupby("asec_year"):
        c = codes_for(ay, defn)
        base = g[g["OCCUP"].isin(c)]
        left = (~base["PEIOOCC"].isin(c)).astype(int)
        num += (left * base["MARSUPWT"]).sum()
        den += base["MARSUPWT"].sum()
        n += len(base)
    return num / den * 100, int(n)


WINDOWS = [
    ("2010-scheme only (cal 2015-2018)", df[df["scheme"] == 2010]),
    ("2018-scheme only (cal 2019-2024)", df[df["scheme"] == 2018]),
    ("full decade (era-consistent codes)",
     df[df["cal_year"].between(2015, 2024)]),
]
DEFS = [("core K-12 (2300-2330)", "core"),
        ("core + teaching assistants", "core+assist"),
        ("core + other teachers/tutors", "core+other"),
        ("core + assistants + other", "core+assist+other")]

print(f"{'definition':32s} | " + " | ".join(f"{w[0][:26]:26s}" for w in WINDOWS))
print("-" * 120)
rows = []
for dl, dk in DEFS:
    cells = []
    for wl, wd in WINDOWS:
        r, n = rate(wd, dk)
        cells.append(f"{r:5.2f}% (n={n:,})")
        rows.append({"definition": dl, "window": wl, "rate": round(r, 2),
                     "n": n})
    print(f"{dl:32s} | " + " | ".join(f"{c:26s}" for c in cells))

pd.DataFrame(rows).to_csv("outputs/definition_sensitivity.csv", index=False)
print("\nAldeman & Yi target: 7.6%")
print("\nnote: the CLEAN number is core K-12 on a single scheme; adding "
      "adjacent\ncodes pulls in non-teachers and lifts the rate.")
