"""From pairs to a rate: what the linked-panel leaving rate estimates."""
import sys
sys.path.insert(0, "replication")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import paperstyle  # noqa: F401

SC = "report/figures_deck"
BLUE, CORAL, GREEN, GOLD = "#00549F", "#B5443C", "#3A8A62", "#D9A21B"
INK, MUT, LGRAY = "#1A2430", "#6B7480", "#E5E8EC"

fig = plt.figure(figsize=(13.33, 7.5))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.05, 0.945, "From pairs to a rate", fontsize=25, fontweight="bold",
        color=INK, va="top")
ax.text(0.05, 0.883, "Yes — the linked-panel rate is computed over teacher-month pairs, "
        "not over people. Here is why that is a choice, not a mistake.",
        fontsize=12.5, color=MUT, va="top")

# ---- one teacher, four windows (leaves teaching in February of year 2) ----
ax.text(0.05, 0.80, "One teacher, four windows — she stops teaching in February of the second year:",
        fontsize=11.5, color=INK, fontweight="bold", va="top")
rows = [("Jan → next Jan", "teaching in Jan y+1", "stayer", GREEN),
        ("Feb → next Feb", "not teaching in Feb y+1", "leaver", CORAL),
        ("Mar → next Mar", "not teaching in Mar y+1", "leaver", CORAL),
        ("Apr → next Apr", "not teaching in Apr y+1", "leaver", CORAL)]
y = 0.745
for lab, mid, verdict, c in rows:
    ax.text(0.07, y, lab, fontsize=10.5, color=INK, va="center", family="monospace")
    ax.annotate("", xy=(0.52, y), xytext=(0.27, y),
                arrowprops=dict(arrowstyle="->", color=c, lw=2.0))
    ax.text(0.395, y + 0.016, mid, fontsize=8.6, color=MUT, ha="center")
    ax.add_patch(FancyBboxPatch((0.545, y - 0.017), 0.085, 0.034,
                 boxstyle="round,pad=0.002,rounding_size=0.008", facecolor=c, edgecolor="none"))
    ax.text(0.5875, y, verdict, fontsize=9, color="white", fontweight="bold",
            ha="center", va="center")
    y -= 0.062
ax.text(0.68, 0.715, "Every verdict is true for its own window:\n"
        "she really was still a teacher one year\nafter January, and really gone one year\n"
        "after February, March and April.\n\nDropping any of them would distort\nthe timing of leaving.",
        fontsize=10, color=INK, va="top", linespacing=1.45)

# ---- what the rate is ----
ax.text(0.05, 0.455, "What the number means:", fontsize=11.5, fontweight="bold", color=BLUE, va="top")
ax.text(0.05, 0.415,
        "rate  =  weighted leaver pairs ÷ all teacher-month pairs   —   the probability that a randomly chosen "
        "teaching month\nis followed, twelve months later, by no teaching. A flow probability, not a head count.",
        fontsize=10.5, color=INK, va="top", linespacing=1.4)
BULL = [
 ("Each calendar month is its own representative snapshot (that is what the CPS monthly weight does), so pooling twelve of\n"
  "them per year just averages twelve monthly cohort rates — more precision, same level.", INK),
 ("A person appearing as stayer in one pair and leaver in another is someone who left between two anniversary months.\n"
  "Her pairs contribute the truth of each window; the mixture is the correct accounting of when she left.", INK),
 ("Keeping a single pair per person would estimate the same object with a quarter of the data — noisier, not cleaner.", INK),
]
y = 0.315
for txt, c in BULL:
    ax.text(0.05, y, "–", fontsize=12, fontweight="bold", color=BLUE, va="top")
    ax.text(0.072, y, txt, fontsize=10.5, color=c, va="top", linespacing=1.35)
    y -= 0.073
ax.text(0.05, 0.085,
        "The March recall rate has none of this: one person appears in exactly one ASEC — one record, one verdict.\n"
        "85,497 teachers, 6,931 exits: person-level by construction.",
        fontsize=10.5, color="#3A8A62", fontweight="bold", va="top", linespacing=1.4)
fig.savefig(f"{SC}/u3c_pairs.png", dpi=160)
print("saved u3c")
