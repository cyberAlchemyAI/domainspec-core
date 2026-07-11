# van Lamsweerde, Axel

## ORIGINAL ATTACK RETURN

# INITIAL POSITION

The corpus has a disciplined conceptual boundary but an unproven ownership boundary. My initial hypothesis was that historical precedents, module manifests, and deferred integrations were being treated as if references themselves conferred legitimate ownership. I attacked three tensions:

- internal coherence versus owner legitimacy;
- passing code versus unsupported contract;
- reference completeness versus operational safety.

Layer status used throughout:

- **Implemented L0:** local Node server, HTML workbench, manifest loading, dry-run envelope, approval endpoint, receipt append, persisted state, one smoke test.
- **Proposed L0.5:** offline MCP/chat admission harness and its stronger approval, custody, and evidence rules.
- **Proposed L0.6:** Chrome MV3 browser adapter.
- **Deferred L1/L2:** IDE wrapper and browser-validation witnesses.

# FINDINGS

## 1. MAJOR — “Schema validation” does not validate schemas or manifest conformance

**Evidence**

`projects/ide-extension/scripts/validate-schemas.mjs:14-18`:

> `JSON.parse(await readFile(path.join(schemaDir, file), 'utf8'));`  
> `const manifests = await loadModuleManifests(moduleDir);`

This proves only that schema files parse as JSON. The manifest loader uses a separate handwritten checker. At `projects/ide-extension/src/kernel/registry.mjs:23-39`, it checks required keys, selected arrays, and the `module_id` pattern, but does not enforce `additionalProperties: false`, `source_refs.minItems`, `uniqueItems`, or the complete JSON Schema contract declared in `projects/ide-extension/schemas/module-manifest.schema.json:6-78`.

Nevertheless, `projects/ide-extension/CRAFT.md:15` calls for “validate schemas,” and the command reports:

> `validated 3 schemas and 6 module manifests`

**Layer distinction**

This is an **implemented L0** defect. It does not attack proposed L0.5/L0.6 behavior.

**Proposed fix**

Use a Draft 2020-12 validator against representative valid and invalid instances, and rename any parse-only command so it cannot be mistaken for contract validation.

---

## 2. MAJOR — Module ownership is asserted but neither resolvable nor authenticated

**Evidence**

The module contract requires an “owner route” and “source refs” at `projects/ide-extension/SPEC.md:85-99`, but the schema defines both as unconstrained strings:

- `projects/ide-extension/schemas/module-manifest.schema.json:27-37`
- `projects/ide-extension/src/kernel/registry.mjs:23-39`

No code resolves a source reference, verifies that an owner route exists, or establishes which base directory relative paths use.

The ResonantOS manifest illustrates the problem at `projects/ide-extension/src/modules/resonantos-browser-first.manifest.json:4-9`:

> `"owner_route": "workspace-resonant-precedent"`  
> `"../workspace-resonant/2.0.0-alpha"`  
> `"../workspace-resonant/2.0.0-alpha-issue-98"`  
> `"../workspace-resonant/2.0.0-alpha-issue-125-module-ownership-map"`

The design artifacts cite exact precedent files instead, for example `projects/ide-extension/development/browser-first-extension-design/ARCHITECTURE-BUNDLE.md:43-49`. The machine manifest therefore points at whole mutable checkouts while claiming capabilities such as `"approval-policy-precedent"` at manifest lines 10-15. It does not bind those claims to the cited files or revisions.

**Layer distinction**

This weakens the **implemented L0** registry and the provenance basis of **proposed L0.6**. It does not prove that the ResonantOS adaptation is wrong; it proves the registry cannot establish its legitimacy.

**Proposed fix**

Define a canonical reference base and require each claimed capability to bind to an exact file plus revision or digest and a registered owner identifier.

---

## 3. MAJOR — Passing L0 code does not prove the documented approval contract

**Evidence**

The smoke test passes, but tests only one happy approval identity:

`projects/ide-extension/tests/l0-smoke.test.mjs:61-67`:

> `body: JSON.stringify({ approved_by: 'smoke-test' })`  
> `assert.equal(approved.body.receipt.status, 'passed');`

The server accepts any caller-provided identity and defaults an absent one to `"human"`:

`projects/ide-extension/src/server.mjs:170-190`:

> `approved_by: body.approved_by || 'human'`

There is no authenticated actor, session, approval expiry, replay check, or proposer/approver separation. Repeating the same approval endpoint can mint another receipt because lines 177-180 only compare the supplied ID to the current envelope.

That is narrower than the proposed L0.5 contract in `projects/ide-extension/SPEC.md:122-124` and acceptance rules at lines 167-171:

> “A proposal cannot approve itself.”  
> “forged, wrong, expired, and reused approvals reject”

**Layer distinction**

The **implemented L0** happy path passes and satisfies its narrow smoke assertions. The stronger protections are explicitly **proposed L0.5**, not implemented L0. The defect is any reading of the passing test as proof of a general approval boundary.

**Proposed fix**

