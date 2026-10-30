# Section 3, version 2 (OECD Style Guide, 4th edition, 2025).
# Blocks: ("h2", t) ("h3", t) ("p", t) ("cap", t) ("src", t) ("table", key)
# ("box", title, [para, ...]); a para is a list of (text, style) runs,
# style in {"", "b", "i", "src"}. Text may use *...* for italics.
# Hard spaces, curly apostrophes and quotes are applied by the builder.

B = []
def h2(t): B.append(("h2", t))
def h3(t): B.append(("h3", t))
def p(t): B.append(("p", t))
def box(title, paras): B.append(("box", title, paras))
def src(t): return [(t, "src")]

# ------------------------------------------------------------------ lead
p("Education systems have used five instruments to bring former teachers "
  "back into schools: financial incentives, information and nudges, support "
  "and training, flexible positions and flexible re-certification. This "
  "section reviews 30 policies from 18 countries. Most respond to teacher "
  "shortages, most target retired teachers and most are short-term measures "
  "adopted to fill local vacancies quickly. Take-up is small relative to the "
  "size of the teaching workforce, and few policies have been evaluated.")

p("The evidence that does exist points to two conclusions. First, single "
  "instruments achieve little on their own. The policies that report the "
  "best results combine several instruments and pay attention to the "
  "conditions that returners find in schools. Second, former teachers appear "
  "most valuable when their role draws on their experience, as mentors, "
  "tutors or flexible staff. The strongest experimental evidence in this "
  "review concerns those roles.")

p("Section 3.1 describes the policies as a whole. Sections 3.2 to 3.6 then "
  "examine each instrument in turn, with boxes on selected country cases. "
  "Section 3.7 draws lessons for the design of re-entry policies.")

# ------------------------------------------------------------------ 3.1
h2("3.1 Main features of the policies")

p("The 30 policies reviewed come from Australia, Austria, the Bahamas, "
  "Canada, China, France, Germany, Ireland, Japan, the Netherlands, "
  "New Zealand, Portugal, Singapore, Spain, Sweden, Switzerland, the "
  "United Kingdom and the United States (Table 2). They were compiled from "
  "legal texts, official documents, parliamentary records and institutional "
  "evaluations. Reputable press reports were used only where no official "
  "source exists. Officials in Lower Saxony (Germany), Quebec (Canada) and "
  "New Zealand provided further information. All policies were checked "
  "against their primary sources in October 2026. Each policy is classified "
  "under its main instrument, although many combine several.")

B.append(("cap", "Table 2. Policies to re-attract former teachers, by main "
          "instrument and target group"))
B.append(("table", "T2"))
B.append(("src", "Note: R: retired teachers; S/L: switchers and leavers; All: "
          "switchers, leavers and retired teachers. Each policy is listed "
          "under its main instrument. Secondary instruments are discussed in "
          "the text. AARP Foundation Experience Corps recruits adults aged "
          "50 and over, not only former teachers."))
B.append(("src", "Source: Legal texts, official documents, parliamentary "
          "records and evaluations cited in Section 3, verified in "
          "October 2026."))

h3("Most policies respond to teacher shortages")

p("The large majority of the policies were adopted to fill vacancies. Many "
  "target shortages that are local or concentrated in particular subjects. "
  "Georgia limited its return-to-work law to the subjects of highest need in "
  "each region, and Louisiana and Virginia to posts declared critical "
  "shortages. Portugal allowed retired teachers to be hired only for "
  "shortage subjects or under-staffed schools. Lower Saxony's letter to "
  "teachers about to retire named science, technology, engineering and "
  "mathematics (STEM), music, art and certain districts as its priorities. "
  "China sends retired teachers to rural schools in the poorest counties.")

p("The COVID-19 pandemic created or extended a large group of these "
  "policies. Absences among serving teachers multiplied the need for "
  "substitutes. Quebec introduced its incentives for retired teachers in "
  "autumn 2020, by decree under the health emergency. Ontario raised the "
  "number of days that retirees may work without losing their pension from "
  "50 to 95 in each school year from 2020/21 to 2022/23. Ireland waived the "
  "reduction of pensions for retired substitutes in 2021. In December 2021, "
  "England called on recently retired teachers and career changers to cover "
  "absences during the Omicron wave (Department for Education, 2021).")

p("A smaller group of policies pursues a different aim: to use the "
  "experience of former teachers in roles that serving teachers rarely have "
  "time for. China asks retired principals and senior teachers to coach "
  "young teachers in rural schools. In the United States, retired teachers "
  "have mentored new teachers in Aurora, Colorado, and tutored pupils who "
  "were falling behind in mathematics and reading. At the University of "
  "Zaragoza (Spain), retired teachers mentored student teachers. "
  "Singapore's adjunct teaching programme aims to keep teachers who resign "
  "in contact with schools on flexible terms.")

h3("Financial incentives are the most common instrument")

p("Financial incentives are the main instrument of 12 of the 30 policies. "
  "Most change the rules on combining a pension with a salary, as in "
  "Ireland, Lower Saxony and Michigan. Seven policies offer flexible "
  "positions, as in China and Singapore. Five rely on information and "
  "nudges, as in Lower Saxony and New South Wales (Australia). Four provide "
  "support and training, as in England and Victoria (Australia). Two make "
  "re-certification more flexible: New Zealand and Virginia.")

p("The policies target the three profiles of former teachers unevenly. Of "
  "the 30 policies, 19 target retired teachers only, 7 target switchers and "
  "leavers, and 4 are open to all three profiles. Retired teachers are easy "
  "to identify and fully qualified, and many retire before they wish to stop "
  "working altogether. The main obstacle to their return is also a rule "
  "that governments control directly: the reduction or suspension of the "
  "pension when a retiree takes paid work in the public sector (Section 2). "
  "Changing that rule is cheap and quick, which explains why it is the most "
  "common policy in the review. Switchers and leavers, who make up most "
  "former teachers below retirement age, are the target of fewer and "
  "smaller programmes.")

h3("Most policies are short-term remedies")

p("Many policies were enacted with an end date and then renewed for one "
  "period at a time. Ireland's waiver of pension reduction was introduced "
  "in 2021 and has been extended twice, most recently to the end of 2027. "
  "Michigan's rules expire in October 2028 and Virginia's in July 2028. "
  "Georgia's law expired in June 2026 and was replaced by a new law that "
  "expires in 2030. Quebec renegotiates its incentives with the teacher "
  "unions every school year. Others were reversed. Ontario's teachers' "
  "federation refused to extend the higher limit on working days in 2024. "
  "Portugal repealed its programme for hiring retired teachers in "
  "September 2026, two years after creating it, because it had ceased to be "
  "justified (Government of Portugal, 2026). This pattern reflects the "
  "purpose of most policies, which is to fill vacancies quickly. Few treat "
  "former teachers as a permanent source of teacher supply.")

h3("Take-up is small, but returners matter for teacher supply")

p("Where take-up is reported, it is small relative to the teaching "
  "workforce. In Germany, a 2023 survey of the federal states counted more "
  "than 5 000 retired teachers who had stayed on or returned, under 1% of "
  "about 800 000 teachers (Kuhn, 2023). In Georgia, about "
  "350 retirees a year returned under the state's return-to-work law, also "
  "under 1% of teachers (Georgia Department of Audits and Accounts, 2025). "
  "Portugal validated 55 retired teachers for a quota of 200 places "
  "(Observador, 2024). In Vienna, 3 of nearly 300 retired teachers contacted "
  "by the education directorate returned to school (ORF Wien, 2023).")

p("Returners nonetheless form a large share of new entrants in some "
  "systems. In England, returners accounted for 17 740 full-time equivalent "
  "qualified teachers entering state schools in 2025/26. This is 43.3% of "
  "all qualified entrants, up from 39.6% in 2023/24, and more than the "
  "16 300 newly qualified teachers who started that year (Department for "
  "Education, 2026a). In Sweden, about 3% of the teaching workforce returned "
  "in 2019 (Skolverket, 2020). Most of these returners came back without "
  "any dedicated programme. The size of this margin therefore depends on "
  "the conditions of the profession at least as much as on any single "
  "instrument.")

h3("Evidence on effectiveness is scarce")

p("Only a handful of the 30 policies have been evaluated, and only three "
  "evaluations are randomised trials (Table 3). All three concern flexible "
  "positions: retired teachers as mentors of new teachers and as tutors of "
  "young pupils. Three official reviews of re-entry programmes, in England, "
  "the Netherlands and Sweden, found low conversion of interest into "
  "returns, substantial deadweight or a failure to reach the target group. "
  "Studies of rules on combining pension and salary in Georgia, North "
  "Carolina and Virginia describe who returned and where, but cannot "
  "identify the effect of the rules on vacancies or pupil learning.")

p("The retention of returners once back in school is almost never "
  "measured. Georgia, where 43% of the retirees hired in 2023 were still "
  "teaching two years later, is an exception. In most systems the data do "
  "not allow returners to be linked to the policy that brought them back. "
  "Lower Saxony, for example, has no unique teacher identifier with which "
  "to follow individual careers.")

B.append(("cap", "Table 3. Evaluations of policies to re-attract former teachers"))
B.append(("table", "T3"))
B.append(("src", "Note: Effect sizes are standardised mean differences. Studies "
          "listed in the order of Sections 3.2 to 3.5."))
