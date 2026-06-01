# Spec card — pipeline.loop (Round 1 foundations: config / errors / types / __init__)

**STATUS:** SELF-LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19 — canonical §5 Pipeline Orchestrator contract
- `pipeline/blueprint/v0.1/section_05_v6_amendment.md` LOCK-READY — InvocationRecord + STR wiring for §5
- Principal sections: §3.2 owned data structures; §3.5 banned imports/patterns; §6 failure-code table (22 F-PIPE-* codes); §7.10–§7.16 invariants; §8 constants + module-load integrity asserts; §9.7.16 / §9.9.30 AST-grep tests

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d`
- `section_05_v6_amendment.md`: `16205371322681cf`

**Spec-card version:** v1
**Round:** §5 Round 1 — foundations (0 upstream Python deps; zero runtime LLM calls)
**Canonical home:** `pipeline/loop/` (NOT `tilth/pipeline/` — blueprint prose uses the `tilth/pipeline/` prefix but the codebase uses `pipeline/`; ARCH-04 R2 `LOOP_LOGICIAN_BAN` policing is already pinned to `pipeline/loop/**/*.py` — see `pipeline/linting/ast_lint.py` line 394)
**Futureproofing scope:** §4.1 public-API boundary; §4.2 schema versioning (`RUNSTATE_SCHEMA_VERSION=2`, `CALIBRATION_REPORT_SCHEMA_VERSION=1`, `INVOCATION_RECORD_SCHEMA_VERSION=1` observability-owned); §4.4 crypto-agility (`CALIBRATION_SIGNING_ALGORITHM: Final[str] = "Ed25519"`); §4.6 BLUEPRINT_DEPS drift detection; §4.9 regression-corpus discipline; §4.10 full type hints (Python 3.11+ `Final`, `Literal`, `frozen=True, kw_only=True` dataclasses); §4.11 docstring blueprint anchors; §4.12 engineering-lessons continuity (E-017 injected-callable, E-019 translator-dataclass available for later rounds)

---

## Summary

Round 1 lays the `pipeline.loop` foundation that every subsequent §5 round (Rounds 2–12) imports from. Four files:

1. `pipeline/loop/__init__.py` — package `__all__` declaring the stable public API; re-exports `config`, `errors`, `types` symbols.
2. `pipeline/loop/config.py` — every §8 constant (v6 LOCKED set), every module-load integrity assert (TAB_ORDERING / EVAL_MODE_ALLOWED_INTENTS / SUBMISSION_MODE_FORBIDDEN_INTENTS / CALIBRATION_SIGNING_ALGORITHM / RUNSTATE_SCHEMA_VERSION / RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED / MAX_CALIBRATION_AGE_DAYS / CALIBRATION_REPORT_SCHEMA_VERSION), plus vault-relative path templates.
3. `pipeline/loop/errors.py` — `PipelineFailure` base class + 22 `F-PIPE-*` exception classes (F-PIPE-01 … F-PIPE-22) enumerated verbatim from §6, each carrying `code`, `trigger`, `severity`, `save_state_contract`, and structured `details`. Also declares the forward-dep sentinel `F_EVAL_CROSS_ORG_READ_CODE: Final[str] = "F-EVAL-CROSS-ORG-READ"` (no exception class — §4 owns the class; §5 only branches on the returned code string).
4. `pipeline/loop/types.py` — the nine frozen/slotted dataclasses that every §5 round references: `RunState`, `IterationState`, `SeatCharter`, `ProviderCascade`, `RateLimiterState`, `TabEnvelope`, `GoldenSetItem`, `CalibrationReportItem`, `CalibrationReport`.

Round 1 ships zero algorithm and zero I/O. It ships only *shape* — so that Round 2 (state_checkpoint.py) can typecheck `RunState`, Round 4 (seat_runner.py) can typecheck `SeatCharter` / `ProviderCascade`, Round 5 (revision_loop.py) can typecheck `IterationState`, etc. Every shape-level invariant ($\text{mode-discriminated union}$, frozen `TabEnvelope`, `frozenset` literal of allowed/forbidden intents) is enforced at dataclass-construction time via `__post_init__` or at module-load via `assert`.

## Design decisions (E1-resolved 2026-04-20)

1. **Canonical home is `pipeline/loop/`, not `tilth/pipeline/`.** Blueprint §3.1 uses `tilth/pipeline/errors.py` et al. as file-path examples because the blueprint was drafted before the codebase convention of putting the runtime at `pipeline/<section>/`. ARCH-04's R2 `LOOP_LOGICIAN_BAN` rule already pins its `target_glob` to `pipeline/loop/**/*.py`. Changing the rule glob would itself be a blueprint drift event; instead, this round treats `pipeline/loop/` as the canonical home and notes in `BLUEPRINT_DEPS` that §5 path prose is a non-normative anchor.

2. **`pipeline.observability` is already LOCKED and imported as-is.** Phase 1 LOCKED 2026-04-19 shipped `pipeline/observability/` with `InvocationRecord`, `STRWindow`, `compute_str`, `INVOCATION_RECORD_SCHEMA_VERSION=1`, `STR_WINDOW_MIN_SESSIONS=5`, `STR_WINDOW_MAX_AGE_DAYS=30`. Round 1 does NOT re-declare those constants. `pipeline.loop.config` imports them if needed at later rounds (Round 4 seat_runner emits `InvocationRecord`). This round does not import observability — Round 1 has zero runtime callers.

3. **`RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED` uses `frozenset` and is integrity-asserted at module load.** Blueprint §8 (line 1101) pins the rationale: MA-07/MB-05 closure — silent upgrade from v1 to v2 would mask the absence of `mode` on legacy state. Module-load assertion with inline literal `frozenset({1})` is V1 discipline applied to a new constant.

4. **Nine dataclasses live in one file, not nine files.** Rationale: all nine are shape-only, zero logic. Splitting per-file adds import fan-out overhead with no encapsulation gain. Blueprint §3.2 groups them together explicitly. A future round may split if any dataclass accrues nontrivial method surface; today, a single `types.py` is the simpler boundary.

5. **Frozen vs slotted.** `TabEnvelope`, `GoldenSetItem`, `CalibrationReportItem`, `CalibrationReport` are **`frozen=True, slots=True, kw_only=True`** — these are signed artifacts or pinned-ordering envelopes where mutation would be a correctness bug. `RunState`, `IterationState`, `RateLimiterState`, `SeatCharter`, `ProviderCascade` are **`slots=True, kw_only=True` but NOT frozen** — they are in-memory state that is rebuilt on each checkpoint write (copy-on-write semantics enforced by the §4.1 checkpoint layer, not at the dataclass level). Kw-only across the board so field additions cannot silently reorder positional calls (v0.2 futureproofing).

6. **`TabEnvelope.tab_ordering` type pin + dataclass-level `__post_init__` integrity check.** Blueprint §3.2.6 types `tab_ordering: tuple[Literal["live_radar"], Literal["deep_brief"], Literal["council_draft"]]`. The runtime check at `assemble_and_deliver` (Round 9) uses an inline tuple literal (V1 discipline — `TAB_ORDERING` module-rebind cannot bypass). Round 1's `TabEnvelope.__post_init__` adds a defence-in-depth sanity check with inline-literal RHS: `if self.tab_ordering != ("live_radar", "deep_brief", "council_draft"): raise F_PIPE_16("tab_envelope_ordering_violation", ...)`. This makes *construction* of a malformed envelope impossible regardless of call-site sloppiness.

7. **Mode-discriminated union enforced in `RunState.__post_init__`.** Blueprint §3.2.1 ⟹ three mode-discriminant invariants (lines 330–332). Round 1 implements them as `__post_init__` raises:
   - `mode == "submission"` requires non-None `rfa_hash` and `project_context_hash`; requires None for `golden_set_ref`, `calibration_report_ref`, `calibration_signature_ref`. Violation → `F_PIPE_21("submission_mode_has_calibration_ref" | "submission_mode_missing_rfa_hash" | ...)`.
   - `mode == "eval"` requires non-None `golden_set_ref`; requires None for `rfa_hash`, `project_context_hash`, `three_tab_envelope_hash`. Violation → `F_PIPE_21("eval_mode_has_tab_envelope_hash" | "eval_mode_missing_golden_set_ref" | ...)`.
   - `schema_version != RUNSTATE_SCHEMA_VERSION` (inline-literal `!= 2`) → `F_PIPE_22("runstate_schema_downgrade")`. This fires at *construction* — Round 2 `resume_run` will also call `_assert_runstate_schema_current` per §4.1 step 1, but defence-in-depth at dataclass level catches in-memory corruption too.

8. **Every `F-PIPE-*` class inherits from `PipelineFailure`.** A single base class lets `state_checkpoint` (Round 2) do `except PipelineFailure as e: write_state_failure_checkpoint(run_state, e.code, e.trigger, e.details)` uniformly. Each subclass pins `CODE: Final[str]` (e.g. `F_PIPE_01.CODE = "F-PIPE-01"`) plus `SEVERITY: Final[str]` (one of `"CRIT" | "HIGH" | "MED" | "LOW"`) and `SAVE_STATE_CONTRACT: Final[str]` (one of the blueprint §6 column values). Sub-trigger taxonomy for F-PIPE-21 and F-PIPE-22 lives in module-level `frozenset` constants (`F_PIPE_21_TRIGGERS`, `F_PIPE_22_TRIGGERS`) with module-load integrity asserts against the exhaustive §6 trigger list.

9. **`CalibrationReport.canonical_bytes()` is NOT shipped in Round 1.** Blueprint §5.6.4 enumerates every canonical-included field, with the sole true exclusion `{"signature": "the signature cannot cover itself"}` (§7.16 invariant). Canonical-bytes serialisation lives in Round 12 (calibration subpackage). Round 1 ships only the dataclass shape; the §7.16 invariant is defended at lock time by the §9.9.30 AST-grep test (to be implemented in Round 12). Shipping canonical-bytes alongside the dataclass would cross the round-granularity boundary (§2 engineering process: round ≤ 40 KiB combined).

10. **No mutable defaults.** All list/dict/tuple defaults use `field(default_factory=...)`. `iterations: list[IterationState]` defaults to `field(default_factory=list)`; `buckets: dict[str, TokenBucket]` defaults to `field(default_factory=dict)`; `run_iteration_families_so_far: dict[str, tuple[str, str]]` defaults to `field(default_factory=dict)`. `TokenBucket` is a forward-dep shape owned by Round 7 (`rate_limiter.py`); Round 1 declares it as a `TYPE_CHECKING`-guarded `Protocol` stub with `capacity: int`, `tokens: float`, `refill_rate_per_sec: float` fields — Round 7 provides the concrete implementation. This keeps `RateLimiterState` typechecking-clean today without shipping bucket logic.

## Public API (goes in `pipeline/loop/__init__.py::__all__`)

```python
# pipeline/loop/__init__.py
from pipeline.loop.config import (
    # Futureproofing pin (§4.6)
    BLUEPRINT_DEPS,
    # §8 constants — v6 LOCKED set
    TAB_ORDERING,
    RUNSTATE_SCHEMA_VERSION,
    RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED,
    CALIBRATION_REPORT_SCHEMA_VERSION,
    CALIBRATION_SIGNING_ALGORITHM,
    MAX_CALIBRATION_AGE_DAYS,
    EVAL_MODE_ALLOWED_INTENTS,
    SUBMISSION_MODE_FORBIDDEN_INTENTS,
    CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS,
    CHECKPOINT_TOTAL_TIMEOUT_SEC,
    CRON_VAULT_RETRY_WINDOW_SEC,
    CRON_VAULT_RETRY_ATTEMPTS,
    RATE_LIMIT_JITTER_RANGE_MS,
    RATE_LIMIT_LEASE_TTL_SEC,
    CRON_STAMP_TTL_HOURS,
    SCRIBE_SUBPROCESS_TIMEOUT_MS,
    EDITOR_SUBPROCESS_TIMEOUT_MS,
    JUDGE_SUBPROCESS_TIMEOUT_MS,
    OPERATOR_INTERRUPT_POLL_INTERVAL_MS,
    MAX_REVISION_ITERATIONS,
    # Vault-relative path templates (§8)
    CALIBRATION_REPORT_PATH_TMPL,
    CALIBRATION_SIGNATURE_PATH_TMPL,
    BYPASS_PENDING_CHECKPOINT_PATH_TMPL,
    # F-PIPE-21 / F-PIPE-22 exhaustive sub-trigger sets
    F_PIPE_21_TRIGGERS,
    F_PIPE_22_TRIGGERS,
)
from pipeline.loop.errors import (
    PipelineFailure,
    # 22 concrete classes
    F_PIPE_01, F_PIPE_02, F_PIPE_03, F_PIPE_04, F_PIPE_05, F_PIPE_06,
    F_PIPE_07, F_PIPE_08, F_PIPE_09, F_PIPE_10, F_PIPE_11, F_PIPE_12,
    F_PIPE_13, F_PIPE_14, F_PIPE_15, F_PIPE_16, F_PIPE_17, F_PIPE_18,
    F_PIPE_19, F_PIPE_20, F_PIPE_21, F_PIPE_22,
    # Forward-dep sentinel (owned by §4, cited here)
    F_EVAL_CROSS_ORG_READ_CODE,
    # Name → class lookup for post-gate dispatch
    F_PIPE_BY_CODE,
)
from pipeline.loop.types import (
    RunState,
    IterationState,
    SeatCharter,
    ProviderCascade,
    RateLimiterState,
    TokenBucketProtocol,
    TabEnvelope,
    GoldenSetItem,
    CalibrationReportItem,
    CalibrationReport,
    RunMode,              # Literal["submission", "eval"]
    RunPhase,             # Literal[...] of 20 phases
    SeatKind,             # Literal["scribe", "editor", "judge"]
    IntentKind,           # Literal[...] of all vault_write intents used by §5
)

