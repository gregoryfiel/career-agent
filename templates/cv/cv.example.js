/**
 * CV data file. One per target role.
 *
 *   cp cv.example.js cv_acme_senior.js
 *   CV_DATA=./cv_acme_senior.js node build.js
 *   CV_DATA=./cv_acme_senior.js ATS_SAFE=1 node build.js
 *
 * ⚠️ Every technology named here must exist in profile/<person>/evidence.md.
 *    tools/verify_evidence.py enforces it. See skills/03-tailored-cv/SKILL.md.
 *
 * Use **double asterisks** for bold anywhere — summary, skills, bullets, education.
 * The parser runs on every field.
 */
module.exports = {
  // outputName: 'Ana_Moraes_Acme',   // optional — defaults to `name`
  name: 'Ana Beatriz Moraes',
  subtitle: 'Analista de Marketing Digital — Conteúdo · Social · Performance',
  email: 'ana@example.com',
  phone: '+55 (51) 90000-0000',
  location: 'Porto Alegre, RS',
  links: [{ label: 'linkedin.com/in/exemplo', url: 'https://www.linkedin.com/in/exemplo/' }],

  labels: {
    sum: 'Resumo Profissional',
    skills: 'Competências',
    exp: 'Experiência Profissional',
    edu: 'Formação',
    cert: 'Certificações e Idiomas',
    tech: 'Ferramentas: ',
  },

  // Lead with whatever the posting leads with.
  summary:
    'Três anos em marketing digital, com foco em **estratégia de conteúdo e social media** para ' +
    'contas B2C. Respondo pelo calendário editorial de **seis contas simultâneas**, com ' +
    'acompanhamento de performance em GA4 e gestão de campanhas em Meta Ads.',

  skills: [
    { label: 'Conteúdo', value: '**Estratégia de conteúdo**, calendário editorial, copywriting, newsletter' },
    { label: 'Social', value: 'Instagram e LinkedIn — publicação diária, gestão de comunidade' },
    { label: 'Performance', value: '**GA4**, **Meta Ads**, relatórios mensais de performance' },
  ],

  experience: [
    {
      title: 'Analista de Marketing Digital',
      company: 'Agência Norte',
      meta: '2023 – 2026 | Porto Alegre, RS',
      bullets: [
        'Assumi a conta considerada irrecuperável pelo time e **cresci de 4.200 para 11.000 seguidores em nove meses**, com renovação do contrato.',
        'Reconstruí o calendário editorial de **seis contas simultâneas** a partir da análise de doze meses de publicações contra os dados de engajamento.',
        'Mantive **22% de taxa média de abertura** na newsletter ao longo de dezoito meses.',
      ],
      tech: 'GA4, Meta Ads, Instagram, LinkedIn, Canva.',
    },
  ],

  education: [
    '**Bacharelado em Publicidade e Propaganda** — Universidade Exemplo | 2019 – 2023',
  ],

  certifications: [
    '**Fundamentos do Marketing de Conteúdo** — LinkedIn Learning (2025)',
  ],

  languages: '**Português** — nativo. **Inglês** — intermediário.',
};
