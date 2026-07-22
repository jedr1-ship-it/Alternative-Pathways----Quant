# Who Leaves Teaching, and Why?

The anatomy of teacher attrition in the United States, 1997-2024, from a
single instrument: the March CPS/ASEC retrospective question comparing
the longest job held last calendar year with the occupation held in the
survey week. A teacher is a respondent whose longest job last year was
K-12 teaching; a leaver is one no longer teaching by the March
interview, routed to another job, unemployment, or out of the labor
force.

## Headline results (paper: report/who_leaves_teaching.pdf)

- Leaving teaching averages 8.6 percent per year over 1997-2024, with
  no trend: peaks of 10.3 (2001) and 10.2 (2019), 7.7 in 2024.
- Of every 100 leavers, 62 are not working the following March, 38 of
  them at retirement ages; only 26 hold another job.
- The dominant predictors are contractual (full-year work, hours,
  pension coverage); the one personal event that matters is a birth.
- Exits are weakly counter-cyclical; leaving pays as a gamble (median
  +15 log points, fat tails, 47 percent with zero earnings next year).
- Teacher pay slid from 77 to 72 percent of the median college
  graduate; attrition nonetheless edged down while most comparison
  professions rose.

## Repository structure

- `replication/` - the pipeline: `build_database.py` (official-layout
  extraction and pooled master, 5,009,129 person-year records) and
  `make_figures.py` (all 18 paper figures), plus `paperstyle.py`.
- `outputs/` - every series, table and research note behind the paper,
  including the cross-country CPF synthesis and the data-access audit.
- `report/` - the paper, the figures-and-appendix companion, the slide
  deck, and the CPF research proposal, with figures and tables.
- `data/raw/docs/` - the official Census ASEC technical documentation
  (cpsmarYY) used to extract the 1998-2010 fixed-width files.

Heavy inputs (raw ASEC files, the master parquet) are gitignored and
fully regenerable with `replication/build_database.py`. Full
development history, including the intermediate series builders, lives
in the git log.
