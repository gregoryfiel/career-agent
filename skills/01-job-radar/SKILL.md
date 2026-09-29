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
   A WhatsApp export is a `.zip` holding one `.txt`; messages start with `DD/MM/YYYY HH:MM - `.
   The same post is repeated several times — de-duplicate by job ID before counting. Salary lines in
   these feeds are usually a bot's estimate by job title, not a published range: label them so.

## Hard filters — apply before ranking

Drop, and say why:

- Outside the declared **seniority band** (both directions — too junior wastes their time too).
- Requires a **core technology with no evidence**. One missing "nice to have" is fine; a missing
  eliminatory requirement is not.
- Violates a **deal-breaker** (location, employment type, salary floor, on-call).
- **Already applied** — check the tracker. Re-applying to the same requisition looks careless.
- **Already skipped** — `skipped` rows in the tracker. Do not resurface a company the person already
  turned down unless something material changed, and when it did, say what.

Flag, do not drop:

- **Conflict of interest** — a posting from the person's current client, or from a client their
  employer serves (`## Conflicts` in `profile.md`). It will look like a perfect match because it is
  their own job description. Show it, name the non-solicitation clause to check, and let the person
  decide. See `AGENTS.md` §5.

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

## Delegating the search to a sub-agent

A sub-agent starts with no memory of this conversation. Before dispatching one, hand it: the band,
the stack it may claim, the deal-breakers, **the in-process list and the `skipped` list from the
tracker**, and the conflicts. Without the two lists it will rediscover and recommend roles the person
already turned down — this has happened. Then check its shortlist against the tracker yourself
before relaying it. A sub-agent's report is a draft, not a result.

## Browser notes — LinkedIn

- **Confirm whose session it is** before trusting "recommended for you": open
  `linkedin.com/in/me/` and read the profile it redirects to. Names in the search box's recent
  history, or in "X and millions of other members use Premium", are not the account owner.
- **Descriptions lazy-load.** The job body renders only after a real scroll event. `window.scrollTo`
  or setting `scrollTop` from a script does not trigger it; the browser tool's native scroll does.
  Scroll, wait about three seconds, then read everything after "About the job".
- **Duplicate postings are an opportunity.** The same requisition is often posted twice; the copy
  with fewer applicants is the same funnel with a shorter queue. Recommend that one.
- **Easy Apply vs Apply.** Easy Apply keeps the application inside LinkedIn and often adds screening
  questions (skill `09`). "Apply" / "Responses managed off LinkedIn" hands off to the company's ATS —
  run skill `02` first.
- Recommendations include roles the person is **already in process with**. Cross-check the tracker
  before counting anything as new.
