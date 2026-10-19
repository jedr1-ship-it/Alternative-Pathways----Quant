"""Two appendix slides on sample sizes, in a consistent universe
(adults 18+, the analysis universe).
Slide 1: survey by survey — March supplement (ASEC) adults, teachers,
and the combined adult interviews of that year's twelve basic monthly
files (cached from 2005).
Slide 2: month by month for 2006 / 2015 / 2024, March and the ASEC row
in bold. The ASEC contains the March basic respondents plus the
February-April oversample households, about 1.45x a single March.
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
monthly, pers = {}, {}
for f in sorted(glob.glob("data/interim/cps_*.parquet")):
    y, m = (int(g) for g in re.search(r"cps_(\d{4})(\d{2})", f).groups())
    monthly.setdefault(y, {})[m] = len(pd.read_parquet(f, columns=["HRMIS"]))
    pers.setdefault(y, []).append(pd.read_parquet(
        f, columns=["HRHHID", "HRHHID2", "PULINENO"]).drop_duplicates())
# distinct adults seen across the year's monthly files (each is
# interviewed about three times within a calendar year)
upers = {y: len(pd.concat(ps).drop_duplicates()) for y, ps in pers.items()}
interviews = {y: sum(ms.values()) for y, ms in monthly.items()}
nmonths = {y: len(ms) for y, ms in monthly.items()}

mast = pd.read_parquet("data/processed/asec_master.parquet",
                       columns=["asec_year", "A_AGE", "teacher"])
mast["teacher"] = pd.to_numeric(mast.teacher, errors="coerce")
allpersons = len(mast)
A = mast[mast.A_AGE >= 18].groupby("asec_year").agg(
    adults=("A_AGE", "size"), teachers=("teacher", "sum"))
tot_ad, tot_te = int(A.adults.sum()), int(A.teachers.sum())
print("adults", tot_ad, "teachers", tot_te)
print("distinct persons by year:", {y: upers[y] for y in sorted(upers)})

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

# ---------------- slide 1: survey by survey ----------------
s1 = new_slide("The sample, survey by survey")
years = list(A.index)
half = (len(years) + 1) // 2
RH = 0.272
# per block: survey, ASEC adults, teachers, all 12 months
CW = [(0.00, 0.78), (0.78, 1.28), (2.06, 1.00), (3.06, 1.44)]
BW = 4.60

def cell(s, bx, y, col, t, bold=False, color=INK, size=12):
    x0, w = CW[col]
    text(s, bx + x0, y, w, t, size=size, bold=bold, color=color,
         align=PP_ALIGN.LEFT if col == 0 else PP_ALIGN.RIGHT)

for bi, block in enumerate([years[:half], years[half:]]):
    bx = 0.75 + bi * 6.45
    y = 1.42
    rule(s1, bx, y - 0.05, BW)
    cell(s1, bx, y, 0, "Survey", True)
    cell(s1, bx, y, 1, "March suppl.", True)
    cell(s1, bx, y, 2, "Teachers", True)
    cell(s1, bx, y, 3, "All 12 months", True)
    rule(s1, bx, y + 0.26, BW)
    y += 0.33
    for yr in block:
        ad, te = int(A.loc[yr, "adults"]), int(A.loc[yr, "teachers"])
        if yr in upers:
            am = f"{upers[yr]:,}" + ("" if nmonths[yr] == 12 else "*")
        else:
            am = "–"
        cell(s1, bx, y, 0, str(yr))
        cell(s1, bx, y, 1, f"{ad:,}")
        cell(s1, bx, y, 2, f"{te:,}")
        cell(s1, bx, y, 3, am)
        y += RH
    rule(s1, bx, y + 0.02, BW)
ytot = 1.42 + 0.33 + half * RH + 0.10
text(s1, 0.75 + 6.45, ytot, 6.0,
     f"Total (ASEC)   {tot_ad:,} adults, {tot_te:,} teachers",
     size=12.5, bold=True, color=NAVY)
text(s1, 0.75, ytot, 5.9,
     "Distinct adults (18+) in both columns. The supplement interviews "
     "each person once; the basic survey interviews each adult about "
     "three times a year (0.9–1.2 million interviews), so we keep "
     "about one person in three and one interview in eight (monthly "
     "files cached from 2005; * 2025: eleven months).",
     size=10.5, color=MUT)
# entry button to copy into the main deck, plus navigation
button(s1, 10.35, 0.30, "sample sizes", 0)
text(s1, 10.35, 0.74, 2.6, "(copy this button to the main deck)",
     size=9.5, color=MUT)
button(s1, 0.75, 6.92, "monthly samples", 1)
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
x0, wlab = 0.55, 1.30
wn, wb, wr, gap = 0.80, 0.95, 0.95, 0.34
BW2 = wn + wb + wr
y = 1.30
TW = wlab + 3 * (BW2 + gap) - gap
rule(s2, x0, y - 0.05, TW)
for i, yr in enumerate(SHOW):
    bx = x0 + wlab + i * (BW2 + gap)
    text(s2, bx, y, BW2, str(yr), size=12.5, bold=True,
         align=PP_ALIGN.CENTER)
    text(s2, bx, y + 0.28, wn, "New", size=10, bold=True,
         align=PP_ALIGN.RIGHT, color=MUT)
    text(s2, bx + wn, y + 0.28, wb, "From last\nyear", size=10,
         bold=True, align=PP_ALIGN.RIGHT, color=MUT)
    text(s2, bx + wn + wb, y + 0.28, wr, "From this\nyear", size=10,
         bold=True, align=PP_ALIGN.RIGHT, color=MUT)
rule(s2, x0, y + 0.78, TW)
y += 0.86
for mi, mname in enumerate(MON):
    bold = (mname == "March")
    c = NAVY if bold else INK
    text(s2, x0, y, wlab, mname, size=10.5, bold=bold, color=c)
    for i, yr in enumerate(SHOW):
        bx = x0 + wlab + i * (BW2 + gap)
        for j, v in enumerate(newrep[yr][mi]):
            text(s2, bx + [0, wn, wn + wb][j], y, [wn, wb, wr][j],
                 f"{v:,}", size=10.5, bold=bold, color=c,
                 align=PP_ALIGN.RIGHT)
    y += 0.238
rule(s2, x0, y + 0.02, TW)
y += 0.08
text(s2, x0, y, wlab, "Sum", size=10.5, bold=True)
for i, yr in enumerate(SHOW):
    bx = x0 + wlab + i * (BW2 + gap)
    for j in range(3):
        text(s2, bx + [0, wn, wn + wb][j], y, [wn, wb, wr][j],
             f"{sum(r[j] for r in newrep[yr]):,}", size=10.5, bold=True,
             align=PP_ALIGN.RIGHT)
y += 0.26
text(s2, x0, y, wlab + 2.2, "Distinct persons (new + from last year)",
     size=10.5, bold=True)
for i, yr in enumerate(SHOW):
    bx = x0 + wlab + i * (BW2 + gap)
    text(s2, bx, y, BW2, f"{upers[yr]:,}", size=10.5, bold=True,
         align=PP_ALIGN.RIGHT)
y += 0.26
text(s2, x0, y, wlab + 2.2, "March supplement (ASEC)", size=10.5,
     bold=True, color=NAVY)
for i, yr in enumerate(SHOW):
    bx = x0 + wlab + i * (BW2 + gap)
    text(s2, bx, y, BW2, f"{int(A.loc[yr, 'adults']):,}", size=10.5,
         bold=True, color=NAVY, align=PP_ALIGN.RIGHT)
rule(s2, x0, y + 0.26, TW)
text(s2, x0, y + 0.40, 12.0,
     "Adults (18+). New: first interview ever. From last year: back "
     "after being interviewed the previous year (first time this year). "
     "From this year: already interviewed in an earlier month of the "
     "year. Each distinct person is counted once in New or From last "
     "year, so those two sums give the year's distinct persons; adding "
     "the From-this-year repeats gives the interviews. The ASEC "
     "interviews each person once: the March respondents plus the "
     "February–April oversamples, 1.45× a single March.",
     size=9.5, color=MUT)
button(s2, 11.45, 6.92, "back", 0)

slides = list(prs.slides)
for sh, idx in BTNS:
    sh.click_action.target_slide = slides[idx]
prs.save(OUT)
print("saved", OUT)