__all__ = [
    # config
    "BLUEPRINT_DEPS",
    "TAB_ORDERING",
    "RUNSTATE_SCHEMA_VERSION",
    "RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED",
    "CALIBRATION_REPORT_SCHEMA_VERSION",
    "CALIBRATION_SIGNING_ALGORITHM",
    "MAX_CALIBRATION_AGE_DAYS",
    "EVAL_MODE_ALLOWED_INTENTS",
    "SUBMISSION_MODE_FORBIDDEN_INTENTS",
    "CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS",
    "CHECKPOINT_TOTAL_TIMEOUT_SEC",
    "CRON_VAULT_RETRY_WINDOW_SEC",
    "CRON_VAULT_RETRY_ATTEMPTS",
    "RATE_LIMIT_JITTER_RANGE_MS",
    "RATE_LIMIT_LEASE_TTL_SEC",
    "CRON_STAMP_TTL_HOURS",
    "SCRIBE_SUBPROCESS_TIMEOUT_MS",
    "EDITOR_SUBPROCESS_TIMEOUT_MS",
    "JUDGE_SUBPROCESS_TIMEOUT_MS",
    "OPERATOR_INTERRUPT_POLL_INTERVAL_MS",
    "MAX_REVISION_ITERATIONS",
    "CALIBRATION_REPORT_PATH_TMPL",
    "CALIBRATION_SIGNATURE_PATH_TMPL",
    "BYPASS_PENDING_CHECKPOINT_PATH_TMPL",
    "F_PIPE_21_TRIGGERS",
    "F_PIPE_22_TRIGGERS",
    # errors
    "PipelineFailure",
    "F_PIPE_01", "F_PIPE_02", "F_PIPE_03", "F_PIPE_04", "F_PIPE_05",
    "F_PIPE_06", "F_PIPE_07", "F_PIPE_08", "F_PIPE_09", "F_PIPE_10",
    "F_PIPE_11", "F_PIPE_12", "F_PIPE_13", "F_PIPE_14", "F_PIPE_15",
    "F_PIPE_16", "F_PIPE_17", "F_PIPE_18", "F_PIPE_19", "F_PIPE_20",
    "F_PIPE_21", "F_PIPE_22",
    "F_EVAL_CROSS_ORG_READ_CODE",
    "F_PIPE_BY_CODE",
    # types
    "RunState", "IterationState", "SeatCharter", "ProviderCascade",
    "RateLimiterState", "TokenBucketProtocol", "TabEnvelope",
    "GoldenSetItem", "CalibrationReportItem", "CalibrationReport",
    "RunMode", "RunPhase", "SeatKind", "IntentKind",
]
```

## Data structures

### `pipeline.loop.types.RunMode` (type alias)

```python
RunMode: TypeAlias = Literal["submission", "eval"]  # §3.2.1 v4 — frozen at start_run
```

### `pipeline.loop.types.RunPhase` (type alias)

```python
RunPhase: TypeAlias = Literal[
    # Submission-mode phases (v1 + v2)
    "initialized",
    "pre_gate_pending", "pre_gate_passed",
    "inner_loop_iter_1", "inner_loop_iter_2", "inner_loop_iter_3",
    "post_gate_pending", "post_gate_passed",
    "signoff_pending", "report_signed", "tabs_delivered", "finalized",
    # Failure / pause states
    "degraded_paused", "aborted_trusted_fail", "aborted_operator", "quarantined",
    # Eval-mode-only phases (v4)
    "eval_iter_pending", "calibration_assembled",
    "calibration_signed", "eval_finalized",
]
```

### `pipeline.loop.types.SeatKind` / `IntentKind`

```python
SeatKind: TypeAlias = Literal["scribe", "editor", "judge"]
IntentKind: TypeAlias = Literal[
    "state-success", "state-failure", "state-quarantine",
    "golden-set-read", "golden-set-write",
    "three-tab-deliver",
    "bypass-pending", "bypass-authorization",
    "admin-risk-append", "cron-stamp",
]
```

### `pipeline.loop.types.TokenBucketProtocol`

```python
@runtime_checkable
class TokenBucketProtocol(Protocol):
    """Round-7-owned shape; declared here so RateLimiterState typechecks in Round 1."""
    capacity: int
    tokens: float
    refill_rate_per_sec: float
