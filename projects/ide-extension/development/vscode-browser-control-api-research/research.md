# VS Code Browser Control API Research - Explorer Transcript

Dispatch: `2026-07-09-vscode-browser-control-api-research`

## Agent 1 - Turing, Alan

**Turing/Alan Read-Only Finding**

Verdict for `ide-extension`: **partial, leaning no**.

A third-party VS Code/VSCodium extension can officially create and control **its own webview**, open URLs, forward localhost/remote URLs, and use command plumbing. It cannot, in the stable public extension API, obtain a browser/page handle for the integrated browser or Simple Browser that supports DOM reads, clicks, navigation observation, screenshots, console capture, or Playwright-style control like VS Code's own chat browser tools.

1. **What extensions can officially do**

- Own a webview: `vscode.window.createWebviewPanel`, webview views, and custom editors let an extension render HTML inside VS Code. The Webview API describes webviews as iframe-like surfaces controlled by the creating extension, with message passing to/from the extension host. See Webview API docs: <https://code.visualstudio.com/api/extension-guides/webview> and API reference for `Webview`, `WebviewPanel`, `WebviewView`.
- Message owned webviews: extension to webview via `webview.postMessage(message)`, webview to extension via `acquireVsCodeApi().postMessage(...)`, received by `webview.onDidReceiveMessage`.
- Observe owned panel lifecycle/view state: `WebviewPanel.onDidDispose`, `onDidChangeViewState`, `visible`, `active`, `reveal`, `dispose`. Important boundary: webview panels are owned by the creating extension; if the extension loses the reference, it cannot regain access.
- Open URLs externally: `vscode.env.openExternal(uri)` opens the default registered app/browser and handles localhost forwarding in remote cases; `vscode.env.asExternalUri(uri)` resolves a URI usable from the client/web side, often for localhost forwarding or webview iframe embedding.
- Execute commands: `vscode.commands.executeCommand(command, ...args)` can invoke built-in or contributed commands, but it returns only the command's result, not a browser automation object.
- Handle auth/browser callbacks: `vscode.window.registerUriHandler` can receive extension-scoped callback URIs, useful for OAuth/browser sign-in flows, but not browser control.
- Store tokens/state: `ExtensionContext.secrets` / `SecretStorage` can persist sensitive auth material, but again this is not browser automation.

2. **What extensions cannot officially do**

No stable public API in `vscode.d.ts` exposes an `IntegratedBrowser`, `BrowserPage`, DOM snapshot, click, type, screenshot, console-log stream, navigation event, or Playwright/CDP session for the integrated browser/Simple Browser. The public API reference is explicitly the extension-author API compiled from `vscode.d.ts`; browser automation objects are not part of that surface.

For webviews, control stops at the extension-owned document and message channel. Webviews are sandboxed, communication is message passing, and DOM-specific objects cannot be posted back to the extension host. If the webview embeds a remote page in an iframe, normal browser same-origin/frame restrictions apply; the VS Code extension API does not bless cross-origin DOM inspection or clicking.

For Simple Browser / Integrated Browser, source-adjacent evidence shows open commands exist. The built-in Simple Browser registers `simpleBrowser.show` / `simpleBrowser.api.open`, and current source routes to `workbench.action.browser.open` when the integrated browser command exists. But that is only an opener path, not a returned page handle or automation API.

VS Code's own chat/browser-tools path is different. Official docs say agents can use built-in browser tools to open/navigate/read/screenshot/click/type/hover/drag/run Playwright code, gated by `workbench.browser.enableChatTools`. Those tool names include `openBrowserPage`, `navigatePage`, `readPage`, `screenshotPage`, `clickElement`, `typeInPage`, and `runPlaywrightCode`. That is an agent/chat product surface, not a stable third-party extension API.

3. **Integrated browser/debug nuance**

The integrated browser can be opened by command palette, localhost links, agents, or `editor-browser` debug configurations. The `editor-browser` debug type can launch/attach for standard debugging, but the docs frame that as debug configuration behavior, not a general extension SDK for DOM automation.

4. **Recommended witness**

Build a tiny witness extension with three commands:

- `witness.webview`: creates a `WebviewPanel`, enables scripts, proves `postMessage` both ways, logs `onDidChangeViewState` / `onDidDispose`.
- `witness.open`: calls `vscode.env.openExternal`, `vscode.env.asExternalUri`, and optionally `vscode.commands.executeCommand('simpleBrowser.api.open', uri)` / `'workbench.action.browser.open'`.
- `witness.noBrowserHandle`: records that opener commands return no stable page object and that `vscode` exports no DOM/click/screenshot/navigation API for integrated browser pages.

That witness cleanly supports: **yes** for self-owned webview control; **partial** for opening/embedding URLs; **no** for official third-party control of VS Code's integrated browser like chat's browser tools.

## Agent 2 - Shannon, Claude

**Verdict**

VS Code now has real built-in browser tools for agents, but I would not describe them as a first-class public "integrated browser control API" for extensions. The stable public surface is generic AI/tool plumbing. The browser behavior itself is product-owned, with one useful but undocumented/internal command witness: `workbench.action.browser.open`.

1. Built-in chat/browser tools can open/navigate browser pages, read page content and console errors, screenshot pages, select/click/hover/drag/type, handle dialogs, and run Playwright code. VS Code also has sharing controls: user-opened tabs must be explicitly shared; agent-opened tabs use isolated ephemeral sessions. The documented tool names include `openBrowserPage`, `navigatePage`, `readPage`, `screenshotPage`, `clickElement`, `hoverElement`, `dragElement`, `typeInPage`, `handleDialog`, and `runPlaywrightCode`. (<https://code.visualstudio.com/docs/agents/guides/browser-agent-testing-guide>)

2. Third-party extensions do have public APIs to build chat participants, language-model tools, and language-model requests: `vscode.chat.createChatParticipant`, `contributes.languageModelTools`, `vscode.lm.registerTool`, `vscode.lm.selectChatModels`, etc. The docs explicitly distinguish extension tools from built-in tools and MCP tools. (<https://code.visualstudio.com/api/extension-guides/ai/tools>)

3. What is not clearly public: there is no documented `vscode.browser.*` API that returns an integrated-browser tab/session/page handle or lets an extension directly drive DOM clicks, screenshots, console capture, shared-tab access, or Playwright execution as a stable browser API. Proposed APIs are explicitly unstable/Insiders-only and not for Marketplace extensions; I saw chat/tool-adjacent proposals, not a browser-control proposal.

4. Commands/surfaces:
`workbench.action.browser.open` appears in VS Code source as the integrated-browser command. `simpleBrowser.show` and `simpleBrowser.api.open` delegate to it when present, and `debug-server-ready` also uses it for `openIntegratedBrowser`. This is a strong witness that "open URL in integrated browser" exists, but it is not listed as a documented stable built-in command API. (<https://code.visualstudio.com/api/references/commands>)

For `ide-extension`: use `workbench.action.browser.open` only as a pragmatic, version-gated witness for opening a URL. Do not build core behavior on controlling VS Code's built-in browser tools unless a runtime witness proves the browser tools appear in `vscode.lm.tools` with usable schemas in the target VS Code build. Recommended witness: a tiny extension command that logs `vscode.lm.tools.map(t => [t.name, t.inputSchema])`, checks for the ten browser tool names, then attempts a guarded `vscode.lm.invokeTool('openBrowserPage', ...)` with `request.toolInvocationToken` from a chat participant. If that fails or schemas are absent, classify browser automation as product-only and use your own Playwright/MCP path.

## Agent 3 - Hewitt, Carl

**Hewitt/Carl Report**

Core distinction: there is no single "VS Code browser control API." There are several control planes, and only two are true browser-act routes.

| Route | Feasible for ide-extension? | DOM/click/navigation? | Boundary |
|---|---:|---:|---|
| Playwright MCP / external Playwright | Yes, as an external agent/tooling route | Yes: click, navigate, inspect, screenshots, network | Outside VS Code extension API; controls a Playwright browser context or attached browser |
| VS Code extension-host tests | Yes | No browser DOM by itself | Full VS Code API inside Extension Development Host |
| Webview messaging | Yes | Only inside the extension-owned webview | Explicit JSON message bridge; webview sandbox/CSP |
| Integrated browser open/command | Partly | Opens/navigates, but not DOM-control API | VS Code workbench browser surface |
| VS Code browser agent tools | Yes for agent surfaces, not plain extension API | Yes: click/type/read/screenshot/run Playwright | Tool enablement, per-session isolation, sharing gates |

**Feasible Routes**

1. **External browser control: Playwright MCP.**
   This is the cleanest "automation/protocol corpus" route. Playwright MCP exposes browser automation through MCP, using accessibility snapshots and tools like `browser_click` and `browser_navigate` for real page interaction. It can run persistent profiles, isolated sessions, CDP attachment, or connect to existing tabs through the Playwright extension. It is explicitly not a security boundary, so host/network/profile controls matter. (<https://github.com/microsoft/playwright-mcp>)

2. **Extension-host automation: `@vscode/test-electron` / `@vscode/test-web`.**
   This proves extension behavior, activation, commands, VS Code API calls, webview setup, and test-controller publication. VS Code's extension tests run in an Extension Development Host with full VS Code API access; CLI wiring is `--extensionDevelopmentPath` plus `--extensionTestsPath`, or `runTests(...)`. Web extensions run via a `browser` entry point in a WebWorker-like host, and `@vscode/test-web` opens VS Code for the Web with the extension loaded. This route does not grant arbitrary DOM control of a website. (<https://code.visualstudio.com/api/working-with-extensions/testing-extension>, <https://code.visualstudio.com/api/extension-guides/web-extensions>)

3. **Webview messaging.**
   This is not browser automation. It is extension-owned UI automation. A webview can run scripts only when `enableScripts: true`; the extension can send JSON via `webview.postMessage`, and webview script can call `acquireVsCodeApi().postMessage(...)` back. The webview script can mutate its own DOM, but the extension host does not gain a general DOM handle. Security rests on least capability, `localResourceRoots`, CSP, sanitization, and keeping the VS Code API object private. (<https://code.visualstudio.com/api/extension-guides/webview>)

4. **Integrated browser opening.**
   The documented integrated browser can open pages, navigate URLs, keep history/session storage, debug with `editor-browser`, and expose manual DevTools. It can be opened by the Browser command, localhost links, debug sessions, or agents. Source also shows `serverReadyAction.action: "openIntegratedBrowser"` dispatching `workbench.action.browser.open`, while `openExternally` uses `vscode.env.openExternal`. That proves opening/routing, not DOM automation. (<https://code.visualstudio.com/docs/debugtest/integrated-browser>, <https://github.com/microsoft/vscode/blob/main/extensions/debug-server-ready/src/extension.ts>, <https://code.visualstudio.com/api/references/vscode-api>)

5. **DOM/browser-act route inside VS Code: browser agent tools.**
   This is the native VS Code agent path. When browser tools are enabled, agents get `openBrowserPage`, `navigatePage`, `readPage`, `screenshotPage`, `clickElement`, `hoverElement`, `dragElement`, `typeInPage`, `handleDialog`, and `runPlaywrightCode`. Agent-opened pages use private in-memory sessions; user-opened pages require explicit Share with Agent, and enterprise policy can disable tools or restrict domains. (<https://code.visualstudio.com/docs/agents/guides/browser-agent-testing-guide>, <https://code.visualstudio.com/docs/debugtest/integrated-browser>)

**Smallest Witnesses**

Playwright MCP: launch isolated MCP, navigate to a localhost page, click a button, assert changed text.

Extension-host: run `@vscode/test-electron` and assert `vscode.commands.executeCommand("myExtension.command")` changes extension state.

Webview: create a webview with one button; extension posts `{command:"setText"}`; webview mutates `<h1>` and posts back `{ok:true}`.

Integrated browser opening: debug config with `serverReadyAction: { action: "openIntegratedBrowser", uriFormat: "http://localhost:%s" }`; observe tab opens.

Browser-act native VS Code: enable Browser tools, ask agent to open localhost test page, click `#increment`, read page text. This is the only integrated-browser route that proves DOM/click/navigation control.

## Agent 4 - Wiener, Norbert

Read-only research return for `2026-07-09-vscode-browser-control-api-research`.

1. **VSCodium-Safe Path For `ide-extension`**

Build the extension against stable VS Code extension APIs, distribute through Open VSX, a signed `.vsix`, or a private/self-hosted gallery. VSCodium's default extension gallery is Open VSX, and its docs explicitly point users away from Microsoft Marketplace dependence for non-Microsoft products. (<https://github.com/VSCodium/vscodium/blob/master/docs/extensions.md>)

For "browser-like" surfaces, the safe core is:

- `vscode.window.createWebviewPanel` or `registerWebviewViewProvider` for an owned in-editor surface. (<https://code.visualstudio.com/api/references/vscode-api>)
- `vscode.env.openExternal` for real external-browser handoff. (<https://code.visualstudio.com/api/references/vscode-api>)
- Message-passing between extension host and webview for control, not DOM access to VS Code itself. (<https://code.visualstudio.com/api/extension-guides/webview>)

Treat VS Code's integrated browser as a runtime feature to witness, not as the portable contract. The VS Code docs say `editor-browser` debugging works where **Visual Studio Code Desktop** is supported; that is not the same as "stable extension API available in VSCodium." (<https://code.visualstudio.com/docs/debugtest/integrated-browser>)

2. **Marketplace / Copilot / Microsoft Service Constraints**

Microsoft Marketplace is not a VSCodium-safe dependency. VSCodium says Microsoft prohibits Marketplace use by other products or `.vsix` redistribution from it, and quotes Marketplace use as limited to Visual Studio products/services. (<https://github.com/VSCodium/vscodium/blob/master/docs/extensions.md>) VSCodium also warns some Microsoft/proprietary debuggers and extensions only function with the official VS Code build, and some are hard-coded to that product. (<https://github.com/VSCodium/vscodium/blob/master/docs/extensions.md>)

Copilot is not a safe baseline. VSCodium's own Copilot note says Copilot features are disabled and not configured by default, requiring settings and `product.json` additions such as `trustedExtensionAuthAccess` and `defaultChatAgent`. (<https://github.com/VSCodium/vscodium/blob/master/docs/ext-github-copilot.md>) So anything relying on Copilot Chat, AI browser tools, or Microsoft/GitHub auth services should be classified "optional/product-service dependent," not part of the VSCodium-safe path.

Also: VSCodium removes or redirects several Microsoft online-service paths, but extensions may still send telemetry on their own. (<https://github.com/VSCodium/vscodium/blob/master/docs/telemetry.md>)

3. **Webview Security / CSP Implications**

Webviews survive well in VSCodium because they are part of the standard extension API surface, but they are not a free-form embedded browser. VS Code says webviews are resource-heavy and should be used sparingly. (<https://code.visualstudio.com/api/extension-guides/webview>) They run in isolated contexts and cannot directly read local resources; local files must be exposed through `asWebviewUri`, with `localResourceRoots` narrowed as much as possible. (<https://code.visualstudio.com/api/extension-guides/webview>)

Security posture should be strict: scripts off unless needed; if enabled, no inline scripts, strict CSP, `default-src 'none'`, only explicit `script-src/style-src/img-src`, sanitize all workspace-derived data, validate every webview message. (<https://code.visualstudio.com/api/extension-guides/webview>)

Do not attempt to control VS Code's own DOM or integrated browser UI from an extension. VS Code explicitly blocks extension access to the workbench DOM for stability and compatibility. (<https://code.visualstudio.com/api/extension-capabilities/overview>)

4. **Blocked / Deferred Paths And Recommended Witness**

Blocked as baseline:

- Direct Microsoft Marketplace install path or Marketplace `.vsix` redistribution.
- Microsoft-only extensions, proprietary debug adapters, Remote Development assumptions.
- Copilot/Chat/browser-agent tools as required dependencies.
- Proposed APIs or product-patched API proposals for a published/general extension. VS Code marks proposed APIs unstable, Insiders-only, and not for published extensions. (<https://code.visualstudio.com/api/advanced-topics/using-proposed-api>)
- Browser automation from a web extension: web extensions run in a browser sandbox, lack Node APIs, and cannot spawn child processes or executables. (<https://code.visualstudio.com/api/extension-guides/web-extensions>)

Deferred pending witness:

- `editor-browser` launch/attach in VSCodium.
- Any `workbench.browser.*` command invocation from an extension.
- Built-in browser tools for agents, because those are documented in the VS Code integrated browser/AI-chat path and require user sharing/organization settings. (<https://code.visualstudio.com/docs/debugtest/integrated-browser>)

Recommended witness: a VSCodium desktop smoke-test matrix. Install a minimal Open VSX/VSIX extension that exercises `createWebviewPanel`, `registerWebviewViewProvider`, `openExternal`, command enumeration, and an attempted `editor-browser` debug launch. Capture: VSCodium version, command availability, network endpoints, whether Microsoft auth/service prompts appear, and whether the same behavior differs in official VS Code. This keeps claim <= proof.

