# Nimbalyst Integration Research - Explorer Transcript

Registered dispatch: `2026-07-11-nimbalyst-integration-research`
Pinned upstream: `Nimbalyst/nimbalyst@c8ca207c6004653ba2df3d81e06133ce2e9fad3d`

The sections below are mechanically copied from the four explorer returns without editorial changes.

## Agent 1 - Simon, Herbert

# Simon, Herbert - Nimbalyst Product-Workflow Exploration

**Registered research:** `2026-07-11-nimbalyst-integration-research`
**Upstream boundary:** `/tmp/nimbalyst-c8ca207c6004` at
`c8ca207c6004653ba2df3d81e06133ce2e9fad3d` (read only)
**Local comparison boundary:** `projects/ide-extension`, then
`projects/ui-prototyping-studio` and `projects/ide-ergonomics` only where noted.

## Method And Evidence Status

This is an empirical product-workflow reading, not an adoption plan or a security
review. `O` means direct observation in the pinned source. `D` means documented
product behavior in upstream README, feature inventory, or docs; it was not
independently exercised here. `I` is a source-backed inference. `R` is a local
recommendation. The official documentation entry point is
<https://docs.nimbalyst.com/>; its rendered content was not relied on where the
pinned source provides a more precise claim.

The upstream client repository is MIT-licensed, but that does **not** make its
separate sync service, hosted surfaces, or its product behavior a local dependency:
the upstream README identifies the Electron, iOS, runtime, protocol, SDK, and
extension packages, then states that the `wss://sync.nimbalyst.com` collaboration
server is a separate project [O:
`c8ca207c6004653ba2df3d81e06133ce2e9fad3d:README.md:124-146`]. Its licensing note
repeats that separation [O: `LICENSING.md:1-9`]. The repository's client code is
MIT [O: `LICENSE:1-20`].

## INITIAL POSITION

**Do not integrate Nimbalyst as an execution substrate, collaboration backend, or
agent authority.** Its interesting contribution to the local work is a set of
product hypotheses: a person may navigate the same work through files, sessions,
and tasks; an agent's change needs a reviewable visual representation; and a task
can keep its evidence, session, and changed files mutually reachable.

**R:** retain those as small, reversible interface/read-model candidates only. The
current `ide-extension` is an L0/L0.5 witness, not an IDE agent:
`SPEC.md:18-77` and `README.md:4-34` bound it to a local workbench and forbid real
external MCP, live browser, provider, GitHub, deployment, and persistent authority
claims. The accepted review additionally leaves present L0 repair work open,
including exactly-once approval, attribution, schema enforcement, and persistence
consistency [O: `projects/ide-extension/development/architecture-review-2026-07-10/findings.md:15-107`].
No Nimbalyst-derived surface should promote an adapter, approve an action, write
durable state, or mint a receipt.

## Observed Feature Map

