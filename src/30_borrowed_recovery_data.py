"""
Data build for the short brief "A Borrowed Recovery? The 2025 teacher
workforce data for the United States" — a CPS-based replication of
EPI (UK), 'A borrowed recovery: the 2025 school workforce data' (2026).

Inputs
  data/raw/cps/<mon><yy>pub.dat.gz   2024-2025 basic monthly files (Census).
                                     October 2025 does not exist: the CPS was
                                     not collected that month (federal
                                     government shutdown).
  data/processed/cps_teacher_panel.csv   linked panel 2005->2025 (02_build)
  outputs/teacher_stock_by_year.csv      monthly-average stocks 2005-2023 (06)
  outputs/evolution_by_year_gender.csv   persistent-leaver + returns (05)
  data/raw/external/*.csv                FRED: CPIAUCSL, LNS14027662,
                                         JTSQUR, JTS1000QUR, LEU0252918500Q,
                                         LEU0252881600Q, CES0500000003
  data/raw/external/tabn203.10.xlsx      NCES Digest 2025, public K-12
                                         enrollment by fall of year

Outputs (outputs/)
  br_stock_by_year.csv        teachers by level, 2005-2025 (millions)
  br_enrollment.csv           public school enrollment, fall 2000-2024
  br_attrition_year.csv       12-month leaver rate by base year, 2005-2024
  br_attrition_age.csv        leaver rate by age band x base year
  br_pay_by_year.csv          teacher real median weekly earnings vs BA+
  br_flows.csv                entry/exit rates 2005-2024
  br_entrants_2024.csv        composition of 2024->2025 entrants
  br_destinations_year.csv    destination shares of leavers by year
  br_market.csv               attrition vs outside labour market conditions
"""
import glob
import importlib.util
import os
import re
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import openpyxl
import pandas as pd

spec = importlib.util.spec_from_file_location(
    "cpsbuild", os.path.join(os.path.dirname(__file__), "02_build_cps_panel.py"))
cpsbuild = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cpsbuild)

RAWDIR, INTDIR = "data/raw/cps", "data/interim"
EXT = "data/raw/external"
OUT = "outputs"
MON = dict(jan=1, feb=2, mar=3, apr=4, may=5, jun=6,
           jul=7, aug=8, sep=9, oct=10, nov=11, dec=12)
K12_OCC = [2310, 2320, 2330]
LEVELS = {2300: "Preschool / kindergarten", 2310: "Elementary / middle",
          2320: "Secondary", 2330: "Special education"}


# ---------------------------------------------------------------- stage 1
def parse_one(path):
    b = os.path.basename(path)
    m = re.match(r"([a-z]{3})(\d{2})pub", b)
    yyyymm = f"20{m.group(2)}{MON[m.group(1)]:02d}"
    out = f"{INTDIR}/cps_{yyyymm}.parquet"
    if os.path.exists(out):
        return yyyymm, "cached"
    d = cpsbuild.read_month(path)
    yr, mo = int(yyyymm[:4]), int(yyyymm[4:])
    assert d["HRYEAR4"].mode().iat[0] == yr, f"year mismatch in {b}"
    assert d["HRMONTH"].mode().iat[0] == mo, f"month mismatch in {b}"
    emp = d[d["PEMLR"].isin([1, 2])]
    share = emp["PTIO1OCD"].isin(cpsbuild.TEACHER_OCC).mean() * 100
    assert 1.0 < share < 6.0, f"teacher share {share:.1f}% off in {b}"
    d.to_parquet(out, index=False)
    return yyyymm, f"{len(d):,} adults, teachers {share:.1f}% of employed"


def stage1():
    files = sorted(glob.glob(f"{RAWDIR}/[a-z][a-z][a-z]2[45]pub.dat.gz"))
    print(f"stage 1: {len(files)} monthly files")
    with ProcessPoolExecutor(max_workers=6) as ex:
        for yyyymm, msg in ex.map(parse_one, files):
            print(f"  {yyyymm}: {msg}", flush=True)


