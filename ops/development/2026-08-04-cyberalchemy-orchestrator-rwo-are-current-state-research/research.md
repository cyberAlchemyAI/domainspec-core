# Verbatim Explorer Returns

## Agent 1 — Turing, Alan — implementation explorer

action_id=spawn-0001; role=implementation-explorer; status=pass; validation=block; artifacts=inline-explorer-return; blockers=FastAPI dependency unavailable, preventing selected runtime and Control Center test modules from importing; no dependency installation authorized

### Exact-binding explorer return

#### Evidence boundary

- Target repository: `projects/cyberalchemy-orchestrator`
- Immutable tracked identity: commit `b42228fcf4a5a6dadefbbfb53dfaa3c3edb28108`
- Worktree verification: HEAD exactly matched the pinned commit. The only reported worktree item was the pre-existing untracked `docs/features/recursive-work-orchestrator/`; it was not read.
- Historical baseline: `strategy-inventory-packet.json` selected entry `cyberalchemy-orchestrator-reasoning-engine-purpose-strategy-result-synthesis`, selectors `#accepted-result`, `#current-state-addendum---2026-07-23`, `#classification-boundary`. This is a non-authority discovery lead classifying the earlier repository as governed multi-agent orchestration/control plane, not a reasoning engine, with whole-engine integration unbuilt.
- Direct documentation identities:
  - `implementations/README.md`: git blob `03b39f04c7b90b8d709edc1a59aae6d15b1455c0`
  - `implementations/AS-BUILT.md`: git blob `e3da5c208d676231dc3df3d1eee88a8580447c7c`
- No repository files were written. `git diff --stat` remained empty.

#### Validation executed

