"""Tests for ``pipeline.logician.gates.f_logician_fabricated_org``.

Two-tier strategy:

1. **Injected-NER tests** — exercise gate logic with a stub `nlp` callable
   that returns canned ORG entities. Run unconditionally; verify denylist
   filtering, allowlist build, fuzzy match, federal-agency short-circuit,
   dependency-unavailable failure modes, sentence-context attachment.

2. **Real-spaCy smoke tests** — skipped when `en_core_web_sm` is not
   installed in the test env. Verify end-to-end NER extraction on a
   realistic Scribe-draft fragment.

Total tests run on every CI machine; spaCy-real tests run only where the
model is available.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from pipeline.logician.gates.f_logician_fabricated_org import (
    DEFAULT_ALLOWLIST_FIELDS,
    DEFAULT_FUZZY_THRESHOLD,
    F_LOGICIAN_FABRICATED_ORG,
    FabricatedOrgFinding,
    FabricatedOrgGateResult,
    build_org_allowlist,
    check_fabricated_orgs,
    extract_org_entities,
)


# --------------------------------------------------------------------------
# Test stubs — fake spaCy doc/ent shapes for injected-NER tests
# --------------------------------------------------------------------------

@dataclass
class _FakeEnt:
    text: str
    label_: str


@dataclass
class _FakeDoc:
    ents: list[_FakeEnt]


def _make_fake_nlp(ent_specs: list[tuple[str, str]]):
    """Return a stub `nlp(text)` callable that emits canned entities.

    `ent_specs` is a list of (text, label) tuples — e.g.
    [("Penn State Extension", "ORG"), ("USDA", "ORG"), ("Title VII", "ORG")].
    The stub ignores `text` and returns the same canned set every call —
    sufficient because each test passes a different stub.
    """
    ents = [_FakeEnt(text=t, label_=l) for t, l in ent_specs]
    doc = _FakeDoc(ents=ents)
    def nlp(_text: str) -> _FakeDoc:
        return doc
    return nlp


def _exact_ratio(a: str, b: str) -> float:
    """Stub rapidfuzz.fuzz.ratio: 100 on exact match, 0 otherwise.

    Sufficient for tests that don't exercise fuzzy bands. Tests that need
    partial-ratio behaviour build a richer stub inline.
    """
    return 100.0 if a == b else 0.0


# --------------------------------------------------------------------------
# build_org_allowlist
# --------------------------------------------------------------------------

class TestBuildOrgAllowlist:

    def test_picks_up_string_fields(self) -> None:
        ctx = {
            "applicant_name": "FIT Farms LLC",
            "fiscal_sponsor": "MycoSymbiotics Coop",
        }
        allow = build_org_allowlist(ctx)
        assert "fit farms llc" in allow
        assert "mycosymbiotics coop" in allow

    def test_walks_list_of_strings(self) -> None:
        ctx = {
            "partners": ["Penn State Extension", "Rodale Institute"],
        }
        allow = build_org_allowlist(ctx)
        assert "penn state extension" in allow
        assert "rodale institute" in allow

    def test_walks_list_of_dicts_with_name(self) -> None:
        ctx = {
            "collaborators": [
                {"name": "USDA NRCS", "role": "technical-assistance"},
                {"organization": "Sustainable Ag Working Group"},
            ],
        }
        allow = build_org_allowlist(ctx)
        assert "usda nrcs" in allow
        assert "sustainable ag working group" in allow

    def test_rfa_issuer_added(self) -> None:
        allow = build_org_allowlist(
            {"applicant_name": "X"},
            rfa_issuer="USDA Rural Development",
        )
        assert "usda rural development" in allow

    def test_normalisation_strips_punctuation(self) -> None:
        ctx = {"applicant_name": "FIT Farms, LLC."}
        allow = build_org_allowlist(ctx)
        # Trailing comma + period stripped
        assert any("fit farms" in entry for entry in allow)

    def test_unknown_field_ignored(self) -> None:
        ctx = {
            "applicant_name": "X",
            "completely_unknown_field": "Y Org",
        }
        allow = build_org_allowlist(ctx)
        assert "y org" not in allow

    def test_custom_allowlist_fields(self) -> None:
        ctx = {
            "applicant_name": "DEFAULT_FIELD_PRESENT",
            "advisory_board": [{"name": "Custom Field Org"}],
        }
        # Default fields don't include 'advisory_board'
        allow = build_org_allowlist(ctx)
        assert "custom field org" not in allow
        # With custom fields tuple, it is picked up
        allow_custom = build_org_allowlist(
            ctx, fields=("applicant_name", "advisory_board")
        )
        assert "custom field org" in allow_custom


# --------------------------------------------------------------------------
# extract_org_entities (injected nlp)
# --------------------------------------------------------------------------

class TestExtractOrgEntities:

    def test_filters_only_org_entities(self) -> None:
        nlp = _make_fake_nlp([
            ("Penn State Extension", "ORG"),
            ("Pennsylvania", "GPE"),  # geo-political entity
            ("FIT Farms LLC", "ORG"),
            ("$200,000", "MONEY"),
        ])
        result = extract_org_entities("any text", nlp=nlp)
        assert result == ("Penn State Extension", "FIT Farms LLC")

    def test_empty_text_returns_empty_tuple(self) -> None:
        nlp = _make_fake_nlp([("ORG-Should-Not-Surface", "ORG")])
        result = extract_org_entities("", nlp=nlp)
        assert result == ()


# --------------------------------------------------------------------------
# check_fabricated_orgs — main entry point with injected deps
# --------------------------------------------------------------------------

class TestCheckFabricatedOrgsPasses:

    def test_empty_draft_passes(self) -> None:
        result = check_fabricated_orgs(
            draft_text="",
            project_context={"applicant_name": "X"},
        )
        assert result.verdict == "PASS"

    def test_whitespace_only_draft_passes(self) -> None:
        result = check_fabricated_orgs(
            draft_text="   \n\t  ",
            project_context={"applicant_name": "X"},
        )
        assert result.verdict == "PASS"

    def test_no_org_entities_passes(self) -> None:
        nlp = _make_fake_nlp([])  # no ORGs at all
        result = check_fabricated_orgs(
            draft_text="A draft with no organizations mentioned.",
            project_context={"applicant_name": "X"},
            nlp=nlp,
            ratio_fn=_exact_ratio,
        )
        assert result.verdict == "PASS"
        assert result.org_count_extracted == 0

    def test_all_orgs_in_allowlist_passes(self) -> None:
        nlp = _make_fake_nlp([
            ("Penn State Extension", "ORG"),
            ("FIT Farms LLC", "ORG"),
        ])
        ctx = {
            "applicant_name": "FIT Farms LLC",
            "partners": ["Penn State Extension"],
        }
        result = check_fabricated_orgs(
            draft_text="In partnership with Penn State Extension and FIT Farms LLC.",
            project_context=ctx,
            nlp=nlp,
            ratio_fn=_exact_ratio,
        )
        assert result.verdict == "PASS"
        assert result.org_count_extracted == 2
        assert result.org_count_after_denylist == 2
        assert result.org_count_ungrounded == 0

    def test_concept_tokens_filtered_by_denylist(self) -> None:
        # spaCy mistakenly tags VAPG, LLM, Title VII as ORG. Denylist
        # filters them out *before* allowlist check, so they don't
        # require PROJECT_CONTEXT membership.
        nlp = _make_fake_nlp([
            ("VAPG", "ORG"),
            ("Title VII", "ORG"),
            ("LLM", "ORG"),
        ])
        result = check_fabricated_orgs(
            draft_text="Pursuant to Title VII the VAPG funded LLM-driven outreach.",
            project_context={"applicant_name": "X"},  # no orgs in allowlist
            nlp=nlp,
            ratio_fn=_exact_ratio,
        )
        assert result.verdict == "PASS"
        assert result.org_count_extracted == 3
        assert result.org_count_after_denylist == 0  # all filtered

    def test_federal_agency_auto_allowed(self) -> None:
        nlp = _make_fake_nlp([("USDA", "ORG"), ("NIFA", "ORG")])
        result = check_fabricated_orgs(
            draft_text="Funded by USDA NIFA.",
            project_context={"applicant_name": "X"},  # USDA/NIFA not declared
            nlp=nlp,
            ratio_fn=_exact_ratio,
        )
        # Federal agencies short-circuit allowlist check by default
        assert result.verdict == "PASS"

    def test_federal_agency_strict_mode_requires_declaration(self) -> None:
        nlp = _make_fake_nlp([("USDA", "ORG")])
        result = check_fabricated_orgs(
            draft_text="The USDA approved this.",
            project_context={"applicant_name": "X"},
            nlp=nlp,
            ratio_fn=_exact_ratio,
            auto_allow_federal_agencies=False,  # strict
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_FABRICATED_ORG

    def test_rfa_issuer_added_to_allowlist(self) -> None:
        nlp = _make_fake_nlp([("USDA Rural Development", "ORG")])
        # auto_allow_federal_agencies=False so we know rfa_issuer is what
        # gets the org through (not the auto-allow shortcut).
        result = check_fabricated_orgs(
            draft_text="From USDA Rural Development.",
            project_context={"applicant_name": "X"},
            rfa_issuer="USDA Rural Development",
            nlp=nlp,
            ratio_fn=_exact_ratio,
            auto_allow_federal_agencies=False,
        )
        assert result.verdict == "PASS"


class TestCheckFabricatedOrgsFails:

    def test_fabricated_partnership_fails(self) -> None:
        nlp = _make_fake_nlp([("Made-Up Org", "ORG")])
        result = check_fabricated_orgs(
            draft_text="In partnership with Made-Up Org we will...",
            project_context={"applicant_name": "FIT Farms LLC"},
            nlp=nlp,
            ratio_fn=_exact_ratio,
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_FABRICATED_ORG
        assert result.reason_tag == "fabricated_org_detected"
        assert result.org_count_ungrounded == 1
        assert len(result.findings) == 1
        assert result.findings[0].org_name == "Made-Up Org"

    def test_finding_attaches_sentence_context(self) -> None:
        nlp = _make_fake_nlp([("Made-Up Org", "ORG")])
        draft = (
            "Project background. We work with Made-Up Org on outreach. "
            "Other content here."
        )
        result = check_fabricated_orgs(
            draft_text=draft,
            project_context={"applicant_name": "X"},
            nlp=nlp,
            ratio_fn=_exact_ratio,
        )
        assert result.verdict == "FAIL"
        assert "Made-Up Org" in result.findings[0].sentence_context

    def test_multiple_fabrications_all_reported(self) -> None:
        nlp = _make_fake_nlp([
            ("Made-Up Org", "ORG"),
            ("Another Fake Org", "ORG"),
        ])
        result = check_fabricated_orgs(
            draft_text=(
                "Made-Up Org agreed. Another Fake Org also signed on."
            ),
            project_context={"applicant_name": "X"},
            nlp=nlp,
            ratio_fn=_exact_ratio,
        )
        assert result.verdict == "FAIL"
        assert result.org_count_ungrounded == 2
        names = {f.org_name for f in result.findings}
        assert names == {"Made-Up Org", "Another Fake Org"}


class TestFuzzyMatching:

    def test_minor_misspelling_passes_above_threshold(self) -> None:
        # Stub ratio fn returns 90 for the misspelling pair, 0 elsewhere
        def fuzzy_ratio(a: str, b: str) -> float:
            if "penn state" in a and "penn state" in b:
                return 90.0  # > 85 threshold → PASS
            return 0.0

        nlp = _make_fake_nlp([("Penn State Extention", "ORG")])  # typo
        result = check_fabricated_orgs(
            draft_text="In partnership with Penn State Extention.",
            project_context={"partners": ["Penn State Extension"]},
            nlp=nlp,
            ratio_fn=fuzzy_ratio,
        )
        assert result.verdict == "PASS"

    def test_low_ratio_below_threshold_fails(self) -> None:
        def fuzzy_ratio(a: str, b: str) -> float:
            return 70.0  # below 85 default

        nlp = _make_fake_nlp([("Made-Up Org", "ORG")])
        result = check_fabricated_orgs(
            draft_text="With Made-Up Org we partner.",
            project_context={"partners": ["Real Different Org"]},
            nlp=nlp,
            ratio_fn=fuzzy_ratio,
        )
        assert result.verdict == "FAIL"
        # Nearest-match recorded since ratio > 0.5
        finding = result.findings[0]
        assert finding.nearest_match == "real different org"
        assert finding.match_ratio == 0.7

    def test_threshold_override(self) -> None:
        def fuzzy_ratio(a: str, b: str) -> float:
            return 80.0  # below 0.85 default, above 0.75

        nlp = _make_fake_nlp([("Some Org", "ORG")])
        # With strict 0.85: FAIL
        strict_result = check_fabricated_orgs(
            draft_text="Some Org partners with us.",
            project_context={"partners": ["Some Org Variant"]},
            nlp=nlp,
            ratio_fn=fuzzy_ratio,
            fuzzy_threshold=0.85,
        )
        assert strict_result.verdict == "FAIL"

        # With relaxed 0.75: PASS
        relaxed_result = check_fabricated_orgs(
            draft_text="Some Org partners with us.",
            project_context={"partners": ["Some Org Variant"]},
            nlp=nlp,
            ratio_fn=fuzzy_ratio,
            fuzzy_threshold=0.75,
        )
        assert relaxed_result.verdict == "PASS"


# --------------------------------------------------------------------------
# Dependency-unavailable failure modes
# --------------------------------------------------------------------------

class TestDependencyFailureModes:

    def test_real_spacy_unavailable_fails_closed(self, monkeypatch) -> None:
        # Force the lazy loader to report spaCy missing
        from pipeline.logician.gates import f_logician_fabricated_org as mod
        monkeypatch.setattr(mod, "_NLP_CACHE", [None])
        monkeypatch.setattr(mod, "_NLP_LOAD_ERROR", [None])

        def _broken_load() -> tuple[Any, str]:
            return None, "spacy not installed: ImportError(...)"

        monkeypatch.setattr(mod, "_try_load_spacy", _broken_load)

        result = check_fabricated_orgs(
            draft_text="Some text mentioning Acme Corp.",
            project_context={"applicant_name": "X"},
            ratio_fn=_exact_ratio,
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_FABRICATED_ORG
        assert result.reason_tag == "dependency_unavailable"
        assert result.dependency_error is not None
        assert "spacy not installed" in result.dependency_error

    def test_real_rapidfuzz_unavailable_fails_closed(self, monkeypatch) -> None:
        from pipeline.logician.gates import f_logician_fabricated_org as mod
        nlp = _make_fake_nlp([("Acme Corp", "ORG")])

        def _broken_rf() -> tuple[Any, str]:
            return None, "rapidfuzz not installed: ImportError(...)"

        monkeypatch.setattr(mod, "_try_import_rapidfuzz", _broken_rf)

        result = check_fabricated_orgs(
            draft_text="Acme Corp partners with us.",
            project_context={"applicant_name": "X"},
            nlp=nlp,
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_FABRICATED_ORG
        assert result.reason_tag == "dependency_unavailable"
        assert "rapidfuzz" in result.dependency_error


# --------------------------------------------------------------------------
# Real-spaCy smoke test (skipped when model unavailable)
# --------------------------------------------------------------------------

def _spacy_model_available() -> bool:
    try:
        import spacy
        spacy.load("en_core_web_sm")
        return True
    except Exception:  # noqa: BLE001
        return False


@pytest.mark.skipif(
    not _spacy_model_available(),
    reason="en_core_web_sm not installed; run `python -m spacy download en_core_web_sm`",
)
class TestRealSpacy:
    """End-to-end smoke tests using the actual spaCy model + rapidfuzz."""

    def test_real_pipeline_passes_clean_draft(self) -> None:
        draft = (
            "FIT Farms LLC will lead the project in partnership with "
            "Penn State Extension. The work is funded by USDA Rural "
            "Development under VAPG."
        )
        ctx = {
            "applicant_name": "FIT Farms LLC",
            "partners": ["Penn State Extension"],
        }
        result = check_fabricated_orgs(
            draft_text=draft,
            project_context=ctx,
            rfa_issuer="USDA Rural Development",
        )
        assert result.verdict == "PASS"

    def test_real_pipeline_catches_fabrication(self) -> None:
        draft = (
            "FIT Farms LLC will lead the project in partnership with "
            "Imaginary Institute of Soil Sciences."
        )
        ctx = {
            "applicant_name": "FIT Farms LLC",
            "partners": [],  # Imaginary Institute deliberately absent
        }
        result = check_fabricated_orgs(
            draft_text=draft,
            project_context=ctx,
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_FABRICATED_ORG
        # The fabricated org appears in findings
        names_lower = {f.org_name.lower() for f in result.findings}
        assert any("imaginary" in n for n in names_lower), (
            f"Expected 'imaginary' in findings, got: {names_lower}"
        )
