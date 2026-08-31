# SWU-BWSL-001 Read-Only Readiness Preflight

## Outcome Brief

`SWU-BWSL-000` remains validated and its eight live postimages rehash exactly. The next synthetic slice has been frozen as one independently reviewed six-target Candidate A. No Body War product execution occurred during this preflight. Product execution remains `BLOCKED` until the Body War product owner confirms the exact request digest below.

- Preflight result: `PASS`
- Product execution: `BLOCK`
- Mutation ready: `false`
- Candidate: `BW-BWSL001-PREFLIGHT-CANDIDATE-A`
- Candidate envelope SHA-256: `5028844e0671fe0f198954ee08789b68de8b503979e7d50c51bef80d6c2f58b5`
- Owner request SHA-256: `2907a9dc20ef91493ce7230e048fe3fe37c5ed60dbae1c61fe10cdc381e01419`

## Boundary And Next Decision

This preflight added run-local evidence only. It did not change the current Body War product bytes; the existing unstaged `SWU-BWSL-000` postimages remain in place. Canonical planning, Craft, Invoke/Arcanum, Git publication, provider, credential, private-data, deployment, and release state remain outside this preflight.

The exact owner decision is whether to authorize Candidate A in the bounded candidate-local prototype fast lane. Confirmation must be:

```text
confirmed 2907a9dc20ef91493ce7230e048fe3fe37c5ed60dbae1c61fe10cdc381e01419
```

That confirmation would authorize only the six product targets and five validation contracts frozen below. Before product mutation, a new repository-local Handoff Notice must preserve the intentionally deferred SWU-BWSL-001 lifecycle synchronization, all six baselines must rehash, and no unexpected helper may remain open.

## Exact Product Envelope

| Path | Operation | Baseline SHA-256 |
| --- | --- | --- |
| `app/server.ts` | update | `d960958d667908862343c7eb4e09a9a97a4ff0093bcb87a422e2c1a86ac4d1a2` |
| `app/src/auth/strava-oauth.ts` | update current SWU-000 postimage | `b349a411b1e142fd377b6081624757414d7a573eadf2c158a72ca90752bc7edf` |
| `app/src/auth/strava-activity-provider.ts` | update current SWU-000 postimage | `b7d9d69d925c126390df061f519f38957f621e27e3dc1c40f31d0793f863c139` |
| `app/tests/auth-consumer.test.ts` | update | `58b9e7bddb4b661e023b611b4fbf34a743d16d716ecfc78a51f1b12598e23cb6` |
| `app/tests/strava-activity-provider.test.ts` | update current SWU-000 postimage | `d7f5620caa63498d55a32452c2b86039eb9ae6e38ce48308531fe5e086acdc9c` |
| `app/e2e/body-war-auth.e2e.ts` | update current SWU-000 postimage | `bc2405f3cfa8453cb17746cd0b5fed6ad593b5090c681938f0c83c3c7a5ad5e5` |

Paths are relative to `projects/body-war/`. Repositories, schema/migrations, package manifests, UI/static files, planning/Craft artifacts, and Arcanum are explicitly excluded.

## Frozen Behavioral Decisions

1. In fake mode, the normal activity method remains repository-backed and any fetch is forbidden.
2. In real mode, the same normal method delegates to the already-tested provider seam; both server consumers retain that shared method and summary identity.
3. Public `page=N` requests exactly provider page `N`. The provider primitive gains a bounded `startPage` window while direct calls retain the accepted page-1 multi-page behavior.
4. The sequential replay key is `principal_id + suggested_track_id + provider_activity_id`.
5. An existing exact replay is rejected before provider fetch with HTTP `409` and exactly `{"error":"evidence_candidate_replay","message":"This activity already has evidence for this suggested track"}`; no second row is created.
6. Database-concurrent or multi-writer deduplication is not claimed and remains separately scoped work.
7. The existing ActivitySummary redaction allowlist remains mandatory; tokens, raw payloads, account/athlete metadata, coordinates, maps, polylines, notes, and secrets remain forbidden.

## Validation Surface

All five contracts are acceptance-critical:

1. targeted provider, consumer, and lifecycle tests with credentials unset, including exact-page, fake no-fetch, replay no-fetch, and stable-error assertions;
2. full `npm --prefix projects/body-war/app run validate` in memory/fake mode, with no generated schema change;
3. local-only PostgreSQL E2E with the existing image, pulling disabled, one-row replay proof, and guaranteed container/volume cleanup;
4. the existing seven-test Playwright regression through the pinned shared runtime in fake loopback mode;
5. exact combined ten-path Git status, update-aware whitespace checks, baseline rehash, privacy/network scans, and forbidden-surface diff.

The current SWU-000 baseline suite passed `37/37`. That is dependency and baseline evidence only; it does not validate unimplemented Candidate A bytes.

## Blockers

The only immediate execution blocker is exact confirmation of the immutable owner request. The new deferred-governance Handoff Notice, baseline rehash, and helper check are mandatory post-confirmation pre-mutation checks, not authority substitutes.

The following remain deliberately deferred: the Invoke governance-tooling repair; canonical planning/Craft synchronization; Task Session lifecycle bookkeeping; database-concurrency uniqueness; `OWNER-BWSL-001`; `SWU-BWSL-002`; credentials, private data, real provider calls, real evidence, deployment, publication, promotion, release, and production claims.

## Decision Gate Result

- Result: `BLOCK`
- Admissible routing: `gate`
- Decisions resolved: `0`
- Blockers remaining: `1`
- Admissible options: authorize Candidate A; defer Candidate A; stop BWSL-001
- Recommendation: authorize Candidate A only if the exact page, replay, sequential-only, and six-target semantics are intended; otherwise request revision.
- Explain / more context: available and non-committal.

## Evidence

- `CANDIDATE-ENVELOPE.json` freezes exact behavior, paths, baselines, validation, and claim ceiling.
- `CONTEXT-PACK.md` binds 23 obligation-linked excerpts from 14 source files.
- `INDEPENDENT-READINESS-REVIEW.md` records independent PASS and the repaired whitespace-only evidence defect.
- `OPTION-ADMISSIBILITY-REQUEST.json` and `OPTION-ADMISSIBILITY-RECEIPT.json` record the Decision Gate prefilter.
- `OWNER-AUTHORIZATION-REQUEST.json` is the immutable single-use owner request.

One bounded helper was spawned, joined, and closed; no helper remains open for this preflight.

## Claim Ceiling

This preflight proves only a current-tree six-target synthetic implementation proposal and a deterministic validation route. It proves no Candidate A implementation bytes or test result, planning acceptance/apply, lifecycle admission, live Strava compatibility, private-data processing, real witness, concurrent deduplication, policy selection, deployment, publication, release, or production readiness.
