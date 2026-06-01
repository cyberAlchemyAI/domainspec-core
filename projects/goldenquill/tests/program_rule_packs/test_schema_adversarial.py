"""Adversarial tests for the Program Rule Pack JSON schema.

Captures every probe from the Red Team adversarial audit at
`pipeline/audits/prp_v0_1_red_team_audit_2026-05-17.md` so future regressions
cannot slip in silently. Two classes of test:

  - **HOLE-class probes** (14 cases): each constructs a malicious PRP body
    and asserts the schema rejects it. If any of these regresses, the
    schema has lost a Red-Team-driven hardening.
  - **LOADER-REALIZED probes** (6 cases): each constructs a body the schema
    CANNOT structurally reject (requires today's date, cross-PRP graph
    state, or per-property uniqueness across array items) and asserts the
    schema is correctly silent. These will move from
    test_schema_adversarial to test_loader_adversarial at v0.2 first wave
    when the F-PRP-* gate bodies graduate from NotImplementedError.

Also includes positive controls so the constraints don't over-tighten:

  - minimal-valid PRP body (BASE) passes
  - signed-runtime-loadable PRP with ed25519_signature passes
  - cross_cutting_regulation with funding_program_ref=null passes
  - cross_cutting_regulation with funding_program_ref omitted passes
  - compliance_framework with funding_program_ref=null passes

Run with:
  scripts/run_tests.sh tests/program_rule_packs/  # operator's venv (3.14)
  python3 -m pytest tests/program_rule_packs/    # sandbox (3.10)
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

# Optional dep: jsonschema. Skip the whole module if not installed.
jsonschema = pytest.importorskip("jsonschema")
from jsonschema import Draft202012Validator  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "pipeline" / "program_rule_packs" / "_schema" / "program_rule_pack.schema.json"


@pytest.fixture(scope="module")
def schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return json.load(f)


@pytest.fixture(scope="module")
def validator(schema: dict) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


@pytest.fixture
def base_prp() -> dict:
    """Minimal-valid PRP body. Every probe mutates a deepcopy of this.

    Updated post-R3-F2: program_specific PRPs now require a non-null
    expiry_date, so the fixture carries one. Tests that probe expiry_date
    semantics explicitly mutate or remove this field.
    """

    return {
        "schema_version": "1.0-prp",
        "prp_id": "TILTH-PRP-USDA-VAPG-FY26",
        "prp_kind": "program_specific",
        "funding_program_ref": {
            "program_name": "USDA Value-Added Producer Grant",
            "agency": "USDA Rural Development",
        },
        "display_name": "USDA Value-Added Producer Grant (VAPG) FY26",
        "effective_date": "2026-01-15",
        "expiry_date": "2027-06-30",
        "live_law_rules": [
            {
                "rule_id": "TILTH-PRP-USDA-VAPG-FY26-R01",
                "rule_type": "eligibility",
                "rule_summary": "Independent producer eligibility.",
                "source_citation": "USDA VAPG FY26 NOFO p.4",
            }
        ],
        "lifecycle": {
            "draft_status": "draft",
            "review_status": "pending",
            "signature_status": "unsigned",
            "runtime_load_status": "not_loaded",
            "runtime_loadable": False,
        },
        "_research_metadata": {
            "authored_at": "2026-05-17T22:30:00Z",
            "authored_by_role": "operator",
            "primary_sources": [
                {
                    "citation": "USDA VAPG FY26 NOFO",
                    "url_or_locator": "https://www.rd.usda.gov/programs-services/business-programs/value-added-producer-grants",
                    "accessed_date": "2026-05-17",
                }
            ],
            "last_verified_date": "2026-05-17",
        },
    }


# ---------------------------------------------------------------------------
# Positive controls — must PASS
# ---------------------------------------------------------------------------


def test_base_minimal_valid_prp_passes(validator: Draft202012Validator, base_prp: dict) -> None:
    errors = list(validator.iter_errors(base_prp))
    assert errors == [], f"base PRP failed validation: {[e.message for e in errors]}"


def test_signed_runtime_loadable_with_signature_passes(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["lifecycle"] = {
        "draft_status": "signed",
        "review_status": "passed",
        "signature_status": "signed",
        "runtime_load_status": "loaded",
        "runtime_loadable": True,
        "signed_at": "2026-06-01T12:00:00Z",
        "signed_by": "operator",
        "content_hash": "sha256:" + "0" * 64,
    }
    body["_research_metadata"]["ed25519_signature"] = "DEADBEEF" * 8
    errors = list(validator.iter_errors(body))
    assert errors == [], f"signed runtime PRP failed: {[e.message for e in errors]}"


@pytest.mark.parametrize("kind", ["cross_cutting_regulation", "compliance_framework"])
def test_non_program_specific_funding_ref_null_passes(
    validator: Draft202012Validator, base_prp: dict, kind: str
) -> None:
    body = copy.deepcopy(base_prp)
    body["prp_id"] = "TILTH-PRP-2CFR200" if kind == "cross_cutting_regulation" else "TILTH-PRP-FERPA-COPPA-HIPAA"
    body["prp_kind"] = kind
    body["funding_program_ref"] = None
    errors = list(validator.iter_errors(body))
    assert errors == [], f"{kind} with null funding_program_ref rejected: {[e.message for e in errors]}"


@pytest.mark.parametrize("kind", ["cross_cutting_regulation", "compliance_framework"])
def test_non_program_specific_funding_ref_omitted_passes(
    validator: Draft202012Validator, base_prp: dict, kind: str
) -> None:
    body = copy.deepcopy(base_prp)
    body["prp_id"] = "TILTH-PRP-2CFR200" if kind == "cross_cutting_regulation" else "TILTH-PRP-FERPA-COPPA-HIPAA"
    body["prp_kind"] = kind
    body.pop("funding_program_ref", None)
    errors = list(validator.iter_errors(body))
    assert errors == [], f"{kind} with omitted funding_program_ref rejected: {[e.message for e in errors]}"


# ---------------------------------------------------------------------------
# HOLE-class probes — must REJECT
#
# Each test corresponds to an audit-probe ID from
# pipeline/audits/prp_v0_1_red_team_audit_2026-05-17.md. If any of these tests
# starts to PASS in CI, the schema has lost a Red-Team-driven hardening.
# ---------------------------------------------------------------------------


def test_A1_cross_cutting_with_funding_program_ref_populated_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["prp_kind"] = "cross_cutting_regulation"
    assert list(validator.iter_errors(body)), "A1 regression: cross_cutting + funding_program_ref now passes"


def test_A2_rule_missing_summary_and_citation_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0] = {"rule_id": "X", "rule_type": "eligibility"}
    assert list(validator.iter_errors(body)), "A2 regression: rule without summary+citation now passes"


def test_A3_primary_source_url_empty_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["_research_metadata"]["primary_sources"][0]["url_or_locator"] = ""
    assert list(validator.iter_errors(body)), "A3 regression: empty url_or_locator now passes"


def test_A4_primary_source_missing_accessed_date_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["_research_metadata"]["primary_sources"][0].pop("accessed_date")
    assert list(validator.iter_errors(body)), "A4 regression: primary_source missing accessed_date now passes"


def test_A5_signed_without_ed25519_signature_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["lifecycle"] = {
        "draft_status": "signed",
        "review_status": "passed",
        "signature_status": "signed",
        "runtime_load_status": "loaded",
        "runtime_loadable": True,
        "signed_at": "2026-06-01T12:00:00Z",
        "signed_by": "operator",
        "content_hash": "sha256:" + "0" * 64,
    }
    # NOTE: ed25519_signature deliberately absent
    assert list(validator.iter_errors(body)), "A5 regression: signed PRP without ed25519_signature now passes"


@pytest.mark.parametrize(
    "field_name",
    [
        "clc_assignment",
        "cic_assignment",
        "cic_clc_matrix",
        "clc_cic_matrix",
        "clc_to_cic_eligibility",
        "cic_to_clc_eligibility",
        "cic_clc_coupling_matrix",
        "clc_to_cic_matrix",
        "cic_to_clc_matrix",
        "common_clc_patterns_observed",
        "eligible_clc_subset",
        "preferred_clcs",
        "preferred_cics",
        "private_member_roster",
        "private_org_underwriting_override",
        "tactical_interpretation",
    ],
)
def test_A6_top_level_coupling_field_rejected(
    validator: Draft202012Validator, base_prp: dict, field_name: str
) -> None:
    body = copy.deepcopy(base_prp)
    body[field_name] = "anything"
    assert list(validator.iter_errors(body)), (
        f"A6 regression: top-level {field_name} now passes — coupling field enumeration broken"
    )


def test_A7_coupling_field_nested_in_lifecycle_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["lifecycle"]["preferred_clcs"] = ["public_purpose_works"]
    assert list(validator.iter_errors(body)), "A7 regression: lifecycle.preferred_clcs now passes"


def test_A8_coupling_field_nested_in_research_metadata_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["_research_metadata"]["clc_allowlist"] = []
    assert list(validator.iter_errors(body)), "A8 regression: _research_metadata.clc_allowlist now passes"


def test_A13_lifecycle_cross_family_thesis_status_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["lifecycle"]["cross_family_thesis_status"] = "passed"
    assert list(validator.iter_errors(body)), (
        "A13 regression: lifecycle.cross_family_thesis_status now passes — this is a card-only lifecycle field"
    )


def test_A15_rule_source_citation_empty_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0]["source_citation"] = ""
    assert list(validator.iter_errors(body)), "A15 regression: empty source_citation now passes"


def test_A24_program_specific_with_null_funding_ref_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["prp_kind"] = "program_specific"
    body["funding_program_ref"] = None
    assert list(validator.iter_errors(body)), (
        "A24 regression: program_specific with null funding_program_ref now passes — cross-kind invariant broken"
    )


@pytest.mark.parametrize(
    "bad_date",
    [
        "01/15/2026",  # US format
        "15/01/2026",  # EU format
        "2026-1-15",  # missing zero-pad
        "Jan 15 2026",  # human readable
        "2026-15-01",  # YYYY-DD-MM — still matches pattern, only loader catches semantic at v0.2
    ],
)
def test_A25_non_iso_effective_date_rejected(
    validator: Draft202012Validator, base_prp: dict, bad_date: str
) -> None:
    body = copy.deepcopy(base_prp)
    body["effective_date"] = bad_date
    errors = list(validator.iter_errors(body))
    if bad_date == "2026-15-01":
        # This one structurally matches \d{4}-\d{2}-\d{2}; documented as
        # loader-realized semantic check, not schema-rejected here.
        # Test serves as a sentinel: if schema starts to reject this,
        # we've added a semantic month/day check — update the test.
        assert errors == [], "schema started rejecting 2026-15-01 — update test"
    else:
        assert errors, f"A25 regression: non-ISO date {bad_date!r} now passes"


def test_A12_prp_id_double_hyphen_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["prp_id"] = "TILTH-PRP--BAD"
    assert list(validator.iter_errors(body))


def test_A14_display_name_empty_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["display_name"] = ""
    assert list(validator.iter_errors(body))


def test_A22_live_law_rules_empty_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["live_law_rules"] = []
    assert list(validator.iter_errors(body))


def test_A23_rule_id_empty_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0]["rule_id"] = ""
    assert list(validator.iter_errors(body))


def test_A26_lifecycle_missing_runtime_loadable_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    del body["lifecycle"]["runtime_loadable"]
    assert list(validator.iter_errors(body))


# ---------------------------------------------------------------------------
# LOADER-REALIZED probes — must remain SILENT at schema layer
#
# These six invariants CANNOT be enforced by JSON Schema alone. They graduate
# to F-PRP-* loader gate bodies at v0.2 first wave. These tests serve as
# documentation: if a future schema change makes any of these structurally
# rejectable, the corresponding test should flip from "passes" to a new
# HOLE-class test under that semantic name.
# ---------------------------------------------------------------------------


def test_A16_tactical_interpretation_for_org_rejected_after_RT1_F1(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """A16 was originally classified LOADER-REALIZED because the schema could
    not enumerate every novel field name. RT1-F1 patternProperties on the
    Law-3 marker regex (tactical_for, tactical_interpretation, etc.) now
    catches this class structurally at schema layer. The test was authored
    with an explicit promotion-path comment; this is the promotion."""
    body = copy.deepcopy(base_prp)
    body["tactical_interpretation_for_fit_farms_llc"] = "VAPG R3 page-limit means..."
    assert list(validator.iter_errors(body)), (
        "A16 regression: schema stopped rejecting tactical_interpretation_for_<org>. "
        "RT1-F1 Law-3 patternProperties broken."
    )


def test_A17_large_live_law_rules_passes_at_schema(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Schema has no maxItems on live_law_rules; loader policy at v0.2."""
    body = copy.deepcopy(base_prp)
    body["live_law_rules"] = [
        {"rule_id": f"R-{i:04d}", "rule_type": "eligibility", "rule_summary": "x", "source_citation": "x"}
        for i in range(2000)  # 2k not 10k — keep test fast
    ]
    assert list(validator.iter_errors(body)) == []


