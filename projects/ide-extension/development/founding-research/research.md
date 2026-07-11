---
dispatch_id: 2026-07-09-ide-extension-founding-research
dispatch_type: research
artifact_type: explorer-transcript
status: complete
---

# Ide Extension Founding Research - Explorer Transcript

This file preserves the explorer returns for the founding research dispatch. It
is source material for [findings.md](findings.md), not the final synthesis.

## Agent 1 - Turing, Alan

Read-only audit only. I inspected `projects/ui-prototyping-studio` relevant
backend, CLI, preview, Playwright, and persistence surfaces; no files edited and
no tests run.

### Evidence Paths

- `projects/ui-prototyping-studio/backend/src/cli/studio.ts`: CLI is the real
  integration seam. It wraps the orchestration module, emits JSON, uses
  `STUDIO_DATA`, and treats generation as external via `variants register`.
- `projects/ui-prototyping-studio/backend/src/cli/studio.ts`: `studio preview`
  starts a loopback `node:http` server, not Fastify, bound to `127.0.0.1`,
  rendering variants, staged before/after, diff, annotation,
  accept/discard/revert.
- `projects/ui-prototyping-studio/backend/src/cli/studio.ts`: export is
  terminal-only and requires `--confirm`; preview intentionally has no export
  button.
- `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/studio-orchestration-module.ts`:
  orchestration module is reusable: session, prompt, variants, baseline,
  comment, synthesize, approve, stage, accept, discard, revert, cycle, handoff,
  snapshot queries.
- `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/infrastructure/file-studio-session-store.ts`:
  persistence is single JSON document plus staged records, atomic
  temp-write/rename, counters, sessions, variants, comments, batches, revisions,
  handoffs.
- `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/infrastructure/file-artifact-content-store.ts`:
  HTML artifacts are content-addressed under the `STUDIO_DATA` directory in
  `artifacts/{staged,committed}`.
- `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/admission.ts`:
  reusable pure-ish scope fence over `data-od-id`, plus honest per-od-id diff.
- `projects/ui-prototyping-studio/backend/e2e/preview-accept.spec.ts`:
  Playwright proves in-preview accept advances head and revert appends a new
  head.
- `projects/ui-prototyping-studio/backend/e2e/human-loop.spec.ts`: Playwright
  proves click-to-annotate writes a core `CommentEvent`.
- `projects/ui-prototyping-studio/backend/e2e/governance.spec.ts`: e2e covers
  export confirmation, revert restore, and append-only revision growth.
- `projects/ui-prototyping-studio/INTEGRATION.md`: current host contract is
  shell-out CLI, JSON stdout, exit-code handling, fresh `STUDIO_DATA` directory
  per run.

### Reuse For `projects/ide-extension`

The strongest reusable contract is not the Fastify server; it is the
CLI-orchestration-preview triangle:

- Use the `studio` CLI contract as the first host boundary: spawn command, parse
  JSON, respect exit codes, keep per-workbench/session `STUDIO_DATA`.
- Reuse the orchestration shape: pure-ish application module behind adapters,
  with a file-backed store and artifact content port.
- Reuse the preview pattern for L0: local loopback server, no build step,
  iframe-rendered HTML/canvas/workbench panes, polling `/state`, reversible
  browser actions, terminal or explicit human gate for irreversible
  export/handoff.
- Reuse the artifact model: content-addressed committed/staged artifacts;
  ide-extension can generalize from HTML refs to canvas snapshots, workbench
  state JSON, Whisper drafts, Craft nodes, agent-envelope transcripts.
- Reuse e2e strategy: Playwright black-box preview tests plus white-box
  CLI/governance tests, each with isolated temp data.

### Overclaim Boundaries

Do not claim Studio gives ide-extension a ready IDE extension architecture. It
gives a local workbench precedent.

Do not claim existing Studio has OpenRouter, Craft, Whisper, ResonantOS,
pluggable agent envelopes, or canvas-native workbench support. Those are
ide-extension requirements, not implemented Studio surfaces.

Do not build on the legacy Fastify API as the governed source of truth without
re-auditing/fixing it. The documented and tested live contract is CLI-first;
Fastify is adjacent/legacy and not the preview server.

