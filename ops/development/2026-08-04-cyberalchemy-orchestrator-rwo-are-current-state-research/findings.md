# cyberalchemy-orchestrator: current-state and integration findings

## Answer first

At tracked commit `b42228fcf4a5a6dadefbbfb53dfaa3c3edb28108`,
`cyberalchemy-orchestrator` is substantially more than a reader or a design
stub: it has a governed orchestration/control-plane and evidence runtime with
host-seat binding, bound launch-plan compilation, an ACI-oriented hash-chained
journal, deterministic protocol compilation, specialised delivery seams,
projections, conservative local recovery operations, and read-oriented Control
Center routes. This is **observed implementation**; protocol compilation is the
only freshly **executed** slice (13/13 tests passed). It is not a semantic
reasoning engine, an external-effect proof, a production service, or proof that
every listed surface works together. [Explorer 1, `research.md#agent-1--turing-alan--implementation-explorer`; tracked source selectors below; E1]

The new Recursive Work Orchestrator (RWO) is not tracked implementation at
that commit. Its `DESIGN.md` and `ontology/ONTOLOGY.md` are separately frozen,
untracked **proposal-only** bytes. The tracked workflow-graph discovery and
autonomous-agent-graph document are also hypotheses/target-model material, not
an adopted schema or runtime. Consequently, no recursive-work implementation,
integration, promotion, or host binding follows from this research. [Explorer
2, `research.md#agent-2--simon-herbert--proposal-explorer`; E2, E2-WG]

The only retained cross-owner direction is a **documentation-only**,
ACI-subordinate, gate-adjacent bounded semantic evaluator. It preserves one
ACI command/event journal and separately owned entry, artifact-admission, and
exact-effect verdicts. The private agent-reasoning-engine (ARE) supplies a
bounded local L0 witness, not a whole-engine or cross-repository runtime
integration. [Explorer 3, `research.md#agent-3--hewitt-carl--integration-explorer`;
`synthesis-revision-2.md#typed-reasoning-entry-boundary`; E3, C1]

Status vocabulary used here: **executed** = freshly run in this research;
**observed** = direct current source/test bytes inspected; **unverified** = no
execution or compatibility evidence. “Proposal” and “hypothesis” are not proof
statuses for implementation.

## Evidence boundary and claim ceiling

Tracked target evidence is pinned to `git:b42228fcf4a5a6dadefbbfb53dfaa3c3edb28108`.
RWO proposal bytes are pinned separately: `DESIGN.md`
`sha256:28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419`
and ontology `sha256:1c6d417c4f0cdfc73c7c42f016c05fd6f8fbccd738a35bf7454472d3cee3b920`.
The workflow discovery and autonomous target are tracked blobs
`f07c6d0d92d60ffb239a2ef733f43d20850140f4` and
`92584e7dd3b30b512994dcdf31cc9cd62dd7e619`. ARE/ACI direct-source evidence
and the bounded L0 witness are separately pinned in E3. [E1–E3,
`receipts/evidence-closure.json#evidence_rows`]

This research does **not** implement, authorize, select an executable seam,
assign an owner, register a target host binding, promote, publish, deploy, or
prove production readiness. It also does not authorize external effects. The
reviewed output is evidence-bounded documentation only. [C1,
`receipts/evidence-closure.json#claim_ceiling`; final reviewer PASS,
`review-final.md#final-reviewer-gate`]

## Tracked implemented state

