# Section 3, version 4. Register of the authors' Section 2; each policy
# described in full once; no colons or dashes in the prose.
import section3_v3 as _v3

B = []
def h2(t): B.append(("h2", t))
def h3(t): B.append(("h3", t))
def p(t): B.append(("p", t))
def box(title, paras): B.append(("box", title, paras))
def src(t): return [(t, "src")]

# ======================================================================
p("Governments have tried to bring former teachers back into schools "
  "through a wide variety of measures, which range from changes to the "
  "pension rules that keep retired teachers out of the classroom to "
  "personal letters, refresher courses and new roles as tutors or mentors. "
  "This section reviews 30 of these policies, adopted in 18 countries and "
  "economies between 1996 and 2026. They were identified through a review "
  "of legal texts, official documents, parliamentary records and "
  "evaluations, complemented with reputable press reports where no "
  "official source exists and with information provided by officials in "
  "Lower Saxony (Germany), Quebec (Canada) and New Zealand. The review does "
  "not claim to be exhaustive, but it covers the main instruments that "
  "education systems have used and includes the few policies whose results "
  "have been evaluated.")

p("The policies are classified according to the main instrument they use. "
  "Financial incentives alter the economic return to teaching for those "
  "who come back, either through the rules that govern the combination of "
  "a pension with a salary or through direct payments to returners and "
  "schools. Information and nudges make former teachers aware of the "
  "options available to them or prompt them to consider a return, and "
  "support and training reduce the practical cost of returning through "
  "refresher courses, supervised placements and induction. Flexible "
  "positions offer roles other than a full-time teaching post, such as "
  "relief teaching, tutoring and mentoring, while flexible re-certification "
  "lowers the regulatory requirements that a former teacher must meet to "
  "teach again. Many policies combine several of these instruments, and "
  "each of them is presented under the instrument that defines it best, "
  "with its secondary instruments indicated in Table 2.")

p("Section 3.1 provides an overview of the objectives, target groups, "
  "duration and available evidence of the policies reviewed. Sections 3.2 "
  "to 3.6 then examine each instrument in turn, describing how the policies "
  "work and what is known about their results, with selected country cases "
  "presented in boxes. Box 13, at the end of the section, brings together "
  "what each instrument suggests for the design of re-entry policies, "
  "following the structure of Box 1.")

# ======================================================================
h2("3.1 Overview of the policies reviewed")

h3("Objectives")

p("Most of the policies reviewed were introduced to respond to teacher "
  "shortages, and in particular to shortages concentrated in specific "
  "subjects, regions or types of school. Georgia (United States), for "
  "example, allowed teachers who had retired after a full career to return "
  "full-time without losing their pension, but only to teach the subjects "
  "of highest need in their region, while Portugal allowed schools to hire "
  "recently retired teachers only for posts in shortage subjects or in "
  "under-staffed schools. China pursues the same aim through a different "
  "channel, since its Silver-Age Lecturing Plan sends retired principals "
  "and senior teachers to rural schools where vacancies are hardest to "
  "fill.")

p("The COVID-19 pandemic gave a strong impulse to these policies, as the "
  "absence of serving teachers multiplied the need for substitutes at a "
  "time when few were available. In autumn 2020, Quebec (Canada) began to "
  "pay retired supply teachers according to their experience instead of a "
  "flat daily rate, and Ontario (Canada) temporarily allowed retired "
  "teachers to work more days a year without losing their pension. In 2021 "
  "Ireland waived, for a limited number of working days each year, the "
  "reduction that public-service pensions normally suffer when a retiree "
  "returns to paid work, and in December of that year the Department for "
  "Education in England called on recently retired teachers and career "
  "changers to cover the absences caused by the Omicron wave, even if only "
  "for one day a week (Department for Education, 2021).")

p("A smaller group of policies pursues a different objective, which is to "
  "make use of the experience of former teachers in roles that serving "
  "teachers rarely have the time to perform. In Aurora, Colorado (United "
  "States), recently retired teachers were paid to mentor new teachers in "
  "high-poverty elementary schools, and in several US school districts "
  "retired teachers have tutored young pupils who were falling behind in "
  "mathematics or reading. The University of Zaragoza (Spain) invited "
  "retired teachers to mentor student teachers, and the Chinese programme "
  "mentioned above also asks retired teachers to coach the young teachers "
  "of the schools that receive them. Singapore pursues a related aim, since "
  "its adjunct teaching programme keeps teachers who resign in contact with "
  "schools by allowing them to work on short and flexible appointments.")

h3("Instruments and target groups")

p("Financial incentives are the main instrument of 12 of the 30 policies, "
  "and in most cases they take the form of changes to the rules on "
  "combining a pension with a salary, such as the Irish waiver or the "
  "decision of Lower Saxony (Germany) to abolish the earnings ceiling for "
  "retired teachers who have reached the statutory retirement age. Seven "
  "policies offer flexible positions, from the adjunct teachers whom "
  "schools in Singapore can hire for short periods to the retired teachers "
  "who serve for at least a school year in Chinese rural schools. Five "
  "policies rely on information and nudges, such as the personal letter "
  "that the Minister of Education of Lower Saxony sent to every teacher "
  "about to retire to explain how to continue teaching, or the calls that "
  "the education department of New South Wales (Australia) made to teachers "
  "who had left its schools in the previous five years. Four policies "
  "provide support and training, as in Victoria (Australia), which pays "
  "former teachers to spend several weeks in a school before they apply for "
  "a post, and the remaining two make re-certification more flexible, as "
  "New Zealand did when it allowed returners with a job offer to replace a "
  "refresher course with a plan agreed with the principal of their new "
  "school.")

p("The policies target the three profiles of former teachers unevenly "
  "(Table 2). Of the 30 policies, 19 are addressed to retired teachers "
  "only, 7 to switchers and leavers, and 4 are open to all former teachers. "
  "Several features of retired teachers account for this prominence. They "
  "are easy to identify through pension records, they are fully qualified "
  "and many retire before they wish to stop working altogether. Moreover, "
  "as discussed in Section 2, the main obstacle to their return lies in a "
  "rule that governments control directly, the reduction or suspension of "
  "the pension when a retiree takes paid work in the public sector. "
  "Changing that rule requires no new programme and has a limited cost, "
  "which explains why it is the most frequent policy in the review. "
  "Switchers and leavers, who represent the majority of former teachers "
  "below retirement age, are the target of fewer and smaller programmes, "
  "most of them focused on support and training.")

B.append(("cap", "Table 2. Policies to re-attract former teachers, by main "
          "instrument"))
B.append(("sub", "Country or economy, policy and period, target group, "
          "instruments used and scale of implementation"))
B.append(("table", "T2"))
B.append(("src", "Note: ● main instrument; ○ secondary instrument. Fin. "
          "financial incentives; Inf. information and nudges; Sup. support "
          "and training; Pos. flexible positions; Rec. flexible "
          "re-certification. Target R refers to retired teachers, S/L "
          "to switchers and leavers and All to the three profiles. Scale "
          "refers to the level of government or institution that runs the "
          "policy. AARP Foundation Experience Corps recruits adults aged 50 "
          "and over, among them former teachers."))
B.append(("src", "Source: Legal texts, official documents, parliamentary "
          "records and evaluations cited in Section 3, verified in "
          "October 2026."))

h3("Duration and take-up")

