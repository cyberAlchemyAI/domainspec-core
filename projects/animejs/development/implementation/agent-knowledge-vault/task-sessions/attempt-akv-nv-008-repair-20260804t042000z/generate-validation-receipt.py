#!/usr/bin/env python3
"""Bind the complete candidate inventory except the recursively self-bound receipt."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[7]
ATTEMPT = Path(__file__).resolve().parent
LIVE = ROOT / "projects/animejs/ontology/agent-knowledge-vault"
STAGED = ATTEMPT / "producer/staged/projects/animejs/ontology/agent-knowledge-vault"
NEW_PATHS = {
    "scripts/validate.mjs",
    "tests/ontology.test.mjs",
    "README.md",
    "RESIDUE.json",
}


def identity(path: Path, logical: str) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": logical, "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


logical_paths = {
    path.relative_to(LIVE).as_posix()
    for path in LIVE.rglob("*")
    if path.is_file() and path.relative_to(LIVE).as_posix() != "receipts/validation-receipt.json"
} | NEW_PATHS
artifacts = []
for logical in sorted(logical_paths):
    source = STAGED / logical if logical in NEW_PATHS else LIVE / logical
    artifacts.append(identity(source, logical))

nodes = json.loads((LIVE / "nodes/nodes.json").read_text())
docs = json.loads((LIVE / "sources/documentation-manifest.json").read_text())
repo = json.loads((LIVE / "sources/repository-manifest.json").read_text())
receipt = {
    "schema_version": "animejs.agent-knowledge-vault.validation-receipt.v1",
    "receipt_id": "animejs-akv-validation-20260804t042000z",
    "package_id": "animejs-agent-knowledge-vault",
    "status": "candidate-local-binding-complete",
    "graph_digest": nodes["graph_digest"],
    "plan_epoch_id": "epoch-acd0e4afd662c4598d70372d",
    "source_manifests": {
        "documentation": docs["semantic_jsonl_sha256"],
        "repository": repo["manifest_jsonl_sha256"],
    },
    "coverage": {
        "documentation_routes": 418,
        "documentation_families": 16,
        "repository_rows": 348,
        "nodes": 1185,
        "relations": 418,
        "search_entries": 766,
        "verified_operational_lessons": 0,
    },
    "validation_contracts": [
        "node projects/animejs/ontology/agent-knowledge-vault/scripts/validate.mjs",
        "node projects/animejs/ontology/agent-knowledge-vault/tests/ontology.test.mjs",
    ],
    "bound_artifact_count": len(artifacts),
    "bound_artifacts": artifacts,
    "self_binding": "excluded-to-avoid-recursive-digest; exact receipt identity is bound by the terminal Task Session receipt",
    "authority_effect": "none",
    "release_admission": "not-granted",
    "publication_class": "internal",
    "residue_ref": "RESIDUE.json",
}
target = STAGED / "receipts/validation-receipt.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
print(f"bound {len(artifacts)} candidate artifacts")
