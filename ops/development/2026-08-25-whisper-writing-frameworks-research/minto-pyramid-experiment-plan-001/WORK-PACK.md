---
module: minto-pyramid-experiment-001
version: proposal-001
status: candidate
updatedAt: 2026-08-25
docType: work-pack
---

# WORK-PACK: Minto Pyramid experiment L0

## Purpose

Canonical proposal-only execution plan for one candidate-specific Minto Pyramid non-vacuity experiment. It prepares an exact three-SWU frontier; it does not select or execute a unit.

## Control fields

| Field | Value | Notes |
|---|---|---|
| workPackId | `WP-MPX-001` | Stable local identity. |
| workPackGateStatus | `pass` | Plan shape passes Distill and exact proof-only readiness checks; execution remains separately blocked. |
| complexity | `medium` | Three independently verifiable SWU outcomes with a multi-artifact human handoff chain. |
| outputMode | `split` | Task and wave contracts are separate. |
| executionPackRef | `EXECUTION-PACK.md` | Required wave choreography. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0–L3 governance lens. |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.json` | Required technique trace. |
| distillValidationStatus | `pass` | Final Balancer review resolves all seven recorded objections with no new objection. |
| swuAtomicityStatus | `pass` | Three one-behavior SWUs recompose without hidden glue; the human chain is one interruption-sensitive transaction. |
| firstUnitNarrownessStatus | `pass` | Initial and final Balancer reviews confirm SWU-MPX-001 is the narrowest reversible first unit. |
| closeoutSyncStatus | `pass` | Every SWU has an exact owner route, inventory, baseline rule, delta set, receipt, and successor. |
| executionDesignation | `execution-candidate` | Mutation-capable future experiment artifacts. |
| implementationReadinessStatus | `pass` | Exact final WPRA and proof-only Implementation Readiness receipt pass without mutation or authority. |
| implementationReadinessReceiptRef | `IMPLEMENTATION-READINESS-PREFLIGHT.json` | Non-reusable, non-mutation-ready, authority-free proof receipt. |
| finiteStreamSupervisorMode | `accepted-finite-stream` | Activation requires later exact acceptance. |
| finiteStreamRequestBudget | `3` | Equals the ordered frontier length. |
| finiteStreamRiskCeiling | `bounded-write` | Repository-local experiment evidence only. |
| exactAcceptanceStatus | `unapproved` | This proposal does not accept itself. |
| admissionTiming | `selected-unit-at-task-session` | Material packages are future unit-local products. |
| executionEntryState | `blocked` | Exact final-plan acceptance and fresh direct execution intent are both explicitly unsatisfied. |
| allowedRoutesDigest | `2873588eb4e70878365b2735f6b14ffed822b644d93121904c1c6b7fa9dae651` | Generated from the exact three Task Session routes; Invoke closeout paths are excluded from Task Session write scopes. |
| activeLayerWindow | `L0` | L1–L3 are deferred. |
| lastUpdatedAt | `2026-08-25T20:42:02Z` | Proposal authoring time. |
| readinessProfile | `pilot` | One feasibility witness only. |

## Objective summary

- Objective: determine whether selecting one declared governing-point support hierarchy changes that one composition-plan decision, prevents `support-association-not-declared`, and yields one complete non-vacuity witness while staying inactive for a discovery-led boundary case.
- Primary inputs: accepted findings, repaired closeout, owner candidate decision, `IMPLEMENTATION-PLAN.md`, and `IMPLEMENTATION-LAYERING.md`.
- Success condition: three exact, sequential artifacts close the source, mechanical, human-semantic, counterexample, and authority boundaries and yield `pass`, `fail`, or `inconclusive` without reader-effect claims.

## Execution policy boundary

- Route policy: automatic only for exact in-scope internal routing after later owner acceptance and direct execution intent.
- Automatic decisions: internal tool selection, capability-owner routing, reversible local defaults, and fresh Task Session resumption.
- Stop decisions: product or semantic choice; scope expansion; destructive or irreversible effect; credentials or secret access; external message or network effect; cost or risk acceptance; authority, promotion, publication, or deployment; failed acceptance-critical validation.
- Effect class: `repository-local-reversible` only.
- Authority effect: `none`.
- Human semantic review in SWU-MPX-003 is a stop decision until a human supplies the bounded review; no agent may fabricate it.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
|---|---|---|---|---|---|
| S-MPX-01 | Source-bound controlled case and mandatory review views exist. | L0 | [W0](work-pack/waves/W0-CASE.md) | none | Closed shape, exact span-set control, nonempty groups, content-preserving views, and inactive untransformed boundary. |
| S-MPX-02 | Declared mechanics are validated without semantic claims. | L0 | [W1](work-pack/waves/W1-MECHANICS.md) | SWU-MPX-001 | Every named mechanical check passes and binds exact case bytes. |
| S-MPX-03 | Role-label-blind human review issues the bounded witness verdict. | L0 | [W2](work-pack/waves/W2-REVIEW.md) | SWU-MPX-002 | Commitment, self-sufficient role-neutral packet context/prompts, response, reveal chronology, actual-byte bindings, human fields, verdict rule, and ceilings enforced. |

## Task status board

| Task | Goal | Layer | Wave | Source | Gate | Status |
|---|---|---|---|---|---|---|
| [TASK-MPX-001-CASE](work-pack/tasks/TASK-MPX-001-CASE.md) | Author the controlled case. | L0 | W0 | `IMPLEMENTATION-PLAN.md#SWU-MPX-001` | blocked pending acceptance | not-started |
| [TASK-MPX-002-MECHANICS](work-pack/tasks/TASK-MPX-002-MECHANICS.md) | Validate declared mechanics only. | L0 | W1 | `IMPLEMENTATION-PLAN.md#SWU-MPX-002` | blocked on SWU-MPX-001 | not-started |
| [TASK-MPX-003-REVIEW](work-pack/tasks/TASK-MPX-003-REVIEW.md) | Run role-label-blind human review and issue the witness verdict. | L0 | W2 | `IMPLEMENTATION-PLAN.md#SWU-MPX-003` | blocked on SWU-MPX-002 and human input | not-started |

