#!/usr/bin/env python3
"""
HRR-004 Builder 2 — dispatch.py
Agent Dispatch: Model Selection, Family Assignment, Parallel Execution, T4 Hot Failover.

Implements:
  - Model selection per wave from run_config model roster
  - Family assignment: cross-assignment for W4, independence for W5
  - Parallel execution with concurrency limits
  - Timeout enforcement (per-wave from run_config)
  - T4 Hot Failover: if model fails, try next in allowed_model_failover_map
  - Max 2 failovers per seat, 3 per wave (spec A.9 + pipeline_bounds)
  - MODEL_SUBSTITUTED structured event on every failover

Spec refs: A.2, A.2.3, A.2.4, A.9, A.10, A.13, B.3, 5.3, F.1 (TP-5)
"""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set, Tuple

from zrig.families import (
    FamilyRegistry,
    DiversityViolationError,
    CrossAssignmentError,
    UNKNOWN_FAMILY,
)


# ---------------------------------------------------------------------------
# Constants (spec A.10 pipeline_bounds)
# ---------------------------------------------------------------------------

MAX_FAILOVER_PER_SEAT: int = 2
MAX_FAILOVER_PER_WAVE: int = 3
TOTAL_PIPELINE_TIMEOUT_MS: int = 86_400_000  # 24h


# ---------------------------------------------------------------------------
# Wave-level defaults (operators may override via run_config.custom_timeouts)
# ---------------------------------------------------------------------------

