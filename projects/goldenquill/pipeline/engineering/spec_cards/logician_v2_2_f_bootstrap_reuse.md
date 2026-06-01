# Spec card — Logician gate F-BOOTSTRAP-REUSE (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1_DRAFT.md` — TSIP v0.1 F-1
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #1

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 2 (reads lock_history.v1.jsonl)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-01`

---

## Gate name and failure code

- **Gate:** `F-BOOTSTRAP-REUSE`
- **Failure code:** `F-AMDT-01`
- **Kind:** POST-gate on LOCK-sealed write

## Purpose

The TSIP bootstrap exception is a one-time mechanism that allows the initial system setup to bypass normal amendment procedures. This gate enforces single-use semantics: once the bootstrap exception has been consumed, no subsequent LOCK-sealed write may reuse it. Without this gate, a malicious or careless amendment could frame itself as a "bootstrap" event and bypass the full thesis review process indefinitely.

## Trigger condition

Fires as a POST-gate on every LOCK-sealed write to `lock_history.v1.jsonl`. Specifically: after the new row is staged (but before the write is committed), the gate evaluates whether the new or any prior row claims `bootstrap_exception: true`.

## Input contract

```python
@runtime_checkable
class LockHistoryReaderCallable(Protocol):
    def __call__(self) -> list[dict]: ...
```

- `lock_history_reader: LockHistoryReaderCallable` — injected callable that returns parsed JSONL rows from `pipeline/engineering/lock_history.v1.jsonl` (includes the staged row).
- `staged_row: dict` — the row about to be committed (available for inspection but also present in the reader output).

## Pass/fail criteria (deterministic — no LLM)

1. Parse all rows from `lock_history.v1.jsonl` via the injected reader.
2. Count rows where `bootstrap_exception` field is `true` (strict boolean, not truthy).
3. **PASS:** count ≤ 1.
4. **FAIL (`F-AMDT-01`):** count > 1.
5. **FAIL (`F-AMDT-01`):** JSONL read failure (reader raises or returns malformed data). Fail-closed.

## Failure behavior

- **DENY** the LOCK-sealed write. The staged row is NOT committed.
- Emit structured failure record to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-01"`, `gate: "F-BOOTSTRAP-REUSE"`, `detail: "bootstrap_exception count: {n}"`.
- Escalate to operator via daily_logs entry. No automatic retry — operator must inspect and resolve.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- Injected `LockHistoryReaderCallable` Protocol — no direct file I/O (E-017 pattern).
- The count check is `sum(1 for row in rows if row.get("bootstrap_exception") is True)`. Explicit `is True` — not truthy evaluation.
- Lives at `pipeline/logician/gates/f_bootstrap_reuse.py`.
- AST-lint R1–R5 clean at module load.

## Test criteria

### Unit tests (≥30)
- Single bootstrap row → PASS.
- Zero bootstrap rows → PASS.
- Two bootstrap rows → DENY with F-AMDT-01.
- Three+ bootstrap rows → DENY.
- `bootstrap_exception: "true"` (string, not bool) → not counted; PASS if sole entry.
- `bootstrap_exception: null` → not counted.
- `bootstrap_exception` key absent → not counted.
- Mixed: one `true`, one `"true"`, one `null` → count=1 → PASS.
- Parametrized over edge cases: empty JSONL, single-row JSONL, 100-row JSONL with 0/1/2 bootstrap entries.
- Reader returns empty list → PASS (count=0).

### Adversarial tests (≥5)
- `test_adv_reader_raises_exception` → gate DENY (fail-closed), not PASS.
- `test_adv_reader_returns_malformed_json` → gate DENY.
- `test_adv_bootstrap_field_is_integer_1` → not counted as `True`; PASS if sole entry.
- `test_adv_bootstrap_field_injected_after_gate_init` → rebind of reader after construction does not affect gate behavior (Protocol is called at gate-fire time, not init time — this is correct behavior, just verified).
- `test_adv_concurrent_staged_rows_both_bootstrap` → two staged rows in same batch, both `bootstrap_exception: true` → DENY.

## Dependencies

- `lock_history.v1.jsonl` schema must be stable (exists today).
- `LockHistoryReaderCallable` Protocol defined (can be shared across Wave 2 gates).
- §4 v2.1 gate infrastructure (gate registration, PRE/POST hook points).

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_bootstrap_reuse.py` |
| Tests | `tests/logician/gates/test_f_bootstrap_reuse.py` + `tests/logician/gates/test_adv_f_bootstrap_reuse.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-BOOTSTRAP-REUSE"`, `failure_code: "F-AMDT-01"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-01 |
| Memory | MEMORY.md index entry |

---

*Spec card v1 — 2026-04-20 — per-gate card split from consolidated logician_v2_2_gates.md.*
