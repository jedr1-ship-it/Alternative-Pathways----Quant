"""
MAIN ANALYSIS of the paper, on the corrected instrument. Our questions --
who leaves teaching, what predicts it, where do they go, how has it moved --
answered with the retrospective March/ASEC measure (the instrument this
project validated person-by-person against the linked panel).

Instrument and universe (fixed after the validation work):
  teacher   = occupation of the longest job held LAST year in K-12 codes
              2300/2310/2320/2330 + teachers n.e.c. (2340 old / 2360 new
              scheme), college graduates (A_HGA >= 43), age 18+
  leaver    = no longer teaching now: employed in another occupation
              (A_LFSR 1-2, PEIOOCC not teaching), unemployed (A_LFSR 3-4),
              or out of the labor force (A_LFSR 0/7)
  window    = ASEC surveys 2016-2025 -> calendar years 2015-2024, MARSUPWT

Outputs (outputs/main_*.csv):
  1 annual leaver series (evolution, COVID)
  2 stayer-vs-leaver profile (characteristics measured in the teaching year)
  3 leaver model: probit average marginal effects, ranked
  4 destinations: the per-100-teachers flow, and top destination occupations
  5 heterogeneity: age x sex x public/private
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.api as sm

RAW = "data/raw/asec"
W = "MARSUPWT"


def teacher_codes(ay):
    return {2300, 2310, 2320, 2330} | ({2340} if ay <= 2019 else {2360})


df = pd.concat([pd.read_parquet(f) for f in
                sorted(glob.glob(f"{RAW}/asec_ha_*.parquet"))],
               ignore_index=True)
for c in df.columns:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df[(df["A_HGA"] >= 43) & (df["A_AGE"] >= 18)]

parts = []
for ay, g in df.groupby("asec_year"):
    cset = teacher_codes(int(ay))
    b = g[g["OCCUP"].isin(cset)].copy()
    emp_now = b["A_LFSR"].isin([1, 2])
    b["switch"] = (emp_now & ~b["PEIOOCC"].isin(cset)).astype(int)
    b["unemp"] = b["A_LFSR"].isin([3, 4]).astype(int)
    b["leftlf"] = (~b["A_LFSR"].isin([1, 2, 3, 4])).astype(int)
    b["leaver"] = (b["switch"] | b["unemp"] | b["leftlf"]).astype(int)
    parts.append(b)
T = pd.concat(parts, ignore_index=True)
T["cal_year"] = T["asec_year"] - 1
print(f"teachers (BA+, K-12) pooled 2015-2024: {len(T):,}")


def wavg(d, col):
    v = d[col].astype(float)
    ok = v.notna() & d[W].notna()
    return np.average(v[ok], weights=d.loc[ok, W])


# ---------- 1. annual series ----------
ann = [{"cal_year": int(y), "leaver_%": round(wavg(g, "leaver") * 100, 2),
        "to_other_job": round(wavg(g, "switch") * 100, 2),
        "unemployed": round(wavg(g, "unemp") * 100, 2),
        "out_of_LF": round(wavg(g, "leftlf") * 100, 2), "n": len(g)}
       for y, g in T.groupby("cal_year")]
ANN = pd.DataFrame(ann)
print("\n=== 1. EVOLUCION ANUAL ===")
print(ANN.to_string(index=False))
ANN.to_csv("outputs/main_annual.csv", index=False)
print(f"pooled: {wavg(T,'leaver')*100:.2f}%")

# ---------- covariates (measured in the teaching year) ----------
T["female"] = (T["A_SEX"] == 2).astype(int)
T["black"] = (T["PRDTRACE"] == 2).astype(int)
T["married"] = T["A_MARITL"].isin([1, 2, 3]).astype(int)
T["sepdiv"] = T["A_MARITL"].isin([5, 6]).astype(int)
T["ma_plus"] = (T["A_HGA"] >= 44).astype(int)
T["public"] = T["LJCW"].isin([2, 3, 4]).astype(int)
T["pension"] = (T["PENPLAN"] == 1).astype(int)
T["parttime"] = (T["HRSWK"].between(1, 34)).astype(int)
T["fullyear"] = (T["WKSWORK"] >= 50).astype(int)
T["earn_wk"] = np.where((T["WSAL_VAL"] > 0) & (T["WKSWORK"] > 0),
                        T["WSAL_VAL"] / T["WKSWORK"], np.nan)
T["age2"] = T["A_AGE"] ** 2

# ---------- 2. stayer vs leaver profile ----------
PROF_VARS = [("Edad", "A_AGE", "num"), ("Mujer", "female", "pct"),
             ("Negra/o", "black", "pct"), ("Casada/o", "married", "pct"),
             ("Separada/divorciada", "sepdiv", "pct"),
             ("Master o mas", "ma_plus", "pct"),
             ("Escuela publica", "public", "pct"),
             ("Con plan de pension", "pension", "pct"),
             ("Tiempo parcial (<35h)", "parttime", "pct"),
             ("Ano completo (50+ sem)", "fullyear", "pct"),
             ("Salario semanal ($)", "earn_wk", "num")]
rows = []
S, L = T[T["leaver"] == 0], T[T["leaver"] == 1]
for lab, v, kind in PROF_VARS:
    a, b = wavg(S, v), wavg(L, v)
    f = (lambda x: round(x * 100, 1)) if kind == "pct" else \
        (lambda x: round(x, 1))
    rows.append({"variable": lab, "stayer": f(a), "leaver": f(b),
                 "diff": f(b - a)})
PR = pd.DataFrame(rows)
print("\n=== 2. PERFIL: stayer vs leaver (caracteristicas del ano docente) ===")
print(PR.to_string(index=False))
PR.to_csv("outputs/main_profile.csv", index=False)

# ---------- 3. probit AME, ranked ----------
XV = ["A_AGE", "age2", "female", "black", "married", "sepdiv", "ma_plus",
      "public", "pension", "parttime", "fullyear"]
sub = T.dropna(subset=XV + ["leaver", W]).copy()
yd = pd.get_dummies(sub["asec_year"], prefix="y", drop_first=True,
                    dtype=float)
X = sm.add_constant(pd.concat([sub[XV].astype(float), yd], axis=1))
pm = sm.Probit(sub["leaver"].astype(float), X).fit(disp=0)
ame = pm.get_margeff(at="overall")
res = pd.DataFrame({"var": XV,
                    "AME_pp": (ame.margeff[:len(XV)] * 100).round(2),
                    "se_pp": (ame.margeff_se[:len(XV)] * 100).round(2)})
res["absAME"] = res["AME_pp"].abs()
res = res.sort_values("absAME", ascending=False).drop(columns="absAME")
print("\n=== 3. MODELO DE ABANDONO: efectos marginales (probit, year FE) ===")
print(res.to_string(index=False))
res.to_csv("outputs/main_ame.csv", index=False)

# ---------- 4. destinations: per-100 flow + top occupations ----------
p100 = {"siguen ensenando": 100 - wavg(T, "leaver") * 100,
        "otro empleo": wavg(T, "switch") * 100,
        "parados": wavg(T, "unemp") * 100,
        "fuera de la fuerza laboral": wavg(T, "leftlf") * 100}
print("\n=== 4. DE CADA 100 DOCENTES (pooled 2015-2024) ===")
for k, v in p100.items():
    print(f"  {k:28s}: {v:5.1f}")
pd.Series(p100).round(2).to_csv("outputs/main_flow100.csv")

sw = T[T["switch"] == 1].copy()
lab = pd.read_csv("outputs/occ2018_labels.csv").set_index("code")["label"]
top = (sw.groupby("PEIOOCC")[W].sum() / sw[W].sum() * 100).sort_values(
    ascending=False).head(12)
DEST = pd.DataFrame({"share_%": top.round(1),
                     "occupation": [lab.get(int(c), "?") for c in top.index]})
print("\n  destino de los que cambian de empleo (top 12, % de switchers):")
print(DEST.to_string())
DEST.to_csv("outputs/main_destinations.csv")
edu_field = sw["PEIOOCC"].between(2200, 2555)
print(f"  ...y {np.average(edu_field, weights=sw[W])*100:.1f}% de los "
      f"switchers permanece en ocupaciones educativas (2200-2555)")

# ---------- 5. heterogeneity ----------
print("\n=== 5. HETEROGENEIDAD (leaver %) ===")
het = []
for lab2, m in [("mujeres", T["female"] == 1), ("hombres", T["female"] == 0),
                ("publica", T["public"] == 1), ("privada", T["public"] == 0),
                ("21-30", T["A_AGE"].between(21, 30)),
                ("31-45", T["A_AGE"].between(31, 45)),
                ("46-55", T["A_AGE"].between(46, 55)),
                ("56-64", T["A_AGE"].between(56, 64)),
                ("65+", T["A_AGE"] >= 65)]:
    d = T[m]
    het.append({"grupo": lab2, "leaver_%": round(wavg(d, "leaver") * 100, 2),
                "n": len(d)})
HET = pd.DataFrame(het)
print(HET.to_string(index=False))
HET.to_csv("outputs/main_heterogeneity.csv", index=False)
