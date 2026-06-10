# Stage 06 — Invoke Redefine / Design
Capability: `invoke` · Mode: `design` · Status: **pass**
Inputs: distill-frame (Shape A) + schema-discipline receipt · Overlay carry: `memory_residue`

## Emitted candidate design
- `candidate/infra-spec.schema.json` — self-contained Draft 2020-12 schema for the operational-contract spine. Reuses dispatch `$def` SHAPES (boundary/authority/receipt/state_namespace/promotion_split/gate); `boundary.kind` redefined to infra enum (network/secret/data_store/tenant/policy/environment); `gate_action` inlined for self-containment.
- Discipline encoded in shape: required floor (10 fields), `status_class: const candidate` (no schema path to a non-candidate record), `not.required[status]` (forbids collapsed status), enums for runtime_profile/boundary.kind/promotion_status.stage/residue.kind/gate_action, minItems on environments/services/gates/residue, service.owner required, `reversal` $def (rollback/migration/backup/retention), `analogy_labels` (analogy-demotion made structural).
- `fixtures/` — 1 spine-pass + 6 shape-layer violations + 3 governance-layer violations + README expectation table.

## Discipline carried from reviewers
- evidence≠authority: `promotion_splits` reused as the structural enforcer; promotion gated by `promotion_guardrail` gate.
- schema≠instance: enums/types only; no instance values baked in.
- analogy labels: borrowed-register vocabulary requires an `analogy_labels` entry (governance rule).
- candidate-only: artifacts in run folder; no `formulae/infra-spec`, no pipeline wiring.

## Verdict
`pass` — design materialized as a runnable candidate. Routed to design-review + toy-game.
