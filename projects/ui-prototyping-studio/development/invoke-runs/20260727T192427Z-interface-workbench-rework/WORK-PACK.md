---
module: ui-prototyping-studio-interface-workbench
version: current
status: draft-pending-plan-distill
updatedAt: 2026-07-27
docType: work-pack
---

# WORK-PACK: Interface Workbench Rework

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block | Plan Distill and explicit SWU selection remain open. |
| complexity | medium | Six tasks, 17 mutation SWUs, split waves/tasks. |
| outputMode | split | Required by complexity. |
| executionPackRef | `EXECUTION-PACK.md` | Wave choreography only. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0–L3 governance. |
| swuManifestRef | `SWU-MANIFEST.json` | Machine identity/dependencies. |
| dispatchTechniqueTrace | `PLAN-TECHNIQUE-TRACE.md` | Pass for draft; Plan Distill dispatch pending. |
| distillValidationStatus | block | Not yet run. |
| swuAtomicityStatus | block | Draft analysis complete; independent validation pending. |
| firstUnitNarrownessStatus | block | SWU-UPW-001 is recommended; Plan Distill pending. |
| closeoutSyncStatus | pass | Every mutation SWU has a complete row below. |
| activeLayerWindow | L0 | Planning focus only. |
| selectedSWU | none | No mutation is authorized. |
| lastUpdatedAt | 2026-07-27 | Plan authoring date. |
| readinessProfile | pilot | Release is outside scope. |

## Objective

Deliver the passing Design as a coherent, stable, no-build Studio workbench
through serial one-behavior SWUs. Success requires exact UPW evidence and full
current regression, not visual completion alone.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | coherent versioned projection | L0 | [W0](work-pack/waves/W0.md) | none | unit + projection E2E |
| S-002 | stable, action-fresh, recoverable continuity | L0 | [W1](work-pack/waves/W1.md) | S-001 | continuity E2E |
| S-003 | six-region governed surface | L1 | [W2](work-pack/waves/W2.md) | S-002 | region/state E2E |
| S-004 | mobile semantic order and state copy | L1 | [W3](work-pack/waves/W3.md) | S-003 | responsive/copy E2E |
| S-005 | bounded semantics and security | L2 | [W4](work-pack/waves/W4.md) | S-004 | a11y/security E2E |
| S-006 | full closure and residue audit | L2 | [W5](work-pack/waves/W5.md) | S-005 | full current suite |

## Task Status Board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-UPW-PROJECTION](work-pack/tasks/TASK-UPW-PROJECTION.md) | deterministic coherent versioned projection | L0 | W0 | blocked on Plan Distill/selection | not-started |
| [TASK-UPW-COORDINATOR](work-pack/tasks/TASK-UPW-COORDINATOR.md) | inert, action-fresh, rollback-capable continuity | L0 | W1 | blocked on W0 | not-started |
| [TASK-UPW-REGIONS](work-pack/tasks/TASK-UPW-REGIONS.md) | six independent workbench regions | L1 | W2 | blocked on W1 | not-started |
| [TASK-UPW-RESPONSIVE-COPY](work-pack/tasks/TASK-UPW-RESPONSIVE-COPY.md) | mobile order and domain-faithful copy | L1 | W3 | blocked on W2 | not-started |
| [TASK-UPW-HARDENING](work-pack/tasks/TASK-UPW-HARDENING.md) | bounded semantics and frame/route security | L2 | W4 | blocked on W3 | not-started |
| [TASK-UPW-VERIFY](work-pack/tasks/TASK-UPW-VERIFY.md) | closure-only verification | L2 | W5 | blocked on W4 | not-started |

## SWU Atomicity Review