| Surface | Direct selector and explorer reference | Status | Supported claim; non-claim |
|---|---|---|---|
| Bound host workflow | `009_host_workflow_binding.sql`; `RuntimeService.bind_host_workflow_turn:5427`, `complete_host_workflow_turn:5736`, `get_host_workflow_binding:5829`; Explorer 1 capability matrix | observed; tests unverified | Per-seat/turn binding, continuity, exact output and conflict constraints are implemented. This does not prove host adoption, provider delivery, authenticated authorship, or that this research dispatch is target-bound. |
| Dispatch workflow | `implementations/server/runtime/dispatch_workflow.py:61,94,231`; Explorer 1 | observed; tests unverified | Opening-record validation and bound launch-plan compilation exist. This is not an end-to-end host launch or recursive expansion engine. |
| One journal | `journal.py:RuntimeJournal.accept:145`, `verify_store:560`; migrations 001–011; Explorer 1 | observed; tests unverified | SQLite acceptance, idempotency/conflict handling, event groups, heads, receipts and verification are implemented. It does not prove complete semantic replay, global recovery, or production operation. |
| Protocol compiler | `protocol_compilation.py:ProtocolCompiler.compile_candidate:368`, `compile_dispatch_candidate:489`; `test_protocol_compilation.py` PC1–PC12; Explorer 1 | **executed** | PC1–PC12 and the frozen golden-manifest test passed, 13/13 in 0.567s. It produces deterministic, closed-schema candidates; it neither confirms, dispatches, reasons, authorizes nor effects. |
| Reference Scout and BUS reveal | `reference_delivery.py:15,45,72,113,200`; `reveal_delivery.py:36,52,106,140`; Explorer 1 | observed; tests unverified | Exact effective-input materialisation and durable service paths exist. Provider effect remains pending; BUS evidence includes a same-seat false-quorum counterexample. |
| APT and projections | `projections.py:ProjectionManager:33`; `service.py:append_apt_event:4224`, `accept_apt_research:6092`; Explorer 1 | observed; tests unverified | Rebuildable projections and an ACI-owned acceptance boundary exist. Projection/ingestion is not authority, prompt use, or semantic reasoning. |
| Operator and Control Center | `operator_recovery.py:51,141,180`; `control_center/api.py:create_router:75`, routes `78–226`; Explorer 1 | observed; tests unverified | Verify/backup/retire and six fail-closed read routes exist. No restore/reinstate, authoritative UI mutation, browser proof, or production service follows. |
| Serving boundary | `main.py:68–76`; `service.py:6289`; Explorer 1 | observed | Production-reader runtime routes are disabled in current composition. This is not a deployment or operational guarantee. |

The broader selected run discovered 22 tests: the same 12 protocol tests
passed, while ten FastAPI-dependent modules could not import because FastAPI
was absent. Those ten are **unverified**, neither passing nor failing; no
dependency was installed. A dependency-complete confirmation → binding →
journal verification remains required. [Explorer 1,
`research.md#validation-executed`; E1]

## Proposal-only RWO and tracked hypotheses

RWO proposes immutable versioned `WorkDefinition`, addressed `WorkRun` and
attempts, a uniform leaf/composite Work envelope, one root expansion,
event-triggered edges, command/event separation, accepted history, a derived
routing cursor, and non-authoritative status projections. Its own central
constraint is recursive composition without nested orchestration authority:
definition graph, expanded run plan, accepted history, routing cursor and
work-owned domain status must remain distinct. These are **proposal claims**,
not target features. [Explorer 2, `research.md#proposal-inventory`; RWO
`DESIGN.md:19–32,54–68,87–146,287–330`; `ONTOLOGY.md:137–187`; E2]

The tracked workflow brief instead remains an unreviewed inquiry into whether
there is one graph at all; the autonomous target proposes that every workflow
graph node is an Agent Node. That conflicts with an RWO `WorkNode` that may be
a gate, join, operation or reusable structural position rather than an agent.
No source resolves which layer owns that distinction. [Explorer 2,
`research.md#hypotheses-and-tensions`, H1 and T1–T5; E2-WG]

## Delta from prior research

The earlier “reader/control-plane UI” classification is directionally useful
but materially incomplete. Current tracked bytes add a governed ACI/APT
runtime, host binding, bound plan compiler, specialised delivery, projections,
recovery mechanics and read-only Control Center; deterministic protocol
compilation now has a fresh local test witness. What did not change is equally
important: target runtime remains orchestration/evidence infrastructure, not
semantic judgment; provider effects, production, full host adoption, executable
RWO, and executable ARE integration remain unproven. [Explorer 1,
`research.md#delta-from-the-historical-inventory-classification`; E1]

## Exact implementation → recursive-work matrix

