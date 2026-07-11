# Hewitt Source Architecture Return

Identity: Hewitt, Carl
Role: computational source-architecture explorer
Inspected upstream: `Nimbalyst/nimbalyst@c8ca207c6004653ba2df3d81e06133ce2e9fad3d`
Inspection date: 2026-07-11

## INITIAL POSITION

Nimbalyst is useful to `ide-extension` primarily as a pinned architecture and API specimen, not as an application substrate. Its strongest bounded reuse seam is the TypeScript contract in `packages/extension-sdk`: manifest contribution types, `EditorHost`, editor lifecycle hooks, read-only host construction, manifest validation, and collab codec interfaces. Those units demonstrate a host-owned capability model with extension-owned presentation and can shorten local contract design. They still require a local adapter because Nimbalyst's contract allows host behaviors and native backend modules that conflict with the accepted `ide-extension` rule that adapters propose/observe while the local kernel owns approval, mutation, evidence, and receipts.

The Electron application, private `@nimbalyst/runtime`, browser implementation, storage layer, and collaboration clients are not low-cost libraries. They form a large coupled product graph around Electron main/preload/renderer IPC, native modules, multiple agent SDKs, PGlite/SQLite repositories, and a separately operated collaboration server. Copying those areas would import maintenance and authority assumptions faster than it removes implementation work.

## Evidence Discipline

- **Observation** means directly present in official documentation or the pinned source.
- **Source-backed inference** means a consequence derived from more than one observed source surface.
- **Recommendation** is an integration choice for `projects/ide-extension`, not a claim about Nimbalyst's intent.
- Upstream source links below are immutable GitHub links rooted at commit `c8ca207c6004653ba2df3d81e06133ce2e9fad3d`. Symbols are named where line drift in a local viewer would otherwise make the evidence hard to locate.

## Pinned Architecture Map

### Workspace and build graph

**Observation.** The root is an npm-workspaces monorepo. The declared workspaces are Electron, runtime, CLI, core, collaboration protocol/adapters, iOS, Android, extension SDK, built-in extensions, and marketplace. The root `build` script builds only runtime; desktop release builds are owned by `packages/electron` and separately build bundled extensions and Electron artifacts. See [`package.json`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/package.json) (`workspaces`, `scripts.build`) and [`packages/electron/package.json`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/package.json) (`scripts.build`, `build:extensions`, `build:dist`).

```text
packages/extension-sdk  public TS contract, validators, hooks, Vite helpers
          ^                     ^
          |                     |
packages/extensions/*      packages/runtime (private, UI/AI/storage/sync)
          \                     /
           \                   /
            packages/electron (main + preload + renderer + packaging)
                       |
          local files, PGlite/SQLite, native process/PTY, agent SDKs

packages/collab-protocol <-> packages/runtime sync clients
                       <-> separate sync.nimbalyst.com server (not in repo)
```

**Observation.** `@nimbalyst/electron` directly depends on `@nimbalyst/runtime`, built-in extension packages, collab adapters, Electron 41, Monaco, Lexical-related runtime exports, native `better-sqlite3`/`node-pty`, MCP, Codex and Anthropic SDKs, git, WebSocket, PostHog, and updater/packager libraries. `@nimbalyst/runtime` itself depends on the extension SDK, collab packages, Lexical, Monaco, Yjs, three agent/provider SDK families, PostHog, and Vite. See the pinned [Electron manifest](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/package.json) and [runtime manifest](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/package.json).

**Observation.** A read-only source census found 503 Electron source files importing `@nimbalyst/runtime`, 19 importing the extension SDK, 11 runtime files importing the SDK, 72 built-in-extension files importing the SDK, 375 `ipcRenderer.invoke` calls in the preload bridge, and 684 test/spec files across the requested package boundary. These are source-query counts at the pinned commit, not stable project metrics.

**Source-backed inference.** The package names suggest layers, but the dependency graph does not make the desktop shell or runtime independently extractable. `runtime` is a private product package with broad UI, AI, storage, sync, and Electron-adjacent exports; Electron is an integration composition root rather than thin chrome.

