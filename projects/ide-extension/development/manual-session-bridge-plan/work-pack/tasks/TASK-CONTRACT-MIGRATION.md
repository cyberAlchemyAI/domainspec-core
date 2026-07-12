# Task Contract: Contract And Replay Migration

## Task Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-CONTRACT-MIGRATION` |
| Objective | Define a v2 bridge contract and replay model without rewriting or invalidating v1 state. |
| Layer / slice / wave | L0 / S-001 / W0 |
| Dependencies | Approved design and decision package. |
| Blockers | None for `SWU-MSB-001`. |
| Execution owner | Task Session (`local-fallback`). |

## Source Handles

- [Shared context](../shared/context.md)
- [Cross-task decisions](../shared/cross-task-decisions.md)
- [Approved decisions](../../../manual-session-bridge-design/DECISIONS.md)
- [Glossary consistency](../../../manual-session-bridge-design/GLOSSARY-CONSISTENCY.md)
- Runtime anchors: `projects/ide-extension/SPEC.md`, `schemas/`,
  `src/kernel/schema-validation.mjs`, `src/kernel/grants.mjs`,
  `src/kernel/projector.mjs`, and current schema/replay tests.

## Ordered Task Rules

1. Preserve every accepted v1 schema shape, event, receipt, and replay result.
2. Add bridge behavior as version 2; do not rewrite persisted logs or silently
   reinterpret a v1 `receipt.appended` event as a v2 execution result.
3. Make authorization, claim, and execution evidence structurally distinct.
4. Keep `skill.invoke` closed to the approved L0 `preview.read` profile.
5. Establish the complete transition oracle before adding bridge endpoints.

## SWU-MSB-001: Versioned Bridge Contract

**Goal:** Add the bounded spec, grant vocabulary, schemas, fixtures, and typed
receipt branches that later behavior must satisfy.

**Dependencies:** None.

**Exact write scope:**

- `projects/ide-extension/SPEC.md`
- `projects/ide-extension/schemas/*.schema.json` and schema fixture directories
- `projects/ide-extension/src/kernel/schema-validation.mjs`
- `projects/ide-extension/src/kernel/grants.mjs`
- `projects/ide-extension/scripts/validate-schemas.mjs`
- focused contract/schema/grant tests and required `package.json` script entries

**Implementation rules:**

1. Specify `approved`, `ready_for_poll`, `claimed`, and `interrupted` as v2
   nonterminal states before existing terminal outcomes.
2. Add `skill.invoke` only when paired with the closed L0 effect set containing
   `preview.read`; fail closed for write, shell, network, provider, or unknown effects.
3. Define target, claim, result, interrupt, and operator release requests with
   explicit actor and binding fields.
4. Model `receipt.schema.json` as a deterministic union of legacy v1 receipt,
   v2 `authorization.receipt`, and v2 `skill.execution`; v2 branches require
   `receipt_kind` and must not overlap.
5. Authorization receipts bind proposal/envelope, task, skill hash, grant hash,
   policy version, operator disposition, and `assurance: unattested`; they carry
   no execution status.
6. Execution receipts bind authorization, claim attempt, session ref, skill
   hash, admitted result status, summary, validation, and evidence refs.
7. Register every new schema explicitly and provide valid plus hostile fixtures.
8. Do not add behavior routes in this SWU.

**Edge cases and failure modes:** empty or path-like skills; blank tasks;
unknown effects; an authorization receipt with `passed`; an execution receipt
without claim/result bindings; union overlap; missing schema registry entries;
legacy fixtures accidentally forced through v2 requirements.

**Done criteria:** spec and schemas agree; valid v1/v2 fixtures pass; every
hostile fixture fails at the intended boundary; grant tests prove L0 remains
read-only; no server behavior changes.

**Acceptance evidence / validation:** `npm run validate:schemas`; focused bridge
contract and grant tests; scoped diff review proving no event-log rewrite.

**Expected result:** `pass` with changed contract paths and test commands, or
`block` naming the schema ambiguity. **Handoff:** route `SWU-MSB-002` only after
all contract fixtures pass.

## SWU-MSB-002: Version-Aware Replay And Typestate

**Goal:** Teach storage/projection to replay v1 unchanged and apply the complete
v2 bridge transition table deterministically.

**Dependencies:** `SWU-MSB-001` pass.

**Exact write scope:** `src/kernel/projector.mjs`, envelope/storage/audit
compatibility modules needed by replay, and focused v1/v2 projector tests.

**Implementation rules:**

1. Dispatch reducer behavior by persisted event/schema version.
2. Freeze v1 fixture outcomes byte-for-byte or field-for-field as appropriate.
3. Add v2 events for authorization, ready/unready, claim, interruption,
   operator release/requeue, result admission, and execution receipt append.
4. Enforce exactly one ready target in the derived workbench projection.
5. Keep authorization active through ready, claim, interruption, and explicit
   L0 release; consume it only when a terminal result is admitted.
6. Preserve every claim/release attempt and reject illegal or repeated transitions.
7. Make restart replay derive the same singleton target, state, attempts, and receipts.

**Edge cases and failure modes:** mixed v1/v2 logs; duplicate event IDs; stale
unready; terminal result replay; interrupted claim without attempt; two ready
events; unknown future version; truncated event stream.

**Done criteria:** v1 regression fixtures are unchanged; every legal v2 path
replays; every illegal transition fails closed; restart projection is stable.

**Acceptance evidence / validation:** focused projector/storage tests including
mixed-version, singleton, and restart fixtures; existing L0 lifecycle/recovery tests.

**Expected result:** `pass` with replay evidence and transition table coverage,
or `block` naming the incompatible historical case. **Handoff:** W0 exit gate,
then `SWU-MSB-003`.

## Synchronization

- Update the parent [work-pack](../../WORK-PACK.md) status/evidence only after a
  Task Session result exists.
- Record newly discovered migration residue in
  [cross-task gaps](../shared/cross-task-gaps.md); do not widen L0 silently.
