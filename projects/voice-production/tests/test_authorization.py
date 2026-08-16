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

from voice_production import evidence  # noqa: E402
from voice_production.contracts import plan_envelope  # noqa: E402
from voice_production.evidence import (  # noqa: E402
    REQUIRED_PREREQUISITE_KINDS,
    AuthorizationRejected,
    ProtectedPrerequisite,
    build_execution_authorization,
    validate_execution_authorization,
)


SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
NOW = "2026-08-09T12:00:00Z"
ACCOUNT = "synthetic-account-A"
SCOPE = "production/chapter-01/segments-001-003"


class SecretResolverSpy:
    def __init__(self) -> None:
        self.called = False

    def __call__(self, *_args, **_kwargs):
        self.called = True
        raise AssertionError("secret resolver crossed the protected boundary")


def make_plan(effect_units: int = 120, warning: str = "synthetic-only"):
    return plan_envelope(
        manifest_digest=SHA_A,
        capability_profile_digest=SHA_B,
        selected_segment_ids=["segment-001", "segment-002", "segment-003"],
        operations=[
            {
                "operation_id": "operation-001",
                "operation_fingerprint": SHA_C,
                "submission_key": f"local-{SHA_C}",
                "selected_segment_ids": [
                    "segment-001",
                    "segment-002",
                    "segment-003",
                ],
                "projected_payload_sha256": SHA_C,
                "expected_output_granularity": "composite",
                "composite_group_id": "group-001",
            }
        ],
        expected_outputs=[
            {
                "expected_output_id": "expected-composite-001",
                "output_granularity": "composite",
                "segment_ids": ["segment-001", "segment-002", "segment-003"],
            }
        ],
        effect_estimates={
            "projected_text_utf8_bytes": effect_units,
            "operation_count": 1,
            "external_effects": 0,
        },
        warnings=[warning],
        blocked_requirements=[],
        transformations=[],
        native_schema_basis={"locator": "synthetic-schema://project/v1", "sha256": SHA_C},
    )


def prerequisites(
    *,
    omit: str | None = None,
    rejected: str | None = None,
    expired: str | None = None,
) -> tuple[ProtectedPrerequisite, ...]:
    return tuple(
        ProtectedPrerequisite(
            kind=kind,
            evidence_id=f"evidence-{index:03d}",
            evidence_sha256=f"{index:x}" * 64,
            accepted=kind != rejected,
            expires_at=(
                "2026-08-09T11:59:59Z"
                if kind == expired
                else "2026-09-01T00:00:00Z"
            ),
        )
        for index, kind in enumerate(sorted(REQUIRED_PREREQUISITE_KINDS), start=1)
        if kind != omit
    )


def make_authorization(
    plan=None,
    *,
    account: str = ACCOUNT,
    scope: str = SCOPE,
    expires_at: str = "2026-09-01T00:00:00Z",
    budget: int = 120,
    prerequisite_values: tuple[ProtectedPrerequisite, ...] | None = None,
):
    return build_execution_authorization(
        plan or make_plan(),
        authorization_id="authorization-001",
        account_ref=account,
        execution_scope=scope,
        issued_at="2026-08-09T00:00:00Z",
        expires_at=expires_at,
        max_effect_units=budget,
        prerequisite_evidence=(
            prerequisites() if prerequisite_values is None else prerequisite_values
        ),
    )


