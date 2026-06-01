"""Sovereignty init marker — RT-v4 HIGH-1 first-boot-reset closure. [§2.7b, §3.11b, §4.9a, §9 step 7c.0a/b]

Section 1 Round I. Closes the RT-v4 HIGH-1 "attacker truncates all ledgers +
deletes watermarks = treated as legitimate first boot" attack by writing a
signed marker ONCE on the genuine first boot and verifying it on every
subsequent boot.

Flow:

* Every boot calls :func:`verify_sovereignty_init_marker`. Three outcomes:
  - **(a)** marker+HMAC present + verifies → returns the marker body.
  - **(b)** marker+HMAC absent + every ledger empty + no watermark body →
    returns ``None`` — caller MUST invoke
    :func:`write_sovereignty_init_marker_first_boot` before any ledger
    append or watermark write.
  - **(c)** any other combination → fail-closed
    (:class:`SovereigntyInitMarkerMissing` F-ADM-11 or
    :class:`SovereigntyInitMarkerMismatch` F-ADM-12).

* :func:`write_sovereignty_init_marker_first_boot` writes body + HMAC
  trailer under a single held ``fcntl.LOCK_EX`` on ``init.marker.lock``,
  with O_NOFOLLOW + inode fstat via :func:`safe_open_lock_file`.

Key material: ``tilth.sovereignty.init.hmac.v1`` (§8 constant).

Blueprint refs:

* §2.7b    SovereigntyInitMarker + HmacTrailer schemas
* §3.11b   verify + write signatures
* §4.9a    implementation sketch
* §9 step 7c.0a/7c.0b — boot sequence integration
* §6.5 F-ADM-11 / F-ADM-12 failure codes
* §7.15    test coverage
"""

from __future__ import annotations

import datetime as _dt
import fcntl
import hmac
import json
import os
import platform
from dataclasses import asdict, dataclass
from pathlib import Path

from pipeline.sovereignty.audit import canonical_json_bytes
from pipeline.sovereignty.crypto_primitives import constant_time_equal
from pipeline.sovereignty.keys import KeyStore
from pipeline.sovereignty.lockfile import safe_open_lock_file

__all__ = [
    "SOVEREIGNTY_INIT_HMAC_KEY_ID",
    "INIT_MARKER_SCHEMA_VERSION",
    "LedgerState",
    "SovereigntyInitMarker",
    "SovereigntyInitMarkerHmacTrailer",
    "SovereigntyInitMarkerError",
    "SovereigntyInitMarkerMissing",
    "SovereigntyInitMarkerMismatch",
    "SovereigntyInitMarkerAlreadyExists",
    "verify_sovereignty_init_marker",
    "write_sovereignty_init_marker_first_boot",
]

SOVEREIGNTY_INIT_HMAC_KEY_ID: str = "tilth.sovereignty.init.hmac.v1"
INIT_MARKER_SCHEMA_VERSION: int = 1


# ---------------------------------------------------------------------------
# Exceptions (E-014 family)
# ---------------------------------------------------------------------------


class SovereigntyInitMarkerError(RuntimeError):
    """Common parent for F-ADM-11 / F-ADM-12."""

    code: str = "F-ADM"


class SovereigntyInitMarkerMissing(SovereigntyInitMarkerError):
    """F-ADM-11 — marker XOR hmac present (partial tamper or crash recovery)."""

    code = "F-ADM-11"


class SovereigntyInitMarkerMismatch(SovereigntyInitMarkerError):
    """F-ADM-12 — HMAC mismatch OR first-boot-reset signature."""

    code = "F-ADM-12"


class SovereigntyInitMarkerAlreadyExists(SovereigntyInitMarkerError):
    """F-ADM-11 — first-boot write found the file already there (race)."""

    code = "F-ADM-11"


# ---------------------------------------------------------------------------
# Dataclasses (§2.7b)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class LedgerState:
    """Input to :func:`verify_sovereignty_init_marker`. [§4.9a]

    ``last_seq_id == 0`` + ``watermark_body_exists is False`` means empty
    ledger + no prior watermark. Both are needed to distinguish the
    legitimate first-boot state (outcome (b)) from the attack state
    (outcome (c)).
    """

    ledger_name: str
    last_seq_id: int
    watermark_body_exists: bool


@dataclass(frozen=True, kw_only=True)
class SovereigntyInitMarker:
    """§2.7b v5 schema. Written ONCE on first boot."""

    init_version: int
    created_at_utc: str
    hostname: str
    operator_slug: str | None
    boot_epoch_ns_first: int
    boot_clock_history_seq_at_init: int


