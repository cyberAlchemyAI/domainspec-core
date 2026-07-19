---
id: ide-extension-open-poll-bridge-refresh-report
project: ide-extension
title: "Invoke Refresh Report - Open Poll Bridge Findings"
status: pass
node_type: refresh-report
updatedAt: 2026-07-16
invoke_mode: refresh
mutation_mode: proposal-only
---

# Refresh Report: Open Poll Bridge Findings

## Identity

- Source session reference: open-poll bridge research dispatch,
  `2026-07-15-ide-extension-open-poll-bridge-research`
- Source evidence:
  - [Open Poll Bridge Findings](../open-poll-bridge-research/findings.md)
  - [Open Poll Bridge Research](../open-poll-bridge-research/research.md)
  - `telemetry/agents/subagents-dispatch.yaml`
- Evidence date: `2026-07-16`
- Refresh scope: convert the open-poll research findings into a proposal-only
  refresh over the completed manual-session-bridge package and current bridge
  runtime surfaces.
- Mutation mode: `proposal-only`
- Target lifecycle owner: `projects/ide-extension`

This refresh does not edit runtime code, tests, schemas, or completed
manual-session-bridge plan status. It creates a handoff-quality delta package
for the next implementation owner.

## Source Signals

| Signal ID | Type | Source | Claim | Confidence | Mutation safety |
| --- | --- | --- | --- | --- | --- |
| `OPB-S1` | `route_changed` | `open-poll-bridge-research/findings.md#verdict` | The next bridge slice should use open singleton availability with claim-bound identity, not a multi-request queue. | high | needs_review |
| `OPB-S2` | `artifact_drift` | `findings.md#evidence-basis` | Current ready polling is Codex-gated at the API edge, while the desired poll surface is caller-neutral. | high | needs_review |
| `OPB-S3` | `artifact_drift` | `findings.md#evidence-basis` | Current claim creation and replay hard-code Codex identity, but the target identity belongs to the winning claim. | high | needs_review |
| `OPB-S4` | `artifact_drift` | `findings.md#evidence-basis` | Workbench copy still uses target/selected language before claim, implying identity binding too early. | high | safe |
| `OPB-S5` | `blocker_opened` | `findings.md#required-witness` | Existing tests prove Codex-bound singleton bridge behavior, not open availability with non-Codex claim identity. | high | blocked |
| `OPB-S6` | `evidence_added` | `findings.md#implementation-surface` | The implementation surface is now bounded: server, bridge helper, schemas, projector, CLI, workbench, and bridge tests. | high | needs_review |
| `OPB-S7` | `no_op` | `findings.md#rejected-paths` | Multi-request visible queues, background polling, pre-claim payload preview, session-side recovery, and production auth claims remain rejected. | high | safe |

## Target Artifact Inventory

| Artifact | Current claim | Refresh relevance |
| --- | --- | --- |
| `manual-session-bridge-plan/WORK-PACK.md` | Completed L0 Codex-bound manual bridge pilot. | Do not reopen; use as baseline evidence and predecessor. |
| `manual-session-bridge-design/ARCHITECTURE-BUNDLE.md` | Manual current-session bridge with Codex target and singleton ready poll. | Needs successor architecture delta, not in-place overwrite. |
| `SESSION-BRIDGE-PROTOCOL.md` | Loopback one-shot ready/claim/result/interrupt protocol. | Needs CLI signature update for caller-neutral ready and claim-time `agent_ref`. |
| `src/server.mjs` | Ready endpoint requires `agent_ref=codex.current-session`; claim/result APIs exist. | Implementation target. |
| `src/envelopes/manual-session-bridge.mjs` | Prepared and claimed bridge identity is Codex-specific. | Implementation target. |
| `src/kernel/projector.mjs` | Replay validates Codex-only claim identity. | Implementation target. |
| `schemas/bridge-claim-request.schema.json` | Claim identity schema is Codex-only. | Implementation target. |
| `schemas/receipt.schema.json` | Execution receipt identity must follow stored claim identity. | Implementation target. |
| `public/demo/l0.html` | Operator UI uses target/selected copy pre-claim. | Implementation target. |
| `tests/manual-session-bridge-*.test.mjs` and `tests/e2e/manual-session-bridge.spec.mjs` | Test old Codex-bound route and bridge safety behavior. | Validation target and required witness home. |

## Delta Summary

| Delta | Count | Target state | Evidence |
| --- | ---: | --- | --- |
| `route_changed` | 1 | Route from completed manual bridge closure to a successor open-poll bridge implementation package. | `OPB-S1` |
| `artifact_drift` | 3 | Runtime/schema/projector/UI contradict caller-neutral discovery and claim-bound identity. | `OPB-S2`..`OPB-S4` |
| `blocker_opened` | 1 | The open-poll witness is missing and must block any proof claim. | `OPB-S5` |
| `evidence_added` | 1 | The findings bound the implementation surface and rejected no-go paths. | `OPB-S6` |
| `no_op` | 1 | Rejected paths are already aligned with L0 limitations and should not become work. | `OPB-S7` |

## Proposed Changes

See [REFRESH-PATCH-PROPOSAL.md](REFRESH-PATCH-PROPOSAL.md) for the proposed
artifact deltas. Summary:

1. Create a successor implementation package for `open singleton availability,
   claim-bound identity`.
