# HAIL artefact

This anonymous package contains the minimum evidence and analysis code needed
to inspect the three evidence streams reported in the HAIL paper and reproduce
the 20-review study results. It contains no author names, affiliations,
reviewer identities, ethics identifiers, credentials, or private
infrastructure details.

## Contents

| Evidence stream | Purpose | Location |
|---|---|---|
| Six retrospective executions | Checkpoint-operation and missing-trace diagnosis | `data/retrospective/` |
| 100 synthetic records | Bounded instrumentation observations | `data/synthetic-instrumentation/` |
| 20 reviews of 10 shared scenarios by two reviewers | Reproducible S1-S9 analysis | `data/review-study/` |

The streams are interpreted separately. Synthetic records do not support
human-behaviour claims, retrospective records do not establish diagnostic-check
values, and the review study is bounded by the disclosed workflow and coding
limitations.

The package also includes:

- `protocols/`: diagnostic-check definitions and the prospective protocol;
- `scripts/analyse_review_study.py`: the canonical review-study analysis;
- `scripts/frozen_analysis/s6_preproc.py`: the frozen S6 computation;
- `MANIFEST.json`: claim-to-evidence mapping;
- `INTEGRITY.sha256` and `scripts/verify_hashes.sh`: integrity verification.

## Requirements

- Python 3.9 or later
- Bash and `shasum`

No database, cloud service, credentials, or third-party Python package is
required.

## Reproduce the results

Run from the package root:

```bash
bash scripts/verify_hashes.sh
python3 scripts/analyse_review_study.py
```

The first command must report that all files pass. The second rewrites
`data/review-study/REVIEW_STUDY_RESULTS.json` and must report:

| Check | Expected status |
|---|---|
| S1 | Available |
| S2 | Partial |
| S3 | Available |
| S4 | Available |
| S5 | Available |
| S6 | Available |
| S7 | Available |
| S8 | Not applicable |
| S9 | Unavailable |

S9 remains Unavailable because all 20 MongoDB inserts produced documents
containing the review action and identifiers, but a stale upstream node reference
terminated the subsequent final-record step. The frozen unrecovered-error rule
therefore excludes those executions. S2 is Partial because each rationale
received one reciprocal cross-code rather than two separately assigned scores.

## Evidence boundaries

- The review study used the same 10 scenarios in the same order for both reviewers.
- The interaction webhook was not exposed to reviewers.
- Required acknowledgements establish form completion, not attention.
- Queueing dominates the available timing measure.
- Reviewer codes are pseudonyms; reviewer background was not collected.
- The legacy runtime value
  `evidence_class="prospective_independent_reviewers"` is retained as source
  metadata and does not establish reviewer independence.

See `data/*/SCOPE.md`, `protocols/evidence_status_rules.md`, and
`MANIFEST.json` for the complete claim boundaries.
