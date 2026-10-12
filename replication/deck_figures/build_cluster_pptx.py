"""Native PPTX mirror of the Data Cluster Beamer deck (LaTeX look).
Latin Modern Sans (fonts shipped in report/data_cluster/fonts), plain
white design, navy structure, appendix with clickable buttons that jump
to the appendix slide and back. Writes
report/data_cluster/Proyect_US_cluster.pptx. Run from the repo root."""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

FIG = "report/figures_deck"
OUT = "report/data_cluster/Proyect_US_cluster.pptx"
LOGO = "report/data_cluster/oecd_logo.png"
EQ_PNG = os.environ.get("EQ_PNG", "report/data_cluster/equation2.png")

FONT = "Latin Modern Sans"
INK = RGBColor(0x1A, 0x1A, 0x1A)
MUT = RGBColor(0x6B, 0x74, 0x80)
NAVY = RGBColor(0x1F, 0x38, 0x64)
BURG = RGBColor(0x7B, 0x25, 0x30)
LGRAYB = RGBColor(0xC9, 0xCF, 0xD6)
BTNBG = RGBColor(0xE4, 0xE9, 0xF2)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
PAGENO = [0]
REG = {}          # key -> slide
BTNS = []         # (shape, target_key)

def new_slide(title=None, number=True, key=None):
    s = prs.slides.add_slide(blank)
    PAGENO[0] += 1
    if key:
        REG[key] = s
    if title:
        box = s.shapes.add_textbox(Inches(0.55), Inches(0.30), Inches(12.3),
                                   Inches(0.55))
        tf = box.text_frame; tf.word_wrap = True; tf.auto_size = None
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = title
        r.font.name = FONT; r.font.size = Pt(22); r.font.bold = True
        r.font.color.rgb = NAVY
    if number:
        nb = s.shapes.add_textbox(Inches(12.55), Inches(7.08), Inches(0.6),
                                  Inches(0.3))
        tf = nb.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
        r = p.add_run(); r.text = str(PAGENO[0])
        r.font.name = FONT; r.font.size = Pt(10); r.font.color.rgb = MUT
    return s

def add_text(s, x, y, w, h, parts, align=PP_ALIGN.LEFT, spacing=1.35):
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

def bullets(s, items, y=1.55, size=17, gap=22, x=0.9, w=11.6, numbered=False):
    parts = []
    for i, it in enumerate(items):
        after = gap if i < len(items) - 1 else 0
        marker = f"{i+1}.   " if numbered else "▸   "
        parts.append([[(marker, size, NAVY, not numbered, False),
                       (it, size, INK, False, False)], after])
    return add_text(s, x, y, w, 5.5, parts, spacing=1.35)

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

def button(s, x, y, label, target_key, back=False):
    w = 0.30 + 0.085 * len(label)
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(0.34))
    sh.fill.solid(); sh.fill.fore_color.rgb = BTNBG
    sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = ("◂ " if back else "") + label
    r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = NAVY
    BTNS.append((sh, target_key))
    return x + w + 0.15

def buttons_row(s, labels_targets, y=6.95, x=0.9):
    for lab, tgt in labels_targets:
        x = button(s, x, y, lab, tgt)

def backbtn(s, target_key):
    button(s, 11.9, 6.95, "back", target_key, back=True)

