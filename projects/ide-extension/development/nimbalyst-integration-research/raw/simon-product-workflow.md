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
