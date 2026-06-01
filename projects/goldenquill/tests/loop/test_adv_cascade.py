"""Adversarial tests for pipeline.loop.cascade — §4.9 v2 selector.

Blueprint §5 v6 §4.9 LOCKED 2026-04-19.

E-024 2× multiplier applied to spec-card adversarial floor (14 → 28
effective). Coverage is 100% on the module; these tests pin edge-case
behaviour that the happy-path suite does not exercise:

- F_PIPE_08 trigger taxonomy (exact string + details shape).
- Empty cascade tail (``current_level_index == len(levels)``) — fast
  exhaustion path.
- All levels same-family editor (sole family landed) — exhausts.
- All levels rate-limited — exhausts with full ``skipped_for_capacity``.
- ``run_iteration_families_so_far`` missing a seat key → no KeyError.
- Non-monotonic clock — ``can_reserve`` refill clamps at zero.
- Deterministic replay — same inputs → same selection.
- V1 rebind-resistance — no §8 constants consulted (grep + monkeypatch).
- ``vault_read`` KeyError on missing state file propagates unwrapped.
- Malformed rate-limiter bytes → ``JSONDecodeError`` / ``ValueError``
  propagate unwrapped.
- Zero-capacity / zero-refill bucket → skipped as capacity=False.
- Scribe exhaustion scenario (trigger string confirmation).
- Invalid ``levels`` / ``current_level_index`` → ValueError.
- Early-exit no-over-probe regression.
- Unrecognised seat_kind → no exclusion (falls through).
- Family-exclusion derivation via helper directly.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any

import pytest

from pipeline.loop import config as loop_config
from pipeline.loop.cascade import (
    CascadeLevel,
    CascadeSelection,
    _derive_excluded_families,
    select_cascade_level,
)
from pipeline.loop.errors import F_PIPE_08
from pipeline.loop.rate_limiter import TokenBucket
from pipeline.loop.types import RateLimiterState, RunState


# ---------------------------------------------------------------------------
# Shared fakes (mirror test_cascade.py — duplicated for self-containment)
# ---------------------------------------------------------------------------


def _mk_runstate(
    *,
    run_id: str = "run-ADV",
    landed: dict[str, tuple[str, str]] | None = None,
) -> RunState:
    return RunState(
        schema_version=2,
        run_id=run_id,
        mode="submission",
        rfa_hash="rfa",
        project_context_hash="pc",
        golden_set_ref=None,
        org_slug="org",
        session_id="sess",
        phase="inner_loop_iter_1",
        run_iteration_families_so_far=landed or {},
    )


def _mk_state(
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
    refill_rate_per_sec: float = 10.0,
) -> None:
    vault.store[
        f"pipeline/rate_limiter/{endpoint}.json"
    ] = _serialize(
        _mk_state(
            endpoint=endpoint,
            capacity=capacity,
            tokens=tokens,
            refill_rate_per_sec=refill_rate_per_sec,
        )
    )


def _mk_level(
    *,
    family: str = "anthropic",
    provider_endpoint: str = "ep",
    budget: int = 10,
    model_id: str = "model-1",
) -> CascadeLevel:
    return CascadeLevel(
        family=family,
        provider_endpoint=provider_endpoint,
        estimated_tokens_budget=budget,
        model_id=model_id,
    )


# ---------------------------------------------------------------------------
# TestFailureTaxonomy — F_PIPE_08 trigger + details pin
# ---------------------------------------------------------------------------


class TestFailureTaxonomy:
    def test_trigger_string_exact_pin(self) -> None:
        levels = (_mk_level(family="anthropic", provider_endpoint="ep-a"),)
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a", tokens=0.0, refill_rate_per_sec=0.0)

        with pytest.raises(F_PIPE_08) as exc_info:
            select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(run_id="run-42"),
                vault_read=vault.read,
                clock=_FakeClock(),
            )
        assert (
            exc_info.value.trigger
            == "cross_family_exhausted:scribe:run-42"
        )
        assert exc_info.value.CODE == "F-PIPE-08"
        assert exc_info.value.SEVERITY == "CRIT"

    def test_details_shape_pin(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
            _mk_level(family="google", provider_endpoint="ep-g", budget=100),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-g", tokens=5.0, refill_rate_per_sec=0.0)

        with pytest.raises(F_PIPE_08) as exc_info:
            select_cascade_level(
                seat_kind="editor",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(
                    run_id="run-D",
                    landed={"scribe": ("anthropic", "ep-a-scribe")},
                ),
                vault_read=vault.read,
                clock=_FakeClock(),
            )
        d = exc_info.value.details
        assert d["seat_kind"] == "editor"
        assert d["run_id"] == "run-D"
        assert d["excluded_families"] == ["anthropic"]
        assert d["skipped_for_capacity"] == ["ep-g"]
        assert d["probe_count"] == 2
        assert d["cascade_length"] == 2
        assert d["current_level_index"] == 0


# ---------------------------------------------------------------------------
# TestEmptyTail — current_level_index == len(levels)
# ---------------------------------------------------------------------------


class TestEmptyTail:
    def test_empty_tail_scribe_exhausts_immediately(self) -> None:
        levels = (_mk_level(),)
        vault = _FakeVault()

        with pytest.raises(F_PIPE_08) as exc_info:
            select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=1,
                run_state=_mk_runstate(),
                vault_read=vault.read,
                clock=_FakeClock(),
            )
        # Empty tail → no probes, no skips, no excluded families.
        d = exc_info.value.details
        assert d["skipped_for_capacity"] == []
        assert d["excluded_families"] == []
        assert d["probe_count"] == 0
        assert d["current_level_index"] == 1
        # Vault never touched.
        assert vault.read_calls == []


# ---------------------------------------------------------------------------
# TestAllLevelsSameFamilyEditor — cross-family exhaust
# ---------------------------------------------------------------------------


class TestAllLevelsSameFamilyEditor:
    def test_editor_single_family_exhausts(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a1"),
            _mk_level(family="anthropic", provider_endpoint="ep-a2"),
        )
        vault = _FakeVault()

        with pytest.raises(F_PIPE_08) as exc_info:
            select_cascade_level(
                seat_kind="editor",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(
                    landed={"scribe": ("anthropic", "ep-a-scribe")}
                ),
                vault_read=vault.read,
                clock=_FakeClock(),
            )
        d = exc_info.value.details
        assert d["excluded_families"] == ["anthropic"]
        # Every level skipped for family → no capacity probes.
        assert d["skipped_for_capacity"] == []
        # Both levels inspected (neither returned capacity).
        assert d["probe_count"] == 2
        # Vault never touched — capacity never probed.
        assert vault.read_calls == []


# ---------------------------------------------------------------------------
# TestAllLevelsRateLimited — capacity exhausts
# ---------------------------------------------------------------------------


class TestAllLevelsRateLimited:
    def test_every_endpoint_empty_exhausts(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a", budget=100),
            _mk_level(family="google", provider_endpoint="ep-g", budget=100),
            _mk_level(family="meta", provider_endpoint="ep-m", budget=100),
        )
        vault = _FakeVault()
        for ep in ("ep-a", "ep-g", "ep-m"):
            _preload(vault, endpoint=ep, tokens=0.0, refill_rate_per_sec=0.0)

        with pytest.raises(F_PIPE_08) as exc_info:
            select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(),
                vault_read=vault.read,
                clock=_FakeClock(),
            )
        d = exc_info.value.details
        assert d["skipped_for_capacity"] == ["ep-a", "ep-g", "ep-m"]
        assert d["probe_count"] == 3


# ---------------------------------------------------------------------------
# TestMissingSeatKey — no KeyError on absent 'scribe' / 'editor'
# ---------------------------------------------------------------------------


class TestMissingSeatKey:
    def test_editor_seat_no_scribe_landed_no_exclusion(self) -> None:
        levels = (_mk_level(family="anthropic", provider_endpoint="ep-a"),)
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a")

        # Editor dispatches before scribe's family is recorded — happens
        # if §4.1 step 3 invokes editor without a prior scribe-landed
        # record (unusual, but defended).
        result = select_cascade_level(
            seat_kind="editor",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(landed={}),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        assert result.selected_level is levels[0]
        assert result.excluded_families == frozenset()

    def test_judge_seat_only_editor_landed(self) -> None:
        levels = (_mk_level(family="anthropic", provider_endpoint="ep-a"),)
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a")

        # Only editor family is recorded — judge excludes it but NOT the
        # absent scribe key (no KeyError).
        with pytest.raises(F_PIPE_08):
            select_cascade_level(
                seat_kind="judge",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(
                    landed={"editor": ("anthropic", "ep-a-ed")}
                ),
                vault_read=vault.read,
                clock=_FakeClock(),
            )


# ---------------------------------------------------------------------------
# TestClockEdgeCases — non-monotonic clock clamps via Round 7
# ---------------------------------------------------------------------------


class TestClockEdgeCases:
    def test_non_monotonic_clock_still_selects(self) -> None:
        """Round 7's ``can_reserve`` clamps negative refill delta at zero."""
        levels = (_mk_level(family="anthropic", provider_endpoint="ep-a"),)
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a")

        # Clock now_ms() is BEFORE the last_refill_iso anchor (1_745_... ms).
        clock = _FakeClock(value=1_000_000)
        result = select_cascade_level(
            seat_kind="scribe",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(),
            vault_read=vault.read,
            clock=clock,
        )
        assert result.selected_level is levels[0]


