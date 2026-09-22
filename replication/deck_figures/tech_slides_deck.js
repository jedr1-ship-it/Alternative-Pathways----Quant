// Technical appendix slides, minimalist booktabs style, Garamond.
// Slide 1: teacher occupation codes.  Slide 2: how the CPS is read.
// Slide 3: where records are linked.  Slide 4: all months vs the March question.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

const BLUE = "00549F", INK = "1A2430", MUT = "6B7480", RED = "B5443C", GREEN = "3A8A62";
const GARA = "Garamond";
const L = 0.75, W = 11.83;

function newSlide(title) {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText(title, { x: L, y: 0.45, w: W, h: 0.55, margin: 0, align: "left",
    valign: "middle", fontFace: GARA, fontSize: 26, bold: true, color: INK });
  s.rule = (y, wpt) => s.addShape(pres.ShapeType.line,
    { x: L, y: y, w: W, h: 0, line: { color: INK, width: wpt } });
  return s;
}
const T = (t, o) => ({ text: t, options: Object.assign({ fontFace: GARA }, o) });

// ============================== Slide 1: codes ==============================
{
const s = newSlide("Who Counts as a Teacher");
s.rule(1.62, 1.4);
const XS = [L, L + 4.23, L + 8.46];
const HEADS = [
  ["Surveys 1998–2002", "1990 Census classification"],
  ["Surveys 2003–2019", "2002/2010 Census classification (SOC)"],
  ["Surveys 2020–2025", "2018 Census classification (SOC 2018)"],
];
for (let i = 0; i < 3; i++) {
  s.addText([
    T(HEADS[i][0], { fontSize: 14, bold: true, color: INK, breakLine: true }),
    T(HEADS[i][1], { fontSize: 10.5, italic: true, color: MUT }),
  ], { x: XS[i], y: 1.74, w: 4.0, h: 0.62, margin: 0, align: "left", valign: "top" });
}
s.rule(2.48, 0.75);
const ROWS = [
  [["155", "Teachers, prekindergarten and kindergarten"],
   ["156", "Teachers, elementary school†"],
   ["157", "Teachers, secondary school†"],
   ["158", "Teachers, special education"],
   ["159", "Teachers, n.e.c. (not elsewhere classified)"]],
  [["2300", "Preschool and kindergarten teachers"],
   ["2310", "Elementary and middle school teachers†"],
   ["2320", "Secondary school teachers"],
   ["2330", "Special education teachers"],
   ["2340", "Other teachers and instructors"]],
  [["2300", "Preschool and kindergarten teachers"],
   ["2310", "Elementary and middle school teachers†"],
   ["2320", "Secondary school teachers"],
   ["2330", "Special education teachers"],
   ["2360", "Other teachers and instructors"]],
];
for (let i = 0; i < 3; i++) {
  const runs = [];
  for (const [code, lab] of ROWS[i]) {
    runs.push(T(code + "   ", { fontSize: 11, bold: true, color: BLUE }));
    runs.push(T(lab, { fontSize: 11, color: INK, breakLine: true, paraSpaceAfter: 5 }));
  }
  s.addText(runs, { x: XS[i], y: 2.62, w: 4.18, h: 1.75, margin: 0, align: "left", valign: "top" });
}
s.rule(4.42, 1.4);
s.addText("Are the codes traceable across census years?", {
  x: L, y: 4.78, w: W, h: 0.32, margin: 0, align: "left",
  fontFace: GARA, fontSize: 13, bold: true, color: INK });
const NOTES = [
  ["Yes", GREEN, "as a block: the K–12 teaching group maps one-to-one across the three classifications — every figure uses the union of the codes, never a sub-code across regimes."],
  ["†", RED, "sub-codes are not: middle-school teachers sit under elementary or secondary before 2003 and with elementary (2310) after; “other teachers” is renumbered 2340 → 2360 in 2020."],
  ["Yes", GREEN, "within each survey: last year’s job (OCCUP) and the current job (PEIOOCC) share one classification, so no leaver/switch comparison straddles a code change (seams: 2003, 2020)."],
  ["Yes", GREEN, "for people, but only two years: the CPS links the same person across two consecutive March interviews (PERIDNUM), never longer."],
];
const nruns = [];
for (const [mark, mc, txt] of NOTES) {
  nruns.push(T(mark + "  ", { fontSize: 10, bold: true, color: mc }));
  nruns.push(T(txt, { fontSize: 10, color: INK, breakLine: true, paraSpaceAfter: 4 }));
}
s.addText(nruns, { x: L, y: 5.14, w: W, h: 1.3, margin: 0, align: "left", valign: "top" });
}

// ========================= Slide 2: how the CPS is read =====================
{
const s = newSlide("How We Read the CPS");
s.rule(1.62, 1.4);
const ROWS = [
  ["Instrument", "CPS March supplement (ASEC), 28 surveys pooled, 1998–2025 — 5,009,129 person-year records."],
  ["Teacher, year t–1", "the occupation of the longest job held last calendar year (OCCUP, the recall question) is a teaching code."],
  ["Outcome, March t", "read off the same record: still teaching (PEIOOCC), switched occupation, unemployed, or out of the labor force (A_LFSR)."],
  ["Why it works", "the recall question makes every March record a two-period panel on its own — the headline measure needs no matching at all."],
  ["Sample", "104,545 teacher-year observations; main sample (bachelor’s or higher, 18+): 85,497, with 6,931 observed exits."],
  ["Extraction", "1998–2010 fixed-width files read at the officially documented byte positions; 2011–2025 machine-readable files; ASEC supplement weights throughout."],
];
let y = 1.78;
for (const [lab, txt] of ROWS) {
  s.addText(lab, { x: L, y: y, w: 2.1, h: 0.5, margin: 0, align: "left", valign: "top",
    fontFace: GARA, fontSize: 11.5, bold: true, color: BLUE });
  s.addText(txt, { x: L + 2.3, y: y, w: W - 2.3, h: 0.55, margin: 0, align: "left", valign: "top",
    fontFace: GARA, fontSize: 11.5, color: INK });
  y += 0.62;
}
s.rule(y - 0.06, 1.4);
s.addText([
  T("One instrument for every flow:  ", { fontSize: 11, bold: true, color: INK }),
  T("the same design, run on the same files, yields the leaving rate of any profession, sector, state or demographic group — so every comparison in this deck is internally consistent.",
    { fontSize: 11, color: INK }),
], { x: L, y: y + 0.25, w: W, h: 0.6, margin: 0, align: "left", valign: "top" });
}

