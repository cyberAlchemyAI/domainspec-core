"""Adversarial tests for F-BOOTSTRAP-REUSE (F-AMDT-01).

Threat model (spec card v1, 2026-04-20):
  * A late amendment attempts to smuggle itself as a "bootstrap" event by
    setting ``bootstrap_exception: true`` after the initial TSIP seed has
    already consumed it.
  * Reader-layer failures (IO, parse) must fail-closed — never conflate
    "empty history" with "read failure".
  * Truthy-but-not-strict-True values must NOT count (attacker might use
    ``1``, ``"true"`` to evade strict-bool enforcement in a non-strict
    implementation).
  * Mutating rows after reader return must not matter — the gate operates
    on what the reader returned at call time.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates import F_AMDT_01, check_bootstrap_reuse


class _FakeBool:
    """A lookalike class with ``__bool__`` that returns True — must not count."""

    def __bool__(self) -> bool:  # pragma: no cover - exercised via isinstance
        return True

    def __repr__(self) -> str:
        return "_FakeBool()"


def test_adv_reader_raises_file_not_found() -> None:
    def _bad() -> list[dict]:
        raise FileNotFoundError("lock_history.v1.jsonl not found")
    r = check_bootstrap_reuse(lock_history_reader=_bad)
    assert r.success is False
    assert r.failure_code == F_AMDT_01
    assert r.detail.reason_tag == "reader_raised"
    assert "FileNotFoundError" in (r.detail.reader_error or "")


def test_adv_reader_raises_value_error_from_malformed_jsonl() -> None:
    def _bad() -> list[dict]:
        raise ValueError("json decode error at line 42")
    r = check_bootstrap_reuse(lock_history_reader=_bad)
    assert r.success is False
    assert r.detail.reason_tag == "reader_raised"
    assert "ValueError" in (r.detail.reader_error or "")


def test_adv_reader_raises_permission_error() -> None:
    def _bad() -> list[dict]:
        raise PermissionError("denied")
    r = check_bootstrap_reuse(lock_history_reader=_bad)
    assert r.success is False
    assert r.detail.reason_tag == "reader_raised"


def test_adv_fake_bool_class_with_truthy_dunder_rejected() -> None:
    """An attacker class with ``__bool__`` returning True must NOT count.

    Gate uses ``is True`` not ``bool(x)`` — identity check defeats duck-typed
    bypass attempts.
    """
    rows = [{"bootstrap_exception": _FakeBool()} for _ in range(5)]
    r = check_bootstrap_reuse(lock_history_reader=lambda: rows)
    assert r.success is True


def test_adv_integer_one_rejected_as_bootstrap() -> None:
    """``1`` is falsy under identity test with ``True``; does not count."""
    rows = [{"bootstrap_exception": 1} for _ in range(10)]
    r = check_bootstrap_reuse(lock_history_reader=lambda: rows)
    assert r.success is True


def test_adv_string_true_rejected_as_bootstrap() -> None:
    rows = [{"bootstrap_exception": "true"}, {"bootstrap_exception": "True"}]
    r = check_bootstrap_reuse(lock_history_reader=lambda: rows)
    assert r.success is True


def test_adv_concurrent_staged_rows_both_bootstrap() -> None:
    """Two rows in same batch both claim bootstrap — DENY."""
    rows = [
        {"module": "a", "bootstrap_exception": True},
        {"module": "b", "bootstrap_exception": True},
    ]
    r = check_bootstrap_reuse(lock_history_reader=lambda: rows)
    assert r.success is False
    assert r.detail.bootstrap_count == 2


def test_adv_reader_mutation_after_gate_return() -> None:
    """Mutating the reader's list after the gate returns must not retroactively
    change the verdict. The gate operates on what the reader returned AT
    call time; the result is a frozen dataclass."""
    rows: list[dict] = [{"bootstrap_exception": True}]
    def _reader() -> list[dict]:
        return rows
    r = check_bootstrap_reuse(lock_history_reader=_reader)
    assert r.success is True

    # Mutate list post-call — should not affect the result.
    rows.append({"bootstrap_exception": True})
    assert r.success is True  # frozen


def test_adv_deeply_nested_row_does_not_confuse_counting() -> None:
    rows = [
        {
            "module": "a",
            "nested": {"bootstrap_exception": True},  # not top-level — no count
            "deeper": {"more": {"bootstrap_exception": True}},
        }
    ] * 10
    r = check_bootstrap_reuse(lock_history_reader=lambda: rows)
    assert r.success is True


def test_adv_bootstrap_value_is_true_class_not_instance() -> None:
    """Passing the ``bool`` class itself instead of its instance."""
    rows = [{"bootstrap_exception": bool}] * 5  # the TYPE, not True
    r = check_bootstrap_reuse(lock_history_reader=lambda: rows)
    assert r.success is True


def test_adv_single_row_is_staged_row_with_true_passes() -> None:
    """The staged row alone, first ever bootstrap write — single True passes."""
    r = check_bootstrap_reuse(
        lock_history_reader=lambda: [{"module": "tsip.bootstrap.seed", "bootstrap_exception": True}]
    )
    assert r.success is True


def test_adv_row_without_dict_at_mid_list_denied_fail_closed() -> None:
    """A malformed row in the middle of an otherwise well-formed list must
    abort counting (fail-closed). Gate must not silently skip bad rows and
    keep counting — that would risk missing legitimate F-AMDT-01 fires on
    larger histories."""
    rows: list[object] = [
        {"bootstrap_exception": True},
        "corrupted",
        {"bootstrap_exception": True},
    ]
    r = check_bootstrap_reuse(lock_history_reader=lambda: rows)  # type: ignore[arg-type]
    assert r.success is False
    assert r.detail.reason_tag == "reader_contract_violation"


def test_adv_huge_history_with_staged_row_scans_all() -> None:
    """A one-million-row history must still be checked end-to-end — an
    attacker cannot hide a reuse by padding the front of the JSONL."""
    n = 10_000
    rows = [{"module": f"m{i}"} for i in range(n)]
    rows[0]["bootstrap_exception"] = True
    rows[-1]["bootstrap_exception"] = True  # the smuggled reuse
    r = check_bootstrap_reuse(lock_history_reader=lambda: rows)
    assert r.success is False
    assert r.detail.bootstrap_count == 2
    assert r.detail.offending_indices == (0, n - 1)
