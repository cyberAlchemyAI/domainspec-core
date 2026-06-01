"""KeyStore ABC + concrete stores + nonce registry. [§3.11, §5.4 BT4, §4.6 M7, §6.6 F-KEY-*, §8]

Provider dispatch via `resolve_keystore()` + `TILTH_KEYSTORE_PROVIDER` env var. Three
concretes: MacOSKeychainKeyStore (security CLI), FileKeyStore (PBKDF2+AES-GCM), YubiHSMKeyStore
stub. ABC seals `retrieve()` via @typing.final + __init_subclass__ per §3.11 v4 RT-v3 HIGH-2
closure. Nonce registry implements §5.4 BT4 v2/v3/v4 (segmented, rolling HMAC chain, pre-gen
size-check rotation).

Keystore-consumer contract: every key value crosses the boundary as SecretBytes wrapping
bytearray (§3.11 v3 HIGH-3 closure). _retrieve_raw returns bytearray; retrieve() wraps in
SecretBytes; subclasses cannot override retrieve() (F-KEY-10 class-def-time assertion).

OUT-OF-MODEL: same-uid hostile Python / ctypes / metaclass bypass (§3.11 v5 trust-boundary note).
"""

from __future__ import annotations

import abc
import errno
import fcntl
import json
import os
import platform
import secrets
import shutil
import subprocess
import time
import typing
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from cryptography.exceptions import InvalidTag

from pipeline.sovereignty.crypto_primitives import (
    SecretBytes,
    aesgcm_decrypt,
    aesgcm_encrypt,
    constant_time_equal,
    hmac_sha3_512,
    pbkdf2_sha3_512,
    sha3_512_hex,
    zero_bytes,
)
from pipeline.sovereignty.org_slug import canonical_slug

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§3.11 KeyStore ABC v4 sealed",
            "§3.11 v3 HIGH-3 SecretBytes contract",
            "§4.6 M7 HMAC key lifecycle (v2 SecretBytes)",
            "§5.4 BT4 MacOSKeychain + FileKeyStore + YubiHSM stub",
            "§5.4 BT4 v3 nonce registry + rolling HMAC chain",
            "§5.4 BT4 v4 pre-gen size-check rotation",
            "§6.6 F-KEY-01..10",
            "§8 KEYCHAIN_SERVICE_TEMPLATE / NONCE_REGISTRY_* / FILE_KEYSTORE_*",
        ],
        "hash_at_lock": None,
        "hash_source_version": "v6",
    },
}

__all__ = [
    # Exceptions (§6.6)
    "KeyStoreConfigError",
    "KeychainLockedError",
    "KeyStoreUnavailable",
    "FileKeyStoreUnavailable",
    "KeyCorrupt",
    "NonceReused",
    "KeyStoreContractViolation",
    "NonceRegistryOverSizeLimit",
    "NonceRegistryTrailerMismatch",
    "NonceRegistryRotationFailed",
    "NonceRegistryTruncated",
    # Primary surface
    "KeyStore",
    "MacOSKeychainKeyStore",
    "FileKeyStore",
    "YubiHSMKeyStore",
    "resolve_keystore",
    # Constants (§8)
    "KEYCHAIN_SERVICE_TEMPLATE",
    "NONCE_REGISTRY_SIZE_LIMIT_BYTES",
    "TILTH_KEYSTORE_PROVIDER_ENV",
    "TILTH_FILE_KEYSTORE_PASSPHRASE_ENV",
]

# --- Constants (§8 pinned values) ---
KEYCHAIN_SERVICE_TEMPLATE: str = "com.goldenquill.tilth.{slug}"
NONCE_REGISTRY_SIZE_LIMIT_BYTES: int = 10 * 1024 * 1024  # 10 MiB per §8
TILTH_KEYSTORE_PROVIDER_ENV: str = "TILTH_KEYSTORE_PROVIDER"
TILTH_FILE_KEYSTORE_PASSPHRASE_ENV: str = "TILTH_FILE_KEYSTORE_PASSPHRASE"

_FILE_KEYSTORE_SALT_BYTES = 16  # per §8 FILE_KEYSTORE_SALT_BYTES
_FILE_KEYSTORE_KEK_BYTES = 32  # per §8 FILE_KEYSTORE_KEK_BYTES
_AESGCM_NONCE_BYTES = 12
_AEAD_FILE_SUFFIX = ".aead"

_PROVIDER_KEYCHAIN = "keychain"
_PROVIDER_FILE = "file"
_PROVIDER_YUBIHSM = "yubihsm"

_VALID_PROVIDERS: frozenset[str] = frozenset(
    {_PROVIDER_KEYCHAIN, _PROVIDER_FILE, _PROVIDER_YUBIHSM}
)

