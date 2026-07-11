# Turing, Alan - Agent And Session Protocol Return

## INITIAL POSITION

Nimbalyst is strongest as a source-backed protocol and transcript precedent, not as
an agent authority to embed. Its MIT client contains real adapters for Claude Code,
Codex, and OpenCode, a normalized session protocol, provider-native raw event
capture, resume/recovery handling, MCP injection, worktree/session grouping, and a
Claude-specific teammate controller. Those mechanisms can shorten
`ide-extension` design and parser work. They cannot be imported as the local
approval or receipt boundary: Nimbalyst's own SDK contract says permission remains
provider-private, while `ide-extension` requires the kernel to own approval,
durable state, and receipt append.

Evidence scope is Nimbalyst commit
`c8ca207c6004653ba2df3d81e06133ce2e9fad3d`, official documentation, and the
accepted local architecture. Source links below use that immutable revision.

## Evidence Labels

- **Observation**: directly stated or implemented by cited evidence.
- **Inference**: the smallest architectural consequence supported by observations.
- **Recommendation**: a local choice; it is not a claim about current Nimbalyst behavior.

## 1. Provider And Protocol Map

**Observation.** The extension SDK owns a provider-neutral `AgentProtocol` with
`createSession`, `resumeSession`, `forkSession`, `sendMessage`, `abortSession`, and
`cleanupSession`. `SessionOptions` carries workspace, model, abort signal,
permission mode, MCP servers, environment, and allow/deny tool lists. Its stream
normalizes raw, text, reasoning, tool-call, tool-result, error, completion, usage,
and planning-mode events. See
[`AgentProtocol.ts` lines 62-94, 147-205, 207-275](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/agents/AgentProtocol.ts).

**Observation.** The host side deliberately does not normalize permission requests
or user questions yet. `AgentProtocolHost` says those stay provider-private;
`permissionMode` is advisory and provider code remains authoritative at tool-call
time. Its five host methods instead cover raw logging, API-key lookup, brokered
workspace read/write, and MCP tool registration. See
[`AgentProtocolHost.ts` symbols `PermissionMode` and `AgentProtocolHost`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/agents/AgentProtocolHost.ts).

**Observation.** `ProviderFactory` caches built-in providers by
`<provider>-<sessionId>` and constructs separate Claude Code SDK/CLI, Codex SDK/ACP,
OpenCode, and extension-contributed providers. Extension providers lazy-start a
privileged backend module after first-use consent. See
[`ProviderFactory.createProvider` and `createExtensionAgentProvider`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/ProviderFactory.ts).

**Inference.** The reusable seam is a lifecycle/event anti-corruption layer. The
permission surface is not reusable as the local authority contract because it
would leave approval split among provider implementations.

### Interface Translation

| Nimbalyst interface | Local translation | Custody rule |
|---|---|---|
| `SessionOptions.workspacePath` | envelope context/artifact ref plus bounded adapter CWD | Kernel validates scope before spawn. |
| `createSession` / `resumeSession` | `prepare` followed by approved `run` | Adapter may return provider session ID; kernel owns run ID. |
| `sendMessage` event stream | `collect` into transcript evidence | Raw provider events are evidence, never receipts. |
| `abortSession` | `interrupt` | Kernel records requested and observed termination separately. |
| `cleanupSession` | adapter resource cleanup | Cleanup success does not imply run success. |
| `permissionMode`, allow/deny tools | adapter capability declaration | Kernel grants and exact approval supersede provider policy. |
| MCP server options | custody descriptor plus allowlist hash | Kernel resolves credentials; adapter gets only approved material. |

## 2. Session And Process Sequences

### New Or Resumed Turn