B.append(("src", "Source: Georgia Department of Audits and Accounts (2025); "
          "Jarrold-Grapes and Mahler (2024); Virginia Retirement System "
          "(2023); Tweede Kamer (2020); Resch (2025); Buchanan et al. (2018); "
          "Skolverket (2020); DeCesare et al. (2017); Gersten et al. (2015); "
          "Morrow-Howell et al. (2009)."))

# ------------------------------------------------------------------ 3.2
h2("3.2 Financial incentives")

p("Financial incentives are the most widely used instrument, and they "
  "mostly target retired teachers. They take two forms. The first, and by "
  "far the most common, is a change in the rules on combining a pension "
  "with a salary, so that retired teachers can return without losing all "
  "or part of their pension. The second consists of direct payments, either "
  "to the returning teacher or to the school that hires them. As Section 2 "
  "showed, pay brings teachers back only for as long as it is paid, while "
  "pension rules often decide whether a retired teacher can return at all.")

h3("Rules on combining pension and salary")

p("In most public-service pension plans, a retiree who takes paid work in "
  "the public sector has the pension reduced or suspended in two "
  "situations: when pension and salary together pass a threshold, or when "
  "the retiree works more than a set number of days. The policies reviewed "
  "relax these rules in three ways. Some allow a number of working days a "
  "year without any reduction. Some raise or remove the earnings ceiling. "
  "Others allow a full return, with full pension and full salary, but only "
  "in posts that are hard to fill.")

p("Ireland and Ontario (Canada) follow the first approach. In Ireland, a "
  "public-service pension is reduced when the retiree's new earnings and "
  "pension together exceed the pay the retiree received on retiring, "
  "uprated over time. Since 2021, the Department of Education has waived "
  "this reduction for the first 50 days that a retired teacher works in a "
  "calendar year. Any day worked counts as a full day, whatever the hours. "
  "The waiver applies only where the need cannot practicably be met by "
  "a teacher who is not retired, and it is lost if the retiree takes a post "
  "that extends beyond 50 days. The current circular covers 2026 and 2027 "
  "(Department of Education, 2026).")

p("In Ontario, retired teachers may work for up to 50 days in a school "
  "year and keep their full pension. Beyond that limit, the pension is "
  "suspended from the end of the month and resumes when the retiree stops "
  "working or at the start of the next school year. The provincial "
  "government and the Ontario Teachers' Federation, which sponsor the "
  "pension plan together, raised the limit to 95 days in each school year "
  "from 2020/21 to 2022/23. The higher limit applied only to positions "
  "that could not be filled by other qualified teachers, and school boards "
  "reported each month on how they used it (Ontario Teachers' Federation, "
  "2020). In March 2024, the federation declined the Ministry of "
  "Education's request to extend it again (Ontario Teachers' Federation, "
  "2024).")

p("Lower Saxony (Germany), France, Michigan and New Mexico follow the "
  "second approach. Lower Saxony raised the earnings ceiling for retired "
  "civil-service teachers from 125% to 150% of their pensionable pay in "
  "October 2022. In October 2024 it abolished the ceiling for those who "
  "have reached the statutory retirement age (Box 5). In France, a retired "
  "teacher who has claimed all pensions and receives a full-rate pension "
  "can combine pension and salary without limit. For other retirees, the "
  "pension is reduced when earnings pass a threshold (Assemblée nationale, "
  "2026). Since 2023, retirees who combine a full-rate pension with work "
  "also accrue new pension rights.")

p("Michigan's Public Act 147 of 2023 shortened the waiting period after "
  "retirement from nine to six months. After six months, a retiree may "
  "return to any school post without an earnings limit or any effect on the "
  "pension. During the waiting period, earnings are capped at USD 15 100 a "
  "year. The law expires in October 2028 (Michigan Office of Retirement "
  "Services, 2023). New Mexico's Educational Retirees Returning to Work Act "
  "of 2022 allows retirees to return 90 days after retiring, with no limit "
  "on earnings, once the Educational Retirement Board has approved the "
  "return. Returners and employers pay contributions that earn no further "
  "pension rights. The maximum period of return was 36 months and was "
  "extended to 60 months in 2025 (New Mexico Educational Retirement Board, "
  "2025). When the law was announced, about 48 000 retired educators were "
  "eligible (Office of the Governor of New Mexico, 2022).")

p("The third approach ties the full return to shortage posts. Georgia's "
  "House Bill 385 allowed teachers retired with 30 years of service to "
  "return full-time in the subjects of highest need in their region "
  "(Box 3). Louisiana's Act 344 of 2026 requires a break of 12 months after "
  "retirement and limits most returners' earnings to 50% of their final "
  "average pay, up from 25%. Returners may earn a full salary without any "
  "reduction of the pension in posts certified as critical shortages. To "
  "certify a shortage, the employer must advertise the post and receive "
  "fewer than three qualified applications from candidates who are not "
  "retired (Teachers' Retirement System of Louisiana, 2026).")

p("Virginia has allowed retirees to return to critical-shortage posts "
  "while keeping their pension since 2001. Between 2008 and 2022, retirees "
  "filled 699 such posts. In July 2023, the state shortened the required "
  "break in service from 12 to 6 months, added specialist support posts and "
  "extended the rule to July 2028. Retirees returning between July and "
  "October rose from 18 in 2022 to 150 in 2023, an increase that the "
  "state's retirement system attributes to the shorter break (Virginia "
  "Retirement System, 2023).")

p("North Carolina offers the longest experience with this approach. "
  "Between 1999 and 2009, retired teachers could return full-time and draw "
  "salary and pension together, which could raise their income by as much "
  "as half. In 1999 the rule applied only to low-performing schools, but "
  "this restriction was lifted in 2000. About 3 500 teachers returned, and "
  "52% of schools hired at least one. More than half of returners (54%) "
  "went back to their own school. Returners were more often found in the "
  "poorest schools: 30% worked in the poorest quartile of schools, against "
  "21% in the least poor quartile (Jarrold-Grapes and Mahler, 2024).")

p("Portugal took the most restrictive route. Decree-Law 51/2024 allowed "
  "schools to offer fixed-term contracts to teachers who had retired five "
  "years ago or less. The posts had to be in shortage subjects or in "
  "under-staffed schools, within an annual national quota. Returners kept "
  "their pension and received an additional payment linked to the first "
  "step of the salary scale, in proportion to their weekly hours (Government "
  "of Portugal, 2024). In the first round, 79 retirees expressed interest "
  "and 55 were validated for 200 places (Observador, 2024). The programme "
  "was repealed with effect from 1 September 2026 (Government of Portugal, "
  "2026).")

p("These rules differ in who pays. Under Georgia's law, the employer paid "
  "both the employer and the employee contributions to the pension fund, "
  "and the returner earned no further service credit. In New Mexico, "
  "Louisiana and, since 2023, Virginia, contributions are paid on the "
  "returner's salary without adding to the pension. Such designs limit the "
  "cost of the policy to the pension system and avoid rewarding early "
  "retirement.")

box("Box 2. Quebec (Canada): Paying retired teachers on their salary step", [
 [("Quebec's incentives for retired teachers began in autumn 2020, under "
   "the COVID-19 health emergency. Until then, a retired teacher who covered "
   "an absence received the flat daily rate for supply teaching. The teacher "
   "reached the salary scale only after 20 consecutive days in the same "
   "replacement. A government decree of September 2020 modified the "
   "collective agreements so that teachers retired in the previous five "
   "years were paid from the first day at the step of the salary scale that "
   "matched their experience and qualifications. They kept their full "
   "pension and paid no further contributions. For a retiree at the top of "
   "the scale, the daily pay rose from a usual maximum of about CAD 212 to "
   "about CAD 412 (Gouvernement du Québec, 2022). The government estimated "
   "the cost at about CAD 4 545 per retiree for each 20-day replacement "
   "(Conseil exécutif du Québec, 2020).", "")],
 [("From 1 October 2021, a temporary premium of 7.89% was added. The "
   "emergency measures ended with the 2021/22 school year. Since 2022/23, "
   "the incentives have been renewed each year through letters of agreement "
   "signed outside the collective agreements with each teacher union "
   "federation. The premiums have changed with each agreement: 7.89% until "
   "2023/24; 7.5% on supply work and 12.5% on contracts of three months or "
   "more in 2024/25; and 12.5% on contracts of one month or more from "
   "2025/26. The five-year limit was lifted, and the 2024/25 agreement "
   "covers any retired teacher who is legally qualified to teach. Employers "
   "must first offer the work to qualified staff they already employ.", "")],
 [("The Ministry of Education funds the measure after the fact, from the "
   "use of retired staff that school service centres report each year. The "
   "envelope for 2026/27 is being adjusted downwards, as fewer retirees are "
   "used and the 7.5% premium has been withdrawn (Ministère de l'Éducation "
   "du Québec, 2026). About 700 retirees returned in 2020/21, more than "
   "2 900 in 2022/23 and more than 5 000 in 2024/25 (Desrosiers, 2023; "
   "Le Devoir, 2025). With the premium, a retiree at the top of the scale "
   "could earn up to CAD 460 a day in 2023 (Desrosiers, 2023). In June 2023 and August 2025, the minister also wrote "
   "to retired teachers to ask them to return. The measure has not been "
   "evaluated.", "")],
 [("Lessons. ", "b"), ("Paying returners on their own salary step removes "
   "the main financial penalty of supply work for experienced teachers. The "
   "cost is moderate, because the payment is made only for days actually "
   "worked. Annual renegotiation keeps the measure responsive to shortages, "
   "but it also leaves retirees and school service centres uncertain about "
   "the terms from one year to the next.", "")],
 src("Source: Conseil exécutif du Québec (2020); Gouvernement du Québec "
     "(2022); Desrosiers (2023); Le Devoir (2025); Ministère de "
     "l'Éducation du Québec (2026)."),
])

