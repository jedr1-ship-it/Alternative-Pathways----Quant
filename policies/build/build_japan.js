// One policy slide, Japan (Miyazaki Prefecture), in the layout of the main deck.
const pptxgen = require("pptxgenjs");
const fs = require("fs"), path = require("path"), sharp = require("sharp");
const React = require("react"), ReactDOMServer = require("react-dom/server"), Fa = require("react-icons/fa");
const GREEN = "1F4E46", SAGE = "EAF2EE", INK = "24313A", ACCENT = "B3542E", WHITE = "FFFFFF", LINE = "CFDCD5";
const OFF = "DCE6E0", OFF_ICON = "AFC0B8", MUTED = "7C8B93";
const HEAD = "Cambria", BODY = "Calibri", W = 13.333, H = 7.5;
const SCALE_COLORS = { Large: GREEN, Medium: "C8892B", Small: ACCENT };
const CATS = [
  { name: "Financial incentives", icon: "FaCoins" },
  { name: "Information & nudges", icon: "FaEnvelopeOpenText" },
  { name: "Support & training", icon: "FaChalkboardTeacher" },
  { name: "Flexible positions", icon: "FaUserClock" },
  { name: "Flexible re-certification", icon: "FaCertificate" },
];

const P = {
  country: "Japan", region: "Miyazaki Prefecture", flag: "jp", scale: "Medium",
  groups: ["Switchers", "Leavers"],
  used: ["Information & nudges", "Flexible positions", "Support & training"],
  title: "Information session on the appeal of teaching, for licence holders not working in schools (Prefectural Board of Education, 2025)",
  desc: "The Prefectural Board of Education holds an information session for people who hold a teaching licence but are not working in schools, a large group in Japan because any accredited university can award the licence after a short practicum. The session shows them what a teacher's day looks like now and how lessons, pupil guidance and club duties have changed since they did their practicum, the professional development on offer, and above all the posts they can take without sitting the competitive examination for a permanent job: temporary full-time teacher, part-time teacher or school support staff, each with its hours and pay. It ends with individual consultations and registration as a temporary teacher, so that the prefecture can call them when a vacancy appears. There is no financial incentive; the session is built around the doubts that keep licence holders away, being out of date, the workload, not feeling ready for a permanent post. No figures on attendance or on how many went on to teach have been published, and there is as yet almost no research in Japan on how these initiatives work.",
  sources: [
    { text: "Miyazaki Prefectural Board of Education, poster for the session (in Japanese)", url: "https://www.pref.miyazaki.lg.jp/documents/102783/102783_20250930165145-1.pdf" },
    { text: "Miyazaki Prefectural Board of Education, 'Information session on the Appeal of Teaching' (2025), slides shared with the OECD and translated by Mamoru Kikuchihara, National Institute of Fitness and Sports in Kanoya; correspondence, August to September 2026" },
  ],
  notes: "Facts from the 2025 session slides of the Miyazaki Prefectural Board of Education (translated by M. Kikuchihara) and from his e-mails of 5 August 2026: open licensing system (any accredited university, practicum of three to four weeks), large pool of inactive licence holders, boards of education across Japan running sessions to bring them back, returners recruited as fixed-term or substitute teachers without the competitive examination, no financial incentive known, almost no empirical research yet. Session content: a teacher's day then and now, Hinata Learning, student guidance as team work, club-activity rest days, in-school and self-directed professional development (Hinata Teacher Academy, NITS on-demand modules), three types of post (temporary full-time teacher, starting pay 241,900 yen a month for a new graduate; fiscal-year part-time teacher, up to 680 hours a year at 2,860 yen an hour; municipal school support staff, up to 800 hours a year at about 1,000 yen an hour), registration with the prefecture as a temporary teacher, next recruitment examination 13 June 2026, individual consultations. Contacts: Mr Ogata and Mr Noguchi, Teacher Recruitment and Professional Development Section, Personnel Division, Miyazaki Prefectural Board of Education.",
};

