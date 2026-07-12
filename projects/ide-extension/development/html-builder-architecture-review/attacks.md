# HTML Builder Architecture Review - Attacks

Dispatch: `2026-07-12-html-builder-architecture-review`

Check-tension gate: checker PASS; reviewer PASS.

## Abramsky, Samson - Initial Position

**INITIAL POSITION**

The evolution is not yet architecturally closed. V0’s algebra is:

```text
Publish(path, metadata, bytes)
  = NoOp                         if hash(bytes) = current hash(path)
  | Append Published(surface, revision(hash(bytes)))

Interact(surface, revision, event)
  = Append Interaction           iff revision = globally current revision
```

A defensible operation algebra needs at least:

```text
Command = Navigate(destination)
        | Transform(mode, path, target?, expected_revision, payload,
                    operation_id)

mode = append | rebuild | replace
target = whole_document | declared_region(region_id)
```

with invariants: serialized compare-and-swap, one durable result per `operation_id`, replay-deterministic output, workspace authority preserved, and omitted `target` retaining whole-document behavior.

**Findings**

1. **CRITICAL — Builder mutation has no authority or approval boundary.**\
   Evidence: `projects/ide-extension/ARCHITECTURE.md:14-16` requires approval and receipts for effectful crossings; `projects/ide-extension/SPEC.md:96-97` excludes filesystem writes without explicit approval and receipt; authorship currently belongs to the active session at `projects/ide-extension/ARCHITECTURE.md:171`. A server-side append/rebuild/replace operation silently transfers HTML authorship and filesystem authority to the server.\
   **Proposed fix:** Specify whether builders return candidate bytes or mutate files; require the existing approval/receipt boundary for any server-side write.

2. **CRITICAL — Operations cannot be replayed from the current event model.**\
   Evidence: the workspace file is canonical and the projection stores no HTML body at `projects/ide-extension/ARCHITECTURE.md:160-162`; replay validation reconstructs publish requests only from path/title/kind at `projects/ide-extension/src/server.mjs:163-169`; content retrieval rereads mutable workspace bytes at `projects/ide-extension/src/server.mjs:642-660`. An `append` or `replace` event without base bytes, payload, and resulting artifact cannot reconstruct its effect.\
   **Proposed fix:** Persist a content-addressed result artifact plus base/result digests and normalized operation input, or explicitly declare operations non-replayable commands followed by ordinary full-document publication.

3. **CRITICAL — Read-before-queue permits stale-base transformations and lost updates.**\
   Evidence: publication reads the file before entering serialization at `projects/ide-extension/src/server.mjs:580-597`; only projection reconciliation and commit occur inside the queue at `projects/ide-extension/src/server.mjs:597-622`. Two transforms can therefore derive from the same base while committing in completion order.\
   **Proposed fix:** Require `expected_revision_id` and perform base verification, canonical reread, transformation, write, and event commit within one serialized compare-and-swap operation.

4. **MAJOR — Candidate operation names do not form disjoint semantics.**\
   Evidence: V0 “Refresh” is a display witness at `projects/ide-extension/ARCHITECTURE.md:173-174`, while publication creates complete revisions at `projects/ide-extension/SPEC.md:250-254`. `navigate/redirect` concerns client control, `append/replace` concerns content transformation, and `rebuild/refresh` presently overlaps established display terminology.\
   **Proposed fix:** Separate navigation commands from content transformations and reserve `refresh` for display reload; define `rebuild` by deterministic inputs and postcondition.

5. **MAJOR — Existing hash idempotency is insufficient for operation retries.**\
   Evidence: V0 idempotency compares only the current content hash at `projects/ide-extension/src/kernel/canvas.mjs:62-65`; a successful append retried against its own result produces different bytes and therefore appends twice.\
   **Proposed fix:** Require a caller-supplied `operation_id`, persist its normalized input digest and result revision, and reject conflicting reuse.

6. **MAJOR — Region targeting is not currently additive to the identity model.**\
   Evidence: one path identifies one entire logical surface at `projects/ide-extension/SPEC.md:250-252`; revisions describe complete-file reads at `projects/ide-extension/SPEC.md:245-246`; the data model has no region identity or declaration at `projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:21-46`. Ad hoc selectors would make operation meaning depend on incidental markup.\
   **Proposed fix:** Keep `whole_document` as the default target and introduce optional author-declared, stable region IDs with uniqueness, missing-target, and duplicate-target rules.