def divider(num, title):
    s = new_slide(number=False)
    add_text(s, 1.0, 2.60, 11.33, 1.1, [(num, 44, NAVY, True, False, 0)],
             align=PP_ALIGN.CENTER)
    add_text(s, 1.0, 3.95, 11.33, 0.6, [(title, 24, INK, False, False, 0)],
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
        r.font.name = FONT; r.font.size = Pt(13); r.font.bold = True
        r.font.color.rgb = lab_color or RGBColor(0xFF, 0xFF, 0xFF)
    return sh

def table(s, cols, rows, y0, header=True, size=13, rowh=0.42, footrows=0):
    """cols: list of (x, w, align); rows: list of row-tuples (or 'RULE')."""
    x0 = cols[0][0]
    x1 = cols[-1][0] + cols[-1][1]
    rule(s, x0, y0, x1 - x0, 1.4)
    y = y0 + 0.10
    first = True
    for row in rows:
        if row == "RULE":
            rule(s, x0, y + 0.02, x1 - x0, 0.75)
            y += 0.12
            continue
        for (x, w, al), (txt, bold, color) in zip(cols, row):
            if txt:
                add_text(s, x, y, w, rowh, [(txt, size, color, bold, False, 0)],
                         align=al)
        y += rowh
        if first and header:
            rule(s, x0, y + 0.02, x1 - x0, 0.75)
            y += 0.12
            first = False
    rule(s, x0, y + 0.04, x1 - x0, 1.4)
    return y

L, C, R = PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.RIGHT
def row(*cells_):
    return [(t, b, c) for t, b, c in cells_]
def pl(t, b=False, c=INK):
    return (t, b, c)

# ================= 1. title =================
s = new_slide(number=False)
add_text(s, 1.2, 2.00, 10.93, 1.6, [
 ("Measuring Teacher Attrition with Labour Force Survey Data", 29, NAVY, True, False, 6),
 ("The Case of the United States", 19, NAVY, True, False, 0)], align=PP_ALIGN.CENTER)
add_text(s, 1.2, 4.05, 10.93, 0.5,
         [("José Elías Durán Roa", 16, INK, False, False, 0)],
         align=PP_ALIGN.CENTER)
add_text(s, 1.2, 4.60, 10.93, 0.4,
         [("Data Cluster · Directorate for Education and Skills", 12.5, MUT, False, False, 0)],
         align=PP_ALIGN.CENTER)
with Image.open(LOGO) as im:
    lw = 1.8
s.shapes.add_picture(LOGO, Inches((13.333 - lw) / 2), Inches(5.5),
                     width=Inches(lw))

# ================= 2. motivation and problem =================
s = new_slide(title="Motivation and problem")
add_text(s, 0.9, 1.45, 11.6, 0.4, [("Motivation", 17, NAVY, True, False, 0)])
bullets(s, [
 "Understand why teachers leave the profession.",
 "Is there a real policy margin to soften teacher shortages by retaining "
 "teachers — or bringing them back?"], y=2.0, size=16, gap=14)
add_text(s, 0.9, 3.75, 11.6, 0.4, [("Problem", 17, NAVY, True, False, 0)])
bullets(s, [
 "Official microdata on teachers are not publicly available for many countries.",
 "We start with the United States: the country with the most information "
 "available."], y=4.3, size=16, gap=14)

# ================= 3. solution =================
s = new_slide(title="Solution")
add_text(s, 0.9, 1.7, 11.6, 0.5,
         [("Use the Current Population Survey to", 17, INK, False, False, 0)])
bullets(s, [
 "reproduce and extend the official statistics on teachers leaving the "
 "profession;",
 "having achieved A, study in detail how many leave, where they go, and why."],
 y=2.5, size=17, gap=24, numbered=True)

divider("0", "Methodological discussion")

# ================= CPS =================
s = new_slide(title="The Current Population Survey", key="maincps")
bullets(s, [
 "The monthly household survey of the United States, run by the Census "
 "Bureau for the Bureau of Labor Statistics. Nationally representative of "
 "the civilian non-institutional population.",
 "We pool 28 consecutive March supplements, 1998–2025: 5.0 million "
 "person-year records.",
 "104,545 of them are teachers — about 3,700 per year."],
 y=1.6, size=16.5, gap=24)
buttons_row(s, [("unemployment", "appunemp"), ("interviews", "approtation"),
                ("migration", "appmigration"), ("identity", "appidentity")])

# ================= ASEC =================
s = new_slide(title="The March supplement (ASEC)")
bullets(s, [
 "Run by the Census Bureau each March since 1948: the source of the "
 "official annual income, poverty and health-insurance statistics.",
 "About 90,000 households: the March sample plus oversamples interviewed "
 "in February and April.",
 "Every adult reports on the previous calendar year: longest job held, "
 "weeks worked, earnings, benefits."], y=1.7, size=16.5, gap=24)

# ================= codes =================
s = new_slide(title="Identifying a teacher: the census occupation codes",
              key="maincodes")
cols = [(0.9, 3.6, L), (4.7, 2.4, C), (7.3, 2.6, C), (10.1, 2.4, C)]
rows = [
 row(pl(""), pl("1990 classification", True), pl("2002/2010 classification", True),
     pl("2018 classification", True)),
 row(pl(""), pl("surveys 1998–2002", False, MUT),
     pl("surveys 2003–2019", False, MUT),
     pl("surveys 2020–2025", False, MUT)),
 "RULE",
 row(pl("Pre-K and kindergarten"), pl("155"), pl("2300"), pl("2300")),
 row(pl("Elementary (and middle)"), pl("156"), pl("2310"), pl("2310")),
 row(pl("Secondary"), pl("157"), pl("2320"), pl("2320")),
 row(pl("Special education"), pl("158"), pl("2330"), pl("2330")),
 row(pl("Other teachers and instructors"), pl("159"), pl("2340"), pl("2360")),
]
yend = table(s, cols, rows, 1.55, header=False, size=14, rowh=0.46)
add_text(s, 0.9, yend + 0.25, 11.6, 0.8, [
 ("The K–12 block maps one-to-one across the three regimes: the group "
  "is constant over time even where single codes are not.",
  13.5, INK, False, False, 0)])
buttons_row(s, [("traceability", "appcodes")])

# ================= rotation =================
s = new_slide()
scw = 11.53 / 16
add_text(s, 0.9, 2.30, 3.5, 0.35, [("interviewed 4 months", 14, NAVY, True, False, 0)])
add_text(s, 4.9, 2.30, 3.6, 0.35, [("8 months out", 13, MUT, False, True, 0)],
         align=C)
add_text(s, 9.0, 2.30, 3.5, 0.35, [("interviewed 4 months", 14, BURG, True, False, 0)],
         align=R)
for i in range(16):
    x0 = 0.9 + i * scw
    if i < 4:
        cell(s, x0, 2.75, scw, 0.62, NAVY, None, str(i + 1))
    elif i >= 12:
        cell(s, x0, 2.75, scw, 0.62, BURG, None, str(i - 7))
    else:
        cell(s, x0, 2.75, scw, 0.62, None, LGRAYB)
for xi, lab in [(0.9, "Mar"), (0.9 + 3 * scw, "Jun"),
                (0.9 + 12 * scw, "Mar"), (0.9 + 15 * scw, "Jun")]:
    add_text(s, xi, 3.43, scw, 0.3, [(lab, 11, MUT, False, False, 0)], align=C)
add_text(s, 0.9, 3.77, 4 * scw, 0.3, [("year 1", 12, MUT, False, True, 0)], align=C)
add_text(s, 0.9 + 12 * scw, 3.77, 4 * scw, 0.3, [("year 2", 12, MUT, False, True, 0)], align=C)
arrow = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.9 + scw / 2),
                               Inches(4.40), Inches(0.9 + 12.5 * scw), Inches(4.40))