p("Most of the policies reviewed are short-term remedies, designed to fill "
  "vacancies quickly in the places where shortages are most acute, and "
  "several were enacted with an end date and later renewed one period at a "
  "time. The Irish waiver, introduced in 2021, has been extended twice and "
  "now runs until the end of 2027, and Georgia replaced its return-to-work "
  "law when it expired in 2026 with a new one that will expire in 2030. "
  "Quebec has never made its incentives permanent and renegotiates them "
  "every school year with the teacher unions. Other policies were reversed "
  "after a short period. The Ontario Teachers' Federation, which "
  "co-sponsors the teachers' pension plan, declined in 2024 to extend the "
  "higher limit on working days, and in September 2026 Portugal repealed "
  "its programme for hiring retired teachers, two years after creating it, "
  "on the grounds that it was no longer justified (Government of Portugal, "
  "2026).")

p("Where take-up is reported, it is small relative to the size of the "
  "teaching workforce. In Germany, a survey of the federal states found "
  "that more than 5 000 retired teachers had stayed on in schools or "
  "returned to them by 2023, under 1% of the almost 800 000 teachers in the "
  "country (Kuhn, 2023). In Georgia, the retirees who returned under the "
  "state's law also represented under 1% of its teachers (Georgia "
  "Department of Audits and Accounts, 2025), and in Portugal only 55 "
  "retired teachers were validated for the 200 places offered in the first "
  "round of the programme (Observador, 2024).")

p("These figures should nonetheless be read in the light of the large "
  "number of teachers who return without the help of any specific "
  "programme. In England, returners accounted for 17 740 full-time "
  "equivalent qualified teachers entering state schools in 2025/26, which "
  "represents 43.3% of all qualified entrants, up from 39.6% in 2023/24, "
  "and exceeds the 16 300 newly qualified teachers who started that year "
  "(Department for Education, 2026a). In Sweden, about 3% of the teaching "
  "workforce returned to the profession in 2019 (Skolverket, 2020). The "
  "number of former teachers who return thus appears to depend at least as "
  "much on the conditions of the profession as on any of the instruments "
  "reviewed in this section.")

h3("Available evidence")

p("Evidence on the effectiveness of these policies is scarce. Only 10 of "
  "the 30 policies have been the subject of some form of evaluation, which "
  "ranges from audits and descriptive studies of administrative data to "
  "three randomised controlled trials (Table 3). The three trials concern "
  "retired teachers working as mentors of new teachers and as tutors of "
  "young pupils in mathematics and reading, and they provide the strongest "
  "evidence in this review. The official reviews of re-entry programmes in "
  "England, the Netherlands and Sweden, presented in Sections 3.2 and 3.4, "
  "reached less encouraging conclusions. In England interest rarely turned "
  "into actual returns, in the Netherlands most returners would have been "
  "hired in any case, and in Sweden the course offered to returners did not "
  "reach its target group. The studies of the rules on combining a pension "
  "with a salary in several US states describe how many retirees returned "
  "and where they went, but cannot identify the effect of these rules on "
  "vacancies or on pupils' learning.")

p("The retention of returners once they are back in school is almost "
  "never measured, and Georgia, where 43% of the retirees hired in 2023 "
  "were still teaching two years later, is a rare exception. In most "
  "systems the available data do not allow returners to be linked to the "
  "policy that brought them back, and some systems lack the unique teacher "
  "identifier that would be needed to follow individual careers over "
  "time.")

B.append(("cap", "Table 3. Evaluations of policies to re-attract former "
          "teachers"))
B.append(("sub", "Type of evidence, data and main results, by instrument"))
B.append(("table", "T3"))
B.append(("src", "Note: Effect sizes are standardised mean differences in "
          "pupils' test scores between the treatment and control groups."))
B.append(("src", "Source: Georgia Department of Audits and Accounts (2025), "
          "*Retired Teachers Return to Work*; Jarrold-Grapes and Mahler "
          "(2024); Virginia Retirement System (2023), *Report on Retirees "
          "Returning to Work in Critical Shortage Positions*; Tweede Kamer "
          "(2020), Kamerstuk 35300-VIII, nr. 212; Resch (2025); Buchanan et "
          "al. (2018), *Evaluation of the Return to Teaching Pilot "
          "Programme*; Skolverket (2020); DeCesare et al. (2017); Gersten et "
          "al. (2015); Morrow-Howell et al. (2009)."))

# ======================================================================
h2("3.2 Financial incentives")

p("For retired teachers, the decision to return to the classroom depends "
  "less on the salary on offer than on what happens to their pension once "
  "they accept it, which is why financial incentives aimed at former "
  "teachers concentrate on this group (Box 1). The policies reviewed take "
  "two forms. The most common modifies the rules that govern the "
  "combination of a pension with a salary, so that retired teachers can "
  "work again without losing all or part of their pension, while a smaller "
  "group offers direct payments, either to the teachers who return or to "
  "the schools that hire them.")

h3("Rules on combining a pension with a salary")

p("In most public-service pension plans, a retired teacher who takes up "
  "paid work in the public sector sees the pension reduced or suspended "
  "once the pension and the new salary together exceed a given threshold, "
  "or once the number of days worked exceeds a given limit. Table 4 "
  "compares how the policies reviewed relax these rules. The simplest way "
  "of doing so, adopted in Ireland and Ontario, is to allow retirees to "
  "work a fixed number of days each year without any reduction of the "
  "pension. In Ireland, a public-service pension is reduced when the new "
  "earnings and the pension together exceed the salary that the retiree "
  "received at the time of retirement, uprated over time. Since 2021 the "
  "Department of Education has waived this reduction for the first 50 days "
  "that a retired teacher works in each calendar year, with any day worked "
  "counting as a full day regardless of the hours taught. The waiver "
  "applies only where the need for a teacher cannot practicably be met in "
  "another way and excludes retirees who take a post that extends beyond "
  "50 days, since its purpose is to provide substitutes for short absences "
  "(Department of Education, 2026).")

p("Ontario applies a similar logic to the school year. Retired teachers can "
  "work up to 50 days in each school year and keep their full pension, "
  "which is otherwise suspended from the end of the month in which the "
  "limit is exceeded. Between 2020/21 and 2022/23, the provincial "
  "government and the Ontario Teachers' Federation, which jointly sponsor "
  "the teachers' pension plan, raised this limit to 95 days, only for "
  "positions that could not be filled by other qualified teachers and with "
  "monthly reports from school boards on how retirees were used (Ontario "
  "Teachers' Federation, 2020).")

p("Other systems have raised or removed the earnings ceiling for all "
  "retired teachers. In October 2022 the parliament of Lower Saxony raised "
  "the ceiling on the combined pension and salary of retired civil-service "
  "teachers from 125% to 150% of their pensionable pay, and in October 2024 "
  "it abolished the ceiling for those who have reached the statutory "
  "retirement age, as part of the broader approach described in Box 4. In "
  "France, a retired teacher who has claimed all pensions and receives a "
  "full-rate pension can combine it with a salary without any limit, and "
  "since 2023 the new work also generates additional pension rights, while "
  "for other retirees the pension is reduced once earnings exceed a "
  "threshold (Assemblée nationale, 2026). In the United States, Michigan "
  "shortened in 2023 the waiting period after retirement from nine to six "
  "months, after which retirees can take any school post without an "
  "earnings limit (Michigan Office of Retirement Services, 2023), and New "
  "Mexico has allowed retired educators since 2022 to return 90 days after "
  "retiring with no limit on earnings. In New Mexico each return must be "
  "approved by the state's Educational Retirement Board, and the maximum "
  "period of return was extended from 36 to 60 months in 2025 (New Mexico "
  "Educational Retirement Board, 2025).")