7. **MINOR — Same-byte publication discards metadata updates.**\
   Evidence: the idempotent branch returns the existing surface before applying `title` or `kind` at `projects/ide-extension/src/kernel/canvas.mjs:62-65`; those fields are assigned only for a new revision at `projects/ide-extension/src/kernel/canvas.mjs:78-86`.\
   **Proposed fix:** Declare metadata immutable, include it in publication identity, or append a distinct metadata-change event.

**Questions For Empirical/Adversarial Disagreement**

1. Do builders mutate the canonical workspace file, produce candidate HTML, or only consolidate operation proposals?
2. Is `navigate/redirect` durable ordered intent, an immediate HTTP response, or a browser-only command?
3. Must replay reproduce final bytes, or only prove that externally stored bytes once matched a digest?
4. Is operation order request-arrival order, queue-entry order, or explicit sequence order?
5. Does `rebuild` replace the whole document from declared sources, and how does it differ from `replace`?
6. On a missing region, must the command fail, create the region, or fall back to whole-document behavior?
7. Are region IDs stable across rebuilds, and who owns their declaration?
8. Should same bytes with changed title/kind create a new durable state transition?

## Abramsky, Samson - Final Robot-Talks Position

# FINAL POSITION

The peers reinforce the central conclusion: the operation API is not admissible until it shares one concurrency, recovery, and idempotency model with whole-document publication.

## 1. Findings That Survive Unchanged

1. **CRITICAL — Builder mutation has no authority or approval boundary.**\
   Evidence: [ARCHITECTURE.md:14](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:14) requires approval and receipts for effectful crossings; [SPEC.md:96](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:96) excludes filesystem writes without explicit approval and receipt; authorship currently belongs to the active session at [ARCHITECTURE.md:171](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:171).\
   **Fix:** Define builders as candidate producers unless explicitly approved to mutate the canonical file, with receipts binding base, intent, and result.

2. **CRITICAL — Operations cannot be replayed from the current event model.**\
   Evidence: the workspace file is canonical and projection stores no HTML body at [ARCHITECTURE.md:160](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:160); replay validation reconstructs only path/title/kind at [server.mjs:163](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:163); content retrieval rereads mutable workspace bytes at [server.mjs:642](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:642).\
   **Fix:** Persist normalized intent, base digest, immutable result bytes/artifact, and result digest behind one recoverable operation record.

3. **CRITICAL — Read-before-queue permits stale-base transformations and lost updates.**\
   Evidence: publication reads before serialization at [server.mjs:580](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:580); reconciliation and commit enter the queue only at [server.mjs:597](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:597).\
   **Fix:** Require `expected_revision_id` and perform verification, transformation, materialization, and commit within the serialized compare-and-swap boundary.

4. **MAJOR — Existing hash idempotency is insufficient for operation retries.**\
   Evidence: V0 compares only the current content hash at [canvas.mjs:62](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:62); idempotent publication emits no event at [server.mjs:600](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:600).\
   **Fix:** Persist a caller-stable `operation_id`, normalized request digest, status, and original result revision independently of output hash.

5. **MAJOR — Candidate operation names do not form disjoint semantics.**\
   Evidence: V0 Refresh is display behavior at [ARCHITECTURE.md:173](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:173), whereas publication creates complete revisions at [SPEC.md:250](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:250).\
   **Fix:** Separate ephemeral navigation/display commands from revision-producing transformations and define `rebuild` independently of `refresh`.

## 2. Findings Revised Or Dropped

**Revised — Region targeting is not merely missing; mixed compatibility makes it destructive.**\
Evidence remains: identity stops at path/surface/revision at [SPEC.md:241](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:241), while unrestricted whole-file publication remains accepted at [server.mjs:568](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:568). A stale V0 publisher can erase a valid region operation even if region semantics are otherwise perfect.\
**Fix:** Require exactly-one author-declared region identity plus base-revision CAS, and prohibit unconditional V0 publication once a surface becomes operation-enabled.

**Revised — Same-byte metadata behavior becomes a contract question, not a primary blocker.**\
The behavior remains real at [canvas.mjs:62](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:62) and [canvas.mjs:78](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:78), but it should be resolved inside the new command identity rules. I demote it from an independent finding.

