---
id: ide-extension-mcp-chat-refresh-report
project: ide-extension
title: "Invoke Refresh Report - MCP/Chat Findings Into Spec, Architecture, And Design"
status: pass
node_type: refresh-report
updatedAt: 2026-07-10
invoke_mode: refresh
mutation_mode: apply-approved
---

# Invoke Refresh Report

## Summary

The MCP/chat integration findings have been applied to the `ide-extension`
spec, architecture, and browser-first design package.

The refresh preserves the local Node kernel as authority and changes the next
implementation route: build the offline `McpChatWitnessAdapter` admission
harness before integrating real external MCP servers, Claude delegation,
Yocoolab, Chrome DevTools, Kernel Cloud, or the Chrome MV3 browser-action lane.

## Refresh Scope

Mutation mode: `apply-approved`

Source evidence:

- `projects/ide-extension/development/mcp-chat-extension-integration-research/findings.md`
- `projects/ide-extension/development/mcp-chat-extension-integration-research/research.md`

Target artifacts:

- `projects/ide-extension/SPEC.md`
- `projects/ide-extension/ARCHITECTURE.md`
- `projects/ide-extension/README.md`
- `projects/ide-extension/development/browser-first-extension-design/ARCHITECTURE-BUNDLE.md`
- `projects/ide-extension/development/browser-first-extension-design/DESIGN-TRANSPORT.md`
- `projects/ide-extension/development/browser-first-extension-design/IMPLEMENTATION-LAYERING-SEED.md`
- `projects/ide-extension/development/browser-first-extension-design/GLOSSARY-CONSISTENCY.md`
- `projects/ide-extension/development/browser-first-extension-design/README.md`
- `projects/ide-extension/development/browser-first-extension-design/INVOKE-RESULT.md`
- `projects/ide-extension/development/browser-first-extension-design/browser-first-extension.dispatch.json`

## Source Signals

| ID | Type | Target Artifacts | Claim | Confidence | Mutation Safety |
| --- | --- | --- | --- | --- | --- |
| `MCP-CHAT-S1` | `evidence_added` | `SPEC.md`, `ARCHITECTURE.md`, design package | L0.5 must prove adapter admission with a fake/local stdio MCP witness before real external integrations. | high | safe |
| `MCP-CHAT-S2` | `route_changed` | `ARCHITECTURE-BUNDLE.md`, `DESIGN-TRANSPORT.md`, `IMPLEMENTATION-LAYERING-SEED.md`, `INVOKE-RESULT.md` | Browser-first MV3 is no longer the first L0.5 slice; it follows the MCP/chat admission harness. | high | safe |
| `MCP-CHAT-S3` | `evidence_added` | `SPEC.md`, `ARCHITECTURE.md`, `GLOSSARY-CONSISTENCY.md` | `DesignFeedbackContextPacket` is evidence/schema only; source candidates are hypotheses, not source truth. | high | safe |
| `MCP-CHAT-S4` | `evidence_added` | `SPEC.md`, `ARCHITECTURE.md`, `ARCHITECTURE-BUNDLE.md` | Adapter evidence must bind through `receipt.evidence_refs` and artifacts unless receipt schema evolves deliberately. | high | safe |
| `MCP-CHAT-S5` | `blocker_opened` | design package, next plan | The adapter descriptor schema, context packet schema/fixture, fake stdio witness server, evidence writer, and negative tests do not exist yet. | high | safe |
| `MCP-CHAT-S6` | `route_changed` | `ARCHITECTURE.md`, design package | `claude-max-mcp` is deferred provider/process delegation, not a simple `network.call`. | high | safe |

## Applied Changes

- Updated `SPEC.md` from an L0-only witness contract to an L0/L0.5 witness
  contract with MCP/chat admission scope, no-go lanes, envelope actor/session
  separation, schema-safe evidence binding, and positive/negative L0.5
  acceptance tests.
- Updated `ARCHITECTURE.md` with adapter admission, `DesignFeedbackContextPacket`,
  deferred provider/process delegation, actor/session separation, evidence refs,
  and a refreshed layer order: L0 local workbench, L0.5 MCP/chat admission, L0.6
  MV3 browser-first, L1 IDE chrome, L2 validation witnesses.
- Updated the browser-first design bundle to insert the offline
  `McpChatWitnessAdapter` harness before the Chrome MV3 lane.
- Updated design transport decisions, technique trace, gaps, and next route so
  `invoke plan` targets the MCP/chat admission harness first.
- Updated the implementation layering seed with L0.5 adapter-admission evidence
  and L0.6 browser-first evidence.
- Updated glossary consistency with new candidate terms and ambiguity checks.
- Updated project and design package README files with the refreshed route.
- Updated `INVOKE-RESULT.md` so future continuation agents do not plan the
  Chrome extension first.
- Updated `browser-first-extension.dispatch.json` metadata handles so the plan
  handoff points to L0.5 adapter admission first and Chrome MV3 as L0.6.

## Dispatch Technique Trace

| Technique | Applied To | Validation Expectation |
| --- | --- | --- |
| `sequence` | Findings -> spec -> architecture -> design package -> report. | Each edited artifact consumes the prior evidence and keeps the route order. |
| `concrete_path_evidence` | Source and target artifact references. | Every source signal points to concrete paths. |
| `artifact_contract_bridge` | Findings into existing invoke-authored artifacts. | Refresh edits preserve artifact roles rather than replacing the lifecycle. |
| `owner_boundary_check` | Kernel versus adapters, providers, browser extensions, and MCP tools. | Kernel remains approval, durable state, and receipt authority. |
| `authority_split_gate` | MCP/chat/model/browser actors. | Proposer, approver/session, invoker, and receipt appender remain separable. |
| `approval_semantics_map` | L0.5 acceptance tests. | Approval is exact, one-use, and required before adapter invocation. |
| `evidence_receipt_link` | Adapter transcript/context hashes. | Binding goes through `evidence_refs` and artifacts unless schema evolves. |
| `state_namespace_boundary` | Adapter evidence versus `.ide-extension/state`. | Adapter records evidence; kernel mints receipts and owns durable state. |
| `validation_loop` | Positive and negative acceptance tests. | Integration is not accepted until offline witness and negative tests pass. |
| `residue_ledger` | Deferred/no-go lanes and missing harness files. | Gaps are preserved for `invoke plan`/`task-session`. |

Full dispatch document: not required. This refresh applied a bounded local
artifact update with no subagent delegation or reusable new dispatch route.

Distill validation: skipped. The refresh scope is already narrow and local:
apply the MCP/chat findings to existing spec/architecture/design artifacts and
route implementation to a later plan.

## Validation

- Review check: local source signals map to applied artifact deltas.
- Review check: stale adapter/context wording was not introduced.
- Review check: L0.5 remains fake/local/offline and does not depend on external
  services, browsers, providers, or network access.
- Review check: next route is `invoke plan`, not direct task execution.

## Unresolved Gaps

Target-artifact gaps:

- No adapter descriptor schema yet.
- No `DesignFeedbackContextPacket` schema/fixture yet.
- No fake stdio MCP witness server yet.
- No adapter registration validator yet.
- No evidence artifact writer/hash binding helper yet.
- No L0.5 smoke/negative tests yet.
- No standalone `ide-extension` glossary yet.

Invoke gaps: none.

## Next Route

`invoke plan` should produce the L0.5 work-pack for the offline MCP/chat adapter
admission harness. `task-session` should own implementation after that plan is
approved.
