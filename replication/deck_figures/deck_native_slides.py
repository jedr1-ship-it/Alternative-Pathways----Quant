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
 ("The monthly household survey behind the official employment statistics: about 60,000 "
  "households, the civilian non-institutional population.", 17, INK, False, False, 0),
])
# descriptive statistics, weighted, computed from asec_master.parquet
DHDR = [("Teachers", 7.10, 2.00), ("Other graduates", 9.55, 2.55)]
DROWS = [
 ("Observations, 1998–2025", "85,497", "726,618"),
 ("Age", "43.7", "43.6"),
 ("Female, percent", "75.9", "46.5"),
 ("Master’s degree or higher, percent", "48.3", "33.8"),
 ("Public sector, percent", "72.9", "16.2"),
 ("Weeks worked in the year", "46.1", "48.6"),
 ("Median annual wage, 2021–2025", "$56,000", "$75,000"),
 ("Left teaching within the year, percent", "8.6", "—"),
]
rule(s, 0.9, 2.95, 11.53, 1.0, INK)
for h, x, w in DHDR:
    add_text(s, x, 3.08, w, 0.4, [(h, 13, HEAD, True, False, 0)], align=PP_ALIGN.RIGHT)
rule(s, 0.9, 3.50, 11.53, 0.6, INK)
y = 3.64
for lab, tv, gv in DROWS:
    add_text(s, 1.05, y, 5.6, 0.4, [(lab, 13, INK, False, False, 0)])
    add_text(s, DHDR[0][1], y, DHDR[0][2], 0.4, [(tv, 13, INK, False, False, 0)],
             align=PP_ALIGN.RIGHT)
    add_text(s, DHDR[1][1], y, DHDR[1][2], 0.4, [(gv, 13, INK, False, False, 0)],
             align=PP_ALIGN.RIGHT)
    y += 0.40
rule(s, 0.9, y + 0.02, 11.53, 1.0, INK)
add_text(s, 0.9, y + 0.20, 11.53, 0.4,
         [("March supplements 1998–2025, weighted; individuals holding a bachelor’s degree or more.",
           12, MUT, False, True, 0)])
made["cps"] = s

# ---------------- Supplements and the March interview ----------------
s = house_slide("Supplements, and why March")
add_text(s, BODY_X, BODY_Y, BODY_W, 4.0, align=PP_ALIGN.JUSTIFY, parts=[
 ("The basic monthly interview measures current activity only. Most months add a supplement "
  "on a rotating topic.", 17, INK, False, False, 16),
 ("The March supplement expands the sample to roughly 90,000 households and asks every adult "
  "about the entire previous calendar year: longest job held, weeks worked, earnings.",
  17, INK, False, False, 16),
 ("An annual leaving rate can therefore be measured in March, and in no other month.",
  17, INK, False, False, 0),
])
made["asec"] = s

# ---------------- From the CPS to a teacher dataset ----------------
s = house_slide("From the CPS to a teacher dataset")
add_text(s, BODY_X, BODY_Y, BODY_W, 3.2, align=PP_ALIGN.JUSTIFY, parts=[
 ("I pool every March supplement from 1998 to 2025: five million records, 104,545 of them "
  "teachers.", 17, INK, False, False, 16),
 ("Whoever taught as last year’s longest job, and no longer teaches at the March interview, "
  "has left the profession within the year.", 17, INK, False, False, 0),
])
made["dataset"] = s

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

# ---------------- The panel definition + alternative measures ----------------
s = house_slide("Measuring attrition: definitions")
# the 4-8-4 strip, square and contiguous
add_text(s, 0.9, 1.55, 3.5, 0.35, [("Year 1: interviews 1–4", 13, NAVY2, True, False, 0)])
add_text(s, 4.9, 1.55, 3.6, 0.35, [("8 months out of the sample", 12.5, MUT, False, True, 0)],
         align=PP_ALIGN.CENTER)
add_text(s, 9.0, 1.55, 3.5, 0.35, [("Year 2: interviews 5–8", 13, BURG, True, False, 0)],
         align=PP_ALIGN.RIGHT)
scw = 11.53 / 16
for i in range(16):
    x0 = 0.9 + i * scw
    if i < 4:
        cell(s, x0, 1.92, scw, 0.50, NAVY2, None, str(i + 1))
    elif i >= 12:
        cell(s, x0, 1.92, scw, 0.50, BURG, None, str(i + 1))
    else:
        cell(s, x0, 1.92, scw, 0.50, None, LGRAYB, str(i + 1), MUT)

