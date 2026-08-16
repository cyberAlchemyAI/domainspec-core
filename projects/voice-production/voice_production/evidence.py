"""Immutable evidence, authorization, and human-gate contracts for L0.

This module validates a provider-neutral chain from a canonical plan through
execution authorization, normalized claims, and a human review gate.  It is
pure: no file, network, credential, provider, submission, or audio operation
is performed, and validation deliberately stops before secret resolution.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Mapping, cast

from .canonical import (
    JsonValue,
    canonical_bytes,
    canonical_clone,
    canonical_loads,
    make_envelope,
    require_valid_envelope,
)
from .contracts import (
    GATE_RECEIPT_SCHEMA_ID,
    NORMALIZED_RECEIPT_SCHEMA_ID,
    PLAN_SCHEMA_ID,
    ContractEnvelope,
    gate_receipt_envelope,
    normalized_receipt_envelope,
)


EXECUTION_AUTHORIZATION_SCHEMA_ID = "voice-production.execution-authorization"
EXECUTION_AUTHORIZATION_SCHEMA_VERSION = "1"
BUDGET_UNIT = "projected_text_utf8_bytes"

REQUIRED_PREREQUISITE_KINDS = frozenset(
    {
        "account-capability-access",
        "terms-commercial-use",
        "privacy-data-processing",
        "artifact-classification",
        "artifact-storage-access",
        "retention-deletion",
        "redacted-plan-evidence-views",
    }
)

_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_CLAIM_CONFIDENCE = frozenset({"observed", "derived", "unknown"})


class EvidenceContractError(ValueError):
    """Base error for invalid evidence, authorization, or gate contracts."""


class AuthorizationRejected(EvidenceContractError):
    """Raised before secret resolution when authorization is not exact/current."""


class ClaimEvidenceError(EvidenceContractError):
    """Raised when normalized claims are not fully evidence-accounted."""


class GateBindingError(EvidenceContractError):
    """Raised when a human gate no longer binds the reviewed inputs."""


def _non_empty(value: str, name: str) -> str:
    if type(value) is not str or not value:
        raise EvidenceContractError(f"{name} must be a non-empty string")
    return value


def _sha256(value: str, name: str) -> str:
    if type(value) is not str or _SHA256_RE.fullmatch(value) is None:
        raise EvidenceContractError(
            f"{name} must be a lowercase SHA-256 hex string"
        )
    return value


def _utc_timestamp(value: str, name: str) -> datetime:
    _non_empty(value, name)
    if not value.endswith("Z"):
        raise EvidenceContractError(f"{name} must be an explicit UTC timestamp")
    try:
        parsed = datetime.fromisoformat(f"{value[:-1]}+00:00")
    except ValueError as exc:
        raise EvidenceContractError(f"{name} is not a valid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise EvidenceContractError(f"{name} must be UTC")
    return parsed


def _envelope_value(
    envelope: Mapping[str, JsonValue], expected_schema_id: str
) -> tuple[dict[str, JsonValue], dict[str, JsonValue]]:
    if type(envelope) is not dict:
        raise EvidenceContractError("contract envelope must be an object")
    detached = cast(dict[str, JsonValue], canonical_clone(dict(envelope)))
    try:
        require_valid_envelope(detached)
    except ValueError as exc:
        raise EvidenceContractError("contract envelope is invalid") from exc
    if detached.get("schema_id") != expected_schema_id:
        raise EvidenceContractError(
            f"expected schema {expected_schema_id!r}; "
            f"got {detached.get('schema_id')!r}"
        )
    value = detached.get("value")
    if type(value) is not dict:
        raise EvidenceContractError("contract value must be an object")
    return detached, cast(dict[str, JsonValue], value)


@dataclass(frozen=True, slots=True)
class FrozenEvidenceEnvelope:
    """Canonical contract bytes with detached envelope access."""

    canonical_envelope_bytes: bytes
    expected_schema_id: str

    def __post_init__(self) -> None:
        if type(self.canonical_envelope_bytes) is not bytes:
            raise TypeError("canonical_envelope_bytes must be bytes")
        _envelope_value(self.as_envelope(), self.expected_schema_id)

    def as_envelope(self) -> ContractEnvelope:
        parsed = canonical_loads(self.canonical_envelope_bytes)
        if type(parsed) is not dict:
            raise EvidenceContractError("contract envelope must be an object")
        envelope = cast(dict[str, JsonValue], parsed)
        require_valid_envelope(envelope)
        return cast(ContractEnvelope, envelope)

    @property
    def digest(self) -> str:
        return cast(str, self.as_envelope()["digest"])

    @property
    def value(self) -> dict[str, JsonValue]:
        value = self.as_envelope()["value"]
        if type(value) is not dict:
            raise EvidenceContractError("contract value must be an object")
        return cast(dict[str, JsonValue], value)


@dataclass(frozen=True, slots=True)
class ProtectedPrerequisite:
    """Accepted evidence for one protected execution prerequisite."""

    kind: str
    evidence_id: str
    evidence_sha256: str
    accepted: bool
    expires_at: str | None

    def __post_init__(self) -> None:
        _non_empty(self.kind, "prerequisite.kind")
        _non_empty(self.evidence_id, "prerequisite.evidence_id")
        _sha256(self.evidence_sha256, "prerequisite.evidence_sha256")
        if type(self.accepted) is not bool:
            raise EvidenceContractError("prerequisite.accepted must be boolean")
        if self.expires_at is not None:
            _utc_timestamp(self.expires_at, "prerequisite.expires_at")

    def as_value(self) -> dict[str, JsonValue]:
        return {
            "kind": self.kind,
            "evidence_id": self.evidence_id,
            "evidence_sha256": self.evidence_sha256,
            "accepted": self.accepted,
            "expires_at": self.expires_at,
        }


@dataclass(frozen=True, slots=True)
class ExecutionGrant:
    """A checked boundary token; it is not a secret or submission result."""

    authorization_digest: str
    plan_digest: str
    account_ref: str
    execution_scope: str
    planned_effect_units: int
    budget_limit: int


@dataclass(frozen=True, slots=True)
class ClaimEvidence:
    """Typed immutable evidence for one normalized claim."""

    evidence_id: str
    claim_id: str
    claim_type: str
    native_locator: str
    native_sha256: str
    observed_at: str
    classification: str
    redaction_profile: str

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "claim_id",
            "claim_type",
            "native_locator",
            "classification",
            "redaction_profile",
        ):
            _non_empty(cast(str, getattr(self, name)), f"evidence.{name}")
        _sha256(self.native_sha256, "evidence.native_sha256")
        _utc_timestamp(self.observed_at, "evidence.observed_at")

    def as_value(self) -> dict[str, JsonValue]:
        return {
            "evidence_id": self.evidence_id,
            "claim_id": self.claim_id,
            "claim_type": self.claim_type,
            "native_locator": self.native_locator,
            "native_sha256": self.native_sha256,
            "observed_at": self.observed_at,
            "classification": self.classification,
            "redaction_profile": self.redaction_profile,
        }


@dataclass(frozen=True, slots=True)
class ClaimRecord:
    """Immutable normalized claim with its value retained as canonical bytes."""

    claim_id: str
    subject_ref: str
    predicate: str
    value_bytes: bytes
    evidence_link_ids: tuple[str, ...]
    confidence: str

    def __post_init__(self) -> None:
        _non_empty(self.claim_id, "claim.claim_id")
        _non_empty(self.subject_ref, "claim.subject_ref")
        _non_empty(self.predicate, "claim.predicate")
        if type(self.value_bytes) is not bytes:
            raise EvidenceContractError("claim.value_bytes must be bytes")
        canonical_loads(self.value_bytes)
        if type(self.evidence_link_ids) is not tuple:
            raise EvidenceContractError("claim.evidence_link_ids must be a tuple")
        for index, evidence_id in enumerate(self.evidence_link_ids):
            _non_empty(evidence_id, f"claim.evidence_link_ids[{index}]")
        if len(set(self.evidence_link_ids)) != len(self.evidence_link_ids):
            raise EvidenceContractError("claim evidence links must be unique")
        if self.confidence not in _CLAIM_CONFIDENCE:
            raise EvidenceContractError(
                f"claim.confidence must be one of {sorted(_CLAIM_CONFIDENCE)}"
            )

    @classmethod
    def create(
        cls,
        *,
        claim_id: str,
        subject_ref: str,
        predicate: str,
        value: JsonValue,
        evidence_link_ids: tuple[str, ...],
        confidence: str,
    ) -> "ClaimRecord":
        return cls(
            claim_id=claim_id,
            subject_ref=subject_ref,
            predicate=predicate,
            value_bytes=canonical_bytes(value),
            evidence_link_ids=evidence_link_ids,
            confidence=confidence,
        )

    @property
    def value(self) -> JsonValue:
        return canonical_loads(self.value_bytes)

    def as_value(self) -> dict[str, JsonValue]:
        return {
            "claim_id": self.claim_id,
            "subject_ref": self.subject_ref,
            "predicate": self.predicate,
            "value": self.value,
            "evidence_link_ids": list(self.evidence_link_ids),
            "confidence": self.confidence,
        }


@dataclass(frozen=True, slots=True)
class ArtifactRecord:
    """Immutable identity for exact artifact bytes."""

    artifact_id: str
    sha256: str
    classification: str
    materialized: bool

    def __post_init__(self) -> None:
        _non_empty(self.artifact_id, "artifact.artifact_id")
        _sha256(self.sha256, "artifact.sha256")
        _non_empty(self.classification, "artifact.classification")
        if type(self.materialized) is not bool:
            raise EvidenceContractError("artifact.materialized must be boolean")

    @classmethod
    def from_bytes(
        cls,
        *,
        artifact_id: str,
        content: bytes,
        classification: str,
        materialized: bool,
    ) -> "ArtifactRecord":
        if type(content) is not bytes:
            raise EvidenceContractError("artifact content must be exact bytes")
        return cls(
            artifact_id=artifact_id,
            sha256=hashlib.sha256(content).hexdigest(),
            classification=classification,
            materialized=materialized,
        )

    def as_value(self) -> dict[str, JsonValue]:
        return {
            "artifact_id": self.artifact_id,
            "sha256": self.sha256,
            "classification": self.classification,
            "materialized": self.materialized,
        }


@dataclass(frozen=True, slots=True)
class CriterionResult:
    """Exact observed result for one human-review criterion."""

    criterion_id: str
    passed: bool
    observed_result: str
    evidence_link_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _non_empty(self.criterion_id, "criterion.criterion_id")
        if type(self.passed) is not bool:
            raise EvidenceContractError("criterion.passed must be boolean")
        _non_empty(self.observed_result, "criterion.observed_result")
        if type(self.evidence_link_ids) is not tuple:
            raise EvidenceContractError("criterion.evidence_link_ids must be a tuple")
        for index, evidence_id in enumerate(self.evidence_link_ids):
            _non_empty(evidence_id, f"criterion.evidence_link_ids[{index}]")

    def as_value(self) -> dict[str, JsonValue]:
        return {
            "criterion_id": self.criterion_id,
            "passed": self.passed,
            "observed_result": self.observed_result,
            "evidence_link_ids": list(self.evidence_link_ids),
        }


def _plan_binding(
    plan: Mapping[str, JsonValue],
) -> tuple[dict[str, JsonValue], dict[str, JsonValue], int]:
    plan_envelope, plan_value = _envelope_value(plan, PLAN_SCHEMA_ID)
    estimates = plan_value.get("effect_estimates")
    if type(estimates) is not dict:
        raise AuthorizationRejected("plan effect estimates are missing")
    planned_units = estimates.get(BUDGET_UNIT)
    if type(planned_units) is not int or planned_units < 0:
        raise AuthorizationRejected(
            f"plan must declare non-negative integer {BUDGET_UNIT}"
        )
    return plan_envelope, plan_value, planned_units


def build_execution_authorization(
    plan: Mapping[str, JsonValue],
    *,
    authorization_id: str,
    account_ref: str,
    execution_scope: str,
    issued_at: str,
    expires_at: str,
    max_effect_units: int,
    prerequisite_evidence: tuple[ProtectedPrerequisite, ...],
) -> FrozenEvidenceEnvelope:
    """Build an exact plan/account/scope/budget authorization envelope."""

    plan_envelope, plan_value, planned_units = _plan_binding(plan)
    _non_empty(authorization_id, "authorization_id")
    _non_empty(account_ref, "account_ref")
    _non_empty(execution_scope, "execution_scope")
    _utc_timestamp(issued_at, "issued_at")
    _utc_timestamp(expires_at, "expires_at")
    if type(max_effect_units) is not int or max_effect_units < 0:
        raise EvidenceContractError("max_effect_units must be non-negative integer")
    if type(prerequisite_evidence) is not tuple:
        raise EvidenceContractError("prerequisite_evidence must be a tuple")

    value: dict[str, JsonValue] = {
        "authorization_id": authorization_id,
        "plan_digest": cast(str, plan_envelope["digest"]),
        "manifest_digest": _sha256(
            cast(str, plan_value.get("manifest_digest")), "manifest_digest"
        ),
        "capability_profile_digest": _sha256(
            cast(str, plan_value.get("capability_profile_digest")),
            "capability_profile_digest",
        ),
        "account_ref": account_ref,
        "execution_scope": execution_scope,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "budget": {
            "unit": BUDGET_UNIT,
            "limit": max_effect_units,
            "planned": planned_units,
        },
        "prerequisite_evidence": [
            prerequisite.as_value() for prerequisite in prerequisite_evidence
        ],
    }
    envelope = make_envelope(
        EXECUTION_AUTHORIZATION_SCHEMA_ID,
        value,
        schema_version=EXECUTION_AUTHORIZATION_SCHEMA_VERSION,
    )
    return FrozenEvidenceEnvelope(
        canonical_bytes(envelope), EXECUTION_AUTHORIZATION_SCHEMA_ID
    )


def validate_execution_authorization(
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue] | None,
    *,
    expected_account_ref: str,
    expected_scope: str,
    now: str,
    secret_resolver: Callable[..., object] | None = None,
) -> ExecutionGrant:
    """Validate all prerequisites and stop immediately before secret access.

    ``secret_resolver`` is accepted solely so tests can prove it remains
    untouched on every rejection.  This L0 boundary never invokes it, even on
    success; resolving a credential belongs to a later effect-owning layer.
    """

    _ = secret_resolver
    plan_envelope, plan_value, planned_units = _plan_binding(plan)
    if authorization is None:
        raise AuthorizationRejected("execution authorization is missing")
    try:
        authorization_envelope, value = _envelope_value(
            authorization, EXECUTION_AUTHORIZATION_SCHEMA_ID
        )
    except EvidenceContractError as exc:
        raise AuthorizationRejected("execution authorization is invalid") from exc

    if value.get("plan_digest") != plan_envelope.get("digest"):
        raise AuthorizationRejected("authorization is stale for the exact plan")
    if value.get("manifest_digest") != plan_value.get("manifest_digest"):
        raise AuthorizationRejected("authorization manifest binding mismatch")
    if value.get("capability_profile_digest") != plan_value.get(
        "capability_profile_digest"
    ):
        raise AuthorizationRejected("authorization capability binding mismatch")
    if value.get("account_ref") != _non_empty(
        expected_account_ref, "expected_account_ref"
    ):
        raise AuthorizationRejected("authorization account binding mismatch")
    if value.get("execution_scope") != _non_empty(expected_scope, "expected_scope"):
        raise AuthorizationRejected("authorization scope binding mismatch")

    now_value = _utc_timestamp(now, "now")
    issued_at = _utc_timestamp(cast(str, value.get("issued_at")), "issued_at")
    expires_at = _utc_timestamp(cast(str, value.get("expires_at")), "expires_at")
    if now_value < issued_at:
        raise AuthorizationRejected("execution authorization is not yet active")
    if now_value >= expires_at:
        raise AuthorizationRejected("execution authorization is expired")

    budget = value.get("budget")
    if type(budget) is not dict:
        raise AuthorizationRejected("authorization budget is missing")
    if budget.get("unit") != BUDGET_UNIT:
        raise AuthorizationRejected("authorization budget unit mismatch")
    limit = budget.get("limit")
    bound_planned = budget.get("planned")
    if type(limit) is not int or limit < 0:
        raise AuthorizationRejected("authorization budget limit is invalid")
    if bound_planned != planned_units:
        raise AuthorizationRejected("authorization budget is stale for the plan")
    if planned_units > limit:
        raise AuthorizationRejected("authorization budget exceeded")

    raw_prerequisites = value.get("prerequisite_evidence")
    if type(raw_prerequisites) is not list:
        raise AuthorizationRejected("protected prerequisite evidence is missing")
    prerequisites: dict[str, dict[str, JsonValue]] = {}
    for index, raw in enumerate(raw_prerequisites):
        if type(raw) is not dict:
            raise AuthorizationRejected(
                f"protected prerequisite {index} must be an object"
            )
        prerequisite = cast(dict[str, JsonValue], raw)
        kind = prerequisite.get("kind")
        if type(kind) is not str or not kind:
            raise AuthorizationRejected("protected prerequisite kind is invalid")
        if kind in prerequisites:
            raise AuthorizationRejected(
                f"protected prerequisite is duplicated: {kind}"
            )
        prerequisites[kind] = prerequisite
    missing = sorted(REQUIRED_PREREQUISITE_KINDS - set(prerequisites))
    unexpected = sorted(set(prerequisites) - REQUIRED_PREREQUISITE_KINDS)
    if missing or unexpected:
        raise AuthorizationRejected(
            "protected prerequisite set mismatch; "
            f"missing={missing}, unexpected={unexpected}"
        )
    for kind in sorted(REQUIRED_PREREQUISITE_KINDS):
        prerequisite = prerequisites[kind]
        if prerequisite.get("accepted") is not True:
            raise AuthorizationRejected(
                f"protected prerequisite is not accepted: {kind}"
            )
        try:
            _non_empty(cast(str, prerequisite.get("evidence_id")), "evidence_id")
            _sha256(
                cast(str, prerequisite.get("evidence_sha256")),
                "evidence_sha256",
            )
        except EvidenceContractError as exc:
            raise AuthorizationRejected(
                f"protected prerequisite evidence is invalid: {kind}"
            ) from exc
        expiry = prerequisite.get("expires_at")
        if expiry is not None:
            try:
                evidence_expiry = _utc_timestamp(
                    cast(str, expiry), "prerequisite.expires_at"
                )
            except EvidenceContractError as exc:
                raise AuthorizationRejected(
                    f"protected prerequisite expiry is invalid: {kind}"
                ) from exc
            if now_value >= evidence_expiry:
                raise AuthorizationRejected(
                    f"protected prerequisite evidence is expired: {kind}"
                )

    return ExecutionGrant(
        authorization_digest=cast(str, authorization_envelope["digest"]),
        plan_digest=cast(str, plan_envelope["digest"]),
        account_ref=cast(str, value["account_ref"]),
        execution_scope=cast(str, value["execution_scope"]),
        planned_effect_units=planned_units,
        budget_limit=limit,
    )


def _authorization_binding(
    plan: Mapping[str, JsonValue], authorization: Mapping[str, JsonValue]
) -> tuple[dict[str, JsonValue], dict[str, JsonValue], dict[str, JsonValue]]:
    plan_envelope, plan_value, _planned_units = _plan_binding(plan)
    authorization_envelope, authorization_value = _envelope_value(
        authorization, EXECUTION_AUTHORIZATION_SCHEMA_ID
    )
    if authorization_value.get("plan_digest") != plan_envelope.get("digest"):
        raise AuthorizationRejected("authorization is stale for the exact plan")
    if authorization_value.get("manifest_digest") != plan_value.get(
        "manifest_digest"
    ):
        raise AuthorizationRejected("authorization manifest binding mismatch")
    if authorization_value.get("capability_profile_digest") != plan_value.get(
        "capability_profile_digest"
    ):
        raise AuthorizationRejected("authorization capability binding mismatch")
    return plan_envelope, plan_value, authorization_envelope


def _validate_claim_links(
    claims: list[dict[str, JsonValue]],
    evidence_links: list[dict[str, JsonValue]],
) -> None:
    claim_by_id: dict[str, dict[str, JsonValue]] = {}
    for index, claim in enumerate(claims):
        claim_id = claim.get("claim_id")
        if type(claim_id) is not str or not claim_id:
            raise ClaimEvidenceError(f"claims[{index}].claim_id is invalid")
        if claim_id in claim_by_id:
            raise ClaimEvidenceError(f"duplicate claim id: {claim_id}")
        confidence = claim.get("confidence")
        if confidence not in _CLAIM_CONFIDENCE:
            raise ClaimEvidenceError(
                f"claim {claim_id} has invalid confidence {confidence!r}"
            )
        references = claim.get("evidence_link_ids")
        if type(references) is not list or any(
            type(item) is not str or not item for item in references
        ):
            raise ClaimEvidenceError(f"claim {claim_id} evidence links are invalid")
        if len(set(references)) != len(references):
            raise ClaimEvidenceError(f"claim {claim_id} evidence links are duplicated")
        if confidence != "unknown" and not references:
            raise ClaimEvidenceError(
                f"non-unknown claim {claim_id} must have typed evidence"
            )
        claim_by_id[claim_id] = claim

    evidence_by_id: dict[str, dict[str, JsonValue]] = {}
    for index, evidence in enumerate(evidence_links):
        evidence_id = evidence.get("evidence_id")
        if type(evidence_id) is not str or not evidence_id:
            raise ClaimEvidenceError(
                f"evidence_links[{index}].evidence_id is invalid"
            )
        if evidence_id in evidence_by_id:
            raise ClaimEvidenceError(f"duplicate evidence id: {evidence_id}")
        claim_id = evidence.get("claim_id")
        if claim_id not in claim_by_id:
            raise ClaimEvidenceError(
                f"evidence {evidence_id} names unknown claim {claim_id!r}"
            )
        for field in (
            "claim_type",
            "native_locator",
            "classification",
            "redaction_profile",
        ):
            if type(evidence.get(field)) is not str or not evidence.get(field):
                raise ClaimEvidenceError(
                    f"evidence {evidence_id} has invalid {field}"
                )
        try:
            _sha256(cast(str, evidence.get("native_sha256")), "native_sha256")
            _utc_timestamp(cast(str, evidence.get("observed_at")), "observed_at")
        except EvidenceContractError as exc:
            raise ClaimEvidenceError(
                f"evidence {evidence_id} has invalid immutable observation"
            ) from exc
        evidence_by_id[evidence_id] = evidence

    referenced: set[str] = set()
    for claim_id, claim in claim_by_id.items():
        references = cast(list[str], claim["evidence_link_ids"])
        for evidence_id in references:
            evidence = evidence_by_id.get(evidence_id)
            if evidence is None:
                raise ClaimEvidenceError(
                    f"claim {claim_id} references missing evidence {evidence_id}"
                )
            if evidence.get("claim_id") != claim_id:
                raise ClaimEvidenceError(
                    f"evidence {evidence_id} is bound to another claim"
                )
            referenced.add(evidence_id)
    orphaned = sorted(set(evidence_by_id) - referenced)
    if orphaned:
        raise ClaimEvidenceError(f"unreferenced evidence links: {orphaned}")


def build_normalized_receipt(
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    *,
    run_id: str,
    output_granularity: str,
    claims: tuple[ClaimRecord, ...],
    evidence_links: tuple[ClaimEvidence, ...],
    artifacts: tuple[ArtifactRecord, ...],
    reconciliation_state: JsonValue,
    composite_groups: tuple[Mapping[str, JsonValue], ...] = (),
    parent_run_id: str | None = None,
) -> FrozenEvidenceEnvelope:
    """Build and immediately validate a normalized evidence receipt."""

    plan_envelope, plan_value, authorization_envelope = _authorization_binding(
        plan, authorization
    )
    if type(claims) is not tuple or type(evidence_links) is not tuple:
        raise EvidenceContractError("claims and evidence_links must be tuples")
    if type(artifacts) is not tuple or type(composite_groups) is not tuple:
        raise EvidenceContractError("artifacts and composite_groups must be tuples")
    claim_values = [claim.as_value() for claim in claims]
    evidence_values = [evidence.as_value() for evidence in evidence_links]
    _validate_claim_links(claim_values, evidence_values)
    if len({artifact.artifact_id for artifact in artifacts}) != len(artifacts):
        raise EvidenceContractError("artifact ids must be unique")
    composite_values = [
        cast(dict[str, JsonValue], canonical_clone(dict(group)))
        for group in composite_groups
    ]
    envelope = normalized_receipt_envelope(
        manifest_digest=cast(str, plan_value["manifest_digest"]),
        capability_profile_digest=cast(
            str, plan_value["capability_profile_digest"]
        ),
        plan_digest=cast(str, plan_envelope["digest"]),
        execution_authorization_digest=cast(
            str, authorization_envelope["digest"]
        ),
        run_id=run_id,
        parent_run_id=parent_run_id,
        output_granularity=output_granularity,
        composite_groups=composite_values,
        claims=cast(list, claim_values),
        evidence_links=cast(list, evidence_values),
        artifacts=[artifact.as_value() for artifact in artifacts],
        reconciliation_state=canonical_clone(reconciliation_state),
    )
    frozen = FrozenEvidenceEnvelope(
        canonical_bytes(envelope), NORMALIZED_RECEIPT_SCHEMA_ID
    )
    validate_normalized_receipt(
        frozen.as_envelope(), plan=plan, authorization=authorization
    )
    return frozen


def validate_normalized_receipt(
    receipt: Mapping[str, JsonValue],
    *,
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
) -> None:
    """Require complete claim evidence and the exact authorization binding."""

    _receipt_envelope, value = _envelope_value(
        receipt, NORMALIZED_RECEIPT_SCHEMA_ID
    )
    plan_envelope, plan_value, authorization_envelope = _authorization_binding(
        plan, authorization
    )
    expected = {
        "manifest_digest": plan_value.get("manifest_digest"),
        "capability_profile_digest": plan_value.get("capability_profile_digest"),
        "plan_digest": plan_envelope.get("digest"),
        "execution_authorization_digest": authorization_envelope.get("digest"),
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise ClaimEvidenceError(f"receipt {field} binding mismatch")
    raw_claims = value.get("claims")
    raw_evidence = value.get("evidence_links")
    if type(raw_claims) is not list or any(type(item) is not dict for item in raw_claims):
        raise ClaimEvidenceError("receipt claims must be objects")
    if type(raw_evidence) is not list or any(
        type(item) is not dict for item in raw_evidence
    ):
        raise ClaimEvidenceError("receipt evidence links must be objects")
    _validate_claim_links(
        cast(list[dict[str, JsonValue]], raw_claims),
        cast(list[dict[str, JsonValue]], raw_evidence),
    )


def build_gate_receipt(
    receipt: Mapping[str, JsonValue],
    *,
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    reviewed_artifacts: tuple[ArtifactRecord, ...],
    criteria_results: tuple[CriterionResult, ...],
    review_scope: str,
    reviewer: str,
    decision: str,
    decided_at: str,
    exceptions: tuple[Mapping[str, JsonValue], ...] = (),
) -> FrozenEvidenceEnvelope:
    """Build a gate over exact receipt, artifact, criterion, and auth inputs."""

    validate_normalized_receipt(receipt, plan=plan, authorization=authorization)
    receipt_envelope, receipt_value = _envelope_value(
        receipt, NORMALIZED_RECEIPT_SCHEMA_ID
    )
    if not reviewed_artifacts:
        raise GateBindingError("at least one reviewed artifact is required")
    if len({item.artifact_id for item in reviewed_artifacts}) != len(
        reviewed_artifacts
    ):
        raise GateBindingError("reviewed artifact ids must be unique")
    receipt_artifacts = receipt_value.get("artifacts")
    if type(receipt_artifacts) is not list:
        raise GateBindingError("receipt artifacts must be a list")
    receipt_hashes = {
        item.get("sha256") for item in receipt_artifacts if type(item) is dict
    }
    missing_hashes = sorted(
        item.sha256 for item in reviewed_artifacts if item.sha256 not in receipt_hashes
    )
    if missing_hashes:
        raise GateBindingError(
            f"reviewed artifacts are absent from receipt: {missing_hashes}"
        )
    if not criteria_results:
        raise GateBindingError("at least one review criterion is required")
    criterion_values = [criterion.as_value() for criterion in criteria_results]
    exception_values = [
        cast(dict[str, JsonValue], canonical_clone(dict(item)))
        for item in exceptions
    ]
    envelope = gate_receipt_envelope(
        synthesis_receipt_digest=cast(str, receipt_envelope["digest"]),
        reviewed_artifact_sha256s=[item.sha256 for item in reviewed_artifacts],
        criteria_results=criterion_values,
        review_scope=review_scope,
        reviewer=reviewer,
        decision=decision,
        decided_at=decided_at,
        exceptions=exception_values,
    )
    frozen = FrozenEvidenceEnvelope(canonical_bytes(envelope), GATE_RECEIPT_SCHEMA_ID)
    validate_gate_receipt(
        frozen.as_envelope(),
        receipt=receipt,
        plan=plan,
        authorization=authorization,
        reviewed_artifacts=reviewed_artifacts,
        criteria_results=criteria_results,
    )
    return frozen


def validate_gate_receipt(
    gate: Mapping[str, JsonValue],
    *,
    receipt: Mapping[str, JsonValue],
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    reviewed_artifacts: tuple[ArtifactRecord, ...],
    criteria_results: tuple[CriterionResult, ...],
) -> None:
    """Fail if any reviewed receipt/evidence/artifact/criterion/auth input moved."""

    validate_normalized_receipt(receipt, plan=plan, authorization=authorization)
    gate_envelope, gate_value = _envelope_value(gate, GATE_RECEIPT_SCHEMA_ID)
    receipt_envelope, _receipt_value = _envelope_value(
        receipt, NORMALIZED_RECEIPT_SCHEMA_ID
    )
    if gate_value.get("synthesis_receipt_digest") != receipt_envelope.get("digest"):
        raise GateBindingError("gate synthesis receipt binding mismatch")
    expected_artifact_hashes = [item.sha256 for item in reviewed_artifacts]
    if gate_value.get("reviewed_artifact_sha256s") != expected_artifact_hashes:
        raise GateBindingError("gate reviewed artifact binding mismatch")
    expected_criteria = [item.as_value() for item in criteria_results]
    if gate_value.get("criteria_results") != expected_criteria:
        raise GateBindingError("gate criteria binding mismatch")
    require_valid_envelope(gate_envelope)
