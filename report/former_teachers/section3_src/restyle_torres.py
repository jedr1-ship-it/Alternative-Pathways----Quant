"""Write the Introduction and apply the layout of Schweickert and Torres (2026),
OECD Education Working Paper No. 342, to the whole Former Teachers draft.

Usage: python3 restyle_torres.py IN.docx OUT.docx [PAGES.json]

Text of the authors' Sections 1 and 2 is not modified (only formatting);
Section 1 receives the new introduction around the authors' paragraph.
PAGES.json maps TOC entry texts to page numbers (from a first rendering).
"""
import copy, json, os, re, sys, unicodedata
import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.paragraph import Paragraph
from docx.table import Table
import intro_content as IC

SRC, OUT = sys.argv[1], sys.argv[2]
PAGES = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}
BLUE, GREY, BEIGE = '4F81BD', 'BFBFBF', 'EEECE1'
NB = '\u00a0'

d = docx.Document(SRC)
body = d.element.body


def el(tag, **a):
    e = OxmlElement(tag)
    for k, v in a.items():
        e.set(qn('w:' + k), str(v))
    return e


def ptext(e):
    return Paragraph(e, d).text


def is_p(e):
    return e.tag == qn('w:p')


def style_of(e):
    return Paragraph(e, d).style.name


def typo(s):
    for _ in range(2):
        s = re.sub(r'\b(\d{1,3}) (\d{3})\b', r'\1' + NB + r'\2', s)
    s = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", s)
    return s


def run(text, bold=False, italic=False, size=None, font=None, color=None):
    r = el('w:r')
    rp = el('w:rPr')
    if font:
        rp.append(el('w:rFonts', ascii=font, hAnsi=font, cs=font, eastAsia=font))
    if bold:
        rp.append(el('w:b'))
    if italic:
        rp.append(el('w:i'))
    if color:
        rp.append(el('w:color', val=color))
    if size:
        rp.append(el('w:sz', val=size))
        rp.append(el('w:szCs', val=size))
    r.append(rp)
    t = el('w:t')
    t.text = typo(text)
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r.append(t)
    return r


def para(runs, style=None, jc=None, after=None, before=None, keep=False,
         num=None, ind=None):
    p = el('w:p')
    pp = el('w:pPr')
    if style:
        pp.append(el('w:pStyle', val=style))
    if keep:
        pp.append(el('w:keepNext'))
    if num is not None:
        npr = el('w:numPr')
        npr.append(el('w:ilvl', val=0))
        npr.append(el('w:numId', val=num))
        pp.append(npr)
    if after is not None or before is not None:
        pp.append(el('w:spacing', before=before or 0, after=after or 0))
    if ind:
        pp.append(el('w:ind', **ind))
    if jc:
        pp.append(el('w:jc', val=jc))
    p.append(pp)
    for r in runs:
        p.append(r)
    return p


def find_h(text, level):
    for e in body:
        if is_p(e) and style_of(e) == level and ptext(e).strip().startswith(text):
            return e
    raise KeyError(text)


def style_id(name):
    return d.styles[name].style_id


# ---------------------------------------------------------------- Section 2 corrections
CORR = [
 ("Here we instead, we first describe", "Here, we first describe"),
 ("and posteriorly develop", "and then develop"),
 ("In USA, which holds one of", "In the United States, which has one of"),
 ("and lead to three main conclusions", "and leads to three main conclusions"),
 ("and retired teacher who returns", "and a retired teacher who returns"),
 ("does not follows on its own", "does not follow on its own"),
 ("maintaining a valid teaching license", "maintaining a valid teaching licence"),
 ("Thirdly, financial factors", "Third, financial factors"),
 ("Organisational Factors", "Organisational factors"),
 ("Teachers\u2019 salary compared to other tertiary-educated workers earnings",
  "Teachers\u2019 salaries compared with the earnings of other tertiary-educated workers"),
 ("A great example is observed in England, where",
  "This is illustrated by evidence from England, where"),
 ("Similarly in the United States and Sweden the same event has long driven female exits",
  "Similarly, in the United States the same event has long driven female exits"),
 ("grey bars report the total rate only", "light blue bars report the total rate only"),
 ("led by Portugal at 128% of the benchmark",
  "led by Peru at 151% of the benchmark, followed by Costa Rica (131%) and Portugal (128%)"),
]


