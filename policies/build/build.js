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
const HEAD = "Cambria";
const BODY = "Calibri";
const W = 13.333, H = 7.5;

const CATS = [
  { name: "Financial incentives", icon: "FaCoins",
    def: "Direct payments or legal changes with an economic effect: rules letting retirees draw salary plus pension, return bonuses for switchers or leavers, bonuses for schools that re-hire them." },
  { name: "Information & nudges", icon: "FaEnvelopeOpenText",
    def: "Informing, reminding or prompting the decision to return: information sessions, career guidance or peer mentoring, a leaflet with the retirement form, personalised letters, calls or e-mails." },
  { name: "Support & training", icon: "FaChalkboardTeacher",
    def: "Refresher courses, return-to-teaching programmes, induction and coaching that make re-entry easier." },
  { name: "Flexible positions", icon: "FaUserClock",
    def: "Roles other than a full-time teaching post: tutoring pupils, mentoring future or novice teachers, part-time or flexible substitute work." },
  { name: "Flexible re-certification", icon: "FaCertificate",
    def: "Lowering administrative or training barriers where former teachers must re-certify: fewer compulsory course days, simplified procedures, limited teaching hours while re-certifying." },
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
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: GREEN }, line: { color: GREEN, width: 0 } });
  const pad = d * 0.24;
  slide.addImage({ data, x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad });
}

