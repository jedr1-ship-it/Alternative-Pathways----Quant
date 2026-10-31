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


def _el(tag, **attrs):
    from docx.oxml import OxmlElement
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn('w:' + k), str(v))
    return e


def _cell(text, width, span=1, vmerge=None, fill=None, bold=False,
          italic=False, center=False, size=17, top='single', bottom='single', keep=False):
    tc = _el('w:tc')
    pr = _el('w:tcPr')
    pr.append(_el('w:tcW', w=width, type='dxa'))
    if span > 1:
        pr.append(_el('w:gridSpan', val=span))
    if vmerge is not None:
        pr.append(_el('w:vMerge', **({'val': 'restart'} if vmerge == 'restart' else {})))
    b = _el('w:tcBorders')
    b.append(_el('w:top', val=top, sz=8, space=0, color='888888' if fill else 'auto') if top != 'nil' else _el('w:top', val='nil'))
    b.append(_el('w:left', val='nil'))
    b.append(_el('w:bottom', val=bottom, sz=8, space=0, color='auto'))
    b.append(_el('w:right', val='nil'))
    pr.append(b)
    if fill:
        pr.append(_el('w:shd', val='clear', color='auto', fill=fill))
    m = _el('w:tcMar')
    for side, w in (('top', 40), ('left', 70), ('bottom', 40), ('right', 70)):
        m.append(_el('w:' + side, w=w, type='dxa'))
    pr.append(m)
    pr.append(_el('w:vAlign', val='center' if center else 'top'))
    tc.append(pr)
    p = _el('w:p')
    ppr = _el('w:pPr')
    if keep:
        ppr.append(_el('w:keepNext'))
    ppr.append(_el('w:spacing', before=0, after=0, line=240, lineRule='auto'))
    if center:
        ppr.append(_el('w:jc', val='center'))
    p.append(ppr)
    if text:
        r = _el('w:r')
        rpr = _el('w:rPr')
        if bold:
            rpr.append(_el('w:b'))
        if italic:
            rpr.append(_el('w:i'))
        rpr.append(_el('w:sz', val=size))
        rpr.append(_el('w:szCs', val=size))
        r.append(rpr)
        t = _el('w:t')
        t.text = typo(text)
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        r.append(t)
        p.append(r)
    tc.append(p)
    return tc


def make_table(spec):
    W = spec['widths']
    ncol = len(W)
    c0, c1 = spec.get('center_from', 99), spec.get('center_to', -1)
    SZ = spec.get('size', 17)
    tbl = _el('w:tbl')
    tp = _el('w:tblPr')
    tp.append(_el('w:tblW', w=sum(W), type='dxa'))
    tp.append(_el('w:tblLayout', type='fixed'))
    tp.append(_el('w:tblLook', val='04A0', firstRow=1, lastRow=0,
                  firstColumn=0, lastColumn=0, noHBand=1, noVBand=1))
    tbl.append(tp)
    g = _el('w:tblGrid')
    for w in W:
        g.append(_el('w:gridCol', w=w))
    tbl.append(g)
    HEAD = 'E8EEF4'
    # header rows with colspan and rowspan
    pending = {}  # grid col -> remaining rows of a vertical merge
    nh = len(spec['head'])
    for hi, hrow in enumerate(spec['head']):
        tr = _el('w:tr')
        trpr = _el('w:trPr')
        trpr.append(_el('w:cantSplit'))
        trpr.append(_el('w:tblHeader'))
        tr.append(trpr)
        col, it = 0, iter(hrow)
        while col < ncol:
            if pending.get(col, 0) > 0:
                pending[col] -= 1
                tr.append(_cell('', W[col], vmerge='cont', fill=HEAD, bold=True, size=SZ))
                col += 1
                continue
            text, span, rspan = next(it)
            w = sum(W[col:col + span])
            vm = 'restart' if rspan > 1 else None
            if rspan > 1:
                pending[col] = rspan - 1
            ctr = span > 1 or (c0 <= col <= c1)
            tr.append(_cell(text, w, span=span, vmerge=vm, fill=HEAD, bold=True,
                            center=ctr, size=SZ))
            col += span
        tbl.append(tr)
    for row in spec['rows']:
        tr = _el('w:tr')
        trpr = _el('w:trPr')
        trpr.append(_el('w:cantSplit'))
        tr.append(trpr)
        if row[0] == 'group':
            tr.append(_cell(row[1], sum(W), span=ncol, fill='F4F7FA', bold=True,
                            italic=True, size=SZ, top='nil', keep=True))
        else:
            for j, (txt, w) in enumerate(zip(row, W)):
                tr.append(_cell(txt, w, center=(c0 <= j <= c1), size=SZ, top='nil'))
        tbl.append(tr)
    return tbl


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
    elif k == 'sub':
        sp = make_par(T_SRC, [(blk[1], 'i')])
        keep_next(sp)
        new.append(sp)
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
