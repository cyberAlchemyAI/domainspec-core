"""pipeline/observability/logfire_bootstrap.py — process-wide Logfire bootstrap shim.

Closes deployment-runbook defect **D-RB-02** (filed 2026-05-15 in
``docs/v0_1_beta_deployment_runbook.md`` §13).

Authority
---------

- v7.0.4-M1 §8.4.1 — *Process-wide Logfire bootstrap shim* (LOCKED 2026-05-10).
- v0.1 Beta deployment runbook §1.4 + §9.1 — observability bringup.
- ADR-001 — Logfire is the canonical observability substrate frozen into
  the Golden Image at build time (no marketplace pulls at runtime).

Direction
---------

This shim is the **enablement** side of §8.4.1.  The Intake CLI uses the
*disablement* side of §8.4.1 (env-var pre-import + ``_LogfireDisabledStub``
injection into ``sys.modules['logfire']`` to refuse all telemetry during
Intake-mode tool calls per ``F-INTAKE-TELEMETRY-LEAK`` +
``F-INTAKE-LOGFIRE-STUB-MISSING``).  This module is what every other entry
point (council seats, orchestrator, CLI surface other than Intake) calls at
process start to bring Logfire up gracefully.

Contract
--------

``bootstrap_logfire()`` is:

1. **Idempotent.**  Subsequent calls in the same process return the
   snapshotted ``BootstrapResult`` without re-running configure().
2. **Honors Intake discipline.**  If ``LOGFIRE_ENABLED=0`` is set in the
   environment (per §8.4.1 Intake pre-import policy), the shim short-
   circuits to ``SKIPPED_DISABLED``.  No ``import logfire`` is attempted.
3. **Honors stub installations.**  If ``sys.modules['logfire']`` resolves
   to a §8.4.1 ``_LogfireDisabledStub`` (sentinel: ``configure`` is not a
   callable attribute), the shim short-circuits to ``SKIPPED_STUB``.
4. **Gracefully degrades on missing install.**  If ``import logfire``
   raises ``ImportError``, the shim logs a WARNING (with the runbook §1.4
   install hint) and returns ``SKIPPED_NOT_INSTALLED``.
5. **Gracefully degrades on missing credentials.**  ``logfire.configure``
   is called with ``send_to_logfire='if-token-present'``, which is
   Logfire's documented graceful-degrade mode — local span machinery
   configures successfully, upload silently no-ops when no write-token is
   found at ``~/.logfire/default.toml`` or in ``LOGFIRE_TOKEN``.  Any
   exception raised by ``configure()`` is caught, a WARNING is logged
   (with the runbook OP-01 ``logfire auth`` hint), and the shim returns
   ``SKIPPED_NO_CREDENTIALS``.
6. **No side effects beyond Logfire.**  The shim does not write to disk,
   does not spawn subprocesses, does not touch the operator's keys or
   the classification register.

What it does NOT do
-------------------

This shim does not enforce that any seat actually emits spans.  Logfire
span emission is the seat's own responsibility; the shim only ensures
``logfire.configure(...)`` has run once before any seat's first
``logfire.span(...)`` / ``logfire.info(...)`` call (in the common case
where ``LOGFIRE_ENABLED`` is unset).

The shim also does not enforce Law 3 (Org Isolation) on span content.
Field-level redaction of Confidential or operator-flagged fields per the
v7.0.7 classification register is the *callsite's* responsibility, not
the bootstrap's.  Future work: a Logfire processor middleware that
consults the classification register and drops confidential fields
before upload — that lands as a separate spec (see runbook §9.1 forward
gap).
"""

from __future__ import annotations

import enum
import logging
import os
import sys
from typing import Any

_logger = logging.getLogger(__name__)


class BootstrapResult(enum.Enum):
    """Outcome of :func:`bootstrap_logfire`.

    The shim snapshots one of these values per process and returns the
    snapshot on every subsequent call (idempotency).
    """

    #: ``bootstrap_logfire()`` has not yet been invoked in this process.
    UNCALLED = "uncalled"

    #: ``logfire.configure(...)`` returned without raising.
    CONFIGURED = "configured"

    #: ``LOGFIRE_ENABLED=0`` honored — Intake discipline per §8.4.1.
    SKIPPED_DISABLED = "skipped_disabled"

    #: ``import logfire`` raised ``ImportError``; logfire is not pinned
    #: in the active environment.
    SKIPPED_NOT_INSTALLED = "skipped_not_installed"

    #: ``sys.modules['logfire']`` resolved to a §8.4.1 stub.
    SKIPPED_STUB = "skipped_stub"

    #: ``logfire.configure(...)`` raised — usually means the operator has
    #: not yet run ``logfire auth`` (runbook §1.4 OP-01).
    SKIPPED_NO_CREDENTIALS = "skipped_no_credentials"


# Process-wide bootstrap snapshot.  Updated exactly once per process under
# normal operation (the idempotent guard in ``bootstrap_logfire`` enforces
# the cap).  Tests use ``_reset_for_testing()`` to clear between cases.
_BOOTSTRAP_RESULT: BootstrapResult = BootstrapResult.UNCALLED


