# TASK-ILP-006: Independent Drift Impact and Typed Refresh

## Objective

Separate byte mismatch from semantic change impact, then make each Refresh
declare exactly one transition kind and postcondition.

- Layer/slice/wave: L2 / S2 / W2
- Lifecycle owner: Spellcraft
- Dependencies: SWU-ILP-003 and SWU-ILP-005
- Source contracts: current `arcanum/spells/invoke/refresh.md`,
  `../../DESIGN.md`, `../shared/DECISIONS.md`

## SWU-ILP-006A: Change-impact classifier

- Primary behavior: classify one changed-path set.
- Write scope:
  - `arcanum/spells/invoke/schemas/change-impact-receipt.schema.json`
  - `arcanum/spells/invoke/scripts/classify_change_impact.py`
  - focused fixtures/runner
- Algorithm:
  1. Verify exact old/new digests and complete epoch path sets.
  2. Reject classifier identity equal to any changed projection writer.
  3. Intersect changed paths with controlling and projection sets.
  4. Return `execution_invalidating`, `projection_only`, `unrelated`, or
     `unclassified` by the precedence in `../../DESIGN.md`.
  5. Never convert exact mismatch into an accepted old join.
- Acceptance boundary: deterministic classifier receipt.
- Candidate children: identity check; set intersections; verdict.
- Retained rationale: all produce one mutually exclusive classification.
- Done criteria: causal fixtures cover all four verdicts, writer conflict, and
  preserved exact mismatch.
- Validation:
  `python3 arcanum/spells/invoke/development/run-lifecycle-progress-fixtures.py --group change-impact`
- Execution owner: `local-fallback` through Spellcraft.

## SWU-ILP-006B: Refresh kind and postcondition

- Primary behavior: admit one Refresh request shape and postcondition.
- Dependencies: SWU-ILP-006A
- Write scope:
  - `arcanum/spells/invoke/refresh.md`
  - `arcanum/spells/invoke/README.md`
  - owner-approved Refresh schemas/scripts/fixtures
  - generated Invoke mirrors through canonical synchronization
- Algorithm:
  1. Require exactly one of `plan_repair`,
     `material_production_validation`, `projection_synchronization`, or
     `route_selection`.
  2. Validate the kind-specific input and postcondition.
  3. Reject target implementation in all kinds.
  4. Submit eligible evidence to the transition owner; do not admit locally.
  5. Let `projection_synchronization` update owner projections but admit no
     lifecycle state edge.
  6. Compare epoch control digest: changed control requires successor;
     evidence-only completion may retain epoch.
- Acceptance boundary: real Refresh entry rejects mixed/invalid kinds and
  returns one typed result.
- Candidate children: enum; postconditions; route; prohibition.
- Retained rationale: partial enforcement preserves overloaded/bypass paths.
- Done criteria: mixed kinds, missing postcondition, target implementation, and
  same-epoch control repair fail; four valid generic cases pass within bounds.
- Validation:
  `python3 arcanum/spells/invoke/development/run-lifecycle-progress-fixtures.py --group refresh-kind`
- Execution owner: `local-fallback` through Spellcraft.

## Closeout

Each SWU independently uses `../shared/CLOSEOUT-CONTRACT.md`. Do not combine
006A and 006B into one Task Session.

