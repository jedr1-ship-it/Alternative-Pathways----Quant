# Section 3 content as blocks:
# ("h2", text) ("h3", text) ("p", text) ("cap", text) ("src", text)
# ("table2",) ("box", title, [para, ...]) where a para is a list of
# (text, style) runs with style in {"", "b", "i"}.

B = []

def h2(t): B.append(("h2", t))
def h3(t): B.append(("h3", t))
def p(t): B.append(("p", t))
def box(title, paras): B.append(("box", title, paras))

# ---------------------------------------------------------------- intro
p("This section reviews the policies that education systems have used to "
  "bring former teachers back into schools. It draws on 30 policies from 18 "
  "countries, collected by the authors from official documents, legal texts, "
  "parliamentary records, institutional evaluations and, where no official "
  "source exists, reputable press, and on exchanges with ministry officials "
  "in Lower Saxony (Germany), Quebec (Canada) and New Zealand. Every "
  "policy was verified against its primary sources in October 2026. The "
  "policies are grouped by the main instrument they use, following the five "
  "categories set out in Table 2: financial incentives, information and "
  "nudges, support and training, flexible positions and flexible "
  "re-certification. Many policies combine more than one instrument, and "
  "each is presented under the one that defines it best.")

h2("3.1 An overview of the policies")

p("Most of the policies reviewed were designed to respond to teacher "
  "shortages, and many to shortages that were local, concentrated in "
  "particular subjects or regions, or sudden. A large group was introduced "
  "or extended during the COVID-19 pandemic, when absences among serving "
  "teachers multiplied the need for substitutes: Quebec created its "
  "incentives for retired teachers in autumn 2020 under the health "
  "emergency, Ontario temporarily raised the number of days retirees may "
  "work without losing their pension, Ireland waived pension abatement for "
  "retired substitutes in 2021, and England called former teachers back to "
  "cover absences during the Omicron wave of winter 2021-22. A smaller group "
  "pursues a different aim, which is to put the experience of former "
  "teachers to use in roles that serving teachers rarely have time for. "
  "China sends retired principals and senior teachers to rural schools to "
  "coach young colleagues, and programmes in the United States and Spain "
  "have used retired teachers as mentors for novice and student teachers or "
  "as tutors for pupils who are falling behind.")

p("The policies target the three profiles of former teachers unevenly. Of "
  "the 30 policies, 19 address retired teachers only, 7 address switchers "
  "and leavers, and 4 are open to all three profiles. The prominence of "
  "retirees has a simple explanation. They are easy to identify, they are "
  "fully qualified, many retire before they wish to stop working "
  "altogether, and the main obstacle to their return is a rule that "
  "governments control directly, namely the reduction or suspension of the "
  "pension when a retiree takes paid work in the public sector. Changing "
  "that rule is the most common policy in the review, and it explains why "
  "financial incentives are the largest category in Table 2.")

p("Most of these policies are short-term remedies. Several were enacted with "
  "a fixed end date and then renewed one period at a time: Ireland's waiver "
  "of pension abatement was introduced in 2021 and has been extended twice, "
  "most recently to the end of 2027; Michigan's rules expire in October "
  "2028; Georgia's law expired in June 2026 and was replaced by a new one "
  "that sunsets in 2030; and Quebec's incentives are renegotiated every "
  "school year with the teacher unions. Others were reversed. Ontario's "
  "teachers' federation declined to extend the higher limit on working days "
  "in 2024, and Portugal repealed its scheme for hiring retired teachers in "
  "September 2026, two years after creating it (Government of Portugal, "
  "2026). This pattern reflects the "
  "purpose of the policies, which is to fill vacancies quickly. Few treat "
  "former teachers as a permanent source of supply.")

p("Where take-up is reported, it is small relative to the size of the "
  "teaching workforce. In Germany, a survey of the federal states counted "
  "more than 5 000 retired teachers who had stayed on or returned by 2023, "
  "under 1% of the teaching workforce (Deutsches Schulportal, "
  "2023). In Georgia, retirees hired under the state's return-to-work law "
  "averaged about 350 a year, also under 1% of teachers (Georgia Department "
  "of Audits and Accounts, 2025), and Portugal validated 55 retired "
  "teachers against a quota of 200 places (Observador, 2024). Returners "
  "nonetheless form a large share of new entrants in some systems. In "
  "England, returners accounted for 17 740 full-time equivalent qualified "
  "teachers entering state schools in 2025/26, 43% of all qualified "
  "entrants and more than the 16 300 newly qualified teachers (Department for Education, 2026a). Most of "
  "these returners came back without any dedicated programme, which "
  "suggests that the size of the margin depends more on the conditions of "
  "the profession than on any single instrument.")

p("Evidence on effectiveness is scarce. Only a handful of the policies have "
  "been evaluated, and only three of those evaluations, all concerning "
  "flexible positions, are randomised trials. Two official evaluations of "
  "re-entry programmes, in England and the Netherlands, found low "
  "conversion or substantial deadweight, and a third, in Sweden, found that "
  "a refresher course barely reached its target group. The retention of "
  "returners once back in school is almost never measured; Georgia, where "
  "43% of the retirees hired in 2023 were still teaching two years later, "
  "is an exception. The sections that follow describe each instrument in "
  "turn, illustrated with selected country cases.")

B.append(("cap", "Table 2. Policies reviewed, by main instrument and target group"))
B.append(("table2",))
B.append(("src", "Note: R: retired teachers; S/L: switchers and leavers; "
          "All: all three profiles. Each policy is listed under its main "
          "instrument; many use secondary instruments as well, which are "
          "discussed in the text. AARP Foundation Experience Corps recruits "
          "older adults in general, not only former teachers."))
B.append(("src", "Source: Authors' compilation from official sources, "
          "verified in October 2026."))

