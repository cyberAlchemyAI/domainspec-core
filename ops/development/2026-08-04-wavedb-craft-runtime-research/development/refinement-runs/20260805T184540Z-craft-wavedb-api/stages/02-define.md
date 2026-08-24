# Stage 02 — Invoke Define

## Invoke result

- Mode: `define`
- Phase status: `pass`
- Target: Craft consultation API, candidate-local design cycle
- Template: DomainSpec specification baseline, selected because the target has
  explicit authority, interface, data, security, and validation aspects
- Discovery: satisfied by the confirmed Refine seed and Context Builder frame
- Distill sanity: required later at stage 5 because the original target spans
  raw snapshot access, normalization, query, refresh, and mutation concerns
- Next route: Interrogation refine-review

## Definition

The Craft consultation API is a private-by-default, read-only HTTP boundary over
one verified immutable WaveDB snapshot. It presents derived metadata and, when
authorized, exact raw ledger bytes. Schema-aware row consultation is a separate
conditional component: it becomes available per space only after a normalizer
validates that ledger's supported schema and unique row identities.

## Vocabulary

| Term | Meaning | Authority |
| --- | --- | --- |
| Craft source ledger | One owner-controlled `.craft/ledger.yml` file. | Authoritative for Craft state. |
| Snapshot | An immutable set of WaveDB records plus manifest and digests. | Derived evidence only. |
| Space | One source ledger represented in a snapshot; addressed by an opaque snapshot-local ID. | Derived locator, not semantic identity. |
| Raw representation | Exact UTF-8 source bytes and byte digest. | Faithful projection, not an editing surface. |
| Normalized row | A versioned query shape derived from one source row. | Derived and conditional on validation. |
| Freshness | `fresh`, `stale`, or `unknown`, computed against live source metadata when the deployment is allowed to inspect it. | Observation, never authority. |
| Provenance | Snapshot, source path, source byte digest, schema version, and import time bound to a response. | Evidence about derivation. |

Glossary linking is `linked` to Craft's canonical source-of-truth, stable-ID,
linking, and freshness contracts. No new canonical term is promoted.

## Goals

1. Discover authorized spaces without exposing their ledger contents.
2. Return exact raw snapshot bytes with byte digest and derivation metadata.
3. Return normalized rows only for supported, validated schema adapters.
4. Make stale, unknown, unsupported, ambiguous, and corrupt states explicit.
5. Make every response testable against the immutable snapshot manifest.

## Non-goals

- No POST, PUT, PATCH, DELETE, refresh-on-read, source edit, promotion, or
  projection regeneration.
- No claim that WaveDB is Craft authority, a production runtime, or safe for
  atomic multi-record batch persistence.
- No global row-ID namespace across spaces.
- No public publication of private paths or content.
- No row search until normalization and index integrity are validated.

## Invariants

1. Read requests have no durable effects.
2. A result always identifies itself as `derived`.
3. Raw and normalized responses bind to one immutable snapshot ID.
4. A stale or unknown projection cannot be labeled current.
5. An unsupported schema cannot fall back to best-effort row parsing.
6. Ambiguous row identity returns a conflict, never an arbitrary row.
7. Access is denied before the existence or path of a private space is revealed.
8. WaveDB values are normalized to bytes before hashing or decoding.

## MVP resource boundary

- Included: service status, authorized space catalog, space metadata, exact raw
  snapshot retrieval, and conditional row retrieval.
- Conditional after normalization proof: row listing/filtering and row lookup.
- Deferred behind independent authorization: snapshot rebuild/replace.
- Rejected: any Craft mutation through this API.

## Dispatch technique trace

- `sequence`: context evidence precedes definition and design.
- `authority_split_gate`: source ledgers, snapshot builder, and query service keep
  separate effects.
- `conditional_component`: normalized rows exist only after adapter validation.
- `protected_context_flag`: private paths/content remain response-policy scoped.
- `residue_ledger`: failed batch and mixed-type observations remain constraints.
- `handle_handoff`: downstream stages consume artifact paths, not copied ledgers.

## Acceptance boundary

The definition passes when the API can be specified entirely as a derived,
read-only consultation boundary. Runtime/server behavior, schemas, and Work Pack
remain downstream design/plan evidence, not implementation proof.

## Gaps carried forward

- Legacy `0.1` shape and migration adapter need fixture-backed discovery.
- Exact authentication principal and deployment owner are not selected.
- Snapshot replacement and concurrency belong to a future refresh capability.
- Public generic contract placement versus private adapter placement requires an
  owner decision before publication or implementation.
