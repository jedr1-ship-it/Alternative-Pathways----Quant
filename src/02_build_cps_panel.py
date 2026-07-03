"""
Build a linked 12-month CPS panel of school teachers, 2005 -> 2025.

Sources (official CPS basic monthly public-use microdata):
  - 2021-2025: U.S. Census Bureau,
    https://www2.census.gov/programs-surveys/cps/datasets/<year>/basic/
    (<mon><yy>pub.dat.gz)
  - 2005-2020: NBER mirror of the same files,
    https://data.nber.org/cps-basic3/dat/<year>/ (cpsb<yyyymm>_dat.zip)

Fixed-width positions are stable for the variables used here since the
January 2003 redesign; the person-link identifier HRHHID2 exists from
May 2004, which is what bounds the panel start at 2005. Teacher occupation
codes 2300-2330 are identical in the 2002, 2010 and 2020 Census
classifications.

CPS rotation design (4-8-4): a household interviewed in month-in-sample
(MIS) 1-4 of month t is re-interviewed exactly 12 months later with MIS 5-8.
We link persons across each year pair via (HRHHID, HRHHID2, PULINENO) and
validate with sex, race, and an age increase of 0-2 years (Madrian-Lefgren).

Analytic teacher sample: employed school teachers (occ 2300 preschool/K,
2310 elementary/middle, 2320 secondary, 2330 special education) holding at
least a bachelor's degree (PEEDUCA >= 43).

Two stages, resumable:
  1. parse each raw monthly file once -> data/interim/cps_<yyyymm>.parquet
  2. link year pairs (loading two years at a time) -> teacher panel CSV
"""
import glob
import os
import re
import numpy as np
import pandas as pd

RAWDIR = "data/raw/cps"
INTDIR = "data/interim"
OUTDIR = "data/processed"
os.makedirs(INTDIR, exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)

FIRST_BASE, LAST_BASE = 2005, 2024   # year pairs (y, y+1)

# (name, start, end) 1-indexed inclusive, from the Basic CPS record layout
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
    ("PRCHLD", 633, 634, int),     # presence of own children <18 by age group
    ("PRNMCHLD", 635, 636, int),   # number of own children <18
    ("PTIO1OCD", 860, 863, int),
]
COLSPECS = [(s - 1, e) for _, s, e, _ in COLS]
NAMES = [n for n, *_ in COLS]

TEACHER_OCC = {2300, 2310, 2320, 2330}


def read_month(path):
    """Parse one raw monthly file (gzip or zip, sniffed by magic bytes)."""
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
    df = df[df["PRTAGE"] >= 18].copy()          # adults only
    df["PWSSWGT"] = df["PWSSWGT"] / 10_000.0    # 4 implied decimals
    for n in NAMES:
        if n not in ("HRHHID", "HRHHID2", "PWSSWGT"):
            df[n] = df[n].astype("Int32")
    df["PWSSWGT"] = df["PWSSWGT"].astype("float32")
    return df


def stage1_cache():
    """Parse every raw file once into a monthly parquet cache."""
    raw = sorted(glob.glob(f"{RAWDIR}/*.dat.gz") + glob.glob(f"{RAWDIR}/cpsb*.zip"))
    MON = dict(jan=1, feb=2, mar=3, apr=4, may=5, jun=6,
               jul=7, aug=8, sep=9, oct=10, nov=11, dec=12)
    done, parsed = 0, 0
    for f in raw:
        b = os.path.basename(f)
        m = re.match(r"cpsb(\d{4})(\d{2})", b)
        if m:
            yyyymm = m.group(1) + m.group(2)
        else:
            m2 = re.match(r"([a-z]{3})(\d{2})pub", b)
            yyyymm = f"20{m2.group(2)}{MON[m2.group(1)]:02d}"
        out = f"{INTDIR}/cps_{yyyymm}.parquet"
        if os.path.exists(out):
            done += 1
            continue
        try:
            d = read_month(f)
        except Exception as e:
            print(f"  SKIP {b}: {type(e).__name__} {e}", flush=True)
            continue
        yr, mo = int(yyyymm[:4]), int(yyyymm[4:])
        assert d["HRYEAR4"].mode().iat[0] == yr, f"year mismatch in {b}"
        assert d["HRMONTH"].mode().iat[0] == mo, f"month mismatch in {b}"
        emp = d[d["PEMLR"].isin([1, 2])]
        share = emp["PTIO1OCD"].isin(TEACHER_OCC).mean() * 100
        assert 1.0 < share < 6.0, f"teacher share {share:.1f}% off in {b}"
        d.to_parquet(out, index=False)
        parsed += 1
        print(f"  cached {yyyymm}  ({len(d):,} adults, teachers "
              f"{share:.1f}% of employed)", flush=True)
    print(f"stage 1: {parsed} parsed, {done} already cached")


