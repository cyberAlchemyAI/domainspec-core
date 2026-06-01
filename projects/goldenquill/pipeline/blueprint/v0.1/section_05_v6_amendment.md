---
title: Blueprint §5 Pipeline — Amendment v6 (InvocationRecord schema + STR derivation + GPP wiring)
filed: 2026-04-19
operator: Josh
amendment_status: LOCKED 2026-05-08 — L-005 two-audit CLOSED 2026-04-19; GPP three-tier closure 2026-05-08 (Tier 1 PASS, Tier 2 live with §5 v6 + §0.5 companion in scope appendix — 14 findings, 5 BLOCKING dispositioned 1 FOLDED_IN (SCHEMA-MISMATCH-02 — §0.5 companion 8-field description corrected to match §5.7.1 canonical) + 3 REJECTED + 1 DEFERRED; Tier 3 signed manifest valid). Paired commit: §0.5 §5 v6 companion (2 rows). Closes the final 3 v7.0.1 carry-forwards.
parent_lock: pipeline/blueprint/v0.1/section_05_pipeline.md  (§5 v5 LOCKED 2026-04-18)
scope_source: pipeline/validation/integration_scope_close_2026-04-19/01_scope_pin.md  (Item 2 — STR column)
architecture_parent: pipeline/architecture/v0.1/tilth_architecture_locked.md  (v7 A1-A12 LOCKED 2026-04-19; v7.1 R.6 row companion lands at §4 v2.3 + v7.1 commit)
companion_index_amendment: TBD — 2 paired §0.5 rows land at this LOCK commit (per_invocation_telemetry_record_schema, str_derivation_and_aggregation)
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state. Forward-looking targets use "target-LOCK at" wording.
---

## Amendment intent

§5 v5 is LOCKED 2026-04-18 under a v6-r2 architecture parent pointer. This amendment:

1. **Updates parent pointer** from architecture v6-r2 to v7 A1-A12 (LOCKED 2026-04-19). No §5 surface change; pointer update only.
2. **Pins the per-invocation telemetry-record schema** (`InvocationRecord`) as a first-class §5 interface contract. v5 described token counts and outcome signals as run-lifecycle outputs but did not pin a named schema with typed fields; this gap was flagged ASPIRATIONAL-LOAD-BEARING in the preflight existence audit.
3. **Names the STR derivation rule** (success-to-token ratio) as a derived column emitted per `InvocationRecord` and aggregated per-seat via rolling window (k=5 W=30d per A11 R.6 discipline).
4. **Absorbs the GPP wiring paragraph** proposed by §4 v2.1.1 amendment (§4.14a, targeting this §5 LOCK window).
5. **Adds module `pipeline.observability`** to §3 Modules with responsibility for record emission, STR derivation, and rolling-window accumulation.

This is a targeted amendment. Existing §5.1–§5.9 (submission_mode run-lifecycle), §4.12 (eval_mode), §5.6 (forward-dep predicates), all failure codes F-PIPE-01 through F-PIPE-22, all v5 invariants, and all nine §10 OQs are preserved without change. The amendment adds new surface; it does not touch existing surface.

---

## §3 Modules — addition

Add one new module row after the `pipeline.modes.eval_mode` entry:

| Module | Responsibility |
|---|---|
| `pipeline.observability` | Per-invocation record emission, STR derivation, and rolling per-seat distribution accumulation. Consumes: token-count pairs + outcome signals from run-lifecycle call sites. Produces: `InvocationRecord` instances (written to session log) + per-seat `STRWindow` state (in-memory, persisted at session-end to node-local telemetry store). Zero cloud dependency; all computation is local. |

---

## §5.7 — Per-invocation telemetry record schema (new subsection)

### §5.7.1 — InvocationRecord schema

Every model invocation within a pipeline run emits exactly one `InvocationRecord`. The record is immutable after emission (append-only write to the session telemetry log). Schema:

| Field | Type | Required | Description |
|---|---|---|---|
| `run_id` | `str` (UUID-4) | YES | Pipeline run identifier; bound at `start_run` or `start_eval_run`. |
| `seat` | `str` | YES | Seat name from `router.yaml` (e.g. `"scribe"`, `"judge"`, `"code_reviewer_1"`). |
| `timestamp` | `str` (ISO 8601 UTC) | YES | Wall-clock time at invocation dispatch (before model round-trip). |
| `model_family_resolved` | `str` | YES | Provider-family of the model that actually received the invocation after fallback resolution (canonical family name from `router.yaml` taxonomy: `"Anthropic"` / `"OpenAI"` / `"OpenAI-OSS"` / `"Alibaba"` / `"Meta"` / `"Moonshot"` / `"Google"` / `"Local-Ollama"`). |
| `token_count_input` | `int` | YES | Input-token count as returned by the provider's response metadata. Minimum 0. |
| `token_count_output` | `int` | YES | Output-token count as returned by the provider's response metadata. Minimum 0. |
| `success_flag` | `int` | YES | 1 = invocation produced a well-formed, non-error response accepted by the consuming seat. 0 = invocation produced an error response, a malformed response, or a response rejected by downstream validation. |
| `latency_ms` | `int` | YES | Round-trip latency from dispatch to response-complete, in milliseconds. |

No optional fields in v0.1. The 8-field schema is the complete canonical surface. Future amendments that add fields must bump the `INVOCATION_RECORD_SCHEMA_VERSION` constant and assert compatibility.

### §5.7.2 — Invariants

- Every invocation that a run-lifecycle call site makes to a seat MUST emit exactly one `InvocationRecord`. Zero-count or multi-count emission is a pipeline invariant violation and triggers `F-PIPE-23.invocation_record_count_mismatch`.
- `token_count_input + token_count_output == 0` is legal (e.g., a cached response or an error that returned before token accounting). The STR derivation handles this as specified in §5.8.1.
- `success_flag` MUST be exactly 0 or 1. Validation occurs at record-emission time: the `InvocationRecord` constructor raises `ValueError` if `success_flag not in (0, 1)`. Any constructor-bypass that results in an out-of-range `success_flag` reaching the aggregation layer is a pipeline invariant violation and triggers `F-PIPE-23.invocation_record_count_mismatch` (the same failure code governs all per-invocation telemetry schema violations). Under the v0.1 trusted-operator envelope (A1–A4) this is an assertion; in future multi-tenant modes it becomes an input-validation boundary check.
- `InvocationRecord` is not a `SubmissionBundle` component and is never included in any submission artifact. The test at §9.36 enforces this.
- `InvocationRecord` is not a `CalibrationReport` component and is never included in any calibration artifact.

---

## §5.8 — STR derivation and rolling-window aggregation (new subsection)

### §5.8.1 — Per-invocation STR derivation

STR (Success-to-Token Ratio) is a derived value computed from each `InvocationRecord`. It is NOT a stored field on the record; it is computed at aggregation time.

```
token_sum = token_count_input + token_count_output
if token_sum == 0:
    str_per_invocation = None  # undefined; excluded from distribution accumulation
else:
    str_per_invocation = success_flag / token_sum
```

`str_per_invocation ∈ [0.0, 1.0]` when defined; `None` when token_sum is zero.

### §5.8.2 — Rolling per-seat distribution accumulation

STR is aggregated per seat over a rolling window. Window parameters are pinned by A11 R.6 discipline:

- **k = 5** — minimum session count before a distribution is considered stable enough to publish.
- **W = 30 days** — maximum age of a session's records in the window; sessions older than 30 days are evicted.

