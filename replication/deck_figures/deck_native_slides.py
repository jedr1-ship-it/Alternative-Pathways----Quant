"""Rebuild the deck with fully NATIVE, editable slides in Garamond:
six section dividers, CPS, words, stayer examples, series table, stacked
native chart (with the full NCES series), countries. Reorders everything."""
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.oxml.ns import qn
from lxml import etree

SC = "/tmp/claude-0/-home-user-Alternative-Pathways----Quant/37b5ad96-b2b0-50d1-9e4b-6301ff28b789/scratchpad"
GARA = "Garamond"
NAVY = RGBColor(0x1F, 0x4E, 0x79)
CORAL = RGBColor(0xB5, 0x44, 0x3C)
CORAL_L = RGBColor(0xD9, 0x9A, 0x94)
CORAL_M = RGBColor(0xC9, 0x72, 0x6A)
INK = RGBColor(0x1A, 0x24, 0x30)
MUT = RGBColor(0x55, 0x60, 0x6B)
PALE = RGBColor(0xE3, 0xE6, 0xEA)
GRAYC = RGBColor(0x8A, 0x90, 0x96)

# NCES TFS public-school leaver series, base school year -> percent
NCES = {1988: 5.6, 1991: 5.1, 1994: 6.6, 2000: 7.4, 2004: 8.4,
        2008: 8.0, 2012: 7.7, 2021: 8.0}

prs = Presentation(f"{SC}/deck.pptx")
W, H = prs.slide_width, prs.slide_height
blank = min(prs.slide_layouts, key=lambda l: len(l.placeholders))

def new_slide():
    s = prs.slides.add_slide(blank)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    return s

def tb(s, x, y, w, h, text, size=12, color=INK, bold=False, italic=False,
       align=PP_ALIGN.LEFT, spacing=1.0):
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        r = p.add_run()
        r.text = ln
        f = r.font
        f.name = GARA; f.size = Pt(size); f.bold = bold; f.italic = italic
        f.color.rgb = color
    return box

def rule(s, x, y, w, weight=1.0, color=INK):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                Inches(x + w), Inches(y))
    ln.line.color.rgb = color
    ln.line.width = Pt(weight)
    return ln

def chip(s, x, y, w, h, fill, line_color=None, radius=0.12):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(h))
    try:
        sh.adjustments[0] = radius
    except Exception:
        pass
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color; sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    return sh

made = {}

# ---------- dividers ----------
PALEBG = RGBColor(0xEC, 0xF0, 0xF4)
for tag, num, title in [("d1", "1", "Data and measurement"),
                        ("d2", "2", "The leaving rate"),
                        ("d3", "3", "Where they go"),
                        ("d4", "4", "Who leaves, and why"),
                        ("d5", "5", "The business cycle"),
                        ("d6", "6", "Pay and pensions")]:
    s = new_slide()
    tb(s, 1.9, 0.75, 9.53, 3.2, num, size=170, color=PALEBG, bold=True,
       align=PP_ALIGN.CENTER)
    tb(s, 1.9, 4.05, 9.53, 0.75, title, size=30, color=INK, bold=True,
       align=PP_ALIGN.CENTER)
    rule(s, 5.87, 5.05, 1.6, 1.6, NAVY)
    made[tag] = s

# ---------- CPS ----------
s = new_slide()
tb(s, 0.9, 0.55, 11.5, 0.6, "The Current Population Survey", size=26, bold=True)
rule(s, 0.9, 1.35, 11.53, 1.0)
paras = [
 "The CPS is the monthly household survey of the United States, run by the Census Bureau for the Bureau of Labor Statistics. The country’s official employment figures are computed from it.",
 "Each March, its Annual Social and Economic Supplement asks every adult about the previous calendar year: the longest job held, weeks worked, earnings, and benefits.",
 "That recall question is the measurement device of this paper. Whoever reports teaching as last year’s longest job, and no longer teaches at the March interview, has left the profession within the year.",
 "Households are interviewed on a fixed rotation, four months in, eight out, four in, so the same person can also be found one year later. That is the basis of the panel measures discussed next.",
]
y = 1.75
for p in paras:
    tb(s, 0.9, y, 11.5, 0.9, p, size=14, spacing=1.25)
    y += 1.08
tb(s, 0.9, y + 0.15, 11.5, 0.5,
   "Pooled here: 28 consecutive supplements, five million records, 104,545 teachers.",
   size=14, color=NAVY, bold=True)
made["cps"] = s