# Nonce registry schema
_NONCE_REGISTRY_SCHEMA_VERSION = "v1"
_NONCE_REGISTRY_GENESIS_PREV = "0" * 128

# Security CLI marker strings for keychain-locked detection
_KEYCHAIN_LOCKED_MARKERS: tuple[str, ...] = (
    "User interaction is not allowed",
    "keychain is locked",
    "could not be found in the current keychain",  # NOT a lock — handled separately
)


# -------- Exceptions (§6.6) --------


class KeyStoreConfigError(RuntimeError):
    """Unknown provider or config error. [F-KEY-01]"""


class KeychainLockedError(RuntimeError):
    """Keychain locked; operator must unlock. [F-KEY-02]"""


class KeyStoreUnavailable(RuntimeError):
    """Selected provider cannot initialize. [F-KEY-03] NEVER silent fallback."""


class FileKeyStoreUnavailable(KeyStoreUnavailable):
    """FileKeyStore passphrase missing. [F-KEY-04]"""


class KeyCorrupt(RuntimeError):
    """Key material corrupt / MAC-failed / unexpected length. [F-KEY-05]"""


class NonceReused(RuntimeError):
    """PRNG-violation signal. [F-KEY-07]"""


class KeyStoreContractViolation(TypeError):
    """Subclass emitted non-bytearray OR attempted to override retrieve(). [F-KEY-08 + F-KEY-10]"""


class NonceRegistryOverSizeLimit(RuntimeError):
    """Registry size would exceed limit without rotation. [F-KEY-09 variant]"""


class NonceRegistryTrailerMismatch(RuntimeError):
    """Rolling HMAC chain across segments broken. [F-KEY-09 variant]"""


class NonceRegistryRotationFailed(RuntimeError):
    """Rotation attempt failed pre-nonce-generation. [F-KEY-09 variant v4 RT-v3 MED-1]"""


class NonceRegistryTruncated(RuntimeError):
    """A segment file was deleted or truncated. [F-KEY-09 variant]"""


# -------- Lock discipline (local subset; cf. Round-B audit.py) --------


@contextmanager
def _acquire_exclusive_lock(lock_path: Path) -> Iterator[int]:
    """fcntl.LOCK_EX on lock_path with O_NOFOLLOW. [§8 LOCK_FILE_OPEN_FLAGS]"""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW
    try:
        fd = os.open(lock_path, flags, 0o600)
    except OSError as e:
        if e.errno == errno.ELOOP:
            raise RuntimeError(
                f"lock_file_symlink_attack: {lock_path} is a symlink"
            ) from e
        raise
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield fd
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def _atomic_write_bytes(target: Path, payload: bytes) -> None:
    """tmp → fsync → rename → fsync parent."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    with open(tmp, "wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    os.rename(tmp, target)
    parent_fd = os.open(target.parent, os.O_RDONLY)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def _canonical_json_bytes(obj: object) -> bytes:
    """Deterministic JSON — matches audit.py pattern; duplicated per §4.1."""
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _iso_utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


# -------- KeyStore ABC (§3.11 v4 sealed) --------


class KeyStore(abc.ABC):
    """Abstract keystore. retrieve() is SEALED. [§3.11 v4]"""

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Reject subclasses that attempt to override sealed retrieve(). [F-KEY-10]

        Inspects cls.__dict__ (class-local, not inherited). Runs inside
        type.__init__ before any instance can be constructed.
        """
        super().__init_subclass__(**kwargs)
        if "retrieve" in cls.__dict__:
            raise KeyStoreContractViolation(
                f"{cls.__name__} attempts to override KeyStore.retrieve(), which "
                "is sealed (@typing.final). Subclasses must override _retrieve_raw "
                "only. RT-v3 HIGH-2 closure — do not bypass the SecretBytes wrap."
            )

    @abc.abstractmethod
    def _retrieve_raw(self, key_id: str) -> bytearray:
        """MUST return bytearray. Never bytes. [§3.11 v3 HIGH-3]"""
        ...

    @typing.final
    def retrieve(self, key_id: str) -> SecretBytes:
        """SEALED public surface. Wraps _retrieve_raw output in SecretBytes. [§3.11 v4]

        Raises KeyStoreContractViolation (F-KEY-08) if _retrieve_raw returns
        anything other than bytearray.
        """
        raw = self._retrieve_raw(key_id)
        if not isinstance(raw, bytearray):
            raise KeyStoreContractViolation(
                f"{type(self).__name__}._retrieve_raw returned {type(raw).__name__}; "
                "must be bytearray. RT-v2 HIGH-3 closure — do not bypass."
            )
        return SecretBytes(raw)

    @abc.abstractmethod
    def store(
        self, *, key_id: str, key_bytes: bytes | bytearray, purpose: str
    ) -> None: ...

    @abc.abstractmethod
    def rotate(self, key_id: str) -> str:
        """Returns new key_id for rotated material."""
        ...

    @abc.abstractmethod
    def zero(self, key_id: str) -> None: ...

    @abc.abstractmethod
    def exists(self, key_id: str) -> bool: ...

    @abc.abstractmethod
    def provider(self) -> str:
        """'keychain' | 'file' | 'yubihsm'."""
        ...


