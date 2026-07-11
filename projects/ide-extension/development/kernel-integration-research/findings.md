# Kernel Integration Research

Dispatch: `2026-07-10-kernel-integration-research`
Status: `resolved`
Question: Can Kernel and `kernel-images` cut development time for `ide-extension` without moving authority away from the local HTML workbench and Node governance kernel?

## Short Answer

Kernel Cloud is a **candidate L0.5 witness lane pending proof**, not a selected integration yet. It may cut time by providing an isolated cloud Chromium lane for a packaged MV3 artifact, remote browser execution, live view, screenshots, and replay. Adoption is gated on a blocking witness that proves local approval-before-action, no bypass path, and local receipt-after-action. See [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:41).

Do not self-host `kernel-images` now. Treat it as Kernel's implementation precedent and future escape hatch if Kernel Cloud fails concrete custody or deployment-control requirements. The local HTML workbench and local Node governance kernel remain authoritative. See [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:72).

## Product Meaning In Plain Language

Kernel Cloud can give us a disposable remote browser where we can load and test our browser extension with less setup. That is useful for proving the extension can run in a controlled browser and for collecting screenshots or replays when something fails.

It does **not** mean Kernel Cloud becomes our agent system. It does **not** mean Kernel Cloud controls the user's already-open local Chrome tab. The local Node governance kernel is still the part that decides whether an action is allowed, records approval, prevents bypasses, and writes the durable receipt. Kernel-provided session identifiers, screenshots, replays, telemetry, and action responses are external observations/artifacts that the local kernel may reference in `evidence_refs`; they are not receipts and are not durable, attributable, or tamper-evident unless the witness proves local binding. See [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:124).

## Verdict Matrix

| Candidate | Verdict | Why |
| --- | --- | --- |
| Kernel hosted adapter | **Candidate, blocking witness required** | Kernel Cloud appears to own the useful remote-browser infrastructure: isolated Chromium, packaged extension loading, session lifecycle, Playwright/CDP execution, live view, screenshots, and replay. Its browser attachment model, permission/action vocabulary, and evidence output still need local proof. |
| `kernel-images` self-host adapter | **Defer** | The repo is self-buildable, but self-hosting would add control-plane, ingress, isolation, credential, retention, sandbox, and operations work before the Cloud witness proves value. |
| Kernel MCP | **Do not expose directly** | MCP is a transport/tool exposure, not an authority path. Any Kernel SDK, MCP, CDP, WebDriver, Playwright, or computer-control use must be admitted by the local Node governance kernel and executed only through the adapter. |
| Kernel extension upload/live view | **Use only inside the witness** | Extension upload/live view can test an isolated cloud Chromium lane. It does not prove local Chrome parity, local-tab control, or an adopted runtime. |
| ResonantOS-style Chrome MV3 extension | **Retain as planned active-local-browser adapter** | It remains the planned path for active-local-browser observation and typed actions unless a separately validated legitimate local-tab attachment path is demonstrated. |
| No-go zones | **Kill** | No Kernel Cloud approval authority, remote-issued receipts, direct model access to Kernel credentials, raw remote execution bypass, public-submit automation, credential entry, wallet/payment/destructive actions, or local-browser-control claims. |

## Architecture Recommendation

The local HTML workbench remains the user-facing local surface. The local Node governance kernel owns authorization, typed envelopes, bypass prevention, append-only audit, durable state, and canonical receipt issuance. See [SPEC.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md) and [ARCHITECTURE.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md).

Name the boundary `KernelCloudBrowserAdapter`. It is a thin local-authority boundary over Kernel Cloud, not a browser runtime and not a governance kernel. It accepts only locally authorized typed requests, calls Kernel Cloud, and normalizes external observations/artifacts into local `evidence_refs`.

