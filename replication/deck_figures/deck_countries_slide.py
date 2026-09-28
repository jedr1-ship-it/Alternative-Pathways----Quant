"""Final slide: where this measurement can be replicated."""
import sys
sys.path.insert(0, "replication")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import paperstyle  # noqa: F401
mpl.rcParams.update({"font.serif": ["STIXGeneral", "DejaVu Serif"],
                     "mathtext.fontset": "stix"})
SC = "report/figures_deck"
NAVY, INK, MUT = "#1F4E79", "#1A2430", "#55606B"

fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.07, 0.93, "Where this could be done next", fontsize=24,
        fontweight="bold", color=INK, va="top")
ax.text(0.07, 0.872, "Labour force surveys with the sample size, the access, and a design that observes the same person twelve months apart",
        fontsize=12.5, color=MUT, va="top", style="italic")

COLS = [0.07, 0.20, 0.475, 0.71]
HEAD = ["", "Instrument", "Twelve-month design", "Sample and access"]
ROWS = [
 ("Italy", "Rilevazione sulle Forze di Lavoro (Istat)",
  "official 12-month longitudinal files",
  "linked individual files for research,\nquarterly series since 2004"),
 ("Germany", "Mikrozensus (Destatis)",
  "2-(2)-2 scheme since 2020",
  "≈810,000 persons per year;\nscientific-use files via the RDCs"),
 ("United Kingdom", "Labour Force Survey (ONS)",
  "five waves; first and fifth a year apart",
  "≈100,000 persons per quarter;\nvia the UK Data Service"),
 ("France", "Enquête emploi en continu (INSEE)",
  "six consecutive quarterly interviews",
  "≈80,000 dwellings per quarter;\nresearch files via Progedo / CASD"),
 ("Spain", "Encuesta de Población Activa (INE)",
  "six-quarter rotation; public flow files",
  "≈60,000 dwellings per quarter;\nmicrodata free to download"),
 ("Brazil", "PNAD Contínua (IBGE)",
  "five quarterly visits",
  "≈210,000 households per quarter;\nmicrodata fully public"),
 ("Mexico", "ENOE (INEGI)",
  "five-quarter rotation",
  "≈150,000 dwellings per quarter;\nmicrodata fully public"),
]
ax.plot([0.07, 0.93], [0.795, 0.795], color=INK, lw=1.3)
for x, h in zip(COLS, HEAD):
    ax.text(x, 0.775, h, fontsize=11, fontweight="bold", color=INK, va="top")
ax.plot([0.07, 0.93], [0.745, 0.745], color=INK, lw=0.6)
y = 0.722
for country, inst, design, acc in ROWS:
    ax.text(COLS[0], y, country, fontsize=11, fontweight="bold", color=NAVY, va="top")
    ax.text(COLS[1], y, inst, fontsize=10.5, color=INK, va="top")
    ax.text(COLS[2], y, design, fontsize=10.5, color=INK, va="top")
    ax.text(COLS[3], y, acc, fontsize=10.5, color=INK, va="top", linespacing=1.3)
    y -= 0.076
ax.plot([0.07, 0.93], [y + 0.018, y + 0.018], color=INK, lw=1.3)
ax.text(0.07, y - 0.022,
        "At two to four percent of employment, each survey yields at least as many teacher observations per year as the CPS does here.",
        fontsize=10.5, color=INK, va="top")
ax.text(0.07, y - 0.066,
        "Australia and Canada cannot: their rotations (eight and six months in sample) never observe the same person twelve months apart.",
        fontsize=9.5, color=MUT, va="top")
fig.savefig(f"{SC}/v_countries.png", dpi=160)
print("saved v_countries")
