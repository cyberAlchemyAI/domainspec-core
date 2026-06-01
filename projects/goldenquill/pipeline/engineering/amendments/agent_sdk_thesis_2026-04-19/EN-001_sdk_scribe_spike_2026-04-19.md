# EN-001 — Scribe-via-Agent-SDK Spike (Deferred Engineering Queue Entry)

**Amendment ID:** EN-001
**Date:** 2026-04-19
**Type:** Engineering Note — deferred queue entry, not active work
**Status:** `LOCKED-internal-simulated` pending operator sign-off + live cross-family re-audit
**Authority:** Thesis debate at `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/00_debate_and_consensus.md`

---

## Scope

Time-boxed engineering experiment ("spike": produces evidence, not committed code) to measure whether the Claude Agent SDK's generic agent runtime improves Scribe's section-by-section drafting operation versus Tilth's current manual orchestration.

Spike is **not on the current engineering queue.** It is queued behind:

1. §6 Operating Envelope blueprint LOCK
2. §4 Logician v2.2 LOCK
3. §0.5 Blueprint Interface Index v4 refresh
4. Real-engineer validator gate per Da Vinci §13

All four preconditions must land before the spike opens.

## Why Scribe and not another seat

Scribe's primary model binding in `router.yaml` is `anthropic/claude-sonnet-4-6` — native target for the Anthropic-published Agent SDK. No LiteLLM translation layer required; tool-use fidelity preserved. All other LLM-backed seats (Editor, Judge, Red Team) use non-Anthropic primaries and would require LiteLLM, which introduces tool-use reliability risk on Llama/Qwen/GPT-OSS families. Scribe is the single SDK-spike candidate with zero translation overhead.

## What the spike measures

Single-grant, single-section autonomous drafting against a real RFA dissection and PROJECT_CONTEXT. Scribe agent reads vault artifacts via built-in Read/Grep/Glob tools, drafts the section, emits clean output per Autonomy Rule 4.

Success metrics (measured in-spike, not inherited from any general benchmark):

- **Tool-use reliability** *(agent successfully calls the right tool with the right arguments and processes the result correctly)* ≥ spike-specific threshold, measured against Tilth's vault schema.
- **Sovereignty posture preserved** — BYOK keys unchanged, no phone-home, all data local.
- **Dependency footprint** — ≤ 200 MB incremental disk/memory over current Scribe path.
- **Latency** — within 20 % of current baseline for an equivalent single-section draft.
- **KGIE preflight** — unchanged pass rate against current Scribe.
- **Law 3 isolation** — zero cross-org file access attempts (enforced by Cedar; not by SDK hooks).

Any failure = abandonment.

## F-code deferral

F-codes governing the spike's PRE/POST hooks (candidates: F-SCRIBE-SPIKE-TOOLUSE-LEAK, F-SCRIBE-SPIKE-KGIE-FAIL, F-SCRIBE-SPIKE-LAW3-BREACH) are **deferred to the spike charter at spike-open**. They are not silently added to the failure-code primitive list now. This amendment introduces zero F-codes.

## Rollback procedure

1. Spike runs on a dedicated branch; main-line Scribe code preserved verbatim.
2. No state persisted in SDK-only format. All spike outputs (drafts, logs, metrics) use Tilth's existing vault schemas.
3. Abandonment = branch revert + zero-state migration. No data loss, no dependency residue.
4. If spike succeeds → second-round Thesis on productionization plan before any main-line merge.

## Controlled-dependency declaration

The Claude Agent SDK is an **external library whose API we do not control**. It is not a sovereignty violation (it is a local Python library, runs in-process, honors BYOK), but its surface area drifts — the 2025 "Claude Code SDK → Claude Agent SDK" rename demonstrates this. Therefore:

- SDK version is pinned at spike-open in `pipeline/engineering/agent_sdk_spike_manifest.yaml`.
- Version bumps are reviewed, not automatic.
- Quarterly audit checkpoint: has the SDK deprecated a feature the spike depends on?
- Exit criterion: if the SDK ships a breaking change that the spike cannot reasonably absorb, spike halts and is re-scoped.

## Cross-family rigor

The spike does **not** violate L-003. Scribe is already Anthropic-family per `router.yaml`; wrapping it in the Anthropic Agent SDK does not add cross-family obligations. Editor, Judge, and Red Team stay on their current non-Anthropic primaries and review the spike's output using their normal channels — cross-family rigor is preserved by the existing Thesis discipline, not by the SDK.

## Not in scope (rejected in the Thesis debate)

