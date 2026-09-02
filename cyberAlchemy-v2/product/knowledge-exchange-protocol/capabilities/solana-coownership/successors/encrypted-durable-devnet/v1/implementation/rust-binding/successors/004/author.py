#!/usr/bin/env python3
"""Author exact successor binding 004 for one dependency-feature repair."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
V1_ROOT = HERE.parents[3]
POLICY_PATH = HERE / "policy.json"
BINDING_PATH = HERE / "generated" / "implementation-binding.json"
PREACCEPTANCE_PATH = HERE / "generated" / "preacceptance-001.json"
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


def locate_cached(crate_relative: str) -> Path:
    cargo_home = Path(os.environ.get("CARGO_HOME", str(Path.home() / ".cargo")))
    matches = sorted((cargo_home / "registry" / "src").glob(f"*/solana-program-test-4.1.2/{crate_relative}"))
    require(len(matches) == 1, f"expected exactly one cached solana-program-test 4.1.2 {crate_relative}, found {len(matches)}")
    return matches[0]


def verify_inputs(policy: dict[str, Any]) -> dict[str, Any]:
    prior = policy["superseded_binding"]
    prior_policy_path, prior_policy = exact_json(prior["policy_path"], prior["policy_sha256"], "binding 003 policy")
    _, prior_binding = exact_json(prior["binding_path"], prior["binding_sha256"], "binding 003 candidate")
    _, acceptance = exact_json(prior["acceptance_decision_path"], prior["acceptance_decision_sha256"], "binding 003 acceptance")

    prior_material = path_null_digest([
        ("policy.json", prior_policy_path.read_bytes()),
        ("generated/implementation-binding.json", canonical_bytes(prior_binding)),
    ])
    require(prior_material == prior["binding_material_digest"], "binding 003 material digest does not reproduce")
    require(prior_binding["binding_id"] == prior["binding_id"], "binding 003 identity mismatch")
    require(acceptance["decision_id"] == prior["acceptance_decision_id"], "binding 003 acceptance identity mismatch")
    require(acceptance["acceptance"]["lifecycle_status"] == "accepted", "binding 003 is not accepted")
    require(acceptance["acceptance"]["accepted_binding_material_digest"] == prior_material, "binding 003 accepted digest mismatch")

    feature = policy["exact_feature_repair"]
    dependencies = prior_binding["rust_substrate"]["dependencies"]
    target = [item for item in dependencies if item["name"] == feature["dependency"]]
    require(len(target) == 1, "binding 003 solana-program-test dependency is not unique")
    require(target[0]["version"] == "=4.1.2", "binding 003 solana-program-test version drift")
    require(target[0]["features"] == feature["from"] == [], "binding 003 omitted-feature premise drift")
    require(feature["to"] == ["agave-unstable-api"], "successor feature repair drift")

    evidence = policy["cached_source_evidence"]
    manifest = locate_cached("Cargo.toml")
    crate_root = locate_cached("src/lib.rs")
    require(sha256_file(manifest) == evidence["cargo_manifest_sha256"], "cached crate manifest drift")
    require(sha256_file(crate_root) == evidence["crate_root_sha256"], "cached crate root drift")
    require(evidence["required_manifest_declaration"] in manifest.read_text(encoding="utf-8"), "required crate feature declaration absent")
    require(crate_root.read_text(encoding="utf-8").splitlines()[0] == evidence["required_crate_gate"], "required crate-root feature gate absent")

    require(prior_binding["selector_closure"] == {"system_nodes": 89, "system_relations": 204, "proof_obligations": 13, "boundaries": 9}, "ontology selector closure drift")
    require(len(dependencies) == 16, "dependency closure drift")
    require(len(prior_binding["planned_targets"]) == 14, "planned target closure drift")
    require(len(prior_binding["forbidden_capabilities"]) == 9, "forbidden capability closure drift")
    require(prior_binding["authority_effect"] == prior_binding["implementation_effect"] == prior_binding["external_effect"] == "none", "binding 003 candidate effect ceiling drift")
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
        "change_set": policy["exact_feature_repair"],
        "all_other_construction_semantics": "byte-equivalent-after-successor-metadata-and-feature-normalization"
    }
    dependency = next(item for item in binding["rust_substrate"]["dependencies"] if item["name"] == "solana-program-test")
    dependency["features"] = copy.deepcopy(policy["exact_feature_repair"]["to"])
    binding["construction_gate"]["binding_acceptance"] = "not_evaluable"
    binding["construction_gate"]["implementation"] = "not-authorized-by-this-successor-candidate"
    binding["claim_ceiling"] = (
        "Exact successor Rust construction-binding candidate only. It repairs the solana-program-test 4.1.2 "
        "agave-unstable-api feature omission and preserves all other accepted binding 003 construction semantics. "
        "It grants no acceptance, implementation, conformance, security, credential, wallet, RPC, deployment, "
        "Devnet, publication, or external-effect authority."
    )
    return binding


def binding_material(binding_raw: bytes) -> tuple[str, list[dict[str, str]]]:
    artifacts = [
        {"path": "policy.json", "sha256": sha256_file(POLICY_PATH)},
        {"path": "generated/implementation-binding.json", "sha256": sha256_bytes(binding_raw)},
    ]
    return path_null_digest([
        ("policy.json", POLICY_PATH.read_bytes()),
        ("generated/implementation-binding.json", binding_raw),
    ]), artifacts


def build_preacceptance(binding_raw: bytes) -> dict[str, Any]:
    binding = json.loads(binding_raw)
    material_digest, artifacts = binding_material(binding_raw)
    return {
        "schema_version": "cav2-kep-sol2-rust-construction-binding-repair-preacceptance/v1",
        "receipt_id": "CA2-RECEIPT-KEP-SOL2-RUST-CONSTRUCTION-BINDING-PREACCEPTANCE-004",
        "route_id": binding["route_id"],
        "delegation_route_id": binding["delegation_route_id"],
        "candidate": {
            "binding_id": binding["binding_id"],
            "lifecycle_status": binding["lifecycle_status"],
            "binding_material_digest_algorithm": "sha256-path-null-bytes-null/v1",
            "binding_material_digest": material_digest,
            "artifacts": artifacts
        },
        "supersession": binding["supersession"],
        "selected_dependency_digests": {
            "accepted_binding_003_material": binding["supersession"]["supersedes_accepted_material_digest"],
            "accepted_implementation_material": binding["selected_dependencies"]["accepted_implementation"]["implementation_material_digest"],
            "accepted_assessment_material": binding["selected_dependencies"]["accepted_local_assessment"]["assessment_material_digest"],
            "admitted_system_ontology_candidate_set": binding["selected_dependencies"]["admitted_system_ontology"]["candidate_set_digest"]
        },
        "closure": {
            "system_nodes": "89/89 selected",
            "system_relations": "204/204 selected",
            "proof_obligations": "13/13 selected",
            "boundaries": "9/9 selected",
            "exact_dependencies": "16/16 PASS",
            "planned_targets": "14/14 PASS",
            "forbidden_external_capabilities": "9/9 PASS",
            "feature_repair": "1/1 PASS",
            "all_other_construction_semantics": "unchanged-from-binding-003 PASS"
        },
        "checks": [
            {"check_id": "accepted-binding-003-exact", "status": "PASS"},
            {"check_id": "cached-crate-source-exact", "status": "PASS"},
            {"check_id": "crate-api-feature-gate-proved", "status": "PASS"},
            {"check_id": "single-feature-repair-exact", "status": "PASS"},
            {"check_id": "other-construction-semantics-preserved", "status": "PASS"},
            {"check_id": "successor-binding-acceptance", "status": "not_evaluable", "causal_blocker": "Human owner has not accepted this exact successor material digest."},
            {"check_id": "implementation-conformance", "status": "not_evaluable", "causal_blocker": "The repaired construction binding is not accepted and cannot authorize successor implementation evidence."},
            {"check_id": "production-security-approval", "status": "not_evaluable", "causal_blocker": "Independent cryptographic security review remains absent."},
            {"check_id": "devnet-evidence", "status": "not_evaluable", "causal_blocker": "Credentials, wallets, RPC, deployment, and Devnet effects remain forbidden."}
        ],
        "author": {"path": "../author.py", "sha256": sha256_file(Path(__file__))},
        "tests": {"path": "../tests/test_author.py", "sha256": sha256_file(TEST_PATH)},
        "decision_gate": {
            "status": "ready-for-exact-successor-construction-binding-decision",
            "required_digest": material_digest,
            "admissible_option_ids": ["ACCEPT-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING", "REJECT-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING", "DEFER-EXACT-SUCCESSOR-RUST-CONSTRUCTION-BINDING"],
            "decision_limit": "Acceptance may bind only this exact one-feature repair candidate; it cannot accept implementation bytes, conformance, security, or external effects."
        },
        "preacceptance": {"status": "PASS", "authority_effect": "none"},
        "authority_effect": "none",
        "implementation_effect": "none",
        "enforcement_effect": "none",
        "external_effect": "none",
        "claim_ceiling": binding["claim_ceiling"]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        binding_raw = canonical_bytes(build_binding())
        preacceptance_raw = canonical_bytes(build_preacceptance(binding_raw))
        if args.check:
            require(BINDING_PATH.is_file(), "missing generated binding")
            require(PREACCEPTANCE_PATH.is_file(), "missing generated preacceptance")
            require(BINDING_PATH.read_bytes() == binding_raw, "generated binding drift")
            require(PREACCEPTANCE_PATH.read_bytes() == preacceptance_raw, "generated preacceptance drift")
            mode = "check"
        else:
            BINDING_PATH.write_bytes(binding_raw)
            PREACCEPTANCE_PATH.write_bytes(preacceptance_raw)
            mode = "write"
        material_digest, _ = binding_material(binding_raw)
        print(json.dumps({
            "result": "pass", "mode": mode, "binding_id": json.loads(binding_raw)["binding_id"],
            "binding_sha256": sha256_bytes(binding_raw), "binding_material_digest": material_digest,
            "preacceptance_sha256": sha256_bytes(preacceptance_raw), "authority_effect": "none",
            "implementation_effect": "none", "external_effect": "none"
        }, indent=2))
        return 0
    except (BindingError, KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({"result": "fail", "error": str(exc), "authority_effect": "none"}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
