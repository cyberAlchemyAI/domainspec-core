# Spec card — pipeline.loop.cascade (Round 8: provider cascade level selection)

**STATUS:** PRE-STAGED (pending operator confirmation — see "Operator choice" below)

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal sections: §4.9 v2 `select_cascade_level` (live landed-family consulted); §3.2.4 `ProviderCascade`; §3.2.1 `RunState.run_iteration_families_so_far`; §6 F-PIPE-08 (`cross_family_exhausted`).
- Cross-section anchors: §5 Round 1 `ProviderCascade` dataclass; §5 Round 7 `rate_limiter.can_reserve` (read-only probe); §4.5 cross-family rigor guard (family exclusion semantics for editor/judge seats).

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d`

**Spec-card version:** v1 (pre-staged 2026-04-21 at §5 Round 7 SELF-LOCK)
**Round:** §5 Round 8 — cascade (provider-cascade level selection consulting live landed-family record + live rate-limiter capacity)
**Depends on:** Round 1 (ProviderCascade, RunState, SeatKind, F_PIPE_08); Round 7 (`rate_limiter.can_reserve`).

## Operator choice — Round 8 candidate A vs B

Round 7 pre-stage identified two candidates for Round 8. This spec card ships **Candidate A (cascade)**. Candidate B (`pipeline/loop/tab_delivery.py` — §4.11 three-tab envelope ordering + signing) is independent and can be dispatched in parallel once approved.

**Why A first:** cascade directly composes `rate_limiter.can_reserve` from Round 7 — the tightest forward-dependency closure, and unblocks §4.1 step 3 seat-invocation routing. Candidate B has no Round 7 dependency (composes Round 1 `TabEnvelope` + §2 vault primitives) and can run in parallel.

If operator prefers B first, swap this spec card's `STATUS` to DEFERRED and dispatch `section_05_round_8_tab_delivery.md` (not yet written) instead.

---

## Summary

Ship `pipeline/loop/cascade.py` — the §4.9 v2 deterministic selector that picks the first cascade level whose family is not already landed in this iteration AND whose endpoint has rate-limiter capacity. Per blueprint §4.9 lines 625–647:

```python
def select_cascade_level(
    *,
    seat_kind: SeatKind,
    cascade: ProviderCascade,
    run_state: RunState,
    vault_read: VaultReadCallable,
    clock: ClockProtocol,
) -> CascadeLevel: ...
```

Iterate `cascade.levels[cascade.current_level_index:]`; skip levels whose `family` is in the `excluded_families` set (derived from `run_state.run_iteration_families_so_far` per seat-kind rules); for each surviving level call `rate_limiter.can_reserve(endpoint=level.provider_endpoint, estimated_tokens=level.estimated_tokens_budget, vault_read=..., clock=...)`; return the first level that both survives family-exclusion AND has capacity. If the tail exhausts with no match → raise `F_PIPE_08` (`cross_family_exhausted`).

Public API:

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class CascadeSelection:
    selected_level: CascadeLevel
    excluded_families: frozenset[str]  # from landed-family consultation
    skipped_for_capacity: tuple[str, ...]  # endpoints that failed can_reserve
    probe_count: int  # levels inspected end-to-end

def select_cascade_level(*, seat_kind, cascade, run_state, vault_read, clock) -> CascadeSelection: ...
```

## §5 v6 compliance decisions (must confirm at ORIENT)

1. **`CascadeLevel` shape.** Round 1 `ProviderCascade.levels` is typed as a sequence but the element dataclass may not yet be defined. Confirm: does `ProviderCascade` carry `levels: tuple[CascadeLevel, ...]` with `CascadeLevel = {family: str, provider_endpoint: str, estimated_tokens_budget: int, ...}`? If yes, Round 8 just consumes it. If no, Round 8 adds the `CascadeLevel` dataclass.

