// The United States interview script as one Word document, with the verified state-by-state table.
const fs = require("fs"), path = require("path"), D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageOrientation,
        Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, convertInchesToTwip } = D;
const SRC = "/home/user/Alternative-Pathways----Quant/policies/interviews/united_states.md";
const FONT = "Garamond", BLACK = "000000", GREY = "555555", SZ = 24;

// ---- the table, every cell checked against the retirement system or legislature named in the sources ----
const COLS = ["State", "The law", "Who can come back", "How long they must wait", "Limit on what they earn", "Must the district show a shortage?", "Until when"];
const ROWS = [
  ["Michigan", "Law of 2023, in force until October 2028.",
   "Any retired school employee who has fully left their job.",
   "Six months. Before that, only if they earn under $15,100 in the year.",
   "None after six months.", "No.", "October 2028."],
  ["Georgia", "Law of 2022, replaced by a new law from July 2026.",
   "Retired teachers with 30 years of service (25 from July 2026, to confirm), hired full time in a classroom.",
   "One year.", "None.",
   "Until June 2026, yes: one of the three subjects most in need in the region. From July 2026, no.",
   "June 2034."],
  ["New Mexico", "Law of 2022, extended in 2025.",
   "Any retired educator, with the retirement board's approval of each return.",
   "90 days.", "None. (Other options: part time, or under $25,000 a year.)", "No.",
   "Up to 60 months of work in total."],
  ["Louisiana", "Law of 2024.",
   "Retired after mid-2020: full or part time as a classroom teacher in listed subjects, or in a shortage post. Retired before mid-2020: part time in a shortage post.",
   "Twelve months.", "None in those posts.", "Yes, for shortage posts: the district certifies it.", "No limit stated."],
  ["North Carolina", "Standing rule. A more generous exception ran from 1999 to 2009.",
   "Any retired teacher.", "Six months.",
   "Half of the former salary or $42,160, whichever is higher. Above that the pension stops.", "No.", "No limit."],
  ["Virginia", "Shortage rule, wait shortened in 2023. A 2022 governor's directive eased licence renewal.",
   "Retired teachers and school staff hired full time into a post the district certifies as a shortage.",
   "Six months.", "None.", "Yes, certified by the district every year.", "July 2028."],
];
const NOTE = "In all six states the pension keeps being paid in full while the retiree works under these rules (in North Carolina, as long as earnings stay under the limit). In Louisiana, a retiree hired through a staffing agency loses that protection and the pension is suspended.";
const SOURCES = [
  "Michigan: Office of Retirement Services, Public Act 147 of 2023 (michigan.gov/orsschools).",
  "Georgia: Teachers Retirement System of Georgia, House Bill 385 and Senate Bill 150 pages (trsga.com); state audit of 2025.",
  "New Mexico: Educational Retirement Board, Returning to Work after Retirement (erb.nm.gov); legislative analysis of Senate Bill 133, 2025.",
  "Louisiana: Teachers' Retirement System of Louisiana, Act 394 of 2024 and Return to Work FAQs (trsl.org).",
  "North Carolina: state retirement system, Return to Work Laws (myncretirement.gov); Jarrold-Grapes on the 1999-2009 policy, Education Policy Analysis Archives.",
  "Virginia: Virginia Retirement System, Critical Shortage Positions (varetire.org).",
];

