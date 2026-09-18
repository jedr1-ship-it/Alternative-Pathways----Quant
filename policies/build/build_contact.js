const pptxgen = require("pptxgenjs");
const fs = require("fs"); const path = require("path"); const sharp = require("sharp");
const GREEN = "1F4E46", SAGE = "EAF2EE", INK = "24313A", ACCENT = "B3542E", WHITE = "FFFFFF", LINE = "CFDCD5";
const HEAD = "Cambria", BODY = "Calibri", W = 13.333, H = 7.5;

async function flagPng(code) {
  const svg = fs.readFileSync(path.join(__dirname, "node_modules/flag-icons/flags/4x3", code + ".svg"));
  return "image/png;base64," + (await sharp(svg, { density: 300 }).resize(600, 450).png().toBuffer()).toString("base64");
}
const T = [
 { country: "Australia", region: "New South Wales", flag: "au", cat: "Information & nudges", groups: "Switchers / Leavers / Retired",
   policy: "Teachers Re-Engage (since 2023)",
   what: "The Department of Education directly contacted teachers who had resigned in the previous five years and asked them to consider coming back. Those interested were offered assistance to renew their accreditation and a placement in casual or temporary work, with the possibility of moving to a permanent post later. It was launched just after teachers received one of the largest pay rises in decades and a cut in administrative work, and the department credits both with helping the returns.",
   why: "It is the cleanest example of a direct-outreach nudge with a published funnel from contacts to placements, and the missing pieces (cost, retention, who came back) exist in the department's records.",
   contact: "NSW Department of Education, Teach NSW / school workforce division (teachers re-engage initiative team).",
   questions: [
     "How did the idea of contacting former teachers directly come about, and how was it organised inside the department?",
     "What did you learn about who responds to this kind of approach, and who does not?",
     "What made it easy or hard for those who came back to settle into teaching again?",
     "Looking back, what would you keep, change or drop, and does the initiative continue in some form?"
   ]},
 { country: "Austria", region: "", flag: "at", cat: "Information & nudges", groups: "Retired",
   policy: "Regional education authorities recruit retired teachers back (2022–)",
   what: "The regional education directorates ask teachers who have retired, or are about to, to keep teaching. Vienna started by writing to recent retirees; when almost nobody replied, it had principals raise the subject personally with staff approaching retirement age, usually offering reduced hours. A teacher who returns keeps the full pension and signs a separate contract paid on the beginner's salary scale. Take-up has stayed small.",
   why: "It is the one case where a cheap nudge visibly failed and was replaced by a different one, with a 2025 academic study pointing to pension and seniority rules as the barrier: the negative lesson the other four cannot give.",
   contact: "Vienna regional education directorate (staffing unit), the Federal Ministry of Education's teacher-personnel section, and the authors of the 2025 European Journal of Teacher Education study.",
   questions: [
     "Why did you decide to approach retired teachers, and how did the different regions go about it?",
     "What did retirees say when they declined, and what convinced the few who came back?",
     "Which rules on pensions, contracts or seniority get in the way, and is anything being done about them?",
     "Do you see retired teachers as a real reserve for the future, or only as an emergency measure?"
   ]},
 { country: "Canada", region: "Quebec", flag: "ca", cat: "Financial incentives", groups: "Retired",
   policy: "Incentive pay for retired teachers who return (since 2020, permanent)",
   what: "Retired teachers who come back to the classroom are paid at the salary step they had reached when they retired, far above the ordinary substitute rate, and keep their pension in full. Introduced during the pandemic and later made permanent, the measure was reinforced by a personal letter from the minister to every retired teacher inviting them back.",
   why: "It is the only financial incentive for retirees running at large scale and now permanent, so the ministry can show whether money changes behaviour, at what cost, and with what side effects on active substitutes and on retirement decisions.",
   contact: "Quebec Ministry of Education, human-resources and workforce-planning branch for the school network.",
   questions: [
     "What led the ministry to pay returning retirees on their former salary scale, and why was it made permanent?",
     "How has the return of retirees played out in schools, for the retirees themselves, for substitutes and for school teams?",
     "What do you know about who comes back, for how long, and why others do not?",
     "How do you weigh the cost of the measure against what it delivers, and how do you see it evolving?"
   ]},
 { country: "Netherlands", region: "", flag: "nl", cat: "Financial incentives", groups: "Switchers / Leavers",
   policy: "Grant to primary schools for re-hiring former teachers (2017–2020)",
   what: "The ministry paid the school rather than the teacher. A primary-school board that hired a qualified teacher who had been out of primary education for at least a year, on a contract of six months or more, received a grant earmarked for that person's coaching and refresher training in the first months back. The scheme ran for two years and then closed.",
   why: "It is the only measure in our set that pays the school rather than the teacher, it is closed, so the whole story can be told, and the Netherlands has the best data on the pool of qualified teachers working outside education.",
   contact: "Dutch Ministry of Education, Culture and Science, primary-education directorate, and the ministry's subsidy agency (DUS-I) that administered the grant.",
   questions: [
     "What was the thinking behind paying the school rather than the returning teacher, and how did schools use the money?",
     "What did you learn about the teachers who came back through the scheme, and about those who stayed away?",
     "Why did the scheme end, and what has taken its place since?",
     "What would you advise a country thinking of a similar scheme today?"
   ]},
 { country: "United States", region: "Michigan", flag: "us", cat: "Financial incentives", groups: "Retired",
   policy: "Public Act 147 of 2023: shorter wait and no earnings cap for retirees who return",
   what: "Retired school staff can be rehired sooner and earn without limit. The waiting period after retirement fell from nine months to six; during the wait a retiree may work if earnings stay under a ceiling, and afterwards there is no earnings cap and no penalty on the pension. Passed in response to shortages, the change expires in 2028.",
   why: "A clean before-and-after in a single state, with every rehired retiree recorded by the state pension office, and a 2028 expiry that forces the state to decide, and probably to measure, whether it worked.",
   contact: "Michigan Office of Retirement Services, which administers the school employees' retirement system, and the Michigan Department of Education's educator workforce office.",
   questions: [
     "What was the reasoning behind loosening the rules for retirees, and how did the pension side and the schools side see it?",
     "How have schools and retirees actually used the new rules since they came in?",
     "Have you seen any unintended effects, on retirement decisions, on younger teachers or on the pension system?",
     "What will decide whether the rules are kept when they expire, and what would you want to know before then?"
   ]}
];

