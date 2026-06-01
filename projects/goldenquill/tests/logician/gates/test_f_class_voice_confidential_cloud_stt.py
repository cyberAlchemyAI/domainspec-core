"""Unit tests for the voice confidential cloud STT gate."""

from __future__ import annotations

from pipeline.logician.gates.f_class_voice_confidential_cloud_stt import (
    F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT,
    POSTURE_LOCAL_ONLY,
    POSTURE_PUBLIC_FRONTIER,
    POSTURE_SPLIT_CONTEXT,
    check_voice_confidential_cloud_stt,
)


def test_protected_posture_confidential_cloud_stt_fails() -> None:
    result = check_voice_confidential_cloud_stt(
        deployment_posture=POSTURE_SPLIT_CONTEXT,
        payload_is_confidential=True,
        stt_provider="cloud-vendor",
    )

    assert result.success is False
    assert result.failure_code == F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT
    assert "confidential payload" in result.detail


def test_local_stt_in_protected_posture_passes() -> None:
    result = check_voice_confidential_cloud_stt(
        deployment_posture=POSTURE_LOCAL_ONLY,
        payload_is_confidential=True,
        stt_provider="local",
    )

    assert result.success is True
    assert result.failure_code is None


def test_public_frontier_non_confidential_cloud_stt_passes() -> None:
    result = check_voice_confidential_cloud_stt(
        deployment_posture=POSTURE_PUBLIC_FRONTIER,
        payload_is_confidential=False,
        stt_provider="cloud-vendor",
    )

    assert result.success is True
    assert result.failure_code is None


def test_non_string_posture_fails_closed() -> None:
    result = check_voice_confidential_cloud_stt(
        deployment_posture=None,  # type: ignore[arg-type]
        payload_is_confidential=True,
        stt_provider="local",
    )

    assert result.success is False
    assert result.failure_code == F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT
