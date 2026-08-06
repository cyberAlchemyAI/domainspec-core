# Context Builder Runtime Handoff

- Run: `20260805T184540Z-craft-wavedb-api`
- Mode: `standard`
- Status: `pass`
- Coverage: `6/6 obligations`
- Files selected: `6/14`
- Excerpt budget: `126/280 lines`
- Protected context: private ledger payloads excluded

## Task frame

Design, but do not implement, a read-only Craft consultation API over the
verified local WaveDB snapshot. Preserve `.craft/ledger.yml` as source
authority. Treat WaveDB as a disposable derived read model. Make freshness,
provenance, privacy, schema compatibility, and observed runtime limitations
explicit.

## Obligation map

| Obligation | Selected evidence | Consequence |
| --- | --- | --- |
| Runtime proof | passing Node 26 receipt, `database`, `verification`, `authority`, `claimCeiling` | Only sequential puts plus explicit flush and exact reopen readback are admitted. |
| Preserved failure | failed atomic-batch receipt, `error.message` | Multi-record batch persistence is not an allowed adapter assumption. |
| Read normalization | importer lines 23–39 and 124–143 | Every read normalizes string or Buffer to bytes before decoding or hashing. |
| Authority | importer lines 91–118 and 189–201 | Raw source bytes and metadata are a projection; source YAML remains authoritative. |
| Craft contract | ledger entrypoint lines 37–47 and 49–93 | Human views and indexes are derived; freshness is `fresh`, `stale`, or `unknown`. |
| Row semantics | core schema lines 1–34 and 313–768 | Stable IDs are family-specific; recomposition uses a composite identity. |

## Known evidence

- `@vijayee/wavedb@0.15.8` ran under Node `v26.6.0`.
- 27 current owner ledgers, 788,960 source bytes, and 55 WaveDB records were
  verified with 411 byte-level assertions before and after reopen.
- Immediate and reopened reads each returned 46 strings and 9 Buffers.
- No row-level normalization or Craft integration was attempted.
- Live owner ledgers include schema `0.2.0` and `0.3.0`; the seed also requires
  explicit treatment of legacy `0.1`.

## Missing proof

- No row-level query model has been validated.
- No global row ID is proven across ledger spaces or schema generations.
- No freshness service, authorization policy, server, concurrency model,
  snapshot replacement protocol, or production placement is proven.
- Atomic batch persistence is contradicted by the preserved failure.

## Constraints handed forward

1. API v1 is read-only; no read route may rebuild the store or mutate Craft.
2. A response declares `authority: derived` and carries source/snapshot
   provenance plus a freshness state.
3. Raw ledger content is returned only to a caller authorized for that exact
   space; collection endpoints expose metadata only.
4. Row endpoints remain unavailable for a space until one schema-specific
   normalizer proves unique IDs and reference integrity.
5. Unsupported, ambiguous, stale, or hash-mismatched data fails closed.
6. Public generic contracts and private repository adapters have separate
   lifecycle owners and placements.

## Downstream handle

`context-builder://20260805T184540Z-craft-wavedb-api/standard`

Consume this Markdown together with `runtime-handoff.index.json`; do not expand
the source boundary without a named gap and a new decision.
