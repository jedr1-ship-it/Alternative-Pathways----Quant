// Codes slide in the house deck style (Garamond, #00549F title + rule).
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

const BLUE = "00549F", INK = "1A2430", MUT = "6B7480", RED = "B5443C", GREEN = "3A8A62";
const GARA = "Garamond";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

// Title + rule, copied from the deck's geometry (x 0.9", y 0.5", rule at 1.12")
s.addText("Who Counts as a Teacher", {
  x: 0.9, y: 0.5, w: 11.5, h: 0.55, margin: 0, align: "left", valign: "middle",
  fontFace: GARA, fontSize: 26, bold: true, color: BLUE,
});
s.addShape(pres.ShapeType.line, {
  x: 0.9, y: 1.12, w: 11.53, h: 0, line: { color: BLUE, width: 1.2 },
});
s.addText(
  "Occupation of the longest job held last year (CPS ASEC) — three Census classifications, 28 survey years",
  { x: 0.9, y: 1.22, w: 11.5, h: 0.35, margin: 0, align: "left",
    fontFace: GARA, fontSize: 13, italic: true, color: MUT });

const COLS = [
  { x: 0.9,  yrs: "Surveys 1998–2002", cal: "teaching years 1997–2001",
    cls: "1990 Census classification",
    rows: [["155", "Teachers, prekindergarten and kindergarten"],
           ["156", "Teachers, elementary school†"],
           ["157", "Teachers, secondary school†"],
           ["158", "Teachers, special education"],
           ["159", "Teachers, n.e.c. (not elsewhere classified)"]] },
  { x: 5.05, yrs: "Surveys 2003–2019", cal: "teaching years 2002–2018",
    cls: "2002/2010 Census classification (SOC)",
    rows: [["2300", "Preschool and kindergarten teachers"],
           ["2310", "Elementary and middle school teachers†"],
           ["2320", "Secondary school teachers"],
           ["2330", "Special education teachers"],
           ["2340", "Other teachers and instructors"]] },
  { x: 9.2,  yrs: "Surveys 2020–2025", cal: "teaching years 2019–2024",
    cls: "2018 Census classification (SOC 2018)",
    rows: [["2300", "Preschool and kindergarten teachers"],
           ["2310", "Elementary and middle school teachers†"],
           ["2320", "Secondary school teachers"],
           ["2330", "Special education teachers"],
           ["2360", "Other teachers and instructors"]] },
];

for (const c of COLS) {
  const runs = [
    { text: c.yrs, options: { fontFace: GARA, fontSize: 15, bold: true, color: BLUE, breakLine: true } },
    { text: c.cal, options: { fontFace: GARA, fontSize: 10.5, color: MUT, breakLine: true } },
    { text: c.cls, options: { fontFace: GARA, fontSize: 10.5, italic: true, color: INK, breakLine: true, paraSpaceAfter: 8 } },
  ];
  for (const [code, lab] of c.rows) {
    runs.push({ text: code + "   ", options: { fontFace: GARA, fontSize: 10.5, bold: true, color: BLUE } });
    runs.push({ text: lab, options: { fontFace: GARA, fontSize: 10.5, color: INK, breakLine: true, paraSpaceAfter: 5 } });
  }
  s.addText(runs, { x: c.x, y: 1.7, w: 4.0, h: 2.6, margin: 0, align: "left", valign: "top" });
}

s.addText(
  "Never included (they carry their own codes, outside the set):  postsecondary teachers (2200s)  ·  " +
  "tutors (2350, 2018 cl.)  ·  teaching assistants (2540/2545)  ·  childcare workers (4600)  ·  " +
  "education administrators (0230)",
  { x: 0.9, y: 4.5, w: 11.5, h: 0.55, margin: 0, align: "left",
    fontFace: GARA, fontSize: 11, italic: true, color: MUT });

s.addText("Are the codes traceable across census years?", {
  x: 0.9, y: 5.1, w: 11.5, h: 0.35, margin: 0, align: "left",
  fontFace: GARA, fontSize: 15, bold: true, color: BLUE,
});

const NOTES = [
  ["Yes", GREEN, "as a block: the K–12 teaching group maps one-to-one across the three classifications — every figure uses the union of the codes, never a sub-code across regimes."],
  ["†", RED, "sub-codes are not: middle-school teachers sit under elementary or secondary before 2003 and with elementary (2310) after; “other teachers” is renumbered 2340 → 2360 in 2020."],
  ["Yes", GREEN, "within each survey: last year’s job (OCCUP) and the current job (PEIOOCC) share one classification, so no leaver/switch comparison straddles a code change (seams: 2003, 2020)."],
  ["Yes", GREEN, "for people, but only two years: the CPS links the same person across two consecutive March interviews (PERIDNUM), never longer."],
];
const nruns = [];
for (const [mark, mc, txt] of NOTES) {
  nruns.push({ text: mark + "  ", options: { fontFace: GARA, fontSize: 11, bold: true, color: mc } });
  nruns.push({ text: txt, options: { fontFace: GARA, fontSize: 11, color: INK, breakLine: true, paraSpaceAfter: 6 } });
}
s.addText(nruns, { x: 0.9, y: 5.5, w: 11.5, h: 1.9, margin: 0, align: "left", valign: "top" });

pres.writeFile({ fileName: "codes_slide.pptx" }).then(() => console.log("written"));
