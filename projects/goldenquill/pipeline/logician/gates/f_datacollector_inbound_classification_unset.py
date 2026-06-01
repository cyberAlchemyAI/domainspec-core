"""F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET — PRE pre-write gate.

Per §13 Data Collector v1 LOCKED 2026-05-10 §13.9.6 + Cycle-2 RT-C2-11
closure (classification register signature re-verified at every inbound
write).

Refuses inbound write to operational-data sub-kind where classification has
not been operator-set for this ``(recipient_id, field_class)`` pair.
Mirrors Intake INCREMENTAL discipline per v7.0.7 §4.1 + §11 v1 — new
inbound facts default ``confidential`` until operator re-classifies.

Sub-tags:

* ``.first_occurrence_unclassified``
* ``.default_confidential_pending_review``
* ``.classification_register_tampered`` (RT-C2-11)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping, Optional

F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET: Final[str] = (
    "F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET"
)

PERMITTED_CLASSIFICATIONS: Final[frozenset[str]] = frozenset({
    "public",
    "shareable",
    "confidential",
    "operator_flagged",
})

PERMITTED_STATUSES: Final[frozenset[str]] = frozenset({
    "OPERATOR_CLASSIFIED",
    "DEFAULT_CONFIDENTIAL_PENDING_REVIEW",
})

SUB_TAG_FIRST_OCCURRENCE_UNCLASSIFIED: Final[str] = (
    ".first_occurrence_unclassified"
)
SUB_TAG_DEFAULT_CONFIDENTIAL_PENDING_REVIEW: Final[str] = (
    ".default_confidential_pending_review"
)
SUB_TAG_CLASSIFICATION_REGISTER_TAMPERED: Final[str] = (
    ".classification_register_tampered"
)


@dataclass(frozen=True, kw_only=True)
class InboundClassificationResult:
    """Result of F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET check."""

    success: bool
    failure_code: Optional[str]
    sub_tag: Optional[str]
    detail: str
    recipient_id: Optional[str] = None
    field_class: Optional[str] = None


def check_inbound_classification_unset(
    *,
    recipient_id: str,
    field_class: str,
    classification_register_signature_valid: bool,
    register_entry: Optional[Mapping[str, object]],
) -> InboundClassificationResult:
    """PRE pre-write classification check.

    Parameters
    ----------
    recipient_id
        Per-recipient opaque identifier.
    field_class
        Field class name (e.g., ``numeric_metric_graduates`` /
        ``narrative_quote`` / ``beneficiary_record``).
    classification_register_signature_valid
        RT-C2-11: caller verifies the register Ed25519 signature on each
        read; pass the result here.
    register_entry
        ``None`` = no entry for ``(recipient_id, field_class)`` →
        first-occurrence unclassified. ``{"classification_status":
        "DEFAULT_CONFIDENTIAL_PENDING_REVIEW"}`` → operator deferred.
        ``{"classification_status": "OPERATOR_CLASSIFIED",
        "classification": <class>}`` → PASS iff classification in
        PERMITTED_CLASSIFICATIONS.
    """
    if not classification_register_signature_valid:
        return InboundClassificationResult(
            success=False,
            failure_code=F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET,
            sub_tag=SUB_TAG_CLASSIFICATION_REGISTER_TAMPERED,
            detail=(
                "classification_register Ed25519 signature does not verify; "
                "refuse inbound write — admin-risk TAMPER_EVENT"
            ),
            recipient_id=recipient_id,
            field_class=field_class,
        )
    if register_entry is None:
        return InboundClassificationResult(
            success=False,
            failure_code=F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET,
            sub_tag=SUB_TAG_FIRST_OCCURRENCE_UNCLASSIFIED,
            detail=(
                f"no classification register entry for "
                f"(recipient_id={recipient_id!r}, field_class={field_class!r}); "
                "operator must classify before operational-data write"
            ),
            recipient_id=recipient_id,
            field_class=field_class,
        )
    status = register_entry.get("classification_status")
    if status == "DEFAULT_CONFIDENTIAL_PENDING_REVIEW":
        return InboundClassificationResult(
            success=False,
            failure_code=F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET,
            sub_tag=SUB_TAG_DEFAULT_CONFIDENTIAL_PENDING_REVIEW,
            detail=(
                f"classification deferred for "
                f"(recipient_id={recipient_id!r}, field_class={field_class!r})"
            ),
            recipient_id=recipient_id,
            field_class=field_class,
        )
    if status != "OPERATOR_CLASSIFIED":
        return InboundClassificationResult(
            success=False,
            failure_code=F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET,
            sub_tag=SUB_TAG_FIRST_OCCURRENCE_UNCLASSIFIED,
            detail=(
                f"unrecognized classification_status={status!r} for "
                f"(recipient_id={recipient_id!r}, field_class={field_class!r})"
            ),
            recipient_id=recipient_id,
            field_class=field_class,
        )
    classification = register_entry.get("classification")
    if (
        not isinstance(classification, str)
        or classification not in PERMITTED_CLASSIFICATIONS
    ):
        return InboundClassificationResult(
            success=False,
            failure_code=F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET,
            sub_tag=SUB_TAG_FIRST_OCCURRENCE_UNCLASSIFIED,
            detail=(
                f"classification value {classification!r} not in permitted "
                f"set {sorted(PERMITTED_CLASSIFICATIONS)}"
            ),
            recipient_id=recipient_id,
            field_class=field_class,
        )
    return InboundClassificationResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail=(
            f"classification OPERATOR_CLASSIFIED for "
            f"(recipient_id={recipient_id!r}, field_class={field_class!r}); "
            f"classification={classification!r}"
        ),
        recipient_id=recipient_id,
        field_class=field_class,
    )


__all__ = [
    "F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET",
    "InboundClassificationResult",
    "PERMITTED_CLASSIFICATIONS",
    "PERMITTED_STATUSES",
    "SUB_TAG_CLASSIFICATION_REGISTER_TAMPERED",
    "SUB_TAG_DEFAULT_CONFIDENTIAL_PENDING_REVIEW",
    "SUB_TAG_FIRST_OCCURRENCE_UNCLASSIFIED",
    "check_inbound_classification_unset",
]
