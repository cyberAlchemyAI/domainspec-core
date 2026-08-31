# SWU-BWSL-002 Standard Context Pack

## Context Pack Summary

- Task: SWU-BWSL-002, one real import/submission witness
- Mode: standard
- Files selected: 12
- External primary sources selected: 2
- Selector groups: 27
- Obligation coverage: 100%
- Noise ratio: 0.0
- Output markdown: this file
- Output index: none
- Runtime handoff pack: none
- Strict coverage: pass for a no-effect readiness verdict
- Readiness verdict: BLOCK

This context pack is run-local preacceptance evidence. It is not canonical
planning, task selection, mutation admission, external-effect authorization,
or proof that a real Strava witness ran.

## Obligations

| ID | Obligation | Evidence | Coverage |
| --- | --- | --- | --- |
| O1 | Bind terminal evidence for SWU-BWSL-000 and SWU-BWSL-001. | Both implementation validation receipts rehash unchanged and report pass. | covered |
| O2 | Bind the selected OWNER-BWSL-001 policy without expanding it. | Owner selection receipt, terminal decision record, and revision-2 graph. | covered |
| O3 | Preserve the separate exact external-effect gate. | Work Pack and owner authority ceiling both withhold live authority. | covered |
| O4 | Freeze the current source, compiled binary, dependency, and runtime identities without reading secrets. | Executable Identity candidate and isolated compile comparison. | covered |
| O5 | Constrain the attempt to the selected OAuth scope and outbound-call ceiling. | Owner graph, application routes, OAuth adapter, and official Strava documentation. | covered |
| O6 | Stop instead of refreshing an expired token. | Selected policy compared with the current automatic-refresh branch. | covered; blocker found |
| O7 | Check the scopes actually granted at callback against exactly read plus activity:read. | Official Strava scope behavior compared with callback storage behavior. | covered; blocker found |
| O8 | Make cleanup independent of the primary process and reachable through Postgres. | Selected supervisor requirement compared with package scripts, server routes, Drizzle methods, and lifecycle tests. | covered; blocker found |
| O9 | Bind an exact private evidence locator before OAuth and preserve unrelated evidence. | Selected deletion contract compared with the database-generated evidence UUID. | covered; blocker found |
| O10 | Permit only the selected non-private terminal receipt fields. | Strict candidate schema compared with current private runtime response projections. | covered; producer blocker found |
| O11 | Abort when app-controlled backup, cache, private log, or temporary payload copies cannot be evaluated. | Selected deletion contract and bounded source scan. | covered; environment proof deferred |
| O12 | Keep local provider-access disposition distinct from Strava-side deauthorization. | Repository implementations and current official Strava deauthorization contract. | covered |
| O13 | Preserve geometry, scoring, release, deployment, and production claim ceilings. | Work Pack, owner graph, and receipt schema. | covered |
| O14 | Leave the deferred Invoke repair untouched. | User boundary and changed-byte inventory. | covered |

## Included Repository Context

1. projects/body-war/development/invoke-runs/20260826T132848Z-body-war-continuation-material/material-package/postimages/projects/body-war/docs/features/strava-linked-pilot/WORK-PACK.md
   - Selectors: SWU-BWSL-002, dependencies, acceptance boundary, effect gate,
     and status.
2. projects/body-war/development/implementation-readiness-runs/20260826T142600Z-swu-bwsl-000-read-only-preflight/IMPLEMENTATION-VALIDATION-RECEIPT.json
   - Selectors: result, authorization consumption, validation, and product
     postimage identity.
3. projects/body-war/development/implementation-readiness-runs/20260826T152048Z-swu-bwsl-001-read-only-preflight/IMPLEMENTATION-VALIDATION-RECEIPT.json
   - Selectors: result, authorization consumption, validation, and next route.
4. projects/body-war/development/decision-gate-runs/20260826T160535Z-owner-bwsl-001/OWNER-SELECTION-RECEIPT.json
   - Selectors: selection, authority ceiling, selection effect, and
     post-selection requirements.
