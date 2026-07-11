# MCP Chat Extension Integration Research

- Dispatch: `2026-07-10-mcp-chat-extension-integration-research`
- Date: 2026-07-10
- Mode: DomainSpec subagent research dispatch
- Scope: `ide-extension` integration strategy for MCP servers, chat extensions, browser-control witnesses, and external patterns from `claude-max-mcp`, Yocoolab MCP, official MCP, Claude Code Chrome, Chrome DevTools for agents, and existing local `ide-extension` architecture.
- Status: explorer transcript complete

This file preserves the explorer pass and robot-talk final positions used by the synthesizer. Minor punctuation has been normalized to ASCII where needed; local and web source references are kept with the agent returns.

## Explorer: Hewitt, Carl

### Initial Return

**Hewitt Finding**

No files edited.

1. **Capability Map**

`claude-max-mcp` is a narrow stdio MCP server with one capability: `ask_claude(prompt)`. It exposes no local authority surface beyond MCP tool invocation; the actual reasoning call is delegated to Claude Code CLI in print mode. Upstream describes this as MCP client -> `claude-max-mcp` -> `claude -p --model ...` -> Claude Code OAuth/subscription path. Source confirms the server uses `@modelcontextprotocol/sdk`, Node `>=18`, and `src/server.js` as the binary.

2. **Install / Config / Env Surface**

Install requires Claude Code CLI, `claude /login`, then `npm install -g claude-max-mcp` or `npx -y claude-max-mcp`; clients register it as a stdio MCP command. Config is entirely env-driven: model, Claude binary path, timeout, cwd, tool name, and extra Claude args. Local fit: `ide-extension` already treats providers as backend/extension-host adapters with keys outside browser storage, and OpenRouter is explicitly "provider-transport," not authority ([openrouter.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/adapters/openrouter.mjs:1), [ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:67)).

3. **How `ask_claude` Works / Custody**

Implementation path is plain subprocess custody: validate `prompt`, build `['-p', prompt, '--model', MODEL, ...EXTRA_ARGS]`, spawn `CLAUDE_BIN`, pipe stdout/stderr, enforce timeout, return final text only. OAuth custody remains with Claude Code reading `~/.claude.json`; upstream says the MCP server does not read the file directly. Authority implication: output is untrusted provider text. It is not an `ide-extension` receipt, approval, ledger mutation, or evidence authority. The delegated session may see `CLAUDE_MAX_MCP_CWD` and whatever Claude Code tools its args allow.

4. **Risks**

Security: subprocess inherits env/HOME/CWD; constrain CWD and pass `--allowed-tools` through extra args. Upstream recommends this for scoping, but the project also admits delegated Claude uses its own default toolset unless configured.

Cost: repo claims calls debit Claude Pro/Max subscription, not API billing, but this should be validated against the user account dashboard; it has no local cost tracking.

Latency: acceptable for chat, weak for tight tool loops; docs cite subprocess overhead and no streaming/persistence.

Subscription/OAuth: login expiry, daemon HOME/PATH stripping, plan caps, and changing Anthropic plan rules are operational risks. Upstream explicitly says limits change and Max is metered, not unlimited.

5. **ide-extension Reuse / Avoid**

Reuse: adapter pattern, server-side credential/OAuth custody, env-scoped model/tool/cwd config, smoke test, multi-instance provider descriptors. Treat `claude-max-mcp` as a `provider-transport` peer to OpenRouter.

Adapt: wrap calls in `ide-extension` envelopes: prepare -> approval -> run -> receipt. Current kernel already blocks before approval and appends receipts ([server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:127), [grants.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/kernel/grants.mjs:1)).

Avoid: upstream Hermes "return Claude unchanged" conduit pattern; it conflicts with local authority, receipts, and claim discipline. Also avoid browser/webview credential storage, default broad CWD/tool access, and treating subscription delegation as free capacity.

6. **Smallest ide-extension Witness**

L0.5 witness: add a `claude-delegation` provider adapter behind the existing local Node kernel. It should prepare an envelope with `requested_grants: ["network.call"]`, `agent_ref: "provider.claude-max-mcp"`, redacted env descriptor, CWD fixture, and `CLAUDE_MAX_MCP_EXTRA_ARGS="--allowed-tools=Read,Glob,Grep"`. First prove `/api/envelopes/run` returns approval-required; after approval, run either `claude-max-mcp --smoke` or one tiny fixture prompt; write a provider-call receipt with model, cwd, timeout, prompt artifact ref, output artifact ref, and "usage unavailable." This extends the current L0 acceptance shape, which already requires render, manifest load, blocked run, approval, receipt, and persisted state ([SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:100), [l0-smoke.test.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/tests/l0-smoke.test.mjs:35)).

