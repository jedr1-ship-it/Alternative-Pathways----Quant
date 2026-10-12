"""PowerPoint version of the Data Cluster deck, built as an exact image
of the Beamer PDF: each page of report/data_cluster/main.pdf is rendered
at 200 dpi and placed full-bleed on a 16:9 slide, and every internal
link annotation of the PDF (the appendix buttons and the back buttons)
becomes a transparent clickable rectangle wired to the same target
slide. Spanish speaker notes are attached to the slides that carry a
guion. Output: report/data_cluster/Proyect_US_cluster.pptx.
Run from the repo root after compiling the Beamer deck twice."""
import glob
import os
import subprocess

import pypdf
from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.enum.shapes import MSO_SHAPE

PDF = "report/data_cluster/main.pdf"
OUT = "report/data_cluster/Proyect_US_cluster.pptx"
TMP = "report/data_cluster/_pages"
SLIDE_W, SLIDE_H = Inches(13.333), Inches(7.5)

# ---------- render pages ----------
os.makedirs(TMP, exist_ok=True)
for f in glob.glob(f"{TMP}/pg*.png"):
    os.remove(f)
subprocess.run(["pdftoppm", "-png", "-r", "200", PDF, f"{TMP}/pg"],
               check=True)
pages = sorted(glob.glob(f"{TMP}/pg-*.png"))
print(f"rendered {len(pages)} pages")

# ---------- read the PDF's internal links ----------
r = pypdf.PdfReader(PDF)
idx = {p.indirect_reference.idnum: i for i, p in enumerate(r.pages)}
box = r.pages[0].mediabox
PW, PH = float(box.width), float(box.height)
links = []   # (page_index, x0, y0, x1, y1, target_index), PDF points
for i, p in enumerate(r.pages):
    for a in (p.get("/Annots") or []):
        o = a.get_object()
        if o.get("/Subtype") != "/Link":
            continue
        raw = None
        if "/A" in o:
            act = o["/A"].get_object()
            if act.get("/S") == "/GoTo":
                raw = act.get("/D")
        elif "/Dest" in o:
            raw = o["/Dest"]
        if raw is None:
            continue
        if isinstance(raw, str):
            d = r.named_destinations.get(raw)
            tgt = idx.get(d.page.idnum) if d is not None else None
        else:
            d0 = raw[0]
            tgt = idx.get(getattr(d0, "idnum", None))
        if tgt is None:
            continue
        x0, y0, x1, y1 = (float(v) for v in o["/Rect"])
        links.append((i, x0, y0, x1, y1, tgt))
print(f"{len(links)} internal links")

# ---------- Spanish speaker notes ----------
NOTES = {
    2: ("Motivacion: entender por que los profesores dejan la profesion y "
        "si hay un margen real de politica para suavizar la escasez "
        "reteniendolos o trayendolos de vuelta. Problema: en muchos paises "
        "no hay microdatos oficiales publicos; empezamos por Estados "
        "Unidos, el pais con mas informacion. Boton: fuentes oficiales y "
        "sus huecos temporales."),
    12: ("Las seis definiciones en un eje: de la mas laxa (17.5) a la mas "
         "estricta (10.5) y el recall anual (8.6). Los rombos negros son "
         "el benchmark oficial del NCES (Teacher Follow-up Survey, 8.0): "
         "nuestra medida retrospectiva aterriza justo encima."),
    14: ("Serie estable. Promedios EAG para paises con datos: 6.6 (datos "
         "2016, EAG 2021), 6.5 (2022/23, EAG 2025), 6.4 (2024/25, EAG "
         "2026). Los paises con series largas (Nueva Zelanda, Suecia, "
         "Israel, Noruega) tambien son estables. EEUU esta por encima de "
         "la mayoria de los que publican tasa."),
    18: ("De cada 100 que dejan la docencia: 29 a otro empleo, 36 fuera "
         "de la poblacion activa con 55 o mas (retiro), 24 fuera antes de "
         "los 55 y 11 en paro. De los 29 empleados: 6 siguen en "
         "educacion, 2 en cuidado, 9 en otras profesiones y 11 en "
         "ventas, oficina y manual."),
    20: ("El grupo que sale antes de los 55: mas de la mitad son madres "
         "con un hijo en casa (13 de los 24). El 13 por ciento del grupo "
         "estudia, casi todos sin hijos: 25 por ciento de esas mujeres y "
         "48 por ciento de esos hombres, frente al 3 por ciento de las "
         "madres."),
    23: ("a: vinculacion al empleo (ano completo, tiempo parcial). c: "
         "compensacion (plan de pension, sector publico, renta del hogar "
         "en el cuartil inferior). f: familia (bebe, hijos, estado "
         "civil). h: salud (salud declarada, discapacidad). d: "
         "demografia (edad, sexo, raza, educacion). delta-t: efectos de "
         "ano. El LPM no esta acotado (22 por ciento de los ajustados "
         "por debajo de cero), asi que el probit es la especificacion "
         "principal; las variantes LPM estan en el anexo."),
}

# ---------- build ----------
prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
blank = prs.slide_layouts[6]
slides = []
for n, png in enumerate(pages, start=1):
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture(png, 0, 0, width=SLIDE_W, height=SLIDE_H)
    if n in NOTES:
        s.notes_slide.notes_text_frame.text = NOTES[n]
    slides.append(s)

for i, x0, y0, x1, y1, tgt in links:
    # PDF points (origin bottom-left) -> slide EMU (origin top-left),
    # with a small padding so the hotspot is easy to hit
    pad = 2.0
    x0, x1 = max(x0 - pad, 0), min(x1 + pad, PW)
    yt = min(y1 + pad, PH)
    yb = max(y0 - pad, 0)
    left = Emu(int(x0 / PW * SLIDE_W))
    top = Emu(int((PH - yt) / PH * SLIDE_H))
    w = Emu(int((x1 - x0) / PW * SLIDE_W))
    h = Emu(int((yt - yb) / PH * SLIDE_H))
    sh = slides[i].shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, w, h)
    sh.fill.background()
    sh.line.fill.background()
    sh.shadow.inherit = False
    sh.click_action.target_slide = slides[tgt]

prs.save(OUT)
print("saved", OUT, f"({os.path.getsize(OUT)/1e6:.1f} MB)")
