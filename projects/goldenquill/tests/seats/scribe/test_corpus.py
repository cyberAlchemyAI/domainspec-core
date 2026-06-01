"""Corpus-driven tests for pipeline.seats.scribe.kgie.

Loads every JSON fixture under ``tests/corpus/scribe/v1/{pass,fail}/``, builds
the equivalent :class:`RfaExtractedRecord` + project_context mapping, and
asserts the KGIE predicate routes the fixture to its declared
``expected_status``.

Blueprint anchor: §7 Scribe v1.1.1 §7.4. Spec card:
`pipeline/engineering/spec_cards/section_07_scribe_round_1_types_and_kgie.md`.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from pipeline.seats.scribe.kgie import kgie_preflight
from pipeline.seats.scribe.types import (
    DateTimeWithTimezone,
    EvaluationCriterion,
    MatchRequirement,
    RfaExtractedRecord,
    SectionSpec,
)


CORPUS_ROOT = Path(__file__).parent.parent.parent / "corpus" / "scribe" / "v1"
FIXED_CLOCK = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)


def _parse_iso(s: str) -> datetime:
    # Python 3.11+ accepts "+00:00" directly; normalize trailing 'Z' for safety.
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _decimal_or_none(v):
    return Decimal(str(v)) if v is not None else None


def _fixture_to_rfa(rfa_dict: dict) -> RfaExtractedRecord:
    match = rfa_dict.get("match_requirement")
    match_req = None
    if match is not None:
        match_req = MatchRequirement(
            ratio_applicant_to_federal=Decimal(match["ratio_applicant_to_federal"]),
            cash_vs_in_kind=match["cash_vs_in_kind"],
            allowable_sources=tuple(match["allowable_sources"]),
        )
    criteria = tuple(
        EvaluationCriterion(
            criterion_name=c["criterion_name"],
            max_points=c["max_points"],
            sub_criteria=tuple(c.get("sub_criteria", ())),
        )
        for c in rfa_dict["evaluation_criteria"]
    )
    sections = tuple(
        SectionSpec(
            section_name=s["section_name"],
            section_order=s["section_order"],
            limit_kind=s["limit_kind"],
            limit_value=s["limit_value"],
            required_content_cues=tuple(s.get("required_content_cues", ())),
        )
        for s in rfa_dict["section_structure"]
    )
    return RfaExtractedRecord(
        program_name=rfa_dict["program_name"],
        cfda_or_aln=rfa_dict["cfda_or_aln"],
        eligible_applicant_types=tuple(rfa_dict["eligible_applicant_types"]),
        eligible_project_activities=tuple(rfa_dict["eligible_project_activities"]),
        award_ceiling=_decimal_or_none(rfa_dict["award_ceiling"]),
        award_floor=_decimal_or_none(rfa_dict["award_floor"]),
        match_requirement=match_req,
        deadline=DateTimeWithTimezone(
            datetime=_parse_iso(rfa_dict["deadline_iso"])
        ),
        evaluation_criteria=criteria,
        section_structure=sections,
        required_attachments=tuple(rfa_dict["required_attachments"]),
        key_terms=dict(rfa_dict["key_terms"]),
        rfa_content_sha3_512=rfa_dict["rfa_content_sha3_512"],
        extracted_at_utc=_parse_iso(rfa_dict["extracted_at_iso"]),
    )


def _collect_fixture_paths() -> list[Path]:
    return sorted(CORPUS_ROOT.glob("**/*.json"))


@pytest.mark.parametrize(
    "fixture_path",
    _collect_fixture_paths(),
    ids=lambda p: f"{p.parent.name}/{p.stem}",
)
def test_fixture_routes_to_expected_status(fixture_path: Path):
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    rfa = _fixture_to_rfa(data["rfa"])
    pc = data["project_context"]
    affirmations = data["operator_affirmations"]
    expected = data["expected_status"]

    result = kgie_preflight(rfa, pc, affirmations, clock=lambda: FIXED_CLOCK)

    assert result.status == expected, (
        f"Fixture {fixture_path.name} expected status={expected!r}, "
        f"got {result.status!r}; needed_fields={result.needed_fields}"
    )

    # If fixture declares expected_needed_field_prefixes, verify each appears.
    prefixes = data.get("expected_needed_field_prefixes", [])
    for prefix in prefixes:
        assert any(n.startswith(prefix) for n in result.needed_fields), (
            f"Fixture {fixture_path.name}: expected a needed_field starting "
            f"with {prefix!r}; got {result.needed_fields}"
        )


def test_corpus_has_minimum_coverage():
    """Spec card §8 Done Definition: ≥2 pass + ≥3 fail fixtures."""
    pass_fixtures = list((CORPUS_ROOT / "pass").glob("*.json"))
    fail_fixtures = list((CORPUS_ROOT / "fail").glob("*.json"))
    assert len(pass_fixtures) >= 2, (
        f"Need ≥2 pass fixtures; found {len(pass_fixtures)}"
    )
    assert len(fail_fixtures) >= 3, (
        f"Need ≥3 fail fixtures; found {len(fail_fixtures)}"
    )
