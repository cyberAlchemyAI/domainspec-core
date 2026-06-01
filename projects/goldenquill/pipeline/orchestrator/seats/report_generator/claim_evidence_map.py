"""§14 Report Generator claim_evidence_map — assembler + Ed25519 signer envelope.

Per §14.5.1 + §14 v1 LOCK 2026-05-10 (RT-1a/1b/1c + RT-6c + RT-7b + RT-8b/8c +
RT-C2-08/09/10 closures). Mirrors the submission-flow assembler in
``pipeline.logician.claim_evidence`` but on the §14-specific schema
(per-period grant reporting; source kinds are operational_data /
proposal_commitments / kfr / benchmarks; per-claim-kind extension fields
for photo caption hash + beneficiary consent_tier history timestamp +
narrative paraphrase flag).

This module:

* Assembles a ``ClaimEvidenceMap`` from a tuple of validated
  ``ClaimEntry`` rows + envelope fields. Construction-time validation
  enforces per-kind invariants (source kinds, required source fields,
  per-claim extension-field compatibility).
* Serializes the map to canonical-JSON bytes deterministically — same
  byte stream regardless of input ordering of claims. ``sort_keys=True``
  + tight separators + UTF-8.
* Computes the signing payload (canonical-JSON of all fields EXCEPT
  ``operator_signature`` + ``operator_signed_at_utc``; the operator
  signs the draft + map state at the moment of pre-finalize check).
* Signs via injected ``Ed25519SignerProtocol`` (E-011 crypto-agility
  envelope — no direct ``cryptography`` / ``nacl`` import; the injected
  signer is the only sanctioned route to the key material).
* Verifies via injected ``Ed25519VerifierProtocol`` against the
  operator's pinned public key.

Post-sign immutability (RT-8b closure): once ``sign_claim_evidence_map``
returns a SIGNED map, mutation is structurally impossible because
``ClaimEvidenceMap`` is a frozen kw_only dataclass. The companion
``draft_<v>.md`` write-lock + chmod 0444 is the seat-level filesystem
discipline; it lives in the WS-J Slice 3 wiring (post-sign filesystem
locking is not a signer responsibility).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Final, Optional, Protocol, runtime_checkable

from ._canonical import (
    canonical_json_bytes,
    compute_sha3_512_hex,
    is_well_formed_sha3_512_hex,
)
from ._schemas import (
    CLAIM_EVIDENCE_MAP_VERSION_V0_2,
    CLAIM_KINDS,
    OPERATOR_SIG_STATUS_PENDING,
    OPERATOR_SIG_STATUS_SIGNED,
    PROPOSAL_COMMITMENT_STATUS_PROMOTED,
    SUB_SECTIONS_V0_2,
    ClaimEntry,
    ClaimEvidenceMap,
    SourceRef,
)

SCHEMA_VERSION_V1: Final[str] = "claim_evidence_map.v1"


# ---------------------------------------------------------------------------
# Injected crypto Protocols (E-011 crypto-agility envelope)
# ---------------------------------------------------------------------------


@runtime_checkable
class Ed25519SignerProtocol(Protocol):
    """Injected Ed25519 signer.

    ``__call__(message_bytes) -> signature_bytes`` returns the Ed25519
    signature over ``message_bytes`` under the operator's private key.
    The signer module holds the key material — this module never sees it.

    Exceptions from the signer propagate to the caller; the SIGNED-map
    transition fail-closes if the signer raises (the caller returns the
    bundle in DRAFT_PENDING_OPERATOR_SIGN state with a failure record).
    """

    def __call__(self, message_bytes: bytes) -> bytes: ...


@runtime_checkable
class Ed25519VerifierProtocol(Protocol):
    """Injected Ed25519 verifier.

    ``__call__(message_bytes, signature, public_key) -> True | False``.

    Strict ``is True`` identity is applied by the gate caller — a
    truthy non-True return is treated as failure (mirrors §4 v2.x
    F-AMDT-05 / F-AMDT-10 / F-AMDT-11 + F-CLASS-* signature-verify
    precedent).
    """

    def __call__(
        self,
        message_bytes: bytes,
        signature: bytes,
        public_key: bytes,
    ) -> bool: ...


# ---------------------------------------------------------------------------
# Wire-format dict assemblers (deterministic; used for canonical-bytes)
# ---------------------------------------------------------------------------


def _source_ref_to_dict(s: SourceRef) -> dict[str, object]:
    """Wire-format dict for a SourceRef. Keys present iff non-None for the kind.

    The ordering inside the returned dict is irrelevant — ``canonical_json_bytes``
    enforces sort_keys=True at serialization.
    """
    out: dict[str, object] = {"kind": s.kind}
    if s.kind == "operational_data":
        out["sub_kind"] = s.sub_kind
        out["source_path"] = s.source_path
        out["source_row_id"] = s.source_row_id
        out["source_content_sha3_512"] = s.source_content_sha3_512
        if s.source_value is not None:
            out["source_value"] = _encode_source_value(s.source_value)
    elif s.kind == "proposal_commitments":
        out["commitment_id"] = s.commitment_id
        out["commitment_status"] = s.commitment_status
        out["scope_tags_at_commitment"] = list(s.scope_tags_at_commitment)
    elif s.kind == "kfr":
        out["source_path"] = s.source_path
        out["source_row_id"] = s.source_row_id
        out["source_content_sha3_512"] = s.source_content_sha3_512
        out["kfr_atomic_snapshot_id"] = s.kfr_atomic_snapshot_id
        if s.source_value is not None:
            out["source_value"] = _encode_source_value(s.source_value)
    elif s.kind == "benchmarks":
        out["source_path"] = s.source_path
        out["source_row_id"] = s.source_row_id
        out["source_content_sha3_512"] = s.source_content_sha3_512
        if s.source_value is not None:
            out["source_value"] = _encode_source_value(s.source_value)
    return out


def _encode_source_value(value: object) -> object:
    """Encode source_value for canonical-JSON.

    Decimal → canonical-string per v7.0.4-M1 Decimal mandate (never float).
    int → int. str → str. Anything else → str(value) as last resort, raising
    on unsupported types is the safer policy.
    """
    if isinstance(value, Decimal):
        # Canonical Decimal: use str() to preserve scale exactly.
        return str(value)
    if isinstance(value, bool):
        # bool is a subtype of int — reject before int branch.
        raise TypeError("source_value must not be bool; use int / Decimal / str")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return value
    raise TypeError(
        f"source_value type {type(value).__name__} unsupported; use Decimal | int | str"
    )


def _claim_entry_to_dict(c: ClaimEntry) -> dict[str, object]:
    out: dict[str, object] = {
        "claim_id": c.claim_id,
        "sub_section": c.sub_section,
        "claim_text": c.claim_text,
        "claim_kind": c.claim_kind,
        "sources": [_source_ref_to_dict(s) for s in c.sources],
    }
    if c.caption_text_sha3_512 is not None:
        out["caption_text_sha3_512"] = c.caption_text_sha3_512
    if c.consent_tier_history_at_read_utc is not None:
        out["consent_tier_history_at_read_utc"] = c.consent_tier_history_at_read_utc
    if c.editor_approved_paraphrase:
        out["editor_approved_paraphrase"] = True
    return out


def _map_to_dict(
    m: ClaimEvidenceMap,
    *,
    include_signature_fields: bool,
) -> dict[str, object]:
    """Serialize the map to a dict.

    When ``include_signature_fields=False`` (the signing-payload shape):

    * ``operator_signature`` and ``operator_signed_at_utc`` are EXCLUDED.
    * ``operator_signature_status`` is NORMALIZED to
      ``OPERATOR_SIG_STATUS_PENDING`` regardless of the map's current
      state. This is what keeps the signing-payload bytes stable across
      the sign→verify transition — the operator commits to the
      PENDING-state map content; after signing the status flips to
      SIGNED but the bytes the signature covers are unchanged.

    When ``include_signature_fields=True`` (the on-disk / content-hash
    shape): all fields are included as-is.
    """
    out: dict[str, object] = {
        "schema_version": m.schema_version,
        "claim_evidence_map_version": m.claim_evidence_map_version,
        "run_id": m.run_id,
        "org_slug": m.org_slug,
        "grant_id": m.grant_id,
        "period_n": m.period_n,
        "draft_path": m.draft_path,
        "draft_version": m.draft_version,
        "draft_content_sha3_512": m.draft_content_sha3_512,
        "authored_at_utc": m.authored_at_utc,
        "authored_by_seat": m.authored_by_seat,
        "claims": [_claim_entry_to_dict(c) for c in m.claims],
    }
    if include_signature_fields:
        out["operator_signature_status"] = m.operator_signature_status
        out["operator_signature"] = m.operator_signature
        out["operator_signed_at_utc"] = m.operator_signed_at_utc
    else:
        out["operator_signature_status"] = OPERATOR_SIG_STATUS_PENDING
    return out


# ---------------------------------------------------------------------------
# Public canonical-byte helpers
# ---------------------------------------------------------------------------


def canonical_map_bytes(m: ClaimEvidenceMap) -> bytes:
    """Full canonical-JSON bytes of the map INCLUDING signature fields.

    This is the content-hash-input form (what
    ``orgs/<slug>/.../operator_signature.signed.yaml`` records in its
    ``claim_evidence_map_content_sha3_512`` field per RT-C2-09 closure).
    """
    return canonical_json_bytes(_map_to_dict(m, include_signature_fields=True))


def signing_payload_bytes(m: ClaimEvidenceMap) -> bytes:
    """Canonical-JSON bytes EXCLUDING operator_signature + operator_signed_at_utc.

    Per §14.5.1: "Operator signs the entire claim_evidence_map.yaml
    (Ed25519 over canonical-JSON of all fields except operator_signature +
    operator_signed_at_utc)". This is the byte stream the injected
    signer / verifier callable consumes.
    """
    return canonical_json_bytes(_map_to_dict(m, include_signature_fields=False))


def compute_map_content_hash(m: ClaimEvidenceMap) -> str:
    """Lowercase-hex SHA3-512 over ``canonical_map_bytes(m)``."""
    return compute_sha3_512_hex(canonical_map_bytes(m))


# ---------------------------------------------------------------------------
# Assembly (pre-sign factory)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ClaimEvidenceMapAssemblyError(ValueError):
    """Raised when assemble_claim_evidence_map detects an invariant violation."""

    rule: str

    def __post_init__(self) -> None:
        super(ValueError, self).__init__(
            f"claim_evidence_map assembly violation: {self.rule}"
        )


def assemble_claim_evidence_map(
    *,
    run_id: str,
    org_slug: str,
    grant_id: str,
    period_n: int,
    draft_path: str,
    draft_version: int,
    draft_content_sha3_512: str,
    authored_at_utc: str,
    authored_by_seat: str,
    claims: tuple[ClaimEntry, ...],
) -> ClaimEvidenceMap:
    """Build a pre-sign ``ClaimEvidenceMap`` in DRAFT/PENDING state.

    Returns a map with:

    * ``operator_signature_status = "PENDING_OPERATOR_REVIEW"``
    * ``operator_signature = ""``
    * ``operator_signed_at_utc = ""``

    Caller signs via ``sign_claim_evidence_map``.

    Per-claim invariants are enforced at ``ClaimEntry`` construction;
    the assembler additionally enforces:

    * claims tuple is non-empty (vacuous evidence maps are structurally
      forbidden — pairs with §14.9.2 .empty_promoted_set + waiver cap)
    * claim_ids are unique within the map
    * draft_content_sha3_512 is well-formed 128-hex
    * proposal_commitments source rows MUST be PROMOTED-status (RT-1a
      and §14.4.1 read filter)
    """
    if not isinstance(claims, tuple):
        raise TypeError(f"claims must be tuple, got {type(claims).__name__}")
    if not claims:
        raise ClaimEvidenceMapAssemblyError(rule="claims_must_be_non_empty")
    if not is_well_formed_sha3_512_hex(draft_content_sha3_512):
        raise ClaimEvidenceMapAssemblyError(rule="draft_content_sha3_512_malformed")
    if not isinstance(period_n, int) or period_n < 1:
        raise ClaimEvidenceMapAssemblyError(rule="period_n_must_be_positive_int")

    seen_ids: set[str] = set()
    for c in claims:
        if not isinstance(c, ClaimEntry):
            raise TypeError(f"claim must be ClaimEntry, got {type(c).__name__}")
        if c.claim_id in seen_ids:
            raise ClaimEvidenceMapAssemblyError(
                rule=f"duplicate_claim_id:{c.claim_id}"
            )
        seen_ids.add(c.claim_id)
        if c.claim_kind not in CLAIM_KINDS:
            raise ClaimEvidenceMapAssemblyError(
                rule=f"claim_kind_unknown:{c.claim_kind}"
            )
        if c.sub_section not in SUB_SECTIONS_V0_2:
            raise ClaimEvidenceMapAssemblyError(
                rule=f"sub_section_unknown:{c.sub_section}"
            )
        for src in c.sources:
            if src.kind == "proposal_commitments":
                if src.commitment_status != PROPOSAL_COMMITMENT_STATUS_PROMOTED:
                    raise ClaimEvidenceMapAssemblyError(
                        rule=(
                            f"proposal_commitments_source_status_not_promoted:"
                            f"{c.claim_id}"
                        )
                    )

    # Deterministic ordering: sort claims by claim_id at assembly time so
    # canonical-JSON bytes are stable regardless of caller-supplied order.
    sorted_claims = tuple(sorted(claims, key=lambda e: e.claim_id))

    return ClaimEvidenceMap(
        schema_version=SCHEMA_VERSION_V1,
        claim_evidence_map_version=CLAIM_EVIDENCE_MAP_VERSION_V0_2,
        run_id=run_id,
        org_slug=org_slug,
        grant_id=grant_id,
        period_n=period_n,
        draft_path=draft_path,
        draft_version=draft_version,
        draft_content_sha3_512=draft_content_sha3_512,
        authored_at_utc=authored_at_utc,
        authored_by_seat=authored_by_seat,
        claims=sorted_claims,
        operator_signature_status=OPERATOR_SIG_STATUS_PENDING,
        operator_signature="",
        operator_signed_at_utc="",
    )


# ---------------------------------------------------------------------------
# Signing + verification (injected crypto Protocol)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SignClaimEvidenceMapResult:
    """Outcome of ``sign_claim_evidence_map``.

    On success: ``signed_map`` carries the SIGNED-state map with the
    operator signature + timestamp populated. ``signing_payload_sha3_512``
    is the lowercase-hex SHA3-512 of the signing-payload bytes (the same
    bytes the signer just signed) — convenient for audit log + the
    paired ``operator_signature.signed.yaml`` per RT-C2-09 closure.
    """

    success: bool
    signed_map: Optional[ClaimEvidenceMap]
    signing_payload_sha3_512: str
    detail: str


def sign_claim_evidence_map(
    map_pending: ClaimEvidenceMap,
    *,
    signer: Ed25519SignerProtocol,
    operator_signed_at_utc: str,
) -> SignClaimEvidenceMapResult:
    """Sign the operator's PENDING map; return a SIGNED-state copy.

    Pre-condition: ``map_pending.operator_signature_status == "PENDING_OPERATOR_REVIEW"``.
    Re-signing an already-SIGNED map fail-closes — operator must explicitly
    re-cycle Scribe and re-sign a fresh draft (mirrors RT-8b draft post-sign
    immutability).

    The signer is the injected Ed25519 callback (E-011 crypto-agility
    envelope). This module never imports a crypto library.
    """
    if map_pending.operator_signature_status != OPERATOR_SIG_STATUS_PENDING:
        return SignClaimEvidenceMapResult(
            success=False,
            signed_map=None,
            signing_payload_sha3_512="",
            detail=(
                f"refuse-resign: operator_signature_status="
                f"{map_pending.operator_signature_status!r}, "
                f"expected={OPERATOR_SIG_STATUS_PENDING!r}"
            ),
        )
    payload = signing_payload_bytes(map_pending)
    payload_hash = compute_sha3_512_hex(payload)
    try:
        signature_bytes = signer(payload)
    except Exception as exc:  # pragma: no cover - exception body unimportant
        return SignClaimEvidenceMapResult(
            success=False,
            signed_map=None,
            signing_payload_sha3_512=payload_hash,
            detail=f"signer raised {type(exc).__name__}: {exc!s}",
        )
    if not isinstance(signature_bytes, bytes):
        return SignClaimEvidenceMapResult(
            success=False,
            signed_map=None,
            signing_payload_sha3_512=payload_hash,
            detail=(
                f"signer returned {type(signature_bytes).__name__}; "
                f"expected bytes"
            ),
        )
    signed = ClaimEvidenceMap(
        schema_version=map_pending.schema_version,
        claim_evidence_map_version=map_pending.claim_evidence_map_version,
        run_id=map_pending.run_id,
        org_slug=map_pending.org_slug,
        grant_id=map_pending.grant_id,
        period_n=map_pending.period_n,
        draft_path=map_pending.draft_path,
        draft_version=map_pending.draft_version,
        draft_content_sha3_512=map_pending.draft_content_sha3_512,
        authored_at_utc=map_pending.authored_at_utc,
        authored_by_seat=map_pending.authored_by_seat,
        claims=map_pending.claims,
        operator_signature_status=OPERATOR_SIG_STATUS_SIGNED,
        operator_signature=signature_bytes.hex(),
        operator_signed_at_utc=operator_signed_at_utc,
    )
    return SignClaimEvidenceMapResult(
        success=True,
        signed_map=signed,
        signing_payload_sha3_512=payload_hash,
        detail=f"signed at {operator_signed_at_utc} payload_sha3_512={payload_hash[:16]}…",
    )


@dataclass(frozen=True, kw_only=True)
class VerifyClaimEvidenceMapResult:
    """Outcome of ``verify_claim_evidence_map_signature``."""

    success: bool
    signing_payload_sha3_512: str
    detail: str


def verify_claim_evidence_map_signature(
    signed_map: ClaimEvidenceMap,
    *,
    verifier: Ed25519VerifierProtocol,
    operator_public_key: bytes,
) -> VerifyClaimEvidenceMapResult:
    """Verify the operator signature against the signing payload + pinned public key.

    Strict ``is True`` identity is applied on the verifier's return value
    (mirrors §4 v2.x F-AMDT-05 / F-AMDT-10 + F-CLASS-REGISTER-SIGNATURE-INVALID
    precedent). Truthy non-True returns FAIL.
    """
    if signed_map.operator_signature_status != OPERATOR_SIG_STATUS_SIGNED:
        return VerifyClaimEvidenceMapResult(
            success=False,
            signing_payload_sha3_512="",
            detail=(
                f"map operator_signature_status="
                f"{signed_map.operator_signature_status!r}; expected SIGNED"
            ),
        )
    if not signed_map.operator_signature:
        return VerifyClaimEvidenceMapResult(
            success=False,
            signing_payload_sha3_512="",
            detail="map operator_signature is empty",
        )
    payload = signing_payload_bytes(signed_map)
    payload_hash = compute_sha3_512_hex(payload)
    try:
        signature_bytes = bytes.fromhex(signed_map.operator_signature)
    except ValueError as exc:
        return VerifyClaimEvidenceMapResult(
            success=False,
            signing_payload_sha3_512=payload_hash,
            detail=f"operator_signature is not valid hex: {exc!s}",
        )
    try:
        verified = verifier(payload, signature_bytes, operator_public_key)
    except Exception as exc:  # pragma: no cover
        return VerifyClaimEvidenceMapResult(
            success=False,
            signing_payload_sha3_512=payload_hash,
            detail=f"verifier raised {type(exc).__name__}: {exc!s}",
        )
    if verified is True:
        return VerifyClaimEvidenceMapResult(
            success=True,
            signing_payload_sha3_512=payload_hash,
            detail=f"verified payload_sha3_512={payload_hash[:16]}…",
        )
    return VerifyClaimEvidenceMapResult(
        success=False,
        signing_payload_sha3_512=payload_hash,
        detail=f"verifier returned {verified!r}; expected True (strict identity)",
    )


__all__ = [
    "ClaimEvidenceMapAssemblyError",
    "Ed25519SignerProtocol",
    "Ed25519VerifierProtocol",
    "SCHEMA_VERSION_V1",
    "SignClaimEvidenceMapResult",
    "VerifyClaimEvidenceMapResult",
    "assemble_claim_evidence_map",
    "canonical_map_bytes",
    "compute_map_content_hash",
    "sign_claim_evidence_map",
    "signing_payload_bytes",
    "verify_claim_evidence_map_signature",
]
