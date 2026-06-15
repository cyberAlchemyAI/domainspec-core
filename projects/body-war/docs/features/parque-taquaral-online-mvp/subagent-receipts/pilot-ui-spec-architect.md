---
dispatch_id: body-war-pilot-domainspec-subagent-strategy-20260614
role_id: pilot-ui-spec-architect
agent_id: 019ec50d-7e9a-7d52-b493-4eff1f8357f7
spawn_status: spawned
join_status: completed
close_status: closed
validation_result: pass
status: complete
last_updated: 2026-06-14
---

# Receipt: Pilot UI Spec Architect

## Scope

Audit missing UI specification coverage for the hosted friend preview page:
friend login, Strava status, activity list, Parque track card, submission, and
preview controller state.

## Key Findings

- The feature folder lacks `ui-spec.md`; the local DomainSpec template expects a
  route table, page layouts, component inventory, data flow, form contracts,
  state-to-UI mapping, accessibility requirements, and UI concept registry.
- The target flow is real friend Strava data on a hosted preview, while the
  current prototype is a local Python/static surface with local token JSON.
- The current prototype can append submissions, but the decision requires an
  observable preview controller update after submission.
- `Park Track Alpha` is a stale placeholder for the selected Parque Taquaral
  pilot target.

## Missing UI Spec Coverage

| Area | Expected Contract | Priority |
| --- | --- | --- |
| Hosted route/access | Public preview route, callback return state, responsive web constraints. | P0 |
| Friend login | Connect Strava, redirect pending, callback success, denied auth, invalid state, not configured. | P0 |
| Strava status | Disconnected/configured/connected/refresh failed/no scope state mapping. | P0 |
| Activity list | Loading, empty real-data state, Strava error, run-like filtering, card fields, submit enablement. | P0 |
| Parque track card | Canonical track name, geometry/source status, controller metric, GPS caveat. | P0 |
| Submission flow | In-flight, success, error, auto-accept preview semantics. | P0 |
| Preview controller | Current holder/fastest time/latest submitted run display contract. | P0 |
| Accessibility | Semantic controls, focus return, live regions, status labels. | P1 |

## Tensions

- Visible fixture/demo runs conflict with the selected real friend data MVP.
  Fixtures should be internal tests unless a later decision explicitly allows
  demo UI.
- Auto-accept preview conflicts with older review/verified wording. The UI must
  show preview acceptance without claiming final verification.
- Hosted managed storage conflicts with current local prototype assumptions.

## Backlog Contribution

1. Create `ui-spec.md` from the local template before UI implementation.
2. Define one compact hosted page with friend submission and preview controller
   regions unless a later split is chosen.
3. Write a state-to-UI matrix for auth, activity, geometry, submission,
   controller, and hosted failure states.
4. Defer full operator review console and native mobile UI.