def test_A18_signed_runtime_with_past_expiry_passes_at_schema(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Schema cannot check today's date against expiry_date. F-PRP-EXPIRED is loader-realized."""
    body = copy.deepcopy(base_prp)
    body["lifecycle"] = {
        "draft_status": "signed",
        "review_status": "passed",
        "signature_status": "signed",
        "runtime_load_status": "loaded",
        "runtime_loadable": True,
        "signed_at": "2026-06-01T12:00:00Z",
        "signed_by": "operator",
        "content_hash": "sha256:" + "0" * 64,
    }
    body["effective_date"] = "2020-01-01"
    body["expiry_date"] = "2020-12-31"
    body["_research_metadata"]["ed25519_signature"] = "DEADBEEF" * 8
    assert list(validator.iter_errors(body)) == []


def test_A19_cross_reference_self_passes_at_schema(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Schema cannot check referential identity. Loader walk at v0.2."""
    body = copy.deepcopy(base_prp)
    body["cross_references"] = [
        {"referenced_prp_id": body["prp_id"], "relationship": "supersedes"}
    ]
    assert list(validator.iter_errors(body)) == []


def test_A20_inverted_window_passes_at_schema(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Schema cannot compare two date fields. F-PRP-EXPIRED sub-tag at v0.2."""
    body = copy.deepcopy(base_prp)
    body["effective_date"] = "2030-01-01"
    body["expiry_date"] = "2026-01-01"
    assert list(validator.iter_errors(body)) == []


def test_A21_duplicate_rule_id_passes_at_schema(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """JSON Schema can't enforce per-property uniqueness across array items."""
    body = copy.deepcopy(base_prp)
    body["live_law_rules"] = [
        {"rule_id": "DUP-01", "rule_type": "eligibility", "rule_summary": "x", "source_citation": "x"},
        {"rule_id": "DUP-01", "rule_type": "deadline", "rule_summary": "y", "source_citation": "y"},
    ]
    assert list(validator.iter_errors(body)) == []


# ---------------------------------------------------------------------------
# Round 1 cross-family Red Team probes (groq/openai/gpt-oss-120b, 2026-05-17)
# Output: pipeline/validation/prp_v0_1_red_team_2026-05-17/red_team.md
#
# RT1-F1 CRITICAL: additionalProperties:true everywhere was a Law-3 backdoor.
# RT1-F2 HIGH: lifecycle.signed_at/signed_by/content_hash were [string,null]
#              even when runtime_loadable=true — null-bypass of signing chain.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "law3_key",
    [
        "internal_budget_breakdown",
        "private_member_data",
        "tactical_for_fit_farms_llc",
        "tactical_interpretation_for_some_org",
        "confidential_secret_amount",
        "underwriting_override_for_x",
        "client_specific_terms",
        "org_specific_data",
        "member_roster_2026",
        "internal_org_notes",
        "internal_budget_categories",
        "internal_financial_summary",
    ],
)
def test_RT1_F1_root_level_law3_key_rejected(
    validator: Draft202012Validator, base_prp: dict, law3_key: str
) -> None:
    """Red Team Round 1 Finding 1: top-level Law-3-marker key names must
    reject via patternProperties even though they aren't in the closed-set
    forbidden_coupling enumeration."""
    body = copy.deepcopy(base_prp)
    body[law3_key] = "anything"
    assert list(validator.iter_errors(body)), (
        f"RT1-F1 regression: top-level {law3_key} now passes — Law-3 patternProperties broken"
    )


@pytest.mark.parametrize(
    "container, law3_key",
    [
        ("live_law_rules_item", "private_budget_data"),
        ("live_law_rules_item", "tactical_for_client"),
        ("live_law_rules_item", "internal_org_override"),
    ],
)
def test_RT1_F1_nested_law3_key_in_live_law_rules_rejected(
    validator: Draft202012Validator, base_prp: dict, container: str, law3_key: str
) -> None:
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0][law3_key] = "x"
    assert list(validator.iter_errors(body)), (
        f"RT1-F1 nested regression: live_law_rules.items[0].{law3_key} now passes"
    )


def test_RT1_F1_nested_law3_key_in_cross_references_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["cross_references"] = [
        {
            "referenced_prp_id": "TILTH-PRP-2CFR200",
            "relationship": "inherits_from",
            "tactical_for_specific_client": "x",
        }
    ]
    assert list(validator.iter_errors(body)), (
        "RT1-F1 cross_references regression: nested tactical_for_specific_client now passes"
    )


def test_RT1_F1_arbitrary_field_in_lifecycle_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """lifecycle is now additionalProperties:false — any field beyond the
    declared 10 must reject. Defense in depth for RT1-F1."""
    body = copy.deepcopy(base_prp)
    body["lifecycle"]["arbitrary_field"] = "x"
    assert list(validator.iter_errors(body)), (
        "RT1-F1 lifecycle additionalProperties regression: arbitrary_field now passes"
    )


def test_RT1_F1_arbitrary_field_in_research_metadata_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """_research_metadata is now additionalProperties:false."""
    body = copy.deepcopy(base_prp)
    body["_research_metadata"]["arbitrary_field"] = "x"
    assert list(validator.iter_errors(body)), (
        "RT1-F1 _research_metadata additionalProperties regression: arbitrary_field now passes"
    )


def test_RT1_F1_arbitrary_field_in_funding_program_ref_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """funding_program_ref is now additionalProperties:false."""
    body = copy.deepcopy(base_prp)
    body["funding_program_ref"]["arbitrary_field"] = "x"
    assert list(validator.iter_errors(body)), (
        "RT1-F1 funding_program_ref additionalProperties regression: arbitrary_field now passes"
    )


def test_RT1_F2_null_lifecycle_fields_with_runtime_loadable_true_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Red Team Round 1 Finding 2: previously lifecycle.signed_at/signed_by/
    content_hash were declared as [string,null], and the runtime_loadable=true
    conditional only checked key presence. An adversary could pass with all
    three set to null. The fixed schema requires non-null strings in the
    conditional 'then' branch."""
    body = copy.deepcopy(base_prp)
    body["lifecycle"] = {
        "draft_status": "signed",
        "review_status": "passed",
        "signature_status": "signed",
        "runtime_load_status": "loaded",
        "runtime_loadable": True,
        "signed_at": None,
        "signed_by": None,
        "content_hash": None,
    }
    body["_research_metadata"]["ed25519_signature"] = "DEADBEEF" * 8
    assert list(validator.iter_errors(body)), (
        "RT1-F2 regression: null signed_at/signed_by/content_hash with runtime_loadable=true now passes"
    )


def test_RT1_F2_null_signed_at_only_with_runtime_loadable_true_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Partial null bypass — only one of three nulled."""
    body = copy.deepcopy(base_prp)
    body["lifecycle"] = {
        "draft_status": "signed",
        "review_status": "passed",
        "signature_status": "signed",
        "runtime_load_status": "loaded",
        "runtime_loadable": True,
        "signed_at": None,
        "signed_by": "operator",
        "content_hash": "sha256:" + "0" * 64,
    }
    body["_research_metadata"]["ed25519_signature"] = "DEADBEEF" * 8
    assert list(validator.iter_errors(body)), (
        "RT1-F2 partial regression: null signed_at-only with runtime_loadable=true now passes"
    )


def test_RT1_F2_empty_signed_at_string_with_runtime_loadable_true_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Empty-string bypass also blocked by minLength:1 in the conditional 'then'."""
    body = copy.deepcopy(base_prp)
    body["lifecycle"] = {
        "draft_status": "signed",
        "review_status": "passed",
        "signature_status": "signed",
        "runtime_load_status": "loaded",
        "runtime_loadable": True,
        "signed_at": "",
        "signed_by": "operator",
        "content_hash": "sha256:" + "0" * 64,
    }
    body["_research_metadata"]["ed25519_signature"] = "DEADBEEF" * 8
    assert list(validator.iter_errors(body)), (
        "RT1-F2 empty-string regression: empty signed_at with runtime_loadable=true now passes"
    )


# ---------------------------------------------------------------------------
# Round 2 cross-family findings (groq/openai/gpt-oss-120b + google/gemini-2.5-pro)
# Output: pipeline/validation/prp_v0_1_red_team_2026-05-17/round_2/{red_team,judge}.md
# Judge round-2 verdict: SPLIT, 72/100 (D2=10/25). Root additionalProperties:true
# was the dominant defect — R2-F1 + R2-F3 + R2-F5 all instantiate the same class.
#
# R2-F1 CRITICAL: root additionalProperties:true → benign-named Law-3 escapes
# R2-F2 CRITICAL: rule_body had no coupling/Law-3 guards
# R2-F3 HIGH:    Unicode/hyphen separator bypass of original regex
# R2-F4 MEDIUM:  whitespace-only signed_at/signed_by satisfied minLength:1
# R2-F5 CRITICAL: cross_references.items additionalProperties:true
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "benign_key",
    [
        "budget_info",
        "financials",
        "cost_breakdown",
        "risk_assessment",
        "arbitrary_random_field",
        "extra_metadata",
        "internal_notes",
    ],
)
def test_R2_F1_root_benign_extra_field_rejected(
    validator: Draft202012Validator, base_prp: dict, benign_key: str
) -> None:
    """Round 2 Finding 1: root additionalProperties:false now blocks ANY
    extra top-level key, including benign-named ones that don't trip the
    Law-3 patternProperties regex."""
    body = copy.deepcopy(base_prp)
    body[benign_key] = "anything"
    assert list(validator.iter_errors(body)), (
        f"R2-F1 regression: top-level {benign_key} now passes — root additionalProperties broken"
    )


def test_R2_F2_coupling_field_in_rule_body_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Round 2 Finding 2: rule_body now applies forbidden_coupling +
    forbidden_law3 guards, so coupling fields nested inside rule_body are
    rejected."""
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0]["rule_body"] = {"cic_assignment": "evil"}
    assert list(validator.iter_errors(body)), (
        "R2-F2 regression: cic_assignment in rule_body now passes"
    )