| Product concern | Observation | Evidence status and source | Local reading |
| --- | --- | --- | --- |
| **Files mode** | A file-tree and multi-tab workspace offers content search, quick-open, auto-save, local document history/diff, and external-change reload. | [D: `docs/FEATURE_INVENTORY.md:160-185`]; separate renderer branches identify files, agent, and tracker view wrappers [O: `packages/electron/src/renderer/App.tsx:525`, `2176-2281`]. | A strong navigation hypothesis; not evidence that the local browser workbench should become a full filesystem editor. |
| **Visual editors and diffs** | Built-ins include rich text, Monaco, CSV, diagrams, mockups, data models, PDFs, database browser, and a browser; cross-editor review offers per-file approval/rejection and editor-specific diff presentations. | [D: `docs/FEATURE_INVENTORY.md:5-27`]. | The useful unit is a review projection: before/after plus explicit disposition, not any particular editor stack. |
| **History, search, tabs** | File history is described as local with a diff viewer; session search is full-text; tabs retain dirty state and reopen/navigate controls. | [D: `docs/FEATURE_INVENTORY.md:37-52`, `160-185`]. | `ide-extension` should first repair evidence-reference integrity before presenting history as a reliable proof surface. |
| **Agent mode** | Full-screen sessions expose plan/model/effort controls, context consumption, edited-file scope, pending review, tool-call red/green diffs, durable interactive prompts, queued inputs, and slash-command typeahead. | [D: `docs/FEATURE_INVENTORY.md:73-99`]. | Attractive interaction grammar, but no authority transfer: local research already says chat may prepare/display evidence, never approve itself [O: `mcp-chat-extension-integration-research/findings.md:19-43`]. |
| **Sessions and workstreams** | Sessions can be searched, resumed, forked, grouped as parent/child workstreams, and shown as a kanban; child sessions share file/tabs overview in sibling mode. | [D: `docs/FEATURE_INVENTORY.md:37-71`]. | A candidate *read-only relation model*: task -> session -> changed artifact -> evidence. It must remain distinct from local receipt authority. |
| **Teams and collaboration** | Document collaboration uses a host-owned transport, encrypted relay, Yjs binding, offline queue, presence, and extension support. | [D: `docs/COLLABORATION_GUIDE.md:3-13`, `27-45`]; the feature inventory says team data has two custody modes and server-managed team data is not zero-knowledge [D: `docs/FEATURE_INVENTORY.md:244-277`]. | Out of scope. This depends on a distinct server/identity/key-management system, not merely an editor component. |
| **Commands and skills** | User-facing slash-command typeahead is documented; extensions can expose editors and AI/MCP tools under host contracts. | [D: `docs/FEATURE_INVENTORY.md:94-99`, `58-60`]. | Do not equate these with Arcanum skills. A command surface may *propose* an existing governed route, but ownership and validation stay local. |
| **Tasks / tracker mode** | Markdown/frontmatter plans are scanned, filtered, linked to sessions, and can launch agent sessions; trackers cover plans, bugs, and decisions. | [D: `docs/PLANNING_SYSTEM.md:5-14`, `80-90`, `125-189`; `docs/TRACKER_WORKFLOWS.md:3-28`]. | Material overlap with Craft/task evidence, but copying the tracker model risks a second canonical ledger. Use references to the existing authority, never a parallel source of truth. |
| **Git, worktrees, terminal** | Developer features include status, commit/PR views, worktrees, and an embedded terminal; worktrees isolate coding sessions and support merge/rebase/cleanup. | [D: `docs/FEATURE_INVENTORY.md:110-121`, `137-158`]. | Explicitly deferred. The local L0.5 no-go excludes live PR/deployment hooks and broad execution; a terminal or worktree is not a harmless view. |
| **Mobile and non-developer operation** | README positions the product for developers, product managers, designers, and builders; mobile clients support session follow-up and interactive responses. | [D: `README.md:1-9`, `49-56`; `docs/FEATURE_INVENTORY.md:205-242`]. | Treat as product evidence that review/approval can be interruptible and low-bandwidth, not as justification for mobile, hosted sync, or remote approval in this research lane. |

## User Jobs

1. **Orient:** “What work exists, where is it, and what needs my attention?”
   Files, sessions, and tracker items become alternate entry points rather than
   disconnected screens [D: `README.md:28-39`; `docs/FEATURE_INVENTORY.md:37-71`].
2. **Externalize work for inspection:** “Show the proposed change in the medium I
   understand.” The upstream product describes WYSIWYG change review rather than
   requiring every person to read raw code [D: `README.md:16-24`].
3. **Keep parallel work legible:** “Which agent/session owns this thread, and what
   did it touch?” Workstreams, kanban, edited-file scope, and teammate status serve
   this job [D: `docs/FEATURE_INVENTORY.md:54-71`, `100-108`].
4. **Decide at an interruption point:** “Can I review, answer, defer, or reject
   without reconstructing the whole session?” The documented interactive prompts
   and mobile response path are evidence for the interaction, not proof of remote
   authority [D: `docs/FEATURE_INVENTORY.md:84-90`, `205-242`].
5. **Return to a durable rationale:** “Why did this change/task/session happen?”
   Markdown planning and decision tracker workflows provide one product answer
   [D: `docs/PLANNING_SYSTEM.md:5-14`; `docs/TRACKER_WORKFLOWS.md:5-28`].

## Interaction Primitives

