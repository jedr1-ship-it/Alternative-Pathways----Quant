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
    def: "Informing, reminding or prompting the decision to return without changing economic incentives: information sessions, career guidance or peer mentoring, a leaflet with the retirement form, personalised letters, calls or e-mails." },
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
    const s = pres.addSlide();
    s.background = { color: GREEN };
    s.addText("Re-attracting Former Teachers", { x: 0.8, y: 1.25, w: 11.7, h: 1.2, fontFace: HEAD, fontSize: 46, bold: true, color: WHITE, margin: 0, isTextBox: true, valign: "bottom" });
    s.addText("Policies that bring them back into education", { x: 0.8, y: 2.55, w: 11.7, h: 0.7, fontFace: BODY, fontSize: 22, color: "CFE3D9", margin: 0, isTextBox: true });
    s.addText("José Manuel Torres – José Elías Durán Roa  ·  September 2026", { x: 0.8, y: 4.45, w: 10, h: 0.4, fontFace: BODY, fontSize: 13, color: "CFE3D9", margin: 0, isTextBox: true });
    // flag strip (unique flags, in deck order)
    const uniq = [...new Set(POLICIES.map(p => p.flag))];
    const fw = 0.78, fh = 0.585, gap = 0.19;
    const total = uniq.length * fw + (uniq.length - 1) * gap;
    let x = (W - total) / 2;
    for (const code of uniq) {
      s.addImage({ data: flags[code], x, y: 5.55, w: fw, h: fh });
      x += fw + gap;
    }
    s.addNotes("Deck built from official sources (laws, ministry and agency web pages) plus, where noted, institutional evaluations and reputable press. Each policy slide carries its main source link in the footer; secondary sources and verification notes are in the speaker notes of each slide. Direct HTTP access was not available in the build environment, so every URL was verified through search-engine indexing of the official pages on 17 September 2026.");
  }

  // ================= 2. DEFINITIONS =================
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("Definitions", { x: 0.6, y: 0.65, w: 8, h: 0.65, fontFace: HEAD, fontSize: 32, bold: true, color: INK, margin: 0, isTextBox: true });

    // left card: target groups
    s.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.55, w: 4.55, h: 5.35, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
    s.addText("Target population: former teachers", { x: 0.75, y: 1.72, w: 4.1, h: 0.4, fontFace: BODY, fontSize: 15, bold: true, color: INK, margin: 0, isTextBox: true });
    let y = 2.3;
    for (const g of GROUPS) {
      iconCircle(s, pres, icons[g.name], 0.78, y + 0.04, 0.55);
      s.addText(g.name, { x: 1.5, y, w: 3.4, h: 0.32, fontFace: BODY, fontSize: 13, bold: true, color: INK, margin: 0, isTextBox: true });
      s.addText(g.def, { x: 1.5, y: y + 0.32, w: 3.4, h: 0.6, fontFace: BODY, fontSize: 11.5, color: INK, margin: 0, isTextBox: true, valign: "top" });
      y += 1.02;
    }

    // right card: instruments
    s.addShape(pres.ShapeType.roundRect, { x: 5.3, y: 1.55, w: 7.53, h: 5.35, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
    s.addText("Five categories: each policy is classified by the instrument it uses", { x: 5.55, y: 1.72, w: 7.1, h: 0.4, fontFace: BODY, fontSize: 15, bold: true, color: INK, margin: 0, isTextBox: true });
    y = 2.3;
    for (const c of CATS) {
      iconCircle(s, pres, icons[c.name], 5.58, y + 0.04, 0.55);
      s.addText(c.name, { x: 6.3, y, w: 6.35, h: 0.3, fontFace: BODY, fontSize: 13, bold: true, color: INK, margin: 0, isTextBox: true });
      s.addText(c.def, { x: 6.3, y: y + 0.3, w: 6.35, h: 0.58, fontFace: BODY, fontSize: 11, color: INK, margin: 0, isTextBox: true, valign: "top" });
      y += 0.9;
    }
    slideNumber(s, 2);
    s.addNotes("Definitions follow the brief: three target groups (switchers, leavers, retired) and five instrument categories (financial incentives; information & nudges; support & training; flexible positions; flexible re-certification).");
  }

  // ================= 3. POLICY SLIDES =================
  let n = 3;
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
    const dr = [];
    p.desc.forEach(([lab, txt], i) => {
      dr.push({ text: lab + ": ", options: { bold: true, color: INK } });
      dr.push({ text: txt, options: { color: INK, breakLine: i < p.desc.length - 1 } });
    });
    s.addText(dr, { x: 1.95, y: 2.62, w: 10.65, h: 2.68, fontFace: BODY, fontSize: 15, color: INK, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.04, paraSpaceAfter: 4 });
    // secondary instruments line (replaces the former fact chips)
    const alsoChip = (p.chips || []).find(t => /^Also:/.test(t));
    const also = alsoChip ? alsoChip.replace(/^Also:\s*/, "").replace(/\s*\(.*\)$/, "") : null;
    s.addText([
      { text: "Secondary instruments: ", options: { bold: true, color: INK } },
      { text: also || "none (single-instrument policy)", options: { color: INK } }
    ], { x: 1.95, y: 5.32, w: 10.65, h: 0.3, fontFace: BODY, fontSize: 11.5, color: INK, margin: 0, isTextBox: true, valign: "middle" });
    // footer: sources (clickable)
    const runs = [];
    p.sources.forEach((u, i) => {
      runs.push({ text: i === 0 ? "Source: " : "Source (see also): ", options: { bold: true, color: INK, breakLine: false } });
      runs.push({ text: u, options: { hyperlink: { url: u, tooltip: u }, color: ACCENT, underline: { style: "sng", color: ACCENT }, breakLine: i < p.sources.length - 1 } });
    });
    s.addText(runs, { x: 0.5, y: 5.92, w: 12.33, h: 0.95, fontFace: BODY, fontSize: 10, color: INK, margin: 0, isTextBox: true, valign: "top" });
    slideNumber(s, n);
    s.addNotes(`${p.country}${p.region ? " (" + p.region + ")" : ""} — ${p.cat} — Target: ${p.groups.join(", ")}.\n\n${p.notes}`);
    n++;
  }

  // ================= 4. SUMMARY TABLE =================
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("Summary: 16 policies at a glance", { x: 0.5, y: 0.3, w: 9, h: 0.6, fontFace: HEAD, fontSize: 28, bold: true, color: INK, margin: 0, isTextBox: true });
    const hdr = ["Country", "Policy", "Category", "Target group(s)"].map(t => ({ text: t, options: { bold: true, color: WHITE, fill: { color: GREEN }, fontSize: 10.5, valign: "middle" } }));
    const rows = [hdr];
    POLICIES.forEach((p, i) => {
      const fill = i % 2 === 0 ? WHITE : "F4F8F6";
      const o = { color: INK, fontSize: 9.5, fill: { color: fill }, valign: "middle" };
      rows.push([
        { text: p.country + (p.region ? " (" + p.region + ")" : ""), options: { ...o, bold: true } },
        { text: p.title, options: { ...o } },
        { text: p.cat, options: { ...o } },
        { text: p.groups.join(" / "), options: { ...o } },
      ]);
    });
    s.addTable(rows, { x: 0.5, y: 1.3, w: 12.33, colW: [2.35, 5.85, 2.2, 1.93], fontFace: BODY, border: { type: "solid", pt: 0.5, color: LINE }, margin: [2, 5, 2, 5], rowH: 0.28, autoPage: false });
    slideNumber(s, n);
    s.addNotes("Summary table of all policies in the deck, in the same order as the slides.");
  }

  const out = path.join(__dirname, "Re-attracting_Former_Teachers.pptx");
  await pres.writeFile({ fileName: out });
  console.log("written", out);
})().catch(e => { console.error(e); process.exit(1); });
