# Spec card — Logician gate F-SDK-PRECEDENT-REUSE (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/` — EN-001 RT-NEW-06
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #4

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 4 (cross-amendment semantics)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-04`

---

## Gate name and failure code

- **Gate:** `F-SDK-PRECEDENT-REUSE`
- **Failure code:** `F-AMDT-04`
- **Kind:** PRE-gate on new-seat Agent-SDK-adoption amendment

## Purpose

The Agent SDK adoption for Scribe (Phase-0 spike) was audited per-seat. That audit evidence is specific to Scribe's threat model, integration surface, and rollback plan. This gate prevents that single-seat audit from being reused as blanket precedent for adopting the Agent SDK on other seats (Scout, Editor, Judge). Each seat must present its own distinct audit evidence. Without this gate, a multi-seat SDK rollout could cite the Scribe spike as sufficient evidence, bypassing the per-seat review that EN-001 RT-NEW-06 requires.

## Trigger condition

Fires as a PRE-gate on any amendment whose frontmatter contains `adopts_agent_sdk: true`. The gate checks whether the amendment's audit evidence is genuinely new or recycled from a prior seat's adoption.

## Input contract

```python
@runtime_checkable
class LockHistoryReaderCallable(Protocol):
    def __call__(self) -> list[dict]: ...
```

- `amendment_frontmatter: dict` — the amendment being proposed. Must contain `adopts_agent_sdk: true` (trigger) and `seat: str` and `audit_evidence_path: str`.
- `lock_history_reader: LockHistoryReaderCallable` — injected callable returning all rows from `lock_history.v1.jsonl`.

## Pass/fail criteria (deterministic — no LLM)

1. Confirm `amendment_frontmatter["adopts_agent_sdk"]` is `True` (trigger guard — if not True, gate is a no-op PASS).
2. Extract `seat` and `audit_evidence_path` from the amendment frontmatter. If either is missing → FAIL (incomplete amendment).
3. Read all rows from lock history via injected reader.
4. Filter rows where `adopts_agent_sdk: true` AND `seat` differs from the current amendment's seat.
5. For each such prior row, compare `audit_evidence_path` against the current amendment's `audit_evidence_path`.
6. **PASS:** no prior row shares the same `audit_evidence_path`.
7. **FAIL (`F-AMDT-04`):** any prior row for a DIFFERENT seat has the same `audit_evidence_path`. Detail: which prior seat's evidence path matches.
8. **FAIL (`F-AMDT-04`):** lock history read failure. Fail-closed.

## Failure behavior

- **DENY** the amendment promotion. Amendment cannot proceed to LOCKED-sealed.
- Emit structured failure record to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-04"`, `gate: "F-SDK-PRECEDENT-REUSE"`, `reused_path`, `prior_seat`, `current_seat`.
- Operator must commission a distinct per-seat audit before re-submitting.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- Injected `LockHistoryReaderCallable` Protocol (E-017 pattern).
- Path comparison is exact string equality — no normalization. Paths in the lock history are canonical.
- Lives at `pipeline/logician/gates/f_sdk_precedent_reuse.py`.
- AST-lint R1–R5 clean at module load.
- Wave 4 because it requires understanding cross-amendment relationships in the lock history (not just single-row validation).

## Test criteria

### Unit tests (≥30)
- First SDK adoption (no prior rows) → PASS.
- Same seat, same evidence path (re-lock of same seat) → PASS (not a different seat).
- Different seat, different evidence path → PASS.
- Different seat, same evidence path → DENY.
- Two prior adoptions for different seats, new seat with unique path → PASS.
- Two prior adoptions, new seat reuses one of them → DENY.
- Amendment missing `seat` field → DENY.
- Amendment missing `audit_evidence_path` → DENY.
- `adopts_agent_sdk: false` → no-op PASS (gate doesn't fire).
- `adopts_agent_sdk` absent → no-op PASS.
- Parametrized over seat names: Scout, Editor, Judge, Scribe.
- Empty lock history → PASS.

### Adversarial tests (≥5)
- `test_adv_lock_history_reader_raises` → DENY (fail-closed).
- `test_adv_evidence_path_differs_by_trailing_slash` → `path/to/evidence` vs `path/to/evidence/` → PASS (exact string match; distinct paths).
- `test_adv_same_seat_different_evidence_overwrites` → same seat submits new evidence path → PASS (not cross-seat reuse).
- `test_adv_adopts_sdk_is_string_true` → `adopts_agent_sdk: "true"` → no-op PASS (strict `is True` check; gate doesn't fire — but amendment is malformed, caught elsewhere).
- `test_adv_circular_reuse_three_seats` → seats A, B, C each try to reuse seat A's evidence → B and C DENY.

## Dependencies

- `lock_history.v1.jsonl` schema with `adopts_agent_sdk`, `seat`, `audit_evidence_path` fields (established by EN-001 lock row).
- `LockHistoryReaderCallable` Protocol (shared with Wave 2 gates).
- §4 v2.1 gate infrastructure (PRE-gate hook on amendment promotion).

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_sdk_precedent_reuse.py` |
| Tests | `tests/logician/gates/test_f_sdk_precedent_reuse.py` + `tests/logician/gates/test_adv_f_sdk_precedent_reuse.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-SDK-PRECEDENT-REUSE"`, `failure_code: "F-AMDT-04"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-04 |
| Memory | MEMORY.md index entry |

---

*Spec card v1 — 2026-04-20 — per-gate card split from consolidated logician_v2_2_gates.md.*
