"""Unit tests for F-UPLOADER-CONTENT-MUTATION (POST-19).

Per Blueprint §12.9.5 + §4 v2.7 amendment.
"""

from __future__ import annotations

from pipeline.logician.gates.f_uploader_content_mutation import (
    F_UPLOADER_CONTENT_MUTATION,
    check_uploader_content_mutation,
)


def test_failure_code_constant() -> None:
    assert F_UPLOADER_CONTENT_MUTATION == "F-UPLOADER-CONTENT-MUTATION"


def test_identical_text_passes() -> None:
    r = check_uploader_content_mutation(
        section_name="narrative",
        input_body_text="The project will improve regional food access.",
        output_extracted_text="The project will improve regional food access.",
    )
    assert r.success is True
    assert r.failure_code is None


def test_whitespace_normalization_passes() -> None:
    """Page numbers / line breaks are not content mutation."""
    r = check_uploader_content_mutation(
        section_name="narrative",
        input_body_text="Line one.\nLine two.",
        output_extracted_text="Line one.\n\n   Line two.   ",
    )
    assert r.success is True


def test_word_change_fails() -> None:
    r = check_uploader_content_mutation(
        section_name="narrative",
        input_body_text="The project will improve regional food access.",
        output_extracted_text="The project will reduce regional food access.",
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_CONTENT_MUTATION
    assert "narrative" in r.detail


def test_missing_sentence_fails() -> None:
    r = check_uploader_content_mutation(
        section_name="budget",
        input_body_text="Total budget is $50,000. Match is $25,000.",
        output_extracted_text="Total budget is $50,000.",
    )
    assert r.success is False


def test_added_text_fails() -> None:
    r = check_uploader_content_mutation(
        section_name="abstract",
        input_body_text="Abstract.",
        output_extracted_text="Abstract. Added by renderer.",
    )
    assert r.success is False


def test_empty_strings_pass() -> None:
    r = check_uploader_content_mutation(
        section_name="empty",
        input_body_text="",
        output_extracted_text="",
    )
    assert r.success is True


def test_whitespace_only_diff_passes() -> None:
    r = check_uploader_content_mutation(
        section_name="ws",
        input_body_text="a b c",
        output_extracted_text="  a   b   c  ",
    )
    assert r.success is True
