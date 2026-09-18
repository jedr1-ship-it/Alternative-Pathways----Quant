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
s.addText("Country", { x: 1.75, y: 0.36, w: 6.8, h: 0.5, fontFace: BODY, fontSize: 22, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
s.addText("Region or state (delete this line if the policy is national)", { x: 1.75, y: 0.86, w: 6.8, h: 0.34, fontFace: BODY, fontSize: 13, color: GREY, margin: 0, isTextBox: true });

// instrument pill + target line
s.addShape(pres.ShapeType.roundRect, { x: 8.93, y: 0.42, w: 3.8, h: 0.47, fill: { color: SAGE }, line: { color: ACCENT, width: 1 }, rectRadius: 0.235 });
s.addText("Main instrument", { x: 8.93, y: 0.42, w: 3.8, h: 0.47, fontFace: BODY, fontSize: 13.5, bold: true, color: ACCENT, align: "center", valign: "middle", margin: 0, isTextBox: true });
s.addText("Target: Switchers / Leavers / Retired", { x: 7.93, y: 0.93, w: 4.8, h: 0.3, fontFace: BODY, fontSize: 11, color: GREY, align: "right", valign: "top", margin: 0, isTextBox: true });

// card
s.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.5, w: 12.33, h: 4.22, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
s.addShape(pres.ShapeType.ellipse, { x: 0.85, y: 1.85, w: 0.85, h: 0.85, fill: { color: "FFFFFF" }, line: { color: GREEN, width: 1.25 } });
s.addText("icon", { x: 0.85, y: 1.85, w: 0.85, h: 0.85, fontFace: BODY, fontSize: 9, color: GREY, align: "center", valign: "middle", margin: 0, isTextBox: true });
s.addText("Policy name, and the year or period", { x: 1.95, y: 1.68, w: 10.65, h: 0.95, fontFace: HEAD, fontSize: 21, bold: true, color: INK, margin: 0, isTextBox: true, valign: "top" });
s.addText(
  "Write four to six lines of plain prose. Open with what the policy actually does, who runs it and whom it is for, then how it works step by step, then what the returner gets. Put dates and figures at the end, and only the ones that carry the story. Do not repeat the country, the region or the policy name: they are already on the slide. Give amounts in the local currency with the approximate euro equivalent in brackets, and describe an institution before naming it, for example a national newspaper (name).",
  { x: 1.95, y: 2.62, w: 10.65, h: 2.68, fontFace: BODY, fontSize: 15, color: GREY, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.06 });
s.addText([{ text: "Secondary instruments: ", options: { bold: true, color: INK } }, { text: "list them with commas, or write none", options: { color: GREY } }],
  { x: 1.95, y: 5.32, w: 10.65, h: 0.3, fontFace: BODY, fontSize: 11.5, margin: 0, isTextBox: true, valign: "middle" });

// sources + scale pill + number
s.addText([{ text: "Source: ", options: { bold: true, color: INK } }, { text: "paste the link, and add a second line 'Source (see also):' if there is another", options: { color: GREY } }],
  { x: 0.5, y: 5.92, w: 10.6, h: 0.95, fontFace: BODY, fontSize: 10, margin: 0, isTextBox: true, valign: "top" });
s.addShape(pres.ShapeType.roundRect, { x: 11.43, y: 6.5, w: 1.4, h: 0.4, fill: { color: GREY }, line: { color: GREY, width: 0 }, rectRadius: 0.2 });
s.addText("Scale", { x: 11.43, y: 6.5, w: 1.4, h: 0.4, fontFace: BODY, fontSize: 12.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
s.addText("0", { x: W - 1.1, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: GREY, align: "right", margin: 0, isTextBox: true });

s.addNotes([
  "Blank policy slide, same layout as the deck. Replace every grey placeholder.",
  "",
  "Flag: delete the grey box and drop in a flag image of the same size (1.05 x 0.79 inches), then put a thin light border around it.",
  "Icon: delete the circle and paste the icon of the main instrument from any slide of the deck, or leave the circle empty.",
  "Instrument: Financial incentives, Information & nudges, Support & training, Flexible positions, Flexible re-certification.",
  "Target: any combination of Switchers, Leavers and Retired.",
  "Scale: Large for a national policy, Medium for a state, region, province or canton, Small for a district, a city or a single institution. Colours: Large 1F4E46, Medium C8892B, Small B3542E.",
  "Fonts: Cambria for the title, Calibri for everything else. Text colours: 24313A and B3542E."
].join("\n"));

const out = path.join(__dirname, "Policy_slide_template.pptx");
pres.writeFile({ fileName: out }).then(() => console.log("written", out));