(async () => {
  const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE";
  pres.author = "José Manuel Torres, José Elías Durán Roa"; pres.title = "Five countries to contact";
  const flags = {}; for (const t of T) flags[t.flag] = await flagPng(t.flag);

  // cover
  let s = pres.addSlide(); s.background = { color: GREEN };
  s.addText("Five countries to contact", { x: 0.8, y: 1.6, w: 11.7, h: 1.1, fontFace: HEAD, fontSize: 44, bold: true, color: WHITE, margin: 0, isTextBox: true, valign: "bottom" });
  s.addText("Re-attracting former teachers: the policies we want to ask about, and what we would like to learn", { x: 0.8, y: 2.85, w: 11.7, h: 0.8, fontFace: BODY, fontSize: 20, color: "CFE3D9", margin: 0, isTextBox: true });
  s.addText("José Manuel Torres – José Elías Durán Roa  ·  September 2026", { x: 0.8, y: 4.3, w: 10, h: 0.4, fontFace: BODY, fontSize: 13, color: "CFE3D9", margin: 0, isTextBox: true });
  let fx = 0.8; for (const t of T) { s.addImage({ data: flags[t.flag], x: fx, y: 5.4, w: 1.0, h: 0.75 }); fx += 1.25; }

  // why these three
  s = pres.addSlide(); s.background = { color: WHITE };
  s.addText("Why these five", { x: 0.6, y: 0.5, w: 8, h: 0.7, fontFace: HEAD, fontSize: 32, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addText("We chose the countries we can learn most from, not the ones with the most or the least information. Each one passes three tests: the policy is real and recent, it adds a different instrument or lesson to the others, and the questions we care about have answers sitting in the administration's own records rather than in what has been published.", { x: 0.6, y: 1.25, w: 12.1, h: 0.85, fontFace: BODY, fontSize: 13.5, color: INK, margin: 0, isTextBox: true, valign: "top" });
  let y = 2.2;
  for (const t of T) {
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 0.88, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.1 });
    s.addImage({ data: flags[t.flag], x: 0.85, y: y + 0.155, w: 0.76, h: 0.57 });
    s.addText([{ text: t.country + (t.region ? " (" + t.region + ")" : "") + ": " + t.policy, options: { bold: true, breakLine: true } }, { text: t.why }],
      { x: 1.85, y: y + 0.06, w: 10.7, h: 0.76, fontFace: BODY, fontSize: 11.5, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    y += 0.98;
  }
  s.addText("2", { x: W - 1.1, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: INK, align: "right", margin: 0, isTextBox: true });

  // country slides
  T.forEach((t, i) => {
    const s = pres.addSlide(); s.background = { color: WHITE };
    s.addImage({ data: flags[t.flag], x: 0.6, y: 0.45, w: 1.05, h: 0.7875 });
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: 0.45, w: 1.05, h: 0.7875, fill: { type: "none" }, line: { color: LINE, width: 0.75 } });
    s.addText(t.country, { x: 1.85, y: 0.4, w: 6.5, h: 0.5, fontFace: BODY, fontSize: 22, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    if (t.region) s.addText(t.region, { x: 1.85, y: 0.9, w: 6.5, h: 0.34, fontFace: BODY, fontSize: 13, color: INK, margin: 0, isTextBox: true });
    s.addShape(pres.ShapeType.roundRect, { x: 8.93, y: 0.45, w: 3.8, h: 0.47, fill: { color: SAGE }, line: { color: ACCENT, width: 1 }, rectRadius: 0.235 });
    s.addText(t.cat, { x: 8.93, y: 0.45, w: 3.8, h: 0.47, fontFace: BODY, fontSize: 13.5, bold: true, color: ACCENT, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText("Target: " + t.groups, { x: 7.93, y: 0.96, w: 4.8, h: 0.3, fontFace: BODY, fontSize: 11, color: INK, align: "right", margin: 0, isTextBox: true });
    // left column
    s.addText(t.policy, { x: 0.6, y: 1.55, w: 5.3, h: 0.9, fontFace: HEAD, fontSize: 20, bold: true, color: INK, margin: 0, isTextBox: true, valign: "top" });
    s.addText(t.what, { x: 0.6, y: 2.5, w: 5.3, h: 2.3, fontFace: BODY, fontSize: 14, color: INK, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.06 });
    s.addText([{ text: "Whom to contact: ", options: { bold: true } }, { text: t.contact }], { x: 0.6, y: 4.75, w: 5.3, h: 1.2, fontFace: BODY, fontSize: 12.5, color: INK, margin: 0, isTextBox: true, valign: "top" });
    // right column card
    s.addShape(pres.ShapeType.roundRect, { x: 6.3, y: 1.55, w: 6.43, h: 3.75, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
    s.addText("What we would like to know", { x: 6.6, y: 1.7, w: 5.9, h: 0.45, fontFace: BODY, fontSize: 15, bold: true, color: ACCENT, margin: 0, isTextBox: true, valign: "middle" });
    s.addText(t.questions.map((q, j) => ({ text: q, options: { bullet: { indent: 14 }, breakLine: j < t.questions.length - 1, paraSpaceAfter: 10 } })),
      { x: 6.6, y: 2.25, w: 5.85, h: 4.4, fontFace: BODY, fontSize: 14.5, color: INK, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.04 });
    s.addText(String(i + 3), { x: W - 1.1, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: INK, align: "right", margin: 0, isTextBox: true });
    s.addNotes("Draft questions for a first contact; sources and figures as in the main deck (slide on this policy).");
  });

  // reserve list
  s = pres.addSlide(); s.background = { color: WHITE };
  s.addText("If one of the five does not answer", { x: 0.6, y: 0.5, w: 11, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: INK, margin: 0, isTextBox: true });
  const reserve = [
    ["Australia (Victoria), Teacher Re-Engagement Initiative", "Paid placements with a known budget and strong initial interest; conversion into jobs never published, and funding after mid-2025 unconfirmed. Same contact route as New South Wales."],
    ["Germany (Lower Saxony), earnings ceiling and letter to retiring teachers", "A clean before-and-after: the ceiling was raised in 2022 and abolished in 2024, with a letter campaign in between. Pension records would show how many hours pensioners now teach."],
    ["New Zealand, streamlined return with fees covered", "352 returners counted by April 2025; the Ministry monitors the pathway and could say who returns and whether they stay."],
    ["Portugal, hiring of retired teachers (Decree-Law 51/2024)", "Low take-up (about 63 of 200 posts) is itself the lesson: why retirees did not come back despite pension plus pay."],
    ["United States (New Mexico), Educational Retirees Returning to Work Act (2022)", "Every returning retiree must be approved by the Educational Retirement Board, so exact counts of applications, approvals and destinations exist; the three-year cap shows how long returners stay."]
  ];
  y = 1.35;
  for (const [a, b] of reserve) {
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 0.98, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.1 });
    s.addText([{ text: a, options: { bold: true, breakLine: true } }, { text: b }], { x: 0.85, y: y + 0.08, w: 11.6, h: 0.82, fontFace: BODY, fontSize: 12.5, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    y += 1.08;
  }
  s.addText(String(T.length + 3), { x: W - 1.1, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: INK, align: "right", margin: 0, isTextBox: true });

  const out = path.join(__dirname, "Five_countries_to_contact.pptx");
  await pres.writeFile({ fileName: out }); console.log("written", out);
})().catch(e => { console.error(e); process.exit(1); });
