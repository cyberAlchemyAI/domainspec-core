"""Pure provider-neutral capability and segment-plan preparation.

This module builds canonical query, profile, and plan envelopes.  It performs
no file, network, secret, provider, submission, or audio operation.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Callable, Mapping, cast

from .canonical import (
    JsonValue,
    canonical_bytes,
    canonical_clone,
    canonical_loads,
    canonical_sha256,
    require_valid_envelope,
)
from .contracts import (
    CAPABILITY_PROFILE_SCHEMA_ID,
    CAPABILITY_QUERY_SCHEMA_ID,
    MANIFEST_SCHEMA_ID,
    PLAN_SCHEMA_ID,
    CapabilityDecision,
    ContractEnvelope,
    PlannedOperation,
    ProjectionRecord,
    capability_profile_envelope,
    capability_query_envelope,
    plan_envelope,
)


_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_CAPABILITY_STATUSES = frozenset(
    {"supported", "translated", "unsupported", "unknown"}
)


class PortContractError(ValueError):
    """Base failure for an invalid provider-neutral preparation contract."""


class MandatoryCapabilityBlocked(PortContractError):
    """Raised when a required capability is not supported or translated."""


class ProjectionApprovalRequired(PortContractError):
    """Raised when projected text differs but no run-local approval is bound."""


@dataclass(frozen=True, slots=True)
class FrozenEnvelope:
    """Immutable canonical bytes with detached envelope access."""

    canonical_envelope_bytes: bytes
    expected_schema_id: str

    def __post_init__(self) -> None:
        if type(self.canonical_envelope_bytes) is not bytes:
            raise TypeError("canonical_envelope_bytes must be bytes")
        envelope = self.as_envelope()
        if envelope["schema_id"] != self.expected_schema_id:
            raise PortContractError(
                f"expected schema {self.expected_schema_id!r}; "
                f"got {envelope['schema_id']!r}"
            )

    def as_envelope(self) -> ContractEnvelope:
        value = canonical_loads(self.canonical_envelope_bytes)
        if type(value) is not dict:
            raise PortContractError("contract envelope must be an object")
        envelope = cast(dict[str, JsonValue], value)
        require_valid_envelope(envelope)
        return cast(ContractEnvelope, envelope)

    @property
    def digest(self) -> str:
        return cast(str, self.as_envelope()["digest"])

    @property
    def value(self) -> dict[str, JsonValue]:
        value = self.as_envelope()["value"]
        if type(value) is not dict:
            raise PortContractError("contract value must be an object")
        return cast(dict[str, JsonValue], value)


def _sha256(value: str, name: str) -> str:
    if type(value) is not str or _SHA256_RE.fullmatch(value) is None:
        raise PortContractError(f"{name} must be lowercase SHA-256 hex")
    return value


def _envelope_value(
    envelope: Mapping[str, JsonValue], expected_schema_id: str
) -> dict[str, JsonValue]:
    if type(envelope) is not dict:
        raise PortContractError("envelope must be an object")
    detached = cast(dict[str, JsonValue], canonical_clone(dict(envelope)))
    require_valid_envelope(detached)
    if detached["schema_id"] != expected_schema_id:
        raise PortContractError(
            f"expected schema {expected_schema_id!r}; "
            f"got {detached['schema_id']!r}"
        )
    value = detached["value"]
    if type(value) is not dict:
        raise PortContractError("envelope value must be an object")
    return cast(dict[str, JsonValue], value)


def _ordered_segments(
    manifest: Mapping[str, JsonValue], selected_segment_ids: list[str]
) -> list[dict[str, JsonValue]]:
    value = _envelope_value(manifest, MANIFEST_SCHEMA_ID)
    raw_segments = value.get("segments")
    if type(raw_segments) is not list:
        raise PortContractError("manifest segments must be a list")
    if type(selected_segment_ids) is not list or not selected_segment_ids:
        raise PortContractError("selected_segment_ids must be non-empty")
    if any(type(item) is not str or not item for item in selected_segment_ids):
        raise PortContractError("selected segment ids must be non-empty strings")
    if len(set(selected_segment_ids)) != len(selected_segment_ids):
        raise PortContractError("selected segment ids must be unique")

    selected = set(selected_segment_ids)
    ordered: list[dict[str, JsonValue]] = []
    for raw in raw_segments:
        if type(raw) is not dict:
            raise PortContractError("manifest segment must be an object")
        segment = cast(dict[str, JsonValue], raw)
        segment_id = segment.get("segment_id")
        if type(segment_id) is not str:
            raise PortContractError("manifest segment_id must be text")
        if segment_id in selected:
            ordered.append(cast(dict[str, JsonValue], canonical_clone(segment)))
    observed = {cast(str, segment["segment_id"]) for segment in ordered}
    missing = sorted(selected - observed)
    if missing:
        raise PortContractError(f"selected segments are missing: {missing}")
    return ordered


def build_capability_query(
    manifest: Mapping[str, JsonValue],
    *,
    selected_segment_ids: list[str],
    required_capabilities: list[str],
    transport_mode: str,
    adapter_id: str,
    adapter_version: str,
    schema_locator: str,
    schema_sha256: str,
    binding_model_settings_descriptor: Mapping[str, JsonValue],
) -> FrozenEnvelope:
    """Build a complete content-, adapter-, schema-, and binding-bound query."""

    segments = _ordered_segments(manifest, selected_segment_ids)
    ordered_ids = [cast(str, segment["segment_id"]) for segment in segments]
    if type(required_capabilities) is not list or not required_capabilities:
        raise PortContractError("required_capabilities must be non-empty")
    if len(set(required_capabilities)) != len(required_capabilities):
        raise PortContractError("required capabilities must be unique")
    if any(type(item) is not str or not item for item in required_capabilities):
        raise PortContractError("required capabilities must be non-empty strings")

    characteristics: dict[str, JsonValue] = {
        "segments": [
            {
                "segment_id": cast(str, segment["segment_id"]),
                "speaker": cast(str, segment["speaker"]),
                "exact_text_sha256": cast(str, segment["exact_text_sha256"]),
                "unicode_codepoints": len(cast(str, segment["exact_text"])),
                "utf8_bytes": len(cast(str, segment["exact_text"]).encode("utf-8")),
                "has_leading_performance_tag": (
                    segment.get("leading_performance_tag") is not None
                ),
            }
            for segment in segments
        ],
        "selection_order": "manifest-order",
    }
    descriptor = cast(
        dict[str, JsonValue],
        canonical_clone(dict(binding_model_settings_descriptor)),
    )
    envelope = capability_query_envelope(
        manifest_digest=cast(str, manifest["digest"]),
        selected_segment_ids=ordered_ids,
        content_characteristics_digest=canonical_sha256(characteristics),
        required_capabilities=sorted(required_capabilities),
        transport_mode=transport_mode,
        adapter={"adapter_id": adapter_id, "adapter_version": adapter_version},
        provider_schema_basis={
            "locator": schema_locator,
            "sha256": _sha256(schema_sha256, "schema_sha256"),
        },
        binding_model_settings_descriptor_digest=canonical_sha256(descriptor),
    )
    return FrozenEnvelope(canonical_bytes(envelope), CAPABILITY_QUERY_SCHEMA_ID)


def evaluate_capabilities(
    query: Mapping[str, JsonValue],
    *,
    statuses: Mapping[str, str],
    evidence_basis: list[dict[str, JsonValue]],
    output_granularity: str = "segment",
) -> FrozenEnvelope:
    """Evaluate a query from explicit static evidence without optimistic defaults."""

    value = _envelope_value(query, CAPABILITY_QUERY_SCHEMA_ID)
    raw_requirements = value.get("required_capabilities")
    if type(raw_requirements) is not list:
        raise PortContractError("query required_capabilities must be a list")
    requirements = [cast(str, item) for item in raw_requirements]
    if set(statuses) != set(requirements):
        raise PortContractError(
            "capability statuses must exactly cover requested requirements"
        )
    decisions: list[CapabilityDecision] = []
    for requirement in requirements:
        status = statuses[requirement]
        if status not in _CAPABILITY_STATUSES:
            raise PortContractError(
                f"invalid capability status for {requirement!r}: {status!r}"
            )
        decisions.append(
            {
                "requirement_ref": requirement,
                "status": status,
                "evidence_links": [
                    f"evidence-basis-{index + 1:03d}"
                    for index in range(len(evidence_basis))
                ],
            }
        )
    envelope = capability_profile_envelope(
        query_digest=cast(str, query["digest"]),
        decisions=decisions,
        output_granularity=output_granularity,
        retry_granularity="segment" if output_granularity == "segment" else "unknown",
        idempotency_support="local-ledger-key-only",
        cancellation_support="unknown",
        evidence_basis=evidence_basis,
    )
    return FrozenEnvelope(canonical_bytes(envelope), CAPABILITY_PROFILE_SCHEMA_ID)


def prepare_segment_plan(
    manifest: Mapping[str, JsonValue],
    query: Mapping[str, JsonValue],
    profile: Mapping[str, JsonValue],
    *,
    projected_text_by_segment: Mapping[str, str] | None = None,
    transformation_approval_ref: str | None = None,
    output_descriptor: str = "synthetic-segment-artifact/v1",
    secret_resolver: Callable[..., object] | None = None,
) -> FrozenEnvelope:
    """Prepare one correlated synthetic expected output per selected segment.

    ``secret_resolver`` is accepted only to prove the preparation boundary.  It
    is deliberately never invoked; secret resolution belongs to later execution.
    """

    _ = secret_resolver
    manifest_value = _envelope_value(manifest, MANIFEST_SCHEMA_ID)
    query_value = _envelope_value(query, CAPABILITY_QUERY_SCHEMA_ID)
    profile_value = _envelope_value(profile, CAPABILITY_PROFILE_SCHEMA_ID)
    if query_value.get("manifest_digest") != manifest.get("digest"):
        raise PortContractError("query is stale for the manifest")
    if profile_value.get("query_digest") != query.get("digest"):
        raise PortContractError("capability profile is stale for the query")
    if profile_value.get("output_granularity") != "segment":
        raise PortContractError("segment plan requires segment output granularity")

    raw_decisions = profile_value.get("decisions")
    if type(raw_decisions) is not list:
        raise PortContractError("profile decisions must be a list")
    blocked: list[str] = []
    for raw in raw_decisions:
        if type(raw) is not dict:
            raise PortContractError("profile decision must be an object")
        decision = cast(dict[str, JsonValue], raw)
        if decision.get("status") not in {"supported", "translated"}:
            blocked.append(
                f"{decision.get('requirement_ref')}:{decision.get('status')}"
            )
    if blocked:
        raise MandatoryCapabilityBlocked(
            f"mandatory capabilities are blocked: {sorted(blocked)}"
        )

    selected_ids = cast(list[str], query_value["selected_segment_ids"])
    segments = _ordered_segments(manifest, selected_ids)
    projections = dict(projected_text_by_segment or {})
    unknown_projection_ids = sorted(set(projections) - set(selected_ids))
    if unknown_projection_ids:
        raise PortContractError(
            f"projections name unselected segments: {unknown_projection_ids}"
        )
    acceptance_policy = manifest_value.get("acceptance_policy")
    if type(acceptance_policy) is not dict:
        raise PortContractError("manifest acceptance_policy must be an object")
    approval_required = bool(
        acceptance_policy.get("transformations_require_approval")
    )

    records: list[ProjectionRecord] = []
    operations: list[PlannedOperation] = []
    expected_outputs: list[dict[str, JsonValue]] = []
    total_exact_bytes = 0
    total_projected_bytes = 0
    schema_basis = cast(
        dict[str, JsonValue],
        canonical_clone(cast(dict[str, JsonValue], query_value["provider_schema_basis"])),
    )
    for ordinal, segment in enumerate(segments, start=1):
        segment_id = cast(str, segment["segment_id"])
        exact_text = cast(str, segment["exact_text"])
        projected_text = projections.get(segment_id, exact_text)
        if type(projected_text) is not str or not projected_text:
            raise PortContractError("projected text must be non-empty")
        changed = projected_text != exact_text
        if changed and approval_required and not transformation_approval_ref:
            raise ProjectionApprovalRequired(
                f"projection approval is required for {segment_id}"
            )
        exact_digest = hashlib.sha256(exact_text.encode("utf-8")).hexdigest()
        projected_digest = hashlib.sha256(
            projected_text.encode("utf-8")
        ).hexdigest()
        transformations: list[dict[str, JsonValue]] = []
        if changed:
            transformations.append(
                {
                    "ordinal": 1,
                    "kind": "explicit-text-projection",
                    "source_sha256": exact_digest,
                    "result_sha256": projected_digest,
                }
            )
        record: dict[str, JsonValue] = {
            "segment_id": segment_id,
            "exact_text": exact_text,
            "exact_text_sha256": exact_digest,
            "projected_text": projected_text,
            "projected_text_sha256": projected_digest,
            "transformations": transformations,
        }
        if changed:
            record["approval_ref"] = cast(str, transformation_approval_ref)
        records.append(cast(ProjectionRecord, record))

        expected = {
            "expected_output_id": f"expected-output-{ordinal:03d}",
            "segment_id": segment_id,
            "output_granularity": "segment",
            "correlation_method": "segment-id",
            "correlation_confidence": "certain",
            "output_descriptor": output_descriptor,
        }
        payload: dict[str, JsonValue] = {
            "segment_id": segment_id,
            "speaker": cast(str, segment["speaker"]),
            "projected_text": projected_text,
            "projected_text_sha256": projected_digest,
            "schema_basis": schema_basis,
            "output_descriptor": output_descriptor,
        }
        payload_digest = canonical_sha256(payload)
        fingerprint = canonical_sha256(
            {
                "payload_sha256": payload_digest,
                "expected_output": expected,
                "correlation_context": segment_id,
            }
        )
        operations.append(
            {
                "operation_id": f"operation-{ordinal:03d}",
                "operation_fingerprint": fingerprint,
                "submission_key": f"local-{fingerprint}",
                "selected_segment_ids": [segment_id],
                "projected_payload_sha256": payload_digest,
                "expected_output_granularity": "segment",
            }
        )
        expected_outputs.append(expected)
        total_exact_bytes += len(exact_text.encode("utf-8"))
        total_projected_bytes += len(projected_text.encode("utf-8"))

    envelope = plan_envelope(
        manifest_digest=cast(str, manifest["digest"]),
        capability_profile_digest=cast(str, profile["digest"]),
        selected_segment_ids=[cast(str, item) for item in selected_ids],
        operations=operations,
        expected_outputs=expected_outputs,
        effect_estimates={
            "operation_count": len(operations),
            "exact_text_utf8_bytes": total_exact_bytes,
            "projected_text_utf8_bytes": total_projected_bytes,
            "external_effects": 0,
        },
        warnings=["synthetic preparation only; no provider execution evidence"],
        blocked_requirements=[],
        transformations=records,
        native_schema_basis=schema_basis,
    )
    return FrozenEnvelope(canonical_bytes(envelope), PLAN_SCHEMA_ID)
