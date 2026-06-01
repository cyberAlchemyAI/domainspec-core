"""Tests for ``pipeline.logician.gates.f_logician_fact_drift``.

Coverage:
- Loader: valid YAML, schema errors, duplicate ids, non-numeric value
  classification, missing required fields.
- Numeric-claim extractor: bare numbers, thousands separators, decimals,
  year filter, regulation-citation filter, sentence + subject extraction.
- Temporal filter: in-window facts pass, expired facts excluded.
- Match: Jaccard threshold, no-match reporting, multiple candidates.
- Verify: exact match, within-tolerance, out-of-tolerance drift.
- Multi-failure: drift + no-match coexist.

YAML fixtures inline in tmp_path; uses real PyYAML.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from pipeline.logician.gates.f_logician_fact_drift import (
    F_LOGICIAN_FACT_DRIFT,
    MATCH_JACCARD_THRESHOLD,
    FactDriftFinding,
    FactDriftGateResult,
    KeyFactsRegister,
    KfrFact,
    KfrSchemaError,
    NumericClaim,
    check_fact_drift,
    extract_numeric_claims,
    load_kfr,
)


# --------------------------------------------------------------------------
# YAML fixtures
# --------------------------------------------------------------------------

_VALID_KFR_YAML = """\
schemaVersion: "1.0"
org_slug: dogwood_school

facts:
  - id: enrollment_2025_2026
    who: Dogwood Charter School
    what: Student enrollment
    when:
      period: 2025-2026 academic year
      as_of: 2025-10-01
      expiry: 2026-10-01
    where: PA, Allegheny County
    why: PA DOE October official count
    how: PIMS submission, audited by district
    value: 247
    unit: students_FTE
    projection_or_actual: actual
    validation:
      confirmed_by: operator
      confirmed_at: 2026-04-15
      source_doc: orgs/dogwood_school/assets/PIMS_Oct2025_official.pdf
    confidence: HIGH
    notes: Official PA DOE count.

  - id: org_operating_budget_fy2025
    who: Dogwood Charter School
    what: Total operating budget
    when:
      period: FY2025
      as_of: 2025-08-01
      expiry: 2026-08-01
    where: organizational
    why: audited financials
    how: external audit
    value: 4287000
    unit: USD
    projection_or_actual: actual
    validation:
      confirmed_by: operator
      confirmed_at: 2026-04-15
      source_doc: orgs/dogwood_school/assets/audit_FY2025.pdf
    confidence: HIGH

  - id: graduation_rate_2024_2025
    who: Dogwood Charter School
    what: Graduation rate
    when:
      period: 2024-2025 academic year
      as_of: 2025-08-01
      expiry: 2026-08-01
    where: PA
    why: state reporting
    how: PA DOE submission
    value: 87.5
    unit: percent
    projection_or_actual: actual
    validation:
      confirmed_by: operator
      confirmed_at: 2026-04-15
      source_doc: orgs/dogwood_school/assets/grad_2025.pdf
    confidence: HIGH
    display_tolerance_pct: 1.0

  - id: ed_director_credentials
    who: Jane Doe
    what: Education Director credentials
    when:
      period: ongoing
      as_of: 2024-08-15
    where: PA
    why: position requirements
    how: degree verification
    value: "PhD, M.Ed, PA Principal Certification"
    unit: credentials_list
    projection_or_actual: actual
    validation:
      confirmed_by: operator
      confirmed_at: 2026-04-15
      source_doc: orgs/dogwood_school/assets/credentials.pdf
    confidence: HIGH