box("Box 3. Georgia (United States): What an audit shows about returning "
    "retirees", [
 [("From July 2022 to June 2026, Georgia's House Bill 385 allowed teachers "
   "who had retired with at least 30 years of service, and had been retired "
   "for at least a year, to return to a full-time classroom post. The post "
   "had to be in one of the subjects of highest need in their region, as "
   "set by the regional education service agency. Returners drew a full "
   "salary on top of the full pension. The employer paid both the employer "
   "and the employee contributions to the pension fund, and the returner "
   "earned no further service credit.", "")],
 [("A state audit published in 2025 is one of the few assessments of such "
   "a rule. Between 2023 and 2025, 635 retirees returned under the law, "
   "rising from 241 to 428 a year. That is an average of about 350 a year, "
   "under 1% of the state's teachers. Just over half of school systems "
   "(55%) used the law, and 64% of returners went back to the system they "
   "had retired from. In 56% of the systems that used it, the post had first "
   "been offered to a candidate who was not retired. Of the 2023 cohort, 43% "
   "were still teaching two years later. Among the systems that did not use "
   "the law, 45 of 72 said they would have liked to, but could find no "
   "eligible retiree.", "")],
 [("The law expired in June 2026. Senate Bill 150 replaced it until "
   "June 2030. Under the new law, at least half of the returner's timetable "
   "must be in a qualifying subject, such as mathematics, science, special "
   "education or career and technical education. Each school system now "
   "defines its own areas of highest need from a five-year average of "
   "vacancies.", "")],
 [("Lessons. ", "b"), ("Strict eligibility keeps the cost of the rule low "
   "but also its reach. The retirees who qualify are few and are "
   "concentrated where they used to work. Defining need locally, as the new "
   "law does, may bring the rule closer to the vacancies it is meant to "
   "fill.", "")],
 src("Source: Georgia Department of Audits and Accounts (2025); Teachers "
     "Retirement System of Georgia (2026)."),
])

h3("Direct payments")

p("Direct payments to returners are less common. Quebec's measure is the "
  "clearest example (Box 2). Several other policies include a payment as a "
  "secondary instrument. Victoria pays former teachers an honorarium during "
  "a supported placement of up to 40 days (Box 9). China pays the retired "
  "teachers it posts to rural schools an allowance of CNY 20 000 a year "
  "(Box 11). New Zealand has paid the registration fees of returning "
  "teachers since October 2024, a measure extended to all teachers from "
  "July 2025 (Box 13). Portugal's additional payment for retired teachers "
  "ended with the repeal of its programme. A separate supplement of EUR 750 "
  "a month remains for teachers who could retire but keep teaching in "
  "shortage regions, which is a retention measure (Government of Portugal, "
  "2026).")

p("The Netherlands paid the school instead (Box 4). The Dutch experience "
  "illustrates a general risk of payments to employers: they may reward "
  "hiring decisions that would have been taken anyway.")

box("Box 4. The Netherlands: A grant to schools that re-hired former "
    "teachers", [
 [("From November 2017, school boards in primary education could claim a "
   "flat EUR 2 500 for each qualified teacher they hired after a break of "
   "at least 12 months from primary teaching. The contract had to last at "
   "least six months. The grant also covered qualified teachers who had "
   "never taught. It was paid to the school board to cover coaching and "
   "refresher training in the returner's first months back, and was not "
   "meant as a salary supplement. The first budget, of EUR 1.25 million, "
   "allowed for up to 500 returners by the end of 2018. Further rounds were "
   "funded in 2019 and 2020, and applications closed in October 2020 "
   "(Ministerie van OCW, 2017; 2019).", "")],
 [("The grant was used for 274 returners between October 2017 and "
   "June 2020. School boards told the ministry that most of these teachers "
   "would have been hired and supported without it. The ministry concluded "
   "that the grant had contributed only to a limited extent, and did not "
   "extend it (Tweede Kamer, 2020).", "")],
 [("The pool of potential returners is large. In 2024, 34 000 qualified "
   "primary teachers and 64 000 secondary and vocational teachers were not "
   "working in education. About 2 400 qualified teachers return to primary "
   "education each year, half as many as ten years earlier (DUO, 2026). "
   "However, most members of this pool already work in other parts of the "
   "public sector, such as health care (de Vries, van Klaveren and Stolp, "
   "2025).", "")],
 [("Lessons. ", "b"), ("A small flat grant to employers did not change "
   "hiring decisions. Schools hired the returners they needed and absorbed "
   "the cost of supporting them. A payment large enough to change behaviour, "
   "or one tied to hard-to-fill posts, would be needed to avoid "
   "deadweight.", "")],
 src("Source: Ministerie van OCW (2017; 2019); Tweede Kamer (2020); DUO "
     "(2026); de Vries, van Klaveren and Stolp (2025)."),
])

h3("What the evidence shows")

p("Three findings emerge from the evidence on financial incentives. First, "
  "the conditions attached to a rule matter as much as the incentive. When "
  "Virginia shortened the required break in service, returns in the first "
  "months of the school year rose more than eightfold. In Portugal, the "
  "limits on the date of retirement, subjects and places left most of the "
  "quota unfilled. In Georgia, 45 school systems wanted to use the rule but "
  "could find no retiree who met its conditions.")

p("Second, rules that allow a full return tend to channel retirees towards "
  "the schools that most need them. In North Carolina and Georgia, returners "
  "were concentrated in high-need subjects and, in North Carolina, in the "
  "poorest schools. Most returners also went back to the system or school "
  "where they had worked. This suggests that these rules mainly help schools "
  "keep their own experienced staff for longer.")

p("Third, these rules raise concerns that are worth anticipating. Ontario's "
  "teachers' federation refused to extend the higher limit on working days "
  "in 2024. It argued that more than 30 000 certified teachers were not "
  "employed by school boards and that a generous rule could encourage early "
  "retirement (Ontario Teachers' Federation, 2024). Returners themselves may "
  "find the experience less rewarding than expected. In Austria, retired "
  "teachers who return are hired on new contracts, and none of the "
  "14 returners interviewed in a 2025 study said they would repeat the "
  "experience (Resch, 2025).")

# ------------------------------------------------------------------ 3.3
h2("3.3 Information and nudges")

p("A second group of policies informs former teachers of the options "
  "available to them, or prompts them to consider returning. These "
  "policies use letters, calls, advisers and information sessions. They are "
  "cheap, and they respond to a barrier that Section 2 identified: many "
  "former teachers are open to returning but are not asked, do not know how "
  "to return, or expect the process to be burdensome. Lower Saxony's "
  "minister wrote to teachers about to retire that many would consider "
  "teaching a few hours a week but were put off by the paperwork "
  "(Niedersächsisches Kultusministerium, 2023).")

h3("Timing and the messenger matter")

p("Austria offers a cautionary case. In December 2022, the education "
  "directorate of Vienna contacted nearly 300 retired teachers, and three "
  "returned. At the end of February 2023, the directorate asked all school "
  "principals to consider which of their teachers could be kept on beyond "
  "the age of 65 (ORF Wien, 2023). Other Austrian provinces chose different routes. "
  "Salzburg wrote to all retired teachers up to the age of 67, and "
  "Vorarlberg sends information on staying on with the forms teachers use "
  "to apply for their pension (ORF, 2023). Nationally, 42 teachers were "
  "employed in provincial schools in autumn 2022 after joining at age 63 "
  "or older (Austrian Parliament, 2023).")

p("Lower Saxony reached the same conclusion as Vienna. It contacts "
  "teachers before they retire and combines the letter with financial and "
  "administrative changes (Box 5). Quebec has also used letters. In "
  "June 2023, the minister wrote to retired teachers to ask them to return "
  "for a day or two a week, or full-time. A second letter followed in "
  "August 2025, when more than 5 000 retirees were already back in schools "
  "(Le Devoir, 2025).")

p("Outreach can also work with teachers who left recently, when it comes "
  "with help with the procedures and with better conditions in the "
  "profession. New South Wales contacted more than 1 500 teachers who had "
  "left in the previous five years, shortly after a large pay rise "
  "(Box 6).")

