"""Native, editable PPTX mirror of the Data Cluster Beamer deck.
Metropolis look: cream background, slate text, orange accent rule under
titles, dark standout section dividers. Short, telegraphic slide text.
Writes report/data_cluster/Proyect_US_cluster.pptx. Run from the repo root."""
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
EQ_PNG = os.environ.get("EQ_PNG", "report/data_cluster/equation.png")

FONT = "Segoe UI"
INK = RGBColor(0x23, 0x37, 0x3B)      # slate
MUT = RGBColor(0x6B, 0x74, 0x80)
NAVY = RGBColor(0x1F, 0x38, 0x64)     # data color (diagram)
BURG = RGBColor(0x7B, 0x25, 0x30)
LGRAYB = RGBColor(0xC9, 0xCF, 0xD6)
SLATE = RGBColor(0x23, 0x37, 0x3B)
ACCENT = RGBColor(0xEB, 0x81, 0x1B)
CREAM = RGBColor(0xFA, 0xFA, 0xFA)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
PAGENO = [0]

def new_slide(title=None, number=True, bg=None):
    s = prs.slides.add_slide(blank)
    PAGENO[0] += 1
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg if bg else CREAM
    if title:
        box = s.shapes.add_textbox(Inches(0.6), Inches(0.34), Inches(12.2),
                                   Inches(0.55))
        tf = box.text_frame; tf.word_wrap = True; tf.auto_size = None
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = title
        r.font.name = FONT; r.font.size = Pt(21); r.font.bold = False
        r.font.color.rgb = SLATE
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6),
                                 Inches(0.94), Inches(12.2), Inches(0.028))
        bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT
        bar.line.fill.background(); bar.shadow.inherit = False
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

def bullets(s, items, y=1.75, size=17, gap=26, x=0.9, w=11.6):
    parts = []
    for i, it in enumerate(items):
        after = gap if i < len(items) - 1 else 0
        parts.append([[("▸   ", size, ACCENT, True, False),
                       (it, size, INK, False, False)], after])
    return add_text(s, x, y, w, 5.3, parts, spacing=1.4)

def rule(s, x, y, w, weight=1.0, color=INK):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                Inches(x + w), Inches(y))
    ln.line.color.rgb = color; ln.line.width = Pt(weight)
    return ln

def fit_picture(s, path, box):
    bx, by, bw, bh = box
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(bw / iw, bh / ih)
    w, h = iw * scale, ih * scale
    s.shapes.add_picture(path, Inches(bx + (bw - w) / 2),
                         Inches(by + (bh - h) / 2), width=Inches(w))

def msg_policy(s, msg, pol, y=6.35):
    add_text(s, 0.9, y, 11.8, 0.45, [[
        [("Message.  ", 14, ACCENT, True, False), (msg, 14, INK, False, False)], 0]])
    add_text(s, 0.9, y + 0.46, 11.8, 0.45, [[
        [("Policy.  ", 14, SLATE, True, False), (pol, 14, INK, False, False)], 0]])

def divider(num, title):
    s = new_slide(number=False, bg=SLATE)
    add_text(s, 1.0, 2.55, 11.33, 1.2, [(num, 54, ACCENT, True, False, 0)],
             align=PP_ALIGN.CENTER)
    add_text(s, 1.0, 4.05, 11.33, 0.6, [(title, 24, CREAM, False, False, 0)],
             align=PP_ALIGN.CENTER)
    return s

def chart_slide(title, png, msg, pol, box=(0.6, 1.25, 12.1, 4.9)):
    s = new_slide(title=title)
    fit_picture(s, f"{FIG}/{png}", box)
    msg_policy(s, msg, pol)
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

# ================= 1. title =================
s = new_slide(number=False)
add_text(s, 1.2, 2.05, 10.93, 1.6, [
 ("Measuring Teacher Attrition with Labour Force Survey Data", 30, SLATE, False, False, 6),
 ("The Case of the United States", 19, MUT, False, False, 0)], align=PP_ALIGN.CENTER)
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.17), Inches(3.78),
                         Inches(3.0), Inches(0.035))
bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT
bar.line.fill.background(); bar.shadow.inherit = False
add_text(s, 1.2, 4.10, 10.93, 0.5,
         [("José Elías Durán Roa", 16, INK, False, False, 0)],
         align=PP_ALIGN.CENTER)
add_text(s, 1.2, 4.65, 10.93, 0.4,
         [("Data Cluster · Directorate for Education and Skills", 12.5, MUT, False, False, 0)],
         align=PP_ALIGN.CENTER)
with Image.open(LOGO) as im:
    lw = 1.8
s.shapes.add_picture(LOGO, Inches((13.333 - lw) / 2), Inches(5.55),
                     width=Inches(lw))

# ================= 2. why =================
s = new_slide(title="Why this project")
bullets(s, [
 "We study the decision to leave teaching. That needs each person’s "
 "leave-or-stay outcome, plus covariates.",
 "Administrative records count best — but access is hard, coverage is "
 "partial, covariates are few.",
 "So we build the outcome from a household survey. This talk is about "
 "doing that carefully."], y=1.95, gap=30)

# ================= 3. contribution =================
s = new_slide(title="Contribution")
C = [("1.  A user’s guide  ",
      "to building a leaving rate from a survey: each choice, each error, "
      "each effect on the number."),
     ("2.  An implementation  ",
      "on 28 years of the CPS, checked against the NCES reference."),
     ("3.  The substance:  ",
      "who leaves, and what correlates with it.")]
y = 2.0
for lead, body in C:
    add_text(s, 0.9, y, 11.6, 1.2, [[
        [(lead, 17, ACCENT, True, False), (body, 17, INK, False, False)], 0]],
        spacing=1.4)
    y += 1.5

divider("1", "The data")

# ================= 4. official numbers =================
s = new_slide(title="Where do the official numbers come from?")
bullets(s, [
 "National reference: the NCES Teacher Follow-up Survey. Itself a survey. "
 "Eight waves since 1988.",
 "Administrative data: state by state, public sector, and they measure "
 "system exit, not profession exit.",
 "No national administrative count exists."], y=1.95, gap=30)

# ================= 5. comparison table =================
s = new_slide(title="The CPS replicates the official picture, every year")
TX = [0.9, 4.7, 8.1, 10.5]
TW = [3.7, 3.1, 2.3, 2.0]
rule(s, 0.9, 1.42, 11.53, 1.4)
for x, w, htxt in zip(TX[1:], TW[1:], ["CPS", "NTPS", "Difference"]):
    add_text(s, x, 1.52, w, 0.35, [(htxt, 14, INK, True, False, 0)],
             align=PP_ALIGN.RIGHT)
rule(s, 0.9, 1.94, 11.53, 0.75)
def trow(y, lab, a, b, d, bold=False, color=INK):
    add_text(s, TX[0], y, TW[0], 0.35, [(lab, 13.5, INK, bold, False, 0)])
    for x, w, v, c in zip(TX[1:], TW[1:], [a, b, d], [color, INK, INK]):
        if v:
            add_text(s, x, y, w, 0.35, [(v, 13.5, c, bold, False, 0)],
                     align=PP_ALIGN.RIGHT)
trow(2.06, "Measurement", "every year, 1997–2024", "occasional waves", "",
     bold=True, color=ACCENT)
rule(s, 0.9, 2.50, 11.53, 0.75)
add_text(s, TX[0], 2.58, 8.0, 0.3,
         [("Example wave: 2020–21, the latest NTPS", 11.5, MUT, False, True, 0)])
trow(2.96, "Female (%)", "75.5", "76.8", "−1.3")
trow(3.38, "Master’s degree or higher (%)", "57.0", "61.0", "−4.0 ***")
trow(3.80, "Average age (years)", "44.0", "42.9", "+1.1 ***")
rule(s, 0.9, 4.24, 11.53, 0.75)
trow(4.34, "Teachers observed in the wave", "3,855", "39,633", "")
rule(s, 0.9, 4.76, 11.53, 1.4)
add_text(s, 0.9, 4.96, 11.53, 0.6, [
 ("Public school teachers, weighted. Stars test the CPS mean against the NTPS "
  "estimate: *** p<0.001. Sources: NCES 2022-113, Digest 209.10, NCES 2024-024.",
  11.5, MUT, False, True, 0)])
