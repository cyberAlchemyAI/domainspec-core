# Ashby, W. Ross

## ORIGINAL ATTACK RETURN

# INITIAL POSITION

Ashby’s test is not whether the corpus describes governance coherently, but whether its executable variety can absorb hostile workflow variety without surrendering the declared invariants. The paper boundary is disciplined: kernel authority is local; modules and adapters are non-authoritative; effectful crossings require approval, evidence, and receipts. The implemented L0 does not yet realize that contract. It demonstrates a happy-path UI loop, not a trustworthy authority boundary.

Layer distinction used throughout:

- **Implemented L0:** local server, manifest loading, singleton envelope preparation, nominal blocking, approval endpoint, JSON state/artifact/event writes, one smoke test.
- **Proposed L0.5:** offline MCP/chat admission, actor/session separation, exact one-use approval, evidence hashing, adapter custody.
- **Proposed L0.6:** MV3 browser observation and typed browser actions.
- **Deferred L1/L2:** IDE chrome and external validation witnesses.

# FINDINGS

## 1. CRITICAL — Any caller can approve; no approving actor or session exists

**Evidence:** `src/server.mjs:170-190` accepts `POST /api/approvals/:id/approve`, takes arbitrary JSON, and supplies `approved_by: body.approved_by || 'human'`. `src/envelopes/dry-run-envelope.mjs:32-35` trusts that string without actor authentication, session identity, proposer comparison, or authorization. Yet `SPEC.md:122-124` requires “the proposing actor, approving actor/session, adapter invocation, and receipt append [to] remain separable.”

A proposer can call the approval endpoint and name itself, `"human"`, or any other identity. This is not merely missing L0.5 hardening: implemented L0 presents the endpoint as an explicit human approval gate.

**Proposed fix:** Introduce kernel-owned actor/session records and require an authenticated approval capability whose actor differs from the envelope proposer.

## 2. CRITICAL — Approval is replayable and mints unlimited receipts

**Evidence:** `src/server.mjs:177-180` checks only whether the approval ID matches the current envelope. It never requires queue state `pending`, checks prior consumption, or rejects an already approved envelope. Lines `182-210` mint and append a new receipt on every successful request. `dry-run-envelope.mjs:32-60` likewise accepts an already passed envelope.

This violates proposed L0.5’s “one explicit approval permits exactly one” invocation (`SPEC.md:163-165`) and also invalidates implemented L0 receipt fidelity: one authorization can produce arbitrarily many supposedly distinct passed receipts.

**Proposed fix:** Atomically consume approval once, reject terminal envelopes and replay, and bind approval to one envelope revision, run, grants set, and action.

## 3. MAJOR — Preparing a second envelope silently destroys the first approval context

**Evidence:** `src/server.mjs:140-144` assigns a singleton `current_envelope` while retaining all pending queue entries. Approval handling at `174-180` then resolves only against that singleton. An older pending approval remains visible but can no longer be approved.

The state model therefore does not preserve run/session separation. Parallel tabs or actors can overwrite each other, producing orphan approvals and misleading durable state. This directly anticipates the hostile-workflow tension: concurrency disproves the declared separability before MCP or browser actors arrive.

**Proposed fix:** Store envelopes by ID/run ID and resolve approvals against immutable envelope records rather than `current_envelope`.

## 4. MAJOR — Grant policy is declared but never enforced

**Evidence:** `src/kernel/grants.mjs:1-16` defines effectful grants and `requiresApproval`, but no caller invokes `requiresApproval`. `dry-run-envelope.mjs:9-25` accepts arbitrary `requested_grants` and always generates the same approval shape. `server.mjs:157-167` checks only whether `approved_at` exists; after approval it returns state without enforcing grant vocabulary, target scope, or action class.

Consequently, unknown or dangerous grants can enter the authoritative state and receive a passed receipt. Manifest `allowed_effects`, `required_gates`, and `forbidden_effects` are display metadata, not kernel policy.

**Proposed fix:** Validate requested grants against a closed kernel vocabulary and evaluate module allow/forbid/gate rules before preparation, approval, and run.

## 5. MAJOR — Approval immediately asserts execution success without a run transition

**Evidence:** `SPEC.md:114-120` declares `awaiting_approval -> running -> terminal`. But `dry-run-envelope.mjs:48-57` changes the envelope directly to `passed`, and `server.mjs:182-210` creates the receipt inside the approval endpoint. `/api/envelopes/run` at `157-167` performs no run and writes no transition.

Approval and execution are therefore collapsed. A receipt with `status: "passed"` proves only that an endpoint was called, not that a governed action ran or that evidence was evaluated.

**Proposed fix:** Make approval record authorization only; require a separate run transition and mint a terminal receipt only after kernel-observed execution and evidence collection.

## 6. MAJOR — “Append-only” receipts lack integrity, atomicity, and recovery

