# Kernel Integration Research

Dispatch: `2026-07-10-kernel-integration-research`
Project: `ide-extension`
Status: evidence substrate
Question: Can Kernel and `kernel-images` cut development time for `ide-extension`, especially for the browser-control lane, without moving authority away from the local HTML workbench and Node kernel?

## Dispatch Frame

`ide-extension` is currently shaped around a local HTML workbench and local Node kernel. The kernel owns approvals, grants, provider mediation, append-only audit, and receipts. The Chrome MV3 lane is designed as a browser adapter: it can observe and perform narrow typed browser actions, but it does not own authority.

This research checked whether Kernel can reduce implementation work by supplying browser runtime, browser automation, live view/replay, extension hosting, MCP, or a self-hosted browser image.

## Source Corpus

- Kernel docs: <https://www.kernel.sh/docs>
- Kernel docs index for LLMs: <https://www.kernel.sh/docs/llms.txt>
- Kernel create docs: <https://www.kernel.sh/docs/introduction/create>
- Kernel control docs: <https://www.kernel.sh/docs/introduction/control>
- Kernel observe docs: <https://www.kernel.sh/docs/introduction/observe>
- Kernel scale docs: <https://www.kernel.sh/docs/introduction/scale>
- Kernel MCP docs: <https://www.kernel.sh/docs/reference/mcp-server>
- Kernel extension upload API: <https://www.kernel.sh/docs/api-reference/extensions/upload-a-browser-extension>
- Kernel ad-hoc extension load API: <https://www.kernel.sh/docs/api-reference/browsers/ad-hoc-upload-one-or-more-unpacked-extensions-to-a-running-browser-instance>
- Kernel Playwright execution API: <https://www.kernel.sh/docs/api-reference/browser-playwright/execute-playwrighttypescript-code-against-the-browser>
- Kernel computer batch API: <https://www.kernel.sh/docs/api-reference/browser-computer-controls/execute-a-batch-of-computer-actions-sequentially>
- `kernel-images` repository: <https://github.com/kernel/kernel-images>
- `kernel-images` reviewed commit: <https://github.com/kernel/kernel-images/tree/ae64afa4a46ff196e50488057ebb7b4168f9691d>
- `ide-extension` specification: [SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md)
- `ide-extension` architecture: [ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md)
- Browser-first architecture bundle: [ARCHITECTURE-BUNDLE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/browser-first-extension-design/ARCHITECTURE-BUNDLE.md)
- VS Code browser-control API research: [findings.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/vscode-browser-control-api-research/findings.md)
- ResonantOS browser-first precedent: [browser-first README](/home/vrondelli/projects/workspace-resonant/2.0.0-alpha/browser-first/README.md)

## Explorer Returns

### Managed Kernel Platform - Abramsky

#### Capability Map

- Kernel can provision sandboxed cloud Chromium and return `session_id`, `cdp_ws_url`, `webdriver_ws_url`, and `browser_live_view_url`. This can replace maintaining a local automation Chromium/Playwright harness for cloud test runs. It cannot observe or control the user's already-open Chrome tab. Source: <https://www.kernel.sh/docs/introduction/create>
- Kernel complements the MV3 lane. Upload the unpacked MV3 extension once, then create a Kernel browser with `extensions: [{ name }]`. This enables repeatable cloud execution of the same extension against target pages. Loading an extension restarts Chromium and may disrupt CDP connections, so build/run cycles need session recreation or a prepared pool. Source: <https://www.kernel.sh/docs/browsers/extensions>
- Kernel complements browser action execution. Use `browsers.computer.*` for screenshot, click, type, key, scroll, and drag, and `browsers.playwright.execute(sessionId, { code })` for DOM extraction, navigation, uploads, and structured return values. Kernel positions this as co-located execution without a local Playwright/Chromium install. Source: <https://www.kernel.sh/docs/introduction/control>
- Kernel complements observability. `browser_live_view_url` can be embedded in an iframe, including read-only mode. Replays and opt-in telemetry streams can enrich debugging and evidence review. They are external observations, not local receipts. Sources: <https://www.kernel.sh/docs/introduction/observe>, <https://www.kernel.sh/docs/browsers/telemetry/overview>
- Kernel should not replace local approval or receipt authority. Kernel's interactive live view, computer controls, Playwright execution, CDP, WebDriver BiDi, and MCP tools all perform browser actions remotely. Letting them invoke actions directly would create an alternate authority path outside local Node approval and receipt issuance. Sources: <https://www.kernel.sh/docs/introduction/control>, <https://www.kernel.sh/docs/reference/mcp-server>

