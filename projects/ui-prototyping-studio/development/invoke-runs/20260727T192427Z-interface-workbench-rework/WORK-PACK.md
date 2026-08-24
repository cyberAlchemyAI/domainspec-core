---
module: ui-prototyping-studio-interface-workbench
version: current
status: plan-distill-block
updatedAt: 2026-07-28
docType: work-pack
---

# WORK-PACK: Interface Workbench Rework

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block | Fresh governed Plan Distill found four MAJOR and two MINOR change requests. |
| complexity | medium | Six tasks and 19 candidate mutation SWUs; 016, 017, and 019 are task-shaped and cannot hand off. |
| outputMode | split | Required by complexity. |
| executionPackRef | `EXECUTION-PACK.md` | Cross-task choreography only. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0–L3 decisions. |
| swuManifestRef | `SWU-MANIFEST.json` | SWU identity, semantic dependencies, serialization order. |
| scopeInventoryRef | `SWU-SCOPE-INVENTORY.json` | Exhaustive implementation mutation authority. |
| acceptanceMatrixRef | `SWU-ACCEPTANCE-MATRIX.json` | Inverse SWU→Design→assertion ownership. |
| closeoutInventoryRef | `CLOSEOUT-SYNC-INVENTORY.json` | Exact receipt/Plan synchronization contracts. |
| distillValidationStatus | block | Verified findings: `plan-redistill-review/findings.md`. |
| swuAtomicityStatus | block-task-shaped-3 | 016, 017, and 019 require independently receipted child units. |
| firstUnitNarrownessStatus | recommendation-only | SWU-UPW-001 remains narrowest; it is not selected. |
| closeoutSyncStatus | block | Field permissions are not literally addressable and W5 lacks an executable schema/decision contract. |
| activeLayerWindow | L0 | Planning focus only. |
| selectedSWU | none | No mutation is authorized. |
| readinessProfile | pilot | Human/release evidence remains outside scope. |

## Objective And Authority

Deliver the passing Design as a coherent, stable, no-build Studio workbench
through one-behavior SWUs. Success requires exact UPW evidence and current
regression; it does not imply human comprehension, accessibility certification,
release, deployment, or production readiness.

Invoke owns this Plan. Task Session owns later selected-SWU execution. Invoke
Refresh owns receipt synchronization. The human/lifecycle owner alone selects
an SWU. No current field authorizes product mutation.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Validation |
| --- | --- | --- | --- | --- |
| S-001 | deterministic coherent versioned projection | L0 | [W0](work-pack/waves/W0.md) | unit + projection E2E |
| S-002 | inert/action-fresh shell, typed context plan, atomic commit | L0 | [W1](work-pack/waves/W1.md) | continuity unit/E2E |
| S-003 | six independently accepted regions | L1 | [W2](work-pack/waves/W2.md) | exact region assertions |
| S-004 | mobile semantic order and state copy | L1 | [W3](work-pack/waves/W3.md) | responsive/copy E2E |
| S-005 | interaction, visual, route, and rendering hardening | L2 | [W4](work-pack/waves/W4.md) | bounded a11y/security tests |
| S-006 | full closure and residue audit | L2 | [W5](work-pack/waves/W5.md) | exact closure JSON + full suite |

## Task Status Board

| Task | Layer/wave | SWUs | Status |
| --- | --- | --- | --- |
| [TASK-UPW-PROJECTION](work-pack/tasks/TASK-UPW-PROJECTION.md) | L0/W0 | 001–003 | not-started |
| [TASK-UPW-COORDINATOR](work-pack/tasks/TASK-UPW-COORDINATOR.md) | L0/W1 | 004–007 | not-started |
| [TASK-UPW-REGIONS](work-pack/tasks/TASK-UPW-REGIONS.md) | L1/W2 | 008–013 | not-started |
| [TASK-UPW-RESPONSIVE-COPY](work-pack/tasks/TASK-UPW-RESPONSIVE-COPY.md) | L1/W3 | 014–015 | not-started |
| [TASK-UPW-HARDENING](work-pack/tasks/TASK-UPW-HARDENING.md) | L2/W4 | 016–019 | not-started |
| [TASK-UPW-VERIFY](work-pack/tasks/TASK-UPW-VERIFY.md) | L2/W5 | closure-only exemption | not-started |

## Candidate SWU Navigation And Atomicity

The current machine rows are a mechanically coherent candidate, not an
execution-ready manifest. Exact algorithms live in the linked task files.
Fresh Distill invalidated the retained boundaries for 016, 017, and 019.

