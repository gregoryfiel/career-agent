/**
 * build.js — renders a CV data file to .docx (and .md).
 *
 *   CV_DATA=./cv_acme.js node build.js           # styled
 *   CV_DATA=./cv_acme.js ATS_SAFE=1 node build.js # ATS-safe: no tables, no columns, no icons
 *
 * ATS-safe mode exists because some parsers mangle multi-column layouts and drop text inside
 * table cells. When in doubt about the employer's parser, send the ATS-safe file.
 */
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle } = require('docx');

const DATA = process.env.CV_DATA || './cv.example.js';
const ATS = !!process.env.ATS_SAFE;
const S = require(path.resolve(DATA));
const L = S.labels || {};

/** Split **bold** markers into docx runs. */
const runs = (text, base = {}) =>
  String(text).split(/(\*\*[^*]+\*\*)/g).filter(Boolean).map((part) =>
    part.startsWith('**') && part.endsWith('**')
      ? new TextRun({ ...base, text: part.slice(2, -2), bold: true })
      : new TextRun({ ...base, text: part })
  );

const heading = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 260, after: 110 },
    border: ATS ? undefined : { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'CCCCCC' } },
    children: [new TextRun({ text: text.toUpperCase(), bold: true, size: 22, color: ATS ? '000000' : '1F3A5F' })],
  });

const body = [];

// Header — contact details as literal text so an ATS can read them.
body.push(new Paragraph({
  alignment: ATS ? AlignmentType.LEFT : AlignmentType.CENTER,
  spacing: { after: 60 },
  children: [new TextRun({ text: S.name, bold: true, size: 34 })],
}));
if (S.subtitle) body.push(new Paragraph({
  alignment: ATS ? AlignmentType.LEFT : AlignmentType.CENTER,
  spacing: { after: 90 },
  children: [new TextRun({ text: S.subtitle, size: 21, color: ATS ? '000000' : '444444' })],
}));
body.push(new Paragraph({
  alignment: ATS ? AlignmentType.LEFT : AlignmentType.CENTER,
  spacing: { after: 180 },
  children: [new TextRun({
    text: [S.email, S.phone, S.location, ...(S.links || []).map((l) => l.label)].filter(Boolean).join(' | '),
    size: 19,
  })],
}));

if (S.summary) {
  body.push(heading(L.summary || 'Summary'));
  body.push(new Paragraph({ spacing: { after: 120 }, children: runs(S.summary, { size: 20 }) }));
}

if (S.skills?.length) {
  body.push(heading(L.skills || 'Skills'));
  for (const s of S.skills) {
    body.push(new Paragraph({
      spacing: { after: 70 },
      children: [new TextRun({ text: `${s.label}: `, bold: true, size: 20 }), ...runs(s.value, { size: 20 })],
    }));
  }
}

if (S.experience?.length) {
  body.push(heading(L.experience || 'Experience'));
  for (const e of S.experience) {
    body.push(new Paragraph({
      spacing: { before: 130, after: 20 },
      children: [new TextRun({ text: `${e.title} | ${e.company}`, bold: true, size: 21 })],
    }));
    if (e.meta) body.push(new Paragraph({
      spacing: { after: 70 },
      children: [new TextRun({ text: e.meta, italics: true, size: 19, color: ATS ? '000000' : '555555' })],
    }));
    for (const b of e.bullets || []) {
      body.push(new Paragraph({ bullet: { level: 0 }, spacing: { after: 50 }, children: runs(b, { size: 20 }) }));
    }
    if (e.tech) body.push(new Paragraph({
      spacing: { after: 70 },
      children: [new TextRun({ text: (L.tech || 'Tech: ') + e.tech, italics: true, size: 18 })],
    }));
  }
}

for (const [key, label] of [['education', L.education || 'Education'], ['certifications', L.certifications || 'Certifications']]) {
  if (!S[key]?.length) continue;
  body.push(heading(label));
  for (const item of S[key]) {
    body.push(new Paragraph({ spacing: { after: 60 }, children: runs(item, { size: 20 }) }));
  }
}

const doc = new Document({
  creator: S.name,
  styles: { default: { document: { run: { font: ATS ? 'Arial' : 'Calibri', size: 20 } } } },
  sections: [{ properties: { page: { margin: { top: 720, right: 720, bottom: 720, left: 720 } } }, children: body }],
});

const slug = (S.name || 'cv').replace(/\s+/g, '_');
const out = `CV_${slug}${ATS ? '_ATS_SAFE' : ''}.docx`;

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(out, buf);
  console.log(`✓ ${out}`);
  console.log('  next: bash ../../tools/check_pages.sh ' + out + ' 2');
  console.log('        python3 ../../tools/verify_evidence.py --cv <md> --profile ../../profile/<person>');
});
