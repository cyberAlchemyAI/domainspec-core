---
stage_id: s07-interrogation-design-review
capability_ref: interrogation
mode: refine-design-review
status: flag
---

# S07 Interrogation Design Review

## Review Question

Can the design route to one Task Session without reopening product or privacy
decisions?

## Verdict

`flag`: route can proceed after repair. There are no blockers, but three
handoff requirements must be explicit.

## Required Handoff Requirements

1. The Task Session must start with a preflight docs/gate update and only then
   mutate app code.
2. The Task Session must add SuggestedTrack-specific tests, not rely only on
   existing auth tests.
3. The Task Session must run concrete validation commands:
   - `npm --prefix projects/body-war/app run validate`
   - `npm --prefix projects/body-war/app test`
   - `npm --prefix projects/body-war/app run e2e`
   - `npm --prefix projects/body-war/app run test:ui` when browser/UI changes
     are included and dependencies are available.

## Non-Blocking Residue

- Existing active Strava-activity evidence blocker remains open until a real
  consenting activity is submitted.
- Source-backed geometry remains deferred.
- Pilot-ready status remains deferred.

