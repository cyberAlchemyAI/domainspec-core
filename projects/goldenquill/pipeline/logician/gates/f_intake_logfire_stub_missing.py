"""F-INTAKE-LOGFIRE-STUB-MISSING — Intake PRE-CLI + PRE-subprocess (M1 §8.4.1).

RT-11 Cycle-2 closure.  The Intake CLI installs a Logfire stub into
``sys.modules['logfire']`` BEFORE any other import to close
transitive-import bypass paths.  The gate fires fail-closed when the
stub is not the active logfire module entry — catches:

* CLI entry without bootstrap (someone imported a sibling module
  before invoking the CLI bootstrap).
* Subprocess entry without bootstrap (subprocess wasn't launched via
  the bootstrap-source bridge).

Wraps :func:`pipeline.cli.tilth_intake.is_logfire_stub_active`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.cli.tilth_intake import (
    F_INTAKE_LOGFIRE_STUB_MISSING,
    is_logfire_stub_active,
)


@dataclass(frozen=True, kw_only=True)
class IntakeLogfireStubResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    is_subprocess: bool = False


def check_intake_logfire_stub_missing(
    *,
    is_subprocess: bool = False,
) -> IntakeLogfireStubResult:
    """PRE-CLI + PRE-subprocess gate: stub must be installed.

    Parameters
    ----------
    is_subprocess
        True when fired at subprocess entry (caller is one of the
        spawn helpers in :mod:`pipeline.cli.tilth_intake`).  False at
        CLI entry.
    """
    if is_logfire_stub_active():
        return IntakeLogfireStubResult(
            success=True,
            failure_code=None,
            detail=(
                "Logfire stub is the active sys.modules['logfire'] entry"
                + (" (subprocess)" if is_subprocess else " (CLI entry)")
            ),
            is_subprocess=is_subprocess,
        )
    return IntakeLogfireStubResult(
        success=False,
        failure_code=F_INTAKE_LOGFIRE_STUB_MISSING,
        detail=(
            "Logfire stub NOT active — Intake bootstrap missing or "
            "overridden"
            + (" at subprocess entry" if is_subprocess else " at CLI entry")
            + " (call install_logfire_disabled_stub() first)"
        ),
        is_subprocess=is_subprocess,
    )


__all__ = [
    "F_INTAKE_LOGFIRE_STUB_MISSING",
    "IntakeLogfireStubResult",
    "check_intake_logfire_stub_missing",
]
