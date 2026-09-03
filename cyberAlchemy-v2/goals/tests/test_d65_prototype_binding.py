#!/usr/bin/env python3
"""Hostile checks for the Goals D65 prototype-construction binding."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PACKAGE_ROOT / "scripts/validate_prototype_construction_binding.py"
SPEC = importlib.util.spec_from_file_location("goals_d65_binding", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PrototypeConstructionBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = MODULE.load(MODULE.REGISTRY_PATH)
        cls.projects = {
            doc["project_id"]: doc
            for path in sorted((PACKAGE_ROOT / "projects").glob("*/project.json"))
            for doc in [MODULE.load(path)]
        }
        cls.goals = {
            doc["goal_id"]: doc
            for path in sorted((PACKAGE_ROOT / "projects").glob("*/goals/*.goal.json"))
            for doc in [MODULE.load(path)]
        }
        cls.upstream = MODULE.load(MODULE.UPSTREAM_CONSTRUCTIONS_PATH)
        cls.scaffolds = MODULE.load(MODULE.UPSTREAM_SCAFFOLDS_PATH)

    def validate(self, registry=None, projects=None, upstream=None, scaffolds=None):
        return MODULE.validate_documents(
            registry or copy.deepcopy(self.registry),
            projects or copy.deepcopy(self.projects),
            copy.deepcopy(self.goals),
            upstream or copy.deepcopy(self.upstream),
            scaffolds or copy.deepcopy(self.scaffolds),
        )

    def test_current_binding_passes(self):
        self.assertEqual(self.validate(), [])

    def test_empty_registry_is_not_pass(self):
        registry = copy.deepcopy(self.registry)
        registry["bindings"] = []
        self.assertTrue(any("non-vacuous" in error for error in self.validate(registry=registry)))

    def test_stale_candidate_manifest_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["bindings"][0]["prototype_contract"]["candidate_manifest_sha256"] = "0" * 64
        self.assertTrue(any("manifest" in error for error in self.validate(registry=registry)))

    def test_preapproval_authority_request_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["bindings"][0]["authority_request_refs"] = ["CA2-AUTHORITY-PREMATURE"]
        self.assertTrue(any("preapproval authority" in error for error in self.validate(registry=registry)))

    def test_scaffold_must_remain_non_authoritative(self):
        scaffolds = copy.deepcopy(self.scaffolds)
        scaffolds["scaffolds"][0]["canonicality"] = "authoritative"
        self.assertTrue(any("non-authoritative" in error for error in self.validate(scaffolds=scaffolds)))

    def test_project_reference_must_close(self):
        projects = copy.deepcopy(self.projects)
        projects["CA2-PROJECT-CYBERALCHEMY-LAB-ONTOLOGY-LIFECYCLE"]["construction_binding_refs"] = []
        self.assertTrue(any("bidirectionally" in error for error in self.validate(projects=projects)))

    def test_unbuilt_product_stage_cannot_be_inflated(self):
        registry = copy.deepcopy(self.registry)
        registry["bindings"][0]["stage_states"]["implementation"] = "tested"
        self.assertTrue(any("exceeds current evidence" in error for error in self.validate(registry=registry)))


if __name__ == "__main__":
    unittest.main()