## SWU manifest

Machine view: `work-pack/SWU-MANIFEST.json`.

| SWU | Parent | Primary behavior | Dependencies | Write scope | Acceptance boundary | Owner | Status |
|---|---|---|---|---|---|---|---|
| SWU-MPX-001 | [TASK-MPX-001-CASE](work-pack/tasks/TASK-MPX-001-CASE.md) | Materialize one source-bound controlled case. | none | future case, precloseout, and Task Session receipt; Invoke closeout is separate | Case and mandatory views pass actual-byte structural and span-control checks. | `subagent` with Task Session fallback | not-selected |
| SWU-MPX-002 | [TASK-MPX-002-MECHANICS](work-pack/tasks/TASK-MPX-002-MECHANICS.md) | Validate only declared mechanics. | SWU-MPX-001 closeout | future mechanical, precloseout, and Task Session receipt; Invoke closeout is separate | Actual case bytes are revalidated, exact check IDs pass, and no semantic authority is claimed. | `local-fallback` | not-selected |
| SWU-MPX-003 | [TASK-MPX-003-REVIEW](work-pack/tasks/TASK-MPX-003-REVIEW.md) | Obtain human semantic judgment and issue the bounded witness verdict. | SWU-MPX-002 closeout | future commitment, packet, response, witness, precloseout, and Task Session receipt; Invoke closeout is separate | The exact role-label-blind chain and verdict rule close without reader or integration claims. | `manual` inside Task Session | not-selected |

## SWU atomicity review

| SWU | Candidate child units | Retained-boundary rationale | Verdict |
|---|---|---|---|
| SWU-MPX-001 | source binding; positive pair; counterexample | These fields form one case contract and cannot be validated as a candidate-specific witness input when separated. | proposed-pass |
| SWU-MPX-002 | syntax check; span control; boundary flags | All are mechanics-only checks over one exact case and share one independent validation receipt; semantic review is already separate. | proposed-pass |
| SWU-MPX-003 | commitment/packet preparation; human response; reveal/verdict calculation | None is independently meaningful as an experiment outcome. The response must bind the precommitted packet, and the candidate verdict must bind the response and reveal; interruption before reveal restarts the whole SWU. | pending-revalidation |

SWU-MPX-001 is the narrowest reversible trust-building step because it creates only the controlled input and can be rejected before any validation or human review output exists.

## Task Session closeout synchronization

Shared rules:

- Lifecycle owner route: `invoke:refresh:apply-approved`, closeout-only.
- Task Session may write only declared material, its precloseout receipt, and its terminal receipt. Invoke alone may write the closeout receipt and lifecycle status targets; these write scopes are disjoint.
- Baseline binding: capture SHA-256 and size for every declared owner target immediately before closeout and require equality with the Task Session admission snapshot except for the exact admitted delta.
- Allowed delta classes: `evidence_added`, `status_changed`, `route_changed`, `blocker_opened`, `blocker_resolved`.
- Forbidden: new experiment semantics, another SWU, authority change, promotion, publication, deployment, destructive cleanup, or unrelated targets.
- Owner receipt schema: `invoke.precloseout-refresh-closeout-receipt.v1`.