def bootstrap_logfire() -> BootstrapResult:
    """Bootstrap Logfire for the current process.

    Returns
    -------
    BootstrapResult
        The outcome of the bootstrap attempt.  Subsequent calls in the
        same process return the same snapshotted value without re-running
        ``configure()``.

    Notes
    -----
    See module docstring for the full contract.  This function is
    designed to be safe to call from ``pipeline/__init__.py`` at
    module-load time of the package.
    """

    global _BOOTSTRAP_RESULT

    # 1. Idempotent guard — return the snapshot on re-entry.
    if _BOOTSTRAP_RESULT is not BootstrapResult.UNCALLED:
        return _BOOTSTRAP_RESULT

    # 2. §8.4.1 Intake discipline — LOGFIRE_ENABLED=0 means stay disabled.
    #    The Intake CLI sets this BEFORE importing pipeline; honoring it
    #    here keeps Intake's process-isolation guarantee intact.
    if os.environ.get("LOGFIRE_ENABLED") == "0":
        _BOOTSTRAP_RESULT = BootstrapResult.SKIPPED_DISABLED
        return _BOOTSTRAP_RESULT

    # 3. Pre-import sys.modules check — if Intake (or a test fixture) has
    #    already installed a §8.4.1 ``_LogfireDisabledStub``, do not
    #    overwrite it.  The stub's ``__getattr__`` raises RuntimeError
    #    rather than AttributeError, so ``hasattr`` propagates instead
    #    of returning False; use a defensive ``_has_configure`` helper.
    pre_existing = sys.modules.get("logfire")
    if pre_existing is not None and not _has_configure(pre_existing):
        _BOOTSTRAP_RESULT = BootstrapResult.SKIPPED_STUB
        return _BOOTSTRAP_RESULT

    # 4. Attempt the import.  Logfire is pinned in pyproject.toml per
    #    D-RB-01; an ImportError here means either the operator has not
    #    yet installed the dev dependencies (`pip install -e '.[dev]'`)
    #    or this is running in an embedded environment where logfire is
    #    intentionally absent.  Either way, degrade gracefully.
    try:
        import logfire  # noqa: PLC0415 — lazy import is the whole point
    except ImportError:
        _logger.warning(
            "logfire not installed; observability disabled. "
            "Install per deployment runbook §1.4: "
            "`pip install 'logfire>=0.42'` (or `pip install -e '.[dev]'`)."
        )
        _BOOTSTRAP_RESULT = BootstrapResult.SKIPPED_NOT_INSTALLED
        return _BOOTSTRAP_RESULT

    # 5. Post-import re-check.  A stub may have been installed between
    #    the sys.modules check above and the import statement (unlikely
    #    in normal flow; possible under test fixtures that patch state).
    if not _has_configure(logfire):
        _BOOTSTRAP_RESULT = BootstrapResult.SKIPPED_STUB
        return _BOOTSTRAP_RESULT

    # 6. Configure.  ``send_to_logfire='if-token-present'`` is Logfire's
    #    documented graceful-degrade mode: local span machinery is set
    #    up, upload silently no-ops when no write-token is found at
    #    ``~/.logfire/default.toml`` or in ``LOGFIRE_TOKEN``.
    try:
        logfire.configure(
            send_to_logfire="if-token-present",
            service_name="tilth",
            service_version=_resolve_service_version(),
        )
        _BOOTSTRAP_RESULT = BootstrapResult.CONFIGURED
    except Exception as exc:  # noqa: BLE001 — any failure → no-op + WARNING
        _logger.warning(
            "logfire.configure() failed (%s: %s); "
            "operator may not have run `logfire auth` yet "
            "(deployment runbook OP-01) — "
            "observability degraded to no-op for this process",
            type(exc).__name__,
            exc,
        )
        _BOOTSTRAP_RESULT = BootstrapResult.SKIPPED_NO_CREDENTIALS

    return _BOOTSTRAP_RESULT


def get_bootstrap_result() -> BootstrapResult:
    """Read-only accessor for the snapshotted bootstrap outcome.

    Production callsites that need to know whether Logfire is live (e.g.
    a span-emitting wrapper that should skip the emission cost when the
    backend is no-op) should consult this rather than re-calling
    ``bootstrap_logfire()``.  Cheap.
    """

    return _BOOTSTRAP_RESULT


def _has_configure(module: Any) -> bool:
    """Return True iff ``module.configure`` is a real callable.

    The §8.4.1 ``_LogfireDisabledStub.__getattr__`` raises ``RuntimeError``
    on any attribute access, which propagates through ``hasattr`` (which
    only catches ``AttributeError``).  Use a broad try/except to keep the
    stub-detection robust against any custom ``__getattr__`` that does not
    follow the ``AttributeError`` convention.
    """

    try:
        attr = getattr(module, "configure", None)
    except Exception:  # noqa: BLE001 — stub may raise on ANY access
        return False
    return callable(attr)


def _resolve_service_version() -> str:
    """Return the ``service_version`` string Logfire should tag spans with.

    Reads ``pipeline.__version__`` via ``sys.modules`` to avoid a circular
    import during ``pipeline/__init__.py`` execution — ``bootstrap_logfire``
    runs while the ``pipeline`` package is still mid-init, so a direct
    ``from pipeline import __version__`` could trip a partial-module
    access in pathological orderings.  ``sys.modules.get('pipeline')``
    returns the partially-initialized module, on which the version
    assignment has already been made (because ``pipeline/__init__.py``
    sets ``__version__`` before calling this shim).
    """

    pipeline_mod = sys.modules.get("pipeline")
    if pipeline_mod is not None:
        version = getattr(pipeline_mod, "__version__", None)
        if isinstance(version, str):
            return version
    return "unknown"


def _reset_for_testing() -> None:
    """Reset the bootstrap snapshot to ``UNCALLED``.

    **TEST USE ONLY.**  Production code must not call this — the
    idempotency guarantee depends on the snapshot persisting for the
    lifetime of the process.  The leading underscore + the
    ``_for_testing`` suffix + this docstring document the convention.
    """

    global _BOOTSTRAP_RESULT
    _BOOTSTRAP_RESULT = BootstrapResult.UNCALLED


__all__ = [
    "BootstrapResult",
    "bootstrap_logfire",
    "get_bootstrap_result",
]
