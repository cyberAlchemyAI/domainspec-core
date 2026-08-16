"""Provider-neutral L0 contract value builders.

Every builder returns the same canonical ``ContractEnvelope`` shape.  The
type-specific manifest, query, profile, plan, receipt, or gate digest is the
outer envelope's ``digest`` value; builders do not introduce a second circular
self-digest inside ``value``.
"""

from __future__ import annotations

import re
from typing import NotRequired, TypedDict, cast

from .canonical import JsonValue, canonical_clone, make_envelope


CONTRACT_SCHEMA_VERSION = "1"
MANIFEST_SCHEMA_ID = "voice-production.manifest"
CAPABILITY_QUERY_SCHEMA_ID = "voice-production.capability-query"
CAPABILITY_PROFILE_SCHEMA_ID = "voice-production.capability-profile"
PLAN_SCHEMA_ID = "voice-production.plan"
NORMALIZED_RECEIPT_SCHEMA_ID = "voice-production.normalized-synthesis-receipt"
GATE_RECEIPT_SCHEMA_ID = "voice-production.gate-receipt"

_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_CAPABILITY_DECISIONS = frozenset(
    {"supported", "translated", "unsupported", "unknown"}
)
_GATE_DECISIONS = frozenset({"accepted", "rejected", "needs_revision"})


class ContractEnvelope(TypedDict):
    schema_id: str
    schema_version: str
    canonicalization_profile: str
    value: JsonValue
    digest_algorithm: str
    digest: str


class CapabilityDecision(TypedDict):
    requirement_ref: str
    status: str
    evidence_links: list[str]


class ProjectionRecord(TypedDict):
    segment_id: str
    exact_text_sha256: str
    projected_text_sha256: str
    transformations: list[dict[str, JsonValue]]
    approval_ref: NotRequired[str]


class PlannedOperation(TypedDict):
    operation_id: str
    operation_fingerprint: str
    submission_key: str
    selected_segment_ids: list[str]
    projected_payload_sha256: str
    expected_output_granularity: str
    composite_group_id: NotRequired[str]


class EvidenceLink(TypedDict):
    claim_id: str
    claim_type: str
    native_locator: str
    native_sha256: str
    observed_at: str
    classification: str
    redaction_profile: str


class NormalizedClaim(TypedDict):
    claim_id: str
    subject_ref: str
    predicate: str
    value: JsonValue
    evidence_link_ids: list[str]
    confidence: str


def _non_empty_text(value: str, name: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _sha256(value: str, name: str) -> str:
    if type(value) is not str or _SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"{name} must be a lowercase SHA-256 hex string")
    return value


def _text_list(values: list[str], name: str, *, unique: bool = False) -> list[str]:
    if type(values) is not list:
        raise ValueError(f"{name} must be a list")
    result = [_non_empty_text(value, f"{name}[{index}]") for index, value in enumerate(values)]
    if unique and len(set(result)) != len(result):
        raise ValueError(f"{name} must not contain duplicates")
    return result


def _object(value: dict[str, JsonValue], name: str) -> dict[str, JsonValue]:
    if type(value) is not dict:
        raise ValueError(f"{name} must be an object")
    return cast(dict[str, JsonValue], canonical_clone(value))


def _objects(
    values: list[dict[str, JsonValue]], name: str
) -> list[dict[str, JsonValue]]:
    if type(values) is not list:
        raise ValueError(f"{name} must be a list")
    return [_object(value, f"{name}[{index}]") for index, value in enumerate(values)]


def _envelope(schema_id: str, value: dict[str, JsonValue]) -> ContractEnvelope:
    return cast(
        ContractEnvelope,
        make_envelope(
            schema_id,
            value,
            schema_version=CONTRACT_SCHEMA_VERSION,
        ),
    )


