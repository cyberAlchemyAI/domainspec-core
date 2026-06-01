"""Tests for pipeline.seats.scribe.program_templates — §7.9."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from pipeline.seats.scribe.program_templates import (
    KNOWN_PROGRAMS,
    ProgramTemplate,
    build_known_template,
    compute_template_sha3_512,
)


_FIXED = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)


def _fixed_clock() -> datetime:
    return _FIXED


_GOOD_SHA = "a" * 128


# ---------------------------------------------------------------------------
# compute_template_sha3_512
# ---------------------------------------------------------------------------


class TestComputeTemplateSha3512:
    def test_empty_bytes_valid(self) -> None:
        h = compute_template_sha3_512(b"")
        assert len(h) == 128
        assert all(c in "0123456789abcdef" for c in h)

    def test_deterministic(self) -> None:
        assert compute_template_sha3_512(b"abc") == compute_template_sha3_512(b"abc")

    def test_differs_per_input(self) -> None:
        assert compute_template_sha3_512(b"abc") != compute_template_sha3_512(b"abd")

    def test_bytearray_accepted(self) -> None:
        h = compute_template_sha3_512(bytearray(b"hello"))
        assert len(h) == 128

    def test_str_rejected(self) -> None:
        with pytest.raises(TypeError, match="bytes"):
            compute_template_sha3_512("not bytes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# KNOWN_PROGRAMS registry
# ---------------------------------------------------------------------------


class TestKnownProgramsRegistry:
    def test_eight_programs(self) -> None:
        assert len(KNOWN_PROGRAMS) == 8

    def test_expected_keys(self) -> None:
        assert set(KNOWN_PROGRAMS.keys()) == {
            "VAPG", "REAP", "SCBGP", "SARE", "SBIR", "AFRI", "2501", "UAIP",
        }

    def test_every_entry_has_cues_and_dialect(self) -> None:
        for code, entry in KNOWN_PROGRAMS.items():
            assert "required_content_cues" in entry
            assert "dialect_default" in entry
            cues = entry["required_content_cues"]
            assert isinstance(cues, tuple)
            assert len(cues) >= 1
            assert entry["dialect_default"] in (
                "conservative", "centrist", "progressive", "soul_fire",
            )

    def test_vapg_dialect_is_conservative(self) -> None:
        assert KNOWN_PROGRAMS["VAPG"]["dialect_default"] == "conservative"

    def test_sare_dialect_is_progressive(self) -> None:
        assert KNOWN_PROGRAMS["SARE"]["dialect_default"] == "progressive"

    def test_sbir_dialect_is_centrist(self) -> None:
        assert KNOWN_PROGRAMS["SBIR"]["dialect_default"] == "centrist"


# ---------------------------------------------------------------------------
# ProgramTemplate shape
# ---------------------------------------------------------------------------


class TestProgramTemplateShape:
    def test_happy_path(self) -> None:
        t = ProgramTemplate(
            program_code="VAPG",
            section_overrides={},
            required_content_cues=("feasibility study",),
            dialect_default="conservative",
            template_content_sha3_512=_GOOD_SHA,
            template_at_utc=_FIXED,
        )
        assert t.program_code == "VAPG"

    def test_is_frozen(self) -> None:
        t = ProgramTemplate(
            program_code="X",
            section_overrides={},
            required_content_cues=("c",),
            dialect_default="conservative",
            template_content_sha3_512=_GOOD_SHA,
            template_at_utc=_FIXED,
        )
        with pytest.raises(Exception):
            t.program_code = "Y"  # type: ignore[misc]

    def test_empty_program_code_rejected(self) -> None:
        with pytest.raises(ValueError, match="program_code"):
            ProgramTemplate(
                program_code="",
                section_overrides={},
                required_content_cues=("c",),
                dialect_default="conservative",
                template_content_sha3_512=_GOOD_SHA,
                template_at_utc=_FIXED,
            )

    def test_whitespace_program_code_rejected(self) -> None:
        with pytest.raises(ValueError, match="program_code"):
            ProgramTemplate(
                program_code="   ",
                section_overrides={},
                required_content_cues=("c",),
                dialect_default="conservative",
                template_content_sha3_512=_GOOD_SHA,
                template_at_utc=_FIXED,
            )

    def test_short_sha_rejected(self) -> None:
        with pytest.raises(ValueError, match="128"):
            ProgramTemplate(
                program_code="X",
                section_overrides={},
                required_content_cues=("c",),
                dialect_default="conservative",
                template_content_sha3_512="a" * 64,
                template_at_utc=_FIXED,
            )

    def test_uppercase_sha_rejected(self) -> None:
        with pytest.raises(ValueError, match="lowercase"):
            ProgramTemplate(
                program_code="X",
                section_overrides={},
                required_content_cues=("c",),
                dialect_default="conservative",
                template_content_sha3_512="A" * 128,
                template_at_utc=_FIXED,
            )

    def test_naive_template_at_rejected(self) -> None:
        with pytest.raises(ValueError, match="timezone-aware"):
            ProgramTemplate(
                program_code="X",
                section_overrides={},
                required_content_cues=("c",),
                dialect_default="conservative",
                template_content_sha3_512=_GOOD_SHA,
                template_at_utc=datetime(2026, 4, 21, 12, 0, 0),
            )

    def test_empty_cues_rejected(self) -> None:
        with pytest.raises(ValueError, match="required_content_cues"):
            ProgramTemplate(
                program_code="X",
                section_overrides={},
                required_content_cues=(),
                dialect_default="conservative",
                template_content_sha3_512=_GOOD_SHA,
                template_at_utc=_FIXED,
            )

    def test_section_overrides_frozen(self) -> None:
        import types as _types
        t = ProgramTemplate(
            program_code="X",
            section_overrides={},
            required_content_cues=("c",),
            dialect_default="conservative",
            template_content_sha3_512=_GOOD_SHA,
            template_at_utc=_FIXED,
        )
        assert isinstance(t.section_overrides, _types.MappingProxyType)


# ---------------------------------------------------------------------------
# build_known_template
# ---------------------------------------------------------------------------


class TestBuildKnownTemplate:
    def test_vapg_happy(self) -> None:
        t = build_known_template("VAPG", clock=_fixed_clock)
        assert t.program_code == "VAPG"
        assert t.dialect_default == "conservative"
        assert "feasibility study reference" in t.required_content_cues
        assert t.template_at_utc == _FIXED
        assert len(t.template_content_sha3_512) == 128

    def test_reap(self) -> None:
        t = build_known_template("REAP", clock=_fixed_clock)
        assert t.dialect_default == "conservative"
        assert any("energy" in c for c in t.required_content_cues)

    def test_sare_progressive(self) -> None:
        t = build_known_template("SARE", clock=_fixed_clock)
        assert t.dialect_default == "progressive"

    def test_sbir_centrist(self) -> None:
        t = build_known_template("SBIR", clock=_fixed_clock)
        assert t.dialect_default == "centrist"

    def test_2501_outreach(self) -> None:
        t = build_known_template("2501", clock=_fixed_clock)
        assert t.dialect_default == "progressive"

    def test_uaip_urban(self) -> None:
        t = build_known_template("UAIP", clock=_fixed_clock)
        assert t.dialect_default == "progressive"

    def test_sha_deterministic_per_code(self) -> None:
        t1 = build_known_template("VAPG", clock=_fixed_clock)
        t2 = build_known_template("VAPG", clock=_fixed_clock)
        assert t1.template_content_sha3_512 == t2.template_content_sha3_512

    def test_sha_differs_across_codes(self) -> None:
        shas = {
            code: build_known_template(code, clock=_fixed_clock).template_content_sha3_512
            for code in KNOWN_PROGRAMS
        }
        # 8 distinct shas
        assert len(set(shas.values())) == 8

    def test_unknown_code_raises(self) -> None:
        with pytest.raises(KeyError, match="Unknown program_code"):
            build_known_template("NOPE")

    def test_default_clock_is_utc(self) -> None:
        t = build_known_template("VAPG")
        assert t.template_at_utc.tzinfo == timezone.utc

    def test_all_known_buildable(self) -> None:
        for code in KNOWN_PROGRAMS:
            t = build_known_template(code, clock=_fixed_clock)
            assert t.program_code == code