box("Box 5. Lower Saxony (Germany): A package for teachers about to retire", [
 [("Lower Saxony combines three instruments aimed at teachers approaching "
   "retirement. The first is financial. A retired civil-service teacher "
   "working for the state had the pension reduced once pension and salary "
   "together exceeded 125% of the pensionable pay. In October 2022, the "
   "state parliament raised this ceiling to 150% for two years. This allowed "
   "a pensioner to teach nine to ten lessons a week on average without any "
   "reduction. In October 2024 it abolished the ceiling for teachers who "
   "have reached the statutory retirement age. Teachers who retire early "
   "remain subject to a ceiling (Niedersächsischer Landtag, 2024).", "")],
 [("The second is information. On 1 November 2023, the Minister of "
   "Education wrote to every teacher about to retire, whether a civil "
   "servant or a salaried employee. The letter set out how to stay on. A "
   "civil servant can ask to postpone retirement by up to three years, and "
   "any teacher can be re-employed on a fixed-term contract immediately "
   "after retiring while drawing the pension. The letter went to teachers "
   "approaching retirement partly because the ministry no longer held the "
   "personnel files of those who had already retired. School principals "
   "were also asked to approach these teachers in person "
   "(Niedersächsisches Kultusministerium, 2023).", "")],
 [("The third is administrative. A teacher who continues at the same "
   "school immediately after retiring does not need to apply through the "
   "online recruitment system or to provide a new police certificate. "
   "Contact persons in each of the four regional school authorities advise "
   "retirees and handle the procedure. The number of teachers past "
   "retirement age working on fixed-term contracts rose from 229 in 2020 to "
   "437 in 2024 (Niedersächsischer Landtag, 2025).", "")],
 [("According to the ministry, the first contact takes place about six "
   "months before retirement. Most returners stay at or return to the "
   "school where they last taught, usually part-time and in a specific "
   "subject such as mathematics. They rarely serve as class teachers or "
   "formal mentors. The funding for these posts must be additional, so that "
   "retirees do not take positions from young teachers. No formal "
   "evaluation has been carried out, and the state has no unique teacher "
   "identifier with which to follow individual careers.", "")],
 [("Lessons. ", "b"), ("The financial change was one part of a package. "
   "A personal letter before retirement, contact through the principal and "
   "a simpler procedure turn the decision to stay into a small step, "
   "instead of a new job application.", "")],
 src("Source: Niedersächsischer Landtag (2024; 2025); Niedersächsisches "
     "Kultusministerium (2023); information provided by the Lower Saxony "
     "Ministry of Education."),
])

box("Box 6. New South Wales (Australia): Calling back recent leavers", [
 [("From November 2023, the New South Wales Department of Education "
   "contacted more than 1 500 teachers who had left its schools in the "
   "previous five years and asked them to consider returning. Those "
   "interested were offered a simpler re-employment process and help with "
   "accreditation, approval to teach and the working-with-children check. "
   "They were then placed in casual or temporary work, with permanent posts "
   "and small-group tutoring roles also available.", "")],
 [("By May 2024, more than 260 had expressed interest and 145 had been "
   "matched with schools. About 60% of them were returning from retirement "
   "(NSW Government, 2024a). The campaign followed the largest pay rise for "
   "the state's teachers in decades, effective from October 2023. The "
   "starting salary rose from AUD 75 791 to AUD 85 000, and administrative "
   "workload was reduced (NSW Government, 2023). Teacher vacancies in the "
   "state fell from a peak of 3 311 in 2022 to 1 294 in February 2025 (NSW "
   "Government, 2025). The contribution of returners to that fall is not "
   "known.", "")],
 [("Lessons. ", "b"), ("Recent leavers can be identified from the "
   "employer's own records. A direct call with practical help converted "
   "about one in ten of those contacted. The call coincided with better pay "
   "and a lighter administrative load. This is consistent with the evidence "
   "in Section 2 that conditions in the profession weigh heavily on whether "
   "former teachers are willing to return.", "")],
 src("Source: NSW Government (2023; 2024a; 2025)."),
])

h3("Advisers and information sessions")

p("England relies on an advisory service. Former teachers can ask for an "
  "adviser who supports them one to one with applications, interviews, "
  "refresher courses and vacancies. The Department for Education's "
  "delivery plan of February 2026 lists the service and a new "
  "step-by-step guide for returners among its measures to recruit "
  "6 500 additional teachers (Department for Education, 2026b). The "
  "service also channelled the emergency call of December 2021, when "
  "former teachers were asked to cover absences through supply agencies, "
  "\"even a day a week\" (Department for Education, 2021).")

p("Japan illustrates a different use of information (Box 7). Its open "
  "licensing system has produced a large pool of licence holders who have "
  "never taught or have long been away from schools. Boards of education "
  "now run information sessions and training to bring them into temporary "
  "and part-time posts.")

box("Box 7. Japan: Information sessions for licence holders who are not "
    "teaching", [
 [("In Japan, students at any accredited university can obtain a teaching "
   "licence with a practicum of three to four weeks. Many licence holders "
   "never teach or leave early, and they form a large pool of potential "
   "teachers. On 1 May 2025, schools were short of 3 827 teachers, against "
   "2 065 in 2021 (MEXT, 2026). The Ministry of Education, Culture, Sports, "
   "Science and Technology (MEXT) encourages boards of education to bring "
   "licence holders into schools and funded such initiatives with "
   "JPY 500 million in 2024. In 2023, 50 of the 68 prefectural and city "
   "boards of education ran sessions or training for licence holders who "
   "were not teaching (MEXT, 2024).", "")],
 [("Results are reported for a few boards. In Saitama, seven seminars in "
   "2023 drew 226 participants. Of these, 122 registered for temporary or "
   "part-time posts and 53 had been appointed by April 2024. In Osaka, "
   "69 people took part in 2022 and 19 were appointed (MEXT, 2024).", "")],
 [("The session held by the Miyazaki Prefectural Board of Education on "
   "15 November 2025 shows what licence holders are told. It described a "
   "teacher's day today, team-based pupil guidance, rest days from club "
   "activities and the professional development on offer. It presented the "
   "posts available without sitting the competitive recruitment "
   "examination. Temporary full-time teachers start at JPY 241 900 a month. "
   "Part-time teachers work up to 680 hours a year at JPY 2 860 an hour, "
   "and school support staff up to 800 hours a year at about JPY 1 000 an "
   "hour. The session ended with individual consultations and registration "
   "as a temporary teacher, so that the prefecture can call on licence "
   "holders when a vacancy appears (Miyazaki Prefectural Board of "
   "Education, 2025).", "")],
 [("Lessons. ", "b"), ("Sessions built around the doubts of licence "
   "holders, such as being out of date, the workload and readiness for a "
   "permanent post, can bring a share of them into schools through flexible "
   "posts. No financial incentive is involved. Research on these "
   "initiatives in Japan is still almost non-existent.", "")],
 src("Source: MEXT (2024; 2026); Miyazaki Prefectural Board of Education "
     "(2025), translated by M. Kikuchihara."),
])

h3("What the evidence shows")

p("None of these outreach initiatives has been evaluated. In most cases "
  "the data do not link returners to the contact that prompted their "
  "return. The available figures suggest that response rates to letters "
  "sent after retirement are very low. Contact before retirement, through "
  "the principal or with help with the procedures, appears more promising.")

# ------------------------------------------------------------------ 3.4
h2("3.4 Support and training")

p("A third group of policies reduces the practical cost of returning, "
  "through refresher courses, supervised time in classrooms, coaching and "
  "induction. These measures respond to the uncertainty that former "
  "teachers often report about changes in curricula, assessment and "
  "classroom practice. They also respond to schools' doubts about teachers "
  "who lack recent experience. The evidence on these programmes is "
  "discouraging, and unusually rich for a field with so few evaluations.")

p("England's Return to Teaching pilot of 2016 drew far more interest than "
  "it could convert into posts (Box 8). A follow-up programme, the "
  "Returners Engagement Programme, ran from November 2016 until it was "
  "withdrawn in March 2018. It funded lead schools in two regions to offer "
  "returners in mathematics, physics and modern foreign languages a course "
  "of two to four weeks that included teaching practice. Support was tied "
  "to identified vacancies. Schools received GBP 1 500 for each returner "
  "they employed, and returners could claim up to GBP 600 for childcare or "
  "travel (Department for Education, 2016). This programme was not "
  "evaluated.")

p("Sweden's National Agency for Education launched a free online course "
  "for returning teachers and preschool teachers in October 2018. It "
  "covered the changes in curricula, laws and guidelines since the "
  "education reforms of 2010 and 2011. By April 2020, 1 018 people had "
  "registered, 175 had completed at least one module and 38 had completed "
  "the whole course. Only about one-third of respondents to a follow-up "
  "survey were actually returning teachers. None of the respondents who "
  "were employed had been given working time, a mentor or a study group to "
  "take the course. The course cost SEK 17 268 per participant, against "
  "SEK 863 for a comparable online course. The agency concluded that it "
  "had not reached its target group (Skolverket, 2020).")

p("Programmes that build re-entry into the school itself appear more "
  "promising, although none has been evaluated. In the canton of Zurich "
  "(Switzerland), teachers returning after eight years or more are entitled "
  "in their first year back to the same induction as new teachers, free of "
  "charge. This includes up to 25 hours of mentoring by a trained colleague "
  "in their own school, group supervision and subject coaching. Returners "
  "can also obtain an individual assessment of the preparation they need. "
  "The canton pays the first hour and the teacher the rest (PH Zürich, "
  "2026). In October 2026, however, the university of teacher education "
  "was not offering counselling for returners. Victoria (Australia) pays "
  "former teachers for up to 40 days in a school before they apply for a "
  "post (Box 9).")

