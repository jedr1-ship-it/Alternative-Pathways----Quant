"""
Extract PERIDNUM/OCCUP/PEIOOCC from the fixed-width ASEC person records for
survey years 2006-2015, completing the confusion-table coverage back to
cohort 2005.

The Census march directories for these years carry the data as .dat.gz,
.zip or .pub.gz, and only 2013-2015 publish a machine-readable dictionary
(asec{y}early_pubuse.dd.txt). Those dictionaries give the SAME positions as
2016-2018 (PERIDNUM 96/22, PEIOOCC 172/4, OCCUP 296/4, MARSUPWT 155/8), so
we apply that layout to every year and VALIDATE it empirically per year:

  (a) the PERIDNUM extracted must match the PERIDNUMs built from the basic
      monthly March file of the same year (HRHHID+HRHHID2+PULINENO) at a
      high rate -- a 22-character join can't match by accident;
  (b) K-12 teacher codes 2300-2330 must be a plausible share of OCCUP.

Years failing validation are reported and skipped, not guessed.
2014 note: we use the tax_fix 5/8 production file (redesign split sample).
"""
import glob
import gzip
import io
import os
import re
import urllib.request
import zipfile
import pandas as pd

ARAW = "data/raw/asec"
RAW = "data/raw/cps"
POS = {"PERIDNUM": (96, 22), "PEIOOCC": (172, 4), "OCCUP": (296, 4),
       "MARSUPWT": (155, 8)}
CORE = {2300, 2310, 2320, 2330}
BASE = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/march/"


def find_data_file(y):
    html = urllib.request.urlopen(BASE.format(y=y), timeout=30).read() \
        .decode("utf-8", "ignore")
    files = re.findall(r'href="([^"]+)"', html)
    cand = [f for f in files
            if re.search(r"(asec|mar).*\.(dat\.gz|zip|pub\.gz)$", f, re.I)
            and "repwgt" not in f.lower() and "dd" not in f.lower()]
    if not cand:
        return None
    # prefer tax-fix / latest production variants, then dat.gz over zip
    cand.sort(key=lambda f: ("tax_fix" not in f, "tax" not in f,
                             not f.endswith(".dat.gz"), f))
    return cand[0]


def open_lines(path):
    if path.endswith(".zip"):
        zf = zipfile.ZipFile(path)
        inner = [n for n in zf.namelist() if not n.endswith("/")][0]
        return io.TextIOWrapper(zf.open(inner), encoding="latin-1")
    return gzip.open(path, "rt", encoding="latin-1")


def extract(y):
    yy = str(y)[2:]
    out = f"{ARAW}/asec_id_{yy}.parquet"
    if os.path.exists(out):
        print(f"  {y}: exists", flush=True)
        return
    fname = find_data_file(y)
    if fname is None:
        print(f"  {y}: NO DATA FILE FOUND", flush=True)
        return
    local = f"{ARAW}/{os.path.basename(fname)}"
    if not os.path.exists(local):
        urllib.request.urlretrieve(BASE.format(y=y) + fname, local)
    recs = {v: [] for v in POS}
    with open_lines(local) as fh:
        for line in fh:
            if not line or line[0] != "3":
                continue
            for v, (s, w) in POS.items():
                recs[v].append(line[s - 1:s - 1 + w])
    d = pd.DataFrame(recs)
    for v in ("PEIOOCC", "OCCUP", "MARSUPWT"):
        d[v] = pd.to_numeric(d[v], errors="coerce")
    d["PERIDNUM"] = d["PERIDNUM"].str.strip()

    # ---- validation (a): PERIDNUM join against the March monthly file ----
    slim = f"{RAW}/slim_{y}_03.parquet"
    ok_join = float("nan")
    if os.path.exists(slim):
        m = pd.read_parquet(slim, columns=["PERIDNUM"])
        ok_join = d["PERIDNUM"].isin(set(m["PERIDNUM"])).mean() * 100
    # ---- validation (b): teacher share of positive OCCUP ----
    pos_occ = d[d["OCCUP"] > 0]
    tshare = pos_occ["OCCUP"].isin(CORE).mean() * 100 if len(pos_occ) else 0
    valid = (ok_join != ok_join or ok_join > 40) and 1.0 < tshare < 6.0
    print(f"  {y}: {len(d):,} persons | PERIDNUM match Mar monthly "
          f"{ok_join:.0f}% | teacher share {tshare:.1f}% -> "
          f"{'OK' if valid else 'REJECTED'}", flush=True)
    if valid:
        d.to_parquet(out, index=False)
    os.remove(local)


if __name__ == "__main__":
    for y in range(2006, 2016):
        try:
            extract(y)
        except Exception as e:
            print(f"  {y}: ERROR {type(e).__name__}: {e}", flush=True)
    print("done", flush=True)
