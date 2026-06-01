"""§13.8.7 — state-rules card substrate tests.

Covers:
- Round-trip authoring + loading with Ed25519 signature (RT-21 closure).
- Tampered card fails signature verify.
- Wrong public key fails.
- Unsupported state code rejected (v0.2 first wave: PA/CA/FL/TX/NY).
- Opt-in record loading.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from pipeline.orchestrator.seats.data_collector import StateRulesCardEntry
from pipeline.orchestrator.seats.data_collector.state_rules_card import (
    SUPPORTED_STATES,
    StateCardNotFound,
    StateCardSignatureError,
    StateCardStateUnsupported,
    author_card_yaml,
    load_opted_in_states,
    load_state_card,
    verify_card_signature,
)


def _gen_keypair():
    sk = Ed25519PrivateKey.generate()
    pk = sk.public_key().public_bytes_raw()
    return sk, pk


def _entry_for(state_code: str, *, version: str = "v1.0.0") -> StateRulesCardEntry:
    return StateRulesCardEntry(
        state_code=state_code,  # type: ignore[arg-type]
        email_disclaimers=[{"text": f"{state_code} CAN-SPAM addendum"}],
        sms_quiet_hours=("07:00", "21:00"),
        sms_required_opt_out_shortcodes=["STOP", "UNSUBSCRIBE"],
        sms_minimum_consent_age_days=0,
        voice_quiet_hours=("08:00", "21:00"),
        voice_automated_call_disclosure_script=f"{state_code} state automated message disclosure",
        voice_state_dnc_check_required=False,
        whatsapp_disclaimers=[{"text": f"{state_code} WhatsApp addendum"}],
        card_version=version,
        signed_by_sn_llc_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        signed_by_sn_llc_pubkey_fingerprint="sha256:" + "0" * 64,
        signature=b"\x00",  # overwritten by author_card_yaml
    )


def _write_card(dirpath: Path, state_code: str, sk: Ed25519PrivateKey) -> Path:
    entry = _entry_for(state_code)
    payload = author_card_yaml(entry, sn_llc_signing_key=sk)
    path = Path(dirpath) / f"{state_code}.yaml"
    with open(path, "w") as fp:
        yaml.safe_dump(payload, fp)
    return path


def test_load_pa_card_roundtrip(tmp_path):
    sk, pk = _gen_keypair()
    _write_card(tmp_path, "PA", sk)
    entry = load_state_card(tmp_path, "PA", sn_llc_pubkey=pk)
    assert entry.state_code == "PA"
    assert entry.sms_quiet_hours == ("07:00", "21:00")


def test_load_all_five_first_wave_states(tmp_path):
    sk, pk = _gen_keypair()
    for state in SUPPORTED_STATES:
        _write_card(tmp_path, state, sk)
    for state in SUPPORTED_STATES:
        entry = load_state_card(tmp_path, state, sn_llc_pubkey=pk)
        assert entry.state_code == state


def test_unsupported_state_rejected(tmp_path):
    _, pk = _gen_keypair()
    with pytest.raises(StateCardStateUnsupported):
        load_state_card(tmp_path, "MA", sn_llc_pubkey=pk)


def test_missing_card_file_raises(tmp_path):
    _, pk = _gen_keypair()
    with pytest.raises(StateCardNotFound):
        load_state_card(tmp_path, "PA", sn_llc_pubkey=pk)


def test_wrong_pubkey_fails_verify(tmp_path):
    sk, _ = _gen_keypair()
    _write_card(tmp_path, "PA", sk)
    _, wrong_pk = _gen_keypair()
    with pytest.raises(StateCardSignatureError):
        load_state_card(tmp_path, "PA", sn_llc_pubkey=wrong_pk)


def test_tampered_card_fails_verify(tmp_path):
    sk, pk = _gen_keypair()
    path = _write_card(tmp_path, "PA", sk)
    # Tamper: rewrite content WITHOUT updating signature.
    with open(path, "rb") as fp:
        data = yaml.safe_load(fp)
    data["sms_quiet_hours"] = ["00:00", "23:59"]
    with open(path, "w") as fp:
        yaml.safe_dump(data, fp)
    with pytest.raises(StateCardSignatureError):
        load_state_card(tmp_path, "PA", sn_llc_pubkey=pk)


def test_missing_signature_field_rejected(tmp_path):
    _, pk = _gen_keypair()
    path = tmp_path / "PA.yaml"
    with open(path, "w") as fp:
        yaml.safe_dump({"state_code": "PA"}, fp)
    with pytest.raises(StateCardSignatureError):
        load_state_card(tmp_path, "PA", sn_llc_pubkey=pk)


def test_load_opted_in_states_empty(tmp_path):
    # Missing file → empty set.
    assert load_opted_in_states(tmp_path / "state_rules_opt_ins.signed.yaml") == frozenset()


def test_load_opted_in_states_returns_uppercase(tmp_path):
    path = tmp_path / "state_rules_opt_ins.signed.yaml"
    with open(path, "w") as fp:
        yaml.safe_dump({"opted_in_states": ["pa", "ca", "ny"]}, fp)
    assert load_opted_in_states(path) == {"PA", "CA", "NY"}


def test_supported_states_v0_2_first_wave():
    assert SUPPORTED_STATES == ("PA", "CA", "FL", "TX", "NY")
