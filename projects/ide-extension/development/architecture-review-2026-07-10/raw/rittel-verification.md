# Rittel, Horst - Skeptic/Verifier Return

Registered review: `2026-07-10-ide-extension-architecture-review`  
Attack vector: counter-example

## Method And Evidence Standard

I inspected `findings.md`, `attacks.md`, all four attacker returns in `raw/`, and every literal target cited by AR-CAND-001 through AR-CAND-011. I made no changes to reviewed architecture or source files. Safe API checks used `createServer()` with a fresh temporary state directory and the repository's real modules/public directories.

I distinguish:

- **Reproduced fact:** observed from the real server or filesystem in a disposable local run.
- **Literal fact:** directly established by the cited source or contract text.
- **Inference:** a consequence or future risk that is not itself executed by L0.

The combined disposable run observed:

```text
self-approval: 201
sequential replay: 201
concurrent replay: [201, 201]
arbitrary grant root.anything: prepare 201
schema-invalid context_refs string: prepare 201
old approval after second prepare: 404 approval_not_found
final read-model receipts: 3
receipt.appended events: 4
default evidence ref exists: true
synthetic after_ref resolves as a file: false
```

The final receipt/event counts include the sequential and concurrent checks in one run. They demonstrate divergence, not a claim that every race must lose exactly one update.

## AR-CAND-001 - VERIFIED

**Literal evidence.** `src/server.mjs:170-190` accepts an unauthenticated request body and passes `body.approved_by || 'human'`; `src/envelopes/dry-run-envelope.mjs:32-55` stores the string without establishing an actor or comparing it to `agent_ref`; `public/demo/l0.html:366-371` supplies the browser-authored label `human`. `SPEC.md:122-124` requires proposer and approver/session separability for L0.5.

**Reproduced fact.** Preparing with `agent_ref: "same-principal"` and approving with `approved_by: "same-principal"` returned `201` and minted a passed receipt.

**Severity.** CRITICAL fits the authority-bearing vocabulary and durable receipt behavior. Loopback binding limits network exposure but does not establish human identity or prevent the proposing process from calling the endpoint.

**Fix fit.** The proposed kernel-owned identity/capability direction fits. Rejection should be based on attested principal/session identity, not string inequality alone; two caller-selected unequal strings would not repair the defect.

## AR-CAND-002 - VERIFIED

**Literal evidence.** `src/server.mjs:177-180` checks only current-envelope ID equality. `src/server.mjs:182-210` performs receipt creation and persistence on every accepted call. `approveDryRunEnvelope()` has no source-state precondition and accepts an envelope already in `passed`.

**Reproduced fact.** A second sequential approval for the same ID returned `201` with a distinct receipt ID. Two concurrent approvals for another single ID both returned `201` with distinct receipt IDs.

**Severity.** CRITICAL fits: one nominal authorization can mint unbounded success receipts. This is independent of AR-CAND-001 because replay survives even with a valid approver.

**Fix fit.** Atomic pending-to-consumed transition and rejection before any artifact/audit write fit. Revision, grant digest, actor/session, and expiry binding are appropriate hardening for L0.5, but the minimum present-L0 repair is atomic one-use consumption bound to the approval/envelope/run.

## AR-CAND-003 - VERIFIED

**Literal evidence.** `SPEC.md:114-120` declares `awaiting_approval -> running -> terminal` and says `running` is the post-approval no-op dry run. `approveDryRunEnvelope()` instead sets `passed` and creates the passed receipt. `/api/envelopes/run` only reports the current state and causes no transition or receipt.

**Reproduced fact.** Approval returned a `passed` receipt without any call to `/api/envelopes/run`.

**Severity.** MAJOR fits implemented L0. `SPEC.md:149` says approval records a no-op receipt, but that acceptance shorthand does not erase the explicit typestate and post-approval `running` statement. The receipt cannot distinguish authorization from completion.

