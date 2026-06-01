"""Tests for pipeline.seats.scribe.compress — §7.10 counters."""

from __future__ import annotations

import pytest

from pipeline.seats.scribe.compress import (
    count_characters,
    count_pages,
    count_words,
    is_over_limit,
)
from pipeline.seats.scribe.section_draft import SectionLimit


# ---------------------------------------------------------------------------
# count_words
# ---------------------------------------------------------------------------


class TestCountWords:
    def test_simple_sentence(self) -> None:
        assert count_words("the quick brown fox") == 4

    def test_empty_string(self) -> None:
        assert count_words("") == 0

    def test_whitespace_only(self) -> None:
        assert count_words("   \t\n  ") == 0

    def test_mixed_whitespace_collapses(self) -> None:
        assert count_words("one\ttwo\n three  four") == 4

    def test_numeric_token_is_one_word(self) -> None:
        # Numeric-verbatim lives in smart.py; compress just splits.
        assert count_words("budget is $12,500.50 total") == 4

    def test_trailing_punctuation_does_not_split(self) -> None:
        assert count_words("hello, world!") == 2

    def test_non_str_raises(self) -> None:
        with pytest.raises(TypeError, match="str"):
            count_words(123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# count_characters
# ---------------------------------------------------------------------------


class TestCountCharacters:
    def test_ascii(self) -> None:
        assert count_characters("hello") == 5

    def test_empty(self) -> None:
        assert count_characters("") == 0

    def test_counts_whitespace(self) -> None:
        assert count_characters("a b") == 3

    def test_unicode_code_points(self) -> None:
        # "café" = 4 code points (c, a, f, é) in NFC.
        assert count_characters("café") == 4

    def test_non_str_raises(self) -> None:
        with pytest.raises(TypeError, match="str"):
            count_characters(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# count_pages
# ---------------------------------------------------------------------------


class TestCountPages:
    def test_empty_is_zero_pages(self) -> None:
        assert count_pages("", chars_per_page=3000) == 0

    def test_exactly_one_page(self) -> None:
        assert count_pages("a" * 3000, chars_per_page=3000) == 1

    def test_one_over_rounds_up_to_two(self) -> None:
        assert count_pages("a" * 3001, chars_per_page=3000) == 2

    def test_half_page_is_one(self) -> None:
        assert count_pages("a" * 1500, chars_per_page=3000) == 1

    def test_small_chars_per_page(self) -> None:
        assert count_pages("abcdefghij", chars_per_page=3) == 4  # ceil(10/3)

    def test_zero_chars_per_page_rejected(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            count_pages("hello", chars_per_page=0)

    def test_negative_chars_per_page_rejected(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            count_pages("hello", chars_per_page=-100)

    def test_non_int_chars_per_page_rejected(self) -> None:
        with pytest.raises(TypeError, match="int"):
            count_pages("hello", chars_per_page=3000.0)  # type: ignore[arg-type]

    def test_bool_chars_per_page_rejected(self) -> None:
        with pytest.raises(TypeError, match="int"):
            count_pages("hello", chars_per_page=True)  # type: ignore[arg-type]

    def test_non_str_text_rejected(self) -> None:
        with pytest.raises(TypeError, match="str"):
            count_pages(42, chars_per_page=3000)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# is_over_limit
# ---------------------------------------------------------------------------


class TestIsOverLimitWords:
    def test_under(self) -> None:
        limit = SectionLimit(limit_kind="words", limit_value=10)
        assert is_over_limit("one two three", limit) is False

    def test_at_boundary_is_not_over(self) -> None:
        limit = SectionLimit(limit_kind="words", limit_value=3)
        assert is_over_limit("one two three", limit) is False

    def test_over(self) -> None:
        limit = SectionLimit(limit_kind="words", limit_value=2)
        assert is_over_limit("one two three", limit) is True


class TestIsOverLimitCharacters:
    def test_under(self) -> None:
        limit = SectionLimit(limit_kind="characters", limit_value=100)
        assert is_over_limit("hello world", limit) is False

    def test_at_boundary_is_not_over(self) -> None:
        limit = SectionLimit(limit_kind="characters", limit_value=5)
        assert is_over_limit("hello", limit) is False

    def test_over(self) -> None:
        limit = SectionLimit(limit_kind="characters", limit_value=4)
        assert is_over_limit("hello", limit) is True


class TestIsOverLimitPages:
    def test_under(self) -> None:
        limit = SectionLimit(limit_kind="pages", limit_value=2)
        assert (
            is_over_limit("a" * 3000, limit, chars_per_page=3000) is False
        )

    def test_at_boundary_is_not_over(self) -> None:
        limit = SectionLimit(limit_kind="pages", limit_value=1)
        assert (
            is_over_limit("a" * 3000, limit, chars_per_page=3000) is False
        )

    def test_over(self) -> None:
        limit = SectionLimit(limit_kind="pages", limit_value=1)
        assert (
            is_over_limit("a" * 3001, limit, chars_per_page=3000) is True
        )

    def test_missing_chars_per_page_rejected(self) -> None:
        limit = SectionLimit(limit_kind="pages", limit_value=2)
        with pytest.raises(ValueError, match="chars_per_page"):
            is_over_limit("hello", limit)
