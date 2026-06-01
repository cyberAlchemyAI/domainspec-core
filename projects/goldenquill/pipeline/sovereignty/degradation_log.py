"""Degradation log — M10 author-seat degraded runs + M13 review-seat bypass events.

Section 1 Round G. Owns:

* :class:`DegradationEvent` — §2.6 schema frozen dataclass.
* :func:`record_degradation` — append-only, hash-chained via
  Round-B :func:`pipeline.sovereignty.audit.append_to_ledger`.
* :func:`read_degradation_tail` — O(n) tail scan for the last ``n`` events.
* :func:`verify_chain` — delegates to :func:`audit.verify_ledger` (fast-tail
  or full verify).

Blueprint references:

* §2.6   DegradationEvent schema
* §3.8   record_degradation public API
* §4.7   M10 author-seat degraded-run recording (Section 1 is recorder only)
* §4.8   M13 review-seat bypass recording (Section 1 is recorder + predicate
         via admin_risk.bypass_is_active)
* §6.5   F-DEG-01..03
* §7.3   unit tests

E-enforcement:

* E-001 arg-type validation before any I/O
* E-005 canonical JSON (sorted keys + ASCII + no whitespace)
* E-014 family exception taxonomy (:class:`DegradationError` parent carries
  a ``code`` attribute; subclasses override.)

v0.1 scope (deferred):

* Boot-time watermark verification — owned by Round I boot.py.
* Full keystore integration — callers pass raw HMAC key bytes; Round I
  wires keystore.retrieve into the record_degradation entrypoint.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from pipeline.sovereignty.audit import (
    LedgerChainBroken,
    LedgerTrailer,
    LedgerUnreadable,
    append_to_ledger,
    verify_ledger,
)

__all__ = [
    "DegradationEvent",
    "DegradationError",
    "BypassExpired",
    "DegradationLogCorrupt",
    "VALID_EVENT_KINDS",
    "VALID_SEATS",
    "record_degradation",
    "read_degradation_tail",
    "verify_chain",
]

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§2.6 DegradationEvent",
            "§3.8 record_degradation public API",
            "§4.7 M10 author-seat degraded-run recording",
            "§4.8 M13 review-seat bypass recording",
            "§6.5 F-DEG-01..03",
            "§7.3 unit tests",
        ],
        "hash_at_lock": None,
        "hash_source_version": "v6",
    },
}

# --- Constants (§2.6 string-valued enums) ---
VALID_EVENT_KINDS: frozenset[str] = frozenset(
    [
        "author_seat_degraded_run",
        "review_seat_bypass_active",
        "bypass_expired",
        "bypass_renewed",
    ]
)
VALID_SEATS: frozenset[str] = frozenset(
    [
        "scout",
        "scribe",
        "editor",
        "judge",
        "red_team",
        "code_review",
        "reasoner_review",
    ]
)


# ---------------------------------------------------------------------------
# Exceptions (E-014 family taxonomy)
# ---------------------------------------------------------------------------


class DegradationError(RuntimeError):
    """Common parent for F-DEG-01..03. Carries a ``code`` attribute."""

    code: str = "F-DEG"


class DegradationLogCorrupt(DegradationError):
    """F-DEG-01. Ledger chain / HMAC trailer corruption."""

    code = "F-DEG-01"


class BypassExpired(DegradationError):
    """F-DEG-02. M13 bypass past expiry used.

    Not a crash — Section 5's router check consults ``expires_at`` and
    treats an expired bypass as "no bypass", re-entering hard-abort
    for the affected review seat. Section 1 raises this to distinguish
    "no bypass event exists" from "bypass event exists but is past its
    wall/mono expiry".
    """

    code = "F-DEG-02"


# ---------------------------------------------------------------------------
# Dataclass (§2.6)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class DegradationEvent:
    """§2.6 schema. Frozen.

    Matches the duck-type that :func:`admin_risk.bypass_is_active` consumes:
    ``event_kind``, ``expires_at``, ``expires_monotonic_ns``,
    ``boot_epoch_ns_at_issuance``.
    """

    seq_id: int
    timestamp_utc: str
    issued_monotonic_ns: int
    event_kind: str
    seat: str
    reason_code: str
    duration_seconds: int | None
    authorization_id: int | None
    expires_at: str | None
    expires_monotonic_ns: int | None
    boot_epoch_ns_at_issuance: int | None
    signed_by_operator: bool
    prev_hash: str
    entry_hash: str


# ---------------------------------------------------------------------------
# Path helpers (§2.8)
# ---------------------------------------------------------------------------


def _ledger_dir(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "ledgers"


def _ledger_path(repo_root: Path) -> Path:
    return _ledger_dir(repo_root) / "degradation.jsonl"


def _lock_path(repo_root: Path) -> Path:
    return _ledger_dir(repo_root) / "degradation.lock"


def _trailer_path(repo_root: Path) -> Path:
    return _ledger_dir(repo_root) / "degradation.hmac"


def _watermarks_path(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "watermarks" / "ledger_watermarks.json"


def _watermarks_hmac_path(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "watermarks" / "ledger_watermarks.hmac"


def _watermarks_lock_path(repo_root: Path) -> Path:
    return repo_root / "sovereignty" / "watermarks" / "ledger_watermarks.lock"


# ---------------------------------------------------------------------------
# Public API — record
# ---------------------------------------------------------------------------


def record_degradation(
    *,
    repo_root: Path,
    event_kind: str,
    seat: str,
    reason_code: str,
    hmac_key: bytes,
    watermarks_hmac_key: bytes,
    duration_seconds: int | None = None,
    authorization_id: int | None = None,
    expires_at: str | None = None,
    expires_monotonic_ns: int | None = None,
    boot_epoch_ns_at_issuance: int | None = None,
    signed_by_operator: bool = False,
) -> DegradationEvent:
    """Append one §2.6 DegradationEvent to ``degradation.jsonl``.

    audit.append_to_ledger takes its own exclusive fcntl lock on
    ``degradation.lock`` — callers do not need to nest a second lock.
    Unlike admin_risk, degradation has no rate-limit; the upstream gate
    is Section 5's threshold detector (30 min for M10, operator ceremony
    for M13). Section 1's contract is just "every call is durable".

    :raises TypeError / ValueError: bad args (E-001).
    :raises LedgerUnreadable / LedgerChainBroken: pre-append chain verify
        failed.
    """
    # E-001 gate.
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(event_kind, str):
        raise TypeError("event_kind must be str")
    if not isinstance(seat, str):
        raise TypeError("seat must be str")
    if not isinstance(reason_code, str):
        raise TypeError("reason_code must be str")
    if not isinstance(hmac_key, (bytes, bytearray)):
        raise TypeError("hmac_key must be bytes")
    if not isinstance(watermarks_hmac_key, (bytes, bytearray)):
        raise TypeError("watermarks_hmac_key must be bytes")
    if duration_seconds is not None and not isinstance(duration_seconds, int):
        raise TypeError("duration_seconds must be int or None")
    if authorization_id is not None and not isinstance(authorization_id, int):
        raise TypeError("authorization_id must be int or None")
    if expires_at is not None and not isinstance(expires_at, str):
        raise TypeError("expires_at must be str or None")
    if expires_monotonic_ns is not None and not isinstance(
        expires_monotonic_ns, int
    ):
        raise TypeError("expires_monotonic_ns must be int or None")
    if boot_epoch_ns_at_issuance is not None and not isinstance(
        boot_epoch_ns_at_issuance, int
    ):
        raise TypeError("boot_epoch_ns_at_issuance must be int or None")
    if not isinstance(signed_by_operator, bool):
        raise TypeError("signed_by_operator must be bool")

    if event_kind not in VALID_EVENT_KINDS:
        raise ValueError(
            f"event_kind must be one of {sorted(VALID_EVENT_KINDS)}; "
            f"got {event_kind!r}"
        )
    if seat not in VALID_SEATS:
        raise ValueError(
            f"seat must be one of {sorted(VALID_SEATS)}; got {seat!r}"
        )
    if not reason_code:
        raise ValueError("reason_code must be non-empty")

    # §4.8 M13 bypass issuance MUST be operator-signed.
    if event_kind == "review_seat_bypass_active" and not signed_by_operator:
        raise ValueError(
            "F-DEG: event_kind='review_seat_bypass_active' requires "
            "signed_by_operator=True (M13 operator attestation)"
        )

    hmac_key_b = bytes(hmac_key)
    watermarks_hmac_key_b = bytes(watermarks_hmac_key)

    entry_fields = {
        "event_kind": event_kind,
        "seat": seat,
        "reason_code": reason_code,
        "duration_seconds": duration_seconds,
        "authorization_id": authorization_id,
        "expires_at": expires_at,
        "expires_monotonic_ns": expires_monotonic_ns,
        "boot_epoch_ns_at_issuance": boot_epoch_ns_at_issuance,
        "signed_by_operator": signed_by_operator,
    }

    append_to_ledger(
        _ledger_path(repo_root),
        entry_fields,
        ledger_name="degradation",
        hmac_key=hmac_key_b,
        lock_path=_lock_path(repo_root),
        trailer_path=_trailer_path(repo_root),
        watermarks_path=_watermarks_path(repo_root),
        watermarks_hmac_key=watermarks_hmac_key_b,
        watermarks_hmac_path=_watermarks_hmac_path(repo_root),
        watermarks_lock_path=_watermarks_lock_path(repo_root),
    )

    tail = read_degradation_tail(repo_root=repo_root, n=1)
    if not tail:
        raise LedgerChainBroken(
            "degradation ledger: append succeeded but tail read returned empty"
        )
    return tail[-1]


# ---------------------------------------------------------------------------
# Public API — read_degradation_tail
# ---------------------------------------------------------------------------


def _event_from_json(line_bytes: bytes) -> DegradationEvent:
    obj = json.loads(line_bytes.decode("utf-8"))
    return DegradationEvent(
        seq_id=int(obj["seq_id"]),
        timestamp_utc=str(obj["timestamp_utc"]),
        issued_monotonic_ns=int(obj["issued_monotonic_ns"]),
        event_kind=str(obj["event_kind"]),
        seat=str(obj["seat"]),
        reason_code=str(obj["reason_code"]),
        duration_seconds=obj.get("duration_seconds"),
        authorization_id=obj.get("authorization_id"),
        expires_at=obj.get("expires_at"),
        expires_monotonic_ns=obj.get("expires_monotonic_ns"),
        boot_epoch_ns_at_issuance=obj.get("boot_epoch_ns_at_issuance"),
        signed_by_operator=bool(obj["signed_by_operator"]),
        prev_hash=str(obj["prev_hash"]),
        entry_hash=str(obj["entry_hash"]),
    )


def read_degradation_tail(
    *, repo_root: Path, n: int = 50
) -> list[DegradationEvent]:
    """Return the last ``n`` events in ledger order (oldest → newest).

    :raises TypeError / ValueError: bad args.
    :raises LedgerUnreadable: JSON parse failure mid-scan.
    """
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n <= 0:
        raise ValueError("n must be positive")

    ledger_path = _ledger_path(repo_root)
    if not ledger_path.is_file():
        return []
    lines: list[bytes] = []
    try:
        with open(ledger_path, "rb") as fh:
            for raw_line in fh:
                stripped = raw_line.strip()
                if stripped:
                    lines.append(stripped)
    except OSError as exc:
        raise LedgerUnreadable(path=ledger_path, reason=str(exc)) from exc
    tail = lines[-n:]
    return [_event_from_json(line) for line in tail]


# ---------------------------------------------------------------------------
# Public API — verify_chain
# ---------------------------------------------------------------------------


def verify_chain(
    *,
    repo_root: Path,
    hmac_key: bytes,
) -> LedgerTrailer:
    """Verify ``degradation.jsonl`` chain + HMAC trailer. [§7.3 BT8 row]

    Delegates to :func:`audit.verify_ledger`, which walks the full chain
    and cross-checks both the trailer HMAC and the ledger-body HMAC.

    A fast-tail variant (blueprint §5.6 ``fast=True``) is deferred to
    Round J Section 1 capstone.

    :raises TypeError: bad args (E-001).
    :raises LedgerUnreadable / LedgerChainBroken / LedgerHMACTrailerMismatch:
        on any chain corruption.
    """
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(hmac_key, (bytes, bytearray)):
        raise TypeError("hmac_key must be bytes")

    return verify_ledger(
        _ledger_path(repo_root),
        trailer_path=_trailer_path(repo_root),
        hmac_key=bytes(hmac_key),
    )
