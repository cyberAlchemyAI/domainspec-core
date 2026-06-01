"""F-VERDICT-BLOCKING-MISSING (F-AMDT-02) — POST-gate on verdict ingest.

Every reviewer verdict (Editor, Judge, Red Team) ingested into the pipeline
must carry a top-level ``blocking`` key whose value is strictly a Python
``bool``. Without this gate, a reviewer that forgot the field — or returned
``"true"`` / ``1`` / ``None`` — would pass silently and be promoted as a
structurally valid verdict. The gate makes the blocking / non-blocking
distinction mechanically enforced, not convention-dependent.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 delta row for F-AMDT-02 (Wave 1, no external deps).

Semantics (spec card v1, 2026-04-20):
  * PASS iff ``verdict_json`` is a ``dict`` AND ``"blocking"`` key is
    present AT THE TOP LEVEL AND ``isinstance(verdict_json["blocking"], bool)``.
  * FAIL (``F-AMDT-02``) otherwise — verdict is DENIED, caller halts at
    verdict step, operator / seat re-submits.

The gate is pure-Python, zero LLM tokens, fail-closed, and has no injected
dependencies: it operates on the in-memory parsed dict that upstream JSON
parsing produced.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Failure-code constant (blueprint §6 v2.2 delta)
# ---------------------------------------------------------------------------


F_AMDT_02: str = "F-AMDT-02"


_DETAIL_KEY_ABSENT: str = "blocking_key_absent"
_DETAIL_WRONG_TYPE: str = "blocking_value_not_bool"
_DETAIL_VERDICT_NOT_DICT: str = "verdict_not_dict"


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class BlockingMissingDetail:
    """Structured failure detail for telemetry / session_log emission."""

    reason_tag: str
    observed_type: str
    observed_repr: str


@dataclass(frozen=True, kw_only=True)
class BlockingMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: Optional[BlockingMissingDetail]


# ---------------------------------------------------------------------------
# Gate predicate
# ---------------------------------------------------------------------------


def check_verdict_blocking(verdict_json: object) -> BlockingMissingResult:
    """POST-gate F-VERDICT-BLOCKING-MISSING (F-AMDT-02).

    Args:
      verdict_json: the reviewer's verdict already parsed from JSON. Upstream
        JSON parsing errors are the parser's responsibility — this gate
        validates *structure*, not syntax.

    Returns:
      BlockingMissingResult with ``success=True`` on PASS, or
      ``success=False`` + ``failure_code=F-AMDT-02`` + populated ``detail``
      on any FAIL path (not-a-dict, key-absent, wrong-type).
    """
    if not isinstance(verdict_json, dict):
        return BlockingMissingResult(
            success=False,
            failure_code=F_AMDT_02,
            detail=BlockingMissingDetail(
                reason_tag=_DETAIL_VERDICT_NOT_DICT,
                observed_type=type(verdict_json).__name__,
                observed_repr=repr(verdict_json)[:200],
            ),
        )

    if "blocking" not in verdict_json:
        return BlockingMissingResult(
            success=False,
            failure_code=F_AMDT_02,
            detail=BlockingMissingDetail(
                reason_tag=_DETAIL_KEY_ABSENT,
                observed_type="NoneType",
                observed_repr="<absent>",
            ),
        )

    value = verdict_json["blocking"]
    if not isinstance(value, bool):
        return BlockingMissingResult(
            success=False,
            failure_code=F_AMDT_02,
            detail=BlockingMissingDetail(
                reason_tag=_DETAIL_WRONG_TYPE,
                observed_type=type(value).__name__,
                observed_repr=repr(value)[:200],
            ),
        )

    return BlockingMissingResult(success=True, failure_code=None, detail=None)
