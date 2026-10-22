"""Render outputs/attrition_selection.csv as the paper-style Table A4
(selection into panel non-observation), compile it with pdflatex and
crop the page to report/data_cluster/_pngx/seltab-1.png.
Run from the repo root after build_attrition_selection.py."""
import os
import subprocess
import pandas as pd
from PIL import Image, ImageOps

D = pd.read_csv("outputs/attrition_selection.csv").set_index("var")
n = int(D.n.iloc[0])
base = D.base.iloc[0]

LAB = [("fullyear", "Full-year contract"),
       ("parttime", "Part-time contract"),
       ("pension", "Employer pension plan"),
       ("public_ly", "Public sector"),
       ("baby", "New baby during the year"),
       ("nkids", "Number of children"),
       ("kid_u6", "Youngest child under 6"),
       ("married", "Married"),
       ("sepdiv", "Separated or divorced"),
       ("female", "Female"),
       ("black", "Black"),
       ("ma_plus", "Master's degree or higher"),
       ("badhealth", "Fair or poor health"),
       ("disab", "With a disability"),
       ("lowinc", "Bottom-quartile household income")]

def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""

rows = []
for v, lab in LAB:
    r = D.loc[v]
    rows.append(
        f"{lab} & ${r.lpm:+.2f}$\\sym{{{stars(r.lpm_p)}}} & "
        f"${r.probit_ame:+.2f}$ \\\\\n & ({r.lpm_se:.2f}) & \\\\[0.2em]")
body = "\n".join(rows)

tex = r"""% Selection into panel non-observation (Table A4).
% Build: pdflatex attrition_selection_table.tex
\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[paperwidth=18cm,paperheight=26cm,margin=0.6cm]{geometry}
\usepackage{booktabs,threeparttable}
\setlength{\tabcolsep}{12pt}
\pagestyle{empty}
\newcommand{\sym}[1]{\rlap{$^{#1}$}}
\begin{document}

\begin{center}
{\large\bfseries Table A4 --- Is the linkage loss selective?}\\[1.0em]
\begin{threeparttable}
\begin{tabular}{lcc}
\toprule
 & \multicolumn{2}{c}{Dependent variable: not observed next March (0--100)} \\
\cmidrule(lr){2-3}
 & LPM & Probit AME \\
\midrule
""" + body + r"""
\midrule
Year fixed effects & Yes & Yes \\
Observations       & """ + f"{n:,}" + r""" & """ + f"{n:,}" + r""" \\
Weighted share not observed & \multicolumn{2}{c}{""" + f"{base:.1f}" + r"""\%} \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]
\footnotesize
\item \emph{Notes:} College-graduate teachers aged at most 70 in the
2019--2024 ASEC. The dependent variable equals 100 when the person is
not found in the following March's ASEC by the validated match
(identifier, sex, race, age advancing at most two years). Coefficients
are percentage points. Roughly half of the non-observations are
mechanical: the 4-8-4 rotation retires about half of each March sample
before the next March, independently of characteristics. Weighted
least squares with ASEC supplement weights and heteroskedasticity-robust
(HC1) standard errors in parentheses; a quadratic in age is included.
Non-observation follows the residential-stability profile (unmarried,
Black, more children) and is uncorrelated with the health, income and
job variables that drive leaving.
$^{*}$ $p<0.10$, $^{**}$ $p<0.05$, $^{***}$ $p<0.01$.
\end{tablenotes}
\end{threeparttable}
\end{center}
\end{document}
"""
with open("report/data_cluster/attrition_selection_table.tex", "w") as f:
    f.write(tex)

subprocess.run(["pdflatex", "-interaction=nonstopmode",
                "attrition_selection_table.tex"],
               cwd="report/data_cluster", check=True,
               stdout=subprocess.DEVNULL)
os.makedirs("report/data_cluster/_pngx", exist_ok=True)
subprocess.run(["pdftoppm", "-png", "-r", "300", "-singlefile",
                "report/data_cluster/attrition_selection_table.pdf",
                "report/data_cluster/_pngx/seltab-1"], check=True)
im = Image.open("report/data_cluster/_pngx/seltab-1.png").convert("RGB")
bbox = ImageOps.invert(im).getbbox()
pad = 30
im = im.crop((max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
              min(bbox[2] + pad, im.width), min(bbox[3] + pad, im.height)))
im.save("report/data_cluster/_pngx/seltab-1.png")
im.save("report/data_cluster/figures/seltab-1.png")
print("saved seltab-1.png")