| Current target precedent | RWO relation | Status | Required discriminator / prohibition |
|---|---|---|---|
| Confirmed dispatch row and compiler, `dispatch_workflow.py:24–28,61–113` | partial `WorkDefinition` analogy | **NARROW** | It may not replace confirmation/registration; needs an accepted definition schema. |
| Bound address `dispatch_id/group_id/seat_index/turn_ordinal/attempt_id`, `host_dispatch_hook.py:42–54` | `WorkRun` identity | **SELECT as identity precedent** | Address is not semantic status or authority. |
| Host hook translation, `host_dispatch_hook.py:332–343,439–512` | leaf executor adapter | **NARROW** | Target conformance required; a host binding is never permission to invoke. |
| Dispatch groups/launch plan, `dispatch_workflow.py:94–181` | composite / graph expansion | **DEFER** | No recursive flattening, boundary projection, or generic event-edge compiler. |
| Declared handoff; `dispatch-sheet.json#connections`; strategy lifecycle `Register and run` | generic sequence | **NARROW** | A typed readiness verdict, not artifact presence, must govern downstream eligibility. |
| Three seats under a parent, `test_host_workflow_binding.py:262–283` | finite fan-out | **SELECT as shape** | Parallel launch does not equal equal judgment, RWO, or shared authority. |
| Declared joins; `dispatch-sheet.json#connections`; RWO `DESIGN.md` §5.3 | generic fan-in | **NARROW / partial** | Requires a typed reconciliation owner and wrong/missing-artifact negatives; arrival/quorum is not reconciliation. |
| Typed handoff label; strategy lifecycle `Register and run`; RWO `DESIGN.md` §5.4 | gate and route | **SELECT as precedent** | Router matches a verdict; it never makes semantic or domain judgment. |
| APT/UI projections, `service.py:655–714` | sidecar | **DEFER**, observational only | Projection may not own lifecycle/status or become a prerequisite route authority. |
| Declared follow-up, `host_dispatch_hook.py:512` | bounded repeat | **NARROW** | Split idempotent redelivery from new attempt; no implicit scope/topology change. |
| ACI command/event lanes, `host_dispatch_hook.py:212–258`, `orchestration_bridge.py:143–248` | protocol precedent | **SELECT** | Transport/persistence is not semantic decision. |
| Current journal | accepted history | **SELECT one owner** | A second integrated RWO/ARE writer is **KILLED**. Generic routing cursor remains deferred. |
| Effect test double, ARE `execute.mjs:150–221` | real effect adapter | **DEFER** | Observed fixed-double witness with prior executable evidence inspected, not freshly executed in this research; requires exact-effect owner, ACI acceptance, adapter and honest-unknown evidence. |

Source and rationale for every row: Explorer 3, `research.md#matrix-a--recursive-work-concept-to-current-orchestrator-ownerwitnessgap`; synthesis verdicts, `synthesis-revision-1.md#current-implementation--recursive-work-verdicts`.

## Exact RWO/orchestrator → ARE matrix

| Typed stage | Conditional producer → consumer and owner split | Status / fail-closed rule |
|---|---|---|
| Reasoning entry | Confirmed Dispatch and bound seat → separately owned `ReasoningEntryVerdict` → mapper | documentation candidate. Missing/stale/mismatched receipt calls no mapper, ACI, actor, evaluator, artifact or effect path. |
| Command and history | Mapper proposes an ACI lifecycle command; ACI alone accepts/rejects and owns one journal | candidate. Unknown schema/digest or cross-run substitution blocks. |
| Journal cut and observations | Verified ACI cut → independently owned observation admission | candidate. Lifecycle record is not automatically an admitted observation. |
| L0 semantics | frozen admitted inputs/rules → bounded evaluator → semantic receipt | **observed bounded local L0 witness; prior promoted/executable evidence inspected; not freshly executed in this research; target/RWO compatibility unverified.** |
| Artifact | semantic receipt → separately owned artifact-admission verdict | **blocked** by `GAP-ARE-ART-001`; no invented owner evidence. |
| Effect | exact envelope → separately owned exact-effect verdict → proposed ACI effect intent | candidate. Recommendation or gate pass alone does not attempt an effect. |
| Replay/revalidation | immutable exact inputs → semantic replay; changed present state → new revalidation run | observed bounded local replay witness; prior executable evidence inspected, not freshly executed in this research; integrated ReplayBridge **deferred**. Replay makes zero mutable/external calls and cannot refresh authority. |
| L1–L3 | L0 receipt → later protocol/integration/effect layers | **deferred** pending ACI/Bus/ACP/APT maturity, conformance and owner receipts. |

