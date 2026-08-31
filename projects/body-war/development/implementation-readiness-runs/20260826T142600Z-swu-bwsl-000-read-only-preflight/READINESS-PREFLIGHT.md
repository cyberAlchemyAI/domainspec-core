# SWU-BWSL-000 Read-Only Readiness Preflight

## Outcome Brief

`HN-30108A027C74` resolved with digest verification PASS. The permitted
current-tree preflight completed and froze one eight-path Candidate A, but no
Body War product execution occurred. Product execution remains BLOCKED until
the Body War product owner answers the exact request digest below.

- Preflight result: `PASS`
- Product execution: `BLOCK`
- Mutation ready: `false`
- Candidate: `BW-BWSL000-PREFLIGHT-CANDIDATE-A`
- Candidate envelope SHA-256:
  `8c00991de02be8f0df59642d2865980c57ac573b6c2cb1be69a92fdf6c58ad2e`
- Owner request SHA-256:
  `7f05a1960441d9adebc89f1e6e9d582572f59d5b6a170c63f40d98a8d5b79a2a`

## Boundary And Next Decision

Changed only this run-local preflight directory. Body War app, canonical
planning, Craft, Invoke/Arcanum, Git, provider, credential, private-data,
deployment and publication state remain unchanged.

The exact owner decision is whether to authorize Candidate A in the bounded
candidate-local prototype fast lane. Confirmation must be:

```text
confirmed 7f05a1960441d9adebc89f1e6e9d582572f59d5b6a170c63f40d98a8d5b79a2a
```

That confirmation would authorize only the eight product paths and validation
surface frozen below. It would not authorize `SWU-BWSL-001/002`, Strava calls,
private evidence, planning apply, Git, deployment, promotion or release.

## Exact Product Envelope

| Path | Operation | Baseline SHA-256 |
| --- | --- | --- |
| `app/e2e/body-war-auth.e2e.ts` | update | `146220cabf8bc68d8c4fd2c3006109d0511fa41cd96f6cdb900fa9dd376da16d` |
| `app/src/auth/body-war-repository.ts` | update | `3fd085deeb2fc716189d8dd1a945c21ec6aaab686b36c3ad907cadbc3f3d5815` |
| `app/src/auth/drizzle-repository.ts` | update | `38eaf706dd96d6d24811ed5d30c388e59571c7629b32a1cf79a684e04692f459` |
| `app/src/auth/memory-repository.ts` | update | `4f1ba3315621586640c6b8cafb03ae00715e58ad6a616745f01b21b86afb2ada` |
| `app/src/auth/strava-activity-provider.ts` | create | absent |
| `app/src/auth/strava-oauth.ts` | update | `798e0f401633ebb235d989191c2f00ccff7183c7f50be7e6b857c7f6473f26b4` |
| `app/tests/evidence-lifecycle.test.ts` | create | absent |
| `app/tests/strava-activity-provider.test.ts` | create | absent |

Paths are relative to `projects/body-war/`. `server.ts`, UI/static files,
`types.ts`, schema/migrations, package manifests and planning/Craft artifacts
are explicitly excluded.

## Frozen Behavioral Decisions

1. Add an injectable, provider-backed `listProviderActivitySummaries` path;
   leave the existing repository-backed `listActivitySummaries` path unchanged
   until `SWU-BWSL-001`.
2. Bound provider access to pages `1..10` and `1..100` records per page; stop
   on a short page and reject invalid bounds before fetch.
3. Retain only `Run`, `TrailRun` and `VirtualRun`, then project the existing
   `ActivitySummary` allowlist.
4. Treat zero eligible activities as a successful empty list, matching the
   live state model.
5. Refresh only an expired latest stored token, persist the rotated token pair
   before activity retrieval, and map provider failures to stable safe errors.
6. Provide idempotent exact-candidate deletion/consent-revocation mechanics.
   Reset only a track whose last evidence candidate was removed.
7. Provider revocation disconnects the account and removes provider tokens,
   while preserving profile and evidence rows. No descendant, backup or cache
   policy is silently selected before `OWNER-BWSL-001`.

## Dependency Graph

```text
synthetic unit fixtures
  -> provider gateway (injected fetch, bounds, filter, safe projection)
  -> additive OAuth provider method
       -> linked account -> latest encrypted token -> refresh/rotation
  -> repository lifecycle contract
       -> memory adapter
       -> Drizzle adapter -> existing Postgres tables

server /api/activities -> existing repository summaries [unchanged]
SWU-BWSL-001 -> later endpoint/SuggestedTrack wiring
OWNER-BWSL-001 -> later real-evidence policy
SWU-BWSL-002 -> separately authorized real witness
```