arrow.line.color.rgb = INK; arrow.line.width = Pt(1.4)
add_text(s, 1.5, 4.57, 10.0, 0.4,
         [("the same interview, twelve months later", 14, INK, False, False, 0)],
         align=C)

# ================= two ways =================
s = new_slide(title="Two ways to identify a leaver")
add_text(s, 0.9, 1.55, 5.6, 0.4, [("A. Follow the individual", 16, NAVY, True, False, 0)])
add_text(s, 0.9, 2.15, 5.6, 0.5, [("All months. Links require matching:", 14, INK, False, False, 0)])
add_text(s, 0.9, 2.75, 5.6, 1.8, [
 ("household identifier", 14, INK, False, False, 6),
 ("dwelling identifier", 14, INK, False, False, 6),
 ("person line number", 14, INK, False, False, 10),
 ("validated on sex, race, age +0–2", 13, MUT, False, False, 0)])
add_text(s, 7.0, 1.55, 5.5, 0.4, [("B. Ask about last year", 16, NAVY, True, False, 0)])
add_text(s, 7.0, 2.15, 5.5, 2.2, [
 ("The March supplement, retrospectively.", 14, INK, False, False, 12),
 ("Taught as last year’s longest job, not teaching this March "
  "⇒ left.", 14, INK, False, False, 0)])

