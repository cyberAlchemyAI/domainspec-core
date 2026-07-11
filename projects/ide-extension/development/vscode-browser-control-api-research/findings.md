# VS Code Browser Control API Findings

Dispatch: `2026-07-09-vscode-browser-control-api-research`
Status: `resolved`
Question: Can `ide-extension` control the VS Code/VSCodium browser through a public API/SDK like VS Code's own chat/browser tools?

## Short Answer

No, not if `control` means obtaining a stable page/session handle or performing
DOM/page actions against VS Code's Integrated Browser or Simple Browser.

A third-party VS Code/VSCodium extension has stable public APIs for owned
webviews, URL handoff/opening, URI conversion, command invocation, extension
tests, and generic chat/Language Model tooling. It does not have a stable public
extension SDK that returns an integrated-browser page object with read, click,
type, screenshot, console, navigation-event, Playwright, or CDP capability.

Treat real browser automation as one of two things:

- external Playwright/Playwright MCP automation; or
- VS Code product/agent tooling that is runtime-gated and not a portable
  VSCodium-safe extension contract.

## Definitions

- `extension-owned webview`: an iframe-like VS Code surface created by the
  extension with a JSON message bridge. The extension can message the webview;
  webview JS can mutate its own DOM. This is not arbitrary browser automation.
- `VS Code Integrated Browser`: VS Code workbench/product browser surface.
  Opening it is not controlling it.
- `Simple Browser`: built-in browser/webview extension surface with source-witnessed
  open commands. It is not a returned page/session API.
- `browser control`: must name an operation. `open/route URL`, `message owned
  webview`, `observe lifecycle`, `read page`, `act on DOM`, and `protocol
  automation` are different capabilities.
- `API`: stable documented extension API unless explicitly labeled as
  source-adjacent command, proposed API, product feature, or runtime observation.
- `SDK`: portable third-party extension contract. A command that happens to work
  in one VS Code build is not an SDK.
- `chat browser control`: VS Code product/browser-agent capability gated by the
  agent runtime, settings, sharing, tokens, and policy.

## Verdict Matrix

| Candidate route | Owner / classification | Witnessed? | Browser-act control? | Verdict |
| --- | --- | --- | --- | --- |
| Extension-owned webview | Official stable API; build-from-owned | Docs and required smoke witness | Only inside owned webview DOM via webview JS/message bridge | APPROVE for L0/L1 host surface |
| `openExternal` / `asExternalUri` / `registerUriHandler` | Official stable API | Docs; smoke witness required | No; handoff/callback only | APPROVE as URL handoff |
| `simpleBrowser.api.open` / `workbench.action.browser.open` | Source-witnessed, undocumented/product command opener | Needs command-enumeration smoke | No page handle; opener only | DEFER as optional version-gated opener |
| `editor-browser` debug | Product/debug feature | Needs VS Code and VSCodium smoke | Debug launch/attach only | DEFER; not automation substrate |
| VS Code browser-agent tools | VS Code product/agent surface | Docs; extension invocation unproven | Yes only inside enabled VS Code browser-agent runtime, not stable third-party SDK | PRODUCT-ONLY unless runtime-proven |
| Language Model tools / chat participants | Official stable generic tool plumbing | Docs | No browser page API | APPROVE for agent UI/tool integration, not browser control |
| Playwright MCP / external Playwright | External automation plane | Docs and required smoke witness | Yes | APPROVE as browser-act adapter |
| VSCodium-safe path | Stable VS Code API subset + Open VSX/VSIX | Needs VSCodium matrix | Owned webview/external handoff only | APPROVE baseline |
| Direct workbench DOM or integrated-browser UI control | Blocked by owner | No | Would be control, but not exposed | KILL |
| Proposed/product-patched APIs | Proposed/internal | No stable published witness | Unknown | KILL as baseline; experiment only |

## Evidence Basis

Agent 1 found that stable public APIs support `createWebviewPanel`, webview
views, webview message passing, `openExternal`, `asExternalUri`, command
execution, URI handlers, and secret storage, but no stable `IntegratedBrowser`,
`BrowserPage`, DOM snapshot, click, type, screenshot, console stream,
navigation-event, Playwright, or CDP session API. See [research.md](research.md:11).

Agent 2 found that VS Code docs say enabled browser-agent tools can open,
navigate, read, screenshot, click, type, handle dialogs, and run Playwright code,
but classified this as product-owned browser behavior, not a first-class public
integrated browser control API for extensions. See [research.md](research.md:51).

Agent 3 separated the control planes: Playwright MCP/external Playwright is real
browser automation; extension-host tests prove extension behavior; webview
messaging controls only the owned webview; integrated browser commands open
surfaces but do not provide DOM control; browser-agent tools are native VS Code
agent tooling. See [research.md](research.md:68).

