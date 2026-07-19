# Cross-Task Blockers And Gaps

| ID | Class | Affects | State | Owner | Repair |
| --- | --- | --- | --- | --- | --- |
| R-BTE-001 | resolved dependency | lane routing | closed | FPR-02 coordination owner | Backend and UI are separate; FPR-02U admission or completion is not an input to any BTE SWU. |
| B-BTE-001 | acceptance blocker | all SWUs | resolved | FPR-02B owners | Accepted by DEC-FPR02-SUPPORTED-PROFILE; no decision blocker remains. |
| B-BTE-002 | contract blocker | BTE-002 onward | resolved | FPR-02B profile + node/edge contract owners | Successor profile, roots, and mapping accepted; implementation remains Task Session-owned. |
| G-BTE-001 | scope gap | FPR-02B | active | relationship owner | Exercise all 16 backend signatures with causal composition/removal evidence. |
| G-BTE-002 | claim gap | FPR-07/FPR-09 | deferred | semantic/conformance owners | Structural checks cannot claim business correctness. |
| G-BTE-003 | evolution gap | future | deferred | cross-feature owner | Trigger only when a cross-feature product claim exists. |
| G-BTE-004 | tooling residue | BTE-001 | accepted | tooling owner | Keep the YAML subset bounded; broaden only from an actual unsupported schema. |
| G-BTE-005 | consumer gate | IOLM | active | IOLM owner | Preserve `G-DSV2-SG: BLOCKED` until exact owner receipts and bounded Sg proof pass. |
| G-BTE-006 | consumer contract | Body War | active | Body War consumer owner | Add private read-only fixture/adapter and redaction proof under the consumer home. |
| G-BTE-007 | continuation sync | Craft/Inventory | active | Craft + Inventory owners | Register the applied refresh and new consumer proof artifacts. |
| G-BTE-008 | authority drift | engine path | needs-review | engine owner | Resolve legacy/v2 path and local source-of-truth wording before implementation handoff. |

## Stable Non-Claims

- `13/13` backend kinds is not full-language coverage.
- `16/16` backend relationship signatures and structural criteria are not semantic satisfiability.
- Empty minted projects may remain valid at compiler altitude; an empty release witness must fail at coverage altitude.
- No passing Task Session or test receipt grants release admission.
- FPR-02U progress, blockage, or completion cannot change backend BTE readiness.
