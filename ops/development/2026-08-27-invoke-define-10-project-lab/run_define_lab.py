#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


LAB = Path(__file__).resolve().parent
REPO = LAB.parents[2]
INVOKE = REPO / "arcanum/spells/invoke"
SCHEMAS = INVOKE / "schemas"
COMPILER_PATH = INVOKE / "scripts/compile_define_source.py"
MANIFEST_PATH = LAB / "cases.json"
SOURCES = LAB / "sources"
OUTPUTS = LAB / "outputs"
RESULT_PATH = LAB / "RESULT.json"
REPORT_PATH = LAB / "RUN-REPORT.md"
INVENTORY_PATH = LAB / "CHANGED-PATH-INVENTORY.json"


def load_compiler():
    spec = importlib.util.spec_from_file_location("compile_define_source", COMPILER_PATH)
    if not spec or not spec.loader:
        raise RuntimeError("cannot load Define compiler")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact_ref(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": digest_bytes(data),
        "size": len(data),
    }


def source_for(case: dict[str, Any]) -> dict[str, Any]:
    discovery = REPO / case["discovery_path"]
    observed = exact_ref(discovery)
    expected = {
        "path": case["discovery_path"],
        "sha256": case["discovery_sha256"],
        "size": case["discovery_size"],
    }
    if observed != expected:
        raise ValueError(f"discovery drift for {case['id']}: {observed} != {expected}")
    declarations = [
        {
            "id": f"D-{index:03d}",
            "title": item["title"],
            "statement": item["statement"],
        }
        for index, item in enumerate(case["declarations"], start=1)
    ]
    glossary = [
        {
            "term": item["term"],
            "definition": item["definition"],
            "link_status": "no-match",
            "rationale": "Experiment-local projection; no upstream glossary promotion is requested.",
        }
        for item in case["glossary"]
    ]
    return {
        "schema_version": "invoke.define-source.v1",
        "source_id": f"DEFINE-LAB-{case['id'].upper()}",
        "target": {"id": case["target_id"], "objective": case["objective"]},
        "discovery": {"kind": "artifact", "ref": expected},
        "template_selection": {
            "profile_id": "invoke.generic-spec-baseline.v1",
            "selected": "invoke.generic-spec-baseline.v1",
            "eligible": ["invoke.generic-spec-baseline.v1"],
            "tie": False,
        },
        "spec_declarations": declarations,
        "glossary": glossary,
        "layering": {
            "kind": "gap",
            "rationale": "This laboratory proves Define authoring only; downstream planning owns implementation layering.",
        },
        "dispatch_trace": {
            "techniques": ["sequence", "owner_boundary_check", "concrete_path_evidence"]
        },
        "distill": {
            "classification": "not-required",
            "rationale": "Each case is one deliberately narrow definition projection of an existing project boundary.",
        },
        "identity_denominator": {
            "classification": "not-applicable",
            "rationale": "The case asserts no exact or canonical ID-to-label denominator.",
        },
        "output_contracts": {
            "spec": "SPEC.md",
            "glossary": "GLOSSARY.md",
            "layering": "LAYERING-GAP.md",
            "template_selection": "TEMPLATE-SELECTION-RECEIPT.json",
            "dispatch_trace": "DISPATCH-TRACE.json",
            "distill": "DISTILL-RECEIPT.json",
            "identity_denominator": "IDENTITY-DENOMINATOR-RECEIPT.json",
            "transport": "DEFINE-TRANSPORT-REPORT.json",
            "stage_receipt": "INVOKE-DEFINE-STAGE-RECEIPT.json",
        },
        "transport_policy": {
            "append_existing_only": True,
            "upstream_mutation": False,
            "targets": [],
        },
        "next_route": "deferred",
    }


def canonical_files(directory: Path) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in sorted(directory.iterdir()) if path.is_file()}


