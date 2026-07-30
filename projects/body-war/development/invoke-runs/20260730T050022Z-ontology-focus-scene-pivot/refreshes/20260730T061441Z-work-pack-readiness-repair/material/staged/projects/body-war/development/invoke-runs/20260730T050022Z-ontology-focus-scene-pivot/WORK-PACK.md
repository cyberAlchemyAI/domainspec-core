---
module: body-war-ontology-focus-scene-pivot
version: current
status: blocked-runtime-admission
updatedAt: 2026-07-30
docType: work-pack
---

# Work Pack — Body War Ontology Focus Scene And Portal Pivot

## Control Fields

| Field | Value |
| --- | --- |
| `workPackGateStatus` | `block-runtime-admission` |
| `complexity` | `high` |
| `outputMode` | `split` |
| `executionPackRef` | `EXECUTION-PACK.md` |
| `layeringArtifactRef` | `IMPLEMENTATION-LAYERING.md` |
| `dispatchTechniqueTrace` | `DISPATCH-TRACE.md` |
| `distillValidationStatus` | `pass` |
| `swuAtomicityStatus` | `pass-after-splits` |
| `firstUnitNarrownessStatus` | `pass` |
| `closeoutSyncStatus` | `pass-plan-contract` |
| `activeLayerWindow` | `L0` |
| `readinessProfile` | `pilot` |
| `selected_swu` | `none` |
| `first_selectable_swu` | `none` |
| `first_planned_swu` | `SWU-OFSP-001` |

`workPackGateStatus: block-runtime-admission` means the refreshed plan
contract is complete, but no SWU may be selected or executed. Material SWUs
lack current material-package admission, and output-only/audit-only units have
no truthful live Task Session mutation mode.

## Objective And Boundary

Deliver a deterministic browser-testable local prototype in which the native
Body War ontology viewer renders one source-derived scene, pivots atomically
through exact relations, preserves provenance/authority, and supports pointer,
keyboard, forced-colors, and reduced-motion operation.

Excluded: ontology/adapter semantic mutation, direct archive/bundle edits, new
package roots/Playwright dependencies, upstream publication, deployment,
release, production, and comprehension claims.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Validation |
| --- | --- | --- | --- | --- |
| S-FOUND | oracle + successor overlay/build tooling | L0 | W0 | independent fixture/overlay/materializer/verifier readiness receipts |
| S-L0-CORE | exact tuple, four-node projection, atomic portal state | L0 | W1 | unit and canonical-state checks |
| S-L0-UI | native bounded renderer, landmark, controls, focus/motion, verified build/browser | L0 | W1 | exact build/browser receipts |
| S-L1 | one-hop, tour reducer/bridge, literal/forced-colors repeatability | L1 | W2 | verified build then separate browser regression |
| S-L2 | pure and rendered degraded behavior + audits | L2 | W3 | negative fixtures and three closure receipts |
| S-L3 | reproducible local handoff | L3 | W3 | clean reproduction receipt |

## Task Board

| Task | Layers | Gate | Status |
| --- | --- | --- | --- |
| [FOUNDATION](work-pack/tasks/TASK-FOUNDATION.md) | L0 | ready | not-started |
| [PROJECTION](work-pack/tasks/TASK-PROJECTION.md) | L0/L1 | dependency-gated | not-started |
| [STATE](work-pack/tasks/TASK-STATE.md) | L0/L1 | dependency-gated | not-started |
| [NATIVE-UI](work-pack/tasks/TASK-NATIVE-UI.md) | L0/L1 | dependency-gated | not-started |
| [ACCEPTANCE](work-pack/tasks/TASK-ACCEPTANCE.md) | L0/L1 | dependency-gated | not-started |
| [RELIABILITY](work-pack/tasks/TASK-RELIABILITY.md) | L2 | L1-gated | not-started |
| `TASK-VERIFY` | L2 closure | after 025 | not-started |
| `TASK-AUDIT-ALIGNMENT` | L2 closure | after VERIFY | not-started |
| `TASK-AUDIT-LAYERING` | L2 closure | after alignment | not-started |
| [PACKAGE](work-pack/tasks/TASK-PACKAGE.md) | L3 | after all audits | not-started |

## Ordered SWU Manifest