add_text(s, 0.9, 5.95, 11.53, 0.8, [[
 [("Full sample:  ", 14, INK, False, False),
  ("5.0 million", 14, SLATE, True, False),
  (" records,  ", 14, INK, False, False),
  ("104,545", 14, SLATE, True, False),
  (" teacher observations,  ", 14, INK, False, False),
  ("48,842", 14, SLATE, True, False),
  (" teachers in the linked panel.", 14, INK, False, False)], 0]])

# ================= 6. rotation diagram =================
s = new_slide()
scw = 11.53 / 16
add_text(s, 0.9, 2.35, 3.5, 0.35, [("interviewed 4 months", 14, NAVY, True, False, 0)])
add_text(s, 4.9, 2.35, 3.6, 0.35, [("8 months out", 13, MUT, False, True, 0)],
         align=PP_ALIGN.CENTER)
add_text(s, 9.0, 2.35, 3.5, 0.35, [("interviewed 4 months", 14, BURG, True, False, 0)],
         align=PP_ALIGN.RIGHT)
for i in range(16):
    x0 = 0.9 + i * scw
    if i < 4:
        cell(s, x0, 2.80, scw, 0.62, NAVY, None, str(i + 1))
    elif i >= 12:
        cell(s, x0, 2.80, scw, 0.62, BURG, None, str(i - 7))
    else:
        cell(s, x0, 2.80, scw, 0.62, None, LGRAYB)
for xi, lab in [(0.9, "Mar"), (0.9 + 3 * scw, "Jun"),
                (0.9 + 12 * scw, "Mar"), (0.9 + 15 * scw, "Jun")]:
    add_text(s, xi, 3.48, scw, 0.3, [(lab, 11, MUT, False, False, 0)],
             align=PP_ALIGN.CENTER)
add_text(s, 0.9, 3.82, 4 * scw, 0.3, [("year 1", 12, MUT, False, True, 0)],
         align=PP_ALIGN.CENTER)
add_text(s, 0.9 + 12 * scw, 3.82, 4 * scw, 0.3, [("year 2", 12, MUT, False, True, 0)],
         align=PP_ALIGN.CENTER)
arrow = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.9 + scw / 2),
                               Inches(4.45), Inches(0.9 + 12.5 * scw), Inches(4.45))
arrow.line.color.rgb = INK; arrow.line.width = Pt(1.4)
add_text(s, 1.5, 4.62, 10.0, 0.4,
         [("the same interview, twelve months later", 14, INK, False, False, 0)],
         align=PP_ALIGN.CENTER)

# ================= 7. codes =================
s = new_slide()
fit_picture(s, f"{FIG}/codes_slide.png", (0.3, 0.2, 12.73, 6.9))

divider("2", "Measuring the leaving rate")

# ================= 8. two ways =================
s = new_slide(title="Two ways to measure it")
add_text(s, 0.9, 1.55, 5.6, 0.4, [("Follow the person", 16, ACCENT, True, False, 0)])
add_text(s, 0.9, 2.15, 5.6, 0.8, [
 ("No person identifier in the CPS. We link on:", 14.5, INK, False, False, 0)])
add_text(s, 0.9, 2.85, 5.6, 1.8, [
 ("household identifier", 14.5, INK, False, False, 6),
 ("dwelling identifier", 14.5, INK, False, False, 6),
 ("person line number", 14.5, INK, False, False, 10),
 ("checked: sex, race, age +0–2", 13, MUT, False, False, 0)])