**Adopted — Coherent-read admission.**\
The peer correctly identifies `stat` followed by unguarded `readFile` at [canvas.mjs:37](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:37) and [canvas.mjs:46](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:46). Builders must materialize through atomic rename or immutable server-owned bytes before publication.

I do not adopt the cursor issue: it is valid V0 hardening, but orthogonal to the proposed operation algebra.

## 3. Disagreements With Peers

- Requiring every pre-operation region digest to remain unchanged after `append` is too strong. Appending can legitimately alter the target container’s normalized DOM. Preservation must name unaffected regions, not demand global digest invariance.
- Author-declared region IDs are insufficient alone. They need uniqueness, exactly-one cardinality, base-revision binding, and preferably a target fingerprint.
- Immutable snapshots alone are insufficient. The operation’s accepted intent and materialized result must be recoverably linked; otherwise crash recovery cannot distinguish “never applied” from “applied but unpublished.”
- `navigate/redirect` should not share the revision algebra. It needs a separately acknowledged command stream with explicit persistence and ordering semantics.

## 4. Recommended Compatibility Boundary

Add a one-way surface mode:

```text
mode = whole_file_v0 | operations_v1
```

- New surfaces default to `whole_file_v0`: existing unconditional complete-file publication remains unchanged; operation requests reject.
- Promotion to `operations_v1` requires an explicit command against the current revision.
- Once promoted, every content mutation, including complete-document replacement, requires `operation_id` plus `expected_revision_id`.
- Legacy `/api/canvas/publish` requests against that surface reject with `409 operation_surface_requires_cas`.
- `target` defaults to `whole_document`; author-declared regions are optional refinements, never a replacement for whole-document behavior.
- Returning to V0 requires a new surface identity, preventing silent compatibility rollback.

This is the smallest boundary that preserves V0 while preventing mixed-client erasure.

## Ashby, W. Ross - Initial Position

**INITIAL POSITION**

The V0 display protocol converges adequately after missed SSE notifications because clients refetch current projected state. The proposed builder/consolidator API does **not yet have a defensible convergence model**. Operations introduce intent, retries, partial materialization, and stale targets that content-hash publication alone cannot represent.

**Findings**

1. **CRITICAL — No atomic recovery boundary between workspace mutation and publication.**\
   Evidence: the workspace file is canonical while projection stores no body ([ARCHITECTURE.md:160](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:160)); content is later reread from that mutable file ([server.mjs:642](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:642)).\
   Failure: a builder writes HTML and the server crashes before publishing; after restart, projection names the old revision while its bytes are permanently unavailable via `409 revision_changed`. Retrying an `append` may then duplicate content.\
   Proposed fix: persist an operation ID, base revision, operation intent, and resulting immutable bytes/event as one recoverable transaction before advancing current revision.

2. **MAJOR — Rapid publications can commit in an order different from their file reads.**\
   Evidence: file reading occurs before entering the mutation queue ([server.mjs:580](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:580)); reconciliation and publication occur only afterward inside it ([server.mjs:597](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:597)).\
   Failure: request A reads revision A, request B reads newer revision B, but scheduling admits B then A; the system converges backward to stale bytes.\
   Proposed fix: perform read/build plus base-revision validation inside the serialized boundary, with compare-and-swap against an explicit expected revision/hash.

3. **MAJOR — “One complete read” does not guarantee one coherent document.**\
   Evidence: implementation performs `stat` followed by an unguarded `readFile` ([canvas.mjs:37](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:37), [canvas.mjs:46](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:46)); the plan nevertheless treats this as a complete-read boundary ([IMPLEMENTATION-PLAN.md:109](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:109)).\
   Failure: rebuild truncates and rewrites while publication reads, admitting partial assembly as a valid revision.\
   Proposed fix: require atomic temp-file rename from builders or verify a stable file identity/hash across repeated reads before admission.

4. **MAJOR — Hash idempotency is insufficient for operation retry semantics.**\
   Evidence: equal content hash immediately returns the existing surface/revision ([canvas.mjs:62](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:62)); the server emits no event or notification for that path ([server.mjs:600](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:600)).\
   Failure: after a lost response, retrying `append` cannot distinguish “previous attempt committed” from “operation never ran”; `navigate/redirect` may also have no document-hash change and vanish entirely.\
   Proposed fix: give every operation a caller-stable idempotency key and durable accepted/applied/rejected result independent of output hash.

