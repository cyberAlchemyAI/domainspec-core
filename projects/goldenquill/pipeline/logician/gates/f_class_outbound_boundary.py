"""F-CLASS-* outbound-boundary gates (PRE/POST per-call).

Per architecture v7.0.7 §1 (routing rule + opaque slot discipline) +
§4.1 (high-stakes flag classification) + §5 (fail-closed defaults) +
§5.1 (architectural-primitive table — LOCKED 2026-05-10 row 180).

Four sub-codes share the same payload-scanner injection surface and
fire at the cloud-routing outbound boundary, so they are housed
together per the v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent.

Sub-codes:

* ``F-CLASS-SLOT-ID-NON-OPAQUE`` — PRE per-call. Cloud-routed prompt
  contains a slot identifier that is NOT of form ``[SLOT_<numeric_id>]``
  (e.g., ``[SLOT_ANNUAL_REVENUE]``). The opaque-ID requirement
  eliminates the (a) plausible-literal-hallucination + (b) field-name
  inference leak surfaces per §1.

* ``F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL`` — POST per-call. Cloud-routed
  payload bytes contain a literal value tagged ``confidential`` or
  ``operator_flagged`` per the per-call classification register lookup.
  P0 fail-closed; pipeline halts; admin-risk ledger HIGH severity.

* ``F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`` — POST per-call.
  Cloud-routed response payload contains a literal value at a position
  registered as a slot template (cloud Scribe synthesized a value into
  a slot position before slot-fill ran). The presence of a literal in
  any registered slot position is the structural-sovereignty bypass
  per §1.

* ``F-CLASS-HIGH-STAKES-FLAG-LEAK`` — POST per-call. Cloud-routed
  payload contains the literal string ``high_stakes`` OR a tagged value
  referencing a per-grant high-stakes flag from the register. Per §4.1
  the flag itself is sensitive operational metadata.

Bypass: SLOT-ID-NON-OPAQUE has NO M13 (structural). Other three are
fail-closed P0; M13 audited admin-risk-HIGH bypass per §5.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Final, Mapping, Optional, Sequence


F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL"
)
F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED"
)
F_CLASS_SLOT_ID_NON_OPAQUE: Final[str] = "F-CLASS-SLOT-ID-NON-OPAQUE"
F_CLASS_HIGH_STAKES_FLAG_LEAK: Final[str] = "F-CLASS-HIGH-STAKES-FLAG-LEAK"

# Opaque slot identifier shape per v7.0.7 §1: `[SLOT_<numeric_id>]` with
# ASCII-digits-only payload. Anything else (e.g., `[SLOT_ANNUAL_REVENUE]`,
# `[SLOT_001A]`, `[SLOT_]`, `[SLOT_१]` Devanagari digit) fail-closes.
#
# RT-12 closure (Cycle 1, 2026-05-10): the opaque-ID payload regex uses
# `re.ASCII` so Python's default Unicode-aware `\d` (which matches
# Devanagari `१`, Arabic-Indic `١`, etc.) does NOT silently admit a
# Unicode-confusable digit as a "valid" opaque slot identifier.
# Downstream code that splits on the captured group expects ASCII digits;
# letting a Unicode digit through would cause an off-substrate slot
# lookup that bypasses the structural-sovereignty contract.
_OPAQUE_SLOT_RE: Final[re.Pattern[str]] = re.compile(
    r"\[SLOT_([0-9]+)\]", flags=re.ASCII
)
_ANY_SLOT_LIKE_RE: Final[re.Pattern[str]] = re.compile(r"\[SLOT_([^\]]*)\]")

# High-stakes leak detection — literal string + tagged-value variants
# per §4.1 enumerated leak surfaces.
_HIGH_STAKES_TOKENS: Final[tuple[str, ...]] = (
    "high_stakes",
    "high-stakes",
    "highstakes",
)

# Classification class names per §2 schema.
CLASS_PUBLIC: Final[str] = "public"
CLASS_SHAREABLE: Final[str] = "shareable"
CLASS_CONFIDENTIAL: Final[str] = "confidential"
CLASS_OPERATOR_FLAGGED: Final[str] = "operator_flagged"

_BLOCKING_CLASSES: Final[frozenset[str]] = frozenset({
    CLASS_CONFIDENTIAL,
    CLASS_OPERATOR_FLAGGED,
})


@dataclass(frozen=True, kw_only=True)
class ClassifiedValue:
    """A literal value plus its classification class.

    Caller (routing layer) materializes one entry per field-value the
    cloud-routed payload should NOT contain literally. The `value`
    string is the substring the gate scans for; `class_name` documents
    the classification at audit.
    """

    value: str
    class_name: str
    field_path: str = ""


@dataclass(frozen=True, kw_only=True)
class SlotPosition:
    """A registered slot position the post-fill output should still carry as opaque.

    `slot_id` is the numeric identifier (the digits inside `[SLOT_XXX]`)
    so the gate can scan for the rendered token. `surrounding_window`
    optional pre/post markers from the slot template let the gate
    detect literal-in-position synthesis where the cloud synthesized a
    plausible value at the slot anchor instead of preserving the
    opaque token.
    """

    slot_id: str
    pre_marker: str = ""
    post_marker: str = ""


@dataclass(frozen=True, kw_only=True)
class OutboundBoundaryResult:
    """Result of one F-CLASS outbound-boundary sub-check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    matched_count: int = 0
    matched_samples: tuple[str, ...] = field(default_factory=tuple)