| SWU | One primary behavior | Independent acceptance | Retained boundary |
| --- | --- | --- | --- |
| 001 | canonical projection digests | `UPW_A_001_DIGEST` | serializer/hash jointly create identity |
| 002 | coherent store-token snapshot | `UPW_A_002_COHERENCE` | before/read/after equality is one invariant |
| 003 | versioned existing-route `/state` | `UPW_A_003_STATE` | integration and endpoint form one contract |
| 004 | inert stable shell | `UPW_A_004_INERT` | mount without inertness leaves defect open |
| 005 | action trailing refresh | `UPW_A_005_TRAILING` | slot and action wait close one freshness behavior |
| 006 | pure typed context plan | `UPW_A_006_CONTEXT_PLAN` | preserve/invalidate are one total decision |
| 007 | atomic region/context commit | `UPW_A_007_ATOMIC_COMMIT` | journal/commit/rollback close together |
| 008 | lifecycle spine | `UPW_A_008_SPINE` | identity/next-action summary |
| 009 | current canvas | `UPW_A_009_CANVAS` | one current-head surface |
| 010 | contextual inspector | `UPW_A_010_INSPECTOR` | one state-to-context mapping |
| 011 | staged review | `UPW_A_011_REVIEW` | one evidence/comparison surface |
| 012 | governed actions | `UPW_A_012_ACTIONS` | transport/gates/state-owned feedback |
| 013 | historical lineage | `UPW_A_013_HISTORY` | one secondary reference surface |
| 014 | mobile semantic order | `UPW_A_014_RESPONSIVE` | width/order/overflow are one behavior |
| 015 | state/action copy | `UPW_A_015_COPY` | one literal language matrix |
| 016 | interaction/focus/live/status | `UPW_A_016_INTERACTION` | one event/focus/feedback outcome |
| 017 | visual perceivability/targets | `UPW_A_017_VISUAL` | one calibrated style/geometry outcome |
| 018 | server route admission | `UPW_A_018_ROUTES` | parse/family check decide one admission |
| 019 | sandbox/safe rendering | `UPW_A_019_RENDERING` | one browser-render admission |

## Dependency Meaning

`SWU-MANIFEST.json` intentionally separates:

- `dependencies`: behavioral evidence required for a SWU to pass;
- `serialization_after`: safe one-at-a-time order caused by overlapping files
  or current selection policy, not a behavioral input; and
- `successor`: the deterministic next candidate after synchronized closeout,
  never automatic selection.

Important repairs:

- SWU-003 consumes only current internal route constructors; arbitrary/new
  route admission is SWU-018.
- SWU-006 is a pure typed planner. SWU-007 alone journals and commits region
  plus context state.
- W2 regions share a semantic baseline (007) but are serialized due overlapping
  projection/shell/spec writes.
- 018 follows 017 only for candidate order; it semantically depends on 003.

## Exact Scope, Acceptance, And Closeout

### Mutation authority

`SWU-SCOPE-INVENTORY.json` lists every repo-relative existing and
create-if-absent implementation target per SWU, protected paths, and the rule
that all omitted paths are unauthorized. Task Session hashes every exact
existing target and binds every future path to `ABSENT` before mutation.

### Acceptance

`SWU-ACCEPTANCE-MATRIX.json` gives every SWU an exact spec, grep/selector or test
name, positive assertion, negative mutant, Design refs, primary owner, and
receipt field. Assertions 008–013 are direct; shared witness rows are
recomposition/regression evidence and never create a second primary owner.

### Task Session closeout

`CLOSEOUT-SYNC-INVENTORY.json` gives each of the 19 SWUs:

- exact `WORK-PACK.md`, manifest, task, wave, `EXECUTION-PACK.md`, and
  `PLAN-TRANSPORT.md` targets;
- exact execution and refresh receipt paths/schemas;
- baseline binding, admitted delta classes, writable/forbidden fields, owner
  validation, and deterministic successor effect.

W5 writes only
`closure-reports/interface-workbench-closure.json` using
`ui-prototyping-studio.interface-workbench-closure.v1` and the exact inventory
in that artifact.

## Validation Strategy

Every selected SWU must:

1. pass scope preflight;
2. pass its exact focused positive and negative assertion;
3. return `task-session.swu-result.v1`;
4. synchronize through `invoke:refresh:apply-approved`;
5. receive `invoke.refresh.v1`; and
6. leave the successor unselected.

Full commands and slice gates are in `PLAN-VALIDATION-STRATEGY.md`. Planned
witnesses remain unexecuted evidence.

## Blockers And Gaps

| ID | Scope | Owner | Effect |
| --- | --- | --- | --- |
| B-PLAN-REDISTILL | Plan admission | Invoke Plan | apply verified findings, regenerate the Plan, then obtain a fresh literal-byte Distill pass |
| B-SWU-ATOMICITY | Plan admission | Invoke Plan | split 016, 017, and 019 and regenerate every affected denominator |
| B-CLOSEOUT-CONTRACT | Plan admission | Invoke Plan | materialize addressable closeout selectors/schemas and deterministic W5 validation |
| B-SWU-SELECTION | mutation admission only | human/lifecycle owner | choose one exact SWU after Plan pass |

Non-blocking deferred scope is in
`work-pack/shared/cross-task-gaps.md`.

## Current Route

1. Obtain explicit authorization for a new Invoke Plan remediation.
2. Apply the ordered change requests in
   `plan-redistill-review/findings.md`.
3. Regenerate and mechanically validate the affected Plan denominators.
4. Run a new governed Plan Distill over the exact changed bytes.
5. Only after a pass may the human select one SWU and Task Session preflight it.

Current next owner: **deferred Invoke Plan remediation**. Task Session remains
blocked.
