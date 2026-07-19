---
id: ide-extension-workbench-bridge-demo-v01-spec
project: ide-extension
title: "Workbench Bridge Demo V0.1"
status: planned
node_type: spec
updatedAt: 2026-07-17
invoke_mode: define
---

# Workbench Bridge Demo V0.1 Spec

## Definition

Workbench Bridge Demo V0.1 is a small product increment that turns the proven
manual bridge into an operator-visible workbench flow.

It does not change the bridge authority model. The local kernel still owns
prepare, approval, ready selection, claim admission, result admission, durable
events, artifacts, and receipts.

## User Need

The current proof works, but the operator has to remember terminal commands and
map IDs by hand. A normal user should be able to prepare a task in the
workbench, see that it is ready, copy the poll/claim commands, and see the
admitted receipt after the session completes.

## Included

- A workbench demo panel for the manual bridge recipe.
- Current ready request status without revealing task details before claim.
- Clear display of prepared, approved, ready, claimed, and terminal states.
- Copyable `workbench-poll --ready` and `workbench-poll --claim` command hints.
- A receipt display after `skill.execution` is admitted.
- Existing API and state model reuse where possible.
- Tests proving the UI does not reveal task or requested skill in ready-only state.

## Excluded

- Automatic background polling.
- Multi-request queue.
- Lease, timeout, or worker registry.
- Real skill execution automation.
- OpenRouter model execution.
- Browser or VSCodium control.
- Remote access or deployment.
- Any direct durable-state mutation outside the existing kernel APIs.

## Success Criteria

1. The workbench shows the manual bridge loop as a single understandable flow.
2. A user can prepare or inspect a ready request without learning the hidden task.
3. The UI gives enough command context for a separate Codex session to poll and claim.
4. After a result is admitted, the workbench shows the execution receipt.
5. Existing bridge tests continue to pass.
6. New UI tests prove the blind boundary is preserved.

## Source Evidence

- `projects/ide-extension/SPEC.md`
- `projects/ide-extension/README.md`
- `projects/ide-extension/SESSION-BRIDGE-PROTOCOL.md`
- `projects/ide-extension/development/open-poll-bridge-plan/WORK-PACK.md`
- `arcanum/arcana/workbench-up/SKILL.md`
- `arcanum/arcana/workbench-poll/SKILL.md`

## Decisions

| ID | Decision | Rationale |
| --- | --- | --- |
| WBD-D1 | Keep the demo manual and one-shot. | The proven L0 contract explicitly excludes worker behavior. |
| WBD-D2 | Use the existing local bridge API. | The kernel already owns authority and receipts. |
| WBD-D3 | Show command recipes, not hidden automation. | This makes the demo usable while preserving proof boundaries. |
| WBD-D4 | Treat receipt display as the terminal proof. | Chat completion alone is not bridge completion. |

## Define Dispatch Technique Trace

| Technique | Applied To | Validation Expectation |
| --- | --- | --- |
| `sequence` | prepare -> ready -> poll -> claim -> result -> receipt | UI order matches bridge typestate. |
| `owner_boundary_check` | operator, poller, kernel, claimant | UI does not grant new authority. |
| `artifact_contract_bridge` | receipt and artifact refs | UI shows admitted receipt, not chat-only output. |
| `concrete_path_evidence` | source contracts | Plan cites exact local files. |

## Distill Sanity Check

Result: pass.

The selected unit is the smallest useful product increment after the bridge
proof: visible repeatability. It does not reopen MCP, worker, provider, browser,
or VSCodium lanes.
