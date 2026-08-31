# SWU-BWSL-001 Standard Context Pack

## Context Pack Summary

- Task: `SWU-BWSL-001` normal endpoint and SuggestedTrack wiring
- Mode: `standard`
- Files selected: `14`
- Snippets selected: `23`
- Obligation coverage: `100%`
- Noise ratio: `0.0`
- Output markdown: this file
- Output index: none
- Handoff pack: none
- Session evidence path: this run-local preflight directory
- Strict coverage: `pass`
- Blockers: `1` exact candidate authorization blocker

This pack is run-local execution-preparation evidence. It is not canonical
planning, task selection, mutation admission, or authority.

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Prove `SWU-BWSL-000` is complete on the live bytes. | implementation receipt plus exact eight-postimage rehash | covered |
| O2 | Route normal activity listing through the provider seam without breaking fake mode. | staged Work Pack; `strava-oauth.ts`; provider tests | covered |
| O3 | Make SuggestedTrack activity lookup use the same route. | `server.ts` activity and evidence handlers | covered |
| O4 | Preserve synthetic fake-provider API/UI/E2E behavior and repository isolation. | server adapter construction; auth test; Postgres E2E; browser spec | covered |
| O5 | Define replay/deduplication behavior explicitly. | current repository/schema absence plus Candidate A rejection policy | covered by proposed owner decision |
| O6 | Keep activity/evidence output token-free and coordinate-free. | provider allowlist; server redaction; existing privacy assertions | covered |
| O7 | Prohibit live network, credentials, and private runner data in this SWU. | direct user boundary; Handoff Notice; fake-mode validation contract | covered |
| O8 | Freeze exact write scope, baselines, and acceptance-critical validation. | Candidate Envelope | covered |
| O9 | Preserve deferred Invoke repair and stale canonical planning as explicit residue. | live Work Pack/Craft hashes; terminal receipt boundaries | covered |

## Included Context

- `projects/body-war/development/implementation-readiness-runs/20260826T142600Z-swu-bwsl-000-read-only-preflight/IMPLEMENTATION-VALIDATION-RECEIPT.json`
  - O1, O7, O9: selectors `result`, `product_postimages`, `runtime_wiring`,
    `validation`, `boundaries`, and `claim_ceiling`.
- `projects/body-war/development/invoke-runs/20260826T132848Z-body-war-continuation-material/material-package/postimages/projects/body-war/docs/features/strava-linked-pilot/WORK-PACK.md`
  - O2-O8: selectors `SWU-BWSL-001`, `OWNER-BWSL-001`, dependency order,
    validation surface, and execution ceiling.
- `projects/body-war/docs/features/strava-linked-pilot/WORK-PACK.md`
  - O9: current canonical Python-era plan, retained only to prove drift and
    non-authority for the candidate lane.
- `.arcanum/handoff-notices/notices/HN-30108A027C74.json`
  - O7, O9: selectors `boundaries`, `authority`, and `transport_claim`.
- `projects/body-war/.craft/ledger.yml`
  - O9: selectors `active_blockers`, `next_moves`, and
    `BLK-STRAVA-ACTIVITY-001`; the ledger has not incorporated BWSL-000.
- `projects/body-war/app/server.ts`
  - O3-O6: symbols `createAuthComponents`, `handleActivities`,
    `handleSuggestedTrackEvidenceCreate`, and `redactedActivitySummary`.
- `projects/body-war/app/src/auth/strava-oauth.ts`
  - O2-O4: symbols `listActivitySummaries` and
    `listProviderActivitySummaries`.
- `projects/body-war/app/src/auth/strava-activity-provider.ts`
  - O2, O6, O7: provider bounds, injected fetch, run filtering, allowlist,
    safe-error mapping, and refresh behavior.
- `projects/body-war/app/src/auth/body-war-repository.ts`
  - O4, O5: current evidence list/add contract used for a pre-fetch replay
    check without repository/schema mutation.
- `projects/body-war/app/src/infrastructure/postgres/schema.ts`
  - O5: evidence table currently has no uniqueness constraint; this prevents
    Candidate A from claiming concurrency-hard deduplication.
- `projects/body-war/app/tests/auth-consumer.test.ts`
  - O3-O7: memory/fake endpoint, evidence submission, status transition, CSRF,
    and redaction assertions.
- `projects/body-war/app/tests/strava-activity-provider.test.ts`
  - O2, O4, O6, O7: injected provider fixtures, bounds, allowlist, token
    rotation, and safe errors.
- `projects/body-war/app/e2e/body-war-auth.e2e.ts`
  - O3-O7: fake gateway plus real PostgreSQL lifecycle witness.
- `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts`
  - O4, O6: browser listing, selection, submission, safe copy, and mobile
    regression.

## Evidence And Inference

Evidence:

- all eight BWSL-000 postimages match the terminal receipt by SHA-256 and size;
- current `npm run validate` passes `37/37` and reports no schema changes;
- both normal server handlers call `strava.listActivitySummaries`;
- the adapter's existing normal method is repository-backed while the additive
  provider method is already tested and unwired;
- no current contract defines duplicate evidence attachment behavior.

Inference proposed for owner review:

- switching inside the adapter remains the smallest server-facing seam because
  both server consumers already share the normal method;
- the provider primitive must add an exact start-page window so the public
  `page` query remains a page number instead of silently becoming a count of
  pages from page 1;
- fake mode should remain repository-backed and must fail on any fetch;
- a sequential duplicate for the same principal, SuggestedTrack, and provider
  activity should return a stable `409` before provider access;
- database-level concurrency uniqueness is a later hardening concern and is
  not proved by this synthetic single-process SWU.

## Excluded Candidates

- `projects/body-war/app/static/app.js` — generic API consumer needs no byte
  change; browser regression covers it.
- `projects/body-war/app/src/auth/memory-repository.ts` and
  `drizzle-repository.ts` — Candidate A performs the bounded replay check via
  the existing list contract; it makes no concurrency-hard repository claim.
- `projects/body-war/app/src/infrastructure/postgres/schema.ts` and
  `projects/body-war/app/drizzle/` — no schema/migration mutation is needed for
  the explicitly bounded sequential-replay policy.
- Invoke/Craft/planning targets — lifecycle synchronization is deliberately
  deferred and cannot be smuggled into product execution.
- credentials, private evidence, deployment, and real Strava — prohibited
  external-effect scope owned by later gates.

## Next Actions

1. Complete independent review of Candidate A and reconcile any scope defect.
2. Validate the option-admissibility request and freeze one exact owner request.
3. Stop for exact digest confirmation before any product mutation.
