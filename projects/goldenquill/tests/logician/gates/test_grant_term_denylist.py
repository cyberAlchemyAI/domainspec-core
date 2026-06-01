"""Tests for ``pipeline.logician.gates._grant_term_denylist``.

Verifies the four public predicates against starter denylist content:
- :func:`is_grant_concept_token` — programs / demographics / ag-concepts /
  generic-tech (not federal agencies)
- :func:`is_federal_agency` — US federal agency abbreviations
- :func:`is_regulation_citation` — Title/Section/CFR/USC/Pub-L/FY/RFA/501c
  regex patterns
- :func:`is_grant_domain_non_org` — union of concept_token + citation

Tests deliberately exercise:
- bare match (``VAPG``)
- punctuation-normalised match (``501(c)(3)`` → bare ``501c3``)
- multi-word match (``USDA NRCS``)
- false-positive guards (ordinary words, partial matches)
- empty / whitespace edge cases
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates._grant_term_denylist import (
    is_federal_agency,
    is_grant_concept_token,
    is_grant_domain_non_org,
    is_regulation_citation,
)


class TestIsGrantConceptToken:
    """Programs, demographics, ag-concepts, generic-tech — NOT federal agencies."""

    @pytest.mark.parametrize(
        "token",
        [
            # Programs
            "VAPG", "REAP", "EQIP", "SARE", "AFRI", "SCBGP", "WIOA",
            # Demographics / entity types
            "BIPOC", "MTVC", "SDA", "MWBE", "L3C",
            # Ag concepts
            "FSMA", "HACCP", "IPM", "ROC", "GAP",
            # Generic tech
            "API", "LLM", "OAuth", "JSON", "ESG", "ROI",
        ],
    )
    def test_bare_concept_matches(self, token: str) -> None:
        assert is_grant_concept_token(token) is True

    @pytest.mark.parametrize(
        "punctuated",
        [
            "501(c)(3)",
            "501 (c) (3)",
            "501(C)(6)",
        ],
    )
    def test_501c_punctuation_normalised(self, punctuated: str) -> None:
        assert is_grant_concept_token(punctuated) is True

    @pytest.mark.parametrize(
        "multi_word",
        [
            "VAPG REAP",   # two known programs
            "SDA MTVC",    # two demographics
            "AI ML",       # two generic-tech
        ],
    )
    def test_multi_word_all_known(self, multi_word: str) -> None:
        assert is_grant_concept_token(multi_word) is True

    def test_federal_agencies_not_in_concept_set(self) -> None:
        # Federal agencies live in a separate set; the consuming gate
        # decides policy. is_grant_concept_token must return False.
        for agency in ("USDA", "NIFA", "NRCS", "EPA", "SBA", "NSF"):
            assert is_grant_concept_token(agency) is False, agency

    @pytest.mark.parametrize(
        "non_match",
        [
            "Penn State Extension",
            "FIT Farms",
            "MycoSymbiotics",
            "Walton Family Foundation",
            "the cooperative",
            "regenerative agriculture",
        ],
    )
    def test_real_org_or_phrase_returns_false(self, non_match: str) -> None:
        assert is_grant_concept_token(non_match) is False

    @pytest.mark.parametrize("empty", ["", "   ", "\t\n"])
    def test_empty_input_returns_false(self, empty: str) -> None:
        assert is_grant_concept_token(empty) is False

    def test_partial_match_does_not_fire(self) -> None:
        # 'VAPGISH' is not VAPG; substring matching must not leak.
        assert is_grant_concept_token("VAPGISH") is False
        # 'BIPOC-led' is not bare BIPOC.
        assert is_grant_concept_token("BIPOC-led") is False


class TestIsFederalAgency:

    @pytest.mark.parametrize(
        "agency",
        ["USDA", "NIFA", "NRCS", "EPA", "SBA", "NSF", "FDA", "BLM", "USFS"],
    )
    def test_known_agencies(self, agency: str) -> None:
        assert is_federal_agency(agency) is True

    @pytest.mark.parametrize("compound", ["USDA NRCS", "USDA NIFA"])
    def test_multi_word_all_agencies(self, compound: str) -> None:
        assert is_federal_agency(compound) is True

    def test_program_not_agency(self) -> None:
        assert is_federal_agency("VAPG") is False
        assert is_federal_agency("EQIP") is False

    def test_real_org_not_agency(self) -> None:
        assert is_federal_agency("Penn State Extension") is False


class TestIsRegulationCitation:

    @pytest.mark.parametrize(
        "citation",
        [
            "Title VII",
            "Title IX of the Education Amendments",
            "Section 9007",
            "Subpart B",
            "Part 200",
            "Article III",
            "7 CFR 1.1",
            "2 CFR 200",
            "7 USC 6502",
            "7 U.S.C. 6502",
            "Pub. L. 117-58",
            "Public Law 117-58",
            "FY 2026",
            "FY26",
            "FY-2026",
            "RFA-26-001",
            "NOFO 26-001",
            "FOA-25-002",
            "BAA-2026-XX",
            "501(c)(3)",
            "501(c)(6)",
        ],
    )
    def test_citation_patterns(self, citation: str) -> None:
        assert is_regulation_citation(citation) is True

    @pytest.mark.parametrize(
        "non_citation",
        [
            "Title",          # bare prefix, no number/numeral
            "Section",
            "the section",
            "FYI",            # FY-prefix-collision but not a fiscal year
            "USDA",
            "regenerative",
            "",
        ],
    )
    def test_non_citations(self, non_citation: str) -> None:
        assert is_regulation_citation(non_citation) is False


class TestIsGrantDomainNonOrg:
    """Union convenience: concept_token OR regulation_citation, NOT agency."""

    def test_concept_passes_through(self) -> None:
        assert is_grant_domain_non_org("VAPG") is True
        assert is_grant_domain_non_org("LLM") is True

    def test_citation_passes_through(self) -> None:
        assert is_grant_domain_non_org("Title VII") is True
        assert is_grant_domain_non_org("7 CFR 1.1") is True

    def test_federal_agency_does_not_pass(self) -> None:
        # Agencies should flow through to the consuming gate's
        # PROJECT_CONTEXT check, not be silently skipped.
        assert is_grant_domain_non_org("USDA") is False
        assert is_grant_domain_non_org("NIFA") is False

    def test_real_org_does_not_pass(self) -> None:
        assert is_grant_domain_non_org("Penn State Extension") is False
        assert is_grant_domain_non_org("MycoSymbiotics") is False
