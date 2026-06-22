---
id: troqar-product-architecture-ui-tests
feature: troqar-product-architecture
title: "TROQAR Frontend Test Specification"
status: active
test-runner: playwright
updatedAt: 2026-06-21
source: domainspec-ui-pipeline
---

# Test Specification: TROQAR Frontend

## Scope

This test specification derives browser E2E obligations from
[UI-SPEC.md](UI-SPEC.md). It complements the existing Node API/auth E2E and
does not replace backend validation.

## E2E Test Matrix

| Test ID | Category | Obligation | Source |
| --- | --- | --- | --- |
| UI-E2E-001 | Auth state | Anonymous runner sees working app shell and connect CTA. | `states.md#auth-state`, `UI-SPEC.md#route-table` |
| UI-E2E-002 | OAuth flow | Fake-Strava connect returns to connected UI state. | `operations.md#op-auth-callback` |
| UI-E2E-003 | Profile safety | Profile renders safe Strava link and no token-like text. | `UI-SPEC.md#security-and-privacy-requirements` |
| UI-E2E-004 | Activity import | Activities render redacted run summaries and geometry caveat. | `queries.md#query-catalog`, `states.md#activity-state` |
| UI-E2E-005 | Evidence submit | Runner can select a pilot track and submit one activity through UI. | `operations.md#op-evidence-submit` |
| UI-E2E-006 | Logout | Logout clears authenticated controls and returns connect CTA. | `interfaces.md#http-interface-table` |
| UI-E2E-007 | Mobile fit | At 390px width, topbar, profile cards, activity selector, and submit button do not overlap. | `../../UI-ARCHITECTURE.md#layout-contract` |
| UI-E2E-008 | Prototype handoff selectors | Studio handoff `data-od-id` anchors exist and carry accepted copy. | `prototype-handoff/STUDIO-PROTOTYPE-HANDOFF.md` |

## Browser E2E Obligations

| File | Status | Notes |
| --- | --- | --- |
| `app/e2e/troqar-product-architecture/ui.spec.ts` | active | Runs against the built BodyWar app with fake-Strava and memory auth. |

## Prototype Handoff Assertions

Browser tests must assert these selectors from the accepted Studio handoff:

- `troqar.shell`
- `topbar.account.actions`
- `auth.connect.cta`
- `profile.safe-athlete-card`
- `profile.strava-link`
- `activity.recent-summary`
- `evidence.submit.cta`

## Runner

```sh
npm --prefix projects/body-war/app run test:ui
```

## Current Validation

```sh
npm --prefix projects/body-war/app run build
npm --prefix projects/body-war/app run build:e2e
npm --prefix projects/body-war/app run check
npm --prefix projects/body-war/app run test:ui
git diff --check -- projects/body-war
```