| Primitive | Nimbalyst evidence | Candidate local reuse | Recommendation |
| --- | --- | --- | --- |
| **Triangulated navigation** | Files, Agent, and Tracker modes are explicit application modes [O: `packages/electron/src/renderer/App.tsx:525`, `2176-2281`]. | A small switch between workbench artifact, envelope/receipt queue, and governed task reference. | **Consider later**, read-only first. |
| **Visual change review** | Editor-specific diffs plus per-file approve/reject are documented [D: `docs/FEATURE_INVENTORY.md:20-27`]. | Make the current evidence pair and disposition legible. | **Candidate after L0 repairs.** The viewer must not imply that a browser click proves human attribution. |
| **Bidirectional links** | File/session linkage and plan/session linkage are documented [D: `README.md:28-39`; `docs/PLANNING_SYSTEM.md:146-189`]. | Link a local task reference to an envelope, evidence artifact, and receipt ID. | **Reuse as schema idea**, references only. |
| **Status lanes** | Session kanban tracks phase columns [D: `docs/FEATURE_INVENTORY.md:63-71`]. | A local queue showing prepared, approval-needed, blocked, and receipt-emitted states. | **Do not reuse yet.** The current L0 lifecycle/replay defects make a status board misleading until fixed. |
| **Interactive prompt** | Approval/permission prompts persist across restart [D: `docs/FEATURE_INVENTORY.md:84-90`]. | A human-facing request for one exact approval. | **Conceptual overlap only.** Local approval requires attested actor/session separation before an effectful lane [O: `projects/ide-extension/development/architecture-review-2026-07-10/findings.md:19-39`]. |
| **Extension/editor host** | Upstream exposes a common editor contract [D: `README.md:58-60`]. | A future visual witness module with narrow input/output contract. | **Future research**, no SDK/code reuse decision. |

## Workflow Sequence (Observed And Adapted)

### Documented upstream sequence

`open/create file -> edit or ask an agent -> inspect red/green change ->
accept/reject -> manage/search/resume the session` [D: `README.md:81-88`]. For
planned development, that expands into `plan document -> launch agent -> record
agent session -> update plan status` [D: `docs/PLANNING_SYSTEM.md:156-189`].

### Local compatible sequence (recommendation)

`governed task/reference -> prepare envelope -> render proposed context and
evidence -> attested human approval -> one allowlisted witness invocation ->
kernel-written evidence -> kernel receipt -> read-only linked history`.

This preserves the local L0.5 shape rather than importing an agent-manager model:
the accepted research requires local/offline stdio, one observe tool, exact approval,
hash-bound evidence, and kernel-minted receipts [O:
`mcp-chat-extension-integration-research/findings.md:45-67`, `81-95`].

## Candidate Reuse Units And Initial Recommendation

| Candidate | Recommendation | Reasoning |
| --- | --- | --- |
| **Evidence/diff viewer** | **Research-ready after L0 fixes; do not implement now.** | Strong fit with `ui-prototyping-studio`'s proposed `apply -> validate -> stage -> accept/discard` split and honest diff [O: `projects/ui-prototyping-studio/interfaces.md:33-48`]. But `ide-extension` lacks materialized/validated after-state evidence today [O: `projects/ide-extension/development/architecture-review-2026-07-10/findings.md:88-107`]. |
| **Task-session-artifact link projection** | **Candidate.** | Aligns with Nimbalyst's user orientation job while keeping Craft/Arcanum as canonical owners. Local IDE Ergonomics says surface cards may route but never promote or execute [O: `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md:35-46`, `247-259`]. |
| **Prepared/approval/receipt queue** | **Defer until correctness repairs land.** | Useful orientation primitive, but a queue is false reassurance while approvals replay, pending items can be orphaned, and state/logs diverge [O: `projects/ide-extension/development/architecture-review-2026-07-10/findings.md:31-84`]. |
| **Visual context packet** | **Research-ready, schema-owned locally.** | The existing local research already proposes `DesignFeedbackContextPacket` with selected element, screenshot/artifact ref, URL, source candidates, and context refs [O: `mcp-chat-extension-integration-research/findings.md:45-65`]. Nimbalyst supports the user-value hypothesis; it does not own the schema. |
| **Nimbalyst extension SDK or editor code** | **No decision / no direct reuse.** | MIT permits code reuse subject to notice, but this research has not established contract fit, dependency envelope, security model, maintenance cost, or a local owner. |
| **MCP configuration/agent provider model** | **Reject for this slice.** | Nimbalyst's provider/MCP surface is broad product infrastructure; local L0.5 admits only a fake, offline, allowlisted observer witness and rejects network, mutation, broad tools, and adapter receipt authority [O: `mcp-chat-extension-integration-research/findings.md:55-87`]. |
| **Worktrees/terminal/git/PR controls** | **Reject for this slice.** | They are action surfaces, not just ergonomic widgets, and conflict with the present L0.5 no-go boundary. |
| **Teams, sync server, hosted/mobile surfaces** | **Out of scope.** | Separate server and custody posture; no local integration rationale or security decision exists. |

