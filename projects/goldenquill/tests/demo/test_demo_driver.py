"""tests.demo.test_demo_driver — Demo Driver MVP end-to-end harness.

Spec card: ``pipeline/engineering/spec_cards/demo_driver_mvp_end_to_end.md``.

Capstone-of-capstones — exercises :func:`pipeline.loop.run_pipeline.run_pipeline`
end-to-end with realistic input bytes (USDA VAPG FY26 RFA snapshot, FIT
Farms LLC PROJECT_CONTEXT snapshot, LOCKed VAPG rubric) and deterministic
LLM-faked seats. The Demo Driver is the **proof that Tilth v0.1 composes
the full council pipeline from a standing start**, not a per-seat unit
test (those LOCKed at §3 / §7 / §8 / §9 whole-section capstones).

This file is **test infrastructure only** — zero new production code per
spec card §7. The harness composes LOCKed §5 R11 ``run_pipeline`` over
LOCKed conftest_section_5 fakes (``InMemoryVault`` / ``Clock`` / ``Launcher``
/ gate fakes). All fakes are E-017 Protocol seams; every fake collaborator
has independent LOCK on record.

Test categories (per spec card §6 mapping):

- **M.1 Happy path** (≥1) — full 11-stage pipeline with all-PASS gates +
  default seat outputs. Asserts terminal-shape success, council-firing
  trail, and JSONSchema conformance.
- **M.2 Degraded mode** (≥5) — Scribe timeout + cascade advance, Editor
  timeout + cascade advance, Judge unparseable → F_PIPE_09 trips revision
  loop, Judge persistent unparseable → F_PIPE_05 cap, PRE-gate soft-fail,
  POST-gate FAIL → bypass-pending, PRE-gate raises RuntimeError →
  state-failure wrapper.
- **M.3 Law enforcement** (≥5) — Law 1 / Law 2 / Law 3 / Law 4 / Law 5
  trips routed through PRE-gate or POST-gate fake; sovereignty no-network
  invariant via AST scan.
- **M.4 Performance gate** (≥1) — checkpoint count budget +
  subprocess-launch count budget + wall-clock ms non-negative under
  deterministic fake clock.
- **M.5 Output schema** (≥1) — :class:`PipelineRunResult` shape validates
  against ``expected/pipeline_output_schema.json`` for all three terminal
  shapes (success / pre-gate-fail / bypass-pending).
- **M.6 Capstone manifest** — fixture-files presence, RFA + PROJECT_CONTEXT
  + rubric content invariants, run_pipeline + PipelineRunResult public
  surface, BLUEPRINT_DEPS pin.

Reference modules used at the seam:

- :mod:`pipeline.loop.run_pipeline` — §5 R11 capstone (LOCKED 2026-04-21).
- :mod:`tests.loop.conftest_section_5` — submission harness builder
  (LOCKED via §5 R13 capstone 2026-04-29).
- :mod:`pipeline.rubrics.vapg_fy26` (live JSON) — VAPG FY26 rubric.
- :mod:`pipeline.loop.errors` — F_PIPE_05 / 06 / 08 / 09 / 21 / 22.
- :mod:`pipeline.logician.pre_gate` — PreGateInput / PreGateResult.

Sovereignty posture: every collaborator is an injected seam (in-memory
vault / fake launcher / fake gates). Demo Driver makes zero network calls;
the §6.3 sovereignty test pins this via AST scan.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
from dataclasses import asdict, fields, is_dataclass
from pathlib import Path
from typing import Any, Final

import pytest

from pipeline.loop.errors import (
    F_PIPE_05,
    F_PIPE_09,
    PipelineFailure,
)
from pipeline.loop.run_pipeline import (
    BLUEPRINT_DEPS,
    PipelineRunResult,
    PreGateInputFactory,
    RunPipelineContext,
    run_pipeline,
)
from pipeline.loop.seat_runner import SubprocessResult

from tests.loop.conftest_section_5 import (
    Launcher,
    SubmissionHarness,
    build_submission_harness,
    make_cascade,
    make_charter,
    post_gate_fail,
    post_gate_pass,
    pre_gate_fail,
    pre_gate_pass,
)


# ---------------------------------------------------------------------------
# Pinned demo-run constants
# ---------------------------------------------------------------------------


DEMO_ORG_SLUG: Final[str] = "fit_farms"
DEMO_SESSION_ID: Final[str] = "demo-mvp-session"
DEMO_RUN_ID_PREFIX: Final[str] = "demo-mvp"

# Per spec card §4: VAPG FY26 rubric carries 7 scoring criteria.
EXPECTED_RUBRIC_CRITERIA_COUNT: Final[int] = 7
EXPECTED_RUBRIC_MIN_SCORE: Final[int] = 50
EXPECTED_RUBRIC_MAX_SCORE: Final[int] = 100
EXPECTED_RUBRIC_FUNDER: Final[str] = "USDA Rural Development"
EXPECTED_RUBRIC_PROGRAM_PREFIX: Final[str] = "Value-Added Producer Grant"

# Per spec card §6.4: 8 GB M1 Mac Mini happy-path budget under deterministic
# fakes — happy path executes ≤30 vault writes (start + per-iter + post-gate
# + signoff + tab + final = ≤9 nominal; 30 budget allows headroom for a
# failed POST-gate / revision-loop overhead).
HAPPY_PATH_WRITE_BUDGET: Final[int] = 30

# Happy path: scribe + editor + judge each fire once on first cascade level
# of iter 1. Budget allows ≤9 launcher calls (3 seats × 3 iters max).
HAPPY_PATH_LAUNCH_BUDGET: Final[int] = 9


# ---------------------------------------------------------------------------
# Module-load integrity assertions (R7 inline-literal rebind-resistance)
# ---------------------------------------------------------------------------


assert (
    EXPECTED_RUBRIC_CRITERIA_COUNT == 7
), "demo driver: expected_rubric_criteria_count rebound; refusing to load"
assert (
    HAPPY_PATH_WRITE_BUDGET == 30
), "demo driver: happy_path_write_budget rebound; refusing to load"
assert (
    HAPPY_PATH_LAUNCH_BUDGET == 9
), "demo driver: happy_path_launch_budget rebound; refusing to load"


# ---------------------------------------------------------------------------
# Helpers — one-line wrappers over :func:`run_pipeline`
# ---------------------------------------------------------------------------


def _run_demo_pipeline(
    h: SubmissionHarness,
    *,
    run_id: str = "demo-mvp-happy",
    org_slug: str = DEMO_ORG_SLUG,
    rfa_hash: str = "rfa-demo-abc",
    project_context_hash: str = "pc-demo-def",
) -> PipelineRunResult:
    """Standard ``run_pipeline`` invocation for demo tests."""

    return run_pipeline(
        run_id=run_id,
        org_slug=org_slug,
        session_id=DEMO_SESSION_ID,
        rfa_hash=rfa_hash,
        project_context_hash=project_context_hash,
        scribe_charter=make_charter("scribe"),
        editor_charter=make_charter("editor"),
        judge_charter=make_charter("judge"),
        scribe_cascade=make_cascade("scribe"),
        editor_cascade=make_cascade("editor"),
        judge_cascade=make_cascade("judge"),
        context=h.context,
        pre_gate_input_factory=h.pre_gate_input_factory,
    )


def _result_as_jsonable(result: PipelineRunResult) -> dict[str, Any]:
    """Encode :class:`PipelineRunResult` for schema validation.

    :class:`PipelineRunResult` is a frozen+slotted dataclass; ``asdict``
    produces a JSONable dict with all nine fields (the eight Round 11
    fields plus the dataclass shape itself).
    """

    return asdict(result)


def _validate_against_demo_schema(
    instance: dict[str, Any], schema: dict[str, object]
) -> None:
    """Stdlib-only JSONSchema-subset validator for PipelineRunResult.

    Validates the subset of draft-07 features used by
    ``expected/pipeline_output_schema.json``: required, type, enum,
    pattern, minimum, maximum, oneOf (with const + type at the leaf).

    The Demo Driver does not pull in ``jsonschema`` as a dependency
    (provisioning manifest scope). The schema document is documentation;
    this validator enforces the contract.
    """

    required = schema.get("required") or []
    assert isinstance(required, list)
    for key in required:
        assert key in instance, f"missing required field: {key}"

    properties = schema.get("properties") or {}
    assert isinstance(properties, dict)
    for key, value in instance.items():
        prop_schema = properties.get(key)
        if prop_schema is None:
            continue
        _validate_property_value(key, value, prop_schema)

    one_of = schema.get("oneOf")
    if isinstance(one_of, list):
        matches = 0
        last_failure: AssertionError | None = None
        for branch in one_of:
            assert isinstance(branch, dict)
            try:
                _validate_branch(instance, branch)
                matches += 1
            except AssertionError as exc:
                last_failure = exc
        assert matches == 1, (
            f"expected exactly 1 oneOf branch to match; got {matches}; "
            f"last_failure={last_failure}"
        )


def _validate_property_value(
    key: str, value: object, prop_schema: object
) -> None:
    assert isinstance(prop_schema, dict)
    type_decl = prop_schema.get("type")
    if isinstance(type_decl, str):
        type_decl = [type_decl]
    if isinstance(type_decl, list):
        ok = False
        for t in type_decl:
            if t == "string" and isinstance(value, str):
                ok = True
                break
            if t == "integer" and isinstance(value, int) and not isinstance(
                value, bool
            ):
                ok = True
                break
            if t == "boolean" and isinstance(value, bool):
                ok = True
                break
            if t == "null" and value is None:
                ok = True
                break
            if t == "object" and isinstance(value, dict):
                ok = True
                break
            if t == "array" and isinstance(value, list):
                ok = True
                break
        assert ok, f"{key}: type {type_decl} mismatch (got {type(value).__name__})"
    pattern = prop_schema.get("pattern")
    if isinstance(pattern, str) and isinstance(value, str):
        assert re.fullmatch(pattern, value), f"{key}: pattern {pattern!r} mismatch"
    enum = prop_schema.get("enum")
    if isinstance(enum, list):
        assert value in enum, f"{key}: not in enum {enum}"
    minimum = prop_schema.get("minimum")
    if isinstance(minimum, int) and isinstance(value, int):
        assert value >= minimum, f"{key}: {value} < minimum {minimum}"
    maximum = prop_schema.get("maximum")
    if isinstance(maximum, int) and isinstance(value, int):
        assert value <= maximum, f"{key}: {value} > maximum {maximum}"


def _validate_branch(
    instance: dict[str, Any], branch: dict[str, object]
) -> None:
    """Validate one of the schema's oneOf branches.

    Each branch carries a ``properties`` block whose entries set
    ``const`` (literal value) or ``type`` (string). The branch matches
    when every constraint holds.
    """

    properties = branch.get("properties") or {}
    assert isinstance(properties, dict)
    for key, prop in properties.items():
        assert isinstance(prop, dict)
        if "const" in prop:
            assert (
                instance.get(key) == prop["const"]
            ), f"branch property {key}: expected const {prop['const']!r}, got {instance.get(key)!r}"
        if "type" in prop:
            type_decl = prop["type"]
            if type_decl == "string":
                assert isinstance(
                    instance.get(key), str
                ), f"branch property {key}: not a string"
    required = branch.get("required") or []
    assert isinstance(required, list)
    for key in required:
        assert key in instance, f"branch missing required field {key}"


# ===========================================================================
# M.1 — Happy Path (1 long-running test, deterministic-fakes equivalent
# of spec card §6.1 real-API run)
# ===========================================================================


class TestM1HappyPath:
    """Full 11-stage pipeline produces a scored PipelineRunResult with
    audit trail. Deterministic-fake equivalent of spec card §6.1 — the
    real-API run is operator-time and uses the same harness with live
    seat subprocesses + live API keys.
    """

    def test_demo_full_pipeline_terminal_shape(
        self,
        demo_submission_harness: SubmissionHarness,
        demo_rfa_hash: str,
        demo_project_context_hash: str,
    ) -> None:
        h = demo_submission_harness
        result = _run_demo_pipeline(
            h,
            rfa_hash=demo_rfa_hash,
            project_context_hash=demo_project_context_hash,
        )

        # Terminal-shape — success path.
        assert result.final_phase == "tabs_delivered"
        assert result.bypass_pending is False
        assert result.pre_gate_failed is False
        assert result.pre_gate_failure_code is None
        assert result.post_gate_rejected_trigger is None

        # Iteration count — happy path passes on first iteration.
        assert result.iterations_consumed == 1

        # Envelope hash — Round 9 SHA-256 hex (64 lowercase hex chars).
        assert result.three_tab_envelope_hash is not None
        assert re.fullmatch(r"^[0-9a-f]{64}$", result.three_tab_envelope_hash)

        # Wall-clock — non-negative integer ms (deterministic-fake clock
        # advances monotonically).
        assert isinstance(result.elapsed_ms, int)
        assert result.elapsed_ms >= 0

        # run_id — caller-minted idempotency key threads through
        # fixed-factory closure into Round 3.
        assert result.run_id == "demo-mvp-happy"

    def test_demo_council_seats_fired_in_sequence(
        self,
        demo_submission_harness: SubmissionHarness,
        demo_rfa_hash: str,
        demo_project_context_hash: str,
    ) -> None:
        """All five council seats engage on a happy run: PRE-gate → Scribe
        → Editor → Judge → POST-gate. (Scout is upstream; the §5 pipeline
        consumes Scout's RFA-hash output, not Scout's process.)
        """

        h = demo_submission_harness
        _run_demo_pipeline(
            h,
            rfa_hash=demo_rfa_hash,
            project_context_hash=demo_project_context_hash,
        )

        # PRE-gate fired exactly once.
        assert len(h.pre_gate_callable.calls) == 1
        # POST-gate fired exactly once.
        assert len(h.post_gate_runner.calls) == 1
        # Scribe + Editor + Judge each fired exactly once on first cascade
        # level — order verified by inspecting launcher.calls.
        seat_order = [c["seat_kind"] for c in h.launcher.calls]
        assert seat_order == ["scribe", "editor", "judge"]
        # Three tab files hashed (Round 9 deliver_tab contract).
        assert len(h.hash_file.calls) == 3

    def test_demo_audit_trail_in_vault(
        self,
        demo_submission_harness: SubmissionHarness,
        demo_rfa_hash: str,
        demo_project_context_hash: str,
    ) -> None:
        """The vault carries a complete checkpoint trail: state.json
        mints + per-phase transitions + tab envelope. Total writes
        non-zero and bounded.
        """

        h = demo_submission_harness
        _run_demo_pipeline(
            h,
            rfa_hash=demo_rfa_hash,
            project_context_hash=demo_project_context_hash,
        )

        # state.json was written and exists in the in-memory vault store.
        state_paths = [
            p for p in h.vault.store.keys() if p.endswith("/state.json")
        ]
        assert len(state_paths) == 1, (
            f"expected one state.json; got {state_paths}"
        )
        # state.json's last-known phase is the terminal phase.
        state_bytes = h.vault.store[state_paths[0]]
        state = json.loads(state_bytes.decode("utf-8"))
        assert state.get("phase") == "tabs_delivered"

        # Vault writes within budget (M.4 perf gate is independent; this
        # asserts non-emptiness + non-divergence).
        assert 1 <= len(h.vault.writes) <= HAPPY_PATH_WRITE_BUDGET


# ===========================================================================
# M.2 — Degraded Mode (≥5 tests; mock seat failures + gate soft-fails)
# ===========================================================================


class TestM2DegradedMode:
    """Realistic failure-mode injection — proves the pipeline fails-closed
    on each documented degraded path. Mocked at the seat-subprocess +
    gate-callable seams; no real LLM / no real vault.
    """

    def test_scribe_first_level_timeout_advances_cascade(
        self,
    ) -> None:
        """Scribe seat times out on cascade level 0 → seat_runner advances
        to level 1 → succeeds. Iteration count stays at 1.
        """

        h = build_submission_harness(run_id="demo-mvp-d1")
        # Scribe call 1 = timeout; subsequent calls fall through to
        # default success (driving cascade advance within the same iter).
        h.launcher.per_seat["scribe"] = [
            SubprocessResult(
                exit_code=0,
                stdout=b"",
                stderr=b"",
                timed_out=True,
                landed_family="anthropic",
                landed_model_id="claude-opus",
            ),
        ]
        result = _run_demo_pipeline(h, run_id="demo-mvp-d1")

        # Pipeline still succeeds, but scribe was called twice.
        assert result.final_phase == "tabs_delivered"
        scribe_calls = [c for c in h.launcher.calls if c["seat_kind"] == "scribe"]
        assert len(scribe_calls) == 2
        # Second call landed on the next cascade family.
        assert scribe_calls[1]["family"] != scribe_calls[0]["family"]

    def test_editor_first_level_timeout_advances_cascade(
        self,
    ) -> None:
        """Editor seat times out on cascade level 0 → seat_runner advances."""

        h = build_submission_harness(run_id="demo-mvp-d2")
        h.launcher.per_seat["editor"] = [
            SubprocessResult(
                exit_code=0,
                stdout=b"",
                stderr=b"",
                timed_out=True,
                landed_family="google",
                landed_model_id="gemini",
            ),
        ]
        result = _run_demo_pipeline(h, run_id="demo-mvp-d2")
        assert result.final_phase == "tabs_delivered"
        editor_calls = [c for c in h.launcher.calls if c["seat_kind"] == "editor"]
        assert len(editor_calls) == 2

    def test_judge_revise_then_pass_runs_two_iterations(
        self,
    ) -> None:
        """Judge returns ``verdict=REVISE`` on iter 1 → revision loop
        advances to iter 2 → default PASS verdict converges →
        ``iterations_consumed == 2``.

        Per blueprint §4.6 + Round 5 docstring: revision loop continues
        when Judge produces a *valid but non-PASS* verdict; an
        unparseable Judge output is fatal at the parser layer (F_PIPE_09)
        and never reaches the convergence check.
        """

        h = build_submission_harness(run_id="demo-mvp-d3")
        h.launcher.per_seat["judge"] = [
            SubprocessResult(
                exit_code=0,
                stdout=(
                    b'{"verdict": "REVISE", "total_score": 60, '
                    b'"per_dimension": {"rigor": 6, "clarity": 5}}'
                ),
                stderr=b"",
                timed_out=False,
                landed_family="openai",
                landed_model_id="gpt",
            ),
        ]
        result = _run_demo_pipeline(h, run_id="demo-mvp-d3")
        assert result.final_phase == "tabs_delivered"
        assert result.iterations_consumed == 2

    def test_judge_unparseable_raises_F_PIPE_09(
        self,
    ) -> None:
        """Judge stdout doesn't parse as JSON → :class:`F_PIPE_09`
        propagates from Round 4 through Round 5's record-and-re-raise to
        Round 11. Pipeline does NOT auto-retry parser failures (the
        revision loop only handles valid-but-non-PASS verdicts).
        """

        h = build_submission_harness(run_id="demo-mvp-d4")
        h.launcher.per_seat["judge"] = [
            SubprocessResult(
                exit_code=0,
                stdout=b"not valid json at all",
                stderr=b"",
                timed_out=False,
                landed_family="openai",
                landed_model_id="gpt",
            ),
        ]
        with pytest.raises(F_PIPE_09):
            _run_demo_pipeline(h, run_id="demo-mvp-d4")

    def test_three_revise_iterations_trips_F_PIPE_05_iteration_cap(
        self,
    ) -> None:
        """Judge returns REVISE with low score (no plateau) for all three
        iterations → cap exhausted → :class:`F_PIPE_05`.

        Score=60 < 75 floor disables the delta-plateau early-exit, so the
        loop runs the full 1..3 iteration range before raising.
        """

        h = build_submission_harness(run_id="demo-mvp-d4b")
        revise = SubprocessResult(
            exit_code=0,
            stdout=(
                b'{"verdict": "REVISE", "total_score": 60, '
                b'"per_dimension": {"rigor": 6, "clarity": 5}}'
            ),
            stderr=b"",
            timed_out=False,
            landed_family="openai",
            landed_model_id="gpt",
        )
        h.launcher.per_seat["judge"] = [revise, revise, revise]
        with pytest.raises(F_PIPE_05):
            _run_demo_pipeline(h, run_id="demo-mvp-d4b")

    def test_pre_gate_soft_fail_returns_early(
        self,
    ) -> None:
        """PRE-gate returns ``passed=False`` → soft-fail return with
        ``pre_gate_failed=True`` and the failure code threaded through.
        No seat invocation, no POST-gate fire.
        """

        h = build_submission_harness(
            run_id="demo-mvp-d5",
            pre_gate_result=pre_gate_fail("F-PRE-05-MISSING-KEYS"),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-d5")

        assert result.final_phase == "pre_gate_pending"
        assert result.pre_gate_failed is True
        assert result.pre_gate_failure_code == "F-PRE-05-MISSING-KEYS"
        assert result.iterations_consumed == 0
        assert result.three_tab_envelope_hash is None
        assert len(h.launcher.calls) == 0
        assert len(h.post_gate_runner.calls) == 0

    def test_post_gate_fail_routes_to_bypass_pending(
        self,
    ) -> None:
        """POST-gate returns ``passed=False`` → :class:`PostGateRejected`
        caught → bypass-pending sidecar written + ``bypass_pending=True``
        on result. Operator's out-of-band sign-off workflow is the next
        step.
        """

        h = build_submission_harness(
            run_id="demo-mvp-d6",
            post_gate_result=post_gate_fail("F-POST-12-RFA-SCOPE-DRIFT"),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-d6")

        assert result.final_phase == "post_gate_pending"
        assert result.bypass_pending is True
        assert result.three_tab_envelope_hash is None
        # Trigger threaded from PostGateRejected.trigger.
        assert result.post_gate_rejected_trigger is not None

        # Bypass-pending sidecar marker landed in the vault.
        bypass_paths = [
            p for p in h.vault.store.keys() if p.endswith("/bypass_pending.json")
        ]
        assert len(bypass_paths) == 1

    def test_pre_gate_callable_raises_state_failure_wrapper(
        self,
    ) -> None:
        """Rogue PRE-gate callable raising RuntimeError → state-failure
        wrapper lands + exception propagates unchanged (trusted-operator
        contract; non-PipelineFailure exceptions are NOT translated).
        """

        h = build_submission_harness(run_id="demo-mvp-d7")
        h.pre_gate_callable.raise_exc = RuntimeError("rogue PRE-gate")

        with pytest.raises(RuntimeError, match="rogue PRE-gate"):
            _run_demo_pipeline(h, run_id="demo-mvp-d7")


# ===========================================================================
# M.3 — Law Enforcement (≥5 tests; trip each of the Five Laws via gate
# fakes plus sovereignty no-network invariant)
# ===========================================================================


class TestM3LawEnforcement:
    """Each of the Five Operating Laws is enforceable through Logician
    PRE-gate (Laws 3, 4) or POST-gate (Laws 1, 2, 5). Demo Driver pins
    the wiring: when a gate fake returns the Law-violation failure code,
    :func:`run_pipeline` produces the expected terminal shape.
    """

    def test_law_1_rfa_truth_violation_routes_bypass_pending(
        self,
    ) -> None:
        """Law 1 — every claim traces to the RFA or PROJECT_CONTEXT.
        POST-gate detects fabricated content → bypass-pending.
        """

        h = build_submission_harness(
            run_id="demo-mvp-l1",
            post_gate_result=post_gate_fail("F-POST-LAW-1-RFA-TRUTH-VIOLATION"),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-l1")
        assert result.bypass_pending is True
        assert result.final_phase == "post_gate_pending"
        # Failure code threaded through PostGateRejected.trigger.
        assert result.post_gate_rejected_trigger is not None

    def test_law_2_boundary_drift_routes_bypass_pending(
        self,
    ) -> None:
        """Law 2 — stay inside RFA scope. POST-gate detects scope drift.
        """

        h = build_submission_harness(
            run_id="demo-mvp-l2",
            post_gate_result=post_gate_fail("F-POST-LAW-2-BOUNDARY-DRIFT"),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-l2")
        assert result.bypass_pending is True
        assert result.final_phase == "post_gate_pending"

    def test_law_3_org_isolation_routes_pre_gate_soft_fail(
        self,
    ) -> None:
        """Law 3 — never cross-reference data between orgs. PRE-gate
        Cedar evaluation catches cross-org reads.
        """

        h = build_submission_harness(
            run_id="demo-mvp-l3",
            pre_gate_result=pre_gate_fail("F-PRE-03-ORG-ISOLATION"),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-l3")
        assert result.pre_gate_failed is True
        assert result.pre_gate_failure_code == "F-PRE-03-ORG-ISOLATION"
        assert result.final_phase == "pre_gate_pending"

    def test_law_4_admin_risk_ledger_break_routes_pre_gate_soft_fail(
        self,
    ) -> None:
        """Law 4 — admin-risk register live + monotonic. PRE-gate check #10
        validates the admin-risk ledger; chain break trips a soft-fail
        (the F-PRE-10 sub-codes are documented in
        :mod:`pipeline.logician.pre_gate`).
        """

        h = build_submission_harness(
            run_id="demo-mvp-l4",
            pre_gate_result=pre_gate_fail("F-PRE-10.admin_risk_chain_break"),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-l4")
        assert result.pre_gate_failed is True
        assert result.pre_gate_failure_code == "F-PRE-10.admin_risk_chain_break"

    def test_law_5_evidence_not_in_draft_routes_bypass_pending(
        self,
    ) -> None:
        """Law 5 — applicant brings substance; Judge evidence quotes must
        appear verbatim in the draft. POST-gate evidence-in-draft check
        fails → bypass-pending.
        """

        h = build_submission_harness(
            run_id="demo-mvp-l5",
            post_gate_result=post_gate_fail(
                "F-POST-LAW-5-EVIDENCE-NOT-IN-DRAFT"
            ),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-l5")
        assert result.bypass_pending is True

    def test_sovereignty_no_network_imports_in_run_pipeline(
        self,
    ) -> None:
        """Sovereignty Promise — :mod:`pipeline.loop.run_pipeline` does NOT
        import any network or socket library. Vault is the only side-effect
        boundary, and the vault is itself an injected Protocol.

        This is a defence-in-depth pin against a future refactor that
        would inadvertently introduce a phone-home path. Failure here is
        an architecture regression, not a behavioural bug.

        Note: ``pipeline.loop.__init__`` re-exports the ``run_pipeline``
        callable, which shadows the submodule attribute on the package.
        Resolution via ``sys.modules`` reaches the actual submodule.
        """

        import sys

        run_pipeline_module = sys.modules["pipeline.loop.run_pipeline"]
        assert run_pipeline_module.__file__ is not None
        source = Path(run_pipeline_module.__file__).read_text("utf-8")
        tree = ast.parse(source)
        forbidden = {
            "urllib",
            "urllib.request",
            "urllib3",
            "requests",
            "httpx",
            "aiohttp",
            "socket",
            "ssl",
            "smtplib",
            "ftplib",
            "telnetlib",
        }
        observed_imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    observed_imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    observed_imports.add(node.module)
        leaks = observed_imports & forbidden
        assert not leaks, (
            f"sovereignty regression — pipeline.loop.run_pipeline imports "
            f"network module(s): {sorted(leaks)}"
        )


# ===========================================================================
# M.4 — Performance Gate (≥1 test; deterministic-fake equivalent of the
# spec card §6.4 wall-clock test on 8 GB M1)
# ===========================================================================


class TestM4PerformanceGate:
    """Under deterministic fakes the wall-clock is the fake clock's
    reported delta; the meaningful budgets are vault-write count and
    subprocess-launch count. Both pin the orchestration cost, which is
    what scales with hardware (32 GB → 128 GB doesn't change the
    checkpoint cadence; LLM call latency does).
    """

    def test_happy_path_vault_writes_within_budget(
        self,
        demo_submission_harness: SubmissionHarness,
        demo_rfa_hash: str,
        demo_project_context_hash: str,
    ) -> None:
        h = demo_submission_harness
        _run_demo_pipeline(
            h,
            rfa_hash=demo_rfa_hash,
            project_context_hash=demo_project_context_hash,
        )
        assert (
            len(h.vault.writes) <= HAPPY_PATH_WRITE_BUDGET
        ), f"vault writes {len(h.vault.writes)} > budget {HAPPY_PATH_WRITE_BUDGET}"

    def test_happy_path_subprocess_launches_within_budget(
        self,
        demo_submission_harness: SubmissionHarness,
        demo_rfa_hash: str,
        demo_project_context_hash: str,
    ) -> None:
        h = demo_submission_harness
        _run_demo_pipeline(
            h,
            rfa_hash=demo_rfa_hash,
            project_context_hash=demo_project_context_hash,
        )
        assert (
            len(h.launcher.calls) <= HAPPY_PATH_LAUNCH_BUDGET
        ), f"launches {len(h.launcher.calls)} > budget {HAPPY_PATH_LAUNCH_BUDGET}"

    def test_happy_path_elapsed_ms_non_negative(
        self,
        demo_submission_harness: SubmissionHarness,
        demo_rfa_hash: str,
        demo_project_context_hash: str,
    ) -> None:
        """Wall-clock invariant — :func:`run_pipeline` clamps elapsed_ms
        to ``max(now_ms() - start_wall_ms, 0)``; a deterministic fake
        clock that advances monotonically yields a positive integer.
        """

        h = demo_submission_harness
        result = _run_demo_pipeline(
            h,
            rfa_hash=demo_rfa_hash,
            project_context_hash=demo_project_context_hash,
        )
        assert isinstance(result.elapsed_ms, int)
        assert result.elapsed_ms >= 0


# ===========================================================================
# M.5 — Output Schema (≥1 test; JSONSchema validation across all three
# terminal shapes)
# ===========================================================================


class TestM5OutputSchema:
    """Each of the three :class:`PipelineRunResult` terminal shapes
    validates against the demo's pipeline_output_schema.json. JSONSchema
    is the documented contract surface — schema drift is caught here.
    """

    def test_happy_path_result_validates(
        self,
        demo_submission_harness: SubmissionHarness,
        demo_pipeline_output_schema: dict[str, object],
    ) -> None:
        h = demo_submission_harness
        result = _run_demo_pipeline(h)
        _validate_against_demo_schema(
            _result_as_jsonable(result), demo_pipeline_output_schema
        )

    def test_pre_gate_fail_result_validates(
        self,
        demo_pipeline_output_schema: dict[str, object],
    ) -> None:
        h = build_submission_harness(
            run_id="demo-mvp-schema-pre",
            pre_gate_result=pre_gate_fail("F-PRE-99-DEMO-STUB"),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-schema-pre")
        _validate_against_demo_schema(
            _result_as_jsonable(result), demo_pipeline_output_schema
        )

    def test_bypass_pending_result_validates(
        self,
        demo_pipeline_output_schema: dict[str, object],
    ) -> None:
        h = build_submission_harness(
            run_id="demo-mvp-schema-bypass",
            post_gate_result=post_gate_fail("F-POST-99-DEMO-STUB"),
        )
        result = _run_demo_pipeline(h, run_id="demo-mvp-schema-bypass")
        _validate_against_demo_schema(
            _result_as_jsonable(result), demo_pipeline_output_schema
        )


# ===========================================================================
# M.6 — Capstone Manifest (pin-the-surface tests)
# ===========================================================================


class TestM6CapstoneManifest:
    """Pin the demo fixture surface + pipeline public-API shape. Catches
    drift in: fixture-file presence, RFA + PROJECT_CONTEXT + rubric
    invariants, run_pipeline + PipelineRunResult exposure, BLUEPRINT_DEPS.
    """

    def test_demo_rfa_snapshot_present_and_well_formed(
        self,
        demo_rfa_path: Path,
        demo_rfa_bytes: bytes,
    ) -> None:
        assert demo_rfa_path.exists()
        rfa = json.loads(demo_rfa_bytes.decode("utf-8"))
        assert rfa["schema_version"] == "demo-rfa-envelope.v1"
        assert rfa["meta"]["funder"] == EXPECTED_RUBRIC_FUNDER
        assert rfa["meta"]["program"].startswith(EXPECTED_RUBRIC_PROGRAM_PREFIX)
        assert rfa["meta"]["fiscal_year"] == 2026
        assert (
            rfa["meta"]["rubric_path"] == "pipeline/rubrics/vapg_fy26.json"
        )
        # Five sections are required (per VAPG application structure).
        assert len(rfa["rfa_sections_required"]) == 5

    def test_demo_project_context_snapshot_present_and_pinned_to_fit_farms(
        self,
        demo_project_context_path: Path,
        demo_project_context_bytes: bytes,
    ) -> None:
        assert demo_project_context_path.exists()
        text = demo_project_context_bytes.decode("utf-8")
        # Front-matter pin — the fixture is for FIT Farms LLC (client
        # role), not FIT Farms Commons (operator role). Law 3 strictly
        # separates the two file-name labels even when they point at the
        # same legal entity.
        assert "org: FIT Farms" in text
        assert "canonical_entity_name: FIT Farms LLC" in text
        assert "role_label: client" in text
        assert "demo_fixture: true" in text
        # Demo fixture uses synthetic EIN 12-3456789 (real EIN is operator-confidential).
        assert "12-3456789" in text

    def test_demo_pipeline_output_schema_present(
        self,
        demo_pipeline_output_schema: dict[str, object],
    ) -> None:
        # Schema is a draft-07 JSONSchema document.
        assert (
            demo_pipeline_output_schema.get("$schema")
            == "http://json-schema.org/draft-07/schema#"
        )
        # Three terminal-shape branches under oneOf.
        one_of = demo_pipeline_output_schema.get("oneOf")
        assert isinstance(one_of, list) and len(one_of) == 3
        # Every PipelineRunResult dataclass field is named in 'required'.
        result_field_names = {f.name for f in fields(PipelineRunResult)}
        required = set(demo_pipeline_output_schema["required"])  # type: ignore[arg-type]
        assert required == result_field_names

    def test_vapg_rubric_pinned_invariants(
        self,
        demo_rubric: dict[str, object],
    ) -> None:
        meta = demo_rubric["meta"]
        assert isinstance(meta, dict)
        assert meta["funder"] == EXPECTED_RUBRIC_FUNDER
        assert meta["program"].startswith(EXPECTED_RUBRIC_PROGRAM_PREFIX)
        assert meta["min_score"] == EXPECTED_RUBRIC_MIN_SCORE
        assert meta["max_score"] == EXPECTED_RUBRIC_MAX_SCORE
        criteria = demo_rubric["scoring_criteria"]
        assert isinstance(criteria, list)
        assert len(criteria) == EXPECTED_RUBRIC_CRITERIA_COUNT

    def test_run_pipeline_public_surface_exposed(
        self,
    ) -> None:
        """:mod:`pipeline.loop.run_pipeline` exposes the four names the
        demo driver consumes: run_pipeline, PipelineRunResult,
        RunPipelineContext, PreGateInputFactory + BLUEPRINT_DEPS.

        Reaches the submodule via ``sys.modules`` because
        ``pipeline.loop.__init__`` re-exports ``run_pipeline`` as a
        callable, which shadows the submodule attribute on the package.
        """

        import sys

        rp = sys.modules["pipeline.loop.run_pipeline"]
        public = set(rp.__all__)
        assert {
            "BLUEPRINT_DEPS",
            "PipelineRunResult",
            "PreGateInputFactory",
            "RunPipelineContext",
            "run_pipeline",
        } <= public
        # Frozen + slotted dataclass shape.
        assert is_dataclass(PipelineRunResult)
        # Nine terminal-result fields per the schema (eight Round 11
        # fields + the dataclass shape itself).
        assert len(fields(PipelineRunResult)) == 9

    def test_blueprint_deps_pinned_to_section_05_v6(
        self,
    ) -> None:
        """:data:`pipeline.loop.run_pipeline.BLUEPRINT_DEPS` is pinned to
        §5 v6 LOCKED 2026-04-19 (hash prefix ``feb5928491e4dc40``). This
        test trips on any silent rebind.
        """

        deps = BLUEPRINT_DEPS["section_05_pipeline.md"]
        assert deps["version"] == "v6"
        assert deps["hash_sha3_512_prefix16"] == "feb5928491e4dc40"

    def test_demo_run_id_format_matches_prefix(
        self,
    ) -> None:
        """Demo runs use the ``demo-mvp`` prefix consistently — caller
        idempotency keys are recognisable in audit logs.
        """

        assert DEMO_RUN_ID_PREFIX == "demo-mvp"
        assert DEMO_ORG_SLUG == "fit_farms"
        assert DEMO_SESSION_ID.startswith("demo-mvp")


# ===========================================================================
# M.7 — Capstone Self-Audit (declarative pin of the demo's invariants;
# would catch silent test-file rewrites that drop categories)
# ===========================================================================


class TestM7CapstoneSelfAudit:
    """Declarative self-pin — names the M.1-M.6 categories so a silent
    re-edit dropping a category trips here.
    """

    def test_demo_test_categories_pinned(self) -> None:
        """The seven demo test classes M.1–M.7 cover the spec card §6
        categories. Classes are imported from this module and verified
        as :class:`type` so a silent class-rename trips this assertion.
        """

        import sys

        module = sys.modules[__name__]
        expected_classes = {
            "TestM1HappyPath",
            "TestM2DegradedMode",
            "TestM3LawEnforcement",
            "TestM4PerformanceGate",
            "TestM5OutputSchema",
            "TestM6CapstoneManifest",
            "TestM7CapstoneSelfAudit",
        }
        observed_classes = {
            name
            for name in dir(module)
            if name.startswith("TestM")
            and isinstance(getattr(module, name), type)
        }
        assert observed_classes == expected_classes

    def test_demo_fixture_files_inventory_pinned(
        self,
        demo_rfa_path: Path,
        demo_project_context_path: Path,
        demo_rubric_path: Path,
        demo_pipeline_output_schema_path: Path,
    ) -> None:
        """Five fixture seams; if any goes missing the demo can't run."""

        for path in (
            demo_rfa_path,
            demo_project_context_path,
            demo_rubric_path,
            demo_pipeline_output_schema_path,
        ):
            assert path.exists(), f"missing demo fixture: {path}"

    def test_demo_uses_locked_section_5_r11_capstone_only(self) -> None:
        """Demo Driver consumes :func:`run_pipeline` (§5 R11 capstone
        LOCKED 2026-04-21) — the symbol is callable + comes from the
        ``pipeline.loop.run_pipeline`` submodule, not from a non-LOCKed
        sibling.

        Reaches the submodule via ``sys.modules`` because
        ``pipeline.loop.__init__`` re-exports ``run_pipeline`` as a
        callable, which shadows the submodule attribute on the package.
        """

        import sys

        rp = sys.modules["pipeline.loop.run_pipeline"]
        assert run_pipeline is rp.run_pipeline
        assert PipelineRunResult is rp.PipelineRunResult
        assert RunPipelineContext is rp.RunPipelineContext
        assert PreGateInputFactory is rp.PreGateInputFactory


