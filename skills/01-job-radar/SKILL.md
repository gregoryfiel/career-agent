# Skill 01 — Job radar

**Goal:** a ranked shortlist of **currently open** roles that match the person's band and stack.

## Inputs
`profile/<person>/profile.md` (targets, band, constraints) and `evidence.md` (what they can back).

## Sources, in order of reliability

1. **Job-board APIs / MCP connectors** — structured, dated, and the posting date is trustworthy.
   The best first pass.
2. **Company career pages** — authoritative for "is this still open?". Slower, no dates usually.
3. **Browser search on professional networks** — good signal (`actively reviewing applicants`),
   requires the person's logged-in session.
4. **Community feeds** (WhatsApp/Telegram/Slack job channels) — high volume, **goes stale fast**.
   Anything older than two weeks needs re-verification before you spend effort on it.

## Hard filters — apply before ranking

Drop, and say why:

- Outside the declared **seniority band** (both directions — too junior wastes their time too).
- Requires a **core technology with no evidence**. One missing "nice to have" is fine; a missing
  eliminatory requirement is not.
- Violates a **deal-breaker** (location, employment type, salary floor, on-call).
- **Already applied** — check the tracker. Re-applying to the same requisition looks careless.

## Ranking

Score each survivor on five dimensions and show the reasoning, not just the number:

| Dimension | Question |
|---|---|
| Stack match | How much of the required stack is in the evidence bank? |
| Seniority fit | Is this their band, honestly? |
| Domain relevance | Have they worked on this kind of problem before? |
| Constraint fit | Location, contract type, compensation signal |
| Trajectory | Does this move them where they said they want to go? |

## Output

Present in batches of five. More than that and nobody reads past the third.

For each: company, role, modality, link, **why it fits**, **what is missing**, and the honest
staleness note (`posted 2 days ago` vs `last seen 3 weeks ago, unverified`).

Then hand off: *"Which of these do you want to pursue? I'll run ATS triage before building any CV."*

## Anti-patterns

- **Do not recommend on title and salary alone.** Read the full description. A "Senior Data
  Engineer" requiring ten years of architecture experience is not a senior data engineer role.
- **Do not present stale leads as live.** Say when you could not confirm.
- **Do not pad the list to reach five.** Three good ones beats five with filler.
