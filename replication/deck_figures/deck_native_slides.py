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
HEAD = RGBColor(0x26, 0x45, 0x6E)
BAND = RGBColor(0x00, 0x54, 0x9F)
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

def top_band(s):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(-0.03),
                            Inches(13.34), Inches(0.65))
    sh.fill.solid(); sh.fill.fore_color.rgb = BAND
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh

def heading(s, text, y, size=28):
    box = s.shapes.add_textbox(Inches(0.75), Inches(y), Inches(10.8), Inches(0.6))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = text
    r.font.name = GARA; r.font.size = Pt(size); r.font.bold = True
    r.font.color.rgb = HEAD
    return box

def house_slide(title):
    """The deck's own text-slide pattern: blue top band, navy Garamond heading."""
    s = new_slide()
    top_band(s)
    heading(s, title, 0.95)
    return s

BODY_X, BODY_Y, BODY_W = 0.85, 1.85, 11.7
made = {}

# ---------------- dividers ----------------
for tag, num, title in [("d1", "1", "Data and measurement"),
                        ("d2", "2", "The leaving rate"),
                        ("d3", "3", "Where they go"),
                        ("d4", "4", "Who leaves, and why"),
                        ("d5", "5", "The business cycle"),
                        ("d6", "6", "Pay and pensions")]:
    s = new_slide()
    top_band(s)
    add_text(s, 1.9, 0.95, 9.53, 3.2, [(num, 170, PALEBG, True, False, 0)],
             align=PP_ALIGN.CENTER)
    add_text(s, 1.9, 4.25, 9.53, 0.75, [(title, 30, HEAD, True, False, 0)],
             align=PP_ALIGN.CENTER)
    rule(s, 5.87, 5.25, 1.6, 1.6, BAND)
    made[tag] = s

# ---------------- The Current Population Survey ----------------
s = house_slide("The Current Population Survey")
add_text(s, BODY_X, BODY_Y, BODY_W, 0.8, align=PP_ALIGN.JUSTIFY, parts=[
 ("The monthly household survey behind the official employment statistics: some 110,000 "
  "persons each month. Every March, a supplement asks about the previous calendar year.",
  16, INK, False, False, 0),
])
# persons and teachers in every March supplement (counts from asec_master.parquet)
SUPP = [(1998, "131,617", "2,620"), (1999, "132,324", "2,719"),
        (2000, "133,710", "2,743"), (2001, "128,821", "2,646"),
        (2002, "217,219", "4,632"), (2003, "216,424", "4,201"),
        (2004, "213,241", "4,344"), (2005, "210,648", "4,361"),
        (2006, "208,562", "4,161"), (2007, "206,639", "4,336"),
        (2008, "206,404", "4,357"), (2009, "207,921", "4,448"),
        (2010, "209,802", "4,357"), (2011, "204,983", "4,301"),
        (2012, "201,398", "4,184"), (2013, "202,634", "4,192"),
        (2014, "139,415", "2,896"), (2015, "199,024", "4,333"),
        (2016, "185,487", "3,972"), (2017, "185,914", "4,045"),
        (2018, "180,084", "4,053"), (2019, "180,101", "3,986"),
        (2020, "157,959", "3,321"), (2021, "163,543", "3,232"),
        (2022, "152,732", "3,040"), (2023, "146,133", "3,141"),
        (2024, "144,265", "3,006"), (2025, "142,125", "2,918")]
BL, BR = 1.05, 7.00           # left edge of each block
def srow(bx, yy, yr, pv, tv, bold=False, sz=11.5):
    add_text(s, bx, yy, 0.9, 0.3, [(str(yr), sz, INK, bold, False, 0)])
    add_text(s, bx + 0.90, yy, 1.75, 0.3, [(pv, sz, INK, bold, False, 0)],
             align=PP_ALIGN.RIGHT)
    add_text(s, bx + 2.75, yy, 1.60, 0.3, [(tv, sz, INK, bold, False, 0)],
             align=PP_ALIGN.RIGHT)
rule(s, 0.9, 2.62, 11.53, 1.6, INK)
for bx in (BL, BR):
    add_text(s, bx, 2.72, 1.8, 0.3, [("Supplement", 12, INK, True, False, 0)])
    add_text(s, bx + 0.90, 2.72, 1.75, 0.3, [("Persons", 12, INK, True, False, 0)],
             align=PP_ALIGN.RIGHT)
    add_text(s, bx + 2.75, 2.72, 1.60, 0.3, [("Teachers", 12, INK, True, False, 0)],
             align=PP_ALIGN.RIGHT)
rule(s, 0.9, 3.08, 11.53, 0.8, INK)
y = 3.18
for i, (yr, pv, tv) in enumerate(SUPP):
    bx = BL if i < 14 else BR
    yy = y + (i % 14) * 0.26
    srow(bx, yy, yr, pv, tv)
