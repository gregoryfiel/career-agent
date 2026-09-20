# Skill 03 — Tailored CV

**Goal:** a CV aimed at one specific posting where **every line traces to the evidence bank**.

## Preconditions

- `profile/<person>/evidence.md` exists and has been read **in this session**. Not summarised from
  memory — read.
- Skill `02` has run and the ATS is known and acceptable.
- The full posting text is saved (skill `04` needs it anyway).

If any is missing, stop and say which.

## Phase 1 — Requirement mapping

Before writing a word, build the table. It is the contract for the whole document.

| Requirement (their words) | Evidence | Verdict |
|---|---|---|
| Azure Databricks | 4 yrs, ilegra + NTT DATA | ✅ strong |
| PySpark, production pipelines | terabyte-scale ETL, ~1 TB fact | ✅ strong |
| CDC / change data capture | MERGE, SCD2, DLT incremental, time travel | ⚠️ partial — no Change Data Feed, no Debezium |
| SSIS | — | ❌ none |

Show this to the person **before drafting**. It is the honest picture of fit, and it is what the
bridge answers in skill `06` are built from.

If the ❌ row is an eliminatory requirement, say so now: *"They call this eliminatory and you don't
have it. Still want the CV?"*

## Phase 2 — Draft

Lead with what the posting leads with. If they open on migration, the summary opens on migration.

- **Verbs, not nouns.** "Migrated 1,677 tables" beats "responsible for migration."
- **Numbers from the evidence bank only**, exactly as recorded.
- **Mirror their vocabulary** where the evidence supports it. They say "lakehouse", the CV says
  lakehouse — but only if the person has actually built one.
- **Never stuff a keyword** the evidence bank does not back. A missing keyword is a gap you address
  in the interview. A fabricated one is a lie you defend badly in the interview.
- Match the target title's level. Do not present as a lead for an individual-contributor role — it
  reads as overqualified and gets filtered.

## Phase 3 — Review (fresh eyes)

Spawn a **separate reviewer** with no memory of the drafting. Give it the posting, the draft and
the evidence bank, and ask for:

1. Any claim not traceable to the evidence bank — quote it.
2. Requirements from the posting that the draft failed to address but the evidence supports.
3. Generic filler that could belong to any candidate.
4. Company research: what does this employer actually do, and does the draft speak to it?

Then revise. The two-pass split catches things a single pass rereading its own work does not.

## Phase 4 — Verify (all four gates must pass)

```bash
python3 tools/verify_evidence.py --cv output/<file>.md --profile profile/<person>
bash tools/check_pages.sh output/<file>.pdf 2      # page ceiling
```

1. **Evidence gate** — exits 0. No unbacked technology anywhere in the document.
2. **Page count** — within the ceiling (2 pages is the default; some markets differ).
3. **ATS text layer** — extract the PDF's text and read it as a parser would. Contact details must
   be literal text, not icon glyphs. Reading order must make sense. No garbled fonts.
4. **Numbers match the evidence bank exactly.** Not approximately.

## Phase 5 — Trimming, when over the page ceiling

Do **not** chop the oldest role. Score every line:

```
score = relevance_to_posting + uniqueness_in_document + story_dependency
```

Cut lowest first. An old role with three matching keywords outranks a recent one with none. A line
that is the only evidence for a required skill is nearly uncuttable. A line whose achievement you
plan to tell as a story in the interview stays.

## Output

```
output/<Company>_<Role>/
  CV_<Person>_<Company>_<Role>.docx
  CV_<Person>_<Company>_<Role>.pdf
  CV_<Person>_<Company>_<Role>_ATS_SAFE.docx   # no tables, no columns, no icons
  requirement-map.md                            # phase 1 table — skill 06 reads this
```

Report to the person: what you led with and why · which requirements are covered · **which are not,
named out loud** · which gates passed.
