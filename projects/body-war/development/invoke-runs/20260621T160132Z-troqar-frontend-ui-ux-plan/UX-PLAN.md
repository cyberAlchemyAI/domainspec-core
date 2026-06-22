# UX Plan - TROQAR Frontend

Status: `invoke-plan-pass`
Generated: `20260621T160132Z`
Source skills: `domainspec-ui-pipeline`, `invoke`
Target feature: `projects/body-war/docs/features/troqar-product-architecture/`

## Objective

Turn the TROQAR product architecture and the newly working auth/profile backend
into a frontend-ready UX contract: explicit UI architecture, feature UI spec,
browser test obligations, and an execution plan for wiring Playwright and
hardening the current static app without expanding into the full game.

## UX Boundary

In scope for the next frontend execution:

- online runner profile shell;
- auth/Strava connection status;
- safe Strava profile link;
- redacted activity summary list;
- track selector and evidence submission;
- submitted evidence list;
- logout;
- mobile layout fit and no-overlap checks.

Out of scope:

- full territory map;
- route geometry proof;
- challenges, clans, rankings, store, sponsor pages;
- React/Vite migration unless explicitly selected by a later work-pack;
- real Strava secret provisioning or VPS deployment.

## User Journey

1. Anonymous runner opens TROQAR and sees a working app surface with `Connect Strava`.
2. Runner connects Strava through fake or real provider flow.
3. App returns to a connected state with a safe athlete summary and Strava profile link.
4. Runner sees privacy reassurance: provider tokens stay server-side and activity summaries are redacted.
5. Runner refreshes/imports recent run summaries.
6. Runner selects a pilot track and submits one activity.
7. App shows submitted preview evidence without verified-geometry language.
8. Runner logs out and returns to anonymous controls.

## Generated Frontend Specs

| Artifact | Role |
| --- | --- |
| `projects/body-war/docs/UI-ARCHITECTURE.md` | BodyWar frontend constitution for L0 static UI and future framework promotion. |
| `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md` | Feature UI contract derived from SPEC/interfaces/operations/queries/states/visual definitions. |
| `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md` | Browser E2E obligations and Playwright wiring requirements. |
| `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts` | Playwright-style scaffold for frontend E2E tests. |

## UX Acceptance

The UX is acceptable when:

- the first viewport has connection state, profile/action affordance, activity state, and evidence path;
- all auth states have recoverable UI copy;
- no token-like strings render in the DOM;
- geometry/scoring caveats remain visible after activity import and submission;
- activity submit works with the CSRF-bound browser session;
- mobile width around 390px keeps account actions, activity selector, and submit button usable;
- Playwright tests run in CI/local once browser dependency wiring is complete.

## Dispatch Technique Trace

| Technique | Applied To | Validation Expectation |
| --- | --- | --- |
| `sequence` | UI pipeline outputs before invoke plan | Specs/test scaffold exist before execution work-pack. |
| `artifact_contract_bridge` | SPEC/interfaces/states to UI-SPEC/TEST-SPEC | Every UI obligation names source docs or API routes. |
| `owner_boundary_check` | BodyWar app vs DomainSpec framework defaults | Current static UI remains valid L0; React/Vite migration is deferred. |
| `scu_swu_reduction` | Work-pack decomposition | First executable unit is Playwright wiring, not full app rebuild. |
| `recomposition_proof` | L0 frontend hardening | Static UI hardening recomposes into app-wide TROQAR UI architecture. |
| `validation_loop` | E2E and visual checks | Browser tests and build checks gate completion. |
| `residue_ledger` | Deferred game pages and deploy evidence | Route/map/challenge/community/VPS gaps remain visible. |

## Next Route

Route the [WORK-PACK.md](WORK-PACK.md) to `task-session` when ready to execute.
The first recommended SWU is `SWU-TUI-001`.
