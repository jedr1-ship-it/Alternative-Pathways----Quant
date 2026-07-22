import os
import re
import subprocess
import pandas as pd
import gzip
import io
import urllib.request
import zipfile
import numpy as np
import glob


DOCS = "data/raw/docs"

WANT = {
    "OCCUP", "PEIOOCC", "A-AGE", "A-SEX", "A-HGA", "A-LFSR", "A-MARITL",
    "A-CLSWKR", "A-USLHRS", "LJCW", "HRSWK", "WKSWORK", "PENPLAN",
    "MARSUPWT", "PERIDNUM", "PRDTRACE", "A-RACE", "A-PARENT", "A-SPOUSE",
    "A-FAMREL", "WSAL-VAL", "PEARNVAL", "A-MJOCC", "A-DTOCC", "PEMLR",
    "A-WKSTAT", "A-UNTYPE", "PUBLICEMP", "PH-SEQ", "A-LINENO", "A-EXPRRP",
    "A-OCC",
}
PAT = re.compile(r"\bD\s+([A-Z][A-Z0-9-]{1,11})\s+(\d{1,2})\s+(\d{1,4})\b")

rows = []
for yy in [f"{v:02d}" for v in list(range(98, 100)) + list(range(0, 11))]:
    pdf = f"{DOCS}/cpsmar{yy}.pdf"
    txt = f"{DOCS}/cpsmar{yy}.txt"
    if not os.path.exists(pdf):
        continue
    if not os.path.exists(txt):
        subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    year = 1900 + int(yy) if int(yy) >= 90 else 2000 + int(yy)
    seen = {}
    for line in open(txt, encoding="utf-8", errors="ignore"):
        for name, size, pos in PAT.findall(line):
            if name not in WANT:
                continue
            key = (name, int(size), int(pos))
            seen.setdefault(name, set()).add(key[1:])
    for name, combos in sorted(seen.items()):
        for size, pos in sorted(combos):
            rows.append({"asec_year": year,
                         "var": name.replace("-", "_"),
                         "size": size, "pos": pos,
                         "conflict": int(len(combos) > 1)})

L = pd.DataFrame(rows)
L.to_csv("outputs/layouts_official.csv", index=False)
piv = L[L["conflict"] == 0].pivot_table(index="var", columns="asec_year",
                                        values="pos")
print(piv.to_string())
nc = L[L["conflict"] == 1]
if len(nc):
    print("\nCONFLICTS (same name, several positions):")
    print(nc.to_string(index=False))


RAW = "data/raw/asec"
BASE = "https://www2.census.gov/programs-surveys/cps/datasets/{y}/march/"
FW = {2004: "asec2004.zip",
      2006: "asec2006_pubuse.zip", 2007: "asec2007_pubuse_tax2.dat.gz",
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
    for attempt in range(4):
        if os.path.exists(local):
            break
        try:
            urllib.request.urlretrieve(BASE.format(y=y) + fname,
                                       local + ".part")
            os.rename(local + ".part", local)
        except Exception as e:
            print(f"{y}: download attempt {attempt+1} failed ({e})",
                  flush=True)
            for p in (local + ".part",):
                if os.path.exists(p):
                    os.remove(p)
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
        d["MARSUPWT"] = d["MARSUPWT"] / 100.0
    d["asec_year"] = y


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
    print(f"{y}: SAVED {out}", flush=True)


if __name__ == "__main__":
    for y in range(1998, 2011):
        try:
            build(y)
        except Exception as e:
            print(f"{y}: FAILED {type(e).__name__}: {e}", flush=True)
    print("done", flush=True)


RAW = "data/raw/asec"
OUT = "data/processed"
CORE = {2300, 2310, 2320, 2330}
T90 = {155, 156, 157, 158, 159}


def tset(ay):
    if ay <= 2002:
        return T90
    return CORE | ({2340} if ay <= 2019 else {2360})


def add_children(R, ptr_cols):
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

    R["WGT"] = R["MARSUPWT"] / 100.0
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


teach = pd.Series(False, index=M.index)
still = pd.Series(False, index=M.index)
for ay, g in M.groupby("asec_year"):
    cs = tset(int(ay))
    teach.loc[g.index] = g["OCCUP"].isin(cs)
    still.loc[g.index] = g["PEIOOCC"].isin(cs)
M["teacher"] = teach.astype(int)

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
