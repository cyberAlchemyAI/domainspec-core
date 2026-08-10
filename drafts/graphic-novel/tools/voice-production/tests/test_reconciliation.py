from __future__ import annotations

import ast
import copy
import inspect
import socket
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest import mock


STAGING_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGING_ROOT))

from voice_production import lifecycle  # noqa: E402
from voice_production.contracts import plan_envelope  # noqa: E402
from voice_production.evidence import (  # noqa: E402
    REQUIRED_PREREQUISITE_KINDS,
    ProtectedPrerequisite,
    build_execution_authorization,
)
from voice_production.lifecycle import (  # noqa: E402
    AttemptObservation,
    LifecycleContractError,
    ReconciliationEvidence,
    RetryBlocked,
    UnknownEffectBlocked,
    build_duplicate_risk_authorization,
    build_operation_ledger,
    prepare_bounded_retry,
    reconcile_unknown,
    record_duplicate_risk_authorization,
    record_submission,
    validate_operation_ledger,
)


SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64
SHA_E = "e" * 64
SHA_F = "f" * 64
ACCOUNT = "synthetic-account-A"
SCOPE = "production/chapter-01/segments-001-003"
NOW = "2026-08-09T12:00:00Z"


class SecretResolverSpy:
    def __init__(self) -> None:
        self.called = False

    def __call__(self, *_args, **_kwargs):
        self.called = True
        raise AssertionError("secret resolution crossed the lifecycle boundary")


def make_plan():
    texts = {
        "segment-001": "first synthetic line",
        "segment-002": "second synthetic line",
        "segment-003": "third synthetic line",
    }
    operations = []
    outputs = []
    transformations = []
    for index, (segment_id, text) in enumerate(texts.items(), start=1):
        fingerprint = f"{index}" * 64
        payload_digest = f"{index + 3:x}" * 64
        operations.append(
            {
                "operation_id": f"operation-{index:03d}",
                "operation_fingerprint": fingerprint,
                "submission_key": f"local-{fingerprint}",
                "selected_segment_ids": [segment_id],
                "projected_payload_sha256": payload_digest,
                "expected_output_granularity": "segment",
            }
        )
        outputs.append(
            {
                "expected_output_id": f"expected-output-{index:03d}",
                "segment_id": segment_id,
                "output_granularity": "segment",
                "correlation_method": "segment-id",
            }
        )
        transformations.append(
            {
                "segment_id": segment_id,
                "exact_text": text,
                "exact_text_sha256": f"{index + 6:x}" * 64,
                "projected_text": text,
                "projected_text_sha256": f"{index + 6:x}" * 64,
                "transformations": [],
            }
        )
    units = sum(len(text.encode("utf-8")) for text in texts.values())
    return plan_envelope(
        manifest_digest=SHA_A,
        capability_profile_digest=SHA_B,
        selected_segment_ids=list(texts),
        operations=operations,
        expected_outputs=outputs,
        effect_estimates={
            "operation_count": 3,
            "projected_text_utf8_bytes": units,
            "external_effects": 0,
        },
        warnings=["synthetic lifecycle fixture"],
        blocked_requirements=[],
        transformations=transformations,
        native_schema_basis={
            "locator": "synthetic-schema://lifecycle/v1",
            "sha256": SHA_C,
        },
    )


def prerequisites() -> tuple[ProtectedPrerequisite, ...]:
    return tuple(
        ProtectedPrerequisite(
            kind=kind,
            evidence_id=f"protected-evidence-{index:03d}",
            evidence_sha256=f"{index:x}" * 64,
            accepted=True,
            expires_at="2026-09-01T00:00:00Z",
        )
        for index, kind in enumerate(sorted(REQUIRED_PREREQUISITE_KINDS), start=1)
    )


def make_authorization(plan, authorization_id: str = "authorization-001"):
    units = plan["value"]["effect_estimates"]["projected_text_utf8_bytes"]
    return build_execution_authorization(
        plan,
        authorization_id=authorization_id,
        account_ref=ACCOUNT,
        execution_scope=SCOPE,
        issued_at="2026-08-09T00:00:00Z",
        expires_at="2026-09-01T00:00:00Z",
        max_effect_units=units,
        prerequisite_evidence=prerequisites(),
    )


def make_ledger(plan, authorization, support: str = "unsupported"):
    return build_operation_ledger(
        plan,
        authorization.as_envelope(),
        run_id="synthetic-run-001",
        provider_idempotency_support=support,
    )


def payload_for(plan, operation_id: str) -> str:
    for operation in plan["value"]["operations"]:
        if operation["operation_id"] == operation_id:
            return operation["projected_payload_sha256"]
    raise AssertionError(operation_id)


