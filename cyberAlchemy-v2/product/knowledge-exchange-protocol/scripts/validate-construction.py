#!/usr/bin/env python3
"""Validate the accepted model -> DomainSpec -> Rust candidate construction chain."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
ACCEPTED_DIGEST = "c9681ea0c08ff56e06be9a582faba23cf347c19fb8ce3ff083e4870ab169a435"


def load(relative: str, errors: list[str]) -> dict[str, Any]:
    path = PACKAGE_ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load {relative}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{relative} must contain one JSON object")
        return {}
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expect(actual: Any, expected: Any, label: str, errors: list[str]) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, observed {actual!r}")


def validate_accepted_model(errors: list[str]) -> None:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        ["python3", str(PACKAGE_ROOT / "validate.py")],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        errors.append(f"accepted model validator failed: {completed.stderr or completed.stdout}")
        return
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        errors.append(f"accepted model validator returned invalid JSON: {exc}")
        return
    expect(result.get("status"), "PASS", "accepted model status", errors)
    expect(result.get("material_digest"), ACCEPTED_DIGEST, "accepted model digest", errors)


def verify_generated_build(errors: list[str]) -> None:
    command = [
        str(REPOSITORY_ROOT / "toolchains/node-typescript/bin/node-env"),
        "run",
        "--project",
        "projects/domainspec-v2/impl",
        "--",
        "node",
        "--import",
        "tsx",
        "../../../cyberAlchemy-v2/product/knowledge-exchange-protocol/scripts/build.ts",
        "--emit-json",
    ]
    completed = subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        errors.append(f"DomainSpec rebuild failed: {completed.stderr or completed.stdout}")
        return
    try:
        artifacts = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        errors.append(f"DomainSpec rebuild returned invalid JSON: {exc}")
        return
    generated = PACKAGE_ROOT / "domainspec/generated"
    for name, expected_bytes in artifacts.items():
        path = generated / name
        if not path.is_file():
            errors.append(f"generated artifact missing: {name}")
        elif path.read_text(encoding="utf-8") != expected_bytes:
            errors.append(f"generated artifact drift: {name}")


def verify_runtime(errors: list[str]) -> None:
    manifest = PACKAGE_ROOT / "runtime/Cargo.toml"
    formatting = subprocess.run(
        ["cargo", "fmt", "--manifest-path", str(manifest), "--", "--check"],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if formatting.returncode != 0:
        errors.append(f"Rust formatting failed: {formatting.stderr or formatting.stdout}")
    with tempfile.TemporaryDirectory(prefix="cav2-kep-cargo-") as target:
        environment = dict(os.environ)
        environment["CARGO_TARGET_DIR"] = target
        tests = subprocess.run(
            ["cargo", "test", "--manifest-path", str(manifest)],
            cwd=REPOSITORY_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
    if tests.returncode != 0:
        errors.append(f"Rust tests failed: {tests.stderr or tests.stdout}")


def validate(verify_build: bool = False, verify_rust: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    acceptance = load("decisions/model-acceptance.json", errors)
    build = load("domainspec/generated/build-receipt.json", errors)
    projection = load("domainspec/generated/system-ontology-receipt.json", errors)
    system = load("domainspec/generated/system-ontology.json", errors)
    binding = load("implementation/implementation-binding.json", errors)
    assessment = load("conformance/assessment.json", errors)

    validate_accepted_model(errors)
    expect(acceptance.get("accepted_material_digest"), ACCEPTED_DIGEST, "acceptance digest", errors)
    expect(acceptance.get("effect_authorized"), False, "acceptance effect ceiling", errors)
    expect(build.get("status"), "pass", "DomainSpec build status", errors)
    expect(build.get("source_set_digest"), binding.get("domainspec", {}).get("source_set_digest"), "source-set binding", errors)
    expect(build.get("artifacts", {}).get("graph_digest"), binding.get("domainspec", {}).get("graph_sha256"), "graph binding", errors)
    expect(projection.get("deterministic_runs"), 2, "projection deterministic runs", errors)
    expect(projection.get("equal_graph_bytes"), True, "equal graph bytes", errors)
    expect(projection.get("equal_system_ontology_bytes"), True, "equal system ontology bytes", errors)
    expect(projection.get("profile_release_admission"), "not-granted", "profile admission", errors)
    expect(projection.get("accepted_model_digest"), ACCEPTED_DIGEST, "projection accepted model", errors)

    bound_domainspec = binding.get("domainspec", {})
    bound_impl = binding.get("implementation", {})
    bound_accepted = binding.get("accepted_model", {})
    hash_bindings = (
        ("decisions/model-acceptance.json", bound_accepted.get("decision_sha256")),
        ("domainspec/development-profile.json", bound_domainspec.get("profile_sha256")),
        ("domainspec/generated/graph.json", bound_domainspec.get("graph_sha256")),
        ("domainspec/generated/system-ontology.json", bound_domainspec.get("system_ontology_sha256")),
        ("runtime/Cargo.toml", bound_impl.get("manifest_sha256")),
        ("runtime/Cargo.lock", bound_impl.get("lockfile_sha256")),
        ("runtime/src/lib.rs", bound_impl.get("target_sha256")),
        ("runtime/tests/protocol.rs", bound_impl.get("test_sha256")),
    )
    for relative, expected_hash in hash_bindings:
        path = PACKAGE_ROOT / relative
        if not path.is_file():
            errors.append(f"bound file missing: {relative}")
        else:
            expect(sha256(path), expected_hash, f"bound digest {relative}", errors)

    contract = system.get("implementation_contract", {})
    expect(contract.get("product_capability_ref"), binding.get("capability_ref"), "system capability binding", errors)
    expect(contract.get("business_ontology_ref"), binding.get("business_ontology_ref"), "system business ontology binding", errors)
    expect(contract.get("implementation_target_ref"), bound_impl.get("target_path"), "system implementation target", errors)
    expect(contract.get("permitted_operations"), bound_impl.get("permitted_operations"), "permitted operation binding", errors)
    expect(contract.get("solana_binding"), "not-present", "Solana claim ceiling", errors)
    expect(contract.get("economic_effect"), "none", "economic effect ceiling", errors)

    binding_path = PACKAGE_ROOT / "implementation/implementation-binding.json"
    expect(sha256(binding_path), assessment.get("binding_sha256"), "assessment binding digest", errors)
    expect(binding.get("binding_status"), "candidate", "binding status", errors)
    expect(binding.get("conformance_status"), "not_evaluable", "binding conformance status", errors)
    expect(assessment.get("rust_test_count"), 11, "Rust test count", errors)
    expect(assessment.get("local_behavioral_evidence"), "PASS", "local behavioral evidence", errors)
    expect(assessment.get("aggregate_conformance"), "NOT_EVALUABLE", "aggregate conformance", errors)
    if not assessment.get("causal_blockers"):
        errors.append("aggregate conformance must retain causal blockers")
    test_source = (PACKAGE_ROOT / "runtime/tests/protocol.rs").read_text(encoding="utf-8")
    expect(test_source.count("#[test]"), 11, "Rust source test count", errors)

    if verify_build:
        verify_generated_build(errors)
    if verify_rust:
        verify_runtime(errors)

    return {
        "schema_version": "cav2-knowledge-exchange-construction-validation/v1",
        "status": "PASS" if not errors else "BLOCK",
        "accepted_model_digest": ACCEPTED_DIGEST,
        "domainspec_source_set_digest": build.get("source_set_digest"),
        "graph_digest": build.get("artifacts", {}).get("graph_digest"),
        "system_ontology_digest": projection.get("system_ontology_digest"),
        "rust_binding_digest": sha256(binding_path) if binding_path.is_file() else None,
        "local_behavioral_evidence": "PASS" if not errors else "BLOCK",
        "aggregate_conformance": "NOT_EVALUABLE",
        "causal_blockers": assessment.get("causal_blockers", []),
        "effect_authorized": False,
        "authority_effect": "none",
        "claim_ceiling": "Validated local candidate construction and Rust behavior only; no cryptographic security, Solana compatibility, aggregate conformance, publication, release, deployment, or external-effect authority.",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-build", action="store_true")
    parser.add_argument("--verify-rust", action="store_true")
    args = parser.parse_args()
    result = validate(verify_build=args.verify_build, verify_rust=args.verify_rust)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
