# Arcanum Building System Research — Verbatim Explorer Returns

The following sections are the unedited native explorer returns for dispatch
`2026-08-05-arcanum-building-system-research`. Synthesis and reviewer text is
excluded by contract.

## Agent 1 — Hewitt, Carl — runtime and failure archaeology

FULL_EXPLORER_RETURN

Scope and identity
- Parent repository observed at commit `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`; `arcanum` submodule observed at `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295` on `heads/codex/intent-route-resolver-addon`, with a materially dirty working tree. Evidence scope was strictly the frozen dispatch inputs plus `arcanum/{arcana/task-session,arcana/continuation-router,spells/task-session-until-blocker,spells/work-pack-readiness-audit,spells/implementation-readiness,runtime/orchestrate}`, generated `.agents/skills/` mirrors, scoped git history/diffs, tests, schemas, and receipts. No repository file was intentionally edited.
- Proof labels: OBSERVED means current bytes/history inspected; EXECUTED means a bounded test was run this turn; UNVERIFIED means prose/fixture/receipt exists but no real owner/product mutation or production route was rerun.

Recent chronology: committed vs live vs generated
1. COMMITTED/OBSERVED (July 30, submodule HEAD): the runtime foundation is a sequence of commits: `7ed9c113` deterministic Task Session governance execution; `8133179` validated until-blocker chain; `952fa42` immutable WP readiness audit; `10d2e19` bounded executor join; `b0090ee` deterministic reconciliation; `d2a7d0c` crash-safe commit resume; `07b01c9` deterministic owner-hook protocol. This is the last immutable source identity; it does not contain the Aug 4-5 route closure.
2. LIVE-UNCOMMITTED/OBSERVED: current diff is ~2,585 insertions/166 deletions over 24 tracked scoped files plus many untracked schemas/scripts/tests. Major additions: Plan Semantic Manifest and selection (`spells/work-pack-readiness-audit/scripts/plan_semantics.py`, `verify_plan_selection.py`); fast entry and plan-once consumption (`arcana/task-session/scripts/fast_execution_entry_guard.py`, `verify-mutation-readiness.py`, governance runner); typed prerequisite and Work-Pack continuation route (`arcana/continuation-router/scripts/`, schemas); fresh-session resumption (`spells/task-session-until-blocker/scripts/fresh_session_resume.py`); and outer loop (`spells/implementation-readiness/scripts/{execution_contracts,execution_loop,readiness_execution}.py`). These are live candidate bytes, not committed or promoted.
3. GENERATED/OBSERVED DRIFT: generated `.agents/skills/work-pack-readiness-audit` is stale relative to canonical live source. Exact hashes differ: canonical/generated `plan_semantics.py` = `4a5ce7...` / `a013a9...`; `verify_plan_selection.py` = `6312ca...` / `2ab2b4...`; `audit_work_pack.py` = `443660...` / `c3a449...`. Direct diff shows generated `plan_semantics.py` lacks `validate_execution_policy`, `execution_policy` in semantic components, allowed-route digest, execution-policy digest, and per-unit routes (canonical selectors lines 151-186, 189-201, 273 onward); generated `verify_plan_selection.py` lacks execution-intent-binding support and selection intent digest (canonical lines 228-242). Generated Task Session and Continuation Router SKILL bytes also differ substantively from canonical live docs. Therefore canonical-live tests do not establish generated-runtime parity.

Runtime action/gate timeline (current live design; OBSERVED, tests below EXECUTED)
1. Audit/plan epoch: normalize declared JSON-pointer semantic values; reject floats, unresolved pointers, duplicate binding IDs, route path escapes, unknown frontier routes, allowed-route digest mismatch, and overlap of automatic/stop decisions (`spells/work-pack-readiness-audit/scripts/plan_semantics.py:25-79,92-148,151-186,189-280`). Manifest remains `authority_effect:none`, `mutation_ready:false`, no selected unit (`verify_plan_selection.py:141-149`).
2. Select exactly one task+SWU from audited bindings; recompute semantic epoch/component/unit digests; verify dependency and lifecycle evidence exact refs; accept explicit confirmation or current execution intent; return `SELECTION_READY` but still non-authoritative (`verify_plan_selection.py:151-251`).
3. Implementation-readiness compiles policy/entry/binding and drives a finite outer loop. `selection-ready` chooses the next captured-frontier unit; unknown route/blocked state/budget/stop decision blocks; completion is `FRONTIER_COMPLETE` (`implementation-readiness/scripts/execution_loop.py:303-373`).
4. Before Context Builder, fast guard reads exactly four logical inputs (work pack, selected unit, execution binding, entry projection), validates binding/frontier, and returns proceed, route-owner, or block with zero mutation and zero owner dispatch (`task-session/scripts/fast_execution_entry_guard.py:63-75,97-164,167-207`; contract `task-session/SKILL.md:150-169`).
5. If owner prerequisite, Continuation Router admits only the exact current Work-Pack route and owner; Task Session does not impersonate owner. If task-ready, Task Session proceeds. The outer loop correlates every join by action, route fingerprint, selected unit, receipt, and session (`execution_loop.py:491-555,640-679`).
6. Plan-once mutation admission independently re-reads exact manifest/selection schema+artifacts, enforces authority ceiling and epoch/unit/receipt identities, matches target-baseline inventory to material writes, rehashes live targets, validates structured validation digest and package/receipt binding (`task-session/scripts/verify-mutation-readiness.py:347-470`). Only then may the governance runner atomically consume admission and enter run writes.
7. After a prerequisite owner pass, fresh resume reclassifies current entry, rejects unchanged/repeated fingerprints and used receipt slots, creates a distinct deterministic session+cursor, and exclusively writes one admission event (`task-session-until-blocker/scripts/fresh_session_resume.py:420-512,515-592`). This is deliberately a fresh Task Session, not recursive same-session execution.
8. Joined task receipts advance visited frontier; one-unit or exhausted frontier completes; otherwise a new entry/session is required (`execution_loop.py:645-679`). Critical validation, protected effects, product decisions, and scope expansion stop the loop.
9. Orchestrate native lifecycle remains separately ordered: action_attempted -> host result -> wait registration -> wait_attempted -> terminal -> close -> receipt join; timeout requires prior wait then one interrupt (`runtime/orchestrate/scripts/validate_run_evidence.py:128-183,185-258`).

