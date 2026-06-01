"""Crypto primitives for Section 1. [§5.1 BT1, §2.1, §4.6 M7, §5.4 BT4, §8 FILE_KEYSTORE_*]

Round-A v1 public surface: SHA-3-512 hash + HMAC + constant_time_equal + zero_bytes.
Round-C v2 extension: SecretBytes mutable-secret context manager + AES-256-GCM
(aesgcm_encrypt / aesgcm_decrypt) + PBKDF2-HMAC-SHA3-512 (pbkdf2_sha3_512). New
extensions service §4.6 v2 SecretBytes contract + §5.4 BT4 FileKeyStore KEK
derivation and AES-GCM envelope. Backward-compatible — Round-A 103 tests unchanged.

OUT-OF-MODEL: same-uid hostile Python / side-channel attacks / post-quantum break of SHA-3.
"""

from __future__ import annotations

import hashlib
import hmac as _stdlib_hmac
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM as _AESGCM

from pipeline.sovereignty._types import HashDigest, HashPair

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§5.1 BT1",
            "§4.6.1 M7 HMAC helper",
            "§4.6 v2 SecretBytes (Round-C extension)",
            "§5.4 BT4 AES-GCM + PBKDF2 primitives (Round-C extension)",
        ],
        "hash_at_lock": None,  # populated at committee LOCK
        "hash_source_version": "v6",
    },
}

__all__ = [
    # Round A public surface (LOCKED)
    "sha3_512_hex",
    "sha3_512_with_nonce",
    "verify_sha3_512_with_nonce",
    "hmac_sha3_512",
    "constant_time_equal",
    "zero_bytes",
    # Round C extension public surface (§4.6 v2 + §5.4 BT4)
    "SecretBytes",
    "ZeroizedBufferAccessed",
    "aesgcm_encrypt",
    "aesgcm_decrypt",
    "pbkdf2_sha3_512",
]

# --- Algorithm identifiers (A12 crypto-agility) ---
# Downstream dispatches on these strings; they are NOT string literals scattered
# across the codebase. One place to add new algorithms when v0.2/v0.3 lands.
_ALGO_SHA3_512 = "sha3-512"
_ALGO_SHA3_512_NONCE = "sha3-512-nonce"

# --- BT1 constants ---
# Nonce size pinned at 32 bytes per blueprint §5.1 ("256 bits of entropy").
# Never read from caller input.
_BT1_NONCE_BYTES = 32

# HMAC-SHA3-512 expected output length (bytes) — SHA-3-512 digest is 64 bytes.
_HMAC_SHA3_512_LEN = 64

# Minimum HMAC key bytes. Per blueprint §4.6 M7 + §8 FD_BROKER_HMAC_KEY_LENGTH_BYTES.
# Enforced by default at the primitive layer (Round-A retry RT-v1-M-01 closure).
# Callers who legitimately need a shorter key may override via `min_key_bytes` kwarg.
_DEFAULT_MIN_HMAC_KEY_BYTES = 32

# --- Round-C constants (§5.4 BT4 + §8) ---
_AESGCM_KEY_BYTES = 32           # AES-256 — per §8 FILE_KEYSTORE_KEK_BYTES
_AESGCM_NONCE_BYTES = 12         # GCM standard — per §8 FILE_KEYSTORE_AEAD_NONCE_BYTES
_AESGCM_TAG_BYTES = 16           # GCM authentication tag
_PBKDF2_DEFAULT_ITERATIONS = 600_000  # per §8 FILE_KEYSTORE_PBKDF2_ITERATIONS
_PBKDF2_DEFAULT_DKLEN = 32       # 32-byte KEK default (matches _AESGCM_KEY_BYTES)
_PBKDF2_HASH_NAME = "sha3_512"   # E-002 lowercase case-discipline identifier


def sha3_512_hex(data: bytes) -> HashDigest:
    """Plain SHA-3-512 over `data`, returned as a HashDigest.

    No nonce injection. Used when the caller needs a content hash without the
    BT1 envelope (e.g., for signing a canonical-bytes-serialized struct).

    [§5.1 BT1 derivative — "no-nonce" variant]

    :param data: input bytes
    :returns: HashDigest(algorithm="sha3-512", digest_hex=<128 hex chars>, nonce_hex="")
    :raises TypeError: if `data` is not bytes (enforced via isinstance; never "should not happen")
    """
    if not isinstance(data, bytes):
        raise TypeError(
            f"sha3_512_hex requires bytes; got {type(data).__name__}"
        )
    return HashDigest(
        algorithm=_ALGO_SHA3_512,
        digest_hex=hashlib.sha3_512(data).hexdigest(),
        nonce_hex="",
    )


