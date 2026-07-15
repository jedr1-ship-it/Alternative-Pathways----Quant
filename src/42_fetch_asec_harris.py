"""
Fetch the ASEC person files for surveys 2016-2025 (calendar 2015-2024) with
the full Harris & Adams (2007) variable set, from the rawest public files:
CSV for surveys >= 2019, fixed-width via each year's dictionary for
2016-2018. One slim parquet per year: data/raw/asec/asec_ha_{yy}.parquet.

Variables (H&A Tables 1-6):
  OCCUP     occupation of longest job LAST year (defines the profession)
  PEIOOCC   current-week occupation (defines leaving)
  A_LFSR    current labor force status (splits unemployed vs left LF)
  A_AGE, A_SEX, A_MARITL, PRDTRACE, A_HGA   demographics
  WSAL_VAL  wage & salary earnings last year   WKSWORK  weeks worked
  HRSWK     usual hours last year              PENPLAN  pension at longest job
  LJCW      class of worker, longest job       MARSUPWT supplement weight
"""
import gzip
import os
import re
import zipfile
import urllib.request
import pandas as pd

RAW = "data/raw/asec"
VARS = ["OCCUP", "PEIOOCC", "A_LFSR", "A_AGE", "A_SEX", "A_MARITL",
        "PRDTRACE", "A_HGA", "WSAL_VAL", "WKSWORK", "HRSWK", "PENPLAN",
        "LJCW", "MARSUPWT"]
CSV_URL = ("https://www2.census.gov/programs-surveys/cps/datasets/"
           "{y}/march/asecpub{yy}csv.zip")
FW = {2016: "asec2016_pubuse_v3.dat.gz",
      2017: "asec2017_pubuse.dat.gz",
      2018: "asec2018_pubuse.dat.gz"}


def fetch_csv(y):
    yy = str(y)[2:]
    out = f"{RAW}/asec_ha_{yy}.parquet"
    if os.path.exists(out):
        print(f"  {y}: exists"); return
    z = f"{RAW}/ha{yy}.zip"
    if not os.path.exists(z):
        urllib.request.urlretrieve(CSV_URL.format(y=y, yy=yy), z)
    zf = zipfile.ZipFile(z)
    name = [n for n in zf.namelist()
            if os.path.basename(n).startswith("pppub")][0]
    p = f"{RAW}/ha_pp{yy}.csv"
    with zf.open(name) as s, open(p, "wb") as d:
        d.write(s.read())
    head = pd.read_csv(p, nrows=0).columns
    use = [v for v in VARS if v in head]
    df = pd.read_csv(p, usecols=use)
    for v in set(VARS) - set(use):
        df[v] = pd.NA
    df["asec_year"] = y
    df.to_parquet(out, index=False)
    os.remove(p); os.remove(z)
    print(f"  {y}: {len(df):,} persons"
          + (f"  MISSING {sorted(set(VARS)-set(use))}"
             if set(VARS) - set(use) else ""), flush=True)


def fetch_fw(y):
    yy = str(y)[2:]
    out = f"{RAW}/asec_ha_{yy}.parquet"
    if os.path.exists(out):
        print(f"  {y}: exists"); return
    dpath = f"{RAW}/dict{y}.txt"
    pos = {}
    for line in open(dpath, encoding="latin-1"):
        m = re.match(r"D\s+(\S+)\s+(\d+)\s+(\d+)", line)
        if m and m.group(1) in VARS and m.group(1) not in pos:
            pos[m.group(1)] = (int(m.group(3)), int(m.group(2)))
    missing = set(VARS) - set(pos)
    dat = f"{RAW}/{FW[y]}"
    if not os.path.exists(dat):
        urllib.request.urlretrieve(
            f"https://www2.census.gov/programs-surveys/cps/datasets/"
            f"{y}/march/{FW[y]}", dat)
    recs = {v: [] for v in pos}
    with gzip.open(dat, "rt", encoding="latin-1") as fh:
        for line in fh:
            if line[0] != "3":
                continue
            for v, (s, w) in pos.items():
                recs[v].append(line[s - 1:s - 1 + w])
    df = pd.DataFrame(recs)
    for v in df.columns:
        df[v] = pd.to_numeric(df[v], errors="coerce")
    for v in missing:
        df[v] = pd.NA
    df["asec_year"] = y
    df.to_parquet(out, index=False)
    os.remove(dat)
    print(f"  {y}: {len(df):,} persons"
          + (f"  MISSING {sorted(missing)}" if missing else ""), flush=True)


if __name__ == "__main__":
    for y in (2016, 2017, 2018):
        fetch_fw(y)
    for y in range(2019, 2026):
        fetch_csv(y)
    print("done", flush=True)
