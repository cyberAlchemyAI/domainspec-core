# Spec card — Logician gate F-DAILY-LOG-LOCK-BLOCK-MISSING (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- Codebase alignment audit 2026-04-20 F-03 (backfill revealed 44-module authoring-discipline gap)
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #12
- Residual-gap flag: Josh 2026-04-20 — "backfilling telemetry doesn't fix the authoring discipline that caused the gap"

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 2 (reads daily_logs + lock_history)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-12`

---

## Gate name and failure code

- **Gate:** `F-DAILY-LOG-LOCK-BLOCK-MISSING`
- **Failure codes:** `F-AMDT-12-MISSING` (no block found), `F-AMDT-12-MALFORMED` (block present but missing required fields)
- **Kind:** POST-gate on `lock_history.v1.jsonl` append

## Purpose

The F-03 backfill incident (2026-04-20, 44 modules recovered) proved that authoring discipline alone does not produce reliable LOCK telemetry. Sessions LOCKed modules and wrote aggregate "Module(s):" lines in daily logs but did not write per-module LOCK blocks at the moment of LOCK, leaving downstream auditors (and Group 10 outside review) without an authoritative record of what was locked when, by whom, with what verdict. This gate enforces per-module LOCK-block presence mechanically: every lock_history append REQUIRES a corresponding LOCK block in today's daily log, in canonical format. Authoring discipline becomes structural.

## Trigger condition

Fires as a POST-gate on every attempted append to `pipeline/engineering/lock_history.v1.jsonl`. Before the new row is committed, the gate checks that `daily_logs/{today_iso}.md` contains a canonical LOCK block matching the staged row's `module` field.

## Input contract

```python
@runtime_checkable
class DailyLogReaderCallable(Protocol):
    def __call__(self, date_iso: str) -> str | None: ...

@runtime_checkable
class ClockProtocol(Protocol):
    def now_utc(self) -> datetime: ...
```

- `clock: ClockProtocol` — injected UTC clock (shared with gates #8, #9, #11).
- `daily_log_reader: DailyLogReaderCallable` — injected callable returning text of `daily_logs/{date_iso}.md` or `None` if the log does not exist (shared with gates #8, #11).
- `staged_row: dict` — the lock_history row about to be committed; must contain `module` field at minimum.

## Canonical LOCK-block format

A valid LOCK block in a daily log is:

```
## LOCK: {module}

- `lock_timestamp_utc`: {ISO8601}
- `committee_round`: {round_id}
- `verdict`: {LOCKED | SELF-LOCKED-pending-committee | LOCKED-backfilled}
- `code_sha3_512_prefix`: {first 16 hex chars OR "n/a" for test-only locks}
- `tests_added_this_module`: {integer}
- `lines_of_code`: {integer}
- `findings_surfaced_at_lock`: {integer}
```

Block is identified by the `## LOCK: {module}` heading (exact prefix match, module name verbatim). Required fields are the seven listed above. Additional fields permitted but ignored.

## Pass/fail criteria (deterministic — no LLM)

