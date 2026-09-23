// Didactic tech slides v3: slide 1 = NATIVE editable codes crosswalk;
// slides 2-6 = full-bleed panels from tech7.py.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const SC = "/tmp/claude-0/-home-user-Alternative-Pathways----Quant/37b5ad96-b2b0-50d1-9e4b-6301ff28b789/scratchpad";
const GARA = "Garamond";
const BLUE = "00549F", CORAL = "B5443C", GREEN = "3A8A62", GOLD = "C08A17",
      GRAY = "5E6672", INK = "1A2430", MUT = "6B7480";

// ============ slide 1: native, editable crosswalk ============
{
const s = pres.addSlide();
s.background = { color: "FFFFFF" };
s.addText("Who counts as a teacher", {
  x: 0.55, y: 0.32, w: 12.2, h: 0.55, margin: 0, fontFace: GARA,
  fontSize: 26, bold: true, color: INK, valign: "middle" });
s.addText("By the Census occupation code — the code the Census Bureau assigns to the occupation of the longest job held last year (CPS ASEC)", {
  x: 0.55, y: 0.90, w: 12.2, h: 0.35, margin: 0, fontFace: GARA,
  fontSize: 12.5, italic: true, color: MUT });

const XCOL = [1.85, 5.68, 9.51], WCOL = 3.55;
const HEADS = [["Surveys 1998–2002", "Census occupation classification of 1990"],
               ["Surveys 2003–2019", "Census occupation classification of 2002/2010 (SOC)"],
               ["Surveys 2020–2025", "Census occupation classification of 2018"]];
for (let i = 0; i < 3; i++) {
  s.addText(HEADS[i][0], { x: XCOL[i], y: 1.42, w: WCOL, h: 0.3, margin: 0,
    fontFace: GARA, fontSize: 13, bold: true, color: INK, align: "center" });
  s.addText(HEADS[i][1], { x: XCOL[i], y: 1.70, w: WCOL, h: 0.3, margin: 0,
    fontFace: GARA, fontSize: 9, italic: true, color: MUT, align: "center" });
}
const LANES = [
  ["Pre-K &\nkindergarten", GOLD, "FBFBF8",
   [["155", "Teachers, prekindergarten and kindergarten"],
    ["2300", "Preschool and kindergarten teachers"],
    ["2300", "Preschool and kindergarten teachers"]]],
  ["Elementary\n& middle †", BLUE, "F8FAFC",
   [["156", "Teachers, elementary school †"],
    ["2310", "Elementary and middle school teachers"],
    ["2310", "Elementary and middle school teachers"]]],
  ["Secondary", GREEN, "F8FBF9",
   [["157", "Teachers, secondary school †"],
    ["2320", "Secondary school teachers"],
    ["2320", "Secondary school teachers"]]],
  ["Special\neducation", CORAL, "FBF8F8",
   [["158", "Teachers, special education"],
    ["2330", "Special education teachers"],
    ["2330", "Special education teachers"]]],
  ["Other\nteachers", GRAY, "F8F9FA",
   [["159", "Teachers, n.e.c. (not elsewhere classified)"],
    ["2340", "Other teachers and instructors"],
    ["2360", "Other teachers and instructors"]]],
];
const Y0 = 2.10, HR = 0.72, GAPR = 0.15;
LANES.forEach((lane, r) => {
  const [lab, c, tint, cells] = lane;
  const y = Y0 + r * (HR + GAPR);
  s.addText(lab, { x: 0.25, y: y, w: 1.45, h: HR, margin: 0, fontFace: GARA,
    fontSize: 11, bold: true, color: c, align: "right", valign: "middle" });
  cells.forEach((cell, i) => {
    const [code, title] = cell;
    s.addShape(pres.ShapeType.roundRect, { x: XCOL[i], y: y, w: WCOL, h: HR,
      rectRadius: 0.07, fill: { color: tint }, line: { color: "C9CFD6", width: 0.75 } });
    s.addText(code, { x: XCOL[i] + 0.12, y: y, w: 0.75, h: HR, margin: 0,
      fontFace: GARA, fontSize: 15, bold: true, color: c, valign: "middle" });
    s.addText(title, { x: XCOL[i] + 0.92, y: y, w: WCOL - 1.05, h: HR, margin: 0,
      fontFace: GARA, fontSize: 9.5, color: INK, valign: "middle" });
    if (i < 2)
      s.addShape(pres.ShapeType.line, { x: XCOL[i] + WCOL, y: y + HR/2,
        w: XCOL[i+1] - XCOL[i] - WCOL, h: 0, line: { color: "C9CFD6", width: 0.75 } });
  });
});
const YB = Y0 + 5 * (HR + GAPR) - GAPR;
for (let i = 0; i < 2; i++) {
  const xm = (XCOL[i] + WCOL + XCOL[i+1]) / 2;
  s.addShape(pres.ShapeType.line, { x: xm, y: 1.42, w: 0, h: YB - 1.42,
    line: { color: "B9C0C8", width: 0.75, dashType: "dash" } });
  s.addText(i === 0 ? "2003 reclassification" : "2020 reclassification",
    { x: xm - 0.9, y: YB + 0.02, w: 1.8, h: 0.24, margin: 0, fontFace: GARA,
      fontSize: 8.5, color: MUT, align: "center" });
}
s.addText([
  { text: "Traceable as a block:  ", options: { fontFace: GARA, fontSize: 10.5, bold: true, color: INK } },
  { text: "the K–12 teaching group maps one-to-one across the three classifications — every figure uses the union, never a sub-code across regimes.",
    options: { fontFace: GARA, fontSize: 10.5, color: INK, breakLine: true, paraSpaceAfter: 4 } },
  { text: "† ", options: { fontFace: GARA, fontSize: 9.5, bold: true, color: MUT } },
  { text: "middle-school teachers sit under elementary or secondary before 2003, with elementary (2310) after.      ",
    options: { fontFace: GARA, fontSize: 9.5, color: MUT } },
  { text: "Never included: postsecondary (2200s) · tutors (2350) · teaching assistants (2540/2545) · childcare workers (4600) · administrators (0230).",
    options: { fontFace: GARA, fontSize: 9.5, color: MUT } },
], { x: 0.55, y: YB + 0.34, w: 12.2, h: 0.85, margin: 0, valign: "top" });
}

// ============ slides 2-6: panels ============
for (const f of ["u2_identity", "u3_eight", "u3b_examples", "u4_twodefs"]) {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addImage({ path: `${SC}/${f}.png`, x: 0, y: 0, w: 13.33, h: 7.5 });
}

pres.writeFile({ fileName: "tech_slides_v3.pptx" }).then(() => console.log("written"));
