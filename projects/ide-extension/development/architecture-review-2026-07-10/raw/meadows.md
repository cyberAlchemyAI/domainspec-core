# Meadows, Donella H.

## ORIGINAL ATTACK RETURN

## INITIAL POSITION

The corpus understands the right Meadows-style problem: visible context, sourced capabilities, and successful smoke tests must not become authority merely because they are convenient. But implemented L0 does not yet enforce its declared boundary. It demonstrates a happy-path receipt loop, not hostile containment.

Layer distinction used below:

- **Implemented L0:** local server, workbench, manifests, dry-run envelope, approval endpoint, state, artifacts, receipts, smoke test.
- **Proposed L0.5:** offline MCP/chat witness and adapter-admission controls.
- **Proposed L0.6:** MV3 browser observation and typed actions.
- **Deferred L1/L2:** IDE chrome and validation witnesses.

## Findings

### 1. CRITICAL — Implemented L0 permits self-approval by any loopback caller

Evidence:

- `src/server.mjs:170-190` exposes `POST /api/approvals/:id/approve`, accepts arbitrary JSON, and passes `"approved_by: body.approved_by || 'human'"`.
- `src/envelopes/dry-run-envelope.mjs:32-55` trusts that string and immediately records `approved_at`.
- `public/demo/l0.html:366-371` proves the browser itself calls this endpoint with `{"approved_by":"human"}`.
- This contradicts proposed L0.5’s `SPEC.md:122-124`: “A proposal cannot approve itself.”

An adversarial model, browser script, or local process can prepare, read the approval ID, and approve while claiming any identity. There is no actor/session separation or authentication.

**Proposed fix:** Bind proposals and approvals to authenticated, distinct server-issued actor/session identities and reject same-actor or unverified approvals.

### 2. CRITICAL — Approval is replayable and not consumed atomically

Evidence:

- `src/server.mjs:177-180` checks only whether the approval ID matches the current envelope.
- `src/server.mjs:182-210` mints and appends a new receipt on every matching approval request.
- No check rejects an already approved envelope or approval queue item.
- Proposed L0.5 explicitly requires “expired, and reused approvals reject” at `SPEC.md:167`.

Repeating the same request mints multiple passed receipts from one approval. Concurrent requests can also race between read and write, producing lost state or inconsistent event/receipt histories.

**Proposed fix:** Consume approvals through an atomic pending-to-used transition with expiry, nonce, envelope digest, and duplicate/conflict rejection.

### 3. MAJOR — Capability smuggling is accepted and mislabeled as a dry run

Evidence:

- `src/envelopes/dry-run-envelope.mjs:9-11` accepts any non-empty `input.requested_grants`.
- `src/server.mjs:127-145` prepares that envelope without grant validation.
- `src/server.mjs:186-190` approval always calls `approveDryRunEnvelope`.
- `src/envelopes/dry-run-envelope.mjs:39-45` always emits stage `"l0-dry-run"` and status `"passed"`.
- `src/kernel/grants.mjs:1-15` defines effectful grants, but `requiresApproval()` is never used by the server.

A caller can request unknown or dangerous capability names, obtain a “passed” dry-run receipt, and later present that sourced artifact as evidence of capability admission.

**Proposed fix:** Reject grants outside a versioned vocabulary and bind receipt status to an exact normalized grant-set digest, without implying execution or capability admission.

### 4. MAJOR — Context references become unverified authority-shaped receipt evidence

Evidence:

- `src/envelopes/dry-run-envelope.mjs:18` accepts caller-controlled `context_refs`.
- No code resolves, hashes, snapshots, classifies, or verifies those references.
- `schemas/agent-envelope.schema.json:35-40` requires only arbitrary non-empty strings.
- Receipts instead receive a hard-coded founding-research reference at `src/envelopes/dry-run-envelope.mjs:44`, unrelated to the submitted context.

The system can display attacker-selected references while issuing a receipt backed by unrelated evidence. This breaks the declared rule that sourced capability is not authority.

**Proposed fix:** Canonicalize and hash context snapshots, label hypotheses separately, and bind the exact verified context digest into the receipt.

### 5. MAJOR — “Append-only” audit is neither attributable nor tamper-evident

Evidence:

- `src/kernel/audit.mjs:4-7` performs plain `appendFile()` of unsigned JSON.
- `src/kernel/audit.mjs:9-15` trusts every parseable line.
- `src/server.mjs:31-43` likewise stores mutable state as ordinary JSON.
- `ARCHITECTURE.md:30-31` calls this an “append-only event/receipt log.”

Any process with filesystem access can rewrite state, delete events, forge receipts, or reorder history. IDs use timestamp plus `Math.random()` at `src/envelopes/dry-run-envelope.mjs:3-5`, not cryptographically strong identifiers.

