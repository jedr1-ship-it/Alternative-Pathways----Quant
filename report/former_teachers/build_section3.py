"""Insert Section 3 into the Former Teachers draft, touching nothing else.

Usage: python3 build_section3_v2.py CONTENT_MODULE SRC.docx OUT.docx
Formats are cloned from the draft: Heading 2/3 from Section 2, body text,
Table 1 (tables), Box 1 (boxes), the 8.5pt "Source:" line and the
reference-list paragraphs. Typography follows the OECD Style Guide (2025):
hard spaces in numbers, currencies and dates; curly quotes.
"""
import copy, importlib, re, sys
import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

C = importlib.import_module(sys.argv[1])
SRC, OUT = sys.argv[2], sys.argv[3]
d = docx.Document(SRC)
body = d.element.body
NB = "\u00a0"
MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
CUR = "AUD|CAD|CHF|CNY|EUR|GBP|JPY|NZD|SEK|USD"


def typo(t, url_safe=True):
    """OECD typography: hard spaces, curly apostrophes and quotes."""
    parts = re.split(r'(https?://\S+)', t)
    out = []
    for i, s in enumerate(parts):
        if i % 2:  # URL, leave untouched
            out.append(s)
            continue
        for _ in range(2):
            s = re.sub(r'\b(\d{1,3}) (\d{3})\b', r'\1' + NB + r'\2', s)
        s = re.sub(r'\b(' + CUR + r') (?=\d)', r'\1' + NB, s)
        s = re.sub(r'\b(\d{1,2}) (' + MONTHS + r')\b', r'\1' + NB + r'\2', s)
        s = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", s)
        s = re.sub(r"s' ", "s\u2019 ", s)
        s = re.sub(r'"(?=\w)', "\u201c", s)
        s = s.replace('"', "\u201d")
        out.append(s)
    return ''.join(out)


def find_p(text, style):
    for e in body:
        if e.tag == qn('w:p'):
            p = Paragraph(e, d)
            if p.style.name == style and p.text.strip().startswith(text):
                return e
    raise KeyError(text)


H1 = find_p('3. The policies', 'Heading 1')
CONC = find_p('4. Conclusions', 'Heading 1')
T_H2 = find_p('2.1 The teacher', 'Heading 2')
T_H3 = find_p('Organisational Factors', 'Heading 3')
T_P = find_p('Closely linked to the daily', 'Normal')
T_CAP = find_p('Table 1. Reasons', 'Normal')
T_SRC = find_p("Source: Authors' elaboration", 'Normal')
tbls = [e for e in body if e.tag == qn('w:tbl')]
T_TBL, T_BOX = tbls[0], tbls[1]
assert 'Box 1' in ''.join(T_BOX.itertext())


def first_run(p):
    return next(iter(p.iter(qn('w:r'))))


def make_run(tpl_run, text, style=''):
    r = copy.deepcopy(tpl_run)
    for c in list(r):
        if c.tag != qn('w:rPr'):
            r.remove(c)
    rpr = r.find(qn('w:rPr'))
    if rpr is None:
        rpr = r.makeelement(qn('w:rPr'), {})
        r.insert(0, rpr)
    for t in ('w:b', 'w:bCs', 'w:i', 'w:iCs'):
        for x in rpr.findall(qn(t)):
            rpr.remove(x)
    if 'i' in style:
        for t in ('w:iCs', 'w:i'):
            rpr.insert(0, rpr.makeelement(qn(t), {}))
    if style in ('b',):
        for t in ('w:bCs', 'w:b'):
            rpr.insert(0, rpr.makeelement(qn(t), {}))
    if style == 'src':  # 8.5 pt, as the draft's Source lines
        for t in ('w:sz', 'w:szCs'):
            for x in rpr.findall(qn(t)):
                rpr.remove(x)
            rpr.append(rpr.makeelement(qn(t), {qn('w:val'): '17'}))
    t = r.makeelement(qn('w:t'), {})
    t.text = typo(text)
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r.append(t)
    return r


def split_italics(text, base=''):
    out = []
    for i, part in enumerate(text.split('*')):
        if part:
            out.append((part, 'i' if i % 2 else base))
    return out


def make_par(tpl_p, runs):
    tr = first_run(tpl_p)
    p = copy.deepcopy(tpl_p)
    for c in list(p):
        if c.tag != qn('w:pPr'):
            p.remove(c)
    for text, st in runs:
        for tx, s2 in (split_italics(text, st) if st in ('', 'src') else [(text, st)]):
            p.append(make_run(tr, tx, s2))
    return p


def keep_next(p):
    ppr = p.find(qn('w:pPr'))
    if ppr is None:
        ppr = p.makeelement(qn('w:pPr'), {})
        p.insert(0, ppr)
    if ppr.find(qn('w:keepNext')) is None:
        ps_ = ppr.find(qn('w:pStyle'))
        kn = ppr.makeelement(qn('w:keepNext'), {})
        if ps_ is not None:
            ps_.addnext(kn)
        else:
            ppr.insert(0, kn)