box("Box 8. England (United Kingdom): Lessons from the evaluation of a "
    "return-to-teaching pilot", [
 [("From January to October 2016, the Department for Education funded "
   "60 partnerships of schools to support qualified teachers returning to "
   "secondary subjects in shortage. The support covered subject knowledge, "
   "updates on assessment and behaviour management, classroom experience "
   "and mentoring, and was free for the returner. The pilot attracted "
   "5 729 registrations, well above its target of 3 000. Of these, "
   "354 received support. By November 2016, 62 were teaching in a state "
   "school and 27 held a permanent post in the targeted subjects. The cost "
   "per additional returner was about GBP 37 400, close to the cost of "
   "training a new teacher. The independent evaluation judged the pilot "
   "unlikely to represent good value for money (Buchanan et al., 2018).", "")],
 [("The evaluation identified several reasons for the low conversion. "
   "Support began in January, when few posts for the following September "
   "remained open. Many schools hesitated to give returners teaching "
   "practice, citing the need to establish their quality and the risk of "
   "disrupting lessons. Only 44% of returners felt their needs had been met. "
   "Half of the returners and schools interviewed said that returners wanted "
   "part-time work, which few schools offered. Returners named their lack "
   "of recent experience, workload, the lack of flexible posts and their "
   "own confidence as the main barriers.", "")],
 [("Lessons. ", "b"), ("Registrations far exceeded the target, and the "
   "losses came later. Re-entry support converts best when it follows the "
   "recruitment calendar, is linked to real vacancies, includes time in "
   "front of a class and is matched by schools willing to offer part-time "
   "posts.", "")],
 src("Source: Buchanan et al. (2018)."),
])

box("Box 9. Victoria (Australia): A paid placement before applying", [
 [("Victoria's Teacher Re-Engagement Initiative, launched in late 2022, "
   "offers registered teachers who have been away from teaching for at "
   "least 12 months a paid placement of up to 40 days in a government "
   "school. During the placement they observe classes and school routines "
   "and are mentored by serving staff, before they apply for a post. A "
   "central team matches participants with schools by subject, experience, "
   "location and availability. At the end of the placement, the team "
   "records whether the participant has returned to teaching.", "")],
 [("The initiative drew more than 1 100 expressions of interest and "
   "received AUD 12 million in the 2023/24 state budget (Victorian "
   "Government, 2023). It is now funded by the schools that host a "
   "returner, at AUD 330 a day to cover the participant's honorarium and "
   "administrative costs (Victorian Government, 2026). No figures have been "
   "published on the number of participants who went on to teach.", "")],
 [("Lessons. ", "b"), ("A supervised placement answers both the "
   "returner's lack of confidence and the school's uncertainty about the "
   "returner, the two obstacles identified by the evaluation in England "
   "(Box 8). Shifting the cost to schools may limit take-up to those that "
   "can afford it.", "")],
 src("Source: Victorian Government (2023; 2026)."),
])

h3("What the evidence shows")

p("No causal evaluation of refresher or re-entry support has been found. "
  "The two programmes with official reviews, in England and Sweden, reached "
  "many interested people but few actual returners. In both cases the "
  "support was detached from schools and from vacancies. The retention of "
  "returners after re-entry has not been measured in any programme.")

# ------------------------------------------------------------------ 3.5
h2("3.5 Flexible positions")

p("A fourth group of policies offers former teachers roles other than a "
  "full-time teaching post: relief and adjunct teaching, tutoring and "
  "mentoring. These roles match the preferences that many former teachers "
  "express. As Section 2 showed, leavers with care responsibilities and "
  "retirees often want to work part of the week. In England, half of the "
  "returners and schools interviewed reported a demand for part-time work "
  "(Buchanan et al., 2018). Flexible roles also allow systems to use "
  "experience where it is most valuable.")

h3("Pools of flexible teachers")

p("Standing pools of former teachers are the simplest version of this "
  "instrument. Singapore has run an adjunct programme for former teachers "
  "since 2004 (Box 10). In July 2026, the Bahamas announced a reserve of "
  "former teachers, retirees and recent graduates, built on its "
  "supply-teacher platform. It is part of a drive to fill about "
  "300 vacancies in 162 public schools on 24 islands. A task force of "
  "several government agencies checks records and accreditation so that "
  "recruits can start quickly. By September 2026, more than 100 teachers "
  "had been recruited through the drive and about 100 more were being "
  "vetted (Ministry of Education of The Bahamas, 2026; ZNS Bahamas, 2026). "
  "Rules on combining pension and salary, such as those in Ireland and "
  "Ontario, also create a pool of retired substitutes.")

box("Box 10. Singapore: An adjunct programme for former teachers", [
 [("Singapore's Ministry of Education launched an adjunct teachers "
   "programme in 2004 to attract former trained teachers back to the "
   "profession on more flexible terms. Under the current Flexi-Adjunct "
   "Teaching Scheme, former teachers register on a ministry portal for "
   "three years. Schools contact them directly for appointments of one day "
   "to ten weeks, for teaching alone or for teaching and other duties "
   "agreed with the school. They are paid by the hour, in tiers that depend "
   "on experience, and earn leave once they have accumulated 90 days of "
   "service. Former ministry teachers must have performed well in their "
   "last three years of service (Ministry of Education Singapore, 2026a). "
   "A companion programme offers former ministry teachers contracts of one "
   "to one and a half years, full-time or part-time (Ministry of Education "
   "Singapore, 2026b).", "")],
 [("From 2022 to 2024, about 220 teachers a year joined the programme "
   "within 12 months of leaving the service. The annual resignation rate "
   "of teachers was 2.4%, or 1.7% excluding those who joined the programme "
   "(Ministry of Education Singapore, 2025a; 2025b). Pay at the highest "
   "tier is below 60% of the median pay package of a classroom teacher "
   "(Ministry of Education Singapore, 2024).", "")],
 [("Lessons. ", "b"), ("A standing pool lets a system keep in contact "
   "with teachers at the moment they leave, before their skills and their "
   "links with schools fade. It allows those who leave for family or other "
   "reasons to keep a foot in the profession on terms they choose. Pay well "
   "below that of regular teachers keeps the programme cheap, but limits "
   "its use to occasional cover.", "")],
 src("Source: Ministry of Education Singapore (2024; 2025a; 2025b; 2026a; "
     "2026b)."),
])

h3("Placements in schools that struggle to attract teachers")

p("China's Silver-Age Lecturing Plan sends retired teachers to rural "
  "schools in the poorest counties (Box 11). It is the largest programme "
  "in this review, and the only one that places returners in schools far "
  "from where they used to work. It also gives them an explicit role in "
  "developing the school's young teachers.")

box("Box 11. China: Retired teachers for rural schools", [
 [("China's Silver-Age Lecturing Plan was launched in 2018 by the "
   "Ministries of Education and Finance. It recruits retired principals, "
   "teaching researchers and senior teachers, generally aged 65 or under, "
   "to serve for at least a school year in rural primary and "
   "lower-secondary schools. The schools are in poor, ethnic-minority and "
   "border counties. Returning to one's own former school does not count. "
   "Participants teach classes, observe lessons and give demonstration "
   "lessons, coach the school's young teachers and help with school "
   "management. Since 2024, retired principals may serve as deputy heads. "
   "Participants keep their pension and receive CNY 20 000 a year for "
   "living costs, travel and insurance. The central government pays in "
   "western provinces, central and provincial governments share the cost "
   "in central provinces, and eastern provinces pay alone (Ministry of "
   "Education and Ministry of Finance of the People's Republic of China, "
   "2018).", "")],
 [("The first plan set a target of 10 000 places for 2018-2020. More than "
   "20 000 retired teachers had been recruited to primary and secondary "
   "schools by mid-2023 (Ministry of Education of the People's Republic of "
   "China, 2023). Recent annual rounds have planned 6 000 to 7 000 places. "
   "The 2026 round makes the coaching of young teachers central to the "
   "role and adds an assessment by the host school at the end of each "
   "placement (Ministry of Education of the People's Republic of China, "
   "2026). No independent evaluation has been published.", "")],
 [("Lessons. ", "b"), ("The plan uses retired teachers above all to "
   "transfer experience to schools that struggle to attract and develop "
   "teachers. This is the use of former teachers that the evidence on "
   "mentoring and peer learning supports (Section 2).", "")],
 src("Source: Ministry of Education and Ministry of Finance of the People's "
     "Republic of China (2018); Ministry of Education of the People's "
     "Republic of China (2023; 2026)."),
])

h3("Mentors and tutors")

p("Mentoring and tutoring by retired teachers have been tested more "
  "rigorously than any other instrument in this review (Box 12). Three "
  "randomised trials in the United States found positive effects on pupils' "
  "learning. The effects were small for the mentoring of new teachers, and "
  "larger for the tutoring of pupils who were falling behind. These results "
  "are consistent with the broader experimental evidence on tutoring cited "
  "in Section 1 (Nickow, Oreopoulos and Quan, 2024). They suggest that "
  "tutoring is one of the most productive uses of former teachers who do "
  "not wish to return to a full post.")

p("Smaller initiatives point in the same direction. At the University of "
  "Zaragoza (Spain), ten retired early-childhood and primary teachers "
  "mentored 57 student teachers in the final years of their degree in "
  "2018. Each group met three times, on the profession, on further training "
  "and on the teaching career. Of the students who responded to a survey, "
  "56% said the sessions had helped them to choose their path (Lizalde Gil "
  "and Cortés Pascual, 2019).")

