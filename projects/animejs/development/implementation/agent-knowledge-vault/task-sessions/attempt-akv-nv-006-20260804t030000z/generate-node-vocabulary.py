#!/usr/bin/env python3
"""Project the reviewed closed node vocabulary into the candidate contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[7]
ATTEMPT = Path(__file__).resolve().parent
SOURCE = ROOT / "projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/knowledge-vault-synthesis-reviewer-repair.json"
TARGET = ATTEMPT / "producer/staged/projects/animejs/ontology/agent-knowledge-vault/contracts/node-vocabulary.json"

review = json.loads(SOURCE.read_text())
closed = review["closed_node_vocabulary"]
rows = []
for row in closed["rows"]:
    rows.append({
        "kind": row["kind"],
        "invariant": row["invariant"],
        "required_fields": row["required_fields"],
        "evidence_class": row["evidence_class"],
        "validity": row["validity"],
        "owner_route": row["owner_route"],
        "misuse_warning": row["misuse_warning"],
    })
TARGET.parent.mkdir(parents=True, exist_ok=True)
TARGET.write_text(json.dumps({
    "schema_version": "animejs.agent-knowledge-vault.node-vocabulary.v1",
    "node_kind_count": len(rows),
    "common_required_fields": closed["common_required_fields"],
    "node_kinds": rows,
}, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
print(f"generated {len(rows)} closed node kinds")