async function flagPng(code) {
  const svg = fs.readFileSync(path.join(__dirname, "node_modules/flag-icons/flags/4x3", code + ".svg"));
  return "image/png;base64," + (await sharp(svg, { density: 300 }).resize(600, 450).png().toBuffer()).toString("base64");
}
async function iconPng(name, color) {
  let svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Fa[name], { size: 256 }));
  svg = svg.replace(/currentColor/g, "#" + color); if (!/xmlns=/.test(svg)) svg = svg.replace(/<svg /, "<svg xmlns=\"http://www.w3.org/2000/svg\" ");
  const buf = await sharp(Buffer.from(svg), { density: 300 }).resize(256, 256, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE";
  pres.author = "José Manuel Torres, José Elías Durán Roa"; pres.title = "Japan — Miyazaki Prefecture";
  const icons = {}, iconsOff = {};
  for (const c of CATS) { icons[c.name] = await iconPng(c.icon, WHITE); iconsOff[c.name] = await iconPng(c.icon, OFF_ICON); }
  const flag = await flagPng(P.flag);

  const s = pres.addSlide(); s.background = { color: WHITE };
  s.addImage({ data: flag, x: 0.5, y: 0.42, w: 1.05, h: 0.7875 });
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 0.42, w: 1.05, h: 0.7875, fill: { type: "none" }, line: { color: LINE, width: 0.75 } });
  s.addText(P.country, { x: 1.75, y: 0.42, w: 9.1, h: 0.5, fontFace: BODY, fontSize: 22, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
  s.addText(P.region, { x: 1.75, y: 0.92, w: 9.1, h: 0.34, fontFace: BODY, fontSize: 13, color: INK, margin: 0, isTextBox: true, valign: "top" });
  // scale, top right
  s.addShape(pres.ShapeType.roundRect, { x: 11.03, y: 0.42, w: 1.8, h: 0.47, fill: { color: SCALE_COLORS[P.scale] }, line: { color: SCALE_COLORS[P.scale], width: 0 }, rectRadius: 0.235 });
  s.addText(P.scale, { x: 11.03, y: 0.42, w: 1.8, h: 0.47, fontFace: BODY, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
  // card
  s.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.5, w: 12.33, h: 4.22, fill: { color: SAGE }, line: { color: SAGE, width: 0 }, rectRadius: 0.12 });
  s.addText(P.title, { x: 0.95, y: 1.7, w: 11.43, h: 0.9, fontFace: HEAD, fontSize: 21, bold: true, color: INK, margin: 0, isTextBox: true, valign: "top" });
  s.addText(P.desc, { x: 0.95, y: 2.64, w: 11.43, h: 2.85, fontFace: BODY, fontSize: 14.5, color: INK, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.06 });
  // sources: a link where there is one, plain text where there is not
  const runs = [];
  P.sources.forEach((src, i) => {
    runs.push({ text: i === 0 ? "Source: " : "Source (see also): ", options: { bold: true, color: INK, breakLine: false } });
    if (src.url) runs.push({ text: src.url, options: { hyperlink: { url: src.url, tooltip: src.text }, color: ACCENT, underline: { style: "sng", color: ACCENT }, breakLine: i < P.sources.length - 1 } });
    else runs.push({ text: src.text, options: { color: INK, breakLine: i < P.sources.length - 1 } });
  });
  s.addText(runs, { x: 0.5, y: 5.8, w: 8.3, h: 0.9, fontFace: BODY, fontSize: 10, color: INK, margin: 0, isTextBox: true, valign: "top" });
  // instrument dots, bottom right, with the target groups under them
  const d = 0.62, gap = 0.20, x0 = 12.83 - (5 * d + 4 * gap);
  CATS.forEach((c, i) => {
    const on = P.used.includes(c.name), x = x0 + i * (d + gap);
    s.addShape(pres.ShapeType.ellipse, { x, y: 6.26, w: d, h: d, fill: { color: on ? GREEN : OFF }, line: { color: on ? GREEN : OFF, width: 0 } });
    const pad = d * 0.24;
    s.addImage({ data: on ? icons[c.name] : iconsOff[c.name], x: x + pad, y: 6.26 + pad, w: d - 2 * pad, h: d - 2 * pad });
  });
  s.addText(P.groups.join(" / "), { x: 7.8, y: 6.97, w: 5.03, h: 0.28, fontFace: BODY, fontSize: 10.5, color: MUTED, align: "right", margin: 0, isTextBox: true, valign: "middle" });
  s.addNotes(`${P.country} (${P.region}) — Instruments lit: ${P.used.join(", ")} — Target: ${P.groups.join(", ")}.\n\n${P.notes}`);

  const out = path.join(__dirname, "Japan_Miyazaki_slide.pptx");
  await pres.writeFile({ fileName: out }); console.log("written", out);
})().catch(e => { console.error(e); process.exit(1); });
