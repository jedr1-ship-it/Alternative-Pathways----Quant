"""Extended ASEC person file, 2019-2025, from the Census public-use CSVs.
Adds state, household income, health, disability, enrollment and reason
for not working to the usual person variables. Writes
data/processed/asec_ext.parquet. Inputs: data/raw/aseccsv/asecpubYYcsv.zip
(download: https://www2.census.gov/programs-surveys/cps/datasets/20YY/march/).
Run from the repo root."""
import io
import zipfile
import pandas as pd

PVARS = ["PERIDNUM", "PH_SEQ", "A_LINENO", "MARSUPWT", "A_AGE", "A_SEX",
         "PRDTRACE", "A_HGA", "A_MARITL", "A_LFSR", "OCCUP", "PEIOOCC",
         "LJCW", "PENPLAN", "WKSWORK", "HRSWK", "WSAL_VAL", "PEPAR1",
         "PEPAR2", "RSNNOTW", "HEA", "DIS_HP", "A_ENRLW", "A_CLSWKR",
         "A_FTPT", "PEMLR", "PRNLFSCH"]
HVARS = ["H_SEQ", "GESTFIPS", "HTOTVAL"]

out = []
for y in range(19, 26):
    z = zipfile.ZipFile(f"data/raw/aseccsv/asecpub{y}csv.zip")
    def member(suffix):
        return next(n for n in z.namelist() if n.endswith(suffix))
    with z.open(member(f"pppub{y}.csv")) as f:
        p = pd.read_csv(f, usecols=PVARS, dtype={"PERIDNUM": str}, low_memory=False)
    with z.open(member(f"hhpub{y}.csv")) as f:
        h = pd.read_csv(f, usecols=HVARS, low_memory=False)
    d = p.merge(h, left_on="PH_SEQ", right_on="H_SEQ", how="left")
    d["asec_year"] = 2000 + y
    out.append(d.drop(columns=["H_SEQ"]))
    print(f"20{y}: {len(d):,} persons", flush=True)

df = pd.concat(out, ignore_index=True)
df.to_parquet("data/processed/asec_ext.parquet", index=False)
print(f"saved asec_ext.parquet: {len(df):,} rows, {len(df.columns)} cols")
