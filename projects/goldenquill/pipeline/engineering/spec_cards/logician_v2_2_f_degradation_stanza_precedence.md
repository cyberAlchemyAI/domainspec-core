# Spec card — Logician gate F-DEGRADATION-STANZA-PRECEDENCE (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit_cycle4/red_team_verdict.md` — EN-003 Cycle 4 C4-NEW-03
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #11
- Closely coupled gate: `logician_v2_2_f_committee_degradation_timeout.md` (gate #8, F-AMDT-08)

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 3 (external state: amendment frontmatter + lock_history + daily_logs)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-11`

---

## Gate name and failure code

- **Gate:** `F-DEGRADATION-STANZA-PRECEDENCE`
- **Failure codes:** `F-AMDT-11-PRECEDENCE` (stanza conflict), `F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION` (architectural-Thesis LOCK carve-out misuse)
- **Kind:** PRE-gate on operator-sign-off stanza AND PRE-gate on code-LOCK promotion under READ-ONLY

## Purpose

C4-NEW-03 (EN-003 Cycle 4 Red Team) has two teeth:

**Tooth (a) — stanza precedence:** When an operator sign-off stanza for F-AMDT-08 (Committee-Degradation-Timeout) contains BOTH a `TARGET_DATE` and a `FRESH_ARCHITECTURAL_THESIS` directive, there is no rule specifying which takes precedence. Ambiguous stanza → gate behavior is undefined.

**Tooth (b) — READ-ONLY deadlock:** The F-AMDT-08 ESCALATE tier requires a fresh architectural Thesis to exit READ-ONLY. But sealing a fresh Thesis is itself a LOCK operation, and READ-ONLY blocks LOCK promotions. The exit condition is self-referentially impossible — classic deadlock.

This gate resolves both mechanically:

**Tooth (a) resolution:** enforce precedence rule `FRESH_ARCHITECTURAL_THESIS` > `TARGET_DATE` (mixed stanza treated as FRESH_ARCHITECTURAL_THESIS; TARGET_DATE ignored, warning emitted).

**Tooth (b) resolution:** carve out a narrow LOCK class — **architectural-Thesis LOCKs** — that is explicitly exempt from code-LOCK READ-ONLY. Architectural-Thesis LOCK is identified by:
- `lock_history.v1.jsonl` row with `lock_class: "architectural_thesis"`
- Operator-signed (Ed25519 operator key signature in the row)
- Targets an architecture-file path (`pipeline/architecture/v0.1/tilth_architecture_locked_v*.md` or an `architecture_v*_amendment.md`)

Code-LOCKs (`lock_class: "code"` or unset) remain subject to READ-ONLY. Architectural-Thesis LOCKs bypass it. Deadlock broken.

## Trigger condition

Fires on TWO distinct events:

**Event 1 (tooth a):** Any operator sign-off stanza written to `daily_logs/YYYY-MM-DD.md` for F-AMDT-08. Gate parses stanza content before F-AMDT-08 re-evaluates.

**Event 2 (tooth b):** Any code-LOCK promotion attempt while F-AMDT-08 is in SUSPEND or ESCALATE tier. Gate verifies whether the staged row is an architectural-Thesis LOCK (bypass eligible) or a code-LOCK (subject to READ-ONLY).

## Input contract

```python
@runtime_checkable
class StanzaReaderCallable(Protocol):
    def __call__(self, date_iso: str) -> str | None: ...  # returns F-AMDT-08 stanza text

@runtime_checkable
class LockHistoryReaderCallable(Protocol):
    def __call__(self) -> list[dict]: ...

@runtime_checkable
class SignatureVerifyCallable(Protocol):
    def __call__(self, row_bytes: bytes, signature: bytes, public_key: bytes) -> bool: ...
```

- `stanza_reader: StanzaReaderCallable` — returns F-AMDT-08 stanza text from today's daily log, or None.
- `lock_history_reader: LockHistoryReaderCallable` — returns parsed lock_history rows.
- `signature_verify: SignatureVerifyCallable` — injected Ed25519 verifier (shared with gates #5, #10).
- `operator_public_key: bytes` — pinned operator Ed25519 public key from sovereignty envelope.
- `staged_row: dict` — the row about to be committed (for Event 2).
- `event_kind: Literal["stanza_check", "lock_promotion_under_readonly"]` — which event triggered the gate.

## Pass/fail criteria — Tooth (a), Event 1 (stanza precedence)

1. Read stanza text via `stanza_reader(today_iso)`. If absent → no-op PASS (no stanza, nothing to check).
2. Parse stanza for presence of directive tokens:
   - `TARGET_DATE: {YYYY-MM-DD}` (per F-AMDT-08 sentinel schema)
   - `FRESH_ARCHITECTURAL_THESIS` (boolean directive)
3. **Precedence rule:**
   - Only `FRESH_ARCHITECTURAL_THESIS` present → PASS; stanza valid; F-AMDT-08 treats as ESCALATE-tier resolution.
   - Only `TARGET_DATE` present → PASS; stanza valid; F-AMDT-08 treats as SUSPEND-tier resolution.
   - Both present → PASS with `event: "F-AMDT-11-PRECEDENCE-MIXED"` emitted to session_log. F-AMDT-08 treats stanza as FRESH_ARCHITECTURAL_THESIS (the stronger directive wins); TARGET_DATE ignored.
   - Neither present → FAIL `F-AMDT-11-PRECEDENCE-EMPTY` — stanza is malformed (no valid directive).

## Pass/fail criteria — Tooth (b), Event 2 (READ-ONLY carve-out)

1. Confirm F-AMDT-08 is in SUSPEND or ESCALATE tier (verified by F-AMDT-08's own evaluation; this gate trusts F-AMDT-08's state). If not → no-op PASS.
2. Extract `lock_class` from `staged_row`. If missing or `"code"` → subject to READ-ONLY → DENY with `F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION` (pass-through — F-AMDT-08 owns the SUSPEND/ESCALATE denial; this gate is the carve-out determinator).
3. If `lock_class == "architectural_thesis"`:
   a. Verify `staged_row` targets an architecture-file path (regex: `^pipeline/architecture/v[0-9]+/(tilth_architecture_locked_v.*\.md|architecture_v.*_amendment\.md)$`). If not → FAIL `F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION` (wrong target path for architectural class).
   b. Verify operator signature over the row bytes using `signature_verify` + `operator_public_key`. If signature absent or invalid → FAIL `F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION`.
   c. All checks pass → **PASS with carve-out** — F-AMDT-08 is instructed to allow this specific LOCK through. Emit `event: "F-AMDT-11-CARVEOUT-GRANTED"` to session_log for audit.
4. **FAIL-CLOSED:** any injected callable raises → DENY with `event: "F-AMDT-11-READER-FAIL"`.

## Failure behavior

**Tooth (a) failures:**
- `F-AMDT-11-PRECEDENCE-EMPTY`: stanza is malformed. F-AMDT-08 does NOT unblock; operator must rewrite stanza.

**Tooth (b) failures:**
- `F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION`: staged row claims architectural-Thesis class but fails one of: target-path check, operator signature check. DENY the LOCK; READ-ONLY stands.

All failures emit structured records to `pipeline/metrics/session_log.jsonl` with full context for operator review.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- Precedence rule (FRESH_ARCHITECTURAL_THESIS > TARGET_DATE) is inline-literal enumeration in the gate, NOT a module-level constant. Change requires v2.3 amendment + new gate version.
- Carve-out target-path regex is inline-literal, rebind-resistance tested.
- Shared Ed25519 `SignatureVerifyCallable` Protocol with gates #5, #10.
- Gate is stateless — each invocation re-reads stanza and/or lock_history fresh. No caching.
- Lives at `pipeline/logician/gates/f_degradation_stanza_precedence.py`.
- AST-lint R1–R5 clean at module load.
- Wave 3 because it depends on external state (daily logs + lock_history + operator signature).
- **Coordination with F-AMDT-08:** This gate is a sibling to F-AMDT-08, not a replacement. F-AMDT-08 owns the day-count logic and SUSPEND/ESCALATE denial; F-AMDT-11 owns the precedence rule for stanza parsing AND the carve-out determination for architectural-Thesis LOCKs. Cross-reference in F-AMDT-08 gate implementation to call F-AMDT-11 at the two trigger points.

## Test criteria

### Unit tests (≥40 — two teeth, two event paths)

**Tooth (a) stanza precedence (≥18):**
- Stanza absent → no-op PASS.
- Stanza has only FRESH_ARCHITECTURAL_THESIS → PASS, no emission.
- Stanza has only TARGET_DATE (valid future date) → PASS, no emission.
- Stanza has both → PASS with `F-AMDT-11-PRECEDENCE-MIXED` emission; F-AMDT-08 directed to treat as FRESH.
- Stanza has neither → FAIL `F-AMDT-11-PRECEDENCE-EMPTY`.
- Stanza has FRESH_ARCHITECTURAL_THESIS plus noise text → PASS (tolerant of surrounding prose).
- Parametrized: TARGET_DATE with various valid/invalid ISO formats → F-AMDT-08 handles date validity; this gate only checks directive presence.

**Tooth (b) READ-ONLY carve-out (≥22):**
- F-AMDT-08 in PASS tier → no-op PASS (gate not triggered).
- F-AMDT-08 in WARN tier → no-op PASS.
- F-AMDT-08 in SUSPEND, staged_row is `lock_class: "code"` → DENY carve-out-violation (code LOCK under SUSPEND, expected).
- F-AMDT-08 in SUSPEND, staged_row is `lock_class: "architectural_thesis"`, valid path, valid signature → PASS carve-out-granted.
- F-AMDT-08 in SUSPEND, `lock_class: "architectural_thesis"`, path is code file (not architecture) → FAIL carve-out-violation.
- F-AMDT-08 in SUSPEND, `lock_class: "architectural_thesis"`, valid path, signature absent → FAIL carve-out-violation.
- F-AMDT-08 in SUSPEND, `lock_class: "architectural_thesis"`, valid path, signature invalid → FAIL carve-out-violation.
- F-AMDT-08 in ESCALATE, architectural-Thesis LOCK valid → PASS (ESCALATE deadlock broken).
- F-AMDT-08 in ESCALATE, code LOCK → DENY.
- Parametrized over architecture-file paths: v0.1, v0.2, amendments.
- Parametrized over lock_class values: `"code"`, `"architectural_thesis"`, `"vault"`, unset → only `"architectural_thesis"` eligible for carve-out.

### Adversarial tests (≥8)

- `test_adv_stanza_reader_raises` → DENY fail-closed.
- `test_adv_lock_history_reader_raises` → DENY fail-closed.
- `test_adv_signature_verify_raises` → DENY fail-closed.
- `test_adv_architectural_thesis_claim_but_code_path` — adversary spoofs `lock_class: "architectural_thesis"` but targets a code module → FAIL carve-out-violation (path check catches).
- `test_adv_signature_valid_but_for_different_row_bytes` — signature verifies over different payload → FAIL carve-out-violation.
- `test_adv_precedence_rule_rebind_attempt` — attempt to rebind the precedence-enumeration in module namespace → module-load invariant holds.
- `test_adv_architecture_path_regex_rebind_at_module_load` — rebind of path regex constant → rebind-resistance test holds.
- `test_adv_stanza_has_both_with_malformed_target_date` — stanza has FRESH_ARCHITECTURAL_THESIS AND a malformed TARGET_DATE → PASS (mixed rule; FRESH wins; malformed TARGET_DATE is irrelevant since ignored).

## Dependencies

- F-AMDT-08 (gate #8) for tier-state coordination.
- Ed25519 signature Protocol (shared with #5, #10).
- Operator Ed25519 public key pinned in sovereignty envelope.
- `lock_history.v1.jsonl` schema extended with `lock_class` field — **schema extension required**. Backfill: existing rows default to `lock_class: "code"`.
- §4 v2.1 gate infrastructure.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_degradation_stanza_precedence.py` |
| Tests | `tests/logician/gates/test_f_degradation_stanza_precedence.py` + `tests/logician/gates/test_adv_f_degradation_stanza_precedence.py` |
| Lock history schema | Add `lock_class: Literal["code", "architectural_thesis", "vault"]` field; backfill existing rows as `"code"` |
| F-AMDT-08 coordination | Update `f_committee_degradation_timeout.py` to call F-AMDT-11 at stanza-parse and lock-promotion trigger points |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-DEGRADATION-STANZA-PRECEDENCE"`, `failure_code: "F-AMDT-11"` |
| Blueprint amendment | §4 v2.2 blueprint delta rows for F-AMDT-11-PRECEDENCE, F-AMDT-11-PRECEDENCE-EMPTY, F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION |
| Memory | MEMORY.md index entry |

## Origin

EN-003 Cycle 4 Red Team Finding C4-NEW-03: two teeth — (a) missing stanza precedence rule, (b) READ-ONLY deadlock. Both text-level-ambiguous; structural resolution via mechanical precedence enforcement + architectural-Thesis LOCK carve-out breaks the deadlock without requiring a fresh architectural Thesis round. Option 3 (fresh Thesis) is avoided by encoding the distinction between code-LOCK and architectural-Thesis-LOCK directly in gate code.

---

*Spec card v1 — 2026-04-20 — new gate from EN-003 Cycle 4 C4-NEW-03 parked to v2.2 queue per operator disposition. Resolves the READ-ONLY deadlock in gate code, avoiding a fresh architectural Thesis round.*