First-knowable / first-detected matrix
- Semantic plan drift: knowable at selection recomputation; detected there as `PLAN_EPOCH_STALE` / component/unit change (`verify_plan_selection.py:165-183`). Forbidden effects: selection/admission/mutation. Current proof EXECUTED.
- Invalid/escaping/overlapping Work-Pack route policy: knowable while semantic manifest is built; detected by canonical normalizer (`plan_semantics.py:151-186`). Generated runtime currently cannot detect these at that gate because of drift. Canonical proof EXECUTED indirectly in selection/integration tests; generated proof BLOCKED by parity.
- Ambiguous selected task/SWU: knowable at selection; detected `SELECTED_UNIT_NOT_UNIQUE` (`verify_plan_selection.py:151-163`). Mutation remains false. OBSERVED; fixture/test family present.
- Stale binding/frontier/entry: knowable at fast guard; detected before Context Builder (`fast_execution_entry_guard.py:167-207`). Context/deep material/admission/mutation/owner dispatch remain unentered. EXECUTED.
- Live target changed after selection: knowable only at mutation admission rehash; detected before mutation (`verify-mutation-readiness.py:428-446`). EXECUTED.
- Missing/unknown owner route or expanded scope/effect/input: knowable at Work-Pack route admission/outer-loop action decision; detected before dispatch (`continuation-router/scripts/work_pack_route.py:158+`; `execution_loop.py:371-423`). EXECUTED via integration cases 11-12.
- Repeated owner/session fingerprint: knowable at fresh-resume preparation; detected before durable admission (`fresh_session_resume.py:429-442,493-503`). EXECUTED.
- Missing/mismatched joined event: knowable at join; detected by phase/action/fingerprint/receipt correlation (`execution_loop.py:491-528`). EXECUTED in integration suite.
- Orchestrate partial-wave timeout: knowable after bounded wait expires; detected only after registration+wait, then interrupt; dependent gates stay closed (`validate_run_evidence.py:224-258`). EXECUTED.
- Closeout synchronization impossibility: knowable before mutation via Task Session closeout preflight; current contract requires target inventory, baselines, source/owner receipt contracts and owner validations (`task-session/SKILL.md:229-240`). Runtime implementation was not independently exercised in this lane: OBSERVED/UNVERIFIED end-to-end.

Finite traces
Normal plan-once path (canonical-live; EXECUTED): audited plan -> semantic manifest (no authority) -> exact unit selection `SELECTION_READY` -> policy/entry/binding -> fast guard four reads/one phase returns task-ready -> Context Builder path -> mutation admission revalidates manifest/selection and live baselines -> governance runner consumes single-use admission -> one fresh Task Session -> joined terminal receipt -> visited frontier -> `FRONTIER_COMPLETE`. Witnesses: plan selection 6 tests, plan end-to-end 1, fast guard suite, admission 3, governance 7, implementation-readiness integration 14.
Failure A, stale semantic plan (EXECUTED): change semantic command/unit contract after manifest -> selection recomputes digest -> first stop `PLAN_EPOCH_STALE`/component or unit change -> exact refresh entry is emitted; no selection authority, Context Builder, admission, or mutation. Witness `test_semantic_drift_emits_exact_refresh_entry` and integration `test_02_semantic_drift_routes_refresh_rejoins_and_starts_task` (the latter shows one owner repair/rejoin before task).
Failure B, target drift/replay (EXECUTED): valid selection then target bytes change or attempt/package reused -> mutation admission rehash/single-use checks fail -> stop before governance run writes and mutation. Witness admission tests `test_live_target_change_blocks_before_mutation`, `test_cross_attempt_package_reuse_blocks`, governance tests for stale request/receipt and atomic second-run rejection.
Failure C, owner prerequisite residue (EXECUTED): entry route-owner -> owner joins pass but reclassification still returns same owner fingerprint -> `UNCHANGED_PREREQUISITE_FINGERPRINT`; or owner receipt non-pass -> `OWNER_PREREQUISITE_BLOCKED`; or session/cursor repeated -> replay codes. No fresh admission event/task session. Witness fresh-resume 5-test suite and integration test 13.
Failure D, protected/critical runtime effects (EXECUTED): product/semantic choice, scope expansion, destructive/external/authority effect, or failed critical validation -> outer loop stop before effect/follow-on effect. Witness integration tests 5-8.
Failure E, native helper timeout (EXECUTED): spawn return -> register -> wait -> timeout -> interrupt -> timed_out receipt; no dependent gate. Native-join 6 tests and partial-wave 3 tests passed.

Current tests and receipts
- Executed now with `PYTHONDONTWRITEBYTECODE=1`: plan-once selection 6/6; plan-once end-to-end 1/1; fast execution guard PASS (4 reads, 1 phase, 0 prompts, 0 mutations); plan admission 3/3; plan governance 7/7; fresh-session resume 5/5; work-pack execution integration 14/14 (`INTEGRATION_CASE_COUNT=14`, 4 entry states, 4 automatic decision classes, 8 stop decisions, 0 prompts); native join 6/6; partial-wave recovery 3/3.
- Present/OBSERVED but not equivalent to production: `spells/implementation-readiness/development/integration/work-pack-execution-observability.json` records plan-once 1 route hop/1 selection join/0 owner joins/0 pre-execution refresh; drift repair 2 hops/1 owner; declared owner retry 3 hops/2 owners. The invoke-run under `spells/implementation-readiness/development/invoke-runs/20260804T184514Z-work-pack-execution-grant/` contains eight SWU receipts and prototype closeout artifacts, but those are candidate development evidence, not promotion or deployment.

Parity/drift, defects, residue
1. REPRODUCIBLE DEFECT/BLOCKER: generated Codex WPRA is stale and omits route-policy semantic binding and execution-intent selection fields. Reproduce with the `diff -u` pairs above or hashes. Consequence: invoking generated WPRA can validate a weaker/older contract than canonical live code; current generated parity is BLOCK even though canonical tests pass.
2. Generated Task Session/Continuation Router SKILL docs also differ from canonical live contracts; some scripts/schemas exist in generated mirrors, but byte parity and package-wide validation were not established. Treat generated-runtime behavior as UNVERIFIED.
3. All Aug 4-5 capability closure is dirty/uncommitted at submodule HEAD, so immutable identity covers only the July 30 foundation. Live test success is not commit, publication, promotion, or release proof.
4. The fresh-session owner intentionally writes an admission event (`fresh_session_resume.py:515-592`) when invoked normally; tests use temporary repositories. This explorer did not invoke it against repository state.
5. Closeout-sync preflight is specified in Task Session, and until-blocker validates owner/router/no-op closeout joins, but a single current end-to-end test from product mutation through actual owner synchronization was not rerun here. Residue remains UNVERIFIED.
6. Orchestrate tests prove event-contract validation, not an actual host timeout/interrupt in this run.

