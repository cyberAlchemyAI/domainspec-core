# Craft Consultation Security Boundary

Status: repaired candidate design. Authentication, deployment, and snapshot
publication owners remain unselected.

## Trust boundaries

1. Craft owners control source ledgers.
2. A separately authorized builder may read scoped ledgers and create a derived
   snapshot.
3. An external publisher may admit a fully closed, read-only/sealed snapshot.
4. The consultation service receives one logically immutable handle and has no
   source or API-visible store writer.
5. Authentication identifies a principal; policy authorizes explicit actions on
   opaque resources.
6. Callers receive only action-authorized fields.

## Required actions

- `craft:status:read`
- `craft:space:list`
- `craft:space:read`
- `craft:path:read`
- `craft:provenance:read`
- `craft:raw:read`
- `craft:rows:list` on a space/family
- `craft:row:read` on a space/family/row

No action implies another. Row authorization precedes family existence,
capability, parsing, lookup, count, and pagination observations. Deny carries no
caller-visible reason.

## Concealment and privacy

- Missing and unauthorized spaces share `404 space_not_found`; row denial and
  absence share `404 row_not_found` after space authorization.
- `/healthz` exposes no snapshot data; `/v1/status` requires authorization.
- Space IDs use a secret-keyed HMAC so private paths cannot be tested offline
  without the key. Key material is never returned, logged, or persisted in a
  cursor.
- Paths require path permission; digests and exact lengths require provenance or
  raw permission. These fields are excluded from list-only responses.
- Raw and row bodies never enter logs, traces, metrics, errors, or public
  artifacts.
- Authenticated cursor tokens bind principal/session, policy revision, visible
  resource set, action, snapshot, route scope, limit, position, version, and
  expiry; they contain no plaintext path.
- Responses are private/no-store and vary on authorization.

## Read-only and runtime enforcement

- The HTTP router registers GET/HEAD only and accepts zero body bytes.
- The adapter exposes `open`, `get`, `verify`, and `close`, not write methods.
- No request reads or writes owner `.craft/ledger.yml` files, refreshes,
  rebuilds, repairs, or switches snapshots.
- Adapter shape gives logical immutability only. Deployment admission additionally
  requires OS-level read-only access or a sealed copy, explicit ownership and
  permissions, no builder/service directory overlap, and independently verified
  fresh-process open evidence.
- Every request captures one active handle. Any post-start read/type/digest or
  WaveDB anomaly invalidates the entire handle; all data routes fail with `503`.

## Resource and parsing boundary

The exact hard ceilings in `API-CONTRACT.md` are configuration invariants.
Manifest/record checks use bounded reads or reject before allocation. YAML is
never parsed on the raw route and L1 parsing disables aliases, custom/executable
tags, and object construction. Limit breaches fail closed, produce content-free
diagnostics, and never return partial content.

## Abuse cases

| Threat | Required control |
| --- | --- |
| Enumerate private spaces | Authorize/filter before sort, count, page, or errors. |
| Guess a private path from ID | Secret-keyed HMAC; negative dictionary attack test. |
| Confirm content from digest/length | Gate both behind provenance/raw permission. |
| Probe family/schema/duplicates | Row authorization first; one external 409 for unavailable capability. |
| Replay a cursor | Bind every authorization and route dimension; authenticate and expire token. |
| Mix snapshots | One captured handle plus explicit snapshot precondition. |
| Exhaust memory/CPU | Mandatory manifest, record, YAML, time, and concurrency ceilings. |
| Mutate during service | Sealed/read-only directory, no overlap, runtime digest checks, global invalidation. |
| Infer authority/freshness | Always label derived; invalid/expired observation becomes unknown. |
| Leak diagnostics/cache | Stable concealed codes, redaction, private/no-store, vary on authorization. |

## Fail-closed states

Startup remains not-ready for an absent/invalid manifest, expected-key closure
failure, collision, limit breach, or reader error. Runtime corruption invalidates
the whole handle. L0 has no last-known-good rollback or recovery; a separate
owner must design replacement and recovery before deployment.

## Public/private placement

A data-free generic contract may later be proposed to public Arcanum only by its
owner. The DomainSpec adapter, policy mappings, keys, paths, principal bindings,
private fixtures, and deployment configuration stay private. This run authorizes
neither publication nor implementation.

## Unresolved owner decisions

- Authentication provider and principal/session format.
- Private implementation/package location.
- Snapshot builder, publisher, and optional freshness observer owners.
- OS sealing, logging retention, recovery, and deployment policy.

These block implementation handoff and deployment, not completion of this
candidate design.
