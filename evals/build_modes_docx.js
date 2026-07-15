/**
 * Build noslop modes comparison DOCX from evals/results/modes drafts + voice JSON.
 */
const fs = require("fs");
const path = require("path");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  HeadingLevel,
  BorderStyle,
  WidthType,
  ShadingType,
  Header,
  Footer,
  PageNumber,
  AlignmentType,
  PageBreak,
} = require("docx");

const ROOT = path.join(__dirname, "..");
const MODES = path.join(ROOT, "evals", "results", "modes");
const OUT = path.join(ROOT, "evals", "results", "noslop_modes_comparison.docx");

const BRIEFS = ["mall_shoe", "cold_email"];
const ARMS = ["default", "modest", "balanced", "max"];
const BRIEF_LABEL = {
  mall_shoe: "Mall shoe (short fiction)",
  cold_email: "Cold email",
};
const MODE_LABEL = {
  default: "default (control — raw slop)",
  modest: "modest (natural flow)",
  balanced: "balanced (ship default)",
  max: "max (research / craft pressure)",
};

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

function cell(text, opts = {}) {
  const { bold = false, fill = null, width = 2340 } = opts;
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: fill ? { fill, type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: String(text),
            bold,
            font: "Arial",
            size: 18,
          }),
        ],
      }),
    ],
  });
}

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after ?? 160 },
    children: [
      new TextRun({
        text,
        font: "Arial",
        size: opts.size ?? 22,
        bold: !!opts.bold,
        italics: !!opts.italics,
        color: opts.color,
      }),
    ],
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 280, after: 200 },
    children: [new TextRun({ text, font: "Arial", bold: true, size: 32 })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 160 },
    children: [new TextRun({ text, font: "Arial", bold: true, size: 26 })],
  });
}

function draftParas(text) {
  return text
    .split(/\n/)
    .map((line) =>
      new Paragraph({
        spacing: { after: line.trim() ? 80 : 40 },
        children: [
          new TextRun({
            text: line.length ? line : " ",
            font: "Consolas",
            size: 18,
          }),
        ],
      })
    );
}

function loadScores() {
  const map = {};
  for (const brief of BRIEFS) {
    map[brief] = {};
    for (const arm of ARMS) {
      const j = JSON.parse(
        fs.readFileSync(path.join(MODES, `${brief}_${arm}_voice.json`), "utf8")
      );
      map[brief][arm] = j;
    }
  }
  return map;
}

function loadDraft(brief, arm) {
  return fs.readFileSync(path.join(MODES, `${brief}_${arm}.md`), "utf8").trim();
}

function scoreTable(scores) {
  const header = new TableRow({
    children: [
      cell("Brief", { bold: true, fill: "E8EEF7", width: 2200 }),
      cell("default", { bold: true, fill: "E8EEF7", width: 1790 }),
      cell("modest", { bold: true, fill: "E8EEF7", width: 1790 }),
      cell("balanced", { bold: true, fill: "E8EEF7", width: 1790 }),
      cell("max", { bold: true, fill: "E8EEF7", width: 1790 }),
    ],
  });
  const rows = BRIEFS.map((brief) => {
    const b = scores[brief];
    return new TableRow({
      children: [
        cell(BRIEF_LABEL[brief], { width: 2200 }),
        cell(
          `${b.default.score.toFixed(2)} (${b.default.hard_fail ? "HARD" : b.default.gate})`,
          { width: 1790 }
        ),
        cell(
          `${b.modest.score.toFixed(2)} (${b.modest.hard_fail ? "HARD" : b.modest.gate})`,
          { width: 1790 }
        ),
        cell(
          `${b.balanced.score.toFixed(2)} (${b.balanced.hard_fail ? "HARD" : b.balanced.gate})`,
          { width: 1790 }
        ),
        cell(
          `${b.max.score.toFixed(2)} (${b.max.hard_fail ? "HARD" : b.max.gate})`,
          { width: 1790 }
        ),
      ],
    });
  });
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2200, 1790, 1790, 1790, 1790],
    rows: [header, ...rows],
  });
}

