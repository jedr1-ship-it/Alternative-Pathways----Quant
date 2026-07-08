"""
Is linkage failure selective for teachers?

For every person eligible to be linked (baseline MIS 1-4), computes the
probability of being found and validated 12 months later, separately for
school teachers (with a bachelor's degree) and comparison groups. If teachers
are re-found at a rate similar to comparable workers, the 33% linkage loss is
not differentially selective for the study population.
"""
import glob
import numpy as np
import pandas as pd

INTDIR = "data/interim"
TEACHER_OCC = {2310, 2320, 2330}
KEY = ["HRHHID", "HRHHID2", "PULINENO", "HRMONTH"]


def load_year(year, lo, hi, cols):
    parts = []
    for f in sorted(glob.glob(f"{INTDIR}/cps_{year}??.parquet")):
        d = pd.read_parquet(f, columns=cols)
        parts.append(d[d["HRMIS"].between(lo, hi)])
    return pd.concat(parts, ignore_index=True) if parts else None


cols0 = KEY + ["HRMIS", "HRYEAR4", "PESEX", "PTDTRACE", "PRTAGE",
               "PEMLR", "PTIO1OCD", "PEEDUCA", "PWSSWGT"]
cols1 = KEY + ["HRMIS", "HRYEAR4", "PESEX", "PTDTRACE", "PRTAGE"]

acc = []
for y0 in range(2005, 2025):
    t0 = load_year(y0, 1, 4, cols0)
    t1 = load_year(y0 + 1, 5, 8, cols1)
    if t0 is None or t1 is None:
        continue
    m = t0.merge(t1, on=KEY, how="left", suffixes=("", "_1"))
    found = m["HRMIS_1"].notna() & (m["HRMIS_1"] - m["HRMIS"] == 4)
    valid = (found
             & (m["PESEX"] == m["PESEX_1"])
             & (m["PTDTRACE"] == m["PTDTRACE_1"])
             & (m["PRTAGE_1"] - m["PRTAGE"]).between(0, 2))
    m["linked"] = valid.astype(int)
    m = m.drop_duplicates(subset=KEY)   # guard against rare key collisions

    emp = m["PEMLR"].isin([1, 2])
    ba = m["PEEDUCA"] >= 43
    tch = emp & m["PTIO1OCD"].isin(TEACHER_OCC) & ba
    groups = {
        "school teachers (BA+)": tch,
        "other college-educated employed": emp & ba & ~tch,
        "all employed": emp,
        "not employed": ~emp,
    }
    for g, mask in groups.items():
        d = m[mask]
        acc.append({"year": y0, "group": g, "n": len(d),
                    "linked_w": np.average(d["linked"], weights=d["PWSSWGT"]),
                    "linked_u": d["linked"].mean()})
    print(f"{y0}: done", flush=True)

res = pd.DataFrame(acc)
pooled = (res.groupby("group")
             .apply(lambda g: np.average(g["linked_w"], weights=g["n"]),
                    include_groups=False) * 100)
print("\nPooled 2005-2024 link-and-validate rate (weighted, %):")
print(pooled.round(1).to_string())
res.round(4).to_csv("outputs/linkage_rates_by_group.csv", index=False)

piv = res.pivot(index="year", columns="group", values="linked_w") * 100
print("\nBy year (weighted %):")
print(piv.round(1).to_string())
print("\nsaved outputs/linkage_rates_by_group.csv")
