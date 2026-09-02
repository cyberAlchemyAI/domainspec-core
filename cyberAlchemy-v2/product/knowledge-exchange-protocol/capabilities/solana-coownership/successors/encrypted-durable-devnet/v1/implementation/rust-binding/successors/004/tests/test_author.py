from __future__ import annotations

import copy
import importlib.util
import json
import unittest


from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR_PATH = HERE.parent / "author.py"
SPEC = importlib.util.spec_from_file_location("sol2_rust_construction_binding_004_author", AUTHOR_PATH)
assert SPEC and SPEC.loader
AUTHOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUTHOR)


class RustConstructionBinding004Tests(unittest.TestCase):
    def policy(self):
        return json.loads(AUTHOR.POLICY_PATH.read_text(encoding="utf-8"))

    def test_two_builds_are_byte_identical(self) -> None:
        self.assertEqual(AUTHOR.canonical_bytes(AUTHOR.build_binding()), AUTHOR.canonical_bytes(AUTHOR.build_binding()))

    def test_exact_single_feature_repair(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        successor = AUTHOR.build_binding(policy)
        prior_dependencies = {item["name"]: item for item in prior["rust_substrate"]["dependencies"]}
        successor_dependencies = {item["name"]: item for item in successor["rust_substrate"]["dependencies"]}
        self.assertEqual([], prior_dependencies["solana-program-test"]["features"])
        self.assertEqual(["agave-unstable-api"], successor_dependencies["solana-program-test"]["features"])
        for name in prior_dependencies.keys() - {"solana-program-test"}:
            self.assertEqual(prior_dependencies[name], successor_dependencies[name])
        prior_target = copy.deepcopy(prior_dependencies["solana-program-test"])
        successor_target = copy.deepcopy(successor_dependencies["solana-program-test"])
        prior_target["features"] = successor_target["features"]
        self.assertEqual(prior_target, successor_target)

    def test_all_other_construction_surfaces_preserved(self) -> None:
        policy = self.policy()
        prior = AUTHOR.verify_inputs(policy)["prior_binding"]
        successor = AUTHOR.build_binding(policy)
        preserved = [
            "selected_dependencies", "selector_closure", "carried_assessment_ceiling", "workstreams",
            "planned_targets", "preserved_surfaces", "local_conformance", "forbidden_capabilities", "security_posture"
        ]
        for key in preserved:
            self.assertEqual(prior[key], successor[key], key)

    def test_candidate_has_no_authority_or_effect(self) -> None:
        binding = AUTHOR.build_binding()
        self.assertEqual("none", binding["authority_effect"])
        self.assertEqual("none", binding["implementation_effect"])
        self.assertEqual("none", binding["external_effect"])
        self.assertEqual("not_evaluable", binding["construction_gate"]["binding_acceptance"])
        self.assertEqual("not-authorized-by-this-successor-candidate", binding["construction_gate"]["implementation"])

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

    def test_cached_manifest_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["cached_source_evidence"]["cargo_manifest_sha256"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_cached_crate_root_drift_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["cached_source_evidence"]["crate_root_sha256"] = "0" * 64
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_feature_omission_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["exact_feature_repair"]["to"] = []
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_extra_feature_fails_closed(self) -> None:
        mutated = self.policy()
        mutated["exact_feature_repair"]["to"].append("unexpected")
        with self.assertRaises(AUTHOR.BindingError):
            AUTHOR.build_binding(mutated)

    def test_preacceptance_collects_dependent_not_evaluable_checks(self) -> None:
        binding_raw = AUTHOR.canonical_bytes(AUTHOR.build_binding())
        receipt = AUTHOR.build_preacceptance(binding_raw)
        checks = {item["check_id"]: item for item in receipt["checks"]}
        self.assertEqual("not_evaluable", checks["successor-binding-acceptance"]["status"])
        self.assertEqual("not_evaluable", checks["implementation-conformance"]["status"])
        self.assertEqual("not_evaluable", checks["production-security-approval"]["status"])
        self.assertEqual("not_evaluable", checks["devnet-evidence"]["status"])


if __name__ == "__main__":
    unittest.main()