# -------- MacOSKeychainKeyStore (§5.4 BT4) --------


class MacOSKeychainKeyStore(KeyStore):
    """macOS `security` CLI subprocess wrapper. [§5.4 BT4, §3.11]"""

    def __init__(self, slug: str, *, security_cli_path: str | None = None) -> None:
        """Bind to a canonicalized org slug. [§8 KEYCHAIN_SERVICE_TEMPLATE]

        :raises ValueError: slug is not canonical (defensive per Round-B topology pattern).
        :raises KeyStoreUnavailable: security CLI not present / not executable.
        """
        if not isinstance(slug, str):
            raise TypeError(f"slug must be str; got {type(slug).__name__}")
        # Round-B topology pattern — loud fail on non-canonical slug.
        canon = canonical_slug(slug)
        if canon != slug:
            raise ValueError(
                f"MacOSKeychainKeyStore: slug {slug!r} is not canonical "
                f"(canonical form is {canon!r}); caller must pre-canonicalize."
            )
        self._slug = slug
        self._service = KEYCHAIN_SERVICE_TEMPLATE.format(slug=slug)
        # Lookup `security` CLI (Darwin default is /usr/bin/security).
        cli = security_cli_path or shutil.which("security")
        if cli is None:
            raise KeyStoreUnavailable(
                "MacOSKeychainKeyStore: `security` CLI not found on PATH. "
                "Provision operator dev env or set TILTH_KEYSTORE_PROVIDER=file."
            )
        self._cli = cli

    def provider(self) -> str:
        return _PROVIDER_KEYCHAIN

    def _account(self, key_id: str, purpose: str = "generic") -> str:
        return f"{purpose}.{key_id}"

    def _run_security(self, args: list[str]) -> subprocess.CompletedProcess:
        """Run `security <args>`. argv-array (no shell). Captures stdout+stderr."""
        return subprocess.run(
            [self._cli] + args,
            capture_output=True,
            text=False,
            check=False,
        )

    def _keychain_locked(self, stderr: bytes) -> bool:
        err_str = stderr.decode("utf-8", errors="replace")
        for marker in _KEYCHAIN_LOCKED_MARKERS:
            if marker == "could not be found in the current keychain":
                continue  # that's a not-found, not a lock
            if marker in err_str:
                return True
        return False

    def store(
        self, *, key_id: str, key_bytes: bytes | bytearray, purpose: str
    ) -> None:
        """Store via `security add-generic-password -U`. [§5.4 BT4]

        ACKNOWLEDGED v0.1 LIMITATION (D-19): macOS `security` CLI does not accept
        password via stdin — it requires either TTY prompt or `-w <hex>` argv.
        v0.1 uses the `-w` argv approach per blueprint §5.4 CLI specification.
        This means the key hex is briefly visible to same-user `ps` / readers of
        `/proc/<pid>/cmdline` during the subprocess lifetime (<50 ms typically).
        Under v0.1 trusted-operator boundary (single operator, single machine),
        same-uid secondary-process inspection is OUT-OF-MODEL (blueprint §3.11
        v5 trust-boundary note). Multi-user-safe storage (macOS Security.framework
        via pyobjc / SecurityFoundation ctypes) is v0.2 roadmap per drift D-19.
        """
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        if not isinstance(key_bytes, (bytes, bytearray)):
            raise TypeError(
                f"key_bytes must be bytes|bytearray; got {type(key_bytes).__name__}"
            )
        if not isinstance(purpose, str):
            raise TypeError(f"purpose must be str; got {type(purpose).__name__}")
        account = self._account(key_id, purpose)
        # -U = update if exists; -w accepts the password as hex (we pass hex of bytes).
        hex_value = bytes(key_bytes).hex()
        result = self._run_security(
            [
                "add-generic-password",
                "-s",
                self._service,
                "-a",
                account,
                "-w",
                hex_value,
                "-U",
            ]
        )
        if result.returncode != 0:
            if self._keychain_locked(result.stderr):
                raise KeychainLockedError(
                    f"keychain locked while storing {key_id}: "
                    f"{result.stderr!r}"
                )
            raise KeyStoreUnavailable(
                f"security add-generic-password failed rc={result.returncode}: "
                f"{result.stderr!r}"
            )

    def _retrieve_raw(self, key_id: str) -> bytearray:
        """`security find-generic-password ... -w`. Returns bytearray. [§3.11 v3]"""
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        # Try both generic and canonical purpose namespaces.
        for purpose in ("generic", "session_hmac", "ledger", "watermarks"):
            account = self._account(key_id, purpose)
            result = self._run_security(
                [
                    "find-generic-password",
                    "-s",
                    self._service,
                    "-a",
                    account,
                    "-w",
                ]
            )
            if result.returncode == 0:
                stdout_str = result.stdout.decode("ascii", errors="strict").strip()
                try:
                    raw = bytearray.fromhex(stdout_str)
                except ValueError as e:
                    raise KeyCorrupt(
                        f"keychain returned non-hex value for {key_id}"
                    ) from e
                return raw
            if self._keychain_locked(result.stderr):
                raise KeychainLockedError(
                    f"keychain locked while retrieving {key_id}"
                )
        raise KeyCorrupt(
            f"keychain: key {key_id} not found under service {self._service}"
        )

    def zero(self, key_id: str) -> None:
        """Delete keychain item(s) matching any purpose for this key_id."""
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        # Delete across the known-purpose namespaces. Missing items return non-zero;
        # we treat that as benign (idempotent zero).
        for purpose in ("generic", "session_hmac", "ledger", "watermarks"):
            account = self._account(key_id, purpose)
            self._run_security(
                ["delete-generic-password", "-s", self._service, "-a", account]
            )

    def exists(self, key_id: str) -> bool:
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        for purpose in ("generic", "session_hmac", "ledger", "watermarks"):
            account = self._account(key_id, purpose)
            result = self._run_security(
                [
                    "find-generic-password",
                    "-s",
                    self._service,
                    "-a",
                    account,
                ]
            )
            if result.returncode == 0:
                return True
            if self._keychain_locked(result.stderr):
                raise KeychainLockedError(
                    f"keychain locked while checking {key_id}"
                )
        return False

    def rotate(self, key_id: str) -> str:
        """Mint new key under `{key_id}.v<N>` suffix, zero old."""
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        # Round-C scope: rotate is a simple "new key_id suffixed with .rot.<ts>".
        # Full v1→v2 suffix logic lives in session.py (Round E) which consumes this.
        new_id = f"{key_id}.rot.{int(time.time())}"
        new_key = secrets.token_bytes(64)
        self.store(key_id=new_id, key_bytes=new_key, purpose="generic")
        self.zero(key_id)
        return new_id


