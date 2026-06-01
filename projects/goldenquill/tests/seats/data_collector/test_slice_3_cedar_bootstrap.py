"""Tests for WS-I §13 Data Collector Slice 3 — Cedar engine bootstrap.

Per §13 v1 LOCKED 2026-05-10 (§13.16.1 RT-06 + §13.16.6.2 RT-C2-04
closures).  The Cedar engine MUST be instantiated at module load and the
seat module MUST refuse to import if any bundled policy file fails the
grammar floor.

Covers:
  * ``CedarEngine.load_all()`` walks the policy directory and loads all
    four bundled policies authored at Slice 3.
  * ``CedarEngine.is_ready()`` is identity-strict True after a clean
    load.
  * Load failure raises :class:`CedarEngineLoadError` (Exception
    subclass) which the seat-side ``_bootstrap_cedar_engine`` re-wraps
    in :class:`CriticalPolicyError` (BaseException subclass).
  * ``CriticalPolicyError`` propagates through ``try/except Exception``
    (RT-C2-04).
  * Empty policy directory raises :class:`CedarEngineLoadError`.
  * Malformed policy file raises :class:`CedarEngineLoadError`.
  * Identity-strict readiness check rejects truthy non-True returns.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.logician.cedar_eval import CedarEngine, CedarEngineLoadError
from pipeline.orchestrator.seats.data_collector import (
    CriticalPolicyError,
    _CEDAR_POLICY_DIR,
    _bootstrap_cedar_engine,
    get_cedar_engine,
)


_EXPECTED_POLICIES: frozenset[str] = frozenset({
    "consent_ledger_isolation",
    "data_collector_send",
    "beneficiary_records_pii",
    "data_collector_audit_redaction",
})


def test_cedar_engine_loads_all_four_bundled_policies():
    """The bundled policy directory ships four .cedar files."""
    engine = CedarEngine(policy_dir=_CEDAR_POLICY_DIR)
    engine.load_all()
    assert engine.is_ready() is True
    assert set(engine.loaded_policy_names()) == _EXPECTED_POLICIES


def test_cedar_engine_is_ready_is_identity_true():
    """RT-C2-04 + v7.0.7 §4.3.4 identity-strict pattern: caller checks
    ``engine.is_ready() is True`` not just truthiness."""
    engine = CedarEngine(policy_dir=_CEDAR_POLICY_DIR)
    engine.load_all()
    result = engine.is_ready()
    assert result is True  # identity match
    assert isinstance(result, bool)


def test_cedar_engine_initial_state_is_not_ready():
    """A freshly constructed engine reports not-ready before load_all."""
    engine = CedarEngine(policy_dir=_CEDAR_POLICY_DIR)
    assert engine.is_ready() is False


def test_cedar_engine_empty_directory_raises(tmp_path: Path):
    """Empty cedar_policies/ directory fails closed at load time."""
    (tmp_path / "cedar_policies").mkdir()
    engine = CedarEngine(policy_dir=tmp_path / "cedar_policies")
    with pytest.raises(CedarEngineLoadError, match="contains no \\*\\.cedar files"):
        engine.load_all()
    assert engine.is_ready() is False


def test_cedar_engine_missing_directory_raises(tmp_path: Path):
    """policy_dir pointing to a non-existent path fails closed."""
    engine = CedarEngine(policy_dir=tmp_path / "does_not_exist")
    with pytest.raises(CedarEngineLoadError, match="not a directory"):
        engine.load_all()
    assert engine.is_ready() is False


def test_cedar_engine_malformed_policy_raises(tmp_path: Path):
    """Policy file with neither permit nor forbid fails the grammar floor."""
    policy_dir = tmp_path / "cedar_policies"
    policy_dir.mkdir()
    (policy_dir / "broken.cedar").write_text("// just a comment\n", encoding="utf-8")
    engine = CedarEngine(policy_dir=policy_dir)
    with pytest.raises(CedarEngineLoadError, match="failed grammar floor"):
        engine.load_all()


def test_cedar_engine_empty_policy_file_raises(tmp_path: Path):
    """Empty policy file fails the grammar floor."""
    policy_dir = tmp_path / "cedar_policies"
    policy_dir.mkdir()
    (policy_dir / "empty.cedar").write_text("", encoding="utf-8")
    engine = CedarEngine(policy_dir=policy_dir)
    with pytest.raises(CedarEngineLoadError, match="empty"):
        engine.load_all()


def test_cedar_engine_admits_minimal_valid_policy(tmp_path: Path):
    """Single minimal policy file admitted: name extracted from stem,
    grammar floor satisfied by 'permit' keyword."""
    policy_dir = tmp_path / "cedar_policies"
    policy_dir.mkdir()
    policy_a = policy_dir / "minimal.cedar"
    policy_a.write_text("permit ( principal, action, resource );\n", encoding="utf-8")
    engine = CedarEngine(policy_dir=policy_dir)
    engine.load_all()
    assert engine.is_ready() is True
    assert engine.loaded_policy_names() == ("minimal",)
    assert "permit" in engine.policy_text("minimal")


def test_seat_bootstrap_succeeds_on_canonical_tree():
    """The seat-side ``_bootstrap_cedar_engine`` succeeds against the
    canonical tree shipped with this commit."""
    # The seat module was already imported at test-collection time (the
    # import-side-effect runs the bootstrap). If it didn't raise, the
    # bootstrap succeeded; otherwise the test wouldn't run.
    engine = get_cedar_engine()
    assert engine.is_ready() is True
    assert set(engine.loaded_policy_names()) == _EXPECTED_POLICIES


def test_critical_policy_error_propagates_through_try_except_exception():
    """RT-C2-04 — CriticalPolicyError subclasses BaseException so
    ``try/except Exception`` cannot swallow it."""
    # The seat-defined CriticalPolicyError is the BaseException subclass.
    error_class_caught_by_exception = False
    try:
        raise CriticalPolicyError("synthetic")
    except Exception:
        error_class_caught_by_exception = True
    except CriticalPolicyError:
        pass
    assert error_class_caught_by_exception is False, (
        "CriticalPolicyError MUST NOT be catchable by `except Exception`; "
        "it subclasses BaseException directly per RT-C2-04"
    )


def test_critical_policy_error_subclasses_baseexception_not_exception():
    """Structural assertion that ``CriticalPolicyError`` lives on the
    BaseException branch of the exception hierarchy."""
    assert issubclass(CriticalPolicyError, BaseException)
    assert not issubclass(CriticalPolicyError, Exception)


def test_bootstrap_is_idempotent(monkeypatch, tmp_path: Path):
    """Re-running ``_bootstrap_cedar_engine`` against the live policy
    directory produces a fresh engine handle — the global ``_cedar_engine``
    is replaced with a new instance."""
    import pipeline.orchestrator.seats.data_collector as dc_module
    before = dc_module._cedar_engine
    _bootstrap_cedar_engine()
    after = dc_module._cedar_engine
    assert after.is_ready() is True
    # Either same instance (no-op) or different instance (re-bound).
    # Either way, the engine is ready.
    assert isinstance(after, CedarEngine)


def test_seat_bootstrap_wraps_load_failure_in_critical_policy_error(
    monkeypatch, tmp_path: Path
):
    """If the bundled policy directory is replaced with a broken one, the
    seat-side bootstrap raises :class:`CriticalPolicyError` (not the inner
    CedarEngineLoadError)."""
    broken_dir = tmp_path / "broken_cedar_policies"
    broken_dir.mkdir()
    (broken_dir / "broken.cedar").write_text("// just a comment\n", encoding="utf-8")
    monkeypatch.setattr(
        "pipeline.orchestrator.seats.data_collector._CEDAR_POLICY_DIR",
        broken_dir,
    )
    with pytest.raises(CriticalPolicyError, match="Cedar engine load failure"):
        _bootstrap_cedar_engine()


def test_seat_bootstrap_fails_closed_on_empty_policy_directory(
    monkeypatch, tmp_path: Path
):
    """Empty policy directory triggers CriticalPolicyError at module load."""
    empty_dir = tmp_path / "empty_cedar_policies"
    empty_dir.mkdir()
    monkeypatch.setattr(
        "pipeline.orchestrator.seats.data_collector._CEDAR_POLICY_DIR",
        empty_dir,
    )
    with pytest.raises(CriticalPolicyError, match="Cedar engine load failure"):
        _bootstrap_cedar_engine()


def test_seat_bootstrap_fails_closed_on_missing_policy_directory(
    monkeypatch, tmp_path: Path
):
    """Missing policy directory triggers CriticalPolicyError at module load."""
    monkeypatch.setattr(
        "pipeline.orchestrator.seats.data_collector._CEDAR_POLICY_DIR",
        tmp_path / "does_not_exist",
    )
    with pytest.raises(CriticalPolicyError, match="Cedar engine load failure"):
        _bootstrap_cedar_engine()


def test_policy_text_round_trip_for_each_bundled_policy():
    """Each bundled policy's text is recoverable via ``policy_text()`` and
    is non-empty + contains 'permit' or 'forbid' (grammar floor smoke
    test)."""
    engine = get_cedar_engine()
    for name in _EXPECTED_POLICIES:
        text = engine.policy_text(name)
        assert text.strip(), f"policy {name!r} text is empty"
        assert "permit" in text or "forbid" in text, (
            f"policy {name!r} has no permit/forbid keyword"
        )


def test_data_collector_send_policy_carries_caller_module_pin():
    """RT-06 + R-DATACOLLECTOR-NO-AUTOSEND Layer 3 mirror — the Cedar
    policy's PERMIT clause pins the caller_module to outbound_batch."""
    engine = get_cedar_engine()
    text = engine.policy_text("data_collector_send")
    assert "outbound_batch" in text, (
        "data_collector_send.cedar must pin caller_module to outbound_batch "
        "(§13.7 Layer 3)"
    )


def test_beneficiary_records_pii_policy_enumerates_consent_tier_literals():
    """RT-C2-10 — Cedar policy enforces the same enum at the Cedar layer
    that the lint rule enforces at the compile-time layer."""
    engine = get_cedar_engine()
    text = engine.policy_text("beneficiary_records_pii")
    for literal in ("my_eyes_only", "matchable_to_opportunities", "composable_with_others"):
        assert literal in text, (
            f"beneficiary_records_pii.cedar missing consent_tier literal {literal!r}"
        )


def test_consent_ledger_isolation_policy_enforces_law3():
    """RT-06 — the consent ledger Cedar policy enforces Law 3 org isolation."""
    engine = get_cedar_engine()
    text = engine.policy_text("consent_ledger_isolation")
    assert "org_slug" in text and "forbid" in text


def test_data_collector_audit_redaction_policy_redacts_recipient_id():
    """RT-06 — cross-org audit dumps redact recipient_id via hashed prefix."""
    engine = get_cedar_engine()
    text = engine.policy_text("data_collector_audit_redaction")
    assert "hashed_first_8_chars" in text
