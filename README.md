# Human–AI Interaction Layer (HAIL)

## Integrating Human Review into Agentic Software Engineering: A Traceability Study of the Human–AI Interaction Layer

This repository contains the sanitised evidence, protocols, schemas, analysis
scripts, and figure sources supporting the Human–AI Interaction Layer (HAIL)
traceability study submitted to ACM Transactions on Software Engineering and
Methodology. Participant and reviewer identities, institutional references,
credentials, private infrastructure details, and confidential metadata are
excluded from the research files.

## Purpose and scope

The paper develops the Human–AI Interaction Layer (HAIL) and a five-stage
traceability assessment with nine diagnostic checks (S1–S9). HAIL integrates a
human review checkpoint into an agentic software engineering pipeline and
returns the connected review action. The traceability assessment defines the
evidence a later observer needs to follow that action through Intent, Review,
Revision, Concordance, and Record.

The repository provides the materials needed to:

1. Inspect the diagnostic-check operational definitions and evidence-status
   rules.
2. Verify the three evidence streams reported in the paper: retrospective
   checkpoint operation, synthetic-record instrumentation, and the
   review study.
3. Reproduce the canonical analysis computations for the review study and
   walkthrough from the released data.
4. Inspect the figure generation sources for all four manuscript figures.
5. Understand the prospective evidence protocol under which future cohorts
   must be collected.

## Relation to paper claims

The paper reports three separately interpreted evidence streams. This
repository preserves those boundaries.

| Evidence stream | Paper role | Repository location |
|---|---|---|
| Six retrospective executions | Checkpoint operation and missing-trace diagnosis | `data/retrospective/` |
| 100 automated synthetic records | Bounded instrumentation observations | `data/synthetic-v3/` |
| 20-review study (10 shared cases, two reviewers) | Bounded human-submitted diagnostic-check evidence | `data/tier3-review-study/` |
| 20-case author-operated walkthrough | Supplementary field-retention and recovery observations | `data/tier2-walkthrough/` |

**The streams must not be pooled.** Synthetic records support instrumentation
observations only, not human-behaviour claims. The six retrospective executions
support checkpoint operation findings, not diagnostic-check values. The review
study supports bounded human-submitted evidence under disclosed departures
from the broader frozen analysis design. The walkthrough is supplementary
audit history.

## Directory map

```
human-ai-interaction-layer/
├── README.md                    This file
├── MANIFEST.json                Machine-readable artefact manifest
├── SANITISATION.md              Anonymisation and sanitisation record
├── PROVENANCE.md                Licence, provenance, and integrity notes
├── LICENSE                      MIT License
├── .gitignore                   Git ignore rules
│
├── schemas/                     JSON schemas for evidence records
│   ├── raw_run.schema.json      Raw execution record schema
│   ├── ground_truth.schema.json Ground truth record schema
│   └── analysis_output.schema.json  Analysis output schema
│
├── protocols/
│   ├── prospective_protocol.md  Frozen prospective cohort protocol
│   └── evidence_status_rules.md Operational definitions of Available,
│                                Partial, Unavailable, Not applicable
│
├── scripts/
│   ├── analyse_tier3_canonical.py   Canonical Tier 3 analysis
│   ├── analyse_tier2_canonical.py   Canonical Tier 2 analysis
│   ├── verify_hashes.sh            Integrity hash verification
│   └── frozen_analysis/            Frozen S6 computation module
│       ├── __init__.py
│       └── s6_preproc.py           5-shingle cosine similarity (v1.0.0)
│
├── figures/
│   ├── make_review_chain_traceability.py
│   ├── make_capra_hail_architectural_view.py
│   ├── make_hail_review_checkpoint.py
│   ├── make_hail_traceability_boundary.py
│   └── *.png                    Generated figure images (4 figures)
│
├── data/
│   ├── retrospective/
│   │   ├── SCOPE.md             What is and is not included
│   │   ├── hail_evaluation_records.jsonl
│   │   ├── feedback_records.jsonl
│   │   └── analysis_output/
│   │       ├── corpus_join_report.json
│   │       └── hail_summary.json
│   │
│   ├── synthetic-v3/
│   │   ├── SCOPE.md
│   │   ├── AUDIT_SUMMARY.md
│   │   └── COHORT_PROTOCOL_FROZEN.md
│   │
│   ├── tier3-review-study/
│   │   ├── SCOPE.md
│   │   ├── TIER3_CANONICAL_RESULTS.json
│   │   ├── cases_tier3.json
│   │   ├── sprint_dispatch_log.jsonl
│   │   ├── raw_runtime/
│   │   │   ├── tier3_present.jsonl
│   │   │   ├── tier3_page1.jsonl
│   │   │   ├── tier3_page2.jsonl
│   │   │   ├── tier3_interaction.jsonl
│   │   │   ├── tier3_mongo_records.jsonl
│   │   │   └── tier3_execution_audit.json
│   │   └── s2_coding/
│   │       ├── rev_a_codes.csv
│   │       └── rev_b_codes.csv
│   │
│   └── tier2-walkthrough/
│       ├── SCOPE.md
│       ├── TIER2_CANONICAL_RESULTS.json
│       └── tier2_enriched_records.jsonl
│
└── INTEGRITY.sha256             SHA-256 hashes for all released files
```

## Prerequisites

- Python 3.9+ (standard library only; no third-party packages required
  for analysis scripts)
