# Hewitt, Carl

## ORIGINAL ATTACK RETURN

# INITIAL POSITION

Scope reviewed without edits: the complete `projects/ide-extension` corpus, including contracts, research/design/refresh material, schemas, runtime, demo, manifests, scripts, and tests.

Level distinction: **implemented L0** is a loopback Node workbench with manifests, a pending envelope, a pre-approval block, and dry-run receipt persistence. **Proposed L0.5** is explicitly not implemented: MCP/chat descriptor, context packet, fake stdio witness, evidence binding, and hostile-path tests remain absent. **Proposed L0.6** MV3, **deferred L1** IDE wrapper, and **deferred L2** browser witnesses have no runtime claim here.

Safe checks run:

```bash
npm run validate:schemas && npm run smoke
```

Result: `validated 3 schemas and 6 module manifests`; one L0 smoke test passed.

## Findings

### CRITICAL - “Human approval” is client-supplied, so an agent can approve its own envelope

Evidence: [src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:127) accepts arbitrary `agent_ref` through `prepareDryRunEnvelope`; [src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:187) accepts `body.approved_by || 'human'`; [src/envelopes/dry-run-envelope.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/envelopes/dry-run-envelope.mjs:16) and [src/envelopes/dry-run-envelope.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/envelopes/dry-run-envelope.mjs:53) preserve both values without identity/session comparison. This contradicts SPEC’s literal requirement that “A proposal cannot approve itself” ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:122)) and the architecture’s required proposer/approver separation ([ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:113)).

Reproduced safe local check: a temporary loopback server accepted an envelope with `agent_ref: "same-principal"` and two approval requests with `approved_by: "same-principal"`; both returned `201`.

Proposed fix: bind approval to authenticated or locally attested actor/session identity and reject matching proposer/approver identities before receipt creation.

Level: breaks the authority interpretation of **implemented L0**; it is also a direct blocker for **proposed L0.5** self-approval rejection. It does not make L0.6/L1/L2 implemented.

### MAJOR - Approval is replayable and concurrent requests mint duplicate audit receipts

Evidence: [src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:177) only verifies that the approval ID matches; it never rejects an already-approved envelope. Both requests then create artifacts and append events at [src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:182) and [src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:202), with no transaction, lock, or state transition guard.

Reproduced safe local check:

```bash
node --input-type=module <temporary harness>
```

The harness prepared one envelope, concurrently POSTed twice to `/api/approvals/<id>/approve`, then inspected temp state. Output: approval statuses `[201, 201]`, two distinct receipt IDs, two `receipt.appended` events, and three artifact files. The workbench JSON retained only one receipt because concurrent read-modify-write lost an update. Thus the alleged durable state and append-only log disagree.

Proposed fix: make approval consumption atomic, transition only `awaiting_approval -> running`, and reject reused/expired approvals before any artifact or audit write.

Level: defects **implemented L0** receipt semantics and violates the exact, one-use approval requirement already specified for **proposed L0.5** ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:167)); L0.6/L1/L2 remain deferred.

### MAJOR - Schemas are parsed, not enforced; API and manifest contracts are advisory

Evidence: [scripts/validate-schemas.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/scripts/validate-schemas.mjs:14) does only `JSON.parse`; it never invokes a JSON Schema validator. Runtime input flows directly from `readBody` ([src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:45)) to envelope construction ([src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:127)). The registry’s handwritten validator does not enforce schema `minItems`/`uniqueItems` despite those requirements in [schemas/module-manifest.schema.json](/home/vrondelli/projects/domainspec-core/projects/ide-extension/schemas/module-manifest.schema.json:31).

Reproduced safe local check: `validateModuleManifest()` accepted a manifest with all schema-required arrays present but empty, although `source_refs` declares `"minItems": 1`. The same harness submitted `context_refs: "not-an-array"`; the server returned `201` and persisted that nonconforming value.

Proposed fix: use one Draft 2020-12 validator for every manifest, envelope, receipt, and request boundary, with invalid-fixture tests.

