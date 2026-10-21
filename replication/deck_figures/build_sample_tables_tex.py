"""Sample-size tables as compiled LaTeX (booktabs, threeparttable),
placed on two slides with navigation buttons.
Table B1: sample sizes by survey year, ASEC vs the basic monthly files.
Table B2: monthly interviews by panel status (new, returning, repeated)
for 2006, 2015 and 2024.
Writes report/data_cluster/sample_tables.tex, compiles it, crops the
pages and builds report/data_cluster/sample_sizes_slides.pptx.
Run from the repo root."""
import glob
import re
import subprocess
import pandas as pd
from PIL import Image, ImageOps
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ---------------- counts ----------------
def tset(y):
    return {2300, 2310, 2320, 2330} | ({2340} if y <= 2019 else {2360})

monthly, pids, tids = {}, {}, {}
for f in sorted(glob.glob("data/interim/cps_*.parquet")):
    y, m = (int(g) for g in re.search(r"cps_(\d{4})(\d{2})", f).groups())
    d = pd.read_parquet(f, columns=["HRHHID", "HRHHID2", "PULINENO",
                                    "PEMLR", "PTIO1OCD"])
    monthly.setdefault(y, {})[m] = \
        d[["HRHHID", "HRHHID2", "PULINENO"]].drop_duplicates()
    t = d[d.PEMLR.isin([1, 2]) & d.PTIO1OCD.isin(tset(y))]
    tids.setdefault(y, []).append(
        t[["HRHHID", "HRHHID2", "PULINENO"]].drop_duplicates())
upers = {y: len(pd.concat(ms.values()).drop_duplicates())
         for y, ms in monthly.items()}
uteach = {y: len(pd.concat(ts).drop_duplicates())
          for y, ts in tids.items()}
nmonths = {y: len(ms) for y, ms in monthly.items()}

mast = pd.read_parquet("data/processed/asec_master.parquet",
                       columns=["asec_year", "A_AGE", "teacher"])
mast["teacher"] = pd.to_numeric(mast.teacher, errors="coerce")
A = mast[mast.A_AGE >= 18].groupby("asec_year").agg(
    adults=("A_AGE", "size"), teachers=("teacher", "sum"))
tot_ad, tot_te = int(A.adults.sum()), int(A.teachers.sum())
print("ASEC totals:", tot_ad, tot_te)

# month-by-month panel status for three years
SHOW = [2006, 2015, 2024]
newrep = {}
for yr in SHOW:
    last = set()
    for m in range(1, 13):
        last |= set(map(tuple, monthly[yr - 1][m].itertuples(index=False)))
    this = set()
    rows = []
    for m in range(1, 13):
        ids = set(map(tuple, monthly[yr][m].itertuples(index=False)))
        rep = len(ids & this)
        back = len((ids - this) & last)
        new = len(ids) - rep - back
        rows.append((new, back, rep))
        this |= ids
    newrep[yr] = rows
    print(yr, "new+back =", sum(r[0] + r[1] for r in rows),
          "distinct =", upers[yr])

# ---------------- Table B1 ----------------
years = list(A.index)
half = (len(years) + 1) // 2
def b1row(yr):
    ad, te = int(A.loc[yr, "adults"]), int(A.loc[yr, "teachers"])
    if yr in upers:
        star = "" if nmonths[yr] == 12 else r"$^{\dagger}$"
        mp, mt = f"{upers[yr]:,}{star}", f"{uteach[yr]:,}{star}"
    else:
        mp = mt = "--"
    return f"{yr} & {ad:,} & {te:,} & {mp} & {mt}"
lines = []
for i in range(half):
    left = b1row(years[i])
    right = b1row(years[half + i]) if half + i < len(years) else "& & & &"
    lines.append(left + " & " + right + r" \\")
b1body = "\n".join(lines)

# ---------------- Table B2 ----------------
MON = ["January", "February", "March", "April", "May", "June", "July",
       "August", "September", "October", "November", "December"]