def manifest_envelope(
    *,
    production_id: str,
    source: dict[str, JsonValue],
    segments: list[dict[str, JsonValue]],
    output_policy: dict[str, JsonValue],
    acceptance_policy: dict[str, JsonValue],
) -> ContractEnvelope:
    """Build a complete source/segment/policy manifest envelope."""

    source_value = _object(source, "source")
    if "sha256" in source_value:
        _sha256(cast(str, source_value["sha256"]), "source.sha256")
    value: dict[str, JsonValue] = {
        "production_id": _non_empty_text(production_id, "production_id"),
        "source": source_value,
        "segments": _objects(segments, "segments"),
        "output_policy": _object(output_policy, "output_policy"),
        "acceptance_policy": _object(acceptance_policy, "acceptance_policy"),
    }
    return _envelope(MANIFEST_SCHEMA_ID, value)


def capability_query_envelope(
    *,
    manifest_digest: str,
    selected_segment_ids: list[str],
    content_characteristics_digest: str,
    required_capabilities: list[str],
    transport_mode: str,
    adapter: dict[str, JsonValue],
    provider_schema_basis: dict[str, JsonValue],
    binding_model_settings_descriptor_digest: str,
) -> ContractEnvelope:
    """Build the content-bound, adapter-version-bound capability query."""

    value: dict[str, JsonValue] = {
        "manifest_digest": _sha256(manifest_digest, "manifest_digest"),
        "selected_segment_ids": _text_list(
            selected_segment_ids, "selected_segment_ids", unique=True
        ),
        "content_characteristics_digest": _sha256(
            content_characteristics_digest, "content_characteristics_digest"
        ),
        "required_capabilities": _text_list(
            required_capabilities, "required_capabilities", unique=True
        ),
        "transport_mode": _non_empty_text(transport_mode, "transport_mode"),
        "adapter": _object(adapter, "adapter"),
        "provider_schema_basis": _object(
            provider_schema_basis, "provider_schema_basis"
        ),
        "binding_model_settings_descriptor_digest": _sha256(
            binding_model_settings_descriptor_digest,
            "binding_model_settings_descriptor_digest",
        ),
    }
    return _envelope(CAPABILITY_QUERY_SCHEMA_ID, value)


def capability_profile_envelope(
    *,
    query_digest: str,
    decisions: list[CapabilityDecision],
    output_granularity: str,
    retry_granularity: str,
    idempotency_support: str,
    cancellation_support: str,
    evidence_basis: list[dict[str, JsonValue]],
) -> ContractEnvelope:
    """Build the evidence-backed result of a capability query."""

    decision_values = _objects(cast(list[dict[str, JsonValue]], decisions), "decisions")
    for index, decision in enumerate(decision_values):
        status = decision.get("status")
        if status not in _CAPABILITY_DECISIONS:
            raise ValueError(
                f"decisions[{index}].status must be one of "
                f"{sorted(_CAPABILITY_DECISIONS)}"
            )
    value: dict[str, JsonValue] = {
        "query_digest": _sha256(query_digest, "query_digest"),
        "decisions": decision_values,
        "output_granularity": _non_empty_text(
            output_granularity, "output_granularity"
        ),
        "retry_granularity": _non_empty_text(
            retry_granularity, "retry_granularity"
        ),
        "idempotency_support": _non_empty_text(
            idempotency_support, "idempotency_support"
        ),
        "cancellation_support": _non_empty_text(
            cancellation_support, "cancellation_support"
        ),
        "evidence_basis": _objects(evidence_basis, "evidence_basis"),
    }
    return _envelope(CAPABILITY_PROFILE_SCHEMA_ID, value)


