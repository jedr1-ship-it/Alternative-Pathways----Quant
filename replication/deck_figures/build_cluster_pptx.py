"""Native, fully editable PPTX of the Data Cluster deck, OECD-style.
Clean corporate look: Arial, dark-blue titles with a rule, large body
text that fills the slide, key-message bands, booktabs-style native
tables, working appendix buttons, and charts as 300-dpi images rendered
from the same PDFs the Beamer deck uses (report/data_cluster/_pngx).
Writes report/data_cluster/Proyect_US_cluster.pptx. Run from the repo
root after compiling the Beamer deck."""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

FIG = "report/data_cluster/_pngx"
OUT = "report/data_cluster/Proyect_US_cluster.pptx"
LOGO = "report/data_cluster/oecd_logo.png"
EQ_PNG = "report/data_cluster/equation3.png"

FONT = "Arial"
INK = RGBColor(0x21, 0x25, 0x29)
MUT = RGBColor(0x6B, 0x74, 0x80)
NAVY = RGBColor(0x10, 0x2D, 0x5E)     # OECD-style dark blue
ACC = RGBColor(0x2D, 0x6C, 0xB5)      # accent blue
BURG = RGBColor(0x8F, 0x2B, 0x36)
LGRAYB = RGBColor(0xC9, 0xCF, 0xD6)
BTNBG = RGBColor(0xE2, 0xEA, 0xF5)
BAND = RGBColor(0xEC, 0xF2, 0xF9)     # key-message band

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
PAGENO = [0]
REG = {}
BTNS = []
NOTES = {}

def new_slide(title=None, number=True, key=None):
    s = prs.slides.add_slide(blank)
    PAGENO[0] += 1
    if key:
        REG[key] = s
    if title:
        box = s.shapes.add_textbox(Inches(0.55), Inches(0.26), Inches(12.3),
                                   Inches(0.62))
        tf = box.text_frame; tf.word_wrap = True; tf.auto_size = None
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = title
        r.font.name = FONT; r.font.size = Pt(25); r.font.bold = True
        r.font.color.rgb = NAVY
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.55),
                                    Inches(1.02), Inches(12.78), Inches(1.02))
        ln.line.color.rgb = ACC; ln.line.width = Pt(2.2)
    if number:
        nb = s.shapes.add_textbox(Inches(12.45), Inches(7.05), Inches(0.7),
                                  Inches(0.32))
        tf = nb.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
        r = p.add_run(); r.text = str(PAGENO[0])
        r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = MUT
    return s

def add_text(s, x, y, w, h, parts, align=PP_ALIGN.LEFT, spacing=1.28):
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para in enumerate(parts):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if isinstance(para[0], list):
            p.space_after = Pt(para[1])
            for text, sz, color, bold, italic in para[0]:
                r = p.add_run(); r.text = text
                f = r.font
                f.name = FONT; f.size = Pt(sz); f.bold = bold
                f.italic = italic; f.color.rgb = color
            p.line_spacing = Pt(para[0][0][1] * spacing)
        else:
            text, size, color, bold, italic, after = para
            p.space_after = Pt(after)
            p.line_spacing = Pt(size * spacing)
            r = p.add_run(); r.text = text
            f = r.font
            f.name = FONT; f.size = Pt(size); f.bold = bold
            f.italic = italic; f.color.rgb = color
    return box

def message(s, text, y=6.14, size=15.5, lead="Key message."):
    band = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55),
                              Inches(y), Inches(12.23), Inches(0.72))
    band.fill.solid(); band.fill.fore_color.rgb = BAND
    band.line.fill.background(); band.shadow.inherit = False
    band.adjustments[0] = 0.12
    tf = band.text_frame; tf.word_wrap = True
    tf.margin_left = Inches(0.22); tf.margin_right = Inches(0.22)
    tf.margin_top = Inches(0.06); tf.margin_bottom = Inches(0.06)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = lead + "  "
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = True
    r.font.color.rgb = NAVY
    r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = False
    r.font.color.rgb = INK
    return band

def bullets(s, items, y=1.55, size=19, gap=22, x=0.9, w=11.8, numbered=False,
            marker_color=None):
    parts = []
    mc = marker_color or ACC
    for i, it in enumerate(items):
        after = gap if i < len(items) - 1 else 0
        marker = f"{i+1}.   " if numbered else "▪  "
        if isinstance(it, tuple):
            lead, rest = it
            parts.append([[(marker, size, mc, True, False),
                           (lead + "  ", size, NAVY, True, False),
                           (rest, size, INK, False, False)], after])
        else:
            parts.append([[(marker, size, mc, True, False),
                           (it, size, INK, False, False)], after])
    return add_text(s, x, y, w, 5.6, parts, spacing=1.28)

def rule(s, x, y, w, weight=1.0, color=INK):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                Inches(x + w), Inches(y))
    ln.line.color.rgb = color; ln.line.width = Pt(weight)
    return ln

def fit_picture(s, path, box):
    bx, by, bw, bh = box
    with Image.open(path) as im:
        iw, ih = im.size
    sc = min(bw / iw, bh / ih)
    w, h = iw * sc, ih * sc
    return s.shapes.add_picture(path, Inches(bx + (bw - w) / 2),
                                Inches(by + (bh - h) / 2), width=Inches(w))

def chart(s, name, box=(0.7, 1.25, 11.9, 4.85)):
    return fit_picture(s, f"{FIG}/{name}.png", box)

def button(s, x, y, label, target_key, back=False):
    w = 0.38 + 0.093 * len(label)
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(0.38))
    sh.fill.solid(); sh.fill.fore_color.rgb = BTNBG
    sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = ("◂ " if back else "") + label
    r.font.name = FONT; r.font.size = Pt(12); r.font.color.rgb = NAVY
    BTNS.append((sh, target_key))
    return x + w + 0.16