function runs(text, o = {}) {
  return text.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(part => {
    const bold = /^\*\*.*\*\*$/.test(part);
    return new TextRun({ text: bold ? part.slice(2, -2) : part, bold, font: FONT, size: o.size || SZ, color: o.color || BLACK, italics: o.italics });
  });
}
function blocks(md) {
  const out = []; let buf = null; const flush = () => { if (buf) { out.push(buf); buf = null; } };
  for (const raw of md.split("\n")) {
    const line = raw.replace(/\s+$/, ""); let m;
    if (!line.trim()) { flush(); continue; }
    if (line === "---") { flush(); continue; }
    if (line === "[[TABLE]]") { flush(); out.push({ kind: "table" }); continue; }
    if ((m = line.match(/^(#{1,3})\s+(.*)$/))) { flush(); out.push({ kind: "h" + m[1].length, text: m[2] }); continue; }
    if ((m = line.match(/^(\d+)\.\s+(.*)$/))) { flush(); buf = { kind: "num", n: m[1], text: m[2] }; continue; }
    if (/^\s+- /.test(line)) { flush(); buf = { kind: "probe", text: line.trim().slice(2) }; continue; }
    if (line.startsWith("- ")) { flush(); buf = { kind: "bullet", text: line.slice(2) }; continue; }
    if (buf) { buf.text += " " + line.trim(); continue; }
    buf = { kind: "p", text: line.trim() };
  }
  flush(); return out;
}
const cell = (text, opts = {}) => new TableCell({
  width: { size: opts.w, type: WidthType.DXA },
  shading: opts.head ? { type: ShadingType.CLEAR, fill: "E8E8E8" } : undefined,
  margins: { top: 40, bottom: 40, left: 60, right: 60 },
  children: text.split("\n").map((t, i) => new Paragraph({ spacing: { after: 40 },
    children: [new TextRun({ text: t, font: FONT, size: 16, bold: opts.head || (i === 0 && opts.first), color: BLACK })] })),
});
function table() {
  const widths = [1000, 1400, 2000, 1250, 1450, 1350, 910];
  const total = 9360; const scale = total / widths.reduce((a, b) => a + b, 0);
  const W = widths.map(w => Math.round(w * scale));
  const border = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: W,
    borders: { top: border, bottom: border, left: border, right: border, insideHorizontal: border, insideVertical: border },
    rows: [
      new TableRow({ tableHeader: true, children: COLS.map((c, i) => cell(c, { w: W[i], head: true })) }),
      ...ROWS.map(r => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, { w: W[i], first: i === 0 })) })),
    ],
  });
}

const before = [], after = []; let target = before; let sub = null;
const bs = blocks(fs.readFileSync(SRC, "utf8"));
bs.forEach(b => {
  if (b.kind === "table") { target = after; return; }
  if (b.kind === "h1") { target.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { after: 0 }, children: [new TextRun({ text: "United States", font: FONT, size: 32, bold: true, color: BLACK })] })); return; }
  if (b.kind === "h2") { target.push(new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: b.text, font: FONT, size: 22, italics: true, color: GREY })] })); return; }
  if (b.kind === "h3") { target.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 80 }, children: [new TextRun({ text: b.text, font: FONT, size: 26, bold: true, color: BLACK })] })); return; }
  if (b.kind === "num") { target.push(new Paragraph({ spacing: { before: 200, after: 60 }, indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.35) }, children: [new TextRun({ text: b.n + ".\t", font: FONT, size: SZ, bold: true }), ...runs(b.text)] })); return; }
  if (b.kind === "probe") { target.push(new Paragraph({ spacing: { after: 40 }, indent: { left: convertInchesToTwip(0.7), hanging: convertInchesToTwip(0.2) }, children: [new TextRun({ text: "–\t", font: FONT, size: 21, color: GREY }), ...runs(b.text, { size: 21, color: GREY })] })); return; }
  if (b.kind === "bullet") { target.push(new Paragraph({ spacing: { before: 40, after: 60 }, indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.2) }, children: [new TextRun({ text: "–\t", font: FONT, size: SZ }), ...runs(b.text)] })); return; }
  target.push(new Paragraph({ spacing: { before: 100, after: 100 }, children: runs(b.text) }));
});

const tableSection = [
  new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Return-to-work rules for retired teachers in the six states", font: FONT, size: 24, bold: true })] }),
  table(),
  new Paragraph({ spacing: { before: 120, after: 80 }, children: [new TextRun({ text: NOTE, font: FONT, size: 18 })] }),
  new Paragraph({ spacing: { before: 80, after: 40 }, children: [new TextRun({ text: "Checked against these sources in September 2026:", font: FONT, size: 17, italics: true, color: GREY })] }),
  ...SOURCES.map(s => new Paragraph({ spacing: { after: 20 }, indent: { left: convertInchesToTwip(0.2), hanging: convertInchesToTwip(0.2) }, children: [new TextRun({ text: "– " + s, font: FONT, size: 17, color: GREY })] })),
];

const portrait = { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } };
const landscape = { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } };
const footer = new D.Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [D.PageNumber.CURRENT], font: FONT, size: 18, color: GREY })] })] });

const doc = new Document({
  creator: "José Manuel Torres, José Elías Durán Roa", title: "United States — interview script",
  styles: { default: { document: { run: { font: FONT, size: SZ, color: BLACK } } } },
  sections: [
    { properties: portrait, footers: { default: footer }, children: before },
    { properties: portrait, footers: { default: footer }, children: tableSection },
    { properties: portrait, footers: { default: footer }, children: after },
  ],
});
Packer.toBuffer(doc).then(buf => { const out = path.join(__dirname, "Interview_script_US.docx"); fs.writeFileSync(out, buf); console.log("written", out, buf.length); });
