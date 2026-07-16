"""
Calibrate the last-year job variables (LJCW, HRSWK, WKSWORK, PENPLAN) in
the undocumented 2006-2010 ASEC layout, using the March-monthly link as
the anchor -- the same self-validating philosophy as the occupation
calibration, with a validation gate per variable per year:

  LJCW     1-digit column whose government codes (2-4) agree with the
           monthly class-of-worker government codes (1-3) for persons
           currently in their longest job
  HRSWK    2-digit column correlated with monthly usual hours (PEHRUSL1)
  WKSWORK  2-digit column in 0-52 with the mass at 52 among workers
  PENPLAN  1-digit 0/1/2 column whose worker share of 1s is plausible and
           whose teacher rate at survey 2010 is continuous with 2011

Variables failing their gate are left missing, never guessed. Output:
asec_jobs_{yy}.parquet with PERIDNUM + validated columns, consumed by the
master build.
"""
import glob
import gzip
import io
import os
import re
import zipfile
import urllib.request
import numpy as np
import pandas as pd

RAW = "data/raw/asec"
BASE = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/march/"
FW = {2006: "asec2006_pubuse.zip", 2007: "asec2007_pubuse_tax2.dat.gz",
      2008: "asec2008_pubuse.dat.gz", 2009: "asec2009_pubuse.dat.gz",
      2010: "asec2010_pubuse.dat.gz"}
PID_O, CUR_O = 911, 90          # 0-based offsets from the id calibration
CORE = {2300, 2310, 2320, 2330, 2340}


def open_lines(path):
    if path.endswith(".zip"):
        zf = zipfile.ZipFile(path)
        inner = [n for n in zf.namelist() if not n.endswith("/")][0]
        return io.TextIOWrapper(zf.open(inner), encoding="latin-1")
    return gzip.open(path, "rt", encoding="latin-1")


def person_lines(path, limit=None):
    with open_lines(path) as fh:
        n = 0
        for line in fh:
            if line and line[0] == "3":
                yield line.rstrip("\n")
                n += 1
                if limit and n >= limit:
                    return


def num(x, o, w):
    s = x[o:o + w].strip()
    try:
        return int(s)
    except ValueError:
        return None


