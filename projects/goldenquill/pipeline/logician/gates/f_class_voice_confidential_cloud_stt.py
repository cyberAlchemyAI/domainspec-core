"""F-CLASS-VOICE-CONFIDENTIAL-CLOUD-STT — Voice posture gate.

Per architecture v7.0.10, Voice is an operator interface.
Fails closed if the deployment posture is Split-Context Hybrid or
Local-Only / Sovereign, and the payload is confidential, but the STT
is running in the cloud.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT: Final[str] = (
    "F-CLASS-VOICE-CONFIDENTIAL-CLOUD-STT"
)

# Canonical postures from v7.0.10
POSTURE_PUBLIC_FRONTIER: Final[str] = "Frontier-Eligible"
POSTURE_SPLIT_CONTEXT: Final[str] = "Split-Context Hybrid"
POSTURE_LOCAL_ONLY: Final[str] = "Local-Only / Sovereign"

_PROTECTED_POSTURES: Final[frozenset[str]] = frozenset({
    POSTURE_SPLIT_CONTEXT,
    POSTURE_LOCAL_ONLY,
})


@dataclass(frozen=True, kw_only=True)
class VoiceConfidentialCloudSttResult:
    """Result of F-CLASS-VOICE-CONFIDENTIAL-CLOUD-STT check."""

    success: bool
    failure_code: Optional[str]
    detail: str


def check_voice_confidential_cloud_stt(
    *,
    deployment_posture: str,
    payload_is_confidential: bool,
    stt_provider: str,
) -> VoiceConfidentialCloudSttResult:
    """Fails closed if protected posture sends confidential audio to cloud STT.

    Parameters
    ----------
    deployment_posture
        The current routing posture per v7.0.10 naming (e.g. "Split-Context Hybrid").
    payload_is_confidential
        Boolean indicating if the session contains confidential facts/flags.
    stt_provider
        The name of the Speech-To-Text provider. "local" is considered on-device.

    Returns
    -------
    VoiceConfidentialCloudSttResult. PASS only when non-protected posture OR
    non-confidential payload OR local STT is used.
    """
    if not isinstance(deployment_posture, str):
        return VoiceConfidentialCloudSttResult(
            success=False,
            failure_code=F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT,
            detail=f"deployment_posture must be string, got {type(deployment_posture).__name__}",
        )

    if not isinstance(payload_is_confidential, bool):
        return VoiceConfidentialCloudSttResult(
            success=False,
            failure_code=F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT,
            detail=f"payload_is_confidential must be bool, got {type(payload_is_confidential).__name__}",
        )

    if not isinstance(stt_provider, str):
        return VoiceConfidentialCloudSttResult(
            success=False,
            failure_code=F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT,
            detail=f"stt_provider must be string, got {type(stt_provider).__name__}",
        )

    is_cloud_stt = stt_provider.lower() != "local"

    if deployment_posture in _PROTECTED_POSTURES and payload_is_confidential and is_cloud_stt:
        return VoiceConfidentialCloudSttResult(
            success=False,
            failure_code=F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT,
            detail=(
                f"posture '{deployment_posture}' + confidential payload cannot be "
                f"routed to cloud STT ('{stt_provider}') — P0 fail-closed"
            )
        )

    return VoiceConfidentialCloudSttResult(
        success=True,
        failure_code=None,
        detail="Voice posture + payload + STT provider configuration is valid",
    )


__all__ = [
    "F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT",
    "POSTURE_PUBLIC_FRONTIER",
    "POSTURE_SPLIT_CONTEXT",
    "POSTURE_LOCAL_ONLY",
    "VoiceConfidentialCloudSttResult",
    "check_voice_confidential_cloud_stt",
]
