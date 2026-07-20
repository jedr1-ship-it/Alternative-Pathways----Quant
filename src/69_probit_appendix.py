"""
AER-style appendix tables backing the who-leaves probit (Figure G6).

Table R (robustness of specification), columns:
  (1) Probit AME    baseline: BA+ teachers, 2015-2024, year FE
  (2) LPM           weighted (MARSUPWT), HC1
  (3) Logit AME
  (4) LPM + state and year FE
  (5) Probit AME    full window 1997-2024
  (6) LPM           occupation-pair leaver definition

Table S (subsamples, LPM with year FE -- probit can fail to converge
in thin cells): women / men / public / private / under 45 / 45+.

Outputs: outputs/t_probit_robustness.csv, t_probit_subsamples.csv and
booktabs LaTeX in report/tables/.
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.api as sm

XV = ["A_AGE", "age2", "female", "black", "married", "sepdiv",
      "ma_plus", "public", "pension", "parttime", "fullyear",
      "n_children", "child_u6", "new_baby"]
LABELS = {
    "A_AGE": "Age (years)", "age2": "Age$^2$/100", "female": "Female",
    "black": "Black", "married": "Married",
    "sepdiv": "Separated/divorced/widowed",
    "ma_plus": "Master's degree or higher",
    "public": "Public school", "pension": "Pension plan at work",
    "parttime": "Part-time (<35 h/wk)",
    "fullyear": "Worked full year (50+ wks)",
    "n_children": "Number of children", "child_u6": "Child under 6",
    "new_baby": "New baby this year"}

M = pd.read_parquet("data/processed/asec_master.parquet")
T = M[(M["teacher"] == 1) & (M["ba_plus"] == 1)
      & M["A_AGE"].between(18, 80)].copy()
T["age2"] = T["A_AGE"] ** 2 / 100
T["sepdiv"] = T["A_MARITL"].isin([4, 5, 6]).astype(float)
T["public"] = T["public_ly"]
T["parttime"] = T["parttime_ly"]
S = pd.concat([pd.read_parquet(f) for f in
               sorted(glob.glob("data/raw/asec/asec_state_*.parquet"))],
              ignore_index=True)
T = T.merge(S, on=["asec_year", "PH_SEQ"], how="left")
# harmonized occupation-pair leaver (definition robustness)
T["leaver_pair"] = np.nan
for ay, g in T.groupby("asec_year"):
    cs = {155, 156, 157, 158, 159} if ay <= 2002 else \
        ({2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360}))
    T.loc[g.index, "leaver_pair"] = (~g["PEIOOCC"].isin(cs)).astype(
        float)


def estimate(d, dep="leaver", kind="probit", fe=("year",),
             weighted=False):
    d = d.dropna(subset=XV + [dep, "WGT"]).copy()
    degenerate = {v for v in XV if d[v].nunique() <= 1}
    xv = [v for v in XV if v not in degenerate]
    fes = []
    if "year" in fe:
        fes.append(pd.get_dummies(d["asec_year"], prefix="y",
                                  drop_first=True, dtype=float))
    if "state" in fe:
        d = d.dropna(subset=["GESTFIPS"])
        fes = [f.loc[d.index] for f in fes]
        fes.append(pd.get_dummies(d["GESTFIPS"].astype(int), prefix="s",
                                  drop_first=True, dtype=float))
    X = sm.add_constant(pd.concat([d[xv].astype(float)] + fes, axis=1))
    y = d[dep].astype(float)
    if kind in ("probit", "logit"):
        cls = sm.Probit if kind == "probit" else sm.Logit
        m = cls(y, X).fit(disp=0, maxiter=200)
        eff = m.get_margeff(at="overall")
        b = dict(zip(xv, eff.margeff[:len(xv)] * 100))
        se = dict(zip(xv, eff.margeff_se[:len(xv)] * 100))
    else:
        w = d["WGT"] if weighted else pd.Series(1.0, index=d.index)
        m = sm.WLS(y, X, weights=w).fit(cov_type="HC1")
        b = {v: m.params[v] * 100 for v in xv}
        se = {v: m.bse[v] * 100 for v in xv}
    return b, se, len(d), degenerate


def stars(b, s):
    z = abs(b / s) if s > 0 else 0
    return "***" if z > 2.576 else "**" if z > 1.96 else \
        "*" if z > 1.645 else ""


def col(spec):
    b, se, n, degenerate = spec
    out = {}
    for v in XV:
        if v in degenerate:
            out[v] = ("--", "")
        else:
            out[v] = (f"{b[v]:.2f}{stars(b[v], se[v])}",
                      f"({se[v]:.2f})")
    out["_N"] = f"{n:,}"
    return out


win = T[T["cal_year"].between(2015, 2024)]
full = T[T["cal_year"].between(1997, 2024)]
print("estimating Table R ...", flush=True)
R_COLS = [
    ("(1) Probit", col(estimate(win, kind="probit"))),
    ("(2) LPM, weighted", col(estimate(win, kind="lpm",
                                       weighted=True))),
    ("(3) Logit", col(estimate(win, kind="logit"))),
    ("(4) LPM, state+year FE", col(estimate(win, kind="lpm",
                                            weighted=True,
                                            fe=("year", "state")))),
    ("(5) Probit, 1997--2024", col(estimate(full, kind="probit"))),
    ("(6) LPM, pair definition", col(estimate(win, dep="leaver_pair",
                                              kind="lpm",
                                              weighted=True))),
]
print("estimating Table S ...", flush=True)
S_COLS = [
    ("Women", col(estimate(win[win["female"] == 1], kind="lpm",
                           weighted=True))),
    ("Men", col(estimate(win[win["female"] == 0], kind="lpm",
                         weighted=True))),
    ("Public", col(estimate(win[win["public"] == 1], kind="lpm",
                            weighted=True))),
    ("Private", col(estimate(win[win["public"] == 0], kind="lpm",
                             weighted=True))),
    ("Under 45", col(estimate(win[win["A_AGE"] < 45], kind="lpm",
                              weighted=True))),
    ("45+", col(estimate(win[win["A_AGE"] >= 45], kind="lpm",
                         weighted=True))),
]


def write_table(cols, fname, drop_vars=()):
    names = [c[0] for c in cols]
    rows = []
    for v in XV:
        if v in drop_vars:
            continue
        rows.append([LABELS[v]] + [c[1][v][0] for c in cols])
        rows.append([""] + [c[1][v][1] for c in cols])
    rows.append(["Observations"] + [c[1]["_N"] for c in cols])
    df = pd.DataFrame(rows, columns=["variable"] + names)
    df.to_csv(f"outputs/{fname}.csv", index=False)
    lines = ["\\begin{tabular}{l" + "c" * len(cols) + "}", "\\toprule",
             " & " + " & ".join(names) + " \\\\", "\\midrule"]
    for r in rows[:-1]:
        lines.append(" & ".join(str(x) for x in r) + " \\\\")
    lines += ["\\midrule",
              " & ".join(["Observations"]
                         + [c[1]["_N"] for c in cols]) + " \\\\",
              "\\bottomrule", "\\end{tabular}"]
    with open(f"report/tables/{fname}.tex", "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(df.to_string(index=False))


write_table(R_COLS, "probit_robustness")
print()
# gender/sector columns drop their own defining regressor
write_table(S_COLS, "probit_subsamples")
print("\n-> outputs/ and report/tables/ written")