Command used, with bytecode writes disabled:

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v implementations.tests.runtime.test_protocol_compilation implementations.tests.runtime.test_golden_manifest_v063`

Result: **13/13 passed** in 0.567 seconds:

- all twelve `ProtocolCompilationTests.test_pc1` through `test_pc12`;
- `GoldenManifestV063Tests.test_manifest_preserves_frozen_baseline_and_binds_extension_bytes`.

A broader selected command ran 22 discovered test entries:

- the same twelve protocol-compilation tests passed;
- ten modules failed during import because `fastapi` is absent from the current Python environment;
- those are environment-blocked/unverified, not observed implementation-test failures;
- no dependency was installed.

The Control Center `test_local_store` module also expects the documented `implementations/` working directory, but its broader run remained blocked within the same dependency-limited attempt.

#### Capability matrix

“Observed” means current tracked source and test bytes were inspected. “Executed” means this run actually ran the named check.

| Capability | Immutable source identity and exact selector | Exact test selector | Check | Proof status | Strongest supported claim | Explicit non-claim |
|---|---|---|---|---|---|---|
| Host workflow binding | commit `b42228f`; migration `009_host_workflow_binding.sql` blob `1f6e4c2`; `service.py` blob `5ba442e`, `RuntimeService.bind_host_workflow_turn` at line 5427, `complete_host_workflow_turn` at 5736, `get_host_workflow_binding` at 5829 | `test_host_workflow_binding.py` blob `9ad8c5a`: `test_three_seats_share_one_parent_dispatch` L262; idempotent/divergent retry L285; parent-close block L304; follow-up continuity L348; exact output bytes L383 | Attempted; import blocked by missing FastAPI | observed; execution unverified | Schema and service methods implement per-seat/per-turn binding, terminal completion, continuity, and exact-output constraints; focused tests exist | Does not prove real Codex/Claude host adoption, universal launch interception, provider delivery, authenticated authorship, or operation for this research dispatch |
| Dispatch workflow and routed launch plan | `dispatch_workflow.py` blob `aaeb01e`; `validate_opening_record` L61, `compile_bound_launch_plan` L94, `run` L231; appender path fixed at L28 | `test_dispatch_workflow.py` blob `aaf17a3`: canonical type L69; exact prompt/manifest L85; mismatch rejection L113; invalid opening before write L127; runtime-managed route absent L168 | Attempted; import blocked | observed; execution unverified | A CLI adapter exists to resolve LIVE dispatch capabilities, validate opening records via the owned appender, compile bound seats, and call host hooks | Does not prove an end-to-end host launch, that installed hosts invoke the hooks, or that external effects occurred |
| Hash-chained transactional journal | `journal.py` blob `94d4d23`; `RuntimeJournal.accept` L145 and `verify_store` L560; migrations 001–011 present | Journal exercised transitively by runtime suites including `test_stage_b.py`, `test_operator_recovery.py`, and delivery suites | Not executed; dependent suites blocked | observed | Durable SQLite command acceptance, idempotency/conflict handling, event groups, heads, receipts, and store verification are implemented in tracked code | Does not prove every repository action enters this journal, complete semantic replay, global recovery, or production operation |
| Protocol compilation | `protocol_compilation.py` blob `4624f9d`; `ProtocolCompiler.compile_candidate` L368 and `compile_dispatch_candidate` L489; `service.py` `compile_and_store_dispatch_candidate` L174 | `test_protocol_compilation.py` blob `280e8a7`, PC1–PC12 at L78–489; golden manifest test | **Executed: 13/13 pass** | executed | Pure, deterministic, closed-schema compilation is locally demonstrated, including golden vectors, unsupported requirements, DAG rejection, restart independence, idempotent storage separation, and candidate non-authority | Compilation neither authorizes dispatch nor executes a provider/effect; it is not a reasoning engine |
| Agent reference delivery | migration `010_agent_reference_delivery.sql` blob `de4a8dd`; `reference_delivery.py` blob `594d269`, selectors `derive_target_identity` L15, `decode_reference_bundle` L45, `build_effective_input` L72, verification L113/L200; `service.py` `deliver_reference_scout` L2658 | `test_agent_reference_delivery.py` blob `0d66b81`: atomic attempt/retry L281, scope drift L301, failpoint rollback L314, byte/lifecycle verification L348, post-commit convergence L365 | Attempted; import blocked | observed; execution unverified | Exact bundle decoding, target derivation, input construction, wrapper verification, and durable delivery service path exist with focused tests | Does not prove provider delivery, agent access/read/use, claim support, or a generic accepted handoff lifecycle |
| Bus/reveal delivery seam | migration `011_bus_reveal_delivery.sql` blob `9a2b166`; `reveal_delivery.py` blob `1e8c9cd`, invocation validation L36, peer entries L52, deterministic materialization L106, effective-input manifest L140 | `test_bus_reveal_delivery.py` blob `2a077e2`: official close/read absence L212, exact restart-stable reveal L229, derived recipient L270, atomicity L496, retry/conflict L575, pending external effect L625 | Attempted; import blocked | observed; execution unverified | A deterministic BUS reveal-to-effective-input seam and persistence schema are implemented; tests explicitly retain the provider effect as pending | Does not prove external provider execution or independent multi-seat judgment; AS-BUILT records a same-seat false-quorum counterexample |
| APT projection and research acceptance | migration chain `004_apt_projection.sql` through `008_reference_scout_ingestion.sql`; `projections.py` blob `c6a59d6`, `ProjectionManager` L33; `service.py` `append_apt_event` L4224, `accept_apt_research` L6092, ACI-owned APT read/mutation ports L5856–6092 | `test_apt_projector.py` blob `2d0e895`: projector-failure catch-up L73, deterministic rebuild L195; `test_apt_stage_b.py`: capture/query/restart L79, official lineage L349, concurrency L682, HTTP subprocess restart L959 | Attempted; import blocked | observed; execution unverified | Rebuildable APT query projections, capture/fact validation, lineage, and an ACI-owned transactional acceptance boundary exist in code | Projections are not authority, raw ingestion is not prompt inclusion/use, and no semantic reasoning-engine integration is shown |
| Operator verification, backup, retirement | `operator_recovery.py` blob `b37f831`; verify L51, online backup L141, retirement L180; CLI exposes corresponding commands | `test_operator_recovery.py` blob `7ca033e`: identity-preserving backup L41, overwrite refusal L54, CLI L61, incomplete cleanup L86, tamper/profile rejection L99/L108, recoverable retirement L122, active-sidecar refusal L144 | Attempted; import blocked | observed; execution unverified | Conservative local database verification, non-overwriting online backup, and byte-preserving retirement are implemented | No supported restore/reinstate command, no whole-harness checkpoint, no proof of an operator drill or production recovery |
| Control Center | `control_center/api.py` blob `aa6907b`, `create_router` L75 with six read routes L78–226; `main.py` blob `ea72c32`, interface-identity binding L91–109; `LocalControlCenterStore` exists separately | `test_binding.py` blob `a162b6a`: incomplete identity hides routes L12, complete identity exposes six L33; `test_api.py` blob `aad1a95`: six-route inventory L30, authority unavailable L75, deterministic path L107, partiality L139; local-store preview/non-apply tests | Attempted; import blocked | observed; execution unverified | Six fail-closed, read-oriented routes and interface binding exist; preview-only store rejects authoritative effects | Does not provide apply/approve/retry/reconcile/promotion; AS-BUILT says the in-process store is not wired to API/UI and visible drafts use browser localStorage |
| Runtime serving boundary | `main.py` blob `ea72c32`, runtime/provenance/health routers explicitly `enabled=lambda: False` at L68–76; `service.py` reports `production_serve_enabled: False` at L6289 | `test_apt_stage_b.py` contains disabled/enabled router cases L287–313; local-pilot and recovery suites | Not executed; dependencies blocked | observed | Production-reader runtime routes are closed in current composition; a separate explicitly gated loopback pilot exists in code | No production serving, deployment, production readiness, non-loopback service, or external effect was proved |
| Recursive Work Orchestrator | only pre-existing untracked subtree reported by status; packet freezes it separately as proposal-only | none admitted as tracked implementation evidence | Deliberately not read or run | unverified/proposal | No tracked implementation claim is supportable at pinned HEAD | Must not be conflated with the runtime primitives above, workflow routing, nested scheduler authority, or an implemented reasoning-engine seam |

#### Trace and proof-tier interpretation

The implemented path is materially richer than a UI-only reader:

1. A dispatch record can be validated and compiled into a bound launch plan.
2. A Session/Dispatch relationship and per-seat/per-turn host binding can be recorded.
3. Accepted commands enter a hash-chained SQLite journal with artifacts, events, heads, receipts, and rebuildable projections.
4. Protocol candidates can be deterministically compiled; this is the only slice directly re-executed here.
5. Specialized Reference Scout and BUS/reveal paths can materialize exact effective inputs.
6. APT can accept bounded research facts/lineage through ACI-owned ports and rebuild read projections.
7. Operators have verify/backup/retire mechanics.
8. Humans have read-oriented dispatch and Control Center surfaces, plus a local confirmation marker.

Those are different proof tiers. Schema and fixtures exist for all these surfaces. Focused tests exist. Only protocol compilation was freshly demonstrated in this environment. No full local server/pilot, cross-process host lifecycle, browser flow, provider effect, deployment, or production path was executed.

#### Delta from the historical Inventory classification

The historical classification remains directionally correct but is now materially incomplete.

What changed in current tracked bytes:

- The repository is no longer accurately summarized as merely a dispatch reader/control-plane UI. It contains an eleven-migration governed ACI/APT runtime, journal, artifacts, capabilities, host hooks, orchestration bridge, protocol compiler, specialized delivery seams, projections, local-pilot gates, and operator recovery.
- Host workflow binding is now a concrete schema/service/test surface, including per-seat/turn identity, terminal continuity, and output-byte constraints.
- Dispatch type resolution and bound launch-plan compilation are concrete CLI/library surfaces.
- Reference Scout delivery and BUS reveal delivery are concrete, transaction-oriented implementations, while their provider effect remains explicitly pending.
- APT projections and research acceptance are concrete local runtime surfaces.
- Control Center has six bound read routes and explicit fail-closed interface identity, though no authoritative mutation.
- Local database preservation is concrete through verification, online backup, and recoverable retirement.
- Protocol compilation moved beyond fixture presence: its deterministic local behavior was executed successfully in this run.

What did **not** change:

- The strongest whole-system identity is still a governed orchestration/control-plane and evidence runtime, not a semantic reasoning engine.
- Real host adoption is conditional and not established merely by hook/configuration bytes.
- Routing, compilation, delivery, journaling, and projection do not perform semantic judgment.
- No target-to-private-agent-reasoning-engine executable binding is present in the inspected target bytes.
- No external provider effect or production operation was proved.
- The recursive-work subtree remains untracked proposal material, not implementation.
- The AS-BUILT gaps remain load-bearing: incomplete host coverage, unauthenticated human authority, output/effect coverage gaps, false BUS quorum, no generic delivery/acceptance lifecycle, no whole-checkpoint restore, and no authoritative Control Center mutation.

#### Blockers and residue

- `fastapi` absent from the current environment blocked fresh execution of host binding, dispatch workflow, reference delivery, BUS reveal, APT projector, operator recovery, and Control Center suites. Installing it was forbidden.
- No current end-to-end local runtime receipt was produced.
- No host-version adoption witness was exercised.
- No external-effect or provider path was exercised.
- No browser validation was run.
- No restore/reinstate implementation was found in the inspected operator-recovery surface.
- No automatic consumer of the UI confirmation marker is supported by the inspected AS-BUILT evidence.
- No executable recursive-work or reasoning-engine integration is established.
- Historical Inventory remains discovery evidence only; the exact delta claim is anchored to current tracked bytes and the packet’s bounded prior classification, not to an assertion that every intervening commit was reconstructed.

## Agent 2 — Simon, Herbert — proposal explorer

action_id=spawn-0002; role=proposal-explorer; status=pass; validation=pass; artifacts=inline-explorer-return; blockers=none

### Exact bindings and claim ceiling

| Evidence | Immutable identity / selector | Status |
|---|---|---|
| Dispatch sheet | `dispatch_id=2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state`; SHA-256 `d5e348…e0e5` | observed; establishes this lane’s read-only scope, not target authority |
| Inventory packet | `2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state`; SHA-256 `a7e078…4fc0` | discovery-only; reports no target-local machine Inventory and unresolved mapping gaps |
| RWO design | untracked `DESIGN.md`; SHA-256 `28b6fc…9419`; `authority: proposal-only` | proposal semantics only |
| RWO ontology | untracked `ontology/ONTOLOGY.md`; SHA-256 `1c6d41…920`; `rwo-architecture@0.1.0` | candidate semantic map; no canonical, runtime, or promotion effect |
| Workflow discovery | tracked blob `f07c6d0d92d60ffb239a2ef733f43d20850140f4` at `b42228f…28108` | draft, unreviewed investigation brief; not a schema/decision/plan |
| Autonomous target | tracked blob `92584e7dd3b30b512994dcdf31cc9cd62dd7e619` at `b42228f…28108` | draft branch intent; target model, not implementation proof |
| Best-understanding view | `research.md`; SHA-256 `3b1de2…b568` | research evidence only; explicitly says no runtime, replay UI, browser, or comprehension result observed |

No target ACI binding was invoked or registered; no files, Git state, dependencies, network, or telemetry were changed.

### Proposal inventory

The RWO proposal has a coherent *candidate* kernel: immutable versioned `WorkDefinition`; `WorkRun` and attempts; leaf/composite substitutability; event-triggered edges; one root expansion; command/event separation; accepted journal; rebuildable cursor; and non-authoritative status projections. Its non-collapse constraints are unusually clear:

- Recursive composition is required, but nested orchestration authority is prohibited (`DESIGN.md:19-32`, `§4.4`, `RWO-I02`; ontology shield `rwo:f.no-nested-orchestrator-invocation`).
- The **definition graph** describes reusable work topology. An expanded **run plan** is instance-specific and addressed; it must not be treated as a new definition or as authority inherited by containment.
- **Accepted history** belongs to the journal; the root’s **routing cursor** is a versioned, rebuildable control projection; **domain status** and confirmation meaning remain work/gate-owned (`DESIGN.md:287-302`; `ONTOLOGY.md:137-187`).
- A command is an addressed request; an event is an accepted fact. Delivery, journal recording, projection, or terminality cannot be silently elevated into authorization, success, approval, or domain truth.

The workflow-graph brief instead frames a repository-wide discovery whose central question is whether there is one graph at all. It separates structure, authority, allocation, communication/coordination, and state until evidence supports a smaller representation. The autonomous-agent target makes a different, still-draft target choice: a workflow graph of **agent nodes**, a human confirmation view, immutable executable Dispatch, and Run facts.

These can inform each other, but they are not yet one model.

### Hypotheses and tensions

| ID | Hypothesis / tension | Exact evidence | Status and required resolution |
|---|---|---|---|
| H1 | RWO `WorkNode` can be a reusable structural work position without equaling an agent. | RWO `DESIGN.md:87-146`; WGQ-2/3 | plausible candidate; target says every workflow-graph node is an Agent Node, creating a direct taxonomy tension. Decide whether RWO is below the workflow layer, or revise one vocabulary. |
| H2 | One root RWO kernel can execute a confirmed Dispatch without becoming the owner of confirmation, domain status, or effects. | `DESIGN.md:54-68,287-330`; target SP-1–SP-5 | candidate only. Requires a total, versioned authority mapping and negative tests. |
| H3 | RWO’s event-triggered graph can represent bounded rework while protocol compilation retains a finite DAG. | `DESIGN.md:148-220`; WGQ-8 | unresolved. “Bounded repeat” must be specified as repetition/new generation/state transition, not assumed compatible. |
| H4 | Journal + reducer can reconstruct routing eligibility without becoming authoritative work state. | `DESIGN.md:287-330`; RWO-OQ-001/006; WGQ-1/7/8 | unresolved. The proposal itself leaves journal-versus-work-state and migration semantics open. |
| H5 | Existing ACI concepts can be reused as adapters/boundaries, not as proof the RWO exists. | workflow discovery §4; target README:44-46 | reuse candidate only; each field/invariant needs claim-by-claim mapping and verification. |
| T1 | RWO’s uniform `Work` allows deterministic operations, gates, joins, adapters, and human approval as leaves; target says every Workflow Graph node represents an agent. | RWO `DESIGN.md:116-146`; target README:369-389 | material conceptual contradiction unless a layer boundary is chosen. Do not encode scheduler/gate/join as agents by convenience. |
| T2 | RWO has a candidate primitive WorkGraph and expansion model; workflow discovery rejects a preselected universal graph. | RWO `§4-5`; WG brief `§1-2, WGQ-1` | RWO may be a bounded lower-layer hypothesis, not an answer to WGQ-1. |
| T3 | RWO calls the journal accepted history and cursor a projection; target requires durable Run facts, attributable decisions, artifacts, and terminal outcomes. | RWO `§7`; target SP-7–SP-9 | incomplete, not necessarily contradictory. Define exact ownership/lineage of Run facts versus journal events and projections. |
| T4 | RWO says external DomainSpec policy becomes adapters/work units; target needs enforcement over tools, prompts, sandbox, effects, and bus communication. | RWO `§3, §12`; target SP-3–SP-4 | boundary is unproven. Adapter placement must not weaken enforceable policy into a work-level convention. |
| T5 | RWO’s at-least-once/idempotency is candidate transport semantics; target requires recovery and honest unknown outcomes. | RWO `§6.2`, RWO-OQ-003; target SP-9 | compatible only after host/process guarantees, outbox/inbox ownership, and effect evidence are selected and tested. |

### Explicit decisions vs preserved non-decisions

**Candidate decisions within RWO only:** uniform outer Work contract; composite closure; one root runtime; explicit event selector/input mapping; bounded cycles; commands/events distinct; projections non-authoritative; no parent authority inheritance; fail-closed unknowns.

**Not decided by RWO:** journal authority; dynamic topology confirmation; delivery guarantees; cancellation/compensation catalog; quorum semantics; migrations; authority-reference minimum; counterexample sufficiency; stream closure; promotion owner; event-class representation; input-mapping purity; executor-adapter ownership; relation transitivity.

**Not decided by workflow discovery:** canonical graph count/name; node=agent; terminal representation; communication’s placement; group irreducibility; `DispatchSpec` schema/migration; runtime capability. It authorizes neither implementation nor promotion.

**Not decided by autonomous target:** detailed schemas, persistence, provider/sandbox/credential/artifact-store implementation, migration from current architecture, compatibility, or implementation phases. Its target shape must not retroactively promote the RWO proposal.

### Open-question matrix

| Question | Owner to resolve | Impact |
|---|---|---|
| RWO-OQ-001 journal authoritative state vs durable copied evidence | RWO/work-state and journal owner | reconciliation, replay, conflict ownership |
| RWO-OQ-002 dynamic graph extension and confirmation | confirmation/Dispatch authority owner | prevents silent topology expansion |
| RWO-OQ-003 cross-host delivery guarantees | protocol/adapter/storage owner | delivery and idempotency architecture |
| RWO-OQ-004 cancellation and compensation combinators | work-policy owner | kernel surface and recovery semantics |
| RWO-OQ-005 structural `quorum(n)` vs gate work | coordination/semantic-governance owner | whether readiness is mistaken for judgment |
| RWO-OQ-006 schema/reducer migrations | versioning/replay owner | historical meaning and deterministic resume |
| RWO-OQ-007 minimum verifiable authority reference | authorization/effect-boundary owner | kernel must not own authorization policy |
| RWO-OQ-008 sufficient bounded-pipeline counterexamples | validation/evidence owner | expressiveness claim ceiling |
| RWO-OQ-009 long-lived stream vs separate subscription | Work-contract owner | closure of uniform Work |
| RWO-OQ-010 promotion owner | canonical-definition/promotion owner | prevents accidental authority |
| Ontology residue 011–014 | ontology source owner, then relevant contract owner | event-class location; mapping purity; adapter ownership; relation transitivity remain open |
| WGQ-1 graph/state structure count | workflow-graph discovery owner | canonical lifecycle authority partition |
| WGQ-2 node meaning | workflow taxonomy owner | whether task/gate/operation/outcome are nodes |
| WGQ-3 node/agent/seat/attempt cardinalities | identity/runtime-domain owner | retry/reuse without collisions |
| WGQ-4 node and edge taxonomy | protocol/workflow schema owner | executable closed schemas and behavior |
| WGQ-5 workflow vs communication | workflow and Bus Contracts owners | prevents duplicate routing/permission authority |
| WGQ-6 collective coordination | group/coordination owner | quorum, dissent, budgets, collective result |
| WGQ-7 completion model | Run/audit/closure owner | separates attempt end, outcome, terminal fact, audit close |
| WGQ-8 rework under a DAG | workflow state/retry owner | bounded loops, generations, replay |
| WGQ-9 compilation and confirmation | protocol compilation + confirmation + Dispatch owners | total mapping, lineage, fail-closed authority |
| WGQ-10 simplified views | projection/UI/telemetry owner | views remain derivable and non-authoritative |

### Current primitives: reuse candidates only

The workflow brief identifies `ProtocolRecipe` finite DAG and node/edge kinds, non-authoritative `DispatchCandidate`, open `DispatchSpec.group_graph`, `AgentInvocationPlan`, and runtime `Group`, `Seat`, `Attempt`, terminal Run facts, and audit close (`workflow-graph/README.md:108-127`). The autonomous target separately names Workflow Graph, Agent Node, Typed Relation, Dispatch, Confirmation View, and Run.

They are useful candidates for a mapping inventory; they do **not** prove RWO compatibility, executable behavior, host guarantees, or an implementation seam. The inventory packet explicitly records that the current implementation-to-RWO mapping has not been verified claim by claim.

### Adoption ladder

1. **Proposal:** keep RWO design/ontology explicitly candidate-local with stable digests, residue, and no authority effect. Current status: reached only at document level.
2. **Implementation-ready:** resolve the question matrix; choose the layer boundary between RWO Work nodes and agent-only Workflow Graph nodes; produce a total source→candidate→confirmation→Dispatch→Run mapping, authority matrix, schemas, owner assignments, counterexamples, and negative tests.
3. **Executable:** implement only the approved slice with graph validation, single-root expansion, versioned journal/reducer/cursor, adapter/effect boundary, and fixtures for duplicates, divergent duplicates, stale attempts, cancellation, bounded exhaustion, replay, and blocked paths.
4. **Integrated:** prove mappings to target-owned Dispatch/Run/AgentInvocationPlan and Bus boundaries with lineage; ensure runtime facts never rewrite frozen confirmed authority; validate end-to-end recovery and audit closure.
5. **Promoted:** explicit canonical-definition and promotion-owner decision (RWO-OQ-010), reviewed evidence, target acceptance, and no remaining proposal-only wording for the promoted contract. No promotion is requested or justified now.

The decisive design constraint is to preserve four separate objects: immutable **definition graph**, confirmed/expanded **run plan**, append-only **accepted history**, and derived **routing cursor**, while retaining work-owned **domain status**. Collapsing any two would contradict at least one source’s stated authority boundary.

## Agent 3 — Hewitt, Carl — integration explorer

action_id=spawn-0003; role=integration-explorer; status=pass; validation=pass; artifacts=inline-explorer-return; blockers=none

### Evidence boundary

- Orchestrator tracked source identity: commit `b42228fcf4a5a6dadefbbfb53dfaa3c3edb28108`.
- Recursive-work proposal identities:
  - `DESIGN.md`: SHA-256 `28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419`
  - `ontology/ONTOLOGY.md`: SHA-256 `1c6d417c4f0cdfc73c7c42f016c05fd6f8fbccd738a35bf7454472d3cee3b920`
- Reasoning architecture identities:
  - `design/ARCHITECTURE.md`: SHA-256 `1958758a104c19af9966fd1460097c18fbf919e480da45e5c8dcc0b5f4ffe0de`
  - `design/aci-reasoning-binding/ARCHITECTURE.md`: SHA-256 `02eaede41676bcf19e45cb8cf9b7130bddf297d6ae786d81fdb67ee456bb2c8c`
- Executable bounded-L0 identities:
  - `execute.mjs`: SHA-256 `72de12f61b8450dc28bce29ce592787c912e99cb2eb781a9481f71998ddc03b5`
  - `reducer.mjs`: SHA-256 `e2a50b3db67ec47476a0a5bf14179535bfff3073a9228894439658b4b602fcaf`
- Proof posture: direct byte inspection. Existing test selectors and the promoted terminal receipt were inspected; no tests were executed in this read-only seat. The recursive-work files explicitly declare `proposal-only`; the whole reasoning engine remains candidate except for the promoted local L0 evaluator witness.

### Matrix A — recursive-work concept to current orchestrator owner/witness/gap

Common authority rule for every row: the orchestrator owns routing/lifecycle mechanics only; the invoked work or external owner retains semantic and effect authority. Failure is fail-closed. Replay never upgrades evidence or authority.

| Recursive-work concept | Current producer → consumer; immutable identity/payload | Current owner and gate | Witness / failure / replay | Status, selector, forbidden substitution |
|---|---|---|---|---|
| `WorkDefinition` | Confirmed dispatch row → dispatch workflow compiler; dispatch ID plus exact row/schema/digest | Dispatch/spec owner has authority; dispatch workflow owns launch lifecycle; type capability owns meaning; canonical appender validation gates admission | `validate_opening_record` rejects malformed/unvalidated rows; current record can be replay-resolved from ledger but is not a generic immutable `WorkDefinition` | **NARROW / partial analogue**. `implementations/server/runtime/dispatch_workflow.py:24-28,61-113`. Do not call a dispatch row a promoted recursive-work definition. |
| `WorkRun` and stable node address | Open parent dispatch → bound host seat; `dispatch_id/group_id/seat_index/turn_ordinal/attempt_id` plus prompt/manifest digests | ACI runtime owns accepted lifecycle/journal identity; host seat owns execution status; dispatch owner owns confirmation | Exact retry returns same `binding_id`; divergent retry raises idempotency conflict; journal supports reconstruction | **SELECT as reusable identity surface**, not semantic equivalence. `host_dispatch_hook.py:42-54`; `test_host_workflow_binding.py:262-300`. Node address grants no authority. |
| Leaf executor adapter | Bound launch item → native host Agent/spawn/follow-up operation; workflow envelope plus manifest | Host adapter owns translation; ACI validates binding; target agent/work owns result semantics | Missing marker, malformed envelope, digest mismatch, wrong target or unbound follow-up blocks | **NARROW**. `host_dispatch_hook.py:332-343,439-512`; `dispatch_workflow.py:137-181`. Host binding is an integration surface, never permission to invoke. |
| Composite body / graph expansion | Dispatch groups/connections → launch plan | Current compiler emits initial per-seat launches, not a general nested graph expansion kernel | Validates groups/agents and emits bounded launch descriptors; no evidence of recursive flattening, typed boundary projection, or arbitrary event-edge interpretation | **DEFER / gap**. `dispatch_workflow.py:94-181`; RWO `DESIGN.md` §§4.4, 5. Current dependency choreography must not be relabeled recursive composition. |
| Sequence | Confirmed group dependency → downstream stage handoff | Strategy/type owner owns readiness semantics; orchestrator owns edge traversal after typed gate | Missing required artifact or non-ready handoff blocks downstream | **NARROW** to governed stage sequencing; no generic RWO operator witness. Dispatch sheet `connections`; strategy lifecycle “Register and run.” Existence of an upstream artifact is not readiness. |
| Fan-out | One parent dispatch → several bound seats | Parent dispatch owns scope; ACI runtime owns each accepted seat binding; agents own outputs | Three seats share one parent and ledger row in test; each has exact attempt identity | **SELECT as finite witness of fan-out shape**, not RWO implementation. `test_host_workflow_binding.py:262-283`. Parallel launch does not confer equal judgment or authority. |
| Fan-in / join | Explorer returns → synthesizer or verifier | Consuming capability owns reconciliation semantics; orchestrator only waits/routes | Current governed dispatch supports joins through declared stage gates; no generic canonical input-manifest reducer witnessed | **NARROW / partial**. Strategy dispatch connections and RWO `DESIGN.md` §5.3. Quorum or arrival count cannot substitute for semantic reconciliation. |
| Gate and route label | Type-owner handoff verdict → eligible downstream edge | Gate owner owns decision/evidence; orchestrator owns exact matching/traversal | `ready`, `needs_feedback`, or `blocked`; undeclared/exhausted feedback edge blocks | **SELECT as architectural precedent**, not uniform Work gate API. Strategy skill Lifecycle §3; RWO `DESIGN.md` §5.4. Routing a positive label is not making the decision. |
| Sidecar | Telemetry/APT/control projections observe accepted runtime facts | Journal/session/dispatch owners retain lifecycle; APT and UI are projection owners | Rebuildable/read-only projections; no evidence of generic start/await/detach/cancel sidecar policy | **DEFER** generic sidecar; **NARROW** observational sidecars only. `service.py:655-714`; RWO §5.5. Projection cannot become status or authority owner. |
| Bounded repeat | Follow-up/zig-zag feedback edge → previously declared seat/stage | Strategy owns loop cap and eligibility; host binding owns exact turn/attempt | Unbound follow-up blocks; exhausted/undeclared feedback must remain residue | **NARROW** to declared governed feedback, not arbitrary repeat combinator. `host_dispatch_hook.py:512`; dispatch `connections`. Retry cannot silently change definition, scope, or authority basis. |
| Command/event lanes | Host lifecycle call/publication → ACI command acceptance/EventJournal | ACI owns canonical acceptance, journal, idempotency and aggregate versions; host/adapter executes | Strict envelopes, capability scope, CAS/idempotency; invalid or duplicate-divergent inputs block | **SELECT** as current protocol precedent. `host_dispatch_hook.py:212-258`; `orchestration_bridge.py:143-248`; `service.py` journal acceptance surfaces. Transport/persistence does not decide semantics. |
| Journal and routing cursor | Accepted commands/events → journal and read projections | ACI has one physical integrated writer; projections own no source lifecycle | Verify/rebuild from accepted offsets and refs; projections are derived | **SELECT journal; DEFER generic RWO cursor**. ARE ACI binding §§2–4; RWO §§6–7. Journal fact is not evaluator admission or domain status. |
| External effect adapter | Exact authorized command → target adapter | Exact-effect gate owner authorizes; ACI accepts effect intent; adapter owns attempt | Current ARE only has fixed in-memory test double; orchestrator has no RWO-wide effect adapter proof | **DEFER real effect integration**. ARE `execute.mjs:150-221`; terminal receipt says test-double only. Neither routing success nor semantic positivity permits an effect. |

Matrix-A conclusion: the current orchestrator supplies strong reusable precedents for confirmed dispatch identity, host-seat binding, idempotent lifecycle acceptance, one journal, finite fan-out, governed handoffs, and projections. It does **not** implement the proposed recursive `WorkDefinition` algebra, recursive composite flattening, generic event-edge compiler, generic sidecars, or a generalized replayable orchestration cursor. Those remain proposal/gap.

### Matrix B — exact reasoning-engine integration bindings

The retained topology is an ACI-subordinate, gate-adjacent semantic adapter. In integrated mode, all command/event/journal/replay-cursor/effect-intent identities remain ACI-owned. The evaluator owns only deterministic admission, applicability, derivation, typed semantic outcome, residue, and semantic receipt content.

| Stage | Producer → consumer; immutable identity and payload | Owners: authority / lifecycle / semantic | Gate, failure, replay | Evidence / selector / forbidden substitution |
|---|---|---|---|---|
| 1. Reasoning entry | Confirmed dispatch + bound seat → `ReasoningRunCommandMapper`; dispatch digest, binding ID, manifest/prompt digests, proposed run envelope | Dispatch/entry-gate owner / ACI / none yet | Exact confirmed dispatch, current binding, entry decision, and schema/digests required; mismatch blocks with zero evaluator calls; replay verifies prior acceptance only | **Candidate binding**, current inputs implemented separately. ARE ACI binding §§2–4; host binding test §§262–300. Target host binding cannot spoof parent confirmation or reasoning admission. |
| 2. Intent projection | Raw expression + selected-local record → Intent Projector/route resolver; request digest, catalog digest, posture-bearing fields | Intent/revision owner / ARE projection component / none | Unresolved semantic source/revision remains unresolved; invalid request/catalog yields non-authorizing disposition | **Implemented local route resolver plus candidate whole-engine projector**. `intent-route-resolver/src/resolve.mjs:103-185`; `authority_effect: none` at lines 172-180. A candidate route is not dispatch authorization. |
| 3. Actor/ACI journal | Accepted ACI command/events → `ActorEventMapper` → immutable actor cut; command/event IDs, offsets, aggregate versions, refs/digests | ACI authority owner / ACI one-writer journal / evaluator only consumes | Unknown schema, missing digest, cross-run substitution, or unverified cut blocks; historical replay reads verified cut and performs no actor calls | **Candidate cross-repo mapping; current ACI journal/binding exists**. ARE ACI binding §§2–4. A local `RuntimeJournal` may not become a second integrated writer. |
| 4. Bounded L0 evaluator | Frozen frame/snapshot/catalog/observations/challenge closure/journal cut → semantic evaluator; `run_id`, input digests, evaluator `semantic-judgment-evaluator@1` | Catalog/authority owners external / evaluator package invocation / evaluator | Record digest/schema checks, active catalog, non-self-appointed owner, acyclic precedence, finite rules and challenge closure; invalidity/defer/escalation produces zero effect | **Promoted bounded L0 witness**. `reducer.mjs:202-320+`; terminal receipt validation all true. Runtime coordination or actor consensus cannot substitute for admitted facts or rules. |
| 5. Challenge/admissibility | Actor proposals + challenge records → Observation Admitter/evaluator; observation IDs/digests, posture, lane limits/deadlines | Challenge/catalog owner / actor protocol journals attempts / evaluator admits and closes under pinned policy | Failed/open/timed-out required lane → `Deferred.Insufficient`; unresolved material dispute → `EscalateOwner`; admitted defeater → `Ineligible.Defeated` | **Executable inside bounded evaluator, broader actor production candidate**. `reducer.mjs:159-193,225-246,315+`. Synthesizer agreement cannot manufacture support or close a challenge. |
| 6. Exact-effect candidate | `RecommendedUnderSnapshot` + persisted semantic receipt → fixed envelope → exact-effect gate → candidate ACI effect command | Exact-effect owner / ACI effect-intent lifecycle / evaluator supplies non-authorizing premise | Receipt persists first; only identical envelope and gate `pass` proceeds; all other outcomes/gate verdicts make zero attempts; mismatch closes incomplete | **Executed only with fixed test double**. `execute.mjs:125-221`. Recommendation, dispatch completion, or entry pass cannot substitute for exact-effect pass and ACI acceptance. |
| 7. Historical replay | Verified journal cut + exact semantic artifacts → `ReplayBridge`/evaluator; retained request and exact receipt bytes | Source owners unchanged / ACI + artifact retention owners / evaluator deterministic reducer | No providers, tools, authority resolver, effect gate, or effects; byte mismatch fails replay proof | **Executable local L0; integrated bridge candidate**. `replay.mjs:5-22`; terminal receipt confirms exact bytes and zero calls. Replay does not refresh truth or authorization. |
| 8. Current revalidation | Prior refs + current authority/catalog/evidence/time → new reasoning run | Current owners / new ACI run lifecycle / evaluator | New IDs/digests and fresh entry/effect gates; may yield `Invalidated`; never overwrites history | **Designed, bounded evaluator temporal branch implemented; integration unwitnessed**. `reducer.mjs:196-200,261-271`; architecture Design Decision ARE-DES-007. Revalidation is not replay. |
| 9. L1–L3 | L0 receipt/ref → future protocol, integration, and effect layers | Owner receipts required per layer / ACI-subordinate lifecycle / semantic owner remains evaluator | External ACI, Bus, ACP, APT maturity and conformance gates must pass before integrated implementation or compatibility claim | **DEFER**. ARE architecture View 6 and ACI binding View 6; decision explicitly says implementation authorized `false`, selected SWU `none`. L0 promotion cannot promote the whole engine. |

### Topology verdicts with finite witnesses/counterexamples

| Option | Verdict | Finite witness or counterexample |
|---|---|---|
| Reasoning engine as leaf `Work` adapter | **NARROW** | Safe shape: one addressed command containing immutable reasoning-run refs; adapter returns accepted lifecycle events and a semantic artifact ref. Counterexample: if the adapter writes an integrated local journal or emits an effect directly after recommendation, it duplicates ACI and effect ownership. Therefore only an ACI-subordinate leaf facade is retainable. |
| Reasoning engine as composite `Work` body | **DEFER** | The candidate whole-engine flow contains entry gate, actor work, evaluator, effect gate, replay, and could structurally compile as a composite. But no recursive-work graph implementation, accepted `WorkDefinition`, or cross-repo composite fixture exists. Calling it composite now would promote proposal syntax into implementation. |
| Gate-adjacent evaluator | **SELECT** | Entry `block` persists and closes with zero evaluator calls (`execute.mjs:102-123`). Entry `pass` permits exactly one bounded evaluation; `RecommendedUnderSnapshot` still requires a fresh exact-effect decision (`125-183`). This distinctly preserves gates from semantic judgment. |
| Sidecar | **NARROW** | A read-only semantic audit/replay observer may consume an immutable journal cut and publish a non-authorizing artifact. Counterexample: a sidecar whose result releases an effect without an explicit gate is de facto a gate and violates RWO §5.5. Sidecar is acceptable only for observation/audit, not primary reasoning needed for routing. |
| None | **KILL as the general answer; retain as fallback** | “None” discards the already-selected ACI-subordinate target and the useful L0 semantic witness. It becomes correct only if cross-repository conformance fails or an owner selects standalone reroute option D. |

Selected topology:

```text
confirmed dispatch / RWO leaf address
  -> ACI canonical command acceptance and one journal
  -> actor cut / proposed observations
  -> gate-adjacent bounded semantic evaluator
  -> immutable semantic receipt artifact + ACI reference acceptance
  -> fresh exact-effect gate
  -> ACI effect intent
  -> external adapter