# ================= disadvantages =================
s = new_slide(title="Disadvantages of each option", key="maindisadv")
add_text(s, 0.9, 1.5, 5.7, 0.4, [("A. Following individuals", 15.5, NAVY, True, False, 0)])
bullets(s, [
 "Identity is not certain: validation can admit noisy people.",
 "Movers are lost: ~25% of addresses are not found a year later.",
 "Normal household attrition on top.",
 "Strong seasonality in teaching.",
 "Many ways to define the rate (next slide)."],
 y=2.05, size=13.5, gap=10, x=0.9, w=5.7, numbered=True)
add_text(s, 7.0, 1.5, 5.6, 0.4, [("B. Retrospective March", 15.5, NAVY, True, False, 0)])
bullets(s, [
 "Recall bias.",
 "Less sample: one observation per person per year (~3,700 teachers) "
 "against ~11,000 monthly teacher observations.",
 "Only March-to-March transitions; within-year spells are smoothed away."],
 y=2.05, size=13.5, gap=10, x=7.0, w=5.6, numbered=True)
buttons_row(s, [("linkage loss", "applink"), ("attachment", "appgradient"),
                ("validation", "appidentity")])

# ================= six definitions =================
s = new_slide(title="Six ways to define leaving, simplest to strictest")
add_text(s, 0.9, 1.35, 11.6, 0.4,
         [("Unit: the individual. Four interviews in year 1, four in year 2.",
           14, INK, False, False, 0)])
cols = [(0.9, 2.3, L), (3.4, 4.4, L), (8.0, 4.4, L)]
rows = [
 row(pl(""), pl("A teacher:", True), pl("A leaver:", True)),
 "RULE",
 row(pl("Single"), pl("seen teaching in ≥ 1 of the 4 year-1 interviews"),
     pl("seen teaching in none of the 4 year-2 interviews")),
 row(pl("Pair"), pl("seen teaching in ≥ 2 of the 4"),
     pl("seen teaching in none of the 4")),
 row(pl("Triple"), pl("seen teaching in ≥ 3 of the 4"),
     pl("seen teaching in none of the 4")),
 row(pl("Strict"), pl("seen teaching in all 4"),
     pl("seen teaching in none of the 4")),
 row(pl("Month pairs"), pl("each teaching month, on its own"),
     pl("not seen teaching twelve months later")),
 row(pl("Annual recall"), pl("teaching was last year’s longest job"),
     pl("not teaching at the March interview")),
]
table(s, cols, rows, 1.95, header=False, size=13.5, rowh=0.62)

s = new_slide(title="The six, on one axis")
fit_picture(s, f"{FIG}/defs6.png", (0.7, 1.3, 11.9, 5.5))

divider("1", "Leaving rate: how many leave")

s = new_slide(title="Leaving teaching, 1997–2024", key="mainevol")
fit_picture(s, f"{FIG}/g2_evolution.png", (0.7, 1.3, 11.9, 5.3))
buttons_row(s, [("public vs private", "apppubpriv")])
s.notes_slide.notes_text_frame.text = (
 "Estable y similar a otros países OCDE. Promedios EAG para países "
 "con datos: 6,6 (datos 2016, EAG 2021); 6,5 (2022/23, EAG 2025); 6,4 "
 "(2024/25, EAG 2026). Países con series largas (Nueva Zelanda, Suecia, "
 "Israel, Noruega) también estables. La tasa de EE. UU. está por "
 "encima de la mayoría de los países que publican una.")

