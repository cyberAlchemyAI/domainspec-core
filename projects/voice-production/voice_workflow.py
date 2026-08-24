"""Deterministic, provider-neutral, no-network voice workflow demonstration.

The module composes the L0 compiler, preparation ports, synthetic adapters,
authorization/evidence gates, and reconciliation ledger.  It can read a local
CSV at the CLI edge, but it cannot contact a provider, resolve credentials, or
materialize audio.  Its only output is a redacted canonical JSON summary.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Callable, Mapping, Protocol, Sequence, cast

from voice_production.canonical import (
    JsonValue,
    canonical_bytes,
    canonical_clone,
    canonical_loads,
    canonical_sha256,
    canonical_text,
    make_envelope,
)
from voice_production.compiler import compile_manifest
from voice_production.compiler_config import (
    CompilerConfig,
    compiler_config_from_json_bytes,
)
from voice_production.contracts import CAPABILITY_QUERY_SCHEMA_ID, manifest_envelope
from voice_production.evidence import (
    REQUIRED_PREREQUISITE_KINDS,
    ArtifactRecord,
    AuthorizationRejected,
    ClaimEvidence,
    ClaimRecord,
    CriterionResult,
    EvidenceContractError,
    ProtectedPrerequisite,
    build_execution_authorization,
    build_gate_receipt,
    build_normalized_receipt,
    validate_execution_authorization,
    validate_gate_receipt,
)
from voice_production.fakes import (
    FakeProjectAdapter,
    FakeSegmentAdapter,
    FrozenCompositeProjection,
    SegmentRetryDenied,
)
from voice_production.factory_handoff import (
    FactoryHandoffError,
    validate_factory_handoff,
)
from voice_production.lifecycle import (
    AttemptObservation,
    ReconciliationEvidence,
    UnknownEffectBlocked,
    build_operation_ledger,
    prepare_bounded_retry,
    reconcile_unknown,
    record_submission,
)
from voice_production.port import (
    FrozenEnvelope,
    MandatoryCapabilityBlocked,
    ProjectionApprovalRequired,
)


SUMMARY_SCHEMA = "voice-workflow-summary/v1"
CLAIM_CEILING = "the synthetic seam passed the declared no-network contract tests"
TOY_SEGMENT_IDS = ("segment-001", "segment-002", "segment-003")
SEGMENT_REQUIREMENTS = (
    "correlated-segment-output",
    "exact-text-ledger",
    "static-effect-estimate",
    "transformation-ledger",
)
PROJECT_REQUIREMENTS = (
    "composite-output",
    "project-reference",
    "correlation-honesty",
)
ACCOUNT_REF = "synthetic-account-A"
EXECUTION_SCOPE = "synthetic/toy/segments-001-003"
NOW = "2026-08-09T12:00:00Z"
EXPIRES_AT = "2026-09-01T00:00:00Z"


class WorkflowContractError(ValueError):
    """Raised when a declared toy-game assertion does not hold."""


class SegmentPreparationAdapter(Protocol):
    """Provider-neutral segment preparation seam."""

    def query(
        self,
        manifest: Mapping[str, JsonValue],
        *,
        selected_segment_ids: list[str],
        required_capabilities: list[str],
        transport_mode: str,
        binding_model_settings_descriptor: Mapping[str, JsonValue],
    ) -> FrozenEnvelope: ...

    def evaluate(self, query: FrozenEnvelope) -> FrozenEnvelope: ...

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
    ) -> FrozenEnvelope: ...


class ProjectPreparationAdapter(Protocol):
    """Provider-neutral composite preparation and projection seam."""

    def query(
        self,
        manifest: Mapping[str, JsonValue],
        *,
        selected_segment_ids: list[str],
        required_capabilities: list[str],
        transport_mode: str,
        binding_model_settings_descriptor: Mapping[str, JsonValue],
    ) -> FrozenEnvelope: ...

    def evaluate(self, query: FrozenEnvelope) -> FrozenEnvelope: ...

    def prepare(
        self,
        manifest: Mapping[str, JsonValue],
        query: FrozenEnvelope,
        profile: FrozenEnvelope,
        *,
        output_descriptor: str = "synthetic-composite-placeholder/v1",
        secret_resolver: Callable[..., object] | None = None,
    ) -> FrozenEnvelope: ...

    def project(
        self,
        plan: FrozenEnvelope,
        *,
        correlation_map: Mapping[str, str] | None = None,
        secret_resolver: Callable[..., object] | None = None,
    ) -> FrozenCompositeProjection: ...

    def prepare_segment_retry(
        self,
        projection: FrozenCompositeProjection,
        segment_ids: list[str],
    ) -> None: ...


@dataclass(frozen=True, slots=True)
class AdapterBundle:
    """Injected adapter pair; no provider SDK type crosses this boundary."""

    segment: SegmentPreparationAdapter
    project: ProjectPreparationAdapter


@dataclass(frozen=True, slots=True)
class FrozenWorkflowSummary:
    """Immutable canonical bytes for the redacted workflow result."""

    canonical_bytes_value: bytes

    def __post_init__(self) -> None:
        if type(self.canonical_bytes_value) is not bytes:
            raise TypeError("canonical_bytes_value must be bytes")
        if self.value.get("schema_version") != SUMMARY_SCHEMA:
            raise WorkflowContractError("unexpected workflow summary schema")

    @property
    def value(self) -> dict[str, JsonValue]:
        parsed = canonical_loads(self.canonical_bytes_value)
        if type(parsed) is not dict:
            raise WorkflowContractError("workflow summary must be an object")
        return cast(dict[str, JsonValue], parsed)

    @property
    def digest(self) -> str:
        return canonical_sha256(self.value)

    def text(self) -> str:
        return canonical_text(self.value)


@dataclass(slots=True)
class _ResolverSpy:
    calls: int = 0

    def __call__(self, *_args: object, **_kwargs: object) -> object:
        self.calls += 1
        raise AssertionError("credential resolution is outside the L0 workflow")


def default_adapters() -> AdapterBundle:
    """Return deterministic synthetic implementations of the neutral seam."""

    return AdapterBundle(
        segment=FakeSegmentAdapter(
            adapter_id="synthetic-segment",
            adapter_version="1.0.0",
            schema_locator="synthetic-schema://segment/v1",
            schema_sha256=_sha(b"synthetic-segment-schema-v1"),
        ),
        project=FakeProjectAdapter(
            adapter_id="synthetic-project",
            adapter_version="1.0.0",
            schema_locator="synthetic-schema://project/v1",
            schema_sha256=_sha(b"synthetic-project-schema-v1"),
        ),
    )


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _object(value: JsonValue, name: str) -> dict[str, JsonValue]:
    if type(value) is not dict:
        raise WorkflowContractError(f"{name} must be an object")
    return cast(dict[str, JsonValue], value)


def _list(value: JsonValue, name: str) -> list[JsonValue]:
    if type(value) is not list:
        raise WorkflowContractError(f"{name} must be a list")
    return cast(list[JsonValue], value)


def _toy_manifest(
    chapter_manifest: Mapping[str, JsonValue],
) -> tuple[dict[str, JsonValue], bytes]:
    chapter_value = _object(chapter_manifest.get("value"), "manifest.value")
    source_segments = _list(chapter_value.get("segments"), "manifest.segments")
    if len(source_segments) < len(TOY_SEGMENT_IDS):
        raise WorkflowContractError("Chapter fixture cannot supply the toy selection")
    selected = cast(
        list[dict[str, JsonValue]],
        canonical_clone(source_segments[: len(TOY_SEGMENT_IDS)]),
    )
    observed = tuple(item.get("segment_id") for item in selected)
    if observed != TOY_SEGMENT_IDS:
        raise WorkflowContractError("toy selection no longer matches source order")
    toy_source_value: list[JsonValue] = [
        {
            "speaker": cast(str, segment["speaker"]),
            "line": cast(str, segment["exact_text"]),
        }
        for segment in selected
    ]
    toy_source_bytes = canonical_bytes(toy_source_value)
    tagged_count = sum(
        item.get("leading_performance_tag") is not None for item in selected
    )
    envelope = manifest_envelope(
        production_id="synthetic-toy.voice-production",
        source={
            "locator": "inline:chapter-01-first-three",
            "sha256": _sha(toy_source_bytes),
            "size_bytes": len(toy_source_bytes),
            "media_type": "application/json",
            "profile": "three-segment-toy/v1",
        },
        segments=selected,
        output_policy={
            "segment_order": "source-row-order",
            "text_representation": "exact",
            "default_output_granularity": "segment",
        },
        acceptance_policy={
            "allowed_speakers": sorted(
                {cast(str, item["speaker"]) for item in selected}
            ),
            "expected_segment_count": len(selected),
            "expected_tagged_row_count": tagged_count,
            "performance_tag_profile": "explicit-leading-bracket/v1",
            "transformations_require_approval": True,
        },
    )
    return cast(dict[str, JsonValue], envelope), toy_source_bytes


def _mutated_envelope(
    envelope: Mapping[str, JsonValue],
    mutate: Callable[[dict[str, JsonValue]], None],
) -> dict[str, JsonValue]:
    value = _object(canonical_clone(envelope.get("value")), "envelope.value")
    mutate(value)
    return make_envelope(
        cast(str, envelope["schema_id"]),
        value,
        schema_version=cast(str, envelope["schema_version"]),
    )


def _frozen_query(envelope: dict[str, JsonValue]) -> FrozenEnvelope:
    return FrozenEnvelope(canonical_bytes(envelope), CAPABILITY_QUERY_SCHEMA_ID)


def _prerequisites() -> tuple[ProtectedPrerequisite, ...]:
    return tuple(
        ProtectedPrerequisite(
            kind=kind,
            evidence_id=f"synthetic-prerequisite-{index:03d}",
            evidence_sha256=_sha(f"synthetic-prerequisite:{kind}".encode()),
            accepted=True,
            expires_at=EXPIRES_AT,
        )
        for index, kind in enumerate(sorted(REQUIRED_PREREQUISITE_KINDS), start=1)
    )


def _authorization(
    plan: Mapping[str, JsonValue],
    *,
    authorization_id: str,
    account_ref: str = ACCOUNT_REF,
    execution_scope: str = EXECUTION_SCOPE,
    expires_at: str = EXPIRES_AT,
    max_effect_units: int | None = None,
):
    plan_value = _object(plan.get("value"), "plan.value")
    estimates = _object(plan_value.get("effect_estimates"), "effect_estimates")
    units = cast(int, estimates["projected_text_utf8_bytes"])
    return build_execution_authorization(
        plan,
        authorization_id=authorization_id,
        account_ref=account_ref,
        execution_scope=execution_scope,
        issued_at="2026-08-09T00:00:00Z",
        expires_at=expires_at,
        max_effect_units=units if max_effect_units is None else max_effect_units,
        prerequisite_evidence=_prerequisites(),
    )


def _expect_authorization_rejection(
    name: str,
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue] | None,
    *,
    account_ref: str,
    execution_scope: str,
    resolver: _ResolverSpy,
) -> str:
    try:
        validate_execution_authorization(
            plan,
            authorization,
            expected_account_ref=account_ref,
            expected_scope=execution_scope,
            now=NOW,
            secret_resolver=resolver,
        )
    except AuthorizationRejected:
        return name
    raise WorkflowContractError(f"authorization case did not reject: {name}")


def _record_outcomes(
    plan: FrozenEnvelope,
    authorization,
    resolver: _ResolverSpy,
):
    plan_envelope = plan.as_envelope()
    ledger = build_operation_ledger(
        plan_envelope,
        authorization.as_envelope(),
        run_id="synthetic-toy-run-001",
        provider_idempotency_support="unsupported",
    )
    states = ("accepted", "rejected-no-effect", "unknown")
    operations = _list(plan.value.get("operations"), "plan.operations")
    artifact_sha = _sha(b"synthetic accepted artifact placeholder")
    for ordinal, (raw_operation, state) in enumerate(
        zip(operations, states, strict=True), start=1
    ):
        operation = _object(raw_operation, "plan.operation")
        observation = AttemptObservation(
            response_state=state,
            evidence_id=f"synthetic-response-{ordinal:03d}",
            evidence_sha256=_sha(f"synthetic-response:{state}".encode()),
            observed_at=f"2026-08-09T12:1{ordinal}:01Z",
            native_effect_ref=(
                "synthetic-effect:operation-001" if state == "accepted" else None
            ),
            accepted_artifact_sha256s=(
                (artifact_sha,) if state == "accepted" else ()
            ),
        )
        ledger = record_submission(
            ledger.as_envelope(),
            plan=plan_envelope,
            authorization=authorization.as_envelope(),
            operation_id=cast(str, operation["operation_id"]),
            sent_payload_sha256=cast(str, operation["projected_payload_sha256"]),
            submitted_at=f"2026-08-09T12:1{ordinal}:00Z",
            observation=observation,
            secret_resolver=resolver,
        )

    try:
        prepare_bounded_retry(
            plan_envelope,
            ledger.as_envelope(),
            authorization.as_envelope(),
            requested_operation_ids=("operation-003",),
            max_retry_operations=3,
            max_retry_depth=2,
            new_authorization_id="synthetic-retry-before-reconcile",
            account_ref=ACCOUNT_REF,
            execution_scope=EXECUTION_SCOPE,
            issued_at=NOW,
            expires_at=EXPIRES_AT,
            max_effect_units=10_000,
            prerequisite_evidence=_prerequisites(),
            secret_resolver=resolver,
        )
    except UnknownEffectBlocked:
        retry_blocked_before_reconciliation = True
    else:
        raise WorkflowContractError("unknown response was retryable without reconciliation")

    ledger_operations = _list(ledger.value.get("operations"), "ledger.operations")
    unknown_operation = _object(ledger_operations[2], "unknown operation")
    attempts = _list(unknown_operation.get("submission_attempts"), "submission attempts")
    attempt = _object(attempts[0], "submission attempt")
    ledger = reconcile_unknown(
        ledger.as_envelope(),
        plan=plan_envelope,
        authorization=authorization.as_envelope(),
        operation_id="operation-003",
        attempt_id=cast(str, attempt["attempt_id"]),
        evidence=ReconciliationEvidence(
            outcome="no-effect",
            evidence_id="synthetic-reconciliation-001",
            evidence_sha256=_sha(b"synthetic reconciliation no effect"),
            observed_at="2026-08-09T12:20:00Z",
        ),
        secret_resolver=resolver,
    )
    retry = prepare_bounded_retry(
        plan_envelope,
        ledger.as_envelope(),
        authorization.as_envelope(),
        requested_operation_ids=(
            "operation-001",
            "operation-002",
            "operation-003",
        ),
        max_retry_operations=3,
        max_retry_depth=2,
        new_authorization_id="synthetic-retry-001",
        account_ref=ACCOUNT_REF,
        execution_scope=EXECUTION_SCOPE,
        issued_at=NOW,
        expires_at=EXPIRES_AT,
        max_effect_units=10_000,
        prerequisite_evidence=_prerequisites(),
        secret_resolver=resolver,
    )
    return ledger, retry, retry_blocked_before_reconciliation


def _gate_mutation_rejections(
    *,
    plan: FrozenEnvelope,
    authorization,
    receipt,
    gate,
    artifact: ArtifactRecord,
    criterion: CriterionResult,
    claim: ClaimRecord,
    evidence: ClaimEvidence,
) -> list[str]:
    rejected: list[str] = []
    changed_artifact = ArtifactRecord.from_bytes(
        artifact_id=artifact.artifact_id,
        content=b"changed synthetic artifact placeholder",
        classification=artifact.classification,
        materialized=False,
    )
    changed_criterion = CriterionResult(
        criterion_id=criterion.criterion_id,
        passed=False,
        observed_result="synthetic criterion changed",
        evidence_link_ids=criterion.evidence_link_ids,
    )
    changed_evidence = ClaimEvidence(
        evidence_id=evidence.evidence_id,
        claim_id=evidence.claim_id,
        claim_type=evidence.claim_type,
        native_locator=evidence.native_locator,
        native_sha256=_sha(b"changed synthetic observation"),
        observed_at=evidence.observed_at,
        classification=evidence.classification,
        redaction_profile=evidence.redaction_profile,
    )
    changed_receipt = build_normalized_receipt(
        plan.as_envelope(),
        authorization.as_envelope(),
        run_id="synthetic-evidence-run-001",
        output_granularity="segment",
        claims=(claim,),
        evidence_links=(changed_evidence,),
        artifacts=(artifact,),
        reconciliation_state={"status": "known"},
    )
    changed_authorization = _authorization(
        plan.as_envelope(),
        authorization_id="synthetic-authorization-changed",
        account_ref="synthetic-account-B",
    )
    cases = {
        "artifact": (
            receipt,
            authorization,
            (changed_artifact,),
            (criterion,),
        ),
        "evidence": (
            changed_receipt,
            authorization,
            (artifact,),
            (criterion,),
        ),
        "criterion": (
            receipt,
            authorization,
            (artifact,),
            (changed_criterion,),
        ),
        "authorization": (
            receipt,
            changed_authorization,
            (artifact,),
            (criterion,),
        ),
    }
    for name, (current_receipt, current_authorization, artifacts, criteria) in cases.items():
        try:
            validate_gate_receipt(
                gate.as_envelope(),
                receipt=current_receipt.as_envelope(),
                plan=plan.as_envelope(),
                authorization=current_authorization.as_envelope(),
                reviewed_artifacts=artifacts,
                criteria_results=criteria,
            )
        except EvidenceContractError:
            rejected.append(name)
        else:
            raise WorkflowContractError(f"gate mutation did not reject: {name}")
    return sorted(rejected)


def _binding_proofs(
    *,
    source_bytes: bytes,
    compiler_config: CompilerConfig,
    chapter_manifest: Mapping[str, JsonValue],
    toy_manifest: Mapping[str, JsonValue],
    segment_adapter: SegmentPreparationAdapter,
    query: FrozenEnvelope,
    profile: FrozenEnvelope,
    plan: FrozenEnvelope,
    transformed_plan: FrozenEnvelope,
    binding: Mapping[str, JsonValue],
) -> dict[str, JsonValue]:
    base_digest = cast(str, toy_manifest["digest"])
    changed_source = source_bytes.replace(b"Presentation", b"presentation", 1)
    if changed_source == source_bytes:
        raise WorkflowContractError("source mutation fixture was not found")
    rebound_manifest = compile_manifest(
        changed_source,
        config=replace(
            compiler_config,
            expected_source_sha256=_sha(changed_source),
        ),
    ).as_envelope()

    def mutate_text(value: dict[str, JsonValue]) -> None:
        segments = _list(value["segments"], "segments")
        first = _object(segments[0], "segment")
        text = cast(str, first["exact_text"]) + "!"
        first["exact_text"] = text
        first["exact_text_sha256"] = _sha(text.encode())

    def mutate_policy(value: dict[str, JsonValue]) -> None:
        policy = _object(value["acceptance_policy"], "acceptance_policy")
        policy["expected_segment_count"] = 4

    def mutate_payload(value: dict[str, JsonValue]) -> None:
        operations = _list(value["operations"], "operations")
        operation = _object(operations[0], "operation")
        operation["projected_payload_sha256"] = _sha(b"changed payload")

    def mutate_output(value: dict[str, JsonValue]) -> None:
        outputs = _list(value["expected_outputs"], "expected_outputs")
        output = _object(outputs[0], "expected output")
        output["output_descriptor"] = "synthetic-segment-artifact/v2"

    def mutate_estimate(value: dict[str, JsonValue]) -> None:
        estimates = _object(value["effect_estimates"], "effect_estimates")
        estimates["projected_text_utf8_bytes"] = (
            cast(int, estimates["projected_text_utf8_bytes"]) + 1
        )

    changed_text = _mutated_envelope(toy_manifest, mutate_text)
    changed_policy = _mutated_envelope(toy_manifest, mutate_policy)
    changed_payload = _mutated_envelope(plan.as_envelope(), mutate_payload)
    changed_output = _mutated_envelope(plan.as_envelope(), mutate_output)
    changed_estimate = _mutated_envelope(plan.as_envelope(), mutate_estimate)

    selected_query = segment_adapter.query(
        toy_manifest,
        selected_segment_ids=list(TOY_SEGMENT_IDS[:2]),
        required_capabilities=list(SEGMENT_REQUIREMENTS),
        transport_mode="synthetic-segment",
        binding_model_settings_descriptor=binding,
    )
    model_binding = cast(dict[str, JsonValue], canonical_clone(dict(binding)))
    model_binding["model_ref"] = "synthetic-model-B"
    model_query = segment_adapter.query(
        toy_manifest,
        selected_segment_ids=list(TOY_SEGMENT_IDS),
        required_capabilities=list(SEGMENT_REQUIREMENTS),
        transport_mode="synthetic-segment",
        binding_model_settings_descriptor=model_binding,
    )
    mode_query = segment_adapter.query(
        toy_manifest,
        selected_segment_ids=list(TOY_SEGMENT_IDS),
        required_capabilities=list(SEGMENT_REQUIREMENTS),
        transport_mode="synthetic-batch",
        binding_model_settings_descriptor=binding,
    )

    def mutate_adapter(value: dict[str, JsonValue]) -> None:
        adapter = _object(value["adapter"], "adapter")
        adapter["adapter_version"] = "1.0.1"

    def mutate_schema(value: dict[str, JsonValue]) -> None:
        schema = _object(value["provider_schema_basis"], "schema basis")
        schema["sha256"] = _sha(b"synthetic-segment-schema-v2")

    adapter_query = _frozen_query(_mutated_envelope(query.as_envelope(), mutate_adapter))
    schema_query = _frozen_query(_mutated_envelope(query.as_envelope(), mutate_schema))

    def chain_rebound(changed_query: FrozenEnvelope) -> bool:
        changed_profile = segment_adapter.evaluate(changed_query)
        changed_plan = segment_adapter.prepare(
            toy_manifest,
            changed_query,
            changed_profile,
        )
        return (
            changed_query.digest != query.digest
            and changed_profile.digest != profile.digest
            and changed_plan.digest != plan.digest
        )

    return {
        "adapter_version": chain_rebound(adapter_query),
        "binding_descriptor": model_query.digest != query.digest,
        "estimate": cast(str, changed_estimate["digest"]) != plan.digest,
        "expected_output": cast(str, changed_output["digest"]) != plan.digest,
        "model_descriptor": chain_rebound(model_query),
        "policy": cast(str, changed_policy["digest"]) != base_digest,
        "projected_payload": cast(str, changed_payload["digest"]) != plan.digest,
        "schema_basis": chain_rebound(schema_query),
        "selection": selected_query.digest != query.digest,
        "source_bytes": rebound_manifest["digest"] != chapter_manifest["digest"],
        "text": cast(str, changed_text["digest"]) != base_digest,
        "transformation": transformed_plan.digest != plan.digest,
        "transport_mode": mode_query.digest != query.digest,
    }


def run_workflow(
    source_bytes: bytes,
    *,
    compiler_config: CompilerConfig,
    adapters: AdapterBundle | None = None,
) -> FrozenWorkflowSummary:
    """Run the complete deterministic L0 toy game with no external effects."""

    if type(source_bytes) is not bytes:
        raise WorkflowContractError("source_bytes must be exact bytes")
    active = default_adapters() if adapters is None else adapters
    resolver = _ResolverSpy()

    chapter_compiled = compile_manifest(source_bytes, config=compiler_config)
    chapter_manifest = chapter_compiled.as_envelope()
    chapter_value = _object(chapter_manifest["value"], "chapter manifest")
    chapter_segments = _list(chapter_value["segments"], "chapter segments")
    toy_manifest, toy_source_bytes = _toy_manifest(chapter_manifest)
    binding: dict[str, JsonValue] = {
        "binding_ref": "synthetic-binding-A",
        "model_ref": "synthetic-model-A",
        "settings": {"pace": "neutral"},
    }

    segment_query = active.segment.query(
        toy_manifest,
        selected_segment_ids=list(TOY_SEGMENT_IDS),
        required_capabilities=list(SEGMENT_REQUIREMENTS),
        transport_mode="synthetic-segment",
        binding_model_settings_descriptor=binding,
    )
    segment_profile = active.segment.evaluate(segment_query)
    segment_plan = active.segment.prepare(
        toy_manifest,
        segment_query,
        segment_profile,
        secret_resolver=resolver,
    )
    first_segment = _object(
        _list(_object(toy_manifest["value"], "toy value")["segments"], "segments")[0],
        "first segment",
    )
    exact_text = cast(str, first_segment["exact_text"])
    tag = cast(str, first_segment["leading_performance_tag"])
    projected_text = exact_text[len(tag) :].lstrip()
    try:
        active.segment.prepare(
            toy_manifest,
            segment_query,
            segment_profile,
            projected_text_by_segment={TOY_SEGMENT_IDS[0]: projected_text},
            secret_resolver=resolver,
        )
    except ProjectionApprovalRequired:
        projection_without_approval_blocked = True
    else:
        raise WorkflowContractError("text projection bypassed required approval")
    transformed_plan = active.segment.prepare(
        toy_manifest,
        segment_query,
        segment_profile,
        projected_text_by_segment={TOY_SEGMENT_IDS[0]: projected_text},
        transformation_approval_ref="synthetic-run-local-approval-001",
        secret_resolver=resolver,
    )

    unknown_query = active.segment.query(
        toy_manifest,
        selected_segment_ids=list(TOY_SEGMENT_IDS),
        required_capabilities=["live-account-evidence"],
        transport_mode="synthetic-segment",
        binding_model_settings_descriptor=binding,
    )
    unknown_profile = active.segment.evaluate(unknown_query)
    try:
        active.segment.prepare(
            toy_manifest,
            unknown_query,
            unknown_profile,
            secret_resolver=resolver,
        )
    except MandatoryCapabilityBlocked:
        unknown_capability_blocked = True
    else:
        raise WorkflowContractError("unknown mandatory capability was not blocked")

    authorization = _authorization(
        segment_plan.as_envelope(), authorization_id="synthetic-authorization-001"
    )
    grant = validate_execution_authorization(
        segment_plan.as_envelope(),
        authorization.as_envelope(),
        expected_account_ref=ACCOUNT_REF,
        expected_scope=EXECUTION_SCOPE,
        now=NOW,
        secret_resolver=resolver,
    )
    plan_units = grant.planned_effect_units
    expired = _authorization(
        segment_plan.as_envelope(),
        authorization_id="synthetic-authorization-expired",
        expires_at=NOW,
    )
    over_budget = _authorization(
        segment_plan.as_envelope(),
        authorization_id="synthetic-authorization-over-budget",
        max_effect_units=plan_units - 1,
    )
    rejected_authorizations = [
        _expect_authorization_rejection(
            "missing",
            segment_plan.as_envelope(),
            None,
            account_ref=ACCOUNT_REF,
            execution_scope=EXECUTION_SCOPE,
            resolver=resolver,
        ),
        _expect_authorization_rejection(
            "expired",
            segment_plan.as_envelope(),
            expired.as_envelope(),
            account_ref=ACCOUNT_REF,
            execution_scope=EXECUTION_SCOPE,
            resolver=resolver,
        ),
        _expect_authorization_rejection(
            "over-budget",
            segment_plan.as_envelope(),
            over_budget.as_envelope(),
            account_ref=ACCOUNT_REF,
            execution_scope=EXECUTION_SCOPE,
            resolver=resolver,
        ),
        _expect_authorization_rejection(
            "wrong-account",
            segment_plan.as_envelope(),
            authorization.as_envelope(),
            account_ref="synthetic-account-B",
            execution_scope=EXECUTION_SCOPE,
            resolver=resolver,
        ),
        _expect_authorization_rejection(
            "wrong-scope",
            segment_plan.as_envelope(),
            authorization.as_envelope(),
            account_ref=ACCOUNT_REF,
            execution_scope="synthetic/other-scope",
            resolver=resolver,
        ),
        _expect_authorization_rejection(
            "stale-plan",
            transformed_plan.as_envelope(),
            authorization.as_envelope(),
            account_ref=ACCOUNT_REF,
            execution_scope=EXECUTION_SCOPE,
            resolver=resolver,
        ),
    ]

    ledger, retry, retry_blocked = _record_outcomes(
        segment_plan, authorization, resolver
    )

    artifact = ArtifactRecord.from_bytes(
        artifact_id="synthetic-artifact-001",
        content=b"synthetic artifact placeholder",
        classification="synthetic-placeholder",
        materialized=False,
    )
    claim = ClaimRecord.create(
        claim_id="synthetic-claim-001",
        subject_ref=artifact.artifact_id,
        predicate="synthetic-artifact-observed",
        value=True,
        evidence_link_ids=("synthetic-claim-evidence-001",),
        confidence="observed",
    )
    claim_evidence = ClaimEvidence(
        evidence_id="synthetic-claim-evidence-001",
        claim_id=claim.claim_id,
        claim_type="artifact-observation",
        native_locator="synthetic-observation://toy-run/artifact-001",
        native_sha256=_sha(b"synthetic artifact observation"),
        observed_at="2026-08-09T12:30:00Z",
        classification="synthetic-placeholder",
        redaction_profile="no-credentials-or-native-payload/v1",
    )
    receipt = build_normalized_receipt(
        segment_plan.as_envelope(),
        authorization.as_envelope(),
        run_id="synthetic-evidence-run-001",
        output_granularity="segment",
        claims=(claim,),
        evidence_links=(claim_evidence,),
        artifacts=(artifact,),
        reconciliation_state={"status": "known", "ledger_digest": ledger.digest},
    )
    criterion = CriterionResult(
        criterion_id="synthetic-artifact-evidence-bound",
        passed=True,
        observed_result="typed synthetic observation matches the reviewed placeholder",
        evidence_link_ids=(claim_evidence.evidence_id,),
    )
    gate = build_gate_receipt(
        receipt.as_envelope(),
        plan=segment_plan.as_envelope(),
        authorization=authorization.as_envelope(),
        reviewed_artifacts=(artifact,),
        criteria_results=(criterion,),
        review_scope="synthetic-no-network-gate",
        reviewer="synthetic-fixture-reviewer",
        decision="accepted",
        decided_at="2026-08-09T12:31:00Z",
        exceptions=({"kind": "no-live-provider-proof", "accepted": False},),
    )
    validate_gate_receipt(
        gate.as_envelope(),
        receipt=receipt.as_envelope(),
        plan=segment_plan.as_envelope(),
        authorization=authorization.as_envelope(),
        reviewed_artifacts=(artifact,),
        criteria_results=(criterion,),
    )
    gate_mutations = _gate_mutation_rejections(
        plan=segment_plan,
        authorization=authorization,
        receipt=receipt,
        gate=gate,
        artifact=artifact,
        criterion=criterion,
        claim=claim,
        evidence=claim_evidence,
    )

    project_binding: dict[str, JsonValue] = {
        "binding_ref": "synthetic-project-binding-A",
        "model_ref": "synthetic-project-model-A",
        "settings": {"mode": "project"},
    }
    project_query = active.project.query(
        toy_manifest,
        selected_segment_ids=list(TOY_SEGMENT_IDS),
        required_capabilities=list(PROJECT_REQUIREMENTS),
        transport_mode="synthetic-project",
        binding_model_settings_descriptor=project_binding,
    )
    project_profile = active.project.evaluate(project_query)
    project_plan = active.project.prepare(
        toy_manifest,
        project_query,
        project_profile,
        secret_resolver=resolver,
    )
    uncorrelated = active.project.project(project_plan, secret_resolver=resolver)
    map_a = {
        segment_id: f"synthetic-marker-{index:03d}-A"
        for index, segment_id in enumerate(TOY_SEGMENT_IDS, start=1)
    }
    map_b = dict(map_a)
    map_b[TOY_SEGMENT_IDS[1]] = "synthetic-marker-002-B"
    correlated_a = active.project.project(
        project_plan, correlation_map=map_a, secret_resolver=resolver
    )
    correlated_b = active.project.project(
        project_plan, correlation_map=map_b, secret_resolver=resolver
    )
    try:
        active.project.prepare_segment_retry(
            uncorrelated, [TOY_SEGMENT_IDS[0]]
        )
    except SegmentRetryDenied:
        composite_segment_retry_denied = True
    else:
        raise WorkflowContractError("composite evidence incorrectly allowed segment retry")

    binding_proofs = _binding_proofs(
        source_bytes=source_bytes,
        compiler_config=compiler_config,
        chapter_manifest=chapter_manifest,
        toy_manifest=toy_manifest,
        segment_adapter=active.segment,
        query=segment_query,
        profile=segment_profile,
        plan=segment_plan,
        transformed_plan=transformed_plan,
        binding=binding,
    )
    if not all(value is True for value in binding_proofs.values()):
        raise WorkflowContractError("one or more digest binding proofs failed")
    if resolver.calls:
        raise WorkflowContractError("credential resolver was called")

    segment_plan_value = segment_plan.value
    project_plan_value = project_plan.value
    uncorrelated_value = uncorrelated.value
    correlated_a_value = correlated_a.value
    correlated_b_value = correlated_b.value
    retry_value = retry.plan.value
    speakers = sorted(
        {cast(str, _object(item, "chapter segment")["speaker"]) for item in chapter_segments}
    )
    tagged_count = sum(
        _object(item, "chapter segment").get("leading_performance_tag") is not None
        for item in chapter_segments
    )
    summary: dict[str, JsonValue] = {
        "schema_version": SUMMARY_SCHEMA,
        "claim_ceiling": CLAIM_CEILING,
        "source": {
            "sha256": _sha(source_bytes),
            "size_bytes": len(source_bytes),
            "manifest_digest": chapter_compiled.digest,
            "segment_count": len(chapter_segments),
            "speakers": speakers,
            "leading_tag_count": tagged_count,
            "order_and_text": "exact-source-order",
        },
        "toy": {
            "source_sha256": _sha(toy_source_bytes),
            "manifest_digest": cast(str, toy_manifest["digest"]),
            "selected_segment_ids": list(TOY_SEGMENT_IDS),
            "segment_count": len(TOY_SEGMENT_IDS),
        },
        "segment": {
            "query_digest": segment_query.digest,
            "profile_digest": segment_profile.digest,
            "plan_digest": segment_plan.digest,
            "expected_output_count": len(
                _list(segment_plan_value["expected_outputs"], "expected outputs")
            ),
            "observed_outcomes": ["accepted", "rejected-no-effect", "unknown"],
            "unknown_reconciled_to": "no-effect",
            "unknown_retry_blocked_before_reconciliation": retry_blocked,
            "retry_selected_segment_ids": cast(
                list[JsonValue], retry_value["selected_segment_ids"]
            ),
            "retry_excluded_operation_ids": list(retry.excluded_operation_ids),
            "retry_authorization_rebound": retry.authorization.digest
            != authorization.digest,
            "provider_idempotency_support": "unsupported",
            "projection_without_approval_blocked": projection_without_approval_blocked,
            "unknown_capability_blocked": unknown_capability_blocked,
        },
        "project": {
            "query_digest": project_query.digest,
            "profile_digest": project_profile.digest,
            "plan_digest": project_plan.digest,
            "expected_output_count": len(
                _list(project_plan_value["expected_outputs"], "expected outputs")
            ),
            "output_granularity": "composite",
            "uncorrelated_segment_states": [
                _object(item, "segment state")["state"]
                for item in _list(
                    uncorrelated_value["segment_states"], "segment states"
                )
            ],
            "correlation_confidence": uncorrelated_value["correlation_confidence"],
            "correlation_rebinds_receipt": correlated_a_value["receipt_input_digest"]
            != correlated_b_value["receipt_input_digest"],
            "correlation_rebinds_gate": correlated_a_value["gate_input_digest"]
            != correlated_b_value["gate_input_digest"],
            "segment_retry_denied": composite_segment_retry_denied,
            "materialized_artifact_count": 0,
        },
        "evidence": {
            "authorization_digest": authorization.digest,
            "normalized_receipt_digest": receipt.digest,
            "gate_receipt_digest": gate.digest,
            "authorization_rejections": rejected_authorizations,
            "gate_mutation_rejections": gate_mutations,
            "non_unknown_claims_have_typed_evidence": True,
        },
        "binding_proofs": binding_proofs,
        "effects": {
            "network_calls": 0,
            "dns_calls": 0,
            "credential_resolver_calls": resolver.calls,
            "provider_calls": 0,
            "audio_artifacts_materialized": 0,
            "external_messages": 0,
        },
    }
    return FrozenWorkflowSummary(canonical_bytes(summary))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the deterministic no-network voice-production toy game."
    )
    parser.add_argument("source_csv", type=Path, help="exact local speaker,line CSV")
    parser.add_argument(
        "compiler_config",
        type=Path,
        help="exact local voice-production compiler config JSON",
    )
    parser.add_argument(
        "factory_handoff",
        type=Path,
        help="accepted-manuscript, local-compile-only Chapter Factory handoff JSON",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="repository root used to resolve and verify handoff bindings",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source_bytes = args.source_csv.read_bytes()
    compiler_config_bytes = args.compiler_config.read_bytes()
    handoff_bytes = args.factory_handoff.read_bytes()
    compiler_config = compiler_config_from_json_bytes(compiler_config_bytes)
    validate_factory_handoff(
        handoff_bytes,
        handoff_path=args.factory_handoff,
        repository_root=args.repo_root,
        source_path=args.source_csv,
        source_bytes=source_bytes,
        compiler_config_path=args.compiler_config,
        compiler_config_bytes=compiler_config_bytes,
        compiler_config=compiler_config,
    )
    summary = run_workflow(
        source_bytes,
        compiler_config=compiler_config,
    )
    print(summary.text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