```

### `pipeline.loop.types.RunState` — §3.2.1 (v4 + v5)

Fields verbatim from blueprint §3.2.1 lines 279–327. `slots=True, kw_only=True, frozen=False` (see design decision #5). `__post_init__` enforces:

- `schema_version == 2` (inline literal) → else `F_PIPE_22("runstate_schema_downgrade")`.
- `schema_version not in frozenset({1})` (inline literal) → else `F_PIPE_22("runstate_schema_downgrade")`.
- `mode == "submission"` ⟹ `rfa_hash is not None and project_context_hash is not None and golden_set_ref is None and calibration_report_ref is None and calibration_signature_ref is None` — else `F_PIPE_21` with specific trigger from `F_PIPE_21_TRIGGERS`.
- `mode == "eval"` ⟹ `golden_set_ref is not None and rfa_hash is None and project_context_hash is None and three_tab_envelope_hash is None` — else `F_PIPE_21`.
- `phase` membership via inline Literal Union (Python's Literal is static-only, so runtime check uses an inline-literal `frozenset` of the 20 phase strings).

### `pipeline.loop.types.IterationState` — §3.2.2 (v1 unchanged)

Minimal shape for Round 1: `iter_number: int`, `seat_draft_hashes: dict[SeatKind, str]`, `judge_verdict: dict[str, Any] | None`, `failure_code: str | None`, `started_at_iso: str`, `completed_at_iso: str | None`. `__post_init__` asserts `1 <= iter_number <= 3`.

### `pipeline.loop.types.SeatCharter` — §3.2.3

Fields: `seat_kind: SeatKind`, `allowed_families: frozenset[str]`, `primary_model: str`, `cascade_level: int`, `subprocess_timeout_ms: int`. `__post_init__` asserts `cascade_level >= 0` and `subprocess_timeout_ms > 0`.

### `pipeline.loop.types.ProviderCascade` — §3.2.4

Fields: `seat_kind: SeatKind`, `levels: tuple[tuple[str, str], ...]` (each `(family, model_id)`), `current_level: int`. `__post_init__` asserts `levels` is non-empty and `0 <= current_level <= len(levels)`.

### `pipeline.loop.types.RateLimiterState` — §3.2.5 (v2)

Fields verbatim from blueprint §3.2.5 lines 345–351. `TokenBucket` → `TokenBucketProtocol` per design decision #10.

### `pipeline.loop.types.TabEnvelope` — §3.2.6 (v2, frozen)

`frozen=True, slots=True, kw_only=True`. Fields verbatim from blueprint §3.2.6 lines 356–365. `__post_init__`: `if self.tab_ordering != ("live_radar", "deep_brief", "council_draft"): raise F_PIPE_16(trigger="tab_envelope_ordering_violation", details={"observed": self.tab_ordering})`. RHS is an inline tuple literal — V1 discipline.

### `pipeline.loop.types.GoldenSetItem` — §5.6.1

`frozen=True, slots=True, kw_only=True`. Fields per blueprint §5.6 (`item_id: str`, `rfa_hash: str`, `project_context_hash: str`, `expected_judge_min_score: float`, `expected_topline_claims: tuple[str, ...]`, `schema_version: int`). `__post_init__` asserts `0.0 <= expected_judge_min_score <= 100.0` and `schema_version == CALIBRATION_REPORT_SCHEMA_VERSION`.

### `pipeline.loop.types.CalibrationReportItem` — §5.6.2

`frozen=True, slots=True, kw_only=True`. Fields: `item_id: str`, `run_id: str`, `actual_judge_score: float`, `iterations_taken: int`, `failure_code: str | None`, `claim_overlap_ratio: float`, `str_observation: float | None`. `__post_init__` asserts `0 <= iterations_taken <= MAX_REVISION_ITERATIONS` and `0.0 <= claim_overlap_ratio <= 1.0`.

### `pipeline.loop.types.CalibrationReport` — §5.6.3

`frozen=True, slots=True, kw_only=True`. Fields: `schema_version: int`, `run_id: str`, `org_slug: str`, `golden_set_manifest_hash: str`, `items: tuple[CalibrationReportItem, ...]`, `signed_at_iso: str`, `signature: str | None` (None before signing; populated post §4.15 step 9). `__post_init__` asserts `schema_version == CALIBRATION_REPORT_SCHEMA_VERSION` (inline literal `== 1`).

## Algorithms

Round 1 ships no algorithms. Every invariant is either (a) a module-load integrity assert, (b) a `__post_init__` construction-time check, or (c) a `Literal` type for static checking. Algorithm-bearing rounds (state_checkpoint, run_lifecycle, seat_runner, revision_loop, rate_limiter, provider_cascade, three_tab_delivery, graceful_degradation, signoff, cron, modes+calibration) land in Rounds 2–12.

## Failure codes

All 22 `F-PIPE-*` codes are declared as exception classes in `errors.py`. Each carries:

| Class | Code | Name | Severity | Save-state |
|-------|------|------|----------|------------|
| `F_PIPE_01` | F-PIPE-01 | run_state_corrupt | CRIT | state-failure + quarantine |
| `F_PIPE_02` | F-PIPE-02 | pre_gate_timeout | HIGH | state-failure |
| `F_PIPE_03` | F-PIPE-03 | post_gate_timeout | HIGH | state-failure |
| `F_PIPE_04` | F-PIPE-04 | judge_convergence_false_positive | MED | state-failure |
| `F_PIPE_05` | F-PIPE-05 | iteration_cap_exceeded | MED | state-failure |
| `F_PIPE_06` | F-PIPE-06 | rate_limit_exhausted | HIGH | state-failure |
| `F_PIPE_07` | F-PIPE-07 | seat_subprocess_timeout | HIGH | state-failure |
| `F_PIPE_08` | F-PIPE-08 | cross_family_violation | CRIT | state-failure + admin-risk CRIT |
| `F_PIPE_09` | F-PIPE-09 | judge_output_malformed | HIGH | state-failure (never success) |
| `F_PIPE_10` | F-PIPE-10 | signoff_cancelled | LOW | state-failure |
| `F_PIPE_11` | F-PIPE-11 | operator_interrupt | LOW | state-failure (post-checkpoint) |
| `F_PIPE_12` | F-PIPE-12 | hardware_degraded_mode_failed | HIGH | state-failure |
| `F_PIPE_13` | F-PIPE-13 | review_seat_outage_pending_bypass | CRIT | state-failure + bypass-pending |
| `F_PIPE_14` | F-PIPE-14 | review_seat_bypass_expired | HIGH | state-failure |
| `F_PIPE_15` | F-PIPE-15 | cron_dedupe_failure | HIGH | state-failure |
| `F_PIPE_16` | F-PIPE-16 | tab_envelope_ordering_violation | CRIT | state-failure + admin-risk CRIT |
| `F_PIPE_17` | F-PIPE-17 | bypass_authorization_ledger_write_failed | CRIT | state-failure |
| `F_PIPE_18` | F-PIPE-18 | resume_phase_mismatch | CRIT | state-failure + quarantine |
| `F_PIPE_19` | F-PIPE-19 | soft_restart_forbidden | CRIT | state-failure + admin-risk CRIT |
| `F_PIPE_20` | F-PIPE-20 | cedar_decision_missing | CRIT | state-failure |
| `F_PIPE_21` | F-PIPE-21 | calibration_report_in_submission_bundle | CRIT | state-failure + admin-risk CRIT |
| `F_PIPE_22` | F-PIPE-22 | runstate_schema_downgrade | CRIT | state-failure + quarantine |

Plus the forward-dep sentinel `F_EVAL_CROSS_ORG_READ_CODE: Final[str] = "F-EVAL-CROSS-ORG-READ"` — Section 4 v2.1 owns the exception class; Round 1 only declares the code string for branching.

### F-PIPE-21 exhaustive sub-triggers (`F_PIPE_21_TRIGGERS`)

Per §6 v5 line 1052:

```python
F_PIPE_21_TRIGGERS: Final[frozenset[str]] = frozenset({
    "mode_change_after_start",
    "eval_mode_has_tab_envelope_hash",
    "eval_mode_invalid_intent",
    "submission_mode_calibration_intent",
    "submission_mode_has_calibration_ref",
    "submission_mode_missing_rfa_hash",
    "submission_mode_missing_project_context_hash",
    "eval_mode_missing_golden_set_ref",
    "eval_mode_has_rfa_hash",
    "eval_mode_has_project_context_hash",
    "golden_set_path_escapes_prefix",
    "golden_set_path_traverses_symlink",
    "eval_run_reached_tab_delivery",
    "calibration_signature_stale",
    "golden_set_manifest_org_mismatch",
})
assert len(F_PIPE_21_TRIGGERS) == 15, \
    "F_PIPE_21_TRIGGERS has been rebound at module load; refusing to load pipeline.loop.config"
