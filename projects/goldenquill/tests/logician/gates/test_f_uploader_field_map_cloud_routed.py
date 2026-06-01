"""Tests for F-UPLOADER-FIELD-MAP-CLOUD-ROUTED (PRE).

Spec: pipeline/blueprint/v0.1/section_12_uploader.md §12.9.6.
Predicate: pipeline/logician/gates/f_uploader_field_map_cloud_routed.py.
Authored as §12 v1 LOCK companion edit per Audit-#1 RT-5c closure
(2026-05-10).
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates.f_uploader_field_map_cloud_routed import (
    FieldMapCallContext,
    check_uploader_field_map_cloud_routed,
)


def _ctx(routed_to: str = "local", classification_at_call: str = "confidential") -> FieldMapCallContext:
    return FieldMapCallContext(
        portal_field_id="sf424.applicant_name",
        portal_field_label="Applicant Name",
        caller_module="pipeline.orchestrator.seats.uploader_adapters.grants_gov",
        routed_to=routed_to,  # type: ignore[arg-type]
        model_id="ollama/mistral:7b",
        classification_at_call=classification_at_call,  # type: ignore[arg-type]
    )


def test_local_routing_passes() -> None:
    result = check_uploader_field_map_cloud_routed(_ctx(routed_to="local"))
    assert result.passed is True
    assert result.code is None


def test_cloud_routing_fails() -> None:
    result = check_uploader_field_map_cloud_routed(_ctx(routed_to="cloud"))
    assert result.passed is False
    assert result.code == "F-UPLOADER-FIELD-MAP-CLOUD-ROUTED"
    assert "cloud" in (result.detail or "")


def test_unknown_routing_fails_closed() -> None:
    """Anything other than the literal 'local' fails closed (defense in depth)."""

    class _MockCtx:
        routed_to = "unknown_provider"

    result = check_uploader_field_map_cloud_routed(_MockCtx())  # type: ignore[arg-type]
    assert result.passed is False
    assert result.code == "F-UPLOADER-FIELD-MAP-CLOUD-ROUTED"


def test_missing_routed_to_attribute_fails_closed() -> None:
    """A bogus context with no `routed_to` attribute is rejected."""

    class _Bogus:
        pass

    result = check_uploader_field_map_cloud_routed(_Bogus())  # type: ignore[arg-type]
    assert result.passed is False
    assert result.code == "F-UPLOADER-FIELD-MAP-CLOUD-ROUTED"


def test_classification_field_does_not_relax_gate() -> None:
    """Public classification does NOT permit cloud routing — gate is unconditional."""
    result = check_uploader_field_map_cloud_routed(
        _ctx(routed_to="cloud", classification_at_call="public")
    )
    assert result.passed is False
    assert result.code == "F-UPLOADER-FIELD-MAP-CLOUD-ROUTED"