The `STRWindow` accumulator holds a deque of `(session_id, session_date, [str_per_invocation values])` tuples. `session_date` is the UTC date derived from the earliest `InvocationRecord.timestamp` emitted in that session (i.e., the session start date). Sessions are identified by `run_id`; the first `InvocationRecord` emitted by a run_id registers that run_id as a new session entry. At window-query time:
1. Evict sessions older than W days.
2. If fewer than k sessions remain after eviction: return `None` (insufficient data — not a failure, treated as "window not yet warm").
3. Else: compute quantile envelope (min, p10, p25, p50, p75, p90, max) over all `str_per_invocation` values in the window.

Output shape: `{"seat": str, "n_sessions": int, "n_invocations": int, "quantiles": {"min": float, "p10": float, "p25": float, "p50": float, "p75": float, "p90": float, "max": float}}` or `None` if the window is not warm.

### §5.8.3 — Export discipline (R.6 class: ratio-metric)

Per A11 R.6 ALLOWED list discipline (v7.1 companion row `str_distribution_allowlist_row`):
- **Distribution-only exports.** The quantile envelope MAY exit the telemetry commons in client-run exports. Per-invocation `str_per_invocation` values MUST NOT.
- **Canary replay exception.** The Canary harness (§4 v2.4 target-LOCK) reads per-session raw `str_per_invocation` arrays for locked-test-vector replay comparisons. These raw reads are local-only (never exported) and scoped to the Canary harness module.
- **No dashboard.** v0.1 ships STR as text/JSON. GUI consumption is Phase 2+.

---

## §6 — New failure code

Add to §6 (Failure-code family extension):

| Code | Tier | Trigger |
|---|---|---|
| `F-PIPE-23.invocation_record_count_mismatch` | POST-gate | A run-lifecycle call site emitted zero or multiple `InvocationRecord` instances for a single invocation. Fail-closed; the run state is written to quarantine and the current session terminates with this failure code. |

---

## §8 — Constants additions

Add to §8 Constants:

```python
# Per-invocation telemetry record schema version.
# Bump when any field is added, renamed, or type-changed.
INVOCATION_RECORD_SCHEMA_VERSION: Final[int] = 1

# STR rolling-window parameters (A11 R.6 k/W discipline).
# k: minimum session count before distribution is considered stable.
# W: maximum session age in days.
STR_WINDOW_MIN_SESSIONS: Final[int] = 5
STR_WINDOW_MAX_AGE_DAYS: Final[int] = 30
```

Module-load integrity assert:
```python
assert STR_WINDOW_MIN_SESSIONS == 5, "STR_WINDOW_MIN_SESSIONS has been rebound at module load; refusing to load pipeline.config"
assert STR_WINDOW_MAX_AGE_DAYS == 30, "STR_WINDOW_MAX_AGE_DAYS has been rebound at module load; refusing to load pipeline.config"
```

---

## §9 — New tests (§9.36–§9.40)

| § | Test name | What it verifies |
|---|---|---|
| 9.36 | `test_invocation_record_not_in_submission_bundle` | An `InvocationRecord` instance added to a `SubmissionBundle` triggers an assertion error or type rejection; telemetry records must never appear in submission artifacts. |
| 9.37 | `test_str_derivation_zero_token_sum_returns_none` | `str_per_invocation(success_flag=1, token_count_input=0, token_count_output=0)` returns `None`, not an error or infinity. |
| 9.38 | `test_str_derivation_basic_ratio` | `str_per_invocation(success_flag=1, token_count_input=100, token_count_output=50)` returns `1/150`. `str_per_invocation(success_flag=0, ...)` returns `0 / token_sum`. |
| 9.39 | `test_str_window_below_min_sessions_returns_none` | An `STRWindow` with fewer than 5 non-evicted sessions returns `None` at query time. |
| 9.40 | `test_str_window_quantile_output_shape` | An `STRWindow` with exactly 5 sessions returns a dict with keys `{seat, n_sessions, n_invocations, quantiles}` and `quantiles` has keys `{min, p10, p25, p50, p75, p90, max}`. |

