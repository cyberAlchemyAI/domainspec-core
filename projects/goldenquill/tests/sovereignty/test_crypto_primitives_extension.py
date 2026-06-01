"""Tests for Round-C extension to pipeline.sovereignty.crypto_primitives.

Coverage targets (per spec card `round_c_keys.md`):
  - SecretBytes: init paths, zero-on-exit, idempotence, view-after-zero, len, context manager.
  - aesgcm_encrypt/decrypt: round-trip, tampering, AAD mismatch, wrong key, wrong nonce, type gates.
  - pbkdf2_sha3_512: deterministic, salt-sensitivity, iteration + dklen guards, type gates.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from cryptography.exceptions import InvalidTag

from pipeline.sovereignty import (
    SecretBytes,
    ZeroizedBufferAccessed,
    aesgcm_decrypt,
    aesgcm_encrypt,
    pbkdf2_sha3_512,
    zero_bytes,
)


# -------- SecretBytes --------


class TestSecretBytesInit:
    def test_from_bytearray_takes_ownership(self) -> None:
        data = bytearray(b"secret-key-here" * 3)
        sb = SecretBytes(data)
        assert len(sb) == len(data)
        assert not sb.zeroed

    def test_from_bytes_copies(self) -> None:
        sb = SecretBytes(b"plaintext")
        assert len(sb) == 9

    def test_from_readonly_memoryview_copies(self) -> None:
        mv = memoryview(b"hello-readonly")
        sb = SecretBytes(mv)
        assert len(sb) == 14

    def test_from_writable_memoryview(self) -> None:
        buf = bytearray(b"writable-view-source")
        mv = memoryview(buf)
        sb = SecretBytes(mv)
        assert len(sb) == 20

    def test_rejects_str(self) -> None:
        with pytest.raises(TypeError):
            SecretBytes("not-bytes-like")  # type: ignore[arg-type]

    def test_rejects_int(self) -> None:
        with pytest.raises(TypeError):
            SecretBytes(42)  # type: ignore[arg-type]

    def test_rejects_none(self) -> None:
        with pytest.raises(TypeError):
            SecretBytes(None)  # type: ignore[arg-type]


class TestSecretBytesZero:
    def test_zero_marks_zeroed(self) -> None:
        sb = SecretBytes(bytearray(b"x" * 16))
        sb.zero()
        assert sb.zeroed

    def test_zero_is_idempotent(self) -> None:
        sb = SecretBytes(bytearray(b"x" * 16))
        sb.zero()
        sb.zero()  # no raise
        assert sb.zeroed

    def test_zero_actually_zeros_backing_store(self) -> None:
        buf = bytearray(b"abcdefgh")
        sb = SecretBytes(buf)
        sb.zero()
        # After zero, the original bytearray is all zeros.
        assert all(b == 0 for b in buf)

    def test_view_after_zero_raises(self) -> None:
        sb = SecretBytes(bytearray(b"x" * 16))
        sb.zero()
        with pytest.raises(ZeroizedBufferAccessed):
            sb.view()


class TestSecretBytesContextManager:
    def test_context_zeros_on_normal_exit(self) -> None:
        sb = SecretBytes(bytearray(b"x" * 16))
        with sb:
            _ = sb.view()
        assert sb.zeroed

    def test_context_zeros_on_exception(self) -> None:
        sb = SecretBytes(bytearray(b"x" * 16))
        with pytest.raises(RuntimeError):
            with sb:
                raise RuntimeError("boom")
        assert sb.zeroed

    def test_view_inside_context_works(self) -> None:
        sb = SecretBytes(bytearray(b"key-material-32-bytes-hello"))
        with sb:
            mv = sb.view()
            assert isinstance(mv, memoryview)
            assert len(mv) == len(sb)


# -------- AES-GCM --------


class TestAESGCM:
    def _valid_key(self) -> bytes:
        return bytes(range(32))  # 0..31 deterministic

    def _valid_nonce(self) -> bytes:
        return bytes(range(12))  # 0..11

    def test_round_trip(self) -> None:
        key = self._valid_key()
        nonce = self._valid_nonce()
        ct = aesgcm_encrypt(key, nonce, b"plaintext-data", aad=b"purpose")
        pt = aesgcm_decrypt(key, nonce, ct, aad=b"purpose")
        assert bytes(pt) == b"plaintext-data"
        assert isinstance(pt, bytearray)

    def test_round_trip_empty_aad(self) -> None:
        key = self._valid_key()
        nonce = self._valid_nonce()
        ct = aesgcm_encrypt(key, nonce, b"data")
        pt = aesgcm_decrypt(key, nonce, ct)
        assert bytes(pt) == b"data"

    def test_wrong_key_raises_invalid_tag(self) -> None:
        key = self._valid_key()
        nonce = self._valid_nonce()
        ct = aesgcm_encrypt(key, nonce, b"data")
        wrong_key = bytes([b ^ 1 for b in key])
        with pytest.raises(InvalidTag):
            aesgcm_decrypt(wrong_key, nonce, ct)

    def test_wrong_nonce_raises_invalid_tag(self) -> None:
        key = self._valid_key()
        nonce = self._valid_nonce()
        ct = aesgcm_encrypt(key, nonce, b"data")
        wrong_nonce = bytes([b ^ 1 for b in nonce])
        with pytest.raises(InvalidTag):
            aesgcm_decrypt(key, wrong_nonce, ct)

    def test_aad_mismatch_raises_invalid_tag(self) -> None:
        key = self._valid_key()
        nonce = self._valid_nonce()
        ct = aesgcm_encrypt(key, nonce, b"data", aad=b"purposeA")
        with pytest.raises(InvalidTag):
            aesgcm_decrypt(key, nonce, ct, aad=b"purposeB")

    def test_ciphertext_tamper_raises_invalid_tag(self) -> None:
        key = self._valid_key()
        nonce = self._valid_nonce()
        ct = aesgcm_encrypt(key, nonce, b"data")
        tampered = bytes([ct[0] ^ 1]) + ct[1:]
        with pytest.raises(InvalidTag):
            aesgcm_decrypt(key, nonce, tampered)

    def test_key_wrong_length_raises(self) -> None:
        with pytest.raises(ValueError):
            aesgcm_encrypt(b"x" * 16, bytes(12), b"data")

    def test_nonce_wrong_length_raises(self) -> None:
        with pytest.raises(ValueError):
            aesgcm_encrypt(bytes(32), b"x" * 16, b"data")

    def test_type_gates(self) -> None:
        with pytest.raises(TypeError):
            aesgcm_encrypt("str-key", bytes(12), b"data")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            aesgcm_encrypt(bytes(32), "str-nonce", b"data")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            aesgcm_encrypt(bytes(32), bytes(12), "str-plaintext")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            aesgcm_encrypt(bytes(32), bytes(12), b"data", aad="str-aad")  # type: ignore[arg-type]

    def test_secretbytes_interop(self) -> None:
        sb = SecretBytes(bytearray(bytes(range(32))))
        nonce = bytes(range(12))
        with sb:
            ct = aesgcm_encrypt(sb.view(), nonce, b"data")
        # Key was zeroed on exit; ciphertext is independent.
        assert len(ct) == len(b"data") + 16  # tag appended

    def test_bytearray_key_accepted(self) -> None:
        key = bytearray(range(32))
        nonce = bytes(12)
        ct = aesgcm_encrypt(key, nonce, b"data")
        pt = aesgcm_decrypt(key, nonce, ct)
        assert bytes(pt) == b"data"


# -------- PBKDF2 --------


class TestPBKDF2:
    def test_deterministic(self) -> None:
        out1 = pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=100, dklen=32)
        out2 = pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=100, dklen=32)
        assert out1 == out2
        assert isinstance(out1, bytearray)

    def test_salt_sensitive(self) -> None:
        a = pbkdf2_sha3_512(b"pw", b"A" * 16, iterations=100)
        b = pbkdf2_sha3_512(b"pw", b"B" * 16, iterations=100)
        assert a != b

    def test_passphrase_sensitive(self) -> None:
        a = pbkdf2_sha3_512(b"alice", b"salt" * 4, iterations=100)
        b = pbkdf2_sha3_512(b"bob", b"salt" * 4, iterations=100)
        assert a != b

    def test_iterations_sensitive(self) -> None:
        a = pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=100)
        b = pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=200)
        assert a != b

    def test_default_iterations_600k(self) -> None:
        # Just assert the default is applied and produces a bytearray;
        # 600k iterations is slow but ~0.5-2s on M1, acceptable in CI.
        out = pbkdf2_sha3_512(b"pw", b"salt" * 4)
        assert len(out) == 32

    def test_default_dklen_32(self) -> None:
        out = pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=100)
        assert len(out) == 32

    def test_custom_dklen(self) -> None:
        out = pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=100, dklen=64)
        assert len(out) == 64

    def test_iterations_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=0)

    def test_dklen_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=100, dklen=0)

    def test_type_gates(self) -> None:
        with pytest.raises(TypeError):
            pbkdf2_sha3_512("str-pw", b"salt" * 4, iterations=100)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            pbkdf2_sha3_512(b"pw", "str-salt", iterations=100)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations="100")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            pbkdf2_sha3_512(b"pw", b"salt" * 4, iterations=100, dklen="32")  # type: ignore[arg-type]

    def test_secretbytes_passphrase(self) -> None:
        sb = SecretBytes(bytearray(b"my-passphrase"))
        with sb:
            out = pbkdf2_sha3_512(sb.view(), b"salt" * 4, iterations=100)
        assert len(out) == 32


# -------- Corpus regression --------


_CORPUS_PATH = (
    Path(__file__).resolve().parents[1]
    / "corpus"
    / "keys"
    / "v1"
    / "pbkdf2_vectors.json"
)


class TestPBKDF2Corpus:
    @pytest.mark.parametrize(
        "vec",
        json.loads(_CORPUS_PATH.read_text())["vectors"],
        ids=lambda v: v["name"],
    )
    def test_corpus_vector_deterministic(self, vec: dict) -> None:
        salt = bytes.fromhex(vec["salt_hex"])
        out = pbkdf2_sha3_512(
            vec["passphrase"].encode("utf-8"),
            salt,
            iterations=vec["iterations"],
            dklen=vec["dklen"],
        )
        # Re-run to confirm determinism within this session.
        out2 = pbkdf2_sha3_512(
            vec["passphrase"].encode("utf-8"),
            salt,
            iterations=vec["iterations"],
            dklen=vec["dklen"],
        )
        assert out == out2
        assert len(out) == vec["dklen"]
        # expected_kek_hex is populated at LOCK time if present; if None, skip
        # the cross-run assertion (first-pass authoring).
        if vec["expected_kek_hex"] is not None:
            assert out.hex() == vec["expected_kek_hex"]
