# TASK-MPX-002-MECHANICS — Validate declared mechanics

## Objective

Check the exact case's declared structural invariants without evaluating truth, equivalence, genre fit, hierarchy plausibility, or reader effects.

## Mapping

- Slice: S-MPX-02
- Layer: L0
- Wave: W1
- SWU: SWU-MPX-002
- Source contracts: `../../IMPLEMENTATION-PLAN.md#SWU-MPX-002--validate-declared-mechanics`; `../shared/VALIDATION-CONTRACTS.json#/units/1`

## Dependencies

- passing SWU-MPX-001 Task Session receipt;
- joined `invoke:refresh` closeout for SWU-MPX-001;
- exact case hash from that closeout.

## Smallest Working Unit: SWU-MPX-002

- Primary behavior: issue one exact mechanics-only validation receipt.
- Independent acceptance boundary: every named structural check is recorded and passes over the exact case bytes while all semantic claims remain false.
- Candidate child units: syntax; span-set equality; hierarchy coverage; boundary flags; claim ceiling.
- Retained-boundary rationale: these are one validation family over one immutable input and one receipt; each isolated command is insufficient evidence for the mechanical gate.
- Write scope:
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/mechanical/MECHANICAL-VALIDATION.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/precloseout/SWU-MPX-002.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/receipts/SWU-MPX-002.task-session.json`
- Invoke-owned closeout output, excluded from Task Session write scope:
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/closeouts/SWU-MPX-002.invoke-refresh.json`
- Done criteria:
  - exact case path, SHA-256, and size recomputed from the actual predecessor bytes;
  - closed required shape and public-safe source binding confirmed;
  - positive span IDs unique and shared exactly by baseline and candidate;
  - baseline has no groups and places the governing point after support;
  - candidate governing point first, appears once, and two or three groups cover every other span exactly once;
  - mandatory review views reconstruct from the exact span text;
  - boundary applicability and activation false and transformation null;
  - the exact nine check IDs are present in order, every individual check records pass, and no failure is masked;
  - `semantic_equivalence_evaluated=false`, `reader_outcome_claims=false`, `integration_authorized=false`, `authority_effect=none`.
- Acceptance evidence: structural result `pass`, exact check inventory, and validation commands passing.
- Execution owner: local fallback under Task Session.
- Handoff note: stop on any input drift; do not repair the case, interpret prose, or convert a human check into lint.

## Mechanical receipt shape

Required top-level keys:

`schema_version`, `experiment_id`, `case_ref`, `checks`, `failed_check_ids`, `semantic_equivalence_evaluated`, `reader_outcome_claims`, `integration_authorized`, `status`, `authority_effect`.

`status=pass` is legal only when `failed_check_ids` is empty, every one of the nine fixed check IDs is present exactly once in order, every check status is `pass`, and the repository-local validator independently revalidates the actual case bytes and the receipt's exact path/hash/size binding.

## Synchronization

On Task Session pass, route only the declared closeout target inventory through `invoke:refresh:apply-approved`. The unique successor is SWU-MPX-003.
