"""pipeline.cards.models — Pydantic models for Cards.

Mirrors the JSON schemas at pipeline/cards/_schema/:
  - card_cic.schema.json
  - card_clc.schema.json
  - pipeline/cards/matrix/_schema/card_matrix.schema.json

Per architecture v7.0.11 §1.3 — schema versions track via SchemaVersion enum;
additive non-breaking changes bump minor; field removal or semantic redefinition
bumps major and triggers a paired §0.5 amendment.

DRAFT at v0.1 LOCK candidate state. Body landings graduate fully validated at
v0.2 first wave per architecture v7.0.11 §5. The dataclass shapes below are
LOCK-ready; field-level validation lives in pipeline/cards/validators.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Optional


# Canonical slug enumerations — must match the schema files byte-for-byte.
# Loader fails closed F-CARDS-SCHEMA-INVALID on any card with an
# off-enum slug.

CIC_SLUGS: frozenset[str] = frozenset({
    "food_systems",
    "educator",
    "public_agency",
    "arts_culture",
    "cooperative",
    "ecosystem_intermediary",
})

CLC_SLUGS: frozenset[str] = frozenset({
    "public_purpose_works",
    "catalytic_change",
    "operating_capacity",
    "research_evidence",
    "market_access",
    "credit_underwriting",
    "sponsorship_corporate",
    "shared_assets",
})

COVERAGE_AXES: frozenset[str] = frozenset({
    "Production",
    "Learning",
    "Public Sector",
    "Culture",
    "Member Ownership",
    "Intermediary Infrastructure",
})


# --- Lifecycle ---------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class Lifecycle:
    """Card lifecycle state block. Per architecture v7.0.11 §1.4.

    ``draft_status`` is the canonical state machine. ``runtime_loadable`` is
    the runtime truth flag. Loader preflight enforces:
      - draft_status != "signed" -> runtime_loadable must be False
      - runtime_loadable is True -> draft_status == "signed" and signed_*
        metadata + content_hash are present and valid
      - draft_status == "draft" -> loader rejects the card
    """

    draft_status: Literal["draft", "review_passed", "signed", "deprecated"]
    review_status: Literal["pending", "passed", "changes_requested"]
    cross_family_thesis_status: Literal["pending", "passed", "failed"]
    signature_status: Literal["unsigned", "signed", "revoked"]
    runtime_load_status: Literal["not_loaded", "loaded", "disabled"]
    runtime_loadable: bool
    signed_at: Optional[str] = None
    signed_by: Optional[str] = None
    content_hash: Optional[str] = None


# --- Research metadata -------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class ResearchMetadata:
    """Per-card research provenance block. Phase 5 review handback shape
    per blueprint §18.11."""

    authored_at: str                                  # ISO 8601
    authored_by_role: str                             # research_session | internal_editor | platform_team
    research_budget_hours_actual: float = 0.0
    priors_consulted: tuple[Mapping[str, str], ...] = ()
    primary_sources: tuple[Mapping[str, str], ...] = ()
    ed25519_signature: Optional[str] = None           # hex-encoded signature on canonical-JSON bytes


# --- CIC card -----------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class CICCard:
    """Customer Identity Card card — applicant-side runtime knowledge.

    Forbidden field names (per architecture v7.0.11 §6.1 + §4 v2.x
    F-CARDS-COUPLING-VIOLATION-EXTENSION):
        common_clc_patterns_observed, eligible_clc_subset, clc_allowlist,
        clc_denylist, preferred_clcs, clc_win_rate, clc_ranking_preferences.

    Loader fails closed F-CARDS-COUPLING-VIOLATION-EXTENSION on any
    YAML card body containing any of these as top-level keys.
    """

    schema_version: Literal["1.0-cic"]
    card_axis: Literal["CIC"]
    card_id: str                                      # ^TILTH-CIC-\d{2}$
    slug: str                                         # in CIC_SLUGS
    display_name: str
    display_name_short: Optional[str] = None          # arch v7.0.11 §7.2; loader resolves to display_name when None
    coverage_axis: str                                # in COVERAGE_AXES
    nickname: Optional[str] = None
    tilth_cic_id: str

    search_vocabulary: Mapping[str, Any]
    evidence_signals: tuple[Mapping[str, Any], ...] = ()
    kfr_fact_classes: tuple[Mapping[str, Any], ...] = ()
    provenance_requirements: Mapping[str, Any] = field(default_factory=dict)
    register_defaults: Mapping[str, Any]
    dialect_routing_table: tuple[Mapping[str, Any], ...] = ()
    admin_risk_term_register: tuple[Mapping[str, Any], ...] = ()
    reporting_cadence_typical: Mapping[str, Any]
    metrics_table_template: tuple[Mapping[str, Any], ...] = ()
    narrative_sections_typical: tuple[str, ...] = ()
    capacity_signals_required: tuple[Mapping[str, Any], ...] = ()
    compliance_burdens: tuple[Mapping[str, Any], ...] = ()
    common_risk_register_entries: tuple[Mapping[str, Any], ...] = ()
    common_funders_observed: tuple[Mapping[str, Any], ...] = ()

    lifecycle: Lifecycle
    research_metadata: ResearchMetadata


# --- CLC card -----------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class CLCCard:
    """Capital Logic Card card — funder-side underwriting knowledge.

    Forbidden field names (per architecture v7.0.11 §6.1 + §4 v2.x
    F-CARDS-COUPLING-VIOLATION-EXTENSION):
        eligible_cic_subset, cic_allowlist, cic_denylist, preferred_cics,
        cic_win_rate, cic_ranking_preferences.
    """

    schema_version: Literal["1.0-clc"]
    card_axis: Literal["CLC"]
    card_id: str                                      # ^TILTH-CLC-\d{2}$
    slug: str                                         # in CLC_SLUGS
    display_name: str
    funding_mechanism_summary: str
    tilth_clc_id: str

    underwriting_criteria: tuple[Mapping[str, Any], ...]
    scoring_weight_patterns: tuple[Mapping[str, Any], ...] = ()
    evidence_weights: Mapping[str, Any]
    common_application_forms: tuple[Mapping[str, Any], ...] = ()
    narrative_section_patterns: tuple[Mapping[str, Any], ...] = ()
    budget_structure_conventions: Mapping[str, Any] = field(default_factory=dict)
    reviewer_profile_typical: Mapping[str, Any]
    common_portals: tuple[Mapping[str, Any], ...] = ()
    common_red_flags: tuple[Mapping[str, Any], ...]
    reporting_requirements_typical: Mapping[str, Any]
    compliance_obligations: tuple[Mapping[str, Any], ...] = ()
    commitment_tracking_pattern: Mapping[str, Any]

    lifecycle: Lifecycle
    research_metadata: ResearchMetadata


# --- Matrix card (forward-compat at v7.0.11 LOCK) -----------------------

@dataclass(frozen=True, kw_only=True)
class MatrixCard:
    """CIC × CLC matrix card — FORWARD-COMPAT ONLY at v7.0.11 LOCK.

    Per architecture v7.0.11 §1.8: no populated matrix content ships before
    the v1.x matrix-phase explicit amendment. status MUST be
    'FORWARD_COMPAT_ONLY' and binding_eligibility MUST be False at v0.1 Beta.
    Loader fails closed F-CARDS-COUPLING-VIOLATION-EXTENSION on any populated
    matrix card encountered before the v1_x_matrix_phase_active runtime
    feature flag flips.
    """

    schema_version: Literal["1.0-cic-clc-matrix"]
    status: Literal["FORWARD_COMPAT_ONLY"]
    card_axis: Literal["MATRIX"]
    cic_slug: str
    clc_slug: str
    intersection_id: str
    binding_eligibility: Literal[False]
    allowed_runtime_readers: tuple[str, ...]
    forbidden_runtime_readers_during_eligibility: tuple[str, ...]

    historical_match_pattern: Mapping[str, Any] = field(default_factory=dict)
    boundary_strategies: tuple[Mapping[str, Any], ...] = ()
    framing_pivots: tuple[Mapping[str, Any], ...] = ()
    evidence_substitution_rules: tuple[Mapping[str, Any], ...] = ()
    red_team_prompts: tuple[str, ...] = ()
    review_status: Literal["pending", "passed", "changes_requested"] = "pending"


# --- Loader return type ------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class LoadedCard:
    """Loader return — opaque to consumers; carries namespace + parsed model +
    runtime registration receipt."""

    namespace: str                                    # cards:cic:<slug> | cards:clc:<slug> | cards:matrix:<intersection_id>
    card: object                                 # CICCard | CLCCard | MatrixCard
    card_path: str                               # absolute on-disk path used for load
    runtime_registered_seats: tuple[str, ...]         # Scout, Scribe, Judge, Logician, Archivist, Report Generator, Model Router
    canonical_bytes_sha256: str                       # SHA-256 of canonical-JSON bytes (signature input)
