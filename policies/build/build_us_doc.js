// The United States interview script as one Word document, with the verified state-by-state table.
const fs = require("fs"), path = require("path"), D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageOrientation,
        Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, convertInchesToTwip } = D;
const SRC = "/home/user/Alternative-Pathways----Quant/policies/interviews/united_states.md";
const FONT = "Garamond", BLACK = "000000", GREY = "555555", SZ = 24;

// ---- the table, every cell checked against the retirement system or legislature named in the sources ----
const COLS = ["State and law", "Who may return", "Waiting period", "Earnings limit", "Shortage required?", "How long / until when", "Pension while working"];
const ROWS = [
  ["Michigan\nPublic Act 147 of 2023 (signed 10 Oct 2023). Replaced PA 184 of 2022.",
   "Any retiree of the school employees' system with a bona fide termination of employment.",
   "Six consecutive months (nine under the 2022 law). A retiree may work before that if earnings stay under $15,100 in the calendar year.",
   "None once six months have passed.",
   "No.",
   "No limit on the return. The law expires 10 Oct 2028.",
   "Unaffected, including the insurance subsidy. Applies whether hired directly or through an agency."],
  ["Georgia\nHouse Bill 385 (2022), 1 Jul 2022 – 30 Jun 2026; replaced by Senate Bill 150 from 1 Jul 2026.",
   "HB 385: retirees with 30+ years of service, certified, hired full time as PreK-12 classroom teachers. SB 150: 25+ years per TRS's legislative update (its SB 150 page still shows 30 in one place; confirm).",
   "One year retired.",
   "None: full salary plus full pension.",
   "HB 385: yes, one of the three highest-need subjects of the region, set by the RESA. SB 150: no.",
   "SB 150 runs to 30 Jun 2034.",
   "Full pension continues. The 2025 state audit counted about 350 returners a year under HB 385."],
  ["New Mexico\nEducational Retirees Returning to Work Act, HB 73 (2022); SB 133 (signed 10 Apr 2025).",
   "Retirees of the Educational Retirement Board; each return is applied for and approved by the Board.",
   "90-day layout after retirement.",
   "None under the months-limited programme. Two alternatives exist: work at 0.25 FTE or less, or earn under $25,000 a fiscal year (was $15,000 before SB 133).",
   "No.",
   "Up to 60 consecutive or non-consecutive months (36 before SB 133).",
   "Full pension continues. Retiree and employer pay non-refundable contributions; no new service credit."],
  ["Louisiana\nAct 394 of 2024 (signed May 2024).",
   "Retired on or after 1 Jul 2020: full or part time as PreK-12 classroom teacher in specified subjects, or in a critical-shortage position. Retired before 1 Jul 2020: part time in a critical-shortage position.",
   "Twelve months.",
   "None in those positions.",
   "Yes for critical-shortage positions: the employer certifies the shortage to TRSL.",
   "No stated limit; certification is renewed with the employer.",
   "Neither suspended nor reduced. Both sides contribute, no new credit. Hired through a staffing agency: benefits suspended."],
  ["North Carolina\nGeneral return-to-work rule of the Teachers' and State Employees' Retirement System. Exception in force 1999–2009 (lapsed).",
   "Any TSERS retiree, after the break.",
   "Six months, during which no paid work for any system employer, substitute teaching included.",
   "The greater of 50% of pre-retirement pay or $42,160 (2026). Above that, the pension is suspended. From 1999 to 2009 retired teachers could return full time on full salary with no cap.",
   "No.",
   "No limit within the cap.",
   "Continues while earnings stay under the cap. Research on the 1999–2009 window finds returners went disproportionately to high-need schools."],
  ["Virginia\nCritical-shortage provisions administered by the Virginia Retirement System, break shortened from 12 to 6 months from 1 Jul 2023; Executive Directive 3 (2022) on licensure.",
   "VRS retirees hired full time into a certified critical-shortage position (teachers, principals, specialised student support, bus drivers). Not those retired under an early-retirement incentive or on disability, and no pre-arranged agreement before retiring.",
   "Six consecutive months with no work, paid or volunteer, for any VRS employer.",
   "None: full salary plus full benefit.",
   "Yes: the school division certifies the position each year (form VRS-160).",
   "The provisions expire 1 Jul 2028.",
   "Full benefit continues; no new service credit."],
];
const SOURCES = [
  "Michigan Office of Retirement Services, Public Act 147 of 2023 FAQs, michigan.gov/orsschools/pa-147-of-2023-faqs; archive of PA 184 of 2022, michigan.gov/psru.",
  "Teachers Retirement System of Georgia, HB 385 Employment and SB 150 Employment pages and Legislative Update, trsga.com; Georgia Department of Audits and Accounts, Retired Teachers Return to Work (2025).",
  "New Mexico Educational Retirement Board, Returning to Work after Retirement, erb.nm.gov; Legislative Education Study Committee analysis of SB 133 (2025), nmlegis.gov.",
  "Teachers' Retirement System of Louisiana, Regular Session News 18 and 19 (2024) and Return to Work FAQs, trsl.org.",
  "North Carolina Retirement Systems, Return to Work Laws, myncretirement.gov; Jarrold-Grapes, Retirees return to work: how a North Carolina policy helped staff high-need schools, Education Policy Analysis Archives.",
  "Virginia Retirement System, Critical Shortage Positions and Employer Update May 2023, varetire.org.",
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
  margins: { top: 60, bottom: 60, left: 80, right: 80 },
  children: text.split("\n").map((t, i) => new Paragraph({ spacing: { after: 40 },
    children: [new TextRun({ text: t, font: FONT, size: 17, bold: opts.head || (i === 0 && opts.first), color: BLACK })] })),
});
function table() {
  const widths = [1900, 2300, 1900, 2000, 1700, 1700, 2100]; // sum 13600 = landscape width inside 1" margins... adjusted below
  const total = 12960; const scale = total / widths.reduce((a, b) => a + b, 0);
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
  new Paragraph({ spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Checked against the following sources, September 2026:", font: FONT, size: 18, italics: true, color: GREY })] }),
  ...SOURCES.map(s => new Paragraph({ spacing: { after: 20 }, indent: { left: convertInchesToTwip(0.2), hanging: convertInchesToTwip(0.2) }, children: [new TextRun({ text: "– " + s, font: FONT, size: 18, color: GREY })] })),
];

const portrait = { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } };
const landscape = { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } };
const footer = new D.Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [D.PageNumber.CURRENT], font: FONT, size: 18, color: GREY })] })] });

const doc = new Document({
  creator: "José Manuel Torres, José Elías Durán Roa", title: "United States — interview script",
  styles: { default: { document: { run: { font: FONT, size: SZ, color: BLACK } } } },
  sections: [
    { properties: portrait, footers: { default: footer }, children: before },
    { properties: landscape, footers: { default: footer }, children: tableSection },
    { properties: portrait, footers: { default: footer }, children: after },
  ],
});
Packer.toBuffer(doc).then(buf => { const out = path.join(__dirname, "Interview_script_US.docx"); fs.writeFileSync(out, buf); console.log("written", out, buf.length); });
