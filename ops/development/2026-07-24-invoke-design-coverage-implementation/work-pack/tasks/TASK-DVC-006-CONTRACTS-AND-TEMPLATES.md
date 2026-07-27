# TASK-DVC-006: Invoke Contracts And Companion Templates

- Slice/layer/wave: S2 / L2 / W2.
- Sources: `../../../DESIGN.md`, `../../../UX-PLAN.md`, complete W1 receipts.
- Dependency: DVC-005.
- Gaps owned: DVC-G01 and DVC-G08.

Capture live baselines before every SWU. `README.md` and the aggregate runner
are already dirty; their SWUs block if the intended delta cannot be isolated.

## SWU-DVC-006A: Design mode contract

- Primary behavior: make Design order manifest, extraction, selection, fixed
  point, companions, and handoff with exact gates.
- Write scope: `arcanum/spells/invoke/design.md`.
- Acceptance: six views remain required; authored-only remediation may plan the
  missing validator; normal Plan handoff requires `design-validator-pass`;
  planned witnesses never count as Plan evidence.
- Validation: design contract fixtures plus Design mode evidence fixture.

## SWU-DVC-006B: Architecture output contract

- Dependencies: DVC-006A.
- Primary behavior: require closed-scope and concern trace while selecting only
  triggered architecture extensions.
- Write scope:
  `arcanum/spells/invoke/templates/domainspec-spec/architecture-bundle.md` and
  `arcanum/spells/invoke/templates/architecture/architecture.md`.
- Retained boundary: both public architecture profiles must expose one
  compatible contract; updating only one creates divergent Design semantics.
- Acceptance: significant behavior scenario, concern-to-view trace, exact
  owners, four dispositions, planned fixture/validator contracts, and
  risk-triggered extension section exist.

## SWU-DVC-006C: UX trigger and output contract

- Dependencies: DVC-006B.
- Primary behavior: select and author UX from the natural-person plus changed
  semantic-contract predicate.
- Write scope:
  `arcanum/spells/invoke/templates/ux-plan/ux-plan.md`.
- Acceptance: success/failure/recovery, correction/reversibility, visible
  evidence meaning, content bounds, focus/reflow/contrast/names/assistive
  operation, responsive semantics, exact acceptance owners, and positive/
  negative trigger examples exist.

## SWU-DVC-006D: Invoke root evidence reporting

- Dependencies: DVC-006C.
- Primary behavior: expose Design evidence state without collapsing the
  existing authored/registry/runtime capability axes or Plan evidence.
- Write scope: `arcanum/spells/invoke/README.md`.
- Acceptance: root output and global gates name the Design-selection receipt,
  evidence ceiling, target gaps, and Spellcraft handoff.
- Dirty-baseline gate: compare pre-write digest and scoped patch against the
  captured DVC-006D baseline; unrelated hunks block.

## SWU-DVC-006E: Aggregate validation integration

- Dependencies: DVC-006D.
- Primary behavior: make aggregate Invoke validation invoke the Design-
  selection runner and preserve its exact failure.
- Write scope:
  `arcanum/spells/invoke/development/run-validation-fixtures.sh`.
- Acceptance: missing runner or nonzero child result fails aggregate validation;
  child report path is surfaced.
- Dirty-baseline gate: preserve all unrelated current runner changes.

## Shared validation

```bash
arcanum/spells/invoke/development/run-design-selection-fixtures.sh
arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- arcanum/spells/invoke
```

Run each command at the earliest SWU where its inputs exist. Use one closeout
receipt per SWU; never combine the five source decisions into one result.

## Completion evidence

- SWU-DVC-006A: pass; Design mode now binds manifest, denominator, total
  selection, two-pass fixed point, remediation-only authored routing, and
  separate Plan evidence. Receipt:
  `../session-evidence/SWU-DVC-006A/execution-receipt.json`.
- SWU-DVC-006B: pass; both architecture profiles preserve the six-view
  baseline and add compatible scope, concern trace, scenario, planned witness,
  exact ownership, and triggered-extension contracts. Receipt:
  `../session-evidence/SWU-DVC-006B/execution-receipt.json`.
- SWU-DVC-006C: pass; UX selection now requires a natural person plus changed
  semantic contract and covers success, failure/recovery, correction,
  reversibility, evidence meaning, content bounds, accessibility, responsive
  semantics, and exact acceptance owners. A downstream contract probe exposed
  and repaired one whitespace-sensitive phrase split; the complete matrix
  re-passed without changing the frozen corpus. Receipt:
  `../session-evidence/SWU-DVC-006C/execution-receipt.json`.
- SWU-DVC-006D: pass; the root contract now reports Design selection receipt,
  evidence state, evidence ceiling, and Plan evidence independently of the
  authored/registry/runtime capability axes, and names exact target gaps and
  Spellcraft handoff. Receipt:
  `../session-evidence/SWU-DVC-006D/execution-receipt.json`.
- SWU-DVC-006E: pass; aggregate Invoke validation now runs the deterministic
  Design-selection suite, preserves its output and report path, and fails
  closed on a missing, non-executable, nonzero, or reportless child. Receipt:
  `../session-evidence/SWU-DVC-006E/execution-receipt.json`.
