#!/usr/bin/env python3
"""Fail closed when LLCP closeout exact references cannot be emitted in order."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[9]
SIDE_ROOT = Path(__file__).resolve().parents[1]
PLAN_ROOT = REPO_ROOT / (
    "projects/lucifers-lights/development/refinement-runs/"
    "20260821T145606Z-chapter-production-pipeline/stages/09-invoke-plan"
)


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected object: {path}")
    return value


def has_cycle(graph: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dependency in graph[node]:
            if dependency not in graph or visit(dependency):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def order_satisfies(order: list[str], graph: dict[str, list[str]]) -> bool:
    positions = {node: index for index, node in enumerate(order)}
    return set(positions) == set(graph) and all(
        positions[dependency] < positions[node]
        for node, dependencies in graph.items()
        for dependency in dependencies
    )


def reverse_continuation_delta(candidate: dict[str, object]) -> dict[str, object]:
    restored = copy.deepcopy(candidate)
    restored.pop("description", None)
    restored["$id"] = "https://lucifers-lights.local/schemas/continuation-state/1-0-0"
    required = restored["required"]
    assert isinstance(required, list)
    required[required.index("terminal_receipt_path")] = "terminal_receipt_ref"
    properties = restored["properties"]
    assert isinstance(properties, dict)
    properties["terminal_receipt_ref"] = {"$ref": "#/$defs/exactArtifactRef"}
    del properties["terminal_receipt_path"]
    return restored


def reverse_owner_delta(candidate: dict[str, object]) -> dict[str, object]:
    restored = copy.deepcopy(candidate)
    restored.pop("description", None)
    restored["$id"] = (
        "https://lucifers-lights.local/schemas/"
        "invoke-refresh-closeout-receipt/1-0-0"
    )
    required = restored["required"]
    assert isinstance(required, list)
    required[required.index("continuation_state_path")] = "continuation_state_ref"
    required[
        required.index("router_verification_receipt_path")
    ] = "router_verification_receipt_ref"
    properties = restored["properties"]
    assert isinstance(properties, dict)
    properties["continuation_state_ref"] = {
        "allOf": [
            {"$ref": "#/$defs/exactArtifactRef"},
            {
                "properties": {
                    "path": {
                        "pattern": (
                            "^projects/lucifers-lights/development/"
                            "chapter-pipeline-evidence/SWU-LLCP-00[1-5]/"
                            "attempts/attempt-[0-9]{3}/CONTINUATION\\.json$"
                        )
                    }
                }
            },
        ]
    }
    properties["router_verification_receipt_ref"] = {
        "allOf": [
            {"$ref": "#/$defs/exactArtifactRef"},
            {
                "properties": {
                    "path": {
                        "pattern": (
                            "^projects/lucifers-lights/development/"
                            "chapter-pipeline-evidence/SWU-LLCP-00[1-5]/"
                            "attempts/attempt-[0-9]{3}/"
                            "CONTINUATION-ROUTE-RECEIPT\\.json$"
                        )
                    }
                }
            },
        ]
    }
    del properties["continuation_state_path"]
    del properties["router_verification_receipt_path"]
    return restored


class CloseoutReferenceDagTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.live_continuation = load(
            PLAN_ROOT / "schemas/llcp-continuation-state.schema.json"
        )
        cls.live_owner = load(
            PLAN_ROOT / "schemas/llcp-invoke-refresh-closeout-receipt.schema.json"
        )
        cls.candidate_continuation = load(
            SIDE_ROOT / "candidate/schemas/llcp-continuation-state.schema.json"
        )
        cls.candidate_owner = load(
            SIDE_ROOT
            / "candidate/schemas/llcp-invoke-refresh-closeout-receipt.schema.json"
        )
        cls.contract = load(SIDE_ROOT / "candidate/REFERENCE-ORDER-CONTRACT.json")

    def test_live_contract_has_cycle(self) -> None:
        live_graph = {
            "invoke_owner": ["continuation_router", "continuation_state"],
            "continuation_router": ["invoke_owner"],
            "continuation_state": [
                "invoke_owner",
                "continuation_router",
                "task_session_terminal",
            ],
            "task_session_terminal": ["invoke_owner", "continuation_state"],
        }
        self.assertTrue(has_cycle(live_graph))

    def test_candidate_deltas_are_minimal_and_schemas_are_valid(self) -> None:
        Draft202012Validator.check_schema(self.candidate_continuation)
        Draft202012Validator.check_schema(self.candidate_owner)
        self.assertEqual(
            reverse_continuation_delta(self.candidate_continuation),
            self.live_continuation,
        )
        self.assertEqual(reverse_owner_delta(self.candidate_owner), self.live_owner)

    def test_candidate_exact_reference_graph_is_acyclic(self) -> None:
        graph = self.contract["exact_reference_dependencies"]
        order = self.contract["emission_order"]
        self.assertIsInstance(graph, dict)
        self.assertIsInstance(order, list)
        assert isinstance(graph, dict)
        assert isinstance(order, list)
        self.assertFalse(has_cycle(graph))
        self.assertTrue(order_satisfies(order, graph))
        self.assertEqual(
            order,
            [
                "precloseout_execution",
                "invoke_owner",
                "continuation_router",
                "continuation_state",
                "task_session_terminal",
            ],
        )

    def test_future_edges_are_paths_and_downstream_edges_remain_exact(self) -> None:
        owner_required = self.candidate_owner["required"]
        continuation_required = self.candidate_continuation["required"]
        assert isinstance(owner_required, list)
        assert isinstance(continuation_required, list)
        self.assertIn("continuation_state_path", owner_required)
        self.assertIn("router_verification_receipt_path", owner_required)
        self.assertNotIn("continuation_state_ref", owner_required)
        self.assertNotIn("router_verification_receipt_ref", owner_required)
        self.assertIn("terminal_receipt_path", continuation_required)
        self.assertNotIn("terminal_receipt_ref", continuation_required)
        self.assertIn("invoke_closeout_receipt_ref", continuation_required)
        self.assertIn("router_verification_receipt_ref", continuation_required)


if __name__ == "__main__":
    unittest.main(verbosity=2)