def replace_in_par(p, old, new):
    runs = [r for r in p.iter(qn('w:r')) if r.find(qn('w:t')) is not None]
    full = ''.join(r.find(qn('w:t')).text or '' for r in runs)
    i = full.find(old)
    if i < 0:
        return False
    j = i + len(old)
    pos = 0
    first = True
    for r in runs:
        t = r.find(qn('w:t'))
        s = t.text or ''
        a, b = pos, pos + len(s)
        pos = b
        if b <= i or a >= j:
            continue
        lo, hi = max(i, a) - a, min(j, b) - a
        if first:
            t.text = s[:lo] + new + s[hi:]
            first = False
        else:
            t.text = s[:lo] + s[hi:]
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return True


for old, new in CORR:
    done = sum(replace_in_par(p, old, new) for p in body.iter(qn('w:p'))
               if old in Paragraph(p, d).text)
    assert done == 1, (old, done)

# ---------------------------------------------------------------- figures (EAG layout)
FIG_DIR = os.environ.get('FIG_DIR')
if FIG_DIR:
    from PIL import Image as _Img
    figs = ['figure1_leaving_rate.png', 'figure2_relative_salaries.png',
            'figure3_age_profiles.png']
    blips = list(body.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'))
    assert len(blips) == 3, len(blips)
    CX = int(16.4 / 2.54 * 914400)
    for blip, fname in zip(blips, figs):
        path = os.path.join(FIG_DIR, fname)
        rid, _ = d.part.get_or_add_image(path)
        blip.set(qn('r:embed'), rid)
        w, h = _Img.open(path).size
        cy = int(CX * h / w)
        inline = blip
        while inline is not None and not inline.tag.endswith('}inline') and not inline.tag.endswith('}anchor'):
            inline = inline.getparent()
        ext = inline.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')
        ext.set('cx', str(CX)); ext.set('cy', str(cy))
        for x in inline.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}ext'):
            if x.get('cx') is not None:
                x.set('cx', str(CX)); x.set('cy', str(cy))

# ---------------------------------------------------------------- bullets
numbering = d.part.numbering_part.element
abs_ids = [int(a.get(qn('w:abstractNumId'))) for a in numbering.findall(qn('w:abstractNum'))]
num_ids = [int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))]
ABS, NUM = max(abs_ids + [0]) + 1, max(num_ids + [0]) + 1
an = el('w:abstractNum', abstractNumId=ABS)
an.append(el('w:multiLevelType', val='singleLevel'))
lvl = el('w:lvl', ilvl=0)
lvl.append(el('w:start', val=1))
lvl.append(el('w:numFmt', val='bullet'))
lvl.append(el('w:lvlText', val='\u25aa'))
lvl.append(el('w:lvlJc', val='left'))
lp = el('w:pPr')
lp.append(el('w:ind', left=567, hanging=284))
lvl.append(lp)
lr = el('w:rPr')
lr.append(el('w:rFonts', ascii='Arial', hAnsi='Arial'))
lr.append(el('w:color', val=BLUE))
lvl.append(lr)
an.append(lvl)
first_num = numbering.find(qn('w:num'))
if first_num is not None:
    first_num.addprevious(an)
else:
    numbering.append(an)
nm = el('w:num', numId=NUM)
nm.append(el('w:abstractNumId', val=ABS))
numbering.append(nm)

