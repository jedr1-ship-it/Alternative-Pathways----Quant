const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const sharp = require("sharp");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const Fa = require("react-icons/fa");
const POLICIES = require("./policies.js");

// ---------- palette & fonts (max 2 fonts, max 2 text colours per slide) ----------
const GREEN = "1F4E46";   // brand / shapes
const SAGE = "EAF2EE";    // card tint
const INK = "24313A";     // text colour 1
const ACCENT = "B3542E";  // text colour 2 (category label, links)
const WHITE = "FFFFFF";
const LINE = "CFDCD5";
const ICON_BG = GREEN;   // dark green on the pale card, as in the first version of the deck
const HEAD = "Cambria";
const BODY = "Calibri";
const W = 13.333, H = 7.5;

const CATS = [
  { name: "Financial incentives", icon: "FaCoins",
    def: "Direct payments or legal changes with an economic effect: rules letting retirees draw salary plus pension, return bonuses." },
  { name: "Information & nudges", icon: "FaEnvelopeOpenText",
    def: "Informing, reminding or prompting the decision to return: information sessions, peer mentoring, calls or e-mails." },
  { name: "Support & training", icon: "FaChalkboardTeacher",
    def: "Refresher courses, return-to-teaching programmes, induction and coaching that make re-entry easier." },
  { name: "Flexible positions", icon: "FaUserClock",
    def: "Roles other than a full-time teaching post: tutoring pupils, mentoring future or novice teachers or part time work." },
  { name: "Flexible re-certification", icon: "FaCertificate",
    def: "Lowering administrative or training : fewer compulsory course days, simplified procedures, limited teaching hours while re-certifying." },
];
const GROUPS = [
  { name: "(a) Switchers", icon: "FaExchangeAlt", def: "Left the teaching profession to work in another sector." },
  { name: "(b) Leavers", icon: "FaDoorOpen", def: "Left the teaching profession and the labour market altogether (not employed)." },
  { name: "(c) Retired", icon: "FaUmbrellaBeach", def: "Retired from teaching." },
];

// ---------- image helpers ----------
async function flagPng(code) {
  const svg = fs.readFileSync(path.join(__dirname, "node_modules/flag-icons/flags/4x3", code + ".svg"));
  const buf = await sharp(svg, { density: 300 }).resize(600, 450).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
async function iconPng(name, color) {
  const Icon = Fa[name];
  if (!Icon) throw new Error("icon missing " + name);
  let svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Icon, { size: 256 }));
  svg = svg.replace(/currentColor/g, "#" + color); if (!/xmlns=/.test(svg)) svg = svg.replace(/<svg /, "<svg xmlns=\"http://www.w3.org/2000/svg\" ");
  const buf = await sharp(Buffer.from(svg), { density: 300 }).resize(256, 256, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

function iconCircle(slide, pres, data, x, y, d) {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: ICON_BG }, line: { color: ICON_BG, width: 0 } });
  const pad = d * 0.24;
  slide.addImage({ data, x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad });
}

// the five instruments as a row of dots: the ones a policy uses are lit
const OFF = "DCE6E0", OFF_ICON = "AFC0B8", MUTED = "7C8B93";
function instrumentDots(slide, pres, icons, iconsOff, used, x0, y, d, gap) {
  CATS.forEach((c, i) => {
    const on = used.includes(c.name);
    const x = x0 + i * (d + gap);
    slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: on ? GREEN : OFF }, line: { color: on ? GREEN : OFF, width: 0 } });
    const pad = d * 0.24;
    slide.addImage({ data: on ? icons[c.name] : iconsOff[c.name], x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad });
  });
}