**Fix fit.** A separate kernel-observed no-op transition is the direct fit. Narrowing the contract is possible only if the receipt/status vocabulary is also changed so approval is not represented as completed execution; merely editing typestate prose would not fit the evidence claim.

## AR-CAND-004 - RECLASSIFY

**Surviving defect.** `prepareDryRunEnvelope()` accepts any non-empty grant array; `src/kernel/grants.mjs:1-16` contains an effectful set and `requiresApproval()`, but the server imports only `blockedBeforeApproval`; receipt creation does not authorize or normalize requested grants.

**Reproduced fact.** `requested_grants: ["root.anything"]` prepared with `201` and was then approvable. The earlier `shell.exec` reproduction is also consistent with the literal code.

**Counter-example to candidate wording.** `requiresApproval()` is not a closed vocabulary or allow/forbid policy: known effectful grants and suffix grants return a boolean, while unknown grants are not rejected. Therefore the code does not contain the full “grant policy” that the candidate says is bypassed. L0 also executes no shell or arbitrary grant effect.

**Reclassified finding.** **MAJOR - requested grant declarations are unvalidated and unbound to receipt semantics.** Unknown authority labels can enter durable governance-shaped records; arbitrary capability execution is an inference, not reproduced L0 behavior.

**Fix fit.** A closed versioned vocabulary and normalization before preparation fit. Module/adapter target-scope policy is a promotion requirement unless L0 begins authorizing module effects. The synthesis must not imply that invoking existing `requiresApproval()` alone fixes this.

## AR-CAND-005 - VERIFIED

**Literal evidence.** Preparation replaces `current_envelope` while retaining all pending queue entries. Approval resolves only against `current_envelope.approval.approval_id`.

**Reproduced fact.** After preparing envelope B, approving still-visible pending approval A returned `404 approval_not_found`.

**Severity.** MAJOR fits because the durable queue advertises pending work that the API can no longer resolve. “Mixes concurrent actor/tab contexts” is an architectural inference, supported by the singleton shape but not needed for the finding.

**Fix fit.** Immutable lookup by approval/envelope/run ID fits. The implementation must also define whether multiple current/runnable envelopes are legal; a map alone does not settle lifecycle policy.

## AR-CAND-006 - VERIFIED

**Literal evidence.** `src/server.mjs:174-209` performs independent read-modify-write state, overwrite-capable artifact writes, workbench rewrite, and event append without serialization. `audit.mjs` does append JSONL; the candidate correctly avoids treating append-only as a cryptographic claim.

**Reproduced fact.** Two concurrent approvals both returned `201` and appended distinct receipt events. In the combined run, the final read model contained three receipts while the event log contained four `receipt.appended` events. Both receipt artifact files from the concurrent calls existed.

**Severity.** MAJOR fits cross-store authoritative inconsistency. This is a consequence enabled by AR-CAND-002 but needs its own consistency remedy.

**Fix fit.** Serialization, recoverable ordering/journaling, exclusive artifact creation, and startup reconciliation fit. Atomic approval consumption is necessary but belongs primarily to AR-CAND-002; synthesis should avoid presenting cryptographic chaining as required evidence.

## AR-CAND-007 - RECLASSIFY

**Literal evidence.** Receipt references are unconstrained non-empty strings in `schemas/receipt.schema.json:34-55`. The server writes a real before artifact but supplies `after_ref: state:<run_id>:passed` without writing a corresponding after artifact. The receipt has `run_id` and `approval_id`, but no `envelope_id`, actor/session identity, grant set, or content digest.

**Reproduced fact.** The default evidence path resolved to an existing repository file. The synthetic `after_ref` did not resolve as a filesystem artifact.

**Counter-example to candidate breadth.** It is false to imply that the default evidence reference is nonexistent: it exists. Whether founding research is “unrelated” is an inference about evidentiary relevance, not a failed resolution check. The receipt is partially bound through `run_id`, `approval_id`, and the before artifact, so “not bound to the approved run” is too absolute.

