---
id: ide-extension-browser-first-design-transport
project: ide-extension
title: "Browser-First Extension Design Transport"
status: flag
node_type: design-transport
updatedAt: 2026-07-10
invoke_mode: design
---

# Design Transport

## Provenance

- Observed capability: `invoke`
- Mode: `design`
- Target artifact: `ide-extension browser-first extension lane`
- Target owner/cycle: `projects/ide-extension`
- Source mode: discovery-mode design from user-approved architecture request
- Phase status: `flag`

The flag is not a design blocker. It records that `ide-extension` lacks a
standalone glossary/aspect-doc define package, and that the Chrome extension
itself still needs a plan and witness implementation.

## Source Contracts

- `projects/ide-extension/SPEC.md`
- `projects/ide-extension/ARCHITECTURE.md`
- `projects/ide-extension/README.md`
- `projects/ide-extension/src/server.mjs`
- `projects/ide-extension/development/founding-research/findings.md`
- `projects/ide-extension/development/vscode-browser-control-api-research/findings.md`
- `projects/ide-extension/development/mcp-chat-extension-integration-research/findings.md`
- `../workspace-resonant/2.0.0-alpha/browser-first/README.md`
- `../workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/manifest.json`
- `../workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/background.js`
- `../workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/lib/browser-page-actions.js`
- `../workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/content.js`
- `../workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/lib/approval-policy.js`
- `../workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/lib/bridge-client.js`

## Dispatch Technique Trace

| Technique | Applied To | Validation Expectation |
| --- | --- | --- |
| `sequence` | Context -> architecture -> boundary mapping -> plan handoff. | Each step consumes prior artifact/frame evidence. |
| `concrete_path_evidence` | Source contracts and local precedent. | Claims cite concrete project paths. |
| `owner_boundary_check` | Extension versus kernel authority. | Extension remains adapter; kernel owns approvals/receipts. |
| `artifact_contract_bridge` | Invoke design output to downstream plan. | Bundle, glossary report, layering seed, dispatch JSON, and result are present. |
| `protected_action_mapping` | Browser actions. | Hard and public-submit boundaries are named before implementation. |
| `approval_semantics_map` | Human approval versus action execution. | Approval record is distinct from model proposal and action result. |
| `state_namespace_boundary` | Extension storage versus `.ide-extension/state`. | Durable state remains local kernel state. |
| `execution_receipt_handoff` | Future extension action result to kernel receipt. | Plan must define receipt fields before enabling actions. |
| `evidence_receipt_link` | MCP/chat adapter transcripts and context packets. | Evidence is linked through `evidence_refs` and artifact hashes unless schema evolves. |
| `authority_split_gate` | MCP/chat/browser/model surfaces versus kernel. | Adapter, model, chat, and browser code cannot approve, mutate durable state, or mint receipts. |
| `validation_loop` | Dispatch validation and future witness checks. | Dispatch JSON validates; plan defines smoke checks. |
| `residue_ledger` | Gaps and deferred lanes. | VS Code wrapper, Playwright MCP, and glossary gaps are preserved. |
| `scu_swu_reduction` | Design unit selection. | Smallest coherent unit is now the offline L0.5 MCP/chat adapter-admission harness. |
| `recomposition_proof` | Fit to existing L0 workbench. | Admission harness and later extension lane compose back into local server/kernel without replacing it. |

Full dispatch document: `projects/ide-extension/development/browser-first-extension-design/browser-first-extension.dispatch.json`

Dispatch validation: `pass` with no blocks or flags.

## Decisions

1. Use a Chrome Manifest V3 extension for real browser-tab control.
2. Keep the local HTML workbench as the canonical UI source.
3. Keep the local Node server/kernel as approval and receipt authority.
4. Frame `/demo/l0` from side panel first; fallback to a tiny extension shell if
   framing is blocked in a target Chrome environment.
5. Implement only typed browser actions.
6. Block credentials, wallets/signatures, payments, public submit, destructive,
   and privileged browser operations for L0.5.
7. Defer VS Code/VSCodium wrapper and Playwright MCP to separate lanes.
8. Insert an offline MCP/chat adapter-admission witness before the Chrome MV3
   browser-action witness.
9. Treat `DesignFeedbackContextPacket` as context/evidence schema, not an
   authority-bearing adapter.
10. Defer `claude-max-mcp`, Yocoolab MCP, Chrome DevTools MCP, Kernel Cloud,
    Streamable HTTP MCP, PR/Pendo/deployment hooks, streaming, persistence, and
    cost accounting.

## Unresolved Gaps

| Gap | Owner | Route |
| --- | --- | --- |
| No standalone `ide-extension` glossary. | `projects/ide-extension` | Follow-up define/refresh or small glossary task. |
| Chrome extension files do not exist yet. | `projects/ide-extension` | Invoke plan -> task-session. |
| MCP/chat admission harness does not exist yet. | `projects/ide-extension` | Invoke plan should build this before the Chrome extension scaffold. |
| `DesignFeedbackContextPacket` schema and fixture do not exist yet. | `projects/ide-extension` | Add to the L0.5 admission work-pack. |
| Fake stdio MCP witness server does not exist yet. | `projects/ide-extension` | Add to the L0.5 admission work-pack. |
| Adapter descriptor registration and custody validation do not exist yet. | `projects/ide-extension` kernel plan | Add offline descriptor schema, env allowlist, fixture CWD, temp/redacted HOME, and tool allowlist checks. |
| Bridge token/config generation is not implemented. | `projects/ide-extension` kernel plan | Include in L0.5 work-pack. |
| Browser action receipt schema extension is not defined. | `projects/ide-extension` schema plan | Keep L0.5 adapter bindings in `evidence_refs` unless receipt schema evolution is deliberately approved. |
| Side-panel iframe behavior may vary by Chrome/CSP/mixed-content environment. | Browser extension plan | Witness iframe path and fallback shell. |
| Playwright MCP browser-act validation is deferred. | Validation lane | Separate L2 plan after L0.5 witness. |
| VS Code/VSCodium wrapper is deferred. | IDE wrapper lane | Separate L1 plan after browser-first proof. |
| Source candidates in context packets can be mistaken for source truth. | `projects/ide-extension` schema/test plan | Mark candidates as hypotheses until separately verified. |

## Next Route

`invoke plan` should first produce an L0.5 work-pack for the offline
`McpChatWitnessAdapter`, `DesignFeedbackContextPacket`, fake stdio witness
server, adapter registration validator, evidence artifact writer, hash binding
helper, and positive/negative test suite.

After that witness passes, a separate browser-first plan can produce the minimal
Chrome extension scaffold and server bridge additions. `task-session` should own
implementation after each plan is approved.