## Unknowns And Required Follow-Up Evidence

- **Runtime verification:** most product claims above are documentation claims. A future product evaluation should run a pinned desktop build and record reproducible UI traces rather than treating README screenshots as behavior proof.
- **Official-doc detail:** the official documentation root was identified, but this pass did not extract page-level documentation evidence. Pinned source is the source of the specific claims above.
- **Version/maintenance fit:** no compatibility, dependency, license-notice placement, or upstream API stability review was performed for direct code reuse.
- **Server boundary:** the separate collaboration server is acknowledged, but its protocol, hosting, authentication, and custody mechanisms were not audited.
- **Local correctness gate:** no integration candidate advances before the accepted L0 change requests are resolved and independently reverified.
- **Product question still open:** whether a governed IDE user benefits more from a single “next governed step” card than a mode-rich workspace is unresolved. The existing local product position intentionally starts with the smaller card [O: `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md:234-245`].

## Evidence Links

- Official docs: <https://docs.nimbalyst.com/>
- Upstream repository: <https://github.com/Nimbalyst/nimbalyst>
- Upstream product/documentation basis: `c8ca207c6004653ba2df3d81e06133ce2e9fad3d:README.md:1-147`; `docs/FEATURE_INVENTORY.md:1-277`; `docs/PLANNING_SYSTEM.md:1-315`; `docs/COLLABORATION_GUIDE.md:1-45`; `LICENSING.md:1-9`; `LICENSE:1-20`.
- Local boundary: `projects/ide-extension/SPEC.md:18-77`; `projects/ide-extension/development/architecture-review-2026-07-10/findings.md:15-180`; `projects/ide-extension/development/mcp-chat-extension-integration-research/findings.md:1-95`.
- Material overlap only: `projects/ui-prototyping-studio/interfaces.md:20-48`; `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md:35-46`, `234-259`.

## ROBOT-TALKS CONFRONTATION

**Confrontation boundary.** This section compares the four independently written
raw returns. It is a research synthesis, not an admission decision. Exact upstream
paths below resolve at `c8ca207c6004653ba2df3d81e06133ce2e9fad3d`; local paths are
the current research/review artifacts.

### 1. Product Grammar Versus Code Reuse - REVISE

**Resolution.** I concede Hewitt's narrower claim: the extension SDK is a real,
separately packaged TypeScript seam with no declared runtime dependencies [O:
`c8ca207c6004653ba2df3d81e06133ce2e9fad3d:packages/extension-sdk/package.json:50-64`].
I do **not** concede that copying it is therefore cheaper. `EditorHost` includes
save, dirty, history, storage, editor API, context, collaboration, and menu
responsibilities [O: `packages/extension-sdk/src/types/editor.ts:283-603`], whereas
the local candidate needs a read-only evidence projection. Copying a broad interface
would require more pruning, provenance, compatibility, and negative tests than
writing the small local port.

**Revised finding.** Adopt the *contract-design precedent*, not the SDK package.
If a future editor needs only preloaded content, filename/path, read-only state,
theme, and subscriptions, locally express a `WorkbenchEvidenceHost`. The upstream
`createReadOnlyHost` is evidence that this smaller form is feasible, but even it
implements the full host through mutating no-ops and an in-memory secret-shaped
storage surface [O: `packages/extension-sdk/src/createReadOnlyHost.ts:44-119`].
That is not a reason to introduce the wider contract.

### 2. SDK Seam Versus Authority Coupling - CONCEDE

