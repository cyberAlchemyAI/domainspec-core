# TASK-WUI-002: Explicit Task Composer

## Objective

Prevent accidental dry runs by making request mode explicit.

## SWU-WUI-004: Explicit Request Mode

- Primary decision: the operator chooses Agent task or Dry run explicitly.
- Dependencies: `SWU-WUI-003`.
- Source anchors: [Spec](../../SPEC.md), request preparation controls in `public/demo/l0.html`, prepare endpoint tests.
- Related context: existing schema-v2 and legacy request payloads.
- Write scope: composer UI and focused prepare/validation tests.
- Done criteria: Agent task defaults selected; Agent task requires a skill; Dry run omits skill; errors preserve entered values.
- Independent acceptance: two focused journeys prove the selected mode emits the intended existing payload and empty Skill never silently changes modes.
- Validation: `npm run test:workbench` plus Agent task and Dry run Playwright cases.
- Owner: `local-fallback`.
- Split analysis: selector, validation, and payload mapping are parts of one request-mode decision; none can be accepted without the other two.
- Handoff: keep server contracts unchanged unless tests prove an existing route cannot express the explicit mode.

## Synchronization

Record payload evidence for both modes before promoting `SWU-WUI-005`.