def plan_envelope(
    *,
    manifest_digest: str,
    capability_profile_digest: str,
    selected_segment_ids: list[str],
    operations: list[PlannedOperation],
    expected_outputs: list[dict[str, JsonValue]],
    effect_estimates: dict[str, JsonValue],
    warnings: list[str],
    blocked_requirements: list[str],
    transformations: list[ProjectionRecord],
    native_schema_basis: dict[str, JsonValue],
) -> ContractEnvelope:
    """Build a pure execution plan whose complete effect surface is covered."""

    value: dict[str, JsonValue] = {
        "manifest_digest": _sha256(manifest_digest, "manifest_digest"),
        "capability_profile_digest": _sha256(
            capability_profile_digest, "capability_profile_digest"
        ),
        "selected_segment_ids": _text_list(
            selected_segment_ids, "selected_segment_ids", unique=True
        ),
        "operations": _objects(
            cast(list[dict[str, JsonValue]], operations), "operations"
        ),
        "expected_outputs": _objects(expected_outputs, "expected_outputs"),
        "effect_estimates": _object(effect_estimates, "effect_estimates"),
        "warnings": _text_list(warnings, "warnings"),
        "blocked_requirements": _text_list(
            blocked_requirements, "blocked_requirements", unique=True
        ),
        "transformations": _objects(
            cast(list[dict[str, JsonValue]], transformations), "transformations"
        ),
        "native_schema_basis": _object(
            native_schema_basis, "native_schema_basis"
        ),
    }
    return _envelope(PLAN_SCHEMA_ID, value)


def normalized_receipt_envelope(
    *,
    manifest_digest: str,
    capability_profile_digest: str,
    plan_digest: str,
    execution_authorization_digest: str,
    run_id: str,
    output_granularity: str,
    composite_groups: list[dict[str, JsonValue]],
    claims: list[NormalizedClaim],
    evidence_links: list[EvidenceLink],
    artifacts: list[dict[str, JsonValue]],
    reconciliation_state: JsonValue,
    parent_run_id: str | None = None,
) -> ContractEnvelope:
    """Build a provider-neutral normalized synthesis receipt envelope."""

    value: dict[str, JsonValue] = {
        "manifest_digest": _sha256(manifest_digest, "manifest_digest"),
        "capability_profile_digest": _sha256(
            capability_profile_digest, "capability_profile_digest"
        ),
        "plan_digest": _sha256(plan_digest, "plan_digest"),
        "execution_authorization_digest": _sha256(
            execution_authorization_digest, "execution_authorization_digest"
        ),
        "run_id": _non_empty_text(run_id, "run_id"),
        "output_granularity": _non_empty_text(
            output_granularity, "output_granularity"
        ),
        "composite_groups": _objects(composite_groups, "composite_groups"),
        "claims": _objects(cast(list[dict[str, JsonValue]], claims), "claims"),
        "evidence_links": _objects(
            cast(list[dict[str, JsonValue]], evidence_links), "evidence_links"
        ),
        "artifacts": _objects(artifacts, "artifacts"),
        "reconciliation_state": canonical_clone(reconciliation_state),
    }
    if parent_run_id is not None:
        value["parent_run_id"] = _non_empty_text(parent_run_id, "parent_run_id")
    return _envelope(NORMALIZED_RECEIPT_SCHEMA_ID, value)


def gate_receipt_envelope(
    *,
    synthesis_receipt_digest: str,
    reviewed_artifact_sha256s: list[str],
    criteria_results: list[dict[str, JsonValue]],
    review_scope: str,
    reviewer: str,
    decision: str,
    decided_at: str,
    exceptions: list[dict[str, JsonValue]],
) -> ContractEnvelope:
    """Build a human gate receipt bound to receipt and artifact bytes."""

    if decision not in _GATE_DECISIONS:
        raise ValueError(f"decision must be one of {sorted(_GATE_DECISIONS)}")
    artifact_digests = [
        _sha256(value, f"reviewed_artifact_sha256s[{index}]")
        for index, value in enumerate(reviewed_artifact_sha256s)
    ]
    value: dict[str, JsonValue] = {
        "synthesis_receipt_digest": _sha256(
            synthesis_receipt_digest, "synthesis_receipt_digest"
        ),
        "reviewed_artifact_sha256s": artifact_digests,
        "criteria_results": _objects(criteria_results, "criteria_results"),
        "review_scope": _non_empty_text(review_scope, "review_scope"),
        "reviewer": _non_empty_text(reviewer, "reviewer"),
        "decision": decision,
        "decided_at": _non_empty_text(decided_at, "decided_at"),
        "exceptions": _objects(exceptions, "exceptions"),
    }
    return _envelope(GATE_RECEIPT_SCHEMA_ID, value)
