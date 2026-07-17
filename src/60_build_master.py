"""
THE unified master database. One script, one output, one codebook.

data/processed/asec_master.parquet -- one row per ASEC person-year,
surveys 1998-2025 (calendar years 1997-2024), built exclusively from
official Census sources:

  tier A  surveys 2011-2025: the modern machine-readable ASEC files.
  tier B  surveys 1998-2010: the raw fixed-width files read at the byte
          positions published in the official technical documentation
          (cpsmarYY.pdf, parsed by 64, extracted by 65). Same variable
          set as tier A except: no PEPAR1/PEPAR2 (children come from the
          single A_PARENT pointer plus spouse crediting) and no PERIDNUM
          before survey 2005.

Every derivation below runs identically for both tiers: era-consistent
teacher codes, the route-based leaver definition (employment status from
A_LFSR, coded the same way in every year), children, covariates, and the
last-year job detail (weeks, hours, class of worker, pension).
outputs/codebook.csv lists every variable with its coverage.
"""
import glob
import os
import numpy as np
import pandas as pd

RAW = "data/raw/asec"
OUT = "data/processed"
CORE = {2300, 2310, 2320, 2330}
T90 = {155, 156, 157, 158, 159}


def tset(ay):
    if ay <= 2002:
        return T90
    return CORE | ({2340} if ay <= 2019 else {2360})


def add_children(R, ptr_cols):
    """Own children under 18 via household parent pointers, credited to
    both the pointed parent and that parent's spouse."""
    ptr = []
    for c in ptr_cols:
        if c not in R.columns:
            continue
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
    return R.drop(columns=["n2", "c2", "b2"])


def build_tier_a():
    parts = []
    for f in sorted(glob.glob(f"{RAW}/asec_rich_*.parquet")):
        d = pd.read_parquet(f)
        for c in d.columns:
            if c != "PERIDNUM":
                d[c] = pd.to_numeric(d[c], errors="coerce")
        parts.append(d)
    R = pd.concat(parts, ignore_index=True)
    R = add_children(R, ["A_PARENT", "PEPAR1", "PEPAR2"])
    R["WGT"] = R["MARSUPWT"]
    R["tier"] = "A"
    print(f"  tier A: {len(R):,} persons, surveys "
          f"{int(R['asec_year'].min())}-{int(R['asec_year'].max())}",
          flush=True)
    return R


def build_tier_b():
    parts = []
    for y in range(1998, 2011):
        f = f"{RAW}/asec_official_{y}.parquet"
        if not os.path.exists(f):
            print(f"  tier B {y}: MISSING {f}", flush=True)
            continue
        parts.append(pd.read_parquet(f))
    R = pd.concat(parts, ignore_index=True)
    old = R["asec_year"] <= 2002
    # pre-2003 names for the same concepts
    if "A_OCC" in R.columns:
        R.loc[old, "PEIOOCC"] = R.loc[old, "A_OCC"]
    if "A_RACE" in R.columns:
        R.loc[old, "PRDTRACE"] = R.loc[old, "A_RACE"]
    R = add_children(R, ["A_PARENT"])
    R["WGT"] = R["MARSUPWT"]
    R["tier"] = "B"
    print(f"  tier B: {len(R):,} persons, surveys "
          f"{int(R['asec_year'].min())}-{int(R['asec_year'].max())}",
          flush=True)
    return R


M = pd.concat([build_tier_a(), build_tier_b()], ignore_index=True)
M["cal_year"] = M["asec_year"] - 1

# ---------------- unified derivations (identical for both tiers) --------
teach = pd.Series(False, index=M.index)
still = pd.Series(False, index=M.index)
for ay, g in M.groupby("asec_year"):
    cs = tset(int(ay))
    teach.loc[g.index] = g["OCCUP"].isin(cs)
    still.loc[g.index] = g["PEIOOCC"].isin(cs)
M["teacher"] = teach.astype(int)
# routes from the labor-force status recode (same 0-7 coding every year)
has_lfsr = M["A_LFSR"].notna()
emp = M["A_LFSR"].isin([1, 2])
un = M["A_LFSR"].isin([3, 4])
M["switch"] = np.where(has_lfsr, (emp & ~still).astype(float), np.nan)
M["unemp"] = np.where(has_lfsr, un.astype(float), np.nan)
M["leftlf"] = np.where(has_lfsr, (~emp & ~un).astype(float), np.nan)
M["leaver"] = np.where(
    has_lfsr,
    ((M["switch"] == 1) | (M["unemp"] == 1) | (M["leftlf"] == 1))
    .astype(float),
    (~still).astype(float))
M["female"] = (M["A_SEX"] == 2).astype(float)
M["black"] = (M["PRDTRACE"] == 2).astype(float)
M["married"] = M["A_MARITL"].isin([1, 2, 3]).astype(float)
M["ba_plus"] = (M["A_HGA"] >= 43).astype(float)
M["ma_plus"] = (M["A_HGA"] >= 44).astype(float)
M["pension"] = np.where(M["PENPLAN"].notna(),
                        (M["PENPLAN"] == 1).astype(float), np.nan)
M["parttime_ly"] = np.where(M["HRSWK"].notna(),
                            M["HRSWK"].between(1, 34).astype(float),
                            np.nan)
M["fullyear"] = np.where(M["WKSWORK"].notna(),
                         (M["WKSWORK"] >= 50).astype(float), np.nan)
M["public_ly"] = np.where(M["LJCW"].notna(),
                          M["LJCW"].isin([2, 3, 4]).astype(float), np.nan)
M["cur_parttime"] = np.where(M["A_USLHRS"].notna(),
                             M["A_USLHRS"].between(1, 34).astype(float),
                             np.nan)
M["cur_public"] = np.where(M["A_CLSWKR"].notna(),
                           M["A_CLSWKR"].isin([2, 3, 4]).astype(float),
                           np.nan)

KEEP = ["asec_year", "cal_year", "tier", "PERIDNUM", "WGT", "teacher",
        "leaver", "switch", "unemp", "leftlf", "OCCUP", "PEIOOCC",
        "A_AGE", "A_LFSR", "female", "black", "married", "A_MARITL",
        "A_HGA", "ba_plus", "ma_plus", "n_children", "child_u6",
        "new_baby", "pension", "parttime_ly", "fullyear", "public_ly",
        "cur_parttime", "cur_public", "WSAL_VAL", "PEARNVAL", "WKSWORK",
        "HRSWK", "PH_SEQ", "A_LINENO"]
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
    cov = M.groupby("asec_year")[c].apply(lambda s: s.notna().mean() > 0.5)
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
