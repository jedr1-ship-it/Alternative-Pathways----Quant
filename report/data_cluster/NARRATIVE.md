# Data Cluster presentation - narrative spec (as dictated, 2026-10-12)

Style: as close to LaTeX as possible in BOTH formats. Same typeface and
sizes (Latin Modern / CMU in the PPTX, fonts shipped with the bundle).
Appendices answer likely audience questions; main deck stays lean.
Beamer buttons (Dispersion, Tables, Logit/Probit, ...) link to appendices;
clickable equivalents in the PPTX.

## Block 0 - Methodological discussion

1. Opening slide
   - Motivation: why teachers leave; is there a real policy margin to
     close/soften teacher shortages by retaining teachers?
   - Problem: no publicly available official microdata for many countries.
     Start with the US: most information available.
2. Solution: use the CPS to
   (a) reproduce and extend the official statistics on teacher leaving;
   (b) having achieved (a), study where they go, how many and why.
3. What the CPS is: one sentence (what, who runs it), years used, total
   persons interviewed in the final base, how many are teachers, national
   representativity. Nothing else. (Drop the mean-difference table.)
4. What the March Supplement is: how many interviewed, months covered,
   who does it, why. Done.
5. How to identify a teacher: academic version of the census-codes slide
   (no colors/rounded boxes): codes used, changes over time, and evidence
   that the teaching group is constant/traceable across classifications.
6. Rotation diagram alone (the one we have).
7. Two ways to identify a leaver, super simple:
   A) follow individuals who do not change dwelling, all months
      (list the linking IDs);
   B) retrospective info from the March Supplement.
8. Disadvantages of each.
   A: validation not 100% (noisy people possible); lose movers (give the
      number); normal household attrition (give the number); strong
      seasonality; multiple ways to define the rate (next slide).
   B: recall bias; less sample than using all months (quantify); plus any
      other (candidates: only March-to-March transitions; within-year
      spells smoothed away).
9. Six definitions of leaving using all months, simplest to strictest,
   UNIT = INDIVIDUAL (not month):
   - single: seen teaching once in the 4 year-1 interviews; leaver if
     never seen teaching in year 2
   - pair: seen >= 2 times, then never
   - triple: seen >= 3 times, then never
   - strict: seen all 4 times, then never
   - month pairs: month-by-month rate, weighted average across months
   - annual recall: March Supplement retrospective
   Computed (pooled, outputs/definitions_ladder.csv):
   single 17.5, month pairs 15.4, pair 13.4, triple 11.7, strict 10.5,
   annual recall 8.6.

## Block 1 - Leaving rate: how many leave
(user to continue narration here)

## Appendix questions captured so far
- How is unemployment computed from the CPS? Only the March supplement or
  how? If monthly: what is the rest of the survey used for, for which
  statistics?
- US internal migration rate (people changing dwelling), official source,
  one brief slide.
- Is there internal validation that persons are the same year to year?
  (roster, line numbers, dependent interviewing; public files lack a
  person ID -> Madrian-Lefgren validation.)
- Are interviews monthly, new people + re-interviews each month, or
  4-month blocks? (Verified: every month ~1/8 per MIS position; table of
  eighths; March 2023 tabulation.)
- Household/observation loss: how many lost overall; is the loss
  correlated with being a teacher? (Verified: ~25.5% of MIS1-4 addresses
  not found 12 months later; teachers link MORE than others, 80% vs 76%.)
- Normal household attrition numbers (non-response year 2).
- Occupation-coding traceability evidence (classification changes 2003,
  2020; one-to-one mapping of the K-12 block).

## Verified external anchors (for context slides)
- NCES TFS waves: 5.6 / 5.1 / 6.6 / 7.4 / 8.4 / 8.0 / 7.7 / 8.0
  (1988-89 ... 2021-22).
- NTPS 2020-21 public teachers: female 76.8%, MA+ 61.0%, age 42.9,
  n=39,633 (NCES 2022-113, Digest 209.10, NCES 2024-024).
- EAG attrition indicator: 2021 (D7, 2016 data, ~15 systems, avg ~6.6);
  2025 (D8, 2022/23, 19 systems, avg 6.5; US only historical 2012/13
  figure, 7.7); 2026 (24 systems, avg 6.4 in 2024/25; US = m).