def make_table(spec):
    widths, rows = spec['widths'], spec['rows']
    ncol = len(widths)
    t = copy.deepcopy(T_TBL)
    trs = t.findall(qn('w:tr'))
    for r in trs[len(rows):]:
        t.remove(r)
    while len(t.findall(qn('w:tr'))) < len(rows):
        t.append(copy.deepcopy(t.findall(qn('w:tr'))[-1]))
    grid = t.find(qn('w:tblGrid'))
    gcs = grid.findall(qn('w:gridCol'))
    while len(gcs) < ncol:
        grid.append(copy.deepcopy(gcs[-1]))
        gcs = grid.findall(qn('w:gridCol'))
    for gc, w in zip(gcs, widths):
        gc.set(qn('w:w'), str(w))
    trs = t.findall(qn('w:tr'))
    for n, (r, vals) in enumerate(zip(trs, rows)):
        tcs = r.findall(qn('w:tc'))
        while len(tcs) < ncol:
            tcs[-1].addnext(copy.deepcopy(tcs[-1]))
            tcs = r.findall(qn('w:tc'))
        for tc, txt, w in zip(tcs, vals, widths):
            tcw = tc.find(qn('w:tcPr')).find(qn('w:tcW'))
            if tcw is not None:
                tcw.set(qn('w:w'), str(w))
                tcw.set(qn('w:type'), 'dxa')
            ps = tc.findall(qn('w:p'))
            tpl = ps[0]
            rpr = first_run(tpl).find(qn('w:rPr'))
            bold = rpr is not None and rpr.find(qn('w:b')) is not None
            np_ = make_par(tpl, [(txt, 'b' if bold else '')])
            for x in ps:
                tc.remove(x)
            tc.append(np_)
            if n < len(rows) - 1:
                keep_next(np_)
        trpr = r.find(qn('w:trPr'))
        if trpr is None:
            trpr = r.makeelement(qn('w:trPr'), {})
            r.insert(1 if r.find(qn('w:tblPrEx')) is not None else 0, trpr)
        if trpr.find(qn('w:cantSplit')) is None:
            trpr.insert(0, trpr.makeelement(qn('w:cantSplit'), {}))
    return t


new = []
for blk in C.B:
    k = blk[0]
    if k == 'h2':
        new.append(make_par(T_H2, [(blk[1], 'b')]))
    elif k == 'h3':
        new.append(make_par(T_H3, [(blk[1], 'b')]))
    elif k == 'p':
        new.append(make_par(T_P, [(blk[1], '')]))
    elif k == 'cap':
        cp = make_par(T_CAP, [(blk[1], 'b')])
        keep_next(cp)
        new.append(cp)
    elif k == 'src':
        new.append(make_par(T_SRC, [(blk[1], '')]))
    elif k == 'table':
        new.append(make_table(C.TABLES[blk[1]]))
    elif k == 'box':
        t = copy.deepcopy(T_BOX)
        tc = t.find('.//' + qn('w:tc'))
        ps = tc.findall(qn('w:p'))
        tpl_title, tpl_body = ps[0], ps[1]
        paras = [make_par(tpl_title, [(blk[1], 'b')])]
        for para in blk[2]:
            paras.append(make_par(tpl_body, para))
        for x in ps:
            tc.remove(x)
        for x in paras:
            tc.append(x)
        for r in t.findall(qn('w:tr')):  # keep each box on one page
            trpr = r.find(qn('w:trPr'))
            if trpr is None:
                trpr = r.makeelement(qn('w:trPr'), {})
                r.insert(1 if r.find(qn('w:tblPrEx')) is not None else 0, trpr)
            if trpr.find(qn('w:cantSplit')) is None:
                trpr.insert(0, trpr.makeelement(qn('w:cantSplit'), {}))
        new.append(t)
        new.append(make_par(T_P, [('', '')]))

# replace the placeholders between "3. The policies" and "4. Conclusions"
els = list(body)
for e in els[els.index(H1) + 1: els.index(CONC)]:
    body.remove(e)
anchor = H1
for e in new:
    anchor.addnext(e)
    anchor = e
anchor.addnext(make_par(T_P, [('', '')]))

# references: insert alphabetically into the existing list
REFH = find_p('References', 'Heading 2')


def ref_list():
    out, e = [], REFH.getnext()
    while e is not None and e.tag == qn('w:p'):
        out.append(e)
        e = e.getnext()
    return out


def key(s):
    import unicodedata
    s = unicodedata.normalize('NFKD', s.replace('*', '')).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9 ]', '', s.lower())


tpl_ref = ref_list()[0]
for r in C.REFS:
    np_ = make_par(tpl_ref, [(r, '')])
    k = key(r)
    refs = ref_list()
    for e in refs:
        if key(Paragraph(e, d).text) > k:
            e.addprevious(np_)
            break
    else:
        refs[-1].addnext(np_)

d.save(OUT)
print('saved', OUT)