# ------------------------------------------------------- stock + enrollment
def build_stock():
    rows = []
    for f in sorted(glob.glob(f"{INTDIR}/cps_202[45]??.parquet")):
        d = pd.read_parquet(f, columns=["PEMLR", "PTIO1OCD", "PEEDUCA",
                                        "HRYEAR4", "HRMONTH", "PWSSWGT"])
        e = d[d["PEMLR"].isin([1, 2])]
        t = e[e["PTIO1OCD"].isin(K12_OCC)]
        tb = t[t["PEEDUCA"] >= 43]
        g = tb.groupby("PTIO1OCD")["PWSSWGT"].sum()
        rows.append({"year": int(d["HRYEAR4"].iat[0]),
                     "month": int(d["HRMONTH"].iat[0]),
                     **{LEVELS[k]: g.get(k, 0.0) for k in LEVELS},
                     "total": tb["PWSSWGT"].sum()})
    new = (pd.DataFrame(rows).groupby("year").mean(numeric_only=True)
           .drop(columns="month") / 1e6)
    old = pd.read_csv(f"{OUT}/teacher_stock_by_year.csv", index_col="year")
    stock = pd.concat([old[old.index < 2024], new.round(3)])
    stock.to_csv(f"{OUT}/br_stock_by_year.csv")
    print("stock 2024-2025:\n", new.round(3))
    return stock


def build_enrollment():
    ws = openpyxl.load_workbook(f"{EXT}/tabn203.10.xlsx").active
    rows = []
    for r in ws.iter_rows(values_only=True):
        y = str(r[0]).strip().lstrip("\n") if r[0] is not None else ""
        if re.fullmatch(r"(19|20)\d{2}", y):
            rows.append({"fall": int(y),
                         "enrollment_k":
                         float(str(r[1]).replace(",", ""))})
    enr = pd.DataFrame(rows).query("fall >= 2000")
    enr.to_csv(f"{OUT}/br_enrollment.csv", index=False)
    print(f"enrollment: fall {enr.fall.min()}-{enr.fall.max()}, "
          f"last = {enr.enrollment_k.iloc[-1]:,.0f}k")
    return enr


# ------------------------------------------------------------- panel-based
def load_panel():
    p = pd.read_csv("data/processed/cps_teacher_panel.csv",
                    dtype={"HRHHID": str, "HRHHID2": str})
    # analytic universe of the brief: full-time K-12 teachers, BA+
    p = p[p["PTIO1OCD_0"].isin(K12_OCC) & ~p["PEHRUSL1_0"].between(1, 34)]
    return p.copy()


def wavg(d, col, w="PWSSWGT_0"):
    return np.average(d[col], weights=d[w]) * 100


def wmedian(x, w):
    o = np.argsort(x)
    c = np.cumsum(w[o])
    return x[o][np.searchsorted(c, 0.5 * c[-1])]


def build_attrition(p):
    ev = pd.read_csv(f"{OUT}/evolution_by_year_gender.csv")
    yr = (p.groupby("base_year")
            .apply(lambda d: pd.Series(
                {"attr12": wavg(d, "leaver"),
                 "n": len(d)}), include_groups=False)
            .reset_index())
    yr = yr.merge(ev[["base_year", "attrp_all", "ret_all"]],
                  on="base_year", how="left")
    yr.to_csv(f"{OUT}/br_attrition_year.csv", index=False)
    print("attr12 tail:\n", yr.tail(4).round(2).to_string(index=False))

    bands = pd.cut(p["PRTAGE_0"], [0, 29, 39, 49, 98],
                   labels=["under 30", "30-39", "40-49", "50+"])
    age = (p.assign(band=bands).groupby(["base_year", "band"], observed=True)
             .apply(lambda d: pd.Series(
                 {"attr12": wavg(d, "leaver"), "n": len(d)}),
                 include_groups=False)
             .reset_index())
    age.to_csv(f"{OUT}/br_attrition_age.csv", index=False)
    return yr


