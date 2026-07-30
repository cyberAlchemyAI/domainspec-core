# Invoke one-shot workflow research transcript

This file mechanically preserves the explorer returns. Synthesis, skepticism,
and final findings are separate artifacts.

## Explorer return 1: local owner-hop forensics

STATUS: pass

VALIDATION: pass

ARTIFACTS:

- `arcanum/spells/invoke/README.md#Purpose`, `#Evidence-Capability-Contract`, `#Lifecycle-Authority-Chain`, `#Distill-Validation`, `#Global-Gates`, `#Global-Failure-Policy` (especially lines 20-26, 46-76, 98-107, 168-178, 280-324)
- `arcanum/spells/invoke/{define.md,design.md,plan.md,refresh.md,handoff.md,validate.md}` mode contracts
- `arcanum/arcana/task-session/SKILL.md#Step-0---Route-Multi-Session-Intent`, `#Step-1---Resolve-Task-Scope`, `#Step-2---Build-Context-Pack`, `#Step-4---Evaluate-Gates` (lines 22-39, 100-154 and mutation-admission sections)
- `.arcanum/observability/reflections/20260723T235741Z-invoke-plan-refresh-churn-reflection.md#Evidence-boundary`, `#Patterns-found`, `#Proposed-iterations`
- `.arcanum/observability/reflections/20260730T163236Z-invoke-refresh-transition-collision-reflection.md#Direct-answer`, `#Evidence-timeline`, `#Findings` (lines 17-110)
- `projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/INVOKE-REPORT.md#Define`, `#Design`, `#Plan`, `#Decisions-And-Gaps`, `#Capability-Ceiling-And-Next-Route` (lines 14-74, 99-126)
- The same run’s `SPEC.md`, `ARCHITECTURE.md`, `UX-PLAN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `EXECUTION-PACK.md`, `PLAN-TRANSPORT.md`, and `CONTINUATION.json`
- `.../refreshes/20260730T065606Z-source-backed-hover-briefs/REFRESH-REPORT.md#Outcome`, `#Plan-refresh`, `#Next-route`
- `.../refreshes/20260730T085945Z-continuation-route-sync/REFRESH-REPORT.md#Source-signal`, `#Applied-delta`, `#Ceilings-and-next-route`
- `.../refreshes/20260730T090724Z-swu-bwaa-001-material-admission/REFRESH-REPORT.md#Outcome`, `#Material-evidence`, `#Boundaries`, `#Next-route`
- `.../refreshes/20260730T090724Z-swu-bwaa-001-material-admission/TASK-SESSION-HANDOFF.json` selectors `created_at`, `status`, `mutation_ready`, `admission_probe`, `material`, `context_pack`, `closeout_owner_contract`, `live_product_mutation_started`
- `.../work-pack/session-evidence/20260730T085748Z-bwaa-all-until-blocker/CHAIN-REPORT.md#Frozen-frontier`, `#Evidence`, `#Continuation`
- `.../work-pack/session-evidence/20260730T085748Z-bwaa-all-until-blocker/CONTINUATION-HANDOFF.json#blocker`, `#probable_next_route`, `#resume_condition`
- `.../work-pack/session-evidence/20260730T164538Z-bwaa-until-blocker/CHAIN-REPORT.md#Preflight`, `#First-Blocker`, `#Closeout`, `#Resume-Route` (lines 14-68)
- `.../work-pack/session-evidence/20260730T164538Z-bwaa-until-blocker/CHAIN-STATE.json` selectors `stop_reason`, `next_route`, `blocker_fingerprint`
- `cyberAlchemy-v2/development/ontology-evidence-workbench/research/2026-07-29-runtime-rebuild-lessons/findings.md#Plain-language-finding`, `#Blocker-chronology-and-measured-churn` (lines 5-22, 42-63)
- `cyberAlchemy-v2/development/ontology-evidence-workbench/research/2026-07-29-runtime-rebuild-lessons/research.md#Agent-2---Simon-Herbert` (lines 33-45)
- `projects/domainspec-v2/development/specified-first-order-logic-framework/WORK-PACK.md` history rows 2026-07-23 through 2026-07-27
- `projects/domainspec-v2/development/specified-first-order-logic-framework/INVOKE-RESULT.md` selectors `Current blocker`, `Next route`
- Central counts were rechecked against both reflection evidence windows; Inventory entries were used only as discovery leads.

BLOCKERS: none

RESEARCH RETURN:

Plain-language finding: the recurring loop is not evidence that fail-closed Task Session is too strict. Invoke can produce a locally valid Plan while explicitly leaving `mutation_runtime_ready` unevaluated; Task Session then becomes the first owner to test exact executable-material and closeout completeness. That mismatch pushes predictable admission defects across the owner boundary. Generic `Refresh` subsequently performs three distinct jobs—planning repair, projection synchronization, and executable handoff materialization—so local passes obscure lifecycle non-progress. The contracts themselves preserve the necessary non-collapse: Invoke authors; Task Session executes one SWU; an authored Plan does not imply runtime readiness (`arcanum/spells/invoke/README.md:24-26,51-70,95-107`; Task Session lines 33-39, 100-111).