def buttons_row(s, labels_targets, y=6.96, x=0.9):
    for lab, tgt in labels_targets:
        x = button(s, x, y, lab, tgt)

def backbtn(s, target_key):
    button(s, 11.82, 6.96, "back", target_key, back=True)

def divider(num, title):
    s = prs.slides.add_slide(blank)
    PAGENO[0] += 1
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width,
                            prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background(); bg.shadow.inherit = False
    add_text(s, 1.0, 2.45, 11.33, 1.3,
             [(num, 60, RGBColor(0xFF, 0xFF, 0xFF), True, False, 0)],
             align=PP_ALIGN.CENTER)
    add_text(s, 1.0, 4.05, 11.33, 0.8,
             [(title, 28, RGBColor(0xD7, 0xE3, 0xF2), False, False, 0)],
             align=PP_ALIGN.CENTER)
    return s

def cell(s, x, y, w, h, fill, border=None, label=None, lab_color=None):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill if fill else RGBColor(0xFF, 0xFF, 0xFF)
    if border is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = border; sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    if label:
        tf = sh.text_frame; tf.word_wrap = False
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = label
        r.font.name = FONT; r.font.size = Pt(15); r.font.bold = True
        r.font.color.rgb = lab_color or RGBColor(0xFF, 0xFF, 0xFF)
    return sh

def table(s, cols, rows, y0, size=15, rowh=0.5):
    x0 = cols[0][0]
    x1 = cols[-1][0] + cols[-1][1]
    rule(s, x0, y0, x1 - x0, 1.6, NAVY)
    y = y0 + 0.12
    for row_ in rows:
        if row_ == "RULE":
            rule(s, x0, y + 0.02, x1 - x0, 0.9, NAVY)
            y += 0.14
            continue
        if isinstance(row_, tuple) and row_ and row_[0] == "GAP":
            y += row_[1]
            continue
        for (x, w, al), spec in zip(cols, row_):
            txt, bold, color = spec[0], spec[1], spec[2]
            sz = spec[3] if len(spec) > 3 else size
            if txt:
                add_text(s, x, y, w, rowh, [(txt, sz, color, bold, False, 0)],
                         align=al)
        y += rowh
    rule(s, x0, y + 0.04, x1 - x0, 1.6, NAVY)
    return y

L, C, R = PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.RIGHT
def row(*cells_):
    return list(cells_)
def pl(t, b=False, c=INK, sz=None):
    return (t, b, c) if sz is None else (t, b, c, sz)

# ================= 1. title =================
s = prs.slides.add_slide(blank)
PAGENO[0] += 1
band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(2.1),
                          prs.slide_width, Inches(2.5))
band.fill.solid(); band.fill.fore_color.rgb = NAVY
band.line.fill.background(); band.shadow.inherit = False
add_text(s, 1.0, 2.45, 11.33, 1.4, [
 ("Measuring Teacher Attrition with Labour Force Survey Data",
  30, RGBColor(0xFF, 0xFF, 0xFF), True, False, 8),
 ("The Case of the United States", 20, RGBColor(0xD7, 0xE3, 0xF2), False, False, 0)],
 align=C)
add_text(s, 1.0, 5.00, 11.33, 0.5,
         [("José Elías Durán Roa", 18, INK, False, False, 0)], align=C)
add_text(s, 1.0, 5.55, 11.33, 0.4,
         [("Data Cluster · Directorate for Education and Skills",
           14, MUT, False, False, 0)], align=C)
s.shapes.add_picture(LOGO, Inches((13.333 - 1.7) / 2), Inches(6.15),
                     width=Inches(1.7))

# ================= 2. motivation =================
s = new_slide(title="Motivation and problem", key="mainmot")
add_text(s, 0.9, 1.35, 11.8, 0.5, [("Motivation", 20, ACC, True, False, 0)])
bullets(s, [
 "Understand why teachers leave the profession.",
 "Is there a real policy margin to soften teacher shortages by retaining "
 "teachers, or bringing them back?"], y=2.00, size=20, gap=20)
add_text(s, 0.9, 4.00, 11.8, 0.5, [("Problem", 20, ACC, True, False, 0)])
bullets(s, [
 "Official microdata on teachers are not publicly available for many countries.",
 "We start with the United States, the country with the most information "
 "available."], y=4.60, size=20, gap=20)
buttons_row(s, [("official sources", "appsources")])
NOTES[2] = ("Motivacion y problema. Boton de fuentes oficiales y sus "
            "huecos temporales.")

# ================= 3. contribution =================
s = new_slide(title="Contribution")
add_text(s, 0.9, 1.75, 11.8, 0.6,
         [("We use the Current Population Survey to", 20, INK, False, False, 0)])
bullets(s, [
 "reproduce and extend the official statistics on teachers leaving the "
 "profession;",
 "having achieved A, study in detail how many leave, where they go, and why."],
 y=3.05, size=22, gap=44, numbered=True)

divider("0", "Methodological discussion")

# ================= 5. CPS =================
s = new_slide(title="The Current Population Survey", key="maincps")
bullets(s, [
 "The monthly household survey of the United States, run by the Census "
 "Bureau for the Bureau of Labor Statistics. Nationally representative of "
 "the civilian non-institutional population.",
 "We pool 28 consecutive March supplements, 1998–2025, which give us "
 "5.0 million person-year records.",
 "104,545 of them are teachers, about 3,700 per year."],
 y=1.95, size=20, gap=46)
buttons_row(s, [("unemployment", "appunemp"), ("interviews", "approtation"),
                ("migration", "appmigration"), ("identity", "appidentity")])

# ================= 6. ASEC =================
s = new_slide(title="The March supplement (ASEC)")
bullets(s, [
 "Run by the Census Bureau each March since 1948. It is the source of the "
 "official annual income, poverty and health-insurance statistics.",
 "About 90,000 households, counting the March sample plus oversamples "
 "interviewed in February and April.",
 "Every adult reports on the previous calendar year, including the longest "
 "job held, weeks worked, earnings and benefits."], y=2.05, size=20, gap=48)