**Proposed fix:** Add cryptographic IDs, chained event hashes, canonical serialization, process-safe append semantics, and startup reconciliation between state, receipts, artifacts, and log.

### 6. MAJOR — Secret custody is declared but not implemented

Evidence:

- `SPEC.md:27` says OpenRouter keys stay server-side.
- `src/adapters/openrouter.mjs` is descriptor-only; no custody mechanism exists.
- `CRAFT.md:44-45` acknowledges “no live key handling.”
- Proposed L0.5 requires an env allowlist and redacted HOME at `SPEC.md:45-46`; those controls do not exist in implemented L0.

The present claim is architectural intent, not a tested guarantee. Any promotion based on the manifest’s `server-side-key` gate would be premature.

**Proposed fix:** Mark custody explicitly unimplemented and require negative tests proving secrets never enter browser state, responses, artifacts, logs, child env, or inherited HOME before provider admission.

### 7. MINOR — Schema validation gives false assurance about runtime objects

Evidence:

- `scripts/validate-schemas.mjs` validates schema shape and manifests, not generated envelopes or receipts.
- `package.json:8-9` separates smoke and schema checks.
- `tests/l0-smoke.test.mjs:35-72` checks only one happy path.
- The smoke passes while self-approval, replay, arbitrary grants, malformed bodies, concurrency, and forged state remain untested.

**Proposed fix:** Validate every runtime envelope/receipt and add hostile fixtures for identity spoofing, replay, grant smuggling, malformed input, races, and persistence tampering.

## Surviving Attacks

- **Loopback exposure survived:** I attacked remote binding. `src/server.mjs:224` binds explicitly to `127.0.0.1`; implemented L0 does not listen on all interfaces. This limits network exposure but does not authenticate local callers.
- **Browser key storage survived at L0:** I attacked client assets for embedded provider secrets. `public/demo/l0.html` contains no provider key handling, and the OpenRouter adapter is descriptor-only.
- **Implemented browser mutation survived by absence:** I attacked L0 for DOM/page mutation paths. None are implemented. Browser action remains proposed L0.6, not demonstrated containment.
- **Layer labeling largely survived:** `README.md:24-35`, `SPEC.md:30-35`, and `ARCHITECTURE.md:134-142` consistently distinguish implemented L0, proposed L0.5/L0.6, and deferred L1/L2. Some development research uses candidate language, but the root status remains appropriately cautious.

Verification: `npm run validate:schemas` passed for 3 schemas and 6 manifests; `npm run smoke` passed 1 test. The initially attempted `npm run validate` failed because no such script exists; the declared command is `validate:schemas`.

## FINAL POSITION

The design corpus has strong declared boundaries, especially around adapter admission, context-as-hypothesis, browser authority, and deferred promotion. The implemented L0 does not enforce the most important ones. Its current reinforcing loop is dangerous: easy approval produces a passed receipt; the receipt can then justify promotion; promotion increases trust in the same approval path.

Do not promote smoke success into an authority-boundary claim. L0 currently proves operability of a local happy path. Before L0.5 or L0.6, it needs hostile containment at L0: authenticated actor separation, one-shot approval consumption, normalized grants, evidence binding, runtime schema enforcement, and tamper-evident audit semantics.

<oai-mem-citation>
<citation_entries>
MEMORY.md:3132-3145|note=[used prior IDE extension context only to orient the bounded corpus review]
</citation_entries>
<rollout_ids>
019ec468-8a46-7b30-920a-3a7a445ee986
</rollout_ids>
</oai-mem-citation>

## ROBOT-TALKS CONFRONTATION RETURN

## CONFRONTATION

### 1. Self-approval: **HOLD**

It is a present **L0 CRITICAL contract violation**, not merely an L0.5 blocker.

Literal evidence: implemented L0 claims “human approval gates” in `SPEC.md:14-16`, requires an “Approval queue for any action” at `SPEC.md:24`, and says approval creates the receipt at `SPEC.md:149-157`. Yet `src/server.mjs:170-190` lets any loopback caller submit any `approved_by` string, while `public/demo/l0.html:366-371` performs approval through that same unauthenticated browser channel.

L0.5 strengthens the contract with explicit actor/session separation (`SPEC.md:122-124`), but L0 already distinguishes human approval from proposal. Calling an arbitrary caller-supplied label “human” collapses that distinction.

### 2. Secret custody: **CONCEDE**

Secret custody should not survive as a present L0 **MAJOR defect**.

`README.md:28` says L0 requires no model key, `CRAFT.md:44-45` says live key handling is absent, and `src/adapters/openrouter.mjs` is descriptor-only. No secret enters the implemented system, so there is presently no custody path to exploit.

