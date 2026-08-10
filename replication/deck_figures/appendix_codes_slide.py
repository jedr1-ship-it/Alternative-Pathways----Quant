"""Appendix slide - the occupation codes that define a teacher, by survey
regime, and how they map across the three Census classifications."""
import sys
sys.path.insert(0, "replication")
import matplotlib.pyplot as plt
import paperstyle  # noqa: F401

OUT = "report/figures_deck"
BLUE, CORAL, DARK, MUT = "#2A5DB0", "#C4534B", "#3B4046", "#8A9096"
BAND = "#F4F6F8"

COLS = [
    ("Surveys 1998–2002", "teaching years 1997–2001",
     "1990 Census classification",
     [("155", "Teachers, prekindergarten and kindergarten"),
      ("156", "Teachers, elementary school†"),
      ("157", "Teachers, secondary school†"),
      ("158", "Teachers, special education"),
      ("159", "Teachers, n.e.c. (not elsewhere classified)")]),
    ("Surveys 2003–2019", "teaching years 2002–2018",
     "2002/2010 Census classification (SOC)",
     [("2300", "Preschool and kindergarten teachers"),
      ("2310", "Elementary and middle school teachers†"),
      ("2320", "Secondary school teachers"),
      ("2330", "Special education teachers"),
      ("2340", "Other teachers and instructors")]),
    ("Surveys 2020–2025", "teaching years 2019–2024",
     "2018 Census classification (SOC 2018)",
     [("2300", "Preschool and kindergarten teachers"),
      ("2310", "Elementary and middle school teachers†"),
      ("2320", "Secondary school teachers"),
      ("2330", "Special education teachers"),
      ("2360", "Other teachers and instructors")]),
]

EXCLUDED = ("Never included (they carry their own codes, outside the set):  postsecondary teachers (2200s)  ·  "
            "tutors (2350, 2018 cl.)\nteaching assistants (2540/2545)  ·  childcare workers (4600)  ·  "
            "education administrators (0230)")

NOTES = [
    ("Yes", "as a block: the K–12 teaching group maps one-to-one across the three classifications. "
            "Every figure uses the union of the codes, never a sub-code across regimes."),
    ("†",   "sub-codes are not: middle-school teachers sit under elementary or secondary before 2003 and with "
            "elementary (2310) after; “other teachers” is renumbered 2340 → 2360 in 2020."),
    ("Yes", "within each survey: last year’s job (OCCUP) and the current job (PEIOOCC) share one classification, "
            "so no leaver/switch comparison straddles a code change (seam surveys: 2003 and 2020)."),
    ("Yes", "for people, but only two years: the CPS links the same person across two "
            "consecutive March interviews (PERIDNUM), never longer."),
]

fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

ax.text(0.045, 0.935, "Who counts as a teacher",
        fontsize=23, color=DARK, fontweight="bold", va="top")
ax.text(0.045, 0.868, "Occupation of the longest job held last year, CPS ASEC — "
        "three Census classifications, 28 survey years",
        fontsize=12, color=MUT, va="top")

xs = [0.045, 0.375, 0.705]
colw = 0.28
y_head = 0.775
row_ys = [0.615, 0.545, 0.475, 0.405, 0.335]

for i, y in enumerate(row_ys):
    if i % 2 == 0:
        ax.axhspan(y - 0.028, y + 0.040, xmin=0.035, xmax=0.985,
                   color=BAND, lw=0, zorder=0)

for x, (yrs, cal, cls, rows) in zip(xs, COLS):
    ax.text(x, y_head, yrs, fontsize=13.5, color=BLUE, fontweight="bold", va="top")
    ax.text(x, y_head - 0.042, cal, fontsize=10, color=MUT, va="top")
    ax.text(x, y_head - 0.082, cls, fontsize=10, color=DARK, va="top", style="italic")
    for (code, lab), y in zip(rows, row_ys):
        ax.text(x, y, code, fontsize=11.5, color=BLUE, fontweight="bold",
                va="center", family="monospace")
        ax.text(x + 0.055, y, lab, fontsize=10.5, color=DARK, va="center")

ax.text(0.045, 0.292, EXCLUDED, fontsize=9.3, color=MUT, va="top",
        style="italic", linespacing=1.6)

ax.text(0.045, 0.228, "Are the codes traceable across census years?",
        fontsize=12.5, color=DARK, fontweight="bold", va="top")
yn = 0.18
for mark, txt in NOTES:
    c = CORAL if mark == "†" else "#3E7C59"
    ax.text(0.048, yn, mark, fontsize=10, color=c, fontweight="bold", va="top")
    ax.text(0.082, yn, txt, fontsize=9.6, color=DARK, va="top", wrap=True)
    yn -= 0.05

fig.savefig(f"{OUT}/codes_slide.png", dpi=200)
fig.savefig(f"{OUT}/codes_slide.pdf")
print("saved codes_slide")