Level: **implemented L0** can display “validated” state without contract enforcement; this is fatal to **proposed L0.5** descriptor/context/evidence containment. No L0.6/L1/L2 enforcement exists yet.

### MAJOR - Requested grants are arbitrary labels, not capability authorization

Evidence: [src/envelopes/dry-run-envelope.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/envelopes/dry-run-envelope.mjs:9) accepts any nonempty caller list; [src/kernel/grants.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/grants.mjs:78) defines `requiresApproval`, but no runtime caller uses it. Approval then records the arbitrary grant request in state ([src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:131)) and issues a passed receipt.

Reproduced safe local check: POSTing `requested_grants: ["shell.exec"]` returned `201`; approving it returned `201` and a passed L0 dry-run receipt. No manifest capability, grant vocabulary, or effect-class check occurred.

Proposed fix: resolve grants against an allowlisted registry plus selected module/adapter capability, reject unknown or incompatible grants, and ensure receipt stage/status reflects the actual no-op effect.

Level: this is misleading in **implemented L0**, even though no shell executes; it would become an execution-boundary bypass in **proposed L0.5**. L0.6/L1/L2 are not implicated as implemented surfaces.

### MINOR - Declared typestate is not the executed API trace

Evidence: SPEC declares `draft -> prepared -> awaiting_approval -> running -> passed...` ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:114)). The approval endpoint writes `state: 'passed'` directly ([src/envelopes/dry-run-envelope.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/envelopes/dry-run-envelope.mjs:56)); `/api/envelopes/run` merely returns the existing state ([src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:166)). The smoke test never calls run after approval.

Proposed fix: either model an explicit no-op `running` transition and completion receipt, or narrow the L0 typestate contract to the implemented prepare/approve receipt flow.

Level: **implemented L0** has a documentation/runtime trace mismatch; **proposed L0.5** must not inherit it because it requires one post-approval invocation. Later layers are deferred.

## Attacks That Survived

- **Pre-approval invocation attack:** POST `/api/envelopes/run` before approval returned `409 approval_required`, as also covered by [tests/l0-smoke.test.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/tests/l0-smoke.test.mjs:57). This containment is implemented L0 evidence.
- **Non-loopback exposure attack:** the standalone listener binds `127.0.0.1` ([src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:224)); no remote-host claim was found.
- **Premature integration claim attack:** the refresh report explicitly says the L0.5 adapter descriptor, packet fixture, fake stdio witness, evidence writer, and negative tests “do not exist yet” ([development/mcp-chat-extension-integration-refresh/refresh-report.json](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/mcp-chat-extension-integration-refresh/refresh-report.json:71)). The corpus correctly keeps L0.5 proposed, L0.6 proposed, and L1/L2 deferred.

# FINAL POSITION

The corpus is candid about its roadmap, but the implemented L0 witness demonstrates a UI/API sequence, not yet a mechanically trustworthy governance boundary. Formal sufficiency is ahead of executable enforcement: schemas are not validators, grants are not authorization, and approval identity/one-use semantics are absent. Repair those L0 mechanics before treating the proposed L0.5 hostile-path contract as attainable evidence.

<oai-mem-citation>
<citation_entries>
MEMORY.md:3132-3156|note=[prior IDE extension routing context used to scope review]
</citation_entries>
<rollout_ids>
019ec468-8a46-7b30-920a-3a7a445ee986
</rollout_ids>
</oai-mem-citation>

## ROBOT-TALKS CONFRONTATION RETURN

## Confrontation

1. **Self-approval: HOLD CRITICAL.**  
This is a present **L0** violation, not merely a L0.5 blocker. The L0 definition binds “human approval gates” into the action boundary ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:14)); the server trusts `approved_by` from the request body ([src/server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:187)). A proposer can supply the same identity as approver. L0.5 makes the separation more explicit, but does not invent the underlying authority requirement.

