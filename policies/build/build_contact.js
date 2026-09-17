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
   policy: "Teachers Re-Engage (2023–24)",
   what: "The Department of Education used its own staff records to contact more than 1,500 teachers who had resigned in the previous five years and offered them fast re-accreditation and a casual or temporary post. By May 2024, 260 had shown interest and 145 were placed. Nothing has been published since.",
   why: "It is the cleanest example of a direct-outreach nudge with a published funnel from contacts to placements, and the missing pieces (cost, retention, who came back) exist in the department's records.",
   contact: "NSW Department of Education, Teach NSW / school workforce division (teachers re-engage initiative team).",
   questions: [
     "The full funnel by group: of the 1,500+ contacted, how many replied, expressed interest, were placed, and how many are still teaching 12 and 24 months later, separating retirees from those who had moved to other jobs.",
     "How the 1,500 were selected from the records (years since resignation, subject, region) and which contact channel worked best: letter, e-mail or phone call.",
     "What the streamlined re-accreditation involved in practice and how long it took a returner to be cleared to teach.",
     "Total cost of the initiative and cost per placement, including staff time.",
     "What returners asked for (casual, temporary, part-time, permanent) and what they were actually offered.",
     "Whether the initiative was discontinued, absorbed into regular recruitment or evaluated, and whether an evaluation can be shared."
   ]},
 { country: "Canada", region: "Quebec", flag: "ca", cat: "Financial incentives", groups: "Retired",
   policy: "Incentive pay for retired teachers who return (since 2020, permanent)",
   what: "Retired teachers who come back are paid from day one at the salary step they had at retirement, about 412 Canadian dollars a day (about 275 euros) instead of the 212-dollar substitute rate, while keeping the full pension. 700 retirees returned in 2020-21; more than 5,000 worked in schools in 2022-23. In 2023 the minister also wrote to every retiree.",
   why: "It is the only financial incentive for retirees running at large scale and now permanent, so the ministry can show whether money changes behaviour, at what cost, and with what side effects on active substitutes and on retirement decisions.",
   contact: "Quebec Ministry of Education, human-resources and workforce-planning branch for the school network.",
   questions: [
     "Number of retirees working each year since 2019-20 (before and after the incentive), with days worked per person and the split between substitute work and fixed-term contracts.",
     "Annual cost of paying retirees at their former salary step rather than the substitute rate, and how it compares with the cost of unfilled absences.",
     "Any sign that the incentive changed retirement timing, for example teachers retiring earlier to come back at higher pay, and whether pension rules had to be adjusted.",
     "Effects on active substitutes and early-career teachers: did retirees take work that would otherwise have gone to them?",
     "The August 2023 letter: how many were sent, how many replied, and what the retirees who did not return said.",
     "Whether the ministry has evaluated the measure or plans to, and which data could be shared for a comparative study."
   ]},
 { country: "Netherlands", region: "", flag: "nl", cat: "Financial incentives", groups: "Switchers / Leavers",
   policy: "Grant to primary schools for re-hiring former teachers (2017–2020)",
   what: "The Ministry of Education paid a primary-school board up to 2,500 euros for every qualified teacher it re-hired after at least twelve months out of primary teaching, on a contract of six months or more, to fund the returner's coaching and refresher training. The first budget covered 500 returners; the scheme closed in 2020.",
   why: "It is the only measure in our set that pays the school rather than the teacher, it is closed, so the whole story can be told, and the Netherlands has the best data on the pool of qualified teachers working outside education.",
   contact: "Dutch Ministry of Education, Culture and Science, primary-education directorate, and the ministry's subsidy agency (DUS-I) that administered the grant.",
   questions: [
     "Take-up: how many returners were actually funded in each round, out of the 500 places, and the profile of those returners (years away, sector they came from, age).",
     "Whether school boards said the grant changed their decision to hire, or mostly subsidised hires that would have happened anyway.",
     "What the 2,500 euros was typically spent on and whether the coaching or refresher training made a difference to the returner's first months.",
     "Retention: how many of the funded returners were still teaching one, two and three years later.",
     "Why the regulation was not renewed after January 2020 and whether anything replaced it, nationally or in the regional shortage plans.",
     "Any monitoring or evaluation report by OCW or DUS-I, and any later work on reaching the reserve of qualified teachers outside education."
   ]}
];

