# Claude Agent SDK — Lifecycle Event ↔ Tilth Mapping Reference

**Authority:** EN-002 amendment at `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-002_sdk_lifecycle_vocabulary_2026-04-19.md`
**SDK version pinned:** as published at https://platform.claude.com/docs/en/agent-sdk/ on 2026-04-19 (post-"Claude Code SDK → Claude Agent SDK" rename; Python SDK `claude-agent-sdk-python` and TypeScript SDK `claude-agent-sdk-typescript` at the `anthropics/` GitHub org)
**Status:** snapshot, not live mapping. Refresh on SDK minor version bump.
**Scope:** reference / interop only. Does NOT rename, replace, or supersede any Tilth primitive.

## Table

| SDK lifecycle event | Tilth lifecycle moment | F-codes / P-surfaces that correspond | Notes |
|---|---|---|---|
| **PreToolUse** | Before a seat invokes a vault / Commons / file / web tool | F-ROUTER-STALE-API (order 5), F-CONTEXT-PLACEMENT (order 7), F-INTAKE-ELIGIBILITY-FAIL, F-INTAKE-SUBSTANCE-GAP, F-TDSL-LEAK-V01, F-COMMONS-SIGNATURE-INVALID, F-COMMONS-RUBRIC-STALE, F-COMMONS-UPLOAD-SCOPE-LEAK, F-OPPORTUNITY-TIER1-UPLOAD-SCOPE-LEAK, F-TELEMETRY-K-ANON-VIOLATION, F-TELEMETRY-PAYLOAD-SCOPE-LEAK, F-CRYPTO-AGILITY-HARDCODED, F-A7-CALIBRATION-MISSING/STALE/UNSIGNED | Tilth's PRE-gate layer; in Tilth, PRE-gate evaluation is deterministic Python + Cedar, fail-closed. |
| **PostToolUse** | After a tool returns; before the next seat step | F-VERDICT-CERT-MALFORMED, F-P-COHERE-1 (intra-grant), F-P-COHERE-2 (grant↔RFA), F-P-COHERE-3 (grant↔PROJECT_CONTEXT), F-COMMONS-DISSECTION-MISMATCH, F-OPPORTUNITY-TIER1-POISON | Tilth's POST-gate layer. |
| **PostToolUseFailure** | Tool errored; failure is a first-class event | Autonomy Rule 1 ("Save State Always — success AND failure") | Tilth already treats failure as first-class; this SDK event name aligns with existing discipline. |
| **PreCompact** | Immediately before a window boundary compacts context | F-A7-WINDOW-BUDGET-OVERFLOW (defensive), F-A7-CROSS-WINDOW-CONTRADICTION (fires POST at next window's Judge) | Section A7 windowing. Tilth uses signed calibration artifact + Option-B compound-txn persist; SDK PreCompact is a primitive that A7's richer machinery would sit on top of. |
| **SubagentStart** | A seat (or sub-seat) invocation begins | Rule 1 state-save on session_start; router.yaml binding verification (F-ROUTER-STALE-API pre-check) | In Tilth v0.1, "subagent" = child seat invocation within a pipeline phase. |
| **SubagentStop** | A seat returns its final output | SFR three-block verdict format validation (A3 F-VERDICT-CERT-MALFORMED), KGIE preflight validation on Scribe returns, cross-family rigor check (reviewer family ≠ author family per L-003) | Tilth's "clean output" discipline (Autonomy Rule 4) lands here. |
| **Stop** | The pipeline phase terminates | P8 final sign-off, session metrics write to `pipeline/metrics/session_log.jsonl`, rails-report assembly | Session Close Self-Check from CLAUDE.md runs here. |
| **UserPromptSubmit** | Operator input event (prompt or sign-off) | P1 (Eligibility), P2 (Substance gaps), P3 (Section list), P4 (Admin-risk substitution), P5 (UNSOURCED claim), P6 (Cross-section contradiction), P7 (Rigor breach / M13 territory), P8 (Final sign-off) | All eight Tilth P-surfaces fire through this lifecycle moment. |
| **PermissionRequest** | Async consent flow | P4 (admin-risk substitution approval), P5 (UNSOURCED claim approval), M13 bypass request | Matches Tilth's "applicant must approve each substitution" discipline (Law 4). |
| **Notification** | Non-interrupt-worthy event surfaces | Rails-report accumulation channel (reviewed at P8), A11 Telemetry Commons event feed | Events that do NOT trigger a P-surface interrupt land here for later review. |

## How to use this table

**Interop scenario 1** — Tilth interoperates with an SDK-based tool or third-party runtime. Map the external tool's lifecycle events onto Tilth's F-codes / P-surfaces using the middle column.

**Interop scenario 2** — A future contributor reads SDK docs and wonders where a given SDK event "lives" in Tilth. Read left to right.

**Interop scenario 3** — An engineer drafts a new F-code and wonders which lifecycle bracket it belongs to. Read right to left; confirm the bracket; match to Tilth's existing PRE/POST/P-surface taxonomy.

## What this table does NOT do

- Does not rename Tilth F-codes to SDK event names.
- Does not authorize substitution of SDK event handling for Tilth's Logician gate evaluation.
- Does not imply the SDK is a dependency of Tilth.
- Does not imply Tilth adopts SDK semantics for any event (e.g., Tilth's "Stop" includes mandatory session metrics write; the SDK's Stop does not).

## Refresh log

| Date | SDK version reference | Change |
|------|-----------------------|--------|
| 2026-04-19 | Initial snapshot at EN-002 LOCK | Initial write. Pinned at Python SDK + TypeScript SDK as published 2026-04-19. |

## Rejected mappings (for future contributors)

The following SDK patterns were explicitly reviewed and rejected as Tilth equivalences during the 2026-04-19 Thesis debate. Do NOT add them to this table on a future refresh without a new Thesis round.

- SDK `canUseTool` runtime callback ≠ Tilth Law 3 enforcement. Tilth uses Cedar; `canUseTool` is an imperative escape hatch, not a Cedar substitute.
- SDK description-driven subagent dispatch ≠ `router.yaml`. Tilth dispatch is deterministic by design.
- SDK permission modes (`plan`, `acceptEdits`, `bypassPermissions`) ≠ Tilth operational gears (Sparring Partner, Co-Pilot, Synthesizer). Different axes.
- SDK `session_id` ≠ A7 signed calibration artifact. A7 is a richer superset.
- SDK automatic CLAUDE.md reload on compaction ≠ A4 prompt-placement discipline. Different failure modes; they compound, not substitute.
