"""
Fetch the pre-2019 ASEC person records, which Census distributes only as
fixed-width .dat.gz (CSV starts in survey year 2019). Covers survey years
2016-2018 (= calendar years 2015-2017), completing the 2015-2024 pool.

Column byte positions are read from each year's own data dictionary so the
parser survives layout changes. Person records are the lines whose first
character is '3' (1=household, 2=family, 3=person). PEIOOCC = -1 means the
person is not currently employed (a leaver if they taught last year).
"""
import gzip
import os
import re
import urllib.request
import pandas as pd

RAW = "data/raw/asec"
VARS = ["PEIOOCC", "OCCUP", "LJCW", "A_CLSWKR", "A_AGE", "A_HGA",
        "WKSWORK", "MARSUPWT"]
BASE = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/march/"
DAT = {2016: "asec2016_pubuse_v3.dat.gz",
       2017: "asec2017_pubuse.dat.gz",
       2018: "asec2018_pubuse.dat.gz"}
DICT = {2016: "Asec2016_Data_Dict_Full.txt",
        2017: "08ASEC2017_Data_Dict_Full.txt",
        2018: "08ASEC2018_Data_Dict_Full.txt"}


def get_positions(year):
    dpath = f"{RAW}/dict{year}.txt"
    if not os.path.exists(dpath):
        urllib.request.urlretrieve(BASE.format(y=year) + DICT[year], dpath)
    pos = {}
    with open(dpath, encoding="latin-1") as fh:
        for line in fh:
            m = re.match(r"D\s+(\S+)\s+(\d+)\s+(\d+)", line)
            if m and m.group(1) in VARS and m.group(1) not in pos:
                name, w, start = m.group(1), int(m.group(2)), int(m.group(3))
                pos[name] = (start, w)
    missing = set(VARS) - set(pos)
    assert not missing, f"{year}: missing {missing}"
    return pos


def parse_year(year):
    slim = f"{RAW}/asec_slim_{str(year)[2:]}.parquet"
    if os.path.exists(slim):
        print(f"  {year}: exists, skip"); return
    pos = get_positions(year)
    dat = f"{RAW}/{DAT[year]}"
    if not os.path.exists(dat):
        print(f"  {year}: downloading {DAT[year]}", flush=True)
        urllib.request.urlretrieve(BASE.format(y=year) + DAT[year], dat)
    recs = {v: [] for v in VARS}
    with gzip.open(dat, "rt", encoding="latin-1") as fh:
        for line in fh:
            if line[0] != "3":
                continue
            for v in VARS:
                s, w = pos[v]
                recs[v].append(line[s - 1:s - 1 + w])
    d = pd.DataFrame(recs)
    for v in VARS:
        d[v] = pd.to_numeric(d[v], errors="coerce")
    d["asec_year"] = year
    d.to_parquet(slim, index=False)
    os.remove(dat)
    print(f"  {year}: {len(d):,} persons -> {slim}", flush=True)


if __name__ == "__main__":
    for y in (2016, 2017, 2018):
        parse_year(y)
    print("done")
