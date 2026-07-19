# TASK-WUI-005: V1 Validation

## Objective

Prove regression safety, responsive usability, and human value before making V1
the default product claim.

## SWU-WUI-011: Integrated Product Verdict

- Primary decision: whether the composed V1 is ready to become the default workbench screen.
- Dependencies: `SWU-WUI-008`, `SWU-WUI-009`, `SWU-WUI-010`.
- Source anchors: all prior SWU receipts, scoped Node/Playwright suites, [UX plan](../../UX-PLAN.md).
- Related context: human usefulness is a promotion gate, not an automated assertion.
- Write scope: tests, retained screenshots/reports, Work Pack/Craft/README status only.
- Done criteria: desktop/mobile matrix passes; keyboard, focus, fit, overlap, real agent-task, Canvas output, and explicit human usefulness verdict are recorded.
- Independent acceptance: machine evidence and human verdict agree; absent human verdict blocks instead of self-approving.
- Validation: full scoped Node/Playwright matrix plus human Decision Gate.
- Owner: `local-fallback-plus-human-review`.
- Split analysis: machine proof and human verdict are separately produced but jointly define one promotion decision; neither alone can close V1 readiness.
- Handoff: do not alter product behavior while validating; route failures back to the owning SWU.

## Synchronization

Close the Work Pack and owning Craft context only after the explicit verdict.
