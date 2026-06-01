"""Hash-chain ledger + HMAC trailer + watermark primitives. [§1 row 4, §5.3 BT3, §5.6 BT8, §6.5, §7.3, §8]

Keystore-agnostic: callers pass raw HMAC key bytes (keys.py resolves key_ids in Round C).
Single `fcntl.LOCK_EX` gates every mutation. E-001 HMAC floor (32 bytes) inherited from Round-A `hmac_sha3_512`.
"""

from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import os
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from pipeline.sovereignty.crypto_primitives import (
    constant_time_equal,
    hmac_sha3_512,
    sha3_512_hex,
)

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§1 row 4 (audit.py)",
            "§5.3 BT3 append protocol",
            "§5.6 BT8 HMAC trailer + watermark",
            "§6.5 Ledger failure codes",
            "§7.3 test vectors",
            "§8 LEDGER_ROTATION_SIZE_LIMIT_BYTES",
        ],
        "hash_at_lock": None,
        "hash_source_version": "v6",
    },
}

__all__ = [
    # Dataclasses
    "LedgerTrailer",
    "WatermarksTrailer",
    "LedgerWatermark",
    # Primitives
    "canonical_json_bytes",
    "append_to_ledger",
    "verify_ledger",
    "verify_watermarks",
    "verify_ledger_freshness",
    "update_watermark",
    "rotate_ledger_if_needed",
    # Constants
    "LEDGER_ROTATION_SIZE_LIMIT_BYTES",
    "CHAIN_VERIFY_FAST_TAIL_ENTRIES",
    # Exceptions
    "LedgerHMACTrailerMismatch",
    "LedgerWatermarkRegression",
    "WatermarkHmacMissing",
    "WatermarkHmacMismatch",
    "LedgerUnreadable",
    "LedgerChainBroken",
]

# --- Constants (per blueprint §8) ---
LEDGER_ROTATION_SIZE_LIMIT_BYTES: int = 100 * 1024 * 1024  # 100 MiB
CHAIN_VERIFY_FAST_TAIL_ENTRIES: int = 100

# Zero-hash used as genesis `prev_hash` for the first ledger entry. SHA-3-512
# output is 64 bytes → 128 hex chars. All zeros is the documented genesis
# marker (cannot collide with a real SHA-3-512 output — requires a preimage).
_GENESIS_PREV_HASH: str = "0" * 128

# Schema versions — bumped only via a Section 1 revision (new audit round).
_LEDGER_TRAILER_SCHEMA_VERSION: str = "v2"
_LEDGER_TRAILER_VERSION: int = 2
_WATERMARKS_TRAILER_SCHEMA_VERSION: str = "v1"
_WATERMARKS_VERSION: int = 1
_LEDGER_WATERMARK_SCHEMA_VERSION: str = "v1"

# Trailer file format: two JSON objects on separate lines.
#   Line 1: canonical JSON of the trailer body (all fields except trailer_hmac)
#   Line 2: canonical JSON of {"trailer_hmac": "<hex>"}
# The trailer_hmac is HMAC-SHA3-512(hmac_key, line_1_bytes).
_TRAILER_BODY_KEY_ORDER: tuple[str, ...] = (
    "schema_version",
    "ledger_name",
    "last_seq_id",
    "last_entry_hash",
    "ledger_hmac",
    "trailer_version",
)

_WATERMARKS_TRAILER_BODY_KEY_ORDER: tuple[str, ...] = (
    "schema_version",
    "watermarks_version",
    "watermarks_hmac",
    "wall_at_write_utc",
)

_WATERMARK_BODY_KEY_ORDER: tuple[str, ...] = (
    "schema_version",
    "ledger_name",
    "last_seq_id",
    "last_trailer_hmac_hex",
    "wall_at_write_utc",
)

# HMAC output length — SHA-3-512 is 64 bytes → 128 hex chars.
_HMAC_HEX_LEN: int = 128


# -------- Exceptions (map to blueprint §6.5) --------


class LedgerUnreadable(RuntimeError):
    """Ledger file cannot be read. [F-ADM-03]"""
    def __init__(self, ledger_path: Path, reason: str) -> None:
        super().__init__(f"ledger {ledger_path} unreadable: {reason}")
        self.ledger_path = ledger_path
        self.reason = reason