Direct evidence: Explorer 3, `research.md#matrix-b--exact-reasoning-engine-integration-bindings`; typed entry controls and fixture F5–F8,
`synthesis-revision-2.md#typed-reasoning-entry-boundary` and
`#eight-executable-discriminating-fixtures`; E3/C1.

## Integration topology verdicts

- **SELECT, documentation analysis only:** a bounded evaluator adjacent to
  typed gates. `execute.mjs:102–123` is an observed local zero-evaluator-call
  non-pass witness with prior executable evidence inspected, not freshly
  executed in this research; `125–183` retains a distinct exact-effect decision.
- **NARROW:** ARE as an ACI-subordinate leaf facade accepting one addressed,
  immutable reasoning command and returning lifecycle events plus a semantic
  artifact reference. It must not write another journal or emit an effect.
- **NARROW:** a read-only audit/replay sidecar, only when its output is
  non-authorizing and cannot release routing/effects.
- **DEFER:** ARE as `CompositeWork`, generic RWO sidecars/fan-in/cursor/repeat,
  an integrated ReplayBridge, and all executable cross-repository seams.
- **KILL:** a second scheduler, a second integrated journal, orchestrator-owned
  semantic judgment, evaluator-owned effect authority, routing-as-reasoning,
  and a result/recommendation-as-authorization path. [Explorer 3,
  `research.md#topology-verdicts-with-finite-witnessescounterexamples`; K1]

## Smallest safe documentation-only contract

1. Pin orchestrator commit, RWO proposal hashes, ARE/ACI architecture hashes,
   evaluator and schema versions; declare `authority_effect: none`.
2. Define immutable envelopes for Dispatch/digest, bound seat, precommitted
   proposed command/digest, verified journal cut, admitted observations,
   semantic receipt/artifact, exact-effect envelope, ACI effect intent and
   observed outcome.
3. Name a distinct source, lifecycle, semantic, entry/artifact/effect-gate,
   artifact, effect and promotion owner for each edge; unselected owners block.
4. Persist `ReasoningEntryVerdict` before mapping. A pass permits only mapping
   and proposal to ACI; it does not accept a command. A block terminates the
   subject, with zero downstream calls and no writes except the valid owner’s
   receipt.
5. Require distinct ACI conformance, ARE invocation compatibility,
   artifact-admission, typed-gate and runtime receipts. Unknown versions,
   missing digests, stale context and cross-run substitution fail closed.
6. Keep historical replay (immutable, zero mutable/external calls) distinct
   from new current revalidation. [Explorer 3,
   `research.md#smallest-safe-documentation-only-integration-contract`;
   `synthesis-revision-2.md#typed-reasoning-entry-boundary`; C1]

## Negative controls and validation still required

The following are explicit controls, not optional cautions: host binding does
not confer parent dispatch authority; proposal is not implementation; a route
label is not a semantic verdict; accepted journal history is not evaluator
admission or domain status; a projection is not source lifecycle; semantic
recommendation is not authorization; exact-effect pass is not ACI acceptance;
and neither replay nor redelivery is new revalidation/attempt. [Explorer 3,
`research.md#smallest-safe-documentation-only-integration-contract`; Quine PASS,
`review-final.md#final-reviewer-gate`]

Before selecting implementation, execute F1–F8 from
`synthesis-revision-2.md#eight-executable-discriminating-fixtures`: a
dependency-complete target lifecycle run; recursive A→readiness→B with
wrong/missing artifacts; semantic fan-in reconciliation; sidecar independence;
entry non-pass zero-call/write-set checks; L0-positive/effect-non-pass and ACI
rejection; replay versus revalidation; and owner-receipt substitution/missing
owner tests. Also obtain cross-owner schemas, conformance receipts, a recursive
compiler/reducer, and owner-approved artifact/effect adapters. [Gödel PASS,
`review-final.md#final-reviewer-gate`; C1]

## Complete open residue

