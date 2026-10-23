"""The policy version of the deck, built to match the author's clean
deck (titles and key messages taken from it verbatim). Two methodology
slides (the CPS in numbers; who counts as a leaver), the results block
with section dividers, the author's Policy options
slides, and a closing open-questions slide. Thirteen content slides, all visual. Reuses the figures in
report/data_cluster/_pngx. Writes report/data_cluster/Proyect_US_policy.pptx.
Run from the repo root."""
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

OUT = "report/data_cluster/Proyect_US_policy.pptx"
FIG = "report/data_cluster/_pngx"
LOGO = "report/data_cluster/oecd_logo.png"
FONT = "Garamond"
INK = RGBColor(0x21, 0x25, 0x29)
MUT = RGBColor(0x6B, 0x74, 0x80)
NAVY = RGBColor(0x10, 0x2D, 0x5E)
ACC = RGBColor(0x2D, 0x6C, 0xB5)
BURG = RGBColor(0x8F, 0x2B, 0x36)
BAND = RGBColor(0xEC, 0xF2, 0xF9)
GREEN = RGBColor(0x2E, 0x7D, 0x32)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C = PP_ALIGN.CENTER

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
PAGENO = [0]

def new_slide(title=None, number=True):
    s = prs.slides.add_slide(blank)
    PAGENO[0] += 1
    if title:
        box = s.shapes.add_textbox(Inches(0.55), Inches(0.24), Inches(12.3),
                                   Inches(0.62))
        tf = box.text_frame; tf.word_wrap = True; tf.auto_size = None
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        r = tf.paragraphs[0].add_run(); r.text = title
        r.font.name = FONT; r.font.size = Pt(28); r.font.bold = True
        r.font.color.rgb = NAVY
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

def message(s, text, y=6.22, size=16, lead="Key message."):
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(y - 0.14),
                              prs.slide_width, Inches(1.05))
    band.fill.solid(); band.fill.fore_color.rgb = BAND
    band.line.fill.background(); band.shadow.inherit = False
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55),
                             Inches(y - 0.02), Inches(0.08), Inches(0.78))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background(); bar.shadow.inherit = False
    add_text(s, 0.9, y, 11.8, 0.9, [[
        [(lead + "  ", size + 1, NAVY, True, False),
         (text, size + 1, NAVY, False, False)], 0]])

def bullets(s, items, y=1.55, size=19, gap=22, x=0.9, w=11.8):
    parts = []
    for i, it in enumerate(items):
        after = gap if i < len(items) - 1 else 0
        if isinstance(it, tuple):
            lead, rest = it
            parts.append([[("▪  ", size, ACC, True, False),
                           (lead + "  ", size, NAVY, True, False),
                           (rest, size, INK, False, False)], after])
        else:
            parts.append([[("▪  ", size, ACC, True, False),
                           (it, size, INK, False, False)], after])
    return add_text(s, x, y, w, 5.6, parts, spacing=1.28)

def chart(s, name, box=(0.7, 1.25, 11.9, 4.85)):
    path = f"{FIG}/{name}.png"
    x, y, w, h = box
    iw, ih = Image.open(path).size
    sc = min(w / iw, h / ih)
    pw, ph = iw * sc, ih * sc
    s.shapes.add_picture(path, Inches(x + (w - pw) / 2),
                         Inches(y + (h - ph) / 2),
                         width=Inches(pw), height=Inches(ph))

def divider(num, title, question=None):
    s = prs.slides.add_slide(blank)
    PAGENO[0] += 1
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width,
                            prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background(); bg.shadow.inherit = False
    add_text(s, 1.0, 2.45, 11.33, 1.3,
             [(num, 60, WHITE, True, False, 0)], align=C)
    add_text(s, 1.0, 4.05, 11.33, 0.8,
             [(title, 28, RGBColor(0xD7, 0xE3, 0xF2), False, False, 0)],
             align=C)
    if question:
        add_text(s, 1.5, 5.35, 10.33, 0.8,
                 [(question, 18, RGBColor(0xBE, 0xD3, 0xEE), False, True,
                   0)], align=C)
    return s

