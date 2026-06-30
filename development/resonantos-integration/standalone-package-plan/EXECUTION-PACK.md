# Execution Pack: ResonantOS CyberAlchemy Standalone Package

## Planning Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| planningGateStatus | pass | Non-executed plan is ready for one-SWU Task Session handoff. |
| complexity | medium | Split waves and task files are required. |
| baselineWave | W0 | Start with package boundary proof. |
| activePlanRef | `work-pack/waves/W0.md` | First wave. |
| workPackManifest | `WORK-PACK.md` | Canonical executable plan. |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` | Layer decisions. |
| specRef | n/a | This is a package plan, not a DomainSpec feature spec. |
| activeLayerWindow | L0 | Package boundary proof. |
| lastPlannedAt | 2026-06-29T16:26:39Z | Initial plan. |
| readinessProfile | pilot | Private package handoff. |

## Task Board

| Task ID | Goal | Layer | Complexity | Waves | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-PACKAGE-BOUNDARY | Package skeleton and boundary. | L0 | medium | W0 | ready | not-started |
| TASK-CONTRACTS-VALIDATORS | Contracts, validators, Review Queue fixtures. | L1 | medium | W1 | ready-after-W0 | not-started |
| TASK-ADAPTER-FIRST-SLICE | Scope tags, read-only observer, no-promotion. | L1-L2 | medium | W1, W2 | ready-after-contracts | not-started |
| TASK-PROMOTION-BODY | Host-side provider body contract. | L3 | medium | W3 | ready-after-no-promotion | not-started |
| TASK-VERIFY-HANDOFF | Scrub, verify, handoff. | L3 | medium | W3 | ready-after-implementation | not-started |

## Wave Order

1. W0: prove package boundary with `SWU-RCI-001`.
2. W1: copy or port public-safe contracts and Review Queue mapping with `SWU-RCI-002` and `SWU-RCI-003`.
3. W2: describe first safe runtime behavior with `SWU-RCI-004` and `SWU-RCI-005`.
4. W3: prepare host-body and handoff readiness with `SWU-RCI-006` and `SWU-RCI-007`.

## Parallelization

No parallel execution until W0 exits. After W0, `SWU-RCI-002` and `SWU-RCI-003` may run in
parallel if their write scopes remain disjoint.

## Closure

Do not execute implementation from this pack as a whole. Select one SWU and route through
`task-session`.
