"""M8 admin-risk-ledger PRE-gate verifier. [§4.7 + §4.2.1 row #10]

Logician-side counterpart to :mod:`pipeline.sovereignty.admin_risk` (the
writer locked in Round F). The Round F module assembles, signs, and
atomically appends ledger entries; this module **verifies** the on-disk
result at PRE-gate check #10 and exposes scan helpers for the POST-gate.

The verifier delegates the heavy chain-walk to
:func:`pipeline.sovereignty.audit.verify_ledger` (which already enforces
strict monotonic ``seq_id``, hash-chain continuity, ledger-body HMAC, and
trailer-over-trailer HMAC). Round 1's job is to translate the audit-layer
exceptions into structured §4.7.3 sub-tags so the rails report can render
``F-PRE-10.<sub_tag>`` consistently.

Severity / entry-kind taxonomy
==============================

The blueprint (§4.7.2) speaks in display terms — HARD_BLOCK / MEMOED /
PRECAUTIONARY / HIGH / INFO and FLAG_TERM / SUBSTITUTION_DECISION / etc.
The locked Round F writer uses GREEN / YELLOW / RED and entry kinds
``flagged_term_substitution`` / ``review_seat_bypass``. The mapping is:

* RED   → HARD_BLOCK    → 🔴
* YELLOW → MEMOED       → 🟡
* GREEN  → PRECAUTIONARY → 🟢

Since the writer is the source of truth (the ledger on disk is what it
wrote), the Logician verifier reads the writer's vocabulary and exposes a
display-side classifier so POST-gate / rails-report code can render the
emoji + display label without scattering string literals.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

from pipeline.sovereignty import (
    AdminRiskEntry,
    LedgerChainBroken,
    LedgerHMACTrailerMismatch,
    LedgerUnreadable,
    admin_risk_entry_from_json as _entry_from_json,
    admin_risk_ledger_path as _ledger_path,
    admin_risk_trailer_path as _trailer_path,
    verify_ledger,
)


# ---------------------------------------------------------------------------
# Failure-code constants (§4.7.3)
# ---------------------------------------------------------------------------


F_PRE_10: str = "F-PRE-10"

_SUB_TAG_UNREADABLE = "admin_risk_unreadable"
_SUB_TAG_CHAIN_BREAK = "admin_risk_chain_break"
_SUB_TAG_TRAILER_TAMPER = "admin_risk_trailer_tamper"
_SUB_TAG_NON_MONOTONIC = "admin_risk_non_monotonic"
_SUB_TAG_REPLAYED_SEQ_ID = "admin_risk_replayed_seq_id"
_SUB_TAG_WATERMARK_REGRESSION = "admin_risk_watermark_regression"


_VALID_SUB_TAGS = frozenset(
    {
        _SUB_TAG_UNREADABLE,
        _SUB_TAG_CHAIN_BREAK,
        _SUB_TAG_TRAILER_TAMPER,
        _SUB_TAG_NON_MONOTONIC,
        _SUB_TAG_REPLAYED_SEQ_ID,
        _SUB_TAG_WATERMARK_REGRESSION,
    }
)


# ---------------------------------------------------------------------------
# Severity / entry-kind classification tables (§4.7.2)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SeverityClassification:
    severity: str            # writer vocab: GREEN / YELLOW / RED
    display_label: str       # blueprint vocab: PRECAUTIONARY / MEMOED / HARD_BLOCK
    emoji: str               # 🟢 / 🟡 / 🔴
    is_hard_block: bool


_SEVERITY_TABLE: dict[str, SeverityClassification] = {
    "GREEN": SeverityClassification(
        severity="GREEN",
        display_label="PRECAUTIONARY",
        emoji="\U0001f7e2",  # 🟢
        is_hard_block=False,
    ),
    "YELLOW": SeverityClassification(
        severity="YELLOW",
        display_label="MEMOED",
        emoji="\U0001f7e1",  # 🟡
        is_hard_block=False,
    ),
    "RED": SeverityClassification(
        severity="RED",
        display_label="HARD_BLOCK",
        emoji="\U0001f534",  # 🔴
        is_hard_block=True,
    ),
}


def classify_severity(severity: str) -> SeverityClassification:
    """Return the §4.7.2 classification for a writer-vocab severity string.

    :raises TypeError: ``severity`` is not a str.
    :raises ValueError: ``severity`` is not GREEN / YELLOW / RED.
    """
    if not isinstance(severity, str):
        raise TypeError(
            f"severity must be str, got {type(severity).__name__}"
        )
    try:
        return _SEVERITY_TABLE[severity]
    except KeyError as exc:
        raise ValueError(
            f"unknown severity {severity!r}; valid: "
            f"{sorted(_SEVERITY_TABLE)}"
        ) from exc


@dataclass(frozen=True, kw_only=True)
class EntryKindMeta:
    entry_kind: str
    requires_operator_signature: bool
    requires_retype_confirmation: bool


_ENTRY_KIND_TABLE: dict[str, EntryKindMeta] = {
    "flagged_term_substitution": EntryKindMeta(
        entry_kind="flagged_term_substitution",
        requires_operator_signature=False,
        requires_retype_confirmation=False,
    ),
    "review_seat_bypass": EntryKindMeta(
        entry_kind="review_seat_bypass",
        requires_operator_signature=True,
        requires_retype_confirmation=True,
    ),
}


def entry_kind_meta(entry_kind: str) -> EntryKindMeta:
    """Return the per-entry-kind §4.7.2 metadata.

    :raises TypeError: ``entry_kind`` is not a str.
    :raises ValueError: ``entry_kind`` is unknown.
    """
    if not isinstance(entry_kind, str):
        raise TypeError(
            f"entry_kind must be str, got {type(entry_kind).__name__}"
        )
    try:
        return _ENTRY_KIND_TABLE[entry_kind]
    except KeyError as exc:
        raise ValueError(
            f"unknown entry_kind {entry_kind!r}; valid: "
            f"{sorted(_ENTRY_KIND_TABLE)}"
        ) from exc


# ---------------------------------------------------------------------------
# Result + exception
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class MonotonicityResult:
    ok: bool
    tail_seq_id: int
    tail_entry_hash: str
    entries_count: int


class AdminRiskMonotonicityFailed(RuntimeError):
    """PRE-gate check #10 failure. Carries §4.7.3 sub-tag.

    ``code`` is always ``F-PRE-10``; ``sub_tag`` is one of the six §4.7.3
    sub-tags; ``full_code`` is the dotted concatenation rails reports
    surface to the operator.
    """

    code: str = F_PRE_10

    def __init__(self, message: str, *, sub_tag: str) -> None:
        super().__init__(message)
        if sub_tag not in _VALID_SUB_TAGS:
            raise ValueError(
                f"sub_tag {sub_tag!r} not in {sorted(_VALID_SUB_TAGS)}"
            )
        self.sub_tag: str = sub_tag

    @property
    def full_code(self) -> str:
        return f"{self.code}.{self.sub_tag}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _classify_chain_break_reason(reason: str) -> str:
    """Map an audit-layer ``LedgerChainBroken.reason`` to a §4.7.3 sub-tag."""
    if reason.startswith("seq_id_non_monotonic"):
        return _SUB_TAG_NON_MONOTONIC
    if reason in {"prev_hash_mismatch", "entry_hash_mismatch"}:
        return _SUB_TAG_CHAIN_BREAK
    if reason.startswith("trailer_seq_mismatch") or reason == "trailer_last_hash_mismatch":
        return _SUB_TAG_CHAIN_BREAK
    if reason.startswith("missing_field"):
        return _SUB_TAG_CHAIN_BREAK
    return _SUB_TAG_CHAIN_BREAK


def _detect_replayed_seq_id(ledger_path: Path) -> bool:
    """Second-pass duplicate-seq scan. Audit's forward walk catches the
    duplicate as ``seq_id_non_monotonic`` (next entry's seq != last+1) but a
    targeted scan lets the verifier promote the sub-tag from
    ``non_monotonic`` to the more specific ``replayed_seq_id`` when a true
    duplicate is observed.
    """
    if not ledger_path.is_file():
        return False
    seen: set[int] = set()
    try:
        with open(ledger_path, "rb") as fh:
            for raw_line in fh:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    entry = _entry_from_json(line)
                except Exception:
                    return False
                if entry.seq_id in seen:
                    return True
                seen.add(entry.seq_id)
    except OSError:
        return False
    return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def verify_admin_risk_ledger(
    *,
    repo_root: Path,
    hmac_key: bytes,
) -> MonotonicityResult:
    """§4.2.1 row #10 — verify the admin-risk ledger at PRE-gate.

    Walks the ledger from genesis forward (via
    :func:`pipeline.sovereignty.audit.verify_ledger`), enforcing:

    * Trailer-over-trailer HMAC integrity.
    * Ledger-body HMAC integrity.
    * Strict-monotonic ``seq_id`` (no skips, no duplicates).
    * Hash-chain continuity (``prev_hash`` == previous ``entry_hash``).
    * Recomputed ``entry_hash`` matches the stored value.

    On failure, raises :class:`AdminRiskMonotonicityFailed` with the §4.7.3
    sub-tag the rails report should surface.

    :raises AdminRiskMonotonicityFailed: PRE-gate check #10 fails.
    :raises TypeError: bad arg types.
    """
    if not isinstance(repo_root, Path):
        raise TypeError(
            f"repo_root must be pathlib.Path, got {type(repo_root).__name__}"
        )
    if not isinstance(hmac_key, (bytes, bytearray)):
        raise TypeError(
            f"hmac_key must be bytes, got {type(hmac_key).__name__}"
        )

    ledger_path = _ledger_path(repo_root)
    trailer_path = _trailer_path(repo_root)

    if not ledger_path.is_file() or not trailer_path.is_file():
        raise AdminRiskMonotonicityFailed(
            f"admin-risk ledger missing under {repo_root}",
            sub_tag=_SUB_TAG_UNREADABLE,
        )

    try:
        trailer = verify_ledger(
            ledger_path, trailer_path, hmac_key=bytes(hmac_key)
        )
    except LedgerHMACTrailerMismatch as exc:
        raise AdminRiskMonotonicityFailed(
            f"admin-risk ledger trailer tamper: {exc.reason}",
            sub_tag=_SUB_TAG_TRAILER_TAMPER,
        ) from exc
    except LedgerChainBroken as exc:
        sub_tag = _classify_chain_break_reason(exc.reason)
        if sub_tag == _SUB_TAG_NON_MONOTONIC and _detect_replayed_seq_id(
            ledger_path
        ):
            sub_tag = _SUB_TAG_REPLAYED_SEQ_ID
        raise AdminRiskMonotonicityFailed(
            f"admin-risk ledger chain broken: {exc.reason}",
            sub_tag=sub_tag,
        ) from exc
    except LedgerUnreadable as exc:
        raise AdminRiskMonotonicityFailed(
            f"admin-risk ledger unreadable: {exc.reason}",
            sub_tag=_SUB_TAG_UNREADABLE,
        ) from exc

    # Audit's verify_ledger only counts the tail; for entries_count, do a
    # cheap line scan. The ledger has already been HMAC-verified so reading
    # it again is safe (and cached by the OS).
    entries_count = 0
    with open(ledger_path, "rb") as fh:
        for raw_line in fh:
            if raw_line.strip():
                entries_count += 1

    return MonotonicityResult(
        ok=True,
        tail_seq_id=trailer.last_seq_id,
        tail_entry_hash=trailer.last_entry_hash,
        entries_count=entries_count,
    )


def iter_admin_risk_entries(*, repo_root: Path) -> Iterator[AdminRiskEntry]:
    """Non-verifying scan helper for POST-gate / rails-report use.

    Yields entries in on-disk (insertion) order. Caller is expected to have
    already verified the ledger via :func:`verify_admin_risk_ledger` at
    PRE-gate; this helper is for scan-and-classify workloads.
    """
    if not isinstance(repo_root, Path):
        raise TypeError(
            f"repo_root must be pathlib.Path, got {type(repo_root).__name__}"
        )
    ledger_path = _ledger_path(repo_root)
    if not ledger_path.is_file():
        return
    with open(ledger_path, "rb") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line:
                continue
            yield _entry_from_json(line)


def count_unresolved_hard_blocks(entries: Iterable[AdminRiskEntry]) -> int:
    """Count RED-severity entries — POST-gate convenience for §4.4.1 step 4."""
    if not isinstance(entries, (list, tuple)) and not hasattr(entries, "__iter__"):
        raise TypeError("entries must be iterable of AdminRiskEntry")
    materialized = list(entries)
    for e in materialized:
        if not isinstance(e, AdminRiskEntry):
            raise TypeError(
                f"entries must yield AdminRiskEntry, got {type(e).__name__}"
            )
    return sum(1 for e in materialized if e.severity == "RED")


__all__ = [
    "F_PRE_10",
    "AdminRiskMonotonicityFailed",
    "EntryKindMeta",
    "MonotonicityResult",
    "SeverityClassification",
    "classify_severity",
    "count_unresolved_hard_blocks",
    "entry_kind_meta",
    "iter_admin_risk_entries",
    "verify_admin_risk_ledger",
]