p("Several US states have instead tied a full return, with a full salary "
  "and a full pension, to posts that are hard to fill. Georgia did so for "
  "teachers who had retired after at least 30 years of service, provided "
  "they returned full-time to one of the subjects of highest need in their "
  "region, and a state audit offers one of the few assessments of a rule of "
  "this kind (Box 2). Louisiana's Act 344 of 2026 requires retirees to wait "
  "12 months before returning and limits their earnings to 50% of their "
  "final average pay, up from 25%, except in posts certified as critical "
  "shortages, where they can earn a full salary without any reduction of "
  "the pension. To certify a shortage, the employer must have advertised "
  "the post and received fewer than three applications from qualified "
  "candidates who are not retired (Teachers' Retirement System of "
  "Louisiana, 2026). Virginia has allowed retirees to return to "
  "critical-shortage posts while keeping their pension since 2001, and "
  "retirees filled 699 such posts between 2008 and 2022. In July 2023 the "
  "state shortened the break in service required before a return from 12 "
  "to 6 months, extended the rule to specialist support posts and "
  "prolonged it until July 2028, after which the number of retirees "
  "returning between July and October rose from 18 in 2022 to 150 in 2023 "
  "(Virginia Retirement System, 2023).")

p("North Carolina has the longest record with this approach. Between 1999 "
  "and 2009, retired teachers could return to a full-time post and draw "
  "their salary and pension together, which raised their income by as much "
  "as half. The rule initially applied only to low-performing schools and "
  "was extended to all schools in 2000. About 3 500 teachers returned under "
  "it, more than half of them (54%) to their own school, and returners were "
  "more frequently employed in the poorest schools, where 30% of them "
  "worked, against 21% in the least poor quartile of schools "
  "(Jarrold-Grapes and Mahler, 2024). Portugal, by contrast, opted for a "
  "highly restrictive design. Its Decree-Law 51/2024 allowed schools to "
  "offer fixed-term contracts to teachers who had retired in the previous "
  "five years, only for posts in shortage subjects or in under-staffed "
  "schools and within an annual national quota. Returners kept their "
  "pension and received an additional payment linked to the first step of "
  "the salary scale, in proportion to their weekly hours (Government of "
  "Portugal, 2024), but most of the places offered went unfilled before "
  "the programme was repealed.")

p("The rules also differ in how they treat pension contributions, which "
  "determines both their cost for the pension system and the incentive "
  "they create to retire early. In Georgia the employer paid both the "
  "employer and the employee contributions on the salary of the returner, "
  "who earned no further pension rights, and in New Mexico, Louisiana and, "
  "since 2023, Virginia, contributions are also paid on the salary of "
  "returners without increasing their pension. Designs of this kind make "
  "the return possible while preventing retirees from accumulating "
  "additional pension entitlements at the expense of the system.")

B.append(("cap", "Table 4. Rules on combining a pension with a salary for "
          "retired teachers in selected systems"))
B.append(("sub", "Eligibility, limits on work or earnings, posts covered "
          "and treatment of pension contributions"))
B.append(("table", "T4"))
B.append(("src", "Note: .. information not available. Rules as in force in "
          "October 2026 or, for policies that have ended, during their last "
          "year of application."))
B.append(("src", "Source: Department of Education (2026), Circular "
          "0017/2026; Ontario Teachers' Federation (2020); Assemblée "
          "nationale (2026); Niedersächsischer Landtag (2024), Drucksache "
          "19/5338; Michigan Office of Retirement Services (2023); New Mexico "
          "Educational Retirement Board (2025); Teachers Retirement System of "
          "Georgia (2026); Teachers' Retirement System of Louisiana (2026); "
          "Virginia Retirement System (2023); Jarrold-Grapes and Mahler "
          "(2024); Government of Portugal (2024), Decreto-Lei n.º 51/2024."))

box("Box 2. The return of retired teachers to high-need subjects in "
    "Georgia (United States)", [
 [("Between July 2022 and June 2026, House Bill 385 allowed teachers in "
   "Georgia who had retired with at least 30 years of service, and who had "
   "been retired for at least a year, to return to a full-time classroom "
   "post and receive a full salary on top of their full pension. The post "
   "had to be in one of the subjects of highest need in their region, as "
   "determined by the regional education service agency, and the employer "
   "paid both the employer and the employee contributions to the pension "
   "fund, while the returner earned no further service credit.", "")],
 [("A state audit published in 2025 assessed how the law had been used. "
   "Between 2023 and 2025, 635 retirees returned under it, a number that "
   "rose from 241 to 428 a year and averaged about 350, under 1% of the "
   "state's teachers. Just over half of school systems (55%) used the law, "
   "64% of returners went back to the system they had retired from, and "
   "43% of those hired in 2023 were still teaching two years later. In 56% "
   "of the systems that used the law, the post had first been offered to a "
   "candidate who was not retired, and 45 of the 72 systems that did not use "
   "it reported that they would have done so had they found an eligible "
   "retiree (Georgia Department of Audits and Accounts, 2025).", "")],
 [("The law expired in June 2026 and was replaced by Senate Bill 150, "
   "which will remain in force until June 2030. Under the new law, at least "
   "half of the returner's timetable must be in a qualifying subject, such "
   "as mathematics, science, special education or career and technical "
   "education, and each school system defines its own areas of highest "
   "need on the basis of a five-year average of vacancies (Teachers "
   "Retirement System of Georgia, 2026).", "")],
 [("Strict eligibility kept the cost of the rule low, but it also limited "
   "its reach, because the retirees who qualified were few and tended to "
   "return to the systems where they used to work. By defining need at the "
   "level of each school system, the new law may bring the rule closer to "
   "the vacancies it is meant to fill.", "")],
 src("Source: Georgia Department of Audits and Accounts (2025), *Retired "
     "Teachers Return to Work*; Teachers Retirement System of Georgia "
     "(2026), “SB 150 FAQs”."),
])

h3("Direct payments to returners and schools")

p("Direct payments are less common among the policies reviewed, and most "
  "of them are made to the returners themselves. The most developed "
  "example is that of Quebec, which since 2020 has paid retired teachers "
  "who cover absences at the step of the salary scale that corresponds to "
  "their experience from the first day of work, together with a premium "
  "that has been renegotiated every year (Box 3). Payments to returners "
  "also appear as a secondary instrument in several of the policies "
  "presented in later sections, as an honorarium during a school "
  "placement, an allowance for teachers posted to remote schools or the "
  "payment of registration fees.")

p("The Netherlands chose instead to pay the schools that hired returners. "
  "Between 2017 and 2020, primary school boards could claim EUR 2 500 for "
  "each qualified teacher they hired after a break of at least a year, to "
  "cover the cost of coaching and refresher training during the first "
  "months back (Ministerie van OCW, 2017). The grant was used for 274 "
  "returners, well below the number that the budget allowed, and school "
  "boards reported to the ministry that most of these teachers would have "
  "been hired and supported without it. The ministry concluded that the "
  "grant had contributed only to a limited extent and did not extend it "
  "(Tweede Kamer, 2020). The pool of potential returners in the country "
  "remains large, with 34 000 qualified primary teachers and 64 000 "
  "secondary and vocational teachers not working in education in 2024 "
  "(DUO, 2026), but most of them already work in other parts of the public "
  "sector, such as health care (de Vries, van Klaveren and Stolp, 2025). "
  "The Dutch experience illustrates a general risk of payments to "
  "employers, which may reward hiring decisions that would have been taken "
  "in any case.")

