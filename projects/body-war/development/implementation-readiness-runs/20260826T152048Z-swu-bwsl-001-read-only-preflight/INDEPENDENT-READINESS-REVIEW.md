# SWU-BWSL-001 Independent Readiness Review

## Outcome Brief

- Verdict: `PASS` for preacceptance readiness of the revised six-target Candidate A.
- Execution status: `BLOCKED` until exact owner confirmation and the remaining declared pre-mutation checks pass.
- Reviewed envelope: `BW-BWSL001-PREFLIGHT-CANDIDATE-A`.
- Envelope SHA-256: `5028844e0671fe0f198954ee08789b68de8b503979e7d50c51bef80d6c2f58b5`.
- Envelope size: `11408` bytes.
- Authority reviewed: `preacceptance-no-effect`; `mutation_ready=false`.
- Reviewer: native bounded helper `/root/bwsl001_readiness_review`.

## Sufficiency Finding

The revised six-target envelope is necessary and sufficient for the declared sequential synthetic slice. The earlier five-target shape was insufficient because passing public `page=N` as a provider page count would fetch pages `1..N`; adding `strava-activity-provider.ts` permits an explicit start-page window while preserving the accepted direct multi-page contract.

The six owned changes are:

1. `server.ts`: reject the exact sequential replay key before provider access and return the frozen `409` payload.
2. `strava-oauth.ts`: keep fake mode repository-backed and delegate real mode through the provider.
3. `strava-activity-provider.ts`: support a bounded `startPage` while retaining direct calls as `startPage=1`.
4. `auth-consumer.test.ts`: prove endpoint identity, first submission, replay rejection, and no fetch on replay.
5. `strava-activity-provider.test.ts`: prove fake/real routing, exact provider page, bounds, and redaction.
6. `body-war-auth.e2e.ts`: prove the first PostgreSQL insert, replay rejection, and one-row preservation.

Both server consumers already call the shared `strava.listActivitySummaries` seam. Existing repository selectors can detect the exact sequential key before provider access. No repository or schema mutation is required for that deliberately narrow single-process claim.

## Frozen Semantics

- Replay key: `principal_id + suggested_track_id + provider_activity_id`.
- Existing row: reject before provider fetch.
- Result: HTTP `409`, code `evidence_candidate_replay`.
- Exact public payload: `{"error":"evidence_candidate_replay","message":"This activity already has evidence for this suggested track"}`.
- Same activity on a different SuggestedTrack is not a replay.
- Normal `page=N` requests exactly provider page `N`; it does not cumulatively request pages `1..N`.
- Fake mode must never fetch.
- Concurrent deduplication is not claimed.

## Validation Finding

The declared validation matrix is adequate only when every acceptance-critical check passes: targeted TypeScript and routing/replay tests with credentials unset; exact-page and no-fetch assertions; full app validation with no schema generation; local PostgreSQL E2E with pull disabled and guaranteed cleanup; the existing seven-test Playwright regression in fake loopback mode; exact combined ten-path status; update/create-aware whitespace checks; privacy and forbidden-surface scans; one-row preservation; and an unchanged provider-call counter on replay.

## Remaining Gates

1. Freeze one immutable owner request and obtain its exact digest confirmation.
2. Publish a new repository-local Handoff Notice for deferred SWU-BWSL-001 lifecycle synchronization.
3. Rehash all six target baselines immediately before mutation.
4. Verify no unexpected helper remains open.

## Claim Ceiling

This review supports candidate-local synthetic wiring only. It does not support live Strava compatibility, concurrent deduplication, private-data processing, planning synchronization, publication, deployment, release, or production readiness. Database uniqueness and conflict translation are mandatory before any multi-writer or production claim.

## Governance-Defect Sidecar

- Classification: `mechanical_evidence_only`.
- Root cause: the initial Context Pack rendering retained an empty terminal line in addition to its final LF.
- Affected invariant: every create target must be whitespace-clean before owner-request emission.
- Repair: one terminal LF was removed from `CONTEXT-PACK.md`; no product, planning, Invoke, or envelope byte changed.
- Revalidation: the normalized live Context Pack ends in exactly one LF, its create-file whitespace check has no diagnostic, and downstream bindings use the repaired digest.
- Renewed acceptance: not required because no owner request or acceptance existed before repair.
- Permanent regression proposal: normalize generated Markdown with `rstrip("\n") + "\n"` and add a fixture that distinguishes a clean create diff (`git diff --no-index --check` exit `1`, no diagnostics) from a whitespace diagnostic.