def build_pay(p):
    t0 = p[p["PTERNWA_0"] > 0][["base_year", "PTERNWA_0", "PWSSWGT_0"]]
    t0.columns = ["year", "wage", "w"]
    s1 = p[(p["teacher_1"] == 1) & (p["tchBA_1"] == 1)
           & ~p["PEHRUSL1_1"].between(1, 34) & (p["PTERNWA_1"] > 0)]
    t1 = s1[["base_year", "PTERNWA_1", "PWSSWGT_1"]].copy()
    t1["base_year"] += 1
    t1.columns = ["year", "wage", "w"]
    long = pd.concat([t0, t1], ignore_index=True)
    long["wage"] /= 100.0        # PTERNWA carries two implied decimals
    med = (long.groupby("year")
               .apply(lambda d: pd.Series(
                   {"teacher_nominal": wmedian(d["wage"].to_numpy(),
                                               d["w"].to_numpy()),
                    "n": len(d)}), include_groups=False)
               .reset_index())

    cpi = fred_annual("CPIAUCSL")
    ba = fred_annual("LEU0252918500Q").rename(columns={"v": "ba_nominal"})
    # LEU0252881600 is already real (1982-84 dollars): index it directly
    allw = fred_annual("LEU0252881600Q").rename(columns={"v": "all_real82"})
    med = (med.merge(cpi.rename(columns={"v": "cpi"}), on="year")
              .merge(ba, on="year").merge(allw, on="year"))
    base_cpi = med.loc[med.year == 2025, "cpi"].iloc[0]
    for c in ["teacher", "ba"]:
        med[f"{c}_real"] = med[f"{c}_nominal"] * base_cpi / med["cpi"]
        b = med.loc[med.year == 2010, f"{c}_real"].iloc[0]
        med[f"{c}_idx"] = med[f"{c}_real"] / b * 100
    med["all_idx"] = (med["all_real82"]
                      / med.loc[med.year == 2010, "all_real82"].iloc[0] * 100)
    med.round(2).to_csv(f"{OUT}/br_pay_by_year.csv", index=False)
    print("pay tail:\n", med[["year", "teacher_real", "teacher_idx",
                              "ba_idx", "n"]].tail(3).round(1)
          .to_string(index=False))
    return med


def build_destinations(p):
    d = (p.groupby("base_year")["dest"]
           .value_counts(normalize=True).unstack() * 100)
    # weighted version
    g = p.groupby(["base_year", "dest"])["PWSSWGT_0"].sum().unstack()
    d = g.div(g.sum(axis=1), axis=0) * 100
    d.round(2).to_csv(f"{OUT}/br_destinations_year.csv")
    return d