| SWU | Terminal source receipt | Owner target inventory | Owner validation | Expected owner receipt | Successor |
|---|---|---|---|---|---|
| SWU-MPX-001 | `../minto-pyramid-experiment-001/receipts/SWU-MPX-001.task-session.json` | this Work Pack; `EXECUTION-ENTRY.json`; unit case, precloseout, terminal, and closeout paths | validate exact target inventory, baseline, case JSON, receipt schema, and successor | `../minto-pyramid-experiment-001/closeouts/SWU-MPX-001.invoke-refresh.json` | SWU-MPX-002 only |
| SWU-MPX-002 | `../minto-pyramid-experiment-001/receipts/SWU-MPX-002.task-session.json` | this Work Pack; `EXECUTION-ENTRY.json`; unit mechanical, precloseout, terminal, and closeout paths | validate exact target inventory, baseline, mechanical receipt, dependency closeout, and successor | `../minto-pyramid-experiment-001/closeouts/SWU-MPX-002.invoke-refresh.json` | SWU-MPX-003 only |
| SWU-MPX-003 | `../minto-pyramid-experiment-001/receipts/SWU-MPX-003.task-session.json` | this Work Pack; `EXECUTION-ENTRY.json`; commitment, packet, response, witness, precloseout, terminal, and closeout paths | validate exact target inventory, baseline, actual-byte review chain and chronology, dependency closeout, and terminal completion | `../minto-pyramid-experiment-001/closeouts/SWU-MPX-003.invoke-refresh.json` | `__complete__` only |

Machine view: `work-pack/shared/CLOSEOUT-CONTRACTS.json`.

## Validation strategy

Machine view: `work-pack/shared/VALIDATION-CONTRACTS.json`.

- All commands are exact argv arrays at repository-root cwd.
- JSON syntax and declared mechanical invariants are executable through the exact plan-owned validator over actual files.
- Every predecessor path, SHA-256, and size is recomputed; self-reported receipt bindings cannot pass alone.
- Truth, fairness, equivalence, genre fit, hierarchy plausibility, and boundary-form appropriateness are human checks performed from the closed packet alone; its role-neutral context, instructions, and prompts are exact validator inputs.
- Failed checks retain their failure; a later successful command cannot mask them.
- No validation command executes during Work-Pack readiness audit.

## Dispatch technique trace

Machine view: `DISPATCH-TECHNIQUE-TRACE.json`.

The route uses sequence, SCU/SWU reduction, recomposition proof, validation loop, owner boundary checking, handle handoff, residue ledger, execution-receipt handoff, authority split, concrete path evidence, and a bounded delegation boundary for Distill review.

## Distill validation

`PLAN-DISTILL-VALIDATION.json` records the initial independent block, two bounded repair cycles, and the final independent `pass` over these conditions:

- all three SWUs are atomic;
- SWU-MPX-001 is the narrowest reversible first unit;
- the three units recompose into exactly one L0 witness;
- no hidden reader study or integration step exists;
- navigation from this Work Pack to every task, wave, source, write scope, and validation contract is exact.
- Task Session and Invoke write scopes are disjoint and exact acceptance/direct execution remain explicit prerequisites.

## Resolved plan gates

| ID | Result | Evidence |
|---|---|---|
| B-MPX-001 | resolved | `PLAN-DISTILL-VALIDATION.json` final verdict is `pass`; recomposition, navigation, packet self-sufficiency, and authority checks pass. |
| B-MPX-002 | resolved | Final WPRA reports `PLAN_SEMANTIC_READY`; `IMPLEMENTATION-READINESS-PREFLIGHT.json` reports `PLAN_IMPLEMENTATION_READY`. |

## Remaining owner and execution gates

| ID | Class | Description | Owner | Repair path |
|---|---|---|---|---|
| G-MPX-001 | downstream gate | Exact owner acceptance of final candidate bytes is absent. | Decision Gate / owner | Generate a separately governed exact acceptance request after all prerequisite closure evidence exists. |
| G-MPX-002 | execution gate | No direct execution intent or unit selection exists. | Owner / Implementation Readiness | Remains intentionally absent in proposal-only mode. |

## Required links

- `PLANNING-CONTEXT.md`
- `IMPLEMENTATION-PLAN.md`
- `IMPLEMENTATION-LAYERING.md`
- `EXECUTION-PACK.md`
- `DISPATCH-TECHNIQUE-TRACE.json`
- `work-pack/SWU-MANIFEST.json`
- `work-pack/shared/VALIDATION-CONTRACTS.json`
- `work-pack/shared/CLOSEOUT-CONTRACTS.json`
- `EXECUTION-ENTRY.json`
- `PLAN-DISTILL-VALIDATION.json`
- `IMPLEMENTATION-READINESS-PREFLIGHT.json`

## Claim and authority ceiling

This Work Pack is a proposal. It does not prove Minto Pyramid improves writing, readers, or outcomes; does not satisfy the non-vacuity witness before execution; does not adopt a framework; and does not authorize any Whisper, Arcanum, Git, promotion, publication, deployment, release, or production change.

## Change log

| Date | Change | Author |
|---|---|---|
| 2026-08-25 | Initial proposal-only execution candidate drafted. | Invoke Plan |
| 2026-08-25 | Reconciled Distill blocks, closed actual-byte and human-packet contracts, separated lifecycle scopes, and froze proof-only readiness. | Invoke Plan |