@dataclass(frozen=True, kw_only=True)
class SovereigntyInitMarkerHmacTrailer:
    """§2.7b HMAC trailer. ``init_hmac`` = HMAC-SHA3-512 over canonical JSON of body."""

    init_version: int
    init_hmac: str
    wall_at_write_utc: str


# ---------------------------------------------------------------------------
# Canonical JSON discipline (§2.7b HMAC canon)
# ---------------------------------------------------------------------------


def _marker_canonical_bytes(body: SovereigntyInitMarker) -> bytes:
    """Canonical JSON of marker body for HMAC computation.

    Delegates to :func:`pipeline.sovereignty.audit.canonical_json_bytes`
    (sorted keys, ASCII-only, no whitespace separators, UTF-8).
    """
    return canonical_json_bytes(asdict(body))


def _trailer_canonical_bytes(trailer: SovereigntyInitMarkerHmacTrailer) -> bytes:
    return canonical_json_bytes(asdict(trailer))


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


# ---------------------------------------------------------------------------
# Verify (every boot, step 7c.0a)
# ---------------------------------------------------------------------------


def verify_sovereignty_init_marker(
    *,
    marker_path: Path,
    hmac_path: Path,
    keystore: KeyStore,
    ledger_states: dict[str, LedgerState],
    key_id: str = SOVEREIGNTY_INIT_HMAC_KEY_ID,
) -> SovereigntyInitMarker | None:
    """§3.11b verify. Returns body on outcome (a), ``None`` on outcome (b),
    raises on outcome (c).

    :raises TypeError: E-001 arg-type.
    :raises SovereigntyInitMarkerMissing: F-ADM-11.
    :raises SovereigntyInitMarkerMismatch: F-ADM-12.
    """
    if not isinstance(marker_path, Path):
        raise TypeError("marker_path must be pathlib.Path")
    if not isinstance(hmac_path, Path):
        raise TypeError("hmac_path must be pathlib.Path")
    if not isinstance(keystore, KeyStore):
        raise TypeError("keystore must be a KeyStore instance")
    if not isinstance(ledger_states, dict):
        raise TypeError("ledger_states must be dict[str, LedgerState]")
    if not isinstance(key_id, str):
        raise TypeError("key_id must be str")

    marker_present = marker_path.is_file()
    hmac_present = hmac_path.is_file()

    all_ledgers_empty = all(
        isinstance(st, LedgerState) and st.last_seq_id == 0
        for st in ledger_states.values()
    )
    any_watermark_body = any(
        isinstance(st, LedgerState) and st.watermark_body_exists
        for st in ledger_states.values()
    )

    # Outcome (b) — legitimate first boot.
    if (
        not marker_present
        and not hmac_present
        and all_ledgers_empty
        and not any_watermark_body
    ):
        return None

    # Outcome (c) — fail-closed.
    if marker_present != hmac_present:
        raise SovereigntyInitMarkerMissing(
            f"F-ADM-11 marker_present={marker_present} hmac_present={hmac_present} "
            "— first-boot-reset attack or partial tamper"
        )
    if not marker_present and not hmac_present:
        # Both absent but ledgers non-empty OR watermark body present.
        raise SovereigntyInitMarkerMismatch(
            "F-ADM-12 init marker absent but ledgers or watermarks non-empty — "
            "RT-v4 HIGH-1 first-boot-reset signature"
        )

    # Outcome (a) — both present; verify HMAC.
    try:
        marker_bytes = marker_path.read_bytes()
        trailer_bytes = hmac_path.read_bytes()
    except OSError as exc:
        raise SovereigntyInitMarkerMismatch(
            f"F-ADM-12 init marker files unreadable: {exc}"
        ) from exc

    try:
        marker_obj = json.loads(marker_bytes)
        trailer_obj = json.loads(trailer_bytes)
    except json.JSONDecodeError as exc:
        raise SovereigntyInitMarkerMismatch(
            f"F-ADM-12 init marker JSON corrupt: {exc}"
        ) from exc

    try:
        body = SovereigntyInitMarker(**marker_obj)
        trailer = SovereigntyInitMarkerHmacTrailer(**trailer_obj)
    except TypeError as exc:
        raise SovereigntyInitMarkerMismatch(
            f"F-ADM-12 init marker schema drift: {exc}"
        ) from exc

    if body.init_version != trailer.init_version:
        raise SovereigntyInitMarkerMismatch(
            f"F-ADM-12 init_version skew: body={body.init_version} "
            f"trailer={trailer.init_version}"
        )

    # HMAC over the CANONICAL form of the body (not the raw on-disk bytes —
    # that way whitespace-only tamper is caught by re-canonicalization).
    canonical = _marker_canonical_bytes(body)
    with keystore.retrieve(key_id) as key:
        key_bytes = bytes(key.view())
        expected = hmac.new(key_bytes, canonical, "sha3_512").hexdigest()

    if not constant_time_equal(
        expected.encode("ascii"), trailer.init_hmac.lower().encode("ascii")
    ):
        raise SovereigntyInitMarkerMismatch(
            "F-ADM-12 init marker HMAC mismatch — RT-v4 HIGH-1 first-boot-reset"
        )

    return body