ACTION_RECEIPT
action_id: spawn-0001
dispatch_id: 2026-08-05-arcanum-building-system-research
run_id: arcanum-building-system-research-run-01
wave_id: explorers
step_id: s1-explore
role: explorer-runtime
capability_ref: research
status: pass
artifacts: [] (self-contained explorer return only; parent-owned `receipts/explorer-runtime.json` was not written)
validation: pass (canonical-live scoped suites listed above); generated parity: block
blockers: [generated-work-pack-readiness-audit-stale, august-4-5-runtime-closure-uncommitted, closeout-sync-real-owner-e2e-unverified]

## Agent 2 — van Lamsweerde, Axel — formal owner and gate contract

FULL_EXPLORER_RETURN

## 1. Repository and evidence identity

- Parent repository: `/home/vrondelli/projects/domainspec-core`
- Parent HEAD: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`
- Arcanum submodule: `/home/vrondelli/projects/domainspec-core/arcanum`
- Arcanum HEAD: `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`
- Dispatch: `2026-08-05-arcanum-building-system-research`
- Run: `arcanum-building-system-research-run-01`
- Frozen target: `ops/development/2026-08-05-arcanum-building-system-research/dispatch-sheet.json#explorers-agent-1`
- Inventory lead: `ops/development/2026-08-05-arcanum-building-system-research/strategy-inventory-packet.json`
- Evidence scope: direct current canonical Arcanum contracts and current Git state. Inventory entries were used only to choose questions and sources.
- Proof status:
  - Contract rows below: `observed`, not executed.
  - Runtime behavior: `unverified` unless explicitly described as a contract requirement.
  - No validator or fixture suite was executed in this action.
  - No file was written.
- Live-uncommitted sources in this return:
  - `arcanum/spells/invoke/plan.md`
  - `arcanum/spells/work-pack-readiness-audit/README.md`
  - `arcanum/spells/implementation-readiness/README.md`
  - `arcanum/arcana/task-session/SKILL.md`
  - related Task Session schemas/scripts and Invoke material-package contracts shown by `git -C arcanum status --short`
- Clean-at-current-Arcanum-HEAD sources used:
  - `arcanum/spells/invoke/define.md`
  - `arcanum/spells/invoke/design.md`
  - `arcanum/spells/invoke/handoff.md`
  - `arcanum/spells/invoke/refresh.md`
  - `arcanum/transmutations/context-builder/SKILL.md`
  - `arcanum/arcana/decision-gate/SKILL.md`
  - `arcanum/arcana/distill/SKILL.md`
  - `arcanum/transmutations/implementation-layering/SKILL.md`

## 2. Owner and integration matrix

| Stage/capability | Entry and authored artifact | Owner and mutation authority | Evidence ceiling | Legal next route | Direct evidence |
|---|---|---|---|---|---|
| Invoke Define | Goal, constraints, existing artifacts → spec, glossary, optional layering seed/gap, transport | Invoke authors definition artifacts; spellcraft/sigil-development retain lifecycle mutation | Definition completeness only; Distill result does not establish plan readiness | Design, clarification/split, or lifecycle-owner handoff | `arcanum/spells/invoke/define.md:11-18`, `:45-54`, `:56-68`, `:105-109` — observed, clean |
| Invoke Design | Approved Define evidence plus closed manifest, denominator receipt, authored concerns → six design views and selection result | Invoke Design authors design contracts; extractor and validator independently check them | `authored-complete` or `design-validator-pass`; Plan evidence is explicitly separate | Normal Plan only after validator pass; bounded remediation Plan otherwise | `arcanum/spells/invoke/design.md:22-31`, `:104-140`, `:146-156`, `:160-182`, `:230-257` — observed, clean |
| Context Builder | Exact task obligations and selector-level sources → compact pack; strict runtime mode emits Markdown plus JSON/index | Selects evidence; does not own plan, task readiness, or source truth | Session execution evidence; persisted packs are not canonical planning documents | Caller resumes only with complete strict coverage | `arcanum/transmutations/context-builder/SKILL.md:15-19`, `:27-49`, `:54-71`, `:77-86` — observed, clean |
| Implementation Layering | Approved design/planning intent → global L0-L3 layer map | Planning companion; does not execute or promote | Layer decisions and validation/promotion criteria, not execution proof | Invoke Plan recomposes work pack and waves | `arcanum/spells/invoke/plan.md:13-23`, `:333-342`, `:344-377`; `arcanum/transmutations/implementation-layering/SKILL.md:54-84` — plan live-uncommitted |
| Distill | Draft model/design/plan plus evidence → coherent-unit selection, recomposition proof, gaps, verdict | Distill owns its analysis and telemetry row, not downstream lifecycle authority | `pass|flag|block`; telemetry cannot change verdict or authorize mutation | Caller’s lifecycle route, subject to caller gates | `arcanum/arcana/distill/SKILL.md:15-16`, `:99-137`, `:203-215`, `:241-257`, `:265-285` — observed, clean |
| Invoke Plan | Approved Design plus source refs → implementation layering, plan, work pack, SWUs, execution/closeout contracts | Invoke authors the executable contract but does not execute source changes | Plan completeness and mutation-handoff eligibility; not selection, admission, or execution | WPRA/readiness, Task Session, or lifecycle owner | `arcanum/spells/invoke/plan.md:13-32`, `:333-342`, `:344-397` — observed, live-uncommitted |
| WPRA | Frozen plan/work-pack/contracts → audit reports; v2 plan-once emits semantic manifest and selection handoff | Audit owner only; explicitly no mutation, selection, approval, or authority effect | `frozen-input-contractual-readiness`; plan-once pass means ready for selection, not mutation | Task Session selection or Invoke Refresh | `arcanum/spells/work-pack-readiness-audit/README.md:198-221`, `:245-265`, `:280-313`, `:315-342` — observed, live-uncommitted |
| Decision Gate | Consequential multi-option blocker → admissibility and decision/override receipts | Human/typed owner gates control protected hazards; generic gate cannot bypass lifecycle owner | Exact decision/one-use override only | Resume caller or route to protected owner | `arcanum/arcana/decision-gate/SKILL.md:52-76`, `:85-101`, `:123-154`, `:175-206` — observed, clean |
| Implementation Readiness outer loop | Exact Work Pack, semantic digest, allowed-route digest, frontier, mode, budget → owner/Task Session joins | Coordinates; does not perform owner mutation or weaken admission | Bound progression state and correlated receipts, not unit completion by inference | Owner prerequisite, fresh Task Session, complete, or block | `arcanum/spells/implementation-readiness/README.md:15-24`, `:33-40`, `:52-84`, `:99-130`, `:137-139` — observed, live-uncommitted |
| Task Session | One exact task/SWU → execution result, terminal receipt, synchronized evidence | Owns bounded execution; does not impersonate producer, Refresh, or lifecycle owners | Execution and validation for one unit; admission receipt is not lifecycle/promotion/publication authority | Required closeout owner hop, then optional one-hop continuation | `arcanum/arcana/task-session/SKILL.md:15-28`, `:148-199`, `:223-250`, `:260-319`, `:321-350`, `:351-420` — observed, live-uncommitted |
| Invoke Refresh | Source evidence plus exact target inventory and mode → proposal or scoped applied synchronization | Invoke Refresh owns updates to Invoke-authored artifacts; apply needs exact package/receipt/approval binding | Refresh artifact completeness and applied validation only; phase pass alone grants no apply authority | Task Session/follow-up or no-op | `arcanum/spells/invoke/refresh.md:11-34`, `:104-126`, `:185-255`, `:317-325` — observed, clean |
| Invoke Handoff | Referenced session plus handoff type → session-evidence handoff | Packages context only; target owner performs work | Coverage of the handoff packet, not execution or lifecycle completion | Task Session, research, reflection, or named lifecycle owner | `arcanum/spells/invoke/handoff.md:23-46`, `:82-122`, `:149-177` — observed, clean |