**Reclassified finding.** **MAJOR - receipt evidence binding is incomplete and the after reference is not materialized or validated.** The receipt does not establish a verifiable before/after pair or bind all authority-relevant inputs.

**Fix fit.** Typed resolvable references, immutable before/after artifacts, relevant digests, and pre-append validation fit. Actor/session and normalized grants should be added only as those concepts become authoritative fields; they cannot be retrofitted by reference typing alone.

## AR-CAND-008 - VERIFIED

**Literal evidence.** `scripts/validate-schemas.mjs:10-18` parses schema documents and delegates manifests to `loadModuleManifests()`. `registry.mjs:23-39` is handwritten and omits schema constraints including `additionalProperties: false`, `source_refs.minItems`, and uniqueness. Prepare/approve boundaries invoke no schema validator.

**Reproduced fact.** A prepare request with schema-invalid `context_refs: "not-an-array"` returned `201` and persisted the scalar value. The same request accepted the unknown grant value. This directly contradicts the declared envelope schema.

**Severity.** MAJOR fits because runtime governance objects can violate their declared closed contract. The command's “validated” wording is secondary.

**Fix fit.** One Draft 2020-12 validator at admission/emission boundaries plus hostile fixtures fits. Validation must occur before durable writes. Merely renaming the parse command would not repair runtime divergence.

## AR-CAND-009 - VERIFIED

**Literal evidence.** The manifest schema models owner/source references as strings. The registry checks shape but does not resolve owner routes, paths, revisions, or claim-to-source relationships. The ResonantOS manifest cites mutable checkout roots, while `ARCHITECTURE-BUNDLE.md:43-49` lists specific precedent files. `SPEC.md:98-99` explicitly says registry visibility does not confer authority.

**Fact versus inference.** Non-resolution is a literal fact. Illegitimate ownership is not established. The promotion risk arises only if these declarations are used for capability admission or authority.

**Severity.** PROMOTION BLOCKER fits; it is not a present L0 defect under the current descriptive-only contract. Do not relabel it MAJOR without evidence that current authority depends on these declarations.

**Fix fit.** Canonical base, registered owner ID, exact file plus revision/digest, and machine-readable verification status fit promotion. Exact file binding should be per claim where one manifest lists multiple capabilities.

## AR-CAND-010 - VERIFIED

**Literal evidence.** `development/mcp-chat-extension-integration-research/research.md:129-149` cites mutable GitHub `main` URLs and derives local requirements. The reviewed material provides no pinned commit, captured local extract, or claim-to-source mapping for those observations.

**Fact versus inference.** Present non-reproducibility from repository-local evidence is literal. A source changing or a derived requirement becoming wrong is a future risk, not reproduced fact.

**Severity.** PROMOTION BLOCKER fits and must remain explicitly outside present L0 defects.

**Fix fit.** A provenance ledger with URL, inspected revision/date, bounded evidence, adopting owner, and adaptation decision fits. A date without immutable revision is insufficient where the upstream is versioned.

## AR-CAND-011 - VERIFIED

**Literal evidence.** `src/adapters/openrouter.mjs:1-9` returns a descriptor and only tests key presence. `CRAFT.md:44-45` explicitly records absent live key handling and streaming proof. No reviewed target implements a provider call or browser secret path.

**Counter-example result.** There is no present secret-custody implementation to attack and no present leak established. This verifies the candidate precisely because it is framed as a future promotion gate, not a defect.

**Severity.** PROMOTION GATE fits. Calling it CRITICAL or MAJOR in current L0 would inflate beyond evidence.

**Fix fit.** Server/process custody, allowlisted env, bounded HOME/CWD, redaction, and negative exfiltration checks fit before a live provider lane. Child-process checks apply only if the provider implementation spawns one; do not require irrelevant machinery from a direct in-process transport.

