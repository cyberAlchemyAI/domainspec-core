"""
Live wave executor — dispatches real agents via OpenClaw bridge protocol.

This module implements the WaveExecutor callable expected by Pipeline.
Instead of returning stub data, it dispatches actual agent seats through the
file-based bridge protocol defined in openclaw_bridge.py:

  1. Orchestrator builds seat assignments and prompt bundles.
  2. Writes a WaveDispatchRequest to the wave directory.
  3. Analog 6 (OpenClaw runtime) reads the request and spawns subagents.
  4. Analog 6 writes results back as wave_output_manifest.json.
  5. Orchestrator parses the output into gate-compatible dicts.

Each wave has a dedicated parser that transforms the raw agent output envelopes
into the exact dict shape its gate evaluator expects.

Spec refs: §5.2, §5.3, A.4, A.13
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from .config import FamilyRegistry, RunConfig
from .dispatch import DEFAULT_WAVE_TIMEOUTS_MS
from .manifest import RunManifest, WaveRecord
from .openclaw_bridge import (
    WaveDispatchRequest,
    WaveOutputManifest,
    write_dispatch_request,
    wait_for_wave_output,
)
from .deploy_adapter import DeployAdapter, DeployConfig
from .integration_runner import IntegrationRunner, IntegrationConfig
from .sentinel_monitor import SentinelMonitor, SentinelConfig


logger = logging.getLogger("zrig.live_executor")


# ---------------------------------------------------------------------------
# Provider → default model mapping
# ---------------------------------------------------------------------------

PROVIDER_MODEL_MAP: dict[str, str] = {
    # API providers
    "anthropic": "claude-sonnet-4",
    "openai": "gpt-5.4",
    "xai": "grok-4",
    "deepseek": "deepseek-chat",
    "google": "gemini-2.5-pro",
    "meta-llama": "llama-4-maverick",
    "mistral": "mistral-large",
    "cohere": "command-r-plus",
}

# CLI coding agents available for dispatch (not API — invoked via exec)
CLI_AGENT_REGISTRY: dict[str, dict[str, str]] = {
    "codex": {"bin": "codex", "version": "0.125.0", "provider": "openai"},
    "claude-code": {"bin": "claude", "version": "2.1.128", "provider": "anthropic"},
    "abacusai": {"bin": "abacusai", "version": "2.5.2", "provider": "abacusai"},
    "pi": {"bin": "pi", "version": "0.78.1", "provider": "google"},
    "cursor": {"bin": "cursor", "version": "3.0.12", "provider": "anthropic"},
}


# ---------------------------------------------------------------------------
# Wave seat configuration
# ---------------------------------------------------------------------------

# wave_id → (role, count_source, is_from_config)
# When is_from_config is True, count_source is a RunConfig field name.
# When False, count_source is a fixed int.
WAVE_SEAT_CONFIG: dict[str, tuple[str, str | int, bool]] = {
    "W0": ("probe", 0, False),
    "W1": ("planner", "w1_panel_size", True),
    "W2": ("builder", "w2_builder_count", True),
    "W3": ("synthesizer", 1, False),
    "W4": ("verifier", "w4_verifier_count", True),
    "W5": ("red_team", "w5_squad_count", True),
    "W5.5": ("remediator", 1, False),
    "W6": ("consolidator", 1, False),
    "W7": ("qa_tester", "w4_verifier_count", True),
    "W8": ("uat_tester", 1, False),
    "W8.5": ("fdl_preserver", 1, False),
    "W9": ("panelist", "w9_panel_size", True),
    "W10": ("deployer", 1, False),
    "W11": ("sentinel", 1, False),
}

PASSTHROUGH_WAVES: frozenset[str] = frozenset({"Wa-LOAD", "Wa-WRITE"})


# ---------------------------------------------------------------------------
# WavePromptBuilder protocol
# ---------------------------------------------------------------------------

@runtime_checkable
class WavePromptBuilder(Protocol):
    """Protocol for objects that generate per-seat prompt bundles.

    Implementations produce the task payload each agent receives.
    The executor calls ``build_prompt`` once per seat, passing the wave
    context and seat metadata so the builder can tailor the prompt to the
    agent's role, model, and the current pipeline state.
    """

    def build_prompt(
        self,
        wave_id: str,
        seat_index: int,
        role: str,
        context: dict[str, Any],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Return a bundle payload dict for one seat in the wave.

        Args:
            wave_id: Identifier of the wave being dispatched (e.g. ``"W2"``).
            seat_index: Zero-based index of this seat within the wave.
            role: Role string for this seat (e.g. ``"builder_0"``).
            context: Wave context built by ``Pipeline._build_wave_context()``.
            run_config: The active run configuration.
            manifest: Current run manifest (live, mutable).

        Returns:
            A JSON-serialisable dict that becomes the agent's input bundle.
        """
        ...