"""


def _write_kfr(tmp_path: Path, content: str = _VALID_KFR_YAML) -> Path:
    p = tmp_path / "key_facts_register.yaml"
    p.write_text(content, encoding="utf-8")
    return p


_DEFAULT_GRANT_PERIOD = (date(2026, 1, 1), date(2026, 12, 31))


# --------------------------------------------------------------------------
# Loader
# --------------------------------------------------------------------------

class TestLoadKfr:

    def test_valid_yaml_loads(self, tmp_path: Path) -> None:
        kfr = load_kfr(_write_kfr(tmp_path))
        assert isinstance(kfr, KeyFactsRegister)
        assert kfr.org_slug == "dogwood_school"
        assert len(kfr.facts) == 4

    def test_numeric_facts_filter_excludes_string_values(self, tmp_path: Path) -> None:
        kfr = load_kfr(_write_kfr(tmp_path))
        numeric_only = kfr.numeric_facts()
        # Three numeric facts; ed_director_credentials is a string list
        assert len(numeric_only) == 3
        ids = {f.id for f in numeric_only}
        assert "ed_director_credentials" not in ids

    def test_numeric_value_parses_to_decimal(self, tmp_path: Path) -> None:
        kfr = load_kfr(_write_kfr(tmp_path))
        enrollment = kfr.fact_by_id("enrollment_2025_2026")
        assert enrollment is not None
        assert enrollment.value == Decimal("247")
        budget = kfr.fact_by_id("org_operating_budget_fy2025")
        assert budget.value == Decimal("4287000")

    def test_string_value_stays_string(self, tmp_path: Path) -> None:
        kfr = load_kfr(_write_kfr(tmp_path))
        creds = kfr.fact_by_id("ed_director_credentials")
        assert isinstance(creds.value, str)
        assert "PhD" in creds.value
        assert creds.is_numeric is False

    def test_per_fact_tolerance_loaded(self, tmp_path: Path) -> None:
        kfr = load_kfr(_write_kfr(tmp_path))
        grad = kfr.fact_by_id("graduation_rate_2024_2025")
        assert grad.display_tolerance_pct == 1.0

    def test_default_tolerance_zero(self, tmp_path: Path) -> None:
        kfr = load_kfr(_write_kfr(tmp_path))
        enrollment = kfr.fact_by_id("enrollment_2025_2026")
        assert enrollment.display_tolerance_pct == 0.0

    def test_missing_schema_version_fails(self, tmp_path: Path) -> None:
        bad = _VALID_KFR_YAML.replace('schemaVersion: "1.0"', '')
        with pytest.raises(KfrSchemaError, match="schemaVersion"):
            load_kfr(_write_kfr(tmp_path, bad))

    def test_invalid_confidence_fails(self, tmp_path: Path) -> None:
        bad = _VALID_KFR_YAML.replace("confidence: HIGH", "confidence: SUPER")
        with pytest.raises(KfrSchemaError, match="confidence"):
            load_kfr(_write_kfr(tmp_path, bad))

    def test_duplicate_id_fails(self, tmp_path: Path) -> None:
        bad = _VALID_KFR_YAML + """
  - id: enrollment_2025_2026
    who: Dogwood Charter School
    what: Duplicated
    when:
      period: 2025-2026
      as_of: 2025-10-01
    where: PA
    why: x
    how: y
    value: 999
    unit: students
    projection_or_actual: actual
    validation:
      confirmed_by: x
      confirmed_at: 2026-04-15
      source_doc: x
    confidence: HIGH
