"""
Re-extract ASEC surveys 1998-2010 from the raw Census fixed-width files
using the OFFICIAL byte positions parsed from the published technical
documentation (outputs/layouts_official.csv). No empirical calibration:
every variable is read where the Census says it is. Light sanity checks
confirm (not choose) the layout:

  ages look human, MARSUPWT positive for nearly everyone, A_HGA in the
  31-46 recode range, teacher share of OCCUP within [1.5, 6] percent.

A year failing any check aborts loudly rather than shipping bad data.
Output: data/raw/asec/asec_official_{yyyy}.parquet, one row per person
record, consumed by the master build.
"""
import gzip
import io
import os
import re
import urllib.request
import zipfile
import numpy as np
import pandas as pd

RAW = "data/raw/asec"
BASE = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/march/"
FW = {2006: "asec2006_pubuse.zip", 2007: "asec2007_pubuse_tax2.dat.gz",
      2008: "asec2008_pubuse.dat.gz", 2009: "asec2009_pubuse.dat.gz",
      2010: "asec2010_pubuse.dat.gz"}
T90 = {155, 156, 157, 158, 159}
T00 = {2300, 2310, 2320, 2330, 2340}
L = pd.read_csv("outputs/layouts_official.csv")


def find_file(y):
    html = urllib.request.urlopen(BASE.format(y=y), timeout=40).read() \
        .decode("utf-8", "ignore")
    files = re.findall(r'href="([^"]+)"', html)
    cand = [f for f in files if re.search(
        r"(mar|asec)[^\"]*\.(dat\.gz|cps\.gz|pub\.gz|zip)$", f, re.I)
        and not re.search(r"repwgt|ffext|hhext|\.dd\.", f, re.I)]
    pref = [f for f in cand if f.endswith(".gz")]
    return (pref or cand or [None])[0]


def open_lines(path):
    if path.endswith(".zip"):
        zf = zipfile.ZipFile(path)
        inner = [n for n in zf.namelist() if not n.endswith("/")][0]
        return io.TextIOWrapper(zf.open(inner), encoding="latin-1")
    return gzip.open(path, "rt", encoding="latin-1")


def build(y):
    out = f"{RAW}/asec_official_{y}.parquet"
    if os.path.exists(out):
        print(f"{y}: exists", flush=True)
        return
    lay = L[L["asec_year"] == y].set_index("var")
    assert not lay["conflict"].any(), f"{y}: unresolved layout conflicts"
    fname = FW.get(y) or os.path.basename(find_file(y))
    local = f"{RAW}/{fname}"
    if not os.path.exists(local):
        urllib.request.urlretrieve(BASE.format(y=y) + fname, local)
    cols = {v: (int(r["pos"]) - 1, int(r["size"]))
            for v, r in lay.iterrows()}
    recs = {v: [] for v in cols}
    n = 0
    with open_lines(local) as fh:
        for line in fh:
            if not line or line[0] != "3":
                continue
            n += 1
            for v, (o, w) in cols.items():
                recs[v].append(line[o:o + w].strip())
    d = pd.DataFrame(recs)
    for v in d.columns:
        if v != "PERIDNUM":
            d[v] = pd.to_numeric(d[v], errors="coerce")
    if "MARSUPWT" in d:
        d["MARSUPWT"] = d["MARSUPWT"] / 100.0   # two implied decimals
    d["asec_year"] = y

    # sanity confirmations -- abort loudly on failure
    adults = d[d["A_AGE"].between(18, 90)]
    assert 0.55 < len(adults) / len(d) < 0.95, f"{y}: age column broken"
    assert (d["MARSUPWT"] > 0).mean() > 0.90, f"{y}: weight column broken"
    hga = d.loc[d["A_AGE"] >= 25, "A_HGA"]
    assert hga.dropna().between(31, 46).mean() > 0.95, f"{y}: A_HGA broken"
    tcodes = T90 if y <= 2002 else T00
    occ = d.loc[d["OCCUP"] > 0, "OCCUP"]
    tshare = occ.isin(tcodes).mean() * 100
    assert 1.5 < tshare < 6, f"{y}: teacher share {tshare:.2f} out of range"
    pen = d.loc[d["OCCUP"].isin(tcodes) & d["PENPLAN"].isin([1, 2]),
                "PENPLAN"]
    print(f"{y}: n={n} teacher_share={tshare:.2f}% "
          f"pension_teacher={(pen == 1).mean() * 100:.1f}% "
          f"wgt_med={d['MARSUPWT'].median():.0f}", flush=True)
    d.to_parquet(out, index=False)
    os.remove(local)
    print(f"{y}: SAVED {out}", flush=True)


if __name__ == "__main__":
    for y in range(1998, 2011):
        try:
            build(y)
        except Exception as e:
            print(f"{y}: FAILED {type(e).__name__}: {e}", flush=True)
    print("done", flush=True)