box("Box 3. Paying retired supply teachers on their salary step in Quebec "
    "(Canada)", [
 [("Until 2020, a retired teacher who covered an absence in a Quebec "
   "public school was paid the flat daily rate for supply teaching and "
   "reached the salary scale only after 20 consecutive days in the same "
   "replacement. In September 2020, during the COVID-19 health emergency, a "
   "government decree modified the collective agreements so that teachers "
   "who had retired in the previous five years would be paid from the first "
   "day at the step of the scale that matched their experience and "
   "qualifications, while keeping their full pension and without paying "
   "further contributions. For a retiree at the top of the scale, daily pay "
   "rose from a usual maximum of about CAD 212 to about CAD 412, at an "
   "estimated cost of CAD 4 545 per retiree for each 20-day replacement "
   "(Conseil exécutif du Québec, 2020; Gouvernement du Québec, 2022).", "")],
 [("A premium of 7.89% was added from 1 October 2021. When the emergency "
   "measures ended with the 2021/22 school year, the government chose to "
   "continue the incentives through letters of agreement signed every year "
   "with each teacher union federation outside the collective agreements, "
   "and the premium has changed with each agreement. It stood at 7.89% "
   "until 2023/24, was split in 2024/25 into 7.5% on supply work and 12.5% "
   "on contracts of three months or more, and has been limited since "
   "2025/26 to 12.5% on contracts of one month or more. The original "
   "five-year limit was also lifted, and the agreement now covers any "
   "retired teacher who is legally qualified to teach, although employers "
   "must first offer the work to the qualified staff they already "
   "employ.", "")],
 [("The Ministry of Education funds the measure after the fact, on the "
   "basis of the use of retired staff that school service centres report "
   "at the end of each year, and the envelope for 2026/27 is being adjusted "
   "downwards as fewer retirees are used and the 7.5% premium has been "
   "withdrawn (Ministère de l'Éducation du Québec, 2026). About 700 "
   "retirees returned in 2020/21, more than 2 900 in 2022/23 and more than "
   "5 000 in 2024/25 (Desrosiers, 2023; Le Devoir, 2025). The measure has "
   "not been evaluated.", "")],
 [("Because the payment is made only for the days actually worked, paying "
   "returners according to their experience removed the main financial "
   "penalty of supply work at a moderate cost. Renegotiating the terms "
   "every year has kept the measure responsive to shortages, although it "
   "leaves retirees and school service centres uncertain about the "
   "conditions that will apply from one year to the next.", "")],
 src("Source: Conseil exécutif du Québec (2020), “Mémoire au Conseil des "
     "ministres”; Gouvernement du Québec (2022), “Opération main-d'œuvre”; "
     "Desrosiers (2023), “La prime de 12 000 $ boudée par des enseignants "
     "retraités”; Le Devoir (2025); Ministère de l'Éducation du Québec "
     "(2026), presentation to the OECD."),
])

h3("Implications for re-entry policies")

p("The experience with financial incentives indicates, first of all, that "
  "the conditions attached to a rule matter as much as the incentive "
  "itself. Returns to Virginia's schools in the first months of the school "
  "year multiplied by eight once the required break in service was "
  "shortened, whereas the narrow eligibility rules of Georgia and Portugal "
  "left many schools without any retiree who could fill their vacancies. "
  "Rules that allow a full return also tend to bring retirees back to the "
  "subjects and schools where they are most needed, as the cases of "
  "Georgia and North Carolina show, although most returners go back to the "
  "school or system where they used to work. These rules therefore seem to "
  "help schools keep their own experienced teachers for longer rather than "
  "attract retirees to new schools.")

p("These rules also raise concerns that governments need to weigh. When "
  "the Ontario Teachers' Federation refused to extend the higher limit on "
  "working days in 2024, it argued that more than 30 000 certified teachers "
  "were not employed by school boards and that a generous rule could "
  "encourage early retirement (Ontario Teachers' Federation, 2024). Payments "
  "to schools, as the Dutch grant showed, carry a different risk, which is "
  "to finance hires that would have taken place anyway.")

# ======================================================================
h2("3.3 Information and nudges")

p("Not every obstacle to returning is financial, and several governments "
  "have tried instead to inform former teachers of the options open to "
  "them, or simply to ask them to consider a return, through letters, "
  "telephone calls, advisers and information sessions. These instruments "
  "are inexpensive and respond to a barrier identified in Section 2, since "
  "many former teachers would consider returning but are not asked, do not "
  "know how to do so or expect the process to be burdensome. The letter "
  "sent by the Minister of Education of Lower Saxony in 2023 acknowledged "
  "this explicitly, noting that many teachers about to retire would be "
  "willing to teach a few hours a week but were deterred by the "
  "bureaucracy involved (Niedersächsisches Kultusministerium, 2023).")

h3("Outreach to retired teachers")

p("In December 2022, the education directorate of Vienna (Austria) "
  "contacted nearly 300 retired teachers to ask them to return to school, "
  "and only three did so. At the end of February 2023 the directorate "
  "changed its approach and asked all school principals to consider which "
  "of their teachers could be kept on beyond the age of 65 (ORF Wien, "
  "2023). Other Austrian provinces opted for different channels, with "
  "Salzburg writing to all retired teachers up to the age of 67 and "
  "Vorarlberg sending information on re-entry together with the forms that "
  "teachers use to apply for their pension (ORF, 2023). Across the country, "
  "only 42 teachers working in the schools run by the provinces in "
  "autumn 2022 had been hired at the age of 63 or later (Austrian "
  "Parliament, 2023). A study based on interviews with retired teachers "
  "who had returned to Austrian schools found that their terms had been "
  "negotiated individually with school principals and that none of them "
  "would repeat the experience (Resch, 2025). The Austrian case suggests "
  "that the timing of the contact and the person who makes it can matter "
  "as much as the message itself.")

p("Lower Saxony reached the same conclusion as Vienna and directs its "
  "outreach to teachers who are about to retire, combining a personal "
  "letter from the minister with financial and administrative changes "
  "(Box 4). Quebec has also relied on letters, which the minister sent in "
  "June 2023 to ask retired teachers to return for one or two days a week "
  "or full-time, and again in August 2025, when more than 5 000 retirees "
  "were already working in schools under the incentives described in "
  "Box 3 (Le Devoir, 2025).")

box("Box 4. A combined approach for teachers approaching retirement in "
    "Lower Saxony (Germany)", [
 [("Lower Saxony has combined financial, informational and administrative "
   "measures aimed at teachers who are about to retire. On the financial "
   "side, a retired civil-service teacher working for the state used to "
   "have the pension reduced once the pension and the new salary together "
   "exceeded 125% of the pensionable pay. In October 2022 the state "
   "parliament raised this ceiling to 150% for two years, which allowed a "
   "pensioner to teach nine to ten lessons a week on average without any "
   "reduction, and in October 2024 it abolished the ceiling for teachers "
   "who have reached the statutory retirement age, while those who retire "
   "early remain subject to it (Niedersächsischer Landtag, 2024).", "")],
 [("Alongside these changes, the Minister of Education wrote on "
   "1 November 2023 to every teacher about to retire, whether a civil "
   "servant or a salaried employee, to explain how to continue teaching. A "
   "civil servant can ask to postpone retirement by up to three years, and "
   "any teacher can be re-employed on a fixed-term contract immediately "
   "after retiring while drawing the pension. The letter was addressed to "
   "teachers approaching retirement partly because the ministry no longer "
   "held the personnel files of those who had already retired, and school "
   "principals were also asked to approach these teachers in person "
   "(Niedersächsisches Kultusministerium, 2023).", "")],
 [("The procedure itself was also simplified. A teacher who continues at "
   "the same school immediately after retiring does not need to apply "
   "through the online recruitment system or to provide a new police "
   "certificate, and contact persons in each of the four regional school "
   "authorities advise retirees and handle the procedure. The number of "
   "teachers past retirement age working on fixed-term contracts rose from "
   "229 in 2020 to 437 in 2024 (Niedersächsischer Landtag, 2025).", "")],
 [("According to the ministry, the first contact takes place about six "
   "months before retirement, and most returners stay at or return to the "
   "school where they last taught, usually part-time and in a specific "
   "subject such as mathematics, and rarely as class teachers or formal "
   "mentors. The funding for these posts must be additional, in order that "
   "retirees do not take positions from young teachers. No formal "
   "evaluation has been carried out, and the state has no unique teacher "
   "identifier with which individual careers could be followed.", "")],
 [("Removing the financial penalty was only one part of the package. A "
   "personal letter before retirement, contact through the principal and a "
   "simpler procedure turn the decision to keep teaching into a small step, "
   "instead of a new job application.", "")],
 src("Source: Niedersächsischer Landtag (2024), Drucksache 19/5338; "
     "Niedersächsischer Landtag (2025), Drucksache 19/8802; "
     "Niedersächsisches Kultusministerium (2023), “Schreiben an angehende "
     "Pensionärinnen und Pensionäre”; information provided by the Lower "
     "Saxony Ministry of Education."),
])

