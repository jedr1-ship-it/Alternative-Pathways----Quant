"""
THE unified master database. One script, one output, one codebook.

data/processed/asec_master.parquet -- one row per ASEC person-year for
every extractable survey year, with a `tier` column stating what that
year's source supports:

  tier A  surveys 2011-2025 (cal 2010-2024): full ASEC extraction --
          identifiers, family pointers, demographics, last-year job
          (occupation, weeks, hours, earnings, pension, class of worker),
          current status, supplement weights.
  tier B  surveys 2006-2010 (cal 2005-2009): calibrated old-layout ASEC
          (PERIDNUM, OCCUP, PEIOOCC) enriched by PERIDNUM-link to the
          March basic monthly file: age, sex, education, race, marital
          status, own children, current hours/class-of-worker, monthly
          weight. Last-year job detail (weeks, earnings, pension) does
          not exist for this tier.
  tier C  surveys 1998-2002 (cal 1997-2001): occupation pair only
          (1990 census codes), unweighted. Rate series only.

Derived once, identically for every year the inputs allow: teacher (era-
consistent codes), leaver and its routes, children variables, covariates.
outputs/codebook.csv lists every variable with its coverage.
"""
import glob
import os
import re
import zipfile
import urllib.request
import numpy as np
import pandas as pd

RAW = "data/raw/asec"
MON = "data/raw/cps"
OUT = "data/processed"
CORE = {2300, 2310, 2320, 2330}
T90 = {155, 156, 157, 158, 159}


def tset(ay):
    if ay <= 2002:
        return T90
    return CORE | ({2340} if ay <= 2019 else {2360})


# ---------------- tier B: March monthly demographics 2006-2010 ------------
MCOLS = [("HRHHID", 1, 15, str), ("HRHHID2", 71, 75, str),
         ("PULINENO", 147, 148, int), ("PRTAGE", 122, 123, int),
         ("PEMARITL", 125, 126, int), ("PESEX", 129, 130, int),
         ("PEEDUCA", 137, 138, int), ("PTDTRACE", 139, 140, int),
         ("PEHRUSL1", 218, 219, int), ("PEIO1COW", 432, 433, int),
         ("PWSSWGT", 613, 622, float), ("PRCHLD", 633, 634, int),
         ("PRNMCHLD", 635, 636, int)]
MSPECS = [(s - 1, e) for _, s, e, _ in MCOLS]
MNAMES = [n for n, *_ in MCOLS]


def march_monthly_demo(year):
    """Demographics from the March basic monthly file, keyed by PERIDNUM."""
    cache = f"{RAW}/mardemo_{year}.parquet"
    if os.path.exists(cache):
        return pd.read_parquet(cache)
    src = f"{MON}/cpsb{year}03.zip"
    if not os.path.exists(src):
        tag = f"mar{str(year)[2:]}pub.zip"
        src = f"{MON}/{tag}"
        if not os.path.exists(src):
            urllib.request.urlretrieve(
                f"https://www2.census.gov/programs-surveys/cps/datasets/"
                f"{year}/basic/{tag}", src)
    zf = zipfile.ZipFile(src)
    d = pd.read_fwf(zf.open(zf.namelist()[0]), colspecs=MSPECS,
                    names=MNAMES, dtype=str)
    for n, _, _, t in MCOLS:
        if t is not str:
            d[n] = pd.to_numeric(d[n], errors="coerce")
    d["HRHHID"] = d["HRHHID"].str.strip()
    d["HRHHID2"] = d["HRHHID2"].str.strip().str.zfill(5)
    d["PULINENO"] = (d["PULINENO"].astype("Int64").astype(str).str.zfill(2))
    d["PERIDNUM"] = d["HRHHID"] + d["HRHHID2"] + d["PULINENO"]
    d["PWSSWGT"] = pd.to_numeric(d["PWSSWGT"], errors="coerce") / 1e4
    d = d.drop(columns=["HRHHID", "HRHHID2", "PULINENO"])
    d.to_parquet(cache, index=False)
    return d


