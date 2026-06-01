"""Adversarial tests for F-ROUTER-INTEGRITY-MULTI-SOURCE (F-AMDT-10).

Target threat model: EN-003 Cycle 4 Red Team finding C4-NEW-02.

The in-repo pair rule (router.yaml co-commits with router_integrity.pinned.json)
is defeated by a single malicious commit touching both files. This gate adds
an out-of-repo HMAC-chained signed manifest as a third independent source.
These tests confirm the gate catches the attacks the third source is designed
to defeat, and that it fails closed under adversarial reader behaviour.
"""

from __future__ import annotations

from typing import Optional

import pytest

from pipeline.logician.gates.f_router_integrity_multi_source import (
    F_AMDT_10_CHAIN_BREAK,
    F_AMDT_10_EXTERNAL,
    F_AMDT_10_READER_FAIL,
    F_AMDT_10_SIGNATURE,
    check_router_integrity_multi_source,
)


def _hash_bytes(data: bytes) -> str:
    """Deterministic fake hash shared across adversarial tests."""

    return "".join(f"{b:02x}" for b in data)[:128] or "EMPTY_FILE_HASH"


def _router_reader(data: bytes):
    def _r() -> bytes:
        return data

    return _r


def _pinned_reader(hash_value: str):
    def _r() -> dict:
        return {"router_yaml_sha3_512": hash_value}

    return _r


def _manifest_reader(manifest: dict):
    def _r() -> dict:
        return manifest

    return _r


def _prior_reader(value: Optional[str]):
    def _r() -> Optional[str]:
        return value

    return _r


def _make_manifest(
    *,
    chain_head_hash: str,
    prior_chain_head_hash: str,
    signature: bytes = b"sig",
    signed_payload_bytes: bytes = b"payload",
) -> dict:
    return {
        "chain_head_hash": chain_head_hash,
        "prior_chain_head_hash": prior_chain_head_hash,
        "signature": signature,
        "signed_payload_bytes": signed_payload_bytes,
    }


# ---------------------------------------------------------------------------
# C4-NEW-02: the headline attack
# ---------------------------------------------------------------------------


def test_adv_c4_new_02_single_commit_mutates_router_and_pinned_denies_external():
    """Single malicious commit rewrites router.yaml + pinned.json consistently.

    In-repo pair check (source 1 vs source 2) passes because both files were
    rewritten together. The external manifest — held outside the repo and
    chained to prior rows — still reflects the *prior* live hash. The gate
    MUST catch this at the external check.
    """

    malicious_yaml = b"router: MALICIOUSLY REWRITTEN"
    malicious_hash = _hash_bytes(malicious_yaml)
    last_known_good_hash = _hash_bytes(b"router: original")
    assert malicious_hash != last_known_good_hash

    manifest = _make_manifest(
        chain_head_hash=last_known_good_hash,
        prior_chain_head_hash="prior-of-last-known-good",
    )

    def sig_verify(payload: bytes, signature: bytes, public_key: bytes) -> bool:
        return True

    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(malicious_yaml),
        pinned_hash_reader=_pinned_reader(malicious_hash),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader("prior-of-last-known-good"),
        signature_verify=sig_verify,
        hash_bytes=_hash_bytes,
        public_key=b"pk",
    )

    assert r.success is False
    assert r.failure_code == F_AMDT_10_EXTERNAL
    assert r.detail.check_failed == "external"
    assert r.detail.reason_tag == "manifest_chain_head_mismatches_live"
    assert r.detail.live_hash == malicious_hash
    assert r.detail.pinned_hash == malicious_hash
    assert r.detail.manifest_chain_head == last_known_good_hash


# ---------------------------------------------------------------------------
# C4-NEW-02 variant: attacker controls the manifest hash but not the key
# ---------------------------------------------------------------------------


def test_adv_signature_valid_but_for_different_manifest_denies_signature():
    """Adversary re-signs a crafted manifest with the wrong key.

    Attack: adversary obtained write access to the out-of-repo manifest path
    and inserted a fresh row with chain_head_hash == malicious live hash.
    Because the adversary does NOT hold the Ed25519 signing key, the
    injected signature fails verification. The strict ``is True`` check
    must reject.
    """

    malicious_yaml = b"router: malicious"
    malicious_hash = _hash_bytes(malicious_yaml)

    manifest = _make_manifest(
        chain_head_hash=malicious_hash,
        prior_chain_head_hash="prior",
        signature=b"forged-signature",
        signed_payload_bytes=b"forged-payload",
    )

    def sig_verify(payload: bytes, signature: bytes, public_key: bytes) -> bool:
        return False

    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(malicious_yaml),
        pinned_hash_reader=_pinned_reader(malicious_hash),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader("prior"),
        signature_verify=sig_verify,
        hash_bytes=_hash_bytes,
        public_key=b"operator-pk",
    )

    assert r.success is False
    assert r.failure_code == F_AMDT_10_SIGNATURE
    assert r.detail.check_failed == "signature"
    assert r.detail.reason_tag == "signature_verify_returned_false"


# ---------------------------------------------------------------------------
# C4-NEW-02 variant: attacker forges chain continuity to hide prior rows
# ---------------------------------------------------------------------------