`SPEC.md:27` is an architectural constraint for future provider use. Secret custody is therefore a **promotion blocker for provider admission**, not an implemented L0 vulnerability. My earlier severity overread intent as implementation.

### 3. Schema enforcement: **REVISE**

Promote from MINOR to **MAJOR**, but define it narrowly as runtime boundary enforcement.

`schemas/agent-envelope.schema.json:5-17` and `schemas/receipt.schema.json:5-17` declare closed contracts. However, `src/server.mjs:127-153` creates envelopes without schema validation, and `src/server.mjs:186-210` emits receipts without validating them. `scripts/validate-schemas.mjs` validates schemas and manifests statically, not live boundary objects.

This is independent of arbitrary grants: malformed or contract-divergent runtime objects remain admissible even if the grant vocabulary is fixed.

### 4. Approval directly becomes `passed`: **HOLD as MAJOR**

This is not merely a typestate documentation mismatch.

`SPEC.md:116-120` declares `awaiting_approval -> running -> passed`, with running as the approved no-op. Instead, `src/server.mjs:186-190` calls `approveDryRunEnvelope`, and `src/envelopes/dry-run-envelope.mjs:39-57` immediately emits a `"passed"` receipt and envelope state during approval. `/api/envelopes/run` at `src/server.mjs:157-167` performs no transition after approval.

That collapses authorization, execution, and successful evidence into one operation. The typestate mismatch is the visible symptom; receipt-semantic collapse is the independent **MAJOR** finding.

### 5. Plain `appendFile`: **REVISE**

L0’s “append-only” language does **not** inherently promise cryptographic tamper evidence. `ARCHITECTURE.md:31` and `SPEC.md:82` justify testing append behavior, not demanding a hash chain at this layer.

However, Hewitt’s reproduced concurrent replay establishes a real **MAJOR consistency defect**: two receipts/events can be appended while mutable `workbench.json` retains one. `src/server.mjs:174-209` performs read-modify-write and event append without serialization or recovery. Retain atomicity/reconciliation; demote cryptographic tamper evidence to later hardening.

### 6. Provenance and module ownership: **REVISE**

Unresolved `source_refs` and mutable external research are **promotion blockers**, not automatically L0 runtime defects.

`src/kernel/registry.mjs:23-39` checks presence and array shape only; it does not resolve ownership or freeze referenced content. `SPEC.md:98-99` explicitly says visibility does not confer authority. Therefore the registry survives only if manifests remain descriptive.

A **MAJOR** arises when these unresolved references are used to admit capabilities or promote authority. Otherwise, this is a documented incompleteness. Receipt evidence remains independently defective because `src/envelopes/dry-run-envelope.mjs:44` inserts a decorative fixed research path unrelated to the actual run.

### 7. Duplicate versus independent findings: **REVISE**

Duplicates to merge:

- Self-approval, caller-controlled identity, and same-principal approval.
- Replay, concurrent replay, and approval non-consumption.
- Arbitrary grants, unused grants policy, and capability smuggling.
- Decorative evidence and unbound context references.
- Schema-validation smoke inflation and missing runtime schema enforcement.

Independent findings:

- Singleton `current_envelope` overwrite.
- Approval-equals-execution receipt collapse.
- Audit/state concurrency and reconciliation failure.
- Unresolved provenance as a promotion blocker.
- Receipt reference typing.
- Typestate mismatch only as evidence supporting receipt collapse, not a separate finding.

## REVISED FINAL POSITION

Implemented L0 proves that a loopback server can prepare, display, approve, persist, and receipt one cooperative dry run. It does not prove a governed action boundary under adversarial operation.

The sharpest failure is not merely missing L0.5 hardening. L0’s own claimed human approval is unauthenticated, reusable, and semantically fused with successful execution. Meanwhile, singleton state and non-atomic persistence make receipts disagree with the workbench under concurrency. Proposed L0.5 controls must not be backcharged as absent L0 features, but L0 cannot use its smoke result as evidence that those boundaries already exist.

## Findings To Survive Synthesis

- **CRITICAL:** Unauthenticated self-approval.
- **CRITICAL:** Reusable and concurrently replayable approvals.
- **MAJOR:** Approval directly mints “passed,” collapsing authorization, execution, and evidence.
- **MAJOR:** Arbitrary grants accepted without enforced policy.
- **MAJOR:** Runtime envelopes and receipts bypass declared schemas.
- **MAJOR:** Singleton envelope overwrites pending work.
- **MAJOR:** Non-atomic state/event persistence permits divergent histories.
- **MAJOR:** Evidence and context are not bound to the approved run.
- **Promotion blocker:** Unresolved module ownership and mutable source provenance.