box("Box 12. United States: Evidence from three randomised trials on "
    "retired teachers as mentors and tutors", [
 [("Mentoring new teachers. ", "b"), ("In Aurora, Colorado, recently "
   "retired teachers and principals mentored teachers in their first three "
   "years in 11 high-poverty elementary schools, in 2013/14 and 2014/15. "
   "Mentors were paid USD 41 an hour and met each new teacher for about an "
   "hour a week over two years. A randomised trial of 77 teachers compared "
   "them with the district's usual support, a colleague paid a small "
   "stipend. Pupils of mentored teachers gained 0.064 standard deviations "
   "in mathematics after the first year, about one month of learning. The "
   "effect was of similar size after the second year, but was no longer "
   "statistically significant. There was no effect on reading or on whether "
   "the new teachers stayed (DeCesare et al., 2017).", "")],
 [("Tutoring in mathematics. ", "b"), ("In 76 schools in four urban "
   "districts, first graders with weak number skills received about 30 "
   "hours of small-group tutoring over 17 weeks. Most of the 86 tutors were "
   "retired or substitute teachers, hired through a temporary staffing "
   "company and trained for one day plus two short follow-up sessions. In "
   "a randomised trial of 994 pupils, tutored pupils outperformed their "
   "peers by an effect size of 0.34 (Gersten et al., 2015).", "")],
 [("Tutoring in reading. ", "b"), ("AARP Foundation Experience Corps "
   "trains volunteers aged 50 and over, among them former teachers, to "
   "tutor children so that they read well by the end of grade 3. In "
   "2023/24, 1 284 volunteers worked with 3 659 children in 18 communities "
   "(AARP Foundation, 2026). A randomised evaluation in 23 schools in "
   "Boston, New York City and Port Arthur found gains in reading "
   "comprehension, with effect sizes of 0.13 to 0.17 for pupils who "
   "attended 35 sessions or more (Morrow-Howell et al., 2009).", "")],
 [("Lessons. ", "b"), ("Short training is enough for experienced teachers "
   "to tutor effectively. The returns on mentoring new teachers are smaller "
   "and depend on the time mentors can spend with them.", "")],
 src("Source: DeCesare et al. (2017); Gersten et al. (2015); "
     "Morrow-Howell et al. (2009); AARP Foundation (2026)."),
])

# ------------------------------------------------------------------ 3.6
h2("3.6 Flexible re-certification")

p("A final group of policies lowers the regulatory barriers to returning. "
  "Section 2 showed that licensing rules rarely drive qualified teachers "
  "out of the profession, but can stand in the way of their return. A "
  "teacher who has been away for several years may need to renew a lapsed "
  "licence or complete a refresher programme before teaching again. That "
  "process can take months and cost money, at the moment when a school is "
  "waiting to fill a post.")

p("New Zealand has gone furthest. It replaced its refresher course with a "
  "plan agreed with the school that offers the returner a job (Box 13). In "
  "the United States, Virginia's Executive Directive 3 of September 2022 "
  "instructed the state's licensing authority to issue licences to retired "
  "teachers whose licences had lapsed. In November 2023, the state "
  "launched an online licensing system (Commonwealth of Virginia, 2022). "
  "Other policies include lighter forms of the same instrument. New South "
  "Wales helped returners with accreditation (Box 6), and Lower Saxony "
  "waives a new police certificate for teachers who continue at their "
  "school after retiring (Box 5). In the Bahamas, a government task force "
  "checks records and accreditation so that recruits can start without "
  "delay.")

box("Box 13. New Zealand: From a refresher course to a plan agreed with "
    "the school", [
 [("To renew a practising certificate, a New Zealand teacher must have at "
   "least two years of satisfactory teaching in the previous five. Teachers "
   "who did not meet this requirement used to complete an external "
   "refresher programme, the Teacher Education Refresh. Since "
   "September 2024, the Teaching Council has allowed returners with a job "
   "offer to replace it with a return-to-practice plan. In December 2025, "
   "the Council made this route permanent from January 2026 under the name "
   "Kia Maia, and extended it to some teachers who would otherwise need the "
   "refresher programme (Teaching Council of Aotearoa New Zealand, 2025).", "")],
 [("The returner assesses, with the principal of the school that has "
   "offered the job, what has changed since they last taught. The plan "
   "lists at least three resources for each professional standard that the "
   "returner will use during the first 12 months back. Both sign the plan. "
   "Council staff review it without assessing the teacher's competence, "
   "and the certificate is renewed. Without a job offer, the refresher "
   "programme is still likely to be required (Teaching Council of Aotearoa "
   "New Zealand, 2026).", "")],
 [("The government also paid the registration fees of returning teachers "
   "from October 2024, supporting 352 returners by April 2025. It has "
   "covered the fees of all teachers since July 2025, with NZD 53.3 million "
   "over three years (Ministry of Education New Zealand, 2025). From "
   "January to October 2026, 501 teachers renewed their certificate through "
   "Kia Maia. Most worked in primary (198) or secondary (133) schools or in "
   "early childhood education (110). Women made up 84% of users, and 62% "
   "were aged 31 to 50. Only 16% were aged 61 or over (Teaching Council of "
   "Aotearoa New Zealand, unpublished). The pathway thus mainly brings back "
   "mid-career teachers who had stepped away.", "")],
 [("Lessons. ", "b"), ("Replacing an external course with a plan agreed "
   "with the employing school removes a cost and a delay at the moment the "
   "returner has a job in hand. It also involves the principal in the "
   "returner's first year, which the evidence on induction and leadership "
   "in Section 2 suggests matters for whether returners stay.", "")],
 src("Source: Teaching Council of Aotearoa New Zealand (2025; 2026; "
     "unpublished); Ministry of Education New Zealand (2025)."),
])

p("No evaluation of these changes is available. New Zealand's data show "
  "who uses the new route, but not whether its users would have returned "
  "through the refresher programme. Collecting comparable data before and "
  "after the change would allow the effect of the reform to be measured.")

# ------------------------------------------------------------------ 3.7
h2("3.7 Lessons for the design of re-entry policies")

p("Five lessons emerge from the 30 policies reviewed. They should be read "
  "with caution, since few policies have been evaluated.")

p("First, instruments work best in combination. Lower Saxony paired the "
  "removal of a financial penalty with a personal letter and a simpler "
  "procedure. New South Wales called back recent leavers after a large pay "
  "rise and a cut in administrative work. New Zealand tied re-certification "
  "to a job offer and to the school's principal. In contrast, the "
  "programmes that offered support or money alone, without suitable posts "
  "or schools willing to take returners, converted little of the interest "
  "they raised.")

p("Second, timing matters. Contact before retirement or at the moment of "
  "leaving reaches teachers while their skills and links with schools are "
  "intact. Lower Saxony writes to teachers about to retire, and Singapore "
  "engages teachers within a year of their resignation. Support offered "
  "after posts have been filled, as in the English pilot, is largely "
  "wasted.")

p("Third, the role offered to returners should match their preferences "
  "and their experience. Many returners want part-time work, and the "
  "strongest evidence of benefits for pupils concerns retired teachers as "
  "tutors and mentors. Policies that only offer a full-time post in a "
  "hard-to-staff school risk sending returners back to the conditions that "
  "led them to leave (Section 2).")

p("Fourth, conditions decide take-up. Waiting periods, limits on the date "
  "of retirement and narrow eligibility rules determined the reach of the "
  "pension policies reviewed, as the cases of Georgia, Portugal and "
  "Virginia show. Designs that pay contributions without new pension "
  "rights can widen access while containing costs and avoiding incentives "
  "to retire early.")

p("Fifth, systems need data to learn from these policies. Few systems can "
  "link returners to the policy that brought them back or follow how long "
  "they stay. A unique teacher identifier, records of who was contacted and "
  "how, and evaluations built into new policies from the start would allow "
  "governments to know which instruments work. Re-entry policies remain a "
  "complement to retention. The evidence in Section 2 suggests that the "
  "conditions that keep teachers in the profession are the same as those "
  "that bring them back.")