5. **MAJOR — Region targeting has no stale-target contract.**\
   Evidence: current schemas cover only whole-document publish and revision-bound interaction ([SPEC.md:231](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:231)); the only stale revision admission check currently protects interactions ([server.mjs:536](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:536)).\
   Failure: a delayed `replace` prepared against revision N can silently modify a same-named but semantically different region rebuilt in revision N+1.\
   Proposed fix: require `base_revision_id` plus stable author-declared region identity/fingerprint, rejecting missing, ambiguous, or changed targets.

6. **MINOR — An ahead-of-server cursor causes permanent missed interactions.**\
   Evidence: any safe integer is accepted and `next_cursor` preserves `max(after, interactionCursor)` ([server.mjs:504](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:504), [server.mjs:519](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:519)).\
   Failure: after state restoration or cursor corruption, `after=1000` against server cursor 20 suppresses events 21–1000 forever.\
   Proposed fix: reject cursors beyond the current high-water mark or return an explicit reset/reconciliation response.

**Questions For Other Attackers**

- Would a formal-methods attacker accept immutable revision snapshots, or require operation intent and materialization to share one linearizable commit point?
- Would a concurrency attacker permit last-writer-wins for whole-document operations, or require every mutating operation to carry `expected_revision_id`?
- Would an adversarial-input attacker consider author-declared region IDs sufficient, or require structural fingerprints and uniqueness proofs?
- Should `navigate/redirect` be durable canvas state, an ephemeral notification, or an acknowledged command stream? Those choices have materially different restart semantics.

## Ashby, W. Ross - Final Robot-Talks Position

# FINAL POSITION

The confrontation strengthens the core conclusion: operation-enabled mutation cannot safely share an unconditional write surface with V0 publication. Serialization, hashes, and notifications are insufficient without a revision-CAS boundary and durable operation identity.

## 1. Findings That Survive Unchanged

1. **MAJOR — Rapid publications can commit in an order different from their file reads.**\
   Evidence: file reading occurs before entering the mutation queue ([server.mjs:580](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:580)); reconciliation and publication occur only afterward inside it ([server.mjs:597](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:597)).\
   Proposed fix: perform read/build plus base-revision validation inside the serialized boundary, with compare-and-swap against an explicit expected revision/hash.

2. **MAJOR — “One complete read” does not guarantee one coherent document.**\
   Evidence: implementation performs `stat` followed by an unguarded `readFile` ([canvas.mjs:37](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:37), [canvas.mjs:46](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:46)); the plan nevertheless treats this as a complete-read boundary ([IMPLEMENTATION-PLAN.md:109](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:109)).\
   Proposed fix: require atomic temp-file rename from builders or verify stable file identity/hash across repeated reads before admission.

3. **MAJOR — Hash idempotency is insufficient for operation retry semantics.**\
   Evidence: equal content hash immediately returns the existing surface/revision ([canvas.mjs:62](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:62)); the server emits no event or notification for that path ([server.mjs:600](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:600)).\
   Proposed fix: give every operation a caller-stable idempotency key and durable accepted/applied/rejected result independent of output hash.

4. **MINOR — An ahead-of-server cursor causes permanent missed interactions.**\
   Evidence: any safe integer is accepted and `next_cursor` preserves `max(after, interactionCursor)` ([server.mjs:504](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:504), [server.mjs:519](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:519)).\
   Proposed fix: reject cursors beyond the current high-water mark or return an explicit reset/reconciliation response.

## 2. Revised Or Dropped

**Revised: atomic recovery becomes a replay/authority finding.**\
My original finding correctly identified the crash window, but the formal attacker identifies the deeper defect: the event model cannot reconstruct or prove a transformation because projection retains no bytes ([ARCHITECTURE.md:160](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:160)) and retrieval rereads mutable workspace state ([server.mjs:642](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:642)). The requirement should be a durable normalized command plus content-addressed result, or an explicitly non-replayable builder whose only durable transition is an ordinary full-document publication.

**Revised: stale-target protection must include cardinality and mixed-client conflicts.**\
A `base_revision_id` and region fingerprint are necessary but insufficient. Region operations need exactly-one-target validation, stable author-declared IDs, and protection from stale V0 clients that can overwrite the complete document through the unrestricted publish route ([server.mjs:568](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:568)).

**Dropped: none.**\
The cursor finding is peripheral to builder semantics, but remains a real missed-notification recovery defect.

## 3. Disagreements With Peers

- I do **not** accept that every server builder necessarily violates the approval boundary. A pure builder returning candidate bytes has no filesystem effect; approval becomes mandatory when the server writes canonical workspace state or advances durable current state.
- I would not define `append` as preserving every prior DOM-region digest. Browser parsing can legitimately alter normalization without changing intended structure. Preservation must be defined against one authoritative server-side parser and declared-region model.
- `navigate/redirect` should not enter the transformation algebra. It is a separately acknowledged navigation channel with its own ordering and restart policy.
- A mutation queue alone is not a transaction. Even moving work inside it leaves crash consistency unresolved unless command, result bytes, canonical write, and revision advancement have an explicit recovery protocol.

## 4. Recommended Compatibility Boundary

Make surface mode immutable:

```text
surface_mode = whole_file_v0 | operations_v1
```

- `whole_file_v0`: accepts the existing unconditional complete-file publish API and rejects operation commands.
- `operations_v1`: rejects legacy `/api/canvas/publish`; every mutation, including whole-document replacement, requires `operation_id`, `expected_revision_id`, explicit target, and durable result revision.
- Migration creates or explicitly promotes to a new operation-enabled surface; it never silently changes an existing V0 surface.
- `navigate/redirect` remains outside both content mutation modes.

This boundary prevents a stale V0 publisher from erasing region operations while preserving V0 behavior exactly where it was promised.

## Turing, Alan - Initial Position

**INITIAL POSITION**

The proposed operation API is not yet safe to admit. V0’s invariant is whole-file replacement guarded by a complete-content hash; none of the reviewed contracts define operation preconditions, selector cardinality, idempotency, ordering, or compatibility rules. Regions therefore do **not** remain demonstrably additive.

**Findings**

1. **CRITICAL — Mixed V0/new clients can erase additive region updates.**\
Evidence: V0 makes the workspace file canonical and republishes changed bytes as a new whole-document revision ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:250)); the server still accepts unrestricted whole-file publication ([server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:568)).\
Counterexample: client A appends region `#notes`; stale V0 client B republishes its complete pre-append file, producing a valid revision that silently removes `#notes`.\
Proposed fix: Define one revision-CAS commit boundary shared by full-document and operation clients, with explicit conflict responses rather than last-writer replacement.

2. **CRITICAL — Serialization alone does not prevent stale-base operation commits.**\
Evidence: the current server reads bytes before entering the mutation queue ([server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:580), [server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:597)); revision identity is generated only afterward ([canvas.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:69)).\
Counterexample: two scripts read revision R; append A commits R1, then replace B computed from R commits R2 and loses A despite serialized event append.\
Proposed fix: Require `base_revision_id` or content hash on every mutating operation and reject mismatches inside the mutation queue.

3. **MAJOR — Selector-based replacement has undefined cardinality and identity semantics.**\
Evidence: the formal request contract defines only path/title/kind and interaction bindings, with no selector or region contract ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:231)); current identity exists only at path/surface/revision level ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:241)).\
Counterexample: malformed append introduces a second `id="main"`; `replace("#main", ...)` may replace first, all, or whichever node the parser returns after normalization.\
Proposed fix: Use author-declared stable region IDs with uniqueness validation and require exactly-one-target semantics before mutation.

4. **MAJOR — `append` does not imply additive behavior without fragment validation.**\
Evidence: current publication hashes one complete opaque file read ([canvas.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:46)); hostile HTML containment is explicitly deferred ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:256)).\
Counterexample: append `</section><script>...</script><section id="x">`, duplicate IDs, or parser-reparenting table fragments; existing nodes may move or acquire changed interpretation despite an “append” label.\
Proposed fix: Parse fragments structurally, reject duplicate declared IDs and context-invalid fragments, then verify that every pre-operation region digest remains unchanged.

5. **MAJOR — Retry and interleaving semantics are absent.**\
Evidence: same-hash full publication is idempotent ([IMPLEMENTATION-PLAN.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:107)), but interactions are only at-least-once with event IDs ([IMPLEMENTATION-PLAN.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:80)); no operation key is specified.\
Counterexample: a timed-out `append` is retried and inserts the fragment twice; `refresh` interleaved between retries rebuilds against a different document.\
Proposed fix: Require a client-generated `operation_id`, persist its result, and return the original result for exact retries while rejecting payload reuse.

