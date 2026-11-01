# Section 3, version 6: structure, boxes and tables modelled on Schweickert
# and Torres (2026), OECD Education Working Paper No. 342. Body text reused
# from version 5 where unchanged.
import copy
import section3_v5 as _v5

V5 = _v5.B
def P(i):
    assert V5[i][0] == 'p', i
    return V5[i][1]

B = []
def h2(t): B.append(("h2", t))
def h3(t): B.append(("h3", t))
def p(t): B.append(("p", t))
def box(title, paras): B.append(("box", title, paras))
def src(t): return [(t, "src")]
def lab(label, text): return [(label + ". ", "b"), (text, "")]

def ret(t, *pairs):
    for a, b in pairs:
        assert a in t, a[:60]
        t = t.replace(a, b)
    return t

# ======================================================================
p("Teacher shortages, ageing workforces and the large number of qualified "
  "teachers who leave the profession before retirement have led many "
  "education systems to look at former teachers as a source of teacher "
  "supply. The measures adopted to bring them back are highly "
  "heterogeneous, and they range from changes to the pension rules that "
  "keep retired teachers out of the classroom to personal letters, "
  "refresher courses and new roles as tutors or mentors. This section "
  "provides an international perspective on these measures, drawing on "
  "30 policies adopted in 18 countries and economies between 1996 and "
  "2026. They were identified through a desk-based review of legal texts, "
  "official documents, parliamentary records and evaluations, complemented "
  "with reputable press reports where no official source exists and with "
  "information provided by officials in Lower Saxony (Germany), Quebec "
  "(Canada) and New Zealand.")

p("The section first proposes a framework that classifies the policies "
  "according to the main instrument they use, and applies it to the "
  "30 policies identified. It then describes the objectives, duration and "
  "available evidence of these policies, before examining each instrument "
  "in turn. Each instrument is illustrated with one or more boxes "
  "showcasing a policy from a specific system, and Box 13, at the end of "
  "the section, brings together what each instrument suggests for the "
  "design of re-entry policies, following the structure of Box 1.")

# ======================================================================
h2("3.1 A framework for policies to re-attract former teachers")

p("In developing a framework for policies that seek to re-attract former "
  "teachers, a first step involves identifying the criteria by which these "
  "policies can be meaningfully distinguished. The policies reviewed differ "
  "along many dimensions, such as the profile of former teachers they "
  "target, the level of government that runs them, their duration or the "
  "resources they mobilise. The framework proposed here classifies them "
  "according to the main instrument they use, since the instrument "
  "reflects the barrier to re-entry that each policy seeks to lower. Five "
  "instruments were identified, each of which can take several forms. "
  "Table 2 presents their definitions and the categories into which the "
  "policies under each instrument can be grouped.")

B.append(("cap", "Table 2. Instruments and categories of policies to "
          "re-attract former teachers"))
B.append(("table", "TC"))
B.append(("src", "Note: Categories derived from the 30 policies reviewed in "
          "this section, listed in Table 3."))

p("The other dimensions considered during the development of the "
  "framework, namely the target group, the level of government and the "
  "period of application, are not used as classification criteria, but "
  "they are reported for each policy in Table 3. Importantly, the "
  "framework is designed as a practical typology intended to provide "
  "guidance rather than a prescriptive standard. Many policies combine "
  "several instruments, and the boundaries between categories are often "
  "blurred. Each policy is therefore assigned to the instrument that "
  "defines it best, while its secondary instruments are also indicated in "
  "Table 3.")

p("Building on these instruments, the framework was applied "
  "systematically to the 30 policies identified through the desk-based "
  "review. " + ret(P(9),
  ("Financial incentives are the main instrument of 12 of the 30 policies,",
   "Financial incentives are the main instrument of 12 of them,"))
  .split(" Five policies rely on")[0])

p("Five policies rely on" + P(9).split(" Five policies rely on")[1])

p(ret(P(10), ("(Table 2)", "(Table 3)")))

B.append(("cap", "Table 3. Policies to re-attract former teachers, by main "
          "instrument"))
B.append(("sub", "Country or economy, policy and period, target group, "
          "instruments used and scale of implementation"))
B.append(("table", "T2"))
for b in V5:
    if b[0] == 'src' and (b[1].startswith('Note: ● main') or
                          b[1].startswith('Source: Legal texts')):
        B.append(b)

