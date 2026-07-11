# Architecture Review Findings

Status: **ACCEPTED REVIEW RESULT**

Registered review: `2026-07-10-ide-extension-architecture-review`.

Final approval: **ACCEPT** by Loregian, Fosco. See [audit.md](audit.md).
This closes the review result, not the implementation work represented by the
`FIX` verdicts and promotion conditions below.

Verifier taxonomy: `VERIFIED` means the material finding survives verification; `RECLASSIFIED` means its evidence survives with corrected wording, severity, or layer. Artifact verdict is **FIX** iff at least one present CRITICAL or MAJOR finding survives for that artifact; otherwise **KEEP**. Promotion-only blockers and gates do not create a present-L0 FIX verdict.

Layer labels: `L0` implemented; `L0.5` proposed effectful MCP/chat/provider slice; `L0.6` proposed MV3 slice; `PROMOTION` a prerequisite before proposed capability becomes authoritative.

## `src/server.mjs`

**Artifact verdict: FIX.** AR-CAND-001, AR-CAND-002, AR-CAND-004, AR-CAND-005, AR-CAND-006, AR-CAND-007, and AR-CAND-008 include present CRITICAL or MAJOR defects in this artifact.

### AR-CAND-001 - Human approval attribution is not established

- **Status:** RECLASSIFIED
- **Severity:** MAJOR present L0; CRITICAL promotion blocker before effectful L0.5+
- **Layer:** L0 attribution; PROMOTION to effectful lanes
- **File:** `src/server.mjs`; `src/envelopes/dry-run-envelope.mjs`; `public/demo/l0.html`
- **Exact evidence:** `src/server.mjs:170-190` accepts `body.approved_by || 'human'`; `src/envelopes/dry-run-envelope.mjs:32-55` persists that unverified label; `public/demo/l0.html:366-371` submits approval through the same unauthenticated browser channel. Disposable verifier reproduction prepared and approved as `same-principal` and received `201`.
- **Consequence:** L0 state and receipts claim human approval without establishing that the label denotes a human. L0 is a loopback no-op witness, so present severity is MAJOR; the defect becomes CRITICAL before any effectful lane is admitted.
- **Proposed fix:** For L0, stop accepting or defaulting caller text as proved human attribution. Before effectful L0.5+, require kernel-attested principal/session separation and reject self-approval based on attested identity, not caller-selected string inequality.
- **Originating attackers:** Ashby; Hewitt; van Lamsweerde; Meadows
- **Verifier note:** Rittel retains a CRITICAL-present-L0 dissent because durable authority-shaped receipts can be minted by the proposing principal even in the no-op witness.

### AR-CAND-002 - Approval is reusable and not atomically consumed

- **Status:** VERIFIED
- **Severity:** CRITICAL present L0
- **Layer:** L0 receipt fidelity; also blocks L0.5
- **File:** `src/server.mjs`; `src/envelopes/dry-run-envelope.mjs`
- **Exact evidence:** `src/server.mjs:177-180` checks only current-envelope ID equality; `src/server.mjs:182-210` creates a fresh receipt on every accepted call; `approveDryRunEnvelope()` has no pending-state precondition. Disposable verifier reproduction observed sequential replay `201` and concurrent replay `[201, 201]` with distinct receipts.
- **Consequence:** One represented approval can mint multiple L0 receipts, independently of who may approve.
- **Proposed fix:** Minimum L0 repair is an atomic pending-to-consumed transition bound to approval/envelope/run, rejecting replay before writes. Expiry, actor/session, revision, normalized-grant, and invocation binding are L0.5 hardening.
- **Originating attackers:** Ashby; Hewitt; van Lamsweerde; Meadows

### AR-CAND-003 - Implemented L0 skips its named `running` state