| SWU | Primary behavior | Candidate child units | Retained-boundary rationale | Draft verdict |
| --- | --- | --- | --- | --- |
| SWU-UPW-001 | canonical whole/region digests | serializer; hasher | neither independently proves projection identity | pass |
| SWU-UPW-002 | coherent snapshot | epoch read; input assembly; retry | coherence is the joint before/after invariant | pass |
| SWU-UPW-003 | versioned `/state` | projection integration; HTTP exposure | one observable compatibility contract | pass |
| SWU-UPW-004 | stable inert polling | shell mount; same-version gate | mounted shell without inertness leaves defect open | pass |
| SWU-UPW-005 | action trailing refresh | queue flag; action await | either alone can remain stale | pass |
| SWU-UPW-006 | recoverable keyed commit | prepare; journal; rollback | partial pieces cannot guarantee failure atomicity | pass |
| SWU-UPW-007 | local-context reconciliation | preserve; invalidate | two outcomes of one identity decision | pass |
| SWU-UPW-008 | lifecycle spine | state label; next action | one summary contract | pass |
| SWU-UPW-009 | current canvas | label; frame identity | one current-head surface | pass |
| SWU-UPW-010 | contextual inspector | annotation; batch; receipt states | one state-selected context surface | pass |
| SWU-UPW-011 | staged review | diff; frames; ack context | one review-evidence surface; action transport split to 012 | pass |
| SWU-UPW-012 | governed actions | handlers; feedback scopes | one action/receipt behavior | pass |
| SWU-UPW-013 | historical lineage | collapse; labels; expansion continuity | one secondary-reference surface | pass |
| SWU-UPW-014 | mobile semantic order | width; order; overflow | one responsive behavior after regions exist | pass |
| SWU-UPW-015 | state copy matrix | browser language; CLI disclosure | one domain-language decision | pass |
| SWU-UPW-016 | bounded interaction semantics | keyboard; focus; live; color | one input/feedback semantic contract | pass |
| SWU-UPW-017 | frame/route security | route validation; sandbox render | jointly enforce one browser content boundary | pass |

Independent Plan Distill must validate these draft verdicts before the control
field changes to pass.

## SWU Execution Handoff

