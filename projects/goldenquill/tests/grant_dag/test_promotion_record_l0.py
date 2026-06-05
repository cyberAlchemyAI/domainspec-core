import json
from pathlib import Path

from pipeline.grant_dag.validate import RULES, load_fixture_pack, validate_fixture_pack


ROOT = Path(__file__).resolve().parents[4]
FIXTURE_PACK = ROOT / "projects/goldenquill/pipeline/grant_dag/fixtures/promotion_record_l0_fixture_pack.json"
EXPECTED = ROOT / "projects/goldenquill/tests/grant_dag/fixtures/promotion_record_l0_expected.json"


def test_fixture_pack_declares_synthetic_non_mutating_boundary():
    pack = load_fixture_pack(FIXTURE_PACK)
    boundary = pack["authority_boundary"]

    assert pack["synthetic_data_only"] is True
    assert boundary["evidence_capture_is_not_promotion"] is True
    assert boundary["kpi_observation_is_not_promotion"] is True
    assert boundary["owner_decision_required_for_approved_reuse"] is True
    assert boundary["production_memory_mutation_allowed"] is False
    assert boundary["signed_card_mutation_allowed"] is False
    assert boundary["dashboard_mutation_allowed"] is False
    assert boundary["canonical_ontology_template_mutation_allowed"] is False


def test_fixture_pack_covers_required_cases_and_rule_ids():
    pack = load_fixture_pack(FIXTURE_PACK)
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    fixture_types = {case["fixture_type"] for case in pack["positive_cases"] + pack["negative_cases"]}

    assert len(pack["positive_cases"]) == expected["positive_case_count"]
    assert len(pack["negative_cases"]) == expected["negative_case_count"]
    assert set(expected["required_fixture_types"]).issubset(fixture_types)
    assert set(expected["required_rule_ids"]).issubset(RULES)
    assert set(expected["required_rule_ids"]).issubset(pack["rule_registry"])


def test_positive_cases_pass_and_negative_cases_fail_closed_with_expected_rule_ids():
    pack = load_fixture_pack(FIXTURE_PACK)
    results = {result.case_id: result for result in validate_fixture_pack(pack)}

    for case in pack["positive_cases"]:
        result = results[case["case_id"]]
        assert result.observed == "pass"
        assert result.failures == []

    for case in pack["negative_cases"]:
        result = results[case["case_id"]]
        assert result.observed == "fail"
        assert result.failures == case["expected_failures"]
