# Section 3, version 5: version 4 with the third review applied.
import copy
import section3_v4 as _v4

B = copy.deepcopy(_v4.B)
TABLES = _v4.TABLES
REFS = _v4.REFS

# exact replacements in paragraphs, box paragraphs and titles
R = [
 # authorial voice, as in Section 2
 ("The policies are classified according to the main instrument they use. ",
  "We group the policies according to the main instrument they use. "),
 ("This section reviews 30 of these policies,",
  "This section reviews 30 of these policies,"),
 # 3.1 objectives
 ("while Portugal allowed schools to hire recently retired teachers only for "
  "posts in shortage subjects or in under-staffed schools. China pursues the "
  "same aim through a different channel, since its Silver-Age Lecturing Plan "
  "sends retired principals and senior teachers to rural schools where "
  "vacancies are hardest to fill.",
  "while Portugal allowed schools to hire recently retired teachers for "
  "shortage posts (Section 3.2). China's Silver-Age Lecturing Plan serves "
  "the same purpose by sending retired principals and senior teachers to "
  "rural schools where vacancies are hardest to fill (Section 3.5)."),
 ("The COVID-19 pandemic gave a strong impulse to these policies, as the "
  "absence of serving teachers multiplied the need for substitutes at a "
  "time when few were available.",
  "The COVID-19 pandemic gave a strong impulse to these policies, because "
  "the absence of serving teachers multiplied the need for substitutes at a "
  "time when few were available."),
 ("Singapore pursues a related aim, since its adjunct teaching programme keeps "
  "teachers who resign in contact with schools by allowing them to work on "
  "short and flexible appointments.",
  "Singapore's adjunct teaching programme has a related aim, which is to "
  "keep teachers who resign in contact with schools by allowing them to "
  "work on short and flexible appointments."),
 # 3.1 instruments
 ("Four policies provide support and training, as in Victoria (Australia), "
  "which pays former teachers to spend several weeks in a school before "
  "they apply for a post, and the remaining two make re-certification more "
  "flexible, as New Zealand did when it allowed returners with a job offer "
  "to replace a refresher course with a plan agreed with the principal of "
  "their new school.",
  "Four policies provide support and training, such as the paid school "
  "placements offered to former teachers in Victoria (Australia), and the "
  "remaining two make re-certification more flexible, as New Zealand has "
  "done for returners who already have a job offer (Section 3.6)."),
 # 3.1 duration
 ("The Irish waiver, introduced in 2021, has been extended twice and now "
  "runs until the end of 2027, and Georgia replaced its return-to-work law "
  "when it expired in 2026 with a new one that will expire in 2030. Quebec "
  "has never made its incentives permanent and renegotiates them every "
  "school year with the teacher unions. Other policies were reversed after "
  "a short period. The Ontario Teachers' Federation, which co-sponsors the "
  "teachers' pension plan, declined in 2024 to extend the higher limit on "
  "working days, and in September 2026",
  "The Irish waiver, introduced in 2021, has been extended twice and now "
  "runs until the end of 2027, and Quebec has never made its incentives "
  "permanent and renegotiates them every school year with the teacher "
  "unions. Other policies were reversed after a short period. Ontario "
  "returned in 2024 to its usual limit on the days that retired teachers "
  "can work, and in September 2026"),
 ("In Georgia, the retirees who returned under the state's law also "
  "represented under 1% of its teachers (Georgia Department of Audits and "
  "Accounts, 2025), and in Portugal",
  "The same order of magnitude is found in Georgia (Box 2), and in "
  "Portugal"),
 # 3.1 evidence
 ("The official reviews of re-entry programmes in England, the Netherlands "
  "and Sweden, presented in Sections 3.2 and 3.4, reached less encouraging "
  "conclusions. In England interest rarely turned into actual returns, in "
  "the Netherlands most returners would have been hired in any case, and in "
  "Sweden the course offered to returners did not reach its target group.",
  "Official reviews of a refresher pilot in England, a hiring grant for "
  "schools in the Netherlands and an online course for returners in Sweden, "
  "presented in Sections 3.2 and 3.4, reached less encouraging "
  "conclusions."),
 ("The retention of returners once they are back in school is almost "
  "never measured, and Georgia, where 43% of the retirees hired in 2023 "
  "were still teaching two years later, is a rare exception.",
  "The retention of returners once they are back in school is almost "
  "never measured, and Georgia is a rare exception (Box 2)."),
 # 3.2
 ("Table 4 compares how the policies reviewed relax these rules. The "
  "simplest way of doing so, adopted in Ireland and Ontario, is to allow "
  "retirees to work a fixed number of days each year without any reduction "
  "of the pension.",
  "Table 4 compares how the policies reviewed relax these rules. Ireland "
  "and Ontario allow retirees to work a fixed number of days each year "
  "without any reduction of the pension."),
 ("Between 2020/21 and 2022/23, the provincial government and the Ontario "
  "Teachers' Federation, which jointly sponsor the teachers' pension plan, "
  "raised this limit to 95 days,",
  "Between 2020/21 and 2022/23, the provincial government and the Ontario "
  "Teachers' Federation, which jointly sponsor the teachers' pension plan, "
  "raised this limit to 95 days in each school year,"),
 ("Other systems have raised or removed the earnings ceiling for all "
  "retired teachers. In October 2022",
  "Other systems have raised or removed the earnings ceiling for all "
  "retired teachers, and they differ mainly in how long retirees must wait "
  "before returning and in whether any limit on earnings remains. In "
  "October 2022"),
 ("In the United States, Michigan shortened in 2023 the waiting period "
  "after retirement from nine to six months,",
  "In 2023 Michigan (United States) shortened the waiting period after "
  "retirement from nine to six months,"),
 ("Several US states have instead tied a full return, with a full salary "
  "and a full pension, to posts that are hard to fill. Georgia did so for "
  "teachers who had retired after at least 30 years of service, provided "
  "they returned full-time to one of the subjects of highest need in their "
  "region, and a state audit offers one of the few assessments of a rule of "
  "this kind (Box 2).",
  "Several US states have instead tied a full return, with a full salary "
  "and a full pension, to posts that are hard to fill, and the "
  "restrictions they impose largely determine how many retirees come back. "
  "Georgia tied the return to the subjects of highest need in each region "
  "(Box 2)."),
 ("North Carolina has the longest record with this approach. Between 1999 "
  "and 2009,",
  "Between 1999 and 2009,"),
 ("retired teachers could return to a full-time post and draw "
  "their salary and pension together,",
  "retired teachers in North Carolina could return to a full-time post and "
  "draw their salary and pension together,"),
 ("Portugal, by contrast, opted for a highly restrictive design. Its "
  "Decree-Law 51/2024 allowed schools to offer fixed-term contracts to "
  "teachers who had retired in the previous five years, only for posts in "
  "shortage subjects or in under-staffed schools and within an annual "
  "national quota.",
  "Portugal, by contrast, opted for a highly restrictive design. Its "
  "Decree-Law 51/2024 limited fixed-term contracts to teachers who had "
  "retired in the previous five years, to posts in shortage subjects or in "
  "under-staffed schools and to an annual national quota."),
 ("In Georgia the employer paid both the employer and the employee "
  "contributions on the salary of the returner, who earned no further "
  "pension rights, and in New Mexico, Louisiana and, since 2023, Virginia, "
  "contributions are also paid on the salary of returners without "
  "increasing their pension.",
  "In Georgia, New Mexico, Louisiana and, since 2023, Virginia, "
  "contributions are paid on the salary of returners without increasing "
  "their pension, and in Georgia the employer even paid the employee's "
  "share."),
 ("Direct payments are less common among the policies reviewed, and most "
  "of them are made to the returners themselves. The most developed "
  "example is that of Quebec, which since 2020 has paid",
  "Direct payments are less common among the policies reviewed, and most "
  "of them are made to the returners themselves. Since 2020 Quebec has "
  "paid"),
 ("The experience with financial incentives indicates, first of all, that "
  "the conditions attached to a rule matter as much as the incentive "
  "itself. Returns to Virginia's schools in the first months of the school "
  "year multiplied by eight once",
  "The experience with financial incentives carries two implications. The "
  "first is that the conditions attached to a rule matter as much as the "
  "incentive itself. Returns to Virginia's schools in the first months of "
  "the school year rose eightfold once"),
 ("These rules also raise concerns that governments need to weigh. When "
  "the Ontario Teachers' Federation refused",
  "The second is that these rules raise concerns that governments need to "
  "weigh. When the Ontario Teachers' Federation, which co-sponsors the "
  "teachers' pension plan, refused"),
 ("Payments to schools, as the Dutch grant showed, carry a different risk, "
  "which is to finance hires that would have taken place anyway.",
  "Payments to schools, as the Dutch grant showed, carry a different "
  "risk."),
 # 3.3
 ("These instruments are inexpensive and respond to a barrier identified in "
  "Section 2, since many former teachers",
  "These instruments are inexpensive and respond to a barrier identified in "
  "Section 2, as many former teachers"),
 ("Outreach has also been directed at teachers who left the profession "
  "more recently, particularly where it can be accompanied by practical "
  "help and by better working conditions. New South Wales offers the "
  "clearest example of a campaign of this kind, which the education "
  "department launched in November 2023, shortly after the state had "
  "approved the largest pay rise for its teachers in decades (Box 5). "
  "England has relied instead",
  "Outreach has also been directed at teachers who left the profession "
  "more recently, particularly where it can be accompanied by practical "
  "help and by better working conditions. In November 2023 the education "
  "department of New South Wales began to call teachers who had left its "
  "schools, offering them help to return at a time when the state was "
  "improving the pay of its teachers (Box 5). England has relied instead"),
 ("Japan faces a different situation, since its open licensing system has "
  "produced",
  "Japan faces a different situation, because its open licensing system has "
  "produced"),
 ("Although none of these initiatives has been formally evaluated, and in "
  "most cases the available data do not link returners to the contact "
  "that prompted their return, the figures available suggest that letters "
  "sent after retirement obtain a very low response.",
  "In most cases the available data do not link returners to the contact "
  "that prompted their return, but the figures available suggest that "
  "letters sent after retirement drew very few replies."),
 # 3.4
 ("England has the most extensive experience with refresher programmes. Its "
  "Return to Teaching pilot,",
  "In England, the Return to Teaching pilot,"),
 ("attracted far more interest than it could convert into posts, and its "
  "evaluation remains the most detailed assessment of a re-entry programme "
  "available (Box 7).",
  "attracted far more interest than it could turn into posts, and its "
  "evaluation remains the most detailed assessment of a re-entry programme "
  "available (Box 7)."),
 ("travel, but the programme was withdrawn without being evaluated "
  "(Department for Education, 2016).",
  "travel, until the programme was withdrawn (Department for Education, "
  "2016)."),
 ("Victoria goes further and pays former teachers to spend several weeks "
  "in a school, observing and teaching with the guidance of serving staff, "
  "before they apply for a post (Box 8).",
  "In Victoria, former teachers are paid to spend several weeks in a "
  "school, observing and teaching with the guidance of serving staff, "
  "before they apply for a post (Box 8)."),
 ("No causal evaluation of refresher or re-entry support has been found, "
  "and the retention of returners after the support ended has not been "
  "measured in any programme. The English and Swedish experiences "
  "indicate that support detached from schools and from vacancies attracts "
  "interest but produces few returns,",
  "The English and Swedish experiences indicate that support detached from "
  "schools and from vacancies attracts interest but produces few returns,"),
 ("Support of this kind is likely to convert better when it follows the "
  "recruitment calendar,",
  "Support of this kind is more likely to lead to returns when it follows "
  "the recruitment calendar,"),
 # 3.5
 ("such as relief and adjunct teaching, tutoring and mentoring.",
  "such as relief teaching, which provides short-term cover for absent "
  "teachers, adjunct teaching, tutoring and mentoring."),
 ("The simplest version of this instrument is a standing pool of former "
  "teachers whom schools can call on when they need them. Singapore has run "
  "such a programme since 2004 (Box 9).",
  "Several systems keep a standing pool of former teachers whom schools "
  "can call on when they need them, as Singapore has done since 2004 "
  "(Box 9)."),
 ("The rules on combining a pension with a salary described in Section 3.2, "
  "such as those of Ireland and Ontario, also create in practice a pool of "
  "retired substitutes.",
  "The rules on combining a pension with a salary described in Section 3.2, "
  "such as those of Ireland and Ontario, also create in practice a pool of "
  "retired substitutes. China's Silver-Age Lecturing Plan follows a "
  "different logic, since it sends returners for a whole school year to "
  "schools far from where they used to work and gives them an explicit "
  "role in developing the young teachers of those schools (Box 10)."),
 ("Flexible positions therefore reach former teachers who would not return "
  "to a full post,",
  "The experience with flexible positions shows that they reach former "
  "teachers who would not return to a full post,"),
 # 3.6
 ("New Zealand has gone furthest among the systems reviewed, replacing its "
  "refresher programme with",
  "New Zealand has replaced its refresher programme with"),
 ("No evaluation of these changes is yet available, and the data of the "
  "Teaching Council show who uses the new route in New Zealand but not "
  "whether its users would have returned through the refresher programme.",
  "The New Zealand data show who uses the new route but not whether its "
  "users would have returned through the refresher programme."),
 ("The policies reviewed in this section respond mostly to shortages and "
  "are addressed mainly to retired teachers, and only a few of them have "
  "been evaluated. Box 13 brings together what each instrument suggests "
  "for the design of re-entry policies, following the structure of Box 1.",
  "Overall, the policies reviewed respond mostly to shortages, are "
  "addressed mainly to retired teachers and have rarely been evaluated. "
  "Box 13 sets out what each instrument suggests for the design of "
  "re-entry policies."),
 # boxes
 ("The measure has not been evaluated.", ""),
 ("No formal evaluation has been carried out, and the state has no unique "
  "teacher identifier with which individual careers could be followed.",
  "The state has no unique teacher identifier with which individual "
  "careers could be followed."),
 ("No independent evaluation has been published.", ""),
 ("Research on these initiatives in Japan is still almost non-existent.", ""),
 ("The funding for these posts must be additional, in order that retirees "
  "do not take positions from young teachers.",
  "The funding for these posts must be additional, so that retirees do not "
  "take positions from young teachers."),
 ("temporary teachers, in order that the prefecture can call on them when "
  "a vacancy appears",
  "temporary teachers, so that the prefecture can call on them when a "
  "vacancy appears"),
 ("Across the three trials, a short training was enough",
  "Across the three trials, a short period of training was enough"),
 ("Letters sent after retirement obtain very low responses.",
  "Letters sent after retirement draw very few replies."),
 ("Support converts best when it follows the recruitment calendar,",
  "Support leads to returns when it follows the recruitment calendar,"),
 ("The pilot attracted 5 729 registrations, well above its target of 3 000, "
  "but only 354 registrants received support,",
  "The pilot attracted 5 729 registrations, well above its target of 3 000, "
  "but only 354 registrants received support,"),
 ("The evaluation identified several reasons for this low conversion.",
  "The evaluation identified several reasons why so few registrants "
  "returned."),
]

