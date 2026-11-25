#!/usr/bin/env python3
"""Character- and word-level evaluation of ALTO XML transcriptions against a reference.

Usage:
    python scripts/evaluate_alto.py --reference data/ground_truth/test \
        --hypothesis data/transcription_v4/alto --pages 5068,5092,5101,5153

Metrics (per folio, plus a total):
  * strict CER : Levenshtein distance between characters, ignoring whitespace and
                 end-of-line hyphens, but respecting case, accents and punctuation.
  * lax CER    : additionally ignores case, accents and punctuation, i.e. it measures
                 whether the same letters are read, not how they are spelled.
  * exact words: share of reference words (lax form) found identically, in order, in the
                 hypothesis.
The total CER is weighted by the number of reference characters; "exact words" is the
mean over folios.

Needs: lxml, rapidfuzz.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from lxml import etree
from rapidfuzz.distance import Levenshtein


def alto_lines(path: Path) -> list[str]:
    """Text of every TextLine of an ALTO file, in document order (empty lines dropped)."""
    tree = etree.parse(str(path))
    lines = []
    for tl in tree.xpath('//*[local-name()="TextLine"]'):
        words = tl.xpath('./*[local-name()="String"]/@CONTENT')
        text = " ".join(words).strip()
        if text:
            lines.append(text)
    return lines


def join_hyphens(lines: list[str]) -> str:
    out = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line.endswith("-") and i + 1 < len(lines):
            out.append(line[:-1])
        else:
            out.append(line + " ")
    return "".join(out).strip()


def strict(s: str) -> str:
    s = unicodedata.normalize("NFC", s).replace("-", "")
    return re.sub(r"\s+", "", s)


def lax(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


def cer(ref: str, hyp: str) -> float:
    return Levenshtein.distance(ref, hyp) / max(1, len(ref))


def exact_words(ref_lines: list[str], hyp_lines: list[str]) -> float:
    ref = [w for w in (lax(w) for w in join_hyphens(ref_lines).split()) if w]
    hyp = [w for w in (lax(w) for w in join_hyphens(hyp_lines).split()) if w]
    if not ref:
        return 0.0
    blocks = SequenceMatcher(None, ref, hyp, autojunk=False).get_matching_blocks()
    return sum(b.size for b in blocks) / len(ref)


def evaluate(ref_lines: list[str], hyp_lines: list[str]) -> dict:
    ref_s, hyp_s = strict("".join(ref_lines)), strict("".join(hyp_lines))
    ref_l, hyp_l = lax("".join(ref_lines)), lax("".join(hyp_lines))
    return {"chars": len(ref_s), "cer_strict": cer(ref_s, hyp_s), "cer_lax": cer(ref_l, hyp_l),
            "exact_words": exact_words(ref_lines, hyp_lines)}


def folio_id(path: Path) -> str:
    m = re.search(r"(\d{4}[a-z]?)", path.stem)
    return m.group(1) if m else path.stem


def find(directory: Path, pid: str) -> Path | None:
    for p in sorted(directory.glob("*.xml")):
        if folio_id(p) == pid:
            return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reference", required=True, help="folder with reference ALTO files")
    ap.add_argument("--hypothesis", required=True, help="folder with ALTO files to evaluate")
    ap.add_argument("--pages", help="comma-separated folio ids (default: all in the reference folder)")
    a = ap.parse_args()
    ref_dir, hyp_dir = Path(a.reference), Path(a.hypothesis)
    ids = a.pages.split(",") if a.pages else sorted(folio_id(p) for p in ref_dir.glob("*.xml"))
    rows = []
    for pid in ids:
        r, h = find(ref_dir, pid), find(hyp_dir, pid)
        if r is None or h is None:
            print(f"skipping {pid}: missing in {'reference' if r is None else 'hypothesis'}", file=sys.stderr)
            continue
        rows.append((pid, evaluate(alto_lines(r), alto_lines(h))))
    if not rows:
        print("nothing to evaluate")
        return 1
    total_chars = sum(m["chars"] for _, m in rows)
    total = {"chars": total_chars,
             "cer_strict": sum(m["cer_strict"] * m["chars"] for _, m in rows) / total_chars,
             "cer_lax": sum(m["cer_lax"] * m["chars"] for _, m in rows) / total_chars,
             "exact_words": sum(m["exact_words"] for _, m in rows) / len(rows)}
    print("| Folio | Reference chars | CER strict | CER lax | Exact words |")
    print("|---|---|---|---|---|")
    for pid, m in rows + [("TOTAL", total)]:
        print(f"| {pid} | {m['chars']} | {m['cer_strict'] * 100:.1f} % | {m['cer_lax'] * 100:.1f} % "
              f"| {m['exact_words'] * 100:.1f} % |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
