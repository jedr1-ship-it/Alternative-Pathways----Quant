"""Step 2 - Build the teacher analysis files from the pooled ASEC master.

Reads  data/processed/asec_master.parquet   (5,009,129 person-year records)
Writes data/processed/teachers.parquet      (every teacher-year observation)
       data/processed/teachers_main.parquet (the main analysis sample:
                                             college graduates aged 18+ with
                                             a valid weight and outcome)

A "teacher" is a person whose longest job in the previous calendar year was
K-12 teaching (occupation codes 155-159 in surveys through 2002, 2300-2340
in surveys 2003-2019, 2300-2330 or 2360 from 2020). The outcome variables
(leaver, switch, unemp, leftlf) describe the person's status at the March
interview of the following survey.
"""
import pandas as pd

SRC = "data/processed/asec_master.parquet"

M = pd.read_parquet(SRC)
for c in M.columns:
    if c != "PERIDNUM":
        M[c] = pd.to_numeric(M[c], errors="coerce")
M["cal_year"] = M["asec_year"] - 1

T = M[M["teacher"] == 1].copy()
T.to_parquet("data/processed/teachers.parquet", index=False)

main = T[(T["ba_plus"] == 1) & (T["A_AGE"] >= 18)
         & T["WGT"].notna() & T["leaver"].notna()].copy()
main.to_parquet("data/processed/teachers_main.parquet", index=False)

print(f"master records         : {len(M):>9,}")
print(f"teacher-year records   : {len(T):>9,}  -> data/processed/teachers.parquet")
print(f"main analysis sample   : {len(main):>9,}  -> data/processed/teachers_main.parquet")
print(f"exits observed (main)  : {int(main['leaver'].sum()):>9,}")
print(f"teaching years covered : {int(main['cal_year'].min())}-{int(main['cal_year'].max())}")
