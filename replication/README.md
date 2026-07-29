# Replication package

Three steps, run in order from the repository root. Step 1 builds the pooled
database, step 2 extracts the teacher files, step 3 rebuilds every figure of
the presentation (`Proyect_US.pptx`).

## 1. Build the database

    python3 replication/build_database.py

Downloads the official Census ASEC technical documentation and public-use
files, extracts the 1998-2010 fixed-width supplements at the officially
documented byte positions, and pools them with the 2011-2025 machine-readable
files into `data/processed/asec_master.parquet` — **5,009,129 person-year
records**, survey years 1998-2025, teaching (calendar) years 1997-2024.
Requires the tier-A raw caches (machine-readable files) and internet access
for the fixed-width downloads.

Intermediate series consumed by the figures (`outputs/*.csv`) ship
precomputed with the repository; the series builders are preserved in the
repository history.

## 2. Build the teacher files

    python3 replication/build_teacher_sample.py

Reads the master file and writes:

| File | Contents |
|---|---|
| `data/processed/teachers.parquet` | every teacher-year observation (longest job last year was K-12 teaching) |
| `data/processed/teachers_main.parquet` | the main analysis sample: college graduates aged 18+, valid weight and outcome (85,497 observations, 6,931 observed exits) |

## 3. Rebuild the presentation figures

    python3 replication/make_deck_figures.py

Runs the 21 scripts in `replication/deck_figures/` in slide order and writes
every figure of the deck to `report/figures_deck/`. Each script is
self-contained and can be run on its own. The mapping, in deck order:

| Deck slide | Script | Output file |
|---|---|---|
| Figure 1. Composition of the Teaching Workforce | `fig01_composition.py` | `g1_workforce` |
| Figure 2. Leaving Teaching, 1997-2024 | `fig02_leaving_series.py` | `g2_evolution` |
| Figure 3. Leaving Teaching by School Sector | `fig03_sector.py` | `pubpriv_series` |
| Figure 4. Rates of Leaving the Occupation, by Profession | `fig04_05_professions.py` | `leave_professions_deck` |
| Figure 5. Labor Force Exit of Women, by Profession | `fig04_05_professions.py` | `lf_professions_deck` |
| Figure 6. Teachers Leaving per Year Across Countries | `fig06_countries.py` | `intl_bars_deck` |
| Figure 7. Destinations of Leavers, 2024 | `fig07_destinations_2024.py` | `g3_flow100_2024` |
| Figure 8. The Routes out of Teaching, 2002-2024 | `fig08_routes_periods.py` | `routes_bars3` |
| Figure 9. Who Leaves the Labor Force Before 55, 2024 | `fig09_cascade_u55_2024.py` | `yellow_flow2024` |
| Figure 10. Where the Employed Leavers Go: Every Occupation | `fig10_all_occupations.py` | `occ_all_slide` |
| Figure 11. Leaving Teaching by Age and Route | `fig11_age_routes.py` | `g4_routes_age` |
| The Model (equation slide) | `pdflatex replication/eq_slide.tex` | — |
| Figure 12. Average Marginal Effects | `fig12_ame.py` | `g6_ame_v2` |
| Figure 13. The Age Profile of Leaving Teaching | `fig13_age_route_profiles.py` | `u_routes_deck` |
| Figure 14. The Effect of a New Baby, by Profession | `fig14_new_baby.py` | `g8_newbaby` |
| Figure 15. Leaving and the Unemployment Rate | `fig15_unemployment.py` | `n5_cyclicality` |
| Figure 16. State-Level Cyclicality | `fig16_state_cyclicality.py` | `states_landscape` |
| Figure 17. Real Earnings Growth since 1997 | `fig17_pay_index.py` | `msgA3` |
| Figure 18. Leaving Rate by Pay Decile | `fig18_pay_deciles.py` | `pay3_deciles_deck` |
| Figure 19. Pay Compression | `fig19_pay_compression.py` | `pay5_compression_deck` |
| Figure 20. The Earnings Change of Leaving, by Destination | `fig20_earnings_by_destination.py` | `pay7_destinations_deck` |
| Figure 21. The Distribution of Earnings Changes | `fig21_earnings_density.py` | `g5b_earnings_density` |
| Figure 22. Pension Coverage and Leaving Across States | `fig22_pension_states.py` | `pension_scatter_deck` |

Data requirements per script: most read `data/processed/asec_master.parquet`
and/or precomputed `outputs/*.csv` only. `fig13` (probit age profiles by
route) and `fig20` (person-level earnings links) additionally need the rich
supplement files `data/raw/asec/asec_rich_*.parquet` produced by step 1.

## 4. Paper figures (older set)

    python3 replication/make_figures.py

Rebuilds the 13 main and 5 appendix figures of the working paper into
`report/figures/`.