# ------------------------------------------------- 2024->2025 link (flows)
def build_flows_2024():
    key = ["HRHHID", "HRHHID2", "PULINENO", "HRMONTH"]
    t0 = cpsbuild.load_year(2024, 1, 4)
    t1 = cpsbuild.load_year(2025, 5, 8)
    m = t0.merge(t1, on=key, suffixes=("_0", "_1"))
    m = m[m["HRMIS_1"] - m["HRMIS_0"] == 4]
    m = m[(m["PESEX_0"] == m["PESEX_1"])
          & (m["PTDTRACE_0"] == m["PTDTRACE_1"])
          & (m["PRTAGE_1"] - m["PRTAGE_0"]).between(0, 2)].copy()
    for t in ("_0", "_1"):
        m[f"employed{t}"] = m[f"PEMLR{t}"].isin([1, 2]).astype(int)
        m[f"teacher{t}"] = ((m[f"employed{t}"] == 1)
                            & m[f"PTIO1OCD{t}"].isin(
                                cpsbuild.TEACHER_OCC)).astype(int)
    m["tchBA_0"] = ((m["teacher_0"] == 1) & (m["PEEDUCA_0"] >= 43)).astype(int)
    m["tchBA_1"] = ((m["teacher_1"] == 1) & (m["PEEDUCA_1"] >= 43)).astype(int)

    w0, w1 = m["PWSSWGT_0"].astype(float), m["PWSSWGT_1"].astype(float)
    row = {"base_year": 2024,
           "teachers_t_w": w0[m["tchBA_0"] == 1].sum(),
           "teachers_t1_w": w1[m["tchBA_1"] == 1].sum(),
           "leavers_w": w0[(m["tchBA_0"] == 1) & (m["teacher_1"] == 0)].sum(),
           "entrants_w": w1[(m["tchBA_1"] == 1) & (m["teacher_0"] == 0)].sum(),
           "links_w": w0.sum(), "n_teachers": int(m["tchBA_0"].sum())}
    row["entry_rate"] = row["entrants_w"] / row["teachers_t1_w"] * 100
    row["exit_rate"] = row["leavers_w"] / row["teachers_t_w"] * 100
    fl = pd.read_csv(f"{OUT}/flows_by_year.csv")
    fl = pd.concat([fl[fl.base_year < 2024],
                    pd.DataFrame([row])], ignore_index=True)
    fl.round(3).to_csv(f"{OUT}/br_flows.csv", index=False)
    print(f"2024->2025: entry {row['entry_rate']:.1f}%  "
          f"exit {row['exit_rate']:.1f}%  (n teachers {row['n_teachers']:,})")

    # composition of entrants (weighted): where were they 12 months earlier?
    en = m[(m["tchBA_1"] == 1) & (m["teacher_0"] == 0)].copy()
    en["origin"] = np.select(
        [en["employed_0"] == 1, en["PEMLR_0"].isin([3, 4]),
         en["PEMLR_0"].isin([5, 6, 7])],
        ["employed outside teaching", "unemployed", "out of the labour force"],
        default="other")
    comp = (en.groupby("origin")["PWSSWGT_1"].sum()
              / en["PWSSWGT_1"].sum() * 100).round(2)
    extra = pd.Series(
        {"share under 30": (en[en.PRTAGE_1 <= 29]["PWSSWGT_1"].sum()
                            / en["PWSSWGT_1"].sum() * 100).round(2),
         "median age": float(wmedian(en["PRTAGE_1"].to_numpy(dtype=float),
                                     en["PWSSWGT_1"].to_numpy()))})
    pd.concat([comp, extra]).to_csv(f"{OUT}/br_entrants_2024.csv",
                                    header=["value"])
    print("entrant origin 2024->2025 (%):\n", comp.to_string())


# ------------------------------------------------------------ market series
def fred_annual(sid):
    d = pd.read_csv(f"{EXT}/{sid}.csv")
    d.columns = ["date", "v"]
    d["year"] = pd.to_datetime(d["date"]).dt.year
    return d.groupby("year", as_index=False)["v"].mean()


def build_market(attr):
    u = fred_annual("LNS14027662").rename(columns={"v": "unemp_ba"})
    q = fred_annual("JTS1000QUR").rename(columns={"v": "quits_private"})
    ahe = fred_annual("CES0500000003").rename(columns={"v": "ahe"})
    cpi = fred_annual("CPIAUCSL").rename(columns={"v": "cpi"})
    mk = u.merge(q, on="year").merge(ahe, on="year").merge(cpi, on="year")
    mk["real_ahe"] = mk["ahe"] / mk["cpi"]
    mk["real_wage_growth"] = mk["real_ahe"].pct_change() * 100
    mk = mk.merge(attr.rename(columns={"base_year": "year"})[
        ["year", "attr12"]], on="year", how="left")
    mk = mk[(mk.year >= 2005) & (mk.year <= 2025)]
    mk.round(3).to_csv(f"{OUT}/br_market.csv", index=False)
    s = mk.dropna(subset=["attr12"])
    for c in ["unemp_ba", "quits_private", "real_wage_growth"]:
        print(f"corr(attr12, {c}) = {s['attr12'].corr(s[c]):+.2f}")
    return mk


if __name__ == "__main__":
    stage1()
    build_stock()
    build_enrollment()
    p = load_panel()
    print(f"\npanel universe: {len(p):,} full-time K-12 teachers, "
          f"base years {p.base_year.min()}-{p.base_year.max()}")
    attr = build_attrition(p)
    build_pay(p)
    build_destinations(p)
    build_flows_2024()
    build_market(attr)
    print("\ndone.")
