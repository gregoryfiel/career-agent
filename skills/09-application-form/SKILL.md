# Skill 09 — Application form ⭐

**Goal:** every field of an application form answered — correctly, consistently and within its
limits — so the person reviews, pastes and clicks **submit** themselves.

The CV is the document the agent polishes for days. The form is where the application is actually
decided, and it gets five careless minutes. Salary, notice period, "why are you leaving", "how many
years of X" — these are read before the CV, filtered on automatically, and remembered in every later
conversation.

## Preconditions

- Skill `02` has identified the platform (Gupy, Factorial, Quickin, Greenhouse, Lever, LinkedIn
  Easy Apply, Workday…).
- The tailored CV exists and has passed skill `03`'s gates. The form must say what the CV says.
- `profile/<person>/profile.md` has the salary floor, contract types accepted and notice period. If
  not, **ask** — `AGENTS.md` §5.

## Phase 1 — Read the real form

Open the form in the person's browser and list **every** field, including the ones below the fold
and the screening questions at the end. Do not work from the posting, and do not work from memory of
"how these forms usually are". For each field record:

| Field | Required | Type | Limit | Who fills it |
|---|---|---|---|---|
| Pretensão salarial | ✱ | text | — | agent drafts, person decides |
| Years with Azure Databricks | ✱ | text | **min 20** / max 200 chars | agent |
| Data de nascimento | ✱ | date | — | **person only** |

**Read the limits.** A "0/200 of 20 characters" counter means a *minimum* of 20 — a bare "3" is
rejected as invalid input. A 60-character maximum means every draft is counted, not estimated.

Never press submit, never tick a consent box, never upload the file. `AGENTS.md` §2.3.

## Phase 2 — Fields only the person can fill

Name them up front, in one list, so nothing is guessed: date of birth, street address, postcode,
tax or company registration number (CNPJ, NIF, EIN), government IDs, disability status, referral
name. **Never invent a placeholder** for these. A plausible-looking wrong CNPJ is caught when the
contract is drafted, and it burns the company.

If a company registration is asked for and the person is still opening one, the honest answer is a
sentence, not a number: *"In progress with <accountant>, active before the contract starts."*

## Phase 3 — Draft every answer

### Numbers must match the CV
"How many years of X?" is subtraction against the dates on the CV the person is attaching. Compute
it from the earliest dated role that mentions X and answer that — not the number in the summary if
the summary rounds up. If they disagree, fix the CV (skill `03`, gate 5) before sending either.

### Yes/No screening questions
Answer "yes" only when the evidence bank backs it. A "no" on a single screening question rarely
eliminates; a false "yes" is found in the first technical call.

### Proficiency scales
Pick the level the evidence supports, not the highest one. "Professional" is not a downgrade from
"Native or bilingual" — it is the true answer for most non-native speakers and it clears a B2 bar.

### Free text: "Why are you open to a new opportunity?"
This is the most dangerous field on the form. The answer must:

- **open by removing the suspicion** — not dissatisfied, not escaping;
- **explain a direction, not a departure** — what they want more of, not what they want less of;
- **reuse the posting's own words** — it shows the posting was read.

It must never mention health, leave, a sabbatical, conflict with a manager or a client, layoffs at
the current employer, or money. Offer a full version and a short one; when there is a character
limit, count it with a tool.

### Salary
Follow skill `08`. On the form:

- If the contract type is **unknown**, say so to the person and give both numbers — CLT and PJ (or
  the local equivalent) differ by 30–50%. Default the field to the type the posting most likely
  implies, and say that it is an inference.
- **Never present a market range as the company's range.** If no company data exists, say so next
  to the number.
- State the floor below which the person should not go.

### Availability / notice period
The contractual notice period. Not "immediate" for someone who is employed — it invites the question
of why they are free.

### Cover letter / "summary of qualifications"
Short, specific, built from the requirement map. Two strong adjacencies beat a list. Do not open
with a gap (`AGENTS.md` §2.6).

## Phase 4 — Hand over

One document, in the order the form shows the fields, each answer in a copy-paste block:

```
applications/<date>_<Company>_<Role>/form.md
```

End with a checklist: the fields only the person fills · the file to attach (PDF unless the form
asks for DOCX; check the size limit) · consent boxes they must read and tick themselves · any
"recover profile" / autofill button that could save them time.

Then ask the tracker question from skill `04`: *"Did you send it?"* — and record the salary quoted.

## Anti-patterns

- **Filling the form in the browser for them.** Typing into fields is one click away from
  submitting on their behalf, and it hides the answers from their review. Draft; they paste.
- **Answering a question from the posting instead of the form.** Forms ask things postings do not.
- **A different number in every form.** The salary and years quoted in week one are the ones the
  offer conversation will hold them to. Record them.
