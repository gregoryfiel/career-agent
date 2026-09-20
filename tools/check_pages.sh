#!/usr/bin/env bash
# check_pages.sh — enforce a page ceiling on a generated CV.
#
#   bash tools/check_pages.sh output/CV_Acme.docx 2
#   bash tools/check_pages.sh output/CV_Acme.pdf  2
#
# Converts DOCX to PDF via LibreOffice when needed, then counts pages with pdfinfo.
# Requires: libreoffice, poppler-utils

set -euo pipefail

FILE="${1:?usage: check_pages.sh <file.docx|file.pdf> [max_pages]}"
MAX="${2:-2}"

[[ -f "$FILE" ]] || { echo "✗ not found: $FILE" >&2; exit 2; }

PDF="$FILE"
if [[ "$FILE" == *.docx || "$FILE" == *.odt ]]; then
  command -v soffice >/dev/null || { echo "✗ libreoffice not installed" >&2; exit 2; }
  TMP="$(mktemp -d)"
  soffice --headless --convert-to pdf --outdir "$TMP" "$FILE" >/dev/null 2>&1
  PDF="$TMP/$(basename "${FILE%.*}").pdf"
fi

command -v pdfinfo >/dev/null || { echo "✗ poppler-utils not installed" >&2; exit 2; }
PAGES="$(pdfinfo "$PDF" | awk '/^Pages:/ {print $2}')"

if (( PAGES > MAX )); then
  echo "✗ $(basename "$FILE"): $PAGES pages (ceiling: $MAX)"
  echo
  echo "  Do not chop the oldest role. Score every line and cut the lowest:"
  echo "    score = relevance_to_posting + uniqueness_in_document + story_dependency"
  echo "  See skills/03-tailored-cv/SKILL.md, phase 5."
  exit 1
fi

echo "✓ $(basename "$FILE"): $PAGES page(s), ceiling $MAX"

# ATS sanity: is there a real text layer?
if command -v pdftotext >/dev/null; then
  CHARS="$(pdftotext "$PDF" - 2>/dev/null | tr -d '[:space:]' | wc -c)"
  if (( CHARS < 800 )); then
    echo "⚠️  text layer is only ${CHARS} chars — an ATS may not be able to read this."
    echo "    Check that contact details are real text, not icons or images."
  else
    echo "✓ text layer: ${CHARS} chars extractable"
  fi
fi