#### Development-Time Cuts

1. Fastest immediate cut: cloud integration test runner. Package the existing MV3 artifact, upload it, create a session, and run deterministic Playwright assertions. This removes local Chrome profile setup, driver lifecycle, and browser binary/version handling. Sources: <https://www.kernel.sh/docs/browsers/extensions>, <https://www.kernel.sh/docs/browsers/playwright-execution>
2. Visual regression/debug lane without building one. Embed Kernel Live View and attach replay IDs/screenshots to failed test reports. Kernel supplies real-time viewing, downloadable MP4 recordings, and screenshot capture. Source: <https://www.kernel.sh/docs/introduction/observe>
3. Authenticated remote fixtures. Profiles persist cookies/local storage, while Managed Auth maintains authenticated sessions and offers hosted, React, or programmatic login flows. This could reduce fixture-login work, but moves credential/session custody to Kernel. Sources: <https://www.kernel.sh/docs/auth/profiles>, <https://www.kernel.sh/docs/auth/overview>
4. Scale later. Browser pools preconfigure extensions, profiles, viewports, and proxies for immediate acquisition. This is not an MVP time saver unless parallel browser jobs are already frequent. Pooled profile changes are read-only and never persisted. Source: <https://www.kernel.sh/docs/browsers/pools/overview>

#### Integration Handles

- SDK: `npm install @onkernel/sdk`; relevant handles include `kernel.browsers.create()`, `kernel.browsers.playwright.execute()`, `kernel.browsers.computer.*`, `kernel.browsers.telemetry.stream()`, and `kernel.browserPools.*`.
- Extension flow: `kernel extensions upload ./extension --name ide-extension`; create with `extensions: [{ name: "ide-extension" }]`; ad-hoc session upload also exists.
- MCP: hosted authenticated remote MCP over streamable HTTP or stdio, with OAuth 2.1/API key auth. Tools include browser/profile/pool management, computer actions, Playwright execution, and VM shell commands. Recommendation from this explorer: do not expose Kernel MCP directly to the approval-capable agent; wrap it behind the local kernel so every mutating call is pre-approved and receipt-recorded.
- Evidence adapter: map Kernel `session_id`, action request/result, telemetry sequence, screenshots, and replay IDs into locally signed receipt metadata. Kernel telemetry is opt-in and category-scoped.

#### Risks And Unknowns

- Kernel docs establish extension loading in Kernel cloud Chromium, not parity with Chrome's extension UI, permissions, service-worker lifecycle, or enterprise policy behavior on a developer's local browser. Validate the actual MV3 contract empirically.
- Kernel docs do not establish that telemetry/replays are tamper-evident, durable enough for the local receipt policy, or attributable to a local approval decision. Treat them as corroborating artifacts until a receipt-binding design is tested.
- Managed Auth says credentials/profiles are encrypted and isolated, but the source corpus does not establish required key custody, retention, export, deletion, or audit guarantees.
- The docs describe Unikraft-based cloud instances and state that core images are open source. They do not establish a self-hostable Docker-equivalent managed platform or operational equivalence with Kernel Cloud.

### Open-Source Image Feasibility - Capucci

#### Self-Hostable Pieces

The `kernel-images` repository is a complete, self-buildable browser-runtime implementation, not merely a client for Kernel's hosted API. The headful image builds a Chromium desktop stack plus Kernel's Go API, CDP and ChromeDriver proxies, Neko live-view server, recorder, and a Vue WebRTC client. Docker is explicitly supported through `images/chromium-headful/build-docker.sh` and `images/chromium-headful/run-docker.sh`.

Self-hostable functions include:

- Headful Chromium automation over CDP on `9222` and ChromeDriver/BiDi proxy on `9224`, suitable for Playwright/Puppeteer attachment and reconnect.
- Browser live view/control via Neko, using WebRTC or non-WebRTC mode. `ENABLE_READONLY_VIEW` is documented for view-only access.
- Screen/audio replay recording through the local API and FFmpeg. The Docker runner mounts output to a host `recordings/` directory.
- Local browser telemetry/event stream. Durable S2 storage is optional and activates only when all three S2 environment variables are supplied.

For `ide-extension`, this is compatible as an optional remote browser executor/observer. It does not need to replace local Node/kernel approval or receipt authority. Chrome MV3 can remain the browser-page observer/action surface, with this image reserved for isolated, reproducible browser sessions.

#### Copy / Reuse Feasibility

The repository license is Apache-2.0, permitting commercial copying, modification, distribution, sublicensing, and patent use subject to preserving the license, notices, and marking modified files.

Practical reuse choices:

- Copy/build the image as infrastructure. Fork or pin the repository, build the Docker image internally, and own ingress, identity, lifecycle, recording retention, and credentials.
- Reuse selected components. The Go API/OpenAPI surface, CDP monitor/proxy, recorder, and image scripts are separable enough to adapt, but they are coupled to supervisor, X11/PulseAudio, and Chromium layout.
- Avoid treating the root `package.json` as the product interface. Its scripts reference `containers/docker/Dockerfile`, which is absent from the reviewed checkout. The maintained operational path is under `images/chromium-*`.
- Audit transitive licenses before redistribution. The repository is Apache-2.0, but its build pulls Chrome for Testing, FFmpeg, Neko, Ubuntu packages, Node dependencies, and other artifacts.

#### Hosted-Service Dependencies

Docker operation is not inherently Kernel-hosted. The Unikraft path is hosted-service dependent as written: it requires Kraft CLI, `UKC_METRO`, `UKC_TOKEN`, a Kraft Cloud image registry/deployment, and public Kraft endpoints. Its scale-to-zero, snapshot/resume, and rapid restart claims belong to that unikernel deployment lane, not ordinary Docker.

Optional external dependencies:

- WebRTC across constrained NAT requires STUN/TURN; the README says Unikraft Cloud needs TURN because UDP exposure is unavailable.
- S2 is an optional durable event sink, not required for runtime operation.
- The Envoy/xDS path requires an external control plane plus instance JWT, but its startup script skips it when required variables are unset.

#### Operational / Security Requirements

Do not expose this image directly to the public Internet. CDP grants broad browser control; the runner publishes `9222`, `9224`, and the API/recording port (`10001` mapped as `444`). The API listeners themselves do not show a general external authorization layer. Place all externally reachable endpoints behind authenticated TLS ingress, network segmentation, and short-lived per-session authorization.

The provided Docker runner uses `--privileged` and its unikernel route defaults to Chromium `--no-sandbox --no-zygote`; both materially weaken host/browser isolation. Run as a dedicated, disposable workload with minimal mounts, non-sensitive test accounts, egress policy, patched base images, image/SBOM scanning, quotas, and explicit teardown.

Change Neko's checked-in `admin`/`neko` credentials before any non-local deployment. The default user profile can connect, host, share media, and access clipboard. Replay and telemetry must be classified as sensitive: they can capture pages, interaction data, browser state, and audio.

#### Risks And Unknowns

- The repository powers Kernel's hosted service, but it does not include a demonstrated multi-tenant control plane, tenant identity, billing, session scheduler, or hardened public ingress. Those must be supplied to operate it as a service.
- The documented Unikraft GUI URL is public to anyone possessing it; this is unsuitable for authenticated user sessions without an additional access gate.
- WebRTC audio is documented as non-functional in the README, despite image-level audio plumbing; validate the exact commit before relying on it.
- Build reproducibility is imperfect: the Dockerfile downloads "latest" FFmpeg artifacts and external browser/tool binaries. Pin artifact digests or mirror them internally for production.
- The repo's browser policies allow extension install sources broadly; tighten policies before loading any extension beyond a controlled, signed allowlist.

