# Provenance and integrity notes

## Provenance

This artefact package accompanies a manuscript submitted for anonymous review.
The evidence was collected and analysed by the authors during the development
and evaluation of the Human–AI Interaction Layer (HAIL) within an agentic
software engineering prototype.

All human-submitted evidence was collected under institutional ethics approval.
Participant consent was recorded. The approval reference and consent records are
held by the authors and will be provided to the editor on request; they are not
included in this anonymous package.

## Licence

The code and documentation in this package are released under the MIT License.
See `LICENSE`.

## Integrity

All released files are listed with their SHA-256 hashes in `INTEGRITY.sha256`.
To verify:

```bash
bash scripts/verify_hashes.sh
```

The hash file itself is the integrity anchor. If any file has been modified
since packaging, the verification script will report the discrepancy.

## Archival status

This package has **not** been deposited in a persistent repository and does
**not** have an archival DOI. The authors intend to release a sanitised,
versioned archive with the final publication. This pre-release version
accompanies the anonymous manuscript for reviewer inspection only.

## Data dictionary

### Evidence-status categories

| Status | Definition |
|---|---|
| Available | Every required record, field, identifier, population, window, and query is present; the diagnostic-check result can be determined |
| Partial | Cohort evidence supports part of the check, but an indispensable record or connection is absent |
| Unavailable | The required construct, population, record, or connection cannot be established |
| Not applicable | Complete evidence establishes that the eligible population is empty |

An observed zero is a possible diagnostic-check result only when evidence is
Available. It is not an evidence-status category.

### Diagnostic checks (S1–S9)

| Check | Name | Review stage |
|---|---|---|
| S1 | Intent completeness | Intent |
| S2 | Intent specificity | Intent |
| S3 | Review latency | Review |
| S4 | Review acknowledgement coverage | Review |
| S5 | Interaction depth | Review |
| S6 | Revision-text similarity | Revision |
| S7 | Action divergence | Concordance |
| S8 | Override rationale coverage | Concordance |
| S9 | Decision recording | Record |

### Key field definitions

| Field | Description |
|---|---|
| `review_id` | Unique identifier linking a review through all five stages |
| `execution_id` | n8n workflow execution identifier |
| `evaluation_id` | Identifier in the evaluation results corpus |
| `revision_id` | Identifier in the feedback/revision results corpus |
| `synthetic` | Boolean; true for automated synthetic records |
| `human_participation` | Boolean; false for synthetic records |
| `generation_method` | `automated` for synthetic; `human_submitted` for review-study records |
| `reviewer_type` | `simulated_human` for synthetic; pseudonymised for human participants |
| `evidence_class` | Classification of the evidence stream (e.g., `pipeline_engineering_stress_test`) |

## Citation

No citation metadata is provided because this is an anonymous pre-release
package. Citation information will be added after the anonymous review
concludes and the authors' identities are disclosed.