# Module-load self-check — test count is at least the spec-card minimum
# (≥1 + ≥5 + ≥5 + ≥1 + ≥1 + ≥5 + ≥3 = ≥21). Pinned here so a silent
# class trim trips the assertion at import time.
_DEMO_TEST_COUNT_FLOOR: Final[int] = 21


def _count_demo_tests_in_module() -> int:
    import sys

    module = sys.modules[__name__]
    total = 0
    for name in dir(module):
        if name.startswith("TestM"):
            cls = getattr(module, name)
            if isinstance(cls, type):
                total += sum(
                    1 for m in dir(cls) if m.startswith("test_")
                )
    return total


assert _count_demo_tests_in_module() >= _DEMO_TEST_COUNT_FLOOR, (
    f"demo driver: test count {_count_demo_tests_in_module()} below floor "
    f"{_DEMO_TEST_COUNT_FLOOR}; silent regression"
)


# Module-load happy-path: the harness imports cleanly and every helper
# resolves. (Pytest will exercise the bodies; this asserts importability.)
__all__ = [
    "DEMO_ORG_SLUG",
    "DEMO_RUN_ID_PREFIX",
    "DEMO_SESSION_ID",
    "EXPECTED_RUBRIC_CRITERIA_COUNT",
    "EXPECTED_RUBRIC_FUNDER",
    "EXPECTED_RUBRIC_MAX_SCORE",
    "EXPECTED_RUBRIC_MIN_SCORE",
    "EXPECTED_RUBRIC_PROGRAM_PREFIX",
    "HAPPY_PATH_LAUNCH_BUDGET",
    "HAPPY_PATH_WRITE_BUDGET",
    "TestM1HappyPath",
    "TestM2DegradedMode",
    "TestM3LawEnforcement",
    "TestM4PerformanceGate",
    "TestM5OutputSchema",
    "TestM6CapstoneManifest",
    "TestM7CapstoneSelfAudit",
]
