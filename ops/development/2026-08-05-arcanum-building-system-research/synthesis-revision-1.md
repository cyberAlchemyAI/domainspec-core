# Arcanum Building System — Evidence-Bound Synthesis, Revision 1

Dispatch: `2026-08-05-arcanum-building-system-research-route`  
Run: `arcanum-building-system-research-run-01`  
Revision action: `synthesis-zig-zag-01`

Parent commit: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`  
Arcanum commit: `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`

`OBSERVED` means source or persisted evidence was inspected. `EXECUTED` means a named bounded test was run and reported by an explorer or reviewer. `UNVERIFIED` means the contract or fixture exists without the corresponding end-to-end operation.

The Arcanum commit does not identify live-uncommitted bytes. For the current snapshot, representative content digests include:

- Invoke README `56a254cf…`, Plan `daedf27d…`
- WPRA README `79257f4e…`
- Implementation Readiness README `e53479e5…`
- Task Session Until Blocker README `eb9e2eec…`
- Task Session SKILL `bd7c4367…`
- Continuation Router SKILL `d7f1c5a1…`
- admission compatibility test `206077ab…`

These hashes identify only the inspected working-tree snapshot. They are not committed source identities, patch manifests, generated-parity receipts, or promotion evidence.

## 1. State and evidence vocabulary

| State family | Owner | Artifact/state | Evidence ceiling |
|---|---|---|---|
| Invoke mode run | Current Invoke mode | Mode report with `phase_status=pass|flag|block|no-op` | Completion status of that mode run only |
| Authored capability axis | Invoke capability resolver using artifact receipt | `artifact_authored.status=pass|flag|block|unsupported` | Whether the mode artifact is authored under its contract |
| Registry-release axis | Registry owner, currently not exactly bound by this dispatch | Registry-owner receipt bound to capability-table digest | Registry release only |
| Mutation-runtime axis | Capability resolver consuming material and runtime receipts | `mutation_runtime_ready.status=true|false` | Whether the exact runtime gates represented by those receipts pass |
| Design evidence | Design author, independent extractor, selection validator | `DesignScopeManifest`, `DesignDenominatorReceipt`, `DesignSelectionResult` | `authored-complete` or `design-validator-pass`; never Plan evidence |
| Plan artifact status | Invoke Plan | Layering, Work Pack, SWUs, validation and closeout contracts, Plan result | Plan artifact/handoff status only; never mutation readiness |
| Frozen Work-Pack audit | WPRA | Readiness report and Plan Semantic Manifest | Frozen contractual and semantic audit only |
| Selected-unit verification | WPRA selection verifier | Non-authoritative selected-unit receipt | Current semantic unit identity; `authority_effect:none` |
| Consumer entry | Task Session fast-entry guard | Fast-entry receipt | Current selected-unit/binding/entry eligibility |
| Material-package validation | Exact producer owner remains deferred | Material package, producer receipt, producer schema | Package integrity only |
| Mutation admission | Task Session | Admission request/receipt and single-use token | Consumer authorization for this exact attempt; not mutation success or lifecycle authority |
| Execution terminal | Task Session | Execution ticket and execution-terminal receipt | One admitted SWU’s execution and critical validation |
| Synchronized completion | Task Session derives overall state; Refresh owns closeout mutation; Router owns hop/join | `CloseoutSync`, separate owner receipt, continuity cursor | Completion only after required closeout passes or a validated no-op applies |
| Lifecycle decision | Sigil Development or Spellcraft | Lifecycle-owner decision supported by experiments/signals/reflection | Candidate maintenance or promotion judgment, not registry release |
| Registry release | Separately bound registry owner | Registry-owner receipt | Registry state only; owner remains unbound here |
| Inventory-native proof | Inventory | Cards, index, lookup projection, lint/conformance result | Its own provenance and exact index/projection conformance |
| Craft ledger state | Craft | `.craft/ledger.yml`; derived `CRAFT.md` and index | Local recursive-state truth only |

Direct evidence: definitional review “Definition, owner, state, artifact, and evidence-ceiling matrix”; `arcanum/spells/invoke/README.md:46-70`; explorer-contract §§2-3; `arcanum/arcana/task-session/SKILL.md:260-420`; `arcanum/arcana/inventory/SKILL.md:247-285,335-339`; `arcanum/arcana/craft/SKILL.md:56-72,277-317`. Current source is mixed clean/live-uncommitted; `OBSERVED`.

## 2. Plain-language model

- `SYS-001` — Invoke authors the agreement. Define fixes intent; Design establishes independently validated Design evidence; Plan authors implementation layering, Work Pack, SWUs, validation, execution, and closeout contracts. A mode’s `phase_status` is separate from `artifact_authored`, `registry_released`, and `mutation_runtime_ready`; no earlier axis implies a later one. Evidence: explorer-contract §§2,4; definitional review; `arcanum/spells/invoke/README.md:46-70`; `define.md:45-68`; `design.md:104-182`; `plan.md:333-397`; mixed clean/live-uncommitted, `OBSERVED`. Repaired.
- `SYS-002` — WPRA freezes and audits the agreement. Its audit and selected-unit verification are distinct, and both remain non-authoritative. Implementation Readiness coordinates a finite Work-Pack frontier but does not perform prerequisite-owner work or infer SWU completion. Evidence: explorer-contract §§2-3; explorer-runtime timeline 1-3; `work-pack-readiness-audit/README.md:194-210,280-342`; `implementation-readiness/README.md:47-100`; live-uncommitted, canonical fixture paths partly `EXECUTED`.
- `SYS-003` — Task Session consumes, but does not acquire, producer authority. It owns current entry checks, mutation admission, one admitted SWU’s execution, critical validation, an execution-terminal receipt, and the overall synchronized result after separate closeout. Exact material-producer identity remains deferred. Evidence: explorer-contract §§2-5; definitional review; `task-session/SKILL.md:148-420`; live-uncommitted; consumer admission fixtures `EXECUTED`, real producer/product/closeout chain `UNVERIFIED`. Repaired.
- `SYS-004` — Continuation Router admits, dispatches, and joins one exact owner hop. The selected capability retains semantic and mutation authority. Goal is a separate Craft-backed graph router. Evidence: explorer-closure dependency graph; `continuation-router/SKILL.md:118-170`; `goal/README.md:1-17`; `OBSERVED`.
- `SYS-005` — Craft owns recursive local project state. It cannot select an SWU, authorize mutation, establish a native result, replace Work-Pack authority, or promote a capability. Evidence: explorer-closure Craft section; `craft/SKILL.md:56-72,277-317`; `OBSERVED`.
- `SYS-006` — Execution terminal and synchronized completion are separate. Passing product execution plus failed or unjoined Refresh closeout preserves execution evidence but leaves the overall Task Session blocked. This is a normative contract claim; no product-through-real-Refresh positive witness was supplied. Evidence: explorer-contract §6G; non-vacuity review failure trace 3; `task-session/SKILL.md:351-420`; `OBSERVED`, E2E `UNVERIFIED`. Repaired.

## 3. Lifecycle graph and unresolved loop boundary

```text
intent
  -> Invoke Define
  -> Invoke Design
       -> authored Design
       -> denominator receipt
       -> fixed-point selection result
  -> Invoke Plan
       -> Plan artifact/handoff status
       -> Implementation Layering
       -> Distill
       -> Work Pack, SWUs, validation, closeout contracts
  -> WPRA frozen audit
       -> semantic manifest
       -> non-authoritative selected-unit verification
  -> consumer entry
       -> exact prerequisite owner hop | task-ready | block
  -> Task Session mutation admission
       -> one SWU execution
       -> execution-terminal receipt
       -> CloseoutSync
       -> Router joins separate Refresh/owner receipt
       -> synchronized result + continuity cursor