def arrow_to(s, x_tip, y_tip, x_tail, y_tail, color, w=1.6):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x_tip),
                               Inches(y_tip), Inches(x_tail), Inches(y_tail))
    c.line.color.rgb = color; c.line.width = Pt(w)
    ln = c.line._get_or_add_ln()
    he = ln.makeelement(qn("a:headEnd"), {"type": "triangle"})
    ln.append(he)
    return c

# ================= 1. title =================
s = prs.slides.add_slide(blank)
PAGENO[0] += 1
band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.55),
                          prs.slide_width, Inches(2.50))
band.fill.solid(); band.fill.fore_color.rgb = NAVY
band.line.fill.background(); band.shadow.inherit = False
add_text(s, 0.33, 2.30, 12.67, 1.5, [
 ("Measuring Teacher Attrition Beyond Administrative Data", 32, WHITE,
  True, False, 4),
 ("The case of the United States", 32, RGBColor(0xD7, 0xE3, 0xF2), False,
  False, 0)], align=C, spacing=1.12)
add_text(s, 1.00, 4.62, 11.33, 0.8, [
 ("José Elías Durán Roa", 20, INK, True, False, 2),
 ("José Manuel Torres", 20, INK, True, False, 0)], align=C,
 spacing=1.15)
add_text(s, 1.00, 5.58, 11.33, 0.4,
         [("Directorate for Education and Skills", 14, MUT, False, False, 0)],
         align=C)
s.shapes.add_picture(LOGO, Inches(5.82), Inches(6.12), width=Inches(1.70))

# ================= 2. why this project =================
s = new_slide(title="Why this project?")
add_text(s, 0.9, 1.35, 11.8, 0.5, [("Motivation", 24, ACC, True, False, 0)])
bullets(s, [
 "Understand why teachers leave the profession.",
 "Is there a real policy margin to soften teacher shortages by retaining "
 "teachers, or bringing them back?"], y=2.00, size=24, gap=20)
add_text(s, 0.9, 4.00, 11.8, 0.5, [("Problem", 24, ACC, True, False, 0)])
bullets(s, [
 "Official microdata on teachers are not publicly available for many "
 "countries.",
 "The US official rate (NCES Teacher Follow-up Survey) appears only "
 "every 4–9 years, not annually."], y=4.60, size=20, gap=18)

# ================= 3. methodology I: the CPS in numbers =================
s = new_slide(title="The Current Population Survey")
TILES = [("28", "Years (1998\u20132025)"),
         ("5 million", "Individual observations"),
         ("103,820", "Teachers in our database"),
         ("51", "States, including the District of Columbia")]
def hrule(s, x, y, w, pt):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                Inches(x + w), Inches(y))
    ln.line.color.rgb = INK; ln.line.width = Pt(pt)
x0, tw, ty = 0.9, 11.53 / 4, 1.75
hrule(s, x0, ty, 11.53, 1.6)
for i, (big, lab) in enumerate(TILES):
    x = x0 + i * tw
    add_text(s, x, ty + 0.42, tw, 1.0,
             [(big, 36, NAVY, True, False, 0)], align=C, spacing=1.0)
    add_text(s, x + 0.15, ty + 1.50, tw - 0.30, 0.7,
             [(lab, 15, MUT, False, True, 0)], align=C, spacing=1.15)
    if i:
        v = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x),
                                   Inches(ty + 0.40), Inches(x),
                                   Inches(ty + 2.05))
        v.line.color.rgb = RGBColor(0xC9, 0xCF, 0xD6); v.line.width = Pt(0.75)
hrule(s, x0, ty + 2.45, 11.53, 0.6)
add_text(s, 0.9, 4.75, 11.8, 1.2, [[
    [("The monthly household survey of the United States, run by the "
      "Census Bureau.", 20, INK, False, False)], 10],
    [[("Every March it asks each adult about last year: the main job "
       "held, weeks worked, earnings and benefits.",
       20, INK, False, False)], 0]])

