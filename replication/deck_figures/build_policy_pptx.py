"""The policy version of the cluster deck: 15-20 minutes for a policy
audience. Methodology is one slide, the body is the results, and the
closing slide poses the open questions for discussion. Reuses the
figures rendered in report/data_cluster/_pngx (from the same PDFs the
main deck uses). Writes report/data_cluster/Proyect_US_policy.pptx.
Run from the repo root after the _pngx images exist."""
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUT = "report/data_cluster/Proyect_US_policy.pptx"
FIG = "report/data_cluster/_pngx"
LOGO = "report/data_cluster/oecd_logo.png"
FONT = "Garamond"
INK = RGBColor(0x21, 0x25, 0x29)
MUT = RGBColor(0x6B, 0x74, 0x80)
NAVY = RGBColor(0x10, 0x2D, 0x5E)
ACC = RGBColor(0x2D, 0x6C, 0xB5)
BAND = RGBColor(0xEC, 0xF2, 0xF9)
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

def message(s, text, y=6.22, size=16):
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(y - 0.14),
                              prs.slide_width, Inches(1.05))
    band.fill.solid(); band.fill.fore_color.rgb = BAND
    band.line.fill.background(); band.shadow.inherit = False
    add_text(s, 0.9, y, 11.8, 0.9, [[
        [("Key message.  ", size, NAVY, True, False),
         (text, size, INK, False, False)], 0]])

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

# ================= 1. title =================
s = prs.slides.add_slide(blank)
PAGENO[0] += 1
band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.55),
                          prs.slide_width, Inches(2.50))
band.fill.solid(); band.fill.fore_color.rgb = NAVY
band.line.fill.background(); band.shadow.inherit = False
add_text(s, 0.33, 2.30, 12.67, 1.5, [
 ("Teacher Attrition in the United States",
  32, RGBColor(0xFF, 0xFF, 0xFF), True, False, 4),
 ("What twenty-eight years of labour force data show", 32,
  RGBColor(0xD7, 0xE3, 0xF2), False, False, 0)], align=C, spacing=1.12)
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
 "Official statistics on teacher attrition are published only every four "
 "or five years.",
 "We start with the United States, the country with the most information "
 "available."], y=4.60, size=20, gap=18)

# ================= 3. the data, in one slide =================
s = new_slide(title="The data, in one slide")
bullets(s, [
 ("One source.", "The Census Bureau's household survey (the CPS), which "
  "records every worker's occupation each year."),
 ("One definition.", "A teacher is anyone whose main job last year was "
  "school teaching; a leaver is a teacher no longer teaching a year "
  "later."),
 ("One series.", "Twenty-eight consecutive years (1998–2025), "
  "matching the official benchmark where it exists and filling the "
  "years in between."),
], y=2.20, size=22, gap=34)
add_text(s, 0.9, 6.30, 11.8, 0.6,
         [("The methodological detail is in the appendix of the long deck "
           "and in the paper.", 14, MUT, False, True, 0)])

# ================= 4-10. results =================
s = new_slide(title="Leaving teaching, 1997–2024")
chart(s, "g2_evolution", (0.7, 1.2, 11.9, 4.85))
message(s, "Around 8 of every 100 teachers leave each year, and the rate "
        "has been stable for 25 years. Attrition is a permanent flow, not "
        "a recent crisis.")

s = new_slide(title="Leaving the occupation, by profession")
chart(s, "leave_professions_deck", (0.7, 1.2, 11.9, 4.85))
message(s, "Teachers leave at rates similar to or below the comparable "
        "professions. The distinctive part of teaching is who leaves and "
        "where they go, not how many.")

s = new_slide(title="Of every 100 leavers (average, 2020–2024)")
chart(s, "flow_employed_5yr", (0.8, 1.15, 11.7, 4.95))
message(s, "Teachers are not being poached: 7 of every 10 leavers exit "
        "employment altogether — to retirement, home or unemployment. "
        "Only 3 in 10 trade teaching for another job.")

