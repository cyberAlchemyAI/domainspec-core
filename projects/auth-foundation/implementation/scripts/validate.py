#!/usr/bin/env python3
"""Validate the exact Auth Foundation D65 candidate and write local evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema


SCRIPT = Path(__file__).resolve()
IMPLEMENTATION = SCRIPT.parents[1]
AUTH_ROOT = SCRIPT.parents[2]
REPOSITORY = SCRIPT.parents[4]
RUNTIME = IMPLEMENTATION / "runtime"
GENERATED = IMPLEMENTATION / "domainspec" / "generated"
AUTH_KERNEL_TOOL = REPOSITORY / "projects/domainspec-v2/impl/cli/tools/auth-kernel.mjs"
NODE = shutil.which("node") or "/home/vrondelli/.nvm/versions/node/v22.12.0/bin/node"
TSX = os.environ.get("DOMAINSPEC_TSX") or shutil.which("tsx") or str(REPOSITORY / "projects/domainspec-v2/impl/node_modules/.bin/tsx")
DOMAINSPEC_CLI = REPOSITORY / "projects/domainspec-v2/impl/cli/src/cli/main.ts"
OPERATION_SOURCE = IMPLEMENTATION / "operation-source"
STANDARD_RUNTIME = IMPLEMENTATION / "standard-runtime"
STANDARD_BEHAVIOR = IMPLEMENTATION / "standard-conformance/behavior.rs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def encoded(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=False) + "\n"


def command(args: list[str], cwd: Path = REPOSITORY) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["TMPDIR"] = "/tmp"
    return subprocess.run(args, cwd=cwd, env=environment, text=True, capture_output=True, check=False)


def require(condition: bool, code: str, checks: list[dict]) -> None:
    checks.append({"check_id": code, "status": "PASS" if condition else "FAIL"})
    if not condition:
        raise AssertionError(code)


def require_unique(values: list[str], code: str, checks: list[dict]) -> None:
    require(len(values) == len(set(values)), code, checks)


def validate_property_denominator(checks: list[dict]) -> None:
    ontology = load(IMPLEMENTATION / "business-ontology.json")
    denominator = load(IMPLEMENTATION / "property-denominator.json")
    runtime_source = (RUNTIME / "src/lib.rs").read_text(encoding="utf-8")
    operation_root = IMPLEMENTATION / "operation-source"

    require(ontology["schema_version"] == "auth-foundation.business-ontology/v2-candidate", "business-ontology-property-contract-version", checks)
    require(ontology["property_contract"]["denominator_ref"] == "property-denominator.json", "business-ontology-denominator-binding", checks)
    require(denominator["ontology_id"] == ontology["ontology_id"], "property-denominator-ontology-binding", checks)
    require(denominator["operation_id"] == ontology["operations"][0]["operation_id"], "property-denominator-operation-binding", checks)
    require(denominator["mapping_state"] == "authored-source-candidate", "property-denominator-authored-source-state", checks)

    properties = ontology["properties"]
    variants = ontology["variants"]
    property_ids = [entry["property_id"] for entry in properties]
    variant_ids = [entry["variant_id"] for entry in variants]
    node_ids = {entry["id"] for entry in ontology["nodes"]}
    rule_ids = [entry["rule_id"] for entry in ontology["rules"]]
    require_unique(property_ids, "business-property-selectors-unique", checks)
    require_unique(variant_ids, "business-variant-selectors-unique", checks)
    require(all(entry["owner"] in node_ids for entry in properties), "business-property-owner-closure", checks)
    require(all(entry["owner"] in node_ids for entry in variants), "business-variant-owner-closure", checks)
    require_unique(rule_ids, "business-rule-selectors-unique", checks)

    allowed_scalars = set(ontology["property_contract"]["type_algebra"]["scalars"])
    named_types = {entry["type"] for entry in ontology["nodes"]}

    def type_supported(type_name: str) -> bool:
        if type_name in allowed_scalars or type_name in named_types:
            return True
        match = re.fullmatch(r"(Set|List|Optional)<([A-Za-z][A-Za-z0-9]*)>", type_name)
        return bool(match and (match.group(2) in allowed_scalars or match.group(2) in named_types))

    require(all(type_supported(entry["type"]) for entry in properties), "business-property-types-supported", checks)
    require(all(entry["payload_type"] is None or type_supported(entry["payload_type"]) for entry in variants), "business-variant-payload-types-supported", checks)
    require(all(entry["cardinality"] in {"one", "optional", "many", "many-unique"} for entry in properties), "business-property-cardinality-supported", checks)
    require(all((entry["cardinality"] == "many-unique") == entry["type"].startswith("Set<") for entry in properties), "business-property-set-cardinality-coherent", checks)
    require(all((entry["cardinality"] == "many") == entry["type"].startswith("List<") for entry in properties), "business-property-list-cardinality-coherent", checks)

    denominator_properties = denominator["record_properties"]
    denominator_variants = denominator["variants"]
    require(denominator["counts"] == {"record_properties": 22, "variants": 15, "rules": 8, "operations": 1}, "property-denominator-exact-counts", checks)
    require(len(denominator_properties) == denominator["counts"]["record_properties"], "property-denominator-record-count", checks)
    require(len(denominator_variants) == denominator["counts"]["variants"], "property-denominator-variant-count", checks)
    require(len(denominator["rules"]) == denominator["counts"]["rules"], "property-denominator-rule-count", checks)
    require_unique([entry["ontology_selector"] for entry in denominator_properties], "property-denominator-record-selectors-unique", checks)
    require_unique([entry["domainspec_selector"] for entry in denominator_properties], "property-denominator-domainspec-record-selectors-unique", checks)
    require_unique([entry["rust_symbol"] for entry in denominator_properties], "property-denominator-rust-record-symbols-unique", checks)
    require_unique([entry["ontology_selector"] for entry in denominator_variants], "property-denominator-variant-selectors-unique", checks)
    require_unique([entry["domainspec_selector"] for entry in denominator_variants], "property-denominator-domainspec-variant-selectors-unique", checks)
    require_unique([entry["rust_symbol"] for entry in denominator_variants], "property-denominator-rust-variant-symbols-unique", checks)
    require({entry["ontology_selector"] for entry in denominator_properties} == set(property_ids), "property-denominator-record-ontology-closure", checks)
    require({entry["ontology_selector"] for entry in denominator_variants} == set(variant_ids), "property-denominator-variant-ontology-closure", checks)
    require(set(denominator["rules"]) == set(rule_ids), "property-denominator-rule-ontology-closure", checks)
    property_types = {entry["property_id"]: entry["type"] for entry in properties}
    require(all(property_types[entry["ontology_selector"]] == entry["type"] for entry in denominator_properties), "property-denominator-type-fidelity", checks)

    feature = load(operation_root / "specs/auth-exact-permission/feature.json")
    nodes = {
        node_id: load(operation_root / f"specs/auth-exact-permission/nodes/{node_id}.json")
        for node_id in feature["nodes"]
    }
    edges = [
        load(operation_root / f"specs/auth-exact-permission/edges/{edge_id}.json")
        for edge_id in feature["edges"]
    ]
    require(len(nodes) == 17 and len(edges) == 10, "operation-source-exact-closure-size", checks)
    authored_properties: dict[str, str] = {}
    authored_variants: dict[str, str] = {}
    authored_rules: set[str] = set()
    authored_operations: set[str] = set()
    for node_id, node in nodes.items():
        contract = node["body"].get("typed_contract")
        require(contract is not None, f"operation-source-typed-contract:{node_id}", checks)
        schema = contract["schema_version"]
        if schema == "domainspec.typed-record/v1":
            for prop in contract["properties"]:
                authored_properties[prop["ontology_property"]] = f"auth-exact-permission:{node_id}#{prop['name']}"
        elif schema == "domainspec.typed-sum/v1":
            for variant in contract["variants"]:
                authored_variants[variant["ontology_variant"]] = f"auth-exact-permission:{node_id}#{variant['name']}"
        elif schema == "domainspec.typed-rule/v1":
            authored_rules.add(contract["ontology_rule"])
        elif schema == "domainspec.typed-operation/v1":
            authored_operations.add(contract["ontology_operation"])
        else:
            require(False, f"operation-source-typed-contract-version:{node_id}", checks)
    require(set(authored_properties) == set(property_ids), "operation-source-property-ontology-closure", checks)
    require(set(authored_variants) == set(variant_ids), "operation-source-variant-ontology-closure", checks)
    require(authored_rules == set(rule_ids), "operation-source-rule-ontology-closure", checks)
    require(authored_operations == {denominator["operation_id"]}, "operation-source-operation-ontology-closure", checks)
    require(all(authored_properties[entry["ontology_selector"]] == entry["domainspec_selector"] for entry in denominator_properties), "operation-source-property-selector-fidelity", checks)
    require(all(authored_variants[entry["ontology_selector"]] == entry["domainspec_selector"] for entry in denominator_variants), "operation-source-variant-selector-fidelity", checks)
    enforcing = {edge["source_node_id"] for edge in edges if edge["relationship"] == "enforces" and edge["target_node_id"] == "authorize"}
    reading = {edge["target_node_id"] for edge in edges if edge["relationship"] == "reads" and edge["source_node_id"] == "authorize"}
    require(len(enforcing) == 8 and all(nodes[node_id]["kind"] == "Rule" for node_id in enforcing), "operation-source-enforcing-rule-closure", checks)
    require(reading == {"session", "role"}, "operation-source-read-entity-closure", checks)

    for entry in denominator_properties:
        owner, field = entry["rust_symbol"].split("::", 1)
        record = re.search(rf"pub struct {re.escape(owner)}(?:<'[^>]+>)?\s*\{{(?P<body>.*?)\n\}}", runtime_source, re.DOTALL)
        require(record is not None and re.search(rf"\bpub {re.escape(field)}\s*:", record.group("body")) is not None, f"property-denominator-runtime-symbol:{owner}:{field}", checks)
    for entry in denominator_variants:
        owner, variant = entry["rust_symbol"].split("::", 1)
        enumeration = re.search(rf"pub enum {re.escape(owner)}\s*\{{(?P<body>.*?)\n\}}", runtime_source, re.DOTALL)
        require(enumeration is not None and re.search(rf"\b{re.escape(variant)}\b", enumeration.group("body")) is not None, f"property-denominator-runtime-variant:{owner}:{variant}", checks)


def validate_standard_candidate(checks: list[dict], write_receipt: bool) -> None:
    denominator = load(IMPLEMENTATION / "property-denominator.json")
    receipt_path = STANDARD_RUNTIME / ".domainspec/instantiations/auth-exact-permission.authorize.json"
    standard_receipt = load(receipt_path)
    closure = standard_receipt["semantic_contract"]["typed_closure"]
    generated_source_path = STANDARD_RUNTIME / "src/domainspec/rust/auth-exact-permission/authorize.rs"
    generated_source = generated_source_path.read_text(encoding="utf-8")

    receipt_check = command([str(TSX), str(DOMAINSPEC_CLI), "receipt", str(STANDARD_RUNTIME)])
    require(receipt_check.returncode == 0 and json.loads(receipt_check.stdout)["observation"]["result"] == "pass", "standard-cli-committed-target-observation", checks)
    require(closure["root_selector"] == "auth-exact-permission:authorize", "standard-closure-root", checks)
    require(len(closure["properties"]) == 22 and len(closure["variants"]) == 15 and len(closure["rules"]) == 8, "standard-closure-exact-counts", checks)

    property_rows = {row["ontology_property"]: row for row in closure["properties"]}
    variant_rows = {row["ontology_variant"]: row for row in closure["variants"]}
    rule_rows = {row["ontology_rule"]: row for row in closure["rules"]}
    coverage_rows: list[dict] = []
    for row in denominator["record_properties"]:
        compiled = property_rows.get(row["ontology_selector"])
        status = compiled is not None and compiled["domainspec_selector"] == row["domainspec_selector"] and row["rust_symbol"] in generated_source
        require(status, f"standard-property-coverage:{row['ontology_selector']}", checks)
        coverage_rows.append({**row, "compiled_ir_selector": compiled["domainspec_selector"], "status": "PASS"})
    variant_coverage: list[dict] = []
    for row in denominator["variants"]:
        compiled = variant_rows.get(row["ontology_selector"])
        status = compiled is not None and compiled["domainspec_selector"] == row["domainspec_selector"] and row["rust_symbol"] in generated_source
        require(status, f"standard-variant-coverage:{row['ontology_selector']}", checks)
        variant_coverage.append({**row, "compiled_ir_selector": compiled["domainspec_selector"], "status": "PASS"})
    rule_coverage: list[dict] = []
    for rule_id in denominator["rules"]:
        compiled = rule_rows.get(rule_id)
        rust_symbol = compiled["domainspec_selector"].split(":", 1)[1].replace("-", "_") if compiled is not None else None
        status = compiled is not None and compiled["domainspec_selector"] in generated_source and f"pub fn {rust_symbol}(" in generated_source
        require(status, f"standard-rule-coverage:{rule_id}", checks)
        rule_coverage.append({"ontology_selector": rule_id, "compiled_ir_selector": compiled["domainspec_selector"], "rust_symbol": rust_symbol, "status": "PASS"})

    run_summaries: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="domainspec-auth-standard-") as parent:
        parent_path = Path(parent)
        for name in ["left", "right"]:
            target = parent_path / name
            result = command([
                str(TSX), str(DOMAINSPEC_CLI), "instantiate", str(OPERATION_SOURCE),
                "--node", "auth-exact-permission:authorize", "--language", "rust", "--target-root", str(target),
            ])
            require(result.returncode == 0, f"standard-cli-clean-instantiation:{name}", checks)
            value = json.loads(result.stdout)
            require(value["result"] == "pass" and value["observation"]["result"] == "pass", f"standard-cli-clean-observation:{name}", checks)
            generated = next(record for record in value["observation"]["observed_artifacts"] if record["relative_path"].endswith("authorize.rs"))
            generated_path = target / generated["relative_path"]
            rust_format = command(["rustfmt", "--edition", "2024", "--check", str(generated_path)])
            require(rust_format.returncode == 0, f"standard-rustfmt-check:{name}", checks)
            strict_output = parent_path / f"{name}.rlib"
            strict_compile = command(["rustc", "--edition", "2024", "--crate-type", "lib", "-D", "warnings", str(generated_path), "-o", str(strict_output)])
            require(strict_compile.returncode == 0, f"standard-strict-rustc:{name}", checks)
            cargo_check = command(["cargo", "check"], target)
            require(cargo_check.returncode == 0, f"standard-cargo-check:{name}", checks)
            cargo_test = command(["cargo", "test"], target)
            require(cargo_test.returncode == 0, f"standard-cargo-test:{name}", checks)
            run_summaries.append({
                "plan_sha256": value["plan_sha256"],
                "receipt_sha256": value["receipt_sha256"],
                "artifact_sha256": generated["sha256"],
                "closure_sha256": load(target / value["receipt_path"])["semantic_contract"]["typed_closure"]["closure_sha256"],
            })
        require(run_summaries[0] == run_summaries[1], "standard-two-run-determinism", checks)
        require(run_summaries[0]["artifact_sha256"] == digest(generated_source_path), "standard-committed-artifact-current", checks)
        require(run_summaries[0]["receipt_sha256"] == standard_receipt["receipt_sha256"], "standard-committed-receipt-current", checks)

        behavior_binary = parent_path / "behavior-tests"
        behavior_build = command(["rustc", "--edition", "2024", "-Awarnings", "--test", str(STANDARD_BEHAVIOR), "-o", str(behavior_binary)])
        require(behavior_build.returncode == 0, "standard-behavior-harness-compiles", checks)
        behavior_runs = [command([str(behavior_binary)]) for _ in range(2)]
        for index, result in enumerate(behavior_runs, start=1):
            require(result.returncode == 0, f"standard-behavior-equivalence-run-{index:03d}", checks)

    theorem_path = AUTH_ROOT / "formalization/cases/AF-EXACT-SESSION-ROLE-PERMISSION-001/THEOREM-OBLIGATION-RECEIPT.v2.json"
    theorem = load(theorem_path)
    require(theorem["normalized_outcome"] == "theorem-checked", "standard-lean-characterization-current", checks)
    compiled_graph_path = IMPLEMENTATION / "standard-conformance/compiled-operation-graph.json"
    compiled_graph = {
        "schema_version": "domainspec.compiled-operation-graph/v1-candidate",
        "graph_id": "AUTH-STANDARD-OPERATION-GRAPH-001",
        "root_selector": closure["root_selector"],
        "source_manifest_sha256": standard_receipt["input"]["source_manifest_sha256"],
        "typed_closure": closure,
        "authority_effect": "none",
    }
    if write_receipt:
        compiled_graph_path.write_text(encoded(compiled_graph), encoding="utf-8")
    require(compiled_graph_path.is_file(), "standard-compiled-operation-graph-present", checks)
    if not write_receipt:
        require(load(compiled_graph_path) == compiled_graph, "standard-compiled-operation-graph-current", checks)

    business_ontology_path = IMPLEMENTATION / "business-ontology.json"
    denominator_path = IMPLEMENTATION / "property-denominator.json"
    construction_binding_path = IMPLEMENTATION / "domainspec/construction-binding.json"
    system_ontology_path = IMPLEMENTATION / "standard-conformance/system-ontology.json"
    system_ontology = {
        "schema_version": "auth-foundation.standard-operation-system-ontology/v1-candidate",
        "ontology_id": "auth-foundation.system.standard-exact-session-role-permission",
        "root_operation": closure["operation"]["ontology_operation"],
        "construction_binding": {"path": str(construction_binding_path.relative_to(AUTH_ROOT)), "sha256": digest(construction_binding_path)},
        "business_ontology": {"path": str(business_ontology_path.relative_to(AUTH_ROOT)), "sha256": digest(business_ontology_path)},
        "property_denominator": {"path": str(denominator_path.relative_to(AUTH_ROOT)), "sha256": digest(denominator_path)},
        "compiled_graph": {"path": str(compiled_graph_path.relative_to(AUTH_ROOT)), "sha256": digest(compiled_graph_path), "closure_sha256": closure["closure_sha256"]},
        "semantic_coverage": {
            "properties": [row["ontology_property"] for row in closure["properties"]],
            "variants": [row["ontology_variant"] for row in closure["variants"]],
            "rules": [row["ontology_rule"] for row in closure["rules"]],
            "counts": {"properties": 22, "variants": 15, "rules": 8, "operations": 1},
            "status": "closed",
        },
        "lifecycle_status": "validated-local-candidate",
        "authority_effect": "none",
        "external_effect": "none",
    }
    if write_receipt:
        system_ontology_path.write_text(encoded(system_ontology), encoding="utf-8")
    require(system_ontology_path.is_file(), "standard-operation-system-ontology-present", checks)
    if not write_receipt:
        require(load(system_ontology_path) == system_ontology, "standard-operation-system-ontology-current", checks)

    evidence = {
        "schema_version": "auth-foundation.standard-operation-conformance/v1-candidate",
        "receipt_id": "AUTH-STANDARD-OPERATION-CONFORMANCE-001",
        "source_manifest_sha256": standard_receipt["input"]["source_manifest_sha256"],
        "typed_closure_sha256": closure["closure_sha256"],
        "system_ontology": {"path": str(system_ontology_path.relative_to(AUTH_ROOT)), "sha256": digest(system_ontology_path), "lifecycle_status": system_ontology["lifecycle_status"]},
        "standard_instantiation": {
            "receipt_path": str(receipt_path.relative_to(AUTH_ROOT)),
            "receipt_sha256": digest(receipt_path),
            "plan_sha256": standard_receipt["plan_sha256"],
            "generated_source_path": str(generated_source_path.relative_to(AUTH_ROOT)),
            "generated_source_sha256": digest(generated_source_path),
            "deterministic_runs": 2,
        },
        "coverage": {"properties": coverage_rows, "variants": variant_coverage, "rules": rule_coverage, "result": "PASS"},
        "compilation": {"cargo_check_runs": 2, "cargo_test_runs": 2, "strict_rustc_runs": 2, "rustfmt_check_runs": 2, "result": "PASS"},
        "behavioral_equivalence": {
            "oracle_path": str((RUNTIME / "src/lib.rs").relative_to(AUTH_ROOT)),
            "oracle_sha256": digest(RUNTIME / "src/lib.rs"),
            "harness_path": str(STANDARD_BEHAVIOR.relative_to(AUTH_ROOT)),
            "harness_sha256": digest(STANDARD_BEHAVIOR),
            "case_count": 24,
            "deterministic_runs": 2,
            "normative_allow_deny_result": "PASS",
            "detailed_deny_reason_equivalence": "not-claimed",
        },
        "formal_characterization": {
            "path": str(theorem_path.relative_to(AUTH_ROOT)),
            "sha256": digest(theorem_path),
            "status": theorem["normalized_outcome"],
        },
        "result": "local-standard-operation-conformance-candidate-pass",
        "authority_effect": "none",
        "external_effect": "none",
        "claim_limit": "Local candidate evidence for structural closure, a deterministic system-ontology candidate, generation, compilation, normative Allow/Deny parity, and current Lean characterization; no ontology admission, acceptance, publication, deployment, or production-service claim.",
    }
    evidence_path = IMPLEMENTATION / "standard-conformance/receipt.json"
    if write_receipt:
        evidence_path.write_text(encoded(evidence), encoding="utf-8")
    require(evidence_path.is_file(), "standard-conformance-receipt-present", checks)
    if not write_receipt:
        require(load(evidence_path) == evidence, "standard-conformance-receipt-current", checks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipt", action="store_true")
    args = parser.parse_args()
    checks: list[dict] = []

    json_paths = sorted(path for path in IMPLEMENTATION.rglob("*.json") if "target" not in path.parts)
    for path in json_paths:
        load(path)
    require(bool(json_paths), "implementation-json-parses", checks)
    validate_property_denominator(checks)
    validate_standard_candidate(checks, args.write_receipt)

    generator_checks = [
        command([str(NODE), str(AUTH_KERNEL_TOOL), "check", str(IMPLEMENTATION / "domainspec"), str(RUNTIME)])
        for _ in range(2)
    ]
    for index, result in enumerate(generator_checks, start=1):
        require(result.returncode == 0, f"domainspec-auth-kernel-generator-check-{index:03d}", checks)

    capability_schema = load(REPOSITORY / "cyberAlchemy-v2/capability/schemas/capability.schema.json")
    capability_schema["$ref"] = "#/$defs/productCapability"
    capability = load(IMPLEMENTATION / "product-capability.json")
    capability_errors = list(jsonschema.Draft202012Validator(capability_schema).iter_errors(capability))
    require(not capability_errors, "product-capability-schema", checks)

    binding_path = IMPLEMENTATION / "domainspec" / "construction-binding.json"
    binding = load(binding_path)
    predecessors = binding["predecessors"]
    for name, record in predecessors.items():
        path = AUTH_ROOT / record["path"]
        require(path.is_file() and digest(path) == record["sha256"], f"predecessor-current:{name}", checks)

    graph_path = GENERATED / "graph.json"
    system_path = GENERATED / "system-ontology.json"
    projection_path = GENERATED / "system-ontology-receipt.json"
    implementation_binding_path = RUNTIME / "implementation-binding.json"
    graph = load(graph_path)
    system = load(system_path)
    projection = load(projection_path)
    implementation_binding = load(implementation_binding_path)
    instantiation_receipt_path = RUNTIME / "DOMAINSPEC-INSTANTIATION-RECEIPT.json"
    instantiation_receipt = load(instantiation_receipt_path)

    require(projection["status"] == "pass" and projection["deterministic_runs"] == 2, "domainspec-two-run-determinism", checks)
    require(projection["source_graph_digest"] == digest(graph_path), "compiled-graph-current", checks)
    require(projection["system_ontology_digest"] == digest(system_path), "system-ontology-current", checks)
    require(system["construction_binding"]["sha256"] == digest(binding_path), "construction-binding-current", checks)
    require(system["semantic_coverage"]["status"] == "closed", "semantic-coverage-closed", checks)
    require(
        implementation_binding["bound_predecessor"]["system_ontology_sha256"] == digest(system_path),
        "implementation-system-binding-current",
        checks,
    )
    require(implementation_binding["implementation"]["generated"] is True, "implementation-generated-by-domainspec-cli", checks)
    require(
        implementation_binding["implementation"]["generator"]["receipt_sha256"] == digest(instantiation_receipt_path),
        "generator-receipt-current",
        checks,
    )
    require(
        instantiation_receipt["baseline"]["id"] == "domainspec-meta-types-current-implemented@10",
        "generator-baseline-current",
        checks,
    )
    generated_lib = next(record for record in instantiation_receipt["artifacts"] if record["relative_path"] == "src/lib.rs")
    require(generated_lib["sha256"] == digest(RUNTIME / "src/lib.rs"), "generated-rust-source-current", checks)
    for record in implementation_binding["implementation"]["files"].values():
        path = AUTH_ROOT / record["path"]
        require(path.is_file() and digest(path) == record["sha256"], f"implementation-file-current:{path.name}", checks)

    fmt = command(["cargo", "fmt", "--check"], RUNTIME)
    require(fmt.returncode == 0, "cargo-fmt", checks)
    check = command(["cargo", "check", "--all-targets"], RUNTIME)
    require(check.returncode == 0, "cargo-check", checks)

    test_runs = [command(["cargo", "test", "--all-targets"], RUNTIME) for _ in range(2)]
    for index, result in enumerate(test_runs, start=1):
        require(result.returncode == 0, f"cargo-test-run-{index:03d}", checks)
    listing = command(["cargo", "test", "--all-targets", "--", "--list"], RUNTIME)
    require(listing.returncode == 0, "cargo-test-inventory", checks)
    test_names = sorted(
        line.rsplit(": test", 1)[0]
        for line in listing.stdout.splitlines()
        if line.endswith(": test")
    )
    require(len(test_names) >= 12, "rust-test-coverage-floor", checks)

    clippy = command(["cargo", "clippy", "--all-targets", "--", "-D", "warnings"], RUNTIME)
    clippy_missing = "clippy" in (clippy.stderr + clippy.stdout).lower() and "not installed" in (clippy.stderr + clippy.stdout).lower()
    if clippy_missing:
        checks.append({"check_id": "cargo-clippy", "status": "not_evaluable", "causal_blocker": "cargo-clippy component is not installed"})
    else:
        require(clippy.returncode == 0, "cargo-clippy", checks)

    rustc = command(["rustc", "--version"]).stdout.strip()
    cargo = command(["cargo", "--version"]).stdout.strip()
    theorem_path = AUTH_ROOT / "formalization/cases/AF-EXACT-SESSION-ROLE-PERMISSION-001/THEOREM-OBLIGATION-RECEIPT.v2.json"
    theorem = load(theorem_path)
    require(theorem["normalized_outcome"] == "theorem-checked", "lean-theorem-evidence-current", checks)

    proof_tests = {
        "AF-PROOF-LEAN-CHARACTERIZATION": ["permitted_case_exact_active_role_grant_allows", "decision_is_total_and_default_deny_for_near_matches"],
        "AF-PROOF-PERMITTED-CASE": ["permitted_case_exact_active_role_grant_allows", "any_one_exact_active_role_grant_is_sufficient"],
        "AF-PROOF-ADMISSIBLE-WITHOUT-GRANT": ["active_role_without_grant_denies"],
        "AF-PROOF-INADMISSIBLE": ["inadmissible_missing_session_denies", "ambiguous_session_resolution_denies", "inactive_or_revoked_session_denies", "expiry_boundary_is_fail_closed", "stale_authorization_revision_denies", "missing_or_untrusted_scope_evidence_denies", "incomplete_active_role_relation_denies", "missing_extra_or_duplicate_resolved_roles_deny"],
        "AF-PROOF-EXACT-MISMATCH-DENY": ["resource_action_or_scope_mismatch_denies"],
        "AF-PROOF-IMPLEMENTATION-EQUIVALENCE": ["decision_is_total_and_default_deny_for_near_matches"],
    }
    require(all(name in test_names for names in proof_tests.values() for name in names), "proof-test-reference-closure", checks)

    receipt = {
        "schema_version": "auth-foundation.rust-conformance-receipt/v1-candidate",
        "receipt_id": "AUTH-RECEIPT-D65-RUST-CONFORMANCE-001",
        "recorded_at": "2026-08-31",
        "implementation_binding": {
            "binding_id": implementation_binding["binding_id"],
            "path": "implementation/runtime/implementation-binding.json",
            "sha256": digest(implementation_binding_path),
        },
        "system_ontology": {
            "ontology_id": system["ontology_id"],
            "path": "implementation/domainspec/generated/system-ontology.json",
            "sha256": digest(system_path),
            "lifecycle_status": system["lifecycle_status"],
        },
        "formal_evidence": {
            "path": str(theorem_path.relative_to(AUTH_ROOT)),
            "sha256": digest(theorem_path),
            "proof_status": theorem["proof_status"],
        },
        "toolchain": {"rustc": rustc, "cargo": cargo},
        "checks": checks,
        "rust_tests": {"count": len(test_names), "names": test_names, "deterministic_runs": 2},
        "proof_requirements": [
            {"proof_id": proof_id, "status": "PASS", "test_refs": names}
            for proof_id, names in proof_tests.items()
        ],
        "result": "local-conformance-candidate-pass",
        "runtime_evidence": "not-claimed",
        "authority_effect": "none",
        "external_effect": "none",
        "claim_limit": "Local static conformance candidate for DomainSpec CLI-generated Rust and exact bound bytes; no integrated resolver, service, deployment, or production-security claim.",
    }
    receipt_path = RUNTIME / "conformance-receipt.json"

    standard_compiled_graph_path = IMPLEMENTATION / "standard-conformance/compiled-operation-graph.json"
    standard_system_ontology_path = IMPLEMENTATION / "standard-conformance/system-ontology.json"
    standard_instantiation_path = IMPLEMENTATION / "standard-runtime/.domainspec/instantiations/auth-exact-permission.authorize.json"
    standard_conformance_path = IMPLEMENTATION / "standard-conformance/receipt.json"
    stages = [
        ("canonical_definitions", AUTH_ROOT / predecessors["canonical_definitions"]["path"], "validated"),
        ("product_capability", AUTH_ROOT / predecessors["product_capability"]["path"], "validated-candidate"),
        ("business_ontology", AUTH_ROOT / predecessors["business_ontology"]["path"], "validated-candidate"),
        ("domainspec_source", OPERATION_SOURCE / "project.json", "validated"),
        ("compiled_graph", standard_compiled_graph_path, "validated"),
        ("system_ontology", standard_system_ontology_path, "validated-local-candidate"),
        ("implementation", standard_instantiation_path, "validated-local-candidate"),
        ("static_conformance", standard_conformance_path, "validated-local-candidate"),
    ]
    if args.write_receipt:
        receipt_path.write_text(encoded(receipt), encoding="utf-8")
    require(receipt_path.is_file(), "conformance-receipt-present", checks)
    if not args.write_receipt:
        require(load(receipt_path)["implementation_binding"]["sha256"] == digest(implementation_binding_path), "conformance-receipt-current", checks)

    chain = {
        "schema_version": "cav2-d65-construction-chain/v1-candidate",
        "construction_id": binding["binding_id"],
        "subject_ref": "CA2-CAP-DECIDE-EXACT-SESSION-ROLE-PERMISSION",
        "stages": [
            {
                "stage": name,
                "state": state,
                "path": str(path.relative_to(AUTH_ROOT)),
                "sha256": digest(path),
            }
            for name, path, state in stages
        ] + [{"stage":"runtime_evidence","state":"absent","path":None,"sha256":None}],
        "result": "complete-local-candidate-through-static-conformance",
        "authority_effect": "none",
        "external_effect": "none",
        "claim_limit": "Complete local candidate D65 chain through static conformance; runtime integration, publication, deployment, and production security remain outside scope.",
    }
    chain_path = IMPLEMENTATION / "d65-chain.json"
    if args.write_receipt:
        chain_path.write_text(encoded(chain), encoding="utf-8")
    require(chain_path.is_file(), "d65-chain-present", checks)

    summary = {
        "status": "pass",
        "checks": len(checks),
        "rust_tests": len(test_names),
        "construction_id": binding["binding_id"],
        "system_ontology_sha256": digest(system_path),
        "implementation_binding_sha256": digest(implementation_binding_path),
        "conformance_receipt_sha256": digest(receipt_path),
        "standard_operation_system_ontology_sha256": digest(standard_system_ontology_path),
        "standard_operation_receipt_sha256": digest(standard_instantiation_path),
        "standard_operation_conformance_sha256": digest(standard_conformance_path),
        "comparison_oracle_implementation_binding_sha256": digest(implementation_binding_path),
        "runtime_evidence": "not-claimed",
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(json.dumps({"status": "fail", "blocker": str(error)}, indent=2))
        raise SystemExit(1)