(async () => {
  const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE";
  pres.author = "José Manuel Torres, José Elías Durán Roa"; pres.title = "Three countries to contact";
  const flags = {}; for (const t of T) flags[t.flag] = await flagPng(t.flag);

  // cover
  let s = pres.addSlide(); s.background = { color: GREEN };
  s.addText("Three countries to contact", { x: 0.8, y: 1.6, w: 11.7, h: 1.1, fontFace: HEAD, fontSize: 44, bold: true, color: WHITE, margin: 0, isTextBox: true, valign: "bottom" });
  s.addText("Re-attracting former teachers: the policies we want to ask about, and what we would like to learn", { x: 0.8, y: 2.85, w: 11.7, h: 0.8, fontFace: BODY, fontSize: 20, color: "CFE3D9", margin: 0, isTextBox: true });
  s.addText("José Manuel Torres – José Elías Durán Roa  ·  September 2026", { x: 0.8, y: 4.3, w: 10, h: 0.4, fontFace: BODY, fontSize: 13, color: "CFE3D9", margin: 0, isTextBox: true });
  let fx = 0.8; for (const t of T) { s.addImage({ data: flags[t.flag], x: fx, y: 5.4, w: 1.0, h: 0.75 }); fx += 1.25; }

  // why these three
  s = pres.addSlide(); s.background = { color: WHITE };
  s.addText("Why these three", { x: 0.6, y: 0.5, w: 8, h: 0.7, fontFace: HEAD, fontSize: 32, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addText("We chose the countries we can learn most from, not the ones with the most or the least information. Each one meets three tests: the policy is real and recent, it works through a different instrument from the other two, and the questions we care about have answers sitting in the administration's own records rather than in what has been published.", { x: 0.6, y: 1.3, w: 12.1, h: 1.1, fontFace: BODY, fontSize: 14.5, color: INK, margin: 0, isTextBox: true, valign: "top" });
  let y = 2.7;
  for (const t of T) {
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 1.35, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.1 });
    s.addImage({ data: flags[t.flag], x: 0.85, y: y + 0.33, w: 0.92, h: 0.69 });
    s.addText([{ text: t.country + (t.region ? " (" + t.region + ")" : "") + ": " + t.policy, options: { bold: true, breakLine: true } }, { text: t.why }],
      { x: 2.0, y: y + 0.12, w: 10.5, h: 1.12, fontFace: BODY, fontSize: 13, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    y += 1.5;
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
    s.addShape(pres.ShapeType.roundRect, { x: 6.3, y: 1.55, w: 6.43, h: 5.2, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
    s.addText("What we would like to know", { x: 6.6, y: 1.7, w: 5.9, h: 0.45, fontFace: BODY, fontSize: 15, bold: true, color: ACCENT, margin: 0, isTextBox: true, valign: "middle" });
    s.addText(t.questions.map((q, j) => ({ text: q, options: { bullet: { indent: 14 }, breakLine: j < t.questions.length - 1, paraSpaceAfter: 6 } })),
      { x: 6.6, y: 2.2, w: 5.85, h: 4.45, fontFace: BODY, fontSize: 13, color: INK, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.04 });
    s.addText(String(i + 3), { x: W - 1.1, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: INK, align: "right", margin: 0, isTextBox: true });
    s.addNotes("Draft questions for a first contact; sources and figures as in the main deck (slide on this policy).");
  });

  // reserve list
  s = pres.addSlide(); s.background = { color: WHITE };
  s.addText("If one of the three does not answer", { x: 0.6, y: 0.5, w: 11, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: INK, margin: 0, isTextBox: true });
  const reserve = [
    ["Australia (Victoria), Teacher Re-Engagement Initiative", "Paid 40-day placements with a known budget and 1,100+ expressions of interest; conversion into jobs never published. Same contact route as New South Wales."],
    ["Germany (Lower Saxony), earnings ceiling and letter to retiring teachers", "A clean before-and-after: ceiling raised in 2022 and abolished in 2024, plus a letter campaign in 2023. Pension records would show how many hours pensioners teach."],
    ["New Zealand, streamlined return with fees covered", "352 returners counted by April 2025; the Ministry monitors the pathway and could say who returns and whether they stay."],
    ["Portugal, hiring of retired teachers (Decree-Law 51/2024)", "Low take-up (about 63 of 200 posts) is itself the lesson: why retirees did not come back despite pension plus pay."]
  ];
  y = 1.45;
  for (const [a, b] of reserve) {
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 1.15, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.1 });
    s.addText([{ text: a, options: { bold: true, breakLine: true } }, { text: b }], { x: 0.85, y: y + 0.1, w: 11.6, h: 0.95, fontFace: BODY, fontSize: 13, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    y += 1.3;
  }
  s.addText("6", { x: W - 1.1, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: INK, align: "right", margin: 0, isTextBox: true });

  const out = path.join(__dirname, "Three_countries_to_contact.pptx");
  await pres.writeFile({ fileName: out }); console.log("written", out);
})().catch(e => { console.error(e); process.exit(1); });
