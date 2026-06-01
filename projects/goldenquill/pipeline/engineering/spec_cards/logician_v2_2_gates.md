# Spec card — Logician v2.2 gates (amendment-policy enforcement layer)

**STATUS:** SUPERSEDED

**Round:** Logician v2.2 (8-gate extension of §4 v2.1)
**Spec-card version:** v1
**Date:** 2026-04-20
**Source amendments:** EN-001, EN-002, EN-003, TSIP v0.1 (all LOCKED-sealed 2026-04-20 under policy-lock interpretation)
**Midas dispatch handoff:** `pipeline/handoffs/midas_logician_v2_2_queue_2026-04-20.md`
**Blueprint anchor:** `pipeline/blueprint/v0.1/section_04_logician.md` (v2.1 current LOCK; v2.2 is the amendment-enforcement extension)

---

## Summary

Twelve deterministic Logician gates (eight original + three from EN-003 Cycle 4 + one from F-03 residual-gap) that mechanically enforce the four Tier 1 policy amendments plus the post-LOCK Cycle 4 tightening pass. Without these gates, the amendment policies are aspirational; with them, they are fail-closed at PRE/POST gate time. Each gate is text-defined here for the v0.2 engineering queue; implementation follows the §4 v2.1 module pattern (pure Python, no LLM, injected Protocol dependencies, ≥30 unit + ≥5 adversarial tests, ≥95% coverage, AST-lint R1–R5 clean).

Per-gate implementation spec-cards land at `pipeline/engineering/spec_cards/logician_v2_2_<gate_slug>.md` before each gate's dispatch round.

### Per-gate spec-card index

| # | Gate | Failure code | Spec card |
|---|------|-------------|-----------|
| 1 | F-BOOTSTRAP-REUSE | F-AMDT-01 | `logician_v2_2_f_bootstrap_reuse.md` |
| 2 | F-VERDICT-BLOCKING-MISSING | F-AMDT-02 | `logician_v2_2_f_verdict_blocking_missing.md` |
| 3 | F-VERDICT-CITATION-MISSING | F-AMDT-03 | `logician_v2_2_f_verdict_citation_missing.md` |
| 4 | F-SDK-PRECEDENT-REUSE | F-AMDT-04 | `logician_v2_2_f_sdk_precedent_reuse.md` |
| 5 | F-ROLLBACK-SCRIPT-INTEGRITY | F-AMDT-05 | `logician_v2_2_f_rollback_script_integrity.md` |
| 6 | F-DEPRECATION-EXEMPTION-REUSE | F-AMDT-06 | `logician_v2_2_f_deprecation_exemption_reuse.md` |
| 7 | F-AMENDMENT-SELF-REFERENCE-DETECT | F-AMDT-07 | `logician_v2_2_f_amendment_self_reference_detect.md` |
| 8 | F-COMMITTEE-DEGRADATION-TIMEOUT | F-AMDT-08 | `logician_v2_2_f_committee_degradation_timeout.md` |
| 9 | F-DEPRECATION-REGISTER-STALENESS | F-AMDT-09 | `logician_v2_2_f_deprecation_register_staleness.md` |
| 10 | F-ROUTER-INTEGRITY-MULTI-SOURCE | F-AMDT-10 | `logician_v2_2_f_router_integrity_multi_source.md` |
| 11 | F-DEGRADATION-STANZA-PRECEDENCE | F-AMDT-11 | `logician_v2_2_f_degradation_stanza_precedence.md` |
| 12 | F-DAILY-LOG-LOCK-BLOCK-MISSING | F-AMDT-12 | `logician_v2_2_f_daily_log_lock_block_missing.md` |

All paths relative to `pipeline/engineering/spec_cards/`.

### Cycle 4 additions (2026-04-20)