class AuthorizationTests(unittest.TestCase):
    def test_valid_authorization_is_exact_deterministic_and_stops_before_secret(self) -> None:
        plan = make_plan()
        first = make_authorization(plan)
        second = make_authorization(plan)
        spy = SecretResolverSpy()
        grant = validate_execution_authorization(
            plan,
            first.as_envelope(),
            expected_account_ref=ACCOUNT,
            expected_scope=SCOPE,
            now=NOW,
            secret_resolver=spy,
        )
        self.assertEqual(
            first.canonical_envelope_bytes, second.canonical_envelope_bytes
        )
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(grant.authorization_digest, first.digest)
        self.assertEqual(grant.plan_digest, plan["digest"])
        self.assertEqual(grant.planned_effect_units, 120)
        self.assertEqual(grant.budget_limit, 120)
        self.assertFalse(spy.called)

    def test_six_required_rejections_happen_before_secret_resolution(self) -> None:
        plan = make_plan()
        base = make_authorization(plan)
        stale_plan = make_plan(warning="different-effect-warning")
        cases = {
            "missing": (plan, None, ACCOUNT, SCOPE, NOW, "missing"),
            "expired": (
                plan,
                make_authorization(plan, expires_at="2026-08-09T12:00:00Z"),
                ACCOUNT,
                SCOPE,
                NOW,
                "expired",
            ),
            "over-budget": (
                plan,
                make_authorization(plan, budget=119),
                ACCOUNT,
                SCOPE,
                NOW,
                "budget exceeded",
            ),
            "wrong-account": (
                plan,
                base,
                "synthetic-account-B",
                SCOPE,
                NOW,
                "account binding",
            ),
            "wrong-scope": (
                plan,
                base,
                ACCOUNT,
                "production/chapter-02",
                NOW,
                "scope binding",
            ),
            "stale-plan": (
                stale_plan,
                base,
                ACCOUNT,
                SCOPE,
                NOW,
                "stale",
            ),
        }
        denied = AssertionError("network helper must not be used")
        for name, (current_plan, current_auth, account, scope, now, message) in cases.items():
            spy = SecretResolverSpy()
            authorization = (
                current_auth.as_envelope()
                if current_auth is not None and hasattr(current_auth, "as_envelope")
                else current_auth
            )
            with self.subTest(name=name):
                with (
                    mock.patch.object(socket, "socket", side_effect=denied),
                    mock.patch.object(socket, "create_connection", side_effect=denied),
                    mock.patch.object(socket, "getaddrinfo", side_effect=denied),
                    self.assertRaisesRegex(AuthorizationRejected, message),
                ):
                    validate_execution_authorization(
                        current_plan,
                        authorization,
                        expected_account_ref=account,
                        expected_scope=scope,
                        now=now,
                        secret_resolver=spy,
                    )
                self.assertFalse(spy.called)

    def test_missing_rejected_and_expired_protected_evidence_fail_closed(self) -> None:
        plan = make_plan()
        first_kind = sorted(REQUIRED_PREREQUISITE_KINDS)[0]
        cases = {
            "missing": (prerequisites(omit=first_kind), "set mismatch"),
            "rejected": (prerequisites(rejected=first_kind), "not accepted"),
            "expired": (prerequisites(expired=first_kind), "evidence is expired"),
        }
        for name, (prerequisite_values, message) in cases.items():
            spy = SecretResolverSpy()
            authorization = make_authorization(
                plan, prerequisite_values=prerequisite_values
            )
            with self.subTest(name=name):
                with self.assertRaisesRegex(AuthorizationRejected, message):
                    validate_execution_authorization(
                        plan,
                        authorization.as_envelope(),
                        expected_account_ref=ACCOUNT,
                        expected_scope=SCOPE,
                        now=NOW,
                        secret_resolver=spy,
                    )
                self.assertFalse(spy.called)

    def test_plan_mutation_invalidates_authorization_before_secret(self) -> None:
        plan = make_plan()
        authorization = make_authorization(plan)
        mutant = copy.deepcopy(plan)
        mutant["value"]["effect_estimates"]["projected_text_utf8_bytes"] = 121
        spy = SecretResolverSpy()
        with self.assertRaisesRegex(evidence.EvidenceContractError, "invalid"):
            validate_execution_authorization(
                mutant,
                authorization.as_envelope(),
                expected_account_ref=ACCOUNT,
                expected_scope=SCOPE,
                now=NOW,
                secret_resolver=spy,
            )
        self.assertFalse(spy.called)

    def test_authorization_and_prerequisite_values_are_immutable_and_digest_bound(self) -> None:
        plan = make_plan()
        base = make_authorization(plan)
        changed = make_authorization(plan, account="synthetic-account-B")
        self.assertNotEqual(base.digest, changed.digest)
        item = prerequisites()[0]
        with self.assertRaises(FrozenInstanceError):
            item.accepted = False  # type: ignore[misc]

    def test_import_surface_has_no_effectful_runtime_modules(self) -> None:
        tree = ast.parse(inspect.getsource(evidence))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module.split(".", 1)[0])
        self.assertFalse(
            imports & {"http", "requests", "socket", "subprocess", "urllib"}
        )


if __name__ == "__main__":
    unittest.main()