DEFAULT_WAVE_TIMEOUTS_MS: Dict[str, int] = {
    "W0": 300_000,      # 5 min
    "W1": 1_800_000,    # 30 min
    "W2": 3_600_000,    # 60 min
    "W3": 3_600_000,    # 60 min
    "W4": 3_600_000,    # 60 min
    "W5": 3_600_000,    # 60 min
    "W5.5": 3_600_000,  # 60 min
    "W6": 3_600_000,    # 60 min (Full Mode)
    "W7": 3_600_000,    # 60 min (Full Mode)
    "W8": 1_800_000,    # 30 min
    "W8.5": 1_800_000,  # 30 min
    "W9": 1_800_000,    # 30 min
    "W10": 1_200_000,   # 20 min
    "W11": 900_000,     # 15 min
    "Wα-LOAD": 300_000,
    "Wα-WRITE": 300_000,
    "M0": 300_000,
    "M1": 900_000,
    "M2": 600_000,
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class AgentStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    FAILOVER = "FAILOVER"
    SKIPPED = "SKIPPED"


@dataclass
class SeatAssignment:
    """One seat in a wave: model selection, family, isolation ID."""
    seat_id: str
    wave: str
    role: str                         # e.g. "builder_1", "verifier_trace", "panel_chair"
    model_requested: str
    model_actual: str
    family_actual: str
    agent_isolation_id: str
    failover_count: int = 0
    failover_chain: List[str] = field(default_factory=list)  # models tried in order


@dataclass
class AgentResult:
    """Outcome of a single agent invocation."""
    seat_id: str
    agent_isolation_id: str
    model_actual: str
    family_actual: str
    wave: str
    status: AgentStatus
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    elapsed_ms: float = 0.0
    token_usage: Optional[Dict] = None
    failover_count: int = 0
    failover_chain: List[str] = field(default_factory=list)


@dataclass
class WaveDispatchResult:
    """Aggregated result of dispatching a whole wave."""
    wave: str
    seats: List[SeatAssignment]
    results: List[AgentResult]
    elapsed_ms: float
    failover_events: List[Dict]        # MODEL_SUBSTITUTED events
    timeout_events: List[Dict]
    wave_failover_count: int = 0

    @property
    def successful_results(self) -> List[AgentResult]:
        return [r for r in self.results if r.status == AgentStatus.SUCCESS]

    @property
    def failed_results(self) -> List[AgentResult]:
        return [r for r in self.results if r.status in (AgentStatus.FAILED, AgentStatus.TIMEOUT)]


# ---------------------------------------------------------------------------
# RunConfig helper (subset used by dispatch)
# ---------------------------------------------------------------------------

@dataclass
class DispatchConfig:
    """Dispatch-relevant slice of run_config."""
    run_id: str
    mode: str                           # MICRO | STANDARD | FULL
    provider_list: List[str]
    allowed_model_failover_map: Dict[str, List[str]]   # model → [failover candidates]
    custom_timeouts: Dict[str, int]                    # wave → ms override
    custom_bounds: Dict[str, Any]
    w1_panel_size: int = 5
    w2_builder_count: int = 3           # 1 | 3 | 5
    w4_verifier_count: int = 2          # 2–3
    w5_squad_count: int = 2             # 1–2
    w9_panel_size: int = 5
    concurrency_limit: int = 5          # max simultaneous agent calls

    def timeout_ms(self, wave: str) -> int:
        """Return per-wave timeout in ms (custom override > default)."""
        override = self.custom_timeouts.get(wave)
        if override is not None:
            return override
        return DEFAULT_WAVE_TIMEOUTS_MS.get(wave, 3_600_000)

    def max_failover_per_seat(self) -> int:
        return int(self.custom_bounds.get("max_failover_per_seat", MAX_FAILOVER_PER_SEAT))

    def max_failover_per_wave(self) -> int:
        return int(self.custom_bounds.get("max_failover_per_wave", MAX_FAILOVER_PER_WAVE))


# ---------------------------------------------------------------------------
# AgentDispatcher
# ---------------------------------------------------------------------------

class AgentDispatcher:
    """
    Central dispatcher: assembles seat assignments, enforces family rules,
    runs agents in parallel with concurrency limits, handles T4 Hot Failover.

    The actual agent execution is delegated to `agents.py` (OpenClaw integration).
    The dispatcher is responsible for:
      - Model selection from run_config roster
      - Family diversity enforcement (MECH-001)
      - Cross-assignment for W4 (no W3 primary synthesizer family)
      - Independence for W5 (no W2 ∪ W3 families)
      - Parallel execution with asyncio semaphore
      - Timeout enforcement (asyncio.wait_for)
      - T4 Hot Failover (try next in failover map on failure)
      - Structured MODEL_SUBSTITUTED events
    """

    def __init__(
        self,
        config: DispatchConfig,
        registry: FamilyRegistry,
        agent_runner: Optional[Callable] = None,
        event_emitter: Optional[Callable] = None,
    ):
        """
        Args:
            config: Dispatch configuration from run_config.
            registry: Locked FamilyRegistry (must have been locked at W0).
            agent_runner: Async callable(seat, bundle) → output dict.
                          Default: agents.run_agent_async (set at runtime).
            event_emitter: Optional callable(event_type, payload) for telemetry.
        """
        self.config = config
        self.registry = registry
        self.agent_runner = agent_runner
        self._emit = event_emitter or (lambda t, p: None)

        # Track family assignments across waves for cross-assignment enforcement
        self._wave_family_assignments: Dict[str, Set[str]] = {}  # wave → set of families
        self._w2_primary_families: Set[str] = set()   # families from W2 builders
        self._w3_primary_families: Set[str] = set()   # families from W3 synthesizers

    # ------------------------------------------------------------------ #
    # Public: wave dispatch                                               #
    # ------------------------------------------------------------------ #

    async def dispatch_wave(
        self,
        wave: str,
        seats: List[SeatAssignment],
        bundles: List[Any],             # List[Bundle] — one per seat
    ) -> WaveDispatchResult:
        """
        Dispatch all seats in a wave in parallel (respecting concurrency limit).
        Applies per-seat timeout and T4 Hot Failover.

        Args:
            wave: Wave identifier (e.g. "W2")
            seats: Pre-assigned seat list (use assign_seats_*() methods)
            bundles: One Bundle per seat (aligned by index)

        Returns:
            WaveDispatchResult with all agent outcomes.
        """
        assert len(seats) == len(bundles), "seats and bundles must be aligned"
        self._emit("WAVE_STARTED", {"run_id": self.config.run_id, "wave": wave, "seat_count": len(seats)})

        sem = asyncio.Semaphore(self.config.concurrency_limit)
        timeout_s = self.config.timeout_ms(wave) / 1000.0
        wave_failover_count = 0
        failover_events: List[Dict] = []
        timeout_events: List[Dict] = []

        async def run_seat(seat: SeatAssignment, bundle: Any) -> AgentResult:
            nonlocal wave_failover_count
            async with sem:
                return await self._run_with_failover(
                    seat=seat,
                    bundle=bundle,
                    timeout_s=timeout_s,
                    wave_failover_count_ref=[wave_failover_count],
                    failover_events=failover_events,
                    timeout_events=timeout_events,
                )

        start_ms = time.monotonic() * 1000
        tasks = [asyncio.create_task(run_seat(s, b)) for s, b in zip(seats, bundles)]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        elapsed = time.monotonic() * 1000 - start_ms

        # Track family assignments for subsequent cross-assignment checks
        self._wave_family_assignments[wave] = {
            r.family_actual for r in results if r.status == AgentStatus.SUCCESS
        }

        self._emit("WAVE_COMPLETED", {
            "run_id": self.config.run_id,
            "wave": wave,
            "elapsed_ms": elapsed,
            "success_count": sum(1 for r in results if r.status == AgentStatus.SUCCESS),
            "fail_count": sum(1 for r in results if r.status != AgentStatus.SUCCESS),
        })

        return WaveDispatchResult(
            wave=wave,
            seats=seats,
            results=list(results),
            elapsed_ms=elapsed,
            failover_events=failover_events,
            timeout_events=timeout_events,
            wave_failover_count=sum(r.failover_count for r in results),
        )

    # ------------------------------------------------------------------ #
    # Seat assignment helpers                                             #
    # ------------------------------------------------------------------ #

    def assign_seats_w2(self, available_models: List[str]) -> List[SeatAssignment]:
        """
        Assign W2 builder seats.
        - w2_builder_count seats (1|3|5 per run_config)
        - Each builder from a unique family (MECH-001)
        - Roles: builder_1, builder_2, builder_3, ...

        Raises DiversityViolationError if < w2_builder_count distinct families available.
        """
        n = self.config.w2_builder_count
        return self._assign_diverse_seats(
            wave="W2",
            n_seats=n,
            available_models=available_models,
            role_prefix="builder",
            excluded_families=set(),
        )

    def assign_seats_w3(
        self, available_models: List[str], w2_dominant_family: str
    ) -> List[SeatAssignment]:
        """
        Assign W3 synthesizer seats.
        - Primary synthesizer (any available family)
        - Conditional challenger: different family from primary
        Note: W3 primary family is recorded for W4 cross-assignment.

        Args:
            available_models: Full model roster
            w2_dominant_family: Family that produced dominant W2 output (excluded for challenger)
        """
        # Primary synthesizer: any available family
        seats = self._assign_diverse_seats(
            wave="W3",
            n_seats=1,
            available_models=available_models,
            role_prefix="synthesizer",
            excluded_families=set(),
        )
        if seats:
            self._w3_primary_families.add(seats[0].family_actual)

        # Challenger: different family from primary
        if len(seats) > 0:
            primary_family = seats[0].family_actual
            challenger_seats = self._assign_diverse_seats(
                wave="W3",
                n_seats=1,
                available_models=available_models,
                role_prefix="challenger",
                excluded_families={primary_family},
            )
            # Relabel role
            for s in challenger_seats:
                s.role = "challenger"
            seats.extend(challenger_seats)

        return seats

    def assign_seats_w4(self, available_models: List[str]) -> List[SeatAssignment]:
        """
        Assign W4 verifier seats.
        - w4_verifier_count seats
        - Cross-assignment: no verifier may share W3 primary synthesizer's family (Standard D14)
        - Verifier 1 → trace-role
        - Verifier 2 → requirements coverage
        - Verifier 3 (optional) → omniscient seat

        Raises CrossAssignmentError on violation.
        """
        roles = ["verifier_trace", "verifier_coverage", "verifier_omniscient"]
        seats = self._assign_diverse_seats(
            wave="W4",
            n_seats=self.config.w4_verifier_count,
            available_models=available_models,
            role_prefix="verifier",
            excluded_families=self._w3_primary_families,
        )
        for i, s in enumerate(seats):
            s.role = roles[i] if i < len(roles) else f"verifier_{i+1}"
        return seats

    def assign_seats_w5(self, available_models: List[str]) -> List[SeatAssignment]:
        """
        Assign W5 red team squad seats.
        - w5_squad_count squads
        - Independence (TP-5): families ∉ W2_families ∪ W3_families (Standard)
        - Squad 1 → technical attacks
        - Squad 2 → whole-artifact adversarial review (≥1 squad MUST do full review)

        Raises CrossAssignmentError if no eligible family available.
        """
        w2_families = self._wave_family_assignments.get("W2", set())
        w3_families = self._wave_family_assignments.get("W3", set())
        excluded = w2_families | w3_families

        roles = ["squad_technical", "squad_wholistic"]
        seats = self._assign_diverse_seats(
            wave="W5",
            n_seats=self.config.w5_squad_count,
            available_models=available_models,
            role_prefix="squad",
            excluded_families=excluded,
        )
        for i, s in enumerate(seats):
            s.role = roles[i] if i < len(roles) else f"squad_{i+1}"
        return seats

    def assign_seats_w1(self, available_models: List[str]) -> List[SeatAssignment]:
        """Assign W1 blueprint panel seats (w1_panel_size, ≥3 distinct families)."""
        roles = [
            "panel_correctness",
            "panel_architecture",
            "panel_safety",
            "panel_pragmatism",
            "panel_integration",
        ]
        seats = self._assign_diverse_seats(
            wave="W1",
            n_seats=self.config.w1_panel_size,
            available_models=available_models,
            role_prefix="panelist",
            excluded_families=set(),
        )
        for i, s in enumerate(seats):
            s.role = roles[i] if i < len(roles) else f"panelist_{i+1}"
        return seats

    def assign_seats_w9(self, available_models: List[str]) -> List[SeatAssignment]:
        """Assign W9 final panel seats (w9_panel_size)."""
        return self._assign_diverse_seats(
            wave="W9",
            n_seats=self.config.w9_panel_size,
            available_models=available_models,
            role_prefix="panelist",
            excluded_families=set(),
        )

    # ------------------------------------------------------------------ #
    # T4 Hot Failover                                                     #
    # ------------------------------------------------------------------ #

    async def _run_with_failover(
        self,
        seat: SeatAssignment,
        bundle: Any,
        timeout_s: float,
        wave_failover_count_ref: List[int],
        failover_events: List[Dict],
        timeout_events: List[Dict],
    ) -> AgentResult:
        """
        Execute one seat with T4 Hot Failover.
        Retries on failure up to max_failover_per_seat, bounded by max_failover_per_wave.
        On each failover, emits MODEL_SUBSTITUTED event.
        """
        models_to_try = [seat.model_actual] + self.config.allowed_model_failover_map.get(
            seat.model_requested, []
        )
        # Enforce per-seat cap
        models_to_try = models_to_try[: self.config.max_failover_per_seat() + 1]

        seat_failover_count = 0
        failover_chain: List[str] = []
        last_error: Optional[str] = None

        for attempt_idx, model in enumerate(models_to_try):
            # Check wave-level failover budget
            if attempt_idx > 0 and wave_failover_count_ref[0] >= self.config.max_failover_per_wave():
                last_error = (
                    f"FM-PROVIDER: wave failover budget exhausted "
                    f"({wave_failover_count_ref[0]}/{self.config.max_failover_per_wave()})"
                )
                break

            if attempt_idx > 0:
                # Emit MODEL_SUBSTITUTED (A.13.8)
                event = {
                    "event": "MODEL_SUBSTITUTED",
                    "run_id": self.config.run_id,
                    "wave": seat.wave,
                    "seat_id": seat.seat_id,
                    "requested": seat.model_requested,
                    "actual": model,
                    "reason": last_error or "PREVIOUS_ATTEMPT_FAILED",
                    "attempt": attempt_idx,
                    "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z",
                }
                failover_events.append(event)
                self._emit("MODEL_SUBSTITUTED", event)
                wave_failover_count_ref[0] += 1
                seat_failover_count += 1

            failover_chain.append(model)

            # Validate family is still OK after substitution
            family = self.registry.family_of(model)
            seat.model_actual = model
            seat.family_actual = family

            # Run with timeout
            start_ms = time.monotonic() * 1000
            try:
                output = await asyncio.wait_for(
                    self._invoke_agent(seat, bundle, model),
                    timeout=timeout_s,
                )
                elapsed = time.monotonic() * 1000 - start_ms
                return AgentResult(
                    seat_id=seat.seat_id,
                    agent_isolation_id=seat.agent_isolation_id,
                    model_actual=model,
                    family_actual=family,
                    wave=seat.wave,
                    status=AgentStatus.SUCCESS,
                    output=output,
                    elapsed_ms=elapsed,
                    failover_count=seat_failover_count,
                    failover_chain=failover_chain,
                )
            except asyncio.TimeoutError:
                elapsed = time.monotonic() * 1000 - start_ms
                event = {
                    "event": "WAVE_TIMEOUT",
                    "run_id": self.config.run_id,
                    "wave": seat.wave,
                    "seat_id": seat.seat_id,
                    "model": model,
                    "elapsed_ms": elapsed,
                    "timeout_ms": timeout_s * 1000,
                    "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z",
                }
                timeout_events.append(event)
                self._emit("WAVE_TIMEOUT", event)
                last_error = "TIMEOUT"
                # Timeout counts as a failure → try next model in failover chain
                continue
            except ProviderError as e:
                elapsed = time.monotonic() * 1000 - start_ms
                last_error = str(e)
                self._emit("PROVIDER_ERROR", {
                    "run_id": self.config.run_id,
                    "wave": seat.wave,
                    "seat_id": seat.seat_id,
                    "model": model,
                    "error": last_error,
                })
                continue
            except Exception as e:
                elapsed = time.monotonic() * 1000 - start_ms
                last_error = f"ORCHESTRATOR_ERROR: {e}"
                break

        # All attempts exhausted
        return AgentResult(
            seat_id=seat.seat_id,
            agent_isolation_id=seat.agent_isolation_id,
            model_actual=seat.model_actual,
            family_actual=seat.family_actual,
            wave=seat.wave,
            status=AgentStatus.FAILED,
            error=last_error,
            failover_count=seat_failover_count,
            failover_chain=failover_chain,
        )

    async def _invoke_agent(self, seat: SeatAssignment, bundle: Any, model: str) -> Dict:
        """
        Actual agent invocation. Delegates to self.agent_runner if set,
        otherwise raises NotImplementedError.
        """
        if self.agent_runner is None:
            raise NotImplementedError(
                "No agent_runner configured. Set AgentDispatcher.agent_runner "
                "to an async callable(seat, bundle, model) → Dict."
            )
        return await self.agent_runner(seat, bundle, model)

    # ------------------------------------------------------------------ #
    # Private: diverse seat assignment                                    #
    # ------------------------------------------------------------------ #

    def _assign_diverse_seats(
        self,
        wave: str,
        n_seats: int,
        available_models: List[str],
        role_prefix: str,
        excluded_families: Set[str],
    ) -> List[SeatAssignment]:
        """
        Select n_seats models ensuring each has a distinct family,
        respecting excluded_families.

        Algorithm:
          1. Filter out models from excluded families.
          2. Greedily pick models, one per family, until n_seats filled.
          3. If < n_seats distinct families available → DiversityViolationError.
        """
        eligible: List[Tuple[str, str]] = []  # (model, family)
        seen_families: Set[str] = set()

        for model in available_models:
            fam = self.registry.family_of(model)
            if fam in excluded_families:
                continue
            if fam in seen_families and fam != UNKNOWN_FAMILY:
                continue
            if fam != UNKNOWN_FAMILY:
                seen_families.add(fam)
            eligible.append((model, fam))

        if len(eligible) < n_seats:
            raise DiversityViolationError(
                f"FM-DIVERSITY: Cannot assign {n_seats} distinct-family seats for {wave}. "
                f"Only {len(eligible)} eligible model(s) after exclusions. "
                f"Excluded families: {sorted(excluded_families)}"
            )

        seats = []
        for i, (model, fam) in enumerate(eligible[:n_seats]):
            seat = SeatAssignment(
                seat_id=f"{wave}_{role_prefix}_{i+1}_{uuid.uuid4().hex[:8]}",
                wave=wave,
                role=f"{role_prefix}_{i+1}",
                model_requested=model,
                model_actual=model,
                family_actual=fam,
                agent_isolation_id=f"agent_{uuid.uuid4()}",
            )
            seats.append(seat)

        return seats

    # ------------------------------------------------------------------ #
    # Diversity verification post-dispatch                                #
    # ------------------------------------------------------------------ #

    def verify_wave_diversity(
        self,
        result: WaveDispatchResult,
        min_families: int,
    ) -> bool:
        """
        Post-dispatch MECH-001 check: verify successful agents have ≥ min_families.
        Returns True if check passes.
        Raises DiversityViolationError if check fails.
        """
        successful = result.successful_results
        families = {r.family_actual for r in successful}
        if len(families) < min_families:
            raise DiversityViolationError(
                f"FM-DIVERSITY: Wave {result.wave} post-dispatch: "
                f"only {len(families)} distinct families in successful agents "
                f"(need {min_families}). Families: {sorted(families)}"
            )
        return True


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class ProviderError(RuntimeError):
    """Raised by agent_runner when provider returns error or bad response (FM-PROVIDER)."""


class DispatchTimeoutError(RuntimeError):
    """Raised when wave-level timeout is exceeded (FM-TIMEOUT)."""


class WaveExhaustionError(RuntimeError):
    """FM-EXHAUSTION: All failover paths tried; insufficient successful agents."""
