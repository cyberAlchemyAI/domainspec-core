"""Honest no-network synthetic adapters for L0 contract tests."""

from __future__ import annotations

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
from .contracts import MANIFEST_SCHEMA_ID, PLAN_SCHEMA_ID, plan_envelope
from .port import (
    FrozenEnvelope,
    MandatoryCapabilityBlocked,
    PortContractError,
    build_capability_query,
    evaluate_capabilities,
    prepare_segment_plan,
)


class CompositeContractError(PortContractError):
    """Raised when a synthetic composite projection is inconsistent."""


class SegmentRetryDenied(CompositeContractError):
    """Raised when composite evidence cannot support segment retry."""


@dataclass(frozen=True, slots=True)
class FrozenCompositeProjection:
    """Immutable canonical bytes for a synthetic composite observation."""

    canonical_bytes_value: bytes

    def __post_init__(self) -> None:
        value = self.value
        if value.get("schema_version") != "synthetic-composite-projection/v1":
            raise CompositeContractError("unexpected composite projection schema")

    @property
    def value(self) -> dict[str, JsonValue]:
        parsed = canonical_loads(self.canonical_bytes_value)
        if type(parsed) is not dict:
            raise CompositeContractError("composite projection must be an object")
        return cast(dict[str, JsonValue], parsed)

    @property
    def digest(self) -> str:
        return canonical_sha256(self.value)


def _manifest_value(
    manifest: Mapping[str, JsonValue],
) -> dict[str, JsonValue]:
    if type(manifest) is not dict:
        raise CompositeContractError("manifest envelope must be an object")
    envelope = cast(dict[str, JsonValue], canonical_clone(dict(manifest)))
    require_valid_envelope(envelope)
    if envelope.get("schema_id") != MANIFEST_SCHEMA_ID:
        raise CompositeContractError("project fake requires a manifest envelope")
    value = envelope.get("value")
    if type(value) is not dict:
        raise CompositeContractError("manifest value must be an object")
    return cast(dict[str, JsonValue], value)


@dataclass(frozen=True, slots=True)
class FakeSegmentAdapter:
    """Static segment-granularity preparation fake.

    It returns contract evidence about its synthetic schema only.  It neither
    submits work nor manufactures provider/account success evidence.
    """

    adapter_id: str
    adapter_version: str
    schema_locator: str
    schema_sha256: str
    unknown_requirements: tuple[str, ...] = (
        "account-entitlement",
        "live-account-evidence",
    )

    def query(
        self,
        manifest: Mapping[str, JsonValue],
        *,
        selected_segment_ids: list[str],
        required_capabilities: list[str],
        transport_mode: str,
        binding_model_settings_descriptor: Mapping[str, JsonValue],
    ) -> FrozenEnvelope:
        return build_capability_query(
            manifest,
            selected_segment_ids=selected_segment_ids,
            required_capabilities=required_capabilities,
            transport_mode=transport_mode,
            adapter_id=self.adapter_id,
            adapter_version=self.adapter_version,
            schema_locator=self.schema_locator,
            schema_sha256=self.schema_sha256,
            binding_model_settings_descriptor=binding_model_settings_descriptor,
        )

    def evaluate(self, query: FrozenEnvelope) -> FrozenEnvelope:
        requirements = query.value["required_capabilities"]
        statuses = {
            str(requirement): (
                "unknown"
                if str(requirement) in self.unknown_requirements
                else "supported"
            )
            for requirement in requirements
        }
        return evaluate_capabilities(
            query.as_envelope(),
            statuses=statuses,
            evidence_basis=[
                {
                    "evidence_id": "evidence-basis-001",
                    "kind": "synthetic-schema-fixture",
                    "locator": self.schema_locator,
                    "sha256": self.schema_sha256,
                    "live_account_evidence": False,
                }
            ],
            output_granularity="segment",
        )

    def prepare(
        self,
        manifest: Mapping[str, JsonValue],
        query: FrozenEnvelope,
        profile: FrozenEnvelope,
        *,
        projected_text_by_segment: Mapping[str, str] | None = None,
        transformation_approval_ref: str | None = None,
        output_descriptor: str = "synthetic-segment-artifact/v1",
        secret_resolver: Callable[..., object] | None = None,
    ) -> FrozenEnvelope:
        return prepare_segment_plan(
            manifest,
            query.as_envelope(),
            profile.as_envelope(),
            projected_text_by_segment=projected_text_by_segment,
            transformation_approval_ref=transformation_approval_ref,
            output_descriptor=output_descriptor,
            secret_resolver=secret_resolver,
        )