Separate outer-loop candidates:
  Implementation Readiness:
    rough-goal staging plus one-unit/finite-frontier/until-real-blocker Work-Pack loop

  Task Session Until Blocker:
    ordered Work-Pack frontier plus immutable chain of distinct Task Sessions
```

`DECISION-LOOP-OWNER-001` — The exact Work-Pack `until-real-blocker` boundary is unresolved. `implementation-readiness` claims `finite-frontier` and `until-real-blocker` execution and owns `execution_loop.py`; `task-session-until-blocker` separately claims bounded serial orchestration and owns `run_chain.py`. Both maintain frontier/visited/join/stop state. This synthesis does not select either owner, combine their reducers, or introduce a third runner. An owner-boundary decision must specify which reducer owns the series and where the other hands off.

Evidence: precedent review `CAP-002/CAP-007`; `arcanum/spells/implementation-readiness/README.md:11-16,47-100`; `arcanum/spells/task-session-until-blocker/README.md:1-37,79-115,211-217`; live-uncommitted, `OBSERVED`.

## 4. Owner and integration matrix

| ID | Owner | Artifact/state and exact ceiling | Evidence |
|---|---|---|---|
| `OWN-001` | Invoke Define | Spec/glossary/scope transport; definition completeness only | explorer-contract §2; `invoke/define.md:45-68`; clean, `OBSERVED` |
| `OWN-002` | Design author/extractor/validator | Design manifest, denominator, fixed-point result; Design evidence only, never Plan evidence | explorer-contract §§2-3; `invoke/design.md:104-182`; clean, `OBSERVED`; repaired wording |
| `OWN-003` | Invoke Plan | Plan, layering, Work Pack, SWUs, validation/closeout contracts; Plan artifact/handoff status only | explorer-contract §2; `invoke/README.md:46-70`; `invoke/plan.md:333-397`; live-uncommitted, `OBSERVED`; collapsed “mutation-handoff eligibility” removed |
| `OWN-004` | Distill | Coherence/recomposition result with `pass|flag|block`; no downstream authority | explorer-contract §2; `distill/SKILL.md:99-137,203-285`; clean, `OBSERVED` |
| `OWN-005` | WPRA | Frozen readiness report and semantic manifest; separately, non-authoritative selected-unit receipt; neither grants mutation | explorer-contract §§2-3; `WPRA README.md:194-210,280-342`; live-uncommitted, canonical selection fixture `EXECUTED`; repaired |
| `OWN-006` | Implementation Readiness | Policy, entry, binding, finite-frontier state, correlated joins; exact until-blocker overlap remains unresolved | explorer-runtime timeline 3; precedent review; `implementation-readiness/README.md:47-100`; live-uncommitted, integration fixtures `EXECUTED`; repaired |
| `OWN-007` | Context Builder | Exact bounded context pack; coverage evidence only | explorer-contract §2; `context-builder/SKILL.md:27-86`; clean, `OBSERVED` |
| `OWN-008` | Decision Gate / typed owner | Decision or one-use override for one consequential choice | explorer-contract §2; `decision-gate/SKILL.md:52-206`; clean, `OBSERVED` |
| `OWN-009` | Task Session | Consumer entry, admission, one-SWU execution-terminal receipt, derived synchronized result | explorer-contract §§2-5; `task-session/SKILL.md:148-420`; live-uncommitted, consumer paths partly `EXECUTED`, full chain `UNVERIFIED` |
| `OWN-010` | Continuation Router | One-hop route/admission/join receipt; never owner work | explorer-closure matrix; `continuation-router/SKILL.md:118-170`; live-uncommitted, route fixtures `EXECUTED` |
| `OWN-011` | Invoke Refresh | Proposal/applied synchronization and its owner receipt; phase pass is not apply authority | explorer-contract §§2,7.8; `invoke/refresh.md:185-255,317-325`; clean, `OBSERVED` |
| `OWN-012` | Craft | `.craft/ledger.yml` local state; views derived; never Work-Pack or lifecycle authority | explorer-closure Craft section; `craft/SKILL.md:56-72,277-317`; clean, `OBSERVED` |
| `OWN-013` | Dispatch Spec, Subagent Strategy, Orchestrate | Route validity, authorization, native spawn/join/gate/close evidence; no semantic/promotion authority | explorer-closure matrix; current SKILL contracts; `OBSERVED` |
| `OWN-014` | Sigil Development or Spellcraft; separate registry owner deferred | Lifecycle judgment belongs to the type-specific lifecycle owner. Registry release is a separate axis and receipt whose exact owner was not bound here | definitional review; `invoke/README.md:46-70`; lifecycle skill selectors cited by explorer-closure; `OBSERVED`; repaired |

## 5. Gate matrix

| ID | Gate and first stop | Forbidden inference/effect | Evidence |
|---|---|---|---|
| `GATE-001` | Design activation, denominator, fixed point | Design pass cannot prove Plan evidence | explorer-contract §3; `design.md:22-31,104-173`; clean, `OBSERVED` |
| `GATE-002` | Plan checks Design, layering, validation, and Distill | Plan `phase_status` or artifact status cannot set release/runtime axes or admit mutation | explorer-contract §3; `invoke/README.md:46-70`; `plan.md:333-397`; live-uncommitted, `OBSERVED`; repaired |
| `GATE-003` | Unknown, duplicate, ambiguous, or task-shaped SWU | No guessed unit or Context Builder entry | explorer-contract §6C; `plan.md:344-370`; `task-session/SKILL.md:113-141`; live-uncommitted, `OBSERVED` |
| `GATE-004` | Invalid semantic pointers/routes/digests or overlapping decisions | No selection from malformed manifest | explorer-runtime timeline 1; `plan_semantics.py:25-280`; canonical fixtures `EXECUTED`, generated parity blocked |
| `GATE-005` | Semantic drift or non-unique selected-unit membership | Selected-unit receipt stays non-authoritative; no entry/admission/mutation | explorer-runtime failure A; `verify_plan_selection.py:141-251`; live-uncommitted, `EXECUTED` |
| `GATE-006` | Stale policy/unit/binding/entry projection | No Context Builder, run-state write, owner dispatch, or mutation | explorer-runtime timeline 4; `fast_execution_entry_guard.py:63-207`; live-uncommitted, `EXECUTED` |
| `GATE-007` | Missing, stale, non-pass, unchanged, replayed, or unjoined owner evidence | No fresh admission or Task Session start | explorer-runtime failure C; split witnesses below; live-uncommitted, bounded fixtures `EXECUTED` |
| `GATE-008` | Missing/stale closeout inventory, baseline, owner contract, validation, delta class, or successor | No implementation write | explorer-contract §6F; `task-session/SKILL.md:229-240`; live-uncommitted, E2E `UNVERIFIED` |
| `GATE-009` | Package/receipt/schema/baseline/write/digest/replay mismatch | Consumer admission cannot establish actual mutation, lifecycle, registry, or publication authority | explorer-runtime failure B; `verify-mutation-readiness.py:347-470`; compatibility test source below; fixture-level `EXECUTED`, real producer identity/compatibility `UNVERIFIED`; repaired |
| `GATE-010` | Failed/unrun critical validation or undeclared output | No execution-terminal pass | explorer-contract §3; `task-session/SKILL.md:321-350`; live-uncommitted, `OBSERVED`; completion wording repaired |
| `GATE-011` | Closeout drift/failure/cycle/ambiguity/missing owner join | No synchronized result, continuity cursor, or next SWU execution | explorer-contract §6G; route fixtures cited by non-vacuity review; `task-session/SKILL.md:351-420`; fixtures `EXECUTED`, product E2E `UNVERIFIED` |
| `GATE-012` | Receipt mismatch/timeout plus global identity and exact-input admission | Dependent wave stays closed; current canonical code lacks pre-spawn global-ID uniqueness and exact receipt-file scoping | explorer-runtime failure E; reviewer defect evidence; `validate_run_evidence.py:128-258`; `native_dispatch_coordinator.py:334-340,499-507,560-571`; validator tests `EXECUTED`, canonical repair absent; repaired |

## 6. Artifact and receipt lineage

- `LIN-001` — Define transport → Design manifest/denominator/fixed-point result → separately authored Plan/layering/Work Pack/SWUs. Design never proves Plan evidence. Explorer-contract §§2-4; `design.md:104-173`; `plan.md:333-397`; `OBSERVED`.
- `LIN-002` — Frozen plan → readiness report/semantic manifest → selection handoff → non-authoritative selected-unit receipt → separate consumer entry → separate mutation admission. Explorer-contract §§3,5; `WPRA README.md:194-210,280-342`; live-uncommitted, selection fixtures `EXECUTED`.
- `LIN-003` — Selected unit + policy + execution binding + entry projection → fast-entry receipt. Semantic selected-unit verification and consumer-entry binding remain distinct. Explorer-contract §7.3; `task-session/SKILL.md:150-169`; live-uncommitted, `EXECUTED`.
- `LIN-004` — Material package + producer receipt/schema + current baselines → Task Session admission → single-use ledger → execution ticket. The test source loads `arcanum/spells/invoke/scripts/material_package_validator.py` and `task-session/scripts/verify-mutation-readiness.py` together, but the exact runtime producer identity and real cross-owner receipt chain remain deferred. Explorer-contract §7.4; precedent review `ATTACK-006`; `task-session/development/test_plan_once_admission.py:21-38,61-72,282-352`; source exists, not executed by this dispatch.
- `LIN-005` — Execution ticket → admitted writes → critical validation → execution-terminal receipt. This proves one SWU’s execution only. Explorer-contract §§3-4; `task-session/SKILL.md:321-350`; live-uncommitted, `OBSERVED`; repaired.
- `LIN-006` — Execution-terminal receipt + typed deltas/current baselines → `CloseoutSync` → separate Refresh/owner receipt → continuity cursor → synchronized Task Session result. Explorer-contract §6G; `task-session/SKILL.md:351-420`; normative `OBSERVED`, E2E `UNVERIFIED`.
- `LIN-007` — Persisted native action → globally unique action ID requirement → attempt → host result → wait registration/attempt → terminal/close → normalized receipt → exact-action-set reduction → gate. Canonical code currently violates pre-spawn global uniqueness and accepts a directory rather than an exact receipt set. Reviewer defect evidence; `native_dispatch_coordinator.py:334-340,499-507,560-571`; `OBSERVED`, failures reproduced; repaired.
- `LIN-008` — Native result → optional `.craft/ledger.yml` reference → derived views. Recording transfers no owner authority. Explorer-closure Craft section; `craft/SKILL.md:56-72,312-317`; `OBSERVED`.

## 7. Recent-change chronology

1. `CHG-001` — July 30 committed foundation at Arcanum `07b01c9`: deterministic Task Session governance, until-blocker chain, immutable WPRA, join/reconciliation/resume, and owner-hook work. Explorer-runtime chronology 1; `COMMITTED/OBSERVED`.
2. `CHG-002` — August 4–5 candidate changes add semantic selection, fast entry, mutation-admission consumption, Work-Pack prerequisite routing, fresh-session resume, finite outer loop, and closeout/native-join contracts. Explorer-runtime chronology 2; `LIVE-UNCOMMITTED/OBSERVED`; named fixtures partly `EXECUTED`. Commit identity does not bind these bytes; snapshot hashes above are non-durable working-tree evidence.
3. `CHG-003` — Generated WPRA provenance is known, but its bytes are stale. Canonical/generated hashes differ and generated semantics omit execution-policy, allowed-route, and selection-intent bindings. Explorer-runtime chronology 3; `GENERATED/OBSERVED`, parity `BLOCK`.
4. `CHG-004` — Task Session and Continuation Router generated provenance is likewise explicit through generated frontmatter, while current canonical/generated bytes diverge. Package-wide behavioral parity remains `UNVERIFIED`. Repaired from “source identity ambiguity.”
5. `CHG-005` — Reported canonical-live suites passed for selection, admission, governance, fresh resume, Work-Pack integration, and native event validation. Each result proves only its fixture/adapter path. It proves neither an exact Invoke-output-to-synchronized-result chain nor generated parity, promotion, registry release, or production. Explorer-runtime test list and non-vacuity review; `EXECUTED` with bounded ceiling.
6. `CHG-006` — Development invoke-run receipts and prototype closeout artifacts remain candidate evidence only. Explorer-runtime current receipts; `OBSERVED/UNVERIFIED` for production.

## 8. Normative and failure traces

### Killed exact-positive claim

`TRACE-NORMAL-001` — **KILLED** as an executed exact-positive witness. The cited plan-once test ends immediately after mutation admission and does not bind an exact Invoke output, execution-terminal receipt, real Refresh-owner join, synchronized result, or continuity cursor. `ATTACK-004` remains sustained.

### `EXPECTED-NORMAL-001` — Normative expected sequence

Invoke result → Design evidence → Plan/Work Pack → WPRA audit/manifest → selected-unit receipt → fast-entry receipt → context pack → closeout preflight → material producer receipt → mutation-admission receipt → single-use consumption → execution ticket → bounded mutation/critical validation → execution-terminal receipt → `CloseoutSync` → Router-dispatched real Refresh owner receipt → synchronized result and continuity cursor.

Proof ceiling: reported fixtures execute selected fragments through admission and static route validation. The complete chain is `UNVERIFIED`.

Evidence: non-vacuity review “Normal trace”; `test_plan_once_end_to_end.py:144-150`; `task-session/SKILL.md:148-420`; live-uncommitted.

### `TRACE-FAIL-001` — Stale semantic selection

One fault: change `execution_bindings[0].command.cwd` after audit. Selection recomputes semantics and returns `selectionVerdict=block`, `mutationReady=false`, `authorityEffect=none`, with `PLAN_EPOCH_STALE` or `PLAN_COMPONENT_CHANGED`. First stop: `verify_plan_selection.py:165-183`. No entry/admission/mutation. `test_plan_once_selection.py:278-291` was `EXECUTED`.

### `TRACE-FAIL-002` — **SUPERSEDED** bundled trace

The original mixed missing, stale, non-pass, unchanged, replay, and unjoined-owner faults. It is replaced by one-fault witnesses:

- `TRACE-FAIL-002A` — Set `helper_closeout=block`. Governance runner raises exact `RunnerBlock("continuation route is not a joined one-hop prerequisite result")` at `task-session-governance-runner.py:767-800`. No resume receipt or consumption ledger is emitted. Adversarial fixture `EXECUTED`; failure is an exception, not a durable negative receipt.
- `TRACE-FAIL-002B` — Missing owner receipt reference. Fresh-resume returns durable `decision=block`, `code=JOIN_RECEIPT_MISSING`, with zero fresh-session starts. `test-fresh-session-resume.py:326-344`; `EXECUTED`.
- `TRACE-FAIL-002C` — Stale owner receipt digest. Fresh-resume returns `decision=block`, `code=JOIN_RECEIPT_STALE`, zero starts. Same test selector; `EXECUTED`.
- `TRACE-FAIL-002D` — Owner result is non-pass. Fresh-resume returns `decision=block`, `code=OWNER_PREREQUISITE_BLOCKED`, zero starts. `fresh_session_resume.py:420-423`; test lines `326-344`; `EXECUTED`.
- `TRACE-FAIL-002E` — Reclassification still returns the same owner fingerprint. Fresh-resume returns `decision=block`, `code=UNCHANGED_PREREQUISITE_FINGERPRINT`. `fresh_session_resume.py:432-442`; test lines `346-368`; `EXECUTED`.
- `TRACE-FAIL-002F` — Reuse the same admitted fresh-session ID. Exclusive evidence write fails and returns `decision=block`, `code=FRESH_SESSION_REPLAY`, zero starts. `fresh_session_resume.py:550-584`; test lines `300-321`; `EXECUTED`.

All six stop before a new Task Session or product mutation. Their codes and artifact forms are not interchangeable.

### `TRACE-FAIL-003` — Target drift or admission replay

One fault per fixture: changed target bytes yields baseline mismatch; cross-attempt package reuse yields `material package plan binding mismatch`. Both stop before governance writes. Explorer-runtime failure B; `test_plan_once_admission.py:332-352`; reported `EXECUTED` by the explorer. Exact runtime producer identity remains unbound.

### `TRACE-FAIL-004` — Missing/failing closeout join

Execution-terminal evidence is preserved. Static Work-Pack route fixtures reject missing or failed owner joins and emit blocked route receipts such as `route-work-pack-missing-join-block.json` or `route-work-pack-owner-failure-block.json`; no executable returned route or continuity cursor is allowed. Fixture semantic validation was `EXECUTED`; real product-through-Refresh E2E remains `UNVERIFIED`. Repaired evidence ceiling.

### `TRACE-FAIL-005` — Native timeout contract

Attempt → host spawn return → wait registration → wait attempt → timeout → one interrupt → normalized timed-out receipt → dependent gate closed. Event-validator suites were `EXECUTED`; no actual host timeout occurred in this dispatch.

## 9. Confusion and bug map

- `BUG-001` — WPRA pass confused with mutation readiness. Preserve audit, selected-unit verification, and admission as separate states.
- `BUG-002` — Selected-unit verification confused with fast entry. Preserve semantic-unit and consumer-entry receipts separately.
- `BUG-003` — Producer package validation confused with Task Session consumer admission. Exact producer identity and real receipt chain remain deferred; source-level compatibility test exists but was not run by this dispatch.
- `BUG-004` — Plan closeout authoring, pre-write synchronizability, and post-run owner join appear duplicative but are separate temporal checks.
- `BUG-005` — Distill `flag` lacks a machine-bound assertion that every flagged gap is non-critical. The binding belongs in existing Plan/Work-Pack data, not a new readiness stage.
- `BUG-006` — Implementation Readiness can be mistaken for the sole multi-unit runner. Its overlap with Task Session Until Blocker is unresolved under `DECISION-LOOP-OWNER-001`.
- `BUG-007` — Refresh phase pass confused with apply authority. Require exact approval and package/receipt/handoff binding.
- `BUG-008` — Generated runtime treated as canonical-live parity. Provenance is known; currentness/parity is stale or divergent.
- `BUG-009` — **REPAIRED**: canonical/generated source identity is not ambiguous. Generated frontmatter identifies canonical sources; byte parity is the defect.
- `BUG-010` — **REPAIRED**: Inventory can prove its own source-path/stable-ID bindings, index rebuild equality, projection metadata/digests, and provenance. It cannot prove downstream source meaning, ontology/definition authority, lifecycle readiness, or promotion. `inventory/SKILL.md:247-285,335-339`; clean, `OBSERVED`.
- `BUG-011` — Execution-terminal pass confused with synchronized completion.
- `BUG-012` — Orchestrate’s `_load_receipts_directory` parses every `*.json`; unrelated governance JSON produced 30 receipt-shape errors. The exact-action-directory rerun passed.
- `BUG-013` — The resulting gate block was incorrectly attributable to explorer receipts; `driver-correction.json` records valid explorer receipts and no retry/respawn.
- `BUG-014` — **REPAIRED**: Goal is canonically bound. `arcanum/spells/goal/README.md:1-17,176-178` is the source contract; `.agents/skills/goal/SKILL.md:1-9` declares `canonical_source: spells/goal/README.md`. Goal is a registered Craft-backed router, not delegated-owner execution. Canonical and generated identity `OBSERVED`.
- `BUG-015` — The Orchestrate coordinator allocates the next wave with `start_action_number=len(actions)+1`, using current-wave cardinality rather than run-global history. After `spawn-0001..0004`, it emitted colliding `spawn-0002..0004`. The run-local deterministic remap to `spawn-0005..0007` preserved semantics, but no canonical code repair or regression test exists. `native_dispatch_coordinator.py:334-340,499-507`; `coordinator-action-id-extension.json`; reproduced `OBSERVED`.

`BUG-012` and `BUG-015` are distinct:

- receipt-directory overreach concerns which documents the reducer parses;
- action-ID allocation concerns globally unique causal identity before host effects.

Both parent corrections are run-local workarounds, not canonical repairs.

## 10. Craft role and non-role

- `CRAFT-001` — Craft may wrap execution for persistent recursive state, blockers, decisions, gaps, child contexts, receipts, and recomposition. `.craft/ledger.yml` is authoritative only inside that ledger scope. Explorer-closure Craft section; `craft/SKILL.md:56-72,193-203,241-317`; `OBSERVED`.
- `CRAFT-002` — Craft cannot replace Work Pack authority, selected-unit verification, mutation admission, native execution, Refresh synchronization, lifecycle judgment, or registry release. Same source; `OBSERVED`.
- `CRAFT-003` — Deferred route-exchange, projection, row-update, validation, and artifact-manifest schemas prohibit claims of a complete automated Craft runner/renderer. `craft/templates/ledger.schema.yml:24-47`; `OBSERVED`.

## 11. Minimal capability closure

- `CAP-001` — Invoke and Implementation Layering own authoring.
- `CAP-002` — WPRA owns audit and semantic selected-unit evidence; Implementation Readiness currently owns one outer-loop implementation. Its overlap with `CAP-007` remains an explicit decision, not a settled architecture.
- `CAP-003` — Task Session, Context Builder, and the applicable validation owner form the one-SWU execution core.
- `CAP-004` — Continuation Router is conditional and load-bearing for a typed prerequisite or closeout owner hop.
- `CAP-005` — Decision Gate is conditional for unresolved consequential choices.
- `CAP-006` — Distill owns recomposition evidence. Invoke Plan must bind flagged-gap criticality; no new gate is proposed.
- `CAP-007` — Task Session Until Blocker is an existing bounded serial runner, not merely a convenience. Whether it or Implementation Readiness owns exact Work-Pack `until-real-blocker` reduction remains unresolved.
- `CAP-008` — Goal is already canonically bound and generated as a registered Craft-backed router. Include it for broad dependent Craft graphs, not ordinary one-SWU work.
- `CAP-009` — Dispatch Spec, Subagent Strategy, and Orchestrate govern delegated work only.
- `CAP-010` — Sigil Development or Spellcraft owns lifecycle judgment; Experiment Harness, Signal Observer, and Workflow Reflect supply evidence, not promotion or registry release.
- `CAP-011` — Craft is optional recursive-state support, never readiness/admission/promotion.
- `CAP-012` — Inventory is optional discovery and lookup support. It can prove its own projection/index conformance and provenance, but is not a downstream semantic or lifecycle proof gate.
- `CAP-013` — Observability Setup is installation/verification support when the standard package is absent.

Evidence: explorer-closure “Minimal capability closure”; precedent and definitional reviews; direct selectors cited above. All are `OBSERVED` unless a narrower fixture result is stated.

## 12. Four operating playbooks

- `PLAY-001` — Ordinary feature: Define → validated Design → Plan/layering/Distill → WPRA audit → selected-unit verification → consumer entry → closeout preflight → admission → one-SWU execution-terminal result → separate Refresh closeout → synchronized result. This is normative; full E2E is `UNVERIFIED`.
- `PLAY-002` — New sigil: Sigil Development → admitted implementation units → Experiment Harness → Signal Observer → Workflow Reflect → lifecycle-owner decision. Registry release remains a separate, currently unbound owner axis.
- `PLAY-003` — New spell: Spellcraft → Dispatch Spec/Orchestrate only for multi-role work → experiment/observation/reflection → Spellcraft lifecycle decision. Registry release remains separate.
- `PLAY-004` — One selected SWU follows fast entry through synchronized closeout. For an explicit ordered series, stop and resolve `DECISION-LOOP-OWNER-001` before choosing Implementation Readiness’s outer loop or Task Session Until Blocker’s chain runner. Do not compose both reducers or invent a third.

## 13. Reviewer attack ledger

- `ATTACK-001` — Generated WPRA byte parity remains blocked.
- `ATTACK-002` — Generated Task Session/Continuation Router behavioral parity remains unproved.
- `ATTACK-003` — August 4–5 sources are live-uncommitted; snapshot hashes do not equal immutable commit/patch identity.
- `ATTACK-004` — Sustained: no exact Invoke-output-through-execution-and-real-Refresh-closeout positive witness exists.
- `ATTACK-005` — Distill flagged-gap criticality binding remains missing.
- `ATTACK-006` — Repaired scope: compatibility test source exists and loads Invoke’s material validator with Task Session admission, but this dispatch did not execute it. Exact runtime material-producer identity and real producer-to-consumer receipt compatibility remain deferred.
- `ATTACK-007` — Superseded/repaired: Goal canonical and generated identity are now bound.
- `ATTACK-008` — Superseded/repaired: provenance is known; byte parity/currentness is stale or divergent.
- `ATTACK-009` — Deferred Craft schemas still forbid automated-loop claims.
- `ATTACK-010` — Timeout tests remain event-contract evidence, not actual host-timeout evidence.
- `ATTACK-011` — Receipt-directory defect remains canonically unrepaired. The action-only rerun is a run-local workaround.
- `ATTACK-012` — Deferred provenance residue: the normalized explorer receipt has the correct `-route` dispatch ID; the claimed verbatim mismatch is not independently persisted for reviewer reproduction.
- `ATTACK-013` — Source-only contract/closure rows remain `OBSERVED`; only specifically reported test paths are `EXECUTED`.
- `ATTACK-014` — Development fixtures and receipts prove neither lifecycle promotion, registry release, deployment, nor production.
- `ATTACK-015` — New and sustained: the canonical coordinator reuses wave-local action IDs and lacks pre-spawn run-global uniqueness validation. The `spawn-0005..0007` extension is a run-local semantic-preserving workaround, not a canonical repair.

## 14. Stable-ID disposition

Repaired in place:

- `SYS-001`, `SYS-003`, `SYS-006`
- `OWN-002`, `OWN-003`, `OWN-005`, `OWN-006`, `OWN-009`, `OWN-014`
- `GATE-002`, `GATE-009`, `GATE-010`, `GATE-012`
- `LIN-004`, `LIN-005`, `LIN-007`
- `CHG-004`, `CHG-005`
- `TRACE-FAIL-004`
- `BUG-005`, `BUG-006`, `BUG-009`, `BUG-010`, `BUG-014`
- `CAP-002`, `CAP-007`, `CAP-008`, `CAP-010`, `CAP-012`
- `PLAY-001`, `PLAY-002`, `PLAY-003`, `PLAY-004`
- `ATTACK-006`, `ATTACK-011`, `ATTACK-012`

Sustained without semantic change:

- `SYS-002`, `SYS-004`, `SYS-005`
- `OWN-001`, `OWN-004`, `OWN-007`, `OWN-008`, `OWN-010..013`
- `GATE-001`, `GATE-003..008`, `GATE-011`
- `LIN-001..003`, `LIN-006`, `LIN-008`
- `CHG-001..003`, `CHG-006`
- `TRACE-FAIL-001`, `TRACE-FAIL-003`, `TRACE-FAIL-005`
- `BUG-001..004`, `BUG-007`, `BUG-008`, `BUG-011..013`
- `CRAFT-001..003`
- `CAP-001`, `CAP-003..006`, `CAP-009`, `CAP-011`, `CAP-013`
- `ATTACK-001..005`, `ATTACK-009`, `ATTACK-010`, `ATTACK-013`, `ATTACK-014`

Killed:

- `TRACE-NORMAL-001` as an executed exact-positive witness.

Superseded:

- `TRACE-NORMAL-001`’s normative content by `EXPECTED-NORMAL-001`.
- Bundled `TRACE-FAIL-002` by `TRACE-FAIL-002A..002F`.
- `ATTACK-007` and `ATTACK-008` in their original “missing/ambiguous identity” forms.

Added:

- `DECISION-LOOP-OWNER-001`
- `EXPECTED-NORMAL-001`
- `TRACE-FAIL-002A..002F`
- `BUG-015`
- `ATTACK-015`

Deferred:

- Exact material-producer runtime owner and real producer receipt chain.
- Exact registry-release owner and current registry-owner receipt.
- Product-through-real-Refresh synchronized positive witness.
- Implementation Readiness versus Task Session Until Blocker series ownership.
- Canonical fixes and regression receipts for both Orchestrate defects.
- Generated package parity.
- Immutable patch identity for the live-uncommitted capability closure.

## 15. Reviewer-repair disposal

1. Invoke phase status and all three capability axes are explicitly separated.
2. Design, WPRA audit/selection, admission, execution terminal, synchronized completion, lifecycle decision, registry release, Inventory-native proof, and Craft state are separately qualified.
3. Goal canonical/generated identity and the existing admission compatibility test source are bound; no execution of that test is claimed.
4. Material-producer identity/real compatibility and registry-release ownership remain explicitly deferred.
5. `TRACE-NORMAL-001` is killed as an executed witness; `EXPECTED-NORMAL-001` is normative only; `ATTACK-004` remains open.
6. The bundled prerequisite trace is split into six one-fault witnesses with exact diagnostics and artifact ceilings.
7. `BUG-015` and `ATTACK-015` record the separate global action-ID defect; both orchestration corrections are run-local workarounds.
8. Inventory-native conformance/provenance proof is preserved while downstream authority is denied.
9. Implementation Readiness versus Task Session Until Blocker is an unresolved owner-boundary decision; no third runner is proposed.
10. Generated provenance is known; stale/divergent parity is the defect.
11. Observed/executed/unverified ceilings and live-uncommitted digest limitations are explicit.

```json
{
  "revision_id": "synthesis-zig-zag-01",
  "dispatch_id": "2026-08-05-arcanum-building-system-research-route",
  "run_id": "arcanum-building-system-research-run-01",
  "action_id": "spawn-0004",
  "role": "synthesizer",
  "status": "pass",
  "validation": "pass",
  "artifact": "native-agent-return:/root/synthesizer_spawn_0004#revision-1",
  "blockers": [],
  "deferred": [
    "exact-material-producer-runtime-owner-and-real-compatibility",
    "exact-registry-release-owner-and-receipt",
    "product-through-real-refresh-closeout-positive-witness",
    "implementation-readiness-vs-task-session-until-blocker-owner-decision",
    "canonical-orchestrate-receipt-scope-repair",
    "canonical-orchestrate-global-action-id-repair",
    "generated-package-parity",
    "immutable-patch-identity-for-live-uncommitted-sources"
  ],
  "repository_writes": []
}
```
