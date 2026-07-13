"""
Backfill from the rawest public files so the TTTT vs March confusion table
covers cohorts 2005-2024 (the maximum: person linkage needs HRHHID2, which
exists only from May 2004).

Stage 1: slim basic monthly files 2005-2017 (Jan-Nov). Reuse the cpsb zips
already on disk (2005-2007); download the rest from Census
({mon}{yy}pub.zip). Layout positions are stable since Jan 2003.

Stage 2: extract PERIDNUM/OCCUP/PEIOOCC from the fixed-width ASEC person
records for survey years 2006-2018 (cohort Y links to ASEC Y+1). Column
positions are read from each year's data dictionary, discovered by listing
the Census march directory.
"""
import glob
import gzip
import io
import os
import re
import urllib.request
import zipfile
import pandas as pd

RAW = "data/raw/cps"
ARAW = "data/raw/asec"
MON = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct",
       "nov", "dec"]
COLS = [("HRHHID", 1, 15), ("HRMONTH", 16, 17), ("HRYEAR4", 18, 21),
        ("HRMIS", 63, 64), ("HRHHID2", 71, 75), ("PULINENO", 147, 148),
        ("PEMLR", 180, 181), ("PTIO1OCD", 860, 863)]
SPECS = [(s - 1, e) for _, s, e in COLS]
NAMES = [n for n, *_ in COLS]


def slim_month(y, mi):
    out = f"{RAW}/slim_{y}_{mi+1:02d}.parquet"
    if os.path.exists(out):
        return
    src = f"{RAW}/cpsb{y}{mi+1:02d}.zip"
    if not os.path.exists(src):
        tag = f"{MON[mi]}{str(y)[2:]}pub.zip"
        url = (f"https://www2.census.gov/programs-surveys/cps/datasets/"
               f"{y}/basic/{tag}")
        src = f"{RAW}/{tag}"
        try:
            urllib.request.urlretrieve(url, src)
        except Exception as e:
            print(f"  {y}-{mi+1:02d}: FAIL download {type(e).__name__}",
                  flush=True)
            return
        dl = True
    else:
        dl = False
    try:
        zf = zipfile.ZipFile(src)
        d = pd.read_fwf(zf.open(zf.namelist()[0]), colspecs=SPECS,
                        names=NAMES, dtype=str)
    except Exception as e:
        print(f"  {y}-{mi+1:02d}: FAIL parse {type(e).__name__}", flush=True)
        return
    for c in ["HRMONTH", "HRYEAR4", "HRMIS", "PEMLR", "PTIO1OCD"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["HRHHID"] = d["HRHHID"].str.strip()
    d["HRHHID2"] = d["HRHHID2"].str.strip().str.zfill(5)
    d["PULINENO"] = (pd.to_numeric(d["PULINENO"], errors="coerce")
                     .astype("Int64").astype(str).str.zfill(2))
    d["PERIDNUM"] = d["HRHHID"] + d["HRHHID2"] + d["PULINENO"]
    d = d[["PERIDNUM", "HRYEAR4", "HRMONTH", "HRMIS", "PEMLR", "PTIO1OCD"]]
    d.to_parquet(out, index=False)
    if dl:
        os.remove(src)
    print(f"  {y}-{mi+1:02d}: {len(d):,} -> slim", flush=True)


def march_dir(y):
    url = (f"https://www2.census.gov/programs-surveys/cps/datasets/"
           f"{y}/march/")
    try:
        html = urllib.request.urlopen(url, timeout=30).read().decode(
            "utf-8", "ignore")
    except Exception:
        return url, []
    return url, re.findall(r'href="([^"]+)"', html)


def asec_ids(y):
    """Extract PERIDNUM/OCCUP/PEIOOCC from fixed-width ASEC of survey year y."""
    yy = str(y)[2:]
    out = f"{ARAW}/asec_id_{yy}.parquet"
    if os.path.exists(out):
        print(f"  ASEC {y}: exists", flush=True)
        return
    base, files = march_dir(y)
    dat = [f for f in files if re.search(r"(asec|mar).*\.dat\.gz$", f, re.I)
           and "repwgt" not in f.lower()]
    dic = [f for f in files if re.search(r"data.?dict", f, re.I)
           and f.endswith(".txt")]
    if not dat or not dic:
        print(f"  ASEC {y}: NOT FOUND (dat={dat[:2]} dict={dic[:2]})",
              flush=True)
        return
    dpath = f"{ARAW}/dict{y}.txt"
    if not os.path.exists(dpath):
        urllib.request.urlretrieve(base + dic[0], dpath)
    pos = {}
    for line in open(dpath, encoding="latin-1"):
        m = re.match(r"D\s+(PERIDNUM|OCCUP|PEIOOCC|A_AGE|MARSUPWT)\s+(\d+)"
                     r"\s+(\d+)", line)
        if m and m.group(1) not in pos:
            pos[m.group(1)] = (int(m.group(3)), int(m.group(2)))
    need = {"PERIDNUM", "OCCUP", "PEIOOCC"}
    if not need <= set(pos):
        print(f"  ASEC {y}: dict missing {need - set(pos)}", flush=True)
        return
    fpath = f"{ARAW}/asec{y}.dat.gz"
    if not os.path.exists(fpath):
        urllib.request.urlretrieve(base + dat[0], fpath)
    recs = {v: [] for v in pos}
    with gzip.open(fpath, "rt", encoding="latin-1") as fh:
        for line in fh:
            if line[0] != "3":
                continue
            for v, (s, w) in pos.items():
                recs[v].append(line[s - 1:s - 1 + w])
    d = pd.DataFrame(recs)
    for v in d.columns:
        if v != "PERIDNUM":
            d[v] = pd.to_numeric(d[v], errors="coerce")
    d["PERIDNUM"] = d["PERIDNUM"].str.strip()
    d.to_parquet(out, index=False)
    os.remove(fpath)
    print(f"  ASEC {y}: {len(d):,} persons -> {out}", flush=True)


if __name__ == "__main__":
    print("stage 1: monthly slims 2005-2017", flush=True)
    for y in range(2005, 2018):
        for mi in range(0, 11):
            slim_month(y, mi)
    print("stage 2: ASEC ids 2006-2018", flush=True)
    for y in range(2006, 2019):
        asec_ids(y)
    print("done", flush=True)