```

Module-load integrity assert with inline literal count (V1 discipline — an attacker who rebinds the frozenset cannot make the length check pass because the RHS `15` is literal).

### F-PIPE-22 exhaustive sub-triggers (`F_PIPE_22_TRIGGERS`)

```python
F_PIPE_22_TRIGGERS: Final[frozenset[str]] = frozenset({
    "runstate_schema_downgrade",
    "calibration_report_schema_mismatch",
})
assert len(F_PIPE_22_TRIGGERS) == 2, \
    "F_PIPE_22_TRIGGERS has been rebound at module load; refusing to load pipeline.loop.config"
```

### `F_PIPE_BY_CODE` dispatch table

```python
F_PIPE_BY_CODE: Final[Mapping[str, type[PipelineFailure]]] = {
    "F-PIPE-01": F_PIPE_01, "F-PIPE-02": F_PIPE_02, ...,  # all 22
}
assert len(F_PIPE_BY_CODE) == 22, \
    "F_PIPE_BY_CODE has been rebound at module load; refusing to load pipeline.loop.errors"
```

## §8 Constants (verbatim from blueprint §8 v6)

```python
# pipeline/loop/config.py — §8 constants (v6 LOCKED)

TAB_ORDERING: Final[tuple[str, str, str]] = ("live_radar", "deep_brief", "council_draft")
assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft"), \
    "TAB_ORDERING has been rebound at module load; refusing to load pipeline.loop.config"

