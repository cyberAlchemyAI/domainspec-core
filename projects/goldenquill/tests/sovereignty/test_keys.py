"""Tests for pipeline.sovereignty.keys.

Coverage targets (per spec card `round_c_keys.md`):
  - KeyStore ABC: sealing via __init_subclass__; retrieve() wraps bytearray in SecretBytes;
    F-KEY-08 on non-bytearray return; F-KEY-10 on retrieve override at class-def time.
  - resolve_keystore: dispatch, unknown → F-KEY-01, non-macOS keychain → F-KEY-03,
    file without passphrase → F-KEY-04, no silent fallback, yubihsm stub.
  - MacOSKeychainKeyStore (conditional on macOS + security CLI): round-trip, zero,
    rotate, exists; keychain-locked → F-KEY-02 (mocked subprocess).
  - FileKeyStore (no platform dep): round-trip, KEK-wrong → F-KEY-05 (tampered ciphertext),
    missing env passphrase → F-KEY-04, zero unlinks, rotate mints new id.
  - NonceRegistry: append under fcntl.LOCK_EX; NonceReused (F-KEY-07); size-limit triggers
    pre-gen rotation; NonceRegistryRotationFailed on disk-full mock; trailer chain verify;
    NonceRegistryTrailerMismatch on segment-tamper; NonceRegistryTruncated on segment-delete.
  - Concurrency: two threads racing FileKeyStore.store serialize via fcntl.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import threading
from pathlib import Path
from unittest.mock import patch

import pytest

from pipeline.sovereignty import (
    FileKeyStore,
    FileKeyStoreUnavailable,
    KEYCHAIN_SERVICE_TEMPLATE,
    KeyCorrupt,
    KeyStore,
    KeyStoreConfigError,
    KeyStoreContractViolation,
    KeyStoreUnavailable,
    MacOSKeychainKeyStore,
    NONCE_REGISTRY_SIZE_LIMIT_BYTES,
    NonceRegistryRotationFailed,
    NonceRegistryTrailerMismatch,
    NonceRegistryTruncated,
    NonceReused,
    SecretBytes,
    TILTH_FILE_KEYSTORE_PASSPHRASE_ENV,
    TILTH_KEYSTORE_PROVIDER_ENV,
    YubiHSMKeyStore,
    resolve_keystore,
)
from pipeline.sovereignty.keys import _nonce_registry_append, _NonceRegistryState


# -------- KeyStore ABC sealing --------


class TestKeyStoreABCSealing:
    def test_subclass_overriding_retrieve_rejected(self) -> None:
        """§3.11 v4 RT-v3 HIGH-2 closure — class-def-time rejection via __init_subclass__."""
        with pytest.raises(KeyStoreContractViolation) as exc_info:
            class MaliciousStore(KeyStore):
                def retrieve(self, key_id):  # type: ignore[override]
                    return b"FAKE"
                # Required abstracts stubbed to make class definition legal at parse-time
                def _retrieve_raw(self, key_id): return bytearray(b"x")
                def store(self, *, key_id, key_bytes, purpose): pass
                def rotate(self, key_id): return key_id
                def zero(self, key_id): pass
                def exists(self, key_id): return False
                def provider(self): return "mal"
        assert "sealed" in str(exc_info.value).lower() or "retrieve" in str(exc_info.value)

    def test_subclass_not_overriding_retrieve_allowed(self) -> None:
        class OK(KeyStore):
            def _retrieve_raw(self, key_id):
                return bytearray(b"ok" * 16)
            def store(self, *, key_id, key_bytes, purpose): pass
            def rotate(self, key_id): return key_id
            def zero(self, key_id): pass
            def exists(self, key_id): return True
            def provider(self): return "ok"

        store = OK()
        with store.retrieve("any") as sb:
            assert bytes(sb.view()).startswith(b"ok")


class TestKeyStoreContractViolationOnBytesReturn:
    """F-KEY-08: _retrieve_raw MUST return bytearray; retrieve() enforces."""

    @pytest.mark.parametrize(
        "bad_return",
        [b"bytes-not-bytearray", "str-is-worse", 42, [], memoryview(b"mv")],
        ids=["bytes", "str", "int", "list", "memoryview"],
    )
    def test_non_bytearray_return_raises(self, bad_return) -> None:
        class BadStore(KeyStore):
            def _retrieve_raw(self, key_id):
                return bad_return
            def store(self, *, key_id, key_bytes, purpose): pass
            def rotate(self, key_id): return key_id
            def zero(self, key_id): pass
            def exists(self, key_id): return False
            def provider(self): return "bad"

        store = BadStore()
        with pytest.raises(KeyStoreContractViolation):
            store.retrieve("any")


# -------- resolve_keystore --------


class TestResolveKeystoreFactory:
    def test_unknown_provider_raises_f_key_01(
        self, monkeypatch, tmp_path
    ) -> None:
        monkeypatch.setenv(TILTH_KEYSTORE_PROVIDER_ENV, "hsm99")
        with pytest.raises(KeyStoreConfigError):
            resolve_keystore(slug="myco", keystore_dir=tmp_path)

    def test_keychain_on_non_darwin_raises_f_key_03(
        self, monkeypatch, tmp_path
    ) -> None:
        monkeypatch.setenv(TILTH_KEYSTORE_PROVIDER_ENV, "keychain")
        with patch("platform.system", return_value="Linux"):
            with pytest.raises(KeyStoreUnavailable):
                resolve_keystore(slug="myco", keystore_dir=tmp_path)

    def test_file_without_passphrase_raises_f_key_04(
        self, monkeypatch, tmp_path
    ) -> None:
        monkeypatch.setenv(TILTH_KEYSTORE_PROVIDER_ENV, "file")
        monkeypatch.delenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, raising=False)
        with pytest.raises(FileKeyStoreUnavailable):
            resolve_keystore(slug="myco", keystore_dir=tmp_path)

    def test_yubihsm_stub_raises_not_implemented(
        self, monkeypatch, tmp_path
    ) -> None:
        monkeypatch.setenv(TILTH_KEYSTORE_PROVIDER_ENV, "yubihsm")
        with pytest.raises(NotImplementedError):
            resolve_keystore(slug="myco", keystore_dir=tmp_path)

    def test_file_without_keystore_dir_raises_config(
        self, monkeypatch
    ) -> None:
        monkeypatch.setenv(TILTH_KEYSTORE_PROVIDER_ENV, "file")
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "pw")
        with pytest.raises(KeyStoreConfigError):
            resolve_keystore(slug="myco", keystore_dir=None)

    def test_missing_env_defaults_by_platform(
        self, monkeypatch, tmp_path
    ) -> None:
        monkeypatch.delenv(TILTH_KEYSTORE_PROVIDER_ENV, raising=False)
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "pw-default-test")
        with patch("platform.system", return_value="Linux"):
            ks = resolve_keystore(slug="myco", keystore_dir=tmp_path)
            assert ks.provider() == "file"


# -------- YubiHSMKeyStore stub --------


class TestYubiHSMStub:
    def test_init_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            YubiHSMKeyStore()


# -------- MacOSKeychainKeyStore (macOS-only) --------


_DARWIN = platform.system() == "Darwin"
_SECURITY_CLI = shutil.which("security")


@pytest.mark.skipif(
    not (_DARWIN and _SECURITY_CLI),
    reason="MacOSKeychainKeyStore requires macOS + `security` CLI",
)
class TestMacOSKeychainKeyStore:
    TEST_SLUG = "tilth-test-round-c-keychain"

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Best-effort cleanup of any test keychain items before + after."""
        yield
        # Delete anything we might have created during the test.
        try:
            ks = MacOSKeychainKeyStore(self.TEST_SLUG)
            for kid in ("test-roundtrip", "test-zero", "test-exists", "test-rotate"):
                try:
                    ks.zero(kid)
                except Exception:
                    pass
        except Exception:
            pass

    def test_rejects_non_canonical_slug(self) -> None:
        with pytest.raises(ValueError):
            MacOSKeychainKeyStore("NotCanonical")

    def test_store_retrieve_roundtrip(self) -> None:
        ks = MacOSKeychainKeyStore(self.TEST_SLUG)
        payload = b"super-secret-32-byte-test-key123"
        ks.store(key_id="test-roundtrip", key_bytes=payload, purpose="generic")
        with ks.retrieve("test-roundtrip") as sb:
            assert bytes(sb.view()) == payload

    def test_exists_true_false(self) -> None:
        ks = MacOSKeychainKeyStore(self.TEST_SLUG)
        assert ks.exists("never-stored-definitely-not-there-xyz123") is False
        ks.store(key_id="test-exists", key_bytes=b"x" * 16, purpose="generic")
        assert ks.exists("test-exists") is True

    def test_zero_removes_item(self) -> None:
        ks = MacOSKeychainKeyStore(self.TEST_SLUG)
        ks.store(key_id="test-zero", key_bytes=b"y" * 16, purpose="generic")
        assert ks.exists("test-zero")
        ks.zero("test-zero")
        assert not ks.exists("test-zero")

    def test_zero_idempotent_on_missing(self) -> None:
        ks = MacOSKeychainKeyStore(self.TEST_SLUG)
        # No raise on zeroing something that isn't there.
        ks.zero("definitely-not-stored-aaa")

    def test_rotate_creates_new_zeros_old(self) -> None:
        ks = MacOSKeychainKeyStore(self.TEST_SLUG)
        ks.store(key_id="test-rotate", key_bytes=b"z" * 32, purpose="generic")
        new_id = ks.rotate("test-rotate")
        assert new_id != "test-rotate"
        assert ks.exists(new_id)
        assert not ks.exists("test-rotate")
        # Cleanup
        ks.zero(new_id)

    def test_service_name_uses_template(self) -> None:
        ks = MacOSKeychainKeyStore(self.TEST_SLUG)
        expected = KEYCHAIN_SERVICE_TEMPLATE.format(slug=self.TEST_SLUG)
        assert ks._service == expected

    def test_type_gate_on_store(self) -> None:
        ks = MacOSKeychainKeyStore(self.TEST_SLUG)
        with pytest.raises(TypeError):
            ks.store(key_id=42, key_bytes=b"x", purpose="p")  # type: ignore[arg-type]

    def test_type_gate_on_retrieve(self) -> None:
        ks = MacOSKeychainKeyStore(self.TEST_SLUG)
        with pytest.raises(TypeError):
            ks._retrieve_raw(42)  # type: ignore[arg-type]

    def test_missing_cli_raises_unavailable(self) -> None:
        with patch("shutil.which", return_value=None):
            with pytest.raises(KeyStoreUnavailable):
                MacOSKeychainKeyStore(self.TEST_SLUG)


