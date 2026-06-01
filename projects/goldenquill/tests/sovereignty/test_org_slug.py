"""Tests for pipeline.sovereignty.org_slug.

Coverage targets (per engineering_process_v0.1.md §11 spec card):
  - §4.3 M3 v2 algorithm step-by-step coverage
  - v1 → v2 regression vectors (whitespace bypass, lossy transliteration)
  - Reserved-slug table (8 entries)
  - Length cap (>64 chars)
  - Monotonic regression corpus at tests/corpus/org_slug/v1/

Property tests cover invariants (idempotence, length bound, character set).
Corpus tests cover specific v1-hardening regression vectors.
Failure-code tests cover every InvalidSlug / ReservedSlug path.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.sovereignty import (
    InvalidSlug,
    ReservedSlug,
    SlugCollisionError,
    canonical_slug,
    ensure_slug_available,
)

_CORPUS_PATH = (
    Path(__file__).resolve().parents[1]
    / "corpus"
    / "org_slug"
    / "v1"
    / "inputs_expected.json"
)


# -------- corpus regression tests --------

def _load_corpus() -> dict:
    with _CORPUS_PATH.open() as f:
        return json.load(f)


class TestCorpusPass:
    """Inputs that MUST canonicalize to the exact expected slug."""

    @pytest.mark.parametrize(
        "vector",
        _load_corpus()["pass"],
        ids=lambda v: f"{v['input']!r}->{v['expected']!r}",
    )
    def test_canonicalization_matches_expected(self, vector: dict) -> None:
        assert canonical_slug(vector["input"]) == vector["expected"]


class TestCorpusRejectInvalid:
    """Inputs that MUST raise InvalidSlug with the expected reason."""

    @pytest.mark.parametrize(
        "vector",
        _load_corpus()["reject_invalid_slug"],
        ids=lambda v: f"{v['input']!r}={v['reason']}",
    )
    def test_raises_invalid_slug(self, vector: dict) -> None:
        with pytest.raises(InvalidSlug) as exc_info:
            canonical_slug(vector["input"])
        assert exc_info.value.reason == vector["reason"]


class TestCorpusRejectReserved:
    """Inputs that MUST raise ReservedSlug with the expected reserved_name."""

    @pytest.mark.parametrize(
        "vector",
        _load_corpus()["reject_reserved"],
        ids=lambda v: f"{v['input']!r}->{v['reserved_name']!r}",
    )
    def test_raises_reserved_slug(self, vector: dict) -> None:
        with pytest.raises(ReservedSlug) as exc_info:
            canonical_slug(vector["input"])
        # ReservedSlug inherits InvalidSlug; verify both type and detail
        assert isinstance(exc_info.value, InvalidSlug)
        assert exc_info.value.details["reserved_name"] == vector["reserved_name"]


class TestCorpusRejectTooLong:
    """Inputs that MUST raise InvalidSlug('too_long')."""

    @pytest.mark.parametrize(
        "vector",
        _load_corpus()["reject_too_long"],
        ids=lambda v: f"{v['input_repeat_char']}*{v['repeat_count']}",
    )
    def test_raises_too_long(self, vector: dict) -> None:
        s = vector["input_repeat_char"] * vector["repeat_count"]
        with pytest.raises(InvalidSlug) as exc_info:
            canonical_slug(s)
        assert exc_info.value.reason == "too_long"


# -------- property / invariant tests --------

class TestProperties:
    def test_idempotence(self) -> None:
        """canonical_slug(canonical_slug(x)) == canonical_slug(x) for any valid x."""
        for raw in [
            "MycoSymbiotics Cooperative",
            "FIT Farms, Inc.",
            "Run-a-Muck!",
            "a",
            "42",
            "phantom-robotix",
        ]:
            once = canonical_slug(raw)
            twice = canonical_slug(once)
            assert once == twice, f"idempotence broken on {raw!r}"

    def test_output_charset_a_z_0_9_dash(self) -> None:
        """Every output character is in [a-z0-9-]."""
        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
        for raw in [
            "Regular Name",
            "CAPS_and_underscores",
            "punctuation!!! marks?",
            "hyphen-native",
            "42 is the answer",
        ]:
            out = canonical_slug(raw)
            assert set(out) <= allowed, f"forbidden char in {out!r}"

    def test_output_never_starts_or_ends_with_dash(self) -> None:
        for raw in [
            "---leading-dashes",
            "trailing-dashes---",
            "!!!(){}[]",
            "   spaces around   ",
            "-!-a-!-",
        ]:
            try:
                out = canonical_slug(raw)
            except InvalidSlug:
                continue
            assert not out.startswith("-")
            assert not out.endswith("-")

    def test_output_length_within_cap(self) -> None:
        """All valid outputs respect the 64-char cap."""
        for raw in [
            "short",
            "a-reasonable-length-organization-name",
            "under-the-cap-by-design-exactly-thirty-three",
        ]:
            out = canonical_slug(raw)
            assert 1 <= len(out) <= 64

    def test_case_insensitive(self) -> None:
        """Case variations of the same input produce the same slug."""
        assert canonical_slug("MYCO") == canonical_slug("myco") == canonical_slug("Myco")


# -------- v1 → v2 regression closures --------

class TestV2RegressionClosures:
    """Explicit tests for the v1 Red Team findings v2 closes."""

    def test_whitespace_padded_reserved_rejected(self) -> None:
        """v1 bug: ` .git ` was accepted as `.git`. v2 rejects."""
        with pytest.raises(ReservedSlug):
            canonical_slug(" .git ")
        with pytest.raises(ReservedSlug):
            canonical_slug("\t.git\t")
        with pytest.raises(ReservedSlug):
            canonical_slug("\n.git\n")

    def test_lossy_transliteration_rejected(self) -> None:
        """v1 bug: `café` silently became `cafe`. v2 rejects."""
        with pytest.raises(InvalidSlug) as exc_info:
            canonical_slug("café")
        assert exc_info.value.reason == "transliteration_lossy"
        assert exc_info.value.details["original"] == "café"

    def test_distinct_unicode_inputs_do_not_collapse(self) -> None:
        """Cornerstone invariant from the lossy-transliteration rule."""
        # If `café` were accepted as `cafe`, then `cafe` (pure ASCII)
        # would collide with it. v2 rejects `café` outright so no
        # collision is possible.
        assert canonical_slug("cafe") == "cafe"  # ASCII input passes
        with pytest.raises(InvalidSlug):
            canonical_slug("café")  # Unicode input rejected

    def test_angstrom_sign_rejected_rt_v1_h_01(self) -> None:
        """Round-A Committee RT-v1-H-01: U+212B ANGSTROM SIGN must reject.

        The earlier "post-NFKD non-ASCII + shrink" rule failed on inputs
        that NFKD-decompose directly to pure ASCII with no combining-mark
        residue. ANGSTROM SIGN U+212B → NFKD → "A" (length 1, pure ASCII),
        so the shrink check returned False and the input was silently
        accepted as slug "a" — colliding with any org legitimately named
        "A".

        v3 rule rejects any non-ASCII in the NFC form outright.
        """
        # Pure ASCII "A" is accepted.
        assert canonical_slug("A") == "a"
        # Å (U+212B ANGSTROM SIGN) is rejected — would otherwise collide.
        with pytest.raises(InvalidSlug) as exc_info:
            canonical_slug("\u212b")
        assert exc_info.value.reason == "transliteration_lossy"

    def test_various_unicode_homoglyphs_rejected_rt_v1_h_01(self) -> None:
        """Round-A Committee RT-v1-H-01 extended coverage."""
        # BLACK-LETTER CAPITAL H (U+210C) → NFKD → "H"
        with pytest.raises(InvalidSlug):
            canonical_slug("\u210c")
        # MICRO SIGN (U+00B5) → NFKD → Greek mu (U+03BC) → drops in ASCII
        with pytest.raises(InvalidSlug):
            canonical_slug("\u00b5")
        # MODIFIER LETTER APOSTROPHE (U+02BC) — visually identical to ASCII '
        with pytest.raises(InvalidSlug):
            canonical_slug("\u02bc")


# -------- type-safety at public surface --------

class TestTypeSafety:
    def test_rejects_int(self) -> None:
        with pytest.raises(TypeError):
            canonical_slug(42)  # type: ignore[arg-type]

    def test_rejects_bytes(self) -> None:
        with pytest.raises(TypeError):
            canonical_slug(b"bytes-slug")  # type: ignore[arg-type]

    def test_rejects_none(self) -> None:
        with pytest.raises(TypeError):
            canonical_slug(None)  # type: ignore[arg-type]


# -------- ensure_slug_available --------

class TestEnsureSlugAvailable:
    def test_passes_when_slug_not_allocated(self, tmp_path: Path) -> None:
        # tmp_path has no orgs/ yet — any slug is available
        (tmp_path / "orgs").mkdir()
        # should not raise
        ensure_slug_available("fit-farms", tmp_path)

    def test_raises_when_slug_exists(self, tmp_path: Path) -> None:
        (tmp_path / "orgs" / "fit-farms").mkdir(parents=True)
        with pytest.raises(SlugCollisionError) as exc_info:
            ensure_slug_available("fit-farms", tmp_path)
        assert exc_info.value.slug == "fit-farms"
        assert exc_info.value.existing_path.name == "fit-farms"

    def test_rejects_non_string_slug(self, tmp_path: Path) -> None:
        with pytest.raises(TypeError):
            ensure_slug_available(42, tmp_path)  # type: ignore[arg-type]

    def test_rejects_non_path_repo_root(self) -> None:
        with pytest.raises(TypeError):
            ensure_slug_available("slug", "/not/a/path/obj")  # type: ignore[arg-type]
