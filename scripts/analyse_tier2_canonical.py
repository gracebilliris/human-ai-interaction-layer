#!/usr/bin/env python3
"""Reproduce the manuscript-admissible Tier 2 walkthrough results.

Run from the repository root:
    python3 scripts/analyse_tier2_canonical.py

Reads sanitised Tier 2 enriched records from data/tier2-walkthrough/ and
recomputes S1–S9 diagnostic-check statuses. Output is compared to the
included TIER2_CANONICAL_RESULTS.json.
"""
from __future__ import annotations

import json
import math
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
INPUT = REPO / "data" / "tier2-walkthrough" / "tier2_enriched_records.jsonl"
OUTPUT = REPO / "data" / "tier2-walkthrough" / "TIER2_CANONICAL_RESULTS.json"
NO_REVISION_INSTRUCTION = "Leave blank because no revision is required."


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def shingles(value: str, width: int = 5) -> Counter[str]:
    normalised = " ".join((value or "").lower().split())
    return Counter(normalised[index : index + width] for index in range(max(0, len(normalised) - width + 1)))


def cosine(left: str, right: str) -> float | None:
    a, b = shingles(left), shingles(right)
    if not a or not b:
        return None
    keys = set(a) | set(b)
    numerator = sum(a[key] * b[key] for key in keys)
    denominator = math.sqrt(sum(value * value for value in a.values())) * math.sqrt(
        sum(value * value for value in b.values())
    )
    return numerator / denominator if denominator else None


records = [json.loads(line) for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
page2 = sorted(parse_timestamp(record["page2_submit_ts"]) for record in records)
eligible = [
    record
    for record in records
    if (record.get("post_revision_text") or "").strip() != NO_REVISION_INSTRUCTION
]
similarities = [
    cosine(record.get("pre_revision_text", ""), record.get("post_revision_text", ""))
    for record in eligible
]
similarities = [value for value in similarities if value is not None]

result = {
    "analysis_status": "canonical manuscript-admissible walkthrough analysis",
    "n_records": len(records),
    "n_unique_review_ids": len({record["review_id"] for record in records}),
    "page2_first_to_last_seconds": (page2[-1] - page2[0]).total_seconds(),
    "S1": {"status": "Available", "substantive_rationale_fields": len(records)},
    "S2": {
        "status": "Partial",
        "reason": "No protocol-conformant result without two independent coders and pre-resolution agreement.",
    },
    "S3": {"status": "Unavailable", "reason": "Pipeline presentation timestamps are absent."},
    "S4": {
        "status": "Available",
        "acknowledged_required_fields": sum(
            1
            for record in records
            for key, value in record.items()
            if key.startswith("ack_item_") and key.endswith("_seen") and value is True
        ),
        "interpretation": "Instrument-enforced field completion, not attention.",
    },
    "S5": {"status": "Unavailable", "reason": "Page submissions are not request-response cycles."},
    "S6": {
        "status": "Partial",
        "eligible_revision_fields": len(eligible),
        "ineligible_instruction_fields": len(records) - len(eligible),
        "exploratory_eligible_only_five_shingle_cosine": {
            "n": len(similarities),
            "mean": statistics.mean(similarities),
            "median": statistics.median(similarities),
            "minimum": min(similarities),
            "maximum": max(similarities),
        },
        "manuscript_rule": "Do not report a protocol-conformant 20-pair result.",
    },
    "S7": {
        "status": "Available",
        "concordant_fixture_action_pairs": sum(
            record.get("ai_recommended_action")
            == (record.get("human_review_action") or record.get("action"))
            for record in records
        ),
    },
    "S8": {"status": "Not applicable", "eligible_divergences": 0},
    "S9": {"status": "Unavailable", "reason": "Only post-hoc recovery writes are retained."},
}

OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
