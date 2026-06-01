"""§13.5.3 + §13.8.6 — Consent ledger substrate.

Per-recipient × per-channel YAML store with fcntl.flock(LOCK_EX) atomic ops.
Implements:

- Atomic read/write of single (recipient_id, channel) entry per §15 v1 NF-02
  closure precedent (30-second lock timeout, fail-closed).
- Cross-channel opt-out propagation per RT-02 closure + RT-C2-02 closure
  copy-on-write rollback semantics (all-or-nothing across 5 ledger files).
- Send-time consent re-read per RT-01 closure (lock-held-through-transport
  per RT-C2-05 closure).
- yaml.safe_load only per RT-27 closure / R-DATACOLLECTOR-CARD-SAFE-LOAD.

This module is always-local per v7.0.7 §4.1 classification routing. It writes
operational Confidential data (PII-bearing consent metadata). Cloud-routed code
paths MUST NOT import this module — F-CLASS-OUTBOUND-BOUNDARY enforces.
"""
from __future__ import annotations

import dataclasses
import errno
import fcntl
import os
import shutil
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Literal

import yaml

from pipeline.orchestrator.seats.data_collector import ConsentLedgerEntry


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CHANNELS: tuple[str, ...] = ("email", "sms", "voice", "telegram", "whatsapp")
LOCK_TIMEOUT_SECONDS: int = 30
PROPAGATION_LOCK_FILENAME: str = ".propagation_lock"

OPT_OUT_KEYWORDS: frozenset[str] = frozenset({
    "STOP", "UNSUBSCRIBE", "END", "QUIT", "CANCEL",
})


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class LedgerError(Exception):
    """Base for consent-ledger substrate errors."""


class LedgerLockTimeout(LedgerError):
    """fcntl.flock acquisition exceeded LOCK_TIMEOUT_SECONDS — fail-closed."""


class LedgerSchemaError(LedgerError):
    """On-disk ledger row failed Pydantic-equivalent dataclass validation."""


class LedgerPropagationError(LedgerError):
    """Cross-channel opt-out propagation rolled back — atomic write failed."""


# ---------------------------------------------------------------------------
# Path construction
# ---------------------------------------------------------------------------

def ledger_path(root: Path, recipient_id: str, channel: str) -> Path:
    """Resolves the canonical per-recipient × per-channel ledger path."""
    if channel not in CHANNELS:
        raise LedgerSchemaError(f"unknown channel: {channel!r}")
    return Path(root) / f"{recipient_id}__{channel}.yaml"


# ---------------------------------------------------------------------------
# Locking — fcntl.flock with timeout
# ---------------------------------------------------------------------------

@contextmanager
def _flock_exclusive(fp, *, timeout_seconds: int = LOCK_TIMEOUT_SECONDS) -> Iterator[None]:
    """Acquire LOCK_EX with poll-loop timeout; fail-closed on exceed."""
    deadline = _monotonic() + timeout_seconds
    while True:
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except OSError as exc:
            if exc.errno not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            if _monotonic() >= deadline:
                raise LedgerLockTimeout(
                    f"fcntl.flock timeout after {timeout_seconds}s"
                ) from exc
            _sleep_short()
    try:
        yield
    finally:
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
        except OSError:
            pass


def _monotonic() -> float:
    import time
    return time.monotonic()


def _sleep_short() -> None:
    import time
    time.sleep(0.05)


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def _entry_to_dict(entry: ConsentLedgerEntry) -> dict:
    """Convert a frozen dataclass to a serializable dict; datetimes → ISO-8601."""
    d = dataclasses.asdict(entry)
    d["consent_captured_at_utc"] = entry.consent_captured_at_utc.isoformat()
    if entry.opt_out_at_utc is not None:
        d["opt_out_at_utc"] = entry.opt_out_at_utc.isoformat()
    return d