# ---------------------------------------------------------------- 3.2
h2("3.2 Financial incentives")

p("Financial incentives take two forms. The first, and by far the most "
  "common, is a change in the rules that govern how pension and salary can "
  "be combined, which allows retired teachers to return without losing all "
  "or part of their pension. The second consists of direct payments, either "
  "to the returning teacher or to the school that hires them.")

h3("Combining pension and salary")

p("In most public-service pension schemes, a retired teacher who takes paid "
  "work in the public sector sees the pension reduced or suspended once "
  "pension and new salary together exceed a threshold, as discussed in "
  "Section 2. The policies in this group relax that rule, and they differ "
  "mainly in how far they relax it and on what conditions. Some allow a "
  "limited number of working days a year without any reduction: Ireland "
  "waives abatement for the first 50 days a retired teacher works in a "
  "calendar year, provided that the need cannot practicably be met in "
  "another way (Department of Education, 2026), and Ontario allows "
  "retirees to work 50 days in a school year, a limit that was raised to "
  "95 days in each of the three school years from 2020-21 to 2022-23 "
  "(Ontario Teachers' Federation, 2020). Others raise or remove the "
  "earnings ceiling. Lower Saxony temporarily raised it to 150% of the "
  "pensionable salary in 2022 and abolished it in 2024 for retirees who "
  "have reached the statutory age (Box 4), and Michigan lets retirees return "
  "to any post without an earnings limit once they have been retired for "
  "six months (Michigan Office of Retirement Services, 2023). France allows full "
  "cumulation of pension and salary to retirees who receive a full-rate "
  "pension and caps earnings for the rest (Assemblée nationale, 2026).")

p("Several systems attach conditions that target the policy on shortages. "
  "In the United States, Georgia required 30 years of service and a "
  "full-time post in a subject of high need (Box 3), Louisiana and "
  "Virginia restrict the full return to posts declared critical shortages, "
  "and Virginia's rule, in force since 2001, applies only after a break in "
  "service that was shortened from 12 to 6 months in 2023 (Virginia "
  "Retirement System, 2023). Portugal allowed schools to hire retired "
  "teachers for hard-to-fill posts within a national quota (Government "
  "of Portugal, 2024). Many schemes also "
  "decide whether returners keep paying into the pension fund. In Georgia "
  "and New Mexico, contributions continue to be paid on the returner's "
  "salary but earn no further pension rights, which limits the cost of the "
  "policy to the pension system.")

p("The evidence on these rules points in three directions. First, the "
  "conditions matter as much as the incentive. When Virginia shortened the "
  "break in service from 12 to 6 months, retirees returning between July "
  "and October rose from 18 in 2022 to 150 in 2023 (Virginia Retirement "
  "System, 2023), whereas Portugal validated 55 retired teachers for "
  "a quota of 200 places before repealing the scheme. Second, rules of this kind "
  "tend to channel returners towards the schools that most need them. In "
  "North Carolina, where retired teachers could return full-time and keep "
  "their pension between 1999 and 2009, about 3 500 teachers did so, and "
  "30% of them worked in schools in the poorest quartile, against 21% in "
  "the least poor (Jarrold-Grapes and Mahler, 2024). Third, they raise "
  "concerns that are worth anticipating. Ontario's teachers' federation "
  "refused to extend the higher limit in 2024, arguing that more than 30 000 "
  "certified teachers were not employed by school boards and that a "
  "generous rule could encourage early retirement (Ontario Teachers' "
  "Federation, 2024), and returners themselves may find the experience less "
  "rewarding than expected. In Austria, none of the 14 returning retirees "
  "interviewed in a 2025 study said they would repeat the experience "
  "(Resch, 2025).")

box("Box 2. Quebec (Canada): paying retired teachers on the salary scale", [
 [("Quebec's incentives for retired teachers were introduced in autumn 2020, "
   "during the COVID-19 health emergency, by a decree that modified the "
   "national and local collective agreements. Until then, a retiree who "
   "covered an absence was paid the flat daily rate for occasional supply "
   "teaching and reached the salary scale only after 20 consecutive days in "
   "the same replacement. Under the decree, a teacher who had retired in the "
   "previous five years was paid from the first day at the step of the single "
   "salary scale that matched their experience and qualifications, and kept "
   "the full pension. For a retiree at the top of the scale this roughly "
   "doubled the daily rate, from a usual maximum of about CAD 212 to about "
   "CAD 412 (Gouvernement du Québec, 2022).", "")],
 [("From 1 October 2021 a temporary premium of 7.89% was added for retirees "
   "in the public-service pension plan. The emergency measures ended with "
   "the 2021-22 school year, and since 2022-23 the incentives have been "
   "renewed each year through letters of agreement signed outside the "
   "collective agreement with each teacher union federation. The premiums "
   "have changed from one agreement to the next: 7.89% until 2023-24, then "
   "7.5% on supply work and 12.5% on contracts of three months or more in "
   "2024-25, and only the 12.5% premium, now on contracts of one month or "
   "more, from 2025-26. Employers must first offer the work to qualified "
   "staff they already employ. Since 2024-25 the measures have been open to "
   "any retired teacher who is legally qualified to teach.", "")],
 [("The ministry funds the measure after the fact, on the basis of the data "
   "that school service centres report each year on their use of retired "
   "staff. The envelope for 2026-27 is being adjusted downwards, as fewer retirees are used and the "
   "7.5% premium has been withdrawn (Ministère de l'Éducation du Québec, "
   "2026). About 700 retirees returned in 2020-21, and the ministry has "
   "reported more than 5 000 in 2024-25 (Le Devoir, 2025). The measure has "
   "not been evaluated.", "")],
 [("Lessons. ", "b"), ("Paying returners on their own salary step removes "
   "the main financial penalty of supply work for experienced teachers, at a "
   "moderate cost, because the payment is made only for days actually "
   "worked. Its annual renegotiation keeps the measure responsive to "
   "shortages, but it also leaves retirees and school service centres "
   "uncertain about the terms from one year to the next.", "")]])