def load_year(year, mis_lo, mis_hi):
    parts = []
    for f in sorted(glob.glob(f"{INTDIR}/cps_{year}??.parquet")):
        d = pd.read_parquet(f)
        parts.append(d[d["HRMIS"].between(mis_lo, mis_hi)])
    return pd.concat(parts, ignore_index=True) if parts else None


def stage2_link():
    key = ["HRHHID", "HRHHID2", "PULINENO", "HRMONTH"]
    panels, flows, total_links = [], [], 0
    for y0 in range(FIRST_BASE, LAST_BASE + 1):
        y1 = y0 + 1
        t0, t1 = load_year(y0, 1, 4), load_year(y1, 5, 8)
        if t0 is None or t1 is None:
            print(f"{y0}->{y1}: MISSING YEAR, skipped")
            continue
        m = t0.merge(t1, on=key, suffixes=("_0", "_1"))
        m = m[m["HRMIS_1"] - m["HRMIS_0"] == 4]
        valid = ((m["PESEX_0"] == m["PESEX_1"])
                 & (m["PTDTRACE_0"] == m["PTDTRACE_1"])
                 & (m["PRTAGE_1"] - m["PRTAGE_0"]).between(0, 2))
        m = m[valid].copy()
        total_links += len(m)

        for t in ("_0", "_1"):
            m[f"employed{t}"] = m[f"PEMLR{t}"].isin([1, 2]).astype(int)
            m[f"teacher{t}"] = ((m[f"employed{t}"] == 1)
                                & m[f"PTIO1OCD{t}"].isin(TEACHER_OCC)).astype(int)
        # BA+ teacher indicators at each end of the link
        m["tchBA_0"] = ((m["teacher_0"] == 1) & (m["PEEDUCA_0"] >= 43)).astype(int)
        m["tchBA_1"] = ((m["teacher_1"] == 1) & (m["PEEDUCA_1"] >= 43)).astype(int)
        tch = m[m["tchBA_0"] == 1].copy()
        tch["base_year"] = y0
        panels.append(tch)

        # gross flows within the linked sample (weighted, population scale)
        w0, w1 = m["PWSSWGT_0"].astype(float), m["PWSSWGT_1"].astype(float)
        flows.append({
            "base_year": y0,
            "teachers_t_w": w0[m["tchBA_0"] == 1].sum(),
            "teachers_t1_w": w1[m["tchBA_1"] == 1].sum(),
            "leavers_w": w0[(m["tchBA_0"] == 1) & (m["teacher_1"] == 0)].sum(),
            "entrants_w": w1[(m["tchBA_1"] == 1) & (m["teacher_0"] == 0)].sum(),
            "links_w": w0.sum(),
            "n_teachers": int(m["tchBA_0"].sum()),
        })
        print(f"{y0}->{y1}: links {len(m):>7,} | teachers (BA+) {len(tch):>5,}",
              flush=True)
        del m, t0, t1

    tch = pd.concat(panels, ignore_index=True)
    tch["still_teacher"] = tch["teacher_1"]
    tch["leaver"] = 1 - tch["teacher_1"]
    tch["dest"] = np.select(
        [tch["teacher_1"] == 1,
         (tch["employed_1"] == 1) & (tch["teacher_1"] == 0),
         tch["PEMLR_1"].isin([3, 4]),
         tch["PEMLR_1"].isin([5, 6, 7])],
        ["still teacher", "other occupation", "unemployed", "out of labor force"],
        default="other/unknown")

    w = tch["PWSSWGT_0"].astype(float)
    print(f"\nTOTAL validated links       : {total_links:,}")
    print(f"teachers (BA+) followed 12m : {len(tch):,}")
    print(f"attrition rate (weighted)   : "
          f"{np.average(tch['leaver'], weights=w):6.2%}")
    print("\ndestination at t+12 (weighted %):")
    print((tch.groupby('dest')['PWSSWGT_0'].sum() / w.sum() * 100).round(2))
    tch.to_csv(f"{OUTDIR}/cps_teacher_panel.csv", index=False)
    pd.DataFrame(flows).to_csv(f"{OUTDIR}/cps_flows.csv", index=False)
    print(f"\nsaved {OUTDIR}/cps_teacher_panel.csv  ({len(tch):,} rows)"
          f" and {OUTDIR}/cps_flows.csv")


if __name__ == "__main__":
    stage1_cache()
    stage2_link()