6. **MINOR — `navigate/redirect` is mixed into the mutation vocabulary without defined persistence.**\
Evidence: browser responsibility is display and forwarding, while the active session owns authorship and publication ([ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:164)); current revisions describe complete content, not navigation state ([ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:160)).\
Counterexample: redirect races with rebuild: one client observes a new URL while another sees a new revision on the old surface.\
Proposed fix: Separate ephemeral navigation commands from revision-producing builder operations and specify ordering between the two channels.

**Disagreement Questions**

- Formal attackers: Is “additive” byte preservation, DOM-node preservation, region-digest preservation, or preservation after HTML parser normalization?
- Formal attackers: Should `replace` require exactly one target, or is deterministic multi-target replacement intentional?
- Empirical attackers: Which parser/runtime is authoritative for malformed fragments: server DOM, browser DOM, or serialized source?
- Empirical attackers: Must legacy V0 publication remain concurrently writable, or may operation-enabled surfaces reject unconditioned V0 publishes?
- Both: Does `rebuild/refresh` mean recompute from authoritative source, replay operations, or replace the complete document? These produce materially different conflict laws.

## Turing, Alan - Final Robot-Talks Position

# FINAL POSITION

The operation API remains architecturally unsafe without a compatibility boundary. Peer review strengthens the concurrency and recovery objections; it does not overturn the additive-region attack.

## 1. Findings That Survive Unchanged

1. **CRITICAL — Mixed V0/new clients can erase additive region updates.**\
Evidence: V0 makes the workspace file canonical and republishes changed bytes as a new whole-document revision ([SPEC.md:250](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:250)); the server still accepts unrestricted whole-file publication ([server.mjs:568](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:568)).\
Counterexample: an operation client appends region content, then a stale V0 client validly republishes a complete file lacking it.\
**Fix:** Do not permit unconditional V0 publication after a surface enters operation-enabled mode.

2. **CRITICAL — Serialization does not prevent stale-base commits.**\
Evidence: bytes are read before the mutation queue ([server.mjs:580](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:580), [server.mjs:597](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:597)); revision identity is assigned afterward ([canvas.mjs:69](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:69)).\
Counterexample: A and B derive from revision R; A commits R1, then B commits an R-derived R2 that loses A.\
**Fix:** Require `expected_revision_id` and perform canonical reread, transform, validation, and commit within one serialized CAS boundary.

3. **MAJOR — `append` is not inherently additive.**\
Evidence: publication treats HTML as an opaque complete-file read ([canvas.mjs:46](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:46)); hostile HTML containment is deferred ([SPEC.md:256](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:256)).\
Counterexample: malformed table fragments, duplicate IDs, or closing tags can reparent or reinterpret existing DOM.\
**Fix:** Parse fragments structurally and prove that all pre-existing declared-region digests remain unchanged.

4. **MAJOR — Content-hash idempotency cannot protect operation retries.**\
Evidence: same-hash publication alone is idempotent ([IMPLEMENTATION-PLAN.md:107](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:107)); interaction delivery already assumes at-least-once behavior ([IMPLEMENTATION-PLAN.md:80](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:80)).\
Counterexample: retrying a successful append produces new bytes and appends twice.\
**Fix:** Persist one accepted/applied/rejected result per caller-stable `operation_id`.

## 2. Findings Revised Or Dropped

- **Selector ambiguity: revised and strengthened.** Duplicate-ID cardinality is only one failure. The deeper defect is the absence of stable region identity and stale-target detection. One path currently identifies an entire surface ([SPEC.md:250](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:250)); revisions describe complete-file reads ([SPEC.md:245](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:245)). Require author-declared unique region IDs plus a base revision and, preferably, a structural fingerprint.

- **Navigation/content mixing: revised from MINOR to MAJOR.** `refresh` already means display reload ([ARCHITECTURE.md:173](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:173)), while `navigate/redirect` has no content-revision semantics. Navigation must be a separate acknowledged command stream; `refresh` should not be overloaded as a builder operation.

- **Metadata idempotency: dropped from this decision.** Same-byte title/kind loss is real, but it does not decide whether operation-enabled regions are additive.

## 3. Disagreements With Peers

- I do **not** accept “server builder implies server filesystem mutation.” The authority/approval finding is CRITICAL only if builders write canonical files. A candidate-byte consolidator followed by an approved ordinary publication preserves current authorship boundaries. The API must decide this explicitly before implementation.

