"""Privacy Router PRE-gate — §4.2.1 Row 21 implementation.

Blueprint §4 v2.3 §4.14 LOCKED 2026-04-19.
Gate runs between seat selection and model dispatch; forces LOCAL-ONLY routing
when classifier returns LOCAL_ONLY or CLASSIFIER_ERROR (fail-closed).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final

from pipeline.privacy._classifier import PrivacyTag, classify_payload

BLUEPRINT_DEPS: Final[dict] = {
    "section_04_v2_3_amendment.md": {
        "sections_implemented": ["§4.14 gate logic", "§6 failure codes v2.3"],
        "hash_source_version": "v2.3",
    },
}

PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR: Final[str] = "F-PRIVACY-CLASSIFIER-ERROR"
PRIVACY_FAILURE_CODE_BYPASS_ATTEMPT: Final[str] = (
    "F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED"
)


@dataclass(frozen=True)
class PrivacyRouteResult:
    """Result of the Privacy Router PRE-gate (§4.14).

    The caller (§4.2.1 Row 21 / Section 5 orchestrator) MUST force local
    routing when routed_local is True, regardless of the seat's default routing.
    Attempting a cloud dispatch after routed_local=True constitutes a bypass
    attempt and must be reported as F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED.
    """

    tag: PrivacyTag
    routed_local: bool
    failure_code: str | None
    detail: dict[str, Any] | None


def run_privacy_pregate(
    payload: str,
    seat: str,
    default_routing: str,
) -> PrivacyRouteResult:
    """Privacy Router content-scan PRE-gate (§4.14). [§4.2.1 Row 21]

    Parameters
    ----------
    payload : str
        Raw inbound query string before any seat-specific formatting.
    seat : str
        Seat name from router.yaml (e.g. "scribe", "judge").
    default_routing : str
        Seat's configured routing: "local" or "cloud".

    Returns
    -------
    PrivacyRouteResult
        Always returns a result; never raises. Classifier exceptions are caught
        and treated as CLASSIFIER_ERROR (fail-closed semantics per §4.14).
    """
    try:
        tag = classify_payload(payload)
    except Exception as exc:
        return PrivacyRouteResult(
            tag=PrivacyTag.CLASSIFIER_ERROR,
            routed_local=True,
            failure_code=PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR,
            detail={
                "seat": seat,
                "default_routing": default_routing,
                "sub_tag": "classifier_exception",
                "exception": str(exc),
            },
        )

    # Type guard before equality check. An attacker-replaced classifier could
    # return an object whose __eq__ claims equality with PrivacyTag.CLOUD_ELIGIBLE
    # while not actually being a PrivacyTag member (adversarial review Finding F1,
    # phase0_through_2b_2026-04-19). Reject anything that is not one of the three
    # canonical members — fail-closed to LOCAL-ONLY.
    if not isinstance(tag, PrivacyTag):
        return PrivacyRouteResult(
            tag=PrivacyTag.CLASSIFIER_ERROR,
            routed_local=True,
            failure_code=PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR,
            detail={
                "seat": seat,
                "default_routing": default_routing,
                "sub_tag": "classifier_returned_non_privacytag",
                "returned_type": type(tag).__name__,
            },
        )

    if tag == PrivacyTag.CLOUD_ELIGIBLE:
        return PrivacyRouteResult(
            tag=tag,
            routed_local=False,
            failure_code=None,
            detail=None,
        )

    if tag == PrivacyTag.LOCAL_ONLY:
        return PrivacyRouteResult(
            tag=tag,
            routed_local=True,
            failure_code=None,
            detail={"seat": seat, "default_routing": default_routing},
        )

    # CLASSIFIER_ERROR (and any unexpected tag value — defense-in-depth).
    return PrivacyRouteResult(
        tag=PrivacyTag.CLASSIFIER_ERROR,
        routed_local=True,
        failure_code=PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR,
        detail={
            "seat": seat,
            "default_routing": default_routing,
            "sub_tag": "stub_always_fires",
        },
    )
