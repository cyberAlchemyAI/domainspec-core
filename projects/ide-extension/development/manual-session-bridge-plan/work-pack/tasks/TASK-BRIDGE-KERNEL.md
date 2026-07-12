# Task Contract: Bridge Kernel

## Task Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-BRIDGE-KERNEL` |
| Objective | Make the kernel the sole authority for targeting, claim ownership, recovery, terminal admission, and receipts. |
| Layer / slice / wave | L0 / S-002 / W1 |
| Dependencies | `SWU-MSB-002` and W0 exit gate. |
| Execution owner | Task Session (`local-fallback`). |

## Source Handles And Invariants

- [Cross-task decisions](../shared/cross-task-decisions.md)
- [Approved architecture](../../../manual-session-bridge-design/ARCHITECTURE-BUNDLE.md)
- Runtime anchors: `src/server.mjs`, `src/kernel/projector.mjs`, storage,
  artifacts, audit, envelope, receipt helpers, and focused API tests.
- The server never resolves or runs a skill. Pre-claim responses never contain
  skill/task payloads. A claiming session cannot ready, release, requeue, or
  mint a receipt. All mutations are serialized through the existing kernel
  mutation boundary and durably appended before success is returned.

## SWU-MSB-003: Authorization And Singleton Target

**Goal:** Turn approval into authorization evidence and add explicit
ready/unready/revoke behavior for exactly one selected request.

**Dependencies:** `SWU-MSB-002` pass.

**Exact write scope:** bridge kernel modules, `src/server.mjs`, projector/storage
integration, receipt/artifact helpers, and focused authorization/target API tests.

**Implementation rules:**

1. Approval transitions `awaiting_approval -> approved` and atomically mints one
   kernel authorization receipt; it does not terminalize or claim execution.
2. Operator ready transitions `approved -> ready_for_poll` only when no other
   ready target exists; silent replacement is forbidden.
3. Pre-claim inventory exposes opaque request handle, state, timestamps, effect
   profile, and assurance only; omit skill, task, arguments, hashes usable for
   guessing, and claim token.
4. Operator unready returns the same request to `approved` and keeps authorization.
5. Rejection/cancellation revokes future use, preserves authorization evidence
   when already approved, and records a terminal blocked/revoked disposition.
6. Every actor-sensitive action rejects missing or incorrect actor class.

**Edge cases:** duplicate approval; second ready target; stale target ID;
unready after claim; reject while ready; cancellation race; artifact append failure.

**Done criteria:** exactly one authorization receipt is durable; singleton
selection survives restart; no pre-claim response discloses the private payload;
all illegal transitions return stable non-2xx errors without partial events.

**Acceptance evidence / validation:** target/authorization API tests, binding
assertions, response-shape secrecy test, restart test, existing approval tests.

**Expected result:** `pass` with receipt and API evidence. **Handoff:**
`SWU-MSB-004` with the authorized ready fixture handle.

## SWU-MSB-004: Atomic Claim And Operator Recovery

**Goal:** Reveal one claim packet to one successful claimant and preserve
human-only recovery after explicit interruption.

**Dependencies:** `SWU-MSB-003` pass.

**Exact write scope:** bridge kernel, server, projector/storage integration,
claim attempt artifacts, and focused concurrency/recovery tests.

**Implementation rules:**

1. Claim requires one singleton ready request plus caller-generated `session_ref`.
2. Under one serialized mutation, transition ready -> claimed, create attempt
   ID/token, bind `assurance: unattested`, append event/artifact, then return the
   first response containing skill and task.
3. Zero/multiple/stale ready targets return conflict without a skill packet.
4. Duplicate/concurrent claims disclose nothing; exactly one request receives
   the packet.
5. Only the bound claimant may interrupt its active claim; interruption records
   reason/evidence and transitions to `interrupted`.
6. Only the operator may release/requeue an interrupted L0 request. Preserve
   attempt history and authorization, return to `approved`, and require a new
   explicit ready action before another claim.
7. The claimant cannot self-release, requeue, or target another proposal.

**Edge cases:** concurrent claim race; response connection loss after durable
claim; interrupt by wrong session; requeue while claimed; duplicate interrupt;
restart in claimed/interrupted state; artifact write failure.

**Done criteria:** one race winner; loser responses contain no payload; actor
separation is proved; restart preserves ownership and attempts; recovery is
visible and never automatic.

**Acceptance evidence / validation:** concurrency, replay, wrong-actor,
restart, and release/requeue tests with event/artifact assertions.

**Expected result:** `pass` with claim/recovery evidence. **Handoff:**
`SWU-MSB-005` with active and interrupted fixtures.

## SWU-MSB-005: Result Admission And Execution Receipt

**Goal:** Admit one bound terminal result and mint truthful execution evidence.

**Dependencies:** `SWU-MSB-004` pass.

**Exact write scope:** bridge kernel, server, receipt/artifact helpers,
projector/storage integration, and focused result/receipt tests.

**Implementation rules:**

1. Accept result only from the bound session/attempt for an active claim.
2. Validate terminal status (`passed`, `flagged`, or `blocked`), bounded summary,
   skill hash, validations, and evidence references; reject raw transcripts and
   out-of-scope payloads.
3. Verify authorization, request, claim, session, skill, grants, and policy bindings.
4. Append admitted result and kernel-minted `skill.execution` receipt atomically.
5. Consume authorization only at admitted terminal result; project terminal
   state only after durable receipt/artifact success.
6. Resolve every evidence ref through the artifact interface and display only
   review-safe summaries.
7. Reject duplicate, stale, wrong-session, wrong-hash, or post-release results.

**Edge cases:** terminal result racing interruption; evidence ref missing;
receipt append failure; duplicate POST; summary too large; unsupported status;
result posted after restart.

**Done criteria:** terminal projection always has a resolvable execution receipt;
authorization receipt remains separately visible and makes no execution claim;
binding failures do not mutate state.

**Acceptance evidence / validation:** result admission, duplicate result,
binding mismatch, artifact resolution, atomic failure, and restart tests.

**Expected result:** `pass` with both receipt paths and terminal projection
evidence. **Handoff:** W1 exit gate; `SWU-MSB-006` and `SWU-MSB-007` become ready.

## Synchronization

- Update task/SWU status only from Task Session results.
- Any need for leases, authentication, workers, or mutation effects is a block
  or deferred gap, never an inline extension of this task.