b2lines = []
for mi, mn in enumerate(MON):
    cells = []
    for yr in SHOW:
        nw, bk, rp = newrep[yr][mi]
        cells += [f"{nw:,}", f"{rp:,}", f"{bk:,}", f"{nw+bk+rp:,}"]
    row = mn + " & " + " & ".join(cells) + r" \\"
    if mn == "March":
        row = r"\textbf{March} & " + " & ".join(
            rf"\textbf{{{c}}}" for c in cells) + r" \\"
    b2lines.append(row)
sums = []
for yr in SHOW:
    sn = sum(r[0] for r in newrep[yr])
    sb = sum(r[1] for r in newrep[yr])
    sr = sum(r[2] for r in newrep[yr])
    sums += [f"{sn:,}", f"{sr:,}", f"{sb:,}", f"{sn+sb+sr:,}"]
b2sum = "Sum & " + " & ".join(sums) + r" \\"
b2dis = (r"Distinct persons (new $+$ last year) & " + " & ".join(
    rf"\multicolumn{{4}}{{r}}{{{upers[yr]:,}}}" if False else ""
    for yr in []) )
dis_cells = " & ".join(
    rf"\multicolumn{{4}}{{r}}{{\textbf{{{upers[yr]:,}}}}}" for yr in SHOW)
asec_cells = " & ".join(
    rf"\multicolumn{{4}}{{r}}{{\textbf{{{int(A.loc[yr,'adults']):,}}}}}"
    for yr in SHOW)
b2body = "\n".join(b2lines)

NS_AD, NS_TE = f"{tot_ad:,}", f"{tot_te:,}"
tex = (r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[paperwidth=21.5cm,paperheight=24cm,margin=0.6cm]{geometry}
\usepackage{booktabs,threeparttable}
\setlength{\tabcolsep}{4.5pt}
\pagestyle{empty}
\begin{document}

\begin{center}
{\large\bfseries Table B1 --- Sample sizes by survey year:
March supplement and basic monthly files}\\[1.0em]
\begin{threeparttable}
\begin{tabular}{l rr rr @{\hskip 1.3em} l rr rr}
\toprule
 & \multicolumn{2}{c}{ASEC} & \multicolumn{2}{c}{12 months}
 & & \multicolumn{2}{c}{ASEC} & \multicolumn{2}{c}{12 months} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){7-8}\cmidrule(lr){9-10}
Survey & Persons & Teachers & Persons & Teachers
 & Survey & Persons & Teachers & Persons & Teachers \\
\midrule
""" + b1body + r"""
\midrule
\multicolumn{10}{l}{Total, March supplements 1998--2025:\quad
\textbf{""" + NS_AD + r"""} persons, \textbf{""" + NS_TE + r"""}
teachers} \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]
\footnotesize
\item \emph{Notes:} Distinct adults (18+), each counted once per survey
year. \emph{ASEC}: respondents of the March supplement --- the March
sample plus the February--April oversamples --- who answer the
retrospective questions once each. \emph{12 months}: distinct
people appearing in that year's twelve basic monthly files; the CPS
interviews each household in four consecutive months twice over two
years, so a person is interviewed about three times per calendar year.
Monthly microdata from 2005; $^{\dagger}$2025 covers eleven months.
Teachers: longest job last year was school teaching (ASEC); employed in
a school-teaching occupation at a monthly interview (monthly files).
\end{tablenotes}
\end{threeparttable}
\end{center}

\clearpage

\begin{center}
{\large\bfseries Table B2 --- Monthly interviews by panel status:
new, returning and repeated respondents}\\[1.0em]
\begin{threeparttable}
\begin{tabular}{l rrrr rrrr rrrr}
\toprule
 & \multicolumn{4}{c}{2006} & \multicolumn{4}{c}{2015}
 & \multicolumn{4}{c}{2024} \\
\cmidrule(lr){2-5}\cmidrule(lr){6-9}\cmidrule(lr){10-13}
 & New & This yr & Last yr & Total & New & This yr & Last yr & Total
 & New & This yr & Last yr & Total \\