- I do **not** require replaying transformations from intent if immutable result bytes, base/result digests, and normalized operation input are durably recorded. Deterministic re-execution is stronger than necessary; deterministic recovery and audit are mandatory.

- Author-declared region IDs are necessary but insufficient. Duplicate rejection does not detect semantic reuse of the same ID after rebuild; stale operations also need `expected_revision_id`, with fingerprints as additional defense.

- Atomic rename addresses torn reads, but not stale-base ordering or crash recovery between canonical-file replacement and event publication. It is an input-admission requirement, not the transaction model.

## 4. Recommended Compatibility Boundary

Add an immutable per-surface mutation mode:

```text
mutation_mode = legacy_v0 | operations_v1
```

- `legacy_v0`: existing `/api/canvas/publish` behavior remains unchanged.
- Transition to `operations_v1`: explicit, revision-CAS guarded, and durably recorded.
- `operations_v1`: legacy `/publish` returns `409 operation_mode_required`.
- Every mutation uses `/operations` with `operation_id`, `expected_revision_id`, and `target`.
- `target` defaults to `whole_document`, preserving whole-document behavior.
- Region targeting is allowed only for unique author-declared region IDs.
- Whole-document replacement remains available as an operation, but never as an unconditional legacy publish.
- Returning to `legacy_v0` requires a separate explicit transition, not client negotiation per request.

This creates a hard epoch boundary: old clients remain valid on V0 surfaces, while they cannot silently erase operation-managed state.

## Rittel, Horst - Verification Return

**REQUIRED REVISIONS**

1. **Drop the proposed operations architecture.** `surface_mode`, CAS, operation IDs, region targets, `append|replace|rebuild`, immutable results, and navigation ordering are not requirements of the reviewed V0 contract. V0 explicitly publishes complete files ([SPEC.md:226](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:226), [IMPLEMENTATION-PLAN.md:5](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:5)). Historical snapshots and hostile-HTML containment are expressly deferred ([SPEC.md:256](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:256)). Drop A2, A3, S2, S3, V1, V2, V3, V4, K2, P2, the compatibility boundary, operation envelope, region scaffolding, rebuild objections, and navigation protocol.

2. **Replace A1/S1 with the actual authority contradiction.** The candidate wrongly centers hypothetical builder filesystem writes. The present route itself commits `canvas.surface_published` durable state without approval or receipt ([server.mjs:568](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:568), [server.mjs:606](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:606)), while the governing architecture says every effectful crossing carries approval and receipts ([ARCHITECTURE.md:14](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:14)) and the spec places actions beyond preview/read behind approval ([SPEC.md:24](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:24)). Required decision: either declare canvas publication a trusted-local exception or route the existing durable publication through approval/receipt. **MAJOR.**

3. **Retain K1/P1, narrowed to coherent admission.** `stat()` and a later unguarded `readFile()` are separate observations ([canvas.mjs:37](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:37), [canvas.mjs:46](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:46)); they do not sustain the plan’s unconditional claim that concurrent change yields “one complete read” ([IMPLEMENTATION-PLAN.md:109](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:109)). **MAJOR.**

4. **Retain K3.** Same-byte publication returns before applying requested `title` or `kind` ([canvas.mjs:62](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:62), [canvas.mjs:78](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:78)), although those fields are required and projected surface state ([SPEC.md:233](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:233), [SPEC.md:243](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:243)). **MINOR.**

**Missed material:** lexical containment does not prevent an in-workspace symlink from resolving outside `workspaceRoot`; `path.resolve()` is checked before `stat/readFile`, with no realpath containment verification ([canvas.mjs:31](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:31), [canvas.mjs:39](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/canvas.mjs:39)). That contradicts the plan’s “beneath configured workspaceRoot” boundary ([IMPLEMENTATION-PLAN.md:56](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md:56)). **MAJOR.**

## Schön, Donald - Verification Return

**REQUIRED REVISIONS**

The candidate substantially overstates a future operations architecture as defects in the declared V0 contract.

**Supported Objection**

1. **Canvas publication bypasses the stated approval boundary.**\
   `SPEC.md:24` requires approval for effects beyond preview/read; `SPEC.md:96-97` explicitly includes publication. `ARCHITECTURE.md:14-16` requires approval and receipts for effectful crossings. Yet `server.mjs:568-611` accepts an unapproved publish and durably commits `canvas.surface_published`.

   Concrete trace: any local client POSTs `{path,title,kind}` and advances durable canvas state without an approval or receipt. The candidate’s approval remedy blocks this only if it explicitly governs canvas publication itself. Builder filesystem behavior is irrelevant to this demonstrated crossing.

