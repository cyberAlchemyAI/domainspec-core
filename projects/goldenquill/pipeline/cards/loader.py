"""pipeline.cards.loader — Card loader.

Per architecture v7.0.11 §1.5 (loader contract). Runtime seat injection still
lands at v0.2 first wave, but lifecycle/coupling preflight is LIVE now because
card lifecycle truth is a trust-boundary invariant: a card marked ``draft`` must
never be runtime-loadable.

Loader contract (ordered):
  1. Read YAML card from disk.
  2. Validate basic schema/lifecycle shape for the declared axis.
  3. Verify lifecycle state matches runtime-loadability truth.
  4. Reject cards encoding CIC × CLC eligibility subset coupling.
  5. Resolve card to its memory namespace.
  6. Build the memory profile (concept graph nodes + edges).
  7. Register runtime defaults with consuming seats.
  8. Record the load event in audit log.

At v0.1 Beta, steps 1-4 are live preflight checks. A valid runtime card then
raises NotImplementedError at the seat-injection boundary, preserving the
v0.1/v0.2 scope split while still fail-closing malformed lifecycle states.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Literal, Mapping, Optional

import yaml

from pipeline.cards.models import (
    CIC_SLUGS,
    CLC_SLUGS,
    CICCard,
    CLCCard,
    LoadedCard,
    MatrixCard,
)


Environment = Literal["development", "production"]
CardAxis = Literal["CIC", "CLC", "MATRIX"]


class CardLoaderError(RuntimeError):
    """Base class for fail-closed card-loader preflight errors."""


class CardSchemaError(CardLoaderError):
    """F-CARDS-SCHEMA-INVALID preflight failure."""


class CardLifecycleError(CardLoaderError):
    """F-CARDS-MALFORMED-LIFECYCLE preflight failure."""


class CardCouplingError(CardLoaderError):
    """F-CARDS-COUPLING-VIOLATION-EXTENSION preflight failure."""


class CardManifestMembershipError(CardLoaderError):
    """F-CARDS-NOT-IN-ACTIVE-MANIFEST preflight failure.

    Production-environment load was attempted on a card whose (card_id, slug,
    card_path) tuple is not declared in the active-card registry at
    ``pipeline/cards/registry.yaml``. The registry is the trust-boundary
    declaration of which cards are runtime-loadable; any card outside it is
    research/draft material and must not enter production.

    Development-environment loads bypass this gate so research dispatches and
    Wave-N audits can iterate on candidate cards without registry churn.
    """


DEFAULT_REGISTRY_PATH: str = "pipeline/cards/registry.yaml"


DRAFT_STATUS_VALUES: frozenset[str] = frozenset({
    "draft",
    "review_passed",
    "signed",
    "deprecated",
})

LIFECYCLE_REQUIRED_FIELDS: frozenset[str] = frozenset({
    "draft_status",
    "review_status",
    "cross_family_thesis_status",
    "signature_status",
    "runtime_load_status",
    "runtime_loadable",
})

SIGNED_LIFECYCLE_REQUIRED_FIELDS: frozenset[str] = frozenset({
    "signed_at",
    "signed_by",
    "content_hash",
})

REQUIRED_FIELDS_BY_AXIS: Mapping[str, frozenset[str]] = {
    "CIC": frozenset({
        "schema_version",
        "card_axis",
        "card_id",
        "slug",
        "display_name",
        "coverage_axis",
        "tilth_cic_id",
        "search_vocabulary",
        "evidence_signals",
        "kfr_fact_classes",
        "register_defaults",
        "admin_risk_term_register",
        "reporting_cadence_typical",
        "lifecycle",
        "_research_metadata",
    }),
    "CLC": frozenset({
        "schema_version",
        "card_axis",
        "card_id",
        "slug",
        "display_name",
        "funding_mechanism_summary",
        "tilth_clc_id",
        "underwriting_criteria",
        "evidence_weights",
        "reviewer_profile_typical",
        "common_red_flags",
        "reporting_requirements_typical",
        "commitment_tracking_pattern",
        "lifecycle",
        "_research_metadata",
    }),
}


# §18.6 v2 Option A — CLC card shape decomposition.
#
# Two mutually-exclusive shapes per pipeline/cards/_schema/card_clc.schema.json
# top-level ``oneOf`` (single-track legacy vs multi-track Option A); both shapes
# share the same root metadata. The loader mirrors the schema's ``oneOf`` here
# without taking a jsonschema runtime dependency:
#
#   * CLC_SHARED_ROOT_REQUIRED_FIELDS  — required at root in both shapes
#   * CLC_SINGLE_TRACK_ROOT_REQUIRED_FIELDS  — required at root ONLY in
#     single-track legacy shape (the six core track-specific fields)
#   * CLC_TRACK_CONTAINER_REQUIRED_FIELDS  — required inside each track_a /
#     track_b container in multi-track shape
#   * CLC_TRACK_SPECIFIC_FIELDS_FORBIDDEN_AT_ROOT_IN_MULTI_TRACK  — any of the
#     14 track-specific keys present at root forces single-track shape (and
#     thus forbids multi-track containers)
#
# Detection rule: if track_a and track_b both appear at root, multi-track shape
# is in force; if neither appears, single-track shape is in force. A card with
# exactly one of track_a / track_b is an oneOf violation and fails closed.

CLC_SHARED_ROOT_REQUIRED_FIELDS: frozenset[str] = frozenset({
    "schema_version",
    "card_axis",
    "card_id",
    "slug",
    "display_name",
    "funding_mechanism_summary",
    "tilth_clc_id",
    "lifecycle",
    "_research_metadata",
})

CLC_SINGLE_TRACK_ROOT_REQUIRED_FIELDS: frozenset[str] = frozenset({
    "underwriting_criteria",
    "evidence_weights",
    "reviewer_profile_typical",
    "common_red_flags",
    "reporting_requirements_typical",
    "commitment_tracking_pattern",
})

CLC_TRACK_CONTAINER_REQUIRED_FIELDS: frozenset[str] = frozenset({
    "track_name",
    "track_description",
    "underwriting_criteria",
    "evidence_weights",
    "reviewer_profile_typical",
    "common_red_flags",
    "reporting_requirements_typical",
    "commitment_tracking_pattern",
})

CLC_TRACK_SPECIFIC_FIELDS_FORBIDDEN_AT_ROOT_IN_MULTI_TRACK: frozenset[str] = frozenset({
    "underwriting_criteria",
    "scoring_weight_patterns",
    "evidence_weights",
    "common_application_forms",
    "narrative_section_patterns",
    "budget_structure_conventions",
    "reviewer_profile_typical",
    "common_portals",
    "common_red_flags",
    "reporting_requirements_typical",
    "compliance_obligations",
    "commitment_tracking_pattern",
    "common_funders_observed",
    "provenance_requirements",
})


def load_card(
    *,
    path: str,
    environment: Environment,
    publisher_pubkey: Optional[bytes] = None,
    v1_x_matrix_phase_active: bool = False,
    manifest_path: Optional[str] = None,
) -> LoadedCard:
    """Load + validate + register a Card.

    Lifecycle, coupling, and manifest-membership preflight are LIVE. Full
    runtime context injection still graduates at v0.2 first wave, so a card
    that passes preflight raises NotImplementedError at the final registration
    boundary.

    Args:
        path: Filesystem path to the card YAML.
        environment: "production" or "development". Production enforces the
            manifest-membership gate; development bypasses it.
        publisher_pubkey: Reserved for v0.2 signature verification. Currently
            unused by the loader preflight.
        v1_x_matrix_phase_active: Gate flag for matrix-card loading; matrix
            cards remain forbidden until the v1.x amendment lands.
        manifest_path: Optional override for the active-card manifest path.
            Defaults to ``pipeline/cards/registry.yaml`` resolved relative to
            the loader's repo root. The override is provided so tests and
            future fleet-deployments can supply a different manifest without
            patching loader internals.

    Raises:
        CardSchemaError: card does not validate against its declared axis's
            basic schema shape.
        CardLifecycleError: lifecycle truth is malformed, including any card
            with draft_status="draft" or runtime_loadable=True while not signed.
        CardCouplingError: card body contains forbidden CIC↔CLC coupling fields.
        CardManifestMembershipError: production-environment load of a card
            whose (card_id, slug, card_path) is not declared in the active-card
            manifest.
        NotImplementedError: valid card reached the v0.2 runtime registration
            boundary.
    """

    card_body = read_card_body(path=path)
    declared_axis = validate_card_schema_shape(card_path=path, card_body=card_body)

    if declared_axis == "MATRIX":
        if not v1_x_matrix_phase_active:
            raise CardCouplingError(
                "F-CARDS-COUPLING-VIOLATION-EXTENSION: matrix card loading is "
                "forbidden before the v1.x matrix-phase explicit amendment."
            )
    else:
        enforce_lifecycle_truth(card_path=path, card_body=card_body)
        enforce_no_forbidden_coupling(
            card_path=path,
            card_body=card_body,
            declared_axis=declared_axis,
        )
        enforce_manifest_membership(
            card_path=path,
            card_body=card_body,
            environment=environment,
            manifest_path=manifest_path,
        )

    raise NotImplementedError(
        "Card runtime registration graduates LIVE at v0.2 first wave per "
        "architecture v7.0.11 §5. Lifecycle/coupling/manifest preflight is "
        "already LIVE so draft, malformed, coupled, or unregistered cards "
        "fail before this boundary."
    )


def enforce_manifest_membership(
    *,
    card_path: str,
    card_body: Mapping[str, Any],
    environment: Environment,
    manifest_path: Optional[str] = None,
) -> None:
    """Fail closed if a production card load is not declared in the manifest.

    The manifest is ``pipeline/cards/registry.yaml`` (the active-card
    registry; ``registry_kind: active_card_registry``). A card passes this
    gate when its (card_id, slug, card_path) tuple matches an entry whose
    ``active: true`` AND ``required_draft_status: signed`` AND
    ``required_runtime_loadable: true``.

    Development-environment loads bypass this gate to allow research and
    Wave-N audit iteration on candidate cards before they enter the manifest.

    The card-path comparison is anchored at the manifest's parent-of-parent
    directory (the repo root by default) so manifest entries written as
    workspace-relative paths (``pipeline/cards/CIC/foo.yaml``) resolve
    correctly regardless of where the loader is invoked from.
    """

    if environment != "production":
        return

    resolved_manifest = _resolve_manifest_path(card_path=card_path, manifest_path=manifest_path)
    try:
        manifest_body = read_card_body(path=str(resolved_manifest))
    except CardSchemaError as exc:
        raise CardManifestMembershipError(
            f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: {card_path} cannot be admitted because "
            f"the manifest at {resolved_manifest} did not parse: {exc}"
        ) from exc
    except FileNotFoundError as exc:
        raise CardManifestMembershipError(
            f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: {card_path} cannot be admitted because "
            f"the manifest at {resolved_manifest} is missing."
        ) from exc

    if manifest_body.get("registry_kind") != "active_card_registry":
        raise CardManifestMembershipError(
            f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: manifest at {resolved_manifest} is not "
            f"declared as registry_kind=active_card_registry."
        )

    entries = manifest_body.get("active_cards")
    if not isinstance(entries, list) or not entries:
        raise CardManifestMembershipError(
            f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: manifest at {resolved_manifest} carries "
            "no active_cards list."
        )

    repo_root = resolved_manifest.parent.parent.parent
    card_path_abs = Path(card_path).resolve()
    candidate_card_id = card_body.get("card_id")
    candidate_slug = card_body.get("slug")
    candidate_axis = card_body.get("card_axis")

    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        if entry.get("card_id") != candidate_card_id:
            continue
        if entry.get("slug") != candidate_slug:
            continue
        if entry.get("card_axis") != candidate_axis:
            continue
        # card_id + slug + axis matched. Verify path matches the manifest's
        # declared card_path (resolved against repo root) AND the entry's
        # active + required_* fields satisfy production semantics.
        declared_path = entry.get("card_path")
        if not isinstance(declared_path, str):
            continue
        manifest_card_path_abs = (repo_root / declared_path).resolve()
        if manifest_card_path_abs != card_path_abs:
            raise CardManifestMembershipError(
                f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: {card_path} matches manifest entry "
                f"(card_id={candidate_card_id!r}, slug={candidate_slug!r}) but its on-disk "
                f"path differs from the declared path {manifest_card_path_abs}. Production "
                "loads must load cards from their registry-declared locations only."
            )
        if entry.get("active") is not True:
            raise CardManifestMembershipError(
                f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: {card_path} matches a manifest entry that "
                "is not active=true."
            )
        if entry.get("required_draft_status") != "signed":
            raise CardManifestMembershipError(
                f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: {card_path} matches a manifest entry whose "
                "required_draft_status is not 'signed'."
            )
        if entry.get("required_runtime_loadable") is not True:
            raise CardManifestMembershipError(
                f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: {card_path} matches a manifest entry whose "
                "required_runtime_loadable is not true."
            )
        return

    raise CardManifestMembershipError(
        f"F-CARDS-NOT-IN-ACTIVE-MANIFEST: {card_path} (card_id={candidate_card_id!r}, "
        f"slug={candidate_slug!r}, axis={candidate_axis!r}) is not declared in the active-card "
        f"manifest at {resolved_manifest}. Production loads are restricted to manifest-listed "
        "cards; if this is a research draft, load with environment='development'."
    )


def _resolve_manifest_path(*, card_path: str, manifest_path: Optional[str]) -> Path:
    """Resolve the manifest path to an absolute Path.

    If ``manifest_path`` is provided, it is used as-is. Otherwise the loader
    looks for ``pipeline/cards/registry.yaml`` anchored to the repo root that
    contains the card-path's ``pipeline/`` ancestor. This lets the loader
    behave correctly whether invoked from the repo root, a sub-directory, or
    a temporary test working directory.
    """

    if manifest_path is not None:
        return Path(manifest_path).resolve()

    card = Path(card_path).resolve()
    # Walk upward looking for a directory that contains DEFAULT_REGISTRY_PATH.
    for ancestor in [card.parent, *card.parents]:
        candidate = ancestor / DEFAULT_REGISTRY_PATH
        if candidate.exists():
            return candidate.resolve()

    # Fall back to repo-root-from-loader location so the error message points
    # somewhere consistent rather than at the temp card directory.
    loader_root = Path(__file__).resolve().parents[2]
    return (loader_root / DEFAULT_REGISTRY_PATH).resolve()


def read_card_body(*, path: str) -> dict[str, Any]:
    """Read a YAML card body from disk and require a mapping root."""

    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f)
    if not isinstance(loaded, dict):
        raise CardSchemaError(f"F-CARDS-SCHEMA-INVALID: {path} root must be a mapping")
    return loaded


def validate_card_schema_shape(*, card_path: str, card_body: Mapping[str, Any]) -> CardAxis:
    """Validate the live subset of the card schemas used by runtime preflight.

    This intentionally does not replace the JSON schema files; it is the small
    fail-closed shape check the loader can run without adding another runtime
    dependency.
    """

    axis = card_body.get("card_axis")
    if axis not in {"CIC", "CLC", "MATRIX"}:
        raise CardSchemaError(
            f"F-CARDS-SCHEMA-INVALID: {card_path} card_axis must be CIC, CLC, or MATRIX"
        )

    if axis == "MATRIX":
        return "MATRIX"

    if axis == "CIC":
        required = REQUIRED_FIELDS_BY_AXIS["CIC"]
        missing = tuple(sorted(k for k in required if k not in card_body))
        if missing:
            raise CardSchemaError(
                f"F-CARDS-SCHEMA-INVALID: {card_path} missing required fields {missing!r}"
            )
        if card_body.get("schema_version") != "1.0-cic":
            raise CardSchemaError(f"F-CARDS-SCHEMA-INVALID: {card_path} schema_version must be 1.0-cic")
        if card_body.get("slug") not in CIC_SLUGS:
            raise CardSchemaError(f"F-CARDS-SCHEMA-INVALID: {card_path} has unknown CIC slug")
    elif axis == "CLC":
        # Shared root fields (required in both single-track and multi-track shapes).
        missing_shared = tuple(
            sorted(k for k in CLC_SHARED_ROOT_REQUIRED_FIELDS if k not in card_body)
        )
        if missing_shared:
            raise CardSchemaError(
                f"F-CARDS-SCHEMA-INVALID: {card_path} missing required fields {missing_shared!r}"
            )

        # §18.6 v2 Option A shape dispatch — mirrors schema oneOf branches.
        has_track_a = "track_a" in card_body
        has_track_b = "track_b" in card_body

        if has_track_a != has_track_b:
            # Exactly one of track_a / track_b is present — oneOf violation.
            raise CardSchemaError(
                f"F-CARDS-SCHEMA-INVALID: {card_path} declares only one of "
                f"track_a / track_b; §18.6 v2 Option A multi-track shape requires "
                f"both containers together"
            )

        if has_track_a and has_track_b:
            # Multi-track Option A shape.
            illegal_at_root = tuple(
                sorted(
                    k for k in CLC_TRACK_SPECIFIC_FIELDS_FORBIDDEN_AT_ROOT_IN_MULTI_TRACK
                    if k in card_body
                )
            )
            if illegal_at_root:
                raise CardSchemaError(
                    f"F-CARDS-SCHEMA-INVALID: {card_path} declares track_a/track_b "
                    f"(§18.6 v2 multi-track shape) but track-specific fields "
                    f"{illegal_at_root!r} also appear at root; track-specific "
                    f"fields must live inside the track containers, not at root"
                )
            for track_key in ("track_a", "track_b"):
                container = card_body.get(track_key)
                if not isinstance(container, Mapping):
                    raise CardSchemaError(
                        f"F-CARDS-SCHEMA-INVALID: {card_path} {track_key} must be a mapping"
                    )
                missing_container = tuple(
                    sorted(
                        k for k in CLC_TRACK_CONTAINER_REQUIRED_FIELDS
                        if k not in container
                    )
                )
                if missing_container:
                    raise CardSchemaError(
                        f"F-CARDS-SCHEMA-INVALID: {card_path} {track_key} missing "
                        f"required fields {missing_container!r}"
                    )
        else:
            # Single-track legacy shape — six track-specific fields required at root.
            missing_single = tuple(
                sorted(
                    k for k in CLC_SINGLE_TRACK_ROOT_REQUIRED_FIELDS
                    if k not in card_body
                )
            )
            if missing_single:
                raise CardSchemaError(
                    f"F-CARDS-SCHEMA-INVALID: {card_path} missing required fields {missing_single!r}"
                )

        if card_body.get("schema_version") != "1.0-clc":
            raise CardSchemaError(f"F-CARDS-SCHEMA-INVALID: {card_path} schema_version must be 1.0-clc")
        if card_body.get("slug") not in CLC_SLUGS:
            raise CardSchemaError(f"F-CARDS-SCHEMA-INVALID: {card_path} has unknown CLC slug")

    lifecycle = card_body.get("lifecycle")
    if not isinstance(lifecycle, Mapping):
        raise CardLifecycleError(
            f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} lifecycle must be a mapping"
        )
    missing_lifecycle = tuple(sorted(k for k in LIFECYCLE_REQUIRED_FIELDS if k not in lifecycle))
    if missing_lifecycle:
        raise CardLifecycleError(
            f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} missing lifecycle fields "
            f"{missing_lifecycle!r}"
        )
    if lifecycle.get("draft_status") not in DRAFT_STATUS_VALUES:
        raise CardLifecycleError(
            f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} draft_status must be one of "
            f"{tuple(sorted(DRAFT_STATUS_VALUES))!r}"
        )
    if not isinstance(lifecycle.get("runtime_loadable"), bool):
        raise CardLifecycleError(
            f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} lifecycle.runtime_loadable must be boolean"
        )

    return axis  # type: ignore[return-value]


def enforce_lifecycle_truth(
    *,
    card_path: str,
    card_body: Mapping[str, Any],
    verify_content_hash: bool = True,
) -> None:
    """Fail closed on lifecycle states that blur draft/review/signed/runtime truth."""

    lifecycle = card_body.get("lifecycle")
    if not isinstance(lifecycle, Mapping):
        raise CardLifecycleError(
            f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} lifecycle must be a mapping"
        )

    draft_status = lifecycle.get("draft_status")
    runtime_loadable = lifecycle.get("runtime_loadable")
    runtime_load_status = lifecycle.get("runtime_load_status")
    signature_status = lifecycle.get("signature_status")

    if draft_status == "draft":
        raise CardLifecycleError(
            f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} has draft_status='draft'. "
            "Loader refuses draft cards; research drafts must stay outside the production registry."
        )

    if draft_status != "signed" and runtime_loadable is not False:
        raise CardLifecycleError(
            f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} has draft_status={draft_status!r}; "
            "runtime_loadable must be false unless draft_status is 'signed'."
        )

    if runtime_loadable is True:
        if draft_status != "signed":
            raise CardLifecycleError(
                f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} runtime_loadable=true requires "
                "draft_status='signed'."
            )
        if signature_status != "signed":
            raise CardLifecycleError(
                f"F-CARDS-UNSIGNED-PRODUCTION-LOAD: {card_path} runtime_loadable=true requires "
                "signature_status='signed'."
            )
        if runtime_load_status != "loaded":
            raise CardLifecycleError(
                f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} runtime_loadable=true requires "
                "runtime_load_status='loaded'."
            )
        missing_signed = tuple(sorted(k for k in SIGNED_LIFECYCLE_REQUIRED_FIELDS if not lifecycle.get(k)))
        if missing_signed:
            raise CardLifecycleError(
                f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} signed runtime card missing "
                f"{missing_signed!r}."
            )
        if verify_content_hash:
            actual_hash = str(lifecycle.get("content_hash"))
            expected_hash = f"sha256:{canonical_bytes_sha256(card_body=card_body)}"
            if actual_hash != expected_hash:
                raise CardLifecycleError(
                    f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} content_hash mismatch; "
                    f"expected {expected_hash}, got {actual_hash}."
                )

    if runtime_loadable is False and runtime_load_status == "loaded":
        raise CardLifecycleError(
            f"F-CARDS-MALFORMED-LIFECYCLE: {card_path} runtime_loadable=false cannot pair "
            "with runtime_load_status='loaded'."
        )


def enforce_no_forbidden_coupling(
    *,
    card_path: str,
    card_body: Mapping[str, Any],
    declared_axis: Literal["CIC", "CLC"],
) -> None:
    """Fail closed on forbidden CIC↔CLC coupling keys anywhere in the YAML tree."""

    from pipeline.logician.gates.f_cards_coupling_violation_extension import (  # local import avoids cycle
        FORBIDDEN_FIELD_REGISTRY,
    )

    forbidden = FORBIDDEN_FIELD_REGISTRY[declared_axis]
    found = tuple(_find_forbidden_keys(card_body, forbidden=forbidden))
    if found:
        raise CardCouplingError(
            f"F-CARDS-COUPLING-VIOLATION-EXTENSION: {card_path} contains forbidden "
            f"{declared_axis} coupling keys {found!r}. CICs may recommend compatible CLCs "
            "only at orchestration time, never by embedding CLC pattern logic in card files."
        )


def _find_forbidden_keys(value: Any, *, forbidden: frozenset[str], prefix: str = "") -> tuple[str, ...]:
    hits: list[str] = []
    if isinstance(value, Mapping):
        for k, v in value.items():
            key = str(k)
            path = f"{prefix}.{key}" if prefix else key
            if key in forbidden:
                hits.append(path)
            hits.extend(_find_forbidden_keys(v, forbidden=forbidden, prefix=path))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            path = f"{prefix}[{i}]" if prefix else f"[{i}]"
            hits.extend(_find_forbidden_keys(item, forbidden=forbidden, prefix=path))
    return tuple(hits)


def canonical_bytes(*, card_body: Mapping[str, object]) -> bytes:
    """Compute canonical-JSON byte sequence for card integrity hashing.

    Deterministic key ordering (sort_keys=True), no whitespace, UTF-8. Signature
    and self-referential integrity fields are excluded before serialization:
    ``_research_metadata.ed25519_signature``, ``lifecycle.signature_status``,
    and ``lifecycle.content_hash``.
    """

    normalized = _without_signature_and_hash_fields(card_body)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def canonical_bytes_sha256(*, card_body: Mapping[str, object]) -> str:
    """SHA-256 hex digest of canonical_bytes() output."""

    return hashlib.sha256(canonical_bytes(card_body=card_body)).hexdigest()


def _without_signature_and_hash_fields(card_body: Mapping[str, object]) -> dict[str, Any]:
    normalized = copy.deepcopy(dict(card_body))
    lifecycle = normalized.get("lifecycle")
    if isinstance(lifecycle, dict):
        lifecycle.pop("signature_status", None)
        lifecycle.pop("content_hash", None)
    research_metadata = normalized.get("_research_metadata")
    if isinstance(research_metadata, dict):
        research_metadata.pop("ed25519_signature", None)
    return normalized


def resolve_card_namespace(
    *,
    card_axis: Literal["CIC", "CLC", "MATRIX"],
    slug: Optional[str] = None,
    intersection_id: Optional[str] = None,
) -> str:
    """Resolve the workspace-shared memory namespace for a given card.

    Per architecture v7.0.11 §1.9:
      - CIC → 'cards:cic:<slug>'
      - CLC → 'cards:clc:<slug>'
      - MATRIX → 'cards:matrix:<intersection_id>' (per-intersection granularity)
    """

    if card_axis == "CIC":
        if slug is None:
            raise ValueError("CIC namespace resolution requires slug")
        return f"cards:cic:{slug}"
    elif card_axis == "CLC":
        if slug is None:
            raise ValueError("CLC namespace resolution requires slug")
        return f"cards:clc:{slug}"
    elif card_axis == "MATRIX":
        if intersection_id is None:
            raise ValueError("MATRIX namespace resolution requires intersection_id")
        return f"cards:matrix:{intersection_id}"
    else:
        raise ValueError(f"Unknown card_axis: {card_axis!r}")


def display_name_for_consumer(
    *,
    card: object,
    consumer: Literal["full", "short"] = "full",
) -> str:
    """Resolve the display name for a CIC/CLC card."""

    if isinstance(card, CICCard):
        if consumer == "short" and card.display_name_short is not None:
            return card.display_name_short
        return card.display_name
    elif isinstance(card, CLCCard):
        return card.display_name
    else:
        raise TypeError(
            f"display_name_for_consumer expects CICCard or CLCCard, got {type(card).__name__}"
        )