Verdict: yes, model-delegation MCP can fit, but only as a provider adapter behind local authority. It should never become the authority boundary itself.

### Robot-Talk Final Position

**Hewitt Final Position**

I accept the siblings' core correction: the integration target is not "add Claude Max MCP." It is "admit MCP/chat/browser capabilities through the local `ide-extension` authority boundary." My initial recommendation was directionally right on Claude Max MCP as a provider adapter, but too centered on model delegation as the first witness.

**What I Accept**

Alexander is right: Yocoolab's reusable value is product shape, not service adoption. The feedback-thread bundle, selection history, correlation IDs, source-candidate ranking, and companion messages are stronger immediate UX patterns than Claude delegation itself.

Wiener is right: MCP is capability exposure, not authority. Stdio should be the default local adapter lane. Streamable HTTP, Chrome DevTools MCP, and Claude Code Chrome are useful witnesses only after origin/auth/session-state risks are bounded.

Ashby is right and should dominate the decision: `ide-extension` authority remains the loopback Node kernel, durable state, schemas, approval queue, and receipts. Chat panels, MCP servers, browser extensions, and model providers propose or observe; they do not approve, mutate, or mint receipts.

**What I Reject**

Reject any conduit pattern where a router returns provider output unchanged as authoritative. That was explicitly present in the Claude Max MCP ecosystem's Hermes example, and it does not fit `ide-extension`.

Reject remote Yocoolab/GitHub/Pendo adoption, direct PR writes, permissive bridge CORS, hidden bridge-token assumptions, or any JWT/PAT custody inside browser/chat surfaces.

Reject treating Claude Max MCP subscription delegation as a cost primitive. It may be useful, but it has no local usage accounting and depends on external OAuth/subscription behavior.

Reject Streamable HTTP or live-browser control as an L0.5 default. Those are later lanes after local stdio/read-only witnesses prove receipt binding.

**Change To My Recommendation**

Change the first witness from `claude-max-mcp provider call` to a common `McpChatWitnessAdapter`.

That adapter should prove: local adapter registration, capability listing, proposal creation, approval block, one approved read/observe/proposal-only invocation, transcript artifact, before/after digest, correlation ID, and receipt binding.

Claude Max MCP then becomes one optional provider-delegation plugin behind that adapter, initially limited to smoke or tiny fixture prompts with sandboxed CWD, explicit allowed tools, redacted env descriptor, and "usage unavailable" in the receipt.

Also add Alexander's context shape now: `correlation_id`, `selection_history`, `source_candidates`, `companion_message`, and `context_refs`. Those fields make the witness useful without granting external authority.

**Final Stance**

Build now:

- `McpChatWitnessAdapter` as a local stdio/read-only/proposal-only admission lane.
- Local design-feedback context payload inspired by Yocoolab.
- Capability enumeration plus transcript/artifact/receipt binding.
- Chat panel semantics as propose/review only.

Build as narrow witness:

- Claude Max MCP delegation, but only as a provider adapter after the common witness shape exists.
- Chrome DevTools MCP read-only observe/snapshot against a non-sensitive local page.

Defer:

- Streamable HTTP MCP.
- Claude Code Chrome/live browser session control beyond read-only witnessing.
- Remote Kernel Cloud or multi-user claims.
- Production model-delegation routing.
- Direct GitHub/PR/Pendo/deployment actions.

No-go:

- Browser/webview credential storage.
- MCP/chat/browser self-approval.
- Direct durable-state mutation outside the kernel.
- Direct PR writes or remote hooks bypassing receipts.
- Returning external model output unchanged as local authority.

Final verdict: build the adapter boundary, not the external tools. Claude Max MCP fits, but only as one contained provider behind local authority, and not as the lead proof.

## Explorer: Alexander, Christopher

### Initial Return

Alexander return for `2026-07-10-mcp-chat-extension-integration-research`.

1. **MCP Tool Categories And Setup**

