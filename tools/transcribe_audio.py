#!/usr/bin/env python3
"""
transcribe_audio.py — local speech-to-text for skill 07 (audio interviews).

Runs Whisper on this machine. Recordings never leave it: no API, no upload, no third party.

Usage
-----
    python3 tools/transcribe_audio.py practice/*.opus --lang pt --out transcripts/
    python3 tools/transcribe_audio.py answer.m4a --lang pt --model small

Install
-------
    pip install faster-whisper
    sudo apt-get install -y ffmpeg

Models: tiny · base · small (default, good for technical speech) · medium · large-v3
On a 2-core CPU, `small` runs at roughly 4-6x realtime.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

# Verbal tics measured for the report. Extend per language.
TICS = {
    "pt": ["a gente", "etc", "então assim", "enfim", "tipo", "né", "basicamente",
           "na verdade", "ou seja", "assim,", "inclusive", "vamos lá"],
    "en": ["you know", "kind of", "sort of", "basically", "actually", "like,",
           "I mean", "etc", "right?", "so yeah"],
}
FIRST_PERSON = {"pt": (r"\beu\b", r"\ba gente\b"), "en": (r"\bI\b", r"\bwe\b")}


def analyse(text: str, duration_s: float, lang: str) -> dict:
    low = text.lower()
    words = len(text.split())
    wpm = words / (duration_s / 60) if duration_s else 0

    tic_counts = {t: len(re.findall(r"\b" + re.escape(t), low)) for t in TICS.get(lang, [])}
    tic_counts = {k: v for k, v in sorted(tic_counts.items(), key=lambda x: -x[1]) if v}

    singular_pat, plural_pat = FIRST_PERSON.get(lang, FIRST_PERSON["en"])
    flags = re.IGNORECASE if lang == "en" else 0
    singular = len(re.findall(singular_pat, text, flags))
    plural = len(re.findall(plural_pat, text, flags))

    first_sentence = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0][:200]

    return {
        "words": words,
        "wpm": wpm,
        "tics": tic_counts,
        "singular": singular,
        "plural": plural,
        "opening": first_sentence,
    }


def verdict(a: dict) -> list[str]:
    notes = []
    if a["wpm"] > 165:
        notes.append(f"⚠️ pace {a['wpm']:.0f} wpm — rushing. Target 120-150.")
    elif a["wpm"] < 105:
        notes.append(f"⚠️ pace {a['wpm']:.0f} wpm — dragging. Target 120-150.")
    else:
        notes.append(f"✓ pace {a['wpm']:.0f} wpm — comfortable.")

    if a["plural"] > a["singular"]:
        notes.append(
            f"🔴 ownership: {a['plural']} plural vs {a['singular']} singular. "
            "You are crediting the team for your own work."
        )
    elif a["singular"]:
        notes.append(f"✓ ownership: {a['singular']} singular vs {a['plural']} plural.")

    if a["tics"]:
        top = ", ".join(f"{k} ({v}x)" for k, v in list(a["tics"].items())[:4])
        notes.append(f"filler: {top}")

    weak = ("simple", "simples", "just ", "apenas ", "only ", "overkill", "canhão", "não sei se")
    if any(w in a["opening"].lower() for w in weak):
        notes.append("🔴 opening sentence undersells the story — rewrite it.")

    return notes


def main() -> int:
    ap = argparse.ArgumentParser(description="Local Whisper transcription + delivery analysis.")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--lang", default="pt", help="pt, en, es… (default: pt)")
    ap.add_argument("--model", default="small")
    ap.add_argument("--out", type=Path, default=Path("transcripts"))
    args = ap.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("error: pip install faster-whisper", file=sys.stderr)
        return 2

    args.out.mkdir(parents=True, exist_ok=True)
    report = args.out / "analysis.md"

    print(f"loading model '{args.model}' (first run downloads it)…")
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    with report.open("w", encoding="utf-8") as fh:
        fh.write(f"# Transcripts and delivery analysis\n\nLanguage: `{args.lang}` · "
                 f"model: `{args.model}`\n")

        for path in args.files:
            if not path.exists():
                print(f"  skip (not found): {path}", file=sys.stderr)
                continue

            t0 = time.time()
            segments, info = model.transcribe(
                str(path), language=args.lang, beam_size=5, vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=700),
            )
            text = " ".join(s.text.strip() for s in segments)
            a = analyse(text, info.duration, args.lang)

            fh.write(f"\n---\n\n## {path.name}\n\n")
            fh.write(f"**{int(info.duration // 60)}min{int(info.duration % 60):02d}s** · "
                     f"{a['words']} words · {a['wpm']:.0f} wpm\n\n")
            for note in verdict(a):
                fh.write(f"- {note}\n")
            fh.write(f"\n**Opening:** _{a['opening']}_\n\n### Transcript\n\n{text}\n")

            print(f"  ✓ {path.name}  ({time.time() - t0:.0f}s, {a['wpm']:.0f} wpm)")

    print(f"\nwritten to {report}")
    print("note: transcripts are gitignored — they stay on this machine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