// ==================== Slide 3: where records are linked =====================
{
const s = newSlide("Where Records Are Linked, and What It Costs");
s.rule(1.62, 1.4);
const XS = [L, L + 2.75, L + 6.05, L + 8.95];
const WS = [2.6, 3.15, 2.75, 2.88];
const HEAD = ["Link", "Keys", "Validation", "Used for"];
for (let i = 0; i < 4; i++)
  s.addText(HEAD[i], { x: XS[i], y: 1.74, w: WS[i], h: 0.3, margin: 0, align: "left",
    valign: "top", fontFace: GARA, fontSize: 12.5, bold: true, color: INK });
s.rule(2.12, 0.75);
const ROWS = [
  ["None — the headline", "recall and current status live in the same record", "—",
   "leaving rate, routes, destinations, every covariate"],
  ["March t → March t+1", "PERIDNUM; rotation 4-8-4: MIS 1–4 return next March as MIS 5–8",
   "sex, race, age advancing 0–2 years (Madrian–Lefgren)", "earnings change at the destination"],
  ["Month t → t+12 (the experiment)", "HRHHID · HRHHID2 · PULINENO, on every basic monthly file",
   "same rule", "linked monthly panel, 2005–2025"],
];
let y = 2.26;
for (const r of ROWS) {
  for (let i = 0; i < 4; i++)
    s.addText(r[i], { x: XS[i], y: y, w: WS[i], h: 0.75, margin: 0, align: "left", valign: "top",
      fontFace: GARA, fontSize: 11, color: i === 0 ? BLUE : INK, bold: i === 0 });
  y += 0.82;
}
s.rule(y - 0.1, 1.4);
const nruns = [
  T("The price of linking:  ", { fontSize: 11, bold: true, color: INK }),
  T("matched share at month t → t+12: teachers 80% · other college graduates 76% · all employed 72% · not employed 70% — the loss is non-random, and movers are exactly the people a study of leaving cares about.",
    { fontSize: 11, color: INK, breakLine: true, paraSpaceAfter: 6 }),
  T("The calendar bound:  ", { fontSize: 11, bold: true, color: INK }),
  T("the household identifier HRHHID2 exists only from May 2004, so no linked monthly panel can start before 2005 — and none can reach back to 1997. The recall design can.",
    { fontSize: 11, color: INK }),
];
s.addText(nruns, { x: L, y: y + 0.22, w: W, h: 1.3, margin: 0, align: "left", valign: "top" });
}

// =============== Slide 4: all months vs the March question ==================
{
const s = newSlide("Every Month of the CPS vs the March Question");
s.rule(1.62, 1.4);
const XS = [L, L + 4.35, L + 8.55, L + 10.0];
const WS = [4.2, 4.05, 1.3, 1.83];
const HEAD = ["Instrument", "What counts as leaving", "Years", "Rate"];
for (let i = 0; i < 4; i++)
  s.addText(HEAD[i], { x: XS[i], y: 1.74, w: WS[i], h: 0.3, margin: 0, align: "left",
    valign: "top", fontFace: GARA, fontSize: 12.5, bold: true, color: INK });
s.rule(2.12, 0.75);
const ROWS = [
  ["Linked monthly panel — every month, the same person re-interviewed twelve months later",
   "not teaching at the interview one year on", "2005–2025", "15.4%\n13.1% never return"],
  ["March recall question — the design behind this deck",
   "the main job held last year is no longer the job held now", "1997–2024", "7.7%"],
];
let y = 2.26;
for (const r of ROWS) {
  for (let i = 0; i < 4; i++)
    s.addText(r[i], { x: XS[i], y: y, w: WS[i], h: 0.85, margin: 0, align: "left", valign: "top",
      fontFace: GARA, fontSize: 11.5, color: i === 3 ? BLUE : INK, bold: i === 3 });
  y += 0.95;
}
s.rule(y - 0.12, 1.4);
const nruns = [
  T("The level tracks the instrument, not the truth.  ", { fontSize: 11.5, bold: true, color: INK }),
  T("A point-in-time re-interview counts summer detours, temporary absences and every misclassified month; the recall question counts durable exits from the main job. Published benchmarks sit on the recall side: retrospective CPS 7.6 (Aldeman–Yi 2025) · TFS roster follow-up 8.4 (2021–22) · Washington payroll 6–8.",
    { fontSize: 11.5, color: INK, breakLine: true, paraSpaceAfter: 8 }),
  T("Why we keep March — one reason only:  ", { fontSize: 11.5, bold: true, color: GREEN }),
  T("it replicates the literature’s measure, so every published benchmark is directly comparable to every number in this deck.",
    { fontSize: 11.5, color: INK }),
];
s.addText(nruns, { x: L, y: y + 0.22, w: W, h: 1.5, margin: 0, align: "left", valign: "top" });
}

pres.writeFile({ fileName: "tech_slides.pptx" }).then(() => console.log("written"));
