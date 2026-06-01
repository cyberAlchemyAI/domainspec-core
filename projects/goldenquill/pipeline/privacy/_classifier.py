"""Content-scan classifier contract and v0.1 stub.

Blueprint §4 v2.3 §4.14 LOCKED 2026-04-19.
v0.1: stub always returns CLASSIFIER_ERROR (fail-closed → LOCAL-ONLY).
v0.2: replace this module with a real local classifier running inside the 128GB envelope (A1).
"""

from __future__ import annotations

from enum import Enum
from typing import Final

BLUEPRINT_DEPS: Final[dict] = {
    "section_04_v2_3_amendment.md": {
        "sections_implemented": ["§4.14 classifier contract"],
        "hash_source_version": "v2.3",
    },
}


class PrivacyTag(str, Enum):
    """Classifier output tag [§4.14]."""

    LOCAL_ONLY = "LOCAL_ONLY"
    CLOUD_ELIGIBLE = "CLOUD_ELIGIBLE"
    CLASSIFIER_ERROR = "CLASSIFIER_ERROR"


def classify_payload(payload: str) -> PrivacyTag:
    """Content-scan classifier stub (v0.1). [§4.14]

    Returns CLASSIFIER_ERROR unconditionally — fail-closed maps to LOCAL-ONLY routing.
    v0.2 wires a real local classifier here; interface is unchanged.
    """
    _ = payload  # v0.1 stub: input is intentionally unused
    return PrivacyTag.CLASSIFIER_ERROR