2. Preserve completed manual-session-bridge L0 closure as predecessor evidence.
3. Add a new acceptance-critical witness: caller-neutral ready poll, non-Codex
   claim identity, one winning claim, loser secrecy, result receipt bound to
   stored claim identity, restart replay, and operator-only recovery.
4. Update UI wording from `target/selected` to `availability/open/closed` before
   claim.
5. Keep singleton ready; explicitly reject multi-request visible queue and
   background polling in V0.

## Applied Changes

- None to target artifacts.
- This refresh creates only the report, patch proposal, machine-readable result,
  and Invoke result.

## Skipped Changes

| Candidate change | Reason skipped |
| --- | --- |
| Patch `src/server.mjs`, schemas, projector, CLI, UI, or tests | Refresh mode does not execute target implementation. |
| Mark manual-session-bridge work-pack incomplete | Existing closure remains true for the Codex-bound pilot; the new findings define a successor slice. |
| Promote multi-request queue semantics | Findings explicitly reject this for L0. |
| Claim open-poll behavior is proven | Non-vacuity gate opened a witness blocker. |

## Blockers And Gaps

Refresh blockers: none.

Target-artifact gaps:

| Gap | Owner | Status | Next action |
| --- | --- | --- | --- |
| `GAP-OPB-001` open-poll witness missing | successor implementation owner | open blocker | Add and pass the witness before claiming open availability is proven. |
| `GAP-OPB-002` Codex-gated ready poll | server/API owner | open implementation gap | Remove ready-time `agent_ref` selector; keep singleton safe projection. |
| `GAP-OPB-003` Codex-only claim identity | schema/projector/helper owner | open implementation gap | Store caller-supplied claim `agent_ref` and replay it immutably. |
| `GAP-OPB-004` UI pre-claim language drift | workbench owner | open UX gap | Rename target/selected language to availability/open/closed. |
| `GAP-OPB-005` CLI compatibility | session protocol owner | open implementation gap | Remove Codex query from `ready`; add `--agent-ref` to `claim` with Codex default. |

Invoke-specific gaps: none.

## Dispatch Technique Trace

| Technique | Refresh effect | Validation expectation |
| --- | --- | --- |
| `sequence` | Research findings -> source signals -> target inventory -> patch proposal -> next route. | Every delta consumes a named source handle. |
| `concrete_path_evidence` | Findings, research, plan, design, source, schema, UI, and test paths are exact. | No placeholder artifact claims. |
| `artifact_contract_bridge` | Keeps completed MSB closure intact while proposing successor artifact deltas. | No false status downgrade of completed L0 pilot. |
| `owner_boundary_check` | Invoke refresh proposes; implementation belongs to plan/task-session owners. | No runtime mutation in refresh. |
| `validation_loop` | Required witness becomes the validation gate for successor work. | No proof claim before tests exist and pass. |
| `residue_ledger` | Preserves witness blocker and rejected paths. | No gap erased by refresh status `pass`. |
| `handle_handoff` | Links concrete findings and patch proposal to next owner. | Next route consumes paths, not ambient conversation. |
| `authority_split_gate` | Separates operator availability, claimant identity, kernel receipts, and Invoke authoring. | Claim identity cannot be established by ready poll. |
| `execution_receipt_handoff` | Successor route must prove result receipt binds stored claim identity. | Receipt evidence required before closeout. |

Full dispatch document: not required. The refresh uses an already completed
research dispatch and creates no new reusable route or delegated execution.

Distill validation: skipped with reason. Refresh unit is narrow and
proposal-only: one findings package becomes one successor implementation
handoff. Distill should run during the follow-up `invoke plan`.

## Validation

- Source evidence present: `findings.md` and `research.md`.
- Target inventory present: completed manual bridge plan/design plus current
  runtime/schema/UI/test surfaces.
- Every proposed delta maps to `OPB-S1`..`OPB-S7`.
- No target runtime or plan artifact was mutated.
- Machine-readable `refresh-report.json` parses successfully.
- Refresh package whitespace check passes.

## Next Route

- Recommended route: `invoke plan`
- Rationale: the change crosses contracts, server, schemas, projector, CLI, UI,
  and tests. It needs a successor work-pack with SWUs and validation gates before
  Task Session execution.
- Suggested plan name: `open-poll-bridge-plan`

## Gate Result

- Status: `pass`
- Reason: source evidence is sufficient to produce a proposal-only refresh and
  successor route. The implementation proof remains intentionally blocked until
  the required witness is created and passes.

## Invoke Validation Fixture Result

- Mode: `refresh`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library
- Phase status: `pass`
- Mode contract: `.agents/skills/invoke/refresh.md`
- Outputs: `REFRESH-REPORT.md`, `REFRESH-PATCH-PROPOSAL.md`, `refresh-report.json`, `INVOKE-RESULT.md`
- Mutation mode: `proposal-only`
- Source signals: 7; route changed, artifact drift, blocker opened, evidence added, no-op
- Target artifacts: completed manual bridge package plus runtime/schema/UI/test surfaces
- Proposed changes: successor implementation package and witness gates
- Applied changes: none to target artifacts
- Skipped changes: runtime mutation, completed-plan downgrade, queue semantics
- Decisions: open singleton availability; claim-bound identity; no L0 multi-request queue
- Unresolved gaps: no Invoke gaps; five target implementation/witness gaps
- Next route: `invoke plan`
