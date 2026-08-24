# Craft Consultation Data Model

Status: repaired candidate design, not an ingested or deployed schema.

## Authority layers

| Layer | Shape | Authority |
| --- | --- | --- |
| Source | `.craft/ledger.yml` bytes and owner lifecycle | Sole Craft state authority. |
| Snapshot | manifest plus `craft/meta/*` and `craft/raw/*` records | Disposable derived projection. |
| Normalized | version adapters, row envelopes, indexes | Derived query aid after validation. |
| API | authorization-filtered representation bound to one snapshot | Derived transport only. |

## Snapshot closure and evidence ceiling

The reader loads `craft/manifest/v1` and normalizes WaveDB values as:

```text
null -> missing failure
Buffer -> exact bytes
string -> UTF-8 bytes
other -> unsupported failure
```

The normalization claim is limited to lossless UTF-8 string-origin records and
the evidenced pairing `@vijayee/wavedb@0.15.8`, Node `v26.6.0`, linux x64.
Empty, large, multibyte, malformed UTF-8, non-string-origin, and unsupported
value fixtures remain required.

The manifest must be `craft-wavedb-snapshot.v1`, declare
`authority=derived-read-model-only` and `encoding=utf-8`, contain unique
canonical paths, bind each path to length and SHA-256, declare the exact expected
metadata/raw key set and expected record count, and fit the configured ceilings.
Every expected metadata and raw record must exist and match. Any failure makes
the whole snapshot unavailable.

This proves expected-key closure only. Current evidence does not prove WaveDB
store exclusivity or reliable enumeration of all physical keys. Extra keys are
therefore ignored and must remain unreachable: the service derives keys only
from the validated manifest and never accepts a caller-supplied WaveDB key.

`snapshot_id` is `sha256:<digest of exact manifest record bytes>`. The passing
receipt proves byte-exact immediate and same-process close/reopen reads for one
55-record snapshot. It does not prove separately launched fresh-process,
crash-restart, multi-process, locking, or production durability.

## Space representation

Base authorized metadata:

```json
{
  "space_id": "<secret-keyed opaque snapshot-local id>",
  "schema_version": "0.1|0.2.0|0.3.0|unknown",
  "authority": "derived",
  "freshness": "fresh|stale|unknown",
  "capabilities": {"raw": true, "rows": false, "row_families": []}
}
```

`source_path` is a path-authorized extension. `source_sha256` and exact
`size_bytes` are provenance-authorized extensions and are never list-only
metadata. Internally all three remain bound to the manifest entry.

Schema version is obtained only by a bounded safe parse of already verified
bytes. Parse failure preserves raw integrity but disables row capability.

## Freshness observation

The optional record is immutable and has:

```json
{
  "schema_version": "craft-freshness-observation.v1",
  "snapshot_id": "sha256:<manifest-record-byte-digest>",
  "scope": [{"path_binding": "<internal entry id>", "observed_sha256": "<hex>"}],
  "observer_id": "<private service identity>",
  "authorization_receipt": "<private receipt ref>",
  "observed_at": "<RFC3339>",
  "expires_at": "<RFC3339>"
}
```

It is valid only when it binds the active snapshot, contains exactly one entry
for every manifest path and no extras, was produced by the configured authorized
observer, has not expired, and each current source digest is compared with that
entry's `source_sha256`. All match means `fresh`; any mismatch/missing source
means `stale`; absent, partial, unauthorized, invalid, or expired means
`unknown`. Observation does not change authority or trigger rebuild/promotion.

## Normalized row envelope

```json
{
  "space_id": "<space>",
  "family": "contexts",
  "row_key": "CTX-EXAMPLE",
  "source_schema_version": "0.3.0",
  "source_id_field": "context_id",
  "row": {},
  "snapshot_id": "sha256:<manifest digest>",
  "authority": "derived"
}
```

Identity is `(space_id,family,row_key)`. The 0.3.0 core ID fields are
`context_id`, `artifact_id`, `description_id`, `definition_id`, `gap_id`,
`relation_id`, `item_id`, and `decision_id`; recomposition uses a length-prefixed
encoding of `(child_id,parent_id)`. Any duplicate disables row capability for
the whole space. Duplicate details are internal.

## Adapter and index contract

Each pure adapter declares exact source versions, families, source ID fields,
transform, reference rules, unknown-field policy, limits, fixture hashes, and a
validator receipt. It never rewrites source or silently upgrades unknown shapes.

| Source version | Current status | API behavior |
| --- | --- | --- |
| `0.3.0` | Canonical contract known; adapter unimplemented. | Raw yes; rows off until tests pass. |
| `0.2.0` | Live ledgers observed; adapter contract absent. | Raw yes; rows off. |
| `0.1` | Requested; no local fixture proven. | Raw yes if snapshot-valid; rows off. |
| Other/missing | Unsupported. | Raw yes if snapshot-valid; rows off. |

An L1 index is constructed outside requests, in memory or in a separate derived
snapshot. It contains only `(family,row_key)->locator` plus validated filter
fields and binds source digest, snapshot ID, adapter/index version, and receipt.

## Runtime and replacement boundary

The service handle is only *logically immutable*: its adapter exports no writer,
but that is not filesystem sealing. Admission requires an externally owned,
read-only or sealed-copy store; builder and service must never overlap on the
same directory. Every raw read is checked against the in-memory validated
manifest. Any later missing value, type anomaly, digest mismatch, WaveDB error,
or underlying mutation signal atomically invalidates the handle and makes every
data route return `503` until restart with a newly admitted snapshot.

L0 has no replacement, rollback, quarantine, or automatic recovery. It remains
unavailable on corruption. A future owner must separately design and test
`prepare -> verify with a separately launched reader -> publish external atomic
pointer -> acquire -> drain -> retire`, plus rollback, crash transitions, lock
contention, multi-reader behavior, retry bounds, and orphan cleanup. The failed
atomic-batch path remains forbidden.

## Provenance ceiling

Existing evidence proves one exact sequentially written 55-record experiment
and same-process reopen. It does not prove adapters, indexes, separately launched
reopen, exclusivity, locking, immutability, replacement, recovery, or deployment.
