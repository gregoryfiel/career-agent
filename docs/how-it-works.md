# How it works

## The shape of it

`career-agent` is markdown instructions plus three small scripts. There is no service, no database
and no account. Your agent reads the skill file for the task at hand and follows it against your
profile folder.

That design is deliberate: you can read every rule the agent is following, change any of them in a
text editor, and see the change in a diff.

## The loop

```
  00 onboarding ─────► evidence.md ◄──────────────────────┐
                            │                             │
                            ▼                             │  new evidence after
  01 job radar ──► 02 ats triage ──► 03 tailored cv       │  every interview
                            │              │              │
                       (Gupy? warn)        ▼              │
                                     04 tracker ──────────┤
                                        │ archives        │
                                        │ the posting     │
                                        ▼                 │
                                  05 inbox sweep          │
                                        │                 │
                                        ▼                 │
                                  06 interview prep ──────┘
                                  07 audio prep
                                  08 salary research
```

## A week in practice

**Monday — onboarding, once.** Twenty minutes of questions produces `evidence.md`. This is the only
step that cannot be skipped: everything downstream reads it, and a CV written without it is a
fabrication waiting to happen.

**Tuesday — radar.** Five roles, ranked, each with why it fits and what is missing. You pick two.

**Tuesday, still — ATS triage.** One minute per role. Two document-based platforms, safe to
proceed. If one had been profile-based and stale, you would have found out now rather than after
building the CV.

**Wednesday — the CVs.** For each: a requirement map you see before any drafting, a draft, a fresh
reviewer that critiques it with company research, then four gates — evidence, page count, ATS text
layer, and numbers matching the evidence bank exactly. You apply. The agent does not.

**Wednesday evening — tracker.** Two rows, two folders, both postings archived in full. This is the
step people skip and regret.

**Friday — inbox sweep.** Every address, not the favourite one. One confirmation, one assessment
link with a deadline.

**Two weeks later — the interview.** The posting has been taken down and the conversation has
scrolled away, but skill `06` reads the archive: what they asked for, what you sent, where the gap
is, the bridge answer for it, likely questions from their own text, and four questions for you to
ask.

**After the interview — close the loop.** What were you actually asked? What do you wish you had
said? New evidence goes back into the bank. That arrow is why the second interview goes better than
the first.

## The one rule that matters

Nothing reaches a document unless `profile/<you>/evidence.md` backs it.

Not "adjacent experience". Not a rounded-up number. Not a keyword that would help the CV get
through a filter.

`tools/verify_evidence.py` enforces it and runs in CI, because a rule nobody checks is a
suggestion. Fabrication does not fail at the CV stage — it fails in the technical interview, in
front of someone who knows the difference. That is worse than never applying.