## 3. Gate and receipt matrix

| Gate | Required proof | Receipt/artifact | Fail-closed result | Evidence |
|---|---|---|---|---|
| Define scope | Core goal, consistent scope, approved intent, template evidence | Define transport and Invoke Result | Missing/contradictory goal or unresolved ambiguity blocks | `invoke/define.md:45-68` — observed |
| Design activation | Approved Define refs, exact target, closed scope manifest, owner approval | `DesignScopeManifest` | Missing approval/reference/manifest blocks | `invoke/design.md:22-31` — observed |
| Design denominator | In-root readable selectors, current digests, independently detected denominator | `DesignDenominatorReceipt` | Missing, stale, self-issued, or unbound evidence blocks | `invoke/design.md:104-127`, `:151-152` — observed |
| Design fixed point | Total signal-to-concern binding, exact owners, legal disposition, unchanged second pass | `DesignSelectionResult` | `CHANGED_PASS_TWO`, unresolved owner, illegal selection, or stale receipt blocks | `invoke/design.md:109-140`, `:164-173` — observed |
| Plan admission | Approved Design, layering, work pack, validation strategy, Distill | Plan transport, layering, Work Pack, Distill validation | Missing Design/companion/critical gap/Distill block prevents mutation route | `invoke/plan.md:333-377` — observed, live-uncommitted |
| SWU selection | Unique SWU with parent, dependencies, scope, acceptance, command, closeout contract | Work Pack SWU row/manifest | Unknown, duplicate, ambiguous, task-shaped, or incomplete SWU blocks | `invoke/plan.md:344-370` — observed, live-uncommitted |
| WPRA semantic audit | Frozen selector bindings and contract graph | Plan Semantic Manifest plus selection handoff | Any non-observability gap blocks | `work-pack-readiness-audit/README.md:280-313`, `:315-335` — observed, live-uncommitted |
| Plan-once selection | Manifest still resolves, exact membership, dependency receipts, lifecycle eligibility, explicit confirmation | Non-authoritative selection receipt | Semantic/normalizer drift blocks and routes Refresh plus re-audit | `work-pack-readiness-audit/README.md:337-342` — observed, live-uncommitted |
| Fast-entry guard | Policy, selected unit, execution binding, execution-entry projection | Fast-entry request and receipt | Anything except `task-ready` or precisely returned owner prerequisite stops before Context Builder/run-state write | `task-session/SKILL.md:150-169` — observed, live-uncommitted |
| Owner prerequisite | Selected Work Pack/unit, prerequisite, satisfaction receipt, separately traced control evidence | Prerequisite classification plus separate owner receipt/control handle | Unmet unauthorized, stale/tampered, drifted, expanded, unsatisfied, replayed, or unjoined blocks | `task-session/SKILL.md:171-192` — observed, live-uncommitted |
| Context coverage | Task contract, source/design refs, dependencies, blockers, scope, done criteria, validation | Context pack; strict mode Markdown and JSON/index | Missing, stale, contradictory, unsafe, or incomplete coverage blocks before mutation | `task-session/SKILL.md:194-199`; `context-builder/SKILL.md:32-49` — observed |
| Decision | Admissible options and explicit resolution | Admissibility and decision/override receipts | Unresolved consequential blocker blocks | `decision-gate/SKILL.md:52-101`, `:123-154` — observed |
| Closeout preflight | Inventory, live baselines, source-receipt contract, owner validation, owner-receipt contract, delta classes, successor policy | Preflight result | Missing/ambiguous/stale/expanded/forbidden input blocks before implementation writes | `task-session/SKILL.md:229-240` — observed, live-uncommitted |
| Mutation admission | Bound task/SWU, controllers, dependency frontier, disjoint write partitions, validations, owner/authority/publication, producer tuple when material-bound | Mutation-admission receipt | Missing/stale/mismatched/expanded/unclassified input blocks before mutation | `task-session/SKILL.md:260-303` — observed, live-uncommitted |
| Plan-once single use | Manifest, selection receipt, package/producer chain, attempt-bound token and ledger | Admission receipt, consumption ledger, execution ticket, terminal receipt | Reuse or pre-joined output blocks | `task-session/SKILL.md:304-319` — observed, live-uncommitted |
| Completion | All acceptance-critical criteria and outputs reconcile with admitted paths | Terminal Task Session receipt | Failed/unrun critical check or undeclared/missing output blocks | `task-session/SKILL.md:328-350` — observed, live-uncommitted |
| Closeout sync | Terminal receipt, typed deltas, current baselines, exact Refresh route and owner receipt | `CloseoutSync`, separate joined Refresh receipt, continuity cursor | Drift, ambiguous successor, failed owner validation, cycle, or unjoined receipt makes Task Session block | `task-session/SKILL.md:351-420` — observed, live-uncommitted |
| Refresh apply | Source evidence, inventory, scoped approval, valid material package/receipt, validation commands | Material-package receipt and Refresh report | Invalid/stale/mismatched package or missing approval blocks apply | `invoke/refresh.md:185-243`, `:317-325` — observed |

