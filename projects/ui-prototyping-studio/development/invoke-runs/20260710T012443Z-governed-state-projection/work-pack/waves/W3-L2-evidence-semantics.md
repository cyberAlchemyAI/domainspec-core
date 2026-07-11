# W3 - L2 Evidence Semantics

## Layer Question

After this wave, we know whether validation and evidence semantics preserve
claim <= proof across tests, handoff, and docs.

## Tasks

- [TASK-GSP-004](../tasks/TASK-GSP-004-validation-handoff-docs.md)
- [TASK-GSP-005](../tasks/TASK-GSP-005-craft-evidence-pack.md)

## Dependencies

- `SWU-GSP-001` for e2e harness and docs sync.
- `SWU-GSP-002` and `SWU-GSP-004` before `CraftEvidencePack`.

## Validation

- Standard checked-in e2e route no longer depends on ambient Corepack.
- Handoff readiness labels do not overclaim when refs/evidence are missing.
- Minimal OD-inspired evidence pack stays behind Studio gates.
