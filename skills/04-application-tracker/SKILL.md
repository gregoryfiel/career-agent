# Skill 04 — Application tracker

**Goal:** one durable record per application — and an **archived copy of the posting**, because it
will disappear from the internet right before the interview.

## Why the archive matters

Postings get taken down the moment the role is filled. Chat histories scroll away. Weeks later the
interview arrives and nobody can remember what was promised on paper. Skill `06` is built entirely
on this archive; without it, interview prep is guesswork.

Archive the **full text**, not the link.

## Structure

```
applications/
  2026-09-18_Acme_Senior-Data-Engineer/
    posting.md            ⭐ full text, captured at apply time
    requirement-map.md    from skill 03
    CV_sent.pdf
    notes.md              salary quoted, referral, recruiter name, every contact
  applications.csv        one row per application
```

## The CSV

```csv
date_applied,company,role,job_id,link,ats,cv_file,status,salary_quoted,source,last_contact,notes
```

**Status values:** `draft` · `sent` · `incomplete` ⚠️ · `screening` · `interview` · `test` ·
`offer` · `rejected` · `withdrawn` · `stale`

`incomplete` is the one that matters most. A half-finished application on a profile-based ATS is
not "not applied" — it is a started record sitting in the employer's system, and it usually expires
silently. Flag it every single time the tracker is read until it is resolved.

## Rules

- **Ask before marking `sent`.** The agent never submits (see `AGENTS.md` §2.3), so it cannot know.
  Ask: *"Did you finish this one?"*
- **Record the salary you quoted**, with the date and the employment type. You will need it when
  the offer conversation happens, and inconsistency between what you said in week one and week six
  is expensive.
- **Never apply twice to the same requisition.** Check here before every new application. Note that
  large consultancies post near-identical roles under different job IDs — those are different
  requisitions, and applying to both is fine. Same ID twice is not.
- **Record why a role was dropped.** Six weeks later you will not remember whether you skipped a
  company because the stack was wrong or because a recruiter told you something.

## Periodic review

When asked for status, report: in flight · waiting on you · gone quiet (>14 days, worth a nudge) ·
⚠️ incomplete · closed. Not a data dump — a decision list.
