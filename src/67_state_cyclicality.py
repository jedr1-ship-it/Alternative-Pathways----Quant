"""
State-level cyclicality of teacher attrition.

Phase 1  recover GESTFIPS for every person-year:
         tier B (surveys 1998-2010): household records of the raw
         fixed-width files already on disk (H_SEQ@2, GESTFIPS@42, both
         from the official dictionaries), merged to persons via PH_SEQ.
         tier A (surveys 2011-2025): the official CSV zips, columns
         PH_SEQ + GESTFIPS from the person file.
         -> data/raw/asec/asec_state_{year}.parquet
Phase 2  state unemployment rates: FRED {ABBR}UR monthly, March value
         of each survey year -> outputs/n_urate_states.csv
Phase 3  per-state weighted LPM of leaver on the state unemployment
         rate at observation (March of survey year), BA+ teachers,
         within-state variation across years. -> outputs/p_state_cycl.csv
"""
import glob
import gzip
import io
import os
import urllib.request
import zipfile
import numpy as np
import pandas as pd

RAW = "data/raw/asec"
FW_FILES = {
    1998: "mar98supp.cps.gz", 1999: "mar99supp.cps.gz",
    2000: "mar00supp.cps.gz", 2001: "mar01supp.dat.gz",
    2002: "mar02supp.dat.gz", 2003: "asec2003.pub.gz",
    2004: "asec2004.zip", 2005: "asec2005_pubuse.pub.gz",
    2006: "asec2006_pubuse.zip", 2007: "asec2007_pubuse_tax2.dat.gz",
    2008: "asec2008_pubuse.dat.gz", 2009: "asec2009_pubuse.dat.gz",
    2010: "asec2010_pubuse.dat.gz"}
CSV_URL = ("https://www2.census.gov/programs-surveys/cps/datasets/"
           "{y}/march/asecpub{yy}csv.zip")
FW_A = {2011: "asec2011_pubuse.dat.gz", 2012: "asec2012_pubuse.dat.gz",
        2013: "asec2013_pubuse.dat.gz",
        2014: "asec2014_pubuse_tax_fix_5x8_2017.dat.gz",
        2015: "asec2015_pubuse.dat.gz",
        2016: "asec2016_pubuse_v3.dat.gz",
        2017: "asec2017_pubuse.dat.gz", 2018: "asec2018_pubuse.dat.gz"}
FIPS_ABBR = {
    1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT",
    10: "DE", 11: "DC", 12: "FL", 13: "GA", 15: "HI", 16: "ID",
    17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
    23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS",
    29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ",
    35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
    41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN",
    48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV",
    55: "WI", 56: "WY"}


def open_lines(path):
    if path.endswith(".zip"):
        zf = zipfile.ZipFile(path)
        inner = [n for n in zf.namelist() if not n.endswith("/")][0]
        return io.TextIOWrapper(zf.open(inner), encoding="latin-1")
    return gzip.open(path, "rt", encoding="latin-1")


# surveys 1998-2000 carry only the 1960-census state code (HG-ST60@40);
# GESTFIPS@42 exists from survey 2001 on
ST60_FIPS = {11: 23, 12: 33, 13: 50, 14: 25, 15: 44, 16: 9,
             21: 36, 22: 34, 23: 42,
             31: 39, 32: 18, 33: 17, 34: 26, 35: 55,
             41: 27, 42: 19, 43: 29, 44: 38, 45: 46, 46: 31, 47: 20,
             51: 10, 52: 24, 53: 11, 54: 51, 55: 54, 56: 37, 57: 45,
             58: 13, 59: 12,
             61: 21, 62: 47, 63: 1, 64: 28,
             71: 5, 72: 22, 73: 40, 74: 48,
             81: 30, 82: 16, 83: 56, 84: 8, 85: 35, 86: 4, 87: 49,
             88: 32,
             91: 53, 92: 41, 93: 6, 94: 2, 95: 15}


def state_tier_b(y):
    out = f"{RAW}/asec_state_{y}.parquet"
    if os.path.exists(out):
        return
    local = f"{RAW}/{FW_FILES[y]}"
    old60 = y <= 2000
    o0, o1 = (39, 41) if old60 else (41, 43)
    hseq, st = [], []
    with open_lines(local) as fh:
        for line in fh:
            if line and line[0] == "1":
                try:
                    hseq.append(int(line[1:6]))
                    st.append(int(line[o0:o1]))
                except ValueError:
                    continue
    d = pd.DataFrame({"PH_SEQ": hseq, "GESTFIPS": st})
    if old60:
        d["GESTFIPS"] = d["GESTFIPS"].map(ST60_FIPS)
    d = d[d["GESTFIPS"].isin(FIPS_ABBR)]
    d["asec_year"] = y
    assert d["GESTFIPS"].nunique() >= 50, f"{y}: state field implausible"
    d.to_parquet(out, index=False)
    print(f"{y}: households={len(d):,} states={d['GESTFIPS'].nunique()}",
          flush=True)