def _dict_to_entry(data: dict) -> ConsentLedgerEntry:
    """Inverse of _entry_to_dict."""
    if not isinstance(data, dict):
        raise LedgerSchemaError(f"expected dict, got {type(data).__name__}")
    required = {
        "recipient_id", "channel", "consent_active",
        "consent_captured_at_utc", "consent_capture_method",
        "opt_out_active", "opt_out_at_utc",
        "opt_out_propagated_from_channel", "frequency_cap_lookback_days",
        "recent_outbound_log", "state_code_for_rules", "audit_chain",
    }
    missing = required - set(data.keys())
    if missing:
        raise LedgerSchemaError(f"missing fields: {sorted(missing)}")
    try:
        return ConsentLedgerEntry(
            recipient_id=data["recipient_id"],
            channel=data["channel"],
            consent_active=bool(data["consent_active"]),
            consent_captured_at_utc=_parse_dt(data["consent_captured_at_utc"]),
            consent_capture_method=data["consent_capture_method"],
            opt_out_active=bool(data["opt_out_active"]),
            opt_out_at_utc=_parse_dt(data["opt_out_at_utc"]) if data["opt_out_at_utc"] else None,
            opt_out_propagated_from_channel=list(data["opt_out_propagated_from_channel"]),
            frequency_cap_lookback_days=int(data["frequency_cap_lookback_days"]),
            recent_outbound_log=list(data["recent_outbound_log"]),
            state_code_for_rules=data["state_code_for_rules"],
            audit_chain=list(data["audit_chain"]),
        )
    except (TypeError, ValueError) as exc:
        raise LedgerSchemaError(str(exc)) from exc


def _parse_dt(value) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    if isinstance(value, str):
        # ISO-8601 with optional trailing Z
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    raise LedgerSchemaError(f"unparseable datetime: {value!r}")


# ---------------------------------------------------------------------------
# Single-entry read / write — RT-01 + RT-22 + §13.5.3 atomic discipline
# ---------------------------------------------------------------------------

def read_entry(root: Path, recipient_id: str, channel: str) -> ConsentLedgerEntry | None:
    """Atomic read of a single (recipient_id, channel) ledger entry.

    Returns None when the ledger file does not exist (caller handles via
    F-DATACOLLECTOR-CONSENT-MISSING.ledger_absent).
    """
    path = ledger_path(root, recipient_id, channel)
    if not path.exists():
        return None
    # Symlink escape: per RT-26 mirror + §13.9.4 .symlink_escape — refuse symlinks.
    if path.is_symlink():
        raise LedgerSchemaError(f"refusing symlink ledger path: {path}")
    with open(path, "rb") as fp:
        with _flock_exclusive(fp):
            data = yaml.safe_load(fp)
    return _dict_to_entry(data)


@contextmanager
def locked_read_entry(
    root: Path,
    recipient_id: str,
    channel: str,
    *,
    timeout_seconds: int = LOCK_TIMEOUT_SECONDS,
) -> Iterator[ConsentLedgerEntry | None]:
    """RT-C2-05 closure — hold LOCK_EX on the ledger entry through context body.

    Used by ``outbound_batch.dispatch_after_operator_approval`` to enforce that
    the send-time consent re-read and the transport substrate call happen with
    the lock held continuously (no TOCTOU window between re-read and send).

    Yields the parsed ``ConsentLedgerEntry`` (or ``None`` if the ledger file is
    absent). Raises ``LedgerLockTimeout`` if the lock cannot be acquired within
    ``timeout_seconds`` (default 30s per §13.7 / §15 v1 NF-02 pattern).

    The lock is released when the context body exits — including on exception.
    """
    path = ledger_path(root, recipient_id, channel)
    if not path.exists():
        yield None
        return
    if path.is_symlink():
        raise LedgerSchemaError(f"refusing symlink ledger path: {path}")
    with open(path, "rb") as fp:
        with _flock_exclusive(fp, timeout_seconds=timeout_seconds):
            data = yaml.safe_load(fp)
            entry = _dict_to_entry(data)
            yield entry