```text
Human -> ide kernel: prepare(agent, task, context, requested grants)
kernel -> envelope store: awaiting_approval
Human -> kernel: approve exact envelope/run
kernel -> adapter: run(run_id, bounded cwd/env/MCP, prior provider_session_id?)
adapter -> Claude/Codex/OpenCode runtime: create or resume
runtime -> adapter: provider session id + native stream
adapter -> kernel: raw/text/tool/error/complete evidence events
kernel -> artifact store: append transcript evidence + hashes
kernel -> receipt log: append terminal receipt linked to approval_id
```

**Observation.** OpenCode chooses resume when its provider-session store has an ID,
passes workspace/MCP/environment/abort options to the protocol, stores raw events,
then persists a newly observed protocol session ID. A missing workspace produces an
error event. See
[`OpenCodeProvider.sendMessage`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/providers/OpenCodeProvider.ts).

**Observation.** Claude Code checks that a resumed SDK session reports the requested
ID and fails loudly on mismatch; expired provider context is marked expired while
the visible Nimbalyst transcript remains. See
[`ClaudeCodeProvider.sendMessage`, `session_id` and `expired_session_error` branches](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/providers/ClaudeCodeProvider.ts).

**Observation.** Codex evicts and kills a cached live protocol session after a
non-abort stream error but preserves the persisted thread ID so a fresh child can
resume next turn. Abort clears pending questions and rejects pending permissions;
destroy cleans all child sessions. See
[`OpenAICodexProvider.evictLiveProtocolSession`, `abort`, and `destroy`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/providers/OpenAICodexProvider.ts).

### Recovery State Machine

```text
prepared -> awaiting_approval -> running
running -> passed | flagged | blocked | failed | interrupted | timeout

provider child crash:
  running -> failed; drop live handle; retain opaque resume token as evidence
next approved run:
  try resume token -> matching session: running
                   -> mismatch/expired: blocked or failed, never silent fresh start
interrupt:
  request abort -> await process/stream observation -> interrupted receipt
cleanup:
  release process only; do not rewrite the terminal outcome
```

**Recommendation.** Preserve Nimbalyst's fail-loud resume identity check. Do not
adopt its automatic fresh-process recovery without a new local approval: a new
process can preserve a provider thread, but it is still a new effectful crossing.

## 3. Transcript And Tool Events

**Observation.** Nimbalyst persists provider-native payloads in
`ai_agent_messages` as the append-only source of truth. Canonical events are rebuilt
in memory through pure provider parsers, a writer, and a projector; providers never
write canonical events directly. Claude resume relies on the SDK's own history,
not this transcript. See
[`TRANSCRIPT_ARCHITECTURE.md` storage and data-flow sections](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/TRANSCRIPT_ARCHITECTURE.md).

**Inference.** This is the best concrete reuse precedent: retain immutable raw
events and derive a stable UI projection. It prevents provider schema churn from
becoming kernel state churn.

**Recommendation.** Adapt the pattern, not the database stack:

1. Store redacted raw event artifacts keyed by `run_id`, provider, sequence, and
   native event ID.
2. Project only `text`, `reasoning`, `tool_call`, `tool_result`, `error`, `complete`,
   and usage into a local canonical view.
3. Correlate tool call/result IDs and hash the final transcript artifact.
4. Let the kernel mint one receipt referencing that hash. Never translate a
   provider `complete` event directly into `passed`.

## 4. Commands, Skills, Teams, MCP, And Worktrees

### Commands And Skills

**Observation.** Claude Code provider initialization receives SDK-reported skills
and commands and keeps a process cache; Nimbalyst also ships Claude plugin commands
and `SKILL.md` packages under extension folders. This is discovery and presentation,
not a common executable command protocol. Source:
[`ClaudeCodeProvider` fields `skills`, `cachedSdkSkills`, and init handling](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/providers/ClaudeCodeProvider.ts).

**Recommendation.** Use a read-only `describe` result with `{kind, name, source_ref,
provider, invocation_hint}`. Invocation still becomes a new envelope. Do not copy
provider slash-command text into kernel policy.

### Agent Teams

