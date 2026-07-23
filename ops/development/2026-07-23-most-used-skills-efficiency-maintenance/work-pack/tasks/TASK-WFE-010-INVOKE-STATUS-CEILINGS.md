# TASK-WFE-010 — Separate Invoke Capability Status Ceilings

- Change: INV-2 / WFE-R04
- Layer/slice/wave: L2 / S2 / W2
- Lifecycle owner: `spellcraft` for Invoke
- Status: complete; see
  `../session-evidence/SWU-WFE-010/receipt.json`

## Objective

Expose artifact authoring, registry release, and mutation-runtime readiness as
three independent machine-readable axes without disabling active Plan authoring
or enabling deferred `full`/`validate` modes.

## Sources

- `arcanum/spells/invoke/mode-capabilities.json`
- `arcanum/spells/invoke/plan.md`: active L2 authoring/nonexecution boundary
- `arcanum/spells/invoke/development/VALIDATION.md`: registry/live regime gates
- INV-1 material validator receipt
- accepted findings INV-2

## SWU-WFE-010

- Primary behavior: capability resolver computes and returns three status axes
  from their own evidence receipts.
- Acceptance boundary: Plan may be authored while registry/runtime remain false;
  deferred `full`/`validate` cannot claim any mutation handoff; no test infers a
  later axis from an earlier one; valid receipts open only their matching axis.
- Split analysis: axes are independent outputs but rows of one capability-status
  resolver; separate implementations risk reconstructing the same collapsed
  label in consumers.

## Data and precedence

```yaml
artifact_authored:
  status: pass | flag | block | unsupported
  evidence: [receipt]
registry_released:
  status: true | false
  evidence: [owner receipt]
mutation_runtime_ready:
  status: true | false
  evidence: [material package and runtime receipts]
```

Rules:

1. Plan authoring pass can set only `artifact_authored=pass`.
2. Registry release requires its existing deterministic/live-regime owner proof.
3. Runtime readiness requires material-package pass plus every mode-specific
   runtime gate.
4. `full` and `validate` remain unsupported/deferred and never emit mutation
   handoff.
5. Existing consumers fail explicitly if they still expect one collapsed field.

## Scope and validation

- Canonical resolver/table, schema/fixtures, docs that consume the fields.
- Declared generated Invoke runtimes only.
- Forbidden: enabling deferred modes, target mutation, or registry promotion.

```bash
bash arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- arcanum/spells/invoke .agents/skills/invoke .claude/skills/invoke
```

- Dependencies: SWU-WFE-003B and TASK-WFE-009 program-order receipt.
- Execution owner: `spellcraft`.
- Receipt: complete mode/status matrix, consumer compatibility result, generated
  parity, unchanged deferred-mode mutation boundary.

## Done

Every active/deferred mode reports honest independent ceilings and no authored
artifact can be mistaken for registry release or runtime mutation readiness.