## 4. Ordinary-feature happy path

Finite contract trace; observed in prose, not executed:

1. Invoke Define receives the feature goal, establishes approved intent, chooses a template with eligibility evidence, authors spec/glossary, and records Distill `pass` or justified `not required` (`invoke/define.md:45-68`).
2. Invoke Design requires approved Define evidence and closed `DesignScopeManifest`; independent extraction emits a current `DesignDenominatorReceipt`; selection validation reaches an unchanged two-pass fixed point and emits `DesignSelectionResult` with `design-validator-pass` (`invoke/design.md:104-156`).
3. Invoke Plan consumes those exact Design refs, authors the global implementation-layering artifact, Work Pack, validation strategy, task/SWU contracts, execution handoff, and complete closeout-sync contract; automatic Distill passes (`invoke/plan.md:333-397`).
4. WPRA freezes the inputs and reports contractual readiness without selecting or authorizing mutation (`work-pack-readiness-audit/README.md:198-210`, `:245-265`).
5. Task Session selects one unique ready SWU, builds the bounded Context Builder pack, resolves any actual blocker through Decision Gate, and passes closeout preflight (`task-session/SKILL.md:194-240`).
6. Immediately before mutation, Task Session verifies mutation admission. For material work, the package and producer receipt bind exactly to material writes; execution outputs are disjoint and their union equals allowed writes (`task-session/SKILL.md:260-303`).
7. Task Session executes only that SWU, runs every acceptance-critical validation, reconciles outputs, and emits its terminal receipt (`task-session/SKILL.md:321-350`).
8. It constructs `CloseoutSync`, derives the narrow bookkeeping-only authorization, routes exactly one `invoke:refresh:apply-approved` hop through Continuation Router, joins a separate validated Refresh receipt, and returns the synchronized next route without executing the successor (`task-session/SKILL.md:351-400`).

Evidence ceiling: this is the prescribed legal sequence, not proof that an end-to-end runtime currently completes it.

## 5. Plan-once happy path

Finite contract trace; observed in live-uncommitted contracts, not executed:

1. Invoke Plan authors complete unit contracts, structured validation contracts, semantic selectors, ownership and closeout contracts.
2. WPRA uses `admission_timing: selected-unit-at-task-session`, resolves and hashes normalized semantic selectors and unit contracts, excludes future material bytes and mutable lifecycle/closeout receipts, and emits `plan-semantic-manifest.json` plus `selection-handoff.json` (`work-pack-readiness-audit/README.md:315-335`).
3. WPRA pass leaves `selected_unit:null`, `mutation_ready:false`, `authority_effect:none`; next owner is Task Session selection (`:205-210`, `:296-304`).
4. Selection re-resolves current semantics, verifies exact task/SWU membership, dependency receipts, lifecycle eligibility, and explicit confirmation, then emits a non-authoritative selection receipt (`:337-342`).
5. The fast-entry guard binds policy, selected unit, execution binding, and entry projection; `task-ready` is persisted and revalidated by the governance runner (`task-session/SKILL.md:150-169`).
6. Task Session requires the exact semantic manifest and selection receipt and binds plan epoch, unit digest, attempt, validation digest, baselines, lifecycle owner, authority, and publication across package, producer receipt, request, and admission receipt (`task-session/SKILL.md:304-313`).
7. Immediately before launch it atomically consumes the attempt-bound admission token, carries the chain into the execution ticket, and requires the terminal receipt to record token, attempt, consumed receipt, and ledger (`:314-319`).
8. Execution, validation, terminal receipt, and required Refresh closeout proceed as in the ordinary path.

## 6. Required blocked traces

### A. Missing Design evidence

- First knowable gate: Invoke Design activation/denominator.
- Inputs: Plan request with absent approved Define/Design refs, or only authored Design without passing denominator/selection receipts.
- Ordered stop:
  1. Plan checks approved Design outputs and source refs.
  2. Missing evidence blocks before layering, Work Pack handoff, or mutation-capable route.
- Expected diagnostic artifact: blocked Invoke Plan result naming missing Design evidence; if only validator infrastructure is missing, Design may route solely to bounded remediation Plan.
- Forbidden effects: no Work Pack treated as execution-ready; no Task Session admission or mutation.
- Evidence: `invoke/design.md:131-140`, `:164-173`; `invoke/plan.md:344-346`.
- Status: observed, Plan portion live-uncommitted.

### B. Missing Distill evidence

- First knowable gate: Invoke Plan’s mandatory Distill phase.
- Inputs: otherwise complete draft plan/layering/work pack without recorded Distill verdict/recomposition proof.
- Ordered stop:
  1. Plan produces draft artifacts.
  2. Mandatory Distill validation is absent or returns block.
  3. Mutation-capable handoff is forbidden.
- Expected artifact: Distill result with `pass|flag|block`, recomposition status, named gaps/owners.
- Forbidden effects: Task Session/runtime-goal handoff on a Distill block.
- Evidence: `invoke/plan.md:339-342`, `:360-361`, `:379-397`.
- Status: observed, live-uncommitted.

### C. Ambiguous SWU

- First knowable gate: Plan decomposition, or Task Session Step 1 if ambiguity survives.
- Inputs: task with several independently verifiable SWUs and no selected unique SWU, duplicate/unknown IDs, or task-shaped SWU.
- Ordered stop:
  1. Plan checks atomicity, independent acceptance, split analysis, and narrow first unit.
  2. Ambiguous/incomplete selection blocks mutation handoff.
  3. Task Session must not infer a unit from convenience.
