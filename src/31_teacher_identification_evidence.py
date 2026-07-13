"""
Evidence on HOW we identify a teacher in the basic monthly CPS, and what is
really going on in the months where a teacher-in-some-months is NOT coded a
teacher. Is the instability genuine job change, an education-adjacent coding
boundary (teacher <-> assistant/instructor/professor/admin), or a
reference-week gap (summer non-employment)?

Identification rule (basic monthly CPS):
  employed  := PEMLR in {1,2}           (labor-force-status recode)
  teacher   := employed AND PTIO1OCD in {2300,2310,2320,2330}
where PTIO1OCD is the census-coded occupation of the person's PRIMARY job,
built from the write-in answers "What kind of work were you doing?" /
"most important activities or duties". Within a rotation spell the CPS uses
DEPENDENT coding (MIS 2-4, 6-8 ask "same job as last month?"), so fresh
independent coding happens at MIS 1 and MIS 5.

Files 2005-2007 use the 2002 Census occupation classification. Teaching =
2300-2340; other education-adjacent codes are labelled below.
"""
import glob
import os
import re
import numpy as np
import pandas as pd

RAW = "data/raw/cps"
TEACHER = {2300, 2310, 2320, 2330}
# 2002 census occupation groups adjacent to K-12 classroom teaching
ADJ = {
    2200: "postsecondary teachers", 2340: "other teachers & instructors",
    2540: "teacher assistants", 230: "education administrators",
    2430: "librarians", 2400: "archivists/curators/museum",
    2000: "counselors", 2010: "social workers",
    2020: "clergy/religious", 2025: "directors relig. activities",
    2060: "other community/social", 2550: "other education/training/library",
}
COLS = [("HRHHID", 1, 15, str), ("HRMONTH", 16, 17, int),
        ("HRYEAR4", 18, 21, int), ("HRMIS", 63, 64, int),
        ("HRHHID2", 71, 75, str), ("PRTAGE", 122, 123, int),
        ("PESEX", 129, 130, int), ("PULINENO", 147, 148, int),
        ("PEMLR", 180, 181, int), ("PTIO1OCD", 860, 863, int)]
SPECS = [(s - 1, e) for _, s, e, _ in COLS]
NAMES = [n for n, *_ in COLS]


def read_month(path):
    import zipfile
    zf = zipfile.ZipFile(path)
    df = pd.read_fwf(zf.open(zf.namelist()[0]), colspecs=SPECS, names=NAMES,
                     dtype=str)
    for n, _, _, typ in COLS:
        if typ is not str:
            df[n] = pd.to_numeric(df[n], errors="coerce")
    df["HRHHID"] = df["HRHHID"].str.strip()
    df["HRHHID2"] = df["HRHHID2"].str.strip()
    return df[df["PRTAGE"] >= 18]


def main():
    parts = []
    for f in sorted(glob.glob(f"{RAW}/cpsb*.zip")):
        if not re.search(r"cpsb200[567]", os.path.basename(f)):
            continue
        parts.append(read_month(f))
    d = pd.concat(parts, ignore_index=True)
    d["date"] = d["HRYEAR4"] * 12 + d["HRMONTH"]
    d["pid"] = (d["HRHHID"] + "|" + d["HRHHID2"] + "|"
                + d["PULINENO"].astype("Int64").astype(str))
    d = d[d.groupby("pid")["PESEX"].transform("nunique") == 1]

    emp = d["PEMLR"].isin([1, 2])
    d["is_teacher"] = (emp & d["PTIO1OCD"].isin(TEACHER)).astype(int)
    d["status"] = np.where(d["is_teacher"] == 1, "T",
                  np.where(emp, "E",
                  np.where(d["PEMLR"].isin([3, 4]), "U", "N")))

    # spell alignment (MIS position 1..8 from first MIS-1 date)
    firsts = d[d["HRMIS"] == 1].groupby("pid")["date"].min().rename("start")
    d = d.merge(firsts, on="pid", how="inner")
    d["rel"] = d["date"] - d["start"]
    d = d[d["rel"].between(0, 15)]
    d["mis_pos"] = np.where(d["rel"] <= 3, d["rel"] + 1, d["rel"] - 7)
    d = d.drop_duplicates(["pid", "mis_pos"])

    pre = d[d["mis_pos"].between(1, 4)]
    ever_pre_T = pre.groupby("pid")["is_teacher"].max()
    tids = ever_pre_T[ever_pre_T == 1].index
    P = pre[pre["pid"].isin(tids)]
    print(f"persons teacher in >=1 pre month: {len(tids):,}")
    print(f"their pre person-months: {len(P):,}")

    print("\n=== (1) in the pre months where they are NOT coded teacher, "
          "what are they? ===")
    notT = P[P["is_teacher"] == 0]
    print(notT["status"].value_counts(normalize=True).mul(100).round(1)
          .to_string(), "  (% of non-teacher pre months)")

    print("\n=== (2) of the EMPLOYED-but-not-teacher months, which occupations? "
          "===")
    e = notT[notT["status"] == "E"].copy()
    e["grp"] = e["PTIO1OCD"].map(ADJ)
    adj_share = e["PTIO1OCD"].isin(ADJ).mean() * 100
    print(f"employed-non-teacher pre months: {len(e):,}")
    print(f"  education-adjacent occupation: {adj_share:.1f}%")
    print("  top adjacent codes:")
    print(e[e["PTIO1OCD"].isin(ADJ)]["grp"].value_counts().head(8).to_string())
    print("  top NON-adjacent codes (raw):")
    print(e[~e["PTIO1OCD"].isin(ADJ)]["PTIO1OCD"].value_counts().head(8)
          .to_string())

    print("\n=== (3) where do flips happen by MIS position? "
          "(dependent coding => MIS1 & MIS5 fresh) ===")
    # for each person, mark at each pre MIS whether teacher; count transitions
    piv = P.pivot(index="pid", columns="mis_pos", values="is_teacher")
    for a, b in [(1, 2), (2, 3), (3, 4)]:
        both = piv[[a, b]].dropna()
        chg = (both[a] != both[b]).mean() * 100
        print(f"  MIS {a}->{b}: {chg:.1f}% change teacher status  "
              f"(n={len(both):,})")

    print("\n=== (4) the boundary at the independent re-code MIS4 -> MIS5 ===")
    allp = d[d["pid"].isin(tids)].pivot(index="pid", columns="mis_pos",
                                        values="is_teacher")
    b45 = allp[[4, 5]].dropna()
    print(f"  MIS 4->5 (fresh independent coding across the 8-month gap): "
          f"{(b45[4] != b45[5]).mean()*100:.1f}% change  (n={len(b45):,})")
    within = [(1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 8)]
    wc = []
    for a, b in within:
        both = allp[[a, b]].dropna()
        wc.append((both[a] != both[b]).mean() * 100)
    print(f"  avg change at WITHIN-spell adjacent pairs (dependent coding): "
          f"{np.mean(wc):.1f}%")

    os.makedirs("outputs", exist_ok=True)
    e["PTIO1OCD"].value_counts().to_csv("outputs/nonteacher_occ_codes.csv")
    print("\nwrote outputs/nonteacher_occ_codes.csv")


if __name__ == "__main__":
    main()
