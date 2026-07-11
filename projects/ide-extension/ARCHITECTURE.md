---
id: ide-extension-architecture
project: ide-extension
title: "ide-extension - Local Governed Workbench Architecture"
status: draft
node_type: architecture
updatedAt: 2026-07-10
---

# ide-extension - Architecture

## One Sentence

The project is a local governed action boundary around IDE-adjacent agent work:
HTML workbench outside, small kernel inside, modules/providers/adapters at the
edges, approval and receipts on every effectful crossing.

## Shape

```text
VS Code/VSCodium chrome (optional later)
        |
        v
Local browser URL: /demo/l0
        |
        v
Local Node server
        |
        +-- kernel/registry       module manifests
        +-- kernel/grants         allowed effects and approval gates
        +-- kernel/audit          append-only event/receipt log
        +-- kernel/artifacts      artifact refs
        +-- adapters/openrouter   provider transport only
        +-- adapters/mcp-chat     offline stdio witness first
        +-- envelopes             dry-run handoff boundary
```

## Kernel Responsibilities

The kernel owns:

- module registry;
- grant vocabulary;
- approval queue;
- audit append;
- artifact refs;
- provider mediation;
- adapter admission and custody descriptors;
- manual stop/emergency controls.

The kernel does not own:

- Craft authority;
- Whisper authority;
- UI Studio authority;
- IDE Ergonomics authority;
- OpenRouter authority;
- MCP server authority;
- browser extension authority;
- OpenClaw/Hermes/repo-agent runtime authority.

Those are modules, adapters, or future integrations.

## Host Strategy

L0 uses an adjacent browser/local URL because it is the strongest evidence path
for Playwright and Playwright MCP. VS Code/VSCodium can later wrap this URL in a
webview or open it through an IDE command, but the wrapper is chrome. It is not
the proof substrate until separately validated.

## Provider Strategy

OpenRouter belongs behind the local backend or extension host. The browser never
stores provider keys. Provider output can propose an envelope or draft; it cannot
approve itself or mutate durable state without a receipt.

## Adapter Admission Strategy

MCP, chat extensions, browser extensions, DevTools, Playwright, Kernel Cloud,
and Claude delegation enter as specimens behind a local adapter-admission
harness. The first harness is `McpChatWitnessAdapter`: a fake/local stdio MCP
server with one allowlisted `observe` tool and no network, provider, Chrome,
GitHub, Pendo, deployment, or authenticated dependency.

The adapter may record evidence artifacts and transcripts. The kernel alone owns
approval, durable state, and receipt append. L0.5 evidence binding uses
`evidence_refs` plus artifact hashes unless the receipt schema is intentionally
evolved.

`DesignFeedbackContextPacket` is a local context schema, not an authority-bearing
adapter. Its selected element, screenshot/artifact ref, page URL, selection
history, source candidates, companion message, and context refs are evidence or
hypotheses. Source candidates do not prove file ownership until separately
verified.

`claude-max-mcp` is deferred provider/process delegation, not a simple
`network.call`. Future admission must describe `process_spawn`, `cwd_scope`,
`env_allowlist`, `home_access`, `tool_allowlist`, `provider_delegation`,
credential source, timeout, and whether network is possible. Broad Claude tools
are no-go for the current slice.

## Agent Envelope Strategy

OpenClaw, Hermes, repo-style agents, and future agentic systems are represented
through envelopes:

- `describe` declares capabilities and receipts.
- `prepare` creates a typed proposal.
- `run` is dry-run/no-op in L0 unless an approval exists.
- `collect` returns artifact refs plus receipts.
- `interrupt` and `inspect` remain explicit controls.

Chat, MCP, and model-originated proposals cannot approve themselves. The
proposer, approver/session, adapter invoker, and receipt appender must remain
separable in the kernel state model.

## Evidence Loop

The workbench must never make canvas state authoritative. Visible nodes point to
source refs:

- packet ids;
- artifact paths;
- Craft ledger rows;
- validation rows;
- provider traces;
- receipt ids.

For L0.5 adapter admission, evidence refs include adapter descriptor hash, tool
allowlist hash, context packet hash, transcript hash, before/after digest, and a
redacted custody descriptor. Rejected runs create no receipt and no external
transcript artifact.

## Layer Order

| Layer | Purpose | Promotion Rule |
| --- | --- | --- |
| L0 local workbench | Local server, manifests, pending approval, dry-run receipt, durable state. | Existing smoke test passes. |
| L0.5 MCP/chat admission | Offline fake stdio witness proves adapter proposal, approval, observe, evidence, and receipt boundaries. | Offline witness plus negative tests pass. |
| L0.6 browser-first MV3 | Chrome extension observes/acts in a real tab through typed actions. | Builds on L0.5 admission; never bypasses local approval/receipt. |
| L1 IDE chrome | VS Code/VSCodium opens or embeds the local workbench URL. | Chrome only; no integrated-browser control claim. |
| L2 validation witnesses | Playwright/DevTools/Kernel Cloud can witness runtime behavior. | Evidence lane only; no remote receipts or authority. |
