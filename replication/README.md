# Replication package

## 1. Build the database

    python3 replication/build_database.py

Downloads the official Census ASEC technical documentation and public-use files, extracts the 1998-2010 fixed-width supplements at the officially documented byte positions, and pools them with the 2011-2025 machine-readable files into `data/processed/asec_master.parquet` (5,009,129 person-year records, surveys 1998-2025, calendar years 1997-2024). Requires the tier-A raw caches produced by `the machine-readable ASEC fetch step (see repository history)` (machine-readable files) and internet access for the fixed-width downloads.

Intermediate series consumed by the figures (`outputs/*.csv`) are produced by the series builders preserved in the repository history and ship precomputed with the repository.

## 2. Make the figures

    python3 replication/make_figures.py

Rebuilds the 13 main figures and 5 appendix figures of the paper into `report/figures/`, each block headed by the figure title as it appears in the paper.
