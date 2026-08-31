# Prospective HAIL evidence protocol

This protocol governs the collection of any future prospective evidence cohort.
It was frozen before the review study and defines the exact gates each
diagnostic check must satisfy.

## Study design

Collect new evidence as a prospective cohort. Do not merge its records or
denominators with the retrospective six-execution cohort. The retrospective
cohort diagnoses the pre-existing traceability gaps; the prospective cohort
tests whether a fully instrumented HAIL execution produces the evidence needed
to determine S1–S9.

Before collection, freeze:

- the prototype, HAIL form, prompt, and agent versions;
- the review action codebook;
- the rationale-coding rubric;
- the interaction-cycle boundary;
- the embedding model and text preprocessing;
- the cross-stage review identifier;
- the observation window;
- the database and execution-trace queries;
- the exclusion and deduplication rules; and
- the cohort size and its methodological rationale.

Every record must carry one non-personal `review_id` from the AI-generated
artefact through the review form, revision, human–AI action comparison, and
target-store decision record.
Do not retain reviewer names or email addresses in the research dataset.

## Cohort eligibility

An execution is eligible when:

1. HAIL presented an AI-generated artefact to a reviewer;
2. the reviewer submitted one action under the frozen action codebook;
3. the execution has a unique `review_id`;
4. the raw execution chain and form payload were exported; and
5. the complete observation window elapsed.

Retain excluded executions with an exclusion reason. Never silently drop an
execution because a record, join, or event is missing.

## Diagnostic-check acceptance gates

| Diagnostic check | Required prospective evidence | Determination and claim boundary |
|---|---|---|
| S1 Intent completeness | Frozen form schema with at least one optional intent field, plus the raw field values or explicit nulls for every eligible review | Substantive optional intent fields divided by eligible optional fields; does not establish reasoning quality |
| S2 Intent specificity | Raw rationale text, frozen 0–2 rubric and codebook, two independent coders, and pre-resolution agreement | Report the score distribution and agreement; does not establish factual correctness |
| S3 Review latency | Emitter-generated dispatch and submission timestamps from the same clock, linked by `review_id` | Report seconds per review and cohort median, IQR, minimum, and maximum; does not measure cognitive effort |
| S4 Review acknowledgement coverage | Item-level surfacing manifest and view or acknowledgement event for each surfaced item before decision submission | Acknowledged surfaced items divided by eligible surfaced items; one form-level checkbox is insufficient when several items are shown |
| S5 Interaction depth | Complete execution chain, frozen request–response cycle definition, and cycle boundaries linked by `review_id` | Count complete cycles per review; page completion or populated identity fields are not cycles |
| S6 Revision-text similarity | Ordered pre- and post-revision texts linked by `review_id`, plus frozen embedding model, checkpoint, preprocessing, and truncation rules | Compute cosine similarity per pair; proposed-change presence or count is not text similarity and does not establish semantic change |
| S7 Action divergence | Persisted AI-recommended action and human action mapped to one frozen codebook and joined by `review_id` | Different action codes divided by eligible linked pairs; a `requires_human_review` flag is not an AI-recommended action unless the codebook establishes equivalence |
| S8 Override rationale coverage | Verified S7 divergences, linked rationale texts, and S2 codes | Divergences with S2 score at least 1 divided by verified divergences; report not applicable only when complete evidence establishes no divergences |
| S9 Decision recording | Review submission and target-store write joined by `review_id`, emitter timestamps, frozen window, retained query, raw query result, and deduplication rule | In-window verified writes divided by eligible decisions; missing or unjoined evidence is unavailable, not zero |

## Validation before analysis

For every execution:

1. verify that `review_id` is identical across all required records;
2. verify that timestamps are emitted by the running pipeline, non-null,
   ordered, and use the stated clock;
3. verify that the raw form payload and execution chain are retained;
4. verify that pre- and post-revision texts are distinct versioned artefacts;
5. verify that the AI recommendation and human action use the frozen codebook;
6. verify that the target-store query is retained with its raw result; and
7. record any failed check as an evidence-status result, not as a behavioural
   zero.

## Analysis and reporting

Report the prospective cohort separately from the retrospective cohort. For
each diagnostic check, state the eligible population, exclusions, numerator and
denominator or distribution, missing data, and evidence status. Do not describe
the diagnostic-check set as validated merely because values can be determined.
Do not claim improved collaboration, trust, reliability, or auditability
effectiveness without an evaluation designed to measure that outcome.
