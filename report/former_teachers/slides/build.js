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

  const X0 = 0.67, COLW = 3.68, GAP = 0.35;
  const colX = i => X0 + i * (COLW + GAP);
  const T = (text, o) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: "Calibri" }, o));

  // Template frame: header band, logo, title, corner triangle (measured from the OECD template slide)
  const PX = 13.333 / 1200;
  s.addShape(pres.shapes.RECTANGLE, { x: 26 * PX, y: 13 * PX, w: (1188 - 26) * PX, h: (101 - 13) * PX,
    fill: { color: "EBF7F9" }, line: { type: "none" }, objectName: "Header band" });
  const chev = dx => `<polygon fill="#19A3AA" points="${52+dx},20 ${70+dx},47.5 ${65+dx},55 ${52+dx},36.5"/>` +
                     `<polygon fill="#102448" points="${70+dx},48.5 ${70+dx},65.5 ${52+dx},93 ${52+dx},77 ${65.5+dx},55.5"/>`;
  const logoSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="50 18 42 77" width="420" height="770">${chev(0)}${chev(20)}</svg>`;
  const logo = await sharp(Buffer.from(logoSvg)).png().toBuffer();
  s.addImage({ data: "image/png;base64," + logo.toString("base64"), x: 50 * PX, y: 18 * PX, w: 42 * PX, h: 77 * PX,
    altText: "OECD logo", objectName: "Logo" });
  T("Former and retired teachers", { x: 113 * PX, y: 13 * PX, w: 9, h: (101 - 13) * PX, fontSize: 24, bold: true,
    color: "022249", valign: "middle", objectName: "Title" });
  const triSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="432" height="750" viewBox="0 0 108 187">
    <defs><linearGradient id="g" x1="1" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#33BB95"/>
    <stop offset="1" stop-color="#3294C4"/></linearGradient></defs><polygon fill="url(#g)" points="108,0 108,187 0,187"/></svg>`;
  const tri = await sharp(Buffer.from(triSvg)).png().toBuffer();
  s.addImage({ data: "image/png;base64," + tri.toString("base64"), x: 1092 * PX, y: 488 * PX, w: 108 * PX, h: 187 * PX,
    objectName: "Corner triangle" });
  s.addText("Unclassified - Non classifié", { isTextBox: true, margin: 0, x: 0, y: 646 * PX, w: 13.333, h: 20 * PX,
    fontSize: 10, fontFace: "Arial", color: "7F7FFF", align: "center", valign: "middle", objectName: "Classification" });

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

  await pres.writeFile({ fileName: process.argv[2] });
})();