def write_entry(root: Path, entry: ConsentLedgerEntry) -> None:
    """Atomic write of a single (recipient_id, channel) ledger entry."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    path = ledger_path(root, entry.recipient_id, entry.channel)
    if path.is_symlink():
        raise LedgerSchemaError(f"refusing symlink ledger path: {path}")
    tmp_fd, tmp_path = tempfile.mkstemp(
        prefix=f".{entry.recipient_id}__{entry.channel}.",
        suffix=".yaml.tmp",
        dir=str(root),
    )
    try:
        with os.fdopen(tmp_fd, "w") as fp:
            with _flock_exclusive(fp):
                yaml.safe_dump(
                    _entry_to_dict(entry),
                    fp,
                    sort_keys=True,
                    default_flow_style=False,
                )
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Cross-channel opt-out propagation — RT-02 + RT-C2-02 closure semantics
# ---------------------------------------------------------------------------

def propagate_opt_out(
    root: Path,
    recipient_id: str,
    *,
    source_channel: Literal["email", "sms", "voice", "telegram", "whatsapp", "operator_explicit"],
    received_at_utc: datetime,
) -> dict[str, ConsentLedgerEntry]:
    """All-or-nothing cross-channel opt-out propagation per RT-C2-02.

    Snapshots all five (recipient × channel) ledger files; writes new
    `opt_out_active=True` state to all five; on partial failure, restores from
    snapshot via os.rename. Returns the new per-channel entries on success.

    Raises LedgerPropagationError on rollback failure (PRE write fail-closed
    realized by F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED gate).
    """
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / PROPAGATION_LOCK_FILENAME
    # Coordinator lock so concurrent propagations serialize.
    with open(lock_path, "a+b") as lockfp:
        with _flock_exclusive(lockfp):
            return _propagate_locked(
                root=root,
                recipient_id=recipient_id,
                source_channel=source_channel,
                received_at_utc=received_at_utc,
            )


def _propagate_locked(
    *,
    root: Path,
    recipient_id: str,
    source_channel: str,
    received_at_utc: datetime,
) -> dict[str, ConsentLedgerEntry]:
    # Snapshot existing files to temp dir; if any later write fails, restore.
    snapshot_dir = Path(tempfile.mkdtemp(prefix=f".propagate_{recipient_id}__", dir=str(root)))
    snapshotted: list[tuple[Path, Path]] = []  # (canonical_path, snapshot_path)
    new_entries: dict[str, ConsentLedgerEntry] = {}
    try:
        for channel in CHANNELS:
            canonical = ledger_path(root, recipient_id, channel)
            if canonical.exists():
                snap = snapshot_dir / canonical.name
                shutil.copy2(canonical, snap)
                snapshotted.append((canonical, snap))

        # Compute new state for each channel that has a ledger entry.
        for channel in CHANNELS:
            existing = read_entry(root, recipient_id, channel)
            if existing is None:
                # No consent capture on this channel — nothing to propagate.
                continue
            propagation_list = list(existing.opt_out_propagated_from_channel)
            if source_channel not in propagation_list:
                propagation_list.append(source_channel)
            updated = dataclasses.replace(
                existing,
                opt_out_active=True,
                opt_out_at_utc=received_at_utc,
                opt_out_propagated_from_channel=propagation_list,
                audit_chain=[
                    *existing.audit_chain,
                    {
                        "kind": "opt_out_propagation",
                        "source_channel": source_channel,
                        "at_utc": received_at_utc.isoformat(),
                    },
                ],
            )
            new_entries[channel] = updated

        # Now write all new entries; any failure → rollback.
        written: list[Path] = []
        try:
            for channel, updated_entry in new_entries.items():
                write_entry(root, updated_entry)
                written.append(ledger_path(root, recipient_id, channel))
        except Exception as write_exc:
            # Rollback: restore from snapshot.
            for canonical, snap in snapshotted:
                try:
                    shutil.copy2(snap, canonical)
                except OSError:
                    pass
            # Remove any files that were created but not in snapshot.
            for path in written:
                if not any(canonical == path for canonical, _ in snapshotted):
                    try:
                        os.unlink(path)
                    except OSError:
                        pass
            raise LedgerPropagationError(
                f"cross-channel opt-out propagation failed; rolled back: {write_exc}"
            ) from write_exc

        return new_entries
    finally:
        # Clean up snapshot directory.
        try:
            shutil.rmtree(snapshot_dir, ignore_errors=True)
        except OSError:
            pass


def is_opt_out_signal(message_body: str) -> bool:
    """RFC §13.6.2 STOP shortcode handling — case-insensitive keyword match."""
    if not isinstance(message_body, str):
        return False
    stripped = message_body.strip().upper()
    return stripped in OPT_OUT_KEYWORDS


# ---------------------------------------------------------------------------
# Send-time consent re-read — RT-01 closure
# ---------------------------------------------------------------------------

def compute_consent_state_hash(entry: ConsentLedgerEntry) -> str:
    """SHA3-512 full digest over canonical-JSON of the consent state.

    Per RT-13 closure — full 128-hex-char digest required for runtime comparison.
    """
    import hashlib
    import json
    canonical = json.dumps(_entry_to_dict(entry), sort_keys=True, separators=(",", ":"))
    return hashlib.sha3_512(canonical.encode("utf-8")).hexdigest()


__all__ = [
    "CHANNELS",
    "LOCK_TIMEOUT_SECONDS",
    "OPT_OUT_KEYWORDS",
    "LedgerError",
    "LedgerLockTimeout",
    "LedgerSchemaError",
    "LedgerPropagationError",
    "compute_consent_state_hash",
    "is_opt_out_signal",
    "ledger_path",
    "locked_read_entry",
    "propagate_opt_out",
    "read_entry",
    "write_entry",
]
