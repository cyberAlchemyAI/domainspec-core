"""F-CHANNEL-G-SANITIZATION-BYPASS — advisory gate (P1).

Per architecture v7.0.5 §3 + §5.4 + companion `section_04_v7_0_5_companion.md`.
Downstream components that further transform Channel G extracted text
(decoders, format converters, render pipelines) MUST invoke the
sanitization wrapper as a POST-transform check. If a transform happened
and sanitization was NOT re-invoked, this gate raises an advisory at the
next REVIEW gate.

This is an *advisory* — it does not block; it surfaces to the operator
for review. The blocking gate is F-CHANNEL-G-CROSS-ORG-LEAK (POST-extract,
fires on actual leaks). Together the two gates compose: SANITIZATION-BYPASS
catches the architectural-discipline violation BEFORE leaks happen;
CROSS-ORG-LEAK catches the leak when sanitization-discipline failed.

No M13 bypass needed — advisory tier.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_CHANNEL_G_SANITIZATION_BYPASS: Final[str] = "F-CHANNEL-G-SANITIZATION-BYPASS"


@dataclass(frozen=True, kw_only=True)
class SanitizationBypassResult:
    """Result of F-CHANNEL-G-SANITIZATION-BYPASS check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    advisory: bool = True


def check_channel_g_sanitization_bypass(
    *,
    transform_invoked: bool,
    sanitization_reinvoked_after_transform: bool,
    transform_name: str = "<unknown>",
) -> SanitizationBypassResult:
    """Advisory gate: any post-extract transform must re-invoke sanitization.

    Parameters
    ----------
    transform_invoked
        Whether a downstream transform (decoder, format converter, render
        pipeline) ran after the original Channel G extract.
    sanitization_reinvoked_after_transform
        Whether the sanitization wrapper was re-invoked AFTER the transform.
    transform_name
        Descriptive name of the transform for audit-trail clarity.

    Returns
    -------
    SanitizationBypassResult. Passes when (a) no transform happened, OR
    (b) transform happened AND sanitization was re-invoked. Fails (advisory)
    when transform happened AND sanitization was NOT re-invoked.
    """
    if not transform_invoked:
        return SanitizationBypassResult(
            success=True,
            failure_code=None,
            detail="no downstream transform; sanitization-discipline N/A",
        )
    if sanitization_reinvoked_after_transform:
        return SanitizationBypassResult(
            success=True,
            failure_code=None,
            detail=(
                f"transform {transform_name!r} ran AND sanitization was "
                "re-invoked post-transform"
            ),
        )
    return SanitizationBypassResult(
        success=False,
        failure_code=F_CHANNEL_G_SANITIZATION_BYPASS,
        detail=(
            f"transform {transform_name!r} ran without post-transform "
            "sanitization re-invocation; advisory raised for operator "
            "REVIEW (does not block; F-CHANNEL-G-CROSS-ORG-LEAK is the "
            "blocking gate if a leak materialized)"
        ),
    )
