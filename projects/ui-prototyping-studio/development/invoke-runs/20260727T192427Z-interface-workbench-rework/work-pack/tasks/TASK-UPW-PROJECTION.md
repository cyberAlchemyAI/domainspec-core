# TASK-UPW-PROJECTION — Coherent Versioned Projection

## Objective

Produce one reproducible, coherent server projection identity without changing
browser authority or UI hierarchy.

- Layer/wave: L0 / W0
- Source: `ARCHITECTURE.md` View 2–3, DDR-01, DDR-04
- Gap state: ready after Plan Distill and explicit SWU selection

## SWU-UPW-001 — Deterministic Projection Versioner

- Primary behavior: canonical whole/region JSON objects produce stable lowercase
  SHA-256 identities and reject non-JSON values.
- Dependencies: none.
- Write scope:
  - `backend/src/modules/ui-prototyping-studio/application/workbench-projection-version.ts`
  - `backend/src/modules/ui-prototyping-studio/application/workbench-projection-version.test.ts`
- Algorithm:
  1. Recursively encode objects with ascending UTF-16 key order.
  2. Preserve array order and JSON scalar encoding.
  3. Reject undefined, functions, symbols, non-finite numbers, and sparse holes.
  4. Hash UTF-8 bytes; exclude declared version fields.
  5. Recompute each region first, then the whole projection.
- Edge/failure cases: null versus absent, Unicode keys/values, negative zero,
  nested arrays, non-finite numbers, object mutation under an old hash.
- Independent acceptance: golden vectors and mismatch mutants pass without
  changing `/state` or rendering.
- Validation:
  `./node_modules/.bin/tsx --test src/modules/ui-prototyping-studio/application/workbench-projection-version.test.ts`
- Execution owner: `subagent`.
- Split analysis: serializer and hasher alone are individually testable but
  neither proves the primary identity behavior; retaining them together is the
  smallest executable semantic unit.
- Handoff: read `ARCHITECTURE.md` canonical JSON rules, UPW-FIX-001/019, and
  existing HTML `canonicalize.ts` only to avoid confusing HTML and JSON
  canonicalization.

## SWU-UPW-002 — Coherent Projection Snapshot

- Primary behavior: one accepted snapshot supplies every projection input.
- Dependencies: SWU-UPW-001 receipt.
- Write scope:
  - `backend/src/modules/ui-prototyping-studio/application/workbench-projection-snapshot.ts`
  - `backend/src/modules/ui-prototyping-studio/application/workbench-projection-snapshot.test.ts`
- Algorithm:
  1. Capture a stable input identity/epoch.
  2. Read session, revisions, variants, current content identity, staged
     candidate, comments, and handoff.
  3. Re-capture the identity.
  4. Accept equality; otherwise retry within the bounded constant.
  5. Return a typed recoverable failure on exhaustion.
- Edge/failure cases: external CLI write between every read boundary, missing
  baseline/current HTML, staged removal, changing comment count, retry
  exhaustion.
- Independent acceptance: interleaving fixture cannot emit a mixed-epoch
  snapshot.
- Validation:
  `./node_modules/.bin/tsx --test src/modules/ui-prototyping-studio/application/workbench-projection-snapshot.test.ts`
- Execution owner: `subagent`.
- Split analysis: epoch acquisition and snapshot assembly cannot pass
  independently because coherence is their joint invariant.
- Handoff: use current store ports and serialized-write behavior; introduce no
  durable store or authority.

## SWU-UPW-003 — Versioned `/state`

- Primary behavior: `/state` serves one versioned workbench projection and
  same-snapshot compatibility fields.
- Dependencies: SWU-UPW-002 receipt.
- Write scope:
  - `backend/src/modules/ui-prototyping-studio/application/governed-state-projection.ts`
  - `backend/src/modules/ui-prototyping-studio/application/governed-state-projection.test.ts`
  - `backend/src/cli/studio.ts`
  - `backend/e2e/governed-state-projection.spec.ts`
- Algorithm:
  1. Build the six region objects from the accepted snapshot.
  2. Attach exact region/whole versions from SWU-UPW-001.
  3. Derive legacy `state`, `head`, `stagedHash`, and `projection` from the same
     object.
  4. Return recoverable HTTP failure for unstable snapshot or invalid route
     data; emit no new version.
- Edge/failure cases: nullable staged state, unknown schema major, torn
  compatibility mutant, unchanged region under changed whole state.
- Independent acceptance: `/state.version` equals server recomputation and all
  compatibility fields match the projection.
- Validation:
  `./node_modules/.bin/tsx --test src/modules/ui-prototyping-studio/application/governed-state-projection.test.ts && ./node_modules/.bin/playwright test e2e/governed-state-projection.spec.ts --reporter=list`
- Execution owner: `subagent`.
- Split analysis: projection integration and endpoint exposure are one
  externally observable contract; splitting would leave no executable consumer.
- Handoff: preserve current action routes and fields additively.

## Synchronization

Each SWU must emit the Task Session result shape, then apply its exact
`WORK-PACK.md` closeout-sync row before its successor can become a candidate.
No successor is auto-selected.
