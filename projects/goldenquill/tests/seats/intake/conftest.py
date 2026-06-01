"""Conftest for the intake test package.

Reload-cleanup fixture
======================

The §11 v1.1 LOCK (rows 209/210, 2026-05-11) added
``test_reload_preserves_identity_when_canonical_home_reloaded_first`` to
this package. That test deliberately mutates module state via
``importlib.reload`` on the canonical commitment_id home
(``pipeline.orchestrator.seats._commitment_id``) and the report_generator
shim (``pipeline.orchestrator.seats.report_generator._commitment_id``).

``importlib.reload`` rebinds every name in a module's ``__dict__``
in-place. Downstream test modules that imported ``CommitmentIdInvalid``
or ``sanitize_commitment_id`` at module load time end up with stale
references to the *pre*-reload class objects. When the reload test runs
*first* in pytest collection order, six assertions in
``tests/seats/report_generator/test_commitment_id.py::
TestSanitizeCommitmentId`` fail under ``pytest.raises(CommitmentIdInvalid)``
because the raised exception is an instance of the *post*-reload class
while the ``raises`` clause checks against the *pre*-reload class.

The fixture below snapshots both modules' ``__dict__`` contents before
the reload test runs and restores them after. ``__dict__.clear()`` +
``__dict__.update(snapshot)`` rebinds every name back to the
pre-reload object identity. Because Python function objects resolve
free names through their owning module's ``__dict__`` (not a frozen
copy), restoring the dict contents makes downstream test modules'
existing references re-resolve correctly on subsequent calls.

Outside the reload-protocol test, the fixture is a fast no-op (two
attribute lookups, then ``yield``). Scope is per-function autouse.
"""

from __future__ import annotations

import sys
from typing import Iterator

import pytest


_CANONICAL_NAME = "pipeline.orchestrator.seats._commitment_id"
_SHIM_NAME = "pipeline.orchestrator.seats.report_generator._commitment_id"

# Tests that call ``importlib.reload`` on the canonical home / shim and
# therefore require snapshot/restore around their execution.
_RELOAD_PROTOCOL_TEST_NAMES = frozenset(
    {
        "test_reload_preserves_identity_when_canonical_home_reloaded_first",
    }
)


@pytest.fixture(autouse=True)
def _restore_commitment_id_module_state(
    request: pytest.FixtureRequest,
) -> Iterator[None]:
    """Snapshot/restore canonical + shim module ``__dict__`` around tests
    that reload them.

    Identifies the reload-protocol test by name (so the cost outside
    that test is a single ``frozenset`` membership check + ``yield``).
    For the reload test: snapshots both modules' ``__dict__`` contents
    pre-test; on teardown ``clear()`` + ``update()`` restores every
    name binding to its pre-reload object identity.
    """
    if request.node.name not in _RELOAD_PROTOCOL_TEST_NAMES:
        yield
        return

    canonical = sys.modules.get(_CANONICAL_NAME)
    shim = sys.modules.get(_SHIM_NAME)

    # Defensive snapshot of the pre-test module dict contents. If either
    # module has not yet been imported, the snapshot is ``None`` and the
    # restore step is a no-op for that module.
    canonical_snapshot = (
        dict(canonical.__dict__) if canonical is not None else None
    )
    shim_snapshot = dict(shim.__dict__) if shim is not None else None

    try:
        yield
    finally:
        # Restore via ``clear() + update()`` so the module's ``__dict__``
        # object identity is preserved; only its contents are rewound.
        # This is what makes the fix work for downstream test modules
        # that hold references to functions whose ``__globals__`` is
        # this same dict.
        if canonical is not None and canonical_snapshot is not None:
            canonical.__dict__.clear()
            canonical.__dict__.update(canonical_snapshot)
        if shim is not None and shim_snapshot is not None:
            shim.__dict__.clear()
            shim.__dict__.update(shim_snapshot)
