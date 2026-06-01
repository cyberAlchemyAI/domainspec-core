"""F-KFR-DUPLICATE-KEY tests (M1 §7.2)."""

from __future__ import annotations

from pipeline.logician.gates.f_kfr_duplicate_key import (
    COMPOSITE_KEY_BYTE_LEN,
    F_KFR_DUPLICATE_KEY,
    check_kfr_duplicate_key,
    compute_composite_key,
)


def _fact(fact_id: str, *, who: str, what: str, when_period: str) -> dict:
    return {
        "id": fact_id,
        "who": who,
        "what": what,
        "when_period": when_period,
    }


def test_failure_code_constant() -> None:
    assert F_KFR_DUPLICATE_KEY == "F-KFR-DUPLICATE-KEY"


def test_unique_composite_key_passes() -> None:
    cand = _fact("F1", who="org_a", what="enrollment", when_period="2025")
    active = [_fact("F2", who="org_a", what="revenue", when_period="2025")]
    r = check_kfr_duplicate_key(
        fact_id="F1",
        candidate_fact=cand,
        active_facts=active,
    )
    assert r.success is True


def test_duplicate_composite_key_fails() -> None:
    cand = _fact("F1", who="org_a", what="enrollment", when_period="2025")
    existing = _fact("F2", who="org_a", what="enrollment", when_period="2025")
    r = check_kfr_duplicate_key(
        fact_id="F1",
        candidate_fact=cand,
        active_facts=[existing],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_DUPLICATE_KEY


def test_self_match_passes_for_same_fact_id() -> None:
    """Re-saving the same entry with same composite key is admitted."""
    cand = _fact("F1", who="org_a", what="enrollment", when_period="2025")
    active = [cand]
    r = check_kfr_duplicate_key(
        fact_id="F1",
        candidate_fact=cand,
        active_facts=active,
    )
    assert r.success is True


def test_compute_composite_key_byte_len() -> None:
    fact = _fact("F1", who="a", what="b", when_period="c")
    key = compute_composite_key(fact)
    assert len(key) == COMPOSITE_KEY_BYTE_LEN


def test_compute_composite_key_changes_with_who() -> None:
    a = compute_composite_key(_fact("F1", who="a", what="b", when_period="c"))
    b = compute_composite_key(_fact("F1", who="x", what="b", when_period="c"))
    assert a != b


def test_compute_composite_key_changes_with_when_period() -> None:
    a = compute_composite_key(_fact("F1", who="a", what="b", when_period="2025"))
    b = compute_composite_key(_fact("F1", who="a", what="b", when_period="2026"))
    assert a != b
