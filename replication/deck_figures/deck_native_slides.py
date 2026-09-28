"""Rebuild the deck: all new slides in the deck's own house format
(Garamond, blue title + blue rule, 16pt ink body). Drops the old Data slide
(content merged into two non-redundant slides). Table = one example year."""
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

SC = "/tmp/claude-0/-home-user-Alternative-Pathways----Quant/37b5ad96-b2b0-50d1-9e4b-6301ff28b789/scratchpad"
GARA = "Garamond"
BLUE = RGBColor(0x00, 0x54, 0x9F)          # the deck's own title blue
INK = RGBColor(0x1A, 0x24, 0x30)           # the deck's own body color
MUT = RGBColor(0x6B, 0x74, 0x80)
CORAL = RGBColor(0xB5, 0x44, 0x3C)
NAVY2 = RGBColor(0x1F, 0x38, 0x64)
BURG = RGBColor(0x7B, 0x25, 0x30)
LGRAYB = RGBColor(0xC9, 0xCF, 0xD6)
PALE = RGBColor(0xE3, 0xE6, 0xEA)
PALEBG = RGBColor(0xEC, 0xF0, 0xF4)
GRAYC = RGBColor(0x8A, 0x90, 0x96)

# 2021 example year (the recent year in which the measures align with the
# NCES wave); values from outputs/*.csv, base year 2021
Y21 = {"recall": "7.1", "pair": "5.0", "verdict": "12.9",
       "pairs": "16.0", "sighting": "19.4", "nces": "8.0"}
EAG = None   # filled when the Education at a Glance figure is verified

prs = Presentation(f"{SC}/deck.pptx")
W, H = prs.slide_width, prs.slide_height
blank = min(prs.slide_layouts, key=lambda l: len(l.placeholders))

def new_slide():
    s = prs.slides.add_slide(blank)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    return s

def add_text(s, x, y, w, h, parts=None, align=PP_ALIGN.LEFT):
    """parts: list of paragraphs; each is (text, size, color, bold, italic, space_after)."""
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, (text, size, color, bold, italic, after) in enumerate(parts):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = Pt(size * 1.5)
        p.space_after = Pt(after)
        r = p.add_run(); r.text = text
        f = r.font
        f.name = GARA; f.size = Pt(size); f.bold = bold; f.italic = italic
        f.color.rgb = color
    return box

def rule(s, x, y, w, weight=1.2, color=BLUE):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                Inches(x + w), Inches(y))
    ln.line.color.rgb = color
    ln.line.width = Pt(weight)
    return ln

def house_slide(title):
    """Title + blue rule, exactly the geometry of the deck's own text slides."""
    s = new_slide()
    box = s.shapes.add_textbox(Emu(822960), Emu(457200), Emu(10515600), Emu(502920))
    tf = box.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = title
    r.font.name = GARA; r.font.size = Pt(26); r.font.bold = True
    r.font.color.rgb = BLUE
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(822960), Emu(1024128),
                                Emu(822960 + 10543032), Emu(1024128))
    ln.line.color.rgb = BLUE
    ln.line.width = Pt(1.2)
    return s

BODY_X, BODY_Y, BODY_W = 0.9, 1.45, 11.53
made = {}

# ---------------- dividers ----------------
for tag, num, title in [("d1", "1", "Data and measurement"),
                        ("d2", "2", "The leaving rate"),
                        ("d3", "3", "Where they go"),
                        ("d4", "4", "Who leaves, and why"),
                        ("d5", "5", "The business cycle"),
                        ("d6", "6", "Pay and pensions")]:
    s = new_slide()
    add_text(s, 1.9, 0.75, 9.53, 3.2, [(num, 170, PALEBG, True, False, 0)],
             align=PP_ALIGN.CENTER)
    add_text(s, 1.9, 4.05, 9.53, 0.75, [(title, 30, INK, True, False, 0)],
             align=PP_ALIGN.CENTER)
    rule(s, 5.87, 5.05, 1.6, 1.6)
    made[tag] = s