Do not claim multi-user, auth, remote deployment, concurrency safety, or durable
locking. Current persistence is local single-user JSON plus artifact files.

Do not overstate the validator: `admission.ts` is useful for `data-od-id` HTML
scope fencing, but its own comments name brittle node identity and incomplete
production-grade CSS handling.

### L0 Scaffold Implications

For `projects/ide-extension`, L0 should be a local governed workbench, not a
full IDE extension yet:

- `backend/` or `workbench/` package with a CLI entrypoint, e.g.
  `ide-workbench`.
- `STUDIO_DATA`-like isolated run directory contract from day one.
- Core module owns session state, artifacts, envelopes, gates, and append-only
  events.
- Preview server should be loopback-only and ephemeral, with `/state`,
  `/raw/*` or `/artifact/*`, `/comment` or `/event`, and reversible POST
  actions.
- Browser UI should show the actual workbench first: canvas/HTML panes, Craft
  context, Whisper draft, agent envelope lane, and state/gate strip. No
  marketing shell.
- First governed loop should be minimal: open session, attach/import
  artifact/context, propose envelope/candidate, preview, annotate/comment,
  accept/revert, append event, export/handoff with explicit confirm.
- Treat OpenRouter and pluggable agents as adapter ports behind the same
  proposer seam, not core dependencies in L0.

The crisp contract: ide-extension can inherit Studio's governed local-loop
pattern, not its domain. The reusable thing is deterministic admission around
non-deterministic proposal, visible in a loopback workbench, tested by CLI plus
Playwright.

## Agent 2 - Simon, Herbert

Read-only synthesis complete. No files edited.

### Evidence Paths

- `projects/ide-ergonomics/README.md`: IDE Ergonomics is a governed action
  surface, not a generic agent launcher. It turns conversation signals into
  bounded owner-safe actions: route cards, Craft panel, Connective,
  self-assembling approval, evidence rail.
- `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md`: The governing model is an
  open, default-deny coordinate space. The invariant floor is restraint:
  candidate is not promotion, preview is not execution, recommendation is not
  execution.
- `projects/ide-ergonomics/craft-control-panel/SPEC.md`: Craft panel is the
  strongest L0 control surface: read `.craft/ledger.yml`, show pending by node,
  select one row, ask one route question, then hand off to the owner route. No
  direct ledger mutation.
- `projects/ide-ergonomics/connective-task-manager/SPEC.md`: Connective adds
  human-factors scheduling: Craft state plus opt-in session indicators plus
  user-executed test evidence plus domain priority. It recommends lanes, never
  executes them.
- `projects/ide-ergonomics/self-assembling-ergonomics/SPEC.md`: Self-assembly
  is high-risk and must stay storyboarded/isolated in L0: evidence-backed
  suggestion, scoped consent, candidate space, frozen criterion, self-test, then
  user test and approval before owner-routed promotion.
- `projects/ide-ergonomics/SPELL-IDE-ASSISTED-ARCANUM-ROUTING.md`: The route
  contract already exists conceptually: action cards classify spans, validate
  bounded menus, preview handoffs/subagents/Craft/Connective, and only execute
  after approval with receipts.
- `projects/ide-ergonomics/development/studio-opportunity-prototypes/findings.md`:
  UI Prototyping Studio precedent says first scaffold should be an interactive
  session harness with stable `data-od-id`s, preview/no-write strips, receipt
  rail, route-card shell, and child sessions.
- `.agents/skills/craft/SKILL.md`: Craft owns durable recursive ledger state.
  `.craft/ledger.yml` is source of truth; `CRAFT.md` and `index.json` are
  derived/read surfaces.
- `.agents/skills/whisper/SKILL.md`: Whisper owns governed composition. Its
  review HTML contract is directly reusable: stable blocks, `part_id`, local
  comments, and exportable agent payloads for targeted revision.

### Product / Governance Contract

`projects/ide-extension` should start as a local HTML-server workbench, not a
full IDE extension and not an autonomous agent runtime.

First scaffold contract:

- Host shell: local server plus HTML/canvas workbench with panels for chat span,
  route card, Craft state, Whisper review, evidence rail, and agent envelope
  preview.
- Source authority: read models only. Craft reads `.craft/ledger.yml`; Whisper
  reads draft/review artifacts; route menus read declared capability contracts.