# illustrative cases painted on the strip itself: on each click the previous
# case is unpainted and the next appears (T marks + verdict in the gap)
from pptx.enum.text import MSO_ANCHOR

def tcell(i):
    return cell(s, 0.9 + i * scw, 1.92, scw, 0.50, NAVY2 if i < 4 else BURG,
                None, "T")

def verdict_box(text, color):
    box = add_text(s, 0.9 + 4 * scw + 0.3, 1.94, 8 * scw - 0.6, 0.46,
                   [(text, 15, color, True, False, 0)], align=PP_ALIGN.CENTER)
    box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    return box

CASES = [([0, 1, 2, 3, 15], "stayer", NAVY2),
         ([0, 1], "leaver", BURG),
         ([0], "not a teacher", MUT)]
groups = []
for idxs, verdict, vc in CASES:
    shapes = [tcell(i) for i in idxs] + [verdict_box(verdict, vc)]
    groups.append([sh.shape_id for sh in shapes])

from lxml import etree
PNS = "http://schemas.openxmlformats.org/presentationml/2006/main"

def timing_xml(groups):
    nid = [2]
    def nx():
        nid[0] += 1
        return nid[0]
    def eff(spid, kind, node_type):
        val = "visible" if kind == "entr" else "hidden"
        return (f'<p:par><p:cTn id="{nx()}" presetID="1" presetClass="{kind}" '
                f'presetSubtype="0" fill="hold" grpId="0" nodeType="{node_type}">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                f'<p:set><p:cBhvr><p:cTn id="{nx()}" dur="1" fill="hold">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
                f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
                f'</p:cBhvr><p:to><p:strVal val="{val}"/></p:to></p:set>'
                f'</p:childTnLst></p:cTn></p:par>')
    clicks, prev = [], None
    for g in groups:
        effs, first = [], True
        if prev:
            for spid in prev:
                effs.append(eff(spid, "exit", "clickEffect" if first else "withEffect"))
                first = False
        for spid in g:
            effs.append(eff(spid, "entr", "clickEffect" if first else "withEffect"))
            first = False
        inner = "".join(effs)
        clicks.append(f'<p:par><p:cTn id="{nx()}" fill="hold"><p:stCondLst>'
                      f'<p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
                      f'<p:par><p:cTn id="{nx()}" fill="hold"><p:stCondLst>'
                      f'<p:cond delay="0"/></p:stCondLst><p:childTnLst>{inner}'
                      f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
        prev = g
    builds = "".join(f'<p:bldP spid="{spid}" grpId="0"/>'
                     for g in groups for spid in g)
    xml = (f'<p:timing xmlns:p="{PNS}"><p:tnLst><p:par>'
           f'<p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
           f'<p:childTnLst><p:seq concurrent="1" nextAc="seek">'
           f'<p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
           f'{"".join(clicks)}</p:childTnLst></p:cTn>'
           f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/>'
           f'</p:tgtEl></p:cond></p:prevCondLst>'
           f'<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/>'
           f'</p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn>'
           f'</p:par></p:tnLst><p:bldLst>{builds}</p:bldLst></p:timing>')
    return etree.fromstring(xml.encode())

s._element.append(timing_xml(groups))
# Definition 1 block
add_text(s, 0.9, 2.56, 4.0, 0.4, [("Definition 1  (benchmark)", 15, HEAD, True, False, 0)])
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
 ("Definition 1, as above", "12.9"),
 ("Retrospective annual measure", "7.1"),
 ("Occupation-pair measure", "5.0"),
 ("Month-pair measure", "16.0"),
 ("Any-sighting measure", "19.4"),
 ("NCES Teacher Follow-up Survey", "8.0"),
]
y2 = y + 0.64
for name, rate in ALT:
    add_text(s, 1.1, y2, 6.0, 0.36, [(name, 12, INK, False, False, 0)])
    add_text(s, 11.0, y2, 1.2, 0.36, [(rate, 12, INK, True, False, 0)])
    y2 += 0.36
rule(s, 0.9, y2 + 0.02, 11.53, 1.0, INK)
made["table"] = s

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
order_tags = [0, 1, "d1", "cps", "asec", "dataset", 3, "words", "table", "chart",
              "d2", 4, 5, 6, 7, 8, 9,
              "d3", 10, 11, 12, 13,
              "d4", 14, 15, 16, 17, 18,
              "d5", 19, 20,
              "d6", 21, 22, 23, 24, 25, 26,
              "countries"]
NEWTAGS = ["d1", "d2", "d3", "d4", "d5", "d6", "cps", "asec", "dataset", "words",
           "table", "chart", "countries"]
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
