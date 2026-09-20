# Skill 00 — Onboarding

**Goal:** produce `profile/<person>/` — the four files everything else depends on.

Run this once per person. Re-run sections when something material changes (new role, new
certification, new evidence surfaced by an interview).

## Output

```
profile/<person>/
  profile.md     identity, targets, constraints, seniority band, language
  evidence.md    ⭐ the evidence bank — single source of truth
  stories.md     CAR stories, reusable across interviews
  voice.md       how this person writes and speaks
```

## Intake paths

Offer all three; most people use a mix.

1. **Documents** — they drop a CV (PDF/DOCX), a LinkedIn export, certificates into a folder. Read
   them. Best fidelity.
2. **Profile URL** — a public LinkedIn profile. Fast, but usually sparse: expect missing
   experience, no dates, no achievements. Treat everything you extract as a **starting point to
   confirm**, never as fact.
3. **Guided conversation** — ask. Slowest, highest quality, and the only path that surfaces the
   things people forget to write down.

## The evidence bank — how to build it

This is the heart of the repository. Get it right and nothing downstream can go wrong.

For every technology, tool, method or domain the person claims, record **where it happened**:

```markdown
| Item | Level | Where it happened | Proof |
|---|---|---|---|
| PySpark | advanced · 4 yrs | ilegra (TK Elevator), NTT DATA (AB InBev) | terabyte-scale ETL, ~1 TB fact table |
| Unity Catalog | advanced | NTT DATA — provisioned as code across SIT/UAT/PROD | 1,677-table cross-tenant migration |
| Kafka | ❌ none | — | do not claim |
```

Rules:

- **Three columns minimum: item, where, proof.** An item without a "where" is not evidence, it is a
  wish. Put it in the `❌ none` block.
- **Record the absences too.** An explicit "does not have Kafka" is more useful than silence,
  because it stops a future agent from inferring it.
- **Numbers get a source.** "1,677 tables" is evidence. "Thousands of tables" is not. If the person
  is unsure of a figure, write `⚠️ to confirm` next to it and make them settle it before it reaches
  a CV — a number that varies between the CV and the interview destroys credibility.
- **Ask about the unglamorous.** The strongest interview stories are usually the ones people do not
  put on a CV: the silent bug they found, the vendor handover they rescued, the process they
  created because it did not exist.

## Questions that surface hidden evidence

Ask these in the guided path. They consistently produce material a CV misses.

- What is the thing you fixed that nobody noticed was broken?
- What did you inherit in bad shape, and what state did you leave it in?
- What did you argue for that turned out to be right? What about wrong?
- What do people on your team come to you for specifically?
- What is the largest thing — data, money, users, time — that you have been responsible for?
- What did you build that is still running after you stopped touching it?
- Where did you say "no", and what happened?

## Seniority band — ask, never infer

Get this explicitly and write it in `profile.md`:

> **Target band:** ____ · **Do not target:** ____ · **Why:** ____

Titles do not map across companies. Someone leading a platform team at one company is a senior
individual contributor at another, and consultancies routinely ask ten years for an "architect"
title. Getting this wrong wastes entire application cycles. If the person has had a conversation
with a recruiter that calibrated their band, record it and treat it as authoritative — recruiter
feedback beats job-posting text.

## Constraints — ask, never infer

Record in `profile.md`: location and remote appetite · employment types accepted · salary floor ·
notice period · languages with honest levels · deal-breakers · ATS platforms they refuse to use ·
companies to avoid and why.

## voice.md

Capture how they actually sound, with samples they wrote. This prevents every generated document
from reading like an AI wrote it. Note: preferred formality, sentence length, words they never use,
whether they write in first person, and any tics to avoid.

## Finish

Read the evidence bank back to them out loud, section by section, and ask: *"Is any of this
stronger or weaker than I wrote it?"* People correct an overstatement faster than they volunteer an
achievement.

Then run `python3 tools/verify_evidence.py --profile profile/<person>` to confirm the file parses.
