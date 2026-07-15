"""
Figures for "A Borrowed Recovery?" (US brief), from outputs/br_*.csv.
House style (paperstyle), saved to report/figures/br_fig*.pdf.
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
mkt = pd.read_csv("outputs/br_market.csv")


def endlab(ax, x, y, txt, color, dy=0, dx=6, fs=9.5):
    ax.annotate(txt, (x, y), xytext=(dx, dy), textcoords="offset points",
                va="center", fontsize=fs, color=color, fontweight="bold")


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
    ax.plot(ei.index, ei.values, color=CORAL, lw=2.6)
    ax.plot(ti.index, ti.values, color=BLUE, lw=2.4, marker="o", ms=3.0)
    ax.scatter([2025], [ti.loc[2025]], s=46, color=BLUE, zorder=4)
    endlab(ax, ti.index[-1], ti.loc[2025], "teachers:\n−3.7% in 2025",
           BLUE, dy=2)
    endlab(ax, ei.index[-1], ei.iloc[-1],
           "pupils: peak 2019,\n−1.4M since", CORAL, dy=-13, dx=10)
    ax.set_xlim(2005, 2028.6)
    ax.set_ylim(93.5, 113)
    yearticks(ax)
    ax.set_ylabel("index, 2010 = 100")
    title(ax, "Pupils have been leaving since 2019; in 2025 teachers followed")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig1_pupils_teachers.pdf")
    plt.close(fig)


# ------------------------------------------------ fig 2: the two exit doors
def fig2():
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    a = attr.sort_values("base_year")
    pre = a[a.base_year <= 2018]["sector_leaver"].mean()
    ax.axhline(pre, color=GRAY, lw=0.8, ls=":", xmax=0.845)
    ax.text(2025.0, 7.06, f"2005–18\naverage, {pre:.1f}%",
            fontsize=8.2, color=GRAY, va="top")
    ax.fill_between(a.base_year, a.sector_leaver, a.class_leaver,
                    color=GOLD, alpha=0.18, lw=0)
    ax.plot(a.base_year, a.class_leaver, color=SUBTLE, lw=1.9, ls="--",
            zorder=2)
    ax.plot(a.base_year, a.sector_leaver, color=BLUE, lw=2.7, zorder=3)
    v19 = a.loc[a.base_year == 2019, "sector_leaver"].iloc[0]
    ax.scatter([2019], [v19], s=44, color=CORAL, zorder=4)
    ax.annotate(f"pandemic spike, {v19:.1f}%",
                xy=(2019, v19), xytext=(2014.2, 14.8), ha="center",
                fontsize=8.8, color=CORAL, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=CORAL, lw=0.8,
                                connectionstyle="arc3,rad=-0.2"))
    # record wedge bracket at 2024
    y0 = a.sector_leaver.iloc[-1]
    y1 = a.class_leaver.iloc[-1]
    ax.annotate("", xy=(2024.35, y1), xytext=(2024.35, y0),
                arrowprops=dict(arrowstyle="<->", color="#8a6d1a", lw=1.3))
    ax.annotate("5.3 pp stay in education\nbut leave the classroom:\na record",
                (2024.45, (y0 + y1) / 2), xytext=(8, 0),
                textcoords="offset points", va="center", fontsize=8.8,
                color="#8a6d1a", fontweight="bold")
    ax.text(2007.6, 12.35, "left the classroom", fontsize=9, color=SUBTLE,
            fontweight="bold")
    ax.text(2010.5, 6.3, "left education entirely", fontsize=9, color=BLUE,
            fontweight="bold")
    endlab(ax, 2024, y1, f"{y1:.1f}%", SUBTLE, dy=9, dx=-11, fs=9)
    endlab(ax, 2024, y0, f"{y0:.1f}%", BLUE, dy=-11, dx=-11, fs=9)
    ax.set_xlim(2005, 2028.4)
    ax.set_ylim(4, 16.4)
    yearticks(ax)
    ax.set_ylabel("share of public-school teachers, 12-month rate (%)")
    title(ax, "The exodus ended in 2021; the classroom leak did not")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig2_attrition.pdf")
    plt.close(fig)


# ------------------------------------------- fig 3: attrition by age band
def fig3():
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    colors = {"under 35": CORAL, "35-49": GREEN, "50+": BLUE}
    for band, g in age.groupby("band"):
        g = g.sort_values("base_year")
        ma = g.sector_leaver.rolling(3, center=True, min_periods=2).mean()
        ax.plot(g.base_year, ma, color=colors[band], lw=2.2)
        endlab(ax, g.base_year.iloc[-1], ma.iloc[-1], band, colors[band])
    ax.axvspan(2019, 2021, color=GRAY, alpha=0.08, lw=0)
    ax.text(2020, 4.6, "COVID\nyears", ha="center", fontsize=8.2, color=GRAY)
    ax.set_xlim(2005, 2026.6)
    yearticks(ax)
    ax.set_ylabel("left education within 12 months (%),\n3-yr moving avg")
    title(ax, "Every age group is back near its own normal")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig3_age.pdf")
    plt.close(fig)


# ---------------------------------------------------- fig 4: real weekly pay
def fig4():
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    p = pay.sort_values("year")
    ax.axhline(100, color=GRAY, lw=0.6, ls=":")
    ax.fill_between(p.year, p.teacher_idx, p.ba_idx, color=CORAL,
                    alpha=0.10, lw=0)
    ax.plot(p.year, p.all_idx, color=GOLD, lw=1.4, alpha=0.8)
    ax.plot(p.year, p.ba_idx, color=SUBTLE, lw=2.2)
    ax.plot(p.year, p.teacher_idx, color=BLUE, lw=2.7)
    endlab(ax, p.year.iloc[-1], p.teacher_idx.iloc[-1],
           f"teachers\n{p.teacher_idx.iloc[-1]:.0f}", BLUE, dy=-2)
    endlab(ax, p.year.iloc[-1], p.ba_idx.iloc[-1],
           f"graduates (BA+)\n{p.ba_idx.iloc[-1]:.0f}", SUBTLE, dy=4)
    endlab(ax, p.year.iloc[-1], p.all_idx.iloc[-1],
           f"all workers\n{p.all_idx.iloc[-1]:.0f}", GOLD, dy=14)
    ax.annotate("a teacher earned 87¢ per\ngraduate dollar in 2010;\n"
                "79¢ in 2025", (2009.4, 108.6), fontsize=9, color=CORAL,
                fontweight="bold", ha="center", va="top")
    ax.set_xlim(2005, 2028.8)
    yearticks(ax)
    ax.set_ylabel("real median weekly earnings, 2010 = 100")
    title(ax, "Teacher pay has fallen behind other graduates")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig4_pay.pdf")
    plt.close(fig)


# --------------------------------- fig 5: unemployment vs leaving teaching
def fig5():
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    m = mkt.dropna(subset=["sector_leaver"]).sort_values("year")
    ax.plot(m.year, m.sector_leaver, color=BLUE, lw=2.8, zorder=3)
    ax.set_ylabel("teachers leaving education (%)", color=BLUE)
    ax.tick_params(axis="y", labelcolor=BLUE)
    ax.set_ylim(6.3, 10.9)
    axr = ax.twinx()
    axr.plot(m.year, m.unrate, color=CORAL, lw=2.2, ls="--", zorder=2)
    axr.set_ylabel("unemployment rate (%), inverted scale", color=CORAL)
    axr.tick_params(axis="y", labelcolor=CORAL)
    axr.set_ylim(12.4, 2.2)          # inverted: good times point up
    axr.spines["right"].set_visible(True)

    def note(x, y, txt, dx, dy, color=SUBTLE):
        ax.annotate(txt, xy=(x, y), xytext=(dx, dy),
                    textcoords="offset points", fontsize=8.8, color=color,
                    fontweight="bold", ha="center",
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))
    note(2009.5, 7.38, "worst market in decades:\nteachers stay put",
         30, -46)
    note(2019, 10.43, "tightest market in 50 years:\nrecord exit", -70, 4)
    note(2023.6, 7.75, "the market cools,\nexits settle", -14, -46)
    endlab(ax, 2024, m.sector_leaver.iloc[-1], "teachers\nleaving", BLUE,
           dy=6)
    axr.text(2006.1, 3.35, "unemployment (inverted)", fontsize=9.5,
             color=CORAL, fontweight="bold")
    ax.set_xlim(2005, 2027.4)
    yearticks(ax, 2005, 2024)
    title(ax, "Teachers leave when jobs are plentiful, and stay when they "
              "are not")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig5_unemployment.pdf")
    plt.close(fig)


# ----------------------------------------------- fig 6: the quits scatter
def fig6():
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    m = mkt.dropna(subset=["sector_leaver"]).sort_values("year")
    r = np.corrcoef(m.sector_leaver, m.quits_private)[0, 1]
    b, a = np.polyfit(m.quits_private, m.sector_leaver, 1)
    xs = np.linspace(m.quits_private.min() - .07,
                     m.quits_private.max() + .07, 50)
    ax.plot(xs, a + b * xs, color=GRAY, lw=1.4)
    ax.scatter(m.quits_private, m.sector_leaver, s=30, color=BLUE, zorder=3)
    hl = m[m.year == 2024]
    ax.scatter(hl.quits_private, hl.sector_leaver, s=64, color=CORAL,
               zorder=4)
    for y in (2009, 2019, 2022, 2024):
        row = m[m.year == y]
        ax.annotate(str(y), (row.quits_private.iloc[0],
                             row.sector_leaver.iloc[0]),
                    xytext=(6, 4), textcoords="offset points", fontsize=8.5,
                    color=CORAL if y == 2024 else SUBTLE,
                    fontweight="bold" if y == 2024 else "normal")
    ax.annotate(f"slope: +{b:.2f} pp of teacher exit\nper pp of quits"
                f"  (r = {r:+.2f})",
                (0.03, 0.94), xycoords="axes fraction", va="top",
                fontsize=9, color=SUBTLE)
    ax.set_xlabel("private-sector quits rate (%)")
    ax.set_ylabel("teachers leaving education (%)")
    title(ax, "Roughly half a point of exit per point of quits")
    fig.tight_layout()
    fig.savefig(f"{FIG}/br_fig6_quits.pdf")
    plt.close(fig)


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print("figures saved to", FIG)
