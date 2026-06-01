"""Adversarial tests for F-DEGRADATION-STANZA-PRECEDENCE (F-AMDT-11).

Covers the eight adversarial cases named by the spec card plus three
additional flavours that exercise the inline-literal precedence rule and
inline-literal architecture-file regex under rebind attempts.
"""

from __future__ import annotations

import re
from typing import Optional

import pytest

from pipeline.logician.gates import f_degradation_stanza_precedence as gate_mod
from pipeline.logician.gates.f_degradation_stanza_precedence import (
    EVENT_CARVEOUT_GRANTED,
    EVENT_KIND_PROMOTION,
    EVENT_KIND_STANZA,
    F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
    F_AMDT_11_READER_FAIL,
    check_degradation_stanza_precedence,
)


def _stanza(text: Optional[str]):
    def _r(date_iso: str) -> Optional[str]:
        return text

    return _r


class _Verifier:
    def __init__(self, *, result: object = True, raises: Optional[BaseException] = None,
                 accept_payload: Optional[bytes] = None):
        self._result = result
        self._raises = raises
        self._accept_payload = accept_payload
        self.calls = []

    def __call__(self, payload: bytes, signature: bytes, public_key: bytes) -> bool:
        self.calls.append((payload, signature, public_key))
        if self._raises is not None:
            raise self._raises
        if self._accept_payload is not None:
            return payload == self._accept_payload
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
# Spec-card adversarial cases
# ---------------------------------------------------------------------------


def test_adv_stanza_reader_raises_fail_closed():
    """Spec case 1 — stanza_reader raises → DENY fail-closed."""
    def raiser(date_iso: str) -> Optional[str]:
        raise OSError("boom")

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


def test_adv_signature_verify_raises_fail_closed():
    """Spec case 3 — signature_verify raises → DENY fail-closed."""
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="escalate",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(raises=Exception("hsm offline")),
        operator_public_key=b"pk",
        staged_row=_arch_row(),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_READER_FAIL
    assert r.detail.reason_tag == "signature_verify_raised"
    assert "Exception" in (r.detail.reader_error or "")


@pytest.mark.parametrize("code_path", [
    "pipeline/logician/gates/f_bootstrap_reuse.py",
    "pipeline/scout/channel_a_federal_apis.py",
    "pipeline/loop/seat_runner.py",
    "router.yaml",
    "pipeline/architecture/v0.1/notes.txt",
])
def test_adv_architectural_thesis_claim_but_code_path(code_path):
    """Spec case 4 — lock_class='architectural_thesis' but module_path points at
    code or non-architecture asset → path check catches → carveout-violation."""
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
        staged_row=_arch_row(module_path=code_path),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
    assert r.detail.reason_tag == "module_path_not_architecture_file"


def test_adv_signature_valid_but_for_different_row_bytes():
    """Spec case 5 — adversary replays a signature valid over different row
    bytes. Verifier returns False for our bytes → carveout-violation."""
    canonical_bytes = b"the-actual-row-the-operator-signed"
    adversary_bytes = b"the-bytes-the-adversary-staged"

    verifier = _Verifier(accept_payload=canonical_bytes)
    row = _arch_row(signed_row_bytes=adversary_bytes, operator_signature=b"op-sig")

    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="escalate",
        stanza_reader=_stanza(None),
        signature_verify=verifier,
        operator_public_key=b"operator-pk",
        staged_row=row,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
    assert r.detail.reason_tag == "signature_verify_returned_false"
    assert verifier.calls == [(adversary_bytes, b"op-sig", b"operator-pk")]


def test_adv_precedence_rule_rebind_attempt_has_no_effect():
    """Spec case 6 — attempt to rebind the precedence enumeration at module
    scope must not change the gate's behaviour (inline-literal defence).

    We overwrite *any* plausible module-level name the adversary might hope
    enables a bypass, then verify the gate still applies FRESH>TARGET."""
    sentinels_before = {k: getattr(gate_mod, k, None) for k in [
        "FRESH_ARCHITECTURAL_THESIS", "TARGET_DATE", "_FRESH_TOKEN",
        "_TARGET_TOKEN", "_PRECEDENCE", "PRECEDENCE_RULE",
    ]}

    setattr(gate_mod, "FRESH_ARCHITECTURAL_THESIS", "XXX_FAKE_TOKEN_XXX")
    setattr(gate_mod, "TARGET_DATE", "YYY_FAKE_TOKEN_YYY")
    setattr(gate_mod, "_PRECEDENCE", ("TARGET_DATE", "FRESH_ARCHITECTURAL_THESIS"))
    try:
        # Stanza contains the canonical tokens — inline literals must still win.
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
    finally:
        # Restore module state so later tests see pristine namespace.
        for k, v in sentinels_before.items():
            if v is None:
                if hasattr(gate_mod, k):
                    delattr(gate_mod, k)
            else:
                setattr(gate_mod, k, v)


