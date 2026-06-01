"""Tests for pipeline.loop.errors — 22 F-PIPE-* classes + dispatch + sentinel.

Blueprint §5 v6 §6 LOCKED 2026-04-19.
"""

from __future__ import annotations

import pytest

from pipeline.loop.errors import (
    F_EVAL_CROSS_ORG_READ_CODE,
    F_PIPE_01,
    F_PIPE_02,
    F_PIPE_03,
    F_PIPE_04,
    F_PIPE_05,
    F_PIPE_06,
    F_PIPE_07,
    F_PIPE_08,
    F_PIPE_09,
    F_PIPE_10,
    F_PIPE_11,
    F_PIPE_12,
    F_PIPE_13,
    F_PIPE_14,
    F_PIPE_15,
    F_PIPE_16,
    F_PIPE_17,
    F_PIPE_18,
    F_PIPE_19,
    F_PIPE_20,
    F_PIPE_21,
    F_PIPE_22,
    F_PIPE_BY_CODE,
    PipelineFailure,
)

_ALL_CLASSES = [
    F_PIPE_01, F_PIPE_02, F_PIPE_03, F_PIPE_04, F_PIPE_05, F_PIPE_06,
    F_PIPE_07, F_PIPE_08, F_PIPE_09, F_PIPE_10, F_PIPE_11, F_PIPE_12,
    F_PIPE_13, F_PIPE_14, F_PIPE_15, F_PIPE_16, F_PIPE_17, F_PIPE_18,
    F_PIPE_19, F_PIPE_20, F_PIPE_21, F_PIPE_22,
]

_EXPECTED_META = {
    "F-PIPE-01": ("CRIT", "state-failure + quarantine marker"),
    "F-PIPE-02": ("HIGH", "state-failure"),
    "F-PIPE-03": ("HIGH", "state-failure"),
    "F-PIPE-04": ("MED", "state-failure"),
    "F-PIPE-05": ("MED", "state-failure"),
    "F-PIPE-06": ("HIGH", "state-failure"),
    "F-PIPE-07": ("HIGH", "state-failure"),
    "F-PIPE-08": ("CRIT", "state-failure + admin-risk CRIT"),
    "F-PIPE-09": ("HIGH", "state-failure (never success)"),
    "F-PIPE-10": ("LOW", "state-failure"),
    "F-PIPE-11": ("LOW", "state-failure (post-checkpoint)"),
    "F-PIPE-12": ("HIGH", "state-failure"),
    "F-PIPE-13": ("CRIT", "state-failure + bypass-pending"),
    "F-PIPE-14": ("HIGH", "state-failure"),
    "F-PIPE-15": ("HIGH", "state-failure"),
    "F-PIPE-16": ("CRIT", "state-failure + admin-risk CRIT"),
    "F-PIPE-17": ("CRIT", "state-failure"),
    "F-PIPE-18": ("CRIT", "state-failure + quarantine"),
    "F-PIPE-19": ("CRIT", "state-failure + admin-risk CRIT"),
    "F-PIPE-20": ("CRIT", "state-failure"),
    "F-PIPE-21": ("CRIT", "state-failure + admin-risk CRIT"),
    "F-PIPE-22": ("CRIT", "state-failure + quarantine"),
}


class TestClassSurface:
    def test_all_subclass_of_pipeline_failure(self):
        for cls in _ALL_CLASSES:
            assert issubclass(cls, PipelineFailure)
            assert issubclass(cls, Exception)

    def test_every_class_pins_code_severity_save_state(self):
        for cls in _ALL_CLASSES:
            expected_code = cls.__name__.replace("_", "-")
            # e.g. F_PIPE_01 -> F-PIPE-01
            expected_code = "-".join(expected_code.split("-"))
            assert cls.CODE == expected_code, (
                f"{cls.__name__}.CODE = {cls.CODE!r}, expected {expected_code!r}"
            )
            assert cls.SEVERITY in {"CRIT", "HIGH", "MED", "LOW"}
            assert cls.SAVE_STATE_CONTRACT, (
                f"{cls.__name__}.SAVE_STATE_CONTRACT must be non-empty"
            )

    def test_severity_and_save_state_match_blueprint(self):
        for cls in _ALL_CLASSES:
            expected_sev, expected_save = _EXPECTED_META[cls.CODE]
            assert cls.SEVERITY == expected_sev, (
                f"{cls.__name__}.SEVERITY = {cls.SEVERITY!r}, expected {expected_sev!r}"
            )
            assert cls.SAVE_STATE_CONTRACT == expected_save, (
                f"{cls.__name__}.SAVE_STATE_CONTRACT mismatch for {cls.CODE}"
            )