box("Box 3. Georgia (United States): what an audit shows about returning "
    "retirees", [
 [("Between July 2022 and June 2026, Georgia's House Bill 385 allowed "
   "teachers who had retired with at least 30 years of service, and had been "
   "retired for at least a year, to return to a full-time classroom post in "
   "one of the subjects of highest need in their region and draw a full "
   "salary on top of the full pension. The employer paid both the employer "
   "and the employee pension contributions, and the returner earned no "
   "further service credit (Teachers Retirement System of Georgia, 2026).", "")],
 [("A state audit published in 2025 is one of the few assessments of such a "
   "rule. Between 2023 and 2025, 635 retirees returned under the law, rising "
   "from 241 to 428 a year, an average of about 350, or under 1% of the "
   "state's teachers. Just over half of school systems used it, and 64% of "
   "returners went back to the system they had retired from. Of the 2023 "
   "cohort, 43% were still teaching two years later. Among the systems that "
   "did not use the law, 45 of 72 said they would have liked to but could "
   "find no eligible retiree (Georgia Department of Audits and Accounts, "
   "2025).", "")],
 [("The law expired in June 2026 and was replaced by Senate Bill 150, which "
   "requires at least half of the returner's timetable to be in a "
   "qualifying subject and lets each school system define its own "
   "areas of highest need from a five-year average of vacancies, and expires "
   "in 2030.", "")],
 [("Lessons. ", "b"), ("Strict eligibility keeps the cost of the rule low "
   "but also its reach, since the retirees who qualify are few and are "
   "concentrated where they used to work. Defining need locally, as the new "
   "law does, can bring the rule closer to the vacancies it is meant to "
   "fill.", "")]])

h3("Direct payments")

p("Direct payments are less common. Quebec's measure, described in Box 2, is "
  "the clearest example of a payment to the returner. Victoria (Australia) "
  "pays former teachers a daily honorarium for a supported placement of up "
  "to 40 days (Box 7), and China pays the teachers it posts to rural "
  "schools an allowance of CNY 20 000 a year (Box 9). New Zealand has paid "
  "the registration fees of returning teachers since October 2024, a "
  "measure extended to all teachers from July 2025 (Box 10).")

p("The Netherlands paid the school instead. Between 2017 and 2020, school "
  "boards received a flat EUR 2 500 for each qualified teacher they re-hired "
  "in primary education after at least a year away, to cover coaching and "
  "refresher training (Ministerie van OCW, 2017). The grant was used for 274 "
  "returners in three years, well below the number the budget allowed, and school boards told "
  "the ministry that most of these teachers would have been hired and "
  "supported without it. The ministry concluded that the grant had "
  "contributed only to a limited extent and did not extend it (Tweede "
  "Kamer, 2020). The Dutch case illustrates a general risk of payments to "
  "employers, which is that they reward hiring decisions that would have "
  "been taken anyway.")

# ---------------------------------------------------------------- 3.3
h2("3.3 Information and nudges")

p("A second group of policies seeks to inform former teachers of the "
  "options available to them, or to prompt them to consider returning, "
  "through letters, telephone calls, advisers or information sessions. "
  "These instruments are cheap, and they address a barrier that the "
  "evidence in Section 2 suggests is real, namely that many former teachers "
  "are open to returning but are not asked, do not know how, or expect the "
  "process to be burdensome.")

p("The timing and the messenger appear to matter. Austria offers a "
  "cautionary case. In December 2022 the education directorate of Vienna "
  "wrote to nearly 300 retired teachers and three returned; from February "
  "2023 it asked school principals instead to talk in person with teachers "
  "approaching retirement age about staying on (ORF Wien, 2023). Other "
  "Austrian provinces followed different routes: Salzburg wrote to all "
  "retired teachers up to the age of 67, and Vorarlberg includes "
  "information on staying on with the forms teachers fill in to apply for "
  "their pension (ORF, 2023). Lower Saxony reached the same conclusion as Vienna, "
  "contacting teachers before they retire rather than after (Box 4). New "
  "South Wales (Australia) shows that outreach can also work with teachers "
  "who left recently, when it is accompanied by help with the procedures "
  "and by better conditions in the profession (Box 5).")

p("England offers an advisory service, through which former teachers can "
  "ask for an adviser who supports them one to one with applications, "
  "interviews, refresher courses and vacancies; in 2026 the Department for "
  "Education committed to keeping it and added a step-by-step guide (Department "
  "for Education, 2026b). Japan illustrates a different use of information. "
  "Because any accredited university can award a teaching licence after a "
  "short practicum, Japan has a large pool of licence holders who have never "
  "taught or have long been away from schools. In 2023, 50 of the 68 "
  "prefectural and city boards of education ran sessions or training for "
  "these licence holders, and the national ministry funds such initiatives "
  "(MEXT, 2024). In Saitama, seven seminars in 2023 drew 226 participants, "
  "of whom 122 registered for temporary or part-time posts and 53 had been "
  "appointed by April 2024. The session held by the Miyazaki Prefectural "
  "Board of Education in November 2025 shows what teachers in this group "
  "are told: how a teacher's day has changed, what professional development "
  "is available, and which posts they can take without sitting the "
  "competitive examination, from temporary full-time teacher to part-time "
  "teacher or school support staff, before individual consultations and "
  "registration as a temporary teacher (Miyazaki Prefectural Board of "
  "Education, 2025).")

p("None of these outreach initiatives has been formally evaluated, and in "
  "most cases the data do not allow returners to be linked to the contact "
  "that prompted them to return.")