Timestamped Body War owner-hop graph:

```text
2026-07-30T06:24:53Z Invoke Define→Design→Plan
  pass; 4 SWUs initially; selected_swu none; mutation_runtime_ready not evaluated
  ↓
2026-07-30T07:11:57Z Invoke Refresh / planning-refresh
  22 planning/content targets rewritten; work pack becomes 5 SWUs
  no SWU selected, no implementation
  ↓
2026-07-30T09:01:59Z Task Session Until Blocker
  freezes five-SWU frontier; BLOCK before invoking a selector
  missing exact SWU-001 material package, producer receipt/schema, closeout contract
  ↓ return to Invoke
2026-07-30T09:04:43Z Invoke Refresh / projection-sync
  one `CONTINUATION.json.next_route` field rewritten
  no executable evidence; invalidates the old closeout-preflight byte binding
  ↓ remains at Invoke
2026-07-30T09:15:22Z Invoke Refresh / materialize-handoff
  exact 3-target staged package + receipt/schema + strict context + closeout contract
  admission=`admit`; mutationReady=true; live mutation still false
  ↓ ready for Task Session
2026-07-30T16:45:38Z Task Session Until Blocker
  empirical concurrent write-target drift after baseline capture
  BLOCK; observed bytes equal staged outputs, but writer attribution and terminal receipt absent
  ↓ return to bounded drift reconciliation
2026-07-30T16:53:51Z onward
  owner closeout receipts show SWU-001 then SWU-002 then SWU-005 advancing;
  this later progress does not erase the two earlier bounces.
```

Blocker matrix:

| Blocker | First knowable | First detected | Responsible owner | Rewritten artifacts | Safety protected? | Product advanced? | Earliest deterministic gate |
|---|---|---|---|---|---|---|---|
| First SWU lacks material package, producer receipt/schema, and closeout-owner contract | Plan/handoff compilation, once routed-mutation profile and SWU-001 were known | First Task Session preflight, 09:01:59Z | Invoke Plan/handoff must name and prove the material owner; materializer produces bytes; Task Session only verifies | Later materialization created three staged product post-images plus package/receipt, context pack, closeout contract; planning refresh had already rewritten 22 controls | Yes: no selector/product mutation ran | No at detection; later executable evidence advanced | A Plan-to-Task-Session execution-admission completeness gate checking the exact five required inputs before emitting the route |
| Continuation projection omitted Context Builder | Initial Plan/continuation emission | Operator-requested projection-sync, 09:04:43Z | Invoke continuation projection | One field in `CONTINUATION.json` | Yes | No | Deterministic continuation-route schema/semantic validator at Plan output |
| Projection-only route edit invalidated exact closeout baseline | Knowable when mutable `CONTINUATION.json` was chosen as a byte-bound join target | After route sync, confirmed by reflection | Plan/closeout protocol owner, not Task Session verifier | Same one-field projection rewrite; later handoff superseded preflight | Yes, exact binding caught staleness | No | Plan-epoch gate plus semantic delta classifier excluding projection-only views from execution-invalidating baselines |
| Concurrent three-target write drift after fresh baseline | Not knowable as a future event; only the possibility was known and recorded as `BWAA-DRIFT` | Second Task Session, 16:45:38Z | External/unknown writer; Task Session correctly owns detection | Task Session rewrote nothing; observed current product bytes and regenerated coverage evidence only | Yes: refused overwrite/adoption without attribution/receipt | Bytes had advanced to staged-equivalent state, but no attributable Task Session capability advance | No preflight can prevent a post-baseline concurrent write; the earliest honest gate is the immediately-before-mutation digest recheck that fired |
| OEW absent `L1-BUILD.lock.json` ownership | Work-pack/lock ownership closure | `013B` attempt 001 | OEW Plan/execution-contract owner | 1 lock + 8 governance projections | Yes | No | Closed write-set/required-input ownership audit before selection |
| OEW incomplete effective build order after `--ignore-scripts` | Plan command-graph compilation | `013B` attempt 002 | OEW execution-plan owner | Lock + 7 governance projections | Yes | No | Clean deterministic dry-run of the frozen command graph before Task Session |
| OEW 48 strict TypeScript errors | Potentially discoverable by compiling planned immutable overlay before selection; empirically confirmed only by `tsc -b` | `013B` attempt 003 / clean replay | Product source owner (`loadOewBundle.ts`, `store.ts`, `types.ts`) | Later typed-overlay refresh changed 9 governance projections; no implementation repair yet | Yes | No browser/product advance | Exact pre-admission build witness; unlike concurrency drift, this deterministic compiler failure was discoverable preflight |

Counts, with scope made explicit:

- Body War through the ready 09:15 handoff: **3 Refreshes**, exactly **1 planning-package rewrite** (22 targets), **1 projection-only rewrite**, **1 materialization run**.
- Body War Task Session bounces in the full current evidence: **2**—missing material at 09:01 and write-target drift at 16:45.
- Body War baseline invalidations/staleness events: **2**—projection-only `CONTINUATION.json` digest change and later three-target post-baseline drift.
- Body War no-progress owner returns: **1 strict return** (the projection sync remained with Invoke and changed no blocker/executable evidence). The first Task Session→Invoke return is a bounce, but the subsequent materialize-handoff changed the blocker fingerprint and is therefore progress, not a no-progress return.
- OEW strongest prior sequence: **4 consumed Task Sessions** from first-working selection (`008F` plus three `013B`), **3/4 blocked**, **at least 56 governance path-write events versus 28 implementation writes**, and **zero browser witnesses**. Governance rewrites were 24 + 6 + 9 + 8 + 9; the latter three correspond to two predictable execution-contract repairs and one product-repair ownership projection.
- Central longitudinal evidence: on 2026-07-23, **58 Invoke-shaped rows / 30 Refresh rows**, with **10 of 13 recent rows Refresh**; by 2026-07-30, **99 Invoke-shaped / 52 Refresh**, 95 meaningful executions, 20 workflow gaps, one output-contract-drift event.

Strict classification:

- **Discoverable preflight blockers:** missing material/receipt/schema; missing closeout-owner contract; malformed/omissive continuation route; mutable projection included in execution baseline without semantic invalidation type; absent OEW lock owner; incomplete OEW build order. The 48 TypeScript errors are also preflight-discoverable because the exact frozen build deterministically reproduces them, although they are ordinary product defects rather than governance defects.
- **Empirical runtime failures/residue:** Body War’s post-baseline concurrent write event is empirical because its occurrence and writer could not be known before the baseline; only the drift policy could be predeclared. Browser behavior, unavailable runtime, flaky external dependencies, and failures arising only while executing admitted commands remain honest empirical residue.
- **Not runtime failures:** human selection, planning refresh, projection sync, materialization, and OEW’s missing lock/build-order defects. These are admission/ownership/plan-graph transitions.
- **Interrupted/incomplete state:** OEW `007T` attempt 001 is neither a proven blocker nor runtime failure; it ended before admission and recorded no technical blocker.

The evidence supports moving every deterministic ownership, dependency, material, validation-command, continuation, and closeout check into an execution-admission compilation gate before Task Session routing. It does not support promising that a complete artifact prevents concurrent drift or future runtime failures, weakening digest checks, merging execution into Invoke, or removing Task Session’s one-SWU boundary.

STARTED_AT: 2026-07-30T17:02:56Z

FINISHED_AT: 2026-07-30T17:06:38Z

## Explorer return 2: primary-source precedents

STATUS: pass

VALIDATION: pass

ARTIFACTS:

- Local, read-only:
  - `ops/development/2026-07-30-invoke-one-shot-workflow-research/dispatch-sheet.json#groups[group_id=explorers].agents[agent_name="Simon, Herbert"]`
  - `ops/development/2026-07-30-invoke-one-shot-workflow-research/strategy-inventory-packet.json#selected_matches`
  - `ops/development/2026-07-30-invoke-one-shot-workflow-research/strategy-inventory-packet.json#unresolved_gaps`
  - `.agents/skills/domainspec-subagents-strategy/SKILL.md#Research-And-Review-Inventory-Preflight`