```

No nested reasoning scheduler; no second journal; no semantic ownership in the orchestrator; no effect authority in the evaluator.

### Smallest safe documentation-only integration contract

1. **Binding identity:** versioned document with exact orchestrator commit, RWO proposal hashes, ARE architecture hashes, evaluator ID/version, and explicit `authority_effect: none`.
2. **Input envelope:** confirmed `dispatch_id` plus dispatch digest; ACI `command_id`/digest and verified journal span; bound host-seat address; semantic `run_id`; frozen input digests.
3. **Ownership table:** ACI owns canonical command/event acceptance, journal, replay cursor, aggregate concurrency, and effect intents. ARE evaluator owns observation admission, applicability, derivation, typed outcome, residue, and semantic receipt content. Artifact owner owns bytes/admission. Gate owners own entry and exact-effect verdicts.
4. **Ordering:** confirmed topology → entry gate persisted → ACI actor facts → evaluator → semantic receipt persisted → exact-effect gate → ACI effect-command acceptance. Every non-pass or persistence failure stops.
5. **Identity rules:** cross-run substitutions, unknown versions, missing digests, stale temporal state, or locally invented ACI identifiers fail closed.
6. **Replay rule:** historical replay consumes immutable accepted facts and exact artifact bytes with zero mutable/external calls. Current revalidation is a new run.
7. **Negative controls:** routing label ≠ semantic judgment; journal acceptance ≠ evaluator admission; recommendation ≠ authorization; effect-gate pass ≠ ACI acceptance; host binding ≠ parent dispatch authority; projection ≠ lifecycle state.
8. **Claim ceiling:** documentation candidate only; no adapter, ACI binding registration, compatibility, integrated runtime, whole-engine promotion, effect, publication, or deployment claim.

### Open owner decisions / explicit residue

- RWO promotion owner and whether the proposal becomes an accepted specification (`RWO-OQ-010`).
- Exact relationship between work-owned state and the ACI journal (`RWO-OQ-001`).
- Dynamic graph extension and what confirmation rebinds changed topology (`RWO-OQ-002`).
- Cross-host delivery guarantees and reducer/schema migration rules (`RWO-OQ-003`, `RWO-OQ-006`).
- Minimal authority reference the orchestration kernel may verify without owning policy (`RWO-OQ-007`).
- Whether the reasoning invocation is standardized as an ACI-subordinate leaf facade; composite representation waits for an actual recursive-work compiler and fixture.
- Accepted cross-repository schemas for command, journal cut, semantic artifact reference, and effect intent.
- Current ACI/Bus/ACP/APT maturity and conformance receipts; all remain external blockers for integrated L1–L3 work.
- Catalog applicability/precedence and challenge-closure owners for non-fixture domains.
- Artifact-admission, retention, and incident/compensation owners.
- No real-effect witness, no integrated replay bridge, no recursive-work runtime, and no whole-engine executable witness presently exist.

Validation result is `pass` for the requested read-only mapping: both matrices are closed to direct selectors and immutable identities, topology options have finite discriminators, and residue is explicit. It is not an integration-readiness or implementation authorization verdict.