s = new_slide(title="Comparable professions: who we compare teachers with")
cols = [(0.9, 4.0, L), (5.1, 1.8, R), (7.0, 1.8, R), (8.9, 1.9, R), (10.9, 1.6, R)]
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
yend = table(s, cols, rows, 1.55, header=False, size=14, rowh=0.48)
add_text(s, 0.9, yend + 0.22, 11.6, 0.4,
         [("College graduates, pooled 2015–2024, weighted; wages from 2020–2024.",
           12, MUT, False, True, 0)])

s = new_slide(title="Leaving the occupation, by profession", key="mainprofs")
fit_picture(s, f"{FIG}/leave_professions_deck.png", (0.7, 1.3, 11.9, 5.3))
buttons_row(s, [("more professions", "appprofs")])

divider("2", "Composition: where they go")

s = new_slide(title="Of every 100 leavers (average, 2020–2024)", key="mainflow")
fit_picture(s, f"{FIG}/flow_unified.png", (0.5, 1.15, 12.3, 5.1))
add_text(s, 0.9, 6.42, 11.6, 0.5, [[
 [("Message.  ", 13.5, NAVY, True, False),
  ("A third find another job; a third retire; the rest split between "
   "early labor-force exit and unemployment.", 13.5, INK, False, False)], 0]])
buttons_row(s, [("vs NCES follow-up", "apptfs")])

s = new_slide(title="Where the employed leavers go")
fit_picture(s, f"{FIG}/occ_all_slide.png", (0.3, 1.15, 12.73, 5.9))

s = new_slide(title="What this says for policy")
bullets(s, [
 "Of every 100 leavers, about 36 retire: a margin for delaying exit, not "
 "for return.",
 "29 move to another job — half of them to destinations that do not "
 "require a degree.",
 "11 are unemployed and 24 leave the labor force before 55; about 13% of "
 "the latter are studying.",
 "The retrievable margin is real but bounded: policy competes with "
 "retirement, family time and re-training — not only with other "
 "employers."], y=1.7, size=16, gap=22)

divider("3", "Correlations: why they leave")

s = new_slide(title="Specification", key="maineq")
fit_picture(s, EQ_PNG, (1.1, 1.8, 11.1, 2.2))
add_text(s, 0.9, 4.6, 11.6, 0.5,
         [("Probit; average marginal effects reported. 2018–2024, n = 18,571.",
           14, INK, False, False, 0)])
buttons_row(s, [("LPM", "applpm"), ("logit / probit", "appmodels"),
                ("bounded?", "appbounded"), ("what we observe", "appframework")])
s.notes_slide.notes_text_frame.text = (
 "a: apego al empleo (año completo, tiempo parcial). c: compensación "
 "(pensión, sector público, hogar en el cuartil bajo de ingreso). "
 "f: familia (nacimiento, hijos, estado civil). h: salud (salud declarada, "
 "discapacidad). d: demografía (edad, sexo, raza, educación). "
 "delta_t: efectos de año. La LPM no queda acotada (22% de predichos "
 "por debajo de 0), así que el probit es la especificación "
 "principal; las variantes LPM van en el apéndice.")

s = new_slide(title="What correlates with leaving")
fit_picture(s, f"{FIG}/ame_ext.png", (0.8, 1.15, 11.7, 5.9))

s = new_slide(title="Relative pay since 1997")
fit_picture(s, f"{FIG}/msgA3.png", (0.7, 1.3, 11.9, 5.3))

s = new_slide(title="Leaving, by position in the teacher pay distribution")
fit_picture(s, f"{FIG}/pay3_deciles_deck.png", (0.9, 1.3, 11.5, 5.3))

s = new_slide(title="Pension coverage and leaving, across states")
fit_picture(s, f"{FIG}/pension_scatter_deck.png", (0.9, 1.3, 11.5, 5.3))

