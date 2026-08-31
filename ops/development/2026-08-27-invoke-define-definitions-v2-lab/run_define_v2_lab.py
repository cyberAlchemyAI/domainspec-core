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
COMPILER_PATH = INVOKE / "scripts/compile_define_source_v2.py"
BASE_CASES_PATH = (
    REPO / "ops/development/2026-08-27-invoke-define-10-project-lab/cases.json"
)
BASELINE_PATH = LAB / "PRE-V2-BASELINE.json"
SOURCES = LAB / "sources"
OUTPUTS = LAB / "outputs"
RESULT_PATH = LAB / "RESULT.json"
REPORT_PATH = LAB / "RUN-REPORT.md"
INVENTORY_PATH = LAB / "CHANGED-PATH-INVENTORY.json"


def load_compiler():
    spec = importlib.util.spec_from_file_location("compile_define_source_v2", COMPILER_PATH)
    if not spec or not spec.loader:
        raise RuntimeError("cannot load Define v2 compiler")
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


def validate_frozen_baseline() -> list[dict[str, str]]:
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    validated: list[dict[str, str]] = []
    entries = [
        *baseline["compatibility_frozen_paths"],
        baseline["definitions_schema_seed"],
    ]
    for entry in entries:
        observed = digest_bytes((REPO / entry["path"]).read_bytes())
        if observed != entry["sha256"]:
            raise ValueError(
                f"frozen baseline drift for {entry['path']}: {observed} != {entry['sha256']}"
            )
        validated.append({"path": entry["path"], "sha256": observed})
    return validated