class LedgerChainBroken(RuntimeError):
    """Hash-chain integrity broken. [F-ADM-04]"""
    def __init__(self, ledger_path: Path, line_number: int, reason: str) -> None:
        super().__init__(f"ledger {ledger_path} chain broken at line {line_number}: {reason}")
        self.ledger_path = ledger_path
        self.line_number = line_number
        self.reason = reason


class LedgerHMACTrailerMismatch(RuntimeError):
    """Trailer HMAC mismatch. [F-ADM-05]"""
    def __init__(self, ledger_path: Path, reason: str = "hmac_mismatch") -> None:
        super().__init__(f"ledger {ledger_path} trailer HMAC mismatch: {reason}")
        self.ledger_path = ledger_path
        self.reason = reason


class LedgerWatermarkRegression(RuntimeError):
    """Seq_id regression or trailer-hmac mismatch at same seq_id. [F-ADM-08]"""
    def __init__(self, ledger_name: str, observed: int, expected_ge: int, reason: str) -> None:
        super().__init__(
            f"ledger {ledger_name} watermark regression: observed={observed} "
            f"expected_ge={expected_ge} ({reason})"
        )
        self.ledger_name = ledger_name
        self.observed = observed
        self.expected_ge = expected_ge
        self.reason = reason


class WatermarkHmacMissing(RuntimeError):
    """Watermarks body / HMAC pair incomplete. [F-ADM-10]"""
    def __init__(self, watermarks_path: Path, reason: str) -> None:
        super().__init__(f"watermarks {watermarks_path} HMAC pair incomplete: {reason}")
        self.watermarks_path = watermarks_path
        self.reason = reason


class WatermarkHmacMismatch(RuntimeError):
    """Watermarks HMAC does not verify. [F-ADM-10] Operator runs admin_risk re-issuance ceremony."""
    def __init__(self, watermarks_path: Path, reason: str = "hmac_mismatch") -> None:
        super().__init__(f"watermarks {watermarks_path} HMAC mismatch: {reason}")
        self.watermarks_path = watermarks_path
        self.reason = reason


# -------- Dataclasses --------


@dataclass(frozen=True, kw_only=True)
class LedgerTrailer:
    """Per-ledger HMAC trailer. [§5.6 BT8]

    ledger_hmac is HMAC-SHA3-512 over the full ledger file bytes.
    trailer_hmac is HMAC-SHA3-512 over canonical JSON of the trailer body
    (all fields except trailer_hmac itself).
    """
    schema_version: str
    ledger_name: str
    last_seq_id: int
    last_entry_hash: str
    ledger_hmac: str
    trailer_version: int
    trailer_hmac: str


@dataclass(frozen=True, kw_only=True)
class WatermarksTrailer:
    """Watermarks-file HMAC trailer. [§5.6 BT8 v4]"""
    schema_version: str
    watermarks_version: int
    watermarks_hmac: str
    wall_at_write_utc: str
    trailer_hmac: str


@dataclass(frozen=True, kw_only=True)
class LedgerWatermark:
    """Per-ledger watermark entry keyed by ledger_name. [§5.6 BT8]"""
    schema_version: str
    ledger_name: str
    last_seq_id: int
    last_trailer_hmac_hex: str
    wall_at_write_utc: str


# -------- Canonical JSON (shared helper) --------


def canonical_json_bytes(obj: object) -> bytes:
    """Deterministic JSON bytes for HMAC / hashing. [§5.6 canon]

    sort_keys=True, separators=(",", ":"), ensure_ascii=False, utf-8.
    Raises TypeError on non-serializable input.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


# -------- Lock discipline --------


@contextmanager
def _acquire_exclusive_lock(lock_path: Path) -> Iterator[int]:
    """fcntl.LOCK_EX on lock_path with O_NOFOLLOW per §8 LOCK_FILE_OPEN_FLAGS.

    Post-open inode + uid checks live in Round E/F safe_open_lock_file.
    """
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
    """Write `payload` to `target` atomically: tmp → fsync → rename → fsync parent."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    with open(tmp, "wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    os.rename(tmp, target)
    # fsync parent so rename is durable.
    parent_fd = os.open(target.parent, os.O_RDONLY)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


# -------- Iso timestamp helper --------


def _iso_utc_now() -> str:
    """Return current UTC time as ISO-8601 with trailing 'Z'."""
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


# -------- Trailer serialization --------


def _trailer_body_dict(trailer: LedgerTrailer) -> dict:
    return {
        "schema_version": trailer.schema_version,
        "ledger_name": trailer.ledger_name,
        "last_seq_id": trailer.last_seq_id,
        "last_entry_hash": trailer.last_entry_hash,
        "ledger_hmac": trailer.ledger_hmac,
        "trailer_version": trailer.trailer_version,
    }