yend = y + 14 * 0.26
rule(s, 0.9, yend + 0.02, 11.53, 0.8, INK)
add_text(s, BL, yend + 0.10, 4.5, 0.3,
         [("All supplements, 1998–2025", 12, INK, True, False, 0)])
srow(BR, yend + 0.10, "", "5,009,129", "104,545", bold=True, sz=12)
rule(s, 0.9, yend + 0.44, 11.53, 1.6, INK)
made["cps"] = s

# ---------------- Supplements and the March interview ----------------
s = house_slide("The March supplement")
add_text(s, BODY_X, BODY_Y, BODY_W, 5.0, align=PP_ALIGN.JUSTIFY, parts=[
 ("The basic monthly interview measures current activity only. Most months add a supplement "
  "on a rotating topic.", 17, INK, False, False, 16),
 ("The March supplement expands the sample to roughly 90,000 households and asks every adult "
  "about the entire previous calendar year: longest job held, weeks worked, earnings.",
  17, INK, False, False, 16),
 ("I pool every March supplement from 1998 to 2025: five million records, 104,545 of them "
  "teachers.", 17, INK, False, False, 16),
 ("Whoever taught as last year’s longest job, and no longer teaches at the March interview, "
  "has left the profession within the year.", 17, INK, False, False, 0),
])
made["asec"] = s

# ---------------- Linking individuals across waves ----------------
s = house_slide("Linking individuals across waves")
add_text(s, BODY_X, BODY_Y, BODY_W, 0.8, [
 ("The CPS carries no individual identifier: records are linked on household identifiers and "
  "validated on demographics (Madrian and Lefgren, 1999).",
  17, INK, False, False, 0)], align=PP_ALIGN.JUSTIFY)
rule(s, 0.9, 3.05, 11.53, 1.0, INK)
add_text(s, 1.1, 3.25, 4.6, 0.4, [("Linkage keys (exact match)", 14, HEAD, True, False, 0)])
add_text(s, 6.6, 3.25, 5.4, 0.4, [("Validation", 14, HEAD, True, False, 0)])
add_text(s, 1.1, 3.78, 4.6, 1.6, [
 ("Household identifier", 13, INK, False, False, 8),
 ("Dwelling identifier", 13, INK, False, False, 8),
 ("Person line number", 13, INK, False, False, 0)])
add_text(s, 6.6, 3.78, 5.4, 1.6, [
 ("Sex, identical", 13, INK, False, False, 8),
 ("Race, identical", 13, INK, False, False, 8),
 ("Age, increasing by zero to two years", 13, INK, False, False, 0)])
rule(s, 0.9, 5.5, 11.53, 1.0, INK)
add_text(s, BODY_X, 5.8, BODY_W, 0.6, [
 ("Validated links: 78 percent of teacher observations.",
  13.5, INK, False, False, 0)], align=PP_ALIGN.JUSTIFY)
made["words"] = s

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

# ---------------- How the CPS follows a household ----------------
s = house_slide("How the CPS follows a household")
add_text(s, BODY_X, BODY_Y, BODY_W, 1.1, align=PP_ALIGN.JUSTIFY, parts=[
 ("Households enter the survey on a fixed rotation: interviewed in four consecutive months, "
  "out for eight, back for four more. Eight interviews over sixteen months.",
  17, INK, False, False, 0),
])
scw = 11.53 / 16
add_text(s, 0.9, 3.30, 3.5, 0.35, [("Year 1: interviews 1–4", 14, NAVY2, True, False, 0)])
add_text(s, 4.9, 3.30, 3.6, 0.35, [("8 months out of the sample", 13, MUT, False, True, 0)],
         align=PP_ALIGN.CENTER)
add_text(s, 9.0, 3.30, 3.5, 0.35, [("Year 2: interviews 5–8", 14, BURG, True, False, 0)],
         align=PP_ALIGN.RIGHT)
for i in range(16):
    x0 = 0.9 + i * scw
    if i < 4:
        cell(s, x0, 3.72, scw, 0.62, NAVY2, None, str(i + 1))
    elif i >= 12:
        cell(s, x0, 3.72, scw, 0.62, BURG, None, str(i + 1))
    else:
        cell(s, x0, 3.72, scw, 0.62, None, LGRAYB, str(i + 1), MUT)
add_text(s, BODY_X, 4.90, BODY_W, 1.2, align=PP_ALIGN.JUSTIFY, parts=[
 ("Interviews 1–4 and 5–8 fall exactly twelve months apart: whoever is observed in year 1 "
  "can be observed again one year later.", 17, INK, False, False, 0),
])
made["rotation"] = s

# ---------------- The panel definition + alternative measures ----------------
# Beamer-style overlays: the slide is repeated, first with the plain strip,
# then with each illustrative case painted over it. Advancing the deck in
# presentation mode paints and unpaints the cases, one verdict at a time.
from pptx.enum.text import MSO_ANCHOR

