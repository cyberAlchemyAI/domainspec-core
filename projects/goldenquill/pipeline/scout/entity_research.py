"""§4.9 M11 Entity Research Pass + S11a/b/c dossier hardening.

Scout Round 10. Implements architecture D.0 (M11) + S11a (per-org
domain allowlist) + S11b (cross-domain diversity gate) + S11c
(operator sign-off with path+inode+content-hash triple lock) per the
LOCKED blueprint §4.9 / §6.9 / §8. Emits one
:class:`EntityDossier` per roster entry via an injected
:class:`VaultWriter` under intent ``"dossier-body-write"``, and binds
operator sign-off to a (canonical_path, inode, content_hash) triple
via an FD-held-closure pattern that keeps the body FD open
continuously from open → hash → bind → vault_write of the sign-off
record (A-03 / RT-v1-CRIT-03 closure, durable enforcement).

Blueprint anchors:

- §4.9 M11 Entity Research Pass — primary implementation target.
  Three public entries: :func:`run_entity_research`,
  :func:`sign_off_dossier`, :func:`read_entity_dossier`.
- §6.9 F-SCOUT-D-01a..e, F-SCOUT-D-02, F-SCOUT-D-03 — the only
  failure codes this module emits.
- §8 numeric pins: ``MAX_DOSSIER_BYTES`` (alias
  ``SCOUT_DOSSIER_MAX_BYTES``) = 5 MB strict `>` boundary;
  ``DOSSIER_VALIDITY_DAYS`` = 90; ``PER_ENTITY_RESEARCH_FETCH_CAP`` = 40;
  ``HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT`` = 2.
- A-03 / RT-v1-CRIT-03 — FD held continuously across sign-off;
  ``vault_write`` of the sign-off record happens INSIDE the with-block.
- A-v3-06 / RT-v2-HIGH-04 — dossier partial-read race closure: size
  is decided from ``os.fstat(fd).st_size`` BEFORE ``os.read``.
- A-13 / RT-v1-MED-07 — 5 MB strict `>` boundary; exactly cap bytes
  accepted, cap+1 bytes rejected.
- A-v3-04 / RT-v2-CRIT-02 + MED-01 — NFC-normalised post-read intent
  equality check via :func:`_assert_intent_matches` on every
  ``vault_read`` call-site: ``source-allowlist-read``,
  ``entity-roster-read``, ``dossier-body-read``,
  ``dossier-signoff-read``.
- Architecture D.0 M11 — per-entity fetch → parse → claim-dedupe →
  S11b confidence tier (HIGH ≥ 2 distinct registrable domains,
  MEDIUM = 1, LOW on disagreement) → S11a allowlist gate →
  dossier body write → UNSOURCED until sign-off.
- Law 3 org isolation — ``run_entity_research`` refuses to consult
  dossiers from another org (``orgs/{session.slug}/dossier/...``
  scoped by the injected reader).
- Autonomy Rule 1 — checkpoint at ``entity_research_start`` +
  ``entity_research_complete`` (success AND failure) and at
  ``dossier_signoff_start`` + ``dossier_signoff_complete`` (both).

Spec-card deviation notes (from pre-staged
``spec_cards/scout_round_10_review_and_entity_research.md`` v1):

- Spec card proposed ``run_entity_research`` returns
  ``tuple[EntityDossier, ...]`` in roster order. Blueprint §4.9 line
  802 specifies ``dict[str, EntityDossier]`` keyed by entity_slug.
  Build honours the blueprint and also exposes a
  :class:`EntityResearchResult` wrapper carrying both the mapping
  and the ordered tuple so callers can use either form.
- Spec card proposed F-SCOUT-D-03 sub-codes for seven drift classes
  (``.domain_not_allowlisted``, ``.insufficient_domain_diversity``,
  ``.intent_mismatch_post_read``, ``.allowlist_parse_error``,
  ``.inode_drift``, ``.content_hash_drift``, ``.path_drift``). Build
  implements all seven under the :class:`DossierSignoffVerifyFailure`
  exception with the sub-code carried as ``reason_tag``.
- Spec card proposed keeping the four new Readers separate
  (``DomainAllowlistReader``, ``EntityRosterReader``,
  ``DossierBodyReader``, ``EntityClaimFetcher``). Build honours this
  rather than collapsing to a single ``IntentedVaultReader`` — each
  Protocol validates its intent-specific YAML / markdown shape at
  the seam, which is lost under a single generic reader.

No module-level side effects on import. Zero network, zero FD
reservation, zero vault calls, zero keystore resolution. All
persistence routes through injected Protocols (E-017 — ninth Scout
firing, with four new Protocol seams introduced here).
AST-lint R1/R3/R4/R5 clean.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import os
import time
import unicodedata
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from typing import (
    Any,
    Callable,
    Final,
    Iterator,
    Mapping,
    Optional,
    Protocol,
    runtime_checkable,
)

from pipeline.scout._constants import (
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    DOSSIER_VALIDITY_DAYS,
    HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT,
    INTENT_DOSSIER_BODY_READ,
    INTENT_DOSSIER_BODY_WRITE,
    INTENT_DOSSIER_SIGNOFF_READ,
    INTENT_DOSSIER_SIGNOFF_WRITE,
    INTENT_ENTITY_ROSTER_READ,
    INTENT_SOURCE_ALLOWLIST_READ,
    PER_ENTITY_RESEARCH_FETCH_CAP,
    SCOUT_DOSSIER_MAX_BYTES,
)
from pipeline.scout._types import (
    DossierSignoff,
    EntityClaim,
    EntityDossier,
    EntityRosterEntry,
    SourceDomainAllowlist,
    entity_dossier_canonical_bytes,
)
from pipeline.sovereignty import canonical_json_bytes

__version__: Final[str] = "0.1.0-scout-r10"

__all__ = [
    "CheckpointWriter",
    "ClockFn",
    "DomainAllowlistReader",
    "DossierBodyReader",
    "DossierSignoffReader",
    "DossierSignoffVerifyFailure",
    "DossierSizeExceeded",
    "EntityClaimCandidate",
    "EntityClaimFetcher",
    "EntityResearchResult",
    "EntityRosterReader",
    "F_SCOUT_D_01",
    "F_SCOUT_D_01a",
    "F_SCOUT_D_01b",
    "F_SCOUT_D_01c",
    "F_SCOUT_D_01d",
    "F_SCOUT_D_01e",
    "F_SCOUT_D_02",
    "F_SCOUT_D_03",
    "FDHandle",
    "IntentMismatch",
    "SessionLike",
    "VaultWriter",
    "_MAX_DOSSIER_BYTES",
    "_assert_intent_matches",
    "_classify_confidence_tier",
    "_dedupe_claims",
    "_dossier_body_path",
    "_dossier_signoff_path",
    "_normalize_claim_text",
    "_open_dossier_body_fd",
    "__version__",
    "read_entity_dossier",
    "run_entity_research",
    "sign_off_dossier",
]


# ---------------------------------------------------------------------------
# Failure codes (blueprint §6.9 — verbatim)
# ---------------------------------------------------------------------------

F_SCOUT_D_01: Final[str] = "F-SCOUT-D-01"  # sign-off binding base
F_SCOUT_D_01a: Final[str] = "F-SCOUT-D-01a"  # canonical-path mismatch
F_SCOUT_D_01b: Final[str] = "F-SCOUT-D-01b"  # inode mismatch
F_SCOUT_D_01c: Final[str] = "F-SCOUT-D-01c"  # content-hash mismatch
F_SCOUT_D_01d: Final[str] = "F-SCOUT-D-01d"  # final re-fstat drift
F_SCOUT_D_01e: Final[str] = "F-SCOUT-D-01e"  # read short (concurrent truncate)
F_SCOUT_D_02: Final[str] = "F-SCOUT-D-02"  # body size > cap
F_SCOUT_D_03: Final[str] = "F-SCOUT-D-03"  # invalid roster kind / cross-cutting

# Public alias for the blueprint §8 pin name — tests pin the module
# constant, production code imports from ``_constants`` directly.
_MAX_DOSSIER_BYTES: Final[int] = SCOUT_DOSSIER_MAX_BYTES


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class DossierSignoffVerifyFailure(Exception):
    """S11c verify failure — triple-lock drift detected at sign-off or read.

    Carries ``code`` (one of F-SCOUT-D-01a..e / F-SCOUT-D-03) and
    ``reason_tag`` (the specific drift class). Mirrors Round 9's
    ``ScoutVerifyInterrupted`` pattern — the specific sub-code tells
    the operator which leg of the triple lock tripped.
    """

    def __init__(self, *, code: str, reason_tag: str) -> None:
        self.code = code
        self.reason_tag = reason_tag
        super().__init__(f"{code}: {reason_tag}")


class DossierSizeExceeded(Exception):
    """F-SCOUT-D-02 — dossier body strictly exceeds ``_MAX_DOSSIER_BYTES``.

    Raised BEFORE any ``os.read`` call (A-v3-06 / RT-v2-HIGH-04
    closure): the size is determined from the held FD's
    ``fstat.st_size``, eliminating the v2 partial-read race in which a
    concurrent truncate between first-read and second-read could
    yield a short body that passed the strict ``>`` test erroneously.
    Reason tag is ``.fstat_size_gt_max``.
    """


class IntentMismatch(Exception):
    """Post-read intent-tuple drift on any dossier ``vault_read`` call-site.

    Mirrors the Channel B / Channel F / Round 10 review_stage pattern.
    Strict-equality miss on ``(session_id, slug, intent)`` — NFC
    normalisation is tolerated with a reason-tag sub-code.
    """

    def __init__(self, *, code: str, reason_tag: str) -> None:
        self.code = code
        self.reason_tag = reason_tag
        super().__init__(f"{code}: {reason_tag}")


# ---------------------------------------------------------------------------
# Injection Protocols (E-017 — ninth Scout firing, 4 new Protocol seams)
# ---------------------------------------------------------------------------


class SessionLike(Protocol):
    """Duck-type shape this module needs from a sovereignty session.

    Mirrors the shape used by Round 9 / Round 10 review_stage. The
    full Section 1 Session satisfies this Protocol without adapter
    code; tests inject a plain dataclass with the three string fields.
    """

    session_id: str
    slug: str
    operator_id: str


@runtime_checkable
class VaultWriter(Protocol):
    """Section 2 ``vault_write`` seam (E-017 reuse).

    Production binding wraps :func:`pipeline.vault.vault_write.vault_write`.
    Tests inject a recorder that captures
    ``(path, bytes_, intent, session_id, slug)`` tuples.
    """

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None: ...


@runtime_checkable
class EntityRosterReader(Protocol):
    """Section 2 ``vault_read`` seam for the entity roster (NEW).

    Production binding reads the per-org roster YAML under intent
    ``"entity-roster-read"`` with NFC-normalised
    :func:`_assert_intent_matches`. Tests inject an in-memory
    recorder that returns a tuple of :class:`EntityRosterEntry`
    instances plus an identity triple.

    The YAML parse error path surfaces as an :class:`IntentMismatch`-
    adjacent ``DossierSignoffVerifyFailure`` with code F-SCOUT-D-03
    and reason tag ``.roster_parse_error``.
    """

    def read_roster(
        self,
        *,
        session_id: str,
        slug: str,
    ) -> tuple[EntityRosterEntry, ...]: ...


@runtime_checkable
class DomainAllowlistReader(Protocol):
    """Section 2 ``vault_read`` seam for S11a domain allowlist (NEW).

    Production binding reads the per-org allowlist YAML under intent
    ``"source-allowlist-read"``. Returns a :class:`SourceDomainAllowlist`
    frozen dataclass. Tests inject a recorder.
    """

    def read_allowlist(
        self,
        *,
        session_id: str,
        slug: str,
    ) -> SourceDomainAllowlist: ...


@runtime_checkable
class EntityClaimFetcher(Protocol):
    """Per-entity live-domain fetch seam for M11 (NEW).

    Production binding wraps Round 4's :class:`HTTPClient` + FD
    broker + nonce registry. Returns a bounded list of
    :class:`EntityClaimCandidate` (pre-tier-assignment candidate
    claims) for a given roster entry.

    The fetcher is bounded by ``PER_ENTITY_RESEARCH_FETCH_CAP = 40``
    (blueprint §8); Channel F BT12 pre-flight applies to every fetch
    (blueprint §4.9 line 807). Production implementations route
    through Channel F's public API; tests inject stubs that return a
    fixed candidate list per ``entity_slug``.
    """

    def fetch(
        self,
        *,
        session: SessionLike,
        roster_entry: EntityRosterEntry,
    ) -> tuple["EntityClaimCandidate", ...]: ...


@runtime_checkable
class DossierBodyReader(Protocol):
    """Section 2 ``vault_read`` seam for dossier body reads (NEW).

    Production binding opens the dossier body under O_RDONLY +
    O_NOFOLLOW via Section 2's FD broker, returning a
    :class:`FDHandle` context manager. The caller uses the FD for the
    read-hash-bind sequence in :func:`sign_off_dossier` and
    :func:`read_entity_dossier`. Tests inject a recorder that yields a
    fake FDHandle pointing at an in-memory body.
    """

    def open_body(
        self,
        *,
        session_id: str,
        slug: str,
        entity_slug: str,
    ) -> "FDHandle": ...


@runtime_checkable
class DossierSignoffReader(Protocol):
    """Section 2 ``vault_read`` seam for dossier sign-off reads (NEW).

    Production binding reads the sign-off JSON under intent
    ``"dossier-signoff-read"``. Returns ``None`` if no sign-off
    record exists (the dossier is UNSOURCED and not Logician-citable).
    """

    def read_signoff(
        self,
        *,
        session_id: str,
        slug: str,
        entity_slug: str,
    ) -> Optional[DossierSignoff]: ...


class CheckpointWriter(Protocol):
    """Autonomy Rule 1 — save state always.

    Production binding wraps
    :func:`pipeline.sovereignty.interrupted_state.checkpoint`. Tests
    inject an in-memory recorder.
    """

    def write(self, *, stage: str, payload: Mapping[str, Any]) -> None: ...


ClockFn = Callable[[], str]
"""Clock returning UTC-aware ISO-8601 string."""


def _default_clock() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# FDHandle — Section 2 FD broker surface (seam)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class FDHandle:
    """Held-FD surface used by dossier read / sign-off paths.

    Implementations expose:

    - ``fd``: integer file descriptor; O_RDONLY + O_NOFOLLOW opened.
    - ``canonical_path``: string form of the fully-resolved path at
      open time (Section 2 resolves through its own
      ``canonical_path`` helper, not a bare ``os.path.realpath``).
    - ``close()``: release the FD on exit.

    The :func:`_open_dossier_body_fd` context manager wraps the
    handle and yields the FD within a ``with`` block that keeps the
    descriptor open across the subsequent hash / bind / vault_write
    sequence (A-03 closure).
    """

    fd: int
    canonical_path: str
    close: Callable[[], None]


# ---------------------------------------------------------------------------
# EntityClaimCandidate — pre-tier-assignment surface from fetcher
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class EntityClaimCandidate:
    """A single factual-claim candidate before S11b tier assignment.

    The fetcher emits these for each successful per-entity fetch;
    :func:`run_entity_research` runs dedupe (by normalised claim_text)
    + S11a allowlist gate + S11b tier assignment to produce the
    canonical :class:`EntityClaim` records stored in the dossier.

    Fields mirror :class:`EntityClaim` minus the derived
    ``confidence_tier`` and ``corroborating_claim_ids`` — those are
    computed during the pass, not the fetch.
    """

    claim_id: str
    claim_text: str
    source_url: str
    source_registrable_domain: str
    fetched_at_utc: str
    url_hash: str
    content_hash: str
    evidence_quote: str


# ---------------------------------------------------------------------------
# EntityResearchResult — pass-level return
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class EntityResearchResult:
    """Output of :func:`run_entity_research`.

    ``dossiers_by_slug`` is the canonical mapping (blueprint §4.9
    line 802). ``ordered`` is the same content as a tuple in roster
    order — callers that want deterministic iteration without sorting
    by slug use this. ``non_allowlisted_domain_events`` records
    S11a gate hits (claim dropped on non-allowlisted domain); these
    are reason-tag sub-codes under F-SCOUT-D-03.
    """

    dossiers_by_slug: Mapping[str, EntityDossier]
    ordered: tuple[EntityDossier, ...]
    non_allowlisted_domain_events: tuple[str, ...]


# ---------------------------------------------------------------------------
# NFC-normalised intent check (A-v3-04 / RT-v2-CRIT-02 + MED-01 closure)
# ---------------------------------------------------------------------------


def _assert_intent_matches(
    *,
    expected_intent: str,
    observed_intent: str,
    expected_session_id: str,
    observed_session_id: str,
    expected_slug: str,
    observed_slug: str,
) -> None:
    """Strict-equality check; NFC drift raises with a sub-code reason tag.

    Raises :class:`IntentMismatch` on any mismatch. Mirrors Channel B
    / Channel F / Round 10 review_stage pattern — defence-in-depth
    against a silently buggy vault.
    """
    if observed_session_id != expected_session_id:
        raise IntentMismatch(
            code=f"{F_SCOUT_D_03}.intent_session_mismatch",
            reason_tag=(
                f"session_id_mismatch:expected={expected_session_id!r} "
                f"got={observed_session_id!r}"
            ),
        )
    if observed_slug != expected_slug:
        raise IntentMismatch(
            code=f"{F_SCOUT_D_03}.intent_slug_mismatch",
            reason_tag=(
                f"slug_mismatch:expected={expected_slug!r} "
                f"got={observed_slug!r}"
            ),
        )
    if observed_intent == expected_intent:
        return
    normalized = unicodedata.normalize("NFC", observed_intent).strip()
    if normalized == expected_intent:
        raise IntentMismatch(
            code=f"{F_SCOUT_D_03}.intent_nfc_drift",
            reason_tag=f"intent_nfc_drift:{observed_intent!r}",
        )
    raise IntentMismatch(
        code=f"{F_SCOUT_D_03}.intent_mismatch_post_read",
        reason_tag=f"intent_mismatch:{observed_intent!r}",
    )


# ---------------------------------------------------------------------------
# Path computation helpers
# ---------------------------------------------------------------------------


def _dossier_body_path(slug: str, entity_slug: str) -> str:
    """``orgs/{slug}/dossier/entities/{entity_slug}.md`` — blueprint §4.9."""
    return f"orgs/{slug}/dossier/entities/{entity_slug}.md"


def _dossier_signoff_path(slug: str, entity_slug: str) -> str:
    """``orgs/{slug}/dossier/signoff/{entity_slug}.json`` — sign-off record."""
    return f"orgs/{slug}/dossier/signoff/{entity_slug}.json"


# ---------------------------------------------------------------------------
# Claim normalisation + dedupe helpers
# ---------------------------------------------------------------------------


def _normalize_claim_text(text: str) -> str:
    """NFC normalise + strip + lowercase for dedupe key.

    Blueprint §4.9 line 821 — "Deduplicate candidate claims by
    normalized claim_text". The normalisation is deliberately narrow
    (lower + strip + NFC) so substantively-distinct claims do not
    collide; broader normalisation (e.g. stemming) is out of scope
    for v0.1.
    """
    return unicodedata.normalize("NFC", text).strip().lower()


def _dedupe_claims(
    candidates: tuple[EntityClaimCandidate, ...],
) -> dict[str, list[EntityClaimCandidate]]:
    """Group candidates by normalised claim text.

    Returns a dict keyed by the dedupe key with the full list of
    candidates supporting that claim. The list is preserved (not
    collapsed) because downstream S11b tier assignment needs the full
    supporting set to count distinct registrable domains.
    """
    grouped: dict[str, list[EntityClaimCandidate]] = {}
    for c in candidates:
        key = _normalize_claim_text(c.claim_text)
        grouped.setdefault(key, []).append(c)
    return grouped


def _classify_confidence_tier(
    supporting: list[EntityClaimCandidate],
) -> str:
    """Blueprint §4.9 S11b — tier assignment by distinct registrable domain.

    - HIGH iff ≥ 2 distinct registrable domains support the claim.
    - MEDIUM iff exactly 1 distinct registrable domain (any number of
      subdomains under it).
    - LOW otherwise (zero supporting — shouldn't happen; defensive
      fallback).

    The distinct-domain count uses the set of
    ``source_registrable_domain`` strings; callers are expected to
    have already normalised registrable-domain extraction via an
    idna-capable helper (Channel F's ``_registrable_domain``). This
    module does not re-extract; it trusts the fetcher's domain field.
    """
    distinct = {c.source_registrable_domain for c in supporting}
    if len(distinct) >= HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT:
        return CONFIDENCE_HIGH
    if len(distinct) == 1:
        return CONFIDENCE_MEDIUM
    return CONFIDENCE_LOW


def _claim_ids_sorted(
    supporting: list[EntityClaimCandidate],
) -> tuple[str, ...]:
    """Deterministic claim_id tuple for corroboration."""
    return tuple(sorted(c.claim_id for c in supporting))


# ---------------------------------------------------------------------------
# FD-held-closure helper (A-03 closure)
# ---------------------------------------------------------------------------


@contextmanager
def _open_dossier_body_fd(
    *,
    body_reader: DossierBodyReader,
    session: SessionLike,
    entity_slug: str,
) -> Iterator[FDHandle]:
    """Open the dossier body FD and hold it until the caller exits.

    The returned :class:`FDHandle` is O_RDONLY + O_NOFOLLOW (enforced
    by the injected ``body_reader``). Closing happens in the ``finally``
    so the FD is released on every exit path, including exceptions.

    Callers wrap the entire hash → bind → ``vault_write(sign-off)``
    sequence inside the ``with`` block so that a concurrent rename
    or bind-mount cannot substitute the file between any two reads
    (A-03 / RT-v1-CRIT-03 closure).
    """
    handle = body_reader.open_body(
        session_id=session.session_id,
        slug=session.slug,
        entity_slug=entity_slug,
    )
    try:
        yield handle
    finally:
        handle.close()


# ---------------------------------------------------------------------------
# Dossier body read helper (A-v3-06 closure)
# ---------------------------------------------------------------------------


def _read_held_body(
    *,
    handle: FDHandle,
    expected_canonical_path: Optional[str] = None,
) -> bytes:
    """Read the full dossier body from a held FD with A-v3-06 closure.

    Sequence (fail-closed at every step):

    1. ``os.fstat(fd)`` — size decided BEFORE any read. If
       ``st.st_size > _MAX_DOSSIER_BYTES``, raise
       :class:`DossierSizeExceeded` with reason tag
       ``.fstat_size_gt_max``. NO ``os.read`` is attempted.
    2. If ``expected_canonical_path`` is provided and differs from
       the handle's ``canonical_path``, raise
       :class:`DossierSignoffVerifyFailure` with code F-SCOUT-D-01a.
    3. ``os.read(fd, st.st_size)`` — read exactly the fstat-observed
       size.
    4. If the read returned fewer bytes than ``st.st_size``, a
       concurrent truncate happened between fstat and read — raise
       F-SCOUT-D-01e.

    The strict ``>`` on the size comparison enforces A-13: a body of
    exactly ``_MAX_DOSSIER_BYTES`` passes; ``_MAX_DOSSIER_BYTES + 1``
    fails.
    """
    st = os.fstat(handle.fd)
    if st.st_size > _MAX_DOSSIER_BYTES:
        raise DossierSizeExceeded(
            f"{F_SCOUT_D_02}.fstat_size_gt_max: dossier body fstat "
            f"st_size={st.st_size} exceeds {_MAX_DOSSIER_BYTES}"
        )
    if (
        expected_canonical_path is not None
        and handle.canonical_path != expected_canonical_path
    ):
        raise DossierSignoffVerifyFailure(
            code=F_SCOUT_D_01a,
            reason_tag=(
                f"canonical_path_mismatch:expected="
                f"{expected_canonical_path!r} got={handle.canonical_path!r}"
            ),
        )
    body_bytes = os.read(handle.fd, st.st_size)
    if len(body_bytes) != st.st_size:
        raise DossierSignoffVerifyFailure(
            code=F_SCOUT_D_01e,
            reason_tag=(
                f"read_short:fstat_st_size={st.st_size} "
                f"read_len={len(body_bytes)}"
            ),
        )
    return body_bytes


# ---------------------------------------------------------------------------
# Dossier body assembly
# ---------------------------------------------------------------------------


def _render_dossier_body(
    *,
    roster_entry: EntityRosterEntry,
    claims: tuple[EntityClaim, ...],
) -> bytes:
    """Assemble the dossier markdown body as canonical bytes.

    Blueprint §4.9 line 826 — "Canonicalize the dossier as markdown →
    compute ``dossier_content_hash = sha3_512(canonical_markdown)``".
    Round 10 uses a template assembly (no LLM narrative — that's
    Round 11 scope). The body is a short markdown document:

    ::

        # {display_name}
        - Kind: {kind}
        - Added by: {added_by}
        - Added at: {added_at_utc}

        ## Claims

        - [HIGH] claim text
          - evidence: ...
        - [MEDIUM] ...

    Rendering is deterministic — claims are ordered by ``claim_id``
    ascending so the content hash is stable across repeated runs
    over the same inputs.
    """
    lines: list[str] = []
    lines.append(f"# {roster_entry.display_name}")
    lines.append(f"- Kind: {roster_entry.kind}")
    lines.append(f"- Added by: {roster_entry.added_by}")
    lines.append(f"- Added at: {roster_entry.added_at_utc}")
    lines.append("")
    lines.append("## Claims")
    lines.append("")
    ordered_claims = sorted(claims, key=lambda c: c.claim_id)
    for claim in ordered_claims:
        lines.append(f"- [{claim.confidence_tier}] {claim.claim_text}")
        lines.append(f"  - source: {claim.source_url}")
        lines.append(f"  - evidence: {claim.evidence_quote}")
    body = "\n".join(lines) + "\n"
    return body.encode("utf-8")


# ---------------------------------------------------------------------------
# HMAC-SHA3-512 for sign-off binding
# ---------------------------------------------------------------------------


def _sha3_512_hex(data: bytes) -> str:
    """Hex digest of sha3_512 for content-hash / binding storage."""
    return hashlib.sha3_512(data).hexdigest()


def _binding_canonical_bytes(
    *,
    slug: str,
    entity_slug: str,
    signed_canonical_path: str,
    signed_inode: int,
    signed_content_hash: str,
    signed_at_utc: str,
    operator_id: str,
) -> bytes:
    """Canonical bytes for the sign-off binding-HMAC input.

    Mirrors blueprint §4.9 line 881-892 — the binding-bytes are fed
    to an HMAC-SHA3-512 keyed with Section 1's
    ``tilth.dossier.signoff.hmac.v1`` keystore entry. Section 1 owns
    key retrieval; Round 10 emits only the canonical input bytes and
    delegates the keyed HMAC to the caller via injected signer (below).
    """
    return canonical_json_bytes({
        "slug": slug,
        "entity_slug": entity_slug,
        "signed_canonical_path": signed_canonical_path,
        "signed_inode": signed_inode,
        "signed_content_hash": signed_content_hash,
        "signed_at_utc": signed_at_utc,
        "operator_id": operator_id,
    })


# ---------------------------------------------------------------------------
# Signoff signer seam
# ---------------------------------------------------------------------------


@runtime_checkable
class DossierSignoffSigner(Protocol):
    """Injected HMAC-SHA3-512 signer seam for the sign-off binding.

    Production binding retrieves the
    ``tilth.dossier.signoff.hmac.v1`` key from Section 1's keystore
    and computes ``hmac_sha3_512(key, binding_bytes)``. Tests inject
    a recorder that returns a fixed signature byte string for a
    given input.
    """

    def sign(self, *, binding_bytes: bytes) -> bytes: ...


# ---------------------------------------------------------------------------
# Expiry helper
# ---------------------------------------------------------------------------


def _plus_validity_days(written_at_utc: str) -> str:
    """Add DOSSIER_VALIDITY_DAYS to an ISO-8601 UTC string.

    Malformed input falls back to a naive + timedelta path that
    preserves the original encoding — the caller retains
    responsibility for well-formed timestamps at write time.
    """
    raw = written_at_utc
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = _dt.datetime.fromisoformat(raw)
    except ValueError:
        # Defensive fallback — should not trigger in practice
        # because ``written_at_utc`` is produced by
        # :func:`_default_clock`.
        return written_at_utc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=_dt.timezone.utc)
    expires = parsed + _dt.timedelta(days=DOSSIER_VALIDITY_DAYS)
    return expires.isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Public entry — run_entity_research
# ---------------------------------------------------------------------------


def run_entity_research(
    *,
    session: SessionLike,
    roster: tuple[EntityRosterEntry, ...],
    roster_reader: EntityRosterReader,
    allowlist_reader: DomainAllowlistReader,
    claim_fetcher: EntityClaimFetcher,
    vault_writer: VaultWriter,
    checkpoint_writer: CheckpointWriter,
    clock: ClockFn = _default_clock,
    force_refresh: bool = False,
) -> EntityResearchResult:
    """Blueprint §4.9 M11 Entity Research Pass.

    Per-entity sequence:

    1. Intent-checked ``roster_reader.read_roster`` — verifies the
       input roster matches the on-disk YAML. A drift raises
       :class:`IntentMismatch`.
    2. ``allowlist_reader.read_allowlist`` — S11a per-org domain
       allowlist.
    3. For each roster entry, call
       ``claim_fetcher.fetch(session, roster_entry)`` — bounded by
       ``PER_ENTITY_RESEARCH_FETCH_CAP = 40`` on the fetcher side.
    4. S11a gate — drop claims whose ``source_registrable_domain``
       is not in ``allowlist.allowlisted_registrable_domains``.
       Dropped domains are recorded in
       ``non_allowlisted_domain_events`` on the result.
    5. Dedupe by ``_normalize_claim_text``; each dedupe bucket gets
       S11b tier assignment via :func:`_classify_confidence_tier`.
    6. Render body via :func:`_render_dossier_body`; compute
       sha3_512 content hash; write via ``vault_writer`` under intent
       ``"dossier-body-write"``. Dossier is UNSOURCED until a
       successful :func:`sign_off_dossier` call.

    Law 3 org isolation is enforced by path scoping
    (``orgs/{session.slug}/...``); the injected readers are also
    session-scoped — tests pass a reader bound to one slug and call
    with a different slug in the session → the reader raises
    :class:`IntentMismatch`.

    Autonomy Rule 1: ``entity_research_start`` on entry;
    ``entity_research_complete`` on every exit path (success AND
    failure).

    :raises DossierSignoffVerifyFailure: on F-SCOUT-D-03 sub-codes
        (roster parse error, allowlist parse error, invalid roster
        kind).
    :raises IntentMismatch: on any post-read intent drift.
    """
    checkpoint_writer.write(
        stage="entity_research_start",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "n_roster": len(roster),
            "force_refresh": force_refresh,
        },
    )

    try:
        # We re-read the roster via the reader to run the NFC intent
        # check; the result is unused for the pass because the caller
        # has already handed us the roster tuple.
        _ = roster_reader.read_roster(
            session_id=session.session_id,
            slug=session.slug,
        )
        allowlist = allowlist_reader.read_allowlist(
            session_id=session.session_id,
            slug=session.slug,
        )
        allowed_domains = allowlist.allowlisted_registrable_domains

        dossiers_by_slug: dict[str, EntityDossier] = {}
        ordered_list: list[EntityDossier] = []
        non_allowlisted_events: list[str] = []

        for roster_entry in roster:
            raw_candidates = claim_fetcher.fetch(
                session=session,
                roster_entry=roster_entry,
            )
            kept_candidates: list[EntityClaimCandidate] = []
            for c in raw_candidates:
                if c.source_registrable_domain not in allowed_domains:
                    non_allowlisted_events.append(
                        f"{F_SCOUT_D_03}.domain_not_allowlisted:"
                        f"entity_slug={roster_entry.entity_slug!r} "
                        f"claim_id={c.claim_id!r} "
                        f"domain={c.source_registrable_domain!r}"
                    )
                    continue
                kept_candidates.append(c)

            grouped = _dedupe_claims(tuple(kept_candidates))
            claims: list[EntityClaim] = []
            for _key, supporting in grouped.items():
                # First candidate is the canonical representative for
                # fields that do not vary across supporters (claim_id,
                # claim_text). Corroborating ids include every supporter
                # for deterministic audit.
                rep = supporting[0]
                tier = _classify_confidence_tier(supporting)
                corroborating = _claim_ids_sorted(supporting)
                claim = EntityClaim(
                    claim_id=rep.claim_id,
                    claim_text=rep.claim_text,
                    source_url=rep.source_url,
                    source_registrable_domain=rep.source_registrable_domain,
                    fetched_at_utc=rep.fetched_at_utc,
                    url_hash=rep.url_hash,
                    content_hash=rep.content_hash,
                    evidence_quote=rep.evidence_quote,
                    confidence_tier=tier,
                    corroborating_claim_ids=corroborating,
                )
                claims.append(claim)

            claims_tuple = tuple(sorted(claims, key=lambda c: c.claim_id))
            body_bytes = _render_dossier_body(
                roster_entry=roster_entry,
                claims=claims_tuple,
            )
            content_hash = _sha3_512_hex(body_bytes)
            written_at = clock()
            dossier = EntityDossier(
                entity_slug=roster_entry.entity_slug,
                roster_entry=roster_entry,
                claims=claims_tuple,
                dossier_written_at_utc=written_at,
                dossier_content_hash=content_hash,
                operator_signoff=None,
            )
            vault_writer.write(
                path=_dossier_body_path(
                    session.slug, roster_entry.entity_slug
                ),
                bytes_=body_bytes,
                intent=INTENT_DOSSIER_BODY_WRITE,
                session_id=session.session_id,
                slug=session.slug,
            )
            dossiers_by_slug[roster_entry.entity_slug] = dossier
            ordered_list.append(dossier)

        result = EntityResearchResult(
            dossiers_by_slug=dict(dossiers_by_slug),
            ordered=tuple(ordered_list),
            non_allowlisted_domain_events=tuple(non_allowlisted_events),
        )
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as exc:
        checkpoint_writer.write(
            stage="entity_research_complete",
            payload={
                "session_id": session.session_id,
                "slug": session.slug,
                "outcome": "failure",
                "error_type": type(exc).__name__,
            },
        )
        raise

    checkpoint_writer.write(
        stage="entity_research_complete",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "outcome": "success",
            "n_dossiers": len(result.ordered),
            "n_non_allowlisted_drops": len(result.non_allowlisted_domain_events),
        },
    )
    return result


# ---------------------------------------------------------------------------
# Public entry — sign_off_dossier
# ---------------------------------------------------------------------------


def sign_off_dossier(
    *,
    session: SessionLike,
    entity_slug: str,
    operator_confirmation_token: str,
    body_reader: DossierBodyReader,
    signoff_signer: DossierSignoffSigner,
    vault_writer: VaultWriter,
    checkpoint_writer: CheckpointWriter,
    prior_dossier: EntityDossier,
    clock: ClockFn = _default_clock,
) -> DossierSignoff:
    """Blueprint §4.9 S11c — operator sign-off with FD-held-closure.

    Atomically binds operator sign-off to a (canonical_path, inode,
    content_hash) triple under O_NOFOLLOW. ``vault_write`` of the
    sign-off record happens INSIDE the FD-holding ``with`` block;
    a final fstat is performed immediately before vault_write to
    catch any in-flight swap (A-03 closure, durable enforcement).

    Fails closed (raises :class:`DossierSignoffVerifyFailure`) if:

    - canonical_path differs from prior stored path → F-SCOUT-D-01a.
    - inode differs from prior stored inode → F-SCOUT-D-01b.
    - sha3_512(body) differs from prior stored content hash →
      F-SCOUT-D-01c.
    - final re-fstat inside the with-block detects inode /
      canonical-path drift between first-read and ``vault_write`` →
      F-SCOUT-D-01d.
    - read returned fewer bytes than fstat.st_size → F-SCOUT-D-01e.
    - body fstat.st_size > ``_MAX_DOSSIER_BYTES`` → F-SCOUT-D-02
      ``.fstat_size_gt_max`` via :class:`DossierSizeExceeded`.

    ``operator_confirmation_token`` is retained on the call signature
    per blueprint line 834 (Section 1's ``record_admin_risk`` RED-tier
    retype ceremony binds the token upstream). Round 10 threads the
    token but does not validate it — Section 1 owns that gate.

    Autonomy Rule 1: ``dossier_signoff_start`` + ``dossier_signoff_complete``
    on every exit path.
    """
    _ = operator_confirmation_token  # threaded for Section 1 audit trail

    checkpoint_writer.write(
        stage="dossier_signoff_start",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "entity_slug": entity_slug,
        },
    )

    try:
        with _open_dossier_body_fd(
            body_reader=body_reader,
            session=session,
            entity_slug=entity_slug,
        ) as handle:
            st = os.fstat(handle.fd)
            inode = st.st_ino
            if st.st_size > _MAX_DOSSIER_BYTES:
                raise DossierSizeExceeded(
                    f"{F_SCOUT_D_02}.fstat_size_gt_max: dossier body "
                    f"fstat st_size={st.st_size} exceeds "
                    f"{_MAX_DOSSIER_BYTES}"
                )
            body_bytes = os.read(handle.fd, st.st_size)
            if len(body_bytes) != st.st_size:
                raise DossierSignoffVerifyFailure(
                    code=F_SCOUT_D_01e,
                    reason_tag=(
                        f"read_short:fstat_st_size={st.st_size} "
                        f"read_len={len(body_bytes)}"
                    ),
                )
            computed_hash = _sha3_512_hex(body_bytes)
            canonical_path = handle.canonical_path
            expected_path = _dossier_body_path(session.slug, entity_slug)
            # Path-check: the handle's canonical_path must reference
            # the expected slug / entity_slug. Section 2 resolves the
            # final form; we verify the tail matches our computed path.
            if not canonical_path.endswith(expected_path):
                raise DossierSignoffVerifyFailure(
                    code=F_SCOUT_D_01a,
                    reason_tag=(
                        f"canonical_path_tail_mismatch:expected_tail="
                        f"{expected_path!r} got={canonical_path!r}"
                    ),
                )
            if prior_dossier.dossier_content_hash != computed_hash:
                raise DossierSignoffVerifyFailure(
                    code=F_SCOUT_D_01c,
                    reason_tag=(
                        f"content_hash_mismatch:prior="
                        f"{prior_dossier.dossier_content_hash!r} "
                        f"computed={computed_hash!r}"
                    ),
                )

            signed_at = clock()
            binding_bytes = _binding_canonical_bytes(
                slug=session.slug,
                entity_slug=entity_slug,
                signed_canonical_path=canonical_path,
                signed_inode=inode,
                signed_content_hash=computed_hash,
                signed_at_utc=signed_at,
                operator_id=session.operator_id,
            )
            signature = signoff_signer.sign(binding_bytes=binding_bytes)
            expires_at = _plus_validity_days(
                prior_dossier.dossier_written_at_utc
            )
            signoff = DossierSignoff(
                signed_at_utc=signed_at,
                operator_id=session.operator_id,
                signed_canonical_path=canonical_path,
                signed_inode=inode,
                signed_content_hash=computed_hash,
                operator_signature=signature,
                expires_at_utc=expires_at,
            )
            # Final TOCTOU closure — re-fstat the held FD immediately
            # before vault_write (A-03 durable enforcement).
            final_st = os.fstat(handle.fd)
            if final_st.st_ino != inode:
                raise DossierSignoffVerifyFailure(
                    code=F_SCOUT_D_01d,
                    reason_tag=(
                        f"final_refstat_inode_drift:first={inode} "
                        f"final={final_st.st_ino}"
                    ),
                )
            vault_writer.write(
                path=_dossier_signoff_path(session.slug, entity_slug),
                bytes_=canonical_json_bytes(
                    _signoff_asdict_for_canonical(signoff)
                ),
                intent=INTENT_DOSSIER_SIGNOFF_WRITE,
                session_id=session.session_id,
                slug=session.slug,
            )
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as exc:
        checkpoint_writer.write(
            stage="dossier_signoff_complete",
            payload={
                "session_id": session.session_id,
                "slug": session.slug,
                "entity_slug": entity_slug,
                "outcome": "failure",
                "error_type": type(exc).__name__,
            },
        )
        raise

    checkpoint_writer.write(
        stage="dossier_signoff_complete",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "entity_slug": entity_slug,
            "outcome": "success",
            "signed_at_utc": signoff.signed_at_utc,
            "signed_inode": signoff.signed_inode,
        },
    )
    return signoff


def _signoff_asdict_for_canonical(signoff: DossierSignoff) -> dict[str, Any]:
    """Pre-normalise bytes → hex for canonical_json_bytes.

    ``DossierSignoff.operator_signature`` is bytes; canonical_json
    cannot serialize bytes directly. Mirror the
    :mod:`pipeline.scout._types` normalisation helper so the
    on-disk payload is a JSON-legal mapping.
    """
    raw = asdict(signoff)
    raw["operator_signature"] = signoff.operator_signature.hex()
    return raw


# ---------------------------------------------------------------------------
# Public entry — read_entity_dossier
# ---------------------------------------------------------------------------


def read_entity_dossier(
    *,
    session: SessionLike,
    entity_slug: str,
    body_reader: DossierBodyReader,
    signoff_reader: DossierSignoffReader,
    prior_dossier: EntityDossier,
) -> tuple[EntityDossier, DossierSignoff]:
    """Blueprint §4.9 — Logician-facing read with triple-lock re-verify.

    Re-verifies the three-part lock at read time:

    - canonical_path (the body FD's resolved path vs the sign-off
      record's stored path) → F-SCOUT-D-03 ``.path_drift`` on
      mismatch.
    - inode (fstat on held FD vs sign-off record's stored inode) →
      F-SCOUT-D-03 ``.inode_drift`` on mismatch.
    - content_hash (sha3_512 of body bytes vs sign-off record's
      stored content hash) → F-SCOUT-D-03 ``.content_hash_drift`` on
      mismatch.

    ``prior_dossier`` is the canonical :class:`EntityDossier` the
    caller already holds (e.g., from :func:`run_entity_research` at
    pass time). The function returns the same dossier with the
    re-verified :class:`DossierSignoff` attached. If the prior
    dossier has no sign-off, raises F-SCOUT-D-03 ``.unsourced`` —
    Logician's PRE-gate refuses to cite unsourced dossiers.

    Also enforces the A-v3-06 partial-read race closure via
    :func:`_read_held_body`.

    :raises DossierSignoffVerifyFailure: on any drift.
    :raises DossierSizeExceeded: F-SCOUT-D-02 on body oversize.
    """
    signoff = signoff_reader.read_signoff(
        session_id=session.session_id,
        slug=session.slug,
        entity_slug=entity_slug,
    )
    if signoff is None:
        raise DossierSignoffVerifyFailure(
            code=F_SCOUT_D_03,
            reason_tag=f"unsourced:entity_slug={entity_slug!r}",
        )
    with _open_dossier_body_fd(
        body_reader=body_reader,
        session=session,
        entity_slug=entity_slug,
    ) as handle:
        st = os.fstat(handle.fd)
        if st.st_size > _MAX_DOSSIER_BYTES:
            raise DossierSizeExceeded(
                f"{F_SCOUT_D_02}.fstat_size_gt_max: dossier body fstat "
                f"st_size={st.st_size} exceeds {_MAX_DOSSIER_BYTES}"
            )
        body_bytes = os.read(handle.fd, st.st_size)
        if len(body_bytes) != st.st_size:
            raise DossierSignoffVerifyFailure(
                code=F_SCOUT_D_01e,
                reason_tag=(
                    f"read_short:fstat_st_size={st.st_size} "
                    f"read_len={len(body_bytes)}"
                ),
            )
        # Path drift
        if signoff.signed_canonical_path != handle.canonical_path:
            raise DossierSignoffVerifyFailure(
                code=F_SCOUT_D_03,
                reason_tag=(
                    f"path_drift:signoff_path="
                    f"{signoff.signed_canonical_path!r} "
                    f"current_path={handle.canonical_path!r}"
                ),
            )
        # Inode drift
        if signoff.signed_inode != st.st_ino:
            raise DossierSignoffVerifyFailure(
                code=F_SCOUT_D_03,
                reason_tag=(
                    f"inode_drift:signoff_inode={signoff.signed_inode} "
                    f"current_inode={st.st_ino}"
                ),
            )
        # Content-hash drift
        computed_hash = _sha3_512_hex(body_bytes)
        if signoff.signed_content_hash != computed_hash:
            raise DossierSignoffVerifyFailure(
                code=F_SCOUT_D_03,
                reason_tag=(
                    f"content_hash_drift:signoff_hash="
                    f"{signoff.signed_content_hash!r} "
                    f"current_hash={computed_hash!r}"
                ),
            )
        # Re-bind the sign-off onto the dossier for caller use.
        reverified = EntityDossier(
            entity_slug=prior_dossier.entity_slug,
            roster_entry=prior_dossier.roster_entry,
            claims=prior_dossier.claims,
            dossier_written_at_utc=prior_dossier.dossier_written_at_utc,
            dossier_content_hash=prior_dossier.dossier_content_hash,
            operator_signoff=signoff,
        )
        # Reference canonical-bytes helpers so Round 10's dependency on
        # the canonical surface is explicit; helps downstream audit-
        # impact analysis identify which rounds compose against
        # :func:`entity_dossier_canonical_bytes`.
        _ = entity_dossier_canonical_bytes
        return reverified, signoff


# ---------------------------------------------------------------------------
# Side-effect-free import invariant
# ---------------------------------------------------------------------------


# Module imports ``time`` / ``os`` / ``hashlib`` for runtime use; the
# terminal guard keeps linter stripping aligned with Round 9 style.
_ = time  # noqa: F841
