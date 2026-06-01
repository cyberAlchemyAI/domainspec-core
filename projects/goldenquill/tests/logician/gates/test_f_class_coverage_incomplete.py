"""Unit tests for F-CLASS-COVERAGE-INCOMPLETE (META PRE-cycle)."""

from __future__ import annotations

import os

from pipeline.logician.gates.f_class_coverage_incomplete import (
    CoverageEntry,
    F_CLASS_COVERAGE_INCOMPLETE,
    REQUIRED_F_CLASS_CODES,
    check_class_coverage_incomplete,
)


def _full_coverage_entries() -> list[CoverageEntry]:
    """Live on-disk coverage matching the WS-L Slice 3 module + test paths."""
    repo_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )

    def m(name: str) -> str:
        return os.path.join(repo_root, "pipeline", "logician", "gates", name)

    def t(name: str) -> str:
        return os.path.join(repo_root, "tests", "logician", "gates", name)

    return [
        CoverageEntry(
            code="F-CLASS-REGISTER-MISSING",
            module_path=m("f_class_register.py"),
            test_path=t("test_f_class_register.py"),
        ),
        CoverageEntry(
            code="F-CLASS-REGISTER-UNSIGNED",
            module_path=m("f_class_register.py"),
            test_path=t("test_f_class_register.py"),
        ),
        CoverageEntry(
            code="F-CLASS-REGISTER-SIGNATURE-INVALID",
            module_path=m("f_class_register.py"),
            test_path=t("test_f_class_register.py"),
        ),
        CoverageEntry(
            code="F-CLASS-REGISTER-HASH-MISMATCH",
            module_path=m("f_class_register.py"),
            test_path=t("test_f_class_register.py"),
        ),
        CoverageEntry(
            code="F-CLASS-NEW-FACT-UNCLASSIFIED",
            module_path=m("f_class_new_fact_unclassified.py"),
            test_path=t("test_f_class_new_fact_unclassified.py"),
        ),
        CoverageEntry(
            code="F-CLASS-ROUTING-INDETERMINATE",
            module_path=m("f_class_routing_indeterminate.py"),
            test_path=t("test_f_class_routing_indeterminate.py"),
        ),
        CoverageEntry(
            code="F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL",
            module_path=m("f_class_outbound_boundary.py"),
            test_path=t("test_f_class_outbound_boundary.py"),
        ),
        CoverageEntry(
            code="F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED",
            module_path=m("f_class_outbound_boundary.py"),
            test_path=t("test_f_class_outbound_boundary.py"),
        ),
        CoverageEntry(
            code="F-CLASS-SLOT-ID-NON-OPAQUE",
            module_path=m("f_class_outbound_boundary.py"),
            test_path=t("test_f_class_outbound_boundary.py"),
        ),
        CoverageEntry(
            code="F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED",
            module_path=m("f_class_per_grant_override.py"),
            test_path=t("test_f_class_per_grant_override.py"),
        ),
        CoverageEntry(
            code="F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID",
            module_path=m("f_class_router_template_signature.py"),
            test_path=t("test_f_class_router_template_signature.py"),
        ),
        CoverageEntry(
            code="F-CLASS-HIGH-STAKES-FLAG-LEAK",
            module_path=m("f_class_outbound_boundary.py"),
            test_path=t("test_f_class_outbound_boundary.py"),
        ),
        CoverageEntry(
            code="F-CLASS-VOICE-CONFIDENTIAL-CLOUD-STT",
            module_path=m("f_class_voice_confidential_cloud_stt.py"),
            test_path=t("test_f_class_voice_confidential_cloud_stt.py"),
        ),
    ]


def test_failure_code_constant() -> None:
    assert F_CLASS_COVERAGE_INCOMPLETE == "F-CLASS-COVERAGE-INCOMPLETE"


def test_required_codes_eleven_others_plus_high_stakes() -> None:
    # Thirteen total after the v7.0.10 voice-STT gate. The COVERAGE gate
    # excludes itself from its own audit target.
    assert len(REQUIRED_F_CLASS_CODES) == 13
    assert "F-CLASS-COVERAGE-INCOMPLETE" not in REQUIRED_F_CLASS_CODES
    assert "F-CLASS-HIGH-STAKES-FLAG-LEAK" in REQUIRED_F_CLASS_CODES
    assert "F-CLASS-VOICE-CONFIDENTIAL-CLOUD-STT" in REQUIRED_F_CLASS_CODES


def test_full_coverage_passes_with_real_paths() -> None:
    """With every Slice 3 module + test on disk, the gate passes."""
    r = check_class_coverage_incomplete(
        coverage_entries=_full_coverage_entries(),
        file_exists=os.path.exists,
    )
    assert r.success is True, r.detail
    assert r.failure_code is None


def test_missing_coverage_entry_fails() -> None:
    entries = [
        entry
        for entry in _full_coverage_entries()
        if entry.code != "F-CLASS-HIGH-STAKES-FLAG-LEAK"
    ]
    r = check_class_coverage_incomplete(
        coverage_entries=entries,
        file_exists=os.path.exists,
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_COVERAGE_INCOMPLETE
    assert "F-CLASS-HIGH-STAKES-FLAG-LEAK" in r.missing_codes


def test_missing_module_file_fails() -> None:
    entries = _full_coverage_entries()
    # Replace the first entry's module path with one that does not exist.
    entries[0] = CoverageEntry(
        code=entries[0].code,
        module_path="/nonexistent/path/to/missing_module.py",
        test_path=entries[0].test_path,
    )
    r = check_class_coverage_incomplete(
        coverage_entries=entries,
        file_exists=os.path.exists,
    )
    assert r.success is False
    assert any("missing_module.py" in m for m in r.missing_modules)


def test_missing_test_file_fails() -> None:
    entries = _full_coverage_entries()
    entries[0] = CoverageEntry(
        code=entries[0].code,
        module_path=entries[0].module_path,
        test_path="/nonexistent/path/to/missing_test.py",
    )
    r = check_class_coverage_incomplete(
        coverage_entries=entries,
        file_exists=os.path.exists,
    )
    assert r.success is False
    assert any("missing_test.py" in t for t in r.missing_tests)


def test_file_exists_raises_fails() -> None:
    def boom(_p: str) -> bool:
        raise PermissionError("denied")

    r = check_class_coverage_incomplete(
        coverage_entries=_full_coverage_entries(),
        file_exists=boom,
    )
    assert r.success is False
    assert "PermissionError" in r.detail


def test_empty_coverage_entries_fails_all() -> None:
    r = check_class_coverage_incomplete(
        coverage_entries=[],
        file_exists=lambda _p: True,
    )
    assert r.success is False
    # All required codes should surface as missing entries (first
    # five surfaced in tuple).
    assert len(r.missing_codes) == 5


def test_no_m13_bypass_in_detail() -> None:
    """Per §5.1: the META gate has NO M13 — Beta deployment is bound."""
    r = check_class_coverage_incomplete(
        coverage_entries=[],
        file_exists=lambda _p: True,
    )
    assert r.success is False
    assert "no M13" in r.detail or "architectural commitment" in r.detail
