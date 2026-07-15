---
id: ide-extension-domainspec-roadmap-lab-work-pack
project: ide-extension
status: ready
updatedAt: 2026-07-14
docType: work-pack
planning_gate_status: pass
active_layer: L0
---

# Work Pack: DomainSpec v2 Roadmap Lab

## Control

| Field | Value | Note |
| --- | --- | --- |
| workPackGateStatus | pass | Structural plan/Distill/dispatch checks pass; mutation still requires one selected SWU. |
| complexity | medium | Brownfield private projection plus shared IDE runtime and real human gate. |
| outputMode | split | Seven task contracts, five waves, shared execution context. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Required choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | Governing L0–L3 decisions. |
| dispatchTechniqueTrace | [PLAN-TRANSPORT.md](PLAN-TRANSPORT.md) | Validated route and technique use. |
| distillValidationStatus | pass | [DISTILL-PLAN-VALIDATION.md](DISTILL-PLAN-VALIDATION.md). |
| activeLayerWindow | L0 | First proof only. |
| executionSelection | none | Task Session must select exactly one ready SWU. |
| readinessProfile | trusted-local-newcomer-pilot | Not general production. |

## Objective

Deliver and prove a proposal-first Roadmap Lab where a newcomer understands
FPR-01, inspects its evidence trail, submits a durable bound proposal, sees an
honest review state, and can witness one accepted presentation-copy update
through rebuild and republish.

Primary inputs are the approved
[architecture](ARCHITECTURE-BUNDLE.md), [UX plan](UX-PLAN.md),
[decisions](DESIGN-DECISIONS.md), and live brownfield contracts summarized in
[shared context](work-pack/shared/context.md).

## Delivery Slices

| Slice | Outcome | Layer | Wave | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Stable copy and semantic-event oracles exist before behavior changes. | L0 | [W0](work-pack/waves/W0.md) | schema/fixture contract suites |
| S-002 | FPR-01 builds deterministically and works through the focused Roadmap Lab route. | L0 | [W1](work-pack/waves/W1.md) | builder, Node, Canvas regression, Playwright witness |
| S-003 | All rendered targets are covered and proposal history handles revision/restart/stale cases. | L1 | [W2](work-pack/waves/W2.md) | coverage, replay, restart, representative browser cases |
| S-004 | Proposals classify to correct owners and failed/unsupported paths preserve authority. | L2 | [W3](work-pack/waves/W3.md) | routing fixtures, receipt-reference checks, denial/retry tests |
| S-005 | Victor completes the real trial and one accepted copy proposal is applied with evidence. | L3 | [W4](work-pack/waves/W4.md) | human report, owner receipt, diff/build/new revision, closeout audit |

## Task Board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-RDL-CONTRACTS](work-pack/tasks/TASK-RDL-CONTRACTS.md) | Define copy and semantic-event oracles. | L0 | W0 | W0 pass | completed |
| [TASK-RDL-BUILDER](work-pack/tasks/TASK-RDL-BUILDER.md) | Extract presentation copy and deterministic build bindings. | L0 | W1 | SWU-003 and SWU-004 pass | completed |
| [TASK-RDL-GUIDED-SURFACE](work-pack/tasks/TASK-RDL-GUIDED-SURFACE.md) | Implement FPR-01 guided UI and focused IDE route. | L0 | W1 | SWU-006 blocked by IDE dirty-scope decision | blocked |
| [TASK-RDL-HISTORY](work-pack/tasks/TASK-RDL-HISTORY.md) | Prove repeatability, history, restart, and stale projection. | L1 | W2 | blocked by W1 | not-started |
| [TASK-RDL-GOVERNED-HANDOFF](work-pack/tasks/TASK-RDL-GOVERNED-HANDOFF.md) | Build owner-classified review packets and receipt-backed dispositions. | L2 | W3 | blocked by W2 | not-started |
| [TASK-RDL-ROUNDTRIP](work-pack/tasks/TASK-RDL-ROUNDTRIP.md) | Prove degraded behavior and one accepted copy application. | L2/L3 | W3/W4 | blocked by 010; 012 also needs owner acceptance | not-started |
| [TASK-RDL-VERIFY](work-pack/tasks/TASK-RDL-VERIFY.md) | Run Victor trial and audit pilot readiness. | L3 | W4 | blocked by W3 and real participant | not-started |

## SWU Execution Manifest

The task files contain full implementation rules and handoff notes. This table
contains every gate-bearing execution field required for selection.

