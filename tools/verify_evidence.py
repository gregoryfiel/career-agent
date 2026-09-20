#!/usr/bin/env python3
"""
verify_evidence.py — the anti-fabrication gate.

Cross-checks a generated document (CV, cover letter, prep pack) against the person's evidence bank
and fails loudly when a technology appears that nothing in their history backs.

This is the rule from AGENTS.md §2.1, made executable. It runs in CI so it cannot be forgotten.

Usage
-----
    # check one document against a profile
    python3 tools/verify_evidence.py --cv output/CV_Acme.md --profile profile/gabriela

    # check that a profile's evidence bank is well formed (no document needed)
    python3 tools/verify_evidence.py --profile profile/gabriela

    # check the committed example (what CI runs)
    python3 tools/verify_evidence.py --profile profile/_example --self-test

Exit codes
----------
    0  clean
    1  a claim was found with no evidence behind it
    2  usage / parsing error
"""

from __future__ import annotations

import argparse
import re
import sys
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
    "Kafka", "Debezium", "Change Data Feed", "Kinesis", "Pub/Sub", "Flink", "Pulsar",
    # infra
    "Terraform", "Bicep", "Pulumi", "Kubernetes", "OpenShift", "Ansible", "Jenkins",
    "ARM Template", "CloudFormation", "Helm",
    # languages / frameworks
    "Scala", "Golang", "Rust", "Java", "C#", ".NET", "Ruby", "PHP", "Angular", "Vue",
    # stores
    "MongoDB", "Cassandra", "DynamoDB", "Neo4j", "Elasticsearch", "ClickHouse",
    # ml / analytics
    "MLflow", "Kubeflow", "SageMaker", "Azure ML", "Vertex AI", "dbt", "Looker", "Tableau",
    # marketing / comms (non-engineering profiles)
    "Salesforce", "HubSpot", "RD Station", "Marketo", "Google Analytics", "GA4",
    "Meta Ads", "Google Ads", "SEMrush", "Ahrefs", "Hootsuite", "Buffer",
]

CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`]*`")
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")

# Lines in evidence.md that mark something as explicitly NOT possessed.
NEGATION_MARKERS = ("❌", "não tenho", "no evidence", "do not claim", "nao tenho", "sem evidência")


def strip_noise(text: str) -> str:
    """Remove code blocks and link targets so we match prose, not markup."""
    text = CODE_FENCE.sub(" ", text)
    text = INLINE_CODE.sub(" ", text)
    text = MD_LINK.sub(r"\1", text)
    return text


def load_evidence(profile_dir: Path) -> tuple[str, set[str], list[str]]:
    """Return (positive evidence text, explicitly denied terms, extra watchlist terms)."""
    ev_path = profile_dir / "evidence.md"
    if not ev_path.exists():
        print(f"error: no evidence bank at {ev_path}", file=sys.stderr)
        print("       run skill 00-onboarding first.", file=sys.stderr)
        raise SystemExit(2)

    raw = ev_path.read_text(encoding="utf-8")
    positive_lines: list[str] = []
    denied: set[str] = set()
    extra_watch: list[str] = []
    in_watchlist = False

    for line in raw.splitlines():
        stripped = line.strip()
        low = stripped.lower()

        if stripped.startswith("#"):
            in_watchlist = "watchlist" in low
            continue

        if in_watchlist:
            term = stripped.lstrip("-*| ").split("|")[0].strip()
            if term:
                extra_watch.append(term)
            continue

        if any(marker in low for marker in NEGATION_MARKERS):
            # First cell of a table row, or the text after a bullet, is the denied item.
            cells = [c.strip() for c in stripped.strip("|").split("|")] if "|" in stripped else [stripped]
            head = cells[0].lstrip("-*• ").strip()
            head = re.sub(r"[❌⚠️✅]", "", head).strip()
            if head:
                denied.add(head.lower())
            continue

        positive_lines.append(stripped)

    return "\n".join(positive_lines).lower(), denied, extra_watch


def find_unbacked(doc_text: str, evidence: str, denied: set[str], watchlist: list[str]):
    """Return (violations, denied_hits) found in doc_text."""
    haystack = strip_noise(doc_text).lower()
    violations, denied_hits = [], []

    for term in watchlist:
        pattern = re.compile(r"(?<![\w-])" + re.escape(term.lower()) + r"(?![\w-])")
        if not pattern.search(haystack):
            continue
        if term.lower() in denied:
            denied_hits.append(term)
        elif not pattern.search(evidence):
            violations.append(term)

    return violations, denied_hits


def main() -> int:
    ap = argparse.ArgumentParser(description="Anti-fabrication gate for career-agent.")
    ap.add_argument("--profile", required=True, type=Path, help="profile/<person> directory")
    ap.add_argument("--cv", type=Path, action="append", default=[],
                    help="document to check (repeatable)")
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

        violations, denied_hits = find_unbacked(
            doc.read_text(encoding="utf-8"), evidence, denied, watchlist
        )

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