box("Box 4. Lower Saxony (Germany): a package for teachers about to retire", [
 [("Lower Saxony's approach combines three instruments aimed at teachers "
   "approaching retirement. The first is financial. Under the civil-service "
   "pension law, a retired teacher working for the state had the pension "
   "reduced once pension and salary together exceeded a share of the former "
   "salary. In 2022 the state parliament raised that ceiling from 125% to "
   "150% of the pensionable salary, which allowed a pensioner to teach about "
   "nine to ten lessons a week without any reduction, and in 2024 it "
   "abolished the ceiling for teachers who have reached the statutory "
   "retirement age (Niedersächsischer Landtag, 2024). Teachers who retire "
   "early remain subject to a ceiling.", "")],
 [("The second is information. In November 2023 the Minister of Education "
   "wrote personally to every teacher about to retire, civil servants and "
   "salaried staff alike, thanking them for their service and setting out "
   "how they could stay on: a civil servant can ask to postpone retirement, "
   "and any teacher can be re-employed on a fixed-term contract immediately "
   "after retiring while drawing the pension. The letter went to teachers "
   "approaching retirement partly because the ministry no longer held the "
   "personnel files of those who had already retired. School principals "
   "were also asked to approach these teachers in person (Niedersächsisches "
   "Kultusministerium, 2023).", "")],
 [("The third is administrative. A teacher who continues at their former "
   "school immediately after retiring does not need to apply through the "
   "online recruitment system or provide a new police certificate, and "
   "contact persons in each of the four regional school authorities advise "
   "retirees and handle the procedure. The number of teachers past "
   "retirement age working on fixed-term contracts rose from 229 in 2020 to "
   "437 in 2024 (Niedersächsischer Landtag, 2025).", "")],
 [("According to the ministry, most returners stay at or return to the "
   "school where they last taught, usually part-time and in a specific "
   "subject such as mathematics, and rarely as class teachers or formal "
   "mentors. The ministry stresses that the funding for these posts must be "
   "additional, so that retirees do not take positions from young teachers. "
   "No formal evaluation has been carried out, and the absence of a unique "
   "teacher identifier prevents the state from following individual "
   "careers.", "")],
 [("Lessons. ", "b"), ("The financial change was one part of a package. "
   "Reaching teachers before they retire, through a personal "
   "letter and their own principal, and simplifying the procedure for those "
   "who simply continue at their school, make the decision to stay a small "
   "step instead of a new application.", "")]])

box("Box 5. New South Wales (Australia): calling back recent leavers", [
 [("In November 2023 the New South Wales Department of Education contacted "
   "more than 1 500 teachers who had left its schools in the previous five "
   "years and asked them to consider returning. Those interested were "
   "offered a simpler re-employment process, help with accreditation, "
   "approval to teach and the working-with-children check, and placement in "
   "casual or temporary work, with permanent posts and small-group tutoring "
   "roles also available.", "")],
 [("By May 2024 more than 260 had expressed interest and 145 had been "
   "matched with schools, about 60% of them coming back from retirement "
   "(NSW Government, 2024). The campaign followed the largest pay rise for "
   "the state's teachers in decades, effective from October 2023, which "
   "raised the starting salary from AUD 75 791 to AUD 85 000, together with "
   "a reduction in administrative workload. Teacher vacancies in the state "
   "fell from a peak of 3 311 in 2022 to 1 294 in February 2025, although "
   "the contribution of returners to that fall is not known.", "")],
 [("Lessons. ", "b"), ("Recent leavers can be identified from the "
   "employer's own records, and a direct call with practical help converted "
   "about one in ten of those contacted. That the call coincided with better "
   "pay and a lighter administrative load is consistent with the evidence "
   "in Section 2 that conditions, more than information alone, determine "
   "whether former teachers are willing to return.", "")]])

# ---------------------------------------------------------------- 3.4
h2("3.4 Support and training")

p("A third group of policies reduces the practical cost of returning, "
  "through refresher courses, supervised time in classrooms, coaching and "
  "induction. These measures respond to the uncertainty that former "
  "teachers often report about changes in curricula, assessment and "
  "classroom practice, and to their lack of recent experience, which schools "
  "may also see as a risk.")

p("The evidence on these programmes is sobering, and it is unusually rich "
  "for a field with so few evaluations. England's Return to Teaching pilot "
  "drew far more interest than it could convert into posts (Box 6). Sweden's "
  "National Agency for Education launched a free online course for "
  "returning teachers in 2018, covering the changes in curricula, laws and "
  "guidelines since the reforms of 2010 and 2011. By April 2020, 1 018 "
  "people had registered, 175 had completed at least one module and 38 had "
  "completed the whole course; only about a third of respondents to the "
  "follow-up survey were actually returning teachers, and none of those who "
  "were employed had been given working time or a mentor to take it. The "
  "agency concluded that the course had not reached its target group "
  "(Skolverket, 2020).")

p("Programmes that build re-entry into the school itself appear more "
  "promising, although they have not been evaluated either. In the canton "
  "of Zurich (Switzerland), teachers returning after eight years or more are "
  "entitled to the same induction as new teachers during their first year "
  "back, free of charge, including mentoring by a trained colleague in "
  "their own school, supervision and subject coaching, and they can obtain "
  "an individual assessment of what preparation their return requires (PH "
  "Zürich, 2026). In October 2026, however, the college was not offering "
  "counselling for returners. Victoria (Australia) pays former teachers for up to 40 "
  "days in a school, observing and teaching alongside serving teachers "
  "before they apply for a post (Box 7).")

