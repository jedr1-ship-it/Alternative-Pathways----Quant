"""Appendix coefficient plot: probit AMEs estimated separately on
calendar 1997-2017 and on the main-deck window 2018-2024, with the
controls available throughout. Writes report/figures_deck/
ame_twoperiods.{pdf,png} and outputs/ame_twoperiods.csv."""
import sys
sys.path.insert(0, "replication")
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["EB Garamond", "STIXGeneral",
                                    "DejaVu Serif"],
                     "mathtext.fontset": "stix"})
INK, NAVY, GRAY = "#23373B", "#1F3864", "#8A9096"

d = pd.read_parquet("data/processed/asec_master.parquet",
    columns=["cal_year", "teacher", "ba_plus", "ma_plus", "A_AGE",
             "A_MARITL", "female", "black", "married", "n_children",
             "child_u6", "new_baby", "pension", "parttime_ly",
             "fullyear", "public_ly", "leaver"])
for c in d.columns:
    d[c] = pd.to_numeric(d[c], errors="coerce")
B = d[(d.teacher == 1) & (d.ba_plus == 1) & d.A_AGE.between(18, 70)
      & d.leaver.notna()].copy()
B["sepdiv"] = B.A_MARITL.isin([4, 5]).astype(float)
B["age"] = B.A_AGE
B["age2"] = B.A_AGE ** 2
XV = ["fullyear", "parttime_ly", "pension", "public_ly",
      "new_baby", "child_u6", "n_children", "married", "sepdiv",
      "age", "age2", "female", "black", "ma_plus"]
B = B.dropna(subset=XV + ["leaver"])

def fit(lo, hi):
    R = B[B.cal_year.between(lo, hi)]
    X = pd.concat([R[XV], pd.get_dummies(R.cal_year.astype(int),
                   prefix="y", drop_first=True).astype(float)], axis=1)
    X = sm.add_constant(X)
    m = sm.Probit(R.leaver.astype(float), X).fit(disp=0, maxiter=200)
    mg = m.get_margeff(at="overall")
    me = pd.Series(mg.margeff, index=X.columns[1:])[XV] * 100
    se = pd.Series(mg.margeff_se, index=X.columns[1:])[XV] * 100
    return me, se, len(R), 100 * R.leaver.mean()

me1, se1, n1, base1 = fit(1997, 2017)
me2, se2, n2, base2 = fit(2018, 2024)
print(f"1997-2017: N={n1:,} base={base1:.1f} | 2018-2024: N={n2:,} "
      f"base={base2:.1f}")
pd.DataFrame({"ame_9717": me1, "se_9717": se1,
              "ame_1824": me2, "se_1824": se2}).to_csv(
    "outputs/ame_twoperiods.csv")

GROUPS = [
 ("Job attachment", [("fullyear", "Full-year contract"),
                     ("parttime_ly", "Part-time contract")]),
 ("Compensation", [("pension", "Employer pension plan"),
                   ("public_ly", "Public sector")]),
 ("Family", [("new_baby", "New baby during the year"),
             ("child_u6", "Child under 6"),
             ("n_children", "Number of children"),
             ("married", "Married"),
             ("sepdiv", "Separated or divorced")]),
 ("Demographics", [("age", "Age (per year)"),
                   ("female", "Female"),
                   ("black", "Black"),
                   ("ma_plus", "Master's degree or higher")]),
]
fig, ax = plt.subplots(figsize=(11.6, 6.8))
yy = 0
yticks, ylabels, heads = [], [], []
for gname, items in GROUPS:
    heads.append((yy, gname))
    yy -= 1
    for v, lab in items:
        for me, se, dy, col, filled in [(me1, se1, -0.20, GRAY, False),
                                        (me2, se2, 0.20, NAVY, True)]:
            a, s = me[v], se[v]
            ax.plot([a - 1.96 * s, a + 1.96 * s], [yy + dy, yy + dy],
                    color=col, lw=1.1, solid_capstyle="butt")
            ax.plot(a, yy + dy, "o", ms=6,
                    mfc=col if filled else "white", mec=col, mew=1.2)
        yticks.append(yy); ylabels.append(lab)
        yy -= 1
    yy -= 0.4
ax.axvline(0, color="#000000", lw=0.8)
for hy, lab in heads:
    ax.text(-13.4, hy, lab, fontsize=12, fontweight="bold", color=INK,
            va="center")
ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=11)
ax.set_xlim(-13.5, 10)
ax.set_ylim(yy + 0.2, 1.2)
ax.set_xticks(range(-12, 10, 3))
ax.set_xlabel("average marginal effect on the probability of leaving "
              "(percentage points)", fontsize=11, color=INK)
from matplotlib.lines import Line2D
ax.legend(handles=[
    Line2D([], [], marker="o", color=NAVY, mfc=NAVY, lw=1.1,
           label=f"2018–2024 (the deck's window, N = {n2:,})"),
    Line2D([], [], marker="o", color=GRAY, mfc="white", lw=1.1,
           label=f"1997–2017 (N = {n1:,})")],
    frameon=False, fontsize=10.5, loc="lower right")
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("report/figures_deck/ame_twoperiods.pdf")
fig.savefig("report/figures_deck/ame_twoperiods.png", dpi=200)
print("saved ame_twoperiods")
