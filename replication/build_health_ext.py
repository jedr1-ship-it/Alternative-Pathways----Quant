"""Self-reported health (HEA) and work-limiting disability (DIS_HP) for
the 2011-2025 tier-A person files, which were cached without them.
2011-2018: extracted from the Census fixed-width public-use files at the
byte positions in each year's data dictionary. 2019-2025: taken from
data/processed/asec_ext.parquet (the Census CSVs). Each year is matched
to data/raw/asec/asec_rich_YY.parquet on (PH_SEQ, A_LINENO) and checked
on age; where Census publishes more than one 2014 file, the one that
matches the cached sample is kept. Writes data/raw/asec/health_tierA.parquet.
Run from the repo root (needs internet access for 2011-2018)."""
import gzip
import os
import re
import urllib.request
import pandas as pd

RAW = "data/raw/asec"
BASE = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/march/"
PAT = re.compile(r"\bD\s+([A-Z][A-Z0-9_-]{1,11})\s+(\d{1,2})\s+(\d{1,4})\b")
NEED = {"PH-SEQ", "A-LINENO", "A-AGE", "HEA", "DIS-HP"}


def listing(y):
    for _ in range(6):
        try:
            html = urllib.request.urlopen(BASE.format(y=y), timeout=240) \
                .read().decode("utf-8", "ignore")
            return re.findall(r'href="([^"]+)"', html)
        except Exception as e:
            print(f"{y}: listing retry ({e})", flush=True)
    raise RuntimeError(f"{y}: no listing")


def fetch(y, name):
    local = f"{RAW}/{name}"
    for _ in range(6):
        if os.path.exists(local):
            return local
        try:
            urllib.request.urlretrieve(BASE.format(y=y) + name, local + ".part")
            os.rename(local + ".part", local)
        except Exception as e:
            print(f"{y}: download retry {name} ({e})", flush=True)
    raise RuntimeError(f"{y}: could not fetch {name}")


def layout(path):
    pos = {}
    for line in open(path, encoding="latin-1"):
        for name, size, p in PAT.findall(line):
            name = name.replace("_", "-")
            if name in NEED and name not in pos:
                pos[name] = (int(p) - 1, int(size))
    missing = NEED - set(pos)
    assert not missing, f"{path}: missing {missing}"
    return pos


def extract(datfile, pos, y):
    rows = {k: [] for k in pos}
    with gzip.open(datfile, "rt", encoding="latin-1") as fh:
        for line in fh:
            if line[:1] != "3":
                continue
            for k, (o, w) in pos.items():
                rows[k].append(line[o:o + w].strip())
    d = pd.DataFrame(rows).apply(pd.to_numeric, errors="coerce")
    d.columns = [c.replace("-", "_") for c in d.columns]
    d["asec_year"] = y
    return d


def match(d, y):
    r = pd.read_parquet(f"{RAW}/asec_rich_{y % 100:02d}.parquet",
                        columns=["PH_SEQ", "A_LINENO", "A_AGE"])
    r = r.apply(pd.to_numeric, errors="coerce")
    m = r.merge(d, on=["PH_SEQ", "A_LINENO"], how="left",
                suffixes=("", "_raw"))
    ok = (m.A_AGE == m.A_AGE_raw).mean()
    return ok, len(r), len(d)


parts = []
for y in range(2011, 2019):
    files = listing(y)
    dats = [f for f in files if re.search(r"asec\d{4}.*\.dat\.gz$", f, re.I)
            and not re.search(r"repwgt", f, re.I)]
    dicts = [f for f in files if re.search(r"(dd\.txt|data_dict.*\.txt)$",
                                           f, re.I)]
    print(f"{y}: data {dats} dict {dicts}", flush=True)
    best = None
    for dct in dicts:
        try:
            pos = layout(fetch(y, dct))
        except AssertionError as e:
            print(f"{y}: skipping {dct} ({e})", flush=True)
            continue
        for dat in dats:
            d = extract(fetch(y, dat), pos, y)
            ok, nr, nd = match(d, y)
            print(f"{y}: {dat} with {dct}: age match {ok:.4f} "
                  f"(cached {nr:,}, raw {nd:,})", flush=True)
            if best is None or ok > best[0]:
                best = (ok, d)
    assert best and best[0] > 0.99, f"{y}: no raw file matches the cache"
    parts.append(best[1][["asec_year", "PH_SEQ", "A_LINENO", "HEA",
                          "DIS_HP"]])

e = pd.read_parquet("data/processed/asec_ext.parquet",
                    columns=["asec_year", "PH_SEQ", "A_LINENO", "HEA",
                             "DIS_HP"])
parts.append(e)
H = pd.concat(parts, ignore_index=True)
H.to_parquet(f"{RAW}/health_tierA.parquet", index=False)
print(f"saved health_tierA.parquet: {len(H):,} rows, years "
      f"{int(H.asec_year.min())}-{int(H.asec_year.max())}")