# ---------------- The Current Population Survey ----------------
s = house_slide("The Current Population Survey")
add_text(s, BODY_X, BODY_Y, BODY_W, 4.8, align=PP_ALIGN.JUSTIFY, parts=[
 ("The CPS is the monthly household survey of the United States, run by the Census Bureau. "
  "The country’s official employment statistics are computed from it.", 16, INK, False, False, 14),
 ("Each March, its Annual Social and Economic Supplement asks every adult about the previous "
  "calendar year: the longest job held, weeks worked, earnings, and benefits.", 16, INK, False, False, 14),
 ("Households are interviewed on a fixed rotation, four months in, eight out, four in, "
  "so the same person can be found again exactly one year later.", 16, INK, False, False, 0),
])
made["cps"] = s

# ---------------- From the CPS to a teacher dataset ----------------
s = house_slide("From the CPS to a teacher dataset")
add_text(s, BODY_X, BODY_Y, BODY_W, 4.8, align=PP_ALIGN.JUSTIFY, parts=[
 ("I pool every March supplement from 1998 to 2025 into a single file: five million individual "
  "records, 104,545 of them teachers, around 3,700 per year.", 16, INK, False, False, 14),
 ("Whoever taught as last year’s longest job, and no longer teaches at the March interview, "
  "has left the profession within the year.", 16, INK, False, False, 14),
 ("Each record carries age, family structure, earnings, school sector, state, and pension "
  "coverage, so leaving can be related to what we observe about the teacher.", 16, INK, False, False, 0),
])
made["dataset"] = s

# ---------------- Linking individuals across waves ----------------
s = house_slide("Linking individuals across waves")
add_text(s, BODY_X, BODY_Y, BODY_W, 1.6, [
 ("The CPS carries no individual identifier across interviews: sampling follows addresses, not "
  "persons. Records are therefore linked across waves on household-level identifiers, and each "
  "candidate link is validated on demographic consistency, following Madrian and Lefgren (1999).",
  16, INK, False, False, 0)], align=PP_ALIGN.JUSTIFY)
rule(s, 0.9, 3.05, 11.53, 1.0, INK)
add_text(s, 1.1, 3.25, 4.6, 0.4, [("Linkage keys (exact match)", 13.5, NAVY2, True, False, 0)])
add_text(s, 6.6, 3.25, 5.4, 0.4, [("Validation (demographic consistency)", 13.5, NAVY2, True, False, 0)])
add_text(s, 1.1, 3.78, 4.6, 1.6, [
 ("Household identifier", 13, INK, False, False, 8),
 ("Dwelling identifier", 13, INK, False, False, 8),
 ("Person line number within the household", 13, INK, False, False, 0)])
add_text(s, 6.6, 3.78, 5.4, 1.6, [
 ("Sex, identical across interviews", 13, INK, False, False, 8),
 ("Race, identical across interviews", 13, INK, False, False, 8),
 ("Age, increasing by zero to two years", 13, INK, False, False, 0)])
rule(s, 0.9, 5.5, 11.53, 1.0, INK)
add_text(s, BODY_X, 5.85, BODY_W, 1.2, [
 ("Validated links are obtained for 78 percent of teacher observations (74 percent of other "
  "college graduates). The loss is concentrated among movers, whose exit propensity exceeds "
  "that of non-movers; panel-based estimates are therefore lower bounds on mobility-related exit.",
  13.5, INK, False, False, 0)], align=PP_ALIGN.JUSTIFY)
made["words"] = s

# ---------------- Definition 1: illustrative cases ----------------
s = house_slide("Definition 1: illustrative cases")
def cell(s, x, y, w, h, fill, border=None, label=None, lab_color=None):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(h))
    if fill is None:
        sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if border is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = border; sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    if label:
        tf = sh.text_frame; tf.word_wrap = False
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = label
        r.font.name = GARA; r.font.size = Pt(12); r.font.bold = True
        r.font.color.rgb = lab_color or RGBColor(0xFF, 0xFF, 0xFF)
    return sh