def sha3_512_with_nonce(content: bytes) -> HashDigest:
    """Compute SHA-3-512 over (content || nonce). [§5.1 BT1]

    Generates a fresh 32-byte nonce via secrets.token_bytes(32). The nonce
    is OS-CSPRNG-sourced; never caller-supplied per BT1 contract.

    :param content: the payload bytes to hash
    :returns: HashDigest(algorithm="sha3-512-nonce", digest_hex=<128 hex>,
              nonce_hex=<64 hex>)
    :raises TypeError: if content is not bytes

    The nonce is carried back to the caller (in `nonce_hex`) so re-verification
    via verify_sha3_512_with_nonce can reproduce the digest.
    """
    if not isinstance(content, bytes):
        raise TypeError(
            f"sha3_512_with_nonce requires bytes; got {type(content).__name__}"
        )
    nonce = secrets.token_bytes(_BT1_NONCE_BYTES)
    digest = hashlib.sha3_512(content + nonce).hexdigest()
    return HashDigest(
        algorithm=_ALGO_SHA3_512_NONCE,
        digest_hex=digest,
        nonce_hex=nonce.hex(),
    )


def verify_sha3_512_with_nonce(
    content: bytes,
    *,
    expected: HashDigest,
) -> bool:
    """Verify a BT1 hash pair. [§5.1 BT1 — re-verification path]

    Re-runs the hash over (content || nonce_from_expected) and compares the
    result to expected.digest_hex using a constant-time comparison.

    :param content: the payload bytes to hash
    :param expected: the HashDigest to verify against; must carry algorithm
                     "sha3-512-nonce" and a 64-hex-char nonce
    :returns: True on match, False on mismatch
    :raises TypeError: if arguments are wrong types
    :raises ValueError: if expected.algorithm is not "sha3-512-nonce" or if
                        nonce_hex is not 64 hex chars
    """
    if not isinstance(content, bytes):
        raise TypeError(
            f"verify_sha3_512_with_nonce: content must be bytes; got "
            f"{type(content).__name__}"
        )
    if not isinstance(expected, HashDigest):
        raise TypeError(
            f"verify_sha3_512_with_nonce: expected must be HashDigest; got "
            f"{type(expected).__name__}"
        )
    if expected.algorithm != _ALGO_SHA3_512_NONCE:
        raise ValueError(
            f"verify_sha3_512_with_nonce: expected.algorithm must be "
            f"'{_ALGO_SHA3_512_NONCE}'; got {expected.algorithm!r}"
        )
    if len(expected.nonce_hex) != _BT1_NONCE_BYTES * 2:
        raise ValueError(
            f"verify_sha3_512_with_nonce: expected.nonce_hex must be "
            f"{_BT1_NONCE_BYTES * 2} hex chars; got {len(expected.nonce_hex)}"
        )
    # Round-A Committee finding RT-v1-L-01 (GPT-OSS-120B 2026-04-19):
    # validate digest_hex shape too — SHA-3-512 output is 128 hex chars.
    # Without this check, a malformed HashDigest could pass type checks
    # but produce silent verification failure OR coincidentally match
    # a truncation of the correct digest. Guarding the shape eliminates
    # that ambiguity and surfaces the error as a ValueError.
    if len(expected.digest_hex) != 128:
        raise ValueError(
            f"verify_sha3_512_with_nonce: expected.digest_hex must be "
            f"128 hex chars (SHA-3-512); got {len(expected.digest_hex)}"
        )
    try:
        bytes.fromhex(expected.digest_hex)
    except ValueError as e:
        raise ValueError(
            "verify_sha3_512_with_nonce: expected.digest_hex is not valid hex"
        ) from e
    try:
        nonce = bytes.fromhex(expected.nonce_hex)
    except ValueError as e:
        raise ValueError(
            "verify_sha3_512_with_nonce: expected.nonce_hex is not valid hex"
        ) from e
    actual_digest = hashlib.sha3_512(content + nonce).hexdigest()
    return constant_time_equal(
        actual_digest.encode("ascii"),
        expected.digest_hex.encode("ascii"),
    )


