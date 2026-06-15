---
node_type: implementation-layering
status: active
topic: Parque Taquaral hosted friend preview implementation layers
last_updated: 2026-06-14
created_by: codex
invoke_mode: plan
---

# Implementation Layering: Parque Taquaral Online MVP

## Purpose

Define the layer boundaries for moving from current docs and Python prototype
evidence to a hosted TypeScript friend preview without overclaiming pilot
readiness.

## Target And Scope

- Target: `projects/body-war/docs/features/parque-taquaral-online-mvp`
- Runtime target: `projects/body-war/app/`
- Scope: feature, UI/API workflow, hosted integration, deployment validation
- Current state: partially implemented Python/local prototype, TypeScript target
  selected, hosted provider/storage and geometry artifact missing

## Layer Boundary Rule

Every layer answers: after this layer, we know whether the next stronger claim
is justified by evidence.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (Spec Baseline) | After this layer, we know whether the MVP is implementation-ready without guessing provider, geometry, UI, API, or validation contracts. | W0 specs and contracts. | `SPEC.md`, `domain.md`, `states.md`, `TRACK-GEOMETRY.md`, `DEPLOYMENT-SECURITY.md`, `interfaces.md`, `operations.md`, `queries.md`, `mappings.md`, `ui-spec.md`, `TEST-SPEC.md`. | TypeScript app mutation and live friend test. | Reviewable docs, selected provider/storage, geometry source, P0 test matrix. | Continue to L1 app build, narrow scope, or stop for blocker decision. |
| L1 (Hosted Flow Build) | After this layer, we know whether the real friend flow can run end to end in a hosted TS app. | TypeScript app replacing Python path with OAuth/activity/submission/controller flow. | TS scaffold, API routes, UI page, Strava adapter, managed storage adapter, preview controller. | Pilot-ready GPS validation, full anti-cheat, operator console. | Hosted dev/staging flow works with no-secret checks and mocked preflight. | Continue to L2 hardening or remediate. |
| L2 (Preview Reliability) | After this layer, we know whether hosted preview security and failure behavior are credible enough for one friend preview. | Hosted deployment with sealed secrets and redacted evidence. | HTTPS deploy, callback config, token refresh/error states, logging redaction, zero-activity handling, deployment smoke. | Scale, public launch, production-grade observability. | Redacted hosted validation receipt, no-secret evidence, controller update proof. | Run friend preview, remediate, or stop. |
| L3 (Pilot Readiness Split) | After this layer, we know whether a stronger pilot-ready claim is credible. | Geometry/GPS proof and operator verification plan. | GPS validation research, review workflow, anti-cheat decision, persistence audit, pilot runbook. | Economy, city-wide map, mobile app, sponsorships. | Separate pilot-ready decision and validation artifacts. | Promote to pilot-ready work or defer. |

## Non Regression Guardrails

- L1 must preserve all L0 contract names and guardrails.
- `preview-accepted` must not become `verified` without a later gate.
- Local JSON token storage must not become hosted authority.
- Friend activity data must stay redacted in repo artifacts.
- Track geometry display must not claim GPS validation until L3 evidence exists.

## Recommended Next Layer

- Next layer: L0.
- Key decision unlocked: whether app mutation can start safely.
- Major deferred scope: TypeScript app replacement, hosted deploy, live friend
  validation, GPS proof, anti-cheat, economy, mobile app.

