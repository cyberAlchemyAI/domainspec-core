---
node_type: runtime-handoff
status: ready-for-task-session
run_id: 20260629T050046Z-suggested-track-decision-build-route
authorization: approved
subagent_authorization: approved
next_handoff_id: HND-SUGGESTED-TRACK-ONE-GO-BUILD-001
---

# Runtime Handoff: SuggestedTrack Decision And One-Go Build Route

Runtime-backed Refine execution is complete. The next runtime surface is one
bounded Task Session with a required preflight before app mutation.

## Objective

Build the SuggestedTrack feature in one governed pass after closing/updating the
feature-local W0/work-pack gate inside the Task Session preflight.

## Confirmed Route Target

```text
decision slate -> refined design -> one-go build handoff
```

## Confirmed Decision Defaults

- Suggested track visibility: connected runners only in L0.
- Suggestion creation: login required before submit.
- Taquaral seed: versioned idempotent seed data after Drizzle migration.
- Promotion authority: operator-only promotion to `source_backed` for L0.
- Storage path: existing Body War Postgres/Drizzle stack.
- Geometry claim: `needs_evidence` until source-backed evidence exists.
- One-go build scope: docs, schema, migration, seed, API, UI, and tests without
  pilot-ready overclaim.

## Completed Subagent Review

1. `product-decision-synthesist`
2. `data-security-schema-reviewer`
3. `one-go-build-slice-planner`

Receipts are stored under `stages/subagent-receipts/`.

## Required Task Session Preflight

Before app code mutation, update the feature docs/work-pack gate so the one-go
Task Session explicitly supersedes the older Slice 1-only next move for this
child context.

## Next Runtime Surface

`task-session` on `HND-SUGGESTED-TRACK-ONE-GO-BUILD-001`.

The Task Session must:

1. Record the confirmed decision slate.
2. Add/update SuggestedTrack docs and tests.
3. Add Drizzle/Postgres schema and generated migration.
4. Seed "Volta do Taquaral" as `needs_evidence`.
5. Add SuggestedTrack API/UI.
6. Preserve live Strava consult, explicit consent, redacted persistence, and no
   source-backed/pilot-ready overclaim.
7. Run:

```bash
npm --prefix projects/body-war/app run validate
npm --prefix projects/body-war/app test
npm --prefix projects/body-war/app run e2e
npm --prefix projects/body-war/app run test:ui
```

`test:ui` may be recorded as blocked only if browser dependencies are missing,
with exact blocker evidence.