- **Status:** RECLASSIFIED
- **Severity:** MINOR present L0; MAJOR promotion blocker for L0.5
- **Layer:** L0 typestate; PROMOTION to L0.5 invocation
- **File:** `src/server.mjs`; `src/envelopes/dry-run-envelope.mjs`; `SPEC.md`
- **Exact evidence:** `SPEC.md:114-120` draws `awaiting_approval -> running -> passed`, but `src/envelopes/dry-run-envelope.mjs:36-59` marks the envelope and receipt `passed` during approval and `src/server.mjs:157-167` performs no transition. However, `SPEC.md:149-157` explicitly says L0 approval records the no-op receipt.
- **Consequence:** Present L0 has a typestate/spec inconsistency, not a reproduced executed-effect claim. At L0.5 the distinction becomes MAJOR because `SPEC.md:159-167` requires one distinct post-approval invocation.
- **Proposed fix:** Reconcile L0 typestate prose with its acceptance sequence. Preserve a mandatory authorize -> invoke -> evidence -> receipt transition before L0.5 promotion.
- **Originating attackers:** Ashby; Hewitt; van Lamsweerde; Meadows
- **Verifier note:** Rittel retains a MAJOR-present-L0 dissent because the explicit typestate says the post-approval no-op enters `running`, and the current receipt cannot distinguish authorization from completion.

### AR-CAND-004 - Requested grants are not validated against the L0 grant contract

- **Status:** RECLASSIFIED
- **Severity:** MAJOR present L0 contract-validation defect
- **Layer:** L0 contract validation; PROMOTION blocker where grants control effects
- **File:** `src/envelopes/dry-run-envelope.mjs`; `src/kernel/grants.mjs`; `src/server.mjs`
- **Exact evidence:** `src/envelopes/dry-run-envelope.mjs:9-11` accepts any non-empty grant array; `src/server.mjs:127-145,186-210` persists and receipts those declarations; `src/kernel/grants.mjs:1-16` provides an effect classifier, not a closed authorization policy. Disposable verifier reproduction prepared and approved `requested_grants: ["root.anything"]` with `201`.
- **Consequence:** Unknown authority-shaped grant declarations enter durable L0 records without vocabulary validation or receipt-semantic binding. No requested capability or arbitrary effect is executed by L0, so no executed capability bypass is claimed.
- **Proposed fix:** For L0, enforce a closed versioned vocabulary, normalize grants before persistence, reject unknown declarations, and bind the normalized declaration to receipt semantics. Adapter/module allow, forbid, target scope, and execution policy are promotion requirements for effectful L0.5+.
- **Originating attackers:** Ashby; Hewitt; van Lamsweerde; Meadows

### AR-CAND-005 - Singleton envelope state orphans pending approvals

- **Status:** VERIFIED
- **Severity:** MAJOR present L0
- **Layer:** L0 concurrency and state model
- **File:** `src/server.mjs`
- **Exact evidence:** `src/server.mjs:140-144` replaces `current_envelope` while retaining pending queue entries; `src/server.mjs:174-180` resolves approval only against the singleton. Disposable verifier reproduction prepared envelope B and then received `404 approval_not_found` for still-visible pending approval A.
- **Consequence:** The API advertises pending work that its own approval route cannot resolve, even with sequential use by one local caller.
- **Proposed fix:** Resolve immutable envelope/run/approval records by ID and define the legal lifecycle for multiple prepared envelopes.
- **Originating attackers:** Ashby; Meadows

### AR-CAND-006 - Durable state and append log diverge under the reproduced race

- **Status:** VERIFIED
- **Severity:** MAJOR present L0
- **Layer:** L0 persistence consistency
- **File:** `src/server.mjs`; `src/kernel/audit.mjs`; `src/kernel/artifacts.mjs`
- **Exact evidence:** `src/server.mjs:174-209` independently performs mutable read/write state, artifact writes, workbench overwrite, and event append without serialization or recovery. The combined disposable verifier run ended with three read-model receipts and four `receipt.appended` events; both concurrent receipt artifacts existed.
- **Consequence:** Persisted read state and append history disagree after a concrete supported API race. This shares a trigger with AR-CAND-002 but requires an independent consistency remedy.
- **Proposed fix:** Serialize persistence, use exclusive artifact creation, define recoverable commit ordering or journaling, and reconcile state with events at startup.
- **Originating attackers:** Ashby; Hewitt; Meadows
- **Boundary correction:** L0 `append-only` does not imply hashes, signatures, cryptographic IDs, or generic tamper evidence; those remain optional hardening.

