const fs = require("fs");
const path = require("path");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, TableOfContents,
        AlignmentType, PageBreak, BorderStyle, PageOrientation, convertInchesToTwip } = D;

const SRC = "/home/user/Alternative-Pathways----Quant/policies/interviews";
const FILES = [
  ["_introduction.md",      "The introduction we use in every interview"],
  ["_how_to_use.md",        "How to use these scripts"],
  ["australia_nsw.md",      null],
  ["australia_victoria.md", null],
  ["canada_quebec.md",      null],
  ["china.md",              null],
  ["netherlands.md",        null],
  ["united_states.md",      null],
];

const INK = "24313A", GREEN = "1F4E46", ACCENT = "B3542E", MUTED = "5A6A72";
const HEAD = "Cambria", BODY = "Calibri";

// split a markdown line into runs, honouring **bold**
function runs(text, opts = {}) {
  const out = [];
  text.split(/(\*\*[^*]+\*\*)/).forEach(part => {
    if (!part) return;
    const bold = /^\*\*.*\*\*$/.test(part);
    out.push(new TextRun({ text: bold ? part.slice(2, -2) : part, bold, font: BODY,
                           size: opts.size || 22, color: opts.color || INK, italics: opts.italics }));
  });
  return out;
}

// join wrapped markdown lines into logical blocks
function blocks(md) {
  const lines = md.split("\n");
  const out = [];
  let buf = null;
  const flush = () => { if (buf) { out.push(buf); buf = null; } };
  for (const raw of lines) {
    const line = raw.replace(/\s+$/, "");
    if (!line.trim()) { flush(); continue; }
    if (line === "---") { flush(); out.push({ kind: "rule" }); continue; }
    let m;
    if ((m = line.match(/^(#{1,3})\s+(.*)$/))) {
      flush(); out.push({ kind: "h" + m[1].length, text: m[2] }); continue;
    }
    if ((m = line.match(/^(\d+)\.\s+(.*)$/))) {
      flush(); buf = { kind: "num", n: m[1], text: m[2] }; continue;
    }
    if (line.startsWith("> ")) { flush(); buf = { kind: "quote", text: line.slice(2) }; continue; }
    if (/^\s+- /.test(line)) { flush(); buf = { kind: "probe", text: line.trim().slice(2) }; continue; }
    if (line.startsWith("- ")) { flush(); buf = { kind: "bullet", text: line.slice(2) }; continue; }
    if (buf) { buf.text += " " + line.trim(); continue; }
    buf = { kind: "p", text: line.trim() };
  }
  flush();
  return out;
}

// section titles, in order, for the contents list
const SECTIONS = FILES.map(([file, override]) => {
  const first = fs.readFileSync(path.join(SRC, file), "utf8").split("\n").find(l => l.startsWith("# "));
  const md = fs.readFileSync(path.join(SRC, file), "utf8");
  const sub = md.split("\n").find(l => l.startsWith("## "));
  return { title: override || first.slice(2).trim(), sub: sub ? sub.slice(3).trim() : null };
});

const children = [];

// ---------- cover ----------
children.push(
  new Paragraph({ spacing: { before: 2600, after: 0 },
    children: [new TextRun({ text: "Re-attracting Former Teachers", font: HEAD, size: 56, bold: true, color: GREEN })] }),
  new Paragraph({ spacing: { before: 200, after: 0 },
    children: [new TextRun({ text: "Interview scripts for the countries we are contacting", font: BODY, size: 28, color: MUTED })] }),
  new Paragraph({ spacing: { before: 1200 },
    children: [new TextRun({ text: "OECD Centre for Educational Research and Innovation", font: BODY, size: 22, color: INK })] }),
  new Paragraph({ spacing: { before: 60 },
    children: [new TextRun({ text: "Unlocking the Potential of Diverse Teaching Profiles", font: BODY, size: 22, italics: true, color: MUTED })] }),
  new Paragraph({ spacing: { before: 400 },
    children: [new TextRun({ text: "José Manuel Torres  ·  José Elías Durán Roa", font: BODY, size: 22, color: INK })] }),
  new Paragraph({ spacing: { before: 60 },
    children: [new TextRun({ text: "September 2026", font: BODY, size: 22, color: MUTED })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- table of contents ----------
children.push(
  new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { after: 240 },
    children: [new TextRun({ text: "Contents", font: HEAD, size: 36, bold: true, color: GREEN })] }),
  new Paragraph({ spacing: { after: 200 },
    children: [new TextRun({ text: "Click a country to jump to its script.", font: BODY, size: 20, italics: true, color: MUTED })] }),
  ...SECTIONS.flatMap((sec, i) => {
    const runsIn = [new TextRun({ text: sec.title, font: BODY, size: 24, bold: true, color: GREEN,
                                  underline: { type: D.UnderlineType.SINGLE, color: GREEN } })];
    const para = new Paragraph({
      spacing: { before: 140, after: sec.sub ? 20 : 140 },
      children: [new D.InternalHyperlink({ anchor: "sec" + i, children: runsIn })] });
    if (!sec.sub) return [para];
    return [para, new Paragraph({
      spacing: { after: 140 }, indent: { left: convertInchesToTwip(0.0) },
      children: [new TextRun({ text: sec.sub, font: BODY, size: 20, color: MUTED })] })];
  }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------- the scripts ----------
FILES.forEach(([file, overrideTitle], idx) => {
  const md = fs.readFileSync(path.join(SRC, file), "utf8");
  const bs = blocks(md);
  let seenH1 = false;
  bs.forEach(b => {
    if (b.kind === "h1") {
      seenH1 = true;
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: idx === 0 ? 0 : 240, after: 60 },
        children: [new D.Bookmark({ id: "sec" + idx,
          children: [new TextRun({ text: overrideTitle || b.text, font: HEAD, size: 36, bold: true, color: GREEN })] })] }));
      return;
    }
    if (b.kind === "h2") {
      children.push(new Paragraph({
        spacing: { before: 0, after: 240 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "CFDCD5", space: 6 } },
        children: [new TextRun({ text: b.text, font: BODY, size: 24, color: ACCENT })] }));
      return;
    }
    if (b.kind === "h3") {
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { before: 320, after: 120 },
        children: [new TextRun({ text: b.text, font: HEAD, size: 26, bold: true, color: INK })] }));
      return;
    }
    if (b.kind === "rule") return;
    if (b.kind === "num") {
      children.push(new Paragraph({
        spacing: { before: 200, after: 80 },
        indent: { left: convertInchesToTwip(0.45), hanging: convertInchesToTwip(0.3) },
        children: [new TextRun({ text: b.n + ".", font: BODY, size: 22, bold: true, color: GREEN }),
                   new TextRun({ text: "\t", font: BODY, size: 22 }),
                   ...runs(b.text)] }));
      return;
    }
    if (b.kind === "probe") {
      children.push(new Paragraph({
        spacing: { before: 0, after: 60 },
        indent: { left: convertInchesToTwip(0.85), hanging: convertInchesToTwip(0.2) },
        children: [new TextRun({ text: "–\t", font: BODY, size: 20, color: MUTED }), ...runs(b.text, { size: 20, color: MUTED })] }));
      return;
    }
    if (b.kind === "bullet") {
      children.push(new Paragraph({
        spacing: { before: 40, after: 80 },
        indent: { left: convertInchesToTwip(0.45), hanging: convertInchesToTwip(0.2) },
        children: [new TextRun({ text: "—\t", font: BODY, size: 22, color: MUTED }), ...runs(b.text)] }));
      return;
    }
    if (b.kind === "quote") {
      children.push(new Paragraph({
        spacing: { before: 120, after: 120 },
        indent: { left: convertInchesToTwip(0.35) },
        border: { left: { style: BorderStyle.SINGLE, size: 12, color: "CFDCD5", space: 12 } },
        children: runs(b.text, { italics: true }) }));
      return;
    }
    // plain paragraph; the "what we already know" block is set apart
    const isContext = /^\*\*(Who to ask for|What we already know|Note for the interviewer)/.test(b.text);
    children.push(new Paragraph({
      spacing: { before: 120, after: 120 },
      shading: isContext ? { type: D.ShadingType.CLEAR, fill: "F1F6F3" } : undefined,
      indent: isContext ? { left: convertInchesToTwip(0.15), right: convertInchesToTwip(0.15) } : undefined,
      children: runs(b.text, isContext ? { size: 21 } : {}) }));
  });
  if (idx < FILES.length - 1) children.push(new Paragraph({ children: [new PageBreak()] }));
});

const doc = new Document({
  creator: "José Manuel Torres, José Elías Durán Roa",
  title: "Re-attracting Former Teachers — Interview scripts",
  styles: { default: { document: { run: { font: BODY, size: 22, color: INK } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
                          margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: {
      default: new D.Footer({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ children: [D.PageNumber.CURRENT], font: BODY, size: 18, color: MUTED })] })] }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname, "Interview_scripts.docx");
  fs.writeFileSync(out, buf);
  console.log("written", out, buf.length);
});
