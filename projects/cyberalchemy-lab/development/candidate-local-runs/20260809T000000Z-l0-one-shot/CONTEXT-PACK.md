# Candidate-local one-shot context — WP-CAL-TEN-L0

This is runtime context for a local prototype fast lane. It is not a lifecycle, publication, or promotion record.

## Outcome

Implement the finite L0 stream `SWU-CAL-001` through `SWU-CAL-010` under `projects/cyberalchemy-lab/research/tower-evidence-navigator/` and the one synthetic witness root. Preserve the candidate/synthetic/no-authority ceiling. Run the complete declared validation surface only after all product writes are complete.

## Obligations

| ID | Scope | Source | Status |
| --- | --- | --- | --- |
| O1 | Canonical JSON identity primitive | `work-pack/tasks/TASK-CAL-CONTRACTS.md#SWU-CAL-001` | covered-existing |
| O2 | Closed records, relations, projection, privacy | `TASK-CAL-CONTRACTS.md#SWU-CAL-002` through `#SWU-CAL-003`; `ARCHITECTURE.md#Closed-record-kinds` | covered |
| O3 | Candidate tower spine and controls | `TASK-CAL-PACKAGE.md#SWU-CAL-004` through `#SWU-CAL-005` | covered |
| O4 | Exact synthetic fixture and graph | `TASK-CAL-PACKAGE.md#SWU-CAL-006`; `08-distill-repair.md#Repair-3--Exact-valid-toy-fixture` | covered |
| O5 | Compiler and mutant matrix | `TASK-CAL-COMPILER.md`; `ARCHITECTURE.md#Compiler-workflow`; `08-distill-repair.md#Required-deterministic-mutant-matrix` | covered |
| O6 | Snapshot self-binding and witness | `TASK-CAL-SNAPSHOT.md`; `TASK-CAL-WITNESS.md` | covered |
| O7 | Boundaries | `work-pack/shared/CONTEXT.md#Global-invariants` and user direct instruction | covered |

## Boundaries

- Allowed product roots: `projects/cyberalchemy-lab/research/tower-evidence-navigator/` and `projects/cyberalchemy-lab/development/witness-runs/l0-synthetic-001/`.
- No network, credentials, package-root/dependency creation, IDE transport, real/representative tower, promotion, publication, deployment, Git operation, or external message.
- Defer Task Session/Invoke/closeout/receipt choreography. The deferred-governance notice is `HN-C73A66BB7C6D`.
- If a source-level ambiguity blocks deterministic implementation, use `refine` only for that named gap and stop product expansion until it is resolved.

## Verification surface

Run at the end, in dependency order: all Node contract tests, full `tests/*.test.mjs`, snapshot `--check`, two isolated compiler runs with byte comparison, and JSON parsing of each witness JSON artifact.