def test_R2_F2_law3_marker_in_rule_body_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0]["rule_body"] = {"private_member_payload": "x"}
    assert list(validator.iter_errors(body)), (
        "R2-F2 regression: private_member_payload in rule_body now passes"
    )


@pytest.mark.parametrize(
    "hyphen_key",
    [
        "internal-budget-breakdown",
        "private-client-data",
        "tactical-for-x",
    ],
)
def test_R2_F3_hyphen_separator_law3_marker_rejected(
    validator: Draft202012Validator, base_prp: dict, hyphen_key: str
) -> None:
    """Round 2 Finding 3: original regex used `(^|_)` separator class which
    missed hyphen-separated variants. Even if the regex misses, the root
    additionalProperties:false also catches arbitrary top-level keys —
    double defense."""
    body = copy.deepcopy(base_prp)
    body[hyphen_key] = "x"
    assert list(validator.iter_errors(body)), (
        f"R2-F3 regression: hyphen-separator {hyphen_key} now passes"
    )


def test_R2_F4_whitespace_only_signed_at_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Round 2 Finding 4: minLength:1 was satisfied by '   '. The conditional
    'then' branch now requires an ISO 8601 datetime pattern."""
    body = copy.deepcopy(base_prp)
    body["lifecycle"] = {
        "draft_status": "signed",
        "review_status": "passed",
        "signature_status": "signed",
        "runtime_load_status": "loaded",
        "runtime_loadable": True,
        "signed_at": "   ",
        "signed_by": "operator",
        "content_hash": "sha256:" + "0" * 64,
    }
    body["_research_metadata"]["ed25519_signature"] = "DEADBEEF" * 8
    assert list(validator.iter_errors(body)), (
        "R2-F4 regression: whitespace-only signed_at now passes"
    )


def test_R2_F4_whitespace_only_signed_by_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["lifecycle"] = {
        "draft_status": "signed",
        "review_status": "passed",
        "signature_status": "signed",
        "runtime_load_status": "loaded",
        "runtime_loadable": True,
        "signed_at": "2026-06-01T12:00:00Z",
        "signed_by": "   ",
        "content_hash": "sha256:" + "0" * 64,
    }
    body["_research_metadata"]["ed25519_signature"] = "DEADBEEF" * 8
    assert list(validator.iter_errors(body)), (
        "R2-F4 regression: whitespace-only signed_by now passes"
    )


def test_R2_F5_arbitrary_field_in_cross_references_item_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Round 2 Finding 5: cross_references.items is now additionalProperties:
    false. The 4 allowed fields are referenced_prp_id, relationship, note,
    and the schema-enforced not.anyOf. Any other key rejects."""
    body = copy.deepcopy(base_prp)
    body["cross_references"] = [
        {
            "referenced_prp_id": "TILTH-PRP-2CFR200",
            "relationship": "inherits_from",
            "evil_extension": "x",
        }
    ]
    assert list(validator.iter_errors(body)), (
        "R2-F5 regression: arbitrary evil_extension in cross_references item now passes"
    )