# ------------------------------------------------------------------ tables
TABLES = {
 "T2": {
  "widths": (2100, 6960),
  "rows": [
   ("Instrument", "Policies reviewed (target group)"),
   ("Financial incentives",
    "Canada: Ontario (R), Quebec (R); France (R); Germany: Lower Saxony, "
    "earnings ceiling (R); Ireland (R); Netherlands (S/L); Portugal (R); "
    "United States: Georgia (R), Louisiana (R), Michigan (R), New Mexico (R), "
    "North Carolina (R)"),
   ("Information and nudges",
    "Australia: New South Wales (All); Austria (R); Germany: Lower Saxony, "
    "letter (R); Japan: Miyazaki (S/L); United Kingdom: England, advisers "
    "(S/L)"),
   ("Support and training",
    "Australia: Victoria (All); Sweden (S/L); Switzerland: Zurich (S/L); "
    "United Kingdom: England, pilot programme (S/L)"),
   ("Flexible positions",
    "Bahamas (All); China (R); Singapore (All); Spain: Zaragoza (R); "
    "United States: AARP Foundation Experience Corps (R), Colorado (R), "
    "four urban districts (R)"),
   ("Flexible re-certification",
    "New Zealand (S/L); United States: Virginia (R)"),
  ]},
 "T3": {
  "widths": (2000, 2400, 4660),
  "rows": [
   ("Policy", "Assessment", "Main findings"),
   ("Georgia (United States), return to work in high-need subjects",
    "State audit of administrative data, 2023-2025",
    "About 350 returners a year, under 1% of teachers; 64% returned to "
    "their former system; 43% of the 2023 cohort still teaching two years "
    "later"),
   ("North Carolina (United States), full return with pension, 1999-2009",
    "Descriptive study of administrative data",
    "About 3 500 returners; 54% returned to their own school; returners "
    "more often employed in the poorest schools; effects on vacancies not "
    "identified"),
   ("Virginia (United States), return to critical-shortage posts",
    "Retirement system report",
    "Shorter break in service raised July-October returns from 18 to 150"),
   ("Netherlands, grant to schools that re-hire former teachers",
    "Ministry evaluation based on school boards' reports",
    "274 returners funded; most would have been hired anyway; not "
    "extended"),
   ("Austria, retired teachers recruited back",
    "Qualitative study, 14 interviews",
    "None of the returners interviewed would repeat their return"),
   ("England (United Kingdom), Return to Teaching pilot",
    "Independent evaluation with comparison group",
    "5 729 registrations, 354 supported, 27 in permanent posts; "
    "GBP 37 400 per additional returner"),
   ("Sweden, online course for returning teachers",
    "Agency report with participant survey",
    "1 018 registered, 38 completed the course; did not reach its target "
    "group"),
   ("Colorado (United States), retired teachers mentor new teachers",
    "Randomised trial, 77 teachers",
    "Mathematics +0.064 after year 1, not significant after year 2; no "
    "effect on reading or retention"),
   ("Four urban districts (United States), mathematics tutoring",
    "Randomised trial, 994 pupils",
    "Mathematics +0.34"),
   ("AARP Foundation Experience Corps (United States), reading tutoring",
    "Randomised trial, 23 schools",
    "Reading comprehension +0.13 to +0.17 for pupils with 35 sessions or "
    "more"),
  ]},
}