\midrule
""" + b2body + r"""
\midrule
""" + b2sum + r"""
Distinct persons & """ + dis_cells + r""" \\
March supplement (ASEC) & """ + asec_cells + r""" \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]
\footnotesize
\item \emph{Notes:} Adults (18+) per basic monthly file. \emph{New}:
first interview ever; \emph{This yr}: already interviewed in an earlier
month of the calendar year; \emph{Last yr}: returning after being
interviewed the previous year (first appearance this year). Within a
month the three sum to the Total; over the year, New $+$ Last yr counts
each person exactly once and equals the distinct persons. The March
supplement interviews each person once: the March respondents plus the
February--April oversamples, about 1.45$\times$ a single March.
\end{tablenotes}
\end{threeparttable}
\end{center}

\end{document}
""")
open("report/data_cluster/sample_tables.tex", "w").write(tex)
subprocess.run(["pdflatex", "-interaction=nonstopmode",
                "sample_tables.tex"], cwd="report/data_cluster",
               capture_output=True)
subprocess.run(["pdftoppm", "-png", "-r", "300", "sample_tables.pdf",
                "_pngx/sampletab"], cwd="report/data_cluster")
for f in ["report/data_cluster/_pngx/sampletab-1.png",
          "report/data_cluster/_pngx/sampletab-2.png"]:
    im = Image.open(f).convert("RGB")
    l, u, r, b = ImageOps.invert(im).getbbox()
    pad = 30
    im.crop((max(0, l - pad), max(0, u - pad),
             min(im.width, r + pad), min(im.height, b + pad))).save(f)
print("tables compiled and cropped")

# ---------------- slides ----------------
FONT = "Garamond"
INK = RGBColor(0x21, 0x25, 0x29); MUT = RGBColor(0x6B, 0x74, 0x80)
NAVY = RGBColor(0x10, 0x2D, 0x5E); BTNBG = RGBColor(0xBE, 0xD3, 0xEE)
prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BTNS = []
def new_slide(title):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    b = s.shapes.add_textbox(Inches(0.55), Inches(0.24), Inches(10.0),
                             Inches(0.62))
    tf = b.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    r = tf.paragraphs[0].add_run(); r.text = title
    r.font.name = FONT; r.font.size = Pt(28); r.font.bold = True
    r.font.color.rgb = NAVY
    return s
def pic(s, path, box=(0.55, 0.95, 12.2, 5.85)):
    bx, by, bw, bh = box
    with Image.open(path) as im:
        iw, ih = im.size
    sc = min(bw / iw, bh / ih)
    w, h = iw * sc, ih * sc
    s.shapes.add_picture(path, Inches(bx + (bw - w) / 2),
                         Inches(by + (bh - h) / 2), width=Inches(w))
def button(s, x, y, lab, idx):
    w = 0.66 + 0.107 * len(lab)
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x),
                            Inches(y), Inches(w), Inches(0.40))
    sh.fill.solid(); sh.fill.fore_color.rgb = BTNBG
    sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "☞ "
    r.font.name = FONT; r.font.size = Pt(18); r.font.bold = True
    r.font.color.rgb = NAVY
    r = p.add_run(); r.text = lab
    r.font.name = FONT; r.font.size = Pt(14); r.font.color.rgb = NAVY
    BTNS.append((sh, idx))

s = new_slide("Sample sizes by survey year")
pic(s, "report/data_cluster/_pngx/sampletab-1.png")
button(s, 10.35, 0.30, "sample sizes", 0)
b = s.shapes.add_textbox(Inches(10.35), Inches(0.74), Inches(2.6),
                         Inches(0.3))
r = b.text_frame.paragraphs[0].add_run()
r.text = "(copy this button to the main deck)"
r.font.name = FONT; r.font.size = Pt(9.5); r.font.color.rgb = MUT
button(s, 0.70, 6.92, "monthly detail", 1)
button(s, 11.45, 6.92, "back", 0)

s = new_slide("Monthly interviews by panel status")
pic(s, "report/data_cluster/_pngx/sampletab-2.png")
button(s, 11.45, 6.92, "back", 0)

slides = list(prs.slides)
for sh, idx in BTNS:
    sh.click_action.target_slide = slides[idx]
prs.save("report/data_cluster/sample_sizes_slides.pptx")
print("saved sample_sizes_slides.pptx")