def test_adv_architecture_path_regex_rebind_at_module_load_has_no_effect():
    """Spec case 7 — rebind any plausible module-level regex constant must
    not change what the gate accepts / rejects as architecture paths."""
    setattr(gate_mod, "_ARCHITECTURE_PATH_REGEX", re.compile(r".*"))
    setattr(gate_mod, "ARCHITECTURE_PATH_REGEX", re.compile(r".*"))
    setattr(gate_mod, "_ARCH_PATH_PATTERN", r".*")
    try:
        # A definitively-not-architecture path must still be rejected.
        r = check_degradation_stanza_precedence(
            event_kind=EVENT_KIND_PROMOTION,
            today_iso="2026-04-21",
            f_amdt_08_tier="suspend",
            stanza_reader=_stanza(None),
            signature_verify=_Verifier(),
            operator_public_key=b"pk",
            staged_row=_arch_row(module_path="pipeline/scout/channel_a_federal_apis.py"),
        )
        assert r.success is False
        assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
        assert r.detail.reason_tag == "module_path_not_architecture_file"

        # And the canonical architecture path is still accepted.
        r2 = check_degradation_stanza_precedence(
            event_kind=EVENT_KIND_PROMOTION,
            today_iso="2026-04-21",
            f_amdt_08_tier="suspend",
            stanza_reader=_stanza(None),
            signature_verify=_Verifier(result=True),
            operator_public_key=b"pk",
            staged_row=_arch_row(),
        )
        assert r2.success is True
        assert r2.detail.emitted_event == EVENT_CARVEOUT_GRANTED
    finally:
        for k in ("_ARCHITECTURE_PATH_REGEX", "ARCHITECTURE_PATH_REGEX", "_ARCH_PATH_PATTERN"):
            if hasattr(gate_mod, k):
                delattr(gate_mod, k)


def test_adv_stanza_has_both_with_malformed_target_date_passes_fresh_wins():
    """Spec case 8 — stanza contains FRESH_ARCHITECTURAL_THESIS AND a
    malformed TARGET_DATE (numeric nonsense). Gate only tokenises presence
    of ``TARGET_DATE:`` token; malformed date is irrelevant because the
    mixed-event rule ignores TARGET_DATE when FRESH wins.

    Expected: PASS, has_fresh=True, has_target=True, emitted_event=MIXED."""
    text = (
        "Operator sign-off:\n"
        "  TARGET_DATE: 99-XYZ-foo-not-a-date\n"
        "  FRESH_ARCHITECTURAL_THESIS: round-4-approved.\n"
    )
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


# ---------------------------------------------------------------------------
# Additional adversarial flavours (defence-in-depth)
# ---------------------------------------------------------------------------


def test_adv_code_lock_under_readonly_denied_even_with_valid_signature():
    """A code LOCK under SUSPEND must NOT be carved out even if the
    adversary provides a valid operator signature over its row bytes."""
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_PROMOTION,
        today_iso="2026-04-21",
        f_amdt_08_tier="suspend",
        stanza_reader=_stanza(None),
        signature_verify=_Verifier(result=True),
        operator_public_key=b"pk",
        staged_row=_arch_row(lock_class="code"),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
    assert r.detail.reason_tag == "lock_class_not_architectural_thesis"


def test_adv_stanza_token_substring_only_not_matched():
    """Adversary tries to sneak ``FRESH_ARCHITECTURAL_THES`` (missing final
    IS) hoping partial match counts. It does NOT — literal match required."""
    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="escalate",
        stanza_reader=_stanza("partial FRESH_ARCHITECTURAL_THES only"),
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "stanza_neither_directive_present"


def test_adv_path_traversal_above_architecture_dir_rejected():
    """``../`` path-traversal components must not bypass the anchored regex."""
    for p in [
        "../pipeline/architecture/v0.1/architecture_v7_1_amendment.md",
        "./pipeline/architecture/v0.1/architecture_v7_1_amendment.md",
        "/pipeline/architecture/v0.1/architecture_v7_1_amendment.md",
        "pipeline/architecture/v0.1/../v0.2/architecture_v8_amendment.md",
    ]:
        r = check_degradation_stanza_precedence(
            event_kind=EVENT_KIND_PROMOTION,
            today_iso="2026-04-21",
            f_amdt_08_tier="suspend",
            stanza_reader=_stanza(None),
            signature_verify=_Verifier(result=True),
            operator_public_key=b"pk",
            staged_row=_arch_row(module_path=p),
        )
        assert r.success is False, f"adversary path {p!r} unexpectedly accepted"
        assert r.failure_code == F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION
        assert r.detail.reason_tag == "module_path_not_architecture_file"


def test_adv_reader_error_clipped_at_500_chars():
    """Oversized exception text must be clipped to 500 chars."""
    huge_msg = "x" * 2000

    def raiser(date_iso: str) -> Optional[str]:
        raise RuntimeError(huge_msg)

    r = check_degradation_stanza_precedence(
        event_kind=EVENT_KIND_STANZA,
        today_iso="2026-04-21",
        f_amdt_08_tier="pass",
        stanza_reader=raiser,
        signature_verify=_Verifier(),
        operator_public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reader_error is not None
    # "stanza_reader: " (15) + clipped 500-char body = 515 max.
    assert len(r.detail.reader_error) <= 515