2. **`run_iteration_families_so_far` shape.** Blueprint §4.9 line 630 reads `landed_so_far = run_state.run_iteration_families_so_far`. Round 1 RunState field presence must be verified; per blueprint line 634 `landed_so_far["scribe"][0]` indexes a tuple whose first element is the family name. Confirm the Round 1 shape: `dict[str, tuple[str, ...]]` or `dict[str, tuple[family, endpoint]]`?

3. **Family-exclusion rules.** Blueprint §4.9 lines 632–638: for `seat_kind == "editor"`, exclude the scribe family; for `seat_kind == "judge"`, exclude scribe + editor families; for `seat_kind == "scribe"`, no exclusions. Round 8 inline-literals these seat-kind strings (V1 discipline).

4. **`can_reserve` token-budget source.** `rate_limiter.can_reserve(estimated_tokens=...)` needs an int. Does `CascadeLevel` carry `estimated_tokens_budget`? Or does Round 8 receive it as a separate kwarg? Propose: it lives on `CascadeLevel` and we pass `level.estimated_tokens_budget`.

5. **F_PIPE_08 trigger string taxonomy.** Round 8 raises `F_PIPE_08(trigger=...)` on tail exhaustion. Propose: `cross_family_exhausted:{seat_kind}:{run_id}:{iter_N}` with `details` carrying `excluded_families`, `skipped_for_capacity`, `probe_count`, `cascade_length`.

## Public surface + invariants

- `select_cascade_level` is **read-only** — no vault_write, no mutation of `run_state`. Pure selection.
- Signature takes `vault_read` + `clock` (to pass through to `rate_limiter.can_reserve`) but does NOT take `sleep` / `randint` / `vault_write` — `can_reserve` does not need them.
- Deterministic: given the same `run_state.run_iteration_families_so_far` + the same persisted rate-limiter state, the same level is always returned.
- No retry loop — Round 8 is a selector, not an actor. If the caller wants to retry after `F_PIPE_08`, they unlock levels via their own policy.

## Test plan

Target coverage **≥95%** (100% achievable — pure selection logic).

**Happy paths** (`tests/loop/test_cascade.py`) — ~12 tests:
- Scribe seat → first level always eligible (no family exclusion); returned when capacity available.
- Editor seat, scribe landed family=anthropic → first non-anthropic level returned.
- Judge seat, scribe landed + editor landed → both families excluded, third-family level returned.
- Capacity skip — first level family-eligible but `can_reserve=False` → second level returned, `skipped_for_capacity` pins endpoint.
- `current_level_index` > 0 → earlier levels not probed.
- Combined family + capacity skip — returns deepest eligible level.
- `CascadeSelection.probe_count` matches levels inspected.
- `excluded_families` pins the derived set.