# ---------- words ----------
s = new_slide()
tb(s, 0.9, 0.55, 11.5, 0.6, "Two ways to measure leaving", size=26, bold=True)
rule(s, 0.9, 1.35, 11.53, 1.0)
tb(s, 0.9, 2.3, 11.0, 1.0,
   "Ask people what they did last year, and look at what they do today.",
   size=20, spacing=1.2)
tb(s, 0.9, 3.05, 11.0, 0.5, "One question, one record, no matching. This is the March measure.",
   size=13, color=MUT, italic=True)
tb(s, 0.9, 4.1, 11.0, 1.0,
   "Or find the same person twice, a year apart, and compare.",
   size=20, spacing=1.2)
tb(s, 0.9, 4.85, 11.0, 0.5, "No person identifier exists, so the second look has to be constructed from household records.",
   size=13, color=MUT, italic=True)
tb(s, 0.9, 5.9, 11.3, 0.9,
   "Every attrition rate in the literature is one of these two, plus a choice of who counts as a teacher and how long you keep looking.",
   size=15, color=INK)
made["words"] = s

# ---------- examples (mega-minimal) ----------
s = new_slide()
tb(s, 0.9, 0.5, 11.5, 0.6, "Who is a stayer", size=26, bold=True)
T, NG, NO = "T", "n", "x"   # teaching / interviewed-not-teaching / not interviewed
ROWS = [
 (["T","T","T","T", "T","T","T","T"], "stayer", NAVY),
 (["T","T","T","T", "n","n","n","T"], "stayer", NAVY),
 (["T","T","n","n", "n","n","n","n"], "leaver", CORAL),
 (["T","n","n","n", "n","n","n","n"], "not counted", GRAYC),
]
cw, ch, gap = 0.62, 0.62, 0.10
y = 1.7
for cells, verdict, vc in ROWS:
    x = 0.9
    for i, cell in enumerate(cells):
        if i == 4:
            x += 0.9   # the eight-month gap
        fill = NAVY if cell == "T" else (PALE if cell == "n" else None)
        border = None if cell != "x" else GRAYC
        c = chip(s, x, y, cw, ch, fill, border)
        if cell == "T":
            tf = c.text_frame; tf.word_wrap = False
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            r = p.add_run(); r.text = "T"
            r.font.name = GARA; r.font.size = Pt(13); r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        x += cw + gap
    ch2 = chip(s, x + 0.5, y + 0.06, 2.2, 0.5, vc)
    tf = ch2.text_frame
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = verdict
    r.font.name = GARA; r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    y += 1.15
tb(s, 0.9, y + 0.1, 5.0, 0.4, "year one", size=12, color=MUT)
tb(s, 6.4, y + 0.1, 5.0, 0.4, "one year later", size=12, color=MUT)
tb(s, 0.9, y + 0.62, 11.5, 0.4,
   "Filled: seen teaching.  Light: interviewed, not teaching.  A single sighting does not make a teacher.",
   size=11, color=MUT, italic=True)
made["examples"] = s

# ---------- series table ----------
s = new_slide()
tb(s, 0.9, 0.55, 11.5, 0.6, "Five ways to count, one file", size=26, bold=True)
rule(s, 0.9, 1.42, 11.53, 1.2)
COLS = [0.9, 4.15, 5.85, 10.9]
tb(s, COLS[0], 1.55, 3.1, 0.4, "Measure", size=12.5, bold=True)
tb(s, COLS[1], 1.55, 1.6, 0.4, "Years", size=12.5, bold=True)
tb(s, COLS[2], 1.55, 4.9, 0.4, "In words", size=12.5, bold=True)
tb(s, COLS[3], 1.55, 1.5, 0.4, "Rate", size=12.5, bold=True)
rule(s, 0.9, 1.95, 11.53, 0.6)
TROWS = [
 ("March recall  (this paper)", "1997–2024", "the main job of last year was teaching, and it is gone by March", "8.6", NAVY),
 ("Pure occupation pair", "2021–2023", "last year’s and today’s occupation compared directly, nothing else", "5.8", NAVY),
 ("Panel, one verdict per teacher", "2005–2024", "seen teaching twice; never seen teaching again a year later", "13.0", CORAL),
 ("Panel, month pairs", "2005–2024", "every teaching month checked exactly twelve months later", "15.4", CORAL),
 ("Panel, any sighting", "2005–2024", "one teaching month is enough to enter the count", "18.2", CORAL),
 ("NCES follow-up survey", "1988–2022", "school rosters re-surveyed the following fall; eight waves", "8.0", MUT),
]
y = 2.18
for name, yrs, words, rate, c in TROWS:
    tb(s, COLS[0], y, 3.1, 0.7, name, size=12.5, bold=True, color=c)
    tb(s, COLS[1], y, 1.6, 0.7, yrs, size=12.5, color=MUT)
    tb(s, COLS[2], y, 4.9, 0.7, words, size=12.5)
    tb(s, COLS[3], y, 1.5, 0.7, rate, size=12.5, bold=True, color=c)
    y += 0.72
