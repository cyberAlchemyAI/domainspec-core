---
id: ide-extension-browser-first-design-index
project: ide-extension
title: "Browser-First Extension Design Package"
status: draft
node_type: invoke-design-index
updatedAt: 2026-07-10
---

# Browser-First Extension Design Package

This package records the Invoke design for adding a minimal Chrome Manifest V3
browser-extension lane to `ide-extension`, refreshed after MCP/chat integration
research to insert an offline adapter-admission witness before the browser lane.

The browser design copies the ResonantOS browser-first shape, not its full
product surface: a side panel, a background router, content scripts for DOM
witness and typed page actions, and a loopback bridge into the existing local
HTML workbench/kernel. The refreshed first implementation slice is smaller:
`McpChatWitnessAdapter`, `DesignFeedbackContextPacket`, and a fake/local stdio
MCP witness with one allowlisted `observe` tool.

## Artifacts

| Path | Purpose |
| --- | --- |
| [ARCHITECTURE-BUNDLE.md](ARCHITECTURE-BUNDLE.md) | Six-view architecture bundle for the browser-first extension lane. |
| [GLOSSARY-CONSISTENCY.md](GLOSSARY-CONSISTENCY.md) | Term consistency check against the existing spec, architecture, and research findings. |
| [IMPLEMENTATION-LAYERING-SEED.md](IMPLEMENTATION-LAYERING-SEED.md) | Design-stage L0-L2 layering seed, not a work-pack. |
| [DESIGN-TRANSPORT.md](DESIGN-TRANSPORT.md) | Handoff notes, decisions, gaps, and next-route recommendation. |
| [browser-first-extension.dispatch.json](browser-first-extension.dispatch.json) | Dispatch Spec route used to validate the design boundary. |
| [INVOKE-RESULT.md](INVOKE-RESULT.md) | Invoke output contract for this run. |

## Boundary

The Chrome extension is not the authority layer. It is a browser adapter around
the local workbench and active browser tabs. MCP/chat tools are also not an
authority layer; they enter first through an offline adapter-admission witness.

Authority remains in the existing local server/kernel:

- module manifests;
- grants;
- approvals;
- audit events;
- receipts;
- provider mediation;
- agent envelope state.

The browser extension may observe pages and perform explicitly mediated browser
actions after policy and approval checks. It must not store provider keys,
mutate Craft/Whisper/Arcanum authority, or claim VS Code Integrated Browser
control.

The MCP/chat admission witness may prepare proposals and record evidence
artifacts after approval. It must not use real external MCP servers, provider
delegation, Chrome, network, GitHub, Pendo, deployment hooks, live authenticated
browser state, self-approval, direct durable mutation, or adapter-minted
receipts.
