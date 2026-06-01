# Spec card — Logician gate F-COMMITTEE-DEGRADATION-TIMEOUT (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit/` — EN-003 F-6-Cycle3
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #8
- §5 Round 2 inline-literal + ClockProtocol pattern: `pipeline/loop/state_checkpoint.py` (CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS rebind-resistance reference)

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 3 (external state: ClockProtocol + DailyLogReader + LockHistoryReader)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-08`

---

## Gate name and failure code

- **Gate:** `F-COMMITTEE-DEGRADATION-TIMEOUT`
- **Failure codes:** `F-AMDT-08-WARN` (advisory), `F-AMDT-08-SUSPEND` (blocking), `F-AMDT-08-ESCALATE` (blocking + mandatory fresh architectural Thesis)
- **Kind:** Time-triggered PRE-gate on code-LOCK-promotion, evaluating elapsed time since the last deprecation-triggered replacement amendment's seal date

## Purpose

When a provider deprecation forces the Code Thesis Committee to degrade from five-family all-pass review to four-family all-pass review (e.g., the Kimi K2 moonshot deprecation that triggered EN-003), the degraded posture is intended to be temporary — a replacement Thesis is in progress. Without a time ceiling, the degraded posture can persist silently, eroding the cross-family rigor that A2 Block 2 locked. This gate enforces a hard three-tier ceiling (warn → suspend → escalate) so that a deprecation event cannot silently become the new normal.

## Trigger condition

Fires as a PRE-gate on every attempt to promote a code LOCK (any entry to `lock_history.v1.jsonl` whose source module is within `pipeline/`) **when** the gate detects that the most recent deprecation-triggered replacement is still in flight. "Still in flight" means:

1. `lock_history.v1.jsonl` contains at least one row with `deprecation_triggered_replacement: true`, AND
2. No subsequent row exists with `deprecation_replacement_complete: true` referencing that deprecation by `deprecation_event_id`.

If neither condition holds (no deprecation in flight), gate returns PASS (no-op).

## Input contract

```python
@runtime_checkable
class ClockProtocol(Protocol):
    def now_utc(self) -> datetime: ...

@runtime_checkable
class LockHistoryReaderCallable(Protocol):
    def __call__(self) -> list[dict]: ...

@runtime_checkable
class DailyLogReaderCallable(Protocol):
    def __call__(self, date_iso: str) -> str | None: ...
