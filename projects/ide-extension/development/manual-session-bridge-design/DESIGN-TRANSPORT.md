---
id: ide-extension-manual-session-bridge-design-transport
project: ide-extension
title: "Manual Session Bridge Design Transport"
status: approved
node_type: design-transport
updatedAt: 2026-07-12
observed_capability: invoke
invoke_mode: design
---

# Design Transport: Manual Codex Session Bridge

## Target Artifact Provenance

| Field | Value |
| --- | --- |
| Observed capability | `invoke` |
| Invoke mode | `design` |
| Target artifact | Manual Codex Session Bridge architecture bundle |
| Target type | Neutral repository feature/integration design |
| Lifecycle owner | `projects/ide-extension` |
| Output root | `projects/ide-extension/development/manual-session-bridge-design/` |
| Runtime mutation | none |
| Recommended next route | `invoke plan` when requested |

## Bounded Context Selection

The design used only:

- ide-extension top-level spec and architecture;
- current envelope, receipt, constructor, projector/server, workbench, and
  focused runtime/UI test contracts;
- the live blind-poll projection and selected skill hash summarized in
  [EXPERIMENT-EVIDENCE.md](EXPERIMENT-EVIDENCE.md);
- the existing browser-first design package as a project-local package pattern;
- Invoke design mode, DomainSpec architecture bundle, candidate UX plan, and
  Dispatch Spec technique contracts.

It did not ingest external service docs, provider APIs, VSCodium browser APIs,
Chrome extension code, Kernel Cloud, OpenClaw, Hermes, or unrelated repository
architecture. Those are not required to design the selected manual bridge.

## Approved Design Intent

The operator selected:

> Manual current-session bridge first. After browser approval, the operator
> says `poll`; the active Codex session claims and runs the request. Persistent
> worker behavior is deferred.

The follow-up decision gate in [DECISIONS.md](DECISIONS.md) resolves the five
remaining blocker-level choices for effect scope, receipt semantics, recovery,
session assurance, and multiple-request targeting.

## Template And Profile Selection

| Candidate | Eligibility | Selection |
| --- | --- | --- |
| DomainSpec architecture profile | Existing `SPEC.md` and `ARCHITECTURE.md`; cross-component state/interface change; six views required. | selected |
| Candidate UX plan | The experiment failed to expose the proposal task clearly; operator journey and state language affect correctness. | selected as invoke-local companion |
| Research family | No external factual claim or unresolved evidence dependency is required. | skipped |
| Spell/sigil family | Target is a repository feature, not a spell or sigil lifecycle. | skipped |

The UX template remains candidate/invoke-local and is not promoted by this run.

## Dispatch Spec Technique Trace

| Technique | Activation and concrete effect |
| --- | --- |
| `sequence` | Orders evidence capture -> design synthesis -> boundary validation -> Distill -> plan handoff. |
| `concrete_path_evidence` | Binds claims to current schemas/server/UI/tests and this package's artifacts. |
| `frame_handoff` | Passes the bounded experiment/context frame into architecture synthesis. |
| `owner_boundary_check` | Keeps approval/receipt authority in the kernel and skill execution in Codex. |
| `delegation_boundary` | Defines the late-disclosure claim packet as the bounded handoff to the active session. |
| `authority_split_gate` | Separates lifecycle, approval, execution, validation, evidence, and promotion owners. |
| `approval_semantics_map` | Prevents human authorization from being mislabeled as successful skill execution. |
| `state_namespace_boundary` | Separates browser input, kernel state/artifacts, session context, and installed skill sources. |
| `execution_receipt_handoff` | Requires the session result to return to the kernel before terminal completion is claimed. |
| `artifact_contract_bridge` | Maps claim/result contracts to schemas, artifacts, projection, and UI evidence. |
| `validation_loop` | Requires fixture, hostile, recovery, and Playwright evidence before promotion. |
| `residue_ledger` | Preserves session identity, recovery, sandbox, and spec delta gaps with owners. |
| `scu_swu_reduction` | Selects one read/preview request as the smallest coherent design unit. |
| `recomposition_proof` | Shows how that unit extends the existing kernel without adding another authority. |
| `handle_handoff` | Routes the next owner through package paths rather than copied session transcript. |

Full dispatch required: yes. The route crosses the Approval Desk/kernel,
current Codex session, and installed skill capability boundary and carries a
human approval plus execution receipt handoff.

Dispatch artifact:
[manual-session-bridge.dispatch.json](manual-session-bridge.dispatch.json).