2. **Secret custody: CONCEDE against calling it a present MAJOR.**  
The OpenRouter surface is descriptor-only: `describeOpenRouterAdapter()` reports readiness and `key_location: 'server-env-only'` ([src/adapters/openrouter.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/adapters/openrouter.mjs:1)); it does not call a provider or expose a key. CRAFT explicitly says “no live key handling or streaming proof yet” ([CRAFT.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/CRAFT.md:44)). This is a **promotion blocker for any live provider lane**, not an implemented-L0 secret leak.

3. **Schema enforcement: HOLD MAJOR.**  
The severity is not about invalid JSON aesthetics. `validate:schemas` only performs `JSON.parse` ([scripts/validate-schemas.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/scripts/validate-schemas.mjs:14)), while the API accepts malformed contract values into durable state. The reproduced `context_refs: "not-an-array"` case is a boundary failure, and the handwritten manifest validator accepts schema-invalid empty `source_refs`. Since the system’s authority claims depend on typed envelopes/manifests/receipts, formal sufficiency without enforcement is material. It becomes even more severe for L0.5, but is already MAJOR in L0.

4. **Typestate approval-to-passed: HOLD MINOR for L0; MAJOR if carried into L0.5.**  
I reject “receipt-semantic collapse” as a present L0 finding. The L0 acceptance contract expressly says “approve records a no-op receipt” ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:149)); direct completion is therefore a deliberately thin dry-run witness. It is nonetheless inconsistent with the declared `... -> running -> passed` trace. For L0.5, where one approved observe invocation must occur exactly once, the same shortcut would become MAJOR.

5. **Plain `appendFile` audit: REVISE.**  
“Append-only” in the current L0 contract means a local sequence log, not tamper-evident ledger semantics. There is no literal requirement for hashes, signatures, fsync durability, or crash recovery, and L0 excludes multi-user/remote guarantees ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:53)). I would not retain generic tamper risk as an independent MAJOR. The demonstrated race is MAJOR because it produces two receipt events but a divergent read model; that is an actual correctness failure, not a speculative integrity standard.

6. **External research provenance and unresolved `source_refs`: REVISE to MINOR L0, promotion blocker later.**  
SPEC requires source references ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:87)) but does not require the L0 registry to resolve or attest them. It also says visibility does not confer authority ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:98)). Thus unresolved research/module paths are documentation and admission-quality defects, not proof that current L0 executes unauthorized work. They become MAJOR for L0.5 adapter admission, where provenance feeds descriptor/custody/evidence binding.

7. **Duplicates versus independent findings.**  
- **Independent CRITICALs:** self-approval answers “who may approve?”; replay/race answers “how many times may one approval authorize?” One identity control cannot substitute for one-use atomic consumption.
- **Related but independent MAJORs:** schema non-enforcement permits malformed state; grant smuggling permits semantically unapproved authority labels. A real schema validator alone could validate `"shell.exec"` as a string, so it does not solve authorization.
- **Duplicate/merge:** generic append-only tamper concern merges into replay/race unless a concrete tampering or recovery failure is reproduced.
- **Deferred, not defects:** L0.5 context-as-authority, adapter evidence, MCP provenance, and provider custody are valuable gates but must not be reported as missing implemented L0 functionality when the corpus says they are proposed.

## Revised Final Position

The L0 workbench proves a narrow local sequence, but it does not yet enforce the authority boundary it represents: approval identity is caller-controlled, approvals are replayable under concurrency, schemas are decorative at runtime, and grants are not authorization. Those four findings should survive synthesis. The project is appropriately candid that L0.5, L0.6, L1, and L2 are unimplemented; their absence is not itself an L0 defect.

**Findings to survive synthesis**
- CRITICAL: self-approval through client-supplied approver identity.
- CRITICAL: replay/concurrent approval causes duplicate receipts/events and divergent state.
- MAJOR: schemas are parsed but not enforced at API or manifest boundaries.
- MAJOR: arbitrary requested grants are persisted and receipted without capability authorization.
- MINOR: declared typestate skips `running` for the intentionally no-op L0 path.