RUNSTATE_SCHEMA_VERSION: Final[int] = 2
assert RUNSTATE_SCHEMA_VERSION == 2, \
    "RUNSTATE_SCHEMA_VERSION has been rebound at module load; refusing to load pipeline.loop.config"

RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED: Final[frozenset[int]] = frozenset({1})
assert RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED == frozenset({1}), \
    "RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED has been rebound at module load; refusing to load pipeline.loop.config"

CALIBRATION_REPORT_SCHEMA_VERSION: Final[int] = 1
assert CALIBRATION_REPORT_SCHEMA_VERSION == 1, \
    "CALIBRATION_REPORT_SCHEMA_VERSION has been rebound at module load; refusing to load pipeline.loop.config"

CALIBRATION_SIGNING_ALGORITHM: Final[str] = "Ed25519"
assert CALIBRATION_SIGNING_ALGORITHM == "Ed25519", \
    "CALIBRATION_SIGNING_ALGORITHM has been rebound at module load; refusing to load pipeline.loop.config"

MAX_CALIBRATION_AGE_DAYS: Final[int] = 90
assert MAX_CALIBRATION_AGE_DAYS == 90, \
    "MAX_CALIBRATION_AGE_DAYS has been rebound at module load; refusing to load pipeline.loop.config"