s = new_slide(title="Leaving and the cycle")
fit_picture(s, f"{FIG}/cycle1.png", (0.7, 1.3, 11.9, 5.3))

s = new_slide(title="Conclusions")
bullets(s, [
 "A household survey can reproduce the official picture of teacher "
 "attrition — and extend it yearly, with covariates records do not have.",
 "Who leaves: the weakly attached, the low-paid, those without pension "
 "coverage, new mothers, teachers with a disability.",
 "We observe only part of the motives — financial and life-cycle, not "
 "working conditions — so these are margins, not the full story.",
 "What could bring teachers back: flexibility, economic security, pension "
 "coverage, and re-entry paths for those who left to study or care."],
 y=1.6, size=16, gap=22)

# ================= appendix =================
divider("A", "Appendix")

s = new_slide(title="How the CPS measures unemployment", key="appunemp")
bullets(s, [
 "The basic monthly interview measures labor force status in the reference "
 "week — that alone produces the official monthly unemployment rate. "
 "Not the March supplement.",
 "The rest of the survey: monthly labor statistics and topical supplements "
 "(school enrollment in October, voting in November, tobacco, computer use).",
 "The March supplement adds the annual income block: the source of income, "
 "poverty and health-insurance statistics — and of our retrospective "
 "measure."], y=1.6, size=15.5, gap=20)
backbtn(s, "maincps")

s = new_slide(title="Are interviews monthly? Who is new each month?", key="approtation")
add_text(s, 0.9, 1.4, 11.6, 0.6,
         [("Yes: every month, one eighth of the sample sits in each position "
           "of the 4-8-4 rotation. Verified in the microdata:", 14, INK, False, False, 0)])
cols = [(0.9, 2.6, L)] + [(3.6 + i * 1.1, 1.0, R) for i in range(8)]
rows = [
 row(pl("Month in sample", True), *[pl(str(i + 1), True) for i in range(8)]),
 "RULE",
 row(pl("March 2023 (%)"), pl("12.5"), pl("12.9"), pl("12.8"), pl("12.5"),
     pl("12.2"), pl("12.4"), pl("12.3"), pl("12.3")),
 row(pl("July 2023 (%)"), pl("12.3"), pl("12.9"), pl("12.9"), pl("12.5"),
     pl("12.2"), pl("12.2"), pl("12.5"), pl("12.4")),
 row(pl("January 2024 (%)"), pl("12.4"), pl("12.9"), pl("12.9"), pl("13.1"),
     pl("11.9"), pl("12.0"), pl("12.1"), pl("12.6")),
]
yend = table(s, cols, rows, 2.25, header=False, size=13, rowh=0.48)
add_text(s, 0.9, yend + 0.25, 11.6, 0.9, [
 ("Each month: ~12.5% new households, ~37.5% in months 2–4, ~50% "
  "returning in months 5–8. Month-to-month overlap 75%; year-to-year "
  "overlap 50%, by design.", 13.5, INK, False, False, 0)])
backbtn(s, "maincps")

s = new_slide(title="Internal migration in the United States", key="appmigration")
bullets(s, [
 "In 2023, 7.8% of Americans changed residence within the year — 25.6 "
 "million people, the lowest rate on record.",
 "3.2% moved to a different county; 1.4% to a different state.",
 "This is the loss channel of any address-based panel: linkage follows "
 "dwellings, not people."], y=1.7, size=15.5, gap=22)
add_text(s, 0.9, 5.3, 11.6, 0.4,
         [("Census Bureau, CPS ASEC, historical table A-1 (1948–2023).",
           12, MUT, False, True, 0)])
backbtn(s, "maincps")

s = new_slide(title="Is the same person validated year to year?", key="appidentity")
bullets(s, [
 "In the field, yes: the interviewer carries the household roster forward, "
 "each member keeps a line number, and occupation uses dependent "
 "interviewing between consecutive months.",
 "The public files carry no person identifier. We reconstruct the roster: "
 "household id + dwelling id + line number, validated on sex, race, and "
 "age advancing 0–2 years.",
 "Validation is not watertight: a mover replaced by someone of the same "
 "sex and similar age can slip through."], y=1.6, size=15.5, gap=20)
