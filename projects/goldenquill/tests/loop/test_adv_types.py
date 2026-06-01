"""Adversarial tests — inline-literal RHS integrity for pipeline.loop.types.

Blueprint §5 v6 §3.2.6 + §3.2.1 + §7.13 + §8 V1 closure.

V1 closure's premise: a module-attribute rebinding of TAB_ORDERING must not
affect runtime checks inside dataclass __post_init__. The check uses an
inline tuple literal as RHS, so rebinding the config constant has no effect
on the check outcome.

Strategy: in the PARENT process, rebind `pipeline.loop.config.TAB_ORDERING`
in-memory AFTER import, then attempt to construct a TabEnvelope with the
ADVERSARIAL ordering. The __post_init__ must still raise F_PIPE_16 because
its RHS is a fresh literal at every call, independent of the config module.
"""

from __future__ import annotations

import importlib

import pytest

from pipeline.loop import config as cfg
from pipeline.loop.errors import F_PIPE_16, F_PIPE_21, F_PIPE_22
from pipeline.loop.types import (
    CalibrationReport,
    GoldenSetItem,
    RunState,
    TabEnvelope,
)


@pytest.fixture(autouse=True)
def _restore_config_constants():
    """Restore the original config constants after each test.

    These tests deliberately rebind module attributes in-process to verify
    that inline-literal RHSs are rebind-resistant. We snapshot and restore
    so subsequent tests see the canonical values.
    """
    snapshot = {
        "TAB_ORDERING": cfg.TAB_ORDERING,
        "RUNSTATE_SCHEMA_VERSION": cfg.RUNSTATE_SCHEMA_VERSION,
        "CALIBRATION_REPORT_SCHEMA_VERSION": cfg.CALIBRATION_REPORT_SCHEMA_VERSION,
    }
    yield
    for name, val in snapshot.items():
        setattr(cfg, name, val)
    # Re-import types module to reset any internal caches that may have been
    # affected (there are none, but defence in depth).
    importlib.reload(importlib.import_module("pipeline.loop.types"))


class TestTabEnvelopeInlineLiteralResistance:
    """V1 closure: rebinding pipeline.loop.config.TAB_ORDERING does NOT let a
    reordered ordering pass __post_init__."""

    def test_baseline_reorder_still_blocked_after_config_rebind(self):
        # Attacker rebinds the config constant.
        cfg.TAB_ORDERING = ("deep_brief", "live_radar", "council_draft")  # type: ignore[misc]
        # But the dataclass check uses an inline tuple literal. A reordered
        # tuple passed as tab_ordering must still raise F_PIPE_16.
        with pytest.raises(F_PIPE_16) as ei:
            TabEnvelope(
                run_id="r",
                tab_ordering=("deep_brief", "live_radar", "council_draft"),
                live_radar_payload_hash="a",
                deep_brief_payload_hash="b",
                council_draft_payload_hash="c",
                assembled_at_iso="t",
                envelope_sha256="h",
            )
        assert ei.value.trigger == "tab_envelope_ordering_violation"

    def test_canonical_order_still_accepts_even_after_config_rebind(self):
        cfg.TAB_ORDERING = ("x", "y", "z")  # type: ignore[misc]
        # A canonical-ordered tuple literal still passes.
        te = TabEnvelope(
            run_id="r",
            tab_ordering=("live_radar", "deep_brief", "council_draft"),
            live_radar_payload_hash="a",
            deep_brief_payload_hash="b",
            council_draft_payload_hash="c",
            assembled_at_iso="t",
            envelope_sha256="h",
        )
        assert te.tab_ordering == ("live_radar", "deep_brief", "council_draft")


class TestRunStateSchemaVersionInlineLiteralResistance:
    """Inline-literal `!= 2` RHS in RunState.__post_init__ resists config rebind."""

    def test_schema_version_1_rejected_even_if_config_rebound(self):
        cfg.RUNSTATE_SCHEMA_VERSION = 1  # type: ignore[misc]
        with pytest.raises(F_PIPE_22):
            RunState(
                schema_version=1,
                run_id="r",
                mode="submission",
                rfa_hash="h",
                project_context_hash="p",
                golden_set_ref=None,
                org_slug="x",
                session_id="s",
                phase="initialized",
            )

    def test_rebound_constant_detected_by_defence_in_depth(self):
        # RunState defensively re-checks the module-local constant (imported
        # into types.py at module load). Rebinding that local name to a
        # non-2 value and constructing a RunState whose schema_version
        # equals the inline literal 2 must still be caught by the
        # defence-in-depth check.
        import pipeline.loop.types as typ
        typ.RUNSTATE_SCHEMA_VERSION = 99  # type: ignore[misc]
        try:
            with pytest.raises(F_PIPE_22):
                RunState(
                    schema_version=2,  # satisfies inline !=2 check, but
                    run_id="r",
                    mode="submission",
                    rfa_hash="h",
                    project_context_hash="p",
                    golden_set_ref=None,
                    org_slug="x",
                    session_id="s",
                    phase="initialized",
                )  # ...types-local rebind caught by defence-in-depth
        finally:
            typ.RUNSTATE_SCHEMA_VERSION = 2  # type: ignore[misc]

    def test_schema_version_2_still_passes_with_pristine_config(self):
        # Sanity: without any rebind, schema_version=2 is accepted.
        rs = RunState(
            schema_version=2,
            run_id="r",
            mode="submission",
            rfa_hash="h",
            project_context_hash="p",
            golden_set_ref=None,
            org_slug="x",
            session_id="s",
            phase="initialized",
        )
        assert rs.schema_version == 2