p("We acknowledge the considerable diversity of the education systems "
  "reviewed, which operate at national, regional and local levels. For the "
  "sake of simplicity, the name of the country is used even when a policy "
  "applies only at a subnational level, and where this is the case it is "
  "indicated in the tables and boxes. Furthermore, the policies showcased "
  "in the boxes are not intended to reflect the most prevalent approach in "
  "each country. They were selected to illustrate the instruments described "
  "in the framework and to cover a variety of education systems and "
  "continents, and they should not be read as representative of the "
  "national system in which they operate.")

h3("Objectives of the policies")
for i in (5, 6, 7):
    p(P(i))

h3("Duration and take-up")
for i in (17, 18, 19):
    p(P(i))

h3("Available evidence")
p(ret(P(21), ("(Table 3)", "(Table 4)")))
p(P(22))
B.append(("cap", "Table 4. Evaluations of policies to re-attract former "
          "teachers"))
B.append(("sub", "Type of evidence, data and main results, by instrument"))
B.append(("table", "T3"))
for b in V5:
    if b[0] == 'src' and (b[1].startswith('Note: Effect sizes') or
                          b[1].startswith('Source: Georgia Department')):
        B.append(b)

# ======================================================================
h2("3.2 Financial incentives")

p("This type of policy is designed to make the return to teaching "
  "worthwhile in economic terms, and it is addressed almost exclusively to "
  "retired teachers. Its core rationale is that, for retired teachers, the "
  "decision to return to the classroom depends less on the salary on offer "
  "than on what happens to their pension once they accept it (Box 1). The "
  "approach is present in most of the systems reviewed, such as France, "
  "Georgia (depicted in Box 2), Ireland, Lower Saxony, Ontario and Quebec "
  "(depicted in Box 3), and it tends to respond to shortages of substitutes "
  "or of teachers in specific subjects. The policies take two forms. The "
  "most common modifies the rules that govern the combination of a pension "
  "with a salary, so that retired teachers can work again without losing "
  "all or part of their pension, while a smaller group offers direct "
  "payments, either to the teachers who return or to the schools that hire "
  "them.")

h3("Rules on combining a pension with a salary")
p(ret(P(31), ("Table 4 compares", "Table 5 compares")))
for i in (32, 33, 34, 35, 36):
    p(P(i))

B.append(("cap", "Table 5. Rules on combining a pension with a salary for "
          "retired teachers in selected systems"))
B.append(("sub", "Eligibility, limits on work or earnings, posts covered "
          "and treatment of pension contributions"))
B.append(("table", "T4"))
for b in V5:
    if b[0] == 'src' and (b[1].startswith('Note: .. information') or
                          b[1].startswith('Source: Department of Education (2026)')):
        B.append(b)

box("Box 2. Full return in high-need subjects in Georgia (United States)", [
 lab("Purpose and origins",
     "House Bill 385, in force between July 2022 and June 2026, was "
     "designed to bring experienced retired teachers back into the subjects "
     "where Georgia's school systems found it hardest to recruit. It allowed "
     "them to return to a full-time classroom post and receive a full salary "
     "on top of their full pension."),
 lab("Design and delivery",
     "Eligible teachers had retired with at least 30 years of service and "
     "had been retired for at least a year. The post had to be in one of the "
     "subjects of highest need in their region, as determined by the "
     "regional education service agency, and the employer paid both the "
     "employer and the employee contributions to the pension fund, while "
     "the returner earned no further service credit."),
 lab("Participants and take-up",
     "A state audit published in 2025 found that 635 retirees returned "
     "under the law between 2023 and 2025, a number that rose from 241 to "
     "428 a year and averaged about 350, under 1% of the state's teachers. "
     "Just over half of school systems (55%) used the law, 64% of returners "
     "went back to the system they had retired from, and in 56% of the "
     "systems that used the law the post had first been offered to a "
     "candidate who was not retired (Georgia Department of Audits and "
     "Accounts, 2025)."),
 lab("Outcomes, impact and challenges",
     "Of the retirees hired in 2023, 43% were still teaching two years "
     "later, one of the few retention figures available for returners. "
     "Strict eligibility kept the cost of the rule low but also limited its "
     "reach, and 45 of the 72 school systems that did not use the law "
     "reported that they would have done so had they found an eligible "
     "retiree (Georgia Department of Audits and Accounts, 2025). Senate Bill "
     "150, which replaced the law until June 2030, requires at least half of "
     "the returner's timetable to be in a qualifying subject, such as "
     "mathematics, science, special education or career and technical "
     "education, and lets each school system define its own areas of "
     "highest need on the basis of a five-year average of vacancies "
     "(Teachers Retirement System of Georgia, 2026)."),
 src("Source: Georgia Department of Audits and Accounts (2025), *Retired "
     "Teachers Return to Work*; Teachers Retirement System of Georgia "
     "(2026), “SB 150 FAQs”."),
])