- Action grammar: every visible action must carry `source_ref`, `owner_route`,
  `allowed_effect`, `required_gate`, `forbidden_effects`, `expected_receipt`.
- Stable review surface: every clickable/control/comment target gets a stable
  id, following Studio `data-od-id` and Whisper `block_id` style.
- Pluggable agent envelopes: OpenRouter or other model backends should be
  transport adapters only. They may fill an envelope, but they do not own route
  authority, promotion, ledger mutation, or approval.
- ResonantOS precedent: based on the inspected corpus, no direct ResonantOS
  contract appears here; treat it as external inspiration for
  branch/session/workbench ergonomics, not as L0 governance authority unless a
  later source is admitted.
- Default posture: preview first, explicit confirmation for execution, receipt
  required for progress claims.

The hard line: the extension can make governed work legible and easier to choose.
It cannot become the thing that silently decides, promotes, mutates ledgers,
spawns agents, or ships assembled improvements.

### Craft And Whisper Fit In L0

Craft is the L0 control plane.

It should provide the left-side or lower rail: scope selector, ledger freshness,
pending-by-node list, selected row, blockers/decisions/gaps, next move, and one
route question. The extension may export and display Craft state, but mutations
must return through Craft or the selected owner route with a receipt.

Whisper is the L0 composition/review pane.

It should provide a reviewable text artifact surface: draft blocks, composition
parts, comments, requested change modes, and an exportable agent payload. This
fits perfectly beside Craft: Craft says what work is pending and who owns it;
Whisper says this text artifact has addressable review blocks and revision
intent.

Together in L0:

- Craft decides the governed work item.
- Whisper handles governed text composition/revision when the selected work item
  is writing-shaped.
- The IDE extension only mediates: select, preview, comment, route, export
  payload, record receipt.

### Risks Of Over-Automation

- Ledger capture becomes ledger authority: the panel starts fixing Craft rows
  directly instead of routing updates through Craft.
- Recommendation becomes execution: Connective ranks lanes and the UI quietly
  runs the top one.
- Human-state inference gets creepy: attention/load/fatigue are inferred or
  retained without explicit user review.
- Model backend becomes owner: OpenRouter/provider selection is mistaken for
  governance permission.
- Self-assembly ships itself: green tests are treated as promotion instead of
  ready for your test plus approval.
- Whisper comments become vague prompts: losing stable `block_id` / `part_id`
  breaks targeted revision and turns review back into prose mush.
- Canvas becomes dashboard theater: too many panels, graphs, or routes obscure
  the one actual next governed choice.
- Private/public boundary drift: IDE workbench copy must not imply
  DomainSpec/Saturn are shipped public capabilities; Arcanum-facing routes
  remain owner-bounded.

Bottom line: L0 should be a governed workbench that makes ownership, gates, and
receipts visible. The first success criterion is not agents do more. It is: the
human can choose the right owner-safe next move faster, with less memory load,
and without weakening governance.

## Agent 3 - Shannon, Claude

Status: read-only complete. Sources checked are current official host/tool/API
docs.

### Source Links And Facts

- VS Code Webview API: <https://code.visualstudio.com/api/extension-guides/webview>.
  Webviews are iframe-like extension-controlled HTML surfaces. They can be
  `WebviewPanel`s, custom editors, sidebar/panel webview views, and communicate
  with extensions through message passing. Scripts are disabled by default and
  require `enableScripts: true`.
- VS Code API `asExternalUri`: <https://code.visualstudio.com/api/references/vscode-api>.
  Extensions can resolve local/remote `http:` or `https:` URIs into externally
  accessible client URIs, including remote port forwarding when needed. Do not
  cache returned URIs.
- VS Code Webview UX: <https://code.visualstudio.com/api/ux-guidelines/webviews>.
  Microsoft's guidance: use webviews only when native VS Code APIs are
  inadequate; webviews have performance/accessibility costs.
- VSCodium: <https://vscodium.com/> and
  <https://github.com/VSCodium/vscodium/blob/master/docs/extensions.md>.
  VSCodium is a freely licensed build of VS Code. It uses Open VSX by default,
  not Microsoft Marketplace. VSIX/manual/private gallery distribution is
  feasible, but Microsoft Marketplace terms and some proprietary Microsoft
  extensions are not VSCodium-safe.