async function main() {
  const scores = loadScores();
  const children = [];

  children.push(
    new Paragraph({
      spacing: { after: 120 },
      children: [
        new TextRun({
          text: "noslop modes comparison",
          bold: true,
          font: "Arial",
          size: 36,
        }),
      ],
    })
  );
  children.push(
    p(
      "Human flow over score maxing. Same briefs, four intensities. VOICE scores from the real noslop CLI path. StoryScope not required; book-band scores (~0.1–0.3) can still mean good writing.",
      { after: 200, italics: true, size: 20 }
    )
  );

  children.push(h1("1. Problem"));
  children.push(
    p(
      "When we max VOICE or StoryScope feature packs, numbers climb and the page often gets stiff: checklist craft, even completion, every beat pays off. Real books can sit near ~0.13 P(human) on StoryScope and still flow. High metric + low readability is failure. This report compares modes so we stop shipping “max” as if it were “best.”"
    )
  );

  children.push(h1("2. Modes"));
  children.push(
    p("default — Control only. Glue phrases, abstract fog, sermon close. Not a skill mode.")
  );
  children.push(
    p(
      "modest — Closest to how people write. Light anchors, digression OK, no arc-toy dump. Scores may sit mid; that is fine."
    )
  );
  children.push(
    p(
      "balanced — DEFAULT SHIP. Readable first; anti-glue/sermon; anchors that help; do not chase VOICE 9+."
    )
  );
  children.push(
    p(
      "max — Research only. Full craft pressure (dense anchors, stamp-ready unevenness, optional StoryScope toys). Document the readability cost."
    )
  );

  children.push(h1("3. VOICE scores"));
  children.push(
    p(
      "Scored with python -m noslop.cli voice / score_voice. Pass threshold for research tables is informative; ship intensity is balanced, not max.",
      { size: 20, italics: true }
    )
  );
  children.push(scoreTable(scores));
  children.push(p(" ", { after: 120 }));
  children.push(
    p(
      "Note: VOICE is a heuristic. A high modest score (e.g. a short clean email) does not mean max is more human-readable — read the drafts.",
      { size: 18, italics: true, color: "555555" }
    )
  );

  children.push(h1("4. Recommendation"));
  children.push(
    p(
      "Ship balanced as the default skill intensity. Use modest for natural letters and low-pressure notes. Use max only when the user asks for research / stress craft — and label it. Never treat the highest VOICE number as the product goal."
    )
  );

  children.push(
    new Paragraph({ children: [new PageBreak()] })
  );
  children.push(h1("5. Full drafts"));

  for (const brief of BRIEFS) {
    children.push(h2(BRIEF_LABEL[brief]));
    for (const arm of ARMS) {
      const sc = scores[brief][arm];
      children.push(
        p(
          `${MODE_LABEL[arm]}  ·  VOICE ${sc.score.toFixed(2)}  ·  gate=${sc.gate}${sc.hard_fail ? "  ·  HARD FAIL" : ""}`,
          { bold: true, after: 100 }
        )
      );
      children.push(...draftParas(loadDraft(brief, arm)));
      children.push(p(" ", { after: 200 }));
    }
  }

  children.push(h1("6. Files"));
  children.push(
    p(
      "Drafts: evals/results/modes/*.md  ·  Scores: *_voice.json  ·  SUMMARY.md  ·  Skill: skills/noslop/modes.md"
    )
  );

  const doc = new Document({
    styles: {
      default: { document: { run: { font: "Arial", size: 22 } } },
      paragraphStyles: [
        {
          id: "Heading1",
          name: "Heading 1",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: { size: 32, bold: true, font: "Arial" },
          paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0 },
        },
        {
          id: "Heading2",
          name: "Heading 2",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: { size: 26, bold: true, font: "Arial" },
          paragraph: { spacing: { before: 200, after: 140 }, outlineLevel: 1 },
        },
      ],
    },
    sections: [
      {
        properties: {
          page: {
            size: { width: 12240, height: 15840 },
            margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
          },
        },
        headers: {
          default: new Header({
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: "noslop · modes comparison · human flow over score maxing",
                    font: "Arial",
                    size: 16,
                    color: "666666",
                  }),
                ],
              }),
            ],
          }),
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                children: [
                  new TextRun({ text: "Page ", font: "Arial", size: 16 }),
                  new TextRun({
                    children: [PageNumber.CURRENT],
                    font: "Arial",
                    size: 16,
                  }),
                ],
              }),
            ],
          }),
        },
        children,
      },
    ],
  });

  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(OUT, buf);
  console.log("wrote", OUT);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
