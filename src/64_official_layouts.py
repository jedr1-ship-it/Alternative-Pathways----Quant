"""
Parse the OFFICIAL Census ASEC technical documentation (cpsmarYY.pdf,
data/raw/docs/) into per-survey-year byte layouts for every variable the
master build needs. This replaces the empirical column calibration for
surveys 1998-2010: positions now come from the published record layout,
not from statistical guessing.

Each dictionary lists person-record variables as lines like
    D OCCUP  4  908
(name, size, 1-based position). The PDFs render in two columns, so the
pattern is matched anywhere in a line. Names use hyphens in the PDFs
(A-HGA) and are normalised to underscores (A_HGA). If a name appears
with more than one position, all occurrences are kept and flagged so the
conflict is resolved explicitly, never silently.

Output: outputs/layouts_official.csv  (asec_year, var, size, pos)
"""
import os
import re
import subprocess
import pandas as pd

DOCS = "data/raw/docs"
# person-record variables the master needs, by their PDF spelling
WANT = {
    "OCCUP", "PEIOOCC", "A-AGE", "A-SEX", "A-HGA", "A-LFSR", "A-MARITL",
    "A-CLSWKR", "A-USLHRS", "LJCW", "HRSWK", "WKSWORK", "PENPLAN",
    "MARSUPWT", "PERIDNUM", "PRDTRACE", "A-RACE", "A-PARENT", "A-SPOUSE",
    "A-FAMREL", "WSAL-VAL", "PEARNVAL", "A-MJOCC", "A-DTOCC", "PEMLR",
    "A-WKSTAT", "A-UNTYPE", "PUBLICEMP",
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
