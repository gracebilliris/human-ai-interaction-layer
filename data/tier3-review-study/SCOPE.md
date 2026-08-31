# Tier 3 review-study evidence scope

## What is included

- `TIER3_CANONICAL_RESULTS.json` — Canonical analysis results governing all
  manuscript claims for the review study.
- `cases_tier3.json` — Case definitions for the 10 shared review cases.
- `sprint_dispatch_log.jsonl` — Sanitised dispatch log mapping review_id to
  reviewer pseudonym, case, domain, and presentation timestamp. Form URLs
  removed.
- `raw_runtime/tier3_present.jsonl` — 20 presentation events with case
  fixtures, pre-revision text, and surfaced items. Form URLs removed;
  `reviewer_from_session` resolved to pseudonyms.
- `raw_runtime/tier3_page1.jsonl` — 20 page-1 submission events with
  rationales. Form URLs removed; reviewer codes resolved.
- `raw_runtime/tier3_page2.jsonl` — 20 page-2 submission events with actions,
  revision text, and similarity inputs. Form URLs removed; reviewer codes
  resolved.
- `raw_runtime/tier3_interaction.jsonl` — Interaction events (empty file;
  no reviewer interactions occurred).
- `raw_runtime/tier3_mongo_records.jsonl` — 20 MongoDB decision-store
  candidates with write timestamps and actions. Connection details removed;
  reviewer codes resolved.
- `raw_runtime/tier3_execution_audit.json` — Execution audit with
  acknowledgement joins, error statuses, and interaction counts.
- `s2_coding/rev_a_codes.csv` — REV-A cross-coding of REV-B rationales.
- `s2_coding/rev_b_codes.csv` — REV-B cross-coding of REV-A rationales.

## What is excluded

- **Raw runtime data** (n8n execution database, MongoDB snapshots) — Contains
  session-derived reviewer handles and infrastructure metadata. Sanitised
  extracts are included above.
- **Reviewer packet files** — Instructions sent to reviewers; may identify
  study logistics.
- **Sprint runbook** — May reference reviewer scheduling details.

## Evidence boundaries

The review study contains 20 reviews of 10 shared cases by two reviewers,
as specified in the operational runbook and completed as designed.

| Check | Status | Key boundary |
|---|---|---|
| S1 | Available | 20/20 non-blank rationales; mean 329.5 characters |
| S2 | Partial | One reciprocal cross-code per rationale; all 20 scored 2; no overlapping independent scores or resolved score |
| S3 | Available | Median 2,098.5 seconds overall; reviewer medians 1,933.2 and 2,289.4 seconds; pipeline-to-submission time dominated by batch queueing |
| S4 | Available | 76/76 required acknowledgement fields joined to surfaced items; instrument-enforced completion, not attention |
| S5 | Available | Mean and maximum 0 cycles on an interaction path not exposed to reviewers |
| S6 | Available | 6/20 submissions contained eligible revision text, mean cosine similarity 0.280; 14 submitted no revision text |
| S7 | Available | 0/20 divergent actions |
| S8 | Not applicable | No natural divergence |
| S9 | Unavailable | All 20 MongoDB inserts produced documents containing review action and identifiers; a stale Tier 2 node reference terminated the subsequent final-record step; frozen unrecovered-error rule excludes these executions |

### Departures from the frozen analysis design

The operational runbook specified and completed 20 reviews of 10 shared cases
by two reviewers. A separate frozen analysis protocol documented the broader
target of at least 30 reviews by at least three reviewers with randomised
assignment and overlapping S2 coding. The following items record where the
completed study departs from that broader design; broader coverage is future
work.

- The frozen analysis protocol targeted at least 30 reviews by at least three
  reviewers; the operational runbook completed 20 reviews by two reviewers.
- The frozen analysis protocol specified randomised assignment per reviewer;
  both reviewers received the same cases in the same fixed order.
- The frozen S2 procedure required overlapping independent codes with
  pre-resolution agreement; each rationale received one reciprocal cross-code.
- Session events for the frozen short-review rule were not emitted; the
  page-1 to page-2 proxy flags 14/20 records below 15 seconds but excludes
  none.
- All presentations were emitted within 2.881 seconds.
- All 20 MongoDB inserts produced documents containing the review action and
  identifiers; the presentation timestamp, rationale, and AI recommendation
  were not propagated to those documents.
- A stale Tier 2 node reference terminated the final-record step in every
  page-2 execution, producing unrecovered errors after the MongoDB insert.
- The S4 form made all four acknowledgement fields mandatory; four three-item
  records produced surplus fourth values that were discarded during the join.
- The S5 webhook was not exposed in reviewer-facing materials.
- A consistent `-04:00` timezone offset is used throughout, converting to
  31 August 2026 UTC.

### Sanitisation applied

- Form URLs (`page1_url`, `page2_url`, `page1_form_url`, `page2_form_url`)
  removed from all records.
- `reviewer_from_session` literal values in page-1, page-2, and MongoDB
  records resolved to correct pseudonyms (REV-A, REV-B) from dispatch log.
- MongoDB `decision_store` connection details replaced with type-only stub.
- See `SANITISATION.md` for the complete record.
