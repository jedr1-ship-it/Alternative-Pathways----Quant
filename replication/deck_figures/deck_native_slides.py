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
for tag, num, title in [("d1", "1", "Data and measurement"),
                        ("d2", "2", "The leaving rate"),
                        ("d3", "3", "Where they go"),
                        ("d4", "4", "Who leaves, and why"),
                        ("d5", "5", "The business cycle"),
                        ("d6", "6", "Pay and pensions")]:
    s = new_slide()
    rule(s, 5.07, 3.05, 3.2, 0.75)
    tb(s, 5.07, 3.25, 3.2, 0.4, num, size=14, color=MUT, align=PP_ALIGN.CENTER)
    tb(s, 3.07, 3.62, 7.2, 0.6, title, size=26, color=INK, align=PP_ALIGN.CENTER)
    rule(s, 5.07, 4.42, 3.2, 0.75)
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
COLS = [0.9, 4.3, 10.9]
tb(s, COLS[0], 1.55, 3.3, 0.4, "Measure", size=12.5, bold=True)
tb(s, COLS[1], 1.55, 6.4, 0.4, "In words", size=12.5, bold=True)
tb(s, COLS[2], 1.55, 1.5, 0.4, "Rate", size=12.5, bold=True)
rule(s, 0.9, 1.95, 11.53, 0.6)
TROWS = [
 ("March recall  (this paper)", "the main job of last year was teaching, and it is gone by March", "8.6", NAVY),
 ("Pure occupation pair", "last year’s and today’s occupation compared directly, nothing else", "5.8", NAVY),
 ("Panel, one verdict per teacher", "seen teaching twice; never seen teaching again a year later", "13.0", CORAL),
 ("Panel, month pairs", "every teaching month checked exactly twelve months later", "15.4", CORAL),
 ("Panel, any sighting", "one teaching month is enough to enter the count", "18.2", CORAL),
 ("NCES follow-up survey", "school rosters re-surveyed the following fall; every four to five years", "5.1 – 8.4", MUT),
]
y = 2.18
for name, words, rate, c in TROWS:
    tb(s, COLS[0], y, 3.3, 0.7, name, size=12.5, bold=True, color=c)
    tb(s, COLS[1], y, 6.4, 0.7, words, size=12.5)
    tb(s, COLS[2], y, 1.5, 0.7, rate, size=12.5, bold=True, color=c)
    y += 0.72
rule(s, 0.9, y + 0.05, 11.53, 1.2)
tb(s, 0.9, y + 0.3, 11.5, 0.5,
   "Same records throughout; only the definition changes. Annual average, percent of teachers.",
   size=11, color=MUT, italic=True)
made["table"] = s

# ---------- stacked native chart ----------
P = pd.read_csv("outputs/p_series.csv")
E = pd.read_csv("outputs/evolution_by_year_gender.csv")
R3 = pd.read_csv("outputs/panel_person_r3.csv"); R3 = R3[R3.base_year <= 2024]
FN = pd.read_csv("outputs/panel_person_final.csv")
years = list(range(1988, 2025))
def series_map(df, ycol, vcol):
    m = dict(zip(df[ycol].astype(int), df[vcol]))
    return [round(float(m[y]), 2) if y in m else None for y in years]

cd = CategoryChartData()
cd.categories = [str(y) for y in years]
cd.add_series("March recall", series_map(P, "cal_year", "leaver_ba"))
cd.add_series("Panel, one verdict per teacher", series_map(FN, "base_year", "leaver_final"))
cd.add_series("Panel, month pairs", series_map(E, "base_year", "attr12_all"))
cd.add_series("Panel, any sighting", series_map(R3, "base_year", "leaver_r3"))
cd.add_series("NCES follow-up (public schools)",
              [NCES.get(y) for y in years])

s = new_slide()
tb(s, 0.9, 0.4, 11.5, 0.6, "All the series, one axis", size=26, bold=True)
gframe = s.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(0.7), Inches(1.15),
                            Inches(12.0), Inches(5.7), cd)
ch_ = gframe.chart
ch_.has_title = False
ch_.font.name = GARA
ch_.font.size = Pt(11)
ch_.has_legend = True
ch_.legend.position = XL_LEGEND_POSITION.BOTTOM
ch_.legend.include_in_layout = False
va = ch_.value_axis
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xEF, 0xF1, 0xF3)
va.maximum_scale = 22.0
va.minimum_scale = 0.0
ca = ch_.category_axis
ca.tick_labels.font.size = Pt(10)
styles = [(NAVY, 2.75, False), (CORAL, 2.5, False),
          (CORAL_M, 1.5, True), (CORAL_L, 1.5, False), (INK, 1.75, True)]
for ser, (col, wpt, dash) in zip(ch_.plots[0].series, styles):
    ser.smooth = False
    ln = ser.format.line
    ln.color.rgb = col
    ln.width = Pt(wpt)
    if dash:
        d = ln._get_or_add_ln()
        pd_ = d.makeelement(qn("a:prstDash"), {"val": "dash"})
        d.append(pd_)
# markers on the sparse NCES series + span blanks
nces_ser = ch_.plots[0].series[4]
serEl = nces_ser._element
marker = etree.SubElement(serEl, qn("c:marker"))
etree.SubElement(marker, qn("c:symbol")).set("val", "circle")
etree.SubElement(marker, qn("c:size")).set("val", "6")
spPr = serEl.find(qn("c:spPr"))
serEl.remove(marker)
spPr.addnext(marker)
chartEl = ch_._chartSpace.find(qn("c:chart"))
disp = etree.SubElement(chartEl, qn("c:dispBlanksAs"))
disp.set("val", "span")
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