# ================= 7. codes =================
s = new_slide(title="Identifying a teacher: the census occupation codes",
              key="maincodes")
cols = [(0.9, 4.0, L), (5.1, 2.4, C), (7.6, 2.6, C), (10.3, 2.4, C)]
rows = [
 row(pl(""), pl("1990 codes", True), pl("2002/2010 codes", True),
     pl("2018 codes", True)),
 row(pl(""), pl("surveys 1998–2002", False, MUT, 12),
     pl("surveys 2003–2019", False, MUT, 12),
     pl("surveys 2020–2025", False, MUT, 12)),
 "RULE",
 row(pl("Pre-K and kindergarten"), pl("155"), pl("2300"), pl("2300")),
 row(pl("Elementary (and middle)"), pl("156"), pl("2310"), pl("2310")),
 row(pl("Secondary"), pl("157"), pl("2320"), pl("2320")),
 row(pl("Special education"), pl("158"), pl("2330"), pl("2330")),
 row(pl("Other teachers and instructors"), pl("159"), pl("2340"), pl("2360")),
]
yend = table(s, cols, rows, 1.45, size=16, rowh=0.52)
add_text(s, 0.9, yend + 0.28, 11.8, 0.8, [
 ("The K–12 block maps one-to-one across the three regimes. The group "
  "is constant over time even where single codes are not.",
  15.5, INK, False, False, 0)])
buttons_row(s, [("traceability", "appcodes")])

# ================= 8. rotation =================
s = new_slide(title="How a household is interviewed")
scw = 11.53 / 16
add_text(s, 0.9, 2.20, 3.5, 0.4, [("interviewed 4 months", 16, NAVY, True, False, 0)])
add_text(s, 4.9, 2.20, 3.6, 0.4, [("8 months out", 15, MUT, False, True, 0)], align=C)
add_text(s, 9.0, 2.20, 3.5, 0.4, [("interviewed 4 months", 16, BURG, True, False, 0)],
         align=R)
for i in range(16):
    x0 = 0.9 + i * scw
    if i < 4:
        cell(s, x0, 2.75, scw, 0.72, NAVY, None, str(i + 1))
    elif i >= 12:
        cell(s, x0, 2.75, scw, 0.72, BURG, None, str(i - 7))
    else:
        cell(s, x0, 2.75, scw, 0.72, None, LGRAYB)
for xi, lab in [(0.9, "Mar"), (0.9 + 3 * scw, "Jun"),
                (0.9 + 12 * scw, "Mar"), (0.9 + 15 * scw, "Jun")]:
    add_text(s, xi, 3.55, scw, 0.3, [(lab, 13, MUT, False, False, 0)], align=C)
add_text(s, 0.9, 3.92, 4 * scw, 0.35, [("year 1", 14, MUT, False, True, 0)], align=C)
add_text(s, 0.9 + 12 * scw, 3.92, 4 * scw, 0.35, [("year 2", 14, MUT, False, True, 0)], align=C)
arrow = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.9 + scw / 2),
                               Inches(4.65), Inches(0.9 + 12.5 * scw), Inches(4.65))
arrow.line.color.rgb = INK; arrow.line.width = Pt(1.6)
add_text(s, 1.5, 4.85, 10.0, 0.45,
         [("the same interview, twelve months later", 16, INK, False, False, 0)],
         align=C)

# ================= 9. two ways =================
s = new_slide(title="Two ways to identify a leaver")
add_text(s, 0.9, 1.50, 5.7, 0.5, [("A. Follow the individual", 19, NAVY, True, False, 0)])
add_text(s, 0.9, 2.20, 5.7, 0.5, [("All months. Links require matching", 16, INK, False, False, 0)])
add_text(s, 0.9, 2.85, 5.7, 2.2, [
 ("household identifier", 16, INK, False, False, 8),
 ("dwelling identifier", 16, INK, False, False, 8),
 ("person line number", 16, INK, False, False, 12),
 ("validated on sex, race, age +0–2", 15, MUT, False, False, 0)])
add_text(s, 7.1, 1.50, 5.5, 0.5, [("B. Ask about last year", 19, NAVY, True, False, 0)])
add_text(s, 7.1, 2.20, 5.5, 2.4, [
 ("The March supplement, retrospectively.", 16, INK, False, False, 14),
 ("Taught as last year’s longest job and not teaching this March "
  "⇒ left.", 16, INK, False, False, 0)])

# ================= 10. disadvantages =================
s = new_slide(title="Disadvantages of each option", key="maindisadv")
add_text(s, 0.9, 1.40, 5.7, 0.5, [("A. Following individuals", 18, NAVY, True, False, 0)])
bullets(s, [
 "Identity is not certain, validation can admit noisy people.",
 "Movers are lost. About 25% of addresses are not found a year later.",
 "Normal household attrition on top.",
 "Strong seasonality in teaching.",
 "Many ways to define the rate (next slide)."],
 y=2.00, size=15, gap=13, x=0.9, w=5.7, numbered=True)
add_text(s, 7.1, 1.40, 5.6, 0.5, [("B. Retrospective March", 18, NAVY, True, False, 0)])
bullets(s, [
 "Recall bias.",
 "Less sample. One observation per person per year (~3,700 teachers) "
 "against ~11,000 monthly teacher observations.",
 "Only March-to-March transitions. Within-year spells are smoothed away."],
 y=2.00, size=15, gap=13, x=7.1, w=5.6, numbered=True)
buttons_row(s, [("linkage loss", "applink"),
                ("definition sensitivity", "appgradient"),
                ("validation", "appidentity")])