class TestDispatchTable:
    def test_size(self):
        assert len(F_PIPE_BY_CODE) == 22

    def test_keys_contiguous(self):
        expected = {f"F-PIPE-{i:02d}" for i in range(1, 23)}
        assert set(F_PIPE_BY_CODE) == expected

    def test_values_bijective(self):
        # Every key maps to a distinct class; class back to the same key.
        for code, cls in F_PIPE_BY_CODE.items():
            assert cls.CODE == code
        assert len({id(c) for c in F_PIPE_BY_CODE.values()}) == 22


class TestConstruction:
    def test_f_pipe_01_basic(self):
        exc = F_PIPE_01(trigger="cas_exhausted", details={"attempts": 3})
        assert exc.code == "F-PIPE-01"
        assert exc.trigger == "cas_exhausted"
        assert exc.details == {"attempts": 3}
        assert isinstance(exc, PipelineFailure)

    def test_base_pipeline_failure_accepts_explicit_code(self):
        exc = PipelineFailure("F-PIPE-XX", trigger="bespoke")
        assert exc.code == "F-PIPE-XX"
        assert exc.trigger == "bespoke"

    def test_exception_can_be_raised_and_caught(self):
        with pytest.raises(F_PIPE_01) as ei:
            raise F_PIPE_01(trigger="cas_exhausted")
        assert ei.value.code == "F-PIPE-01"
        # Can also be caught via the base class
        with pytest.raises(PipelineFailure):
            raise F_PIPE_08(trigger="no_cross_family_level")


class TestFPipe21TriggerValidation:
    def test_valid_trigger_accepted(self):
        exc = F_PIPE_21(trigger="eval_mode_has_tab_envelope_hash")
        assert exc.trigger == "eval_mode_has_tab_envelope_hash"

    def test_invalid_trigger_rejected(self):
        with pytest.raises(ValueError, match="F_PIPE_21_TRIGGERS"):
            F_PIPE_21(trigger="made_up_trigger")

    def test_empty_trigger_rejected(self):
        # Empty trigger is not in the enumerated set.
        with pytest.raises(ValueError):
            F_PIPE_21()


class TestFPipe22TriggerValidation:
    def test_valid_trigger_accepted(self):
        exc = F_PIPE_22(trigger="runstate_schema_downgrade")
        assert exc.trigger == "runstate_schema_downgrade"

    def test_calibration_report_schema_trigger_accepted(self):
        exc = F_PIPE_22(trigger="calibration_report_schema_mismatch")
        assert exc.trigger == "calibration_report_schema_mismatch"

    def test_invalid_trigger_rejected(self):
        with pytest.raises(ValueError, match="F_PIPE_22_TRIGGERS"):
            F_PIPE_22(trigger="runstate_schema_upgrade")


class TestForwardDepSentinel:
    def test_code_string(self):
        assert F_EVAL_CROSS_ORG_READ_CODE == "F-EVAL-CROSS-ORG-READ"

    def test_no_class_exported(self):
        # Section 4 owns the class; Section 5 only exports the code string.
        # Verify no F_EVAL_CROSS_ORG_READ class exists in pipeline.loop.errors.
        import pipeline.loop.errors as errs
        assert not hasattr(errs, "F_EVAL_CROSS_ORG_READ")
