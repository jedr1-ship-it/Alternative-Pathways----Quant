"""Two appendix slides on sample sizes, in one consistent unit:
distinct people (adults 18+).
Slide 1: survey by survey, all years - the March supplement (persons
and teachers, each person once) next to the distinct persons and
teachers seen across that year's twelve monthly files (from 2005).
Slide 2: month by month for 2006/2015/2024 - every interview split into
new, back from last year, and repeats from earlier months of the year.
Run from the repo root. Writes report/data_cluster/sample_sizes_slides.pptx."""
import glob
import re
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

OUT = "report/data_cluster/sample_sizes_slides.pptx"
FONT = "Garamond"
INK = RGBColor(0x21, 0x25, 0x29)
MUT = RGBColor(0x6B, 0x74, 0x80)
NAVY = RGBColor(0x10, 0x2D, 0x5E)
BTNBG = RGBColor(0xBE, 0xD3, 0xEE)

# ---------------- counts ----------------
def tset(y):
    return {2300, 2310, 2320, 2330} | ({2340} if y <= 2019 else {2360})

monthly, pids, tids = {}, {}, {}
for f in sorted(glob.glob("data/interim/cps_*.parquet")):
    y, m = (int(g) for g in re.search(r"cps_(\d{4})(\d{2})", f).groups())
    d = pd.read_parquet(f, columns=["HRHHID", "HRHHID2", "PULINENO",
                                    "PEMLR", "PTIO1OCD"])
    monthly.setdefault(y, {})[m] = len(d)
    pids.setdefault(y, []).append(
        d[["HRHHID", "HRHHID2", "PULINENO"]].drop_duplicates())
    t = d[d.PEMLR.isin([1, 2]) & d.PTIO1OCD.isin(tset(y))]
    tids.setdefault(y, []).append(
        t[["HRHHID", "HRHHID2", "PULINENO"]].drop_duplicates())
upers = {y: len(pd.concat(ps).drop_duplicates()) for y, ps in pids.items()}
uteach = {y: len(pd.concat(ts).drop_duplicates()) for y, ts in tids.items()}
interviews = {y: sum(ms.values()) for y, ms in monthly.items()}
nmonths = {y: len(ms) for y, ms in monthly.items()}

mast = pd.read_parquet("data/processed/asec_master.parquet",
                       columns=["asec_year", "A_AGE", "teacher"])
mast["teacher"] = pd.to_numeric(mast.teacher, errors="coerce")
A = mast[mast.A_AGE >= 18].groupby("asec_year").agg(
    adults=("A_AGE", "size"), teachers=("teacher", "sum"))
tot_ad, tot_te = int(A.adults.sum()), int(A.teachers.sum())
print("ASEC totals:", tot_ad, tot_te)
print("monthly distinct, e.g. 2006:", upers.get(2006), uteach.get(2006))

# ---------------- pptx helpers ----------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
BTNS = []

def new_slide(title):
    s = prs.slides.add_slide(blank)
    box = s.shapes.add_textbox(Inches(0.55), Inches(0.24), Inches(10.5),
                               Inches(0.62))
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    r = tf.paragraphs[0].add_run(); r.text = title
    r.font.name = FONT; r.font.size = Pt(28); r.font.bold = True
    r.font.color.rgb = NAVY
    return s

def text(s, x, y, w, t, size=12, bold=False, color=INK,
         align=PP_ALIGN.LEFT, italic=False):
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w),
                               Inches(size / 50))
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = t
    f = r.font
    f.name = FONT; f.size = Pt(size); f.bold = bold; f.italic = italic
    f.color.rgb = color
    return box

def rule(s, x, y, w, weight=1.0):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x),
                                Inches(y), Inches(x + w), Inches(y))
    ln.line.color.rgb = INK; ln.line.width = Pt(weight)
    ln.shadow.inherit = False

def button(s, x, y, label, target_idx):
    lab = label[0].upper() + label[1:]
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
    BTNS.append((sh, target_idx))

# ---------------- slide 1: survey by survey, all years ----------------
s1 = new_slide("The sample, survey by survey")
years = list(A.index)
half = (len(years) + 1) // 2
RH = 0.268
# per block: survey | ASEC persons | ASEC teachers | 12m persons | 12m teachers
CW = [(0.00, 0.52), (0.52, 1.04), (1.56, 0.82), (2.38, 1.10), (3.48, 0.84)]
BW = 4.32

def cell(s, bx, y, col, t, bold=False, color=INK, size=11.5):
    x0, w = CW[col]
    text(s, bx + x0, y, w, t, size=size, bold=bold, color=color,
         align=PP_ALIGN.LEFT if col == 0 else PP_ALIGN.RIGHT)

for bi, block in enumerate([years[:half], years[half:]]):
    bx = 0.70 + bi * 6.50
    y = 1.32
    rule(s1, bx, y - 0.07, BW, weight=1.4)
    # grouped header
    text(s1, bx + CW[1][0], y, CW[1][1] + CW[2][1], "March suppl.",
         size=11.5, bold=True, align=PP_ALIGN.CENTER)
    text(s1, bx + CW[3][0], y, CW[3][1] + CW[4][1], "All 12 months*",
         size=11.5, bold=True, align=PP_ALIGN.CENTER)
    y += 0.26
    cell(s1, bx, y, 0, "Survey", True)
    cell(s1, bx, y, 1, "Persons", True, MUT, 10.5)
    cell(s1, bx, y, 2, "Teachers", True, MUT, 10.5)
    cell(s1, bx, y, 3, "Persons", True, MUT, 10.5)
    cell(s1, bx, y, 4, "Teachers", True, MUT, 10.5)
    rule(s1, bx, y + 0.24, BW, weight=0.6)
    y += 0.32
    for yr in block:
        ad, te = int(A.loc[yr, "adults"]), int(A.loc[yr, "teachers"])
        star = "" if nmonths.get(yr, 12) == 12 else "*"
        mp = f"{upers[yr]:,}{star}" if yr in upers else "–"
        mt = f"{uteach[yr]:,}{star}" if yr in uteach else "–"
        cell(s1, bx, y, 0, str(yr))
        cell(s1, bx, y, 1, f"{ad:,}")
        cell(s1, bx, y, 2, f"{te:,}")
        cell(s1, bx, y, 3, mp)
        cell(s1, bx, y, 4, mt)
        y += RH
    rule(s1, bx, y + 0.03, BW, weight=1.4)
ytot = 1.32 + 0.26 + 0.32 + half * RH + 0.12
text(s1, 0.70 + 6.50, ytot, 6.0,
     f"Total (ASEC)   {tot_ad:,} persons, {tot_te:,} teachers",
     size=12, bold=True, color=NAVY)
text(s1, 0.70, ytot, 6.1,
     "Distinct adults (18+), each counted once per year. March suppl.: "
     "the March respondents plus the February–April oversamples. "
     "* All 12 months: people seen across the year's twelve monthly "
     "files, interviewed about three times each (files from 2005; 2025: "
     "eleven months). Teachers: longest job last year (ASEC); employed "
     "in a teaching occupation at any interview (monthly).",
     size=9.5, color=MUT)
button(s1, 10.35, 0.30, "sample sizes", 0)
text(s1, 10.35, 0.74, 2.6, "(copy this button to the main deck)",
     size=9.5, color=MUT)
button(s1, 0.70, 6.92, "monthly samples", 1)
button(s1, 11.45, 6.92, "back", 0)

# ---------------- slide 2: month by month, new vs seen before ----------
SHOW = [2006, 2015, 2024]
def ids_of(y, m):
    d = pd.read_parquet(f"data/interim/cps_{y}{m:02d}.parquet",
                        columns=["HRHHID", "HRHHID2", "PULINENO"])
    return set(map(tuple, d.drop_duplicates().itertuples(index=False)))

newrep = {}
for yr in SHOW:
    last = set()
    for m in range(1, 13):          # previous year: the panel's memory
        last |= ids_of(yr - 1, m)
    this = set()
    rows = []
    for m in range(1, 13):
        ids = ids_of(yr, m)
        rep = len(ids & this)                 # seen earlier this year
        back = len((ids - this) & last)       # first time this year,
        new = len(ids) - rep - back           # interviewed last year
        rows.append((new, back, rep))
        this |= ids
    newrep[yr] = rows
    print(yr, "new:", sum(r[0] for r in rows), "+ back:",
          sum(r[1] for r in rows), "= distinct:", upers[yr])

