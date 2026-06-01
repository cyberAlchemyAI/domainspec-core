"""Tests for pipeline.seats.scribe.section_draft — §7.5 + §7.2 Law 1 + §7.11 + §7.4a."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from pipeline.seats.scribe.compress import count_characters, count_words
from pipeline.seats.scribe.section_draft import (
    AdminRiskFlag,
    ClaimEvidence,
    CompressedSectionDraft,
    ConversationAnchor,
    EligibleActivityMatch,
    ScopeCheckComment,
    SectionDraft,
    SectionLimit,
)


_FIXED = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)
_GOOD_SHA_128 = "a" * 128
_GOOD_ANCHOR_PREFIX = "f" * 32


def _mk_draft(
    *,
    body_text: str = "hello world",
    rfa_section_limit: SectionLimit | None = None,
    over_limit_flag: bool = False,
    claim_evidence_map: tuple[ClaimEvidence, ...] = (),
    eligible_activity_map: tuple[EligibleActivityMatch, ...] = (),
    admin_risk_flags: tuple[AdminRiskFlag, ...] = (),
    scope_check_comments: tuple[ScopeCheckComment, ...] = (),
) -> SectionDraft:
    return SectionDraft(
        section_name="Project Description",
        section_order=1,
        body_text=body_text,
        word_count=count_words(body_text),
        character_count=count_characters(body_text),
        rfa_section_limit=rfa_section_limit,
        over_limit_flag=over_limit_flag,
        claim_evidence_map=claim_evidence_map,
        eligible_activity_map=eligible_activity_map,
        admin_risk_flags=admin_risk_flags,
        scope_check_comments=scope_check_comments,
        draft_dialect="centrist",
        drafted_at_utc=_FIXED,
    )


# ---------------------------------------------------------------------------
# SectionLimit
# ---------------------------------------------------------------------------


class TestSectionLimit:
    def test_words(self) -> None:
        lim = SectionLimit(limit_kind="words", limit_value=500)
        assert lim.limit_value == 500

    def test_characters(self) -> None:
        lim = SectionLimit(limit_kind="characters", limit_value=3000)
        assert lim.limit_kind == "characters"

    def test_pages(self) -> None:
        lim = SectionLimit(limit_kind="pages", limit_value=3)
        assert lim.limit_kind == "pages"

    def test_zero_value_rejected(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            SectionLimit(limit_kind="words", limit_value=0)

    def test_negative_value_rejected(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            SectionLimit(limit_kind="words", limit_value=-1)

    def test_invalid_kind_rejected(self) -> None:
        with pytest.raises(ValueError, match="limit_kind"):
            SectionLimit(limit_kind="bogus", limit_value=100)  # type: ignore[arg-type]

    def test_frozen(self) -> None:
        lim = SectionLimit(limit_kind="words", limit_value=500)
        with pytest.raises(Exception):
            lim.limit_value = 1000  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ClaimEvidence
# ---------------------------------------------------------------------------


class TestClaimEvidence:
    def test_rfa_kind(self) -> None:
        ev = ClaimEvidence(
            claim_text="applicant has 8 years operating",
            evidence_kind="RFA",
            source_pointer="vapg_rfa.pdf#p14",
        )
        assert ev.evidence_kind == "RFA"

    def test_project_context_kind(self) -> None:
        ev = ClaimEvidence(
            claim_text="located in Lycoming County",
            evidence_kind="PROJECT_CONTEXT",
            source_pointer="orgs/fit_farms/PROJECT_CONTEXT.md#location.county",
        )
        assert ev.evidence_kind == "PROJECT_CONTEXT"

    def test_user_data_kind(self) -> None:
        ev = ClaimEvidence(
            claim_text="Josh mentioned Penn State partnership",
            evidence_kind="USER_DATA",
            source_pointer="USER_DATA:run_42:7:abcd1234abcd1234abcd1234abcd1234",
        )
        assert ev.evidence_kind == "USER_DATA"

    def test_empty_claim_rejected(self) -> None:
        with pytest.raises(ValueError, match="claim_text"):
            ClaimEvidence(
                claim_text="",
                evidence_kind="RFA",
                source_pointer="x",
            )

    def test_whitespace_claim_rejected(self) -> None:
        with pytest.raises(ValueError, match="claim_text"):
            ClaimEvidence(
                claim_text="   ",
                evidence_kind="RFA",
                source_pointer="x",
            )

    def test_invalid_kind_rejected(self) -> None:
        with pytest.raises(ValueError, match="evidence_kind"):
            ClaimEvidence(
                claim_text="x",
                evidence_kind="WEB",  # type: ignore[arg-type]
                source_pointer="y",
            )

    def test_empty_pointer_rejected(self) -> None:
        with pytest.raises(ValueError, match="source_pointer"):
            ClaimEvidence(
                claim_text="x",
                evidence_kind="RFA",
                source_pointer="",
            )


# ---------------------------------------------------------------------------
# EligibleActivityMatch
# ---------------------------------------------------------------------------


class TestEligibleActivityMatch:
    def test_matched_no_flag(self) -> None:
        m = EligibleActivityMatch(
            activity_phrase="on-farm processing equipment",
            matched_rfa_activity="on-farm value-added processing",
            scope_check_flag=False,
        )
        assert m.matched_rfa_activity == "on-farm value-added processing"

    def test_matched_with_flag_ok(self) -> None:
        m = EligibleActivityMatch(
            activity_phrase="outreach to underserved",
            matched_rfa_activity="outreach activities",
            scope_check_flag=True,
        )
        assert m.scope_check_flag is True

    def test_unmatched_must_flag(self) -> None:
        with pytest.raises(ValueError, match="scope_check_flag=True"):
            EligibleActivityMatch(
                activity_phrase="real estate acquisition",
                matched_rfa_activity=None,
                scope_check_flag=False,
            )

    def test_unmatched_with_flag_ok(self) -> None:
        m = EligibleActivityMatch(
            activity_phrase="real estate acquisition",
            matched_rfa_activity=None,
            scope_check_flag=True,
        )
        assert m.matched_rfa_activity is None

    def test_empty_phrase_rejected(self) -> None:
        with pytest.raises(ValueError, match="activity_phrase"):
            EligibleActivityMatch(
                activity_phrase="",
                matched_rfa_activity="x",
                scope_check_flag=False,
            )

    def test_whitespace_matched_rejected(self) -> None:
        with pytest.raises(ValueError, match="matched_rfa_activity"):
            EligibleActivityMatch(
                activity_phrase="x",
                matched_rfa_activity="   ",
                scope_check_flag=False,
            )


# ---------------------------------------------------------------------------
# AdminRiskFlag
# ---------------------------------------------------------------------------


class TestAdminRiskFlag:
    def test_low_severity(self) -> None:
        f = AdminRiskFlag(
            term="DEI",
            severity="low",
            proposed_substitution="community-inclusive",
            applicant_approved=True,
        )
        assert f.severity == "low"

    def test_medium_severity(self) -> None:
        f = AdminRiskFlag(
            term="equity",
            severity="medium",
            proposed_substitution="fairness",
            applicant_approved=False,
        )
        assert f.applicant_approved is False

    def test_high_severity(self) -> None:
        f = AdminRiskFlag(
            term="climate justice",
            severity="high",
            proposed_substitution=None,
            applicant_approved=False,
        )
        assert f.proposed_substitution is None

    def test_invalid_severity_rejected(self) -> None:
        with pytest.raises(ValueError, match="severity"):
            AdminRiskFlag(
                term="x",
                severity="critical",  # type: ignore[arg-type]
                proposed_substitution=None,
                applicant_approved=False,
            )

    def test_empty_term_rejected(self) -> None:
        with pytest.raises(ValueError, match="term"):
            AdminRiskFlag(
                term="",
                severity="low",
                proposed_substitution=None,
                applicant_approved=False,
            )

    def test_whitespace_substitution_rejected(self) -> None:
        with pytest.raises(ValueError, match="proposed_substitution"):
            AdminRiskFlag(
                term="x",
                severity="low",
                proposed_substitution="  ",
                applicant_approved=False,
            )


# ---------------------------------------------------------------------------
# ScopeCheckComment
# ---------------------------------------------------------------------------


class TestScopeCheckComment:
    def test_ok(self) -> None:
        c = ScopeCheckComment(
            activity_phrase="land acquisition",
            comment="Not in RFA eligible_project_activities; confirm scope.",
        )
        assert "scope" in c.comment

    def test_empty_phrase_rejected(self) -> None:
        with pytest.raises(ValueError, match="activity_phrase"):
            ScopeCheckComment(activity_phrase="", comment="x")

    def test_empty_comment_rejected(self) -> None:
        with pytest.raises(ValueError, match="comment"):
            ScopeCheckComment(activity_phrase="x", comment="  ")


# ---------------------------------------------------------------------------
# ConversationAnchor
# ---------------------------------------------------------------------------


class TestConversationAnchor:
    def test_ok(self) -> None:
        a = ConversationAnchor(
            run_id="run_abc",
            turn_ordinal=7,
            sha3_512_prefix32=_GOOD_ANCHOR_PREFIX,
        )
        assert a.turn_ordinal == 7

    def test_ordinal_zero_ok(self) -> None:
        a = ConversationAnchor(
            run_id="run_abc",
            turn_ordinal=0,
            sha3_512_prefix32=_GOOD_ANCHOR_PREFIX,
        )
        assert a.turn_ordinal == 0

    def test_negative_ordinal_rejected(self) -> None:
        with pytest.raises(ValueError, match="turn_ordinal"):
            ConversationAnchor(
                run_id="run_abc",
                turn_ordinal=-1,
                sha3_512_prefix32=_GOOD_ANCHOR_PREFIX,
            )

    def test_empty_run_id_rejected(self) -> None:
        with pytest.raises(ValueError, match="run_id"):
            ConversationAnchor(
                run_id="",
                turn_ordinal=0,
                sha3_512_prefix32=_GOOD_ANCHOR_PREFIX,
            )

    def test_wrong_prefix_length_rejected(self) -> None:
        with pytest.raises(ValueError, match="32 hex"):
            ConversationAnchor(
                run_id="run_abc",
                turn_ordinal=0,
                sha3_512_prefix32="f" * 16,
            )

    def test_uppercase_hex_rejected(self) -> None:
        with pytest.raises(ValueError, match="lowercase"):
            ConversationAnchor(
                run_id="run_abc",
                turn_ordinal=0,
                sha3_512_prefix32="F" * 32,
            )

    def test_non_hex_char_rejected(self) -> None:
        with pytest.raises(ValueError, match="lowercase"):
            ConversationAnchor(
                run_id="run_abc",
                turn_ordinal=0,
                sha3_512_prefix32="g" * 32,
            )

    def test_as_source_pointer(self) -> None:
        a = ConversationAnchor(
            run_id="run_xyz",
            turn_ordinal=3,
            sha3_512_prefix32="a" * 32,
        )
        assert a.as_source_pointer() == f"USER_DATA:run_xyz:3:{'a' * 32}"


# ---------------------------------------------------------------------------
# SectionDraft
# ---------------------------------------------------------------------------


class TestSectionDraftBase:
    def test_happy_path_no_limit(self) -> None:
        d = _mk_draft()
        assert d.word_count == 2
        assert d.character_count == 11

    def test_empty_body_ok(self) -> None:
        d = _mk_draft(body_text="")
        assert d.word_count == 0
        assert d.character_count == 0

    def test_word_count_mismatch_rejected(self) -> None:
        with pytest.raises(ValueError, match="word_count"):
            SectionDraft(
                section_name="X",
                section_order=1,
                body_text="one two three",
                word_count=2,
                character_count=13,
                rfa_section_limit=None,
                over_limit_flag=False,
                claim_evidence_map=(),
                eligible_activity_map=(),
                admin_risk_flags=(),
                scope_check_comments=(),
                draft_dialect="centrist",
                drafted_at_utc=_FIXED,
            )

    def test_character_count_mismatch_rejected(self) -> None:
        with pytest.raises(ValueError, match="character_count"):
            SectionDraft(
                section_name="X",
                section_order=1,
                body_text="hi",
                word_count=1,
                character_count=5,
                rfa_section_limit=None,
                over_limit_flag=False,
                claim_evidence_map=(),
                eligible_activity_map=(),
                admin_risk_flags=(),
                scope_check_comments=(),
                draft_dialect="centrist",
                drafted_at_utc=_FIXED,
            )

    def test_empty_section_name_rejected(self) -> None:
        with pytest.raises(ValueError, match="section_name"):
            SectionDraft(
                section_name="",
                section_order=1,
                body_text="",
                word_count=0,
                character_count=0,
                rfa_section_limit=None,
                over_limit_flag=False,
                claim_evidence_map=(),
                eligible_activity_map=(),
                admin_risk_flags=(),
                scope_check_comments=(),
                draft_dialect="centrist",
                drafted_at_utc=_FIXED,
            )

    def test_section_order_zero_rejected(self) -> None:
        with pytest.raises(ValueError, match="section_order"):
            SectionDraft(
                section_name="X",
                section_order=0,
                body_text="",
                word_count=0,
                character_count=0,
                rfa_section_limit=None,
                over_limit_flag=False,
                claim_evidence_map=(),
                eligible_activity_map=(),
                admin_risk_flags=(),
                scope_check_comments=(),
                draft_dialect="centrist",
                drafted_at_utc=_FIXED,
            )

    def test_naive_utc_rejected(self) -> None:
        with pytest.raises(ValueError, match="timezone-aware"):
            SectionDraft(
                section_name="X",
                section_order=1,
                body_text="",
                word_count=0,
                character_count=0,
                rfa_section_limit=None,
                over_limit_flag=False,
                claim_evidence_map=(),
                eligible_activity_map=(),
                admin_risk_flags=(),
                scope_check_comments=(),
                draft_dialect="centrist",
                drafted_at_utc=datetime(2026, 4, 21, 12, 0, 0),
            )

    def test_body_non_str_rejected(self) -> None:
        with pytest.raises(ValueError, match="body_text"):
            SectionDraft(
                section_name="X",
                section_order=1,
                body_text=b"bytes not str",  # type: ignore[arg-type]
                word_count=0,
                character_count=0,
                rfa_section_limit=None,
                over_limit_flag=False,
                claim_evidence_map=(),
                eligible_activity_map=(),
                admin_risk_flags=(),
                scope_check_comments=(),
                draft_dialect="centrist",
                drafted_at_utc=_FIXED,
            )


class TestSectionDraftOverLimit:
    def test_words_under_limit_flag_false_ok(self) -> None:
        lim = SectionLimit(limit_kind="words", limit_value=10)
        d = _mk_draft(
            body_text="one two three",
            rfa_section_limit=lim,
            over_limit_flag=False,
        )
        assert d.over_limit_flag is False

    def test_words_over_limit_flag_true_ok(self) -> None:
        lim = SectionLimit(limit_kind="words", limit_value=2)
        d = _mk_draft(
            body_text="one two three four",
            rfa_section_limit=lim,
            over_limit_flag=True,
        )
        assert d.over_limit_flag is True

    def test_words_over_limit_unflagged_rejected(self) -> None:
        lim = SectionLimit(limit_kind="words", limit_value=2)
        with pytest.raises(ValueError, match="over_limit_flag"):
            _mk_draft(
                body_text="one two three four",
                rfa_section_limit=lim,
                over_limit_flag=False,
            )

    def test_words_under_limit_flag_true_rejected(self) -> None:
        lim = SectionLimit(limit_kind="words", limit_value=10)
        with pytest.raises(ValueError, match="over_limit_flag"):
            _mk_draft(
                body_text="one two",
                rfa_section_limit=lim,
                over_limit_flag=True,
            )

    def test_characters_over_limit(self) -> None:
        lim = SectionLimit(limit_kind="characters", limit_value=5)
        d = _mk_draft(
            body_text="hello world",
            rfa_section_limit=lim,
            over_limit_flag=True,
        )
        assert d.character_count == 11

    def test_characters_under_limit(self) -> None:
        lim = SectionLimit(limit_kind="characters", limit_value=100)
        d = _mk_draft(
            body_text="hello",
            rfa_section_limit=lim,
            over_limit_flag=False,
        )
        assert d.over_limit_flag is False

    def test_characters_mismatch_rejected(self) -> None:
        lim = SectionLimit(limit_kind="characters", limit_value=3)
        with pytest.raises(ValueError, match="character-count-vs-limit"):
            _mk_draft(
                body_text="hello",
                rfa_section_limit=lim,
                over_limit_flag=False,
            )

    def test_pages_limit_skipped_at_shape_layer(self) -> None:
        # R2 trusts seat-computed over_limit_flag for pages-kind.
        lim = SectionLimit(limit_kind="pages", limit_value=1)
        d = _mk_draft(
            body_text="anything",
            rfa_section_limit=lim,
            over_limit_flag=True,
        )
        assert d.over_limit_flag is True

    def test_no_limit_flag_true_rejected(self) -> None:
        with pytest.raises(ValueError, match="must be False"):
            _mk_draft(
                body_text="hi",
                rfa_section_limit=None,
                over_limit_flag=True,
            )


# ---------------------------------------------------------------------------
# CompressedSectionDraft
# ---------------------------------------------------------------------------


class TestCompressedSectionDraft:
    def test_ok(self) -> None:
        d = _mk_draft()
        c = CompressedSectionDraft(
            compressed_draft=d,
            source_uncut_draft_sha3_512=_GOOD_SHA_128,
            compression_rationale=("removed two paragraphs on outreach",),
        )
        assert c.compressed_draft is d

    def test_short_sha_rejected(self) -> None:
        d = _mk_draft()
        with pytest.raises(ValueError, match="hex chars"):
            CompressedSectionDraft(
                compressed_draft=d,
                source_uncut_draft_sha3_512="a" * 64,
                compression_rationale=("x",),
            )

    def test_uppercase_sha_rejected(self) -> None:
        d = _mk_draft()
        with pytest.raises(ValueError, match="lowercase"):
            CompressedSectionDraft(
                compressed_draft=d,
                source_uncut_draft_sha3_512="A" * 128,
                compression_rationale=("x",),
            )

    def test_empty_rationale_rejected(self) -> None:
        d = _mk_draft()
        with pytest.raises(ValueError, match="non-empty"):
            CompressedSectionDraft(
                compressed_draft=d,
                source_uncut_draft_sha3_512=_GOOD_SHA_128,
                compression_rationale=(),
            )

    def test_empty_rationale_entry_rejected(self) -> None:
        d = _mk_draft()
        with pytest.raises(ValueError, match=r"compression_rationale\[1\]"):
            CompressedSectionDraft(
                compressed_draft=d,
                source_uncut_draft_sha3_512=_GOOD_SHA_128,
                compression_rationale=("ok", "   "),
            )

    def test_over_limit_compressed_rejected(self) -> None:
        lim = SectionLimit(limit_kind="words", limit_value=2)
        d = _mk_draft(
            body_text="one two three four",
            rfa_section_limit=lim,
            over_limit_flag=True,
        )
        with pytest.raises(ValueError, match="over_limit_flag=True"):
            CompressedSectionDraft(
                compressed_draft=d,
                source_uncut_draft_sha3_512=_GOOD_SHA_128,
                compression_rationale=("x",),
            )
