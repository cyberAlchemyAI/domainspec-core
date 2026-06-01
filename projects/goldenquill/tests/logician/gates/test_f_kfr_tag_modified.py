"""F-KFR-TAG-MODIFIED tests (M1 §4 / §4.2 / §4.4)."""

from __future__ import annotations

from pipeline.logician.gates.f_kfr_tag_modified import (
    F_KFR_TAG_MODIFIED,
    LEDGER_KIND_TAG_MODIFIED,
    check_kfr_tag_modified,
    compute_tag_set_hash,
)


def _fact(*, required_for_funder=None, required_for_category=None,
          key_credentials=None) -> dict:
    return {
        "id": "F1",
        "required_for_funder": required_for_funder or [],
        "required_for_category": required_for_category or [],
        "key_credentials": key_credentials,
    }


def test_failure_code_constant() -> None:
    assert F_KFR_TAG_MODIFIED == "F-KFR-TAG-MODIFIED"


def test_no_change_passes() -> None:
    fact = _fact(required_for_funder=["USDA-VAPG"])
    r = check_kfr_tag_modified(
        fact_id="F1",
        fact_before=fact,
        fact_after=dict(fact),
        ledger_entries=[],
    )
    assert r.success is True


def test_tag_added_without_signed_ledger_fails() -> None:
    before = _fact(required_for_funder=["USDA-VAPG"])
    after = _fact(required_for_funder=["USDA-VAPG", "USDA-RD"])
    r = check_kfr_tag_modified(
        fact_id="F1",
        fact_before=before,
        fact_after=after,
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_TAG_MODIFIED


def test_tag_removed_without_signed_ledger_fails() -> None:
    """RT-04 verbatim closure path."""
    before = _fact(required_for_funder=["USDA-VAPG"])
    after = _fact(required_for_funder=[])
    r = check_kfr_tag_modified(
        fact_id="F1",
        fact_before=before,
        fact_after=after,
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_TAG_MODIFIED


def test_tag_modification_with_signed_ledger_passes() -> None:
    before = _fact(required_for_funder=["USDA-VAPG"])
    after = _fact(required_for_funder=["USDA-VAPG", "USDA-RD"])
    hash_before = compute_tag_set_hash(before).hex()
    hash_after = compute_tag_set_hash(after).hex()
    ledger = [
        {
            "ledger_kind": LEDGER_KIND_TAG_MODIFIED,
            "fact_id": "F1",
            "tag_set_hash_before": hash_before,
            "tag_set_hash_after": hash_after,
            "operator_key_id": "op1",
            "signed_at_utc": "2026-05-10T00:00:00Z",
            "rationale": "operator added USDA-RD funder",
        },
    ]
    r = check_kfr_tag_modified(
        fact_id="F1",
        fact_before=before,
        fact_after=after,
        ledger_entries=ledger,
    )
    assert r.success is True


def test_reordered_tag_list_does_not_trigger_when_set_unchanged() -> None:
    """Order shouldn't matter — sorted under the hood."""
    before = _fact(required_for_funder=["USDA-VAPG", "USDA-RD"])
    after = _fact(required_for_funder=["USDA-RD", "USDA-VAPG"])
    r = check_kfr_tag_modified(
        fact_id="F1",
        fact_before=before,
        fact_after=after,
        ledger_entries=[],
    )
    assert r.success is True


def test_key_credentials_added_fails_without_ledger() -> None:
    before = _fact()
    after = _fact(key_credentials={"ein": "12-3456789"})
    r = check_kfr_tag_modified(
        fact_id="F1",
        fact_before=before,
        fact_after=after,
        ledger_entries=[],
    )
    assert r.success is False


def test_compute_tag_set_hash_deterministic() -> None:
    h1 = compute_tag_set_hash(_fact(required_for_funder=["A", "B"]))
    h2 = compute_tag_set_hash(_fact(required_for_funder=["B", "A"]))
    assert h1 == h2  # sort discipline


def test_compute_tag_set_hash_different_for_different_sets() -> None:
    h1 = compute_tag_set_hash(_fact(required_for_funder=["A"]))
    h2 = compute_tag_set_hash(_fact(required_for_funder=["B"]))
    assert h1 != h2


def test_unsigned_ledger_row_does_not_authorize() -> None:
    before = _fact(required_for_funder=["USDA-VAPG"])
    after = _fact(required_for_funder=[])
    hash_before = compute_tag_set_hash(before).hex()
    hash_after = compute_tag_set_hash(after).hex()
    ledger = [
        {
            "ledger_kind": LEDGER_KIND_TAG_MODIFIED,
            "fact_id": "F1",
            "tag_set_hash_before": hash_before,
            "tag_set_hash_after": hash_after,
            "operator_key_id": "",  # missing operator
            "signed_at_utc": "2026-05-10T00:00:00Z",
            "rationale": "ratio",
        },
    ]
    r = check_kfr_tag_modified(
        fact_id="F1",
        fact_before=before,
        fact_after=after,
        ledger_entries=ledger,
    )
    assert r.success is False
