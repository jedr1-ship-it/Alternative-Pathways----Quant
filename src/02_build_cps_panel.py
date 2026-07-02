"""
Build a linked 12-month CPS panel of school teachers, 2021 -> 2025.

Source: official Current Population Survey basic monthly public-use microdata,
downloaded from https://www2.census.gov/programs-surveys/cps/datasets/<year>/basic/
(files <mon><yy>pub.dat.gz, fixed-width; positions from the 2025 record layout,
stable for these variables across 2021-2025; teacher occupation codes
2300-2330 are identical in the 2010 and 2020 Census classifications).

CPS rotation design (4-8-4): a household interviewed in month-in-sample (MIS)
1-4 of month t is re-interviewed exactly 12 months later with MIS 5-8. We link
persons across each year pair via (HRHHID, HRHHID2, PULINENO) and validate the
match with sex, race, and an age increase of 0-2 years (Madrian-Lefgren).

Analytic teacher sample: employed school teachers (occ 2300 preschool/K,
2310 elementary/middle, 2320 secondary, 2330 special education) holding at
least a bachelor's degree (PEEDUCA >= 43) -- the standard restriction in the
teacher-attrition literature.
"""
import glob
import os
import numpy as np
import pandas as pd

RAWDIR = "data/raw/cps"
OUTDIR = "data/processed"
os.makedirs(OUTDIR, exist_ok=True)

YEAR_PAIRS = [(2021, 2022), (2022, 2023), (2023, 2024), (2024, 2025)]

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
        yr = d["HRYEAR4"].mode().iat[0]
        assert 2021 <= yr <= 2025, f"unexpected year {yr} in {f}"
        print(f"  {os.path.basename(f):18s} {len(d):>7,} adult records  (year {yr})")
        frames.append(d)
    cps = pd.concat(frames, ignore_index=True)

    cps["employed"] = cps["PEMLR"].isin([1, 2]).astype(int)
    cps["teacher"] = ((cps["employed"] == 1)
                      & cps["PTIO1OCD"].isin(TEACHER_OCC)).astype(int)

    key = ["HRHHID", "HRHHID2", "PULINENO", "HRMONTH"]
    panels = []
    for y0, y1 in YEAR_PAIRS:
        t0 = cps[(cps["HRYEAR4"] == y0) & (cps["HRMIS"].between(1, 4))]
        t1 = cps[(cps["HRYEAR4"] == y1) & (cps["HRMIS"].between(5, 8))]
        m = t0.merge(t1, on=key, suffixes=("_0", "_1"))
        m = m[m["HRMIS_1"] - m["HRMIS_0"] == 4]
        valid = ((m["PESEX_0"] == m["PESEX_1"])
                 & (m["PTDTRACE_0"] == m["PTDTRACE_1"])
                 & (m["PRTAGE_1"] - m["PRTAGE_0"]).between(0, 2))
        m = m[valid].copy()
        m["base_year"] = y0
        panels.append(m)
        print(f"\n{y0}->{y1}: validated links {len(m):,}")
    linked = pd.concat(panels, ignore_index=True)
    print(f"\nTOTAL validated links: {len(linked):,}")

    # --- teacher attrition sample: employed teacher at t with BA+ ---
    tch = linked[(linked["teacher_0"] == 1)
                 & (linked["PEEDUCA_0"] >= 43)].copy()
    tch["still_teacher"] = tch["teacher_1"]
    tch["leaver"] = 1 - tch["teacher_1"]
    tch["dest"] = np.select(
        [tch["teacher_1"] == 1,
         (tch["employed_1"] == 1) & (tch["teacher_1"] == 0),
         tch["PEMLR_1"].isin([3, 4]),
         tch["PEMLR_1"].isin([5, 6, 7])],
        ["still teacher", "other occupation", "unemployed", "out of labor force"],
        default="other/unknown")

    w = tch["PWSSWGT_0"]
    print(f"\nteachers (BA+) linked 12 months : {len(tch):,}")
    print("by base year:", tch.groupby("base_year").size().to_dict())
    print(f"attrition rate (weighted)       : "
          f"{np.average(tch['leaver'], weights=w):6.2%}")
    print("\ndestination at t+12 (weighted %):")
    print((tch.groupby('dest')['PWSSWGT_0'].sum() / w.sum() * 100).round(2))

    tch.to_csv(f"{OUTDIR}/cps_teacher_panel.csv", index=False)
    print(f"\nsaved {OUTDIR}/cps_teacher_panel.csv  ({len(tch):,} rows)")


if __name__ == "__main__":
    main()
