"""Intake CLI entry point with Logfire bootstrap shim (v7.0.4-M1 §8.4 / §8.4.1).

CF-RT-07 + RT-11 closure.  The Intake subprocess MUST set
``LOGFIRE_ENABLED=0`` AND inject a stub into ``sys.modules['logfire']``
BEFORE any other import so that:

* Direct ``import logfire`` calls resolve to the stub (RT-11 leg 1).
* Transitive imports (a shared util module imported by Intake which in
  turn imports Logfire) also resolve to the stub (RT-11 leg 2).
* Subprocesses spawned by Intake inherit the env var AND must run
  the same bootstrap before doing actual work (RT-11 leg 3).

The stub raises on any attribute access so the failure is loud — no
silent partial telemetry, no late-binding leak.

Loading discipline:

* This module is the canonical Intake CLI entry — invoked as
  ``python -m pipeline.cli.tilth_intake`` or via
  ``tilth intake`` shell wrapper.
* The bootstrap MUST execute at module import time, BEFORE any
  ``from pipeline.orchestrator.seats.intake import ...`` lands.
* ``F-INTAKE-LOGFIRE-STUB-MISSING`` fires if a Logician PRE-gate
  observes ``sys.modules['logfire']`` is not the stub at Intake CLI
  entry or at any subprocess entry.
"""

from __future__ import annotations

import os
import sys
import types
from typing import Any, Final


LOGFIRE_DISABLED_ENV: Final[str] = "LOGFIRE_ENABLED"
LOGFIRE_DISABLED_VALUE: Final[str] = "0"
LOGFIRE_STUB_NAME: Final[str] = "logfire"
LOGFIRE_STUB_MARKER: Final[str] = "_tilth_logfire_disabled_stub"

F_INTAKE_LOGFIRE_STUB_MISSING: Final[str] = "F-INTAKE-LOGFIRE-STUB-MISSING"


class _LogfireDisabledStub(types.ModuleType):
    """Stub module that raises on any attribute access.

    Per §8.4.1, the stub closes the transitive-import path: any
    transitive ``import logfire`` resolves to this stub instead of the
    real package.  Any access (read or write) raises ``RuntimeError``
    so a misbehaving import path fails loud.
    """

    def __init__(self) -> None:
        super().__init__(LOGFIRE_STUB_NAME)
        # Mark the stub so :func:`is_logfire_stub_active` can identify
        # it without relying on isinstance (which fails across module
        # reloads or vendoring).
        super().__setattr__(LOGFIRE_STUB_MARKER, True)

    def __getattr__(self, name: str) -> Any:  # noqa: D401 — module hook
        if name == LOGFIRE_STUB_MARKER:
            return True
        raise RuntimeError(
            f"Logfire access denied during Intake "
            f"({LOGFIRE_DISABLED_ENV}={LOGFIRE_DISABLED_VALUE}). "
            f"Attempted access: logfire.{name}. "
            f"Per {F_INTAKE_LOGFIRE_STUB_MISSING} §8.4.1."
        )

    def __setattr__(self, name: str, value: Any) -> None:
        if name == LOGFIRE_STUB_MARKER:
            super().__setattr__(name, value)
            return
        raise RuntimeError(
            f"Logfire mutation denied during Intake "
            f"(attempted set logfire.{name})."
        )


def install_logfire_disabled_stub() -> None:
    """Install the stub into :data:`sys.modules` (idempotent).

    Sets the env var as a side-effect so that any code that consults
    ``os.environ`` instead of ``sys.modules`` also fails-closed.
    """
    os.environ[LOGFIRE_DISABLED_ENV] = LOGFIRE_DISABLED_VALUE
    existing = sys.modules.get(LOGFIRE_STUB_NAME)
    if existing is not None and getattr(existing, LOGFIRE_STUB_MARKER, False):
        return  # already installed
    sys.modules[LOGFIRE_STUB_NAME] = _LogfireDisabledStub()


