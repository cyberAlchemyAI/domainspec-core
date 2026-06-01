"""S11c cite-time dossier lock verify + BT11 cross-org reference policy.
[§4.4.1 step 5 + §4.6.5 + §3 Scout §2.5]

Pure-function verifiers for the §4.4.1 step 5 POST-gate hook. Three-part lock
verify (S11c) compares live ``(canonical_path, inode, content_hash)`` against
the operator-signed dossier signoff; cross-org policy (BT11) inspects the
dossier path's org slug against the current session and demands draft-time
secondary confirmation + audit-entry presence.

This module mirrors :class:`pipeline.scout.entity_research.DossierSignoff`
locally as :class:`DossierSignoffSnapshot` to keep the verifier a pure leaf
— Section 4 must not import from Section 3 at this layer because the Scout
module has not landed yet and we must not create a circular-build dependency.
Round 6 capstone may swap to the direct Scout import once that section lands;
the snapshot's field set is a strict superset of the Scout dataclass.

Round 6 capstone wires :func:`verify_dossier_cite` into §4.4.1 step 5 after
``vault_read(intent="dossier-verify-read")`` loads both the signoff JSON and
the live dossier body bytes.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# Failure-code constants (§6.2 / §6.6 / §4.7.2)
# ---------------------------------------------------------------------------


F_POST_08_FAIL_PATH: str = "F-POST-08.dossier_s11c_fail_path"
F_POST_08_FAIL_INODE: str = "F-POST-08.dossier_s11c_fail_inode"
F_POST_08_FAIL_HASH: str = "F-POST-08.dossier_s11c_fail_hash"
F_POST_08_SIGNOFF_MISSING: str = "F-POST-08.dossier_s11c_signoff_missing"
F_POST_08_SIGNOFF_EXPIRED: str = "F-POST-08.dossier_s11c_signoff_expired"
F_POST_08_SIGNATURE_INVALID: str = "F-POST-08.dossier_s11c_signature_invalid"

F_PRE_14_DOSSIER_UNSIGNED: str = "F-PRE-14.dossier_unsigned"

F_BT11_01: str = "F-BT11-01.cross_org_reference_created_without_audit_entry"
F_BT11_02: str = "F-BT11-02.cross_org_reference_missing_draft_time_confirmation"
F_POST_09: str = "F-POST-09.bt11_cross_org_unconfirmed"


_DOSSIER_PATH_RE = re.compile(
    r"(?:^|/)orgs/(?P<slug>[A-Za-z0-9_\-]+)/dossier/entities/[^/]+$"
)


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class DossierSignoffSnapshot:
    """Local mirror of :class:`pipeline.scout.entity_research.DossierSignoff`.

    Field set matches §3 Scout v0.1 §2.5 exactly. ``operator_signature`` is
    bytes (the on-disk JSON encodes it as hex; :func:`parse_signoff_json`
    handles the conversion).
    """

    signed_at_utc: str
    operator_id: str
    signed_canonical_path: str
    signed_inode: int
    signed_content_hash: str
    operator_signature: bytes
    expires_at_utc: str


@dataclass(frozen=True, kw_only=True)
class DossierLiveState:
    """Snapshot of the dossier body as observed at cite-time.

    All three fields are produced by the caller via Section 2's
    ``vault_read(intent="dossier-verify-read")`` — Round 5 itself does no
    filesystem I/O.
    """

    canonical_path: str
    inode: int
    content_hash: str


@dataclass(frozen=True, kw_only=True)
class S11cVerifyResult:
    """Three-part lock verify outcome."""

    s11c_pass: bool
    failure_code: Optional[str]
    failure_detail: str


@dataclass(frozen=True, kw_only=True)
class CrossOrgVerifyResult:
    """BT11 cross-org reference policy outcome."""

    cross_org_pass: bool
    cross_org_dossier: bool
    failure_codes: tuple[str, ...]
    failure_detail: str


@dataclass(frozen=True, kw_only=True)
class DossierCiteVerifyResult:
    """Composed S11c + BT11 result for §4.4.1 step 5."""

    s11c_pass: bool
    cross_org_pass: bool
    overall_pass: bool
    cross_org_dossier: bool
    failure_codes: tuple[str, ...]
    failure_detail: str


# ---------------------------------------------------------------------------
# Hash helper
# ---------------------------------------------------------------------------


def compute_dossier_body_hash(body: bytes) -> str:
    """SHA3-512 hex digest of dossier markdown bytes (128 hex chars)."""

    if not isinstance(body, (bytes, bytearray)):
        raise TypeError(f"body must be bytes, got {type(body).__name__}")
    return hashlib.sha3_512(bytes(body)).hexdigest()


# ---------------------------------------------------------------------------
# Signoff JSON parser
# ---------------------------------------------------------------------------


def parse_signoff_json(data) -> DossierSignoffSnapshot:
    """Parse a dossier-signoff JSON document into the local snapshot dataclass.

    Accepts ``str`` (JSON text), ``bytes`` / ``bytearray`` (UTF-8 JSON), or a
    pre-parsed ``dict`` (already loaded by the caller). Raises ``ValueError``
    on malformed payload, ``KeyError`` on missing fields, ``TypeError`` on
    wrong input type.
    """

    if isinstance(data, dict):
        obj = data
    elif isinstance(data, (bytes, bytearray)):
        obj = json.loads(bytes(data).decode("utf-8"))
    elif isinstance(data, str):
        obj = json.loads(data)
    else:
        raise TypeError(
            f"data must be str, bytes, or dict, got {type(data).__name__}"
        )

    sig_raw = obj["operator_signature"]
    if isinstance(sig_raw, (bytes, bytearray)):
        signature_bytes = bytes(sig_raw)
    else:
        signature_bytes = bytes.fromhex(str(sig_raw))

    return DossierSignoffSnapshot(
        signed_at_utc=str(obj["signed_at_utc"]),
        operator_id=str(obj["operator_id"]),
        signed_canonical_path=str(obj["signed_canonical_path"]),
        signed_inode=int(obj["signed_inode"]),
        signed_content_hash=str(obj["signed_content_hash"]),
        operator_signature=signature_bytes,
        expires_at_utc=str(obj["expires_at_utc"]),
    )


# ---------------------------------------------------------------------------
# §4.4.1 step 5 / §4.7-BT11 — S11c three-part lock verifier
# ---------------------------------------------------------------------------


def verify_s11c_lock(
    *,
    signoff: Optional[DossierSignoffSnapshot],
    live: DossierLiveState,
    signature_verifier: Optional[Callable[[DossierSignoffSnapshot], bool]] = None,
    current_utc: Optional[str] = None,
) -> S11cVerifyResult:
    """Three-part dossier lock verify against the operator signoff.

    Order of checks:

    1. Signoff present (else :data:`F_POST_08_SIGNOFF_MISSING`).
    2. Signoff not expired (if ``current_utc`` is given). UTC ISO-8601
       lexicographic compare against ``signoff.expires_at_utc``.
    3. Optional signature verification via injected callable.
    4. canonical_path equality.
    5. inode equality.
    6. content_hash equality.

    First failure short-circuits with the corresponding failure code.
    """

    if not isinstance(live, DossierLiveState):
        raise TypeError(
            f"live must be DossierLiveState, got {type(live).__name__}"
        )

    if signoff is None:
        return S11cVerifyResult(
            s11c_pass=False,
            failure_code=F_POST_08_SIGNOFF_MISSING,
            failure_detail="dossier signoff is missing — Law 5 unsigned dossier",
        )
    if not isinstance(signoff, DossierSignoffSnapshot):
        raise TypeError(
            f"signoff must be DossierSignoffSnapshot, got {type(signoff).__name__}"
        )

    if current_utc is not None:
        if not isinstance(current_utc, str):
            raise TypeError("current_utc must be ISO-8601 str or None")
        if current_utc > signoff.expires_at_utc:
            return S11cVerifyResult(
                s11c_pass=False,
                failure_code=F_POST_08_SIGNOFF_EXPIRED,
                failure_detail=(
                    f"signoff expired at {signoff.expires_at_utc} "
                    f"(now {current_utc})"
                ),
            )

    if signature_verifier is not None:
        if not callable(signature_verifier):
            raise TypeError("signature_verifier must be callable or None")
        if not signature_verifier(signoff):
            return S11cVerifyResult(
                s11c_pass=False,
                failure_code=F_POST_08_SIGNATURE_INVALID,
                failure_detail="operator_signature verification failed",
            )

    if live.canonical_path != signoff.signed_canonical_path:
        return S11cVerifyResult(
            s11c_pass=False,
            failure_code=F_POST_08_FAIL_PATH,
            failure_detail=(
                f"canonical_path drift: live={live.canonical_path!r} "
                f"signed={signoff.signed_canonical_path!r}"
            ),
        )
    if live.inode != signoff.signed_inode:
        return S11cVerifyResult(
            s11c_pass=False,
            failure_code=F_POST_08_FAIL_INODE,
            failure_detail=(
                f"inode drift: live={live.inode} signed={signoff.signed_inode}"
            ),
        )
    if live.content_hash != signoff.signed_content_hash:
        return S11cVerifyResult(
            s11c_pass=False,
            failure_code=F_POST_08_FAIL_HASH,
            failure_detail=(
                f"content_hash drift: live={live.content_hash[:16]}... "
                f"signed={signoff.signed_content_hash[:16]}..."
            ),
        )

    return S11cVerifyResult(
        s11c_pass=True,
        failure_code=None,
        failure_detail="",
    )


# ---------------------------------------------------------------------------
# BT11 — cross-org dossier reference policy
# ---------------------------------------------------------------------------


def extract_org_slug_from_dossier_path(canonical_path: str) -> Optional[str]:
    """Extract the org slug from a dossier path of shape
    ``...orgs/{slug}/dossier/entities/{entity_slug}.md``.

    Returns ``None`` for paths that don't match the dossier shape (e.g.
    ``vault_shared/`` or unrelated paths) — those are not BT11-relevant.
    """

    if not isinstance(canonical_path, str):
        raise TypeError("canonical_path must be str")
    m = _DOSSIER_PATH_RE.search(canonical_path)
    if m is None:
        return None
    return m.group("slug")


def is_cross_org_dossier(
    *, dossier_canonical_path: str, current_org_slug: str
) -> bool:
    """True iff the dossier belongs to a different org than the current session.

    Returns False for non-dossier paths (vault_shared/, anything that doesn't
    match the dossier path shape).
    """

    if not isinstance(current_org_slug, str):
        raise TypeError("current_org_slug must be str")
    dossier_slug = extract_org_slug_from_dossier_path(dossier_canonical_path)
    if dossier_slug is None:
        return False
    return dossier_slug != current_org_slug


def verify_cross_org_reference(
    *,
    dossier_canonical_path: str,
    current_org_slug: str,
    draft_time_confirmation_present: bool,
    audit_entry_present: bool,
) -> CrossOrgVerifyResult:
    """BT11 cross-org reference policy.

    For same-org references → unconditional PASS, ``cross_org_dossier=False``.

    For cross-org references, both flags must be True:
    * ``audit_entry_present=False`` → :data:`F_BT11_01` (and
      :data:`F_POST_09` is added to the failure-code list to surface in the
      rails report at §4.4.1 step 5).
    * ``draft_time_confirmation_present=False`` → :data:`F_BT11_02` +
      :data:`F_POST_09`.
    Both missing → both codes appear plus a single :data:`F_POST_09`.
    """

    cross_org = is_cross_org_dossier(
        dossier_canonical_path=dossier_canonical_path,
        current_org_slug=current_org_slug,
    )
    if not cross_org:
        return CrossOrgVerifyResult(
            cross_org_pass=True,
            cross_org_dossier=False,
            failure_codes=(),
            failure_detail="",
        )

    codes: list[str] = []
    detail_bits: list[str] = []
    if not audit_entry_present:
        codes.append(F_BT11_01)
        detail_bits.append("audit entry missing for cross-org reference")
    if not draft_time_confirmation_present:
        codes.append(F_BT11_02)
        detail_bits.append("draft-time secondary confirmation missing")

    if codes:
        codes.append(F_POST_09)
        return CrossOrgVerifyResult(
            cross_org_pass=False,
            cross_org_dossier=True,
            failure_codes=tuple(codes),
            failure_detail="; ".join(detail_bits),
        )

    return CrossOrgVerifyResult(
        cross_org_pass=True,
        cross_org_dossier=True,
        failure_codes=(),
        failure_detail="",
    )


# ---------------------------------------------------------------------------
# Composed cite-time verifier (§4.4.1 step 5)
# ---------------------------------------------------------------------------


def verify_dossier_cite(
    *,
    signoff: Optional[DossierSignoffSnapshot],
    live: DossierLiveState,
    current_org_slug: str,
    draft_time_confirmation_present: bool = False,
    audit_entry_present: bool = False,
    signature_verifier: Optional[Callable[[DossierSignoffSnapshot], bool]] = None,
    current_utc: Optional[str] = None,
) -> DossierCiteVerifyResult:
    """Compose S11c three-part lock verify + BT11 cross-org policy.

    Both verifiers run unconditionally so a failure of one does not mask the
    other. The result's ``overall_pass`` is the conjunction; the
    ``failure_codes`` tuple lists every code surfaced (S11c at most one;
    BT11 zero / one / two BT-codes plus one F-POST-09 grouping code).
    """

    s11c = verify_s11c_lock(
        signoff=signoff,
        live=live,
        signature_verifier=signature_verifier,
        current_utc=current_utc,
    )
    cross = verify_cross_org_reference(
        dossier_canonical_path=live.canonical_path,
        current_org_slug=current_org_slug,
        draft_time_confirmation_present=draft_time_confirmation_present,
        audit_entry_present=audit_entry_present,
    )

    failure_codes: list[str] = []
    detail_bits: list[str] = []
    if not s11c.s11c_pass:
        failure_codes.append(s11c.failure_code or "")
        detail_bits.append(f"S11c: {s11c.failure_detail}")
    if not cross.cross_org_pass:
        failure_codes.extend(cross.failure_codes)
        detail_bits.append(f"BT11: {cross.failure_detail}")

    return DossierCiteVerifyResult(
        s11c_pass=s11c.s11c_pass,
        cross_org_pass=cross.cross_org_pass,
        overall_pass=s11c.s11c_pass and cross.cross_org_pass,
        cross_org_dossier=cross.cross_org_dossier,
        failure_codes=tuple(failure_codes),
        failure_detail="; ".join(detail_bits),
    )


__all__ = [
    "F_POST_08_FAIL_PATH",
    "F_POST_08_FAIL_INODE",
    "F_POST_08_FAIL_HASH",
    "F_POST_08_SIGNOFF_MISSING",
    "F_POST_08_SIGNOFF_EXPIRED",
    "F_POST_08_SIGNATURE_INVALID",
    "F_PRE_14_DOSSIER_UNSIGNED",
    "F_BT11_01",
    "F_BT11_02",
    "F_POST_09",
    "DossierSignoffSnapshot",
    "DossierLiveState",
    "S11cVerifyResult",
    "CrossOrgVerifyResult",
    "DossierCiteVerifyResult",
    "compute_dossier_body_hash",
    "parse_signoff_json",
    "verify_s11c_lock",
    "extract_org_slug_from_dossier_path",
    "is_cross_org_dossier",
    "verify_cross_org_reference",
    "verify_dossier_cite",
]
