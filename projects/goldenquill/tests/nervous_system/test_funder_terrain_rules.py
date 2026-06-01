import pytest
from pipeline.nervous_system.funder_terrain.rules import FunderTerrainRule, hash_rules, check_rules

def test_rule_validation_exact_and_regex():
    r = FunderTerrainRule(
        rule_id="r1", target_field="filename", priority=10,
        regex_patterns=["exact match", r"^regex.*test$"],
        output_value="Val", confidence="CONFIRMED_BY_FILENAME",
        review_required=False, rationale="test"
    )
    assert len(r.regex_patterns) == 2

def test_rule_validation_invalid_regex_fails():
    with pytest.raises(ValueError, match="Invalid regex pattern"):
        FunderTerrainRule(
            rule_id="r1", target_field="filename", priority=10,
            regex_patterns=["["],
            output_value="Val", confidence="CONFIRMED",
            review_required=False, rationale="test"
        )

def test_rule_validation_suspicious_regex_fails():
    with pytest.raises(ValueError, match="Suspicious/High-Risk regex"):
        FunderTerrainRule(
            rule_id="r1", target_field="filename", priority=10,
            regex_patterns=[r"(a+)+b"],
            output_value="Val", confidence="CONFIRMED",
            review_required=False, rationale="test"
        )

def test_ruleset_hashing_determinism():
    r1 = FunderTerrainRule(rule_id="r1", target_field="a", priority=1, regex_patterns=["a"], output_value="a", confidence="C", review_required=False, rationale="a")
    r2 = FunderTerrainRule(rule_id="r2", target_field="b", priority=2, regex_patterns=["b"], output_value="b", confidence="C", review_required=False, rationale="b")

    hash1 = hash_rules([r1, r2])
    hash2 = hash_rules([r2, r1])
    assert hash1 == hash2

    r3 = FunderTerrainRule(rule_id="r1", target_field="b", priority=1, regex_patterns=["a"], output_value="a", confidence="C", review_required=False, rationale="a")
    hash3 = hash_rules([r3, r2])
    assert hash1 != hash3

def test_priority_ordering():
    rules = [
        FunderTerrainRule(rule_id="low", target_field="filename", priority=5, regex_patterns=["test"], output_value="Low", confidence="C", review_required=False, rationale="test"),
        FunderTerrainRule(rule_id="high", target_field="filename", priority=10, regex_patterns=["test"], output_value="High", confidence="C", review_required=False, rationale="test")
    ]
    match = check_rules("test file", rules)
    assert match[0].rule_id == "high"

def test_no_match():
    rules = [
        FunderTerrainRule(rule_id="low", target_field="filename", priority=5, regex_patterns=["nothing"], output_value="Low", confidence="C", review_required=False, rationale="test")
    ]
    match = check_rules("test file", rules)
    assert match is None
