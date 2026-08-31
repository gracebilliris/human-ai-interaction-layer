# HAIL operational prospective cohort — frozen protocol v3

Cohort identifier: **HAIL_OPERATIONAL_2026-08-31**

Instrument version: **HAIL-v3**. Workflow: **HAIL Operational Cohort v3** (`hail-operational-cohort-v3`). Pipeline version: **CAPRA-v1.0.82**. Form schema version: **HAIL-form-v3**. AI prompt version: **capra-prompt-v1**. Default AI model version: **gpt-4o-mini-2024-07-18** unless a case fixture stipulates a more specific model.

Workflow export: `evidence/prospective_cohort_2026-08-31/hail_operational_workflow_v3.json`.
Workflow export SHA-256: `32a57b6159c29412043a01c2c78958fc59e077d1238c066c6da8fd1df7867b13`.

## Purpose

Complement the six-execution retrospective cohort with an operational prospective cohort using an instrumented HAIL interface that satisfies the reviewer-facing engineering requirements that can be automated for a scripted stress-test cohort.

All cohort records are synthetic stress-test records: `synthetic: true` and `evidence_class: "pipeline_engineering_stress_test"`. Requirements that only a real human reviewer can satisfy, including real inspection, unseeded rationale generation, and a second independent S2 coder, are outside the automation boundary and must be disclosed as such in analysis.

## HAIL-v3 endpoints and retained event stores

- Present webhook: `POST http://localhost:5678/webhook/hail-op-present` with `{review_id, case_id}`. Appends `event: "present"` with server-emitted `review_presented_ts` to `/home/node/.n8n/hail_operational_present.jsonl` and returns the current page-1 form URL.
- Dispatch webhook: `POST http://localhost:5678/webhook/hail-op-dispatch` with `{review_id, case_id, reviewer_code}` and optional case fields. Appends `event: "dispatch"` to `/home/node/.n8n/hail_operational_dispatch.jsonl` including `surfaced_items_manifest`, `pre_revision_text`, `pre_revision_version: "v0"`, `reviewer_code`, and the embedded version manifest. If fields are omitted, the workflow resolves them from the frozen `cases.json` fixtures embedded in workflow static/code data.
- Page-1 form: `http://localhost:5678/form/hail-op-page1-v3`. Records `case_id`, `review_id`, four required acknowledgement checkboxes (`ack_item_1_seen` through `ack_item_4_seen`), and `rationale`; appends `event: "page1_submit"` to `/home/node/.n8n/hail_operational_page1.jsonl`.
- Page-2 form: `http://localhost:5678/form/hail-op-page2-v3`. Records `review_id`, `case_id`, `action`, and `edited_text`; appends `event: "page2_submit"` to `/home/node/.n8n/hail_operational_page2.jsonl`.
- Final JSONL provenance store: `/home/node/.n8n/hail_operational.jsonl`; receives `event: "final"` only after a successful MongoDB decision-store insert.
- Exclusion ledger: `/home/node/.n8n/hail_exclusions.jsonl`; receives `{review_id, case_id, node_that_failed, error_message, exclusion_reason, ts}` for MongoDB write failures and workflow-node errors routed through the HAIL-v3 error ledger branch.

The orchestrator must call the present webhook immediately before opening page 1. The server-emitted `review_presented_ts` in the present event is the pipeline-generated start timestamp used for S3.

## Decision store

The designed target decision store for S9 is MongoDB database `capra`, collection `hail_decision_store`.

For this stress-test run, Atlas credentials were unavailable in n8n. A docker-local MongoDB instance represents the target decision-store class:

- Container: `capra-mongo-decision`
- External host/port: `localhost:27018`
- Hostname reachable from n8n: `host.docker.internal:27018`
- Credential in n8n: `CAPRA local Mongo decision store` (`mongoDb`, id `capra-mongo-decision-local`)

Each successful page-2 submission is composed into a decision record and inserted into `capra.hail_decision_store`. The MongoDB insert returns an `_id`, captured in the final JSONL record as `decision_record_id`, together with `decision_store_write_ts`.

## Frozen S1–S9 definitions

- S1 Intent completeness: eligible optional intent fields with substantive content divided by eligible optional intent fields. Substantive means length ≥ 4 characters, not whitespace, not in the trivial set {ok, yes, no, fine, sure}. Optional intent field = the HAIL page-1 `rationale` input.
- S2 Intent specificity rubric (frozen before coding):
  - 0: no rationale text.
  - 1: rationale is generic — bare agreement or disagreement without naming an attribute, mechanism, standard, or requested change.
  - 2: rationale names an artefact attribute, mechanism, standard, code, or requested change (verified by the frozen keyword register below). Any rationale text without a keyword-register match but with non-trivial content is scored 1.