- Expected artifact: blocker/gap ledger or Task Session blocked resolution receipt.
- Forbidden effects: Context Builder/mutation for a guessed unit.
- Evidence: `invoke/plan.md:344-370`; Task Session’s nearest-unit rules at `task-session/SKILL.md:113-141`.
- Status: observed; Plan and Task Session sources live-uncommitted.

### D. Stale semantic plan

- First knowable gate: plan-once selection re-resolution.
- Inputs: existing Plan Semantic Manifest whose selected semantic value or normalizer output changed.
- Ordered stop:
  1. Selection verifier re-resolves semantic selectors.
  2. Digest mismatch blocks selection.
  3. Route is Invoke Refresh followed by readiness re-audit.
- Expected artifact: blocked selection receipt/diagnostic.
- Forbidden effects: package production, admission, or mutation from stale epoch.
- Evidence: `work-pack-readiness-audit/README.md:337-342`; downstream recheck `task-session/SKILL.md:304-313`.
- Status: observed, live-uncommitted.

### E. Absent material producer/package

- First knowable gate:
  - In plan-once: missing future package is intentionally pending at WPRA and first blocks mutation at Task Session admission.
  - In full-frontier readiness: missing required material blocks WPRA.
- Inputs: material-bound selected SWU without current package, producer receipt, or owner schema.
- Ordered stop:
  1. Task Session derives `material-bound`.
  2. Requires exact package, producer receipt, and producer-owned schema.
  3. Missing or mismatched tuple returns block before mutation.
- Expected artifact: blocked mutation-admission receipt; never fabricated material evidence.
- Forbidden effects: material writes or fallback to execution-output-only.
- Evidence: `work-pack-readiness-audit/README.md:315-335`; `task-session/SKILL.md:270-303`.
- Status: observed, live-uncommitted.

### F. Failed closeout preflight

- First knowable gate: Task Session Step 4, before mutation admission.
- Inputs: SWU missing exact closeout inventory, baseline binding, source-receipt contract, owner validation, expected owner receipt, admitted delta classes, or unique successor.
- Ordered stop:
  1. Preflight resolves all closeout obligations against current baselines.
  2. Missing, stale, expanded, ambiguous, or forbidden input blocks.
  3. No implementation write and no owner dispatch occurs.
- Expected artifact: persisted blocked preflight result bound to Work Pack identity and baselines.
- Forbidden effects: implementation writes, Refresh dispatch, or claiming completion.
- Evidence: `invoke/plan.md:364-367`; `task-session/SKILL.md:229-240`.
- Status: observed, live-uncommitted.

### G. Closeout failure after successful execution

- First detectable gate: Step 8 owner join/receipt validation.
- Inputs: passing terminal execution receipt but target drift, owner validation failure, ambiguous successor, cycle, or unjoined owner.
- Ordered stop:
  1. Preserve successful execution result.
  2. Required synchronization remains incomplete.
  3. Overall Task Session returns block.
- Expected artifacts: terminal execution receipt, `CloseoutSync`, separate failed/missing owner receipt status.
- Forbidden claim: “Task Session complete” or synchronized next route.
- Evidence: `task-session/SKILL.md:353-389`.
- Status: observed, live-uncommitted.

## 7. Contradictions, duplication, and gaps

1. **Canonical packaging ambiguity**
   - `work-pack-readiness-audit` and `implementation-readiness` have canonical public `README.md` contracts but no `SKILL.md` at those source directories, while generated mirrors exist elsewhere.
   - This is not proof of runtime drift, but it creates a source-selection hazard: callers may treat a generated package as canonical.
   - Status: observed; generated parity not validated.

2. **Plan-once readiness wording is carefully split but easy to collapse**
   - WPRA uses “pass” while simultaneously fixing `selected_unit:null`, `mutation_ready:false`, `authority_effect:none`.
   - Any summary saying “WPRA pass admits mutation” contradicts `work-pack-readiness-audit/README.md:205-210` and `:296-304`.

3. **Two selection-related guards are intentionally separate**
   - WPRA selection receipt proves current semantic selection.
   - Task Session fast-entry receipt proves the four-input execution entry and is revalidated by the governance runner.
   - They appear duplicative but check different boundaries. Collapsing them would lose either semantic epoch binding or consumer-entry binding.
   - Evidence: WPRA `:337-342`; Task Session `:150-169`.

4. **Producer versus consumer validation is intentionally duplicated only at the boundary**
   - Invoke owns material-package production/validation.
   - Task Session must consume and bind it but explicitly must not copy the Invoke validator.
   - Evidence: `task-session/SKILL.md:270-290`.
   - Gap: current live changes touch both Invoke material schemas/validator and Task Session admission schemas/scripts; parity and compatibility were not executed here.

5. **Closeout is both a Plan obligation and Task Session runtime gate**
   - Plan must make closeout executable before handoff; Task Session revalidates it pre-mutation and again after execution.
   - This is justified temporal duplication: authored contract, pre-mutation currentness, post-execution currentness.
   - Evidence: `invoke/plan.md:364-367`; `task-session/SKILL.md:229-240`, `:351-389`.

6. **Distill flag boundary needs explicit criticality**
   - Plan states a Distill flag must add named gaps/owners/repair paths, while only a Distill block explicitly prevents mutation-capable routing.
   - The contract does not, in the cited lines, state a standalone mechanical rule proving every flagged gap is non-acceptance-critical before handoff.
   - Task Session later treats acceptance-critical unknowns as blockers, but permitting the handoff may relocate rather than eliminate the ambiguity.
   - Evidence: `invoke/plan.md:360-372`; `task-session/SKILL.md:328-349`.
   - Status: observed contract gap, not runtime defect proof.

7. **Implementation Readiness versus Task Session ownership is separated but operationally dense**
   - Outer loop owns frontier progression and fresh-session orchestration; Task Session owns one selected unit.
   - Owner receipts and Task Session receipts must remain separate; successful prerequisite work cannot be inferred as unit completion.
   - Evidence: `implementation-readiness/README.md:52-112`.
   - Gap: live implementation-readiness schemas/scripts are untracked, so executable proof and generated parity remain unverified.

8. **Refresh phase pass is not mutation readiness**
   - A complete proposal-only Refresh can pass while handoff is gated and `mutation_ready:false`.
   - A schema-valid package also remains insufficient without current approval, exact binding, and ready handoff.
   - Evidence: `invoke/refresh.md:185-255`, `:317-325`.

