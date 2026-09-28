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

def add_text(s, x, y, w, h, parts, align=PP_ALIGN.LEFT):
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
add_text(s, BODY_X, BODY_Y, BODY_W, 4.8, [
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
add_text(s, BODY_X, BODY_Y, BODY_W, 4.8, [
 ("I pool every March supplement from 1998 to 2025 into a single file: five million individual "
  "records, 104,545 of them teachers, around 3,700 per year.", 16, INK, False, False, 14),
 ("Whoever taught as last year’s longest job, and no longer teaches at the March interview, "
  "has left the profession within the year.", 16, INK, False, False, 14),
 ("Each record carries age, family structure, earnings, school sector, state, and pension "
  "coverage, so leaving can be related to what we observe about the teacher.", 16, INK, False, False, 0),
])
made["dataset"] = s

# ---------------- Two ways to measure leaving ----------------
s = house_slide("Two ways to measure leaving")
add_text(s, BODY_X, 2.1, 11.0, 4.0, [
 ("Ask people what they did last year, and look at what they do today.", 20, INK, False, False, 6),
 ("One question, one record, no matching. This is the March measure.", 13, MUT, False, True, 30),
 ("Or find the same person twice, a year apart, and compare.", 20, INK, False, False, 6),
 ("No person identifier exists, so the second look is built from household records.", 13, MUT, False, True, 0),
])
made["words"] = s

# ---------------- Who is a stayer ----------------
s = house_slide("Who is a stayer")
T, NG = "T", "n"
ROWS = [
 (["T","T","T","T", "T","T","T","T"], "stayer", BLUE),
 (["T","T","T","T", "n","n","n","T"], "stayer", BLUE),
 (["T","T","n","n", "n","n","n","n"], "leaver", CORAL),
 (["T","n","n","n", "n","n","n","n"], "not counted", GRAYC),
]
def chip(s, x, y, w, h, fill, label=None, lab_size=13):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(h))
    try:
        sh.adjustments[0] = 0.12
    except Exception:
        pass
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    if label:
        tf = sh.text_frame; tf.word_wrap = False
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = label
        r.font.name = GARA; r.font.size = Pt(lab_size); r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    return sh

cw, ch2, gap = 0.62, 0.62, 0.10
y = 1.75
for cells, verdict, vc in ROWS:
    x = 0.9
    for i, cell in enumerate(cells):
        if i == 4:
            x += 0.9
        chip(s, x, y, cw, ch2, BLUE if cell == "T" else PALE,
             "T" if cell == "T" else None)
        x += cw + gap
    chip(s, x + 0.5, y + 0.06, 2.2, 0.5, vc, verdict)
    y += 1.12
add_text(s, 0.9, y + 0.05, 5.0, 0.4, [("year one", 12, MUT, False, False, 0)])
add_text(s, 6.4, y + 0.05, 5.0, 0.4, [("one year later", 12, MUT, False, False, 0)])
add_text(s, 0.9, y + 0.5, 11.5, 0.4,
         [("Filled: seen teaching.  Light: interviewed, not teaching.", 11, MUT, False, True, 0)])
made["examples"] = s

# ---------------- the table: one example year ----------------
s = house_slide("Six measures, one year")
add_text(s, BODY_X, 1.28, BODY_W, 0.4,
         [("Percent of teachers leaving between 2021 and 2022", 13, MUT, False, True, 0)])
COLS = [0.9, 4.4, 10.9]
yh = 1.95
add_text(s, COLS[0], yh, 3.4, 0.4, [("Measure", 13, INK, True, False, 0)])
add_text(s, COLS[1], yh, 6.3, 0.4, [("In words", 13, INK, True, False, 0)])
add_text(s, COLS[2], yh, 1.5, 0.4, [("2021", 13, INK, True, False, 0)])
rule(s, 0.9, yh + 0.42, 11.53, 0.6, INK)
TROWS = [
 ("March recall  (this paper)", "the main job of last year was teaching, and it is gone by March", Y21["recall"]),
 ("Pure occupation pair", "last year’s and today’s occupation compared directly, nothing else", Y21["pair"]),
 ("Panel, one verdict per teacher", "seen teaching twice; never seen teaching again a year later", Y21["verdict"]),
 ("Panel, month pairs", "every teaching month checked exactly twelve months later", Y21["pairs"]),
 ("Panel, any sighting", "one teaching month is enough to enter the count", Y21["sighting"]),
 ("NCES follow-up survey", "school rosters re-surveyed the following fall", Y21["nces"]),
]
if EAG is not None:
    TROWS.append(("Education at a Glance 2025", EAG[0], EAG[1]))
y = yh + 0.58
for name, words, rate in TROWS:
    add_text(s, COLS[0], y, 3.4, 0.6, [(name, 13, INK, True, False, 0)])
    add_text(s, COLS[1], y, 6.3, 0.6, [(words, 13, INK, False, False, 0)])
    add_text(s, COLS[2], y, 1.5, 0.6, [(rate, 13, INK, True, False, 0)])
    y += 0.58
rule(s, 0.9, y + 0.05, 11.53, 1.2, INK)
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
order_tags = [0, 1, "d1", "cps", "dataset", 3, "words", "examples", "table", "chart",
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
