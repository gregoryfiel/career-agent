/**
 * CV data file. One per target role — copy this, rename, override what the posting needs.
 *
 *   cp cv.example.js cv_acme_senior.js
 *   CV_DATA=./cv_acme_senior.js node build.js
 *
 * ⚠️ Every technology named here must exist in profile/<person>/evidence.md.
 *    tools/verify_evidence.py enforces it.
 */
module.exports = {
  name: 'Ana Beatriz Moraes',
  subtitle: 'Analista de Marketing Digital | Conteúdo · Social · Performance',
  email: 'ana@example.com',
  phone: '+55 (51) 90000-0000',
  location: 'Porto Alegre, RS',
  links: [{ label: 'linkedin.com/in/exemplo', url: 'https://linkedin.com/in/exemplo' }],

  labels: {
    summary: 'Resumo Profissional',
    skills: 'Competências',
    experience: 'Experiência Profissional',
    education: 'Formação',
    certifications: 'Certificações e Idiomas',
    tech: 'Ferramentas: ',
  },

  // Lead with whatever the posting leads with.
  summary:
    'Três anos em marketing digital, com foco em estratégia de conteúdo e social media para ' +
    'contas B2C. Responsável pelo calendário editorial de seis contas simultâneas, com ' +
    'acompanhamento de performance em GA4 e gestão de campanhas em Meta Ads.',

  skills: [
    { label: 'Conteúdo', value: 'Estratégia de conteúdo, calendário editorial, copywriting, newsletter' },
    { label: 'Social', value: 'Instagram, LinkedIn — publicação diária, gestão de comunidade' },
    { label: 'Performance', value: 'GA4, Meta Ads, relatórios mensais de performance' },
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

  education: ['**Bacharelado em Publicidade e Propaganda** — Universidade Exemplo | 2019 – 2023'],
  certifications: ['**Português** — nativo. **Inglês** — intermediário.'],
};