9. **Handoff artifacts are non-authoritative**
   - Context Builder and Invoke Handoff persist session evidence but neither establishes plan authority, task readiness, or lifecycle completion.
   - Evidence: `context-builder/SKILL.md:32-49`; `invoke/handoff.md:82-122`.

10. **Current-live repair status cannot be promoted**
    - The August 4–5 Plan, WPRA, Implementation Readiness, Task Session, schemas, scripts, and tests are modified or untracked relative to Arcanum HEAD.
    - Their prose currently describes repairs for plan-once selection, producer/admission binding, pre-execution owner prerequisites, fast entry, outer-loop control, and closeout preflight.
    - Without executing fixtures and parity checks, these are live-uncommitted contract claims, not validated or promoted runtime behavior.

ACTION_RECEIPT

- action_id: `spawn-0002`
- dispatch_id: `2026-08-05-arcanum-building-system-research`
- run_id: `arcanum-building-system-research-run-01`
- wave_id: `explorers`
- step_id: `s1-explore`
- role: `explorer-contract`
- capability_ref: `research`
- status: `pass`
- artifacts:
  - `FULL_EXPLORER_RETURN` in this response
  - expected parent-owned normalized output: `receipts/explorer-contract.json` — not written by this action
- validation: `pass`
  - frozen prompt read
  - direct current canonical sources inspected
  - parent and Arcanum source identities recorded
  - current Arcanum dirty state inspected
  - no repository mutation performed
  - proof statuses and live-uncommitted claims explicitly separated
- blockers:
  - Runtime fixture execution was outside this read-only explorer action; executable behavior remains unverified.
  - Generated mirror parity was not validated.
  - Live-uncommitted contracts cannot support promotion, release, or current-runtime-complete claims.

## Agent 3 — Beer, Stafford — recursive state and builder closure

FULL_EXPLORER_RETURN

Identity and evidence scope

- Parent repository: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`; Arcanum submodule HEAD: `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`. Both worktrees are dirty; claims below are observations of current bytes, not a clean-tree or execution proof.
- Dispatch target: `ops/development/2026-08-05-arcanum-building-system-research/dispatch-sheet.json` selectors `groups[0].agents[2]`, lines 51-55. Inventory was used only as a discovery lead; canonical sources were read directly.
- Status legend: all source-contract statements are observed; no Craft mutation, dispatch execution, generated-parity test, or lifecycle/promotion action was executed.

Craft: exact role and non-role

- Craft is the project-local recursive-state ledger: context, blockers, enablers, decisions, gaps, definitions, next moves, child contexts, validation evidence, and recomposition. `arcanum/arcana/craft/SKILL.md:14-31`.
- `.craft/ledger.yml` is authoritative for its chosen scope; `CRAFT.md` is a human view; `.craft/index.json` is rebuildable derived lookup; `.craft/artifacts/` may hold supporting evidence/receipts. `arcanum/arcana/craft/SKILL.md:56-72`; `templates/ledger.schema.yml:37-47,65-93`.
- The ledger has local authority over its own state, not over the native result it records: Craft can prepare handoffs, receive/apply receipt evidence, and open residue, while the called capability retains artifact contract, validation, and verdict ownership. `arcanum/arcana/craft/SKILL.md:312-317`.
- “Route memory” is therefore ledger state only. A route string/record does not authorize execution; Craft does not turn a dispatch or receipt into lifecycle authority. `arcanum/arcana/craft/SKILL.md:114-126,360-377`.
- Child contexts require recomposition evidence before closure; refinement supplies closure criteria, not closure evidence. `arcanum/arcana/craft/SKILL.md:193-203,241-268`.
- No current direct binding makes Craft a required Invoke → WPRA → Task Session stage. Task Session’s required sigils are Context Builder, Decision Gate, and one-hop Continuation Router. `arcanum/arcana/task-session/SKILL.md:22-30`. Craft may be a scoped state owner around that flow, or Goal may govern a broad multi-node Craft graph; it is not the executor. `arcanum/arcana/continuation-router/SKILL.md:45-54,85-96`.

Dependency graph

```text
ordinary intent
  -> Invoke authoring / implementation-layering (conditional)
  -> WPRA / implementation-readiness (selection and admission owners)
  -> Task Session (one SWU)
       -> Context Builder [required]
       -> Decision Gate [only unresolved consequential choice]
       -> Continuation Router [required closeout/one-hop]
       -> native owner execution + validation
  -> owner-controlled synchronization / terminal evidence

Craft <-> scoped contexts, blockers, decisions, gaps, receipts, residue,
          child-context recomposition; records, never replaces arrows above.

broad dependent Craft graph -> Goal (outer loop), not Continuation Router.
multi-agent route -> Dispatch Spec validates -> Orchestrate schedules/joins/closes.
reusable capability lifecycle -> Sigil Development or Spellcraft
  -> Experiment Harness -> Signal Observer -> Workflow Reflect -> owner revision route.
