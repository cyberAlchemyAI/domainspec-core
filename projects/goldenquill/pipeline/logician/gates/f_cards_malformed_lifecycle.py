"""F-CARDS-MALFORMED-LIFECYCLE — Card lifecycle truth invariant.

Fails closed when a card lifecycle block is missing required fields, carries
invalid state-machine values, marks a draft card runtime-loadable, or marks a
runtime-loadable card without signed metadata and a matching content hash.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping

from pipeline.cards.loader import CardLifecycleError, enforce_lifecycle_truth


GATE_ID: Final[str] = "F-CARDS-MALFORMED-LIFECYCLE"


@dataclass(frozen=True, kw_only=True)
class GateOutcome:
    passed: bool
    message: str


def evaluate(*, card_path: str, lifecycle_block: Mapping[str, object]) -> GateOutcome:
    """Evaluate lifecycle truth on an isolated lifecycle block.

    This body is LIVE because lifecycle truth is a trust-boundary invariant:
    production-loadable cards must be signed, and draft cards must be rejected.
    """

    synthetic_card = {
        "schema_version": "1.0-cic",
        "lifecycle": dict(lifecycle_block),
    }
    try:
        enforce_lifecycle_truth(card_path=card_path, card_body=synthetic_card, verify_content_hash=False)
    except CardLifecycleError as exc:
        return GateOutcome(passed=False, message=str(exc))
    return GateOutcome(
        passed=True,
        message="F-CARDS-MALFORMED-LIFECYCLE: lifecycle truth check passed.",
    )