CASES = [([0, 1, 2, 3, 15], "stayer", NAVY2),
         ([0, 1], "leaver", BURG),
         ([0], "not a teacher", MUT)]

def defs_slide(case=None):
    s = house_slide("Measuring attrition: definitions")
    add_text(s, 0.9, 1.55, 3.5, 0.35, [("Year 1: interviews 1–4", 13, NAVY2, True, False, 0)])
    if case is None:
        add_text(s, 4.9, 1.55, 3.6, 0.35,
                 [("8 months out of the sample", 12.5, MUT, False, True, 0)],
                 align=PP_ALIGN.CENTER)
    else:
        add_text(s, 4.9, 1.55, 3.6, 0.35,
                 [(CASES[case][1], 14, CASES[case][2], True, False, 0)],
                 align=PP_ALIGN.CENTER)
    add_text(s, 9.0, 1.55, 3.5, 0.35, [("Year 2: interviews 5–8", 13, BURG, True, False, 0)],
             align=PP_ALIGN.RIGHT)
    scw = 11.53 / 16
    painted = set() if case is None else set(CASES[case][0])
    for i in range(16):
        x0 = 0.9 + i * scw
        if i in painted:
            cell(s, x0, 1.92, scw, 0.50, NAVY2 if i < 4 else BURG, None, "T")
        elif i < 4:
            cell(s, x0, 1.92, scw, 0.50, NAVY2, None, str(i + 1))
        elif i >= 12:
            cell(s, x0, 1.92, scw, 0.50, BURG, None, str(i + 1))
        else:
            cell(s, x0, 1.92, scw, 0.50, None, LGRAYB, str(i + 1), MUT)
    # Definition 1 block
    add_text(s, 0.9, 2.56, 5.0, 0.4, [("The panel measure  (benchmark)", 15, HEAD, True, False, 0)])
    rule(s, 0.9, 3.00, 11.53, 1.0, INK)
    D1 = [("Teacher", NAVY2, "teaching, with a bachelor’s degree, in at least two year-1 interviews"),
          ("Stayer", NAVY2, "teaching in at least one year-2 interview"),
          ("Leaver", BURG, "never teaching in year 2, given two or more interviews, one outside the summer")]
    y = 3.14
    for term, c, desc in D1:
        add_text(s, 1.1, y, 1.6, 0.42, [(term, 13, c, True, False, 0)])
        add_text(s, 2.9, y, 9.3, 0.42, [(desc, 13, INK, False, False, 0)])
        y += 0.44
    rule(s, 0.9, y + 0.05, 11.53, 1.0, INK)
    # Alternative measures block
    add_text(s, 0.9, y + 0.10, 6.0, 0.4, [("Alternative measures", 15, HEAD, True, False, 0)])
    add_text(s, 11.0, y + 0.10, 1.4, 0.4, [("2021", 13, INK, True, False, 0)])
    rule(s, 0.9, y + 0.52, 11.53, 0.6, INK)
    ALT = [
     ("Panel measure", "12.9"),
     ("Annual recall", "7.1"),
     ("Occupation pair", "5.0"),
     ("Month pairs", "16.0"),
     ("Any sighting", "19.4"),
     ("NCES follow-up survey", "8.0"),
    ]
    y2 = y + 0.64
    for name, rate in ALT:
        add_text(s, 1.1, y2, 6.0, 0.36, [(name, 12, INK, False, False, 0)])
        add_text(s, 11.0, y2, 1.2, 0.36, [(rate, 12, INK, True, False, 0)])
        y2 += 0.36
    rule(s, 0.9, y2 + 0.02, 11.53, 1.0, INK)
    return s

made["table"] = defs_slide(None)
made["case0"] = defs_slide(0)
made["case1"] = defs_slide(1)
made["case2"] = defs_slide(2)

# ---------------- all series, one axis (image) ----------------
s = house_slide("All the series, one axis")
s.shapes.add_picture(f"{SC}/v_allseries.png", Inches(0.65), Inches(1.62),
                     width=Inches(12.05))
made["chart"] = s

# ---------------- countries ----------------
s = house_slide("Where this could be done next")
add_text(s, BODY_X, 1.62, BODY_W, 0.4,
         [("Labour force surveys with the sample, the access, and a design that sees the same person twelve months apart",
           13, MUT, False, True, 0)])
CC = [0.9, 2.7, 6.6, 9.4]
yh = 2.2
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
order_tags = [0, 1, "d1", "cps", "rotation", "asec", 3, "words",
              "table", "case0", "case1", "case2", "chart",
              "d2", 4, 5, 6, 7, 8, 9,
              "d3", 10, 11, 12, 13,
              "d4", 14, 15, 16, 17, 18,
              "d5", 19, 20,
              "d6", 21, 22, 23, 24, 25, 26,
              "countries"]
NEWTAGS = ["d1", "d2", "d3", "d4", "d5", "d6", "cps", "asec", "words",
           "rotation", "table", "case0", "case1", "case2", "chart", "countries"]
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