### Extension host seam

**Observation.** `ExtensionManifest` provides identity, version, `main`, styles, API version, permissions, contribution declarations, release channel, default enablement, and marketplace metadata. See [`ExtensionManifest`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/types/extension.ts#L174-L224).

**Observation.** `EditorHost` is the primary custom-editor boundary. It owns file identity, theme/read-only/embed state, content load/save, file-change subscriptions, dirty state, save requests, history, optional diff/source mode, namespaced storage, editor-to-chat context, imperative editor API registration, optional collaboration, and menu items. See [`EditorHost`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/types/editor.ts#L283-L603), especially `loadContent`, `saveContent`, `setEditorContext`, `registerEditorAPI`, and `collaboration`.

**Observation.** `useEditorLifecycle` centralizes load/save, echo detection, file watching, diff mode, theme, parsing, and serialization for custom editors. `createReadOnlyHost` supplies a small Electron-free `EditorHost` used by web sharing and isolated tests. See [`useEditorLifecycle.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/useEditorLifecycle.ts) and [`createReadOnlyHost`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/createReadOnlyHost.ts#L49-L120).

**Observation.** The SDK package has no runtime dependencies, but peer-depends on React/Vite/Tailwind/Yjs surfaces. Its public check builds the SDK, dry-runs `npm pack`, typechecks the extension dev kit, and builds/typechecks three examples. See [`packages/extension-sdk/package.json`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/package.json) and [`scripts/extension-sdk-public-checks.sh`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/scripts/extension-sdk-public-checks.sh).

**Source-backed inference.** This is the best extraction seam because it is typed, separately packaged, dependency-light, has public-package checks, and already supports an Electron-free read-only host. It is not authority-safe as-is: `saveContent`, editor API registration, AI tools, storage secrets, and native backend contributions must be narrowed or routed through local envelopes.

### Privileged extensions and permission cost

**Observation.** Nimbalyst's permission contract explicitly says backend modules can use ambient Node `fs`, `net`, and `child_process`; broker permissions do not sandbox those powers. Granting a backend module is consent to native code with user-account authority. Built-ins are auto-granted. See [`types/permissions.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/types/permissions.ts#L1-L32) and [`BackendModuleContribution`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/types/permissions.ts#L87-L132).

**Observation.** Backend modules run in Electron utility processes or worker threads; lifecycle and validation are implemented by Electron main-process code. See [`backendModuleLifecycle.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/extensions/backendModuleLifecycle.ts), [`extensionBackendBootstrap.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/extensions/extensionBackendBootstrap.ts), and [`manifestValidation.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/manifestValidation.ts).

**Recommendation.** Do not copy the backend-module trust model into `ide-extension`. Reuse its honest permission wording and validation structure as precedent, while retaining the local adapter descriptor, closed grant vocabulary, actor/session separation, exact approval consumption, and kernel-only receipt authority.

### Browser implementation

**Observation.** The built-in browser extension declares HTML and virtual editors plus AI tools for navigation, page inspection, click/type/scroll/evaluate, and screenshots. Its client calls an untyped `window.electronAPI.invoke`; the actual browser is a main-process `WebContentsView` managed by `BrowserSessionService`, with IPC handlers and a custom local-preview protocol. See [`packages/extensions/browser/manifest.json`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extensions/browser/manifest.json), [`browserClient.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extensions/browser/src/browserClient.ts), [`BrowserSessionService`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/services/BrowserSessionService.ts), and [`BrowserSessionHandlers`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/ipc/BrowserSessionHandlers.ts).

**Source-backed inference.** The extension UI and tool naming are reusable product/API precedent, but the implementation is not a VS Code/VSCodium browser SDK and cannot be transplanted without owning Electron main-process browser lifecycle. This agrees with the local finding that stable VS Code APIs offer owned webviews and URL handoff, while real browser acts require an external Playwright plane ([local findings](../../vscode-browser-control-api-research/findings.md#short-answer)).

**Recommendation.** Adapt the browser tool contract into the planned `McpChatWitnessAdapter`/Playwright lane. Do not extract `BrowserSessionService`, the Electron IPC client, or `nim-preview` protocol into the IDE extension baseline.

### Storage and IPC

**Observation.** Desktop persistence is not only filesystem-first content. Internal state includes PGlite and a migrating `better-sqlite3` implementation, worker-thread database execution, repositories, backup/recovery, database locking, Electron Store fallback/config, history, sessions, worktrees, and a very broad preload bridge. See [`database/initialize.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/database/initialize.ts), [`SQLiteDatabase.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/database/sqlite/SQLiteDatabase.ts), and [`preload/index.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/preload/index.ts). Official docs accurately emphasize that user documents/workflows remain standard local files, but that statement should not be expanded into “the client has no internal database” ([Open Data, Workflow, File Storage](https://docs.nimbalyst.com/open-private-secure)).

**Source-backed inference.** Repository classes may contain good local implementation ideas, but importing them would also import schema, migration, worker, backup, and Electron IPC assumptions. The local kernel already owns durable envelopes/artifacts/events and currently has known consistency defects; adding Nimbalyst storage would multiply stores before those defects are repaired.

**Recommendation.** Use storage code only as recovery/migration precedent. Do not reuse repositories or database workers in L0/L0.5. First close AR-CAND-002 and AR-CAND-005 through AR-CAND-008 in the accepted local review ([findings](../../architecture-review-2026-07-10/findings.md#severity-ordered-change-requests)).

### Collaboration, cloud, hosted, and mobile boundary

**Observation.** This repository is MIT licensed, subject to preserving its copyright and permission notice. `LICENSING.md` says the Cloudflare Worker behind `wss://sync.nimbalyst.com` is a separate project. See [`LICENSE`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/LICENSE) and [`LICENSING.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/LICENSING.md).

**Observation.** `@nimbalyst/collab-protocol` is private and source-exported; it defines wire messages for desktop/mobile clients and the server, including team documents, trackers, rooms, personal sync, history, and inbox. Document messages carry encrypted Yjs updates/state, while runtime clients connect by WebSocket and use JWTs. See [`collab-protocol/src/index.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/collab-protocol/src/index.ts), [`teamDocument.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/collab-protocol/src/teamDocument.ts), and [`CollabV3Sync.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/sync/CollabV3Sync.ts).

**Source-backed inference.** The open client includes protocol and encryption/client logic, but not the separately operated server needed for a complete collaboration deployment. The docs' mobile/sync workflows describe a hosted product surface, not an MIT server deliverable. Therefore “MIT client code” must not be represented as “self-hostable Nimbalyst collaboration.”

**Recommendation.** Keep collaboration and mobile out of the first integration. If later needed, treat `CollabCodec`/`createTextCollabContentAdapter` as document-codec precedent and design a locally owned transport/server contract. Never make `sync.nimbalyst.com`, hosted sharing, mobile approval, or server-minted state part of kernel authority by implication.

## Candidate Reuse Units

| Unit | Exact source | Dependencies/coupling | Extraction cost | Maintenance risk | Disposition |
| --- | --- | --- | --- | --- | --- |
| Minimal editor-host port | `types/editor.ts`: `EditorContext`, `DiffConfig`, selected `EditorHost` methods | TypeScript only after pruning; local file/envelope adapters | Low-medium | Low if locally frozen/versioned | **ADAPT behind local `WorkbenchEditorHost`** |
| Manifest contribution and validation pattern | `types/extension.ts`, `manifestValidation.ts`, `validate.ts` | TypeScript; current full validator knows Nimbalyst-specific contributions | Medium | Medium as upstream schema expands | **ADAPT fields/fixtures, do not copy whole manifest** |
| `createReadOnlyHost` | `createReadOnlyHost.ts` | TypeScript; `EditorHost` type | Low | Low | **ADOPT/port for specimen and isolated editor tests** |
| Lifecycle state machine | `useEditorLifecycle.ts` | React hooks plus `EditorHost`; diff/file echo semantics | Medium | Medium | **ADAPT only after local host contract exists** |
| Text collaboration codec | `collab/createTextCollabContentAdapter.ts`, `types/collab.ts` | Yjs/Y-protocols and server-aware lifecycle | Medium | Medium-high | **DEFER; precedent first** |
| Extension public-check script shape | `extension-sdk-public-checks.sh`; SDK examples | npm/Vite/TypeScript | Low | Low | **ADAPT as contract/package smoke checks** |
| Browser tool vocabulary/UI split | browser manifest, `aiTools.ts`, `browserClient.ts` | Electron IPC and main-process service for implementation | Low for interface, high for behavior | High if forked | **PRECEDENT; map to Playwright/MCP adapter** |
| `BrowserSessionService`/preview protocol | Electron main services and IPC handlers | Electron `WebContentsView`, windows, sessions, workspace roots | High | High, security-sensitive | **KILL for VS Code/VSCodium baseline** |
| Backend module runtime | permissions types, privileged host/bootstrap/lifecycle | Electron utility process/worker, ambient Node authority | High | High | **KILL as local authority model; retain wording precedent** |
| Storage/repositories | runtime repositories, Electron DB workers/migrations | PGlite, better-sqlite3, workers, schemas, backups | Very high | High | **KILL for L0/L0.5 reuse** |
| Collaboration protocol/client | collab protocol/adapters, runtime sync | Yjs, crypto, JWT/Stytch, separate server | High without server | High, service-coupled | **DEFER/PRECEDENT only** |
| Built-in visual editors | `packages/extensions/{excalidraw,datamodellm,csv-spreadsheet,...}` | React plus substantial editor-specific libraries; some collab/runtime assumptions | Medium-high each | Medium-high | **Use as UX specimens; evaluate one at a time** |

## Local Integration Fit

**Observation.** The accepted local review keeps visibility separate from authority and requires repair of exactly-once approval, ID-addressed lifecycle, persistence consistency, evidence resolution, runtime schema enforcement, provenance, and secret custody before effectful promotion. It explicitly closes review, not implementation ([accepted findings](../../architecture-review-2026-07-10/findings.md#architecture-review-findings)).

**Observation.** The browser-first/MCP design assigns approval, durable mutation, artifacts, and receipt minting to the local Node kernel. MCP, chat, browser, and provider surfaces are adapters/witnesses only ([MCP findings](../../mcp-chat-extension-integration-research/findings.md#lane-ownership)).

**Source-backed inference.** A direct Nimbalyst extension-host adoption would blur that boundary because its host contract includes direct saves, extension storage/secrets, imperative AI/editor APIs, and native backend execution. A narrowed port can still save time by avoiding fresh design of editor lifecycle, contribution registration, theme/read-only handling, and isolated host tests.

## Recommended Extraction Sequence

1. **Repair local L0 first.** Nimbalyst code must not bypass AR-CAND-001 through AR-CAND-008 or stand in for their acceptance tests.
2. **Write a local `WorkbenchEditorHost` interface.** Start with `filePath`, `fileName`, `theme`, `readOnly`, `loadContent`, file-change/theme subscriptions, `setDirty`, and a proposal-only save method that prepares an envelope. Exclude collaboration, secrets, native modules, direct AI tool execution, and receipt creation.
3. **Port `createReadOnlyHost` and its tests.** This is the smallest concrete witness that a visual editor can render without Electron, IPC, cloud, or effect authority.
4. **Adapt manifest validation.** Add only local editor/view contributions and adapter descriptors; validate with the local Draft 2020-12 boundary rather than importing Nimbalyst's expanding manifest wholesale.
5. **Adapt lifecycle behavior.** Bring over echo detection/theme/read-only/diff ideas only after the local host's save path proves prepare -> approval -> invoke -> evidence -> receipt.
6. **Map browser tools to the existing MCP/Playwright lane.** Keep a typed `BrowserActPort`; implement it outside VS Code's public browser APIs and behind exact grants/approval.
7. **Defer collaboration and rich built-ins.** Reassess one codec/editor only when a specific local user job and acceptance test justify its dependency graph.

## Proportionate Checks Run

- Verified the shared checkout HEAD equals `c8ca207c6004653ba2df3d81e06133ce2e9fad3d`; checkout status was clean.
- Parsed root and requested package manifests with `jq`; enumerated workspaces and package dependencies.
- Queried import edges, IPC calls/handlers, named APIs, storage implementations, collaboration wire types, browser implementation, and test files with read-only `rg`/`find`/`wc` commands.
- No dependency installation, build, generated output, or upstream mutation was attempted. The checkout had no `node_modules`, so package typechecks/tests were not runnable without violating the no-install constraint.

## Final Position

The credible development-time reduction is a small, locally governed extraction: adapt the SDK's editor-host vocabulary and lifecycle patterns, port the Electron-free read-only host, and reuse its public-package verification shape. Treat the browser extension, built-in editors, storage system, and collaboration clients as pinned precedent until a bounded local witness proves a lower total cost than building against existing local owners.

Do not adopt Nimbalyst's Electron/runtime graph, native extension trust model, or hosted collaboration assumptions. The MIT license permits reuse of repository code with notice preservation, but it does not supply the separate collaboration server and does not erase dependency, security, or maintenance cost. Nimbalyst can accelerate the local presentation/extension contract; it must not become a shortcut around the local kernel's approval and receipt authority.

## ROBOT-TALKS CONFRONTATION

### 1. Product grammar versus code reuse

**REVISE.** `packages/extension-sdk` remains the strongest *bounded source seam*, but that does not establish that copying its code is cheaper than expressing the required local contract. Simon correctly leaves direct reuse undecided because the local owner, security fit, dependency envelope, and maintenance cost were not established (`simon-product-workflow.md:111-130`). The full `EditorHost` includes direct save, extension storage including secrets, editor API registration, and optional collaboration (`packages/extension-sdk/src/types/editor.ts:283-603`), while the local contract needs proposal-only mutation and kernel receipts. Copying that interface would require subtractive adaptation and compatibility tracking.

The cheapest first witness is therefore a locally named `WorkbenchEditorHost` subset derived from, but not source-compatible with, Nimbalyst. Only `createReadOnlyHost` behavior is small enough to consider a literal port: it is one factory with in-memory/no-op mutation and no Electron imports (`createReadOnlyHost.ts:25-120`). Even there, local expression is likely cheaper than preserving upstream interface compatibility. Revised disposition: **ADAPT the contract shape; port code only if a symbol-level diff proves less work than a clean local implementation.**

### 2. SDK seam versus authority coupling

**CONCEDE.** Turing and Ashby establish that “public TypeScript” is not equivalent to “authority-neutral.” `AgentProtocol.SessionOptions` carries permission mode, MCP servers, environment, and allow/deny tools, while `AgentProtocolHost` leaves permission authoritative inside provider code (`turing-agent-protocol.md:25-50`). The SDK permission types explicitly admit ambient `fs`, `net`, and `child_process` after native-module consent and auto-grant built-ins (`packages/extension-sdk/src/types/permissions.ts:1-25,87-132`).

The safe seam is narrower than the package: passive editor/view types, pure validation/data-shaping logic after pruning, and read-only host behavior. `saveContent`, secrets, `registerEditorAPI`, AI tools, backend modules, provider lifecycle, MCP registration, and collaboration are integration boundaries, not reusable authority contracts. Any local type must make kernel custody visible rather than retain Nimbalyst method names whose semantics differ.

### 3. Provider/event projection

**HOLD, with a later trigger.** Turing's raw-native-event plus pure canonical-projection pattern is structurally sound: Nimbalyst stores provider-native messages as source, rebuilds canonical events through pure parsers/projectors, and does not equate provider completion with kernel pass (`turing-agent-protocol.md:118-139`). Explicit `abortSession` and `cleanupSession`, fail-loud resume identity, and separation of termination request from observed termination improve Simon's workflow by making session status and changed-artifact views reconstructable and honest; otherwise a user-facing “completed” lane can hide parser loss, resume mismatch, or orphaned work.

Exact coupling blocks direct extraction. `AgentProtocol.ts` is light enough to read as vocabulary, but concrete providers are constructed by private `@nimbalyst/runtime`, cached by provider/session, and pull provider SDKs, storage, MCP/environment options, privileged extension modules, and process recovery (`turing-agent-protocol.md:27-46,80-95,245-256`; `packages/runtime/package.json`). Direct provider classes are therefore **KILL** for embedding. A locally expressed event vocabulary is **ADAPT NOW as schema precedent**; provider-specific parser code is **DEFER until two admitted providers create actual duplication**. Process custody still requires bounded CWD/environment, no ambient HOME, timeout, process-tree cancellation, orphan cleanup, and negative egress tests (`ashby-safety-operations.md:83-93`).

### 4. Diff approval

**REVISE.** Simon's visual review primitive survives only as presentation. Ashby's distinction is decisive: Nimbalyst Keep/Undo reviews an already-produced filesystem change; it is not pre-effect authorization (`ashby-safety-operations.md:23-25`). Local evidence also says the current kernel does not materialize/resolve after-state evidence (`architecture-review-2026-07-10/findings.md:88-107`).

Disposition: **DEFER presentation until validated before/after artifacts exist.** Then adapt red/green/per-change projection as a read-only disposition view. The UI must label pre-effect approval and post-effect accept/reject as different acts, bind both to exact digests, and never treat a click as attested identity or a provider “complete” event as receipt status. Kill any candidate that writes the working tree directly or mints/changes receipts.

### 5. Tasks, workstreams, and session links

**REVISE.** Nimbalyst contributes a distinct *navigation projection*, not a distinct state model. Its useful product hypothesis is bidirectional reachability among task, session, changed artifact, and evidence (`simon-product-workflow.md:54-57,82-89,111-118`). Craft/Arcanum already owns task/status/routing; importing trackers, kanban state, workstream lifecycle, or launch semantics would create a second canonical ledger.

The surviving unit is a read-only relation record containing owner-qualified references and derived labels. It may show `task_ref -> run_id -> provider_session_ref -> artifact/evidence refs -> receipt_id`; all status is resolved from canonical local owners and may be stale/unknown rather than locally overwritten. Disposition: **ADAPT a projection only after L0 lifecycle consistency is repaired; KILL duplicated task/session authority.**

### 6. Permission, MCP, and session execution

**CONCEDE the kills; HOLD three pure residues.** Direct reuse of `ToolPermissionService`, permission modes/pattern caches, shell-environment MCP merging, terminal/Git/worktree execution, credential/sync/mobile, PostHog, updater, and internal SSE topology would import ambient authority or operations obligations (`ashby-safety-operations.md:19-34,63-81`). Concrete provider/session implementations also pull private runtime storage and provider-specific recovery (`turing-agent-protocol.md:245-256`).

Three independently reusable residues remain:

1. **Pure lifecycle/event vocabulary:** locally express create/resume/send/interrupt/cleanup and raw/text/tool/result/error/complete/usage kinds; provider permission never becomes kernel policy.
2. **Pure parser/projector ideas:** preserve unknown raw events and deterministically derive a UI view from fixtures; defer code porting until two providers justify it.
3. **Pure descriptors and failure semantics:** parse an explicitly admitted redacted MCP descriptor, and treat worktree partial success as `flagged` precedent. Do not read/migrate home config or execute Git.

These residues are **ADAPT/PRECEDENT**, subject to zero Electron, storage, analytics, credential, network, and process imports. Everything else named above remains **KILL** or **DEFER**.

### 7. Development-time accounting

**REVISE.** My initial report underweighted abandonment and policy-duplication costs. Use six cost columns for every candidate: extraction, authority adaptation, tests, provenance/license, upgrades, and abandonment. Qualitative totals below assume the current single fake/offline witness and no installed upstream dependency.

| ID | Candidate | Extract | Adapt | Test | Provenance | Upgrade | Abandon | Net reduction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `NIM-H01` | Local editor-host subset | Low | Medium | Medium | Low | Low if locally owned | Low | **Positive**, after L0 repair |
| `NIM-H02` | Read-only host behavior | Low | Low | Low | Low | Low | Low | **Positive now as isolated witness** |
| `NIM-H03` | Full SDK/manifest compatibility | Medium | High | High | Medium | High | Medium | **Negative**; second contract authority |
| `NIM-P01` | Local lifecycle/event vocabulary | Low | Medium | Medium | Low | Low | Low | **Positive** as schema precedent |
| `NIM-P02` | Provider raw-event projectors | Medium | Medium | High fixture cost | Medium | High per SDK drift | Medium | **Positive only at second provider** |
| `NIM-D01` | Evidence/diff projection | Low-medium | Medium | High evidence/UI tests | Low | Low | Low | **Positive only after before/after proof** |
| `NIM-R01` | Task-session-artifact relation view | Low | Medium owner resolution | Medium | Low | Medium owner drift | Low | **Small positive** if read-only |
| `NIM-B01` | Browser tool vocabulary | Low | Medium | High hostile browser tests | Low | Medium | Low | **Positive as Playwright adapter precedent** |
| `NIM-X01` | Provider/runtime/permission/MCP execution | High | Very high | Very high | High | Very high | High | **Negative** |
| `NIM-C01` | Collaboration/mobile/sync | High | Very high | Very high | Server unknown | Very high | Very high | **Negative** |

No candidate counts as a reducer if it creates a second policy, task, session, approval, or receipt authority. A positive initial-code delta is insufficient; the candidate must remain positive after hostile tests, provenance, one upstream upgrade rehearsal, and a documented delete/replace path.

## REVISED FINAL POSITION

Shared-ready candidate list:

| ID / name | Revised recommendation | Boundary |
| --- | --- | --- |
| `NIM-H01` `WorkbenchEditorHost` subset | **ADAPT** | Locally express passive editor/view contract; proposal-only mutation; no upstream compatibility promise. |
| `NIM-H02` read-only host | **ADAPT** | Reimplement or port the tiny behavior with symbol-level provenance and isolated tests. |
| `NIM-H03` full extension SDK/validators | **KILL** | Full compatibility imports Nimbalyst contribution and authority semantics; use selected validation patterns only. |
| `NIM-P01` lifecycle/event vocabulary | **ADAPT** | Local schema behind envelopes; explicit interrupt/cleanup; raw events are evidence. |
| `NIM-P02` provider raw-to-canonical projectors | **DEFER** | Port pure parser code only when a second provider proves duplication and fixtures cover drift. |
| `NIM-D01` red/green evidence view | **DEFER**, then **ADAPT presentation only** | Requires materialized, validated before/after evidence; never substitutes for pre-effect approval. |
| `NIM-R01` task-session-artifact relation projection | **ADAPT after L0 repair** | Read-only owner-qualified links; Craft/Arcanum and kernel remain canonical. |
| `NIM-B01` browser tools/UI split | **PRECEDENT** | Implement through the local Playwright/MCP adapter, not Electron `WebContentsView` code. |
| `NIM-M01` redacted MCP descriptor parser | **PRECEDENT/ADAPT narrowly** | Explicit per-run config only; no HOME migration, shell-env merge, credentials, or network in the witness. |
| `NIM-W01` worktree partial-success semantics | **PRECEDENT** | Context/evidence refs only; no Git/worktree executor reuse. |
| `NIM-X01` provider classes, permission service, backend modules, terminal/Git execution | **KILL** | Creates ambient process authority and a second policy/session control plane. |
| `NIM-C01` collaboration server/client, sync, hosted sharing, mobile approval | **KILL for current layer** | Separate server and identity/key/remote-approval obligations; client MIT license is insufficient. |
| `NIM-O01` telemetry/updater | **KILL** | Adds egress and executable supply-chain duties unrelated to the local witness. |

The revised common position is narrower than my initial return: Nimbalyst reduces development time through pinned vocabulary, tiny passive host behavior, pure projection patterns, and product precedent. It does not justify importing an SDK compatibility surface or any execution substrate. Local contracts should cite the exact upstream inspiration while remaining deliberately non-compatible where Nimbalyst semantics conflict with kernel-owned approval, evidence, task ownership, session state, and receipts.