rule(s, 0.9, y + 0.05, 11.53, 1.2)
tb(s, 0.9, y + 0.3, 11.5, 0.5,
   "Same records throughout; only the definition changes. Rate: annual average over the years shown; for the NCES, the latest wave (2021–22).",
   size=11, color=MUT, italic=True)
made["table"] = s

# ---------- all-series slide (image; native charts choke this template) ----------
s = new_slide()
tb(s, 0.9, 0.4, 11.5, 0.6, "All the series, one axis", size=26, bold=True)
s.shapes.add_picture(f"{SC}/v_allseries.png", Inches(0.65), Inches(1.2),
                     width=Inches(12.05))
made["chart"] = s

# ---------- countries ----------
s = new_slide()
tb(s, 0.9, 0.5, 11.5, 0.6, "Where this could be done next", size=26, bold=True)
tb(s, 0.9, 1.12, 11.5, 0.4,
   "Labour force surveys with the sample, the access, and a design that sees the same person twelve months apart",
   size=12.5, color=MUT, italic=True)
CC = [0.9, 2.7, 6.6, 9.4]
rule(s, 0.9, 1.72, 11.53, 1.2)
for x, h in zip(CC, ["", "Instrument", "Twelve-month design", "Sample and access"]):
    tb(s, x, 1.82, 2.7, 0.35, h, size=11.5, bold=True)
rule(s, 0.9, 2.22, 11.53, 0.6)
CROWS = [
 ("Italy", "Rilevazione sulle Forze di Lavoro (Istat)", "official 12-month longitudinal files", "research files, quarterly since 2004"),
 ("Germany", "Mikrozensus (Destatis)", "2-(2)-2 scheme since 2020", "810,000 persons a year; RDC files"),
 ("United Kingdom", "Labour Force Survey (ONS)", "five waves; first and fifth a year apart", "100,000 persons a quarter; UK Data Service"),
 ("France", "Enquête emploi en continu (INSEE)", "six consecutive quarters", "80,000 dwellings a quarter; Progedo, CASD"),
 ("Spain", "Encuesta de Población Activa (INE)", "six-quarter rotation; public flow files", "60,000 dwellings a quarter; free download"),
 ("Brazil", "PNAD Contínua (IBGE)", "five quarterly visits", "210,000 households a quarter; fully public"),
 ("Mexico", "ENOE (INEGI)", "five-quarter rotation", "150,000 dwellings a quarter; fully public"),
]
y = 2.42
for co, inst, des, acc in CROWS:
    tb(s, CC[0], y, 1.75, 0.5, co, size=11.5, bold=True, color=NAVY)
    tb(s, CC[1], y, 3.8, 0.5, inst, size=11.5)
    tb(s, CC[2], y, 2.7, 0.5, des, size=11.5)
    tb(s, CC[3], y, 3.0, 0.5, acc, size=11.5)
    y += 0.52
rule(s, 0.9, y + 0.08, 11.53, 1.2)
tb(s, 0.9, y + 0.28, 11.5, 0.4,
   "At two to four percent of employment, each yields at least as many teacher observations per year as the CPS does here.",
   size=11.5)
tb(s, 0.9, y + 0.68, 11.5, 0.4,
   "Australia and Canada cannot: eight and six months in sample never show the same person twelve months apart.",
   size=10.5, color=MUT, italic=True)
made["countries"] = s

# ---------- reorder ----------
order_tags = [0, 1, "d1", "cps", 2, 3, "words", "examples", "table", "chart",
              "d2", 4, 5, 6, 7, 8, 9,
              "d3", 10, 11, 12, 13,
              "d4", 14, 15, 16, 17, 18,
              "d5", 19, 20,
              "d6", 21, 22, 23, 24, 25, 26,
              "countries"]
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
slide_id_of = {}
for i, el in enumerate(ids):
    slide_id_of[i] = el
new_ids = {tag: ids[27 + i] for i, tag in enumerate(
    ["d1", "d2", "d3", "d4", "d5", "d6", "cps", "words", "examples",
     "table", "chart", "countries"])}
for el in ids:
    sldIdLst.remove(el)
for t in order_tags:
    sldIdLst.append(new_ids[t] if isinstance(t, str) else slide_id_of[t])
prs.save(f"{SC}/deck_v3.pptx")
print(f"saved deck_v3.pptx with {len(order_tags)} slides")