# ================= 4. methodology II: who counts as a leaver ===========
s = new_slide(title="Who counts as a leaver?")
mw = 0.74
bx, by, bh = 0.95, 3.05, 0.80
for i, m in enumerate("JFMAMJJASOND"):
    cell = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx + i * mw),
                              Inches(by), Inches(mw), Inches(bh))
    cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
    cell.line.color.rgb = WHITE; cell.line.width = Pt(1.0)
    cell.shadow.inherit = False
    tf = cell.text_frame
    p = tf.paragraphs[0]; p.alignment = C
    r = p.add_run(); r.text = m
    r.font.name = FONT; r.font.size = Pt(15); r.font.bold = True
    r.font.color.rgb = WHITE
mar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.25), Inches(by),
                         Inches(0.98), Inches(bh))
mar.fill.solid(); mar.fill.fore_color.rgb = BURG
mar.line.fill.background(); mar.shadow.inherit = False
tf = mar.text_frame
p = tf.paragraphs[0]; p.alignment = C
r = p.add_run(); r.text = "Mar"
r.font.name = FONT; r.font.size = Pt(15); r.font.bold = True
r.font.color.rgb = WHITE
add_text(s, bx, 2.42, 12 * mw, 0.4,
         [("Last calendar year", 17, NAVY, True, False, 0)], align=C)
add_text(s, 10.45, 2.42, 2.6, 0.4,
         [("this March", 17, BURG, True, False, 0)], align=C)
arrow_to(s, bx + 12 * mw + 0.10, by + bh / 2, 11.20, by + bh / 2, BURG,
         w=1.8)
add_text(s, bx, 4.05, 12 * mw, 0.45, [[
    [("Longest job held: teaching  ", 17, INK, True, False),
     ("✓", 19, GREEN, True, False)], 0]], align=C)
add_text(s, 10.45, 4.05, 2.6, 0.45, [[
    [("teaching now?  ", 17, INK, True, False),
     ("✗", 19, BURG, True, False)], 0]], align=C)
add_text(s, 0.9, 5.35, 11.8, 0.8,
         [("Leavers are the ones who taught as last year’s longest "
           "job and are not teaching this March.", 20, INK, False, False,
           0)], align=C)

# ================= part 1 =================
divider("1", "Leaving rate: how many leave?",
        "For discussion: how often does your system measure who leaves?")

s = new_slide(title="Leaving teaching, 1997–2024")
chart(s, "g2_evolution", (0.7, 1.2, 11.9, 4.85))
message(s, "The leaving rate has remained stable, oscillating between 7 "
        "and 10%. The US rate stands slightly above the average (6.5%) of "
        "the OECD countries with reported data in the latest edition of "
        "Education at a Glance.", size=14.5)

s = new_slide(title="Comparable professions")
chart(s, "comparables_table", (1.6, 1.10, 10.1, 4.95))
message(s, "Teaching is similar to nursing, social work and counseling in "
        "age and gender, and to social work in education and wages; the "
        "main difference is nurses' pay.", size=14.5)

s = new_slide(title="Leaving the occupation, by profession")
chart(s, "leave_professions_deck", (0.7, 1.2, 11.9, 4.85))
message(s, "Teachers leave at about the same or at a lower rate than "
        "comparable professions.")

# ================= part 2 =================
divider("2", "Composition: where they go?",
        "For discussion: where do teachers go when they leave in your country?")

s = new_slide(title="Who leaves teaching (average, 2020–2025)")
chart(s, "flow_employed_5yr", (0.8, 1.15, 11.7, 4.95))
message(s, "Among the leavers, we have switchers, early exits and "
        "retirees, besides the unemployed. Among the switchers, 31% stay "
        "in education or care.", lead="Key messages.")

s = new_slide(title="Who leaves the labor force before 55 (average, 2020–2025)")
chart(s, "flow_olf55_5yr", (0.8, 1.15, 11.7, 4.95))
message(s, "Among early exits, more than half (57%) are mothers with a "
        "child at home.")

# ================= part 3 =================
divider("3", "Correlations: why they leave?",
        "For discussion: which of these levers can your system move?")

s = new_slide(title="Why do teachers leave?")
add_text(s, 0.9, 1.30, 11.8, 0.5,
         [("Reasons identified in the literature", 16, MUT, False, True,
           0)])
