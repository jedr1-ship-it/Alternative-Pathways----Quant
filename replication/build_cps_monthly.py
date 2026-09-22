"""Download and cache the CPS basic monthly files, 2005-2025.

Sources (official public-use microdata):
  - 2005-2023: NBER mirror,  data.nber.org/cps-basic3/dat/<year>/cpsb<yyyymm>_dat.zip
  - 2024-2025: Census Bureau, www2.census.gov/programs-surveys/cps/datasets/<year>/basic/<mon><yy>pub.dat.gz

Writes data/raw/cps/ (raw) and data/interim/cps_<yyyymm>.parquet (parsed).
Fixed-width positions are stable since the January 2003 redesign. Safe to
re-run: existing files are kept, missing ones fetched.
"""
import glob
import os
import re
import subprocess
import sys
import zipfile
import pandas as pd

RAWDIR = "data/raw/cps"
INTDIR = "data/interim"
os.makedirs(RAWDIR, exist_ok=True)
os.makedirs(INTDIR, exist_ok=True)
MONNAMES = ["jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"]

COLS = [
    ("HRHHID",   1, 15,  str), ("HRMONTH", 16, 17,  int),
    ("HRYEAR4", 18, 21,  int), ("HRMIS",   63, 64,  int),
    ("HRHHID2", 71, 75,  str), ("PRTAGE", 122, 123, int),
    ("PESEX", 129, 130, int),  ("PEEDUCA", 137, 138, int),
    ("PTDTRACE", 139, 140, int), ("PULINENO", 147, 148, int),
    ("PEMLR", 180, 181, int),  ("PEHRUSL1", 218, 219, int),
    ("PEIO1COW", 432, 433, int), ("PWSSWGT", 613, 622, float),
    ("PTIO1OCD", 860, 863, int),
]
COLSPECS = [(s - 1, e) for _, s, e, _ in COLS]
NAMES = [n for n, *_ in COLS]
TEACHER_OCC = {2300, 2310, 2320, 2330}


def fetch(url, dest):
    r = subprocess.run(["curl", "-s", "--max-time", "300", "--retry", "3",
                        "--retry-delay", "4", url, "-o", dest])
    return r.returncode == 0 and os.path.getsize(dest) > 1_000_000 if os.path.exists(dest) else False


def download():
    for y in range(2005, 2026):
        for m in range(1, 13):
            nber = f"{RAWDIR}/cpsb{y}{m:02d}.zip"
            cens = f"{RAWDIR}/{MONNAMES[m-1]}{y % 100:02d}pub.dat.gz"
            if os.path.exists(nber) or os.path.exists(cens):
                continue
            if y <= 2023:
                ok = fetch(f"https://data.nber.org/cps-basic3/dat/{y}/cpsb{y}{m:02d}_dat.zip", nber)
                if ok:
                    try:
                        zipfile.ZipFile(nber).testzip()
                    except Exception:
                        ok = False
                if not ok and os.path.exists(nber):
                    os.remove(nber)
            else:
                ok = fetch(f"https://www2.census.gov/programs-surveys/cps/datasets/{y}/basic/{MONNAMES[m-1]}{y % 100:02d}pub.dat.gz", cens)
                if not ok and os.path.exists(cens):
                    os.remove(cens)
            print(f"{y}-{m:02d}: {'ok' if ok else 'MISSING'}", flush=True)


def read_month(path):
    with open(path, "rb") as fh:
        magic = fh.read(2)
    if magic == b"PK":
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
    df = df[df["PRTAGE"] >= 18].copy()
    df["PWSSWGT"] = (df["PWSSWGT"] / 10_000.0).astype("float32")
    for n in NAMES:
        if n not in ("HRHHID", "HRHHID2", "PWSSWGT"):
            df[n] = df[n].astype("Int32")
    return df


def cache():
    raw = sorted(glob.glob(f"{RAWDIR}/*.dat.gz") + glob.glob(f"{RAWDIR}/cpsb*.zip"))
    MON = {m: i + 1 for i, m in enumerate(MONNAMES)}
    parsed = kept = 0
    for f in raw:
        b = os.path.basename(f)
        m = re.match(r"cpsb(\d{4})(\d{2})", b)
        yyyymm = m.group(1) + m.group(2) if m else \
            f"20{re.match(r'([a-z]{3})(\d{2})pub', b).group(2)}{MON[re.match(r'([a-z]{3})(\d{2})pub', b).group(1)]:02d}"
        out = f"{INTDIR}/cps_{yyyymm}.parquet"
        if os.path.exists(out):
            kept += 1
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
        print(f"  cached {yyyymm} ({len(d):,} adults, teachers {share:.1f}% of employed)", flush=True)
    print(f"cache: {parsed} parsed, {kept} already present")


if __name__ == "__main__":
    if "--no-download" not in sys.argv:
        download()
    cache()
