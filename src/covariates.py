"""Shared covariate construction for the CPS teacher-attrition panel.

Analytic sample: school teachers holding at least a bachelor's degree
(PEEDUCA >= 43), the standard restriction in the teacher-attrition
literature. Education enters as master's+ vs the bachelor's-only reference.
"""

COVS = ["age", "age2", "female", "married", "n_children", "child_u6",
        "fem_child_u6", "black", "hispanic", "noncitizen",
        "ma_plus", "parttime", "hours_missing", "faminc75k",
        "preschool_kg", "secondary", "special_ed"]

# human-readable names for figures/tables
LABELS = {
    "age": "Age (years)",
    "age2": "Age$^2$/100",
    "female": "Female",
    "married": "Married",
    "n_children": "Number of own children",
    "child_u6": "Child under 6 at home",
    "fem_child_u6": "Female $\\times$ child under 6",
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


def load_panel():
    """Load the teacher panel with covariates and both leaver definitions.

    - leaver12   (definition A): not an employed school teacher at t+12.
    - leaver_p   (definition B, main): additionally not observed teaching in
      any of the up-to-3 monthly re-interviews after t+12. Only defined on
      the subsample with a potential follow-up interview (baseline MIS 1-3),
      flagged by `sampleB`. Leavers whose follow-up interview is missing
      (~4%) are kept as persistent.
    """
    import pandas as pd
    df = pd.read_csv("data/processed/cps_teacher_panel.csv",
                     dtype={"HRHHID": str, "HRHHID2": str})
    df = add_covariates(df)
    df["leaver12"] = df["leaver"]
    ret = pd.read_csv("data/processed/cps_returns.csv",
                      dtype={"HRHHID": str, "HRHHID2": str})
    df = df.merge(ret, on=["HRHHID", "HRHHID2", "PULINENO",
                           "HRMONTH", "base_year"], how="left")
    df["sampleB"] = df["HRMIS_0"] <= 3
    df["leaver_p"] = ((df["leaver12"] == 1)
                      & (df["returned"].fillna(0) == 0)).astype(int)
    return df


def add_covariates(df):
    """Build model covariates (measured at t) on the linked teacher panel."""
    df = df.copy()
    df["age"] = df["PRTAGE_0"]
    df["age2"] = df["age"] ** 2 / 100.0
    df["female"] = (df["PESEX_0"] == 2).astype(int)
    df["married"] = df["PEMARITL_0"].isin([1, 2]).astype(int)
    # own children <18 in the household (PRNMCHLD; -1 = not a parent -> 0)
    df["n_children"] = df["PRNMCHLD_0"].clip(lower=0)
    # PRCHLD codes containing the 0-2 or 3-5 age groups
    df["child_u6"] = df["PRCHLD_0"].isin(
        [1, 2, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15]).astype(int)
    df["fem_child_u6"] = df["female"] * df["child_u6"]
    df["fem_fertile"] = ((df["female"] == 1)
                         & df["PRTAGE_0"].between(25, 44)).astype(int)
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
