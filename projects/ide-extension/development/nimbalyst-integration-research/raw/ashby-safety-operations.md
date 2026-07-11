# Ashby Safety and Operations Return

**Identity:** W. Ross Ashby, adversarial safety-and-operations explorer
**Inspected upstream:** `Nimbalyst/nimbalyst` at `c8ca207c6004653ba2df3d81e06133ce2e9fad3d`
**Evidence classes:** **Observation** reports a source fact. **Inference** derives a bounded consequence. **Recommendation** states a local adoption condition.

## INITIAL POSITION

Do not adopt Nimbalyst as the `ide-extension` execution, permission, credential, update, or sync substrate. Use it as product precedent and, at most, adapt small MIT-licensed client-side units behind the local adapter boundary after an offline hostile witness passes. The decisive issue is not whether Nimbalyst has safety controls; it does. The issue is that its controls govern a large Electron application with coding-agent SDKs, terminals, Git/worktrees, persistent approvals, internal and user MCP servers, optional analytics, auto-update, and cross-device approval. That authority set is much wider than the accepted local model: HTML outside, a small kernel inside, and one approval/evidence/receipt boundary for every effectful crossing ([local architecture](../../../ARCHITECTURE.md#one-sentence)).

Nimbalyst's visual Keep/Undo diff is review of an already-produced filesystem change, not proof that the local kernel authorized the effect before execution. Nimbalyst's tool permission flow is real enforcement for supported provider paths, but it includes modes and caches that deliberately remove prompts. Therefore no Nimbalyst approval UI, trust mode, or permission service may substitute for kernel-owned exact-once approval and kernel-minted receipts.

## Boundary And Licensing

- **Observation:** The inspected repository is MIT-licensed, with notice retention required and no warranty ([LICENSE](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/LICENSE)). The repository describes its Electron, runtime, iOS, protocol, SDK, and extension packages as client code, while `wss://sync.nimbalyst.com` and its collaboration server are a separate project ([README `Major workspaces`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/README.md#building-from-source), [README `License`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/README.md#license)).
- **Inference:** MIT permission over this checkout does not establish source availability, deployability, licensing, retention, incident response, or compatibility guarantees for the separate collaboration server or hosted/mobile distribution surfaces.
- **Recommendation:** Any reuse record must name the exact copied symbols and commit, preserve the MIT notice, and classify cloud/mobile behavior as external-service precedent unless separately evidenced and contracted.

## Claimed-Versus-Enforced Control Map

| Surface | Claim | Enforced at pinned source | Residual authority / local disposition |
|---|---|---|---|
| Workspace trust | Projects must be trusted before agents act; Ask, Allow All, and Bypass All are available ([official permissions](https://docs.nimbalyst.com/open-safe-private-secure/permissions-and-safety)). | `PermissionEvaluator.shouldPromptUser` suppresses prompting for `bypass-all` and approved patterns; Allow All classifies Read/Write/Edit and related file tools for automatic approval ([source](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/permissions/PermissionEvaluator.ts#L97-L147)). | A mode switch or persisted pattern expands ambient authority. **KILL** as kernel policy; precedent only.
| Per-action approval | Ask mode offers deny, once, session, and permanent approval ([official permissions](https://docs.nimbalyst.com/open-safe-private-secure/permissions-and-safety#how-approval-works-in-ask-mode)). | `ToolPermissionService` blocks on a pending promise, accepts desktop IPC or polled cross-device response, persists `always` patterns, and caches session-or-higher patterns ([source](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/permissions/ToolPermissionService.ts#L181-L225)). | Enforcement exists, but approval is reusable and may arrive through remote state. No kernel receipt/evidence binding is shown here. **Do not adapt** without exact proposal digest, actor/session attestation, expiry, and replay rejection.
| Visual diff approval | AI edits appear as red/green diffs with Keep/Undo ([official docs](https://docs.nimbalyst.com/markdown-editor-%2B-ai/ai-editing-red-green-diff-approval)). | The docs also state Agent mode gives the agent full power and tool calls include file operations and execution. The quickstart says an agent can manipulate files outside the project with permission ([quickstart](https://docs.nimbalyst.com/getting-started/quickstart)). | Post-effect review is not pre-effect authorization. **Precedent only** for presentation.
| Internal MCP | Internal tools are integrated and user MCP connections run locally ([official MCP docs](https://docs.nimbalyst.com/setup-nimbalyst/mcp)). | Several internal MCP and team-coordination tools are always allowed by name; internal SSE config includes week-long blocking timeouts and host/settings/session orchestration ([evaluator](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/permissions/PermissionEvaluator.ts#L150-L201), [`McpConfigService`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/runtime/src/ai/server/services/McpConfigService.ts#L130-L202)). | Tool-name trust and internal-server privilege are broader than a descriptor-bound, one-tool offline witness. **KILL** direct reuse; retain protocol/config parsing only as specimen.
| MCP credentials | API keys/tokens are said to be stored securely locally and not sent to Nimbalyst servers ([official MCP docs](https://docs.nimbalyst.com/setup-nimbalyst/mcp#privacy-security)). | MCP config merges user/workspace configuration and shell environment for providers (`McpConfigService.getMcpServersConfig`). This is local custody, but potentially broad inherited-secret custody. | Require redacted HOME, fixture CWD, explicit env allowlist, no shell-env merge, and negative exfiltration tests. Otherwise **KILL**.
| Filesystem | Sensitive paths are claimed always blocked; compound commands receive nonpersistent patterns ([official permissions](https://docs.nimbalyst.com/open-safe-private-secure/permissions-and-safety#security-notes)). | `SafePathValidator` supplies a separate path-defense layer; agent providers and embedded terminals still operate with host process authority. No OS sandbox boundary was found in inspected evidence. | Path filtering is not process isolation and cannot constrain arbitrary binaries after spawn. **KILL** as sufficient containment.
| Terminal / Git / worktrees | Product includes terminal, Git operations, commits, worktrees, rebases, and auto-stashing ([README](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/README.md#features), [worktree docs](https://docs.nimbalyst.com/code-and-coding-with-nimbalyst/worktrees)). | Electron main-process handlers and `TerminalSessionManager` create and control host terminal sessions; worktrees isolate file state, not credentials, network, parent processes, or shared Git objects. | High-impact ambient authority. Never expose through an `ide-extension` UI adapter; require a separately governed process runner if later needed.
| Credentials / sync keys | Sync is described as end-to-end encrypted and local-first. | `CredentialService` uses Electron `safeStorage`, but falls back to plaintext JSON when unavailable; QR pairing contains the encryption seed, server URL, analytics ID, and identity metadata ([source](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/services/CredentialService.ts#L72-L112), [pairing payload](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/electron/src/main/services/CredentialService.ts#L207-L230)). | Plaintext fallback is fail-open secret custody. Pairing expands the trust boundary to camera/display/mobile and account identity. **KILL** sync/credential reuse.
| Mobile / cloud approvals | Mobile can answer permission prompts and approve diffs; desktop changes sync immediately ([quickstart](https://docs.nimbalyst.com/getting-started/quickstart#mobile-app)). | Permission responses are polled from stored agent messages; client crypto/protocol exists, but the server is separate. The repository's own mobile security review records open JWT-validation and service risks ([review](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/design/MobileSync/SECURITY_REVIEW.md)). | Remote approval introduces identity, freshness, ordering, replay, availability, and service-custody obligations. **KILL** for current local boundary.
| Telemetry | Anonymous PostHog analytics are optional; file content, paths, tokens, and chat content are claimed excluded ([README telemetry](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/README.md#telemetry)). | Renderer initializes PostHog conditionally and the main analytics service holds install/session identity. The event catalogue includes agent, terminal, permission, MCP, worktree, and mobile actions. | Metadata still reveals operational behavior. Any adapted unit must have no analytics dependency and pass a zero-egress test. Product use requires an event/property audit, not the summary claim alone.
| Auto-update | Stable installs check automatically and can opt into alpha; users are notified ([README auto-updates](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/README.md#auto-updates)). | Electron updater code checks remote release metadata and downloads/installs through the application update path. | Adds release-channel, signing, rollback, supply-chain, and compatibility duties. **KILL** updater reuse; pin dependencies and update deliberately.
| Renderer isolation / extensions | Extensions declare permissions and use a common host contract. | Main windows set `nodeIntegration: false` and `contextIsolation: true`; extension grants are separately stored. The repository security review still treats extension backends and APIs as privileged attack surfaces. | Useful defense in depth, not a sandbox for spawned agents or terminals. Extension permission UI may inspire grammar only.

## Threat And Authority Map

| Principal | Authority held | Asset exposed | Failure mode |
|---|---|---|---|
| Renderer / extension UI | IPC calls and user attention | approval intent, workspace state | confused-deputy prompt, malicious extension, approval fatigue |
| Electron main process | filesystem, credentials, IPC, updater, terminal lifecycle | repository, user profile, tokens, executable supply chain | one process compromise crosses multiple control planes |
| Coding-agent provider / CLI | tools, shell, inherited environment, external network according to provider config | files beyond project, Git state, credentials | prompt injection or overbroad persisted pattern produces host effects |
| Internal or configured MCP server | named tool authority, credentials, local/network service access | third-party accounts and local data | tool-name allowlisting masks changed implementation or excessive input scope |
| Sync/mobile client | remote response and document/session state | approval decisions, encrypted content, identity keys | stale/replayed/misattributed response or device compromise |
| Separate collaboration service | routing, authentication, availability, ciphertext/metadata custody | account and collaboration metadata | unreviewable server drift, outage, retention, protocol incompatibility |
| PostHog / release infrastructure | behavioral metadata / executable update channel | operational privacy / installed binary | analytics-policy drift or supply-chain compromise |

Worktrees reduce accidental file collision; they do not reduce the variety required of the controller because Git objects, credentials, processes, network, updates, and remote approval remain shared or adjacent. In Ashby terms, the product adds operational variety faster than the local kernel can currently absorb.

## Operational Overhead Ledger

| Obligation introduced | Recurring cost | Adoption consequence |
|---|---|---|
| Track fast-moving monorepo symbols and provider SDK behavior | pin, diff, retest each upgrade | Bounded copies fork quickly; prefer tiny stable interfaces over service extraction. |
| Electron security and signing | Chromium/Electron CVEs, packaging, codesigning, updater validation | Incompatible with the current browser-first local-server economy unless Electron itself is an explicit product decision. |
| Permission parity across Claude, Codex, CLI hooks, MCP, terminal, mobile | cross-provider negative tests and semantic drift review | A borrowed permission service creates a second policy authority beside the kernel. |
| Credential and MCP lifecycle | OS-keychain variance, rotation, revocation, redaction, OAuth callback review | No credential-bearing reuse before a dedicated custody design. |
| Sync/mobile/cloud | server SLA, auth, E2EE key recovery, protocol migration, deletion/retention, incident response | Separate program, not an IDE feature shortcut. |
| Telemetry and update governance | event-schema audit, consent defaults, egress tests, release rollback | Remove from any adapted component; do not inherit silently. |
| Git/worktree automation | dirty-tree, auto-stash, conflict, submodule, recovery tests | Local submodule discipline and receipts must remain authoritative. |
| License/provenance | exact commit/symbol ledger and MIT notices | Cheap for isolated code; expensive when copying coupled services. |

## Adoption Dispositions

1. **ADAPT behind an adapter, conditionally:** pure UI rendering or data-shaping helpers only when dependency-free enough to isolate, with exact-symbol provenance, no Electron/analytics/storage import, and local tests.
2. **PRECEDENT:** red/green diff presentation, permission-mode vocabulary, session/worktree status views, extension permission grammar, MCP status diagnostics.
3. **DEFER:** any provider-session adapter until the local exact-once approval, concurrency, schema enforcement, evidence binding, and secret-custody L0 findings are repaired. The accepted review explicitly blocks promotion on those defects ([local findings](../../architecture-review-2026-07-10/findings.md#severity-ordered-change-requests)).
4. **KILL:** Nimbalyst permission service as kernel policy; embedded terminal or Git/worktree executor; shell-environment MCP merge; credential/sync/mobile stack; PostHog integration; auto-updater; direct internal SSE MCP topology.

## Kill Conditions

Stop a candidate immediately if any is true:

- It can mutate, spawn, use network, access Git, read credentials, or persist approval without a kernel-issued exact proposal authorization.
- Approval is reusable by default, pattern-based without argument binding, remotely accepted without attested actor/session/freshness, or not consumed exactly once.
- It mints or edits receipts, or reports UI acceptance as evidence of executed effect.
- It inherits ambient `HOME`, shell environment, broad CWD, login shell, host keychain, or user MCP configuration.
- It depends on the separate collaboration server, hosted service, mobile distribution, telemetry, or update channel to satisfy the local witness.
- It has plaintext credential fallback, unbounded logs/transcripts, or cannot prove zero secret/event egress.
- Its claimed time saving excludes upgrade, security, provenance, and negative-test maintenance.
- It bypasses any accepted L0 repair or the existing offline MCP witness rule ([local MCP findings](../../mcp-chat-extension-integration-research/findings.md#acceptance-tests)).

## Evidence Required Before Adoption

1. Exact upstream commit, path, symbol, license notice, dependency closure, and adopting owner.
2. A smallest local offline witness with fake credentials, fake HOME, fixture CWD, no network, and one non-mutating allowlisted operation.
3. Negative tests for pre-approval invocation, wrong/expired/replayed approval, changed arguments after approval, non-allowlisted tool, path escape, symlink escape, env leakage, shell chaining, child-process escape, and receipt forgery.
4. Kernel evidence binding for envelope, approval, actor/session, adapter digest, tool/input digest, environment descriptor, before/after artifacts, transcript digest, and kernel-minted receipt.
5. Process-tree cancellation, timeout, crash recovery, orphan cleanup, and concurrent-run tests.
6. A zero-egress capture proving no PostHog, updater, sync, OAuth, MCP, or provider endpoint is contacted by the adapted unit.
7. Secret-custody proof with fail-closed behavior when secure storage is unavailable; rotation, revocation, redaction, and deletion tests.
8. An upgrade budget: pinned dependencies, upstream-diff trigger, compatibility owner, rollback, and abandonment path.
9. For any cloud/mobile proposal, separate evidence for server source/license, authentication, E2EE threat model, metadata retention/deletion, audit logs, replay protection, device revocation, SLA, and incident response.

## Final Return

Nimbalyst demonstrates a mature, broad workbench and contains genuine control mechanisms. That is precisely why whole-layer reuse is unsafe here: the controls are inseparable from a much larger authority and operations envelope. The development-time-saving move is to borrow product grammar and perhaps a few pure MIT client helpers, not to import its execution substrate. Until the local kernel can prove its own approval, grants, concurrency, schema, evidence, and secret-custody invariants, adding Nimbalyst's provider, MCP, terminal, sync, telemetry, or updater machinery would increase uncontrolled variety rather than reduce implementation risk.

## ROBOT-TALKS CONFRONTATION

### 1. Product grammar versus code reuse

**REVISE** My initial allowance for “a few pure MIT client helpers” was too loose. Simon establishes useful product hypotheses but explicitly makes no SDK reuse decision because contract fit, dependencies, security, maintenance, and ownership were not proved (`simon-product-workflow.md:111-120`). Hewitt establishes that `@nimbalyst/extension-sdk` has no runtime dependencies and has package checks, but its `EditorHost` spans load/save, storage, AI/editor APIs, collaboration, history, and context (`hewitt-source-architecture.md:48-58`). That makes it a strong *specimen*, not yet a cheaper copy.

For the first local host, expressing the narrow contract locally is cheaper than copying and pruning the 300-line-plus Nimbalyst host surface: `filePath`, `theme`, `readOnly`, content load, subscriptions, dirty state, and a proposal-only save method. Hewitt independently recommends writing that local `WorkbenchEditorHost` before porting `createReadOnlyHost` (`hewitt-source-architecture.md:119-125`). Copy code only if a line/import/dependency delta and a two-upgrade replay show lower total cost than the local expression.

**Cost account:** local expression has low extraction, low adaptation, medium contract tests, no upstream provenance beyond design citation, low upgrade cost, and low abandonment cost. Copy/prune has low-medium extraction, medium adaptation, medium tests, mandatory MIT provenance, continuing upstream-diff review, and medium abandonment cost because local names and semantics diverge.

### 2. SDK seam versus authority coupling

**HOLD** against direct SDK adoption; **CONCEDE** a bounded read-only test specimen. Hewitt's own evidence states that `EditorHost` includes direct save, namespaced storage, AI/editor API registration, secrets-capable surfaces, and optional collaboration (`hewitt-source-architecture.md:50-58`, `111-117`). More decisively, Nimbalyst's permission contract admits that backend modules may use ambient Node `fs`, `net`, and `child_process`, are not sandboxed by broker permissions, and built-ins are auto-granted (`hewitt-source-architecture.md:60-66`). Turing shows the analogous provider seam leaves permission requests provider-private and makes `permissionMode` advisory (`turing-agent-protocol.md:27-50`).

`createReadOnlyHost` is independently testable and Electron-free, but it is typed against the broad `EditorHost`. Therefore: **ADAPT**, not adopt. Reimplement its minimal behavior against the local narrow interface; use upstream fixtures/behavior as precedent. Do not import `types/permissions.ts`, backend contribution types, `saveContent`, secrets, imperative AI tools, collaboration, or receipt-like state.

**Cost account:** behavior re-expression is low extraction/adaptation, medium negative tests, citation-only provenance, low upgrade and abandonment. A literal port is low extraction but medium pruning/test/provenance, medium upgrade review, and medium abandonment because the source type graph remains a pressure toward Nimbalyst lifecycle semantics.

### 3. Provider/event projection

**CONCEDE** the architecture; **REVISE** timing from “adapt now” to “define now, implement with the first admitted provider witness.” Turing's exact source trace shows a provider-neutral lifecycle with create/resume/fork/send/abort/cleanup and normalized event kinds, while provider permission remains private (`turing-agent-protocol.md:25-50`). Nimbalyst preserves provider-native payloads and derives canonical events through parsers/projectors rather than making canonical projections the source of truth (`turing-agent-protocol.md:118-139`). Explicit abort, cleanup, fail-loud resume identity, and raw-event preservation improve the user workflow by distinguishing “stop requested,” “process observed stopped,” “resume token rejected,” and “projection complete” instead of presenting a false generic success. This supports Simon's jobs of resuming work, inspecting what changed, and returning to rationale (`simon-product-workflow.md:61-76`).

The coupling limit is equally exact: direct provider classes pull runtime storage, provider-private permissions, environment/MCP custody, and process recovery (`turing-agent-protocol.md:245-256`); Hewitt maps `runtime` and Electron as broad product graphs rather than extractable libraries (`hewitt-source-architecture.md:45-46`). Custody remains kernel-bounded: redacted raw events are evidence; provider IDs are opaque tokens; a new process crossing needs approval; abort must verify process-tree termination; cleanup cannot rewrite outcome; provider `complete` cannot mint `passed`.

**Cost account:** local vocabulary has low extraction, medium adaptation, high fixture/crash/timeout tests, citation-only provenance, low-medium provider-schema upgrades, and low abandonment. Porting parsers before two providers has medium extraction/adaptation, high fixtures, MIT provenance, high schema-upgrade tracking, and medium abandonment. Hence pure parser reuse is **DEFER** until two providers create demonstrated duplication.

### 4. Diff approval

**HOLD** The candidate is **presentation-only and gated on materialized after-state evidence**. Simon calls the useful unit a before/after review projection and independently says `ide-extension` must repair evidence-reference integrity before history or review can be reliable (`simon-product-workflow.md:46-53`, `80-88`, `111-116`). My source trace shows Nimbalyst Keep/Undo occurs in a product where Agent mode can already operate on files and execute tools; it is not evidence of pre-effect kernel authorization.

Do not kill the viewer. Kill the names and semantics `approve`, `accept`, or `authorized` for post-effect review. Render kernel-resolved before/after artifacts, their hashes, provenance, and an explicit disposition such as `retain`/`revert proposal`; never let the viewer attest actor identity, authorize an effect, or mint a receipt. No implementation before AR-CAND-001, AR-CAND-002, AR-CAND-006, AR-CAND-007, and AR-CAND-008 are repaired.

**Cost account:** precedent-only interaction design has zero extraction, low adaptation, medium honest-state tests, citation provenance, low upgrade, low abandonment. Copying editor diff code has medium-high extraction/adaptation, high editor-specific tests, MIT provenance, medium-high dependency upgrades, and high abandonment. **PRECEDENT**, then locally build the smallest evidence viewer.

### 5. Tasks, workstreams, and session links

**REVISE** from broad “session/worktree status view precedent” to one distinct projection only: a read-only relation index over existing canonical IDs.

Simon observes a useful navigation relation `task -> session -> changed artifact -> evidence`, but also states that copying Nimbalyst's tracker risks a second canonical ledger and that local surface cards may route but never promote or execute (`simon-product-workflow.md:54-57`, `80-88`, `111-120`). Turing likewise requires provider team/session state to remain evidence and models every invocation as a new envelope (`turing-agent-protocol.md:143-167`). The distinct addition is not status, planning, routing, workstreams, or kanban; Craft/Arcanum already own those. It is a disposable query/view joining canonical `task_ref`, `envelope_id`, `run_id`, `provider_session_ref`, `artifact_ref`, and `receipt_id`, with no write path and no locally invented status.

**Cost account:** local projection has no extraction, low adaptation, medium broken-reference/unknown-ID tests, no copied-code provenance, low schema-version upgrade, and trivial abandonment. Nimbalyst tracker reuse has high extraction/adaptation, high authority reconciliation tests, MIT provenance, high dual-schema upgrades, and high migration/abandonment. **ADAPT schema idea locally**; **KILL** tracker/workstream state reuse.

### 6. Permission, MCP, and session execution

**HOLD** all direct-execution kills; **CONCEDE** three independently reusable *ideas*, not implementations:

1. A pure MCP descriptor parser may validate a redacted, already-admitted per-run descriptor. It must not read or migrate `~/.claude.json`, `.mcp.json`, shell environment, OAuth/token stores, or Nimbalyst user/workspace config. Turing confirms those are current custody locations and recommends temporary post-approval config with cleanup (`turing-agent-protocol.md:169-181`). **ADAPT locally after the offline MCP witness**, not from `McpConfigService`.
2. Pure provider event types/projectors may be adapted after fixtures from two admitted providers prove duplication (`turing-agent-protocol.md:233-243`). **DEFER**.
3. Fail-loud resume mismatch and partial-success Git/worktree outcomes are valuable failure-semantics precedent (`turing-agent-protocol.md:86-116`, `183-196`). They are not reusable process or Git implementations. **PRECEDENT**.

The Nimbalyst permission service, provider classes, internal SSE topology, shell-environment merge, terminal, Git/worktree executor, backend modules, storage, sync/mobile, telemetry, updater, and collaboration clients remain **KILL** for direct embedding. Hewitt independently assigns high or very high coupling and maintenance to those units (`hewitt-source-architecture.md:94-109`), and Turing calculates negative initial development-time reduction for provider/runtime/team/MCP/worktree extraction (`turing-agent-protocol.md:245-256`).

### 7. Development-time accounting

**REVISE** No candidate is a reducer merely because upstream code exists. The decision function is:

`net reduction = local design/build avoided - extraction - authority adaptation - acceptance/security tests - provenance - expected upgrade review - abandonment/migration`

Apply a hard multiplier when the candidate creates a second owner of policy, session truth, durable state, credentials, process lifecycle, or receipts: such candidates are negative until that authority is removed. Apply a timing gate when savings depend on future multiplicity: a shared provider projector cannot save work before two providers exist; a read-only host cannot save work before one local editor contract is stable. Every surviving candidate needs a one-page delta recording copied lines/symbols, imports, removed powers, local acceptance tests, pinned commit/license, upstream-diff trigger, owner, rollback, and deletion plan.

## REVISED FINAL POSITION

Nimbalyst should enter the shared synthesis as a pinned product/protocol specimen with a very small locally owned adaptation set. I retract any implication that “pure MIT helper” status alone makes copying cheaper. The default is local expression from source-backed contracts; literal code reuse must win a measured total-cost comparison and remain replaceable.

Shared-ready candidates:

| ID / name | Revised disposition | Minimum boundary and total-cost reading |
|---|---|---|
| `NIM-C01 WorkbenchEditorHost vocabulary` | **ADAPT locally** | Prune to read-only/load/subscription/dirty plus proposal-only save. Low build, medium tests, low upgrades; cheaper than copying broad `EditorHost`. |
| `NIM-C02 ReadOnlyHost behavior` | **ADAPT after C01** | Reexpress behavior against C01; no Electron, storage, AI, collaboration, backend, or authority imports. Low-medium total cost. |
| `NIM-C03 Manifest/validator pattern` | **PRECEDENT; ADAPT local fields/fixtures** | Use local Draft 2020-12 schemas and closed grants. Copying Nimbalyst's expanding manifest is medium recurring cost. |
| `NIM-C04 Public package smoke-check shape` | **ADAPT** | Local pack/type/example checks; no runtime authority. Low extraction, test, upgrade, and abandonment cost. |
| `NIM-C05 Raw-native event evidence plus canonical projection` | **ADAPT architecture; DEFER parser code** | Define artifact/projection contract now; implement with admitted provider witness; copy parsers only after two-provider duplication. |
| `NIM-C06 ExternalAgent lifecycle vocabulary` | **ADAPT with first provider witness** | `describe/prepare/run/collect/interrupt/inspect`, explicit abort/cleanup and fail-loud resume; kernel owns approval/outcome/receipt. Medium tests dominate cost. |
| `NIM-C07 Evidence diff viewer` | **PRECEDENT; DEFER implementation until L0 repair** | Presentation only over resolved before/after hashes; no “approval” semantics. Local build is cheaper than editor-code extraction. |
| `NIM-C08 Task-session-artifact-receipt relation view` | **ADAPT locally** | Read-only join over canonical IDs; no status, routing, tracker, or workstream ownership. Low total and abandonment cost. |
| `NIM-C09 Visual context packet` | **BUILD FROM OWNED local schema** | Nimbalyst supports user value only; local MCP research already owns the packet. |
| `NIM-C10 Redacted per-run MCP descriptor parser` | **DEFER until offline MCP witness; then ADAPT locally** | No ambient HOME/env/config/credentials; temporary post-approval materialization and cleanup. |
| `NIM-C11 Browser tool vocabulary` | **PRECEDENT** | Map later to local MCP/Playwright adapter; do not copy Electron browser service or IPC. |
| `NIM-C12 Failure semantics for resume/worktree partial success` | **PRECEDENT** | Preserve mismatch, interruption, and residue states; no provider/Git implementation reuse. |
| `NIM-C13 Nimbalyst permission/provider/session runtime` | **KILL direct reuse** | Creates second approval/session/process authority; negative total cost. |
| `NIM-C14 Terminal/Git/worktree/backend/storage execution` | **KILL direct reuse** | Ambient host authority and large state/dependency graph; separate future adapters only. |
| `NIM-C15 Sync/mobile/collaboration/credential stack` | **KILL current integration** | Separate server and remote-approval/custody threat model; high recurring operations and abandonment cost. |
| `NIM-C16 Telemetry and updater` | **KILL reuse** | Adds egress and executable supply-chain owners without reducing core implementation work. |

The revised adoption rule is strict: **ADAPT** only non-authoritative local contracts, views, validators, and evidence projections; use Nimbalyst UI and failure behavior as **PRECEDENT**; **DEFER** code whose value appears only with later providers or repaired L0; and **KILL** every path that imports a second policy, credential, process, session, durable-state, update, cloud, or receipt authority.