def check_class_slot_id_non_opaque(
    *,
    cloud_routed_prompt: str,
) -> OutboundBoundaryResult:
    """PRE per-call: every slot identifier in the prompt must be opaque.

    Scans the prompt for slot-like tokens (anything matching
    ``[SLOT_<payload>]``) and fail-closes if any payload is not
    purely-numeric. Per §1 the opaque-ID requirement is structural —
    semantic slot names like ``[SLOT_ANNUAL_REVENUE]`` cannot reach a
    cloud-routed seat.

    Returns
    -------
    OutboundBoundaryResult. PASS only when every slot-like token in the
    prompt is of the form ``[SLOT_<digits>]``.
    """
    if not isinstance(cloud_routed_prompt, str):
        return OutboundBoundaryResult(
            success=False,
            failure_code=F_CLASS_SLOT_ID_NON_OPAQUE,
            detail=(
                f"cloud_routed_prompt is not a string "
                f"(got {type(cloud_routed_prompt).__name__})"
            ),
        )

    bad: list[str] = []
    for match in _ANY_SLOT_LIKE_RE.finditer(cloud_routed_prompt):
        payload = match.group(1)
        if not payload or not (payload.isascii() and payload.isdigit()):
            bad.append(match.group(0))

    if bad:
        return OutboundBoundaryResult(
            success=False,
            failure_code=F_CLASS_SLOT_ID_NON_OPAQUE,
            detail=(
                f"non-opaque slot identifier(s) found in cloud-routed prompt: "
                f"{', '.join(bad[:5])}"
                + (f" (+{len(bad) - 5} more)" if len(bad) > 5 else "")
                + " — fail-closed per §1; semantic slot names are forbidden "
                "(no M13)"
            ),
            matched_count=len(bad),
            matched_samples=tuple(bad[:5]),
        )
    return OutboundBoundaryResult(
        success=True,
        failure_code=None,
        detail=(
            "all slot identifiers in cloud-routed prompt are opaque "
            "[SLOT_<digits>]"
        ),
    )


def check_class_cloud_received_confidential(
    *,
    cloud_routed_payload: str,
    classified_values: Sequence[ClassifiedValue],
) -> OutboundBoundaryResult:
    """POST per-call: payload must not contain confidential/operator_flagged literals.

    Scans the payload for any literal value whose registered class is
    ``confidential`` or ``operator_flagged``. Both class names route
    identically per §1. P0 fail-closed.

    Parameters
    ----------
    cloud_routed_payload
        Raw text of the cloud-routed request (or response on POST).
    classified_values
        Sequence of (value, class_name, field_path) triples. The
        routing layer assembles this set from the classification
        register before each cloud-routed call. Empty values are
        silently skipped (no false positive on 0-length needle).

    Returns
    -------
    OutboundBoundaryResult. PASS only when no confidential or
    operator_flagged literal substring appears in the payload.
    """
    if not isinstance(cloud_routed_payload, str):
        return OutboundBoundaryResult(
            success=False,
            failure_code=F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
            detail=(
                f"cloud_routed_payload is not a string "
                f"(got {type(cloud_routed_payload).__name__})"
            ),
        )

    matches: list[str] = []
    for entry in classified_values:
        if entry.class_name not in _BLOCKING_CLASSES:
            continue
        needle = entry.value
        if not isinstance(needle, str) or not needle:
            continue
        if needle in cloud_routed_payload:
            tag = (
                f"{entry.class_name}:{entry.field_path}"
                if entry.field_path
                else entry.class_name
            )
            matches.append(tag)

    if matches:
        return OutboundBoundaryResult(
            success=False,
            failure_code=F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
            detail=(
                "cloud-routed payload contains literal value(s) tagged "
                f"confidential/operator_flagged: {', '.join(matches[:5])}"
                + (f" (+{len(matches) - 5} more)" if len(matches) > 5 else "")
                + " — P0 fail-closed; admin-risk HIGH; pipeline halts"
            ),
            matched_count=len(matches),
            matched_samples=tuple(matches[:5]),
        )
    return OutboundBoundaryResult(
        success=True,
        failure_code=None,
        detail=(
            f"cloud-routed payload contains no confidential/operator_flagged "
            f"literal (scanned {len(classified_values)} classified values)"
        ),
    )


