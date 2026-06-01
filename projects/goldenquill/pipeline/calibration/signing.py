"""pipeline.calibration.signing — §4.15 step 10 Ed25519 sign/verify.

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.15 step 10 sign_report + verify_calibration_report
- §4.15 step 10 v5 operator-pubkey first-write-wins provenance (MA-09)
- §4.15 step 10 v5 verify-time freshness-window check (MB-06) — 90-day default
- §6 F-PIPE-21 sub-trigger ``calibration_signature_stale``
- §8 CALIBRATION_KEY_PATH_TMPL + MAX_CALIBRATION_AGE_DAYS + CALIBRATION_SIGNING_ALGORITHM

**BT13-style detached Ed25519.** The signature covers exactly the canonical
bytes produced by ``pipeline.calibration.report.canonical_bytes`` (the ONE
field excluded is ``CalibrationReport.signature`` itself; ``canonical_sha256``
is also excluded because it stores the hash OF the canonical bytes).

**Pubkey location + first-write-wins provenance (v5 MA-09 closure).**
The operator's Ed25519 verification public key lives at
``vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519`` — an
inline-literal path template at every call site. The pubkey is written
exactly once per operator via a ``state-success`` write-if-absent primitive
on first sign-off; subsequent sign-offs compare the fresh pubkey against
the on-disk pubkey and REJECT any divergence (rotation requires an explicit
``key-rotation-write`` intent, deferred to v0.2). A provenance sidecar at
``vault/{operator_org_slug}/calibration/keys/pubkey_first_write_provenance.json``
records the ULID + ISO-time of the first write.

**Verify-time freshness check (v5 MB-06 closure).** ``verify_calibration_report``
asserts ``(now - report.signed_at_iso) < timedelta(days=MAX_CALIBRATION_AGE_DAYS)``
BEFORE validating the Ed25519 signature. Stale signatures raise
``F-PIPE-21.calibration_signature_stale``. Default window: 90 days.

**V1 discipline.** Inline-literal RHS: the key-path template is re-built at
every call site; the 90-day freshness window is re-checked against the
inline literal; the ``"Ed25519"`` algorithm tag is compared as an inline
literal.

**E-017 Protocol seams.** All vault I/O + all clock reads are injected.
The ``cryptography`` dependency is the only runtime third-party binding;
tests may inject a ``CalibrationSignerProtocol`` fake to exercise signing
logic without real Ed25519 compute.

Spec card: ``pipeline/engineering/spec_cards/section_05_round_12_run_eval_pipeline.md``
(R12.A split).
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Final, Protocol, runtime_checkable

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from pipeline.calibration.report import CalibrationReport, canonical_bytes
from pipeline.loop.config import (
    CALIBRATION_SIGNING_ALGORITHM,
    MAX_CALIBRATION_AGE_DAYS,
)
from pipeline.loop.errors import F_PIPE_21

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.15 step 10 sign_report (Ed25519 detached)",
            "§4.15 step 10 verify_calibration_report (freshness + signature)",
            "§4.15 step 10 v5 first-write-wins operator pubkey + provenance",
            "§6 F-PIPE-21.calibration_signature_stale",
            "§8 CALIBRATION_KEY_PATH_TMPL + MAX_CALIBRATION_AGE_DAYS",
        ],
    },
}

# ---------------------------------------------------------------------------
# Module-load integrity asserts (V1 discipline)
# ---------------------------------------------------------------------------

# Defence-in-depth: the imported constants must still equal their blueprint-
# declared values at import of this module.
assert CALIBRATION_SIGNING_ALGORITHM == "Ed25519", (
    "pipeline.loop.config.CALIBRATION_SIGNING_ALGORITHM has been rebound "
    "before pipeline.calibration.signing import; refusing to load"
)
assert MAX_CALIBRATION_AGE_DAYS == 90, (
    "pipeline.loop.config.MAX_CALIBRATION_AGE_DAYS has been rebound "
    "before pipeline.calibration.signing import; refusing to load"
)

# Inline-literal path templates — the blueprint's §8 v5 row is
# ``vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519`` —
# kept in this module as inline literals (not exported by config.py in v6).
# Any future relocation to config.py would add paired module-load asserts.
CALIBRATION_KEY_PATH_TMPL: Final[str] = (
    "vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519"
)
assert (
    CALIBRATION_KEY_PATH_TMPL
    == "vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519"
), (
    "CALIBRATION_KEY_PATH_TMPL has been rebound at module load; "
    "refusing to load pipeline.calibration.signing"
)

CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL: Final[str] = (
    "vault/{operator_org_slug}/calibration/keys/"
    "pubkey_first_write_provenance.json"
)
assert CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL == (
    "vault/{operator_org_slug}/calibration/keys/"
    "pubkey_first_write_provenance.json"
), (
    "CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL has been rebound at module load; "
    "refusing to load pipeline.calibration.signing"
)


# ---------------------------------------------------------------------------
# Protocol seams (E-017)
# ---------------------------------------------------------------------------


@runtime_checkable
class CalibrationSignerProtocol(Protocol):
    """Produces a detached Ed25519 signature over given canonical bytes.

    Production wiring holds the operator's Ed25519 private key (HSM or
    file-backed). Test wiring may use a deterministic in-memory key.
    The protocol exists so ``sign_report`` never directly handles the
    private key material.
    """

    def sign(self, canonical_bytes_: bytes) -> bytes: ...

    def public_key_bytes(self) -> bytes:
        """Return the 32-byte raw Ed25519 public key (for pubkey provenance)."""
        ...


@runtime_checkable
class PubkeyVaultReader(Protocol):
    """Reads the operator's stored public key bytes, if any.

    Returns ``None`` if no pubkey is stored yet (first-write case).
    On any other failure (transient vault error) raises to the caller
    unchanged — the signing path aborts to state-failure.
    """

    def __call__(self, *, operator_org_slug: str) -> bytes | None: ...


@runtime_checkable
class PubkeyVaultWriter(Protocol):
    """Writes the operator's public key bytes + paired provenance sidecar.

    Production wiring routes through ``vault_write(intent="state-success",
    write_mode="write-if-absent")``. The callable accepts the pubkey bytes +
    provenance JSON bytes and returns the ``(pubkey_ref, provenance_ref)``
    pair (commit hashes or vault-relative paths — opaque to this module).
    """

    def __call__(
        self,
        *,
        operator_org_slug: str,
        pubkey_bytes: bytes,
        provenance_bytes: bytes,
    ) -> tuple[str, str]: ...


@runtime_checkable
class ClockNowUTC(Protocol):
    """Injected UTC-aware ``now`` — lets tests pin freshness-check timing.

    Production wiring passes ``datetime.now(timezone.utc)``. The protocol
    is a zero-arg callable returning a ``datetime`` that MUST be
    timezone-aware (verify asserts).
    """

    def __call__(self) -> datetime: ...


# ---------------------------------------------------------------------------
# §4.15 step 10 — sign_report
# ---------------------------------------------------------------------------


def sign_report(
    report: CalibrationReport,
    *,
    signer: CalibrationSignerProtocol,
    signed_at_iso: str,
) -> CalibrationReport:
    """§4.15 step 10 — detach-sign a ``CalibrationReport``.

    Computes canonical bytes (``pipeline.calibration.report.canonical_bytes``),
    asks the injected ``signer`` to produce a detached signature, and returns
    a new frozen ``CalibrationReport`` with ``signature`` + ``signed_at_iso``
    populated. The signer never handles the report structure directly — only
    the pre-computed canonical bytes.

    The returned report's ``canonical_sha256`` is the sha256 of the SIGNED
    variant's canonical bytes (i.e., with ``signed_at_iso`` populated).
    ``signed_at_iso`` IS canonical-included, so populating it changes canonical
    bytes — the signer covers those NEW bytes, and ``canonical_sha256`` must
    mirror them so ``verify_calibration_report``'s recomputation step matches.
    (``signature`` and ``canonical_sha256`` themselves remain excluded from
    canonical bytes; a self-referential hash would be circular.)

    :raises ValueError: on empty ``signed_at_iso`` or already-signed report.
    """
    if not isinstance(signed_at_iso, str):
        raise TypeError(
            f"signed_at_iso must be str; got {type(signed_at_iso).__name__}"
        )
    if not signed_at_iso:
        raise ValueError("signed_at_iso must be non-empty")
    if report.signature is not None:
        raise ValueError(
            "CalibrationReport is already signed; refusing to re-sign "
            "(rotation deferred to v0.2 key-rotation-write intent)"
        )

    import hashlib as _hashlib

    # Build an intermediate with signed_at_iso populated so canonical bytes
    # reflect the final signed-variant layout. ``signature`` is excluded from
    # canonical bytes (§5.6.4), so we stage a 64-byte placeholder here only to
    # satisfy the dataclass's both-None-or-both-set invariant — the placeholder
    # never appears in the bytes we hash or sign. ``canonical_sha256`` is also
    # excluded; we seed it empty and overwrite with the real digest below.
    intermediate = CalibrationReport(
        schema_version=1,
        run_id=report.run_id,
        operator_org_slug=report.operator_org_slug,
        golden_set_manifest_path=report.golden_set_manifest_path,
        golden_set_manifest_hash=report.golden_set_manifest_hash,
        items=report.items,
        summary_judge_mean=report.summary_judge_mean,
        summary_judge_stddev=report.summary_judge_stddev,
        summary_per_dimension_mean=report.summary_per_dimension_mean,
        council_charter_snapshot_hash=report.council_charter_snapshot_hash,
        router_yaml_snapshot_hash=report.router_yaml_snapshot_hash,
        assembled_at_iso=report.assembled_at_iso,
        canonical_sha256="",
        signature=b"\x00" * 64,
        signed_at_iso=signed_at_iso,
    )
    cbytes = canonical_bytes(intermediate)
    digest = _hashlib.sha256(cbytes).hexdigest()
    sig = signer.sign(cbytes)
    if not isinstance(sig, bytes):
        raise TypeError(
            f"CalibrationSignerProtocol.sign must return bytes; "
            f"got {type(sig).__name__}"
        )
    # Ed25519 detached signatures are 64 bytes — inline-literal check
    # (V1 discipline). Non-Ed25519 signers would fail this gate.
    if len(sig) != 64:
        raise ValueError(
            f"CalibrationSignerProtocol.sign returned signature of "
            f"{len(sig)} bytes; expected 64 (Ed25519 detached)"
        )

    return CalibrationReport(
        schema_version=1,
        run_id=report.run_id,
        operator_org_slug=report.operator_org_slug,
        golden_set_manifest_path=report.golden_set_manifest_path,
        golden_set_manifest_hash=report.golden_set_manifest_hash,
        items=report.items,
        summary_judge_mean=report.summary_judge_mean,
        summary_judge_stddev=report.summary_judge_stddev,
        summary_per_dimension_mean=report.summary_per_dimension_mean,
        council_charter_snapshot_hash=report.council_charter_snapshot_hash,
        router_yaml_snapshot_hash=report.router_yaml_snapshot_hash,
        assembled_at_iso=report.assembled_at_iso,
        canonical_sha256=digest,
        signature=sig,
        signed_at_iso=signed_at_iso,
    )


# ---------------------------------------------------------------------------
# §4.15 step 10 v5 — first-write-wins operator pubkey provenance
# ---------------------------------------------------------------------------


def _pubkey_key_path(operator_org_slug: str) -> str:
    """Build the vault-relative operator pubkey path.

    Inline-literal RHS (V1 discipline — re-formatted from a fresh literal
    at every call site so a rebind of the module-level template cannot
    redirect the write).
    """
    if not operator_org_slug:
        raise ValueError("operator_org_slug must be non-empty")
    return (
        f"vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519"
    )


def _pubkey_provenance_path(operator_org_slug: str) -> str:
    """Build the vault-relative provenance sidecar path. Inline-literal RHS."""
    if not operator_org_slug:
        raise ValueError("operator_org_slug must be non-empty")
    return (
        f"vault/{operator_org_slug}/calibration/keys/"
        f"pubkey_first_write_provenance.json"
    )


def _build_provenance_bytes(
    *,
    operator_org_slug: str,
    run_id: str,
    first_write_iso: str,
) -> bytes:
    """Serialize the provenance sidecar JSON.

    Stable-sorted keys + UTF-8 encoding to match the vault's canonical
    persistence convention. The algorithm tag is the inline literal
    ``"Ed25519"`` — a rebind of ``CALIBRATION_SIGNING_ALGORITHM`` cannot
    fool this payload.
    """
    payload: dict[str, str] = {
        "operator_org_slug": operator_org_slug,
        "first_write_run_id": run_id,
        "first_write_iso": first_write_iso,
        "algorithm": "Ed25519",
        "schema_version": "1",
    }
    return json.dumps(
        payload, sort_keys=True, separators=(", ", ": "), ensure_ascii=False
    ).encode("utf-8")


def reconcile_operator_pubkey(
    *,
    operator_org_slug: str,
    run_id: str,
    first_write_iso: str,
    signer: CalibrationSignerProtocol,
    pubkey_read: PubkeyVaultReader,
    pubkey_write: PubkeyVaultWriter,
) -> tuple[bytes, bool]:
    """§4.15 step 10 v5 — first-write-wins pubkey provenance reconciler.

    1. Read the stored pubkey via ``pubkey_read`` (``None`` if absent).
    2. Fetch the signer's current pubkey bytes.
    3. If absent: write (pubkey + provenance) via ``pubkey_write`` under
       ``state-success`` write-if-absent semantics. Return (fresh_pubkey,
       is_first_write=True).
    4. If present: assert byte-equal match; return (stored_pubkey,
       is_first_write=False) on match.
    5. On mismatch: rotation attempt. v0.1 rejects rotation hard — raise
       ``ValueError`` (deferred to v0.2 ``key-rotation-write`` intent).
       The message carries enough info to drive the operator-visible
       "key rotation not supported in v0.1" surface.

    :returns: ``(authoritative_pubkey_bytes, is_first_write)``.
    """
    if not operator_org_slug:
        raise ValueError("operator_org_slug must be non-empty")
    if not run_id:
        raise ValueError("run_id must be non-empty")
    if not first_write_iso:
        raise ValueError("first_write_iso must be non-empty")

    stored = pubkey_read(operator_org_slug=operator_org_slug)
    fresh = signer.public_key_bytes()
    if not isinstance(fresh, bytes):
        raise TypeError(
            f"CalibrationSignerProtocol.public_key_bytes must return bytes; "
            f"got {type(fresh).__name__}"
        )
    # Ed25519 raw public keys are 32 bytes.
    if len(fresh) != 32:
        raise ValueError(
            f"CalibrationSignerProtocol.public_key_bytes returned "
            f"{len(fresh)} bytes; expected 32 (Ed25519 raw pubkey)"
        )

    if stored is None:
        provenance = _build_provenance_bytes(
            operator_org_slug=operator_org_slug,
            run_id=run_id,
            first_write_iso=first_write_iso,
        )
        pubkey_write(
            operator_org_slug=operator_org_slug,
            pubkey_bytes=fresh,
            provenance_bytes=provenance,
        )
        return fresh, True

    if stored != fresh:
        raise ValueError(
            f"operator pubkey rotation detected for {operator_org_slug!r}: "
            f"stored={stored.hex()[:16]}... fresh={fresh.hex()[:16]}... "
            f"— rotation requires key-rotation-write intent (v0.2)"
        )

    return stored, False


# ---------------------------------------------------------------------------
# §4.15 step 10 v5 — verify_calibration_report (freshness + signature)
# ---------------------------------------------------------------------------


def _parse_signed_at(signed_at_iso: str) -> datetime:
    """Parse ``signed_at_iso`` to a timezone-aware ``datetime``.

    Accepts ``Z`` suffix by normalizing to ``+00:00`` (Python's
    ``datetime.fromisoformat`` in 3.11+ handles ``Z`` natively, but we
    normalize defensively).

    :raises ValueError: on malformed timestamp or naive datetime.
    """
    normalized = (
        signed_at_iso[:-1] + "+00:00"
        if signed_at_iso.endswith("Z")
        else signed_at_iso
    )
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(
            f"signed_at_iso must be timezone-aware; got naive {signed_at_iso!r}"
        )
    return parsed


def verify_calibration_report(
    report: CalibrationReport,
    *,
    pubkey_bytes: bytes,
    now_utc: ClockNowUTC | None = None,
) -> None:
    """§4.15 step 10 v5 — verify a signed CalibrationReport.

    Order (per blueprint — freshness BEFORE signature):

    1. Reject unsigned reports (``signature is None`` or
       ``signed_at_iso is None``) with ``ValueError``. These are operator-
       refusal artifacts, not verification failures.

    2. Freshness check: parse ``signed_at_iso``; assert
       ``(now - signed_at) < timedelta(days=90)``. Inline-literal RHS —
       rebind of ``MAX_CALIBRATION_AGE_DAYS`` cannot broaden the window.
       On stale: raise ``F-PIPE-21.calibration_signature_stale``.

    3. Canonical bytes recomputation: compute ``canonical_bytes(report)``
       and verify the attached ``canonical_sha256`` matches. Mismatch =>
       tampering or re-assembly drift; raise ``ValueError`` (tests will
       convert this to F_PIPE_21 as needed at the run_eval_pipeline layer).

    4. Ed25519 signature verification against ``pubkey_bytes`` (32 raw).
       ``cryptography.exceptions.InvalidSignature`` propagates on tamper.
    """
    now_fn: ClockNowUTC = (
        now_utc if now_utc is not None else (lambda: datetime.now(timezone.utc))
    )

    # Step 1.
    if report.signature is None or report.signed_at_iso is None:
        raise ValueError(
            "CalibrationReport is unsigned (signature=None or "
            "signed_at_iso=None); verify is not applicable"
        )

    # Step 2 — freshness. Inline-literal 90-day RHS.
    signed_at = _parse_signed_at(report.signed_at_iso)
    now = now_fn()
    if now.tzinfo is None:
        raise ValueError("ClockNowUTC returned a naive datetime")
    window = timedelta(days=90)
    age = now - signed_at
    if age >= window:
        raise F_PIPE_21(
            trigger="calibration_signature_stale",
            details={
                "run_id": report.run_id,
                "operator_org_slug": report.operator_org_slug,
                "signed_at_iso": report.signed_at_iso,
                "now": now.isoformat(),
                "age_days": age.days,
                "max_days": 90,
            },
        )

    # Step 3 — canonical bytes + sha256 match.
    cbytes = canonical_bytes(report)
    import hashlib as _hashlib

    recomputed = _hashlib.sha256(cbytes).hexdigest()
    if recomputed != report.canonical_sha256:
        raise ValueError(
            f"CalibrationReport canonical_sha256 mismatch: "
            f"attached={report.canonical_sha256!r} "
            f"recomputed={recomputed!r}"
        )

    # Step 4 — Ed25519 signature.
    if not isinstance(pubkey_bytes, bytes):
        raise TypeError(
            f"pubkey_bytes must be bytes; got {type(pubkey_bytes).__name__}"
        )
    if len(pubkey_bytes) != 32:
        raise ValueError(
            f"pubkey_bytes must be 32 bytes (Ed25519 raw); got {len(pubkey_bytes)}"
        )

    pubkey = Ed25519PublicKey.from_public_bytes(pubkey_bytes)
    try:
        pubkey.verify(report.signature, cbytes)
    except InvalidSignature:
        # Re-raise the cryptography-native exception so callers can
        # distinguish "tampered signature" from other verify failures.
        raise


# ---------------------------------------------------------------------------
# Reference signer — wraps cryptography's Ed25519PrivateKey
# ---------------------------------------------------------------------------


class Ed25519ReferenceSigner:
    """Reference ``CalibrationSignerProtocol`` implementation.

    Wraps a ``cryptography.hazmat.primitives.asymmetric.ed25519.Ed25519PrivateKey``.
    Production wiring constructs one of these from an operator-owned key
    (HSM, age-encrypted file, OS keychain). Tests construct one via
    ``Ed25519PrivateKey.generate()`` for deterministic sign/verify round-
    trips.
    """

    def __init__(self, private_key: Ed25519PrivateKey) -> None:
        if not isinstance(private_key, Ed25519PrivateKey):
            raise TypeError(
                f"private_key must be Ed25519PrivateKey; "
                f"got {type(private_key).__name__}"
            )
        self._private_key: Ed25519PrivateKey = private_key

    def sign(self, canonical_bytes_: bytes) -> bytes:
        if not isinstance(canonical_bytes_, bytes):
            raise TypeError(
                f"canonical_bytes_ must be bytes; "
                f"got {type(canonical_bytes_).__name__}"
            )
        return self._private_key.sign(canonical_bytes_)

    def public_key_bytes(self) -> bytes:
        from cryptography.hazmat.primitives import serialization

        return self._private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )


__all__ = [
    "BLUEPRINT_DEPS",
    "CALIBRATION_KEY_PATH_TMPL",
    "CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL",
    "CalibrationSignerProtocol",
    "ClockNowUTC",
    "Ed25519ReferenceSigner",
    "PubkeyVaultReader",
    "PubkeyVaultWriter",
    "_build_provenance_bytes",
    "_parse_signed_at",
    "_pubkey_key_path",
    "_pubkey_provenance_path",
    "reconcile_operator_pubkey",
    "sign_report",
    "verify_calibration_report",
]