# -------- FileKeyStore (no platform dep) --------


class TestFileKeyStore:
    @pytest.fixture
    def ks(self, tmp_path, monkeypatch):
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "test-passphrase-xyz")
        return FileKeyStore("myco", keystore_dir=tmp_path)

    def test_init_rejects_non_canonical_slug(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "pw")
        with pytest.raises(ValueError):
            FileKeyStore("MyCo", keystore_dir=tmp_path)

    def test_init_zeros_passphrase_env(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "will-be-deleted")
        FileKeyStore("myco", keystore_dir=tmp_path)
        assert TILTH_FILE_KEYSTORE_PASSPHRASE_ENV not in os.environ

    def test_init_missing_passphrase_raises(self, tmp_path, monkeypatch) -> None:
        monkeypatch.delenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, raising=False)
        with pytest.raises(FileKeyStoreUnavailable):
            FileKeyStore("myco", keystore_dir=tmp_path)

    def test_store_retrieve_roundtrip(self, ks) -> None:
        payload = b"session-hmac-key-material-here" * 2
        ks.store(key_id="test-1", key_bytes=payload, purpose="session_hmac")
        with ks.retrieve("test-1") as sb:
            assert bytes(sb.view()) == payload

    def test_retrieve_returns_secretbytes(self, ks) -> None:
        ks.store(key_id="test-sb", key_bytes=b"material", purpose="p")
        with ks.retrieve("test-sb") as sb:
            assert isinstance(sb, SecretBytes)
            assert bytes(sb.view()) == b"material"

    def test_missing_key_raises_key_corrupt(self, ks) -> None:
        with pytest.raises(KeyCorrupt):
            ks.retrieve("does-not-exist")

    def test_tampered_ciphertext_raises_key_corrupt(self, ks, tmp_path) -> None:
        ks.store(key_id="test-tamper", key_bytes=b"secret", purpose="p")
        path = tmp_path / "myco" / "test-tamper.aead"
        body = json.loads(path.read_text())
        # Flip one nibble in ct.
        tampered_ct = body["ct_hex"][:-2] + ("00" if body["ct_hex"][-2:] != "00" else "ff")
        body["ct_hex"] = tampered_ct
        path.write_text(json.dumps(body, sort_keys=True, separators=(",", ":")))
        with pytest.raises(KeyCorrupt):
            ks.retrieve("test-tamper")

    def test_aad_mismatch_raises_key_corrupt(self, ks, tmp_path) -> None:
        ks.store(key_id="test-aad", key_bytes=b"secret", purpose="purposeA")
        path = tmp_path / "myco" / "test-aad.aead"
        body = json.loads(path.read_text())
        body["purpose"] = "purposeB"  # change AAD
        path.write_text(json.dumps(body, sort_keys=True, separators=(",", ":")))
        with pytest.raises(KeyCorrupt):
            ks.retrieve("test-aad")

    def test_zero_unlinks_file(self, ks, tmp_path) -> None:
        ks.store(key_id="test-z", key_bytes=b"secret", purpose="p")
        path = tmp_path / "myco" / "test-z.aead"
        assert path.exists()
        ks.zero("test-z")
        assert not path.exists()

    def test_zero_idempotent(self, ks) -> None:
        ks.zero("never-stored")  # no raise

    def test_exists(self, ks) -> None:
        assert not ks.exists("never-stored")
        ks.store(key_id="e1", key_bytes=b"x", purpose="p")
        assert ks.exists("e1")

    def test_rotate_mints_new_zeros_old(self, ks) -> None:
        ks.store(key_id="rotme", key_bytes=b"original", purpose="p")
        new_id = ks.rotate("rotme")
        assert new_id != "rotme"
        assert ks.exists(new_id)
        assert not ks.exists("rotme")

    def test_provider_identifier(self, ks) -> None:
        assert ks.provider() == "file"

    def test_context_manager_zeros_kek_on_exit(self, tmp_path, monkeypatch) -> None:
        """D-22 closure — `with FileKeyStore(...) as ks:` zeroes KEK on exit."""
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "ctx-manager-test")
        with FileKeyStore("myco", keystore_dir=tmp_path) as ks:
            ks.store(key_id="ctx-1", key_bytes=b"payload", purpose="p")
            kek_ref = ks._kek
            assert any(b != 0 for b in kek_ref)
        # After exit, KEK bytearray is all zeros.
        assert all(b == 0 for b in kek_ref)

    def test_context_manager_zeros_on_exception(self, tmp_path, monkeypatch) -> None:
        """Zero-on-exception — guarantees erasure even on early abort."""
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "ctx-manager-exc")
        ks_ref = None
        with pytest.raises(RuntimeError):
            with FileKeyStore("myco", keystore_dir=tmp_path) as ks:
                ks_ref = ks
                raise RuntimeError("boom")
        assert ks_ref is not None
        assert all(b == 0 for b in ks_ref._kek)

    def test_close_is_idempotent(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "close-idempotent")
        ks = FileKeyStore("myco", keystore_dir=tmp_path)
        ks.close()
        ks.close()  # no raise
        assert all(b == 0 for b in ks._kek)

    def test_salt_reused_across_instances(self, tmp_path, monkeypatch) -> None:
        """Salt is per-slug persistent — second init with same passphrase yields same KEK."""
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "stable-pw")
        ks1 = FileKeyStore("myco", keystore_dir=tmp_path)
        ks1.store(key_id="persist-test", key_bytes=b"secret-data", purpose="p")
        # Wipe in-memory instance; re-init with same passphrase.
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "stable-pw")
        ks2 = FileKeyStore("myco", keystore_dir=tmp_path)
        with ks2.retrieve("persist-test") as sb:
            assert bytes(sb.view()) == b"secret-data"

    def test_wrong_passphrase_raises_key_corrupt(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "correct-pw")
        ks1 = FileKeyStore("myco", keystore_dir=tmp_path)
        ks1.store(key_id="wpw-test", key_bytes=b"data", purpose="p")
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "WRONG-pw")
        ks2 = FileKeyStore("myco", keystore_dir=tmp_path)
        with pytest.raises(KeyCorrupt):
            ks2.retrieve("wpw-test")