### AR-CAND-007 - Receipt evidence binding is incomplete and after-state evidence is not materialized

- **Status:** RECLASSIFIED
- **Severity:** MAJOR present L0
- **Layer:** L0 reference integrity; stronger binding is an L0.5 promotion requirement
- **File:** `src/envelopes/dry-run-envelope.mjs`; `src/server.mjs`; `schemas/receipt.schema.json`
- **Exact evidence:** The receipt is partially bound through `run_id`, `approval_id`, and a real before artifact. `src/server.mjs:182-190` does not materialize the symbolic `after_ref: state:${run_id}:passed`; `schemas/receipt.schema.json:34-55` accepts non-empty strings without resolution. Disposable verifier checks established that the default evidence file exists and the synthetic after reference does not resolve as a file.
- **Consequence:** L0 lacks a verifiable preserved before/after pair and validation of all receipt references. The default evidence path is real; whether it is relevant to a specific run is an inference, not a resolution failure. Binding is incomplete, not absent.
- **Proposed fix:** For L0, type and resolve references, persist actual before and after artifacts, and validate evidence references before append. Envelope, actor/session, adapter, context-packet, normalized-grant, and digest custody binding belong to L0.5 as those fields become authoritative.
- **Originating attackers:** Ashby; van Lamsweerde; Meadows

### AR-CAND-008 - Declared schemas are not enforced at runtime

- **Status:** VERIFIED
- **Severity:** MAJOR present L0
- **Layer:** L0 contract enforcement
- **File:** `scripts/validate-schemas.mjs`; `src/kernel/registry.mjs`; `src/server.mjs`; `schemas/agent-envelope.schema.json`; `schemas/receipt.schema.json`; `schemas/module-manifest.schema.json`
- **Exact evidence:** `scripts/validate-schemas.mjs:10-18` parses schema documents and delegates manifests to a handwritten checker; `src/kernel/registry.mjs:23-39` omits declared constraints; prepare and approve paths invoke no JSON Schema validator. Disposable verifier reproduction persisted schema-invalid `context_refs: "not-an-array"` after prepare returned `201`.
- **Consequence:** Runtime governance objects can violate declared closed contracts while validation reports success.
- **Proposed fix:** Apply one Draft 2020-12 validator before durable writes at manifest, request, envelope, and receipt boundaries; add valid and hostile invalid fixtures; label any retained parse-only command honestly.
- **Originating attackers:** Ashby; Hewitt; van Lamsweerde; Meadows

## `src/envelopes/dry-run-envelope.mjs`

**Artifact verdict: FIX.** AR-CAND-001, AR-CAND-002, AR-CAND-004, and AR-CAND-007 include present CRITICAL or MAJOR defects. AR-CAND-003 is MINOR at L0 but gates L0.5 promotion.

## `src/kernel/grants.mjs`

**Artifact verdict: FIX.** AR-CAND-004 is a MAJOR L0 contract-validation defect across grant construction and server admission. Existing `requiresApproval()` is only a classifier and is not sufficient repair.

## `src/kernel/audit.mjs` and `src/kernel/artifacts.mjs`

**Artifact verdict: FIX.** AR-CAND-006 is a MAJOR L0 cross-store consistency defect. Cryptographic chaining is not required by this verdict.

## Schemas, registry, and validation script

**Artifact verdict: FIX.** AR-CAND-007 and AR-CAND-008 are MAJOR L0 reference-integrity and runtime contract-enforcement defects.

