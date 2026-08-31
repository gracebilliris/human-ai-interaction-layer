#!/usr/bin/env python3
"""
S6 Revision Similarity — Frozen preprocessing and cosine calculation.

Version: 1.0.0
Frozen:  2026-08-31 (pre-collection)

Compute cosine similarity between pre_revision_text and post_revision_text
using 5-character shingles (character n-grams, n=5) on lowercased,
whitespace-normalised input.

RULES:
  - Applies only when revision_required is true AND both pre and post are
    non-empty strings.
  - When revision_required is false OR unchanged, S6 must be recorded as
    similarity = 1.0 with s6_status = "no_revision" (post equals pre by
    construction).
  - Empty pre or post text after normalisation => s6_status = "invalid_input",
    similarity = null, record excluded from S6 aggregates.
  - No stemming, no stop-word removal, no lemmatisation.
  - Cosine over term-frequency vectors of the shingles.

Any change to this file after data collection begins invalidates S6.
"""
from __future__ import annotations
import math
import re
import sys
from collections import Counter

VERSION = "1.0.0"
SHINGLE_N = 5
_WS = re.compile(r"\s+")


def normalise(text: str) -> str:
    if text is None:
        return ""
    return _WS.sub(" ", str(text).strip().lower())


def shingles(text: str, n: int = SHINGLE_N) -> Counter:
    t = normalise(text)
    if len(t) < n:
        return Counter([t]) if t else Counter()
    return Counter(t[i : i + n] for i in range(len(t) - n + 1))


def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[s] * b[s] for s in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def compute_s6(pre: str, post: str, revision_required: bool):
    if not revision_required:
        return {"similarity": 1.0, "s6_status": "no_revision", "version": VERSION}
    pre_n = normalise(pre)
    post_n = normalise(post)
    if not pre_n or not post_n:
        return {"similarity": None, "s6_status": "invalid_input", "version": VERSION}
    if pre_n == post_n:
        return {"similarity": 1.0, "s6_status": "unchanged_but_flagged", "version": VERSION}
    sim = cosine(shingles(pre_n), shingles(post_n))
    return {"similarity": round(sim, 6), "s6_status": "ok", "version": VERSION}


if __name__ == "__main__":  # smoke test
    demo = compute_s6("The address field is exposed to the shipper.",
                      "The address field must be redacted before the shipper sees it.",
                      True)
    print(demo)
    print(compute_s6("same text", "same text", True))
    print(compute_s6("anything", "anything", False))
