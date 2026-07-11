# MCP Chat Extension Integration Findings

Dispatch: `2026-07-10-mcp-chat-extension-integration-research`
Date: 2026-07-10
Verdict: build the local adapter admission harness, not MCP/chat/browser tool adoption.

## Finding

L0.5 must prove the existing `ide-extension` kernel authority boundary with a deterministic offline witness before any external specimen is admitted. MCP servers, chat extensions, Chrome/MV3 extensions, browser tools, model providers, and cloud browser systems are adapter or witness surfaces only. They may propose, observe, and produce evidence; they must not approve, mutate durable state, or mint receipts.

## Source Basis

Local basis: [research.md](./research.md), [SPEC.md](../../SPEC.md), [ARCHITECTURE.md](../../ARCHITECTURE.md), [server.mjs](../../src/server.mjs), [grants.mjs](../../src/kernel/grants.mjs), [agent-envelope.schema.json](../../schemas/agent-envelope.schema.json), [receipt.schema.json](../../schemas/receipt.schema.json), [l0-smoke.test.mjs](../../tests/l0-smoke.test.mjs), [ARCHITECTURE-BUNDLE.md](../browser-first-extension-design/ARCHITECTURE-BUNDLE.md).

External basis: MCP host/client/server and tool/transport model ([architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture), [tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools), [transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)); `claude-max-mcp` stdio/provider-delegation precedent ([repo](https://github.com/Jonahbkerr/claude-max-mcp)); Yocoolab product grammar and risk surface ([README](https://github.com/Yocoolab/mcp-server/blob/main/README.md), [bridge](https://github.com/Yocoolab/mcp-server/blob/main/src/http-bridge.ts)); Claude Code Chrome and Chrome DevTools browser-control risks ([Claude Chrome](https://code.claude.com/docs/en/chrome), [Chrome DevTools agents](https://developer.chrome.com/docs/devtools/agents/get-started)); later witness specimens only: [Playwright MCP](https://github.com/microsoft/playwright-mcp), [Kernel MCP](https://www.kernel.sh/docs/reference/mcp-server).

## Definitions

MCP transport: JSON-RPC channel between MCP client and server; L0.5 admits only local stdio. Streamable HTTP is deferred.

MCP server/tool: capability exposure. A tool description is not authority and must be treated as untrusted until admitted by the kernel.

Model backend: provider transport. It may generate text or proposals; it cannot approve itself or mutate durable state.

Chat extension: proposal/review UI. It can prepare envelopes and display evidence, not authorize its own work.

Chrome/MV3 extension: browser adapter. It can mediate active-tab observation and typed page actions; durable authority remains local Node.

Local kernel authority: loopback Node kernel owning manifests, grant vocabulary, approvals, audit, artifacts, provider mediation, envelopes, and receipts.

Evidence: artifact refs, transcript hashes, screenshots, context packets, and before/after digests that support a receipt.

Receipt: kernel-minted record of an approved run. Adapters record evidence; the kernel mints receipts.

Adapter: bounded connector with descriptor, transport, allowlist, custody statement, and no independent authority.

Witness: deterministic local proof that an adapter can only act through prepare -> approval -> run -> receipt.

Proposal: prepared envelope awaiting explicit approval.

Approval: exact authorization for one proposal/run/tool under actor/session separation.

Self-approval: adapter, model, or proposing actor approving its own request. This is a no-go.

## Lane Ownership

Build now: `McpChatWitnessAdapter`, local-only fake stdio MCP server, one allowlisted `observe` tool, adapter descriptor validation, transcript/artifact hashing, and approval-bound evidence binding. If the proof uses `dry_run`, treat it as a separate kernel dry-run envelope class, not the adapter observe class.

Build now as schema/product grammar: `DesignFeedbackContextPacket`, inspired by Yocoolab but owned locally. Required fields: selected element, screenshot/artifact ref, page URL, selection history, source candidates, companion message, and context refs. Source candidates are hypotheses, not claims.

Use as precedent only: MCP stdio transport and the existing local prepare -> approval -> run -> receipt implementation.

Treat as specimens/later witnesses only: `claude-max-mcp`, Yocoolab MCP, official MCP servers, Claude Code Chrome, Chrome DevTools MCP, Playwright, and Kernel Cloud.

## L0.5 Harness Shape

The first witness is fake/local/offline: no Claude, Yocoolab, GitHub, Pendo, Chrome, Kernel Cloud, deployment, live browser, external network, or authenticated dependency.

Registration must accept only an adapter descriptor with `transport: stdio`, bounded command/args, fixture CWD, redacted/temp HOME, explicit env allowlist, one `observe` tool allowlist, `network: false`, `mutation: false`, `receipt_authority: false`, and a custody statement.

The adapter prepares an agent envelope using existing envelope semantics. `/api/envelopes/run` must reject before approval. After exact approval, the kernel invokes only the allowlisted fake tool and appends a local receipt.

## Mechanical Binding

Do not widen the closed receipt schema unless intentionally evolving it. For L0.5, bind through `receipt.evidence_refs` to kernel-written artifacts containing: `envelope_id`, `approval_id`, `adapter_id`, `adapter_descriptor_hash`, `tool_allowlist_hash`, `context_packet_sha256`, `transcript_sha256`, artifact refs and hashes, before/after digest, custody statement, and redacted env/CWD/HOME descriptor.

If receipt schema evolution is chosen later, add binding fields deliberately and update schema/tests together. Do not smuggle adapter-specific fields into receipts while `additionalProperties: false` remains in force.

## Claude Max MCP Position

`claude-max-mcp` is deferred provider delegation, not a simple `network.call`. Admission requires grants for process spawn, cwd scope, env allowlist, HOME access, provider delegation, credential source, timeout, tool allowlist, and whether network is possible. Broad Claude Code tools, inherited unconstrained HOME/CWD, and delegated mutation are no-go for this slice.

## Deferred

Defer `claude-max-mcp`, Chrome DevTools beyond one later bounded witness, Streamable HTTP MCP, Kernel Cloud, Playwright/DevTools validation lanes, streaming, persistence, cost accounting, PR hooks, Pendo hooks, deployment hooks, and live authenticated browser control.

## Kill / No-Go For L0.5

Reject self-approval, direct durable mutation, adapter-minted receipts, remote receipts, broad Claude tools, direct PR/Pendo/deployment hooks, browser/webview credential storage, live authenticated sensitive Chrome control, mutation-capable tools, network access, and any adapter descriptor that claims approval or receipt authority.

## Acceptance Tests

Positive tests: register adapter; prepare proposal; run before approval is blocked and invokes nothing; approve exactly one adapter read/observe invocation; adapter invokes only after approval; kernel appends receipt with evidence refs and binding artifacts. If testing a kernel `dry_run`, use a separate case that does not pretend the adapter tool performed it.

Negative tests: forged, wrong, expired, or reused approval rejects; non-allowlisted tool rejects; mutation/network rejects; self-approval rejects by actor/session separation; adapter cannot mint receipts; rejected runs create no receipt/transcript; hostile fake stdio server cannot see non-allowlisted env, real HOME, or broad CWD; registration rejects mutation, network, PR, deployment, Pendo, credential, broad-Claude, and live-write actions.

Acceptance rule: integration is not accepted until the offline witness and the negative tests pass.

## Final Verdict

Proceed with `McpChatWitnessAdapter` as a local adapter admission harness. Do not integrate external MCP/chat/browser tools yet. L0.5 succeeds only when the existing kernel proves that adapter proposals remain blocked until approval, adapter execution is allowlisted and offline, evidence is hash-bound, and receipts are minted only by the kernel.

## Next Implementation Slice

Add the adapter descriptor schema, `DesignFeedbackContextPacket` schema/fixture, fake stdio MCP witness server, registration validator, evidence artifact writer, hash binding helper, and a focused L0.5 smoke/negative test suite extending the current L0 approval/receipt loop.
