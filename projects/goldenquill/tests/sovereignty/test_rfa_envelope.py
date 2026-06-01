"""Unit + adversarial tests for pipeline.sovereignty.rfa_envelope.

Section 1 Round F1. Covers §4.1 M1 dual-hash ingest and v2 URL re-verify
path + §6.1 F-RFA-01..05 failure codes + §7.6 test criteria:

* test_m1_rfa_rehash_detects_content_change
* test_m1_rfa_rehash_detects_inode_swap
* test_m1_nonce_is_32_bytes

Adversarial probes (*_adv_*) exercise the TOCTOU + URL-tamper surfaces.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from pipeline.sovereignty._types import HashPair
from pipeline.sovereignty.rfa_envelope import (
    RFADriftError,
    RFAEnvelope,
    RFAEnvelopeCorrupt,
    RFAError,
    RFAMissing,
    ingest_rfa,
    reverify_rfa,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def repo_root(tmp_path: Path) -> Path:
    """Fresh empty repo root under pytest tmp_path."""
    (tmp_path / "orgs" / "acme-coop").mkdir(parents=True)
    return tmp_path


@pytest.fixture()
def sample_ingest(repo_root: Path) -> tuple[RFAEnvelope, bytes]:
    """Default-shape ingest for re-use across tests."""
    content = b"the quick brown fox jumps over the lazy dog\n"
    env = ingest_rfa(
        url="https://example.gov/rfa/vapg-2026.pdf",
        content_bytes=content,
        slug="acme-coop",
        operator_id="josh@fitfarms",
        rfa_id="vapg-fy26",
        repo_root=repo_root,
    )
    return env, content


# ---------------------------------------------------------------------------
# Ingest path
# ---------------------------------------------------------------------------


def test_ingest_produces_populated_envelope(sample_ingest):
    env, content = sample_ingest
    assert env.rfa_id == "vapg-fy26"
    assert env.session_bound_slug == "acme-coop"
    assert env.ingested_by == "josh@fitfarms"
    assert env.url_at_ingest == "https://example.gov/rfa/vapg-2026.pdf"
    assert env.size_bytes == len(content)
    assert env.inode > 0
    assert env.device != 0
    assert env.ingested_at.endswith("Z")


def test_ingest_writes_raw_content_file(sample_ingest, repo_root):
    env, content = sample_ingest
    raw_path = repo_root / "orgs" / "acme-coop" / "rfa" / "vapg-fy26.raw"
    assert raw_path.is_file()
    assert raw_path.read_bytes() == content
    # Mode is owner-only per 0o600.
    assert oct(raw_path.stat().st_mode)[-3:] == "600"


def test_ingest_writes_envelope_json(sample_ingest, repo_root):
    env, _ = sample_ingest
    env_path = repo_root / "sovereignty" / "envelopes" / "rfa" / "vapg-fy26.json"
    assert env_path.is_file()
    parsed = json.loads(env_path.read_text("utf-8"))
    assert parsed["rfa_id"] == "vapg-fy26"
    assert parsed["hashes"]["algorithm"] == "SHA3-512"
    assert len(parsed["hashes"]["url_hash"]) == 128
    assert len(parsed["hashes"]["content_hash"]) == 128
    assert len(parsed["hashes"]["nonce_hex"]) == 64


def test_ingest_writes_audit_line(sample_ingest, repo_root):
    env, _ = sample_ingest
    audit_path = repo_root / "orgs" / "acme-coop" / "rfa_audit.jsonl"
    assert audit_path.is_file()
    lines = audit_path.read_text("utf-8").splitlines()
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert set(rec.keys()) == {"rfa_id", "envelope_hash", "operator_id", "ingested_at"}
    assert rec["operator_id"] == "josh@fitfarms"


def test_m1_nonce_is_32_bytes(sample_ingest):
    env, _ = sample_ingest
    # 32 bytes = 64 hex chars.
    assert len(env.hashes.nonce_hex) == 64
    int(env.hashes.nonce_hex, 16)  # must be valid hex


def test_two_ingests_have_distinct_nonces_and_content_hashes(repo_root):
    content = b"identical content"
    e1 = ingest_rfa(
        url="https://x.gov/a",
        content_bytes=content,
        slug="acme-coop",
        operator_id="op",
        rfa_id="a",
        repo_root=repo_root,
    )
    e2 = ingest_rfa(
        url="https://x.gov/b",
        content_bytes=content,
        slug="acme-coop",
        operator_id="op",
        rfa_id="b",
        repo_root=repo_root,
    )
    assert e1.hashes.nonce_hex != e2.hashes.nonce_hex
    assert e1.hashes.content_hash != e2.hashes.content_hash


def test_identical_urls_produce_identical_url_hashes(repo_root):
    e1 = ingest_rfa(
        url="https://same-url.example/doc",
        content_bytes=b"x",
        slug="acme-coop",
        operator_id="op",
        rfa_id="a",
        repo_root=repo_root,
    )
    e2 = ingest_rfa(
        url="https://same-url.example/doc",
        content_bytes=b"y",
        slug="acme-coop",
        operator_id="op",
        rfa_id="b",
        repo_root=repo_root,
    )
    assert e1.hashes.url_hash == e2.hashes.url_hash


# ---------------------------------------------------------------------------
# E-001 type gate + validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kwarg,value,exc",
    [
        ("url", 123, TypeError),
        ("content_bytes", "not bytes", TypeError),
        ("slug", 42, TypeError),
        ("operator_id", None, TypeError),
        ("repo_root", "/tmp", TypeError),
        ("url", "", ValueError),
        ("slug", "", ValueError),
        ("operator_id", "", ValueError),
    ],
)
def test_ingest_rejects_bad_args(repo_root, kwarg, value, exc):
    base = dict(
        url="https://x/a",
        content_bytes=b"x",
        slug="acme-coop",
        operator_id="op",
        rfa_id="ok",
        repo_root=repo_root,
    )
    base[kwarg] = value
    with pytest.raises(exc):
        ingest_rfa(**base)


@pytest.mark.parametrize(
    "rfa_id,exc",
    [
        (123, TypeError),
        ("", ValueError),
        (".hidden", ValueError),
        ("slash/inside", ValueError),
        ("has space", ValueError),
        ("a" * 129, ValueError),
    ],
)
def test_ingest_rejects_bad_rfa_id(repo_root, rfa_id, exc):
    with pytest.raises(exc):
        ingest_rfa(
            url="https://x/a",
            content_bytes=b"x",
            slug="acme-coop",
            operator_id="op",
            rfa_id=rfa_id,
            repo_root=repo_root,
        )


def test_ingest_accepts_bytearray(repo_root):
    ba = bytearray(b"mutable payload")
    env = ingest_rfa(
        url="https://x/a",
        content_bytes=ba,
        slug="acme-coop",
        operator_id="op",
        rfa_id="ba",
        repo_root=repo_root,
    )
    assert env.size_bytes == len(ba)


def test_reverify_rejects_non_envelope_arg():
    with pytest.raises(TypeError):
        reverify_rfa({"not": "an envelope"})


# ---------------------------------------------------------------------------
# Reverify happy path
# ---------------------------------------------------------------------------


def test_reverify_happy_path(sample_ingest):
    env, _ = sample_ingest
    # No exception means success; reverify returns None.
    assert reverify_rfa(env) is None


def test_reverify_after_repeated_reads_is_stable(sample_ingest):
    env, _ = sample_ingest
    for _ in range(3):
        reverify_rfa(env)


# ---------------------------------------------------------------------------
# §7.6 — RFA drift / inode / url failure modes (F-RFA-01..05)
# ---------------------------------------------------------------------------


def test_m1_rfa_rehash_detects_content_change(sample_ingest):
    env, _ = sample_ingest
    raw_path = Path(env.canonical_path)
    # Flip one byte in place (keeps inode + size).
    data = bytearray(raw_path.read_bytes())
    data[5] ^= 0xFF
    # Use os.open + O_WRONLY to preserve inode (do NOT rename).
    fd = os.open(str(raw_path), os.O_WRONLY)
    try:
        os.pwrite(fd, bytes(data), 0)
    finally:
        os.close(fd)
    with pytest.raises(RFADriftError) as excinfo:
        reverify_rfa(env)
    assert excinfo.value.reason == "rfa_content_hash_mismatch"


def test_m1_rfa_rehash_detects_inode_swap(sample_ingest):
    env, content = sample_ingest
    raw_path = Path(env.canonical_path)
    # Move + re-create to trigger a new inode while preserving size.
    raw_path.rename(str(raw_path) + ".bak")
    raw_path.write_bytes(content)
    with pytest.raises(RFADriftError) as excinfo:
        reverify_rfa(env)
    assert excinfo.value.reason == "rfa_inode_changed"


def test_m1_rfa_rehash_detects_size_change(sample_ingest):
    env, content = sample_ingest
    raw_path = Path(env.canonical_path)
    raw_path.rename(str(raw_path) + ".bak")
    raw_path.write_bytes(content + b"tail")  # size shifts; new inode too
    with pytest.raises(RFADriftError) as excinfo:
        reverify_rfa(env)
    # Either inode or size can fire first; both are drift.
    assert excinfo.value.reason in {"rfa_inode_changed", "rfa_size_changed"}


def test_reverify_missing_file_raises_rfa_missing(sample_ingest):
    env, _ = sample_ingest
    Path(env.canonical_path).unlink()
    with pytest.raises(RFAMissing):
        reverify_rfa(env)


def test_reverify_detects_url_hash_tamper(sample_ingest):
    env, _ = sample_ingest
    # Rebuild envelope with a url_at_ingest that no longer matches hashes.url_hash.
    tampered = RFAEnvelope(
        rfa_id=env.rfa_id,
        ingested_at=env.ingested_at,
        hashes=env.hashes,
        session_bound_slug=env.session_bound_slug,
        canonical_path=env.canonical_path,
        inode=env.inode,
        device=env.device,
        size_bytes=env.size_bytes,
        ingested_by=env.ingested_by,
        url_at_ingest=env.url_at_ingest + "?attacker_param",
    )
    with pytest.raises(RFADriftError) as excinfo:
        reverify_rfa(tampered)
    assert excinfo.value.reason == "rfa_url_hash_mismatch"


# ---------------------------------------------------------------------------
# Adversarial probes
# ---------------------------------------------------------------------------


def test_adv_content_hash_also_catches_pure_append(sample_ingest):
    env, _ = sample_ingest
    raw_path = Path(env.canonical_path)
    # Append only; size changes but content prefix is intact. Size check fires first.
    with open(raw_path, "ab") as fh:
        fh.write(b"extra")
    with pytest.raises(RFADriftError):
        reverify_rfa(env)


def test_adv_content_swap_to_same_length_same_inode(sample_ingest):
    """Swap content of same length without changing inode — content_hash must fire."""
    env, content = sample_ingest
    raw_path = Path(env.canonical_path)
    # Overwrite in place at the same length via O_TRUNC would reset inode;
    # we need to truncate+rewrite without unlinking.
    new_bytes = bytes([0xAA] * len(content))
    fd = os.open(str(raw_path), os.O_WRONLY)
    try:
        os.pwrite(fd, new_bytes, 0)
    finally:
        os.close(fd)
    # Size stayed the same; inode stayed the same. Only content_hash should fire.
    with pytest.raises(RFADriftError) as excinfo:
        reverify_rfa(env)
    assert excinfo.value.reason == "rfa_content_hash_mismatch"


def test_adv_nonce_is_unpredictable_across_ingests(repo_root):
    """E-014 / BT1 — 32-byte nonce should be high-entropy and distinct."""
    nonces = set()
    for i in range(20):
        env = ingest_rfa(
            url=f"https://x/{i}",
            content_bytes=b"x",
            slug="acme-coop",
            operator_id="op",
            rfa_id=f"r{i}",
            repo_root=repo_root,
        )
        nonces.add(env.hashes.nonce_hex)
    assert len(nonces) == 20


def test_adv_tampered_nonce_hex_breaks_reverify(sample_ingest):
    """Envelope whose nonce_hex field has been tampered must fail content check."""
    env, _ = sample_ingest
    # Flip the first nibble of nonce.
    tampered_nonce = ("0" if env.hashes.nonce_hex[0] != "0" else "f") + env.hashes.nonce_hex[1:]
    tampered_hashes = HashPair(
        url_hash=env.hashes.url_hash,
        content_hash=env.hashes.content_hash,
        algorithm=env.hashes.algorithm,
        nonce_hex=tampered_nonce,
    )
    tampered = RFAEnvelope(
        rfa_id=env.rfa_id,
        ingested_at=env.ingested_at,
        hashes=tampered_hashes,
        session_bound_slug=env.session_bound_slug,
        canonical_path=env.canonical_path,
        inode=env.inode,
        device=env.device,
        size_bytes=env.size_bytes,
        ingested_by=env.ingested_by,
        url_at_ingest=env.url_at_ingest,
    )
    with pytest.raises(RFADriftError) as excinfo:
        reverify_rfa(tampered)
    assert excinfo.value.reason == "rfa_content_hash_mismatch"


def test_adv_envelope_is_frozen(sample_ingest):
    env, _ = sample_ingest
    with pytest.raises(Exception):
        env.rfa_id = "hostile"  # type: ignore[misc]


def test_adv_ingest_and_reverify_with_empty_content(repo_root):
    env = ingest_rfa(
        url="https://x/empty",
        content_bytes=b"",
        slug="acme-coop",
        operator_id="op",
        rfa_id="empty",
        repo_root=repo_root,
    )
    assert env.size_bytes == 0
    reverify_rfa(env)