# ---------------------------------------------------------------- intro
H1_INTRO = find_h('1. Introduction', 'Heading 1')
nxt = H1_INTRO.getnext()
note = nxt if is_p(nxt) and ptext(nxt).startswith('Pendiente de escribir') else None
keep_para = None
e = H1_INTRO.getnext()
while e is not None and not (is_p(e) and style_of(e) == 'Heading 1'):
    if is_p(e) and ptext(e).startswith('Re-attracting former teachers'):
        keep_para = e
    e = e.getnext()
assert keep_para is not None
if note is not None:
    body.remove(note)


def body_par(text):
    p = copy.deepcopy(keep_para)
    for c in list(p):
        if c.tag != qn('w:pPr'):
            p.remove(c)
    p.append(run(text))
    return p


# paper title and Key take-aways panel before "1. Introduction"
title_p = para([run(IC.PAPER_TITLE)], after=240, keep=True)
title_p.set(qn('w:rsidR'), '00000000')
TITLE_MARK = 'paper-title'
H1_INTRO.addprevious(title_p)

kt = el('w:tbl')
tp = el('w:tblPr')
tp.append(el('w:tblW', w=9310, type='dxa'))
tp.append(el('w:tblLayout', type='fixed'))
kt.append(tp)
g = el('w:tblGrid')
g.append(el('w:gridCol', w=9310))
kt.append(g)
tr = el('w:tr')
tc = el('w:tc')
tcp = el('w:tcPr')
tcp.append(el('w:tcW', w=9310, type='dxa'))
tc.append(tcp)
tc.append(para([run('Key take-aways')], after=120))
for head, items in IC.TAKEAWAYS:
    tc.append(para([run(head, bold=True)], before=120, after=60, keep=True))
    for lab, txt in items:
        tc.append(para([run(lab + ' ', bold=True), run(txt)], num=NUM, after=60,
                       jc='both'))
tr.append(tc)
kt.append(tr)
H1_INTRO.addprevious(kt)
H1_INTRO.addprevious(para([], after=120))

# introduction paragraphs around the authors' paragraph
anchor = H1_INTRO
for txt in IC.INTRO:
    if txt == 'KEEP':
        anchor.addnext(keep_para)  # moves it into place
        anchor = keep_para
    else:
        p = body_par(txt)
        anchor.addnext(p)
        anchor = p

# ---------------------------------------------------------------- refs
REFH = find_h('References', 'Heading 2')


def ref_list():
    out, e = [], REFH.getnext()
    while e is not None and is_p(e):
        out.append(e)
        e = e.getnext()
    return out


def key(s):
    s = unicodedata.normalize('NFKD', s.replace('*', '')).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9 ]', '', s.lower())


tpl_ref = ref_list()[1]
for r in IC.NEW_REFS:
    p = copy.deepcopy(tpl_ref)
    for c in list(p):
        if c.tag != qn('w:pPr'):
            p.remove(c)
    for i, part in enumerate(r.split('*')):
        if part:
            p.append(run(part, italic=bool(i % 2)))
    for e in ref_list():
        if key(ptext(e)) > key(r):
            e.addprevious(p)
            break

# ---------------------------------------------------------------- styles
st = d.styles
# document defaults: Arial 10
rpd = d.styles.element.find(qn('w:docDefaults')).find(qn('w:rPrDefault')).find(qn('w:rPr'))
rf = rpd.find(qn('w:rFonts'))
for a in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
    rf.set(qn('w:' + a), 'Arial')
for t in ('w:sz', 'w:szCs'):
    rpd.find(qn(t)).set(qn('w:val'), '20')


def set_style(name, font='Arial', size=10, bold=False, italic=False, color=None,
              before=None, after=None, keep=False, indent=None, align=None):
    s = st[name]
    f = s.font
    f.name = font
    rpr = s.element.get_or_add_rPr()
    rfo = rpr.find(qn('w:rFonts'))
    for a in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
        rfo.set(qn('w:' + a), font)
    for a in ('asciiTheme', 'hAnsiTheme', 'cstheme', 'eastAsiaTheme'):
        if rfo.get(qn('w:' + a)) is not None:
            del rfo.attrib[qn('w:' + a)]
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = RGBColor.from_string(color or '000000')
    pf = s.paragraph_format
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    pf.keep_with_next = keep
    if indent is not None:
        pf.left_indent = Cm(indent)
    if align is not None:
        pf.alignment = align


