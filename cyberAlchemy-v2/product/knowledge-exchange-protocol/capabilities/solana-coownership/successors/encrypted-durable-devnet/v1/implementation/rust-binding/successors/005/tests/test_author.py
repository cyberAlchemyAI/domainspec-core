from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUTHOR_PATH = HERE.parent / "author.py"
SPEC = importlib.util.spec_from_file_location("sol2_rust_construction_binding_005_author", AUTHOR_PATH)
assert SPEC and SPEC.loader
AUTHOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUTHOR)


class RustConstructionBinding005Tests(unittest.TestCase):
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

    def test_exact_five_entry_graph_repair(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        successor = AUTHOR.build_binding(policy)
        old = AUTHOR.dependency_map(prior)
        new = AUTHOR.dependency_map(successor)
        expected = {item["dependency"]: item for item in policy["exact_graph_repair"]}
        self.assertEqual(set(old) | {"solana-address"}, set(new))
        for name, change in expected.items():
            target = change["to"]
            self.assertEqual(target["version"], new[name]["version"])
            self.assertEqual(target["default_features"], new[name]["default_features"])
            self.assertEqual(target["features"], new[name]["features"])
        for name in old.keys() - expected.keys():
            self.assertEqual(old[name], new[name], name)

    def test_wincode_is_preserved_and_schema_pins_are_exact(self) -> None:
        dependencies = AUTHOR.dependency_map(AUTHOR.build_binding())
        self.assertEqual(["wincode"], dependencies["solana-transaction"]["features"])
        self.assertEqual("=4.1.4", dependencies["solana-transaction"]["version"])
        self.assertEqual("=3.4.1", dependencies["solana-instruction"]["version"])
        self.assertEqual("=4.2.0", dependencies["solana-pubkey"]["version"])
        self.assertEqual("=2.6.1", dependencies["solana-address"]["version"])

    def test_non_graph_surfaces_and_fourteen_targets_are_preserved(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        successor = AUTHOR.build_binding(policy)
        preserved = [
            "selected_dependencies", "selector_closure", "carried_assessment_ceiling", "planned_targets",
            "preserved_surfaces", "local_conformance", "forbidden_capabilities", "security_posture",
        ]
        for key in preserved:
            self.assertEqual(prior[key], successor[key], key)
        self.assertEqual(14, len(successor["planned_targets"]))
        self.assertEqual("1.94.0", successor["rust_substrate"]["minimum_rust_version"])

    def test_only_provider_version_label_changes_in_workstreams(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        successor = AUTHOR.build_binding(policy)
        prior_workstreams = copy.deepcopy(prior["workstreams"])
        successor_workstreams = copy.deepcopy(successor["workstreams"])
        old_w4 = next(item for item in prior_workstreams if item["workstream_id"] == "FE-W4-SOLANA-PROGRAM-TEST")
        new_w4 = next(item for item in successor_workstreams if item["workstream_id"] == "FE-W4-SOLANA-PROGRAM-TEST")
        self.assertEqual(["solana-program-test-4.1.2-in-process"], old_w4["provider_bindings"])
        self.assertEqual(["solana-program-test-4.2.2-in-process"], new_w4["provider_bindings"])
        old_w4["provider_bindings"] = new_w4["provider_bindings"]
        self.assertEqual(prior_workstreams, successor_workstreams)

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
        mutated["superseded_binding"]["binding_material_digest"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_predecessor_acceptance_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["superseded_binding"]["acceptance_decision_sha256"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_selected_ontology_digest_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["selected_ontology_dependency"]["accepted_candidate_set_digest"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_cached_manifest_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["cached_manifest_evidence"][0]["sha256"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_probe_lock_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["isolated_probe"]["lock_sha256"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_removing_transaction_wincode_fails_closed(self) -> None:
        mutated = self.policy()
        change = next(item for item in mutated["exact_graph_repair"] if item["dependency"] == "solana-transaction")
        change["to"]["features"] = []
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_program_test_version_drift_fails_closed(self) -> None:
        mutated = self.policy()
        change = next(item for item in mutated["exact_graph_repair"] if item["dependency"] == "solana-program-test")
        change["to"]["version"] = "=4.2.1"
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_extra_graph_feature_fails_closed(self) -> None:
        mutated = self.policy()
        change = next(item for item in mutated["exact_graph_repair"] if item["dependency"] == "solana-instruction")
        change["to"]["features"].append("wincode")
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_preacceptance_collects_dependent_not_evaluable_checks(self) -> None:
        binding_raw = AUTHOR.canonical_bytes(AUTHOR.build_binding())
        decision_raw = AUTHOR.canonical_bytes(AUTHOR.build_author_decision(binding_raw))
        receipt = AUTHOR.build_preacceptance(binding_raw, decision_raw)
        checks = {item["check_id"]: item for item in receipt["checks"]}
        self.assertEqual("not_evaluable", checks["successor-binding-acceptance"]["status"])
        self.assertEqual("not_evaluable", checks["implementation-conformance"]["status"])
        self.assertEqual("not_evaluable", checks["production-security-approval"]["status"])
        self.assertEqual("not_evaluable", checks["devnet-evidence"]["status"])


if __name__ == "__main__":
    unittest.main()