| SWU | Parent task | Source anchors | Dependencies | Write scope | Done/evidence | Validation | Owner | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 001 | [PROJECTION](work-pack/tasks/TASK-UPW-PROJECTION.md) | Architecture canonical JSON; UPW-FIX-001/019 | none | `application/workbench-projection-version.ts` + test | golden vectors and mutants | focused `tsx --test` | subagent | candidate; not selected |
| 002 | [PROJECTION](work-pack/tasks/TASK-UPW-PROJECTION.md) | DDR-01; snapshot algorithm | 001 | `application/workbench-projection-snapshot.ts` + test | torn reads never emit | focused `tsx --test` | subagent | blocked on 001 |
| 003 | [PROJECTION](work-pack/tasks/TASK-UPW-PROJECTION.md) | `/state`; projection builder | 002 | projection source/test, `studio.ts`, projection E2E | version/compatibility coherence | unit + focused Playwright | subagent | blocked on 002 |
| 004 | [COORDINATOR](work-pack/tasks/TASK-UPW-COORDINATOR.md) | pollScript; UPW-FIX-002 | 003 | `studio.ts`, workbench shell, continuity E2E | zero unchanged nav/patch | focused Playwright | subagent | blocked on 003 |
| 005 | [COORDINATOR](work-pack/tasks/TASK-UPW-COORDINATOR.md) | actScript; DDR-03 | 004 | coordinator/shell + race E2E | one trailing fetch/apply | focused Playwright | subagent | blocked on 004 |
| 006 | [COORDINATOR](work-pack/tasks/TASK-UPW-COORDINATOR.md) | DDR-02; failure contract | 005 | coordinator/shell + failure E2E | rollback mounts/context/versions | focused Playwright | subagent | blocked on 005 |
| 007 | [COORDINATOR](work-pack/tasks/TASK-UPW-COORDINATOR.md) | Context Reconciler; UPW-FIX-003/006 | 006 | context/shell + continuity E2E | preserve valid/reset stale only | focused Playwright | subagent | blocked on 006 |
| 008 | [REGIONS](work-pack/tasks/TASK-UPW-REGIONS.md) | UX lifecycle spine | 007 | shell/projection + state E2E | exact state/next action | focused Playwright | subagent | blocked on 007 |
| 009 | [REGIONS](work-pack/tasks/TASK-UPW-REGIONS.md) | UX active canvas | 008 | shell/projection + canvas E2E | stable current frame | focused Playwright | subagent | blocked on 008 |
| 010 | [REGIONS](work-pack/tasks/TASK-UPW-REGIONS.md) | UX inspector | 009 | shell/projection + annotation E2E | exact state context | focused Playwright | subagent | blocked on 009 |
| 011 | [REGIONS](work-pack/tasks/TASK-UPW-REGIONS.md) | UX staged review | 010 | shell/projection + review E2E | diff/named frames/ack | focused Playwright | subagent | blocked on 010 |
| 012 | [REGIONS](work-pack/tasks/TASK-UPW-REGIONS.md) | action routes/live scopes | 011 | shell/actions + action E2E | gates and exact status scopes | focused Playwright | subagent | blocked on 011 |
| 013 | [REGIONS](work-pack/tasks/TASK-UPW-REGIONS.md) | UX lineage | 012 | shell/history + state E2E | collapsed non-current history | focused Playwright | subagent | blocked on 012 |
| 014 | [RESPONSIVE](work-pack/tasks/TASK-UPW-RESPONSIVE-COPY.md) | responsive contract | 013 | shell styles + mobile E2E | 390px order/no overflow | focused Playwright | subagent | blocked on 013 |
| 015 | [COPY](work-pack/tasks/TASK-UPW-RESPONSIVE-COPY.md) | FR-14/content rules | 014 | labels/copy + copy E2E | state/copy matrix | focused Playwright | subagent | blocked on 014 |
| 016 | [HARDENING](work-pack/tasks/TASK-UPW-HARDENING.md) | accessibility contract | 015 | shell/status + a11y E2E | keyboard/focus/live/color checks | focused Playwright | subagent | blocked on 015 |
| 017 | [HARDENING](work-pack/tasks/TASK-UPW-HARDENING.md) | security contract | 016 | route validation/shell + security tests | sandbox/allowlist mutants fail | unit + focused Playwright | subagent | blocked on 016 |

Each task file supplies the exact algorithm, edge cases, split analysis, and
handoff context. IDs above abbreviate the `SWU-UPW-*` prefix only in this table.

## Task Session Closeout Sync Contract

Common contract for every row:

- lifecycle owner route: `invoke:refresh:apply-approved`;
- terminal source receipt:
  `execution-receipts/<SWU-ID>.json`, schema `task-session.swu-result.v1`;
- baseline: SHA-256 of each declared target at Task Session preflight; a future
  receipt path is admitted only as explicitly absent;
- allowed planning deltas: `evidence_added`, `blocker_opened`,
  `blocker_resolved`, `status_changed`, `route_changed`;
- owner validation: receipt parses, SWU ID appears exactly once in manifest,
  task, and wave, dependencies remain satisfied, and source validation named
  by the task passed;
- expected owner receipt:
  `refresh-receipts/<SWU-ID>.json`, schema `invoke.refresh.v1`;
- the successor becomes a candidate only when dependency-ready and is never
  auto-selected.

