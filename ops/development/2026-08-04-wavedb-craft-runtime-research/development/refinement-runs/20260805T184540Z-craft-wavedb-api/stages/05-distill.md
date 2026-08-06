# Stage 05 — Initial Distill

## Result

Pass. The target is reduced from a general Craft API to one coherent first
capability: **consult an already-built immutable snapshot without changing it**.

## Two-round trace

### Round 1 — Proposer

Proposed unit: health, space catalog, raw snapshot retrieval, normalized rows,
search, refresh, and future mutation under one API.

### Round 1 — Balancer

Rejected as overbuilt. Raw retrieval is proven at the byte layer; normalization,
search, refresh, and mutation have different evidence and effect boundaries.

### Round 2 — Proposer

Selected unit: readiness plus authorized space metadata and exact raw snapshot
retrieval from one immutable manifest-closed store.

### Round 2 — Balancer

Accepted. Readiness without retrieval proves too little; retrieval without
readiness/provenance can misstate corrupt or stale data. These pieces share one
acceptance boundary: a caller can retrieve only bytes whose record, manifest,
and response digests close over the same snapshot.

The two roles were simulated by the parent because the confirmed delegated
agents are reserved for stage 7's three design critics.

## Smallest coherent unit

`Snapshot Consultation L0`

- `GET /healthz` reports process liveness only.
- `GET /v1/status` reports snapshot readiness and non-authoritative freshness.
- `GET /v1/spaces` returns authorization-filtered metadata.
- `GET /v1/spaces/{space_id}` returns metadata and capabilities.
- `GET /v1/spaces/{space_id}/raw` returns exact UTF-8 bytes plus provenance.

No normalized row or search endpoint belongs to L0.

## Deferred components

- L1: version-specific normalizers, row capability, list/filter/lookup.
- L2: policy hardening, freshness observer, corruption/degraded-mode evidence.
- L3: separately owned snapshot builder/replacement and packaging.
- Rejected: Craft writes through the consultation API.

## Recomposition proof

L0 establishes the snapshot identity, authorization, provenance, byte
normalization, and failure vocabulary that every later row response must reuse.
L1 can add normalized rows without changing authority. L2 hardens observation.
L3 can rebuild snapshots out of band, then atomically switch the service to a new
validated immutable handle. No later layer requires L0 to gain write authority.

## Residue

- The design must specify concealment-safe errors and conditional capabilities.
- L1 cannot claim `0.1` support until fixture-backed.
- Refresh remains a separate route and lifecycle owner.
