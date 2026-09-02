#!/usr/bin/env python3
"""Author exact successor binding 006 for the bounded signer-pin repair."""

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

EXPECTED_DEPENDENCY_NAMES = [
    "chacha20poly1305", "getrandom", "hpke", "sha2", "sqlx", "tokio", "zeroize",
    "solana-account-info", "solana-address", "solana-instruction", "solana-program-entrypoint",
    "solana-program-error", "solana-pubkey", "solana-program-test", "solana-keypair",
    "solana-signer", "solana-transaction",
]
EXPECTED_SOLANA_PROBE_NAMES = [
    "solana-address", "solana-instruction", "solana-keypair", "solana-program-test",
    "solana-pubkey", "solana-signer", "solana-transaction",
]
EXPECTED_REPAIR = {
    "dependency": "solana-signer",
    "from": {"version": "=3.0.0", "kind": "test", "default_features": False, "features": []},
    "to": {"version": "=3.0.1", "kind": "test", "default_features": False, "features": []},
}


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


def manifest_projection(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    projection: dict[str, dict[str, Any]] = {}
    for table in ("dependencies", "dev-dependencies"):
        for name, declaration in manifest.get(table, {}).items():
            require(isinstance(declaration, dict), f"{table}.{name} must use an exact table declaration")
            require(name not in projection, f"duplicate manifest dependency: {name}")
            projection[name] = {
                "version": declaration.get("version"),
                "default_features": declaration.get("default-features", True),
                "features": declaration.get("features", []),
            }
    return projection


def binding_projection(binding: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "version": item["version"],
            "default_features": item["default_features"],
            "features": item["features"],
        }
        for name, item in dependency_map(binding).items()
    }


def projected_successor(prior: dict[str, Any]) -> dict[str, dict[str, Any]]:
    projection = copy.deepcopy(binding_projection(prior))
    projection["solana-signer"] = {
        "version": "=3.0.1",
        "default_features": False,
        "features": [],
    }
    return projection


def verify_cached_manifest_contracts(manifests: dict[str, dict[str, Any]]) -> None:
    program_test = manifests["solana-program-test"]
    require(program_test["dependencies"]["solana-signer"]["version"] == "3.0.1", "program-test signer lower bound drift")
    require(program_test["dependencies"]["solana-keypair"]["version"] == "3.1.2", "program-test keypair version drift")
    require(program_test["dependencies"]["solana-transaction"]["version"] == ">=4.1.4,<4.2.0", "program-test transaction range drift")

    transaction = manifests["solana-transaction"]
    require(transaction["dependencies"]["solana-signer"]["version"] == "3.0.1", "transaction signer lower bound drift")
    require(transaction["dependencies"]["solana-signer"]["optional"] is True, "transaction signer optionality drift")
    require(transaction["dependencies"]["solana-signer"]["default-features"] is False, "transaction signer default-feature drift")
    require("dep:solana-signer" in transaction["features"]["wincode"], "transaction wincode no longer selects signer")

    keypair = manifests["solana-keypair"]
    require(keypair["dependencies"]["solana-signer"]["version"] == "3.0.0", "keypair signer compatible range drift")
    signer = manifests["solana-signer"]
    require(signer["package"]["version"] == "3.0.1", "signer package version drift")