def _watermarks_trailer_body_dict(trailer: WatermarksTrailer) -> dict:
    return {
        "schema_version": trailer.schema_version,
        "watermarks_version": trailer.watermarks_version,
        "watermarks_hmac": trailer.watermarks_hmac,
        "wall_at_write_utc": trailer.wall_at_write_utc,
    }


def _serialize_ledger_trailer(trailer: LedgerTrailer) -> bytes:
    """Two canonical-JSON lines: body, then {"trailer_hmac": "..."}."""
    body = canonical_json_bytes(_trailer_body_dict(trailer))
    hmac_line = canonical_json_bytes({"trailer_hmac": trailer.trailer_hmac})
    return body + b"\n" + hmac_line + b"\n"


def _serialize_watermarks_trailer(trailer: WatermarksTrailer) -> bytes:
    body = canonical_json_bytes(_watermarks_trailer_body_dict(trailer))
    hmac_line = canonical_json_bytes({"trailer_hmac": trailer.trailer_hmac})
    return body + b"\n" + hmac_line + b"\n"


def _load_ledger_trailer(trailer_path: Path) -> LedgerTrailer:
    try:
        raw = trailer_path.read_bytes()
    except FileNotFoundError as e:
        raise LedgerUnreadable(trailer_path, "trailer_missing") from e
    except OSError as e:
        raise LedgerUnreadable(trailer_path, f"os_error:{e}") from e
    lines = raw.splitlines()
    if len(lines) < 2:
        raise LedgerUnreadable(trailer_path, "trailer_truncated")
    try:
        body = json.loads(lines[0])
        hmac_obj = json.loads(lines[1])
    except json.JSONDecodeError as e:
        raise LedgerUnreadable(trailer_path, f"trailer_not_json:{e}") from e
    required = set(_TRAILER_BODY_KEY_ORDER)
    if set(body.keys()) != required:
        raise LedgerUnreadable(
            trailer_path, f"trailer_body_keys_mismatch:{sorted(body.keys())}"
        )
    if set(hmac_obj.keys()) != {"trailer_hmac"}:
        raise LedgerUnreadable(
            trailer_path, f"trailer_hmac_line_keys_mismatch:{sorted(hmac_obj.keys())}"
        )
    return LedgerTrailer(
        schema_version=body["schema_version"],
        ledger_name=body["ledger_name"],
        last_seq_id=body["last_seq_id"],
        last_entry_hash=body["last_entry_hash"],
        ledger_hmac=body["ledger_hmac"],
        trailer_version=body["trailer_version"],
        trailer_hmac=hmac_obj["trailer_hmac"],
    )


def _load_watermarks_trailer(hmac_path: Path) -> WatermarksTrailer:
    try:
        raw = hmac_path.read_bytes()
    except FileNotFoundError as e:
        raise WatermarkHmacMissing(hmac_path, "hmac_missing") from e
    except OSError as e:
        raise WatermarkHmacMissing(hmac_path, f"os_error:{e}") from e
    lines = raw.splitlines()
    if len(lines) < 2:
        raise WatermarkHmacMissing(hmac_path, "trailer_truncated")
    try:
        body = json.loads(lines[0])
        hmac_obj = json.loads(lines[1])
    except json.JSONDecodeError as e:
        raise WatermarkHmacMissing(hmac_path, f"trailer_not_json:{e}") from e
    required = set(_WATERMARKS_TRAILER_BODY_KEY_ORDER)
    if set(body.keys()) != required:
        raise WatermarkHmacMissing(
            hmac_path, f"trailer_body_keys_mismatch:{sorted(body.keys())}"
        )
    if set(hmac_obj.keys()) != {"trailer_hmac"}:
        raise WatermarkHmacMissing(
            hmac_path,
            f"trailer_hmac_line_keys_mismatch:{sorted(hmac_obj.keys())}",
        )
    return WatermarksTrailer(
        schema_version=body["schema_version"],
        watermarks_version=body["watermarks_version"],
        watermarks_hmac=body["watermarks_hmac"],
        wall_at_write_utc=body["wall_at_write_utc"],
        trailer_hmac=hmac_obj["trailer_hmac"],
    )


# -------- Helpers: hex-shape validation --------