---

## §5 run-lifecycle — GPP wiring paragraph (absorbed from §4 v2.1.1 proposal)

Add the following paragraph to §5 run-lifecycle description (after the "pipeline entry-point selection" paragraph, before seat-resolution):

> When a pipeline run is triggered by a plan-layer artifact (scope-close, sequencing plan, dispatch plan, preflight existence audit, or handoff contract per §4.14a.1), §5 run-lifecycle invokes GPP-DET first at pipeline-start. GPP-DET output is evaluated before any PRE-gate or seat resolution proceeds. Any FAIL returns control to the operator with the failure report; no seats invoked, no tokens spent. FLAGs require Tier 2 council disposition before the run proceeds. A PASS+disposed state allows the run to continue to §4.2.1 ordered PRE-gate execution.

---

## §0.5 paired-commit rows (2 rows, land at this LOCK commit)

| Primitive ID | Kind | Source section |
|---|---|---|
| `per_invocation_telemetry_record_schema` | schema | §5 v6 §5.7 |
| `str_derivation_and_aggregation` | mechanism | §5 v6 §5.8 |

**Row count: 2.** F-INDEX-STALE PRE-gate must find both rows in §0.5 index at LOCK commit, or commit fails closed. `parent_lock_version` for both rows = "§5 v6 LOCKED [date]"; `parent_lock_commit_hash` = TBD at commit time.

---

## Non-goals for this amendment

- Does not address concurrent `STRWindow` access. In v0.1 trusted-operator single-session envelope (A1–A4), only one session runs at a time; locking semantics are deferred to v0.2 multi-tenant scope.
- Does not guarantee telemetry-log write durability beyond the trusted local filesystem assumption (A4). A node-local write failure can lose `InvocationRecord`s; this is accepted in the single-client single-node envelope.
- Does not introduce a new pipeline entry point. `pipeline.observability` is a library module called by existing entry points; it does not add a new top-level `start_*` function.
- Does not modify the `SubmissionBundle`, `CalibrationReport`, or any v5 data contract.
- Does not introduce a dashboard or GUI.
- Does not expose per-invocation STR values in any export path.
- Does not add a new primitive kind in §0.5. Both rows use existing primitive kinds (schema, mechanism).
- Does not change F-PIPE-01 through F-PIPE-22 semantics.
- Does not change A11 R.6 structure — the `str_distribution_allowlist_row` companion row lands at the §4 v2.3 + v7.1 architecture commit (not this §5 v6 LOCK).

---

## Thesis round expectations

- **Audit pass 1 (Editor + Judge):** Editor audits §5.7 schema precision (are all 8 fields necessary and sufficient? is the failure-code invariant in §5.7.2 clear?), §5.8 derivation clarity (is the zero-token-sum branch obvious?), §5.8.2 window semantics (is "fewer than k sessions" well-defined after eviction?), §5.8.3 export discipline (is "distribution-only" enforceable?), §6 new code (does `F-PIPE-23` naming follow existing convention?), §9 test coverage (do the 5 tests cover the meaningful branches?). Judge scores against §5 v5 rubric with dimension 14 renamed `v6_revision_discipline`.
- **Audit pass 2 (Red Team + Reasoner):** Red Team fires: what if two concurrent runs race on STRWindow state? what if `success_flag` is not 0/1 (e.g., a provider returns an unexpected value)? what if session-log writes fail mid-run — do we lose `InvocationRecord`s silently? does the GPP-wiring paragraph introduce a circular dependency (§5 references §4.14a which references §5 v6)? Reasoner audits: was the "rolling quantile deque" approach considered against an in-memory histogram approach? was the choice of 8 schema fields justified against the A11 R.6 ALLOWED-list shape?
- **Synthesis:** operator + Opus 4.7 synthesizes both passes. LOCK commit lands atomically with 2 §0.5 paired rows.

---

## End of amendment
