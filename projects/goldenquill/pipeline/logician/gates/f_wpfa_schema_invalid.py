"""F-WPFA-SCHEMA-INVALID — PRE-write + POST-read gate. [§5.1.WPFA.11]

Trigger: schema validation failure (any of the 17 CycleReceipt invariants
in §17.3.4) at write OR at decode round-trip.

Sub-tags: ``.numeric_field_float``, ``.classification_register_version_invalid``,
``.dimensions_active_invalid``, ``.per_model_aggregate_mismatch``,
``.delta_arithmetic_mismatch``, ``.semver_version_invalid``,
``.schema_drift_advisory``.

The CycleReceipt ``__post_init__`` is the canonical invariant authority;
this gate wraps it and surfaces a structured GateOutcome with sub-tag
identification by inspecting the exception message.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_WPFA_SCHEMA_INVALID: Final[str] = "F-WPFA-SCHEMA-INVALID"


@dataclass(frozen=True, kw_only=True)
class SchemaInvalidResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


# Map error message fragments to sub-tags. Ordered most-specific first so
# overlapping fragments resolve deterministically.
_MESSAGE_SUBTAGS: Final[tuple[tuple[str, str], ...]] = (
    ("delta_arithmetic_mismatch", "delta_arithmetic_mismatch"),
    ("per_model_aggregate_mismatch", "per_model_aggregate_mismatch"),
    ("dimensions_active", "dimensions_active_invalid"),
    ("classification_register_version", "classification_register_version_invalid"),
    ("schema_version must match semver", "semver_version_invalid"),
    ("must decode as int", "numeric_field_float"),
    ("A12 mandate", "numeric_field_float"),
)


def check_f_wpfa_schema_invalid(
    *,
    error_message: Optional[str] = None,
    error_type: Optional[type[Exception]] = None,
) -> SchemaInvalidResult:
    """POST-read: classify a CycleReceipt schema invariant failure.

    Callers invoke after catching a ValueError raised by
    ``CycleReceipt.__post_init__`` or its decoder helpers. Pass the
    exception's args[0] as ``error_message`` and the exception class
    as ``error_type``; this gate returns a structured result with the
    appropriate sub-tag.

    If ``error_message`` is None the gate returns success — callers are
    expected to invoke this gate only on the failure path.
    """
    if error_message is None:
        return SchemaInvalidResult(
            success=True,
            failure_code=None,
            detail="no error to classify",
        )
    if not isinstance(error_message, str):
        return SchemaInvalidResult(
            success=False,
            failure_code=F_WPFA_SCHEMA_INVALID,
            detail=f"non-string error_message: {error_message!r}",
        )
    msg_lower = error_message.lower()
    sub_tag: Optional[str] = None
    for fragment, mapped in _MESSAGE_SUBTAGS:
        if fragment.lower() in msg_lower:
            sub_tag = mapped
            break
    if sub_tag is None:
        # Unclassified — default to schema_drift_advisory at v0.1 (tolerant
        # reader path); upgrade in follow-on minor amendment if needed.
        sub_tag = "schema_drift_advisory"
    return SchemaInvalidResult(
        success=False,
        failure_code=F_WPFA_SCHEMA_INVALID,
        sub_tag=sub_tag,
        detail=(
            f"CycleReceipt schema invariant violated [{error_type.__name__ if error_type else 'Exception'}]: "
            f"{error_message}"
        ),
    )


__all__ = [
    "F_WPFA_SCHEMA_INVALID",
    "SchemaInvalidResult",
    "check_f_wpfa_schema_invalid",
]
