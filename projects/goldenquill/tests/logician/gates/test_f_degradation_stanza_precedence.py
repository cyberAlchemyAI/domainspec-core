"""Unit tests for F-DEGRADATION-STANZA-PRECEDENCE (F-AMDT-11)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Optional

import pytest

from pipeline.logician.gates.f_degradation_stanza_precedence import (
    EVENT_CARVEOUT_GRANTED,
    EVENT_KIND_PROMOTION,
    EVENT_KIND_STANZA,
    EVENT_PRECEDENCE_MIXED,
    F_AMDT_11,
    F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
    F_AMDT_11_PRECEDENCE_EMPTY,
    F_AMDT_11_READER_FAIL,
    StanzaPrecedenceDetail,
    StanzaPrecedenceResult,
    check_degradation_stanza_precedence,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stanza(text: Optional[str]):
    def _r(date_iso: str) -> Optional[str]:
        return text

    return _r


class _Verifier:
    def __init__(self, *, result: object = True, raises: Optional[BaseException] = None):
        self._result = result
        self._raises = raises
        self.calls = []

    def __call__(self, payload: bytes, signature: bytes, public_key: bytes) -> bool:
        self.calls.append((payload, signature, public_key))
        if self._raises is not None:
            raise self._raises
        return self._result  # type: ignore[return-value]


def _arch_row(
    *,
    lock_class: str = "architectural_thesis",
    module_path: str = "pipeline/architecture/v0.1/architecture_v7_1_amendment.md",
    signed_row_bytes: bytes = b"canonical-row-bytes",
    operator_signature: bytes = b"sig",
) -> dict:
    return {
        "lock_class": lock_class,
        "module_path": module_path,
        "signed_row_bytes": signed_row_bytes,
        "operator_signature": operator_signature,
    }


# ---------------------------------------------------------------------------
# Tooth (a) — stanza precedence
# ---------------------------------------------------------------------------


def test_stanza_absent_no_op_pass():
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="pass",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is True
    assert r.detail.event_kind == EVENT_KIND_STANZA
    assert r.detail.reason_tag == "stanza_absent_no_op"
    assert r.detail.emitted_event == ""


def test_stanza_only_fresh_passes():
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="escalate",
        stanza_reader=_stanza("Operator sign-off: FRESH_ARCHITECTURAL_THESIS now."),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is True
    assert r.detail.has_fresh is True
    assert r.detail.has_target is False
    assert r.detail.reason_tag == "stanza_fresh_architectural_thesis"
    assert r.detail.emitted_event == ""


def test_stanza_only_target_passes():
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza("Operator: TARGET_DATE: 2026-05-30"),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is True
    assert r.detail.has_target is True
    assert r.detail.has_fresh is False
    assert r.detail.reason_tag == "stanza_target_date_only"
    assert r.detail.emitted_event == ""


def test_stanza_both_passes_with_mixed_event():
    text = "TARGET_DATE: 2026-07-01\nFRESH_ARCHITECTURAL_THESIS: approved."
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="escalate",
        stanza_reader=_stanza(text),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is True
    assert r.detail.has_fresh is True
    assert r.detail.has_target is True
    assert r.detail.reason_tag == "stanza_both_fresh_wins"
    assert r.detail.emitted_event == EVENT_PRECEDENCE_MIXED


def test_stanza_neither_fails_empty():
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza("Operator acknowledges; escalation pending."),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_PRECEDENCE_EMPTY
    assert r.detail.reason_tag == "stanza_neither_directive_present"


def test_stanza_fresh_with_surrounding_prose_still_passes():
    text = "Long preamble... FRESH_ARCHITECTURAL_THESIS ... more text, signed by operator."
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="escalate",
        stanza_reader=_stanza(text),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is True
    assert r.detail.has_fresh is True


@pytest.mark.parametrize("target_date_format", [
    "TARGET_DATE: 2026-06-15",
    "TARGET_DATE: 2027-01-01",
    "TARGET_DATE: 2030-12-31",
])
def test_stanza_target_date_various_formats_only_checks_token_presence(target_date_format):
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(f"Stanza:\n{target_date_format}"),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is True
    assert r.detail.has_target is True


def test_stanza_case_sensitive_fresh_token_not_matched():
    # Gate uses exact string match — lowercase variant should NOT match.
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="escalate",
        stanza_reader=_stanza("fresh_architectural_thesis present"),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_PRECEDENCE_EMPTY


def test_stanza_target_date_without_colon_not_recognised():
    # Token includes the colon; "TARGET_DATE 2026-06-15" (no colon) should NOT match.
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza("TARGET_DATE 2026-06-15"),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False


def test_stanza_reader_raises_fail_closed():
    def raiser(date_iso: str) -> Optional[str]:
        raise OSError("daily log unreadable")

    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="pass",
        stanza_reader=raiser,
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_READER_FAIL
    assert r.detail.reason_tag == "stanza_reader_raised"
    assert r.detail.reader_error is not None
    assert "stanza_reader:" in r.detail.reader_error
    assert "OSError" in r.detail.reader_error


@pytest.mark.parametrize("bad", [123, b"bytes", [1], {"x": 1}])
def test_stanza_reader_returns_non_str_non_none_fails(bad):
    def reader(date_iso: str):
        return bad

    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="pass",
        stanza_reader=reader,  # type: ignore[arg-type]
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_READER_FAIL
    assert r.detail.reason_tag == "stanza_reader_return_invalid"


# ---------------------------------------------------------------------------
# Tooth (b) — READ-ONLY carve-out
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("tier", ["pass", "warn"])
def test_promotion_tier_pass_or_warn_no_op_pass(tier):
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier=tier,
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=_arch_row(),
    )
    assert r.success is True
    assert r.detail.reason_tag == "tier_not_suspend_or_escalate_no_op"


@pytest.mark.parametrize("tier", ["suspend", "escalate"])
def test_promotion_architectural_thesis_with_valid_path_and_sig_passes(tier):
    verifier = _Verifier(result=True)
    row = _arch_row(
        module_path="pipeline/architecture/v0.1/tilth_architecture_locked_v8.md",
    )
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier=tier,
        stanza_reader=_stanza(None),
        signature_verify=verifier,
        operator_public_key=b"operator-pk",
        staged_row=row,
    )
    assert r.success is True
    assert r.detail.reason_tag == "carveout_granted"
    assert r.detail.emitted_event == EVENT_CARVEOUT_GRANTED
    assert r.detail.lock_class == "architectural_thesis"
    assert len(verifier.calls) == 1
    assert verifier.calls[0] == (b"canonical-row-bytes", b"sig", b"operator-pk")


@pytest.mark.parametrize("tier", ["suspend", "escalate"])
@pytest.mark.parametrize("lock_class", ["code", "vault", "", "unknown"])
def test_promotion_non_architectural_lock_class_denied_carveout(tier, lock_class):
    row = _arch_row(lock_class=lock_class)
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier=tier,
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=row,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
    assert r.detail.reason_tag == "lock_class_not_architectural_thesis"


def test_promotion_lock_class_missing_denies_carveout():
    row = {
        "module_path": "pipeline/architecture/v0.1/architecture_v7_1_amendment.md",
        "signed_row_bytes": b"b",
        "operator_signature": b"s",
    }
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=row,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
    assert r.detail.reason_tag == "lock_class_not_architectural_thesis"


@pytest.mark.parametrize("bad_path", [
    "pipeline/logician/gates/code.py",
    "pipeline/architecture/readme.md",
    "other/dir/architecture_v1_amendment.md",
    "pipeline/architecture/v0.1/readme.md",
    "pipeline/architecture/v/tilth_architecture_locked_v1.md",
    "pipeline/architecture/v0.1/tilth_architecture_locked_v8.txt",
    "pipeline/architecture/v0.1/architecture_amendment.md",
    "",
])
def test_promotion_architectural_thesis_wrong_path_denies_carveout(bad_path):
    row = _arch_row(module_path=bad_path)
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=row,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
    assert r.detail.reason_tag == "module_path_not_architecture_file"


@pytest.mark.parametrize("good_path", [
    "pipeline/architecture/v0.1/tilth_architecture_locked_v7.md",
    "pipeline/architecture/v0.1/tilth_architecture_locked_v7_1_amendment.md",
    "pipeline/architecture/v0.2/tilth_architecture_locked_v12.md",
    "pipeline/architecture/v1/tilth_architecture_locked_v100.md",
    "pipeline/architecture/v0.1/architecture_v7_1_amendment.md",
    "pipeline/architecture/v0.2/architecture_v8_amendment.md",
])
def test_promotion_architectural_thesis_valid_path_variants_pass(good_path):
    row = _arch_row(module_path=good_path)
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(result=True),
        operator_public_key=b"pk",
        staged_row=row,
    )
    assert r.success is True
    assert r.detail.reason_tag == "carveout_granted"


def test_promotion_module_path_not_str_denies_carveout():
    row = _arch_row()
    row["module_path"] = 123  # type: ignore[assignment]
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=row,
    )
    assert r.success is False
    assert r.detail.reason_tag == "module_path_not_str"


@pytest.mark.parametrize("bad", ["str", 123, None, [1]])
def test_promotion_signed_row_bytes_not_bytes_denies(bad):
    row = _arch_row()
    row["signed_row_bytes"] = bad  # type: ignore[assignment]
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=row,
    )
    assert r.success is False
    assert r.detail.reason_tag == "signed_row_bytes_not_bytes"


@pytest.mark.parametrize("bad", ["str", 123, None, [1]])
def test_promotion_operator_signature_not_bytes_denies(bad):
    row = _arch_row()
    row["operator_signature"] = bad  # type: ignore[assignment]
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=row,
    )
    assert r.success is False
    assert r.detail.reason_tag == "operator_signature_not_bytes"


def test_promotion_signature_verify_returns_false_denies_carveout():
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(result=False),
        operator_public_key=b"pk",
        staged_row=_arch_row(),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
    assert r.detail.reason_tag == "signature_verify_returned_false"


@pytest.mark.parametrize("truthy", [1, "true", "True", [True], (True,), {"ok": True}])
def test_promotion_signature_verify_truthy_non_True_denies(truthy):
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="escalate",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(result=truthy),
        operator_public_key=b"pk",
        staged_row=_arch_row(),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
    assert r.detail.reason_tag == "signature_verify_returned_false"


def test_promotion_signature_verify_raises_fail_closed():
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(raises=RuntimeError("crypto engine offline")),
        operator_public_key=b"pk",
        staged_row=_arch_row(),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_READER_FAIL
    assert r.detail.reason_tag == "signature_verify_raised"
    assert r.detail.reader_error is not None
    assert "signature_verify:" in r.detail.reader_error


@pytest.mark.parametrize("bad_row", ["str", 1, None, [1]])
def test_promotion_staged_row_not_dict_denies(bad_row):
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=bad_row,  # type: ignore[arg-type]
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_READER_FAIL
    assert r.detail.reason_tag == "staged_row_not_dict"


# ---------------------------------------------------------------------------
# Structural input validation (top-level)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_event", ["stanza", "promotion", "", "STANZA_CHECK", None, 1])
def test_invalid_event_kind_denies(bad_event):
    r = check_degradation_stanza_precedence(
        event_kind=bad_event,  # type: ignore[arg-type]
        today_iso="2026-04-21",
        f_amdt_08_tier="pass",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_READER_FAIL
    assert r.detail.reason_tag == "invalid_event_kind"


@pytest.mark.parametrize("bad", ["", None, 1, b"2026-04-21", [1]])
def test_invalid_today_iso_denies(bad):
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso=bad,  # type: ignore[arg-type]
        f_amdt_08_tier="pass",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "invalid_today_iso"


@pytest.mark.parametrize("bad", ["unknown", "", None, 1, "SUSPEND"])
def test_invalid_tier_denies(bad):
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier=bad,  # type: ignore[arg-type]
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "invalid_tier"


@pytest.mark.parametrize("bad_pk", [None, "str", 123, [1]])
def test_public_key_not_bytes_denies(bad_pk):
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="pass",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=bad_pk,  # type: ignore[arg-type]
    )
    assert r.success is False
    assert r.detail.reason_tag == "public_key_not_bytes"


# ---------------------------------------------------------------------------
# Frozen + constants
# ---------------------------------------------------------------------------


def test_result_and_detail_are_frozen():
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="pass",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    with pytest.raises(FrozenInstanceError):
        r.success = False  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        r.detail.reason_tag = "x"  # type: ignore[misc]


def test_failure_code_and_event_constants():
    assert F_AMDT_11 == "F-AMDT-11"
    assert F_AMDT_11_PRECEDENCE_EMPTY == "F-AMDT-11-PRECEDENCE-EMPTY"
    assert F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION == "F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION"
    assert F_AMDT_11_READER_FAIL == "F-AMDT-11-READER-FAIL"
    assert EVENT_PRECEDENCE_MIXED == "F-AMDT-11-PRECEDENCE-MIXED"
    assert EVENT_CARVEOUT_GRANTED == "F-AMDT-11-CARVEOUT-GRANTED"
    assert EVENT_KIND_STANZA == "stanza_check"
    assert EVENT_KIND_PROMOTION == "lock_promotion_under_readonly"
