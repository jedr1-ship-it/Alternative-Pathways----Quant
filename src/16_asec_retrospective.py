"""
Replication of the retrospective March CPS (ASEC) measure of teacher
attrition used by Harris and Adams (2007) and Aldeman and Yi (2025), on
the 2022-2024 supplements. A person is a teacher if the occupation of the
longest job held LAST year (OCCUP) is a school-teaching code and she holds
a bachelor's degree; she is a leaver if the current-week occupation
(PEIOOCC) is no longer a teaching code, including not being employed.
Appends the pooled rate to outputs/ and prints the year detail.
"""
import numpy as np
import pandas as pd

TEACHER_OCC = [2300, 2310, 2320, 2330]
COLS = ["PEIOOCC", "OCCUP", "A_HGA", "MARSUPWT", "A_AGE"]

rows = []
for y in (22, 23, 24):
    d = pd.read_csv(f"data/raw/asec/pppub{y}.csv", usecols=COLS)
    t = d[(d["OCCUP"].isin(TEACHER_OCC)) & (d["A_HGA"] >= 43)
          & (d["A_AGE"] >= 18)].copy()
    t["left"] = (~t["PEIOOCC"].isin(TEACHER_OCC)).astype(int)
    rate = np.average(t["left"], weights=t["MARSUPWT"]) * 100
    # split: switched occupation vs not employed in the survey week
    sw = np.average(((t["PEIOOCC"] > 0)
                     & ~t["PEIOOCC"].isin(TEACHER_OCC)).astype(int),
                    weights=t["MARSUPWT"]) * 100
    ne = np.average((t["PEIOOCC"] <= 0).astype(int),
                    weights=t["MARSUPWT"]) * 100
    rows.append({"asec_year": 2000 + y, "teachers_n": len(t),
                 "leaver_rate": rate, "to_other_occ": sw,
                 "not_employed": ne})
    print(f"ASEC {2000+y}: n={len(t):,}  leaver {rate:.1f}%  "
          f"(other occ {sw:.1f}, not employed {ne:.1f})")

res = pd.DataFrame(rows)
pooled_n = res["teachers_n"].sum()
pooled = np.average(res["leaver_rate"], weights=res["teachers_n"])
print(f"pooled 2022-2024: n={pooled_n:,}  leaver {pooled:.1f}%")
res.round(2).to_csv("outputs/asec_retrospective.csv", index=False)
