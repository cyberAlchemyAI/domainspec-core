# Spec card — Logician gate F-DEPRECATION-REGISTER-STALENESS (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit_cycle4/red_team_verdict.md` — EN-003 Cycle 4 C4-NEW-01
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #9
- Related gate (same domain): `logician_v2_2_f_deprecation_exemption_reuse.md` (gate #6, F-AMDT-06)

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 3 (external state: ClockProtocol + feed-reader + JSONL-reader)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-09`

---

## Gate name and failure code

- **Gate:** `F-DEPRECATION-REGISTER-STALENESS`
- **Failure code:** `F-AMDT-09`
- **Kind:** PRE-gate on amendment with `forced_replacement: false` claim

## Purpose

C4-NEW-01 (EN-003 Cycle 4 Red Team): an amendment can set `forced_replacement: false` to avoid the F-AMDT-06 (`F-DEPRECATION-EXEMPTION-REUSE`) path even when a deprecation IS in effect, if `deprecation_register.jsonl` has not yet been updated to record the deprecation announcement. The timing window between the provider's public deprecation announcement and the operator's register update is an undefended bypass. This gate closes it by independently consulting a deprecation-announcement feed (or a cached snapshot of it) and failing closed when the register lags beyond a bounded staleness window.

## Trigger condition

Fires as a PRE-gate on any amendment whose frontmatter contains `forced_replacement: false` AND names a provider/model slug in `affected_model:`. Cross-checks `deprecation_register.jsonl` and the deprecation-announcement feed for the named model. If the feed reports the model as deprecated but the register does not (or the register entry is older than the announcement by more than `STALENESS_WINDOW_HOURS`), gate DENIES.

## Input contract

```python
@runtime_checkable
class ClockProtocol(Protocol):
    def now_utc(self) -> datetime: ...

@runtime_checkable
class DeprecationRegisterReaderCallable(Protocol):
    def __call__(self) -> list[dict]: ...

@runtime_checkable
class DeprecationFeedReaderCallable(Protocol):
    def __call__(self, affected_model: str) -> dict | None: ...
```

- `clock: ClockProtocol` — injected UTC clock (pattern: §5 Round 2 `state_checkpoint.py`).
- `deprecation_register_reader: DeprecationRegisterReaderCallable` — returns parsed `deprecation_register.jsonl` rows.
- `deprecation_feed_reader: DeprecationFeedReaderCallable` — returns `{announcement_iso8601, deprecation_effective_iso8601, source_url}` for the named model from a cached provider-announcement feed (or `None` if not in feed).
- `amendment_frontmatter: dict` — contains `forced_replacement: bool` and `affected_model: str`.

## Threshold (inline-literal `Final[int]`, rebind-resistance enforced)

```python
STALENESS_WINDOW_HOURS: Final[int] = 72
```

- 72-hour window captures weekend-posted announcements without requiring operator to update register the same hour. Tunable in v0.2 based on empirical deprecation-announcement cadence.

## Pass/fail criteria (deterministic — no LLM)

1. If `amendment_frontmatter["forced_replacement"] is not False` → no-op PASS (gate only fires on explicit false claim).
2. Extract `affected_model` from frontmatter. If missing → FAIL (fail-closed on ambiguity).
3. Call `deprecation_feed_reader(affected_model)`. If returns `None` → PASS (model not in deprecation feed, claim is consistent).
4. Call `deprecation_register_reader()`. Walk for a row matching `affected_model` with `deprecated: true`.
5. **Register present AND register row's `registered_at_iso8601` ≥ feed's `announcement_iso8601`** → PASS (register is current).
6. **Register present BUT register row older than feed announcement by > STALENESS_WINDOW_HOURS** → DENY `F-AMDT-09-STALE`.
7. **Register absent entirely while feed reports deprecation** → DENY `F-AMDT-09-MISSING`.
8. **FAIL-CLOSED:** any injected callable raises → DENY with `event: "F-AMDT-09-READER-FAIL"`.

## Failure behavior

- **DENY** the amendment promotion. `forced_replacement: false` claim rejected as inconsistent with live deprecation state.
- Emit to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-09-STALE"` or `"F-AMDT-09-MISSING"`, `affected_model`, `feed_announcement_iso8601`, `register_registered_at_iso8601` (or `null`), `staleness_hours`.
- Operator remediation: update `deprecation_register.jsonl` for the affected model, then re-submit amendment. If feed is wrong (false positive), operator can add a register row explicitly marking the model as `not_deprecated: true` with evidence, which the gate honors.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- `DeprecationFeedReaderCallable` reads a cached snapshot of provider announcement feeds under `pipeline/vault_shared/deprecation_feed_cache/` (feed-ingestion is a separate cron, not part of this gate). Cache staleness is handled by the cron's own freshness guard; this gate trusts the cache as presented.
- `STALENESS_WINDOW_HOURS` is inline-literal `Final[int]` with rebind-resistance tests (pattern: `state_checkpoint.py` CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS, gate #8 F-COMMITTEE-DEGRADATION-TIMEOUT threshold pattern).
- Lives at `pipeline/logician/gates/f_deprecation_register_staleness.py`.
- AST-lint R1–R5 clean at module load.
- Wave 3 because it depends on ClockProtocol + two external readers.

## Test criteria

### Unit tests (≥30)

- `forced_replacement: true` → no-op PASS.
- `forced_replacement: false`, model not in feed → PASS.
- `forced_replacement: false`, feed reports deprecation, register current (registered_at == announcement time) → PASS.
- `forced_replacement: false`, feed reports deprecation, register ahead of announcement → PASS.
- `forced_replacement: false`, feed reports deprecation, register 1 hour behind announcement → PASS (within window).
- `forced_replacement: false`, feed reports deprecation, register 72 hours behind → PASS (boundary).
- `forced_replacement: false`, feed reports deprecation, register 73 hours behind → DENY `F-AMDT-09-STALE`.
- `forced_replacement: false`, feed reports deprecation, register row absent → DENY `F-AMDT-09-MISSING`.
- `affected_model` field missing → DENY (fail-closed).
- Parametrized over model slugs: `moonshotai/kimi-k2-instruct`, `openai/gpt-4-32k`, etc.

### Adversarial tests (≥5)

- `test_adv_clock_raises` → DENY fail-closed.
- `test_adv_feed_reader_raises` → DENY fail-closed.
- `test_adv_register_reader_raises` → DENY fail-closed.
- `test_adv_staleness_window_hours_rebind_at_module_load` — rebind attempt → module-load assert holds.
- `test_adv_staleness_window_hours_rebind_at_runtime` — rebind attempt post-import → gate still compares against inline-literal `72`.
- `test_adv_register_row_has_not_deprecated_override` → operator-asserted `not_deprecated: true` in register overrides feed → PASS (false-positive escape hatch).
- `test_adv_negative_staleness_clock_skew` → register registered_at is in the future relative to announcement (impossible but defensive) → treat as PASS (register is ahead; clock-skew logged separately).

## Dependencies

- `ClockProtocol` (pattern: §5 Round 2).
- `pipeline/vault_shared/deprecation_register.jsonl` — new shared artifact; schema: `{affected_model, deprecated: bool, registered_at_iso8601, evidence_url, not_deprecated: bool (optional override)}`. Schema extension required.
- `pipeline/vault_shared/deprecation_feed_cache/<provider>.jsonl` — new cached feed; schema: `{affected_model, announcement_iso8601, deprecation_effective_iso8601, source_url}`. Feed-ingestion cron out of this gate's scope.
- §4 v2.1 gate infrastructure (PRE-gate hook on amendment promotion).

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_deprecation_register_staleness.py` |
| Tests | `tests/logician/gates/test_f_deprecation_register_staleness.py` + `tests/logician/gates/test_adv_f_deprecation_register_staleness.py` |
| Shared artifact schema | `pipeline/vault_shared/deprecation_register.jsonl` schema doc + bootstrap empty file |
| Shared artifact schema | `pipeline/vault_shared/deprecation_feed_cache/README.md` with feed schema |
| Feed-ingestion cron | Separate spec card (out of this gate's scope) — `pipeline/engineering/spec_cards/deprecation_feed_cron.md` (PENDING) |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-DEPRECATION-REGISTER-STALENESS"`, `failure_code: "F-AMDT-09"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-09 |
| Memory | MEMORY.md index entry |

## Origin

EN-003 Cycle 4 Red Team Finding C4-NEW-01: `forced_replacement: false` still evades when `deprecation_register.jsonl` lags the actual deprecation announcement. Text-level closure hit the policy-prose ceiling (L-005 signal); mechanical enforcement via independent feed cross-check is the structural resolution.

---

*Spec card v1 — 2026-04-20 — new gate from EN-003 Cycle 4 C4-NEW-01 parked to v2.2 queue per operator disposition.*
