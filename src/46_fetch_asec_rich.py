"""
Rich ASEC extraction for the full paper: surveys 2011-2025, one parquet per
year (asec_rich_{yy}.parquet). Adds to the Harris set the person identifier
(PERIDNUM, for the March-to-March earnings link), and the family pointers
(PH_SEQ, A_LINENO, A_PARENT, A_SPOUSE) from which own-children variables are
built for every person -- teachers and comparison professions alike.

Surveys 2019-2025 come as CSV; 2011-2018 as fixed-width. The 2011-2018
byte layout is identical (verified: PERIDNUM/PEIOOCC/OCCUP/MARSUPWT agree
with the 2013 and 2016-2018 dictionaries, and extraction validates against
the March monthly PERIDNUM join), so dict2018 positions are used for all
fixed-width years with per-year validation.
"""
import gzip
import os
import re
import zipfile
import urllib.request
import pandas as pd

RAW = "data/raw/asec"
VARS = ["PERIDNUM", "PH_SEQ", "A_LINENO", "A_PARENT", "A_SPOUSE",
        "PEPAR1", "PEPAR2",
        "OCCUP", "PEIOOCC", "A_LFSR", "A_AGE", "A_SEX", "A_MARITL",
        "PRDTRACE", "A_HGA", "WSAL_VAL", "WKSWORK", "HRSWK", "PENPLAN",
        "LJCW", "MARSUPWT"]
CSV_URL = ("https://www2.census.gov/programs-surveys/cps/datasets/"
           "{y}/march/asecpub{yy}csv.zip")
FW = {2011: "asec2011_pubuse.dat.gz", 2012: "asec2012_pubuse.dat.gz",
      2013: "asec2013_pubuse.dat.gz",
      2014: "asec2014_pubuse_tax_fix_5x8_2017.dat.gz",
      2015: "asec2015_pubuse.dat.gz", 2016: "asec2016_pubuse_v3.dat.gz",
      2017: "asec2017_pubuse.dat.gz", 2018: "asec2018_pubuse.dat.gz"}
CORE = {2300, 2310, 2320, 2330}


def positions():
    pos = {}
    for line in open(f"{RAW}/dict2018.txt", encoding="latin-1"):
        m = re.match(r"D\s+(\S+)\s+(\d+)\s+(\d+)", line)
        if m and m.group(1) in VARS and m.group(1) not in pos:
            pos[m.group(1)] = (int(m.group(3)), int(m.group(2)))
    need = set(VARS) - {"PEPAR1", "PEPAR2"}
    assert need <= set(pos), f"missing {need-set(pos)}"
    return pos


def fetch_csv(y):
    yy = str(y)[2:]
    out = f"{RAW}/asec_rich_{yy}.parquet"
    if os.path.exists(out):
        print(f"  {y}: exists"); return
    z = f"{RAW}/rich{yy}.zip"
    if not os.path.exists(z):
        urllib.request.urlretrieve(CSV_URL.format(y=y, yy=yy), z)
    zf = zipfile.ZipFile(z)
    name = [n for n in zf.namelist()
            if os.path.basename(n).startswith("pppub")][0]
    p = f"{RAW}/rich_pp{yy}.csv"
    with zf.open(name) as s, open(p, "wb") as d:
        d.write(s.read())
    head = pd.read_csv(p, nrows=0).columns
    use = [v for v in VARS if v in head]
    df = pd.read_csv(p, usecols=use, dtype={"PERIDNUM": str})
    for v in set(VARS) - set(use):
        df[v] = pd.NA
    df["asec_year"] = y
    df.to_parquet(out, index=False)
    os.remove(p); os.remove(z)
    print(f"  {y}: {len(df):,}"
          + (f" MISSING {sorted(set(VARS)-set(use))}"
             if set(VARS) - set(use) else ""), flush=True)


def fetch_fw(y, pos):
    yy = str(y)[2:]
    out = f"{RAW}/asec_rich_{yy}.parquet"
    if os.path.exists(out):
        print(f"  {y}: exists"); return
    dat = f"{RAW}/{FW[y]}"
    if not os.path.exists(dat):
        urllib.request.urlretrieve(
            f"https://www2.census.gov/programs-surveys/cps/datasets/"
            f"{y}/march/{FW[y]}", dat)
    recs = {v: [] for v in VARS}
    with gzip.open(dat, "rt", encoding="latin-1") as fh:
        for line in fh:
            if line[0] != "3":
                continue
            for v, (s, w) in pos.items():
                recs[v].append(line[s - 1:s - 1 + w])
    df = pd.DataFrame(recs)
    for v in VARS:
        if v != "PERIDNUM":
            df[v] = pd.to_numeric(df[v], errors="coerce")
    df["PERIDNUM"] = df["PERIDNUM"].str.strip()
    # validation: teacher share of OCCUP and plausible age distribution
    posocc = df[df["OCCUP"] > 0]
    tsh = posocc["OCCUP"].isin(CORE).mean() * 100
    aok = df["A_AGE"].between(0, 85).mean() * 100
    ok = 1.0 < tsh < 6.0 and aok > 99
    print(f"  {y}: {len(df):,} | teacher share {tsh:.1f}% | age ok {aok:.0f}%"
          f" -> {'OK' if ok else 'REJECTED'}", flush=True)
    if ok:
        df["asec_year"] = y
        df.to_parquet(out, index=False)
    os.remove(dat)


if __name__ == "__main__":
    pos = positions()
    for y in range(2011, 2019):
        fetch_fw(y, pos)
    for y in range(2019, 2026):
        fetch_csv(y)
    print("done", flush=True)
