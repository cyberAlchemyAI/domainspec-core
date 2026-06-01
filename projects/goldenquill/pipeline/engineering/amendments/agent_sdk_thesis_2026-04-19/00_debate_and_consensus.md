# Agent SDK Amendment — Thesis Debate + Consensus

**Date:** 2026-04-19
**Scope:** Decide what, if anything, Tilth adopts from the Claude Agent SDK after the exploration in `pipeline/engineering/agent_sdk_exploration.md`.
**Audit cycle:** L-005 strict two-cycle. Simulated (single-family voice); not a substitute for live cross-family review.
**Status:** `LOCKED-internal-simulated` pending operator sign-off and live cross-family re-audit.
**Outcome artifacts:**
- `EN-001_sdk_scribe_spike_2026-04-19.md` (engineering queue entry, deferred)
- `EN-002_sdk_lifecycle_vocabulary_2026-04-19.md` (documentation hygiene, immediate)
- `pipeline/engineering/references/sdk_lifecycle_map.md` (EN-002 content)

---

## Draft v1 — Initial Amendment

Two changes proposed:

**A. Scribe-via-Agent-SDK spike** — autonomous section drafting using the SDK's generic runtime. Scribe's primary is already `anthropic/claude-sonnet-4-6`; no LiteLLM translation layer required. SDK hooks (PreToolUse/PostToolUse) enforce Law 3 and KGIE. Rejection criteria if tool-use reliability or sovereignty compromised.

**B. Lifecycle vocabulary alignment** — add a cross-reference table mapping Tilth's F-codes and P-surfaces to the SDK's ten lifecycle event names. Zero semantic change. Portability reference only.

---

## Cycle 1 — DRIVER (per-seat audit)

### Scout (citation discipline)

REQUIRES_MINOR_FIXES.

- Claim "tool-use reliability < 95%" is unsourced. If it's a proposed threshold, declare it as such. If borrowed from a benchmark, cite the benchmark URL + SDK version + date.
- The SDK version at spike-start must be pinned. Without a pin, `router.yaml` and spike artifacts drift. Add requirement: `pipeline/engineering/agent_sdk_spike_manifest.yaml` with SDK version hash at spike-open.
- Document B's mapping table must name the SDK version it's mapped against. The "Claude Code SDK → Claude Agent SDK" rename of 2025 shows this vocabulary already drifts.

### Scribe (one voice, no fabrication)

REQUIRES_MINOR_FIXES.

- A and B are different artifacts with different timelines. A is gated on multiple preconditions; B is immediate. Don't bundle them in one amendment. Split.
- Draft v1 mixes past-tense reflection ("I oversold it") with present-tense amendment language. Amendment text is present-tense-only, declarative. Strip the reflection from the amendment surface; keep it in the debate doc.
- No new fabricated capabilities — existing Scribe capabilities from `section_02` and `router.yaml` are preserved verbatim.

### Editor (clarity, accessibility)

REQUIRES_MINOR_FIXES.

- "Lifecycle vocabulary alignment" is jargon. Plain: *if Tilth ever needs to interoperate with the SDK or another generic agent runtime, we need a translation table so the same event is called the same thing.*
- "Tool-use reliability" needs one-line definition at first use: *the agent successfully calls the right tool with the right arguments and processes the result correctly.*
- "Spike" needs one-line gloss: *time-boxed engineering experiment that produces evidence, not committed code.*
- Rephrase "controlled dependency" → *external library whose API we do not control; we pin its version and review changes on each bump.*

### Judge (rubric scoring, SFR format)

PASS with findings. 88/100 on engineering-amendment rubric.

**Premises cited:**
- P1: `pipeline/engineering/agent_sdk_exploration.md` §3 — SDK is ~150 MB Python, fits 8GB M1.
- P2: `router.yaml` lines 30–34 — Scribe primary = `anthropic/claude-sonnet-4-6`, already native SDK target.
- P3: `CLAUDE.md` "Sovereignty Promise" — nothing phones home.
- P4: `/AGENTS.md` L-003 — cross-family review discipline; SDK is Anthropic-only natively.
- P5: `pipeline/engineering/da_vinci_engineer_prompt_v2.md` §7 — engineering queue prioritizes scope-close backfills, §6 Operating Envelope, §4 v2.2, §0.5 v4 refresh.

