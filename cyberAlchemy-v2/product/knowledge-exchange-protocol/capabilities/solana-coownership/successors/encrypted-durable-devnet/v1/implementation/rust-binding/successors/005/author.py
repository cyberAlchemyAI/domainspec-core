#!/usr/bin/env python3
"""Author exact successor binding 005 for the bounded Solana graph repair."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import tomllib
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
V1_ROOT = HERE.parents[3]
KEP_ROOT = V1_ROOT.parents[4]
POLICY_PATH = HERE / "policy.json"
BINDING_PATH = HERE / "generated" / "implementation-binding.json"
PREACCEPTANCE_PATH = HERE / "generated" / "preacceptance-001.json"
AUTHOR_DECISION_PATH = HERE / "generated" / "author-decision.json"
TEST_PATH = HERE / "tests" / "test_author.py"


class BindingError(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BindingError(message)


def path_null_digest(entries: list[tuple[str, bytes]]) -> str:
    digest = hashlib.sha256()
    for relative, raw in sorted(entries):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(raw)
        digest.update(b"\0")
    return digest.hexdigest()


def exact_json(relative: str, expected_sha: str, label: str) -> tuple[Path, dict[str, Any]]:
    path = V1_ROOT / relative
    require(path.is_file(), f"missing {label}: {relative}")
    require(sha256_file(path) == expected_sha, f"{label} drift: {relative}")
    return path, load_json(path)


def exact_file(path: Path, expected_sha: str, label: str) -> bytes:
    require(path.is_file(), f"missing {label}: {path}")
    raw = path.read_bytes()
    require(sha256_bytes(raw) == expected_sha, f"{label} drift: {path}")
    return raw


def locate_cached_manifest(crate: str, version: str) -> Path:
    cargo_home = Path(os.environ.get("CARGO_HOME", str(Path.home() / ".cargo")))
    matches = sorted((cargo_home / "registry" / "src").glob(f"*/{crate}-{version}/Cargo.toml"))
    require(len(matches) == 1, f"expected exactly one cached {crate} {version} manifest, found {len(matches)}")
    return matches[0]


def dependency_map(binding: dict[str, Any]) -> dict[str, dict[str, Any]]:
    dependencies = binding["rust_substrate"]["dependencies"]
    mapped = {item["name"]: item for item in dependencies}
    require(len(mapped) == len(dependencies), "dependency names are not unique")
    return mapped


def verify_manifest_contracts(manifests: dict[str, dict[str, Any]]) -> None:
    program_test = manifests["solana-program-test"]
    require(program_test["features"].get("agave-unstable-api") == [], "program-test unstable API feature drift")
    require(program_test["dependencies"]["solana-address"]["version"] == ">=2.6.1,<2.7.0", "program-test address range drift")
    require(program_test["dependencies"]["solana-transaction"]["version"] == ">=4.1.4,<4.2.0", "program-test transaction range drift")

    runtime_transaction = manifests["solana-runtime-transaction"]
    require(runtime_transaction["dependencies"]["solana-transaction"]["features"] == ["wincode"], "runtime-transaction wincode selection drift")
    require(runtime_transaction["dependencies"]["wincode"]["version"] == "0.5.5", "runtime-transaction wincode version drift")

    transaction = manifests["solana-transaction"]
    required_transaction_wincode = ["dep:solana-signer", "dep:wincode", "solana-short-vec/wincode", "solana-message/wincode", "solana-signature/wincode"]
    require(transaction["features"]["wincode"] == required_transaction_wincode, "transaction wincode feature contract drift")
    require(transaction["dependencies"]["solana-address"]["version"] == "2.6.1", "transaction address version drift")
    require(transaction["dependencies"]["wincode"]["version"] == "0.5.0", "transaction wincode family drift")

    message = manifests["solana-message"]
    require(message["dependencies"]["solana-address"]["version"] == ">=2.6.1,<2.7.0", "message address range drift")
    require(message["dependencies"]["wincode"]["version"] == "0.5.0", "message wincode family drift")

    instruction = manifests["solana-instruction"]
    require(instruction["dependencies"]["solana-pubkey"]["version"] == ">=4.2.0,<4.3.0", "instruction pubkey range drift")
    require(instruction["dependencies"]["wincode"]["version"] == "0.5.0", "instruction wincode family drift")

    pubkey = manifests["solana-pubkey"]
    require(pubkey["features"]["wincode"] == ["solana-address/wincode"], "pubkey wincode propagation drift")

    address = manifests["solana-address"]
    require(address["features"]["wincode"] == ["dep:wincode"], "address wincode feature drift")
    require(address["dependencies"]["wincode"]["version"] == "0.5.0", "address wincode family drift")


def verify_inputs(policy: dict[str, Any]) -> dict[str, Any]:
    expected_repair = [
        {
            "dependency": "solana-program-test",
            "from": {"version": "=4.1.2", "default_features": False, "features": ["agave-unstable-api"]},
            "to": {"version": "=4.2.2", "default_features": False, "features": ["agave-unstable-api"]},
        },
        {
            "dependency": "solana-transaction",
            "from": {"version": "=4.1.1", "default_features": False, "features": ["wincode"]},
            "to": {"version": "=4.1.4", "default_features": False, "features": ["wincode"]},
        },
        {
            "dependency": "solana-instruction",
            "from": {"version": "=3.4.0", "default_features": False, "features": ["std"]},
            "to": {"version": "=3.4.1", "default_features": False, "features": ["std"]},
        },
        {
            "dependency": "solana-pubkey",
            "from": {"version": "=4.2.0", "default_features": False, "features": ["std"]},
            "to": {"version": "=4.2.0", "default_features": False, "features": ["std"]},
        },
        {
            "dependency": "solana-address",
            "from": None,
            "to": {"version": "=2.6.1", "kind": "runtime-and-test", "default_features": False, "features": []},
        },
    ]
    require(policy["exact_graph_repair"] == expected_repair, "exact five-entry graph repair drift")

    prior = policy["superseded_binding"]
    prior_policy_path, prior_policy = exact_json(prior["policy_path"], prior["policy_sha256"], "binding 004 policy")
    _, prior_binding = exact_json(prior["binding_path"], prior["binding_sha256"], "binding 004 candidate")
    _, acceptance = exact_json(prior["acceptance_decision_path"], prior["acceptance_decision_sha256"], "binding 004 acceptance")

    prior_material = path_null_digest([
        ("policy.json", prior_policy_path.read_bytes()),
        ("generated/implementation-binding.json", canonical_bytes(prior_binding)),
    ])
    require(prior_material == prior["binding_material_digest"], "binding 004 material digest does not reproduce")
    require(prior_binding["binding_id"] == prior["binding_id"], "binding 004 identity mismatch")
    require(acceptance["decision_id"] == prior["acceptance_decision_id"], "binding 004 acceptance identity mismatch")
    require(acceptance["acceptance"]["lifecycle_status"] == "accepted", "binding 004 is not accepted")
    require(acceptance["acceptance"]["accepted_binding_material_digest"] == prior_material, "binding 004 accepted digest mismatch")

    ontology = policy["selected_ontology_dependency"]
    selected_ontology = prior_binding["selected_dependencies"]["admitted_system_ontology"]
    require(selected_ontology["ontology_id"] == ontology["ontology_id"], "selected ontology identity drift")
    require(selected_ontology["candidate_set_digest"] == ontology["accepted_candidate_set_digest"], "selected ontology digest drift")
    require(selected_ontology["selectors"] == ontology["selectors"], "selected ontology selector drift")
    require(prior_binding["selected_dependencies"]["semantic_profiles"] == ontology["semantic_profiles"], "selected semantic profile drift")

    projection = policy["current_accepted_projection"]
    projection_path = KEP_ROOT / projection["path"]
    projection_raw = exact_file(projection_path, projection["sha256"], "current accepted Cargo projection")
    projection_text = projection_raw.decode("utf-8")
    for declaration in [
        'solana-instruction = { version = "=3.4.0", default-features = false, features = ["std"] }',
        'solana-pubkey = { version = "=4.2.0", default-features = false, features = ["std"] }',
        'solana-program-test = { version = "=4.1.2", default-features = false, features = ["agave-unstable-api"] }',
        'solana-transaction = { version = "=4.1.1", default-features = false, features = ["wincode"] }',
    ]:
        require(declaration in projection_text, f"accepted Cargo projection declaration drift: {declaration}")

    manifests: dict[str, dict[str, Any]] = {}
    for evidence in policy["cached_manifest_evidence"]:
        manifest_path = locate_cached_manifest(evidence["crate"], evidence["version"])
        raw = exact_file(manifest_path, evidence["sha256"], f"cached {evidence['crate']} manifest")
        parsed = tomllib.loads(raw.decode("utf-8"))
        require(parsed["package"]["name"] == evidence["crate"], f"cached {evidence['crate']} package identity drift")
        require(parsed["package"]["version"] == evidence["version"], f"cached {evidence['crate']} package version drift")
        manifests[evidence["crate"]] = parsed
    verify_manifest_contracts(manifests)

    probe = policy["isolated_probe"]
    probe_manifest_raw = exact_file(Path(probe["manifest_path"]), probe["manifest_sha256"], "isolated probe manifest")
    probe_lock_raw = exact_file(Path(probe["lock_path"]), probe["lock_sha256"], "isolated probe lock")
    probe_manifest = tomllib.loads(probe_manifest_raw.decode("utf-8"))
    for dependency, expected in {item["dependency"]: item["to"] for item in policy["exact_graph_repair"]}.items():
        selected = probe_manifest["dependencies"][dependency]
        require(selected["version"] == expected["version"], f"probe {dependency} version drift")
        require(selected.get("default-features", True) == expected["default_features"], f"probe {dependency} default-features drift")
        if dependency != "solana-instruction":
            require(selected.get("features", []) == expected["features"], f"probe {dependency} feature drift")

    probe_lock = tomllib.loads(probe_lock_raw.decode("utf-8"))
    locked = {(item["name"], item["version"]) for item in probe_lock["package"]}
    for package, version in probe["expected_packages"].items():
        require((package, version) in locked, f"probe lock missing {package} {version}")
    for forbidden in probe["forbidden_wincode_versions"]:
        require(("wincode", forbidden) not in locked, f"probe lock contains forbidden wincode {forbidden}")

    dependencies = dependency_map(prior_binding)
    require(len(dependencies) == 16, "binding 004 dependency closure drift")
    for change in policy["exact_graph_repair"]:
        old = change["from"]
        if old is None:
            require(change["dependency"] not in dependencies, f"binding 004 unexpectedly contains {change['dependency']}")
            continue
        actual = dependencies[change["dependency"]]
        require(actual["version"] == old["version"], f"binding 004 {change['dependency']} version drift")
        require(actual["default_features"] == old["default_features"], f"binding 004 {change['dependency']} default-features drift")
        require(actual["features"] == old["features"], f"binding 004 {change['dependency']} feature drift")

    require(prior_binding["rust_substrate"]["minimum_rust_version"] == policy["preservation"]["minimum_rust_version"], "Rust version drift")
    require(len(prior_binding["planned_targets"]) == policy["preservation"]["planned_target_count"], "planned target closure drift")
    require(len(prior_binding["forbidden_capabilities"]) == 9, "forbidden capability closure drift")
    require(prior_binding["authority_effect"] == prior_binding["implementation_effect"] == prior_binding["external_effect"] == "none", "binding 004 candidate effect ceiling drift")
    return {"prior_binding": prior_binding}


def build_binding(policy_override: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = copy.deepcopy(policy_override) if policy_override is not None else load_json(POLICY_PATH)
    prior = verify_inputs(policy)["prior_binding"]
    binding = copy.deepcopy(prior)
    binding["binding_id"] = policy["binding_id"]
    binding["policy_id"] = policy["policy_id"]
    binding["source_authorization"] = policy["source_authorization"]
    binding["supersession"] = {
        "supersedes_binding_id": policy["superseded_binding"]["binding_id"],
        "supersedes_accepted_material_digest": policy["superseded_binding"]["binding_material_digest"],
        "cause": policy["causal_defect"],
        "change_set": policy["exact_graph_repair"],
        "all_other_construction_semantics": "byte-equivalent-after-successor-metadata-provider-label-and-dependency-graph-normalization",
    }

    dependencies = binding["rust_substrate"]["dependencies"]
    mapped = dependency_map(binding)
    for change in policy["exact_graph_repair"]:
        target = change["to"]
        if change["from"] is None:
            insertion = {
                "name": change["dependency"],
                "version": target["version"],
                "kind": target["kind"],
                "default_features": target["default_features"],
                "features": copy.deepcopy(target["features"]),
            }
            index = next(i for i, item in enumerate(dependencies) if item["name"] == "solana-instruction")
            dependencies.insert(index, insertion)
        else:
            mapped[change["dependency"]]["version"] = target["version"]
            mapped[change["dependency"]]["default_features"] = target["default_features"]
            mapped[change["dependency"]]["features"] = copy.deepcopy(target["features"])

    workstream = next(item for item in binding["workstreams"] if item["workstream_id"] == "FE-W4-SOLANA-PROGRAM-TEST")
    workstream["provider_bindings"] = ["solana-program-test-4.2.2-in-process"]
    binding["construction_gate"]["binding_acceptance"] = "not_evaluable"
    binding["construction_gate"]["implementation"] = "not-authorized-by-this-successor-candidate"
    binding["claim_ceiling"] = (
        "Exact successor Rust construction-binding candidate only. It repairs the accepted binding 004 Solana "
        "dependency graph into one coherent wincode 0.5 schema family and preserves all fourteen local FE-W3 and "
        "FE-W4 targets and semantics. It grants no acceptance, implementation, conformance, security, credential, "
        "wallet, RPC, deployment, Devnet, publication, or external-effect authority."
    )
    return binding


def binding_material(binding_raw: bytes) -> tuple[str, list[dict[str, str]]]:
    artifacts = [
        {"path": "policy.json", "sha256": sha256_file(POLICY_PATH)},
        {"path": "generated/implementation-binding.json", "sha256": sha256_bytes(binding_raw)},
    ]
    material = path_null_digest([
        ("policy.json", POLICY_PATH.read_bytes()),
        ("generated/implementation-binding.json", binding_raw),
    ])
    return material, artifacts


def build_author_decision(binding_raw: bytes) -> dict[str, Any]:
    binding = json.loads(binding_raw)
    material_digest, artifacts = binding_material(binding_raw)
    return {
        "schema_version": "cav2-bounded-helper-construction-binding-author-decision/v1",
        "decision_id": "CA2-AUTHOR-DECISION-KEP-SOL2-RUST-CONSTRUCTION-BINDING-005",
        "decision_kind": "candidate-authorship-only",
        "route_id": binding["route_id"],
        "delegation_route_id": binding["delegation_route_id"],
        "disposition": "AUTHOR-CANDIDATE-AND-REQUEST-HUMAN-OWNER-DECISION",
        "candidate": {
            "binding_id": binding["binding_id"],
            "binding_material_digest_algorithm": "sha256-path-null-bytes-null/v1",
            "binding_material_digest": material_digest,
            "artifacts": artifacts,
        },
        "authorship_findings": [
            "accepted-binding-004-exact",
            "selected-ontology-and-semantic-profiles-exact",
            "cached-manifest-graph-contracts-exact",
            "isolated-probe-material-and-lock-exact",
            "five-entry-graph-repair-exact",
            "fourteen-target-and-FE-W3-FE-W4-preservation-exact",
        ],
        "self_acceptance": False,
        "acceptance_status": "not_evaluable",
        "implementation_status": "not-authorized-by-this-candidate",
        "authority_effect": "none",
        "implementation_effect": "none",
        "enforcement_effect": "none",
        "external_effect": "none",
        "claim_ceiling": binding["claim_ceiling"],
    }


def build_preacceptance(binding_raw: bytes, author_decision_raw: bytes) -> dict[str, Any]:
    binding = json.loads(binding_raw)
    material_digest, artifacts = binding_material(binding_raw)
    return {
        "schema_version": "cav2-kep-sol2-rust-construction-binding-graph-repair-preacceptance/v1",
        "receipt_id": "CA2-RECEIPT-KEP-SOL2-RUST-CONSTRUCTION-BINDING-PREACCEPTANCE-005",
        "route_id": binding["route_id"],
        "delegation_route_id": binding["delegation_route_id"],
        "candidate": {
            "binding_id": binding["binding_id"],
            "lifecycle_status": binding["lifecycle_status"],
            "binding_material_digest_algorithm": "sha256-path-null-bytes-null/v1",
            "binding_material_digest": material_digest,
            "artifacts": artifacts,
        },
        "supersession": binding["supersession"],
        "selected_dependency_digests": {
            "accepted_binding_004_material": binding["supersession"]["supersedes_accepted_material_digest"],
            "accepted_implementation_material": binding["selected_dependencies"]["accepted_implementation"]["implementation_material_digest"],
            "accepted_assessment_material": binding["selected_dependencies"]["accepted_local_assessment"]["assessment_material_digest"],
            "admitted_system_ontology_candidate_set": binding["selected_dependencies"]["admitted_system_ontology"]["candidate_set_digest"],
        },
        "closure": {
            "system_nodes": "89/89 selected",
            "system_relations": "204/204 selected",
            "proof_obligations": "13/13 selected",
            "boundaries": "9/9 selected",
            "exact_dependencies": "17/17 PASS",
            "cached_manifests": "7/7 PASS",
            "coherent_graph_packages": "8/8 PASS",
            "forbidden_wincode_0_6": "absent PASS",
            "planned_targets": "14/14 PASS",
            "forbidden_external_capabilities": "9/9 PASS",
            "graph_repair": "5/5 PASS",
            "all_other_construction_semantics": "unchanged-from-binding-004 PASS",
        },
        "checks": [
            {"check_id": "accepted-binding-004-exact", "status": "PASS"},
            {"check_id": "selected-ontology-dependencies-exact", "status": "PASS"},
            {"check_id": "cached-crate-manifests-exact", "status": "PASS"},
            {"check_id": "wincode-feature-required", "status": "PASS"},
            {"check_id": "isolated-coherent-graph-exact", "status": "PASS"},
            {"check_id": "five-entry-graph-repair-exact", "status": "PASS"},
            {"check_id": "other-construction-semantics-preserved", "status": "PASS"},
            {"check_id": "successor-binding-acceptance", "status": "not_evaluable", "causal_blocker": "Human owner has not accepted this exact successor material digest."},
            {"check_id": "implementation-conformance", "status": "not_evaluable", "causal_blocker": "This construction-binding candidate grants no implementation or conformance claim."},
            {"check_id": "production-security-approval", "status": "not_evaluable", "causal_blocker": "Independent cryptographic security review remains absent."},
            {"check_id": "devnet-evidence", "status": "not_evaluable", "causal_blocker": "Credentials, wallets, RPC, deployment, and Devnet effects remain forbidden."},
        ],
        "author": {"path": "../author.py", "sha256": sha256_file(Path(__file__))},
        "tests": {"path": "../tests/test_author.py", "sha256": sha256_file(TEST_PATH)},
        "author_decision": {"path": "author-decision.json", "sha256": sha256_bytes(author_decision_raw)},
        "decision_gate": {
            "status": "ready-for-exact-successor-construction-binding-decision",
            "required_digest": material_digest,
            "admissible_option_ids": ["ACCEPT-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING", "REJECT-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING", "DEFER-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING"],
            "decision_limit": "Acceptance may bind only this exact dependency-graph repair candidate; it cannot accept implementation bytes, conformance, security, or external effects.",
        },
        "preacceptance": {"status": "PASS", "authority_effect": "none"},
        "authority_effect": "none",
        "implementation_effect": "none",
        "enforcement_effect": "none",
        "external_effect": "none",
        "claim_ceiling": binding["claim_ceiling"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        binding_raw = canonical_bytes(build_binding())
        author_decision_raw = canonical_bytes(build_author_decision(binding_raw))
        preacceptance_raw = canonical_bytes(build_preacceptance(binding_raw, author_decision_raw))
        outputs = [
            (BINDING_PATH, binding_raw, "generated binding"),
            (AUTHOR_DECISION_PATH, author_decision_raw, "generated author decision"),
            (PREACCEPTANCE_PATH, preacceptance_raw, "generated preacceptance"),
        ]
        if args.check:
            for path, raw, label in outputs:
                require(path.is_file(), f"missing {label}")
                require(path.read_bytes() == raw, f"{label} drift")
            mode = "check"
        else:
            for path, raw, _ in outputs:
                path.write_bytes(raw)
            mode = "write"
        material_digest, _ = binding_material(binding_raw)
        print(json.dumps({
            "result": "pass",
            "mode": mode,
            "binding_id": json.loads(binding_raw)["binding_id"],
            "binding_sha256": sha256_bytes(binding_raw),
            "binding_material_digest": material_digest,
            "author_decision_sha256": sha256_bytes(author_decision_raw),
            "preacceptance_sha256": sha256_bytes(preacceptance_raw),
            "authority_effect": "none",
            "implementation_effect": "none",
            "external_effect": "none",
        }, indent=2))
        return 0
    except (BindingError, KeyError, TypeError, ValueError, OSError, tomllib.TOMLDecodeError) as exc:
        print(json.dumps({"result": "fail", "error": str(exc), "authority_effect": "none"}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
