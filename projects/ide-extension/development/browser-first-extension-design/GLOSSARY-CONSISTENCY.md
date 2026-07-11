---
id: ide-extension-browser-first-glossary-consistency
project: ide-extension
title: "Browser-First Extension Glossary Consistency"
status: flag
node_type: glossary-consistency-report
updatedAt: 2026-07-10
invoke_mode: design
---

# Glossary Consistency Report

## Status

`flag`

`ide-extension` has a `SPEC.md`, `ARCHITECTURE.md`, and research findings, but
does not yet have a standalone glossary or full DomainSpec aspect-doc concept
registry. This report therefore checks term consistency against the local
project artifacts and records candidate terms without promoting them.

## Consistent Existing Terms

| Term | Consistency |
| --- | --- |
| `local-server-first governed workbench` | Matches `README.md`, `SPEC.md`, and `ARCHITECTURE.md`. |
| `IDE-adjacent` | Means editor-adjacent workbench/chrome, not autonomous IDE mutation. |
| `kernel` | Owns manifests, grants, approvals, audit, artifacts, provider mediation, and envelopes. |
| `module manifest` | Registered capability descriptor; visibility does not grant authority. |
| `agent envelope` | Boundary object for proposed action/agent crossing with typestate and receipts. |
| `approval queue` | Human authorization surface before effectful crossings. |
| `receipt` | Durable evidence object for approved or blocked effects. |
| `evidence_refs` | Kernel receipt links to owner-held artifacts; adapter-specific hashes stay in evidence artifacts unless receipt schema evolves. |
| `OpenRouter provider adapter` | Provider transport only; not authority, agent core, or approval owner. |
| `VS Code/VSCodium wrapper` | Optional chrome around the local URL; not browser-control proof. |
| `browser-act adapter` | External browser action plane, approved for Chrome extension or Playwright MCP lane. |
| `MCP transport` | JSON-RPC capability transport; not authority, consent, durable state, or receipts. |

## Candidate Terms Introduced By This Design

These terms are candidate design vocabulary only.

| Candidate Term | Working Meaning | Promotion Status |
| --- | --- | --- |
| `browser-first extension lane` | Chrome MV3 extension path that wraps the local workbench and mediates real web tabs. | Candidate, not canonical. |
| `McpChatWitnessAdapter` | Owned local adapter-admission harness using fake/local stdio MCP and one allowlisted `observe` tool. | Candidate, not canonical. |
| `DesignFeedbackContextPacket` | Local context/evidence packet inspired by Yocoolab selection/thread grammar. Source candidates are hypotheses. | Candidate, not canonical. |
| `adapter descriptor` | Registration record for transport, command/args, custody statement, env allowlist, CWD/HOME scope, and tool allowlist. | Candidate, not canonical. |
| `adapter admission harness` | Kernel-owned path that proves a proposed adapter can act only through approval, allowlist, evidence refs, and kernel receipts. | Candidate, not canonical. |
| `provider delegation` | Later provider/process lane such as `claude-max-mcp`; requires process, cwd, env, HOME, tool, timeout, credential, and network descriptors. | Candidate, not canonical. |
| `side-panel shell` | Minimal Chrome side-panel HTML that frames or mirrors `/demo/l0`. | Candidate, not canonical. |
| `background router` | MV3 service worker that connects side panel, content scripts, and local server. | Candidate, not canonical. |
| `content-script witness` | Per-page DOM observer/action executor with typed messages and refs. | Candidate, not canonical. |
| `browser snapshot` | Summarized active-tab context: URL, title, text, links, controls, fields, frames, viewport. | Candidate, not canonical. |
| `control ref` | Stable-enough page-local reference assigned to visible controls and fields. | Candidate, not canonical. |
| `bridge token` | Per-run or configured loopback authorization token for extension-to-kernel calls. | Candidate, not canonical. |
| `capability token` | Optional route-scoped token for bridge calls. | Candidate, not canonical. |
| `hard browser boundary` | Action class blocked in L0.5: credentials, wallet/signature, payment, destructive, privileged operations. | Candidate, not canonical. |
| `public-submit boundary` | Submit/publish/post/share/send/save/confirm class requiring human-only handling in L0.5. | Candidate, not canonical. |

## Conflict Checks

| Check | Result |
| --- | --- |
| `extension` ambiguity | Flagged. Use `Chrome browser extension` for this lane and `VS Code/VSCodium wrapper` for editor chrome. |
| `browser control` ambiguity | Flagged. Use specific operations: open URL, read page, detect forms, click, type, scroll, screenshot/test via Playwright. |
| `adapter` ambiguity | Flagged. Distinguish MCP/chat witness adapter, Chrome/MV3 browser adapter, provider adapter, and validation witness. |
| `context packet` authority drift | Pass with caveat. The refreshed design marks source candidates as hypotheses, not source truth. |
| `network.call` collapse | Pass. The refreshed design classifies `claude-max-mcp` as deferred provider/process delegation, not just network. |
| `agent` overclaim | Pass. The design keeps agent envelopes/proposals separate from autonomous execution. |
| `OpenRouter core` overclaim | Pass. OpenRouter stays behind backend provider adapter. |
| `canvas authority` drift | Pass. Canvas/workbench nodes must point to source refs, approvals, run ids, and receipts. |
| `VS Code Integrated Browser SDK` claim | Pass. The design rejects this as baseline. |

## Patch Requests

No upstream mutation is applied by this design mode.

Recommended later glossary patch:

- add a small `GLOSSARY.md` or concept table for `ide-extension`;
- disambiguate `Chrome browser extension` from `VS Code/VSCodium wrapper`;
- disambiguate `McpChatWitnessAdapter`, `DesignFeedbackContextPacket`,
  provider delegation, browser adapter, and validation witness;
- define `browser snapshot`, `browser action`, `bridge token`, and `hard browser boundary`;
- link each term to the owning artifact and receipt behavior.
