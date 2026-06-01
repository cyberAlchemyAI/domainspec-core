"""boot_clock_history.jsonl — tamper-evident wall-clock progression log. [§4.8 v4, §9 step 2.5]

Section 1 Round I. One append per :func:`boot.boot_envelope` call.

On-disk artifacts (under ``sovereignty/clock/``):

* ``boot_clock_history.jsonl`` — one JSON line per boot with a chained
  ``prev_hash`` / ``entry_hash``; each line carries
  ``{boot_epoch_ns, wall_at_boot_utc, recorded_at_utc, prev_hash, entry_hash}``.
* ``boot_clock_history.hmac`` — rolling HMAC-SHA3-512 trailer over the
  full file, keyed by ``tilth.clock.boot_history.hmac.v1`` (§8).
* ``boot_clock_history.lock`` — fcntl exclusive lock opened via
  :func:`safe_open_lock_file`; held across append + HMAC recompute +
  trailer rewrite (RT-v3 MED-2 closure).

Blueprint refs:

* §4.8 v4   append_boot_clock_record + atomicity invariant
* §9 step 2.5  boot-sequence integration
* §6.5 F-ADM-09  failure-code family
* §7.14    atomic-append tests

platform_boot:

* :func:`read_boot_epoch_ns` — macOS ``sysctl kern.boottime`` (via
  ``/usr/sbin/sysctl -n kern.boottime``) / Linux ``/proc/stat btime``.
  Returned value is nanoseconds since the Unix epoch at which the
  current OS boot began.
"""

from __future__ import annotations

import datetime as _dt
import fcntl
import hmac
import json
import os
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from pipeline.sovereignty.admin_risk import BootClockRecord
from pipeline.sovereignty.audit import canonical_json_bytes
from pipeline.sovereignty.crypto_primitives import constant_time_equal, sha3_512_hex
from pipeline.sovereignty.keys import KeyStore
from pipeline.sovereignty.lockfile import safe_open_lock_file

__all__ = [
    "BOOT_HISTORY_HMAC_KEY_ID",
    "CLOCK_ROLLBACK_TOLERANCE_SECONDS",
    "BootClockHistoryError",
    "BootClockHistoryRollback",
    "BootClockHistoryTrailerMissing",
    "BootClockHistoryTrailerMismatch",
    "BootClockHistoryCorrupt",
    "BootEpochUnavailable",
    "BootClockHistoryEntry",
    "BootClockTrailer",
    "append_boot_clock_record",
    "read_boot_clock_history",
    "read_boot_epoch_ns",
    "verify_boot_clock_history_chain",
]

BOOT_HISTORY_HMAC_KEY_ID: str = "tilth.clock.boot_history.hmac.v1"
CLOCK_ROLLBACK_TOLERANCE_SECONDS: int = 300
_GENESIS_PREV_HASH: str = "0" * 128


# ---------------------------------------------------------------------------
# Exceptions (F-ADM-09 family)
# ---------------------------------------------------------------------------


class BootClockHistoryError(RuntimeError):
    """Common parent for boot_clock_history failures. E-014 taxonomy."""

    code: str = "F-ADM-09"


class BootClockHistoryRollback(BootClockHistoryError):
    """F-ADM-09 — wall clock regressed past tolerance vs prior entry."""

    code = "F-ADM-09"


class BootClockHistoryTrailerMissing(BootClockHistoryError):
    """F-ADM-09 — non-empty jsonl with absent ``.hmac`` trailer."""

    code = "F-ADM-09"


class BootClockHistoryTrailerMismatch(BootClockHistoryError):
    """F-ADM-09 — trailer HMAC does not match the full-file hash."""

    code = "F-ADM-09"


class BootClockHistoryCorrupt(BootClockHistoryError):
    """F-ADM-09 — chain (prev_hash / entry_hash) broken."""

    code = "F-ADM-09"


class BootEpochUnavailable(RuntimeError):
    """Kernel boot epoch could not be read (platform / permission)."""


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class BootClockHistoryEntry:
    """One line of ``boot_clock_history.jsonl``. Extends the minimal
    :class:`BootClockRecord` shape (§2.5) with chain-metadata fields."""

    boot_epoch_ns: int
    wall_at_boot_utc: str
    recorded_at_utc: str
    prev_hash: str
    entry_hash: str


@dataclass(frozen=True, kw_only=True)
class BootClockTrailer:
    """Rolling HMAC trailer over the full ``boot_clock_history.jsonl``."""

    boot_clock_history_hmac: str
    last_boot_epoch_ns: int
    last_seq_id: int
    wall_at_write_utc: str


# ---------------------------------------------------------------------------
# Time helper
# ---------------------------------------------------------------------------


