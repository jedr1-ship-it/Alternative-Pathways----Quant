// Codes slide, minimalist LaTeX-table (booktabs) style, Garamond.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

const BLUE = "00549F", INK = "1A2430", MUT = "6B7480", RED = "B5443C", GREEN = "3A8A62";
const GARA = "Garamond";
const L = 0.75, W = 11.83;           // left margin, table width
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

s.addText("Who Counts as a Teacher", {
  x: L, y: 0.45, w: W, h: 0.55, margin: 0, align: "left", valign: "middle",
  fontFace: GARA, fontSize: 26, bold: true, color: INK,
});

const rule = (y, wpt) => s.addShape(pres.ShapeType.line, {
  x: L, y: y, w: W, h: 0, line: { color: INK, width: wpt },
});

// ---- booktabs table ----
rule(1.62, 1.4);                                        // \toprule

const XS = [L, L + 4.23, L + 8.46];
const HEADS = [
  ["Surveys 1998–2002", "1990 Census classification"],
  ["Surveys 2003–2019", "2002/2010 Census classification (SOC)"],
  ["Surveys 2020–2025", "2018 Census classification (SOC 2018)"],
];
for (let i = 0; i < 3; i++) {
  s.addText([
    { text: HEADS[i][0], options: { fontFace: GARA, fontSize: 14, bold: true, color: INK, breakLine: true } },
    { text: HEADS[i][1], options: { fontFace: GARA, fontSize: 10.5, italic: true, color: MUT } },
  ], { x: XS[i], y: 1.74, w: 4.0, h: 0.62, margin: 0, align: "left", valign: "top" });
}

rule(2.48, 0.75);                                       // \midrule

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
    runs.push({ text: code + "   ", options: { fontFace: GARA, fontSize: 11, bold: true, color: BLUE } });
    runs.push({ text: lab, options: { fontFace: GARA, fontSize: 11, color: INK, breakLine: true, paraSpaceAfter: 5 } });
  }
  s.addText(runs, { x: XS[i], y: 2.62, w: 4.18, h: 1.75, margin: 0, align: "left", valign: "top" });
}

rule(4.42, 1.4);                                        // \bottomrule

// ---- notes ----
s.addText("Are the codes traceable across census years?", {
  x: L, y: 4.78, w: W, h: 0.32, margin: 0, align: "left",
  fontFace: GARA, fontSize: 13, bold: true, color: INK,
});
const NOTES = [
  ["Yes", GREEN, "as a block: the K–12 teaching group maps one-to-one across the three classifications — every figure uses the union of the codes, never a sub-code across regimes."],
  ["†", RED, "sub-codes are not: middle-school teachers sit under elementary or secondary before 2003 and with elementary (2310) after; “other teachers” is renumbered 2340 → 2360 in 2020."],
  ["Yes", GREEN, "within each survey: last year’s job (OCCUP) and the current job (PEIOOCC) share one classification, so no leaver/switch comparison straddles a code change (seams: 2003, 2020)."],
  ["Yes", GREEN, "for people, but only two years: the CPS links the same person across two consecutive March interviews (PERIDNUM), never longer."],
];
const nruns = [];
for (const [mark, mc, txt] of NOTES) {
  nruns.push({ text: mark + "  ", options: { fontFace: GARA, fontSize: 10, bold: true, color: mc } });
  nruns.push({ text: txt, options: { fontFace: GARA, fontSize: 10, color: INK, breakLine: true, paraSpaceAfter: 4 } });
}
s.addText(nruns, { x: L, y: 5.14, w: W, h: 1.3, margin: 0, align: "left", valign: "top" });

pres.writeFile({ fileName: "codes_slide.pptx" }).then(() => console.log("written"));