# ------------------------------------------------------------------ refs
# *...* marks italics. OECD Style Guide (2025) formats.
ACC = " (accessed on 30 October 2026)"
REFS = [
 "AARP Foundation (2026), “Experience Corps”, https://www.aarp.org/experience-corps/" + ACC + ".",
 "Assemblée nationale (2026), “Question écrite n° 11063: Cumul emploi-retraite”, réponse publiée le 12 mai 2026, https://questions.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE11063.pdf" + ACC + ".",
 "Austrian Parliament (2023), Anfragebeantwortung 12765/AB zu 13105/J, XXVII. Gesetzgebungsperiode, 18 January 2023, https://www.parlament.gv.at/dokument/XXVII/AB/12765/imfname_1504460.pdf" + ACC + ".",
 "Buchanan, E. et al. (2018), *Evaluation of the Return to Teaching Pilot Programme: Final Report*, National Foundation for Educational Research, Slough, https://assets.publishing.service.gov.uk/media/5b33aeef40f0b67f6744de9d/Evaluation_of_the_Return_to_Teaching_pilot_programme.pdf.",
 "Commonwealth of Virginia (2022), Executive Directive Three (2022): Addressing Teacher Shortages in Virginia Schools, Office of the Governor, Richmond, 1 September 2022, https://www.governor.virginia.gov/media/governorvirginiagov/governor-of-virginia/pdf/ed/ED-3-Addressing-Teacher-Shortages-in-Virginia-Schools.pdf.",
 "Conseil exécutif du Québec (2020), “Mémoire au Conseil des ministres: Retour des enseignants retraités”, Gouvernement du Québec, Quebec City, https://cdn-contenu.quebec.ca/cdn-contenu/gouvernement/MCE/dossiers-soumis-conseil-ministres/Memoire-Retour-des-enseignants-retraites.pdf" + ACC + ".",
 "de Vries, R., C. van Klaveren and M. Stolp (2025), “Herintrede leraren uit stille reserve beperkte oplossing voor tekorten”, *ESB*, 27 June 2025, https://esb.nu/herintrede-leraren-uit-stille-reserve-beperkte-oplossing-voor-tekorten/" + ACC + ".",
 "Desrosiers, S. (2023), “La prime de 12 000 $ boudée par des enseignants retraités”, *Radio-Canada*, 5 July 2023, https://ici.radio-canada.ca/nouvelle/1993748/prime-enseignants-retraite-quebec-penurie" + ACC + ".",
 "Department for Education (2016), “Returners Engagement Programme”, https://www.gov.uk/government/publications/returners-engagement-programme" + ACC + ".",
 "Department for Education (2021), “Education Secretary calls for ex-teachers to return to classrooms”, press release, 20 December 2021, https://www.gov.uk/government/news/education-secretary-calls-for-ex-teachers-to-return-to-classrooms" + ACC + ".",
 "Department for Education (2026a), *School Workforce in England: Reporting Year 2025*, Department for Education, London, https://explore-education-statistics.service.gov.uk/find-statistics/school-workforce-in-england.",
 "Department for Education (2026b), *6,500 Additional Teachers: Delivery Plan*, CP 1508-II, Department for Education, London, https://assets.publishing.service.gov.uk/media/6995de6aa58a315dbe72bf7c/6500_additional_teachers_delivery_plan_print_ready_version.pdf.",
 "Department of Education (2026), Circular 0017/2026: Extension to the Waiver of Abatement of Public Service Pensions for Retired Teachers, Department of Education, Dublin, 26 January 2026.",
 "Kuhn, A. (2023), “Mehrheit der Länder wirbt gezielt um Lehrkräfte im Pensionsalter”, *Deutsches Schulportal*, 2 August 2023, https://deutsches-schulportal.de/bildungswesen/laenderueberblick-umfrage-lehrermangel-pensionierte-lehrer/" + ACC + ".",
 "DUO (2026), “Stille reserve oud-leraren in het onderwijs afgelopen 10 jaar afgenomen”, press release, 28 May 2026, https://duo.nl/organisatie/pers/stille-reserve-oud-leraren-in-het-onderwijs-afgelopen-10-jaar-afgenomen.jsp" + ACC + ".",
 "Georgia Department of Audits and Accounts (2025), *Retired Teachers Return to Work*, Report No. 24-20, Atlanta, https://www.audits.ga.gov/ReportSearch/download/32615.",
 "Gersten, R. et al. (2015), “Intervention for first graders with limited number knowledge: Large-scale replication of a randomized controlled trial”, *American Educational Research Journal*, Vol. 52/3, pp. 516-546, https://doi.org/10.3102/0002831214565787.",
 "Gouvernement du Québec (2022), “Opération main-d’œuvre: Offensive pour attirer davantage de personnel dans le domaine de l’éducation”, press release, 24 January 2022, https://newswire.ca/fr/news-releases/operation-main-d-oeuvre-offensive-pour-attirer-davantage-de-personnel-dans-le-domaine-de-l-education-803384845.html" + ACC + ".",
 "Government of Portugal (2024), Decreto-Lei n.º 51/2024, de 28 de agosto, *Diário da República*, Lisbon, https://diariodarepublica.pt/dr/detalhe/decreto-lei/51-2024-885927817.",
 "Government of Portugal (2026), Decreto-Lei n.º 175/2026, de 3 de setembro, *Diário da República*, Lisbon.",
 "Jarrold-Grapes, J. and P. Mahler (2024), “Retirees return to work: How a North Carolina policy helped staff high-need schools”, *Education Policy Analysis Archives*, Vol. 32/4, https://files.eric.ed.gov/fulltext/EJ1425366.pdf.",
 "Le Devoir (2025), “Québec espère de nouveau attirer des milliers d’enseignants retraités dans les écoles”, *Le Devoir*, 29 August 2025, https://www.ledevoir.com/actualites/education/912921/quebec-espere-nouveau-attirer-milliers-enseignants-retraites-ecoles" + ACC + ".",
 "Lizalde Gil, M. and A. Cortés Pascual (2019), “10 mirrors: El acompañamiento y la orientación formativa de los estudiantes de los grados en magisterio desde la experiencia profesional”, in *Orientación y calidad educativa universitarias*, Prensas de la Universidad de Zaragoza, Zaragoza, https://zaguan.unizar.es/record/79095/files/BOOK-2019-021.pdf.",
 "MEXT (2024), “Case collection on training for teaching-licence holders not currently teaching”, Ministry of Education, Culture, Sports, Science and Technology, Tokyo, https://www.mext.go.jp/content/20240617-mxt_syokyo02-000036498_6.pdf" + ACC + ".",
 "MEXT (2026), “Results of the survey on the shortage of teachers, fiscal year 2025”, Ministry of Education, Culture, Sports, Science and Technology, Tokyo, https://www.mext.go.jp/content/20260302-mxt_kyoikujinzai01-000047773_1_1.pdf" + ACC + ".",
 "Michigan Office of Retirement Services (2023), “Public Act 147 of 2023 FAQs”, https://www.michigan.gov/orsschools/pa-147-of-2023-faqs" + ACC + ".",
 "Ministère de l’Éducation du Québec (2026), “Incitatifs financiers aux personnes retraitées effectuant un retour à l’enseignement”, presentation to the OECD, 14 October 2026, Quebec City.",
 "Ministerie van OCW (2017), Regeling tegemoetkoming herintreders primair onderwijs, *Staatscourant* 2017, nr. 62002, The Hague, https://zoek.officielebekendmakingen.nl/stcrt-2017-62002.html.",
 "Ministerie van OCW (2019), Wijziging van de Regeling tegemoetkoming herintreders primair onderwijs, *Staatscourant* 2019, nr. 28510, The Hague, https://zoek.officielebekendmakingen.nl/stcrt-2019-28510.html.",
 "Ministry of Education and Ministry of Finance of the People’s Republic of China (2018), Notice on the Implementation of the Silver-Age Lecturing Plan, Jiaoshi [2018] No. 7, Beijing, http://www.moe.gov.cn/srcsite/A10/s7151/201807/t20180719_343448.html.",
 "Ministry of Education New Zealand (2025), “Budget 2025: Fund New Zealand teacher practising certificates”, https://workforce.education.govt.nz/budget-2025-fund-new-zealand-teacher-practising-certificates-0" + ACC + ".",
 "Ministry of Education of the People’s Republic of China (2023), news release, 1 September 2023, https://www.moe.gov.cn/jyb_xwfb/s5147/202309/t20230901_1077691.html" + ACC + ".",
 "Ministry of Education of the People’s Republic of China (2026), Notice on the 2026 Silver-Age Lecturing Plan, Jiaoshi Tinghan [2026] No. 9, Beijing, http://www.moe.gov.cn/srcsite/A10/s7151/202609/t20260929_1452671.html.",
 "Ministry of Education of The Bahamas (2026), “The Ministry of Education aiming to attract more Bahamian teachers”, press release, 17 July 2026, https://www.bahamas.gov.bs/news-press-release/the-ministry-of-education-aiming-to-attract-more-bahamian-teachers" + ACC + ".",
 "Ministry of Education Singapore (2024), “Median annual salary of flexi-adjunct teachers in past five years”, parliamentary reply, 9 January 2024, https://www.moe.gov.sg/news/parliamentary-replies/20240109-median-annual-salary-of-flex-adjunct-teachers-in-past-five-years" + ACC + ".",
 "Ministry of Education Singapore (2025a), “Statistics on teachers who joined Flexi-Adjunct Teaching Scheme and median duration of teachers on scheme”, parliamentary reply, 23 September 2025, https://www.moe.gov.sg/news/parliamentary-replies/20250923-statistics-on-teachers-who-joined-flexi-adjunct-teaching-scheme-and-median-duration-of-teachers-on-scheme" + ACC + ".",
 "Ministry of Education Singapore (2025b), “Number of teachers who have entirely left teaching profession in last three years”, parliamentary reply, 25 September 2025, https://www.moe.gov.sg/news/parliamentary-replies/20250925-number-of-teachers-who-have-entirely-left-teaching-profession-in-last-three-years" + ACC + ".",
 "Ministry of Education Singapore (2026a), “Flexi-Adjunct Teaching Scheme”, https://www.moe.gov.sg/careers/adjunct-and-relief-schemes/flexi-adjunct-teaching-scheme" + ACC + ".",
 "Ministry of Education Singapore (2026b), “Contract Adjunct Teaching Scheme”, https://www.moe.gov.sg/careers/adjunct-and-relief-schemes/contract-adjunct-teaching-scheme" + ACC + ".",
 "Miyazaki Prefectural Board of Education (2025), “Information session on the appeal of teaching”, Miyazaki, https://www.pref.miyazaki.lg.jp/documents/102783/102783_20250930165145-1.pdf" + ACC + ".",
 "Morrow-Howell, N. et al. (2009), *Evaluation of Experience Corps: Student Reading Outcomes*, Center for Social Development, Washington University in St. Louis, St. Louis.",
 "New Mexico Educational Retirement Board (2025), “Return to work comparison table”, https://www.erb.nm.gov/rtw-comparison-table/" + ACC + ".",
 "Niedersächsischer Landtag (2024), Drucksache 19/5338, Hanover, https://landtag-niedersachsen.de/drucksachen/drucksachen_19_07500/05001-05500/19-05338.pdf.",
 "Niedersächsischer Landtag (2025), Drucksache 19/8802: Antwort der Landesregierung, Hanover, https://www.landtag-niedersachsen.de/drucksachen/drucksachen_19_10000/08501-09000/19-08802.pdf.",
 "Niedersächsisches Kultusministerium (2023), “Schreiben an angehende Pensionärinnen und Pensionäre”, 1 November 2023, Hanover, https://www.mk.niedersachsen.de/download/201317/Schreiben_an_angehende_Pensionaerinnen_und_Pensionaere.pdf" + ACC + ".",
 "NSW Government (2023), “NSW teachers to receive largest pay rise in decades”, media release, https://www.nsw.gov.au/media-releases/nsw-teachers-to-receive-largest-pay-rise-in-decades" + ACC + ".",
 "NSW Government (2024a), “Retired teachers return to classrooms”, media release, 8 May 2024, https://www.nsw.gov.au/media-releases/retired-teachers-return-to-classrooms" + ACC + ".",
 "NSW Government (2025), “Teacher vacancies drop under Minns Labor Government”, media release, https://www.nsw.gov.au/ministerial-releases/teacher-vacancies-drop-under-minns-labor-government" + ACC + ".",
 "Observador (2024), “A partir de janeiro, 55 professores que estavam reformados vão poder voltar a dar aulas”, *Observador*, 19 December 2024, https://observador.pt/2024/12/19/a-partir-de-janeiro-55-professores-que-estavam-reformados-vao-poder-voltar-a-dar-aulas/" + ACC + ".",
 "Office of the Governor of New Mexico (2022), “Retired educators now eligible to return to work without losing pension benefits”, press release, 28 June 2022, https://www.governor.state.nm.us/2022/06/28/retired-educators-now-eligible-to-return-to-work-without-losing-pension-benefits/" + ACC + ".",
 "Ontario Teachers’ Federation (2020), “50-day re-employment rule increased to 95 days for some OTPP retirees until June 30, 2021”, Toronto, https://www.otffeo.on.ca/en/wp-content/uploads/sites/2/2020/11/50-Day-Re-employment-Rule-increased-to-95-Days-for-some-OTPP-retirees-until-June-30-2021.pdf" + ACC + ".",
 "Ontario Teachers’ Federation (2024), “OTF declines Ministry of Education’s request to amend 50-day re-employment rule”, 4 March 2024, https://www.otffeo.on.ca/en/news/otf-declines-ministry-of-educations-request-to-amend-50-day-re-employment-rule/" + ACC + ".",
 "ORF (2023), “Lehrkräftemangel: Pensionisten umworben”, 11 March 2023, https://oesterreich.orf.at/stories/3198263/" + ACC + ".",
 "ORF Wien (2023), “Pensionisten kehren kaum in Job zurück”, 29 March 2023, https://wien.orf.at/stories/3200562/" + ACC + ".",
 "PH Zürich (2026), “Wiedereinstieg in den Lehrberuf”, Pädagogische Hochschule Zürich, https://phzh.ch/de/weiterbildung/weiterbildung-fuer-die-volksschule/berufslaufbahn/wiedereinstieg/" + ACC + ".",
 "Resch, K. (2025), “Retired teachers return to school to tackle teacher shortages in Austrian schools: An untapped reserve or emergency response?”, *European Journal of Teacher Education*, https://doi.org/10.1080/02619768.2025.2531930.",
 "Skolverket (2020), *Webbutbildning för återvändande lärare och förskollärare: Redovisning av uppdrag*, Dnr 2019:01515, Swedish National Agency for Education, Stockholm, https://www.skolverket.se/download/18.70f8d1a017495c3cb593080/1608285624392/Pdf7659.pdf.",
 "Teachers’ Retirement System of Louisiana (2026), “Return to work”, https://www.trsl.org/retirees/return_to_work" + ACC + ".",
 "Teachers Retirement System of Georgia (2026), “SB 150 FAQs”, https://www.trsga.com/employer/hiring-trs-retirees/sb-150-faqs/" + ACC + ".",
 "Teaching Council of Aotearoa New Zealand (2025), “Introducing Kia Maia”, 10 December 2025, https://teachingcouncil.nz/en/news-and-advocacy/news-and-articles/introducing-kia-maia" + ACC + ".",
 "Teaching Council of Aotearoa New Zealand (2026), “Renew after time away”, https://teachingcouncil.nz/en/maintain-my-practising-certificate/manage-my-practising-certificate/renew-after-time-away" + ACC + ".",
 "Teaching Council of Aotearoa New Zealand (unpublished), “Kia Maia users by sex, sector and age, January-October 2026”.",
 "Tweede Kamer (2020), Kamerstuk 35300-VIII, nr. 212, The Hague, https://zoek.officielebekendmakingen.nl/kst-35300-VIII-212.html.",
 "Victorian Government (2023), “Ensuring a strong, sustainable and supported school workforce”, https://www.vic.gov.au/ensuring-strong-sustainable-and-supported-school-workforce" + ACC + ".",
 "Victorian Government (2026), “Teacher Re-Engagement Initiative”, https://www.vic.gov.au/teacher-re-engagement-initiative" + ACC + ".",
 "Virginia Retirement System (2023), *Report on Retirees Returning to Work in Critical Shortage Positions*, RD577, Richmond, https://rga.lis.virginia.gov/Published/2023/RD577/PDF.",
 "ZNS Bahamas (2026), “Teacher recruitment update”, 23 September 2026, https://znsbahamas.com/teacher-recruitment-update/" + ACC + ".",
]