def state_tier_a(y):
    """Surveys 2011-2018: household records of the documented
    fixed-width files (same positions as tier B). Surveys 2019+: the
    hhpub file inside the official CSV zip."""
    out = f"{RAW}/asec_state_{y}.parquet"
    if os.path.exists(out):
        return
    if y <= 2018:
        local = f"{RAW}/{FW_A[y]}"
        if not os.path.exists(local):
            urllib.request.urlretrieve(
                f"https://www2.census.gov/programs-surveys/cps/datasets/"
                f"{y}/march/{FW_A[y]}", local + ".part")
            os.rename(local + ".part", local)
        hseq, st = [], []
        with open_lines(local) as fh:
            for line in fh:
                if line and line[0] == "1":
                    try:
                        hseq.append(int(line[1:6]))
                        st.append(int(line[41:43]))
                    except ValueError:
                        continue
        d = pd.DataFrame({"PH_SEQ": hseq, "GESTFIPS": st})
        os.remove(local)
    else:
        yy = str(y)[2:]
        z = f"{RAW}/asecpub{yy}csv.zip"
        if not os.path.exists(z):
            urllib.request.urlretrieve(CSV_URL.format(y=y, yy=yy),
                                       z + ".part")
            os.rename(z + ".part", z)
        zf = zipfile.ZipFile(z)
        hh = [n for n in zf.namelist() if "hhpub" in n.lower()][0]
        d = pd.read_csv(zf.open(hh), usecols=["H_SEQ", "GESTFIPS"])
        d = d.rename(columns={"H_SEQ": "PH_SEQ"}).drop_duplicates(
            "PH_SEQ")
        os.remove(z)
    d = d[d["GESTFIPS"].isin(FIPS_ABBR)]
    d["asec_year"] = y
    assert d["GESTFIPS"].nunique() >= 50, f"{y}: state field implausible"
    d.to_parquet(out, index=False)
    print(f"{y}: households={len(d):,} states={d['GESTFIPS'].nunique()}",
          flush=True)


def fetch_state_urates():
    out = "outputs/n_urate_states.csv"
    if os.path.exists(out):
        return pd.read_csv(out)
    rows = []
    for fips, ab in FIPS_ABBR.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={ab}UR"
        raw = urllib.request.urlopen(url, timeout=60).read().decode()
        d = pd.read_csv(io.StringIO(raw))
        d["date"] = pd.to_datetime(d["observation_date"])
        mar = d[d["date"].dt.month == 3]
        for _, r in mar.iterrows():
            rows.append({"GESTFIPS": fips, "abbr": ab,
                         "survey_year": r["date"].year,
                         "u_march": float(r[f"{ab}UR"])})
        print(f"  {ab} ok", flush=True)
    U = pd.DataFrame(rows)
    U.to_csv(out, index=False)
    return U


if __name__ == "__main__":
    for y in range(1998, 2011):
        state_tier_b(y)
    for y in range(2011, 2026):
        try:
            state_tier_a(y)
        except Exception as e:
            print(f"{y}: FAILED {type(e).__name__}: {e}", flush=True)
    U = fetch_state_urates()

    # ---- merge and per-state regressions ----
    M = pd.read_parquet("data/processed/asec_master.parquet")
    T = M[(M["teacher"] == 1) & (M["ba_plus"] == 1) & (M["A_AGE"] >= 18)
          & M["WGT"].notna() & M["leaver"].notna()]
    S = pd.concat([pd.read_parquet(f) for f in
                   sorted(glob.glob(f"{RAW}/asec_state_*.parquet"))],
                  ignore_index=True)
    T = T.merge(S, on=["asec_year", "PH_SEQ"], how="left")
    print(f"teachers with state: {T['GESTFIPS'].notna().mean()*100:.1f}%",
          flush=True)
    T = T.dropna(subset=["GESTFIPS"])
    T["survey_year"] = T["asec_year"]
    T = T.merge(U, on=["GESTFIPS", "survey_year"], how="left")
    T = T.dropna(subset=["u_march"])

    res = []
    for (fips, ab), g in T.groupby(["GESTFIPS", "abbr"]):
        if len(g) < 400 or g["u_march"].std() < 0.5:
            continue
        # weighted LPM: leaver on state unemployment at observation
        x = g["u_march"].values
        yv = g["leaver"].values
        w = g["WGT"].values
        xm = np.average(x, weights=w)
        ym = np.average(yv, weights=w)
        b = (np.sum(w * (x - xm) * (yv - ym))
             / np.sum(w * (x - xm) ** 2))
        a = ym - b * xm
        e = yv - a - b * x
        # HC1-style robust SE
        se = np.sqrt(np.sum((w * (x - xm) * e) ** 2)
                     / np.sum(w * (x - xm) ** 2) ** 2)
        res.append({"abbr": ab, "GESTFIPS": int(fips), "n": len(g),
                    "beta_pp": round(b * 100, 2),
                    "se_pp": round(se * 100, 2),
                    "mean_leave": round(ym * 100, 2)})
    R = pd.DataFrame(res).sort_values("beta_pp")
    R.to_csv("outputs/p_state_cycl.csv", index=False)
    print(R.to_string(index=False))
