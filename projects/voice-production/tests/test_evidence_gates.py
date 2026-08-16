from __future__ import annotations

import copy
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path


STAGING_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGING_ROOT))

from voice_production.contracts import plan_envelope  # noqa: E402
from voice_production.evidence import (  # noqa: E402
    REQUIRED_PREREQUISITE_KINDS,
    ArtifactRecord,
    ClaimEvidence,
    ClaimEvidenceError,
    ClaimRecord,
    CriterionResult,
    EvidenceContractError,
    GateBindingError,
    ProtectedPrerequisite,
    build_execution_authorization,
    build_gate_receipt,
    build_normalized_receipt,
    validate_gate_receipt,
    validate_normalized_receipt,
)


SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64
SHA_E = "e" * 64


def make_plan():
    return plan_envelope(
        manifest_digest=SHA_A,
        capability_profile_digest=SHA_B,
        selected_segment_ids=["segment-001"],
        operations=[
            {
                "operation_id": "operation-001",
                "operation_fingerprint": SHA_C,
                "submission_key": f"local-{SHA_C}",
                "selected_segment_ids": ["segment-001"],
                "projected_payload_sha256": SHA_C,
                "expected_output_granularity": "segment",
            }
        ],
        expected_outputs=[
            {
                "expected_output_id": "expected-output-001",
                "segment_id": "segment-001",
                "output_granularity": "segment",
            }
        ],
        effect_estimates={
            "projected_text_utf8_bytes": 64,
            "operation_count": 1,
            "external_effects": 0,
        },
        warnings=["synthetic evidence only"],
        blocked_requirements=[],
        transformations=[],
        native_schema_basis={"locator": "synthetic-schema://segment/v1", "sha256": SHA_C},
    )


def prerequisite_evidence() -> tuple[ProtectedPrerequisite, ...]:
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


def make_authorization(plan, *, account: str = "synthetic-account-A"):
    return build_execution_authorization(
        plan,
        authorization_id="authorization-001",
        account_ref=account,
        execution_scope="production/chapter-01/segment-001",
        issued_at="2026-08-09T00:00:00Z",
        expires_at="2026-09-01T00:00:00Z",
        max_effect_units=64,
        prerequisite_evidence=prerequisite_evidence(),
    )


def make_claim(
    *,
    value=True,
    evidence_link_ids: tuple[str, ...] = ("evidence-001",),
    confidence: str = "observed",
) -> ClaimRecord:
    return ClaimRecord.create(
        claim_id="claim-001",
        subject_ref="artifact-001",
        predicate="artifact-observed",
        value=value,
        evidence_link_ids=evidence_link_ids,
        confidence=confidence,
    )


def make_evidence(*, digest: str = SHA_D, claim_id: str = "claim-001") -> ClaimEvidence:
    return ClaimEvidence(
        evidence_id="evidence-001",
        claim_id=claim_id,
        claim_type="artifact-observation",
        native_locator="synthetic-observation://run-001/artifact-001",
        native_sha256=digest,
        observed_at="2026-08-09T12:00:00Z",
        classification="synthetic-placeholder",
        redaction_profile="no-secrets/v1",
    )


def make_receipt(
    plan,
    authorization,
    artifact: ArtifactRecord,
    *,
    claim: ClaimRecord | None = None,
    evidence_link: ClaimEvidence | None = None,
):
    claim_value = make_claim() if claim is None else claim
    evidence_value = make_evidence() if evidence_link is None else evidence_link
    return build_normalized_receipt(
        plan,
        authorization.as_envelope(),
        run_id="synthetic-run-001",
        output_granularity="segment",
        claims=(claim_value,),
        evidence_links=(evidence_value,),
        artifacts=(artifact,),
        reconciliation_state={"status": "known", "attempt": 1},
    )


class EvidenceGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = make_plan()
        self.authorization = make_authorization(self.plan)
        self.artifact = ArtifactRecord.from_bytes(
            artifact_id="artifact-001",
            content=b"synthetic artifact bytes v1",
            classification="synthetic-placeholder",
            materialized=False,
        )
        self.claim = make_claim()
        self.evidence_link = make_evidence()
        self.receipt = make_receipt(
            self.plan,
            self.authorization,
            self.artifact,
            claim=self.claim,
            evidence_link=self.evidence_link,
        )
        self.criterion = CriterionResult(
            criterion_id="artifact-evidence-is-bound",
            passed=True,
            observed_result="exact digest and typed observation agree",
            evidence_link_ids=("evidence-001",),
        )
        self.gate = build_gate_receipt(
            self.receipt.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            reviewed_artifacts=(self.artifact,),
            criteria_results=(self.criterion,),
            review_scope="synthetic-evidence-gate",
            reviewer="fixture-reviewer",
            decision="accepted",
            decided_at="2026-08-09T12:01:00Z",
            exceptions=({"kind": "no-live-provider-proof", "accepted": False},),
        )

    def test_fixed_inputs_are_byte_stable_and_gate_binding_passes(self) -> None:
        second_receipt = make_receipt(
            self.plan,
            self.authorization,
            self.artifact,
            claim=self.claim,
            evidence_link=self.evidence_link,
        )
        second_gate = build_gate_receipt(
            second_receipt.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            reviewed_artifacts=(self.artifact,),
            criteria_results=(self.criterion,),
            review_scope="synthetic-evidence-gate",
            reviewer="fixture-reviewer",
            decision="accepted",
            decided_at="2026-08-09T12:01:00Z",
            exceptions=({"kind": "no-live-provider-proof", "accepted": False},),
        )
        self.assertEqual(
            self.receipt.canonical_envelope_bytes,
            second_receipt.canonical_envelope_bytes,
        )
        self.assertEqual(self.gate.canonical_envelope_bytes, second_gate.canonical_envelope_bytes)
        validate_gate_receipt(
            self.gate.as_envelope(),
            receipt=self.receipt.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
            reviewed_artifacts=(self.artifact,),
            criteria_results=(self.criterion,),
        )

    def test_receipt_retains_exact_execution_authorization_digest(self) -> None:
        value = self.receipt.value
        self.assertEqual(
            value["execution_authorization_digest"], self.authorization.digest
        )
        self.assertEqual(value["plan_digest"], self.plan["digest"])
        validate_normalized_receipt(
            self.receipt.as_envelope(),
            plan=self.plan,
            authorization=self.authorization.as_envelope(),
        )

    def test_every_non_unknown_claim_requires_resolved_typed_evidence(self) -> None:
        observed_without_evidence = make_claim(evidence_link_ids=())
        with self.assertRaisesRegex(ClaimEvidenceError, "must have typed evidence"):
            build_normalized_receipt(
                self.plan,
                self.authorization.as_envelope(),
                run_id="synthetic-run-missing-evidence",
                output_granularity="segment",
                claims=(observed_without_evidence,),
                evidence_links=(),
                artifacts=(self.artifact,),
                reconciliation_state={"status": "known"},
            )

        missing_reference = make_claim(evidence_link_ids=("evidence-999",))
        with self.assertRaisesRegex(ClaimEvidenceError, "missing evidence"):
            build_normalized_receipt(
                self.plan,
                self.authorization.as_envelope(),
                run_id="synthetic-run-bad-reference",
                output_granularity="segment",
                claims=(missing_reference,),
                evidence_links=(self.evidence_link,),
                artifacts=(self.artifact,),
                reconciliation_state={"status": "known"},
            )

    def test_unknown_claim_may_remain_explicitly_evidenceless(self) -> None:
        unknown = make_claim(
            value=None,
            evidence_link_ids=(),
            confidence="unknown",
        )
        receipt = build_normalized_receipt(
            self.plan,
            self.authorization.as_envelope(),
            run_id="synthetic-run-unknown",
            output_granularity="segment",
            claims=(unknown,),
            evidence_links=(),
            artifacts=(self.artifact,),
            reconciliation_state={"status": "unknown"},
        )
        self.assertEqual(receipt.value["claims"][0]["confidence"], "unknown")
        self.assertEqual(receipt.value["claims"][0]["evidence_link_ids"], [])

    def test_cross_claim_or_orphan_evidence_is_rejected(self) -> None:
        wrong_claim_evidence = make_evidence(claim_id="claim-999")
        with self.assertRaisesRegex(ClaimEvidenceError, "unknown claim"):
            make_receipt(
                self.plan,
                self.authorization,
                self.artifact,
                evidence_link=wrong_claim_evidence,
            )

        unknown = make_claim(value=None, evidence_link_ids=(), confidence="unknown")
        with self.assertRaisesRegex(ClaimEvidenceError, "unreferenced"):
            build_normalized_receipt(
                self.plan,
                self.authorization.as_envelope(),
                run_id="synthetic-run-orphan",
                output_granularity="segment",
                claims=(unknown,),
                evidence_links=(self.evidence_link,),
                artifacts=(self.artifact,),
                reconciliation_state={"status": "unknown"},
            )

    def test_artifact_evidence_criteria_and_authorization_mutations_break_gate(self) -> None:
        changed_artifact = ArtifactRecord.from_bytes(
            artifact_id="artifact-001",
            content=b"synthetic artifact bytes v2",
            classification="synthetic-placeholder",
            materialized=False,
        )
        changed_criterion = CriterionResult(
            criterion_id=self.criterion.criterion_id,
            passed=False,
            observed_result="digest mismatch observed",
            evidence_link_ids=("evidence-001",),
        )
        changed_authorization = make_authorization(
            self.plan, account="synthetic-account-B"
        )
        changed_receipt = make_receipt(
            self.plan,
            self.authorization,
            self.artifact,
            claim=self.claim,
            evidence_link=make_evidence(digest=SHA_E),
        )
        cases = {
            "artifact": {
                "receipt": self.receipt,
                "authorization": self.authorization,
                "artifacts": (changed_artifact,),
                "criteria": (self.criterion,),
                "message": "artifact",
            },
            "evidence": {
                "receipt": changed_receipt,
                "authorization": self.authorization,
                "artifacts": (self.artifact,),
                "criteria": (self.criterion,),
                "message": "synthesis receipt",
            },
            "criteria": {
                "receipt": self.receipt,
                "authorization": self.authorization,
                "artifacts": (self.artifact,),
                "criteria": (changed_criterion,),
                "message": "criteria",
            },
            "authorization": {
                "receipt": self.receipt,
                "authorization": changed_authorization,
                "artifacts": (self.artifact,),
                "criteria": (self.criterion,),
                "message": "execution_authorization_digest",
            },
        }
        for name, values in cases.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(EvidenceContractError, values["message"]):
                    validate_gate_receipt(
                        self.gate.as_envelope(),
                        receipt=values["receipt"].as_envelope(),
                        plan=self.plan,
                        authorization=values["authorization"].as_envelope(),
                        reviewed_artifacts=values["artifacts"],
                        criteria_results=values["criteria"],
                    )

    def test_noncanonical_receipt_or_gate_mutation_fails_closed(self) -> None:
        receipt_mutant = copy.deepcopy(self.receipt.as_envelope())
        receipt_mutant["value"]["run_id"] = "mutated-run"
        with self.assertRaises(EvidenceContractError):
            validate_normalized_receipt(
                receipt_mutant,
                plan=self.plan,
                authorization=self.authorization.as_envelope(),
            )

        gate_mutant = copy.deepcopy(self.gate.as_envelope())
        gate_mutant["value"]["reviewer"] = "mutated-reviewer"
        with self.assertRaises(EvidenceContractError):
            validate_gate_receipt(
                gate_mutant,
                receipt=self.receipt.as_envelope(),
                plan=self.plan,
                authorization=self.authorization.as_envelope(),
                reviewed_artifacts=(self.artifact,),
                criteria_results=(self.criterion,),
            )

    def test_gate_rejects_artifact_not_present_in_normalized_receipt(self) -> None:
        other = ArtifactRecord.from_bytes(
            artifact_id="artifact-002",
            content=b"unreviewed artifact",
            classification="synthetic-placeholder",
            materialized=False,
        )
        with self.assertRaisesRegex(GateBindingError, "absent from receipt"):
            build_gate_receipt(
                self.receipt.as_envelope(),
                plan=self.plan,
                authorization=self.authorization.as_envelope(),
                reviewed_artifacts=(other,),
                criteria_results=(self.criterion,),
                review_scope="synthetic-evidence-gate",
                reviewer="fixture-reviewer",
                decision="accepted",
                decided_at="2026-08-09T12:01:00Z",
            )

    def test_typed_values_are_frozen_and_detached_from_mutable_inputs(self) -> None:
        value = {"nested": ["original"]}
        claim = ClaimRecord.create(
            claim_id="claim-detached",
            subject_ref="artifact-001",
            predicate="metadata",
            value=value,
            evidence_link_ids=(),
            confidence="unknown",
        )
        value["nested"][0] = "mutated"
        self.assertEqual(claim.value, {"nested": ["original"]})
        with self.assertRaises(FrozenInstanceError):
            self.evidence_link.classification = "mutated"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
