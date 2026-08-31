# Synthetic v3 package audit summary

This is a sanitised summary of the independent audit of the 100-record
synthetic pipeline-engineering stress test. The full audit report is retained
privately because it contains local filesystem paths.

## Audit result

- **Total files audited:** 546
- **Hash verification:** 546/546 passed (after correction addendum)
- **Initial pass:** 581/583 — two files had been modified between packaging
  and first-pass verification; the correction addendum verified 583/583.

## Key findings

1. All 100 enriched records carry `synthetic: true`, `human_participation:
   false`, and `generation_method: automated`.
2. All 100 records have unique review identifiers and successful execution
   status.
3. The `Simulated Human Reviewer` designation describes a software role, not
   a person.
4. S5 output is not accepted: it counts page-1 and page-2 submissions as two
   interaction cycles, contrary to the governing request–response definition.
5. S6 output is not accepted: it uses a sentence-transformer calculation,
   whereas the frozen protocol specifies five-character shingles.
6. S2 lacks a second independent coder.
7. All 100 submissions had one retained, queryable write in the docker-local
   MongoDB target-store class.

## Metadata defect

`VERSION_MANIFEST.md` assigns the SHA-256 of `harvest_operational_v3_bugged.py`
to the active `harvest_operational_v3.py`. The active script's verified SHA-256
is `4fd07cbd1f4d59f6fbf4243daeff228f9851d730abcd8181caa57a6220cc241a`.

## Evidence class

All records use `pipeline_engineering_stress_test` as their evidence class.
No value from this package changes the retrospective evidence ceiling or the
results reported in the manuscript.