## Deterministic Test Matrix

| Group | Required cases |
| --- | --- |
| Provider bounds | invalid page/per-page rejects before fetch; at most 10 pages and 100 records/page; short-page stop |
| Filtering | retain only `Run`, `TrailRun`, `VirtualRun`; zero eligible returns `[]` |
| Redaction | output only the allowlist; reject tokens, raw payload, athlete/account data, maps, polylines, coordinates, notes and secrets |
| Token lifecycle | newest unexpired token skips refresh; expired token refreshes once, persists both rotated tokens and uses the rotated access token |
| Safe errors | missing scope/account/token, unreadable ciphertext, rejected refresh, 401/403, 429, malformed/network/5xx response |
| Memory lifecycle | exact disposition, repeat disposition, last-evidence projection reset, provider revocation and repeat revocation |
| Postgres lifecycle | repeat the memory contract against ephemeral PostgreSQL using the existing tables |
| Regression | existing API/UI remain fake-provider, repository-backed and free of external Strava calls |

All provider fixtures inject `fetch`, use fixed clocks and synthetic payloads,
and fail on any unexpected URL.

## Validation Surface

All are acceptance-critical for Candidate A:

1. memory/fake-provider unit suite with Strava credential variables unset;
2. `npm --prefix projects/body-war/app run validate`;
3. exact new provider/lifecycle tests after `build:test`;
4. Drizzle E2E against the already-installed `postgres:16-alpine` image with
   pulling disabled and guaranteed container/volume cleanup;
5. loopback Playwright UI regression with the fake gateway;
6. exact update/create whitespace checks, privacy scans, baseline rehash and
   exactly-eight-path scoped Git status.

The current existing synthetic suite passed `17/17`. That is baseline evidence
only; it does not validate unimplemented Candidate A bytes. The run left
`projects/body-war/app` and `projects/auth-user-management` unchanged in Git.

Environment observed: Node `22.13.0`, npm `10.9.2`, TypeScript `5.9.3`, Docker
`28.0.1`, Compose `2.33.1`, local Playwright `1.61.0`, Chromium revision
`1228`, and local Postgres image
`sha256:b97fe41a065781e884f8a23fd3dfd04c3348ce02d7a7c5cb2c0645317b4eb663`.

## Blockers

Execution blockers:

- canonical planning still contains the old Python-era Work Pack; the staged
  TypeScript SWU contract is non-executing, unselected and unapplied;
- Candidate A has not received exact owner confirmation;
- no Task Session admission or mutation receipt exists (intentionally deferred
  only if the owner selects the candidate-local fast lane).

Later blockers that do not prevent synthetic Candidate A mechanics:

- `OWNER-BWSL-001` retention, deletion timing, descendant/cache/backup,
  public-receipt, identity/scope and real-witness rules;
- real credentials, provider calls and a real activity witness;
- deployment, geometry, scoring, competition, release and production gates.

## Decision Gate Result

- Result: `BLOCK`
- Admissible routing: `gate`
- Decisions resolved: `0`
- Blockers remaining: `1`
- Admissible options: authorize Candidate A; defer Candidate A; stop BWSL-000
- Recommendation: authorize Candidate A only if the frozen semantics and exact
  candidate-local boundary are intended; otherwise request revision.
- Explain / more context: available and non-committal.

## Evidence

- `CANDIDATE-ENVELOPE.json` — exact behavior, paths, baselines, validation and
  claim ceiling.
- `INDEPENDENT-READINESS-REVIEW.md` — independent convergence and split audit.
- `OPTION-ADMISSIBILITY-REQUEST.json` and
  `OPTION-ADMISSIBILITY-RECEIPT.json` — Decision Gate prefilter evidence.
- `OWNER-AUTHORIZATION-REQUEST.json` — immutable single-use owner request.

## Claim Ceiling

This preflight proves a current-tree, exact-path implementation proposal and a
deterministic validation route. It proves no candidate implementation bytes,
candidate test PASS, planning acceptance/apply, selection/admission, mutation
readiness, live provider compatibility, private-data processing, real witness,
policy selection, deployment, publication, release or production readiness.