@dataclass(frozen=True, slots=True)
class FakeProjectAdapter:
    """Synthetic project fake with honest composite granularity."""

    adapter_id: str
    adapter_version: str
    schema_locator: str
    schema_sha256: str
    unknown_requirements: tuple[str, ...] = (
        "account-entitlement",
        "live-account-evidence",
    )

    def query(
        self,
        manifest: Mapping[str, JsonValue],
        *,
        selected_segment_ids: list[str],
        required_capabilities: list[str],
        transport_mode: str,
        binding_model_settings_descriptor: Mapping[str, JsonValue],
    ) -> FrozenEnvelope:
        return build_capability_query(
            manifest,
            selected_segment_ids=selected_segment_ids,
            required_capabilities=required_capabilities,
            transport_mode=transport_mode,
            adapter_id=self.adapter_id,
            adapter_version=self.adapter_version,
            schema_locator=self.schema_locator,
            schema_sha256=self.schema_sha256,
            binding_model_settings_descriptor=binding_model_settings_descriptor,
        )

    def evaluate(self, query: FrozenEnvelope) -> FrozenEnvelope:
        requirements = query.value["required_capabilities"]
        statuses = {
            str(requirement): (
                "unknown"
                if str(requirement) in self.unknown_requirements
                else "supported"
            )
            for requirement in requirements
        }
        return evaluate_capabilities(
            query.as_envelope(),
            statuses=statuses,
            evidence_basis=[
                {
                    "evidence_id": "composite-evidence-basis-001",
                    "kind": "synthetic-project-schema-fixture",
                    "locator": self.schema_locator,
                    "sha256": self.schema_sha256,
                    "live_account_evidence": False,
                }
            ],
            output_granularity="composite",
        )

    def prepare(
        self,
        manifest: Mapping[str, JsonValue],
        query: FrozenEnvelope,
        profile: FrozenEnvelope,
        *,
        output_descriptor: str = "synthetic-composite-placeholder/v1",
        secret_resolver: Callable[..., object] | None = None,
    ) -> FrozenEnvelope:
        """Prepare one composite operation without resolving any secret."""

        _ = secret_resolver
        manifest_value = _manifest_value(manifest)
        query_value = query.value
        profile_value = profile.value
        if query_value.get("manifest_digest") != manifest.get("digest"):
            raise CompositeContractError("query is stale for the manifest")
        if profile_value.get("query_digest") != query.digest:
            raise CompositeContractError("profile is stale for the query")
        if profile_value.get("output_granularity") != "composite":
            raise CompositeContractError(
                "project fake requires composite output granularity"
            )

        decisions = profile_value.get("decisions")
        if type(decisions) is not list:
            raise CompositeContractError("profile decisions must be a list")
        blocked = [
            f"{item.get('requirement_ref')}:{item.get('status')}"
            for item in decisions
            if type(item) is dict
            and item.get("status") not in {"supported", "translated"}
        ]
        if blocked:
            raise MandatoryCapabilityBlocked(
                f"mandatory capabilities are blocked: {sorted(blocked)}"
            )

        selected_ids = query_value.get("selected_segment_ids")
        if type(selected_ids) is not list or not selected_ids:
            raise CompositeContractError("selected segments must be non-empty")
        raw_segments = manifest_value.get("segments")
        if type(raw_segments) is not list:
            raise CompositeContractError("manifest segments must be a list")
        by_id = {
            item["segment_id"]: item
            for item in raw_segments
            if type(item) is dict and type(item.get("segment_id")) is str
        }
        missing = [item for item in selected_ids if item not in by_id]
        if missing:
            raise CompositeContractError(f"selected segments are missing: {missing}")

        schema_basis = cast(
            dict[str, JsonValue],
            canonical_clone(
                cast(dict[str, JsonValue], query_value["provider_schema_basis"])
            ),
        )
        group_seed: dict[str, JsonValue] = {
            "manifest_digest": cast(str, manifest["digest"]),
            "profile_digest": profile.digest,
            "selected_segment_ids": cast(list[JsonValue], selected_ids),
            "output_descriptor": output_descriptor,
            "schema_basis": schema_basis,
        }
        group_id = f"composite-group-{canonical_sha256(group_seed)[:16]}"
        payload: dict[str, JsonValue] = {
            "composite_group_id": group_id,
            "selected_segments": [
                {
                    "segment_id": segment_id,
                    "exact_text_sha256": by_id[segment_id]["exact_text_sha256"],
                }
                for segment_id in selected_ids
            ],
            "output_descriptor": output_descriptor,
            "schema_basis": schema_basis,
        }
        payload_digest = canonical_sha256(payload)
        expected: dict[str, JsonValue] = {
            "expected_output_id": "expected-composite-001",
            "output_granularity": "composite",
            "composite_group_id": group_id,
            "segment_ids": cast(list[JsonValue], selected_ids),
            "correlation_method": "none",
            "correlation_confidence": "unknown",
            "output_descriptor": output_descriptor,
        }
        fingerprint = canonical_sha256(
            {
                "payload_sha256": payload_digest,
                "expected_output": expected,
                "correlation_context": group_id,
            }
        )
        transformations = [
            {
                "segment_id": segment_id,
                "exact_text": by_id[segment_id]["exact_text"],
                "exact_text_sha256": by_id[segment_id]["exact_text_sha256"],
                "projected_text": by_id[segment_id]["exact_text"],
                "projected_text_sha256": by_id[segment_id]["exact_text_sha256"],
                "transformations": [],
            }
            for segment_id in selected_ids
        ]
        envelope = plan_envelope(
            manifest_digest=cast(str, manifest["digest"]),
            capability_profile_digest=profile.digest,
            selected_segment_ids=cast(list[str], selected_ids),
            operations=[
                {
                    "operation_id": "operation-composite-001",
                    "operation_fingerprint": fingerprint,
                    "submission_key": f"local-{fingerprint}",
                    "selected_segment_ids": cast(list[str], selected_ids),
                    "projected_payload_sha256": payload_digest,
                    "expected_output_granularity": "composite",
                    "composite_group_id": group_id,
                }
            ],
            expected_outputs=[expected],
            effect_estimates={
                "operation_count": 1,
                "selected_segment_count": len(selected_ids),
                "external_effects": 0,
            },
            warnings=[
                "synthetic composite preparation only; no native effect evidence"
            ],
            blocked_requirements=[],
            transformations=transformations,
            native_schema_basis=schema_basis,
        )
        return FrozenEnvelope(canonical_bytes(envelope), PLAN_SCHEMA_ID)

    def project(
        self,
        plan: FrozenEnvelope,
        *,
        correlation_map: Mapping[str, str] | None = None,
        secret_resolver: Callable[..., object] | None = None,
    ) -> FrozenCompositeProjection:
        """Project one non-materialized composite placeholder observation."""

        _ = secret_resolver
        plan_value = plan.value
        selected_ids = plan_value.get("selected_segment_ids")
        expected_outputs = plan_value.get("expected_outputs")
        operations = plan_value.get("operations")
        if type(selected_ids) is not list or not selected_ids:
            raise CompositeContractError("composite plan selection is empty")
        if type(expected_outputs) is not list or len(expected_outputs) != 1:
            raise CompositeContractError("composite plan must expect one output")
        if type(operations) is not list or len(operations) != 1:
            raise CompositeContractError("composite plan must contain one operation")
        expected = expected_outputs[0]
        if type(expected) is not dict:
            raise CompositeContractError("expected composite output must be an object")
        if expected.get("output_granularity") != "composite":
            raise CompositeContractError("expected output is not composite")
        group_id = expected.get("composite_group_id")
        if type(group_id) is not str or not group_id:
            raise CompositeContractError("composite group id is missing")

        if correlation_map is None:
            correlation_value: dict[str, str] | None = None
            correlation_digest: str | None = None
            method = "none"
            confidence = "unknown"
            state = "unknown"
        else:
            correlation_value = dict(correlation_map)
            if set(correlation_value) != set(selected_ids):
                raise CompositeContractError(
                    "correlation map must exactly cover selected segments"
                )
            if any(type(value) is not str or not value for value in correlation_value.values()):
                raise CompositeContractError(
                    "correlation references must be non-empty strings"
                )
            if len(set(correlation_value.values())) != len(correlation_value):
                raise CompositeContractError("correlation references must be unique")
            correlation_digest = canonical_sha256(correlation_value)
            method = "explicit-synthetic-map"
            confidence = "synthetic-derived"
            state = "correlated"

        artifact_sha256 = canonical_sha256(
            {
                "plan_digest": plan.digest,
                "composite_group_id": group_id,
                "output_descriptor": expected.get("output_descriptor"),
            }
        )
        artifact: dict[str, JsonValue] = {
            "artifact_id": "synthetic-composite-artifact-001",
            "sha256": artifact_sha256,
            "classification": "synthetic-placeholder",
            "materialized": False,
        }
        segment_states: list[dict[str, JsonValue]] = [
            {
                "segment_id": segment_id,
                "state": state,
                "correlation_ref": (
                    correlation_value[segment_id]
                    if correlation_value is not None
                    else None
                ),
                "correlation_method": method,
                "correlation_confidence": confidence,
            }
            for segment_id in selected_ids
        ]
        receipt_input: dict[str, JsonValue] = {
            "plan_digest": plan.digest,
            "output_granularity": "composite",
            "composite_group_id": group_id,
            "artifact": artifact,
            "segment_states": segment_states,
            "correlation_map_digest": correlation_digest,
            "correlation_method": method,
            "correlation_confidence": confidence,
        }
        receipt_input_digest = canonical_sha256(receipt_input)
        gate_input: dict[str, JsonValue] = {
            "receipt_input_digest": receipt_input_digest,
            "reviewed_artifact_sha256s": [artifact_sha256],
            "criteria_results": [
                {
                    "criterion": "composite-correlation-honesty",
                    "observed_method": method,
                    "observed_confidence": confidence,
                    "correlation_map_digest": correlation_digest,
                }
            ],
        }
        value: dict[str, JsonValue] = {
            "schema_version": "synthetic-composite-projection/v1",
            "plan_digest": plan.digest,
            "output_granularity": "composite",
            "composite_group_id": group_id,
            "native_project_ref": f"synthetic-project:{group_id}",
            "artifacts": [artifact],
            "segment_states": segment_states,
            "correlation_map": correlation_value,
            "correlation_map_digest": correlation_digest,
            "correlation_method": method,
            "correlation_confidence": confidence,
            "receipt_input_digest": receipt_input_digest,
            "gate_input_digest": canonical_sha256(gate_input),
        }
        return FrozenCompositeProjection(canonical_bytes(value))

    def prepare_segment_retry(
        self,
        projection: FrozenCompositeProjection,
        segment_ids: list[str],
    ) -> None:
        _ = projection.value
        _ = segment_ids
        raise SegmentRetryDenied(
            "segment retry denied: composite projection has no native "
            "segment-completion evidence"
        )