## Design Decisions

| Decision | Status | Source |
| --- | --- | --- |
| Manual poll before persistent worker. | approved | operator answer `1 we should this first poll thing` |
| Skill remains unresolved by server and undisclosed until claim. | approved design consequence | blind experiment goal and result |
| Approval and execution produce separate typed receipts. | approved | `DECISIONS.md` DG-MSB-002 |
| First bridge is read/preview-only. | approved | `DECISIONS.md` DG-MSB-001 |
| Interrupted claims require explicit operator release/requeue. | approved | `DECISIONS.md` DG-MSB-003 |
| Session assurance remains unattested. | approved | `DECISIONS.md` DG-MSB-004 |
| Exactly one proposal is marked ready in the desk before poll. | approved | `DECISIONS.md` DG-MSB-005 |
| Visible required Proposal task replaces generic default. | required UX repair | experiment submitted the default task accidentally |

## Upstream Patch Requests

No upstream artifacts were edited in this design run. The next approved plan
must account for these deltas:

1. `SPEC.md`: add a bounded manual-session bridge layer/slice and preserve
   no-autonomous-execution language.
2. Agent envelope/approval schemas: add approved/ready/claimed/interrupted
   transitions and delay approval consumption until terminal result.
3. Receipt semantics: add typed `authorization.receipt` and `skill.execution`
   receipts without conflating their claims.
4. Grant vocabulary: add `skill.invoke` while keeping L0 execution
   `preview.read` only.
5. Approval Desk UX: visible required task, truthful receipt copy, singleton
   ready target, operator release/requeue, and claim/result evidence.

## Gap Ledger

| Gap | Class | Owner | Repair route | Plan effect |
| --- | --- | --- | --- | --- |
| Existing spec does not name the manual bridge. | target artifact | ide-extension owner | approve spec delta in plan/task route | first plan slice |
| Approval currently terminalizes as passed. | target artifact | schema/projector/server | typestate migration | blocks execution until fixed |
| No target/claim/release/result schemas or endpoints. | target artifact | ide-extension bridge | implementation plan | core L0 work |
| Session identity is unattested. | target artifact | future identity/executor design | L2/L3 | explicit limitation, not L0 blocker |
| Timed lease and automatic reclaim are absent. | target artifact | bridge reliability | L1 | operator recovery is accepted for L0 |
| Current session effects are not technically sandboxed. | target artifact | executor adapter | L2 | blocks write/network grants |
| Invoke template has no dedicated session-bridge family. | invoke-specific | Invoke development cycle | workflow reflection only if pattern repeats | no current block |

## Distill Validation

- Selected unit: one approved read/preview request through desk target selection,
  explicit poll, claim, late disclosure, operator recovery when interrupted,
  execution, and result receipt.
- Recomposition target: existing ide-extension envelope/approval/event/artifact
  kernel and HTML workbench.
- Hidden acceptance-critical gaps: approval/execution conflation and missing
  result admission are surfaced as first-slice obligations.
- Deferred complexity: worker, authenticated identity, timed/automatic recovery,
  sandboxed mutation, IDE, browser, provider, and remote adapters.
- Verdict: `pass` for design-unit coherence.

## Transport And Observability

- Plan context readiness: package paths, source anchors, state/interface rules,
  validation surfaces, gaps, and owner boundaries are explicit.
- Necronomicon transport: skipped; no matching target section was required or
  mutated.
- Observability: this package and dispatch id provide the design trace. No
  runtime execution signal is claimed by Invoke.

## Gate Status

| Gate | Result | Note |
| --- | --- | --- |
| Core goal and actor known | pass | human operator and active Codex session are explicit |
| Six design views | pass | architecture bundle contains all six |
| UX workflow | pass | task discoverability and lifecycle language are specified |
| Glossary consistency | pass | accepted typed receipt and consumption deltas are named |
| Dispatch technique trace | pass | full dispatch validated with `VALIDATION=pass` |
| Distill design-unit check | pass | smallest unit and split pressure are explicit |
| Decision gate | pass | five blockers resolved in `DECISIONS.md`; no override |
| Plan activation | pass | approved design and upstream delta ownership are explicit |

## Next Route

Route this approved package to `invoke plan` when planning is requested. Plan
mode should produce a split work-pack if the schema, projector, server, UI,
test, and real manual-witness changes exceed the low-complexity threshold.
Source mutation then proceeds through `task-session`, one SWU at a time.