h3("Direct payments to returners and schools")
p(P(44))
p(P(45))

box("Box 3. Experience-based pay for retired supply teachers in Quebec "
    "(Canada)", [
 lab("Purpose and origins",
     "Until 2020, a retired teacher who covered an absence in a Quebec "
     "public school was paid the flat daily rate for supply teaching and "
     "reached the salary scale only after 20 consecutive days in the same "
     "replacement. In September 2020, during the COVID-19 health emergency, "
     "a government decree modified the collective agreements so that "
     "teachers who had retired in the previous five years would be paid from "
     "the first day at the step of the scale that matched their experience "
     "and qualifications, while keeping their full pension and without "
     "paying further contributions (Conseil exécutif du Québec, 2020)."),
 lab("Design and delivery",
     "For a retiree at the top of the scale, daily pay rose from a usual "
     "maximum of about CAD 212 to about CAD 412 (Gouvernement du Québec, "
     "2022). A premium of 7.89% was added from 1 October 2021, and when the "
     "emergency measures ended with the 2021/22 school year the government "
     "chose to continue the incentives through letters of agreement signed "
     "every year with each teacher union federation outside the collective "
     "agreements. The premium stood at 7.89% until 2023/24, was split in "
     "2024/25 into 7.5% on supply work and 12.5% on contracts of three months "
     "or more, and has been limited since 2025/26 to 12.5% on contracts of "
     "one month or more. The Ministry of Education funds the measure after "
     "the fact, on the basis of the use of retired staff that school service "
     "centres report at the end of each year."),
 lab("Participants and take-up",
     "The original five-year limit was lifted, and the agreement now covers "
     "any retired teacher who is legally qualified to teach, although "
     "employers must first offer the work to the qualified staff they "
     "already employ. About 700 retirees returned in 2020/21, more than "
     "2 900 in 2022/23 and more than 5 000 in 2024/25 (Desrosiers, 2023; "
     "Le Devoir, 2025)."),
 lab("Outcomes, impact and challenges",
     "Because the payment is made only for the days actually worked, the "
     "government estimated the cost at about CAD 4 545 per retiree for each "
     "20-day replacement (Conseil exécutif du Québec, 2020). The envelope "
     "for 2026/27 is being adjusted downwards as fewer retirees are used and "
     "the 7.5% premium has been withdrawn (Ministère de l'Éducation du "
     "Québec, 2026), and the annual renegotiation leaves retirees and school "
     "service centres uncertain about the conditions that will apply from "
     "one year to the next."),
 src("Source: Conseil exécutif du Québec (2020), “Mémoire au Conseil des "
     "ministres”; Gouvernement du Québec (2022), “Opération main-d'œuvre”; "
     "Desrosiers (2023), “La prime de 12 000 $ boudée par des enseignants "
     "retraités”; Le Devoir (2025); Ministère de l'Éducation du Québec "
     "(2026), presentation to the OECD."),
])

h3("Implications for re-entry policies")
p(P(48))
p(P(49))

# ======================================================================
h2("3.3 Information and nudges")

p("This type of policy is designed to make former teachers aware of the "
  "options open to them, or simply to ask them to consider a return, "
  "through letters, telephone calls, advisers and information sessions. "
  "Its core rationale is that many former teachers would consider returning "
  "but are not asked, do not know how to do so or expect the process to be "
  "burdensome (Section 2). The letter sent by the Minister of Education of "
  "Lower Saxony in 2023 acknowledged this explicitly, noting that many "
  "teachers about to retire would be willing to teach a few hours a week "
  "but were deterred by the bureaucracy involved (Niedersächsisches "
  "Kultusministerium, 2023). The approach is present in Austria, England, "
  "Japan (depicted in Box 6), Lower Saxony (depicted in Box 4) and New "
  "South Wales (depicted in Box 5), and it is among the least expensive "
  "instruments available to governments.")

h3("Outreach to retired teachers")
p(P(53))
p(P(54))

