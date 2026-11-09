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

  const X0 = 0.75, COLW = 3.65, GAP = 0.42;
  const colX = i => X0 + i * (COLW + GAP);
  const T = (text, o) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: "Calibri" }, o));

  // Title
  T("Former and retired teachers", { x: X0, y: 0.45, w: 11.8, h: 0.6, fontSize: 30, bold: true, color: NAVY });

  // Key figures
  const stats = [["30+", "policies mapped across 18 countries", NAVY],
                 ["62%", "use financial incentives", TEAL],
                 ["3/4", "combine two or more instruments", PURPLE]];
  stats.forEach(([n, lab, c], i) => {
    T(n, { x: colX(i), y: 1.4, w: COLW, h: 0.8, fontSize: 48, bold: true, color: c, valign: "bottom" });
    T(lab, { x: colX(i), y: 2.22, w: COLW, h: 0.35, fontSize: 15, color: GREY });
  });
  s.addShape(pres.shapes.LINE, { x: X0, y: 2.95, w: colX(2) + COLW - X0, h: 0, line: { color: LINE, width: 0.75 } });

  // Column headers
  const heads = [["Three profiles", NAVY], ["Five policy instruments", TEAL], ["Fit, not just barriers", PURPLE]];
  heads.forEach(([h, c], i) => T(h, { x: colX(i), y: 3.25, w: COLW, h: 0.4, fontSize: 19, bold: true, color: c }));

  const Y1 = 3.9;

  // Column 1: profiles with icons
  const profiles = [[fa.FaBriefcase, "Switchers", "moved to another occupation"],
                    [fa.FaHome, "Leavers", "left the labour market"],
                    [fa.FaHourglassEnd, "Retired teachers", "reached the end of their career"]];
  for (let k = 0; k < profiles.length; k++) {
    const [I, name, desc] = profiles[k];
    const y = Y1 + k * 0.72;
    s.addShape(pres.shapes.OVAL, { x: colX(0), y, w: 0.5, h: 0.5, fill: { color: TINT[NAVY] }, line: { type: "none" } });
    s.addImage({ data: await icon(I, NAVY), x: colX(0) + 0.14, y: y + 0.14, w: 0.22, h: 0.22 });
    T([{ text: name, options: { bold: true, color: INK, fontSize: 15, breakLine: true } },
       { text: desc, options: { color: GREY, fontSize: 14 } }],
      { x: colX(0) + 0.68, y: y - 0.04, w: COLW - 0.68, h: 0.6, valign: "middle" });
  }

  // Column 2: numbered instruments
  const inst = ["Financial incentives", "Information and nudges", "Support and training",
                "Flexible re-certification", "Flexible positions"];
  inst.forEach((t, k) => {
    const y = Y1 + 0.05 + k * 0.43;
    s.addShape(pres.shapes.OVAL, { x: colX(1), y, w: 0.32, h: 0.32, fill: { color: TEAL }, line: { type: "none" } });
    T(String(k + 1), { x: colX(1), y, w: 0.32, h: 0.32, fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(t, { x: colX(1) + 0.5, y: y - 0.02, w: COLW - 0.5, h: 0.36, fontSize: 15, color: INK, valign: "middle" });
  });

  // Column 3: two messages with icons
  const msgs = [[fa.FaUnlockAlt, "Removing barriers is not enough",
                 "if returners face the conditions that contributed to their departure."],
                [fa.FaPuzzlePiece, "Differentiated roles",
                 "Part-time, mentoring and tutoring roles make a better fit."]];
  for (let k = 0; k < msgs.length; k++) {
    const [I, head, body] = msgs[k];
    const y = Y1 + k * 1.08;
    s.addShape(pres.shapes.OVAL, { x: colX(2), y, w: 0.5, h: 0.5, fill: { color: TINT[PURPLE] }, line: { type: "none" } });
    s.addImage({ data: await icon(I, PURPLE), x: colX(2) + 0.14, y: y + 0.14, w: 0.22, h: 0.22 });
    T([{ text: head, options: { bold: true, color: INK, fontSize: 15, breakLine: true } },
       { text: body, options: { color: GREY, fontSize: 14 } }],
      { x: colX(2) + 0.68, y: y - 0.02, w: COLW - 0.68, h: 0.9, valign: "top" });
  }

  // Take-away lines, aligned across columns
  const take = ["Reasons for leaving differ, and so must the policies that re-attract them.",
                "Most policies combine several instruments."];
  take.forEach((t, i) => T(t, { x: colX(i), y: 6.2, w: COLW, h: 0.55, fontSize: 14, italic: true, color: [NAVY, TEAL, PURPLE][i], valign: "top" }));

  T("Unclassified - Non classifié", { x: 0, y: 7.1, w: 13.333, h: 0.25, fontSize: 10, color: "7B7FD6", align: "center" });

  await pres.writeFile({ fileName: process.argv[2] });
})();
