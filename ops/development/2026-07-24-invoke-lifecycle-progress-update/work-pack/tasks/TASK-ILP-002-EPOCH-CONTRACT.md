# TASK-ILP-002: Immutable Epoch and Control Graph

## Objective

Implement one deterministic verdict that accepts a complete immutable
selected-SWU epoch and rejects incomplete or mutable control identity.

- Layer/slice/wave: L1 / S1 / W1
- Lifecycle owner: Spellcraft
- Dependencies: SWU-ILP-001 pass
- Source contracts: `../../DESIGN.md` sections 2-3,
  `../shared/DECISIONS.md`
- Candidate write scope, subject to SWU-ILP-001:
  - `arcanum/spells/invoke/schemas/execution-epoch.schema.json`
  - `arcanum/spells/invoke/scripts/validate_execution_epoch.py`
  - `arcanum/spells/invoke/development/fixtures/lifecycle-progress-cases.json`
  - `arcanum/spells/invoke/development/run-lifecycle-progress-fixtures.py`

## Algorithm

1. Parse and schema-check the epoch candidate.
2. Require exactly one selected unit and one execution mode.
3. Traverse declared work-pack/task/SWU/source/dependency/validation/closeout
   references using concrete normalized paths.
4. Reject unresolved globs, missing paths, duplicate paths, unknown dependency
   IDs, overlapping controlling/projection classes, and incomplete role data.
5. Recompute exact SHA-256 for controlling paths.
6. Canonically sort every set and compute `epoch_control_digest`.
7. Reject a supplied digest mismatch.
8. Emit a completeness receipt; do not admit a lifecycle edge.

If later discovery finds an undeclared control, the validator does not patch
the epoch. The caller must author a successor candidate.

## Smallest Working Unit

### SWU-ILP-002

- Primary behavior: decide epoch-issuance completeness.
- Acceptance boundary: one validator receipt binds the complete declared graph
  and exact control digest.
- Candidate children: schema, traversal, digest, fixtures.
- Retained rationale: each is a necessary conjunct of one issuance verdict;
  none is independently deployable.
- Execution owner: `local-fallback` through Spellcraft-accepted Task Session.
- Done criteria:
  - valid one-unit candidate passes;
  - omitted mutation handoff, path class, dependency, allowed write, validation,
    or receipt class fails causally;
  - changed plan/unit/mode/role/path/dependency/write/validation/class changes
    the recomputed digest;
  - validator emits no transition authority claim.
- Validation:
  `python3 arcanum/spells/invoke/development/run-lifecycle-progress-fixtures.py --group epoch`
- Handoff context: `../shared/CONTEXT.md`, `../../DESIGN.md`,
  SWU-ILP-001 receipt.

## Closeout

Use `../shared/CLOSEOUT-CONTRACT.md`. The owner receipt must also prove
canonical/generated Invoke parity if runtime surfaces change.

## Expected return

Standard SWU receipt plus epoch fixture counts and exact validator path.