def test_R2_F5_cic_clc_matrix_in_cross_references_item_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["cross_references"] = [
        {
            "referenced_prp_id": "TILTH-PRP-2CFR200",
            "relationship": "inherits_from",
            "cic_clc_matrix": {},
        }
    ]
    assert list(validator.iter_errors(body)), (
        "R2-F5 regression: cic_clc_matrix in cross_references item now passes"
    )


def test_R2_F5_arbitrary_field_in_live_law_rules_item_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """live_law_rules.items also closed to additionalProperties:false in R2 fix."""
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0]["evil_extension"] = "x"
    assert list(validator.iter_errors(body)), (
        "R2-F5 regression: evil_extension in live_law_rules item now passes"
    )


def test_R2_positive_all_eleven_top_level_fields_pass(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Positive control: a PRP using all 11 allowed top-level fields must pass."""
    body = copy.deepcopy(base_prp)
    body["expiry_date"] = "2027-06-30"
    body["cross_references"] = [
        {
            "referenced_prp_id": "TILTH-PRP-2CFR200",
            "relationship": "inherits_from",
            "note": "Uniform Guidance inheritance",
        }
    ]
    errors = list(validator.iter_errors(body))
    assert errors == [], (
        f"R2 positive control regression: full-field PRP rejected: {[e.message for e in errors]}"
    )


# ---------------------------------------------------------------------------
# Round 3 cross-family findings (groq/openai/gpt-oss-120b + google/gemini-2.5-pro)
# Output: pipeline/validation/prp_v0_1_red_team_2026-05-17/round_3/{red_team,judge}.md
# Judge round-3 verdict: PASS, 86/100. Two genuine findings remained:
#
# R3-F2 HIGH: program_specific PRPs allowed expiry_date null/absent —
#             a Law-2 (No Boundary Drift) hole.
# R3-Judge-D2 MEDIUM: camelCase regex bypass inside rule_body — fixed by
#             closing rule_body to additionalProperties:false.
#
# (Red Team also claimed $ref-sibling-dropping in rule_body — empirically
# FALSE in Draft 2020-12; that finding was a confusion with Draft 4 semantics.)
# ---------------------------------------------------------------------------


def test_R3_F2_program_specific_missing_expiry_date_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Round 3 Finding 2: program_specific PRPs MUST carry a non-null
    expiry_date. NOFO rules have finite windows; allowing null would let
    the rule remain in force after the funding opportunity closes (Law 2)."""
    body = copy.deepcopy(base_prp)
    body.pop("expiry_date")
    assert list(validator.iter_errors(body)), (
        "R3-F2 regression: program_specific without expiry_date now passes"
    )


def test_R3_F2_program_specific_null_expiry_date_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    body = copy.deepcopy(base_prp)
    body["expiry_date"] = None
    assert list(validator.iter_errors(body)), (
        "R3-F2 regression: program_specific with null expiry_date now passes"
    )


@pytest.mark.parametrize(
    "kind, prp_id",
    [
        ("cross_cutting_regulation", "TILTH-PRP-2CFR200"),
        ("compliance_framework", "TILTH-PRP-FERPA-COPPA-HIPAA"),
    ],
)
def test_R3_F2_non_program_specific_null_expiry_passes(
    validator: Draft202012Validator, base_prp: dict, kind: str, prp_id: str
) -> None:
    """cross_cutting_regulation and compliance_framework PRPs legitimately
    have no operator-known expiry — durable regulations and frameworks
    persist until superseded. R3-F2 conditional must NOT apply to them."""
    body = copy.deepcopy(base_prp)
    body["prp_kind"] = kind
    body["prp_id"] = prp_id
    body["funding_program_ref"] = None
    body["expiry_date"] = None
    errors = list(validator.iter_errors(body))
    assert errors == [], (
        f"R3-F2 over-tightened: {kind} with null expiry rejected: {[e.message for e in errors]}"
    )


@pytest.mark.parametrize(
    "camelcase_key",
    [
        "orgBudget",
        "mySecretNotes",
        "privateData",
        "tacticalPayload",
        "internalOrgInfo",
        "PrivateMemberData",
    ],
)
def test_R3_Judge_D2_camelcase_key_in_rule_body_rejected(
    validator: Draft202012Validator, base_prp: dict, camelcase_key: str
) -> None:
    """Round 3 Judge D2 finding: the patternProperties regex used non-
    alphanumeric word boundaries, allowing camelCase bypasses like
    'orgBudget' inside rule_body (the only container still
    additionalProperties:true). Fix: closed rule_body to
    additionalProperties:false at v0.1; per-rule_type sub-schemas land at
    v0.2 first wave."""
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0]["rule_body"] = {camelcase_key: "x"}
    assert list(validator.iter_errors(body)), (
        f"R3-Judge-D2 regression: camelCase {camelcase_key} in rule_body now passes"
    )