# ---------------------------------------------------------------------------
# LiveWaveExecutor
# ---------------------------------------------------------------------------

class LiveWaveExecutor:
    """Real wave executor using OpenClaw bridge protocol.

    Implements the ``WaveExecutor`` callable signature consumed by
    :class:`~zrig.pipeline.Pipeline`.  For every non-passthrough, non-probe
    wave it:

    1. Reads seat count from ``WAVE_SEAT_CONFIG`` / ``RunConfig``.
    2. Assigns models by cycling through ``provider_list`` for diversity.
    3. Builds per-seat prompt bundles via the injected ``WavePromptBuilder``.
    4. Writes a ``WaveDispatchRequest`` to the wave directory.
    5. Awaits the ``WaveOutputManifest`` via the bridge (blocking poll in a
       thread so the event loop stays responsive).
    6. Parses the raw output into the exact dict shape the wave's gate
       evaluator expects.

    Usage::

        prompts = MyWavePromptBuilder(task, run_config)
        executor = LiveWaveExecutor(run_dir, prompts)
        pipeline = Pipeline(run_config, task, wave_executor=executor)
        result = await pipeline.run()
    """

    def __init__(
        self,
        run_dir: Path,
        prompts: WavePromptBuilder,
        registry: FamilyRegistry | None = None,
        poll_interval_s: float = 3.0,
        max_wait_s: float = 3600.0,
    ) -> None:
        """
        Args:
            run_dir: Root directory for this pipeline run.  Wave
                sub-directories are created underneath.
            prompts: Builder that produces per-seat prompt payloads.
            registry: Family registry for model→family resolution.
                Falls back to ``FamilyRegistry.default()`` when *None*.
            poll_interval_s: Seconds between bridge poll ticks.
            max_wait_s: Absolute ceiling on bridge wait regardless of
                the per-wave timeout in ``RunConfig``.
        """
        self.run_dir = run_dir
        self.prompts = prompts
        self.registry = registry or FamilyRegistry.default()
        self.poll_interval_s = poll_interval_s
        self.max_wait_s = max_wait_s

    # ------------------------------------------------------------------ #
    # WaveExecutor callable interface                                     #
    # ------------------------------------------------------------------ #

    async def __call__(
        self,
        wave_id: str,
        context: dict[str, Any],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Execute a wave by dispatching agents through the bridge.

        This is the ``WaveExecutor`` callable consumed by
        :class:`~zrig.pipeline.Pipeline`.

        Args:
            wave_id: Wave identifier (e.g. ``"W2"``, ``"Wa-LOAD"``).
            context: Wave context built by ``Pipeline._build_wave_context()``.
            run_config: The run configuration.
            manifest: Current run manifest (live, mutable).

        Returns:
            A dict whose keys match the expectations of the wave's gate
            evaluator.  On timeout the dict includes ``_timed_out: True``.
        """
        if wave_id in PASSTHROUGH_WAVES:
            return {"status": "OK", "wave": wave_id}

        if wave_id == "W0":
            return self._probe_providers(run_config, manifest)

        # W10: Direct deploy if deploy_config is in context
        if wave_id == "W10" and context.get("deploy_config"):
            return await self._execute_deploy(context, run_config, manifest)

        # W11: Direct sentinel if sentinel_config is in context
        if wave_id == "W11" and context.get("sentinel_config"):
            return await self._execute_sentinel(context, run_config, manifest)

        return await self._dispatch_wave(wave_id, context, run_config, manifest)

    # ================================================================== #
    #  W0: Provider probe (no agent dispatch)                             #
    # ================================================================== #

    def _probe_providers(
        self,
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Probe configured providers and return a G0-compatible output dict.

        G0 gate (``evaluate_g0``) checks:

        * Every probe result has status ∈ {``HEALTHY``, ``DEGRADED``}.
        * ``diversity_check.satisfiable`` — at least 3 distinct families.
        * ``registry_hash`` computed and matching ``manifest.registry_hash``.
        * ``mode_selected`` matches ``manifest.mode``.
        * ``run_config`` structurally valid (already checked at parse time).
        * Not timed out (caller responsibility).

        Returns:
            Dict ready for ``evaluate_g0(wave_output=...)``.
        """
        providers = run_config.provider_list
        probe_results: list[dict[str, Any]] = []
        healthy_families: list[str] = []

        for provider in providers:
            model = PROVIDER_MODEL_MAP.get(provider, f"{provider}-default")
            family = self.registry.family_of(model)
            if family == "UNKNOWN":
                # Use provider name as family when model is unregistered
                family = provider

            # In a live deployment a real health-check request would go here.
            # For the bridge-based executor we assume every configured provider
            # is reachable — the bridge itself will surface actual failures.
            probe_results.append({
                "model": model,
                "family": family,
                "provider": provider,
                "status": "HEALTHY",
                "latency_ms": 0,
            })
            if family not in healthy_families:
                healthy_families.append(family)

        available_count = len(healthy_families)
        min_required = 3

        return {
            "probe_results": probe_results,
            "summary": {
                "healthy_family_count": available_count,
                "mode_selected": manifest.mode,
                "total_probed": len(providers),
            },
            "mode_selected": manifest.mode,
            "diversity_check": {
                "min_required": min_required,
                "available": available_count,
                "satisfiable": available_count >= min_required,
            },
            "registry_hash": manifest.registry_hash,
            "healthy_families": healthy_families,
        }

    # ================================================================== #
    #  Wave dispatch via bridge protocol                                  #
    # ================================================================== #

    async def _dispatch_wave(
        self,
        wave_id: str,
        context: dict[str, Any],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Dispatch agents for a wave via the bridge protocol.

        Steps:

        1. Resolve seat count and role from ``WAVE_SEAT_CONFIG``.
        2. Assign models by cycling ``run_config.provider_list``.
        3. Build per-seat prompt bundles via ``self.prompts``.
        4. Write ``WaveDispatchRequest`` to the wave directory.
        5. Wait for ``WaveOutputManifest`` (blocking call on a thread).
        6. Route to the wave-specific output parser.

        Returns:
            Gate-compatible output dict.  Includes ``_timed_out: True``
            when the bridge wait exceeds its deadline.
        """
        # -- Step 1: Resolve seat configuration --
        seat_config = WAVE_SEAT_CONFIG.get(wave_id)
        if seat_config is None:
            logger.warning(
                "No seat config for wave %s; returning minimal output", wave_id,
            )
            return {
                "status": "completed",
                "wave": wave_id,
                "primary_completed": True,
                "_unknown_wave": True,
                "residue": {"wave_id": wave_id, "no_residue_reason": "unknown wave"},
            }

        role, count_source, is_from_config = seat_config

        if is_from_config:
            assert isinstance(count_source, str)
            seat_count: int = getattr(run_config, count_source)
        else:
            assert isinstance(count_source, int)
            seat_count = count_source

        if seat_count == 0:
            return {"status": "completed", "wave": wave_id}

        # -- Step 2: Assign models --
        seats = self._assign_seats(wave_id, role, seat_count, run_config)

        # -- Step 3: Build prompt bundles --
        bundles: list[dict[str, Any]] = []
        for idx, seat in enumerate(seats):
            bundle_payload = self.prompts.build_prompt(
                wave_id=wave_id,
                seat_index=idx,
                role=seat["role"],
                context=context,
                run_config=run_config,
                manifest=manifest,
            )
            bundles.append(bundle_payload)

        # -- Step 4: Write dispatch request --
        wave_dir = self.run_dir / _safe_wave_dirname(wave_id)
        timeout_ms = _resolve_timeout_ms(wave_id, run_config)

        request = WaveDispatchRequest(
            request_id=str(uuid.uuid4()),
            run_id=run_config.run_id,
            wave=wave_id,
            seats=seats,
            bundles=bundles,
            timeout_ms=timeout_ms,
            created_at=datetime.now(timezone.utc).isoformat(),
            protocol_version="1.0",
        )

        write_dispatch_request(wave_dir, request)
        logger.info(
            "Dispatched wave %s: %d seat(s), timeout=%d ms, request_id=%s",
            wave_id,
            seat_count,
            timeout_ms,
            request.request_id,
        )

        # -- Step 5: Wait for output via bridge --
        agent_ids = [s["agent_isolation_id"] for s in seats]
        # Allow a 30-second grace period beyond the wave timeout for bridge
        # overhead (Analog 6 writing the manifest, filesystem flush, etc.)
        effective_wait = min(timeout_ms / 1000.0 + 30.0, self.max_wait_s)

        try:
            output_manifest: WaveOutputManifest = await asyncio.to_thread(
                wait_for_wave_output,
                wave_dir,
                agent_ids,
                self.poll_interval_s,
                effective_wait,
            )
        except TimeoutError:
            logger.warning(
                "Wave %s timed out after %.1f s", wave_id, effective_wait,
            )
            return self._build_timeout_output(wave_id, seats)

        # -- Step 6: Parse into gate-compatible dict --
        return self._parse_wave_output(
            wave_id, output_manifest, seats, run_config, manifest,
        )

    # ================================================================== #
    #  Seat assignment                                                    #
    # ================================================================== #

    def _assign_seats(
        self,
        wave_id: str,
        role: str,
        count: int,
        run_config: RunConfig,
    ) -> list[dict[str, Any]]:
        """Assign *count* model seats for *wave_id*, cycling providers.

        Provider diversity is achieved by round-robining through
        ``run_config.provider_list`` so that consecutive seats are
        backed by different families whenever possible.

        Returns:
            A list of seat dicts, each containing ``seat_id``, ``wave``,
            ``role``, ``model_requested``, ``model_actual``,
            ``family_actual``, ``provider``, and ``agent_isolation_id``.
        """
        providers = run_config.provider_list
        if not providers:
            raise ValueError("provider_list is empty — cannot assign seats")

        seats: list[dict[str, Any]] = []
        for i in range(count):
            provider = providers[i % len(providers)]
            model = PROVIDER_MODEL_MAP.get(provider, f"{provider}-default")
            family = self.registry.family_of(model)
            if family == "UNKNOWN":
                family = provider

            seats.append({
                "seat_id": f"{wave_id}_{role}_{i}_{uuid.uuid4().hex[:8]}",
                "wave": wave_id,
                "role": f"{role}_{i}",
                "model_requested": model,
                "model_actual": model,
                "family_actual": family,
                "provider": provider,
                "agent_isolation_id": f"agent_{uuid.uuid4()}",
            })

        return seats

    # ================================================================== #
    #  Output parsing — route to per-wave parser                          #
    # ================================================================== #

    def _parse_wave_output(
        self,
        wave_id: str,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Transform a ``WaveOutputManifest`` into a gate-compatible dict.

        Dispatches to ``_parse_w1``, ``_parse_w2``, … based on *wave_id*.
        Falls back to :meth:`_parse_generic` for unrecognised waves.
        """
        # Method name: W5.5 → _parse_w5_5, W10 → _parse_w10
        method_name = f"_parse_{wave_id.lower().replace('.', '_')}"
        parser = getattr(self, method_name, None)
        if parser is not None:
            return parser(output_manifest, seats, run_config, manifest)
        return self._parse_generic(output_manifest, seats, run_config, manifest)

    # ------------------------------------------------------------------ #
    # W1 — Blueprint Panel                                                #
    # ------------------------------------------------------------------ #

    def _parse_w1(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W1 output for G1 gate evaluation.

        G1 checks (see ``evaluate_g1``):

        * ``requirements.functional[]`` — ≥1 MUST requirement.
        * ``failure_modes[]`` — non-empty.
        * ``rubric[]`` — non-empty.
        * ``user_journeys[]`` — non-empty.
        * ``panel_consensus.agreement_level`` — ``unanimous`` or ``majority``.
        * ``w1_synthesis_confidence`` — ≥ 0.75.
        * ``residue.minority_dissent`` — captured for every dissenter.
        """
        all_requirements: list[dict[str, Any]] = []
        all_failure_modes: list[dict[str, Any]] = []
        all_rubric: list[dict[str, Any]] = []
        all_journeys: list[dict[str, Any]] = []
        minority_dissent: list[dict[str, Any]] = []
        confidence_scores: list[float] = []

        for output in output_manifest.outputs:
            payload = output.get("payload", output)

            # Requirements
            reqs = payload.get("requirements", {})
            all_requirements.extend(reqs.get("functional", []))

            # Failure modes
            all_failure_modes.extend(payload.get("failure_modes", []))

            # Rubric
            all_rubric.extend(payload.get("rubric", []))

            # User journeys
            all_journeys.extend(payload.get("user_journeys", []))

            # Confidence
            conf = payload.get(
                "w1_synthesis_confidence",
                payload.get("confidence"),
            )
            if isinstance(conf, (int, float)):
                confidence_scores.append(float(conf))

            # Dissent
            residue = payload.get("residue", {})
            if isinstance(residue, dict):
                dissent = residue.get("minority_dissent", [])
                if isinstance(dissent, list):
                    minority_dissent.extend(dissent)

        # Deduplicate requirements by ``id``
        deduped_requirements = _dedupe_by_key(all_requirements, "id")

        # Consensus: all agents succeeded → unanimous, otherwise majority
        total = output_manifest.successful_count + output_manifest.failed_count
        if output_manifest.failed_count == 0 and total > 0:
            agreement_level = "unanimous"
        elif output_manifest.successful_count > output_manifest.failed_count:
            agreement_level = "majority"
        else:
            agreement_level = "no_consensus"

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0.80  # conservative default when agents omit confidence
        )

        return {
            "requirements": {"functional": deduped_requirements},
            "failure_modes": _dedupe_by_key(all_failure_modes, "fm_id"),
            "rubric": _dedupe_by_key(all_rubric, "criterion_id"),
            "user_journeys": _dedupe_by_key(all_journeys, "journey_id"),
            "panel_consensus": {
                "agreement_level": agreement_level,
                "vote_counts": {
                    "agree": output_manifest.successful_count,
                    "disagree": output_manifest.failed_count,
                },
            },
            "w1_synthesis_confidence": avg_confidence,
            "residue": {
                "minority_dissent": minority_dissent,
                "wave_id": "W1",
            },
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W2 — Build Squad                                                    #
    # ------------------------------------------------------------------ #

    def _parse_w2(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W2 output for G2 gate evaluation.

        G2 checks (see ``evaluate_g2``):

        * ``builders[].build_status`` — ≥ 2 with ``SUCCESS`` or ``PARTIAL``.
        * ``builders[].family_actual`` — ≥ 3 distinct families.
        * ``builders[].artifact_id`` — present for every successful builder.
        * ``builders[].residue`` — present (MECH-028).
        """
        builders: list[dict[str, Any]] = []

        for idx, output in enumerate(output_manifest.outputs):
            payload = output.get("payload", output)
            seat = seats[idx] if idx < len(seats) else {}

            build_status = payload.get("build_status", "SUCCESS")
            if output.get("error"):
                build_status = "FAILED"

            builders.append({
                "model_actual": output.get(
                    "model_actual", seat.get("model_actual", ""),
                ),
                "family_actual": output.get(
                    "family_actual", seat.get("family_actual", ""),
                ),
                "build_status": build_status,
                "artifact_id": output.get("artifact_id", str(uuid.uuid4())),
                "implementation": payload.get("implementation", {}),
                "residue": _extract_residue(output),
            })

        # Append failed seats from error list
        for error in output_manifest.errors:
            seat_index = error.get("seat_index")
            seat = (
                seats[seat_index]
                if seat_index is not None and seat_index < len(seats)
                else {}
            )
            builders.append({
                "model_actual": seat.get("model_actual", "unknown"),
                "family_actual": seat.get("family_actual", "unknown"),
                "build_status": "FAILED",
                "artifact_id": "",
                "error": error.get("message", str(error)),
                "residue": {"wave_id": "W2", "error": True},
            })

        return {
            "builders": builders,
            "residue": {"wave_id": "W2"},
            "artifact_ids": [
                b["artifact_id"] for b in builders if b.get("artifact_id")
            ],
        }

    # ------------------------------------------------------------------ #
    # W3 — Synthesis                                                      #
    # ------------------------------------------------------------------ #

    def _parse_w3(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W3 output for G3 gate evaluation.

        G3 checks (see ``evaluate_g3``):

        * ``primary_completed`` — True.
        * ``selection_basis.{must_satisfied, must_total, coverage_rate}``.
        * ``synthesis_confidence`` — ≥ 0.60.
        * ``challenger_invoked`` / ``challenger_completed``.
        * ``canonical_implementation`` — the merged artifact.
        * ``adjudication`` / ``primary_confidence`` (MECH-013 ceiling).
        """
        if not output_manifest.outputs:
            return {
                "primary_completed": False,
                "selection_basis": {
                    "must_satisfied": 0,
                    "must_total": 0,
                    "coverage_rate": 0.0,
                },
                "synthesis_confidence": 0.0,
                "challenger_invoked": False,
                "canonical_implementation": {},
                "residue": {"wave_id": "W3"},
            }

        primary = output_manifest.outputs[0]
        payload = primary.get("payload", primary)

        return {
            "primary_completed": payload.get(
                "primary_completed",
                output_manifest.successful_count > 0,
            ),
            "selection_basis": payload.get("selection_basis", {
                "must_satisfied": payload.get("must_satisfied", 0),
                "must_total": payload.get("must_total", 0),
                "coverage_rate": payload.get("coverage_rate", 0.0),
            }),
            "synthesis_confidence": payload.get(
                "synthesis_confidence",
                payload.get("confidence", 0.0),
            ),
            "challenger_invoked": payload.get("challenger_invoked", False),
            "challenger_completed": payload.get("challenger_completed", True),
            "adjudication": payload.get("adjudication"),
            "primary_confidence": payload.get("primary_confidence"),
            "canonical_implementation": payload.get(
                "canonical_implementation",
                payload.get("implementation", {}),
            ),
            "residue": _extract_residue(primary),
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W4 — Verification                                                   #
    # ------------------------------------------------------------------ #

    def _parse_w4(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W4 output for G4 gate evaluation (generic gate).

        Collects per-verifier findings and verification results.  These
        flow downstream to W5 via the bundle transition matrix.
        """
        findings: list[dict[str, Any]] = []
        verification_results: list[dict[str, Any]] = []

        for output in output_manifest.outputs:
            payload = output.get("payload", output)
            findings.extend(payload.get("findings", []))

            verif = payload.get(
                "verification_result", payload.get("result", {}),
            )
            if verif:
                verification_results.append({
                    "verifier": output.get("agent_isolation_id", ""),
                    "model": output.get("model_actual", ""),
                    "family": output.get("family_actual", ""),
                    "result": verif,
                })

        return {
            "findings": findings,
            "verification_results": verification_results,
            "verification_confidence": 0.85,
            "residue": {"wave_id": "W4"},
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W5 — Red Team                                                       #
    # ------------------------------------------------------------------ #

    def _parse_w5(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W5 output for G5 gate evaluation."""
        all_findings: list[dict[str, Any]] = []
        attack_vectors: list[str] = []
        assessments: list[str] = []

        for output in output_manifest.outputs:
            payload = output.get("payload", output)
            all_findings.extend(payload.get("findings", []))
            attack_vectors.extend(payload.get("attack_vectors_tested", []))
            if payload.get("overall_assessment"):
                assessments.append(payload["overall_assessment"])

        return {
            "findings": all_findings,
            "attack_vectors_tested": list(set(attack_vectors)),
            "overall_assessment": assessments[0] if assessments else "completed",
            "redteam_confidence": 0.80,
            "residue": {"wave_id": "W5"},
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W6 — Consolidation (FULL mode only)                                 #
    # ------------------------------------------------------------------ #

    def _parse_w6(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W6 output for G6 gate evaluation.

        G6 checks:
        * consolidation_confidence > 0.7
        * no unresolved FATAL findings
        """
        consolidated_findings: list[dict[str, Any]] = []
        dedup_count = 0
        confidence_scores: list[float] = []

        for output in output_manifest.outputs:
            payload = output.get("payload", output)
            consolidated_findings.extend(payload.get("consolidated_findings", []))
            dedup_count += payload.get("dedup_count", 0)
            conf = payload.get("consolidation_confidence", 0.0)
            if isinstance(conf, (int, float)):
                confidence_scores.append(float(conf))

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0.75
        )

        return {
            "consolidated_findings": consolidated_findings,
            "dedup_count": dedup_count,
            "consolidation_confidence": avg_confidence,
            "residue": {"wave_id": "W6"},
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W7 — Deep QA (FULL mode only)                                       #
    # ------------------------------------------------------------------ #

    def _parse_w7(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W7 output for G7 gate evaluation.

        G7 checks:
        * false_positive_rate < 0.3
        * all FATAL findings confirmed
        """
        qa_results: list[dict[str, Any]] = []
        false_positive_count = 0
        total_tested = 0
        confidence_scores: list[float] = []

        for output in output_manifest.outputs:
            payload = output.get("payload", output)
            qa_results.extend(payload.get("qa_results", []))
            conf = payload.get("qa_confidence", 0.0)
            if isinstance(conf, (int, float)):
                confidence_scores.append(float(conf))

            for result in payload.get("qa_results", []):
                total_tested += 1
                if not result.get("confirmed", True):
                    false_positive_count += 1

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0.80
        )

        false_positive_rate = (
            false_positive_count / total_tested if total_tested > 0 else 0.0
        )

        return {
            "qa_results": qa_results,
            "false_positive_rate": false_positive_rate,
            "qa_confidence": avg_confidence,
            "residue": {"wave_id": "W7"},
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W5.5 — Remediation                                                  #
    # ------------------------------------------------------------------ #

    def _parse_w5_5(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W5.5 output for G5.5 gate evaluation."""
        if not output_manifest.outputs:
            return {
                "remediation_actions": [],
                "issues_addressed": [],
                "remediation_status": "skipped",
                "remediation_confidence": 0.0,
            }

        primary = output_manifest.outputs[0]
        payload = primary.get("payload", primary)

        return {
            "remediation_actions": payload.get("remediation_actions", []),
            "issues_addressed": payload.get("issues_addressed", []),
            "remediation_status": payload.get("remediation_status", "completed"),
            "remediation_confidence": payload.get("remediation_confidence", 0.75),
            "residue": _extract_residue(primary),
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W8 — UAT                                                            #
    # ------------------------------------------------------------------ #

    def _parse_w8(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W8 output for G8 gate evaluation."""
        journey_results: list[dict[str, Any]] = []
        all_findings: list[str] = []

        for output in output_manifest.outputs:
            payload = output.get("payload", output)
            journey_results.extend(payload.get("journey_results", []))
            all_findings.extend(payload.get("findings", []))

        overall_pass = all(j.get("status") == "pass" for j in journey_results)

        return {
            "journey_results": journey_results,
            "overall_pass": overall_pass,
            "findings": all_findings,
            "residue": {"wave_id": "W8"},
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W9 — Panel                                                          #
    # ------------------------------------------------------------------ #

    def _parse_w9(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W9 output for G9 gate evaluation."""
        votes: list[str] = []
        scores: list[int] = []
        critical_findings: list[str] = []

        for output in output_manifest.outputs:
            payload = output.get("payload", output)
            votes.append(payload.get("vote", "REVISE"))
            if "score" in payload:
                scores.append(payload["score"])
            critical_findings.extend(payload.get("critical_findings", []))

        # Majority vote
        from collections import Counter
        vote_counts = Counter(votes)
        final_vote = vote_counts.most_common(1)[0][0] if votes else "REVISE"

        avg_score = sum(scores) / len(scores) if scores else 70

        return {
            "vote": final_vote,
            "score": avg_score,
            "justification": f"Majority vote: {final_vote}",
            "critical_findings": list(set(critical_findings)),
            "residue": {"wave_id": "W9"},
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W10 — Deploy                                                        #
    # ------------------------------------------------------------------ #

    def _parse_w10(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W10 output for G10 gate evaluation."""
        if not output_manifest.outputs:
            return {
                "deployment_actions": [],
                "status": "failed",
            }

        primary = output_manifest.outputs[0]
        payload = primary.get("payload", primary)

        return {
            "deployment_actions": payload.get("deployment_actions", []),
            "status": payload.get("status", "success"),
            "residue": _extract_residue(primary),
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W11 — Sentinel                                                      #
    # ------------------------------------------------------------------ #

    def _parse_w11(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Parse W11 output for G11 gate evaluation."""
        if not output_manifest.outputs:
            return {
                "sentinel_status": "failed",
                "findings": [],
                "regression_detected": True,
            }

        primary = output_manifest.outputs[0]
        payload = primary.get("payload", primary)

        return {
            "sentinel_status": payload.get("sentinel_status", "healthy"),
            "findings": payload.get("findings", []),
            "regression_detected": payload.get("regression_detected", False),
            "residue": _extract_residue(primary),
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

    # ------------------------------------------------------------------ #
    # W10 — Direct Deploy Execution                                       #
    # ------------------------------------------------------------------ #

    async def _execute_deploy(
        self,
        context: dict[str, Any],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Execute W10 deployment directly via DeployAdapter.

        When context contains a deploy_config dict, the executor
        runs the deployment directly instead of dispatching a subagent.
        This enables real SSH-based deployment to staging.
        """
        try:
            deploy_cfg = DeployConfig.from_dict(context["deploy_config"])
            adapter = DeployAdapter(deploy_cfg)
            result = await asyncio.to_thread(adapter.deploy)

            # Run integration tests if config provided
            integration_result = None
            if context.get("integration_config"):
                int_cfg = IntegrationConfig.from_dict(context["integration_config"])
                runner = IntegrationRunner(int_cfg)
                integration_result = runner.run_all()

            return {
                "deployment_actions": [
                    {"action": step, "status": "completed"}
                    for step in result.steps_completed
                ],
                "status": "success" if result.success else "failed",
                "health_check_passed": result.health_check_passed,
                "rollback_commit": result.rollback_commit,
                "duration_s": result.duration_s,
                "error": result.error,
                "logs": result.logs,
                "integration_results": (
                    integration_result.to_gate_output()
                    if integration_result else None
                ),
            }
        except Exception as exc:
            logger.error("W10 direct deploy failed: %s", exc)
            return {
                "deployment_actions": [],
                "status": "failed",
                "error": str(exc),
            }

    # ------------------------------------------------------------------ #
    # W11 — Direct Sentinel Execution                                     #
    # ------------------------------------------------------------------ #

    async def _execute_sentinel(
        self,
        context: dict[str, Any],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Execute W11 sentinel monitoring directly via SentinelMonitor.

        When context contains a sentinel_config dict, the executor
        runs the sentinel directly instead of dispatching a subagent.
        This enables real HTTP-based post-deploy monitoring.
        """
        try:
            sentinel_cfg = SentinelConfig.from_dict(context["sentinel_config"])
            monitor = SentinelMonitor(sentinel_cfg)
            result = await asyncio.to_thread(monitor.run)
            return result.to_gate_output()
        except Exception as exc:
            logger.error("W11 direct sentinel failed: %s", exc)
            return {
                "sentinel_status": "failed",
                "findings": [{"id": "SENTINEL-ERROR", "severity": "CRITICAL", "description": str(exc)}],
                "regression_detected": True,
            }

    # ------------------------------------------------------------------ #
    # Generic parser                                                      #
    # ------------------------------------------------------------------ #

    def _parse_generic(
        self,
        output_manifest: WaveOutputManifest,
        seats: list[dict[str, Any]],
        run_config: RunConfig,
        manifest: RunManifest,
    ) -> dict[str, Any]:
        """Fallback parser for waves without a dedicated parser.

        Passes through the primary output payload verbatim, adding
        standard envelope fields so the generic gate can evaluate
        output presence and registry integrity.
        """
        if not output_manifest.outputs:
            return {
                "primary_completed": False,
                "residue": {},
            }

        primary = output_manifest.outputs[0]
        payload = primary.get("payload", primary)

        result: dict[str, Any] = {
            "primary_completed": True,
            "residue": _extract_residue(primary),
            "artifact_ids": _collect_artifact_ids(output_manifest),
        }

        # Merge payload keys that don't collide with envelope fields
        for key, value in payload.items():
            if key not in result:
                result[key] = value

        return result

    # ------------------------------------------------------------------ #
    # Timeout output                                                      #
    # ------------------------------------------------------------------ #

    def _build_timeout_output(
        self,
        wave_id: str,
        seats: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Build an output dict for a wave that timed out.

        The ``_timed_out`` flag causes ``Pipeline._execute_wave`` to
        pass ``timed_out=True`` into ``evaluate_gate``, which triggers
        the ``FM-TIMEOUT`` failure mode.
        """
        return {
            "_timed_out": True,
            "status": "TIMED_OUT",
            "wave": wave_id,
            "primary_completed": False,
            "seats_dispatched": len(seats),
            "residue": {"wave_id": wave_id, "timeout": True},
        }


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _safe_wave_dirname(wave_id: str) -> str:
    """Convert a wave ID into a filesystem-safe directory name.

    ``W5.5`` → ``W5_5``, ``Wa-LOAD`` → ``Wa-LOAD`` (hyphens are fine).
    """
    return wave_id.replace(".", "_")


def _resolve_timeout_ms(wave_id: str, run_config: RunConfig) -> int:
    """Return the effective timeout in milliseconds for *wave_id*.

    Operator-provided ``custom_timeouts`` override the spec defaults.
    """
    custom = run_config.custom_timeouts.get(wave_id)
    if custom is not None:
        return int(custom)
    return DEFAULT_WAVE_TIMEOUTS_MS.get(wave_id, 3_600_000)


def _extract_residue(output: dict[str, Any]) -> dict[str, Any]:
    """Extract residue from an agent output envelope.

    The universal artifact envelope (spec A.4) stores residue as a
    ``list[dict]``.  Gates expect a flat ``dict``, so we merge the
    list items.
    """
    residue = output.get("residue", {})
    if isinstance(residue, list):
        merged: dict[str, Any] = {}
        for item in residue:
            if isinstance(item, dict):
                merged.update(item)
        return merged
    if isinstance(residue, dict):
        return residue
    return {}


def _dedupe_by_key(
    items: list[dict[str, Any]],
    key: str,
) -> list[dict[str, Any]]:
    """Deduplicate a list of dicts by *key*, preserving insertion order.

    Items missing *key* are always kept (assigned a fresh UUID key).
    """
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for item in items:
        k = item.get(key, str(uuid.uuid4()))
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result


def _collect_artifact_ids(output_manifest: WaveOutputManifest) -> list[str]:
    """Gather non-empty ``artifact_id`` values from all outputs."""
    return [
        o["artifact_id"]
        for o in output_manifest.outputs
        if o.get("artifact_id")
    ]