EROWS = [
 (["T","T","T","T", "T","T","T","T"], "stayer", NAVY2),
 (["T","T","T","T", "n","n","n","T"], "stayer", NAVY2),
 (["T","T","n","n", "n","n","n","n"], "leaver", BURG),
 (["T","n","n","n", "n","n","n","n"], "excluded: a single year-1 observation", MUT),
]
cw, chh, gap = 0.60, 0.60, 0.06
y = 1.85
for cells_, verdict, vc in EROWS:
    x0 = 0.9
    for i, c_ in enumerate(cells_):
        if i == 4:
            x0 += 0.85
        if c_ == "T":
            fill = NAVY2 if i < 4 else BURG
            cell(s, x0, y, cw, chh, fill, None, "T")
        else:
            cell(s, x0, y, cw, chh, None, LGRAYB)
        x0 += cw + gap
    add_text(s, x0 + 0.35, y + 0.12, 5.0, 0.45,
             [(verdict, 14, vc, True, False, 0)])
    y += 1.02
add_text(s, 0.9, y + 0.08, 5.0, 0.35, [("Year 1", 12, MUT, False, True, 0)])
add_text(s, 6.35, y + 0.08, 5.0, 0.35, [("Year 2", 12, MUT, False, True, 0)])
add_text(s, 0.9, y + 0.52, 11.5, 0.4,
         [("Filled cells denote interviews in which the individual is observed teaching; bordered cells, interviews without teaching.",
           12, MUT, False, True, 0)])
made["examples"] = s

# ---------------- The panel definition + alternative measures ----------------
s = house_slide("Measuring attrition: definitions")
# the 4-8-4 strip, square and contiguous
add_text(s, 0.9, 1.26, 3.5, 0.35, [("Year 1: interviews 1–4", 13, NAVY2, True, False, 0)])
add_text(s, 4.9, 1.26, 3.6, 0.35, [("8 months out of the sample", 12.5, MUT, False, True, 0)],
         align=PP_ALIGN.CENTER)
add_text(s, 9.0, 1.26, 3.5, 0.35, [("Year 2: interviews 5–8", 13, BURG, True, False, 0)],
         align=PP_ALIGN.RIGHT)
scw = 11.53 / 16
for i in range(16):
    x0 = 0.9 + i * scw
    if i < 4:
        cell(s, x0, 1.62, scw, 0.50, NAVY2, None, str(i + 1))
    elif i >= 12:
        cell(s, x0, 1.62, scw, 0.50, BURG, None, str(i + 1))
    else:
        cell(s, x0, 1.62, scw, 0.50, None, LGRAYB, str(i + 1), MUT)
# Definition 1 block
add_text(s, 0.9, 2.26, 4.0, 0.4, [("Definition 1  (benchmark)", 14, INK, True, False, 0)])
rule(s, 0.9, 2.70, 11.53, 1.0, INK)
D1 = [("Teacher", NAVY2, "employed with a teaching occupation, holding a bachelor’s degree, in at least two year-1 interviews"),
      ("Stayer", NAVY2, "observed teaching in at least one year-2 interview"),
      ("Leaver", BURG, "never observed teaching in year 2, given two or more year-2 interviews, one outside June–August")]
y = 2.84
for term, c, desc in D1:
    add_text(s, 1.1, y, 1.6, 0.42, [(term, 13, c, True, False, 0)])
    add_text(s, 2.9, y, 9.3, 0.42, [(desc, 13, INK, False, False, 0)])
    y += 0.44
rule(s, 0.9, y + 0.05, 11.53, 1.0, INK)
# Alternative measures block
add_text(s, 0.9, y + 0.14, 6.0, 0.4, [("Alternative measures", 14, INK, True, False, 0)])
add_text(s, 11.0, y + 0.14, 1.4, 0.4, [("2021", 13, INK, True, False, 0)])
rule(s, 0.9, y + 0.58, 11.53, 0.6, INK)
ALT = [
 ("Definition 1, as above", "one classification per individual", "12.9"),
 ("Retrospective annual measure", "longest job of the previous year no longer held at the March interview", "7.1"),
 ("Occupation-pair measure", "previous-year and current occupation codes compared directly", "5.0"),
 ("Month-pair measure", "each teaching month matched to its interview twelve months ahead", "16.0"),
 ("Any-sighting measure", "any individual observed teaching once in year 1 enters the denominator", "19.4"),
 ("NCES Teacher Follow-up Survey", "roster-based re-survey of a teacher sample; wave 2021–22", "8.0"),
]
y2 = y + 0.72
for name, desc, rate in ALT:
    add_text(s, 1.1, y2, 3.1, 0.36, [(name, 11.5, INK, True, False, 0)])
    add_text(s, 4.35, y2, 6.4, 0.36, [(desc, 11.5, INK, False, False, 0)])
    add_text(s, 11.0, y2, 1.2, 0.36, [(rate, 11.5, INK, True, False, 0)])
    y2 += 0.37