const SCALE_COLORS = { Large: GREEN, Medium: "C8892B", Small: ACCENT };
function scaleLabel(slide, pres, scale) {
  const w = 1.4, h = 0.4, x = 11.43, y = 6.5;
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: SCALE_COLORS[scale] }, line: { color: SCALE_COLORS[scale], width: 0 }, rectRadius: 0.2 });
  slide.addText(scale, { x, y, w, h, fontFace: BODY, fontSize: 12.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function slideNumber(slide, n) {
  slide.addText(String(n), { x: W - 1.1, y: H - 0.42, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 9, color: INK, align: "right", margin: 0, isTextBox: true });
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
  pres.author = "José Manuel Torres, José Elías Durán Roa";
  pres.title = "Re-attracting Former Teachers";

  const icons = {};
  for (const c of CATS) icons[c.name] = await iconPng(c.icon, WHITE);
  for (const g of GROUPS) icons[g.name] = await iconPng(g.icon, WHITE);
  const flags = {};
  for (const p of POLICIES) if (!flags[p.flag]) flags[p.flag] = await flagPng(p.flag);

  // ================= 1. COVER =================
  {
    const logoPath = path.join(__dirname, "oecd-logo.png");
    const logoData = fs.existsSync(logoPath) ? "image/png;base64," + fs.readFileSync(logoPath).toString("base64") : null;
    const s = pres.addSlide();
    s.background = { color: GREEN };
    if (logoData) s.addImage({ data: logoData, x: 0.8, y: 0.6, w: 2.6, h: 0.75, sizing: { type: "contain", w: 2.6, h: 0.75 } });
    s.addText("Re-attracting Former Teachers", { x: 0.8, y: 2.0, w: 11.7, h: 1.15, fontFace: HEAD, fontSize: 44, bold: true, color: WHITE, margin: 0, isTextBox: true, valign: "bottom" });
    s.addText("Policies that bring them back into education", { x: 0.8, y: 3.25, w: 11.7, h: 0.6, fontFace: BODY, fontSize: 21, color: "CFE3D9", margin: 0, isTextBox: true });
    s.addText("José Manuel Torres &  José Elías Durán Roa  ·  September 2026", { x: 0.8, y: 6.5, w: 10, h: 0.4, fontFace: BODY, fontSize: 13, color: "CFE3D9", margin: 0, isTextBox: true });
    const uniqueFlags = [...new Set(POLICIES.map(p => p.flag))];
    const gap = 0.12, avail = 12.33;
    const fw = Math.min(0.78, (avail - (uniqueFlags.length - 1) * gap) / uniqueFlags.length);
    const fh = fw * 0.75;
    const total = uniqueFlags.length * fw + (uniqueFlags.length - 1) * gap;
    let x = (W - total) / 2;
    for (const code of uniqueFlags) { s.addImage({ data: flags[code], x, y: 5.15, w: fw, h: fh }); x += fw + gap; }
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
    s.addText("Classified by the instrument it uses to re-attract teachers", { x: 0.73, y: 1.12, w: 11.8, h: 0.35, fontFace: BODY, fontSize: 14, color: ACCENT, margin: 0, isTextBox: true });
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
    s.addText(p.country, { x: 1.75, y: 0.36, w: 6.8, h: 0.5, fontFace: BODY, fontSize: 22, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    if (p.region) s.addText(p.region, { x: 1.75, y: 0.86, w: 6.8, h: 0.34, fontFace: BODY, fontSize: 13, color: INK, margin: 0, isTextBox: true, valign: "top" });
    // category pill + target groups (top-right)
    s.addShape(pres.ShapeType.roundRect, { x: 9.03, y: 0.42, w: 3.8, h: 0.47, fill: { color: SAGE }, line: { color: ACCENT, width: 1 }, rectRadius: 0.235 });
    s.addText(p.cat, { x: 9.03, y: 0.42, w: 3.8, h: 0.47, fontFace: BODY, fontSize: 13.5, bold: true, color: ACCENT, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText("Target: " + p.groups.join(" / "), { x: 8.03, y: 0.93, w: 4.8, h: 0.3, fontFace: BODY, fontSize: 11, color: INK, align: "right", valign: "top", margin: 0, isTextBox: true });
    // body card
    s.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.5, w: 12.33, h: 4.22, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
    iconCircle(s, pres, icons[p.cat], 0.85, 1.85, 0.85);
    s.addText(p.title, { x: 1.95, y: 1.68, w: 10.65, h: 0.95, fontFace: HEAD, fontSize: 21, bold: true, color: INK, margin: 0, isTextBox: true, valign: "top" });
    s.addText(p.desc, { x: 1.95, y: 2.62, w: 10.65, h: 2.68, fontFace: BODY, fontSize: 15, color: INK, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.06 });
    // secondary instruments line
    s.addText([
      { text: "Secondary instruments: ", options: { bold: true, color: INK } },
      { text: (p.secondary && p.secondary.length) ? p.secondary.join(", ") : "none", options: { color: INK } }
    ], { x: 1.95, y: 5.32, w: 10.65, h: 0.3, fontFace: BODY, fontSize: 11.5, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    // footer: sources (clickable)
    const runs = [];
    p.sources.forEach((u, i) => {
      runs.push({ text: i === 0 ? "Source: " : "Source (see also): ", options: { bold: true, color: INK, breakLine: false } });
      runs.push({ text: u, options: { hyperlink: { url: u, tooltip: u }, color: ACCENT, underline: { style: "sng", color: ACCENT }, breakLine: i < p.sources.length - 1 } });
    });
    s.addText(runs, { x: 0.5, y: 5.92, w: 10.6, h: 0.95, fontFace: BODY, fontSize: 10, color: INK, margin: 0, isTextBox: true, valign: "top" });
    scaleLabel(s, pres, p.scale);
    slideNumber(s, n);
    s.addNotes(`${p.country}${p.region ? " (" + p.region + ")" : ""} — ${p.cat} — Target: ${p.groups.join(", ")}.\n\n${p.notes}\n\nEuro amounts in brackets are approximate conversions, rounded, for orientation only.`);
    n++;
  }

  // ================= 4. SUMMARY TABLE (two slides) =================
  const half = Math.ceil(POLICIES.length / 2);
  [POLICIES.slice(0, half), POLICIES.slice(half)].forEach((part, pi) => {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText(`Summary: ${POLICIES.length} policies at a glance (${pi + 1}/2)`, { x: 0.5, y: 0.3, w: 10, h: 0.6, fontFace: HEAD, fontSize: 28, bold: true, color: INK, margin: 0, isTextBox: true });
    const hdr = ["Country", "Policy", "Category", "Target group(s)", "Scale"].map(t => ({ text: t, options: { bold: true, color: WHITE, fill: { color: GREEN }, fontSize: 10.5, valign: "middle" } }));
    const rows = [hdr];
    part.forEach((p, i) => {
      const fill = i % 2 === 0 ? WHITE : "F4F8F6";
      const o = { color: INK, fontSize: 9.5, fill: { color: fill }, valign: "middle" };
      rows.push([
        { text: p.country + (p.region ? " (" + p.region + ")" : ""), options: { ...o, bold: true } },
        { text: p.title, options: { ...o } },
        { text: p.cat, options: { ...o } },
        { text: p.groups.join(" / "), options: { ...o } },
        { text: p.scale, options: { ...o } },
      ]);
    });
    s.addTable(rows, { x: 0.5, y: 1.1, w: 12.33, colW: [2.35, 5.3, 2.0, 1.93, 0.75], fontFace: BODY, border: { type: "solid", pt: 0.5, color: LINE }, margin: [2, 5, 2, 5], rowH: 0.28, autoPage: false });
    slideNumber(s, n + pi);
    s.addNotes("Summary table of all policies in the deck, in the same order as the slides.");
  });

  const out = path.join(__dirname, "Re-attracting_Former_Teachers.pptx");
  await pres.writeFile({ fileName: out });
  console.log("written", out);
})().catch(e => { console.error(e); process.exit(1); });