Gates #9–#11 + the v1.1 extension of gate #7 absorb EN-003 Cycle 4 Red Team findings C4-NEW-01 through C4-NEW-04 per operator disposition (Option 2: park to v2.2 queue). Text-level closure hit the L-005 ceiling after Cycle 3→4 each generated sub-findings; remaining work is mechanical enforcement. See each new gate's spec card for finding origin and threat model. Gate #7 (F-AMENDMENT-SELF-REFERENCE-DETECT) extended to v1.1 to cover C4-NEW-04 author-family anti-collision across the full Code Thesis Committee family set.

---

## Gate inventory

### 1. `F-BOOTSTRAP-REUSE`

**Origin:** TSIP v0.1 F-1
**Kind:** POST-gate on LOCK-sealed write
**Spec:** The TSIP bootstrap exception must fire exactly once across the lock_history.v1.jsonl lifetime. Gate reads the full JSONL for rows with `bootstrap_exception: true`. If count > 1, gate DENY with F-BOOTSTRAP-REUSE. Fail-closed: on JSONL read failure, DENY.
**Closes:** prevents TSIP bootstrap framing from being reused as a blanket exception for subsequent amendments that do not meet bootstrap criteria.

---

### 2. `F-VERDICT-BLOCKING-MISSING`

**Origin:** TSIP v0.1 F-5
**Kind:** POST-gate on reviewer-verdict ingest
**Spec:** Every reviewer verdict ingested into the pipeline must contain a strict-boolean `blocking` field (JSON `true` or `false`, not a string or null). Gate parses the raw verdict JSON; if `blocking` key is absent or non-boolean, DENY with F-VERDICT-BLOCKING-MISSING. Applies to all seat verdicts (Editor, Judge, Red Team).
**Closes:** prevents ambiguous or unstructured reviewer outputs from being promoted as valid verdicts.

---

### 3. `F-VERDICT-CITATION-MISSING`

**Origin:** TSIP v0.1 Judge-citation-validation derivative
**Kind:** POST-gate on Judge verdict ingest
**Spec:** Each per-dimension scoring entry in a Judge verdict must contain an evidence-string citation that resolves against the draft under review. Gate tokenizes each `evidence:` field in the Judge verdict and confirms each token appears verbatim in the draft text (§4 v2.1 `source_tag_verify` infrastructure reused). Missing or non-resolving citation → DENY with F-VERDICT-CITATION-MISSING.
**Closes:** prevents Judge scores from floating free of the draft content, which would allow arbitrary scores with fabricated citations.

---

### 4. `F-SDK-PRECEDENT-REUSE`

**Origin:** EN-001 RT-NEW-06
**Kind:** PRE-gate on new-seat Agent-SDK-adoption amendment
**Spec:** Any amendment that adopts the Agent SDK for a seat beyond the Scribe Phase-0 spike must present per-seat audit evidence distinct from the Scribe spike. Gate reads the amendment frontmatter for `adopts_agent_sdk: true` + `seat:` fields, then scans lock_history.v1.jsonl for prior SDK-adoption rows. If a prior row exists for a different seat, the gate checks that the new amendment's `audit_evidence_path` is a distinct file (not the same path as any prior adoption's evidence). Reuse of the same evidence path → DENY with F-SDK-PRECEDENT-REUSE.
**Closes:** prevents one-seat Agent SDK audit from being treated as a blanket approval for multi-seat adoption without per-seat review.

---

### 5. `F-ROLLBACK-SCRIPT-INTEGRITY`

**Origin:** EN-001 RT-NEW-01 follow-through
**Kind:** PRE-gate on rollback-script execution
**Spec:** Any execution of `spike_rollback.sh` (or a script registered in the rollback_scripts manifest) must pass two checks: (a) Ed25519 signature over script bytes verifies against the pinned public key stored in the sovereignty envelope; (b) the JSONL ledger hash at the ledger head matches the script's `ledger_hash_at_pin` metadata field. Either check failure → DENY with F-ROLLBACK-SCRIPT-INTEGRITY. Uses §2 Round M `crypto_primitives` if available; falls back to stdlib Ed25519 per E-011.
**Closes:** prevents a tampered rollback script from being executed under the authority of the original script's audit evidence.