def is_logfire_stub_active() -> bool:
    """Returns True iff the stub is the active ``sys.modules['logfire']``.

    Production callers (Logician PRE-Intake-CLI gate) check this
    invariant before allowing any Intake-tagged tool call to proceed.
    """
    if os.environ.get(LOGFIRE_DISABLED_ENV) != LOGFIRE_DISABLED_VALUE:
        return False
    mod = sys.modules.get(LOGFIRE_STUB_NAME)
    if mod is None:
        return False
    return bool(getattr(mod, LOGFIRE_STUB_MARKER, False))


def subprocess_bootstrap_source() -> str:
    """Return the ``-c`` bootstrap source for Intake-spawned subprocesses.

    Subprocess discipline per §8.4.1 — the bootstrap text injects the
    same stub into the subprocess's ``sys.modules`` BEFORE any other
    import.  Callers do:

    .. code-block:: python

        import subprocess, sys
        from pipeline.cli.tilth_intake import subprocess_bootstrap_source
        subprocess.run([
            sys.executable, "-c",
            subprocess_bootstrap_source() + "; import target.module; target.module.main()",
        ], env={**os.environ, LOGFIRE_DISABLED_ENV: LOGFIRE_DISABLED_VALUE})
    """
    # Standalone — no imports from pipeline so the subprocess doesn't
    # accidentally drag the rest of the package up before the stub
    # lands.
    return (
        "import sys, os, types; "
        f"os.environ['{LOGFIRE_DISABLED_ENV}']='{LOGFIRE_DISABLED_VALUE}'; "
        "class _S(types.ModuleType):\n"
        "  def __init__(self):\n"
        "    super().__init__('logfire')\n"
        f"    super().__setattr__('{LOGFIRE_STUB_MARKER}', True)\n"
        "  def __getattr__(self, name):\n"
        f"    if name == '{LOGFIRE_STUB_MARKER}': return True\n"
        "    raise RuntimeError('logfire denied (subprocess bootstrap)')\n"
        "  def __setattr__(self, name, value):\n"
        f"    if name == '{LOGFIRE_STUB_MARKER}':\n"
        "      super().__setattr__(name, value); return\n"
        "    raise RuntimeError('logfire denied (subprocess bootstrap)')\n"
        "sys.modules['logfire'] = _S()"
    )


# Bootstrap fires at module import — any caller that does
# ``import pipeline.cli.tilth_intake`` lands the stub before going on
# to import the rest of the Intake stack.  Callers that do
# ``python -m pipeline.cli.tilth_intake`` get the same effect via the
# ``__main__`` block at the bottom of the file.
install_logfire_disabled_stub()


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - thin entry
    """Intake CLI entry — re-binds bootstrap then dispatches.

    The bootstrap is already installed by import (above).  The CLI
    proper lives in :mod:`pipeline.orchestrator.seats.intake` (out of
    M1 scope).  This function is here to host the ``__main__`` entry
    invariant.
    """
    install_logfire_disabled_stub()
    # The actual Intake dispatch wires up at v0.1 Beta time.  For now,
    # provide a clean "not-implemented" exit code so the CLI is
    # importable and the Logfire stub installable from tests.
    print(
        "tilth_intake: bootstrap installed; "
        "pipeline.orchestrator.seats.intake CLI dispatch not yet wired",
        file=sys.stderr,
    )
    return 0


__all__ = [
    "F_INTAKE_LOGFIRE_STUB_MISSING",
    "LOGFIRE_DISABLED_ENV",
    "LOGFIRE_DISABLED_VALUE",
    "LOGFIRE_STUB_MARKER",
    "LOGFIRE_STUB_NAME",
    "install_logfire_disabled_stub",
    "is_logfire_stub_active",
    "subprocess_bootstrap_source",
    "main",
]


if __name__ == "__main__":  # pragma: no cover - thin entry
    raise SystemExit(main(sys.argv[1:]))
