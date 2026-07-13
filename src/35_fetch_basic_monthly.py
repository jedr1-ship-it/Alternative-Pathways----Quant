"""
Fetch basic monthly CPS files needed to follow the 2023 entry cohorts across
their 8 interviews (MIS 1-8) and slim them to the columns needed to build the
TTTT / NT-NT-NT-NT panel and link to the ASEC by PERIDNUM.

Entry cohorts Jan-Aug 2023: MIS 1-4 fall in Jan-Nov 2023, MIS 5-8 in
Jan-Nov 2024. PERIDNUM = HRHHID(15) + HRHHID2(5) + PULINENO(2).
"""
import os
import zipfile
import urllib.request
import pandas as pd

RAW = "data/raw/cps"
COLS = [("HRHHID", 1, 15), ("HRMONTH", 16, 17), ("HRYEAR4", 18, 21),
        ("HRMIS", 63, 64), ("HRHHID2", 71, 75), ("PULINENO", 147, 148),
        ("PEMLR", 180, 181), ("PTIO1OCD", 860, 863)]
SPECS = [(s - 1, e) for _, s, e in COLS]
NAMES = [n for n, *_ in COLS]
MON = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct",
       "nov", "dec"]
URL = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/basic/{f}"


def fetch(y, mi):
    tag = f"{MON[mi]}{str(y)[2:]}"
    out = f"{RAW}/slim_{y}_{mi+1:02d}.parquet"
    if os.path.exists(out):
        return
    z = f"{RAW}/{tag}pub.zip"
    if not os.path.exists(z):
        urllib.request.urlretrieve(URL.format(y=y, f=f"{tag}pub.zip"), z)
    zf = zipfile.ZipFile(z)
    d = pd.read_fwf(zf.open(zf.namelist()[0]), colspecs=SPECS, names=NAMES,
                    dtype=str)
    for c in ["HRMONTH", "HRYEAR4", "HRMIS", "PEMLR", "PTIO1OCD"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["HRHHID"] = d["HRHHID"].str.strip()
    d["HRHHID2"] = d["HRHHID2"].str.strip().str.zfill(5)
    d["PULINENO"] = (pd.to_numeric(d["PULINENO"], errors="coerce")
                     .astype("Int64").astype(str).str.zfill(2))
    d["PERIDNUM"] = d["HRHHID"] + d["HRHHID2"] + d["PULINENO"]
    d = d[["PERIDNUM", "HRYEAR4", "HRMONTH", "HRMIS", "PEMLR", "PTIO1OCD"]]
    d.to_parquet(out, index=False)
    os.remove(z)
    print(f"  {tag}: {len(d):,} rows -> {out}", flush=True)


if __name__ == "__main__":
    for mi in range(0, 11):        # Jan..Nov
        fetch(2023, mi)
        fetch(2024, mi)
    print("done")