def build_tier_b():
    parts = []
    for ay in range(2006, 2011):
        a = pd.read_parquet(f"{RAW}/asec_id_{str(ay)[2:]}.parquet")
        for c in ("OCCUP", "PEIOOCC"):
            a[c] = pd.to_numeric(a[c], errors="coerce")
        m = march_monthly_demo(ay)
        d = a.merge(m, on="PERIDNUM", how="left")
        d["asec_year"] = ay
        # map monthly variables into the master's unified names
        d["A_AGE"] = d.pop("PRTAGE")
        d["A_SEX"] = d.pop("PESEX")
        d["A_HGA"] = d.pop("PEEDUCA")          # same 31-46 coding
        d["PRDTRACE"] = d.pop("PTDTRACE")      # 1=white, 2=black in both
        d["A_MARITL"] = d.pop("PEMARITL")      # 1-3 married in both
        d["child_u6"] = d.pop("PRCHLD").isin([1, 2, 3, 5, 6, 7,
                                              9, 11]).astype(float)
        d["n_children"] = d.pop("PRNMCHLD").clip(lower=0)
        d["cur_parttime"] = d.pop("PEHRUSL1").between(1, 34).astype(float)
        d["cur_public"] = d.pop("PEIO1COW").isin([1, 2, 3]).astype(float)
        d["WGT"] = d.pop("PWSSWGT")            # monthly person weight
        d["linked_demo"] = d["A_AGE"].notna().astype(int)
        d["tier"] = "B"
        parts.append(d)
        print(f"  tier B {ay}: {len(d):,} persons, demo linked "
              f"{d['linked_demo'].mean()*100:.0f}%", flush=True)
    return pd.concat(parts, ignore_index=True)


