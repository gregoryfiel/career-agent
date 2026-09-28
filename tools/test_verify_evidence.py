#!/usr/bin/env python3
"""Tests for verify_evidence.py — stdlib only, run with:  python3 -m unittest tools/test_verify_evidence.py"""

from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_evidence as ve  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EXAMPLE = REPO / "profile" / "_example"


def _profile(evidence_md: str) -> Path:
    d = Path(tempfile.mkdtemp())
    (d / "evidence.md").write_text(evidence_md, encoding="utf-8")
    return d


def _check(profile: Path, text: str, watch=None):
    evidence, denied, extra = ve.load_evidence(profile)
    return ve.find_unbacked(text, evidence, denied, (watch or ve.DEFAULT_WATCHLIST) + extra)


def _docx(text: str) -> Path:
    """Smallest valid-enough .docx: only word/document.xml, which is all the gate reads."""
    p = Path(tempfile.mkdtemp()) / "cv.docx"
    paras = "".join(f"<w:p><w:r><w:t>{line}</w:t></w:r></w:p>" for line in text.splitlines())
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           f"<w:body>{paras}</w:body></w:document>")
    with zipfile.ZipFile(p, "w") as z:
        z.writestr("word/document.xml", xml)
    return p


class NegationParsing(unittest.TestCase):
    def test_positive_row_with_negated_aside_keeps_subject(self):
        # Regression: this used to deny Databricks because ❌ appeared anywhere on the line.
        p = _profile("| Tech | Status | Notes |\n|---|---|---|\n"
                     "| Databricks | ✅ 3 yrs | not Snowflake ❌ |\n")
        violations, denied = _check(p, "Pipelines on Databricks.")
        self.assertEqual((violations, denied), ([], []))

    def test_positive_bullet_with_negated_aside_is_evidence(self):
        # Regression: the whole line was dropped, so Terraform lost its evidence.
        p = _profile("- Terraform ✅ — no evidence of Pulumi\n")
        violations, denied = _check(p, "Infra as code with Terraform.")
        self.assertEqual((violations, denied), ([], []))

    def test_denied_row(self):
        p = _profile("| Kafka | ❌ | never used |\n")
        _, denied = _check(p, "Streaming with Kafka.")
        self.assertEqual(denied, ["Kafka"])

    def test_denied_bullet_extracts_the_name_only(self):
        # Regression: the denied item used to be the whole sentence, so it never matched.
        p = _profile("- ❌ Kafka — never used, only Delta Live Tables\n")
        _, denied = _check(p, "Streaming with Kafka.")
        self.assertEqual(denied, ["Kafka"])

    def test_gap_section_denies_every_tool_in_the_cell(self):
        p = _profile("## Explicit gaps — do not claim\n"
                     "| Item | Status |\n|---|---|\n"
                     "| Video editing (Premiere, After Effects) | none |\n")
        _, denied = _check(p, "Edited video in After Effects.", watch=["After Effects"])
        self.assertEqual(denied, ["After Effects"])


class DocumentFormats(unittest.TestCase):
    def test_docx_is_read(self):
        # Regression: the gate crashed with UnicodeDecodeError on the real deliverable.
        doc = _docx("Campanhas em Google Ads.")
        evidence, denied, extra = ve.load_evidence(EXAMPLE)
        text = ve.read_document(doc)
        _, denied_hits = ve.find_unbacked(text, evidence, denied, ve.DEFAULT_WATCHLIST + extra)
        self.assertIn("Google Ads", denied_hits)

    def test_js_comments_do_not_trip_the_gate(self):
        # CV data files list what was deliberately left OUT in a header comment. That is not a claim.
        js = Path(tempfile.mkdtemp()) / "cv_x.js"
        js.write_text(
            "/**\n * NOT mentioned anywhere, by design: Google Ads · HubSpot\n */\n"
            "// also not: RD Station\n"
            "module.exports = { summary: 'Meta Ads e GA4.', link: 'https://x.io/a//b' };\n",
            encoding="utf-8")
        evidence, denied, extra = ve.load_evidence(EXAMPLE)
        v, d = ve.find_unbacked(ve.read_document(js), evidence, denied,
                                ve.DEFAULT_WATCHLIST + extra)
        self.assertEqual((v, d), ([], []))

    def test_js_claims_in_strings_are_still_caught(self):
        js = Path(tempfile.mkdtemp()) / "cv_y.js"
        js.write_text("module.exports = { summary: 'Automação com RD Station.' };\n",
                      encoding="utf-8")
        evidence, denied, extra = ve.load_evidence(EXAMPLE)
        _, d = ve.find_unbacked(ve.read_document(js), evidence, denied,
                                ve.DEFAULT_WATCHLIST + extra)
        self.assertIn("RD Station", d)


class ExampleProfileContract(unittest.TestCase):
    """The same two cases CI has always run — behaviour must not change."""

    def test_fabricated_claim_is_rejected(self):
        v, d = _check(EXAMPLE, "Campanhas em Google Ads e automação com RD Station.")
        self.assertTrue(v or d)

    def test_clean_claim_passes(self):
        v, d = _check(EXAMPLE, "Campanhas em Meta Ads e relatórios mensais em GA4.")
        self.assertEqual((v, d), ([], []))


if __name__ == "__main__":
    unittest.main(verbosity=2)