Kernel Cloud owns remote browser operations only: isolated Chromium, packaged MV3 loading for cloud compatibility testing, remote execution surfaces, live view, screenshots, and replay. Kernel documentation describes browser creation, control, and observation primitives. See [Create](https://www.kernel.sh/docs/introduction/create), [Control](https://www.kernel.sh/docs/introduction/control), and [Observe](https://www.kernel.sh/docs/introduction/observe).

OpenRouter remains server-side and can propose envelopes only. MCP, CDP, Playwright, SDK calls, and computer-control endpoints are invocation transports or remote execution surfaces, not authority mechanisms.

## What Kernel Cuts / Does Not Cut

Kernel Cloud can reduce work on a focused remote browser harness: isolated Chromium provisioning, packaged extension loading for cloud tests, Playwright execution, live debugging, screenshots, and replay. See [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:49).

It does not remove local governance, approval recording, durable state, provider credential custody, canonical receipt construction, or the planned active-local-browser MV3 lane. It also does not prove local Chrome/MV3 lifecycle, policy, profile, permission, or active-tab parity. See [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:142).

## Blocking L0.5 Witness

Define `KernelCloudBrowserAdapter` with exactly `observe` and typed `scroll`. Forbid raw MCP, CDP, WebDriver, Playwright code, navigation, click, type, credential handling, submit, payment, wallet, destructive action, and durable write outside the adapter. See [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:156).

Build and hash the packaged MV3 artifact. Pin the Kernel browser/image version, fixture version, and evidence-retention policy. Upload the artifact, create an isolated Kernel Cloud Chromium session, and prove both a fixture-visible content-script marker and service-worker runtime-message acknowledgement. A successful upload/create response alone is not enough. See [Kernel extension upload API](https://www.kernel.sh/docs/api-reference/extensions/upload-a-browser-extension) and [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:63).

Prove these invariants:

- A `scroll` without `approval_id` is locally rejected, makes zero remote action calls, and leaves observed scroll state unchanged.
- An approved `scroll` binds one typed envelope to one local approval and executes only through `KernelCloudBrowserAdapter`.
- No approval-capable agent has direct Kernel API credentials or direct MCP/CDP/WebDriver/Playwright access.
- The local canonical receipt includes at least the current contract fields: `receipt_id`, `run_id`, `stage`, `status`, `before_ref`, `after_ref`, `approval_id`, `evidence_refs`, and `created_at`.
- Proposed extra binding fields include envelope digest, artifact hash, fixture/origin, Kernel session ID, action request/result digests, and before/after evidence digests.
- Restarting the local Node governance kernel on the same state directory preserves the receipt/hash chain, recovers the completed run, and replaying the same `run_id` causes no second remote action.

This witness proves only isolated packaged-MV3 compatibility testing behind local authority. It does not prove local Chrome active-tab control, local MV3 lifecycle/policy parity, or general reproducibility beyond the pinned artifact, provider version, fixture, and retention configuration.

## Kill Criteria

Stop the Kernel Cloud lane if any action reaches Kernel Cloud without a local authorization decision, if rejected actions make a remote call or mutate remote browser state, or if the required observations/artifacts cannot be bound to a local receipt.

Also stop if content-script or service-worker acknowledgement is unreliable in the pinned fixture, if the lane needs raw remote execution primitives beyond `observe` and typed `scroll`, or if Kernel Cloud cannot meet the pinned retention, custody, or fixture requirements.

## `kernel-images` Deferral Rationale

`kernel-images` is useful as source evidence and an escape hatch, but not as the next implementation target. The repository can self-host a Chromium runtime, live view, replay, CDP, ChromeDriver/BiDi proxy, and local API, but it does not include a ready multi-tenant control plane. See [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:72).

Deferral is based on concrete risks: public CDP/API exposure, privileged Docker and weakened Chromium sandboxing, default Neko credentials and clipboard access, sensitive replay/telemetry retention, required ingress/auth/segmentation ownership, mutable build dependencies, broad extension-install policy, and missing multi-tenant control-plane ownership. See [research.md](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md:104).

Advance to `kernel-images` only if a concrete custody, deployment-control, or availability requirement cannot be met by Kernel Cloud and the team explicitly accepts disposable-hosting, authenticated ingress, network isolation, image pinning, recording retention, and sandbox-risk ownership.

## Development-Time Impact

If the blocking witness passes, Kernel Cloud can cut development time by avoiding a bespoke isolated browser test platform and by giving us live view/replay/screenshot evidence early. That lets the project focus on the real differentiator: local authority, typed action admission, approval receipts, and a usable HTML workbench.

If the witness fails, the fallback is not immediately self-hosting everything. The first fallback is to keep the ResonantOS-style MV3 lane and direct Playwright/MCP validation lane while preserving the same local approval/receipt model.

## Next Implementation Slice

1. Define the `KernelCloudBrowserAdapter` interface and a strict two-operation allowlist.
2. Add local envelope, approval, audit, receipt, no-bypass, and idempotence tests before any Kernel Cloud call.
3. Build, hash, upload, and verify the packaged MV3 artifact in an isolated Kernel Cloud Chromium fixture.
4. Implement approved typed `scroll` only, normalize Kernel observations/artifacts as local `evidence_refs`, and verify the full rejection/approval/restart witness.

## Sources

- [Kernel Integration Research](/home/vrondelli/projects/domainspec-core/projects/ide-extension/development/kernel-integration-research/research.md)
- [ide-extension Specification](/home/vrondelli/projects/domainspec-core/projects/ide-extension/SPEC.md)
- [ide-extension Architecture](/home/vrondelli/projects/domainspec-core/projects/ide-extension/ARCHITECTURE.md)
- [Kernel documentation](https://www.kernel.sh/docs)
- [Kernel Create docs](https://www.kernel.sh/docs/introduction/create)
- [Kernel Control docs](https://www.kernel.sh/docs/introduction/control)
- [Kernel Observe docs](https://www.kernel.sh/docs/introduction/observe)
- [Kernel extension upload API](https://www.kernel.sh/docs/api-reference/extensions/upload-a-browser-extension)
- [`kernel-images` reviewed commit](https://github.com/kernel/kernel-images/tree/ae64afa4a46ff196e50488057ebb7b4168f9691d)