- S3 Review latency (seconds): `page2_submit_ts − review_presented_ts`, both recorded by the pipeline/server. `review_presented_ts` is emitted by `POST /webhook/hail-op-present` immediately before the orchestrator opens page 1; `page2_submit_ts` is emitted by the page-2 form submission.
- S4 Review acknowledgement coverage: acknowledged surfaced items divided by surfaced items in the dispatch-time `surfaced_items_manifest`. HAIL-v3 records item-level acknowledgement objects: `[{item_index, item_id, acknowledged, acknowledged_at}, ...]`. Slots beyond the case's surfaced-item count are ignored.
- S5 Interaction depth: reconstructed request-response cycles per bounded interaction. `interaction_cycles` is derived by counting retained page events for a given `review_id` (page-1 submit and page-2 submit). It is not a client-set literal.
- S6 Revision-text similarity: cosine similarity in [0, 1] between 5-shingle character sets of `pre_revision_text` and `post_revision_text`. HAIL-v3 records `pre_revision_text` from dispatch/case fixtures with `pre_revision_version: "v0"`; page 2 derives `post_revision_text` as non-empty `edited_text`, otherwise `pre_revision_text`, with `post_revision_version: "v1"`. `edited` is derived from raw text inequality.
- S7 Action divergence: linked AI-recommended and human review action pairs with different codes divided by eligible linked pairs. Codebook (frozen): `{Approve, Reject}`. Every case exposes an `ai_recommended_action` and every submission commits an `action`/`human_review_action` under the same codebook.
- S8 Override rationale coverage: verified S7 divergences with rationale specificity ≥ 1 divided by verified divergences.
- S9 Decision recording: eligible submitted review actions with a verified in-window write to the retained target MongoDB store divided by eligible submitted review actions. Deduplication rule: unique `review_id`.

## Target store and retained S9 query

Primary target store: MongoDB `capra.hail_decision_store`.

Retained S9 query text, frozen for harvest after the run and not executed inside the workflow:

```javascript
verify_mongo: db.getSiblingDB('capra').hail_decision_store.find({review_id: <id>, review_presented_ts: {$gte: w0, $lte: w1}}).count() === 1
verify_jsonl: sha256(one JSONL line per review_id within [w0, w1]) matches decision-store write.
```

Observation window: auto-bounded by the first retained `review_presented_ts`/`dispatch_ts` and the last retained `page2_submit_ts`/`decision_store_write_ts` for cohort review identifiers.

JSONL files are provenance/fallback artifacts, not the primary S9 decision store.

## S2 rubric and frozen keyword register

The S2 rubric is frozen before coding:

- 0: no rationale text.
- 1: rationale is generic — bare agreement or disagreement without naming an attribute, mechanism, standard, or requested change.
- 2: rationale names an artefact attribute, mechanism, standard, code, or requested change.

Frozen keyword register: `NIST`, `FERPA`, `OWASP`, `AES-*`, `HMAC`, `rate-limit`, `rotation`, `encrypt`, `redact`, `audit-log`, `domain`, `hash`, `SLO`, `PHI`, `PII`, `credential`, `stuffing`, `correlation`, `anti-abuse`, `traceable`, `accountable`, `compliance`, `rpm`, `req/min`, `token`, `key`.

Any rationale text without a keyword-register match but with non-trivial content is scored 1. Non-trivial content follows the S1 substantive-text rule.

## S6 method

S6 computes cosine similarity over 5-character shingles of `pre_revision_text` and `post_revision_text`. The comparison is lexical and reproducible; it does not claim semantic equivalence.

## Reviewer identity and cadence protocol

HAIL-v3 captures only a pseudonymous `reviewer_code` (for example, `reviewer_auto_01`). It does not capture reviewer name or email. Cadence is natural for human operation; scripted stress-test operation must be labelled as synthetic pipeline-engineering evidence and not represented as real independent human inspection.

## Disclosed limitations that remain after execution

- Stress-test records are synthetic and do not establish real human inspection.
- A single scripted runner cannot satisfy requirements for unseeded human rationale generation or independent reviewer judgment.
- Independent second coding for S2 rationale specificity is not automated here and must be performed separately if claimed.
- N=20; supports measurability, not inferential statistics.
- AI-recommended actions are pre-attached to case fixtures rather than emitted by an independent upstream agent at review time.
- The local MongoDB target is a MongoDB instance representing the target decision-store class because Atlas credentials were unavailable for this stress-test run.

# Change log

- 2026-08-30 — v3: added server-emitted present event and `review_presented_ts`; item-level surfaced-item manifest/acknowledgement records; dispatch-time `pre_revision_text` with v0/v1 revision identifiers; pseudonymous `reviewer_code` only; embedded version manifest for present/dispatch/page-1/page-2/final records; MongoDB decision-store write to `capra.hail_decision_store`; exclusion ledger; retained S9 query text; and workflow export SHA-256.
- 2026-08-30 — v2: operational two-page HAIL form and JSONL provenance stores for dispatch and submission.
- 2026-08-30 — v1: initial frozen prospective-cohort protocol and S1–S9 metric definitions.
