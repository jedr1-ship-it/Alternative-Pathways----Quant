# Proposal for the reviewer comment on teachers' aides (INES/EAG)

Figure: `figures/figure_teacher_aides.png` (script `replication/deck_figures/fig_oecd_teacher_aides.py`, data `figures/figure_aides_data.csv` and `figures/figure_aides_primary.csv`).

## Proposed text after the paragraph on learning support staff

International data on teachers' aides are collected through the joint UNESCO-UIS, OECD and Eurostat (UOE) data collection on educational personnel, although they cover fewer countries than the data on teachers. Among the 20 countries with data for 2024, teachers' aides make up 47% of contact staff in primary education in the United Kingdom, at least a fifth in six other countries and less than 5% in Bulgaria, Canada, Colombia, Denmark, Peru and Romania (Figure X). Their weight has grown in most countries with comparable data. Between 2014 and 2024, the share of teachers' aides in primary education rose from 3% to 20% in Lithuania, from 5% to 14% in Czechia, from 6% to 31% in the Slovak Republic and from 8% to 21% in Sweden, and in the Netherlands it rose from 14% in 2015 to 24% in 2024.

**Figure X. Teachers' aides as a share of contact staff in primary education (2014 and 2024)**

*Note:* Contact staff comprise classroom teachers and teachers' aides in public and private institutions, measured in full-time equivalents. Teachers' aides include personnel or students who support teachers in providing instruction to students. Data for 2014 are not available for Canada, Colombia, Hungary, Ireland and Peru. Denmark reports 10 teachers' aides in full-time equivalents in primary education in 2024. Countries are ranked in descending order of the share of teachers' aides in 2024.
1. Year of reference 2015 instead of 2014.
*Source:* OECD (2026), *Education at a Glance Database*, https://data-explorer.oecd.org/ (accessed on 4 November 2026).

## Figures behind the text (primary education, FTE)

| Country | Share 2014 (%) | Share 2024 (%) | Aides 2014 | Aides 2024 |
|---|---|---|---|---|
| Czechia | 5.1 | 14.2 | 1 473 | 5 386 |
| Lithuania | 3.1 | 19.7 | 340 | 2 165 |
| Netherlands | 14.1 (2015) | 24.4 | 12 368 (2015) | 23 147 |
| Slovak Republic | 5.9 | 30.8 | 778 | 7 576 |
| Sweden | 8.1 | 20.7 | 4 916 | 16 764 |
| United Kingdom | 43.6 | 46.8 | 177 541 | 214 376 |

## Method and checks

- Share = FTE teachers' aides / (FTE teachers' aides + FTE classroom teachers), all educational institutions, formal education. Dataflows OECD.EDU.IMEP `DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_RAW_INST2` (Number of teacher aides) and `@DF_UOE_NF_PERS_RAW_INST` (classroom teachers).
- The same calculation for pre-primary education in 2023 reproduces EAG 2025 Table D2.1, column 7, for all 17 countries with data (asserted in the script).
- EAG 2025 publishes teachers' aides only for early childhood education (Table D2.1 and Figure D2.1). The school-level series exist only in the database, so the source line cites the database.
- No OECD average is shown because only 16 OECD countries have data for 2024.
- Malta is not covered by the teachers' aides dataflow.