backbtn(s, "maindisadv")

s = new_slide(title="How much is lost in linking, and who", key="applink")
bullets(s, [
 "Of the addresses due to return twelve months later, 74.5% are found "
 "again (March 2023 → March 2024); the missing quarter is moves plus "
 "household non-response.",
 "Teachers link more than others, not less: ~80% of teacher observations "
 "vs ~76% of other college graduates.",
 "The loss is still selective: movers leave teaching more, so panel "
 "measures are lower bounds on mobility-related exit."],
 y=1.6, size=15.5, gap=20)
backbtn(s, "maindisadv")

s = new_slide(title="Attachment: seen once, gone", key="appgradient")
fit_picture(s, f"{FIG}/sighting_gradient.png", (1.2, 1.2, 10.9, 4.9))
add_text(s, 0.9, 6.3, 11.6, 0.6, [
 ("Of teachers seen teaching in a single year-1 interview, 54% are never "
  "seen teaching in their year-2 interviews; 10% of those seen in all "
  "four. Summer-only patterns are just 3% of these leavers.",
  12.5, MUT, False, False, 0)])
backbtn(s, "maindisadv")

s = new_slide(title="Public vs private schools", key="apppubpriv")
fit_picture(s, f"{FIG}/pubpriv_series.png", (0.8, 1.25, 11.7, 5.5))
backbtn(s, "mainevol")

s = new_slide(title="More professions, and their average", key="appprofs")
fit_picture(s, f"{FIG}/profs_ext.png", (0.8, 1.25, 11.7, 5.5))
backbtn(s, "mainprofs")

s = new_slide(title="Our destinations vs the NCES follow-up survey", key="apptfs")
cols = [(0.9, 5.4, L), (6.5, 2.6, R), (9.3, 2.6, R)]
rows = [
 row(pl("Of every 100 leavers…"), pl("CPS, 2020–2024", True),
     pl("TFS, 2021–22", True)),
 "RULE",
 row(pl("Working in another job"), pl("28.8"), pl("57.2")),
 row(pl("   of which outside education"), pl("—"), pl("11.8")),
 row(pl("Retired / out of the LF, 55+"), pl("36.4"), pl("27.7")),
 row(pl("Out of the LF, under 55"), pl("23.7"), pl("10.1 *")),
 row(pl("Unemployed"), pl("11.1"), pl("4.8")),
]
yend = table(s, cols, rows, 1.6, header=False, size=14, rowh=0.5)
add_text(s, 0.9, yend + 0.22, 11.6, 1.2, [
 ("* Caring for family 5.6 + student 1.8 + disabled 0.3 + other 2.4. TFS "
  "covers regular classroom teachers in public schools and counts K–12 "
  "non-teaching jobs (39.3) as work; our occupation-based measure spans "
  "public and private and all teaching attachment. Sources: NCES 2024-039, "
  "table A-8 and NTPS estimate tables.", 11.5, MUT, False, True, 0)])
backbtn(s, "mainflow")

s = new_slide(title="Is the teacher group constant across code changes?", key="appcodes")
bullets(s, [
 "The five-code K–12 block maps one-to-one across the 1990, 2002/2010 "
 "and 2018 classifications; we always use the block, never a single code "
 "across regimes.",
 "Evidence: re-computing the whole series on the narrow core (dropping "
 "special education and other teachers) moves the pooled rate from 8.67 "
 "to 8.57 — a 0.1 point change.",
 "The 2003 and 2020 reclassifications leave no visible break in the series."],
 y=1.6, size=15.5, gap=20)
backbtn(s, "maincodes")

