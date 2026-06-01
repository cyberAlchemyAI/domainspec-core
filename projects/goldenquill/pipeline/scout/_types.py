"""Scout package data schemas — §2.1..§2.7 of section_03_scout.md.

Eleven frozen, keyword-only dataclasses, plus four free-function canonical-
bytes helpers used by sibling rounds' signing call-sites. No validation beyond
what Python dataclasses provide natively — per-channel invariants (feed prefix
matching, intent domain checks, etc.) are enforced at each channel module's
construction boundary in later rounds.

Blueprint anchors:
- §2.1 Candidate
- §2.2 VerificationVerdict
- §2.3 HealthTuple + SignedHealthTuple
- §2.4 ReviewQueueItem
- §2.5 EntityRosterEntry + EntityClaim + EntityDossier + DossierSignoff
- §2.6 SourceDomainAllowlist (S11a)
- §2.7 ChannelFJurisdictionPolicy (BT12)
- §2.3 note: canonical bytes use sorted-key JSON so verifier canonicalization
  is bit-identical to signer canonicalization
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from pipeline.sovereignty import canonical_json_bytes


# ---------------------------------------------------------------------------
# §2.1 Candidate — DISCOVER-stage row from any of Channels A..F
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class Candidate:
    candidate_id: str
    channel: str
    feed_or_adapter_id: str
    source_key: str
    title: str
    funder: str
    funder_kind: str
    url: str
    close_date_utc: Optional[str]
    award_ceiling: Optional[int]
    award_floor: Optional[int]
    applicant_types: tuple[str, ...]
    program_page_url: Optional[str]
    fetch_timestamp_utc: str
    url_hash: str
    content_hash: Optional[str]
    fit_score_cached: int
    cache_provenance: Optional[str]


# ---------------------------------------------------------------------------
# §2.2 VerificationVerdict — VERIFY-stage output per Candidate
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class VerificationVerdict:
    candidate_id: str
    verdict: str
    reason_code: str
    live_synopsis_url: Optional[str]
    live_content_hash: Optional[str]
    fetched_at_utc: Optional[str]
    timeout_seconds: int
    eligibility_live: tuple[str, ...]
    award_floor_live: Optional[int]
    award_ceiling_live: Optional[int]
    close_date_live_utc: Optional[str]
    evidence_quote: Optional[str]


# ---------------------------------------------------------------------------
# §2.3 HealthTuple + SignedHealthTuple — M7 per-run health signing surface
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class HealthTuple:
    session_id: str
    slug: str
    run_id: str
    run_wall_ns: int
    channel_a: str
    channel_b: str
    channel_c: str
    channel_d: str
    channel_e: str
    channel_f: str
    channel_a_endpoints: dict[str, str]
    backbone_failed: bool
    # §4.10 body adds a run_entropy audit-replay field that the §2.3 table
    # does not list. Round 2 lands the field here (Option A of the Round 2
    # spec card) so the signer and the Section 4 verifier canonicalize the
    # same schema. F-BLUEPRINT-DRIFT noted in the Round 2 LOCK memory —
    # §2.3 table is the stale side; the §4.10 body is authoritative.
    run_entropy: dict[str, object]


@dataclass(frozen=True, kw_only=True)
class SignedHealthTuple:
    tuple_canonical: bytes
    hmac_sha3_512: bytes
    signed_at_utc: str
    hmac_key_id: str


# ---------------------------------------------------------------------------
# §2.4 ReviewQueueItem — human-gate payload
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ReviewQueueItem:
    candidate_id: str
    queued_at_utc: str
    queued_by_verdict: str
    candidate_snapshot: Candidate
    verification_snapshot: VerificationVerdict
    fit_rationale: str
    operator_decision: Optional[str]
    operator_decided_at_utc: Optional[str]
    operator_decision_reason: Optional[str]


# ---------------------------------------------------------------------------
# §2.5 EntityRosterEntry + EntityClaim + EntityDossier + DossierSignoff
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class EntityRosterEntry:
    entity_slug: str
    display_name: str
    kind: str
    seed_urls: tuple[str, ...]
    added_by: str
    added_at_utc: str


@dataclass(frozen=True, kw_only=True)
class EntityClaim:
    claim_id: str
    claim_text: str
    source_url: str
    source_registrable_domain: str
    fetched_at_utc: str
    url_hash: str
    content_hash: str
    evidence_quote: str
    confidence_tier: str
    corroborating_claim_ids: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class DossierSignoff:
    signed_at_utc: str
    operator_id: str
    signed_canonical_path: str
    signed_inode: int
    signed_content_hash: str
    operator_signature: bytes
    expires_at_utc: str


@dataclass(frozen=True, kw_only=True)
class EntityDossier:
    entity_slug: str
    roster_entry: EntityRosterEntry
    claims: tuple[EntityClaim, ...]
    dossier_written_at_utc: str
    dossier_content_hash: str
    operator_signoff: Optional[DossierSignoff]


# ---------------------------------------------------------------------------
# §2.6 SourceDomainAllowlist — S11a per-org domain allowlist
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SourceDomainAllowlist:
    slug: str
    allowlisted_registrable_domains: frozenset[str]
    last_updated_at_utc: str
    last_updated_by_operator_id: str


# ---------------------------------------------------------------------------
# §2.7 ChannelFJurisdictionPolicy — BT12 per-org policy
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ChannelFJurisdictionPolicy:
    slug: str
    opt_in: bool
    allowed_jurisdictions: frozenset[str]
    disallowed_registrable_domains: frozenset[str]
    last_updated_at_utc: str


# ---------------------------------------------------------------------------
# Canonical-bytes helpers
#
# Used by sibling Scout rounds to produce the exact byte string that goes
# under HMAC / SHA3 (§2.3 invariant: signer and verifier canonicalize
# identically). `_normalize_for_json` rewrites container types that
# `json.dumps` cannot serialize natively (bytes → hex; frozenset/set →
# sorted list) while leaving JSON-native types untouched. Ordering under
# `sort_keys=True` in `canonical_json_bytes` covers dict-key determinism.
# ---------------------------------------------------------------------------


def _normalize_for_json(obj: object) -> object:
    """Recursively rewrite a container so every node is JSON-serializable.

    Rules (applied before `json.dumps`):
    * ``bytes`` → lowercase hex string.
    * ``frozenset`` / ``set`` → sorted list (stable across invocations).
    * ``tuple`` / ``list`` → list of normalized elements.
    * ``dict`` → dict with normalized values (keys left untouched; callers
      that use non-string keys must stringify upstream).

    Other types pass through unchanged. Callers pair this with
    ``canonical_json_bytes`` which supplies ``sort_keys=True`` +
    ``separators=(",", ":")`` + UTF-8 for full byte-determinism.
    """
    if isinstance(obj, bytes):
        return obj.hex()
    if isinstance(obj, (frozenset, set)):
        return sorted(_normalize_for_json(x) for x in obj)
    if isinstance(obj, (list, tuple)):
        return [_normalize_for_json(x) for x in obj]
    if isinstance(obj, dict):
        return {key: _normalize_for_json(value) for key, value in obj.items()}
    return obj


def health_tuple_canonical_bytes(tuple_: HealthTuple) -> bytes:
    """Canonical bytes for M7 HMAC signing (§2.3)."""
    return canonical_json_bytes(_normalize_for_json(asdict(tuple_)))


def candidate_canonical_bytes(candidate: Candidate) -> bytes:
    """Canonical bytes for Candidate hashing / dedup keys."""
    return canonical_json_bytes(_normalize_for_json(asdict(candidate)))


def entity_dossier_canonical_bytes(dossier: EntityDossier) -> bytes:
    """Canonical bytes for dossier content hashing (§2.5)."""
    return canonical_json_bytes(_normalize_for_json(asdict(dossier)))


def dossier_signoff_canonical_bytes(signoff: DossierSignoff) -> bytes:
    """Canonical bytes for dossier sign-off verification (§2.5 / S11c)."""
    return canonical_json_bytes(_normalize_for_json(asdict(signoff)))