**Missed Material**

2. **Workspace containment is bypassable through symlinks.**\
   `IMPLEMENTATION-PLAN.md:55-58` requires resolution beneath `workspaceRoot`. `canvas.mjs:32-44` checks only the lexical path, then follows symlinks through `stat`; `canvas.mjs:46` follows the same link during `readFile`.

   Concrete trace:

   ```text
   workspace/external.html -> /tmp/external.html
   POST /api/canvas/publish {"path":"external.html",...}
   GET revision content
   ```

   The outside file is admitted and served. Require realpath containment or an equivalent descriptor-based no-follow policy.

3. **Replay validation does not validate the publication record.**\
   `server.mjs:163-169` reconstructs and validates only `{path,title,kind}`. It does not validate surface identity, revision binding, hash, byte length, or timestamps carried by the event.

   Concrete replay: an event with valid path/title/kind but malformed revision identifiers or digest passes this validation branch. The candidate incorrectly describes this as content recovery rather than event-integrity validation.

**Findings That Must Be Dropped**

- **A2, V3:** Immutable historical bodies are explicitly deferred by `SPEC.md:252-258`; mutable rereading is the stated V0 design. Also, `server.mjs:606-609` commits the surface and revision, so V3’s “reconstructs using path/title/kind only” characterization is false.
- **A3:** `refresh` is only a display command at `ARCHITECTURE.md:173-174`; no transformation algebra exists.
- **S2, S3:** No region targeting or `append` operation is specified. Hostile HTML containment is explicitly deferred at `SPEC.md:256-258`.
- **V1, V2, V4, K2, P2:** CAS, operation IDs, operation retries, and mixed operation/V0 clients are absent from the reviewed contract. Concurrent V0 publishes are complete-file publications; `409 revision_changed` is the specified stale-content outcome.
- **K1, P1:** `readFile` coherence hardening may be worthwhile, but the cited artifacts do not promise an atomic filesystem snapshot. The concrete containment defect is symlink traversal.
- **K3:** Same-hash publication is expressly idempotent at `SPEC.md:250-252`; metadata changes therefore do not establish a new publication under V0.

A static parser would also not block the candidate’s script counterexample: an admitted `<script>` can mutate supposedly unaffected regions at runtime. That concern belongs to the explicitly deferred hostile-HTML containment boundary, not an `append` contract that does not yet exist.

## Loregian, Fosco - Initial Audit

REJECT

Required revisions:

1. **Fix backward compatibility.** The proposed `surface_mode` promotion rejects legacy whole-file publication on an `operations_v1` surface. That does not preserve existing whole-file behavior while making named regions additive. Specify either:
   - legacy whole-file publication remains valid as whole-document replacement, with revision handling that preserves old clients; or
   - promotion creates a new surface identity while the original V0 surface remains fully compatible.

2. **Reclassify or substantiate V2.** No cited V0 contract requires replay validation of every persisted field. Add an exact architectural/specification invariant and demonstrated failure impact, or move V2 to evolution/hardening obligations and lower its severity.

3. **Reclassify or tighten K2/P2.** A single `readFile()` can reasonably satisfy “one complete read” without promising a coherent `stat`/content snapshot. Quote the exact surrounding language establishing snapshot consistency, demonstrate a resulting V0 correctness failure, or demote this to clarification/hardening rather than a MAJOR defect.

4. **Make receipt evidence exact.** A1/S1/V1 assert that no receipt is produced, but the route records `canvas.surface_published`. Establish from an exact cited definition why that event is not a receipt. Also separate the SPEC-supported approval contradiction from the ARCHITECTURE-supported receipt contradiction.

5. **State attack coverage explicitly.** All five targets receive findings, so there is no zero-findings red flag, but the final does not map the submitted attacker positions to examined/refuted/retained outcomes. Add a compact coverage matrix proving every registered attack was adjudicated.

The V0/evolution separation and dropped/refuted list are otherwise clear.

## Loregian, Fosco - Final Audit

ACCEPT

All five required revisions are satisfied: compatibility is preserved through separate surface identity; replay integrity was dropped; coherence findings were demoted; approval and receipt evidence were separated and tightened; and all five attack classes and review targets are explicitly covered.
