"""§14 Report Generator — SN-LLC first-wave marker hash binding (RT-C2-04 closure).

Per §14 v1 LOCKED 2026-05-10 §14.9.5 + WS-J Slice 3 handoff (2026-05-11).

The SN-LLC "first-wave" funder marker is a signed manifest file at
``vault_shared/funder_intelligence/<funder_id>/sn_llc_first_wave.signed.yaml``
that announces "SN-LLC publishes a curated reporting template for this
funder at the v0.2 first wave". Per §14.9.5, missing-or-tampered markers
for first-wave funders FAIL-CLOSED at PRE-pre-track-dispatch.

**Three-way binding** (RT-C2-04 closure):

1. The marker file itself carries an Ed25519 signature over the marker
   content under the SN-LLC publisher key. Tampering with the marker
   text invalidates the signature.
2. The marker content includes the SHA3-512 of the published
   reporting-template at the SN-LLC release ceremony. Operator clients
   re-hash the on-disk published template and compare against the
   marker's recorded hash — drift detection.
3. The marker hash itself is recorded in a workspace-wide immutable
   ledger ``lock_history/first_wave_markers.signed.yaml``. The ledger
   is signed by SN-LLC at release ceremony; the operator client
   verifies the ledger signature at every read AND looks up the
   funder's marker-hash from the ledger to confirm the on-disk marker
   matches the lock-history-bound hash.

A funder is "first-wave" iff its ``funder_id`` appears in the
:data:`FIRST_WAVE_FUNDER_IDS` set — VAPG / NIFA / SARE / EPA NEETP /
SBIR per §14.9.5 closure.

The lock_history file is **operator-deployment-empty by default**.
SN-LLC populates it via signed release ceremony; until then the
verifier's ``hash_bound_to_lock_history`` field returns False (and
the gate routes through ``.workspace_published_template_marker_tampered``).
This module never writes the lock-history file; it is read-only.

Substrate I/O is performed BY THE CALLER (the report_mode track runner
PRE-pre-track-dispatch consolidated check). Injected ``MarkerReader`` +
``LockHistoryReader`` + ``SignatureVerifier`` protocols return
pre-parsed dicts. This module is zero-token, fail-closed, and never
calls ``open()`` or imports a crypto library.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping, Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Closed set of first-wave funder IDs per §14.9.5 closure
# ---------------------------------------------------------------------------


FIRST_WAVE_FUNDER_IDS: Final[frozenset[str]] = frozenset(
    {
        "VAPG",
        "NIFA",
        "SARE",
        "EPA_NEETP",
        "SBIR",
    }
)
assert len(FIRST_WAVE_FUNDER_IDS) == 5, (
    "FIRST_WAVE_FUNDER_IDS has been rebound at module load; refusing to "
    "load pipeline.logician.first_wave_marker — §14.9.5 closure fixes the "
    "set at exactly 5 funders for v0.2 first wave"
)


# ---------------------------------------------------------------------------
# Injected protocols (zero-token Logician discipline — caller does I/O)
# ---------------------------------------------------------------------------


@runtime_checkable
class MarkerReader(Protocol):
    """Reads the per-funder ``sn_llc_first_wave.signed.yaml`` marker file.

    ``__call__(funder_id) -> dict | None`` returns the parsed marker
    dict (with keys ``funder_id``, ``marker_content_sha3_512``,
    ``published_at_utc``, ``signature``) when the marker file exists
    AND parses successfully, otherwise ``None``.

    Marker dict shape (caller normalizes):

    * ``funder_id``: str  — must equal the lookup ``funder_id``
    * ``marker_content_sha3_512``: str  — 128-hex of the marker file's
      canonical content (the same bytes the signature covers)
    * ``signature``: bytes  — Ed25519 signature over the marker content
      bytes
    * ``signed_bytes``: bytes  — the exact byte stream the signature
      covers (caller provides — typically the file content with the
      signature field excluded, canonicalized)
    """

    def __call__(self, funder_id: str) -> Optional[Mapping[str, object]]: ...


@runtime_checkable
class LockHistoryReader(Protocol):
    """Reads the workspace ``lock_history/first_wave_markers.signed.yaml`` ledger.

    ``__call__() -> dict | None`` returns the parsed lock-history dict
    when the ledger file exists AND parses successfully, otherwise
    ``None`` (operator-deployment-empty default).

    Lock-history dict shape (caller normalizes):

    * ``schema_version``: str  — pinned ``"first_wave_markers.v1"``
    * ``signed_at_utc``: str
    * ``signature``: bytes  — Ed25519 over the canonical-JSON of the
      remaining fields (caller pre-computes ``signed_bytes`` for verify)
    * ``signed_bytes``: bytes  — what the ``signature`` covers
    * ``entries``: dict[str, dict]  — funder_id → {"marker_content_sha3_512": ...,
      "released_at_utc": ...}
    """

    def __call__(self) -> Optional[Mapping[str, object]]: ...


@runtime_checkable
class SignatureVerifier(Protocol):
    """Ed25519 verifier callable.

    ``__call__(message_bytes, signature, public_key) -> True | False``.

    Strict ``is True`` identity is applied by the gate caller — any
    truthy non-True return is treated as failure (mirrors §4 v2.x
    F-AMDT-05 / F-CLASS-REGISTER-SIGNATURE-INVALID + claim_evidence_map
    verify precedent).
    """

    def __call__(
        self,
        message_bytes: bytes,
        signature: bytes,
        public_key: bytes,
    ) -> bool: ...


# ---------------------------------------------------------------------------
# Verdict dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class FirstWaveMarkerVerdict:
    """Per §14.9.5 outcome of the first-wave marker hash-binding check.

    Three independent booleans:

    * ``present`` — marker file readable + parsed; ``funder_id`` field
      matches the looked-up funder.
    * ``signature_valid`` — marker file's Ed25519 signature verifies
      against the pinned SN-LLC publisher public key (strict identity).
    * ``hash_bound_to_lock_history`` — marker's
      ``marker_content_sha3_512`` exists in
      ``lock_history/first_wave_markers.signed.yaml`` under the same
      funder_id AND the lock-history ledger signature itself verifies
      against the pinned SN-LLC publisher public key.

    A first-wave funder requires ALL THREE to be ``True`` before the
    workspace-published template will be trusted; otherwise the
    F-REPORT-TEMPLATE-MISMATCH gate fires
    ``.workspace_published_template_marker_tampered``.

    ``detail`` carries the human-readable rationale (audit-log
    contribution).
    """

    funder_id: str
    is_first_wave: bool
    present: bool
    signature_valid: bool
    hash_bound_to_lock_history: bool
    detail: str = ""


def is_first_wave_funder(funder_id: str) -> bool:
    """Return True iff ``funder_id`` is in :data:`FIRST_WAVE_FUNDER_IDS`."""
    return funder_id in FIRST_WAVE_FUNDER_IDS


def verify_first_wave_marker(
    funder_id: str,
    *,
    marker_reader: MarkerReader,
    lock_history_reader: LockHistoryReader,
    signature_verifier: SignatureVerifier,
    sn_llc_public_key: bytes,
) -> FirstWaveMarkerVerdict:
    """Per RT-C2-04 — verify the three-way marker integrity.

    Returns :class:`FirstWaveMarkerVerdict`. Strict ``is True`` identity
    on every signature-verify return value; any failure leaves the
    relevant boolean False with detail populated.

    The function never raises on missing inputs (it is a verifier, not
    a precondition) — any None return from the readers surfaces as
    ``present=False`` / ``hash_bound_to_lock_history=False`` with
    detail set.

    For non-first-wave funders, the verdict carries
    ``is_first_wave=False`` and all three booleans set per the same
    rules — the gate caller then decides via §14.9.5 whether the
    funder being non-first-wave downgrades the missing-marker case
    from FAIL-CLOSED to ADVISORY (the gate's responsibility, not this
    module's).
    """
    if not isinstance(funder_id, str) or not funder_id:
        return FirstWaveMarkerVerdict(
            funder_id=str(funder_id),
            is_first_wave=False,
            present=False,
            signature_valid=False,
            hash_bound_to_lock_history=False,
            detail="funder_id must be a non-empty string",
        )

    is_first_wave = is_first_wave_funder(funder_id)

    # 1. Read marker file
    try:
        marker = marker_reader(funder_id)
    except Exception as exc:  # pragma: no cover - exception body unimportant
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=False,
            signature_valid=False,
            hash_bound_to_lock_history=False,
            detail=f"marker_reader raised {type(exc).__name__}: {exc!s}",
        )
    if marker is None:
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=False,
            signature_valid=False,
            hash_bound_to_lock_history=False,
            detail=f"sn_llc_first_wave.signed.yaml not found for funder {funder_id!r}",
        )

    # Validate marker shape
    marker_funder_id = marker.get("funder_id")
    if marker_funder_id != funder_id:
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=False,
            signature_valid=False,
            hash_bound_to_lock_history=False,
            detail=(
                f"marker funder_id={marker_funder_id!r} != lookup "
                f"funder_id={funder_id!r}; tampered or mis-published"
            ),
        )
    marker_content_hash = marker.get("marker_content_sha3_512")
    if not isinstance(marker_content_hash, str) or len(marker_content_hash) != 128:
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=False,
            hash_bound_to_lock_history=False,
            detail=(
                f"marker_content_sha3_512 malformed: "
                f"{marker_content_hash!r}"
            ),
        )
    signature = marker.get("signature")
    signed_bytes = marker.get("signed_bytes")
    if not isinstance(signature, (bytes, bytearray)) or not isinstance(
        signed_bytes, (bytes, bytearray)
    ):
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=False,
            hash_bound_to_lock_history=False,
            detail=(
                "marker.signature and marker.signed_bytes must both be bytes"
            ),
        )

    # 2. Verify marker signature
    try:
        sig_ok = signature_verifier(
            bytes(signed_bytes), bytes(signature), sn_llc_public_key
        )
    except Exception as exc:  # pragma: no cover
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=False,
            hash_bound_to_lock_history=False,
            detail=(
                f"signature_verifier raised on marker: "
                f"{type(exc).__name__}: {exc!s}"
            ),
        )
    signature_valid = sig_ok is True
    if not signature_valid:
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=False,
            hash_bound_to_lock_history=False,
            detail=(
                f"marker signature did not verify against SN-LLC publisher "
                f"key (verifier returned {sig_ok!r}; strict is-True required)"
            ),
        )

    # 3. Look up in lock_history + verify the ledger signature
    try:
        ledger = lock_history_reader()
    except Exception as exc:  # pragma: no cover
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=True,
            hash_bound_to_lock_history=False,
            detail=(
                f"lock_history_reader raised: "
                f"{type(exc).__name__}: {exc!s}"
            ),
        )
    if ledger is None:
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=True,
            hash_bound_to_lock_history=False,
            detail=(
                "lock_history/first_wave_markers.signed.yaml is "
                "operator-deployment-empty (SN-LLC release ceremony not yet "
                "applied)"
            ),
        )

    ledger_signature = ledger.get("signature")
    ledger_signed_bytes = ledger.get("signed_bytes")
    if not isinstance(ledger_signature, (bytes, bytearray)) or not isinstance(
        ledger_signed_bytes, (bytes, bytearray)
    ):
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=True,
            hash_bound_to_lock_history=False,
            detail=(
                "lock_history ledger missing signature or signed_bytes"
            ),
        )

    try:
        ledger_sig_ok = signature_verifier(
            bytes(ledger_signed_bytes),
            bytes(ledger_signature),
            sn_llc_public_key,
        )
    except Exception as exc:  # pragma: no cover
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=True,
            hash_bound_to_lock_history=False,
            detail=(
                f"signature_verifier raised on lock_history: "
                f"{type(exc).__name__}: {exc!s}"
            ),
        )
    if ledger_sig_ok is not True:
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=True,
            hash_bound_to_lock_history=False,
            detail=(
                f"lock_history ledger signature did not verify "
                f"(verifier returned {ledger_sig_ok!r}; strict is-True required)"
            ),
        )

    entries = ledger.get("entries")
    if not isinstance(entries, Mapping):
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=True,
            hash_bound_to_lock_history=False,
            detail="lock_history ledger 'entries' missing or non-mapping",
        )

    entry = entries.get(funder_id)
    if not isinstance(entry, Mapping):
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=True,
            hash_bound_to_lock_history=False,
            detail=(
                f"no lock_history entry for funder_id={funder_id!r}; marker "
                f"not bound to immutable ledger"
            ),
        )
    bound_hash = entry.get("marker_content_sha3_512")
    if bound_hash != marker_content_hash:
        return FirstWaveMarkerVerdict(
            funder_id=funder_id,
            is_first_wave=is_first_wave,
            present=True,
            signature_valid=True,
            hash_bound_to_lock_history=False,
            detail=(
                f"lock_history-bound hash={str(bound_hash)[:16]}… != marker "
                f"hash={marker_content_hash[:16]}…; tamper detected"
            ),
        )

    return FirstWaveMarkerVerdict(
        funder_id=funder_id,
        is_first_wave=is_first_wave,
        present=True,
        signature_valid=True,
        hash_bound_to_lock_history=True,
        detail=(
            f"marker present + signature valid + hash bound to lock_history "
            f"({marker_content_hash[:16]}…)"
        ),
    )


__all__ = [
    "FIRST_WAVE_FUNDER_IDS",
    "FirstWaveMarkerVerdict",
    "LockHistoryReader",
    "MarkerReader",
    "SignatureVerifier",
    "is_first_wave_funder",
    "verify_first_wave_marker",
]
