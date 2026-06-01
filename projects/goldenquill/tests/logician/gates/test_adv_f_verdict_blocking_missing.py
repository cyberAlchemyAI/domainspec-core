"""Adversarial tests for F-VERDICT-BLOCKING-MISSING (F-AMDT-02).

These are NOT happy-path variants. Each test exercises a specific attack
surface or threat vector the gate must reject fail-closed.

Threat model (spec card v1, 2026-04-20):
  * Case-confusion: reviewer returns "Blocking" / "BLOCKING" hoping lax
    normalisation will accept. Gate must be case-sensitive.
  * Type-confusion: numpy.bool_ / np.True_ / custom bool-lookalike classes
    that answer ``__bool__`` but fail ``isinstance(_, bool)``.
  * Non-dict verdict (string / list) — must not crash with AttributeError
    or TypeError, must DENY cleanly.
  * Mutation races — dict state mutated after gate receives reference but
    before the gate reads it (gate reads at fire time, not init).
  * Empty dict — must not raise KeyError.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_02,
    check_verdict_blocking,
)


def test_adv_blocking_key_case_sensitivity() -> None:
    """`{"Blocking": true}` — case-sensitive key match must refuse."""
    for variant in ("Blocking", "BLOCKING", "bLoCkInG", "Blocking "):
        r = check_verdict_blocking({variant: True})
        assert r.success is False, f"variant {variant!r} wrongly passed"
        assert r.failure_code == F_AMDT_02
        assert r.detail.reason_tag == "blocking_key_absent"


def test_adv_blocking_value_is_bool_lookalike() -> None:
    """Custom class that answers ``__bool__`` must not satisfy ``isinstance(_, bool)``.

    Documents the strict-isinstance limitation: duck-typed truthiness is
    explicitly rejected. Only stdlib bool passes.
    """

    class FakeBool:
        def __bool__(self) -> bool:  # noqa: D401
            return True

        def __repr__(self) -> str:
            return "FakeBool()"

    r = check_verdict_blocking({"blocking": FakeBool()})
    assert r.success is False
    assert r.failure_code == F_AMDT_02
    assert r.detail.reason_tag == "blocking_value_not_bool"
    assert r.detail.observed_type == "FakeBool"


def test_adv_verdict_is_not_dict() -> None:
    """Verdict passed as string / list / int / None / tuple — clean DENY, no crash."""
    for non_dict in ("blocking: true", ["blocking", True], 42, None, (True,), b"{}"):
        r = check_verdict_blocking(non_dict)  # type: ignore[arg-type]
        assert r.success is False, f"non-dict {non_dict!r} wrongly passed"
        assert r.failure_code == F_AMDT_02
        assert r.detail.reason_tag == "verdict_not_dict"


def test_adv_blocking_field_added_after_initial_parse() -> None:
    """Mutation race — gate reads dict at fire time, not init time."""
    d: dict = {}
    r_before = check_verdict_blocking(d)
    assert r_before.success is False
    assert r_before.detail.reason_tag == "blocking_key_absent"

    d["blocking"] = True
    r_after = check_verdict_blocking(d)
    assert r_after.success is True

    d["blocking"] = "true"
    r_mutated = check_verdict_blocking(d)
    assert r_mutated.success is False
    assert r_mutated.detail.reason_tag == "blocking_value_not_bool"


def test_adv_empty_verdict_no_crash() -> None:
    """`{}` — clean DENY, no KeyError, no AttributeError."""
    # Repeat multiple times — the gate must be stateless.
    for _ in range(5):
        r = check_verdict_blocking({})
        assert r.success is False
        assert r.failure_code == F_AMDT_02
        assert r.detail.reason_tag == "blocking_key_absent"


def test_adv_subclass_of_dict_accepted() -> None:
    """A ``dict`` subclass (e.g. ``OrderedDict``) still hits the isinstance branch."""
    from collections import OrderedDict

    od: OrderedDict = OrderedDict()
    od["blocking"] = True
    r = check_verdict_blocking(od)
    assert r.success is True


def test_adv_dict_with_blocking_key_mapped_to_callable_denied() -> None:
    """Callable value (e.g. a lambda returning True) — not a bool."""
    r = check_verdict_blocking({"blocking": lambda: True})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_value_not_bool"


def test_adv_deeply_nested_blocking_does_not_leak() -> None:
    """Blocking nested 5 levels deep must NOT satisfy the top-level check."""
    nested = {
        "a": {"b": {"c": {"d": {"e": {"blocking": True}}}}}
    }
    r = check_verdict_blocking(nested)
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


def test_adv_non_string_key_matching_blocking_denied() -> None:
    """A non-string key (bytes, int) that happens to equal 'blocking' via str()
    coercion must not satisfy the check — dict lookup is by identity-aware
    equality, not by repr."""
    d = {b"blocking": True, 123: True}
    r = check_verdict_blocking(d)
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


def test_adv_frozenset_or_mappingproxy_verdict_rejected_as_non_dict() -> None:
    """A ``types.MappingProxyType`` wrapping a dict IS still a Mapping but
    is NOT a ``dict`` subclass — the gate insists on ``dict`` specifically
    because the upstream JSON parser emits plain dicts."""
    import types

    mp = types.MappingProxyType({"blocking": True})
    r = check_verdict_blocking(mp)
    assert r.success is False
    assert r.detail.reason_tag == "verdict_not_dict"
