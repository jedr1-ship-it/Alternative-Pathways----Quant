"""
Build a linked 12-month CPS panel of school teachers (2024 -> 2025).

Source: official Current Population Survey basic monthly public-use microdata,
downloaded from https://www2.census.gov/programs-surveys/cps/datasets/<year>/basic/
(files <mon><yy>pub.dat.gz, fixed-width; positions from the 2025 record layout).

CPS rotation design (4-8-4): a household interviewed in month-in-sample (MIS)
1-4 of month t is re-interviewed exactly 12 months later with MIS 5-8. We link
persons across the year via (HRHHID, HRHHID2, PULINENO) and validate the match
with sex, race, and an age increase of 0-2 years (Madrian-Lefgren criterion).

Teachers = employed with primary-job occupation (2020 Census codes):
  2300 preschool/kindergarten, 2310 elementary/middle, 2320 secondary,
  2330 special education.
"""
import glob
import gzip
import os
import numpy as np
import pandas as pd

RAWDIR = "data/raw/cps"
OUTDIR = "data/processed"
os.makedirs(OUTDIR, exist_ok=True)

# (name, start, end) 1-indexed inclusive, from 2025 Basic CPS record layout
COLS = [
    ("HRHHID",   1, 15,  str),
    ("HRMONTH", 16, 17,  int),
    ("HRYEAR4", 18, 21,  int),
    ("HEFAMINC", 39, 40, int),
    ("HRMIS",   63, 64,  int),
    ("HRHHID2", 71, 75,  str),
    ("GESTFIPS", 93, 94, int),
    ("PRTAGE", 122, 123, int),
    ("PEMARITL", 125, 126, int),
    ("PESEX", 129, 130, int),
    ("PEEDUCA", 137, 138, int),
    ("PTDTRACE", 139, 140, int),
    ("PULINENO", 147, 148, int),
    ("PEHSPNON", 157, 158, int),
    ("PRCITSHP", 172, 173, int),
    ("PEMLR", 180, 181, int),
    ("PEHRUSL1", 218, 219, int),
    ("PWSSWGT", 613, 622, float),
    ("PTIO1OCD", 860, 863, int),
]
COLSPECS = [(s - 1, e) for _, s, e, _ in COLS]
NAMES = [n for n, *_ in COLS]

TEACHER_OCC = {2300, 2310, 2320, 2330}


def read_month(path):
    # some files are ZIP despite the .gz name — sniff magic bytes
    with open(path, "rb") as fh:
        magic = fh.read(2)
    if magic == b"PK":
        import zipfile
        zf = zipfile.ZipFile(path)
        inner = zf.open(zf.namelist()[0])
        df = pd.read_fwf(inner, colspecs=COLSPECS, names=NAMES, dtype=str)
    else:
        df = pd.read_fwf(path, colspecs=COLSPECS, names=NAMES,
                         compression="gzip", dtype=str)
    for n, _, _, typ in COLS:
        if typ is not str:
            df[n] = pd.to_numeric(df[n], errors="coerce")
    df["HRHHID"] = df["HRHHID"].str.strip()
    df["HRHHID2"] = df["HRHHID2"].str.strip().str.zfill(5)
    # adults only (labor-force universe)
    df = df[df["PRTAGE"] >= 18].copy()
    df["PWSSWGT"] = df["PWSSWGT"] / 10_000.0   # 4 implied decimals
    return df


def main():
    files = sorted(glob.glob(f"{RAWDIR}/*.dat.gz"))
    print(f"{len(files)} monthly files")
    frames = []
    for f in files:
        d = read_month(f)
        print(f"  {os.path.basename(f):18s} {len(d):>7,} adult records")
        frames.append(d)
    cps = pd.concat(frames, ignore_index=True)

    cps["employed"] = cps["PEMLR"].isin([1, 2]).astype(int)
    cps["teacher"] = ((cps["employed"] == 1)
                      & cps["PTIO1OCD"].isin(TEACHER_OCC)).astype(int)

    # --- period t: 2024, MIS 1-4 ; period t+12: 2025 same month, MIS 5-8 ---
    key = ["HRHHID", "HRHHID2", "PULINENO", "HRMONTH"]
    t0 = cps[(cps["HRYEAR4"] == 2024) & (cps["HRMIS"].between(1, 4))].copy()
    t1 = cps[(cps["HRYEAR4"] == 2025) & (cps["HRMIS"].between(5, 8))].copy()

    m = t0.merge(t1, on=key, suffixes=("_0", "_1"))
    # same person within household: MIS advances exactly 4, demographics agree
    m = m[m["HRMIS_1"] - m["HRMIS_0"] == 4]
    valid = ((m["PESEX_0"] == m["PESEX_1"])
             & (m["PTDTRACE_0"] == m["PTDTRACE_1"])
             & (m["PRTAGE_1"] - m["PRTAGE_0"]).between(0, 2))
    print(f"\nlinked pairs (raw)      : {len(m):,}")
    m = m[valid].copy()
    print(f"linked pairs (validated): {len(m):,}")

    # --- teacher attrition sample ---
    tch = m[m["teacher_0"] == 1].copy()
    tch["still_teacher"] = tch["teacher_1"]
    tch["leaver"] = 1 - tch["teacher_1"]
    # decomposition of leavers at t+12
    tch["dest"] = np.select(
        [tch["teacher_1"] == 1,
         (tch["employed_1"] == 1) & (tch["teacher_1"] == 0),
         tch["PEMLR_1"].isin([3, 4]),
         tch["PEMLR_1"].isin([5, 6, 7])],
        ["still teacher", "other occupation", "unemployed", "out of labor force"],
        default="other/unknown")

    print(f"\nteachers in t linked to t+12 : {len(tch):,}")
    w = tch["PWSSWGT_0"]
    print(f"attrition rate (unweighted)  : {tch['leaver'].mean():6.2%}")
    print(f"attrition rate (weighted)    : {np.average(tch['leaver'], weights=w):6.2%}")
    print("\ndestination at t+12 (weighted %):")
    print((tch.groupby('dest')['PWSSWGT_0'].sum() / w.sum() * 100).round(2))

    tch.to_csv(f"{OUTDIR}/cps_teacher_panel.csv", index=False)
    print(f"\nsaved {OUTDIR}/cps_teacher_panel.csv  ({len(tch):,} rows)")

    # also save the full linked panel for context (all occupations)
    m[["HRMONTH", "teacher_0", "teacher_1", "employed_0", "employed_1",
       "PWSSWGT_0"]].to_csv(f"{OUTDIR}/cps_linked_all.csv", index=False)


if __name__ == "__main__":
    main()
