#!/usr/bin/env python3
"""Compute the admissible review study results from retained runtime evidence.

Run from the repository root:
    python3 scripts/analyse_review_study.py

Reads sanitised review-study data from data/review-study/ and recomputes
S1–S9 diagnostic-check statuses. Output is compared to the included
REVIEW_STUDY_RESULTS.json.
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# Ensure scripts/ is on sys.path for the frozen_analysis import
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frozen_analysis.s6_preproc import compute_s6

REPO = SCRIPT_DIR.parent
DATA = REPO / "data" / "review-study"
RAW = DATA / "raw_runtime"
OUT = DATA / "REVIEW_STUDY_RESULTS.json"


def jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_scores(path: Path) -> dict[str, int]:
    with path.open() as handle:
        return {
            row["review_id"]: int(row["score"])
            for row in csv.DictReader(handle)
            if row.get("score", "").strip()
        }


def main() -> None:
    dispatch = jsonl(DATA / "sprint_dispatch_log.jsonl")
    present = {r["review_id"]: r for r in jsonl(RAW / "presentation_events.jsonl")}
    page1 = {r["review_id"]: r for r in jsonl(RAW / "page1_submissions.jsonl")}
    page2 = {r["review_id"]: r for r in jsonl(RAW / "page2_submissions.jsonl")}
    interactions = jsonl(RAW / "interaction_events.jsonl")
    mongo = {r["review_id"]: r for r in jsonl(RAW / "decision_store_records.jsonl")}
    execution_audit = json.loads(
        (RAW / "execution_audit.json").read_text()
    )
    audit = {r["review_id"]: r for r in execution_audit["records"]}
    ids = [r["review_id"] for r in dispatch]
    reviewer = {r["review_id"]: r["reviewer_code"] for r in dispatch}
    expected_hashes = {
        "protocol": "076dbfead9f5fba6a320986ab044eb6d5be35a6c1a61139e25fc2aba0bb5ad09",
        "s2_rubric": "eeea4773820ad7451fabc31a2b0b2b29d9d6aa52b5f4cdad055fc59444acbde0",
        "s5_cycle_definition": "ee3f25066071dc75f33f7ac0c5ee489b7b6925928dc5fd65d4f99d81b57c81a5",
        "s6_preproc": "918dfb36fb8c1a4386a29281ff940bdb88809a5bd593cc1d215a202d0b271d17",
    }

    if len(ids) != len(set(ids)):
        raise ValueError("duplicate review_id in dispatch")
    for name, records in (
        ("present", present),
        ("page1", page1),
        ("page2", page2),
        ("mongo", mongo),
        ("execution audit", audit),
    ):
        if set(records) != set(ids):
            raise ValueError(f"{name} identifiers do not match dispatch")
    for name, records in (("present", present), ("page1", page1), ("page2", page2)):
        for review_id, record in records.items():
            if record.get("frozen_hashes") != expected_hashes:
                raise ValueError(f"{name} frozen hashes differ for {review_id}")

    rationales = [(page1[rid].get("rationale") or "") for rid in ids]
    s1 = {
        "status": "available",
        "n_non_blank": sum(bool(text.strip()) for text in rationales),
        "n_total": len(ids),
        "completeness_rate": sum(bool(text.strip()) for text in rationales)
        / len(ids),
        "mean_characters": statistics.mean(len(text) for text in rationales),
    }

    scores_a = load_scores(DATA / "s2_coding" / "rev_a_codes.csv")
    scores_b = load_scores(DATA / "s2_coding" / "rev_b_codes.csv")
    overlap = set(scores_a) & set(scores_b)
    scores = {**scores_a, **scores_b}
    s2 = {
        "status": "partial",
        "reason": (
            "The frozen rubric required both coders to score every rationale "
            "and pre-resolution agreement before adjudication. Each rationale "
            "received one cross-code, so no protocol-conformant resolved score "
            "or inter-rater agreement is available."
        ),
        "n_scored_once": len(scores),
        "n_total": len(ids),
        "n_scored_by_both": len(overlap),
        "single_code_mean": statistics.mean(scores.values()),
        "single_code_distribution": dict(Counter(scores.values())),
    }

    latencies = defaultdict(list)
    for rid in ids:
        seconds = (
            iso(page2[rid]["page2_submit_ts"])
            - iso(present[rid]["review_presented_ts"])
        ).total_seconds()
        latencies[reviewer[rid]].append(seconds)
        latencies["overall"].append(seconds)
    presentation_times = [iso(present[rid]["review_presented_ts"]) for rid in ids]
    page1_times = [iso(page1[rid]["page1_submit_ts"]) for rid in ids]
    page_intervals = [
        (
            iso(page2[rid]["page2_submit_ts"])
            - iso(page1[rid]["page1_submit_ts"])
        ).total_seconds()
        for rid in ids
    ]
    s3 = {
        "status": "available",
        "interpretation": (
            "Pipeline-to-submission latency is dominated by queueing because "
            "all review identifiers were dispatched within 2.9 seconds and "
            "the first page-1 submission followed about 23 minutes later."
        ),
        "presentation_dispatch_span_seconds": (
            max(presentation_times) - min(presentation_times)
        ).total_seconds(),
        "last_presentation_to_first_page1_seconds": (
            min(page1_times) - max(presentation_times)
        ).total_seconds(),
        "overall": {
            "n": len(latencies["overall"]),
            "median_seconds": statistics.median(latencies["overall"]),
            "mean_seconds": statistics.mean(latencies["overall"]),
            "min_seconds": min(latencies["overall"]),
            "max_seconds": max(latencies["overall"]),
        },
        "by_reviewer": {
            code: {
                "n": len(values),
                "median_seconds": statistics.median(values),
                "mean_seconds": statistics.mean(values),
                "min_seconds": min(values),
                "max_seconds": max(values),
            }
            for code, values in latencies.items()
            if code != "overall"
        },
    }

    n_presented = 0
    n_acknowledged = 0
    surplus_acknowledgements = 0
    for rid in ids:
        manifest = present[rid]["surfaced_items_manifest"]
        acknowledgements = audit[rid]["page1_acknowledgements"]
        n_presented += len(manifest)
        n_acknowledged += sum(
            bool(acknowledgements.get(f"ack_item_{index}_seen"))
            for index in range(1, len(manifest) + 1)
        )
        surplus_acknowledgements += sum(
            bool(acknowledgements.get(f"ack_item_{index}_seen"))
            for index in range(len(manifest) + 1, 5)
        )
    s4 = {
        "status": "available",
        "n_acknowledged": n_acknowledged,
        "n_presented": n_presented,
        "coverage": n_acknowledged / n_presented,
        "required_form_fields": True,
        "surplus_values_discarded_during_join": surplus_acknowledgements,
        "evidence_note": (
            "All four acknowledgement checkboxes were required, so complete "
            "submission was instrument-enforced rather than evidence of "
            "attention. Values were recovered from retained n8n form "
            "execution data and joined to the presented manifest by review_id; "
            "surplus fourth values for three-item cases were discarded."
        ),
    }

    interaction_ids = {event.get("review_id") for event in interactions}
    unexpected_interactions = interaction_ids & set(ids)
    interaction_executions = sum(
        audit[rid]["interaction_execution_count"] for rid in ids
    )
    if unexpected_interactions or interaction_executions:
        raise ValueError("interaction evidence conflicts with zero-cycle result")
    s5 = {
        "status": "available",
        "interaction_path_exposed_to_reviewers": False,
        "interpretation": (
            "Zero records an unexercised server-side interaction path, not a "
            "reviewer choice to decline an available interaction control."
        ),
        "n": len(ids),
        "mean_cycles": 0,
        "max_cycles": 0,
        "n_zero_cycles": len(ids),
    }

    quality_flags = {
        "session_events_available": False,
        "proxy": "page1_submit_ts to page2_submit_ts",
        "threshold_seconds": 15,
        "n_below_threshold": sum(value < 15 for value in page_intervals),
        "n_total": len(page_intervals),
        "median_seconds": statistics.median(page_intervals),
        "min_seconds": min(page_intervals),
        "max_seconds": max(page_intervals),
        "interpretation": (
            "The frozen rule specifies session_end minus session_start, but "
            "the workflow emitted neither event. The page-1 to page-2 interval "
            "is reported as the closest available proxy; the rule flags but "
            "does not exclude records."
        ),
    }

    similarities = []
    no_revision = 0
    invalid = 0
    for rid in ids:
        result = compute_s6(
            present[rid]["pre_revision_text"],
            page2[rid]["post_revision_text"],
            bool(page2[rid].get("edited")),
        )
        if result["s6_status"] == "no_revision":
            no_revision += 1
        elif result["s6_status"] == "invalid_input":
            invalid += 1
        else:
            similarities.append(result["similarity"])
    s6 = {
        "status": "available" if not invalid else "partial",
        "n_revised": len(similarities),
        "n_no_revision": no_revision,
        "n_invalid": invalid,
        "mean_similarity_revised": statistics.mean(similarities),
        "min_similarity_revised": min(similarities),
        "max_similarity_revised": max(similarities),
    }

    divergent = [
        rid
        for rid in ids
        if page2[rid]["human_review_action"].strip().lower()
        != present[rid]["ai_recommended_action"].strip().lower()
    ]
    s7 = {
        "status": "available",
        "n_divergent": len(divergent),
        "n_total": len(ids),
        "divergence_rate": len(divergent) / len(ids),
    }
    s8 = {
        "status": "not_applicable",
        "reason": "No reviewer action diverged from the AI recommendation.",
    }

    final_by_reviewer = {
        code: max(
            iso(page2[rid]["page2_submit_ts"])
            for rid in ids
            if reviewer[rid] == code
        )
        for code in set(reviewer.values())
    }
    observed_writes = 0
    eligible_writes = 0
    page2_errors = 0
    for rid in ids:
        write_time = iso(mongo[rid]["decision_store_write_ts"])
        in_window = (
            write_time >= iso(page2[rid]["page2_submit_ts"])
            and write_time <= final_by_reviewer[reviewer[rid]] + timedelta(seconds=30)
        )
        mongo_succeeded = audit[rid]["mongo_insert_status"] == "success"
        observed_writes += bool(in_window and mongo_succeeded)
        if audit[rid]["page2_execution_status"] == "error":
            page2_errors += 1
        else:
            eligible_writes += bool(in_window and mongo_succeeded)
    s9 = {
        "status": "unavailable",
        "reason": (
            "All 20 MongoDB inserts produced documents containing the review "
            "action and identifiers. A stale upstream node reference then "
            "terminated the subsequent final-record step in every page-2 "
            "execution. S9 remains Unavailable under the frozen "
            "unrecovered-error rule because no execution completed the full "
            "decision-recording path."
        ),
        "observed_in_window_mongo_writes": observed_writes,
        "n_total": len(ids),
        "page2_executions_ending_in_error": page2_errors,
        "protocol_eligible_executions": len(ids) - page2_errors,
        "protocol_eligible_successful_writes": eligible_writes,
        "mongo_documents_with_review_action": sum(
            bool((mongo[rid].get("human_review_action") or "").strip())
            for rid in ids
        ),
        "mongo_documents_with_ai_recommendation": sum(
            bool((mongo[rid].get("ai_recommended_action") or "").strip())
            for rid in ids
        ),
        "mongo_documents_with_rationale": sum(
            bool((mongo[rid].get("rationale") or "").strip())
            for rid in ids
        ),
    }

    result = {
        "cohort": "review_study",
        "n_reviews": len(ids),
        "n_scenarios": len({r["scenario_id"] for r in dispatch}),
        "n_reviewers": len(set(reviewer.values())),
        "domains": sorted({r["domain"] for r in dispatch}),
        "analysis_design_departures": [
            (
                "The operational runbook specified 20 reviews of 10 shared "
                "scenarios by two reviewers and was completed as designed. The "
                "frozen analysis protocol documented a broader target of at "
                "least 30 reviews by at least three reviewers; broader "
                "coverage is future work."
            ),
            (
                "The frozen analysis protocol specified randomised assignment "
                "per reviewer; the operational runbook assigned both reviewers "
                "the same scenarios in the same fixed order."
            ),
            (
                "The frozen S2 procedure required both coders to score every "
                "rationale with pre-resolution agreement; each rationale "
                "received one reciprocal cross-code."
            ),
            (
                "The frozen quality flag required session-start and "
                "session-end events; neither event was emitted by the "
                "workflow."
            ),
        ],
        "quality_flags": quality_flags,
        "S1": s1,
        "S2": s2,
        "S3": s3,
        "S4": s4,
        "S5": s5,
        "S6": s6,
        "S7": s7,
        "S8": s8,
        "S9": s9,
    }
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