**Execution trace:**
- P1 + P2 ⟹ Scribe spike has no LiteLLM dependency, lowest friction SDK adoption point (score dim: scope clarity 18/20).
- P3 + SDK-is-local-library ⟹ BYOK posture preserved in spike (score dim: sovereignty 18/20 — 2 pts deducted for controlled-dependency surface-area risk).
- P4 + SDK-is-Anthropic-native ⟹ Scribe spike does not violate cross-family (Scribe is already Anthropic); other seats would (score dim: cross-family rigor 20/20).
- P5 + spike competes with prioritized queue work ⟹ spike must be explicitly deferred, not jump the queue (score dim: reversibility / sequencing 16/20).
- Missing: explicit F-code deferral language for PRE/POST hooks in spike (score dim: Cedar/Logician integration 16/20).

**Conclusion:** Draft v1 survives structurally. Fixable gaps: sequencing, F-code deferral, controlled-dependency risk statement.

### Logician (deterministic, fail-closed, Cedar-compatible)

PRE-gate check:

- F-codes introduced by amendment A? **None in draft v1.** Either define them now (F-SCRIBE-SPIKE-TOOLUSE-LEAK, F-SCRIBE-SPIKE-KGIE-FAIL) or defer explicitly to spike charter. Silent deferral = fail-closed trigger. **FIX: declare deferral explicitly.**
- Cedar rule changes? **None.** Pass.
- Amendment B zero-code? **Yes.** Pass.
- Does amendment A propose `canUseTool` displacing Cedar? **No — rejected in prior turn.** Pass.
- Does amendment A propose SDK-level permission modes displacing operational gears? **No.** Pass.
- Does amendment A propose subagent-dispatch displacing `router.yaml`? **No.** Pass.

**One REQUIRES_FIX:** F-code deferral language.

### Red Team (adversarial, cross-family)

5 findings: 1 HIGH, 3 MED, 1 LOW. SFR format.

**RT-A-01 HIGH — Reversibility / exit criteria.** Draft v1 says "roll back if criteria violated" without defining rollback. Mitigation required: spike runs on a branch; no persistent state in SDK-only format; baseline Scribe code preserved verbatim; abandonment = revert branch + zero-state migration. **REQUIRES_FIX.**

**RT-A-02 MED — Premature optimization / queue jump.** Da Vinci §7 engineering queue has priority items already. The spike competes with scope-close backfills for operator review bandwidth. **REQUIRES_FIX:** explicit queue position — "queued behind §6 Operating Envelope blueprint LOCK, §4 Logician v2.2 LOCK, §0.5 v4 refresh, real-engineer validator gate per Da Vinci §13."

**RT-A-03 MED — Vendor lock-in surface area.** The SDK is an Anthropic-controlled library. Claude Code SDK → Claude Agent SDK rename proves it drifts. Tilth's sovereignty promise ("Nothing phones home") is not violated — the SDK is a local Python library — but the API surface is externally controlled. **REQUIRES_FIX:** declare SDK as *external controlled dependency*, version-pinned, reviewed on each minor-version bump, exit criteria documented.

**RT-B-01 MED — Vocabulary mapping staleness.** Amendment B's table goes stale on SDK minor-version bumps. **REQUIRES_FIX:** table version-pinned to SDK version X.Y.Z at write-time; refresh-on-minor-bump policy stated; treated as snapshot, not live mapping.

**RT-A-04 LOW — Threshold sourcing.** "Tool-use reliability < 95%" is either a published benchmark or an invented threshold. If invented, declare it spike-specific and measured in-spike against Tilth's own vault schema, not inherited.

### Summary of Cycle 1 findings

| Seat | Verdict | Findings |
|------|---------|----------|
| Scout | REQUIRES_MINOR_FIXES | 2 documentary (citation pinning) |
| Scribe | REQUIRES_MINOR_FIXES | 1 structural (split), 1 voice (strip reflection) |
| Editor | REQUIRES_MINOR_FIXES | 3 jargon glosses |
| Judge | PASS with findings | 88/100, 2 dimensions < 20 |
| Logician | REQUIRES_FIX | 1 (F-code deferral language) |
| Red Team | REQUIRES_MINOR_FIXES | 1 HIGH + 3 MED + 1 LOW |

No BLOCKING findings. Proposal survives. Fixable in Cycle 1 → Cycle 2.

---

## Synthesis — Consensus Revisions

