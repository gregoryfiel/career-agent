# The Brazilian market — what this repo knows

Notes that generalise badly across borders, kept separate so other markets can add their own file.

## Applicant-tracking systems

| Platform | Share | What matters |
|---|---|---|
| **Gupy** | dominant, especially mid-to-large employers | **Profile-based.** The platform submits your stored Gupy profile, not the file you attach. Free-text fields resist automation — five methods were tried on one occasion and all failed silently. Plan to fill those by hand. |
| Greenhouse / Lever | tech, startups, multinationals | Document-based, clean, upload works |
| inHire, recrut.ai | Brazilian tech | Document-based |
| Abler, Sólides | SMB | Varies |
| LinkedIn Easy Apply | everywhere | Submits your LinkedIn profile — keep it current |

**The profile-based trap.** A beautifully tailored CV attached to a stale profile is worse than
useless: the recruiter reads the profile. A real example from the search this repo came from — the
Gupy profile still listed an employer the candidate had left, and said nothing about the current
role, while every CV being sent said the opposite. Skill `02` flags this before you apply.

## Two inboxes, not one

LinkedIn notifies the address on the **LinkedIn account**. Every other ATS notifies the address
**typed into its form**. If those differ — and they usually do — checking one inbox finds half the
picture.

In the search this repo came from, two of four confirmations were sitting unread in a second
address. Skill `05` sweeps all of them.

## CLT vs PJ

Two different employment models, not two names for the same thing.

**CLT** is the registered-employee regime: 13th salary, vacation plus a third, FGTS deposits,
employer social security, and whatever benefits the company adds.

**PJ** means you invoice through your own company. Higher gross, none of the above, and you carry
the tax and accounting yourself.

Moving CLT → PJ at the same number is a pay cut. Roughly:

| Lost | Approx. |
|---|---|
| 13th salary | +8.3% |
| Vacation + ⅓ | +11.1% |
| FGTS | +8% |
| Employer contributions, health plan, meal allowance, life insurance | varies — often the biggest piece |

Market rule of thumb: **PJ needs about 30–50% above CLT gross** to hold the package even. Then
subtract the Simples Nacional band (revenue level decides it, and crossing a bracket changes the
effective rate materially), the accountant, and the payroll draw needed to stay in the favourable
annex.

**Service exports** are treated differently — typically exempt from municipal service tax and from
PIS/COFINS, so the effective rate lands below the headline table. Confirm the specifics with an
accountant; do not assume them. See skill `08`.

## Salary in foreign currency

Nearshore and staffing firms quote USD. Three things to put in front of the person, every time:
today's official central-bank rate with its date, the downside scenario if the local currency
appreciates, and the conversion spread — which varies by an order of magnitude between providers.

And ask whether the contract has an annual review clause. A fixed foreign-currency number with no
review is a slow pay cut.

## Asynchronous audio interviews

Increasingly common, and unfamiliar to most candidates. A bot sends a question over WhatsApp, a
timer runs, you record one audio answer, a human reviews it later. **DigAI** is the platform behind
several large employers' screens.

What surprises people: the clock includes reading time, the platform may reject an answer sent
after the deadline, and structure counts for more than depth because a reviewer is comparing dozens
of recordings. Skill `07` prepares for this specifically.

## Seniority titles do not translate

Consultancies routinely ask ten years for an "architect" title, while the same scope at a product
company is a senior individual contributor. Getting the band wrong burns whole application cycles
on roles that were never going to convert.

Recruiter feedback beats posting text. When a recruiter calibrates the band in conversation, record
it in `profile/<person>/profile.md` and treat it as authoritative.