set_style('Normal', size=10, before=0, after=6)
st['Normal'].paragraph_format.line_spacing = 1.0
set_style('Heading 1', font='Arial', size=12, bold=True, color=BLUE, before=18,
          after=9, keep=True)
set_style('Heading 2', font='Arial', size=11, bold=True, italic=True,
          before=14, after=7, keep=True)
set_style('Heading 3', font='Arial', size=11, italic=True, color='7F7F7F',
          before=10, after=6, keep=True, indent=0.6)
set_style('Title', font='Arial Narrow', size=26, bold=True, color=BLUE)
set_style('toc 1', font='Arial', size=10, color=BLUE, before=6, after=2)
set_style('toc 2', font='Arial', size=9, before=0, after=0, indent=0.35)

# ---------------------------------------------------------------- runs
STRIP = ('w:rFonts', 'w:sz', 'w:szCs', 'w:color', 'w:highlight')


def strip_runs(p, also=()):
    for r in p.iter(qn('w:r')):
        rp = r.find(qn('w:rPr'))
        if rp is None:
            continue
        for t in STRIP + tuple(also):
            for x in rp.findall(qn(t)):
                rp.remove(x)
        # in-text citations: plain text, as in the working paper
        for x in rp.findall(qn('w:rStyle')):
            if x.get(qn('w:val')) == 'Hyperlink':
                rp.remove(x)
        for x in rp.findall(qn('w:u')):
            rp.remove(x)


def set_runs(p, font=None, size=None, bold=None, italic=None, color=None):
    for r in p.iter(qn('w:r')):
        rp = r.find(qn('w:rPr'))
        if rp is None:
            rp = el('w:rPr')
            r.insert(0, rp)
        for t in STRIP:
            for x in rp.findall(qn(t)):
                rp.remove(x)
        if bold is not None:
            for x in rp.findall(qn('w:b')) + rp.findall(qn('w:bCs')):
                rp.remove(x)
            if bold:
                rp.insert(0, el('w:b'))
        if italic is not None:
            for x in rp.findall(qn('w:i')) + rp.findall(qn('w:iCs')):
                rp.remove(x)
            if italic:
                rp.insert(0, el('w:i'))
        if font:
            rp.insert(0, el('w:rFonts', ascii=font, hAnsi=font, cs=font, eastAsia=font))
        if color:
            rp.append(el('w:color', val=color))
        if size:
            rp.append(el('w:sz', val=size))
            rp.append(el('w:szCs', val=size))


def set_spacing(p, before=None, after=None, keep=None):
    pp = p.find(qn('w:pPr'))
    if pp is None:
        pp = el('w:pPr')
        p.insert(0, pp)
    if keep:
        if pp.find(qn('w:keepNext')) is None:
            pp.insert(1 if pp.find(qn('w:pStyle')) is not None else 0, el('w:keepNext'))
    sp = pp.find(qn('w:spacing'))
    if sp is None:
        sp = el('w:spacing')
        # schema order: spacing after keepNext/numPr etc. (append before ind/jc)
        ref = pp.find(qn('w:ind'))
        if ref is None:
            ref = pp.find(qn('w:jc'))
        if ref is not None:
            ref.addprevious(sp)
        else:
            pp.append(sp)
    if before is not None:
        sp.set(qn('w:before'), str(before))
    if after is not None:
        sp.set(qn('w:after'), str(after))
    for a in ('line', 'lineRule'):
        if sp.get(qn('w:' + a)) is not None:
            del sp.attrib[qn('w:' + a)]