Label current approval as an unauthenticated L0 simulation and make L0.5 introduce one-time, expiring approvals bound to actor, session, envelope, grants, and invocation.

---

## 4. MAJOR — Historical MCP/chat requirements are not locally reproducible

**Evidence**

The MCP/chat research derives concrete requirements from mutable external sources, including Yocoolab package behavior and tool implementation:

`projects/ide-extension/development/mcp-chat-extension-integration-research/research.md:129-149` cites GitHub URLs for `package.json`, `setup.ts`, `http-bridge.ts`, `types.ts`, hooks, mapper logic, and PR tooling.

Those observations are then transformed into locally named proposed contracts:

- `McpChatWitnessAdapter`
- `DesignFeedbackContextPacket`
- descriptor custody fields
- env/HOME/CWD containment
- rejection categories

The design correctly labels these terms “Candidate, not canonical” in `projects/ide-extension/development/browser-first-extension-design/GLOSSARY-CONSISTENCY.md:39-59`. However, the corpus contains no captured source snapshot, revision identifier, evidence extract, or claim-to-source table that would let a later reviewer reproduce which historical version justified each imported requirement without browsing.

**Layer distinction**

No **implemented L0** behavior depends on this material. This is a provenance defect in **proposed L0.5** and in the rationale for deferred external integrations. L0.6 and L1/L2 remain proposals/deferred lanes.

**Proposed fix**

Add a local provenance ledger binding each imported requirement to source URL, inspected revision/date, bounded evidence excerpt, adopting owner, and adaptation decision.

---

## 5. MINOR — The receipt model names references but does not define referential integrity

**Evidence**

`projects/ide-extension/schemas/receipt.schema.json:34-51` accepts `before_ref`, `after_ref`, and every `evidence_refs` item as any non-empty string.

The implemented receipt mixes reference kinds:

`projects/ide-extension/src/envelopes/dry-run-envelope.mjs:41-44`:

> `before_ref: ... 'state:workbench-before-approval'`  
> `after_ref: ... 'state:workbench-after-approval'`  
> `evidence_refs: ... ['projects/ide-extension/development/founding-research/findings.md']`

The server replaces only `before_ref` with an artifact path and leaves `after_ref` as an unverifiable symbolic string at `projects/ide-extension/src/server.mjs:182-190`. Thus “receipt” currently means a persisted assertion containing references, not proof that all references resolve to preserved before/after evidence.

**Layer distinction**

This is an **implemented L0** evidence-integrity limitation. Proposed L0.5 adds hashes and custody artifacts, while proposed L0.6 and deferred L2 require stronger runtime evidence.

**Proposed fix**

Type each reference, require resolvable artifact IDs or content digests, and validate referenced artifacts before appending the receipt.

# SURVIVING ATTACKS

- **Layer honesty survived.** I attacked the corpus for silently presenting MCP/chat, MV3, IDE, or Playwright behavior as implemented. `ARCHITECTURE.md:134-142`, `README.md:24-35`, and `IMPLEMENTATION-LAYERING-SEED.md:17-23` consistently separate implemented L0, proposed L0.5/L0.6, and deferred L1/L2.
- **Canvas authority survived.** I looked for UI state promoted over source evidence. `ARCHITECTURE.md:117-132` explicitly rejects canvas authority and treats source candidates as hypotheses.
- **Remote precedent capture survived operationally.** I attacked Kernel Cloud, Yocoolab, DevTools, and provider findings for immediate adoption. The corpus repeatedly keeps them deferred or specimen-only and denies them receipt authority.
- **The narrow L0 smoke survived.** `npm run validate:schemas` and `npm run smoke` both completed successfully; the latter passed its single prepare/block/approve/persist scenario. The attack is against the breadth of the inferred contract, not that narrow execution result.

# FINAL POSITION

The corpus is internally coherent and unusually honest about layer status. Its weakest point is not architectural confusion but ownership machinery: references are strings, owners are labels, historical sources are not frozen, and passing tests prove less than the surrounding governance vocabulary can suggest.

I therefore accept **implemented L0 as a functioning local demonstration**, not yet as a reference-integrity-enforced governance kernel. I accept **L0.5 and L0.6 as bounded proposals**, with L0.5 correctly preceding browser action. I accept **L1/L2 as deferred**. Promotion should be blocked until machine validation covers reference resolution, ownership binding, one-time approval semantics, and evidence-artifact integrity.

## ROBOT-TALKS CONFRONTATION RETURN

# CONFRONTATION

## 1. Self-approval and replay

**REVISE**

I previously treated self-approval mainly as an overreading of the L0 smoke test. The literal L0 contract is stronger than that reading.

`SPEC.md:24` places an “Approval queue for any action with effects beyond preview/read” inside L0, while `README.md:5-6` says every handoff is “approval-gated.” Yet `server.mjs:170-190` accepts an unauthenticated `approved_by`, defaults it to `"human"`, and immediately mints the receipt. `server.mjs:177-180` checks only whether the approval ID matches the current envelope. It does not reject an already used approval.