# -------- Nonce registry --------


class TestNonceRegistry:
    @pytest.fixture
    def state(self, tmp_path) -> _NonceRegistryState:
        reg_dir = tmp_path / "nonce_registry"
        reg_dir.mkdir()
        return _NonceRegistryState(
            slug="myco",
            registry_dir=reg_dir,
            lock_path=reg_dir / ".nonce_registry.lock",
            hmac_key=bytearray(b"K" * 32),
        )

    def test_append_creates_segment_0(self, state) -> None:
        _nonce_registry_append(state, "key-a", b"\x00" * 12)
        assert (state.registry_dir / ".nonce_registry.0000.jsonl").exists()
        assert (state.registry_dir / ".nonce_registry.0000.hmac").exists()

    def test_append_monotonic_seq_id(self, state) -> None:
        for i in range(5):
            _nonce_registry_append(state, f"k-{i}", bytes([i] * 12))
        lines = (state.registry_dir / ".nonce_registry.0000.jsonl").read_bytes().splitlines()
        entries = [json.loads(l) for l in lines]
        assert [e["seq_id"] for e in entries] == [1, 2, 3, 4, 5]

    def test_nonce_reused_raises_f_key_07(self, state) -> None:
        nonce = b"\x42" * 12
        _nonce_registry_append(state, "k-dup", nonce)
        with pytest.raises(NonceReused):
            _nonce_registry_append(state, "k-dup", nonce)

    def test_different_key_id_same_nonce_allowed(self, state) -> None:
        # NonceReused check is per (key_id, nonce_hex) pair; the same nonce under
        # a different key_id is technically allowed by this impl. (Blueprint leaves
        # this latitude; F-KEY-07 fires on "duplicate under the same key_id".)
        n = b"\x11" * 12
        _nonce_registry_append(state, "k-a", n)
        # Current impl's _nonce_already_registered checks both fields equal —
        # confirm that's the behaviour (different key_id → no collision).
        _nonce_registry_append(state, "k-b", n)  # no raise

    def test_rotation_on_size_limit(self, state, monkeypatch) -> None:
        # Monkey-patch NONCE_REGISTRY_SIZE_LIMIT_BYTES low.
        import pipeline.sovereignty.keys as keys_mod
        monkeypatch.setattr(keys_mod, "NONCE_REGISTRY_SIZE_LIMIT_BYTES", 200)
        for i in range(20):
            _nonce_registry_append(state, f"k-{i}", bytes([i] * 12))
        # At least one rotation should have happened.
        segments = sorted(state.registry_dir.glob(".nonce_registry.*.jsonl"))
        assert len(segments) >= 2

    def test_trailer_chain_verify_green_after_appends(self, state) -> None:
        from pipeline.sovereignty.keys import _verify_nonce_registry_chain
        for i in range(3):
            _nonce_registry_append(state, f"k-{i}", bytes([i] * 12))
        # Should not raise.
        _verify_nonce_registry_chain(state)

    def test_trailer_tamper_detected(self, state) -> None:
        from pipeline.sovereignty.keys import _verify_nonce_registry_chain
        _nonce_registry_append(state, "k-a", b"\x00" * 12)
        # Tamper the segment body — flip a byte in the ledger line.
        seg = state.registry_dir / ".nonce_registry.0000.jsonl"
        raw = seg.read_bytes()
        seg.write_bytes(bytes([raw[0] ^ 0x01]) + raw[1:])
        with pytest.raises(NonceRegistryTrailerMismatch):
            _verify_nonce_registry_chain(state)

    def test_truncation_detected(self, state, monkeypatch) -> None:
        from pipeline.sovereignty.keys import _verify_nonce_registry_chain
        import pipeline.sovereignty.keys as keys_mod
        monkeypatch.setattr(keys_mod, "NONCE_REGISTRY_SIZE_LIMIT_BYTES", 200)
        for i in range(15):
            _nonce_registry_append(state, f"k-{i}", bytes([i] * 12))
        # Remove segment 0 entirely.
        (state.registry_dir / ".nonce_registry.0000.jsonl").unlink()
        (state.registry_dir / ".nonce_registry.0000.hmac").unlink()
        with pytest.raises(NonceRegistryTruncated):
            _verify_nonce_registry_chain(state)

    def test_rotation_failure_is_detected(self, state, monkeypatch) -> None:
        """If the rotation IO fails (disk full sim), raise NonceRegistryRotationFailed."""
        import pipeline.sovereignty.keys as keys_mod
        monkeypatch.setattr(keys_mod, "NONCE_REGISTRY_SIZE_LIMIT_BYTES", 100)
        # Fill segment 0.
        for i in range(10):
            _nonce_registry_append(state, f"k-{i}", bytes([i] * 12))
        # Simulate disk full by patching _atomic_write_bytes to raise OSError.
        original = keys_mod._atomic_write_bytes

        def failing_write(target, payload):
            # Only fail when writing the trailer for segment 0 during rotation.
            raise OSError(28, "simulated disk full")

        monkeypatch.setattr(keys_mod, "_atomic_write_bytes", failing_write)
        with pytest.raises(NonceRegistryRotationFailed):
            _nonce_registry_append(state, "k-trigger-rotate", b"\xff" * 12)
        monkeypatch.setattr(keys_mod, "_atomic_write_bytes", original)


# -------- Concurrency --------


class TestConcurrency:
    def test_two_threads_append_serialize(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv(TILTH_FILE_KEYSTORE_PASSPHRASE_ENV, "conc-test-pw")
        ks = FileKeyStore("myco", keystore_dir=tmp_path)
        errors = []

        def worker(n):
            try:
                ks.store(key_id=f"k-{n}", key_bytes=bytes([n] * 16), purpose="p")
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == [], f"concurrency errors: {errors}"
        # Verify all 6 succeeded.
        for i in range(6):
            assert ks.exists(f"k-{i}")
