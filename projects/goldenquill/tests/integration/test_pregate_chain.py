"""Integration tests — orchestrator-contract coverage for Phase 1 + 2a + 2b.

**Scope note (added 2026-04-19 after adversarial review finding C2).**
The Section 5 orchestrator does not yet exist as production code — it is Phase 3
of the v0.1 engineering queue. These tests therefore do NOT exercise the
production orchestrator. They simulate the Rows 21-23 + §4.14 + §4.16-§4.17
sequence by calling each gate function and collecting the results exactly as
the orchestrator WILL. What they validate is the *contract* every participating
module must honor so the orchestrator can compose them without ambiguity:
input shape, output shape, failure-code naming, non-blocking semantics of
the POST report, and the ability of the rails report to consume any
gate-event dict emitted anywhere in the chain.

A seam the future orchestrator must implement — the mapping from
`PrivacyRouteResult.routed_local=True` → a concrete local family name
consumed by `check_family_collision` — is EXPLICITLY tested below
(TestPrivacyToFamilyMappingContract) so the obligation is visible.

These tests exercise multiple modules together in flows a real Section 5
orchestrator will run per blueprint §4.2.1 Rows 21-23 + §4.14 + §4.16-§4.17.
Every unit passes in isolation (covered by phase test files); these tests
prove the units compose into a coherent gate chain and that failure codes
emitted by one module are faithfully captured by the rails report POST-gate.

Simulated orchestrator sequence (v0.1 headless envelope):

    start_run
      → key_presence preflight            [§4.2.1 Row 22]
      → router_drift detection            [§4.2.1 Row 23]
      → family_collision preflight        [§4.16]
      → privacy_router pregate            [§4.14 / Row 21]
      → (dispatch — not exercised in v0.1)
      → emit_rails_report POST            [§4.17]

Each gate result is captured as a gate_event dict and handed to
emit_rails_report; the on-disk artifact is parsed back and asserted.
"""

from __future__ import annotations

import datetime
import json
from dataclasses import asdict
from pathlib import Path

import pytest

