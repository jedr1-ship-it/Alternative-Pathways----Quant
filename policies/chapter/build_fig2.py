"""Figure 2 of the chapter: primary teachers' actual salaries relative to earnings of tertiary-educated workers.
Input: eag_d3_2.csv with columns country,ratio (ratio as a decimal, e.g. 0.83) taken from
Education at a Glance 2026, Table D3.2 (2025 data), primary teachers. Rows named "OECD average" are
drawn as the dashed line, not as a bar. Output: figure2_salary_ratio.png.
Run: python3 build_fig2.py [input.csv]"""
import sys, csv, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

src = sys.argv[1] if len(sys.argv) > 1 else "eag_d3_2.csv"
rows = [(r["country"].strip(), float(r["ratio"])) for r in csv.DictReader(open(src, encoding="utf8")) if r["ratio"].strip()]
avg = next((v for c, v in rows if c.lower().startswith("oecd")), None)
rows = sorted([(c, v) for c, v in rows if not c.lower().startswith("oecd")], key=lambda t: t[1])

GREEN, RED, INK, MUTED = "#2E8B57", "#B03A3A", "#1A1A1A", "#5F6368"
fig, ax = plt.subplots(figsize=(11, 0.28 * len(rows) + 1.2), dpi=200)
fig.patch.set_facecolor("white")
ax.barh(range(len(rows)), [v for _, v in rows], color=[GREEN if v >= 1 else RED for _, v in rows], height=0.62, zorder=3)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([c for c, _ in rows], fontsize=10)
ax.axvline(1.0, color=INK, lw=1.2, zorder=4)
ax.text(1.01, len(rows) - 0.3, "Parity with other tertiary-educated workers", fontsize=10, color=INK, va="bottom")
if avg is not None:
    ax.axvline(avg, color=MUTED, lw=1.2, ls="--", zorder=4)
    ax.text(avg - 0.01, len(rows) - 0.3, f"OECD average {avg:.2f}", fontsize=10, color=MUTED, va="bottom", ha="right")
ax.set_xlabel("Primary teachers' actual earnings relative to other tertiary-educated workers", fontsize=10.5)
ax.xaxis.grid(True, color="#E3E3E0", lw=0.8, zorder=0)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0); ax.set_ylim(-0.7, len(rows) + 0.4); ax.set_xlim(0, max(1.6, max(v for _, v in rows) + 0.05))
fig.subplots_adjust(left=0.2, right=0.98, top=0.98, bottom=0.08)
out = "figure2_salary_ratio.png"; fig.savefig(out, facecolor="white"); print("written", out, len(rows), "countries")