h3("Outreach to recent leavers and licence holders")

p("Outreach has also been directed at teachers who left the profession "
  "more recently, particularly where it can be accompanied by practical "
  "help and by better working conditions. New South Wales offers the "
  "clearest example of a campaign of this kind, which the education "
  "department launched in November 2023, shortly after the state had "
  "approved the largest pay rise for its teachers in decades (Box 5). "
  "England has relied instead on a permanent advisory service, through "
  "which former teachers can request an adviser who supports them "
  "individually with applications, interviews, refresher courses and "
  "vacancies. The plan published by the Department for Education in "
  "February 2026 to recruit 6 500 additional teachers includes this service "
  "among its measures, together with a new step-by-step guide for "
  "returners (Department for Education, 2026b).")

p("Japan faces a different situation, since its open licensing system has "
  "produced a large pool of people who hold a teaching licence but have "
  "never taught or have long been away from schools. Most boards of "
  "education now organise information sessions and training for them, with "
  "the aim of bringing them into temporary and part-time posts that do not "
  "require passing the competitive recruitment examination (Box 6).")

box("Box 5. Contacting teachers who recently left the profession in "
    "New South Wales (Australia)", [
 [("From November 2023, the Department of Education of New South Wales "
   "contacted more than 1 500 teachers who had left its schools in the "
   "previous five years and asked them to consider returning. Those "
   "interested were offered a simpler re-employment process and help with "
   "their accreditation, their approval to teach and the "
   "working-with-children check, before being placed in casual or temporary "
   "work, with permanent posts and small-group tutoring roles also "
   "available.", "")],
 [("By May 2024, more than 260 former teachers had expressed interest and "
   "145 had been matched with schools, about 60% of them returning from "
   "retirement (NSW Government, 2024). The campaign followed the largest "
   "pay rise for the state's teachers in decades, effective from "
   "October 2023, which raised the starting salary from AUD 75 791 to "
   "AUD 85 000 and was accompanied by a reduction in administrative "
   "workload (NSW Government, 2023). Teacher vacancies in the state fell "
   "from a peak of 3 311 in 2022 to 1 294 in February 2025 (NSW Government, "
   "2025), although the contribution of returners to that fall is not "
   "known.", "")],
 [("Recent leavers can be identified from the employer's own records, and "
   "in New South Wales a direct call accompanied by practical help "
   "converted about one in ten of the teachers contacted. Because the call "
   "coincided with better pay and a lighter administrative load, its "
   "results cannot be separated from those of the wider improvement in "
   "working conditions, which is consistent with the weight that Section 2 "
   "gives to those conditions in the decision to return.", "")],
 src("Source: NSW Government (2023), “NSW teachers to receive largest pay "
     "rise in decades”; NSW Government (2024), “Retired teachers return to "
     "classrooms”; NSW Government (2025), “Teacher vacancies drop under "
     "Minns Labor Government”."),
])

box("Box 6. Information sessions for teaching licence holders in Japan", [
 [("In Japan, students at any accredited university can obtain a teaching "
   "licence after a practicum of three to four weeks, and many licence "
   "holders never teach or leave the profession early, which has produced "
   "a large pool of potential teachers. On 1 May 2025, schools were short of "
   "3 827 teachers, against 2 065 in 2021 (MEXT, 2026). The Ministry of "
   "Education, Culture, Sports, Science and Technology (MEXT) encourages "
   "boards of education to bring licence holders into schools and funded "
   "such initiatives with JPY 500 million in 2024. In 2023, 50 of the 68 "
   "prefectural and city boards of education organised sessions or "
   "training for licence holders who were not teaching (MEXT, 2024).", "")],
 [("Results are reported only for a few boards. In Saitama, seven seminars "
   "held in 2023 attracted 226 participants, of whom 122 registered for "
   "temporary or part-time posts and 53 had been appointed by April 2024, "
   "while in Osaka 69 people took part in 2022 and 19 were appointed (MEXT, "
   "2024).", "")],
 [("The session organised by the Miyazaki Prefectural Board of Education "
   "on 15 November 2025 illustrates what licence holders are told. It "
   "described a teacher's working day today, team-based pupil guidance, "
   "the rest days introduced in club activities and the professional "
   "development on offer, and presented the posts available without "
   "passing the competitive recruitment examination. Temporary full-time "
   "teachers start at JPY 241 900 a month, part-time teachers work up to "
   "680 hours a year at JPY 2 860 an hour, and school support staff work up "
   "to 800 hours a year at about JPY 1 000 an hour. The session ended with "
   "individual consultations and the registration of participants as "
   "temporary teachers, in order that the prefecture can call on them when "
   "a vacancy appears (Miyazaki Prefectural Board of Education, 2025).", "")],
 [("These sessions are built around the doubts that keep licence holders "
   "away from schools, such as the fear of being out of date, the workload "
   "and the lack of readiness for a permanent post, and they bring part of "
   "this pool into schools through flexible posts without any financial "
   "incentive. Research on these initiatives in Japan is still almost "
   "non-existent.", "")],
 src("Source: MEXT (2024), “Case collection on training for "
     "teaching-licence holders not currently teaching”; MEXT (2026), "
     "“Results of the survey on the shortage of teachers, fiscal year "
     "2025”; Miyazaki Prefectural Board of Education (2025), “Information "
     "session on the appeal of teaching”, translated by M. Kikuchihara."),
])

h3("Implications for re-entry policies")

p("Although none of these initiatives has been formally evaluated, and in "
  "most cases the available data do not link returners to the contact "
  "that prompted their return, the figures available suggest that letters "
  "sent after retirement obtain a very low response. Contact made before "
  "retirement, through the school principal or together with help with the "
  "procedures, appears more promising, as does outreach to teachers who "
  "left recently and can be traced through the employer's records. "
  "Information therefore seems most useful when it reaches former teachers "
  "while their skills and their links with schools are still intact, and "
  "when it comes with measures that make the return easier.")

# ======================================================================
h2("3.4 Support and training")

p("Former teachers who have been away for some years often doubt that "
  "they are still up to date with curricula, assessment and classroom "
  "practice, and schools may share those doubts when they consider their "
  "applications. Refresher courses, supervised time in classrooms, coaching "
  "and induction seek to reduce this practical cost of returning. These "
  "programmes are addressed mainly to switchers and leavers, who have "
  "usually been away from schools for longer than retired teachers, and "
  "the evidence on their results is the least encouraging of the five "
  "instruments.")

h3("Refresher programmes")

