---
id: ide-extension-spec
project: ide-extension
title: "ide-extension - L0/L0.5 Witness Contract"
status: draft
node_type: spec
updatedAt: 2026-07-12
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
- Approval queue for protected actions with effects beyond preview/read.
- Durable state under `.ide-extension/state/`.
- JSON schemas for manifests, envelopes, and receipts.
- OpenRouter provider adapter shape, with keys staying server-side.
- Optional later VS Code/VSCodium wrapper around the same local workbench URL.

## L0 Manual Session Bridge Contract (Version 2)

The manual session bridge extends L0 without replacing the legacy dry-run
witness. The operator prepares a concrete task and safe skill slug, approves
the request, selects exactly one approved envelope as `ready_for_poll`, and
then says `poll` in the intended Codex session. The local kernel remains the
authority for target selection, claim admission, state, artifacts, and receipts.

The bridge effect profile is exactly:

```json
["preview.read", "skill.invoke"]
```

`skill.invoke` is invalid without `preview.read` and cannot be combined with
`dry-run.noop`, writes, shell execution, network, provider, browser-act, commit,
push, publication, or any unknown effect. The server does not resolve or run
the skill. The active session resolves it only after a successful atomic claim.

Version 2 lifecycle:

```text
draft -> prepared -> awaiting_approval -> approved -> ready_for_poll -> claimed
claimed -> passed|flagged|blocked|failed
claimed -> interrupted -> approved
```

The `interrupted -> approved` transition requires an explicit local operator
release/requeue action and preserves prior claim attempts. Authorization stays
active through targeting, claim, interruption, and read-only requeue; an
admitted terminal result consumes it. Timed leases, automatic retry, technical
effect sandboxing, and authenticated session identity are outside L0.

All v2 request records carry `schema_version: "2"` and explicit actor or
session bindings. Pre-claim responses omit task and skill. The successful claim
packet is the first agent-facing bridge response that reveals them.

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
  outside the trusted-local canvas preview/display exception without explicit
  approval and receipt.
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

Every action admitted through a protected-effect approval writes a receipt
with:

- `receipt_id`;
- `run_id`;
- `stage`;
- `status`;
- `before_ref`;
- `after_ref`;
- `approval_id`;
- `evidence_refs`;
- `created_at`.

The trusted-local canvas exception defined below does not enter this approval
or receipt lifecycle. Its canvas events are local audit evidence, not receipt
records under this contract.

L0.5 adapter evidence must bind through `evidence_refs` and kernel-written
artifacts unless the receipt schema is intentionally evolved. Required bound
evidence includes `envelope_id`, `approval_id`, `adapter_id`,
`adapter_descriptor_hash`, `tool_allowlist_hash`, `context_packet_sha256`,
`transcript_sha256`, artifact refs and hashes, before/after digest, custody
statement, and redacted env/CWD/HOME descriptor.

The receipt schema is a non-overlapping union:

- legacy receipts have no `receipt_kind` and preserve the existing dry-run shape;
- `authorization.receipt` binds task, skill/grant hashes, policy version,
  approval, and the unattested local operator action, but has no execution status;
- `skill.execution` binds authorization, claim attempt, unattested session,
  resolved skill hash, terminal result, validation, and evidence artifacts.

Approval alone never creates a `skill.execution` receipt or terminal execution
state. Chat output alone is not completion evidence; the kernel must admit a
bound result and mint the execution receipt.

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

## Session Content Workbench V0 Contract

The trusted-local V0 adds a separate interactive canvas protocol. It does not
attach content to a terminal bridge result. A Codex session publishes a complete
project HTML file by normalized workspace-relative path, and later polls named
interaction events while the session remains active.

Canvas publication and display are a narrow trusted-local preview/read
exception. Publication reads an operator-controlled workspace HTML artifact and
mutates only the local canvas projection and displayed revision. It does not
write the source file or authorize shell, filesystem write, network, provider,
browser-act, Craft or Whisper action, export, commit, push, or remote
publication. Those protected effects retain their owning approval and receipt
requirements.

`canvas.surface_published` is an append-only audit event binding surface and
revision metadata. It is evidence that local canvas publication occurred, but
it is not a receipt record under the Receipt Contract and carries no protected-
effect execution authority.

Canvas request contracts use `schema_version: "1"`:

- `canvas-publish-request` requires `path`, `title`, and `kind`;
- `kind` is `presentation`, `decision`, `craft`, or `generic`;
- `path` is a normalized relative `.html` path with no absolute, traversal,
  backslash, or percent-encoded form;
- `canvas-interaction-request` requires `surface_id`, `revision_id`,
  `event_name`, and a JSON-object `payload`;
- the complete interaction request is limited to 16 KiB at the HTTP boundary.

Projected canvas records are:

- `CanvasSurface`: stable id, normalized path, title, kind, current revision,
  and ordered revision ids;
- `CanvasRevision`: revision id, surface id, SHA-256, byte length, and publish
  timestamp for the bytes returned by one opened-file read; this is not an
  atomic filesystem snapshot against a concurrent writer;
- `CanvasInteraction`: stable event id, monotonic cursor, current surface and
  revision bindings, event name, payload, and receive timestamp.

One normalized path identifies one logical surface. Republishing the same path
with changed bytes preserves `surface_id` and creates a revision. Republishing
the same hash is idempotent. The workspace file remains canonical; if its bytes
change before republish, the content route reports `revision_changed` instead of
claiming the old revision is still available.

V0 has one global current canvas and append-only interaction stream. Historical
snapshots, authenticated per-session routing, hostile HTML containment, remote
access, and effect completion are deferred. A `craft.action.requested` event is
a request, not evidence that Craft completed.