**Evidence:** `src/kernel/audit.mjs:4-7` performs a plain `appendFile` of unchained JSON. `src/kernel/artifacts.mjs:8-12` uses overwrite-capable `writeFile`. `server.mjs:191-209` writes artifact, then workbench state, then event with no transaction or recovery protocol. A crash can leave any subset committed; artifacts can be replaced by ID; event history has no hash chain or sequence.

`ARCHITECTURE.md:31` and `SPEC.md:82` call this an append-only event/receipt log, but append mechanics alone do not establish tamper evidence or consistency.

**Proposed fix:** Add exclusive artifact creation, monotonic event sequence plus previous-record hash, and recoverable commit ordering or journaling.

## 7. MAJOR — Receipt evidence is decorative rather than bound evidence

**Evidence:** `dry-run-envelope.mjs:41-45` accepts arbitrary string refs and defaults to a research Markdown file. `server.mjs:182-190` records a before artifact but sets `after_ref` to the invented string `state:${run_id}:passed`; no after artifact or digest is written. `receipt.schema.json:34-55` requires only non-empty strings.

Thus the implemented L0 receipt does not establish before/after identity, content integrity, envelope identity, actor identity, or evidence ownership. Proposed L0.5 correctly demands hashes (`SPEC.md:140-145`), but the underlying L0 receipt semantics are too weak to extend safely.

**Proposed fix:** Bind receipts to envelope, actor/session, immutable before/after artifact hashes, grants, and evidence digests validated by the kernel.

## 8. MINOR — “Schema validation” does not validate instances against schemas

**Evidence:** `scripts/validate-schemas.mjs:10-18` merely parses schema JSON, then invokes a bespoke manifest validator. It never validates envelopes or receipts against their schemas. The command nevertheless prints `validated 3 schemas`.

`CRAFT.md:42-43` acknowledges minimal manifest validation, but the broader command label overstates what passed.

**Proposed fix:** Compile all schemas with a JSON Schema validator and exercise valid and invalid fixtures for manifests, envelopes, and receipts.

# SURVIVING ATTACKS

- **Loopback exposure survived:** I attacked remote-host exposure; `src/server.mjs:221-226` binds explicitly to `127.0.0.1`. This supports implemented L0’s local-only claim, though it is not caller authentication.
- **Browser credential custody survived:** I searched the demo, server, adapter, and manifests for provider-key handling. No browser-side key storage or live provider call is implemented; OpenRouter remains a descriptor stub.
- **L0.5/L0.6/L1/L2 implementation inflation mostly survived:** README and architecture consistently label MCP/chat and MV3 as proposed and IDE/witness integration as deferred. No executable MCP, Chrome, VS Code, Playwright, or external authority path was found.
- **Happy-path persistence survived:** `npm run validate:schemas` and `npm run smoke` pass. The smoke test proves rendering, manifest loading, pre-approval blocking, one approval response, and persisted state/event count. It does not attack replay, concurrency, forged actors, invalid grants, tampering, or crash consistency.

# FINAL POSITION

The corpus has high paper fidelity about ownership boundaries and commendable restraint about proposed L0.5, proposed L0.6, and deferred L1/L2. Its implemented L0, however, is not yet a governed kernel. It is a deterministic demonstration in which possession of the local endpoint equals approval authority, approval equals successful execution, evidence is unverified reference text, and receipts can be replayed or left inconsistent.

The central governance failure is categorical: the code models fields named approval, evidence, and receipt, but not the invariants that make those objects authoritative. L0 should remain described as a UI and persistence witness until actor/session separation, single-use authorization, state-machine enforcement, evidence binding, and receipt integrity are executable and negatively tested.

## ROBOT-TALKS CONFRONTATION RETURN

# CONFRONTATION

## 1. Self-approval at L0

**HOLD: CRITICAL present L0 violation.**

This is not merely absence of proposed L0.5 actor/session machinery. Implemented L0 claims “approval and receipts on every effectful crossing” (`ARCHITECTURE.md:14-16`) and “explicit human approval” (`README.md:68-69`). Yet `server.mjs:170-190` accepts any caller-provided `approved_by`, defaulting to `"human"`, without establishing a human principal.

The L0 dry run is nominally no-op, but its durable effects are real: it mutates authoritative workbench state and mints a passed receipt. The endpoint can therefore manufacture the evidence that L0 claims to govern. L0.5’s stronger separation language at `SPEC.md:122-124` sharpens the required remedy; it does not create the underlying defect.

Hewitt’s same-principal reproduction confirms exploitability. It belongs with this finding rather than as a separate issue.

## 2. Secret custody

**CONCEDE: not a present MAJOR defect.**

`CRAFT.md:44-45` explicitly says the OpenRouter adapter is a stub with “no live key handling,” while `README.md:35` calls it “provider adapter only.” The browser contains no credential mechanism and no provider call. Therefore the claim at `ARCHITECTURE.md:73-75` that keys stay outside the browser is presently satisfied by non-implementation.

