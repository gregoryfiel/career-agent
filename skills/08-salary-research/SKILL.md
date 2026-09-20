# Skill 08 — Salary research ⭐

**Goal:** walk into the compensation conversation with a number the person chose on purpose, backed
by data about **that company and that role** — not a national average.

> This is market research, not financial advice. The agent is not a financial advisor or an
> accountant. Present the data, show the arithmetic, name the assumptions, and let the person
> decide. For anything tax-related, tell them to confirm with their accountant.

## Procedure

**1. Company-specific first.** Aggregate national averages are nearly useless for negotiation.
Salary sites let you drill to company + role + country; that page is the one that matters. Record
the sample size and the confidence label — a range built on four self-reports is a hint, not a
benchmark.

**2. Find the closest peer.** A range of "X to Y" hides everything. Look at the individual reports
and find the one matching the person's actual years of experience. Someone with fifteen years sets
the top of that range and it is not the number to anchor on with four.

**3. Check the level in the title.** A "Senior" band and a non-senior band at the same company can
differ by a third. If the posting title lacks the seniority word, the budget may be in the lower
band — worth asking before quoting.

**4. Check variable pay.** If reports show zero variable compensation, base is everything and there
is no bonus to make up a low offer.

**5. Look for the margin.** For staffing and consultancy firms, what they bill the end client is
often public in market analyses. Knowing the bill rate tells you whether your ask is reasonable —
not to quote at them, but so you stop anchoring low out of politeness.

## When the employment type changes

Moving from employee to contractor is not a lateral move at the same number. Lay out what is lost
and what it costs to replace.

For Brazil specifically — the CLT → PJ conversion:

| Lost | Approx. |
|---|---|
| 13th salary | +8.3% |
| Vacation + ⅓ | +11.1% |
| FGTS | +8% |
| Employer social security, health plan, meal allowance, life insurance | varies, often the largest piece |

Market rule of thumb: **PJ needs roughly 30–50% above the CLT gross** to hold the package even.
Then subtract the PJ-side costs: the Simples Nacional band (which the revenue level determines —
crossing a bracket materially changes the effective rate), the accountant's fee, and the payroll
draw required to stay in the favourable annex.

⚠️ Service **exports** are treated differently — typically exempt from municipal service tax and
from PIS/COFINS, which lowers the effective rate below the headline table. This is exactly the kind
of thing to confirm with the accountant, not to assume.

## When the salary is in foreign currency

Three things to surface, every time:

1. **Today's official rate**, from the central bank, dated. Not an app's mid-market quote.
2. **The FX exposure.** Salary in one currency, bills in another. Model the downside: *"at 4.50
   instead of 5.15, this offer is 13% smaller and nobody will tell you."*
3. **Conversion cost.** Spreads vary by an order of magnitude between providers. On a monthly
   salary that is real money.

Then: does the contract have an annual review clause? Ask.

## Output

```markdown
### Verified data
| Reference | Value | Source | Sample |

### The recommendation
|          | Monthly | Hourly | Local currency |
| Anchor   |         |        |                |
| Target   |         |        |                |
| Floor    |         |        |                |

### Why the anchor is here and not higher
### Why the floor is here and not lower
### ⚠️ What I could not verify
### The negotiation script
```

## Negotiation script

**Turn the question around first:**
> *"Before I give you a number — is this employee or contractor, and is it quoted monthly or
> hourly? That changes my answer."*

**Then anchor, with a reason attached** — a number with a justification is harder to negotiate down
than a bare number.

**If they say it is above budget:**
> *"I understand. What range is the client working with? If we're close I'd rather talk about it
> than rule it out."*

Never cut your own number before hearing theirs.

⚠️ Never let the person say *"I'm flexible"* or *"whatever's fair"* without a number. Staffing firms
work on margin; a vague answer becomes a low offer.

Record the quoted figure and date in the tracker (skill `04`).