**Observation.** Nimbalyst's teammate layer intercepts Claude team tools, manages
running/idle/completed state, queues messages, resumes idle teammates, persists team
context, and implements shutdown. These are Nimbalyst additions over Claude SDK
facilities. Codex explicitly disables teams. See
[`TEAMMATE_IMPLEMENTATION.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/TEAMMATE_IMPLEMENTATION.md)
and [`OpenAICodexProvider.buildSystemPrompt`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/providers/OpenAICodexProvider.ts).

**Recommendation.** **Defer.** A team adapter would multiply process, grant,
transcript, and termination identities before the single-agent receipt invariant is
proved. Later, model each teammate as a child run with its own envelope and joined
parent receipt; never treat provider team state as kernel state.

### MCP Configuration And Custody

**Observation.** Official docs describe user- and workspace-level MCP servers and
claim local connections and local credential storage. The client implementation
shares Claude user MCP config through `~/.claude.json`, workspace config through
`.mcp.json`, and migrates/deletes a legacy file; project-local scope inside
`~/.claude.json` is noted as unimplemented. See [official MCP docs](https://docs.nimbalyst.com/setup-nimbalyst/mcp)
and [`MCP_CONFIG_MIGRATION.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/MCP_CONFIG_MIGRATION.md).

**Recommendation.** **Do not adopt custody.** Read only an explicitly admitted,
redacted descriptor; materialize a per-run temporary config after approval; pass an
environment allowlist; hash descriptor/tool allowlist; remove it on cleanup. Shared
home-file migration or mutation is outside the minimal adapter.

### Worktrees

