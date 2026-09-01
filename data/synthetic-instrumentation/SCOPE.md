# Synthetic instrumentation evidence scope

## What is included

- This scope statement records the admissible observations and evidence
  boundaries for the 100-record synthetic instrumentation exercise.

## What is excluded

- **Enriched synthetic records** — Safe by content (all synthetic, zero human
  participation) but the parent directory contains workflow exports and
  execution snapshots with local filesystem paths.
- **Workflow export files** — Contain n8n node configurations with local paths.
- **Execution data snapshots** — May contain infrastructure identifiers.
- **MongoDB decision-store dump** — Contains docker-local connection metadata.
- **Operational protocol, audit report, and package history** — Contain local
  paths and implementation labels that are not needed to interpret the
  manuscript's bounded instrumentation findings.

## Evidence boundaries

- Every record carries `synthetic: true`, `human_participation: false`, and
  `generation_method: automated`.
- The `Simulated Human Reviewer` designation describes the role simulated by
  software; it does not identify a person or imply human participation.
- S3: Pipeline/server timestamps retained and linked; intervals are not
  human-review latency evidence.
- S4: Surfaced-item and acknowledgement fields retained and linked;
  acknowledgement values are scripted, not human acknowledgement behaviour.
- S5: **Not accepted** — counts two form submissions as two interaction cycles,
  contrary to the governing request–response definition.
- S6: **Not accepted** — uses sentence-transformer calculation, whereas the
  frozen protocol specifies five-character shingles.
- S9: 100 writes to docker-local MongoDB retained and queryable; establishes
  stress-test persistence, not human-review decision recording.
- S1, S2, S7, S8: Inadmissible for human-review claims because content was
  scripted. S2 also lacks a second independent coder.