COLS = [("Beyond household data", MUT, RGBColor(0xF2, 0xF2, 0xF2), INK,
         ["Working conditions", "Organizational support",
          "Autonomy and intrinsic motives"]),
        ("What we explore", WHITE, NAVY, WHITE,
         ["Financial factors", "Personal life-cycle motives",
          "Sociodemographics"])]
for ci, (head, hc, fill, tc, items) in enumerate(COLS):
    x = 0.9 + ci * 6.0
    box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.95),
                             Inches(5.53), Inches(3.35))
    box.fill.solid(); box.fill.fore_color.rgb = fill
    box.line.fill.background(); box.shadow.inherit = False
    add_text(s, x + 0.35, 2.15, 4.9, 0.5,
             [(head, 20, hc if ci else NAVY, True, False, 0)])
    add_text(s, x + 0.35, 2.85, 4.9, 2.3,
             [(it, 22, tc, False, False, 14) for it in items])
message(s, "Are there more? Which ones matter most in your country?",
        y=5.95, lead="For discussion.")

s = new_slide(title="Relative pay since 1997")
chart(s, "msgA3", (0.7, 1.2, 11.9, 4.85))
message(s, "Teacher pay has not grown in 25 years.")

s = new_slide(title="Leaving, by position in the teacher pay distribution")
chart(s, "pay3_deciles_deck", (0.9, 1.2, 11.5, 4.85))
message(s, "Leavers are concentrated in the bottom two deciles.")

s = new_slide(title="Pension coverage and leaving, across states")
chart(s, "pension_scatter_deck", (0.9, 1.2, 11.5, 4.85))
message(s, "States where more teachers have a pension plan have fewer "
        "early exits.")

# ================= 4. what it means for policy =================
divider("4", "What it means for policy",
        "For discussion: what would bring teachers back in your country?")

s = new_slide(title="Policy options for re-attraction")
BLOCKS = [
 ("Short term and retirees",
  "A reserve for local shortages. They bring experience and can mentor "
  "new teachers. Make it easy to return, for example part-time or "
  "“double-dipping”."),
 ("Medium term and switchers",
  "Early-career conditions (secure contracts, fair pay at the bottom) "
  "and support (mentoring). Learn why some move to jobs that do not "
  "require a degree."),
 ("Long term and early exits",
  "Flexibility, so those who want to return can do so in favoring "
  "conditions, and clear paths to return."),
 ("Research agenda",
  "Working conditions inside schools. Do these patterns hold in other "
  "countries?"),
]
for i, (head, body) in enumerate(BLOCKS):
    x = 0.9 + (i % 2) * 6.05
    y = 1.45 + (i // 2) * 2.45
    add_text(s, x, y, 5.6, 0.5, [(head, 21, ACC, True, False, 0)])
    add_text(s, x, y + 0.55, 5.6, 1.7, [(body, 17, INK, False, False, 0)])
rule = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.9),
                              Inches(6.35), Inches(12.43), Inches(6.35))
rule.line.color.rgb = NAVY; rule.line.width = Pt(1.0)
add_text(s, 0.9, 6.55, 11.8, 0.5,
         [("Across all three: economic security.", 20, NAVY, True, False,
           0)], align=C)

s = new_slide(title="Open questions")
bullets(s, [
 ("Pay floors.", "Leaving concentrates in the bottom two pay deciles. "
  "Would raising the floor retain more teachers than raising the "
  "average?"),
 ("Early careers.", "Exits peak in the first years of the career. Which "
  "policies move this margin — mentoring, stable placements, or "
  "pay?"),
 ("Family exits.", "Half of the early labor-force exits are mothers with "
  "a child at home. Is this an education policy problem or a child-care "
  "one?"),
 ("Re-entry.", "The young leave to study and mothers leave to care. How "
  "many could come back, and what would bring them back?"),
 ("What we cannot see.", "Working conditions and school climate are "
  "invisible in household data. What would it take to measure them "
  "every year?"),
], y=1.70, size=20, gap=26)

prs.save(OUT)
print(f"saved {OUT} with {len(prs.slides._sldIdLst)} slides")