EVAL_MODE_ALLOWED_INTENTS: Final[frozenset[str]] = frozenset({"golden-set-write", "state-success", "state-failure"})
assert EVAL_MODE_ALLOWED_INTENTS == frozenset({"golden-set-write", "state-success", "state-failure"}), \
    "EVAL_MODE_ALLOWED_INTENTS has been rebound at module load; refusing to load pipeline.loop.config"

SUBMISSION_MODE_FORBIDDEN_INTENTS: Final[frozenset[str]] = frozenset({"golden-set-read", "golden-set-write"})
assert SUBMISSION_MODE_FORBIDDEN_INTENTS == frozenset({"golden-set-read", "golden-set-write"}), \
    "SUBMISSION_MODE_FORBIDDEN_INTENTS has been rebound at module load; refusing to load pipeline.loop.config"

CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS: Final[tuple[int, int, int]] = (50, 200, 800)
CHECKPOINT_TOTAL_TIMEOUT_SEC: Final[int] = 10
CRON_VAULT_RETRY_WINDOW_SEC: Final[int] = 300
CRON_VAULT_RETRY_ATTEMPTS: Final[int] = 6
RATE_LIMIT_JITTER_RANGE_MS: Final[tuple[int, int]] = (0, 300)
RATE_LIMIT_LEASE_TTL_SEC: Final[int] = 30
CRON_STAMP_TTL_HOURS: Final[int] = 36
SCRIBE_SUBPROCESS_TIMEOUT_MS: Final[int] = 300_000
EDITOR_SUBPROCESS_TIMEOUT_MS: Final[int] = 180_000
JUDGE_SUBPROCESS_TIMEOUT_MS: Final[int] = 180_000
OPERATOR_INTERRUPT_POLL_INTERVAL_MS: Final[int] = 500
MAX_REVISION_ITERATIONS: Final[int] = 3