Secret custody remains a **promotion gate** for any live provider slice, not a defect in implemented L0. Meadows is attacking a future attack surface as though it were current executable authority.

## 3. Schema enforcement

**REVISE: MAJOR, but narrowly framed.**

My previous MINOR rating treated `validate:schemas` chiefly as label inflation. Van Lamsweerde and Hewitt are right that the consequence reaches the boundary: `scripts/validate-schemas.mjs:10-18` only parses schema documents and validates manifests through bespoke code; it never validates emitted envelopes or receipts. Meanwhile the server writes those objects as durable governance evidence.

Because `SPEC.md:26` places JSON schemas inside implemented L0 and acceptance depends on structurally meaningful envelopes and receipts, runtime/schema divergence is a **MAJOR contract-enforcement failure**. The misleading success message is secondary.

## 4. Approval directly becomes passed

**HOLD: MAJOR receipt-semantic collapse.**

This exceeds a typestate documentation mismatch. `SPEC.md:116-120` separates `awaiting_approval -> running -> passed`, but `dry-run-envelope.mjs:48-57` moves directly to `passed`, while `server.mjs:182-210` mints the successful receipt during approval. `/api/envelopes/run` at `157-167` executes and records nothing after approval.

The receipt therefore attests approval, not execution. Hewitt’s MINOR classification underweights the semantic role of a passed receipt. Even a no-op run needs a distinct kernel-observed transition if the receipt is evidence of completion.

## 5. Plain `appendFile`

**REVISE: split the claim.**

I withdraw the implication that “append-only” necessarily promises cryptographic tamper evidence or transactional recovery at L0. `SPEC.md:82` literally promises an “Append-only local event/receipt log,” and `audit.mjs:4-7` does append rather than rewrite. That narrow property survives.

However, a **MAJOR consistency defect** remains independently: `server.mjs:191-209` performs artifact write, workbench rewrite, and event append as separate operations. Concurrent replay can produce two receipts/events while a lost state update retains one, as Hewitt reproduced. The issue is cross-store receipt consistency, not failure to provide an unpromised hash chain.

## 6. Provenance and module ownership

**REVISE: promotion blockers, with one current MAJOR validation gap.**

Mutable URLs and unresolved `source_refs` do not automatically violate L0 because manifests describe modules without granting them authority (`SPEC.md:98-99`). External research provenance for proposed L0.5 is likewise not an implemented control.

But registry admission currently checks manifest shape, not whether owner routes or local source references resolve. Since L0 acceptance says manifests load, it must not be overread as ownership verification. I classify unresolved ownership and mutable provenance as **promotion blockers** for capability admission, not current authority leaks. The current MAJOR issue is that the UI/API exposes unverified declarations without machine-readable verification status.

## 7. Duplicate versus independent findings

**Duplicates:**

- Self-approval, unauthenticated approval, and same-principal approval are one finding.
- Sequential replay and concurrent replay share missing single-use consumption; concurrent lost updates add a separate consistency consequence.
- Arbitrary grants, grant smuggling, and unused `requiresApproval` are one finding.
- Decorative evidence, weak receipt references, and context-as-authority overlap when unverified strings support passed receipts.
- Schema label inflation is subordinate to missing schema enforcement.

**Independent:**

- Singleton envelope overwrite is separate from approval replay.
- Approval-to-passed collapse is separate from authentication.
- Cross-store consistency is separate from append-only mechanics.
- Provenance/ownership verification is separate from schema conformance.

# REVISED FINAL POSITION

Implemented L0 is a useful local persistence demonstration, but not yet a trustworthy governance kernel. Its decisive failures are not missing future MCP or browser controls. They are present executable defects: callers can self-approve and replay authorization; grants are not enforced; approval itself manufactures success evidence; concurrent durable records can disagree; and schemas do not constrain the objects carrying authority.

The corpus remains disciplined about keeping proposed L0.5, proposed L0.6, and deferred L1/L2 outside current claims. Secret custody, external MCP provenance, cryptographic audit integrity, and full actor/session machinery should be treated as promotion requirements unless current prose explicitly claims them as implemented.

# Findings That Should Survive Synthesis

- **CRITICAL:** unauthenticated self-approval.
- **CRITICAL:** reusable approval mints multiple receipts.
- **MAJOR:** arbitrary grants bypass dormant policy.
- **MAJOR:** approval collapses into passed execution receipt.
- **MAJOR:** singleton/concurrent state produces orphaned or inconsistent records.
- **MAJOR:** envelopes and receipts are not schema-enforced.
- **MAJOR:** evidence references do not bind passed receipts to verified before/after state.
- **Promotion blocker:** ownership and provenance declarations lack verification status.
