# TASK-BTE-INTEGRATION — Fail-closed required check and receipt

## Objective

Expose backend formation and downstream consumer-proof completeness through one deterministic, fail-closed validation command and a machine-verifiable required-check manifest.

## Dependencies and blockers

- SWU-BTE-008 depends on SWU-BTE-001 through SWU-BTE-007.
- This task cannot admit the profile or change release state; it produces evidence for the owning release gate.

## SWU-BTE-008 — Integrate the backend completeness check

### Goal

Add an owner-named command such as `validate:backend-engine` that runs every proof surface needed for the bounded backend formation claim and emits one replayable receipt.

### Algorithm

1. Define a machine-readable required-check manifest containing the criterion-kernel tests, content validation, instance validation, node/edge compiler tests, exact-set comparison, generated-suite execution, causal mutation proof, consumer receipts, and typecheck.
2. Run each check with explicit command, working directory, expected artifact, and non-zero failure propagation.
3. Fail before success when the selected profile, witness, independent catalogue, generated manifest, or required receipt is missing or empty.
4. Reconcile exact kind, signature, criterion, obligation, test, mutation, and consumer receipt ID sets; do not use aggregate counts as the sole proof.
5. Emit a receipt with input digests, commands, tool versions, exit statuses, output artifact digests, and the bounded claim.
6. Add negative integration tests for missing feature, empty witness, catalogue drift, undiscovered test, skipped test, surviving mutant, and absent receipt.
7. Route any release-state or supported-profile admission change to its owning decision gate.

### Write scope

- `impl/package.json` scripts
- A required-check manifest and runner under `impl/tools/`
- Direct integration tests and negative fixtures
- Run-scoped backend completeness receipt
- Minimal documentation pointers to the canonical command and bounded claim

### Done criteria

- One documented command runs the complete bounded proof and exits non-zero on every listed negative case.
- The successful receipt proves:
  - `Kinds_profile = Kinds_exercised = 13`
  - `Backend_signatures_admitted = Backend_signatures_exercised = 16`
  - `Criteria_profile = O_spec = O_gen = T_gen = E_run = 16`
  - integrated BTE + IOLM + Body War manifest identity and digest comparison pass.
  - zero skips, todos, orphans, unrunnable obligations, and surviving targeted mutants.
- Receipt verification detects any input or output digest change.
- The command does not claim relationship, semantic, cross-feature, UI, code-conformance, or universal completeness.

### Validation

```bash
npm --prefix projects/domainspec-v2/impl run validate:backend-engine
npm --prefix projects/domainspec-v2/impl run validate
```

The second command is required only after the repository aggregate explicitly includes the new required check.

### Owner and handoff

- Implementation owner: DomainSpec v2 validation owner.
- Release decision owner: first-production-release owner.
- Handoff: refresh this Invoke package with receipt paths and route independent verification through TASK-BTE-VERIFY.
