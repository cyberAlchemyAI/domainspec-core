#!/usr/bin/env python3
"""Run the DVC four-case composed Define -> Design -> Plan boundary proof."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
CANONICAL = ROOT / "arcanum/spells/invoke"
FIXTURE_DIR = CANONICAL / "development/fixtures/design-selection"
EXPECTED_PATH = HERE / "expected-live-proof.json"
CASE_IDS = (
    "DESIGN-BOUND-002",
    "DESIGN-BOUND-006",
    "DESIGN-NEG-005",
    "DESIGN-NEG-014",
)
SURFACES = {
    "canonical": CANONICAL,
    "repo-codex": ROOT / ".agents/skills/invoke",
    "claude": ROOT / ".claude/skills/invoke",
}


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"JSON object required: {path}")
    return value


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def projection(result: dict[str, Any]) -> dict[str, Any]:
    dispositions = {
        item["primary_class"]: item["disposition"]
        for item in result["concerns"]
    }
    return {
        "verdict": result["verdict"],
        "primary_concerns": sorted(
            key
            for key, disposition in dispositions.items()
            if disposition != "not-applicable-with-rationale"
        ),
        "dispositions": dispositions,
        "selected_outputs": result["selected_outputs"],
        "evidence_state": result["evidence_state"],
        "diagnostic_codes": sorted(
            {item["code"] for item in result["diagnostics"]}
        ),
    }


def execute_surface(
    surface_name: str,
    surface: Path,
    manifest: dict[str, Any],
    authored: list[dict[str, Any]],
    witnesses: list[dict[str, Any]],
    extra_ids: list[str],
    case_root: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    extractor = load_module(
        f"dvc_live_extractor_{surface_name.replace('-', '_')}",
        surface / "scripts/design_scope_extractor.py",
    )
    validator = load_module(
        f"dvc_live_validator_{surface_name.replace('-', '_')}",
        surface / "scripts/design_selection_validator.py",
    )
    schemas = {
        "manifest": load_json(surface / "schemas/design-scope-manifest.schema.json"),
        "receipt": load_json(
            surface / "schemas/design-denominator-receipt.schema.json"
        ),
        "result": load_json(surface / "schemas/design-selection-result.schema.json"),
    }
    receipt = extractor.extract_denominator(
        manifest,
        case_root,
        schemas["manifest"],
        [item["concern_id"] for item in authored] + extra_ids,
    )
    result = validator.validate_selection(
        manifest,
        receipt,
        authored,
        witnesses,
        schemas,
    )
    repeat = validator.validate_selection(
        manifest,
        receipt,
        authored,
        witnesses,
        schemas,
    )
    if repeat["result_digest"] != result["result_digest"]:
        raise AssertionError(f"{surface_name}: repeat result digest changed")
    return receipt, result


def main() -> int:
    runner = load_module(
        "dvc_live_fixture_runner",
        FIXTURE_DIR / "run_fixture_matrix.py",
    )
    matrix = load_json(FIXTURE_DIR / "fixture-matrix.json")
    denominator = load_json(FIXTURE_DIR / "fixture-denominator-receipt.json")
    expected_live = load_json(EXPECTED_PATH)
    expected_by_id = {
        item["fixture_id"]: item for item in expected_live["cases"]
    }
    cases_by_id = {item["fixture_id"]: item for item in matrix["cases"]}
    if runner.canonical_digest(matrix) != denominator["corpus_digest"]:
        raise AssertionError("frozen corpus digest changed")

    proof_cases = []
    evidence_trace = []
    failures = []
    for fixture_id in CASE_IDS:
        case = cases_by_id[fixture_id]
        case_root = HERE / "live-cases" / fixture_id
        case_root.mkdir(parents=True, exist_ok=True)
        manifest, authored, witnesses, extra_ids = runner.build_manifest(
            fixture_id,
            matrix["profiles"][case["profile"]],
            case["faults"],
            case_root,
        )
        define_input = {
            "schema_version": "invoke.dvc-live-define-input.v1",
            "fixture_id": fixture_id,
            "title": case["title"],
            "profile": case["profile"],
            "faults": case["faults"],
            "source_contracts": manifest["source_contracts"],
            "target_footprint": manifest["target_footprint"],
        }
        dump(case_root / "define-input.json", define_input)
        dump(case_root / "design-scope-manifest.json", manifest)

        surface_results: dict[str, Any] = {}
        canonical_receipt: dict[str, Any] | None = None
        canonical_result: dict[str, Any] | None = None
        for surface_name, surface in SURFACES.items():
            receipt, result = execute_surface(
                surface_name,
                surface,
                manifest,
                authored,
                witnesses,
                extra_ids,
                case_root,
            )
            dump(case_root / f"{surface_name}-denominator-receipt.json", receipt)
            dump(case_root / f"{surface_name}-selection-result.json", result)
            surface_results[surface_name] = projection(result)
            if surface_name == "canonical":
                canonical_receipt = receipt
                canonical_result = result

        assert canonical_receipt is not None and canonical_result is not None
        expected_compare = runner.compare_case(
            case,
            surface_results["canonical"],
        )
        parity = (
            surface_results["repo-codex"] == surface_results["canonical"]
            and surface_results["claude"] == surface_results["canonical"]
        )
        canonical_projection = surface_results["canonical"]
        plan_route = (
            "normal-plan"
            if canonical_projection["verdict"] == "pass"
            and canonical_projection["evidence_state"] == "design-validator-pass"
            else "blocked-before-plan"
        )
        plan_evidence_state = (
            "plan-evidence-pending" if plan_route == "normal-plan" else "n/a"
        )
        expected_route = expected_by_id[fixture_id]
        expected_fields_match = all(
            canonical_projection[key] == expected_route[key]
            for key in ("verdict", "evidence_state")
        )
        expected_fields_match = expected_fields_match and all(
            (
                key not in expected_route
                or canonical_projection[key] == expected_route[key]
            )
            for key in ("diagnostic_codes",)
        )
        route_match = (
            plan_route == expected_route["plan_route"]
            and plan_evidence_state == expected_route["plan_evidence_state"]
        )
        case_status = (
            "pass"
            if expected_compare["status"] == "pass"
            and parity
            and expected_fields_match
            and route_match
            else "fail"
        )
        if case_status != "pass":
            failures.append(fixture_id)

        plan_handoff = {
            "schema_version": "invoke.dvc-live-plan-handoff.v1",
            "fixture_id": fixture_id,
            "route": plan_route,
            "design_evidence_state": canonical_projection["evidence_state"],
            "plan_evidence_state": plan_evidence_state,
            "selection_result_digest": canonical_result["result_digest"],
            "normal_implementation_readiness": plan_route == "normal-plan",
        }
        dump(case_root / "plan-handoff.json", plan_handoff)
        case_summary = {
            "fixture_id": fixture_id,
            "title": case["title"],
            "status": case_status,
            "expected_comparison": expected_compare,
            "runtime_parity": parity,
            "actual": canonical_projection,
            "plan_handoff": plan_handoff,
        }
        dump(case_root / "case-summary.json", case_summary)
        proof_cases.append(case_summary)
        evidence_trace.append(
            {
                "fixture_id": fixture_id,
                "define": "source-contract-closed",
                "design": canonical_projection["evidence_state"],
                "design_verdict": canonical_projection["verdict"],
                "plan_route": plan_route,
                "plan": plan_evidence_state,
                "capability_axes_inferred": [],
            }
        )

    source_digests = {}
    for surface_name, surface in SURFACES.items():
        source_digests[surface_name] = {
            "README.md": digest(surface / "README.md"),
            "design.md": digest(surface / "design.md"),
            "extractor": digest(surface / "scripts/design_scope_extractor.py"),
            "validator": digest(surface / "scripts/design_selection_validator.py"),
            "manifest_schema": digest(
                surface / "schemas/design-scope-manifest.schema.json"
            ),
            "denominator_schema": digest(
                surface / "schemas/design-denominator-receipt.schema.json"
            ),
            "selection_schema": digest(
                surface / "schemas/design-selection-result.schema.json"
            ),
        }
    result = {
        "schema_version": "invoke.design-selection-live-proof.v1",
        "result": "pass" if not failures else "block",
        "fixture_corpus_digest": denominator["corpus_digest"],
        "expected_contract_sha256": digest(EXPECTED_PATH),
        "source_digests": source_digests,
        "cases": proof_cases,
        "failures": failures,
        "authority_effect": "evidence-only-no-promotion",
    }
    dump(HERE / "live-proof.json", result)
    dump(
        HERE / "evidence-state-trace.json",
        {
            "schema_version": "invoke.dvc-evidence-state-trace.v1",
            "result": result["result"],
            "traces": evidence_trace,
        },
    )
    report_lines = [
        "# DVC Generic Composed Experiment Report",
        "",
        "- Artifact: `arcanum/spells/invoke`",
        "- Profile: `DVC Define -> Design -> Plan boundary proof`",
        f"- Result: `{result['result']}`",
        "- Cases: `4`",
        "- Runtime surfaces: `canonical`, `repo-codex`, `claude`",
        "- Authority effect: evidence only; no promotion, release, commit, or push",
        "",
        "## Case results",
        "",
    ]
    for item in proof_cases:
        report_lines.append(
            f"- `{item['fixture_id']}`: `{item['status']}`; "
            f"Design `{item['actual']['evidence_state']}`; "
            f"Plan `{item['plan_handoff']['plan_evidence_state']}`."
        )
    report_lines.extend(
        [
            "",
            "Positive Designs route to normal Plan only at "
            "`design-validator-pass`, and Plan begins at "
            "`plan-evidence-pending`. Blocked Designs do not enter normal Plan.",
            "",
        ]
    )
    (HERE / "EXPERIMENT-REPORT.md").write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "result": result["result"],
                "cases": len(proof_cases),
                "failures": failures,
            },
            sort_keys=True,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
