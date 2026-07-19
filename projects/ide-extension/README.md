# ide-extension

`ide-extension` is a local-server-first governed workbench for IDE-adjacent
agent work. It starts as a small HTML/canvas-like local browser surface, with an
optional future VS Code/VSCodium wrapper, and treats every model, module, browser
act, and agent handoff as an approval-gated crossing into durable state.

The project is deliberately scoped to an L0 witness: prove the boundary before
claiming an IDE agent.

## What's Here

| Path | What it is |
| --- | --- |
| [SPEC.md](SPEC.md) | L0 witness contract and acceptance boundary. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Minimal kernel, modules, agent envelopes, provider adapter, and evidence loop. |
| [CRAFT.md](CRAFT.md) and [.craft/ledger.yml](.craft/ledger.yml) | Project Craft state. Source of truth is `.craft/ledger.yml`. |
| [schemas/](schemas/) | JSON schemas for module manifests, agent envelopes, and receipts. |
| [src/](src/) | Tiny local server and kernel slices for the first witness path. |
| [public/demo/l0.html](public/demo/l0.html) | The first workbench screen. |
| [development/founding-research/](development/founding-research/) | Dispatch transcript and findings that founded the project. |
| [development/mcp-chat-extension-integration-research/](development/mcp-chat-extension-integration-research/) | Findings for the MCP/chat adapter-admission harness and no-go external lanes. |

## Current Status

- Founding research: complete.
- Project scaffold: in place.
- L0 server witness: minimal, local-only, no model key required.
- L0 manual session bridge: bounded pilot ready; manual `poll`, singleton target,
  late skill disclosure, read/preview-only grants, unattested local session, and
  separate authorization/execution receipts. See the
  [closure report](development/manual-session-bridge-plan/task-sessions/20260712T115410Z-task-verify-readiness/CLOSURE-REPORT.md).
- Workbench Bridge Demo V0.1: complete; ready, claim, result, and receipt are
  visible, and `workbench-poll --claim` now continues execution in the active
  session by default.
- Operations V1: complete for trusted-local whole-document derive, replace,
  append, rebuild, display, interaction, and retention.
- Workbench UI V1: active planned increment. It makes Agent task explicit,
  centers Canvas, and composes Craft and evidence around one run lifecycle. See
  the [work pack](development/workbench-ui-v1/WORK-PACK.md).
- L0.5 MCP/chat admission witness: deferred behind the active UI V1 increment;
  fake/local stdio only when resumed.
- Chrome MV3 browser-first extension: designed as later browser adapter lane
  after the adapter-admission boundary is proven.
- VS Code/VSCodium wrapper: deferred until the browser path is witnessed.
- Playwright MCP/VSCodium webview control: unproven; use adjacent browser first.
- OpenRouter: provider adapter only; not the kernel or authority layer.

## Active V1 Sequence

```text
SWU-WUI-001 semantic regions -> 002 desktop grid -> 003 mobile navigation
  -> 004 explicit composer -> 005 RunView mapper -> 006 timeline -> 007 legal action
  -> 008 primary Canvas -> 009 Craft seed -> 010 evidence Inspector
  -> 011 product validation
```

V1 is a UI/product milestone over the local workbench. It does not imply an
autonomous worker, browser-control adapter, provider execution, or IDE wrapper.

## Running

Requires Node 20 or newer.

```bash
cd projects/ide-extension
npm run start
```

Open the printed local URL, or go directly to:

```text
http://127.0.0.1:8765/demo/l0
```

Run the no-dependency smoke test:

```bash
cd projects/ide-extension
npm run smoke
```

## Boundary

The workbench may show Craft state, compose/review Whisper-like text, display UI
Studio artifacts, recommend IDE Ergonomics actions, call OpenRouter through a
backend adapter, and prepare OpenClaw/Hermes/repo-style agent envelopes.

It may not silently mutate Craft, Whisper, Arcanum, repository files, browser
state, provider settings, external accounts, public surfaces, or generated
runtime packages. Any write, shell, network, browser-act, export, handoff,
commit, push, provider-key change, or publication crosses an explicit approval
gate and must leave a receipt.

## First Witness

The first proof is not "a webview opens." The first proof is:

1. local server boots;
2. workbench renders;
3. manifests load;
4. a dry-run envelope becomes pending approval;
5. approval creates a receipt;
6. durable state records the event.

The next proof is not "MCP is connected." The next proof is:

1. a fake/local stdio `McpChatWitnessAdapter` registers with one allowlisted
   `observe` tool;
2. a `DesignFeedbackContextPacket` fixture prepares a proposal;
3. run before approval invokes nothing;
4. one explicit approval permits one observe call;
5. evidence is written as local artifact refs and hashes;
6. the kernel, not the adapter, mints the receipt;
7. negative tests reject self-approval, bad approvals, mutation/network tools,
   credential exposure, broad Claude tools, PR/Pendo/deployment hooks, and live
   browser write actions.
