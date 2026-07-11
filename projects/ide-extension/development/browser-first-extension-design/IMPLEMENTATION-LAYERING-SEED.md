---
id: ide-extension-browser-first-layering-seed
project: ide-extension
title: "Browser-First Extension Implementation Layering Seed"
status: draft
node_type: implementation-layering-seed
updatedAt: 2026-07-10
invoke_mode: design
---

# Implementation Layering Seed

This is a design-stage layering seed, not an execution work-pack.

## Layer Snapshot

| Layer | Claim | Evidence Needed Before Promotion |
| --- | --- | --- |
| L0 existing | Local HTML workbench, kernel state, approval queue, dry-run envelope, receipt append. | Existing `npm run smoke` and schema validation pass. |
| L0.5 MCP/chat adapter admission | Fake/local stdio MCP server, one allowlisted `observe` tool, local `DesignFeedbackContextPacket`, approval-gated invocation, local evidence refs, and kernel-minted receipt. | Offline positive and negative tests pass; no external service, browser, network, provider, or authenticated dependency is required. |
| L0.6 browser-first extension | Chrome MV3 extension opens side panel, reaches local workbench/kernel, reads active page, blocks hard actions, and performs one approved safe typed action on a fixture. | Extension loads unpacked; side panel renders; content script snapshot works; approval policy tests pass; approved action receipt is appended after L0.5 admission proof. |
| L1 IDE chrome wrapper | VS Code/VSCodium wrapper opens or embeds the same local workbench URL. | Extension-host tests prove owned webview/openExternal behavior; no integrated-browser control claim. |
| L2 automation witness | Playwright MCP/direct Playwright drives the local workbench or a fixture browser page for regression evidence. | Playwright test proves read/click/type/scroll fixture behavior and screenshot/snapshot evidence. |

## Promotion Guardrails

- L0.5 does not require OpenRouter keys.
- L0.5 does not require VS Code/VSCodium integration.
- L0.5 does not require Playwright MCP.
- L0.5 does not require Chrome, Chrome DevTools, Kernel Cloud, Yocoolab,
  GitHub, Pendo, deployment hooks, live browser sessions, external network, or
  provider delegation.
- L0.5 does not execute shell, file writes, commits, pushes, publication,
  external account actions, browser mutation, or network actions.
- Adapter evidence promotes only the adapter-admission harness, not a general
  MCP integration, autonomous IDE-agent, or browser-control claim.
- Browser action evidence promotes only the later browser-first extension lane,
  not a general autonomous IDE-agent claim.

## Minimum L0.5 Evidence Shape

| Evidence | Required Check |
| --- | --- |
| Adapter registration | Descriptor accepts only `transport: stdio`, bounded command/args, fixture CWD, temp/redacted HOME, env allowlist, one `observe` tool, `network: false`, `mutation: false`, and `receipt_authority: false`. |
| Context packet | `DesignFeedbackContextPacket` fixture includes selected element, URL, screenshot/artifact ref, selection history, source-candidate hypotheses, companion message, and context refs. |
| Approval block | Run before approval returns approval-required and invokes nothing. |
| Approved observe | One explicit approval invokes exactly one allowlisted fake observe call. |
| Evidence binding | Receipt references kernel-written evidence artifacts for envelope, approval, adapter, descriptor hash, allowlist hash, context hash, transcript hash, before/after digest, and custody descriptor. |
| Negative approval tests | Forged, wrong, expired, and reused approvals reject. |
| Negative tool tests | Non-allowlisted, mutation, network, PR, deployment, Pendo, credential, broad-Claude, and live-write actions reject at registration or run. |
| Self-approval block | Proposer, approver/session, adapter invoker, and receipt appender remain separable. |
| Env containment | Hostile fake stdio server sees only allowlisted env, temp/redacted HOME, and bounded fixture CWD. |

## Minimum L0.6 Browser Evidence Shape

| Evidence | Required Check |
| --- | --- |
| Manifest load | Chrome accepts unpacked extension with side panel and content scripts. |
| Side panel mount | Side panel frames `/demo/l0` or fallback shell fetches `/api/state`. |
| Bridge health | Extension background reaches loopback server and handles unauthorized/missing bridge state. |
| Page read | Content script returns title, URL, text excerpt, controls, fields, and frame count. |
| Safe action | Approved click/type/scroll on local fixture appends a receipt. |
| Hard-boundary block | Credential/wallet/payment/public-submit/destructive attempt is blocked before content action. |
| State separation | Receipts live under `.ide-extension/state/`; extension storage does not become authority. |

## Layer Split

The next plan should build L0.5 only. L0.6, L1, and L2 stay separate because
mixing MCP/chat admission, Chrome extension, VSCodium wrapper, and Playwright
MCP in one first slice would hide the proof boundary.