box("Box 4. A combined approach for teachers approaching retirement in "
    "Lower Saxony (Germany)", [
 lab("Purpose and origins",
     "Lower Saxony, a federal state of Germany, has combined financial, "
     "informational and administrative measures aimed at teachers who are "
     "about to retire, as part of a broader set of measures to improve the "
     "staffing of its schools. A retired civil-service teacher working for "
     "the state used to have the pension reduced once the pension and the "
     "new salary together exceeded 125% of the pensionable pay. In "
     "October 2022 the state parliament raised this ceiling to 150% for two "
     "years, which allowed a pensioner to teach nine to ten lessons a week "
     "on average without any reduction, and in October 2024 it abolished the "
     "ceiling for teachers who have reached the statutory retirement age, "
     "while those who retire early remain subject to it "
     "(Niedersächsischer Landtag, 2024)."),
 lab("Design and delivery",
     "On 1 November 2023, the Minister of Education wrote to every teacher "
     "about to retire, whether a civil servant or a salaried employee, to "
     "explain how to continue teaching. A civil servant can ask to postpone "
     "retirement by up to three years, and any teacher can be re-employed "
     "on a fixed-term contract immediately after retiring while drawing the "
     "pension. The letter was addressed to teachers approaching retirement "
     "partly because the ministry no longer held the personnel files of "
     "those who had already retired, and school principals were also asked "
     "to approach these teachers in person (Niedersächsisches "
     "Kultusministerium, 2023). A teacher who continues at the same school "
     "does not need to apply through the online recruitment system or to "
     "provide a new police certificate, and contact persons in each of the "
     "four regional school authorities advise retirees and handle the "
     "procedure."),
 lab("Participants and take-up",
     "The number of teachers past retirement age working on fixed-term "
     "contracts rose from 229 in 2020 to 437 in 2024 (Niedersächsischer "
     "Landtag, 2025). According to the ministry, the first contact takes "
     "place about six months before retirement, and most returners stay at "
     "or return to the school where they last taught, usually part-time and "
     "in a specific subject such as mathematics, and rarely as class "
     "teachers or formal mentors."),
 lab("Outcomes, impact and challenges",
     "The funding for these posts must be additional, so that retirees do "
     "not take positions from young teachers. The state has no unique "
     "teacher identifier with which individual careers could be followed, "
     "which limits any assessment of how long returners stay."),
 src("Source: Niedersächsischer Landtag (2024), Drucksache 19/5338; "
     "Niedersächsischer Landtag (2025), Drucksache 19/8802; "
     "Niedersächsisches Kultusministerium (2023), “Schreiben an angehende "
     "Pensionärinnen und Pensionäre”; information provided by the Lower "
     "Saxony Ministry of Education."),
])

h3("Outreach to recent leavers and licence holders")
p(P(57))
p(P(58))

box("Box 5. Outreach to recent leavers in New South Wales (Australia)", [
 lab("Purpose and origins",
     "In November 2023, the Department of Education of New South Wales, an "
     "Australian state, began to contact teachers who had left its schools "
     "in the previous five years, shortly after the largest pay rise for "
     "the state's teachers in decades took effect. The rise, effective from "
     "October 2023, raised the starting salary from AUD 75 791 to "
     "AUD 85 000 and was accompanied by a reduction in administrative "
     "workload (NSW Government, 2023)."),
 lab("Design and delivery",
     "The department contacted more than 1 500 former teachers and asked "
     "them to consider returning. Those interested were offered a simpler "
     "re-employment process and help with their accreditation, their "
     "approval to teach and the working-with-children check, before being "
     "placed in casual or temporary work, with permanent posts and "
     "small-group tutoring roles also available."),
 lab("Participants and take-up",
     "By May 2024, more than 260 former teachers had expressed interest and "
     "145 had been matched with schools, about 60% of them returning from "
     "retirement (NSW Government, 2024)."),
 lab("Outcomes, impact and challenges",
     "Teacher vacancies in the state fell from a peak of 3 311 in 2022 to "
     "1 294 in February 2025 (NSW Government, 2025), although the "
     "contribution of returners to that fall is not known. Because the "
     "campaign coincided with better pay and a lighter administrative load, "
     "its results cannot be separated from those of the wider improvement "
     "in working conditions."),
 src("Source: NSW Government (2023), “NSW teachers to receive largest pay "
     "rise in decades”; NSW Government (2024), “Retired teachers return to "
     "classrooms”; NSW Government (2025), “Teacher vacancies drop under "
     "Minns Labor Government”."),
])

