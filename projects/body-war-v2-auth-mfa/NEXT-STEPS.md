# Next Body War pilot steps

Status: planning candidate, 2026-09-07. Owner: Body War product owner.
Archive migration remains removed. Reusing private data for validation does not
restore an archive queue, legacy endpoint or automatic user-data import.

## Inspected evidence

- [Original app documentation](../body-war/app/README.md#private-strava-geometry-export)
  describes a bounded Strava exporter for GPS, distance and time streams, producing
  private `app/.runtime/geometry/strava-activities.geojson` and `export-report.json`.
  The exporter exists in the source, but those runtime files are absent from the
  inspected `../body-war` checkout. Its `app/data/` contains only `.gitkeep`.
- The preserved local `app/data/tracks.json` contains two tracks;
  `app/data/track-submissions.json` contains 28 submissions sharing one nonnumeric
  activity ID, with no top-level GPS/polyline/geometry/coordinate fields. This agrees
  with the original README's fixture-ID warning. It does not prove real-run geometry.
- [Current staging receipt](evidence/migration-removal-deployment.json) records two
  mock runs, one mock track and three evidence candidates. They are rehearsal data.
- The local project index has no Body War/TROQAR entry. The original source path is
  established by this rebuild's README and provenance/imports.json. Another working
  copy or deployment may contain ignored real exports; their location is unresolved.

## Product construction

Current frontier: finish evidence ownership/withdrawal and qualify existing real
activity data for repeatable validation. No new run is required if a suitable saved
export is found. No ontology-runtime record or selector is required for this plan.

| Step | Planned work | Acceptance evidence |
| --- | --- | --- |
| 1. Qualify saved data | Locate the original private geometry export/report; record file hashes, source, acquisition time, athlete separation, schema and stream completeness without publishing identities or coordinates. | At least one provenance-backed real activity; reject fixture IDs, malformed coordinates, nonmonotonic times/distances and mismatched stream lengths. Numeric IDs alone do not establish authenticity. |
| 2. Replay ordinary flow | Adapt one qualified export through a private test-only provider into the normal activity -> track -> consent -> evidence path. Preserve originals; label recorded replay separately from live provider reads and synthetic mocks. | Correct summary/redaction, explicit consent, ownership isolation, duplicate rejection and persistence across restart; no migration API dependency. |
| 3. Complete evidence lifecycle | Define runner-visible withdrawal and data-retention behavior; model the request, owner checks, lifecycle and response in Alch before changing adapters/UI. | Owner can withdraw; another runner cannot; retries are safe; active views and storage follow the selected retention semantics after restart. Withdrawal does not silently claim physical erasure. |
| 4. Validate geometry matching | Define candidate route geometry, match criteria and tolerances; use qualified recordings plus off-route, partial-route and noisy-GPS controls. | Repeatable match/nonmatch outcomes with explicit uncertainty. Activity geometry alone does not certify a suggested track. No scoring or territory award yet. |

Runnable now when implementation is requested: lifecycle definitions/model work and
synthetic negative controls; locating saved exports. Real-data replay and matching
are causally blocked only on a qualified dataset and the specific semantics they use.

D65 construction chain: candidate domain definitions -> authored Alch/application
ontology -> shared DomainSpec compilation -> bound implementation -> exact tested
candidate -> product review. Product approval and any later deployment remain
separate boundaries. This plan does not register admitted execution state.

## Assurance in this flow

TDE derives the added consent, ownership, withdrawal and geometry obligations while
retaining the full unverified denominator. EVF binds finite positive and cause-specific
negative cases to generated behavior, with repeats and an independent verifier.
Compiler parity must hold between Alch lowering and the native DomainSpec CLI.
ORODI rehearses health, restart persistence, fault recovery and rollback for the
changed candidate; production readiness remains a separate operational assessment.
Saved real data can validate parsing/replay and matching, but cannot prove current
OAuth, live-provider availability, token refresh or current scopes. Validate those
separately with a bounded live read when required.

## Operational support

| Task and owner | Affected stage | Causal dependency / deferred residue |
| --- | --- | --- |
| Locate ignored original export or runtime copy — agent, with location supplied by owner if discovery is exhausted | Real-data qualification | Blocks real-data replay only; do not scan credentials or copy private GPS into tracked fixtures. |
| Establish selected athlete permission and private handling — data owner | Use of real dataset | Exact prerequisite to copying/replaying another athlete's private data; inspection here emitted metadata only. |
| Package, review and update private staging — agent/operator after implementation authorization and tested candidate | Deployment | Deferred; this planning turn changes no runtime or provider configuration. |
| Public DNS/TLS, production identity/backups and independent production ORODI — operator | Production release | Deferred; does not block local model, lifecycle or replay work. |

## Open Questions

1. Where is the original ignored geometry export or working runtime containing it?
   The inspected source checkout does not contain it; the archived submissions do
   not establish real runs. Prefer finding the existing export before fetching anew.
2. Does withdrawal remove the full stored summary, or retain a minimal audit marker?
   Define duplicate/resubmission behavior alongside that decision.
3. What route-match tolerance and minimum coverage should qualify evidence?
   Keep this candidate until tested against selected real and negative examples.

## Implementation progress

Owner-authorized implementation now exposes `WithdrawEvidence` from Alch through
the generated dispatcher and browser control. The existing disposal policy selects
physical candidate/consent deletion, no tombstone, idempotent retries and fresh
consent on resubmission. API, browser and PostgreSQL tests cover this slice.

Run `npm run build` then
`node scripts/qualify-geometry.mjs <private-geojson> <private-export-report>`
to check a saved original export offline. It emits counts, hashes and explicit
provenance/permission limitations; it does not copy GPS data or make provider calls.
Structural validity cannot establish authenticity. Real replay and matching remain
blocked on the missing saved export and selected matching criteria. The owner has
been asked for its working-copy/VPS location; independent lifecycle work continues.