def build_tier_a():
    parts = []
    for f in sorted(glob.glob(f"{RAW}/asec_rich_*.parquet")):
        d = pd.read_parquet(f)
        for c in d.columns:
            if c != "PERIDNUM":
                d[c] = pd.to_numeric(d[c], errors="coerce")
        parts.append(d)
    R = pd.concat(parts, ignore_index=True)
    # children from the household parent/spouse pointers
    ptr = []
    for c in ["A_PARENT", "PEPAR1", "PEPAR2"]:
        k = R[(pd.to_numeric(R[c], errors="coerce") > 0)
              & (R["A_AGE"] < 18)][["asec_year", "PH_SEQ", c,
                                    "A_AGE", "A_LINENO"]].rename(
            columns={c: "pl", "A_LINENO": "kl"})
        ptr.append(k)
    kids = pd.concat(ptr).drop_duplicates(["asec_year", "PH_SEQ", "pl",
                                           "kl"])
    agg = kids.groupby(["asec_year", "PH_SEQ", "pl"])["A_AGE"].agg(
        n_children="size", child_u6=lambda s: float((s < 6).any()),
        new_baby=lambda s: float((s < 1).any())).reset_index().rename(
        columns={"pl": "A_LINENO"})
    R = R.merge(agg, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
    sp = R[R["A_SPOUSE"] > 0][["asec_year", "PH_SEQ", "A_SPOUSE",
                               "n_children", "child_u6", "new_baby"]]
    sp = sp.rename(columns={"A_SPOUSE": "A_LINENO", "n_children": "n2",
                            "child_u6": "c2", "new_baby": "b2"})
    sp = sp.groupby(["asec_year", "PH_SEQ", "A_LINENO"]).max().reset_index()
    R = R.merge(sp, on=["asec_year", "PH_SEQ", "A_LINENO"], how="left")
    for a, b in [("n_children", "n2"), ("child_u6", "c2"),
                 ("new_baby", "b2")]:
        R[a] = R[[a, b]].max(axis=1).fillna(0)
    R = R.drop(columns=["n2", "c2", "b2"])
    R["WGT"] = R["MARSUPWT"]
    R["tier"] = "A"
    print(f"  tier A: {len(R):,} persons, surveys "
          f"{int(R['asec_year'].min())}-{int(R['asec_year'].max())}",
          flush=True)
    return R


def build_tier_c():
    parts = []
    for f in sorted(glob.glob(f"{RAW}/asec_90s_*.parquet")):
        d = pd.read_parquet(f)
        for c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d["tier"] = "C"
        parts.append(d)
    C = pd.concat(parts, ignore_index=True)
    print(f"  tier C: {len(C):,} persons, surveys "
          f"{int(C['asec_year'].min())}-{int(C['asec_year'].max())}",
          flush=True)
    return C


M = pd.concat([build_tier_a(), build_tier_b(), build_tier_c()],
              ignore_index=True)
M["cal_year"] = M["asec_year"] - 1

# ---------------- unified derivations ----------------
teach = pd.Series(False, index=M.index)
still = pd.Series(False, index=M.index)
for ay, g in M.groupby("asec_year"):
    cs = tset(int(ay))
    teach.loc[g.index] = g["OCCUP"].isin(cs)
    still.loc[g.index] = g["PEIOOCC"].isin(cs)
M["teacher"] = teach.astype(int)
# routes: tier A has current labor-force status; B/C occupation pair only
emp = M["A_LFSR"].isin([1, 2]) if "A_LFSR" in M else pd.Series(False,
                                                               M.index)
M["switch"] = np.where(M["tier"] == "A",
                       (emp & ~still).astype(float), np.nan)
M["unemp"] = np.where(M["tier"] == "A",
                      M["A_LFSR"].isin([3, 4]).astype(float), np.nan)
M["leftlf"] = np.where(M["tier"] == "A",
                       (~M["A_LFSR"].isin([1, 2, 3, 4])).astype(float),
                       np.nan)
M["leaver"] = np.where(M["tier"] == "A",
                       ((M["switch"] == 1) | (M["unemp"] == 1)
                        | (M["leftlf"] == 1)).astype(float),
                       (~still).astype(float))   # B/C: occupation pair
M["female"] = (M["A_SEX"] == 2).astype(float)
M["black"] = (M["PRDTRACE"] == 2).astype(float)
M["married"] = M["A_MARITL"].isin([1, 2, 3]).astype(float)
M["ba_plus"] = (M["A_HGA"] >= 43).astype(float)
M["ma_plus"] = (M["A_HGA"] >= 44).astype(float)
M["pension"] = np.where(M["tier"] == "A",
                        (M["PENPLAN"] == 1).astype(float), np.nan)
M["parttime_ly"] = np.where(M["tier"] == "A",
                            M["HRSWK"].between(1, 34).astype(float),
                            np.nan)
M["fullyear"] = np.where(M["tier"] == "A",
                         (M["WKSWORK"] >= 50).astype(float), np.nan)
M["public_ly"] = np.where(M["tier"] == "A",
                          M["LJCW"].isin([2, 3, 4]).astype(float), np.nan)

KEEP = ["asec_year", "cal_year", "tier", "PERIDNUM", "WGT", "teacher",
        "leaver", "switch", "unemp", "leftlf", "OCCUP", "PEIOOCC",
        "A_AGE", "female", "black", "married", "A_MARITL", "A_HGA",
        "ba_plus", "ma_plus", "n_children", "child_u6", "new_baby",
        "pension", "parttime_ly", "fullyear", "public_ly", "cur_parttime",
        "cur_public", "WSAL_VAL", "WKSWORK", "HRSWK", "PH_SEQ",
        "A_LINENO", "linked_demo"]
for k in KEEP:
    if k not in M.columns:
        M[k] = np.nan
M = M[KEEP]
os.makedirs(OUT, exist_ok=True)
M.to_parquet(f"{OUT}/asec_master.parquet", index=False)

# ---------------- codebook with coverage ----------------
rows = []
for c in M.columns:
    if c in ("asec_year", "cal_year", "tier"):
        continue
    cov = M.groupby("asec_year")[c].apply(
        lambda s: s.notna().mean() > 0.5 if s.dtype != object
        else s.notna().mean() > 0.5)
    yrs = cov[cov].index.tolist()
    span = f"{min(yrs)}-{max(yrs)}" if yrs else "--"
    rows.append({"variable": c, "surveys_covered": span,
                 "n_nonmissing": int(M[c].notna().sum())})
CB = pd.DataFrame(rows)
CB.to_csv("outputs/codebook.csv", index=False)
print("\n=== MASTER ===")
print(f"rows: {len(M):,}   surveys {int(M['asec_year'].min())}-"
      f"{int(M['asec_year'].max())}   (cal "
      f"{int(M['cal_year'].min())}-{int(M['cal_year'].max())})")
print(M.groupby("tier")["asec_year"].agg(["min", "max", "count"])
      .to_string())
print("\ncodebook -> outputs/codebook.csv")
print(CB.to_string(index=False))