The proposed actor/session separation and explicit replay tests remain **L0.5** requirements at `SPEC.md:122-124,159-171`. Their absence alone would not violate L0. But accepting the same approval twice violates the present meaning of an L0 gate: no authorization state transition is consumed.

I accept **CRITICAL** for replay and self-approval together because the approval boundary can be bypassed by assertion and reused to mint authoritative receipts.

## 2. Secret custody

**HOLD**

Secret custody is not a present MAJOR implementation defect. `openrouter.mjs:1-9` is descriptor-only; it reads only whether `OPENROUTER_API_KEY` exists and returns `"key_location": "server-env-only"`. `CRAFT.md:42-45` explicitly says live key handling and streaming proof are absent.

A future adapter could mishandle inherited environment state, but that belongs to **proposed L0.5 provider/process custody** or later integration. Without a live provider call or secret transmission path, Meadows’s MAJOR severity exceeds implemented L0 evidence.

## 3. Schema enforcement

**HOLD**

I retain **MAJOR**, but narrowly. `validate-schemas.mjs:14-18` parses schema JSON and then invokes a handwritten manifest checker. It does not validate instances against the schemas. `registry.mjs:23-39` omits declared constraints such as `additionalProperties: false`, `source_refs.minItems`, and `uniqueItems`.

This would be MINOR if the command were named “parse schemas.” It is MAJOR because L0 acceptance requires manifest loading, the module registry is part of the authority boundary, and the command reports “validated … schemas and … manifests.” Passing code is being used as unsupported contract evidence.

## 4. Approval directly becomes `passed`

**REVISE**

This is independent of replay and is **MAJOR**, not merely a typestate wording mismatch.

`SPEC.md:116-120` declares:

> `draft -> prepared -> awaiting_approval -> running -> passed...`

and says `running` is a no-op dry run only after approval. But `approveDryRunEnvelope()` sets `state: 'passed'` and creates the receipt at `dry-run-envelope.mjs:36-59`. `/api/envelopes/run` at `server.mjs:157-167` performs no run transition after approval.

Therefore approval is execution, and the receipt attests to a stage that never ran. This collapses authorization evidence and execution evidence inside **implemented L0**.

## 5. `appendFile` and “append-only”

**CONCEDE**

Plain `appendFile` is not, by itself, a CRITICAL or MAJOR L0 violation. `audit.mjs:4-7` accurately implements append-only application behavior. L0 does not literally promise cryptographic tamper evidence, crash recovery, locking, or atomic multi-file transactions.

However, concurrent replay exposing divergence between `events.jsonl` and `workbench.json` is independently significant. The appropriate finding is **MAJOR consistency/atomicity risk**, not “append-only falsely implies tamper evidence.” Tamper evidence belongs to later hardening unless explicitly promoted into the contract.

## 6. Research provenance and module references

**HOLD**

These are promotion blockers, not cosmetic documentation work.

`module-manifest.schema.json:27-37` accepts arbitrary owner and source strings; `registry.mjs:23-39` never resolves them. The ResonantOS manifest cites mutable checkout roots at `resonantos-browser-first.manifest.json:4-15`, while the design’s actual claims rely on specific files in `ARCHITECTURE-BUNDLE.md:43-49`.

Likewise, MCP/chat requirements are derived from mutable external URLs in `mcp-chat-extension-integration-research/research.md:129-149` without captured revision or local evidence. This does not break current L0 execution, but it blocks legitimate promotion of **L0.5/L0.6** requirements and precedent claims.

## 7. Duplicate versus independent findings

**CONCEDE**

Self-approval, unauthenticated `approved_by`, and replay are one authorization-consumption finding. Concurrent duplicate receipts are its strongest reproduced consequence, not a separate root cause.

Grant smuggling and unused grant policy are one independent finding: arbitrary `requested_grants` enter at `dry-run-envelope.mjs:9-11`, while approval does not evaluate them.

Approval-to-`passed` is independent because it corrupts typestate and receipt meaning even with perfect identity checks.

Decorative evidence and untyped receipt refs overlap. Context-as-authority is separate only where unverified caller context influences an authorization or execution decision.

# REVISED FINAL POSITION

Implemented L0 is a functioning demonstration, but not yet a defensible governed boundary. Its central failure is now CRITICAL: approval is unauthenticated, reusable, and receipt-minting. Separately, approval collapses directly into successful execution, arbitrary grants are admitted without policy enforcement, and schema validation overstates its proof.

L0.5/L0.6 remain honestly proposed, but their promotion must be blocked until historical requirements and module ownership references become reproducible and resolvable.

**Findings that should survive synthesis**

- **CRITICAL:** unauthenticated self-approval plus reusable/concurrent approval replay.
- **MAJOR:** approval equals execution; no real `running` transition.
- **MAJOR:** arbitrary grants accepted without authorization policy.
- **MAJOR:** schema command does not enforce declared schemas.
- **MAJOR:** state/event consistency lacks atomic replay protection.
- **MAJOR promotion blocker:** unresolved module ownership and mutable research provenance.
- **MINOR:** receipt references lack typed resolution semantics.