def validate_bundle(source: dict[str, Any], output: Path, receipt: dict[str, Any], result_schema: dict[str, Any]) -> None:
    errors = list(Draft202012Validator(result_schema).iter_errors(receipt))
    if errors:
        raise ValueError("receipt schema invalid: " + "; ".join(error.message for error in errors))
    expected_names = set(source["output_contracts"].values())
    actual_names = set(canonical_files(output))
    if actual_names != expected_names:
        raise ValueError(f"output set mismatch: {sorted(actual_names)} != {sorted(expected_names)}")
    for ref in receipt["outputs"]:
        path = output / ref["path"]
        data = path.read_bytes()
        if ref["sha256"] != digest_bytes(data) or ref["size"] != len(data):
            raise ValueError(f"receipt output ref mismatch: {ref['path']}")


def run() -> dict[str, Any]:
    if SOURCES.exists() or OUTPUTS.exists() or RESULT_PATH.exists() or REPORT_PATH.exists() or INVENTORY_PATH.exists():
        raise ValueError("persistent run outputs already exist; preserve them and use a fresh laboratory epoch")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    cases = manifest["cases"]
    if len(cases) != 10 or len({case["id"] for case in cases}) != 10:
        raise ValueError("the laboratory requires exactly ten unique cases")
    SOURCES.mkdir()
    OUTPUTS.mkdir()
    compiler = load_compiler()
    result_schema = json.loads((SCHEMAS / "define-result-v1.schema.json").read_text(encoding="utf-8"))
    case_results: list[dict[str, Any]] = []

    for case in cases:
        source = source_for(case)
        source_path = SOURCES / f"{case['id']}.json"
        source_path.write_text(json.dumps(source, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        output = OUTPUTS / case["id"]
        receipt = compiler.compile_source(source_path, output, REPO, SCHEMAS)
        validate_bundle(source, output, receipt, result_schema)

        with tempfile.TemporaryDirectory(prefix=f"invoke-define-{case['id']}-") as temp_name:
            temporary = Path(temp_name)
            second = temporary / "second"
            second_receipt = compiler.compile_source(source_path, second, REPO, SCHEMAS)
            deterministic = canonical_files(output) == canonical_files(second)
            if not deterministic or receipt != second_receipt:
                raise ValueError(f"non-deterministic compilation for {case['id']}")

            stale_source = json.loads(source_path.read_text(encoding="utf-8"))
            stale_source["discovery"]["ref"]["sha256"] = "0" * 64
            stale_path = temporary / "stale-source.json"
            stale_path.write_text(json.dumps(stale_source, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            stale_output = temporary / "stale-output"
            stale_blocked = False
            try:
                compiler.compile_source(stale_path, stale_output, REPO, SCHEMAS)
            except ValueError as error:
                stale_blocked = "stale" in str(error) and not stale_output.exists()
            if not stale_blocked:
                raise ValueError(f"stale discovery was not rejected atomically for {case['id']}")

        case_results.append(
            {
                "id": case["id"],
                "target_id": case["target_id"],
                "result": "pass",
                "source_ref": exact_ref(source_path),
                "discovery_ref": source["discovery"]["ref"],
                "output_dir": output.relative_to(REPO).as_posix(),
                "output_file_count": len(canonical_files(output)),
                "stage_receipt_digest": receipt["receipt_digest"],
                "determinism_second_run": "pass",
                "stale_discovery_negative": "pass",
                "completion_boundary": case["completion_boundary"],
                "semantic_projection_review": "human-curated-input; not validated by compiler",
                "authority_effect": "none",
            }
        )

    result = {
        "schema_version": "invoke.define-ten-project-lab-result.v1",
        "experiment_id": manifest["experiment_id"],
        "result": "pass",
        "case_count": len(case_results),
        "bundle_pass_count": sum(item["result"] == "pass" for item in case_results),
        "determinism_pass_count": sum(item["determinism_second_run"] == "pass" for item in case_results),
        "stale_discovery_negative_pass_count": sum(item["stale_discovery_negative"] == "pass" for item in case_results),
        "persistent_bundle_file_count": sum(item["output_file_count"] for item in case_results),
        "cases": case_results,
        "experiment_harness": {
            "mode": "run",
            "artifact": "arcanum/spells/invoke",
            "artifact_type": "spell",
            "profile_id": "invoke-live",
            "selection": "all-explicit-ten-project-cases",
            "validation": "pass",
            "profile_validation": "flag",
            "observation": "skipped-private-supplemental-run",
            "next_unrun": "none",
            "quality_bar_status": "pass",
            "anti_pattern_hits": [],
            "workflow_gaps": [
                {
                    "category": "semantic-validation",
                    "severity": "medium",
                    "summary": "The compiler does not validate the truth of the human-curated semantic projection."
                },
                {
                    "category": "profile",
                    "severity": "low",
                    "summary": "This supplemental batch is not registered in the invoke-live prompt and regime sets."
                }
            ]
        },
        "claim_ceiling": "Atomic Define compiler evidence over ten curated projections; not semantic extraction, project completion, registry release, runtime readiness, acceptance, publication, or production evidence.",
        "authority_effect": "none",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows = "\n".join(
        f"| {item['id']} | PASS | 9 | PASS | PASS | {item['stage_receipt_digest']} |"
        for item in case_results
    )
    REPORT_PATH.write_text(
        "# Invoke Define Ten-Project Run Report\n\n"
        "## Outcome\n\n"
        "Ten of ten curated project projections compiled atomically. Each published a nine-file bundle, reproduced byte-identically in a second temporary run, and rejected a stale discovery digest without publishing output.\n\n"
        "| Case | Bundle | Files | Determinism | Stale discovery | Stage receipt digest |\n"
        "| --- | --- | ---: | --- | --- | --- |\n"
        f"{rows}\n\n"
        "## Experiment Harness Result\n\n"
        "- Mode: run\n"
        "- Artifact: arcanum/spells/invoke\n"
        "- Artifact type: spell\n"
        "- Profile: invoke-live\n"
        "- Selection: all-explicit-ten-project-cases\n"
        "- Output: ten persistent private bundles\n"
        "- Report: this file\n"
        "- Validation: pass\n"
        "- Profile validation: flag; supplemental batch is not registered in the existing prompt/regime sets\n"
        "- Observation: skipped; private supplemental run, not promotion evidence\n"
        "- Next unrun: none\n\n"
        "PROFILE_ID=invoke-live\n"
        "LIFECYCLE_OWNER=invoke\n"
        "ARTIFACT_TYPE=spell\n"
        "CONTRACT_PATH=arcanum/spells/invoke/README.md\n"
        "PROMPT_SET=ten-project-private-replay\n"
        "REGIME_SET=SUPPLEMENTAL-DEFINE-10-PROJECTS-001\n"
        "PROFILE_VALIDATION=flag\n"
        "QUALITY_BAR_STATUS=pass\n"
        "ANTI_PATTERN_HITS_JSON=[]\n"
        "WORKFLOW_GAPS_JSON=[{\"category\":\"semantic-validation\",\"severity\":\"medium\",\"summary\":\"compiler does not validate human-curated semantic truth\"},{\"category\":\"profile\",\"severity\":\"low\",\"summary\":\"supplemental batch is not registered in invoke-live\"}]\n\n"
        "## Claim Ceiling\n\n"
        f"{result['claim_ceiling']}\n",
        encoding="utf-8",
    )

    inventory_entries = []
    for path in sorted(candidate for candidate in LAB.rglob("*") if candidate.is_file() and candidate != INVENTORY_PATH):
        inventory_entries.append(exact_ref(path))
    inventory = {
        "schema_version": "invoke.define-ten-project-lab-inventory.v1",
        "experiment_id": manifest["experiment_id"],
        "inventory_self_excluded": True,
        "entries": inventory_entries,
        "entry_count": len(inventory_entries),
        "authority_effect": "none",
    }
    INVENTORY_PATH.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    try:
        result = run()
    except Exception as error:
        print(json.dumps({"result": "block", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps({
        "result": result["result"],
        "case_count": result["case_count"],
        "bundle_pass_count": result["bundle_pass_count"],
        "determinism_pass_count": result["determinism_pass_count"],
        "stale_discovery_negative_pass_count": result["stale_discovery_negative_pass_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
