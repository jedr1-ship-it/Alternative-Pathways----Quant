"""
Why, and to where: destination-specific models of teacher exit. Separate
probits for each exit route (another occupation, out of the labor force,
unemployment) with the full covariate set and base-year fixed effects, the
modern national counterpart of Stinebrickner (2002) and of the competing
risks question of Dolton and van der Klaauw (1999). Also the wage submodel
by destination on the outgoing-rotation subsample. Writes
report/table_destmodel.tex.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from covariates import load_panel, COVS, LABELS

df = load_panel()
B = df[df["sampleB"]].copy()
B["dest_occ"] = ((B["leaver_p"] == 1)
                 & (B["dest"] == "other occupation")).astype(int)
B["dest_olf"] = ((B["leaver_p"] == 1)
                 & (B["dest"] == "out of labor force")).astype(int)
B["dest_unemp"] = ((B["leaver_p"] == 1)
                   & (B["dest"] == "unemployed")).astype(int)
rhs = " + ".join(COVS) + " + C(base_year)"

SHOW = ["parttime", "public", "prof_phd", "ma_plus", "black", "noncitizen",
        "new_baby", "fem_newbaby", "n_children", "female"]


def stars(p):
    return "$^{***}$" if p < 0.01 else "$^{**}$" if p < 0.05 else \
        "$^{*}$" if p < 0.1 else ""


def fit_ames(y, data, extra=""):
    m = smf.probit(f"{y} ~ " + rhs + extra, data=data).fit(
        cov_type="cluster", cov_kwds={"groups": data["HRHHID"]}, disp=False)
    me = m.get_margeff(at="overall")
    idx = list(me.summary_frame().index)
    return m, {v: (me.margeff[idx.index(v)] * 100,
                   me.margeff_se[idx.index(v)] * 100,
                   me.pvalues[idx.index(v)])
               for v in idx if v in SHOW + ["lnw"]}


OUTS = [("leaver_p", "Any exit"), ("dest_occ", "Another occupation"),
        ("dest_olf", "Out of labor force"), ("dest_unemp", "Unemployed")]
models, ames = {}, {}
for y, lab in OUTS:
    print("probit", y, "...", flush=True)
    models[y], ames[y] = fit_ames(y, B)
    print({v: round(a[0], 2) for v, a in ames[y].items()}, flush=True)

# wage submodel by destination: earnings exist only for MIS-4 baselines,
# which have no re-interview window, so this panel uses the conventional
# 12-month definition, as in the main wage result of the paper
W = df[(df["HRMIS_0"] == 4) & df["wkearn"].notna()].copy()
W["lnw"] = np.log(W["wkearn"].clip(lower=50))
W["w_occ"] = ((W["leaver12"] == 1)
              & (W["dest"] == "other occupation")).astype(int)
W["w_olf"] = ((W["leaver12"] == 1)
              & (W["dest"] == "out of labor force")).astype(int)
W["w_unemp"] = ((W["leaver12"] == 1)
                & (W["dest"] == "unemployed")).astype(int)
WOUTS = ["leaver12", "w_occ", "w_olf", "w_unemp"]
wame = {}
for y, wy in zip([o for o, _ in OUTS], WOUTS):
    print("wage probit", wy, "...", flush=True)
    _, a = fit_ames(wy, W, extra=" + lnw")
    wame[y] = a["lnw"]
    print(wy, "lnw AME", round(a["lnw"][0], 3), flush=True)

LABELS_TEX = {**LABELS,
              "parttime": "Part-time ($<$35 h/week)"}
with open("report/table_destmodel.tex", "w") as fh:
    fh.write("""\\begin{tabular}{lcccc}
\\toprule
 & (1) & (2) & (3) & (4) \\\\
 & Any exit & Another & Out of the & Unemployed \\\\
 & & occupation & labor force & \\\\
\\midrule
""")
    for v in SHOW:
        row, serow = [LABELS_TEX[v]], [""]
        for y, _ in OUTS:
            est, se, p = ames[y][v]
            row.append(f"{est:.2f}{stars(p)}")
            serow.append(f"({se:.2f})")
        fh.write(" & ".join(row) + " \\\\\n")
        fh.write(" & ".join(serow) + " \\\\[2pt]\n")
    fh.write("\\midrule\n\\multicolumn{5}{l}{\\textit{Outgoing-rotation"
             " subsample with weekly earnings}} \\\\[2pt]\n")
    row, serow = ["Log weekly earnings"], [""]
    for y, _ in OUTS:
        est, se, p = wame[y]
        row.append(f"{est:.2f}{stars(p)}")
        serow.append(f"({se:.2f})")
    fh.write(" & ".join(row) + " \\\\\n")
    fh.write(" & ".join(serow) + " \\\\[2pt]\n")
    mdep = [B["leaver_p"].mean(), B["dest_occ"].mean(), B["dest_olf"].mean(),
            B["dest_unemp"].mean()]
    fh.write("\\midrule\nBase-year fixed effects & Yes & Yes & Yes & Yes \\\\\n"
             "Full covariate set & Yes & Yes & Yes & Yes \\\\\n"
             "Mean of dependent variable & "
             + " & ".join(f"{m:.3f}" for m in mdep) + " \\\\\n"
             f"Observations & {len(B):,} & {len(B):,} & {len(B):,} & {len(B):,} \\\\\n"
             f"\\quad wage subsample & {len(W):,} & {len(W):,} & {len(W):,} & {len(W):,} \\\\\n"
             "\\bottomrule\n\\end{tabular}\n")
print("wrote report/table_destmodel.tex")
comp = pd.DataFrame({lab: {v: ames[y][v][0] for v in SHOW}
                     for y, lab in OUTS})
comp.loc["lnw"] = [wame[y][0] for y, _ in OUTS]
comp.round(2).to_csv("outputs/destination_model.csv")
print(comp.round(2).to_string())