s = new_slide(title="Where the employed leavers go")
chart(s, "occ_all_slide", (0.4, 1.12, 12.5, 5.1))
message(s, "More than a third of the employed leavers move to occupations "
        "where most workers hold no college degree (in red). Leaving "
        "teaching usually means leaving the profession, not moving up.",
        y=6.30, size=14.5)

s = new_slide(title="Who leaves the labor force before 55 (average, 2020–2024)")
chart(s, "flow_olf55_5yr", (0.8, 1.15, 11.7, 4.95))
message(s, "Early labor-force exit is mostly a family story. More than "
        "half of this group are mothers with a child at home.")

s = new_slide(title="And the youngest of them leave to study")
chart(s, "study_bygroup", (0.8, 1.15, 11.7, 4.95))
message(s, "Studying is the exit of the young and the childless, not of "
        "the mothers. Among leavers under 30, almost half are enrolled "
        "in school.")

s = new_slide(title="Leaving, over the life cycle")
chart(s, "u_routes_deck", (0.7, 1.25, 11.9, 4.75))
message(s, "Put retention efforts where they can work: the first years of "
        "the career (mentoring, stable placements). Retirements can only "
        "be planned for, not prevented.")

# ================= 11. three margins =================
s = new_slide(title="What this says for policy: three margins, quantified")
add_text(s, 0.9, 1.35, 11.8, 0.5, [[
    [("Retirees ", 22, ACC, True, False),
     ("(out of the labor force, over 55)", 18, MUT, False, False)], 0]])
add_text(s, 0.9, 1.90, 11.8, 1.0, [
 ("About 3% of teachers retire each year, a third of all exits. Delaying "
  "retirement extends careers but does not reintegrate anyone.",
  19, INK, False, False, 0)])
add_text(s, 0.9, 3.10, 11.8, 0.5, [[
    [("Switchers ", 22, ACC, True, False),
     ("(employed in another job)", 18, MUT, False, False)], 0]])
add_text(s, 0.9, 3.65, 11.8, 1.0, [
 ("About 2% move to another job each year, often to jobs that do not "
  "require a degree. A real margin, but shortages cannot be closed "
  "through retention alone.", 19, INK, False, False, 0)])
add_text(s, 0.9, 4.95, 11.8, 0.5, [[
    [("Early exits ", 22, ACC, True, False),
     ("(out of the labor force, under 55)", 18, MUT, False, False)], 0]])
add_text(s, 0.9, 5.50, 11.8, 1.2, [
 ("About 2% leave the labor force before 55 each year. Most are mothers "
  "at home, for whom flexibility may be the missing piece. The young and "
  "childless leave to study and need re-entry paths.",
  19, INK, False, False, 0)])

# ================= 12-15. drivers =================
s = new_slide(title="What correlates with leaving")
chart(s, "ame_ext", (0.6, 1.12, 12.1, 6.1))

s = new_slide(title="Relative pay since 1997")
chart(s, "msgA3", (0.7, 1.2, 11.9, 4.85))
message(s, "Teacher pay has not grown in 25 years, and neither has it in "
        "the closest helping professions. The typical graduate now "
        "out-earns a teacher by $30,000 a year.")

s = new_slide(title="Leaving, by position in the teacher pay distribution")
chart(s, "pay3_deciles_deck", (0.9, 1.2, 11.5, 4.85))
message(s, "Leaving is concentrated in the bottom two pay deciles, where "
        "part-year and part-time contracts live. Above the median, pay "
        "barely matters.")

s = new_slide(title="Pension coverage and leaving, across states")
chart(s, "pension_scatter_deck", (0.9, 1.2, 11.5, 4.85))
message(s, "States where more teachers have a pension plan lose fewer "
        "teachers before 55. Economic security retains.")

# ================= 16. open questions =================
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