def verify_inputs(policy: dict[str, Any]) -> dict[str, Any]:
    require(policy["exact_graph_repair"] == EXPECTED_REPAIR, "exact signer repair drift")
    require(policy["current_runtime_projection"]["dependency_count"] == 17, "runtime full projection count drift")
    require(policy["preservation"]["dependency_count"] == 17, "preserved dependency count drift")
    require(policy["preservation"]["planned_target_count"] == 14, "planned target count drift")

    prior = policy["accepted_predecessor"]
    prior_policy_path, _ = exact_json(prior["policy_path"], prior["policy_sha256"], "binding 005 policy")
    _, prior_binding = exact_json(prior["binding_path"], prior["binding_sha256"], "binding 005 candidate")
    _, acceptance = exact_json(prior["acceptance_decision_path"], prior["acceptance_decision_sha256"], "binding 005 acceptance")
    prior_material = path_null_digest([
        ("policy.json", prior_policy_path.read_bytes()),
        ("generated/implementation-binding.json", canonical_bytes(prior_binding)),
    ])
    require(prior_material == prior["binding_material_digest"], "binding 005 material digest does not reproduce")
    require(prior_binding["binding_id"] == prior["binding_id"], "binding 005 identity mismatch")
    require(acceptance["decision_id"] == prior["acceptance_decision_id"], "binding 005 acceptance identity mismatch")
    require(acceptance["acceptance"]["lifecycle_status"] == "accepted", "binding 005 is not accepted")
    require(acceptance["acceptance"]["accepted_binding_material_digest"] == prior_material, "binding 005 accepted digest mismatch")

    ontology = policy["selected_ontology_dependency"]
    selected = prior_binding["selected_dependencies"]["admitted_system_ontology"]
    require(selected["ontology_id"] == ontology["ontology_id"], "selected ontology identity drift")
    require(selected["candidate_set_digest"] == ontology["accepted_candidate_set_digest"], "selected ontology digest drift")
    require(selected["selectors"] == ontology["selectors"], "selected ontology selectors drift")
    require(prior_binding["selected_dependencies"]["semantic_profiles"] == ontology["semantic_profiles"], "semantic profile drift")

    prior_dependencies = dependency_map(prior_binding)
    require(list(prior_dependencies) == EXPECTED_DEPENDENCY_NAMES, "binding 005 full dependency order or closure drift")
    require(len(prior_dependencies) == 17, "binding 005 dependency count drift")
    require(prior_dependencies["solana-signer"] == {"name": "solana-signer", **EXPECTED_REPAIR["from"]}, "binding 005 signer selection drift")

    runtime = policy["current_runtime_projection"]
    runtime_raw = exact_file(KEP_ROOT / runtime["path"], runtime["sha256"], "actual runtime Cargo projection")
    runtime_projection = manifest_projection(tomllib.loads(runtime_raw.decode("utf-8")))
    require(len(runtime_projection) == 17 and set(runtime_projection) == set(EXPECTED_DEPENDENCY_NAMES), "actual runtime full dependency closure drift")
    require(runtime_projection == binding_projection(prior_binding), "actual runtime does not project all 17 accepted binding 005 dependencies")

    manifests: dict[str, dict[str, Any]] = {}
    for evidence in policy["cached_manifest_evidence"]:
        manifest_path = locate_cached_manifest(evidence["crate"], evidence["version"])
        raw = exact_file(manifest_path, evidence["sha256"], f"cached {evidence['crate']} manifest")
        parsed = tomllib.loads(raw.decode("utf-8"))
        require(parsed["package"]["name"] == evidence["crate"], f"cached {evidence['crate']} identity drift")
        require(parsed["package"]["version"] == evidence["version"], f"cached {evidence['crate']} version drift")
        manifests[evidence["crate"]] = parsed
    require(set(manifests) == {"solana-program-test", "solana-signer", "solana-keypair", "solana-transaction"}, "cached manifest closure drift")
    verify_cached_manifest_contracts(manifests)

    expected_successor = projected_successor(prior_binding)
    solana_probe = policy["isolated_solana_probe"]
    require(solana_probe["required_direct_dependencies"] == EXPECTED_SOLANA_PROBE_NAMES, "isolated probe direct closure drift")
    solana_manifest_raw = exact_file(Path(solana_probe["manifest_path"]), solana_probe["manifest_sha256"], "isolated Solana probe manifest")
    solana_lock_raw = exact_file(Path(solana_probe["lock_path"]), solana_probe["lock_sha256"], "isolated Solana probe lock")
    solana_projection = manifest_projection(tomllib.loads(solana_manifest_raw.decode("utf-8")))
    require(list(solana_projection) == EXPECTED_SOLANA_PROBE_NAMES, "isolated probe omits signer, keypair, or another required direct dependency")
    for name in EXPECTED_SOLANA_PROBE_NAMES:
        require(solana_projection[name]["version"] == expected_successor[name]["version"], f"isolated probe {name} version drift")
        require(solana_projection[name]["default_features"] == expected_successor[name]["default_features"], f"isolated probe {name} default-feature drift")
        if name != "solana-instruction":
            require(solana_projection[name]["features"] == expected_successor[name]["features"], f"isolated probe {name} feature drift")
    solana_locked = {(item["name"], item["version"]) for item in tomllib.loads(solana_lock_raw.decode("utf-8"))["package"]}
    for name in EXPECTED_SOLANA_PROBE_NAMES:
        require((name, expected_successor[name]["version"].lstrip("=")) in solana_locked, f"isolated probe lock missing {name}")

    full_probe = policy["full_manifest_probe"]
    require(full_probe["direct_dependency_count"] == 17, "full-manifest probe projection count drift")
    require(full_probe["locked_package_count"] == 774, "full-manifest probe package closure drift")
    require(full_probe["resolved_dependency_package_count"] == 773, "full-manifest resolved dependency count drift")
    require(full_probe["observed_result"] == "PASS", "full-manifest probe observed result drift")
    full_manifest_raw = exact_file(HERE / full_probe["manifest_path"], full_probe["manifest_sha256"], "full-manifest probe manifest")
    full_lock_raw = exact_file(HERE / full_probe["lock_path"], full_probe["lock_sha256"], "full-manifest probe lock")
    exact_file(HERE / full_probe["source_path"], full_probe["source_sha256"], "full-manifest probe source")
    full_projection = manifest_projection(tomllib.loads(full_manifest_raw.decode("utf-8")))
    require(len(full_projection) == 17 and set(full_projection) == set(EXPECTED_DEPENDENCY_NAMES), "full-manifest probe missing accepted dependency projection")
    require(full_projection == expected_successor, "full-manifest probe is not the exact repaired 17-entry projection")
    lock_packages = tomllib.loads(full_lock_raw.decode("utf-8"))["package"]
    require(len(lock_packages) == 774, "full-manifest probe locked package count mismatch")
    locked = {(item["name"], item["version"]) for item in lock_packages}
    for name, selected_dependency in expected_successor.items():
        require((name, selected_dependency["version"].lstrip("=")) in locked, f"full-manifest lock missing direct selection {name}")
    roots = [item for item in lock_packages if item["name"] == "ca2_kep_sol2_binding_006_full_manifest_probe"]
    require(len(roots) == 1, "full-manifest probe root package closure drift")
    root_names = [item.split(" ", 1)[0] for item in roots[0]["dependencies"]]
    require(len(root_names) == 17 and set(root_names) == set(EXPECTED_DEPENDENCY_NAMES), "full-manifest lock root does not project all 17 dependencies")

    require(prior_binding["rust_substrate"]["minimum_rust_version"] == policy["preservation"]["minimum_rust_version"], "Rust version drift")
    require(len(prior_binding["planned_targets"]) == 14, "planned target closure drift")
    require(prior_binding["authority_effect"] == prior_binding["implementation_effect"] == prior_binding["external_effect"] == "none", "binding 005 effect ceiling drift")
    return {"prior_binding": prior_binding}


