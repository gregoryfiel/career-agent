#!/usr/bin/env python3
"""
verify_evidence.py — the anti-fabrication gate.

Cross-checks a generated document (CV, cover letter, prep pack) against the person's evidence bank
and fails loudly when a technology appears that nothing in their history backs.

This is the rule from AGENTS.md §2.1, made executable. It runs in CI so it cannot be forgotten.

Usage
-----
    # check the real deliverable — the build writes these
    python3 tools/verify_evidence.py --profile profile/<person> \\
        --cv output/<name>/CV_<name>.docx

    # the CV data file, the PDF, or a markdown draft work too (repeat --cv for several)
    python3 tools/verify_evidence.py --profile profile/<person> \\
        --cv templates/cv/cv_acme.js --cv output/<name>/CV_<name>.pdf

    # check that a profile's evidence bank is well formed (no document needed)
    python3 tools/verify_evidence.py --profile profile/<person>

    # check the committed example (what CI runs)
    python3 tools/verify_evidence.py --profile profile/_example --self-test

Supported documents
-------------------
    .md .txt   read as text
    .docx      text extracted from word/document.xml (stdlib only)
    .pdf       text extracted with `pdftotext` (poppler-utils)
    .js .json  CV data files — comments are stripped first, so a header that lists the
               technologies deliberately left OUT of the CV does not trip the gate

Exit codes
----------
    0  clean
    1  a claim was found with no evidence behind it
    2  usage / parsing error
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# ── Terms worth policing ──────────────────────────────────────────────────────
# Not an exhaustive tech list — these are the ones that get fabricated, because they are common
# "nice to haves" that feel adjacent to something the person genuinely knows.
# Extend per profile via a `## Watchlist` section in evidence.md.
DEFAULT_WATCHLIST = [
    # cloud
    "AWS", "GCP", "Google Cloud", "Azure", "Alibaba Cloud", "OCI",
    # data platforms
    "Snowflake", "BigQuery", "Redshift", "Databricks", "Synapse", "Microsoft Fabric",
    "Teradata", "Hive", "SAS", "SSIS", "Informatica", "Talend",
    # streaming / CDC
    "Kafka", "MSK", "Event Hubs", "Debezium", "Change Data Feed", "Auto Loader", "Kinesis",
    "Pub/Sub", "Flink", "Pulsar",
    # infra
    "Terraform", "Bicep", "Pulumi", "Kubernetes", "OpenShift", "Ansible", "Jenkins",
    "ARM Template", "CloudFormation", "Helm",
    # languages / frameworks
    "Scala", "Golang", "Rust", "Java", "C#", ".NET", "Ruby", "PHP", "Angular", "Vue",
    # stores
    "MongoDB", "Cassandra", "DynamoDB", "Cosmos DB", "Neo4j", "Elasticsearch", "ClickHouse",
    # ml / analytics
    "MLflow", "Kubeflow", "SageMaker", "Azure ML", "Vertex AI", "dbt", "Looker", "Tableau",
    "Genie",
    # ERP
    "SAP BW", "BODS",
    # marketing / comms (non-engineering profiles)
    "Salesforce", "HubSpot", "RD Station", "Marketo", "Google Analytics", "GA4",
    "Meta Ads", "Google Ads", "SEMrush", "Ahrefs", "Hootsuite", "Buffer",
]

CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`]*`")
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")

# Markers in evidence.md that mean "this is NOT possessed".
NEGATION_MARKERS = ("❌", "não tenho", "nao tenho", "no evidence", "do not claim",
                    "sem evidência", "sem evidencia", "never used", "nunca usei")
POSITIVE_MARKER = "✅"

# A heading containing any of these opens a section where every row is a denial.
GAP_HEADING = re.compile(r"(❌|\bgaps?\b|lacunas?|do not claim|não reivindicar|nao reivindicar)",
                         re.IGNORECASE)

# Where a denied item's name ends in a free-text bullet: "Kafka — never used", "Kafka: no".
HEAD_SPLIT = re.compile(r"\s+[—–-]\s+|:\s|\(|,|;")


# ── Reading documents ─────────────────────────────────────────────────────────

def _docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = re.sub(r"</w:p>", "\n", xml)          # paragraph → line
    xml = re.sub(r"<w:tab/>", " ", xml)
    xml = re.sub(r"<[^>]+>", "", xml)           # drop every tag, keep <w:t> text
    return html.unescape(xml)


def _pdf_text(path: Path) -> str:
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext not installed (poppler-utils) — check the .docx instead")
    out = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                         capture_output=True, check=True)
    return out.stdout.decode("utf-8", errors="replace")


def _js_text(path: Path) -> str:
    src = path.read_text(encoding="utf-8")
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.DOTALL)                 # block comments
    src = re.sub(r"(?m)^\s*//.*$", " ", src)                               # line comments
    src = re.sub(r"(?<![:'\"\w])//[^\n'\"]*$", " ", src, flags=re.MULTILINE)  # trailing //
    return src


def read_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return _docx_text(path)
    if suffix == ".pdf":
        return _pdf_text(path)
    if suffix in (".js", ".cjs", ".mjs", ".json"):
        return _js_text(path)
    return path.read_text(encoding="utf-8")


def strip_noise(text: str) -> str:
    """Remove code blocks and link targets so we match prose, not markup."""
    text = CODE_FENCE.sub(" ", text)
    text = INLINE_CODE.sub(" ", text)
    text = MD_LINK.sub(r"\1", text)
    return text


# ── Reading the evidence bank ─────────────────────────────────────────────────

def _clean_head(text: str) -> str:
    text = re.sub(r"[❌⚠✅️]", "", text)
    text = text.lstrip("-*•| ").strip()
    return HEAD_SPLIT.split(text, maxsplit=1)[0].strip() if text else ""


def classify_line(line: str, in_gap_section: bool) -> tuple[str, str]:
    """Return ("deny", item) or ("positive", line) for one evidence-bank line.

    A line is a denial only when the negation is about the line's own subject. A positive line that
    merely mentions something else it does NOT have ("Databricks ✅ — not Snowflake ❌") stays
    positive: its subject is evidenced, and the aside is not a claim about the subject.
    """
    stripped = line.strip()
    low = stripped.lower()
    is_row = stripped.startswith("|")
    cells = [c.strip() for c in stripped.strip("|").split("|")] if is_row else [stripped]

    if in_gap_section and not set(stripped) <= set("|-: "):
        # Inside an explicit gaps section the first cell / bullet text is always the denied item.
        # Keep the whole first cell so "Video editing (Premiere, After Effects)" denies both tools.
        head = re.sub(r"[❌⚠✅️]", "", cells[0]).lstrip("-*•| ").strip()
        return ("deny", head) if head else ("positive", stripped)

    neg_positions = [low.find(m) for m in NEGATION_MARKERS if m in low]
    if not neg_positions:
        return "positive", stripped
    first_neg = min(neg_positions)

    first_pos = stripped.find(POSITIVE_MARKER)
    if first_pos != -1 and first_pos < first_neg:
        return "positive", stripped              # opens positive; the negation is an aside

    if is_row:
        # Only the subject cell or the status cell may carry the verdict about the subject.
        verdict_cells = " ".join(cells[:2]).lower()
        if not any(m in verdict_cells for m in NEGATION_MARKERS):
            return "positive", stripped
        return "deny", re.sub(r"[❌⚠✅️]", "", cells[0]).strip()

    head = _clean_head(stripped)
    return ("deny", head) if head else ("positive", stripped)


def load_evidence(profile_dir: Path) -> tuple[str, list[str], list[str]]:
    """Return (positive evidence text, explicitly denied items, extra watchlist terms)."""
    ev_path = profile_dir / "evidence.md"
    if not ev_path.exists():
        print(f"error: no evidence bank at {ev_path}", file=sys.stderr)
        print("       run skill 00-onboarding first.", file=sys.stderr)
        raise SystemExit(2)

    raw = ev_path.read_text(encoding="utf-8")
    positive_lines: list[str] = []
    denied: list[str] = []
    extra_watch: list[str] = []
    in_watchlist = in_gaps = False

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("#"):
            low = stripped.lower()
            in_watchlist = "watchlist" in low
            in_gaps = bool(GAP_HEADING.search(stripped)) and not in_watchlist
            continue

        if in_watchlist:
            term = stripped.lstrip("-*| ").split("|")[0].strip()
            if term:
                extra_watch.append(term)
            continue

        # Table header / separator rows carry no claim.
        if set(stripped) <= set("|-: "):
            continue

        kind, value = classify_line(stripped, in_gaps)
        if kind == "deny":
            denied.append(value.lower())
        else:
            positive_lines.append(value)

    return "\n".join(positive_lines).lower(), denied, extra_watch


# ── Checking ──────────────────────────────────────────────────────────────────

def _term_pattern(term: str) -> re.Pattern:
    return re.compile(r"(?<![\w-])" + re.escape(term.lower()) + r"(?![\w-])")


def find_unbacked(doc_text: str, evidence: str, denied: list[str], watchlist: list[str]):
    """Return (violations, denied_hits) found in doc_text."""
    haystack = strip_noise(doc_text).lower()
    violations, denied_hits = [], []

    for term in watchlist:
        pattern = _term_pattern(term)
        if not pattern.search(haystack):
            continue
        if any(pattern.search(d) for d in denied):
            denied_hits.append(term)
        elif not pattern.search(evidence):
            violations.append(term)

    return violations, denied_hits


def main() -> int:
    ap = argparse.ArgumentParser(description="Anti-fabrication gate for career-agent.")
    ap.add_argument("--profile", required=True, type=Path, help="profile/<person> directory")
    ap.add_argument("--cv", type=Path, action="append", default=[],
                    help="document to check: .docx .pdf .js .md .txt (repeatable)")
    ap.add_argument("--self-test", action="store_true",
                    help="only validate that the evidence bank parses")
    args = ap.parse_args()

    if not args.profile.is_dir():
        print(f"error: {args.profile} is not a directory", file=sys.stderr)
        return 2

    evidence, denied, extra_watch = load_evidence(args.profile)

    # Merge and de-duplicate case-insensitively, keeping first-seen spelling.
    watchlist, seen = [], set()
    for term in DEFAULT_WATCHLIST + extra_watch:
        if term.lower() not in seen:
            seen.add(term.lower())
            watchlist.append(term)

    print(f"evidence bank : {args.profile / 'evidence.md'}")
    print(f"watchlist     : {len(watchlist)} terms ({len(extra_watch)} profile-specific)")
    print(f"explicit gaps : {len(denied)} recorded")

    if args.self_test or not args.cv:
        if not evidence.strip():
            print("\n✗ evidence bank is empty — nothing to verify against", file=sys.stderr)
            return 1
        print("\n✓ evidence bank parses")
        return 0

    failed = False
    for doc in args.cv:
        if not doc.exists():
            print(f"\n✗ {doc}: file not found", file=sys.stderr)
            failed = True
            continue

        try:
            text = read_document(doc)
        except (RuntimeError, KeyError, zipfile.BadZipFile, subprocess.CalledProcessError,
                UnicodeDecodeError) as exc:
            print(f"\n✗ {doc}: could not read ({exc})", file=sys.stderr)
            return 2

        violations, denied_hits = find_unbacked(text, evidence, denied, watchlist)

        print(f"\n── {doc}")
        if denied_hits:
            failed = True
            print("  ✗ CLAIMS SOMETHING THE EVIDENCE BANK EXPLICITLY DENIES:")
            for t in denied_hits:
                print(f"      • {t}  ← recorded as 'does not have'")
        if violations:
            failed = True
            print("  ✗ NO EVIDENCE FOUND FOR:")
            for t in violations:
                print(f"      • {t}")
        if not denied_hits and not violations:
            print("  ✓ every watched term traces to the evidence bank")

    if failed:
        print(
            "\n"
            "─────────────────────────────────────────────────────────────\n"
            "Fix by one of:\n"
            "  1. remove the claim from the document, or\n"
            "  2. add real evidence to evidence.md — role, project, proof.\n"
            "\n"
            "Do not add it to the evidence bank unless it actually happened.\n"
            "A CV gets you the interview. Fabrication loses it in front of\n"
            "someone who knows the difference.\n"
            "─────────────────────────────────────────────────────────────",
            file=sys.stderr,
        )
        return 1

    print("\n✓ all documents clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