def test_adv_chain_head_is_current_but_prior_chain_head_forged_denies_chain_break():
    """Adversary crafts chain_head valid, signature valid, but prior link lies.

    Attack: adversary can bypass both pair and signature checks but cannot
    rewrite history — prior_chain_head_reader reads the PRIOR row's authentic
    chain_head_hash from out-of-repo storage. A fabricated prior_chain_head_hash
    in the current manifest row exposes the splice.
    """

    yaml = b"router: current"
    live = _hash_bytes(yaml)

    manifest = _make_manifest(
        chain_head_hash=live,
        prior_chain_head_hash="FORGED-PRIOR-HASH",
    )

    def sig_verify(payload: bytes, signature: bytes, public_key: bytes) -> bool:
        return True

    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader("GENUINE-PRIOR-HASH"),
        signature_verify=sig_verify,
        hash_bytes=_hash_bytes,
        public_key=b"pk",
    )

    assert r.success is False
    assert r.failure_code == F_AMDT_10_CHAIN_BREAK
    assert r.detail.check_failed == "chain_break"
    assert r.detail.reason_tag == "prior_chain_head_hash_mismatches_prior_reader"


# ---------------------------------------------------------------------------
# Fail-closed: environment denial-of-read
# ---------------------------------------------------------------------------


def test_adv_all_readers_raise_short_circuits_on_first_raise():
    """Adversary (or hardware fault) makes every reader raise.

    Gate MUST fail closed on the first raise — router_yaml_reader is first
    in the ordering. No downstream reader should be consulted.
    """

    call_log: list[str] = []

    class RouterRaise:
        def __call__(self) -> bytes:
            call_log.append("router")
            raise OSError("disk offline")

    class PinnedRaise:
        def __call__(self) -> dict:
            call_log.append("pinned")
            raise OSError("pinned offline")

    class ManifestRaise:
        def __call__(self) -> dict:
            call_log.append("manifest")
            raise OSError("manifest offline")

    class PriorRaise:
        def __call__(self) -> Optional[str]:
            call_log.append("prior")
            raise OSError("prior offline")

    class VerifyRaise:
        def __call__(self, p: bytes, s: bytes, k: bytes) -> bool:
            call_log.append("verify")
            raise RuntimeError("verifier offline")

    class HashRaise:
        def __call__(self, data: bytes) -> str:
            call_log.append("hash")
            raise RuntimeError("hash offline")

    r = check_router_integrity_multi_source(
        router_yaml_reader=RouterRaise(),
        pinned_hash_reader=PinnedRaise(),
        external_manifest_reader=ManifestRaise(),
        prior_chain_head_reader=PriorRaise(),
        signature_verify=VerifyRaise(),
        hash_bytes=HashRaise(),
        public_key=b"pk",
    )

    assert r.success is False
    assert r.failure_code == F_AMDT_10_READER_FAIL
    assert r.detail.check_failed == "reader_fail"
    assert r.detail.reason_tag == "router_yaml_reader_raised"
    assert call_log == ["router"], (
        "short-circuit violated: subsequent readers must not be consulted"
    )


# ---------------------------------------------------------------------------
# Degenerate but valid: operator intentionally empties router.yaml
# ---------------------------------------------------------------------------


def test_adv_router_yaml_empty_file_but_consistent_across_sources_passes():
    """Operator cleared router.yaml intentionally. Hash of empty bytes is
    a deterministic non-empty string under real SHA3-512; gate must accept
    when all three sources agree on that empty-file hash and the manifest
    is properly chained.
    """

    empty_yaml = b""
    empty_hash = _hash_bytes(empty_yaml)
    assert empty_hash != ""

    manifest = _make_manifest(
        chain_head_hash=empty_hash,
        prior_chain_head_hash="prior-nonempty",
    )

    def sig_verify(p: bytes, s: bytes, k: bytes) -> bool:
        return True

    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(empty_yaml),
        pinned_hash_reader=_pinned_reader(empty_hash),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader("prior-nonempty"),
        signature_verify=sig_verify,
        hash_bytes=_hash_bytes,
        public_key=b"pk",
    )

    assert r.success is True
    assert r.detail.live_hash == empty_hash


# ---------------------------------------------------------------------------
# Bonus: bootstrap-row forgery
# ---------------------------------------------------------------------------


def test_adv_bootstrap_forgery_claims_no_prior_when_prior_exists_denies_chain_break():
    """Adversary rewrites the manifest to claim prior_chain_head_hash=""
    (the bootstrap convention) to hide historical rows. prior_chain_head_reader
    reads the genuine prior hash from out-of-repo storage and returns a str,
    so the chain-break check catches the forgery.
    """

    yaml = b"router: current"
    live = _hash_bytes(yaml)
    manifest = _make_manifest(
        chain_head_hash=live,
        prior_chain_head_hash="",  # forged bootstrap claim
    )

    def sig_verify(p: bytes, s: bytes, k: bytes) -> bool:
        return True

    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader("GENUINE-PRIOR"),
        signature_verify=sig_verify,
        hash_bytes=_hash_bytes,
        public_key=b"pk",
    )

    assert r.success is False
    assert r.failure_code == F_AMDT_10_CHAIN_BREAK
    assert r.detail.reason_tag == "prior_chain_head_hash_mismatches_prior_reader"


# ---------------------------------------------------------------------------
# Bonus: strict is-True verifier contract — no truthy bypass
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("truthy", [1, "true", "True", [True], (True,), {"ok": True}])
def test_adv_signature_verify_truthy_non_True_value_denies_signature(truthy):
    """Adversary-supplied verifier that returns a truthy-but-not-True value
    (e.g. int, list, dict) to pretend success — gate's strict ``is True``
    identity check catches every variant.
    """

    yaml = b"router: x"
    live = _hash_bytes(yaml)
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="")

    class Verifier:
        def __call__(self, p: bytes, s: bytes, k: bytes):
            return truthy

    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=Verifier(),  # type: ignore[arg-type]
        hash_bytes=_hash_bytes,
        public_key=b"pk",
    )

    assert r.success is False
    assert r.failure_code == F_AMDT_10_SIGNATURE
