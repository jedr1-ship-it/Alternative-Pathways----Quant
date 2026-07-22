# Replication package

## 1. Build the database

    python3 replication/build_database.py

Downloads the official Census ASEC technical documentation and public-use files, extracts the 1998-2010 fixed-width supplements at the officially documented byte positions, and pools them with the 2011-2025 machine-readable files into `data/processed/asec_master.parquet` (5,009,129 person-year records, surveys 1998-2025, calendar years 1997-2024). Requires the tier-A raw caches produced by `src/46_fetch_asec_rich.py` (machine-readable files) and internet access for the fixed-width downloads.

Intermediate series consumed by the figures (`outputs/*.csv`) are produced by `src/61_children_and_workforce.py`, `src/62_series_from_master.py`, `src/67_state_cyclicality.py`, `src/68_pfl_baby_test.py`, and `src/69_probit_appendix.py`, and ship with the repository.

## 2. Make the figures

    python3 replication/make_figures.py

Rebuilds the 13 main figures and 5 appendix figures of the paper into `report/figures/`, each block headed by the figure title as it appears in the paper.
