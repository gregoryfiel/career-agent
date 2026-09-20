# Skill 02 — ATS triage ⭐

**Goal:** know which applicant-tracking system a job runs on **before** anyone writes a CV for it.

## Why this skill exists

A complete two-page CV was built, reviewed and exported for a role. Only at submission time did we
discover the application ran on a platform whose free-text fields reject every automation method —
five were tried, all failed. The work was thrown away, and the half-finished application sat in the
system for days as a liability.

This check costs one minute. Skipping it costs an afternoon.

## Procedure

1. **Resolve the apply link to its final destination.** Job boards use redirect shorteners; follow
   through to the real host. The domain is the answer.
2. **Match the host against the ATS table** in `profile/<person>/profile.md` and the reference
   below.
3. **Check the person's do-not-use list.** If the platform is on it, **stop** and report before any
   CV work.
4. **Record the result** in the tracker row for that job.

## Reading the destination

| Host pattern | Platform | Notes |
|---|---|---|
| `*.gupy.io` | Gupy | Dominant in Brazil. Profile-based: it submits your stored profile, so the *profile* must be current, not just the CV. Free-text fields are hostile to automation — plan to fill them by hand. |
| `boards.greenhouse.io`, `job-boards.greenhouse.io` | Greenhouse | Clean, file upload, predictable |
| `jobs.lever.co` | Lever | Clean, file upload |
| `*.inhire.app` | inHire | Common in Brazilian tech |
| `*.recrut.ai` | recrut.ai | Common in Brazilian tech |
| `*.workday*.com` | Workday | Long forms, account required |
| `*.abler.com.br`, `*.solides.com.br` | Abler / Sólides | Brazilian SMB |
| `linkedin.com/jobs/…` + Easy Apply | LinkedIn | Submits your LinkedIn profile — **confirmations route to whichever address the LinkedIn account uses**, see skill 05 |
| company's own domain | In-house | Read the form before promising anything |

When the host is unfamiliar: say so, describe what you can see of the form, and let the person
decide. Never guess.

## Profile-based vs document-based — the distinction that matters

**Document-based** (Greenhouse, Lever, inHire): you upload a file. The tailored CV *is* the
application. Skill 03 output goes straight in.

**Profile-based** (Gupy, LinkedIn Easy Apply, Workday): the platform submits a **stored profile**.
A beautifully tailored CV attached to a stale profile is worse than useless — the recruiter reads
the profile. Before applying through one of these, check that the stored profile reflects the
current role. A profile still listing an employer the person left two years ago will contradict
everything the CV says.

Warn about this explicitly. It is the most common silent failure in the whole process.

## Output

```markdown
**ATS:** Greenhouse (`boards.greenhouse.io/acme`)
**Type:** document-based — tailored CV uploads directly
**Do-not-use list:** clear
**Profile sync needed:** no
**→ Safe to build the CV.**
```

or

```markdown
**ATS:** Gupy (`acme.gupy.io`)
**Type:** profile-based — submits your stored Gupy profile
**Do-not-use list:** ⚠️ ON IT — you decided to hold Gupy applications
**Profile sync needed:** yes, and your Gupy profile still lists your previous employer
**→ Do not build a CV yet. Decide first: fix the profile, or skip this role?**
```