# ================= 11. six definitions =================
s = new_slide(title="Six ways to define leaving, simplest to strictest")
add_text(s, 0.9, 1.30, 11.8, 0.45,
         [("Unit: the individual. Four interviews in year 1, four in year 2.",
           15.5, MUT, False, False, 0)])
cols = [(0.9, 2.4, L), (3.5, 4.5, L), (8.2, 4.4, L)]
rows = [
 row(pl(""), pl("A teacher…", True), pl("A leaver…", True)),
 "RULE",
 row(pl("Single", True, NAVY), pl("seen teaching in ≥ 1 of the 4 year-1 interviews"),
     pl("seen teaching in none of the 4 year-2 interviews")),
 row(pl("Pair", True, NAVY), pl("seen teaching in ≥ 2 of the 4"),
     pl("seen teaching in none of the 4")),
 row(pl("Triple", True, NAVY), pl("seen teaching in ≥ 3 of the 4"),
     pl("seen teaching in none of the 4")),
 row(pl("Strict", True, NAVY), pl("seen teaching in all 4"),
     pl("seen teaching in none of the 4")),
 row(pl("Month pairs", True, NAVY), pl("each teaching month, on its own"),
     pl("not seen teaching twelve months later")),
 row(pl("Annual recall", True, NAVY), pl("teaching was last year’s longest job"),
     pl("not teaching at the March interview")),
]
table(s, cols, rows, 1.90, size=14.5, rowh=0.70)

# ================= 12. defs6 =================
s = new_slide(title="The six, on one axis")
chart(s, "defs6", (0.7, 1.2, 11.9, 5.4))
add_text(s, 0.9, 6.78, 11.8, 0.4,
         [("NCES is the National Center for Education Statistics. Its Teacher "
           "Follow-up Survey is the official benchmark.", 13, MUT, False, False, 0)])
NOTES[12] = ("Seis definiciones en un eje. Rombos negros, benchmark "
             "oficial del NCES (TFS, 8.0).")

divider("1", "Leaving rate: how many leave")

# ================= 14. evolution =================
s = new_slide(title="Leaving teaching, 1997–2024", key="mainevol")
chart(s, "g2_evolution", (0.7, 1.2, 11.9, 4.85))
message(s, "Around 8 of every 100 teachers leave each year, and the rate has "
        "been stable for 25 years. Attrition is a permanent flow, not a "
        "recent crisis.")
buttons_row(s, [("public vs private", "apppubpriv")])
NOTES[14] = ("Serie estable. Promedios EAG para paises con datos: 6,6 "
             "(datos 2016, EAG 2021); 6,5 (2022/23, EAG 2025); 6,4 "
             "(2024/25, EAG 2026). Paises con series largas tambien "
             "estables. EEUU por encima de la mayoria.")

# ================= 15. comparability =================
s = new_slide(title="Comparable professions: who we compare teachers with")
cols = [(0.9, 4.0, L), (5.1, 1.8, R), (7.0, 1.8, R), (8.9, 1.9, R), (10.9, 1.7, R)]
rows = [
 row(pl(""), pl("Teachers", True), pl("Nurses", True),
     pl("Social workers", True), pl("Accountants", True)),
 "RULE",
 row(pl("Female (%)"), pl("76.0"), pl("88.2"), pl("82.9"), pl("57.0")),
 row(pl("Average age (years)"), pl("44.4"), pl("43.1"), pl("43.4"), pl("44.1")),
 row(pl("Master’s or higher (%)"), pl("51.9"), pl("25.9"), pl("50.8"), pl("31.3")),
 row(pl("Public sector (%)"), pl("70.2"), pl("12.3"), pl("43.1"), pl("11.0")),
 row(pl("Weeks worked"), pl("46.6"), pl("49.3"), pl("49.6"), pl("49.5")),
 row(pl("Median annual wage ($)"), pl("56,000"), pl("80,000"), pl("57,000"), pl("77,000")),
 "RULE",
 row(pl("Observations"), pl("28,932"), pl("13,107"), pl("3,407"), pl("6,897")),
]
yend = table(s, cols, rows, 1.40, size=15, rowh=0.47)
add_text(s, 0.9, yend + 0.16, 11.8, 0.4,
         [("College graduates, pooled 2015–2024, weighted; wages from 2020–2024.",
           12.5, MUT, False, True, 0)])
message(s, "Teaching shares its age and gender profile with nursing and "
        "social work. What sets it apart is pay and the public sector.",
        y=6.55, size=14.5)

# ================= 16. professions =================
s = new_slide(title="Leaving the occupation, by profession", key="mainprofs")
chart(s, "leave_professions_deck", (0.7, 1.2, 11.9, 4.85))
message(s, "Teachers leave at about the same rate as comparable professions. "
        "What makes teaching special is not how many leave, but who leaves "
        "and where they go.")
buttons_row(s, [("more professions", "appprofs")])

divider("2", "Composition: where they go")

# ================= 18. flow employed =================
s = new_slide(title="Of every 100 leavers (average, 2020–2024)", key="mainflow")
chart(s, "flow_employed_5yr", (0.8, 1.15, 11.7, 4.95))
message(s, "A third find another job, a third retire, and the rest split "
        "between early labor-force exit and unemployment.")
buttons_row(s, [("vs NCES follow-up", "apptfs")])
NOTES[18] = ("De cada 100 que dejan la docencia: 29 otro empleo, 36 retiro "
             "(55+), 24 salida antes de 55, 11 paro. De los 29 empleados: "
             "6 educacion, 2 cuidado, 9 otras profesiones, 11 resto.")

# ================= 19. occupations =================
s = new_slide(title="Where the employed leavers go", key="mainocc")
chart(s, "occ_all_slide", (0.4, 1.12, 12.5, 5.1))
message(s, "36% of the employed leavers move to occupations where fewer "
        "than half of US workers hold a college degree (in red).",
        y=6.30, size=14.5)
