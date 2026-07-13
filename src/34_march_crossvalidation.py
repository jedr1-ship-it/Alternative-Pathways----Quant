"""
Robustness: for the SAME individuals, does the March retrospective leaver
measure agree with a point-in-time matched-panel measure?

The ASEC (March CPS) carries PERIDNUM, the CPS person identifier, so the
re-interviewed half of the sample links from one March to the next. Linking
ASEC 2023 <-> ASEC 2024 by PERIDNUM gives, for each linked person:

  PEIOOCC_2023  current occupation, March 2023  (from ASEC 2023)
  PEIOOCC_2024  current occupation, March 2024  (from ASEC 2024)
  OCCUP_2024    longest job in 2023             (from ASEC 2024, retrospective)

Two leaver measures on the same people (base = teacher):
  retrospective (Harris-Adams): OCCUP_2024 teacher & PEIOOCC_2024 not teacher
  matched point-in-time       : PEIOOCC_2023 teacher & PEIOOCC_2024 not teacher

This isolates the instrument: same persons, same 12-month window.
"""
import os
import zipfile
import urllib.request
import numpy as np
import pandas as pd

RAW = "data/raw/asec"
CORE = {2300, 2310, 2320, 2330}
COLS = ["PERIDNUM", "OCCUP", "PEIOOCC", "A_AGE", "A_SEX", "A_HGA",
        "MARSUPWT"]
URL = ("https://www2.census.gov/programs-surveys/cps/datasets/"
       "{y}/march/asecpub{yy}csv.zip")


def get(yy):
    out = f"{RAW}/asec_id_{yy}.parquet"
    if os.path.exists(out):
        return pd.read_parquet(out)
    z = f"{RAW}/asec{yy}.zip"
    if not os.path.exists(z):
        urllib.request.urlretrieve(URL.format(y=2000 + yy, yy=yy), z)
    zf = zipfile.ZipFile(z)
    name = [n for n in zf.namelist()
            if os.path.basename(n).startswith("pppub")][0]
    p = f"{RAW}/{os.path.basename(name)}"
    with zf.open(name) as s, open(p, "wb") as d:
        d.write(s.read())
    df = pd.read_csv(p, usecols=COLS, dtype={"PERIDNUM": str})
    df.to_parquet(out, index=False)
    os.remove(p)
    os.remove(z)
    return df


def teach(col, codes=CORE):
    return col.isin(codes)


a23 = get(23).add_suffix("_23").rename(columns={"PERIDNUM_23": "PERIDNUM"})
a24 = get(24).add_suffix("_24").rename(columns={"PERIDNUM_24": "PERIDNUM"})
m = a23.merge(a24, on="PERIDNUM")
# validate the link: same sex, age advancing 0-2 years
m = m[(m["A_SEX_23"] == m["A_SEX_24"])
      & (m["A_AGE_24"] - m["A_AGE_23"]).between(0, 2)]
print(f"ASEC 2023 persons : {len(a23):,}")
print(f"ASEC 2024 persons : {len(a24):,}")
print(f"linked & validated: {len(m):,}  "
      f"({len(m)/len(a24)*100:.0f}% of the 2024 file)\n")

# --- retrospective base: taught in 2023 per OCCUP_24 (longest job last year)
R = m[teach(m["OCCUP_24"])].copy()
R["left"] = ~teach(R["PEIOOCC_24"])
r_rate = np.average(R["left"], weights=R["MARSUPWT_24"]) * 100

# --- matched point-in-time base: teacher in March 2023 per PEIOOCC_23
P = m[teach(m["PEIOOCC_23"])].copy()
P["left"] = ~teach(P["PEIOOCC_24"])
p_rate = np.average(P["left"], weights=P["MARSUPWT_24"]) * 100

print("=== leaver rate on the SAME linked people, two instruments ===")
print(f"retrospective (OCCUP_2023 -> PEIOOCC_2024) : {r_rate:5.2f}%  "
      f"n={len(R):,}")
print(f"matched Mar23 -> Mar24 (PEIOOCC point-in-time): {p_rate:5.2f}%  "
      f"n={len(P):,}")

# --- agreement among people flagged teacher by BOTH bases
both = m[teach(m["OCCUP_24"]) & teach(m["PEIOOCC_23"])].copy()
both["retro_leaver"] = ~teach(both["PEIOOCC_24"])          # identical outcome
# where the two BASES disagree on who was a teacher
only_retro = m[teach(m["OCCUP_24"]) & ~teach(m["PEIOOCC_23"])]
only_pit = m[~teach(m["OCCUP_24"]) & teach(m["PEIOOCC_23"])]
print("\n=== who each instrument counts as a base-year teacher ===")
print(f"both agree teacher      : {len(both):,}")
print(f"only retrospective says : {len(only_retro):,}  "
      "(longest-2023-job teacher, but NOT teaching March 2023)")
print(f"only point-in-time says : {len(only_pit):,}  "
      "(teaching March 2023, but longest-2023-job not teacher)")

# destinations of the retrospective leavers (switch vs not employed)
sw = np.average((R["left"] & (R["PEIOOCC_24"] > 0)),
                weights=R["MARSUPWT_24"]) * 100
ne = np.average((R["left"] & (R["PEIOOCC_24"] <= 0)),
                weights=R["MARSUPWT_24"]) * 100
print(f"\nretrospective leaver split: switch {sw:.2f} | not-employed {ne:.2f}")

pd.DataFrame([{"instrument": "retrospective March", "rate": round(r_rate, 2),
               "n": len(R)},
              {"instrument": "matched Mar->Mar point-in-time",
               "rate": round(p_rate, 2), "n": len(P)}]).to_csv(
    "outputs/march_crossvalidation.csv", index=False)

# --- individual-level confusion matrix: OUR prospective label vs the
# retrospective answer, on people teaching in March 2023 (our base) ---
base = m[teach(m["PEIOOCC_23"])].copy()
base["our"] = np.where(teach(base["PEIOOCC_24"]), "our_STAYER", "our_LEAVER")
base["retro"] = np.where(teach(base["OCCUP_24"]),
                         "retro_teacher_2023", "retro_not_teacher_2023")
conf = pd.crosstab(base["our"], base["retro"], margins=True)
print("\n=== confusion matrix (base = teaching March 2023) ===")
print(conf.to_string())
L = base[base["our"] == "our_LEAVER"]
S = base[base["our"] == "our_STAYER"]
print(f"\nour leavers confirmed by retrospective : "
      f"{teach(L['OCCUP_24']).mean()*100:.0f}%  (n={len(L)})")
print(f"our stayers confirmed by retrospective : "
      f"{teach(S['OCCUP_24']).mean()*100:.0f}%  (n={len(S)})")
conf.to_csv("outputs/march_confusion_matrix.csv")