1. **Split into EN-001 and EN-002.** Different timelines, different precondition sets.
2. **EN-001 explicitly deferred** behind §6 Operating Envelope blueprint LOCK, §4 Logician v2.2 LOCK, §0.5 v4 refresh, real-engineer validator gate (Da Vinci §13). Not on current queue.
3. **EN-001 defines rollback procedure** — spike on branch, no state persisted in SDK-only format, baseline preserved, abandonment = branch revert.
4. **EN-001 declares SDK as external controlled dependency** — version-pinned, reviewed on minor-bump, audit quarterly.
5. **EN-001 defers F-code definition** to spike charter at spike-open — explicit, not silent.
6. **EN-001 threshold sourcing** — all thresholds declared spike-specific, measured in-spike, not inherited.
7. **EN-002 version-pins** the mapping table to SDK version + date; refresh-on-minor-bump policy stated.
8. **EN-002 plain-English** rephrase per Editor findings.
9. **Both amendments** strip reflective voice from amendment surface (stay in this debate doc only).
10. **Explicit rejections captured** (patterns proposed in exploration that do NOT survive):
    - `canUseTool` displacing Cedar — REJECT (Cedar is declarative and verifiable; `canUseTool` is imperative escape hatch)
    - Skills semantic dispatch displacing `router.yaml` — REJECT (non-determinism breaks audit chain)
    - MCP channels for Scout at v0.1 — DEFER (v0.2+ federation concern)
    - Permission modes as operational-gears rename — REJECT (different axes)
    - SDK auto-reload replacing A4 prompt placement — REJECT (different failure modes; they compound, don't substitute)
    - Subagent isolation displacing Cedar Law 3 enforcement — REJECT (Cedar is primary; subagent isolation is complementary at best)
    - `session_id` as primary state handle — REJECT (A7 signed calibration artifact is a richer superset)

---

## Cycle 2 — VERIFICATION

### Scout
- Citations now pinned: SDK version required in spike manifest, mapping table version-pinned. **READY.**

### Scribe
- Split into EN-001 + EN-002. Amendment text is declarative, present-tense. Reflection in debate doc only. **READY.**

### Editor
- Plain-English glosses added for spike, tool-use reliability, controlled dependency. **READY.**

### Judge
- Re-score engineering-amendment rubric: 96/100.
  - Scope clarity: 20/20 (split + explicit queue position)
  - Reversibility: 19/20 (rollback procedure defined)
  - Cross-family rigor: 20/20 (unchanged)
  - Cedar/Logician: 19/20 (F-code deferral explicit)
  - Sovereignty: 18/20 (controlled-dependency risk acknowledged but inherent)
- PASS. ready_to_lock=true. **READY.**

### Logician
- F-code deferral now explicit. No silent additions. No Cedar rule changes. **READY.**

### Red Team
- RT-A-01 HIGH — CLOSED (rollback defined).
- RT-A-02 MED — CLOSED (queue position explicit).
- RT-A-03 MED — CLOSED (controlled-dependency declaration).
- RT-B-01 MED — CLOSED (version-pin + refresh policy).
- RT-A-04 LOW — CLOSED (spike-specific thresholds declared).
- Zero in-scope remaining. **READY.**

### Cycle 2 outcome

All six reviewers READY. L-005 two-cycle bar met.

**Status:** `LOCKED-internal-simulated`. Not `LOCKED-sealed` — Josh's operator sign-off and a live cross-family re-audit are the promotion gates.

---

## Implementation

Files written this turn:

1. `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/00_debate_and_consensus.md` — this file (the audit trail).
2. `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-001_sdk_scribe_spike_2026-04-19.md` — deferred engineering queue entry for the Scribe SDK spike.
3. `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-002_sdk_lifecycle_vocabulary_2026-04-19.md` — documentation hygiene amendment.
4. `pipeline/engineering/references/sdk_lifecycle_map.md` — the version-pinned mapping table (EN-002 content).

Pointer added to `pipeline/engineering/agent_sdk_exploration.md` §6 (footer) referencing this debate and the two amendments.

## Da Vinci engineering queue impact

EN-001 is queue position N+4 (after §6 blueprint LOCK, §4 v2.2 LOCK, §0.5 v4 refresh, real-engineer validator gate). Zero current-turn code written.
EN-002 is immediate zero-code. Adds one reference file. No test impact.