# -------- NonceRegistry (§5.4 BT4 v2/v3/v4) --------


@dataclass(frozen=True, kw_only=True)
class _NonceRegistryState:
    """In-memory tracker for a per-slug nonce registry."""

    slug: str
    registry_dir: Path
    lock_path: Path
    hmac_key: bytearray  # bytes held on instance; not SecretBytes (see D-16 rationale)


def _segment_path(state: _NonceRegistryState, seq: int) -> Path:
    # Per §8 NONCE_REGISTRY_ROTATION_PATH_TEMPLATE = `keys/{slug}/.nonce_registry.{seq}.jsonl`
    return state.registry_dir / f".nonce_registry.{seq:04d}.jsonl"


def _segment_trailer_path(state: _NonceRegistryState, seq: int) -> Path:
    return state.registry_dir / f".nonce_registry.{seq:04d}.hmac"


def _current_segment_seq(state: _NonceRegistryState) -> int:
    """Find highest existing segment seq number, or 0 if none yet."""
    existing = sorted(state.registry_dir.glob(".nonce_registry.*.jsonl"))
    if not existing:
        return 0
    # Name pattern .nonce_registry.NNNN.jsonl
    try:
        return max(int(p.name.split(".")[2]) for p in existing)
    except (ValueError, IndexError):
        return 0


def _compute_segment_hmac_hex(state: _NonceRegistryState, seg: int) -> str:
    """HMAC-SHA3-512 over the full segment file bytes."""
    p = _segment_path(state, seg)
    try:
        data = p.read_bytes()
    except FileNotFoundError:
        data = b""
    return hmac_sha3_512(bytes(state.hmac_key), data).hex()


def _read_segment_trailer(state: _NonceRegistryState, seg: int) -> dict | None:
    p = _segment_trailer_path(state, seg)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_bytes())
    except json.JSONDecodeError as e:
        raise NonceRegistryTrailerMismatch(
            f"segment {seg} trailer not JSON: {e}"
        ) from e