---

### 6. `F-DEPRECATION-EXEMPTION-REUSE`

**Origin:** EN-003 F-1-Cycle3
**Kind:** PRE-gate on amendment with `amendment.forced_replacement: true`
**Spec:** When an amendment sets `amendment.forced_replacement: true`, the gate verifies two fields before promotion to LOCKED-sealed: (a) a live cross-family audit artifact exists at the canonical path specified by `amendment.audit_artifact_path`; (b) that artifact's final Red Team verdict is `blocking: false` OR the artifact contains an explicit Cycle N fix section addressing each blocking finding with closure evidence. Either field absent or failing → DENY with F-DEPRECATION-EXEMPTION-REUSE. Gate fails closed on any file-read error.
**Closes:** ensures that "forced by deprecation" is never used as a bypass for the L-005 cross-family review obligation; the deprecation event triggers the amendment but cannot pre-approve the replacement.

---

### 7. `F-AMENDMENT-SELF-REFERENCE-DETECT`

**Origin:** EN-003 F-4-Cycle3
**Kind:** PRE-gate on amendment with `modifies_committee: true`
**Spec:** Fires when ALL THREE conditions hold: (a) amendment frontmatter sets `modifies_committee: true`; (b) the `added_reviewer_family` field in the amendment matches the `judge_primary_family` field read from `router.yaml` at PRE-gate time; (c) the amendment `author_family` field ≠ the `judge_primary_family`. When all three hold AND the amendment does NOT also set `judge_reassigned_to:` a non-self-referencing family, gate DENY with F-AMENDMENT-SELF-REFERENCE-DETECT. Fails closed on ambiguity (missing fields, router.yaml unreadable). False-negatives logged to lessons.md as recurring-pattern candidates.
**Closes:** ensures that any amendment adding the active Judge's model family to a governed committee triggers mandatory Judge reassignment to a non-self-referencing reviewer, making the protocol structural rather than procedural.

---

### 8. `F-COMMITTEE-DEGRADATION-TIMEOUT`

**Origin:** EN-003 F-6-Cycle3
**Kind:** Time-triggered gate reading `deprecation_amendment.locked_at_iso8601` vs current clock
**Spec:** When a deprecation-triggered replacement Thesis is in progress (a prior LOCKED-sealed deprecation amendment exists in lock_history.v1.jsonl with `deprecation_triggered_replacement: true`), the gate reads `locked_at_iso8601` from that row and computes days elapsed against the injected clock. Three thresholds — **all inline-literal `Final[int]` with rebind-resistance tests, NOT module-level constants**:
- Days 0–13: PASS (no action)
- Days 14–29: PASS with WARN emitted to `pipeline/metrics/session_log.jsonl` (`event: "F-AMDT-08-WARN"`)
- Days 30–59: DENY with `F-AMDT-08-SUSPEND` — no new code LOCKs may promote; operator escalation required; escalation procedure: entry written to `daily_logs/YYYY-MM-DD.md` with explicit acknowledgment + commitment to target date or immediate dispatch
- Days ≥ 60: DENY with `F-AMDT-08-ESCALATE` — mandatory operator escalation; fresh architectural Thesis required; piecemeal replacement no longer permitted

Gate re-evaluates after operator sign-off entry exists at `daily_logs/` (injected `DailyLogReaderCallable`). Injected Protocols: `ClockProtocol` (pattern: §5 Round 2 `state_checkpoint.py`), `DailyLogReaderCallable`, `LockHistoryReaderCallable`.
**Closes:** ensures Committee degradation from 5-family to 4-family all-pass review cannot persist indefinitely; hard ceiling prevents silent architectural erosion from a provider deprecation event.

---

## Implementation constraints (non-negotiable)