def _assert_hex128(value: str, label: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be str; got {type(value).__name__}")
    if len(value) != _HMAC_HEX_LEN:
        raise ValueError(
            f"{label} must be {_HMAC_HEX_LEN} hex chars; got {len(value)}"
        )
    try:
        bytes.fromhex(value)
    except ValueError as e:
        raise ValueError(f"{label} is not valid hex") from e


# -------- Ledger HMAC computation --------


def _compute_ledger_hmac(ledger_path: Path, hmac_key: bytes) -> str:
    """HMAC-SHA3-512 over the full ledger file bytes, returned as hex."""
    try:
        data = ledger_path.read_bytes()
    except FileNotFoundError:
        data = b""  # empty ledger — HMAC of b"" is legal
    except OSError as e:
        raise LedgerUnreadable(ledger_path, f"os_error:{e}") from e
    return hmac_sha3_512(hmac_key, data).hex()


def _compute_trailer_hmac_over_body(trailer_body_dict: dict, hmac_key: bytes) -> str:
    """HMAC over the canonical JSON bytes of the trailer body."""
    body_bytes = canonical_json_bytes(trailer_body_dict)
    return hmac_sha3_512(hmac_key, body_bytes).hex()


# -------- Watermarks body --------


def _load_watermarks_body(watermarks_path: Path) -> dict[str, LedgerWatermark]:
    try:
        raw = watermarks_path.read_bytes()
    except FileNotFoundError:
        return {}
    except OSError as e:
        raise LedgerUnreadable(watermarks_path, f"os_error:{e}") from e
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        raise LedgerUnreadable(
            watermarks_path, f"watermarks_not_json:{e}"
        ) from e
    if not isinstance(parsed, dict):
        raise LedgerUnreadable(
            watermarks_path,
            f"watermarks_root_not_dict:{type(parsed).__name__}",
        )
    result: dict[str, LedgerWatermark] = {}
    for name, entry in parsed.items():
        if not isinstance(entry, dict):
            raise LedgerUnreadable(
                watermarks_path, f"watermark_entry_not_dict:{name}"
            )
        if set(entry.keys()) != set(_WATERMARK_BODY_KEY_ORDER):
            raise LedgerUnreadable(
                watermarks_path,
                f"watermark_keys_mismatch:{name}:{sorted(entry.keys())}",
            )
        result[name] = LedgerWatermark(
            schema_version=entry["schema_version"],
            ledger_name=entry["ledger_name"],
            last_seq_id=entry["last_seq_id"],
            last_trailer_hmac_hex=entry["last_trailer_hmac_hex"],
            wall_at_write_utc=entry["wall_at_write_utc"],
        )
    return result


def _watermarks_body_bytes(watermarks: dict[str, LedgerWatermark]) -> bytes:
    """Canonical JSON bytes for the watermarks body.

    Each value is a plain dict (asdict) so JSON can serialize it directly.
    """
    serializable: dict[str, dict] = {}
    for name, wm in watermarks.items():
        serializable[name] = asdict(wm)
    return canonical_json_bytes(serializable)


# -------- Verify: watermarks --------


def verify_watermarks(
    watermarks_path: Path,
    hmac_path: Path,
    *,
    watermarks_hmac_key: bytes,
) -> dict[str, LedgerWatermark]:
    """Verify watermarks body + HMAC pair. [§5.6 BT8 v4]

    Both absent → {} (first-boot). One-missing → WatermarkHmacMissing.
    Both present → verify trailer HMAC + body HMAC → dict or WatermarkHmacMismatch.
    """
    if not isinstance(watermarks_path, Path):
        raise TypeError("watermarks_path must be Path")
    if not isinstance(hmac_path, Path):
        raise TypeError("hmac_path must be Path")
    if not isinstance(watermarks_hmac_key, bytes):
        raise TypeError("watermarks_hmac_key must be bytes")

    body_exists = watermarks_path.exists()
    hmac_exists = hmac_path.exists()
    if not body_exists and not hmac_exists:
        return {}
    if body_exists and not hmac_exists:
        raise WatermarkHmacMissing(watermarks_path, "body_without_hmac")
    if hmac_exists and not body_exists:
        raise WatermarkHmacMissing(watermarks_path, "hmac_without_body")

    # Both exist — verify trailer + body HMAC.
    trailer = _load_watermarks_trailer(hmac_path)
    # Step 1: verify trailer_hmac signs trailer body.
    expected_trailer_hmac = _compute_trailer_hmac_over_body(
        _watermarks_trailer_body_dict(trailer), watermarks_hmac_key
    )
    if not constant_time_equal(
        expected_trailer_hmac.encode("ascii"),
        trailer.trailer_hmac.encode("ascii"),
    ):
        raise WatermarkHmacMismatch(watermarks_path, "trailer_hmac_mismatch")
    # Step 2: load watermarks body, re-canonicalize, verify HMAC.
    try:
        raw_body = watermarks_path.read_bytes()
    except OSError as e:
        raise LedgerUnreadable(watermarks_path, f"os_error:{e}") from e
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as e:
        raise LedgerUnreadable(
            watermarks_path, f"body_not_json:{e}"
        ) from e
    body_canonical = canonical_json_bytes(parsed)
    expected_body_hmac = hmac_sha3_512(
        watermarks_hmac_key, body_canonical
    ).hex()
    if not constant_time_equal(
        expected_body_hmac.encode("ascii"),
        trailer.watermarks_hmac.encode("ascii"),
    ):
        raise WatermarkHmacMismatch(watermarks_path, "body_hmac_mismatch")
    return _load_watermarks_body(watermarks_path)


# -------- Verify: ledger --------


def _iter_ledger_entries(
    ledger_path: Path,
) -> Iterator[tuple[int, dict, bytes]]:
    """Yield (line_number, parsed_entry, raw_line_bytes) per ledger line.

    :raises LedgerUnreadable: on structural failure.
    """
    try:
        with ledger_path.open("rb") as fh:
            for idx, raw_line in enumerate(fh, start=1):
                stripped = raw_line.rstrip(b"\n")
                if not stripped:
                    raise LedgerChainBroken(
                        ledger_path, idx, "empty_line"
                    )
                try:
                    obj = json.loads(stripped)
                except json.JSONDecodeError as e:
                    raise LedgerChainBroken(
                        ledger_path, idx, f"line_not_json:{e}"
                    ) from e
                if not isinstance(obj, dict):
                    raise LedgerChainBroken(
                        ledger_path, idx, "line_not_dict"
                    )
                yield idx, obj, stripped
    except FileNotFoundError as e:
        raise LedgerUnreadable(ledger_path, "ledger_missing") from e
    except PermissionError as e:
        raise LedgerUnreadable(ledger_path, "ledger_permission_denied") from e
    except OSError as e:
        raise LedgerUnreadable(ledger_path, f"os_error:{e}") from e


def _verify_chain(ledger_path: Path) -> tuple[int, str]:
    """Walk ledger, check prev_hash / entry_hash continuity. [§5.6]

    Returns (last_seq_id, last_entry_hash) — (0, genesis) on empty.
    Raises LedgerChainBroken / LedgerUnreadable.
    """
    prev_hash = _GENESIS_PREV_HASH
    last_seq = 0
    last_entry_hash = _GENESIS_PREV_HASH
    saw_any = False
    for line_num, entry, raw in _iter_ledger_entries(ledger_path):
        saw_any = True
        # Required fields.
        for key in ("seq_id", "prev_hash", "entry_hash"):
            if key not in entry:
                raise LedgerChainBroken(
                    ledger_path, line_num, f"missing_field:{key}"
                )
        if entry["prev_hash"] != prev_hash:
            raise LedgerChainBroken(
                ledger_path, line_num, "prev_hash_mismatch"
            )
        if entry["seq_id"] != last_seq + 1:
            raise LedgerChainBroken(
                ledger_path, line_num, f"seq_id_non_monotonic:{entry['seq_id']}"
            )
        # Recompute entry_hash: sha3_512_hex(canonical_bytes_of_entry_sans_hash || prev_hash)
        entry_sans_hash = {k: v for k, v in entry.items() if k != "entry_hash"}
        canon = canonical_json_bytes(entry_sans_hash)
        expected_hash = sha3_512_hex(
            canon + prev_hash.encode("ascii")
        ).digest_hex
        if entry["entry_hash"] != expected_hash:
            raise LedgerChainBroken(
                ledger_path, line_num, "entry_hash_mismatch"
            )
        prev_hash = expected_hash
        last_entry_hash = expected_hash
        last_seq = entry["seq_id"]
    if not saw_any:
        return 0, _GENESIS_PREV_HASH
    return last_seq, last_entry_hash


def verify_ledger(
    ledger_path: Path,
    trailer_path: Path,
    *,
    hmac_key: bytes,
) -> LedgerTrailer:
    """Trailer HMAC + ledger-body HMAC + chain continuity. [§5.6]

    v0.1 uses one HMAC key per ledger for both the ledger-body HMAC and the
    trailer-over-trailer HMAC. Raises LedgerUnreadable / LedgerHMACTrailerMismatch /
    LedgerChainBroken.
    """
    if not isinstance(ledger_path, Path):
        raise TypeError("ledger_path must be Path")
    if not isinstance(trailer_path, Path):
        raise TypeError("trailer_path must be Path")
    if not isinstance(hmac_key, bytes):
        raise TypeError("hmac_key must be bytes")
    trailer = _load_ledger_trailer(trailer_path)
    _assert_hex128(trailer.ledger_hmac, "ledger_hmac")
    _assert_hex128(trailer.trailer_hmac, "trailer_hmac")
    _assert_hex128(trailer.last_entry_hash, "last_entry_hash")
    # Step 1: trailer-over-trailer HMAC.
    expected_trailer_hmac = _compute_trailer_hmac_over_body(
        _trailer_body_dict(trailer), hmac_key
    )
    if not constant_time_equal(
        expected_trailer_hmac.encode("ascii"),
        trailer.trailer_hmac.encode("ascii"),
    ):
        raise LedgerHMACTrailerMismatch(ledger_path, "trailer_over_trailer")
    # Step 2: ledger-file HMAC.
    actual_ledger_hmac = _compute_ledger_hmac(ledger_path, hmac_key)
    if not constant_time_equal(
        actual_ledger_hmac.encode("ascii"),
        trailer.ledger_hmac.encode("ascii"),
    ):
        raise LedgerHMACTrailerMismatch(ledger_path, "ledger_body_hmac")
    # Step 3: chain continuity.
    last_seq, last_hash = _verify_chain(ledger_path)
    if last_seq != trailer.last_seq_id:
        raise LedgerChainBroken(
            ledger_path, last_seq, f"trailer_seq_mismatch:{trailer.last_seq_id}"
        )
    if last_hash != trailer.last_entry_hash:
        raise LedgerChainBroken(
            ledger_path, last_seq, "trailer_last_hash_mismatch"
        )
    return trailer


def verify_ledger_freshness(
    ledger_path: Path,
    trailer_path: Path,
    watermarks: dict[str, LedgerWatermark],
    *,
    hmac_key: bytes,
) -> LedgerTrailer:
    """verify_ledger + watermark-regression cross-check. [§5.6 v4]

    Rollback surfaces as LedgerWatermarkRegression.
    """
    trailer = verify_ledger(ledger_path, trailer_path, hmac_key=hmac_key)
    wm = watermarks.get(trailer.ledger_name)
    if wm is None:
        return trailer  # first-boot: no prior watermark
    if trailer.last_seq_id < wm.last_seq_id:
        raise LedgerWatermarkRegression(
            ledger_name=trailer.ledger_name,
            observed=trailer.last_seq_id,
            expected_ge=wm.last_seq_id,
            reason="seq_id_regression",
        )
    if trailer.last_seq_id == wm.last_seq_id:
        if not constant_time_equal(
            trailer.ledger_hmac.encode("ascii"),
            wm.last_trailer_hmac_hex.encode("ascii"),
        ):
            raise LedgerWatermarkRegression(
                ledger_name=trailer.ledger_name,
                observed=trailer.last_seq_id,
                expected_ge=wm.last_seq_id,
                reason="trailer_hmac_mismatch_at_same_seq",
            )
    return trailer


# -------- Rotation --------


def rotate_ledger_if_needed(
    ledger_path: Path,
    *,
    trailer_path: Path,
) -> Path | None:
    """Rotate ledger at ≥ LEDGER_ROTATION_SIZE_LIMIT_BYTES. [§5.6, §8]

    Renames to `<stem>.segment_<NNN>.jsonl` + creates fresh empty ledger.
    Caller MUST hold the lock. Returns rotated segment path or None.
    """
    if not isinstance(ledger_path, Path):
        raise TypeError("ledger_path must be Path")
    if not isinstance(trailer_path, Path):
        raise TypeError("trailer_path must be Path")
    if not ledger_path.exists():
        return None
    try:
        size = ledger_path.stat().st_size
    except OSError as e:
        raise LedgerUnreadable(ledger_path, f"stat_error:{e}") from e
    if size < LEDGER_ROTATION_SIZE_LIMIT_BYTES:
        return None
    # Find next available segment number.
    parent = ledger_path.parent
    stem = ledger_path.stem
    suffix = ledger_path.suffix
    seg_num = 0
    while True:
        candidate = parent / f"{stem}.segment_{seg_num:03d}{suffix}"
        if not candidate.exists():
            break
        seg_num += 1
    os.rename(ledger_path, candidate)
    # Create empty ledger at original path.
    ledger_path.touch()
    # fsync parent for durability.
    parent_fd = os.open(parent, os.O_RDONLY)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)
    return candidate