def _write_segment_trailer(
    state: _NonceRegistryState,
    seg: int,
    segment_hmac_hex: str,
    prev_segment_trailer_hash: str,
    last_nonce_seq_id: int,
) -> str:
    body = {
        "schema_version": _NONCE_REGISTRY_SCHEMA_VERSION,
        "segment_seq": seg,
        "last_nonce_seq_id": last_nonce_seq_id,
        "segment_hmac": segment_hmac_hex,
        "prev_segment_trailer_hash": prev_segment_trailer_hash,
    }
    body_bytes = _canonical_json_bytes(body)
    trailer_hmac = hmac_sha3_512(bytes(state.hmac_key), body_bytes).hex()
    full = dict(body, trailer_hmac=trailer_hmac)
    _atomic_write_bytes(_segment_trailer_path(state, seg), _canonical_json_bytes(full))
    return trailer_hmac


def _verify_nonce_registry_chain(state: _NonceRegistryState) -> None:
    """Walk every segment, verify HMAC + prev-trailer link. [§5.4 v3]"""
    segments = sorted(state.registry_dir.glob(".nonce_registry.*.jsonl"))
    if not segments:
        return  # empty registry, legal first-boot
    prev_trailer_hash = _NONCE_REGISTRY_GENESIS_PREV
    seq_numbers = []
    for p in segments:
        try:
            seq = int(p.name.split(".")[2])
        except (ValueError, IndexError):
            raise NonceRegistryTruncated(
                f"unparseable segment filename {p.name}"
            )
        seq_numbers.append(seq)
    seq_numbers.sort()
    # Detect missing segments (truncation mid-chain).
    if seq_numbers[0] != 0:
        raise NonceRegistryTruncated(
            f"segment 0 missing; earliest present is {seq_numbers[0]}"
        )
    for i in range(1, len(seq_numbers)):
        if seq_numbers[i] != seq_numbers[i - 1] + 1:
            raise NonceRegistryTruncated(
                f"segment gap between {seq_numbers[i-1]} and {seq_numbers[i]}"
            )
    for seq in seq_numbers:
        trailer = _read_segment_trailer(state, seq)
        if trailer is None:
            raise NonceRegistryTruncated(
                f"segment {seq} has no trailer .hmac file"
            )
        # Re-compute expected trailer HMAC over the body sans trailer_hmac.
        body = {k: v for k, v in trailer.items() if k != "trailer_hmac"}
        expected_trailer_hmac = hmac_sha3_512(
            bytes(state.hmac_key), _canonical_json_bytes(body)
        ).hex()
        if not constant_time_equal(
            expected_trailer_hmac.encode("ascii"),
            trailer["trailer_hmac"].encode("ascii"),
        ):
            raise NonceRegistryTrailerMismatch(
                f"segment {seq}: trailer-over-trailer HMAC mismatch"
            )
        # Re-compute segment body HMAC.
        actual_segment_hmac = _compute_segment_hmac_hex(state, seq)
        if not constant_time_equal(
            actual_segment_hmac.encode("ascii"),
            trailer["segment_hmac"].encode("ascii"),
        ):
            raise NonceRegistryTrailerMismatch(
                f"segment {seq}: segment-body HMAC mismatch"
            )
        if trailer["prev_segment_trailer_hash"] != prev_trailer_hash:
            raise NonceRegistryTrailerMismatch(
                f"segment {seq}: prev_segment_trailer_hash does not match "
                f"segment {seq - 1} trailer"
            )
        prev_trailer_hash = trailer["trailer_hmac"]


def _nonce_already_registered(
    state: _NonceRegistryState, key_id: str, nonce_hex: str
) -> bool:
    """O(segments * entries) scan. Called only on the append path under the lock."""
    for p in sorted(state.registry_dir.glob(".nonce_registry.*.jsonl")):
        if not p.exists():
            continue
        try:
            with p.open("rb") as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if entry.get("key_id") == key_id and entry.get("nonce_hex") == nonce_hex:
                        return True
        except OSError:
            continue
    return False


def _last_nonce_seq_id(state: _NonceRegistryState) -> int:
    """Return the last (max) nonce_seq_id across all segments, or 0 if none."""
    last = 0
    for p in sorted(state.registry_dir.glob(".nonce_registry.*.jsonl")):
        if not p.exists():
            continue
        try:
            with p.open("rb") as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    seq = entry.get("seq_id", 0)
                    if seq > last:
                        last = seq
        except OSError:
            continue
    return last