box("Box 6. England (United Kingdom): lessons from the evaluation of a "
    "return-to-teaching pilot", [
 [("Between January and October 2016, the Department for Education funded "
   "60 partnerships of schools to support qualified teachers returning to "
   "secondary subjects in shortage, with subject training, updates on "
   "assessment and behaviour management, classroom experience and "
   "mentoring, free of charge for the returner. The pilot attracted 5 729 "
   "registrations, well above its target of 3 000. Of these, 354 received "
   "support, 62 were teaching in a state school by November 2016 and 27 held "
   "a permanent post in the targeted subjects. The cost per additional "
   "returner was about GBP 37 400, close to the cost of training a new "
   "teacher, and the independent evaluation judged the pilot unlikely to "
   "represent good value for money (Buchanan et al., 2018).", "")],
 [("The evaluation identified several reasons for the low conversion. "
   "Support was offered from January, when few posts for the following "
   "September remained open. Many schools hesitated to give returners "
   "teaching practice, citing the need to establish their quality and the "
   "risk of disrupting lessons, and only 44% of returners felt their needs "
   "had been met. Half of the returners interviewed wanted part-time work, "
   "which few schools offered. Returners named their lack of recent "
   "experience, workload, the lack of flexible posts and their own "
   "confidence as the main barriers. A follow-up programme in 2016-17 tied "
   "support to identified vacancies, made teaching practice compulsory and "
   "paid returners a bursary of up to GBP 600 for childcare or travel, but "
   "was not evaluated.", "")],
 [("Lessons. ", "b"), ("Registrations far exceeded the target, and the "
   "losses came later. Re-entry support converts best when it is timed to the recruitment calendar, linked to "
   "real vacancies, includes time in front of a class, and is matched by "
   "schools willing to offer the part-time posts that many returners "
   "want.", "")]])

box("Box 7. Victoria (Australia): a paid placement before applying", [
 [("Victoria's Teacher Re-Engagement Initiative, launched in late 2022, "
   "offers qualified teachers who have been away from teaching for at least "
   "12 months a paid placement of up to 40 days in a government school. "
   "During the placement they observe classes and school routines with the "
   "mentoring of serving staff before they apply for a post. A central team "
   "matches participants with schools by subject, experience, location and "
   "availability, and records at the end of the placement whether the "
   "participant has re-engaged with teaching.", "")],
 [("The initiative drew more than 1 100 expressions of interest and received AUD 12 million in the 2023-24 state budget (Victorian "
   "Government, 2026). It is now funded by the schools that "
   "host a returner, at AUD 330 per day to cover the participant's "
   "honorarium and administrative costs. No figures have been published on "
   "the number of participants who went on to teach.", "")],
 [("Lessons. ", "b"), ("A supervised placement addresses at once the "
   "returner's lack of confidence and the school's uncertainty about the "
   "returner, the two obstacles that the English evaluation identified. "
   "Shifting the cost to schools may limit take-up to those that can "
   "afford it.", "")]])

# ---------------------------------------------------------------- 3.5
h2("3.5 Flexible positions")

p("A fourth group of policies offers former teachers roles other than a "
  "full-time teaching post, such as relief and adjunct teaching, tutoring "
  "and mentoring. These roles match the preferences that many former "
  "teachers express, particularly leavers with care responsibilities and "
  "retirees who want to work part of the week, and they allow systems to "
  "use experience where it is most valuable.")

p("Pools of flexible teachers are the simplest version. Singapore has run "
  "an adjunct scheme for former teachers since 2004 (Box 8), and the "
  "Bahamas announced in July 2026 a reserve of former teachers, retirees "
  "and graduates, built on its supply-teacher platform, as part of a "
  "recruitment drive to fill about 300 vacancies across 162 public schools "
  "on 24 islands; more than 100 teachers had been recruited through the "
  "drive by September 2026 (Ministry of Education of The Bahamas, 2026). "
  "China's Silver-Age Lecturing Plan places retired teachers in rural "
  "schools to teach and to coach the young teachers there (Box 9).")

p("Mentoring and tutoring by retired teachers have been tested more "
  "rigorously than any other instrument in this review. In Aurora, "
  "Colorado, recently retired teachers and principals were paid to mentor "
  "teachers in their first three years in high-poverty elementary schools, "
  "for about an hour a week over two years. A randomised trial found a small "
  "positive effect on pupils' mathematics after the first year, of similar "
  "size but no longer significant after the second, and no significant "
  "effect on whether the mentored teachers stayed (DeCesare et al., "
  "2017). Tutoring shows larger effects. In a randomised trial in 76 "
  "schools in four urban districts of the United States, first graders with "
  "weak number skills who received about 30 hours of small-group "
  "mathematics tutoring, mostly from retired and substitute teachers, "
  "outperformed their peers by an effect size of 0.34 (Gersten et al., "
  "2015). AARP Foundation Experience Corps, which trains adults over 50, "
  "among them former teachers, to tutor young readers, improved reading "
  "comprehension in a randomised evaluation (Morrow-Howell et al., 2009). "
  "These results are consistent with the broader experimental evidence on "
  "tutoring cited in Section 1, and they suggest that tutoring is one of "
  "the most productive uses of former teachers who do not wish to return to "
  "a full post. Smaller initiatives point in the same direction. At the "
  "University of Zaragoza (Spain), ten retired teachers mentored 57 "
  "student teachers in their final years in 2018 (Lizalde Gil and Cortés "
  "Pascual, 2019).")

