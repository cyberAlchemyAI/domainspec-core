---
stage_id: s06-invoke-design
capability_ref: invoke
mode: design
status: pass
---

# S06 Invoke Redefine / Design

## Context View

Body War has a TypeScript app with Strava auth, runner profile, activity consult,
Drizzle/Postgres auth storage, and validation scripts. SuggestedTrack should
turn route expansion into a user-visible product loop while preserving the
existing protected-data posture.

## High-Level Structure View

```text
Connected runner
  -> SuggestedTrack list/detail
  -> Suggest track
  -> Help existing suggestion
  -> Live Strava activity consult
  -> Consent to attach one redacted summary
  -> Operator review/promotion later
```

## Low-Level Components View

| Component | Owner | Build expectation |
| --- | --- | --- |
| SuggestedTrack schema | Body War app Drizzle/Postgres | new table + generated migration |
| Evidence candidate schema | Body War app Drizzle/Postgres | new table, redacted summary, consent fields |
| Taquaral seed | Body War app data/bootstrap | idempotent `needs_evidence` seed |
| SuggestedTrack API | Body War server | list/create/detail/help/evidence attach endpoints |
| Activity consult | Existing Strava auth/server | authenticated live consult; no persistence during browsing |
| Home UI | Body War static app | connected-runner suggestions and help flow |
| Validation | Body War app tests/e2e | unit/integration/UI/no-secret checks |

## Workflow Process View

1. Connected runner sees suggested tracks.
2. Runner creates a suggestion or opens "Tenho essa corrida" on an existing
   suggestion.
3. Server consults Strava activities live using existing auth.
4. Browser receives redacted summaries only.
5. Runner explicitly consents to attach one activity as evidence.
6. Server stores an `ActivityEvidenceCandidate`, not a raw provider payload.
7. Suggestion status can move to `evidence_submitted` or `operator_review`.
8. `source_backed` and `pilot_ready` stay unavailable until operator/source
   evidence exists.

## Decision Flow View

- Visibility: connected runners only for L0.
- Creation: login required before submit.
- Seed: idempotent data seed after migration.
- Promotion: operator-only in L0.
- Storage: existing Postgres/Drizzle.
- Geometry: no source-backed claim in this build.

## Dependency Interface View

- Use `projects/body-war/app/src/infrastructure/postgres/schema.ts`.
- Generate migration via `npm --prefix projects/body-war/app run db:generate`.
- Use existing auth/session/Strava services for activity consult.
- Do not reuse legacy JSON-file `/api/submissions` as the evidence-candidate
  persistence layer.

## Design Verdict

`pass`: the design resolves route and ownership enough for plan handoff, with
repair applied in S08 for the older Craft/work-pack gate mismatch.

