---
node_type: execution-pack
status: active
topic: Parque Taquaral online MVP execution pack
last_updated: 2026-06-14
created_by: codex
invoke_mode: plan
---

# Execution Pack: Parque Taquaral Online MVP

## Planning Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| planningGateStatus | block-for-app-mutation | W0 docs can execute; app mutation waits. |
| complexity | medium | Split work-pack required. |
| baselineWave | W0 | Mandatory spec baseline. |
| activePlanRef | `work-pack/waves/W0.md` | Current wave. |
| workPackManifest | `WORK-PACK.md` | Canonical execution manifest. |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` | L0-L3 boundary. |
| activeLayerWindow | L0 | Spec baseline. |
| lastPlannedAt | 2026-06-14T00:00:00Z | Date-only source session. |
| readinessProfile | pilot-preview | Hosted friend preview only. |

## Task Board

| Task ID | Goal | Layer | Complexity | Waves | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-W0-SPEC-BASELINE | Write P0 specs and contracts. | L0 | medium | W0 | ready | not-started |
| TASK-W1-TYPESCRIPT-SCAFFOLD | Replace Python app path with TS scaffold. | L1 | medium | W1 | blocked-until-W0 | not-started |
| TASK-W1-FRIEND-FLOW | Implement friend Strava flow and controller. | L1 | medium | W1 | blocked-until-W0 | not-started |
| TASK-W2-HOSTED-PREVIEW | Deploy hosted preview. | L2 | medium | W2 | blocked-until-W1 | not-started |
| TASK-W3-VERIFY-AND-AUDIT | Verify preview and audit alignment/layering. | L2 | medium | W3 | ready-after-implementation | not-started |

## Closure Obligations

1. Completion verification is `TASK-W3-VERIFY-AND-AUDIT`.
2. Alignment and layering audits are required because mutation-capable stages are
   planned after W0.
3. If W0 remains docs-only, closure evidence is reviewable specs plus updated
   gate status, not runtime proof.

## Design-Guided Task Directives

| Task ID | Source Contracts | Coverage IDs | Architecture References | Implementation Directive | Verification Evidence |
| --- | --- | --- | --- | --- | --- |
| TASK-W0-SPEC-BASELINE | `DESIGN.md`, `PILOT-DOMAINSPEC-BACKLOG.md` | SWU-BWPT-001..006 | `ARCHITECTURE-AUDIT.md` | Write contracts before runtime mutation; preserve preview-only guardrails. | P0 docs exist and review cleanly. |
| TASK-W1-TYPESCRIPT-SCAFFOLD | W0 specs | SWU-BWPT-007 | `ARCHITECTURE-AUDIT.md` | Keep domain/application code separate from adapters; configure DomainSpec path/source refs. | Typecheck and route smoke. |
| TASK-W1-FRIEND-FLOW | `interfaces.md`, `operations.md`, `queries.md`, `mappings.md`, `ui-spec.md` | SWU-BWPT-008 | `DESIGN.md` views | Implement auth/activity/submission/controller according to W0 contracts. | Local or hosted preflight receipts. |
| TASK-W2-HOSTED-PREVIEW | `DEPLOYMENT-SECURITY.md`, `TEST-SPEC.md` | SWU-BWPT-009 | security/dependency interface view | Use sealed secrets and managed storage; no local JSON authority. | Hosted no-secret smoke. |
| TASK-W3-VERIFY-AND-AUDIT | `TEST-SPEC.md`, `IMPLEMENTATION-LAYERING.md` | SWU-BWPT-010 | all design views | Validate preview only and record deferrals for pilot-ready claims. | PTV matrix and audit notes. |

## Wave Status Board

| Wave | Objective | Entry Gate | Exit Gate | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| W0 | Lock P0 spec baseline. | Work-pack exists. | W0 SWUs pass. | ready | `work-pack/waves/W0.md` |
| W1 | Build TypeScript hosted-flow app. | W0 pass. | App smoke plus controller update preflight. | blocked | `work-pack/waves/W1.md` |
| W2 | Deploy hosted preview with managed storage/secrets. | W1 pass. | Hosted URL/callback/no-secret smoke. | blocked | `work-pack/waves/W2.md` |
| W3 | Verify preview and close audits. | W2 pass. | PTV matrix and alignment/layering notes. | blocked | `work-pack/waves/W3.md` |

## Delivery Stage Coverage

| Stage | Required | Wave Mapping | Status | Evidence | Skip Reason |
| --- | --- | --- | --- | --- | --- |
| discover | yes | W0 | completed | `DISCOVERY.md`, decision record | n/a |
| design-baseline | yes | W0 | completed | `DESIGN.md` | n/a |
| specification | yes | W0 | not-started | W0 SWUs | n/a |
| scenarios | yes | W0/W1 | not-started | `ui-spec.md`, `TEST-SPEC.md` | n/a |
| tests | yes | W0/W3 | not-started | `TEST-SPEC.md`, PTV matrix | n/a |
| implementation | yes | W1 | blocked | W0 gate | n/a |
| interface-experience | yes | W0/W1 | blocked | `ui-spec.md` first | n/a |
| telemetry-spec | yes | W2 | deferred | no telemetry beyond preview receipts | preview scope |
| telemetry-instrument | yes | W2 | deferred | no telemetry beyond preview receipts | preview scope |
| telemetry-verify | yes | W3 | deferred | no telemetry beyond preview receipts | preview scope |
| deployment | yes | W2 | blocked | `DEPLOYMENT-SECURITY.md` first | n/a |
| concept-index-sync | yes | W3 | deferred | no registry promotion | project-local only |
| readiness-review | yes | W3 | blocked | PTV matrix | n/a |
| completion-verify | yes | W3 | blocked | TASK-W3-VERIFY-AND-AUDIT | n/a |
| audit-alignment | yes | W3 | blocked | TASK-W3-VERIFY-AND-AUDIT | n/a |
| audit-layering | yes | W3 | blocked | TASK-W3-VERIFY-AND-AUDIT | n/a |

## Notes

- Execute one SWU at a time during W0.
- W1 app mutation must not start from the Python prototype alone; use W0 specs
  as source contracts.
- Friend secrets and raw activity payloads stay out of repo docs.

