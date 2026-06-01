"""F-INTAKE-TELEMETRY-LEAK — Intake POST-tool-call + PRE-CLI gate (M1 §8.4).

CF-RT-07 closure.  Intake operates on Confidential per-org content;
Logfire telemetry would emit ``source_quote`` strings into a remote
observability endpoint.  The gate fires fail-closed when:

* ``LOGFIRE_ENABLED`` is not ``"0"`` at Intake CLI entry (PRE-CLI), OR
* a Logfire event was emitted during a tagged Intake tool-call AND
  the event includes a ``source_quote`` field OR a field tagged
  ``confidential`` per v7.0.7 (POST-tool-call).

Severity: LOW (advisory; logged at MEDIUM if recurring; HARD-BLOCK
at HIGH if endpoint is non-local).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence

from pipeline.cli.tilth_intake import (
    LOGFIRE_DISABLED_ENV,
    LOGFIRE_DISABLED_VALUE,
)


F_INTAKE_TELEMETRY_LEAK: Final[str] = "F-INTAKE-TELEMETRY-LEAK"

CONFIDENTIAL_FIELD_NAMES: Final[frozenset[str]] = frozenset({
    "source_quote",
})


@dataclass(frozen=True, kw_only=True)
class IntakeTelemetryLeakResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    severity: str = "LOW"


def _event_is_local_only(event: Mapping[str, Any]) -> bool:
    """Heuristic — True iff the Logfire event endpoint is local.

    The event row is expected to carry an ``endpoint`` field per the
    standard Logfire event shape; when absent / non-local, the gate
    escalates severity to HIGH per the §8.4 schedule.
    """
    endpoint = event.get("endpoint")
    if not isinstance(endpoint, str):
        return False
    cleaned = endpoint.strip().lower()
    if cleaned in {"", "local", "stdout", "stderr"}:
        return True
    if cleaned.startswith("file://"):
        return True
    if cleaned.startswith("unix://"):
        return True
    if "127.0.0.1" in cleaned or "localhost" in cleaned:
        return True
    return False


def _event_carries_confidential(event: Mapping[str, Any]) -> Optional[str]:
    """Returns the offending field name, or None if clean."""
    for field in CONFIDENTIAL_FIELD_NAMES:
        if field in event:
            return field
    classifications = event.get("classifications")
    if isinstance(classifications, Mapping):
        for field, klass in classifications.items():
            if isinstance(klass, str) and klass.strip().lower() == "confidential":
                return str(field)
    fields = event.get("fields")
    if isinstance(fields, Sequence):
        for f in fields:
            if isinstance(f, Mapping):
                if f.get("classification") == "confidential":
                    return str(f.get("name") or "<unnamed>")
    return None


def check_intake_telemetry_leak(
    *,
    cli_entry: bool = False,
    intake_tool_call_events: Sequence[Mapping[str, Any]] = (),
) -> IntakeTelemetryLeakResult:
    """POST-tool-call + PRE-CLI gate: detect Logfire leaks during Intake.

    Parameters
    ----------
    cli_entry
        True when fired at Intake CLI entry (the env-var leg).  False
        when fired post-tool-call (the events leg).
    intake_tool_call_events
        Logfire event rows captured during the Intake tool-call.  When
        the env-var leg fires, this should be empty; when both legs
        fire in one invocation, both are checked.
    """
    if cli_entry:
        env_value = os.environ.get(LOGFIRE_DISABLED_ENV)
        if env_value != LOGFIRE_DISABLED_VALUE:
            return IntakeTelemetryLeakResult(
                success=False,
                failure_code=F_INTAKE_TELEMETRY_LEAK,
                detail=(
                    f"{LOGFIRE_DISABLED_ENV}={env_value!r} at Intake CLI "
                    f"entry; expected {LOGFIRE_DISABLED_VALUE!r} "
                    "(LOW severity advisory; logged HIGH if endpoint non-local)"
                ),
                severity="LOW",
            )

    for event in intake_tool_call_events:
        if not isinstance(event, Mapping):
            continue
        offending = _event_carries_confidential(event)
        if offending is not None:
            severity = "LOW" if _event_is_local_only(event) else "HIGH"
            return IntakeTelemetryLeakResult(
                success=False,
                failure_code=F_INTAKE_TELEMETRY_LEAK,
                detail=(
                    f"Logfire event during Intake carries confidential "
                    f"field {offending!r}; severity={severity} based "
                    f"on endpoint locality"
                ),
                severity=severity,
            )

    return IntakeTelemetryLeakResult(
        success=True,
        failure_code=None,
        detail=(
            f"Intake telemetry clean: env={LOGFIRE_DISABLED_ENV}=0; "
            f"{len(intake_tool_call_events)} event(s) carry no "
            "confidential fields"
        ),
    )


__all__ = [
    "CONFIDENTIAL_FIELD_NAMES",
    "F_INTAKE_TELEMETRY_LEAK",
    "IntakeTelemetryLeakResult",
    "check_intake_telemetry_leak",
]
