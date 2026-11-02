"""Find the page of every TOC entry in a rendered PDF. Usage: toc_pages.py DOCX.toc.json PDF OUT.json"""
import json, re, subprocess, sys
ents = json.load(open(sys.argv[1])); pdf = sys.argv[2]
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
norm = lambda s: re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip()
P = [norm(subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout) for i in range(1, n + 1)]
toc = next(i for i, p in enumerate(P) if 'Table of contents' in p[:60])
out = {}; start = toc + 1
for t in ents:
    key = norm(t)[:45]
    rng = range(0, toc) if t in ('Abstract', 'Résumé') else range(start, n)
    out[t] = next((i + 1 for i in rng if key in P[i]), '')
    if out[t] and t not in ('Abstract', 'Résumé'):
        start = out[t] - 1
print('missing:', [t for t in ents if not out[t]])
json.dump(out, open(sys.argv[3], 'w'))