- Primary external:
  - LLVM 24.0.0git, [“LLVM’s Analysis and Transform Passes,” Introduction](https://llvm.org/docs/Passes.html#introduction), especially analysis/transform separation and explicit analysis invalidation.
  - Bazel 5.1.1, [Glossary: Action graph, Action key, Analysis phase, Execution phase](https://docs.bazel.build/versions/5.1.1/glossary.html).
  - Terraform current CLI docs, [`terraform plan`: Introduction and Other Options](https://developer.hashicorp.com/terraform/cli/commands/plan); Terraform Enterprise, [Remote Saved Plans](https://developer.hashicorp.com/terraform/enterprise/workspaces/run/cli#remote-saved-plans).
  - Temporal Platform docs current as retrieved 2026-07-30, [Workflow Execution overview: Durability, Reliability, Replays, Commands, Status](https://docs.temporal.io/workflow-execution); [Worker Versioning: concepts and choosing a versioning behavior](https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning).
  - OMG ReqIF 1.1, adopted October 2013, immutable OMG file ID `formal/13-10-01`, [normative specification record](https://www.omg.org/spec/ReqIF/1.1/); normative XSD file ID `dtc/11-04-05`.
  - Hector Garcia-Molina and Kenneth Salem, “Sagas,” SIGMOD 1987, pp. 249–259, DOI [`10.1145/38713.38742`](https://doi.org/10.1145/38713.38742), especially the saga definition/recovery model.

BLOCKERS: none

RESEARCH RETURN:

The desired Arcanum pattern is **build-from-owned**, not precedent-clean and not already owned end-to-end. The Inventory packet shows accepted local ownership for planning/review, readiness evidence, bounded Task Sessions, and fail-closed routing, while explicitly recording three unowned compositions: a normalized cross-owner plan epoch, semantic invalidation spanning Invoke through closeout, and a proven outer frontier run without generic Refresh bounce. External precedents supply mature mechanics for those joins, but none should be imported as a new monolithic “workflow engine.”

| Precedent | Exact behavior owned | Detects before execution | Unknown runtime failures | Plan/version invalidation | Resume semantics | Transfer / do not transfer | Classification |
|---|---|---|---|---|---|---|---|
| LLVM pass pipeline | Analysis passes compute facts; transforms consume them and may invalidate them; code-generation preparation is a distinct transform. | Structural/semantic facts expressible over available IR: dominance, dependencies, aliasing, stack safety, etc. It cannot prove environmental properties absent from its model; LLVM explicitly notes examples where a transform assumes an environment rather than verifies it. | Later transforms/code generation may still fail or encounter target/environment limits. Analysis is not a promise of successful execution. | A transform must preserve or invalidate analysis results; stale derived facts are not silently authoritative. | Recompute invalidated analyses and continue through the pipeline; not durable operational replay. | Transfer explicit producer/consumer declarations and invalidation sets for every derived readiness fact. Do not treat Invoke as a compiler that can prove future environment behavior, or collapse planning and execution into one pass manager. | Build-from-owned: local stages exist; explicit cross-stage invalidation is the missing composition. |
| Bazel analysis/execution graph | Loading resolves packages; analysis evaluates rules into an in-memory action graph; execution runs only those actions. Actions declare inputs, outputs, command/environment metadata; action keys drive deterministic reuse/invalidation. | Missing/invalid targets, rule-analysis failures, dependency and declared-artifact graph defects, conflicting producers, and action scheduling structure. | Compilers/scripts can still fail, machines can fail, and undeclared environmental behavior can escape analysis. Failure remains attached to the action; the graph is not retroactively “incomplete planning.” | Action keys invalidate cached results when relevant metadata changes. The action graph is derived, not canonical intent. | Re-run only invalidated or failed work where keys and outputs permit; cache survives server restarts. | Transfer a compiled execution-admission graph with single output ownership, declared inputs/outputs, per-SWU keys, and selective invalidation. Do not transfer hermeticity claims until Arcanum inputs and environments are actually pinned, and do not make the generated graph canonical intent. | Build-from-owned: Context Builder/readiness/Task Session provide ingredients; an action-graph-like admitted projection is missing. |
| Terraform saved plan/apply | `plan` refreshes observed state, compares configuration with prior state, proposes actions without applying; `-out` creates an opaque executable artifact; applying a saved plan performs those reviewed actions. Remote saved plans are discarded when their base state becomes stale. | Configuration errors, state/config differences, provider planning errors, and the proposed action set. Speculative plans explicitly may diverge if the target changes before apply. | Provider/API failures and drift can occur during apply. Terraform does not claim that a successful plan guarantees apply success. | Saved plan binds configuration, values, options, and the state snapshot. HCP Terraform automatically detects/discards stale remote saved plans after the underlying state changes. | Re-plan after staleness; after partial apply, refresh state and produce a new plan rather than pretending the old plan remains exact. | Transfer an opaque/hash-bound plan epoch, explicit speculative versus admitted status, approval of exact bytes, and fail-closed stale-plan rejection. Do not transfer secrets-in-plan behavior, global infrastructure refresh semantics, or automatic approval bypass. | Strongest build-from-owned precedent for exact admission; no local owner currently spans the whole binding. |
| Temporal durable workflows | Workflow code emits commands; service records resulting events; replay regenerates commands and checks them against Event History. State persists through outages and resumes from the last recorded event. | Determinism/replay compatibility and workflow-level command structure; not whether external activities will succeed. | Activity/workflow failures, retries, cancellation, timeout, and termination remain explicit states. Runtime failure is durable residue, not evidence that discovery should have predicted it. | Replay-incompatible code is unsafe. Worker Versioning pins executions to a build or requires replay-safe patching for auto-upgrade workflows. | Replay from Event History; retry/continue-as-new form an execution chain. | Transfer append-only transition history, exact command/event matching, resumable outer routing, and explicit workflow-version binding. Do not transfer an always-on service, hidden retries, “effectively once” wording for external side effects, or erase the one-SWU inner Task Session boundary. | Build-from-owned: Goal/Task Session/observability own pieces; durable outer replay across SWUs is unowned. |
| OMG ReqIF 1.1 | Standardized interchange of typed requirement objects, attributes, specifications, and explicit relations across tools; normative XML schema gives stable identities and machine validation. | Schema/type/reference defects in the exchanged requirement package, plus missing links if a profile makes them mandatory. It does not validate implementation feasibility or execution readiness. | Outside scope: operational failures remain with downstream engineering/execution systems. | Identity/version/change must be reconciled by the consuming repositories; the standard preserves structure but does not define Arcanum-like plan epoch admission. | Re-import/merge/reconcile exchanged requirement sets; no execution checkpoint replay. | Transfer stable IDs, typed relation edges, source/target traceability, and machine-validatable required fields into the objective-execution manifest. Do not mistake trace completeness for decision closure, readiness, or successful execution. | Already owned in principle by local typed artifacts and evidence links; build-from-owned only for enforcing complete cross-stage trace edges. |
| Saga transactions | A long-lived transaction is decomposed into committed subtransactions with corresponding compensating transactions; interleaving is allowed, avoiding a single long-held transaction. | Known sequence and declared compensations can be checked before start. It cannot predict arbitrary failures or guarantee that real-world effects are perfectly reversible. | On failure, execute compensations according to the saga recovery policy; failures remain operational and may require forward recovery/manual residue. Compensation is not database rollback. | The admitted saga definition must be version-bound; changing steps or compensations during a live saga requires migration/versioning, though the 1987 paper does not provide a modern deployment protocol. | Resume forward from durable progress or compensate completed steps; do not replay already committed external effects blindly. | Transfer per-SWU commit receipts, explicit compensation/repair owner, and terminal residue when compensation is unavailable. Do not promise atomic rollback across repository/external effects or turn every SWU into a reversible transaction. | Build-from-owned: Task Session/closeout provide boundaries, but compensation metadata and outer recovery policy are not normalized. |

Transferable invariants:

1. **Admission binds exact derived work to exact authority inputs.** The executable projection must carry hashes/versions for objective, decisions, dependencies, materials, validation contracts, and owner routes. Any semantically relevant change invalidates the epoch before another SWU starts.

2. **Derived artifacts declare preservation and invalidation, never inherit authority by convenience.** Like LLVM analyses and Bazel action graphs, readiness facts and continuation projections need explicit producers, consumers, and invalidation sets. Regeneration must not create a new canonical plan silently.

3. **Preflight completeness is bounded by knowability.** Schema, ownership, dependency, material, trace, and declared-environment defects belong before admission. Provider failures, tool crashes, race conditions, and genuinely new drift remain typed runtime residue. A “complete plan” must never mean empirical certainty.

4. **Replay is receipt-driven and effect-aware.** Resume from the last accepted transition, skip only work whose key and evidence remain valid, and never blindly repeat an external side effect. Failed steps require retry policy, compensation/repair ownership, or an explicit terminal blocker.

5. **Outer durability must preserve inner bounded execution.** One approved work-pack route may traverse a finite SWU graph, but every SWU remains a separately admitted Task Session with its own inputs, mutation boundary, validation, receipt, and closeout. The outer route coordinates; it does not absorb Task Session ownership.

No writes were made. The pre-existing dirty worktree remained untouched.

STARTED_AT: 2026-07-30T17:02:56Z

FINISHED_AT: 2026-07-30T17:06:46Z

## Explorer return 3: formal protocol

STATUS: pass

VALIDATION: pass

ARTIFACTS:

- `ops/development/2026-07-30-invoke-one-shot-workflow-research/dispatch-sheet.json#groups[group_id=explorers].agents[agent_name="van Lamsweerde, Axel"]`
- `ops/development/2026-07-30-invoke-one-shot-workflow-research/strategy-inventory-packet.json#selected_matches,#unresolved_gaps,#design_consequences`
- `.agents/skills/domainspec-subagents-strategy/SKILL.md#Arcanum-Core-Boundary,#Lifecycle` — generated runtime consulted to obey the dispatched route; it points to the private repo-local owner.
- `arcanum/spells/invoke/README.md#Mode-Contracts,#Lifecycle-Authority-Chain,#Mode-Router,#Global-Gates`
- `arcanum/spells/invoke/define.md#Inputs,#Execution-Phases,#Mode-Gates`
- `arcanum/spells/invoke/design.md#Design-Selection-Protocol,#Execution-Phases,#Mode-Gates`
- `arcanum/spells/invoke/plan.md#Activation-Gate,#Planning-Artifact-Boundary-Policy,#Smallest-Working-Unit-Policy,#Execution-Phases,#Mode-Gates` (especially lines 281-327)
- `arcanum/spells/invoke/refresh.md#Refresh-Signal-Model,#Mutation-Modes,#Mode-Gates,#Phase-Status,#Blocker-Scope`
- `arcanum/spells/invoke/handoff.md#Context-Builder-Policy,#Output-Contract,#Mode-Gates`
- `arcanum/spells/invoke/validate.md#Identity,#Deferral-Reason,#Planned-Scope-Draft` — currently deferred; it is not a live lifecycle-validation owner.
- `arcanum/arcana/task-session/SKILL.md#Step-1---Resolve-Task-Scope,#Step-2---Build-Context-Pack,#Step-3---Build-Decision-Pack,#Step-4---Evaluate-Gates,#Step-5A---Verify-Routed-Mutation-Admission,#Step-7---Validate-Completion,#Step-8---Synchronize-Evidence` (mutation admission lines 216-259)
- `arcanum/spells/task-session-until-blocker/README.md#Preconditions,#Shared-Chain-State,#Phases,#Stop-Conditions,#Authority-Boundaries` (lines 64-168)
- `arcanum/spells/goal/README.md#Purpose,#Control-Spine,#Gates,#Failure-Policy`
- `arcanum/transmutations/context-builder/SKILL.md` process steps 1-14 and `#Context-Pack-Summary`
- `arcanum/arcana/decision-gate/SKILL.md` process steps 1-15 and `#Decision-Gate-Result`
- `arcanum/arcana/structured-interview-kits/SKILL.md` process steps 1-12 and `#Structured-Interview-Result`
- `arcanum/spells/work-pack-readiness-audit/README.md#Input-Contract,#Shared-State,#Phase-Contract,#Verdicts,#Failure-Policy` (lines 56-214)

BLOCKERS: none for this research return. Implementation remains blocked on an approved capability-design/migration route and fixtures; `invoke validate` is deferred and must not be represented as current enforcement.

RESEARCH RETURN:

### Root conclusion

The target should not be “a more exhaustive Plan” or “automatic Refresh.” The repository already separates:

- Invoke Define: objective/concept baseline.
- Invoke Design: selected architecture, exact concern denominator, accountable/contributing/artifact/validator owners.
- Invoke Plan: executable decomposition, SWUs, validation and closeout contracts.
- Context Builder: obligation-linked evidence coverage.
- Interrogation: one-question-at-a-time ambiguity reduction.
- Decision Gate: consequential multi-option closure.
- Work Pack Readiness Audit: immutable, non-mutating frontier proof.
- Task Session: mutation admission and execution of exactly one bounded unit.
- Task Session Until Blocker: bounded sequencing of fresh one-unit Task Sessions.
- Invoke Refresh: evidence-backed lifecycle-state synchronization.
- Goal: generic risk-classified autonomous DAG control, approval-gated promotion.

The missing mechanism is a distinct **execution-admission compiler/materializer** between authored Plan and frontier execution. It should normalize already-owned outputs into one exact manifest, prove closure with Work Pack Readiness Audit, freeze a plan epoch, and issue the sole outer-run admission receipt. It does not discover product intent, make unresolved choices, author the Plan, execute SWUs, or refresh lifecycle state.

### Target protocol

1. **Objective discovery — Invoke Define owns `DISCOVERING → OBJECTIVE_CLOSED`.**
   Context Builder builds the evidence baseline; Interrogation asks only evidence-relevant questions. Exit requires objective, delivery boundary, acceptance obligations, constraints, non-goals, authority/publication class, and unresolved-item ledger. Unknown runtime behavior may be an explicit experiment obligation; it is not falsely “resolved.”

2. **Question and decision closure — Interrogation and Decision Gate own closure, called by Define/Design/Plan.**
   Interrogation owns ambiguity questions and artifact update after each answer. Decision Gate owns consequential choices with 2+ admissible options and returns PASS/BLOCK plus a durable record. No compiler may choose silently.

3. **Owner/dependency closure — Invoke Design owns `OBJECTIVE_CLOSED → DESIGN_CLOSED`.**
   Its immutable scope manifest/denominator and total selection result must bind every concern to accountable, contributing, artifact, and validator owners. Required dependency/interface edges and dispositions must be total. Planned validators remain design evidence, never executed proof.

4. **Executable decomposition — Invoke Plan owns `DESIGN_CLOSED → PLAN_AUTHORED`.**
   Plan authors work pack, layering, graph, task/SWU contracts, exact write scopes, validation, expected receipts, closeout inventory/baselines/delta classes/owner validation/successor policy, and Distill result. Plan never executes or silently mutates Define/Design.

5. **Execution-admission compilation — new compiler owns `PLAN_AUTHORED → MANIFEST_COMPILED`.**
   It consumes exact approved artifacts and emits the normalized manifest below. It performs deterministic normalization and reference closure only. Missing/ambiguous facts are typed blockers routed to their existing owner; the compiler never repairs them.

6. **Immutable readiness proof — Work Pack Readiness Audit owns `MANIFEST_COMPILED → FRONTIER_AUDITED`.**
   Capture exact paths/digests/sizes, normalize the graph, validate commands/writes/attempts/teardown, reconcile live Task Session admission, adversarially test receipt semantics, simulate closeout, and recheck the snapshot. Preserve separate `plan_contract_status` and `runtime_admission_status`.

7. **Human approval — Decision Gate/human owns `FRONTIER_AUDITED → EPOCH_APPROVED`.**
   Approval binds manifest digest, complete source snapshot, frontier, runtime identity policy, risk ceiling, and run budget. Approval cannot repair a failed binding.

8. **Outer frontier run — Task Session Until Blocker owns `EPOCH_APPROVED → RUNNING → COMPLETE|BLOCKED`.**
   It captures the approved finite frontier once and runs one fresh Task Session per SWU. It continues only after execution PASS/FLAG, joined closeout PASS/NO_OP, novel continuity cursor, and one declared dependency-ready successor. Newly discovered work never joins the epoch.

9. **Inner execution — Task Session exclusively owns each `UNIT_READY → UNIT_TERMINAL`.**
   Immediately before the first write it re-reads controlling artifacts and verifies mutation admission. Only `admit + mutationReady=true` crosses the gate. It validates done criteria and reconciles actual outputs with the admitted union.

10. **Closeout — Invoke Refresh exclusively owns admitted bookkeeping mutation.**
    Task Session may authorize only the exact receipt-bound `invoke:refresh:apply-approved` hop over declared targets and allowed delta classes. Refresh cannot execute the next SWU. After the final unit, the outer runner emits terminal chain closeout; Goal/Craft promotion remains separately approval-gated where applicable.

### Normalized Objective-Execution Manifest

```yaml
schemaVersion:
manifestId:
objective:
  statement:
  deliveryBoundary:
  acceptanceObligations: [{id, claim, evidenceRequired, validatorOwner}]
  constraints: []
  nonGoals: []
  authorityClass:
  publicationClass:
sourceClosure:
  refs: [{path, selectors, sha256, size, authorityOwner}]
  defineReceipt:
  designScopeManifest:
  designDenominatorReceipt:
  designSelectionResult:
  planReceipt:
questionClosure:
  questions: [{id, owner, status: resolved|deferred-nonblocking|blocked, artifactRef}]
decisionClosure:
  decisions: [{id, consequence, reversibility, optionsReceipt, decisionRef, status}]
ownership:
  concerns: [{id, accountableOwner, contributingOwners, artifactOwner, validatorOwner}]
  lifecycleOwners: {authoring, compilation, audit, execution, closeout, promotion}
graph:
  units: [{id, parentTask, primaryBehavior, dependencies, successor, closureKind}]
  frontier: []
executionContracts:
  - unitId:
    taskClass:
    argv: []
    cwd:
    environment:
    timeout:
    expectedExit:
    riskClass:
    materialWrites: []
    executionOutputs: []
    allowedWrites: []
    immutablePaths: []
    validation: []
    attemptPolicy: {identity, collision, retention, successTeardown, failureTeardown}
    materialPackageRef:
    dependencyReceipts: []
receiptContracts:
  terminalSchema:
  semanticValidator:
  expectedReceipts: [{unitId, owner, path}]
closeoutContracts:
  - unitId:
    targetInventory: []
    baselines: [{path, sha256}]
    allowedDeltaClasses: []
    ownerValidation: []
    expectedOwnerReceipt:
    successorPolicy:
runtimeBinding:
  taskSessionRequestSchema:
  runtimeIdentityPolicy:
  executionMode:
readiness:
  planContractStatus: pass|flag|block
  runtimeAdmissionStatus: pass|block
  receiptSemanticStatus: pass|block
  frontierStatus: pass|block
  snapshotStatus: pass|block
  verdict: pass|flag|block
  blockers: []
epoch:
  epochId:
  manifestDigest:
  snapshotDigest:
  approvedFrontier: []
  runBudget:
  approvalRef:
  status: draft|compiled|audited|approved|running|complete|invalidated|blocked
invalidation:
  semanticInputs: []
  lastCheckedAt:
  reason:
residue:
  empiricalRuntimeUnknowns: []
  noncritical: []
```

### Invariants

- `materialWrites ∪ executionOutputs = allowedWrites`; material and execution outputs are disjoint.
- Every unit, dependency, successor, owner, receipt destination, validation surface, and closeout target is total and in-scope.
- Every acceptance obligation maps to an artifact/receipt and validator owner.
- No unresolved consequential decision exists at approval.
- One concern/decision has one accountable transition owner; contributors do not gain authority.
- Manifest references are immutable within an epoch; exact-byte semantic inputs are digest-bound.
- Readiness Audit does not select or execute a unit.
- Outer runner never changes Task Session’s one-unit boundary or synthesizes one combined execution receipt.
- Refresh owns closeout mutation only; it does not repair planning or execute product work.
- A complete preflight means “all currently knowable admission contracts close,” never “runtime success is guaranteed.”

### Typed blockers and routing

- `OBJECTIVE_AMBIGUITY` → Invoke Define + Interrogation.
- `CONSEQUENTIAL_DECISION_OPEN` / `APPROVAL_MISSING` → Decision Gate/human.
- `OWNER_UNRESOLVED`, `DEPENDENCY_INTERFACE_UNRESOLVED`, `DESIGN_DENOMINATOR_DRIFT` → Invoke Design.
- `PLAN_DETAIL_MISSING`, `SWU_NONATOMIC`, `VALIDATION_CONTRACT_MISSING`, `CLOSEOUT_CONTRACT_MISSING` → Invoke Plan.
- `REFERENCE_MISSING`, `SCHEMA_UNSUPPORTED`, `GRAPH_INVALID`, `COMMAND_CONTRACT_INVALID`, `WRITE_PARTITION_INVALID`, `RECEIPT_SEMANTICS_INVALID` → compiler finding routed to the artifact/schema owner.
- `MATERIAL_PACKAGE_MISSING_OR_STALE`, `DEPENDENCY_RECEIPT_MISMATCH`, `RUNTIME_MODE_FALSE` → runtime-admission owner/material producer.
- `SNAPSHOT_DRIFT` or any semantic-input digest change → invalidate epoch and return to the earliest owning stage.
- `SUCCESSOR_AMBIGUOUS`, `CURSOR_REPEAT`, `FRONTIER_EXPANSION`, `CLOSEOUT_JOIN_FAILED` → outer runner stops; owner-specific repair follows.
- `EMPIRICAL_VALIDATION_FAILURE`, `TOOL_UNAVAILABLE`, `ENVIRONMENT_FAILURE`, `IMPLEMENTATION_DEFECT` → Task Session terminal BLOCK/residue. These are runtime facts, not proof that planning was incomplete unless the required precondition was knowable and omitted.

Readiness verdicts: `pass` only when all critical dimensions pass; `flag` only for named residue incapable of falsifying admission; `block` for any critical closure failure. `approved` is a later human transition, not an alias for `pass`.

### Semantic invalidation

Invalidate the epoch when any bound semantic input changes: objective/acceptance claim, selected design concern or disposition, accountable owner, dependency/successor edge, unit boundary, write partition, validation/receipt semantics, closeout target/baseline/delta policy, runtime identity/admission schema, authority/publication class, or approved frontier/budget. Observability-only metadata, timestamps, or regenerated views with provably identical canonical semantic digest do not invalidate. Canonical semantic digest—not path mtime or projection-only bytes—owns this distinction.

### Candidate comparison

| Candidate | Verdict | Reason |
|---|---|---|
| Harden Invoke Plan | partial, not sufficient | Plan should strengthen required fields and emit compiler-ready inputs, but making it reconcile live runtime schemas, freeze epochs, and simulate receipts collapses authoring into admission/audit. |
| Add pre-Plan closure stage | reject as a new stage | Define/Design plus Interrogation/Decision Gate already own objective, question, decision, owner, and dependency closure. Improve their exit gates; do not duplicate them. |
| Separate execution-admission compiler/materializer | recommend | It closes the genuine missing boundary: deterministic normalization of authored artifacts into the exact input consumed by the existing readiness audit and outer runner. It has no product or execution authority. |
| Keep generic Refresh repair | reject as normal path | Refresh is evidence-to-artifact synchronization. Using it to discover missing admission contracts after routing preserves late detection and bounce; retain it for genuine drift and receipt-backed closeout only. |

### Migration boundaries

1. Define a public, project-agnostic manifest schema and semantic-digest rules; do not move private DomainSpec vocabulary into Arcanum.
2. Extend existing Invoke stage exit validators to emit typed closure receipts, without adding execution authority.
3. Add compiler/materializer as a bounded capability that consumes but never edits source artifacts.
4. Adapt Work Pack Readiness Audit config generation to consume the manifest; retain its read-only verdict and separate plan/runtime statuses.
5. Bind Task Session Until Blocker to an approved epoch manifest and captured frontier.
6. Keep Task Session admission and Refresh closeout contracts unchanged except for consuming manifest handles rather than reconstructing missing facts.
7. Add observability for first-knowable stage, first-detected stage, owner return, epoch invalidation, and completed units; do not call telemetry authority.
8. Validate by fixtures and one bounded Body War replay before registry/promotion claims. Do not activate deferred `invoke validate` by implication.

### Fixtures

Positive fixture `P1-linear-two-swu`:

- Closed Define/Design decisions and owners.
- Two-unit acyclic graph, unique root, exact argv/cwd/runtime, disjoint write partitions, complete receipts and closeout contracts.
- Audit PASS; human approves epoch E1.
- Outer runner invokes two fresh Task Sessions; each admission/validation/closeout passes; unique successor then none.
- Expected: `COMPLETE`, zero generic Refresh repair returns, two inner receipts, two closeout receipts/NO_OP proofs, unchanged semantic digest.

Single-fault negatives:

- `N1-open-decision`: one consequential decision unresolved → block before compilation; owner Decision Gate.
- `N2-owner-gap`: validator owner absent → Design block.
- `N3-missing-closeout-baseline`: one SWU lacks target baseline → Plan/compiler block before Task Session.
- `N4-write-union-mismatch`: undeclared execution output → readiness block.
- `N5-stale-material`: package digest differs → Task Session admission block before write.
- `N6-receipt-semantic-pass-not-run`: schema-valid receipt says pass with validation not run → readiness/closeout block.
- `N7-snapshot-drift`: source changes after audit → epoch invalidated; no run.
- `N8-ambiguous-successor`: two ready successors after unit receipt → outer runner block without selecting.
- `N9-runtime-command-failure`: all admission gates pass, command fails empirically → Task Session BLOCK; preserve evidence, do not claim preflight failure.
- `N10-frontier-expansion`: newly discovered SWU during E1 → stop or finish only captured frontier according to terminal result; new unit requires E2.
- `N11-projection-only-regeneration`: generated view changes but canonical semantic digest is identical → no invalidation; receipt proves equivalence.
- `N12-semantic-owner-change`: accountable owner changes with otherwise similar bytes → invalidate E1.

Body War acceptance witness: the missing SWU-001 material package/target inventory/baselines/allowed deltas/owner receipt/successor policy must fail `PLAN_AUTHORED → MANIFEST_COMPILED` or readiness audit, before any Task Session mutation route. If it first appears inside Task Session, the protocol has merely renamed the bounce and fails non-vacuity.

STARTED_AT: 2026-07-30T17:04:00Z

FINISHED_AT: 2026-07-30T17:09:00Z
