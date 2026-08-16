"""Pure operation ledger, unknown reconciliation, and bounded retry planning.

The lifecycle is represented only as immutable canonical envelopes.  It keeps
submission uncertainty explicit and never interprets timeout as proof of no
effect.  This L0 module performs no file, network, credential, provider,
submission, or audio operation and always stops before secret resolution.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Mapping, cast

from .canonical import (
    JsonValue,
    canonical_bytes,
    canonical_clone,
    canonical_loads,
    canonical_sha256,
    make_envelope,
    require_valid_envelope,
)
from .contracts import PLAN_SCHEMA_ID, ContractEnvelope
from .evidence import (
    EXECUTION_AUTHORIZATION_SCHEMA_ID,
    FrozenEvidenceEnvelope,
    ProtectedPrerequisite,
    build_execution_authorization,
)


OPERATION_LEDGER_SCHEMA_ID = "voice-production.operation-ledger"
DUPLICATE_RISK_AUTHORIZATION_SCHEMA_ID = (
    "voice-production.duplicate-risk-authorization"
)
LIFECYCLE_SCHEMA_VERSION = "1"

IDEMPOTENCY_SUPPORT_VALUES = frozenset({"supported", "unsupported", "unknown"})
RESPONSE_STATES = frozenset({"accepted", "rejected-no-effect", "unknown"})
RECONCILIATION_OUTCOMES = frozenset(
    {"no-effect", "effect-found", "still-unknown"}
)
OPERATION_STATES = frozenset(
    {
        "planned",
        "accepted",
        "rejected-no-effect",
        "unknown",
        "reconciled-no-effect",
        "effect-found",
        "duplicate-risk-authorized",
    }
)

_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


class LifecycleContractError(ValueError):
    """Base failure for invalid lifecycle contracts or transitions."""


class UnknownEffectBlocked(LifecycleContractError):
    """Raised when an unknown effect has neither resolution nor risk approval."""


class RetryBlocked(LifecycleContractError):
    """Raised when a requested retry is unsafe, empty, or outside its bound."""


def _non_empty(value: str, name: str) -> str:
    if type(value) is not str or not value:
        raise LifecycleContractError(f"{name} must be a non-empty string")
    return value


def _sha256(value: str, name: str) -> str:
    if type(value) is not str or _SHA256_RE.fullmatch(value) is None:
        raise LifecycleContractError(
            f"{name} must be a lowercase SHA-256 hex string"
        )
    return value


def _timestamp(value: str, name: str) -> datetime:
    _non_empty(value, name)
    if not value.endswith("Z"):
        raise LifecycleContractError(f"{name} must be an explicit UTC timestamp")
    try:
        parsed = datetime.fromisoformat(f"{value[:-1]}+00:00")
    except ValueError as exc:
        raise LifecycleContractError(f"{name} is not a valid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise LifecycleContractError(f"{name} must be UTC")
    return parsed


def _envelope_value(
    envelope: Mapping[str, JsonValue], expected_schema_id: str
) -> tuple[dict[str, JsonValue], dict[str, JsonValue]]:
    if type(envelope) is not dict:
        raise LifecycleContractError("contract envelope must be an object")
    detached = cast(dict[str, JsonValue], canonical_clone(dict(envelope)))
    try:
        require_valid_envelope(detached)
    except ValueError as exc:
        raise LifecycleContractError("contract envelope is invalid") from exc
    if detached.get("schema_id") != expected_schema_id:
        raise LifecycleContractError(
            f"expected schema {expected_schema_id!r}; "
            f"got {detached.get('schema_id')!r}"
        )
    value = detached.get("value")
    if type(value) is not dict:
        raise LifecycleContractError("contract value must be an object")
    return detached, cast(dict[str, JsonValue], value)


@dataclass(frozen=True, slots=True)
class FrozenLifecycleEnvelope:
    """Canonical lifecycle bytes with detached envelope access."""

    canonical_envelope_bytes: bytes
    expected_schema_id: str

    def __post_init__(self) -> None:
        if type(self.canonical_envelope_bytes) is not bytes:
            raise TypeError("canonical_envelope_bytes must be bytes")
        _envelope_value(self.as_envelope(), self.expected_schema_id)

    def as_envelope(self) -> ContractEnvelope:
        parsed = canonical_loads(self.canonical_envelope_bytes)
        if type(parsed) is not dict:
            raise LifecycleContractError("contract envelope must be an object")
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
            raise LifecycleContractError("contract value must be an object")
        return cast(dict[str, JsonValue], value)


@dataclass(frozen=True, slots=True)
class AttemptObservation:
    """Typed immutable observation of one submission response boundary."""

    response_state: str
    evidence_id: str
    evidence_sha256: str
    observed_at: str
    native_effect_ref: str | None = None
    accepted_artifact_sha256s: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.response_state not in RESPONSE_STATES:
            raise LifecycleContractError(
                f"response_state must be one of {sorted(RESPONSE_STATES)}"
            )
        _non_empty(self.evidence_id, "observation.evidence_id")
        _sha256(self.evidence_sha256, "observation.evidence_sha256")
        _timestamp(self.observed_at, "observation.observed_at")
        if self.native_effect_ref is not None:
            _non_empty(self.native_effect_ref, "observation.native_effect_ref")
        if type(self.accepted_artifact_sha256s) is not tuple:
            raise LifecycleContractError(
                "accepted_artifact_sha256s must be a tuple"
            )
        for index, digest in enumerate(self.accepted_artifact_sha256s):
            _sha256(digest, f"accepted_artifact_sha256s[{index}]")
        if self.response_state == "accepted":
            if self.native_effect_ref is None or not self.accepted_artifact_sha256s:
                raise LifecycleContractError(
                    "accepted response requires native effect and artifact evidence"
                )
        elif self.accepted_artifact_sha256s:
            raise LifecycleContractError(
                "only accepted responses may name accepted artifacts"
            )
        if self.response_state == "rejected-no-effect" and self.native_effect_ref:
            raise LifecycleContractError(
                "rejected-no-effect response cannot name a native effect"
            )

    def as_value(self) -> dict[str, JsonValue]:
        return {
            "response_state": self.response_state,
            "evidence_id": self.evidence_id,
            "evidence_sha256": self.evidence_sha256,
            "observed_at": self.observed_at,
            "native_effect_ref": self.native_effect_ref,
            "accepted_artifact_sha256s": list(self.accepted_artifact_sha256s),
        }


@dataclass(frozen=True, slots=True)
class ReconciliationEvidence:
    """Typed evidence that preserves rather than guesses unknown state."""

    outcome: str
    evidence_id: str
    evidence_sha256: str
    observed_at: str
    native_effect_ref: str | None = None
    observed_artifact_sha256s: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.outcome not in RECONCILIATION_OUTCOMES:
            raise LifecycleContractError(
                f"outcome must be one of {sorted(RECONCILIATION_OUTCOMES)}"
            )
        _non_empty(self.evidence_id, "reconciliation.evidence_id")
        _sha256(self.evidence_sha256, "reconciliation.evidence_sha256")
        _timestamp(self.observed_at, "reconciliation.observed_at")
        if self.native_effect_ref is not None:
            _non_empty(self.native_effect_ref, "reconciliation.native_effect_ref")
        if type(self.observed_artifact_sha256s) is not tuple:
            raise LifecycleContractError(
                "observed_artifact_sha256s must be a tuple"
            )
        for index, digest in enumerate(self.observed_artifact_sha256s):
            _sha256(digest, f"observed_artifact_sha256s[{index}]")
        if self.outcome == "effect-found":
            if self.native_effect_ref is None or not self.observed_artifact_sha256s:
                raise LifecycleContractError(
                    "effect-found requires native effect and artifact evidence"
                )
        elif self.observed_artifact_sha256s:
            raise LifecycleContractError(
                "only effect-found may name observed artifacts"
            )
        if self.outcome == "no-effect" and self.native_effect_ref is not None:
            raise LifecycleContractError(
                "no-effect reconciliation cannot name a native effect"
            )

    def as_value(self) -> dict[str, JsonValue]:
        return {
            "outcome": self.outcome,
            "evidence_id": self.evidence_id,
            "evidence_sha256": self.evidence_sha256,
            "observed_at": self.observed_at,
            "native_effect_ref": self.native_effect_ref,
            "observed_artifact_sha256s": list(self.observed_artifact_sha256s),
        }


@dataclass(frozen=True, slots=True)
class RetryBundle:
    """A retry plan paired with its new exact execution authorization."""

    plan: FrozenLifecycleEnvelope
    authorization: FrozenEvidenceEnvelope
    excluded_operation_ids: tuple[str, ...]


def _plan_authorization_binding(
    plan: Mapping[str, JsonValue], authorization: Mapping[str, JsonValue]
) -> tuple[
    dict[str, JsonValue],
    dict[str, JsonValue],
    dict[str, JsonValue],
    dict[str, JsonValue],
]:
    plan_envelope, plan_value = _envelope_value(plan, PLAN_SCHEMA_ID)
    authorization_envelope, authorization_value = _envelope_value(
        authorization, EXECUTION_AUTHORIZATION_SCHEMA_ID
    )
    if authorization_value.get("plan_digest") != plan_envelope.get("digest"):
        raise LifecycleContractError("authorization is stale for the exact plan")
    if authorization_value.get("manifest_digest") != plan_value.get(
        "manifest_digest"
    ):
        raise LifecycleContractError("authorization manifest binding mismatch")
    if authorization_value.get("capability_profile_digest") != plan_value.get(
        "capability_profile_digest"
    ):
        raise LifecycleContractError("authorization capability binding mismatch")
    return plan_envelope, plan_value, authorization_envelope, authorization_value


def _operation_map(value: dict[str, JsonValue]) -> dict[str, dict[str, JsonValue]]:
    raw_operations = value.get("operations")
    if type(raw_operations) is not list:
        raise LifecycleContractError("ledger operations must be a list")
    result: dict[str, dict[str, JsonValue]] = {}
    for raw in raw_operations:
        if type(raw) is not dict:
            raise LifecycleContractError("ledger operation must be an object")
        operation = cast(dict[str, JsonValue], raw)
        operation_id = operation.get("operation_id")
        if type(operation_id) is not str or not operation_id:
            raise LifecycleContractError("ledger operation id is invalid")
        if operation_id in result:
            raise LifecycleContractError(f"duplicate operation id: {operation_id}")
        result[operation_id] = operation
    return result


def _idempotency_value(support: str) -> dict[str, JsonValue]:
    if support not in IDEMPOTENCY_SUPPORT_VALUES:
        raise LifecycleContractError(
            f"idempotency support must be one of {sorted(IDEMPOTENCY_SUPPORT_VALUES)}"
        )
    if support == "supported":
        return {
            "support": support,
            "submission_key_enforcement": "native-effect-boundary",
            "limitation": None,
        }
    limitation = (
        "submission key is local ledger correlation only; native duplicate "
        "suppression is unsupported"
        if support == "unsupported"
        else "native duplicate suppression support is unknown"
    )
    return {
        "support": support,
        "submission_key_enforcement": "local-ledger-only",
        "limitation": limitation,
    }


def build_operation_ledger(
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    *,
    run_id: str,
    provider_idempotency_support: str,
    parent_run_id: str | None = None,
) -> FrozenLifecycleEnvelope:
    """Build revision zero of a stable operation/submission ledger."""

    plan_envelope, plan_value, authorization_envelope, _authorization_value = (
        _plan_authorization_binding(plan, authorization)
    )
    _non_empty(run_id, "run_id")
    if parent_run_id is not None:
        _non_empty(parent_run_id, "parent_run_id")
    idempotency = _idempotency_value(provider_idempotency_support)
    raw_operations = plan_value.get("operations")
    if type(raw_operations) is not list or not raw_operations:
        raise LifecycleContractError("plan operations must be a non-empty list")
    operations: list[dict[str, JsonValue]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_operations):
        if type(raw) is not dict:
            raise LifecycleContractError(f"plan operation {index} must be an object")
        operation = cast(dict[str, JsonValue], raw)
        operation_id = _non_empty(
            cast(str, operation.get("operation_id")), f"operations[{index}].id"
        )
        if operation_id in seen:
            raise LifecycleContractError(f"duplicate operation id: {operation_id}")
        seen.add(operation_id)
        selected = operation.get("selected_segment_ids")
        if type(selected) is not list or not selected:
            raise LifecycleContractError(
                f"operation {operation_id} selection must be non-empty"
            )
        operations.append(
            {
                "operation_id": operation_id,
                "operation_fingerprint": _sha256(
                    cast(str, operation.get("operation_fingerprint")),
                    f"{operation_id}.operation_fingerprint",
                ),
                "submission_key": _non_empty(
                    cast(str, operation.get("submission_key")),
                    f"{operation_id}.submission_key",
                ),
                "projected_payload_sha256": _sha256(
                    cast(str, operation.get("projected_payload_sha256")),
                    f"{operation_id}.projected_payload_sha256",
                ),
                "selected_segment_ids": canonical_clone(
                    cast(list[JsonValue], selected)
                ),
                "idempotency": canonical_clone(idempotency),
                "state": "planned",
                "submission_attempts": [],
                "duplicate_risk_authorization": None,
            }
        )
    value: dict[str, JsonValue] = {
        "run_id": run_id,
        "parent_run_id": parent_run_id,
        "plan_digest": cast(str, plan_envelope["digest"]),
        "execution_authorization_digest": cast(
            str, authorization_envelope["digest"]
        ),
        "revision": 0,
        "previous_ledger_digest": None,
        "provider_idempotency_support": provider_idempotency_support,
        "operations": operations,
    }
    envelope = make_envelope(
        OPERATION_LEDGER_SCHEMA_ID,
        value,
        schema_version=LIFECYCLE_SCHEMA_VERSION,
    )
    frozen = FrozenLifecycleEnvelope(
        canonical_bytes(envelope), OPERATION_LEDGER_SCHEMA_ID
    )
    validate_operation_ledger(
        frozen.as_envelope(), plan=plan, authorization=authorization
    )
    return frozen


def _validate_evidence_fields(value: dict[str, JsonValue], prefix: str) -> None:
    _non_empty(cast(str, value.get("evidence_id")), f"{prefix}.evidence_id")
    _sha256(
        cast(str, value.get("evidence_sha256")), f"{prefix}.evidence_sha256"
    )
    _timestamp(cast(str, value.get("observed_at")), f"{prefix}.observed_at")


def validate_operation_ledger(
    ledger: Mapping[str, JsonValue],
    *,
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
) -> None:
    """Require exact plan/auth binding and internally coherent operation state."""

    ledger_envelope, value = _envelope_value(ledger, OPERATION_LEDGER_SCHEMA_ID)
    plan_envelope, plan_value, authorization_envelope, _authorization_value = (
        _plan_authorization_binding(plan, authorization)
    )
    if value.get("plan_digest") != plan_envelope.get("digest"):
        raise LifecycleContractError("ledger plan binding mismatch")
    if value.get("execution_authorization_digest") != authorization_envelope.get(
        "digest"
    ):
        raise LifecycleContractError("ledger authorization binding mismatch")
    revision = value.get("revision")
    if type(revision) is not int or revision < 0:
        raise LifecycleContractError("ledger revision is invalid")
    previous = value.get("previous_ledger_digest")
    if previous is not None:
        _sha256(cast(str, previous), "previous_ledger_digest")
    support = value.get("provider_idempotency_support")
    if support not in IDEMPOTENCY_SUPPORT_VALUES:
        raise LifecycleContractError("ledger idempotency support is invalid")

    ledger_operations = _operation_map(value)
    raw_plan_operations = plan_value.get("operations")
    if type(raw_plan_operations) is not list:
        raise LifecycleContractError("plan operations must be a list")
    plan_operations = {
        cast(str, operation["operation_id"]): operation
        for operation in raw_plan_operations
        if type(operation) is dict and type(operation.get("operation_id")) is str
    }
    if list(ledger_operations) != list(plan_operations):
        raise LifecycleContractError("ledger operation inventory/order mismatch")

    expected_idempotency = _idempotency_value(cast(str, support))
    for operation_id, operation in ledger_operations.items():
        planned = cast(dict[str, JsonValue], plan_operations[operation_id])
        bindings = {
            "operation_fingerprint": planned.get("operation_fingerprint"),
            "submission_key": planned.get("submission_key"),
            "projected_payload_sha256": planned.get("projected_payload_sha256"),
            "selected_segment_ids": planned.get("selected_segment_ids"),
        }
        for field, expected in bindings.items():
            if operation.get(field) != expected:
                raise LifecycleContractError(
                    f"ledger {operation_id} {field} binding mismatch"
                )
        if operation.get("idempotency") != expected_idempotency:
            raise LifecycleContractError(
                f"ledger {operation_id} idempotency disclosure mismatch"
            )
        state = operation.get("state")
        if state not in OPERATION_STATES:
            raise LifecycleContractError(
                f"ledger {operation_id} state is invalid: {state!r}"
            )
        attempts = operation.get("submission_attempts")
        if type(attempts) is not list or len(attempts) > 1:
            raise LifecycleContractError(
                f"ledger {operation_id} permits at most one submission attempt"
            )
        risk = operation.get("duplicate_risk_authorization")
        if not attempts:
            if state != "planned" or risk is not None:
                raise LifecycleContractError(
                    f"unsubmitted operation {operation_id} has impossible state"
                )
            continue

        attempt = attempts[0]
        if type(attempt) is not dict:
            raise LifecycleContractError("submission attempt must be an object")
        attempt_value = cast(dict[str, JsonValue], attempt)
        if attempt_value.get("sent_payload_sha256") != operation.get(
            "projected_payload_sha256"
        ):
            raise LifecycleContractError(
                f"{operation_id} sent payload differs from planned payload"
            )
        if attempt_value.get("submission_key") != operation.get("submission_key"):
            raise LifecycleContractError(
                f"{operation_id} submission key differs from plan"
            )
        _timestamp(
            cast(str, attempt_value.get("submitted_at")),
            f"{operation_id}.submitted_at",
        )
        response_state = attempt_value.get("response_state")
        if response_state not in RESPONSE_STATES:
            raise LifecycleContractError(f"{operation_id} response state is invalid")
        _validate_evidence_fields(attempt_value, f"{operation_id}.response")
        reconciliations = attempt_value.get("reconciliation_attempts")
        if type(reconciliations) is not list:
            raise LifecycleContractError("reconciliation attempts must be a list")

        expected_state = cast(str, response_state)
        if response_state == "unknown":
            expected_state = "unknown"
            for ordinal, raw_reconciliation in enumerate(reconciliations, start=1):
                if type(raw_reconciliation) is not dict:
                    raise LifecycleContractError(
                        "reconciliation evidence must be an object"
                    )
                reconciliation = cast(dict[str, JsonValue], raw_reconciliation)
                if reconciliation.get("ordinal") != ordinal:
                    raise LifecycleContractError(
                        "reconciliation ordinals must be contiguous"
                    )
                _validate_evidence_fields(
                    reconciliation, f"{operation_id}.reconciliation[{ordinal}]"
                )
                outcome = reconciliation.get("outcome")
                if outcome not in RECONCILIATION_OUTCOMES:
                    raise LifecycleContractError("reconciliation outcome is invalid")
                expected_state = {
                    "still-unknown": "unknown",
                    "no-effect": "reconciled-no-effect",
                    "effect-found": "effect-found",
                }[cast(str, outcome)]
                if outcome != "still-unknown" and ordinal != len(reconciliations):
                    raise LifecycleContractError(
                        "terminal reconciliation must be the last attempt"
                    )
            if risk is not None:
                if expected_state != "unknown" or type(risk) is not dict:
                    raise LifecycleContractError(
                        "duplicate-risk authorization requires unresolved unknown"
                    )
                _sha256(
                    cast(str, risk.get("authorization_digest")),
                    "duplicate_risk_authorization.digest",
                )
                expected_state = "duplicate-risk-authorized"
        elif reconciliations or risk is not None:
            raise LifecycleContractError(
                f"{operation_id} non-unknown response cannot be reconciled"
            )
        if state != expected_state:
            raise LifecycleContractError(
                f"{operation_id} state {state!r} does not match evidence "
                f"{expected_state!r}"
            )
    require_valid_envelope(ledger_envelope)


def _next_ledger(
    ledger: Mapping[str, JsonValue], value: dict[str, JsonValue]
) -> FrozenLifecycleEnvelope:
    previous_envelope, _previous_value = _envelope_value(
        ledger, OPERATION_LEDGER_SCHEMA_ID
    )
    current_revision = value.get("revision")
    if type(current_revision) is not int:
        raise LifecycleContractError("ledger revision is invalid")
    value["revision"] = current_revision + 1
    value["previous_ledger_digest"] = cast(str, previous_envelope["digest"])
    envelope = make_envelope(
        OPERATION_LEDGER_SCHEMA_ID,
        value,
        schema_version=LIFECYCLE_SCHEMA_VERSION,
    )
    return FrozenLifecycleEnvelope(
        canonical_bytes(envelope), OPERATION_LEDGER_SCHEMA_ID
    )


def record_submission(
    ledger: Mapping[str, JsonValue],
    *,
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    operation_id: str,
    sent_payload_sha256: str,
    submitted_at: str,
    observation: AttemptObservation,
    secret_resolver: Callable[..., object] | None = None,
) -> FrozenLifecycleEnvelope:
    """Append the sole submission attempt for an operation without effects."""

    _ = secret_resolver
    validate_operation_ledger(ledger, plan=plan, authorization=authorization)
    _ledger_envelope, value = _envelope_value(ledger, OPERATION_LEDGER_SCHEMA_ID)
    operation = _operation_map(value).get(operation_id)
    if operation is None:
        raise LifecycleContractError(f"unknown operation: {operation_id}")
    if operation.get("state") != "planned":
        raise LifecycleContractError(
            f"operation {operation_id} already has a submission attempt"
        )
    payload_digest = _sha256(sent_payload_sha256, "sent_payload_sha256")
    if payload_digest != operation.get("projected_payload_sha256"):
        raise LifecycleContractError("sent payload differs from planned payload")
    _timestamp(submitted_at, "submitted_at")
    run_id = cast(str, value["run_id"])
    attempt_value = observation.as_value()
    attempt_value.update(
        {
            "attempt_id": f"{run_id}:{operation_id}:attempt-001",
            "submission_key": cast(str, operation["submission_key"]),
            "sent_payload_sha256": payload_digest,
            "submitted_at": submitted_at,
            "reconciliation_attempts": [],
        }
    )
    operation["submission_attempts"] = [attempt_value]
    operation["state"] = observation.response_state
    next_ledger = _next_ledger(ledger, value)
    validate_operation_ledger(
        next_ledger.as_envelope(), plan=plan, authorization=authorization
    )
    return next_ledger


def reconcile_unknown(
    ledger: Mapping[str, JsonValue],
    *,
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    operation_id: str,
    attempt_id: str,
    evidence: ReconciliationEvidence,
    secret_resolver: Callable[..., object] | None = None,
) -> FrozenLifecycleEnvelope:
    """Append explicit reconciliation evidence for an unresolved submission."""

    _ = secret_resolver
    validate_operation_ledger(ledger, plan=plan, authorization=authorization)
    _ledger_envelope, value = _envelope_value(ledger, OPERATION_LEDGER_SCHEMA_ID)
    operation = _operation_map(value).get(operation_id)
    if operation is None:
        raise LifecycleContractError(f"unknown operation: {operation_id}")
    if operation.get("state") != "unknown":
        raise UnknownEffectBlocked(
            f"operation {operation_id} is not an unresolved unknown"
        )
    attempts = cast(list[dict[str, JsonValue]], operation["submission_attempts"])
    attempt = attempts[0]
    if attempt.get("attempt_id") != attempt_id:
        raise LifecycleContractError("reconciliation attempt binding mismatch")
    reconciliations = cast(
        list[dict[str, JsonValue]], attempt["reconciliation_attempts"]
    )
    record = evidence.as_value()
    record["ordinal"] = len(reconciliations) + 1
    reconciliations.append(record)
    operation["state"] = {
        "still-unknown": "unknown",
        "no-effect": "reconciled-no-effect",
        "effect-found": "effect-found",
    }[evidence.outcome]
    next_ledger = _next_ledger(ledger, value)
    validate_operation_ledger(
        next_ledger.as_envelope(), plan=plan, authorization=authorization
    )
    return next_ledger


def build_duplicate_risk_authorization(
    ledger: Mapping[str, JsonValue],
    *,
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    operation_id: str,
    attempt_id: str,
    authorization_id: str,
    reviewer: str,
    risk_statement: str,
    authorized_at: str,
    expires_at: str,
) -> FrozenLifecycleEnvelope:
    """Build a separate owner decision for one exact unresolved attempt."""

    validate_operation_ledger(ledger, plan=plan, authorization=authorization)
    ledger_envelope, value = _envelope_value(ledger, OPERATION_LEDGER_SCHEMA_ID)
    operation = _operation_map(value).get(operation_id)
    if operation is None or operation.get("state") != "unknown":
        raise UnknownEffectBlocked("duplicate-risk decision requires exact unknown")
    attempts = cast(list[dict[str, JsonValue]], operation["submission_attempts"])
    if attempts[0].get("attempt_id") != attempt_id:
        raise LifecycleContractError("duplicate-risk attempt binding mismatch")
    _non_empty(authorization_id, "authorization_id")
    _non_empty(reviewer, "reviewer")
    _non_empty(risk_statement, "risk_statement")
    _timestamp(authorized_at, "authorized_at")
    _timestamp(expires_at, "expires_at")
    risk_value: dict[str, JsonValue] = {
        "authorization_id": authorization_id,
        "decision": "accept-duplicate-effect-risk",
        "ledger_digest": cast(str, ledger_envelope["digest"]),
        "plan_digest": cast(str, value["plan_digest"]),
        "operation_id": operation_id,
        "operation_fingerprint": cast(str, operation["operation_fingerprint"]),
        "attempt_id": attempt_id,
        "reviewer": reviewer,
        "risk_statement": risk_statement,
        "authorized_at": authorized_at,
        "expires_at": expires_at,
    }
    envelope = make_envelope(
        DUPLICATE_RISK_AUTHORIZATION_SCHEMA_ID,
        risk_value,
        schema_version=LIFECYCLE_SCHEMA_VERSION,
    )
    return FrozenLifecycleEnvelope(
        canonical_bytes(envelope), DUPLICATE_RISK_AUTHORIZATION_SCHEMA_ID
    )


def record_duplicate_risk_authorization(
    ledger: Mapping[str, JsonValue],
    risk_authorization: Mapping[str, JsonValue],
    *,
    plan: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    now: str,
    secret_resolver: Callable[..., object] | None = None,
) -> FrozenLifecycleEnvelope:
    """Consume and record one current, exact duplicate-risk decision."""

    _ = secret_resolver
    validate_operation_ledger(ledger, plan=plan, authorization=authorization)
    ledger_envelope, value = _envelope_value(ledger, OPERATION_LEDGER_SCHEMA_ID)
    risk_envelope, risk_value = _envelope_value(
        risk_authorization, DUPLICATE_RISK_AUTHORIZATION_SCHEMA_ID
    )
    if risk_value.get("ledger_digest") != ledger_envelope.get("digest"):
        raise LifecycleContractError("duplicate-risk authorization is stale")
    if risk_value.get("plan_digest") != value.get("plan_digest"):
        raise LifecycleContractError("duplicate-risk plan binding mismatch")
    now_value = _timestamp(now, "now")
    authorized_at = _timestamp(
        cast(str, risk_value.get("authorized_at")), "authorized_at"
    )
    expires_at = _timestamp(cast(str, risk_value.get("expires_at")), "expires_at")
    if now_value < authorized_at:
        raise LifecycleContractError("duplicate-risk authorization is not active")
    if now_value >= expires_at:
        raise LifecycleContractError("duplicate-risk authorization is expired")
    operation_id = cast(str, risk_value.get("operation_id"))
    operation = _operation_map(value).get(operation_id)
    if operation is None or operation.get("state") != "unknown":
        raise UnknownEffectBlocked("duplicate-risk target is not unresolved unknown")
    attempts = cast(list[dict[str, JsonValue]], operation["submission_attempts"])
    if attempts[0].get("attempt_id") != risk_value.get("attempt_id"):
        raise LifecycleContractError("duplicate-risk attempt binding mismatch")
    if operation.get("operation_fingerprint") != risk_value.get(
        "operation_fingerprint"
    ):
        raise LifecycleContractError("duplicate-risk operation binding mismatch")
    operation["duplicate_risk_authorization"] = {
        "authorization_digest": cast(str, risk_envelope["digest"]),
        "authorized_ledger_digest": cast(str, ledger_envelope["digest"]),
        "authorization_id": risk_value.get("authorization_id"),
        "reviewer": risk_value.get("reviewer"),
        "risk_statement": risk_value.get("risk_statement"),
        "authorized_at": risk_value.get("authorized_at"),
        "expires_at": risk_value.get("expires_at"),
    }
    operation["state"] = "duplicate-risk-authorized"
    next_ledger = _next_ledger(ledger, value)
    validate_operation_ledger(
        next_ledger.as_envelope(), plan=plan, authorization=authorization
    )
    return next_ledger


def _retry_effect_units(
    plan_value: dict[str, JsonValue], selected_segment_ids: list[str]
) -> tuple[int, list[dict[str, JsonValue]]]:
    raw_transformations = plan_value.get("transformations")
    if type(raw_transformations) is not list:
        raise RetryBlocked("plan transformation ledger is missing")
    selected = set(selected_segment_ids)
    transformations: list[dict[str, JsonValue]] = []
    projected_by_segment: dict[str, str] = {}
    for raw in raw_transformations:
        if type(raw) is not dict:
            raise RetryBlocked("plan transformation record is invalid")
        record = cast(dict[str, JsonValue], raw)
        segment_id = record.get("segment_id")
        if segment_id in selected:
            transformations.append(
                cast(dict[str, JsonValue], canonical_clone(record))
            )
            projected = record.get("projected_text")
            if type(segment_id) is str and type(projected) is str:
                projected_by_segment[segment_id] = projected
    if set(projected_by_segment) != selected:
        all_selected = plan_value.get("selected_segment_ids")
        estimates = plan_value.get("effect_estimates")
        if (
            all_selected == selected_segment_ids
            and type(estimates) is dict
            and type(estimates.get("projected_text_utf8_bytes")) is int
        ):
            return cast(int, estimates["projected_text_utf8_bytes"]), transformations
        missing = sorted(selected - set(projected_by_segment))
        raise RetryBlocked(
            f"retry effect estimate lacks projected text for segments: {missing}"
        )
    units = sum(
        len(projected_by_segment[segment_id].encode("utf-8"))
        for segment_id in selected_segment_ids
    )
    return units, transformations


def prepare_bounded_retry(
    plan: Mapping[str, JsonValue],
    ledger: Mapping[str, JsonValue],
    authorization: Mapping[str, JsonValue],
    *,
    requested_operation_ids: tuple[str, ...],
    max_retry_operations: int,
    max_retry_depth: int,
    new_authorization_id: str,
    account_ref: str,
    execution_scope: str,
    issued_at: str,
    expires_at: str,
    max_effect_units: int,
    prerequisite_evidence: tuple[ProtectedPrerequisite, ...],
    secret_resolver: Callable[..., object] | None = None,
) -> RetryBundle:
    """Build one bounded retry plan and a distinct exact authorization."""

    _ = secret_resolver
    validate_operation_ledger(ledger, plan=plan, authorization=authorization)
    ledger_envelope, ledger_value = _envelope_value(
        ledger, OPERATION_LEDGER_SCHEMA_ID
    )
    plan_envelope, plan_value, authorization_envelope, authorization_value = (
        _plan_authorization_binding(plan, authorization)
    )
    if type(requested_operation_ids) is not tuple or not requested_operation_ids:
        raise RetryBlocked("requested_operation_ids must be a non-empty tuple")
    if len(set(requested_operation_ids)) != len(requested_operation_ids):
        raise RetryBlocked("requested retry operations must be unique")
    if type(max_retry_operations) is not int or max_retry_operations < 1:
        raise RetryBlocked("max_retry_operations must be positive")
    if type(max_retry_depth) is not int or max_retry_depth < 1:
        raise RetryBlocked("max_retry_depth must be positive")
    if new_authorization_id == authorization_value.get("authorization_id"):
        raise RetryBlocked("retry requires a new authorization id")

    lineage = plan_value.get("retry_lineage")
    if lineage is None:
        parent_depth = 0
    elif type(lineage) is dict and type(lineage.get("retry_depth")) is int:
        parent_depth = cast(int, lineage["retry_depth"])
    else:
        raise RetryBlocked("parent retry lineage is invalid")
    retry_depth = parent_depth + 1
    if retry_depth > max_retry_depth:
        raise RetryBlocked("retry depth exceeds the declared bound")

    operations = _operation_map(ledger_value)
    unknown_ids = sorted(set(requested_operation_ids) - set(operations))
    if unknown_ids:
        raise RetryBlocked(f"retry names unknown operations: {unknown_ids}")
    eligible: list[dict[str, JsonValue]] = []
    excluded: list[str] = []
    excluded_evidence: list[dict[str, JsonValue]] = []
    eligibility_evidence: list[dict[str, JsonValue]] = []
    blocked: list[str] = []
    for operation_id in requested_operation_ids:
        operation = operations[operation_id]
        state = operation.get("state")
        attempts = cast(list[dict[str, JsonValue]], operation["submission_attempts"])
        if state in {"accepted", "effect-found"}:
            excluded.append(operation_id)
            attempt = attempts[0]
            artifact_hashes = cast(
                list[JsonValue], attempt.get("accepted_artifact_sha256s", [])
            )
            if state == "effect-found":
                reconciliations = cast(
                    list[dict[str, JsonValue]], attempt["reconciliation_attempts"]
                )
                artifact_hashes = cast(
                    list[JsonValue],
                    reconciliations[-1].get("observed_artifact_sha256s", []),
                )
            excluded_evidence.append(
                {
                    "operation_id": operation_id,
                    "state": cast(str, state),
                    "artifact_sha256s": canonical_clone(artifact_hashes),
                }
            )
            continue
        if state in {"planned", "unknown"}:
            blocked.append(f"{operation_id}:{state}")
            continue
        if state not in {
            "rejected-no-effect",
            "reconciled-no-effect",
            "duplicate-risk-authorized",
        }:
            blocked.append(f"{operation_id}:{state}")
            continue
        eligible.append(operation)
        if state == "rejected-no-effect":
            source = attempts[0]
            eligibility_evidence.append(
                {
                    "operation_id": operation_id,
                    "basis": "response-proved-no-effect",
                    "evidence_id": source.get("evidence_id"),
                    "evidence_sha256": source.get("evidence_sha256"),
                }
            )
        elif state == "reconciled-no-effect":
            reconciliations = cast(
                list[dict[str, JsonValue]], attempts[0]["reconciliation_attempts"]
            )
            source = reconciliations[-1]
            eligibility_evidence.append(
                {
                    "operation_id": operation_id,
                    "basis": "reconciliation-proved-no-effect",
                    "evidence_id": source.get("evidence_id"),
                    "evidence_sha256": source.get("evidence_sha256"),
                }
            )
        else:
            risk = cast(dict[str, JsonValue], operation["duplicate_risk_authorization"])
            eligibility_evidence.append(
                {
                    "operation_id": operation_id,
                    "basis": "duplicate-effect-risk-authorized",
                    "authorization_digest": risk.get("authorization_digest"),
                }
            )
    if blocked:
        raise UnknownEffectBlocked(
            f"retry blocked until exact reconciliation or risk authorization: {blocked}"
        )
    if not eligible:
        raise RetryBlocked("no retryable operations remain after evidence exclusion")
    if len(eligible) > max_retry_operations:
        raise RetryBlocked("retry operation count exceeds the declared bound")

    retry_segment_ids: list[str] = []
    retry_groups: set[str] = set()
    for operation in eligible:
        for segment_id in cast(list[str], operation["selected_segment_ids"]):
            if segment_id not in retry_segment_ids:
                retry_segment_ids.append(segment_id)
        planned_operation = next(
            cast(dict[str, JsonValue], item)
            for item in cast(list[JsonValue], plan_value["operations"])
            if type(item) is dict
            and item.get("operation_id") == operation.get("operation_id")
        )
        group_id = planned_operation.get("composite_group_id")
        if type(group_id) is str:
            retry_groups.add(group_id)

    support = cast(str, ledger_value["provider_idempotency_support"])
    retry_operations: list[dict[str, JsonValue]] = []
    source_operation_ids: list[str] = []
    for ordinal, operation in enumerate(eligible, start=1):
        operation_id = cast(str, operation["operation_id"])
        source_operation_ids.append(operation_id)
        planned_operation = next(
            cast(dict[str, JsonValue], item)
            for item in cast(list[JsonValue], plan_value["operations"])
            if type(item) is dict and item.get("operation_id") == operation_id
        )
        retry_operation = cast(
            dict[str, JsonValue], canonical_clone(planned_operation)
        )
        retry_operation["parent_operation_id"] = operation_id
        retry_operation["operation_id"] = (
            f"retry-{retry_depth:03d}-{ordinal:03d}-{operation_id}"
        )
        if support != "supported":
            fingerprint = cast(str, operation["operation_fingerprint"])
            retry_operation["submission_key"] = (
                "local-"
                + canonical_sha256(
                    {
                        "parent_plan_digest": cast(str, plan_envelope["digest"]),
                        "operation_fingerprint": fingerprint,
                        "retry_depth": retry_depth,
                        "retry_ordinal": ordinal,
                    }
                )
            )
        retry_operations.append(retry_operation)

    raw_outputs = plan_value.get("expected_outputs")
    if type(raw_outputs) is not list:
        raise RetryBlocked("parent expected outputs are missing")
    retry_outputs: list[dict[str, JsonValue]] = []
    selected_set = set(retry_segment_ids)
    for raw in raw_outputs:
        if type(raw) is not dict:
            raise RetryBlocked("parent expected output is invalid")
        output = cast(dict[str, JsonValue], raw)
        output_segments = output.get("segment_ids")
        matches = output.get("segment_id") in selected_set
        if type(output_segments) is list and set(output_segments) & selected_set:
            matches = True
        if output.get("composite_group_id") in retry_groups:
            matches = True
        if matches:
            retry_output = cast(dict[str, JsonValue], canonical_clone(output))
            parent_output_id = retry_output.get("expected_output_id")
            retry_output["parent_expected_output_id"] = parent_output_id
            retry_output["expected_output_id"] = (
                f"retry-{retry_depth:03d}-{parent_output_id}"
            )
            retry_outputs.append(retry_output)
    if not retry_outputs:
        raise RetryBlocked("no expected outputs match retry operations")

    effect_units, retry_transformations = _retry_effect_units(
        plan_value, retry_segment_ids
    )
    native_schema_basis = plan_value.get("native_schema_basis")
    if type(native_schema_basis) is not dict:
        raise RetryBlocked("parent native schema basis is invalid")
    warnings = plan_value.get("warnings")
    if type(warnings) is not list:
        raise RetryBlocked("parent warnings must be a list")
    retry_lineage: dict[str, JsonValue] = {
        "parent_plan_digest": cast(str, plan_envelope["digest"]),
        "parent_ledger_digest": cast(str, ledger_envelope["digest"]),
        "parent_execution_authorization_digest": cast(
            str, authorization_envelope["digest"]
        ),
        "parent_run_id": ledger_value.get("run_id"),
        "retry_depth": retry_depth,
        "source_operation_ids": source_operation_ids,
        "excluded_operation_ids": excluded,
        "excluded_accepted_evidence": excluded_evidence,
        "eligibility_evidence": eligibility_evidence,
        "provider_idempotency_support": support,
        "submission_key_limitation": _idempotency_value(support)["limitation"],
    }
    retry_value: dict[str, JsonValue] = {
        "manifest_digest": cast(str, plan_value["manifest_digest"]),
        "capability_profile_digest": cast(
            str, plan_value["capability_profile_digest"]
        ),
        "selected_segment_ids": retry_segment_ids,
        "operations": retry_operations,
        "expected_outputs": retry_outputs,
        "effect_estimates": {
            "operation_count": len(retry_operations),
            "projected_text_utf8_bytes": effect_units,
            "external_effects": 0,
        },
        "warnings": cast(
            list[JsonValue],
            canonical_clone(
                [
                    *cast(list[str], warnings),
                    "bounded retry plan only; no provider execution evidence",
                ]
            ),
        ),
        "blocked_requirements": [],
        "transformations": retry_transformations,
        "native_schema_basis": canonical_clone(native_schema_basis),
        "retry_lineage": retry_lineage,
    }
    retry_envelope = make_envelope(
        PLAN_SCHEMA_ID,
        retry_value,
        schema_version=LIFECYCLE_SCHEMA_VERSION,
    )
    retry_plan = FrozenLifecycleEnvelope(
        canonical_bytes(retry_envelope), PLAN_SCHEMA_ID
    )
    new_authorization = build_execution_authorization(
        retry_plan.as_envelope(),
        authorization_id=new_authorization_id,
        account_ref=account_ref,
        execution_scope=execution_scope,
        issued_at=issued_at,
        expires_at=expires_at,
        max_effect_units=max_effect_units,
        prerequisite_evidence=prerequisite_evidence,
    )
    if new_authorization.digest == authorization_envelope.get("digest"):
        raise RetryBlocked("retry authorization must be distinct from parent")
    return RetryBundle(
        plan=retry_plan,
        authorization=new_authorization,
        excluded_operation_ids=tuple(excluded),
    )