- VSCodium extension compatibility:
  <https://github.com/VSCodium/vscodium/blob/master/docs/extensions-compatibility.md>.
  Some Microsoft extensions are license- or product-gated and may not run on
  VSCodium. A self-authored webview extension using stable VS Code APIs should
  be the cleanest path.
- Playwright MCP: <https://github.com/microsoft/playwright-mcp>. Official
  Microsoft MCP server exposing browser automation through Playwright.
  Requirements include Node.js 18+ and VS Code, Cursor, Windsurf, Claude
  Desktop, Goose, Junie or any other MCP client. Supports
  `npx @playwright/mcp@latest`.
- Playwright MCP browser modes: same README. Can use persistent profiles,
  isolated profiles, `--cdp-endpoint`, `--extension` for existing Chrome/Edge
  tabs, headless/headed browsers, permissions grants, and local/SSE/programmatic
  server modes.
- OpenRouter Quickstart: <https://openrouter.ai/docs/quickstart>. Direct HTTP
  API to `/api/v1/chat/completions`, compatible with any language/framework;
  OpenAI SDK can be pointed at OpenRouter.
- OpenRouter Auth: <https://openrouter.ai/docs/api/reference/authentication>.
  Bearer-token API keys; keys may have credit limits. OpenAI SDK base URL is
  `https://openrouter.ai/api/v1`.
- OpenRouter Streaming: <https://openrouter.ai/docs/api/reference/streaming>.
  Streaming is supported via SSE; comment keepalives may appear and must be
  ignored by clients.
- OpenRouter Responses Beta:
  <https://openrouter.ai/docs/api/reference/responses/overview>. Responses API
  is beta, stateless, and may have breaking changes.

### Feasible Architecture For `projects/ide-extension`

Feasible L0 contract:

- Local HTML/canvas workbench served by a local Node backend, with
  Craft/Whisper/UI Studio/agent-envelope state kept server-side.
- VS Code/VSCodium extension shell opens the workbench as either embedded
  `WebviewPanel` or sidebar/panel `WebviewView`, for IDE-native experience, or
  adjacent external browser/local URL, resolved through `asExternalUri`, for
  stronger Playwright controllability.
- Webview frontend talks only to extension/backend through explicit message or
  HTTP channels.
- OpenRouter calls should be made from local backend/extension host, not
  directly from the webview, to avoid exposing API keys.
- Playwright MCP is best treated as an adjacent browser-control capability over
  the local workbench URL, not as proof that it can safely drive VSCodium's
  internal Electron webview panel.

### Hard Constraints And Security Boundaries

- VS Code webviews are powerful but discouraged unless native APIs are
  insufficient. Here, a canvas IDE workbench likely qualifies, but the claim
  must be explicit.
- Webview JavaScript is disabled by default; enabling it expands risk.
- Webview scripts do not get direct VS Code API access. They only get the
  special `acquireVsCodeApi()` bridge and JSON-serializable message passing.
- Keep the VS Code API object private; do not leak it globally.
- Use strict CSP: start from `default-src 'none'`; allow only required
  scripts/styles/images/connect targets.
- Restrict `localResourceRoots`; it is not a complete security boundary.
- Sanitize file contents, paths, settings, and workspace-derived text before
  rendering.
- Avoid `retainContextWhenHidden` unless necessary; it keeps scripts/state alive
  and has high memory overhead.
- VSCodium distribution must avoid reliance on Microsoft Marketplace-only or
  proprietary extensions.
- Playwright MCP can evaluate JS and mutate pages; use isolated profiles for
  tests and explicit approval gates for browser-control actions.
- OpenRouter Responses API is beta/stateless; Chat Completions is the safer
  initial API surface.

### Possible Vs Locally Proven

Possible from official docs:

- VSCodium-compatible extension with embedded HTML/canvas workbench via stable
  VS Code webview APIs.
- Adjacent local-server browser workbench opened from the IDE.
- Playwright MCP controlling a browser pointed at the local workbench.
- OpenRouter-backed model calls and streaming from a local backend.
- VSIX/Open VSX/private-gallery distribution for VSCodium.

Not locally proven in this stage:

- Playwright MCP controlling the embedded VSCodium/VS Code webview itself.
- CSP shape for localhost/WebSocket/SSE inside the final webview.
- OpenRouter key storage and streaming behavior in the actual scaffold.
- Any Craft/Whisper/UI Studio/agent envelope integration inside
  `projects/ide-extension`.

Recommendation: scaffold L0 as local-server-first with optional VS
Code/VSCodium webview wrapper. Treat embedded webview as the IDE chrome, not the
automation substrate; use adjacent browser mode for Playwright evidence until
local proof says otherwise.

## Agent 4 - Hewitt, Carl

Read-only. I did not edit files.

The envelope should be an actor boundary, not a runtime. L0 should define how a
pluggable agent is addressed, granted limited capabilities, asked to act, and
forced to return receipts. It should not claim autonomous IDE execution. The
dispatch row itself says the project is bounded founding research and not yet
our own Codex or Claude Code.

### Minimum Agent-Envelope Ports And Message Shape

Ports:

- `describe()`: returns adapter identity, runtime kind, supported modes,
  required env, permission vocabulary, and receipt support.
- `prepare(request)`: validates the requested task against grants and returns a
  plan/handoff, not execution.
- `run(envelope)`: optional L0 stub or dry run only unless explicitly approved.
- `interrupt(run_id)`: cancellation boundary.
- `collect(run_id)`: returns final artifact refs plus receipt.
- `inspect(run_id)`: returns current status/events without mutating state.

Minimum message:

```json
{
  "envelope_id": "uuid",
  "run_id": "uuid-or-null",
  "agent_ref": "openclaw|hermes|repo-agent|dry-run",
  "task": {
    "goal": "string",
    "context_refs": ["repo-relative-path-or-handle"],
    "expected_outputs": ["artifact|receipt|browser_receipt"]
  },
  "grants": {
    "filesystem": [{"scope": "path", "mode": "read|write|none"}],
    "network": "none|declared-hosts",
    "browser": "none|observe|act-after-approval",
    "shell": "none|allowlisted"
  },
  "approval": {
    "required": true,
    "approval_id": "id-or-null",
    "human_gate": "pending|approved|rejected"
  },
  "state": "draft|prepared|awaiting_approval|running|blocked|flagged|passed|failed|interrupted|timeout",
  "receipts": []
}
```

This mirrors existing dispatch constraints: subagents receive bounded `context`,
`initial_prompt`, `model`, `token_budget`, role, and angle, while orchestration
lives outside the agent. It also matches Arcanum adapters, where native surfaces
are parent-orchestrated handoffs with artifact-plus-stage receipt, not autonomous
shell-only execution.

### Tool Permission And Browser-Control Receipt Boundaries

L0 grants should be explicit, per-run, and revocable. Do not encode ambient
authority.

Minimum grant classes:

- `fs.read`: repo-relative allowlist only.
- `fs.write`: off by default; if enabled, target must be an approved
  project/work folder.
- `shell.exec`: off in L0 except declared dry-run commands.
- `network.call`: off by default; OpenRouter or external APIs need named
  provider, env var, model, and cost/timeout cap.
- `browser.observe`: allowed for screenshot/DOM/state capture.
- `browser.act`: gated; any click/type/navigation that changes state needs a
  pending action preview and human approval.
- `browser.external`: blocked in L0 for auth, wallet, payment, DAO, deployment,
  or account settings.

Browser-control receipt shape:

```json
{
  "receipt_id": "browser-receipt-id",
  "run_id": "run-id",
  "surface": "local-server|vscodium-webview|playwright",
  "action": "observe|navigate|click|type|screenshot",
  "target": "url-or-selector",
  "approval_id": "required-for-act",
  "before_ref": "artifact-path",
  "after_ref": "artifact-path",
  "status": "pass|flag|block|timeout",
  "residue": ["what could not be proven"]
}
```

This should follow receipt discipline already present in `dispatch-spec`: pass
receipts need artifacts or validation; block/flag needs blockers or residue.
Arcanum receipt validation also requires `receipt_id`, `run_id`, `stage`,
`owner`, `handoff_path`, arrays for artifacts/validation/blockers, and terminal
status.

### State Transitions And Failure/Approval Boundaries

Recommended L0 typestate:

`draft -> prepared -> awaiting_approval -> running -> passed|flagged|blocked|failed|interrupted|timeout`

Rules:

- `draft -> prepared`: adapter validates request and grants.
- `prepared -> awaiting_approval`: any write, shell, network, or browser-act
  grant is present.
- `awaiting_approval -> running`: explicit human approval only. Existing
  dispatch rules are blunt: nothing persists/runs before confirm, silence is not
  approval, and changed sheets re-enter the gate.
- `running -> passed`: requires receipt with artifact or validation evidence.
- `running -> flagged`: result exists but residue needs operator review.
- `running -> blocked`: missing grant, missing dependency, failed approval, or
  unsafe scope.
- `running -> interrupted|timeout|failed`: terminal, with receipt and reroute
  note.
- Any partial agent failure must be surfaced downstream, not hidden; the
  dispatch router explicitly treats agent errors as partial group results that
  downstream groups/final approver must know about.

Approval must remain parent-owned. An adapter may recommend; it must not
self-approve. Existing dispatch approval forbids self-approval and falls back to
parent on failure.

### What Must Remain Gated Or Out Of L0

Out of L0:

- Full autonomous agent runtime.
- Direct OpenClaw/Hermes execution beyond `describe/prepare/dry-run`.
- Unbounded repo writes.
- Shell execution outside allowlisted dry-run checks.
- Browser actions that mutate real accounts, credentials, wallets, payments,
  deployments, repository remotes, or production services.
- Trusted IDE agent claims.
- Background loops, multi-agent fanout, or nested dispatch without the governed
  dispatch gate.
- Treating `CRAFT.md` or UI state as authority. Craft says `.craft/ledger.yml`
  is source of truth; `CRAFT.md` and indexes are views.
- Any scaffold that makes `projects/ide-extension` look already validated.
  Current evidence supports a scaffold contract, not product proof.

The sharp L0 contract: a local HTML workbench can show Craft state,
compose/review prompts, prepare agent handoffs, and collect structured receipts;
every external agent/browser/tool act crosses an explicit grant plus approval
boundary. That gives OpenClaw/Hermes/repo-style agents a common envelope without
pretending the envelope is the agent.

## Agent 5 - Wiener, Norbert

Read-only; no files edited. Route treated as an already-authorized dispatch
return for `2026-07-09-ide-extension-founding-research`.

### Evidence Paths

