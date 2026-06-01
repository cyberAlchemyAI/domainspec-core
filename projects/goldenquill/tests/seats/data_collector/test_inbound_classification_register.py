"""§13.9.6 + RT-C2-11 — inbound classification register substrate tests."""
from __future__ import annotations

import base64
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from pipeline.orchestrator.seats.data_collector.inbound_classification_register import (
    CLASSIFICATION_STATUS_DEFAULT_CONFIDENTIAL_PENDING_REVIEW,
    CLASSIFICATION_STATUS_OPERATOR_CLASSIFIED,
    ClassificationEntry,
    ClassificationRegisterNotFound,
    ClassificationRegisterSignatureError,
    load_classification_register,
    lookup_classification,
    write_classification_register,
)


def _gen():
    sk = Ed25519PrivateKey.generate()
    pk = sk.public_key().public_bytes_raw()
    return sk, pk


def test_register_write_then_load_round_trip(tmp_path):
    sk, pk = _gen()
    entries = {
        ("recipient-X", "graduates_count"): ClassificationEntry(
            recipient_id="recipient-X",
            field_class="graduates_count",
            classification_status=CLASSIFICATION_STATUS_OPERATOR_CLASSIFIED,
            classification_value="Shareable",
            operator_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        ),
    }
    path = tmp_path / "classification_register.signed.yaml"
    write_classification_register(
        path,
        entries=entries,
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        operator_signing_key=sk,
    )
    loaded = load_classification_register(path, operator_pubkey=pk)
    looked_up = lookup_classification(loaded, "recipient-X", "graduates_count")
    assert looked_up is not None
    assert looked_up.classification_status == CLASSIFICATION_STATUS_OPERATOR_CLASSIFIED
    assert looked_up.classification_value == "Shareable"


def test_register_missing_raises(tmp_path):
    _, pk = _gen()
    with pytest.raises(ClassificationRegisterNotFound):
        load_classification_register(
            tmp_path / "missing.signed.yaml", operator_pubkey=pk,
        )


def test_register_wrong_pubkey_fails(tmp_path):
    sk, _ = _gen()
    _, wrong_pk = _gen()
    path = tmp_path / "classification_register.signed.yaml"
    write_classification_register(
        path,
        entries={},
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        operator_signing_key=sk,
    )
    with pytest.raises(ClassificationRegisterSignatureError):
        load_classification_register(path, operator_pubkey=wrong_pk)


def test_register_tampered_signature_fails(tmp_path):
    """RT-C2-11 — every read re-verifies signature; tampering caught."""
    sk, pk = _gen()
    path = tmp_path / "classification_register.signed.yaml"
    write_classification_register(
        path,
        entries={
            ("r1", "metric"): ClassificationEntry(
                recipient_id="r1",
                field_class="metric",
                classification_status=CLASSIFICATION_STATUS_OPERATOR_CLASSIFIED,
                classification_value="Public",
                operator_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
            ),
        },
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        operator_signing_key=sk,
    )
    # Tamper: rewrite without updating signature.
    with open(path) as fp:
        data = yaml.safe_load(fp)
    data["entries"]["r1::metric"]["classification_value"] = "Confidential"
    with open(path, "w") as fp:
        yaml.safe_dump(data, fp)
    with pytest.raises(ClassificationRegisterSignatureError):
        load_classification_register(path, operator_pubkey=pk)


def test_lookup_returns_none_for_missing_pair(tmp_path):
    sk, pk = _gen()
    path = tmp_path / "r.signed.yaml"
    write_classification_register(
        path, entries={},
        signed_at_utc=datetime(2026, 5, 10, tzinfo=timezone.utc),
        operator_signing_key=sk,
    )
    reg = load_classification_register(path, operator_pubkey=pk)
    assert lookup_classification(reg, "absent", "field") is None