buttons_row(s, [("proportions", "appoccprop")])

# ================= 20. flow olf55 =================
s = new_slide(title="Who leaves the labor force before 55 (average, 2020–2024)")
chart(s, "flow_olf55_5yr", (0.8, 1.15, 11.7, 4.95))
message(s, "Early labor-force exit is mostly a family story. More than half "
        "of this group are mothers with a child at home.")
NOTES[20] = ("Salida temprana, historia de familia. Mas de la mitad madres "
             "con hijo en casa (13 de los 24).")

# ================= 21. study =================
s = new_slide(title="And the youngest of them leave to study")
chart(s, "study_olf55", (0.8, 1.15, 11.7, 4.95))
message(s, "Studying is concentrated among the young and the childless. 45% "
        "of those under 30 are enrolled in school, against 3% of the mothers "
        "with a child at home.")
NOTES[21] = ("Estudia el 45% de los menores de 30 y el 25-48% de los que "
             "no tienen hijos, frente al 3% de las madres. n pequenos, "
             "indicados en el grafico.")

# ================= 22. policy =================
s = new_slide(title="What this says for policy: three margins, quantified")
bullets(s, [
 ("Retirees.", "About 3% of teachers retire each year, a third of all "
  "exits. Delaying retirement is a short-term margin that extends careers "
  "but does not reintegrate anyone."),
 ("Switchers.", "About 2% of teachers move to another job each year, more "
  "than a third of them to jobs that do not require a degree. The margin is "
  "real but moderate, so shortages cannot be closed through retention "
  "alone."),
 ("Early exits.", "About 2% of teachers leave the labor force before 55 "
  "each year. Most are mothers at home, for whom flexibility may be the "
  "missing piece. The young and childless leave to study and need re-entry "
  "paths.")], y=1.85, size=19, gap=44)

divider("3", "Correlations: why they leave")

# ================= 24. specification =================
s = new_slide(title="Specification", key="maineq")
fit_picture(s, EQ_PNG, (2.1, 1.30, 9.1, 1.30))
cols = [(1.4, 1.0, L), (2.5, 10.0, L)]
rows = [
 row(pl("y", True, NAVY), pl("teacher i left teaching in year t")),
 row(pl("a", True, NAVY), pl("job attachment – full-year contract, part-time contract")),
 row(pl("c", True, NAVY), pl("pay and security – pension plan, public sector, "
                             "bottom-quartile household income")),
 row(pl("f", True, NAVY), pl("family – new baby, children, marital status")),
 row(pl("h", True, NAVY), pl("health – self-reported health, disability")),
 row(pl("d", True, NAVY), pl("demographics – age, sex, race, education")),
 row(pl("δt", True, NAVY), pl("year fixed effects (state FE variant in the appendix)")),
]
yend = table(s, cols, rows, 2.85, size=14, rowh=0.43)
add_text(s, 1.4, yend + 0.18, 10.8, 0.45,
         [("Probit, average marginal effects, robust standard errors. "
           "2018–2024, n = 18,571.", 14, INK, False, False, 0)])
buttons_row(s, [("LPM", "applpm"), ("logit / probit", "appmodels"),
                ("bounded?", "appbounded"), ("what we observe", "appframework")])
NOTES[24] = ("a: vinculacion al empleo. c: pago y seguridad. f: familia. "
             "h: salud. d: demografia. delta-t: efectos de ano. La LPM no "
             "esta acotada (22% de ajustados bajo cero), por eso el probit "
             "es la especificacion principal.")

# ================= 25. AME =================
s = new_slide(title="What correlates with leaving")
chart(s, "ame_ext", (0.6, 1.12, 12.1, 6.1))

# ================= 26-29 =================
s = new_slide(title="Relative pay since 1997")
chart(s, "msgA3", (0.7, 1.2, 11.9, 4.85))
message(s, "Real teacher pay is 4% below its 1997 level while every "
        "comparison group gained ground. The gap to other graduates is now "
        "$29,000 a year.")

s = new_slide(title="Leaving, by position in the teacher pay distribution")
chart(s, "pay3_deciles_deck", (0.9, 1.2, 11.5, 4.85))
message(s, "Leaving is concentrated in the bottom two pay deciles, where "
        "part-year and part-time contracts live. Above the median, pay "
        "barely matters.")

s = new_slide(title="Pension coverage and leaving, across states")
chart(s, "pension_scatter_deck", (0.9, 1.2, 11.5, 4.85))
message(s, "States where more teachers have a pension plan lose fewer "
        "teachers before 55. Economic security retains.")

s = new_slide(title="Leaving and the cycle")
chart(s, "cycle1", (0.7, 1.2, 11.9, 4.85))
message(s, "Leaving rises when unemployment rises (correlation +0.32). "
        "Teachers are pushed out in bad times more than pulled away in good "
        "ones.")

# ================= 30-31. conclusions =================
s = new_slide(title="Conclusions: what we learn")
bullets(s, [
 "Teacher attrition is not bad in itself. Much of it reflects an active "
 "labor market, and it moves with the general cycle. The question for "
 "policy is who leaves, and why.",
 "Working conditions weigh heavily. A full-year contract is the single "
 "strongest protection against leaving, so job security is fundamental to "
 "retain a teacher.",
 "Not everyone who leaves earns more afterwards, and leaving concentrates "
 "at the bottom of the pay scale. The financial lever still has room as a "
 "retention incentive.",
 "A quarter of exits are neither another job nor retirement but care at "
 "home or further study. For that group flexibility is the incentive that "
 "can bring them back, and additional qualifications should pay when they "
 "return."], y=1.45, size=16.5, gap=20)

