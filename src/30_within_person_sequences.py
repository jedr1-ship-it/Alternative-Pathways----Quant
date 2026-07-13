"""
Reconstruct the FULL within-person sequence across all 8 month-in-sample
(MIS) interviews, to understand -- before fixing any definition -- how
stable "teacher" status is month to month and how much of the apparent
leaving is reference-week / occupation-coding volatility.

A CPS rotation spell: MIS 1-4 in consecutive months of year y, then MIS 5-8
in the same 4 months of y+1. We pool the raw monthly files, key each person
by (HRHHID, HRHHID2, PULINENO), and lay their status out over MIS 1..8.

Status per interview:
  T teacher (employed, occ 2300-2330)   E employed, other occupation
  U unemployed                          N not in labor force
  . not observed that month

Only the raw files for 2005-2007 survive on disk, which fully cover the
2005 and 2006 base cohorts -- enough to characterize the patterns.
"""
import glob
import os
import re
import numpy as np
import pandas as pd

RAW = "data/raw/cps"
TEACHER = {2300, 2310, 2320, 2330}
COLS = [("HRHHID", 1, 15, str), ("HRMONTH", 16, 17, int),
        ("HRYEAR4", 18, 21, int), ("HRMIS", 63, 64, int),
        ("HRHHID2", 71, 75, str), ("PRTAGE", 122, 123, int),
        ("PESEX", 129, 130, int), ("PTDTRACE", 139, 140, int),
        ("PULINENO", 147, 148, int), ("PEMLR", 180, 181, int),
        ("PWSSWGT", 613, 622, float), ("PTIO1OCD", 860, 863, int)]
SPECS = [(s - 1, e) for _, s, e, _ in COLS]
NAMES = [n for n, *_ in COLS]


def read_month(path):
    import zipfile
    with open(path, "rb") as fh:
        magic = fh.read(2)
    if magic == b"PK":
        zf = zipfile.ZipFile(path)
        src = zf.open(zf.namelist()[0])
        df = pd.read_fwf(src, colspecs=SPECS, names=NAMES, dtype=str)
    else:
        df = pd.read_fwf(path, colspecs=SPECS, names=NAMES,
                         compression="gzip", dtype=str)
    for n, _, _, typ in COLS:
        if typ is not str:
            df[n] = pd.to_numeric(df[n], errors="coerce")
    df["HRHHID"] = df["HRHHID"].str.strip()
    df["HRHHID2"] = df["HRHHID2"].str.strip()
    return df


def status(row):
    if row["PEMLR"] in (1, 2):
        return "T" if row["PTIO1OCD"] in TEACHER else "E"
    if row["PEMLR"] in (3, 4):
        return "U"
    return "N"


def load_raw():
    files = sorted(glob.glob(f"{RAW}/*.zip") + glob.glob(f"{RAW}/*.dat.gz"))
    parts = []
    for f in files:
        b = os.path.basename(f)
        m = re.match(r"cpsb(\d{4})(\d{2})", b)
        if not m:
            continue
        d = read_month(f)
        d = d[d["PRTAGE"] >= 18]
        parts.append(d)
        print(f"  read {b}: {len(d):,}", flush=True)
    return pd.concat(parts, ignore_index=True)