Yocoolab MCP is a Node 20+ stdio MCP server published as `@yocoolab/mcp-server` with `mcp-server` / `yocoolab-mcp` bins, currently package `2.2.1` in `package.json` ([package](https://github.com/Yocoolab/mcp-server/blob/main/package.json)). Setup is `npx -y @yocoolab/mcp-server@2 setup`, which writes MCP config for Claude Code, Cursor, Cline, Roo Code, and Windsurf ([README](https://github.com/Yocoolab/mcp-server/blob/main/README.md); [setup.ts](https://github.com/Yocoolab/mcp-server/blob/main/src/commands/setup.ts)).

Tool groups: Threads, Selection/Bridge, Activity, AI, Deployment, optional Pendo analytics. Env: `YOCOOLAB_API_URL`, `YOCOOLAB_TOKEN`, `GITHUB_TOKEN`, `YOCOOLAB_BRIDGE_PORT`, `YOCOOLAB_BRIDGE_WORKSPACE`, `YOCOOLAB_AGENT_NAME`, `YOCOOLAB_AGENT_TYPE`; source also supports `PENDO_INTEGRATION_KEY` ([index.ts](https://github.com/Yocoolab/mcp-server/blob/main/src/index.ts)).

2. **Chrome Extension / Local Bridge Shape**

The bridge is a local HTTP server on `127.0.0.1:${port}`. It accepts element-selection events, stores recent selections, exposes `/selections/latest`, `/selections`, `/health`, `/agents/register`, `/thread-updates` SSE, companion-message routes, and activity-monitor routes ([http-bridge.ts](https://github.com/Yocoolab/mcp-server/blob/main/src/http-bridge.ts)). Chrome extension context flows into MCP tools via selection payloads: page URL/title/viewport, element selector/tag/text/attrs/bounds, computed styles, framework hints, and correlation id ([types.ts](https://github.com/Yocoolab/mcp-server/blob/main/src/types.ts)). Hooks can poll bridge messages/selections and inject them into Claude Code context ([check-companion.sh](https://github.com/Yocoolab/mcp-server/blob/main/hooks/check-companion.sh), [check-selection.sh](https://github.com/Yocoolab/mcp-server/blob/main/hooks/check-selection.sh)).

3. **Patterns Worth Adapting**

Adapt the product shape, not the authority model:

- Feedback thread as context bundle: selector, screenshot, page/view state, messages, iteration history, PR refs ([get-context.ts](https://github.com/Yocoolab/mcp-server/blob/main/src/tools/get-context.ts)).
- Selection history with correlation ids.
- Source-candidate ranking from selected UI text/id/aria/classes into workspace files ([mapper.ts](https://github.com/Yocoolab/mcp-server/blob/main/src/mapper.ts)).
- Companion message shape: content plus page context, screenshots, one or many elements ([index.ts](https://github.com/Yocoolab/mcp-server/blob/main/src/index.ts)).
- PR action shape only as an envelope proposal: "thread -> files changed -> PR link -> notify participants," not as direct execution ([create-pr.ts](https://github.com/Yocoolab/mcp-server/blob/main/src/tools/create-pr.ts)).

4. **Risks**

Credential custody is the big one: Yocoolab JWT, GitHub PAT with `repo`, `gh auth token` auto-detection, and Pendo keys. The bridge source sets permissive CORS and I did not see bridge-token auth in the local routes, so copy that only with a hardening pass. PR creation writes full file contents to GitHub branches, updates backend thread state, registers preview URL patterns, and notifies participants; that is far beyond `ide-extension` L0 authority. Screenshots, DOM text, selectors, page URLs, analytics, and AI conversations may leave the local machine through Yocoolab/Pendo/GitHub remote services.

5. **Reuse / Adapt / Avoid For `ide-extension`**

Reuse: MCP server packaging as an adapter surface, selection/context tool taxonomy, source-candidate mapper idea, companion messages as user-facing context.

Adapt: Chrome bridge into the existing browser-first design: side panel, background router, content script, and loopback bridge already fit `ide-extension`'s planned L0.5 lane ([browser-first README](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/browser-first-extension-design/README.md:12)). But authority must stay in local Node: manifests, grants, approvals, audit, receipts, provider mediation, envelope state ([ARCHITECTURE](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:37)).

Avoid: direct GitHub PR tools, direct Pendo tracking, remote Yocoolab dependency, unauthenticated bridge endpoints, auto-use of `gh` credentials, hook-based context injection that bypasses approval/receipt, and any claim that the bridge itself is authority.

6. **Smallest `ide-extension` Witness**

Build a local-only "design feedback context" witness:

- Simulated MV3/content-script posts one `ELEMENT_SELECTED`-like payload plus screenshot artifact hash to local kernel.
- Kernel records it as evidence under `.ide-extension/state/`, not canvas authority.
- Workbench shows latest selection, context bundle, and ranked source candidates.
- User prepares "address feedback" envelope; run is blocked before approval.
- Approval creates a dry-run receipt binding `correlation_id`, screenshot/artifact ref, source-candidate refs, and envelope id.
- No Yocoolab, GitHub, Pendo, provider key, PR, push, or external network call.

This directly extends the current L0 proof: local server, workbench, manifests, pending approval, receipt, durable state ([README](/home/vrondelli/projects/domainspec-core/projects/ide-extension/README.md:66), [SPEC](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:100), [smoke test](/home/vrondelli/projects/domainspec-core/projects/ide-extension/tests/l0-smoke.test.mjs:35)).

### Robot-Talk Final Position

**Final Explorer Position**

I accept the siblings' shared constraint: MCP, chat panels, Claude delegation, DevTools, Chrome extension bridges, and Yocoolab-style tools are adapter surfaces only. None should gain approval authority, durable state authority, or receipt-minting authority. That belongs to the loopback Node kernel.

I would revise my Yocoolab recommendation downward in one important way: the "feedback thread -> selection -> screenshot -> source candidates -> PR action" pattern is useful as a product grammar, but `ide-extension` should not copy the PR/action end of it yet. The safe import is the context packet shape, not the workflow automation.

**What I Accept**

Hewitt is right that Claude Max MCP is only a provider-transport peer, comparable to OpenRouter. It belongs behind `prepare -> approval -> run -> receipt`, with constrained cwd/tools/env and a receipt that records delegation metadata.

Wiener is right that MCP is capability exposure, not authority. Stdio is the best first local path; Streamable HTTP can wait until bridge auth/origin hardening exists. Chrome DevTools MCP is a witness/validation lane, not the product runtime.

Ashby is right on the core boundary: chat proposes/reviews; it does not approve, mutate durable state, or mint receipts. MV3 remains the active-local-browser adapter. Playwright/DevTools MCP remain validation witnesses.

**What I Reject**

Do not make Yocoolab-style `create_pr_for_thread` a first-class `ide-extension` capability now. PR creation combines file replacement, GitHub token custody, external account mutation, branch/PR side effects, preview URL assumptions, and participant notification. That is too much surface before the local receipt kernel has a browser/chat witness.

Do not adopt unauthenticated loopback bridge patterns, permissive local CORS, hook-injected companion context, auto-discovered GitHub credentials, or remote analytics as defaults.

Do not treat Claude Code Chrome, DevTools MCP, Kernel Cloud, or Yocoolab as replacements for the local MV3 path. They can witness, compare, or validate.

**Changed Recommendation**

My initial Yocoolab "adapt feedback-thread, selection, screenshot, PR-action, companion-message shapes" becomes:

Build: feedback/context packet, selection history, screenshot/artifact refs, source-candidate ranking, companion-message proposal shape.

Defer: PR action, deployment preview, thread-addressing, remote activity dashboard, AI conversation import, Pendo analytics.

No-go for now: direct GitHub write tools, remote service custody, auto credential pickup, external participant notification, bridge bypass around local approval.

**Final Build / Defer / No-Go Stance**

Build first: `McpChatWitnessAdapter` plus `DesignFeedbackContextAdapter`. One local MCP/chat proposal creates a pending envelope from a Yocoolab-like context packet: selected element, page URL, screenshot artifact hash, source candidates, companion message text. It is blocked before approval. After approval, run one read-only observe or dry-run action and append a local receipt referencing transcript, context digest, before/after digest, approval id, and adapter id.

Build later: `ClaudeDelegationProviderAdapter` as provider transport, with constrained env/cwd/tools and cost/custody metadata.

Defer: Chrome DevTools MCP and Playwright MCP as validation lanes after the proposal-only witness.

Keep planned: MV3 active-local-browser adapter as the real browser bridge.

No-go: any adapter that can approve itself, mutate `.ide-extension/state` directly, mint receipts, push commits/PRs, call remote analytics, or act in a live browser without local approval and receipt binding.

## Explorer: Wiener, Norbert

### Initial Return

**1. MCP Map**

MCP is a protocol for exposing external context and capabilities to AI apps, not a grant of local authority. In an `ide-extension` shape:

- **Host**: the IDE extension/chat runtime. It owns user consent, security policy, lifecycle, model integration, context aggregation, and cross-server isolation. MCP explicitly assigns those coordination duties to the host. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/architecture))
- **Client**: a per-server connector inside the host. One client maintains one stateful session with one server, handles capability negotiation, and routes JSON-RPC messages. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/architecture))
- **Server**: a local process or remote service exposing focused capabilities: **resources**, **tools**, and **prompts**. Servers should not see the whole conversation or other servers; the host enforces that boundary. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/architecture))

Implications:

- **Tools** are model-invocable execution surfaces. They should be treated as adapters, with user-visible exposure and confirmation for risky actions. MCP itself says tool behavior descriptions are not automatically trusted and hosts must obtain explicit consent before invocation. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18))
- **Resources** are URI-addressed context surfaces: files, schemas, app data. They fit read-model/witness roles better than authority roles. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/server/resources))
- **Prompts** are user-controlled templates/workflows, typically surfaced as commands. They are good UX handles, not policy engines. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts))
- Client-side **roots/sampling/elicitation** matter because they put filesystem boundaries, recursive LLM calls, and extra user input under host/client control. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18))

