"""F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID tests (M1 §5.2.3)."""

from __future__ import annotations

import base64

from pipeline.logician.benchmarks.seeding_allowlist_loader import (
    canonical_allowlist_payload,
)
from pipeline.logician.gates.f_benchmark_seeding_allowlist_signature_invalid import (
    F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID,
    check_benchmark_seeding_allowlist_signature_invalid,
)


def _allowlist_yaml(*, key_id: str = "op1", sig_b64: str = "AAAA") -> bytes:
    return (
        b"schema_version: benchmark_seeding_allowlist.v1\n"
        b"canonicalization: kfr_canonical.v1\n"
        b"populated_by: op1\n"
        b'populated_at: "2026-05-10T00:00:00Z"\n'
        b"allowed_source_domains: ['*.usda.gov']\n"
        b"allowed_source_path_prefixes: ['vault_shared/funder_intelligence/docs/']\n"
        b"forbidden_source_path_prefixes: ['orgs/']\n"
        b"audit_chain: ['initial']\n"
        + f'signature_ed25519: "{sig_b64}"\n'.encode()
        + f'signature_key_id: "{key_id}"\n'.encode()
    )


def test_failure_code_constant() -> None:
    assert (
        F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID
        == "F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID"
    )


def test_signature_verifies_passes() -> None:
    raw = _allowlist_yaml()

    # Compute the canonical-JSON the loader would build (everything
    # except signature_*).  The fake verifier accepts iff the payload
    # bytes match.
    import yaml
    parsed = yaml.safe_load(raw)
    expected_payload = canonical_allowlist_payload(parsed)

    def verifier(message: bytes, signature: bytes, public_key: bytes) -> bool:
        del signature, public_key
        return message == expected_payload

    r = check_benchmark_seeding_allowlist_signature_invalid(
        raw_bytes=raw,
        operator_public_key=b"pk",
        expected_key_id="op1",
        signature_verify=verifier,
    )
    assert r.success is True


def test_signature_verification_fails() -> None:
    def verifier(message: bytes, signature: bytes, public_key: bytes) -> bool:
        return False

    r = check_benchmark_seeding_allowlist_signature_invalid(
        raw_bytes=_allowlist_yaml(),
        operator_public_key=b"pk",
        expected_key_id="op1",
        signature_verify=verifier,
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID


def test_key_id_mismatch_fails() -> None:
    def verifier(*_: object) -> bool:
        return True

    r = check_benchmark_seeding_allowlist_signature_invalid(
        raw_bytes=_allowlist_yaml(key_id="op1"),
        operator_public_key=b"pk",
        expected_key_id="op2",
        signature_verify=verifier,
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID


def test_anchor_in_yaml_fails() -> None:
    bad = (
        b"schema_version: &foo bar\n"
        b"canonicalization: *foo\n"
        b"signature_ed25519: AAAA\n"
        b"signature_key_id: op1\n"
    )

    def verifier(*_: object) -> bool:
        return True

    r = check_benchmark_seeding_allowlist_signature_invalid(
        raw_bytes=bad,
        operator_public_key=b"pk",
        expected_key_id="op1",
        signature_verify=verifier,
    )
    assert r.success is False


def test_invalid_base64_signature_fails() -> None:
    raw = _allowlist_yaml(sig_b64="not!valid_base64_string")

    def verifier(*_: object) -> bool:
        return True

    r = check_benchmark_seeding_allowlist_signature_invalid(
        raw_bytes=raw,
        operator_public_key=b"pk",
        expected_key_id="op1",
        signature_verify=verifier,
    )
    assert r.success is False


def test_rt10_extra_org_slug_key_rejected() -> None:
    # RT-10 closure (Cycle 1, 2026-05-10): an attacker (or a careless
    # operator) cannot smuggle an `org_slug` (or any other extra key)
    # through the allowlist YAML. Defense-in-depth against per-org
    # content leakage via fields the loader would otherwise silently
    # ignore.
    bad = (
        b"schema_version: benchmark_seeding_allowlist.v1\n"
        b"canonicalization: kfr_canonical.v1\n"
        b"populated_by: op1\n"
        b'populated_at: "2026-05-10T00:00:00Z"\n'
        b"allowed_source_domains: ['*.usda.gov']\n"
        b"allowed_source_path_prefixes: ['vault_shared/funder_intelligence/docs/']\n"
        b"forbidden_source_path_prefixes: ['orgs/']\n"
        b"audit_chain: ['initial']\n"
        b"org_slug: mycosymbiotics_cooperative\n"  # FORBIDDEN extra key
        b'signature_ed25519: "AAAA"\n'
        b'signature_key_id: "op1"\n'
    )

    def verifier(*_: object) -> bool:
        return True

    r = check_benchmark_seeding_allowlist_signature_invalid(
        raw_bytes=bad,
        operator_public_key=b"pk",
        expected_key_id="op1",
        signature_verify=verifier,
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID


def test_rt10_extra_who_field_rejected() -> None:
    # RT-10 closure: any per-org-identifying field (who, what, fact_id,
    # ein, uei) similarly fails-closed at the load step.
    bad = (
        b"schema_version: benchmark_seeding_allowlist.v1\n"
        b"canonicalization: kfr_canonical.v1\n"
        b"populated_by: op1\n"
        b'populated_at: "2026-05-10T00:00:00Z"\n'
        b"allowed_source_domains: ['*.usda.gov']\n"
        b"allowed_source_path_prefixes: ['vault_shared/funder_intelligence/docs/']\n"
        b"forbidden_source_path_prefixes: ['orgs/']\n"
        b"audit_chain: []\n"
        b'who: "Josh Inklovich"\n'  # FORBIDDEN extra key
        b'signature_ed25519: "AAAA"\n'
        b'signature_key_id: "op1"\n'
    )

    def verifier(*_: object) -> bool:
        return True

    r = check_benchmark_seeding_allowlist_signature_invalid(
        raw_bytes=bad,
        operator_public_key=b"pk",
        expected_key_id="op1",
        signature_verify=verifier,
    )
    assert r.success is False