### Local Authority Fit - Noether

#### Boundary Fit

Kernel fits only as a browser-act adapter/module behind the local Node kernel, never as the governance kernel itself. The existing contract assigns grants, human approval, append-only audit, artifact refs, provider mediation, and emergency controls to the local kernel; the browser lane is expressly an adapter.

This means Kernel can reduce browser-operation implementation only if it exposes typed, local-callable observation/action primitives that can be invoked after a locally approved envelope. It must return enough evidence to form the required receipt fields; it cannot be the issuer of approval or the durable receipt writer.

The supplied local corpus contains no separate Kernel artifact or API contract beyond the research target, so this is a capability-fit assessment, not a confirmed integration claim.

#### Replaceable Pieces

Kernel could replace the bespoke implementation of:

- typed action execution and result shaping: read page, inspect forms, click a non-submit control, type into an editable field, scroll, and tab selection;
- DOM snapshot/ref production, if it returns stable control/field references and frame-aware evidence;
- perhaps the MV3 background/content-script message plumbing, but only if Kernel already has a legitimate attachment to the active Chrome tab.

Those are operational responsibilities assigned to the extension adapter, not to authority. ResonantOS demonstrates the same separable layer: an MV3 side panel/content-script system dispatches typed messages, supports frame reads, and injects its content code when needed.

Kernel can also save time by inheriting a narrow typed vocabulary instead of inventing a model-to-JavaScript bridge. ResonantOS validates and bounds planner actions rather than executing arbitrary script.

#### Non-Replaceable Pieces

Kernel must not replace:

- local approval queue, grant vocabulary, envelope typestate, or manual stop controls;
- `.ide-extension/state/` and the append-only event/receipt authority;
- receipt construction, including `approval_id`, before/after refs, and evidence refs;
- the canonical HTML workbench and its `/demo/l0` local-server witness;
- backend-held provider credentials.

These are explicit L0 requirements, including no browser-act without explicit approval and receipt.

Kernel also cannot erase the browser-host problem by assertion. If it lacks active-tab access, a Chrome extension, CDP attachment, or comparable browser-side authority, MV3 infrastructure remains necessary. The current design chose MV3 precisely because VS Code/VSCodium does not provide a stable third-party page/session control API.

#### Smallest Witness

Build one adapter-shaped witness, not a Kernel migration:

1. Add a `KernelBrowserAdapter` module declaration with only `observe` and `scroll` capabilities; forbid submit, credentials, payments, wallets, destructive actions, and durable writes.
2. `observe` returns a summarized page snapshot plus source/evidence refs; the local kernel persists it through the designed `/api/browser/context` route.
3. `scroll` follows: prepare typed envelope, local approval record, short-lived per-run capability token, Kernel call, result posted to `/api/browser/actions/:run_id/result`, and local kernel receipt append.
4. Smoke-test rejection before approval, success after approval, and durable receipt persistence.

That maps to the proposed bridge interfaces and preserves the desired source of truth.

#### Risks And Unknowns

- Kernel's browser attachment model, permission model, supported action vocabulary, and evidence output are absent from the local allowed corpus.
- A direct Kernel integration that lets it approve, retain broad credentials, or write receipts would invert the designed boundary.
- The ResonantOS precedent confirms a viable alternative: loopback bridge, per-run token, generated local config, MV3 adapter. It does not prove Kernel can replace it.
- Retain hard/public-submit classification even if Kernel offers a broader capability set. ResonantOS blocks those action classes before execution.

## Evidence Notes

- Kernel cloud can cut work fastest as a hosted browser test/observation lane, especially for MV3 extension upload, Playwright execution, live view, replay, and screenshot evidence.
- `kernel-images` can cut infrastructure work if the project wants a self-hosted isolated browser runtime, but it brings significant operations and security work. It is not a ready multi-tenant browser-control service.
- Neither Kernel cloud nor `kernel-images` should become the approval or receipt authority for `ide-extension`.
- The narrowest useful witness is an adapter behind the existing local kernel: observe plus scroll, with rejection-before-approval and receipt-after-action proof.