def test_R3_empty_rule_body_passes(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """rule_body locked to additionalProperties:false with empty properties
    means {} is the only legal non-omitted value at v0.1."""
    body = copy.deepcopy(base_prp)
    body["live_law_rules"][0]["rule_body"] = {}
    errors = list(validator.iter_errors(body))
    assert errors == [], (
        f"R3 positive control regression: empty rule_body rejected: {[e.message for e in errors]}"
    )


# ---------------------------------------------------------------------------
# Round 4 cross-family finding (groq/openai/gpt-oss-120b)
# Output: pipeline/validation/prp_v0_1_red_team_2026-05-17/round_4/red_team.md
# Judge round-4 verdict: PASS, 100/100, CONVERGENCE_ATTESTED — but the Judge
# MISSED this hole. The Red Team caught it: _research_metadata.primary_sources
# .items was the last container without additionalProperties:false or the
# coupling guards. Coupling fields could slip in via provenance.
#
# R4-F1 CRITICAL: primary_sources.items now locked to additionalProperties:
# false + forbidden_coupling + forbidden_law3_key_patterns.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "forbidden_key",
    [
        "cic_assignment",
        "preferred_clcs",
        "cic_clc_matrix",
        "private_member_roster",
        "cic_to_clc_eligibility",
        "common_cic_patterns_observed",
    ],
)
def test_R4_F1_coupling_field_in_primary_sources_item_rejected(
    validator: Draft202012Validator, base_prp: dict, forbidden_key: str
) -> None:
    """Round 4 Finding 1: _research_metadata.primary_sources.items must
    reject enumerated coupling fields just like every other nested object."""
    body = copy.deepcopy(base_prp)
    body["_research_metadata"]["primary_sources"][0][forbidden_key] = "x"
    assert list(validator.iter_errors(body)), (
        f"R4-F1 regression: {forbidden_key} in primary_sources item now passes"
    )