def build_binding(policy_override: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = copy.deepcopy(policy_override) if policy_override is not None else load_json(POLICY_PATH)
    prior = verify_inputs(policy)["prior_binding"]
    binding = copy.deepcopy(prior)
    binding["binding_id"] = policy["binding_id"]
    binding["policy_id"] = policy["policy_id"]
    binding["source_authorization"] = policy["source_authorization"]
    binding["supersession"] = {
        "supersedes_binding_id": policy["accepted_predecessor"]["binding_id"],
        "supersedes_accepted_material_digest": policy["accepted_predecessor"]["binding_material_digest"],
        "cause": policy["causal_defect"],
        "change_set": [policy["exact_graph_repair"]],
        "all_other_construction_semantics": "byte-equivalent-after-successor-metadata-and-signer-pin-normalization",
    }
    dependency_map(binding)["solana-signer"]["version"] = "=3.0.1"
    binding["construction_gate"]["binding_acceptance"] = "not_evaluable"
    binding["construction_gate"]["implementation"] = "not-authorized-by-this-successor-candidate"
    binding["construction_gate"]["candidate_bytes"] = "authored"
    binding["construction_gate"]["local_tests"] = "candidate-author-and-resolution-probe-PASS"
    binding["claim_ceiling"] = (
        "Exact successor Rust construction-binding candidate only. It repairs accepted binding 005 solely by "
        "changing direct solana-signer =3.0.0 to =3.0.1 and preserves the other sixteen dependencies, Rust 1.94.0, "
        "all fourteen local FE-W3 and FE-W4 targets, workstreams, selectors, profiles, and semantics. Full-manifest "
        "offline resolution evidence does not grant acceptance, implementation, conformance, security, credential, "
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
        "decision_id": "CA2-AUTHOR-DECISION-KEP-SOL2-RUST-CONSTRUCTION-BINDING-006",
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
            "accepted-binding-005-exact",
            "selected-ontology-and-profiles-exact",
            "solana-signer-causal-conflict-exact",
            "direct-signer-and-keypair-probe-closure-exact",
            "full-seventeen-dependency-projection-and-lock-exact",
            "fourteen-target-workstream-and-FE-W3-FE-W4-preservation-exact",
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
        "schema_version": "cav2-kep-sol2-rust-construction-binding-full-projection-repair-preacceptance/v1",
        "receipt_id": "CA2-RECEIPT-KEP-SOL2-RUST-CONSTRUCTION-BINDING-PREACCEPTANCE-006",
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
            "accepted_binding_005_material": binding["supersession"]["supersedes_accepted_material_digest"],
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
            "unchanged_dependencies": "16/16 PASS",
            "signer_repair": "1/1 PASS",
            "cached_manifests": "4/4 PASS",
            "isolated_solana_direct_projection": "7/7 PASS including signer and keypair",
            "full_manifest_direct_projection": "17/17 PASS",
            "full_manifest_locked_packages": "774/774 PASS including root; 773 resolved dependencies",
            "full_manifest_offline_check": "PASS",
            "planned_targets": "14/14 PASS",
            "all_other_construction_semantics": "unchanged-from-accepted-binding-005 PASS",
        },
        "checks": [
            {"check_id": "accepted-binding-005-exact", "status": "PASS"},
            {"check_id": "selected-ontology-and-profiles-exact", "status": "PASS"},
            {"check_id": "signer-lower-bound-cause-exact", "status": "PASS"},
            {"check_id": "direct-signer-and-keypair-probe-closure", "status": "PASS"},
            {"check_id": "full-seventeen-dependency-projection", "status": "PASS"},
            {"check_id": "full-manifest-offline-resolution", "status": "PASS"},
            {"check_id": "only-signer-pin-changed", "status": "PASS"},
            {"check_id": "other-construction-semantics-preserved", "status": "PASS"},
            {"check_id": "successor-binding-acceptance", "status": "not_evaluable", "causal_blocker": "Human owner has not accepted this exact successor material digest."},
            {"check_id": "implementation-conformance", "status": "not_evaluable", "causal_blocker": "This construction-binding candidate grants no implementation or conformance claim."},
            {"check_id": "production-security-approval", "status": "not_evaluable", "causal_blocker": "Independent cryptographic security review remains absent."},
            {"check_id": "devnet-evidence", "status": "not_evaluable", "causal_blocker": "Credentials, wallets, RPC, deployment, and Devnet effects remain forbidden."},
        ],
        "resolution_evidence": {
            "manifest": {"path": "../full-manifest-probe/Cargo.toml", "sha256": sha256_file(HERE / "full-manifest-probe" / "Cargo.toml")},
            "lock": {"path": "../full-manifest-probe/Cargo.lock", "sha256": sha256_file(HERE / "full-manifest-probe" / "Cargo.lock")},
            "source": {"path": "../full-manifest-probe/src/lib.rs", "sha256": sha256_file(HERE / "full-manifest-probe" / "src" / "lib.rs")},
            "command": "cargo check --all-targets --locked --offline --manifest-path full-manifest-probe/Cargo.toml",
            "result": "PASS",
        },
        "author": {"path": "../author.py", "sha256": sha256_file(Path(__file__))},
        "tests": {"path": "../tests/test_author.py", "sha256": sha256_file(TEST_PATH)},
        "author_decision": {"path": "author-decision.json", "sha256": sha256_bytes(author_decision_raw)},
        "decision_gate": {
            "status": "ready-for-exact-successor-construction-binding-decision",
            "required_digest": material_digest,
            "admissible_option_ids": ["ACCEPT-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING", "REJECT-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING", "DEFER-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING"],
            "decision_limit": "Acceptance may bind only this exact signer-pin repair candidate; it cannot accept implementation bytes, conformance, security, or external effects.",
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
                path.parent.mkdir(parents=True, exist_ok=True)
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
            "full_manifest_direct_dependencies": 17,
            "full_manifest_locked_packages": 774,
            "full_manifest_resolved_dependencies": 773,
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
