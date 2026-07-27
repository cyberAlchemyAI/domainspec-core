---
id: ui-prototyping-studio-governed-state-projection-amended-work-pack
project: ui-prototyping-studio
docType: work-pack
invoke_run: invoke-20260727T042935Z-architecture-review-refresh
status: active
selectedSWU: SWU-GSP-001
updatedAt: 2026-07-27T04:29:35Z
---

# WORK-PACK: Governed State Projection — Amended Execution

## Authority Boundary

- `.craft/ledger.yml` owns scoped lifecycle state.
- The accepted 2026-07-27 architecture review owns the verified change-request
  input, not implementation truth.
- This amended work-pack is the owner-approved execution contract.
- Task Session receipts and current code bytes own implementation evidence.
- Human-study conclusions and release authorization are separate and unbound.
- The 2026-07-10 package is retained as historical proposal evidence.

## Objective

Make preview, annotation, diff, reversible actions, browser evidence, and
handoff readiness project one coherent governed state without claiming
release readiness.

Implementation completion requires all seven SWUs to pass against current
bytes. It does not imply human ergonomics proof or release authorization.

## Execution Board

| Task | SWU | Primary behavior | Dependencies | Status |
| --- | --- | --- | --- | --- |
| [TASK-GSP-001](work-pack/tasks/TASK-GSP-001-evidence-harness.md) | `SWU-GSP-001` | Deterministic, fail-fast browser evidence startup. | none | selected |
| [TASK-GSP-002](work-pack/tasks/TASK-GSP-002-store-freshness.md) | `SWU-GSP-002` | Every read observes current persisted session state. | `SWU-GSP-001` | blocked-by-dependency |
| [TASK-GSP-003](work-pack/tasks/TASK-GSP-003-current-head-projection.md) | `SWU-GSP-003` | Application-owned current-head preview and annotation projection. | `SWU-GSP-002` | blocked-by-dependency |
| [TASK-GSP-004](work-pack/tasks/TASK-GSP-004-visible-change-diff.md) | `SWU-GSP-004` | Style/global changes always produce explicit evidence. | `SWU-GSP-003` | blocked-by-dependency |
| [TASK-GSP-005](work-pack/tasks/TASK-GSP-005-action-annotation-mobile.md) | `SWU-GSP-005` | Actor-neutral confirmation and inspectable annotation/mobile flow. | `SWU-GSP-003` | blocked-by-dependency |
| [TASK-GSP-006](work-pack/tasks/TASK-GSP-006-handoff-readiness.md) | `SWU-GSP-006` | Export, completeness, integration, and implementation readiness remain distinct. | `SWU-GSP-001` | blocked-by-dependency |
| [TASK-GSP-007](work-pack/tasks/TASK-GSP-007-docs-craft-closeout.md) | `SWU-GSP-007` | Current docs and Craft reflect only current receipts. | `SWU-GSP-001..006` | blocked-by-dependency |

There is exactly one selected unit: `SWU-GSP-001`.

## SWU Manifest

| SWU | Write scope | Acceptance evidence | Verification |
| --- | --- | --- | --- |
| `SWU-GSP-001` | `backend/e2e/helpers.ts`; helper-focused tests if needed | Standard Playwright command starts locally, preserves launch diagnostics, and fails promptly on premature exit. | `cd backend && ./node_modules/.bin/playwright test --reporter=list` |
| `SWU-GSP-002` | `file-studio-session-store.ts`; store tests | A second process writes Accept/Revert/stage state and an existing reader observes it without restart. | unit/slice plus independent-process probe |
| `SWU-GSP-003` | new application projection module; `studio.ts`; focused tests/e2e | Current head is primary; annotation uses the same head/revision; variants are labeled history. | typecheck, unit, focused Playwright |
| `SWU-GSP-004` | admission/diff model; preview/handoff consumers; tests | CSS-only change cannot produce silent zero evidence; style/global/unattributed lane is explicit. | unit plus focused Playwright |
| `SWU-GSP-005` | `studio.ts`; focused e2e | Accept/Revert require actor-neutral acknowledgment; blank annotation target is unavailable; 390px comparison is inspectable. | focused desktop/mobile Playwright |
| `SWU-GSP-006` | handoff domain/use case/tests | Missing refs make `evidenceComplete=false`; export confirmation never alone sets integration or implementation ready. | unit/slice regression |
| `SWU-GSP-007` | root active docs, Craft ledger/view, closeout receipts | Counts, state, proof boundaries, selected/completed SWUs, and next move match current receipts. | grep review, Craft validation, full suite |

## Layering

| Layer | SWUs | Question answered |
| --- | --- | --- |
| L0 evidence floor | 001 | Can every later browser claim use one checked-in deterministic route? |
| L1 state truth | 002–003 | Does the browser project current persisted governed state? |
| L2 trust evidence | 004–006 | Are visible change, durable actions, and handoff claims honest? |
| L3 closeout | 007 | Do active docs and Craft match the receipts without claiming release? |

The optional Open Design evidence-profile expansion is not part of this
completion graph. It may be reconsidered only after this work-pack closes.

## Global Validation

```sh
cd projects/ui-prototyping-studio/backend
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test --reporter=list
```

The completion audit must additionally run an independent-process freshness
witness and inspect the 390px staged comparison.

## Distill Result

Skipped with a recorded rationale in `DISTILL-VALIDATION.md`. The accepted
review already decomposed the implementation into independent defects; this
amendment narrows the mixed historical tasks into seven one-behavior units.

## Gaps Preserved

- human-study ergonomics proof;
- release owner and release authorization;
- broader Open Design evidence/profile integration;
- historical L4–L6 deep-spec ambitions outside the accepted review.

## Next Route

Run Task Session on selected `SWU-GSP-001`. Do not execute another SWU until
its declared dependencies have passing receipts and Craft selects it.
