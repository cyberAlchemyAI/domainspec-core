# Ide Extension Founding Research Findings

Dispatch: `2026-07-09-ide-extension-founding-research`
Status: `resolved`
Decision altitude: L0 witness contract, not product proof

## Resolved Definition

`projects/ide-extension` is a local, IDE-adjacent governance workbench that
binds editor-visible intent, module manifests, external agent envelopes, human
approval gates, and evidence receipts into one auditable action boundary.

Its distinctive contract is not chat, canvas, preview, model access, or agent
execution by itself. The contract is deciding what may cross from IDE-visible
intent into owner-routed action, under explicit grants, receipts, and durable
state.

## Verdict Matrix

| Candidate | Evidence status | Verdict |
| --- | --- | --- |
| Local-server-first governed workbench | Buildable from owned precedent: UI Prototyping Studio local preview/persistence/Playwright loop, IDE Ergonomics governance grammar, ResonantOS browser-first local bridge/module precedent, and agent envelope boundaries. | APPROVE for L0 scaffold. |
| Full autonomous IDE agent | Not witnessed. The evidence supports prepare, dry-run, approval, and receipts, not autonomous mutation. | KILL for L0. |
| VSCodium embedded webview with Playwright control | VS Code/VSCodium webview shell is feasible, but embedded webview control by Playwright MCP is not locally proven. | DEFER. Use adjacent browser/local URL first. |
| OpenRouter as agent core | OpenRouter is a provider transport and model access surface, not governance, permission, state, or authority. | KILL as core. Allow as backend adapter. |

## Evidence Map

- UI Prototyping Studio supplies the owned local loopback, file-backed state,
  artifact, CLI, and browser-evidence precedent. It does not already own
  OpenRouter, Craft, Whisper, ResonantOS, pluggable envelopes, or a canvas-native
  IDE workbench. Evidence: `research.md` lines 35-119.
- IDE Ergonomics supplies the restraint grammar: preview is not execution,
  recommendation is not authority, and every visible action needs source,
  owner, effect, gate, and receipt fields. Evidence: `research.md` lines
  164-238.
- Official docs support a VS Code/VSCodium-compatible host shell, OpenRouter
  backend calls, and Playwright MCP for adjacent browser automation. They do not
  prove embedded VSCodium webview control. Evidence: `research.md` lines
  242-357.
- The agent envelope is an actor boundary, not an agent runtime. L0 may
  describe, prepare, dry-run after approval, collect, interrupt, inspect, and
  receipt. Evidence: `research.md` lines 363-510.
- The added `../workspace-resonant` explorer contributes browser-first local
  bridge, module ownership, Delegation Packet-like envelope, approval policy,
  and minimal-kernel precedent. Evidence: `research.md` lines 520-630.

## L0 Scope

L0 may claim only this:

1. A one-command local server opens `/demo/l0`.
2. A real workbench renders: canvas/work area, module list, selected work item,
   approval queue, and evidence rail.
3. State persists outside browser memory under `.ide-extension/state/`.
4. At least one manifest-registered module validates against a schema.
5. A dry-run agent envelope reaches `awaiting_approval`.
6. Execution is blocked until an explicit approval record exists.
7. An approved no-op appends a durable receipt.
8. A smoke test proves the path.

## Architecture Boundary

The kernel owns only:

- module registry;
- grant vocabulary;
- audit/event append;
- artifact references;
- provider mediation;
- approval queue;
- emergency/manual controls.

Craft, Whisper, UI Prototyping Studio, IDE Ergonomics, OpenRouter, ResonantOS
precedents, OpenClaw, Hermes, and repo-style agents are modules or adapters.
They do not become kernel dependencies.

## Non-Goals

- No autonomous IDE agency claim.
- No validated VSCodium embedded-webview automation claim.
- No provider secrets in browser or webview code.
- No direct Craft or Whisper authority mutation from the workbench.
- No canvas-as-authority model; canvas nodes must point to packets, artifacts,
  ledger rows, validation rows, provider traces, or receipts.
- No multi-user, remote, auth, marketplace, production, or concurrency-safety
  claim.
- No claim that private DomainSpec or Saturn surfaces are shipped product
  features.

## First Witness Checklist

- `npm run start` serves `/demo/l0`.
- `npm run smoke` proves the local path without a model key.
- The module registry loads at least one manifest.
- Invalid manifests fail the schema validator.
- `POST /api/envelopes/prepare` creates a pending approval.
- `POST /api/approvals/:id/approve` creates a receipt.
- Receipt writes include `receipt_id`, `run_id`, `stage`, `status`, `before_ref`,
  `after_ref`, `approval_id`, and evidence refs.
- A later Playwright MCP pass drives the adjacent local browser URL, not an
  embedded VSCodium webview, until the embedded surface is separately witnessed.

## Wording Discipline

Use: `L0 witness contract`, `local-server-first governed workbench`,
`IDE-adjacent chrome`, `provider adapter`, `agent envelope`, `approval-gated dry
run`, and `durable receipt`.

Avoid: `IDE agent`, `autonomous agent`, `product proof`, `unified authority
layer`, `VSCodium-native automation`, and `OpenRouter-powered core`.