def hmac_sha3_512(
    key: bytes,
    data: bytes,
    *,
    min_key_bytes: int = _DEFAULT_MIN_HMAC_KEY_BYTES,
) -> bytes:
    """Compute HMAC-SHA3-512(key, data). [§4.6.1 M7 primitive]

    :param key: HMAC key bytes. Default floor is 32 bytes (per blueprint §4.6 M7
                + §8 FD_BROKER_HMAC_KEY_LENGTH_BYTES). Callers who legitimately
                need a shorter key (rare) can override via `min_key_bytes` kwarg.
                Round-A retry RT-v1-M-01 resolution: primitive enforces by default
                so accidental short-key use by callers fails loudly at the primitive
                layer; override is explicit and reviewable.
    :param data: message bytes; MUST be pre-canonicalized when used for
                 §4.6.1 wire-protocol signing (canonicalization is a
                 caller-side concern, not this primitive's).
    :param min_key_bytes: minimum accepted key length in bytes. Default 32.
                 Set to 1 (or any value ≥ 1) to accept shorter keys; set to a
                 larger value to enforce a stricter policy at the call site.
                 Must be ≥ 1 (empty keys always rejected).
    :returns: 64 raw bytes (not hex) — the HMAC output. Hex encoding is
              a caller-side concern.
    :raises TypeError: if arguments are wrong types
    :raises ValueError: if key length < min_key_bytes
    """
    if not isinstance(key, bytes):
        raise TypeError(
            f"hmac_sha3_512 key must be bytes; got {type(key).__name__}"
        )
    if not isinstance(data, bytes):
        raise TypeError(
            f"hmac_sha3_512 data must be bytes; got {type(data).__name__}"
        )
    if not isinstance(min_key_bytes, int) or isinstance(min_key_bytes, bool):
        raise TypeError(
            f"hmac_sha3_512 min_key_bytes must be int; got "
            f"{type(min_key_bytes).__name__}"
        )
    if min_key_bytes < 1:
        raise ValueError(
            f"hmac_sha3_512 min_key_bytes must be >= 1; got {min_key_bytes}"
        )
    if len(key) < min_key_bytes:
        raise ValueError(
            f"hmac_sha3_512 key must be >= {min_key_bytes} bytes; "
            f"got {len(key)}"
        )
    result = _stdlib_hmac.new(key, data, hashlib.sha3_512).digest()
    assert len(result) == _HMAC_SHA3_512_LEN, (
        "sha3_512 digest size invariant broken — hashlib regression"
    )
    return result


def constant_time_equal(a: bytes, b: bytes) -> bool:
    """Constant-time byte-sequence comparison. [§4.6.1 M7 primitive]

    Wraps hmac.compare_digest for clarity — the caller should never use `==`
    for comparing hashes, MACs, or tokens. This function is the one True
    Path.

    :param a, b: bytes to compare. Do NOT pass str (timing depends on the
                 `!=` compare becoming O(min(len)) vs O(len)). str equality
                 in Python uses == which is NOT constant time.
    :returns: True if equal, False if not (including different lengths)
    :raises TypeError: if either argument is not bytes
    """
    if not isinstance(a, bytes) or not isinstance(b, bytes):
        raise TypeError(
            f"constant_time_equal requires bytes for both arguments; got "
            f"{type(a).__name__}, {type(b).__name__}"
        )
    return _stdlib_hmac.compare_digest(a, b)