Agent 4 found the VSCodium-safe baseline: stable extension APIs, Open VSX/VSIX
distribution, owned webviews, and external URL handoff. Microsoft Marketplace,
Copilot/browser-agent tools, proprietary debugger assumptions, proposed APIs,
and product-specific browser tools are not safe as baseline dependencies. See
[research.md](research.md:111).

Official/source-adjacent sources used by the explorers include:

- VS Code Webview API: <https://code.visualstudio.com/api/extension-guides/webview>
- VS Code API reference: <https://code.visualstudio.com/api/references/vscode-api>
- VS Code Commands guide: <https://code.visualstudio.com/api/extension-guides/command>
- VS Code Integrated Browser docs: <https://code.visualstudio.com/docs/debugtest/integrated-browser>
- VS Code browser-agent tools guide: <https://code.visualstudio.com/docs/agents/guides/browser-agent-testing-guide>
- VS Code Language Model Tool API: <https://code.visualstudio.com/api/extension-guides/ai/tools>
- Playwright MCP: <https://github.com/microsoft/playwright-mcp>
- Simple Browser source: <https://github.com/microsoft/vscode/blob/main/extensions/simple-browser/src/extension.ts>
- debug-server-ready integrated browser opener source: <https://github.com/microsoft/vscode/blob/main/extensions/debug-server-ready/src/extension.ts>
- VSCodium extension docs: <https://github.com/VSCodium/vscodium/blob/master/docs/extensions.md>

## Implementation Recommendation

### L0

Keep the current local-server workbench as the proof substrate. Add an optional
VS Code/VSCodium wrapper only as chrome:

- open the local workbench URL externally via `vscode.env.openExternal`;
- optionally expose the workbench inside an extension-owned webview;
- use `asExternalUri` for remote/forwarded localhost cases;
- keep all provider keys and effectful actions in the local backend or extension
  host, never in browser/webview code;
- record every action as an envelope and receipt as the current L0 already does.

Do not claim integrated-browser control in L0.

### L1

Add two adapter lanes:

1. **Portable host lane:** owned webview + message bridge + extension-host tests.
   This proves IDE chrome and extension behavior.
2. **Automation lane:** Playwright MCP or direct Playwright against an external or
   adjacent browser. This proves actual browser acts: read, click, type,
   screenshot, console, navigation.

Add an optional, version-gated **integrated-browser opener lane**:

- enumerate commands with `vscode.commands.getCommands(true)`;
- if present, try `simpleBrowser.api.open` or `workbench.action.browser.open`;
- record that it opened a URL;
- record that no page/session handle was returned.

Keep this lane out of the core contract.

### Product-Only Experiment

For official VS Code only, not VSCodium baseline:

- enable browser tools;
- ask a VS Code agent to open a localhost page;
- click an element and read changed text;
- separately test whether a third-party chat participant/LM tool can see or
  invoke browser tools in the target build.

If the runtime witness fails, browser-agent automation remains product-only.

## Required Witness Queue

| Witness | Command / shape | Claim unlocked |
| --- | --- | --- |
| Webview smoke | extension command creates a webview, sends `webview.postMessage`, receives `acquireVsCodeApi().postMessage`, logs view/dispose events | Extension-owned webview control |
| URL handoff smoke | command runs `openExternal`, `asExternalUri`, and `registerUriHandler` callback flow | External handoff / URI forwarding |
| Integrated opener smoke | command enumeration plus `executeCommand('simpleBrowser.api.open' or 'workbench.action.browser.open')`; record no page handle | Optional opener only |
| Extension test smoke | `@vscode/test-electron` invokes extension commands and asserts state | Extension behavior proof |
| Playwright MCP smoke | navigate to localhost, click a button, assert text/screenshot/snapshot | Real browser automation outside VS Code API |
| VSCodium matrix | install VSIX/Open VSX build and run the above stable-API smoke tests | VSCodium-safe baseline |
| VS Code browser-agent experiment | product agent opens/clicks/reads page; extension separately probes LM tool visibility | Product-only browser tools status |

## Consequence For `ide-extension`

The correct architecture remains:

```text
VS Code/VSCodium wrapper          optional chrome
extension-owned webview           owned IDE UI surface
local Node workbench              governance kernel + durable state
Playwright MCP / external browser browser-act adapter
VS Code browser-agent tools       optional product-only experiment
```

So the project should not try to become "VS Code chat controls browser through
an SDK." It should become a governed workbench that can be opened from the IDE,
can host its own webview surface, and can route real browser automation through
an explicit Playwright/MCP adapter with approval and receipts.