p("England has the most extensive experience with refresher programmes. "
  "Its Return to Teaching pilot, which in 2016 funded partnerships of "
  "schools to support qualified teachers returning to secondary subjects in "
  "shortage, attracted far more interest than it could convert into posts, "
  "and its evaluation remains the most detailed assessment of a re-entry "
  "programme available (Box 7). The Department for Education followed it "
  "with the Returners Engagement Programme, which between November 2016 and "
  "March 2018 funded lead schools in two regions to offer returners in "
  "mathematics, physics and modern foreign languages a course of two to "
  "four weeks that included teaching practice. Support was tied to "
  "identified vacancies, schools received GBP 1 500 for each returner they "
  "employed and returners could claim up to GBP 600 to cover childcare or "
  "travel, but the programme was withdrawn without being evaluated "
  "(Department for Education, 2016).")

p("In October 2018 Sweden's National Agency for Education launched a free "
  "online course for teachers and preschool teachers returning to the "
  "profession, which covered the changes in curricula, legislation and "
  "guidelines introduced since the reforms of 2010 and 2011. By April 2020, "
  "1 018 people had registered, 175 had completed at least one module and "
  "only 38 had completed the whole course. About one-third of the "
  "respondents to a follow-up survey were actually returning teachers, and "
  "none of those already employed had been given working time, a mentor or "
  "a study group to take the course. With a cost of SEK 17 268 per "
  "participant, against SEK 863 for a comparable online course, the agency "
  "concluded that the course had not reached its target group (Skolverket, "
  "2020).")

box("Box 7. Evaluation of the Return to Teaching pilot in England "
    "(United Kingdom)", [
 [("Between January and October 2016, the Department for Education funded "
   "60 partnerships of schools to support qualified teachers returning to "
   "secondary subjects in shortage. The support was free for the returner "
   "and covered subject knowledge, updates on assessment and behaviour "
   "management, classroom experience and mentoring. The pilot attracted "
   "5 729 registrations, well above its target of 3 000, but only 354 "
   "registrants received support, and by November 2016, 62 of them were "
   "teaching in a state school and 27 held a permanent post in the targeted "
   "subjects. The cost per additional returner was about GBP 37 400, close "
   "to the cost of training a new teacher, and the independent evaluation "
   "judged the pilot unlikely to represent good value for money (Buchanan "
   "et al., 2018).", "")],
 [("The evaluation identified several reasons for this low conversion. "
   "Support began in January, when few posts for the following September "
   "remained open, and many schools hesitated to give returners teaching "
   "practice, citing the need to establish their quality and the risk of "
   "disrupting lessons, with the result that only 44% of returners felt "
   "that their needs had been met. Half of the returners and schools "
   "interviewed also reported that returners were looking for part-time "
   "work, which few schools offered, and returners named their lack of "
   "recent experience, the workload, the lack of flexible posts and their "
   "own confidence as the main barriers to their return.", "")],
 [("Interest in returning was not the binding constraint in this pilot, "
   "since registrations far exceeded the target and most of the losses "
   "occurred at the later stages, when support had to turn into a post.", "")],
 src("Source: Buchanan, E. et al. (2018), *Evaluation of the Return to "
     "Teaching Pilot Programme*."),
])

h3("Induction and placements in schools")

p("Programmes that build the return into the school itself appear more "
  "promising, although none of them has been evaluated. In the canton of "
  "Zurich (Switzerland), teachers who return after eight years or more "
  "away are entitled during their first year back to the same induction "
  "programme as new teachers, free of charge, including up to 25 hours of "
  "mentoring by a trained colleague in their own school, group supervision "
  "and subject coaching. Returners can also obtain an individual "
  "assessment of the preparation they need, of which the canton pays the "
  "first hour and the teacher the rest, although the university of teacher "
  "education that provides this assessment was not offering counselling to "
  "returners in October 2026 (PH Zürich, 2026). Victoria goes further and "
  "pays former teachers to spend several weeks in a school, observing and "
  "teaching with the guidance of serving staff, before they apply for a "
  "post (Box 8).")

box("Box 8. Paid school placements for former teachers in Victoria "
    "(Australia)", [
 [("Victoria's Teacher Re-Engagement Initiative, launched in late 2022, "
   "offers registered teachers who have been away from teaching for at "
   "least 12 months a paid placement of up to 40 days in a government "
   "school. During the placement, participants observe classes and school "
   "routines and are mentored by serving staff, before they apply for a "
   "post. A central team matches participants with schools according to "
   "their subject, experience, location and availability, and records at "
   "the end of the placement whether the participant has returned to "
   "teaching.", "")],
 [("The initiative attracted more than 1 100 expressions of interest and "
   "received AUD 12 million in the 2023/24 state budget (Victorian "
   "Government, 2023). It is now funded by the schools that host a "
   "returner, at a cost of AUD 330 a day that covers the participant's "
   "honorarium and the administrative costs (Victorian Government, 2026). "
   "No figures have been published on the number of participants who went "
   "on to teach.", "")],
 [("A supervised placement responds at the same time to the returner's "
   "lack of confidence and to the school's uncertainty about the returner, "
   "the two obstacles identified by the evaluation of the English pilot "
   "(Box 7). Shifting the cost of the placement to schools, however, may "
   "limit its use to those that can afford it.", "")],
 src("Source: Victorian Government (2023), “Ensuring a strong, sustainable "
     "and supported school workforce”; Victorian Government (2026), "
     "“Teacher Re-Engagement Initiative”."),
])

h3("Implications for re-entry policies")

p("No causal evaluation of refresher or re-entry support has been found, "
  "and the retention of returners after the support ended has not been "
  "measured in any programme. The English and Swedish experiences "
  "indicate that support detached from schools and from "
  "vacancies attracts interest but produces few returns, whereas the "
  "programmes of Zurich and Victoria place the returner in a school from "
  "the start. Support of this kind is likely to convert better when it "
  "follows the recruitment calendar, is tied to real posts and includes "
  "time in front of a class, and when schools are willing to offer the "
  "part-time positions that many returners want.")

# ======================================================================
h2("3.5 Flexible positions")

p("Many former teachers would come back to schools, but not to a "
  "full-time teaching post, and several systems have therefore created "
  "other roles for them, such as relief and adjunct teaching, tutoring and "
  "mentoring. As discussed in Section 2, leavers with care "
  "responsibilities and retirees often prefer to work only part of the "
  "week, and half of the returners and schools interviewed in the "
  "evaluation of the English pilot reported a demand for part-time work "
  "that few schools were able to meet (Buchanan et al., 2018). Flexible "
  "roles also allow education systems to use the experience of former "
  "teachers where it is most valuable.")

h3("Pools of flexible teachers")

p("The simplest version of this instrument is a standing pool of former "
  "teachers whom schools can call on when they need them. Singapore has run "
  "such a programme since 2004 (Box 9). In July 2026 the Bahamas announced "
  "a similar reserve of former teachers, retirees and recent graduates, "
  "built on its existing platform for supply teachers, as part of a "
  "recruitment drive to fill about 300 vacancies in 162 public schools "
  "spread over 24 islands. A task force of several government agencies "
  "checks the records and accreditation of candidates to allow them to "
  "start quickly, and by September 2026 more than 100 teachers had been "
  "recruited through the drive and about 100 more were being vetted "
  "(Ministry of Education of The Bahamas, 2026; ZNS Bahamas, 2026). The "
  "rules on combining a pension with a salary described in Section 3.2, "
  "such as those of Ireland and Ontario, also create in practice a pool of "
  "retired substitutes.")

