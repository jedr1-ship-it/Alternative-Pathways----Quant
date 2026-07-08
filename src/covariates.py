"""Shared covariate construction for the CPS teacher-attrition panel.

Analytic sample: school teachers holding at least a bachelor's degree
(PEEDUCA >= 43), the standard restriction in the teacher-attrition
literature. Education enters as master's+ vs the bachelor's-only reference.
"""

COVS = ["age", "age2", "female", "married", "n_children", "child_u6",
        "fem_child_u6", "new_baby", "fem_newbaby",
        "black", "hispanic", "noncitizen",
        "ma_plus", "prof_phd", "hours_missing", "multjob",
        "public", "faminc75k", "midwest", "south", "west",
        "secondary", "special_ed"]

# human-readable names for figures/tables
LABELS = {
    "age": "Age (years)",
    "age2": "Age$^2$/100",
    "female": "Female",
    "married": "Married",
    "n_children": "Number of own children",
    "child_u6": "Child under 6 at home",
    "fem_child_u6": "Female $\\times$ child under 6",
    "new_baby": "New baby during the year",
    "fem_newbaby": "Female $\\times$ new baby",
    "black": "Black",
    "hispanic": "Hispanic",
    "noncitizen": "Non-citizen",
    "ma_plus": "Master's degree or higher",
    "prof_phd": "Professional degree or doctorate",
    "parttime": "Part-time (<35 h/week)",
    "hours_missing": "Hours not reported",
    "multjob": "Holds more than one job",
    "public": "Public-sector employer",
    "faminc75k": "Family income $75k+",
    "midwest": "Midwest",
    "south": "South",
    "west": "West",
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
    # analytic universe: elementary-through-secondary classroom teachers
    # (the CPS code merges preschool with kindergarten, so 2300 is out),
    # working full time at baseline
    df = df[df["PTIO1OCD_0"].isin([2310, 2320, 2330])
            & ~df["PEHRUSL1_0"].between(1, 34)]
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
    # a child aged 0-2 present at t+12 but not at t: a birth during the year
    U3 = [1, 5, 6, 7, 11, 12, 13, 15]
    df["new_baby"] = (df["PRCHLD_1"].isin(U3)
                      & ~df["PRCHLD_0"].isin(U3)).astype(int)
    df["fem_newbaby"] = df["female"] * df["new_baby"]
    df["black"] = (df["PTDTRACE_0"] == 2).astype(int)
    df["hispanic"] = (df["PEHSPNON_0"] == 1).astype(int)
    df["noncitizen"] = (df["PRCITSHP_0"] == 5).astype(int)
    # PEEDUCA: 43 bachelor's; 44 master's; 45 professional; 46 doctorate
    df["ma_plus"] = (df["PEEDUCA_0"] >= 44).astype(int)
    df["hours"] = df["PEHRUSL1_0"].where(df["PEHRUSL1_0"] > 0)
    df["parttime"] = (df["hours"] < 35).astype(int).where(df["hours"].notna(), 0)
    df["hours_missing"] = df["hours"].isna().astype(int)
    df["faminc75k"] = (df["HEFAMINC_0"] >= 13).astype(int)
    # PEEDUCA 45 = professional degree, 46 = doctorate
    df["prof_phd"] = (df["PEEDUCA_0"] >= 45).astype(int)
    # class of worker: 1-3 = federal/state/local government
    df["public"] = df["PEIO1COW_0"].isin([1, 2, 3]).astype(int)
    df["multjob"] = (df["PEMJOT_0"] == 1).astype(int)
    # census regions from state FIPS (ref.: Northeast)
    NE = {9, 23, 25, 33, 44, 50, 34, 36, 42}
    MW = {17, 18, 26, 39, 55, 19, 20, 27, 29, 31, 38, 46}
    SO = {10, 11, 12, 13, 24, 37, 45, 51, 54, 1, 21, 28, 47, 5, 22, 40, 48}
    df["midwest"] = df["GESTFIPS_0"].isin(MW).astype(int)
    df["south"] = df["GESTFIPS_0"].isin(SO).astype(int)
    df["west"] = (~df["GESTFIPS_0"].isin(NE | MW | SO)).astype(int)
    # weekly earnings, only asked in outgoing rotations (MIS 4 and 8);
    # PTERNWA has two implied decimals
    df["wkearn"] = df["PTERNWA_0"].where(df["PTERNWA_0"] > 0) / 100.0
    df["preschool_kg"] = (df["PTIO1OCD_0"] == 2300).astype(int)
    df["secondary"] = (df["PTIO1OCD_0"] == 2320).astype(int)
    df["special_ed"] = (df["PTIO1OCD_0"] == 2330).astype(int)
    return df
