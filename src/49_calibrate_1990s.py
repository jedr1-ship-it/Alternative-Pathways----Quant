"""
Extend the attrition series into the 1990s. Census hosts the March
supplements from 1998 (survey year) onward; surveys 1998-2002 use the 1990
census occupation codes (3-digit; K-12 teachers 155-159, aides 387) and
2003-2005 the 2000-census 4-digit codes (2300-2340). No published
machine-readable dictionaries survive for these files, so byte positions
are recovered empirically with self-validating anchors:

  A_AGE     2-digit column with a human age distribution
  OCCUP     occupation of longest job last year: occupation-shaped column
            with MORE positive entries than the current one (anyone who
            worked last year vs employed in March)
  PEIOOCC   current occupation: agrees with OCCUP for 60-95% of the
            both-positive rows (most March workers kept last year's job)
  A_HGA     2-digit education recode 31-46 (coding fixed since 1992),
            BA+ share 20-35% of adults
  MARSUPWT  8-digit positive weight

Validation gates per year: teacher share of OCCUP in [1.5, 6]%, leaver
rate in [3, 15]%, or the year is rejected. Output: asec_90s_{yyyy}.parquet
with OCCUP/PEIOOCC/A_AGE/A_HGA/MARSUPWT.
"""
import gzip
import io
import os
import re
import urllib.request
import zipfile
from collections import Counter
import pandas as pd

RAW = "data/raw/asec"
BASE = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/march/"
T90 = {155, 156, 157, 158, 159}
T00 = {2300, 2310, 2320, 2330, 2340}


def find_file(y):
    try:
        html = urllib.request.urlopen(BASE.format(y=y), timeout=40).read() \
            .decode("utf-8", "ignore")
    except Exception:
        return None
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
    yyyy = str(y)
    out = f"{RAW}/asec_90s_{yyyy}.parquet"
    if os.path.exists(out):
        print(f"{y}: exists", flush=True)
        return
    fname = find_file(y)
    if not fname:
        print(f"{y}: no data file found", flush=True)
        return
    local = f"{RAW}/{os.path.basename(fname)}"
    if not os.path.exists(local):
        urllib.request.urlretrieve(BASE.format(y=y) + fname, local)
    sample = list(person_lines(local, limit=5000))
    if len(sample) < 1000:
        print(f"{y}: too few person lines ({len(sample)})", flush=True)
        os.remove(local)
        return
    L = min(len(x) for x in sample)
    tset, wocc = (T90, 3) if y <= 2002 else (T00, 4)

    # --- age column ---
    age_cands = []
    for o in range(0, L - 2):
        v = [num(x, o, 2) for x in sample[:600]]
        v = [z for z in v if z is not None]
        if len(v) < 550:
            continue
        if all(0 <= z <= 99 for z in v):
            kids = sum(z < 18 for z in v) / len(v)
            adults = sum(18 <= z <= 90 for z in v) / len(v)
            med = sorted(v)[len(v) // 2]
            if 0.15 < kids < 0.4 and adults > 0.6 and 25 < med < 45:
                age_cands.append((o, kids))
    if not age_cands:
        print(f"{y}: no age column", flush=True)
        os.remove(local)
        return
    ao = age_cands[0][0]

    # --- occupation-shaped columns ---
    occ_cands = []
    for o in range(0, L - wocc):
        v = [num(x, o, wocc) for x in sample[:800]]
        ok = [z for z in v if z is not None]
        if len(ok) < 700:
            continue
        pos = [z for z in ok if z > 0]
        if not (0.25 < len(pos) / len(ok) < 0.75):
            continue
        tsh = sum(z in tset for z in pos) / max(len(pos), 1)
        if 0.01 < tsh < 0.08:
            occ_cands.append(o)
    pairs = []
    for a in occ_cands:
        for b in occ_cands:
            if abs(a - b) < wocc:
                continue
            both = [(num(x, a, wocc), num(x, b, wocc)) for x in sample[:800]]
            both = [(p, q) for p, q in both if p and q and p > 0 and q > 0]
            if len(both) < 150:
                continue
            agree = sum(p == q for p, q in both) / len(both)
            if 0.55 < agree < 0.97:
                pa = sum(1 for x in sample[:800] if (num(x, a, wocc) or 0) > 0)
                pb = sum(1 for x in sample[:800] if (num(x, b, wocc) or 0) > 0)
                pairs.append((a, b, agree, pa, pb))
    if not pairs:
        print(f"{y}: no occupation pair", flush=True)
        os.remove(local)
        return
    pairs.sort(key=lambda t: -t[2])
    a, b, agree, pa, pb = pairs[0]
    oo, eo = (a, b) if pa >= pb else (b, a)   # OCCUP has the larger base

    # --- education column (A_HGA 31-46) ---
    hga = None
    for o in range(0, L - 2):
        v = [num(x, o, 2) for x in sample[:600]
             if (num(x, ao, 2) or 0) >= 25]
        v = [z for z in v if z is not None]
        if len(v) < 300:
            continue
        if all(0 <= z <= 46 for z in v) and \
                sum(31 <= z <= 46 for z in v) / len(v) > 0.9:
            ba = sum(z >= 43 for z in v) / len(v)
            if 0.15 < ba < 0.45:
                hga = o
                break
    # --- weight column (8-digit positive) ---
    wt = None
    for o in range(0, L - 8):
        v = [num(x, o, 8) for x in sample[:300]]
        v = [z for z in v if z is not None]
        if len(v) == 300 and all(z > 0 for z in v) \
                and 2e5 < sorted(v)[150] < 5e7:
            wt = o
            break

    # --- full extraction ---
    recs = {"OCCUP": [], "PEIOOCC": [], "A_AGE": [], "A_HGA": [],
            "MARSUPWT": []}
    for x in person_lines(local):
        recs["OCCUP"].append(num(x, oo, wocc))
        recs["PEIOOCC"].append(num(x, eo, wocc))
        recs["A_AGE"].append(num(x, ao, 2))
        recs["A_HGA"].append(num(x, hga, 2) if hga is not None else None)
        recs["MARSUPWT"].append(num(x, wt, 8) if wt is not None else None)
    d = pd.DataFrame(recs)
    base = d[d["OCCUP"].isin(tset)]
    lv = (~base["PEIOOCC"].isin(tset)).mean() * 100
    posocc = d[d["OCCUP"].notna() & (d["OCCUP"] > 0)]
    tsh = posocc["OCCUP"].isin(tset).mean() * 100
    print(f"{y}: occ@{oo+1}/cur@{eo+1}/age@{ao+1}"
          f"/hga@{(hga or -1)+1}/wt@{(wt or -1)+1} agree {agree*100:.0f}% | "
          f"teachers n={len(base):,} share {tsh:.1f}% | leaver {lv:.1f}%",
          flush=True)
    if 1.5 < tsh < 6 and 3 < lv < 15 and len(base) > 1500:
        d["asec_year"] = y
        d.to_parquet(out, index=False)
        print(f"{y}: SAVED", flush=True)
    else:
        print(f"{y}: REJECTED", flush=True)
    os.remove(local)


if __name__ == "__main__":
    for y in range(1998, 2006):
        try:
            calibrate(y)
        except Exception as e:
            print(f"{y}: ERROR {type(e).__name__}: {e}", flush=True)
    print("done", flush=True)