box("Box 6. Information sessions for teaching licence holders in Japan", [
 lab("Purpose and origins",
     "In Japan, students at any accredited university can obtain a teaching "
     "licence after a practicum of three to four weeks, and many licence "
     "holders never teach or leave the profession early, which has produced "
     "a large pool of potential teachers. On 1 May 2025, schools were short "
     "of 3 827 teachers, against 2 065 in 2021 (MEXT, 2026). The Ministry of "
     "Education, Culture, Sports, Science and Technology (MEXT) encourages "
     "boards of education to bring licence holders into schools and funded "
     "such initiatives with JPY 500 million in 2024."),
 lab("Design and delivery",
     "The session organised by the Miyazaki Prefectural Board of Education "
     "on 15 November 2025 illustrates what licence holders are told. It "
     "described a teacher's working day today, team-based pupil guidance, "
     "the rest days introduced in club activities and the professional "
     "development on offer, and presented the posts available without "
     "passing the competitive recruitment examination. Temporary full-time "
     "teachers start at JPY 241 900 a month, part-time teachers work up to "
     "680 hours a year at JPY 2 860 an hour, and school support staff work "
     "up to 800 hours a year at about JPY 1 000 an hour. The session ended "
     "with individual consultations and the registration of participants as "
     "temporary teachers, so that the prefecture can call on them when a "
     "vacancy appears (Miyazaki Prefectural Board of Education, 2025)."),
 lab("Participants and take-up",
     "In 2023, 50 of the 68 prefectural and city boards of education "
     "organised sessions or training for licence holders who were not "
     "teaching. In Saitama, seven seminars held that year attracted 226 "
     "participants, of whom 122 registered for temporary or part-time posts "
     "and 53 had been appointed by April 2024, while in Osaka 69 people took "
     "part in 2022 and 19 were appointed (MEXT, 2024)."),
 lab("Outcomes, impact and challenges",
     "These sessions are built around the doubts that keep licence holders "
     "away from schools, such as the fear of being out of date, the workload "
     "and the lack of readiness for a permanent post, and they rely on "
     "flexible posts rather than on financial incentives. Results are "
     "reported only for a few boards."),
 src("Source: MEXT (2024), “Case collection on training for "
     "teaching-licence holders not currently teaching”; MEXT (2026), "
     "“Results of the survey on the shortage of teachers, fiscal year "
     "2025”; Miyazaki Prefectural Board of Education (2025), “Information "
     "session on the appeal of teaching”, translated by M. Kikuchihara."),
])

h3("Implications for re-entry policies")
p(P(62))

# ======================================================================
h2("3.4 Support and training")

p("This type of policy is designed to reduce the practical cost of "
  "returning through refresher courses, supervised time in classrooms, "
  "coaching and induction. Its core rationale is that former teachers who "
  "have been away for some years often doubt that they are still up to "
  "date with curricula, assessment and classroom practice, and that schools "
  "may share those doubts when they consider their applications. The "
  "approach is present in England (depicted in Box 7), Sweden, the canton "
  "of Zurich and Victoria (depicted in Box 8), and it is addressed mainly "
  "to switchers and leavers, who have usually been away from schools for "
  "longer than retired teachers. The evidence on its results is the least "
  "encouraging of the five instruments.")

h3("Refresher programmes")
p(P(66))
p(P(67))

box("Box 7. The Return to Teaching pilot in England (United Kingdom)", [
 lab("Purpose and origins",
     "Between January and October 2016, the Department for Education "
     "funded 60 partnerships of schools to support qualified teachers "
     "returning to secondary subjects in shortage, with a target of 3 000 "
     "registrations."),
 lab("Design and delivery",
     "The support was free for the returner and covered subject knowledge, "
     "updates on assessment and behaviour management, classroom experience "
     "and mentoring, delivered by the schools in each partnership."),
 lab("Participants and take-up",
     "The pilot attracted 5 729 registrations, but only 354 registrants "
     "received support, and by November 2016, 62 of them were teaching in a "
     "state school and 27 held a permanent post in the targeted subjects. "
     "The cost per additional returner was about GBP 37 400, close to the "
     "cost of training a new teacher, and the independent evaluation judged "
     "the pilot unlikely to represent good value for money (Buchanan et al., "
     "2018)."),
 lab("Outcomes, impact and challenges",
     "The evaluation identified several reasons why so few registrants "
     "returned. Support began in January, when few posts for the following "
     "September remained open, and many schools hesitated to give returners "
     "teaching practice, citing the need to establish their quality and the "
     "risk of disrupting lessons, with the result that only 44% of returners "
     "felt that their needs had been met. Half of the returners and schools "
     "interviewed reported that returners were looking for part-time work, "
     "which few schools offered. Interest in returning was therefore not the "
     "binding constraint, since most of the losses occurred at the later "
     "stages, when support had to turn into a post."),
 src("Source: Buchanan, E. et al. (2018), *Evaluation of the Return to "
     "Teaching Pilot Programme*."),
])