def _rotate_nonce_registry(state: _NonceRegistryState, current_seq: int) -> int:
    """Seal current segment, open seq+1. [§5.4 v4 RT-v3 MED-1]

    Raises NonceRegistryRotationFailed on IO failure BEFORE a nonce is generated,
    so no half-state is left behind.
    """
    try:
        # Seal current segment's trailer.
        segment_hmac = _compute_segment_hmac_hex(state, current_seq)
        prev_hash = _NONCE_REGISTRY_GENESIS_PREV
        if current_seq > 0:
            prev_trailer = _read_segment_trailer(state, current_seq - 1)
            if prev_trailer is not None:
                prev_hash = prev_trailer["trailer_hmac"]
        # last_nonce_seq_id inside this segment.
        last_nonce_seq = _last_nonce_seq_id(state)
        _write_segment_trailer(
            state, current_seq, segment_hmac, prev_hash, last_nonce_seq
        )
        # Create the NEW segment file (empty).
        new_seg_path = _segment_path(state, current_seq + 1)
        new_seg_path.touch()
        return current_seq + 1
    except OSError as e:
        raise NonceRegistryRotationFailed(
            f"rotation failed pre-nonce-generation: {e}"
        ) from e


def _nonce_registry_append(
    state: _NonceRegistryState, key_id: str, nonce: bytes
) -> None:
    """Append under single held fcntl.LOCK_EX. [§5.4 v3/v4]"""
    nonce_hex = nonce.hex()
    with _acquire_exclusive_lock(state.lock_path):
        current_seq = _current_segment_seq(state)
        current_path = _segment_path(state, current_seq)
        if not current_path.exists():
            current_path.touch()
        # Pre-gen size check (v4 RT-v3 MED-1).
        size = current_path.stat().st_size
        if size >= NONCE_REGISTRY_SIZE_LIMIT_BYTES:
            current_seq = _rotate_nonce_registry(state, current_seq)
            current_path = _segment_path(state, current_seq)
        # Collision check — O(segments).
        if _nonce_already_registered(state, key_id, nonce_hex):
            raise NonceReused(
                f"key_id={key_id} nonce_hex={nonce_hex[:16]}... already registered"
            )
        # Build entry with chain metadata.
        last_seq = _last_nonce_seq_id(state)
        entry = {
            "schema_version": _NONCE_REGISTRY_SCHEMA_VERSION,
            "seq_id": last_seq + 1,
            "key_id": key_id,
            "nonce_hex": nonce_hex,
            "ts_utc": _iso_utc_now(),
        }
        line = _canonical_json_bytes(entry) + b"\n"
        # Append via O_APPEND atomic write.
        fd = os.open(
            current_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600
        )
        try:
            os.write(fd, line)
            os.fsync(fd)
        finally:
            os.close(fd)
        # Recompute segment trailer (seals the CURRENT segment with the new entry).
        prev_hash = _NONCE_REGISTRY_GENESIS_PREV
        if current_seq > 0:
            prev_trailer = _read_segment_trailer(state, current_seq - 1)
            if prev_trailer is not None:
                prev_hash = prev_trailer["trailer_hmac"]
        _write_segment_trailer(
            state,
            current_seq,
            _compute_segment_hmac_hex(state, current_seq),
            prev_hash,
            entry["seq_id"],
        )


# -------- FileKeyStore (§5.4 BT4 v2+v3) --------