**Adversarial** (`tests/loop/test_adv_cascade.py`) — ~14 tests × E-024 2× multiplier:
- F_PIPE_08 trigger-string taxonomy pin.
- Empty cascade tail after `current_level_index` → F_PIPE_08 with empty `skipped_for_capacity` + empty `excluded_families` (for scribe).
- All levels same family + editor seat (that family landed) → F_PIPE_08 with single-element `excluded_families`.
- All levels rate-limited (every `can_reserve` returns False) → F_PIPE_08 with all endpoints in `skipped_for_capacity`.
- `run_iteration_families_so_far` missing a seat key → no exclusion added (no KeyError).
- Non-monotonic `clock.now_ms()` → `can_reserve` still returns correctly (clamp defended at Round 7).
- Deterministic replay — same state twice → same `CascadeSelection`.
- V1 rebind-resistance — cascade does not depend on any §8 constants (confirm by grep + monkeypatch probe).
- `vault_read` raising `KeyError` (endpoint path absent) → error propagates unwrapped (E-023 residual — trusted-operator envelope).
- Malformed rate-limiter state at probed endpoint → `JSONDecodeError` / `ValueError` propagates unwrapped.
- Zero-capacity / zero-refill bucket at probed endpoint → skipped via `can_reserve` returning False (regression pin).
- Seat-kind "scribe" never excludes any family (even when scribe has already landed — irrelevant for scribe's own seat).
- Large cascade (20+ levels) — probe_count pinned; early-exit on first match (no over-probe).
- `can_reserve` called exactly once per probed level (no double-probe).

## Done definition

- [ ] `pipeline/loop/cascade.py` ships with `select_cascade_level` + `CascadeSelection` + any necessary `CascadeLevel` dataclass-extension.
- [ ] 100% coverage on the module via the two test files.
- [ ] Full suite green (baseline 4333 → target ≥ 4359 after +26 tests).
- [ ] AST-lint R1–R7 on `pipeline/loop/` clean.
- [ ] `pipeline/loop/__init__.py` re-exports public surface.
- [ ] `lock_history.v1.jsonl` entry.
- [ ] MEMORY.md index + round-recap memory file.
- [ ] Pre-stage Round 9 spec card (§4.10 cron scheduler OR §4.11 tab delivery — operator confirms).

## Lines-of-code target (E-024 2× multiplier)

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/loop/cascade.py` | 250 | 190–310 | Selection loop + family-exclusion helper + F_PIPE_08 dispatch + 1 result dataclass. Simpler than Round 7 (no CAS loop, no refill arithmetic). |
| `tests/loop/test_cascade.py` | 400 | 300–500 | ~12 tests × ~35 LOC/test with shared fakes. |
| `tests/loop/test_adv_cascade.py` | 650 | 490–810 | ~14 adv tests × 2× multiplier. |

## Self-LOCK eligibility

**Eligible if single-cycle pass.** Pure §5 orchestrator selector — no network, no subprocess, no §4 Logician consumption. Consumes only already-LOCKed primitives (Round 1 + Round 7). Follow §5 R3/R4/R5/R6/R7 precedent.

## Round 9+ preview

**Round 9 candidate A** — `pipeline/loop/tab_delivery.py` — §4.11 three-tab envelope ordering + signing (TabEnvelope from Round 1 + §2 vault primitives).

**Round 9 candidate B** — `pipeline/loop/cron_scheduler.py` — §4.10 v2 flock + vault-stamp two-layer dedupe, DST-safe task-id, F_PIPE_15 cron dedupe failure.

**Round 10-12** — eval-mode orchestrator (§4.15), golden-set scoring (§4.14), calibration-report (§4.16), capstone `run_pipeline.py` wiring all §5 rounds.

## Open questions (resolve at ORIENT)

1. **`CascadeLevel` shape.** Need Round 1 types.py re-read to confirm presence + field names. If absent, Round 8 adds it as a frozen slotted dataclass alongside the selector.

2. **`run_iteration_families_so_far` shape + mutation path.** Who writes this field? Round 4 `invoke_seat` (on landed family recording)? Round 5 inner-loop? Round 8 reads it but does not mutate. Confirm writer is upstream.

3. **Review-seat handling.** Blueprint §4.9 line 649 defers review-seat exhaustion to `graceful_degradation.request_bypass_authorization` (§4.12). Round 8 does NOT handle review-seat special-casing — it raises F_PIPE_08 uniformly. Confirm: review-seat invocation does not go through `select_cascade_level` (review is post-POST-gate, §M13).

4. **`can_reserve` failure modes.** If `vault_read` raises on an endpoint whose rate-limiter file has never been initialised (first-run boot), what is the expected behaviour? Propose: Round 8 lets `KeyError` propagate (E-023 residual) — operators must ensure per-endpoint state files exist as part of `start_run` boot. Document explicitly.

5. **Concurrency.** Two iterations racing on cascade selection for the same seat — each call does its own `vault_read` of rate-limiter state. The `can_reserve` result can become stale between probe and the subsequent `reserve`. Is this documented as a benign race (the subsequent `reserve` will return `InsufficientTokens` and the caller re-enters cascade selection)? Propose: yes, document in module docstring.
