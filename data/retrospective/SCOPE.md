# Retrospective evidence scope

## What is included

- `hail_evaluation_records.jsonl` — 110 Atlas evaluation documents with 58
  unique evaluation identifiers. This is a whole-collection contextual snapshot,
  not the six-execution HAIL cohort.
- `feedback_records.jsonl` — 74 Atlas feedback documents with 54 unique revision
  identifiers. This is a whole-collection contextual snapshot.
- `analysis_output/corpus_join_report.json` — Heuristic identifier-string and
  embedded-document-ID matches. This is an audit artefact, not a documented
  stable join and not a diagnostic-check result.
- `analysis_output/hail_summary.json` — Legacy derived summary. Its 13/97
  labels map `requires_human_review` to approve/reject and must not be
  interpreted as human decisions.

## What is excluded

- **Raw form payloads** for the six HAIL executions — not retained.
- **Selection query and observation window** — not retained.
- **Raw execution chains** — not retained.
- **73-record offline artefact** (`hil_review_records.jsonl`) — excluded because
  the n8n workflow did not activate and records were written outside the running
  pipeline.
- **Exploratory aggregations** (`corpus_remeasurement.json`,
  `hil_signal_remeasurement.json`) — proxy calculations that do not implement
  the predeclared diagnostic checks.

## Evidence boundaries

- All nine diagnostic checks are **Unavailable** for the six-execution cohort.
- The contextual corpus does not enlarge the execution cohort and does not
  support per-execution field, revision, or decision-record counts.
- No verified key connects either snapshot to the six HAIL executions.
- Two retained summaries conflict on the branch distribution (4 Approve /
  2 Reject versus 3 Approve / 3 Reject); no branch proportion is reported.
- The six documented executions comprise 12 form-page completions and six
  returned review actions.