box("Box 8. Singapore: an adjunct scheme for former teachers", [
 [("Singapore's Ministry of Education launched an adjunct teachers "
   "programme in 2004 to attract former trained teachers back to the "
   "profession on more flexible terms. Under the current Flexi-Adjunct "
   "Teaching Scheme, former teachers register on a ministry portal for "
   "three years, and schools contact them directly for appointments of one "
   "day to ten weeks, for teaching alone or for teaching and other duties "
   "agreed with the school. They are paid by the hour, in tiers that depend "
   "on experience, and earn leave once they have accumulated 90 days of "
   "service. A companion scheme offers former teachers contracts of one to "
   "one and a half years, full-time or part-time (Ministry of Education "
   "Singapore, 2026).", "")],
 [("Between 2022 and 2024, about 220 teachers a year were engaged as "
   "flexi-adjunct teachers within twelve months of leaving the service. In "
   "the same period the annual resignation rate of teachers was 2.4%, and "
   "1.7% excluding those who joined the scheme (Ministry of Education "
   "Singapore, 2025).", "")],
 [("Lessons. ", "b"), ("A standing pool lets a system keep in contact with "
   "teachers at the moment they leave, before their skills and their links "
   "with schools fade, and lets those who left for family or other reasons "
   "keep a foot in the profession on terms they choose. Pay well below that "
   "of regular teachers keeps the scheme cheap but limits its use to "
   "occasional cover.", "")]])

box("Box 9. China: retired teachers for rural schools", [
 [("China's Silver-Age Lecturing Plan, launched in 2018 by the Ministries of "
   "Education and Finance, recruits retired principals, teaching "
   "researchers and senior teachers, generally aged 65 or under, to serve "
   "for at least a school year in rural primary and lower-secondary schools "
   "in poor, ethnic-minority and border counties. They teach classes, "
   "observe and give demonstration lessons, coach the school's young "
   "teachers and help with school management, and retired principals may "
   "serve as deputy heads. They keep their pension and receive CNY 20 000 a "
   "year for living costs, travel and insurance, paid by the central "
   "government in western provinces, shared between central and provincial "
   "governments in central provinces, and paid by the province in eastern "
   "ones. Returning to one's own former school does not count (Ministry of "
   "Education and Ministry of Finance of the People's Republic of China, "
   "2018).", "")],
 [("More than 20 000 retired teachers had been recruited by mid-2023, and "
   "recent annual rounds have planned 6 000 to 7 000 places. In 2023 ten "
   "government departments set a target of about 120 000 retired teachers "
   "across all levels of education. The 2026 round places the coaching of "
   "young teachers at the centre of the role and introduces an assessment "
   "by the host school at the end of each placement (Ministry of Education "
   "of the People's Republic of China, 2026).", "")],
 [("Lessons. ", "b"), ("The plan uses retired teachers above all to "
   "transfer experience to schools that struggle to attract and develop "
   "teachers, which is the use of former teachers that the evidence on mentoring and peer learning supports.", "")]])

# ---------------------------------------------------------------- 3.6
h2("3.6 Flexible re-certification")

p("A final group of policies lowers the regulatory barriers to returning. "
  "As discussed in Section 2, licensing rules rarely drive qualified "
  "teachers out of the profession but can stand in the way of their "
  "return, since a teacher who has been away for several years may need to "
  "renew a lapsed licence or complete a refresher programme before teaching "
  "again. New Zealand has replaced its refresher course with a plan agreed "
  "with the employing school (Box 10). In the United States, Virginia "
  "instructed its licensing authority in 2022 to issue licences to retired "
  "teachers whose licences had lapsed, and launched an online licensing "
  "system in 2023 (Commonwealth of Virginia, "
  "2022). Other policies include lighter forms of the same instrument, "
  "such as the help with accreditation that New South Wales offered to "
  "returners (Box 5).")

box("Box 10. New Zealand: from a refresher course to a plan agreed with "
    "the school", [
 [("To renew a practising certificate, a New Zealand teacher must have at "
   "least two years of satisfactory teaching in the previous five. Teachers "
   "who did not meet that requirement used to complete an external refresher "
   "programme, the Teacher Education Refresh, which was costly and could "
   "take months. Since September 2024 the Teaching Council has allowed returners with "
   "a job offer to replace it with a return-to-practice plan, and in December "
   "2025 it made this route permanent, under the name Kia Maia, from January "
   "2026 (Teaching Council of Aotearoa New Zealand, 2025). The returner "
   "assesses, together with the principal of the school that has offered "
   "the job, what has changed since they last taught and which resources "
   "they will use to update their knowledge against each of the professional "
   "standards over their first year back. Both sign the plan, Council staff "
   "review it without assessing the teacher's competence, and the "
   "certificate is renewed. Without a job offer, the refresher programme is "
   "still likely to be required.", "")],
 [("The government also paid the registration fees of returning teachers "
   "from October 2024, supporting 352 returners by April 2025, and has "
   "covered the fees of all teachers since July 2025 with NZD 53.3 million "
   "over three years. Between January and October 2026, 501 teachers renewed "
   "their certificate through Kia Maia. Most worked in primary (198) or "
   "secondary (133) schools or in early childhood education (110), 84% were "
   "women, and 62% were aged 31 to 50, while 16% were 61 or older "
   "(Teaching Council of Aotearoa New Zealand, personal communication, "
   "October 2026). The pathway thus mainly brings back mid-career teachers "
   "who had stepped away.", "")],
 [("Lessons. ", "b"), ("Replacing an external course with a plan agreed "
   "with the employing school removes a cost and a delay at the moment the "
   "returner has a job in hand, and it involves the principal in the "
   "returner's first year, which the evidence on induction and leadership in "
   "Section 2 suggests matters for whether they stay.", "")]])

# ---------------------------------------------------------------- 3.7
h2("3.7 Taken together")

p("The policies reviewed share three features. They are mostly reactive, "
  "introduced to fill vacancies quickly and renewed or withdrawn as "
  "shortages change. They focus on retired teachers, whose return depends "
  "on rules that governments can change at little cost, while switchers and "
  "leavers, who make up most former teachers below retirement age, are "
  "addressed by fewer and smaller programmes. And they are rarely evaluated, "
  "so that most of what is known about their effects comes from take-up "
  "figures that cannot separate the returners they attracted from those who "
  "would have come back anyway.")