add_text(s, 7.0, 1.55, 5.5, 0.4, [("Ask about last year", 16, ACCENT, True, False, 0)])
add_text(s, 7.0, 2.15, 5.5, 2.6, [
 ("Each March, the supplement asks about the previous calendar year: "
  "longest job, weeks, earnings.", 14.5, INK, False, False, 12),
 ("Taught last year, not teaching now ⇒ left.", 14.5, INK, False, False, 12),
 ("The measure used in the literature.", 13, MUT, False, False, 0)])

# ================= 9. four definitions =================
s = new_slide(title="Four definitions, one language")
add_text(s, 0.9, 1.30, 11.6, 0.4,
         [("Four interviews in year 1, four in year 2, twelve months apart.",
           15, INK, False, False, 0)])
DC = [(0.9, 2.6), (3.9, 4.0), (8.3, 4.2)]
rule(s, 0.9, 1.95, 11.6, 1.4)
for (x, w), htxt in zip(DC, ["", "A teacher:", "A leaver:"]):
    if htxt:
        add_text(s, x, 2.05, w, 0.35, [(htxt, 15, INK, True, False, 0)])
rule(s, 0.9, 2.48, 11.6, 0.75)
DROWS = [
 ("Any sighting", False,
  "seen teaching in ≥ 1 of the 4 year-1 interviews",
  "seen teaching in none of the 4 year-2 interviews"),
 ("Month pairs", False,
  "each teaching interview counts on its own",
  "not seen teaching twelve months later"),
 ("Panel (benchmark)", True,
  "seen teaching in ≥ 2 of the 4 year-1 interviews",
  "seen teaching in none of the 4 year-2 interviews *"),
 ("Annual recall", False,
  "teaching was the longest job of last year",
  "not teaching at the March interview"),
]
y = 2.64
for m, bench, a, b in DROWS:
    add_text(s, DC[0][0], y, DC[0][1], 0.7,
             [(m, 15, ACCENT if bench else INK, bench, False, 0)])
    add_text(s, DC[1][0], y, DC[1][1], 0.7, [(a, 15, INK, False, False, 0)])
    add_text(s, DC[2][0], y, DC[2][1], 0.7, [(b, 15, INK, False, False, 0)])
    y += 0.78
rule(s, 0.9, y + 0.02, 11.6, 1.4)
add_text(s, 0.9, y + 0.20, 11.6, 0.6,
         [("* At least two year-2 interviews, one outside the summer.  "
           "Annual recall is the only one not built by counting interviews.",
           12.5, MUT, False, True, 0)])

# ================= 10. all series =================
s = chart_slide("One dataset, one rate per definition", "v_allseries.png",
 "The definition moves the rate by a factor of four.",
 "Fix the definition before comparing studies.",
 box=(0.6, 1.20, 12.1, 4.70))
add_text(s, 0.9, 7.10, 11.6, 0.35, [
 ("Recall: ≈3,700 teachers per year. Panel: ≈2,500. Dots: NCES follow-up.",
  11.5, MUT, False, True, 0)])