class TestCalibrationSchemaVersionInlineLiteralResistance:
    def test_golden_set_item_schema_version_check_rebind_resistant(self):
        # Attacker rebinds CALIBRATION_REPORT_SCHEMA_VERSION to 2 in hopes
        # of sneaking a version-2 GoldenSetItem through. GoldenSetItem's
        # __post_init__ compares against inline literal 1.
        cfg.CALIBRATION_REPORT_SCHEMA_VERSION = 2  # type: ignore[misc]
        with pytest.raises(F_PIPE_22) as ei:
            GoldenSetItem(
                item_id="x",
                rfa_hash="r",
                project_context_hash="p",
                expected_judge_min_score=1.0,
                expected_topline_claims=(),
                schema_version=2,
            )
        assert ei.value.trigger == "calibration_report_schema_mismatch"

    def test_calibration_report_schema_version_check_rebind_resistant(self):
        cfg.CALIBRATION_REPORT_SCHEMA_VERSION = 2  # type: ignore[misc]
        with pytest.raises(F_PIPE_22):
            CalibrationReport(
                schema_version=2,
                run_id="r",
                org_slug="x",
                golden_set_manifest_hash="h",
                items=(),
                signed_at_iso="t",
                signature=None,
            )


class TestRunStateModeDiscriminationAttackSurface:
    """Attacker tries to slip through mode-discriminated union via edge cases."""

    def test_both_modes_invalid_reject_before_discrimination(self):
        # "other" is not submission or eval; fails at mode validity check.
        with pytest.raises(ValueError, match="mode"):
            RunState(
                schema_version=2,
                run_id="r",
                mode="neither",
                rfa_hash="h",
                project_context_hash="p",
                golden_set_ref=None,
                org_slug="x",
                session_id="s",
                phase="initialized",
            )

    def test_eval_mode_with_calibration_signature_ref_accepted(self):
        # After signing, eval_mode CAN have calibration_signature_ref and
        # calibration_report_ref populated. Verify the discriminator doesn't
        # over-reject.
        rs = RunState(
            schema_version=2,
            run_id="r",
            mode="eval",
            rfa_hash=None,
            project_context_hash=None,
            golden_set_ref="vault/x/gs/m.json",
            org_slug="x",
            session_id="s",
            phase="calibration_signed",
            calibration_report_ref="vault/x/gs/cr.json",
            calibration_signature_ref="vault/x/gs/cr.sig",
        )
        assert rs.calibration_report_ref == "vault/x/gs/cr.json"

    def test_submission_mode_with_tab_envelope_hash_accepted(self):
        # Submission mode CAN set three_tab_envelope_hash after §4.11
        # assemble-and-deliver. Verify not over-rejected.
        rs = RunState(
            schema_version=2,
            run_id="r",
            mode="submission",
            rfa_hash="h",
            project_context_hash="p",
            golden_set_ref=None,
            org_slug="x",
            session_id="s",
            phase="tabs_delivered",
            three_tab_envelope_hash="h",
        )
        assert rs.three_tab_envelope_hash == "h"


class TestFailureTriggerExhaustiveness:
    """Every F_PIPE_21 / F_PIPE_22 sub-trigger triggerable at Round 1 layer
    is exercised by at least one test in test_types."""

    def test_f_pipe_21_triggers_reachable_from_runstate(self):
        # These are the RunState-triggerable subset of F_PIPE_21_TRIGGERS.
        # The remaining 7 triggers are raised by algorithm code in Rounds
        # 2-12 (three_tab_delivery, rate_limiter, eval_mode, etc.).
        reachable = {
            "submission_mode_missing_rfa_hash",
            "submission_mode_missing_project_context_hash",
            "submission_mode_calibration_intent",
            "submission_mode_has_calibration_ref",
            "eval_mode_missing_golden_set_ref",
            "eval_mode_has_rfa_hash",
            "eval_mode_has_project_context_hash",
            "eval_mode_has_tab_envelope_hash",
        }
        # Exercise: construct a bad RunState for each reachable trigger.
        for trig in reachable:
            with pytest.raises(F_PIPE_21) as ei:
                kwargs = dict(
                    schema_version=2,
                    run_id="r",
                    mode="submission",
                    rfa_hash="h",
                    project_context_hash="p",
                    golden_set_ref=None,
                    org_slug="x",
                    session_id="s",
                    phase="initialized",
                )
                if trig == "submission_mode_missing_rfa_hash":
                    kwargs["rfa_hash"] = None
                elif trig == "submission_mode_missing_project_context_hash":
                    kwargs["project_context_hash"] = None
                elif trig == "submission_mode_calibration_intent":
                    kwargs["golden_set_ref"] = "vault/x/gs/m"
                elif trig == "submission_mode_has_calibration_ref":
                    kwargs["calibration_report_ref"] = "vault/x/gs/cr"
                elif trig == "eval_mode_missing_golden_set_ref":
                    kwargs = dict(kwargs, mode="eval", rfa_hash=None,
                                  project_context_hash=None, golden_set_ref=None)
                elif trig == "eval_mode_has_rfa_hash":
                    kwargs = dict(kwargs, mode="eval", rfa_hash="h",
                                  project_context_hash=None,
                                  golden_set_ref="vault/x/gs/m")
                elif trig == "eval_mode_has_project_context_hash":
                    kwargs = dict(kwargs, mode="eval", rfa_hash=None,
                                  project_context_hash="p",
                                  golden_set_ref="vault/x/gs/m")
                elif trig == "eval_mode_has_tab_envelope_hash":
                    kwargs = dict(kwargs, mode="eval", rfa_hash=None,
                                  project_context_hash=None,
                                  golden_set_ref="vault/x/gs/m",
                                  three_tab_envelope_hash="h")
                RunState(**kwargs)
            assert ei.value.trigger == trig, (
                f"Expected trigger {trig!r}, got {ei.value.trigger!r}"
            )