| Identifier | Unresolved question | Owner to resolve | Integration / implementation impact |
|---|---|---|---|
| RWO-OQ-001 | journal authoritative state versus durable copied evidence | RWO/work-state and journal owner | reconciliation, replay, conflict ownership |
| RWO-OQ-002 | dynamic graph extension and confirmation | confirmation/Dispatch authority owner | prevents silent topology expansion |
| RWO-OQ-003 | cross-host delivery guarantees | protocol/adapter/storage owner | delivery and idempotency architecture |
| RWO-OQ-004 | cancellation and compensation combinators | work-policy owner | kernel surface and recovery semantics |
| RWO-OQ-005 | structural `quorum(n)` versus gate work | coordination/semantic-governance owner | prevents readiness being mistaken for judgment |
| RWO-OQ-006 | schema/reducer migrations | versioning/replay owner | historical meaning and deterministic resume |
| RWO-OQ-007 | minimum verifiable authority reference | authorization/effect-boundary owner | kernel must not own authorization policy |
| RWO-OQ-008 | sufficient bounded-pipeline counterexamples | validation/evidence owner | expressiveness claim ceiling |
| RWO-OQ-009 | long-lived stream versus separate subscription | Work-contract owner | closure of uniform Work |
| RWO-OQ-010 | promotion owner | canonical-definition/promotion owner | prevents accidental authority |
| Ontology residue 011 | event-class location | ontology source owner, then relevant contract owner | event semantics remain unassigned |
| Ontology residue 012 | mapping purity | ontology source owner, then relevant contract owner | prevents covert input/authority transformation |
| Ontology residue 013 | executor-adapter ownership | ontology source owner, then relevant contract owner | prevents duplicate lifecycle/effect owner |
| Ontology residue 014 | relation transitivity | ontology source owner, then relevant contract owner | prevents invalid graph/authority inference |
| WGQ-1 | graph/state structure count | workflow-graph discovery owner | canonical lifecycle authority partition |
| WGQ-2 | node meaning | workflow taxonomy owner | whether task/gate/operation/outcome are nodes |
| WGQ-3 | node/agent/seat/attempt cardinalities | identity/runtime-domain owner | retry/reuse without collisions |
| WGQ-4 | node and edge taxonomy | protocol/workflow schema owner | executable closed schemas and behavior |
| WGQ-5 | workflow versus communication | workflow and Bus Contracts owners | prevents duplicate routing/permission authority |
| WGQ-6 | collective coordination | group/coordination owner | quorum, dissent, budgets, collective result |
| WGQ-7 | completion model | Run/audit/closure owner | separates attempt end, outcome, terminal fact, audit close |
| WGQ-8 | rework under a DAG | workflow state/retry owner | bounded loops, generations, replay |
| WGQ-9 | compilation and confirmation | protocol compilation + confirmation + Dispatch owners | total mapping, lineage, fail-closed authority |
| WGQ-10 | simplified views | projection/UI/telemetry owner | views remain derivable and non-authoritative |

Source for every row: Explorer 2, `research.md#open-question-matrix`.

Cross-owner blockers are: unselected reasoning-entry/artifact/exact-effect
owners; `GAP-ARE-ART-001`; unaccepted command/cut/artifact/effect schemas;
ARE invocation/runtime compatibility; ACI/Bus/ACP/APT conformance; catalog
applicability/precedence and challenge-closure owners; no recursive compiler or
fixtures; and incomplete target test environment. [Explorer 3,
`research.md#open-owner-decisions--explicit-residue`; Explorer 1,
`research.md#blockers-and-residue`]

## Reviewer verdict matrix

| Gate | Verdict | What the final review established | What it did not establish |
|---|---|---|---|
| Precedent / ownership — Lakatos | **PASS** | Confirmation/host binding stay target-owned; one ACI journal is preserved; entry, artifact and effect owners are separate/unselected. | Present allocation, executable seam, promotion or adoption. |
| Non-vacuity — Gödel | **PASS** | F1–F8 have frozen inputs, ordered positive/negative observations, zero-call/no-write assertions, terminal/replay expectations and evidence tiers. | Execution of those future fixtures. |
| Definitions / authority — Quine | **PASS** | `ReasoningEntryVerdict` is uniquely before mapping/ACI; cursor, replay, lifecycle, semantic, artifact, effect and execution are non-interchangeable. | A production vocabulary or runtime conformance. |

Source: `review-final.md#final-reviewer-gate`; terminal receipts
`receipts/reviewer-precedent.json`, `receipts/reviewer-non-vacuity.json`, and
`receipts/reviewer-definitional.json` (all `status: pass`, `validation: pass`).