const SCALE_COLORS = { Large: GREEN, Medium: "C8892B", Small: ACCENT };
function scaleLabel(slide, pres, scale) {
  const w = 1.8, h = 0.47, x = 11.03, y = 0.42;
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: SCALE_COLORS[scale] }, line: { color: SCALE_COLORS[scale], width: 0 }, rectRadius: 0.2 });
  slide.addText(scale, { x, y, w, h, fontFace: BODY, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function slideNumber(slide, n) {
  slide.addText(String(n), { x: 0.5, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: INK, align: "left", margin: 0, isTextBox: true });
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
  pres.author = "José Manuel Torres, José Elías Durán Roa";
  pres.title = "Re-attracting Former Teachers";

  const icons = {}, iconsOff = {};
  for (const c of CATS) { icons[c.name] = await iconPng(c.icon, WHITE); iconsOff[c.name] = await iconPng(c.icon, OFF_ICON); }
  for (const g of GROUPS) icons[g.name] = await iconPng(g.icon, WHITE);
  const flags = {};
  for (const p of POLICIES) if (!flags[p.flag]) flags[p.flag] = await flagPng(p.flag);

  // ================= 1. COVER =================
  {
    const logoPath = path.join(__dirname, "oecd-logo.png");
    const logoData = fs.existsSync(logoPath) ? "image/png;base64," + fs.readFileSync(logoPath).toString("base64") : null;
    const s = pres.addSlide();
    s.background = { color: GREEN };
    s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: W, h: 1.58, fill: { color: WHITE }, line: { color: WHITE, width: 0 } });
    if (logoData) s.addImage({ data: logoData, x: 0.7, y: 0.47, w: 2.0, h: 0.51 });
    s.addText("Directorate for Education and Skills", { x: 0.7, y: 0.98, w: 6.0, h: 0.32, fontFace: "Garamond", fontSize: 14, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    s.addText("Re-attracting Former Teachers", { x: 0.8, y: 2.0, w: 11.7, h: 1.15, fontFace: HEAD, fontSize: 44, bold: true, color: WHITE, margin: 0, isTextBox: true, valign: "bottom" });
    s.addText("Various international policies and experiences", { x: 0.8, y: 3.25, w: 11.7, h: 0.6, fontFace: BODY, fontSize: 21, color: "CFE3D9", margin: 0, isTextBox: true });
    s.addText([
      { text: "José Manuel Torres &  José Elías Durán Roa ", options: { bold: true, breakLine: true } },
      { text: "September 2026" }
    ], { x: 0.93, y: 5.2, w: 10, h: 0.4, fontFace: HEAD, fontSize: 16, color: "CFE3D9", margin: 0, isTextBox: true });
    s.addNotes("Deck built from official sources, plus institutional evaluations and reputable press where noted. Each policy slide carries its source links; verification notes are in the speaker notes of each slide." + (logoData ? "" : " No logo file supplied yet: drop oecd-logo.png into the build folder and rebuild to place it top-left."));
  }

  // ================= 2. TARGET GROUPS =================
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("Who we mean by former teachers", { x: 0.7, y: 0.6, w: 11.8, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: INK, margin: 0, isTextBox: true });
    let y = 2.05;
    for (const g of GROUPS) {
      iconCircle(s, pres, icons[g.name], 0.9, y, 0.8);
      s.addText(g.name, { x: 2.0, y: y - 0.04, w: 10.2, h: 0.42, fontFace: BODY, fontSize: 19, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
      s.addText(g.def, { x: 2.0, y: y + 0.38, w: 10.2, h: 0.55, fontFace: BODY, fontSize: 14, color: INK, margin: 0, isTextBox: true, valign: "top" });
      y += 1.32;
    }
    slideNumber(s, 2);
    s.addNotes("Three target groups, as defined in the brief. A policy may target one group or several.");
  }

  // ================= 3. INSTRUMENT CATEGORIES =================
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("Five policy instruments", { x: 0.7, y: 0.45, w: 11.8, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: INK, margin: 0, isTextBox: true });
    s.addText("Classified by the instrument used to re-attract teachers", { x: 0.73, y: 1.12, w: 11.8, h: 0.35, fontFace: BODY, fontSize: 14, color: ACCENT, margin: 0, isTextBox: true });
    let y = 1.85;
    for (const c of CATS) {
      iconCircle(s, pres, icons[c.name], 0.9, y, 0.68);
      s.addText(c.name, { x: 1.85, y: y - 0.05, w: 10.6, h: 0.36, fontFace: BODY, fontSize: 16.5, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
      s.addText(c.def, { x: 1.85, y: y + 0.3, w: 10.6, h: 0.6, fontFace: BODY, fontSize: 13, color: INK, margin: 0, isTextBox: true, valign: "top" });
      y += 1.0;
    }
    slideNumber(s, 3);
    s.addNotes("The five instrument categories used to classify every policy in the deck. Secondary instruments are named on each policy slide.");
  }

  // ================= 4. SCALE LABELS =================
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("Scale", { x: 0.7, y: 0.6, w: 11.8, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: INK, margin: 0, isTextBox: true });
    const scales = [["Large", "National policy"], ["Medium", "State, region, province or canton"], ["Small", "District, city or a single institution"]];
    let y = 2.35;
    for (const [k, v] of scales) {
      s.addShape(pres.ShapeType.ellipse, { x: 0.95, y: y + 0.09, w: 0.28, h: 0.28, fill: { color: SCALE_COLORS[k] }, line: { color: SCALE_COLORS[k], width: 0 } });
      s.addText(k, { x: 1.45, y, w: 2.2, h: 0.46, fontFace: BODY, fontSize: 20, bold: true, color: SCALE_COLORS[k], margin: 0, isTextBox: true, valign: "middle" });
      s.addText(v, { x: 3.6, y, w: 9.0, h: 0.46, fontFace: BODY, fontSize: 15, color: INK, margin: 0, isTextBox: true, valign: "middle" });
      y += 0.95;
    }
    slideNumber(s, 4);
    s.addNotes("Scale tells the reader how far a policy reaches: a whole country, a state or region, or one district or institution.");
  }

  // ================= 3. POLICY SLIDES =================
  let n = 5;
  for (const p of POLICIES) {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    // flag + country (top-left)
    s.addImage({ data: flags[p.flag], x: 0.5, y: 0.42, w: 1.05, h: 0.7875 });
    s.addShape(pres.ShapeType.rect, { x: 0.5, y: 0.42, w: 1.05, h: 0.7875, fill: { type: "none" }, line: { color: LINE, width: 0.75 } });
    s.addText(p.country, { x: 1.75, y: 0.42, w: 9.1, h: 0.5, fontFace: BODY, fontSize: 22, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    if (p.region) s.addText(p.region, { x: 1.75, y: 0.92, w: 9.1, h: 0.34, fontFace: BODY, fontSize: 13, color: INK, margin: 0, isTextBox: true, valign: "top" });
    // body card
    s.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.5, w: 12.33, h: 4.22, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
    s.addText(p.title, { x: 0.95, y: 1.7, w: 11.43, h: 0.9, fontFace: HEAD, fontSize: 21, bold: true, color: INK, margin: 0, isTextBox: true, valign: "top" });
    s.addText(p.desc, { x: 0.95, y: 2.64, w: 11.43, h: 2.85, fontFace: BODY, fontSize: 15, color: INK, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.06 });
    // footer: sources (clickable)
    const runs = [];
    p.sources.forEach((u, i) => {
      runs.push({ text: i === 0 ? "Source: " : "Source (see also): ", options: { bold: true, color: INK, breakLine: false } });
      runs.push({ text: u, options: { hyperlink: { url: u, tooltip: u }, color: ACCENT, underline: { style: "sng", color: ACCENT }, breakLine: i < p.sources.length - 1 } });
    });
    s.addText(runs, { x: 0.5, y: 5.8, w: 8.3, h: 0.9, fontFace: BODY, fontSize: 10, color: INK, margin: 0, isTextBox: true, valign: "top" });
    // instruments used, as lit dots, with the target groups under them
    const used = [p.cat, ...(p.secondary || [])];
    const dotD = 0.62, dotGap = 0.20, dotN = 5;
    const dotsW = dotN * dotD + (dotN - 1) * dotGap;
    const dotsX = 12.83 - dotsW;
    instrumentDots(s, pres, icons, iconsOff, used, dotsX, 6.26, dotD, dotGap);
    s.addText(p.groups.join(" / "), { x: 7.8, y: 6.97, w: 5.03, h: 0.28, fontFace: BODY, fontSize: 10.5, color: MUTED, align: "right", margin: 0, isTextBox: true, valign: "middle" });
    scaleLabel(s, pres, p.scale);
    slideNumber(s, n);
    s.addNotes(`${p.country}${p.region ? " (" + p.region + ")" : ""} — Instruments lit: ${used.join(", ")} — Target: ${p.groups.join(", ")}.\n\n${p.notes}\n\nEuro amounts in brackets are approximate conversions, rounded, for orientation only.`);
    n++;
  }

  // ================= 4. BLANK TEMPLATE SLIDE =================
  {
    const GREY = "8C9B95";
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addShape(pres.ShapeType.rect, { x: 0.5, y: 0.42, w: 1.05, h: 0.7875, fill: { color: "F4F7F5" }, line: { color: LINE, width: 1 } });
    s.addText("flag", { x: 0.5, y: 0.42, w: 1.05, h: 0.7875, fontFace: BODY, fontSize: 10, color: GREY, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText("Country", { x: 1.75, y: 0.42, w: 9.1, h: 0.5, fontFace: BODY, fontSize: 22, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    s.addText("Region or state (delete this line if the policy is national)", { x: 1.75, y: 0.92, w: 9.1, h: 0.34, fontFace: BODY, fontSize: 13, color: GREY, margin: 0, isTextBox: true });
    s.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.5, w: 12.33, h: 4.22, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
    s.addText("Policy name, and the year or period", { x: 0.95, y: 1.7, w: 11.43, h: 0.9, fontFace: HEAD, fontSize: 21, bold: true, color: INK, margin: 0, isTextBox: true, valign: "top" });
    s.addText("Write four to six lines of plain prose. Open with what the policy actually does, who runs it and whom it is for, then how it works step by step, then what the returner gets. Put dates and figures at the end, and only the ones that carry the story. Do not repeat the country, the region or the policy name: they are already on the slide.",
      { x: 0.95, y: 2.64, w: 11.43, h: 2.85, fontFace: BODY, fontSize: 15, color: GREY, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.06 });
    s.addText([{ text: "Source: ", options: { bold: true, color: INK } }, { text: "paste the link, and add a second line 'Source (see also):' if there is another", options: { color: GREY } }],
      { x: 0.5, y: 5.8, w: 8.3, h: 0.9, fontFace: BODY, fontSize: 10, margin: 0, isTextBox: true, valign: "top" });
    const tD = 0.62, tGap = 0.20, tW = 5 * tD + 4 * tGap, tX = 12.83 - tW;
    instrumentDots(s, pres, icons, iconsOff, [], tX, 6.26, tD, tGap);
    s.addText("Switchers / Leavers / Retired", { x: 7.8, y: 6.97, w: 5.03, h: 0.28, fontFace: BODY, fontSize: 10.5, color: GREY, align: "right", margin: 0, isTextBox: true, valign: "middle" });
    s.addShape(pres.ShapeType.roundRect, { x: 11.03, y: 0.42, w: 1.8, h: 0.47, fill: { color: GREY }, line: { color: GREY, width: 0 }, rectRadius: 0.235 });
    s.addText("Scale", { x: 11.03, y: 0.42, w: 1.8, h: 0.47, fontFace: BODY, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
    slideNumber(s, n);
    s.addNotes([
      "Blank policy slide, same layout as the deck. Replace every grey placeholder.",
      "Flag: delete the grey box and drop in a flag image of the same size (1.05 x 0.79 inches), then put a thin light border around it.",
      "Instrument dots: in order, Financial incentives, Information & nudges, Support & training, Flexible positions, Flexible re-certification. Copy a lit dot from any slide over the ones this policy uses and leave the rest grey.",
      "Target groups: the grey line under the dots. Any combination of Switchers, Leavers and Retired.",
      "Scale: Large for a national policy, Medium for a state, region, province or canton, Small for a district, a city or a single institution. Colours: Large 1F4E46, Medium C8892B, Small B3542E.",
      "Fonts: Cambria for the title, Calibri for everything else. Text colours: 24313A and B3542E."
    ].join("\n"));
  }

  // ================= 5. INDEX (two slides, every policy linked to its slide) =================
  {
    const half = Math.ceil(POLICIES.length / 2);
    [POLICIES.slice(0, half), POLICIES.slice(half)].forEach((part, pi) => {
      const s = pres.addSlide();
      s.background = { color: WHITE };
      s.addText(`Index: the ${POLICIES.length} policies (${pi + 1}/2)`, { x: 0.5, y: 0.3, w: 10, h: 0.6, fontFace: HEAD, fontSize: 28, bold: true, color: INK, margin: 0, isTextBox: true });
      s.addText("Click a policy to go to its slide", { x: 0.5, y: 0.88, w: 10, h: 0.3, fontFace: BODY, fontSize: 11.5, color: ACCENT, margin: 0, isTextBox: true });
      const hdr = ["Country", "Policy", "Target group(s)", "Scale"].map(t => ({ text: t, options: { bold: true, color: WHITE, fill: { color: GREEN }, fontSize: 10.5, valign: "middle" } }));
      const rows = [hdr];
      part.forEach((p, i) => {
        const fill = i % 2 === 0 ? WHITE : "F4F8F6";
        const o = { color: INK, fontSize: 9.5, fill: { color: fill }, valign: "middle" };
        const target = 5 + POLICIES.indexOf(p);
        rows.push([
          { text: p.country + (p.region ? " (" + p.region + ")" : ""), options: { ...o, bold: true } },
          { text: [{ text: p.title, options: { hyperlink: { slide: target, tooltip: "Go to slide " + target }, color: ACCENT, underline: { style: "sng", color: ACCENT } } }], options: { ...o } },
          { text: p.groups.join(" / "), options: { ...o } },
          { text: p.scale, options: { ...o, color: SCALE_COLORS[p.scale], bold: true } },
        ]);
      });
      s.addTable(rows, { x: 0.5, y: 1.25, w: 12.33, colW: [2.45, 6.25, 2.68, 0.95], fontFace: BODY, border: { type: "solid", pt: 0.5, color: LINE }, margin: [2, 5, 2, 5], rowH: 0.28, autoPage: false });
      slideNumber(s, n + 1 + pi);
      s.addNotes("Index of every policy in the deck. Each policy name links to its own slide.");
    });
  }

  const out = path.join(__dirname, "Re-attracting_Former_Teachers.pptx");
  await pres.writeFile({ fileName: out });
  console.log("written", out);
})().catch(e => { console.error(e); process.exit(1); });