# ---------------------------------------------------------------------------
# Write (first boot only, step 7c.0b)
# ---------------------------------------------------------------------------


def _atomic_write(target: Path, payload: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + f".tmp.{os.getpid()}")
    with open(tmp, "wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(str(tmp), str(target))
    parent_fd = os.open(str(target.parent), os.O_RDONLY)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def write_sovereignty_init_marker_first_boot(
    *,
    marker_path: Path,
    hmac_path: Path,
    lock_path: Path,
    keystore: KeyStore,
    boot_clock_history_seq: int,
    boot_epoch_ns: int,
    operator_slug: str | None = None,
    key_id: str = SOVEREIGNTY_INIT_HMAC_KEY_ID,
) -> SovereigntyInitMarker:
    """§3.11b first-boot write. Single held ``fcntl.LOCK_EX`` across body +
    HMAC trailer + fsyncs. Raises if either file already exists.

    :raises TypeError: E-001 arg-type gate.
    :raises SovereigntyInitMarkerAlreadyExists: F-ADM-11 — race / re-run.
    :raises LockFileSymlinkAttack: F-ISO-07 from lock-file open.
    """
    if not isinstance(marker_path, Path):
        raise TypeError("marker_path must be pathlib.Path")
    if not isinstance(hmac_path, Path):
        raise TypeError("hmac_path must be pathlib.Path")
    if not isinstance(lock_path, Path):
        raise TypeError("lock_path must be pathlib.Path")
    if not isinstance(keystore, KeyStore):
        raise TypeError("keystore must be a KeyStore instance")
    if not isinstance(boot_clock_history_seq, int) or isinstance(
        boot_clock_history_seq, bool
    ):
        raise TypeError("boot_clock_history_seq must be int")
    if not isinstance(boot_epoch_ns, int) or isinstance(boot_epoch_ns, bool):
        raise TypeError("boot_epoch_ns must be int")
    if operator_slug is not None and not isinstance(operator_slug, str):
        raise TypeError("operator_slug must be str or None")

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    marker_path.parent.mkdir(parents=True, exist_ok=True)
    hmac_path.parent.mkdir(parents=True, exist_ok=True)

    lock_fd = safe_open_lock_file(lock_path)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        if marker_path.exists() or hmac_path.exists():
            raise SovereigntyInitMarkerAlreadyExists(
                "F-ADM-11 init marker already exists — write-once invariant"
            )

        body = SovereigntyInitMarker(
            init_version=INIT_MARKER_SCHEMA_VERSION,
            created_at_utc=_iso_utc_now(),
            hostname=platform.node(),
            operator_slug=operator_slug,
            boot_epoch_ns_first=boot_epoch_ns,
            boot_clock_history_seq_at_init=boot_clock_history_seq,
        )
        body_bytes = _marker_canonical_bytes(body)

        with keystore.retrieve(key_id) as key:
            key_bytes = bytes(key.view())
            hmac_hex = hmac.new(key_bytes, body_bytes, "sha3_512").hexdigest()

        trailer = SovereigntyInitMarkerHmacTrailer(
            init_version=INIT_MARKER_SCHEMA_VERSION,
            init_hmac=hmac_hex,
            wall_at_write_utc=_iso_utc_now(),
        )
        trailer_bytes = _trailer_canonical_bytes(trailer)

        # Body first so the asymmetric failure (marker-present / hmac-absent)
        # produces F-ADM-11 on next boot, which is the documented recovery
        # path (§4.9a recovery notes).
        _atomic_write(marker_path, body_bytes)
        _atomic_write(hmac_path, trailer_bytes)
        return body
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)