- `canUseTool` runtime callback displacing Cedar policies. Cedar is declarative and verifiable; `canUseTool` is an imperative escape hatch. REJECT.
- Skills / description-driven semantic dispatch displacing `router.yaml`. Non-determinism breaks the audit chain. REJECT.
- SDK permission modes (`plan`, `acceptEdits`, `bypassPermissions`) renamed or merged with operational gears (Sparring Partner / Co-Pilot / Synthesizer). Different axes — tool-call approval friction vs. operator autonomy delegation. REJECT.
- SDK auto-reload of memory files replacing A4 prompt-placement discipline. Different failure modes (attention decay within a window vs. information loss across compaction). They compound; neither substitutes for the other. REJECT.
- Subagent context isolation displacing Cedar's Law 3 enforcement. Cedar is primary; subagent isolation is complementary at best. REJECT as substitute.
- `session_id` replacing A7's signed calibration artifact. A7 is a richer superset. REJECT.
- MCP channels for Scout. Right shape at v0.2+ federation scale, premature at v0.1. DEFER (not REJECT — revisit at the v0.2 Section 3 rewrite).

## Dependency chain

| Dependency | Reason |
|------------|--------|
| §6 Operating Envelope blueprint LOCK | Hosts PRE-gate precedence + context-placement enforcement; spike hooks must reference it |
| §4 Logician v2.2 LOCK | F-code primitives updated; spike charter can reference stable set |
| §0.5 v4 refresh | Interface index captures post-v7 A12 primitives the spike would depend on |
| Real-engineer validator gate (Da Vinci §13) | Outside-impartial audit gate — no SDK spike without a real engineer's code-review signature |

All four preconditions gate spike-open. Without them, this amendment is dormant.

## Sign-off

- Cycle 1 verdict: REQUIRES_MINOR_FIXES across all seats; no BLOCKING findings.
- Cycle 2 verdict: READY across all seats.
- Judge score Cycle 2: 96/100.
- Logician Cycle 2: no silent F-code additions, no Cedar rule changes.
- Red Team Cycle 2: zero in-scope remaining (1 HIGH + 3 MED + 1 LOW from Cycle 1 all CLOSED).

Operator signature required for promotion from `LOCKED-internal-simulated` to `LOCKED-sealed`. Until then, this amendment is documentation — it describes an experiment that may run in a future phase, not an experiment in progress.

---

## Cycle 2 Fixes — Applied 2026-04-20 (addresses live cross-family audit findings)

The live cross-family audit at `cross_family_audit/` surfaced 1 HIGH + 5 MED + 1 LOW + Editor notes. Fixes F-1 through F-7 below address each finding inline.

### F-1 — Concrete rollback procedure (addresses RT-NEW-01 HIGH + JUDGE-DISSENT reversibility dock)

**Replaces the "Rollback procedure" section with:**

1. **Branch-only code isolation.** Spike runs on dedicated branch `spike/scribe-sdk-<iso-timestamp>`. Main-line Scribe code preserved verbatim; no merges to main during the spike.
2. **External-state inventory, pre-spike.** Before the spike opens, the spike manifest enumerates every external mutable store the Scribe SDK agent may touch: ChromaDB collections (list specific collection names), vault paths (list specific paths under `vault/`), lessons.md entries (spike must NOT write to lessons.md — any proposed addition goes in `spike-proposed-lessons.md` for operator review post-spike), daily_logs entries (spike writes to `daily_logs/spike-<id>.md` only, not the main daily log), git working tree.
3. **Transactional sandbox.** All external writes during spike execution are mirrored to a `spike-scratch/<spike-id>/` directory. Mirrors include pre/post snapshots of any file touched. Abandonment procedure reverts the mirror and discards the scratch directory.
4. **Concrete abandonment commands.**
   ```bash
   # dry-run preview
   scripts/spike_rollback.sh --spike-id <id> --dry-run
   # apply
   scripts/spike_rollback.sh --spike-id <id> --apply
   # verify
   scripts/spike_rollback.sh --spike-id <id> --verify
   ```
   Rollback script restores snapshotted files, deletes scratch dir, checks out main branch, confirms git working-tree clean.
5. **Decision gates.** Operator signs rollback approval via `pipeline/engineering/spike_rollback_ledger.jsonl` entry (similar to existing lock_history.v1.jsonl pattern). Gate is operator-alone for v0.1; Da Vinci joins when live.
6. **Timeline.** Rollback must complete in ≤ 1 hour from spike-abandonment declaration. If rollback hits an unexpected obstacle, escalation path: operator re-declares spike FAILED in ledger, opens fresh Thesis round for remediation, does NOT leave partial rollback state.

### F-2 — SDK breaking-change detection mechanism (addresses RT-NEW-02 MED)

**Adds to the "Controlled-dependency declaration" section:**

*Silent-change detection: spike manifest includes an automated integration test (`tilth/tests/sdk_contract_check.sh`) that runs at spike-open, at each SDK version bump, and at the quarterly audit. The test:*
- *Captures the pinned SDK's public interface as a snapshot JSON (method names, signatures, field shapes on known response types).*
- *Compares subsequent SDK versions against the snapshot; any change to existing public surface area triggers operator review before the version bump lands.*
- *Monitors outbound HTTP traffic during test runs (via mitmproxy or similar). All outbound destinations must be on an allowlist (Anthropic API endpoints only). Any additional destination = sovereignty violation = test fails.*

