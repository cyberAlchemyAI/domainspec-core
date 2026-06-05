"""Deterministic L0 validator for GoldenQuill PromotionRecord fixtures.

This module intentionally validates synthetic fixture files only. It does not
read organization memory, signed cards, dashboard state, or ontology templates.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RULES = {
    "GQ-PR-L0-001": "GrantOutcomeEvent requires a source truth record.",
    "GQ-PR-L0-002": "GrantKpiObservation requires denominator semantics.",
    "GQ-PR-L0-003": "Application stage depth cannot be treated as outcome truth.",
    "GQ-PR-L0-004": "PromotionCandidate requires a contradiction path.",
    "GQ-PR-L0-005": "PromotionCandidate cannot carry approved uses before owner decision.",
    "GQ-PR-L0-006": "Org-scoped feedback needs redaction/generalization before workspace reuse.",
    "GQ-PR-L0-007": "OntologyVaultProjection requires evidence references.",
    "GQ-PR-L0-008": "KPI threshold alone cannot directly promote.",
    "GQ-PR-L0-009": "OntologyVaultProjection must project to record_kind promotion_record.",
    "GQ-PR-L0-010": "Approved OwnerDecision requires approved allowed uses and decision source.",
    "GQ-PR-L0-011": "PromotionCandidate requires proposed allowed uses.",
}


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    fixture_type: str
    expected: str
    observed: str
    failures: list[str]

    @property
    def matched_expectation(self) -> bool:
        return self.expected == self.observed


def _has_source(source: Any) -> bool:
    return (
        isinstance(source, dict)
        and bool(source.get("type"))
        and bool(source.get("locator") or source.get("uri"))
        and bool(source.get("captured_at"))
    )


def _has_denominator(definition: Any) -> bool:
    return (
        isinstance(definition, dict)
        and bool(definition.get("numerator"))
        and bool(definition.get("denominator"))
        and bool(definition.get("period"))
    )


def _non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def validate_case(case: dict[str, Any]) -> CaseResult:
    failures: list[str] = []
    case_id = case.get("case_id", "<missing-case-id>")
    fixture_type = case.get("fixture_type", "<missing-fixture-type>")
    expected = case.get("expected", "pass")
    data = case.get("data", {})

    if fixture_type == "GrantOutcomeEvent":
        if not _has_source(data.get("source")):
            failures.append("GQ-PR-L0-001")
        if data.get("outcome_truth_from") == "application_stage":
            failures.append("GQ-PR-L0-003")

    elif fixture_type == "GrantKpiObservation":
        if not _has_denominator(data.get("denominator_definition")):
            failures.append("GQ-PR-L0-002")
        if data.get("triggers_promotion_directly") is True:
            failures.append("GQ-PR-L0-008")

    elif fixture_type == "PromotionCandidate":
        if not _non_empty_list(data.get("proposed_allowed_uses")):
            failures.append("GQ-PR-L0-011")
        if not data.get("contradiction_path"):
            failures.append("GQ-PR-L0-004")
        if data.get("approved_allowed_uses") and not data.get("owner_decision_ref"):
            failures.append("GQ-PR-L0-005")
        if (
            data.get("source_feedback_scope") == "org_scoped"
            and "workspace_reuse" in data.get("proposed_allowed_uses", [])
            and data.get("redaction_status") not in {"redacted", "generalized"}
        ):
            failures.append("GQ-PR-L0-006")

    elif fixture_type == "OntologyVaultProjection":
        if data.get("record_kind") != "promotion_record":
            failures.append("GQ-PR-L0-009")
        if not _non_empty_list(data.get("evidence_refs")):
            failures.append("GQ-PR-L0-007")

    elif fixture_type == "OwnerDecision":
        if data.get("decision") == "approved":
            if not _non_empty_list(data.get("approved_allowed_uses")) or not _has_source(data.get("decision_source")):
                failures.append("GQ-PR-L0-010")

    else:
        failures.append("GQ-PR-L0-000")

    observed = "fail" if failures else "pass"
    return CaseResult(
        case_id=case_id,
        fixture_type=fixture_type,
        expected=expected,
        observed=observed,
        failures=failures,
    )


def validate_fixture_pack(pack: dict[str, Any]) -> list[CaseResult]:
    cases = pack.get("positive_cases", []) + pack.get("negative_cases", [])
    return [validate_case(case) for case in cases]


def load_fixture_pack(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def result_payload(results: list[CaseResult]) -> dict[str, Any]:
    return {
        "status": "pass" if all(result.matched_expectation for result in results) else "fail",
        "results": [
            {
                "case_id": result.case_id,
                "fixture_type": result.fixture_type,
                "expected": result.expected,
                "observed": result.observed,
                "failures": result.failures,
                "matched_expectation": result.matched_expectation,
            }
            for result in results
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GoldenQuill PromotionRecord L0 fixture pack.")
    parser.add_argument("fixture_pack", type=Path)
    args = parser.parse_args()

    pack = load_fixture_pack(args.fixture_pack)
    payload = result_payload(validate_fixture_pack(pack))
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