s = new_slide(title="Conclusions: where the policy margins are")
bullets(s, [
 ("Short term.", "Retirees, about 3% of teachers each year, are a pool "
  "that can cover local shortages. They bring experience and positive "
  "spillovers to the schools that re-engage them."),
 ("Medium term.", "The young. The probability of leaving is highest at "
  "the start of the career, so mentoring and accompaniment belong where "
  "the risk is."),
 ("Across the board.", "Economic security (full-year contracts, pension "
  "coverage) and flexibility, so that teachers who want to stay or to "
  "return can do so. Insecurity should not be the reason a position is "
  "left."),
 ("Caveat.", "We observe financial and life-cycle motives, not conditions "
  "inside schools. These are margins, not the full story.")],
 y=1.45, size=16.5, gap=20)

# ================= appendix =================
divider("A", "Appendix")

s = new_slide(title="Where official numbers exist, and when", key="appsources")
chart(s, "tfs_waves", (0.9, 1.15, 11.5, 4.1))
add_text(s, 0.9, 5.45, 11.8, 1.4, [
 ("The NCES (National Center for Education Statistics) follows up a sample "
  "of teachers one year later in the Teacher Follow-up Survey. There are "
  "eight waves since 1988–89, published with a 2–3 year lag, and "
  "nine years separate the last two. The OECD’s Education at a Glance "
  "collects national rates only in its 2021, 2025 and 2026 editions, with "
  "no current figure for the United States.", 14.5, INK, False, False, 0)])
backbtn(s, "mainmot")

s = new_slide(title="One survey, three instruments", key="appunemp")
cols = [(0.9, 3.0, L), (4.1, 4.3, L), (8.6, 3.9, L)]
rows = [
 row(pl("Instrument", True), pl("What it asks", True), pl("What it produces", True)),
 "RULE",
 row(pl("Basic monthly interview"), pl("Labor force status in the reference "
     "week, occupation, hours"), pl("The official monthly unemployment "
     "rate, employment and earnings statistics")),
 ("GAP", 0.85),
 row(pl("Topical supplements"), pl("School enrollment (Oct.), voting "
     "(Nov.), tobacco, computer use"), pl("Topic-specific official "
     "statistics")),
 ("GAP", 0.55),
 row(pl("March supplement (ASEC)"), pl("The previous calendar year, from "
     "the longest job to weeks, income and benefits"), pl("Official income, "
     "poverty and health-insurance statistics, and our retrospective "
     "measure")),
 ("GAP", 0.85),
]
table(s, cols, rows, 1.70, size=15, rowh=0.5)
backbtn(s, "maincps")

s = new_slide(title="Are interviews monthly? Who is new each month?", key="approtation")
add_text(s, 0.9, 1.35, 11.8, 0.7,
         [("Yes. Every month, one eighth of the sample sits in each position "
           "of the 4-8-4 rotation. Verified in all 251 monthly files, "
           "January 2005 to November 2025.", 15.5, INK, False, False, 0)])
cols = [(0.9, 2.8, L)] + [(3.8 + i * 1.1, 1.0, R) for i in range(8)]
rows = [
 row(pl("Month in sample", True), *[pl(str(i + 1), True) for i in range(8)]),
 "RULE",
 row(pl("Average share (%)"), pl("12.4"), pl("12.5"), pl("12.6"), pl("12.5"),
     pl("12.6"), pl("12.5"), pl("12.4"), pl("12.5")),
 row(pl("Minimum (%)"), pl("10.1"), pl("11.1"), pl("11.5"), pl("11.8"),
     pl("12.0"), pl("12.0"), pl("11.9"), pl("12.0")),
 row(pl("Maximum (%)"), pl("13.0"), pl("13.0"), pl("13.1"), pl("13.0"),
     pl("14.9"), pl("13.9"), pl("13.5"), pl("13.2")),
]
yend = table(s, cols, rows, 2.50, size=15, rowh=0.52)
add_text(s, 0.9, yend + 0.30, 11.8, 0.9, [
 ("So each month, about 12.5% of households are new, 37.5% sit in months "
  "2–4, and 50% are returning in months 5–8. Month-to-month "
  "overlap is 75% and year-to-year overlap is 50%, by design.",
  15, INK, False, False, 0)])
backbtn(s, "maincps")

s = new_slide(title="Internal migration in the United States", key="appmigration")
chart(s, "migration_rate", (0.9, 1.15, 11.5, 4.95))
message(s, "In 2023, 7.8% of Americans moved. This is the loss channel of "
        "any address-based panel.  (Census Bureau, CPS ASEC, table A-1.)",
        y=6.35, size=14.5)
backbtn(s, "maincps")

s = new_slide(title="Is the same person validated year to year?", key="appidentity")
cols = [(0.9, 5.6, L), (6.9, 5.8, L)]
rows = [
 row(pl("In the field", True), pl("In the public files", True)),
 "RULE",
 row(pl("Roster carried forward by the interviewer"),
     pl("No person identifier at all")),
 ("GAP", 0.30),
 row(pl("Each member keeps a line number"),
     pl("Household id + dwelling id + line number reconstruct it")),
 ("GAP", 0.65),
 row(pl("Occupation asked by dependent interviewing month to month"),
     pl("Validated on sex, race, age advancing 0–2 years")),
 ("GAP", 0.65),
 row(pl("Identity is known", True, NAVY),
     pl("Identity is inferred. A mover replaced by someone of the same sex "
        "and similar age can slip through", True, BURG)),
 ("GAP", 0.95),
]
table(s, cols, rows, 1.60, size=15, rowh=0.5)
backbtn(s, "maindisadv")

s = new_slide(title="How much is lost in linking, and who", key="applink")
chart(s, "linkage_series", (0.9, 1.15, 11.5, 4.95))
message(s, "Teachers link more than other graduates, not less. But movers "
        "leave teaching more, so panel measures are lower bounds on "
        "mobility-related exit.", y=6.35, size=14.5)
backbtn(s, "maindisadv")