s.notes_slide.notes_text_frame.text = (
 "GUION. En este gráfico veis cuatro líneas y unos puntos. Cada línea es una "
 "forma distinta de medir lo mismo, calculada sobre los mismos registros del CPS, de la "
 "menos estricta a la más precisa. Los puntos son la referencia nacional, el Teacher "
 "Follow-up Survey del NCES (8,0 en su última ola).\n\n"
 "ANY SIGHTING (~18): entra cualquiera visto enseñando en una sola entrevista del "
 "año 1. Más del doble de la referencia por tres causas: (1) dominante, a quién "
 "deja entrar un solo avistamiento — sustitutos y spells de un mes. Ojo con el dato: "
 "de los vistos enseñando en UNA sola entrevista del año 1, el 55% no aparece "
 "enseñando en NINGUNA de sus entrevistas del año 2 (no significa 'nunca más': "
 "el CPS solo los ve 16 meses). El gradiente: una vez 55%, dos 30%, tres 17%, cuatro 11%. "
 "(2) Un solo mes de código de ocupación es ruidoso. (3) La estacionalidad pesa "
 "poco: solo-verano es ~3% de estos leavers.\n\n"
 "MONTH PAIRS (~15): la unidad es el par mes-mes+12, no la persona; la misma persona puede "
 "contar como leaver en un par y stayer en otro. La caída de tres puntos hasta la "
 "siguiente línea es lo que se gana imponiendo un veredicto por persona.\n\n"
 "PANEL (~13): una persona, un veredicto (profesor si enseña en 2+ entrevistas del "
 "año 1; leaver solo si nunca enseña en el año 2, con 2+ entrevistas, una "
 "fuera del verano). Queda 4-5 puntos sobre el recall por dos razones: (1) concepto de "
 "año puntual — quien enseñó casi todo el año pero no en esas "
 "entrevistas cuenta como leaver; (2) retornos — uno de cada seis leavers del panel "
 "vuelve a enseñar en tres meses; la medida anual los absorbe.\n\n"
 "ANNUAL RECALL (8,6): empleo más largo del año anterior y ya no enseña en "
 "marzo. Comparte concepto con la encuesta oficial (empleo principal del año) y por "
 "eso aterriza junto a los puntos. Su riesgo propio: error de recuerdo.\n\n"
 "EJE: el recall empieza en 1997 (suplementos armonizados desde 1998); las líneas de "
 "panel empiezan en 2005 porque el identificador de hogar solo es único desde mayo de "
 "2004.\n\n"
 "CIERRE: ninguna línea es 'la correcta'; cada construcción responde a una "
 "pregunta distinta. Si construyes tu variable de abandono desde una encuesta porque el "
 "registro administrativo no es accesible, debes saber qué elección tomas y "
 "qué le hace a tu número.")

# ================= 11. why the lines differ =================
s = new_slide(title="Why the lines differ")
GAPS = [
 ("18.2", "Any sighting.  ", "Lets in substitutes and one-month spells."),
 ("15.4", "Month pairs.  ", "Counts the same person several times."),
 ("13.0", "Panel.  ",
  "One verdict per person — but one leaver in six is back within "
  "three months."),
 ("8.6", "Annual recall.  ", "The official concept: the year’s main job."),
 ("8.0", "NCES follow-up.  ", "The reference."),
]
y = 1.70
for num, lead, body in GAPS:
    add_text(s, 0.9, y, 1.0, 0.4, [(num, 16, ACCENT, True, False, 0)],
             align=PP_ALIGN.RIGHT)
    add_text(s, 2.15, y, 10.3, 0.6, [[
        [(lead, 15, SLATE, True, False), (body, 15, INK, False, False)], 0]],
        spacing=1.25)
    y += 0.92
add_text(s, 0.9, y + 0.15, 11.6, 0.35,
         [("The choice, not the data, drives the spread.", 12.5, MUT, False, True, 0)])

# ================= 12. gradient =================
s = new_slide(title="Seen once, gone")
fit_picture(s, f"{FIG}/sighting_gradient.png", (0.9, 1.15, 11.5, 4.65))
add_text(s, 0.9, 6.05, 11.8, 0.45, [[
 [("Message.  ", 14, ACCENT, True, False),
  ("Seen teaching once: 54 percent not seen teaching a year later. Seen "
   "four times: 10.", 14, INK, False, False)], 0]])
add_text(s, 0.9, 6.60, 11.8, 0.45, [[
 [("Caveat.  ", 14, SLATE, True, False),
  ("Linkage follows addresses: movers drop out, and movers leave more.",
   14, INK, False, False)], 0]])

divider("3", "What the data show")

# ================= 13. framework =================
s = new_slide(title="Why teachers leave: what the CPS sees")
rule(s, 0.9, 1.60, 11.53, 1.4)
add_text(s, 1.1, 1.72, 7.0, 0.35, [("Reasons in the literature", 15, INK, True, False, 0)])
add_text(s, 9.3, 1.72, 3.0, 0.35, [("In the CPS?", 15, INK, True, False, 0)])
rule(s, 0.9, 2.16, 11.53, 0.75)
FROWS = [("Working conditions", "no"),
         ("Organizational support", "no"),
         ("Autonomy and intrinsic motives", "no"),
         ("Financial factors", "yes"),
         ("Personal life-cycle motives", "yes")]