1. Extract `module` from `staged_row`. If absent or empty string → FAIL (fail-closed on ambiguity; can't check without a module name).
2. Compute `today_iso = clock.now_utc().date().isoformat()`.
3. Call `daily_log_reader(today_iso)`. If returns `None` → FAIL `F-AMDT-12-MISSING` (today's daily log does not exist; operator must create it before any LOCK).
4. Search the returned text for the canonical heading `## LOCK: {module}`. If absent → FAIL `F-AMDT-12-MISSING`.
5. Parse the block after the heading up to the next `## ` heading or EOF. Check all seven required fields are present as `- \`{field}\`:` lines with non-empty values.
6. Any required field missing → FAIL `F-AMDT-12-MALFORMED` (detail: which fields).
7. **PASS:** block found and well-formed.
8. **FAIL-CLOSED:** any injected callable raises → DENY with `event: "F-AMDT-12-READER-FAIL"`.

## Backfill exception (F-03 carve-out)

Lock rows with `verdict: "LOCKED-backfilled"` AND `backfilled: true` are EXEMPT from this gate. Rationale: backfilled rows are recovering historical locks from before this gate existed; requiring a daily log block for a lock that happened weeks ago would gate-block the backfill itself. Carve-out is narrow — only rows marked `backfilled: true` pass without daily-log check, and the backfill_evidence field must point to the recovered audit trail.

Any new (non-backfill) LOCK on or after 2026-04-21 is subject to the full gate.

## Failure behavior

- **DENY** the lock_history append. The staged row does NOT land in `lock_history.v1.jsonl`.
- Emit structured failure record to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-12-{MISSING|MALFORMED|READER-FAIL}"`, `gate: "F-DAILY-LOG-LOCK-BLOCK-MISSING"`, `staged_module`, `today_iso`, `missing_fields` (if MALFORMED).
- Operator remediation: write the canonical LOCK block to today's daily log, then retry the append.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- `ClockProtocol` and `DailyLogReaderCallable` shared with gates #8 (F-COMMITTEE-DEGRADATION-TIMEOUT), #9, #11. Single Protocol instance per run.
- Block-parsing is line-oriented: split daily log text on `\n## `, locate the block whose first line is `LOCK: {module}`, parse the bullet list for required fields. No markdown AST parsing — simple string matching is sufficient and deterministic.
- Module-name matching is exact (case-sensitive, whitespace-sensitive). Canonical module names match the Python import path form (e.g., `pipeline.sovereignty.audit`, NOT `audit.py`).
- Lives at `pipeline/logician/gates/f_daily_log_lock_block_missing.py`.
- AST-lint R1–R5 clean at module load.
- Wave 2 because it depends only on file readers shared with other Wave 2/3 gates (no crypto, no external network).

## Test criteria

### Unit tests (≥30)

- Daily log exists + contains canonical block for module → PASS.
- Daily log exists + no block for module → DENY `F-AMDT-12-MISSING`.
- Daily log does not exist → DENY `F-AMDT-12-MISSING`.
- Block exists but missing `lock_timestamp_utc` → DENY `F-AMDT-12-MALFORMED`.
- Block exists but missing `committee_round` → DENY `F-AMDT-12-MALFORMED`.
- Block exists but `tests_added_this_module: 0` (valid zero) → PASS.
- Block exists but `tests_added_this_module: ` (empty value) → DENY `F-AMDT-12-MALFORMED`.
- Multiple LOCK blocks in same daily log for different modules → gate finds the matching one → PASS.
- Block heading has trailing whitespace (`## LOCK: foo  `) → PASS (whitespace tolerant on heading only).
- `staged_row` missing `module` field → DENY.
- `staged_row["module"]` is empty string → DENY.
- **Backfill carve-out:** `staged_row["backfilled"] is True` AND `verdict == "LOCKED-backfilled"` → PASS without daily-log check.
- Backfill carve-out: only `backfilled: true` without `LOCKED-backfilled` verdict → gate runs normally (don't accept half-marked backfill).
- Parametrized over module names: sovereignty modules, vault modules, logician modules, loop modules, scout modules.

### Adversarial tests (≥5)

- `test_adv_daily_log_reader_raises` → DENY fail-closed.
- `test_adv_clock_raises` → DENY fail-closed.
- `test_adv_block_heading_close_but_not_exact` — heading `## LOCK:foo` (no space after colon) → DENY `F-AMDT-12-MISSING` (exact-match discipline).
- `test_adv_block_for_different_module_with_similar_name` — block heading `## LOCK: pipeline.scout.types` when staged module is `pipeline.scout._types` → DENY (exact match required).
- `test_adv_required_field_value_is_whitespace_only` — field value is `   ` (spaces) → DENY `F-AMDT-12-MALFORMED` (empty-after-strip).
- `test_adv_block_fields_out_of_order` — required fields present but in different order from canonical → PASS (order not enforced; presence is).
- `test_adv_backfill_carveout_without_evidence_path` — `backfilled: true` + `LOCKED-backfilled` verdict but no `backfill_evidence_path` field → PASS this gate (evidence check is a separate gate; gate #12 scope is narrow).

## Dependencies

- `ClockProtocol` (pattern: §5 Round 2; shared with gates #8, #9, #11).
- `DailyLogReaderCallable` (shared with gates #8, #11).
- `daily_logs/YYYY-MM-DD.md` naming convention (existing; no schema change).
- §4 v2.1 gate infrastructure (POST-gate hook on lock_history append).
- `lock_history.v1.jsonl` schema extension — add optional fields `backfilled: bool`, `verdict: Literal["LOCKED", "SELF-LOCKED-pending-committee", "LOCKED-backfilled"]`. F-03 backfill already uses these conventionally; this gate formalizes them.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_daily_log_lock_block_missing.py` |
| Tests | `tests/logician/gates/test_f_daily_log_lock_block_missing.py` + `tests/logician/gates/test_adv_f_daily_log_lock_block_missing.py` |
| Lock history schema | `lock_history.v1.jsonl` schema extension documenting `backfilled`, `verdict` fields (F-03 convention formalized) |
| Daily log template | `daily_logs/TEMPLATE.md` with a "## LOCK: {module}" block template + field checklist (author-ergonomic) |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-DAILY-LOG-LOCK-BLOCK-MISSING"`, `failure_code: "F-AMDT-12"` |
| Blueprint amendment | §4 v2.2 blueprint delta rows for F-AMDT-12-MISSING / F-AMDT-12-MALFORMED |
| Memory | MEMORY.md index entry |

## Origin

Codebase alignment audit 2026-04-20 F-03: lock_history.v1.jsonl was introduced mid-build (~Round A, 2026-04-19); 44 modules were implemented and LOCKed without lock_history entries. Backfill recovered the telemetry but not the authoring discipline. Josh's residual-gap flag (2026-04-20): "backfilling telemetry doesn't fix the authoring discipline that caused the gap." This gate closes the discipline gap mechanically by binding every lock_history append to a daily_log LOCK block. A session that LOCKs a module without writing the daily_log block is now DENIED at the append, not discovered weeks later by an audit.

---

*Spec card v1 — 2026-04-20 — new gate #12 from F-03 residual-gap flag; closes the authoring-discipline gap revealed by the 44-module backfill. Approved by operator same session as spec-card creation.*
