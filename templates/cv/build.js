/**
 * build.js — renders a CV data file to .docx (and .pdf, when LibreOffice is installed).
 *
 *   CV_DATA=./cv_acme.js node build.js            # styled (the house template)
 *   CV_DATA=./cv_acme.js ATS_SAFE=1 node build.js # ATS-safe: Arial, no colour, no borders
 *
 * Options (environment variables)
 *   OUT_DIR=<dir>   where to write. Default: <repo>/output/<outputName>/ — gitignored, so a real
 *                   CV never lands next to the template where `git add .` would pick it up.
 *   PDF=0           skip the PDF. By default a PDF is written whenever `soffice` is found.
 *   SOFFICE=<path>  LibreOffice binary, if it is not on PATH (common on Windows).
 *   STRICT=1        exit non-zero when the lint finds a problem (see lint.js).
 *
 * ── Provenance ───────────────────────────────────────────────────────────────
 * The styled layout is not invented. It was recovered from the OOXML of CVs this
 * template actually produced, so every measurement below is the real one:
 *
 *   page          Letter (12240 × 15840 twips), margins 648 vertical / 792 horizontal
 *   body font     Calibri 9.5pt (sz 19 half-points)
 *   accent        #1F3864
 *   name          bold, accent, 15pt, centred, 20 after
 *   subtitle      #444444, 10pt, centred, 20 after
 *   contact       #333333, 9pt, centred, 160 after, links #0563C1 underlined, "  |  " separator
 *   heading       bold accent 10pt UPPERCASE, bottom rule (single, accent, sz 6, space 2),
 *                 160 before / 64 after
 *   summary       9.5pt, justified, 60 after
 *   skill label   bold accent 9pt, own paragraph
 *   skill value   9pt, own paragraph
 *   role title    bold 10pt, 118 before / 8 after
 *   role meta     italic #595959 8.5pt, 55 after
 *   bullet        9.5pt, numbered list, 30 after
 *   tech line     bold italic #444444 8.5pt, 40 before / 20 after
 *   education     9.5pt, 35 after
 *
 * ── Fixed vs the original ────────────────────────────────────────────────────
 * The original applied the **bold** parser only to summary, experience bullets and
 * education — so `**Databricks Asset Bundles**` shipped with literal asterisks inside
 * the skills section of at least one real CV. Here every text field goes through the
 * same parser.
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const {
  Document, Packer, Paragraph, TextRun, ExternalHyperlink,
  AlignmentType, BorderStyle, LevelFormat, convertInchesToTwip,
} = require('docx');
const { lintTenure } = require('./lint');

const DATA = process.env.CV_DATA || './cv.example.js';
const ATS = !!process.env.ATS_SAFE;
const S = require(path.resolve(DATA));
const L = S.labels || {};
const REPO = path.resolve(__dirname, '..', '..');

// ── Lint before building — an inconsistent CV should never reach a recruiter ──
{
  const warnings = lintTenure(S);
  if (warnings.length) {
    console.warn('\n⚠️  CV lint — tenure claims that the dated roles do not support:');
    warnings.forEach((w) => console.warn(`   • ${w}`));
    console.warn('   AGENTS.md §2.1: no rounding a number up.\n');
    if (process.env.STRICT) process.exit(1);
  }
}

// ── Design tokens (recovered) ────────────────────────────────────────────────
const FONT = ATS ? 'Arial' : 'Calibri';
const ACCENT = ATS ? '000000' : '1F3864';
const MUTED = ATS ? '000000' : '444444';
const META = ATS ? '000000' : '595959';
const CONTACT = ATS ? '000000' : '333333';
const LINK = ATS ? '000000' : '0563C1';

const SZ = { name: 30, subtitle: 20, contact: 18, heading: 20, body: 19, skill: 18, role: 20, meta: 17, tech: 17 };

/** Split **bold** markers into runs. Applied to every text field — see header note. */
const runs = (text, base = {}) =>
  String(text ?? '')
    .split(/(\*\*[^*]+\*\*)/g)
    .filter(Boolean)
    .map((part) =>
      part.startsWith('**') && part.endsWith('**')
        ? new TextRun({ font: FONT, ...base, text: part.slice(2, -2), bold: true })
        : new TextRun({ font: FONT, ...base, text: part })
    );

const heading = (text) =>
  new Paragraph({
    spacing: { before: 160, after: 64 },
    border: ATS ? undefined : { bottom: { style: BorderStyle.SINGLE, color: ACCENT, size: 6, space: 2 } },
    children: [new TextRun({
      font: FONT, text: String(text).toUpperCase(), bold: true, color: ACCENT, size: SZ.heading,
    })],
  });

const body = [];

// ── Header ───────────────────────────────────────────────────────────────────
body.push(new Paragraph({
  spacing: { after: 20 },
  alignment: ATS ? AlignmentType.LEFT : AlignmentType.CENTER,
  children: [new TextRun({ font: FONT, text: S.name, bold: true, color: ACCENT, size: SZ.name })],
}));

if (S.subtitle) {
  body.push(new Paragraph({
    spacing: { after: 20 },
    alignment: ATS ? AlignmentType.LEFT : AlignmentType.CENTER,
    children: [new TextRun({ font: FONT, text: S.subtitle, color: MUTED, size: SZ.subtitle })],
  }));
}

