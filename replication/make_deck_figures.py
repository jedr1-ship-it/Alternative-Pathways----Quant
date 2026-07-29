"""Step 3 - Rebuild every figure of the presentation (Proyect_US.pptx).

Runs the scripts in replication/deck_figures/ in slide order and writes all
figures to report/figures_deck/. Each script is self-contained and can also
be run on its own from the repository root:

    python3 replication/deck_figures/fig07_destinations_2024.py

Inputs: data/processed/asec_master.parquet   (step 1)
        data/raw/asec/asec_rich_*.parquet    (step 1; needed by fig13, fig20)
        outputs/*.csv                        (precomputed series, shipped)

The only slide not produced here is "The Model", which is a LaTeX equation:
compile replication/eq_slide.tex with pdflatex (standalone class).
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent / "deck_figures"
Path("report/figures_deck").mkdir(parents=True, exist_ok=True)

FIGS = [
    ("fig01_composition.py", "Figure 1. Composition of the Teaching Workforce, 2005-2024"),
    ("fig02_leaving_series.py", "Figure 2. Leaving Teaching, 1997-2024"),
    ("fig03_sector.py", "Figure 3. Leaving Teaching by School Sector, 1997-2024"),
    ("fig04_05_professions.py", "Figures 4-5. Leaving the Occupation / Labor Force Exit of Women, by Profession"),
    ("fig06_countries.py", "Figure 6. Teachers Leaving per Year Across Countries"),
    ("fig07_destinations_2024.py", "Figure 7. Destinations of Teachers Who Leave the Profession, 2024"),
    ("fig08_routes_periods.py", "Figure 8. The Routes out of Teaching, 2002-2024"),
    ("fig09_cascade_u55_2024.py", "Figure 9. Who Leaves the Labor Force Before 55, 2024"),
    ("fig10_all_occupations.py", "Figure 10. Where the Employed Leavers Go: Every Occupation, 2019-2024"),
    ("fig11_age_routes.py", "Figure 11. Leaving Teaching by Age and Route"),
    ("fig12_ame.py", "Figure 12. Average Marginal Effects on the Probability of Leaving Teaching"),
    ("fig13_age_route_profiles.py", "Figure 13. The Age Profile of Leaving Teaching (three panels)"),
    ("fig14_new_baby.py", "Figure 14. The Effect of a New Baby on Leaving, by Profession"),
    ("fig15_unemployment.py", "Figure 15. Leaving Teaching and the Unemployment Rate, 1997-2024"),
    ("fig16_state_cyclicality.py", "Figure 16. State-Level Cyclicality of Leaving Across the States"),
    ("fig17_pay_index.py", "Figure 17. Real Earnings Growth by Profession since 1997"),
    ("fig18_pay_deciles.py", "Figure 18. Leaving Rate by Position in the Teacher Pay Distribution"),
    ("fig19_pay_compression.py", "Figure 19. Pay Compression: Teachers and Comparable Professions"),
    ("fig20_earnings_by_destination.py", "Figure 20. The Earnings Change of Leaving, by Destination"),
    ("fig21_earnings_density.py", "Figure 21. The Distribution of Earnings Changes: Stayers and Leavers"),
    ("fig22_pension_states.py", "Figure 22. Pension Coverage and Leaving Teaching Across States"),
]

failed = []
for script, title in FIGS:
    t0 = time.time()
    print(f"\n=== {title}\n    [{script}]")
    r = subprocess.run([sys.executable, str(HERE / script)])
    print(f"    {'OK' if r.returncode == 0 else 'FAILED'} ({time.time()-t0:.0f}s)")
    if r.returncode != 0:
        failed.append(script)

print("\n" + "=" * 60)
if failed:
    print("FAILED:", ", ".join(failed))
    sys.exit(1)
print("All deck figures written to report/figures_deck/")
print('Remaining slide: "The Model" -> pdflatex replication/eq_slide.tex')