# Vault-relative path templates (§8 v4)
CALIBRATION_REPORT_PATH_TMPL: Final[str] = "{org_slug}/golden_set/calibration_reports/{run_id}.json"
CALIBRATION_SIGNATURE_PATH_TMPL: Final[str] = "{org_slug}/golden_set/calibration_reports/{run_id}.sig"
BYPASS_PENDING_CHECKPOINT_PATH_TMPL: Final[str] = "pipeline/{run_id}/bypass_pending.json"
```

## Test surface

### Property tests (`tests/loop/test_config.py`, `test_errors.py`, `test_types.py`)

- Every constant has a round-trip equality test against its blueprint-pinned value.
- Every type alias (`RunMode`, `RunPhase`, `SeatKind`, `IntentKind`) has a `typing.get_args` exhaustiveness test against the blueprint-enumerated set.
- Every dataclass constructs successfully with a minimal valid kwarg set.
- `F_PIPE_BY_CODE` is bijective: keys == `{f"F-PIPE-{i:02d}" for i in range(1,23)}`; values == 22 distinct classes.

### Failure-code tests (`tests/loop/test_types_failures.py`)

One test per `F-PIPE-*` code that Round 1 can trigger at construction time:

- `test_f_pipe_16_raised_on_reordered_tab_envelope` — construct `TabEnvelope(tab_ordering=("deep_brief", "live_radar", "council_draft"), ...)` → `F_PIPE_16` with trigger `tab_envelope_ordering_violation`.
- `test_f_pipe_21_raised_on_submission_mode_with_calibration_ref` — `RunState(mode="submission", calibration_report_ref="x", ...)` → `F_PIPE_21` with trigger `submission_mode_has_calibration_ref`.
- `test_f_pipe_21_raised_on_eval_mode_with_tab_envelope_hash` — `RunState(mode="eval", three_tab_envelope_hash="x", ...)` → `F_PIPE_21` with trigger `eval_mode_has_tab_envelope_hash`.
- `test_f_pipe_21_raised_on_submission_mode_missing_rfa_hash` — `RunState(mode="submission", rfa_hash=None, ...)` → `F_PIPE_21`.
- `test_f_pipe_21_raised_on_eval_mode_missing_golden_set_ref` — `RunState(mode="eval", golden_set_ref=None, ...)` → `F_PIPE_21`.
- `test_f_pipe_22_raised_on_runstate_schema_version_1` — `RunState(schema_version=1, ...)` → `F_PIPE_22`.
- `test_f_pipe_22_raised_on_runstate_schema_version_3` — `RunState(schema_version=3, ...)` → `F_PIPE_22`.

(F-PIPE-01..15, 17..20 are not Round-1-triggerable — they fire in algorithm modules in Rounds 2–12. Round 1 tests verify class declaration shape, not runtime triggering, for those 17 codes.)

### Adversarial tests (`tests/loop/test_adv_config.py`, `test_adv_types.py`)

V1-discipline attacks — spawn a subprocess that monkey-patches `pipeline.loop.config` before import and assert module load fails:

- `test_adv_tab_ordering_module_load_integrity` — rebind `TAB_ORDERING` to a reordered tuple; import fails at the `assert`.
- `test_adv_eval_mode_allowed_intents_module_load_integrity` — rebind → import fails.
- `test_adv_submission_mode_forbidden_intents_module_load_integrity` — rebind → import fails.
- `test_adv_calibration_signing_algorithm_module_load_integrity` — rebind `"Ed25519"` → `"MD5"`; import fails.
- `test_adv_runstate_schema_version_module_load_integrity` — rebind `2` → `1`; import fails.
- `test_adv_max_calibration_age_days_module_load_integrity` — rebind `90` → `99999`; import fails.
- `test_adv_tab_envelope_post_init_inline_literal` — construct `TabEnvelope` with `tab_ordering=TAB_ORDERING` BUT after rebinding `pipeline.loop.config.TAB_ORDERING` to `("x","y","z")` in the calling process — the `__post_init__` inline-literal RHS still catches the violation. (The RHS is `("live_radar","deep_brief","council_draft")` as a fresh tuple every call, so module-attribute rebinding cannot affect it.)

### Corpus tests (`tests/corpus/loop_round1/v1/`)

- v1/runstate_submission_happy.json — canonical valid submission-mode RunState; expected `RunState.__post_init__` to pass.
- v1/runstate_eval_happy.json — canonical valid eval-mode RunState; expected `__post_init__` to pass.
- v1/tab_envelope_happy.json — canonical valid envelope; expected `__post_init__` to pass.
- v1/calibration_report_happy.json — canonical valid report (signature=None before signing); expected `__post_init__` to pass.

## Futureproofing commitments

- **§4.1 Public-API boundary.** `__all__` declared in `pipeline/loop/__init__.py`. Downstream sections import from `pipeline.loop`, never from `pipeline.loop.config` / `.errors` / `.types` directly. ARCH-04 R2 already enforces no `from pipeline.logician.<internal>` imports in `pipeline/loop/**`; Round 1 reciprocally commits to publishing only via `__init__`. Round 10 of ARCH-05 (walker-intensive rules) may add a symmetric `LOOP_INTERNAL_IMPORT_BAN` if cross-section discipline proves insufficient; not blocking here.
- **§4.2 Schema versioning.** Every on-disk artifact carries `schema_version`. Round 1 ships three schema constants: `RUNSTATE_SCHEMA_VERSION=2`, `CALIBRATION_REPORT_SCHEMA_VERSION=1`, and re-exports `INVOCATION_RECORD_SCHEMA_VERSION=1` from `pipeline.observability`. `RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED=frozenset({1})` makes downgrade-rejection explicit rather than silent.
- **§4.4 Crypto-agility.** `CALIBRATION_SIGNING_ALGORITHM: Final[str] = "Ed25519"` — ML-DSA addition is a row append, not a refactor. Round 12's calibration.signing module will dispatch on algorithm; Round 1 pins the constant.
- **§4.6 BLUEPRINT_DEPS drift detection.** Every Round 1 module declares:
  ```python
  BLUEPRINT_DEPS = {
      "section_05_pipeline.md": {
          "version": "v6",
          "hash_sha3_512_prefix16": "34ef007f3ab6d59d",
          "sections_implemented": [...section-specific list...],
      },
      "section_05_v6_amendment.md": {
          "version": "LOCK-READY",
          "hash_sha3_512_prefix16": "16205371322681cf",
          "sections_implemented": ["§0.5 paired-commit row references only"],
      },
  }
  ```
- **§4.9 Backwards-compat corpus.** `tests/corpus/loop_round1/v1/` preserved monotonic per §4.3.
- **§4.10 Type hints.** Python 3.11+ fully typed; `Literal`, `Final`, `frozenset`, `Mapping`, `Protocol` from `collections.abc` / `typing` as appropriate. No `Any` escape hatches except `IterationState.judge_verdict: dict[str, Any] | None` (Judge JSON payload shape is §4 Logician's concern, not Round 1's).
- **§4.11 Docstring blueprint anchors.** Every module docstring, class docstring, and public-function docstring cites the exact blueprint § and line-range it implements.
- **§4.12 Engineering lessons.** E-017 (injected-callable) + E-019 (translator-dataclass) available for Rounds 2–12; no Round 1 application.

## AST-lint compliance

Round 1 code under `pipeline/loop/` passes all five ARCH-04 rules:

- **R1 LOGICIAN_IMPORT_BAN** — N/A (rule targets `pipeline/logician/**`).
- **R2 LOOP_LOGICIAN_BAN** — Round 1 imports nothing from `pipeline.logician.<internal>`; imports nothing from `pipeline.logician` at all (the §5 orchestrator calls `gate_runner` in Rounds 3+ via the public API `from pipeline.logician import gate_runner`, which is permitted by R2).
- **R3 LOGICIAN_OPEN_BAN** — N/A.
- **R4 SCOUT_NO_SETATTR_OPERATOR_DECISION** — N/A.
- **R5 SCOUT_NO_EVAL** — N/A.

Round 1 test files also pass — no `eval`/`exec`, no `setattr` on vault items, no forbidden imports.

## Done definition

- [ ] All tests in `tests/loop/` green under `.venv/bin/python3 -m pytest` (per `scripts/run_tests.sh`).
- [ ] Cumulative pytest ≥ 1733 + new-test-count (baseline: 1733 after ARCH-04 LOCK).
- [ ] Coverage ≥ 95% for each of `pipeline/loop/config.py`, `errors.py`, `types.py`, `__init__.py`.
- [ ] `pipeline/linting/ast_lint.py` run against `pipeline/` tree returns zero violations.
- [ ] All 22 F-PIPE classes declared, each with `CODE`, `SEVERITY`, `SAVE_STATE_CONTRACT` `Final[str]` attributes pinned to §6 v6 values.
- [ ] All §8 v6 constants declared with module-load integrity asserts (8 assertions total per §8 lines 1109–1126).
- [ ] `F_PIPE_21_TRIGGERS` length assert `== 15`; `F_PIPE_22_TRIGGERS` length assert `== 2`; `F_PIPE_BY_CODE` length assert `== 22`.
- [ ] Every dataclass's `__post_init__` shape invariants exercised by red-first failing test before implementation.
- [ ] `BLUEPRINT_DEPS` at top of every module with SHA3-512[:16] of section_05_pipeline.md v6 + section_05_v6_amendment.md pinned.
- [ ] Committee dispatch via router.yaml `code_*` rows (5 reviewers) — all_pass merge rule; retry cap 1.
- [ ] Lock history telemetry appended to `pipeline/engineering/lock_history.v1.jsonl`.
- [ ] Memory entry written; daily log updated; §0.5 Interface Index v5 paired-commit row added (new row: `loop_foundations_v1` → `pipeline.loop.{config,errors,types}.v1`).

## Lines-of-code target

| File | Target | Target ±25% |
|------|--------|-------------|
| `pipeline/loop/__init__.py` | 90 | 68–113 |
| `pipeline/loop/config.py` | 180 | 135–225 |
| `pipeline/loop/errors.py` | 320 | 240–400 |
| `pipeline/loop/types.py` | 380 | 285–475 |

Combined module + test bytes must stay under 40 KiB per §2 round-granularity rule. Four foundation files + their tests should land well under the cap.

## Round 2+ spec-card preview

After Round 1 LOCK, Round 2 spec card covers `pipeline/loop/state_checkpoint.py` (§4.13 checkpoint primitive: CAS with `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS` + `CHECKPOINT_TOTAL_TIMEOUT_SEC` + state-quarantine marker + `_assert_runstate_schema_current` entry-level call). Round 2 is the first round that consumes Round 1's `RunState`, `F_PIPE_01`, `F_PIPE_22` types.