box("Box 9. A standing pool of adjunct teachers in Singapore", [
 [("Singapore's Ministry of Education launched an adjunct teachers "
   "programme in 2004 to attract trained former teachers back to the "
   "profession on more flexible terms. Under the current Flexi-Adjunct "
   "Teaching Scheme, former teachers register on a ministry portal for three "
   "years, and schools contact them directly for appointments of one day to "
   "ten weeks, either for teaching alone or for teaching combined with other "
   "duties agreed with the school. Adjunct teachers are paid by the hour, at "
   "rates that depend on their experience, and earn leave once they have "
   "accumulated 90 days of service, while former teachers of the ministry "
   "must have performed well in their last three years of service to join "
   "(Ministry of Education Singapore, 2026a). A companion programme offers "
   "former ministry teachers contracts of one to one and a half years, "
   "full-time or part-time (Ministry of Education Singapore, 2026b).", "")],
 [("Between 2022 and 2024, about 220 teachers a year joined the programme "
   "within 12 months of leaving the service. In the same period, the annual "
   "resignation rate of teachers was 2.4%, or 1.7% if those who joined the "
   "programme are excluded (Ministry of Education Singapore, 2025a; 2025b). "
   "Pay at the highest rate is below 60% of the median pay package of a "
   "classroom teacher (Ministry of Education Singapore, 2024).", "")],
 [("The programme keeps the system in contact with teachers at the moment "
   "they leave, before their skills and their links with schools fade, and "
   "allows those who leave for family or other reasons to keep a foot in "
   "the profession on terms they choose.", "")],
 src("Source: Ministry of Education Singapore (2024; 2025a; 2025b), "
     "parliamentary replies; Ministry of Education Singapore (2026a), "
     "“Flexi-Adjunct Teaching Scheme”; Ministry of Education Singapore "
     "(2026b), “Contract Adjunct Teaching Scheme”."),
])

h3("Placements in schools with staffing difficulties")

p("China's Silver-Age Lecturing Plan is the largest programme in this "
  "review and the only one that sends returners to schools far from where "
  "they used to work (Box 10). It also gives them an explicit role in the "
  "development of the young teachers of the schools that receive them, "
  "which brings it close to the mentoring roles discussed below.")

box("Box 10. Retired teachers in rural schools in China", [
 [("China's Silver-Age Lecturing Plan was launched in 2018 by the "
   "Ministries of Education and Finance. It recruits retired principals, "
   "teaching researchers and senior teachers, generally aged 65 or under, to "
   "serve for at least a school year in rural primary and lower secondary "
   "schools of poor, ethnic minority and border counties, and returning to "
   "one's own former school is not allowed. Participants teach classes, "
   "observe lessons and give demonstration lessons, coach the young "
   "teachers of the school and help with its management, and since 2024 "
   "retired principals may serve as deputy heads. They keep their pension "
   "and receive CNY 20 000 a year to cover living costs, travel and "
   "insurance, an amount paid by the central government in western "
   "provinces, shared between central and provincial governments in "
   "central provinces and paid by the provinces themselves in the east "
   "(Ministry of Education and Ministry of Finance of the People's Republic "
   "of China, 2018).", "")],
 [("The first plan set a target of 10 000 places for the period 2018 to "
   "2020, and more than 20 000 retired teachers had been recruited to "
   "primary and secondary schools by mid-2023 (Ministry of Education of the "
   "People's Republic of China, 2023). Recent annual rounds have planned "
   "between 6 000 and 7 000 places. The 2026 round places the coaching of "
   "young teachers at the centre of the role and introduces an assessment "
   "by the host school at the end of each placement (Ministry of Education "
   "of the People's Republic of China, 2026). No independent evaluation has "
   "been published.", "")],
 [("The plan uses retired teachers above all to transfer experience to "
   "schools that struggle to attract and develop teachers, which is the use "
   "of former teachers that the evidence on mentoring and peer learning "
   "reviewed in Section 2 supports most clearly.", "")],
 src("Source: Ministry of Education and Ministry of Finance of the People's "
     "Republic of China (2018), Jiaoshi [2018] No. 7; Ministry of Education "
     "of the People's Republic of China (2023; 2026)."),
])

h3("Mentoring and tutoring")

p("Mentoring and tutoring by retired teachers are the uses of former "
  "teachers that have been tested most rigorously. Three randomised trials "
  "in the United States, presented in Box 11, found positive effects on "
  "pupils' learning, which were small in the case of retired teachers "
  "mentoring new teachers and larger in the case of tutoring for pupils "
  "who were falling behind. These results are consistent with the broader "
  "experimental evidence on tutoring cited in Section 1 (Nickow, "
  "Oreopoulos and Quan, 2024), and suggest that tutoring is one of the most "
  "productive uses of former teachers who do not wish to return to a full "
  "teaching post. Smaller initiatives point in the same direction. In 2018, "
  "ten retired early childhood and primary teachers mentored 57 student "
  "teachers at the University of Zaragoza in the final years of their "
  "degree, meeting each group three times to discuss the profession, "
  "further training and the teaching career, and 56% of the students who "
  "answered a survey said that the sessions had helped them to orient their "
  "careers (Lizalde Gil and Cortés Pascual, 2019).")

box("Box 11. Experimental evidence on retired teachers as mentors and "
    "tutors in the United States", [
 [("Mentoring new teachers. ", "b"), ("In 2013/14 and 2014/15, recently "
   "retired teachers and principals mentored teachers in their first three "
   "years in 11 high-poverty elementary schools of Aurora, Colorado. "
   "Mentors were paid USD 41 an hour and met each new teacher for about an "
   "hour a week over two years. A randomised trial of 77 teachers compared "
   "them with the usual support of the district, provided by a colleague "
   "who received a small stipend. Pupils of mentored teachers gained 0.064 "
   "standard deviations in mathematics after the first year, about one "
   "month of learning, and the effect was of similar size after the second "
   "year but no longer statistically significant. The trial found no effect "
   "on reading or on the retention of the new teachers (DeCesare et al., "
   "2017).", "")],
 [("Tutoring in mathematics. ", "b"), ("In 76 schools of four urban "
   "districts, first graders with weak number skills received about 30 "
   "hours of small-group tutoring over 17 weeks. Most of the 86 tutors were "
   "retired or substitute teachers, hired through a temporary staffing "
   "company and trained for one day, with two short follow-up sessions. In "
   "a randomised trial of 994 pupils, tutored pupils outperformed their "
   "peers by an effect size of 0.34 (Gersten et al., 2015).", "")],
 [("Tutoring in reading. ", "b"), ("AARP Foundation Experience Corps "
   "trains volunteers aged 50 and over, among them former teachers, to "
   "tutor children to read well by the end of grade 3. In 2023/24, "
   "1 284 volunteers worked with 3 659 children in 18 communities (AARP "
   "Foundation, 2026). A randomised evaluation in 23 schools in Boston, New "
   "York City and Port Arthur found gains in reading comprehension, with "
   "effect sizes of 0.13 to 0.17 for pupils who attended 35 sessions or "
   "more (Morrow-Howell et al., 2009).", "")],
 [("Across the three trials, a short training was enough for experienced "
   "teachers to tutor pupils effectively, while the benefits of mentoring "
   "new teachers were smaller and depended on the time that mentors could "
   "spend with them.", "")],
 src("Source: DeCesare, D., A. McClelland and B. Randel (2017), *Impacts "
     "of the Retired Mentors for New Teachers Program*; Gersten, R. et al. "
     "(2015); Morrow-Howell, N. et al. (2009), *Evaluation of Experience "
     "Corps*; AARP Foundation (2026)."),
])

h3("Implications for re-entry policies")

