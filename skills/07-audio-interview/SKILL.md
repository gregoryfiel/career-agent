# Skill 07 — Asynchronous audio interview ⭐

**Goal:** perform well in one-way recorded screens — a bot sends a question, you record an answer
against a clock, a human reviews it later.

Common in the Brazilian market (DigAI is the platform CI&T and others use over WhatsApp) and
spreading elsewhere. Very few candidates prepare for the format specifically, which is the opening.

## Why this skill exists

A candidate finished one of these and got feedback that was accurate but vague: *"be more
structured, be more objective."* Only after transcribing the recordings did the real picture
appear — the pacing was fine, but he said *"we"* eighty-one times instead of *"I"*, opened his
strongest story with *"this was a simple problem to solve"*, buried his best number three minutes
in, and sent one answer **after the clock expired**.

None of that is visible without the transcript. All of it is fixable in an afternoon.

## Part A — Before: the format

**The clock includes reading time.** The timer starts when the question appears, not when recording
starts. Budget for it.

**Send at 80% of the limit.** Five minutes means send at four. An answer cut short still counts; an
answer sent after the deadline may count as nothing.

**One question, one recording.** Do not re-record unless the platform explicitly allows it.

**Structure beats content here.** The reviewer is comparing dozens of recordings. Structure is what
makes yours followable.

## Part B — The answer shape

```
 0:00–0:20   RESULT FIRST     "I'll tell you about the time I cut X to Y."
 0:20–1:00   CONTEXT          where, which client, what was wrong
 1:00–2:45   ACTION           one or two decisions — what I investigated and decided, and why
 2:45–3:30   RESULT           the measured outcome
 3:30–4:00   LEARNING         the rule you carry forward
 4:00–5:00   SAFETY MARGIN    send here
```

Two rules do most of the work:

1. **Lead with the result.** A reviewer who hears the outcome in the first fifteen seconds listens
   to the rest. One who waits three minutes has already scored you.
2. **Two decisions maximum.** Every additional technical thread reduces clarity. Pick two, go deep.

## Part C — Practice, then measure

Have the person record practice answers to the likely questions (from skill `06`). Then:

```bash
python3 tools/transcribe_audio.py practice/*.opus --lang pt --out transcripts/
```

Runs locally via Whisper. **Recordings never leave the machine.**

Analyse the transcript for:

| Signal | Why it matters | Target |
|---|---|---|
| **Pace** | Nervousness shows as speed | 120–150 wpm |
| **"we" vs "I"** | ⭐ Dilutes ownership of your own work | "I" for what you decided, built or defended |
| **Opening sentence** | First ten seconds carry disproportionate weight | Never self-deprecating |
| **Where the number lands** | Buried results do not register | First thirty seconds |
| **Filler density** | "etc", "kind of", "like", trailing lists | Close your lists |
| **Technical terms** | ASR mishearing you reveals unclear diction | Say the important ones slowly |
| **Unfinished sentences** | Three ideas in one sentence, thread lost | Short sentence. Full stop. |
| **Numbers vs the CV** | ⭐ A figure that differs from the CV destroys credibility | Identical, always |

The self-sabotage patterns to flag explicitly, because people do not hear themselves doing it:

- *"This was a simple problem"* — opening a hard-problem question by devaluing the story
- *"It's overkill, but…"* — undermining a decision that was correct
- Over-explaining a gap in the CV, which reads as defensive

## Part D — Deliver

```
interview-audio-prep-<company>-<date>.md
```

Containing: the transcript with the measured table · the specific habits to break, quoted from
their own words · each story rebuilt in the shape above with a clock · a pronunciation list for the
terms that came out wrong · the execution protocol · a pocket card.

Keep transcripts out of git — they are in `.gitignore` for a reason.