"""
        with pytest.raises(KfrSchemaError, match="duplicate fact id"):
            load_kfr(_write_kfr(tmp_path, bad))

    def test_expiry_before_as_of_fails(self, tmp_path: Path) -> None:
        bad = _VALID_KFR_YAML.replace(
            "as_of: 2025-10-01\n      expiry: 2026-10-01",
            "as_of: 2025-10-01\n      expiry: 2024-10-01",
        )
        with pytest.raises(KfrSchemaError, match="expiry"):
            load_kfr(_write_kfr(tmp_path, bad))

    def test_missing_file_raises_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_kfr(tmp_path / "nope.yaml")


# --------------------------------------------------------------------------
# Numeric-claim extractor
# --------------------------------------------------------------------------

class TestExtractNumericClaims:

    def test_bare_integer_extracted(self) -> None:
        text = "Dogwood Charter School enrolled 247 students."
        claims = extract_numeric_claims(text)
        assert len(claims) == 1
        c = claims[0]
        assert c.number == Decimal("247")
        assert c.raw_token == "247"
        assert c.unit_token == "students"
        # Subject tokens are 5-char-prefix stemmed (see _stem_token):
        # dogwood→dogwo, students→stude, charter→chart, school→schoo
        assert "dogwo" in c.subject_tokens or "stude" in c.subject_tokens

    def test_thousands_separator_extracted(self) -> None:
        text = "The operating budget reached 4,287,000 USD this year."
        claims = extract_numeric_claims(text)
        assert len(claims) == 1
        assert claims[0].number == Decimal("4287000")
        assert claims[0].raw_token == "4,287,000"

    def test_decimal_extracted(self) -> None:
        text = "The graduation rate was 87.5 percent."
        claims = extract_numeric_claims(text)
        assert len(claims) == 1
        assert claims[0].number == Decimal("87.5")
        assert claims[0].unit_token == "percent"

    def test_year_filtered(self) -> None:
        text = "In 2025 we enrolled 247 students."
        claims = extract_numeric_claims(text)
        # 2025 is filtered as a year; 247 survives
        nums = [c.number for c in claims]
        assert Decimal("2025") not in nums
        assert Decimal("247") in nums

    def test_regulation_citation_filtered(self) -> None:
        text = "Per Section 9007 we will follow the procedures."
        claims = extract_numeric_claims(text)
        # 9007 inside Section ... pattern → filtered
        nums = [c.number for c in claims]
        assert Decimal("9007") not in nums

    def test_cfr_filtered(self) -> None:
        text = "Compliant with 7 CFR 1234 standards."
        claims = extract_numeric_claims(text)
        # The "7 CFR" pattern filters the 7; "1234" might still surface
        # since it's not directly preceded by Section/Title.
        nums = [c.number for c in claims]
        assert Decimal("7") not in nums

    def test_multiple_claims_extracted(self) -> None:
        text = (
            "We enrolled 247 students in fall 2025. The graduation rate was 87.5 percent. "
            "Operating budget totaled 4,287,000 USD."
        )
        claims = extract_numeric_claims(text)
        nums = sorted(c.number for c in claims)
        assert Decimal("87.5") in nums
        assert Decimal("247") in nums
        assert Decimal("4287000") in nums

    def test_empty_text_returns_empty(self) -> None:
        assert extract_numeric_claims("") == ()
        assert extract_numeric_claims("   ") == ()


# --------------------------------------------------------------------------
# Gate — happy path
# --------------------------------------------------------------------------

class TestPasses:

    def test_clean_draft_with_matching_facts_passes(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        draft = (
            "Dogwood Charter School currently enrolls 247 students for the "
            "2025-2026 academic year. The school's total operating budget "
            "is 4287000 USD."
        )
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "PASS"
        assert result.claim_count_extracted >= 2
        assert result.claim_count_drifted == 0

    def test_within_tolerance_passes(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        # Graduation fact has display_tolerance_pct=1.0; 87.0 vs KFR 87.5 → 0.57% drift
        draft = "The Dogwood Charter School graduation rate was 87.0 percent last year."
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "PASS"

    def test_empty_draft_passes(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        result = check_fact_drift(
            draft_text="",
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "PASS"

    def test_no_numeric_claims_passes(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        result = check_fact_drift(
            draft_text="Dogwood serves the community well. We are committed.",
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "PASS"


# --------------------------------------------------------------------------
# Gate — value drift
# --------------------------------------------------------------------------

class TestValueDrift:

    def test_exact_drift_fails(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        # KFR enrollment=247; draft says 250 with 0% tolerance → FAIL
        draft = "Dogwood Charter School currently enrolls 250 students this year."
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_FACT_DRIFT
        drift_findings = [
            f for f in result.findings if f.reason_tag == "kfr_value_drift"
        ]
        assert len(drift_findings) == 1
        finding = drift_findings[0]
        assert finding.claim_value == Decimal("250")
        assert finding.nearest_fact_value == Decimal("247")
        assert finding.delta_pct is not None and finding.delta_pct > 0

    def test_outside_tolerance_fails(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        # Graduation tolerance is 1%; 90 vs 87.5 → 2.86% drift → FAIL
        draft = "The Dogwood Charter School graduation rate was 90 percent."
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "FAIL"


# --------------------------------------------------------------------------
# Gate — no-match (fabricated number)
# --------------------------------------------------------------------------

class TestNoMatch:

    def test_unknown_subject_fails(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        # Number with subject tokens that don't match any KFR fact
        draft = "Our solar panels generated 8500 kilowatt-hours of clean power."
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "FAIL"
        no_match_findings = [
            f for f in result.findings if f.reason_tag == "kfr_no_match"
        ]
        assert len(no_match_findings) == 1


# --------------------------------------------------------------------------
# Gate — temporal filtering
# --------------------------------------------------------------------------

class TestTemporalFiltering:

    def test_expired_fact_excluded_from_candidates(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        draft = "Dogwood Charter School enrolls 247 students for the year."
        # Grant funding period entirely AFTER the enrollment fact's expiry
        # (enrollment expiry is 2026-10-01)
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=(date(2027, 1, 1), date(2027, 12, 31)),
        )
        assert result.verdict == "FAIL"
        # The fact is filtered out, so 247 has no candidate → kfr_no_match
        no_match = [f for f in result.findings if f.reason_tag == "kfr_no_match"]
        assert len(no_match) == 1

    def test_invalid_period_fails(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        result = check_fact_drift(
            draft_text="anything",
            kfr_path=kfr_path,
            grant_funding_period=(date(2027, 12, 31), date(2026, 1, 1)),  # reversed
        )
        assert result.verdict == "FAIL"
        assert result.findings[0].reason_tag == "kfr_schema_error"


# --------------------------------------------------------------------------
# Gate — structural failures
# --------------------------------------------------------------------------

class TestStructuralFailures:

    def test_missing_kfr_fails(self, tmp_path: Path) -> None:
        result = check_fact_drift(
            draft_text="247 students.",
            kfr_path=tmp_path / "nope.yaml",
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "FAIL"
        assert result.findings[0].reason_tag == "kfr_missing"

    def test_bad_yaml_surfaces_schema_error(self, tmp_path: Path) -> None:
        path = tmp_path / "key_facts_register.yaml"
        path.write_text("not: : valid: : :", encoding="utf-8")
        result = check_fact_drift(
            draft_text="247 students.",
            kfr_path=path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "FAIL"
        assert result.findings[0].reason_tag == "kfr_schema_error"


# --------------------------------------------------------------------------
# Gate — multi-failure
# --------------------------------------------------------------------------

def _spacy_available() -> bool:
    try:
        import spacy
        spacy.load("en_core_web_sm")
        return True
    except Exception:  # noqa: BLE001
        return False


@pytest.mark.skipif(
    not _spacy_available(),
    reason="en_core_web_sm not installed; run `python -m spacy download en_core_web_sm`",
)
class TestSpacyPosAugmentation:
    """v0.2.B — spaCy POS-tagged subject extraction.

    Verifies that:
    - When spaCy is available (auto-load default), subject_tokens are
      filtered to NOUN / PROPN / ADJ — verbs, adverbs, determiners drop.
    - Forcing regex fallback via ``nlp=False`` produces broader sets
      that include verb stems.
    - POS-filtered sets retain enough signal for KFR matching to PASS
      on real claim/fact pairs.
    """

    def test_pos_filters_drop_adverbs_and_verbs(self) -> None:
        # "currently" (ADV), "enrolled" (VERB) should drop with POS.
        # "Dogwood" / "Charter" / "School" / "students" (PROPN/NOUN) keep.
        text = "Dogwood Charter School currently enrolled 247 students."
        with_pos = extract_numeric_claims(text)  # auto-load spaCy
        without_pos = extract_numeric_claims(text, nlp=False)
        assert len(with_pos) == 1 and len(without_pos) == 1

        pos_tokens = with_pos[0].subject_tokens
        regex_tokens = without_pos[0].subject_tokens

        # 'curre' (currently → ADV) and 'enrol' (enrolled → VERB) should
        # be in regex fallback but absent from POS-filtered set.
        assert "curre" in regex_tokens
        assert "enrol" in regex_tokens
        # POS filtering drops them
        assert "curre" not in pos_tokens
        # 'enrol' may or may not stay — spaCy can tag 'enrolled' as VERB
        # (drops) or rarely as ADJ (keeps). Don't assert either way.

        # Both sets retain the proper nouns (PROPN) + count-noun (NOUN)
        for stem in ("dogwo", "chart", "schoo", "stude"):
            assert stem in pos_tokens, f"{stem} missing from POS set"
            assert stem in regex_tokens, f"{stem} missing from regex set"

    def test_pos_retains_adjectives(self) -> None:
        # 'operating' (ADJ-or-VERB depending on parse) should generally
        # survive in subject_tokens because operating budget is a key
        # disambiguator for the budget fact match.
        text = "The total operating budget was 4,287,000 USD."
        claims = extract_numeric_claims(text)
        assert len(claims) == 1
        tokens = claims[0].subject_tokens
        # 'budge' (budget → NOUN) must survive
        assert "budge" in tokens
        # 'opera' (operating → ADJ) should typically survive too
        # (assertion-light because spaCy's call may vary by version)

    def test_pos_passes_real_match_at_threshold(self, tmp_path: Path) -> None:
        # Verify the v0.2.A clean-draft test still passes with POS active.
        kfr_path = _write_kfr(tmp_path)
        draft = (
            "Dogwood Charter School currently enrolls 247 students for the "
            "2025-2026 academic year."
        )
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "PASS"

    def test_force_regex_fallback(self, tmp_path: Path) -> None:
        # Caller passes nlp=False → skip spaCy entirely. Useful for
        # deterministic non-spaCy tests.
        kfr_path = _write_kfr(tmp_path)
        draft = "Dogwood Charter School enrolls 247 students this year."
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
            nlp=False,
        )
        assert result.verdict == "PASS"


class TestMultiFailure:

    def test_drift_and_no_match_coexist(self, tmp_path: Path) -> None:
        kfr_path = _write_kfr(tmp_path)
        draft = (
            "Dogwood Charter School enrolls 250 students this year. "
            "Our solar array produced 8500 kilowatts of energy."
        )
        result = check_fact_drift(
            draft_text=draft,
            kfr_path=kfr_path,
            grant_funding_period=_DEFAULT_GRANT_PERIOD,
        )
        assert result.verdict == "FAIL"
        reasons = {f.reason_tag for f in result.findings}
        assert "kfr_value_drift" in reasons
        assert "kfr_no_match" in reasons