## Exact Disposition Table

| Item | Disposition | Final severity/class | Reproduced material fact |
| --- | --- | --- | --- |
| AR-CAND-001 | VERIFIED | CRITICAL present L0 authority defect | Same principal proposed and approved; `201` |
| AR-CAND-002 | VERIFIED | CRITICAL present L0 one-use defect | Sequential replay `201`; concurrent `[201, 201]` |
| AR-CAND-003 | VERIFIED | MAJOR present L0 receipt-semantic defect | Approval minted `passed` without run call |
| AR-CAND-004 | RECLASSIFY | MAJOR unvalidated/unbound grant declarations | Unknown `root.anything` prepared and approved |
| AR-CAND-005 | VERIFIED | MAJOR present L0 singleton/orphan defect | Older visible pending approval became `404` |
| AR-CAND-006 | VERIFIED | MAJOR present L0 persistence-consistency defect | 3 read-model receipts versus 4 receipt events |
| AR-CAND-007 | RECLASSIFY | MAJOR incomplete evidence binding | Evidence path exists; synthetic after ref does not resolve |
| AR-CAND-008 | VERIFIED | MAJOR present L0 contract-enforcement defect | Scalar `context_refs` accepted with `201` |
| AR-CAND-009 | VERIFIED | PROMOTION BLOCKER, not present L0 defect | Not separately executed; non-resolution is literal code fact |
| AR-CAND-010 | VERIFIED | PROMOTION BLOCKER, not present L0 defect | Not executed; mutable unpinned citations are literal text fact |
| AR-CAND-011 | VERIFIED | PROMOTION GATE, not present implementation defect | No live provider/secret path exists in reviewed targets |

No item is REFUTED or MERGED. AR-CAND-002 and AR-CAND-006 share a trigger but have independent violated invariants and remedies. AR-CAND-004 and AR-CAND-008 overlap at malformed input admission but separate semantic authorization from structural conformance. AR-CAND-007 is narrowed rather than softened: the absolute/unresolved-evidence wording is dropped, while the reproduced missing after artifact and incomplete binding remain.

## Required Synthesis Edits

1. **AR-CAND-004:** replace “Requested grants bypass capability policy” with “Requested grant declarations are unvalidated and unbound to receipt semantics.” State that existing `requiresApproval()` is a classifier, not a closed authorization policy, and that no arbitrary effect execution was reproduced. Keep MAJOR.
2. **AR-CAND-004 fix:** separate minimum L0 repair (closed vocabulary, normalization, rejection before persistence, receipt binding) from module/adapter target-scope policy required for promotion.
3. **AR-CAND-007:** replace the absolute title with “Receipt evidence binding is incomplete and after-state evidence is not materialized.” Record that the default evidence file exists; drop any implication that it is non-resolving. Label relevance/unrelatedness as inference.
4. **AR-CAND-007 evidence:** acknowledge existing partial binding through `run_id`, `approval_id`, and the before artifact, then identify the absent `envelope_id`, identity, normalized grants, digests, validated after artifact, and relevance contract.
5. **AR-CAND-001 fix:** say attested principal/session separation; do not imply caller-provided string inequality is sufficient.
6. **AR-CAND-002 fix:** distinguish minimum atomic one-use consumption at L0 from expiry and richer revision/session binding for L0.5.
7. **AR-CAND-003:** resolve the recorded dissent in favor of MAJOR and cite both the explicit typestate and the acceptance shorthand; explain why the former controls receipt semantics.
8. **AR-CAND-006:** preserve the explicit boundary correction that append-only does not imply hashes/signatures. Keep cross-store divergence independent from replay consumption.
9. **AR-CAND-009 through 011:** preserve their non-present classifications exactly. Do not include them in a count of implemented L0 defects.
10. **Reproduction language:** label the observed outputs as disposable local reproductions and keep future impact claims visibly separate as inference.