```

Current source basis: Task Session `SKILL.md:100-199,223-250`; Continuation Router `SKILL.md:98-171`; Dispatch Spec `SKILL.md:21-38,65-101,126-174`; Orchestrate `SKILL.md:59-68,77-140`.

State-authority matrix

| State/artifact | Owner | What it can establish | What it cannot establish |
|---|---|---|---|
| `.craft/ledger.yml` | Craft scope | local recursive state and local pending/residue | SWU selection, mutation permission, execution success, promotion |
| `CRAFT.md`, `.craft/index.json` | derived Craft views | human/machine navigation | source authority (`craft/SKILL.md:67-71`) |
| Inventory cards/indexes | Inventory | discovery, projections, contradiction visibility | source proof or meaning/promotion authority (`inventory/SKILL.md:335-339`) |
| Context pack | Context Builder | bounded, selected execution context | readiness/admission or successful execution |
| Decision record | Decision Gate / relevant owner | resolution of a blocker choice | all downstream validation or execution |
| Dispatch sheet | Dispatch Spec + parent | valid route shape and capability-bound roles | subagent execution or lifecycle completion (`dispatch-spec/SKILL.md:103-111,152-174`) |
| action/run receipt | Orchestrate | host preflight, spawn/join/gate/closeout state | delegate semantic work or promotion (`runtime/orchestrate/SKILL.md:63-68`) |
| terminal Task Session receipt | Task Session | one-SWU result plus required synchronization path | another owner’s work or recursive series |
| continuation receipt | Continuation Router | exactly one authorized/joined owner hop | owner mutation authority (`continuation-router/SKILL.md:147-171`) |
| signal/reflection report | observability family | maintenance evidence/proposal | direct sigil/spell rewrite or promotion |

Minimal capability closure

- Core stage: Invoke/implementation-layering where authoring/design/plan is needed; readiness owners; Task Session for exactly one selected SWU; Context Builder; validation owner; closeout synchronization.
- Conditional gate: Decision Gate for consequential unresolved choice; Distill for coherent-unit/plan evidence; Continuation Router for a terminal or typed prerequisite owner hop; Craft only when the target scope needs persistent recursive state.
- Outer-loop owner: Goal for a broad dependent Craft-backed graph; Task Session Until Blocker for explicitly requested ordered multi-SWU series. Task Session expressly must not execute more than one SWU in its receipt. `task-session/SKILL.md:32-39,100-111`.
- Delegated-work closure: Dispatch Spec validates explicit capability-bound graph; Subagent Strategy supplies authorization/lifecycle rules; Orchestrate performs preflight, spawn, join, wave gate, and closeout. `dispatch-spec/SKILL.md:87-101,126-174`; `runtime/orchestrate/SKILL.md:77-130`.
- Evidence/read-model support: Inventory is discovery/read-model support, never proof; Craft is state/read-model support around owner work; telemetry is evidence for maintenance, not authority.
- Capability-development owner: Sigil Development owns sigil contract mutation/lifecycle; Spellcraft owns multi-sigil composition/lifecycle; Experiment Harness supplies repeated-use evidence; Signal Observer derives signals; Workflow Reflect proposes, but does not mutate. `sigil-development/SKILL.md:54-73`; `spellcraft/SKILL.md:15-35`; `experiment-harness/SKILL.md:58-83`; `signal-observer/SKILL.md:89-96`; `workflow-reflect/SKILL.md:128-135`.

Omitted-skill shortlist

- Include `Goal` as load-bearing only for broad dependent Craft graphs; exclude from ordinary one-SWU work. Continuation Router explicitly routes that graph to Goal instead of itself.
- Include `work-pack-readiness-audit` and `implementation-readiness` as load-bearing readiness/admission owners, though their detailed contracts were outside this explorer’s source slice; do not substitute Craft state for them.
- Include `task-session-until-blocker` only for explicit series intent; it prevents collapsing a sequence into one Task Session.
- Include `Subagent Strategy` and `Dispatch Spec` only for delegated/multi-agent work; a route validator is not execution.
- Include `observability-setup` only when a repository lacks the observability package and reusable capability work needs it; otherwise it is setup convenience.
- Exclude `Inventory` as a mandatory execution gate: it supports discovery/context but is expressly non-authority.
- Exclude `Workflow Reflect` from normal feature completion: it is an outer maintenance loop driven by accumulated signals, not a task closeout gate.
- Exclude Craft from mutation admission and promotion: doing otherwise collapses state recording with lifecycle ownership.

Operating playbooks

1. Ordinary feature
   - Invoke/implementation-layering as needed → readiness selection/admission → Task Session selects exactly one SWU → Context Builder → Decision Gate if needed → mutation/validation → owner closeout synchronization → optionally record outcome/residue in the scoped Craft ledger.
   - First stop: missing selection, write scope, validation, or unresolved consequential decision. No Craft entry converts that stop to pass.

2. New sigil
   - Sigil Development owns candidate/contract mutation and lifecycle → Experiment Harness validates realistic use → Signal Observer records post-run evidence → Workflow Reflect may propose revision → Sigil Development/maintainer owns any update/promotion decision.
   - Craft may track the project’s local blockers/recomposition, but cannot promote the sigil.

3. New spell
   - Spellcraft composes referenced sigils, phases, shared state, gates, handoffs, and observability → Dispatch Spec when the composition needs an executable multi-role route → Experiment Harness/observer/reflector → Spellcraft/maintainer revision.
   - Do not copy sigil internals into a spell; do not claim one bounded Task Session proves reusable-spell readiness.

4. One selected SWU
   - Select/live-revalidate one eligible SWU → Task Session’s fast-entry/prerequisite checks where applicable → Context Builder → gates/admission → execute/validate → required one-hop closeout synchronization.
   - If a prerequisite owner hop is needed, Continuation Router validates the exact tuple, dispatches at most one owner, joins its distinct receipt, then returns to the same Task Session attempt; it never performs owner work. `continuation-router/SKILL.md:73-82,98-166`.

5. Until-real-blocker series
   - Explicit series intent → Task Session routes to Task Session Until Blocker → each iteration remains a distinct Task Session SWU and terminal receipt → stop at first real blocker → synchronize/record residue → route one bounded next owner only where admitted.
   - Craft can show pending-by-node and recomposition residue, but cannot erase the stop condition. `craft/SKILL.md:271-310`.

Residue / attack points

- The canonical source paths for Goal are not present under the expected `arcanum/spells/goal/` location in this worktree; only a reading-package example surfaced. Treat Goal’s role above as corroborated by Continuation Router’s current route catalog, not as independently contract-verified.
- Likewise, detailed WPRA and Implementation Readiness contracts were not inspected in this explorer’s bounded slice; their owner classification is supported by the frozen dispatch prompt and Task Session’s current required flow, but their exact receipt/admission details need the formal-contract explorer.
- Arcanum is dirty, including generated mirrors and related Task Session/readiness surfaces. No generated parity claim is warranted.
- Current Craft schema lists deferred route-exchange, projection, row-update, validation, and artifact-manifest schemas, so do not infer an implemented automated Craft route/renderer. `templates/ledger.schema.yml:24-47`.
- No direct live test was run; all validation status is unverified beyond source inspection.

ACTION_RECEIPT

- action_id: `spawn-0003`
- dispatch_id: `2026-08-05-arcanum-building-system-research-route`
- run_id: `arcanum-building-system-research-run-01`
- wave_id: `explorers`
- step_id: `s1-explore`
- role: `explorer-closure`
- capability_ref: `research`
- status: `pass`
- artifacts: parent-owned expected normalized output `receipts/explorer-closure.json`; no artifact written by this agent
- validation: `pass` — frozen target read; direct canonical/current sources inspected; no writes performed
- blockers: canonical Goal package path not independently located; WPRA/Implementation Readiness detailed contracts and generated parity intentionally left to sibling explorer scope; dirty worktree prevents clean identity/parity conclusion
