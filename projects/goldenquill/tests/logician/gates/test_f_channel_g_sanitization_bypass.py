"""Unit tests for F-CHANNEL-G-SANITIZATION-BYPASS (advisory, P1).

Per architecture v7.0.5 §3 + §5.4.
"""

from __future__ import annotations

from pipeline.logician.gates.f_channel_g_sanitization_bypass import (
    F_CHANNEL_G_SANITIZATION_BYPASS,
    check_channel_g_sanitization_bypass,
)


def test_failure_code_constant() -> None:
    assert F_CHANNEL_G_SANITIZATION_BYPASS == "F-CHANNEL-G-SANITIZATION-BYPASS"


def test_no_transform_passes() -> None:
    r = check_channel_g_sanitization_bypass(
        transform_invoked=False,
        sanitization_reinvoked_after_transform=False,
    )
    assert r.success is True
    assert r.failure_code is None


def test_transform_with_resanitize_passes() -> None:
    r = check_channel_g_sanitization_bypass(
        transform_invoked=True,
        sanitization_reinvoked_after_transform=True,
        transform_name="markdown_render",
    )
    assert r.success is True


def test_transform_without_resanitize_advisory_fails() -> None:
    r = check_channel_g_sanitization_bypass(
        transform_invoked=True,
        sanitization_reinvoked_after_transform=False,
        transform_name="pdf_to_text",
    )
    assert r.success is False
    assert r.failure_code == F_CHANNEL_G_SANITIZATION_BYPASS
    assert r.advisory is True
    assert "pdf_to_text" in r.detail


def test_transform_name_appears_in_detail() -> None:
    r = check_channel_g_sanitization_bypass(
        transform_invoked=True,
        sanitization_reinvoked_after_transform=True,
        transform_name="docx_extract",
    )
    assert "docx_extract" in r.detail


def test_advisory_flag_default_true() -> None:
    # The advisory flag defaults True so admin-risk routing knows this is
    # a non-blocking advisory rather than a hard-block deny.
    r = check_channel_g_sanitization_bypass(
        transform_invoked=False,
        sanitization_reinvoked_after_transform=False,
    )
    assert r.advisory is True