CAP = re.compile(r'^(Table|Figure) \d+\. ')
NOTE = re.compile(r'^(Note|Notes|Source)s?\b')
els = list(body)
in_refs = False
toc_start = find_h('Table of contents', 'Heading 1')
prev_cap = False
for e in els:
    if not is_p(e):
        prev_cap = False
        continue
    sname = style_of(e)
    txt = ptext(e)
    if e is REFH:
        in_refs = True
    if sname.startswith('Heading'):
        set_runs(e, bold=None, italic=None)
        strip_runs(e, also=('w:b', 'w:bCs', 'w:i', 'w:iCs'))
        prev_cap = False
        continue
    if e is title_p:
        set_runs(e, font='Arial Narrow', size=32, bold=True, color=BLUE)
        continue
    if CAP.match(txt):
        set_runs(e, font='Arial Narrow', size=24, bold=True, color=BLUE)
        set_spacing(e, before=240, after=80, keep=True)
        prev_cap = True
        continue
    if prev_cap and txt and len(txt) < 200 and not NOTE.match(txt):
        # subtitle under a table or figure title
        set_runs(e, size=18, italic=False)
        set_spacing(e, before=0, after=80, keep=True)
        prev_cap = False
        continue
    prev_cap = False
    if NOTE.match(txt):
        set_runs(e, size=16)
        set_spacing(e, before=0, after=40)
        continue
    if in_refs:
        set_runs(e, size=18)
        continue
    strip_runs(e)

# title page
tp_title = next(e for e in els if is_p(e) and ptext(e).startswith('Former Teachers: Barriers'))
set_runs(tp_title, font='Arial Narrow', size=52, bold=True, color=BLUE)
for e in els:
    if is_p(e) and ptext(e).strip() == 'Directorate for Education and Skills':
        set_runs(e, size=26, color='595959')
    if is_p(e) and ptext(e).strip().startswith('WORKING DRAFT'):
        set_runs(e, size=22, bold=True, color='595959')
# "Table of contents" title, as in the working paper
set_runs(toc_start, font='Arial Narrow', size=40, bold=False, color=BLUE)

# ---------------------------------------------------------------- tables
def borders(tc, top=None, bottom=None, left=None, right=None):
    pr = tc.find(qn('w:tcPr'))
    if pr is None:
        pr = el('w:tcPr')
        tc.insert(0, pr)
    old = pr.find(qn('w:tcBorders'))
    if old is not None:
        pr.remove(old)
    b = el('w:tcBorders')
    for side, spec in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        if spec is None:
            b.append(el('w:' + side, val='nil'))
        else:
            b.append(el('w:' + side, val='single', sz=spec[0], space=0, color=spec[1]))
    # schema order inside tcPr: tcW, gridSpan, vMerge, tcBorders, shd, ...
    anchor = None
    for t in ('w:vMerge', 'w:gridSpan', 'w:tcW'):
        anchor = pr.find(qn(t))
        if anchor is not None:
            break
    if anchor is not None:
        anchor.addnext(b)
    else:
        pr.insert(0, b)
    return pr


def shade(tc, fill):
    pr = tc.find(qn('w:tcPr'))
    for x in pr.findall(qn('w:shd')):
        pr.remove(x)
    if fill:
        s = el('w:shd', val='clear', color='auto', fill=fill)
        b = pr.find(qn('w:tcBorders'))
        (b.addnext(s) if b is not None else pr.append(s))