# -------- Update watermark --------


def _build_watermark_entry(
    ledger_name: str,
    trailer: LedgerTrailer,
) -> LedgerWatermark:
    return LedgerWatermark(
        schema_version=_LEDGER_WATERMARK_SCHEMA_VERSION,
        ledger_name=ledger_name,
        last_seq_id=trailer.last_seq_id,
        last_trailer_hmac_hex=trailer.ledger_hmac,
        wall_at_write_utc=_iso_utc_now(),
    )


def update_watermark(
    ledger_name: str,
    trailer: LedgerTrailer,
    watermarks_path: Path,
    hmac_path: Path,
    *,
    watermarks_hmac_key: bytes,
    lock_path: Path,
) -> WatermarksTrailer:
    """Atomic body-then-HMAC update under single fcntl lock. [§5.6 v4]

    Body → fsync → rename → HMAC recompute over canonical body bytes → HMAC
    atomic write. A reader under the same lock convention never observes
    body-paired-with-stale-hmac.
    """
    if not isinstance(ledger_name, str):
        raise TypeError("ledger_name must be str")
    if not isinstance(trailer, LedgerTrailer):
        raise TypeError("trailer must be LedgerTrailer")
    for p, name in (
        (watermarks_path, "watermarks_path"),
        (hmac_path, "hmac_path"),
        (lock_path, "lock_path"),
    ):
        if not isinstance(p, Path):
            raise TypeError(f"{name} must be Path")
    if not isinstance(watermarks_hmac_key, bytes):
        raise TypeError("watermarks_hmac_key must be bytes")
    with _acquire_exclusive_lock(lock_path):
        # Load current body (may be empty) and update the entry for this ledger.
        body = _load_watermarks_body(watermarks_path)
        body[ledger_name] = _build_watermark_entry(ledger_name, trailer)
        body_bytes = _watermarks_body_bytes(body)
        _atomic_write_bytes(watermarks_path, body_bytes)
        # Recompute HMAC over canonical body.
        body_hmac_hex = hmac_sha3_512(
            watermarks_hmac_key, body_bytes
        ).hex()
        new_trailer_body = {
            "schema_version": _WATERMARKS_TRAILER_SCHEMA_VERSION,
            "watermarks_version": _WATERMARKS_VERSION,
            "watermarks_hmac": body_hmac_hex,
            "wall_at_write_utc": _iso_utc_now(),
        }
        trailer_hmac_hex = _compute_trailer_hmac_over_body(
            new_trailer_body, watermarks_hmac_key
        )
        new_trailer = WatermarksTrailer(
            schema_version=_WATERMARKS_TRAILER_SCHEMA_VERSION,
            watermarks_version=_WATERMARKS_VERSION,
            watermarks_hmac=body_hmac_hex,
            wall_at_write_utc=new_trailer_body["wall_at_write_utc"],
            trailer_hmac=trailer_hmac_hex,
        )
        _atomic_write_bytes(hmac_path, _serialize_watermarks_trailer(new_trailer))
        return new_trailer


