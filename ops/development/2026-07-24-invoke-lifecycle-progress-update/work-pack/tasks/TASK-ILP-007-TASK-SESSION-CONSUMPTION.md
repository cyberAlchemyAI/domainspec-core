# TASK-ILP-007: Task Session Ready-Epoch Consumption

## Objective

Require a current admitted ready epoch before Task Session mutation while
preserving its independent live pre-write checks and one-SWU boundary.

- Layer/slice/wave: L2 / S2 / W2
- Lifecycle owner: Sigil Development
- Dependencies: SWU-ILP-004 and SWU-ILP-005; SWU-ILP-006B for typed closeout
- Source contracts: current `arcanum/arcana/task-session/SKILL.md`, mutation
  admission schemas/verifier, `../../DESIGN.md`
- Write scope:
  - `arcanum/arcana/task-session/SKILL.md`
  - `arcanum/arcana/task-session/README.md`
  - `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`
  - `arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json`
  - `arcanum/arcana/task-session/scripts/verify-mutation-readiness.py`
  - focused Task Session fixtures/runner
  - generated Task Session mirrors through canonical synchronization

## Algorithm

1. Resolve exactly one selected epoch and SWU.
2. Require admitted `handoff_ready`, readiness receipt, producer output/receipt,
   producer schema, and epoch/control digests.
3. Validate receipt identities against the owner-approved schemas; do not copy
   Invoke validator logic.
4. Reread every live controlling artifact and dependency.
5. Compare unit, paths, allowed writes, dependencies, validation, receipt
   classes, and closeout contract.
6. On any absence/staleness/mismatch, emit `admission_blocked` before mutation.
7. On pass, emit an epoch-bound admission receipt.
8. Preserve one-SWU execution, first-effect receipt, live validation, and
   separate closeout owner join.

## Smallest Working Unit

### SWU-ILP-007

- Primary behavior: decide Task Session mutation admission for one ready epoch.
- Acceptance boundary: one admission receipt plus zero writes on every reject.
- Candidate children: ready receipt check; live reread; receipt extension.
- Retained rationale: all are conjuncts of the single first-write gate.
- Execution owner: `local-fallback` through Sigil Development.
- Done criteria:
  - absent, gated, blocked, stale, mismatched, wrong-unit, and changed-control
    cases block before write;
  - current ready local contract admits and still runs live validation;
  - current packaged modes preserve existing exact validation;
  - no receipt claims multiple SWUs.
- Validation:
  `python3 arcanum/arcana/task-session/development/validate-mutation-admission.py && python3 arcanum/arcana/task-session/development/run-lifecycle-progress-fixtures.py`
- Handoff context: SWU-ILP-004/005/006B receipts and current admission fixtures.

## Closeout

Use `../shared/CLOSEOUT-CONTRACT.md`. Task Session emits the implementation
receipt; Invoke Refresh owns exact planning synchronization; the transition
owner separately admits lifecycle progress.

