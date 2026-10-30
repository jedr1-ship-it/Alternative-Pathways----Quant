import copy, re, sys
sys.path.insert(0, '.')
import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
import section3_content as C

SRC, OUT = sys.argv[1], sys.argv[2]
d = docx.Document(SRC)
body = d.element.body
els = list(body)

def find_p(text, style=None):
    for e in body:
        if e.tag == qn('w:p'):
            p = Paragraph(e, d)
            if p.text.strip().startswith(text) and (style is None or p.style.name == style):
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
T_TBL = tbls[0]   # Table 1
T_BOX = tbls[1]   # Box 1
assert 'Box 1' in ''.join(T_BOX.itertext())

RUNLIKE = (qn('w:r'), qn('w:hyperlink'), qn('w:proofErr'), qn('w:bookmarkStart'),
           qn('w:bookmarkEnd'), qn('w:ins'), qn('w:del'), qn('w:smartTag'))

def first_run(p):
    return next(iter(p.iter(qn('w:r'))))

def set_flag(rpr, tag, on):
    for x in rpr.findall(qn(tag)):
        rpr.remove(x)
    if on:
        el = rpr.makeelement(qn(tag), {})
        # keep schema order loosely: b/i near the start
        rpr.insert(0, el)

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
        set_flag(rpr, 'w:iCs', True); set_flag(rpr, 'w:i', True)
    if 'b' in style:
        set_flag(rpr, 'w:bCs', True); set_flag(rpr, 'w:b', True)
    t = r.makeelement(qn('w:t'), {})
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r.append(t)
    return r

def make_par(tpl_p, runs, keep_bold=None):
    """runs: list of (text, style). If keep_bold is True/False, overrides."""
    tr = first_run(tpl_p)
    p = copy.deepcopy(tpl_p)
    for c in list(p):
        if c.tag != qn('w:pPr'):
            p.remove(c)
    for text, st in runs:
        p.append(make_run(tr, text, st))
    return p

def italic_runs(text):
    """split *...* markers into italic runs"""
    out = []
    for i, part in enumerate(re.split(r'\*', text)):
        if part:
            out.append((part, 'i' if i % 2 else ''))
    return out

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
        ppr = cp.find(qn('w:pPr'))
        if ppr.find(qn('w:keepNext')) is None:
            ps_ = ppr.find(qn('w:pStyle'))
            kn = ppr.makeelement(qn('w:keepNext'), {})
            (ps_.addnext(kn) if ps_ is not None else ppr.insert(0, kn))
        new.append(cp)
    elif k == 'src':
        new.append(make_par(T_SRC, [(blk[1], '')]))
    elif k == 'table2':
        t = copy.deepcopy(T_TBL)
        rows = t.findall(qn('w:tr'))
        for r in rows[len(C.TABLE2):]:
            t.remove(r)
        for r, (a, b) in zip(t.findall(qn('w:tr')), C.TABLE2):
            for tc, txt in zip(r.findall(qn('w:tc')), (a, b)):
                ps = tc.findall(qn('w:p'))
                tpl = ps[0]
                hdr_bold = any(x is not None for x in [first_run(tpl).find(qn('w:rPr'))]) and \
                    first_run(tpl).find(qn('w:rPr')).find(qn('w:b')) is not None
                np_ = make_par(tpl, [(txt, 'b' if hdr_bold else '')])
                for x in ps:
                    tc.remove(x)
                tc.append(np_)
        W = (2100, 6960)
        for gc, w in zip(t.find(qn('w:tblGrid')).findall(qn('w:gridCol')), W):
            gc.set(qn('w:w'), str(w))
        for r in t.findall(qn('w:tr')):
            for tc, w in zip(r.findall(qn('w:tc')), W):
                tcw = tc.find(qn('w:tcPr')).find(qn('w:tcW'))
                if tcw is not None:
                    tcw.set(qn('w:w'), str(w)); tcw.set(qn('w:type'), 'dxa')
        rows = t.findall(qn('w:tr'))
        for n, r in enumerate(rows):
            trpr = r.find(qn('w:trPr'))
            if trpr is None:
                trpr = r.makeelement(qn('w:trPr'), {}); r.insert(0 if r.find(qn('w:tblPrEx')) is None else 1, trpr)
            if trpr.find(qn('w:cantSplit')) is None:
                trpr.insert(0, trpr.makeelement(qn('w:cantSplit'), {}))
            if n < len(rows) - 1:
                for pp in r.iter(qn('w:p')):
                    ppr = pp.find(qn('w:pPr'))
                    if ppr is None:
                        ppr = pp.makeelement(qn('w:pPr'), {}); pp.insert(0, ppr)
                    if ppr.find(qn('w:keepNext')) is None:
                        ps_ = ppr.find(qn('w:pStyle'))
                        kn = ppr.makeelement(qn('w:keepNext'), {})
                        if ps_ is not None: ps_.addnext(kn)
                        else: ppr.insert(0, kn)
        new.append(t)
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
        new.append(t)
        # spacer paragraph after each box, as after Box 1
        new.append(make_par(T_P, [('', '')]))

# remove placeholders between "3. The policies" and "4. Conclusions"
idx_h1 = list(body).index(H1)
idx_c = list(body).index(CONC)
for e in list(body)[idx_h1 + 1: idx_c]:
    body.remove(e)
anchor = H1
for e in new:
    anchor.addnext(e)
    anchor = e
anchor.addnext(make_par(T_P, [('', '')]))

# references: insert alphabetically after "References" heading
REFH = find_p('References', 'Heading 2')
refs = []
e = REFH.getnext()
while e is not None and e.tag == qn('w:p'):
    refs.append(e); e = e.getnext()
tpl_ref = refs[0]

def ref_runs(s):
    # italicise the title: quoted article -> journal; otherwise first segment after "), "
    m = re.match(r'^(.*?\(\d{4}[a-z]?\), )(.*)$', s)
    head, rest = m.group(1), m.group(2)
    if rest.startswith('"'):
        m2 = re.match(r'^(".*?", )(.*?)(, (Vol\.|https|pp\.).*|$)', rest)
        if m2 and not m2.group(2).startswith('in '):
            return [(head + m2.group(1), ''), (m2.group(2), 'i'), (m2.group(3), '')]
        m3 = re.match(r'^(".*?", in )(.*?)(, .*)$', rest)
        if m3:
            return [(head + m3.group(1), ''), (m3.group(2), 'i'), (m3.group(3), '')]
        return [(s, '')]
    j = rest.find(', ')
    return [(head, ''), (rest[:j], 'i'), (rest[j:], '')]

def key(s):
    return re.sub(r'[^a-z0-9 ]', '', s.lower().replace('é', 'e').replace('ä', 'a').replace('ü', 'u').replace('ö', 'o'))

for r in C.REFS:
    np_ = make_par(tpl_ref, ref_runs(r))
    k = key(r)
    placed = False
    for e in refs:
        if key(Paragraph(e, d).text) > k:
            e.addprevious(np_); placed = True; break
    if not placed:
        refs[-1].addnext(np_)
    refs = []
    e = REFH.getnext()
    while e is not None and e.tag == qn('w:p'):
        refs.append(e); e = e.getnext()

d.save(OUT)
print('saved', OUT)
