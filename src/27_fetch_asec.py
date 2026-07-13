"""
Download the CPS ASEC (March supplement) person files 2015-2024 from the
Census Bureau and keep only the handful of columns the Aldeman-Yi
retrospective turnover measure needs. Disk-careful: fetch one zip, extract
the person file, slim it to parquet, delete the zip and the full csv.

Retrospective instrument columns:
  OCCUP    detailed occupation of the longest job held LAST year
  PEIOOCC  detailed occupation of the current (survey-week) job
  LJCW     class of worker, longest job last year (1-2 private, 3-5 gov)
  A_CLSWKR class of worker, current
  A_AGE    age
  A_HGA    educational attainment (43 = bachelor's, >=44 master's+)
  WKSWORK  weeks worked last year
  MARSUPWT ASEC person supplement weight (2 implied decimals)
"""
import os
import zipfile
import urllib.request
import pandas as pd

RAW = "data/raw/asec"
os.makedirs(RAW, exist_ok=True)
COLS = ["PEIOOCC", "OCCUP", "LJCW", "A_CLSWKR", "A_AGE", "A_HGA",
        "WKSWORK", "MARSUPWT"]
URL = ("https://www2.census.gov/programs-surveys/cps/datasets/"
       "{yyyy}/march/asecpub{yy}csv.zip")


def fetch_year(yy):
    slim = f"{RAW}/asec_slim_{yy}.parquet"
    if os.path.exists(slim):
        print(f"  20{yy}: slim exists, skip")
        return
    yyyy = 2000 + yy
    zpath = f"{RAW}/asec{yy}.zip"
    if not os.path.exists(zpath):
        url = URL.format(yyyy=yyyy, yy=yy)
        print(f"  20{yy}: downloading {url}", flush=True)
        urllib.request.urlretrieve(url, zpath)
    z = zipfile.ZipFile(zpath)
    person = [n for n in z.namelist()
              if os.path.basename(n).startswith("pppub")][0]
    ppath = f"{RAW}/{os.path.basename(person)}"
    with z.open(person) as src, open(ppath, "wb") as dst:
        dst.write(src.read())
    # some early years may name columns slightly differently; intersect
    head = pd.read_csv(ppath, nrows=0)
    use = [c for c in COLS if c in head.columns]
    missing = set(COLS) - set(use)
    d = pd.read_csv(ppath, usecols=use)
    d["asec_year"] = yyyy
    d.to_parquet(slim, index=False)
    os.remove(ppath)
    os.remove(zpath)
    print(f"  20{yy}: {len(d):,} persons -> {slim}"
          + (f"  MISSING {missing}" if missing else ""), flush=True)


if __name__ == "__main__":
    # Census publishes ASEC as CSV only from survey year 2019 onward.
    for yy in range(19, 26):
        fetch_year(yy)
    print("done")
