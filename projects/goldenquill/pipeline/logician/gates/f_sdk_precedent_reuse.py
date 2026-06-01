"""F-SDK-PRECEDENT-REUSE (F-AMDT-04) — PRE-gate.

Fires as a PRE-gate on any amendment whose frontmatter carries
``adopts_agent_sdk: True``. Prevents a single prior seat's SDK-adoption
audit evidence from being re-used as blanket precedent for a DIFFERENT
seat adopting the Agent SDK. Each seat must present its own distinct
audit evidence.

Closes EN-001 RT-NEW-06: the Scribe Phase-0 spike audit is specific to
Scribe's threat model, integration surface, and rollback plan; Scout /
Editor / Judge each need their own per-seat audit round before
promoting an SDK-adoption amendment.

**Implementation.** The gate walks ``lock_history.v1.jsonl`` via the
injected ``LockHistoryReaderCallable`` and looks for any prior row
where ``adopts_agent_sdk == True`` AND ``seat != current_seat`` AND
``audit_evidence_path`` exactly matches the current amendment's
``audit_evidence_path``. Any such match → DENY ``F-AMDT-04`` with
``F-AMDT-04-REUSE`` event.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-4 delta rows for F-AMDT-04.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.gates._protocols import LockHistoryReaderCallable


F_AMDT_04: Final[str] = "F-AMDT-04"
F_AMDT_04_REUSE: Final[str] = "F-AMDT-04-REUSE"
F_AMDT_04_AMBIGUOUS: Final[str] = "F-AMDT-04-AMBIGUOUS"
F_AMDT_04_READER_FAIL: Final[str] = "F-AMDT-04-READER-FAIL"

EVENT_REUSE: Final[str] = "F-AMDT-04-REUSE"
EVENT_AMBIGUOUS: Final[str] = "F-AMDT-04-AMBIGUOUS"
EVENT_READER_FAIL: Final[str] = "F-AMDT-04-READER-FAIL"


_REASON_NO_OP_SDK_NOT_TRUE: Final[str] = "adopts_agent_sdk_not_true_noop"
_REASON_FRONTMATTER_NOT_DICT: Final[str] = "frontmatter_not_dict"
_REASON_SEAT_MISSING: Final[str] = "seat_missing"
_REASON_SEAT_NOT_STR: Final[str] = "seat_not_str"
_REASON_SEAT_EMPTY: Final[str] = "seat_empty"
_REASON_PATH_MISSING: Final[str] = "audit_evidence_path_missing"
_REASON_PATH_NOT_STR: Final[str] = "audit_evidence_path_not_str"
_REASON_PATH_EMPTY: Final[str] = "audit_evidence_path_empty"
_REASON_NO_PRIOR_ROW: Final[str] = "no_prior_sdk_row"
_REASON_NO_MATCH: Final[str] = "no_cross_seat_path_match"
_REASON_CROSS_SEAT_REUSE: Final[str] = "cross_seat_evidence_path_reuse"

_REASON_LOCK_HISTORY_RAISED: Final[str] = "lock_history_reader_raised"
_REASON_LOCK_HISTORY_NOT_LIST: Final[str] = "lock_history_return_not_list"


@dataclass(frozen=True, kw_only=True)
class SdkPrecedentReuseDetail:
    """Structured detail for F-AMDT-04 result."""

    reason_tag: str
    emitted_event: str
    current_seat: str
    current_audit_evidence_path: str
    prior_seat: str
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class SdkPrecedentReuseResult:
    success: bool
    failure_code: Optional[str]
    detail: SdkPrecedentReuseDetail


def _clip_error(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"[:500]


def _fail(
    *,
    failure_code: str,
    reason_tag: str,
    emitted_event: str = "",
    current_seat: str = "",
    current_audit_evidence_path: str = "",
    prior_seat: str = "",
    reader_error: Optional[str] = None,
) -> SdkPrecedentReuseResult:
    return SdkPrecedentReuseResult(
        success=False,
        failure_code=failure_code,
        detail=SdkPrecedentReuseDetail(
            reason_tag=reason_tag,
            emitted_event=emitted_event,
            current_seat=current_seat,
            current_audit_evidence_path=current_audit_evidence_path,
            prior_seat=prior_seat,
            reader_error=reader_error,
        ),
    )


def _ok(
    *,
    reason_tag: str,
    current_seat: str = "",
    current_audit_evidence_path: str = "",
) -> SdkPrecedentReuseResult:
    return SdkPrecedentReuseResult(
        success=True,
        failure_code=None,
        detail=SdkPrecedentReuseDetail(
            reason_tag=reason_tag,
            emitted_event="",
            current_seat=current_seat,
            current_audit_evidence_path=current_audit_evidence_path,
            prior_seat="",
            reader_error=None,
        ),
    )


def check_sdk_precedent_reuse(
    *,
    amendment_frontmatter: dict,
    lock_history_reader: LockHistoryReaderCallable,
) -> SdkPrecedentReuseResult:
    """PRE-gate F-SDK-PRECEDENT-REUSE (F-AMDT-04).

    Caller wires this into the amendment promotion hook. Returns a frozen
    result; the caller is responsible for emitting the ``emitted_event``
    (if any) to ``pipeline/metrics/session_log.jsonl``.
    """

    if not isinstance(amendment_frontmatter, dict):
        return _fail(
            failure_code=F_AMDT_04_AMBIGUOUS,
            reason_tag=_REASON_FRONTMATTER_NOT_DICT,
            emitted_event=EVENT_AMBIGUOUS,
        )

    # Strict `is True` — "true" string / 1 / truthy non-True values all
    # route to no-op (the amendment is malformed; F-AMDT-01 and friends
    # catch the malformed frontmatter elsewhere).
    if amendment_frontmatter.get("adopts_agent_sdk") is not True:
        return _ok(reason_tag=_REASON_NO_OP_SDK_NOT_TRUE)

    # Extract seat and audit_evidence_path BEFORE touching the reader.
    if "seat" not in amendment_frontmatter:
        return _fail(
            failure_code=F_AMDT_04_AMBIGUOUS,
            reason_tag=_REASON_SEAT_MISSING,
            emitted_event=EVENT_AMBIGUOUS,
        )
    current_seat = amendment_frontmatter["seat"]
    if not isinstance(current_seat, str):
        return _fail(
            failure_code=F_AMDT_04_AMBIGUOUS,
            reason_tag=_REASON_SEAT_NOT_STR,
            emitted_event=EVENT_AMBIGUOUS,
        )
    if current_seat == "":
        return _fail(
            failure_code=F_AMDT_04_AMBIGUOUS,
            reason_tag=_REASON_SEAT_EMPTY,
            emitted_event=EVENT_AMBIGUOUS,
        )

    if "audit_evidence_path" not in amendment_frontmatter:
        return _fail(
            failure_code=F_AMDT_04_AMBIGUOUS,
            reason_tag=_REASON_PATH_MISSING,
            emitted_event=EVENT_AMBIGUOUS,
            current_seat=current_seat,
        )
    current_path = amendment_frontmatter["audit_evidence_path"]
    if not isinstance(current_path, str):
        return _fail(
            failure_code=F_AMDT_04_AMBIGUOUS,
            reason_tag=_REASON_PATH_NOT_STR,
            emitted_event=EVENT_AMBIGUOUS,
            current_seat=current_seat,
        )
    if current_path == "":
        return _fail(
            failure_code=F_AMDT_04_AMBIGUOUS,
            reason_tag=_REASON_PATH_EMPTY,
            emitted_event=EVENT_AMBIGUOUS,
            current_seat=current_seat,
        )

    try:
        rows = lock_history_reader()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_04_READER_FAIL,
            reason_tag=_REASON_LOCK_HISTORY_RAISED,
            emitted_event=EVENT_READER_FAIL,
            current_seat=current_seat,
            current_audit_evidence_path=current_path,
            reader_error=f"lock_history_reader: {_clip_error(exc)}",
        )
    if not isinstance(rows, list):
        return _fail(
            failure_code=F_AMDT_04_READER_FAIL,
            reason_tag=_REASON_LOCK_HISTORY_NOT_LIST,
            emitted_event=EVENT_READER_FAIL,
            current_seat=current_seat,
            current_audit_evidence_path=current_path,
        )

    saw_any_sdk_row = False
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("adopts_agent_sdk") is not True:
            continue
        saw_any_sdk_row = True
        prior_seat = row.get("seat")
        if not isinstance(prior_seat, str) or prior_seat == "":
            continue
        if prior_seat == current_seat:
            # Same seat re-locking with a new (or same) evidence path is
            # not cross-seat reuse. Skip.
            continue
        prior_path = row.get("audit_evidence_path")
        if not isinstance(prior_path, str) or prior_path == "":
            continue
        if prior_path == current_path:
            # Cross-seat reuse: DIFFERENT seat's prior row shares the
            # same audit_evidence_path. DENY.
            return _fail(
                failure_code=F_AMDT_04,
                reason_tag=_REASON_CROSS_SEAT_REUSE,
                emitted_event=EVENT_REUSE,
                current_seat=current_seat,
                current_audit_evidence_path=current_path,
                prior_seat=prior_seat,
            )

    if not saw_any_sdk_row:
        return _ok(
            reason_tag=_REASON_NO_PRIOR_ROW,
            current_seat=current_seat,
            current_audit_evidence_path=current_path,
        )
    return _ok(
        reason_tag=_REASON_NO_MATCH,
        current_seat=current_seat,
        current_audit_evidence_path=current_path,
    )
