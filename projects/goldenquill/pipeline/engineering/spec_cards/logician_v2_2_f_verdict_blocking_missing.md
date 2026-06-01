# Spec card — Logician gate F-VERDICT-BLOCKING-MISSING (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1_DRAFT.md` — TSIP v0.1 F-5
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #2

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 1 (no external deps)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-02`

---

## Gate name and failure code

- **Gate:** `F-VERDICT-BLOCKING-MISSING`
- **Failure code:** `F-AMDT-02`
- **Kind:** POST-gate on reviewer-verdict ingest

## Purpose

Every reviewer verdict ingested into the pipeline (Editor, Judge, Red Team) must contain an explicit `blocking: true` or `blocking: false` field. Without this gate, ambiguous or structurally incomplete verdicts could be promoted as valid — a reviewer that forgot the field or returned free-text would silently pass. This gate makes the blocking/non-blocking distinction mechanically enforced, not convention-dependent.

## Trigger condition

Fires as a POST-gate on every reviewer-verdict ingest event. Any seat that produces a verdict (Editor, Judge, Red Team) has its output validated by this gate before the verdict is recorded in the pipeline state.

## Input contract

```python
verdict_json: dict  # The raw parsed verdict from the reviewer seat
```

- `verdict_json: dict` — the reviewer's verdict, already parsed from JSON. Gate does not handle JSON parsing errors (upstream parser responsibility); gate validates structure.

## Pass/fail criteria (deterministic — no LLM)

1. Check `"blocking"` key exists in `verdict_json`.
2. Check `verdict_json["blocking"]` is strictly `True` or `False` (Python bool). Not `"true"`, not `1`, not `None`, not absent.
3. **PASS:** key exists AND value is `bool`.
4. **FAIL (`F-AMDT-02`):** key absent.
5. **FAIL (`F-AMDT-02`):** key present but value is not `bool`.

## Failure behavior

- **DENY** the verdict ingest. The verdict is NOT recorded in pipeline state.
- Emit structured failure record to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-02"`, `gate: "F-VERDICT-BLOCKING-MISSING"`, `detail` describing whether key was absent or wrong type.
- The pipeline halts at this verdict step. Operator or seat must re-submit a structurally valid verdict.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- No injected dependencies required — operates on in-memory dict.
- Check is `isinstance(verdict_json.get("blocking"), bool)`. Single expression.
- Lives at `pipeline/logician/gates/f_verdict_blocking_missing.py`.
- AST-lint R1–R5 clean at module load.
- Applies uniformly to all reviewer seats — no seat-specific carve-outs.

## Test criteria

### Unit tests (≥30)
- `{"blocking": true, ...}` → PASS.
- `{"blocking": false, ...}` → PASS.
- `{}` (empty dict) → DENY.
- `{"blocking": "true"}` → DENY.
- `{"blocking": "false"}` → DENY.
- `{"blocking": 1}` → DENY.
- `{"blocking": 0}` → DENY.
- `{"blocking": None}` → DENY.
- `{"blocking": []}` → DENY.
- Key absent entirely → DENY.
- Verdict with many other fields but no `blocking` → DENY.
- Verdict with `blocking: true` plus extra fields → PASS.
- Parametrized over all three seat types (Editor, Judge, Red Team) with valid/invalid variants.
- Nested dict where `blocking` is at wrong depth → DENY (must be top-level).

### Adversarial tests (≥5)
- `test_adv_blocking_key_case_sensitivity` — `{"Blocking": true}` → DENY (case-sensitive).
- `test_adv_blocking_value_is_numpy_bool` — `numpy.bool_(True)` is not `bool` — DENY (strict isinstance check; documented limitation).
- `test_adv_verdict_is_not_dict` — verdict passed as string or list → DENY with appropriate error, not crash.
- `test_adv_blocking_field_added_after_initial_parse` — mutating dict after gate init but before fire → gate reads at fire time (correct behavior verified).
- `test_adv_empty_verdict_no_crash` — `{}` → clean DENY, no KeyError.

## Dependencies

- §4 v2.1 gate infrastructure (verdict ingest hook point).
- No external file or state dependencies — Wave 1 gate.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_verdict_blocking_missing.py` |
| Tests | `tests/logician/gates/test_f_verdict_blocking_missing.py` + `tests/logician/gates/test_adv_f_verdict_blocking_missing.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-VERDICT-BLOCKING-MISSING"`, `failure_code: "F-AMDT-02"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-02 |
| Memory | MEMORY.md index entry |

---

*Spec card v1 — 2026-04-20 — per-gate card split from consolidated logician_v2_2_gates.md.*