def check_class_cloud_received_opaque_slot_filled(
    *,
    cloud_routed_payload: str,
    slot_positions: Sequence[SlotPosition],
) -> OutboundBoundaryResult:
    """POST per-call: registered slot positions must remain opaque post-cloud.

    For each registered slot, the gate verifies that the rendered token
    ``[SLOT_<slot_id>]`` is still present in the payload at the
    expected anchor (delimited by ``pre_marker`` / ``post_marker`` when
    those are non-empty). When the cloud Scribe synthesized a literal
    value into the slot position instead of preserving the opaque
    token, the slot-fill bypass surfaces here.

    Parameters
    ----------
    cloud_routed_payload
        Cloud-routed response text the slot-fill agent will read.
    slot_positions
        Sequence of registered slot positions; the routing layer
        assembles one per slot the prompt template defined.

    Returns
    -------
    OutboundBoundaryResult. PASS only when every registered slot's
    opaque token is present at its expected anchor.
    """
    if not isinstance(cloud_routed_payload, str):
        return OutboundBoundaryResult(
            success=False,
            failure_code=F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED,
            detail=(
                f"cloud_routed_payload is not a string "
                f"(got {type(cloud_routed_payload).__name__})"
            ),
        )

    missing: list[str] = []
    for slot in slot_positions:
        if not slot.slot_id or not slot.slot_id.isdigit():
            # Slot ID must be opaque digits — but that's covered by
            # F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate; here we just refuse
            # to check non-conforming slots and fail-closed.
            missing.append(f"<malformed slot_id={slot.slot_id!r}>")
            continue
        opaque_token = f"[SLOT_{slot.slot_id}]"
        if slot.pre_marker or slot.post_marker:
            anchor = f"{slot.pre_marker}{opaque_token}{slot.post_marker}"
            if anchor not in cloud_routed_payload:
                missing.append(slot.slot_id)
        else:
            if opaque_token not in cloud_routed_payload:
                missing.append(slot.slot_id)

    if missing:
        return OutboundBoundaryResult(
            success=False,
            failure_code=F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED,
            detail=(
                "cloud-routed payload synthesized literal(s) at registered "
                f"slot position(s): {', '.join(missing[:5])}"
                + (f" (+{len(missing) - 5} more)" if len(missing) > 5 else "")
                + " — slot-fill bypass; cloud-Scribe synthesized into slot "
                "anchor instead of preserving opaque token"
            ),
            matched_count=len(missing),
            matched_samples=tuple(missing[:5]),
        )
    return OutboundBoundaryResult(
        success=True,
        failure_code=None,
        detail=(
            f"all {len(slot_positions)} registered slot positions remain "
            "opaque in cloud-routed payload"
        ),
    )


def check_class_high_stakes_flag_leak(
    *,
    cloud_routed_payload: str,
    high_stakes_flag_values: Sequence[str] = (),
) -> OutboundBoundaryResult:
    """POST per-call: payload must not leak high-stakes operational metadata.

    Scans for the literal ``high_stakes`` token in any case variant per
    §4.1. Optional `high_stakes_flag_values` covers tagged values
    referencing the per-grant register flag (e.g., a stringified
    grant_id appearing in a "high_stakes_grants" list).

    Returns
    -------
    OutboundBoundaryResult. PASS only when none of the high-stakes
    leak tokens appear in the payload.
    """
    if not isinstance(cloud_routed_payload, str):
        return OutboundBoundaryResult(
            success=False,
            failure_code=F_CLASS_HIGH_STAKES_FLAG_LEAK,
            detail=(
                f"cloud_routed_payload is not a string "
                f"(got {type(cloud_routed_payload).__name__})"
            ),
        )

    payload_lower = cloud_routed_payload.lower()
    matches: list[str] = []
    for tok in _HIGH_STAKES_TOKENS:
        if tok in payload_lower:
            matches.append(tok)
    for val in high_stakes_flag_values:
        if isinstance(val, str) and val and val in cloud_routed_payload:
            matches.append(val)

    if matches:
        return OutboundBoundaryResult(
            success=False,
            failure_code=F_CLASS_HIGH_STAKES_FLAG_LEAK,
            detail=(
                "cloud-routed payload contains high-stakes leak token(s): "
                f"{', '.join(matches[:5])}"
                + (f" (+{len(matches) - 5} more)" if len(matches) > 5 else "")
                + " — per §4.1 the high-stakes flag is confidential operational "
                "metadata; fail-closed"
            ),
            matched_count=len(matches),
            matched_samples=tuple(matches[:5]),
        )
    return OutboundBoundaryResult(
        success=True,
        failure_code=None,
        detail="no high-stakes leak tokens found in cloud-routed payload",
    )


__all__ = [
    "CLASS_CONFIDENTIAL",
    "CLASS_OPERATOR_FLAGGED",
    "CLASS_PUBLIC",
    "CLASS_SHAREABLE",
    "ClassifiedValue",
    "F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL",
    "F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED",
    "F_CLASS_HIGH_STAKES_FLAG_LEAK",
    "F_CLASS_SLOT_ID_NON_OPAQUE",
    "OutboundBoundaryResult",
    "SlotPosition",
    "check_class_cloud_received_confidential",
    "check_class_cloud_received_opaque_slot_filled",
    "check_class_high_stakes_flag_leak",
    "check_class_slot_id_non_opaque",
]