def main():
    d = load_raw()
    d["date"] = d["HRYEAR4"] * 12 + d["HRMONTH"]
    d["st"] = d.apply(status, axis=1)
    d["pid"] = (d["HRHHID"] + "|" + d["HRHHID2"] + "|"
                + d["PULINENO"].astype("Int64").astype(str))

    # keep persons with a consistent sex across their records (link check)
    ok = d.groupby("pid")["PESEX"].transform("nunique") == 1
    d = d[ok]

    # a rotation spell has 8 MIS over 16 months; identify a person's cohort by
    # the earliest date at which they are MIS 1 (start of the spell)
    firsts = (d[d["HRMIS"] == 1].groupby("pid")["date"].min()
              .rename("start_date"))
    d = d.merge(firsts, on="pid", how="inner")
    # months since spell start -> expected MIS position (0-3 -> MIS1-4,
    # 12-15 -> MIS5-8)
    d["rel"] = d["date"] - d["start_date"]
    d = d[d["rel"].between(0, 15)]

    # pivot MIS 1..8 status per person
    d["mis_pos"] = np.where(d["rel"] <= 3, d["rel"] + 1, d["rel"] - 7)
    d = d.drop_duplicates(["pid", "mis_pos"])
    seq = d.pivot(index="pid", columns="mis_pos", values="st")
    seq = seq.reindex(columns=range(1, 9))
    seq["pre"] = seq[[1, 2, 3, 4]].apply(
        lambda r: "".join(x if isinstance(x, str) else "." for x in r), axis=1)
    seq["post"] = seq[[5, 6, 7, 8]].apply(
        lambda r: "".join(x if isinstance(x, str) else "." for x in r), axis=1)
    seq["full"] = seq["pre"] + "-" + seq["post"]

    # universe: teacher in at least one of the pre months
    ever_pre = seq["pre"].str.contains("T")
    T = seq[ever_pre].copy()
    print(f"\n=== persons teacher in >=1 pre-month (cohorts 2005-2006): "
          f"{len(T):,} ===")

    T["n_pre_obs"] = T["pre"].str.replace(".", "", regex=False).str.len()
    T["n_pre_T"] = T["pre"].str.count("T")
    print("\n(a) of their observed PRE months, how many say 'teacher':")
    tab = (T.groupby(["n_pre_obs", "n_pre_T"]).size()
           .rename("persons").reset_index())
    print(tab.to_string(index=False))

    print("\n(b) among those observed all 4 pre months, the exact pre pattern:")
    full4 = T[T["n_pre_obs"] == 4]
    print(full4["pre"].value_counts().head(15).to_string())

    print("\n(c) volatility: pre status changes >=1 time within the 4 pre "
          "months (a real teacher shouldn't flip):")
    def flips(s):
        s = s.replace(".", "")
        return sum(a != b for a, b in zip(s, s[1:]))
    T["pre_flips"] = T["pre"].apply(flips)
    print(T["pre_flips"].value_counts().sort_index().to_string())
    obs2 = T[T["n_pre_obs"] >= 2]
    print(f"  share with >=1 flip (of those with >=2 pre obs): "
          f"{(obs2['pre_flips'] > 0).mean()*100:.1f}%")

    print("\n(d) most common FULL 8-interview sequences (pre-post):")
    print(T["full"].value_counts().head(20).to_string())

    # how the leaver label would swing by which post month you pick
    print("\n(e) among all-8-observed teachers-in-pre, is post volatile too?")
    full8 = T[(T["n_pre_obs"] == 4)
              & (T["post"].str.replace(".", "", regex=False).str.len() == 4)]
    full8_post_flips = full8["post"].apply(flips)
    print(f"  n with all 8 obs: {len(full8):,}")
    print(f"  share whose POST 4 months flip status >=1 time: "
          f"{(full8_post_flips > 0).mean()*100:.1f}%")
    # leaver by strict (never teach in post) vs lax (not teacher in month 5)
    strict = ~full8["post"].str.contains("T")
    lax_m5 = full8[5] != "T"
    print(f"  leaver rate if 'never teaches in any post month': "
          f"{strict.mean()*100:.1f}%")
    print(f"  leaver rate if 'not teacher in FIRST post month (MIS5)': "
          f"{lax_m5.mean()*100:.1f}%")

    os.makedirs("outputs", exist_ok=True)
    T[["pre", "post", "full", "n_pre_obs", "n_pre_T", "pre_flips"]].to_csv(
        "outputs/within_person_sequences.csv")
    print("\nwrote outputs/within_person_sequences.csv")


if __name__ == "__main__":
    main()