def test_R4_F1_arbitrary_field_in_primary_sources_item_rejected(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """primary_sources.items is now additionalProperties:false — any non-
    enumerated key rejects."""
    body = copy.deepcopy(base_prp)
    body["_research_metadata"]["primary_sources"][0]["evil_extension"] = "x"
    assert list(validator.iter_errors(body)), (
        "R4-F1 regression: evil_extension in primary_sources item now passes"
    )


def test_R4_F1_verbatim_quote_in_primary_sources_item_passes(
    validator: Draft202012Validator, base_prp: dict
) -> None:
    """Positive control: verbatim_quote is one of the declared properties of
    primary_sources.items and must continue to validate."""
    body = copy.deepcopy(base_prp)
    body["_research_metadata"]["primary_sources"][0]["verbatim_quote"] = (
        "Verbatim quote from the source."
    )
    errors = list(validator.iter_errors(body))
    assert errors == [], (
        f"R4-F1 over-tightened: verbatim_quote in primary_sources rejected: {[e.message for e in errors]}"
    )


# ---------------------------------------------------------------------------
# Loader-level sanity: top-level call still raises NotImplementedError so any
# seat wiring PRP loading before v0.2 first wave fails-closed.
# ---------------------------------------------------------------------------


def test_loader_top_level_raises_not_implemented() -> None:
    """The PRP loader top-level call MUST raise NotImplementedError at v0.1.

    If this regresses, a seat could silently dispatch PRP enforcement before
    the v0.2 first wave graduation ceremony, bypassing the gate bodies that
    are intentionally stubbed.
    """

    import sys
    sys.path.insert(0, str(REPO_ROOT))
    from pipeline.program_rule_packs import loader as prp_loader

    assert prp_loader.PRP_SCHEMA_VERSION_PINNED == "1.0-prp"
    assert prp_loader.F_PRP_PRIMITIVE_NAMES == (
        "F-PRP-NOT-IN-ACTIVE-MANIFEST",
        "F-PRP-SCHEMA-VERSION-MISMATCH",
        "F-PRP-LIFECYCLE-ENV-MISMATCH",
        "F-PRP-CONTENT-HASH-INVALID",
        "F-PRP-SIGNATURE-INVALID",
        "F-PRP-EXPIRED",
        "F-PRP-COUPLING-VIOLATION",
    )

    with pytest.raises(NotImplementedError, match="v0.2 first wave"):
        prp_loader.load_active_prps(environment="production")


# ---------------------------------------------------------------------------
# Manifest sanity: all 6 entries status=draft, content_hash=TBD.
# ---------------------------------------------------------------------------


def test_active_manifest_all_entries_are_draft() -> None:
    """The v0.1 DRAFT manifest MUST keep every entry at status=draft.

    If this regresses, an entry has graduated to 'signed' status without the
    v0.2 first wave ceremony — manifest got hand-edited.
    """

    import yaml

    manifest_path = REPO_ROOT / "pipeline" / "program_rule_packs" / "_manifest" / "active_prps.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())
    assert manifest["registry_kind"] == "active_prp_registry"
    assert len(manifest["active_prps"]) == 6
    for entry in manifest["active_prps"]:
        assert entry["status"] == "draft", f"{entry['prp_id']} is no longer draft"
        assert entry["content_hash"] == "TBD", f"{entry['prp_id']} content_hash changed from TBD"
