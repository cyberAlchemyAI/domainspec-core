#!/usr/bin/env python3
"""Compile deterministic Implementation Readiness evidence for the selected SWU."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[7]
OUT = Path(__file__).resolve().parent
WORK_PACK = OUT.parent / "WORK-PACK.md"
CONTRACTS_PATH = REPO / ".agents/skills/implementation-readiness/scripts/execution_contracts.py"


def load_contracts():
    spec = importlib.util.spec_from_file_location("whisper_readiness_contracts", CONTRACTS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load execution contracts")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(name: str, value: dict) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    contracts = load_contracts()
    material = [
        "projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/synthesis-revision-3.md",
        "projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/state.schema.json",
        "projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/event-sequence.json",
        "projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/negative-fixtures.json",
        "projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/validate-state-contract.mjs",
        "projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/receipts/state-contract-validation.json",
    ]
    terminal = "projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/development/state-contract-repair/execution/task-session-terminal-receipt.json"
    route = {
        "route_id": "route:whisper-research-state-contract-repair",
        "frontier_swu": "SWU-WHISPER-RSCH-STATE-001",
        "capability": "task-session",
        "mode": "execute",
        "target": "projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/development/state-contract-repair/work-pack/tasks/TASK-WHISPER-RSCH-STATE-001.md",
        "write_scope": material + [terminal],
        "effect_class": "repository-local-reversible",
        "required_inputs": [
            "WORK-PACK.md",
            "work-pack/tasks/TASK-WHISPER-RSCH-STATE-001.md",
            "readiness/CONTEXT-PACK.json",
            "readiness/material-package.json",
            "readiness/material-producer-receipt.json",
        ],
        "expected_receipt": terminal,
    }
    policy = {
        "schema_version": "1.0.0",
        "work_pack_id": "WP-WHISPER-RSCH-STATE-001",
        "work_pack_semantic_digest": hashlib.sha256(WORK_PACK.read_bytes()).hexdigest(),
        "frontier": ["SWU-WHISPER-RSCH-STATE-001"],
        "allowed_routes": [route],
        "allowed_routes_digest": contracts.allowed_routes_digest([route]),
        "automatic_decisions": ["internal-tool-selection", "reversible-local-default"],
        "stop_decisions": [
            "scope-expansion",
            "destructive-or-irreversible-effect",
            "credentials-or-secret-access",
            "external-message-or-network-effect",
            "authority-promotion-publication-deployment",
            "failed-acceptance-critical-validation",
        ],
        "validation_commands": [
            "node projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/validate-state-contract.mjs",
            "node projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/state-contract/validate-state-contract.mjs --self-test",
            "python3 -m json.tool projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/receipts/state-contract-validation.json",
        ],
        "scope_source": "exact-work-pack-and-captured-frontier",
        "validation_policy": "owner-gates-remain-mandatory",
        "authority_effect": "none",
    }
    entry = {
        "schema_version": "1.0.0",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "entry_state": "task-ready",
        "selected_unit": "SWU-WHISPER-RSCH-STATE-001",
        "route_id": route["route_id"],
        "next_owner": {"capability": "task-session", "mode": "execute", "target": route["target"]},
        "blocker_code": None,
        "authority_effect": "none",
    }
    binding = contracts.build_execution_intent_binding(
        policy,
        entry,
        source_invocation_id="invoke:whisper-state-contract-repair:20260806T024957Z",
        created_at="2026-08-06T02:49:57Z",
        execution_mode="one-unit",
    )
    request = {
        "schema_version": "1.0.0",
        "execution_policy": policy,
        "execution_entry": entry,
        "execution_binding": binding,
        "selected_unit": {"work_pack_id": policy["work_pack_id"], "swu_id": "SWU-WHISPER-RSCH-STATE-001"},
        "authority_effect": "none",
    }
    write_json("execution-policy.json", policy)
    write_json("execution-entry.json", entry)
    write_json("execution-intent-binding.json", binding)
    write_json("fast-entry-request.json", request)
    print("implementation-readiness-contracts-pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