**Observation.** Official docs expose per-worktree AI sessions and terminals, with
auto-stashing for rebase. In source, the worktree row is the container and sessions
are flat siblings; worktree plus parent-session nesting is invalid. The Git service
locks operations and has explicit partial-success outcomes where rebase succeeds
but stash restoration fails. See [official worktree docs](https://docs.nimbalyst.com/code-and-coding-with-nimbalyst/worktrees),
[`SESSION_HIERARCHY.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/SESSION_HIERARCHY.md),
and [`GitWorktreeService.rebaseFromBase`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/services/GitWorktreeService.ts).

**Recommendation.** Use this only as failure-semantics precedent. A worktree path,
branch, and HEAD become context/evidence refs. Creation, rebase, merge, archive, and
remove each require separate grants and receipts. Partial success must be `flagged`,
not `passed`.

## 5. Authority And Failure Matrix

| Concern | Nimbalyst owner | Required local owner | Failure meaning |
|---|---|---|---|
| Provider process/session | Provider class + protocol adapter | Admitted adapter under kernel run | Crash loses live handle, not necessarily resume token. |
| Transcript raw log | Nimbalyst repository/database layer | Kernel artifact store | Projection can be rebuilt; missing raw sequence blocks proof. |
| Tool permission | Provider-private permission service/UI | Kernel grants + approval queue | Denial/timeout is blocked or failed, never provider-approved receipt. |
| Tool execution | Coding-agent runtime/MCP server | External runtime after exact grant | Tool result is evidence; kernel adjudicates terminal status. |
| MCP config/credentials | Nimbalyst/Claude config and provider | Kernel custody descriptor | Missing/redacted credential blocks launch; no ambient HOME fallback. |
| Team lifecycle | Claude SDK plus `TeammateManager` | Deferred child-run coordinator | Orphan/idle teammate prevents parent pass. |
| Worktree/git | `GitWorktreeService` + stores | Separate future git adapter | Partial git/stash recovery is flagged with residue. |
| Resume | Provider session store + native runtime | Kernel run state + opaque adapter token | ID mismatch/expiry fails loud and requires user-visible recovery. |
| Receipt | No equivalent kernel receipt authority | ide-extension kernel only | Adapter can submit evidence, never mint or append receipt. |

Nimbalyst's permission implementation includes `allow-all` and `bypass-all`,
session caches, and provider pattern files; it warns that wildcard allowed tools can
bypass callbacks. This is useful threat evidence, not a local design to inherit.
See [`AGENT_PERMISSIONS.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/AGENT_PERMISSIONS.md).

## 6. Minimal Adapter Options

### A. Protocol Vocabulary Adapter - ADAPT NOW

Implement no Nimbalyst dependency. Borrow the six lifecycle methods and nine core
event kinds into an `ExternalAgentAdapter` descriptor mapped to the existing
`describe/prepare/run/collect/interrupt/inspect` envelope strategy.

- Dependencies: Node child-process/stream primitives and existing local schemas.
- Authority cost: low; kernel remains sole approver and receipt appender.
- Acceptance witness: fake stdio agent emits text, one tool call/result, complete,
  malformed event, crash, timeout, and resume mismatch; every effectful run blocks
  before approval and produces one kernel receipt only after evidence collection.
- Development-time reduction: **medium**, because provider adapters share one tested
  state and event vocabulary.

### B. Raw-To-Canonical Transcript Extract - ADAPT AFTER L0.5

Port selected pure parser ideas/types, with MIT notice, only after fixtures identify
which provider-native formats are required. Do not port PGLite/Electron UI.

- Dependencies: provider fixture corpus, artifact hashing, pure projectors.
- Authority cost: low; projection is non-authoritative.
- Acceptance witness: replayed fixtures produce deterministic events and transcript
  hash; unknown events remain preserved in raw evidence.
- Development-time reduction: **medium to high** once two providers are admitted;
  premature for the single fake MCP witness.

### C. Provider Runtime, Team, MCP, Or Worktree Extraction - DEFER/KILL FOR L0

Directly importing provider classes pulls Electron/runtime storage, provider-private
permission paths, ambient process/environment behavior, MCP home-file custody, and
provider-specific recovery into the kernel boundary. Team and worktree code add
large independent state machines.

- Minimum safe witness is not currently small enough for L0/L0.5.
- Development-time reduction: **negative initially** due to dependency and authority
  adaptation.
- Disposition: **DEFER** as source precedent; **KILL** direct embedding as the first
  adapter.

## 7. License And Product Boundary

**Observation.** The inspected client repository is MIT and requires preservation
of its copyright and permission notice in copied substantial portions. Its
`LICENSING.md` states that the collaboration sync server powering
`wss://sync.nimbalyst.com` is a separate project. See
[`LICENSE`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/LICENSE)
and [`LICENSING.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/LICENSING.md).

**Inference.** Client source supports claims about local provider/session behavior.
It does not license or prove the implementation of the separate collaboration
server. Official mobile claims such as remote approval, resume, and desktop sync
describe hosted/mobile surfaces, not an open-client-only integration guarantee; see
the [official Quickstart](https://docs.nimbalyst.com/getting-started/quickstart).

**Recommendation.** Keep all hosted sync, mobile custody, and cross-device approval
out of the adapter candidate. Revisit only with separately licensed server evidence
and an explicit remote-approver threat model.

## FINAL POSITION

Adopt Nimbalyst's **shape**, not its authority: a provider-neutral lifecycle,
provider-native raw events, pure canonical projections, explicit abort/cleanup, and
fail-loud resume identity are credible development-time reducers. The smallest
compatible local move is Option A behind the existing agent envelope, followed by
Option B only when a second real provider justifies parser reuse. Direct provider,
permission, MCP-custody, team, worktree, collaboration-server, or mobile integration
would bypass or overload the accepted kernel boundary and should not enter the
current layer.

This preserves the local invariant in
`projects/ide-extension/ARCHITECTURE.md`: adapters propose and emit evidence; the
kernel alone approves effects, owns durable run state, and appends receipts.

## ROBOT-TALKS CONFRONTATION

### 1. Product Grammar Versus Code Reuse - REVISE

My initial Option A said "borrow" the lifecycle vocabulary but labelled it
`ADAPT NOW`, which could be read as a source port. I revise that claim: **locally
express the contract; do not copy `AgentProtocol.ts` for the first witness**.

Exact evidence: the useful upstream protocol is only six lifecycle methods and a
small event union
([`AgentProtocol.ts`, `ProtocolEventType` and `AgentProtocol`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/agents/AgentProtocol.ts#L147-L275)),
while the local architecture already names `describe`, `prepare`, `run`, `collect`,
`interrupt`, and `inspect` (`projects/ide-extension/ARCHITECTURE.md`, "Agent
Envelope Strategy"). Copying adds MIT notice, upstream-diff, and semantic-mapping
work without removing local schema or kernel tests. Simon's evidence/diff and
task-session-artifact links remain product hypotheses, not SDK evidence
(`simon-product-workflow.md`, "Candidate Reuse Units And Initial
Recommendation").

Hewitt establishes a different bounded seam: `createReadOnlyHost` is Electron-free
and the public SDK has no runtime dependencies, although it peer-depends on
React/Vite/Tailwind/Yjs surfaces (`hewitt-source-architecture.md`, "Extension host
seam"). That may justify a later port for an isolated editor specimen; it does not
justify copying the agent protocol.

### 2. SDK Seam Versus Authority Coupling - HOLD

I hold that the public TypeScript boundary is **not authority-safe as a whole**.
Exact evidence: `AgentProtocolHost` calls `permissionMode` advisory and leaves
tool-call authorization provider-private
([`AgentProtocolHost.ts`, `PermissionMode`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/agents/AgentProtocolHost.ts#L46-L62));
it also brokers durable raw logging, API-key resolution, workspace writes, and MCP
registration
([`AgentProtocolHost`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/agents/AgentProtocolHost.ts#L101-L220)).
`EditorHost` includes direct save, namespaced storage, editor API, AI-tool, and
collaboration surfaces (`hewitt-source-architecture.md`, "Extension host seam").
Backend-module permissions explicitly permit ambient Node `fs`, `net`, and
`child_process`, and built-ins are auto-granted (`hewitt-source-architecture.md`,
"Privileged extensions and permission cost").

Therefore only pruned read-only types/helpers may cross. `saveContent`, secrets,
MCP registration, native modules, provider permission, and receipt creation must be
replaced by local proposal/evidence interfaces.

### 3. Provider/Event Projection - HOLD

I hold the raw-provider-event plus pure-projection pattern because it improves both
recovery and the user workflow without transferring authority. Nimbalyst persists
provider-native messages as its sole transcript source and rebuilds canonical
events through pure per-provider parsers
([`TRANSCRIPT_ARCHITECTURE.md`, storage and parsers](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/TRANSCRIPT_ARCHITECTURE.md#storage-model)).
Simon identifies the corresponding user job: inspect full history, tool calls, and
files touched without reconstructing a session (`simon-product-workflow.md`, "User
Jobs" 3 and 5). The projection therefore improves orientation and recovery, but a
provider `complete` remains evidence, not a kernel `passed` receipt.

Hewitt's coupling evidence narrows implementation: do not import the private
runtime, repositories, PGLite/SQLite, Electron IPC, or UI projector
(`hewitt-source-architecture.md`, "Storage and IPC"). Ashby's process/custody gate
also applies: fixtures must use redacted HOME, fixture CWD, explicit environment
allowlist, no network, process-tree cancellation, and zero-egress tests
(`ashby-safety-operations.md`, "Evidence Required Before Adoption" 2, 5, and 6).
Thus the independently reusable unit is a pure parser/projection over captured
fixtures, only after two provider formats create real duplication.

### 4. Diff Approval - REVISE

I revise the candidate to **presentation-only and gated on materialized after-state
evidence**. Nimbalyst documents red/green Keep/Undo, but its agent may already have
performed filesystem operations; Ashby correctly distinguishes post-effect review
from pre-effect authorization (`ashby-safety-operations.md`, "Claimed-Versus-Enforced
Control Map", "Visual diff approval"). Simon independently says the current local
project lacks materialized/validated after-state evidence and places the viewer
after L0 repairs (`simon-product-workflow.md`, "Evidence/diff viewer").

The admissible sequence is `approved effect -> captured before/after artifacts ->
validated hashes -> diff projection -> accept/discard presentation`. A diff click
cannot approve an unexecuted effect, prove actor attribution, or mint a receipt.
Kill any candidate that conflates Keep/Undo with kernel approval.

### 5. Tasks, Workstreams, And Session Links - REVISE

I revise this to a **distinct read-only join projection, with no copied tracker or
status model**. Nimbalyst demonstrates links among plans, sessions, and touched
files (`simon-product-workflow.md`, "Tasks / tracker mode"), but Simon also records
material overlap with Craft and warns that copying the tracker creates a second
canonical ledger. The local candidate is only a view over existing identifiers:
`governed_task_ref -> envelope_id/run_id -> evidence_refs -> receipt_id`.

This adds a distinct navigation projection when it resolves those existing refs in
one place. It is duplication and must be killed if it stores independent task
status, invents workstream authority, promotes a route, or permits edits to Craft or
Arcanum-owned state. Session kanban/status lanes remain deferred until the accepted
approval replay and persistence defects are repaired (`simon-product-workflow.md`,
"Prepared/approval/receipt queue").

### 6. Permission, MCP, And Session Execution - CONCEDE

I concede Ashby's stronger kill boundary for direct execution-layer reuse. The
Nimbalyst permission service supports reusable session/permanent patterns and
`allow-all`/`bypass-all`; its own documentation warns that wildcard allowed tools
can bypass the callback
([`AGENT_PERMISSIONS.md`, storage and SDK configuration](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/AGENT_PERMISSIONS.md#storage)).
MCP configuration shares `~/.claude.json`, may contain environment secrets, and has
provider/home custody
([`MCP_CONFIG_MIGRATION.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/MCP_CONFIG_MIGRATION.md)).
Terminal, Git/worktree, sync/mobile, telemetry, and updater surfaces each add an
independent authority or operations plane (`ashby-safety-operations.md`, "Adoption
Dispositions").

What survives independently is narrower: locally authored lifecycle/event types;
later pure transcript parsers over fixtures; pruned manifest-validation ideas; the
Electron-free read-only host as a separately evaluated specimen; and presentation
projections. None may spawn, resolve credentials, approve tools, mutate durable
state, or append receipts.

### 7. Development-Time Accounting - REVISE

I revise all savings claims to include total ownership cost:

| Candidate | Extraction | Adaptation | Tests | Provenance | Upgrade | Abandonment | Net decision |
|---|---|---|---|---|---|---|---|
| Local lifecycle/event contract | None; re-express about six methods and event tags | Map to existing envelope states | Fake stdio, crash, timeout, mismatch, forged receipt | Record precedent only; no copied code | Local schema owner; optional upstream comparison | Delete adapter/types with no migration | **ADOPT locally**, low total cost. |
| `createReadOnlyHost` specimen | Small source/test port | Prune `EditorHost` to read-only local contract | Render, no-write, no-network, dependency and schema tests | Pin symbol/SHA and preserve MIT notice | Frozen local fork plus explicit upstream-diff trigger | Remove specimen; no durable state | **DEFER then ADAPT** if an editor witness is selected. |
| Manifest validator pattern | Select fields/fixtures, not whole schema | Translate to local Draft 2020-12 descriptors | Positive/negative schema and unknown-field tests | Precedent or exact copied helpers ledger | Local schema evolves independently | Regenerate/remove fixtures | **ADAPT pattern**, not package. |
| Raw/canonical transcript parser | Extract only required pure parsers after two providers | Map to local event union and redaction | Fixture replay, unknown event, ordering, correlation, hash determinism | Per-symbol MIT ledger | Provider-format compatibility owner and pinned fixtures | Keep raw evidence; discard projector and rebuild | **DEFER**, then ADAPT if duplication is measured. |
| Diff projection | No upstream code initially | Render local before/after evidence and disposition | Missing/stale/hash-mismatch/attribution and accessibility tests | Product precedent only | Local evidence schema owner | Remove viewer; artifacts remain valid | **PRECEDENT now; ADOPT local presentation after L0 repairs.** |
| Task-session-artifact join | No upstream code | Resolve Craft/Arcanum/envelope/receipt refs read-only | Broken/stale/unauthorized ref and no-write tests | Product precedent only | Track local owner schemas | Remove projection; canonical ledgers remain | **ADOPT local projection only when a concrete user query justifies it.** |
| Provider/permission/MCP/process stack | High despite available code | Replace authority, storage, env, credentials, and recovery | Cross-provider security, cancellation, concurrency, custody, egress | Large MIT/dependency ledger | Continuous SDK/security drift | Sessions/config/migrations make exit expensive | **KILL direct reuse.** |
| Teams/worktrees/sync/mobile/storage/Electron | High to very high | Multiple new state and service authorities | Git recovery, process, crypto, remote identity, migration, supply-chain suites | Multi-package/service boundary | High recurring operations burden | Stateful and service-coupled | **KILL L0/L0.5; precedent or separate future program.** |

The first contract saves design time because it creates no second policy/session
authority. The read-only host and parsers save time only if their bounded witnesses
cost less than local implementation after provenance, negative tests, upgrades, and
deletion are priced. All execution-stack reuse fails that test.

## REVISED FINAL POSITION

Shared-ready candidate list:

| ID | Candidate | Revised recommendation |
|---|---|---|
| `NIM-AG-01` | Locally owned external-agent lifecycle and event vocabulary | **ADOPT** local expression; Nimbalyst is cited precedent, not copied authority. |
| `NIM-AG-02` | Electron-free read-only editor-host specimen | **DEFER**, then **ADAPT** a pinned minimal port only for a selected visual-editor witness. |
| `NIM-AG-03` | Local manifest/descriptor validation fixtures and package smoke checks | **ADAPT** the pattern; do not import the full Nimbalyst manifest. |
| `NIM-AG-04` | Provider-native raw evidence plus pure canonical transcript projection | **DEFER**, then **ADAPT** parsers only when two admitted providers prove duplication. |
| `NIM-UX-01` | Before/after evidence diff viewer | **PRECEDENT** now; **ADOPT** local presentation only after materialized evidence and L0 repairs. |
| `NIM-UX-02` | Governed task-session-artifact-receipt join | **ADOPT** only as a read-only local projection; **KILL** any parallel tracker/status authority. |
| `NIM-BR-01` | Browser tool vocabulary | **PRECEDENT** for the existing typed MCP/Playwright adapter lane. |
| `NIM-EX-01` | Nimbalyst provider, permission, MCP custody, terminal, Git/worktree execution | **KILL** direct reuse in L0/L0.5. |
| `NIM-EX-02` | Teams, Electron/runtime/storage, collaboration server, sync/mobile, telemetry, updater | **KILL** as an integration shortcut; **DEFER** only as separately governed future programs. |

The converged position is narrower than my initial return: Nimbalyst reduces local
development time chiefly as pinned precedent and as a source of a few independently
testable, presentation-side contracts. The immediate implementation-worthy unit is
a **locally authored** lifecycle/event vocabulary behind the existing envelope. No
Nimbalyst execution, permission, session store, credential, MCP, process, Git,
remote, or receipt authority crosses the kernel boundary. Code is copied only when
a concrete witness proves that extraction plus adaptation, tests, provenance,
upgrade, and abandonment cost less than implementing against the already-owned
local contract.
