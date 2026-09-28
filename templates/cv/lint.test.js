// node --test templates/cv/   (Node 18+, no dependencies)
const test = require('node:test');
const assert = require('node:assert');
const { lintTenure, parseRange } = require('./lint');

const NOW = new Date(2026, 8, 28);
const role = (meta, tech, bullets = []) => ({ title: 'Eng', company: 'Co', meta, tech, bullets });

test('parses English and Portuguese ranges, including open-ended ones', () => {
  assert.deepStrictEqual(parseRange('Aug 2023 – Sep 2025 | Remote', NOW),
    { start: new Date(2023, 7, 1), end: new Date(2025, 8, 1) });
  assert.deepStrictEqual(parseRange('Set 2025 – Atual | Remoto', NOW),
    { start: new Date(2025, 8, 1), end: NOW });
  assert.strictEqual(parseRange('Remote only', NOW), null);
});

test('flags a tenure claim longer than the dated roles support', () => {
  // The real case this lint exists for: "four of them … on Databricks" with Databricks from Aug 2023.
  const S = {
    summary: 'Six years working with data, four of them in data engineering on **Azure Databricks**.',
    experience: [
      role('Aug 2023 – Present | Remote', 'Databricks, PySpark.'),
      role('Apr 2020 – Aug 2022 | Porto Alegre', 'Python, R.'),
    ],
  };
  const w = lintTenure(S, NOW);
  assert.strictEqual(w.length, 1);
  assert.match(w[0], /claims 4 years of Databricks/);
  assert.match(w[0], /Aug 2023/);
});

test('Portuguese number words and "deles" are understood', () => {
  const S = {
    summary: 'Seis anos com dados, quatro deles sobre Databricks.',
    experience: [role('Ago 2023 – Atual', 'Databricks.'), role('Abr 2020 – Ago 2022', 'Python.')],
  };
  assert.strictEqual(lintTenure(S, NOW).length, 1);
});

test('an honest claim passes, including total experience with no technology named', () => {
  const S = {
    summary: 'Six years working with data, three of them on Databricks. 10+ three-hour workshops.',
    experience: [role('Aug 2023 – Present', 'Databricks.'), role('Apr 2020 – Aug 2022', 'Python.')],
  };
  assert.deepStrictEqual(lintTenure(S, NOW), []);
});

test('total-experience claims are checked against the earliest role', () => {
  const S = {
    summary: 'Ten years of experience.',
    experience: [role('Apr 2020 – Present', 'Python.')],
  };
  assert.match(lintTenure(S, NOW)[0], /of total experience/);
});

test('a CV with no dated roles produces no warnings rather than crashing', () => {
  assert.deepStrictEqual(lintTenure({ summary: '5 years of Python.', experience: [] }, NOW), []);
});