5. projects/body-war/development/decision-gate-runs/20260826T160535Z-owner-bwsl-001/OWNER-BWSL-001-DECISION-RECORD.json
   - Selectors: terminal result, gate transition, blocked successor, next step,
     and claim ceiling.
6. projects/body-war/development/decision-gate-runs/20260826T160535Z-owner-bwsl-001/OWNER-BWSL-001-DECISION-GRAPH.json
   - Selectors: recommended aggregate selection, receipt fields, retention,
     deletion, residue, outbound calls, and post-selection boundary.
7. projects/body-war/app/package.json
   - Selectors: version, build/start commands, and absence of a cleanup
     supervisor or witness receipt command.
8. projects/body-war/app/server.ts
   - Selectors: OAuth start/callback at lines 476-527; activity listing at
     529-558; evidence creation at 672-739; current import receipt at 305-329;
     private evidence projection at 355-402; route table at 809-832.
9. projects/body-war/app/src/auth/strava-oauth.ts
   - Selectors: requested scope at line 17; authorization at 61-104; callback
     storage at 107-181; normal provider seam at 194-217 and 235-356;
     automatic refresh at 313-347; token exchange at 381-415.
10. projects/body-war/app/src/auth/strava-activity-provider.ts
    - Selectors: activity endpoint, exact pagination query, run allowlist,
      allowlisted translation, and refresh endpoint.
11. projects/body-war/app/src/auth/drizzle-repository.ts
    - Selectors: local provider disposition at 188-215; evidence insertion at
      310-339; exact evidence disposition at 355-388.
12. projects/body-war/app/tests/evidence-lifecycle.test.ts
    - Selectors: in-process memory idempotency, unrelated evidence
      preservation, token absence, and repeated already_absent results.

## External Primary Sources

1. https://developers.strava.com/docs/authentication/
   - Current selectors: web authorization GET, token exchange POST, returned
     granted scope may differ from requested scope, short-lived token refresh,
     and provider-side deauthorization/revoke.
2. https://developers.strava.com/docs/reference/
   - Current selector: List Athlete Activities is GET /athlete/activities,
     requires activity:read, and accepts page and per_page.

Both pages were checked on 2026-08-26. They establish provider mechanics only;
they do not authorize a call.

## Evidence And Inference

Evidence:

- SWU-BWSL-000 and SWU-BWSL-001 have unchanged terminal pass receipts.
- OWNER-BWSL-001 is terminal PASS for policy selection only.
- The current TypeScript source compiles, an isolated emit is byte-identical to
  the current dist tree, and the checked JavaScript entrypoints parse.
- The normal app path already performs the selected page-1/per_page=12 and
  page-1/per_page=50 activity requests.
- The repository has idempotent exact-row deletion and local token deletion /
  account disconnection primitives.
- The live package has no independent supervisor, no no-refresh witness mode,
  no exact granted-scope gate, and no strict durable receipt producer.
- The Postgres evidence identifier is generated at insert time, so the exact
  candidate locator is not available before OAuth under the current contract.

Inference:

- The current private HTTP responses can support an interactive attempt, but
  they cannot serve as the permitted non-private durable receipt.
- A Postgres-only independent supervisor plus an exact preallocated evidence
  locator is the smallest safe cleanup architecture under the selected policy.
- Current revokeProviderAccess proves Body War-local token disposition and
  account disconnection only. It does not prove Strava-side deauthorization.

## Excluded Context

- projects/body-war/docs/features/strava-linked-pilot/WORK-PACK.md and all
  deferred Invoke repair targets: excluded by the user's explicit boundary.
- projects/body-war/app/src/auth/memory-repository.ts: synthetic proof remains
  useful, but a memory backend cannot be independently cleaned after the
  primary process terminates.
- Credentials, .env values, database rows, private runner identity, provider
  identity, activities, and tokens: prohibited in this no-effect pass.
- Geometry, scoring, deployment, release, publication, and production
  materials: outside SWU-BWSL-002.

## Terminal Context Conclusion

The evidence is sufficient to return a strict readiness BLOCK without a human
policy decision. The next safe work is a separately admitted no-effect product
prerequisite patch. Re-entering the live witness with this unchanged blocker
fingerprint is prohibited.