def zero_bytes(buf: bytearray | memoryview) -> None:
    """Overwrite a mutable byte buffer with zeros in place.

    Secure-erase analogue for bytearray or writable memoryview. Callers
    holding sensitive key material should call this when done, then drop
    the reference. This is BEST EFFORT — Python GC may have already
    duplicated the bytes elsewhere (immutable `bytes` objects cannot be
    zeroed, which is why this primitive refuses them).

    [§5.1 SecretBytes helper surface — the explicit "do not handle secrets
    as immutable bytes" discipline.]

    :param buf: bytearray or writable memoryview. NOT bytes (immutable).
    :raises TypeError: if buf is bytes, str, or any non-mutable sequence.
    """
    if isinstance(buf, (bytes, str)):
        raise TypeError(
            f"zero_bytes cannot zero immutable type {type(buf).__name__}; "
            f"use bytearray or a writable memoryview for sensitive material"
        )
    if isinstance(buf, bytearray):
        for i in range(len(buf)):
            buf[i] = 0
        return
    if isinstance(buf, memoryview):
        if buf.readonly:
            raise TypeError(
                "zero_bytes cannot zero a read-only memoryview"
            )
        for i in range(len(buf)):
            buf[i] = 0
        return
    raise TypeError(
        f"zero_bytes requires bytearray or writable memoryview; got "
        f"{type(buf).__name__}"
    )


def _derive_hashpair_from_url_and_content(
    url: str,
    content: bytes,
) -> HashPair:
    """Compose §2.1 HashPair from raw inputs.

    Internal helper — the public surface for ingesting an RFA is
    `rfa_envelope.py` (later round). This function exists here because
    it uses only crypto primitives and isolates the dual-hash construction
    for the test suite.

    url_hash: SHA-3-512 of url.encode("utf-8"). No nonce.
    content_hash: BT1 form — SHA-3-512 of (content || nonce).
    algorithm: "SHA3-512" per §2.1.
    nonce_hex: 64 hex chars from secrets.token_bytes(32).

    [§2.1 HashPair + §5.1 BT1]
    """
    if not isinstance(url, str):
        raise TypeError(
            f"_derive_hashpair: url must be str; got {type(url).__name__}"
        )
    if not isinstance(content, bytes):
        raise TypeError(
            f"_derive_hashpair: content must be bytes; got "
            f"{type(content).__name__}"
        )
    url_hash = hashlib.sha3_512(url.encode("utf-8")).hexdigest()
    content_digest = sha3_512_with_nonce(content)
    return HashPair(
        url_hash=url_hash,
        content_hash=content_digest.digest_hex,
        # Round-A retry (Gemini finding): algorithm identifier normalized to
        # lowercase for dispatcher consistency with HashDigest. Blueprint §2.1
        # specifies "SHA3-512" uppercase — drift noted at D-09; v6.1 backfill
        # should lowercase the blueprint spec too, OR introduce an explicit
        # case-normalization step at load time. Lowercase is the canonical
        # identifier per _ALGO_SHA3_512.
        algorithm=_ALGO_SHA3_512,
        nonce_hex=content_digest.nonce_hex,
    )


# ===================================================================
# Round-C v2 extension — SecretBytes + AES-GCM + PBKDF2
# Blueprint: §4.6 v2 SecretBytes, §5.4 BT4 FileKeyStore primitives, §8 constants.
# Backward-compatible extension of Round-A public surface.
# ===================================================================


class ZeroizedBufferAccessed(RuntimeError):
    """SecretBytes.view() called after zero(). [§4.6 v2]"""


