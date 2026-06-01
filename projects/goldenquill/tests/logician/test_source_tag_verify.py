"""Tests for pipeline.logician.source_tag_verify (BT10 grep-windowed). [§4.6]

Round 3 lands the deterministic sentence tokenizer with §8.2 abbreviation
carve-outs, the windowed-grep primitive (±2 default, ±5 fallback, full-text
fallback), the M12 source-directory whitelist enforcement, and the
inode/content-hash drift predicates that POST-gate step 4/5 surface as
F-POST-04 sub-tags.

The full POST-gate wiring + USER_DATA conversation_anchor verifier land in
Round 4 (BT9). This round is self-contained: pure-function classifier with
zero filesystem coupling beyond M12 path predicates.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from pipeline.logician.source_tag_verify import (
    BT10_BASE_ABBREVIATIONS,
    F_BT10_01,
    F_BT10_02,
    F_POST_04_CONTENT_HASH_MISMATCH,
    F_POST_04_INODE_DRIFT,
    F_POST_04_PATH_OUTSIDE_M12,
    F_POST_04_SYMLINK_IN_PATH,
    BT10TokenizerFailed,
    SourceTagVerifyResult,
    extract_grep_string,
    find_first_sentence_index,
    is_under_m12_root,
    path_has_symlink_component,
    tokenize_sentences,
    verify_content_hash,
    verify_doc_sourced_claim,
    verify_inode,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_base_abbreviations_pinned(self) -> None:
        # §8.2 — verbatim pinned list
        for a in (
            "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "Inc.", "Ltd.", "Co.", "Corp.",
            "etc.", "vs.", "e.g.", "i.e.", "U.S.", "U.K.", "U.N.", "a.m.", "p.m.",
            "No.", "Vol.", "Ch.", "St.", "Ave.", "Blvd.", "Rd.", "Jr.", "Sr.",
            "Ph.D.", "M.D.", "B.A.", "M.A.", "B.S.", "M.S.",
        ):
            assert a in BT10_BASE_ABBREVIATIONS

    def test_failure_codes(self) -> None:
        assert F_BT10_01 == "F-BT10-01"
        assert F_BT10_02 == "F-BT10-02"
        assert F_POST_04_SYMLINK_IN_PATH == "F-POST-04.symlink_in_source_path"
        assert F_POST_04_INODE_DRIFT == "F-POST-04.inode_drift"
        assert F_POST_04_PATH_OUTSIDE_M12 == "F-POST-04.path_outside_m12_whitelist"
        assert F_POST_04_CONTENT_HASH_MISMATCH == "F-POST-04.content_hash_mismatch"


# ---------------------------------------------------------------------------
# Sentence tokenizer
# ---------------------------------------------------------------------------


class TestTokenize:
    def test_simple_period(self) -> None:
        s = tokenize_sentences("Eligible applicants are 501c3 entities. Funding is annual.")
        assert s == ("Eligible applicants are 501c3 entities.", "Funding is annual.")

    def test_question_mark(self) -> None:
        s = tokenize_sentences("Are matching funds required? No.")
        assert s == ("Are matching funds required?", "No.")

    def test_exclamation(self) -> None:
        s = tokenize_sentences("Apply now! Deadline approaches.")
        assert s == ("Apply now!", "Deadline approaches.")

    def test_paragraph_break(self) -> None:
        s = tokenize_sentences("First.\n\nSecond.")
        assert "First." in s
        assert "Second." in s
        assert len(s) == 2

    def test_abbreviation_not_split(self) -> None:
        # "Dr. Smith leads the cohort." must be ONE sentence.
        s = tokenize_sentences("Dr. Smith leads the cohort. Funding starts FY26.")
        assert s[0] == "Dr. Smith leads the cohort."
        assert s[1] == "Funding starts FY26."

    def test_us_uk_abbreviation_not_split(self) -> None:
        s = tokenize_sentences("The U.S. and U.K. cooperate. Both sign treaties.")
        assert s == ("The U.S. and U.K. cooperate.", "Both sign treaties.")

    def test_eg_ie_not_split(self) -> None:
        s = tokenize_sentences("Plants e.g. corn and beans grow well. Seeds spread.")
        assert s == ("Plants e.g. corn and beans grow well.", "Seeds spread.")

    def test_phd_md_not_split(self) -> None:
        s = tokenize_sentences("Jane Doe Ph.D. M.D. signed off. Approval recorded.")
        assert s == ("Jane Doe Ph.D. M.D. signed off.", "Approval recorded.")

    def test_empty_string_yields_empty(self) -> None:
        assert tokenize_sentences("") == ()

    def test_whitespace_only_yields_empty(self) -> None:
        assert tokenize_sentences("   \n  \n  ") == ()

    def test_no_terminator_returns_whole_text(self) -> None:
        s = tokenize_sentences("Single fragment with no period")
        assert s == ("Single fragment with no period",)

    def test_extension_abbreviations_carve_out(self) -> None:
        s = tokenize_sentences(
            "USDA Sec. Vilsack signed. Funding announced.",
            extension_abbreviations=("Sec.",),
        )
        assert s == ("USDA Sec. Vilsack signed.", "Funding announced.")

    def test_tokenizer_rejects_non_str(self) -> None:
        with pytest.raises(BT10TokenizerFailed):
            tokenize_sentences(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# extract_grep_string
# ---------------------------------------------------------------------------


class TestExtractGrepString:
    def test_first_sentence_used(self) -> None:
        g = extract_grep_string("Eligible applicants must be 501c3. Other conditions apply.")
        assert g == "Eligible applicants must be 501c3."

    def test_no_terminator_returns_full_text(self) -> None:
        g = extract_grep_string("Just a phrase")
        assert g == "Just a phrase"

    def test_empty_returns_empty(self) -> None:
        assert extract_grep_string("") == ""


# ---------------------------------------------------------------------------
# find_first_sentence_index
# ---------------------------------------------------------------------------


class TestFindFirstSentenceIndex:
    def test_finds_match(self) -> None:
        sents = ("Alpha sentence.", "Beta sentence.", "Gamma sentence.")
        i = find_first_sentence_index(sents, "Beta sentence.", case_sensitive=True)
        assert i == 1

    def test_substring_match(self) -> None:
        sents = ("Alpha pre.", "The full Beta phrase here.", "Gamma.")
        i = find_first_sentence_index(sents, "Beta phrase", case_sensitive=True)
        assert i == 1

    def test_not_found_returns_none(self) -> None:
        sents = ("Alpha.", "Beta.")
        assert find_first_sentence_index(sents, "Zeta", case_sensitive=True) is None

    def test_case_insensitive(self) -> None:
        sents = ("ALPHA SENTENCE.",)
        assert (
            find_first_sentence_index(sents, "alpha sentence", case_sensitive=False)
            == 0
        )


# ---------------------------------------------------------------------------
# verify_doc_sourced_claim — happy path PM2
# ---------------------------------------------------------------------------


class TestVerifyDocSourcedHappy:
    def test_pm2_pass(self) -> None:
        file_text = (
            "Background. "
            "Eligible applicants must be 501c3 entities. "
            "Other conditions apply."
        )
        result = verify_doc_sourced_claim(
            claim_text="Eligible applicants must be 501c3 entities.",
            file_text=file_text,
        )
        assert isinstance(result, SourceTagVerifyResult)
        assert result.verify_result == "PASS"
        assert result.verify_method == "grep_windowed_pm2"
        assert result.window_size_sentences == 2
        assert result.tag == "DOC_SOURCED"

    def test_window_includes_neighbours(self) -> None:
        file_text = "S0. S1. S2 anchor. S3. S4."
        result = verify_doc_sourced_claim(
            claim_text="S2 anchor",
            file_text=file_text,
        )
        assert result.verify_result == "PASS"
        # Anchor at index 2; window [0, 5) contains S0..S4
        assert "S2 anchor." in result.matched_window
        assert "S1." in result.matched_window
        assert "S3." in result.matched_window


# ---------------------------------------------------------------------------
# Fallback paths
# ---------------------------------------------------------------------------


class TestVerifyDocSourcedFallbacks:
    def test_pm5_fallback_not_needed_when_pm2_succeeds(self) -> None:
        # In current spec, pm5 is a wider window for the same find — but if
        # the grep string is found at all, pm2 succeeds (find is over the
        # whole sentence list). We assert that a found claim never falls back.
        file_text = "Sentence one. The anchor sits here. Sentence three."
        result = verify_doc_sourced_claim(
            claim_text="anchor sits here",
            file_text=file_text,
        )
        assert result.verify_method == "grep_windowed_pm2"

    def test_unresolved_when_not_found(self) -> None:
        file_text = "Nothing matching here. At all."
        result = verify_doc_sourced_claim(
            claim_text="completely unrelated phrase",
            file_text=file_text,
        )
        assert result.verify_result == "FAIL"
        assert result.verify_method == "unresolved"
        assert result.tag == "UNSOURCED"

    def test_fulltext_fallback_finds_across_sentence_boundary(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Hard to construct organically: the tokenizer is permissive enough
        # that grep targets surviving extract_grep_string almost always also
        # survive sentence-level search. Force the over-split scenario by
        # monkey-patching tokenize_sentences inside the module to split
        # aggressively, then verify the full-text fallback engages.
        import pipeline.logician.source_tag_verify as stv

        real_tokenize = stv.tokenize_sentences

        def fake_tokenize(text, *, extension_abbreviations=()):
            # Force a wrong split between "Sept." and "Submit" in the file
            # text; for the claim text, simulate the operator carve-out
            # (claim text doesn't split). Together this models a tokenizer
            # bug that would silently mark a well-sourced claim UNSOURCED
            # without the full-text fallback safety net.
            if text == "Apply by Sept. Submit early to win.":
                return ("Apply by Sept.", "Submit early to win.")
            if text == "by Sept. Submit":
                return ("by Sept. Submit",)
            return real_tokenize(text, extension_abbreviations=extension_abbreviations)

        monkeypatch.setattr(stv, "tokenize_sentences", fake_tokenize)

        result = verify_doc_sourced_claim(
            claim_text="by Sept. Submit",
            file_text="Apply by Sept. Submit early to win.",
        )
        assert result.verify_result == "PASS"
        assert result.verify_method == "grep_fulltext_fallback"

    def test_case_insensitive_opt_in(self) -> None:
        file_text = "BACKGROUND. ELIGIBLE APPLICANTS MUST BE NONPROFIT. OTHER."
        result = verify_doc_sourced_claim(
            claim_text="eligible applicants must be nonprofit",
            file_text=file_text,
            case_sensitive=False,
        )
        assert result.verify_result == "PASS"

    def test_case_sensitive_default_misses(self) -> None:
        file_text = "BACKGROUND. ELIGIBLE APPLICANTS MUST BE NONPROFIT. OTHER."
        result = verify_doc_sourced_claim(
            claim_text="eligible applicants must be nonprofit",
            file_text=file_text,
        )
        assert result.verify_result == "FAIL"


# ---------------------------------------------------------------------------
# F-BT10-01 / F-BT10-02
# ---------------------------------------------------------------------------


class TestBT10FailureModes:
    def test_empty_file_yields_window_empty_failure(self) -> None:
        result = verify_doc_sourced_claim(
            claim_text="Anything",
            file_text="",
        )
        assert result.verify_result == "FAIL"
        assert result.failure_code == F_BT10_02

    def test_tokenizer_failure_surfaces_f_bt10_01(self) -> None:
        with pytest.raises(BT10TokenizerFailed):
            tokenize_sentences(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# M12 whitelist
# ---------------------------------------------------------------------------


class TestM12Whitelist:
    def test_under_rfa_root(self, tmp_path: Path) -> None:
        rfa = tmp_path / "rfa"
        rfa.mkdir()
        f = rfa / "rfa-001.md"
        f.write_text("body")
        assert is_under_m12_root(
            canonical_path=f,
            session_slug="fit",
            m12_roots=(tmp_path / "rfa", tmp_path / "orgs"),
        )

    def test_under_session_org_root(self, tmp_path: Path) -> None:
        org = tmp_path / "orgs" / "fit" / "materials"
        org.mkdir(parents=True)
        f = org / "doc.md"
        f.write_text("body")
        assert is_under_m12_root(
            canonical_path=f,
            session_slug="fit",
            m12_roots=(tmp_path / "rfa", tmp_path / "orgs"),
        )

    def test_excludes_cross_org(self, tmp_path: Path) -> None:
        # orgs/<other_slug>/ is not under session "fit"
        other = tmp_path / "orgs" / "mystic" / "materials"
        other.mkdir(parents=True)
        f = other / "doc.md"
        f.write_text("body")
        assert not is_under_m12_root(
            canonical_path=f,
            session_slug="fit",
            m12_roots=(tmp_path / "rfa", tmp_path / "orgs"),
        )

    def test_outside_all_roots(self, tmp_path: Path) -> None:
        f = tmp_path / "elsewhere.md"
        f.write_text("body")
        assert not is_under_m12_root(
            canonical_path=f,
            session_slug="fit",
            m12_roots=(tmp_path / "rfa", tmp_path / "orgs"),
        )

    def test_excludes_scout_cache(self, tmp_path: Path) -> None:
        cache = tmp_path / "orgs" / "fit" / "vault" / "cached"
        cache.mkdir(parents=True)
        f = cache / "scrape.json"
        f.write_text("body")
        # Scout cache is excluded EVEN under session_slug org root
        assert not is_under_m12_root(
            canonical_path=f,
            session_slug="fit",
            m12_roots=(tmp_path / "orgs",),
        )


# ---------------------------------------------------------------------------
# Symlink detection
# ---------------------------------------------------------------------------


class TestSymlinkDetection:
    def test_no_symlink(self, tmp_path: Path) -> None:
        f = tmp_path / "real.md"
        f.write_text("body")
        assert not path_has_symlink_component(f)

    def test_file_is_symlink(self, tmp_path: Path) -> None:
        target = tmp_path / "real.md"
        target.write_text("body")
        link = tmp_path / "link.md"
        link.symlink_to(target)
        assert path_has_symlink_component(link)

    def test_intermediate_symlink_dir(self, tmp_path: Path) -> None:
        real_dir = tmp_path / "real_dir"
        real_dir.mkdir()
        f = real_dir / "doc.md"
        f.write_text("body")
        link_dir = tmp_path / "link_dir"
        link_dir.symlink_to(real_dir)
        # Path traverses link_dir → must detect intermediate symlink
        composite = link_dir / "doc.md"
        assert path_has_symlink_component(composite)


# ---------------------------------------------------------------------------
# Inode + content-hash drift
# ---------------------------------------------------------------------------


class TestInodeContentDrift:
    def test_inode_match(self) -> None:
        assert verify_inode(prior_inode=12345, current_inode=12345) is True

    def test_inode_mismatch(self) -> None:
        assert verify_inode(prior_inode=12345, current_inode=99999) is False

    def test_content_hash_match(self) -> None:
        h = "a" * 128
        assert verify_content_hash(prior_hash=h, current_hash=h) is True

    def test_content_hash_mismatch(self) -> None:
        assert verify_content_hash(prior_hash="a" * 128, current_hash="b" * 128) is False


# ---------------------------------------------------------------------------
# SourceTagVerifyResult shape
# ---------------------------------------------------------------------------


class TestResultShape:
    def test_frozen(self) -> None:
        r = verify_doc_sourced_claim(
            claim_text="anchor here",
            file_text="anchor here.",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.tag = "UNSOURCED"  # type: ignore[misc]

    def test_kw_only(self) -> None:
        with pytest.raises(TypeError):
            SourceTagVerifyResult(  # type: ignore[misc]
                "DOC_SOURCED", "PASS", "grep_windowed_pm2", "", 2, "", None
            )


# ---------------------------------------------------------------------------
# Type gates
# ---------------------------------------------------------------------------


class TestTypeGates:
    def test_claim_text_must_be_str(self) -> None:
        with pytest.raises(TypeError):
            verify_doc_sourced_claim(claim_text=42, file_text="x")  # type: ignore[arg-type]

    def test_file_text_must_be_str(self) -> None:
        with pytest.raises(TypeError):
            verify_doc_sourced_claim(claim_text="x", file_text=42)  # type: ignore[arg-type]

    def test_window_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            verify_doc_sourced_claim(
                claim_text="x", file_text="y.", primary_window=0
            )