# -------- Append --------


def _read_ledger_tail(ledger_path: Path) -> tuple[int, str]:
    """Return (last_seq_id, last_entry_hash). 0 / genesis if empty/missing."""
    if not ledger_path.exists():
        return 0, _GENESIS_PREV_HASH
    try:
        size = ledger_path.stat().st_size
    except OSError as e:
        raise LedgerUnreadable(ledger_path, f"stat_error:{e}") from e
    if size == 0:
        return 0, _GENESIS_PREV_HASH
    # Chain-verify the whole file to get the last entry cheaply (and detect
    # tamper at append time). For large ledgers this is O(N); §5.3 describes
    # a day-counter optimization, and BT8 describes a fast-tail mode — both
    # live at the caller layer or in a later hardening pass.
    last_seq, last_hash = _verify_chain(ledger_path)
    return last_seq, last_hash


def append_to_ledger(
    ledger_path: Path,
    entry_fields: dict,
    *,
    ledger_name: str,
    hmac_key: bytes,
    lock_path: Path,
    trailer_path: Path,
    watermarks_path: Path,
    watermarks_hmac_key: bytes,
    watermarks_hmac_path: Path,
    watermarks_lock_path: Path,
) -> LedgerTrailer:
    """Atomic append + trailer + watermark under single fcntl.LOCK_EX. [§5.3, §5.6]

    audit.py adds chain metadata (seq_id, prev_hash, entry_hash, timestamps) to
    `entry_fields`. Reserved keys in entry_fields → ValueError. Pre-append
    chain-verify → LedgerUnreadable / LedgerChainBroken on broken tail.
    """
    # Type gate (E-001).
    if not isinstance(ledger_path, Path):
        raise TypeError("ledger_path must be Path")
    if not isinstance(entry_fields, dict):
        raise TypeError("entry_fields must be dict")
    if not isinstance(ledger_name, str):
        raise TypeError("ledger_name must be str")
    if not isinstance(hmac_key, bytes):
        raise TypeError("hmac_key must be bytes")
    for p, name in (
        (lock_path, "lock_path"),
        (trailer_path, "trailer_path"),
        (watermarks_path, "watermarks_path"),
        (watermarks_hmac_path, "watermarks_hmac_path"),
        (watermarks_lock_path, "watermarks_lock_path"),
    ):
        if not isinstance(p, Path):
            raise TypeError(f"{name} must be Path")
    if not isinstance(watermarks_hmac_key, bytes):
        raise TypeError("watermarks_hmac_key must be bytes")

    reserved = {"seq_id", "prev_hash", "entry_hash", "timestamp_utc", "issued_monotonic_ns"}
    clash = reserved & entry_fields.keys()
    if clash:
        raise ValueError(
            f"entry_fields contains reserved chain keys: {sorted(clash)}"
        )

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with _acquire_exclusive_lock(lock_path):
        # Step 1: read + verify tail.
        last_seq, prev_hash = _read_ledger_tail(ledger_path)
        # Step 2: rotation.
        rotate_ledger_if_needed(ledger_path, trailer_path=trailer_path)
        # Rotation creates a fresh empty ledger; last_seq carries forward.
        # Step 3: build new entry.
        new_seq = last_seq + 1
        entry = dict(entry_fields)
        entry["seq_id"] = new_seq
        entry["prev_hash"] = prev_hash
        entry["timestamp_utc"] = _iso_utc_now()
        entry["issued_monotonic_ns"] = time.monotonic_ns()
        canon_sans_hash = canonical_json_bytes(entry)
        entry_hash = sha3_512_hex(
            canon_sans_hash + prev_hash.encode("ascii")
        ).digest_hex
        entry["entry_hash"] = entry_hash
        line_bytes = canonical_json_bytes(entry) + b"\n"
        # Step 4: append line via O_APPEND atomic write.
        fd = os.open(
            ledger_path,
            os.O_WRONLY | os.O_CREAT | os.O_APPEND,
            0o600,
        )
        try:
            os.write(fd, line_bytes)
            os.fsync(fd)
        finally:
            os.close(fd)
        # Step 5: recompute ledger HMAC + write trailer atomically.
        new_ledger_hmac = _compute_ledger_hmac(ledger_path, hmac_key)
        new_trailer_body = {
            "schema_version": _LEDGER_TRAILER_SCHEMA_VERSION,
            "ledger_name": ledger_name,
            "last_seq_id": new_seq,
            "last_entry_hash": entry_hash,
            "ledger_hmac": new_ledger_hmac,
            "trailer_version": _LEDGER_TRAILER_VERSION,
        }
        trailer_hmac_hex = _compute_trailer_hmac_over_body(
            new_trailer_body, hmac_key
        )
        new_trailer = LedgerTrailer(
            schema_version=_LEDGER_TRAILER_SCHEMA_VERSION,
            ledger_name=ledger_name,
            last_seq_id=new_seq,
            last_entry_hash=entry_hash,
            ledger_hmac=new_ledger_hmac,
            trailer_version=_LEDGER_TRAILER_VERSION,
            trailer_hmac=trailer_hmac_hex,
        )
        _atomic_write_bytes(trailer_path, _serialize_ledger_trailer(new_trailer))
        # Step 6: update watermark (separate lock, safe to nest).
        update_watermark(
            ledger_name,
            new_trailer,
            watermarks_path,
            watermarks_hmac_path,
            watermarks_hmac_key=watermarks_hmac_key,
            lock_path=watermarks_lock_path,
        )
        return new_trailer
