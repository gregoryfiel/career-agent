/**
 * lint.js — consistency checks that run on every CV build, before a single byte is written.
 *
 * Tenure claims
 * ─────────────
 * A summary that says "four years on Databricks" while the dated roles show Databricks starting
 * in August 2023 is the exact inconsistency a recruiter spots in ten seconds — and it is rounding a
 * number up, which AGENTS.md §2.1 forbids. This check reads every "N years / N anos / N of them /
 * N deles" claim in the text, finds the technology it refers to, and compares it with the earliest
 * dated role that mentions that technology.
 *
 * It is a heuristic, so it warns rather than fails. `STRICT=1 node build.js` turns warnings into a
 * non-zero exit for CI or for people who want the hard stop.
 */

const MONTHS = {
  jan: 0, feb: 1, fev: 1, mar: 2, apr: 3, abr: 3, may: 4, mai: 4, jun: 5, jul: 6,
  aug: 7, ago: 7, sep: 8, sept: 8, set: 8, oct: 9, out: 9, nov: 10, dec: 11, dez: 11,
};
const NOW = /^(present|current|now|today|atual|atualmente|presente|hoje)$/i;
const WORDS = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10,
  um: 1, uma: 1, dois: 2, duas: 2, 'três': 3, tres: 3, quatro: 4, cinco: 5, seis: 6, sete: 7,
  oito: 8, nove: 9, dez: 10,
};
const NUM = `(\\d{1,2}|${Object.keys(WORDS).join('|')})`;
const B = '(?<![\\p{L}\\d])';               // unicode-safe word boundary (\b is ASCII-only in JS)
const E = '(?![\\p{L}\\d])';
const CLAIMS = [
  new RegExp(`${B}${NUM}\\+?\\s+(?:years?|yrs?|anos)${E}`, 'giu'),          // "4 years", "quatro anos"
  new RegExp(`${B}${NUM}\\s+(?:of them|deles|delas|dos quais|das quais)${E}`, 'giu'), // "four of them"
];
const SLACK_YEARS = 0.25;                     // "almost 4" may say 4; "3.1" may not

const plain = (s) => String(s ?? '').replace(/\*\*/g, '');
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const mentions = (text, term) =>
  new RegExp(`${B}${esc(term)}${E}`, 'iu').test(text);

function parseDate(tok, now) {
  const t = tok.trim().replace(/\.$/, '');
  if (NOW.test(t)) return now;
  let m = t.match(/^([\p{L}]{3,})\.?\s+(\d{4})$/u);
  if (m) {
    const mon = MONTHS[m[1].toLowerCase().slice(0, 4)] ?? MONTHS[m[1].toLowerCase().slice(0, 3)];
    return mon === undefined ? null : new Date(Number(m[2]), mon, 1);
  }
  m = t.match(/^(\d{1,2})\/(\d{4})$/);
  if (m) return new Date(Number(m[2]), Number(m[1]) - 1, 1);
  m = t.match(/^(\d{4})$/);
  if (m) return new Date(Number(m[1]), 0, 1);   // year only: most generous reading
  return null;
}

/** "Aug 2023 – Sep 2025 | Porto Alegre" → { start, end } */
function parseRange(meta, now) {
  const head = plain(meta).split('|')[0];
  const parts = head.split(/\s+[–—-]\s+/);
  if (parts.length < 2) return null;
  const start = parseDate(parts[0], now);
  const end = parseDate(parts[1], now);
  return start && end ? { start, end } : null;
}

const years = (from, to) => (to - from) / (365.25 * 24 * 3600 * 1000);
const fmt = (d) => d.toLocaleString('en', { month: 'short', year: 'numeric' });

/** Every string a reader will see, with a label saying where it came from. */
function textFields(S) {
  const out = [];
  if (S.summary) out.push(['summary', S.summary]);
  (S.skills || []).forEach((s) => out.push([`skills › ${s.label}`, s.value]));
  (S.experience || []).forEach((e) =>
    (e.bullets || []).forEach((b, i) => out.push([`${e.company} › bullet ${i + 1}`, b])));
  return out.map(([where, t]) => [where, plain(t)]);
}

function lintTenure(S, now = new Date()) {
  const roles = (S.experience || [])
    .map((e) => ({
      range: parseRange(e.meta || '', now),
      text: plain([e.title, e.company, ...(e.bullets || []), e.tech].join(' ')),
      tech: plain(e.tech || '').replace(/\.$/, '').split(',').map((x) => x.trim()).filter(Boolean),
    }))
    .filter((r) => r.range);
  if (!roles.length) return [];

  const earliestAll = roles.reduce((a, r) => (r.range.start < a ? r.range.start : a), now);
  const terms = [...new Set(roles.flatMap((r) => r.tech))].filter((t) => t.length > 1);
  const earliestFor = (term) => roles
    .filter((r) => mentions(r.text, term))
    .reduce((a, r) => (!a || r.range.start < a ? r.range.start : a), null);

  const warnings = [];
  for (const [where, text] of textFields(S)) {
    for (const re of CLAIMS) {
      re.lastIndex = 0;
      let m;
      while ((m = re.exec(text))) {
        const raw = m[1].toLowerCase();
        const claimed = /^\d+$/.test(raw) ? Number(raw) : WORDS[raw];
        // The claim is about whatever comes next, up to the end of the clause.
        const window = text.slice(m.index + m[0].length).split(/[.;,\n]/)[0].slice(0, 140);
        const term = terms
          .filter((t) => mentions(window, t))
          .sort((a, b) => b.length - a.length)[0];
        const since = term ? earliestFor(term) : earliestAll;
        if (!since) continue;
        const actual = years(since, now);
        if (claimed > actual + SLACK_YEARS) {
          const about = term ? `of ${term}` : 'of total experience';
          warnings.push(
            `${where}: "${m[0]}${window}" claims ${claimed} years ${about}, ` +
            `but the earliest dated role with it starts ${fmt(since)} ` +
            `(${actual.toFixed(1)} years). Fix the claim or the dates.`);
        }
      }
    }
  }
  return warnings;
}

module.exports = { lintTenure, parseRange, parseDate };
