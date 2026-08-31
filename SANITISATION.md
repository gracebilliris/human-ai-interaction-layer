# Sanitisation record

This document records every anonymisation and sanitisation transformation
applied to produce this public, sanitised artefact repository.

## Principles

1. **Remove identifying study metadata.** Author names and email addresses in
   study records, institutional affiliations, reviewer identities, ethics
   reference identifiers, and private infrastructure paths are removed or
   replaced. Repository ownership and the copyright notice remain public.
2. **Preserve analytical identifiers through pseudonyms.** Where an identifier
   is needed for reproducibility (e.g., to distinguish two reviewers), a
   stable pseudonym is used.
3. **Do not alter analytical content.** Numeric values, timestamps (except
   where uniquely identifying), diagnostic-check statuses, and field contents
   are preserved exactly.
4. **Document every transformation.** No silent removal or substitution.

## Transformations applied

### Tier 3 review-study data

| Category | Original content | Transformation | Rationale |
|---|---|---|---|
| Form URLs | `page1_url`, `page2_url`, `page1_form_url`, `page2_form_url` containing `localhost:5678` endpoints | Removed from all included records | Expose infrastructure configuration |
| Reviewer session handles | `reviewer_code: "reviewer_from_session"` literal in page-1, page-2, and MongoDB records | Resolved to correct pseudonyms (REV-A, REV-B) using dispatch log mapping | Literal value is a metadata defect; pseudonyms preserve analytical distinction |
| MongoDB connection details | `decision_store.database`, `decision_store.collection`, `decision_store.target` with docker-local addresses | Replaced with `{"type": "MongoDB", "note": "Connection details removed for anonymisation"}` | Connection strings expose infrastructure |

### Tier 2 walkthrough data

| Category | Original content | Transformation | Rationale |
|---|---|---|---|
| Ethics reference | `hrec_ref` (format: XX-YYYY-NNNN) in reviewer block | Removed; replaced with `ethics_note` stating approval is held | Institutional identifier |
| Participant identity | `reviewer_display_name`, `participant_id: "author_first_person_01"`, `reviewer_code: "AUTHOR-01"` | Replaced with `participant_id: "PARTICIPANT-01"`, `reviewer_code: "PARTICIPANT-01"` | Author identity |
| HREC metadata | `hrec_status`, `hrec_note` fields in reviewer block | Removed; replaced with generic ethics note | Institutional metadata |
| Recovery note paths | `/home/node/.n8n/hail_tier2_*.jsonl` in `recovery_note` | Replaced with `[internal-path]` | Filesystem path |
| Author name in notes | Author's given name in `recovery_note` text | Replaced with "the participant's" | Author identity |

### Global transformations

| Category | Original content | Transformation | Rationale |
|---|---|---|---|
| Author names | Author names and emails in governance records | Not copied; public-facing content derived instead | Governance records contain confidential metadata throughout |
| Institutional ethics ID | Ethics approval reference (format: XX-YYYY-NNNN) | Removed; stated as "institutional ethics approval is held" | Confidential governance record |
| Reviewer identities | Reviewer names and session-derived handles in raw runtime data | Replaced with stable pseudonyms REV-A and REV-B | Reviewers must remain anonymous; methodology requires distinguishing two participants |
| Historical form labels | `HAIL-form-tier2-first-person` schema metadata | Retained and disclosed as a metadata defect | Does not change elapsed intervals or review joins |
| Local filesystem paths | `/Users/*/`, `~/Projects/`, OneDrive paths | Removed from all included files | Identify the author's computing environment |
| Cloud connection strings | MongoDB Atlas URIs, n8n database paths | Not included in any released file | Security and identification risk |
| Machine/container IDs | Docker container IDs, process IDs in execution logs | Removed where present in included files | Could identify infrastructure |
| Related submission details | Companion submission title and metadata | Not included | Belongs in confidential editor disclosure |
| Timezone offsets | Consistent `-04:00` offset in Tier 3 event strings | Retained and disclosed; converts to known UTC date | Does not identify individuals; elapsed intervals unchanged |
| Execution IDs | n8n execution IDs (e.g. 1298) | Retained as-is | Operationally necessary for cohort definition; not individually identifying |
| Review identifiers | Unique review_id values in enriched records | Retained as-is | Analytically necessary for join verification |

## Files not copied from the manuscript directory

The following governance records contain confidential information and were not
copied wholesale into this repository:

- `EVIDENCE_LEDGER.md` — Contains author-confirmed institutional references
- `REVIEWER_RISK_REGISTER.md` — Contains internal revision strategy
- `SUBMISSION_DECLARATIONS.md` — Contains author metadata, ORCID, CRediT, related submissions
- `SESSION_HANDOVER.md` — Contains filesystem paths, revision chronology, author feedback
- `STORY_DIAGNOSIS.md` — Contains internal narrative strategy
- `REVISION_STATUS.md` — Contains detailed revision history with hash trails
- `COMMENT_RESOLUTION_LEDGER.md` — Contains reviewer-specific feedback items
- `PHASE1_REVIEW.md`, `PHASE2_RESOLUTION.md` — Superseded internal review records

Safe public-facing content from these records (evidence-status rules,
diagnostic-check definitions, protocol requirements, and evidence-stream
boundaries) has been derived into the `protocols/` directory.

## Remaining excluded items

The following items are excluded because they cannot be safely sanitised or
are not needed for reproducibility:

1. **Synthetic v3 enriched records and workflow exports:** Safe by content
   (all synthetic) but the parent directory contains workflow exports with
   local filesystem paths in node configurations.
2. **Raw retrospective payloads:** Not retained; the cohort is report-defined.
3. **Atlas backup:** Contains absolute local paths and cloud-service identifiers.
4. **30 August harness:** All executions ended in error; files retain
   identifying metadata.

Each excluded item is documented in `MANIFEST.json` under `excluded_material`.
