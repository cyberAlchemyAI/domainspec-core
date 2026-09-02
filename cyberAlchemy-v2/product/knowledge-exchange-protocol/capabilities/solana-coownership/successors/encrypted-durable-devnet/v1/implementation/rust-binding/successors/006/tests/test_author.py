from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUTHOR_PATH = HERE.parent / "author.py"
SPEC = importlib.util.spec_from_file_location("sol2_rust_construction_binding_006_author", AUTHOR_PATH)
assert SPEC and SPEC.loader
AUTHOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUTHOR)


class RustConstructionBinding006Tests(unittest.TestCase):
    def policy(self):
        return json.loads(AUTHOR.POLICY_PATH.read_text(encoding="utf-8"))

    def test_two_complete_builds_are_byte_identical(self) -> None:
        first_binding = AUTHOR.canonical_bytes(AUTHOR.build_binding())
        first_decision = AUTHOR.canonical_bytes(AUTHOR.build_author_decision(first_binding))
        first_receipt = AUTHOR.canonical_bytes(AUTHOR.build_preacceptance(first_binding, first_decision))
        second_binding = AUTHOR.canonical_bytes(AUTHOR.build_binding())
        second_decision = AUTHOR.canonical_bytes(AUTHOR.build_author_decision(second_binding))
        second_receipt = AUTHOR.canonical_bytes(AUTHOR.build_preacceptance(second_binding, second_decision))
        self.assertEqual((first_binding, first_decision, first_receipt), (second_binding, second_decision, second_receipt))

    def test_only_signer_pin_changes_in_dependency_closure(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        successor = AUTHOR.build_binding(policy)
        old = AUTHOR.dependency_map(prior)
        new = AUTHOR.dependency_map(successor)
        self.assertEqual(list(old), list(new))
        self.assertEqual(17, len(new))
        self.assertEqual("=3.0.0", old["solana-signer"]["version"])
        self.assertEqual("=3.0.1", new["solana-signer"]["version"])
        self.assertFalse(new["solana-signer"]["default_features"])
        self.assertEqual([], new["solana-signer"]["features"])
        for name in old.keys() - {"solana-signer"}:
            self.assertEqual(old[name], new[name], name)

    def test_full_manifest_projects_all_seventeen_candidate_dependencies(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        expected = AUTHOR.projected_successor(prior)
        raw = (AUTHOR.HERE / policy["full_manifest_probe"]["manifest_path"]).read_bytes()
        actual = AUTHOR.manifest_projection(AUTHOR.tomllib.loads(raw.decode("utf-8")))
        self.assertEqual(set(AUTHOR.EXPECTED_DEPENDENCY_NAMES), set(actual))
        self.assertEqual(17, len(actual))
        self.assertEqual(expected, actual)

    def test_signer_and_keypair_are_mandatory_in_solana_probe(self) -> None:
        policy = self.policy()
        required = policy["isolated_solana_probe"]["required_direct_dependencies"]
        self.assertIn("solana-signer", required)
        self.assertIn("solana-keypair", required)
        self.assertEqual(7, len(required))

    def test_targets_workstreams_selectors_profiles_and_rust_are_preserved(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        successor = AUTHOR.build_binding(policy)
        preserved = [
            "selected_dependencies", "selector_closure", "carried_assessment_ceiling", "workstreams",
            "planned_targets", "preserved_surfaces", "local_conformance", "forbidden_capabilities", "security_posture",
        ]
        for key in preserved:
            self.assertEqual(prior[key], successor[key], key)
        self.assertEqual(14, len(successor["planned_targets"]))
        self.assertEqual("1.94.0", successor["rust_substrate"]["minimum_rust_version"])

    def test_successor_metadata_is_bounded_and_predecessor_is_accepted_005(self) -> None:
        binding = AUTHOR.build_binding()
        self.assertEqual("CA2-D65-KEP-SOL2-RUST-CONSTRUCTION-005", binding["supersession"]["supersedes_binding_id"])
        self.assertEqual("af5de6c6a168c0e83e0a4246306b28aee23c262bebb24f5648c2a931a9d8aba3", binding["supersession"]["supersedes_accepted_material_digest"])
        self.assertEqual(1, len(binding["supersession"]["change_set"]))

    def test_candidate_and_author_decision_have_no_authority(self) -> None:
        binding_raw = AUTHOR.canonical_bytes(AUTHOR.build_binding())
        binding = json.loads(binding_raw)
        decision = AUTHOR.build_author_decision(binding_raw)
        for artifact in (binding, decision):
            self.assertEqual("none", artifact["authority_effect"])
            self.assertEqual("none", artifact["implementation_effect"])
            self.assertEqual("none", artifact["external_effect"])
        self.assertFalse(decision["self_acceptance"])
        self.assertEqual("not_evaluable", decision["acceptance_status"])

    def test_predecessor_digest_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["accepted_predecessor"]["binding_material_digest"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_predecessor_acceptance_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["accepted_predecessor"]["acceptance_decision_sha256"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_selected_ontology_digest_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["selected_ontology_dependency"]["accepted_candidate_set_digest"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_cached_signer_manifest_drift_fails_closed(self) -> None:
        mutated = self.policy()
        signer = next(item for item in mutated["cached_manifest_evidence"] if item["crate"] == "solana-signer")
        signer["sha256"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_signer_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["exact_graph_repair"]["to"]["version"] = "=3.0.2"
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_missing_full_projection_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["full_manifest_probe"]["direct_dependency_count"] = 16
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_full_projection_lock_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["full_manifest_probe"]["lock_sha256"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_missing_signer_from_probe_closure_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["isolated_solana_probe"]["required_direct_dependencies"].remove("solana-signer")
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_missing_keypair_from_probe_closure_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["isolated_solana_probe"]["required_direct_dependencies"].remove("solana-keypair")
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_non_signer_dependency_mutation_is_detected(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        successor = AUTHOR.build_binding(policy)
        mutated = copy.deepcopy(successor)
        AUTHOR.dependency_map(mutated)["hpke"]["version"] = "=0.14.1"
        self.assertNotEqual(AUTHOR.binding_projection(successor), AUTHOR.binding_projection(mutated))

    def test_preacceptance_collects_dependent_not_evaluable_checks(self) -> None:
        binding_raw = AUTHOR.canonical_bytes(AUTHOR.build_binding())
        decision_raw = AUTHOR.canonical_bytes(AUTHOR.build_author_decision(binding_raw))
        receipt = AUTHOR.build_preacceptance(binding_raw, decision_raw)
        checks = {item["check_id"]: item for item in receipt["checks"]}
        self.assertEqual("not_evaluable", checks["successor-binding-acceptance"]["status"])
        self.assertEqual("not_evaluable", checks["implementation-conformance"]["status"])
        self.assertEqual("not_evaluable", checks["production-security-approval"]["status"])
        self.assertEqual("not_evaluable", checks["devnet-evidence"]["status"])
        self.assertEqual("PASS", checks["full-manifest-offline-resolution"]["status"])


if __name__ == "__main__":
    unittest.main()
