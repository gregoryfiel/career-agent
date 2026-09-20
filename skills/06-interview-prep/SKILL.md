# Skill 06 — Interview prep ⭐

**Goal:** the person walks in holding the exact posting they applied to, the exact CV they sent,
and an honest map of where the two meet and where they do not.

## Why this skill exists

By interview time the posting has usually been taken down and the conversation where it was
discussed has scrolled away. Candidates walk in without remembering what they promised on paper —
and get caught out by a requirement they never noticed.

Skill `04` archived it. This skill reads it back.

## Inputs — read all of these before writing anything

```
applications/<folder>/posting.md            what they asked for
applications/<folder>/requirement-map.md    the honest fit table from skill 03
applications/<folder>/CV_sent.pdf           what you actually claimed
profile/<person>/evidence.md                what you can back
profile/<person>/stories.md                 CAR stories
tracker row                                 salary quoted, recruiter name, history
```

Then research the company **fresh** — and cite sources. Never state a company fact you did not
read somewhere nameable.

## Calibrate to the stage

The single most common mistake is preparing for the wrong conversation.

| Stage | What is actually measured | Prepare |
|---|---|---|
| **Recruiter screen** (20–30 min) | Communication, language level, availability, salary, does the CV match the person | Pitch, logistics answers, salary number **decided in advance** |
| **Technical** | Depth, judgement, how you think under uncertainty | Two-layer answers (below), the requirement map, the gaps |
| **Panel / hiring manager** | Ownership, collaboration, conflict, trajectory | CAR stories, questions that show you understand their problem |
| **Final / executive** | Motivation, fit, closing | Why them specifically, what you want next |

A recruiter screen is not a technical interview. Dumping architecture detail on a recruiter reads
as poor communication, not as expertise.

## Two-layer technical answers

Build every technical answer in two layers, and **always open with layer one**:

- **Layer 1 — for a non-specialist.** One or two sentences, plain language, an analogy if it helps.
  This is what a recruiter writes down and repeats to the hiring manager. If they cannot repeat it,
  it did not land.
- **Layer 2 — if they push.** The real depth: mechanism, trade-offs, what you would check first.

Then ask: *"Do you want me to go deeper on that?"* and only descend if they say yes. Explaining
simply reads as mastery; leading with jargon reads as hiding.

## Gaps — the bridge answer

For every ⚠️ and ❌ in the requirement map, write the bridge **before** the interview:

> *"I haven't used <X> specifically. The closest thing I've done is <Y> — <one concrete example>.
> The pattern is familiar and it's a short ramp-up."*

Three rules: name the gap first, do not oversell the adjacency, never invent. The recruiter may not
catch a bluff; the technical interviewer will, and that is the interview you actually wanted.

## Questions they will ask

Generate from the posting itself, not from a generic list:

- Every eliminatory requirement → *"Tell me about your experience with…"*
- Every ⚠️ partial → the probing follow-up
- The project context described in the posting → a situational question about it
- The seniority band → scope, ownership and mentoring questions
- Behavioural standards: strength, weakness, failure, conflict, why leaving, five years, why us

For each: the answer, which story it maps to, and the number that lands it.

## Questions the person asks

Four, chosen to be useful rather than performative. Reserve the last minutes.

Good ones surface risk: who is on the team and what is the split of seniority · what does success
at ninety days look like · what is the state of the thing I would inherit · why is the role open ·
what happens between projects (for consultancies and staffing firms) · what are the next steps and
the timeline.

## Output

```
applications/<folder>/interview-prep-<stage>-<date>.md
```

Containing: what this stage measures · the company, researched and cited · **the requirement map
re-served** · the pitch · technical answers in two layers · bridge answers for every gap ·
behavioural answers mapped to stories · questions to ask · logistics (salary decided, notice
period, availability) · a one-page pocket card.

## After the interview — close the loop

Ask what they were actually asked, and what they wish they had said. Then:

1. Add new evidence to `evidence.md` — interviews always surface forgotten work.
2. Add any question that caught them out to this prep file for next time.
3. Update the tracker.

This is the feedback arrow in the loop. Skipping it means making the same mistake twice.
