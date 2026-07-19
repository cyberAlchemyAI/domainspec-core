# TASK-WUI-004: Canvas, Craft, And Evidence

## Objective

Make the artifact the center of the workbench while keeping source work and
governance evidence reachable.

## SWU-WUI-008: Primary Canvas

- Primary behavior: place the retained Canvas artifact in the primary workspace.
- Dependencies: `SWU-WUI-003`.
- Source anchors: existing Canvas frame, refresh/notification behavior, Canvas tests.
- Related context: current revision identity and old-frame failure preservation.
- Write scope: Canvas placement and focused Canvas/browser tests.
- Done criteria: current artifact and revision remain visible; navigation failure keeps the previous frame usable.
- Independent acceptance: Canvas tests and one desktop/mobile placement witness pass without Craft or evidence changes.
- Validation: existing Canvas suite plus focused Playwright witness.
- Owner: `local-fallback`.
- Split analysis: placement and revision label share one retained-artifact oracle; interaction behavior remains unchanged.
- Handoff: do not add new Canvas server behavior.

## SWU-WUI-009: Craft Seed

- Primary behavior: seed task and context fields from one selected Craft frontier item.
- Dependencies: `SWU-WUI-004`.
- Source anchors: Craft frontier read route and composer fields.
- Related context: Craft remains the source ledger and is never mutated by selection.
- Write scope: Craft selection UI, composer seeding, focused API/UI tests.
- Done criteria: selecting a frontier item fills intended fields and leaves Craft ledger bytes unchanged.
- Independent acceptance: read projection and seed assertions pass without running or publishing a task.
- Validation: focused Craft API/UI test plus ledger hash comparison.
- Owner: `local-fallback`.
- Split analysis: task and context values are one selection projection and share one no-write oracle.
- Handoff: no Craft mutation endpoints or hidden synchronization.

## SWU-WUI-010: Evidence Inspector

- Primary behavior: present evidence attributable to the admitted run receipt.
- Dependencies: `SWU-WUI-006`, `SWU-WUI-007`.
- Source anchors: admitted receipt projection and current validation/grant/context metadata.
- Related context: ready metadata remains opaque before claim.
- Write scope: Inspector evidence projection and focused receipt journey tests.
- Done criteria: receipt, validation, grants, context, identifiers, and storage remain linked to one run without treating chat output as completion.
- Independent acceptance: a retained receipt journey resolves each evidence group to the same admitted run.
- Validation: focused receipt/evidence Playwright journey plus bridge tests.
- Owner: `local-fallback`.
- Split analysis: evidence groups are projections of one admitted receipt and share one attribution oracle.
- Handoff: consume existing read projections; widen server scope only if a focused test proves missing data.

## Synchronization

Promote to product validation only after all three workspace SWUs pass.