class SecretBytes:
    """Mutable secret buffer, zeros in-place on __exit__ or explicit zero(). [§4.6 v2]

    Built on bytearray + memoryview so HMAC / AEAD primitives can read the key
    via memoryview without copying into immutable bytes. `with` block zeroes on
    exit including on exception. Subsequent `view()` raises ZeroizedBufferAccessed.
    Idempotent zero().
    """

    __slots__ = ("_buf", "_view", "_zeroed")

    def __init__(self, data: bytes | bytearray | memoryview) -> None:
        if isinstance(data, bytes):
            # Round-C committee note: accepting immutable bytes requires one copy.
            # The original immutable object lives in the caller's scope for the
            # lifetime the caller holds it — caller responsibility to not pass
            # long-lived secret bytes in the first place. SecretBytes itself is
            # zero-able from this point forward.
            self._buf = bytearray(data)
        elif isinstance(data, bytearray):
            # Move semantics — SecretBytes takes ownership; callers should drop
            # their reference after wrapping.
            self._buf = data
        elif isinstance(data, memoryview):
            if data.readonly:
                self._buf = bytearray(data.tobytes())
            else:
                self._buf = bytearray(data)
        else:
            raise TypeError(
                f"SecretBytes requires bytes | bytearray | memoryview; got "
                f"{type(data).__name__}"
            )
        self._view = memoryview(self._buf)
        self._zeroed = False

    def view(self) -> memoryview:
        """Return a memoryview into the mutable backing store.

        Callers pass this into `hmac_sha3_512(key.view(), data)` or AES-GCM,
        keeping the key in mutable-buffer form all the way through.
        Raises ZeroizedBufferAccessed if already zeroed.
        """
        if self._zeroed:
            raise ZeroizedBufferAccessed("SecretBytes already zeroed")
        return self._view

    def zero(self) -> None:
        """Overwrite backing store with zeros. Idempotent."""
        if self._zeroed:
            return
        # Release the active memoryview first — Python does not allow resizing
        # (or, on some paths, reassigning) a bytearray while a memoryview is
        # active. Writing zeros byte-by-byte is safe with an active view, but
        # we release the view reference first to be defensive against future
        # internal-buffer operations.
        self._view.release()
        for i in range(len(self._buf)):
            self._buf[i] = 0
        self._view = memoryview(self._buf)
        self._zeroed = True

    def __enter__(self) -> "SecretBytes":
        return self

    def __exit__(self, *_: object) -> None:
        self.zero()

    def __len__(self) -> int:
        return len(self._buf)

    @property
    def zeroed(self) -> bool:
        """True if zero() has been called."""
        return self._zeroed


def aesgcm_encrypt(
    key: bytes | bytearray | memoryview,
    nonce: bytes,
    plaintext: bytes,
    aad: bytes = b"",
) -> bytes:
    """AES-256-GCM encrypt. [§5.4 BT4]

    :param key: 32 bytes (AES-256). Accepts bytes / bytearray / memoryview for
                SecretBytes interop.
    :param nonce: 12 bytes (GCM standard).
    :param plaintext: payload bytes.
    :param aad: additional authenticated data (default empty).
    :returns: ciphertext || 16-byte-tag as bytes.
    :raises TypeError: on wrong arg types.
    :raises ValueError: on wrong key / nonce length.
    """
    # E-001 type gate.
    if not isinstance(key, (bytes, bytearray, memoryview)):
        raise TypeError(
            f"aesgcm_encrypt key must be bytes|bytearray|memoryview; got {type(key).__name__}"
        )
    if not isinstance(nonce, bytes):
        raise TypeError(
            f"aesgcm_encrypt nonce must be bytes; got {type(nonce).__name__}"
        )
    if not isinstance(plaintext, bytes):
        raise TypeError(
            f"aesgcm_encrypt plaintext must be bytes; got {type(plaintext).__name__}"
        )
    if not isinstance(aad, bytes):
        raise TypeError(
            f"aesgcm_encrypt aad must be bytes; got {type(aad).__name__}"
        )
    if len(key) != _AESGCM_KEY_BYTES:
        raise ValueError(
            f"aesgcm_encrypt key must be {_AESGCM_KEY_BYTES} bytes; got {len(key)}"
        )
    if len(nonce) != _AESGCM_NONCE_BYTES:
        raise ValueError(
            f"aesgcm_encrypt nonce must be {_AESGCM_NONCE_BYTES} bytes; got {len(nonce)}"
        )
    # cryptography's AESGCM accepts bytes-like via bytes() conversion; we convert
    # from memoryview to bytes here intentionally because AESGCM internally
    # memcpy's the key regardless (C-library contract); SecretBytes remains
    # zeroable post-call.
    if isinstance(key, memoryview):
        key_bytes = bytes(key)
    elif isinstance(key, bytearray):
        key_bytes = bytes(key)
    else:
        key_bytes = key
    aead = _AESGCM(key_bytes)
    return aead.encrypt(nonce, plaintext, aad if aad else None)


