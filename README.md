<div align="center">

# career-agent

**The job search that lives in your repo — and never invents a thing.**

[![License: MIT](https://img.shields.io/badge/License-MIT-000000.svg?style=flat-square)](LICENSE)
[![Agent-agnostic](https://img.shields.io/badge/agent-agnostic-6f42c1?style=flat-square)](AGENTS.md)
[![Evidence gate](https://img.shields.io/badge/anti--fabrication-enforced%20in%20CI-0a7d33?style=flat-square)](tools/verify_evidence.py)
[![pt-BR](https://img.shields.io/badge/leia%20em-portugu%C3%AAs-009c3b?style=flat-square)](README.pt-BR.md)

*Nine skills that find the job, screen the ATS before you waste a CV, tailor the résumé against a
locked evidence bank, and hand back the exact posting on the day of the interview.*

[What makes it different](#what-makes-it-different) · [Install](#install) · [The loop](#the-loop) ·
[Skills](#the-nine-skills) · [Privacy](#privacy)

</div>

---

## Why this exists

This started as one person's job search, run entirely through a coding agent. Fifteen applications,
five different applicant-tracking systems, one asynchronous audio screen, one recruiter on WhatsApp.

Along the way the same problems kept repeating, and none of the existing job-search agents solved
them:

- A full CV was built for a role, and only then did we discover the application ran on **Gupy** —
  whose free-text fields reject every form of automation. The work was wasted.
- Two applications were sitting **confirmed in a second inbox** nobody was checking, because
  LinkedIn routes to one address and every other ATS routes to another.
- A recommendation to target architect-level roles was **wrong by five years of seniority**, and only
  a real conversation with a recruiter surfaced it.
- An interview arrived and the posting had **scrolled out of the chat history** — no way to recall
  what had been promised on paper.
- An asynchronous **audio interview** came back with feedback that was right but vague; the actual
  problem only became visible after transcribing the recordings and counting how many times the
  candidate said *"we"* instead of *"I"*. It was eighty-one times.

Every one of those became a skill. That is what this repository is.

## What makes it different

Most job-search agents optimise for volume. This one optimises for **not embarrassing you**.

**A locked evidence bank.** `profile/<you>/evidence.md` is the single source of truth. A technology
can only reach your CV if it is in there, with the role and project where you actually used it.
`tools/verify_evidence.py` runs in CI and fails the build if anything slips through. No "adjacent"
skills, no inflated numbers, no keyword stuffing. Fabrication does not fail at the CV stage — it
fails in the technical interview, which is worse than never applying.

**ATS triage before CV work.** Skill `02` identifies the applicant-tracking system from the posting
link *before* a single line of CV gets written, and warns you when the platform is one you have
decided not to deal with. Cheap check, expensive mistake.

**The posting comes back for the interview.** Skill `04` archives the full job description at apply
time. Skill `06` reads it back weeks later and builds the prep pack: what they asked for, what you
sent, where the two meet, where the gap is, likely HR questions, likely technical questions, and the
honest bridge answer for everything you cannot claim.

**Audio interview preparation.** Asynchronous audio screens are now standard in some markets. Skill
`07` transcribes your own practice recordings locally with Whisper, measures pace, counts verbal
tics and ownership language, and rebuilds each answer in a Context → Action → Result shape with a
clock against it.

**Compensation maths that matches reality.** Skill `08` pulls per-company, per-role data rather than
national averages, and — for markets where it matters — does the employment-type conversion
(Brazil's CLT ↔ PJ), the tax band, and the FX exposure when salary is quoted in a foreign currency.

**It runs anywhere.** Instructions live in [`AGENTS.md`](AGENTS.md), the open format that Claude
Code, Codex, Cursor, Gemini CLI, Copilot and Windsurf all read. `CLAUDE.md` is a one-line pointer.
No lock-in.

## Install

```bash
gh repo clone gregoryfiel/career-agent   # or: git clone https://github.com/gregoryfiel/career-agent
cd career-agent

# Optional — only skill 07 (audio) and the page checker need these
pip install -r tools/requirements.txt
sudo apt-get install -y ffmpeg libreoffice poppler-utils
```

Then open the folder in your agent of choice and say:

```
Run skill 00-onboarding for me.
```

The onboarding interview takes about twenty minutes and produces your evidence bank. Everything else
depends on it.

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

The arrow that matters most is the one going back into the evidence bank. Every interview surfaces
something you had forgotten you did.

## The nine skills

| # | Skill | What it does |
|---|---|---|
| `00` | **onboarding** | Builds the evidence bank from your CV, LinkedIn or a guided conversation. Marks gaps rather than filling them. |
| `01` | **job-radar** | Finds open roles across job boards and LinkedIn, scores fit against your profile, filters by your seniority band. |
| `02` | **ats-triage** | ⭐ Resolves the application link to its ATS **before** CV work starts. Flags platforms on your do-not-use list. |
| `03` | **tailored-cv** | Drafter writes, a fresh reviewer critiques with company research, then verification: evidence gate, page count, ATS text layer. |
| `04` | **application-tracker** | One row per application, one folder per company — CV sent, posting archived, status, salary quoted. |
| `05` | **inbox-sweep** | Sweeps every inbox you actually use, because confirmations do not all land in the same one. |
| `06` | **interview-prep** | ⭐ Re-serves the archived posting. Builds HR and technical prep, maps your stories, writes honest bridge answers. |
| `07` | **audio-interview** | ⭐ Transcribes practice recordings locally. Measures pace, tics, ownership language. Rebuilds answers as Context → Action → Result. |
| `08` | **salary-research** | ⭐ Per-company compensation data, employment-type conversion, FX exposure, and the negotiation script. |

⭐ = not found in any comparable project. Each one came from a specific failure.

## Privacy

Your career is not training data and it is not a public artefact.

`profile/` is gitignored except the fictional example. Nothing personal is ever committed, pasted
into a web form, or sent to a third-party service. Audio transcription runs locally on your machine
via Whisper — recordings never leave it.

The agent **never submits anything on your behalf**. It drafts, verifies, and hands it over. Clicking
"apply" is yours, always. Full detail in [`docs/privacy.md`](docs/privacy.md).

## Documentation

- [`AGENTS.md`](AGENTS.md) — canonical agent instructions ([português](AGENTS.pt-BR.md))
- [`docs/how-it-works.md`](docs/how-it-works.md) — the loop end to end ([português](docs/how-it-works.pt-BR.md))
- [`docs/brazilian-market.md`](docs/brazilian-market.md) — Gupy, CLT vs PJ, audio screens, inbox routing ([português](docs/brazilian-market.pt-BR.md))
- [`docs/privacy.md`](docs/privacy.md) — what never leaves your machine ([português](docs/privacy.pt-BR.md))

## Contributing

The skills are markdown. If your market has a different dominant ATS, a different employment-type
maths, or a screening format this repo has not met yet — open a PR. That is the whole extension
mechanism.

## License

MIT — see [LICENSE](LICENSE).
