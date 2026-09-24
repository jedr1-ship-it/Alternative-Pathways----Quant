// One Word document with the interview scripts: title, clickable index, scripts. Garamond throughout.
const fs = require("fs");
const path = require("path");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageBreak, convertInchesToTwip } = D;

const SRC = "/home/user/Alternative-Pathways----Quant/policies/interviews";
// file, country, region (null when the script is national), one-line subtitle under the heading
const FILES = [
  ["australia_nsw.md",      "Australia",     "New South Wales", "Teachers Re-Engage, since 2023"],
  ["australia_victoria.md", "Australia",     "Victoria",        "Teacher Re-Engagement Initiative, since 2022"],
  ["canada_quebec.md",      "Canada",        "Quebec",          "Measure 15178, pay for returning retired teachers, since 2020"],
  ["china.md",              "China",         null,              "Silver-Age Lecturing Plan, since 2018"],
  ["netherlands.md",        "Netherlands",   null,              "Grant to schools for re-hiring former teachers, 2017–2022"],
  ["united_states.md",      "United States", null,              "State laws on retired teachers returning to work"],
  ["sweden.md",             "Sweden",        null,              "Online course for returning teachers, since 2018"],
  ["new_zealand.md",        "New Zealand",   null,              "Return without a refresher course, with registration fees paid, since 2024"],
];
// optional: node build_doc.js --only netherlands.md,united_states.md --out Interview_scripts_NL_US.docx
const argv = process.argv.slice(2);
const argOf = k => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : null; };
const ONLY = argOf("--only"); const OUT = argOf("--out") || "Interview_scripts.docx";
const FILES_USED = ONLY ? FILES.filter(f => ONLY.split(",").includes(f[0])) : FILES;
// heading of each section: the region where a country has more than one script, otherwise the country
const countryCount = FILES_USED.reduce((m, f) => (m[f[1]] = (m[f[1]] || 0) + 1, m), {});
const headingOf = f => (countryCount[f[1]] > 1 ? f[2] : f[1]);
const subtitleOf = f => (countryCount[f[1]] > 1 || !f[2]) ? f[3] : f[2] + ". " + f[3];

const FONT = "Garamond", BLACK = "000000", GREY = "555555";
const SZ = 24; // 12 pt

function runs(text, opts = {}) {
  const out = [];
  text.split(/(\*\*[^*]+\*\*)/).forEach(part => {
    if (!part) return;
    const bold = /^\*\*.*\*\*$/.test(part);
    out.push(new TextRun({ text: bold ? part.slice(2, -2) : part, bold, font: FONT,
                           size: opts.size || SZ, color: opts.color || BLACK, italics: opts.italics }));
  });
  return out;
}

