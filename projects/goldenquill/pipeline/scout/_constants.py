"""Scout package constants — pinned numeric + policy + intent strings.

Every constant here is a `Final[...]`. Values match `pipeline/blueprint/v0.1/
section_03_scout.md` §8 (numeric pins) and §2 / §3.3 / §9 (string literals).

Scope: Round 1 of the Section 3 Scout build. Declarative only — no runtime
behaviour. Sibling Scout rounds import from here; Pipeline (§5) and Logician
(§4) consume via the public ``pipeline.scout`` re-export.

Blueprint anchors: §2 (enum domains), §3.3 (vault intents), §8 (numeric
pins), §9 (LLM-call boundary table).
"""

from __future__ import annotations

from typing import Final


# ---------------------------------------------------------------------------
# §8 — pinned numeric + policy constants
# ---------------------------------------------------------------------------

CHANNEL_A_CONNECT_TIMEOUT_S: Final[int] = 10
CHANNEL_A_READ_TIMEOUT_S: Final[int] = 30
CHANNEL_A_RETRY_COUNT: Final[int] = 3

VERIFY_LIVE_SYNOPSIS_TIMEOUT_S: Final[int] = 10
VERIFY_POOL_MAX_WORKERS: Final[int] = 4

DISCOVER_POOL_MAX_WORKERS: Final[int] = 6
DISCOVER_PER_CHANNEL_HARD_TIMEOUT_S: Final[int] = 120

CACHE_WATERMARK_DEGRADED_DAYS: Final[int] = 14
RSS_STALE_FEED_DEGRADED_DAYS: Final[int] = 60

CHANNEL_E_RUNAWAY_MAX: Final[int] = 100
CHANNEL_D_MAX_CANDIDATES_PER_PAGE: Final[int] = 200
CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER: Final[int] = 500

SCOUT_CANDIDATE_VERIFY_CAP: Final[int] = 1000
SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO: Final[float] = 0.25
SCOUT_REVIEW_LOCK_STRIPES: Final[int] = 64

FEED_POLL_MIN_INTERVAL_MIN: Final[int] = 15

SESSION_HMAC_KEY_LEN_BYTES: Final[int] = 64

CANDIDATE_ID_HEX_LEN: Final[int] = 24
RUN_ID_HEX_LEN: Final[int] = 24
CLAIM_ID_HEX_LEN: Final[int] = 24

MAX_DOSSIER_BYTES: Final[int] = 5 * 1024 * 1024
DOSSIER_VALIDITY_DAYS: Final[int] = 90
PER_ENTITY_RESEARCH_FETCH_CAP: Final[int] = 40
HIGH_CONFIDENCE_DISTINCT_DOMAIN_REQUIREMENT: Final[int] = 2

ROTATION_GRACE_WINDOW_S: Final[int] = 5


# ---------------------------------------------------------------------------
# §2.1 Candidate.channel domain
# ---------------------------------------------------------------------------

CHANNEL_A: Final[str] = "A"
CHANNEL_B: Final[str] = "B"
CHANNEL_C: Final[str] = "C"
CHANNEL_D: Final[str] = "D"
CHANNEL_E: Final[str] = "E"
CHANNEL_F: Final[str] = "F"


# ---------------------------------------------------------------------------
# §2.2 VerificationVerdict.verdict domain
# ---------------------------------------------------------------------------

VERDICT_VERIFIED_FIT: Final[str] = "VERIFIED_FIT"
VERDICT_VERIFIED_NOT_FIT: Final[str] = "VERIFIED_NOT_FIT"
VERDICT_UNVERIFIED: Final[str] = "UNVERIFIED"
VERDICT_VERIFICATION_FAILED: Final[str] = "VERIFICATION_FAILED"


# ---------------------------------------------------------------------------
# §2.4 ReviewQueueItem.operator_decision domain
# ---------------------------------------------------------------------------

DECISION_ACCEPT: Final[str] = "ACCEPT"
DECISION_REJECT: Final[str] = "REJECT"
DECISION_HOLD: Final[str] = "HOLD"


# ---------------------------------------------------------------------------
# §2.3 HealthTuple.channel_{a..f} domain
# ---------------------------------------------------------------------------

HEALTH_OK: Final[str] = "OK"
HEALTH_DEGRADED: Final[str] = "DEGRADED"
HEALTH_FAILED: Final[str] = "FAILED"


