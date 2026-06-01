"""Tests for pipeline.logician.claim_evidence and pipeline.logician.post_gate.

§4.4 + §4.5 — POST-gate skeleton + claim-evidence-map BT7 discipline. Round 2
delivers the data-structure floor (frozen ClaimEntry / SourceRef /
ClaimEvidenceMap / SignedClaimEvidenceMap), the canonical-JSON-byte-identical
assembler (§7.5), and a POST-gate skeleton that composes the M8 admin-risk
verifier with the F-POST-10 / F-POST-11 hard-block predicates. The full BT10
grep-windowed verifier lands in Round 3; S11c lock-verify in Round 5; the gate
runner capstone in Round 6.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest

from pipeline.logician.claim_evidence import (
    GENERATOR_VERSION,
    SOURCE_KINDS,
    TAGS,
    VERIFY_METHODS,
    ClaimEntry,
    ClaimEvidenceMap,
    SignedClaimEvidenceMap,
    SourceRef,
    assemble_claim_evidence_map,
    canonical_map_bytes,
    compute_claim_id,
    compute_content_hash,
    compute_map_id,
    verify_canonical_idempotent,
)
from pipeline.logician.post_gate import (
    F_POST_10,
    F_POST_11,
    PostGateResult,
    PostGateSkeletonFailed,
    run_post_gate_skeleton,
)


_DRAFT_HASH = "a" * 128
_RFA_HASH = "b" * 128
_SESSION_ID = "01HZ9V0TEST00000000000000000"
_ORG_SLUG = "fit_farms_llc"
_RFA_URL_HASH = "c" * 128


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _src(path: str = "/m12/rfa.md") -> SourceRef:
    return SourceRef(
        source_kind="RFA",
        canonical_path=path,
        inode=12345,
        content_hash="d" * 128,
        grep_string="the quoted ±2 sentences from the RFA",
        window_size_sentences=2,
    )


def _doc_claim(text: str = "Eligible applicants include 501c3 entities.") -> ClaimEntry:
    return ClaimEntry(
        claim_id=compute_claim_id(
            draft_hash=_DRAFT_HASH, draft_offset=0, claim_text=text
        ),
        draft_offset=0,
        claim_text=text,
        tag="DOC_SOURCED",
        source_ref=_src(),
        verify_method="grep_windowed_pm2",
        verify_result="PASS",
        verify_detail="matched ±2 sentence window",
        rigor_breach_flag=False,
    )


def _unsourced_claim(text: str = "Soil microbe richness rose 47%.") -> ClaimEntry:
    return ClaimEntry(
        claim_id=compute_claim_id(
            draft_hash=_DRAFT_HASH, draft_offset=400, claim_text=text
        ),
        draft_offset=400,
        claim_text=text,
        tag="UNSOURCED",
        source_ref=None,
        verify_method="unresolved",
        verify_result="FAIL",
        verify_detail="grep window ±2 + ±5 fallback both failed",
        rigor_breach_flag=False,
    )


def _user_data_claim(text: str = "Operator stated FIT Farms has 12 acres.") -> ClaimEntry:
    return ClaimEntry(
        claim_id=compute_claim_id(
            draft_hash=_DRAFT_HASH, draft_offset=120, claim_text=text
        ),
        draft_offset=120,
        claim_text=text,
        tag="USER_DATA",
        source_ref=SourceRef(
            source_kind="CONVERSATION_LOG",
            canonical_path="/orgs/fit/vault/conversation/log.jsonl",
            inode=22222,
            content_hash="e" * 128,
            grep_string=None,
            window_size_sentences=None,
        ),
        verify_method="conversation_anchor",
        verify_result="PASS",
        verify_detail="anchored to log entry hash",
        rigor_breach_flag=False,
    )


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_tags_set(self) -> None:
        assert TAGS == frozenset({"DOC_SOURCED", "USER_DATA", "UNSOURCED"})

    def test_source_kinds_set(self) -> None:
        assert "RFA" in SOURCE_KINDS
        assert "PROJECT_CONTEXT" in SOURCE_KINDS
        assert "CONVERSATION_LOG" in SOURCE_KINDS

    def test_verify_methods_set(self) -> None:
        assert "grep_windowed_pm2" in VERIFY_METHODS
        assert "grep_windowed_pm5_fallback" in VERIFY_METHODS
        assert "conversation_anchor" in VERIFY_METHODS
        assert "unresolved" in VERIFY_METHODS

    def test_generator_version_pinned(self) -> None:
        assert GENERATOR_VERSION == "s4-v1"


# ---------------------------------------------------------------------------
# Dataclass shape
# ---------------------------------------------------------------------------


class TestSourceRefShape:
    def test_frozen(self) -> None:
        s = _src()
        with pytest.raises(dataclasses.FrozenInstanceError):
            s.inode = 999  # type: ignore[misc]

    def test_kw_only(self) -> None:
        with pytest.raises(TypeError):
            SourceRef("RFA", "/x", 1, "h", None, None)  # type: ignore[misc]


class TestClaimEntryShape:
    def test_frozen(self) -> None:
        c = _doc_claim()
        with pytest.raises(dataclasses.FrozenInstanceError):
            c.tag = "UNSOURCED"  # type: ignore[misc]

    def test_kw_only(self) -> None:
        with pytest.raises(TypeError):
            ClaimEntry("id", 0, "t", "DOC_SOURCED", None, "m", "PASS", "d", False)  # type: ignore[misc]


class TestClaimEvidenceMapShape:
    def test_frozen(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            m.unsourced_count = 99  # type: ignore[misc]


# ---------------------------------------------------------------------------
# compute_claim_id / compute_map_id
# ---------------------------------------------------------------------------


class TestComputeClaimId:
    def test_deterministic(self) -> None:
        a = compute_claim_id(draft_hash=_DRAFT_HASH, draft_offset=0, claim_text="x")
        b = compute_claim_id(draft_hash=_DRAFT_HASH, draft_offset=0, claim_text="x")
        assert a == b
        assert len(a) == 24

    def test_offset_changes_id(self) -> None:
        a = compute_claim_id(draft_hash=_DRAFT_HASH, draft_offset=0, claim_text="x")
        b = compute_claim_id(draft_hash=_DRAFT_HASH, draft_offset=1, claim_text="x")
        assert a != b


class TestComputeMapId:
    def test_deterministic(self) -> None:
        a = compute_map_id(draft_hash=_DRAFT_HASH, rfa_hash=_RFA_HASH, session_id=_SESSION_ID)
        b = compute_map_id(draft_hash=_DRAFT_HASH, rfa_hash=_RFA_HASH, session_id=_SESSION_ID)
        assert a == b
        assert len(a) == 24


# ---------------------------------------------------------------------------
# Assembler — counts derived correctly
# ---------------------------------------------------------------------------


class TestAssembler:
    def test_counts_unsourced(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(), _unsourced_claim(), _user_data_claim()),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert m.unsourced_count == 1
        assert m.hard_block_count == 0  # admin-risk hard-block lives elsewhere; default 0
        assert len(m.entries) == 3

    def test_entries_sorted_by_claim_id(self) -> None:
        # Pass entries in arbitrary order; assembler must sort by claim_id ascending
        # so canonical-bytes are deterministic regardless of input order.
        c1 = _doc_claim("alpha claim")
        c2 = _doc_claim("beta claim")
        c3 = _doc_claim("gamma claim")
        m_a = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(c1, c2, c3),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        m_b = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(c3, c1, c2),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert m_a.entries == m_b.entries
        ids = [e.claim_id for e in m_a.entries]
        assert ids == sorted(ids)

    def test_rigor_breach_propagated(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=True,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert m.rigor_breach_active is True

    def test_hard_block_count_param(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
            hard_block_count=3,
        )
        assert m.hard_block_count == 3

    def test_map_id_deterministic_in_assembler(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert m.map_id == compute_map_id(
            draft_hash=_DRAFT_HASH, rfa_hash=_RFA_HASH, session_id=_SESSION_ID
        )

    def test_generator_version_recorded(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert m.generator_version == GENERATOR_VERSION

    def test_unsourced_must_have_no_source_ref(self) -> None:
        bad = ClaimEntry(
            claim_id=compute_claim_id(
                draft_hash=_DRAFT_HASH, draft_offset=0, claim_text="x"
            ),
            draft_offset=0,
            claim_text="x",
            tag="UNSOURCED",
            source_ref=_src(),  # forbidden
            verify_method="unresolved",
            verify_result="FAIL",
            verify_detail="d",
            rigor_breach_flag=False,
        )
        with pytest.raises(ValueError):
            assemble_claim_evidence_map(
                draft_hash=_DRAFT_HASH,
                rfa_hash=_RFA_HASH,
                session_id=_SESSION_ID,
                org_slug=_ORG_SLUG,
                rfa_url_hash=_RFA_URL_HASH,
                claims=(bad,),
                rigor_breach_active=False,
                generated_at_utc="2026-04-19T00:00:00.000000Z",
            )

    def test_doc_sourced_must_have_source_ref(self) -> None:
        bad = ClaimEntry(
            claim_id=compute_claim_id(
                draft_hash=_DRAFT_HASH, draft_offset=0, claim_text="x"
            ),
            draft_offset=0,
            claim_text="x",
            tag="DOC_SOURCED",
            source_ref=None,  # forbidden
            verify_method="grep_windowed_pm2",
            verify_result="PASS",
            verify_detail="d",
            rigor_breach_flag=False,
        )
        with pytest.raises(ValueError):
            assemble_claim_evidence_map(
                draft_hash=_DRAFT_HASH,
                rfa_hash=_RFA_HASH,
                session_id=_SESSION_ID,
                org_slug=_ORG_SLUG,
                rfa_url_hash=_RFA_URL_HASH,
                claims=(bad,),
                rigor_breach_active=False,
                generated_at_utc="2026-04-19T00:00:00.000000Z",
            )

    def test_invalid_tag_rejected(self) -> None:
        # Construction of a ClaimEntry with an invalid tag passes (just a str
        # field), but the assembler must reject the map.
        bad = ClaimEntry(
            claim_id=compute_claim_id(
                draft_hash=_DRAFT_HASH, draft_offset=0, claim_text="x"
            ),
            draft_offset=0,
            claim_text="x",
            tag="BANANA",  # invalid
            source_ref=_src(),
            verify_method="grep_windowed_pm2",
            verify_result="PASS",
            verify_detail="d",
            rigor_breach_flag=False,
        )
        with pytest.raises(ValueError):
            assemble_claim_evidence_map(
                draft_hash=_DRAFT_HASH,
                rfa_hash=_RFA_HASH,
                session_id=_SESSION_ID,
                org_slug=_ORG_SLUG,
                rfa_url_hash=_RFA_URL_HASH,
                claims=(bad,),
                rigor_breach_active=False,
                generated_at_utc="2026-04-19T00:00:00.000000Z",
            )


# ---------------------------------------------------------------------------
# canonical_map_bytes — §7.5 byte-identical
# ---------------------------------------------------------------------------


class TestCanonicalBytes:
    def test_byte_identical_round_trip(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(), _unsourced_claim(), _user_data_claim()),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        b1 = canonical_map_bytes(m)
        b2 = canonical_map_bytes(m)
        assert b1 == b2

    def test_canonical_bytes_independent_of_input_order(self) -> None:
        c1 = _doc_claim("alpha")
        c2 = _doc_claim("beta")
        m_a = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(c1, c2),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        m_b = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(c2, c1),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert canonical_map_bytes(m_a) == canonical_map_bytes(m_b)

    def test_canonical_bytes_is_valid_json(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        b = canonical_map_bytes(m)
        parsed = json.loads(b)
        assert parsed["map_id"] == m.map_id
        assert parsed["draft_hash"] == _DRAFT_HASH
        assert isinstance(parsed["entries"], list)


class TestComputeContentHash:
    def test_deterministic(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        h1 = compute_content_hash(m)
        h2 = compute_content_hash(m)
        assert h1 == h2
        assert len(h1) == 128


class TestVerifyCanonicalIdempotent:
    def test_passes_for_canonical(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        b = canonical_map_bytes(m)
        assert verify_canonical_idempotent(b) is True

    def test_fails_for_non_canonical_bytes(self) -> None:
        # Non-canonical: pretty-printed JSON, keys not sorted
        non_canon = b'{ "x": 1,  "a": 2 }'
        assert verify_canonical_idempotent(non_canon) is False


# ---------------------------------------------------------------------------
# SignedClaimEvidenceMap shape
# ---------------------------------------------------------------------------


class TestSignedShape:
    def test_signed_map_frozen(self) -> None:
        m = assemble_claim_evidence_map(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        signed = SignedClaimEvidenceMap(
            map=m,
            content_hash=compute_content_hash(m),
            signature=b"\x00" * 64,
            operator_key_id="key-2026-04",
            signed_at_utc="2026-04-19T00:00:01.000000Z",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            signed.operator_key_id = "x"  # type: ignore[misc]
        assert signed.map is m


# ---------------------------------------------------------------------------
# POST-gate skeleton
# ---------------------------------------------------------------------------


class TestPostGateSkeletonHappy:
    def test_pass_with_only_doc_sourced(self) -> None:
        result = run_post_gate_skeleton(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(), _user_data_claim()),
            rigor_breach_active=False,
            admin_risk_hard_block_count=0,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert isinstance(result, PostGateResult)
        assert result.success is True
        assert result.failure_codes == ()
        assert result.claim_evidence_map is not None
        assert result.unsourced_count == 0
        assert result.hard_block_count == 0


class TestPostGateSkeletonUnsourced:
    def test_unsourced_blocks_with_f_post_11(self) -> None:
        result = run_post_gate_skeleton(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(), _unsourced_claim()),
            rigor_breach_active=False,
            admin_risk_hard_block_count=0,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert result.success is False
        assert F_POST_11 in result.failure_codes
        assert result.unsourced_count == 1
        # Map IS produced — POST-gate produces artifacts even on block; operator
        # sees the map to decide which UNSOURCED resolution path to take.
        assert result.claim_evidence_map is not None


class TestPostGateSkeletonHardBlock:
    def test_hard_block_routes_f_post_10(self) -> None:
        result = run_post_gate_skeleton(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            admin_risk_hard_block_count=2,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert result.success is False
        assert F_POST_10 in result.failure_codes
        assert result.hard_block_count == 2

    def test_both_unsourced_and_hard_block_surface_both_codes(self) -> None:
        result = run_post_gate_skeleton(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_unsourced_claim(),),
            rigor_breach_active=False,
            admin_risk_hard_block_count=1,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        assert result.success is False
        assert F_POST_10 in result.failure_codes
        assert F_POST_11 in result.failure_codes


class TestPostGateConstants:
    def test_f_post_10(self) -> None:
        assert F_POST_10 == "F-POST-10"

    def test_f_post_11(self) -> None:
        assert F_POST_11 == "F-POST-11"


class TestPostGateResultShape:
    def test_frozen(self) -> None:
        result = run_post_gate_skeleton(
            draft_hash=_DRAFT_HASH,
            rfa_hash=_RFA_HASH,
            session_id=_SESSION_ID,
            org_slug=_ORG_SLUG,
            rfa_url_hash=_RFA_URL_HASH,
            claims=(_doc_claim(),),
            rigor_breach_active=False,
            admin_risk_hard_block_count=0,
            generated_at_utc="2026-04-19T00:00:00.000000Z",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.success = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Type gates
# ---------------------------------------------------------------------------


class TestTypeGates:
    def test_claims_must_be_tuple_of_claimentry(self) -> None:
        with pytest.raises(TypeError):
            run_post_gate_skeleton(
                draft_hash=_DRAFT_HASH,
                rfa_hash=_RFA_HASH,
                session_id=_SESSION_ID,
                org_slug=_ORG_SLUG,
                rfa_url_hash=_RFA_URL_HASH,
                claims=[{"x": 1}],  # type: ignore[arg-type]
                rigor_breach_active=False,
                admin_risk_hard_block_count=0,
                generated_at_utc="2026-04-19T00:00:00.000000Z",
            )

    def test_admin_risk_hard_block_count_must_be_nonneg_int(self) -> None:
        with pytest.raises((TypeError, ValueError)):
            run_post_gate_skeleton(
                draft_hash=_DRAFT_HASH,
                rfa_hash=_RFA_HASH,
                session_id=_SESSION_ID,
                org_slug=_ORG_SLUG,
                rfa_url_hash=_RFA_URL_HASH,
                claims=(_doc_claim(),),
                rigor_breach_active=False,
                admin_risk_hard_block_count=-1,
                generated_at_utc="2026-04-19T00:00:00.000000Z",
            )

    def test_assembler_rejects_non_tuple_claims(self) -> None:
        with pytest.raises(TypeError):
            assemble_claim_evidence_map(
                draft_hash=_DRAFT_HASH,
                rfa_hash=_RFA_HASH,
                session_id=_SESSION_ID,
                org_slug=_ORG_SLUG,
                rfa_url_hash=_RFA_URL_HASH,
                claims=[_doc_claim()],  # type: ignore[arg-type]
                rigor_breach_active=False,
                generated_at_utc="2026-04-19T00:00:00.000000Z",
            )


# ---------------------------------------------------------------------------
# PostGateSkeletonFailed exception (escape hatch for callers that want to raise)
# ---------------------------------------------------------------------------


class TestPostGateSkeletonFailedException:
    def test_carries_codes(self) -> None:
        e = PostGateSkeletonFailed(("F-POST-11",))
        assert "F-POST-11" in str(e)
        assert e.failure_codes == ("F-POST-11",)
