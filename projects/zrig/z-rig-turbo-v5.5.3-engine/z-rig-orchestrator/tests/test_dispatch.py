#!/usr/bin/env python3
"""
HRR-004 Builder 2 — tests/test_dispatch.py
Tests for dispatch.py: seat assignment, diversity enforcement,
T4 Hot Failover, cross-assignment (W4), independence (W5), timeout.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from zrig.dispatch import (
    AgentDispatcher,
    AgentStatus,
    DispatchConfig,
    ProviderError,
    SeatAssignment,
    WaveDispatchResult,
)
from zrig.families import (
    FamilyRegistry,
    DiversityViolationError,
    RegistryTamperError,
)
from zrig.agents import StubAgentRunner, wrap_in_envelope
from zrig.bundles import BundleAssembler, Bundle


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

AVAILABLE_MODELS = [
    "claude-opus-4",       # anthropic
    "gpt-4.1",             # openai
    "gemini-2.5-pro",      # google
    "grok-4",              # xai
    "deepseek-r1",         # deepseek
    "llama-4-maverick",    # meta-llama
    "mistral-large",       # mistral
    "command-r-plus",      # cohere
]


def make_config(
    *,
    w2_builder_count: int = 3,
    w4_verifier_count: int = 2,
    w5_squad_count: int = 2,
    failover_map: Dict = None,
    custom_bounds: Dict = None,
) -> DispatchConfig:
    return DispatchConfig(
        run_id="HRR-TEST-001",
        mode="STANDARD",
        provider_list=["anthropic", "openai", "google", "xai", "deepseek"],
        allowed_model_failover_map=failover_map or {
            "claude-opus-4": ["claude-sonnet-4"],
            "gpt-4.1": ["o3-pro"],
        },
        custom_timeouts={},
        custom_bounds=custom_bounds or {},
        w2_builder_count=w2_builder_count,
        w4_verifier_count=w4_verifier_count,
        w5_squad_count=w5_squad_count,
    )


def make_dispatcher(
    config: DispatchConfig = None,
    agent_runner=None,
) -> AgentDispatcher:
    registry = FamilyRegistry.default()
    registry.lock()
    return AgentDispatcher(
        config=config or make_config(),
        registry=registry,
        agent_runner=agent_runner,
    )


def make_bundle(wave: str = "W2") -> Bundle:
    assembler = BundleAssembler(run_id="HRR-TEST-001")
    source = {
        "requirements": {"functional": [{"id": "REQ-001", "priority": "MUST"}]},
        "failure_modes": [{"fm_id": "FM-001", "description": "test", "recovery": "none"}],
        "rubric": [{"criterion_id": "RC-001", "weight": 1.0, "pass_condition": "ok", "fail_condition": "nok"}],
        "build_directives": {},
        "mechanism_registry": {},
    }
    transition_map = {
        "W1→W2": assembler.transitions["W1→W2"],
    }
    return assembler.assemble("W1→W2", source)


# ---------------------------------------------------------------------------
# Family registry tests
# ---------------------------------------------------------------------------

class TestFamilyRegistry:

    def test_family_of_known_model(self):
        reg = FamilyRegistry.default()
        assert reg.family_of("claude-opus-4") == "anthropic"
        assert reg.family_of("gpt-4.1") == "openai"
        assert reg.family_of("gemini-2.5-pro") == "google"

    def test_family_of_unknown_model(self):
        reg = FamilyRegistry.default()
        assert reg.family_of("some-unknown-model-xyz") == "UNKNOWN"

    def test_diversity_check_pass(self):
        reg = FamilyRegistry.default()
        result = reg.diversity_check(
            ["claude-opus-4", "gpt-4.1", "gemini-2.5-pro"], min_families=3
        )
        assert result.ok is True
        assert result.count == 3

    def test_diversity_check_fail(self):
        reg = FamilyRegistry.default()
        result = reg.diversity_check(
            ["claude-opus-4", "claude-sonnet-4"], min_families=3
        )
        assert result.ok is False

    def test_registry_hash_lock_and_verify(self):
        reg = FamilyRegistry.default()
        h = reg.lock()
        assert len(h) == 64  # SHA-256 hex
        assert reg.verify_hash() is True

    def test_registry_tamper_detection(self):
        reg = FamilyRegistry.default()
        reg.lock()
        # Tamper
        reg.data["families"]["anthropic"]["models"].append("evil-model-x")
        with pytest.raises(RegistryTamperError):
            reg.verify_hash()

    def test_registry_hash_not_locked_raises(self):
        reg = FamilyRegistry.default()
        with pytest.raises(RuntimeError, match="not been locked"):
            reg.verify_hash()

    def test_cross_assignment_pass(self):
        reg = FamilyRegistry.default()
        # No exclusion violations
        reg.assert_cross_assignment(
            ["gpt-4.1", "gemini-2.5-pro"],
            excluded_families={"anthropic"},
            wave_label="W4",
        )

    def test_cross_assignment_fail(self):
        from zrig.families import CrossAssignmentError
        reg = FamilyRegistry.default()
        with pytest.raises(CrossAssignmentError, match="FM-INDEPENDENCE"):
            reg.assert_cross_assignment(
                ["claude-opus-4"],  # anthropic — excluded
                excluded_families={"anthropic"},
                wave_label="W4",
            )

    def test_full_mode_partition_feasible(self):
        reg = FamilyRegistry.default()
        families = ["anthropic", "openai", "google", "xai", "deepseek",
                    "meta-llama", "mistral", "cohere"]
        assert reg.full_mode_partition_feasible(families) is True

    def test_full_mode_partition_not_feasible(self):
        reg = FamilyRegistry.default()
        # Only 4 families — need 8 for full mode (5+3)
        assert reg.full_mode_partition_feasible(["anthropic", "openai", "google", "xai"]) is False


# ---------------------------------------------------------------------------
# Seat assignment tests
# ---------------------------------------------------------------------------

class TestSeatAssignment:

    def test_w2_assigns_three_diverse_seats(self):
        d = make_dispatcher()
        seats = d.assign_seats_w2(AVAILABLE_MODELS)
        assert len(seats) == 3
        families = {s.family_actual for s in seats}
        assert len(families) == 3

    def test_w2_assigns_five_seats_full_mode(self):
        config = make_config(w2_builder_count=5)
        d = make_dispatcher(config)
        seats = d.assign_seats_w2(AVAILABLE_MODELS)
        assert len(seats) == 5
        families = {s.family_actual for s in seats}
        assert len(families) == 5

    def test_w2_diversity_violation_raises(self):
        d = make_dispatcher()
        # Only 2 distinct-family models
        with pytest.raises(DiversityViolationError, match="FM-DIVERSITY"):
            d.assign_seats_w2(["claude-opus-4", "claude-sonnet-4"])

    def test_w4_excludes_w3_family(self):
        d = make_dispatcher(make_config(w4_verifier_count=2))
        # Simulate W3 used anthropic
        d._w3_primary_families.add("anthropic")
        seats = d.assign_seats_w4(AVAILABLE_MODELS)
        for s in seats:
            assert s.family_actual != "anthropic", (
                f"W4 verifier {s.seat_id} uses excluded anthropic family"
            )

    def test_w5_excludes_w2_and_w3_families(self):
        d = make_dispatcher(make_config(w5_squad_count=2))
        # Simulate W2 used anthropic, openai; W3 used google
        d._wave_family_assignments["W2"] = {"anthropic", "openai"}
        d._wave_family_assignments["W3"] = {"google"}
        seats = d.assign_seats_w5(AVAILABLE_MODELS)
        for s in seats:
            assert s.family_actual not in {"anthropic", "openai", "google"}, (
                f"W5 squad {s.seat_id} uses excluded family {s.family_actual}"
            )

    def test_w5_diversity_violation_when_too_few_eligible(self):
        d = make_dispatcher(make_config(w5_squad_count=3))
        # Exclude all but 2 families
        d._wave_family_assignments["W2"] = {"anthropic", "openai", "google", "xai", "deepseek", "meta-llama"}
        d._wave_family_assignments["W3"] = {"mistral"}
        with pytest.raises(DiversityViolationError, match="FM-DIVERSITY"):
            d.assign_seats_w5(AVAILABLE_MODELS)

    def test_w1_panel_roles_assigned(self):
        d = make_dispatcher()
        seats = d.assign_seats_w1(AVAILABLE_MODELS)
        assert len(seats) == 5
        roles = {s.role for s in seats}
        assert "panel_correctness" in roles
        assert "panel_architecture" in roles

    def test_each_seat_has_unique_isolation_id(self):
        d = make_dispatcher()
        seats = d.assign_seats_w2(AVAILABLE_MODELS)
        ids = [s.agent_isolation_id for s in seats]
        assert len(set(ids)) == len(ids)


# ---------------------------------------------------------------------------
# T4 Hot Failover tests
# ---------------------------------------------------------------------------

class TestT4HotFailover:

    def test_failover_on_first_model_failure(self):
        """When primary model fails, dispatcher tries next in failover chain."""
        failover_map = {"claude-opus-4": ["gpt-4.1"]}
        config = make_config(w2_builder_count=1, failover_map=failover_map)

        # Fail claude-opus-4, succeed gpt-4.1
        runner = StubAgentRunner(fail_on_models=["claude-opus-4"], latency_s=0.0)
        d = make_dispatcher(config, agent_runner=runner)

        # Manually assign one seat
        d._wave_family_assignments["W2"] = set()  # avoid stale state
        seats = [SeatAssignment(
            seat_id="W2_builder_1_test",
            wave="W2",
            role="builder_1",
            model_requested="claude-opus-4",
            model_actual="claude-opus-4",
            family_actual="anthropic",
            agent_isolation_id=f"agent_test_{id(self)}",
        )]
        bundle = make_bundle("W2")

        result = asyncio.run(d.dispatch_wave("W2", seats, [bundle]))
        assert len(result.successful_results) == 1
        winning = result.successful_results[0]
        assert winning.model_actual == "gpt-4.1"
        assert winning.failover_count == 1
        assert "claude-opus-4" in winning.failover_chain
        assert len(result.failover_events) == 1
        assert result.failover_events[0]["event"] == "MODEL_SUBSTITUTED"

    def test_no_failover_on_success(self):
        """Successful primary model incurs no failover."""
        config = make_config(w2_builder_count=1)
        runner = StubAgentRunner()
        d = make_dispatcher(config, agent_runner=runner)
        seats = d.assign_seats_w2(["claude-opus-4"])

        bundle = make_bundle("W2")
        result = asyncio.run(d.dispatch_wave("W2", seats, [bundle]))
        assert len(result.successful_results) == 1
        assert result.successful_results[0].failover_count == 0
        assert len(result.failover_events) == 0

    def test_all_failovers_exhausted_returns_failed(self):
        """If all models in failover chain fail, result is FAILED."""
        failover_map = {"claude-opus-4": ["gpt-4.1"]}
        config = make_config(w2_builder_count=1, failover_map=failover_map)
        runner = StubAgentRunner(always_fail=True)
        d = make_dispatcher(config, agent_runner=runner)
        seats = d.assign_seats_w2(["claude-opus-4"])
        bundle = make_bundle("W2")

        result = asyncio.run(d.dispatch_wave("W2", seats, [bundle]))
        assert len(result.failed_results) == 1
        assert result.failed_results[0].status == AgentStatus.FAILED

    def test_timeout_triggers_failover(self):
        """Timed-out seat attempts failover to next model."""
        async def slow_then_fast(seat, bundle, model):
            if model == "claude-opus-4":
                await asyncio.sleep(10)  # Will timeout
            seat.model_actual = model
            return wrap_in_envelope({"stub": True}, seat)

        failover_map = {"claude-opus-4": ["gpt-4.1"]}
        config = make_config(w2_builder_count=1, failover_map=failover_map)
        config.custom_timeouts["W2"] = 100  # 100ms timeout (claude-opus-4 will exceed this)

        registry = FamilyRegistry.default()
        registry.lock()
        d = AgentDispatcher(config=config, registry=registry, agent_runner=slow_then_fast)
        seats = d.assign_seats_w2(["claude-opus-4"])
        bundle = make_bundle("W2")

        result = asyncio.run(d.dispatch_wave("W2", seats, [bundle]))
        # gpt-4.1 should succeed after claude times out
        assert len(result.successful_results) == 1
        assert result.successful_results[0].model_actual == "gpt-4.1"

    def test_wave_failover_budget_enforced(self):
        """After max_failover_per_wave exceeded, subsequent seats can't failover."""
        # 3 seats, each fails primary — but budget is 2
        failover_map = {
            "claude-opus-4": ["gpt-4.1"],
            "gemini-2.5-pro": ["grok-4"],
            "deepseek-r1": ["llama-4-maverick"],
        }
        config = make_config(
            w2_builder_count=3,
            failover_map=failover_map,
            custom_bounds={"max_failover_per_wave": 2, "max_failover_per_seat": 1},
        )
        runner = StubAgentRunner(
            fail_on_models=["claude-opus-4", "gemini-2.5-pro", "deepseek-r1"]
        )
        d = make_dispatcher(config, agent_runner=runner)
        seats = d.assign_seats_w2(AVAILABLE_MODELS)
        bundles = [make_bundle("W2") for _ in seats]

        result = asyncio.run(d.dispatch_wave("W2", seats, bundles))
        # Wave failover count should not exceed max
        assert result.wave_failover_count <= 2