h3("Induction and placements in schools")
p(P(70))

box("Box 8. Paid school placements for former teachers in Victoria "
    "(Australia)", [
 lab("Purpose and origins",
     "Victoria, an Australian state, launched its Teacher Re-Engagement "
     "Initiative in late 2022 to help qualified teachers who had left the "
     "profession to return to government schools."),
 lab("Design and delivery",
     "Registered teachers who have been away from teaching for at least "
     "12 months are offered a paid placement of up to 40 days in a "
     "government school, during which they observe classes and school "
     "routines and are mentored by serving staff, before they apply for a "
     "post. A central team matches participants with schools according to "
     "their subject, experience, location and availability, and records at "
     "the end of the placement whether the participant has returned to "
     "teaching."),
 lab("Participants and take-up",
     "The initiative attracted more than 1 100 expressions of interest and "
     "received AUD 12 million in the 2023/24 state budget (Victorian "
     "Government, 2023). It is now funded by the schools that host a "
     "returner, at a cost of AUD 330 a day that covers the participant's "
     "honorarium and the administrative costs (Victorian Government, "
     "2026)."),
 lab("Outcomes, impact and challenges",
     "No figures have been published on the number of participants who went "
     "on to teach. A supervised placement responds at the same time to the "
     "returner's lack of confidence and to the school's uncertainty about "
     "the returner, the two obstacles identified in England (Box 7), but "
     "shifting its cost to schools may limit its use to those that can "
     "afford it."),
 src("Source: Victorian Government (2023), “Ensuring a strong, sustainable "
     "and supported school workforce”; Victorian Government (2026), "
     "“Teacher Re-Engagement Initiative”."),
])

h3("Implications for re-entry policies")
p(P(73))

# ======================================================================
h2("3.5 Flexible positions")

p("This type of policy offers former teachers roles other than a full-time "
  "teaching post, such as relief teaching, which provides short-term cover "
  "for absent teachers, adjunct teaching, tutoring and mentoring. Its core "
  "rationale is that many former teachers would come back to schools, but "
  "not to a full-time post. As discussed in Section 2, leavers with care "
  "responsibilities and retirees often prefer to work only part of the "
  "week, and half of the returners and schools interviewed in the "
  "evaluation of the English pilot reported a demand for part-time work "
  "that few schools were able to meet (Buchanan et al., 2018). The approach "
  "is present in the Bahamas, China (depicted in Box 10), Singapore "
  "(depicted in Box 9), Spain and the United States (depicted in Box 11), "
  "and it also allows education systems to use the experience of former "
  "teachers where it is most valuable.")

h3("Pools of flexible teachers")
p(P(77))

box("Box 9. A standing pool of adjunct teachers in Singapore", [
 lab("Purpose and origins",
     "Singapore's Ministry of Education launched an adjunct teachers "
     "programme in 2004 to attract trained former teachers back to the "
     "profession on more flexible terms."),
 lab("Design and delivery",
     "Under the current Flexi-Adjunct Teaching Scheme, former teachers "
     "register on a ministry portal for three years, and schools contact "
     "them directly for appointments of one day to ten weeks, either for "
     "teaching alone or for teaching combined with other duties agreed with "
     "the school. Adjunct teachers are paid by the hour, at rates that depend "
     "on their experience, and earn leave once they have accumulated 90 days "
     "of service, while former teachers of the ministry must have performed "
     "well in their last three years of service to join (Ministry of "
     "Education Singapore, 2026a). A companion programme offers former "
     "ministry teachers contracts of one to one and a half years, full-time "
     "or part-time (Ministry of Education Singapore, 2026b)."),
 lab("Participants and take-up",
     "Between 2022 and 2024, about 220 teachers a year joined the programme "
     "within 12 months of leaving the service. In the same period, the annual "
     "resignation rate of teachers was 2.4%, or 1.7% if those who joined the "
     "programme are excluded (Ministry of Education Singapore, 2025a; "
     "2025b)."),
 lab("Outcomes, impact and challenges",
     "The programme keeps the system in contact with teachers at the moment "
     "they leave, before their skills and their links with schools fade. Pay "
     "at the highest rate is below 60% of the median pay package of a "
     "classroom teacher (Ministry of Education Singapore, 2024), which keeps "
     "the programme inexpensive but limits its use to occasional cover."),
 src("Source: Ministry of Education Singapore (2024; 2025a; 2025b), "
     "parliamentary replies; Ministry of Education Singapore (2026a), "
     "“Flexi-Adjunct Teaching Scheme”; Ministry of Education Singapore "
     "(2026b), “Contract Adjunct Teaching Scheme”."),
])