s = new_slide(title="Why the rate falls as the definition tightens", key="appgradient")
chart(s, "sighting_gradient", (1.2, 1.12, 10.9, 4.5))
add_text(s, 0.9, 5.80, 11.8, 1.1, [
 ("How many times must we see someone teaching in year 1 before calling "
  "them a teacher? Seen once, 54% are never seen teaching in their year-2 "
  "interviews. Seen in all four, 10%. The stricter the definition, the "
  "lower the measured leaving rate. That is the whole ladder of the six "
  "definitions.", 14.5, INK, False, False, 0)])
backbtn(s, "maindisadv")

s = new_slide(title="Public vs private schools", key="apppubpriv")
chart(s, "pubpriv_series", (0.8, 1.2, 11.7, 5.4))
backbtn(s, "mainevol")

s = new_slide(title="More professions, and their average", key="appprofs")
chart(s, "profs_ext", (0.8, 1.2, 11.7, 5.4))
backbtn(s, "mainprofs")

s = new_slide(title="Our destinations vs the NCES follow-up survey", key="apptfs")
cols = [(0.6, 3.3, L), (4.0, 1.2, R), (5.3, 1.2, R)]
rows = [
 row(pl("Of every 100 leavers…", True), pl("CPS", True), pl("TFS", True)),
 row(pl(""), pl("2020–24 avg.", False, MUT, 10.5), pl("2021–22", True, INK, 10.5)),
 "RULE",
 row(pl("Working in another job"), pl("28.8"), pl("57.2")),
 row(pl("   K–12, non-teaching"), pl("–"), pl("39.3")),
 row(pl("   outside education"), pl("–"), pl("11.8")),
 row(pl("Retired / out of LF, 55+"), pl("36.4"), pl("27.7")),
 row(pl("Out of the LF, under 55"), pl("23.7"), pl("10.1")),
 row(pl("Unemployed"), pl("11.1"), pl("4.8")),
]
yend = table(s, cols, rows, 1.50, size=13, rowh=0.42)
add_text(s, 0.6, yend + 0.20, 6.0, 1.2,
         [("TFS is the Teacher Follow-up Survey 2021–22, the follow-up "
           "of the 2020–21 NTPS. Sources: NCES 2024-039, table A-8, and "
           "NTPS estimate tables.", 11, MUT, False, True, 0)])
add_text(s, 7.1, 1.40, 5.7, 0.45, [("Why the columns differ", 16, NAVY, True, False, 0)])
bullets(s, [
 ("Who counts as a teacher.", "TFS follows regular classroom teachers of "
  "public schools, sampled in schools. We cover public and private, and "
  "anyone whose longest job was teaching."),
 ("What counts as working.", "39 of the TFS’s 57 employed leavers hold "
  "non-teaching K–12 jobs. They left the classroom, not the school "
  "system. Our 28.8 means leaving the teaching occupation."),
 ("Who is reachable.", "A school-based sample under-represents weakly "
  "attached teachers, exactly those who exit to non-participation. A "
  "household survey catches them."),
 ("The window.", "Our column averages five years, 2020–2024. The TFS "
  "is the single year 2021–22.")],
 y=1.95, size=12, gap=10, x=7.1, w=5.7, numbered=True)
backbtn(s, "mainflow")

s = new_slide(title="The proportions behind the destinations chart", key="appoccprop")
cols = [(0.9, 7.6, L), (8.7, 2.2, R)]
rows = [
 row(pl("Of every 100 employed leavers\u2026", True), pl("share", True)),
 "RULE",
 row(pl("Education, non-teaching"), pl("22.6")),
 row(pl("Care"), pl("8.5")),
 row(pl("Professional and managerial"), pl("32.4")),
 row(pl("Sales, office and manual"), pl("36.5")),
 "RULE",
 row(pl("Memo: occupations where fewer than half of US workers "
        "hold a college degree (in red)", False, BURG), pl("36.3", True, BURG)),
]
yend = table(s, cols, rows, 1.60, size=15.5, rowh=0.52)
add_text(s, 0.9, yend + 0.30, 11.8, 1.2,
         [("Calendar 2020\u20132024; 344 employed leavers. The college-degree "
           "share of each destination occupation is computed among all "
           "employed US workers aged 25\u201364 in the same ASEC files, "
           "2021\u20132025. 31.2 of the 36.3 red points sit in the sales, "
           "office and manual group; 5.1 in professional occupations.",
           13, MUT, False, False, 0)])
backbtn(s, "mainocc")

s = new_slide(title="Is the teacher group constant across code changes?", key="appcodes")
chart(s, "codes_narrow", (0.9, 1.15, 11.5, 4.95))
message(s, "Recomputing the whole series on the narrow core moves the "
        "pooled rate by 0.1 points. The 2003 and 2020 reclassifications "
        "leave no visible break.", y=6.35, size=14.5)
backbtn(s, "maincodes")

