"""
Empirically calibrate the pre-2011 fixed-width ASEC record layout so the
confusion table reaches back to cohort 2005. The Census WAF blocks the old
data dictionaries, so instead of guessing byte positions we FIND them, with
two self-validating anchors against the March basic monthly file (whose
PERIDNUM and PTIO1OCD we already parse with a documented layout):

  1. PERIDNUM offset: scan every offset for the 22-character slice that
     matches the March monthly PERIDNUM set. A 22-char join cannot match by
     accident.
  2. PEIOOCC offset: the ASEC interview happens with the March basic
     interview, so the current-occupation column must agree with the
     monthly PTIO1OCD for the linked persons.
  3. OCCUP offset (longest job LAST year): among occupation-shaped columns,
     the one that is populated (>0) for people whose current occupation is
     absent (worked last year, not employed in March) -- a duplicate of the
     current-occ column cannot do that.

Each year 2006-2010 is calibrated independently; results are printed so any
layout drift between years is visible. Output: asec_id_{yy}.parquet.
"""
import io
import os
import re
import gzip
import zipfile
import urllib.request
import pandas as pd

ARAW = "data/raw/asec"
RAW = "data/raw/cps"
CORE = {2300, 2310, 2320, 2330}
BASE = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/march/"


def find_data_file(y):
    html = urllib.request.urlopen(BASE.format(y=y), timeout=30).read() \
        .decode("utf-8", "ignore")
    files = re.findall(r'href="([^"]+)"', html)
    cand = [f for f in files
            if re.search(r"(asec|mar).*\.(dat\.gz|zip|pub\.gz)$", f, re.I)
            and "repwgt" not in f.lower() and "dd" not in f.lower()]
    cand.sort(key=lambda f: ("tax" not in f, not f.endswith(".dat.gz"), f))
    return cand[0] if cand else None


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


def calibrate(y):
    yy = str(y)[2:]
    out = f"{ARAW}/asec_id_{yy}.parquet"
    if os.path.exists(out):
        print(f"{y}: exists", flush=True)
        return
    fname = find_data_file(y)
    local = f"{ARAW}/{os.path.basename(fname)}"
    if not os.path.exists(local):
        urllib.request.urlretrieve(BASE.format(y=y) + fname, local)

    mon = pd.read_parquet(f"{RAW}/slim_{y}_03.parquet",
                          columns=["PERIDNUM", "PTIO1OCD", "PEMLR"])
    pset = set(mon["PERIDNUM"])
    occ_of = dict(zip(mon["PERIDNUM"], mon["PTIO1OCD"]))

    sample = list(person_lines(local, limit=4000))
    L = min(len(x) for x in sample)

    # ---- 1. find PERIDNUM offset ----
    best_o, best_hit = None, 0.0
    for o in range(0, L - 22):
        hits = sum(1 for x in sample[:800] if x[o:o + 22] in pset)
        if hits > best_hit:
            best_o, best_hit = o, hits
    hit_rate = best_hit / 800 * 100
    print(f"{y}: PERIDNUM offset {best_o + 1} (match {hit_rate:.0f}%)",
          flush=True)
    if hit_rate < 30:
        print(f"{y}: FAILED peridnum scan", flush=True)
        os.remove(local)
        return
    po = best_o

    # linked sample with known current occupation from the monthly file
    linked = [(x, occ_of[x[po:po + 22]]) for x in sample
              if x[po:po + 22] in occ_of]
    lk_emp = [(x, c) for x, c in linked if c and c > 0]

    def parse4(x, o):
        s = x[o:o + 4].strip()
        try:
            return int(s)
        except ValueError:
            return None

    # ---- 2. find PEIOOCC: max agreement with monthly PTIO1OCD ----
    best = (None, 0.0)
    for o in range(0, L - 4):
        ag = sum(1 for x, c in lk_emp[:600] if parse4(x, o) == c)
        r = ag / min(len(lk_emp), 600)
        if r > best[1]:
            best = (o, r)
    eo, er = best
    print(f"{y}: PEIOOCC offset {eo + 1} (agreement {er*100:.0f}%)",
          flush=True)

    # ---- 3. find OCCUP: occupation-shaped, populated when PEIOOCC absent --
    lk_non = [x for x, c in linked
              if (parse4(x, eo) or 0) <= 0]     # not employed in March
    cand = []
    for o in range(0, L - 4):
        if abs(o - eo) < 4:
            continue
        vals = [parse4(x, o) for x, c in lk_emp[:400]]
        vals = [v for v in vals if v is not None]
        if not vals:
            continue
        pos = [v for v in vals if v > 0]
        if len(pos) < 200:
            continue
        tsh = sum(v in CORE for v in pos) / len(pos) * 100
        if not (0.5 < tsh < 8):
            continue
        agree = sum(1 for x, c in lk_emp[:400] if parse4(x, o) == c) \
            / min(len(lk_emp), 400)
        if not (0.3 < agree < 0.97):
            continue
        # discriminator: >0 while current occ <=0 (worked last yr, not now)
        r_non = sum(1 for x in lk_non[:300] if (parse4(x, o) or 0) > 0) \
            / max(len(lk_non[:300]), 1)
        cand.append((o, agree, r_non, tsh))
    cand.sort(key=lambda t: (-t[2], -t[1]))
    if not cand:
        print(f"{y}: FAILED occup scan", flush=True)
        os.remove(local)
        return
    oo, oagree, onon, otsh = cand[0]
    print(f"{y}: OCCUP offset {oo + 1} (agree cur {oagree*100:.0f}%, "
          f">0 when not employed {onon*100:.0f}%, teacher {otsh:.1f}%)",
          flush=True)

    # ---- full extraction with the calibrated offsets ----
    recs = {"PERIDNUM": [], "PEIOOCC": [], "OCCUP": []}
    for x in person_lines(local):
        recs["PERIDNUM"].append(x[po:po + 22])
        recs["PEIOOCC"].append(x[eo:eo + 4])
        recs["OCCUP"].append(x[oo:oo + 4])
    d = pd.DataFrame(recs)
    for v in ("PEIOOCC", "OCCUP"):
        d[v] = pd.to_numeric(d[v].str.strip(), errors="coerce")
    match = d["PERIDNUM"].isin(pset).mean() * 100
    posocc = d[d["OCCUP"] > 0]
    tshare = posocc["OCCUP"].isin(CORE).mean() * 100
    print(f"{y}: extracted {len(d):,} | PERIDNUM match {match:.0f}% | "
          f"teacher share {tshare:.1f}%", flush=True)
    if match > 40 and 1.0 < tshare < 6.0:
        d.to_parquet(out, index=False)
        print(f"{y}: SAVED {out}", flush=True)
    else:
        print(f"{y}: REJECTED after full pass", flush=True)
    os.remove(local)


if __name__ == "__main__":
    for y in range(2006, 2011):
        try:
            calibrate(y)
        except Exception as e:
            print(f"{y}: ERROR {type(e).__name__}: {e}", flush=True)
    print("done", flush=True)