def definition_for(
    case: dict[str, Any],
    glossary: dict[str, str],
    index: int,
    source_ref: dict[str, Any],
    line_count: int,
) -> dict[str, Any]:
    definition_id = f"DEF-{case['id'].upper()}-{index:03d}"
    declaration = case["declarations"][min(index - 1, len(case["declarations"]) - 1)]
    return {
        "id": definition_id,
        "term": glossary["term"],
        "aliases": [],
        "status": "candidate",
        "status_detail": None,
        "deferred_as": None,
        "supersedes": [],
        "superseded_by": None,
        "source_kinds": ["local-inference"],
        "voices": {
            "normative": glossary["definition"],
            "formal": declaration["statement"],
            "operational": glossary["definition"],
            "plain_language": glossary["definition"],
            "domain_context": (
                f"{case['objective']} Boundary: {case['completion_boundary']}"
            ),
        },
        "notation": [],
        "boundary": {
            "includes": [case["objective"]],
            "excludes": [case["completion_boundary"]],
            "conditions": [item["statement"] for item in case["declarations"]],
        },
        "source_refs": [
            {
                "role": "evidence",
                "path": source_ref["path"],
                "visibility": "private",
                "selector_type": "line-span",
                "selector": f"lines 1-{line_count}",
                "start_line": 1,
                "end_line": line_count,
                "sha256": source_ref["sha256"],
                "size": source_ref["size"],
            }
        ],
        "primary_consumers": ["DEFINITIONS.md", "GLOSSARY.md", "SPEC.md"],
        "relations": [],
        "use_carefully": "Treat this as a human-curated project projection, not extraction proof.",
        "misuse_warning": "Candidate packaging grants no semantic or operational authority.",
        "challenge_contract": None,
        "promotion_boundary": (
            "Candidate only; definitions-governance owns any later review and promotion."
        ),
        "drift_route": "definitions-governance",
        "definition_version": "1",
        "structural_schema": None,
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
    line_count = len(discovery.read_text(encoding="utf-8").splitlines())
    if line_count < 1:
        raise ValueError(f"empty discovery source for {case['id']}")

    declarations = [
        {
            "id": f"D-{index:03d}",
            "title": item["title"],
            "statement": item["statement"],
        }
        for index, item in enumerate(case["declarations"], start=1)
    ]
    definitions = [
        definition_for(case, item, index, expected, line_count)
        for index, item in enumerate(case["glossary"], start=1)
    ]
    return {
        "schema_version": "invoke.define-source.v2",
        "source_id": f"DEFINE-V2-LAB-{case['id'].upper()}",
        "target": {"id": case["target_id"], "objective": case["objective"]},
        "discovery": {"kind": "artifact", "ref": expected},
        "template_selection": {
            "profile_id": "invoke.generic-definitions-baseline.v2",
            "selected": "invoke.generic-definitions-baseline.v2",
            "eligible": ["invoke.generic-definitions-baseline.v2"],
            "tie": False,
        },
        "spec_declarations": declarations,
        "definition_registry": {
            "registry_id": f"{case['id']}.definitions.v2",
            "title": f"{case['target_id']} Candidate Definitions",
            "owner_route": "definitions-governance",
            "authority_scope": {"kind": "project", "ref": case["id"]},
            "visibility": "private",
            "definitions": definitions,
        },
        "layering": {
            "kind": "gap",
            "rationale": (
                "This laboratory proves Define authoring only; downstream planning owns "
                "implementation layering."
            ),
        },
        "dispatch_trace": {
            "techniques": [
                "sequence",
                "owner_boundary_check",
                "concrete_path_evidence",
            ]
        },
        "distill": {
            "classification": "not-required",
            "rationale": (
                "Each case is one deliberately narrow definition projection of an existing "
                "project boundary."
            ),
        },
        "identity_denominator": {
            "classification": "not-applicable",
            "rationale": "The case asserts no exact or canonical ID-to-label denominator.",
        },
        "output_contracts": {
            "spec": "SPEC.md",
            "definitions": "DEFINITIONS.json",
            "definitions_view": "DEFINITIONS.md",
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
    return {
        path.name: path.read_bytes()
        for path in sorted(directory.iterdir())
        if path.is_file()
    }


def validate_bundle(
    source: dict[str, Any],
    output: Path,
    receipt: dict[str, Any],
    result_schema: dict[str, Any],
) -> None:
    errors = list(Draft202012Validator(result_schema).iter_errors(receipt))
    if errors:
        raise ValueError(
            "receipt schema invalid: " + "; ".join(error.message for error in errors)
        )
    expected_names = set(source["output_contracts"].values())
    actual_names = set(canonical_files(output))
    if actual_names != expected_names:
        raise ValueError(
            f"output set mismatch: {sorted(actual_names)} != {sorted(expected_names)}"
        )
    for ref in receipt["outputs"]:
        path = output / ref["path"]
        data = path.read_bytes()
        if ref["sha256"] != digest_bytes(data) or ref["size"] != len(data):
            raise ValueError(f"receipt output ref mismatch: {ref['path']}")
    definitions = json.loads((output / "DEFINITIONS.json").read_text(encoding="utf-8"))
    if definitions["registry_status"] != "candidate":
        raise ValueError("generated registry status is not candidate")
    if definitions["authority_effect"] != "none":
        raise ValueError("generated registry has an authority effect")
    if len(definitions["definitions"]) != 2:
        raise ValueError("generated registry does not contain exactly two definitions")


def assert_atomic_negative(
    compiler: Any,
    source_path: Path,
    source: dict[str, Any],
    output: Path,
    expected_error: str,
) -> None:
    source_path.write_text(
        json.dumps(source, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    try:
        compiler.compile_source(source_path, output, REPO, SCHEMAS)
    except ValueError as error:
        if expected_error not in str(error) or output.exists():
            raise ValueError(
                f"negative control failed: expected {expected_error!r}, observed {error!s}"
            ) from error
    else:
        raise ValueError(f"negative control unexpectedly passed: {expected_error}")


def run() -> dict[str, Any]:
    generated = [SOURCES, OUTPUTS, RESULT_PATH, REPORT_PATH, INVENTORY_PATH]
    if any(path.exists() for path in generated):
        raise ValueError(
            "persistent run outputs already exist; preserve them and use a fresh laboratory epoch"
        )
    baseline_validation = validate_frozen_baseline()
    manifest = json.loads(BASE_CASES_PATH.read_text(encoding="utf-8"))
    cases = manifest["cases"]
    if len(cases) != 10 or len({case["id"] for case in cases}) != 10:
        raise ValueError("the laboratory requires exactly ten unique cases")
    SOURCES.mkdir()
    OUTPUTS.mkdir()
    compiler = load_compiler()
    result_schema = json.loads(
        (SCHEMAS / "define-result-v2.schema.json").read_text(encoding="utf-8")
    )
    case_results: list[dict[str, Any]] = []

    for case in cases:
        source = source_for(case)
        source_path = SOURCES / f"{case['id']}.json"
        source_path.write_text(
            json.dumps(source, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        output = OUTPUTS / case["id"]
        receipt = compiler.compile_source(source_path, output, REPO, SCHEMAS)
        validate_bundle(source, output, receipt, result_schema)

        with tempfile.TemporaryDirectory(
            prefix=f"invoke-define-v2-{case['id']}-"
        ) as temp_name:
            temporary = Path(temp_name)
            second = temporary / "second"
            second_receipt = compiler.compile_source(
                source_path, second, REPO, SCHEMAS
            )
            if canonical_files(output) != canonical_files(second):
                raise ValueError(f"non-deterministic compilation for {case['id']}")
            if receipt != second_receipt:
                raise ValueError(f"non-deterministic receipt for {case['id']}")

            stale_discovery = json.loads(source_path.read_text(encoding="utf-8"))
            stale_discovery["discovery"]["ref"]["sha256"] = "0" * 64
            assert_atomic_negative(
                compiler,
                temporary / "stale-discovery.json",
                stale_discovery,
                temporary / "stale-discovery-output",
                "discovery exact ref is stale",
            )

            stale_definition = json.loads(source_path.read_text(encoding="utf-8"))
            stale_definition["definition_registry"]["definitions"][0]["source_refs"][0][
                "sha256"
            ] = "0" * 64
            assert_atomic_negative(
                compiler,
                temporary / "stale-definition.json",
                stale_definition,
                temporary / "stale-definition-output",
                "source SHA-256 is stale",
            )

        case_results.append(
            {
                "id": case["id"],
                "target_id": case["target_id"],
                "result": "pass",
                "source_ref": exact_ref(source_path),
                "discovery_ref": source["discovery"]["ref"],
                "output_dir": output.relative_to(REPO).as_posix(),
                "output_file_count": len(canonical_files(output)),
                "definition_count": 2,
                "stage_receipt_digest": receipt["receipt_digest"],
                "determinism_second_run": "pass",
                "stale_discovery_negative": "pass",
                "stale_definition_source_negative": "pass",
                "completion_boundary": case["completion_boundary"],
                "semantic_projection_review": (
                    "human-curated-input; semantic truth not validated by compiler"
                ),
                "authority_effect": "none",
            }
        )

    result = {
        "schema_version": "invoke.define-ten-project-definitions-lab-result.v2",
        "experiment_id": "INVOKE-DEFINE-DEFINITIONS-V2-10-PROJECTS-20260827",
        "source_case_manifest": exact_ref(BASE_CASES_PATH),
        "result": "pass",
        "case_count": len(case_results),
        "bundle_pass_count": sum(item["result"] == "pass" for item in case_results),
        "definition_count": sum(item["definition_count"] for item in case_results),
        "determinism_pass_count": sum(
            item["determinism_second_run"] == "pass" for item in case_results
        ),
        "stale_discovery_negative_pass_count": sum(
            item["stale_discovery_negative"] == "pass" for item in case_results
        ),
        "stale_definition_source_negative_pass_count": sum(
            item["stale_definition_source_negative"] == "pass"
            for item in case_results
        ),
        "persistent_bundle_file_count": sum(
            item["output_file_count"] for item in case_results
        ),
        "frozen_baseline_validation": {
            "result": "pass",
            "validated_paths": baseline_validation,
        },
        "cases": case_results,
        "claim_ceiling": (
            "Atomic Define v2 compiler evidence over twenty human-curated candidate "
            "definitions in ten existing project projections; not semantic extraction, "
            "semantic truth, project completion, definition promotion, registry release, "
            "runtime readiness, acceptance, publication, deployment, or production evidence."
        ),
        "authority_effect": "none",
    }
    RESULT_PATH.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    rows = "\n".join(
        f"| {item['id']} | PASS | 2 | 11 | PASS | PASS | PASS | {item['stage_receipt_digest']} |"
        for item in case_results
    )
    REPORT_PATH.write_text(
        "# Invoke Define v2 Ten-Project Run Report\n\n"
        "## Outcome\n\n"
        "Ten of ten curated project projections compiled atomically. The run emitted "
        "twenty candidate definitions across ten 11-file bundles, reproduced each bundle "
        "byte-identically, and rejected stale discovery and definition-source evidence "
        "without publishing output.\n\n"
        "| Case | Bundle | Definitions | Files | Determinism | Stale discovery | Stale definition source | Stage receipt digest |\n"
        "| --- | --- | ---: | ---: | --- | --- | --- | --- |\n"
        f"{rows}\n\n"
        "## Compatibility\n\n"
        f"- Frozen v1/schema paths checked: {len(baseline_validation)}\n"
        "- Result: PASS; every captured SHA-256 still matches.\n\n"
        "## Claim Ceiling\n\n"
        f"{result['claim_ceiling']}\n",
        encoding="utf-8",
    )

    inventory_entries = []
    for path in sorted(
        candidate
        for candidate in LAB.rglob("*")
        if candidate.is_file() and candidate != INVENTORY_PATH
    ):
        inventory_entries.append(exact_ref(path))
    inventory = {
        "schema_version": "invoke.define-ten-project-definitions-lab-inventory.v2",
        "experiment_id": result["experiment_id"],
        "inventory_self_excluded": True,
        "entries": inventory_entries,
        "entry_count": len(inventory_entries),
        "authority_effect": "none",
    }
    INVENTORY_PATH.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    try:
        result = run()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"BLOCK: {error}")
        return 2
    print(
        json.dumps(
            {
                "result": result["result"],
                "case_count": result["case_count"],
                "definition_count": result["definition_count"],
                "persistent_bundle_file_count": result[
                    "persistent_bundle_file_count"
                ],
                "authority_effect": result["authority_effect"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