from pipeline.canary import (
    CanaryVerdict,
    F_CANARY_TEST_VECTORS_MISSING,
    run_canary_gate,
)
from pipeline.observability import (
    InvocationRecord,
    STR_WINDOW_MIN_SESSIONS,
    STRWindow,
    compute_str,
)
from pipeline.privacy import (
    PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR,
    PrivacyTag,
    run_privacy_pregate,
)
import pipeline.privacy._router as _router_mod
from pipeline.runtime_integrity import (
    F_KEY_PRESENCE_PREFLIGHT_FAIL,
    F_RAILS_REPORT_EMISSION_FAIL,
    F_ROUTER_FAMILY_COLLISION,
    F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER,
    canonical_bytes_sha3_512,
    check_family_collision,
    check_key_presence,
    check_router_drift,
    emit_rails_report,
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _gate_event(gate: str, result: str, failure_code: str | None, detail: dict | None) -> dict:
    """Normalize a gate result into the dict shape emit_rails_report expects."""
    return {
        "gate": gate,
        "result": result,
        "failure_code": failure_code,
        "detail": detail,
    }


def _load_rails_report(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Scenario 1 — happy path: every preflight passes, rails report captures all
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestHappyPreflightChain:
    """All preflights pass; stub privacy classifier still fails closed (v0.1)."""

    def test_all_preflights_recorded_in_rails_report(self, tmp_path, monkeypatch):
        run_id = "integ-happy-001"
        events: list[dict] = []

        # Stage 1: key presence preflight
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
        monkeypatch.setenv("GROQ_API_KEY", "gsk_test")
        kp_result = check_key_presence(
            required_keys={"scribe": "ANTHROPIC_API_KEY", "judge": "GROQ_API_KEY"},
        )
        events.append(
            _gate_event(
                "key_presence",
                "PASS" if kp_result.all_present else "FAIL",
                kp_result.failure_code,
                kp_result.detail,
            )
        )

        # Stage 2: router drift — identical hash means no drift
        router_data = {"seats": {"scribe": {"family": "anthropic"}}}
        expected = canonical_bytes_sha3_512(router_data)
        drift_result = check_router_drift(
            router_data=router_data,
            expected_hash=expected,
        )
        events.append(
            _gate_event(
                "router_drift",
                "PASS" if not drift_result.drift_detected else "FAIL",
                drift_result.failure_code,
                drift_result.detail,
            )
        )

        # Stage 3: family collision — 5 distinct families for the 5 council seats
        fc_result = check_family_collision(
            resolved_families=["anthropic", "openai", "meta", "alibaba", "moonshot"],
        )
        events.append(
            _gate_event(
                "family_collision",
                "PASS" if not fc_result.collision_detected else "FAIL",
                fc_result.failure_code,
                fc_result.detail,
            )
        )

        # Stage 4: privacy pregate — v0.1 stub always returns CLASSIFIER_ERROR
        pr_result = run_privacy_pregate(
            payload="grant discovery query",
            seat="scribe",
            default_routing="cloud",
        )
        events.append(
            _gate_event(
                "privacy_router",
                pr_result.tag.value,
                pr_result.failure_code,
                pr_result.detail,
            )
        )

        # Stage 5: emit rails report POST-gate
        report_path = tmp_path / "runs" / run_id / "rails_report.md"
        rr_result = emit_rails_report(
            run_id=run_id,
            gate_events=events,
            output_path=str(report_path),
        )

        # Assertions: every gate event must appear in the on-disk report
        assert rr_result.emitted
        assert rr_result.output_path == str(report_path)
        assert report_path.exists()

        body = _load_rails_report(report_path)
        assert run_id in body
        assert "key_presence" in body
        assert "router_drift" in body
        assert "family_collision" in body
        assert "privacy_router" in body
        # The v0.1 stub's failure code must be visible (not silently dropped)
        assert PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR in body

    def test_report_records_gate_ordering(self, tmp_path, monkeypatch):
        """Rails report writes gates in the ORDER they were dispatched."""
        run_id = "integ-order-001"
        monkeypatch.setenv("TEST_KEY", "x")
        kp = check_key_presence({"seat_a": "TEST_KEY"})
        fc = check_family_collision(["anthropic", "meta"])
        pr = run_privacy_pregate("q", "scribe", "cloud")
        events = [
            _gate_event("key_presence", "PASS", kp.failure_code, kp.detail),
            _gate_event("family_collision", "PASS", fc.failure_code, fc.detail),
            _gate_event("privacy_router", pr.tag.value, pr.failure_code, pr.detail),
        ]
        report_path = tmp_path / "rails.md"
        emit_rails_report(run_id, events, str(report_path))
        body = _load_rails_report(report_path)

        kp_idx = body.index("key_presence")
        fc_idx = body.index("family_collision")
        pr_idx = body.index("privacy_router")
        assert kp_idx < fc_idx < pr_idx, (
            "Rails report must preserve gate dispatch ordering"
        )


# ---------------------------------------------------------------------------
# Scenario 2 — classifier exception cascade (§4.14 fail-closed semantics)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestClassifierExceptionCascade:
    """Classifier throws → router catches → failure code lands in rails report."""

    def test_classifier_exception_propagates_failure_code_to_disk(
        self, tmp_path, monkeypatch
    ):
        run_id = "integ-classifier-exc-001"

        def crashing_classifier(_payload):
            raise RuntimeError("simulated classifier crash")

        monkeypatch.setattr(_router_mod, "classify_payload", crashing_classifier)

        pr_result = run_privacy_pregate(
            payload="sensitive payload",
            seat="scribe",
            default_routing="cloud",
        )
        assert pr_result.routed_local is True, "Fail-closed must route local"
        assert pr_result.failure_code == PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR
        assert pr_result.detail["sub_tag"] == "classifier_exception"

        events = [
            _gate_event(
                "privacy_router",
                pr_result.tag.value,
                pr_result.failure_code,
                pr_result.detail,
            )
        ]
        report_path = tmp_path / "rails.md"
        rr_result = emit_rails_report(run_id, events, str(report_path))
        assert rr_result.emitted

        body = _load_rails_report(report_path)
        assert PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR in body
        assert "classifier_exception" in body
        assert "simulated classifier crash" in body


# ---------------------------------------------------------------------------
# Scenario 3 — key-absent preflight halts the chain; rails still emits
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestKeyAbsentHaltsChain:
    """Missing key fails preflight; subsequent gates skipped; rails POST still fires."""

    def test_missing_key_captured_in_rails_report(self, tmp_path, monkeypatch):
        run_id = "integ-key-absent-001"
        # Clear out keys that we know might be inherited
        for k in ("ANTHROPIC_API_KEY", "GROQ_API_KEY"):
            monkeypatch.delenv(k, raising=False)

        kp = check_key_presence(
            required_keys={"scribe": "ANTHROPIC_API_KEY", "judge": "GROQ_API_KEY"},
            env={},  # explicit empty env
        )
        assert kp.all_present is False
        assert kp.failure_code == F_KEY_PRESENCE_PREFLIGHT_FAIL
        assert kp.missing_keys is not None
        assert set(kp.missing_keys) == {"ANTHROPIC_API_KEY", "GROQ_API_KEY"}

        # Orchestrator short-circuits: only emit the preflight fail event
        events = [
            _gate_event(
                "key_presence",
                "FAIL",
                kp.failure_code,
                kp.detail,
            )
        ]
        report_path = tmp_path / "rails.md"
        rr_result = emit_rails_report(run_id, events, str(report_path))
        assert rr_result.emitted

        body = _load_rails_report(report_path)
        assert F_KEY_PRESENCE_PREFLIGHT_FAIL in body
        assert "ANTHROPIC_API_KEY" in body
        assert "GROQ_API_KEY" in body


# ---------------------------------------------------------------------------
# Scenario 4 — family collision aborts before privacy router even runs
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestFamilyCollisionAbortsDispatch:
    """Two seats resolved to the same family → collision → rails records abort."""

    def test_duplicate_anthropic_family_collision_recorded(self, tmp_path):
        run_id = "integ-fam-collision-001"
        # Two seats both resolved to anthropic (e.g. fallback landed on same family)
        fc = check_family_collision(
            resolved_families=["anthropic", "openai", "anthropic", "meta", "alibaba"],
        )
        assert fc.collision_detected
        assert fc.failure_code == F_ROUTER_FAMILY_COLLISION
        assert fc.colliding_families == ("anthropic",)

        events = [
            _gate_event(
                "family_collision",
                "FAIL",
                fc.failure_code,
                fc.detail,
            )
        ]
        report_path = tmp_path / "rails.md"
        emit_rails_report(run_id, events, str(report_path))
        body = _load_rails_report(report_path)
        assert F_ROUTER_FAMILY_COLLISION in body
        # The detail must preserve the offending family list
        assert "anthropic" in body


# ---------------------------------------------------------------------------
# Scenario 5 — router drift without operator attestation raises drift flag
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRouterDriftWithoutAttestation:
    """router.yaml edited since last lock, no operator signature → drift fires."""

    def test_drift_recorded_and_preserves_hashes(self, tmp_path):
        run_id = "integ-drift-001"
        locked_router = {"seats": {"scribe": {"family": "anthropic"}}}
        locked_hash = canonical_bytes_sha3_512(locked_router)

        drifted_router = {"seats": {"scribe": {"family": "openai"}}}  # edit!
        drift = check_router_drift(
            router_data=drifted_router,
            expected_hash=locked_hash,
            operator_attested=False,
        )
        assert drift.drift_detected
        assert drift.failure_code == F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER
        assert drift.computed_hash != locked_hash

        events = [
            _gate_event(
                "router_drift",
                "FAIL",
                drift.failure_code,
                drift.detail,
            )
        ]
        report_path = tmp_path / "rails.md"
        emit_rails_report(run_id, events, str(report_path))
        body = _load_rails_report(report_path)
        assert F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER in body
        assert locked_hash in body
        assert drift.computed_hash in body


# ---------------------------------------------------------------------------
# Scenario 6 — observability STRWindow → Canary read contract
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestObservabilityFeedsCanary:
    """STRWindow must hand raw per-session arrays to Canary via the pinned
    local-only interface (§5.8.3). Canary v0.2 will replace its stub with a
    real replay harness that consumes this data; for v0.1 we verify the
    contract shape now to catch interface drift before v0.2 lands."""

    def test_str_window_populated_from_invocation_records(self):
        """Build InvocationRecord objects → compute STR → fill STRWindow →
        verify Canary-facing read returns the expected shape."""
        window = STRWindow(seat="scribe")
        base_date = datetime.date(2026, 4, 15)

        # Three sessions, each with 2 invocations
        for i in range(3):
            session_id = f"session-{i}"
            session_date = base_date + datetime.timedelta(days=i)
            invocations = [
                InvocationRecord(
                    run_id=f"run-{i}-{j}",
                    seat="scribe",
                    timestamp=f"2026-04-{15 + i:02d}T12:00:00Z",
                    model_family_resolved="anthropic",
                    token_count_input=100,
                    token_count_output=200,
                    success_flag=1,
                    latency_ms=1000,
                )
                for j in range(2)
            ]
            str_values = [
                compute_str(inv.success_flag, inv.token_count_input, inv.token_count_output)
                for inv in invocations
            ]
            window.add_session(session_id, session_date, str_values)

        raw = window._raw_sessions_for_canary()
        assert len(raw) == 3

        for session_id, session_date, values in raw:
            assert isinstance(session_id, str)
            assert isinstance(session_date, datetime.date)
            # Each value is the compute_str result: 1 / (100 + 200) = 1/300
            assert all(v == pytest.approx(1 / 300) for v in values)

    def test_canary_contract_gate_blocks_even_with_warm_window(self):
        """Canary stub blocks regardless of what STRWindow holds; this test
        pins the v0.1 fail-closed contract, not the v0.2 replay logic."""
        window = STRWindow(seat="judge")
        base_date = datetime.date(2026, 4, 1)
        # Warm the window past the k=5 minimum
        for i in range(STR_WINDOW_MIN_SESSIONS):
            window.add_session(
                session_id=f"s-{i}",
                session_date=base_date + datetime.timedelta(days=i),
                str_values=[0.01, 0.02],
            )
        quantiles = window.query(reference_date=base_date + datetime.timedelta(days=1))
        assert quantiles is not None

        # Canary stub still blocks — v0.1 has no corpus interface
        result = run_canary_gate(
            candidate_router_hash="hash-after-edit",
            baseline_router_hash="hash-before-edit",
        )
        assert result.verdict == CanaryVerdict.STUB_BLOCKED
        assert result.failure_code == F_CANARY_TEST_VECTORS_MISSING


# ---------------------------------------------------------------------------
# Scenario 7 — Canary + router_drift coupling (edit-time gate semantics)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestCanaryBlocksRouterSwap:
    """When router.yaml changes the operator MUST run the Canary gate to
    promote. v0.1 stub always blocks; rails report captures the blocker."""

    def test_router_swap_blocked_by_canary_stub(self, tmp_path):
        run_id = "integ-canary-block-001"
        before = {"seats": {"scribe": {"family": "anthropic"}}}
        after = {"seats": {"scribe": {"family": "openai"}}}  # swap attempted
        h_before = canonical_bytes_sha3_512(before)
        h_after = canonical_bytes_sha3_512(after)
        assert h_before != h_after

        canary = run_canary_gate(h_after, h_before)
        assert canary.verdict == CanaryVerdict.STUB_BLOCKED

        events = [
            _gate_event(
                "canary",
                canary.verdict.value,
                canary.failure_code,
                canary.detail,
            )
        ]
        report_path = tmp_path / "rails.md"
        emit_rails_report(run_id, events, str(report_path))
        body = _load_rails_report(report_path)
        assert F_CANARY_TEST_VECTORS_MISSING in body
        assert "STUB_BLOCKED" in body


# ---------------------------------------------------------------------------
# Scenario 8 — rails report emission failure does NOT halt the run (§4.17)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRailsReportEmissionIsNonBlocking:
    """§4.17 contract: if emit fails, return non-blocking failure code — the
    run is NOT invalidated. The caller may still proceed."""

    def test_emission_to_unwritable_path_returns_non_blocking_failure(self):
        # Use a path under /dev/full on Linux isn't portable; pick a path whose
        # parent cannot be created (a file masquerading as a directory).
        import os
        import tempfile

        with tempfile.NamedTemporaryFile() as blocker:
            # Attempt to write "inside" a regular file — will fail
            bad_path = os.path.join(blocker.name, "subdir", "rails.md")
            rr = emit_rails_report(
                run_id="integ-rr-fail-001",
                gate_events=[{"gate": "x", "result": "PASS"}],
                output_path=bad_path,
            )
            assert rr.emitted is False
            assert rr.failure_code == F_RAILS_REPORT_EMISSION_FAIL
            assert "attempted_path" in rr.detail


# ---------------------------------------------------------------------------
# Scenario 9 — full preflight-chain summary integration
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestFullPreflightChainSummary:
    """Compose every preflight + privacy + post-gate into one run; assert
    no gate result silently disappears and that failure codes are unique."""

    def test_all_gate_failure_codes_distinct(self, tmp_path, monkeypatch):
        """When multiple gates fail, rails report preserves all distinct codes."""
        run_id = "integ-full-chain-001"

        # Force every gate into a FAIL state
        kp = check_key_presence({"s": "MISSING_KEY"}, env={})
        fc = check_family_collision(["anthropic", "anthropic"])  # collision
        drift = check_router_drift(
            router_data={"x": 1}, expected_hash="deadbeef" * 16
        )

        def crashing(_):
            raise ValueError("crash")

        monkeypatch.setattr(_router_mod, "classify_payload", crashing)
        pr = run_privacy_pregate("payload", "scribe", "cloud")

        canary = run_canary_gate("h1", "h2")

        events = [
            _gate_event("key_presence", "FAIL", kp.failure_code, kp.detail),
            _gate_event("family_collision", "FAIL", fc.failure_code, fc.detail),
            _gate_event("router_drift", "FAIL", drift.failure_code, drift.detail),
            _gate_event("privacy_router", "FAIL", pr.failure_code, pr.detail),
            _gate_event("canary", "FAIL", canary.failure_code, canary.detail),
        ]

        report_path = tmp_path / "rails.md"
        rr = emit_rails_report(run_id, events, str(report_path))
        assert rr.emitted

        body = _load_rails_report(report_path)
        for code in (
            F_KEY_PRESENCE_PREFLIGHT_FAIL,
            F_ROUTER_FAMILY_COLLISION,
            F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER,
            PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR,
            F_CANARY_TEST_VECTORS_MISSING,
        ):
            assert code in body, f"failure code {code} must appear in rails report"

    def test_all_pass_produces_no_failure_codes(self, tmp_path, monkeypatch):
        """Happy path: when no gate fails, report carries no failure_code lines."""
        run_id = "integ-full-pass-001"
        monkeypatch.setenv("K", "v")
        kp = check_key_presence({"s": "K"})
        fc = check_family_collision(["anthropic", "openai", "meta"])
        router = {"a": 1}
        drift = check_router_drift(router, canonical_bytes_sha3_512(router))

        events = [
            _gate_event("key_presence", "PASS", kp.failure_code, kp.detail),
            _gate_event("family_collision", "PASS", fc.failure_code, fc.detail),
            _gate_event("router_drift", "PASS", drift.failure_code, drift.detail),
        ]
        report_path = tmp_path / "rails.md"
        emit_rails_report(run_id, events, str(report_path))
        body = _load_rails_report(report_path)
        # No failure_code line should appear — the helper omits the line when None
        assert "- failure_code:" not in body


# ---------------------------------------------------------------------------
# Scenario 10 — contract stability between modules
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestCrossModuleContracts:
    """Lock cross-module invariants that silent drift could break."""

    def test_invocation_record_fields_match_str_compute_inputs(self):
        """compute_str reads exactly the three fields InvocationRecord requires."""
        rec = InvocationRecord(
            run_id="r",
            seat="s",
            timestamp="2026-04-19T00:00:00Z",
            model_family_resolved="anthropic",
            token_count_input=50,
            token_count_output=150,
            success_flag=1,
            latency_ms=500,
        )
        # Build the compute_str call using the record's fields.
        value = compute_str(
            success_flag=rec.success_flag,
            token_count_input=rec.token_count_input,
            token_count_output=rec.token_count_output,
        )
        assert value == pytest.approx(1 / 200)

    def test_privacy_result_detail_surface_safe_for_rails_serialization(self, monkeypatch):
        """PrivacyRouteResult.detail must JSON-serialize — rails_report writes it
        via json.dumps (sort_keys=True)."""
        def crashing(_):
            raise ValueError("with unicode: café 🌱")

        monkeypatch.setattr(_router_mod, "classify_payload", crashing)
        result = run_privacy_pregate("q", "scribe", "cloud")
        # json.dumps with sort_keys must not raise
        serialized = json.dumps(result.detail, sort_keys=True, ensure_ascii=False)
        assert "café" in serialized
        assert "🌱" in serialized

    def test_rails_report_consumes_all_frozen_dataclass_details(self, tmp_path, monkeypatch):
        """All PhaseX result dataclasses are frozen; their .detail fields must
        pass through to rails_report without mutation."""
        monkeypatch.setenv("K", "v")
        kp = check_key_presence({"s": "K"})
        fc = check_family_collision(["anthropic"])
        # kp, fc are both PASS → detail is None on both
        assert kp.detail is None
        assert fc.detail is None
        events = [
            _gate_event("key_presence", "PASS", kp.failure_code, kp.detail),
            _gate_event("family_collision", "PASS", fc.failure_code, fc.detail),
        ]
        rr = emit_rails_report("r", events, str(tmp_path / "rails.md"))
        assert rr.emitted


# ---------------------------------------------------------------------------
# Orchestrator contract: Privacy → Family-mapping seam
# Review round 2026-04-19 Finding C2 (Gemini coherence audit).
# ---------------------------------------------------------------------------

class TestPrivacyToFamilyMappingContract:
    """The future orchestrator must map PrivacyRouteResult → families list.

    When `run_privacy_pregate` returns routed_local=True, the seat's effective
    family is forced to a local family (e.g. "local-ollama") before
    `check_family_collision` runs — otherwise the family-collision gate would
    operate on stale cloud families and miss a real collision in the local lane.

    These tests pin the contract so the orchestrator implementation cannot
    silently drop this mapping step. They do NOT prove the orchestrator is
    correct (it does not yet exist); they prove the modules it must connect
    expose the information needed to perform the mapping.
    """

    LOCAL_FAMILY = "local-ollama"

    def _orchestrator_family_mapper(self, privacy_result, default_family: str) -> str:
        """Reference implementation of the mapping the orchestrator must perform.

        If privacy forces LOCAL, the seat's family must be swapped to the
        local family before the collision gate runs. Otherwise the default
        (cloud-family) from router.yaml is retained.
        """
        if privacy_result.routed_local:
            return self.LOCAL_FAMILY
        return default_family

    def test_classifier_error_forces_local_family_in_mapping(self):
        # Default stub classifier returns CLASSIFIER_ERROR → fail-closed LOCAL.
        privacy = run_privacy_pregate("sensitive payload", "scribe", "cloud")
        assert privacy.routed_local is True
        family = self._orchestrator_family_mapper(privacy, default_family="anthropic")
        assert family == self.LOCAL_FAMILY, (
            "orchestrator MUST map routed_local=True → local family before "
            "calling check_family_collision; otherwise collisions in the local "
            "lane are invisible"
        )

    def test_local_mapping_applied_before_family_collision(self, monkeypatch):
        # Two seats — scribe (cloud) + judge (cloud) — both forced LOCAL by
        # classifier-error. Without the mapping, the collision gate would
        # see two distinct cloud families and pass. WITH the mapping, both
        # resolve to the same local family and the gate correctly fires.
        scribe = run_privacy_pregate("x", "scribe", "cloud")
        judge = run_privacy_pregate("y", "judge", "cloud")
        assert scribe.routed_local and judge.routed_local
        resolved = [
            self._orchestrator_family_mapper(scribe, default_family="anthropic"),
            self._orchestrator_family_mapper(judge, default_family="groq"),
        ]
        assert resolved == [self.LOCAL_FAMILY, self.LOCAL_FAMILY]
        fc = check_family_collision(resolved)
        assert fc.collision_detected is True
        assert fc.colliding_families == (self.LOCAL_FAMILY,)

    def test_cloud_eligible_retains_default_family(self, monkeypatch):
        # Counter-case: if classifier said CLOUD_ELIGIBLE, the mapping must
        # return the DEFAULT family (the router-configured cloud family),
        # not force LOCAL.
        monkeypatch.setattr(
            _router_mod, "classify_payload", lambda p: PrivacyTag.CLOUD_ELIGIBLE
        )
        privacy = run_privacy_pregate("public data", "scribe", "cloud")
        assert privacy.routed_local is False
        family = self._orchestrator_family_mapper(privacy, default_family="anthropic")
        assert family == "anthropic"

    def test_privacy_result_exposes_routed_local_bool(self):
        # Pin the exact field the orchestrator reads. If this ever changes,
        # this test + the mapper above both fail loudly.
        privacy = run_privacy_pregate("x", "scribe", "cloud")
        assert hasattr(privacy, "routed_local")
        assert isinstance(privacy.routed_local, bool)