s = new_slide(title="Linear probability model, fixed-effects variants", key="applpm")
cols = [(0.9, 4.2, L), (5.3, 2.3, R), (7.8, 2.3, R), (10.2, 2.4, R)]
rows = [
 row(pl(""), pl("Year FE", True), pl("No FE", True), pl("State + year FE", True)),
 "RULE",
 row(pl("Worked full year"), pl("−11.6 (0.7)"), pl("−11.5 (0.7)"), pl("−11.7 (0.7)")),
 row(pl("Part-time"), pl("+8.7 (1.1)"), pl("+8.7 (1.1)"), pl("+8.6 (1.1)")),
 row(pl("Employer pension plan"), pl("−2.3 (0.5)"), pl("−2.4 (0.5)"), pl("−2.3 (0.5)")),
 row(pl("Public sector"), pl("−2.4 (0.6)"), pl("−2.4 (0.6)"), pl("−2.4 (0.6)")),
 row(pl("New baby"), pl("+5.6 (1.6)"), pl("+5.7 (1.6)"), pl("+5.7 (1.6)")),
 row(pl("With a disability"), pl("+8.9 (2.1)"), pl("+8.9 (2.1)"), pl("+8.9 (2.1)")),
 row(pl("Bottom-quartile income"), pl("+4.1 (1.2)"), pl("+4.2 (1.2)"), pl("+4.0 (1.2)")),
]
yend = table(s, cols, rows, 1.55, header=False, size=13.5, rowh=0.47)
add_text(s, 0.9, yend + 0.2, 11.6, 0.6,
         [("Coefficients × 100, robust SE in parentheses. 2018–2024, "
           "n = 18,571. Full set of controls as in the main specification.",
           11.5, MUT, False, True, 0)])
backbtn(s, "maineq")

s = new_slide(title="LPM vs logit vs probit", key="appmodels")
cols = [(0.9, 4.2, L), (5.3, 2.2, R), (7.7, 2.2, R), (10.1, 2.2, R)]
rows = [
 row(pl(""), pl("LPM", True), pl("Logit AME", True), pl("Probit AME", True)),
 "RULE",
 row(pl("Worked full year"), pl("−11.6"), pl("−11.0"), pl("−10.8")),
 row(pl("Part-time"), pl("+8.7"), pl("+4.4"), pl("+5.0")),
 row(pl("Employer pension plan"), pl("−2.3"), pl("−2.3"), pl("−2.4")),
 row(pl("Public sector"), pl("−2.4"), pl("−2.6"), pl("−2.6")),
 row(pl("New baby"), pl("+5.6"), pl("+6.1"), pl("+5.6")),
 row(pl("With a disability"), pl("+8.9"), pl("+5.3"), pl("+5.9")),
 row(pl("Bottom-quartile income"), pl("+4.1"), pl("+2.4"), pl("+2.6")),
]
yend = table(s, cols, rows, 1.55, header=False, size=13.5, rowh=0.47)
add_text(s, 0.9, yend + 0.2, 11.6, 0.6,
         [("Percentage points. Same specification and sample throughout. The "
           "ranking and significance of every margin is unchanged across "
           "estimators.", 11.5, MUT, False, True, 0)])
backbtn(s, "maineq")

s = new_slide(title="Is the LPM bounded between 0 and 1?", key="appbounded")
fit_picture(s, f"{FIG}/lpm_check.png", (1.3, 1.25, 10.7, 4.9))
add_text(s, 0.9, 6.35, 11.6, 0.5, [
 ("No: 22% of fitted values fall below zero. By that check, the probit is "
  "the main specification and the LPM a robustness variant.",
  12.5, MUT, False, False, 0)])
backbtn(s, "maineq")

s = new_slide(title="What the CPS observes, of why teachers leave", key="appframework")
cols = [(0.9, 7.6, L), (8.7, 3.2, L)]
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
table(s, cols, rows, 1.6, header=False, size=14.5, rowh=0.5)
backbtn(s, "maineq")

# ---- wire the buttons ----
for sh, key in BTNS:
    sh.click_action.target_slide = REG[key]

prs.save(OUT)
print(f"saved {OUT} with {len(prs.slides._sldIdLst)} slides")