| SWU | Declared target inventory | Deterministic successor |
| --- | --- | --- |
| SWU-UPW-001 | `WORK-PACK.md`; `SWU-MANIFEST.json`; `work-pack/tasks/TASK-UPW-PROJECTION.md`; `work-pack/waves/W0.md`; `execution-receipts/SWU-UPW-001.json` | SWU-UPW-002 |
| SWU-UPW-002 | same control/manifest; PROJECTION task; W0; `execution-receipts/SWU-UPW-002.json` | SWU-UPW-003 |
| SWU-UPW-003 | same control/manifest; PROJECTION task; W0; `execution-receipts/SWU-UPW-003.json` | SWU-UPW-004 |
| SWU-UPW-004 | same control/manifest; COORDINATOR task; W1; `execution-receipts/SWU-UPW-004.json` | SWU-UPW-005 |
| SWU-UPW-005 | same control/manifest; COORDINATOR task; W1; `execution-receipts/SWU-UPW-005.json` | SWU-UPW-006 |
| SWU-UPW-006 | same control/manifest; COORDINATOR task; W1; `execution-receipts/SWU-UPW-006.json` | SWU-UPW-007 |
| SWU-UPW-007 | same control/manifest; COORDINATOR task; W1; `execution-receipts/SWU-UPW-007.json` | SWU-UPW-008 |
| SWU-UPW-008 | same control/manifest; REGIONS task; W2; `execution-receipts/SWU-UPW-008.json` | SWU-UPW-009 |
| SWU-UPW-009 | same control/manifest; REGIONS task; W2; `execution-receipts/SWU-UPW-009.json` | SWU-UPW-010 |
| SWU-UPW-010 | same control/manifest; REGIONS task; W2; `execution-receipts/SWU-UPW-010.json` | SWU-UPW-011 |
| SWU-UPW-011 | same control/manifest; REGIONS task; W2; `execution-receipts/SWU-UPW-011.json` | SWU-UPW-012 |
| SWU-UPW-012 | same control/manifest; REGIONS task; W2; `execution-receipts/SWU-UPW-012.json` | SWU-UPW-013 |
| SWU-UPW-013 | same control/manifest; REGIONS task; W2; `execution-receipts/SWU-UPW-013.json` | SWU-UPW-014 |
| SWU-UPW-014 | same control/manifest; RESPONSIVE-COPY task; W3; `execution-receipts/SWU-UPW-014.json` | SWU-UPW-015 |
| SWU-UPW-015 | same control/manifest; RESPONSIVE-COPY task; W3; `execution-receipts/SWU-UPW-015.json` | SWU-UPW-016 |
| SWU-UPW-016 | same control/manifest; HARDENING task; W4; `execution-receipts/SWU-UPW-016.json` | SWU-UPW-017 |
| SWU-UPW-017 | same control/manifest; HARDENING task; W4; `execution-receipts/SWU-UPW-017.json` | none; W5 verification becomes eligible but is not mutation |

“Same control/manifest” expands exactly to `WORK-PACK.md` and
`SWU-MANIFEST.json`; the named task/wave and receipt path complete each row’s
inventory. Invoke Refresh may update only those targets.

## Blockers

| Blocker | Scope | Owner | Repair |
| --- | --- | --- | --- |
| B-PLAN-DISTILL | Plan admission | Invoke/Distill | run governed Plan Distill and apply accepted repairs |
| B-SWU-SELECTION | mutation only | human/lifecycle owner | select one exact SWU after Plan pass |

Residue that does not block Plan authoring is in
`work-pack/shared/cross-task-gaps.md`.

## Dispatch Technique Trace

The trace at `PLAN-TECHNIQUE-TRACE.md` binds `sequence`,
`scu_swu_reduction`, `recomposition_proof`, `validation_loop`,
`owner_boundary_check`, `handle_handoff`, `residue_ledger`, and
`execution_receipt_handoff` to exact artifacts/gates.

## Distill Validation

| Check | Current result | Evidence/gap |
| --- | --- | --- |
| smallest coherent SWUs | block pending review | draft atomicity table |
| first-unit narrowness | block pending review | recommended SWU-UPW-001 |
| recomposition | block pending review | traceability and waves authored |
| hidden acceptance gaps | block pending review | task detail and residue authored |
| deferred complexity | pass-for-draft | L3 and excluded scope explicit |
| navigation | pass-for-draft | linked work-pack, waves, tasks, source anchors |

## Current Route

The work-pack is not mutation-ready. Next route is governed Plan Distill. After
a passing gate, return to the human for explicit SWU selection; Task Session
must refuse an unselected candidate.
