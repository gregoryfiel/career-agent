# Skill 05 — Inbox sweep

**Goal:** find every employer reply, across **every address the person actually uses**.

## Why this skill exists

During a real search, four applications were confirmed by email. Two landed in a primary Gmail
account. Two landed in a completely different Outlook address — because the LinkedIn account was
registered to it, and LinkedIn-submitted applications notify the LinkedIn address.

Checking one inbox found half the picture and produced a wrong conclusion: *"nobody replied."*

## The routing rule

**Confirmations follow the account that submitted them, not your preferred address.**

| Submitted via | Lands in |
|---|---|
| LinkedIn Easy Apply | the address on the **LinkedIn account** |
| Job-board apply | the address on the **job-board account** |
| ATS direct (Greenhouse, Lever, Gupy, inHire…) | the address **typed into that form** |
| Recruiter outreach | wherever they found you — often a third address, or WhatsApp |

Record every address and its route in `profile/<person>/profile.md` during onboarding. Sweep all of
them, every time.

## Procedure

1. **Sweep each inbox for the window since the last sweep.** Record the date so the next run knows
   where to start.
2. **Search broad, then narrow.** A date-bounded sweep first, then targeted searches per company
   name from the tracker, then keyword searches (`interview`, `entrevista`, `próxima etapa`,
   `candidatura`, `processo seletivo`, `assessment`, `offer`).
3. **Read the thread, not the preview.** Previews show the oldest messages; the reply you are
   looking for is the newest one.
4. **Do not act.** Never reply, archive, label or delete. Report and let the person decide.

## What to look for, in priority order

1. 🔴 **Deadlines and expiring links** — assessments, scheduling links, incomplete applications.
   These are time-bombs.
2. 🟠 **Interview invitations** and scheduling requests.
3. 🟡 **Rejections** — update the tracker, and note the stage it died at. The pattern across several
   rejections is more useful than any single one.
4. 🟢 **Confirmations** — match to the tracker, mark `sent` if it was uncertain.
5. ⚪ **Recruiter outreach** for roles not yet in the tracker.

Ignore job alerts and newsletters entirely.

## Output

```markdown
## Sweep — <date> (window: <last sweep> → now)

🔴 Needs action today
- <Company>: assessment link expires <date> — <inbox>

🟠 Replies
- <Company>: interview invitation, <date> — <inbox>

✅ Confirmations matched to tracker
- <Company> (<ATS>) — <inbox>

Nothing new from: <list>

⚠️ Not swept: <inbox> — <why>
```

Always state which inboxes you could **not** reach. Silence in an unswept inbox is not good news.