def aesgcm_decrypt(
    key: bytes | bytearray | memoryview,
    nonce: bytes,
    ciphertext: bytes,
    aad: bytes = b"",
) -> bytearray:
    """AES-256-GCM decrypt. [§5.4 BT4]

    Returns bytearray (mutable, §3.11 contract — caller can wrap in SecretBytes
    for zero-on-exit).

    :raises cryptography.exceptions.InvalidTag: MAC failure. Caller maps to KeyCorrupt (F-KEY-05).
    :raises TypeError: on wrong arg types.
    :raises ValueError: on wrong key / nonce length.
    """
    if not isinstance(key, (bytes, bytearray, memoryview)):
        raise TypeError(
            f"aesgcm_decrypt key must be bytes|bytearray|memoryview; got {type(key).__name__}"
        )
    if not isinstance(nonce, bytes):
        raise TypeError(
            f"aesgcm_decrypt nonce must be bytes; got {type(nonce).__name__}"
        )
    if not isinstance(ciphertext, bytes):
        raise TypeError(
            f"aesgcm_decrypt ciphertext must be bytes; got {type(ciphertext).__name__}"
        )
    if not isinstance(aad, bytes):
        raise TypeError(
            f"aesgcm_decrypt aad must be bytes; got {type(aad).__name__}"
        )
    if len(key) != _AESGCM_KEY_BYTES:
        raise ValueError(
            f"aesgcm_decrypt key must be {_AESGCM_KEY_BYTES} bytes; got {len(key)}"
        )
    if len(nonce) != _AESGCM_NONCE_BYTES:
        raise ValueError(
            f"aesgcm_decrypt nonce must be {_AESGCM_NONCE_BYTES} bytes; got {len(nonce)}"
        )
    if isinstance(key, memoryview):
        key_bytes = bytes(key)
    elif isinstance(key, bytearray):
        key_bytes = bytes(key)
    else:
        key_bytes = key
    aead = _AESGCM(key_bytes)
    plaintext = aead.decrypt(nonce, ciphertext, aad if aad else None)
    # Blueprint §3.11 v3 contract: _retrieve_raw-ish returns bytearray. AESGCM.decrypt
    # emits bytes; we wrap once. The intermediate `plaintext` bytes object lives
    # for one stack frame; accepted trusted-operator boundary cost.
    return bytearray(plaintext)


def pbkdf2_sha3_512(
    passphrase: bytes | bytearray | memoryview,
    salt: bytes,
    iterations: int = _PBKDF2_DEFAULT_ITERATIONS,
    dklen: int = _PBKDF2_DEFAULT_DKLEN,
) -> bytearray:
    """PBKDF2-HMAC-SHA3-512 → bytearray KEK. [§5.4 BT4, §8 FILE_KEYSTORE_PBKDF2_ITERATIONS]

    :param passphrase: bytes / bytearray / memoryview. SecretBytes interop via view().
    :param salt: bytes.
    :param iterations: default 600_000 per §8 (OWASP 2024).
    :param dklen: derived-key length in bytes; default 32 (AES-256 KEK).
    :returns: bytearray of length `dklen`.
    :raises TypeError: on wrong arg types.
    :raises ValueError: on iterations < 1 or dklen < 1.
    """
    if not isinstance(passphrase, (bytes, bytearray, memoryview)):
        raise TypeError(
            f"pbkdf2_sha3_512 passphrase must be bytes|bytearray|memoryview; got {type(passphrase).__name__}"
        )
    if not isinstance(salt, bytes):
        raise TypeError(
            f"pbkdf2_sha3_512 salt must be bytes; got {type(salt).__name__}"
        )
    if not isinstance(iterations, int) or isinstance(iterations, bool):
        raise TypeError(
            f"pbkdf2_sha3_512 iterations must be int; got {type(iterations).__name__}"
        )
    if not isinstance(dklen, int) or isinstance(dklen, bool):
        raise TypeError(
            f"pbkdf2_sha3_512 dklen must be int; got {type(dklen).__name__}"
        )
    if iterations < 1:
        raise ValueError(
            f"pbkdf2_sha3_512 iterations must be >= 1; got {iterations}"
        )
    if dklen < 1:
        raise ValueError(
            f"pbkdf2_sha3_512 dklen must be >= 1; got {dklen}"
        )
    # hashlib.pbkdf2_hmac accepts bytes-like via bytes() conversion.
    if isinstance(passphrase, memoryview):
        pw_bytes = bytes(passphrase)
    elif isinstance(passphrase, bytearray):
        pw_bytes = bytes(passphrase)
    else:
        pw_bytes = passphrase
    derived = hashlib.pbkdf2_hmac(_PBKDF2_HASH_NAME, pw_bytes, salt, iterations, dklen)
    return bytearray(derived)