| SWU | Parent/source | Dependencies | Exact write scope | Done criteria | Acceptance evidence | Validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-RDL-001 | [Contracts](work-pack/tasks/TASK-RDL-CONTRACTS.md); design RDL-D04 | none | new visibility copy schema/data fixtures/tests only | stable field/node/role contract rejects invalid identity and authority mixing | [PASS: schema plus 1 valid/6 invalid fixtures and 5 focused tests](task-sessions/20260714T215441Z-swu-rdl-001/TASK-SESSION-RESULT.md) | scoped Python contract tests + schema validation | local-fallback | completed |
| SWU-RDL-002 | [Contracts](work-pack/tasks/TASK-RDL-CONTRACTS.md); architecture semantic events | none | new visibility event schemas/fixtures/tests only | five event types and class variants have strict bounded payload oracles | [PASS: 9 valid fixtures, 8 invalid fixtures, size/canvas-composition checks, and no runtime registration](task-sessions/20260714T215923Z-swu-rdl-002/TASK-SESSION-RESULT.md) | scoped Python/JSON-schema tests | local-fallback | completed |
| SWU-RDL-003 | [Builder](work-pack/tasks/TASK-RDL-BUILDER.md); copy oracle | 001 | visibility `roadmap-copy.json`, builder, template, builder tests, regenerated HTML | migrated human copy is externalized; no hidden required fallback; build remains equivalent | [PASS: 67-field copy map, coverage proof, no fallback strings, regenerated outputs](task-sessions/20260714T221718Z-swu-rdl-003/TASK-SESSION-RESULT.md) | builder unit suite and generated artifact check | local-fallback | completed |
| SWU-RDL-004 | [Builder](work-pack/tasks/TASK-RDL-BUILDER.md); RDL-O01 | 002–003 | visibility builder/template/build metadata tests and regenerated HTML | deterministic fingerprint/manifest/source refs embedded; two builds match | [PASS: normalized build manifest, mutation proof, deterministic double-build hashes](task-sessions/20260714T222610Z-swu-rdl-004/TASK-SESSION-RESULT.md) | builder suite twice + no-absolute-path check | local-fallback | completed |
| SWU-RDL-005 | [Guided surface](work-pack/tasks/TASK-RDL-GUIDED-SURFACE.md); UX journey | 004 | visibility template/copy/build tests/browser fixtures/regenerated HTML | FPR-01 supports orient, learn, restate, source request, propose, retry-safe ack | [PASS: exact postMessages, waiting-for-storage boundary, draft preservation, screenshots](task-sessions/20260714T223345Z-swu-rdl-005/TASK-SESSION-RESULT.md) | builder tests + focused Playwright surface spec | local-fallback | completed |
| SWU-RDL-006 | [Guided surface](work-pack/tasks/TASK-RDL-GUIDED-SURFACE.md); ide Canvas contract | 005 | ide `server.mjs`, `l0.html`, focused route tests, package scripts only if required | dedicated route/mode shows current roadmap, forwards events, hides unrelated Craft context | [BLOCK: IDE dirty-scope overlap with Craft Frontier/Operations v1 requires owner decision](task-sessions/20260714T224609Z-swu-rdl-006/TASK-SESSION-RESULT.md) | focused Node/API/UI/Playwright + existing Canvas suite | local-fallback | blocked-dirty-scope |
| SWU-RDL-007 | [History](work-pack/tasks/TASK-RDL-HISTORY.md); S-003 | 006 | visibility coverage fixtures/tests plus minimal copy data for representative nodes | every rendered interactive target has stable copy/source/event coverage without node-specific forks | coverage report and representative-node browser cases | builder coverage + focused Playwright | local-fallback | blocked-dependency |
| SWU-RDL-008 | [History](work-pack/tasks/TASK-RDL-HISTORY.md); proposal state machine | 007 | ide focused-mode history projection/tests and visibility stale fixtures only | submitted proposals survive refresh/restart projection and mismatches become stale-review-required | replay/restart/stale payload and browser evidence | Node replay + Playwright republish/restart tests | local-fallback | blocked-dependency |
| SWU-RDL-009 | [Governed handoff](work-pack/tasks/TASK-RDL-GOVERNED-HANDOFF.md); RDL-O03 | 008 | new visibility review-packet schema, adapter, fixtures, tests | five proposal classes revalidate and produce correct owner/unsupported packets | valid, tampered, stale, unsupported fixture receipts | scoped adapter/schema tests | local-fallback | blocked-dependency |
| SWU-RDL-010 | [Governed handoff](work-pack/tasks/TASK-RDL-GOVERNED-HANDOFF.md); state transitions | 009 | visibility disposition contract/tests plus ide focused history projection/tests | only evidence-referenced owner dispositions project accepted/rejected/applied states | missing/invalid/valid evidence-reference cases and UI states | schema/adapter + focused Node/Playwright | local-fallback | blocked-dependency |
| SWU-RDL-011 | [Roundtrip](work-pack/tasks/TASK-RDL-ROUNDTRIP.md); L2 exit | 010 | focused template/IDE tests and minimal error/retry source fixes within owned files | bounded, disconnected, duplicate, stale, retry, unsupported paths fail safely and preserve drafts/originals | failure matrix, no-direct-effect review, regression output | scoped negative suites + existing Canvas suite | local-fallback | blocked-dependency |
| SWU-RDL-012 | [Roundtrip](work-pack/tasks/TASK-RDL-ROUNDTRIP.md); RDL-O04 | 011, 013, owner acceptance | accepted field in visibility copy data; regenerated HTML; W4 evidence/task-session result only | accepted copy is applied by owner route, validated, rebuilt, republished, and linked to old/new bindings | owner acceptance, source diff, tests, fingerprints, revisions, before/after | full visibility suite + focused Canvas/browser witness | manual | blocked-human-owner |
| SWU-RDL-013 | [Verify](work-pack/tasks/TASK-RDL-VERIFY.md); UX comprehension gate | 011, real Victor | W4 trial protocol/report/evidence only; no product source | real 30-minute trial retains answers, help/confusion, actionable proposal, and truthful verdict | signed/labeled trial record and stored proposal event | manual protocol review against five questions | manual | blocked-human |
| SWU-RDL-014 | [Verify](work-pack/tasks/TASK-RDL-VERIFY.md); traceability | 012–013 | work-pack status/traceability/gaps plus W4 closeout evidence only | all receipts reconcile; pilot claim is bounded; remaining production gaps named | closeout matrix and no-overclaim verdict | link/status audit + planned suites/evidence review | manual | blocked-dependency |

