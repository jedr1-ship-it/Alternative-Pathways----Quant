const pptxgen = require("pptxgenjs");
const path = require("path");
const GREEN = "1F4E46", SAGE = "EAF2EE", INK = "24313A", ACCENT = "B3542E", WHITE = "FFFFFF", LINE = "CFDCD5", GREY = "8C9B95";
const HEAD = "Cambria", BODY = "Calibri", W = 13.333, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Policy slide template";
const s = pres.addSlide();
s.background = { color: WHITE };

// flag slot
s.addShape(pres.ShapeType.rect, { x: 0.5, y: 0.42, w: 1.05, h: 0.7875, fill: { color: "F4F7F5" }, line: { color: LINE, width: 1 } });
s.addText("flag", { x: 0.5, y: 0.42, w: 1.05, h: 0.7875, fontFace: BODY, fontSize: 10, color: GREY, align: "center", valign: "middle", margin: 0, isTextBox: true });
s.addText("Country", { x: 1.75, y: 0.42, w: 9.1, h: 0.5, fontFace: BODY, fontSize: 22, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
s.addText("Region or state (delete this line if the policy is national)", { x: 1.75, y: 0.92, w: 9.1, h: 0.34, fontFace: BODY, fontSize: 13, color: GREY, margin: 0, isTextBox: true });

// card
s.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.5, w: 12.33, h: 4.22, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
s.addText("Policy name, and the year or period", { x: 0.95, y: 1.7, w: 11.43, h: 0.9, fontFace: HEAD, fontSize: 21, bold: true, color: INK, margin: 0, isTextBox: true, valign: "top" });
s.addText(
  "Write four to six lines of plain prose. Open with what the policy actually does, who runs it and whom it is for, then how it works step by step, then what the returner gets. Put dates and figures at the end, and only the ones that carry the story. Do not repeat the country, the region or the policy name: they are already on the slide. Give amounts in the local currency with the approximate euro equivalent in brackets, and describe an institution before naming it, for example a national newspaper (name).",
  { x: 0.95, y: 2.64, w: 11.43, h: 2.85, fontFace: BODY, fontSize: 15, color: GREY, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.06 });
// sources + scale pill + number
s.addText([{ text: "Source: ", options: { bold: true, color: INK } }, { text: "paste the link, and add a second line 'Source (see also):' if there is another", options: { color: GREY } }],
  { x: 0.5, y: 5.8, w: 8.9, h: 0.9, fontFace: BODY, fontSize: 10, margin: 0, isTextBox: true, valign: "top" });

// the five instruments: light up the ones the policy uses, leave the rest grey
const tW = 5 * 0.52 + 4 * 0.18, tX = 12.83 - tW;
for (let i = 0; i < 5; i++) {
  const x = tX + i * 0.70;
  s.addShape(pres.ShapeType.ellipse, { x, y: 6.36, w: 0.52, h: 0.52, fill: { color: "DCE6E0" }, line: { color: "DCE6E0", width: 0 } });
  s.addText(String(i + 1), { x, y: 6.36, w: 0.52, h: 0.52, fontFace: BODY, fontSize: 10, color: GREY, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
s.addText("Switchers / Leavers / Retired", { x: 7.8, y: 6.95, w: 5.03, h: 0.28, fontFace: BODY, fontSize: 10.5, color: GREY, align: "right", margin: 0, isTextBox: true, valign: "middle" });
s.addShape(pres.ShapeType.roundRect, { x: 11.03, y: 0.42, w: 1.8, h: 0.47, fill: { color: GREY }, line: { color: GREY, width: 0 }, rectRadius: 0.235 });
s.addText("Scale", { x: 11.03, y: 0.42, w: 1.8, h: 0.47, fontFace: BODY, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
s.addText("0", { x: 0.5, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: GREY, align: "left", margin: 0, isTextBox: true });

s.addNotes([
  "Blank policy slide, same layout as the deck. Replace every grey placeholder.",
  "",
  "Flag: delete the grey box and drop in a flag image of the same size (1.05 x 0.79 inches), then put a thin light border around it.",
  "Instrument dots: the five circles at the foot are, in order, Financial incentives, Information & nudges, Support & training, Flexible positions and Flexible re-certification. Copy a lit dot from any slide of the deck over the ones this policy uses, and leave the others grey.",
  "Target groups: the grey line under the dots. Any combination of Switchers, Leavers and Retired.",
  
  "Scale: Large for a national policy, Medium for a state, region, province or canton, Small for a district, a city or a single institution. Colours: Large 1F4E46, Medium C8892B, Small B3542E.",
  "Fonts: Cambria for the title, Calibri for everything else. Text colours: 24313A and B3542E."
].join("\n"));

const out = path.join(__dirname, "Policy_slide_template.pptx");
pres.writeFile({ fileName: out }).then(() => console.log("written", out));