- `/home/vrondelli/projects/workspace-resonant/.craft/ledger.yml`: Root Craft
  ledger is not generic product architecture; it tracks a security-pipeline
  workspace with artifacts, gaps, validations, blockers, and next moves. Useful
  precedent: L0 needs durable state indexes, artifact IDs, validation rows, and
  explicit active gaps rather than chat-only continuity.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/README.md`:
  Browser-first alpha is extension plus local Node bridge, not desktop shell.
  Key boundary: Augmentor acts only through typed mediated browser tools;
  wallet/signing/credentials/payment/public submits stay human-only.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/PRODUCT_GUIDE_BROWSER_FIRST.md`:
  Product path is one workbench/browser app, not dashboard controlling another
  app. Main workspace, side panel, memory, add-ons, provider routing, and task
  monitor are co-present surfaces.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-011-living-archive-host-service.md`:
  Living Archive precedent is host-mediated memory, not raw filesystem/vector
  store access. Intake, review, promotion, source ledgers, rollback, and audit
  logs are separate commands.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-012-living-archive-approval-policy.md`:
  Approval is tiered: auto, strategist/verifier, human. L0 should avoid
  everything manual and everything automatic.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-015-delegation-fabric-addon-catalog-native-tools.md`:
  Delegation Packet is canonical; `TASK.md` is rendered interoperability.
  Strong scaffold precedent for pluggable agent envelopes.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/docs/architecture/ADR-018-addon-sdk-v0.md`:
  Add-ons are workflow packages with manifests, capabilities, surfaces, tools,
  skills, scripts, hooks, engineer setup, audit, and non-goals.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha-issue-125-module-ownership-map/docs/architecture/MODULE-OWNERSHIP.md`:
  Current ownership contract: modules own UI/controllers/tests; `src/core` owns
  shared contracts; host routes own privileged actions. This is the clearest
  scaffold precedent for ide-extension.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha-issue-125-module-ownership-map/docs/architecture/ADR-026-minimal-kernel-replaceable-default-addons.md`:
  Minimal kernel plus replaceable default add-ons. Important for not making
  Whisper/Craft/OpenRouter/UI Studio inseparable core.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha-issue-125-module-ownership-map/docs/architecture/ADR-031-agent-addon-sdk-lessons-from-hermes.md`:
  Agent add-ons require identity, model state, memory access, smoke tests,
  install/audit preservation, approval gates, visible author labels.
- `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/lib/agent-control-planner.js`
  and `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/resonantos-side-panel-extension/src/lib/approval-policy.js`:
  Browser control is classified by task class, typed steps, success signals,
  stop conditions, and hard approval boundaries.

### Patterns ide-extension Should Build From

- Workbench as operating surface, not marketing shell. L0 should open directly
  into an HTML local-server/canvas IDE workbench: project canvas, active
  context, agent lanes, evidence/artifacts, local server health, and approval
  queue.
- Minimal kernel plus replaceable defaults. Kernel owns routing, capability
  grants, local server bridge, audit log, artifact registry, provider
  mediation, and emergency/manual controls. Craft, Whisper, UI Prototyping
  Studio, IDE Ergonomics, OpenRouter, and agent envelopes should be default
  modules/add-ons, not hardcoded monolith pieces.
- Delegation Packet as agent envelope base. For each pluggable agent:
  `envelope.json` as source of truth; rendered `TASK.md` or prompt as adapter
  artifact; return protocol, expected artifacts, verification, allowed tools,
  forbidden actions, approval gates, audit path.
- Craft-style durable state. L0 should create `.craft` or project-local
  governed state immediately: ledger, artifacts index, validation rows,
  gaps/blockers, next moves. Canvas state alone is not governance.
- Host-mediated memory/context. Whisper/Craft context should be read through
  scoped contracts. Writes should land as intake/artifacts first; promotion into
  canonical project memory requires review/validation.
- Typed action loop. Canvas/IDE actions need the same observe-plan-act-verify
  loop: task class, allowed actions, stop conditions, approval mode, visible
  trace, rollback/undo where possible.
- Manifested modules. Each studio/tool should declare: id, runtime type,
  surfaces, capabilities, connectors, scripts, hooks, model/provider needs,
  memory access mode, smoke tests, and non-goals.

### Avoid Duplicating Or Misnaming

- Do not call everything agent. Separate prompt, skill, connector, script, hook,
  module/add-on, and agent runtime.
- Do not duplicate ResonantOS names unless actually reusing the contract.
  Living Archive should not be renamed onto Craft/Whisper. Use neutral
  `memory-provider`, `artifact-ledger`, `context-intake`, `promotion-review`.
- Do not make OpenRouter the kernel. It is provider fabric input, not authority.
- Do not make UI Prototyping Studio the product. It is one workbench module
  inside a governed IDE surface.
- Do not let canvas nodes become authority without backing artifacts. A node
  should point to a packet, artifact, ledger row, validation result, or provider
  trace.
- Do not copy browser-first wallet boundaries literally, but do copy the class
  of boundary: human-only for external sends, public publication, credential
  entry, destructive filesystem changes, repo commits/pushes, provider key
  changes.

### L0 Product Boundary Implications

L0 should be a governed local IDE workbench scaffold, not a full autonomous IDE.
The contract should prove:

- local HTML server boots;
- canvas/workbench renders;
- modules register by manifest;
- Craft ledger/artifact index exists;
- agent envelope schema exists;
- OpenRouter/provider routing is mediated;
- actions are typed and auditable;
- human-only boundaries are enforced;
- first smoke tests validate module manifests, envelope shape, audit append, and
  a no-op delegated task.

The first architecture should name four layers:

- Kernel: local server, shell, registry, capabilities, audit, provider
  mediation.
- Workbench Modules: Craft, Whisper, UI Studio, IDE Ergonomics,
  provider/settings, artifact viewer.
- Agent Envelopes: packet schema, runtime adapters, return artifacts,
  verification.
- Evidence Loop: intake, validation, promotion, ledger/index updates.

That gives `projects/ide-extension` a clean L0: a system for governing IDE work,
not yet a claim that it can safely build arbitrary systems.