| Order | SWU | Parent | One behavior | Depends on | Layer |
| --- | --- | --- | --- | --- | --- |
| 1 | 001 | FOUNDATION | derive independent oracle | none | L0 |
| 2 | 002 | FOUNDATION | admit successor overlay | 001 | L0 |
| 3 | 003 | FOUNDATION | author isolated materializer | 002 | L0 |
| 4 | 004 | FOUNDATION | author independent handle verifier | 003 | L0 |
| 5 | 005 | PROJECTION | join exact source literals | 001,004 | L0 |
| 6 | 006 | PROJECTION | project exact tour scene | 005 | L0 |
| 7 | 007 | STATE | commit focus/internal selection | 006 | L0 |
| 8 | 008 | STATE | commit portal/Back | 007 | L0 |
| 9 | 009 | NATIVE-UI | bridge native store | 004,008 | L0 |
| 10 | 010 | NATIVE-UI | render bounded scene/portals | 009 | L0 |
| 11 | 011 | NATIVE-UI | add landmark/focus transfer | 010 | L0 |
| 12 | 012 | NATIVE-UI | make relation controls input-equivalent | 011 | L0 |
| 13 | 013 | NATIVE-UI | add visible focus/reduced motion | 012 | L0 |
| 14 | 014 | ACCEPTANCE | produce/verify L0 build | 013 | L0 |
| 15 | 015 | ACCEPTANCE | implement browser validator | 014 | L0 |
| 16 | 016 | ACCEPTANCE | execute L0 browser acceptance | 015 | L0 |
| 17 | 017 | PROJECTION | project non-tour one-hop | 016 | L1 |
| 18 | 018 | STATE | implement pure tour lifecycle | 017 | L1 |
| 19 | 019 | STATE | bridge native tour controls | 018 | L1 |
| 20 | 020 | NATIVE-UI | integrate literals across surfaces | 019 | L1 |
| 21 | 021 | NATIVE-UI | add forced-colors redundancy | 020 | L1 |
| 22 | 022 | ACCEPTANCE | produce/verify L1 build | 021 | L1 |
| 23 | 023 | ACCEPTANCE | execute L1 browser regression | 022 | L1 |
| 24 | 024 | RELIABILITY | enforce pure degraded policy | 023 | L2 |
| 25 | 025 | RELIABILITY | render degraded recovery | 024 | L2 |
| 26 | 026 | PACKAGE | package local prototype | 025 + three closure tasks | L3 |

Every numeric ID expands to `SWU-OFSP-NNN`. `001` is the only currently
dependency-ready unit and remains unselected.

## Atomicity Review

| Units | Independent boundary | Split decision | Verdict |
| --- | --- | --- | --- |
| 001–010 | oracle, admission, tooling, tuple, projection, reducer, store, renderer each have their own tests/receipts | retained as authored | pass |
| 011 | landmark/skip/post-commit focus | split from controls and style/motion | pass |
| 012 | pointer/Enter/Space relation-control parity | split from focus destination and CSS/motion | pass |
| 013 | focus geometry/reduced-motion presentation | split from semantic operation | pass |
| 014–017 | build, validator, browser attempt, one-hop each have separate evidence | retained/separated | pass |
| 018 | pure tour protocol | split from LearnPanel | pass |
| 019 | native tour bridge/announcements | split from reducer | pass |
| 020 | source literals across surfaces | split from forced-colors visual redundancy | pass |
| 021 | forced-colors redundancy | split from literal integration | pass |
| 022 | verified L1 build | split from browser regression | pass |
| 023 | immutable L1 browser regression | split from build | pass |
| 024 | pure degraded policy | split from rendered recovery | pass |
| 025 | degraded UI/browser recovery | split from selector/reducer | pass |
| 026 | local manifest/guide/reproduction contract | upstream/release/research remain separate | pass |

Atomicity-only result: `0 of 26` task-shaped. This does not imply
command, receipt, closeout, or runtime readiness.

## Exact Execution Handoff

Each task file gives complete repository-relative write paths, acceptance,
validation, split analysis, and dependencies. Common sources:

- [execution context](work-pack/shared/CONTEXT.md);
- [traceability](work-pack/shared/TRACEABILITY.md);
- [gap ledger](work-pack/shared/CROSS-TASK-GAPS.md);
- [closeout chain](work-pack/shared/CLOSEOUT-CONTRACT.md);
- [closure task contracts](work-pack/tasks/TASK-CLOSURE.md);
- [exact command matrix](work-pack/shared/COMMAND-MATRIX.json);
- hardened `TASK-SESSION-RECEIPT.schema.json` plus semantic validator
  `work-pack/shared/validate-task-session-receipt.py`.

Context Builder generates a Task Session pack only after explicit selection.
Invoke does not pre-generate it.

## Evidence And Receipt Separation

- 003/004 produce Task Session tooling-readiness receipts only.
- 014 produces and independently verifies the first immutable build handle.
- 015 authors the validator.
- 016 executes the first immutable browser attempt.
- L1 repeats build/browser separation in 022/023.
- generated attempts are new directories and never source.

## Blockers And Deferrals

- Plan-contract gaps found by the readiness audit are repaired and must be
  rechecked by the post-refresh audit.
- Runtime admission remains blocked for all 29 units: material SWUs need current
  exact material packages, while output-only and audit-only tasks need a
  truthful Task Session execution mode owned by the Task Session lifecycle.
- Native feature source remains blocked until 002–004 pass.
- Deliberately deferred: human comprehension, optional rotation, upstream
  publication, deployment, release, production.

## Technique And Distill State

Dispatch technique trace: `DISPATCH-TRACE.md`; validated dispatch:
`EXECUTION-DISPATCH.json`.

Proposer repairs applied after Balancer block:

- split five task-shaped units into eleven atomic units;
- normalized exact write scopes and patch ordering;
- defined test-only fixture transport;
- selected presentation graph as runtime literal authority;
- made W0 evidence tooling-readiness only;
- normalized Task Session/Dispatch/Refresh receipt schema;
- inserted exact closure audit receipts into successor chain;
- repaired traceability and navigation.

Distill atomicity recheck passed with `0 of 26` task-shaped units. The
later full-frontier readiness audit correctly blocked selection and supersedes
any broader readiness inference.

## Gate Result

- Design prerequisite: pass
- plan authored/repaired: pass pending post-refresh audit
- plan evidence: pending
- runtime admission: block
- selected SWU: none
- implementation authority: not granted
- next route: rerun `work-pack-readiness-audit`; then route Task Session
  task-class admission to `sigil-development` and build a material package for
  the first explicitly selected material SWU