for t in body.findall(qn('w:tbl')):
    tcs = t.findall('.//' + qn('w:tc'))
    first = ''.join(x.text or '' for x in t.iter(qn('w:t'))).strip()
    if len(tcs) == 1 and (first.startswith('Box ') or first.startswith('Key take-aways')):
        tc = tcs[0]
        pr = borders(tc, (8, BLUE), (8, BLUE), (8, BLUE), (8, BLUE))
        shade(tc, BEIGE)
        m = pr.find(qn('w:tcMar'))
        if m is None:
            m = el('w:tcMar')
            pr.append(m)
        for x in list(m):
            m.remove(x)
        for side, w in (('top', 170), ('left', 200), ('bottom', 170), ('right', 200)):
            m.append(el('w:' + side, w=w, type='dxa'))
        ps = tc.findall(qn('w:p'))
        for k, p in enumerate(ps):
            txt = ptext(p)
            if k == 0:
                big = txt.startswith('Key take-aways')
                set_runs(p, font='Arial Narrow', size=32 if big else 24, bold=True,
                         color=BLUE)
                set_spacing(p, before=0, after=120, keep=True)
            elif NOTE.match(txt):
                set_runs(p, size=16)
                set_spacing(p, before=60, after=0)
            else:
                strip_runs(p)
                set_spacing(p, after=100)
        continue
    # data tables
    rows = t.findall(qn('w:tr'))
    if not rows:
        continue
    is_old = rows[0].find('.//' + qn('w:shd')) is not None
    nhead = sum(1 for r in rows if r.find('.//' + qn('w:tblHeader')) is not None) or 1
    for ri, r in enumerate(rows):
        cells = r.findall(qn('w:tc'))
        for ci, tc in enumerate(cells):
            if is_old:
                left = (4, GREY) if ci > 0 else None
                if ri == 0:
                    borders(tc, top=(12, BLUE), bottom=(6, BLUE), left=left)
                    shade(tc, None)
                else:
                    borders(tc, bottom=(4, GREY), left=left)
            for p in tc.findall(qn('w:p')):
                for rr in p.iter(qn('w:r')):
                    rp = rr.find(qn('w:rPr'))
                    if rp is None:
                        rp = el('w:rPr')
                        rr.insert(0, rp)
                    for x in rp.findall(qn('w:rFonts')) + rp.findall(qn('w:color')):
                        rp.remove(x)
                    rp.insert(0, el('w:rFonts', ascii='Arial Narrow', hAnsi='Arial Narrow',
                                    cs='Arial Narrow', eastAsia='Arial Narrow'))
                    sz = rp.find(qn('w:sz'))
                    cur = int(sz.get(qn('w:val'))) if sz is not None else 20
                    new = 18 if is_old else max(cur + 1, 16)
                    for x in rp.findall(qn('w:sz')) + rp.findall(qn('w:szCs')):
                        rp.remove(x)
                    rp.append(el('w:sz', val=new))
                    rp.append(el('w:szCs', val=new))
                    if is_old and ri == 0:
                        for x in rp.findall(qn('w:b')):
                            rp.remove(x)
                        rp.insert(1, el('w:b'))

# ---------------------------------------------------------------- refs: *x* -> italics
def asterisks_to_italics(p):
    italic = False
    for r in list(p.iter(qn('w:r'))):
        t = r.find(qn('w:t'))
        if t is None or t.text is None:
            continue
        parts = t.text.split('*')
        new_runs = []
        for k, part in enumerate(parts):
            if k > 0:
                italic = not italic
            if not part:
                continue
            nr = copy.deepcopy(r)
            nt = nr.find(qn('w:t'))
            nt.text = part
            nt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            rp = nr.find(qn('w:rPr'))
            if rp is None:
                rp = el('w:rPr')
                nr.insert(0, rp)
            for x in rp.findall(qn('w:i')) + rp.findall(qn('w:iCs')):
                rp.remove(x)
            if italic:
                rp.insert(0, el('w:i'))
            new_runs.append(nr)
        for nr in new_runs:
            r.addprevious(nr)
        r.getparent().remove(r)


for e in ref_list():
    if '*' in ptext(e):
        asterisks_to_italics(e)

# ---------------------------------------------------------------- page
sec = d.sections[0]
sec.left_margin = Cm(2.29)
sec.right_margin = Cm(2.29)
sec.different_first_page_header_footer = True
d.settings.odd_and_even_pages_header_footer = True
FOOT = ('FORMER TEACHERS: BARRIERS, INCENTIVES AND POLICY LESSONS FOR RE-ENTRY '
        '\u00a9 OECD 2026')