// Contact line — plain text so an ATS can read it, links only in the styled variant.
{
  const sep = '  |  ';
  const plain = (t) => new TextRun({ font: FONT, text: t, color: CONTACT, size: SZ.contact });
  const kids = [];
  const push = (node) => { if (kids.length) kids.push(plain(sep)); kids.push(node); };

  if (S.email) push(plain(S.email));
  for (const l of S.links || []) {
    push(ATS
      ? plain(l.label)
      : new ExternalHyperlink({
          link: l.url,
          children: [new TextRun({
            font: FONT, text: l.label, color: LINK, size: SZ.contact, underline: {},
          })],
        }));
  }
  if (S.phone) push(plain(S.phone));
  if (S.location) push(plain(S.location));

  body.push(new Paragraph({
    spacing: { after: 160 },
    alignment: ATS ? AlignmentType.LEFT : AlignmentType.CENTER,
    children: kids,
  }));
}

// ── Summary ──────────────────────────────────────────────────────────────────
if (S.summary) {
  body.push(heading(L.sum || L.summary || 'Resumo Profissional'));
  body.push(new Paragraph({
    spacing: { after: 60 },
    alignment: ATS ? AlignmentType.LEFT : AlignmentType.JUSTIFIED,
    children: runs(S.summary, { size: SZ.body }),
  }));
}

// ── Skills — label and value are separate paragraphs ─────────────────────────
if (S.skills?.length) {
  body.push(heading(L.skills || 'Competências Técnicas'));
  for (const s of S.skills) {
    body.push(new Paragraph({
      children: [new TextRun({ font: FONT, text: s.label, bold: true, color: ACCENT, size: SZ.skill })],
    }));
    body.push(new Paragraph({ children: runs(s.value, { size: SZ.skill }) }));
  }
}

// ── Experience ───────────────────────────────────────────────────────────────
if (S.experience?.length) {
  body.push(heading(L.exp || L.experience || 'Experiência Profissional'));
  for (const e of S.experience) {
    body.push(new Paragraph({
      spacing: { before: 118, after: 8 },
      children: [new TextRun({
        font: FONT, text: [e.title, e.company].filter(Boolean).join(' | '), bold: true, size: SZ.role,
      })],
    }));
    if (e.meta) {
      body.push(new Paragraph({
        spacing: { after: 55 },
        children: [new TextRun({ font: FONT, text: e.meta, italics: true, color: META, size: SZ.meta })],
      }));
    }
    for (const b of e.bullets || []) {
      body.push(new Paragraph({
        numbering: { reference: 'cv-bullets', level: 0 },
        spacing: { after: 30 },
        children: runs(b, { size: SZ.body }),
      }));
    }
    if (e.tech) {
      body.push(new Paragraph({
        spacing: { before: 40, after: 20 },
        children: [new TextRun({
          font: FONT, text: (L.tech || 'Tecnologias: ') + e.tech,
          bold: true, italics: true, color: MUTED, size: SZ.tech,
        })],
      }));
    }
  }
}

// ── Education (plain paragraphs) and certifications (bulleted) ───────────────
if (S.education?.length) {
  body.push(heading(L.edu || L.education || 'Formação'));
  for (const item of S.education) {
    body.push(new Paragraph({ spacing: { after: 35 }, children: runs(item, { size: SZ.body }) }));
  }
}

const tail = [...(S.certifications || [])];
if (S.languages) tail.push(S.languages);
if (tail.length) {
  body.push(heading(L.cert || L.certifications || 'Certificações e Idiomas'));
  for (const item of tail) {
    body.push(new Paragraph({
      numbering: { reference: 'cv-bullets', level: 0 },
      spacing: { after: 35 },
      children: runs(item, { size: SZ.body }),
    }));
  }
}

// ── Document ─────────────────────────────────────────────────────────────────
const doc = new Document({
  creator: S.name,
  styles: { default: { document: { run: { font: FONT, size: SZ.body } } } },
  numbering: {
    config: [{
      reference: 'cv-bullets',
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: '•',
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: convertInchesToTwip(0.25), hanging: convertInchesToTwip(0.16) } } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 648, bottom: 648, left: 792, right: 792 },
      },
    },
    children: body,
  }],
});

const slug = (S.outputName || S.name || 'cv').replace(/\s+/g, '_');
const outDir = process.env.OUT_DIR
  ? path.resolve(process.env.OUT_DIR)
  : path.join(REPO, 'output', slug);
fs.mkdirSync(outDir, { recursive: true });
const out = path.join(outDir, `CV_${slug}${ATS ? '_ATS_SAFE' : ''}.docx`);
const rel = (p) => path.relative(REPO, p) || '.';

/** First LibreOffice binary that answers, or null. */
function findSoffice() {
  const candidates = [process.env.SOFFICE, 'soffice', 'libreoffice'].filter(Boolean);
  for (const bin of candidates) {
    try { execFileSync(bin, ['--version'], { stdio: 'ignore' }); return bin; } catch { /* next */ }
  }
  return null;
}

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(out, buf);
  console.log(`✓ ${rel(out)}`);

  let pdf = null;
  if (process.env.PDF !== '0') {
    const soffice = findSoffice();
    if (soffice) {
      try {
        execFileSync(soffice, ['--headless', '--convert-to', 'pdf', '--outdir', outDir, out],
          { stdio: 'ignore' });
        pdf = out.replace(/\.docx$/, '.pdf');
        console.log(`✓ ${rel(pdf)}`);
      } catch (e) {
        console.warn(`⚠️  PDF export failed (${e.message.split('\n')[0]}) — the .docx is fine.`);
      }
    } else {
      console.log('ℹ  LibreOffice not found — PDF skipped. Set SOFFICE=<path> or export from Word.');
    }
  }

  console.log('\n  next — both must pass before this CV is sent (skills/03, phase 4):');
  console.log(`    python3 tools/verify_evidence.py --profile profile/<person> --cv ${rel(out)}`);
  console.log(`    bash tools/check_pages.sh ${rel(pdf || out)} 2`);
});