p("Flexible positions therefore reach former teachers who would not "
  "return to a full post, and particularly retirees and leavers with care "
  "responsibilities. Their value for pupils depends on the role assigned to "
  "returners, since the largest benefits observed come from tutoring, and "
  "their cost depends on the pay offered. Singapore keeps its pool "
  "inexpensive by paying adjunct teachers well below regular teachers, but "
  "this also limits the use of the pool to occasional cover, whereas China "
  "and the tutoring programmes assign returners a defined role over a "
  "whole school year.")

# ======================================================================
h2("3.6 Flexible re-certification")

p("Although licensing requirements play a minor part in the decision to "
  "leave teaching (Section 2), a teacher who has been away for several "
  "years may need to renew a lapsed licence or complete a refresher "
  "programme before teaching again, a process that can take months and "
  "involve costs precisely when a school is waiting to fill a post. A small "
  "number of systems have tried to lighten this process for returners.")

p("New Zealand has gone furthest among the systems reviewed, replacing its "
  "refresher programme with a plan agreed between the returner and the "
  "principal of the school that offers the job (Box 12). In the United "
  "States, Virginia's Executive Directive 3 of September 2022 instructed "
  "the state's licensing authority to issue licences to retired teachers "
  "whose licences had lapsed, and the state launched an online licensing "
  "system in November 2023 (Commonwealth of Virginia, 2022). Other policies "
  "include lighter versions of the same instrument. New South Wales helped "
  "returners to renew their accreditation (Box 5), Lower Saxony exempts "
  "teachers who continue at their school immediately after retiring from "
  "providing a new police certificate or applying through the online "
  "recruitment system (Box 4), and the task force set up in the Bahamas "
  "checks the records and accreditation of recruits (Section 3.5).")

box("Box 12. Replacing the refresher course with a plan agreed with the "
    "school in New Zealand", [
 [("To renew a practising certificate, a teacher in New Zealand must have "
   "at least two years of satisfactory teaching in the previous five. "
   "Teachers who did not meet this requirement used to complete an external "
   "refresher programme, the Teacher Education Refresh, before returning. "
   "Since September 2024, the Teaching Council has allowed returners with a "
   "job offer to replace it with a return-to-practice plan, and in "
   "December 2025 it made this route permanent from January 2026 under the "
   "name Kia Maia, extending it to some teachers who would otherwise have "
   "needed the refresher programme (Teaching Council of Aotearoa New "
   "Zealand, 2025).", "")],
 [("The returner assesses, together with the principal of the school that "
   "has offered the job, what has changed since they last taught, and the "
   "plan lists at least three resources for each professional standard that "
   "the returner will use during the first 12 months back. Both sign the "
   "plan, which Council staff review without assessing the teacher's "
   "competence, and the certificate is then renewed. Without a job offer, "
   "the refresher programme is still likely to be required (Teaching "
   "Council of Aotearoa New Zealand, 2026).", "")],
 [("The government also paid the registration fees of returning teachers "
   "from October 2024, supporting 352 returners by April 2025, and has "
   "covered the fees of all teachers since July 2025 with NZD 53.3 million "
   "over three years (Ministry of Education New Zealand, 2025). Between "
   "January and October 2026, 501 teachers renewed their certificate "
   "through Kia Maia, most of them working in primary (198) or secondary "
   "(133) schools or in early childhood education (110). Women made up 84% "
   "of users and 62% were aged 31 to 50, while only 16% were aged 61 or "
   "over (Teaching Council of Aotearoa New Zealand, unpublished). These "
   "figures indicate that the pathway mainly brings back mid-career "
   "teachers who had stepped away from the profession.", "")],
 [("Linking the renewal of the certificate to a job offer removes a cost "
   "and a delay at the moment when the returner is ready to start, and it "
   "involves the principal in the returner's first year, which the "
   "evidence on induction and leadership reviewed in Section 2 suggests is "
   "important for whether returners stay.", "")],
 src("Source: Teaching Council of Aotearoa New Zealand (2025), “Introducing "
     "Kia Maia”; Teaching Council of Aotearoa New Zealand (2026), “Renew "
     "after time away”; Teaching Council of Aotearoa New Zealand "
     "(unpublished), data on Kia Maia users; Ministry of Education New "
     "Zealand (2025)."),
])

h3("Implications for re-entry policies")

p("No evaluation of these changes is yet available, and the data of the "
  "Teaching Council show who uses the new route in New Zealand but not "
  "whether its users would have returned through the refresher programme. "
  "Estimating the effect of the reform would require comparable data "
  "collected before and after it. The instrument nonetheless has a "
  "practical appeal for systems with demanding renewal rules, since it acts "
  "at the point where a returner who has already found a post could still "
  "be lost.")

p("The policies reviewed in this section respond mostly to shortages and "
  "are addressed mainly to retired teachers, and only a few of them have "
  "been evaluated. Box 13 brings together what each instrument suggests "
  "for the design of re-entry policies, following the structure of "
  "Box 1.")

box("Box 13. What the policies reviewed teach us about re-attracting former "
    "teachers", [
 [("Each instrument responds to a barrier identified in Section 2, and "
   "the policies with the most encouraging results combine several of "
   "them.", "")],
 [("Financial incentives. ", "b"), ("Mainly retired teachers. ", "i"),
  ("Changing the rules on combining a pension with a salary is inexpensive "
   "and brings back experienced teachers, mostly to the schools where they "
   "used to work. Waiting periods, eligibility rules and the posts covered "
   "determine the reach of these rules as much as the incentive itself, and "
   "payments to schools risk rewarding hires that would have taken place "
   "anyway.", "")],
 [("Information and nudges. ", "b"), ("All profiles. ", "i"),
  ("Letters sent after retirement obtain very low responses. Contact "
   "before retirement or soon after leaving, made through the principal "
   "and accompanied by help with the procedures, appears more effective, "
   "particularly when it coincides with better working conditions.", "")],
 [("Support and training. ", "b"), ("Mainly switchers and leavers. ", "i"),
  ("Refresher courses detached from schools and vacancies attract interest "
   "but few returns. Support converts best when it follows the recruitment "
   "calendar, is tied to real posts and includes supervised time in front "
   "of a class.", "")],
 [("Flexible positions. ", "b"), ("All profiles. ", "i"),
  ("Pools of relief and adjunct teachers bring back those who would not "
   "return to a full post, and the strongest evidence of benefits for "
   "pupils in this review concerns retired teachers working as tutors and "
   "mentors.", "")],
 [("Flexible re-certification. ", "b"), ("Mainly switchers and leavers. ", "i"),
  ("Linking the renewal of a licence to a job offer and to a plan agreed "
   "with the school removes a cost and a delay at the moment of return, "
   "and involves the principal in the returner's first year.", "")],
 [("Overall. ", "b"),
  ("Most policies are short-term remedies for local shortages, and few "
   "have been evaluated or allow returners to be followed over time. "
   "Combining instruments, reaching teachers at the right moment and "
   "offering roles that match their preferences appear to matter more than "
   "the size of any single incentive, and building evaluation and data on "
   "returners into new policies would allow systems to learn which of them "
   "work.", "")],
])

TABLES = _v3.TABLES
TABLES["T2"]["widths"] = (1400, 2850, 800, 530, 530, 530, 530, 530, 1360)
TABLES["T2"]["size"] = 15
TABLES["T2"]["head"][1][4] = ("Rec.", 1, 1)
TABLES["T2"]["head"][0][2] = ("Target", 1, 2)
TABLES["T3"]["widths"] = (1450, 1700, 1500, 1500, 2910)
TABLES["T3"]["size"] = 16
TABLES["T4"]["widths"] = (1200, 1450, 2050, 1750, 1610, 1000)
TABLES["T4"]["size"] = 16
REFS = [r for r in _v3.REFS if not r.startswith(('Ministerie van OCW (2019)', 'Office of the Governor of New Mexico'))]
