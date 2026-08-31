# Tier 2 walkthrough evidence scope

## What is included

- `TIER2_CANONICAL_RESULTS.json` — Canonical analysis results for the
  author-operated walkthrough.
- `tier2_enriched_records.jsonl` — 20 sanitised enriched records with
  rationales, actions, revision text, surfaced items, and acknowledgements.
  Ethics reference removed, participant pseudonymised (PARTICIPANT-01),
  filesystem paths redacted, author identity replaced.

## What is excluded

- **Recovered submissions** (`recovered_submissions.json`) — Contains
  author-attested fields recovered from n8n execution data after original
  file-write node failure. The relevant fields are included in the enriched
  records above.
- **Case definitions** (`cases_tier2.json`) — Safe by content but excluded
  as the walkthrough evidence is fully contained in the enriched records.
- **Historical harvester** (`harvest_tier2_first_person.py`) — Superseded for
  manuscript claims; retained only for audit history.

## Evidence boundaries

The Tier 2 package is a supplementary author-operated instrumentation and
execution-recovery walkthrough. It is **not** a fresh reviewer-behaviour study.

- One participant completed the walkthrough.
- No external practitioners were recruited.
- 20 page-2 submissions span 13.45 minutes, substantially less than the
  approximately 100-minute protocol expectation.
- Pipeline presentation timestamps are absent.
- All recovery writes were created post hoc after the original file-write
  node failed.

| Check | Status | Key boundary |
|---|---|---|
| S1 | Available | 20/20 substantive rationale fields retained |
| S2 | Partial | No protocol-conformant specificity result; two independent coders absent |
| S3 | Unavailable | Pipeline presentation timestamps absent |
| S4 | Available | 75/75 required acknowledgement fields retained; instrument-enforced completion |
| S5 | Unavailable | Two page submissions do not establish request–response cycles |
| S6 | Partial | 18 eligible revision fields and 2 instruction fields; no protocol-conformant 20-pair aggregate |
| S7 | Available | 20/20 submitted actions matched pre-attached fixture recommendations |
| S8 | Not applicable | Complete linked pairs contain no divergences |
| S9 | Unavailable | Only post-hoc recovery writes retained |

The historical `S1_S9_results_tier2.json` is superseded for manuscript claims.
Use `TIER2_CANONICAL_RESULTS.json` and `analyse_tier2_canonical.py`.

### Sanitisation applied

- Ethics reference (`hrec_ref`) removed from reviewer metadata block.
- `reviewer_display_name` removed.
- `participant_id` and `reviewer_code` replaced with PARTICIPANT-01.
- `recovery_note` paths replaced with `[internal-path]`.
- Author name references replaced with "the participant's".
- See `SANITISATION.md` for the complete record.
