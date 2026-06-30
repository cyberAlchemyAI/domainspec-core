---
tags: [parque-taquaral-online-mvp, suggested-track, spec, test]
node_type: spec
is_session: false
layer: application
nature: procedural, technical
status: active
version: 0.1.0
last_updated: 2026-06-29
---

# Test Spec: SuggestedTrack Route Expansion

This spec covers the one-go SuggestedTrack build in `projects/body-war/app`.
Tests live in the existing Node API test, Postgres e2e runner, and Playwright UI
suite.

## Test Matrix

| ID | Test | Validates |
| --- | --- | --- |
| SGT-T1 | Connected fake-Strava runner can list seeded `Volta do Taquaral`. | [queries.md QT-1](queries.md#rules), [operations.md SD-1](operations.md#ensuredefaultsuggestedtracks) |
| SGT-T2 | Anonymous or missing-CSRF creation is rejected. | [interfaces.md POST /api/suggested-tracks](interfaces.md#post-apisuggested-tracks) |
| SGT-T3 | Connected runner can create a suggestion as `needs_evidence`. | [operations.md CT-2](operations.md#rules) |
| SGT-T4 | Evidence attach requires consent and stores only redacted summary fields. | [operations.md EC-2](operations.md#rules) |
| SGT-T5 | Evidence attach moves `needs_evidence` to `evidence_submitted` without source-backed or pilot-ready claim. | [states.md Allowed Transitions](states.md#allowed-transitions) |
| SGT-T6 | UI shows SuggestedTrack list/create/help flow after fake Strava login. | [ui-spec.md Connected Runner Surface](ui-spec.md#connected-runner-surface) |
| SGT-T7 | UI and API responses do not leak tokens, raw OAuth terms, or verified/pilot-ready claims. | [ui-spec.md Copy Rules](ui-spec.md#copy-rules) |

## Known Gaps

### G1 - Operator Promotion

Operator-only `operator_review`, `source_backed`, `accepted`, and `rejected`
flows are documented but not implemented in this build.

### G2 - Real Geometry

Parque Taquaral source-backed geometry remains a separate gap and is not proven
by SuggestedTrack candidate evidence.
