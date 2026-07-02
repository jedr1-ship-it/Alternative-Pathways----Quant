"""Shared covariate construction for the CPS teacher-attrition panel.

Analytic sample: school teachers holding at least a bachelor's degree
(PEEDUCA >= 43), the standard restriction in the teacher-attrition
literature. Education enters as master's+ vs the bachelor's-only reference.
"""

COVS = ["age", "age2", "female", "married", "black", "hispanic", "noncitizen",
        "ma_plus", "parttime", "hours_missing", "faminc75k",
        "preschool_kg", "secondary", "special_ed"]

# human-readable names for figures/tables
LABELS = {
    "age": "Age (years)",
    "age2": "Age$^2$/100",
    "female": "Female",
    "married": "Married",
    "black": "Black",
    "hispanic": "Hispanic",
    "noncitizen": "Non-citizen",
    "ma_plus": "Master's degree or higher",
    "parttime": "Part-time (<35 h/week)",
    "hours_missing": "Hours not reported",
    "faminc75k": "Family income $75k+",
    "preschool_kg": "Preschool / kindergarten",
    "secondary": "Secondary school",
    "special_ed": "Special education",
}


def add_covariates(df):
    """Build model covariates (measured at t) on the linked teacher panel."""
    df = df.copy()
    df["age"] = df["PRTAGE_0"]
    df["age2"] = df["age"] ** 2 / 100.0
    df["female"] = (df["PESEX_0"] == 2).astype(int)
    df["married"] = df["PEMARITL_0"].isin([1, 2]).astype(int)
    df["black"] = (df["PTDTRACE_0"] == 2).astype(int)
    df["hispanic"] = (df["PEHSPNON_0"] == 1).astype(int)
    df["noncitizen"] = (df["PRCITSHP_0"] == 5).astype(int)
    # PEEDUCA: 43 bachelor's; 44 master's; 45 professional; 46 doctorate
    df["ma_plus"] = (df["PEEDUCA_0"] >= 44).astype(int)
    df["hours"] = df["PEHRUSL1_0"].where(df["PEHRUSL1_0"] > 0)
    df["parttime"] = (df["hours"] < 35).astype(int).where(df["hours"].notna(), 0)
    df["hours_missing"] = df["hours"].isna().astype(int)
    df["faminc75k"] = (df["HEFAMINC_0"] >= 13).astype(int)
    df["preschool_kg"] = (df["PTIO1OCD_0"] == 2300).astype(int)
    df["secondary"] = (df["PTIO1OCD_0"] == 2320).astype(int)
    df["special_ed"] = (df["PTIO1OCD_0"] == 2330).astype(int)
    return df
