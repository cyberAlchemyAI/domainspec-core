---
node_type: refine-seed-proposal
status: strategy-proposed
run_id: 20260629T050046Z-suggested-track-decision-build-route
target: projects/body-war
preset: standard
research_mode: research-if-gap-appears
authorization: requires_user_permission
---

# Refine Seed Proposal: SuggestedTrack Decision And One-Go Build Route

## Operator Intent

Open the remaining decision paths for the SuggestedTrack feature, choose a
single coherent route, and prepare the project to build the feature in one
bounded pass after confirmation.

The requested outcome is not another loose plan. It is a decision slate plus a
runtime-ready refinement route that can converge on one build handoff.

## Current Evidence

- Body War Craft owns the work under `CTX-BODY-WAR-SUGGESTED-TRACKS`.
- The existing SuggestedTrack route selected this product chain:

```text
SuggestedTrack -> EvidenceRequest -> ActivityEvidenceCandidate -> SourceBackedTrack
```

- The existing runtime handoff is blocked until the operator confirms the route.
- The previous architecture plan left four explicit decisions open:
  suggested-track visibility, login timing, Taquaral seed mechanism, and first
  promotion authority.
- The broader Parque Taquaral work-pack still blocks app mutation until W0
  provider/schema, geometry, API, UI, and validation contracts are closed.

## Decision Paths To Confirm

| Decision | Recommended path | Other viable paths | Why this default fits one-go build |
| --- | --- | --- | --- |
| Suggested track visibility | Connected runners can see suggestions in L0. | Public read-only cards; operator-only preview. | Avoids public route claims before source-backed evidence while still making the feature useful. |
| Suggestion creation | Login required before submit. | Anonymous draft then connect; operator-only creation. | Keeps ownership, abuse control, and audit trail simple for the first pass. |
| Taquaral seed | Versioned seed data applied idempotently after Drizzle migration. | Migration insert; static JSON compatibility only. | Keeps generated schema migration clean while still treating Taquaral as data, not a hardcoded exception. |
| Promotion authority | Operator-only promotion to `source_backed` for L0. | Automatic promotion after evidence; crowd threshold. | Preserves geometry honesty and review control until pilot rules mature. |
| Storage/provider | Reuse the existing Body War Postgres/Drizzle path. | New managed provider selection; local JSON. | The app already has Drizzle/Postgres surfaces, so one-go build should not reopen provider selection. |
| Geometry claim | Seed `Volta do Taquaral` as `needs_evidence`; no `source_backed` claim in this build. | Attempt sourced geometry now; keep no seed. | Lets the feature ship honestly while preserving the active geometry gap. |
| One-go build scope | Docs, schema, migration, seed, suggestion API, evidence consult/attach contract, home UI, and tests in one task session. | Slice 1 specs/schema only; full pilot-ready geometry. | Matches the operator request while excluding pilot-ready overclaims. |

## Planned Write Scope After Confirmation

Documentation and contracts:

- `projects/body-war/docs/features/parque-taquaral-online-mvp/SPEC.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/domain.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/states.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/interfaces.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/queries.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/ui-spec.md`
- `projects/body-war/docs/features/parque-taquaral-online-mvp/TEST-SPEC.md`

Application surfaces:

- `projects/body-war/app/src/infrastructure/postgres/schema.ts`
- `projects/body-war/app/src/infrastructure/postgres/migrations.ts`
- `projects/body-war/app/src/infrastructure/postgres/database.ts`
- generated Drizzle migration files under `projects/body-war/app/drizzle/`
- suggested-track seed data/helper under `projects/body-war/app/src/infrastructure/postgres/`
- `projects/body-war/app/server.ts`
- `projects/body-war/app/static/index.html`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/static/styles.css`
- `projects/body-war/app/tests/*`
- `projects/body-war/app/e2e/*`

## Done Criteria For The Future One-Go Build

1. SuggestedTrack, evidence request, evidence candidate, and source-backed track
   concepts are documented with non-goals and owner boundaries.
2. Statuses distinguish `needs_evidence`, `evidence_submitted`,
   `operator_review`, `source_backed`, and `pilot_ready`.
3. Drizzle/Postgres schema and generated migration add the suggested-track and
   evidence-candidate records without storing raw Strava activity payloads.
4. "Volta do Taquaral" is seeded as a suggested track with `needs_evidence`.
5. Connected runners can view suggested tracks, propose a track, and help an
   existing suggestion.
6. Strava activity consult remains live/ephemeral until explicit consent to
   attach one redacted activity summary.
7. Tests prove schema, API validation, redaction/no-secret behavior, UI smoke,
   and no geometry/source-backed overclaim.

## Research Decision

`research-if-gap-appears`.

Use local repository evidence first. External research is deferred unless the
confirmed refinement run identifies a specific implementation field gap, such as
an exact Strava activity field or Drizzle migration behavior that cannot be
resolved from local code.