## `public/demo/l0.html`

**Artifact verdict: FIX.** AR-CAND-001 is a MAJOR L0 human-attribution defect because the demo submits the unverified `human` label through the same unauthenticated channel.

## Module manifests and provenance

**Artifact verdict: KEEP at present L0; promotion gated.** AR-CAND-009 and AR-CAND-010 are promotion blockers only and do not establish present unauthorized execution or authority.

### AR-CAND-009 - Owner routes and `source_refs` are unresolved promotion inputs

- **Status:** VERIFIED
- **Severity:** PROMOTION BLOCKER only; not a present L0 defect
- **Layer:** PROMOTION to L0.5/L0.6 capability admission
- **File:** `schemas/module-manifest.schema.json`; `src/kernel/registry.mjs`; `src/modules/resonantos-browser-first.manifest.json`; `development/browser-first-extension-design/ARCHITECTURE-BUNDLE.md`
- **Exact evidence:** Owner/source references are strings; `src/kernel/registry.mjs:23-39` does not resolve them; the ResonantOS manifest cites mutable checkout roots while `ARCHITECTURE-BUNDLE.md:43-49` cites specific precedent files. `SPEC.md:98-99` says visibility does not confer authority.
- **Consequence:** Non-resolution is literal; illegitimate ownership is not established. Promotion is blocked only when these declarations would support capability admission or authority.
- **Proposed fix:** Before promotion, bind each capability claim to a canonical base, registered owner ID, exact file and revision/digest, and machine-readable verification status.
- **Originating attackers:** Ashby; Hewitt; van Lamsweerde; Meadows

### AR-CAND-010 - External MCP/chat provenance is mutable and not locally reproducible

- **Status:** VERIFIED
- **Severity:** PROMOTION BLOCKER only; not a present L0 defect
- **Layer:** PROMOTION to L0.5 and later precedent claims
- **File:** `development/mcp-chat-extension-integration-research/research.md`
- **Exact evidence:** Lines `129-149` derive local requirements from mutable GitHub file URLs without an inspected immutable revision, captured local extract, or claim-to-source map.
- **Consequence:** Repository-local reproduction of the historical basis is unavailable; upstream change or requirement invalidity remains future risk, not reproduced fact.
- **Proposed fix:** Before promotion, record URL, immutable revision, inspection date, bounded evidence, adopting owner, and adaptation decision in a local provenance ledger.
- **Originating attackers:** Hewitt; van Lamsweerde

## OpenRouter adapter

**Artifact verdict: KEEP at present L0; provider promotion gated.** No live provider call, secret path, or present custody defect exists.

### AR-CAND-011 - Secret custody is an unverified provider-promotion gate

- **Status:** VERIFIED
- **Severity:** PROMOTION GATE only; no present implementation defect
- **Layer:** PROMOTION to any live provider lane
- **File:** `src/adapters/openrouter.mjs`; `SPEC.md`; `CRAFT.md`
- **Exact evidence:** `src/adapters/openrouter.mjs:1-9` is descriptor-only and tests key presence; `CRAFT.md:44-45` records no live key handling or streaming proof; no reviewed target implements a provider call or browser secret path.
- **Consequence:** There is no present secret leak. A live provider cannot be admitted on descriptor claims alone.
- **Proposed fix:** Before provider promotion, prove relevant server/process custody, environment allowlisting, bounded HOME/CWD, redaction, and negative exfiltration checks. Require child-process controls only if the implementation spawns one.
- **Originating attackers:** Ashby; Hewitt; van Lamsweerde; Meadows

## Severity-Ordered Change Requests

