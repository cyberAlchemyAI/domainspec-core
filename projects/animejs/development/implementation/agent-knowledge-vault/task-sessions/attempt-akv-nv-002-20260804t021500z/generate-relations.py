#!/usr/bin/env python3
"""Project the reviewed 25-row relation matrix into the closed stored vocabulary."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[7]
ATTEMPT = Path(__file__).resolve().parent
TARGET = ATTEMPT / "producer/staged/projects/animejs/ontology/agent-knowledge-vault/contracts"
MATRIX = ROOT / "projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-relation-behavior-witness-matrix.json"
SYNTHESIS = ROOT / "projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/knowledge-vault-synthesis-reviewer-repair.json"


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def kinds(raw: str) -> list[str]:
    if raw == "same exact kind as source":
        return ["$same-as-source"]
    return sorted({part.split("[")[0] for part in raw.split("|")})


matrix = json.loads(MATRIX.read_text())
review = json.loads(SYNTHESIS.read_text())
rows = matrix.get("rows", matrix)
endpoint_by_name = {row["name"]: row for row in review["closed_relation_vocabulary"]}
merge_representation = {
    "AKV-REL-009": "WorkEpisode.task_id canonical; addresses derived and never stored",
    "AKV-REL-011": "Attempt.episode_id canonical; WorkEpisode.attempt_ids is a sorted derived index; contains never stored",
    "AKV-REL-018": "Outcome.attempt_id canonical; Attempt.outcome_id is a unique reverse-derived lookup; yields never stored",
    "AKV-REL-024": "NextQuestion.gap_id canonical; QueryReceipt.next_question_ids is derived; suggestsNextQuestion never stored",
    "AKV-REL-025": "QueryReceipt.evidence_record_ids canonical; citesEvidence never stored",
}

vocabulary_rows = []
decision_rows = []
for row in rows:
    endpoint = endpoint_by_name[row["relation_name"]]
    decision = {
        "relation_id": row["relation_id"],
        "name": row["relation_name"],
        "disposition": row["disposition"],
        "consumer": row["consumer"],
        "reason": row["rationale"],
        "canonical_representation": (
            "stored-edge"
            if row["disposition"] == "RETAIN"
            else merge_representation.get(row["relation_id"], "deferred-residue; stored edge forbidden")
        ),
    }
    decision_rows.append(decision)
    if row["disposition"] != "RETAIN":
        continue
    vocabulary_rows.append({
        "relation_id": row["relation_id"],
        "name": row["relation_name"],
        "source_kinds": kinds(endpoint["source"]),
        "target_kinds": kinds(endpoint["target"]),
        "source_contract": endpoint["source"],
        "target_contract": endpoint["target"],
        "cardinality": endpoint["cardinality"],
        "consumer": row["consumer"],
        "mutation": row["mutation"],
        "expected_mutant_delta": row["expected_mutant_delta"],
        "failure_assertion": row["failure_assertion"],
    })

write(TARGET / "relation-vocabulary.json", {
    "schema_version": "animejs.agent-knowledge-vault.relation-vocabulary.v1",
    "representation": "stored-directed-edge",
    "relation_count": len(vocabulary_rows),
    "relations": vocabulary_rows,
})
write(TARGET / "relation-decisions.json", {
    "schema_version": "animejs.agent-knowledge-vault.relation-decisions.v1",
    "source_matrix": MATRIX.relative_to(ROOT).as_posix(),
    "counts": {"RETAIN": 17, "MERGE": 5, "DEFER": 3, "KILL": 0},
    "decisions": decision_rows,
    "stored_edge_policy": "Only RETAIN rows may appear in graph.edges; MERGE rows use the named canonical field and DEFER rows remain explicit residue.",
})
print(f"generated {len(vocabulary_rows)} stored relations and {len(decision_rows)} decisions")