// join wrapped markdown lines into logical blocks
function blocks(md) {
  const out = []; let buf = null;
  const flush = () => { if (buf) { out.push(buf); buf = null; } };
  for (const raw of md.split("\n")) {
    const line = raw.replace(/\s+$/, "");
    if (!line.trim()) { flush(); continue; }
    if (line === "---") { flush(); continue; }
    let m;
    if ((m = line.match(/^(#{1,3})\s+(.*)$/))) { flush(); out.push({ kind: "h" + m[1].length, text: m[2] }); continue; }
    if ((m = line.match(/^(\d+)\.\s+(.*)$/))) { flush(); buf = { kind: "num", n: m[1], text: m[2] }; continue; }
    if (/^\s+- /.test(line)) { flush(); buf = { kind: "probe", text: line.trim().slice(2) }; continue; }
    if (line.startsWith("- ")) { flush(); buf = { kind: "bullet", text: line.slice(2) }; continue; }
    if (buf) { buf.text += " " + line.trim(); continue; }
    buf = { kind: "p", text: line.trim() };
  }
  flush();
  return out;
}

const children = [];

// ---------- title and index on the first page ----------
children.push(
  new Paragraph({ spacing: { after: 120 },
    children: [new TextRun({ text: "Re-attracting Former Teachers", font: FONT, size: 40, bold: true, color: BLACK })] }),
  new Paragraph({ spacing: { after: 480 },
    children: [new TextRun({ text: "Interview scripts", font: FONT, size: 28, color: GREY })] }),
);
// index: the country, and under it each region when a country has more than one script
let lastCountry = null;
FILES_USED.forEach((f, i) => {
  const [, country, region] = f;
  const link = (text, size, indent) => new Paragraph({
    spacing: { before: indent ? 40 : 120, after: 0 },
    indent: indent ? { left: convertInchesToTwip(0.35) } : undefined,
    children: [new D.InternalHyperlink({ anchor: "sec" + i, children: [
      new TextRun({ text, font: FONT, size, bold: !indent, color: BLACK, underline: { type: D.UnderlineType.SINGLE } })] })] });
  if (countryCount[country] > 1) {
    if (country !== lastCountry) children.push(new Paragraph({ spacing: { before: 120, after: 0 },
      children: [new TextRun({ text: country, font: FONT, size: SZ, bold: true, color: BLACK })] }));
    children.push(link(region, 22, true));
  } else {
    children.push(link(country, SZ, false));
  }
  lastCountry = country;
});
children.push(new Paragraph({ children: [new PageBreak()] }));

// ---------- the scripts ----------
FILES_USED.forEach((f, idx) => {
  const [file] = f; const title = headingOf(f); const sub = subtitleOf(f);
  const bs = blocks(fs.readFileSync(path.join(SRC, file), "utf8"));
  bs.forEach(b => {
    if (b.kind === "h1") {
      children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 0, after: sub ? 0 : 200 },
        children: [new D.Bookmark({ id: "sec" + idx, children: [new TextRun({ text: title, font: FONT, size: 32, bold: true, color: BLACK })] })] }));
      if (sub) children.push(new Paragraph({ spacing: { after: 240 },
        children: [new TextRun({ text: sub, font: FONT, size: 22, italics: true, color: GREY })] }));
      return;
    }
    if (b.kind === "h2") return; // the long policy name: replaced by the short subtitle above
    if (b.kind === "h3") {
      children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 80 },
        children: [new TextRun({ text: b.text, font: FONT, size: 26, bold: true, color: BLACK })] }));
      return;
    }
    if (b.kind === "num") {
      children.push(new Paragraph({ spacing: { before: 200, after: 60 },
        indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.35) },
        children: [new TextRun({ text: b.n + ".\t", font: FONT, size: SZ, bold: true, color: BLACK }), ...runs(b.text)] }));
      return;
    }
    if (b.kind === "probe") {
      children.push(new Paragraph({ spacing: { before: 0, after: 40 },
        indent: { left: convertInchesToTwip(0.7), hanging: convertInchesToTwip(0.2) },
        children: [new TextRun({ text: "–\t", font: FONT, size: 21, color: GREY }), ...runs(b.text, { size: 21, color: GREY })] }));
      return;
    }
    if (b.kind === "bullet") {
      children.push(new Paragraph({ spacing: { before: 40, after: 60 },
        indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.2) },
        children: [new TextRun({ text: "–\t", font: FONT, size: SZ }), ...runs(b.text)] }));
      return;
    }
    children.push(new Paragraph({ spacing: { before: 100, after: 100 }, children: runs(b.text) }));
  });
  if (idx < FILES_USED.length - 1) children.push(new Paragraph({ children: [new PageBreak()] }));
});

const doc = new Document({
  creator: "José Manuel Torres, José Elías Durán Roa",
  title: "Re-attracting Former Teachers — Interview scripts",
  styles: { default: { document: { run: { font: FONT, size: SZ, color: BLACK } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new D.Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [new TextRun({ children: [D.PageNumber.CURRENT], font: FONT, size: 18, color: GREY })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname, OUT);
  fs.writeFileSync(out, buf);
  console.log("written", out, buf.length);
});