1. **CRITICAL L0:** Make approval consumption atomic and exactly once; reject sequential and concurrent replay before any write (AR-CAND-002).
2. **MAJOR L0:** Stop asserting caller-provided/defaulted text as proved human approval; retain attested actor/session separation as a CRITICAL gate before effectful L0.5+ (AR-CAND-001).
3. **MAJOR L0:** Validate and normalize requested grant declarations without claiming L0 executed a capability; add effect-specific policy only before effectful promotion (AR-CAND-004).
4. **MAJOR L0:** Replace singleton envelope resolution with an ID-addressed lifecycle that does not advertise unreachable pending approvals (AR-CAND-005).
5. **MAJOR L0:** Serialize and reconcile state, artifact, and event persistence so the read model cannot diverge from receipt history (AR-CAND-006).
6. **MAJOR L0:** Materialize and validate the after artifact and all receipt references while preserving the existing run/approval/before partial binding (AR-CAND-007).
7. **MAJOR L0:** Enforce Draft 2020-12 schemas at admission and emission boundaries before persistence (AR-CAND-008).
8. **MINOR L0:** Reconcile the L0 `running` typestate with the acceptance sequence; require a distinct invocation before L0.5 promotion (AR-CAND-003).
9. **PROMOTION:** Resolve owner/source claims per capability and pin external research provenance before L0.5/L0.6 admission (AR-CAND-009, AR-CAND-010).
10. **PROMOTION:** Prove secret custody before any live provider lane (AR-CAND-011).

## Surviving Strengths

- The listener binds to `127.0.0.1`; no remote-host implementation claim survived.
- Pre-approval `/api/envelopes/run` rejects with `409 approval_required`.
- Implemented L0, proposed L0.5/L0.6, and deferred L1/L2 remain honestly separated.
- OpenRouter is descriptor-only; no browser key handling, live provider call, or browser mutation path exists.
- The default receipt evidence path exists; receipt binding already includes `run_id`, `approval_id`, and a real before artifact.
- The narrow cooperative prepare/block/approve/persist smoke path passes.
- The design rejects canvas visibility as authority and keeps remote precedent specimen-only.

## Verification Commands And Evidence

- Attackers ran `npm run validate:schemas && npm run smoke`: three schema documents and six manifests were reported validated; one L0 smoke test passed. AR-CAND-008 limits what the schema command proves.
- Hewitt used a disposable temporary-server harness to reproduce same-principal approval, concurrent replay, duplicate receipts/events, state/event divergence, arbitrary grant acceptance, and malformed `context_refs` acceptance.
- Rittel used `createServer()` with a fresh temporary state directory and real module/public directories. Observed: `self-approval: 201`; `sequential replay: 201`; `concurrent replay: [201, 201]`; `root.anything` prepare `201`; scalar `context_refs` prepare `201`; older approval after second prepare `404`; three final read-model receipts versus four receipt events; default evidence exists; synthetic after reference does not resolve as a file.
- All verifier runs were disposable local reproductions. Future effectful impact is classified as inference or promotion risk, not as executed L0 behavior.

## Unresolved Verifier Dissent

- **AR-CAND-001:** Final synthesis is MAJOR present L0 and CRITICAL before effectful L0.5+. Rittel dissents and rates present L0 CRITICAL because the same principal can mint durable authority-shaped receipts; Schon controls the conservative layer-specific classification because L0 is no-op and explicit actor/session separation belongs to L0.5.
- **AR-CAND-003:** Final synthesis is MINOR present L0 and MAJOR L0.5 promotion blocker. Rittel dissents and rates present L0 MAJOR because explicit typestate distinguishes `running`; Schon controls the conservative classification because `SPEC.md:149-157` says approval records the L0 no-op receipt.

## Final Counts

- **Present L0:** 1 CRITICAL, 6 MAJOR, 1 MINOR.
- **Promotion-only items:** 3 total: 2 PROMOTION BLOCKERs and 1 PROMOTION GATE.
- **Additional layered promotion dispositions:** AR-CAND-001 is CRITICAL before effectful L0.5+; AR-CAND-003 is MAJOR before L0.5; AR-CAND-004 blocks any lane where grants control effects.