**2. Transport And Authorization**

For `ide-extension`, default to **stdio for local adapters** and treat Streamable HTTP as a stricter remote/network path.

- `stdio`: client launches server as subprocess; JSON-RPC over stdin/stdout; stdout must contain only MCP messages. This is the smallest local adapter shape. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports))
- **Streamable HTTP**: single endpoint, POST/GET, optional SSE. Local HTTP servers must validate `Origin`, bind to localhost when local, and use proper authentication, because otherwise web pages can reach local MCP servers via DNS rebinding-style attacks. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports))
- **Authorization** is optional overall, but for HTTP transports the spec points to OAuth 2.1-style flows. Stdio should retrieve credentials from environment rather than using the HTTP authorization spec. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization))
- Remote/protected MCP requires bearer tokens on every HTTP request, no tokens in query strings, token audience validation, PKCE, HTTPS auth endpoints, and exact redirect handling. ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)) ([modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization))

So: the IDE extension can be a host/control plane, but local authority still comes from repo policy, filesystem scope, user consent, and signed/known server configuration, not from "MCP says this tool exists."

**3. Claude Code Chrome**

Claude Code Chrome is a browser-control adapter, not a general authority layer.

Evidence-supported model:

- It connects Claude Code to Chrome/Edge through the Claude in Chrome extension and visible browser actions; it can use logged-in browser state. ([code.claude.com](https://code.claude.com/docs/en/chrome))
- Login pages and CAPTCHAs pause for manual user handling. ([code.claude.com](https://code.claude.com/docs/en/chrome))
- Site-level browse/click/type permissions come from Chrome extension settings. ([code.claude.com](https://code.claude.com/docs/en/chrome))
- In plan mode, read-only browser calls can run without prompt; state-changing calls prompt for approval. ([code.claude.com](https://code.claude.com/docs/en/chrome))
- Operationally it depends on native messaging host config and can fail on extension detection, idle service workers, dialogs, or WSL/unsupported browsers. ([code.claude.com](https://code.claude.com/docs/en/chrome))

Limit: strong for browser observation/interaction and logged-in UI workflows; weak as an authorization model for local repo truth. It can witness a UI state, but cannot certify source authority.

**4. Chrome DevTools For Agents**

Chrome DevTools for agents is the clearest official precedent for "browser capability exposed through MCP."

- It provides an MCP server, CLI, and agentic skills, letting agents control and inspect live Chrome. ([developer.chrome.com](https://developer.chrome.com/docs/devtools/agents/get-started))
- It exposes browser content to the agent and can read, inspect, debug, and modify browser/DevTools data. Google explicitly warns against exposing sensitive browser sessions to untrusted agents. ([developer.chrome.com](https://developer.chrome.com/docs/devtools/agents/get-started))
- It supports MCP installation for Codex with `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest`. ([developer.chrome.com](https://developer.chrome.com/docs/devtools/agents))
- Tooling includes input, navigation, emulation, performance, network, debugging, screenshot, console, Lighthouse, and trace surfaces. ([github.com](https://github.com/ChromeDevTools/chrome-devtools-mcp))
- Configuration has real safety knobs: isolated profile, URL allow/block patterns, header redaction, slim mode, category enable/disable, usage-statistics and CrUX toggles. ([developer.chrome.com](https://developer.chrome.com/docs/devtools/agents/get-started/configuration))
- Auto-connect deliberately crosses into live browser state: tabs, extensions, cookies, local/session storage, and active app state. It requires remote debugging and a Chrome permission dialog. ([developer.chrome.com](https://developer.chrome.com/docs/devtools/agents/use-cases/auto-connect))

Limit: excellent precedent for a browser witness/adapter. Not precedent for granting local project authority to page-exposed JavaScript or browser state.

**5. Adapter, Witness, No-Go**

- **Adapter**: MCP server wrappers around browser automation, IDE commands, DevTools, local app inspection, and remote services. They expose capability; host keeps consent.
- **Witness**: read-only or bounded evidence surfaces: `resources/list`, `resources/read`, screenshots, DOM snapshots, console/network reads, Lighthouse results, trace summaries, capability manifests, tool-list diffs.
- **No-go**: treating MCP tool descriptions, page-exposed third-party tools, browser logged-in state, or remote server assertions as canonical repo authority. Chrome's third-party tools are explicitly experimental, page-scoped, JS-defined, and non-persistent across origins/reloads. ([developer.chrome.com](https://developer.chrome.com/docs/devtools/agents/use-cases/third-party-tools))

The hard line: browser-agent surfaces may expose runtime truth; they do not promote that runtime truth into source-of-truth governance.

**6. Smallest Official-Surface Witness**

Smallest credible witness for this integration:

1. Configure a stdio MCP server, ideally Chrome DevTools MCP:
   `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest`
2. Ask the host to list capabilities/tools.
3. Run one read-only browser witness against a non-sensitive local page: `list_pages`, `take_snapshot`, `list_console_messages`, or `lighthouse_audit`.
4. Save only the witness output shape in the integration design: server name, transport, declared tools, user approval behavior, observed page URL, timestamp, and bounded result.
5. Do not auto-connect to a personal authenticated browser for the first witness. Use isolated/headless or a fresh profile; auto-connect is a later, explicitly trusted mode.

No files edited.

### Robot-Talk Final Position

**Final Position**

I accept Ashby's local-fit position as the governing architecture: `ide-extension` authority belongs in the loopback Node kernel, durable schemas, approval queue, and receipt ledger. MCP, chat panels, Chrome extension bridges, Claude delegation, and DevTools are admission or witness surfaces only. That is not just a local preference; it follows the MCP split where hosts own consent/security/context aggregation while servers only expose tools/resources/prompts. Sources: [MCP architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture), [MCP tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools).

**What I Accept**

I accept Hewitt's `claude-max-mcp` classification: useful as a narrow provider-transport peer to OpenRouter, not as core authority. It can become a `claude-delegation` adapter only behind `prepare -> approval -> run -> receipt`, with constrained `cwd`, redacted env/HOME descriptor, explicit network grant, allowed-tools limits, and receipt binding.

I accept Alexander's Yocoolab product-shape findings: local Chrome-extension bridge, feedback-thread context bundle, selection history, correlation IDs, source-candidate ranking, and companion messages are good UX/control-plane patterns. The reusable part is the shape, not the remote service.

I accept Ashby's hard boundary: chat panels can propose and review; they cannot approve, mutate durable state, or mint receipts. MV3 can observe/bridge the active browser. Playwright/Chrome DevTools MCP can witness runtime behavior. Kernel Cloud is later.

**What I Reject**

Reject any MCP server as local authority. MCP servers expose capabilities; they do not own policy, approval, durable state, or cross-server truth.

Reject direct Claude CLI delegation as an execution shortcut. Subscription/OAuth custody in Claude Code is tolerable only if the kernel treats it like an external provider call, with grant/receipt/cost controls. Otherwise inherited env, broad tools, and drift are too loose.

Reject remote Yocoolab/GitHub/Pendo/direct PR write paths for this phase. They introduce credential custody and remote mutation before the local authority boundary is proven.

Reject browser-agent state as canonical. Claude Code Chrome and Chrome DevTools can inspect logged-in/live sessions, but official docs explicitly warn that these surfaces expose browser data and can act on behalf of the user. Sources: [Claude Code Chrome](https://code.claude.com/docs/en/chrome), [Chrome DevTools for agents](https://developer.chrome.com/docs/devtools/agents/get-started), [auto-connect](https://developer.chrome.com/docs/devtools/agents/use-cases/auto-connect).

**Change To My Initial Recommendation**

My initial smallest witness was too browser-tool centered. I would now tighten it: Chrome DevTools MCP remains the best official read/observe witness, but the first witness must prove the `ide-extension` authority boundary, not just prove DevTools works.

New smallest witness:

1. `McpChatWitnessAdapter` creates a proposal-only envelope.
2. Kernel blocks it before approval.
3. Approval queue grants exactly one read/observe call.
4. Adapter runs a read-only MCP/browser observation.
5. Kernel mints the receipt, binding `correlation_id`, MCP transcript reference, before/after digest, artifact refs, and redacted environment descriptor.

**Final Stance**

Build: local loopback kernel, schemas, approval queue, receipts, proposal-only chat/MCP adapter, local MV3 bridge shape, correlation IDs, context bundles, read-only witness path.

Defer: Claude delegation provider, remote provider routing, auto-connect to personal authenticated browser, Kernel Cloud, direct GitHub/Pendo/Yocoolab integrations.

No-go: MCP/chat/browser extension approving work, mutating durable state directly, minting receipts, bypassing kernel approval, or treating runtime/browser observations as canonical authority.

## Explorer: Ashby, W. Ross

### Initial Return

**Ashby Readout**

1. **Local Authority Invariants**

`ide-extension` is not "an IDE agent"; it is a local governed workbench binding intent, manifests, external envelopes, approval gates, and receipts into one boundary: [SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:14). L0 authority stays with the loopback Node server, durable `.ide-extension/state`, schemas, approval queue, and server-side provider adapter: [SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:20).

The kernel owns registry, grants, approvals, audit, artifacts, provider mediation, and emergency controls, but not Craft/Whisper/UI Studio/IDE/OpenRouter/runtime authority: [ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:37). Any browser/MCP/chat extension must therefore be an adapter or witness, not a second authority. The browser-first bundle states this explicitly for MV3: extension owns side-panel chrome, active-tab mediation, DOM snapshots, and typed page actions; local Node/kernel owns manifests, grants, approvals, provider mediation, envelopes, audit, and receipts: [ARCHITECTURE-BUNDLE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/browser-first-extension-design/ARCHITECTURE-BUNDLE.md:21).

2. **Integration Boundary Map**

MCP should enter as an invocation transport plus evidence source. It must not expose Kernel, Playwright, CDP, WebDriver, provider, or computer-control credentials directly to approval-capable agents; Kernel research already says MCP is not authority and must be admitted through the local governance kernel: [findings.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/findings.md:25).

Chat extensions should enter as proposal/review surfaces. VS Code chat/LM tooling is approved only as generic agent UI/tool plumbing, not browser page control: [findings.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/vscode-browser-control-api-research/findings.md:52). A chat panel can draft an envelope, show state, or request approval; it cannot approve itself, mutate durable state, or mint receipts.

Browser-control adapters split into three lanes: MV3 local active-browser adapter, Playwright/MCP validation adapter, and Kernel Cloud remote witness adapter. The existing recommendation remains: Playwright MCP/direct Playwright proves real browser acts outside VS Code; VS Code/VSCodium wrapper is chrome only: [findings.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/vscode-browser-control-api-research/findings.md:155).

3. **Replace / Complement / No-Go Zones**

Replace: replace any baseline claim that VS Code/VSCodium exposes stable third-party integrated-browser DOM control. Prior findings reject stable page/session handles for read/click/type/screenshot/CDP: [findings.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/vscode-browser-control-api-research/findings.md:9).

Complement: MCP can complement as a tool/witness adapter. Chat extensions can complement as UI/proposal surfaces. Kernel Cloud can complement as an isolated remote Chromium witness only after the blocking local approval/receipt proof: [findings.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/findings.md:46).

No-go: direct model access to MCP/Kernel credentials, raw remote execution bypass, arbitrary DOM JS, remote-issued receipts, self-approval, direct Craft/Whisper/repo mutation, and credential/wallet/payment/public-submit/destructive browser automation. The local spec already forbids effectful browser/shell/fs/network/export/commit/push/publication without approval and receipt: [SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:30).

4. **Credential Custody / Receipts**

Provider keys stay server-side; browser code must not hold them: [SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:27), [ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:67). OpenRouter's manifest forbids browser/webview key storage and self-approval: [openrouter.manifest.json](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/modules/openrouter.manifest.json:24).

MCP/chat adapters should hold only narrow, revocable bridge/session tokens. ResonantOS is the useful witness pattern: loopback bridge, per-run bridge token, generated ignored config: [README.md](/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/README.md:18). External IDs, screenshots, replay URLs, MCP call traces, and Kernel session IDs are `evidence_refs`, not receipts. The receipt schema is currently closed and requires only canonical local fields: [receipt.schema.json](/home/vrondelli/projects/domainspec-core/projects/ide-extension/schemas/receipt.schema.json:5). Extra binding digests either need evidence artifacts referenced by the receipt or a deliberate schema evolution.

5. **Smallest Local Witness**

Smallest honest witness: `McpChatWitnessAdapter`, proposal-only plus one read/observe call.

Flow: chat extension/MCP tool calls existing `/api/envelopes/prepare`; kernel creates pending approval; `/api/envelopes/run` blocks before approval; human approves through `/api/approvals/:id/approve`; adapter performs one `observe` only after approval; kernel appends one local receipt with `evidence_refs` to the MCP transcript and before/after digest. Current server already proves prepare/block/approve/receipt for dry-run: [server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:127), and the smoke test proves that loop: [l0-smoke.test.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/tests/l0-smoke.test.mjs:35).

Do not make the first witness click/type/navigate. If an effect is needed, use Kernel's stricter `observe` + typed `scroll` witness shape and require no remote call on rejection: [findings.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/findings.md:52).

6. **Change To Kernel / MV3 Recommendation**

No major change. MCP/chat-extension integration strengthens the prior recommendation: MV3 remains the active-local-browser adapter; Playwright MCP remains validation/browser-act witness; Kernel Cloud remains candidate remote witness; VS Code/VSCodium remains optional chrome. The new addition is naming MCP/chat as adapter admission surfaces, never authority surfaces.

Read-only closeout: no files edited, no tests run. Status: no blocker, but the next proof must bind MCP/chat tool invocation to local approval and local receipt before claiming integration.

### Robot-Talk Final Position

**Final Position**

I accept the sibling convergence: MCP and chat extensions are not a new control plane for `ide-extension`; they are adapter admission surfaces. The local Node kernel remains the authority for manifests, grants, approvals, audit, artifacts, provider mediation, and receipts, while external systems provide proposals, transport, or evidence only ([ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md:37), [SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md:14)).

What I accept:

- From **Hewitt**: `claude-max-mcp` is useful only as a provider-delegation adapter, peer to OpenRouter, never as an agent authority. OAuth custody staying in Claude Code is acceptable only if the local receipt records custody and the run is constrained.
- From **Alexander**: Yocoolab's good material is product shape, not infrastructure dependency: feedback threads, selection context, correlation IDs, source ranking, and companion messages are worth adapting locally.
- From **Wiener**: MCP is capability exposure, not authority. Stdio should be the default local adapter transport. Streamable HTTP is deferred until localhost/origin/auth hardening is explicit.

What I reject:

- `network.call` alone is not enough for `claude-max-mcp`. It spawns a local CLI and inherits process context, so the grant model must treat it as provider delegation plus process/cwd/env exposure, not just a remote API call.
- A Chrome DevTools MCP smoke test alone does not prove integration. It proves tool availability. It becomes an `ide-extension` witness only when routed through prepare -> approval -> run -> local receipt.
- Remote Yocoolab/GitHub/Pendo/Deployment hooks are no-go for this slice. Direct PR writes, permissive bridge CORS, JWT/PAT custody, and remote leakage conflict with the local approval/receipt boundary ([README.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/README.md:54)).
- Any chat extension that can approve its own tool call, mutate durable state, or issue receipts is a category error.

Change to my initial recommendation:

The first integration should not be "MCP support" broadly. It should be an **adapter admission harness**: adapter descriptor, transport kind, tool allowlist, credential-custody statement, redacted env/HOME/CWD descriptor, requested grants, approval id, evidence refs, and local receipt. Then individual adapters plug into that harness.

Final stance for `ide-extension`:

**Build now:** one local MCP/chat witness harness, stdio-first, proposal-only by default. The smallest good witness is a read-only local-page observe against `/demo/l0` using an MCP browser witness or a local design-feedback context payload. It must prove blocked-before-approval using the existing envelope path ([server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:127)), then append a local receipt after approval ([server.mjs](/home/vrondelli/projects/domainspec-core/projects/ide-extension/src/server.mjs:170)).

**Defer:** actual `claude-max-mcp` delegation, Chrome DevTools MCP beyond read-only observe, Streamable HTTP MCP, Kernel Cloud, remote Yocoolab, GitHub/Pendo deployment hooks, streaming, persistence, and cost accounting. These need the admission harness first.

**No-go:** direct MCP tool bypass, raw Claude/Kernel/DevTools credentials exposed to agents, broad Claude Code tool access, inherited unconstrained HOME/CWD, live sensitive browser sessions, credential/wallet/payment/public-submit/destructive automation, remote-issued receipts, and any claim that VS Code/VSCodium gives stable third-party integrated-browser control. The prior MV3/Kernel recommendation stands: MV3 remains the active-local-browser adapter, Playwright/DevTools MCP are witness lanes, Kernel Cloud is candidate-only, and IDE/chat surfaces are chrome plus proposal UI, not authority.