class FileKeyStore(KeyStore):
    """PBKDF2-SHA3-512 → AES-256-GCM on-disk envelope. [§5.4 BT4]"""

    def __init__(
        self,
        slug: str,
        *,
        keystore_dir: Path,
        passphrase_env: str = TILTH_FILE_KEYSTORE_PASSPHRASE_ENV,
    ) -> None:
        """Bind to slug; derive KEK from env passphrase; zeroize env + passphrase.

        [§5.4 BT4 v2 passphrase hygiene]

        :raises FileKeyStoreUnavailable: passphrase env var absent (F-KEY-04).
        :raises ValueError: slug is not canonical.
        """
        if not isinstance(slug, str):
            raise TypeError(f"slug must be str; got {type(slug).__name__}")
        if not isinstance(keystore_dir, Path):
            raise TypeError(
                f"keystore_dir must be Path; got {type(keystore_dir).__name__}"
            )
        canon = canonical_slug(slug)
        if canon != slug:
            raise ValueError(
                f"FileKeyStore: slug {slug!r} is not canonical "
                f"(canonical form is {canon!r}); caller must pre-canonicalize."
            )
        self._slug = slug
        self._base = keystore_dir / slug
        self._base.mkdir(parents=True, exist_ok=True)
        # Passphrase → KEK hygiene.
        raw_pw = os.environ.get(passphrase_env)
        if raw_pw is None:
            raise FileKeyStoreUnavailable(
                f"{passphrase_env} env var not set; cannot initialize FileKeyStore. "
                "Operator must either set the env var or use the `tilth keystore-unlock` CLI."
            )
        pw_buf = bytearray(raw_pw.encode("utf-8"))
        # Load or create a per-slug salt stored at keystore_dir/slug/.salt .
        salt_path = self._base / ".salt"
        if salt_path.exists():
            salt = salt_path.read_bytes()
            if len(salt) != _FILE_KEYSTORE_SALT_BYTES:
                raise KeyCorrupt(
                    f"salt file {salt_path} has wrong length {len(salt)}"
                )
        else:
            salt = os.urandom(_FILE_KEYSTORE_SALT_BYTES)
            _atomic_write_bytes(salt_path, salt)
        self._salt = salt
        # Derive KEK as bytearray. Hold on instance (not SecretBytes per D-16).
        kek = pbkdf2_sha3_512(
            pw_buf, salt, iterations=600_000, dklen=_FILE_KEYSTORE_KEK_BYTES
        )
        # Zero the passphrase buffer; delete env var; drop the reference to raw_pw.
        zero_bytes(pw_buf)
        try:
            del os.environ[passphrase_env]
        except KeyError:
            pass
        self._kek: bytearray = kek
        # Nonce registry state (keyed with a derived sub-key for registry HMAC).
        # We reuse the KEK for HMAC-ing registry trailers; v0.1 scope — deriving a
        # distinct key per §4.6 M7 belongs to later rounds when a full keystore
        # key-derivation tree lands.
        registry_dir = self._base / "nonce_registry"
        registry_dir.mkdir(parents=True, exist_ok=True)
        self._registry_state = _NonceRegistryState(
            slug=slug,
            registry_dir=registry_dir,
            lock_path=registry_dir / ".nonce_registry.lock",
            hmac_key=bytearray(self._kek),
        )

    def provider(self) -> str:
        return _PROVIDER_FILE

    def _key_path(self, key_id: str) -> Path:
        return self._base / f"{key_id}{_AEAD_FILE_SUFFIX}"

    def zero_kek(self) -> None:
        """Zeroize in-memory KEK + nonce-registry HMAC key. [D-16, D-22]

        Call at shutdown / end_session. Idempotent — safe to call twice.
        """
        zero_bytes(self._kek)
        zero_bytes(self._registry_state.hmac_key)

    def close(self) -> None:
        """Alias for zero_kek() — pairs with context-manager __exit__."""
        self.zero_kek()

    def __enter__(self) -> "FileKeyStore":
        return self

    def __exit__(self, *_: object) -> None:
        """Deterministic zero-on-exit per Round-C D-22 closure.

        Round-E session.py uses this pattern at end_session; ad-hoc callers
        may also use `with FileKeyStore(...) as ks:` to guarantee KEK erasure
        even on exception. No reliance on __del__ / GC non-determinism.
        """
        self.close()

    def store(
        self, *, key_id: str, key_bytes: bytes | bytearray, purpose: str
    ) -> None:
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        if not isinstance(key_bytes, (bytes, bytearray)):
            raise TypeError(
                f"key_bytes must be bytes|bytearray; got {type(key_bytes).__name__}"
            )
        if not isinstance(purpose, str):
            raise TypeError(f"purpose must be str; got {type(purpose).__name__}")
        nonce = os.urandom(_AESGCM_NONCE_BYTES)
        # Register nonce BEFORE the encrypt write — pre-gen size check lives
        # inside _nonce_registry_append per v4.
        self._nonce_registry_check_and_register(key_id, nonce)
        aad = purpose.encode("utf-8")
        ct = aesgcm_encrypt(self._kek, nonce, bytes(key_bytes), aad)
        # On-disk format: canonical JSON wrapping nonce_hex + ct_hex + purpose.
        body = {
            "schema_version": "v1",
            "key_id": key_id,
            "purpose": purpose,
            "nonce_hex": nonce.hex(),
            "ct_hex": ct.hex(),
        }
        _atomic_write_bytes(self._key_path(key_id), _canonical_json_bytes(body))

    def _nonce_registry_check_and_register(
        self, key_id: str, nonce: bytes
    ) -> None:
        """Pre-gen check + append. Wrap per v4 discipline."""
        _nonce_registry_append(self._registry_state, key_id, nonce)

    def _retrieve_raw(self, key_id: str) -> bytearray:
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        path = self._key_path(key_id)
        if not path.exists():
            raise KeyCorrupt(
                f"FileKeyStore: key {key_id} not present at {path}"
            )
        try:
            body = json.loads(path.read_bytes())
        except json.JSONDecodeError as e:
            raise KeyCorrupt(f"FileKeyStore: malformed envelope for {key_id}: {e}") from e
        required = {"schema_version", "key_id", "purpose", "nonce_hex", "ct_hex"}
        if set(body.keys()) != required:
            raise KeyCorrupt(
                f"FileKeyStore: envelope keys mismatch for {key_id}: {sorted(body.keys())}"
            )
        try:
            nonce = bytes.fromhex(body["nonce_hex"])
            ct = bytes.fromhex(body["ct_hex"])
        except ValueError as e:
            raise KeyCorrupt(f"FileKeyStore: non-hex field for {key_id}") from e
        aad = body["purpose"].encode("utf-8")
        try:
            # Return bytearray (§3.11 v3 HIGH-3 contract).
            return aesgcm_decrypt(self._kek, nonce, ct, aad)
        except InvalidTag as e:
            raise KeyCorrupt(
                f"FileKeyStore: MAC failure for {key_id} (tampered or wrong KEK)"
            ) from e

    def zero(self, key_id: str) -> None:
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        path = self._key_path(key_id)
        if not path.exists():
            return  # idempotent
        # Overwrite with zeros of the same length then unlink.
        try:
            size = path.stat().st_size
            with path.open("r+b") as fh:
                fh.write(b"\x00" * size)
                fh.flush()
                os.fsync(fh.fileno())
            path.unlink()
        except OSError:
            # Best-effort; blueprint §5.4 documents APFS journal-level erasure
            # limitation.
            pass

    def exists(self, key_id: str) -> bool:
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        return self._key_path(key_id).exists()

    def rotate(self, key_id: str) -> str:
        """Mint fresh key under suffixed id, zero old."""
        if not isinstance(key_id, str):
            raise TypeError(f"key_id must be str; got {type(key_id).__name__}")
        new_id = f"{key_id}.rot.{int(time.time())}"
        new_key = secrets.token_bytes(64)
        self.store(key_id=new_id, key_bytes=new_key, purpose="rotation")
        self.zero(key_id)
        return new_id