### F-3 — Concrete "LOCK landed" definition (addresses RT-NEW-03 MED)

**Adds to the "Dependency chain" table a lead-in:**

*"LOCK landed" for each of the four preconditions means: (a) the LOCK artifact exists at its canonical path AND is signed by operator in `pipeline/engineering/lock_history.v1.jsonl` AND its SHA-3-512 hash matches the operator-signed hash in the ledger. Ambiguity resolved at the file level, not in prose — no precondition is "landed" until all three conditions are mechanically verifiable by a zero-token Logician pre-check.*

### F-4 — L-003 precedent statement (addresses RT-NEW-06 MED)

**Adds to the "Cross-family rigor" section:**

*Precedent scope: successful completion of the Scribe-SDK spike does NOT create a precedent for SDK adoption in other seats. Any future SDK adoption for a non-Anthropic seat (Editor, Judge, Red Team, or Scout) requires its own independent spike under TSIP, its own L-003 cross-family audit, and its own operator sign-off. "Scribe spike passed, let's do Editor next without re-audit" is explicitly prohibited. Each seat's SDK adoption carries distinct cross-family implications — no blanket approval propagates from one spike to another.*

### F-5 — Vocabulary drift enforcement (addresses RT-NEW-04 MED, applies to EN-002)

See companion EN-002 Cycle 2 note below. Summary: EN-002's mapping table gets a lint rule blocking production-code imports of SDK lifecycle event names; references to the table in prose remain fine.

### F-6 — Sovereignty test for SDK error states (addresses RT-NEW-05 LOW)

**Adds to the spike "Success metrics" list:**

*Sovereignty verification under error conditions: the spike forces the SDK into four representative error states (auth failure, timeout, invalid tool arg, network blip) and inspects outbound traffic during each. All outbound traffic must be to the pinned Anthropic API endpoint and only there. Any additional destinations (error-reporting telemetry, diagnostic uploads, usage beacons) = sovereignty violation = spike FAIL.*

### F-7 — Editor cleanups

Jargon glosses added for "deferred engineering queue entry," "time-boxed," "controlled dependency," "skills semantic dispatch," and "sdk_lifecycle_map.archive" on first use throughout EN-001 and EN-002. Amendment surface normalized to declarative present-tense; reflection moved to debate doc. "Controlled dependency" clause broken into bulleted sub-claims for readability.

## Cycle 2 status (EN-001)

- RT-NEW-01 HIGH: CLOSED (F-1 concrete rollback procedure).
- JUDGE-DISSENT MED: CLOSED (F-1 same fix).
- RT-NEW-02 MED: CLOSED (F-2 detection mechanism).
- RT-NEW-03 MED: CLOSED (F-3 LOCK-landed definition).
- RT-NEW-04 MED: CLOSED (F-5, via EN-002 companion).
- RT-NEW-06 MED: CLOSED (F-4 precedent statement).
- RT-NEW-05 LOW: CLOSED (F-6 sovereignty test).
- Editor findings: CLOSED (F-7 applied in place).

**EN-001 Cycle 2 status: READY for re-audit.** A follow-up live cross-family audit using the now-live OpenClaw path should verify the closures hold. If all three seats return READY with zero new in-scope findings, the amendment promotes `LOCKED-internal-simulated` → `LOCKED-sealed` pending operator signature.

---

## Operator Sign-off — LOCKED-sealed 2026-04-20

**Status:** `LOCKED-sealed`
**Interpretation adopted:** policy-lock (amendment seals policy; referenced scripts/tests/Logician gates are engineering queue items tracked under Da Vinci §7 + Logician v0.2 — not LOCK blockers).
**Cycle 2 re-audit outcomes:** Editor READY, Judge 100/100 PASS (reversibility recovered 14→20), Red Team REQUIRES_MINOR_FIXES with all findings re-classified under policy-lock as CLOSED-policy + 11 engineering-queue items.
**Audit trail:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/cross_family_audit_cycle2/synthesis.md`
**Operator authorization token:** Josh Inklovich, session authorization 2026-04-20. L-003 cross-family rigor honored; policy-lock interpretation operator-directed; engineering queue absorbs implementation surface.
**Cryptographic seal (Ed25519):** pending — Ed25519 operator-key infrastructure lands with v2.2 gate #5 (`F-ROLLBACK-SCRIPT-INTEGRITY`) + gate #10 (`F-ROUTER-INTEGRITY-MULTI-SOURCE`). Hash-bound authorization recorded at `pipeline/engineering/operator_authorization_ledger.v1.jsonl` with SHA3-512 of canonical amendment bytes. `LOCKED-sealed` label reflects policy-lock interpretation; promotion to cryptographic seal is a separate event when Ed25519 infrastructure lands.
**Effective:** LOCKED-sealed 2026-04-20, subject to quarterly review per TSIP Phase 7 operating discipline.
