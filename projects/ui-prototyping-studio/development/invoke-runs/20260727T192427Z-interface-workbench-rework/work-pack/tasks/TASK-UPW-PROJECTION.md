# TASK-UPW-PROJECTION — Deterministic Coherent Projection

Status: `not-started`

## Objective

Produce a deterministic, coherent, versioned `/state` response without changing
route admission policy or application authority.

- Layer/wave: L0 / W0
- Source: `ARCHITECTURE.md#workbench-projection`, DDR-01
- Scope authority: `SWU-SCOPE-INVENTORY.json` rows 001–003
- Acceptance authority: `SWU-ACCEPTANCE-MATRIX.json` assertions
  `UPW-A-001-DIGEST` through `UPW-A-003-STATE`
- Closeout authority: `CLOSEOUT-SYNC-INVENTORY.json` rows 001–003

All omitted implementation paths are unauthorized. Existing paths are bound by
SHA-256 at Task Session preflight; create-if-absent paths are bound to the
literal `ABSENT` sentinel. A mismatch blocks before mutation.

## SWU-UPW-001 — Canonical Projection Versioner

- Primary behavior: deterministic whole/region digests over exact canonical
  JSON objects.
- Semantic dependencies: none.
- Serialization-only predecessors: none.
- Exact write scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-001`.
- Inputs: projection-without-version fields and keyed region objects.
- Outputs: lowercase SHA-256 whole and region digests.
- Algorithm:
  1. Recursively reject undefined, functions, symbols, non-finite numbers, and
     sparse array holes.
  2. Sort object keys by ascending UTF-16 code-unit order; preserve array order.
  3. Encode JSON primitives with exact `JSON.stringify` semantics.
  4. Hash UTF-8 bytes and return lowercase hexadecimal.
  5. Recompute every supplied digest during contract validation.
- Failure: invalid value or digest mismatch returns a typed validation error;
  no best-effort encoding.
- Split analysis: serializer and hasher are plausible children, but neither
  independently proves the digest identity consumed by `/state`; retain.
- Acceptance/command:
  `./node_modules/.bin/tsx --test src/modules/ui-prototyping-studio/application/workbench-projection-version.test.ts`.
- Receipt field: `validation.assertions.UPW_A_001_DIGEST`.
- Owner/handoff: `subagent`; read the Architecture canonical JSON rules,
  UPW-FIX-001/019, and current HTML `canonicalize.ts` only to avoid confusing
  HTML and projection canonicalization.

## SWU-UPW-002 — Store-Token Coherent Snapshot

- Primary behavior: one accepted store epoch supplies every projection input.
- Semantic dependencies: passing SWU-UPW-001 receipt.
- Serialization-only predecessors: none.
- Exact write scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-002`.
- Authoritative token producer:
  `StudioSessionStorePort.getProjectionReadToken()`.
  - file-store implementation: literal `file:absent` when the store file does
    not exist, otherwise `file:sha256:<lowercase digest>` over the exact raw
    store-file bytes;
  - in-memory implementation: `memory:<decimal counter>` from a monotonic
    mutation counter incremented once by each mutating port operation.
- Equality rule: before and after tokens are admitted only by exact JavaScript
  string equality (`before === after`); tokens are opaque to the snapshot
  reader.
- Retry rule: `PROJECTION_SNAPSHOT_RETRY_LIMIT = 2`. One attempt means
  before-token, all projection reads, after-token. A mismatch discards the
  entire attempt. The initial attempt plus exactly two retries yields at most
  three attempts.
- Terminal failure: a third mismatch throws
  `ProjectionSnapshotUnstableError` with
  `{sessionId, attempts: 3, retryLimit: 2, beforeToken, afterToken}`; no
  snapshot/version is emitted.
- Artifact assumption: HTML refs are content-addressed and immutable once
  published; the store token therefore binds their identities, while HTML
  content is resolved from the accepted refs after admission.
- Inputs read per attempt: session, revisions, variants, current-content ref,
  staged candidate, revision-bound comments, batches needed by the inspector,
  and handoff.
- Edge cases: write between any two reads, absent store file, missing head,
  staged removal, comment append, corrupt store, and retry exhaustion.
- Split analysis: token acquisition and snapshot assembly cannot pass
  independently because before/after equality is the coherence invariant.
- Acceptance/command:
  `./node_modules/.bin/tsx --test src/modules/ui-prototyping-studio/application/workbench-projection-snapshot.test.ts src/modules/ui-prototyping-studio/infrastructure/file-store-freshness.test.ts`.
- Receipt field: `validation.assertions.UPW_A_002_COHERENCE`.
- Owner/handoff: `subagent`; do not add durable browser authority, new locking,
  or mutable artifact content.

## SWU-UPW-003 — Versioned `/state` Over Existing Routes

- Primary behavior: `/state` exposes one accepted snapshot with exact
  version/region versions and same-snapshot compatibility fields.
- Semantic dependencies: passing SWU-UPW-002 receipt.
- Serialization-only predecessors: none.
- Exact write scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-003`.
- Route boundary: this SWU consumes only the currently constructed route
  families already present in `governed-state-projection.ts`:
  `/raw/current`, `/annotate/current`, `/raw/staged`, and
  `/raw/variant/${VariantLabel}`. It accepts no request-supplied or new route
  family and makes no unknown-route failure claim. New route-family admission
  belongs only to SWU-UPW-018.
- Algorithm:
  1. Acquire the accepted snapshot from SWU-UPW-002.
  2. Build the six region data objects using only current route constructors.
  3. Compute exact region and whole digests with SWU-UPW-001.
  4. Derive legacy `state`, `head`, `stagedHash`, and `projection` from that
     same object.
  5. Return recoverable HTTP failure on snapshot exhaustion or schema failure;
     emit no new version.
- Edge cases: null staged state, unknown schema major, torn compatibility
  mutant, changed whole with unchanged region, and unavailable current HTML.
- Split analysis: projection integration and endpoint exposure are one
  externally observable compatibility contract; neither is useful alone.
- Acceptance/command:
  `./node_modules/.bin/tsx --test src/modules/ui-prototyping-studio/application/governed-state-projection.test.ts && ./node_modules/.bin/playwright test e2e/governed-state-projection.spec.ts --grep "UPW-003 versioned state compatibility" --reporter=list`.
- Receipt field: `validation.assertions.UPW_A_003_STATE`.
- Owner/handoff: `subagent`; preserve current action routes and add fields
  compatibly.

## Synchronization

Each SWU returns `task-session.swu-result.v1`, including its named acceptance
field, then routes through the exact target/permission row in
`CLOSEOUT-SYNC-INVENTORY.json`. A successor becomes a candidate only; no
successor is selected automatically.
