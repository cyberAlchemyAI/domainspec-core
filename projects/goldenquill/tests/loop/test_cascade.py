"""Tests for pipeline.loop.cascade — §4.9 v2 select_cascade_level.

Blueprint §5 v6 §4.9 LOCKED 2026-04-19.

Happy-path coverage targets (spec card
``section_05_round_8_cascade.md``):

- Scribe seat — no family exclusion, first level returned when capacity.
- Editor seat — scribe-family excluded.
- Judge seat — scribe + editor families excluded.
- Capacity skip — second level returned when first is rate-limited.
- ``current_level_index > 0`` — earlier levels not probed.
- Combined family + capacity skip — deepest eligible level returned.
- ``CascadeSelection.probe_count`` reflects only inspected levels
  (early-exit on first hit — no over-probe).
- ``excluded_families`` pins the derived set.
- ``CascadeLevel`` construction invariants (non-empty family / endpoint
  / model_id; non-negative token budget).
- Zero-budget level probed with ``can_reserve(estimated_tokens=0)`` — any
  non-zero capacity satisfies.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

import pytest

from pipeline.loop.cascade import (
    CascadeLevel,
    CascadeSelection,
    select_cascade_level,
)
from pipeline.loop.rate_limiter import TokenBucket
from pipeline.loop.types import RateLimiterState, RunState


# ---------------------------------------------------------------------------
# Fixtures / fakes — mirror Round 7 test pattern (self-contained)
# ---------------------------------------------------------------------------


def _mk_runstate(
    *,
    run_id: str = "run-R",
    run_iteration_families_so_far: dict[str, tuple[str, str]] | None = None,
) -> RunState:
    """Build a valid submission-mode :class:`RunState` for cascade tests."""
    return RunState(
        schema_version=2,
        run_id=run_id,
        mode="submission",
        rfa_hash="rfa-hash",
        project_context_hash="pc-hash",
        golden_set_ref=None,
        org_slug="org-X",
        session_id="sess-S",
        phase="inner_loop_iter_1",
        run_iteration_families_so_far=run_iteration_families_so_far or {},
    )


def _mk_bucket_state(
    *,
    endpoint: str,
    capacity: int = 100,
    tokens: float = 100.0,
    refill_rate_per_sec: float = 10.0,
    last_refill_iso: str = "2026-04-21T12:00:00.000+00:00",
) -> RateLimiterState:
    return RateLimiterState(
        buckets={
            endpoint: TokenBucket(
                capacity=capacity,
                tokens=tokens,
                refill_rate_per_sec=refill_rate_per_sec,
            )
        },
        last_refill_iso=last_refill_iso,
    )


def _serialize(state: RateLimiterState) -> bytes:
    return json.dumps(
        asdict(state), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


@dataclass
class _FakeClock:
    value: int = 1_714_000_000_000

    def now_ms(self) -> int:
        return self.value

    def now_iso(self) -> str:
        return "2026-04-21T12:00:00.000+00:00"


@dataclass
class _FakeVault:
    """In-process read-only vault fake — cascade.py never writes."""

    store: dict[str, bytes] = field(default_factory=dict)
    read_calls: list[str] = field(default_factory=list)

    def read(self, *, path: str) -> bytes:
        self.read_calls.append(path)
        if path not in self.store:
            raise KeyError(path)
        return self.store[path]


def _preload(
    vault: _FakeVault,
    *,
    endpoint: str,
    tokens: float = 100.0,
    capacity: int = 100,
) -> None:
    state = _mk_bucket_state(
        endpoint=endpoint, capacity=capacity, tokens=tokens
    )
    vault.store[f"pipeline/rate_limiter/{endpoint}.json"] = _serialize(state)


def _mk_level(
    *,
    family: str,
    provider_endpoint: str,
    estimated_tokens_budget: int = 10,
    model_id: str | None = None,
) -> CascadeLevel:
    return CascadeLevel(
        family=family,
        provider_endpoint=provider_endpoint,
        estimated_tokens_budget=estimated_tokens_budget,
        model_id=model_id or f"{family}-model-1",
    )


# ---------------------------------------------------------------------------
# TestScribeSeat — no family exclusion ever
# ---------------------------------------------------------------------------


class TestScribeSeat:
    def test_scribe_first_level_returned_no_landed_seats(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
            _mk_level(family="google", provider_endpoint="ep-g"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a")
        _preload(vault, endpoint="ep-g")

        result = select_cascade_level(
            seat_kind="scribe",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(),
            vault_read=vault.read,
            clock=_FakeClock(),
        )

        assert isinstance(result, CascadeSelection)
        assert result.selected_level is levels[0]
        assert result.excluded_families == frozenset()
        assert result.skipped_for_capacity == ()
        assert result.probe_count == 1
        # Only the first endpoint was probed (early-exit).
        assert vault.read_calls == ["pipeline/rate_limiter/ep-a.json"]

    def test_scribe_no_exclusion_even_if_scribe_already_landed(self) -> None:
        """Scribe-seat dispatches for scribe never exclude scribe's own family."""
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a")

        result = select_cascade_level(
            seat_kind="scribe",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(
                run_iteration_families_so_far={
                    "scribe": ("anthropic", "ep-a"),
                }
            ),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        assert result.selected_level is levels[0]
        assert result.excluded_families == frozenset()


# ---------------------------------------------------------------------------
# TestEditorSeat — scribe-family excluded
# ---------------------------------------------------------------------------


class TestEditorSeat:
    def test_editor_excludes_scribe_family(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
            _mk_level(family="google", provider_endpoint="ep-g"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-g")

        result = select_cascade_level(
            seat_kind="editor",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(
                run_iteration_families_so_far={
                    "scribe": ("anthropic", "ep-a-scribe"),
                }
            ),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        # anthropic excluded → google level returned.
        assert result.selected_level is levels[1]
        assert result.excluded_families == frozenset({"anthropic"})
        assert result.skipped_for_capacity == ()
        assert result.probe_count == 2
        # anthropic endpoint never probed (skipped for family).
        assert vault.read_calls == ["pipeline/rate_limiter/ep-g.json"]


# ---------------------------------------------------------------------------
# TestJudgeSeat — scribe + editor families excluded
# ---------------------------------------------------------------------------


class TestJudgeSeat:
    def test_judge_excludes_both_scribe_and_editor(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
            _mk_level(family="google", provider_endpoint="ep-g"),
            _mk_level(family="meta", provider_endpoint="ep-m"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-m")

        result = select_cascade_level(
            seat_kind="judge",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(
                run_iteration_families_so_far={
                    "scribe": ("anthropic", "ep-a-scribe"),
                    "editor": ("google", "ep-g-editor"),
                }
            ),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        assert result.selected_level is levels[2]
        assert result.excluded_families == frozenset(
            {"anthropic", "google"}
        )
        assert result.probe_count == 3
        assert vault.read_calls == ["pipeline/rate_limiter/ep-m.json"]


# ---------------------------------------------------------------------------
# TestCapacitySkip — can_reserve=False forces probe forward
# ---------------------------------------------------------------------------


class TestCapacitySkip:
    def test_first_level_rate_limited_second_returned(self) -> None:
        levels = (
            _mk_level(
                family="anthropic",
                provider_endpoint="ep-a",
                estimated_tokens_budget=100,
            ),
            _mk_level(
                family="google",
                provider_endpoint="ep-g",
                estimated_tokens_budget=100,
            ),
        )
        vault = _FakeVault()
        # ep-a empty → can_reserve False; ep-g full → can_reserve True.
        _preload(vault, endpoint="ep-a", tokens=5.0, capacity=100)
        _preload(vault, endpoint="ep-g", tokens=100.0, capacity=100)

        result = select_cascade_level(
            seat_kind="scribe",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        assert result.selected_level is levels[1]
        assert result.skipped_for_capacity == ("ep-a",)
        assert result.probe_count == 2

    def test_combined_family_and_capacity_skip_returns_deepest(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
            _mk_level(
                family="google",
                provider_endpoint="ep-g",
                estimated_tokens_budget=100,
            ),
            _mk_level(family="meta", provider_endpoint="ep-m"),
        )
        vault = _FakeVault()
        # ep-g rate-limited; ep-m fine.
        _preload(vault, endpoint="ep-g", tokens=5.0, capacity=100)
        _preload(vault, endpoint="ep-m")

        result = select_cascade_level(
            seat_kind="editor",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(
                run_iteration_families_so_far={
                    "scribe": ("anthropic", "ep-a-scribe"),
                }
            ),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        assert result.selected_level is levels[2]
        # anthropic excluded by family; google skipped by capacity.
        assert result.excluded_families == frozenset({"anthropic"})
        assert result.skipped_for_capacity == ("ep-g",)
        assert result.probe_count == 3


# ---------------------------------------------------------------------------
# TestStartIndex — current_level_index > 0 prunes the head
# ---------------------------------------------------------------------------


class TestStartIndex:
    def test_current_level_index_skips_head(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
            _mk_level(family="google", provider_endpoint="ep-g"),
            _mk_level(family="meta", provider_endpoint="ep-m"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-g")

        result = select_cascade_level(
            seat_kind="scribe",
            levels=levels,
            current_level_index=1,
            run_state=_mk_runstate(),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        assert result.selected_level is levels[1]
        assert result.probe_count == 1
        # ep-a never probed.
        assert vault.read_calls == ["pipeline/rate_limiter/ep-g.json"]


# ---------------------------------------------------------------------------
# TestProbeCount — early-exit invariant
# ---------------------------------------------------------------------------


class TestProbeCount:
    def test_probe_count_matches_inspected_levels(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
            _mk_level(family="google", provider_endpoint="ep-g"),
            _mk_level(family="meta", provider_endpoint="ep-m"),
            _mk_level(family="openai", provider_endpoint="ep-o"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a")

        result = select_cascade_level(
            seat_kind="scribe",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        # Early-exit on first level → probe_count=1.
        assert result.probe_count == 1
        # Only one vault read.
        assert len(vault.read_calls) == 1


# ---------------------------------------------------------------------------
# TestCascadeLevelInvariants — __post_init__ edge cases
# ---------------------------------------------------------------------------


class TestCascadeLevelInvariants:
    def test_empty_family_raises(self) -> None:
        with pytest.raises(ValueError, match="family must be non-empty"):
            CascadeLevel(
                family="",
                provider_endpoint="ep",
                estimated_tokens_budget=10,
                model_id="m",
            )

    def test_empty_endpoint_raises(self) -> None:
        with pytest.raises(
            ValueError, match="provider_endpoint must be non-empty"
        ):
            CascadeLevel(
                family="f",
                provider_endpoint="",
                estimated_tokens_budget=10,
                model_id="m",
            )

    def test_empty_model_id_raises(self) -> None:
        with pytest.raises(ValueError, match="model_id must be non-empty"):
            CascadeLevel(
                family="f",
                provider_endpoint="ep",
                estimated_tokens_budget=10,
                model_id="",
            )

    def test_negative_budget_raises(self) -> None:
        with pytest.raises(
            ValueError, match="estimated_tokens_budget must be >= 0"
        ):
            CascadeLevel(
                family="f",
                provider_endpoint="ep",
                estimated_tokens_budget=-1,
                model_id="m",
            )

    def test_zero_budget_permitted(self) -> None:
        """A zero-budget probe is a valid no-op-capacity check."""
        level = CascadeLevel(
            family="f",
            provider_endpoint="ep",
            estimated_tokens_budget=0,
            model_id="m",
        )
        assert level.estimated_tokens_budget == 0


# ---------------------------------------------------------------------------
# TestPublicSurface — shape / re-export sanity
# ---------------------------------------------------------------------------


class TestPublicSurface:
    def test_cascade_selection_frozen(self) -> None:
        result = CascadeSelection(
            selected_level=_mk_level(family="f", provider_endpoint="ep"),
            excluded_families=frozenset(),
            skipped_for_capacity=(),
            probe_count=1,
        )
        with pytest.raises((AttributeError, TypeError)):
            setattr(result, "probe_count", 999)  # type: ignore[misc]

    def test_module_reexport_on_pipeline_loop(self) -> None:
        from pipeline.loop import (  # noqa: F401
            CascadeLevel as CL_re,
            CascadeSelection as CS_re,
            select_cascade_level as scl_re,
        )

        assert CL_re is CascadeLevel
        assert CS_re is CascadeSelection
        assert scl_re is select_cascade_level
