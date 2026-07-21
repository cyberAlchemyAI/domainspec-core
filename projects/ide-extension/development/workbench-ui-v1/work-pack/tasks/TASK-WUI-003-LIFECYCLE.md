# TASK-WUI-003: Run Lifecycle

## Objective

Present one understandable run lifecycle and only legal actions for its state.

## SWU-WUI-005: RunView Projection

- Primary behavior: map raw envelope, approval, claim, result, and receipt state into one pure `RunView`.
- Dependencies: `SWU-WUI-004`.
- Source anchors: bridge projector/state types, current run rendering in `public/demo/l0.html`, bridge contract tests.
- Related context: ready secrecy and admitted receipt semantics.
- Write scope: pure UI mapper and mapper fixtures/tests.
- Done criteria: every supported bridge typestate maps to one truthful label, stage, legal-action set, and evidence handle without DOM effects.
- Independent acceptance: mapper fixture matrix passes independently of rendering.
- Validation: focused mapper unit tests plus `npm run test:bridge`.
- Owner: `local-fallback`.
- Split analysis: per-state mappers are branches of one exhaustive projection contract and share one completeness oracle.
- Handoff: do not render the timeline or wire actions in this SWU.

## SWU-WUI-006: Run Timeline

- Primary behavior: render Prepared, Approved, Available, Running, Result, and Receipt stages from `RunView`.
- Dependencies: `SWU-WUI-005`.
- Source anchors: `RunView` contract and current history/result markup.
- Related context: claimed is not completed; chat output is not admitted completion.
- Write scope: lifecycle renderer and focused browser fixtures.
- Done criteria: each stage appears in order with truthful current/completed/pending treatment.
- Independent acceptance: browser fixtures render every typestate without action controls.
- Validation: focused desktop/mobile lifecycle Playwright cases.
- Owner: `local-fallback`.
- Split analysis: one SWU per stage would not prove ordered lifecycle comprehension; stages are fixtures of one renderer.
- Handoff: consume `RunView`; do not rederive kernel state in DOM code.

## SWU-WUI-007: Legal Primary Action

- Primary decision: expose one legal primary action for each `RunView` state.
- Dependencies: `SWU-WUI-005`.
- Source anchors: existing approve, make-available, interrupt, release, and receipt actions.
- Related context: destructive alternatives belong in a secondary menu.
- Write scope: action resolver, controls, and action matrix tests.
- Done criteria: no state shows an illegal or premature completion action; secondary destructive actions remain reachable.
- Independent acceptance: action matrix and one end-to-end journey pass without timeline assertions.
- Validation: focused action tests plus `npm run test:bridge`.
- Owner: `local-fallback`.
- Split analysis: primary selection and secondary overflow together enforce one legal-action policy.
- Handoff: derive actions only from `RunView`; preserve ready-only secrecy.

## Synchronization

- `SWU-WUI-005`: completed on 2026-07-20 with
  [PASS evidence](../../task-sessions/20260720T161925Z-swu-wui-005/TASK-SESSION-RESULT.md).
- `SWU-WUI-006`: completed on 2026-07-20 with
  [PASS evidence](../../task-sessions/20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md).
- `SWU-WUI-007`: completed on 2026-07-20 with
  [PASS evidence](../../task-sessions/20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md).
- `TASK-WUI-003`: completed for RunView projection, ordered timeline, and legal
  action projection.
- `SWU-WUI-008`: now owns the next mutation-capable handle in the workspace
  task; it remains sequenced after the lifecycle task.
- `SWU-WUI-009` through `SWU-WUI-011`: remain planned behind workspace and
  evidence dependencies.