y = 2.32
for lab, v in FROWS:
    add_text(s, 1.1, y, 7.6, 0.35, [(lab, 15, INK, False, False, 0)])
    add_text(s, 9.3, y, 3.0, 0.35,
             [(v, 15, ACCENT if v == "yes" else MUT, v == "yes", False, 0)])
    y += 0.52
rule(s, 0.9, y + 0.02, 11.53, 0.75)
add_text(s, 1.1, y + 0.14, 7.6, 0.35, [("Sociodemographics", 15, INK, False, False, 0)])
add_text(s, 9.3, y + 0.14, 3.0, 0.35, [("yes", 15, ACCENT, True, False, 0)])
rule(s, 0.9, y + 0.62, 11.53, 1.4)

# ================= 14. five messages =================
s = new_slide(title="Five messages")
FM = [
 "Economics beats demographics.",
 "Exits concentrate among part-time, part-year, low-paid teachers.",
 "Those exits leave employment — not for better jobs.",
 "A birth is the largest single trigger.",
 "Pensions retain, and states differ widely.",
]
y = 1.85
for i, m in enumerate(FM, 1):
    add_text(s, 0.9, y, 11.6, 0.8, [[
        [(f"{i}.  ", 17, ACCENT, True, False), (m, 17, INK, False, False)], 0]],
        spacing=1.3)
    y += 0.95

# ================= 15+. charts =================
RUN = [
 ("Leaving teaching, 1997–2024", "g2_evolution.png",
  "Flat around 8.6 since 1997.", "A steady cost, not an emergency."),
 ("Teachers next to comparable professions", "leave_professions_deck.png",
  "Teachers are no outlier.", "Benchmarks temper alarm."),
 ("Destinations, 2024", "g3_flow100_2024.png",
  "A third find another job; most leave employment.",
  "The rival is retirement and care, not other employers."),
 ("Who leaves the labor force before 55", "yellow_flow2024.png",
  "Half of the early exits are mothers.",
  "Childcare policy is retention policy."),
 ("By age and route", "g4_routes_age.png",
  "U-shaped in age; non-employment at both ends.",
  "Different exits, different instruments."),
 ("EQUATION", None, None, None),
 ("What correlates with leaving", "ame_seminar.png",
  "Attachment and compensation dominate.", "The levers are contractual."),
 ("A new baby, by profession", "g8_newbaby.png",
  "A birth adds 5.9 points — the most of any profession.",
  "Parental leave targets the largest trigger."),
 ("Across states", "states_level.png",
  "From 4 to 13 percent across states.", "State institutions are first-order."),
 ("Relative pay since 1997", "msgA3.png",
  "Teacher pay fell 4 percent; other graduates gained.",
  "A stock, not a shock."),
 ("By position in the pay distribution", "pay3_deciles_deck.png",
  "Exits pile up in the lowest deciles.", "Stabilize the bottom."),
 ("Pension coverage, across states", "pension_scatter_deck.png",
  "More coverage, fewer leavers.", "Pension design retains."),
]
for title, png, msg, pol in RUN:
    if title == "EQUATION":
        s = new_slide(title="The econometric specification")
        fit_picture(s, EQ_PNG, (1.2, 1.5, 10.9, 2.3))
        bullets(s, [
         "Probit, 2015–2024, year effects, n = 28,900. AMEs in points.",
         "Robust: logit, LPM, state and year FE, full window, "
         "occupation-pair definition."], y=4.45, size=15, gap=14)
    else:
        chart_slide(title, png, msg, pol)

# ================= conclusion =================
s = new_slide(title="Conclusion")
bullets(s, [
 "A labour force survey measures attrition yearly — and matches the "
 "official picture.",
 "The definition is first-order: 5 to 19 percent from the same records.",
 "Attachment, pay, pensions and births drive exits. And the design "
 "travels to any LFS."], y=1.95, gap=30)

prs.save(OUT)
print(f"saved {OUT} with {len(prs.slides._sldIdLst)} slides")
