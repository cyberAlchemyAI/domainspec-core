---
id: ide-extension-spec
project: ide-extension
title: "ide-extension - L0/L0.5 Witness Contract"
status: draft
node_type: spec
updatedAt: 2026-07-10
---

# ide-extension - L0/L0.5 Witness Contract

## Definition

`ide-extension` is a local, IDE-adjacent governance workbench. It binds
IDE-visible intent, module manifests, external agent envelopes, human approval
gates, and evidence receipts into one auditable action boundary.

## In Scope For L0

- Local Node server, loopback-only by default.
- HTML workbench at `/demo/l0`.
- Module manifest registry.
- Agent envelope preparation and dry-run no-op receipts.
- Approval queue for any action with effects beyond preview/read.
- Durable state under `.ide-extension/state/`.
- JSON schemas for manifests, envelopes, and receipts.
- OpenRouter provider adapter shape, with keys staying server-side.
- Optional later VS Code/VSCodium wrapper around the same local workbench URL.

## In Scope For L0.5 MCP/Chat Admission

L0.5 admits MCP/chat capabilities only through a deterministic local witness.
It does not integrate real external MCP servers, Claude delegation, Yocoolab,
Chrome DevTools, Kernel Cloud, live browser sessions, GitHub, Pendo, deployment,
or networked providers.

The first L0.5 proof is:

- `McpChatWitnessAdapter`, registered as a local adapter descriptor;
- fake/local stdio MCP server only;
- one allowlisted `observe` tool;
- `DesignFeedbackContextPacket` fixture with selected element, page URL,
  screenshot/artifact ref, selection history, source-candidate hypotheses,
  companion message, and context refs;
- explicit env allowlist, fixture CWD, temp/redacted HOME, `network: false`,
  `mutation: false`, and `receipt_authority: false`;
- adapter evidence written as local artifacts;
- receipt minted only by the local kernel through existing receipt semantics.

If a dry run is tested, it is a separate kernel dry-run envelope class. It is
not treated as an MCP adapter tool action.

## Out Of Scope For L0

- Autonomous IDE execution.
- Embedded VSCodium webview automation as proof.
- Direct Craft or Whisper authority mutation.
- Provider credentials in browser code.
- Browser-act, shell, fs write, network, export, commit, push, or publication
  without explicit approval and receipt.
- Multi-user or remote-host guarantees.
- Marketplace packaging.

## Out Of Scope For L0.5 MCP/Chat Admission

- Self-approval by chat, model, MCP server, browser extension, or adapter.
- Direct durable-state mutation outside the local kernel.
- Adapter-minted or remote-issued receipts.
- Browser/webview credential storage.
- Broad Claude Code tool access or unconstrained inherited HOME/CWD/env.
- Direct PR, Pendo, deployment, GitHub write, public-submit, credential,
  wallet/signature, payment, or destructive automation.
- Live authenticated sensitive Chrome control.
- Treating MCP tool descriptions, model output, browser state, or remote service
  assertions as local authority.

## Required State Files

| Path | Purpose |
| --- | --- |
| `.ide-extension/state/workbench.json` | Current workbench read model. |
| `.ide-extension/state/events.jsonl` | Append-only local event/receipt log. |
| `.ide-extension/state/artifacts/` | Local artifact refs for witness outputs. |

## Module Contract

Every module must have a manifest that declares:

- stable `module_id`;
- owner route;
- source refs;
- capabilities;
- allowed effects;
- required gates;
- forbidden effects;
- expected receipts.

The kernel can list and validate modules. The module does not become authority
by being visible in the workbench.

## Agent Envelope Contract

An agent envelope represents a proposed boundary crossing. It must name:

- envelope and run ids;
- agent ref;
- task;
- context refs;
- requested grants;
- required approval;
- current typestate;
- expected receipts.

L0 typestate:

```text
draft -> prepared -> awaiting_approval -> running -> passed|flagged|blocked|failed|interrupted|timeout
```

In this scaffold, `running` is a no-op dry run only after approval.

For L0.5 MCP/chat admission, an envelope may be prepared by a chat or MCP
surface, but the proposing actor, approving actor/session, adapter invocation,
and receipt append must remain separable. A proposal cannot approve itself.

## Receipt Contract

Every approved action writes a receipt with:

- `receipt_id`;
- `run_id`;
- `stage`;
- `status`;
- `before_ref`;
- `after_ref`;
- `approval_id`;
- `evidence_refs`;
- `created_at`.

L0.5 adapter evidence must bind through `evidence_refs` and kernel-written
artifacts unless the receipt schema is intentionally evolved. Required bound
evidence includes `envelope_id`, `approval_id`, `adapter_id`,
`adapter_descriptor_hash`, `tool_allowlist_hash`, `context_packet_sha256`,
`transcript_sha256`, artifact refs and hashes, before/after digest, custody
statement, and redacted env/CWD/HOME descriptor.

## Acceptance

L0 is accepted only when a smoke test proves:

1. server boots;
2. `/demo/l0` renders;
3. module manifests load;
4. prepare creates a pending approval;
5. run is blocked before approval;
6. approve records a no-op receipt;
7. state and events persist outside browser memory.

L0.5 MCP/chat admission is accepted only when tests prove:

1. adapter descriptor registration accepts only the offline stdio witness shape;
2. a proposal prepares a pending approval;
3. run before approval is blocked and invokes nothing;
4. one explicit approval permits exactly one allowlisted observe call;
5. the adapter invokes only after approval;
6. the kernel appends the receipt with evidence refs and binding artifacts;
7. forged, wrong, expired, and reused approvals reject;
8. non-allowlisted, mutation, network, PR, deployment, Pendo, credential,
   broad-Claude, and live-write actions reject;
9. self-approval rejects by actor/session separation;
10. rejected runs create no receipt or transcript;
11. a hostile fake stdio server sees only allowlisted env, temp/redacted HOME,
    and bounded fixture CWD.
