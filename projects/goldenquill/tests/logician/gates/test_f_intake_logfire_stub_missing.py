"""F-INTAKE-LOGFIRE-STUB-MISSING tests (M1 §8.4.1)."""

from __future__ import annotations

import sys
import types

from pipeline.cli.tilth_intake import (
    LOGFIRE_DISABLED_ENV,
    LOGFIRE_DISABLED_VALUE,
    LOGFIRE_STUB_NAME,
    install_logfire_disabled_stub,
    is_logfire_stub_active,
    subprocess_bootstrap_source,
)
from pipeline.logician.gates.f_intake_logfire_stub_missing import (
    F_INTAKE_LOGFIRE_STUB_MISSING,
    check_intake_logfire_stub_missing,
)


def test_failure_code_constant() -> None:
    assert F_INTAKE_LOGFIRE_STUB_MISSING == "F-INTAKE-LOGFIRE-STUB-MISSING"


def test_stub_active_after_bootstrap_passes() -> None:
    install_logfire_disabled_stub()
    assert is_logfire_stub_active() is True
    r = check_intake_logfire_stub_missing()
    assert r.success is True


def test_stub_missing_when_not_installed_fails(monkeypatch) -> None:
    """Simulate the bootstrap not running by replacing the module."""
    monkeypatch.delenv(LOGFIRE_DISABLED_ENV, raising=False)
    fake = types.ModuleType("logfire")  # plain module, NOT the stub
    monkeypatch.setitem(sys.modules, LOGFIRE_STUB_NAME, fake)
    r = check_intake_logfire_stub_missing()
    assert r.success is False
    assert r.failure_code == F_INTAKE_LOGFIRE_STUB_MISSING


def test_stub_attribute_access_raises() -> None:
    install_logfire_disabled_stub()
    stub = sys.modules[LOGFIRE_STUB_NAME]
    try:
        stub.info  # noqa: B018 -- intentional access
    except RuntimeError as exc:
        assert "Logfire access denied" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("stub did not raise on attribute access")


def test_stub_mutation_raises() -> None:
    install_logfire_disabled_stub()
    stub = sys.modules[LOGFIRE_STUB_NAME]
    try:
        stub.foo = "bar"
    except RuntimeError as exc:
        assert "denied" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("stub did not raise on attribute set")


def test_subprocess_bootstrap_source_strips_quotes() -> None:
    src = subprocess_bootstrap_source()
    assert "logfire" in src
    assert "LOGFIRE_ENABLED" in src
    assert LOGFIRE_DISABLED_VALUE in src


def test_subprocess_marker_after_install() -> None:
    install_logfire_disabled_stub()
    assert is_logfire_stub_active() is True
    r = check_intake_logfire_stub_missing(is_subprocess=True)
    assert r.success is True
    assert r.is_subprocess is True
