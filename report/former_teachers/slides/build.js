const pptxgen = require("pptxgenjs");
const React = require("react");
const RDS = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const NAVY = "1F3864", TEAL = "17A398", PURPLE = "7A3B7E";
const INK = "222B3A", GREY = "5B6573", LINE = "D9DEE5";
const TINT = { [NAVY]: "E8ECF3", [TEAL]: "E3F4F2", [PURPLE]: "F1E8F1" };

async function icon(Comp, color) {
  const svg = RDS.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: 256 }));
  const png = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
  pres.theme = { headFontFace: "Calibri", bodyFontFace: "Calibri" };
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };

  const GUIDES = process.argv[3] === "guides";
  const X0 = 0.67, COLW = 3.68, GAP = 0.35;
  const colX = i => X0 + i * (COLW + GAP);
  const T = (text, o) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: "Calibri" }, o));

  if (GUIDES) { // preview only: template header band, title and corner triangle
    s.addShape(pres.shapes.RECTANGLE, { x: 0.27, y: 0.13, w: 12.95, h: 0.98, fill: { color: "EAF5F8" }, line: { type: "none" } });
    T("Former and retired teachers", { x: 1.25, y: 0.38, w: 8, h: 0.5, fontSize: 24, bold: true, color: "0B2545" });
    s.addShape(pres.shapes.RIGHT_TRIANGLE, { x: 12.1, y: 5.44, w: 1.233, h: 2.06, flipH: true, fill: { color: "2BB3A0" }, line: { type: "none" } });
  }

  // Key figures in boxes
  const stats = [["30+", "policies mapped across 18 countries", NAVY],
                 ["62%", "use financial incentives", TEAL],
                 ["3/4", "combine two or more instruments", PURPLE]];
  stats.forEach(([n, lab, c], i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: colX(i), y: 1.42, w: COLW, h: 1.38, rectRadius: 0.16,
      fill: { color: "DCE8F1" }, line: { color: c, width: 1.25 } });
    T(n, { x: colX(i), y: 1.55, w: COLW, h: 0.72, fontSize: 40, bold: true, color: c, align: "center", valign: "middle" });
    T(lab, { x: colX(i), y: 2.3, w: COLW, h: 0.34, fontSize: 15, color: INK, align: "center", valign: "middle" });
  });

  // Column headers, same baseline
  const heads = [["Three profiles", NAVY], ["Five policy instruments", TEAL], ["Fit, not just barriers", PURPLE]];
  heads.forEach(([h, c], i) => T(h, { x: colX(i), y: 3.12, w: COLW, h: 0.42, fontSize: 20, bold: true, color: c, valign: "middle" }));

  const Y1 = 3.75;

  // Column 1: profiles
  const profiles = [[fa.FaBriefcase, "Switchers", "moved to another occupation"],
                    [fa.FaHome, "Leavers", "left the labour market"],
                    [fa.FaHourglassEnd, "Retired teachers", "reached the end of their career"]];
  for (let k = 0; k < profiles.length; k++) {
    const [I, name, desc] = profiles[k];
    const y = Y1 + k * 0.78;
    s.addShape(pres.shapes.OVAL, { x: colX(0), y, w: 0.56, h: 0.56, fill: { color: TINT[NAVY] }, line: { type: "none" } });
    s.addImage({ data: await icon(I, NAVY), x: colX(0) + 0.165, y: y + 0.165, w: 0.23, h: 0.23 });
    T([{ text: name, options: { bold: true, color: INK, fontSize: 15, breakLine: true } },
       { text: desc, options: { color: GREY, fontSize: 14 } }],
      { x: colX(0) + 0.76, y, w: COLW - 0.76, h: 0.56, valign: "middle" });
  }

  // Column 2: instruments, spread over the same height as column 1
  const inst = ["Financial incentives", "Information and nudges", "Support and training",
                "Flexible re-certification", "Flexible positions"];
  const step2 = (2 * 0.78 + 0.56 - 0.38) / 4;
  inst.forEach((t, k) => {
    const y = Y1 + k * step2;
    s.addShape(pres.shapes.OVAL, { x: colX(1) + 0.09, y, w: 0.38, h: 0.38, fill: { color: TEAL }, line: { type: "none" } });
    T(String(k + 1), { x: colX(1) + 0.09, y, w: 0.38, h: 0.38, fontSize: 13, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(t, { x: colX(1) + 0.76, y, w: COLW - 0.76, h: 0.38, fontSize: 15, color: INK, valign: "middle" });
  });

  // Column 3: two messages
  const msgs = [[fa.FaUnlockAlt, "Removing barriers is not enough",
                 "if returners face the conditions that contributed to their departure."],
                [fa.FaPuzzlePiece, "Differentiated roles",
                 "Part-time, mentoring and tutoring roles make a better fit."]];
  for (let k = 0; k < msgs.length; k++) {
    const [I, head, body] = msgs[k];
    const y = Y1 + k * 1.15;
    s.addShape(pres.shapes.OVAL, { x: colX(2), y, w: 0.56, h: 0.56, fill: { color: TINT[PURPLE] }, line: { type: "none" } });
    s.addImage({ data: await icon(I, PURPLE), x: colX(2) + 0.165, y: y + 0.165, w: 0.23, h: 0.23 });
    T([{ text: head, options: { bold: true, color: INK, fontSize: 15, breakLine: true } },
       { text: body, options: { color: GREY, fontSize: 14 } }],
      { x: colX(2) + 0.76, y: y + 0.02, w: COLW - 0.76, h: 0.95, valign: "top" });
  }

  // Take-away under column 1
  T("Reasons for leaving differ, and so must the policies that re-attract them!",
    { x: colX(0), y: 6.2, w: COLW, h: 0.62, fontSize: 15, color: NAVY, valign: "top" });

  if (GUIDES) T("Unclassified - Non classifié", { x: 0, y: 7.2, w: 13.333, h: 0.25, fontSize: 10, color: "7B7FD6", align: "center" });
  await pres.writeFile({ fileName: process.argv[2] });
})();