# ---------------------------------------------------------------------------
# TestDeterministicReplay — same inputs → same selection
# ---------------------------------------------------------------------------


class TestDeterministicReplay:
    def test_two_invocations_same_result(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a", budget=100),
            _mk_level(family="google", provider_endpoint="ep-g"),
        )

        def _run() -> CascadeSelection:
            vault = _FakeVault()
            _preload(vault, endpoint="ep-a", tokens=5.0, refill_rate_per_sec=0.0)
            _preload(vault, endpoint="ep-g")
            return select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(),
                vault_read=vault.read,
                clock=_FakeClock(),
            )

        a = _run()
        b = _run()
        assert a == b


# ---------------------------------------------------------------------------
# TestRebindResistance — §8 constants not consulted
# ---------------------------------------------------------------------------


class TestRebindResistance:
    def test_no_section_8_constant_rebind_affects_dispatch(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Rebinding every §8 constant must not alter cascade selection.

        cascade.py inline-literals the seat-kind strings and does not
        import any §8 constants itself. It transitively consumes
        :mod:`pipeline.loop.rate_limiter` which has its own rebind
        resistance tests; here we pin cascade-level non-dependence.
        """
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a", budget=100),
            _mk_level(family="google", provider_endpoint="ep-g"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a", tokens=5.0, refill_rate_per_sec=0.0)
        _preload(vault, endpoint="ep-g")

        # Rebind a few §8 constants to values that would break cascade
        # behaviour IF they were consulted. They must not be.
        monkeypatch.setattr(
            loop_config, "RATE_LIMIT_JITTER_RANGE_MS", (999, 999)
        )
        monkeypatch.setattr(
            loop_config, "RATE_LIMIT_LEASE_TTL_SEC", 1
        )
        monkeypatch.setattr(loop_config, "MAX_REVISION_ITERATIONS", 99)

        result = select_cascade_level(
            seat_kind="editor",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(
                landed={"scribe": ("anthropic", "ep-a-scribe")}
            ),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        # anthropic excluded → google returned. Behaviour unchanged.
        assert result.selected_level is levels[1]

    def test_no_config_imports_in_source(self) -> None:
        """Grep-check: cascade.py does not import any §8 constant."""
        from pathlib import Path

        # Resolve relative to __file__ so the test works under pytest-xdist
        # workers whose cwd may differ from the repo root.
        repo_root = Path(__file__).resolve().parents[2]
        src = (repo_root / "pipeline" / "loop" / "cascade.py").read_text(
            encoding="utf-8"
        )
        # The only pipeline.loop.config reference allowed would be a
        # comment; there must be NO `from pipeline.loop.config import ...`
        # or `import pipeline.loop.config` at module scope.
        lines = [
            line
            for line in src.splitlines()
            if line.strip().startswith(("import ", "from "))
        ]
        for line in lines:
            assert "pipeline.loop.config" not in line, (
                f"cascade.py imports from pipeline.loop.config "
                f"— §8-constant dependency forbidden: {line!r}"
            )


# ---------------------------------------------------------------------------
# TestResiduals — E-023 unwrapped-propagation contract
# ---------------------------------------------------------------------------


class TestResiduals:
    def test_missing_state_file_raises_keyerror(self) -> None:
        levels = (_mk_level(family="anthropic", provider_endpoint="ep-ghost"),)
        vault = _FakeVault()  # nothing preloaded.

        with pytest.raises(KeyError):
            select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(),
                vault_read=vault.read,
                clock=_FakeClock(),
            )

    def test_malformed_state_bytes_raises_json_decode_error(self) -> None:
        levels = (_mk_level(family="anthropic", provider_endpoint="ep-a"),)
        vault = _FakeVault()
        vault.store["pipeline/rate_limiter/ep-a.json"] = b"not-json"

        with pytest.raises(json.JSONDecodeError):
            select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(),
                vault_read=vault.read,
                clock=_FakeClock(),
            )

    def test_endpoint_absent_from_buckets_raises_keyerror(self) -> None:
        levels = (_mk_level(family="anthropic", provider_endpoint="ep-x"),)
        vault = _FakeVault()
        # Preload state file but under a DIFFERENT bucket key.
        other_state = _mk_state(endpoint="ep-y")
        vault.store["pipeline/rate_limiter/ep-x.json"] = _serialize(
            other_state
        )

        with pytest.raises(KeyError):
            select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=0,
                run_state=_mk_runstate(),
                vault_read=vault.read,
                clock=_FakeClock(),
            )


# ---------------------------------------------------------------------------
# TestZeroCapacityBucket — bucket is empty + never refills → always skipped
# ---------------------------------------------------------------------------


class TestZeroCapacityBucket:
    def test_zero_tokens_zero_refill_skipped(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a", budget=1),
            _mk_level(family="google", provider_endpoint="ep-g", budget=1),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a", tokens=0.0, refill_rate_per_sec=0.0)
        _preload(vault, endpoint="ep-g", tokens=100.0)

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


# ---------------------------------------------------------------------------
# TestInputValidation — ValueError on malformed inputs
# ---------------------------------------------------------------------------


class TestInputValidation:
    def test_empty_levels_raises(self) -> None:
        with pytest.raises(ValueError, match="levels must be non-empty"):
            select_cascade_level(
                seat_kind="scribe",
                levels=(),
                current_level_index=0,
                run_state=_mk_runstate(),
                vault_read=_FakeVault().read,
                clock=_FakeClock(),
            )

    def test_negative_current_level_index_raises(self) -> None:
        levels = (_mk_level(),)
        with pytest.raises(
            ValueError, match="current_level_index out of range"
        ):
            select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=-1,
                run_state=_mk_runstate(),
                vault_read=_FakeVault().read,
                clock=_FakeClock(),
            )

    def test_out_of_range_current_level_index_raises(self) -> None:
        levels = (_mk_level(),)
        with pytest.raises(
            ValueError, match="current_level_index out of range"
        ):
            select_cascade_level(
                seat_kind="scribe",
                levels=levels,
                current_level_index=2,
                run_state=_mk_runstate(),
                vault_read=_FakeVault().read,
                clock=_FakeClock(),
            )


# ---------------------------------------------------------------------------
# TestNoOverProbe — regression: once hit, stop
# ---------------------------------------------------------------------------


class TestNoOverProbe:
    def test_first_eligible_stops_probe_no_read_subsequent(self) -> None:
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a"),
            _mk_level(family="google", provider_endpoint="ep-g"),
            _mk_level(family="meta", provider_endpoint="ep-m"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a")
        # ep-g, ep-m intentionally NOT preloaded — if selector over-probes,
        # we'd see KeyError from the vault fake.

        result = select_cascade_level(
            seat_kind="scribe",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        assert result.selected_level is levels[0]
        assert vault.read_calls == ["pipeline/rate_limiter/ep-a.json"]

    def test_can_reserve_called_exactly_once_per_probed_level(self) -> None:
        """Each probed level must invoke ``can_reserve`` exactly once."""
        levels = (
            _mk_level(family="anthropic", provider_endpoint="ep-a", budget=100),
            _mk_level(family="google", provider_endpoint="ep-g"),
        )
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a", tokens=5.0, refill_rate_per_sec=0.0)
        _preload(vault, endpoint="ep-g")

        select_cascade_level(
            seat_kind="scribe",
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        # Exactly one read per probed endpoint.
        assert vault.read_calls == [
            "pipeline/rate_limiter/ep-a.json",
            "pipeline/rate_limiter/ep-g.json",
        ]


# ---------------------------------------------------------------------------
# TestUnrecognisedSeatKind — falls through to no-exclusion
# ---------------------------------------------------------------------------


class TestUnrecognisedSeatKind:
    def test_unknown_seat_kind_no_exclusion(self) -> None:
        """An unrecognised seat_kind is treated as "no family exclusion".

        The blueprint pseudo-code only enumerates editor + judge branches;
        the scribe/default branch is no-op. Round 8 matches verbatim.
        """
        levels = (_mk_level(family="anthropic", provider_endpoint="ep-a"),)
        vault = _FakeVault()
        _preload(vault, endpoint="ep-a")

        result = select_cascade_level(
            seat_kind="observer",  # not a declared SeatKind
            levels=levels,
            current_level_index=0,
            run_state=_mk_runstate(
                landed={"scribe": ("anthropic", "ep-a-scribe")}
            ),
            vault_read=vault.read,
            clock=_FakeClock(),
        )
        # Despite scribe having landed anthropic, the unrecognised
        # seat_kind does not exclude.
        assert result.selected_level is levels[0]
        assert result.excluded_families == frozenset()


# ---------------------------------------------------------------------------
# TestDeriveExcludedFamilies — helper unit coverage
# ---------------------------------------------------------------------------


class TestDeriveExcludedFamilies:
    def test_scribe_returns_empty(self) -> None:
        got = _derive_excluded_families(
            seat_kind="scribe",
            landed_so_far={
                "scribe": ("anthropic", "ep-a"),
                "editor": ("google", "ep-g"),
            },
        )
        assert got == frozenset()

    def test_editor_returns_scribe_family(self) -> None:
        got = _derive_excluded_families(
            seat_kind="editor",
            landed_so_far={"scribe": ("anthropic", "ep-a")},
        )
        assert got == frozenset({"anthropic"})

    def test_judge_returns_both_families(self) -> None:
        got = _derive_excluded_families(
            seat_kind="judge",
            landed_so_far={
                "scribe": ("anthropic", "ep-a"),
                "editor": ("google", "ep-g"),
            },
        )
        assert got == frozenset({"anthropic", "google"})

    def test_judge_empty_landed_returns_empty(self) -> None:
        got = _derive_excluded_families(
            seat_kind="judge", landed_so_far={}
        )
        assert got == frozenset()

    def test_unrecognised_seat_kind_returns_empty(self) -> None:
        got = _derive_excluded_families(
            seat_kind="observer",
            landed_so_far={"scribe": ("anthropic", "ep-a")},
        )
        assert got == frozenset()
