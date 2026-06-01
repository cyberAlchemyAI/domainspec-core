"""Unit tests for pipeline.vault.init_marker (§5.1 + §5.6 + §6.11 + §7.2).

Round M (BT14.a + BT14.f ceremony).

Covers:
* Fresh write produces canonical marker + HMAC trailer
* Second write raises VaultInitAlreadyExists (F-INIT-01)
* Verify on clean marker round-trips
* Missing marker/hmac → VaultInitMissing (F-INIT-01)
* Tampered body → VaultInitHMACMismatch (F-INIT-02)
* Whitespace-only tamper → VaultInitHMACMismatch (canonicalisation re-check)
* Wrong HMAC key → mismatch
* Scope / slug mismatch at verify time
* Drifted volume UUID → VaultInitIdentityDrift (F-INIT-03)
* Drifted fs_type → VaultInitIdentityDrift
* Shared scope requires slug="", org scope requires non-empty slug
* E-001 arg-type gates
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pytest

from pipeline.sovereignty.audit import canonical_json_bytes
from pipeline.sovereignty.keys import KeyStore
from pipeline.vault.error_codes import (
    F_INIT_01,
    F_INIT_02,
    F_INIT_03,
    VaultInitError,
    VaultInitHMACMismatch,
    VaultInitIdentityDrift,
)
from pipeline.vault.init_marker import (
    VAULT_INIT_HMAC_KEY_ID,
    VaultInitAlreadyExists,
    VaultInitMissing,
    verify_vault_init_marker,
    write_vault_init_marker,
)
from pipeline.vault.schemas import IdentityTuple, VaultInitMarker


_HMAC_KEY = b"\xcd" * 32


class _StubKeyStore(KeyStore):
    def __init__(self, *, key_bytes: bytes = _HMAC_KEY) -> None:
        self._key = key_bytes

    def _retrieve_raw(self, key_id: str) -> bytearray:
        return bytearray(self._key)

    def store(self, *, key_id: str, key_bytes, purpose: str) -> None:
        raise NotImplementedError

    def rotate(self, key_id: str) -> str:
        raise NotImplementedError

    def zero(self, key_id: str) -> None:
        raise NotImplementedError

    def exists(self, key_id: str) -> bool:
        return True

    def provider(self) -> str:
        return "stub"


def _make_identity(
    volume_uuid: str = "a" * 32,
    fs_type: str = "apfs",
) -> IdentityTuple:
    return IdentityTuple(
        volume_uuid=volume_uuid,
        fs_file_id="0" * 16,
        mount_id="0" * 16,
        fs_type=fs_type,
        captured_at="2026-04-19T00:00:00Z",
    )


@pytest.fixture
def patched_identity(monkeypatch: pytest.MonkeyPatch):
    """Override resolve_identity_tuple inside init_marker with a fixture-controlled box."""
    box: dict[str, IdentityTuple] = {"tuple": _make_identity()}

    def fake(path: Path) -> IdentityTuple:
        return box["tuple"]

    monkeypatch.setattr("pipeline.vault.init_marker.resolve_identity_tuple", fake)
    return box


@pytest.fixture
def paths(tmp_path: Path) -> dict[str, Path]:
    vault = tmp_path / "vault"
    vault.mkdir(parents=True, exist_ok=True)
    return {
        "marker": vault / "init.marker",
        "hmac": vault / "init.marker.hmac",
        "lock": vault / "init.marker.lock",
        "vault": vault,
    }


@pytest.fixture
def keystore() -> _StubKeyStore:
    return _StubKeyStore()


def _write_default(
    paths: dict[str, Path],
    keystore: KeyStore,
    *,
    scope: str = "org",
    slug: str = "mycosymbiotics",
    operator_id: str = "josh",
    section_lock_hash: str = "deadbeef" * 8,
) -> VaultInitMarker:
    return write_vault_init_marker(
        marker_path=paths["marker"],
        hmac_path=paths["hmac"],
        lock_path=paths["lock"],
        keystore=keystore,
        scope=scope,
        slug=slug,
        operator_id=operator_id,
        section_lock_hash=section_lock_hash,
    )


# ---------------------------------------------------------------------------
# Fresh-write ceremony
# ---------------------------------------------------------------------------


class TestWrite:
    def test_first_write_creates_marker_and_hmac(
        self, paths, keystore, patched_identity
    ) -> None:
        body = _write_default(paths, keystore)
        assert paths["marker"].is_file()
        assert paths["hmac"].is_file()
        assert body.scope == "org"
        assert body.slug == "mycosymbiotics"
        assert body.created_under_uuid == patched_identity["tuple"].volume_uuid

    def test_body_on_disk_is_canonical(
        self, paths, keystore, patched_identity
    ) -> None:
        body = _write_default(paths, keystore)
        on_disk = paths["marker"].read_bytes()
        assert on_disk == canonical_json_bytes(asdict(body))

    def test_hmac_file_is_hex_sha3_512_length(
        self, paths, keystore, patched_identity
    ) -> None:
        _write_default(paths, keystore)
        hmac_hex = paths["hmac"].read_text(encoding="ascii").strip()
        assert len(hmac_hex) == 128  # SHA3-512 = 64 bytes = 128 hex chars

    def test_second_write_raises_already_exists(
        self, paths, keystore, patched_identity
    ) -> None:
        _write_default(paths, keystore)
        with pytest.raises(VaultInitAlreadyExists):
            _write_default(paths, keystore)

    def test_shared_scope_requires_empty_slug(
        self, paths, keystore, patched_identity
    ) -> None:
        with pytest.raises(ValueError):
            _write_default(paths, keystore, scope="shared", slug="myco")

    def test_org_scope_requires_non_empty_slug(
        self, paths, keystore, patched_identity
    ) -> None:
        with pytest.raises(ValueError):
            _write_default(paths, keystore, scope="org", slug="")

    def test_invalid_scope_rejected(
        self, paths, keystore, patched_identity
    ) -> None:
        with pytest.raises(ValueError):
            _write_default(paths, keystore, scope="bogus", slug="x")

    def test_shared_scope_accepts_empty_slug(
        self, paths, keystore, patched_identity
    ) -> None:
        body = _write_default(paths, keystore, scope="shared", slug="")
        assert body.scope == "shared"
        assert body.slug == ""


# ---------------------------------------------------------------------------
# Arg-type gates (E-001)
# ---------------------------------------------------------------------------


class TestArgTypes:
    def test_marker_path_must_be_path(self, paths, keystore, patched_identity) -> None:
        with pytest.raises(TypeError):
            write_vault_init_marker(
                marker_path=str(paths["marker"]),  # type: ignore[arg-type]
                hmac_path=paths["hmac"],
                lock_path=paths["lock"],
                keystore=keystore,
                scope="org",
                slug="x",
                operator_id="josh",
                section_lock_hash="0" * 64,
            )

    def test_hmac_path_must_be_path(self, paths, keystore, patched_identity) -> None:
        with pytest.raises(TypeError):
            write_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=str(paths["hmac"]),  # type: ignore[arg-type]
                lock_path=paths["lock"],
                keystore=keystore,
                scope="org",
                slug="x",
                operator_id="josh",
                section_lock_hash="0" * 64,
            )

    def test_keystore_must_be_keystore(self, paths, patched_identity) -> None:
        with pytest.raises(TypeError):
            write_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                lock_path=paths["lock"],
                keystore=object(),  # type: ignore[arg-type]
                scope="org",
                slug="x",
                operator_id="josh",
                section_lock_hash="0" * 64,
            )

    def test_slug_must_be_str(self, paths, keystore, patched_identity) -> None:
        with pytest.raises(TypeError):
            write_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                lock_path=paths["lock"],
                keystore=keystore,
                scope="org",
                slug=None,  # type: ignore[arg-type]
                operator_id="josh",
                section_lock_hash="0" * 64,
            )


# ---------------------------------------------------------------------------
# Verify success
# ---------------------------------------------------------------------------


class TestVerify:
    def test_verify_clean_marker_returns_body(
        self, paths, keystore, patched_identity
    ) -> None:
        body = _write_default(paths, keystore)
        got = verify_vault_init_marker(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            keystore=keystore,
            expected_slug="mycosymbiotics",
            expected_scope="org",
        )
        assert got.slug == body.slug
        assert got.scope == body.scope
        assert got.created_under_uuid == body.created_under_uuid


# ---------------------------------------------------------------------------
# Missing artefacts → F-INIT-01
# ---------------------------------------------------------------------------


class TestMissing:
    def test_marker_missing(self, paths, keystore, patched_identity) -> None:
        _write_default(paths, keystore)
        paths["marker"].unlink()
        with pytest.raises(VaultInitMissing) as exc:
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="mycosymbiotics",
                expected_scope="org",
            )
        assert exc.value.code == F_INIT_01

    def test_hmac_missing(self, paths, keystore, patched_identity) -> None:
        _write_default(paths, keystore)
        paths["hmac"].unlink()
        with pytest.raises(VaultInitMissing) as exc:
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="mycosymbiotics",
                expected_scope="org",
            )
        assert exc.value.code == F_INIT_01


# ---------------------------------------------------------------------------
# HMAC mismatch → F-INIT-02
# ---------------------------------------------------------------------------


class TestHMACMismatch:
    def test_tampered_body_detected(
        self, paths, keystore, patched_identity
    ) -> None:
        _write_default(paths, keystore)
        body = json.loads(paths["marker"].read_bytes())
        body["operator_id"] = "attacker"
        paths["marker"].write_bytes(canonical_json_bytes(body))
        with pytest.raises(VaultInitHMACMismatch) as exc:
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="mycosymbiotics",
                expected_scope="org",
            )
        assert exc.value.code == F_INIT_02

    def test_whitespace_only_tamper_detected(
        self, paths, keystore, patched_identity
    ) -> None:
        _write_default(paths, keystore)
        canonical = paths["marker"].read_bytes()
        # Pretty-print: same JSON semantics, different bytes. Canonical
        # recomputation in verify should flag this before HMAC is compared.
        pretty = json.dumps(json.loads(canonical), indent=2).encode("utf-8")
        assert pretty != canonical
        paths["marker"].write_bytes(pretty)
        with pytest.raises(VaultInitHMACMismatch):
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="mycosymbiotics",
                expected_scope="org",
            )

    def test_wrong_hmac_key_rejected(
        self, paths, keystore, patched_identity
    ) -> None:
        _write_default(paths, keystore)
        wrong = _StubKeyStore(key_bytes=b"\xff" * 32)
        with pytest.raises(VaultInitHMACMismatch):
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=wrong,
                expected_slug="mycosymbiotics",
                expected_scope="org",
            )

    def test_tampered_hmac_file_rejected(
        self, paths, keystore, patched_identity
    ) -> None:
        _write_default(paths, keystore)
        paths["hmac"].write_text("0" * 128 + "\n", encoding="ascii")
        with pytest.raises(VaultInitHMACMismatch):
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="mycosymbiotics",
                expected_scope="org",
            )


# ---------------------------------------------------------------------------
# Scope/slug mismatch at verify time
# ---------------------------------------------------------------------------


class TestScopeSlugMismatch:
    def test_scope_mismatch(self, paths, keystore, patched_identity) -> None:
        _write_default(paths, keystore, scope="org", slug="myco")
        with pytest.raises(VaultInitError):
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="myco",
                expected_scope="shared",
            )

    def test_slug_mismatch(self, paths, keystore, patched_identity) -> None:
        _write_default(paths, keystore, scope="org", slug="myco")
        with pytest.raises(VaultInitError):
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="other_org",
                expected_scope="org",
            )


# ---------------------------------------------------------------------------
# Identity drift → F-INIT-03
# ---------------------------------------------------------------------------


class TestIdentityDrift:
    def test_volume_uuid_drift(
        self, paths, keystore, patched_identity
    ) -> None:
        _write_default(paths, keystore)
        patched_identity["tuple"] = _make_identity(volume_uuid="b" * 32)
        with pytest.raises(VaultInitIdentityDrift) as exc:
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="mycosymbiotics",
                expected_scope="org",
            )
        assert exc.value.code == F_INIT_03

    def test_fs_type_drift(self, paths, keystore, patched_identity) -> None:
        _write_default(paths, keystore)
        # Same volume UUID, different fs_type — this is the remount-as-ext4
        # scenario the drift detector is designed to catch.
        patched_identity["tuple"] = _make_identity(
            volume_uuid=patched_identity["tuple"].volume_uuid, fs_type="ext4"
        )
        with pytest.raises(VaultInitIdentityDrift) as exc:
            verify_vault_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=keystore,
                expected_slug="mycosymbiotics",
                expected_scope="org",
            )
        assert exc.value.code == F_INIT_03


# ---------------------------------------------------------------------------
# HMAC key ID pin
# ---------------------------------------------------------------------------


class TestKeyID:
    def test_uses_expected_key_id(
        self, paths, patched_identity, monkeypatch
    ) -> None:
        seen: list[str] = []

        class _Recorder(_StubKeyStore):
            def _retrieve_raw(self, key_id: str) -> bytearray:
                seen.append(key_id)
                return super()._retrieve_raw(key_id)

        ks = _Recorder()
        _write_default(paths, ks)
        assert seen == [VAULT_INIT_HMAC_KEY_ID]


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin (F-2..F-5: vault_batch_1_redispatch_2026-04-22)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        import importlib
        _mod = importlib.import_module('pipeline.vault.init_marker')
        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