**Resolution.** Turing and Ashby are correct that the agent/provider surface is
coupled to Nimbalyst-owned lifecycle and authority. `SessionOptions` carries absolute
workspace path, permission mode, MCP configuration, environment, and tool lists [O:
`packages/extension-sdk/src/agents/AgentProtocol.ts:62-94`]. The host then offers
credential lookup, workspace reads/writes, raw-log persistence, and session-scoped
MCP registration [O: `packages/extension-sdk/src/agents/AgentProtocolHost.ts:160-219`],
while making provider permission authoritative at tool-call time [O:
`AgentProtocolHost.ts:45-62`]. Its extension permissions separately acknowledge
ambient Node powers in backend modules [O:
`packages/extension-sdk/src/types/permissions.ts:1-132`].

**Consequence.** `EditorHost` can inform a read-only visual port only. The
`AgentProtocol`, provider host, backend-module, storage, and permission interfaces
are **not** candidate local authority. This holds the existing local rule that an
adapter can propose/observe but cannot approve, mutate durable state, or mint a
receipt [O: `projects/ide-extension/development/mcp-chat-extension-integration-research/findings.md:45-67`].

### 3. Provider/Event Projection - REVISE

**Resolution.** Turing's provider-native raw-event plus pure-projection pattern
improves the user workflow only when there are multiple real provider formats or a
need to revisit a run without losing inspectable evidence. It supports the user job
of returning to a durable rationale and rendering tool/error progress without
treating a provider completion as approval. The upstream actually rebuilds canonical
events from raw messages and projects a view model [O:
`packages/runtime/src/ai/server/transcript/TranscriptRuntime.ts:266-286`;
`packages/runtime/src/ai/server/transcript/TranscriptProjector.ts:120-160`].

**Revised finding.** Adopt a local event vocabulary now only as an explicitly
non-authoritative descriptor for the fake stdio witness: `raw`, `text`, `tool_call`,
`tool_result`, `error`, `complete`, plus observed interrupt/cleanup outcomes. Defer
raw-to-canonical parser extraction until a second real provider is admitted. Do not
copy the provider host: its raw logging writes to Nimbalyst session storage, and its
protocol carries provider permission/MCP/env custody. This agrees with Turing's
two-stage recommendation [O:
`raw/turing-agent-protocol.md:217-256`].

### 4. Diff Approval - REVISE

**Resolution.** Ashby is right: red/green/Keep/Undo is not pre-effect
authorization. I revise the evidence/diff candidate from “research-ready after L0
fixes” to **presentation-only precedent until a local after-state artifact exists**.
The accepted review establishes that the current `after_ref` is symbolic and does
not resolve as a file [O:
`projects/ide-extension/development/architecture-review-2026-07-10/findings.md:88-107`].

**Consequence.** A viewer may render a proposed before/after pair and an approval
status; it must neither cause execution nor claim that visual acceptance is the
kernel authorization. Adapt it only after actual before/after artifacts, reference
validation, exact-once approval, and actor/session attribution are independently
reverified [O: `architecture-review-2026-07-10/findings.md:19-39`, `88-107`].

### 5. Tasks, Workstreams, And Session Links - HOLD

**Resolution.** The user job is distinct, but the local canonical state is not.
Nimbalyst demonstrates useful traversal between plans, files, and sessions [D:
`c8ca207c6004653ba2df3d81e06133ce2e9fad3d:README.md:28-39`; `docs/PLANNING_SYSTEM.md:146-189`].
Craft/Arcanum already owns routing and status; the local product rule is that a
surface may route but not promote or execute [O:
`projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md:35-46`, `247-259`].

**Held position.** A derived, read-only relation projection is genuinely useful
only when it joins existing canonical IDs: `task/reference -> envelope/run ->
evidence -> receipt`. It must not persist its own task/session status, phase, or
route. Without those links resolving to existing owners, it is duplicate state and
is rejected.

### 6. Permission, MCP, And Session Execution - CONCEDE

**Resolution.** Ashby's kills stand for direct reuse: permission service,
shell-environment MCP configuration, terminal/Git/worktree execution, sync/mobile,
telemetry, and updater all create an authority/custody plane that the local witness
does not own [O: `raw/ashby-safety-operations.md:19-34`, `63-81`]. Hewitt and
Turing identify a smaller independently reusable residue: type/vocabulary shapes,
manifest-validation *patterns*, pure projection functions, and package-check
discipline [O: `raw/hewitt-source-architecture.md:94-109`; `raw/turing-agent-protocol.md:217-256`].

