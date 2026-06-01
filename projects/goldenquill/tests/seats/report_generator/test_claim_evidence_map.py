"""Tests for ``pipeline.orchestrator.seats.report_generator.claim_evidence_map``.

Per §14.5.1 Cycle 1 + Cycle 2 closures (RT-1a/1b/1c + RT-6c + RT-7b + RT-8b/8c
+ RT-C2-08/09/10). Assembly + canonical-byte stability + Ed25519 signer
envelope.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from pipeline.orchestrator.seats.report_generator._schemas import (
    CLAIM_EVIDENCE_MAP_VERSION_V0_2,
    OPERATOR_SIG_STATUS_PENDING,
    OPERATOR_SIG_STATUS_SIGNED,
    ClaimEntry,
    SourceRef,
)
from pipeline.orchestrator.seats.report_generator.claim_evidence_map import (
    ClaimEvidenceMapAssemblyError,
    SCHEMA_VERSION_V1,
    SignClaimEvidenceMapResult,
    VerifyClaimEvidenceMapResult,
    assemble_claim_evidence_map,
    canonical_map_bytes,
    compute_map_content_hash,
    sign_claim_evidence_map,
    signing_payload_bytes,
    verify_claim_evidence_map_signature,
)


def _make_simple_source() -> SourceRef:
    return SourceRef(
        kind="operational_data",
        sub_kind="metrics",
        source_path="orgs/myorg/vault/operational/grants/G1/period_1/metrics/x.yaml",
        source_row_id="r1",
        source_content_sha3_512="a" * 128,
        source_value=Decimal("50"),
    )


def _make_simple_claim() -> ClaimEntry:
    return ClaimEntry(
        claim_id="CLAIM-001",
        sub_section="metrics_table",
        claim_text="50 workshops delivered",
        claim_kind="numeric",
        sources=(_make_simple_source(),),
    )


def _assemble_simple():
    return assemble_claim_evidence_map(
        run_id="RUN-1",
        org_slug="myorg",
        grant_id="G1",
        period_n=1,
        draft_path="orgs/myorg/vault/grants/G1/reports/period_1/draft_1.md",
        draft_version=1,
        draft_content_sha3_512="f" * 128,
        authored_at_utc="2026-05-11T00:00:00Z",
        authored_by_seat="scribe",
        claims=(_make_simple_claim(),),
    )


class TestAssembly:
    def test_happy_path_pending_state(self):
        m = _assemble_simple()
        assert m.operator_signature_status == OPERATOR_SIG_STATUS_PENDING
        assert m.operator_signature == ""
        assert m.operator_signed_at_utc == ""
        assert m.schema_version == SCHEMA_VERSION_V1
        assert m.claim_evidence_map_version == CLAIM_EVIDENCE_MAP_VERSION_V0_2

    def test_empty_claims_raises(self):
        with pytest.raises(ClaimEvidenceMapAssemblyError):
            assemble_claim_evidence_map(
                run_id="r", org_slug="o", grant_id="g", period_n=1,
                draft_path="d", draft_version=1, draft_content_sha3_512="a" * 128,
                authored_at_utc="now", authored_by_seat="scribe",
                claims=(),
            )

    def test_duplicate_claim_id_raises(self):
        c1 = _make_simple_claim()
        c2 = ClaimEntry(
            claim_id="CLAIM-001",  # duplicate
            sub_section="narrative",
            claim_text="X",
            claim_kind="narrative",
            sources=(SourceRef(
                kind="operational_data", sub_kind="narrative_entries",
                source_path="p", source_row_id="r2",
                source_content_sha3_512="b" * 128,
            ),),
        )
        with pytest.raises(ClaimEvidenceMapAssemblyError):
            assemble_claim_evidence_map(
                run_id="r", org_slug="o", grant_id="g", period_n=1,
                draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
                authored_at_utc="now", authored_by_seat="scribe",
                claims=(c1, c2),
            )

    def test_malformed_draft_hash_raises(self):
        with pytest.raises(ClaimEvidenceMapAssemblyError):
            assemble_claim_evidence_map(
                run_id="r", org_slug="o", grant_id="g", period_n=1,
                draft_path="d", draft_version=1, draft_content_sha3_512="not-hex",
                authored_at_utc="now", authored_by_seat="scribe",
                claims=(_make_simple_claim(),),
            )

    def test_invalid_period_n_raises(self):
        with pytest.raises(ClaimEvidenceMapAssemblyError):
            assemble_claim_evidence_map(
                run_id="r", org_slug="o", grant_id="g", period_n=0,
                draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
                authored_at_utc="now", authored_by_seat="scribe",
                claims=(_make_simple_claim(),),
            )

    def test_pending_commitment_source_status_raises(self):
        with pytest.raises(ValueError, match="PROMOTED"):
            # ValueError raised at SourceRef construction time
            # (proposal_commitments source rejects non-PROMOTED status).
            SourceRef(
                kind="proposal_commitments",
                commitment_id="COMMIT-001",
                commitment_status="PENDING_OPERATOR_REVIEW",
                scope_tags_at_commitment=("a",),
            )

    def test_claims_sorted_by_id(self):
        c2 = ClaimEntry(
            claim_id="CLAIM-002",
            sub_section="narrative",
            claim_text="X",
            claim_kind="narrative",
            sources=(SourceRef(
                kind="operational_data", sub_kind="narrative_entries",
                source_path="p", source_row_id="r2",
                source_content_sha3_512="b" * 128,
            ),),
        )
        c1 = _make_simple_claim()
        m = assemble_claim_evidence_map(
            run_id="r", org_slug="o", grant_id="g", period_n=1,
            draft_path="d", draft_version=1, draft_content_sha3_512="f" * 128,
            authored_at_utc="now", authored_by_seat="scribe",
            claims=(c2, c1),
        )
        assert tuple(c.claim_id for c in m.claims) == ("CLAIM-001", "CLAIM-002")


class TestCanonicalBytes:
    def test_deterministic_across_construction_order(self):
        m1 = _assemble_simple()
        m2 = _assemble_simple()
        assert canonical_map_bytes(m1) == canonical_map_bytes(m2)

    def test_content_hash_128_lowercase_hex(self):
        m = _assemble_simple()
        h = compute_map_content_hash(m)
        assert len(h) == 128
        assert all(c in "0123456789abcdef" for c in h)

    def test_signing_payload_excludes_signature_fields(self):
        m = _assemble_simple()
        payload = signing_payload_bytes(m)
        assert b"operator_signature" not in payload[:200] or b'"operator_signature_status"' in payload
        # The "operator_signature" key is excluded; "operator_signature_status" is rewritten to PENDING.
        # Strict check — signature value and timestamp are excluded entirely.
        assert b'"operator_signature":' not in payload
        assert b'"operator_signed_at_utc":' not in payload


class TestSignAndVerify:
    def test_sign_pending_returns_signed(self):
        m = _assemble_simple()
        signer = lambda payload: b"S" * 64
        r = sign_claim_evidence_map(
            m, signer=signer, operator_signed_at_utc="2026-05-11T01:00:00Z"
        )
        assert r.success
        assert r.signed_map is not None
        assert r.signed_map.operator_signature_status == OPERATOR_SIG_STATUS_SIGNED
        assert r.signed_map.operator_signature == ("53" * 64)  # "S" * 64 hex
        assert r.signed_map.operator_signed_at_utc == "2026-05-11T01:00:00Z"

    def test_sign_refuses_resign_signed_map(self):
        m = _assemble_simple()
        signer = lambda payload: b"S" * 64
        r = sign_claim_evidence_map(m, signer=signer, operator_signed_at_utc="t1")
        assert r.success
        # Re-sign refused
        r2 = sign_claim_evidence_map(
            r.signed_map, signer=signer, operator_signed_at_utc="t2"
        )
        assert not r2.success
        assert "refuse-resign" in r2.detail

    def test_sign_with_failing_signer_returns_failure(self):
        m = _assemble_simple()
        def bad_signer(payload):
            raise RuntimeError("hardware key unplugged")
        r = sign_claim_evidence_map(m, signer=bad_signer, operator_signed_at_utc="t")
        assert not r.success
        assert "RuntimeError" in r.detail

    def test_sign_with_non_bytes_return_fails(self):
        m = _assemble_simple()
        r = sign_claim_evidence_map(
            m, signer=lambda payload: "not bytes", operator_signed_at_utc="t"
        )
        assert not r.success
        assert "expected bytes" in r.detail

    def test_verify_signed_map_with_True_verifier_passes(self):
        m = _assemble_simple()
        r = sign_claim_evidence_map(m, signer=lambda p: b"S"*64, operator_signed_at_utc="t")
        v = verify_claim_evidence_map_signature(
            r.signed_map, verifier=lambda payload, sig, pk: True,
            operator_public_key=b"PUB",
        )
        assert v.success
        assert v.signing_payload_sha3_512

    def test_verify_signed_map_with_False_verifier_fails(self):
        m = _assemble_simple()
        r = sign_claim_evidence_map(m, signer=lambda p: b"S"*64, operator_signed_at_utc="t")
        v = verify_claim_evidence_map_signature(
            r.signed_map, verifier=lambda payload, sig, pk: False,
            operator_public_key=b"PUB",
        )
        assert not v.success

    def test_verify_pending_map_fails(self):
        m = _assemble_simple()
        v = verify_claim_evidence_map_signature(
            m, verifier=lambda payload, sig, pk: True, operator_public_key=b"PUB",
        )
        assert not v.success
        assert "expected SIGNED" in v.detail

    def test_verify_with_truthy_non_True_fails_strict_identity(self):
        m = _assemble_simple()
        r = sign_claim_evidence_map(m, signer=lambda p: b"S"*64, operator_signed_at_utc="t")
        v = verify_claim_evidence_map_signature(
            r.signed_map, verifier=lambda payload, sig, pk: 1,  # truthy not True
            operator_public_key=b"PUB",
        )
        assert not v.success
        assert "strict identity" in v.detail

    def test_signing_payload_byte_stable_across_sign_verify(self):
        m = _assemble_simple()
        pre_payload = signing_payload_bytes(m)
        r = sign_claim_evidence_map(m, signer=lambda p: b"S"*64, operator_signed_at_utc="t")
        post_payload = signing_payload_bytes(r.signed_map)
        assert pre_payload == post_payload

    def test_verifier_exception_fails_closed(self):
        m = _assemble_simple()
        r = sign_claim_evidence_map(m, signer=lambda p: b"S"*64, operator_signed_at_utc="t")
        def bad(payload, sig, pk):
            raise ValueError("public key malformed")
        v = verify_claim_evidence_map_signature(
            r.signed_map, verifier=bad, operator_public_key=b"PUB",
        )
        assert not v.success
        assert "ValueError" in v.detail