- `matplotlib` 3.7+ (for figure generation only)
- No database, cloud service, or credentials required for verification

## Setup

```bash
git clone https://github.com/gracebilliris/human-ai-interaction-layer.git
cd human-ai-interaction-layer/
python3 -m pip install "matplotlib>=3.7"
```

The analysis scripts use only the Python standard library. Installing
`matplotlib` is necessary only when regenerating the figures.

## Reproduction and verification steps

Run the following commands from the repository root after completing the setup
steps above.

### 1. Verify integrity

```bash
bash scripts/verify_hashes.sh
```

This checks all released files against `INTEGRITY.sha256`.

### 2. Reproduce Tier 3 canonical results

```bash
python3 scripts/analyse_tier3_canonical.py
```

Reads the sanitised Tier 3 runtime evidence from `data/tier3-review-study/`
and recomputes S1–S9 statuses. The script overwrites
`data/tier3-review-study/TIER3_CANONICAL_RESULTS.json`; the output should
match the committed version.

### 3. Reproduce Tier 2 canonical results

```bash
python3 scripts/analyse_tier2_canonical.py
```

Reads the sanitised Tier 2 enriched records from `data/tier2-walkthrough/`
and recomputes S1–S9 statuses. The script overwrites
`data/tier2-walkthrough/TIER2_CANONICAL_RESULTS.json`; the output should
match the committed version.

### 4. Regenerate figures

```bash
python3 figures/make_review_chain_traceability.py
python3 figures/make_capra_hail_architectural_view.py
python3 figures/make_hail_review_checkpoint.py
python3 figures/make_hail_traceability_boundary.py
```

Each script generates its PNG in `figures/` at the paper's column width.

## Expected outputs

| Step | Expected result |
|---|---|
| Hash verification | All listed files pass SHA-256 check |
| Tier 3 analysis | S1 Available, S2 Partial, S3 Available, S4 Available, S5 Available, S6 Available, S7 Available, S8 Not applicable, S9 Unavailable |
| Tier 2 analysis | S1 Available, S2 Partial, S3 Unavailable, S4 Available, S5 Unavailable, S6 Partial, S7 Available, S8 Not applicable, S9 Unavailable |
| Figure generation | Four PNG files matching the manuscript figures |

## Evidence-stream boundaries

- **Retrospective (6 executions):** All nine diagnostic checks are Unavailable
  for this cohort. The records support checkpoint-operation and missing-trace
  findings only.
- **Synthetic (100 records):** Every record carries `synthetic: true`,
  `human_participation: false`, and `generation_method: automated`. S5 and S6
  outputs conflict with their governing definitions and are not accepted as
  protocol-conformant results. No human-behaviour claim is supported.
- **Review study (20 reviews):** S9 is Unavailable because all 20 MongoDB
  inserts produced documents containing the review action and identifiers,
  but a stale Tier 2 node reference terminated the subsequent final-record
  step; the frozen unrecovered-error rule excludes these executions. S2 is
  Partial because each rationale received one reciprocal cross-code rather
  than overlapping independent scores. S8 is Not applicable because no
  verified divergences exist. The interaction webhook was not exposed to
  reviewers.
- **Walkthrough (20 cases):** An author-operated instrumentation and recovery
  exercise. Does not constitute fresh reviewer-behaviour evidence. The
  13.45-minute submission span, single designer-participant, and post-hoc
  recovery provenance are disclosed.

## Known limitations

1. **Raw retrospective payloads are unavailable.** The six-execution cohort is
   report-defined; raw form payloads, the selection query, and the observation
   window are not retained.
2. **Excluded 30 August harness.** The `prospective_cohort_2026-08-30` package
   is excluded because all executions ended in error, the S9 computation does
   not verify persistence, and the files retain identifying metadata.
3. **Atlas backup excluded.** The `atlas_backup/` directory contains
   absolute local paths and unsanitised provenance metadata.
4. **S9 was not demonstrated.** All 20 MongoDB inserts produced documents
   containing the review action and identifiers, but a stale Tier 2 node
   reference terminated the subsequent final-record step. Missing evidence
   is never zero.
5. **No archival DOI.** This GitHub repository provides the current versioned
   release, but it has not yet been deposited in a DOI-minting archive.
6. **Synthetic enriched records excluded.** Safe by content but the parent
   directory contains workflow exports with local filesystem paths.

## Sanitisation statement

The research files in this repository have been sanitised to remove:

- Author email addresses and institutional affiliations from study records
- Institutional ethics reference identifiers
- Reviewer names, session-derived handles, and identifying metadata
- Local filesystem paths, home directories, and machine identifiers
- Private URLs, tokens, and cloud-service connection strings
- Related-submission details that belong in confidential editor disclosure
- Historical form labels that could expose provenance
- MongoDB connection details and infrastructure identifiers

Where analytically necessary identifiers were present, they have been replaced
with stable pseudonyms (REV-A, REV-B for reviewers; PARTICIPANT-01 for the
walkthrough participant; execution IDs are retained because they are
operationally necessary and not individually identifying).

The `reviewer_from_session` literal values in page-1, page-2, and MongoDB
records have been resolved to the correct pseudonyms (REV-A, REV-B) using
the dispatch log mapping.

The complete sanitisation record is in `SANITISATION.md`.
Repository ownership and the copyright notice identify the project maintainer;
they are intentionally public and are separate from the sanitised study data.
