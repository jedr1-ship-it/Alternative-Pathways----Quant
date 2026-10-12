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

## Block structure after Block 0
- Block 1: Leaving rate - how many leave
- Block 2: Composition - where they go
- Block 3: Correlations - why they leave

## Block 1 - Leaving rate: how many leave  (THREE things only)
1. Slide: US leaving-rate evolution alone (g2_evolution).
   SPEAKER NOTES (not on slide): stable and similar to other OECD
   countries; EAG averages for countries with data: 6.6 (2016 data,
   EAG 2021) -> 6.5 (2022/23, EAG 2025) -> 6.4 (2024/25, EAG 2026)
   [corrected from dictated "6.9 in 2015"]. Countries with long series
   (New Zealand, Sweden, Israel, Norway) also look stable [verify for
   notes]. The US rate is higher than most other countries.
   APPENDIX (button): private vs public chart (pubpriv_series); private
   is where mobility is highest.
2. NEW slide: why the comparison professions are comparable. Academic
   paper-style table, no subtitles: variables (gender, salary, whatever
   works), means and differences, teachers vs nurses / social workers /
   accountants. Must actually support "they are similar".
3. Slide: existing comparison chart (teachers vs nurses, social workers,
   accountants = leave_professions_deck).
   APPENDIX (button): same chart with ~5 additional professions
   (candidates: lawyers, pharmacists, physical therapists, physicians,
   +1) AND a line for the average of all other professions.
   [Series exist for lawyers; others need computing from the master.]

## Block 2 - Composition: where they go
Problem now: charts are inconsistent. Fix:
- ONE master chart: of every 100 leavers, AVERAGE OF THE LAST 5 YEARS:
  another job (~1/3) / out of LF 55+ (trivial, do not open) /
  out of LF under 55 / unemployed. Every later opening must branch from
  THESE SAME NUMBERS.
- Opening 1 (the employed): destination professions list (keep, with the
  red-circle nuance below).
- Opening 2 (OLF under 55): mothers / non-mothers / men, AND ALSO fathers
  (paternity, not just maternity), AND whether they are STUDYING
  (leaving to study is not leaving to not work).
- On the master chart: short text with the general message and the policy
  margin: how many of the leavers are plausibly retrievable (mothers
  probably not - do not write that explicitly). If policy text sits ugly
  on charts, give the messages their own slide.
- APPENDIX: comparison of our openings/proportions with the NCES Teacher
  Follow-up Survey destinations - how our numbers square with theirs.
- On the all-professions destinations slide: RED CIRCLES around
  destinations that likely require no prior degree (sales, commercial...)
  - where teachers tend to go.

## Block 3 - Correlations: why they leave
- Equation slide: clean, no title clutter; the equation only; variables
  as vectors (x'beta), NOT described in text; explained verbally
  component by component. Nothing else on the slide.
- Main specification: LINEAR PROBABILITY MODEL (was probit).
  - Check fitted probabilities bounded in [0,1]; show the check chart in
    appendix. If not bounded, keep probit as main.
  - More sociodemographic variables: health/disability, years of
    education, high/low household income dummy, and similar.
  - Redo the coefficient plot with LPM coefficients.
- APPENDIX tables: (a) LPM without time FE, plus a column with state FE;
  (b) main LPM vs logit vs probit (AMEs).
- Pay sequence in the main deck: teachers vs rest pay evolution; exits
  concentrated in the lowest deciles; then pensions with ONLY the state
  scatter. ALL other pay/pension charts to the appendix.
- Cyclicality: ONE clear chart only, overall (not by state) - e.g. the
  unemployment series vs the leaving rate; drop the two-panel version
  (slopes unreadable; the grey slope does not matter).
- The what-the-CPS-sees framework table moves to the APPENDIX; the
  conclusions still acknowledge unobserved motives.
- Close: conclusions - what we learn and what it says for policy:
  flexibility matters, economic security matters, pension coverage
  matters, it is precisely [the low-attached/low-paid] teachers who
  leave; we only observe some motives (financial, life-cycle,
  demographics; others unobserved); given what we learn, what could
  bring teachers back.

## Window notes
- Flow master chart: last 5 calendar years available (2020-2024).
- Extended LPM runs on ASEC CSV years 2019-2025 (cal 2018-2024), the
  years with state, health, disability, household income and enrollment
  available in the public CSVs.

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
