# Evidence-status rules

These are the operational definitions governing all diagnostic-check
classifications in the paper. They are derived from the manuscript's HAIL
traceability assessment.

## Four evidence-status categories

### Available

Every required record, field, identifier, population, window, and query is
present, so the diagnostic-check result can be determined.

### Partial

Cohort evidence supports part of the diagnostic check, but an indispensable
record or connection is absent.

### Unavailable

The required construct, population, record, or connection cannot be
established.

### Not applicable

Complete evidence establishes that the eligible population is empty.

## Critical distinctions

### Unavailable evidence is not zero

An observed zero is a possible diagnostic-check result only when the evidence
is Available. It is not an evidence-status category. When evidence is
Unavailable, the diagnostic-check result cannot be determined—it may be zero,
non-zero, or undefined. Reporting Unavailable evidence as zero misrepresents
the state of knowledge.

This distinction governs S9 throughout the paper: no target-store query,
observation window, or raw result is retained for the retrospective cohort,
so the result is Unavailable rather than zero.

### Missing evidence versus a measurement boundary

A diagnostic check classified as Unavailable reflects a measurement boundary:
the instrument, pipeline, or study design did not produce the evidence needed
to determine the result. It does not mean the underlying behaviour failed or
that the pipeline malfunctioned.

### Conditional checks

S8 (Override rationale coverage) requires verified S7 divergences as a
prerequisite. If S7 produces zero eligible divergences from Available evidence,
S8 is Not applicable. If S7 is Unavailable, S8 is also Unavailable because
its precondition cannot be established.

### Synthetic evidence boundaries

Records marked `synthetic: true` and `human_participation: false` support
bounded instrumentation observations only. Their field values were generated
by software and cannot support human intent, attention, judgement, editing, or
behaviour claims. S5 and S6 outputs from synthetic records conflict with their
governing operational definitions and are not accepted as protocol-conformant
results.

### Protocol-conformant versus produced outputs

A diagnostic check may produce a numeric output without satisfying its
governing operational definition. For example, counting two form-page
submissions as two interaction cycles does not establish S5 Interaction depth
because the governing definition requires reconstructed request–response cycle
boundaries. Produced outputs that conflict with their definitions are disclosed
but not accepted as results.