- **V1 discipline on all inline thresholds.** Any time-bound constants (e.g., F-COMMITTEE-DEGRADATION-TIMEOUT 14/30/60-day ceilings, see midas handoff for gate #8) must be inline-literal RHS with rebind-resistance tests (pattern: `state_checkpoint.py` `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS`).
- **Injected-callable Protocols for time, file, crypto.** Do not import stdlib directly where a Protocol can be injected (E-017 pattern).
- **AST-lint R1–R5 clean at module load.**
- **Test budget: ≥30 unit + ≥5 adversarial per gate.**
- **E-023 closure pattern.** Isomorphic-to-deferred-scope findings remediated via `test_adv_*` + Threat-model docstring, not re-dispatch. Third firing of E-023 → elevate to spec-card-template clause.
- **Failure-code taxonomy prefix.** Propose `F-AMDT-*` or `F-PROT-*` prefix per gate in each per-gate spec-card to maintain lexical separation from the §4 v2.1 30 failure codes.

## Implementation ordering

Per midas handoff (parallelizable after per-gate spec-cards land):

- **Wave 1 (no external deps):** F-VERDICT-BLOCKING-MISSING, F-VERDICT-CITATION-MISSING
- **Wave 2 (reads lock_history.v1.jsonl + daily_logs):** F-BOOTSTRAP-REUSE, F-DEPRECATION-EXEMPTION-REUSE, F-AMENDMENT-SELF-REFERENCE-DETECT (v1 + v1.1 extension), F-DAILY-LOG-LOCK-BLOCK-MISSING
- **Wave 3 (external state):** F-ROLLBACK-SCRIPT-INTEGRITY (Ed25519 + HMAC-SHA3-512), F-COMMITTEE-DEGRADATION-TIMEOUT (ClockProtocol + DailyLogReader), F-DEPRECATION-REGISTER-STALENESS (ClockProtocol + feed-reader), F-ROUTER-INTEGRITY-MULTI-SOURCE (Ed25519 + external manifest), F-DEGRADATION-STANZA-PRECEDENCE (stanza-reader + lock_history + Ed25519)
- **Wave 4 (cross-amendment semantics):** F-SDK-PRECEDENT-REUSE

## Done definition (v2.2 milestone)

1. Per-gate spec-cards written + operator-reviewed for all 8 gates listed above.
2. All 8 gates implemented: ≥30 unit + ≥5 adversarial tests each, ≥95% coverage, AST-lint clean.
3. §4 v2.2 blueprint amendment drafted covering the 8 new failure-code rows; cross-family audit per TSIP Phase 3.
4. `pipeline/engineering/lock_history.v1.jsonl` LOCK row per gate.
5. Cumulative pytest green at each gate LOCK.
6. MEMORY.md index updated per gate LOCK.

---

*Spec card v1 — 2026-04-20 — backlog queue for Logician v2.2 implementation dispatch.*
*Spec card v1.1 — 2026-04-20 — gate #8 F-COMMITTEE-DEGRADATION-TIMEOUT added (from EN-003 F-6-Cycle3); summary updated 7→8; Wave 3 + done-definition updated to reflect 8 gates.*
*Spec card v1.2 — 2026-04-20 — EN-003 Cycle 4 closure: gates #9 (F-DEPRECATION-REGISTER-STALENESS), #10 (F-ROUTER-INTEGRITY-MULTI-SOURCE), #11 (F-DEGRADATION-STANZA-PRECEDENCE) added from C4-NEW-01/02/03; gate #7 extended to v1.1 covering C4-NEW-04 author-family anti-collision. Summary updated 8→11 + extension. EN-003 LOCK stands; Cycle 4 findings absorbed as structural enforcement rather than prose iteration (L-005 ceiling respected).*
*Spec card v1.3 — 2026-04-20 — gate #12 F-DAILY-LOG-LOCK-BLOCK-MISSING added from F-03 backfill residual-gap flag (authoring-discipline gap: 44-module telemetry gap recovered via backfill, but discipline requires mechanical enforcement). Wave 2 expanded to include daily_logs reader. Summary updated 11→12.*