# -------- YubiHSMKeyStore stub (§5.4 BT4) --------


class YubiHSMKeyStore(KeyStore):
    """v0.1 stub — raises NotImplementedError. [§5.4 BT4 Phase-2 roadmap]"""

    def __init__(self) -> None:
        raise NotImplementedError(
            "YubiHSM support deferred to Phase 2; see §5.4 BT4 roadmap. "
            "Set TILTH_KEYSTORE_PROVIDER=keychain or =file for v0.1."
        )

    def provider(self) -> str:
        return _PROVIDER_YUBIHSM

    def _retrieve_raw(self, key_id: str) -> bytearray:
        raise NotImplementedError("YubiHSM Phase-2")

    def store(
        self, *, key_id: str, key_bytes: bytes | bytearray, purpose: str
    ) -> None:
        raise NotImplementedError("YubiHSM Phase-2")

    def rotate(self, key_id: str) -> str:
        raise NotImplementedError("YubiHSM Phase-2")

    def zero(self, key_id: str) -> None:
        raise NotImplementedError("YubiHSM Phase-2")

    def exists(self, key_id: str) -> bool:
        raise NotImplementedError("YubiHSM Phase-2")


# -------- resolve_keystore factory (§5.4 BT4 + §6.6) --------


def resolve_keystore(
    *,
    slug: str,
    keystore_dir: Path | None = None,
    env_var: str = TILTH_KEYSTORE_PROVIDER_ENV,
) -> KeyStore:
    """Provider dispatch per env var. [§5.4 BT4 + §6.6 F-KEY-01/F-KEY-03/F-KEY-04]

    NEVER silent fallback — if the selected provider cannot init, we raise
    KeyStoreUnavailable so the operator knows. Silent fallbacks are how
    sovereignty promises die (blueprint §5.4 BT4 verbatim).
    """
    if not isinstance(slug, str):
        raise TypeError(f"slug must be str; got {type(slug).__name__}")
    if keystore_dir is not None and not isinstance(keystore_dir, Path):
        raise TypeError(
            f"keystore_dir must be Path|None; got {type(keystore_dir).__name__}"
        )
    # Default on macOS is keychain; elsewhere it's file (if passphrase set) → operator-configurable.
    provider = os.environ.get(env_var)
    if provider is None:
        provider = (
            _PROVIDER_KEYCHAIN if platform.system() == "Darwin" else _PROVIDER_FILE
        )
    provider = provider.lower().strip()
    if provider not in _VALID_PROVIDERS:
        raise KeyStoreConfigError(
            f"unknown provider {provider!r}; must be one of {sorted(_VALID_PROVIDERS)}"
        )
    if provider == _PROVIDER_KEYCHAIN:
        if platform.system() != "Darwin":
            raise KeyStoreUnavailable(
                "keychain provider selected on non-macOS platform. "
                "Set TILTH_KEYSTORE_PROVIDER=file to opt into the FileKeyStore."
            )
        return MacOSKeychainKeyStore(slug)
    if provider == _PROVIDER_FILE:
        if keystore_dir is None:
            raise KeyStoreConfigError(
                "file provider requires keystore_dir kwarg to resolve_keystore()"
            )
        return FileKeyStore(slug, keystore_dir=keystore_dir)
    # provider == yubihsm
    return YubiHSMKeyStore()