## Blockers And Gaps

| ID | Type | Scope | State | Owner / treatment |
| --- | --- | --- | --- | --- |
| RDL-GAP-001 | worktree ownership | `SWU-RDL-006` IDE route/kernel files | active blocker | [Decision Gate](task-sessions/20260714T224609Z-swu-rdl-006/DECISION-GATE.md): finish/isolate current IDE Operations/Craft work first, or explicitly authorize composition. Never clean/revert. |
| RDL-GAP-002 | human availability | SWU-013 | deferred until W4 | Victor; return blocked-human if unavailable. |
| RDL-GAP-003 | owner acceptance | SWU-012 | deferred until proposal review | Presentation owner; trial may pass without acceptance, but applied round trip cannot. |
| RDL-GAP-004 | source browsing | L0/L1 | intentionally deferred | Keep copyable paths and source-request events; separate design if resolver becomes necessary. |
| RDL-GAP-005 | identity/collaboration | beyond pilot | intentionally deferred | No authenticated or multi-user claim. |
| RDL-GAP-006 | broader lifecycle effects | graph/Craft/research proposals | intentionally handoff-only | Owner routes validate packets; Roadmap Lab does not execute effects. |

`SWU-RDL-006` is blocked by the active IDE dirty-scope decision. No later SWU is
selectable until this blocker is resolved.

## Dispatch Technique Trace

| Technique | Applied to | Validation expectation | Status |
| --- | --- | --- | --- |
| `sequence` | design -> design Distill -> plan -> plan Distill -> handoff | no phase consumes an unvalidated predecessor | pass |
| `scu_swu_reduction` | one-node L0 and 14 SWUs | each unit is meaningful, bounded, and recomposable | pass |
| `recomposition_proof` | tasks/SWUs -> UX and architecture outcomes | traceability covers every accepted outcome | pass |
| `validation_loop` | every layer/slice/SWU | positive, negative, degraded, or human evidence is named | pass |
| `owner_boundary_check` | browser/session/target owners | no event grants mutation or promotion | pass |
| `state_namespace_boundary` | roadmap/copy/Canvas/review state | writes stay in owned namespaces | pass |
| `residue_ledger` | deferred hardening and human/owner gates | gaps have explicit treatment and no hidden promotion | pass |

## Gate Checks

1. Select exactly one ready SWU before Task Session mutation.
2. Re-run dirty-worktree ownership review for that exact write scope.
3. Preserve private/public boundary; no Roadmap Lab content enters `arcanum/`.
4. Keep W0/W1 on L0; do not pull owner automation or hardening forward.
5. Do not advance a layer without its exit evidence.
6. Preserve existing Canvas regression evidence whenever shared IDE files move.
7. A submitted event never satisfies accepted/applied criteria.
8. Human and owner gates may block; never simulate them.
9. Parallel execution is disabled for overlapping brownfield files. The two W0
   new-file contracts may be reordered, but this plan does not authorize
   concurrent mutation.
10. Distill plan status and dispatch validation must remain pass.

## Result Contract

```yaml
swu_id: SWU-RDL-NNN
result: pass | flag | block | interrupted
files_touched: []
validation: []
blockers: []
handoff_note: concise next state
```

## Next Route

Resolve the `SWU-RDL-006` dirty-scope Decision Gate before running another
Task Session. Recommended route: finish or isolate the current IDE
Operations/Craft work, then rerun `SWU-RDL-006`.