s2 = new_slide("The sample, month by month")
MON = ["January", "February", "March", "April", "May", "June", "July",
      "August", "September", "October", "November", "December"]
x0, wlab = 0.50, 1.00
CWS = [0.66, 1.00, 1.00, 0.80]      # new, seen this yr, seen last yr, total
BW2 = sum(CWS)
gap = 0.24
y = 1.26
TW = wlab + 3 * (BW2 + gap) - gap
HD = ["New", "Seen this yr", "Seen last yr", "Total"]
rule(s2, x0, y - 0.07, TW, weight=1.4)
for i, yr in enumerate(SHOW):
    bx = x0 + wlab + i * (BW2 + gap)
    text(s2, bx, y, BW2, str(yr), size=12, bold=True, align=PP_ALIGN.CENTER)
    cx = bx
    for w, h in zip(CWS, HD):
        text(s2, cx, y + 0.27, w, h, size=9, bold=True,
             align=PP_ALIGN.RIGHT, color=MUT)
        cx += w
rule(s2, x0, y + 0.56, TW, weight=0.6)
y += 0.64
for mi, mname in enumerate(MON):
    bold = (mname == "March")
    c = NAVY if bold else INK
    text(s2, x0, y, wlab, mname, size=9.5, bold=bold, color=c)
    for i, yr in enumerate(SHOW):
        bx = x0 + wlab + i * (BW2 + gap)
        nw, bk, rp = newrep[yr][mi]
        vals = [nw, rp, bk, nw + rp + bk]
        cx = bx
        for w, v in zip(CWS, vals):
            text(s2, cx, y, w, f"{v:,}", size=9.5, bold=bold, color=c,
                 align=PP_ALIGN.RIGHT)
            cx += w
    y += 0.232
rule(s2, x0, y + 0.02, TW, weight=0.6)
y += 0.08
text(s2, x0, y, wlab, "Sum", size=9.5, bold=True)
for i, yr in enumerate(SHOW):
    bx = x0 + wlab + i * (BW2 + gap)
    sn = sum(r[0] for r in newrep[yr])
    sb = sum(r[1] for r in newrep[yr])
    sr = sum(r[2] for r in newrep[yr])
    cx = bx
    for w, v in zip(CWS, [sn, sr, sb, sn + sb + sr]):
        text(s2, cx, y, w, f"{v:,}", size=9.5, bold=True,
             align=PP_ALIGN.RIGHT)
        cx += w
y += 0.26
text(s2, x0, y, wlab + 2.6, "Distinct persons (New + Seen last yr)",
     size=9.5, bold=True)
for i, yr in enumerate(SHOW):
    bx = x0 + wlab + i * (BW2 + gap)
    text(s2, bx, y, BW2, f"{upers[yr]:,}", size=9.5, bold=True,
         align=PP_ALIGN.RIGHT)
y += 0.26
text(s2, x0, y, wlab + 2.6, "March supplement (ASEC), each person once",
     size=9.5, bold=True, color=NAVY)
for i, yr in enumerate(SHOW):
    bx = x0 + wlab + i * (BW2 + gap)
    text(s2, bx, y, BW2, f"{int(A.loc[yr, 'adults']):,}", size=9.5,
         bold=True, color=NAVY, align=PP_ALIGN.RIGHT)
rule(s2, x0, y + 0.26, TW, weight=1.4)
text(s2, x0, y + 0.40, 12.3,
     "Adults (18+). New: first interview ever. Seen last yr: back after "
     "being interviewed the previous year (first time this year). Seen "
     "this yr: already interviewed in an earlier month of the year. "
     "Within a month the three sum to the Total; down the year, New + "
     "Seen last yr counts each person exactly once → the distinct "
     "persons. The ASEC interviews each person once: the March "
     "respondents plus the February–April oversamples, 1.45× a "
     "single March.", size=9.5, color=MUT)
button(s2, 11.45, 6.92, "back", 0)

slides = list(prs.slides)
for sh, idx in BTNS:
    sh.click_action.target_slide = slides[idx]
prs.save(OUT)
print("saved", OUT)