# ---------------------------------------------------------------------------
# Parallel dispatch tests
# ---------------------------------------------------------------------------

class TestParallelDispatch:

    def test_three_builders_dispatch_in_parallel(self):
        """W2: 3 builders should all succeed."""
        config = make_config(w2_builder_count=3)
        runner = StubAgentRunner()
        d = make_dispatcher(config, agent_runner=runner)
        seats = d.assign_seats_w2(AVAILABLE_MODELS)
        bundles = [make_bundle("W2") for _ in seats]

        result = asyncio.run(d.dispatch_wave("W2", seats, bundles))
        assert len(result.successful_results) == 3

    def test_concurrency_limit_respected(self):
        """Semaphore keeps concurrent agents ≤ limit."""
        concurrent_peak = [0]
        current = [0]

        async def tracking_runner(seat, bundle, model):
            current[0] += 1
            concurrent_peak[0] = max(concurrent_peak[0], current[0])
            await asyncio.sleep(0.05)
            current[0] -= 1
            return wrap_in_envelope({"stub": True}, seat)

        config = make_config(w2_builder_count=3)
        config.concurrency_limit = 2  # max 2 at once
        registry = FamilyRegistry.default()
        registry.lock()
        d = AgentDispatcher(config=config, registry=registry, agent_runner=tracking_runner)
        seats = d.assign_seats_w2(AVAILABLE_MODELS)
        bundles = [make_bundle("W2") for _ in seats]

        asyncio.run(d.dispatch_wave("W2", seats, bundles))
        assert concurrent_peak[0] <= 2


