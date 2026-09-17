// Data for the deck. Ordered by country, then category.
// cat: one of the five instrument categories; groups: subset of Switchers/Leavers/Retired
module.exports = [
  {
    country: "Australia", region: "Victoria", flag: "au",
    cat: "Support & training", groups: ["Switchers", "Leavers", "Retired"],
    title: "Teacher Re-Engagement Initiative (TREI), 2022–2025",
    desc: "Victorian Department of Education scheme for qualified teachers who have been out of a fixed-term or ongoing teaching role for 12+ months, including retirees and people on career breaks. A re-engagement team contacts each registrant, then offers a funded placement of up to 40 days in a government school (classroom observation, teaching activities, mentoring by current staff) plus free professional development and one-to-one employability coaching. Returners from retirement or career breaks receive an honorarium of up to AUD 12,000 for a 40-day placement.",
    chips: ["Launched late 2022; 1,100+ expressions of interest", "AUD 12m in the 2023/24 State Budget; placements to 30 Jun 2025", "Also: Financial incentives · Information & nudges"],
    sources: ["https://www.vic.gov.au/teacher-re-engagement-initiative"],
    notes: "Secondary instruments: financial (honorarium up to AUD 12,000) and information/nudges (re-engagement team contacts every registrant). Eligibility: VIT registration or Working with Children Check. Teachers returning from extended parental absence instead get a temporary resumption of up to 40 days on their substantive salary. Extra reference: Victorian Government 'Support for returning teachers' page, https://www.vic.gov.au/returning-teacher-support-services"
  },
  {
    country: "Canada", region: "Quebec", flag: "ca",
    cat: "Financial incentives", groups: ["Retired"],
    title: "Incentive pay for returning retired teachers (2020, made permanent) and ministerial letter campaign (2023)",
    desc: "Retired teachers with a teaching authorisation who return to Quebec public schools are paid on the salary scale they had at retirement from their first day of substitute teaching (up to about CAD 412 a day instead of the usual CAD 212 rate), with no penalty on their pension. Introduced on 21 September 2020 during the pandemic, it drew 700 retirees back in 2020–21 and was made permanent. In August 2023 the Minister of Education wrote to all retired teachers inviting them back: over 5,000 had worked in schools the previous year, mostly as substitutes or part-time, and the top daily incentive rose to CAD 578.",
    chips: ["Since 21 Sep 2020 (permanent); letter campaign Aug 2023", "700 returners in 2020–21; 5,000+ retirees in 2022–23", "Also: Information & nudges · Flexible positions"],
    sources: ["https://www.quebec.ca/en/government/work-government/jobs-education/teaching-general-education-youth-sector-vocational-training-adult-education/return-work-retired-teacher", "https://www.ledevoir.com/actualites/education/912921/quebec-espere-nouveau-attirer-milliers-enseignants-retraites-ecoles"],
    notes: "Primary source: Gouvernement du Québec page 'Retour à l'emploi des retraités du réseau de l'éducation' (incentive introduced 21 September 2020, made permanent; 700 retirees in 2020-21; pay at the scale held at departure from day one; daily maximum about CAD 412 vs CAD 212.15 usual substitute rate; no penalty on pension). The 2023 letter (signed 25 August 2023 by Minister Bernard Drainville), the 5,000+ figure and the CAD 578 daily incentive for retirees at the top of the scale on contracts of at least one month are reported by Le Devoir (press source)."
  },
  {
    country: "China", region: "", flag: "cn",
    cat: "Flexible positions", groups: ["Retired"],
    title: "Silver-Age Lecturing Plan (银龄讲学计划), 2018–",
    desc: "Joint Ministry of Education and Ministry of Finance programme recruiting retired principals, teaching-research staff and senior or ‘special-grade’ teachers, generally aged 65 or under, to serve at least one school year in rural compulsory-education schools in poor and remote counties, where they teach, coach young teachers and advise on school management. Retirees keep their pension and receive a central-government allowance of CNY 20,000 a year (compulsory-education level) covering a stipend, travel and accident insurance. The 2018 plan targeted 10,000 recruits for 2018–2020; the 2024 round recruited 7,000.",
    chips: ["Since 2018; expanded by the 2023 National Silver-Age Teachers Action Plan", "Target 10,000 recruits (2018–20); 7,000 recruited in 2024", "Also: Financial incentives"],
    sources: ["http://www.moe.gov.cn/srcsite/A10/s7151/201807/t20180719_343448.html", "https://www.gov.cn/zhengce/zhengceku/202408/content_6967278.htm"],
    notes: "Primary sources: MoE/MoF notice of 19 July 2018 issuing the implementation plan (eligibility: mainly principals, teaching researchers, special-grade and backbone teachers, generally 65 or under; 10,000 recruits planned 2018-2020; first cohort autumn 2018), and the 2024 implementation notice (7,000 recruits; central funding of CNY 20,000 per person per year at compulsory-education level, used for work stipend, travel and accident insurance). The 2023 National Silver-Age Teachers Action Plan (10 ministries) sets a target of roughly 120,000 silver-age teachers across all education levels within about three years."
  },
  {
    country: "Germany", region: "Lower Saxony", flag: "de",
    cat: "Financial incentives", groups: ["Retired"],
    title: "Raising and then abolishing the earnings ceiling for retired teachers (Hinzuverdienstgrenze), 2022–2024",
    desc: "Under Lower Saxony's civil-service pension rules, retired teachers who teach again lose pension once pay plus pension exceed an earnings ceiling. The 2022 ‘Lehrkräfte-Gewinnungspaket’ raised that ceiling from 125% to 150% of pensionable pay from 1 October 2022 (it had already risen from 100% to 125% in 2019), so pensioners can teach about 9–10 hours a week with no deductions, and overtime pay for teachers rose 15%. On 31 October 2024 the ceiling for pensioned teachers was abolished altogether, as a further incentive to keep working in schools after retirement.",
    chips: ["Ceiling 125% → 150% (1 Oct 2022); abolished 31 Oct 2024", "≈9–10 teaching hours/week without pension cuts (2022 rule)", "Also: Information & nudges (letters to teachers nearing retirement)"],
    sources: ["https://www.mk.niedersachsen.de/startseite/aktuelles/presseinformationen/lehrkrafte-gewinnungspaket-landtag-erhoht-hinzuverdienstgrenze-und-mehrarbeitsvergutung-tonne-unterrichten-lohnt-sich-215592.html", "https://www.mk.niedersachsen.de/startseite/aktuelles/presseinformationen/2-schulhalbjahr-2024-2025-unterrichtsversorgung-bleibt-stabil-238881.html"],
    notes: "Sources: Lower Saxony Ministry of Education press releases. The 2022 release (Lehrkräfte-Gewinnungspaket) reports the Landtag decision to raise the Hinzuverdienstgrenze from 125% to 150% of pensionable pay from 1 October 2022, initially limited to two years, letting pensioned teachers teach on average 9-10 hours without pension reduction, plus a 15% rise in overtime pay. The 2024/25 release states that the earnings ceiling for pensioned teachers was removed as of 31 October 2024. Context: a 2023 survey by Deutsches Schulportal found that 13 of 16 Länder actively approach retired teachers and that more than 5,000 teachers nationwide had been won to stay or return (https://deutsches-schulportal.de/bildungswesen/laenderueberblick-umfrage-lehrermangel-pensionierte-lehrer/)."
  },
  {
    country: "Germany", region: "Lower Saxony", flag: "de",
    cat: "Information & nudges", groups: ["Retired"],
    title: "Minister's letter to teachers approaching retirement (November 2023)",
    desc: "In November 2023 Lower Saxony's Minister of Education, Julia Willie Hamburg, wrote personally to teachers approaching retirement, thanking them for their service and asking for their continued support in schools facing rising pupil numbers. The letter and its information sheet spell out the options: civil-servant teachers may postpone retirement by up to three years on request, and both civil-servant and salaried teachers can be re-hired on fixed-term contracts immediately after retiring, alongside their pension, under the relaxed earnings rules. A registration guide for retired teachers was enclosed.",
    chips: ["Letter sent November 2023", "Options: defer retirement up to 3 years, or be re-hired after retiring", "Also: Financial incentives (pension plus salary)"],
    sources: ["https://www.mk.niedersachsen.de/startseite/aktuelles/kultusministerin_hamburg_schreibt_an_angehende_pensionare/umfangreicher-erfahrungsschatz-kultusministerin-hamburg-informiert-lehrkrafte-kurz-vor-dem-ruhestand-uber-moglichkeiten-der-weiterbeschaftigung-227231.html", "https://www.mk.niedersachsen.de/download/201317/Schreiben_an_angehende_Pensionaerinnen_und_Pensionaere.pdf"],
    notes: "Source: Ministry press release 'Umfangreicher Erfahrungsschatz – Kultusministerin Hamburg informiert Lehrkräfte kurz vor dem Ruhestand über Möglichkeiten der Weiterbeschäftigung' and the letter itself (PDF). The information sheet ('Anlage zum Brief') covers staying in service (deferral of up to three years for civil servants, on application before the end of the preceding school half-year) and fixed-term re-employment under the collective agreement immediately after retirement. This matches the 'leaflet with the retirement paperwork' type of nudge."
  },
  {
    country: "Ireland", region: "", flag: "ie",
    cat: "Financial incentives", groups: ["Retired"],
    title: "Waiver of pension abatement for retired teachers: 50 days a year (2021–2027)",
    desc: "Public-service ‘abatement’ normally reduces a retired teacher's pension when pension plus new salary exceed their pre-retirement pay. To ease teacher-supply difficulties the Department of Education introduced a waiver in 2021 (Circular 0003/2021): the first 50 days a retired teacher works in a calendar year as a substitute or fixed-term teacher are exempt from abatement, each working day counting as one day whatever the hours. Retirees keep their full pension while covering absences; abatement is assessed only beyond day 50. Renewed for 2024–2025 (Circular 04/2024) and 2026–2027 (Circular 17/2026).",
    chips: ["In force since 2021; renewed through 2027", "First 50 working days per calendar year exempt", "Also: Flexible positions (substitute cover)"],
    sources: ["https://www.gov.ie/en/department-of-education/publications/working-as-a-substitute-while-receiving-a-teachers-pension/"],
    notes: "Source: Department of Education (gov.ie) 'Working as a substitute while receiving a teacher's pension'. Circular numbers (0003/2021, 04/2024, 17/2026) as cited by the Department and by the Retired Teachers' Association of Ireland (https://rtaireland.ie/pension-abatement/). Abatement applies only where earnings plus pension exceed pensionable pay at retirement (uprated); it stops as soon as the retiree stops working."
  },
  {
    country: "Japan", region: "", flag: "jp",
    cat: "Flexible re-certification", groups: ["Switchers", "Leavers"],
    title: "Abolition of the teacher licence renewal system (1 July 2022)",
    desc: "From 2009 Japanese teaching licences expired every ten years unless holders completed a 30-hour renewal course, so the licences of people who had left teaching lapsed into ‘paper’ credentials. A May 2022 amendment to the Educational Personnel Certification Act abolished the renewal system from 1 July 2022: every licence valid on that date, including dormant ones held by former teachers, became permanently valid with no procedure or fee, removing a major barrier to re-entry. Boards of education now add ‘paper-teacher’ seminars and consultation days for licence holders who left or never entered teaching (e.g. Saitama, Chiba, Nagoya).",
    chips: ["Renewal system abolished 1 July 2022 (Act amended 11 May 2022)", "Paper-teacher programmes: 50 boards in FY2023, 58 planned FY2024", "Also: Information & nudges (seminars, consultation days)"],
    sources: ["https://www.mext.go.jp/content/20221028-mxt_kyoikujinzai02-000022570_3.pdf", "https://www.pref.saitama.lg.jp/f2213/paperteacher.html"],
    notes: "Sources: MEXT explanatory document on the abolition of the licence renewal system (licences valid on 1 July 2022, including dormant ones, become licences without expiry, no procedure needed) and Saitama Prefectural Board of Education 'paper teacher seminar' page. The counts of boards of education running paper-teacher programmes (50 in FY2023, 58 planned in FY2024, about 70%) are MEXT figures reported by AERA (press source); treat as indicative. MEXT archive on the former renewal system: https://www.mext.go.jp/a_menu/shotou/koushin/"
  },
  {
    country: "Netherlands", region: "", flag: "nl",
    cat: "Financial incentives", groups: ["Switchers", "Leavers"],
    title: "Regeling tegemoetkoming herintreders primair onderwijs (2017–2020)",
    desc: "Ministry of Education (OCW) scheme paying primary-school boards up to EUR 2,500 for each ‘herintreder’ (returner) they hired: a qualified teacher who had not worked as a primary teacher for at least 12 consecutive months, appointed on or after 1 August 2017 for at least six months. The grant was earmarked for the guidance and support returners need in their first months (coaching, refresher training), making re-entry attractive for teacher and school alike. The initial budget of EUR 1.25 million covered up to 500 returners by end-2018; the regulation ran from 1 November 2017 to 1 January 2020, with a further round in 2019.",
    chips: ["1 Nov 2017 – 1 Jan 2020 (closed)", "EUR 2,500 per returner; first budget for 500 returners", "Also: Support & training"],
    sources: ["https://wetten.overheid.nl/1.3:c:BWBR0040130&g=2020-07-01&z=2025-10-18", "https://www.nieuwsbrievenminocw.nl/actueel/nieuws/2019/07/03/subsidie-voor-herintreders"],
    notes: "Primary source: text of the 'Regeling tegemoetkoming herintreders primair onderwijs' on wetten.overheid.nl (BWBR0040130), plus the OCW newsletter of 3 July 2019 announcing a new application round. Conditions: appointment from 1 August 2017, contract of at least six months, no work as a primary-school teacher in the 12 months before appointment; grant of up to EUR 2,500 per returner paid to the school board for guidance and support costs; EUR 1.25 million available until 31 December 2018 (max. 500 returners)."
  },
  {
    country: "New Zealand", region: "", flag: "nz",
    cat: "Flexible re-certification", groups: ["Switchers", "Leavers"],
    title: "Streamlined return-to-teaching pathway: no refresher course, fees covered (2024–2028)",
    desc: "Registered teachers who had not taught for five years or more used to need a Teacher Education Refresh (TER) programme before regaining a practising certificate. Now a returning teacher with a job offer can renew the certificate without TER, may relief-teach for up to 20 half-days while the renewal is processed, and may instead be asked to agree a ‘Kia Maia | Future-Ready Teaching Plan’ with the principal. The Government also pays practising-certificate and Limited Authority to Teach fees: 352 teachers were supported back into classrooms between October 2024 and April 2025, and Budget 2025 funds all registration fees and levies until 30 June 2028.",
    chips: ["Fees covered from Oct 2024; NZD 53.3m for 2025–2028", "352 teachers returned Oct 2024 – Apr 2025", "Also: Financial incentives"],
    sources: ["https://workforce.education.govt.nz/current-teachers/returning-teaching/returning-teaching-after-break", "https://www.beehive.govt.nz/release/backing-teachers-teacher-registrations-funded"],
    notes: "Sources: Ministry of Education 'Education Workforce' page 'Returning to teaching after a break' (no TER required even after five or more years away when there is a job offer; 20 half-days of relief teaching allowed while renewing; fees and levies covered until 30 June 2028) and the Government press release 'Backing teachers: Teacher registrations funded' (352 teachers supported to return since October 2024; NZD 53.3 million over three financial years from 1 July 2025)."
  },
  {
    country: "Portugal", region: "", flag: "pt",
    cat: "Financial incentives", groups: ["Retired"],
    title: "Decreto-Lei n.º 51/2024: contracting retired teachers for shortage areas (2024/25–)",
    desc: "Part of the ‘+Aulas +Sucesso’ plan against teacher shortages, this decree-law of 28 August 2024 lets public schools sign fixed-term contracts with qualified retired teachers to fill temporary needs in shortage recruitment groups or designated under-staffed schools (‘escolas carenciadas’), subject to ministerial authorisation and an annual quota set jointly with the Finance ministry; teachers retired for more than five years are excluded. Returning retirees keep their full pension and receive an extra payment tied to the first index of the teaching salary scale, proportional to their weekly teaching hours; applications go through an online DGAE form.",
    chips: ["In force from school year 2024/25", "62 retirees cleared to return in the first round (Nov 2024, Público)", "Also: Flexible positions (part-time hours)"],
    sources: ["https://diariodarepublica.pt/dr/detalhe/decreto-lei/51-2024-885927817", "https://www.dgae.medu.pt/noticias/atribuicao-de-servico-docente-aos-aposentados-e-reformados"],
    notes: "Primary sources: Decreto-Lei n.º 51/2024 of 28 August (Diário da República) and DGAE notice on the procedure for assigning teaching service to retired teachers. Key provisions: fixed-term public-employment contracts with retired/pensioned teachers holding professional qualification, for shortage recruitment groups or under-staffed schools, with authorisation from the member of Government responsible for education; not applicable to those retired for more than five years; annual quota fixed by joint order (Finance, Public Administration, Education); pension maintained plus an additional payment corresponding to the 1st index of the salary scale according to weekly teaching hours. The figure of 62 retirees comes from Público, 5 November 2024 (press source)."
  },
  {
    country: "Singapore", region: "", flag: "sg",
    cat: "Flexible positions", groups: ["Switchers", "Leavers", "Retired"],
    title: "Flexi-Adjunct Teaching Scheme (Ministry of Education)",
    desc: "Ministry of Education scheme through which trained ex-teachers (holders of the NIE Postgraduate Diploma or Diploma in Education, including retirees) register as Flexi-Adjunct Teachers and are engaged directly by schools for short, flexible stints of 1 day to 10 weeks per appointment, for teaching only or a mix of teaching, CCA and other duties agreed with the school; pro-rated leave accrues after 90 days of cumulative service. It sits beside the Contract Adjunct scheme (1–1.5-year contracts for former MOE teachers). In 2022–2024 about 220 teachers a year were engaged as Flexi-Adjunct Teachers within 12 months of leaving the Education Service.",
    chips: ["Ongoing MOE scheme; appointments of 1 day to 10 weeks", "≈220 recent leavers a year engaged (2022–2024)", "Related: Contract Adjunct scheme (1–1.5-year contracts)"],
    sources: ["https://www.moe.gov.sg/careers/adjunct-and-relief-schemes/flexi-adjunct-teaching-scheme", "https://www.moe.gov.sg/news/parliamentary-replies/20250923-statistics-on-teachers-who-joined-flexi-adjunct-teaching-scheme-and-median-duration-of-teachers-on-scheme"],
    notes: "Sources: MOE careers page for the Flexi-Adjunct Teaching Scheme (qualification: PGDE or Diploma in Education from NIE, other professional teaching qualifications considered; appointments from 1 day to 10 weeks; teaching or mixed duties; pro-rated leave after 90 days of cumulative service; registration via the Relief Employment Management System) and MOE parliamentary reply of 23 September 2025 (2022-2024: around 220 teachers on average engaged as Flexi-Adjunct Teachers within 12 months of leaving the Education Service). Launch year of the scheme not stated on the page."
  },
  {
    country: "Sweden", region: "", flag: "se",
    cat: "Support & training", groups: ["Switchers", "Leavers"],
    title: "Skolverket web-based training for returning teachers and preschool teachers (since 2018)",
    desc: "At the Government's request, the National Agency for Education (Skolverket) built a self-paced online course for qualified teachers and preschool teachers who want to return to the profession after working elsewhere. Available on Skolverket's learning platform since October 2018, it has two tracks (school teachers; preschool teachers) and lets participants choose modules in any order, mainly updating them on the curricula, laws and steering documents that changed while they were away, with a certificate after each module. The aim is to lower the threshold to re-entry and tap the large pool of trained teachers outside the profession.",
    chips: ["Online since October 2018; government assignment reported 2020", "Two tracks: school teachers · preschool teachers", "Open to returners with a teaching licence or qualifying degree"],
    sources: ["https://www.skolverket.se/skolutveckling/kurser-och-utbildningar/atervandande-larare-och-forskollarare---webbaserad-utbildning", "https://www.skolverket.se/publikationsserier/regeringsuppdrag/2020/uppdrag-om-en-webbutbildning-for-atervandande-larare-och-forskollarare"],
    notes: "Sources: Skolverket course page 'Återvändande lärare och förskollärare – webbaserad utbildning' (available since October 2018; two tracks; participants choose modules; certificate per module; aimed at returners with legitimation or a qualifying degree) and Skolverket's 2020 report on the government assignment. No participation figures found on the pages."
  },
  {
    country: "Switzerland", region: "Canton of Zurich", flag: "ch",
    cat: "Support & training", groups: ["Switchers", "Leavers"],
    title: "PH Zürich ‘Wiedereinstieg’ re-entry programme for returning teachers",
    desc: "PH Zürich (Zurich University of Teacher Education) and the cantonal school office support qualified teachers returning to compulsory-school teaching after a long break or a career elsewhere. Re-entry starts with counselling and a ‘Standortbestimmung’ (positioning assessment, first hour free, co-funded by the canton) that checks whether returning makes sense and what preparation is needed. In the first school year back, teachers who have been out for at least eight years use PH Zürich's induction offer free of charge: workplace mentoring (up to 25 hours), individual and group supervision, subject-didactic coaching and optional courses on assessment, classroom management, differentiation and parent work.",
    chips: ["Ongoing; induction free in year one for returners after 8+ years away", "Mentoring up to 25 h, supervision, coaching, optional courses", "Also: Information & nudges (re-entry counselling)"],
    sources: ["https://phzh.ch/de/weiterbildung/weiterbildung-fuer-die-volksschule/berufslaufbahn/wiedereinstieg/"],
    notes: "Source: PH Zürich 'Wiedereinstieg' page (with the Wiedereinstiegsberatung offer). Teachers returning after at least eight years can use the induction (Berufseinführung) offer free of charge in their first school year, with financial participation of the Volksschulamt of the Canton of Zurich; the positioning assessment is subsidised by the Volksschulamt (first hour free, hours 2-6 charged); workplace mentoring (Fachbegleitung) up to 25 hours. No take-up figures published on the page."
  },
  {
    country: "United Kingdom", region: "England", flag: "gb",
    cat: "Information & nudges", groups: ["Switchers", "Leavers"],
    title: "Return to Teaching Advisers (Department for Education)",
    desc: "Anyone who previously taught or trained to teach in the UK can get a free personal Return to Teaching Adviser through the Department for Education's ‘Get Into Teaching’ service. Advisers work one-to-one by phone, text or e-mail for as long as needed: mapping skills gained during the career break, helping write applications and prepare for interviews, pointing to subject-knowledge refreshers and National Professional Qualifications, flagging vacancies and running webinars. The DfE used the same channel in its ‘Come back to teaching’ campaign of January 2022. Returners are a major supply source: about 17,500 FTE qualified teachers returned in 2023, 38% of all qualified entrants.",
    chips: ["Ongoing DfE service; ‘Come back to teaching’ campaign Jan 2022", "17,500 FTE returners in 2023 = 38% of entrants (Commons Education Committee)", "Also: Support & training (courses, NPQs)"],
    sources: ["https://getintoteaching.education.gov.uk/returning-to-teaching", "https://publications.parliament.uk/pa/cm5901/cmselect/cmeduc/627/report.html"],
    notes: "Sources: DfE 'Get Into Teaching' page 'Get support returning to teaching' (eligibility: previously taught or trained to teach in the UK; free one-to-one support with applications, courses such as NPQs, vacancies, webinars) and the House of Commons Education Committee report 'Teacher recruitment, training and retention' (returners 35-40% of entrants in recent years; about 17,500 FTE qualified returners in 2023, 38% of qualified entrants). The January 2022 'Come back to teaching' campaign is documented by local-authority pages (e.g. Warwickshire County Council)."
  },
  {
    country: "United States", region: "Georgia", flag: "us",
    cat: "Financial incentives", groups: ["Retired"],
    title: "House Bill 385: full-time return of retired teachers in high-need subjects (2022–2026)",
    desc: "Georgia law effective 1 July 2022 allowing Teachers Retirement System members who retired with 30 or more years of service, and have been retired at least one year, to be re-employed full-time as pre-K–12 classroom teachers in one of the three highest-need subject areas identified by their Regional Education Service Agency (typically special education, maths, science, English language arts and elementary) while drawing their full pension on top of a full salary. Employers pay both employee and employer contributions; retirees earn no further service credit. A 2025 state audit found about 350 full-time retirees employed each year, under 1% of Georgia's teacher workforce.",
    chips: ["1 Jul 2022 – 30 Jun 2026; succeeded by Senate Bill 150 (2026)", "≈350 retirees a year, <1% of the workforce (2025 state audit)", "Retirees keep full pension plus full salary"],
    sources: ["https://www.trsga.com/retiree/working-after-retirement/hb-385-employment/", "https://www.audits.ga.gov/ReportSearch/download/32615"],
    notes: "Sources: Teachers Retirement System of Georgia 'HB 385 Employment' page (30+ years of service, retired for one year, full-time classroom teacher in a highest-need area determined by the RESA, effective 1 July 2022 to 30 June 2026, employer pays contributions, no additional creditable service; HB 385 sunsets 30 June 2026 and SB 150 was passed in the 2026 session) and the Georgia Department of Audits and Accounts report 'Retired Teachers Return to Work' (about 350 full-time retirees employed each year, less than 1% of the workforce), summarised by Georgia Public Broadcasting, 7 May 2025."
  },
  {
    country: "United States", region: "Colorado", flag: "us",
    cat: "Flexible positions", groups: ["Retired"],
    title: "Retired Mentors for New Teachers (Aurora Public Schools; REL Central evaluation, 2017)",
    desc: "District programme that hires recently retired, highly effective Aurora teachers to mentor probationary (new) teachers in high-need Title I elementary schools for two years, with weekly mentoring and classroom observations, far more intensive than the district's usual one-year ‘buddy’ mentoring. It gives retirees a paid, part-time route back into the system while passing expertise to novices. A randomised controlled trial by REL Central (Institute of Education Sciences, 2017) with 77 teachers in 11 schools found a small positive effect on pupils' maths achievement after year one (effect size 0.06, not sustained in year two), no effect on reading and no effect on new-teacher retention.",
    chips: ["Aurora Public Schools, Colorado; RCT report 2017", "77 new teachers in 11 Title I schools; two-year mentoring", "Retired teachers as paid, part-time mentors of novices"],
    sources: ["https://ies.ed.gov/use-work/resource-library/report/descriptive-study/impacts-retired-mentors-new-teachers-program"],
    notes: "Source: Institute of Education Sciences, REL Central, 'Impacts of the Retired Mentors for New Teachers program' (DeCesare, McClelland & Randel, 2017, REL 2017-225). Design: 77 classroom teachers across 11 schools randomly assigned to mentoring by retired, highly effective district educators or to the district's business-as-usual mentoring. Results: no effect on retention; effect size 0.06 on maths achievement (significant at end of year one, not at end of year two); no effect on reading. Programme start year not stated on the summary page."
  }
];