box("Box 10. Retired teachers in rural schools in China", [
 lab("Purpose and origins",
     "China's Silver-Age Lecturing Plan was launched in 2018 by the "
     "Ministries of Education and Finance to strengthen rural primary and "
     "lower secondary schools in poor, ethnic minority and border counties "
     "with the experience of retired teachers."),
 lab("Design and delivery",
     "The plan recruits retired principals, teaching researchers and senior "
     "teachers, generally aged 65 or under, to serve for at least a school "
     "year in these schools, and returning to one's own former school is not "
     "allowed. Participants teach classes, observe lessons and give "
     "demonstration lessons, coach the young teachers of the school and help "
     "with its management, and since 2024 retired principals may serve as "
     "deputy heads. They keep their pension and receive CNY 20 000 a year to "
     "cover living costs, travel and insurance, an amount paid by the central "
     "government in western provinces, shared between central and provincial "
     "governments in central provinces and paid by the provinces themselves "
     "in the east (Ministry of Education and Ministry of Finance of the "
     "People's Republic of China, 2018)."),
 lab("Participants and take-up",
     "The first plan set a target of 10 000 places for the period 2018 to "
     "2020, and more than 20 000 retired teachers had been recruited to "
     "primary and secondary schools by mid-2023 (Ministry of Education of "
     "the People's Republic of China, 2023). Recent annual rounds have "
     "planned between 6 000 and 7 000 places."),
 lab("Outcomes, impact and challenges",
     "The 2026 round places the coaching of young teachers at the centre of "
     "the role and introduces an assessment by the host school at the end of "
     "each placement (Ministry of Education of the People's Republic of "
     "China, 2026), which may provide the first systematic information on "
     "the results of the plan."),
 src("Source: Ministry of Education and Ministry of Finance of the People's "
     "Republic of China (2018), Jiaoshi [2018] No. 7; Ministry of Education "
     "of the People's Republic of China (2023; 2026)."),
])

h3("Mentoring and tutoring")
p(P(81))

box("Box 11. Experimental evidence on retired teachers as mentors and "
    "tutors in the United States", [
 [("Mentoring new teachers. ", "b"), (V5[82][2][0][1][0], "")],
 [("Tutoring in mathematics. ", "b"), (V5[82][2][1][1][0], "")],
 [("Tutoring in reading. ", "b"), (V5[82][2][2][1][0], "")],
 V5[82][2][3],
])

h3("Implications for re-entry policies")
p(P(84))

# ======================================================================
h2("3.6 Flexible re-certification")

p("This type of policy lowers the regulatory requirements that a former "
  "teacher must meet to teach again. Its core rationale is that, although "
  "licensing requirements play a minor part in the decision to leave "
  "teaching (Section 2), a teacher who has been away for several years may "
  "need to renew a lapsed licence or complete a refresher programme before "
  "teaching again, a process that can take months and involve costs "
  "precisely when a school is waiting to fill a post. The approach is "
  "present in New Zealand (depicted in Box 12) and Virginia, and in lighter "
  "forms in several of the policies described in previous sections.")

p(P(87))