p("Read against the reasons for leaving reviewed in Section 2, the cases "
  "suggest that instruments work best in combination with the conditions "
  "that former teachers return to. Lower Saxony paired the removal of a "
  "financial penalty with a personal letter and a simpler procedure, New "
  "South Wales called back recent leavers after a large pay rise and a cut "
  "in administrative work, and New Zealand tied re-certification to a job "
  "offer and to the school's principal. Conversely, the programmes that "
  "offered support or money alone, without posts that suited returners or "
  "schools willing to take them, converted little of the interest they "
  "raised. The returners themselves appear to be most valuable when their "
  "role matches their experience, as mentors, tutors or flexible staff, "
  "and the strongest experimental evidence in this review concerns those "
  "roles.")

# references to add (alphabetical insertion into the reference list)
REFS = [
 "Assemblée nationale (2026), Question écrite n° 11063 sur le cumul emploi-retraite, réponse publiée le 12 mai 2026, Paris, https://questions.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE11063.pdf.",
 "Buchanan, E. et al. (2018), Evaluation of the Return to Teaching Pilot Programme, National Foundation for Educational Research for the Department for Education, London, https://assets.publishing.service.gov.uk/media/5b33aeef40f0b67f6744de9d/Evaluation_of_the_Return_to_Teaching_pilot_programme.pdf.",
 "Commonwealth of Virginia (2022), Executive Directive Three: Addressing Teacher Shortages in Virginia Schools, Office of the Governor, Richmond.",
 "Department for Education (2026a), School Workforce in England: Reporting Year 2025, National Statistics, London, https://explore-education-statistics.service.gov.uk/find-statistics/school-workforce-in-england.",
 "Department for Education (2026b), 6,500 Additional Teachers: Delivery Plan, CP 1508-II, London, https://assets.publishing.service.gov.uk/media/6995de6aa58a315dbe72bf7c/6500_additional_teachers_delivery_plan_print_ready_version.pdf.",
 "Department of Education (2026), Circular 0017/2026: Extension to the Waiver of Abatement of Public Sector Pensions under Section 52 of the Public Service Pensions (Single Scheme and Other Provisions) Act 2012, Dublin.",
 "Government of Portugal (2024), Decreto-Lei n.º 51/2024, de 28 de agosto, Diário da República, Lisbon, https://diariodarepublica.pt/dr/detalhe/decreto-lei/51-2024-885927817.",
 "Government of Portugal (2026), Decreto-Lei n.º 175/2026, de 3 de setembro, Diário da República, Lisbon.",
 "Deutsches Schulportal (2023), Länderüberblick: Wie die Länder pensionierte Lehrkräfte zurückgewinnen, Robert Bosch Stiftung, Berlin, https://deutsches-schulportal.de/bildungswesen/laenderueberblick-umfrage-lehrermangel-pensionierte-lehrer/.",
 "Georgia Department of Audits and Accounts (2025), Retired Teachers Return to Work, Report 24-20, Atlanta, https://www.audits.ga.gov/ReportSearch/download/32615.",
 "Gersten, R. et al. (2015), \"Intervention for first graders with limited number knowledge: Large-scale replication of a randomized controlled trial\", American Educational Research Journal, Vol. 52/3, pp. 516-546, https://doi.org/10.3102/0002831214565787.",
 "Gouvernement du Québec (2022), Opération main-d'oeuvre : offensive pour attirer davantage de personnel dans le domaine de l'éducation, communiqué du 24 janvier 2022, Quebec City.",
 "Jarrold-Grapes, J. and P. Mahler (2024), \"Retirees return to work: How a North Carolina policy helped staff high-need schools\", Education Policy Analysis Archives, Vol. 32/4, https://files.eric.ed.gov/fulltext/EJ1425366.pdf.",
 "Le Devoir (2025), \"Québec espère de nouveau attirer des milliers d'enseignants retraités dans les écoles\", 29 August 2025, Montreal.",
 "Lizalde Gil, M. and A. Cortés Pascual (2019), \"10 mirrors: el acompañamiento y la orientación formativa de los estudiantes de los grados en magisterio desde la experiencia profesional\", in Orientación y calidad educativa universitarias, Prensas de la Universidad de Zaragoza, Zaragoza, pp. 373-384.",
 "MEXT (2024), Case Collection on Training for Teaching-Licence Holders Not Currently Teaching, Ministry of Education, Culture, Sports, Science and Technology, Tokyo, https://www.mext.go.jp/content/20240617-mxt_syokyo02-000036498_6.pdf.",
 "Michigan Office of Retirement Services (2023), Public Act 147 of 2023 FAQs, Lansing, https://www.michigan.gov/orsschools/pa-147-of-2023-faqs.",
 "Ministère de l'Éducation du Québec (2026), Incitatifs financiers aux personnes retraitées effectuant un retour à l'enseignement, presentation by the Direction des relations du travail du personnel enseignant, 14 October 2026, Quebec City.",
 "Ministerie van OCW (2017), Regeling tegemoetkoming herintreders primair onderwijs, Staatscourant 2017, nr. 62002, The Hague, https://zoek.officielebekendmakingen.nl/stcrt-2017-62002.html.",
 "Ministry of Education and Ministry of Finance of the People's Republic of China (2018), Notice on the Implementation of the Silver-Age Lecturing Plan, Jiaoshi [2018] No. 7, Beijing, http://www.moe.gov.cn/srcsite/A10/s7151/201807/t20180719_343448.html.",
 "Ministry of Education of the People's Republic of China (2026), Notice on the 2026 Silver-Age Lecturing Plan, Jiaoshi Tinghan [2026] No. 9, Beijing, http://www.moe.gov.cn/srcsite/A10/s7151/202609/t20260929_1452671.html.",
 "Ministry of Education of The Bahamas (2026), The Ministry of Education Aiming to Attract More Bahamian Teachers, press release, 17 July 2026, Nassau.",
 "Ministry of Education Singapore (2025), Statistics on Teachers who Joined Flexi-Adjunct Teaching Scheme, parliamentary reply, 23 September 2025, Singapore, https://www.moe.gov.sg/news/parliamentary-replies/20250923-statistics-on-teachers-who-joined-flexi-adjunct-teaching-scheme-and-median-duration-of-teachers-on-scheme.",
 "Ministry of Education Singapore (2026), Flexi-Adjunct Teaching Scheme, Singapore, https://www.moe.gov.sg/careers/adjunct-and-relief-schemes/flexi-adjunct-teaching-scheme.",
 "Miyazaki Prefectural Board of Education (2025), Information Session on the Appeal of Teaching, Miyazaki, https://www.pref.miyazaki.lg.jp/documents/102783/102783_20250930165145-1.pdf.",
 "Morrow-Howell, N. et al. (2009), Evaluation of Experience Corps: Student Reading Outcomes, Center for Social Development, Washington University in St. Louis, St. Louis.",
 "Niedersächsischer Landtag (2024), Drucksache 19/5338, Hanover, https://landtag-niedersachsen.de/drucksachen/drucksachen_19_07500/05001-05500/19-05338.pdf.",
 "Niedersächsischer Landtag (2025), Drucksache 19/8802, Antwort der Landesregierung, Hanover, https://www.landtag-niedersachsen.de/drucksachen/drucksachen_19_10000/08501-09000/19-08802.pdf.",
 "Niedersächsisches Kultusministerium (2023), Schreiben an angehende Pensionärinnen und Pensionäre, 1 November 2023, Hanover, https://www.mk.niedersachsen.de/download/201317/Schreiben_an_angehende_Pensionaerinnen_und_Pensionaere.pdf.",
 "NSW Government (2024), Retired Teachers Return to Classrooms, media release, 8 May 2024, Sydney, https://www.nsw.gov.au/media-releases/retired-teachers-return-to-classrooms.",
 "Observador (2024), \"A partir de janeiro, 55 professores que estavam reformados vão poder voltar a dar aulas\", 19 December 2024, Lisbon.",
 "Ontario Teachers' Federation (2020), 50-Day Re-employment Rule Increased to 95 Days for Some OTPP Retirees, Toronto.",
 "Ontario Teachers' Federation (2024), OTF Declines Ministry of Education's Request to Amend 50-Day Re-employment Rule, Toronto, https://www.otffeo.on.ca/en/news/otf-declines-ministry-of-educations-request-to-amend-50-day-re-employment-rule/.",
 "ORF (2023), Lehrermangel: Länder holen Pensionisten zurück, 11 March 2023, Vienna, https://oesterreich.orf.at/stories/3198263/.",
 "ORF Wien (2023), Pensionierte Lehrkräfte: Nur drei kehrten zurück, 29 March 2023, Vienna, https://wien.orf.at/stories/3200562/.",
 "PH Zürich (2026), Wiedereinstieg in den Lehrberuf, Pädagogische Hochschule Zürich, Zurich, https://phzh.ch/de/weiterbildung/weiterbildung-fuer-die-volksschule/berufslaufbahn/wiedereinstieg/.",
 "Resch, K. (2025), \"Retired teachers return to school to tackle teacher shortages in Austrian schools. An untapped reserve or emergency response?\", European Journal of Teacher Education, https://doi.org/10.1080/02619768.2025.2531930.",
 "Skolverket (2020), Webbutbildning för återvändande lärare och förskollärare: redovisning av uppdrag, Swedish National Agency for Education, Stockholm.",
 "Teachers Retirement System of Georgia (2026), HB 385 Employment and SB 150 FAQs, Atlanta, https://www.trsga.com/employer/hiring-trs-retirees/sb-150-faqs/.",
 "Teaching Council of Aotearoa New Zealand (2025), Introducing Kia Maia, 10 December 2025, Wellington, https://teachingcouncil.nz/en/news-and-advocacy/news-and-articles/introducing-kia-maia.",
 "Tweede Kamer (2020), Kamerstuk 35300-VIII, nr. 212, The Hague, https://zoek.officielebekendmakingen.nl/kst-35300-VIII-212.html.",
 "Victorian Government (2026), Support for Returning Teachers, Melbourne, https://www.vic.gov.au/teacher-re-engagement-initiative.",
 "Virginia Retirement System (2023), Report on Retirees Returning to Work in Critical Shortage Positions, RD577, Richmond, https://rga.lis.virginia.gov/Published/2023/RD577/PDF.",
]

# Table 2 rows: (instrument, text)
TABLE2 = [
 ("Instrument", "Policies reviewed (target group)"),
 ("Financial incentives",
  "Canada, Ontario (R); Canada, Quebec (R); France (R); Germany, Lower Saxony, earnings ceiling (R); Ireland (R); Netherlands (S/L); Portugal (R); United States: Georgia (R), Louisiana (R), Michigan (R), New Mexico (R), North Carolina (R)"),
 ("Information and nudges",
  "Australia, New South Wales (All); Austria (R); Germany, Lower Saxony, letter (R); Japan, Miyazaki (S/L); United Kingdom, England, advisers (S/L)"),
 ("Support and training",
  "Australia, Victoria (All); Sweden (S/L); Switzerland, Zurich (S/L); United Kingdom, England, pilot programme (S/L)"),
 ("Flexible positions",
  "Bahamas (All); China (R); Singapore (All); Spain, Zaragoza (R); United States: AARP Foundation Experience Corps (R), Colorado (R), four urban districts (R)"),
 ("Flexible re-certification",
  "New Zealand (S/L); United States, Virginia (R)"),
]
