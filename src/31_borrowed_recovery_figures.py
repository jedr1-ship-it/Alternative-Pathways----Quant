"""
Figures for "A Borrowed Recovery?" (US brief), from outputs/br_*.csv.
Six figures, house style (paperstyle), saved to report/figures/br_fig*.pdf.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from paperstyle import *

FIG = "report/figures"
os.makedirs(FIG, exist_ok=True)

stock = pd.read_csv("outputs/br_stock_by_year.csv")
enr = pd.read_csv("outputs/br_enrollment.csv")
attr = pd.read_csv("outputs/br_attrition_year.csv")
age = pd.read_csv("outputs/br_attrition_age.csv")
pay = pd.read_csv("outputs/br_pay_by_year.csv")
flows = pd.read_csv("outputs/br_flows.csv")
mkt = pd.read_csv("outputs/br_market.csv")


def endlab(ax, x, y, txt, color, dy=0):
    ax.annotate(txt, (x, y), xytext=(6, dy), textcoords="offset points",
                va="center", fontsize=9.5, color=color, fontweight="bold")


def yearticks(ax, lo=2005, hi=2025):
    ax.set_xticks(range(lo, hi + 1, 5))
    ax.set_xticks(range(lo, hi + 1), minor=True)


def title(ax, txt):
    ax.set_title(txt, loc="left", fontsize=12.5, fontweight="bold", pad=10)


# ------------------------------------------------ fig 1: pupils vs teachers
def fig1():
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    tb = stock.set_index("year")["total"].loc[2005:2025]
    eb = enr.set_index("fall")["enrollment_k"].loc[2005:2024]
    ti = tb / tb.loc[2010] * 100
    ei = eb / eb.loc[2010] * 100
    ax.axhline(100, color=GRAY, lw=0.6, ls=":")
    ax.axvspan(2019.5, 2025.5, color=GRAY, alpha=0.07, lw=0)
    ax.plot(ei.index, ei.values, color=CORAL, lw=2.6)
    ax.plot(ti.index, ti.values, color=BLUE, lw=2.2, marker="o", ms=3.4)
    endlab(ax, ti.index[-1], ti.iloc[-1], f"teachers\n{ti.iloc[-1]:.0f}",
           BLUE, dy=2)
    endlab(ax, ei.index[-1], ei.iloc[-1], f"pupils\n{ei.iloc[-1]:.0f}",
           CORAL, dy=-8)
    ax.annotate("2019 peaks", (2019, ti.loc[2019]), xytext=(-46, 8),
                textcoords="offset points", fontsize=9, color=SUBTLE)
    ax.set_xlim(2005, 2027.6)
    yearticks(ax)
    ax.set_ylabel("index, 2010 = 100")
    title(ax, "Enrolment is falling; in 2025 the teaching stock fell too")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig1_pupils_teachers.pdf")
    plt.close(fig)


# ------------------------------------------------ fig 2: the wastage cycle
def fig2():
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    a = attr.sort_values("base_year")
    pre = a[a.base_year <= 2018]["attr12"].mean()
    ax.axhline(pre, color=GRAY, lw=0.8, ls=":")
    ax.text(2005.1, pre - .45, f"2005–18 average ({pre:.1f}%)",
            fontsize=8.5, color=GRAY)
    ax.plot(a.base_year, a.attr12, color=BLUE, lw=2.6, zorder=3)
    ax.plot(a.base_year, a.attrp_all, color=GRAY, lw=1.6, ls="--", zorder=2)
    notes = {2019: "2019→20\n(COVID year)", 2022: "2022 peak",
             2024: "2024→25"}
    for y, lab in notes.items():
        v = a.loc[a.base_year == y, "attr12"].iloc[0]
        ax.scatter([y], [v], s=42, color=CORAL, zorder=4)
        ax.annotate(f"{lab}\n{v:.1f}%", (y, v), xytext=(0, 12),
                    textcoords="offset points", ha="center",
                    fontsize=8.8, color=CORAL, fontweight="bold")
    ax.text(a.base_year.iloc[-1] + .5, a.attrp_all.dropna().iloc[-1],
            "persistent\nleavers", fontsize=9, color=GRAY, va="center")
    ax.text(2005.3, 19.6, "12-month leaver rate", fontsize=9.5,
            color=BLUE, fontweight="bold")
    ax.set_xlim(2005, 2026.4)
    ax.set_ylim(10, 20.4)
    yearticks(ax)
    ax.set_ylabel("share of teachers leaving within 12 months (%)")
    title(ax, "Off the peak, but stuck above the old normal")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig2_attrition.pdf")
    plt.close(fig)


# ------------------------------------------- fig 3: attrition by age band
def fig3():
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    colors = {"under 30": CORAL, "30-39": GOLD, "40-49": GREEN, "50+": BLUE}
    dy = {"under 30": 6, "30-39": 5, "40-49": -6, "50+": 0}
    for band, g in age.groupby("band"):
        g = g.sort_values("base_year")
        ma = g.attr12.rolling(3, center=True, min_periods=2).mean()
        ax.plot(g.base_year, ma, color=colors[band], lw=2.2)
        endlab(ax, g.base_year.iloc[-1], ma.iloc[-1], band, colors[band],
               dy=dy[band])
    ax.set_xlim(2005, 2027)
    yearticks(ax)
    ax.set_ylabel("12-month leaver rate, 3-yr moving avg (%)")
    title(ax, "The rise has been steepest among the youngest teachers")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig3_age.pdf")
    plt.close(fig)


# ---------------------------------------------------- fig 4: real weekly pay
def fig4():
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    p = pay.sort_values("year")
    ax.axhline(100, color=GRAY, lw=0.6, ls=":")
    ax.plot(p.year, p.ba_idx, color=GRAY, lw=2.0)
    ax.plot(p.year, p.all_idx, color=GOLD, lw=2.0)
    ax.plot(p.year, p.teacher_idx, color=BLUE, lw=2.6)
    endlab(ax, p.year.iloc[-1], p.teacher_idx.iloc[-1],
           f"teachers\n{p.teacher_idx.iloc[-1]:.0f}", BLUE, dy=-2)
    endlab(ax, p.year.iloc[-1], p.ba_idx.iloc[-1],
           f"graduates (BA+)\n{p.ba_idx.iloc[-1]:.0f}", SUBTLE, dy=4)
    endlab(ax, p.year.iloc[-1], p.all_idx.iloc[-1],
           f"all workers\n{p.all_idx.iloc[-1]:.0f}", GOLD, dy=14)
    ax.set_xlim(2005, 2028.6)
    yearticks(ax)
    ax.set_ylabel("real median weekly earnings, 2010 = 100")
    title(ax, "Teacher pay has fallen behind other graduates")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig4_pay.pdf")
    plt.close(fig)


# ------------------------------------------------- fig 5: entry vs exit
def fig5():
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    f = flows.sort_values("base_year")
    ex = f.exit_rate.rolling(3, center=True, min_periods=2).mean()
    en = f.entry_rate.rolling(3, center=True, min_periods=2).mean()
    ax.plot(f.base_year, f.exit_rate, color=CORAL, lw=0.9, alpha=0.35)
    ax.plot(f.base_year, f.entry_rate, color=GREEN, lw=0.9, alpha=0.35)
    ax.plot(f.base_year, ex, color=CORAL, lw=2.6)
    ax.plot(f.base_year, en, color=GREEN, lw=2.6)
    ax.fill_between(f.base_year, en, ex, where=ex >= en,
                    color=CORAL, alpha=0.14, lw=0)
    ax.fill_between(f.base_year, en, ex, where=ex < en,
                    color=GREEN, alpha=0.14, lw=0)
    endlab(ax, f.base_year.iloc[-1], ex.iloc[-1],
           f"exits\n{f.exit_rate.iloc[-1]:.1f}%", CORAL, dy=4)
    endlab(ax, f.base_year.iloc[-1], en.iloc[-1],
           f"entries\n{f.entry_rate.iloc[-1]:.1f}%", GREEN, dy=-8)
    ax.set_xlim(2005, 2027)
    yearticks(ax, 2005, 2024)
    ax.set_ylabel("gross flows, % of the teaching stock")
    title(ax, "In 2024–25 exits outpaced entries")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig5_flows.pdf")
    plt.close(fig)


# --------------------------------------- fig 6: the borrowed-recovery test
def fig6():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.0),
                                  gridspec_kw={"width_ratios": [1.45, 1]})
    m = mkt.dropna(subset=["attr12"]).sort_values("year")
    ax.plot(m.year, m.attr12, color=BLUE, lw=2.6)
    ax.set_ylabel("teacher leaver rate (%)", color=BLUE)
    ax.tick_params(axis="y", labelcolor=BLUE)
    axr = ax.twinx()
    axr.plot(m.year, m.quits_private, color=CORAL, lw=2.2, ls="--")
    axr.set_ylabel("private-sector quits rate (%)", color=CORAL)
    axr.tick_params(axis="y", labelcolor=CORAL)
    axr.spines["right"].set_visible(True)
    ax.axvspan(2022.4, 2024.6, color=GRAY, alpha=0.10, lw=0)
    ax.annotate("the market cools;\nteachers keep leaving",
                xy=(2023.4, 17.2), xytext=(2007, 17.9), fontsize=8.8,
                color=SUBTLE, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8,
                                connectionstyle="arc3,rad=-0.18"))
    ax.set_xlim(2005, 2025)
    yearticks(ax, 2005, 2024)
    title(ax, "Teachers quit when everyone quits — until now")

    r = np.corrcoef(m.attr12, m.quits_private)[0, 1]
    b, a = np.polyfit(m.quits_private, m.attr12, 1)
    xs = np.linspace(m.quits_private.min() - .05,
                     m.quits_private.max() + .05, 50)
    ax2.plot(xs, a + b * xs, color=GRAY, lw=1.4)
    ax2.scatter(m.quits_private, m.attr12, s=26, color=BLUE, zorder=3)
    hl = m[m.year == 2024]
    ax2.scatter(hl.quits_private, hl.attr12, s=52, color=CORAL, zorder=4)
    for y in (2009, 2019, 2022, 2024):
        row = m[m.year == y]
        if len(row):
            ax2.annotate(str(y), (row.quits_private.iloc[0],
                                  row.attr12.iloc[0]),
                         xytext=(5, 4), textcoords="offset points",
                         fontsize=8.5,
                         color=CORAL if y == 2024 else SUBTLE,
                         fontweight="bold" if y == 2024 else "normal")
    ax2.set_xlabel("private quits rate (%)")
    ax2.set_ylabel("teacher leaver rate (%)")
    title(ax2, f"r = {r:+.2f}")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig6_market.pdf")
    plt.close(fig)


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print("figures saved to", FIG)