def observation(state: str, ordinal: int) -> AttemptObservation:
    return AttemptObservation(
        response_state=state,
        evidence_id=f"response-evidence-{ordinal:03d}",
        evidence_sha256=f"{ordinal + 8:x}" * 64,
        observed_at=f"2026-08-09T10:0{ordinal}:01Z",
        native_effect_ref=(
            f"synthetic-effect:operation-{ordinal:03d}"
            if state == "accepted"
            else None
        ),
        accepted_artifact_sha256s=((SHA_D,) if state == "accepted" else ()),
    )


def submit(
    ledger,
    plan,
    authorization,
    operation_id: str,
    state: str,
    ordinal: int,
    *,
    secret_resolver=None,
):
    return record_submission(
        ledger.as_envelope(),
        plan=plan,
        authorization=authorization.as_envelope(),
        operation_id=operation_id,
        sent_payload_sha256=payload_for(plan, operation_id),
        submitted_at=f"2026-08-09T10:0{ordinal}:00Z",
        observation=observation(state, ordinal),
        secret_resolver=secret_resolver,
    )


def ledger_with_three_outcomes(plan, authorization, support: str = "unsupported"):
    ledger = make_ledger(plan, authorization, support)
    ledger = submit(ledger, plan, authorization, "operation-001", "accepted", 1)
    ledger = submit(ledger, plan, authorization, "operation-002", "unknown", 2)
    ledger = submit(
        ledger,
        plan,
        authorization,
        "operation-003",
        "rejected-no-effect",
        3,
    )
    return ledger


def attempt_id(ledger, operation_id: str) -> str:
    for operation in ledger.value["operations"]:
        if operation["operation_id"] == operation_id:
            return operation["submission_attempts"][0]["attempt_id"]
    raise AssertionError(operation_id)


def retry_kwargs(
    *,
    authorization_id: str = "authorization-retry-001",
    max_retry_operations: int = 3,
    max_retry_depth: int = 2,
    secret_resolver=None,
):
    return {
        "max_retry_operations": max_retry_operations,
        "max_retry_depth": max_retry_depth,
        "new_authorization_id": authorization_id,
        "account_ref": ACCOUNT,
        "execution_scope": SCOPE,
        "issued_at": "2026-08-09T12:00:00Z",
        "expires_at": "2026-09-01T00:00:00Z",
        "max_effect_units": 1_000,
        "prerequisite_evidence": prerequisites(),
        "secret_resolver": secret_resolver,
    }


class ReconciliationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = make_plan()
        self.authorization = make_authorization(self.plan)

    def test_initial_ledger_is_byte_stable_and_idempotency_limitation_is_explicit(self) -> None:
        first = make_ledger(self.plan, self.authorization)
        second = make_ledger(self.plan, self.authorization)
        self.assertEqual(first.canonical_envelope_bytes, second.canonical_envelope_bytes)
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(first.value["provider_idempotency_support"], "unsupported")
        for operation in first.value["operations"]:
            disclosure = operation["idempotency"]
            self.assertEqual(disclosure["support"], "unsupported")
            self.assertEqual(disclosure["submission_key_enforcement"], "local-ledger-only")
            self.assertIn("unsupported", disclosure["limitation"])

    def test_submission_ledger_retains_effect_fingerprint_payload_time_and_evidence(self) -> None:
        initial = make_ledger(self.plan, self.authorization)
        recorded = submit(
            initial,
            self.plan,
            self.authorization,
            "operation-002",
            "unknown",
            2,
        )
        operation = recorded.value["operations"][1]
        attempt = operation["submission_attempts"][0]
        self.assertEqual(operation["state"], "unknown")
        self.assertEqual(operation["operation_fingerprint"], "2" * 64)
        self.assertEqual(attempt["sent_payload_sha256"], payload_for(self.plan, "operation-002"))
        self.assertEqual(attempt["submitted_at"], "2026-08-09T10:02:00Z")
        self.assertEqual(attempt["response_state"], "unknown")
        self.assertEqual(attempt["reconciliation_attempts"], [])
        self.assertEqual(recorded.value["revision"], 1)
        self.assertEqual(recorded.value["previous_ledger_digest"], initial.digest)

    def test_unknown_and_repeat_submission_block_before_secret_or_network(self) -> None:
        ledger = make_ledger(self.plan, self.authorization)
        spy = SecretResolverSpy()
        ledger = submit(
            ledger,
            self.plan,
            self.authorization,
            "operation-002",
            "unknown",
            2,
            secret_resolver=spy,
        )
        denied = AssertionError("network helper must not be used")
        with (
            mock.patch.object(socket, "socket", side_effect=denied),
            mock.patch.object(socket, "create_connection", side_effect=denied),
            mock.patch.object(socket, "getaddrinfo", side_effect=denied),
            self.assertRaisesRegex(UnknownEffectBlocked, "reconciliation"),
        ):
            prepare_bounded_retry(
                self.plan,
                ledger.as_envelope(),
                self.authorization.as_envelope(),
                requested_operation_ids=("operation-002",),
                **retry_kwargs(secret_resolver=spy),
            )
        with self.assertRaisesRegex(LifecycleContractError, "already"):
            submit(
                ledger,
                self.plan,
                self.authorization,
                "operation-002",
                "unknown",
                2,
                secret_resolver=spy,
            )
        self.assertFalse(spy.called)

    def test_still_unknown_remains_blocked_then_no_effect_enables_retry(self) -> None:
        ledger = make_ledger(self.plan, self.authorization)
        ledger = submit(
            ledger,
            self.plan,
            self.authorization,
            "operation-002",
            "unknown",
            2,
        )
        bound_attempt = attempt_id(ledger, "operation-002")
        still_unknown = reconcile_unknown(
            ledger.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            operation_id="operation-002",
            attempt_id=bound_attempt,
            evidence=ReconciliationEvidence(
                outcome="still-unknown",
                evidence_id="reconciliation-001",
                evidence_sha256=SHA_E,
                observed_at="2026-08-09T11:00:00Z",
            ),
        )
        self.assertEqual(still_unknown.value["operations"][1]["state"], "unknown")
        with self.assertRaises(UnknownEffectBlocked):
            prepare_bounded_retry(
                self.plan,
                still_unknown.as_envelope(),
                self.authorization.as_envelope(),
                requested_operation_ids=("operation-002",),
                **retry_kwargs(),
            )
        no_effect = reconcile_unknown(
            still_unknown.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            operation_id="operation-002",
            attempt_id=bound_attempt,
            evidence=ReconciliationEvidence(
                outcome="no-effect",
                evidence_id="reconciliation-002",
                evidence_sha256=SHA_F,
                observed_at="2026-08-09T11:30:00Z",
            ),
        )
        bundle = prepare_bounded_retry(
            self.plan,
            no_effect.as_envelope(),
            self.authorization.as_envelope(),
            requested_operation_ids=("operation-002",),
            **retry_kwargs(),
        )
        self.assertEqual(bundle.plan.value["selected_segment_ids"], ["segment-002"])
        basis = bundle.plan.value["retry_lineage"]["eligibility_evidence"][0]
        self.assertEqual(basis["basis"], "reconciliation-proved-no-effect")
        self.assertEqual(basis["evidence_sha256"], SHA_F)

    def test_accepted_evidence_is_excluded_and_retry_has_lineage_and_new_auth(self) -> None:
        ledger = ledger_with_three_outcomes(self.plan, self.authorization)
        ledger = reconcile_unknown(
            ledger.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            operation_id="operation-002",
            attempt_id=attempt_id(ledger, "operation-002"),
            evidence=ReconciliationEvidence(
                outcome="no-effect",
                evidence_id="reconciliation-no-effect",
                evidence_sha256=SHA_F,
                observed_at="2026-08-09T11:30:00Z",
            ),
        )
        first = prepare_bounded_retry(
            self.plan,
            ledger.as_envelope(),
            self.authorization.as_envelope(),
            requested_operation_ids=(
                "operation-001",
                "operation-002",
                "operation-003",
            ),
            **retry_kwargs(),
        )
        second = prepare_bounded_retry(
            self.plan,
            ledger.as_envelope(),
            self.authorization.as_envelope(),
            requested_operation_ids=(
                "operation-001",
                "operation-002",
                "operation-003",
            ),
            **retry_kwargs(),
        )
        self.assertEqual(first.plan.canonical_envelope_bytes, second.plan.canonical_envelope_bytes)
        self.assertEqual(first.authorization.canonical_envelope_bytes, second.authorization.canonical_envelope_bytes)
        self.assertEqual(first.excluded_operation_ids, ("operation-001",))
        self.assertEqual(first.plan.value["selected_segment_ids"], ["segment-002", "segment-003"])
        self.assertEqual(
            [item["segment_id"] for item in first.plan.value["expected_outputs"]],
            ["segment-002", "segment-003"],
        )
        lineage = first.plan.value["retry_lineage"]
        self.assertEqual(lineage["parent_plan_digest"], self.plan["digest"])
        self.assertEqual(lineage["parent_ledger_digest"], ledger.digest)
        self.assertEqual(lineage["excluded_accepted_evidence"][0]["artifact_sha256s"], [SHA_D])
        self.assertEqual(lineage["provider_idempotency_support"], "unsupported")
        self.assertIn("unsupported", lineage["submission_key_limitation"])
        self.assertNotEqual(first.authorization.digest, self.authorization.digest)
        self.assertEqual(first.authorization.value["authorization_id"], "authorization-retry-001")
        self.assertEqual(first.authorization.value["plan_digest"], first.plan.digest)

    def test_effect_found_is_evidence_bound_and_excluded_from_retry(self) -> None:
        ledger = make_ledger(self.plan, self.authorization)
        ledger = submit(
            ledger,
            self.plan,
            self.authorization,
            "operation-002",
            "unknown",
            2,
        )
        ledger = reconcile_unknown(
            ledger.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            operation_id="operation-002",
            attempt_id=attempt_id(ledger, "operation-002"),
            evidence=ReconciliationEvidence(
                outcome="effect-found",
                evidence_id="reconciliation-effect-found",
                evidence_sha256=SHA_E,
                observed_at="2026-08-09T11:15:00Z",
                native_effect_ref="synthetic-effect:operation-002",
                observed_artifact_sha256s=(SHA_D,),
            ),
        )
        self.assertEqual(ledger.value["operations"][1]["state"], "effect-found")
        with self.assertRaisesRegex(RetryBlocked, "no retryable"):
            prepare_bounded_retry(
                self.plan,
                ledger.as_envelope(),
                self.authorization.as_envelope(),
                requested_operation_ids=("operation-002",),
                **retry_kwargs(),
            )

    def test_separate_duplicate_risk_authorization_is_exact_current_and_recorded(self) -> None:
        ledger = make_ledger(self.plan, self.authorization)
        ledger = submit(
            ledger,
            self.plan,
            self.authorization,
            "operation-002",
            "unknown",
            2,
        )
        bound_attempt = attempt_id(ledger, "operation-002")
        risk = build_duplicate_risk_authorization(
            ledger.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            operation_id="operation-002",
            attempt_id=bound_attempt,
            authorization_id="duplicate-risk-001",
            reviewer="fixture-owner",
            risk_statement="owner accepts a possible duplicate synthetic effect",
            authorized_at="2026-08-09T11:45:00Z",
            expires_at="2026-08-09T13:00:00Z",
        )
        recorded = record_duplicate_risk_authorization(
            ledger.as_envelope(),
            risk.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            now=NOW,
        )
        operation = recorded.value["operations"][1]
        self.assertEqual(operation["state"], "duplicate-risk-authorized")
        self.assertEqual(
            operation["duplicate_risk_authorization"]["authorization_digest"],
            risk.digest,
        )
        bundle = prepare_bounded_retry(
            self.plan,
            recorded.as_envelope(),
            self.authorization.as_envelope(),
            requested_operation_ids=("operation-002",),
            **retry_kwargs(),
        )
        basis = bundle.plan.value["retry_lineage"]["eligibility_evidence"][0]
        self.assertEqual(basis["basis"], "duplicate-effect-risk-authorized")
        self.assertEqual(basis["authorization_digest"], risk.digest)

        expired_risk = build_duplicate_risk_authorization(
            ledger.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            operation_id="operation-002",
            attempt_id=bound_attempt,
            authorization_id="duplicate-risk-expired",
            reviewer="fixture-owner",
            risk_statement="expired duplicate risk decision",
            authorized_at="2026-08-09T11:00:00Z",
            expires_at=NOW,
        )
        spy = SecretResolverSpy()
        with self.assertRaisesRegex(LifecycleContractError, "expired"):
            record_duplicate_risk_authorization(
                ledger.as_envelope(),
                expired_risk.as_envelope(),
                plan=self.plan,
                authorization=self.authorization.as_envelope(),
                now=NOW,
                secret_resolver=spy,
            )
        self.assertFalse(spy.called)

    def test_retry_count_depth_and_new_authorization_are_bounded(self) -> None:
        ledger = ledger_with_three_outcomes(self.plan, self.authorization)
        ledger = reconcile_unknown(
            ledger.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            operation_id="operation-002",
            attempt_id=attempt_id(ledger, "operation-002"),
            evidence=ReconciliationEvidence(
                outcome="no-effect",
                evidence_id="reconciliation-no-effect",
                evidence_sha256=SHA_F,
                observed_at="2026-08-09T11:30:00Z",
            ),
        )
        with self.assertRaisesRegex(RetryBlocked, "operation count"):
            prepare_bounded_retry(
                self.plan,
                ledger.as_envelope(),
                self.authorization.as_envelope(),
                requested_operation_ids=("operation-002", "operation-003"),
                **retry_kwargs(max_retry_operations=1),
            )
        with self.assertRaisesRegex(RetryBlocked, "new authorization id"):
            prepare_bounded_retry(
                self.plan,
                ledger.as_envelope(),
                self.authorization.as_envelope(),
                requested_operation_ids=("operation-003",),
                **retry_kwargs(authorization_id="authorization-001"),
            )

        first_retry = prepare_bounded_retry(
            self.plan,
            ledger.as_envelope(),
            self.authorization.as_envelope(),
            requested_operation_ids=("operation-003",),
            **retry_kwargs(max_retry_depth=2),
        )
        retry_ledger = build_operation_ledger(
            first_retry.plan.as_envelope(),
            first_retry.authorization.as_envelope(),
            run_id="synthetic-run-002",
            parent_run_id="synthetic-run-001",
            provider_idempotency_support="unsupported",
        )
        retry_operation_id = first_retry.plan.value["operations"][0]["operation_id"]
        retry_ledger = record_submission(
            retry_ledger.as_envelope(),
            plan=first_retry.plan.as_envelope(),
            authorization=first_retry.authorization.as_envelope(),
            operation_id=retry_operation_id,
            sent_payload_sha256=first_retry.plan.value["operations"][0]["projected_payload_sha256"],
            submitted_at="2026-08-09T12:10:00Z",
            observation=AttemptObservation(
                response_state="rejected-no-effect",
                evidence_id="retry-response-no-effect",
                evidence_sha256=SHA_E,
                observed_at="2026-08-09T12:10:01Z",
            ),
        )
        with self.assertRaisesRegex(RetryBlocked, "depth"):
            prepare_bounded_retry(
                first_retry.plan.as_envelope(),
                retry_ledger.as_envelope(),
                first_retry.authorization.as_envelope(),
                requested_operation_ids=(retry_operation_id,),
                **retry_kwargs(
                    authorization_id="authorization-retry-002",
                    max_retry_depth=1,
                ),
            )

    def test_supported_idempotency_preserves_submission_key_on_retry(self) -> None:
        ledger = make_ledger(self.plan, self.authorization, "supported")
        ledger = submit(
            ledger,
            self.plan,
            self.authorization,
            "operation-003",
            "rejected-no-effect",
            3,
        )
        bundle = prepare_bounded_retry(
            self.plan,
            ledger.as_envelope(),
            self.authorization.as_envelope(),
            requested_operation_ids=("operation-003",),
            **retry_kwargs(),
        )
        original_key = self.plan["value"]["operations"][2]["submission_key"]
        self.assertEqual(bundle.plan.value["operations"][0]["submission_key"], original_key)
        self.assertIsNone(bundle.plan.value["retry_lineage"]["submission_key_limitation"])

    def test_mutation_and_stale_bindings_fail_and_typed_evidence_is_frozen(self) -> None:
        ledger = make_ledger(self.plan, self.authorization)
        mutant = copy.deepcopy(ledger.as_envelope())
        mutant["value"]["provider_idempotency_support"] = "supported"
        with self.assertRaisesRegex(LifecycleContractError, "invalid"):
            validate_operation_ledger(
                mutant,
                plan=self.plan,
                authorization=self.authorization.as_envelope(),
            )
        stale_plan = copy.deepcopy(self.plan)
        stale_plan["value"]["warnings"] = ["mutated"]
        with self.assertRaises(LifecycleContractError):
            validate_operation_ledger(
                ledger.as_envelope(),
                plan=stale_plan,
                authorization=self.authorization.as_envelope(),
            )
        item = ReconciliationEvidence(
            outcome="no-effect",
            evidence_id="immutable-reconciliation",
            evidence_sha256=SHA_E,
            observed_at="2026-08-09T11:00:00Z",
        )
        with self.assertRaises(FrozenInstanceError):
            item.outcome = "effect-found"  # type: ignore[misc]

    def test_import_and_claim_surfaces_have_zero_effect_capability(self) -> None:
        tree = ast.parse(inspect.getsource(lifecycle))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module.split(".", 1)[0])
        self.assertFalse(
            imports & {"http", "requests", "socket", "subprocess", "urllib"}
        )
        source = inspect.getsource(lifecycle).casefold()
        for forbidden_claim in (
            "provider success",
            "providers are replaceable",
            "production ready",
            "live submission succeeded",
        ):
            with self.subTest(forbidden_claim=forbidden_claim):
                self.assertNotIn(forbidden_claim, source)


if __name__ == "__main__":
    unittest.main()