TITLES = {
 "Box 3. Paying retired supply teachers on their salary step in Quebec "
 "(Canada)": "Box 3. Experience-based pay for retired supply teachers in "
             "Quebec (Canada)",
 "Box 5. Contacting teachers who recently left the profession in "
 "New South Wales (Australia)": "Box 5. Outreach to recent leavers in "
                                "New South Wales (Australia)",
 "Box 12. Replacing the refresher course with a plan agreed with the "
 "school in New Zealand": "Box 12. A school-based return-to-practice plan "
                          "in New Zealand",
}

# boxes whose closing interpretive paragraph is dropped (end on the facts)
DROP_CLOSING = ("Box 3.", "Box 4.", "Box 5.", "Box 6.", "Box 8.", "Box 9.",
                "Box 10.", "Box 11.")

used = set()
def fix(t):
    for a, b in R:
        if a in t:
            t = t.replace(a, b)
            used.add(a)
    return t.replace("  ", " ").replace(" .", ".")

out = []
for blk in B:
    k = blk[0]
    if k == 'p':
        out.append(('p', fix(blk[1]).strip()))
    elif k == 'box':
        title = TITLES.get(blk[1], blk[1])
        paras = [[(fix(t), s) if s != 'src' else (t, s) for t, s in pp]
                 for pp in blk[2]]
        if title.startswith(DROP_CLOSING):
            body = [pp for pp in paras if pp[0][1] != 'src']
            srcs = [pp for pp in paras if pp[0][1] == 'src']
            paras = body[:-1] + srcs
        paras = [pp for pp in paras if ''.join(t for t, _ in pp).strip()]
        out.append(('box', title, paras))
    else:
        out.append(blk)
B = out

# merge the two-sentence China subsection into "Pools of flexible teachers"
i = next(j for j, b in enumerate(B) if b == ('h3', 'Placements in schools with staffing difficulties'))
assert B[i + 1][0] == 'p' and 'Silver-Age' in B[i + 1][1]
del B[i:i + 2]

# give the closing paragraph and Box 13 their own heading
j = next(j for j, b in enumerate(B) if b[0] == 'p' and b[1].startswith('Overall, the policies reviewed'))
B.insert(j, ('h2', '3.7 Summary of the review'))

missing = [a[:70] for a, _ in R if a not in used]
assert not missing, missing

POST = [
 ("follows a different logic, since it sends returners", "follows a different logic. It sends returners"),
 ("depends on the role assigned to returners, since the largest", "depends on the role assigned to returners, as the largest"),
 ("with demanding renewal rules, since it acts at the point", "with demanding renewal rules, because it acts at the point"),
]
def _post(t):
    for a, b in POST:
        t = t.replace(a, b)
    return t
B = [('p', _post(b[1])) if b[0] == 'p' else b for b in B]