def _iso_utc_now() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _parse_iso(ts: str) -> _dt.datetime:
    v = ts.replace("Z", "+00:00") if ts.endswith("Z") else ts
    return _dt.datetime.fromisoformat(v)


# ---------------------------------------------------------------------------
# Platform boot epoch readers
# ---------------------------------------------------------------------------


def read_boot_epoch_ns() -> int:
    """Return the current OS boot epoch in nanoseconds since the Unix epoch.

    macOS: parses ``sysctl -n kern.boottime`` (``{ sec = N, usec = M }``).
    Linux: reads ``/proc/stat`` and returns ``btime * 1_000_000_000``.

    :raises BootEpochUnavailable: if the underlying call fails or returns
        a value the parser doesn't recognize.
    """
    system = platform.system()
    if system == "Darwin":
        return _read_boot_epoch_ns_darwin()
    if system == "Linux":
        return _read_boot_epoch_ns_linux()
    raise BootEpochUnavailable(f"unsupported platform: {system}")


def _read_boot_epoch_ns_darwin() -> int:
    try:
        result = subprocess.run(
            ["/usr/sbin/sysctl", "-n", "kern.boottime"],
            capture_output=True,
            check=False,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise BootEpochUnavailable(f"sysctl unavailable: {exc}") from exc
    if result.returncode != 0:
        raise BootEpochUnavailable(
            f"sysctl kern.boottime failed: rc={result.returncode} "
            f"stderr={result.stderr.decode(errors='replace').strip()}"
        )
    line = result.stdout.decode("utf-8", errors="replace").strip()
    # Format: "{ sec = 1719410011, usec = 123456 } Wed Jun 26 14:13:31 2024"
    sec: int | None = None
    usec: int = 0
    for token in line.replace("{", "").replace("}", "").replace(",", " ").split():
        if token == "sec":
            continue
        if token == "usec":
            continue
        if token == "=":
            continue
        if sec is None:
            try:
                sec = int(token)
            except ValueError:
                continue
        else:
            try:
                usec = int(token)
            except ValueError:
                pass
            break
    if sec is None:
        raise BootEpochUnavailable(f"sysctl output unparseable: {line!r}")
    return sec * 1_000_000_000 + usec * 1_000


def _read_boot_epoch_ns_linux() -> int:
    try:
        proc_stat = Path("/proc/stat").read_text(encoding="utf-8")
    except OSError as exc:
        raise BootEpochUnavailable(f"/proc/stat unavailable: {exc}") from exc
    for line in proc_stat.splitlines():
        if line.startswith("btime "):
            try:
                return int(line.split()[1]) * 1_000_000_000
            except (IndexError, ValueError) as exc:
                raise BootEpochUnavailable(
                    f"/proc/stat btime unparseable: {line!r}"
                ) from exc
    raise BootEpochUnavailable("btime not found in /proc/stat")


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _clock_dir(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "clock"


def _jsonl_path(repo_root: Path) -> Path:
    return _clock_dir(repo_root) / "boot_clock_history.jsonl"


def _hmac_path(repo_root: Path) -> Path:
    return _clock_dir(repo_root) / "boot_clock_history.hmac"


def _lock_path(repo_root: Path) -> Path:
    return _clock_dir(repo_root) / "boot_clock_history.lock"


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------


def _atomic_write(target: Path, payload: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + f".tmp.{os.getpid()}")
    with open(tmp, "wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(str(tmp), str(target))


# ---------------------------------------------------------------------------
# Chain helpers
# ---------------------------------------------------------------------------


def _entry_canonical_for_hash(
    *,
    boot_epoch_ns: int,
    wall_at_boot_utc: str,
    recorded_at_utc: str,
    prev_hash: str,
) -> bytes:
    """Canonical bytes that feed into entry_hash = sha3_512(prev_hash || canonical)."""
    return canonical_json_bytes(
        {
            "boot_epoch_ns": boot_epoch_ns,
            "wall_at_boot_utc": wall_at_boot_utc,
            "recorded_at_utc": recorded_at_utc,
            "prev_hash": prev_hash,
        }
    )


def _compute_entry_hash(
    *,
    boot_epoch_ns: int,
    wall_at_boot_utc: str,
    recorded_at_utc: str,
    prev_hash: str,
) -> str:
    canonical = _entry_canonical_for_hash(
        boot_epoch_ns=boot_epoch_ns,
        wall_at_boot_utc=wall_at_boot_utc,
        recorded_at_utc=recorded_at_utc,
        prev_hash=prev_hash,
    )
    return sha3_512_hex(prev_hash.encode("ascii") + canonical).digest_hex


def _hmac_sha3_512_file(key: bytes, jsonl_path: Path) -> str:
    mac = hmac.new(key, b"", "sha3_512")
    if jsonl_path.is_file():
        with open(jsonl_path, "rb") as fh:
            while True:
                chunk = fh.read(64 * 1024)
                if not chunk:
                    break
                mac.update(chunk)
    return mac.hexdigest()


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------


def read_boot_clock_history(repo_root: Path) -> list[BootClockHistoryEntry]:
    """Read every entry from ``boot_clock_history.jsonl``; empty list if absent."""
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    path = _jsonl_path(repo_root)
    if not path.is_file():
        return []
    entries: list[BootClockHistoryEntry] = []
    with open(path, "rb") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                entries.append(BootClockHistoryEntry(**obj))
            except (json.JSONDecodeError, TypeError) as exc:
                raise BootClockHistoryCorrupt(
                    f"F-ADM-09 boot_clock_history.jsonl line {lineno} corrupt: {exc}"
                ) from exc
    return entries


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------


def verify_boot_clock_history_chain(
    *,
    repo_root: Path,
    keystore: KeyStore,
    key_id: str = BOOT_HISTORY_HMAC_KEY_ID,
    tolerance_seconds: int = CLOCK_ROLLBACK_TOLERANCE_SECONDS,
) -> list[BootClockHistoryEntry]:
    """Walk the chain, assert wall-clock monotonic (with NTP-slop tolerance),
    and verify the HMAC trailer. Returns the list of entries on success.

    Invariants verified:

    * Empty jsonl + absent trailer → legitimate first boot (returns []).
    * Non-empty jsonl + absent trailer → F-ADM-09 TrailerMissing.
    * Non-empty jsonl + trailer → full-file HMAC MUST match trailer.
    * Chain: each entry's ``prev_hash`` equals the prior entry's
      ``entry_hash``; first entry's ``prev_hash`` = 128 zeros.
    * Wall monotonicity: ``wall_at_boot_utc[i]`` ≥ max prior
      ``wall_at_boot_utc`` minus ``tolerance_seconds``.

    :raises BootClockHistoryError: any invariant broken.
    """
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(keystore, KeyStore):
        raise TypeError("keystore must be a KeyStore instance")

    entries = read_boot_clock_history(repo_root)
    jsonl = _jsonl_path(repo_root)
    trailer_path = _hmac_path(repo_root)

    if not entries:
        if trailer_path.is_file():
            raise BootClockHistoryTrailerMismatch(
                "F-ADM-09 trailer present without jsonl body"
            )
        return []

    if not trailer_path.is_file():
        raise BootClockHistoryTrailerMissing(
            "F-ADM-09 boot_clock_history.hmac absent but jsonl non-empty"
        )

    try:
        trailer_obj = json.loads(trailer_path.read_bytes())
        trailer = BootClockTrailer(**trailer_obj)
    except (json.JSONDecodeError, TypeError) as exc:
        raise BootClockHistoryTrailerMismatch(
            f"F-ADM-09 trailer unparseable: {exc}"
        ) from exc

    # Chain walk.
    prev = _GENESIS_PREV_HASH
    max_wall: _dt.datetime | None = None
    for idx, entry in enumerate(entries):
        if entry.prev_hash != prev:
            raise BootClockHistoryCorrupt(
                f"F-ADM-09 chain broken at entry {idx}: expected prev_hash={prev}, "
                f"got {entry.prev_hash}"
            )
        expected = _compute_entry_hash(
            boot_epoch_ns=entry.boot_epoch_ns,
            wall_at_boot_utc=entry.wall_at_boot_utc,
            recorded_at_utc=entry.recorded_at_utc,
            prev_hash=entry.prev_hash,
        )
        if not constant_time_equal(
            expected.encode("ascii"), entry.entry_hash.encode("ascii")
        ):
            raise BootClockHistoryCorrupt(
                f"F-ADM-09 entry_hash mismatch at entry {idx}"
            )
        wall = _parse_iso(entry.wall_at_boot_utc)
        if max_wall is not None:
            regression = (max_wall - wall).total_seconds()
            if regression > tolerance_seconds:
                raise BootClockHistoryRollback(
                    f"F-ADM-09 wall-clock rollback at entry {idx}: "
                    f"regressed {regression:.0f}s (tolerance {tolerance_seconds}s)"
                )
        if max_wall is None or wall > max_wall:
            max_wall = wall
        prev = entry.entry_hash

    # Trailer HMAC over full file.
    with keystore.retrieve(key_id) as key:
        key_bytes = bytes(key.view())
        actual = _hmac_sha3_512_file(key_bytes, jsonl)
    if not constant_time_equal(
        actual.encode("ascii"), trailer.boot_clock_history_hmac.lower().encode("ascii")
    ):
        raise BootClockHistoryTrailerMismatch(
            "F-ADM-09 trailer HMAC mismatch vs full-file hash"
        )
    if trailer.last_boot_epoch_ns != entries[-1].boot_epoch_ns:
        raise BootClockHistoryTrailerMismatch(
            f"F-ADM-09 trailer.last_boot_epoch_ns={trailer.last_boot_epoch_ns} "
            f"!= last entry {entries[-1].boot_epoch_ns}"
        )
    if trailer.last_seq_id != len(entries):
        raise BootClockHistoryTrailerMismatch(
            f"F-ADM-09 trailer.last_seq_id={trailer.last_seq_id} != {len(entries)}"
        )

    return entries


# ---------------------------------------------------------------------------
# Append (§4.8 v4 single-held-lock atomic)
# ---------------------------------------------------------------------------


def append_boot_clock_record(
    *,
    repo_root: Path,
    record: BootClockRecord,
    keystore: KeyStore,
    key_id: str = BOOT_HISTORY_HMAC_KEY_ID,
    tolerance_seconds: int = CLOCK_ROLLBACK_TOLERANCE_SECONDS,
) -> BootClockHistoryEntry:
    """Append one entry to ``boot_clock_history.jsonl`` under a single held
    ``fcntl.LOCK_EX``. Recomputes the rolling HMAC trailer atomically.

    Idempotency: if the latest entry's ``boot_epoch_ns`` equals
    ``record.boot_epoch_ns`` byte-for-byte, returns the existing entry
    without writing (per §9 step 2.5 "process running under a boot that
    was already recorded").

    :raises TypeError: E-001 arg-type.
    :raises BootClockHistoryRollback: wall-clock regression past tolerance.
    :raises BootClockHistoryError: any other chain / trailer invariant broken.
    """
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(record, BootClockRecord):
        raise TypeError("record must be BootClockRecord")
    if not isinstance(keystore, KeyStore):
        raise TypeError("keystore must be a KeyStore instance")

    clock_dir = _clock_dir(repo_root)
    clock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = _lock_path(repo_root)
    jsonl_path = _jsonl_path(repo_root)
    trailer_path = _hmac_path(repo_root)

    lock_fd = safe_open_lock_file(lock_path)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)

        # Verify chain from disk (inside lock — caller may not have).
        existing = verify_boot_clock_history_chain(
            repo_root=repo_root,
            keystore=keystore,
            key_id=key_id,
            tolerance_seconds=tolerance_seconds,
        )

        # Idempotency: same boot already recorded.
        if existing and existing[-1].boot_epoch_ns == record.boot_epoch_ns:
            return existing[-1]

        # Rollback check against max prior wall.
        new_wall = _parse_iso(record.wall_at_boot_utc)
        if existing:
            max_prior = max(_parse_iso(e.wall_at_boot_utc) for e in existing)
            regression = (max_prior - new_wall).total_seconds()
            if regression > tolerance_seconds:
                raise BootClockHistoryRollback(
                    f"F-ADM-09 new record regresses {regression:.0f}s vs prior "
                    f"max (tolerance {tolerance_seconds}s)"
                )

        prev_hash = existing[-1].entry_hash if existing else _GENESIS_PREV_HASH
        recorded_at = _iso_utc_now()
        entry_hash = _compute_entry_hash(
            boot_epoch_ns=record.boot_epoch_ns,
            wall_at_boot_utc=record.wall_at_boot_utc,
            recorded_at_utc=recorded_at,
            prev_hash=prev_hash,
        )
        entry = BootClockHistoryEntry(
            boot_epoch_ns=record.boot_epoch_ns,
            wall_at_boot_utc=record.wall_at_boot_utc,
            recorded_at_utc=recorded_at,
            prev_hash=prev_hash,
            entry_hash=entry_hash,
        )

        # Append line.
        line_bytes = canonical_json_bytes(asdict(entry)) + b"\n"
        with open(jsonl_path, "ab") as fh:
            fh.write(line_bytes)
            fh.flush()
            os.fsync(fh.fileno())

        # Recompute trailer HMAC over full file.
        with keystore.retrieve(key_id) as key:
            key_bytes = bytes(key.view())
            full_hmac = _hmac_sha3_512_file(key_bytes, jsonl_path)

        trailer = BootClockTrailer(
            boot_clock_history_hmac=full_hmac,
            last_boot_epoch_ns=record.boot_epoch_ns,
            last_seq_id=len(existing) + 1,
            wall_at_write_utc=_iso_utc_now(),
        )
        _atomic_write(trailer_path, canonical_json_bytes(asdict(trailer)))

        # Fsync parent dir so rename is durable.
        parent_fd = os.open(str(clock_dir), os.O_RDONLY)
        try:
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)

        return entry
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)