def calibrate(y):
    out = f"{RAW}/asec_jobs_{str(y)[2:]}.parquet"
    if os.path.exists(out):
        print(f"{y}: exists", flush=True)
        return
    local = f"{RAW}/{FW[y]}"
    if not os.path.exists(local):
        urllib.request.urlretrieve(BASE.format(y=y) + FW[y], local)
    mon = pd.read_parquet(f"{RAW}/mardemo_{y}.parquet")
    hours_of = dict(zip(mon["PERIDNUM"],
                        pd.to_numeric(mon["PEHRUSL1"], errors="coerce")))
    cow_of = dict(zip(mon["PERIDNUM"],
                      pd.to_numeric(mon["PEIO1COW"], errors="coerce")))
    sample = list(person_lines(local, limit=6000))
    L = min(len(x) for x in sample)
    linked = []
    for x in sample:
        pid = x[PID_O:PID_O + 22].strip()
        cur = num(x, CUR_O, 4)
        if pid in hours_of and cur and cur > 0:
            linked.append((x, hours_of.get(pid), cow_of.get(pid)))
    print(f"{y}: linked working sample n={len(linked)}", flush=True)

    # ---- HRSWK: correlation with monthly usual hours ----
    best_h = (None, 0.0)
    hrs = np.array([h if h and h > 0 else np.nan for _, h, _ in linked],
                   dtype=float)
    for o in range(0, L - 2):
        v = np.array([num(x, o, 2) for x, _, _ in linked], dtype=float)
        ok = ~np.isnan(v) & ~np.isnan(hrs) & (v > 0)
        if ok.sum() < 400 or v[ok].std() < 1:
            continue
        r = np.corrcoef(v[ok], hrs[ok])[0, 1]
        if r > best_h[1]:
            best_h = (o, r)
    ho, hr = best_h
    # ---- LJCW: government agreement with monthly class of worker ----
    best_c = (None, 0.0)
    gov_m = np.array([1 if c and c in (1, 2, 3) else 0 if c else -1
                      for _, _, c in linked])
    for o in range(0, L - 1):
        v = np.array([num(x, o, 1) for x, _, _ in linked], dtype=float)
        ok = ~np.isnan(v) & (v >= 1) & (v <= 7) & (gov_m >= 0)
        if ok.sum() < 400 or len(np.unique(v[ok])) < 3:
            continue
        gov_a = np.isin(v[ok], (2, 3, 4)).astype(int)
        agree = (gov_a == gov_m[ok]).mean()
        share = gov_a.mean()
        if 0.1 < share < 0.4 and agree > best_c[1]:
            best_c = (o, agree)
    co, ca = best_c
    # ---- WKSWORK: 0-52 with mass at 52 among workers ----
    best_w = (None, 0.0)
    for o in range(0, L - 2):
        v = np.array([num(x, o, 2) for x, _, _ in linked], dtype=float)
        ok = ~np.isnan(v)
        if ok.sum() < 500 or v[ok].max() > 52 or v[ok].max() < 52:
            continue
        m52 = (v[ok] == 52).mean()
        if 0.5 < m52 < 0.9 and m52 > best_w[1]:
            best_w = (o, m52)
    wo, wm = best_w
    # ---- PENPLAN: 0/1/2, worker share of 1s plausible ----
    pen_cands = []
    for o in range(0, L - 1):
        v = np.array([num(x, o, 1) for x, _, _ in linked], dtype=float)
        ok = ~np.isnan(v)
        if ok.sum() < 500 or not set(np.unique(v[ok])) <= {0, 1, 2}:
            continue
        pos = v[ok][v[ok] > 0]
        if len(pos) / ok.sum() < 0.7:
            continue
        s1 = (pos == 1).mean()
        if 0.35 < s1 < 0.75:
            pen_cands.append((o, s1))
    print(f"{y}: HRSWK@{(ho or -1)+1} r={hr:.2f} | LJCW@{(co or -1)+1} "
          f"agree={ca:.2f} | WKSWORK@{(wo or -1)+1} m52={wm:.2f} | "
          f"PENPLAN cands={[(o+1, round(s,2)) for o, s in pen_cands[:4]]}",
          flush=True)

    gates = {"HRSWK": (ho, hr > 0.45), "LJCW": (co, ca > 0.85),
             "WKSWORK": (wo, wm > 0.5)}
    # pension: pick the candidate whose teacher share is 65-85% (validated
    # against tier A 2010->2011 continuity of ~76-77%)
    pen_o = None
    for o, s1 in pen_cands:
        tv = []
        for x in person_lines(local, limit=200000):
            occ = num(x, 907, 4)
            if occ in CORE:
                tv.append(num(x, o, 1))
        tv = [z for z in tv if z in (1, 2)]
        if tv:
            sh = np.mean([z == 1 for z in tv])
            if 0.62 <= sh <= 0.85:
                pen_o = o
                print(f"{y}: PENPLAN@{o+1} teacher share {sh:.2f} -> OK",
                      flush=True)
                break
    recs = {"PERIDNUM": [], "HRSWK": [], "LJCW": [], "WKSWORK": [],
            "PENPLAN": []}
    for x in person_lines(local):
        recs["PERIDNUM"].append(x[PID_O:PID_O + 22].strip())
        recs["HRSWK"].append(num(x, ho, 2)
                             if gates["HRSWK"][1] and ho is not None
                             else None)
        recs["LJCW"].append(num(x, co, 1)
                            if gates["LJCW"][1] and co is not None
                            else None)
        recs["WKSWORK"].append(num(x, wo, 2)
                               if gates["WKSWORK"][1] and wo is not None
                               else None)
        recs["PENPLAN"].append(num(x, pen_o, 1)
                               if pen_o is not None else None)
    d = pd.DataFrame(recs)
    d["asec_year"] = y
    d.to_parquet(out, index=False)
    os.remove(local)
    print(f"{y}: SAVED {out}", flush=True)


if __name__ == "__main__":
    for y in range(2006, 2011):
        try:
            calibrate(y)
        except Exception as e:
            print(f"{y}: ERROR {type(e).__name__}: {e}", flush=True)
    print("done", flush=True)