# ---------------------------------------------------------------------------
# §2.1 Candidate.funder_kind domain
# ---------------------------------------------------------------------------

FUNDER_FEDERAL: Final[str] = "federal"
FUNDER_STATE: Final[str] = "state"
FUNDER_FOUNDATION: Final[str] = "foundation"
FUNDER_INTERMEDIARY: Final[str] = "intermediary"
FUNDER_UNKNOWN: Final[str] = "unknown"


# ---------------------------------------------------------------------------
# §2.5 EntityRosterEntry.kind domain (D.0 taxonomy)
# ---------------------------------------------------------------------------

ENTITY_KIND_PERSON_LEAD: Final[str] = "person_lead"
ENTITY_KIND_PERSON_PARTNER: Final[str] = "person_partner"
ENTITY_KIND_PERSON_REFERENCED: Final[str] = "person_referenced"
ENTITY_KIND_ORG_APPLICANT: Final[str] = "org_applicant"
ENTITY_KIND_ORG_PARTNER: Final[str] = "org_partner"
ENTITY_KIND_ORG_REFERENCED: Final[str] = "org_referenced"
ENTITY_KIND_PRODUCT: Final[str] = "product"
ENTITY_KIND_PUBLICATION: Final[str] = "publication"


# ---------------------------------------------------------------------------
# §2.5 EntityClaim.confidence_tier domain (S11b)
# ---------------------------------------------------------------------------

CONFIDENCE_HIGH: Final[str] = "HIGH"
CONFIDENCE_MEDIUM: Final[str] = "MEDIUM"
CONFIDENCE_LOW: Final[str] = "LOW"


# ---------------------------------------------------------------------------
# §2.5 EntityRosterEntry.added_by domain
# ---------------------------------------------------------------------------

ROSTER_ADDED_BY_OPERATOR: Final[str] = "operator"
ROSTER_ADDED_BY_SCOUT_PROPOSAL: Final[str] = "scout_proposal_accepted"


# ---------------------------------------------------------------------------
# §2.1 Candidate.feed_or_adapter_id prefixes (A-v3-09)
#
# Call sites compose the full value as f"{FEED_PREFIX_X}:{source_key}".
# The colon lives at the composition site, not in the constant.
# ---------------------------------------------------------------------------

FEED_PREFIX_API: Final[str] = "api"
FEED_PREFIX_CACHE: Final[str] = "cache"
FEED_PREFIX_PORTAL: Final[str] = "portal"
FEED_PREFIX_ALN: Final[str] = "aln"
FEED_PREFIX_RSS: Final[str] = "rss"
FEED_PREFIX_SEARXNG: Final[str] = "searxng"
FEED_PREFIX_BRAVE: Final[str] = "brave"


# ---------------------------------------------------------------------------
# §3.3 + §9 — vault_read / vault_write intent strings
# ---------------------------------------------------------------------------

INTENT_READ: Final[str] = "read"
INTENT_CHANNEL_F_POLICY_READ: Final[str] = "channel-f-policy-read"
INTENT_REVIEW_QUEUE_WRITE: Final[str] = "review-queue-write"
INTENT_REVIEW_QUEUE_READ: Final[str] = "review-queue-read"
INTENT_SOURCE_ALLOWLIST_READ: Final[str] = "source-allowlist-read"
INTENT_ENTITY_ROSTER_READ: Final[str] = "entity-roster-read"
INTENT_DOSSIER_BODY_WRITE: Final[str] = "dossier-body-write"
INTENT_DOSSIER_BODY_READ: Final[str] = "dossier-body-read"
INTENT_DOSSIER_SIGNOFF_WRITE: Final[str] = "dossier-signoff-write"
INTENT_DOSSIER_SIGNOFF_READ: Final[str] = "dossier-signoff-read"
INTENT_SCOUT_RUN_LOG_WRITE: Final[str] = "scout-run-log-write"

# Spec-card nomenclature alias — §4.9 references ``SCOUT_DOSSIER_MAX_BYTES``
# while blueprint §8 table + body refer to ``_MAX_DOSSIER_BYTES`` /
# ``MAX_DOSSIER_BYTES``. Both names bind to the identical integer so code
# paths spec-card-style-imported and blueprint-style-imported see the
# same pin. 5 MB strict `>` boundary per A-13.
SCOUT_DOSSIER_MAX_BYTES: Final[int] = MAX_DOSSIER_BYTES