rule(s, 0.9, y2 + 0.02, 11.53, 1.0, INK)
made["table"] = s

# ---------------- all series, one axis (image) ----------------
s = house_slide("All the series, one axis")
s.shapes.add_picture(f"{SC}/v_allseries.png", Inches(0.65), Inches(1.35),
                     width=Inches(12.05))
made["chart"] = s

# ---------------- countries ----------------
s = house_slide("Where this could be done next")
add_text(s, BODY_X, 1.28, BODY_W, 0.4,
         [("Labour force surveys with the sample, the access, and a design that sees the same person twelve months apart",
           13, MUT, False, True, 0)])
CC = [0.9, 2.7, 6.6, 9.4]
yh = 1.95
for x, h, wdt in zip(CC, ["", "Instrument", "Twelve-month design", "Sample and access"],
                     [1.7, 3.8, 2.7, 3.0]):
    add_text(s, x, yh, wdt, 0.35, [(h, 12, INK, True, False, 0)])
rule(s, 0.9, yh + 0.4, 11.53, 0.6, INK)
CROWS = [
 ("Italy", "Rilevazione sulle Forze di Lavoro (Istat)", "official 12-month longitudinal files", "research files, quarterly since 2004"),
 ("Germany", "Mikrozensus (Destatis)", "2-(2)-2 scheme since 2020", "810,000 persons a year; RDC files"),
 ("United Kingdom", "Labour Force Survey (ONS)", "five waves; first and fifth a year apart", "100,000 persons a quarter; UK Data Service"),
 ("France", "Enquête emploi en continu (INSEE)", "six consecutive quarters", "80,000 dwellings a quarter; Progedo, CASD"),
 ("Spain", "Encuesta de Población Activa (INE)", "six-quarter rotation; public flow files", "60,000 dwellings a quarter; free download"),
 ("Brazil", "PNAD Contínua (IBGE)", "five quarterly visits", "210,000 households a quarter; fully public"),
 ("Mexico", "ENOE (INEGI)", "five-quarter rotation", "150,000 dwellings a quarter; fully public"),
]
y = yh + 0.55
for co, inst, des, acc in CROWS:
    add_text(s, CC[0], y, 1.7, 0.5, [(co, 12, INK, True, False, 0)])
    add_text(s, CC[1], y, 3.8, 0.5, [(inst, 12, INK, False, False, 0)])
    add_text(s, CC[2], y, 2.7, 0.5, [(des, 12, INK, False, False, 0)])
    add_text(s, CC[3], y, 3.0, 0.5, [(acc, 12, INK, False, False, 0)])
    y += 0.52
rule(s, 0.9, y + 0.06, 11.53, 1.2, INK)
add_text(s, 0.9, y + 0.24, 11.5, 0.4,
         [("Australia and Canada cannot: eight and six months in sample never show the same person twelve months apart.",
           11, MUT, False, True, 0)])
made["countries"] = s

# ---------------- reorder (original Data slide, index 2, is dropped) ----------------
order_tags = [0, 1, "d1", "cps", "dataset", 3, "words", "table", "examples", "chart",
              "d2", 4, 5, 6, 7, 8, 9,
              "d3", 10, 11, 12, 13,
              "d4", 14, 15, 16, 17, 18,
              "d5", 19, 20,
              "d6", 21, 22, 23, 24, 25, 26,
              "countries"]
NEWTAGS = ["d1", "d2", "d3", "d4", "d5", "d6", "cps", "dataset", "words",
           "examples", "table", "chart", "countries"]
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
new_ids = {tag: ids[27 + i] for i, tag in enumerate(NEWTAGS)}
for el in ids:
    sldIdLst.remove(el)
dropped = 0
for t in order_tags:
    sldIdLst.append(new_ids[t] if isinstance(t, str) else ids[t])
prs.save(f"{SC}/deck_v4.pptx")
print(f"saved deck_v4.pptx with {len(order_tags)} slides (EAG row: {EAG is not None})")