box("Box 12. A school-based return-to-practice plan in New Zealand", [
 lab("Purpose and origins",
     "To renew a practising certificate, a teacher in New Zealand must have "
     "at least two years of satisfactory teaching in the previous five. "
     "Teachers who did not meet this requirement used to complete an "
     "external refresher programme, the Teacher Education Refresh, before "
     "returning. Since September 2024, the Teaching Council has allowed "
     "returners with a job offer to replace it with a return-to-practice "
     "plan, and in December 2025 it made this route permanent from January "
     "2026 under the name Kia Maia (Teaching Council of Aotearoa New "
     "Zealand, 2025)."),
 lab("Design and delivery",
     "The returner assesses, together with the principal of the school that "
     "has offered the job, what has changed since they last taught, and the "
     "plan lists at least three resources for each professional standard "
     "that the returner will use during the first 12 months back. Both sign "
     "the plan, which Council staff review without assessing the teacher's "
     "competence, and the certificate is then renewed. Without a job offer, "
     "the refresher programme is still likely to be required (Teaching "
     "Council of Aotearoa New Zealand, 2026). The government also paid the "
     "registration fees of returning teachers from October 2024, supporting "
     "352 returners by April 2025, and has covered the fees of all teachers "
     "since July 2025 with NZD 53.3 million over three years (Ministry of "
     "Education New Zealand, 2025)."),
 lab("Participants and take-up",
     "Between January and October 2026, 501 teachers renewed their "
     "certificate through Kia Maia, most of them working in primary (198) or "
     "secondary (133) schools or in early childhood education (110). Women "
     "made up 84% of users and 62% were aged 31 to 50, while only 16% were "
     "aged 61 or over (Teaching Council of Aotearoa New Zealand, "
     "unpublished), which indicates that the pathway mainly brings back "
     "mid-career teachers who had stepped away from the profession."),
 lab("Outcomes, impact and challenges",
     "Linking the renewal of the certificate to a job offer removes a cost "
     "and a delay at the moment when the returner is ready to start, and it "
     "involves the principal in the returner's first year, which the "
     "evidence on induction and leadership reviewed in Section 2 suggests is "
     "important for whether returners stay."),
 src("Source: Teaching Council of Aotearoa New Zealand (2025), “Introducing "
     "Kia Maia”; Teaching Council of Aotearoa New Zealand (2026), “Renew "
     "after time away”; Teaching Council of Aotearoa New Zealand "
     "(unpublished), data on Kia Maia users; Ministry of Education New "
     "Zealand (2025)."),
])

h3("Implications for re-entry policies")
p(P(90))

h2("3.7 Summary of the review")
p(P(92))
B.append(copy.deepcopy(V5[93]))

# ======================================================================
TABLES = dict(_v5.TABLES)
TABLES["TC"] = {
 "widths": (1500, 2250, 1900, 3410),
 "size": 16,
 "style": "torres",
 "first_bi": True, "italic_cols": (2,),
 "head": [[("Instrument", 1, 1), ("Definition", 1, 1), ("Categories", 1, 1),
           ("Category description", 1, 1)]],
 "rows": [
  ("Financial incentives", "Change the economic return to teaching for former teachers who come back.",
   "Rules on combining pension and salary", "Waivers, higher or abolished earnings ceilings, shorter waiting periods or full returns in shortage posts that allow retirees to teach while keeping their pension."),
  (None, None, "Direct payments to returners", "Salary steps, premiums, allowances or fees paid to the teachers who return."),
  (None, None, "Payments to schools", "Grants to the schools or employers that hire returners."),
  ("Information and nudges", "Make former teachers aware of the options to return or prompt them to consider it.",
   "Outreach to retired teachers", "Letters and contact through principals addressed to teachers about to retire or already retired."),
  (None, None, "Outreach to recent leavers", "Calls or campaigns addressed to teachers who left in recent years, often with help to return."),
  (None, None, "Advisory services and information sessions", "Advisers or sessions that explain how to return and which posts are available."),
  ("Support and training", "Reduce the practical cost of returning by updating skills and building confidence.",
   "Refresher programmes", "Courses, online or school-based, on the changes in curricula, assessment and practice."),
  (None, None, "Supervised placements and induction", "Paid time in a school, mentoring or induction during the first months back."),
  ("Flexible positions", "Offer roles other than a full-time teaching post.",
   "Pools of relief and adjunct teachers", "Registers of former teachers whom schools can hire for short or part-time appointments."),
  (None, None, "Placements in hard-to-staff schools", "Fixed-term placements of returners in schools with staffing difficulties."),
  (None, None, "Mentoring and tutoring", "Roles supporting new teachers, student teachers or pupils who are falling behind."),
  ("Flexible re-certification", "Lower the regulatory requirements to teach again.",
   "Re-certification linked to a job offer", "Renewal of the licence through a plan agreed with the employing school instead of an external course."),
  (None, None, "Simplified licensing and checks", "Reissue of lapsed licences, waived documents or faster checks of records and accreditation."),
 ]}
for k in ("T2", "T3", "T4"):
    TABLES[k] = dict(TABLES[k], style="torres")
REFS = _v5.REFS
