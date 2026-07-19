---
taskId: TASK-HALP-CONTRACTS
docType: work-pack-task
status: blocked-by-decisions
layer: L0
slice: S-000
---

# TASK-HALP-CONTRACTS — Artifact Schemas And Validators

## Objective

Materialize the shared identity, state, and validation grammar for decisions,
protocols, fixtures, trial cells, model stacks, capacity, runs, scores,
analysis, and resource frontiers.

Related context: [shared execution context](../shared/context.md),
[cross-task gaps](../shared/cross-task-gaps.md), and
[traceability](../shared/traceability.md).

## Smallest Working Units

### SWU-HALP-006

- Primary behavior: deterministically accept valid artifacts and reject invalid
  identity/state/receipt transitions.
- Independent acceptance boundary: one validation fixture suite covering the
  interoperating artifact family.
- Split analysis: one schema per artifact was considered; schemas may be files,
  but their shared IDs/references and transition invariants must close together
  before any downstream artifact is useful.
- Dependencies: SWU 001–005.
- Source anchors: [domain](../../domain.md), [interfaces](../../interfaces.md),
  [states](../../states.md), [events](../../events.md).
- Related context: [architecture component view](../../ARCHITECTURE-BUNDLE.md#3-low-level-component-view).
- Write scope: `schemas/`, `src/validate/`, `fixtures/contracts/`, validation
  scripts/package metadata strictly required for those validators.

### Implementation Detail

Inputs: approved decision records and spec concepts.

Outputs: versioned JSON Schemas, semantic validators, positive/negative
fixtures, deterministic validation report.

Algorithm:

1. Define stable IDs and content-hash fields.
2. Encode required structural fields per artifact.
3. Add semantic checks for state transitions, cross-reference existence,
   frozen-version immutability, exact trial factor tuples, and receipt lineage.
4. Add failure-code and arm/estimand enumerations from approved decisions.
5. Create at least one valid fixture and one failure per load-bearing invariant.
6. Run twice and compare reports byte-for-byte after timestamp normalization or
   require timestamps as explicit inputs.

Edge/failure cases: duplicate IDs, missing upstream hash, invalid lifecycle
transition, unknown arm, absent raw-output handle, incompatible score semantics,
unowned exclusion, and frontier axis without boundary metadata.

### Acceptance

- Done: every interface artifact has schema coverage; semantic validators cover
  cross-artifact invariants; fixtures prove positive and negative behavior.
- Evidence: schema inventory and deterministic test report.
- Validation: `node src/validate/validate-contracts.mjs --fixtures fixtures/contracts`.
- Execution owner: local-fallback.
- Handoff note: use only approved decision enum/value ranges; do not invent a
  default to make a fixture pass.

## Synchronization

Update work-pack gate only for contract coverage. A validator pass does not
close human, platform, or resource blockers.