def page_field():
    rs = []
    r1 = el('w:r'); r1.append(el('w:fldChar', fldCharType='begin')); rs.append(r1)
    r2 = el('w:r'); it = el('w:instrText'); it.text = ' PAGE '
    it.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); r2.append(it); rs.append(r2)
    r3 = el('w:r'); r3.append(el('w:fldChar', fldCharType='separate')); rs.append(r3)
    r4 = run('1', bold=True, size=24); rs.append(r4)
    r5 = el('w:r'); r5.append(el('w:fldChar', fldCharType='end')); rs.append(r5)
    for r in rs[:3] + rs[4:]:
        rp = el('w:rPr'); rp.append(el('w:b')); rp.append(el('w:sz', val=24)); r.insert(0, rp)
    return rs


def fill(hf, runs, jc):
    hf.is_linked_to_previous = False
    hel = hf._element
    for x in list(hel):
        hel.remove(x)
    hel.append(para(runs, jc=jc, after=0))


fill(sec.header, [run('| ', size=24, color='7F7F7F')] + page_field(), 'right')
fill(sec.even_page_header, page_field() + [run(' |', size=24, color='7F7F7F')], 'left')
fill(sec.footer, [run(FOOT, size=16)], 'center')
fill(sec.even_page_footer, [run(FOOT, size=16)], 'center')
fill(sec.first_page_header, [], 'left')
fill(sec.first_page_footer, [], 'left')

# ---------------------------------------------------------------- TOC
# remove the old static entries and write a TOC in the working-paper layout
e = toc_start.getnext()
old = []
while e is not None and is_p(e) and '\t' in ptext(e):
    old.append(e)
    e = e.getnext()
for x in old:
    body.remove(x)

entries = []  # (kind, text)
for x in body:
    if not is_p(x):
        if x.tag == qn('w:tbl'):
            t1 = ''.join(tt.text or '' for tt in x.iter(qn('w:t'))).strip()
            m = re.match(r'^(Box \d+\. .*?)(?:(?<=[a-z\)])(?=[A-Z][a-z])|$)', t1)
            first_p = x.find('.//' + qn('w:p'))
            if t1.startswith('Box ') and first_p is not None:
                entries.append(('box', ptext(first_p)))
        continue
    s = style_of(x)
    t = ptext(x).strip()
    if s == 'Heading 1' and t and t != 'Table of contents':
        entries.append(('h1', t))
    elif s == 'Heading 2' and t:
        entries.append(('h2', t))
    elif CAP.match(t):
        entries.append(('fig' if t.startswith('Figure') else 'tab', t))

RT = 9310


def toc_line(text, page, style, color=None, size=None):
    p = para([run(text, color=color, size=size), run('\t'),
              run(str(page), color=color, size=size)], style=style_id(style), after=0)
    pp = p.find(qn('w:pPr'))
    tabs = el('w:tabs')
    tabs.append(el('w:tab', val='right', pos=RT))
    pp.insert(1, tabs)
    return p


new = []
for kind, t in entries:
    if kind == 'h1':
        new.append(toc_line(t, PAGES.get(t, ''), 'toc 1'))
    elif kind == 'h2':
        new.append(toc_line(t, PAGES.get(t, ''), 'toc 2'))
for label, kind in (('FIGURES', 'fig'), ('TABLES', 'tab'), ('BOXES', 'box')):
    items = [t for k, t in entries if k == kind]
    if not items:
        continue
    new.append(para([run(label, bold=True, color=BLUE, size=20)], before=280, after=80))
    for t in items:
        new.append(toc_line(t, PAGES.get(t, ''), 'toc 2', size=17))
anchor = toc_start
for p in new:
    anchor.addnext(p)
    anchor = p

d.save(OUT)
json.dump([t for _, t in entries], open(OUT + '.toc.json', 'w'))
print('saved', OUT)