**Consequence.** That residue is to be re-expressed locally with no Nimbalyst
runtime dependency. A parser/type is admissible only when it takes supplied data,
performs no I/O, performs no policy decision, and cannot gain credentials, ambient
environment, process, network, or durable-write authority. It remains subject to
MIT provenance if copied rather than independently expressed.

### 7. Development-Time Accounting - HOLD

Initial coding time is not the decision metric. A candidate is a reducer only when
its total cost remains below local expression **without** creating a second
policy/session authority. Costs below are qualitative and include the full requested
life cycle.

| ID | Candidate | Extraction | Adaptation | Test | Provenance | Upgrade | Abandonment | Net / disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RT-01 | `WorkbenchEvidenceHost` contract, inspired by read-only editor host | Low | Low | Low-medium fixture/render tests | Low if re-expressed; medium if copied | Low | Low | **ADAPT** by local expression; copied helper has no demonstrated advantage. |
| RT-02 | Before/after evidence-diff projection | Low | Medium: bind to local artifact refs | Medium-high negative evidence/approval tests | Low | Low | Low | **DEFER**, then **ADAPT** only after L0 evidence/approval repairs. |
| RT-03 | Task-session-artifact relation projection | Low | Medium: resolve existing IDs only | Medium broken/stale-link tests | Low | Low | Low | **ADAPT** as derived read model; **KILL** if it stores a parallel lifecycle. |
| RT-04 | External-agent lifecycle/event vocabulary | Low | Medium: map to envelope/run states | Medium-high fake-agent crash/timeout/abort/replay fixtures | Low | Low-medium | Low | **ADOPT** as locally owned vocabulary, no dependency. |
| RT-05 | Raw-to-canonical transcript projection | Medium | Medium | High deterministic multi-provider corpus | Medium if code copied | Medium | Medium | **DEFER** until a second provider; then **ADAPT** pattern or selected pure code. |
| RT-06 | SDK manifest/validator pattern and public checks | Low | Medium: remove Nimbalyst contributions | Medium hostile-manifest tests | Medium | Medium | Low | **PRECEDENT** now; **ADAPT** only for a separately owned local module contract. |
| RT-07 | Permission service, provider host, MCP config, terminal/Git/worktree | High | Very high authority rewrite | Very high custody/process negative suite | High | High | High | **KILL** direct reuse. |
| RT-08 | Collaboration server/client, mobile, telemetry, updater | Very high | Very high service/identity operations | Very high | High | High | High | **KILL** for this research boundary. |

## REVISED FINAL POSITION

Nimbalyst remains a strong **product and protocol precedent**, not a substrate.
The local development-time reducers are: a locally owned, read-only evidence host;
a derived task/run/evidence/receipt relation projection; and a small external-agent
lifecycle/event vocabulary. None copies Nimbalyst policy, session authority,
credential handling, process execution, or storage.

Visual diff is now explicitly presentation-only and blocked on real after-state
evidence. Raw-to-canonical projection is deferred until two provider formats make
its fixture and maintenance cost worthwhile. The current L0 repair list remains a
hard gate before any effectful adapter or UI implication is promoted [O:
`projects/ide-extension/development/architecture-review-2026-07-10/findings.md:171-180`].

### Shared-Ready Candidate List

| ID | Name | Revised recommendation |
| --- | --- | --- |
| RT-01 | Local read-only `WorkbenchEvidenceHost` | **ADAPT** by local expression. |
| RT-02 | Evidence-diff projection | **DEFER**, then **ADAPT** after evidence and approval gates pass. |
| RT-03 | Canonical task/run/evidence/receipt relation projection | **ADAPT** as read-only derived state; **KILL** parallel authority. |
| RT-04 | External-agent lifecycle and event vocabulary | **ADOPT** as a local contract, no upstream dependency. |
| RT-05 | Raw-to-canonical transcript projector | **DEFER** until a second provider; then **ADAPT** selectively. |
| RT-06 | Manifest/validator and package-check pattern | **PRECEDENT**; adapt only under a local owner. |
| RT-07 | Nimbalyst permission/provider/MCP/terminal/Git/worktree execution | **KILL** direct reuse. |
| RT-08 | Collaboration, hosted sync, mobile, telemetry, updater | **KILL** for current boundary. |

## Agent 2 - Hewitt, Carl

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

## Agent 3 - Turing, Alan

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

## Agent 4 - Ashby, W. Ross

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