def aer_table(s, header3, rows7, bottom, note):
    x0, x1 = 1.1, 11.5
    rule(s, x0, 1.42, x1 - x0, 1.6, NAVY)
    add_text(s, 5.5, 1.50, 6.0, 0.3,
             [(header3[0], 12.5, INK, False, False, 0)], align=C)
    rule(s, 5.5, 1.86, 6.0, 0.9, NAVY)
    y = 1.93
    for i, h in enumerate(header3[1]):
        add_text(s, 5.5 + i * 2.05, y, 1.85, 0.3, [(h, 12.5, INK, True, False, 0)],
                 align=R)
    y += 0.36
    rule(s, x0, y, x1 - x0, 0.9, NAVY)
    y += 0.09
    for lab, coefs, ses in rows7:
        add_text(s, 1.1, y, 4.2, 0.3, [(lab, 12.5, INK, False, False, 0)])
        for i, cfe in enumerate(coefs):
            add_text(s, 5.5 + i * 2.05, y, 1.85, 0.3,
                     [(cfe, 12.5, INK, False, False, 0)], align=R)
        y += 0.28
        for i, se in enumerate(ses):
            add_text(s, 5.5 + i * 2.05, y, 1.85, 0.3,
                     [(se, 11, MUT, False, False, 0)], align=R)
        y += 0.29
    rule(s, x0, y + 0.02, x1 - x0, 0.9, NAVY)
    y += 0.11
    for lab, vals in bottom:
        add_text(s, 1.1, y, 4.2, 0.3, [(lab, 12.5, INK, False, False, 0)])
        for i, v in enumerate(vals):
            add_text(s, 5.5 + i * 2.05, y, 1.85, 0.3,
                     [(v, 12.5, INK, False, False, 0)], align=R)
        y += 0.32
    rule(s, x0, y + 0.02, x1 - x0, 1.6, NAVY)
    add_text(s, 1.1, y + 0.16, 10.4, 0.6, [(note, 10.5, MUT, False, True, 0)])

VARS = ["Full-year contract", "Part-time contract", "Employer pension plan",
        "Public sector", "New baby during the year", "With a disability",
        "Bottom-quartile household income"]
s = new_slide(title="Linear probability model, fixed-effects variants", key="applpm")
aer_table(s,
 ("Dependent variable: left teaching (×100)", ["(1)", "(2)", "(3)"]),
 [(VARS[0], ["−11.54***", "−11.55***", "−11.65***"], ["(0.67)", "(0.66)", "(0.67)"]),
  (VARS[1], ["+8.67***", "+8.67***", "+8.63***"], ["(1.09)", "(1.09)", "(1.10)"]),
  (VARS[2], ["−2.35***", "−2.33***", "−2.33***"], ["(0.52)", "(0.52)", "(0.52)"]),
  (VARS[3], ["−2.35***", "−2.38***", "−2.39***"], ["(0.56)", "(0.56)", "(0.56)"]),
  (VARS[4], ["+5.72***", "+5.63***", "+5.71***"], ["(1.56)", "(1.56)", "(1.56)"]),
  (VARS[5], ["+8.85***", "+8.94***", "+8.94***"], ["(2.14)", "(2.14)", "(2.14)"]),
  (VARS[6], ["+4.17***", "+4.13***", "+4.01***"], ["(1.24)", "(1.24)", "(1.25)"])],
 [("Year fixed effects", ["No", "Yes", "Yes"]),
  ("State fixed effects", ["No", "No", "Yes"]),
  ("Observations", ["18,571", "18,571", "18,571"])],
 "Robust standard errors in parentheses. * p<0.10, ** p<0.05, *** p<0.01. "
 "Weighted. Full set of controls as in the main specification.")
backbtn(s, "maineq")

s = new_slide(title="LPM vs logit vs probit", key="appmodels")
aer_table(s,
 ("Average marginal effect on leaving (×100)", ["LPM", "Logit", "Probit"]),
 [(VARS[0], ["−11.13***", "−8.78***", "−8.49***"], ["(0.55)", "(0.40)", "(0.39)"]),
  (VARS[1], ["+8.77***", "+3.86***", "+4.32***"], ["(0.92)", "(0.44)", "(0.47)"]),
  (VARS[2], ["−2.55***", "−2.38***", "−2.41***"], ["(0.44)", "(0.39)", "(0.38)"]),
  (VARS[3], ["−2.17***", "−2.24***", "−2.27***"], ["(0.47)", "(0.39)", "(0.39)"]),
  (VARS[4], ["+5.65***", "+4.74***", "+4.59***"], ["(1.33)", "(0.90)", "(0.91)"]),
  (VARS[5], ["+8.31***", "+3.78***", "+4.19***"], ["(1.84)", "(0.80)", "(0.88)"]),
  (VARS[6], ["+4.67***", "+2.24***", "+2.50***"], ["(1.10)", "(0.58)", "(0.62)"])],
 [("Year fixed effects", ["Yes", "Yes", "Yes"]),
  ("Observations", ["18,571", "18,571", "18,571"])],
 "Standard errors in parentheses, delta method for the logit and probit "
 "marginal effects. * p<0.10, ** p<0.05, *** p<0.01. The probit column is "
 "the main specification of the coefficient plot.")
backbtn(s, "maineq")

s = new_slide(title="Is the LPM bounded between 0 and 1?", key="appbounded")
chart(s, "lpm_check", (1.3, 1.12, 10.7, 4.9))
message(s, "No. 22% of fitted values fall below zero, so the probit is the "
        "main specification and the LPM a robustness variant.",
        y=6.30, size=14.5)
backbtn(s, "maineq")

s = new_slide(title="What the CPS observes, of why teachers leave", key="appframework")
cols = [(0.9, 7.6, L), (8.7, 3.4, L)]
rows = [
 row(pl("Reasons in the literature", True), pl("In the CPS?", True)),
 "RULE",
 row(pl("Working conditions"), pl("no", False, MUT)),
 row(pl("Organizational support"), pl("no", False, MUT)),
 row(pl("Autonomy and intrinsic motives"), pl("no", False, MUT)),
 row(pl("Financial factors"), pl("yes", True, NAVY)),
 row(pl("Personal life-cycle motives"), pl("yes", True, NAVY)),
 "RULE",
 row(pl("Sociodemographics"), pl("yes", True, NAVY)),
]
table(s, cols, rows, 1.70, size=16.5, rowh=0.56)
backbtn(s, "maineq")

# ---- wire the buttons, attach notes ----
for sh, key in BTNS:
    sh.click_action.target_slide = REG[key]
for n, txt in NOTES.items():
    prs.slides[n - 1].notes_slide.notes_text_frame.text = txt

prs.save(OUT)
print(f"saved {OUT} with {len(prs.slides._sldIdLst)} slides")