# ---------------------------------------------------------------------------
# Post-dispatch diversity verification
# ---------------------------------------------------------------------------

class TestPostDispatchDiversityVerification:

    def test_verify_wave_diversity_pass(self):
        from zrig.dispatch import AgentResult
        d = make_dispatcher()
        wave_result = WaveDispatchResult(
            wave="W2",
            seats=[],
            results=[
                AgentResult(seat_id="s1", agent_isolation_id="a1", model_actual="claude-opus-4",
                            family_actual="anthropic", wave="W2", status=AgentStatus.SUCCESS),
                AgentResult(seat_id="s2", agent_isolation_id="a2", model_actual="gpt-4.1",
                            family_actual="openai", wave="W2", status=AgentStatus.SUCCESS),
                AgentResult(seat_id="s3", agent_isolation_id="a3", model_actual="gemini-2.5-pro",
                            family_actual="google", wave="W2", status=AgentStatus.SUCCESS),
            ],
            elapsed_ms=100.0,
            failover_events=[],
            timeout_events=[],
        )
        assert d.verify_wave_diversity(wave_result, min_families=3) is True

    def test_verify_wave_diversity_fail(self):
        from zrig.dispatch import AgentResult
        d = make_dispatcher()
        wave_result = WaveDispatchResult(
            wave="W2",
            seats=[],
            results=[
                AgentResult(seat_id="s1", agent_isolation_id="a1", model_actual="claude-opus-4",
                            family_actual="anthropic", wave="W2", status=AgentStatus.SUCCESS),
                AgentResult(seat_id="s2", agent_isolation_id="a2", model_actual="claude-sonnet-4",
                            family_actual="anthropic", wave="W2", status=AgentStatus.SUCCESS),
            ],
            elapsed_ms=100.0,
            failover_events=[],
            timeout_events=[],
        )
        with pytest.raises(DiversityViolationError, match="FM-DIVERSITY"):
            d.verify_wave_diversity(wave_result, min_families=3)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