```

- `clock: ClockProtocol` — injected UTC clock (pattern: §5 Round 2 `state_checkpoint.py`).
- `lock_history_reader: LockHistoryReaderCallable` — injected callable returning parsed `lock_history.v1.jsonl` rows.
- `daily_log_reader: DailyLogReaderCallable` — injected callable returning the text of `daily_logs/{date_iso}.md` or `None` if the log does not exist.
- `staged_row: dict` — the row about to be committed.

## Thresholds (inline-literal `Final[int]`, rebind-resistance enforced)

Per V1 discipline (see `logician_v2_2_gates.md` implementation constraints + `state_checkpoint.py` reference pattern), all three thresholds are inline-literal `Final[int]` RHS values, NOT module-level constants, with rebind-resistance tests asserting module-load and `__post_init__`-time invariants:

```python
WARN_THRESHOLD_DAYS: Final[int] = 14
SUSPEND_THRESHOLD_DAYS: Final[int] = 30
ESCALATE_THRESHOLD_DAYS: Final[int] = 60
```

Three tiers:
- **Days 0–13:** PASS (no emission).
- **Days 14–29:** PASS with WARN. Emit `event: "F-AMDT-08-WARN"` to `pipeline/metrics/session_log.jsonl`. Code LOCK promotion proceeds.
- **Days 30–59:** DENY with `F-AMDT-08-SUSPEND`. No new code LOCKs may promote until one of: (a) `deprecation_replacement_complete: true` row lands in `lock_history.v1.jsonl`, OR (b) operator sign-off entry exists at `daily_logs/{today}.md` per escalation procedure below.
- **Days ≥ 60:** DENY with `F-AMDT-08-ESCALATE`. Mandatory operator escalation; piecemeal replacement no longer permitted. Fresh architectural Thesis required (full round, not Cycle N). Operator sign-off in `daily_logs/` does NOT unblock; only a fresh architectural Thesis LOCK clears this state.

## Pass/fail criteria (deterministic — no LLM)

1. **Call `lock_history_reader()`.** Walk rows for the most recent row with `deprecation_triggered_replacement: true` (by `lock_timestamp_utc` descending). If none found → PASS (no-op).
2. **Check for completion row.** Scan for a later row with `deprecation_replacement_complete: true` and matching `deprecation_event_id`. If found → PASS (no-op).
3. **Compute elapsed days.** Read `locked_at_iso8601` (or `lock_timestamp_utc`) from the deprecation row. Parse as UTC datetime. Days elapsed = `(clock.now_utc() - locked_at).days`.
4. **Apply thresholds** (exact integer comparisons against inline-literal `Final[int]`):
   - `days < WARN_THRESHOLD_DAYS` → PASS silent.
   - `WARN_THRESHOLD_DAYS <= days < SUSPEND_THRESHOLD_DAYS` → PASS with WARN emission.
   - `SUSPEND_THRESHOLD_DAYS <= days < ESCALATE_THRESHOLD_DAYS` → Check `daily_log_reader(today_iso)` for operator sign-off sentinel (see below). If sign-off present → PASS with WARN. Otherwise → DENY `F-AMDT-08-SUSPEND`.
   - `days >= ESCALATE_THRESHOLD_DAYS` → DENY `F-AMDT-08-ESCALATE` unconditionally (daily-log sign-off does NOT clear this state).
5. **FAIL (`F-AMDT-08-*`):** any injected callable raises → DENY, fail-closed, emit `event: "F-AMDT-08-READER-FAIL"`.

## Operator sign-off sentinel (SUSPEND tier only)

For days 30–59, the gate reads `daily_logs/{today_iso}.md` (via `daily_log_reader`) and looks for the exact sentinel string:

```
F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment target {YYYY-MM-DD}
```

- Sentinel must appear verbatim (case-sensitive, single line).
- `{YYYY-MM-DD}` must parse as a valid ISO date in the future (strictly greater than `today_iso`).
- Sentinel absence OR malformed date OR past date → SUSPEND stands, DENY.
- Sentinel-induced PASS still emits WARN to `session_log.jsonl` (so the acknowledgment is itself audit-logged).

## Failure behavior

- **Days 0–13 (PASS silent):** no emission.
- **Days 14–29 (PASS+WARN):** emit `event: "F-AMDT-08-WARN"` to `pipeline/metrics/session_log.jsonl` with `days_elapsed`, `deprecation_event_id`, `deprecation_locked_at`.
- **Days 30–59 (SUSPEND):** DENY the code LOCK promotion. Emit `event: "F-AMDT-08-SUSPEND"` with full context. Operator must add sentinel to today's daily log to unblock.
- **Days ≥ 60 (ESCALATE):** DENY. Emit `event: "F-AMDT-08-ESCALATE"`. Daily-log sign-off no longer unblocks; only a fresh architectural Thesis LOCK clears.
- **Reader-raises (fail-closed):** DENY. Emit `event: "F-AMDT-08-READER-FAIL"` with the exception class name.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed on all injected-callable raises.
- `ClockProtocol` pattern mirrors `pipeline/loop/state_checkpoint.py` exactly — no direct `datetime.now()` in gate code.
- `LockHistoryReaderCallable` must return rows in committed order; gate walks from end for latest-deprecation-first.
- `DailyLogReaderCallable` returns `None` if log file does not exist; gate treats `None` as "no sign-off present."
- All three thresholds inline-literal RHS at module load (pattern: `state_checkpoint.py` CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS). Rebind-resistance tests required — see E-023 pattern for adversarial closure.
- Lives at `pipeline/logician/gates/f_committee_degradation_timeout.py`.
- AST-lint R1–R5 clean at module load.
- Wave 3 because it depends on `ClockProtocol` + `DailyLogReaderCallable` + `LockHistoryReaderCallable` (all external state).

## Test criteria

### Unit tests (≥30)

- No deprecation row in lock_history → PASS (no-op).
- Deprecation row present + completion row present → PASS (no-op).
- Deprecation row present, no completion, days=0 → PASS silent (no WARN emission).
- Deprecation row present, no completion, days=13 → PASS silent.
- Deprecation row present, no completion, days=14 → PASS with WARN emission.
- Deprecation row present, no completion, days=29 → PASS with WARN emission.
- Deprecation row present, no completion, days=30, no sign-off sentinel → DENY `F-AMDT-08-SUSPEND`.
- Deprecation row present, no completion, days=30, valid sign-off sentinel with future date → PASS with WARN.
- Deprecation row present, no completion, days=59, valid sign-off → PASS with WARN.
- Deprecation row present, no completion, days=60 → DENY `F-AMDT-08-ESCALATE` (sign-off does NOT clear).
- Deprecation row present, no completion, days=200 → DENY `F-AMDT-08-ESCALATE`.
- Sign-off sentinel malformed (missing target date) → SUSPEND stands if in 30–59 range.
- Sign-off target date in the past → SUSPEND stands (sentinel invalid).
- Sign-off target date equals today → SUSPEND stands (strictly future required).
- Multiple deprecation rows → gate uses most recent by `lock_timestamp_utc`.
- Deprecation row present, later completion row exists for DIFFERENT `deprecation_event_id` → gate treats current deprecation as still in flight.
- Parametrized over days boundaries (13/14, 29/30, 59/60) to lock integer comparison semantics.

### Adversarial tests (≥5 — E-023 closure pattern for rebind-resistance)

- `test_adv_warn_threshold_days_rebind_at_module_load` — attempt to rebind `WARN_THRESHOLD_DAYS` before import → module load asserts inline-literal value survives.
- `test_adv_suspend_threshold_days_rebind_at_runtime` — attempt to rebind `SUSPEND_THRESHOLD_DAYS` post-import → gate still compares against inline-literal `30`.
- `test_adv_escalate_threshold_days_rebind_at_runtime` — same pattern, `ESCALATE_THRESHOLD_DAYS` defence-in-depth.
- `test_adv_clock_raises` → DENY with `F-AMDT-08-READER-FAIL` (fail-closed).
- `test_adv_lock_history_reader_raises` → DENY fail-closed.
- `test_adv_daily_log_reader_raises_in_suspend_tier` → DENY `F-AMDT-08-SUSPEND` fail-closed (reader failure does NOT pass-through sign-off).
- `test_adv_days_elapsed_negative_clock_skew` → when `clock.now_utc()` is before `locked_at` (clock skew / NTP anomaly), gate treats as days=0 (PASS silent) and emits `event: "F-AMDT-08-CLOCK-SKEW-WARN"`.

## Dependencies

- `ClockProtocol` (pattern: §5 Round 2 `state_checkpoint.py`).
- `lock_history.v1.jsonl` with `deprecation_triggered_replacement` + `deprecation_event_id` + `deprecation_replacement_complete` fields. **Schema delta required** — these fields are not yet in the canonical row schema. Landing the gate requires the schema extension + a backfill entry for EN-003's Kimi K2 deprecation event.
- `daily_logs/YYYY-MM-DD.md` readable by `DailyLogReaderCallable`.
- `pipeline/metrics/session_log.jsonl` append-only writer (existing observability module).
- §4 v2.1 gate infrastructure (PRE-gate hook on code-LOCK promotion).

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_committee_degradation_timeout.py` |
| Tests | `tests/logician/gates/test_f_committee_degradation_timeout.py` + `tests/logician/gates/test_adv_f_committee_degradation_timeout.py` |
| Lock history schema | `lock_history.v1.jsonl` schema extension — add `deprecation_triggered_replacement`, `deprecation_event_id`, `deprecation_replacement_complete` fields |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-COMMITTEE-DEGRADATION-TIMEOUT"`, `failure_code: "F-AMDT-08"` |
| Lock history backfill | Backfill row for Kimi K2 deprecation event (2026-03-23) with `deprecation_triggered_replacement: true`, `deprecation_event_id: "en003-kimi-k2-2026-03-23"` |
| Blueprint amendment | §4 v2.2 blueprint delta rows for F-AMDT-08-WARN / F-AMDT-08-SUSPEND / F-AMDT-08-ESCALATE |
| Memory | MEMORY.md index entry |

## Coupling to EN-003

The Kimi K2 deprecation of 2026-03-23 is the first real-world invocation of this gate. When EN-003 is LOCKED-sealed, the backfill lock_history row that records the deprecation event is the seed row against which this gate evaluates all future code LOCK promotions until the five-family Committee is restored. If EN-003's replacement Thesis does not complete within the thresholds, this gate enforces the escalation path that EN-003's F-6-Cycle3 closure commits to.

---

*Spec card v1 — 2026-04-20 — per-gate card split from consolidated logician_v2_2_gates.md gate #8 (was "pending — spec card not yet split"); origin EN-003 F-6-Cycle3; closes the final v2.2 queue gap.*
