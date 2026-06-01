"""Coefficient Registry schema + signature + load_active tests. [§2.14]"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.vault.sub_kinds.coefficient_registry import (
    CoefficientEntry,
    CoefficientRegistry,
    CoefficientRegistryUnreadableError,
    CoefficientRegistryUnsignedError,
    CoefficientSchemaInvalidError,
    CoefficientSignatureInvalidError,
    load_active,
    to_canonical_bytes,
    to_signing_payload,
)


def _make_entry(*, model_id: str = "claude-sonnet-4-6", is_local: bool = False) -> CoefficientEntry:
    return CoefficientEntry(
        model_id=model_id,
        is_local=is_local,
        hardware_sku="apple_m3_ultra" if is_local else None,
        dollars_per_million_input_tokens_minor_units=300,
        dollars_per_million_output_tokens_minor_units=1500,
        watt_hours_per_million_input_tokens_micro=400000,
        watt_hours_per_million_output_tokens_micro=800000,
        idle_watts_baseline_micro=10000000 if is_local else None,
        peak_watts_under_load_micro=200000000 if is_local else None,
        citation_url="https://example.com/cite",
        measurement_date="2026-07-01",
        measurement_methodology_url="https://example.com/methodology",
    )


def _make_registry(*, signature_hex: str = "a" * 128) -> CoefficientRegistry:
    return CoefficientRegistry(
        schema_version="1.0.0",
        quarter="Q3-2026",
        published_at="2026-07-01T00:00:00Z",
        sn_llc_signature_ed25519=signature_hex,
        sn_llc_signing_key_id="sn-llc-2026-q3",
        baseline_model_id="claude-sonnet-4-6",
        entries=(_make_entry(),),
        methodology_url="https://example.com/wpfa-method",
        rollback_pointer=None,
    )


class TestEntryInvariants:
    def test_local_requires_hardware_sku(self) -> None:
        with pytest.raises(ValueError, match="hardware_sku"):
            CoefficientEntry(
                model_id="local",
                is_local=True,
                hardware_sku=None,
                dollars_per_million_input_tokens_minor_units=0,
                dollars_per_million_output_tokens_minor_units=0,
                watt_hours_per_million_input_tokens_micro=0,
                watt_hours_per_million_output_tokens_micro=0,
                idle_watts_baseline_micro=0,
                peak_watts_under_load_micro=0,
                citation_url="https://example.com/c",
                measurement_date="2026-07-01",
                measurement_methodology_url="https://example.com/m",
            )

    def test_cloud_rejects_hardware_sku(self) -> None:
        with pytest.raises(ValueError, match="hardware_sku=None"):
            CoefficientEntry(
                model_id="cloud",
                is_local=False,
                hardware_sku="apple_m3_ultra",
                dollars_per_million_input_tokens_minor_units=0,
                dollars_per_million_output_tokens_minor_units=0,
                watt_hours_per_million_input_tokens_micro=0,
                watt_hours_per_million_output_tokens_micro=0,
                idle_watts_baseline_micro=None,
                peak_watts_under_load_micro=None,
                citation_url="https://example.com/c",
                measurement_date="2026-07-01",
                measurement_methodology_url="https://example.com/m",
            )

    def test_negative_coefficients_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-negative int"):
            CoefficientEntry(
                model_id="m",
                is_local=False,
                hardware_sku=None,
                dollars_per_million_input_tokens_minor_units=-1,
                dollars_per_million_output_tokens_minor_units=0,
                watt_hours_per_million_input_tokens_micro=0,
                watt_hours_per_million_output_tokens_micro=0,
                idle_watts_baseline_micro=None,
                peak_watts_under_load_micro=None,
                citation_url="https://example.com/c",
                measurement_date="2026-07-01",
                measurement_methodology_url="https://example.com/m",
            )

    def test_date_only_format(self) -> None:
        with pytest.raises(ValueError, match="measurement_date"):
            CoefficientEntry(
                model_id="m",
                is_local=False,
                hardware_sku=None,
                dollars_per_million_input_tokens_minor_units=0,
                dollars_per_million_output_tokens_minor_units=0,
                watt_hours_per_million_input_tokens_micro=0,
                watt_hours_per_million_output_tokens_micro=0,
                idle_watts_baseline_micro=None,
                peak_watts_under_load_micro=None,
                citation_url="https://example.com/c",
                measurement_date="2026-07-01T00:00:00Z",  # too detailed
                measurement_methodology_url="https://example.com/m",
            )


class TestRegistryInvariants:
    def test_minimal_valid_registry(self) -> None:
        r = _make_registry()
        assert r.baseline_model_id == "claude-sonnet-4-6"

    def test_baseline_must_resolve_in_entries(self) -> None:
        with pytest.raises(ValueError, match="must resolve"):
            CoefficientRegistry(
                schema_version="1.0.0",
                quarter="Q3-2026",
                published_at="2026-07-01T00:00:00Z",
                sn_llc_signature_ed25519="a" * 128,
                sn_llc_signing_key_id="k",
                baseline_model_id="missing-baseline",
                entries=(_make_entry(),),
                methodology_url="https://example.com/m",
                rollback_pointer=None,
            )

    def test_duplicate_model_id_rejected(self) -> None:
        with pytest.raises(ValueError, match="duplicate model_id"):
            CoefficientRegistry(
                schema_version="1.0.0",
                quarter="Q3-2026",
                published_at="2026-07-01T00:00:00Z",
                sn_llc_signature_ed25519="a" * 128,
                sn_llc_signing_key_id="k",
                baseline_model_id="claude-sonnet-4-6",
                entries=(_make_entry(), _make_entry()),
                methodology_url="https://example.com/m",
                rollback_pointer=None,
            )

    def test_lookup_resolves(self) -> None:
        r = _make_registry()
        assert r.lookup("claude-sonnet-4-6") is not None
        assert r.lookup("nope") is None


class TestSigningPayloadDeterminism:
    def test_signing_payload_excludes_signature(self) -> None:
        r = _make_registry()
        payload = to_signing_payload(r)
        assert b"sn_llc_signature_ed25519" not in payload

    def test_signing_payload_sorted_keys(self) -> None:
        r = _make_registry()
        payload = to_signing_payload(r).decode("utf-8")
        d = json.loads(payload)
        # JSON object key order is preserved by json.loads in Python 3.7+
        # but the canonical bytes must be sorted-key. Reserialize and compare.
        resorted = json.dumps(d, sort_keys=True, separators=(",", ":"))
        assert resorted == payload

    def test_canonical_bytes_includes_signature(self) -> None:
        r = _make_registry()
        full = to_canonical_bytes(r)
        assert b"sn_llc_signature_ed25519" in full


class _StubVerifier:
    def __init__(self, *, returns: object) -> None:
        self.returns = returns
        self.calls: list[tuple[bytes, bytes, bytes]] = []

    def __call__(
        self, message_bytes: bytes, signature: bytes, public_key: bytes
    ) -> bool:
        self.calls.append((message_bytes, signature, public_key))
        if isinstance(self.returns, Exception):
            raise self.returns
        return bool(self.returns) if self.returns is not True else True


class TestLoadActive:
    def _write_yaml(self, tmp_path: Path, payload: dict) -> Path:
        p = tmp_path / "active.yaml"
        p.write_bytes(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        )
        return p

    def _full_payload(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "quarter": "Q3-2026",
            "published_at": "2026-07-01T00:00:00Z",
            "sn_llc_signature_ed25519": "a" * 128,
            "sn_llc_signing_key_id": "k",
            "baseline_model_id": "claude-sonnet-4-6",
            "entries": [
                {
                    "model_id": "claude-sonnet-4-6",
                    "is_local": False,
                    "hardware_sku": None,
                    "dollars_per_million_input_tokens_minor_units": 300,
                    "dollars_per_million_output_tokens_minor_units": 1500,
                    "watt_hours_per_million_input_tokens_micro": 400000,
                    "watt_hours_per_million_output_tokens_micro": 800000,
                    "idle_watts_baseline_micro": None,
                    "peak_watts_under_load_micro": None,
                    "citation_url": "https://example.com/c",
                    "measurement_date": "2026-07-01",
                    "measurement_methodology_url": "https://example.com/m",
                },
            ],
            "methodology_url": "https://example.com/wpfa",
            "rollback_pointer": None,
        }

    def test_load_active_happy_path(self, tmp_path: Path) -> None:
        path = self._write_yaml(tmp_path, self._full_payload())
        verifier = _StubVerifier(returns=True)
        r = load_active(
            registry_path=path,
            pinned_pubkey_hex="b" * 64,
            signature_verify=verifier,
        )
        assert isinstance(r, CoefficientRegistry)
        assert len(verifier.calls) == 1

    def test_load_active_unreadable(self, tmp_path: Path) -> None:
        with pytest.raises(CoefficientRegistryUnreadableError):
            load_active(
                registry_path=tmp_path / "does-not-exist.yaml",
                pinned_pubkey_hex="b" * 64,
                signature_verify=_StubVerifier(returns=True),
            )

    def test_load_active_unsigned(self, tmp_path: Path) -> None:
        payload = self._full_payload()
        payload["sn_llc_signature_ed25519"] = ""
        path = self._write_yaml(tmp_path, payload)
        with pytest.raises(CoefficientRegistryUnsignedError):
            load_active(
                registry_path=path,
                pinned_pubkey_hex="b" * 64,
                signature_verify=_StubVerifier(returns=True),
            )

    def test_load_active_signature_invalid(self, tmp_path: Path) -> None:
        path = self._write_yaml(tmp_path, self._full_payload())
        with pytest.raises(CoefficientSignatureInvalidError) as excinfo:
            load_active(
                registry_path=path,
                pinned_pubkey_hex="b" * 64,
                signature_verify=_StubVerifier(returns=False),
            )
        assert excinfo.value.sub_tag in {
            "pubkey_mismatch",
            "signature_bytes_invalid",
            "canonical_json_mismatch",
        }

    def test_load_active_verifier_raises_fail_closed(self, tmp_path: Path) -> None:
        path = self._write_yaml(tmp_path, self._full_payload())
        verifier = _StubVerifier(returns=RuntimeError("boom"))
        with pytest.raises(CoefficientSignatureInvalidError) as excinfo:
            load_active(
                registry_path=path,
                pinned_pubkey_hex="b" * 64,
                signature_verify=verifier,
            )
        assert "RuntimeError" in str(excinfo.value)

    def test_load_active_rejects_wrong_pubkey_length(self, tmp_path: Path) -> None:
        path = self._write_yaml(tmp_path, self._full_payload())
        with pytest.raises(CoefficientSignatureInvalidError) as excinfo:
            load_active(
                registry_path=path,
                pinned_pubkey_hex="b" * 32,  # too short
                signature_verify=_StubVerifier(returns=True),
            )
        assert excinfo.value.sub_tag == "pubkey_mismatch"

    def test_load_active_schema_invalid_top_level(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.yaml"
        path.write_bytes(b"[1,2,3]")  # array, not object
        with pytest.raises(CoefficientSchemaInvalidError):
            load_active(
                registry_path=path,
                pinned_pubkey_hex="b" * 64,
                signature_verify=_StubVerifier(returns=True),
            )
